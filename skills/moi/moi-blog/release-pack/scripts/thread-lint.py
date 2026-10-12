#!/usr/bin/env python3
"""thread-lint: check an announcement pack's posts before anything is drafted, scheduled or sent.

Usage (run from the working copy that holds the pack folder; SKILLS is the folder that holds
the moi-* skills; quote it because a path can hold spaces):
    python3 "$SKILLS/moi-blog/release-pack/scripts/thread-lint.py" <target> [--platform x|linkedin|discord] [--note RELEASE-NOTE.md]
    python3 "$SKILLS/moi-blog/release-pack/scripts/thread-lint.py" --list-rules

<target> is one of
    a thread folder   holds 1.txt, 2.txt, ... the form `scripts/buffer.mjs --thread-dir` reads
    a social folder   holds thread/ and single-post files such as x.txt, linkedin.txt, discord.txt
    a pack folder     protocol-release-<version>/, which holds social/
    one file          one post. The platform is read from the file name: a name containing
                      "linkedin" or "discord" uses that platform, any other name uses x.
--platform overrides the platform for every file. --note adds an advisory check that each
sentence of each post appears in the release note (a verbatim pack adds no facts).

What it checks, per post: the platform length limit (X 280 with every URL counted as 23, the
website pipeline's rule; LinkedIn 3000; Discord 2000), the em dash, 12:00 AM and other AM/PM
times (with a colon or a dot: 12:00 AM, 12.00 AM), "midnight", relative day words next to a
time, retired terms, placeholders left in, links without a scheme, backticks and bold markers
on X and LinkedIn, emoji, and the slop-lint ignore marker.
Per thread folder: file names are 1.txt to N.txt with no gap, duplicate or stray file, a number
written inside a post matches its file, and post 1 carries the release moment in UTC.
It reads files only. It never writes, sends or calls a service. It refuses an env file (.env,
.env.*, *.env, .envrc): those can hold keys and are never opened, so naming one is exit 2.

Output:  file:line:rule:excerpt   one line per hit on stdout. A rule shown as name(warn) is
         advisory. A summary and the lengths go to stderr. Any run of 20 or more characters
         without a space is replaced by <masked> in an excerpt, so a token that sits next to
         a flagged phrase is never echoed, and a not-in-note line prints only the first six
         words of the sentence. Spaced-out secrets such as a recovery phrase are not masked,
         so run secret-scan.sh on the folder before you lint it.
Exit:    0 no error-level hit (warnings allowed), 1 at least one error-level hit,
         2 usage error, a path that cannot be read, an env file named, or no post found.

This is not slop-lint.sh. It carries only the rules that bite in a release pack. Run both.
Python 3 standard library only.
"""
import os
import re
import sys

LIMITS = {"x": 280, "linkedin": 3000, "discord": 2000}
X_URL_LEN = 23
NEAR = 10          # warn when a post is this close to its limit or closer
NUM = re.compile(r"^(\d+)\.txt$")
URL = re.compile(r"https?://\S+")
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
IGNORE = re.compile(r"slop-lint:\s*ignore")
MASK_RUN = re.compile(r"\S{20,}")
TIME_NEARBY = re.compile(r"\d{1,2}:\d{2}|\bUTC\b|\b(?:am|pm)\b|\bscheduled\b", re.I)
RELATIVE = re.compile(r"\b(?:today|tonight|tomorrow|yesterday)\b", re.I)
BARE_LINK = re.compile(
    r"(?<![\w@./:-])((?:[a-z0-9][a-z0-9-]*\.)+(?:technology|com|org|net|io|ai|dev|app|xyz)"
    r"(?::\d+)?(?:/[^\s]*)?)(?![\w-])", re.I)
INLINE_NUM = re.compile(r"^\(?(\d+)\s*/\s*(\d+)?\)?(?:\s|$)")
INLINE_NUM_END = re.compile(r"(?:^|\s)\(?(\d+)\s*/\s*(\d+)?\)?$")

# (id, level, regex flags, regex, platforms or None for all, message)
RULES = [
    ("em-dash", "error", 0, "\u2014", None,
     "Em dash. Use a comma, a colon or a full stop."),
    ("twelve-am", "error", re.I, r"(?<![\d:.])(?:12|0?0)(?:[:.]00)?\s*(?:am|a\.m\.)(?!\w)", None,
     "12:00 AM is read as noon. Write 00:00 UTC with the date, then the India time."),
    ("am-pm", "warn", re.I,
     r"(?<![\d:.])(?!(?:12|0?0)(?:[:.]00)?\s*(?:am|a\.m\.)(?!\w))\d{1,2}(?:[:.]\d{2})?\s*(?:am|pm)\b", None,
     "Use 24-hour times, for example 00:00 UTC (05:30 IST)."),
    ("midnight", "warn", re.I, r"\bmidnight\b", None,
     "Midnight is read as the start or the end of a day. Write 00:00 UTC with the date."),
    ("voyage-devnet", "error", re.I, r"\bvoyage\s+devnet\b", None,
     "Say devnet. Voyage is the explorer, not the network."),
    ("fixed-supply", "error", re.I, r"\bfixed[- ]supply\b", None,
     "Say capped supply."),
    ("fuel-universal", "error", re.I,
     r"\bevery\s+(?:action|interaction|transaction|call)\b[^.\n]{0,40}\bcosts?\s+fuel\b", None,
     "A universal the protocol does not guarantee. Say what this release changes."),
    ("account-centric", "error", re.I, r"\baccount[- ](?:centric|based)\b", None,
     "MOI is participant-centric, not account-centric or account-based."),
    ("serval-labs", "error", re.I, r"\bserval\s+labs\b", None,
     "The company is Sarva Labs."),
    ("old-network-name", "warn", 0, r"\b(?:Indus|Babylon)\b", None,
     "Not the current network. Say devnet."),
    ("chain-id", "warn", re.I, r"\bchain[- ]?id\b", None,
     "MOI's own identifier is the network ID."),
    ("the-token", "warn", re.I, r"\b(?:the token|MOI'?s own token)\b", None,
     "Name KMOI."),
    ("the-fee", "warn", re.I, r"\bthe fee\b(?!\s+(?:payer|delegation))", None,
     "Say fuel, fee payer or fee delegation, whichever you mean."),
    ("unverified-phrase", "warn", re.I,
     r"native asset standard (?:made for|of its own)|made for KMOI alone|reserved for the fuel token", None,
     "Not in the release note and not traced to source. Use the note's words or source it."),
    ("rc-as-shipped", "warn", re.I,
     r"(?:-rc\d+|release candidate)[^.\n]{0,80}\b(?:latest|stable|shipped|released|generally available)\b|"
     r"\b(?:latest|stable|shipped|released)\b[^.\n]{0,80}(?:-rc\d+|release candidate)", None,
     "A release candidate is not stable. Quote the version as tagged."),
    ("placeholder", "error", 0,
     r"\b[A-Z][A-Z0-9]*_URL\b|\{\{[^}\n]*\}\}|\bTODO\b|\bREPLACE-WITH\b|<<<", None,
     "Placeholder text must not ship."),
    ("backtick", "error", 0, "`", ("x", "linkedin"),
     "X and LinkedIn show backticks literally."),
    ("bold-marker", "error", 0, r"\*\*", ("x", "linkedin"),
     "X and LinkedIn show ** literally."),
    ("emoji", "warn", 0, EMOJI.pattern, None,
     "Emoji. MOI posts carry none."),
    ("ignore-marker", "error", 0, IGNORE.pattern, None,
     "The slop-lint ignore marker would be posted as text. Remove it."),
]
RULE_IDS = [r[0] for r in RULES] + [
    "link-scheme", "relative-day", "non-ascii", "length", "length-near", "empty",
    "thread-number", "thread-file", "thread-order", "thread-root", "not-in-note"]
COMPILED = [(rid, lvl, re.compile(rx, fl), plats, msg) for rid, lvl, fl, rx, plats, msg in RULES]


class Report:
    def __init__(self):
        self.errors = 0
        self.warns = 0
        self.files = 0

    def hit(self, path, line, rule, level, text):
        label = rule if level == "error" else rule + "(warn)"
        sys.stdout.write("%s:%d:%s:%s\n" % (path, line, label, excerpt(text)))
        if level == "error":
            self.errors += 1
        else:
            self.warns += 1


def excerpt(text, limit=120):
    return MASK_RUN.sub("<masked>", text).strip().replace("\t", " ")[:limit]


def around(line, m, pad=25):
    """The masked line around a match, or the start of the line when the match was masked."""
    safe = MASK_RUN.sub("<masked>", line)
    word = m.group(0)[:40]
    k = safe.find(word)
    if k >= 0:
        return safe[max(0, k - pad):k + len(word) + pad]
    return safe[:70]


def norm(s):
    s = re.sub(r"^\s*[-*]\s+", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def measure(text, platform):
    if platform == "x":
        return len(URL.sub("x" * X_URL_LEN, text))
    return len(text)


def lint_post(path, text, platform, rep, note_norm, label=None):
    """Lint one post. Returns its measured length."""
    rep.files += 1
    stripped = text.strip()
    if not stripped:
        rep.hit(path, 1, "empty", "error", "the post is empty")
        return 0
    limit = LIMITS[platform]
    size = measure(stripped, platform)
    if size > limit:
        rep.hit(path, 1, "length", "error", "%d characters, %s limit is %d" % (size, platform, limit))
    elif size > limit - NEAR:
        rep.hit(path, 1, "length-near", "warn", "%d of %d characters, no room for an edit" % (size, limit))
    for number, line in enumerate(text.splitlines(), 1):
        for rid, lvl, rx, plats, msg in COMPILED:
            if plats and platform not in plats:
                continue
            m = rx.search(line)
            if m:
                rep.hit(path, number, rid, lvl, around(line, m))
        for m in BARE_LINK.finditer(line):
            host = re.split(r"[/:]", m.group(1), maxsplit=1)[0][:30]
            rep.hit(path, number, "link-scheme", "error", "link without https:// at host " + host)
        for m in RELATIVE.finditer(line):
            near = TIME_NEARBY.search(line)
            rep.hit(path, number, "relative-day", "error" if near else "warn",
                    "'%s' goes stale once scheduled. Write the date." % m.group(0))
        if platform == "x":
            seen = set()
            for ch in line:
                if ord(ch) > 127 and ch != "\u2014" and not EMOJI.match(ch) and ch not in seen:
                    seen.add(ch)
                    rep.hit(path, number, "non-ascii", "warn",
                            "U+%04X is outside plain ASCII. The evidence does not say how X counts it." % ord(ch))
        if note_norm is not None:
            for piece in re.split(r"(?<=[.!?])\s+", line):
                p = norm(piece)
                if len(p.split()) >= 4 and p not in note_norm:
                    # Only the first six words are printed: the line number finds the rest, and a
                    # sentence is never echoed whole (a recovery phrase has no 20-character run to mask).
                    words = piece.split()
                    rep.hit(path, number, "not-in-note", "warn",
                            " ".join(words[:6]) + (" ..." if len(words) > 6 else ""))
    return size


def platform_for(path, override):
    if override:
        return override
    name = os.path.basename(path).lower()
    if "linkedin" in name:
        return "linkedin"
    if "discord" in name:
        return "discord"
    return "x"


def is_env_file(path):
    """An env-named file is never opened: .env, .envrc, .env.*, *.env, anything holding .env."""
    names = [os.path.basename(path)]
    try:
        names.append(os.path.basename(os.path.realpath(path)))
    except OSError:
        pass
    for n in names:
        low = n.lower()
        if low in (".env", ".envrc") or low.startswith(".env.") or low.endswith(".env") or ".env." in low:
            return True
    return False


def refuse_env(path):
    sys.stderr.write(
        "thread-lint: refusing to read %s: an env file can hold keys and is never opened. "
        "Pass the post file instead.\n" % os.path.basename(path))


def read(path):
    if is_env_file(path):
        refuse_env(path)
        return None
    try:
        with open(path, "r", encoding="utf-8-sig", errors="replace") as fh:
            return fh.read()
    except OSError as exc:
        sys.stderr.write("thread-lint: cannot read %s: %s\n" % (path, exc.strerror))
        return None


def lint_thread(folder, override, rep, note_norm, lengths):
    platform = override or "x"
    entries = sorted(e for e in os.listdir(folder) if not e.startswith("."))
    posts = {}
    for e in entries:
        full = os.path.join(folder, e)
        m = NUM.match(e)
        if os.path.isdir(full):
            continue
        if not m:
            rep.hit(full, 1, "thread-file", "warn",
                    "not named <n>.txt, so buffer.mjs --thread-dir ignores it without saying so")
            continue
        posts.setdefault(int(m.group(1)), []).append(full)
    if not posts:
        sys.stderr.write("thread-lint: no <n>.txt files in %s\n" % folder)
        return False
    for n, files in posts.items():
        if len(files) > 1:
            rep.hit(files[1], 1, "thread-number", "error",
                    "two files are post %d: %s" % (n, ", ".join(os.path.basename(f) for f in files)))
    top = max(posts)
    if min(posts) != 1:
        rep.hit(os.path.join(folder, "%d.txt" % min(posts)), 1, "thread-number", "error",
                "the thread starts at %d, it must start at 1" % min(posts))
    missing = [n for n in range(min(posts), top + 1) if n not in posts]
    for n in missing:
        rep.hit(folder, 1, "thread-number", "error", "%d.txt is missing. A gap usually means a post was lost" % n)
    count = len(posts)
    inline = {}
    sizes = []
    for n in sorted(posts):
        path = posts[n][0]
        text = read(path)
        if text is None:
            return False
        sizes.append(lint_post(path, text, platform, rep, note_norm))
        lines = [l for l in text.strip().splitlines() if l.strip()]
        if lines:
            found = INLINE_NUM.match(lines[0].strip()) or INLINE_NUM_END.search(lines[-1].strip())
            if found:
                inline[n] = found
                if int(found.group(1)) != n:
                    rep.hit(path, 1, "thread-order", "error",
                            "the post says %s/ but it is file %d.txt" % (found.group(1), n))
                elif found.group(2) and int(found.group(2)) != count:
                    rep.hit(path, 1, "thread-order", "error",
                            "the post says %s/%s but the thread has %d posts" % (found.group(1), found.group(2), count))
        if n == min(posts) and "UTC" not in text:
            rep.hit(path, 1, "thread-root", "warn",
                    "post 1 should state the release moment as a date and a 24-hour UTC time")
    if inline and len(inline) != count:
        for n in sorted(posts):
            if n not in inline:
                rep.hit(posts[n][0], 1, "thread-order", "warn",
                        "other posts carry a number inside the text and this one does not")
    lengths.append("%s: thread of %d posts, characters %s (limit %d)" % (
        folder, count, " / ".join(str(s) for s in sizes), LIMITS[platform]))
    return True


def collect(target):
    """Return a list of jobs: ('thread', folder) or ('file', path)."""
    if os.path.isfile(target):
        return [("file", target)]
    if not os.path.isdir(target):
        return None
    base = target
    social = os.path.join(base, "social")
    if os.path.isdir(social):
        base = social
    names = sorted(os.listdir(base))
    thread_sub = os.path.join(base, "thread")
    if any(NUM.match(n) for n in names) or os.path.basename(os.path.normpath(base)) == "thread":
        return [("thread", base)]
    jobs = []
    if os.path.isdir(thread_sub):
        jobs.append(("thread", thread_sub))
    for n in names:
        full = os.path.join(base, n)
        if os.path.isfile(full) and n.endswith(".txt"):
            jobs.append(("file", full))
    return jobs


USAGE = ("usage: thread-lint.py <thread-folder | social-folder | pack-folder | file> "
         "[--platform x|linkedin|discord] [--note RELEASE-NOTE.md]\n"
         "       thread-lint.py --list-rules\n"
         "exit: 0 no error, 1 at least one error, 2 usage error, env file or nothing to lint")


def main(argv):
    args = argv[1:]
    if not args:
        sys.stderr.write(USAGE + "\n")
        return 2
    if args[0] in ("-h", "--help"):
        sys.stdout.write(USAGE + "\n")
        return 0
    if args[0] == "--list-rules":
        for rid, lvl, fl, rx, plats, msg in RULES:
            sys.stdout.write("%-18s %-5s %s\n" % (rid, lvl, msg))
        extra = [
            ("link-scheme", "error", "Write every link with its scheme, https:// included."),
            ("relative-day", "error", "today, tonight, tomorrow, yesterday next to a time (warn elsewhere). Write the date."),
            ("non-ascii", "warn", "X only: a character outside plain ASCII."),
            ("length", "error", "Over the platform limit (X 280 with URLs as 23, LinkedIn 3000, Discord 2000)."),
            ("length-near", "warn", "Within 10 characters of the limit."),
            ("empty", "error", "An empty post."),
            ("thread-number", "error", "Gap, duplicate or wrong start in the file numbers of a thread."),
            ("thread-file", "warn", "A file in a thread folder that buffer.mjs would skip."),
            ("thread-order", "error", "A number written inside a post disagrees with its file or the thread length."),
            ("thread-root", "warn", "Post 1 has no UTC time."),
            ("not-in-note", "warn", "With --note: a sentence that is not in the release note."),
        ]
        for rid, lvl, msg in extra:
            sys.stdout.write("%-18s %-5s %s\n" % (rid, lvl, msg))
        return 0
    override = None
    note = None
    target = None
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--platform" and i + 1 < len(args):
            override = args[i + 1]
            i += 2
        elif a == "--note" and i + 1 < len(args):
            note = args[i + 1]
            i += 2
        elif a.startswith("--"):
            sys.stderr.write(USAGE + "\n")
            return 2
        elif target is None:
            target = a
            i += 1
        else:
            sys.stderr.write(USAGE + "\n")
            return 2
    if target is None or (override and override not in LIMITS):
        sys.stderr.write(USAGE + "\n")
        return 2
    for named in (target, note):
        if named and is_env_file(named):
            refuse_env(named)
            return 2
    note_norm = None
    if note:
        raw = read(note)
        if raw is None:
            return 2
        note_norm = norm(raw)
    jobs = collect(target)
    if jobs is None:
        sys.stderr.write("thread-lint: cannot read %s\n" % target)
        return 2
    if not jobs:
        sys.stderr.write("thread-lint: no posts found under %s (expected <n>.txt files or .txt posts)\n" % target)
        return 2
    rep = Report()
    lengths = []
    unreadable = False
    for kind, path in jobs:
        if kind == "thread":
            if not lint_thread(path, override, rep, note_norm, lengths):
                unreadable = True
        else:
            text = read(path)
            if text is None:
                unreadable = True
                continue
            platform = platform_for(path, override)
            size = lint_post(path, text, platform, rep, note_norm)
            lengths.append("%s: %s post, %d of %d characters" % (path, platform, size, LIMITS[platform]))
    sys.stdout.flush()
    for line in lengths:
        sys.stderr.write("  " + line + "\n")
    sys.stderr.write("thread-lint: %d error(s), %d warning(s) in %d post(s)\n" % (rep.errors, rep.warns, rep.files))
    if unreadable:
        return 2
    return 1 if rep.errors else 0


sys.exit(main(sys.argv))
