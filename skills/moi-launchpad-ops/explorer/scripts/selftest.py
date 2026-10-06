#!/usr/bin/env python3
"""selftest.py: checks explorer-health.sh against canned answers from a short-lived local test server.

Usage (SKILLS is the folder that holds the moi-* skills):
    python3 "$SKILLS/moi-launchpad-ops/explorer/scripts/selftest.py"

It starts one HTTP server inside this process, on a free local port, and stops it when the process ends. It
runs explorer-health.sh against that server (EXPLORER_UI, EXPLORER_API and EXPLORER_RPC point at it in every
case; a case may replace one), once per case: healthy, outages, malformed answers, answers nested or numbered
to break a parser, secret-shaped text, huge and slow answers, bad arguments and bad addresses. It never touches
the public hosts, writes no file and needs no key. One case waits 15 seconds, for the timeout. Secret-shaped
inputs are built here at run time from a known prefix plus filler, and each case that holds one asserts the
filler, the prefixes and the words are absent from the output. Every case also fails on the word Traceback.
Exit codes: 0 every case passed, 1 a case failed, 2 the script under test was not found.
Python 3 standard library only. Needs bash and curl, as the script does.
"""
import json
import os
import socket
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "explorer-health.sh")
if not os.path.isfile(SCRIPT):
    print("explorer-health.sh not found next to this file", file=sys.stderr)
    sys.exit(2)

FILL = "zq" * 20
SK = "sk-ant-" + FILL
GH = "ghp_" + FILL
JWT = "eyJ" + "zq" * 6 + "." + "zq" * 6 + "." + "zq" * 6
HEX = "0x" + "ab12" * 16
AKIA = "AKIA" + "ZQ" * 8
# Twelve short words with no ordinary English word among them, the shape of a recovery phrase: zqa, zqb ... zql.
PHRASE = " ".join("zq" + chr(97 + i) for i in range(12))
SECRETS = [FILL, "zqzqzq", HEX[2:12], "zqa", "ZQZQZQ"]

state = {}
seen = []


def now_ms():
    return int(time.time() * 1000)


class Quiet(ThreadingHTTPServer):
    def handle_error(self, request, client_address):  # a client that hangs up is part of some cases
        pass


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, body, ctype="application/json"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body)
        if isinstance(body, str):
            body = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def route(self, method):
        seen.append(self.path)
        path = self.path.split("?")[0]
        r = state.get(method + " " + path)
        if r is None:
            return self.send(404, {"error": "Not found"})
        if callable(r):
            r = r()
        if r.get("sleep"):
            time.sleep(r["sleep"])
        self.send(r.get("code", 200), r["body"], r.get("ctype", "application/json"))

    def do_GET(self):
        self.route("GET")

    def do_POST(self):
        self.rfile.read(int(self.headers.get("Content-Length") or 0))
        self.route("POST")


def agent(i, host="launchpad.moi.technology", verified=False, card=True):
    return {"agent_id": "agent_%d" % i, "owner": "o", "agent_wallet": "w", "status": "ACTIVE",
            "verified": verified, "url": "https://%s/x" % host, "card_uri": "https://%s/api/moi/card/%d" % (host, i),
            "card": {"name": "n"} if card else None}


def healthy():
    st = {}
    st["GET /"] = {"body": "<html></html>", "ctype": "text/html"}
    st["GET /health"] = lambda: {"body": {"status": "ok", "timestamp": int(time.time())}}
    st["GET /registry/agents"] = {"body": {"agents": [agent(1, verified=True), agent(2, verified=True), agent(3)], "total": 3}}
    st["GET /admin/sync"] = lambda: {"body": {"running": False, "last": {
        "trigger": "schedule", "startedAt": now_ms() - 3700000, "finishedAt": now_ms() - 3600000,
        "onChain": 3, "added": 0, "refreshed": 3, "failed": 0, "verified": 2, "error": None}}}
    st["POST /devnet/"] = {"body": {"jsonrpc": "2.0", "id": 1, "result": "0.13.0"}}
    return st


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


srv = Quiet(("127.0.0.1", 0), H)
BASE = "http://localhost:%d" % srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
ENV = {"EXPLORER_UI": BASE, "EXPLORER_API": BASE, "EXPLORER_RPC": BASE + "/devnet/"}

total = 0
failed = []


def case(name, args, want, must=(), mustnot=(), env=None, mod=None, timeout=90):
    global total
    total += 1
    state.clear()
    state.update(healthy())
    del seen[:]
    if mod:
        mod(state)
    e = {k: v for k, v in os.environ.items() if not k.startswith("EXPLORER_")}
    e["PYTHONDONTWRITEBYTECODE"] = "1"
    e.update(ENV)  # every case starts from the local test server, so no case can reach a public host
    if env is not None:
        e.update(env)
    t = time.time()
    p = subprocess.run(["bash", SCRIPT] + args, capture_output=True, text=True, env=e, timeout=timeout)
    both = p.stdout + p.stderr
    problems = []
    if p.returncode != want:
        problems.append("exit %d, wanted %d" % (p.returncode, want))
    problems += ["missing: " + m for m in must if m not in both]
    problems += ["leaked: " + m[:12] for m in mustnot if m in both]
    if "Traceback" in both:
        problems.append("traceback")
    print("%-5s %-34s exit=%d %.1fs" % ("ok" if not problems else "FAIL", name, p.returncode, time.time() - t))
    if problems:
        failed.append(name)
        print("      " + "; ".join(problems))
        print(both.rstrip())
    return both


def err_in_sync(text):
    def f(s):
        s["GET /admin/sync"] = {"body": {"running": False, "last": {"trigger": "schedule", "finishedAt": now_ms(), "error": text}}}
    return f


# --- healthy shapes
case("healthy-all-pass", [], 0, must=["Summary: 5 PASS, 0 WARN, 0 FAIL"])
case("chain-count-equal", ["--chain-count", "3"], 0, must=["the same as the chain"])
case("chain-count-missing", ["--chain-count", "5"], 0, must=["2 are missing"])
case("chain-count-extra", ["--chain-count", "1"], 0, must=["2 rows are not on chain"])
case("skip-rpc", ["--skip-rpc"], 0, must=["skipped"], mustnot=["net.Version answered"])

# --- outages and malformed answers
def site_down(s):
    s["GET /"] = {"code": 500, "body": "boom", "ctype": "text/plain"}
    s["GET /health"] = {"code": 500, "body": {"error": "x"}}
case("site-and-api-500", [], 1, must=["FAIL  GET / answered HTTP 500", "FAIL  GET /health answered HTTP 500", "explorer/references/troubleshoot.md", "explorer/references/rollback.md"], mod=site_down)
case("health-200-not-ok", [], 0, must=["WARN  GET /health answered 200 but not"],
     mod=lambda s: s.update({"GET /health": {"body": {"status": "starting"}}}))
case("index-not-json", [], 1, must=["FAIL  GET /registry/agents answered 200 but not"],
     mod=lambda s: s.update({"GET /registry/agents": {"body": "<html>gateway</html>", "ctype": "text/html"}}))
case("index-500", [], 1, must=["FAIL  GET /registry/agents answered HTTP 500: Failed to fetch agents"],
     mod=lambda s: s.update({"GET /registry/agents": {"code": 500, "body": {"error": "Failed to fetch agents", "detail": "db down"}}}))
case("index-wrong-types", [], 1, must=["FAIL  GET /registry/agents answered 200 but not"],
     mod=lambda s: s.update({"GET /registry/agents": {"body": {"agents": "nope", "total": "3"}}}))
case("index-weird-rows", [], 0, must=["total 7, verified 0", "WARN  total 7 but the answer lists 4"],
     mod=lambda s: s.update({"GET /registry/agents": {"body": {"agents": [None, 5, "x", {"verified": "yes", "url": 7, "card_uri": None}], "total": 7}}}))
case("index-empty", [], 0, must=["WARN  the index is empty"],
     mod=lambda s: s.update({"GET /registry/agents": {"body": {"agents": [], "total": 0}}}))
case("index-retired-host", [], 0, must=["WARN  2 rows use the retired Launchpad host", "Rows with no card: 1"],
     mod=lambda s: s.update({"GET /registry/agents": {"body": {"agents": [
         agent(1, host="moi-agent-launchpad.vercel.app"), agent(2, host="moi-agent-launchpad.vercel.app"), agent(3, card=False)], "total": 3}}}))

# --- the reconcile record
case("sync-404", [], 0, must=["WARN  GET /admin/sync is 404", "A stale index: explorer/references/index-sync.md"], mod=lambda s: s.pop("GET /admin/sync"))
case("sync-never-ran", [], 0, must=["a reconcile is running now", "WARN  no reconcile has finished"],
     mod=lambda s: s.update({"GET /admin/sync": {"body": {"running": True, "last": None}}}))


def sync_old(s):
    s["GET /admin/sync"] = lambda: {"body": {"running": False, "last": {"trigger": "admin", "finishedAt": now_ms() - 20 * 3600000,
        "onChain": 9, "added": 0, "refreshed": 3, "failed": 2, "verified": 1, "error": None}}}
case("sync-old-failed-mismatch", [], 0, must=["more than twice the 4 h interval", "2 agents failed to index", "saw 9 agents on chain, the index holds 3"], mod=sync_old)
case("sync-old-custom-interval", ["--sync-hours", "12"], 0, must=["PASS  last reconcile (admin) finished 20."], mod=sync_old)
case("sync-garbage-shape", [], 0, must=["WARN  GET /admin/sync answered HTTP 200 with an unexpected body"],
     mod=lambda s: s.update({"GET /admin/sync": {"body": {"running": "maybe", "last": 7}}}))
case("sync-incomplete-record", [], 0, must=["WARN  the last reconcile record is incomplete"],
     mod=lambda s: s.update({"GET /admin/sync": {"body": {"running": False, "last": {"trigger": "script", "finishedAt": "soon"}}}}))
case("sync-not-json", [], 0, must=["WARN  GET /admin/sync answered HTTP 200 with an unexpected body"],
     mod=lambda s: s.update({"GET /admin/sync": {"body": "not json at all", "ctype": "text/plain"}}))

# --- secret-shaped text in answers: masked before the cut
case("err-more-token-prefixes", [], 0, must=["WARN  the last reconcile aborted: tokens <masked> <masked> <masked>"],
     mustnot=[FILL, "glpat", "hf_", "sk_live"],
     mod=err_in_sync("tokens glpat-%s hf_%s sk_live_%s" % (FILL, FILL, FILL)))
case("err-secret-shapes", [], 0,
     must=["WARN  the last reconcile aborted: account not found for <masked> token <masked>"],
     mustnot=SECRETS + [SK[:12], GH[:8], JWT[:10], AKIA[:8]],
     mod=err_in_sync("account not found for %s token %s %s %s %s %s phrase %s" % (HEX, SK, GH, JWT, AKIA, FILL, PHRASE)))
case("err-prose-kept", [], 0, must=["because the node was not reachable"],
     mod=err_in_sync("failed to read the registry because the node was not reachable from the server today"))
case("err-phrase-comma-separated", [], 0, must=["WARN  the last reconcile aborted:"], mustnot=["zqa", "zqb", "zql"],
     mod=err_in_sync("bad: " + ", ".join(PHRASE.split())))
case("err-phrase-inside-prose", [], 0, must=["<masked: 12 short words>"], mustnot=["zqa", "zql"],
     mod=err_in_sync("the node returned " + PHRASE + " and stopped"))
case("err-phrase-uppercase", [], 0, mustnot=["ZQA", "zqa", "ZQL"], mod=err_in_sync(PHRASE.upper()))
case("err-secret-straddles-col-120", [], 0, must=["WARN  the last reconcile aborted:"], mustnot=[FILL, "sk-ant"],
     mod=err_in_sync(("x" * 95) + " " + SK + " tail"))
case("err-url-with-key-in-path", [], 0, must=["https://rpc.example.test/..."], mustnot=["KEYabc123", "/path"],
     mod=err_in_sync("failed to reach https://rpc.example.test/KEYabc123/path now"))
case("err-1MB-string", [], 0, must=["WARN  the last reconcile aborted:"], mustnot=[FILL], mod=err_in_sync(SK + " " + ("word " * 200000)))
case("err-long-word-over-32", [], 0, must=["<masked>"], mustnot=["q" * 33], mod=err_in_sync("id " + "q" * 40))
case("err-newlines-and-tabs", [], 0, must=["WARN  the last reconcile aborted: line one line two"], mod=err_in_sync("line one\n\tline two"))
case("rpc-error-object", [], 0, must=["WARN  net.Version returned an error: method not found <masked>"], mustnot=[FILL],
     mod=lambda s: s.update({"POST /devnet/": {"body": {"jsonrpc": "2.0", "id": 1, "error": {"code": -32601, "message": "method not found %s" % SK}}}}))
case("rpc-not-json", [], 0, must=["WARN  net.Version answered HTTP 200 with an unexpected body"],
     mod=lambda s: s.update({"POST /devnet/": {"body": "<html>proxy</html>", "ctype": "text/html"}}))
case("rpc-result-secret-shape", [], 0, must=["net.Version answered <masked>"], mustnot=["ab12ab12", AKIA],
     mod=lambda s: s.update({"POST /devnet/": {"body": {"jsonrpc": "2.0", "id": 1, "result": HEX + AKIA}}}))

# --- clock
case("health-clock-skew", [], 0, must=["WARN  the API clock differs from this machine by"],
     mod=lambda s: s.update({"GET /health": {"body": {"status": "ok", "timestamp": int(time.time()) - 3600}}}))
case("health-no-timestamp", [], 0, must=["WARN  /health carried no whole-number timestamp"],
     mod=lambda s: s.update({"GET /health": {"body": {"status": "ok"}}}))

# --- answers shaped to break a parser: nesting thousands deep, and numbers hundreds of digits long. None may
# print a traceback; a deep or huge answer is read as "not the expected shape".
DEEP = "[" * 200000
HUGE = "1" + "0" * 400
case("deep-json-index", [], 1, must=["FAIL  GET /registry/agents answered 200 but not"],
     mod=lambda s: s.update({"GET /registry/agents": {"body": DEEP}}))
case("deep-json-sync", [], 0, must=["WARN  GET /admin/sync answered HTTP 200 with an unexpected body"],
     mod=lambda s: s.update({"GET /admin/sync": {"body": DEEP}}))
case("deep-json-health", [], 0, must=["WARN  GET /health answered 200 but not"],
     mod=lambda s: s.update({"GET /health": {"body": DEEP}}))
case("deep-json-rpc", [], 0, must=["WARN  net.Version answered HTTP 200 with an unexpected body"],
     mod=lambda s: s.update({"POST /devnet/": {"body": DEEP}}))
case("huge-int-health-timestamp", [], 0, must=["WARN  /health carried no whole-number timestamp"],
     mod=lambda s: s.update({"GET /health": {"body": '{"status":"ok","timestamp":%s}' % HUGE}}))
case("huge-int-index-total", [], 1, must=["FAIL  GET /registry/agents answered 200 but not"],
     mod=lambda s: s.update({"GET /registry/agents": {"body": '{"agents":[],"total":%s}' % HUGE}}))
case("huge-int-sync-finished", [], 0, must=["WARN  the last reconcile record is incomplete"],
     mod=lambda s: s.update({"GET /admin/sync": {"body": '{"running":false,"last":{"trigger":"admin","finishedAt":%s,'
                                                          '"onChain":1,"added":0,"refreshed":1,"failed":0,"verified":0,"error":null}}' % HUGE}}))

# --- limits and unreachable hosts
case("index-body-over-5MB", [], 1, must=["FAIL  GET /registry/agents is unreachable: curl exit"],
     mod=lambda s: s.update({"GET /registry/agents": {"body": "x" * 6_000_000}}))
case("health-hangs-past-15s", ["--skip-rpc"], 1, must=["FAIL  the API is unreachable: curl exit 28"],
     mod=lambda s: s.update({"GET /health": {"sleep": 18, "body": {"status": "ok", "timestamp": int(time.time())}}}))
dead = "http://localhost:%d" % free_port()
case("everything-unreachable", [], 1,
     must=["FAIL  the site is unreachable", "FAIL  the API is unreachable", "FAIL  GET /registry/agents is unreachable",
           "WARN  GET /admin/sync is unreachable", "WARN  the devnet RPC is unreachable"],
     env={"EXPLORER_UI": dead, "EXPLORER_API": dead, "EXPLORER_RPC": dead + "/devnet/"})
secret_base = BASE + "/" + SK
case("secret-in-base-path", ["--skip-rpc"], 1, must=["http://localhost:"], mustnot=[FILL, "sk-ant"],
     env={"EXPLORER_UI": secret_base, "EXPLORER_API": secret_base})
total += 1
if not any(SK in p for p in seen):
    failed.append("secret-in-base-path-reached-server")
    print("FAIL  the base path did not reach the server, so the test above proved nothing")

# --- usage errors
case("usage-unknown-arg", ["--nope"], 2, must=["unknown argument: --nope", "usage:"])
case("usage-env-file-as-arg", [".env"], 2, must=["unknown argument: .env"])
case("usage-secret-as-arg", [SK], 2, must=["unknown argument: <masked>"], mustnot=[FILL])
case("usage-chain-count-no-value", ["--chain-count"], 2, must=["--chain-count needs a value"])
case("usage-chain-count-text", ["--chain-count", "many"], 2, must=["whole number of 0 or more"])
case("usage-chain-count-secret", ["--chain-count", SK], 2, must=["whole number of 0 or more"], mustnot=[FILL])
case("usage-chain-count-negative", ["--chain-count", "-3"], 2, must=["whole number of 0 or more"])
case("usage-sync-hours-zero", ["--sync-hours", "0"], 2, must=["number above 0"])
case("usage-sync-hours-text", ["--sync-hours", "soon"], 2, must=["number above 0"])
case("usage-help", ["--help"], 0, must=["usage: explorer-health.sh"])
case("env-ftp-scheme", [], 2, must=["EXPLORER_API must be an http:// or https:// address"], env={"EXPLORER_API": "ftp://example.test/x"})
FAKE_PW = "hun" + "ter" + "2"  # built at run time so the source holds no password-shaped literal
case("env-userinfo", [], 2, must=["EXPLORER_UI must be an http:// or https:// address"], mustnot=[FAKE_PW],
     env={"EXPLORER_UI": "https://alice:" + FAKE_PW + "@example.test"})
case("env-query-string", [], 2, must=["EXPLORER_RPC must be an http:// or https:// address"], mustnot=["abc123"],
     env={"EXPLORER_RPC": "https://example.test/rpc?key=abc123"})
case("env-garbage", [], 2, must=["EXPLORER_API must be"], env={"EXPLORER_API": "not a url"})
case("env-bad-port-number", [], 2, must=["EXPLORER_API must be"], env={"EXPLORER_API": "http://localhost:99999"})
case("env-bad-port-text", [], 2, must=["EXPLORER_UI must be"], env={"EXPLORER_UI": "http://localhost:abc"})

srv.shutdown()
print("\n%d cases, %d failed" % (total, len(failed)))
if failed:
    print("failed: " + ", ".join(failed))
sys.exit(1 if failed else 0)
