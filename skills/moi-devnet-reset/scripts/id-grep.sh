#!/usr/bin/env bash
# id-grep.sh: list every file and line under the given paths that pins a MOI id or address.
#
# Use it after a devnet reset to find where the OLD registry id (or market contract id, asset id,
# read caller) is still written, and again to check where the NEW one now stands.
#
# Usage:   bash "$SKILLS/moi-devnet-reset/scripts/id-grep.sh" [--files] [--no-short] <id> <path> [<path>...]
#          <id>     8 to 64 hex digits, with or without a leading 0x. An id is public on chain; never pass a
#                   key or a recovery phrase here.
#          <path>   a file or a folder (walked recursively). SKILLS is the folder that holds the moi-* skills.
#          --files  print one line per file with its hit count, not one line per hit.
#          --no-short  do not also search the short name (see below).
# Matching: case-insensitive, with or without 0x. A registry or other logic id (64 hex digits starting
#          20000000) is also searched by its short name, the 8 hex digits at positions 9 to 16
#          (0x20000000c684f926... is called c684f926 in code comments and docs). That finds truncated
#          copies such as "0x20000000c684f926...". Any other 64-digit id (an asset id such as KMOI's, an
#          account) is also searched by its first 16 digits, because the digits at positions 9 to 16 are
#          shared by KMOI's old and new ids and would flag the wrong one. A hit is labelled [full],
#          [short] or [prefix].
# Output:  path:line:[full|short|prefix] excerpt   (stdout). The excerpt is the line with every secret-shaped
#          value masked first (known key prefixes, JWTs, private-key blocks, URL passwords, bearer tokens,
#          secret-named assignments, runs of 12 or more short words, and any hex run of 32 digits or more,
#          which is shortened to its first 16 digits, the searched id included), then cut to 160
#          characters. A summary goes to stderr: hits, files scanned, and what was skipped.
# Skips:   .git, node_modules and build folders; binary files; files over 2 MB; symlinks; anything that is
#          not a regular file (a named pipe, a socket, a device); and every env-named file (.env, .env.*,
#          *.env, anything containing .env.), which is NEVER opened. That includes .env.example and
#          .env.production.example: search those with plain grep for the 16-digit prefix of the id.
# Exit:    0 at least one hit
#          1 no hit, everything given was read (the id is not pinned in these paths)
#          2 usage error, a path that is missing or unreadable, or an env-named file given on the command
#            line. The scan is incomplete, so a "no hit" means nothing until it is fixed.
# Read-only: writes nothing, calls no network. Python 3 standard library only. Works under bash 3.2 and zsh.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
export SCRIPT_DIR
exec python3 - "$@" <<'PY'
import os
import re
import stat
import sys

SKIP_DIRS = {".git", "node_modules", ".next", "dist", "build", ".venv", "venv", "__pycache__", ".cache",
             "coverage", ".turbo", ".astro", ".svn", ".hg"}
MAX_BYTES = 2 * 1024 * 1024
EXCERPT_MAX = 160

USAGE = (
    "usage: id-grep.sh [--files] [--no-short] <id> <path> [<path>...]\n"
    "  <id>  8 to 64 hex digits, with or without 0x (an id is public; never pass a key)\n"
    "output: path:line:[full|short|prefix] excerpt   (secret-shaped values masked)\n"
    "exit: 0 hit found, 1 no hit, 2 usage error or something could not be read (scan incomplete)"
)

# ---- masking (shared shape with reset-detect.sh) --------------------------------------------------
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
WORD = re.compile(r"[A-Za-z]{3,8}")
PHRASE = re.compile(r"(?:\b[A-Za-z]{3,8}\b[ ,;]+){11,}\b[A-Za-z]{3,8}\b")
STOP = frozenset("after and are been being both but could did does each every for from get got had has her here him "
                 "his how its let many may most not our out per see she should some than the their them these those "
                 "too using via was were which while who why with would yes your".split())


def mask_phrase(m):
    words = re.findall(r"[A-Za-z]+", m.group(0))
    if any(w.lower() in STOP for w in words):
        return m.group(0)
    return "<masked>"


def mask_line(text):
    """Mask secret-shaped values. Runs before any truncation."""
    for rx in TOKEN_RULES:
        text = rx.sub("<masked>", text)
    text = URLPASS.sub(lambda m: m.group(1) + "<masked>@", text)
    text = ASSIGN.sub(lambda m: m.group(1) + "<masked>", text)
    text = PHRASE.sub(mask_phrase, text)
    text = HEXRUN.sub(lambda m: (m.group(1) or "") + m.group(2)[:16] + "...", text)
    return text


def is_env_file(name):
    low = name.lower()
    return low == ".env" or low == ".envrc" or low.startswith(".env.") or low.endswith(".env") or ".env." in low


def env_named(path):
    names = [os.path.basename(path)]
    try:
        names.append(os.path.basename(os.path.realpath(path)))
    except OSError:
        pass
    return any(is_env_file(n) for n in names)


def die(msg, code=2):
    print("id-grep: " + msg, file=sys.stderr)
    sys.exit(code)


def parse_args(argv):
    files_only = False
    short = True
    rest = []
    for a in argv:
        if a in ("-h", "--help"):
            print(USAGE)
            sys.exit(0)
        if a == "--files":
            files_only = True
        elif a == "--no-short":
            short = False
        elif a.startswith("-") and len(a) > 1:
            die("unknown option %s\n%s" % (a, USAGE))
        else:
            rest.append(a)
    if len(rest) < 2:
        die("needs an id and at least one path\n" + USAGE)
    return files_only, short, rest[0], rest[1:]


def build_needles(raw, short):
    h = raw.strip()
    if h.lower().startswith("0x"):
        h = h[2:]
    if not re.fullmatch(r"[0-9a-fA-F]{8,64}", h or ""):
        die("the id must be 8 to 64 hex digits, with or without 0x")
    h = h.lower()
    needles = [("full", h)]
    if short and len(h) == 64:
        if h.startswith("20000000"):
            needles.append(("short", h[8:16]))
        else:
            needles.append(("prefix", h[:16]))
    return needles


def window(line, start):
    if len(line) <= EXCERPT_MAX:
        return line
    lo = max(0, start - EXCERPT_MAX // 2)
    return line[lo:lo + EXCERPT_MAX]


def main():
    files_only, short, raw_id, paths = parse_args(sys.argv[1:])
    needles = build_needles(raw_id, short)
    rx = [(kind, re.compile(re.escape(n), re.IGNORECASE)) for kind, n in needles]

    stats = {"files": 0, "big": 0, "binary": 0, "env": 0, "symlinks": 0, "special": 0, "dirs": 0, "unreadable": [], "missing": []}
    refused = []
    hits = 0
    hit_files = {}

    def scan_file(path):
        try:
            st = os.stat(path)
        except OSError:
            stats["unreadable"].append(path)
            return
        if not stat.S_ISREG(st.st_mode):
            stats["special"] += 1
            return
        if st.st_size > MAX_BYTES:
            stats["big"] += 1
            return
        try:
            with open(path, "rb") as fh:
                data = fh.read()
        except OSError:
            stats["unreadable"].append(path)
            return
        if b"\x00" in data[:8192]:
            stats["binary"] += 1
            return
        stats["files"] += 1
        text = data.decode("utf-8", errors="replace")
        file_hits = 0
        for i, line in enumerate(text.splitlines(), 1):
            for kind, r in rx:
                if not r.search(line):
                    continue
                file_hits += 1
                # Mask first, the searched id included (a long hex run shows its first 16 digits), then cut.
                masked = mask_line(line).strip()
                low = masked.lower()
                found = [low.find(n[:16]) for _, n in needles if low.find(n[:16]) >= 0]
                excerpt = window(masked, min(found) if found else 0)
                if not files_only:
                    print("%s:%d:[%s] %s" % (path, i, kind, excerpt))
                break
        if file_hits:
            hit_files[path] = file_hits

    for p in paths:
        if env_named(p):
            print("id-grep: refusing to read %s: an env file can hold keys and is never opened" % os.path.basename(p),
                  file=sys.stderr)
            refused.append(p)
            continue
        if not os.path.exists(p):
            stats["missing"].append(p)
            continue
        if os.path.islink(p) and os.path.isfile(p):
            stats["symlinks"] += 1
            continue
        if os.path.isfile(p):
            scan_file(p)
            continue
        if not os.path.isdir(p):
            stats["unreadable"].append(p)
            continue
        for root, dirs, files in os.walk(p, followlinks=False, onerror=lambda e: stats["unreadable"].append(str(e.filename))):
            kept = []
            for d in sorted(dirs):
                if d in SKIP_DIRS:
                    stats["dirs"] += 1
                elif os.path.islink(os.path.join(root, d)):
                    stats["symlinks"] += 1
                else:
                    kept.append(d)
            dirs[:] = kept
            for name in sorted(files):
                fp = os.path.join(root, name)
                if is_env_file(name):
                    stats["env"] += 1
                    continue
                if os.path.islink(fp):
                    stats["symlinks"] += 1
                    continue
                scan_file(fp)

    if files_only:
        for fp in sorted(hit_files):
            print("%s  (%d)" % (fp, hit_files[fp]))
    hits = sum(hit_files.values())

    notes = []
    if stats["env"]:
        notes.append("%d env-named file(s) not opened" % stats["env"])
    if stats["binary"]:
        notes.append("%d binary" % stats["binary"])
    if stats["big"]:
        notes.append("%d over 2 MB" % stats["big"])
    if stats["symlinks"]:
        notes.append("%d symlink(s) not followed" % stats["symlinks"])
    if stats["special"]:
        notes.append("%d not a regular file (pipe, socket or device)" % stats["special"])
    if stats["dirs"]:
        notes.append("%d folder(s) skipped by name (.git, node_modules, build output)" % stats["dirs"])
    searched = ", ".join("%s %s" % (k, ("0x" + n if len(n) == 64 else n)[:18] + ("..." if len(n) == 64 else "")) for k, n in needles)
    print("id-grep: %d hit(s) in %d file(s); %d file(s) read; searched %s." % (hits, len(hit_files), stats["files"], searched),
          file=sys.stderr)
    if notes:
        print("id-grep: skipped: " + "; ".join(notes) + ".", file=sys.stderr)
    incomplete = bool(stats["missing"] or stats["unreadable"] or refused)
    if stats["missing"]:
        print("id-grep: path not found: " + ", ".join(stats["missing"]), file=sys.stderr)
    if stats["unreadable"]:
        print("id-grep: could not read: " + ", ".join(stats["unreadable"][:5]), file=sys.stderr)
    if incomplete:
        print("id-grep: the scan is incomplete, so a result of no hit means nothing yet.", file=sys.stderr)
        sys.exit(2)
    sys.exit(0 if hits else 1)


main()
PY
