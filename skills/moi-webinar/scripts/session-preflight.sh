#!/usr/bin/env bash
# session-preflight.sh: read-only checks before a rehearsal or the live run of a MOI Builders session.
#
# Usage:   bash "$SKILLS/moi-webinar/scripts/session-preflight.sh" [--offline] [<session-folder>]
#          Run it from the root of the working copy of moi-foundation/MOI-Webinars.
#          SKILLS is the folder that holds the moi-* skills.
#          --offline   skip the three network reads (devnet net.Version, net.NetworkID, explorer).
# Checks:  1. Tools and versions the demo needs: git, node (the live scripts run .ts files with plain
#             node, so the version matters), npm, python3; Chrome, coco, pdfinfo, vhs and ffmpeg only
#             matter for the deck PDF, a logic recompile and the rehearsal video, so they WARN.
#          2. With a folder: its name (session-<N>), package.json, node_modules, that .env exists and is
#             ignored by git and not tracked (the file is never opened), the .env.example header number,
#             the event page title numeral against N, unresolved fill-in markers and template notes in the
#             session documents, the slide count the run sheet states against the deck, and moi-webinar/deck's
#             check-deck.py on deck/index.html (any FAIL there is a FAIL here).
#          3. Devnet (unless --offline), two JSON-RPC read methods and one explorer GET. The endpoint is the
#             first devnet RPC URL in moi-devrel/references/devnet.md. net.Version is compared with what
#             the release says by you, by hand. net.NetworkID answered "method not found" on 2026-10-02,
#             so that is a WARN, not a FAIL.
# Does not: run npm, a demo, a setup script or the session's own preflight; open any .env file; write
#          anything; send anything. It cannot see accounts, balances or LOGIC_ID: the session's own
#          `npm run preflight` reads those and spends nothing. Wire field names (payer or fee_payer) are not
#          checked here: devnet.md, "Before you say live", step 3.
# Output:  PASS, WARN or FAIL per line, then a summary. Read every WARN: they do not change the exit code.
# Env:     SKILLS, when set, is where moi-devrel/references/devnet.md and the deck branch (moi-webinar/deck)
#          are looked for first; otherwise they are found beside this skill.
#          SESSION_PREFLIGHT_RPC overrides the devnet RPC URL. It must start with http:// or https://.
#          Only the scheme, host and port are ever printed, because a URL can carry a key in its path.
# Exit:    0 no FAIL, 1 at least one FAIL, 2 bad usage, a folder that does not exist, or an env-named
#          argument (refused, never opened). A file it cannot read is a WARN, never a crash.
# Works under bash 3.2 and zsh (run it with bash). Python 3 standard library only.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
export SCRIPT_DIR
exec python3 - "$@" <<'PY'
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from urllib.parse import urlsplit

SCRIPT_DIR = os.environ["SCRIPT_DIR"]
OWN_LIBRARY = os.path.dirname(os.path.dirname(SCRIPT_DIR))


def sibling(rel):
    """A file of another skill or branch: under $SKILLS when set, else beside this skill."""
    for base in (os.environ.get("SKILLS", ""), OWN_LIBRARY):
        if base and os.path.isfile(os.path.join(base, rel)):
            return os.path.join(base, rel)
    return os.path.join(OWN_LIBRARY, rel)


DEVNET_MD = sibling("moi-devrel/references/devnet.md")
FALLBACK_RPC = "https://dev.voyage-rpc.moi.technology/devnet/"
EXPLORER = "https://voyage.moi.technology/"

counts = {"PASS": 0, "WARN": 0, "FAIL": 0}


def say(level, msg):
    counts[level] += 1
    print("%-5s %s" % (level, msg))


def note(msg):
    print("      " + msg)


def run(cmd, timeout=15):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except (OSError, subprocess.SubprocessError) as e:
        return 127, str(e)


def first_line(text):
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


unreadable = []


def read_text(path):
    """The text of a file, or "" when it cannot be read (the path is remembered for one WARN)."""
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        unreadable.append(path)
        return ""


def where(url):
    """scheme://host[:port]/... of a URL, so that a key in its path or its user part is never printed."""
    try:
        u = urlsplit(url)
        host = u.hostname or "?"
        port = ":%d" % u.port if u.port else ""
        return "%s://%s%s/..." % (u.scheme, host, port)
    except ValueError:
        return "the URL given in SESSION_PREFLIGHT_RPC"


def strip_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def roman_to_int(s):
    vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    prev = 0
    for ch in reversed(s):
        v = vals[ch]
        total += v if v >= prev else -v
        prev = max(prev, v)
    return total


def usage(code=2):
    print('usage: session-preflight.sh [--offline] [<session-folder>]', file=sys.stderr if code else sys.stdout)
    sys.exit(code)


args = sys.argv[1:]
offline = False
folder = None
for a in args:
    if a in ("-h", "--help"):
        usage(0)
    elif a == "--offline":
        offline = True
    elif a.startswith("-"):
        usage()
    elif folder is None:
        folder = a.rstrip("/") or a
    else:
        usage()

# Bad input is exit 2, before any check runs. Exit 1 stays for "checked and found a FAIL".
if folder is not None:
    low = os.path.basename(os.path.abspath(folder)).lower()
    if low in (".env", ".envrc") or low.startswith(".env.") or low.endswith(".env") or ".env." in low:
        print("session-preflight: refusing %s: an env file can hold keys and is never opened. "
              "Pass the session folder instead." % os.path.basename(os.path.abspath(folder)), file=sys.stderr)
        sys.exit(2)
    if not os.path.isdir(folder):
        print("session-preflight: %s is not a folder here. Run this from the root of the working copy "
              "of moi-foundation/MOI-Webinars and name a session folder such as session-10." % folder, file=sys.stderr)
        sys.exit(2)

# ---------------------------------------------------------------- 1. tools
print("Tools")
rc, out = run(["git", "--version"])
if rc == 0:
    say("PASS", "git present (%s)" % first_line(out))
else:
    say("FAIL", "git is missing")

node_major = None
if shutil.which("node"):
    rc, out = run(["node", "--version"])
    v = first_line(out)
    m = re.match(r"v?(\d+)\.", v)
    node_major = int(m.group(1)) if m else None
    if node_major is None:
        say("FAIL", "node answered %r, which is not a version" % v)
    elif node_major < 20:
        say("FAIL", "node %s is below 20, the engines floor of the session packages" % v)
    elif node_major < 24:
        say("WARN", "node %s: the session 8 live scripts run as plain `node scripts/tick.ts` and their author used Node 24; "
                    "the packages say >=20. Rehearse on the machine you present from" % v)
    else:
        say("PASS", "node %s (Node 24 was the author's version when the session 8 live scripts were written)" % v)
else:
    say("FAIL", "node is missing: the demo scripts need it")

if shutil.which("npm"):
    rc, out = run(["npm", "--version"])
    say("PASS", "npm present (%s)" % first_line(out))
else:
    say("FAIL", "npm is missing: the demo is run with npm run commands")

pv = sys.version_info
if pv >= (3, 9):
    say("PASS", "python3 %d.%d.%d (deck checks, time-table.sh)" % pv[:3])
else:
    say("WARN", "python3 %d.%d is below 3.9, which time-table.sh needs" % pv[:2])

chrome = None
for cand in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",):
    if os.path.exists(cand):
        chrome = cand
for name in ("google-chrome", "chromium", "chrome"):
    if not chrome and shutil.which(name):
        chrome = shutil.which(name)
say("PASS" if chrome else "WARN", "Chrome present (deck PDF export)" if chrome else "Chrome not found: only the deck PDF export needs it")

coco_version = None
if shutil.which("coco"):
    rc, out = run(["coco", "version"])
    m = re.search(r"^Coco\s+(\d+\.\d+\.\d+)", out, re.M)
    coco_version = m.group(1) if m else None
    say("PASS", "coco present (%s)" % (("Coco " + coco_version) if coco_version else "version not read"))
else:
    say("WARN", "coco not found: only needed to recompile a logic (the checked-in manifest runs without it)")

for tool, why in (("pdfinfo", "checking a PDF's page count"), ("vhs", "recording the rehearsal video"),
                  ("ffmpeg", "assembling a voiceover")):
    if shutil.which(tool):
        say("PASS", "%s present" % tool)
    else:
        say("WARN", "%s not found: only needed for %s" % (tool, why))

# ---------------------------------------------------------------- 2. the session folder
if folder is not None:
    print("")
    print("Session folder %s" % folder)
    base = os.path.basename(os.path.abspath(folder))
    if not os.path.isdir(folder):
        say("FAIL", "%s is not a folder here. Run this from the root of the working copy" % folder)
    else:
        m = re.match(r"^session-(\d+)(?:-[a-z0-9]+)*$", base)
        n = int(m.group(1)) if m else None
        if n is None:
            say("WARN", "the folder name %r does not look like session-<N>, so the numeral checks are skipped" % base)
        else:
            say("PASS", "folder name gives session number %d" % n)

        pkg = os.path.join(folder, "package.json")
        scripts = {}
        if os.path.isfile(pkg):
            try:
                with open(pkg, encoding="utf-8") as fh:
                    data = json.load(fh)
                if not isinstance(data, dict):
                    raise ValueError("package.json is not a JSON object")
                if isinstance(data.get("scripts"), dict):
                    scripts = data["scripts"]
                engines = data.get("engines")
                eng = engines.get("node") if isinstance(engines, dict) else None
                say("PASS", "package.json present (engines.node %s)" % (eng if isinstance(eng, str) and eng else "not set"))
            except (OSError, ValueError):
                say("WARN", "package.json could not be read as a JSON object")
        else:
            say("WARN", "no package.json: fine for a talk with no demo code, a problem for a demo")

        if os.path.isdir(os.path.join(folder, "node_modules")) or os.path.isdir("node_modules"):
            say("PASS", "node_modules present")
        elif os.path.isfile(pkg):
            say("WARN", "node_modules is missing: run npm install yourself (this script does not)")

        envp = os.path.join(folder, ".env")
        if os.path.exists(envp):
            inside = run(["git", "-C", folder, "rev-parse", "--is-inside-work-tree"])[0] == 0
            if not inside:
                say("WARN", ".env exists (not opened), but this is not a git repository, so its ignore state is unknown")
            else:
                ignored = run(["git", "-C", folder, "check-ignore", "-q", ".env"])[0] == 0
                tracked = run(["git", "-C", folder, "ls-files", "--error-unmatch", ".env"])[0] == 0
                if tracked:
                    say("FAIL", ".env is tracked by git: remove it from the index and treat its contents as exposed")
                elif not ignored:
                    say("FAIL", ".env exists and git does not ignore it: add it to .gitignore before anything else")
                else:
                    say("PASS", ".env exists (not opened) and is ignored by git")
        else:
            say("WARN", "no .env yet: copy .env.example and fill it in yourself. Never paste a recovery phrase into the chat")

        ex = os.path.join(folder, ".env.example")
        if n is not None and os.path.isfile(ex):
            head = read_text(ex).splitlines()[:5]
            nums = set()
            for line in head:
                for hit in re.findall(r"#\s*(\d+)", line):
                    nums.add(int(hit))
            if nums and n not in nums:
                say("WARN", ".env.example header names session %s, the folder is %d (the session-8 first-design and session-9 folders carried a stale #7)"
                    % (",".join(str(x) for x in sorted(nums)), n))
            elif nums:
                say("PASS", ".env.example header number matches")

        docs = ["README.md", "STORYLINE.md", "NOTES.md", "RUNBOOK.md", "GAMEDAY.md", "LUMA.md", "SOCIAL.md", "SCRIPT.md"]
        present = [d for d in docs if os.path.isfile(os.path.join(folder, d))]
        social = sorted(p for p in glob.glob(os.path.join(folder, "social", "*.txt")) if os.path.isfile(p))

        # event page numeral against N
        luma = os.path.join(folder, "LUMA.md")
        if n is not None and os.path.isfile(luma):
            text = strip_comments(read_text(luma))
            found = None
            for line in text.splitlines():
                mm = re.search(r"MOI Builders\s+(?:#\s*(\d+)|([IVXLCDM]+)\b)", line)
                if mm:
                    found = (mm.group(1), mm.group(2), line.strip())
                    break
            if not found:
                say("WARN", "LUMA.md has no 'MOI Builders #N' or 'MOI Builders <numeral>' title line to check")
            else:
                shown = int(found[0]) if found[0] else roman_to_int(found[1])
                if shown != n:
                    say("FAIL", "LUMA.md title says session %d, the folder is session %d (session 8's live page read VII on 2 Sep 2026)" % (shown, n))
                else:
                    say("PASS", "LUMA.md title numeral matches the folder")
            note("the live page can differ from LUMA.md: open the page and read its title yourself")
        elif os.path.isdir(folder) and n is not None:
            say("WARN", "no LUMA.md: the event page copy is not written yet")

        # placeholders
        marker = re.compile(r"\bFILL\b|\bTODO\b|<<<|REPLACE-WITH|LUMA_URL|EVENT_URL|CANONICAL_URL|TEMPLATE NOTES")  # slop-lint:ignore
        hits = []
        for d in present:
            c = sum(1 for line in read_text(os.path.join(folder, d)).splitlines() if marker.search(line))
            if c:
                hits.append("%s (%d)" % (d, c))
        for p in social:
            c = sum(1 for line in read_text(p).splitlines() if marker.search(line))
            if c:
                hits.append("social/%s (%d)" % (os.path.basename(p), c))
        if hits:
            say("WARN", "unresolved markers (FILL, TODO, template notes, an event or canonical URL placeholder, ...): " + ", ".join(hits))  # slop-lint:ignore
        elif present:
            say("PASS", "no unresolved markers in the session documents")

        # slide count the run sheet states against the deck
        deck = os.path.join(folder, "deck", "index.html")
        count = None
        if os.path.isfile(deck):
            html = read_text(deck)
            count = len(re.findall(r'<section\s+class="slide[\s"]', html))
        if count is not None:
            for d in ("RUNBOOK.md", "GAMEDAY.md"):
                p = os.path.join(folder, d)
                if not os.path.isfile(p):
                    continue
                stated = None
                for line in [l for l in strip_comments(read_text(p)).splitlines() if l.strip()][:12]:
                    mm = re.search(r"(\d+)\s+slides", line)
                    if mm:
                        stated = int(mm.group(1))
                        break
                if stated is not None and stated != count:
                    say("WARN", "%s says %d slides, the deck has %d (session 8: 18 against 19, so slide numbers drifted by one)"
                        % (d, stated, count))
                elif stated is not None:
                    say("PASS", "%s slide count matches the deck" % d)

        # the deck check, through moi-webinar/deck
        checker = sibling("moi-webinar/deck/scripts/check-deck.py")
        if count is None:
            say("WARN", "no deck/index.html yet")
        elif not os.path.isfile(checker):
            say("WARN", "moi-webinar/deck's check-deck.py was not found under $SKILLS or inside this skill, so the deck was not checked")
        else:
            cmd = [sys.executable, checker, deck]
            sp = os.path.join(folder, "SCRIPT.md")
            if os.path.isfile(sp):
                cmd += ["--script", sp]
            rc, out = run(cmd, timeout=90)
            result = ""
            fail_lines = []
            for line in out.splitlines():
                if line.startswith("RESULT:"):
                    result = line.strip()
                if line.startswith("FAIL"):
                    fail_lines.append(line.strip()[:150])
            if rc == 0:
                say("PASS", "deck check: " + (result or "no FAIL"))
            else:
                say("FAIL", "deck check failed. " + (result or "see check-deck.py output"))
                for line in fail_lines[:4]:
                    note(line)
                note("a deck that prints a perfect PDF can still be dead live: fix before presenting")

        if "preflight" in scripts:
            note("next, by you: run `npm run preflight` in %s (reads only; checks accounts and the logic id)" % folder)
        if "demo" in scripts or any(k.startswith("setup") for k in scripts):
            note("`npm run demo` and the setup scripts spend devnet funds: they need the operator's yes")

        nut = os.path.join(folder, "ticker-logic", "coco.nut")
        for cand in glob.glob(os.path.join(folder, "*", "coco.nut")):
            nut = cand
            break
        if coco_version and os.path.isfile(nut):
            mm = re.search(r'^\s*version\s*=\s*"(\d+\.\d+\.\d+)"', read_text(nut), re.M)
            if mm and mm.group(1).rsplit(".", 1)[0] != coco_version.rsplit(".", 1)[0]:
                say("WARN", "the logic was built with coco %s, your compiler is %s: recompile only if you edit the logic, and rehearse after"
                    % (mm.group(1), coco_version))

        if unreadable:
            say("WARN", "could not read %d file(s), so they were not checked: %s" % (len(unreadable), ", ".join(sorted(set(unreadable))[:5])))

# ---------------------------------------------------------------- 3. devnet
print("")
print("Devnet")
if offline:
    say("WARN", "--offline: devnet and explorer were not read")
else:
    rpc = os.environ.get("SESSION_PREFLIGHT_RPC", "")
    if not rpc:
        md = read_text(DEVNET_MD)
        mm = re.search(r"https://dev\.voyage-rpc\.moi\.technology/devnet/", md)
        rpc = mm.group(0) if mm else FALLBACK_RPC
    if not re.match(r"^https?://[^\s]+$", rpc):
        say("FAIL", "SESSION_PREFLIGHT_RPC must be one URL that starts with http:// or https://. Devnet was not read")
    elif not shutil.which("curl"):
        say("WARN", "curl not found: devnet was not read")
    else:
        why = []  # curl's own reason for the last failed read, with the URL taken out

        def call(method):
            body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": []})
            rc, out = run(["curl", "-sS", "-m", "15", "--proto", "=http,https", "-X", "POST", rpc,
                           "-H", "content-type: application/json", "-d", body], timeout=25)
            if rc != 0 or not out.strip():
                why[:] = [re.sub(r"\S*://\S*", "<URL>", first_line(out).replace(rpc, "<URL>"))[:120]] if out.strip() else []
                return None
            try:
                data = json.loads(out)
            except ValueError:
                return None
            return data if isinstance(data, dict) else None

        def short(value):
            return str(value)[:40]

        r = call("net.Version")
        if r is None:
            say("FAIL", "devnet RPC did not answer net.Version at %s: the live demo depends on it%s"
                % (where(rpc), (" (curl said: %s)" % why[0]) if why else ""))
        elif "result" in r:
            say("PASS", "net.Version %s (0.13.0 on 2026-10-02). Compare it with the release before you say anything is live" % short(r["result"]))
        else:
            say("FAIL", "net.Version returned an error: %s" % json.dumps(r.get("error"))[:120])

        r = call("net.NetworkID")
        if r is None:
            say("WARN", "net.NetworkID was not read (no answer)")
        elif "result" in r:
            say("PASS", "net.NetworkID %s (devnet is expected to be 112, only that value has two sources)" % short(r["result"]))
        else:
            err = r.get("error")
            code = err.get("code") if isinstance(err, dict) else None
            say("WARN", "net.NetworkID answered error %s (-32601 means method not found, as on 2026-10-02): "
                        "the network ID is not confirmed. ASK: Gokul" % short(code))

        rc, out = run(["curl", "-s", "-m", "15", "-o", "/dev/null", "-w", "%{http_code}", EXPLORER], timeout=25)
        code = out.strip()
        if code == "200":
            say("PASS", "explorer answers 200 (it can lag the chain by minutes: a hash may not show at once)")
        else:
            say("WARN", "explorer answered %r: have the receipts in NOTES.md ready as the fallback" % code)

print("")
print("Not checked here: accounts and balances, the logic id, and the wire field names. See the header of this script.")
print("Summary: %d PASS, %d WARN, %d FAIL." % (counts["PASS"], counts["WARN"], counts["FAIL"]))
sys.exit(1 if counts["FAIL"] else 0)
PY
