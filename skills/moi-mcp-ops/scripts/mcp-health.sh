#!/usr/bin/env bash
# mcp-health.sh: read-only health check of the hosted MOI MCP server from outside.
#
# Usage:   bash "$SKILLS/moi-mcp-ops/scripts/mcp-health.sh" [options]
#          SKILLS is the folder that holds the moi-* skills. It can run from anywhere: it reads no file.
#   --env prod|dev       which hosted pair to check (default prod). dev uses the dev-mcp hosts.
#   --write-host HOST    check this write gateway host instead (for example a PR preview host)
#   --read-host HOST     check this read gateway host instead
#   --no-read            skip the read gateway (a PR preview may have none)
#   --no-rpc             skip the two devnet RPC net.Version reads
#   --github             also read the public GitHub state of sarvalabs/moi-mcp: open chain-canary and
#                        upstream-release issues, and the latest scheduled canary and watch runs.
#                        No credential is sent, so GitHub allows about 60 such requests an hour.
#   --expect-write N     tools the write gateway should list (default 13, the count live on 2026-10-03)
#   --expect-read N      tools the read gateway should list (default 6, the count live on 2026-10-03)
#   --timeout SECONDS    per request, 1 to 60 (default 15)
#   --selftest           check the secret masking and the host rule on strings built at run time; no network
#   -h, --help
# Checks per gateway: /health; for the write gateway also the OAuth issuer, the protected-resource
#   metadata, and that a wallet tool answers 401 without a token; then tools/list, a ping call and a
#   moi_resolve_agent call (the registry read). Then net.Version on the /devnet/ and /babylon/ RPC paths.
# Only these requests are ever made: GET, a JSON-RPC tools/list, a tools/call of ping,
#   moi_resolve_agent or moi_wallet_status (without a token), and a JSON-RPC net.Version. Nothing signs,
#   writes, pairs a wallet, signs in or spends. No redirect is followed and no credential is sent.
# Output:  PASS, WARN or FAIL per line, each starting with the host called, then a summary. A WARN is a
#   fact to read, not a failure. Text taken from a response, and any bad argument echoed in a usage error,
#   is masked (long hex, key prefixes, JWTs, recovery-phrase-shaped word runs) before it is cut short.
#   The script prints host names, never a URL. It reads no file and writes no file.
# Exit:    0 no FAIL, 1 at least one FAIL, 2 bad usage (a clear message, no traceback),
#          3 unexpected internal error (a script fault, not a finding about the server).
# Python 3 standard library only. Works under bash 3.2 and zsh (run it with bash).

command -v python3 >/dev/null 2>&1 || { echo "mcp-health.sh needs python3 on the PATH" >&2; exit 2; }
exec python3 - "$@" <<'PY'
import argparse
import datetime
import http.client as httpclient
import io
import json
import os
import re
import socket
import ssl
import sys
import urllib.error
import urllib.request

DEFAULT_WRITE = {"prod": "mcp.voyage.moi.technology", "dev": "dev-mcp.voyage.moi.technology"}
DEFAULT_READ = {"prod": "mcp-read.voyage.moi.technology", "dev": "dev-mcp-read.voyage.moi.technology"}
RPC_HOST = "dev.voyage-rpc.moi.technology"
RPC_PATHS = ("devnet", "babylon")
GITHUB_HOST = "api.github.com"
REPO = "sarvalabs/moi-mcp"
SAFE_TOOLS = ("ping", "moi_resolve_agent", "moi_wallet_status")
HOST_RX = re.compile(r"^(?=.{4,253}\Z)([A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}\Z")
TOOL_RX = re.compile(r"^[a-z0-9_]{1,40}$")

# ---- masking: same shapes as moi-devrel/claim-check/scripts/ledger-status.py, applied before any cut ----
LONG_HEX = re.compile(r"0x[0-9A-Fa-f]{17,}|[0-9A-Fa-f]{24,}")
SECRET_SHAPES = [re.compile(p) for p in (
    r"\bsk-[A-Za-z0-9_-]{8,}",
    r"\bgsk_[A-Za-z0-9]{12,}",
    r"\bAIza[0-9A-Za-z_-]{20,}",
    r"\b(?:AKIA|ASIA)[0-9A-Z]{12,}",
    r"\b(?:sk|rk)_live_[0-9A-Za-z]{8,}",
    r"\bnpm_[A-Za-z0-9]{20,}",
    r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{16,}|\bgithub_pat_[A-Za-z0-9_]{16,}",
    r"\bxox[abprso]-[A-Za-z0-9-]{8,}",
    r"https://hooks\.slack\.com/services/\S+",
    r"https://(?:ptb\.|canary\.)?discord(?:app)?\.com/api/webhooks/\S+",
    r"\b\d{8,10}:[A-Za-z0-9_-]{30,}",
    r"-----BEGIN (?:[A-Z]+ )*PRIVATE KEY(?: BLOCK)?-----",
    r"\beyJ[A-Za-z0-9_-]{6,}\.eyJ[A-Za-z0-9_-]{6,}\.[A-Za-z0-9_-]{6,}",
    r"(?<![A-Za-z0-9+/=])(?=[A-Za-z0-9+/=]*[A-Za-z])(?=[A-Za-z0-9+/=]*\d)[A-Za-z0-9+/=]{32,}",
)]
PHRASE_MIN = 12
PHRASE_STOP = frozenset(
    "after and are been being both but could did does each every for from get got had has her here "
    "him his how its let many may most not our out per see she should some than the their them these "
    "those too using via was were which while who why with would yes your".split())
_PIECE = re.compile(r"[A-Za-z]+|[^A-Za-z]+")


def _mask_phrases(s):
    spans, run = [], []

    def close():
        if len(run) >= PHRASE_MIN:
            spans.append((run[0][1], run[-1][2]))
        del run[:]

    for m in _PIECE.finditer(s):
        text = m.group(0)
        if text[0].isalpha():
            if 3 <= len(text) <= 8 and text.lower() not in PHRASE_STOP:
                run.append((text, m.start(), m.end()))
            else:
                close()
        elif re.fullmatch(r"[\s,;]+", text):
            continue
        else:
            close()
    close()
    for a, b in reversed(spans):
        s = s[:a] + "(masked: 12 or more short words, possible recovery phrase)" + s[b:]
    return s


def mask(s):
    s = str(s)
    s = LONG_HEX.sub(lambda m: m.group(0)[:6] + "...(masked)", s)
    for rx in SECRET_SHAPES:
        s = rx.sub(lambda m: m.group(0)[:4] + "...(masked)", s)
    return _mask_phrases(s)


def ex(s, n=160):
    """Text from a response or an error: masked first, then made one line, then cut."""
    s = " ".join(mask(s).split())
    return s if len(s) <= n else s[: n - 3] + "..."


def tool_label(name):
    """A tool name from a response, masked like everything else. Anything that is not a plain name shows as ?."""
    return ex(name, 40) if isinstance(name, str) and TOOL_RX.match(name) else "?"


def redirect_host(location):
    """The host a Location header names. Any user:password part is dropped, never printed."""
    m = re.match(r"https?://(?:[^/@?#]*@)?([^/:?#]+)", location or "")
    return m.group(1) if m else None


class MaskedParser(argparse.ArgumentParser):
    """argparse echoes a bad value in its error. Here the message is masked first, and the exit code is 2."""

    def error(self, message):
        self.print_usage(sys.stderr)
        hint = ""
        if message.startswith("unrecognized arguments"):
            hint = ". This script reads no file and takes no path: use only the options above."
        sys.stderr.write("%s: error: %s%s\n" % (self.prog, mask(message), hint))
        sys.exit(2)


# ---- output ----
counts = {"PASS": 0, "WARN": 0, "FAIL": 0}
hosts_called = []


def say(level, host, msg):
    counts[level] += 1
    print("%-4s %s: %s" % (level, ex(host, 80), msg))


def note(msg):
    print("     " + msg)


class Unreachable(Exception):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def ssl_context():
    """Verifying context. Some python.org builds on macOS ship no CA list, so fall back to the system one. Never unverified."""
    ctx = ssl.create_default_context()
    if ctx.cert_store_stats().get("x509_ca", 0) == 0 and not os.environ.get("SSL_CERT_FILE"):
        for p in ("/etc/ssl/cert.pem", "/etc/ssl/certs/ca-certificates.crt", "/etc/pki/tls/certs/ca-bundle.crt"):
            if os.path.isfile(p):
                try:
                    ctx.load_verify_locations(p)
                    break
                except (OSError, ssl.SSLError):
                    continue
    return ctx


OPENER = urllib.request.build_opener(NoRedirect, urllib.request.HTTPSHandler(context=ssl_context()))
TIMEOUT = 15


def describe(e):
    if isinstance(e, socket.gaierror):
        return "the name does not resolve"
    if isinstance(e, ssl.SSLCertVerificationError):
        return "the TLS certificate did not verify: the host's certificate, or this machine's CA list"
    if isinstance(e, ssl.SSLError):
        return "TLS error"
    if isinstance(e, (socket.timeout, TimeoutError)):
        return "timed out after %ss" % TIMEOUT
    if isinstance(e, httpclient.IncompleteRead):
        return "the server closed the connection before it finished its answer"
    if isinstance(e, httpclient.HTTPException) and not isinstance(e, OSError):
        return "the server did not answer in HTTP"
    return ex(e, 80)


def http(host, path, body=None, extra=None):
    """One request. Returns (status, headers, text). Raises Unreachable. HTTPS only, no redirect, no credential."""
    if host not in hosts_called:
        hosts_called.append(host)
    hdrs = {"User-Agent": "moi-mcp-health/1.0", "Accept": "application/json"}
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        hdrs["Content-Type"] = "application/json"
        hdrs["Accept"] = "application/json, text/event-stream"
    if extra:
        hdrs.update(extra)
    req = urllib.request.Request("https://" + host + path, data=data, headers=hdrs,
                                 method="POST" if body is not None else "GET")
    try:
        with OPENER.open(req, timeout=TIMEOUT) as r:
            return r.status, dict(r.headers), r.read(2_000_000).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        try:
            text = e.read(2_000_000).decode("utf-8", "replace")
        except Exception:
            text = ""
        return e.code, dict(e.headers or {}), text
    except urllib.error.URLError as e:
        raise Unreachable(describe(e.reason))
    except (OSError, ValueError, httpclient.HTTPException) as e:
        raise Unreachable(describe(e))


def jbody(text):
    """A JSON object, or None."""
    try:
        v = json.loads(text)
    except (ValueError, RecursionError):
        return None
    return v if isinstance(v, dict) else None


def rpc_answer(text):
    """A JSON-RPC answer sent as plain JSON or as server-sent events (the last data: line)."""
    last = None
    for line in text.splitlines():
        if line.startswith("data:"):
            try:
                last = json.loads(line[5:].strip())
            except (ValueError, RecursionError):
                pass
    if isinstance(last, dict):
        return last
    return jbody(text.strip())


def tool_call(host, name, arguments):
    assert name in SAFE_TOOLS, "this script only calls read tools"
    body = {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": name, "arguments": arguments}}
    return http(host, "/mcp", body)


def tool_text(result):
    parts = []
    for c in (result or {}).get("content") or []:
        if isinstance(c, dict) and isinstance(c.get("text"), str):
            parts.append(c["text"])
    return " ".join(parts)


# ---- the checks ----
def check_gateway(host, kind, expect):
    try:
        st, hd, tx = http(host, "/health")
    except Unreachable as e:
        say("FAIL", host, "health: unreachable (%s). Further checks skipped. DNS, TLS, nginx or the VM: ASK: Upendhar" % e)
        return
    if 300 <= st < 400:
        target = redirect_host(hd.get("Location") or hd.get("location") or "")
        say("FAIL", host, "health: redirect (HTTP %d) to %s. A redirect in front of a gateway drops the Authorization header "
                          "and breaks sign-in. Further checks skipped" % (st, ex(target, 60) if target else "somewhere"))
        return
    j = jbody(tx)
    if st != 200 or not j or j.get("ok") is not True:
        hint = ""
        if st in (502, 503, 504):
            hint = {502: " The process is down or nginx points at the wrong port: pm2 status on the VM (ASK: Upendhar).",
                    503: " The shared config failed to load: the error log names the variable (ASK: Upendhar).",
                    504: " nginx timed out waiting for the process (ASK: Upendhar)."}[st]
        say("FAIL", host, "health: HTTP %d, ok is not true.%s Further checks skipped" % (st, hint))
        return
    say("PASS", host, "health ok (network %s, readOnly %s)" % (ex(j.get("network"), 20), ex(j.get("readOnly"), 8)))
    want_ro = kind == "read"
    if j.get("readOnly") is not want_ro:
        say("WARN", host, "health says readOnly %s; a %s gateway should say %s" % (ex(j.get("readOnly"), 8), kind, str(want_ro).lower()))
    if kind == "write" and j.get("pairingMounted") is not True:
        say("WARN", host, "health says pairingMounted is not true: wallet pairing pages are not wired")

    if kind == "write":
        check_oauth(host)

    # tools/list
    try:
        st, hd, tx = http(host, "/mcp", {"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    except Unreachable as e:
        say("FAIL", host, "tools/list: unreachable (%s)" % e)
        return
    r = rpc_answer(tx)
    tools = (((r or {}).get("result") or {}).get("tools")) if r else None
    if st != 200 or not isinstance(tools, list) or not tools:
        say("FAIL", host, "tools/list: HTTP %d and no tool list (%s)" % (st, ex(tx, 80)))
        return
    names = [t.get("name") if isinstance(t, dict) else None for t in tools]
    shown = [tool_label(n) for n in names]
    if len(tools) == expect:
        say("PASS", host, "tools/list answers %d tools" % len(tools))
    else:
        say("WARN", host, "tools/list answers %d tools, expected %d. A deploy changes the count: say which build is live "
                          "(architecture.md) before treating it as a fault" % (len(tools), expect))
    note("tools: " + " ".join(shown))
    if "moi_get_account" not in names:
        say("FAIL", host, "tools/list does not include moi_get_account, which CI asserts")

    # ping
    try:
        st, hd, tx = tool_call(host, "ping", {})
        r = rpc_answer(tx)
        res = (r or {}).get("result") or {}
        sc = res.get("structuredContent") if isinstance(res.get("structuredContent"), dict) else {}
        if st == 200 and not res.get("isError") and sc:
            say("PASS", host, "ping answers (server %s, version %s, network %s)"
                % (ex(sc.get("server"), 40), ex(sc.get("version"), 20), ex(sc.get("network"), 20)))
            if kind == "write" and sc.get("readOnly") is True:
                note("ping says readOnly true even here (seen 2026-10-03): read the gateway kind from health, not from ping")
        else:
            say("FAIL", host, "ping call failed (HTTP %d: %s)" % (st, ex(tool_text(res) or tx, 100)))
    except Unreachable as e:
        say("FAIL", host, "ping call: unreachable (%s)" % e)

    # the registry read
    try:
        st, hd, tx = tool_call(host, "moi_resolve_agent", {"query": "agent"})
        r = rpc_answer(tx)
        res = (r or {}).get("result") or {}
        text = tool_text(res)
        if st == 200 and not res.get("isError"):
            say("PASS", host, "moi_resolve_agent answers: the registry read works")
        elif re.search(r"Could not load the MOI agent registry|account not found", text, re.I):
            say("WARN", host, "moi_resolve_agent fails with the stale-registry signature (the registry id is wiped or "
                              "MOI_READ_CALLER is unset). Registry reads do not work. ASK: Gokul for the current id. "
                              "Text: %s" % ex(text, 110))
        else:
            say("WARN", host, "moi_resolve_agent returned HTTP %d: %s" % (st, ex(text or tx, 110)))
    except Unreachable as e:
        say("FAIL", host, "moi_resolve_agent call: unreachable (%s)" % e)


def check_oauth(host):
    want = "https://" + host
    try:
        st, hd, tx = http(host, "/.well-known/oauth-authorization-server")
        j = jbody(tx) or {}
        issuer = j.get("issuer")
        if st == 200 and issuer == want:
            say("PASS", host, "oauth issuer equals the public host")
        elif isinstance(issuer, str) and issuer.startswith("http://localhost"):
            say("FAIL", host, "oauth issuer is localhost: PUBLIC_URL never reached the process, sign-in will loop")
        else:
            say("FAIL", host, "oauth discovery: HTTP %d and the issuer is not this host, so sign-in will loop" % st)
    except Unreachable as e:
        say("FAIL", host, "oauth discovery: unreachable (%s)" % e)

    # protected-resource metadata: claude.ai needs `resource` to equal the connector URL, /mcp included
    try:
        st, hd, tx = http(host, "/.well-known/oauth-protected-resource")
        res = (jbody(tx) or {}).get("resource")
        st2, hd2, tx2 = http(host, "/.well-known/oauth-protected-resource/mcp")
        if res == want + "/mcp" and st2 == 200:
            form = "ok"
        elif res == want:
            form = "bare origin"
        else:
            form = "unexpected"
        if form == "ok":
            say("PASS", host, "protected-resource metadata names the /mcp endpoint and is served at the /mcp path too")
        else:
            say("WARN", host, "protected-resource metadata: %s, and the /mcp path answers HTTP %d. The /mcp form is what PR #18 "
                              "(commit 93d4d9d) added so that claude.ai Connect does not spin; the deployed copy may predate "
                              "it (inferred). Test Connect by hand (connect-and-verify.md)"
                % ("resource is the bare origin" if form == "bare origin" else "resource has an unexpected value", st2))
    except Unreachable as e:
        say("FAIL", host, "protected-resource metadata: unreachable (%s)" % e)

    # a wallet tool without a token must be refused
    try:
        st, hd, tx = tool_call(host, "moi_wallet_status", {})
        if st == 401:
            hv = hd.get("WWW-Authenticate") or hd.get("www-authenticate") or ""
            m = re.search(r'resource_metadata="https?://[^"/]+([^"]*)"', hv)
            path = m.group(1) if m else ""
            say("PASS", host, "a wallet tool without a token is refused with 401")
            if not path.endswith("/oauth-protected-resource/mcp"):
                say("WARN", host, "the 401 challenge points at the root metadata document, not the /mcp one (same cause as "
                                  "the protected-resource WARN: the build predates PR #18, inferred)")
        else:
            say("WARN", host, "a wallet tool without a token answered HTTP %d, not 401; check by hand (connect-and-verify.md)" % st)
    except Unreachable as e:
        say("FAIL", host, "auth gate check: unreachable (%s)" % e)


def check_rpc():
    seen = {}
    why = []
    for p in RPC_PATHS:
        try:
            st, hd, tx = http(RPC_HOST, "/%s/" % p, {"jsonrpc": "2.0", "id": 1, "method": "net.Version", "params": []})
            j = jbody(tx) or {}
            seen[p] = j.get("result") if st == 200 and isinstance(j.get("result"), str) else None
        except Unreachable as e:
            seen[p] = None
            if str(e) not in why:
                why.append(str(e))
    shown = {p: (ex(v, 20) if v else "no answer") for p, v in seen.items()}
    if all(v is None for v in seen.values()):
        say("FAIL", RPC_HOST, "neither RPC path answered net.Version%s: every read tool will fail. ASK: Gokul"
            % (" (%s)" % "; ".join(why) if why else ""))
    elif any(v is None for v in seen.values()):
        say("WARN", RPC_HOST, "net.Version: %s. The hosted read gateway uses the /babylon/ path, the code default is /devnet/"
            % ", ".join("%s %s" % (p, shown[p]) for p in RPC_PATHS))
    elif seen["devnet"] != seen["babylon"]:
        say("WARN", RPC_HOST, "net.Version differs: devnet %s, babylon %s. Whether they are one chain is unknown. ASK: Gokul"
            % (shown["devnet"], shown["babylon"]))
    else:
        say("PASS", RPC_HOST, "net.Version %s on both the /devnet/ and /babylon/ paths (0.13.0 on 2026-10-03)" % shown["devnet"])


def gh_json(path):
    st, hd, tx = http(GITHUB_HOST, path, extra={"Accept": "application/vnd.github+json"})
    try:
        return st, json.loads(tx)
    except ValueError:
        return st, None


def check_github():
    for label in ("chain-canary", "upstream-release"):
        try:
            st, items = gh_json("/repos/%s/issues?labels=%s&state=open&per_page=20" % (REPO, label))
        except Unreachable as e:
            say("WARN", GITHUB_HOST, "%s issues not read (%s)" % (label, e))
            continue
        if st in (403, 429):
            say("WARN", GITHUB_HOST, "GitHub refused the read (HTTP %d, probably the unauthenticated rate limit). Try later" % st)
            return
        if st != 200 or not isinstance(items, list):
            say("WARN", GITHUB_HOST, "%s issues not read (HTTP %d)" % (label, st))
            continue
        issues = [i for i in items if isinstance(i, dict) and "pull_request" not in i]
        if not issues:
            say("PASS", GITHUB_HOST, "no open %s issue in %s" % (label, REPO))
            continue
        say("WARN", GITHUB_HOST, "%d open %s issue(s) in %s. Triage them: watch-and-canary.md" % (len(issues), label, REPO))
        for i in issues[:5]:
            note("#%s opened %s: %s" % (ex(i.get("number"), 8), ex((i.get("created_at") or "")[:10], 10), ex(i.get("title"), 80)))
    try:
        st, d = gh_json("/repos/%s/actions/runs?per_page=30&event=schedule" % REPO)
    except Unreachable as e:
        say("WARN", GITHUB_HOST, "scheduled runs not read (%s)" % e)
        return
    runs = d.get("workflow_runs") if isinstance(d, dict) else None
    if st != 200 or not isinstance(runs, list):
        say("WARN", GITHUB_HOST, "scheduled runs not read (HTTP %d)" % st)
        return
    now = datetime.datetime.now(datetime.timezone.utc)
    for name in ("Chain canary", "Upstream watch"):
        mine = [r for r in runs if isinstance(r, dict) and r.get("name") == name]
        if not mine:
            say("WARN", GITHUB_HOST, "no scheduled run of '%s' in the latest 30 scheduled runs. Check Actions" % name)
            continue
        r = mine[0]
        try:
            when = datetime.datetime.strptime(r.get("created_at", ""), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
            age = (now - when).total_seconds() / 3600.0
        except ValueError:
            age = None
        ok = r.get("conclusion") == "success"
        txt = "latest scheduled '%s' run: %s, %s" % (name, ex(r.get("conclusion") or r.get("status"), 20),
                                                       "age unknown" if age is None else "%.0f hours old" % age)
        if ok and age is not None and age <= 36:
            say("PASS", GITHUB_HOST, txt + ". A green watch run does not prove the private upstreams were read (watch-and-canary.md)"
                if name == "Upstream watch" else txt + ". It does not read the registry or the hosted server (watch-and-canary.md)")
        else:
            say("WARN", GITHUB_HOST, txt + ". Open Actions in " + REPO)


# ---- self test ----
def selftest():
    bad = 0

    def expect(label, cond):
        nonlocal bad
        print("%-4s selftest: %s" % ("PASS" if cond else "FAIL", label))
        if not cond:
            bad += 1

    filler = "zq" * 30
    built = {
        "an sk- key": "error near sk-" + filler,
        "a github token": "token ghp_" + filler,
        "an AKIA key": "id AKIA" + "ZQ" * 12,
        "a JWT": "eyJ" + filler[:12] + ".eyJ" + filler[:12] + "." + filler[:12],
        "64 hex": "0x" + "ab12" * 16,
        "a bot token": "123456789:" + filler[:35],
        "12 short words": " ".join("zq" + chr(97 + i) + "x" for i in range(12)),
    }
    for label, s in built.items():
        out = ex("context " + s + " tail")
        leaked = filler in out or ("ab12" * 8) in out or "zqax zqbx" in out
        expect("%s is masked in what is printed" % label, not leaked and "masked" in out)
    long_line = "x " * 10 + "sk-" + filler + " " + "y" * 200
    expect("masking happens before the cut", filler[:20] not in ex(long_line, 40))
    expect("a plain sentence is left alone", ex("Could not load the MOI agent registry. account not found") ==
           "Could not load the MOI agent registry. account not found")
    for good in ("mcp.voyage.moi.technology", "pr-12-mcp.preview.voyage.moi.technology"):
        expect("host %s is accepted" % good, bool(HOST_RX.match(good)))
    for bad_host in ("https://a.example.com", "a.example.com/x", "a.example.com:8788", "user@a.example.com", "localhost", "a b.example.com", ""):
        expect("host %r is refused" % bad_host, not HOST_RX.match(bad_host))
    sse = 'event: message\ndata: {"result":{"tools":[{"name":"ping"}]}}\n\n'
    expect("a server-sent-event answer is parsed", rpc_answer(sse)["result"]["tools"][0]["name"] == "ping")
    expect("a plain JSON answer is parsed", rpc_answer('{"a":1}') == {"a": 1})
    expect("garbage gives None, not a traceback", rpc_answer("<html>") is None)
    expect("only read tools can be called", all(t in ("ping", "moi_resolve_agent", "moi_wallet_status") for t in SAFE_TOOLS))
    try:
        tool_call("a.example.com", "moi_transfer", {})
        expect("a write tool is refused by the script", False)
    except AssertionError:
        expect("a write tool is refused by the script", True)
    expect("a host with a trailing newline is refused", not HOST_RX.match("a.example.com\n"))
    expect("a secret-shaped tool name is masked", filler not in tool_label("gsk_" + "zq" * 12) and "masked" in tool_label("gsk_" + "zq" * 12))
    expect("an odd tool name shows as ?", tool_label("Bad Name!") == "?")
    expect("a redirect target drops user:password", redirect_host("https://user:pw@next.example.com/x") == "next.example.com")
    expect("a plain redirect target is read", redirect_host("https://next.example.com:8443/x?a=b") == "next.example.com")
    expect("deeply nested JSON gives None, not a traceback", jbody("[" * 200000) is None and rpc_answer("data: " + "[" * 200000) is None)

    class Broken:
        def __init__(self, exc):
            self.exc = exc

        def open(self, req, timeout=None):
            raise self.exc

    real = globals()["OPENER"]
    try:
        for label, exc in (("a truncated answer", httpclient.IncompleteRead(b"ab", 9)),
                           ("a reply that is not HTTP", httpclient.BadStatusLine("garbage")),
                           ("an over-long header", httpclient.LineTooLong("header line")),
                           ("a timeout", socket.timeout("timed out"))):
            globals()["OPENER"] = Broken(exc)
            try:
                http("a.example.com", "/health")
                ok = False
            except Unreachable:
                ok = True
            except Exception:
                ok = False
            expect("%s is reported as unreachable, not a traceback" % label, ok)
    finally:
        globals()["OPENER"] = real

    ap = build_parser()
    for label, args in (("a stray key-shaped argument", ["ghp_" + filler]),
                        ("a bad --timeout value", ["--timeout", "sk-" + filler]),
                        ("a bad --env value", ["--env", "AKIA" + "ZQ" * 12]),
                        ("a stray twelve-word argument", [" ".join("zq" + chr(97 + i) + "x" for i in range(12))])):
        saved, buf = sys.stderr, io.StringIO()
        sys.stderr = buf
        try:
            try:
                ap.parse_args(args)
                code = None
            except SystemExit as e:
                code = e.code
        finally:
            sys.stderr = saved
        msg = buf.getvalue()
        expect("usage error for %s exits 2 and echoes no secret" % label,
               code == 2 and filler not in msg and "ZQZQZQ" not in msg and "zqax zqbx" not in msg and "masked" in msg)
    print("Selftest: %s." % ("all passed" if not bad else "%d failed" % bad))
    return 1 if bad else 0


def build_parser():
    ap = MaskedParser(prog="mcp-health.sh", allow_abbrev=False, description="Read-only health check of the hosted MOI MCP server.")
    ap.add_argument("--env", choices=("prod", "dev"), default="prod")
    ap.add_argument("--write-host")
    ap.add_argument("--read-host")
    ap.add_argument("--no-read", action="store_true")
    ap.add_argument("--no-rpc", action="store_true")
    ap.add_argument("--github", action="store_true")
    ap.add_argument("--expect-write", type=int, default=13)
    ap.add_argument("--expect-read", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=15)
    ap.add_argument("--selftest", action="store_true")
    return ap


def main():
    global TIMEOUT
    ap = build_parser()
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not 1 <= a.timeout <= 60:
        ap.error("--timeout must be between 1 and 60")
    for flag, v in (("--expect-write", a.expect_write), ("--expect-read", a.expect_read)):
        if not 0 <= v <= 200:
            ap.error("%s must be between 0 and 200" % flag)
    for flag, v in (("--write-host", a.write_host), ("--read-host", a.read_host)):
        if v is not None and not HOST_RX.match(v):
            ap.error("%s needs a bare host name such as mcp.voyage.moi.technology: no scheme, port, path or user" % flag)
    TIMEOUT = a.timeout
    write_host = (a.write_host or DEFAULT_WRITE[a.env]).lower()
    read_host = (a.read_host or DEFAULT_READ[a.env]).lower()
    check_gateway(write_host, "write", a.expect_write)
    if not a.no_read:
        check_gateway(read_host, "read", a.expect_read)
    if not a.no_rpc:
        check_rpc()
    if a.github:
        check_github()
    print("")
    print("Not checked here: the phone-approved write path, the OAuth consent page, a wallet pairing, the registry id itself, "
          "and anything on the VM (pm2, nginx, logs). See health.md and connect-and-verify.md.")
    print("Hosts called: %s" % ", ".join(ex(h, 80) for h in hosts_called))
    print("Summary: %d PASS, %d WARN, %d FAIL." % (counts["PASS"], counts["WARN"], counts["FAIL"]))
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.stderr.write("mcp-health.sh: interrupted\n")
        sys.exit(130)
    except Exception as exc:
        # Only the class name is printed: the message could hold text from a response.
        sys.stderr.write("mcp-health.sh: unexpected internal error (%s). This is a fault in the script, not a finding about "
                         "the server. Run it with --selftest and tell the person who maintains the skill.\n" % type(exc).__name__)
        sys.exit(3)
PY
