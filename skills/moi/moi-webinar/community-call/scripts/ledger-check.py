#!/usr/bin/env python3
"""Compare the figures printed on a deck's slides with a numbers ledger.

Usage (run from the working copy that holds the call folder, SKILLS set to the
folder that holds the moi-* skills):
    python3 "$SKILLS/moi-webinar/community-call/scripts/ledger-check.py" \
        community-call-<N>/deck/index.html community-call-<N>/numbers-ledger.csv [--notes]

What it reads (read-only, it never writes a file):
    deck.html   the visible text of every <section class="slide">. Slide badges
                (.slide-num), the ghost numeral (.ghost-num), photo filename
                frames (.ph), <style>, <script>, <svg> and <title> are ignored.
    ledger.csv  header: slide,figure,value,source,as_of,confirmed_by,status
                (extra columns are allowed, order does not matter; a UTF-8 byte
                order mark is accepted). Quote any cell that contains a comma.

What counts as a figure: any token with a digit that is not inside a word
(so x402 and MAS0 are ignored): numbers (17.3%, 1,203, 120+, #14), versions
(0.13.0, 0.9.0-rc2), hex ids (0x1080...), and the words thousand, million,
billion, trillion. Other spelled-out numbers ("seventh", "fifty") are NOT
detected: add those rows by hand.

Status words:
    confirmed             good. Needs source, as_of and confirmed_by.
    accepted-unverified   the human decided to keep a figure nobody verified. Needs
                          confirmed_by to read "accepted by <name> on <YYYY-MM-DD>:
                          <reason>" (who and when). A WARN, not a FAIL.
    superseded, dropped   retire a figure.
    anything else         (unverified, pending, empty) is "not confirmed", a FAIL.

Matching: a figure on a slide is covered when its token appears in the figure or
value cell of any non-retired ledger row. Write the value the way the slide
prints it ("17.3%", not "17.3 percent"). With --notes the NOTES array in the
deck's script is checked too, ignoring % and + so "17.3 percent" matches "17.3%".
NOTES strings may use double, single or backtick quotes.

FAIL lists (any entry gives exit 1):
    1. figures on slides with no ledger row
    2. ledger rows whose status is not confirmed (the reason belongs in confirmed_by)
    3. retired figures that are still on a slide
    4. confirmed rows with no source, as_of or confirmed_by; accepted-unverified
       rows with no who and when
WARN list (does not change the exit code):
    5. rows accepted without verification. Name each one in the hand-back.

Long hex ids (more than 18 characters) are masked in everything printed.
An env file (.env, .env.*, *.env, .envrc) is refused and never opened.

Exit codes: 0 no FAIL list has an entry (list 5 may); 1 a FAIL list has an
entry; 2 bad input (unreadable file, an env file, bad header, a row with more
cells than the header, no slides, or --notes without readable NOTES entries).
"""
import argparse
import os
import csv
import re
import sys
from html.parser import HTMLParser

REQUIRED = ["slide", "figure", "value", "source", "as_of", "confirmed_by", "status"]
RETIRED = {"superseded", "dropped"}
ACCEPTED = "accepted-unverified"
VOID = {"meta", "link", "br", "img", "input", "hr", "source", "use", "path",
        "stop", "circle", "rect", "area", "base", "col", "embed", "wbr"}
SKIP_TAGS = {"style", "script", "svg", "title"}
SKIP_CLASSES = {"slide-num", "ghost-num", "ph"}

TOKEN = re.compile(
    r"(?<![A-Za-z0-9_])(?:"
    r"0x[0-9A-Fa-f]+"
    r"|v?\d+(?:\.\d+){2,}(?:-[A-Za-z0-9.]+)?"
    r"|\#?\d+(?:,\d{3})*(?:\.\d+)?[%+]?"
    r"|(?:thousand|million|billion|trillion)(?![A-Za-z])"
    r")",
    re.IGNORECASE,
)
LONG_HEX = re.compile(r"0x[0-9A-Fa-f]{17,}|[0-9A-Fa-f]{24,}")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def mask(s):
    """Hide long hex strings so a pasted key is never echoed."""
    return LONG_HEX.sub(lambda m: m.group(0)[:6] + "...(masked)", s)


def show(s=""):
    print(mask(s))


def status_of(r):
    return r["status"].strip().lower().replace("_", "-").replace(" ", "-")


def accepted_ok(r):
    """An accepted-unverified row reads "accepted by <name> on <YYYY-MM-DD>: <reason>"."""
    who_when = r["confirmed_by"]
    return bool(re.search(r"accepted\s+by\s+[A-Za-z]", who_when, re.I) and DATE.search(who_when))


class SlideText(HTMLParser):
    """Collect the visible text of each <section class="slide">, in order."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []        # (tag, skipping_started_here)
        self.skip = 0
        self.slides = []       # list of lists of text chunks
        self.cur = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = set((a.get("class") or "").split())
        if tag == "section" and "slide" in classes:
            self.slides.append([])
            self.cur = self.slides[-1]
        if tag in VOID:
            return
        starts_skip = tag in SKIP_TAGS or bool(classes & SKIP_CLASSES)
        if starts_skip:
            self.skip += 1
        self.stack.append((tag, starts_skip))

    def handle_startendtag(self, tag, attrs):
        # self-closing form such as <svg ... /> or <div/>: nothing to push
        if tag == "section":
            self.handle_starttag(tag, attrs)
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        for k in range(len(self.stack) - 1, -1, -1):
            if self.stack[k][0] == tag:
                for _, started in self.stack[k:]:
                    if started:
                        self.skip -= 1
                del self.stack[k:]
                break
        if tag == "section":
            self.cur = None

    def handle_data(self, data):
        if self.cur is not None and self.skip == 0:
            self.cur.append(data)


def norm(tok, loose=False):
    t = tok.lower().replace(",", "").lstrip("#")
    if re.match(r"^v\d", t):
        t = t[1:]
    if loose:
        t = t.rstrip("%+")
    return t


def figures(text, loose=False):
    """Return a list of (normalised token, raw token, context)."""
    out = []
    for m in TOKEN.finditer(text):
        raw = m.group(0)
        a, b = max(0, m.start() - 28), min(len(text), m.end() + 28)
        ctx = " ".join(text[a:b].split())
        out.append((norm(raw, loose), raw, ctx))
    return out


ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f", "v": "\v", "0": "\0"}


def read_string(js, i):
    """Read a JavaScript string literal that starts at js[i] (a quote). Return (text, next index)."""
    q, j, n, buf = js[i], i + 1, len(js), []
    while j < n:
        ch = js[j]
        if ch == "\\" and j + 1 < n:
            nx = js[j + 1]
            if nx in ESCAPES:
                buf.append(ESCAPES[nx]); j += 2
            elif nx == "x" and re.match(r"[0-9a-fA-F]{2}", js[j + 2:j + 4]):
                buf.append(chr(int(js[j + 2:j + 4], 16))); j += 4
            elif nx == "u":
                m = re.match(r"\{([0-9a-fA-F]+)\}|([0-9a-fA-F]{4})", js[j + 2:])
                if m:
                    buf.append(chr(int(m.group(1) or m.group(2), 16))); j += 2 + m.end()
                else:
                    buf.append("u"); j += 2
            elif nx == "\n":
                j += 2
            else:
                buf.append(nx); j += 2
        elif ch == q:
            return "".join(buf), j + 1
        else:
            buf.append(ch); j += 1
    return "".join(buf), n


def read_notes(html):
    """The entries of the NOTES array (any quote style), or None when there is no such array."""
    m = re.search(r"\b(?:var|let|const)\s+NOTES\s*=\s*\[", html)
    if not m:
        return None
    i, n = m.end(), len(html)
    notes, cur = [], None
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
            s, i = read_string(html, i)
            cur = (cur or "") + s
        elif c == ",":
            if cur is not None:
                notes.append(cur)
            cur = None
            i += 1
        elif c == "]":
            break
        else:
            i += 1
    if cur is not None:
        notes.append(cur)
    return notes


def slide_numbers(cell):
    return {int(n) for n in re.findall(r"\d+", cell or "")}


def is_env_file(path):
    """An env-named file is never opened: .env, .envrc, .env.*, *.env, anything holding .env."""
    names = [os.path.basename(str(path))]
    try:
        names.append(os.path.basename(os.path.realpath(str(path))))
    except OSError:
        pass
    for n in names:
        low = n.lower()
        if low in (".env", ".envrc") or low.startswith(".env.") or low.endswith(".env") or ".env." in low:
            return True
    return False


def main():
    ap = argparse.ArgumentParser(
        description="Compare slide figures with a numbers ledger.",
        epilog="Exit 0 no FAIL, 1 findings, 2 bad input.")
    ap.add_argument("deck")
    ap.add_argument("ledger")
    ap.add_argument("--notes", action="store_true",
                    help="also check the figures in the NOTES array")
    args = ap.parse_args()

    for named in (args.deck, args.ledger):
        if is_env_file(named):
            print("ledger-check: refusing to read %s: an env file can hold keys and is never opened. "
                  "Pass the deck and the ledger instead." % os.path.basename(named), file=sys.stderr)
            return 2
    try:
        html = open(args.deck, encoding="utf-8-sig").read()
    except (OSError, UnicodeDecodeError) as e:
        print(f"ledger-check: cannot read deck: {e}", file=sys.stderr)
        return 2
    try:
        with open(args.ledger, encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            header = [h.strip() for h in (reader.fieldnames or [])]
            missing = [c for c in REQUIRED if c not in header]
            if missing:
                print("ledger-check: ledger is missing column(s): " + ", ".join(missing)
                      + "\n  expected header: " + ",".join(REQUIRED), file=sys.stderr)
                return 2
            rows = []
            for r in reader:
                if None in r:
                    print(f"ledger-check: ledger line {reader.line_num} has more cells than the "
                          "header; quote any cell that contains a comma", file=sys.stderr)
                    return 2
                r = {(k or "").strip(): (v or "").strip() for k, v in r.items()}
                if not any(r.values()) or r["slide"].startswith("#"):
                    continue
                rows.append(r)
    except (OSError, csv.Error, UnicodeDecodeError) as e:
        print(f"ledger-check: cannot read ledger: {e}", file=sys.stderr)
        return 2

    p = SlideText()
    p.feed(html)
    slides = [" ".join(chunks) for chunks in p.slides]
    if not slides:
        print("ledger-check: no <section class=\"slide\"> found in the deck", file=sys.stderr)
        return 2

    live_rows = [r for r in rows if status_of(r) not in RETIRED]
    retired_rows = [r for r in rows if status_of(r) in RETIRED]

    def row_tokens(r, loose=False):
        return {t for t, _, _ in figures(r["figure"] + " " + r["value"], loose)}

    covered, covered_loose = set(), set()
    token_slides = {}
    for r in live_rows:
        covered |= row_tokens(r)
        covered_loose |= row_tokens(r, True)
        for t in row_tokens(r):
            token_slides.setdefault(t, set()).update(slide_numbers(r["slide"]))
    retired_only = set()
    for r in retired_rows:
        retired_only |= row_tokens(r)
    retired_only -= covered

    missing_figs, retired_hits, wrong_slide = [], [], []
    for n, text in enumerate(slides, 1):
        seen = set()
        for tok, raw, ctx in figures(text):
            if tok in seen:
                continue
            seen.add(tok)
            if tok in covered:
                rs = token_slides.get(tok, set())
                if rs and n not in rs and "all" not in {r["slide"].lower() for r in live_rows}:
                    wrong_slide.append((n, raw, sorted(rs)))
            elif tok in retired_only:
                retired_hits.append((n, raw, ctx))
            else:
                missing_figs.append((n, raw, ctx))

    notes_checked = False
    if args.notes:
        notes = read_notes(html)
        if notes is None:
            print("ledger-check: --notes given but no NOTES array found; the notes were NOT checked",
                  file=sys.stderr)
            return 2
        if not notes:
            print("ledger-check: --notes given but the NOTES array has no entries this script can "
                  "read; the notes were NOT checked", file=sys.stderr)
            return 2
        if len(notes) != len(slides):
            print("ledger-check: NOTES has %d entries for %d slides, so the notes cannot be matched "
                  "to slides; fix the deck (check e of check-deck.py) and run again"
                  % (len(notes), len(slides)), file=sys.stderr)
            return 2
        notes_checked = True
        retired_loose = {norm(x, True) for x in retired_only}
        for n, text in enumerate(notes, 1):
            seen = set()
            for tok, raw, ctx in figures(text, True):
                if tok in seen:
                    continue
                seen.add(tok)
                if tok in covered_loose:
                    continue
                if tok in retired_loose:
                    retired_hits.append((n, raw + " (in notes)", ctx))
                else:
                    missing_figs.append((n, raw + " (in notes)", ctx))

    not_confirmed = [r for r in live_rows if status_of(r) not in ("confirmed", ACCEPTED)]
    incomplete = [r for r in live_rows if status_of(r) == "confirmed"
                  and not (r["source"] and r["as_of"] and r["confirmed_by"])]
    incomplete += [r for r in live_rows if status_of(r) == ACCEPTED and not accepted_ok(r)]
    accepted = [r for r in live_rows if status_of(r) == ACCEPTED and accepted_ok(r)]

    show(f"ledger-check: {args.deck} against {args.ledger}")
    show(f"slides scanned: {len(slides)}   ledger rows: {len(rows)}"
         f" ({len(retired_rows)} retired)   notes checked: {'yes' if notes_checked else 'no'}\n")

    def section(title, items, fmt):
        show(f"{title} ({len(items)})")
        for it in items:
            show("  " + fmt(it))
        if not items:
            show("  none")
        show()

    section("1. FIGURES ON SLIDES WITH NO LEDGER ROW", missing_figs,
            lambda x: f"slide {x[0]}: {x[1]}    ...{x[2]}...")
    section("2. LEDGER ROWS NOT CONFIRMED", not_confirmed,
            lambda r: f"slide {r['slide']} | {r['figure']} = {r['value']} | status={r['status'] or '(empty)'}"
                      f" | {r['confirmed_by'] or 'no reason given'}")
    section("3. RETIRED FIGURES STILL ON A SLIDE", retired_hits,
            lambda x: f"slide {x[0]}: {x[1]}    ...{x[2]}...")
    section("4. ROWS WITH MISSING FIELDS (confirmed needs source, as_of, confirmed_by;"
            " accepted-unverified needs who and when in confirmed_by)", incomplete,
            lambda r: f"slide {r['slide']} | {r['figure']} = {r['value']} | status={r['status']}")
    section("5. WARN: ACCEPTED WITHOUT VERIFICATION (name each one in the hand-back)", accepted,
            lambda r: f"slide {r['slide']} | {r['figure']} = {r['value']} | {r['confirmed_by']}")
    if wrong_slide:
        show(f"warning: the ledger names a different slide for {len(wrong_slide)} figure(s):")
        for n, raw, rs in wrong_slide:
            show(f"  {raw} is on slide {n}, ledger says slide {', '.join(map(str, rs))}")
        show()

    bad = missing_figs or not_confirmed or retired_hits or incomplete
    if bad:
        show("RESULT: FAIL, resolve every FAIL list above before the call (exit 1)")
    elif accepted:
        show(f"RESULT: PASS WITH WARNINGS, every figure is in the ledger; {len(accepted)} accepted "
             "without verification and must be named in the hand-back (exit 0)")
    else:
        show("RESULT: PASS, every figure is in the ledger and confirmed (exit 0)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
