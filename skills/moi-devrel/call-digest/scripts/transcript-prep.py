#!/usr/bin/env python3
"""transcript-prep.py: get a call transcript ready to digest without repeating what must not be repeated.

Usage (SKILLS is the folder that holds the moi-* skills; quote it, a path can hold spaces):
    python3 "$SKILLS/moi-devrel/call-digest/scripts/transcript-prep.py" <transcript>
    python3 "$SKILLS/moi-devrel/call-digest/scripts/transcript-prep.py" <transcript> --out <cleaned-copy>
    python3 "$SKILLS/moi-devrel/call-digest/scripts/transcript-prep.py" <transcript> --out <cleaned-copy> --force
    python3 "$SKILLS/moi-devrel/call-digest/scripts/transcript-prep.py" <transcript> --limit 50      (cap each list at 50 rows)

What it does, in order:
  1. Reads the transcript (plain text from Otter, Gemini notes, Zoom or Meet; .txt .md .vtt .srt).
     It never changes the input and never touches the network. It refuses an env-named file
     (.env, .env.*, *.env, anything holding .env.) without opening it, and it follows a symlink
     before checking the name.
  2. Masks what must not be repeated: secret-shaped strings (long hex, API key and token prefixes,
     JWTs, webhook URLs, bot tokens, private key headers, long mixed tokens, a secret-named
     assignment, a spoken password with a digit in it), personal-provider email addresses, phone
     numbers, and recovery-phrase shapes (a run of 12 or more short words, with or without list
     numbers between them, 12 or more lines of one short word each, the words that follow "word
     number three is" or "the 5th word is", and, in the 25 lines after "seed phrase" or "recovery
     phrase" is mentioned, any line of 1 to 11 short words with no common English word). Masking
     happens first.
     Every list below is built from the masked text, and a long word, or a word of 12 or more
     characters that holds a digit, is shown as a placeholder, so a value is never printed.
  3. Prints a report to stdout: format and size, the last timecode, speaker labels with turns and
     share of the text, privacy findings (line numbers and rule names only), known mishearings and
     corrected wordings from the table below, every number, version and amount, every date and
     time, and every capitalised name with its lines, split into people on the roster, known MOI
     terms and other words to spell-check.
  4. With --out PATH, writes the masked copy to PATH and nowhere else. The copy keeps one output line
     per input line, so line numbers in the report match the original. PATH must not exist (--force
     replaces a plain file), must not be the input, must not be env-named and must not be a symlink.
     The copy is created readable by its owner only.

THIS IS A BACKSTOP, NOT PROOF. A clean result does not mean the transcript holds no secret: a phrase
spoken in some other way, a key spelled out letter by letter and a value shown only on a shared
screen are not caught. Read references/privacy.md. The numbers, dates and names are a checklist, not
an extraction of claims: nothing here says a figure is right.

Exit codes: 0 done and nothing secret-shaped was masked
            1 done and at least one secret-shaped or recovery-phrase-shaped item was masked
              (read the Privacy section of the report, then references/privacy.md)
            2 bad input or an unwritable output: nothing was changed
Python 3 standard library only.
"""
import argparse
import os
import re
import signal
import sys

MAX_BYTES = 10 * 1024 * 1024

# ---------------------------------------------------------------------------------------------
# KNOWN MISHEARINGS: the small table to edit. Same rows as references/mishearings.md.
# (id, regex, ignore case, the form to check against, kind, where it was recorded)
#   heard    a recorded mishearing: auto-notes wrote the left side for the right side
#   check    recorded as unreliable, but the intended form was not recorded: ask what was meant
#   wording  a spoken form MOI has corrected (moi-devrel/references/terminology.md)
# ---------------------------------------------------------------------------------------------
MISHEARINGS = [
    ("moy", r"\bmoy\b", True, "MOI", "heard", "Gemini notes, read 2026-10-02"),
    ("koi", r"\bkoi\b", True, "KMOI", "heard", "Gemini notes, read 2026-10-02"),
    ("server-labs", r"\bser(?:ver|val)\s+labs\b", True, "Sarva Labs", "heard", "Gemini notes; the 2026-09-14 call transcript"),
    ("grock", r"\bgrock\b", True, "Groq", "heard", "Gemini notes, read 2026-10-02"),
    ("x402", r"\bx\s?(?:42|002)\b", True, "x402 (the payment protocol)", "heard", "Otter file of 2026-08-04, read 2026-10-03"),
    ("my-forge", r"\bmy\s+forge\b", True, "MOI Forge", "heard", "Gemini notes of Forge calls"),
    ("open-claw", r"\bopen\s+claw\b", True, "OpenClaw (one word; intended form inferred)", "heard", "Gemini notes, read 2026-10-02"),
    ("hermes", r"\bhermes\b", True, "check what was meant (the session 3 roadmap lists Hermes as a framework)", "check", "Gemini notes, read 2026-10-02"),
    ("voyage", r"\bvoyage\b", True, "Voyage is the explorer site, not the network; check it was not another word", "check", "pasted Otter or Zoom transcripts"),
    ("iome", r"\biome\b", True, "IOME is the earlier wallet login; check it was not MOI or MOI Wallet", "check", "pasted Otter or Zoom transcripts"),
    ("kl-or-pr", r"\bkl\s+or\s+pr\b", True, "check what was meant", "check", "Gemini standup notes, August 2026"),
    ("lms", r"\blms\b", True, "check what was meant", "check", "Gemini standup notes, August 2026"),
    ("twelve-am-utc", r"(?<![\d:])\b(?:12|0?0)(?::00)?\s*(?:am|a\.m\.)\s+utc\b", True, "00:00 UTC with the date and IST", "wording", "2026-09-10 release time misread"),
    ("us-zone", r"\b(?:EST|EDT|PST|PDT)\b", False, "area/city zone; convert with time-table.sh", "wording", "calendar.md, time zones"),
    ("rc-suffix", r"\brc\s?\d\b|\brelease candidate\b", True, "keep the -rc suffix; a candidate is not shipped", "wording", "CC13, 2026-08-27"),
    ("voyage-devnet", r"\bvoyage\s+devnet\b", True, "devnet", "wording", "terminology.md, 2026-09-25"),  # slop-lint: ignore
    ("chain-id", r"\bchain[- ]?id\b", True, "network ID (MOI's own identifier)", "wording", "terminology.md, 2026-09-14"),  # slop-lint: ignore
    ("account-centric", r"\baccount[- ](?:centric|based)\b", True, "participant-centric", "wording", "terminology.md, 2026-09-14"),  # slop-lint: ignore
    ("old-network", r"\b(?:indus|babylon)\b", True, "devnet (retired or other network name)", "wording", "terminology.md"),  # slop-lint: ignore
    ("building-in-public", r"\bbuilding in public\b", True, "The Campfire Chat (retired call name)", "wording", "CC14, 2026-09"),  # slop-lint: ignore
]
MIS_COMPILED = [(i, re.compile(rx, re.I if ic else 0), want, kind, src) for i, rx, ic, want, kind, src in MISHEARINGS]

# People who appear in the evidence (first names, lowercase) and a note where the name needs care.
ROSTER = {
    "rahul": "", "gokul": "", "upendhar": "", "vinay": "", "prakhar": "", "abhinav": "", "robert": "",
    "spendl": "", "špendl": "", "chetna": "", "manish": "", "shameer": "", "kiran": "",
    "vardan": "", "piyush": "", "sujatha": "", "prateek": "", "louis": "",
    "sai": "Sai Kiran?",
    "srikar": "spelling varies on record (also Sreekar)", "sreekar": "spelling varies on record (also Srikar)",
    "harsh": "ambiguous, ask which: Harsh Gupta (Points), Harsh Rastogi (SDK), and a Harsh tied to Galxe",
    "ram": "shares a first letter with Rahul and Rishal: confirm who spoke",
    "rishal": "shares a first letter with Rahul and Ram: confirm who spoke",
    "ruta": "the host; two spellings on record (also Rutha): confirm with the host",
    "rutha": "the host; two spellings on record (also Ruta): confirm with the host",
    "krishna": "the video editor, match inferred: confirm",
    "adithya": "the previous operator", "adi": "the previous operator (nickname)",
    "bertan": "heard at session III, spelling unverified",
}
KNOWN_TERMS = frozenset((
    "moi kmoi masn mas0 masx mas1 anu voyage "
    "coco cocolang pisa launchpad explorer dataroom points mcp "
    "x402 casa caip sarva foundation campfire scribble buffer "
    "mailchimp luma discord telegram slack otter gemini zoom "
    "teams github cloudflare supabase vercel groq openai anthropic "
    "claude openclaw teleport mdag tesseract tesseracts babylon indus "
    "iome wallet sprint forge builders presidency pccoe moipod "
    "sdk rpc npm ghcr nginx youtube linkedin twitter "
    "ama kra "
).split())
KNOWN_PREFIXES = ("js-moi", "go-moi", "go-pisa", "moi-", "coco-", "voyage-", "js-polo")
LOWER_OK = frozenset(("x402", "moipod", "mas0", "masx", "mas1"))
NOT_NAMES = frozenset((
    "ok am pm utc gmt ist "
    "est edt pst pdt cet cest "
    "bst eod eow cob "
).split())

# ---------------------------------------------------------------------------------------------
# What to mask
# ---------------------------------------------------------------------------------------------
SECRET_RULES = [
    ("openai-style-key", re.compile(r"\bsk-[A-Za-z0-9_-]{8,}")),
    ("groq-api-key", re.compile(r"\bgsk_[A-Za-z0-9]{12,}")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_-]{20,}")),
    ("aws-access-key-id", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{12,}")),
    ("stripe-live-key", re.compile(r"\b(?:sk|rk)_live_[0-9A-Za-z]{8,}")),
    ("npm-token", re.compile(r"\bnpm_[A-Za-z0-9]{20,}")),
    ("github-token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{16,}|\bgithub_pat_[A-Za-z0-9_]{16,}")),
    ("slack-token", re.compile(r"\bxox[abprso]-[A-Za-z0-9-]{8,}")),
    ("slack-webhook-url", re.compile(r"https://hooks\.slack\.com/services/\S+")),
    ("discord-webhook-url", re.compile(r"https://(?:ptb\.|canary\.)?discord(?:app)?\.com/api/webhooks/\S+")),
    ("telegram-bot-token", re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{30,}")),
    ("private-key-block", re.compile(r"-----BEGIN (?:[A-Z]+ )*PRIVATE KEY(?: BLOCK)?-----")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{6,}\.eyJ[A-Za-z0-9_-]{6,}\.[A-Za-z0-9_-]{6,}")),
    ("long-hex", re.compile(r"0x[0-9A-Fa-f]{17,}|[0-9A-Fa-f]{24,}")),
]
MIXED_RUN = re.compile(r"[A-Za-z0-9+/=]{24,}")   # a run holding a letter and a digit is masked (see mask_line)
ASSIGN = re.compile(
    r"\b[a-z0-9_]{0,40}(?:secret|token|passw(?:or)?d|passphrase|mnemonic|api_?key|private_?key)[a-z0-9_]{0,40}[\"']?\s*[=:]\s*[\"']?([A-Za-z0-9+/_=.\-]{20,})",
    re.I)
SPOKEN_CREDENTIAL = re.compile(
    r"\b(?:password|passcode|pass phrase|api key|access key|secret key|private key|auth token|bearer token)\b[^.\n]{0,20}?"
    r"\b(?:is|was|equals|=|:)\s+[\"']?((?=[^\s\"']*\d)[^\s\"']{6,})", re.I)
CREDENTIAL_CUE = re.compile(r"\b(?:password|passcode|passphrase|api key|access key|secret key|private key|auth token|bearer token)\b", re.I)
# The look-behind keeps the search from starting inside a long run of name characters: without it a 100 KB
# line with no "@" took half a minute (quadratic backtracking).
PERSONAL_MAIL = re.compile(
    r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+@(?:gmail|googlemail|yahoo|ymail|hotmail|outlook|live|msn|icloud|me|mac|aol|proton|protonmail|pm|gmx|"
    r"yandex|mail|rediffmail|hey|fastmail|zoho|tutanota)\.[A-Za-z.]{2,}", re.I)
PHONE = re.compile(
    r"(?<![\w.])\+\d{1,3}[\s.-]?(?:\d[\s.-]?){8,12}\d(?!\w)"
    r"|(?<![\w.])\(\d{3}\)[\s.-]?\d{3}[\s.-]\d{4}(?!\w)"
    r"|(?<![\w.])\d{3}[\s.-]\d{3}[\s.-]\d{4}(?!\w)"
    r"|(?<![\w.,])[6-9]\d{4}[\s-]\d{5}(?![\w,])"
    r"|(?<![\w.,])[6-9]\d{9}(?![\w,])")

# Recovery phrases: 3 to 8 letter words, the BIP-39 shape the MOI Wallet uses.
PHRASE_MIN = 12
# Common English words that are NOT on the BIP-39 list (the 2048-word English list in the js-moi-bip39 package; every
# word below was checked against it on 2026-10-03, and none is on it). A run that holds one is prose, never a phrase.
# Do not add a word without checking it against that list: "that", "this", "they", "then", "there", "will", "what",
# "when", "can", "you", "have", "right", "sure", "okay" and "thank" ARE on the list and must stay out of this set.
STOPWORDS = frozenset((
    "after and are been being both but could "
    "did does each every for from get got "
    "had has her here him his how its "
    "let many may most not our out per "
    "see she should some than the their them "
    "these those too using via was were which "
    "while who why with would yes your said "
    "yeah thanks done going think look take back "
    "actually agreed although anyone anything asked called came "
    "comes days deadline decided decision deck docs doing "
    "everyone friday gets getting goes gone gonna guys "
    "having hours lot maybe means meant minutes monday "
    "months nobody others probably really saying says seeing "
    "slides talked talking thursday tuesday told though updates "
    "wanna week weeks well went whether working works "
    "yours years "
).split())
# Back-channel words that a one-word line or a short line after a phrase cue may be without being a secret
# (all checked against the same list).
BENIGN_SHORT = STOPWORDS | frozenset("hmm yep nope umm uhh alright".split())
PIECE = re.compile(r"[A-Za-z]+|[^A-Za-z]+")
NUMBERING = re.compile(r"[\s,;]*\d{1,2}\s*[.):\-]?[\s,;]*")   # "1.", "2)", "3:" between the words of a numbered list
SINGLE = re.compile(r"^\s*(?:[-*+>]+\s*)?(?:\d{1,3}[.):]\s*)?[`\"'(\[]?([A-Za-z]{3,8})[`\"')\]]?[,;]?\s*$")
PHRASE_CUE = re.compile(
    r"\b(?:seed(?:\s+(?:phrase|words?))?|recovery\s+(?:phrase|words?)|secret\s+recovery|mnemonic|backup\s+phrase|"
    r"(?:12|24|twelve|twenty[- ]four)[- ]words?)\b", re.I)
POSITIONAL = re.compile(
    r"\b(?:word\s*(?:number\s*|no\.?\s*|#\s*)?(?:\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
    r"|(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|last|next|\d{1,2}(?:st|nd|rd|th))\s+word"
    r"|(?:number|no\.)\s*#?\s*\d{1,2})"
    r"[\s,:=(\[-]*(?:(?:it|that|this|its|is|was|are|the|word|says|said)\s*[\s,:=(\[-]*)*[\"'“]?([A-Za-z]{3,8})\b", re.I)
AFTER_CUE_WORDS = re.compile(
    r"(?:\bis|\bwas|\bare|:|=)\s+((?:[A-Za-z]{3,8}[\s,]+){2,}[A-Za-z]{3,8})\b")
CUE_WINDOW = 25

# ---------------------------------------------------------------------------------------------
# Line shapes
# ---------------------------------------------------------------------------------------------
TS = r"(?:\d{1,2}:)?\d{1,3}:\d{2}(?:[.,]\d{1,3})?"
RE_CUE = re.compile(r"^\s*(?P<ts>%s)\s*-->\s*%s" % (TS, TS))
RE_LABEL_TS = re.compile(r"^\s*(?P<spk>[A-Za-z][A-Za-z0-9 .'’\-]{0,40}?)\s{1,}(?P<ts>%s)\s*$" % TS)
RE_TS_ONLY = re.compile(r"^\s*\[?(?P<ts>%s)\]?\s*$" % TS)
RE_INLINE = re.compile(
    r"^\s*(?:\[?(?P<ts>%s)\]?\s+)?(?P<spk>[A-Z][A-Za-z0-9.'’\-]*(?: [A-Za-z0-9.'’\-]+){0,3}?):\s+(?P<rest>\S.*)$" % TS)
RE_SHARE = re.compile(r"^\s*(?P<spk>[A-Za-z][A-Za-z0-9 .'\u2019\-]{0,40}?)\s*\((?P<pct>\d{1,3})%\)\s*$")
RE_SECTION = re.compile(r"^\s*#*\s*(summary|decisions?|next steps?|action items?|details|transcript|keywords|speakers)\s*:?\s*$", re.I)
NOT_SPEAKERS = frozenset("note notes summary decision decisions next action actions details warning example q a re fwd subject date time "
                         "agenda attendees keywords speakers transcript todo link links source".split())


def looks_like_name(spk):
    words = spk.split()
    if not 1 <= len(words) <= 4:
        return False
    if spk.split()[0].lower() in NOT_SPEAKERS and len(words) == 1:
        return False
    return all(w[0].isupper() or w[0].isdigit() for w in words)


def split_label(kind, line):
    """Split an inline 'Name: text' line into the label part and the spoken part."""
    if kind == "inline":
        m = RE_INLINE.match(line)
        if m:
            return line[:m.start("rest")], line[m.start("rest"):]
    return "", line


def to_seconds(ts):
    parts = re.split(r"[:]", re.sub(r"[.,]\d+$", "", ts))
    try:
        nums = [int(p) for p in parts]
    except ValueError:
        return None
    total = 0
    for n in nums:
        total = total * 60 + n
    return total


def fmt_seconds(total):
    return "%d:%02d:%02d" % (total // 3600, (total % 3600) // 60, total % 60)


# ---------------------------------------------------------------------------------------------
# Env-file guard and reading
# ---------------------------------------------------------------------------------------------
def is_env_named(path):
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


BAD_EXT = {".zip": "unzip it first and pass the text file inside", ".pdf": "export the transcript as plain text",
           ".docx": "export the document as plain text", ".doc": "export the document as plain text",
           ".pptx": "this is a deck, not a transcript", ".xlsx": "this is a sheet, not a transcript",
           ".mp4": "this is a recording, not a transcript", ".mov": "this is a recording, not a transcript",
           ".m4a": "this is a recording, not a transcript", ".mp3": "this is a recording, not a transcript",
           ".wav": "this is a recording, not a transcript", ".png": "this is an image", ".jpg": "this is an image",
           ".jpeg": "this is an image", ".gz": "unpack it first", ".gdoc": "export the document as plain text"}


class Bad(Exception):
    pass


def read_input(path):
    if is_env_named(path):
        raise Bad("refusing %s: the name marks it as an env file, which is never opened" % os.path.basename(path))
    ext = os.path.splitext(path)[1].lower()
    if ext in BAD_EXT:
        raise Bad("%s is not a plain-text transcript: %s" % (os.path.basename(path), BAD_EXT[ext]))
    try:
        st = os.stat(path)
    except FileNotFoundError:
        raise Bad("no such file: %s" % path)
    except OSError as exc:
        raise Bad("cannot read %s: %s" % (path, exc.strerror or "error"))
    if os.path.isdir(path):
        raise Bad("%s is a folder: pass the transcript file" % path)
    if not os.path.isfile(path):
        raise Bad("%s is not a regular file" % path)
    if st.st_size > MAX_BYTES:
        raise Bad("%s is %d bytes: over the %d byte limit. Split it or pass the Summary and Transcript parts apart"
                  % (os.path.basename(path), st.st_size, MAX_BYTES))
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        raise Bad("cannot read %s: %s" % (path, exc.strerror or "error"))
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
        try:
            text = data.decode("utf-16")
        except UnicodeError:
            raise Bad("%s starts like UTF-16 text but does not decode" % os.path.basename(path))
    else:
        if b"\x00" in data[:8192]:
            raise Bad("%s looks binary (it holds NUL bytes): export the transcript as plain text" % os.path.basename(path))
        text = data.decode("utf-8-sig", errors="replace")
        bad = text.count("�")
        if bad > max(20, len(text) // 50):
            raise Bad("%s is not UTF-8 text (%d undecodable bytes)" % (os.path.basename(path), bad))
    return text, len(data)


# ---------------------------------------------------------------------------------------------
# Masking
# ---------------------------------------------------------------------------------------------
def mark(rule):
    return "[masked:%s]" % rule


def mask_phrase_runs(line):
    """Mask runs of PHRASE_MIN or more 3 to 8 letter words that hold no common English word."""
    pieces = [(m.group(0), m.start(), m.end()) for m in PIECE.finditer(line)]
    spans, run = [], []

    def close():
        if len(run) >= PHRASE_MIN:
            spans.append((run[0][1], run[-1][2]))
        del run[:]

    for text, a, b in pieces:
        if text[0].isalpha():
            if 3 <= len(text) <= 8 and text.lower() not in STOPWORDS:
                run.append((text, a, b))
            else:
                close()
        elif re.fullmatch(r"[\s,;]+", text) or NUMBERING.fullmatch(text):
            continue      # a space, a comma, or a list number such as " 7. " between two words
        else:
            close()
    close()
    for a, b in reversed(spans):
        line = line[:a] + mark("recovery-phrase-run") + line[b:]
    return line, len(spans)


def mask_line(line, hits):
    """Mask one line. hits is a list that gets one rule name per substitution."""
    for rule, rx in SECRET_RULES:
        line, n = rx.subn(mark(rule), line)
        hits.extend([rule] * n)
    pieces, last, n = [], 0, 0
    for m in MIXED_RUN.finditer(line):
        tok = m.group(0)
        if re.search(r"[A-Za-z]", tok) and re.search(r"\d", tok):
            pieces.append(line[last:m.start()])
            pieces.append(mark("long-mixed-token"))
            last = m.end()
            n += 1
    if n:
        pieces.append(line[last:])
        line = "".join(pieces)
        hits.extend(["long-mixed-token"] * n)

    def sub_group(rx, rule, text):
        out, pos, count = [], 0, 0
        for m in rx.finditer(text):
            out.append(text[pos:m.start(1)])
            out.append(mark(rule))
            pos = m.end(1)
            count += 1
        out.append(text[pos:])
        return "".join(out), count

    line, n = sub_group(ASSIGN, "secret-named-assignment", line)
    hits.extend(["secret-named-assignment"] * n)
    line, n = sub_group(SPOKEN_CREDENTIAL, "spoken-credential", line)
    hits.extend(["spoken-credential"] * n)
    line, n = PERSONAL_MAIL.subn(mark("personal-email"), line)
    hits.extend(["personal-email"] * n)
    line, n = PHONE.subn(mark("phone-number"), line)
    hits.extend(["phone-number"] * n)
    line, n = mask_phrase_runs(line)
    hits.extend(["recovery-phrase-run"] * n)
    return line


# ---------------------------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------------------------
MONTHS = "January|February|March|April|June|July|August|September|October|November|December"
MON3 = "Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec"
WEEKDAYS = "Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday"
DATE_RX = [re.compile(p, re.I) for p in (
    r"\b\d{4}-\d{2}-\d{2}\b",
    r"\b\d{4}/\d{2}/\d{2}\b",
    r"(?<![\d/])\b\d{1,2}/\d{1,2}/\d{2,4}\b",
    r"\b(?:%s|%s|May)\.?\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s+\d{4})?\b" % (MONTHS, MON3),
    r"\b\d{1,2}(?:st|nd|rd|th)?\s+(?:of\s+)?(?:%s|%s|May)(?:,?\s+\d{4})?\b" % (MONTHS, MON3),
    r"\b(?:in|of|by|until|since|from|last|next|this|early|late|mid)\s+May\b",
    r"\b(?:%s)\b" % MONTHS,
    r"\b(?:%s)\b" % WEEKDAYS,
    r"\b(?:today|tomorrow|yesterday|tonight|tonite)\b",
    r"\b(?:this|next|last|coming|previous)\s+(?:week|weekend|month|quarter|year|morning|afternoon|evening|call|session|release|%s)\b" % WEEKDAYS,
    r"\b(?:end of|by the end of|beginning of|start of|middle of)\s+(?:the\s+)?(?:day|week|month|quarter|year)\b",
    r"\b(?:EOD|EOW|COB)\b",
    r"\bin\s+(?:a|an|\d+|one|two|three|four|five|six|seven|ten)\s+(?:minutes?|hours?|days?|weeks?|months?)\b",
    r"\b\d{1,2}(?::\d{2})?\s?(?:am|pm|a\.m\.|p\.m\.)(?!\w)",
    r"(?<![\d:.])\b\d{1,2}:\d{2}\b(?![:.]\d)",
    r"\b(?:UTC|GMT|IST|EST|EDT|PST|PDT|CET|CEST|BST)\b",
    r"\bQ[1-4]\b",
)]
UNITS = "zero|one|two|three|four|five|six|seven|eight|nine"
TEENS = "ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen"
TENS = "twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety"
SCALE = "hundred|thousand|million|billion|trillion|lakh|crore"
NUMWORD = r"(?:%s|%s|%s|%s|half|dozen)" % (UNITS, TEENS, TENS, SCALE)
NUM_PHRASE = re.compile(r"\b%s(?:(?:[-\s]|\s+and\s+)%s)*(?:\s?k\b)?" % (NUMWORD, NUMWORD), re.I)
NUM_UNIT_AFTER = re.compile(r"\s+(?:kmoi|anu|percent|per cent|points?|%)", re.I)
NUM_VERSION = re.compile(r"\bv?\d+\.\d+\.\d+(?:-?rc\d*)?\b", re.I)
NUM_DIGITS = re.compile(
    r"(?<![\w.:/-])\$?\d+(?:,\d+)*(?:\.\d+)?(?:\s?(?:%|percent|KMOI|anu|[kKmMbB](?![A-Za-z])))?(?![\w:])")
TOKEN = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ0-9'’\-]*")


class Group(object):
    def __init__(self):
        self.items = {}
        self.order = []
        self.total = 0

    def add(self, key, line, snippet, display=None):
        self.total += 1
        if key not in self.items:
            self.items[key] = {"n": 0, "lines": [], "snip": snippet, "display": display or key}
            self.order.append(key)
        it = self.items[key]
        it["n"] += 1
        if not it["lines"] or it["lines"][-1] != line:
            it["lines"].append(line)


def snippet_of(text, start, end):
    s = text[max(0, start - 30):end + 30]
    s = " ".join(s.split())
    s = re.sub(r"\S{20,}", "<long>", s)
    s = re.sub(r"\S{12,19}", lambda m: "<token>" if re.search(r"[A-Za-z]", m.group(0)) and re.search(r"\d", m.group(0))
               else m.group(0), s)
    return s[:90]


def safe_display(tok):
    """A word as the report prints it: a long word, or a long one with a digit, may be a credential."""
    if len(tok) >= 20:
        return "<long word>"
    if len(tok) >= 12 and re.search(r"\d", tok):
        return "<word with digits>"
    return tok


def ranges(nums):
    nums = sorted(set(nums))
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(str(nums[i]) if i == j else "%d-%d" % (nums[i], nums[j]))
        i = j + 1
    return ", ".join(out)


def line_list(lines, cap=8):
    shown = ", ".join(str(n) for n in lines[:cap])
    if len(lines) > cap:
        shown += ", +%d more" % (len(lines) - cap)
    return shown


def analyse(raw_lines):
    """Return a dict with masked lines and everything the report needs."""
    n = len(raw_lines)
    masked = []
    hits_by_line = {}
    for i, raw in enumerate(raw_lines, 1):
        hits = []
        masked.append(mask_line(raw, hits))
        if hits:
            hits_by_line[i] = hits

    kinds = [None] * n          # blank, label, ts, cue, inline, content, meta, index
    speaker_at = [None] * n
    tc_at = [None] * n
    text_at = [None] * n
    cur_tc, cur_spk = None, None
    labels, label_count, cue_count, inline_count = {}, 0, 0, 0
    sections = []
    header_share = {}
    first_label_line = None
    chars_unlabelled = 0
    lines_unlabelled = 0
    last_tc = None
    for idx, ln in enumerate(masked):
        s = ln.strip()
        if not s:
            kinds[idx] = "blank"
        elif s.upper().startswith("WEBVTT") or re.match(r"^(NOTE|Kind:|Language:)\b", s):
            kinds[idx] = "meta"
        elif re.fullmatch(r"\d{1,6}", s) and idx + 1 < n and RE_CUE.match(masked[idx + 1]):
            kinds[idx] = "index"
        elif RE_CUE.match(ln):
            kinds[idx] = "cue"
            cue_count += 1
            cur_tc = RE_CUE.match(ln).group("ts")
        elif RE_LABEL_TS.match(ln) and looks_like_name(RE_LABEL_TS.match(ln).group("spk").strip()):
            m = RE_LABEL_TS.match(ln)
            kinds[idx] = "label"
            label_count += 1
            if first_label_line is None:
                first_label_line = idx + 1
            cur_spk = " ".join(m.group("spk").split())
            cur_tc = m.group("ts")
            labels.setdefault(cur_spk, {"turns": 0, "chars": 0, "first": idx + 1})["turns"] += 1
        elif RE_TS_ONLY.match(ln):
            kinds[idx] = "ts"
            cur_tc = RE_TS_ONLY.match(ln).group("ts")
        elif RE_SECTION.match(ln):
            kinds[idx] = "meta"
            sections.append((RE_SECTION.match(ln).group(1).title(), idx + 1))
        elif RE_SHARE.match(ln) and looks_like_name(RE_SHARE.match(ln).group("spk").strip()):
            kinds[idx] = "meta"
            header_share[" ".join(RE_SHARE.match(ln).group("spk").split())] = RE_SHARE.match(ln).group("pct")
        else:
            m = RE_INLINE.match(ln)
            if m and looks_like_name(m.group("spk")) and m.group("spk").strip().lower() not in NOT_SPEAKERS:
                kinds[idx] = "inline"
                inline_count += 1
                if first_label_line is None:
                    first_label_line = idx + 1
                cur_spk = " ".join(m.group("spk").split())
                if m.group("ts"):
                    cur_tc = m.group("ts")
                labels.setdefault(cur_spk, {"turns": 0, "chars": 0, "first": idx + 1})["turns"] += 1
                text_at[idx] = m.group("rest")
            else:
                kinds[idx] = "content"
                text_at[idx] = ln
        speaker_at[idx] = cur_spk
        tc_at[idx] = cur_tc
        if cur_tc:
            sec = to_seconds(cur_tc)
            if sec is not None:
                last_tc = sec
        if kinds[idx] in ("content", "inline") and text_at[idx] is not None:
            if cur_spk:
                labels[cur_spk]["chars"] += len(text_at[idx])
            else:
                chars_unlabelled += len(text_at[idx])
                lines_unlabelled += 1

    # Multi-line recovery-phrase shapes, on content lines only.
    def content_core(idx):
        return text_at[idx] if kinds[idx] in ("content", "inline") else None

    run = []

    def end_run():
        if len(run) >= PHRASE_MIN:
            for j in run:
                w = SINGLE.match(content_core(j)).group(1)
                masked[j] = masked[j].replace(w, mark("recovery-phrase-line"), 1)
                hits_by_line.setdefault(j + 1, []).append("recovery-phrase-line")
        del run[:]

    for idx in range(n):
        core = content_core(idx)
        if core is None:
            continue   # blank, label and timestamp lines do not break a run
        m = SINGLE.match(core)
        if m and m.group(1).lower() not in BENIGN_SHORT:
            run.append(idx)
        else:
            end_run()
    end_run()

    # Windows after a recovery-phrase cue.
    mentions = []
    window_end = -1
    for idx in range(n):
        if kinds[idx] in ("blank", "label", "ts", "cue", "index", "meta"):
            continue
        body = text_at[idx] or ""
        on_cue_line = bool(PHRASE_CUE.search(body))
        if on_cue_line:
            mentions.append(idx + 1)
            window_end = idx + CUE_WINDOW
        if idx > window_end:
            continue
        core = content_core(idx)
        # A line after the cue that holds only 3 to 8 letter words and no common English word is hidden whole
        # (up to PHRASE_MIN - 1 words: a longer run is the recovery-phrase-run rule, and a phrase read out
        # over several lines arrives in pieces).
        short = re.findall(r"[A-Za-z]+", core) if core is not None else []
        whole_line = (core is not None and not on_cue_line
                      and 1 <= len(short) < PHRASE_MIN and all(3 <= len(w) <= 8 for w in short)
                      and not any(w.lower() in BENIGN_SHORT for w in short)
                      and "[masked:" not in core)
        body_start = masked[idx].rfind(core) if whole_line and core in masked[idx] else -1
        if body_start >= 0:
            masked[idx] = masked[idx][:body_start] + mark("recovery-phrase-window")
            hits_by_line.setdefault(idx + 1, []).append("recovery-phrase-window")
            continue

        def hide_word(m, line_no=idx + 1):
            if m.group(1).lower() in BENIGN_SHORT:
                return m.group(0)
            hits_by_line.setdefault(line_no, []).append("recovery-phrase-position")
            return m.group(0)[:m.start(1) - m.start(0)] + mark("recovery-phrase-position")

        def hide_list(m, line_no=idx + 1):
            words = m.group(1).split()
            if any(w.strip(",").lower() in STOPWORDS for w in words):
                return m.group(0)
            hits_by_line.setdefault(line_no, []).append("recovery-phrase-after-cue")
            return m.group(0)[:m.start(1) - m.start(0)] + mark("recovery-phrase-after-cue")
        masked[idx] = POSITIONAL.sub(hide_word, masked[idx])
        # The "is / are / :" list rule looks only at the words after the speaker label, so the label's own colon
        # never starts it.
        pre, rest = split_label(kinds[idx], masked[idx])
        masked[idx] = pre + AFTER_CUE_WORDS.sub(hide_list, rest)
    credential_mentions = [i + 1 for i in range(n) if kinds[i] in ("content", "inline") and CREDENTIAL_CUE.search(text_at[i] or "")
                           and (i + 1) not in hits_by_line]
    # Re-read the text of masked lines (the windows may have changed them).
    for idx in range(n):
        if kinds[idx] == "inline":
            m = RE_INLINE.match(masked[idx])
            text_at[idx] = m.group("rest") if m else masked[idx]
        elif kinds[idx] == "content":
            text_at[idx] = masked[idx]

    res = {"masked": masked, "hits_by_line": hits_by_line, "kinds": kinds, "tc_at": tc_at, "text_at": text_at,
           "labels": labels, "label_count": label_count, "cue_count": cue_count, "inline_count": inline_count,
           "sections": sections, "last_tc": last_tc, "header_share": header_share, "first_label_line": first_label_line, "lines_unlabelled": lines_unlabelled,
           "chars_unlabelled": chars_unlabelled, "mentions": mentions, "credential_mentions": credential_mentions}
    return res


def collect(res):
    kinds, text_at, tc_at = res["kinds"], res["text_at"], res["tc_at"]
    numbers, dates, names = Group(), Group(), Group()
    mis = {}
    name_forms = set()
    occurrences = []     # (line, token, sentence_start, start, end, text)
    for idx, kind in enumerate(kinds):
        if kind not in ("content", "inline"):
            continue
        text = text_at[idx] or ""
        line = idx + 1
        taken = bytearray(len(text))      # characters already claimed by a date or time
        # mishearings
        for mid, rx, want, mkind, src in MIS_COMPILED:
            for m in rx.finditer(text):
                rec = mis.setdefault(mid, {"want": want, "kind": mkind, "src": src, "heard": {}, "lines": []})
                rec["heard"][m.group(0)] = rec["heard"].get(m.group(0), 0) + 1
                if not rec["lines"] or rec["lines"][-1] != line:
                    rec["lines"].append(line)
        # dates and times
        for rx in DATE_RX:
            for m in rx.finditer(text):
                if taken[m.start()]:
                    continue
                taken[m.start():m.end()] = b"\x01" * (m.end() - m.start())
                dates.add(" ".join(m.group(0).lower().split()), line, snippet_of(text, m.start(), m.end()))
        # versions, then amounts
        ntaken = bytearray(len(text))     # characters already claimed by a version or an amount
        for m in NUM_VERSION.finditer(text):
            ntaken[m.start():m.end()] = b"\x01" * (m.end() - m.start())
            numbers.add(m.group(0).lower(), line, snippet_of(text, m.start(), m.end()))
        for m in NUM_DIGITS.finditer(text):
            if ntaken[m.start()] or taken[m.start()]:
                continue
            ntaken[m.start():m.end()] = b"\x01" * (m.end() - m.start())
            numbers.add(m.group(0).replace(" ", "").lower(), line, snippet_of(text, m.start(), m.end()))
        for m in NUM_PHRASE.finditer(text):
            phrase = " ".join(m.group(0).lower().replace("-", " ").split())
            if phrase == "one" and not NUM_UNIT_AFTER.match(text[m.end():m.end() + 12]):
                continue
            if ntaken[m.start()]:
                continue
            numbers.add(phrase, line, snippet_of(text, m.start(), m.end()))
        # capitalised words
        for m in TOKEN.finditer(text):
            tok = m.group(0).strip("'’-")
            if len(tok) < 2 or tok.lower() in NOT_NAMES or re.fullmatch(r"I['’](?:m|ll|ve|d)", tok):
                continue
            i = m.start() - 1                 # walk back over spaces and opening quotes; no copy of the line
            while i >= 0 and text[i] in " \t\"'“‘([":
                i -= 1
            start = i < 0 or text[i] in ".!?"
            occurrences.append((line, tok, start, m.start(), m.end(), text))
            low = tok.lower()
            if tok.isupper() and len(tok) >= 2 and not tok.isdigit():
                name_forms.add(low)
            elif tok[0].isupper() and not start and not any(re.fullmatch(p, tok, re.I) for p in (MONTHS, MON3, WEEKDAYS)):
                name_forms.add(low)
            elif re.search(r"[a-z][A-Z]", tok):
                name_forms.add(low)
    month_day = re.compile(r"^(?:%s|%s|%s|may)$" % (MONTHS, MON3, WEEKDAYS), re.I)
    for line, tok, start, a, b, text in occurrences:
        low = tok.lower()
        if month_day.match(tok):
            continue
        # A roster name or a known term counts only when written with a capital (harsh, ram, points, wallet are
        # ordinary words); a product prefix or x402 counts in any case.
        listed = (tok[0].isupper() and (low in name_forms or low in ROSTER or low in KNOWN_TERMS)) \
            or low.startswith(KNOWN_PREFIXES) or low in LOWER_OK
        if listed:
            shown = safe_display(tok)
            # A word that is hidden is grouped under one key, so its spelling is never a dictionary key either.
            names.add(low if shown == tok else shown, line, snippet_of(text, a, b), display=shown)
    res.update({"numbers": numbers, "dates": dates, "names": names, "mis": mis})
    return res


# ---------------------------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------------------------
def out(s=""):
    sys.stdout.write(s + "\n")


def print_group(title, group, limit, note):
    out()
    out("%s (distinct %d, occurrences %d). %s" % (title, len(group.order), group.total, note))
    if not group.order:
        out("  none found")
        return
    keys = group.order if limit == 0 else group.order[:limit]
    width = min(28, max(len(k) for k in keys))
    for k in keys:
        it = group.items[k]
        out("  %s %4d  lines %s | %s" % (k.ljust(width), it["n"], line_list(it["lines"]), it["snip"]))
    if len(keys) < len(group.order):
        out("  ... %d more not shown; run again with --limit 0 to list all" % (len(group.order) - len(keys)))


def print_names(group, limit):
    people, terms, other = [], [], []
    for k in group.order:
        if k in ROSTER:
            people.append(k)
        elif k in KNOWN_TERMS or k in LOWER_OK or k.startswith(KNOWN_PREFIXES):
            terms.append(k)
        else:
            other.append(k)
    out()
    out("Capitalised names (distinct %d). Compare each with references/mishearings.md and the roster in "
        "moi-devrel/references/people-and-teams.md." % len(group.order))
    for title, bucket in (("People on the roster", people), ("Known MOI terms", terms),
                          ("Other capitalised words: check the spelling", other)):
        out("  %s:" % title)
        if not bucket:
            out("    none")
            continue
        shown = bucket if limit == 0 else bucket[:limit]
        for k in shown:
            it = group.items[k]
            extra = ""
            if k in ROSTER and ROSTER[k]:
                extra = "  NOTE: " + ROSTER[k]
            out("    %-22s %4d  lines %s%s" % (it["display"], it["n"], line_list(it["lines"]), extra))
        if len(shown) < len(bucket):
            out("    ... %d more not shown; run again with --limit 0" % (len(bucket) - len(shown)))


def report(path, size, raw_lines, res, limit):
    kinds = res["kinds"]
    out("transcript-prep: %s" % os.path.basename(path))
    out("Read only. The original is untouched and nothing was sent anywhere. Every value below comes from the masked text.")
    fmt = []
    if res["label_count"] >= 1:
        fmt.append("speaker label then timecode on its own line (Otter style)")
    if res["cue_count"] >= 1:
        fmt.append("timed cues (VTT or SRT)")
    if res["inline_count"] >= 1:
        fmt.append("Name: text lines (Gemini or Zoom style)")
    out("Input: %d lines, %d bytes. Format guess: %s." % (len(raw_lines), size, "; ".join(fmt) if fmt else
        "no speaker labels found, so every spoken line is unattributed"))
    if res["last_tc"] is not None:
        out("Last timecode: %s. Check it is where the call ended; a cut-off file hides the last decisions." % fmt_seconds(res["last_tc"]))
    else:
        out("Last timecode: none found.")
    if res["sections"]:
        out("Sections: " + ", ".join("%s at line %d" % s for s in res["sections"]) +
            ". Text above the transcript is an auto summary: a lead, not evidence.")

    out()
    out("Speakers (%d label(s)). A label that is a number is not a name: ask the operator who was on the call (if they were not on it, ASK: Adithya)." % len(res["labels"]))
    total_chars = sum(v["chars"] for v in res["labels"].values()) + res["chars_unlabelled"]
    if res["labels"]:
        ordered = sorted(res["labels"].items(), key=lambda kv: kv[1]["first"])
        shown = ordered if limit == 0 else ordered[:limit]
        for name, v in shown:
            share = (100.0 * v["chars"] / total_chars) if total_chars else 0.0
            first = name.split()[0].lower() if name.split() else ""
            if re.match(r"^(speaker|guest|unknown|participant|host)\b", name, re.I):
                note = "  a placeholder, not a name"
            elif first in ROSTER:
                note = "  on the roster" + (": " + ROSTER[first] if ROSTER[first] else "")
            else:
                note = "  not on the roster: check the spelling and who this is"
            label = " ".join(safe_display(w) for w in name.split())
            out("  %-26s turns %4d  share %5.1f%%  first line %d%s" % (label, v["turns"], share, v["first"], note))
    else:
        out("  none")
    if res["header_share"]:
        out("  The file's own header gives each speaker's share of the talk: " +
            ", ".join("%s %s%%" % (k, v) for k, v in res["header_share"].items()))
    if res["first_label_line"] is None:
        out("  No speaker labels at all: every spoken line (%d) is unattributed. Follow references/method.md, section 4."
            % res["lines_unlabelled"])
    elif res["lines_unlabelled"]:
        out("  Lines before the first label (line %d): %d. These are the title, the header or an auto summary."
            % (res["first_label_line"], res["lines_unlabelled"]))

    out()
    hits = res["hits_by_line"]
    by_rule = {}
    for ln, rules in hits.items():
        for r in rules:
            by_rule.setdefault(r, []).append(ln)
    out("Privacy (rule and line numbers only; no value is ever printed)")
    if by_rule:
        for r in sorted(by_rule):
            out("  masked %-28s %3d  lines %s" % (r, len(by_rule[r]), ranges(by_rule[r])))
        out("  The masked copy hides these. Tell the operator now: references/privacy.md, section 3.")
    else:
        out("  nothing secret-shaped was masked")
    if res["mentions"]:
        out("  NOTE a recovery phrase or seed is mentioned at lines %s. Read the 25 lines after each in the ORIGINAL for a "
            "wallet setup on a shared screen." % ranges(res["mentions"]))
    if res["credential_mentions"]:
        out("  NOTE a password, key or token is mentioned at lines %s with no value masked. Read them." % ranges(res["credential_mentions"]))
    out("  A clean result is not proof. A phrase spelled letter by letter or shown only on a screen is not caught.")

    out()
    mis = res["mis"]
    total = sum(len(v["lines"]) for v in mis.values())
    out("Known mishearings and corrected wordings (%d rows hit, %d lines). Table: top of this script and "
        "references/mishearings.md. A hit is a prompt to check, never a correction." % (len(mis), total))
    if not mis:
        out("  none of the table's forms appear")
    for row in MISHEARINGS:
        mid = row[0]
        if mid not in mis:
            continue
        v = mis[mid]
        heard = ", ".join('"%s" x%d' % (h, c) for h, c in sorted(v["heard"].items()))
        out("  [%s] %s -> check %s | lines %s | %s" % (v["kind"], heard, v["want"], line_list(v["lines"]), v["src"]))

    print_group("Numbers, versions and amounts", res["numbers"], limit,
                "Check each against its source. Recompute any sum or unit. Two different figures for one thing are both quoted.")
    print_group("Dates and times", res["dates"], limit,
                "Turn each relative word into a date from the call date. Convert a time with time-table.sh before it is written down.")
    print_names(res["names"], limit)
    out()
    out("Next: references/method.md. This list is a checklist of what to verify, not a list of facts.")


# ---------------------------------------------------------------------------------------------
def write_copy(src, dest, lines, text, force):
    if not dest.strip():
        raise Bad("--out needs a file path")
    if os.path.isdir(dest):
        raise Bad("%s is a folder: give a file path for the masked copy" % dest)
    if is_env_named(dest):
        raise Bad("refusing to write %s: the name marks it as an env file" % os.path.basename(dest))
    if os.path.lexists(dest) and os.path.islink(dest):
        raise Bad("refusing to write %s: it is a symlink" % dest)
    if os.path.exists(dest) and os.path.realpath(dest) == os.path.realpath(src):
        raise Bad("the output path is the input file: choose another path")
    if os.path.exists(dest) and not force:
        raise Bad("%s already exists: choose a new path, or add --force to replace it" % dest)
    if os.path.exists(dest) and not os.path.isfile(dest):
        raise Bad("%s is not a regular file" % dest)
    folder = os.path.dirname(os.path.abspath(dest))
    if not os.path.isdir(folder):
        raise Bad("the folder for the output does not exist: %s" % folder)
    body = "\n".join(lines)
    if text.endswith(("\n", "\r")):
        body += "\n"
    flags = os.O_WRONLY | os.O_CREAT | (os.O_TRUNC if force else os.O_EXCL)
    try:
        fd = os.open(dest, flags, 0o600)
        try:
            os.fchmod(fd, 0o600)   # a replaced file keeps its old mode unless it is set here
        except (AttributeError, OSError):
            pass
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
            fh.write(body)
    except OSError as exc:
        raise Bad("cannot write %s: %s" % (dest, exc.strerror or "error"))


def main(argv):
    parser = argparse.ArgumentParser(
        prog="transcript-prep.py", add_help=True,
        description="Mask secrets and list the numbers, dates, names and known mishearings of a call transcript. "
                    "Read-only on the input. Exit 0 clean, 1 something was masked, 2 bad input.")
    parser.add_argument("transcript", help="a plain-text transcript or auto-notes export")
    parser.add_argument("--out", metavar="PATH", help="write the masked copy here (must not exist unless --force)")
    parser.add_argument("--force", action="store_true", help="replace an existing plain file given to --out")
    parser.add_argument("--limit", type=int, default=0, metavar="N", help="cap each list at N rows (default 0: list every row)")
    args = parser.parse_args(argv[1:])
    if args.limit < 0:
        sys.stderr.write("transcript-prep: --limit must be 0 or more\n")
        return 2
    try:
        text, size = read_input(args.transcript)
        raw_lines = re.split(r"\r\n|\n|\r", text)
        if raw_lines and raw_lines[-1] == "" and len(raw_lines) > 1:
            raw_lines = raw_lines[:-1]
        if not "".join(raw_lines).strip():
            raise Bad("%s is empty" % os.path.basename(args.transcript))
        res = collect(analyse(raw_lines))
        if args.out is not None:
            write_copy(args.transcript, args.out, res["masked"], text, args.force)
        report(args.transcript, size, raw_lines, res, args.limit)
        if args.out is not None:
            out()
            out("Wrote the masked copy (%d lines, same line numbers as the original, owner-only permissions) to %s"
                % (len(res["masked"]), args.out))
        sys.stdout.flush()
    except Bad as exc:
        sys.stderr.write("transcript-prep: %s\n" % exc)
        return 2
    return 1 if res["hits_by_line"] else 0


if __name__ == "__main__":
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    try:
        code = main(sys.argv)
    except SystemExit:
        raise
    except KeyboardInterrupt:
        sys.stderr.write("transcript-prep: interrupted; nothing was changed\n")
        code = 2
    except Exception as exc:   # never a traceback: the input may hold what must not be printed
        sys.stderr.write("transcript-prep: unexpected %s; the input was not changed\n" % type(exc).__name__)
        code = 2
    sys.exit(code)
