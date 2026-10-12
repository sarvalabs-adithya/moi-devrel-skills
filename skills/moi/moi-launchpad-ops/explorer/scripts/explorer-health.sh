#!/usr/bin/env bash
# explorer-health.sh: read-only health check of the MOI Agent Explorer (agents.moi.technology).
#
# Usage:   bash "$SKILLS/moi-launchpad-ops/explorer/scripts/explorer-health.sh" [--chain-count N] [--sync-hours H] [--skip-rpc]
#          SKILLS is the folder that holds the moi-* skills. It needs no working copy and no key.
#   --chain-count N  the number of agents the registry holds on chain, read by someone who can (see
#                    explorer/references/index-sync.md, section 4). The script compares it with the index total.
#   --sync-hours H   the scheduled reconcile interval to expect (default 4, the default of SYNC_INTERVAL_HOURS
#                    in the code of PR #5). A last reconcile older than twice this is a WARN.
#   --skip-rpc       do not call the devnet RPC.
# Env:     EXPLORER_UI, EXPLORER_API, EXPLORER_RPC override the three hosts (defaults: the public hosts).
#          Each must start with http:// or https:// and carry no user name, password, query string or bad port.
#          Only scheme and host are ever printed.
# Calls:   GET on the site and three API paths (/health, /registry/agents, /admin/sync), and one HTTP POST
#          that carries a read-only JSON-RPC call (net.Version) to the devnet RPC. Nothing is signed, written
#          or submitted. Each call has a 15 second timeout and a 5 MB cap. It prints the host it called, never
#          a full URL. It reads no file and writes no file.
# Checks:  1. the site answers 200 with HTML.
#          2. the API /health says ok (this proves the process only) and its clock is near this machine's.
#          3. /registry/agents is readable: total, verified, rows on the retired Launchpad host, rows with no card.
#          4. /admin/sync: 404 means the reconcile code of PR #5 is not deployed; 200 reports the last run.
#          5. the devnet RPC answers net.Version (compare it with the release by hand).
#          6. with --chain-count, the index total against the chain.
# Output:  PASS, WARN or FAIL per line, then a summary. FAIL is for an outage (site or API down, index unreadable).
#          A stale index is a WARN. Read every WARN: WARN does not change the exit code.
#          Text taken from an answer is masked (hex of 24 or more characters, known token prefixes, JWTs,
#          runs of 12 short words, any 32-character word) before it is cut to 120 characters.
# Exit:    0 no FAIL, 1 at least one FAIL, 2 bad usage, a bad address in an EXPLORER_* variable, or an
#          unexpected internal error (one line on stderr, never a traceback; treat the result as unknown).
# Works under bash 3.2 and zsh (run it with bash). Python 3 standard library only.

exec python3 - "$@" <<'PY'
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import urlsplit

DEFAULTS = {
    "EXPLORER_UI": "https://agents.moi.technology",
    "EXPLORER_API": "https://api.agents.moi.technology",
    "EXPLORER_RPC": "https://dev.voyage-rpc.moi.technology/devnet/",
}
# The Launchpad's retired host (its cards stopped being served there) and its current host. Both are in the
# default of LAUNCHPAD_HOSTS in PR #5. The Launchpad moved hosts on 2026-08-03.
RETIRED_LAUNCHPAD_HOST = "moi-agent-launchpad.vercel.app"
CURRENT_LAUNCHPAD_HOST = "launchpad.moi.technology"
UA = "moi-explorer-ops-health/1.0 (read-only)"
CAP = 5_000_000
TIMEOUT = 15

counts = {"PASS": 0, "WARN": 0, "FAIL": 0}


def _no_traceback(kind, value, tb):
    """Last resort: an answer shaped in a way this script did not expect must not print a traceback, and must
    not look like an outage (exit 1). Only the exception class is printed, never its message."""
    sys.stdout.flush()
    print("explorer-health.sh: unexpected %s, so the check could not finish. Treat the result as unknown."
          % kind.__name__, file=sys.stderr)
    sys.stderr.flush()
    os._exit(2)


sys.excepthook = _no_traceback


def say(level, msg):
    counts[level] += 1
    print("%-5s %s" % (level, msg))


def note(msg):
    print("      " + msg)


def usage(code=2):
    print('usage: explorer-health.sh [--chain-count N] [--sync-hours H] [--skip-rpc]',
          file=sys.stderr if code else sys.stdout)
    sys.exit(code)


# ---------------------------------------------------------------- masking
HEX = re.compile(r"(?:0x)?[0-9a-fA-F]{24,}")
PREFIXES = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"\bgsk_[A-Za-z0-9]{16,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{30,}"),
    re.compile(r"\bnpm_[A-Za-z0-9]{20,}"),
    re.compile(r"\bglpat-[A-Za-z0-9_-]{16,}"),
    re.compile(r"\bhf_[A-Za-z0-9]{20,}"),
    re.compile(r"\b(?:sk|pk|rk)_(?:live|test)_[A-Za-z0-9]{10,}"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{5,}"),
]
RUN = re.compile(r"(?:\b[a-z]{3,8}\b[ ,]+)+\b[a-z]{3,8}\b", re.I)
URLS = re.compile(r"(https?://[^/\s:@]+(?::\d+)?)/[^\s]*")
# Common English words that are not on the BIP-39 list (the same list as moi-devrel's secret-scan.sh, checked
# 2026-10-02). A real phrase never holds one, so a word from this list ends a run.
PROSE = frozenset(
    "after and are been being both but could did does each every for from get got had has her here him "
    "his how its let many may most not our out per see she should some than the their them these those "
    "too using via was were which while who why with would yes your".split()
)


def _phrase(m):
    """A run of 12 or more short words is a possible recovery phrase. An ordinary English word ends a segment,
    so a long sentence is kept and a bare run is masked whole, with any label word that sits in front of it."""
    out, seg = [], []

    def flush():
        if len(seg) >= 12:
            out.append("<masked: 12 short words> ")
        else:
            out.extend(w + sep for w, sep in seg)
        del seg[:]

    for w, sep in re.findall(r"([A-Za-z]+)([ ,]*)", m.group(0)):
        if w.lower() in PROSE:
            flush()
            out.append(w + sep)
        else:
            seg.append((w, sep))
    flush()
    return "".join(out).rstrip()


def safe(value, limit=120):
    """Mask secret shapes first, then cut. Used on every string that came from an answer."""
    s = " ".join(str(value).split())
    s = URLS.sub(r"\1/...", s)
    for rx in PREFIXES:
        s = rx.sub("<masked>", s)
    s = HEX.sub("<masked>", s)
    s = RUN.sub(_phrase, s)
    s = " ".join("<masked>" if len(tok) >= 32 else tok for tok in s.split(" "))
    return s[:limit]


def where(url):
    """scheme://host[:port] of a URL, so a path or a key in it is never printed."""
    try:
        u = urlsplit(url)
        port = ":%d" % u.port if u.port else ""
        return "%s://%s%s" % (u.scheme, u.hostname or "?", port)
    except ValueError:
        return "<unparseable address>"


def host_of(value):
    try:
        return (urlsplit(str(value or "")).hostname or "").lower()
    except ValueError:
        return ""


# ---------------------------------------------------------------- arguments
chain_count = None
sync_hours = 4.0
skip_rpc = False
args = sys.argv[1:]
i = 0
while i < len(args):
    a = args[i]
    if a in ("-h", "--help"):
        usage(0)
    elif a == "--skip-rpc":
        skip_rpc = True
    elif a in ("--chain-count", "--sync-hours"):
        i += 1
        if i >= len(args):
            print("%s needs a value" % a, file=sys.stderr)
            usage()
        try:
            if a == "--chain-count":
                chain_count = int(args[i])
                if chain_count < 0:
                    raise ValueError
            else:
                sync_hours = float(args[i])
                if not sync_hours > 0 or sync_hours > 10000:
                    raise ValueError
        except ValueError:
            print("%s needs a %s" % (a, "whole number of 0 or more" if a == "--chain-count" else "number above 0"),
                  file=sys.stderr)
            usage()
    else:
        print("unknown argument: %s" % safe(a, 40), file=sys.stderr)
        usage()
    i += 1

hosts = {}
for name, default in DEFAULTS.items():
    url = os.environ.get(name) or default
    try:
        u = urlsplit(url)
        u.port  # raises ValueError for a port that is not a number from 0 to 65535
        bad = (u.scheme not in ("http", "https") or not u.hostname or u.username or u.password
               or u.query or u.fragment)
    except ValueError:
        bad = True
    if bad:
        print("%s must be an http:// or https:// address with a valid port and no user name, password or query string"
              % name, file=sys.stderr)
        sys.exit(2)
    hosts[name] = url.rstrip("/")


# ---------------------------------------------------------------- requests
class Unreachable(Exception):
    pass


def request(method, url, body=None):
    """One request. Returns (status, content_type, text). Uses curl when installed (system certificates)."""
    if shutil.which("curl"):
        mark = "__EXPLORER_HEALTH_META__"
        cmd = ["curl", "-sS", "-L", "--max-redirs", "3", "--max-time", str(TIMEOUT),
               "--max-filesize", str(CAP), "--proto", "=http,https", "--proto-redir", "=http,https",
               "-A", UA, "-X", method, "-w", "\n" + mark + "%{http_code}|%{content_type}"]
        if body is not None:
            cmd += ["-H", "content-type: application/json", "--data-binary", body]
        cmd.append(url)
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=TIMEOUT + 10)
        except (OSError, subprocess.SubprocessError) as e:
            raise Unreachable(safe(e, 80))
        if r.returncode != 0:
            raise Unreachable("curl exit %d: %s" % (r.returncode, safe(r.stderr.decode("utf-8", "replace"), 80)))
        out = r.stdout.decode("utf-8", "replace")
        text, _, meta = out.rpartition("\n" + mark)
        code, _, ctype = meta.partition("|")
        return int(code or 0), ctype.strip(), text
    data = body.encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={"User-Agent": UA,
                                 **({"Content-Type": "application/json"} if data else {})})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status, r.headers.get("Content-Type", ""), r.read(CAP).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        try:
            text = e.read(CAP).decode("utf-8", "replace")
        except Exception:
            text = ""
        return e.code, e.headers.get("Content-Type", "") if e.headers else "", text
    except (urllib.error.URLError, OSError) as e:
        raise Unreachable(safe(getattr(e, "reason", e), 80))


def parse(text):
    """JSON or None. A body nested thousands deep raises RecursionError, which is not a ValueError."""
    try:
        return json.loads(text)
    except (ValueError, RecursionError):
        return None


def is_int(v):
    """A whole number of a believable size. A 400-digit number would overflow the float sums below."""
    return isinstance(v, int) and not isinstance(v, bool) and abs(v) < 10 ** 15


now = time.time()
print("Explorer health, %s UTC" % time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(now)))

# ---------------------------------------------------------------- 1. the site
ui = hosts["EXPLORER_UI"]
print("Site (%s)" % where(ui))
try:
    code, ctype, _ = request("GET", ui + "/")
    if code == 200 and "html" in ctype.lower():
        say("PASS", "GET / answered 200 with HTML")
    elif code == 200:
        say("WARN", "GET / answered 200 but the content type is %s, not HTML" % safe(ctype, 40))
    else:
        say("FAIL", "GET / answered HTTP %d" % code)
except Unreachable as e:
    say("FAIL", "the site is unreachable: %s" % e)

# ---------------------------------------------------------------- 2. the API process
api = hosts["EXPLORER_API"]
print("API (%s)" % where(api))
api_up = False
try:
    code, _, text = request("GET", api + "/health")
    d = parse(text)
    if code == 200 and isinstance(d, dict) and d.get("status") == "ok":
        api_up = True
        say("PASS", "GET /health says ok (this proves the process is up and nothing about the data)")
        ts = d.get("timestamp")
        if is_int(ts):
            skew = abs(now - ts)
            if skew > 300:
                say("WARN", "the API clock differs from this machine by %d seconds (a cached answer, or clock drift)" % skew)
        else:
            say("WARN", "/health carried no whole-number timestamp")
    elif code == 200:
        say("WARN", "GET /health answered 200 but not {\"status\":\"ok\"}")
    else:
        say("FAIL", "GET /health answered HTTP %d" % code)
except Unreachable as e:
    say("FAIL", "the API is unreachable: %s" % e)

# ---------------------------------------------------------------- 3. the index
total = None
print("Index")
try:
    code, _, text = request("GET", api + "/registry/agents")
    d = parse(text)
    if code == 200 and isinstance(d, dict) and isinstance(d.get("agents"), list) and is_int(d.get("total")):
        rows = [a for a in d["agents"] if isinstance(a, dict)]
        total = d["total"]
        verified = sum(1 for a in rows if a.get("verified") is True)
        retired = sum(1 for a in rows if RETIRED_LAUNCHPAD_HOST in (host_of(a.get("card_uri")), host_of(a.get("url"))))
        current = sum(1 for a in rows if CURRENT_LAUNCHPAD_HOST in (host_of(a.get("card_uri")), host_of(a.get("url"))))
        nocard = sum(1 for a in rows if a.get("card") is None)
        say("PASS", "GET /registry/agents readable: total %d, verified %d" % (total, verified))
        if total != len(d["agents"]):
            say("WARN", "total %d but the answer lists %d agents" % (total, len(d["agents"])))
        if total == 0:
            say("WARN", "the index is empty")
        if retired:
            say("WARN", "%d rows use the retired Launchpad host %s, which stopped serving cards"
                % (retired, RETIRED_LAUNCHPAD_HOST))
        note("rows on %s: %d. Rows with no card: %d." % (CURRENT_LAUNCHPAD_HOST, current, nocard))
    elif code == 200:
        say("FAIL", "GET /registry/agents answered 200 but not {agents: [...], total: N}")
    else:
        err = d.get("error") if isinstance(d, dict) else None
        say("FAIL", "GET /registry/agents answered HTTP %d%s" % (code, (": " + safe(err, 60)) if err else ""))
except Unreachable as e:
    say("FAIL", "GET /registry/agents is unreachable: %s" % e)

# ---------------------------------------------------------------- 4. the reconcile
print("Reconcile")
try:
    code, _, text = request("GET", api + "/admin/sync")
    d = parse(text)
    if code == 404:
        say("WARN", "GET /admin/sync is 404: the reconcile code of PR #5 is not deployed. "
                    "Nothing refreshes existing rows on a schedule and the admin page has no sync button")
    elif code == 200 and isinstance(d, dict) and isinstance(d.get("running"), bool):
        last = d.get("last")
        if d["running"]:
            note("a reconcile is running now")
        if last is None:
            say("WARN", "no reconcile has finished since the API last started (the first scheduled run is one "
                        "interval after boot, and every deploy restarts the clock)")
        elif isinstance(last, dict):
            fin = last.get("finishedAt")
            err = last.get("error")
            trig = last.get("trigger") if last.get("trigger") in ("schedule", "admin", "script") else "?"
            nums = {k: last.get(k) for k in ("onChain", "added", "refreshed", "failed", "verified")}
            ok_nums = all(is_int(v) for v in nums.values())
            if err:
                say("WARN", "the last reconcile aborted: %s" % safe(err))
            elif not is_int(fin) or not ok_nums:
                say("WARN", "the last reconcile record is incomplete")
            else:
                age = (now * 1000 - fin) / 3600000.0
                line = ("last reconcile (%s) finished %.1f h ago: on chain %d, added %d, refreshed %d, failed %d, "
                        "verified %d" % (trig, age, nums["onChain"], nums["added"], nums["refreshed"],
                                         nums["failed"], nums["verified"]))
                if age > 2 * sync_hours:
                    say("WARN", line + ". That is more than twice the %.4g h interval" % sync_hours)
                else:
                    say("PASS", line)
                if nums["failed"] > 0:
                    say("WARN", "%d agents failed to index in the last reconcile" % nums["failed"])
                if total is not None and nums["onChain"] != total:
                    say("WARN", "the last reconcile saw %d agents on chain, the index holds %d "
                                "(rows are never deleted, so extra rows stay after a reset)" % (nums["onChain"], total))
        else:
            say("WARN", "/admin/sync carried an unexpected 'last' value")
    else:
        say("WARN", "GET /admin/sync answered HTTP %d with an unexpected body" % code)
except Unreachable as e:
    say("WARN", "GET /admin/sync is unreachable: %s" % e)

# ---------------------------------------------------------------- 5. the devnet RPC
if skip_rpc:
    note("devnet RPC check skipped (--skip-rpc)")
else:
    rpc = hosts["EXPLORER_RPC"]
    print("Devnet RPC (%s)" % where(rpc))
    try:
        code, _, text = request("POST", rpc + "/", '{"jsonrpc":"2.0","id":1,"method":"net.Version","params":[]}')
        d = parse(text)
        if code == 200 and isinstance(d, dict) and isinstance(d.get("result"), str):
            say("PASS", "net.Version answered %s. Compare it with the release by hand" % safe(d["result"], 30))
        elif code == 200 and isinstance(d, dict) and isinstance(d.get("error"), dict):
            say("WARN", "net.Version returned an error: %s" % safe(d["error"].get("message", ""), 60))
        else:
            say("WARN", "net.Version answered HTTP %d with an unexpected body" % code)
    except Unreachable as e:
        say("WARN", "the devnet RPC is unreachable from here: %s" % e)

# ---------------------------------------------------------------- 6. the chain count
if chain_count is not None:
    print("Chain count (given by you)")
    if total is None:
        say("WARN", "the index total is unknown, so --chain-count %d cannot be compared" % chain_count)
    elif total == chain_count:
        say("PASS", "the index holds %d agents, the same as the chain" % total)
    elif total < chain_count:
        say("WARN", "the index holds %d agents, the chain %d: %d are missing" % (total, chain_count, chain_count - total))
    else:
        say("WARN", "the index holds %d agents, the chain %d: %d rows are not on chain (rows are never deleted)"
            % (total, chain_count, total - chain_count))
else:
    note("Chain count not read. Without it, an index can look healthy and be frozen: explorer/references/index-sync.md, section 4.")

print("Summary: %d PASS, %d WARN, %d FAIL" % (counts["PASS"], counts["WARN"], counts["FAIL"]))
if counts["FAIL"]:
    print("An outage: explorer/references/troubleshoot.md, then explorer/references/rollback.md. A VM action: ASK: Upendhar.")
elif counts["WARN"]:
    print("Read every WARN. A stale index: explorer/references/index-sync.md. Anything else: explorer/references/troubleshoot.md.")
sys.exit(1 if counts["FAIL"] else 0)
PY
