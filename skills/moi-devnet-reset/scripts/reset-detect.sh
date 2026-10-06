#!/usr/bin/env bash
# reset-detect.sh: read-only signals that the MOI devnet was reset, wiped or re-pointed.
#
# Usage:   bash "$SKILLS/moi-devnet-reset/scripts/reset-detect.sh" [options]
#          SKILLS is the folder that holds the moi-* skills. Run it from anywhere; it reads no repo.
# Options: --state FILE         baseline of the last known good state: key=value lines, # comments. Keys used:
#                               version, network_id, genesis_account, genesis_hash (a prefix of at least 16 hex
#                               digits is enough), known_hash, registry (repeat the line or comma-separate).
#                               Values are checked against a strict shape; anything else exits 2.
#          --registry ID        a registry (or other logic) id to look for on chain; repeatable
#          --genesis-account ID a founding account, for example the KMOI asset id from the installed js-moi-sdk
#          --genesis-hash HEX   expected genesis tesseract hash, a prefix of at least 16 hex digits
#          --known-hash HASH    an interaction hash that existed before the event
#          --version V          expected net.Version, for example 0.13.0
#          --network-id N       expected net.NetworkID
#          --rpc URL            read this JSON-RPC endpoint instead of the default devnet path (http or https;
#                               only its host is ever printed). Use a keyless URL: curl receives it as an argument,
#                               so a key in it would show in the process list
#          --no-products        skip the Launchpad, Explorer and MCP reads
#          --no-mcp             skip the one POST to the read-only MCP gateway (a tools/call of a read tool)
#          --no-wait            do not wait 20 seconds and read the Launchpad again when it says stale
#          --print-state        after the reads, print a baseline block to stdout (version and the genesis hash
#                               prefix) for you to save; the script itself writes no file
#          --timeout SEC        per request, default 15
# What it reads (every request is a GET or a JSON-RPC read; nothing is submitted, signed or funded):
#          the node: net.Version and net.NetworkID on the devnet and babylon paths of the Voyage RPC host
#          the genesis tesseract of a founding account (moi.Tesseract, height 0). Its hash is said to change when
#          a network is re-initialised (a local, untracked file of the previous operator; ASK: Adithya for a copy).
#          No reset has yet been watched to confirm it, so treat a change as strong evidence and read
#          references/detect.md
#          each --registry id: moi.AccountMetaInfo (exists?), moi.LogicManifest (the routines the Launchpad
#          package calls are present?)
#          the --known-hash: moi.InteractionByHash
#          products: launchpad.moi.technology /api/stats and /api/marketplace?source=chain, the Explorer API
#          /health and /registry/agents, the MCP /health on both hosts and one read tool call
# Output:  one line per signal, with the UTC time of the read:  HH:MM:SSZ LEVEL  what [host]
#          With no baseline and no id to look for (no version, genesis hash, registry or known hash) every
#          PASS only says the node answers. The script says so in a WARN: such a run cannot show a reset.
#          PASS     the signal matches the baseline, or it is healthy and there is no baseline to compare
#          WARN     not enough to decide: a missing baseline, a method that does not exist, a read that failed
#          CHANGED  the signal shows the reset signature, or differs from the baseline
# Masking: every value taken from a file, an argument or a remote answer is checked first: known key prefixes,
#          JWTs, private-key blocks, secret-named assignments and runs of 12 or more short words become <masked>,
#          and a hex run of 32 digits or more is shown as its first 16 digits and "...". Masking happens before
#          any cut to length. A state file named like an env file (.env, .env.*, *.env) is refused and never opened.
# Exit:    0 no signal changed and every read answered
#          1 at least one CHANGED
#          2 usage error or an unusable state file
#          3 nothing CHANGED but at least one read got no answer (an outage looks green otherwise)
# Writes nothing. Python 3 standard library only. Works under bash 3.2 and zsh.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
export SCRIPT_DIR
exec python3 - "$@" <<'PY'
import json
import os
import re
import sys
import shutil
import subprocess
import time
from urllib.parse import urlsplit

DEVNET = "https://dev.voyage-rpc.moi.technology/devnet/"
BABYLON = "https://dev.voyage-rpc.moi.technology/babylon/"
LAUNCHPAD = "https://launchpad.moi.technology"
EXPLORER_API = "https://api.agents.moi.technology"
MCP_WRITE = "https://mcp.voyage.moi.technology"
MCP_READ = "https://mcp-read.voyage.moi.technology"
# The routines the Launchpad's registry package calls (ops research, 942827a method; read from the live
# registry manifest on 2026-10-03).
REGISTRY_ROUTINES = ["RegisterAgent", "GetAllAgentIds", "GetAgentsByOwner", "GetAgentProfile", "SetAgentStatus",
                     "SetScore", "TransferAgent", "UpdateCard", "UpdateAgentWallet", "GetAgentCount"]
MAX_BODY = 2 * 1024 * 1024
LINE_MAX = 200

USAGE = (
    "usage: reset-detect.sh [--state FILE] [--registry ID]... [--genesis-account ID] [--genesis-hash HEX]\n"
    "                       [--known-hash HASH] [--version V] [--network-id N] [--rpc URL] [--no-products]\n"
    "                       [--no-mcp] [--no-wait] [--print-state] [--timeout SEC]\n"
    "read-only: PASS, WARN or CHANGED per signal. exit: 0 unchanged, 1 CHANGED, 2 usage, 3 a read got no answer"
)

# ---- masking ---------------------------------------------------------------------------------------
TOKEN_RULES = [
    re.compile(r"\bsk-ant-[A-Za-z0-9_-]{8,}"),
    re.compile(r"\bsk-(?!ant-)(?:proj-)?[A-Za-z0-9_-]{16,}"),
    re.compile(r"\bgsk_[A-Za-z0-9]{12,}"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{20,}"),
    re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{12,}"),
    re.compile(r"\b(?:sk|rk)_live_[0-9A-Za-z]{12,}"),
    re.compile(r"\bnpm_[A-Za-z0-9]{20,}"),
    re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}|\bgithub_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"\bxox[abprso]-[A-Za-z0-9-]{8,}"),
    re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{30,}"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"),
    re.compile(r"-----BEGIN (?:[A-Z]+ )*PRIVATE KEY(?: BLOCK)?-----"),
    re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{20,}"),
]
URLPASS = re.compile(r"(\b[a-z][a-z0-9+.-]*://)[^\s/:@]+:[^\s/@]+@", re.IGNORECASE)
ASSIGN = re.compile(
    r"(\b[a-z0-9_]*(?:secret|token|passw(?:or)?d|passphrase|mnemonic|api_?key|private_?key)[a-z0-9_]*[\"']?\s*[=:]\s*[\"']?)"
    r"([A-Za-z0-9+/_=.\-]{16,})", re.IGNORECASE)
HEXRUN = re.compile(r"(0x)?([0-9a-fA-F]{32,})")
PHRASE = re.compile(r"(?:\b[A-Za-z]{3,8}\b[ ,;]+){11,}\b[A-Za-z]{3,8}\b")
STOP = frozenset("after and are been being both but could did does each every for from get got had has her here him "
                 "his how its let many may most not our out per see she should some than the their them these those "
                 "too using via was were which while who why with would yes your".split())


def _phrase(m):
    words = re.findall(r"[A-Za-z]+", m.group(0))
    return m.group(0) if any(w.lower() in STOP for w in words) else "<masked>"


def mask(text):
    """Mask secret-shaped values first, and only then cut to length."""
    text = str(text)
    for rx in TOKEN_RULES:
        text = rx.sub("<masked>", text)
    text = URLPASS.sub(lambda m: m.group(1) + "<masked>@", text)
    text = ASSIGN.sub(lambda m: m.group(1) + "<masked>", text)
    text = PHRASE.sub(_phrase, text)
    text = HEXRUN.sub(lambda m: (m.group(1) or "") + m.group(2)[:16] + "...", text)
    text = " ".join(text.split())
    return text if len(text) <= LINE_MAX else text[:LINE_MAX - 3] + "..."


def short(h):
    """A hex id shown as its first 16 digits (enough to read the registry's short name)."""
    h = str(h)
    m = re.fullmatch(r"(0x)?([0-9a-fA-F]+)", h)
    if not m:
        return mask(h)
    return (m.group(1) or "0x") + m.group(2)[:16] + ("..." if len(m.group(2)) > 16 else "")


def is_env_file(name):
    low = name.lower()
    return low == ".env" or low == ".envrc" or low.startswith(".env.") or low.endswith(".env") or ".env." in low


def die(msg, code=2):
    print("reset-detect: " + mask(msg), file=sys.stderr)
    sys.exit(code)


def hex64(value, what):
    v = str(value).strip()
    if v.lower().startswith("0x"):
        v = v[2:]
    if not re.fullmatch(r"[0-9a-fA-F]{64}", v):
        die("%s must be 64 hex digits, with or without 0x" % what)
    return "0x" + v.lower()


def hexprefix(value, what):
    v = str(value).strip()
    if v.lower().startswith("0x"):
        v = v[2:]
    if not re.fullmatch(r"[0-9a-fA-F]{16,64}", v):
        die("%s must be 16 to 64 hex digits, with or without 0x" % what)
    return v.lower()


def looks_secret(value):
    """True when a value from the state file has a secret shape (not an id or a hash: those are plain hex)."""
    v = str(value)
    if any(rx.search(v) for rx in TOKEN_RULES) or ASSIGN.search(v):
        return True
    return bool(PHRASE.search(v))


# ---- state and arguments -----------------------------------------------------------------------------
class Cfg(object):
    version = None
    network_id = None
    genesis_account = None
    genesis_hash = None
    known_hash = None
    registries = []
    rpc = None
    products = True
    mcp = True
    wait = True
    print_state = False
    timeout = 15.0


def read_state(path, cfg):
    names = [os.path.basename(path)]
    try:
        names.append(os.path.basename(os.path.realpath(path)))
    except OSError:
        pass
    if any(is_env_file(n) for n in names):
        die("refusing to read %s: a state file named like an env file is never opened" % os.path.basename(path))
    try:
        size = os.path.getsize(path)
        if size > 65536:
            die("the state file is over 64 KB; it should hold a handful of lines")
        with open(path, encoding="utf-8", errors="strict") as fh:
            lines = fh.read().splitlines()
    except OSError as e:
        die("cannot read the state file: %s" % e.strerror)
    except UnicodeDecodeError:
        die("the state file is not UTF-8 text")
    ignored = 0
    for n, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            die("state file line %d has no key=value shape" % n)
        key, _, val = line.partition("=")
        key = key.strip().lower()
        val = val.strip()
        if not val:
            continue
        if looks_secret(val):
            die("state file line %d holds something secret-shaped (not echoed). Remove it; ids and hashes only" % n)
        if key == "version":
            if not re.fullmatch(r"[0-9A-Za-z][0-9A-Za-z.+_-]{0,39}", val):
                die("state file line %d: version has an unusual shape" % n)
            cfg.version = cfg.version or val
        elif key == "network_id":
            if not re.fullmatch(r"[0-9]{1,10}", val):
                die("state file line %d: network_id must be a whole number" % n)
            cfg.network_id = cfg.network_id or val
        elif key == "genesis_account":
            cfg.genesis_account = cfg.genesis_account or hex64(val, "genesis_account on line %d" % n)
        elif key == "genesis_hash":
            cfg.genesis_hash = cfg.genesis_hash or hexprefix(val, "genesis_hash on line %d" % n)
        elif key == "known_hash":
            cfg.known_hash = cfg.known_hash or hex64(val, "known_hash on line %d" % n)
        elif key == "registry":
            for part in val.split(","):
                if part.strip():
                    cfg.registries.append(hex64(part, "registry on line %d" % n))
        else:
            ignored += 1
    return ignored


def parse(argv):
    cfg = Cfg()
    cfg.registries = []
    state = None
    i = 0
    while i < len(argv):
        a = argv[i]

        def val():
            if i + 1 >= len(argv):
                die("%s needs a value\n%s" % (a, USAGE))
            return argv[i + 1]

        if a in ("-h", "--help"):
            print(USAGE)
            sys.exit(0)
        elif a == "--state":
            state = val(); i += 1
        elif a == "--registry":
            cfg.registries.append(hex64(val(), "--registry")); i += 1
        elif a == "--genesis-account":
            cfg.genesis_account = hex64(val(), "--genesis-account"); i += 1
        elif a == "--genesis-hash":
            cfg.genesis_hash = hexprefix(val(), "--genesis-hash"); i += 1
        elif a == "--known-hash":
            cfg.known_hash = hex64(val(), "--known-hash"); i += 1
        elif a == "--version":
            v = val(); i += 1
            if not re.fullmatch(r"[0-9A-Za-z][0-9A-Za-z.+_-]{0,39}", v):
                die("--version has an unusual shape")
            cfg.version = v
        elif a == "--network-id":
            v = val(); i += 1
            if not re.fullmatch(r"[0-9]{1,10}", v):
                die("--network-id must be a whole number")
            cfg.network_id = v
        elif a == "--rpc":
            v = val(); i += 1
            if not re.fullmatch(r"https?://[^\s]+", v):
                die("--rpc must be one http:// or https:// URL")
            cfg.rpc = v
        elif a == "--timeout":
            v = val(); i += 1
            try:
                cfg.timeout = float(v)
            except ValueError:
                die("--timeout must be a number of seconds")
            if not 1 <= cfg.timeout <= 120:
                die("--timeout must be between 1 and 120 seconds")
        elif a == "--no-products":
            cfg.products = False
        elif a == "--no-mcp":
            cfg.mcp = False
        elif a == "--no-wait":
            cfg.wait = False
        elif a == "--print-state":
            cfg.print_state = True
        else:
            die("unknown argument %s\n%s" % (mask(a)[:40], USAGE))
        i += 1
    ignored = 0
    if state:
        ignored = read_state(state, cfg)
    seen = set()
    cfg.registries = [r for r in cfg.registries if not (r in seen or seen.add(r))]
    return cfg, ignored


# ---- reading ---------------------------------------------------------------------------------------
def host_of(url):
    try:
        return urlsplit(url).hostname or "?"
    except ValueError:
        return "?"


def request(url, timeout, body=None, headers=None):
    """(status, text, error). Never raises. error is a short masked string when no answer came.
    Uses curl, which reads the system certificate store (Python builds from python.org often do not)."""
    cmd = ["curl", "-sS", "-m", str(int(timeout)), "--proto", "=http,https", "--max-filesize", str(MAX_BODY),
           "-A", "moi-devnet-reset/1 (read-only)", "-w", "\n%{http_code}"]
    for k, v in (headers or {}).items():
        cmd += ["-H", "%s: %s" % (k, v)]
    if body is not None:
        cmd += ["-X", "POST", "--data-binary", "@-"]
    cmd.append(url)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5, input=body)
    except (OSError, subprocess.SubprocessError) as e:
        return None, "", mask("%s" % (e,))[:80]
    out = r.stdout or ""
    head, _, code = out.rpartition("\n")
    if r.returncode != 0 or not code.strip().isdigit() or code.strip() == "000":
        first = (r.stderr or "").strip().splitlines()[:1]
        reason = re.sub(r"^curl: \(\d+\)\s*", "", first[0]) if first else "no answer"
        return None, "", mask(reason)[:80]
    return int(code.strip()), head, None


def rpc(url, method, params, timeout):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
    st, text, err = request(url, timeout, body, {"content-type": "application/json"})
    if err:
        return {"transport": err}
    try:
        d = json.loads(text)
    except ValueError:
        return {"transport": "HTTP %s, not JSON" % st}
    return d if isinstance(d, dict) else {"transport": "HTTP %s, not a JSON object" % st}


class Out(object):
    def __init__(self):
        self.counts = {"PASS": 0, "WARN": 0, "CHANGED": 0}
        self.unread = 0

    def line(self, level, text, host=None, unread=False):
        self.counts[level] += 1
        if unread:
            self.unread += 1
        stamp = time.strftime("%H:%M:%SZ", time.gmtime())
        tail = "  [%s]" % host if host else ""
        print("%s %-7s %s%s" % (stamp, level, mask(text), tail))


def err_text(d):
    e = d.get("error")
    if isinstance(e, dict):
        return "%s %s" % (e.get("code"), e.get("message"))
    return "%s" % (e,)


def main():
    cfg, ignored = parse(sys.argv[1:])
    if not shutil.which("curl"):
        die("curl is not installed; it makes every request here")
    out = Out()
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    print("moi-devnet-reset reset-detect: read-only, started %s" % started)
    if ignored:
        print("note: %d state line(s) use keys this script does not read" % ignored)

    paths = []
    if cfg.rpc:
        paths.append(("rpc", cfg.rpc))
    else:
        paths.append(("devnet path", DEVNET))
        paths.append(("babylon path", BABYLON))
    main_url = paths[0][1]
    mh = host_of(main_url)

    # 1. node build
    versions = {}
    for label, url in paths:
        d = rpc(url, "net.Version", [], cfg.timeout)
        if "transport" in d:
            out.line("WARN", "net.Version got no answer on the %s: %s" % (label, d["transport"]), mh, unread=True)
            continue
        if "result" not in d:
            out.line("WARN", "net.Version on the %s answered an error: %s" % (label, err_text(d)), mh)
            continue
        v = str(d["result"])
        versions[label] = v
        if cfg.version and v != cfg.version:
            out.line("CHANGED", "net.Version on the %s is %s, the baseline says %s. A new build: devnet was wiped "
                     "about a day after a release once so far (2026-09-10 and 11). Not a wipe by itself. ASK: Gokul" % (label, v, cfg.version), mh)
        elif cfg.version:
            out.line("PASS", "net.Version on the %s is %s, as the baseline says" % (label, v), mh)
        else:
            out.line("PASS", "net.Version on the %s is %s (no baseline: compare it with the release by hand)" % (label, v), mh)
    if len(set(versions.values())) > 1:
        out.line("WARN", "the paths report different builds: %s" % ", ".join("%s %s" % kv for kv in versions.items()), mh)

    # 2. network id
    d = rpc(main_url, "net.NetworkID", [], cfg.timeout)
    if "transport" in d:
        out.line("WARN", "net.NetworkID got no answer: %s" % d["transport"], mh, unread=True)
    elif "result" in d:
        nid = str(d["result"])
        if cfg.network_id and nid != cfg.network_id:
            out.line("CHANGED", "net.NetworkID is %s, the baseline says %s" % (nid, cfg.network_id), mh)
        else:
            out.line("PASS", "net.NetworkID is %s%s" % (nid, "" if cfg.network_id else " (no baseline; 112 is the expected value)"), mh)
    else:
        code = (d.get("error") or {}).get("code") if isinstance(d.get("error"), dict) else None
        out.line("WARN", "net.NetworkID answered error %s (-32601 is method not found, as on 2026-10-02 and 2026-10-03): "
                 "the network ID cannot be read from the node. ASK: Gokul" % code, mh)

    # 3. genesis tesseract of a founding account
    genesis_seen = None
    if not cfg.genesis_account:
        out.line("WARN", "genesis check skipped: no --genesis-account. Pass the KMOI asset id from the installed "
                 "js-moi-sdk (KMOI_ASSET_ID), see references/detect.md", mh)
    else:
        hashes = {}
        for label, url in paths:
            params = [{"id": cfg.genesis_account, "with_interactions": False, "with_commit_info": False,
                       "options": {"tesseract_number": 0}}]
            d = rpc(url, "moi.Tesseract", params, cfg.timeout)
            if "transport" in d:
                out.line("WARN", "genesis read got no answer on the %s: %s" % (label, d["transport"]), mh, unread=True)
                continue
            res = d.get("result")
            if not isinstance(res, dict) or "hash" not in res:
                msg = err_text(d)
                if "account not found" in msg.lower():
                    out.line("CHANGED", "the founding account %s does not exist on the %s: the network was wiped, or the "
                             "id moved, or the id came from an old SDK (KMOI's id changed at v0.13.0)" % (short(cfg.genesis_account), label), mh)
                else:
                    out.line("WARN", "genesis read on the %s answered an error: %s. Check the founding account id: an SDK older "
                             "than 0.9.0-rc2 prints KMOI's retired id" % (label, msg), mh)
                continue
            h = str(res["hash"]).lower()
            hashes[label] = h
            genesis_seen = genesis_seen or h
            hexpart = h[2:] if h.startswith("0x") else h
            if cfg.genesis_hash:
                if hexpart.startswith(cfg.genesis_hash):
                    out.line("PASS", "genesis tesseract %s on the %s matches the baseline: not re-initialised since" % (short(h), label), mh)
                else:
                    out.line("CHANGED", "genesis tesseract is now %s on the %s, the baseline starts %s: the network was "
                             "re-initialised since the baseline" % (short(h), label, "0x" + cfg.genesis_hash[:16]), mh)
            else:
                out.line("PASS", "genesis tesseract %s on the %s (no baseline: save it with --print-state)" % (short(h), label), mh)
        if len(set(hashes.values())) > 1:
            out.line("WARN", "the two paths hold different genesis tesseracts, so they are different networks", mh)
        elif len(hashes) == 2:
            out.line("PASS", "both paths hold the same genesis tesseract (consistent with one network)", mh)

    # 4. registries
    for reg in cfg.registries:
        d = rpc(main_url, "moi.AccountMetaInfo", [{"id": reg}], cfg.timeout)
        if "transport" in d:
            out.line("WARN", "registry %s: no answer: %s" % (short(reg), d["transport"]), mh, unread=True)
            continue
        res = d.get("result")
        if not isinstance(res, dict):
            msg = err_text(d)
            if "account not found" in msg.lower():
                out.line("CHANGED", "registry %s does not exist on this network (account not found): it was wiped or replaced" % short(reg), mh)
            else:
                out.line("WARN", "registry %s: error %s" % (short(reg), msg), mh)
            continue
        out.line("PASS", "registry %s exists (type %s, height %s). A read cannot show that writes still execute "
                 "(2026-08-06): only a registration receipt can" % (short(reg), res.get("type"), res.get("height")), mh)
        m = rpc(main_url, "moi.LogicManifest", [{"logic_id": reg, "encoding": "JSON", "options": {"tesseract_number": -1}}], cfg.timeout)
        names = None
        if isinstance(m.get("result"), str):
            try:
                raw = m["result"]
                manifest = json.loads(bytes.fromhex(raw[2:] if raw.startswith("0x") else raw))
                names = set()
                for el in manifest.get("elements", []):
                    data = el.get("data") if isinstance(el, dict) else None
                    if isinstance(data, dict) and data.get("name"):
                        names.add(str(data["name"]))
            except (ValueError, AttributeError, TypeError):
                names = None
        if names is None:
            out.line("WARN", "registry %s: the manifest could not be read or parsed" % short(reg), mh)
        else:
            missing = [r for r in REGISTRY_ROUTINES if r not in names]
            if missing:
                out.line("WARN", "registry %s lacks routines the Launchpad package calls: %s" % (short(reg), ", ".join(missing)), mh)
            else:
                out.line("PASS", "registry %s exposes all %d routines the Launchpad package calls" % (short(reg), len(REGISTRY_ROUTINES)), mh)

    # 5. a hash that existed before
    if cfg.known_hash:
        d = rpc(main_url, "moi.InteractionByHash", [{"hash": cfg.known_hash}], cfg.timeout)
        if "transport" in d:
            out.line("WARN", "known hash %s: no answer: %s" % (short(cfg.known_hash), d["transport"]), mh, unread=True)
        elif isinstance(d.get("result"), dict):
            out.line("PASS", "known hash %s is still on chain" % short(cfg.known_hash), mh)
        else:
            out.line("CHANGED", "known hash %s is not found (%s): the network was wiped since it was made, or the hash "
                     "was never on this network" % (short(cfg.known_hash), err_text(d)), mh)

    # no baseline at all: a PASS above only says the node answers
    if not (cfg.version or cfg.genesis_hash or cfg.registries or cfg.known_hash):
        out.line("WARN", "no baseline, so this run cannot show a reset: a PASS only says the node answers. "
                 "Build one from values that predate the event: references/detect.md, First baseline", mh)
    elif cfg.genesis_hash and not cfg.genesis_account:
        out.line("WARN", "genesis_hash is set but no genesis account was given, so the genesis hash was not compared", mh)

    # 6. products
    if cfg.products:
        launchpad(cfg, out)
        explorer(cfg, out)
        mcp(cfg, out)

    print("")
    c = out.counts
    print("Summary: %d PASS, %d WARN, %d CHANGED. %d read(s) got no answer. Nothing was written." % (c["PASS"], c["WARN"], c["CHANGED"], out.unread))
    if c["CHANGED"]:
        print("A CHANGED line is a suspected reset or a dead product, not proof. Next: references/detect.md, section Decide.")
    if cfg.print_state:
        print("")
        print("# baseline read %s by reset-detect.sh (public ids and hash prefixes only; save it yourself)" % started)
        for label, v in list(versions.items())[:1]:
            print("version=%s" % mask(v))
        if genesis_seen:
            gs = genesis_seen[2:] if genesis_seen.startswith("0x") else genesis_seen
            print("genesis_hash=0x%s" % gs[:24])
        print("# genesis_account, registry and known_hash take full 66-character ids and hashes, which this script never prints.")
        print("# Write them yourself from the SDK constants and the protocol team's message. Full-line comments only; no inline comments.")
    if c["CHANGED"]:
        sys.exit(1)
    sys.exit(3 if out.unread else 0)


def jget(text):
    try:
        d = json.loads(text)
        return d if isinstance(d, dict) else None
    except ValueError:
        return None


def launchpad(cfg, out):
    host = host_of(LAUNCHPAD)
    st, text, err = request(LAUNCHPAD + "/api/stats", cfg.timeout)
    d = jget(text) if st == 200 else None
    if err or d is None:
        out.line("WARN", "Launchpad /api/stats got no usable answer (%s). A host outage is DevOps's: ASK: Upendhar" %
                 (err or "HTTP %s" % st), host, unread=True)
    else:
        status = d.get("chainStatus")
        if status != "ok" and cfg.wait:
            print("      Launchpad says %s; the chain refresh is request-driven, so waiting 20 seconds and reading again" % mask(status))
            time.sleep(20)
            st, text, err = request(LAUNCHPAD + "/api/stats", cfg.timeout)
            d2 = jget(text) if st == 200 else None
            d = d2 or d
            status = d.get("chainStatus")
        chain_err = d.get("chainError")
        if status == "ok":
            age = ""
            try:
                age = ", read %ds ago" % max(0, int(time.time() - int(d["chainAsOf"]) / 1000))
            except (KeyError, ValueError, TypeError, OverflowError):
                pass
            out.line("PASS", "Launchpad chainStatus ok (%s active agents%s)" % (d.get("activeAgents"), age), host)
        elif chain_err and "account not found" in str(chain_err).lower():
            out.line("CHANGED", "Launchpad chainStatus %s with 'account not found': its registry or read caller is gone" % status, host)
        else:
            out.line("WARN", "Launchpad chainStatus %s, chainError %s" % (status, chain_err), host)
    st, text, err = request(LAUNCHPAD + "/api/marketplace?source=chain", cfg.timeout)
    if st == 502 and cfg.wait:
        print("      the chain marketplace answered 502; reading once more in 5 seconds to rule out a blip")
        time.sleep(5)
        again, text2, err2 = request(LAUNCHPAD + "/api/marketplace?source=chain", cfg.timeout)
        if err2 is None:
            if again == 502:
                text = text2
            else:
                st = again if again != 200 else -200
    if err:
        out.line("WARN", "Launchpad /api/marketplace?source=chain got no answer (%s)" % err, host, unread=True)
    elif st == 200:
        out.line("PASS", "Launchpad marketplace read from the chain answers 200", host)
    elif st == -200:
        out.line("WARN", "Launchpad marketplace read from the chain answered 502 once, then 200: a blip, not a reset signal", host)
    elif st == 502 and cfg.wait:
        d2 = jget(text) or {}
        out.line("CHANGED", "Launchpad marketplace read from the chain answers 502 twice (%s): the registry it points at cannot be read" %
                 (d2.get("error") or "chain_unreachable"), host)
    elif st == 502:
        out.line("WARN", "Launchpad marketplace read from the chain answered 502 and was not read again (--no-wait). Read it again before believing it", host)
    else:
        out.line("WARN", "Launchpad marketplace read from the chain answers HTTP %s" % st, host)


def explorer(cfg, out):
    host = host_of(EXPLORER_API)
    st, text, err = request(EXPLORER_API + "/health", cfg.timeout)
    d = jget(text) if st == 200 else None
    if err or d is None:
        out.line("WARN", "Explorer API /health got no usable answer (%s). ASK: Upendhar (VM), Gokul (app)" % (err or "HTTP %s" % st), host, unread=True)
        return
    out.line("PASS", "Explorer API process is up (status %s). That says nothing about the index" % d.get("status"), host)
    st, text, err = request(EXPLORER_API + "/registry/agents", cfg.timeout)
    d = jget(text) if st == 200 else None
    if err or d is None:
        out.line("WARN", "Explorer /registry/agents got no usable answer (%s)" % (err or "HTTP %s" % st), host, unread=True)
    else:
        out.line("WARN", "Explorer index lists %s agent(s). Not a wipe signal: the index is not cleared by a reset, so compare it "
                 "with the registry count (moi-launchpad-ops/explorer)" % d.get("total"), host)


def mcp(cfg, out):
    for name, base in (("write gateway", MCP_WRITE), ("read gateway", MCP_READ)):
        host = host_of(base)
        st, text, err = request(base + "/health", cfg.timeout)
        d = jget(text) if st == 200 else None
        if err or d is None:
            out.line("WARN", "MCP %s /health got no usable answer (%s). ASK: Upendhar (VM)" % (name, err or "HTTP %s" % st), host, unread=True)
        elif d.get("ok") is True:
            out.line("PASS", "MCP %s /health ok" % name, host)
        else:
            out.line("WARN", "MCP %s /health says ok=%s" % (name, d.get("ok")), host)
    if not cfg.mcp:
        return
    host = host_of(MCP_READ)
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                       "params": {"name": "moi_resolve_agent", "arguments": {"query": "agent"}}})
    st, text, err = request(MCP_READ + "/mcp", cfg.timeout, body,
                            {"content-type": "application/json", "accept": "application/json, text/event-stream"})
    if err:
        out.line("WARN", "MCP read gateway tool call got no answer (%s)" % err, host, unread=True)
        return
    payload = None
    for ln in text.splitlines():
        if ln.startswith("data:"):
            payload = jget(ln[5:].strip())
            break
    if payload is None:
        payload = jget(text)
    if payload is None:
        out.line("WARN", "MCP read gateway tool call: HTTP %s, answer not understood" % st, host)
        return
    err = payload.get("error")
    if err is not None:
        out.line("WARN", "MCP read gateway tool call answered a protocol error: %s" % (err if not isinstance(err, dict) else
                 "%s %s" % (err.get("code"), err.get("message"))), host)
        return
    res = payload.get("result")
    if not isinstance(res, dict):
        out.line("WARN", "MCP read gateway tool call: answer not understood", host)
        return
    content = res.get("content") if isinstance(res.get("content"), list) else []
    msg = " ".join(str(c.get("text", "")) for c in content if isinstance(c, dict))
    if res.get("isError"):
        low = msg.lower()
        if "account not found" in low or "could not load the moi agent registry" in low:
            out.line("CHANGED", "MCP read gateway cannot load its registry (account not found): it still points at a registry that is gone", host)
        else:
            out.line("WARN", "MCP read gateway tool call failed: %s" % msg, host)
    elif not msg.strip():
        out.line("WARN", "MCP read gateway tool call returned no text, so nothing shows the registry was read", host)
    else:
        out.line("PASS", "MCP read gateway answered a registry read with no error (this does not show that writes work)", host)


main()
PY
