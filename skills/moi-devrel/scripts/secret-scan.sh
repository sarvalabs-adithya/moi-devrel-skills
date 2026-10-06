#!/usr/bin/env bash
# secret-scan.sh: look for secret-shaped strings in text files before a folder is shared, committed
# or a transcript or log is saved.
#
# Usage:   bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" <path> [<path>...]
#          a file or a folder (walked recursively). SKILLS is the folder that holds the moi-* skills.
# Output:  file:line:rule-name   one line per finding. The matched text is NEVER printed, and a file
#          name that is itself secret-shaped is masked before it is printed.
#          A summary goes to stderr: what was scanned, what was NOT scanned, what could not be read.
#          Lower-level notes (see "64-digit hex" below) also go to stderr, never to stdout.
# Exit codes: 0 nothing found and everything given was read
#             1 at least one finding (and everything given was read)
#             2 usage error, or a path or file or folder could not be read. The scan is then
#               incomplete, so even a "0 findings" line means nothing: fix access and run it again.
#
# THIS IS A BACKSTOP, NOT PROOF. A clean result does not mean a file is safe to share. It only looks
# for the shapes listed below and misses a secret in any other shape, in a binary, a PDF or a Word file.
#
# What it looks for: common API key prefixes (Anthropic, OpenAI style, Groq, Google, AWS, Stripe, npm),
# GitHub tokens, Slack tokens and webhook URLs, Discord webhook URLs, Telegram bot tokens, private key
# blocks, JWTs (a Supabase key is one), and these shapes added after review:
#   url-with-password          scheme://user:password@host
#   token-in-query             ?token=, &api_key=, &secret=, &sig= and similar names with a long value
#   bearer-token               "Bearer" followed by a long value
#   secret-named-assignment    a secret-named variable with a long value: NAME=value, NAME: value,
#                              "NAME = value", JSON "name": "value", and prose such as "the admin
#                              secret is <value>". A value that is one repeated character, holds a
#                              placeholder word (your, example, changeme, redacted ...), or starts
#                              with $, <, {, / or process.env is treated as a placeholder. A value made
#                              only of letters, hyphens, dots and underscores (no digit, no mixed case,
#                              no symbol) is treated as prose or another variable's name, not a key.
# and recovery phrases in these shapes: a run of 12 or more short words on one line (after any label,
# prefix, quote, bullet or numbering, in any letter case, separated by spaces, commas or semicolons,
# or inside a sentence), a hyphen-joined run of 12 or more short words (recovery-phrase-hyphen-run),
# and 12 or more consecutive lines that each hold one short word. A run that contains a common English
# word that is not on the BIP-39 list (the, and, for, with, was ...) is treated as prose. Ordinary prose
# rarely forms such a run, but a hit is a prompt to look, not proof, and a phrase written some other
# way is not caught.
# 64-digit hex (an "info" note, NOT a finding): a bare run of 64 hex digits, with or without 0x, is
# common public chain data (interaction hashes, account and asset ids), and it looks exactly like a
# private key. So it is reported on stderr as file:line:hex64-info, at most 20 lines, and it NEVER changes
# the exit code. Read each one: if it is a key, treat it as exposed.
# What it skips, and says so in the summary: .git, node_modules and build folders; binary files;
# files over 2 MB; files with a skipped extension (images, PDF, Word, archives); symlinks (counted);
# and any env-named file, which is NEVER opened: a name that is .env, starts with .env., ends with .env or
# contains .env. (so .env, .env.local, prod.env and server.env.example are all left unopened). The name
# is checked again after resolving a symlink given on the command line.
# If a real secret is found: do not copy it anywhere, name it only, and say it should be rotated
# (references/consent-and-identity.md).
# Python 3 standard library only. Works under bash 3.2 and zsh.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
export SCRIPT_DIR
exec python3 - "$@" <<'PY'
import os
import re
import sys

# Rule name, regex. The recovery-phrase and secret-assignment rules are handled in code below.
RULES = [
    ("anthropic-api-key", r"\bsk-ant-[A-Za-z0-9_-]{20,}"),
    ("openai-style-key", r"\bsk-(?!ant-)(?:proj-)?[A-Za-z0-9_-]{20,}"),
    ("groq-api-key", r"\bgsk_[A-Za-z0-9]{20,}"),
    ("google-api-key", r"\bAIza[0-9A-Za-z_-]{35}\b"),
    ("aws-access-key-id", r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    ("stripe-live-key", r"\b(?:sk|rk)_live_[0-9A-Za-z]{16,}"),
    ("npm-token", r"\bnpm_[A-Za-z0-9]{36}\b"),
    ("github-token", r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}|\bgithub_pat_[A-Za-z0-9_]{22,}"),
    ("slack-token", r"\bxox[abprso]-[A-Za-z0-9-]{10,}"),
    ("slack-webhook-url", r"https://hooks\.slack\.com/services/[A-Z0-9]+/[A-Z0-9]+/[A-Za-z0-9]+"),
    ("discord-webhook-url", r"https://(?:ptb\.|canary\.)?discord(?:app)?\.com/api/webhooks/\d+/[A-Za-z0-9_-]{20,}"),
    ("telegram-bot-token", r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b"),
    ("private-key-block", r"-----BEGIN (?:[A-Z]+ )*PRIVATE KEY(?: BLOCK)?-----"),
    ("jwt", r"\beyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"),
]
COMPILED = [(name, re.compile(rx)) for name, rx in RULES]

# Shapes added after review. These need a check on the matched value, so they are handled in code.
URL_PASSWORD = re.compile(r"\b[a-z][a-z0-9+.-]{1,15}://[^\s/:@'\"<>]+:([^\s/@'\"<>]{6,})@[^\s/'\"<>]+", re.IGNORECASE)
QUERY_SECRET = re.compile(
    r"[?&;](?:access[_-]?token|id[_-]?token|refresh[_-]?token|auth[_-]?token|token|api[_-]?key|apikey|key|"
    r"client[_-]?secret|secret|password|passwd|pwd|authorization|auth|signature|sig|jwt)=([A-Za-z0-9._~+/%=-]{16,})",
    re.IGNORECASE,
)
BEARER = re.compile(r"\bbearer[ \t]+([A-Za-z0-9._~+/=-]{16,})", re.IGNORECASE)
HYPHEN_RUN = re.compile(r"(?<![A-Za-z0-9-])[A-Za-z]{3,8}(?:-[A-Za-z]{3,8}){11,}(?![A-Za-z0-9-])")
HEX64 = re.compile(r"(?<![0-9A-Fa-f])(?:0x)?[0-9A-Fa-f]{64}(?![0-9A-Fa-f])")
URL_PASSWORD_PLACEHOLDERS = frozenset("pass password passwd secret token user username pwd changeme yourpassword".split())
INFO_LIMIT = 20

# Recovery phrases (the MOI Wallet uses the 2048-word BIP-39 English list: 3 to 8 letters a word).
# A phrase shape is PHRASE_MIN or more consecutive short words (3 to 8 letters) separated only by
# whitespace, commas, semicolons or quote marks. A "1." or "2)" numbering between words is skipped and
# does not end the run. Any other character ends it: a period, colon, bracket, pipe, backtick, hyphen,
# a word under 3 or over 8 letters. A label, bullet, "> " quote marker, assignment or surrounding
# sentence therefore does not matter, and letter case does not matter.
PHRASE_MIN = 12
TOKEN = re.compile(r"\d+[.):]?|[A-Za-z]+|[^\sA-Za-z\d,;\"']")
# Common English words that are NOT on the BIP-39 list. A real phrase never holds one, so a run that
# does is prose (a list of nouns joined by "and", for example). Checked against the list, 2026-10-02.
STOPWORDS = frozenset(
    "after and are been being both but could did does each every for from get got had has her here him "
    "his how its let many may most not our out per see she should some than the their them these those "
    "too using via was were which while who why with would yes your".split()
)
# One short word alone on a line, with an optional bullet, quote marker, numbering, quotes or comma.
SINGLE = re.compile(r"^\s*(?:[-*+>]+\s*)?(?:\d{1,3}[.):]\s*)?[`\"'(\[]?[A-Za-z]{3,8}[`\"')\]]?[,;]?\s*$")

# A secret-named variable with a long value: NAME=value, NAME: value, "NAME = value", "name": "value",
# NAME => value, or "the admin secret is value". Placeholder-looking values are ignored.
ASSIGN = re.compile(
    r"\b[\w-]*(?:secret|token|passw(?:or)?d|passphrase|mnemonic|api[-_ ]?key|private[-_ ]?key|credential)[\w-]*[\"']?"
    r"\s*(=>|:=|=|:|\s(?:is|was|are|equals)\s)\s*[\"'`]?([^\s\"'`<>,;(){}\[\]]{16,})",
    re.IGNORECASE,
)
PLACEHOLDER_WORDS = ("your", "example", "changeme", "placeholder", "redacted", "dummy", "sample", "token_here", "replace", "insert", "....")
CODE_PREFIXES = ("process.", "env.", "os.environ", "os.getenv", "getenv", "secrets.", "settings.", "config.", "vars.")


def placeholder_like(value):
    """True for a value that is a stand-in: one character repeated, a placeholder word, or a variable reference."""
    low = value.lower()
    if len(set(low)) <= 2:
        return True
    if any(word in low for word in PLACEHOLDER_WORDS):
        return True
    return value[:1] in "<${%[/" or low.startswith(CODE_PREFIXES)


def random_looking(value):
    """True if the value has a digit, mixed case or a symbol, as a key does. Words made only of letters, hyphens,
    dots and underscores (prose, or the name of another variable) are not."""
    if any(c.isdigit() for c in value):
        return True
    if any(c.isupper() for c in value) and any(c.islower() for c in value):
        return True
    return any(c in "+=!@#$%^&*~/" for c in value)


def secret_assignment(line):
    for m in ASSIGN.finditer(line):
        connector, value = m.group(1), m.group(2)
        if "://" in value or placeholder_like(value):
            continue
        if random_looking(value):
            return True
    return False


def hyphen_run_is_phrase(run):
    words = run.lower().split("-")
    return any(not any(w in STOPWORDS for w in words[i:i + PHRASE_MIN]) for i in range(len(words) - PHRASE_MIN + 1))


def other_shapes(line):
    """Names of the review-added shapes found in the line."""
    names = []
    for m in URL_PASSWORD.finditer(line):
        pw = m.group(1)
        if pw.lower() not in URL_PASSWORD_PLACEHOLDERS and not placeholder_like(pw):
            names.append("url-with-password")
            break
    for m in QUERY_SECRET.finditer(line):
        if not placeholder_like(m.group(1)) and random_looking(m.group(1)):
            names.append("token-in-query")
            break
    for m in BEARER.finditer(line):
        if not placeholder_like(m.group(1)) and random_looking(m.group(1)):
            names.append("bearer-token")
            break
    if any(hyphen_run_is_phrase(m.group(0)) for m in HYPHEN_RUN.finditer(line)):
        names.append("recovery-phrase-hyphen-run")
    if not names and secret_assignment(line):
        names.append("secret-named-assignment")
    return names


def safe_path(path):
    """A path with every secret-shaped piece replaced, so a file name can never carry a key into the output."""
    text = str(path)
    for _name, rx in COMPILED:
        text = rx.sub("<masked>", text)
    return re.sub(r"[0-9A-Fa-f]{40,}", "<masked>", text)

SKIP_DIRS = {".git", "node_modules", ".next", "dist", "build", ".venv", "venv", "__pycache__", ".cache", "coverage", ".turbo", ".astro"}
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".gz", ".tgz", ".mp4", ".mov", ".mp3", ".wav",
            ".woff", ".woff2", ".ttf", ".otf", ".docx", ".pptx", ".xlsx", ".bundle", ".jar", ".class", ".so", ".dylib"}
MAX_BYTES = 2 * 1024 * 1024

USAGE = (
    "usage: secret-scan.sh <path> [<path>...]\n"
    "output: file:line:rule-name (the matched text is never printed)\n"
    "exit: 0 nothing found, 1 findings, 2 usage error or something could not be read\n"
    "a backstop, not proof: a clean result does not mean a file is safe to share"
)


def new_stats():
    return {
        "files": 0, "skipped_big": 0, "skipped_binary": 0, "env_skipped": 0, "symlinks": 0, "skipped_dirs": 0,
        "info": 0, "info_shown": 0,
        "skipped_ext": {}, "unreadable_files": [], "unreadable_dirs": [], "missing": [],
    }


def is_env_file(name):
    """An env-named file is never opened: .env, .env.*, *.env, anything containing .env., and .envrc."""
    low = name.lower()
    return low == ".env" or low == ".envrc" or low.startswith(".env.") or low.endswith(".env") or ".env." in low


def env_named(path):
    """True if the name, or the name of what a symlink points at, is an env file."""
    names = [os.path.basename(path)]
    try:
        names.append(os.path.basename(os.path.realpath(path)))
    except OSError:
        pass
    return any(is_env_file(n) for n in names)


def skipped_extension(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in SKIP_EXT:
        return ext
    real_ext = os.path.splitext(os.path.realpath(path))[1].lower()
    return real_ext if real_ext in SKIP_EXT else None


def phrase_run(line):
    """True if the line holds PHRASE_MIN or more consecutive short words and none is a common English word."""
    run = []
    found = [False]

    def flush():
        if len(run) >= PHRASE_MIN:
            for i in range(len(run) - PHRASE_MIN + 1):
                if not any(w in STOPWORDS for w in run[i:i + PHRASE_MIN]):
                    found[0] = True
        del run[:]

    for tok in TOKEN.findall(line):
        if tok[0].isdigit():
            continue
        if tok.isalpha() and 3 <= len(tok) <= 8:
            run.append(tok.lower())
        else:
            flush()
    flush()
    return found[0]


def scan_file(path, stats):
    found = 0
    try:
        size = os.path.getsize(path)
        if size > MAX_BYTES:
            stats["skipped_big"] += 1
            return 0
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        stats["unreadable_files"].append(path)
        return 0
    if b"\x00" in data[:8192]:
        stats["skipped_binary"] += 1
        return 0
    stats["files"] += 1
    text = data.decode("utf-8", errors="replace")
    single_start, single_count, single_reported = 0, 0, False
    for number, line in enumerate(text.splitlines(), 1):
        names = []
        for name, rx in COMPILED:
            if rx.search(line):
                names.append(name)
        if phrase_run(line):
            names.append("recovery-phrase-shaped-line")
        if SINGLE.match(line):
            if single_count == 0:
                single_start, single_reported = number, False
            single_count += 1
            if single_count >= PHRASE_MIN and not single_reported:
                sys.stdout.write("%s:%d:recovery-phrase-one-word-per-line\n" % (safe_path(path), single_start))
                found += 1
                single_reported = True
        else:
            single_count = 0
        names.extend(other_shapes(line))
        for name in names:
            sys.stdout.write("%s:%d:%s\n" % (safe_path(path), number, name))
            found += 1
        if HEX64.search(line):
            # Public chain data and private keys look the same: a note on stderr, never a finding.
            stats["info"] += 1
            if stats["info_shown"] < INFO_LIMIT:
                stats["info_shown"] += 1
                sys.stdout.flush()
                sys.stderr.write("secret-scan: info: %s:%d:hex64-info\n" % (safe_path(path), number))
    return found


def count_ext(stats, ext):
    stats["skipped_ext"][ext] = stats["skipped_ext"].get(ext, 0) + 1


def walk(root, stats):
    total = 0

    def onerror(err):
        stats["unreadable_dirs"].append(getattr(err, "filename", None) or root)

    for current, dirs, files in os.walk(root, topdown=True, onerror=onerror, followlinks=False):
        keep = []
        for d in sorted(dirs):
            full = os.path.join(current, d)
            if os.path.islink(full):
                stats["symlinks"] += 1
            elif is_env_file(d):
                stats["env_skipped"] += 1
            elif d in SKIP_DIRS:
                stats["skipped_dirs"] += 1
            else:
                keep.append(d)
        dirs[:] = keep
        for name in sorted(files):
            full = os.path.join(current, name)
            if os.path.islink(full):
                stats["symlinks"] += 1
                continue
            if is_env_file(name):
                stats["env_skipped"] += 1
                continue
            ext = skipped_extension(full)
            if ext:
                count_ext(stats, ext)
                continue
            total += scan_file(full, stats)
    return total


def main(argv):
    args = argv[1:]
    if args and args[0] in ("-h", "--help"):
        sys.stdout.write(USAGE + "\n")
        return 0
    if not args:
        sys.stderr.write(USAGE + "\n")
        return 2
    stats = new_stats()
    total = 0
    for path in args:
        try:
            os.stat(path)
        except FileNotFoundError:
            stats["missing"].append(path)
            continue
        except OSError:
            stats["unreadable_files"].append(path)
            continue
        if os.path.isdir(path):
            total += walk(path, stats)
        elif os.path.isfile(path):
            if env_named(path):
                stats["env_skipped"] += 1
                continue
            ext = skipped_extension(path)
            if ext:
                count_ext(stats, ext)
                continue
            total += scan_file(path, stats)
        else:
            stats["unreadable_files"].append(path)
    sys.stdout.flush()
    err = sys.stderr
    for path in stats["missing"]:
        err.write("secret-scan: no such file or folder: %s\n" % safe_path(path))
    for path in stats["unreadable_files"]:
        err.write("secret-scan: cannot read file: %s\n" % safe_path(path))
    for path in stats["unreadable_dirs"]:
        err.write("secret-scan: cannot read folder: %s\n" % safe_path(path))
    ext_text = ", ".join("%s x%d" % (e, n) for e, n in sorted(stats["skipped_ext"].items())) or "none"
    err.write("secret-scan: %d finding(s) in %d file(s) scanned. Values are never printed.\n" % (total, stats["files"]))
    if stats["info"]:
        more = stats["info"] - stats["info_shown"]
        err.write(
            "secret-scan: %d line(s) hold a 64-digit hex string%s. That is usually public chain data (a hash or id) and "
            "looks like a private key; it is NOT a finding and did not change the exit code. Read each one.\n"
            % (stats["info"], (" (%d more not listed)" % more) if more else "")
        )
    err.write(
        "secret-scan: NOT scanned: %d env-named file(s) (never opened), %d binary, %d over 2 MB, "
        "skipped by extension: %s, %d symlink(s), %d folder(s) skipped by name.\n"
        % (stats["env_skipped"], stats["skipped_binary"], stats["skipped_big"], ext_text, stats["symlinks"], stats["skipped_dirs"])
    )
    unreadable = len(stats["unreadable_files"]) + len(stats["unreadable_dirs"]) + len(stats["missing"])
    err.write(
        "secret-scan: could not read: %d file(s), %d folder(s), %d missing path(s).\n"
        % (len(stats["unreadable_files"]), len(stats["unreadable_dirs"]), len(stats["missing"]))
    )
    err.write("secret-scan: a backstop, not proof. A clean result does not mean the files are safe to share.\n")
    if unreadable:
        return 2
    return 1 if total else 0


sys.exit(main(sys.argv))
PY
