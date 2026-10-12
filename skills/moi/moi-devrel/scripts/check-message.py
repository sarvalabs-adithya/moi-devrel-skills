#!/usr/bin/env python3
"""check-message.py: the last check on a drafted teammate message, before the operator sends it.

Part of moi-devrel. The shapes a message takes and what a DevOps request must hold are in
references/house-style.md section 4; fill-in drafts are in templates/messages.md. Run it from the
working copy the message is about, never from inside a skill folder.

Usage (SKILLS is the folder that holds the moi-* skills; quote it, a path can hold spaces):
    python3 "$SKILLS/moi-devrel/scripts/check-message.py" [--to KIND] DRAFT
    python3 "$SKILLS/moi-devrel/scripts/check-message.py" --to devops --max-lines 12 DRAFT
    python3 "$SKILLS/moi-devrel/scripts/check-message.py" --to protocol --hashes-ok DRAFT
  DRAFT      one message in a plain text or markdown file (a regular file, not a pipe or device).
  --to KIND  devops, protocol, reviewer, status or other (default other). The kind turns on the
             checks that only make sense for it (see below).
  --max-lines N, --max-chars N   warn when the draft is longer. No limit is recorded in the MOI
             evidence, so there is no default; the summary always reports both counts.
  --hashes-ok   a 40 or 64 digit hex value is normally an error, because a private key looks the
             same. With this flag it is a warning instead. Use it only when each such value is an
             interaction hash or a commit id that you copied from the explorer or from git log.

What it looks for. Findings print as   file:line:rule:message | excerpt   and a rule shown as
name(warn) is advisory. Exit 1 only for an error-level finding.
  every kind   placeholder left in (<NAME>, {{x}}, [DATE], TBD, TODO, RELEASE_URL), em dash,
               skill markers that must not reach a person (ASK:, GATE, $SKILLS, a moi-* skill name,
               the operator),
               a secret-shaped value (never printed): long hex, known token prefixes, JWTs, long
               mixed tokens, a Bearer value, a URL with a password in it, a secret-named
               assignment or query value, a run of 12 or more short words on a line, or on 12
               or more lines in a row, that could be a recovery phrase;
               a request for a secret (a sentence that says the sender will not send one is not a
               request), an Owner: or Assignee: label (warn for Task:, Problem: and similar
               labels), "12:00 AM UTC", relative times (today, tomorrow, ASAP, a weekday with no
               date), a weekday that does not match the ISO date beside it, US time-zone
               abbreviations (EST and the like), no calendar date at all, a private IP address,
               wording that describes a security weakness or finding (generic terms only), a
               request to rotate the Launchpad agent-key secret, more than one question with no
               numbered points, no question.
  devops       the Launchpad platform wallet variable (settled with DevOps by 2026-08-03),
               Vercel as a deploy target.
  status       future-tense lines outside a To do section, a Done line with no evidence (a PR
               number, a commit, a URL, a date), no To do or Not verified line at all.
It does NOT replace slop-lint.sh or secret-scan.sh (in the same scripts folder): run both as well. It cannot
tell whether a claim is true, whether the person is the right one, or whether the ask is clear.

Reads one file, writes nothing, never touches the network. It refuses a file whose name marks it
as an env file (.env, .env.*, *.env): those can hold keys and are never opened. Everything it
prints is masked first (long hex, common token prefixes, JWTs, long mixed tokens, credentials in
URLs, secret-named values, runs of 12 or more short words that could be a recovery phrase, IP
addresses) and truncated after masking. A line that is part of a multi-line word run is not
printed at all.

Exit codes: 0 no error-level finding, 1 at least one error-level finding, 2 bad input (missing,
unreadable, binary, empty, not a regular file or env-named file, or a wrong option). Python 3
standard library only.
"""
import argparse
import datetime
import os
import re
import stat
import sys

MAX_BYTES = 200000
EXCERPT = 100

# ---------------------------------------------------------------- masking
LONG_HEX = re.compile(r"0x[0-9A-Fa-f]{17,}|[0-9A-Fa-f]{24,}")
HASH_HEX = re.compile(r"(?<![0-9A-Fa-f])(?:0x)?(?:[0-9A-Fa-f]{64}|[0-9A-Fa-f]{40})(?![0-9A-Fa-f])")
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
    r"\bBearer\s+[A-Za-z0-9._~+/=-]{12,}",
    r"://[^/\s:@]+:[^/\s@]+@",
    r"[?&](?:key|sig|signature|auth|code|apikey|api_key|token|access_token)=[A-Za-z0-9_\-+/=.%]{8,}",
)]
# A secret-named assignment such as  api_key = a1b2c3...  or  password is Passw0rd... (a value of 12
# or more characters that mixes letters and digits). Prose like "token: needed" is not caught.
SECRET_ASSIGN = re.compile(
    r"(?:secret|token|passw(?:or)?d|pwd|api[_-]?key|apikey|private[_-]?key|credential|mnemonic)"
    r"[A-Za-z0-9_.-]{0,40}\s{0,3}(?:[:=]|\bis\b)\s{0,3}[\"'`]?"
    r"(?=[A-Za-z0-9_\-+/=.]{0,200}\d)(?=[A-Za-z0-9_\-+/=.]{0,200}[A-Za-z])[A-Za-z0-9_\-+/=.]{12,200}", re.I)
SECRET_SHAPES.append(SECRET_ASSIGN)
IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
PHRASE_MIN = 12
PHRASE_STOP = frozenset(
    "after and are been being both but could did does each every for from get got had has her here "
    "him his how its let many may most not our out per see she should some than the their them these "
    "those too using via was were which while who why with would yes your".split())
_PIECE = re.compile(r"[A-Za-z]+|[^A-Za-z]+")
# Between two words of a phrase: spaces, commas, semicolons, a number such as "3." or "(3)", a hyphen
# or an underscore. A full stop or a colon on its own ends the run.
_SEP_OK = re.compile(r"(?:[\s,;()]|\d{1,2}[.):]?|[-_])+")
_WORD_LINE = re.compile(r"[A-Za-z]{3,8}")


def _phrase_spans(s):
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
        elif _SEP_OK.fullmatch(text):
            continue
        else:
            close()
    close()
    return spans


def word_line_runs(lines):
    """1-based numbers of lines inside a run of PHRASE_MIN or more lines that each hold one short word
    (after any bullet or number). A recovery phrase written one word to a line looks like this."""
    hits, run = set(), []
    for i, raw in enumerate(lines, 1):
        s = re.sub(r"^\s*(?:[-*•]|\d{1,2}[.):]?)?\s*", "", raw).strip(" \t\"'`,;.")
        if _WORD_LINE.fullmatch(s) and s.lower() not in PHRASE_STOP:
            run.append(i)
        else:
            if len(run) >= PHRASE_MIN:
                hits.update(run)
            run = []
    if len(run) >= PHRASE_MIN:
        hits.update(run)
    return hits


def has_secret_shape(s):
    if LONG_HEX.search(s) or _phrase_spans(s):
        return True
    return any(rx.search(s) for rx in SECRET_SHAPES)


def only_hash_shapes(s):
    """True when the only secret-shaped thing on the line is one or more 40 or 64 digit hex values."""
    return bool(HASH_HEX.search(s)) and not has_secret_shape(HASH_HEX.sub("(hash)", s))


def mask(s):
    """Replace every secret-shaped piece, whole, and every IP address. Runs before any truncation."""
    s = LONG_HEX.sub("(masked)", s)
    for rx in SECRET_SHAPES:
        s = rx.sub("(masked)", s)
    for a, b in reversed(_phrase_spans(s)):
        s = s[:a] + "(masked: 12 or more short words)" + s[b:]
    return IPV4.sub("(masked ip)", s)


def is_env_file(path):
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


# ---------------------------------------------------------------- rules
MONTHS = (r"(?:January|February|March|April|May|June|July|August|September|October|November|December|"
          r"Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)")
DATE_RX = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b|\b\d{1,2}(?:st|nd|rd|th)?\s+" + MONTHS + r"\b|\b" + MONTHS +
                     r"\.?\s+\d{1,2}\b", re.I)

PLACEHOLDER = re.compile(
    r"<(?![^<>\n]*(?:@|://))[A-Za-z][^<>\n]{0,60}>|\{\{[^{}\n]{1,60}\}\}|\[\[[^\[\]\n]{1,60}\]\]|"
    r"\[[A-Z][A-Z0-9 _/-]{2,30}\]|\b(?:TBD|TODO|FIXME|XXX)\b|\b[A-Z][A-Z0-9]{2,}_(?:URL|DATE|NAME|HERE)\b|_{4,}")
EM_DASH = re.compile(chr(0x2014))
MARKERS = re.compile(r"\bASK:|\bGATE\b|\$SKILLS|\bmoi-(?:devrel|webinar|blog|docs|launchpad-ops|mcp-ops|devnet-reset|standards-submission|education-programs)\b")
OPERATOR_WORD = re.compile(r"\bthe operator\b|\bClaude\b", re.I)
LABEL_ERR = re.compile(r"^\s*[-*]?\s*\**(?:owner|assignee)\**\s*:", re.I)
LABEL_WARN = re.compile(
    r"^\s*[-*]?\s*\**(?:task|priority|subject|action|problem|solution|context|summary|deadline|"
    r"request|verify|background|impact|steps?)\**\s*:", re.I)
BOILERPLATE = re.compile(r"\beverything below is a task\b", re.I)
SECRET_ASK = re.compile(
    r"\b(?:send|share|paste|give|dm|post|forward|email|provide|drop|hand over)\b[^.\n?]{0,40}?"
    r"\b(?:tokens?|api[ _-]?keys?|passwords?|passphrases?|secrets?|pat|private keys?|env files?|"
    r"\.env|mnemonics?|seed phrases?|recovery phrases?|credentials?)\b", re.I)
# "I will not send a token" is the opposite of a request: a negation right before the verb.
NEGATED = re.compile(r"(?:\bnot|\bnever|n't|\bno|\bnor)\s+(?:\w+\s+)?$", re.I)
AM_UTC = re.compile(r"\b(?:12:00|00:00)\s*(?:AM|PM)\s*UTC\b|\b12\s*(?:AM|PM)\s*UTC\b", re.I)
RELATIVE = re.compile(
    r"\b(?:today|tomorrow|tonight|yesterday|this (?:morning|afternoon|evening|week|weekend)|"
    r"next (?:week|month|weekend)|last (?:week|month|night)|eod|end of (?:day|week)|asap|soon|shortly)\b", re.I)
WEEKDAY = re.compile(r"\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", re.I)
WEEKDAY_ISO = re.compile(
    r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b[\s,(]{0,3}(20\d{2})-(\d{2})-(\d{2})\b", re.I)
TZ_ABBREV = re.compile(r"\b(?:EST|EDT|PST|PDT|CST|CDT|MST|MDT)\b")
SECURITY = re.compile(
    r"\b(?:vulnerab\w*|exploit\w*|insecure|unauthenticated|CVE-\d{4}|auth(?:entication)? bypass|"
    r"security (?:hole|flaw|issue|bug|weakness|problem|risk|concern|gap|finding|incident|breach)|"
    r"(?:default|hard-?coded|leaked|exposed|weak) (?:password|secret|credential|key|token|admin)|"
    r"anyone can (?:read|write|delete|log ?in|access)|admin (?:secret|password|key)s? (?:is|are|can|was))\b", re.I)
ROTATE = re.compile(r"\b(?:rotat\w*|regenerat\w*|replac\w*|chang\w*|reset\w*|new value)\b", re.I)
PLATFORM = re.compile(r"MOI_PLATFORM_MNEMONIC|platform wallet", re.I)
VERCEL = re.compile(r"\bvercel\b", re.I)
FUTURE = re.compile(r"\b(?:will|going to|plan to|planning to|about to|i'll|we'll|to be done|next step)\b", re.I)
EVIDENCE = re.compile(r"#\d+|https?://|\b[0-9a-f]{7,40}\b|\b20\d{2}-\d{2}-\d{2}\b|\bPR\s?\d+\b")
BULLET = re.compile(r"^\s*(?:[-*]|\d+[.)])\s+")
NUMBERED = re.compile(r"^\s*\d+[.)]\s+")
URL = re.compile(r"https?://\S+")

SECTION = [
    ("partly", re.compile(r"^\s*[-*#]*\s*\**(?:partly done|partially done|in progress|almost done)\b", re.I)),
    ("done", re.compile(r"^\s*[-*#]*\s*\**(?:done|completed|shipped|finished)\b", re.I)),
    ("todo", re.compile(r"^\s*[-*#]*\s*\**(?:to do|to-do|todo|next|planned|not started|not done|remaining|blocked|still open|open)\b", re.I)),
    ("unverified", re.compile(r"^\s*[-*#]*\s*\**(?:not verified|unverified|assumed|not checked)\b", re.I)),
    ("needs", re.compile(r"^\s*[-*#]*\s*\**(?:needs from you|decisions?|questions?|waiting on)\b", re.I)),
]


def asks_for_secret(line):
    for m in SECRET_ASK.finditer(line):
        if not NEGATED.search(line[:m.start()]):
            return True
    return False


def weekday_mismatch(line):
    """The first weekday that does not match the ISO date written beside it, or None."""
    for m in WEEKDAY_ISO.finditer(line):
        try:
            actual = datetime.date(int(m.group(2)), int(m.group(3)), int(m.group(4)))
        except ValueError:
            return "an impossible date " + m.group(2) + "-" + m.group(3) + "-" + m.group(4)
        if actual.strftime("%A").lower() != m.group(1).lower():
            return "%s is a %s, not a %s" % (actual.isoformat(), actual.strftime("%A"), m.group(1).capitalize())
    return None


def analyse(text, kind, max_lines, max_chars, hashes_ok=False):
    findings = []  # (line, rule, level, message, excerpt)
    lines = text.split("\n")
    hidden = word_line_runs(lines)

    def add(n, rule, level, msg, line=None, hide=False):
        if n in hidden:
            hide = True
        ex = "(value not shown)" if hide else mask(lines[n - 1].strip() if line is None else line)[:EXCERPT]
        findings.append((n, rule, level, msg, ex))

    in_fence = False
    section = None
    seen_done = seen_open = False
    asks = 0
    numbered = 0
    any_date = bool(DATE_RX.search(text))

    for i, raw in enumerate(lines, 1):
        line = raw.rstrip("\r")
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not line.strip():
            continue
        if i in hidden:
            add(i, "secret-shaped", "error",
                "A line in a run of 12 or more one-word lines, which could be a recovery phrase. Remove it. "
                "Name the variable and where it lives, never the value.", hide=True)
        elif has_secret_shape(line):
            if hashes_ok and only_hash_shapes(line):
                add(i, "hash-shaped", "warn",
                    "A 40 or 64 digit hex value. Confirm it is an interaction hash or a commit id, not a key.", hide=True)
            else:
                hint = (" It is 40 or 64 hex digits: if it is an interaction hash or a commit id, run again with --hashes-ok."
                        if only_hash_shapes(line) else "")
                add(i, "secret-shaped", "error",
                    "A secret-shaped value. Remove it. Name the variable and where it lives, never the value." + hint,
                    hide=True)
        if EM_DASH.search(line):
            add(i, "em-dash", "error", "Em dash. Use a comma, a colon or a full stop.", line)
        m = PLACEHOLDER.search(line)
        if m:
            add(i, "placeholder", "error", "Unfilled placeholder. Placeholders never ship.", line)
        if MARKERS.search(line):
            add(i, "skill-marker", "error", "A skill marker (ASK:, GATE, $SKILLS, a moi-* skill name) must not reach a person.", line)
        if OPERATOR_WORD.search(line):
            add(i, "operator-word", "warn", "The message goes out in the operator's own name. Cut 'the operator' and 'Claude'.", line)
        if LABEL_ERR.search(line):
            add(i, "label-owner", "error", "An 'Owner:' style label reads as a form. Write it as a person would.", line)
        elif LABEL_WARN.search(line):
            add(i, "label-line", "warn", "A labelled field reads as a form. Write plain sentences.", line)
        if BOILERPLATE.search(line):
            add(i, "boilerplate", "error", "Boilerplate. Say what is needed and why, for this app.", line)
        if asks_for_secret(line):
            lvl = "error" if kind == "devops" else "warn"
            add(i, "secret-ask", lvl, "Never ask anyone to send or paste a secret value. Secrets live in GitHub.", line)
        if AM_UTC.search(line):
            add(i, "twelve-am-utc", "error", "Write 00:00 UTC with the date and the India time, never 12:00 AM UTC.", line)
        if RELATIVE.search(line):
            add(i, "relative-time", "warn", "Relative time goes stale. Write the date, 24-hour UTC and India time.", line)
        for wm in WEEKDAY.finditer(line):
            if not re.search(r"\d", line[wm.end():wm.end() + 25]):
                add(i, "weekday-no-date", "warn", "A weekday with no date. Add the date.", line)
                break
        wrong = weekday_mismatch(line)
        if wrong:
            add(i, "weekday-date-mismatch", "error", "The weekday and the date disagree: %s. Run time-table.sh." % wrong, line)
        if TZ_ABBREV.search(line):
            add(i, "tz-abbreviation", "warn", "US zone abbreviations are wrong half the year. Use UTC or area/city.", line)
        if IPV4.search(line):
            add(i, "ip-address", "warn", "An IP address. It belongs only in the message the operator sends, never in a saved draft.", line)
        if SECURITY.search(line):
            add(i, "security-detail", "warn",
                "Do not describe or mention a security weakness or finding in a draft. Tell the operator only the "
                "one line on that product's row in moi-devrel/references/repo-map.md and leave it out of the message.", line)
        if "AGENT_KEY_ENCRYPTION_SECRET" in line and ROTATE.search(line):
            add(i, "never-rotate", "error", "AGENT_KEY_ENCRYPTION_SECRET is never rotated. If this is not a request to rotate it, reword the line.", line)
        if kind == "devops":
            if PLATFORM.search(line):
                add(i, "settled-subject", "error",
                    "The platform wallet was settled with DevOps by 2026-08-03. Do not raise it again.", line)
            if VERCEL.search(line):
                add(i, "vercel", "warn",
                    "The MOI sites and the Launchpad moved off Vercel in August 2026 (a few demos still run there). "
                    "Say VM, GitHub Actions or Cloudflare Pages.", line)
        if kind == "status":
            for name, rx in SECTION:
                if rx.search(line):
                    section = name
                    if name == "done":
                        seen_done = True
                    if name in ("todo", "unverified"):
                        seen_open = True
                    break
            else:
                if section in (None, "done") and FUTURE.search(line):
                    add(i, "future-claim", "warn", "Future tense outside a To do section. Label planned work as a to-do.", line)
                if section == "done" and BULLET.match(line) and not EVIDENCE.search(line):
                    add(i, "done-no-evidence", "warn", "A Done line with no PR, commit, URL or date. Add its evidence.", line)
        if not in_fence:
            asks += URL.sub("", line).count("?")
            if NUMBERED.match(line):
                numbered += 1

    n_lines = len([ln for ln in lines if ln.strip()])
    n_chars = len(text)
    if kind != "status":
        if asks > 1 and numbered < 2:
            findings.append((1, "several-asks", "warn",
                             "More than one question and no numbered points. Split the message, or number the points.", "(whole draft)"))
        if asks == 0:
            findings.append((1, "no-question", "warn",
                             "No question mark. Phrase the ask as a question the reader can answer.", "(whole draft)"))
    if kind == "status" and not seen_open:
        findings.append((1, "status-no-open-items", "warn",
                         "No To do or Not verified line. Say what is still open, or that nothing is.", "(whole draft)"))
    if not any_date:
        findings.append((1, "no-date", "warn",
                         "No calendar date. Say the date you need an answer by.", "(whole draft)"))
    if max_lines is not None and n_lines > max_lines:
        findings.append((1, "long", "warn", "%d non-empty lines, over the %d you set." % (n_lines, max_lines), "(whole draft)"))
    if max_chars is not None and n_chars > max_chars:
        findings.append((1, "long", "warn", "%d characters, over the %d you set." % (n_chars, max_chars), "(whole draft)"))
    findings.sort(key=lambda f: (f[0], f[1]))
    return findings, n_lines, n_chars, asks, numbered


def fail(msg):
    sys.stderr.write("check-message: %s\n" % msg)
    sys.exit(2)


def nonneg(v):
    try:
        n = int(v)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a whole number of 0 or more")
    if n < 0:
        raise argparse.ArgumentTypeError("must be a whole number of 0 or more")
    return n


def main():
    ap = argparse.ArgumentParser(prog="check-message.py", description="Last check on a drafted teammate message.")
    ap.add_argument("--to", choices=["devops", "protocol", "reviewer", "status", "other"], default="other")
    ap.add_argument("--max-lines", type=nonneg, default=None)
    ap.add_argument("--max-chars", type=nonneg, default=None)
    ap.add_argument("--hashes-ok", action="store_true",
                    help="treat a 40 or 64 digit hex value as a warning, not an error (interaction hashes, commit ids)")
    ap.add_argument("draft")
    args = ap.parse_args()

    path = args.draft
    if is_env_file(path):
        fail("refusing to read %s: an env file can hold keys and is never opened" % os.path.basename(path))
    try:
        st = os.stat(path)
    except OSError as e:
        reason = "no such file" if isinstance(e, FileNotFoundError) else (e.strerror or "unreadable")
        fail("cannot read %s: %s" % (path, reason))
    if stat.S_ISDIR(st.st_mode):
        fail("%s is a folder, not a draft file" % path)
    if not stat.S_ISREG(st.st_mode):
        fail("%s is not a regular file (a pipe, device or socket). Save the draft to a file first" % path)
    if st.st_size > MAX_BYTES:
        fail("%s is %d bytes. A message that long is a document: put it in a doc and send a short message" % (path, st.st_size))
    try:
        with open(path, "rb") as fh:
            data = fh.read(MAX_BYTES + 1)
    except OSError as e:
        fail("cannot read %s: %s" % (path, e.strerror or "unreadable"))
    if len(data) > MAX_BYTES:
        fail("%s is longer than %d bytes. A message that long is a document: put it in a doc and send a short message"
             % (path, MAX_BYTES))
    if b"\x00" in data:
        fail("%s looks binary. Give it a plain text draft" % path)
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        fail("%s is not UTF-8 text" % path)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text.strip():
        fail("%s is empty" % path)

    findings, n_lines, n_chars, asks, numbered = analyse(text, args.to, args.max_lines, args.max_chars, args.hashes_ok)
    errors = warns = 0
    out = []
    for n, rule, level, msg, ex in findings:
        tag = rule if level == "error" else rule + "(warn)"
        out.append("%s:%d:%s:%s | %s" % (path, n, tag, msg, ex))
        if level == "error":
            errors += 1
        else:
            warns += 1
    try:
        if out:
            sys.stdout.write("\n".join(out) + "\n")
        sys.stdout.flush()
    except BrokenPipeError:
        pass
    sys.stderr.write(
        "check-message: %d error(s), %d warning(s); kind %s; %d non-empty lines, %d characters, %d question mark(s), "
        "%d numbered point(s). Also run slop-lint.sh and secret-scan.sh from the same folder.\n"
        % (errors, warns, args.to, n_lines, n_chars, asks, numbered))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as exc:  # never a traceback for a person who gave bad input
        sys.stderr.write("check-message: could not process the draft (%s)\n" % type(exc).__name__)
        sys.exit(2)
