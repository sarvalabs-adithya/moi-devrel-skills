#!/usr/bin/env python3
"""Print the sentences of a draft that need a claim check, as claim-ledger rows.

Usage (run from the working copy you are working in; SKILLS is the folder that holds the
moi-* skills, quoted because a path can hold spaces):
    python3 "$SKILLS/moi-devrel/claim-check/scripts/extract-claims.py" <file> [more files] > claims-candidates.csv
    python3 "$SKILLS/moi-devrel/claim-check/scripts/extract-claims.py" --all <file> [more files] > claims-candidates.csv
    python3 "$SKILLS/moi-devrel/claim-check/scripts/extract-claims.py" --against ledger.csv <file> [more files]
    python3 "$SKILLS/moi-devrel/claim-check/scripts/extract-claims.py" --against ledger.csv --dropped claims-candidates.csv <file> [more files]

Reads (never writes a file, never touches the network). It refuses a file whose name marks it as an
env file (.env, .env.*, *.env): those can hold keys and are never opened.
    markdown or plain text   YAML front matter (title, summary, description, takeaways, faq),
                             headings, paragraphs, list items, table rows, and one row per
                             fenced code block. HTML comments are skipped.
    HTML (a deck or page)    the visible text of every block, with the slide number, and every
                             entry of the NOTES array (the presenter script). <style>, <script>,
                             <svg>, <head> and the slide badges are skipped.

Output: CSV on stdout with the header id,claim,where,type,source,verdict,checked_by,as_of,note.
    One row per sentence that carries any of: a number, a version, a date or time, the name of a
    product or network, a superlative or universal ("first", "only", "every", "never", "all"), a
    comparison with another project, a promise about the future, or a statement that something is
    live. Two additions: a verb of what a system does (rejects, charges, signs, returns, can) and
    a vague attribution ("people say", "according to"). "where" is file:line, plus the
    slide number for a deck. "type" lists every kind found, separated by ";", in this order, which
    is the order of the kind that decides how to check the sentence: live, promise, comparison,
    universal, attribution, version, date, number, behavior, name. A fenced code block gets one row
    of type code. The verdict is always unverified. source, checked_by, as_of and note are empty.

A bare product name or a small number is enough to flag a sentence, so many rows are not claims.
Delete a row only after reading its sentence, keep the raw output, and say in the hand-back how
many rows you deleted. IT ALSO MISSES: a plain statement with no trigger word above ("The wallet
shows the address in full.", "Gokul approved the change.") is not listed. The summary on stderr
counts those sentences. Use --all to list every sentence, or read the text yourself once.
Secret shapes are masked in the claim text: a long hex string (a private key has the same
shape), common API key and token prefixes, a JWT, a private key header, a webhook URL, a long
mixed letter and digit token, and a run of 12 or more short words that could be a recovery
phrase. The mask is a backstop, not proof. Read what a row hides at the line named in "where".

--all: also list the sentences no trigger matched, with an empty type. Use it for text that will go
    out, then delete the rows that state nothing checkable.
--against LEDGER: print only what the ledger does not cover, for the re-run after the text was
    changed. Stdout gets the new rows (same columns, ids continue after the highest id in the
    ledger). Stderr lists every ledger row with verdict cut whose sentence is still in the text.
    A sentence is covered when its text equals a ledger claim after lower-casing and ignoring
    punctuation and spacing, so when you reword a sentence you must reword the ledger claim too.
--dropped CANDIDATES: with --against, a sentence that is in this file (the raw extractor output) and
    not in the ledger was dropped on purpose as not a claim, so it counts as covered. Without it,
    every row you delete from the ledger comes back as a new candidate on every re-run and the run
    can never exit 0. New ids continue after the highest id in the ledger and this file.
--start N, --prefix P: first id number (default 1) and id prefix (default C, letters then
    letters or digits).

Exit codes: 0 done (with --against: nothing new and no cut sentence left), 1 with --against and
something to do, 2 usage error, an unreadable file or ledger, or an env file.
"""
import argparse
import bisect
import csv
import os
import re
import signal
import sys
from html.parser import HTMLParser

COLUMNS = ["id", "claim", "where", "type", "source", "verdict", "checked_by", "as_of", "note"]
PRIORITY = ["live", "promise", "comparison", "universal", "attribution", "version", "date",
            "number", "behavior", "name", "code"]

# ---------------------------------------------------------------- triggers
_NUMWORDS = (r"two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|"
             r"fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|"
             r"seventy|eighty|ninety|hundreds?|thousands?|millions?|billions?|trillions?|dozens?")
NUMBER = re.compile(
    r"(?<![A-Za-z0-9_])(?:\$?\d[\d,]*(?:\.\d+)?\s?%?|0x[0-9A-Fa-f]+)(?![A-Za-z0-9_])"
    r"|\b(?:" + _NUMWORDS + r")\b", re.I)
VERSION = re.compile(
    r"(?<![A-Za-z0-9_])v?\d+\.\d+\.\d+(?:-[A-Za-z0-9.]+)?|(?<![A-Za-z0-9_])v\d+(?:\.\d+)*(?![A-Za-z0-9_])"
    r"|-rc\d+\b|\brc\d+\b|\bversion\s+v?\d")
_MONTHS = (r"January|February|March|April|May|June|July|August|September|October|November|December")
_MON3 = r"Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec"
DATE = re.compile(
    r"\b(?:" + _MONTHS + r")\b|\b(?:" + _MON3 + r")\.?\s+\d|\b\d{1,2}\s+(?:" + _MON3 + r")\b"
    r"|\b\d{4}-\d{2}-\d{2}\b|\b(?:19|20)\d\d\b|\bQ[1-4]\b"
    r"|\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b"
    r"|\b(?:UTC|GMT|IST|PST|PDT|EST|EDT|CET|CEST|BST)\b|\b\d{1,2}:\d{2}\b"
    r"|\b(?:today|tomorrow|yesterday|tonight|recently|lately)\b"
    r"|\b(?:last|next)\s+(?:week|month|year|quarter|call|session|release|friday|monday|tuesday|"
    r"wednesday|thursday|saturday|sunday)\b|\bthis\s+(?:week|month|year|quarter|morning|evening)\b"
    r"|\bsince\b|\buntil\b|\bas of\b", re.I)
NAMES = re.compile(
    r"\b(?:MOI|KMOI|MASN|MASX|MAS\d|MOIPod|moipod|Voyage|devnet|Devnet|testnet|mainnet|Babylon|Indus|"  # slop-lint: ignore
    r"js-moi-sdk|js-moi-[a-z-]+|js-polo|go-moi|go-pisa|PISA|Coco|Cocolang|Launchpad|"
    r"Agent Launchpad|Agent Explorer|Dataroom|Points Program|MOI Wallet|MCP|x402|CASA|CAIP-\d+|"
    r"Sarva Labs|MOI Foundation|Campfire Chat|Scribble|Buffer|Mailchimp|Luma)\b")
OTHERS = (r"Ethereum|ETH|Solana|Bitcoin|BTC|Sui|Aptos|Stellar|Cardano|Polygon|Arbitrum|Avalanche|"
          r"Cosmos|Stripe|Visa|Mastercard|PayPal|Lit Protocol|ERC-\d+|EIP-\d+|Optimism")
COMPARISON = re.compile(
    r"\b(?:than|unlike|versus|vs\.?|compared (?:to|with)|in contrast|better|worse|faster|slower|"
    r"cheaper|outperform\w*|instead of|rather than|similar to|same as|competitors?|alternatives?)\b"
    r"|\b(?:" + OTHERS + r")\b")
UNIVERSAL = re.compile(
    r"\b(?:first|only|every|everyone|everything|everywhere|never|always|all|anyone|anything|none|"
    r"nobody|no one|nothing|cannot|impossible|guarantee[ds]?|best|fastest|cheapest|largest|biggest|"
    r"lowest|highest|strongest|safest|simplest|easiest|most|leading|unique|entire|entirely|"
    r"completely|zero)\b|\bno\s+(?:account|user|one|developer|app|code|chain|interaction|"
    r"participant|manager)s?\b|\bat all\b|\b100\s?%", re.I)
PROMISE = re.compile(
    r"\b(?:will|won't|going to|soon|planned|plans? to|upcoming|roadmap|expected to|expects? to|"
    r"scheduled|stay tuned|we'll|to come|in the future|coming (?:soon|next|up))\b"
    r"|\bnext\s+(?:call|release|month|week|quarter|session|version)\b|\blater this\b", re.I)
LIVE = re.compile(
    r"\blive\b|\bshipped\b|\blaunched\b|\bdeployed\b|\bgenerally available\b|\bin production\b|"
    r"\brolled out\b|\brolling out\b|\bavailable\b|\bsupported\b|\bstable\b|\blatest\b|"
    r"\bcurrently\b|\bright now\b|\bat the moment\b|\bnow\s+(?:has|have|can|uses?|prices?|reads?|"
    r"supports?|accepts?|rejects?|refuses?|returns?|exports?|works?|runs?|requires?|lets?|allows?|"
    r"live|available|priced|counts?)\b|\balready\b", re.I)
ATTRIBUTION = re.compile(
    r"\b(?:most|many|some)\s+(?:teams|developers|people|projects|users|experts)\b|\bexperts?\b|"
    r"\bstudies show\b|\bresearch shows\b|\baccording to\b|\breportedly\b|\bwidely\b|"
    r"\beveryone knows\b|\bsome say\b", re.I)

BEHAVIOR = re.compile(
    r"\b(?:reject|refuse|accept|charge|pay|burn|mint|sign|lock|require|return|read|store|cover|cost|"
    r"deduct|debit|credit|fail|revert|enforce|validate|verify|verifies|allow|prevent|block|deny|"
    r"denies|grant|revoke|settle|encode|decode|derive|emit|expose|export|support|use|run|check|"
    r"charge|reserve|inflate|spend)(?:s|es|ed|d)?\b|\b(?:can|cannot|can't|must)\b", re.I)

LONG_HEX = re.compile(r"0x[0-9A-Fa-f]{17,}|[0-9A-Fa-f]{24,}")
# Common secret shapes, looser than secret-scan.sh on purpose: masking too much only costs a
# readable claim, and echoing a key into a ledger costs a rotation.
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
)]
# Words of 3 to 8 letters make up a recovery phrase. These common English words are not on the
# BIP-39 list, so a run that holds one is prose.
PHRASE_MIN = 12
PHRASE_STOP = frozenset(
    "after and are been being both but could did does each every for from get got had has her here "
    "him his how its let many may most not our out per see she should some than the their them these "
    "those too using via was were which while who why with would yes your".split())
_PIECE = re.compile(r"[A-Za-z]+|[^A-Za-z]+")


def _mask_phrases(s):
    pieces = [(m.group(0), m.start(), m.end()) for m in _PIECE.finditer(s)]
    spans, run = [], []

    def close():
        if len(run) >= PHRASE_MIN:
            spans.append((run[0][1], run[-1][2]))
        del run[:]

    for text, a, b in pieces:
        if text[0].isalpha():
            if 3 <= len(text) <= 8 and text.lower() not in PHRASE_STOP:
                run.append((text, a, b))
            else:
                close()
        elif re.fullmatch(r"[\s,;]+", text):
            continue
        else:
            close()
    close()
    for a, b in reversed(spans):
        s = s[:a] + "(masked: 12 or more short words, possible recovery phrase)" + s[b:]
    return s


def mask(s):
    """Hide secret shapes: long hex (a private key has the same shape as an asset id), common
    token prefixes, JWTs, long mixed tokens and runs of short words that could be a phrase."""
    s = LONG_HEX.sub(lambda m: m.group(0)[:6] + "...(masked)", s)
    for rx in SECRET_SHAPES:
        s = rx.sub(lambda m: m.group(0)[:4] + "...(masked)", s)
    return _mask_phrases(s)


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


def classify(sentence):
    kinds = set()
    if LIVE.search(sentence):
        kinds.add("live")
    if PROMISE.search(sentence):
        kinds.add("promise")
    if COMPARISON.search(sentence):
        kinds.add("comparison")
    if UNIVERSAL.search(sentence):
        kinds.add("universal")
    if ATTRIBUTION.search(sentence):
        kinds.add("attribution")
    if VERSION.search(sentence):
        kinds.add("version")
    if DATE.search(sentence):
        kinds.add("date")
    if NUMBER.search(sentence):
        kinds.add("number")
    if BEHAVIOR.search(sentence):
        kinds.add("behavior")
    if NAMES.search(sentence):
        kinds.add("name")
    return [k for k in PRIORITY if k in kinds]


# ---------------------------------------------------------------- sentences
ABBREV = {"e.g", "i.e", "vs", "etc", "approx", "fig", "mr", "mrs", "dr", "st", "inc", "ltd", "cf",
          "al", "ca"}
TERMINATOR = re.compile(r"[.!?][\"')\]*_`]*\s+")


def split_sentences(text):
    """Return [(sentence, start offset)] for a block of running text."""
    out, start, n = [], 0, len(text)
    for m in TERMINATOR.finditer(text):
        end = m.end()
        if end >= n:
            continue
        nxt = text[end]
        if not (nxt.isalnum() or nxt in "\"'\u201c([*`_<"):
            continue
        before = text[start:m.start() + 1].rstrip(".!?\"')]*_`")
        words = before.split()
        last = words[-1].lower() if words else ""
        if last in ABBREV or re.fullmatch(r"[a-z]", last):
            continue
        out.append((text[start:end].strip(), start))
        start = end
    tail = text[start:].strip()
    if tail:
        out.append((tail, start))
    merged = []   # keep a bare "No." or "Yes." with the sentence that explains it
    for sent, so in out:
        if merged and re.fullmatch(r"(?:yes|no)[.!]", merged[-1][0], re.I):
            merged[-1] = (merged[-1][0] + " " + sent, merged[-1][1])
        else:
            merged.append((sent, so))
    return merged


def clean_md(s):
    s = re.sub(r"<!--.*?-->", "", s)
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\[[^\]]*\]", r"\1", s)
    s = re.sub(r"<(?:https?://[^>]+)>", lambda m: m.group(0)[1:-1], s)
    s = re.sub(r"</?[A-Za-z][^>]*>", "", s)
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = re.sub(r"\*\*|__|~~", "", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)([^*]+?)\*(?![\w*])", r"\1", s)
    s = re.sub(r"(?<!\w)_(?!\s)([^_]+?)_(?!\w)", r"\1", s)
    s = re.sub(r"\{#[^}]+\}", "", s)
    return " ".join(s.split())


# ---------------------------------------------------------------- markdown and text
FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})\s*([\w+-]*)")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.*?)\s*#*\s*$")
HRULE = re.compile(r"^\s{0,3}(?:-{3,}|\*{3,}|_{3,})\s*$")
LISTITEM = re.compile(r"^(\s*)(?:[-*+]|\d+[.)])\s+(.*)$")
TABLE_SEP = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")
FM_KEYS = {"title", "summary", "description", "takeaways", "faq"}


def _unquote(v):
    v = v.strip()
    m = re.match(r'^"((?:[^"\\]|\\.)*)"\s*(?:#.*)?$', v) or re.match(r"^'((?:[^']|'')*)'\s*(?:#.*)?$", v)
    if m:
        return m.group(1).replace('\\"', '"').replace("''", "'")
    return re.sub(r"\s+#\s.*$", "", v)


def frontmatter_units(lines, start, end):
    out, key = [], None
    for k in range(start, end):
        raw = lines[k]
        if not raw.strip():
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", raw)
        if m and not raw.startswith((" ", "\t", "-")):
            key = m.group(1).lower()
            val = m.group(2).strip()
            if key in FM_KEYS and val and val not in ("|", ">", "|-", ">-", "[]"):
                out.append((_unquote(val), k + 1))
            continue
        if key in FM_KEYS:
            s = re.sub(r"^-\s*", "", raw.strip())
            s = re.sub(r"^(?:q|a|question|answer):\s*", "", s)
            if s:
                out.append((_unquote(s), k + 1))
    return out


def md_units(text):
    """Return [(text, lineno, kind)] where kind is 'text' or 'code'."""
    lines = text.split("\n")
    n, i, units = len(lines), 0, []
    if n and lines[0].strip() == "---":
        j = 1
        while j < n and lines[j].strip() not in ("---", "..."):
            j += 1
        if j < n:
            for t, ln in frontmatter_units(lines, 1, j):
                units.extend((s, ln, "text") for s, _ in split_sentences(clean_md(t)))
            i = j + 1
    para = []   # [(lineno, raw text)]

    def flush():
        if not para:
            return
        joined, starts, off = "", [], 0
        for ln, t in para:
            if joined:
                joined += " "
                off += 1
            starts.append((off, ln))
            joined += t
            off += len(t)
        offs = [o for o, _ in starts]
        for sent, so in split_sentences(joined):
            ln = starts[max(0, bisect.bisect_right(offs, so) - 1)][1]
            units.append((clean_md(sent), ln, "text"))
        del para[:]

    while i < n:
        line = lines[i]
        s = line.strip()
        fm = FENCE.match(line)
        if fm:
            flush()
            marker, lang, first, count, j = fm.group(2), fm.group(3), "", 0, i + 1
            while j < n and not (lines[j].strip().startswith(marker[0] * len(marker))
                                 and not lines[j].strip().strip(marker[0])):
                if lines[j].strip() and not first:
                    first = lines[j].strip()
                count += 1
                j += 1
            label = "code block (%s%d lines): %s" % ((lang + ", ") if lang else "", count, first)
            units.append((" ".join(label.split()), i + 1, "code"))
            i = j + 1
            continue
        if s.startswith("<!--"):
            flush()
            while i < n and "-->" not in lines[i]:
                i += 1
            i += 1
            continue
        if not s:
            flush()
        elif HEADING.match(line):
            flush()
            units.append((clean_md(HEADING.match(line).group(1)), i + 1, "text"))
        elif HRULE.match(line):
            flush()
        elif s.startswith("|"):
            flush()
            if not TABLE_SEP.match(s):
                cells = [clean_md(c) for c in s.strip("|").split("|")]
                units.append((" | ".join(c for c in cells if c), i + 1, "text"))
        else:
            lm = LISTITEM.match(line)
            if lm:
                flush()
                para.append((i + 1, lm.group(2)))
            else:
                bq = re.match(r"^\s*>\s?(.*)$", line)
                para.append((i + 1, bq.group(1) if bq else s))
        i += 1
    flush()
    return units


# ---------------------------------------------------------------- HTML
VOID = {"meta", "link", "br", "img", "input", "hr", "source", "use", "path", "stop", "circle",
        "rect", "area", "base", "col", "embed", "wbr"}
SKIP_TAGS = {"style", "script", "svg", "title", "head", "noscript", "template"}
SKIP_CLASSES = {"slide-num", "ghost-num", "ph"}
BLOCK = {"p", "div", "li", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "td", "th",
         "section", "article", "header", "footer", "blockquote", "br", "table", "figure",
         "figcaption", "dl", "dt", "dd", "pre", "main", "aside", "nav", "summary", "details",
         "body", "hr"}


class HtmlText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.skip, self.slide = [], 0, 0
        self.pieces = []       # [(offset, lineno)] for the current block
        self.buf = ""
        self.units = []        # [(text, lineno, slide)]
        self.block_slide = 0

    def _flush(self):
        if self.buf.strip():
            offs = [o for o, _ in self.pieces]
            for sent, so in split_sentences(self.buf):
                ln = self.pieces[max(0, bisect.bisect_right(offs, so) - 1)][1]
                t = " ".join(sent.split())
                if t:
                    self.units.append((t, ln, self.block_slide))
        self.buf, self.pieces = "", []

    def handle_starttag(self, tag, attrs):
        classes = set((dict(attrs).get("class") or "").split())
        if tag in BLOCK:
            self._flush()
        if tag == "section" and "slide" in classes:
            self.slide += 1
        self.block_slide = self.slide
        if tag in VOID:
            return
        starts = tag in SKIP_TAGS or bool(classes & SKIP_CLASSES)
        if starts:
            self.skip += 1
        self.stack.append((tag, starts))

    def handle_startendtag(self, tag, attrs):
        if tag in BLOCK:
            self._flush()

    def handle_endtag(self, tag):
        if tag in BLOCK:
            self._flush()
        if tag in VOID:
            return
        for k in range(len(self.stack) - 1, -1, -1):
            if self.stack[k][0] == tag:
                for _, started in self.stack[k:]:
                    if started:
                        self.skip -= 1
                del self.stack[k:]
                break

    def handle_data(self, data):
        if self.skip or not data.strip():
            return
        piece = " ".join(data.split())
        if self.buf and not re.match(r"[.,;:!?)\]]", piece):
            self.buf += " "
        self.pieces.append((len(self.buf), self.getpos()[0]))
        self.buf += piece
        self.block_slide = self.slide


ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f", "v": "\v", "0": "\0"}


def _read_string(js, i):
    q, j, n, buf = js[i], i + 1, len(js), []
    while j < n:
        ch = js[j]
        if ch == "\\" and j + 1 < n:
            nx = js[j + 1]
            if nx in ESCAPES:
                buf.append(ESCAPES[nx])
                j += 2
            elif nx == "\n":
                j += 2
            else:
                buf.append(nx)
                j += 2
        elif ch == q:
            return "".join(buf), j + 1
        else:
            buf.append(ch)
            j += 1
    return "".join(buf), n


def notes_entries(html):
    """[(text, offset of the string)] for the NOTES array, or []."""
    m = re.search(r"\b(?:var|let|const)\s+NOTES\s*=\s*\[", html)
    if not m:
        return []
    i, n, notes, cur, cur_at = m.end(), len(html), [], None, 0
    while i < n:
        c = html[i]
        if c.isspace() or c == "+":
            i += 1
        elif html.startswith("//", i):
            j = html.find("\n", i)
            i = n if j < 0 else j
        elif html.startswith("/*", i):
            j = html.find("*/", i + 2)
            i = n if j < 0 else j + 2
        elif c in "\"'`":
            at = i
            s, i = _read_string(html, i)
            if cur is None:
                cur_at = at
            cur = (cur or "") + s
        elif c == ",":
            if cur is not None:
                notes.append((cur, cur_at))
            cur = None
            i += 1
        elif c == "]":
            break
        else:
            i += 1
    if cur is not None:
        notes.append((cur, cur_at))
    return notes


NO_NOTES = []   # paths of HTML files in which no NOTES array was found


def html_units(html, path=""):
    p = HtmlText()
    p.feed(html)
    p._flush()
    units = [(t, ln, "text", "slide %d" % sl if sl else "") for t, ln, sl in p.units]
    entries = notes_entries(html)
    if not entries:
        NO_NOTES.append(path)
    for k, (txt, at) in enumerate(entries, 1):
        ln = html.count("\n", 0, at) + 1
        for sent, _ in split_sentences(" ".join(txt.split())):
            units.append((sent, ln, "text", "notes, slide %d" % k))
    return units


# ---------------------------------------------------------------- main
def read_units(path):
    with open(path, encoding="utf-8-sig") as fh:
        text = fh.read().replace("\r\n", "\n")
    head = text.lstrip()[:200].lower()
    is_html = path.lower().endswith((".html", ".htm")) or head.startswith(("<!doctype html", "<html"))
    if is_html:
        return html_units(text, path)
    return [(t, ln, kind, "") for t, ln, kind in md_units(text)]


def norm(s):
    return " ".join(re.sub(r"[^a-z0-9]+", " ", mask(s).lower()).split())


def read_ledger(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        header = [h.strip() for h in (reader.fieldnames or [])]
        if "claim" not in header or "id" not in header:
            raise ValueError("the ledger needs the columns id and claim")
        rows = []
        for r in reader:
            if None in r:
                raise ValueError("ledger line %d has more cells than the header" % reader.line_num)
            r = {(k or "").strip(): (v or "").strip() for k, v in r.items()}
            if any(r.values()) and not r["id"].startswith("#"):
                rows.append(r)
    return rows


def _start(v):
    n = int(v)
    if n < 0:
        raise argparse.ArgumentTypeError("must be 0 or more")
    return n


def _prefix(v):
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", v):
        raise argparse.ArgumentTypeError("must be letters, then letters or digits (a # starts a comment row)")
    return v


def main():
    ap = argparse.ArgumentParser(
        description="Print candidate claims as claim-ledger rows. Flags sentences by trigger words: "
                    "it over-collects on purpose and can miss a plain statement (use --all).",
        epilog="Exit 0 done, 1 with --against and something to do, 2 bad input.")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--all", action="store_true",
                    help="also list sentences that matched no trigger word (empty type)")
    ap.add_argument("--against", metavar="LEDGER")
    ap.add_argument("--dropped", metavar="CANDIDATES",
                    help="with --against: raw extractor output; its sentences missing from the ledger "
                         "were dropped on purpose and count as covered")
    ap.add_argument("--start", type=_start, default=None)
    ap.add_argument("--prefix", type=_prefix, default="C")
    args = ap.parse_args()

    if args.dropped and not args.against:
        ap.error("--dropped needs --against")
    for path in args.files + [x for x in (args.against, args.dropped) if x]:
        if is_env_file(path):
            print("extract-claims: refusing to read %s: an env file can hold keys and is never opened. "
                  "Pass the text file instead." % os.path.basename(path), file=sys.stderr)
            return 2

    ledger, covered, cut_rows, id_source, n_dropped = [], set(), [], [], 0
    if args.against:
        try:
            ledger = read_ledger(args.against)
        except (OSError, UnicodeDecodeError, csv.Error, ValueError) as e:
            print("extract-claims: cannot read the ledger: %s" % e, file=sys.stderr)
            return 2
        covered = {norm(r["claim"]) for r in ledger}
        cut_rows = [r for r in ledger if r.get("verdict", "").lower() == "cut"]
        if args.dropped:
            try:
                dropped_rows = read_ledger(args.dropped)
            except (OSError, UnicodeDecodeError, csv.Error, ValueError) as e:
                print("extract-claims: cannot read the dropped file: %s" % e, file=sys.stderr)
                return 2
            n_dropped = sum(1 for r in dropped_rows if norm(r["claim"]) not in covered)
            covered |= {norm(r["claim"]) for r in dropped_rows}
            id_source = ledger + dropped_rows
        else:
            n_dropped, id_source = 0, ledger

    found, sentences, unflagged, seen_norm = [], 0, 0, set()
    for path in args.files:
        try:
            units = read_units(path)
        except (OSError, UnicodeDecodeError) as e:
            print("extract-claims: cannot read %s: %s" % (path, e), file=sys.stderr)
            return 2
        for item in units:
            text, ln, kind = item[0], item[1], item[2]
            ctx = item[3] if len(item) > 3 else ""
            sentences += 1
            if not text.strip():
                continue   # a bare HTML comment or marker left nothing to check
            n = norm(text)
            seen_norm.add(n)
            kinds = ["code"] if kind == "code" else classify(text)
            if not kinds:
                unflagged += 1
                if not args.all:
                    continue
            where = "%s:%d" % (path, ln) + (" (%s)" % ctx if ctx else "")
            found.append((mask(text), where, ";".join(kinds), n))
    for path in NO_NOTES:
        print("extract-claims: NOTE: no NOTES array found in %s. If it is a deck, its presenter notes "
              "were NOT read: pass the notes file as well." % path, file=sys.stderr)

    next_n = args.start
    if next_n is None:
        top = 0
        for r in id_source:
            m = re.search(r"(\d+)$", r.get("id", ""))
            if m:
                top = max(top, int(m.group(1)))
        next_n = top + 1
    rows = [f for f in found if not args.against or f[3] not in covered]
    width = max(3, len(str(next_n + len(rows))))
    out = csv.writer(sys.stdout, lineterminator="\n")
    out.writerow(COLUMNS)
    for k, (claim, where, kinds, _) in enumerate(rows):
        out.writerow([args.prefix + str(next_n + k).zfill(width), claim, where, kinds, "",
                      "unverified", "", "", ""])

    left = [r for r in cut_rows if norm(r["claim"]) in seen_norm]
    if args.against:
        print("extract-claims: %d candidate sentence(s) not in the ledger %s" % (len(rows), args.against),
              file=sys.stderr)
        if args.dropped:
            print("extract-claims: %d sentence(s) counted as dropped on purpose (in %s, not in the ledger)" %
                  (n_dropped, args.dropped), file=sys.stderr)
        if unflagged and not args.all:
            print("extract-claims: %d sentence(s) matched no trigger word and were not checked against the "
                  "ledger. Use --all to include them." % unflagged, file=sys.stderr)
        print("extract-claims: CUT BUT STILL IN THE TEXT (%d)" % len(left), file=sys.stderr)
        for r in left:
            print("  %s | %s" % (r["id"], mask(r["claim"])[:110]), file=sys.stderr)
        return 1 if (rows or left) else 0
    print("extract-claims: %d candidate claim(s) from %d file(s), %d sentence(s) read. %s Read each row "
          "before deleting it. Every row is unverified." %
          (len(rows), len(args.files), sentences,
           ("--all: every sentence is listed." if args.all else
            "%d sentence(s) matched no trigger word and are not listed (use --all, and read the text "
            "yourself for plain statements)." % unflagged)), file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)   # a closed pipe such as | head ends quietly
    except (AttributeError, ValueError):
        pass
    sys.exit(main())
