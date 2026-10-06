#!/usr/bin/env bash
# launchpad-health.sh: read-only health check of the public MOI Agent Launchpad.
#
# Usage (SKILLS is the folder that holds the moi-* skills; the working directory does not matter):
#   bash "$SKILLS/moi-launchpad-ops/scripts/launchpad-health.sh" [--origin URL] [--wait SECONDS]
#                                                               [--timeout SECONDS] [--with-rpc]
#   --origin URL     the site to check (default https://launchpad.moi.technology). Scheme and host only.
#                    Plain http is accepted for localhost, 127.0.0.1 and ::1 only. An address with a user,
#                    password, path, query or fragment is refused.
#   --wait SECONDS   when chainStatus is pending or stale, wait this long and read /api/stats once more
#                    (default 30, 0 = do not wait, at most 120). An idle site reports stale on its first read.
#   --timeout N      seconds allowed for one request (default 25, 3 to 120). The chain read gets at least 45.
#   --with-rpc       also ask the public devnet node for net.Version (a JSON-RPC read method, sent as one
#                    POST). Without this flag every request is a plain GET.
#
# Checks, each printed as PASS, WARN, FAIL or INFO with the UTC time at the top and the bottom:
#   site          GET /                           200
#   stats         GET /api/stats                  chainStatus ok (pending or stale: WARN, unreachable: FAIL)
#   chain-listing GET /api/marketplace?source=chain   200 with source chain (502 chain_unreachable: FAIL)
#   market        GET /api/marketplace/<addr>/listing   the listing read for the first agent of the chain
#                 listing (onchain null means the read is unavailable, not that the agent is unlisted: WARN)
#   runtime       GET /api/runtime/version        200 with a version (a hash of the served runtime bundle)
#   rpc           POST net.Version (only with --with-rpc)
# It prints the host it called and never a full address. It sends no cookie, no key and no body (except the
# net.Version request), reads no file, and never opens an env file. Every string taken from an answer is
# masked first (long hex, tokens with known prefixes, JWTs, bearer tokens, private key blocks, runs of 12 or
# more short words) and cut to 200 characters after masking.
# Exit codes: 0 no FAIL (WARN allowed), 1 at least one FAIL, 2 bad usage or curl or python3 missing
# (or an unexpected internal error, reported without a traceback), 130 stopped with Ctrl-C.
# Needs python3 (standard library only) and curl. Works when started by bash or zsh.

command -v python3 >/dev/null 2>&1 || { echo "launchpad-health.sh needs python3 on the PATH" >&2; exit 2; }
export PYTHONDONTWRITEBYTECODE=1
exec python3 - "$@" <<'PY'
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import time
from urllib.parse import urlparse

DEFAULT_ORIGIN = "https://launchpad.moi.technology"
RPC_URL = "https://dev.voyage-rpc.moi.technology/devnet/"
RPC_HOST = "dev.voyage-rpc.moi.technology"
UA = "moi-launchpad-health/1.0 (read-only)"
MARK = "__LP_HEALTH_META__"
STALE_SECONDS = 15 * 60  # the app's own rule: a good read older than 15 minutes is stale

# ----------------------------------------------------------------------------
# Masking. Everything taken from an answer goes through safe() before it is printed.
# ----------------------------------------------------------------------------
SECRET_SHAPES = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?(?:-----END [A-Z ]*PRIVATE KEY-----|$)"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"),
    re.compile(r"\b(?:sk-ant-|sk-proj-|sk-|gsk_|ghp_|gho_|ghu_|ghs_|ghr_|github_pat_|xox[abprso]-|npm_|AIza|AKIA|ASIA)[A-Za-z0-9_\-]{8,}"),
    re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{30,}\b"),
    re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{8,}"),
    re.compile(r"(?:0x)?[0-9a-fA-F]{32,}"),
    re.compile(r"[A-Za-z0-9+/_=-]{40,}"),
]
PHRASE_MIN = 12
# Words of 3 to 8 letters joined by any short run of non-letters (spaces, commas, quotes, brackets, pipes,
# numbering such as "3. "), so a phrase written as a JSON list or a numbered list is caught as well.
PHRASE_RUN = re.compile(r"(?<![A-Za-z])(?:[A-Za-z]{3,8}(?![A-Za-z])[^A-Za-z]{1,6}){%d,}[A-Za-z]{3,8}(?![A-Za-z])" % (PHRASE_MIN - 1))
# Common English words that are not on the BIP-39 word list: a run that holds one is prose, not a phrase.
STOPWORDS = frozenset(
    "after and are been being both but could did does each every for from get got had has her here him "
    "his how its let many may most not our out per see she should some than the their them these those "
    "too using via was were which while who why with would yes your".split()
)
URL_USERINFO = re.compile(r"(https?://)[^/\s:@]+:[^/\s@]+@")
URL_QUERY = re.compile(r"(https?://[^\s?#]*)\?[^\s]*")
CONTROL = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")


def _mask_phrase(m):
    words = [w.lower() for w in re.findall(r"[A-Za-z]{3,8}", m.group(0))]
    run = 0
    for w in words:
        run = 0 if w in STOPWORDS else run + 1
        if run >= PHRASE_MIN:
            return "<masked: possible recovery phrase>"
    return m.group(0)


def mask(text):
    s = CONTROL.sub("?", str(text))
    s = URL_USERINFO.sub(r"\1<masked>@", s)
    s = URL_QUERY.sub(r"\1?<query hidden>", s)
    for rx in SECRET_SHAPES:
        s = rx.sub("<masked>", s)
    return PHRASE_RUN.sub(_mask_phrase, s)


def safe(text, limit=200):
    """Mask first, then collapse white space, then cut. Never the other way round."""
    s = re.sub(r"\s+", " ", mask(text)).strip()
    return s if len(s) <= limit else s[: limit - 3] + "..."


def num(v):
    return str(v) if isinstance(v, int) and not isinstance(v, bool) else "?"


def word(v):
    return v if isinstance(v, str) and re.fullmatch(r"[A-Za-z_]{1,24}", v) else "?"


# ----------------------------------------------------------------------------
# Arguments
# ----------------------------------------------------------------------------
def origin_arg(s):
    try:
        u = urlparse(s)
        port = u.port
    except ValueError:
        raise argparse.ArgumentTypeError("not an address I can read")
    if u.scheme not in ("http", "https") or not u.hostname:
        raise argparse.ArgumentTypeError("give an http or https address such as https://launchpad.moi.technology")
    if u.username or u.password or "@" in u.netloc:
        raise argparse.ArgumentTypeError("an address with a user or password is refused")
    if u.query or u.fragment or u.params or u.path not in ("", "/"):
        raise argparse.ArgumentTypeError("give the origin only (scheme and host), with no path or query")
    if u.scheme == "http" and u.hostname not in ("localhost", "127.0.0.1", "::1"):
        raise argparse.ArgumentTypeError("plain http is accepted for a local server only")
    host = u.hostname if ":" not in u.hostname else "[%s]" % u.hostname
    return "%s://%s%s" % (u.scheme, host, (":%d" % port) if port else "")


def bounded(lo, hi):
    def f(s):
        try:
            n = int(s)
        except ValueError:
            raise argparse.ArgumentTypeError("must be a whole number")
        if not lo <= n <= hi:
            raise argparse.ArgumentTypeError("must be between %d and %d" % (lo, hi))
        return n
    return f


class MaskedParser(argparse.ArgumentParser):
    """argparse echoes unknown arguments in its error text; mask that text like every other output."""

    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, "%s: error: %s\n" % (self.prog, safe(message, 300)))


def parse_args(argv):
    p = MaskedParser(
        prog="launchpad-health.sh",
        description="Read-only health check of the MOI Agent Launchpad. PASS, WARN or FAIL per check, with the UTC time.",
        epilog="Exit codes: 0 no FAIL, 1 at least one FAIL, 2 bad usage.",
    )
    p.add_argument("--origin", type=origin_arg, default=DEFAULT_ORIGIN, help="site to check (default %s)" % DEFAULT_ORIGIN)
    p.add_argument("--wait", type=bounded(0, 120), default=30, help="seconds to wait before one re-read when chainStatus is pending or stale (default 30)")
    p.add_argument("--timeout", type=bounded(3, 120), default=25, help="seconds allowed per request (default 25)")
    p.add_argument("--with-rpc", action="store_true", help="also read net.Version from the public devnet node (one POST of a read method)")
    p.add_argument("extra", nargs="*", help=argparse.SUPPRESS)
    a = p.parse_args(argv)
    if a.extra:
        p.error("takes no file or path arguments (it reads no files and never opens an env file): %s" % safe(" ".join(a.extra), 60))
    return a


# ----------------------------------------------------------------------------
# HTTP through curl (the system certificate store; GET unless a body is given)
# ----------------------------------------------------------------------------
def fetch(url, timeout, body=None, want_body=True):
    cmd = ["curl", "-sS", "--max-time", str(timeout), "--connect-timeout", "10", "--proto", "=http,https",
           "--max-filesize", "2000000", "-A", UA,
           "-o", "-" if want_body else os.devnull, "-w", "\n" + MARK + "%{http_code} %{time_total}"]
    if want_body:
        cmd += ["-H", "Accept: application/json"]
    if body is not None:
        cmd += ["-H", "Content-Type: application/json", "--data-binary", body]
    cmd.append(url)
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout + 15)
    except subprocess.TimeoutExpired:
        return {"code": 0, "err": "timed out after %ds" % timeout, "json": None, "secs": float(timeout)}
    out = r.stdout.decode("utf-8", "replace")
    i = out.rfind(MARK)
    if i < 0:
        return {"code": 0, "err": (r.stderr.decode("utf-8", "replace").strip() or "curl exit %d" % r.returncode), "json": None, "secs": 0.0}
    text, meta = out[:i], out[i + len(MARK):].split()
    try:
        code, secs = int(meta[0]), float(meta[1])
    except (IndexError, ValueError):
        code, secs = 0, 0.0
    err = ""
    if r.returncode != 0:  # a transport failure after the status line (too large, cut off): do not trust the answer
        code, err = 0, (r.stderr.decode("utf-8", "replace").strip() or "curl exit %d" % r.returncode)
    elif not code:
        err = r.stderr.decode("utf-8", "replace").strip() or "no answer"
    try:
        j = json.loads(text) if text.strip() else None
    except ValueError:
        j = None
    return {"code": code, "err": err, "json": j, "secs": secs, "text": text}


# ----------------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------------
RESULTS = []


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def say(level, name, msg, count=True):
    print("%-5s %-14s %s" % (level, name, msg))
    if count:
        RESULTS.append(level)


# ----------------------------------------------------------------------------
# Checks
# ----------------------------------------------------------------------------
def check_site(origin, host, timeout):
    r = fetch(origin + "/", timeout, want_body=False)
    if r["code"] == 0:
        say("FAIL", "site", "no answer from %s: %s. DNS, TLS, nginx or the container is down: only DevOps can act" % (host, safe(r["err"], 120)))
    elif r["code"] == 200:
        lvl = "WARN" if r["secs"] > 5 else "PASS"
        say(lvl, "site", "GET / -> 200 in %.2fs" % r["secs"])
    elif 300 <= r["code"] < 400:
        say("WARN", "site", "GET / -> %d (a redirect; the site normally answers 200)" % r["code"])
    else:
        say("FAIL", "site", "GET / -> %d" % r["code"])


def stats_line(j):
    parts = ["chainStatus=%s" % word(j.get("chainStatus")),
             "activeAgents=%s owners=%s registered=%s runs=%s" % (num(j.get("activeAgents")), num(j.get("owners")),
                                                                  num(j.get("registered")) if j.get("registered") is not None else "null", num(j.get("runs")))]
    as_of = j.get("chainAsOf")
    if isinstance(as_of, (int, float)) and not isinstance(as_of, bool):
        parts.append("chain read %ds ago" % max(0, int(time.time() - as_of / 1000.0)))
    else:
        parts.append("chain never read")
    if j.get("chainError"):
        parts.append("chainError: " + safe(j.get("chainError"), 140))
    return "; ".join(parts)


def classify_stats(r):
    if r["code"] == 0:
        return "FAIL", "no answer: " + safe(r["err"], 120), None
    if r["code"] != 200:
        return "FAIL", "GET /api/stats -> %d" % r["code"], None
    j = r["json"]
    if not isinstance(j, dict) or "chainStatus" not in j:
        return "FAIL", "HTTP 200 but not the stats JSON (an error page is being served?)", None
    st = j.get("chainStatus")
    line = stats_line(j)
    if st == "ok":
        as_of = j.get("chainAsOf")
        if isinstance(as_of, (int, float)) and time.time() - as_of / 1000.0 > STALE_SECONDS:
            return "WARN", line + " (older than the app's 15 minute stale rule)", st
        return "PASS", line, st
    if st in ("pending", "stale"):
        return "WARN", line, st
    if st == "unreachable":
        return "FAIL", line, st
    return "WARN", line + " (a chainStatus value this script does not know)", st


def check_stats(origin, timeout, wait):
    r = fetch(origin + "/api/stats", timeout)
    lvl, msg, st = classify_stats(r)
    if st in ("pending", "stale") and wait > 0:
        say("INFO", "stats", "first read: " + msg + "; reading again in %ds (refresh runs only when someone asks)" % wait, count=False)
        time.sleep(wait)
        r = fetch(origin + "/api/stats", timeout)
        lvl, msg, st = classify_stats(r)
        msg = "second read: " + msg
    say(lvl, "stats", msg)


def check_chain_listing(origin, timeout):
    r = fetch(origin + "/api/marketplace?source=chain", max(timeout, 45))
    j = r["json"]
    if r["code"] == 0:
        say("FAIL", "chain-listing", "no answer: " + safe(r["err"], 120))
        return None
    if r["code"] == 502 and isinstance(j, dict) and j.get("error") == "chain_unreachable":
        say("FAIL", "chain-listing", "502 chain_unreachable: " + safe(j.get("message", ""), 150))
        return None
    if r["code"] != 200 or not isinstance(j, dict) or not isinstance(j.get("agents"), list):
        say("FAIL", "chain-listing", "GET /api/marketplace (chain read) -> %d, not the expected JSON" % r["code"])
        return None
    n = len(j["agents"])
    if j.get("source") != "chain":
        say("WARN", "chain-listing", "200 but source=%s, so this is not a chain read (%d agents)" % (word(j.get("source")), n))
    elif n == 0:
        say("WARN", "chain-listing", "200 from the chain with 0 agents listed (read again; an empty list also comes from a failing enumeration)")
    else:
        say("PASS", "chain-listing", "200 from the chain, agents listed: %d, in %.1fs" % (n, r["secs"]))
    for a in j["agents"]:
        addr = a.get("address") if isinstance(a, dict) else None
        if isinstance(addr, str) and re.fullmatch(r"0x[0-9a-fA-F]{64}", addr):
            return addr
    return None


def check_market(origin, timeout, addr):
    if not addr:
        say("INFO", "market", "skipped: the chain listing gave no agent address to read a listing for", count=False)
        return
    r = fetch(origin + "/api/marketplace/" + addr + "/listing", timeout)
    j = r["json"]
    if r["code"] == 0:
        say("FAIL", "market", "no answer: " + safe(r["err"], 120))
    elif r["code"] == 404:
        say("WARN", "market", "the first listed agent has no public row (404), so the listing read was not exercised")
    elif r["code"] != 200 or not isinstance(j, dict) or "onchain" not in j:
        say("FAIL", "market", "listing read -> %d, not the expected JSON" % r["code"])
    elif j["onchain"] is None:
        say("WARN", "market", "onchain=null: the market read is unavailable (this does not mean the agent is unlisted); paid features depend on it")
    else:
        say("PASS", "market", "the market contract answers a listing read")


def check_runtime(origin, timeout):
    r = fetch(origin + "/api/runtime/version", timeout)
    j = r["json"]
    if r["code"] == 0:
        say("FAIL", "runtime", "no answer: " + safe(r["err"], 120))
    elif r["code"] == 200 and isinstance(j, dict) and isinstance(j.get("version"), str) and j["version"]:
        say("PASS", "runtime", "version %s (a hash of the runtime bundle served; it changes when public/runtime.cjs changes)" % safe(j["version"], 20))
    else:
        say("WARN", "runtime", "GET /api/runtime/version -> %d, no version in the answer" % r["code"])


def check_rpc(timeout):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "net.Version", "params": []})
    r = fetch(RPC_URL, timeout, body=body)
    j = r["json"]
    if r["code"] == 0:
        say("WARN", "rpc", "no answer from %s: %s (chain side)" % (RPC_HOST, safe(r["err"], 100)))
    elif isinstance(j, dict) and isinstance(j.get("result"), str):
        say("PASS", "rpc", "%s answers net.Version %s" % (RPC_HOST, safe(j["result"], 30)))
    elif isinstance(j, dict) and isinstance(j.get("error"), dict):
        say("WARN", "rpc", "%s answered an error: %s" % (RPC_HOST, safe(j["error"].get("message", ""), 100)))
    else:
        say("WARN", "rpc", "%s answered HTTP %d, not a JSON-RPC result" % (RPC_HOST, r["code"]))


def main(argv):
    args = parse_args(argv)
    if not shutil.which("curl"):
        print("launchpad-health.sh needs curl on the PATH", file=sys.stderr)
        return 2
    host = safe(urlparse(args.origin).netloc, 80)
    print("Launchpad health  %s  host=%s  (read-only; GET%s)" % (now(), host, " plus one POST of net.Version" if args.with_rpc else " only"))
    check_site(args.origin, host, args.timeout)
    check_stats(args.origin, args.timeout, args.wait)
    addr = check_chain_listing(args.origin, args.timeout)
    check_market(args.origin, args.timeout, addr)
    check_runtime(args.origin, args.timeout)
    if args.with_rpc:
        check_rpc(args.timeout)
    worst = "FAIL" if "FAIL" in RESULTS else ("WARN" if "WARN" in RESULTS else "PASS")
    print("RESULT: %s at %s  (PASS %d, WARN %d, FAIL %d)" % (worst, now(), RESULTS.count("PASS"), RESULTS.count("WARN"), RESULTS.count("FAIL")))
    return 1 if worst == "FAIL" else 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        print("interrupted; no result", file=sys.stderr)
        sys.exit(130)
    except Exception as e:  # never show a traceback: a health check that crashes must still say so plainly
        print("ERROR: unexpected failure (%s); no result. Run the checks by hand from moi-launchpad-ops/references/health.md" % type(e).__name__, file=sys.stderr)
        sys.exit(2)
PY
