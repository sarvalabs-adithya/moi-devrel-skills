#!/usr/bin/env python3
"""check-deck.py: check a MOI deck for the faults a PDF hides.

Usage:   check-deck.py <deck.html> [--script SCRIPT.md] [--stale PHRASE]...
                       [--skip LETTERS] [--require-node] [--quiet]
                       [--layout [--chrome PATH]]
Output:  one line per check: PASS, WARN, FAIL or SKIPPED, then indented detail.
Exit:    0 when nothing FAILed (WARN and SKIPPED do not fail), 1 on any FAIL (checked and failed),
         2 when the file cannot be read, is an env file (.env, .env.*, *.env: refused, never opened)
         or the arguments are wrong.
Needs:   python3, standard library only. node is used for check a when present.
         --layout also needs Chrome or Chromium ($CHROME, or the usual install paths;
         $CHROME_FLAGS adds flags, for example --no-sandbox in a container).
Writes:  nothing beside the deck. It makes one temporary file for node --check and one for the
         layout page, both deleted afterwards. With --layout, Chrome writes its own state under
         the user's profile folders (on macOS ~/Library/Application Support/Google/).

Checks (letters are stable, other docs refer to them):
  a  the inline script parses (node --check)
  b  every slide is a direct child of the stage; every badge is inside its slide
  c  badge equals page number; cover and close carry none
  d  no two neighbouring slides share a background
  e  TITLES and NOTES have exactly one entry per slide
  f  retired phrases: FAIL for wording that is wrong everywhere ("Voyage devnet", "account-centric",
     "12:00 AM UTC"), WARN with the reason for wording removed from one deck ("Open Q&A",
     "Building in Public"); presenter window title matches the document title
  g  no em dash in slide text, notes or titles
  h  with --script: each NOTES entry equals its section of SCRIPT.md
  i  relative time words that go stale (WARN)
  j  files the slides point at exist (WARN)
  k  README.md slide count matches the deck (WARN)
  l  variant HTML files beside the deck that have become identical (WARN)
  m  placeholder markers left in the deck (WARN)
  n  "not X, not Y" style contrasts (WARN, a heuristic: check by ear)
  o  with --layout: no slide content runs off the 1920x1080 slide (measured in Chrome)
"""
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from urllib.parse import unquote

EM_DASH = chr(0x2014)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}
BLOCK = {"div", "section", "p", "li", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6", "table", "tr",
         "td", "th", "br", "blockquote", "figure", "figcaption", "nav", "svg"}
STRUCTURAL = {"div", "section", "nav", "main", "header", "footer", "article", "aside", "table"}
# Wrong everywhere (founder and previous-operator corrections): FAIL.
RETIRED = ["Voyage devnet", "account-centric", "12:00 AM UTC"]
# Removed from one deck or one series, so another deck may still want it: WARN, with the reason.
RETIRED_SOFT = [
    ("Open Q&A", "removed from the community call 14 close, 2026-09-24/25; fine if this deck wants a Q&A slide"),
    ("Building in Public", "retired as the community call name when call 14 became The Campfire Chat, 2026-09-24/25; "
                           "fine in a deck for another series"),
]
WEEKDAYS = "monday|tuesday|wednesday|thursday|friday|saturday|sunday"
RELATIVE = re.compile(
    r"\b(?:yesterday|tomorrow|tonight"
    r"|(?:this|last|next)\s+(?:week|weekend|month|quarter|year)"
    r"|(?:last|this|next)\s+(?:%s)"
    r"|since\s+(?:the\s+)?last\s+(?:call|session|time|month|week)"
    r"|recently|right now|these days|at the moment)\b" % WEEKDAYS, re.I)
PLACEHOLDER = re.compile(r"\bTODO\b|\bFIXME\b|<<<|REPLACE-WITH|lorem ipsum", re.I)
CONTRASTS = [
    (re.compile(r"\bnot\s+[^.;:!?\n]{1,50}?,\s+not\b", re.I), "'not X, not Y'"),
    (re.compile(r"\b(?:it|this|that)(?:'s|’s|\s+is)\s+not\s+[^.;:!?\n]{1,70}[.;,]\s+"
                r"(?:it|this|that)(?:'s|’s|\s+is)\b", re.I), "'It's not X. It's Y'"),
    (re.compile(r"\bnot\s+(?:about|just|only|merely)\s+[^.;:!?\n]{1,50}[,.;]\s+"
                r"(?:it's|it’s|it is|but|this is|that's)\b", re.I), "'not about X, it's Y'"),
]


def norm(s):
    return " ".join(s.replace(chr(0xa0), " ").split())


def desc(el):
    d = el["tag"]
    if el["attrs"].get("id"):
        d += "#" + el["attrs"]["id"]
    for c in el["classes"][:3]:
        d += "." + c
    return d


class DeckParser(HTMLParser):
    """Tracks the open-element stack the way a browser does, so a stray </div>
    moves things in this model exactly as it does in Chrome."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.slides = []
        self.badges = []
        self.scripts = []
        self.images = []
        self.title = None
        self.implicit = []   # (line, end tag, [closed elements])
        self.stray = []      # (line, end tag)
        self._script = None
        self._title = False
        self._chunks = []    # text before any slide (ignored)

    # helpers
    def _in(self, tag):
        return any(e["tag"] == tag for e in self.stack)

    def _slide(self):
        for e in reversed(self.stack):
            if e.get("slide") is not None:
                return e["slide"]
        return None

    def _open(self, tag, attrs, selfclose):
        a = {k: (v if v is not None else "") for k, v in attrs}
        classes = a.get("class", "").split()
        line = self.getpos()[0]
        el = {"tag": tag, "attrs": a, "classes": classes, "line": line}
        parent = self.stack[-1] if self.stack else None
        if tag == "section" and "slide" in classes:
            s = {"index": len(self.slides) + 1, "classes": classes, "line": line,
                 "parent": desc(parent) if parent else "(none)",
                 "parent_is_stage": bool(parent) and (parent["attrs"].get("id") in ("stage", "deck-stage")
                                                       or "deck-stage" in parent["classes"]),
                 "text": [], "badges": []}
            self.slides.append(s)
            el["slide"] = s
        if "slide-num" in classes:
            b = {"line": line, "text": [], "slide": self._slide(),
                 "parent": desc(parent) if parent else "(none)"}
            self.badges.append(b)
            if b["slide"] is not None:
                b["slide"]["badges"].append(b)
            el["badge"] = b
        cur0 = self._slide()
        if cur0 is not None and tag in BLOCK:
            cur0["text"].append("\n")
        if tag == "img" and a.get("src"):
            self.images.append((a["src"], self._slide(), line))
        cur = self._slide()
        if cur is not None:
            for key in ("alt", "aria-label"):
                if a.get(key):
                    cur["text"].append(a[key] + "\n")
        if tag == "title" and not self._in("svg"):
            self._title = True
        if tag == "script" and "src" not in a:
            self._script = {"line": line, "text": []}
        foreign = self._in("svg") or tag == "svg"
        if tag in VOID or (selfclose and foreign):
            return
        self.stack.append(el)

    def handle_starttag(self, tag, attrs):
        self._open(tag, attrs, False)

    def handle_startendtag(self, tag, attrs):
        self._open(tag, attrs, True)

    def handle_endtag(self, tag):
        line = self.getpos()[0]
        if tag == "script" and self._script is not None:
            self.scripts.append({"line": self._script["line"], "text": "".join(self._script["text"])})
            self._script = None
        if tag == "title":
            self._title = False
        if tag in VOID:
            return
        cur1 = self._slide()
        if cur1 is not None and tag in BLOCK:
            cur1["text"].append("\n")
        for k in range(len(self.stack) - 1, -1, -1):
            if self.stack[k]["tag"] == tag:
                closed = self.stack[k + 1:]
                bad = [desc(e) for e in closed if e["tag"] in STRUCTURAL]
                if bad:
                    self.implicit.append((line, tag, desc(self.stack[k]), bad))
                del self.stack[k:]
                return
        self.stray.append((line, tag))

    def handle_data(self, data):
        if self._script is not None:
            self._script["text"].append(data)
            return
        if self._title:
            self.title = (self.title or "") + data
            return
        if self._in("style"):
            return
        for e in reversed(self.stack):
            if e.get("badge") is not None:
                e["badge"]["text"].append(data)
                return
        cur = self._slide()
        if cur is not None:
            cur["text"].append(data)


# ---- JavaScript string-array reader (lenient, so it can report what node would reject)

def _read_string(js, i):
    q = js[i]
    j = i + 1
    n = len(js)
    buf = []
    raw_nl = False
    while j < n:
        ch = js[j]
        if ch == "\\" and j + 1 < n:
            nx = js[j + 1]
            simple = {"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f", "v": "\v", "0": "\0"}
            if nx in simple:
                buf.append(simple[nx]); j += 2
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
            elif nx == "\r":
                j += 3 if js[j + 2:j + 3] == "\n" else 2
            else:
                buf.append(nx); j += 2
        elif ch == q:
            return "".join(buf), j + 1, raw_nl
        else:
            if ch == "\n" and q != "`":
                raw_nl = True
            buf.append(ch); j += 1
    return "".join(buf), n, raw_nl


def parse_array(js, name, base_line):
    """Return (entries, problems). entries: list of {text, raw_newline, line}; None if absent."""
    m = re.search(r"\b(?:var|let|const)\s+%s\s*=\s*\[" % re.escape(name), js)
    if not m:
        return None, []
    i, n = m.end(), len(js)
    entries, problems = [], []
    cur = None
    plus = False

    def flush():
        nonlocal cur
        if cur is not None:
            entries.append(cur)
        cur = None

    while i < n:
        c = js[i]
        if c.isspace():
            i += 1
        elif js.startswith("//", i):
            j = js.find("\n", i)
            i = n if j < 0 else j
        elif js.startswith("/*", i):
            j = js.find("*/", i + 2)
            i = n if j < 0 else j + 2
        elif c in "\"'`":
            line = base_line + js.count("\n", 0, i)
            s, i, raw = _read_string(js, i)
            if cur is not None and not plus:
                problems.append("missing comma before entry %d (line %d)" % (len(entries) + 2, line))
                flush()
            if cur is None:
                cur = {"text": "", "raw_newline": False, "line": line}
            cur["text"] += s
            cur["raw_newline"] = cur["raw_newline"] or raw
            plus = False
            if raw:
                problems.append("entry %d (line %d) has a real line break inside the string; use \\n"
                                % (len(entries) + 1, line))
        elif c == "+":
            plus = True; i += 1
        elif c == ",":
            flush(); plus = False; i += 1
        elif c == "]":
            flush()
            return entries, problems
        else:
            problems.append("unexpected %r at line %d" % (c, base_line + js.count("\n", 0, i)))
            i += 1
    flush()
    problems.append("array %s is not closed" % name)
    return entries, problems


# ---- SCRIPT.md reader

def script_sections(text, raw=False):
    """Map slide number -> body text, from headings that contain 'SLIDE N' (or OPENING SLIDE).
    raw=False gives whitespace-normalised text; raw=True keeps paragraph breaks."""
    sections, dupes = {}, []
    cur, body, started = None, [], False
    fenced = False

    def close():
        nonlocal cur, body, started
        if cur is not None:
            if cur in sections:
                dupes.append(cur)
            if raw:
                t = "\n".join(l.rstrip() for l in body).strip()
                sections[cur] = re.sub(r"\n{3,}", "\n\n", t)
            else:
                sections[cur] = norm(" ".join(body))
        cur, body, started = None, [], False

    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced      # headings inside a code fence are examples, not slides
            if cur is not None and started:
                close()
            continue
        if fenced:
            continue
        h = re.match(r"^\s{0,3}#{1,6}\s+(.*)$", line)
        banner = re.match(r"^\s*(?:={3,}|-{3,}|\*{3,}|_{3,})\s*$", line)
        if h:
            close()
            t = h.group(1)
            m = re.search(r"\bslide\s*0*(\d+)\b", t, re.I)
            if m:
                cur = int(m.group(1))
            elif re.search(r"\b(?:opening|title)\s+slide\b", t, re.I):
                cur = 1
        elif cur is not None:
            if banner:
                if started:
                    close()
            elif line.strip():
                started = True
                body.append(line)
            elif started:
                body.append(line)
    close()
    return sections, dupes


# ---- the checks

class Report:
    def __init__(self, quiet):
        self.rows = []
        self.quiet = quiet

    def add(self, letter, status, msg, details=()):
        self.rows.append((letter, status, msg, list(details)))

    def show(self):
        for letter, status, msg, details in self.rows:
            if self.quiet and status == "PASS":
                continue
            print("%-8s %s  %s" % (status, letter, msg))
            shown = details[:8]
            for d in shown:
                print("             " + d)
            if len(details) > len(shown):
                print("             ... and %d more" % (len(details) - len(shown)))

    def count(self, status):
        return sum(1 for r in self.rows if r[1] == status)


def check_a(rep, parser, require_node, notes_probs):
    scripts = [s for s in parser.scripts if s["text"].strip()]
    if not scripts:
        rep.add("a", "FAIL", "no inline <script> block: arrow keys, dots and the presenter window will not exist")
        return
    node = shutil.which("node")
    raw = [p for p in notes_probs if "line break" in p or "missing comma" in p]
    if not node:
        status = "FAIL" if (require_node or raw) else "SKIPPED"
        rep.add("a", status,
                "node not found: the script was NOT syntax-checked. Install node, or open the deck "
                "in Chrome and press P to test by hand."
                + (" The fallback scan found real errors:" if raw else ""), raw)
        return
    ver = subprocess.run([node, "--version"], capture_output=True, text=True).stdout.strip()
    errs = []
    for s in scripts:
        fd, path = tempfile.mkstemp(suffix=".js", prefix="moi-deck-check-")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(s["text"])
            r = subprocess.run([node, "--check", path], capture_output=True, text=True)
        finally:
            os.unlink(path)
        if r.returncode != 0:
            lines = [l for l in r.stderr.splitlines() if l.strip()]
            m = re.search(r":(\d+)\s*$", lines[0]) if lines else None
            where = " (deck line %d)" % (s["line"] + int(m.group(1)) - 1) if m else ""
            err = next((l for l in lines if "Error" in l), "syntax error")
            errs.append("script starting at line %d: %s%s" % (s["line"], err.strip(), where))
    if errs:
        rep.add("a", "FAIL", "the inline script does not parse, so arrow keys, dots and the presenter "
                "window are dead (the PDF still prints)", errs + raw)
    else:
        rep.add("a", "PASS", "inline script parses (node %s, %d block%s)" % (ver, len(scripts), "" if len(scripts) == 1 else "s"))


def check_b(rep, parser):
    slides = parser.slides
    if not slides:
        rep.add("b", "FAIL", "no <section class=\"slide\"> found")
        return
    problems = []
    stage_missing = not any(s["parent_is_stage"] for s in slides)
    bad = [s for s in slides if not s["parent_is_stage"]]
    if bad:
        by_parent = {}
        for s in bad:
            by_parent.setdefault(s["parent"], []).append(str(s["index"]))
        for parent, idx in by_parent.items():
            problems.append("slide%s %s: parent is %s, not the stage (they will not scale with it)"
                            % ("s" if len(idx) > 1 else "", ", ".join(idx), parent))
    if stage_missing and not bad:
        problems.append("no stage element (id=\"stage\" or class deck-stage) found")
    for b in parser.badges:
        if b["slide"] is None:
            problems.append("badge \"%s\" at line %d sits outside every slide (parent %s)"
                            % (norm("".join(b["text"])), b["line"], b["parent"]))
    unbalanced = []
    for line, tag, matched, skipped in parser.implicit:
        if tag == "div":
            unbalanced.append("line %d: </div> closes %s and, on the way, %s (a stray </div> just above this line)"
                              % (line, matched, ", ".join(skipped)))
        else:
            unbalanced.append("line %d: </%s> arrives while %s still open (a </div> is missing before this line)"
                              % (line, tag, ", ".join(skipped)))
    for line, tag in parser.stray:
        if tag in STRUCTURAL:
            unbalanced.append("line %d: stray </%s> with nothing open to close" % (line, tag))
    if problems:
        rep.add("b", "FAIL", "slide structure is broken", problems + unbalanced)
    elif unbalanced:
        rep.add("b", "WARN", "slides and badges are placed correctly, but tags are unbalanced", unbalanced)
    else:
        rep.add("b", "PASS", ("the slide is a direct child" if len(slides) == 1
                              else "all %d slides are direct children" % len(slides))
                + " of the stage; every badge is inside its slide")


def check_c(rep, parser):
    slides = parser.slides
    n = len(slides)
    problems = []
    for s in slides:
        k = s["index"]
        nums = [norm("".join(b["text"])) for b in s["badges"]]
        edge = k == 1 or k == n
        if edge:
            if nums:
                problems.append("slide %d (%s) carries badge %s; cover and close carry none"
                                % (k, "cover" if k == 1 else "close", ", ".join(nums)))
            continue
        if not nums:
            problems.append("slide %d has no badge" % k)
        elif len(nums) > 1:
            problems.append("slide %d has %d badges" % (k, len(nums)))
        elif not re.fullmatch(r"\d+", nums[0]) or int(nums[0]) != k:
            problems.append("slide %d carries badge \"%s\"" % (k, nums[0]))
    if problems:
        rep.add("c", "FAIL", "badges do not match page numbers", problems)
    else:
        rep.add("c", "PASS", ("badges 02 to %02d match their pages; " % (n - 1) if n > 2 else "")
                + "cover and close carry none")


def bg_key(classes):
    if "dark" in classes:
        return "dark grad" if "grad" in classes else "dark"
    for c in ("lav", "light"):
        if c in classes:
            return c
    return None


def check_d(rep, parser):
    slides = parser.slides
    fails, warns = [], []
    keys = [bg_key(s["classes"]) for s in slides]
    for s, k in zip(slides, keys):
        if k is None:
            warns.append("slide %d has no background class (light, lav, dark, dark grad)" % s["index"])
    for i in range(1, len(slides)):
        a, b = keys[i - 1], keys[i]
        if a and a == b:
            fails.append("slides %d and %d are both '%s'" % (i, i + 1, a))
        elif a and b and a.startswith("dark") and b.startswith("dark"):
            warns.append("slides %d and %d are both dark ('%s' then '%s'); they look alike" % (i, i + 1, a, b))
    if fails:
        rep.add("d", "FAIL", "neighbouring slides share a background", fails + warns)
    elif warns:
        rep.add("d", "WARN", "backgrounds alternate, with caveats", warns)
    else:
        rep.add("d", "PASS", "backgrounds alternate (%s)" % ", ".join(k or "?" for k in keys))


def check_e(rep, parser, titles, notes, tprob, nprob):
    n = len(parser.slides)
    problems = []
    for name, ent in (("TITLES", titles), ("NOTES", notes)):
        if ent is None:
            problems.append("%s array not found (looked for var %s = [ ... ])" % (name, name))
        elif len(ent) != n:
            problems.append("%s has %d entries, the deck has %d slides" % (name, len(ent), n))
    for p in tprob + nprob:
        if "line break" not in p and "missing comma" not in p:
            problems.append(p)
    if problems:
        rep.add("e", "FAIL", "TITLES and NOTES do not line up with the slides", problems)
    else:
        rep.add("e", "PASS", "TITLES and NOTES each have %d entr%s, one per slide" % (n, "y" if n == 1 else "ies"))


def build_corpus(parser, titles, notes):
    """Return (corpus, lines). corpus: (where, normalised text). lines: the same text split at
    block boundaries and paragraph breaks, so a pattern cannot run across two elements."""
    raw = []
    for s in parser.slides:
        raw.append(("slide %d" % s["index"], "".join(s["text"])))
    for i, e in enumerate(titles or [], 1):
        raw.append(("TITLES %d" % i, e["text"]))
    for i, e in enumerate(notes or [], 1):
        raw.append(("NOTES %d" % i, e["text"]))
    corpus = [(w, norm(t)) for w, t in raw]
    lines = [(w, norm(l)) for w, t in raw for l in t.split("\n") if l.strip()]
    return corpus, lines


def presenter_title(parser, doc_title):
    js = "\n".join(s["text"] for s in parser.scripts)
    if "document.title" in js:
        return "from-document", None
    m = re.search(r"<title>(.*?)</title>", js)
    if not m:
        return "none", None
    return "literal", m.group(1)


def check_f(rep, corpus, parser, stale):
    hits = []
    for phrase in RETIRED + stale:
        p = norm(phrase).lower()
        for where, text in corpus:
            if p in text.lower():
                hits.append("%s: \"%s\"" % (where, phrase))
        if parser.title and p in norm(parser.title).lower():
            hits.append("document title: \"%s\"" % phrase)
    soft = []
    for phrase, why in RETIRED_SOFT:
        p = norm(phrase).lower()
        found = [where for where, text in corpus if p in text.lower()]
        if parser.title and p in norm(parser.title).lower():
            found.append("document title")
        if found:
            soft.append("%s: \"%s\" (%s)" % (", ".join(found[:4]) + (" ..." if len(found) > 4 else ""), phrase, why))
    kind, lit = presenter_title(parser, parser.title)
    warn = []
    if kind == "literal":
        def key(t):
            t = re.sub(r"^\s*presenter\s*[:\-|" + chr(0x2013) + chr(0x2014) + chr(0xb7) + r"]*\s*", "", t, flags=re.I)
            return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()
        a, b = key(lit), key(parser.title or "")
        if a != b:
            msg = "presenter window title is hard-coded as \"%s\" but the document title is \"%s\"" % (norm(lit), norm(parser.title or ""))
            (warn if a and a in b else hits).append(msg)
    if hits:
        rep.add("f", "FAIL", "retired phrase or stale presenter title", hits + warn + soft)
    elif warn or soft:
        what = (["a phrase removed from an earlier deck"] if soft else []) + \
               (["a presenter title that is a hard-coded copy of the document title"] if warn else [])
        rep.add("f", "WARN", "check by eye: " + " and ".join(what), warn + soft)
    else:
        how = "taken from the document title" if kind == "from-document" else "no presenter title found"
        rep.add("f", "PASS", "no retired phrase; presenter title %s" % how)


def check_g(rep, corpus, parser):
    hits = ["%s: %s" % (w, _ctx(t, EM_DASH)) for w, t in corpus if EM_DASH in t]
    kind, lit = presenter_title(parser, parser.title)
    warn = []
    if parser.title and EM_DASH in parser.title:
        warn.append("document title contains an em dash (it shows in the browser tab and the PDF)")
    if lit and EM_DASH in lit:
        warn.append("presenter window title contains an em dash")
    if hits:
        rep.add("g", "FAIL", "em dash in text the audience or the presenter reads", hits + warn)
    elif warn:
        rep.add("g", "WARN", "no em dash in slides or notes, but the titles have one", warn)
    else:
        rep.add("g", "PASS", "no em dash in slide text, notes or titles")


def _ctx(text, needle, width=34):
    k = text.find(needle) if isinstance(needle, str) else needle.start()
    return "...%s..." % text[max(0, k - width):k + width + 1]


def loose(s):
    """Wording with markup, cue brackets, arrows and case removed."""
    return norm(re.sub(r"[*_`\[\](){}\u27f6]", "", s)).lower()


def check_h(rep, notes, script_path):
    if script_path is None:
        rep.add("h", "SKIPPED", "no --script given: NOTES were not compared with a script file")
        return
    try:
        with open(script_path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        rep.add("h", "FAIL", "cannot read %s: %s" % (script_path, e))
        return
    sections, dupes = script_sections(text)
    if not sections:
        rep.add("h", "FAIL", "no slide sections found in %s; headings must contain SLIDE N (see templates/SCRIPT.md)"
                % os.path.basename(script_path))
        return
    problems = ["two sections for slide %d in the script file" % d for d in dupes]
    same, fmt = 0, []
    for k in sorted(sections):
        if notes is None or k > len(notes):
            problems.append("script has a section for slide %d but the deck has no NOTES entry %d" % (k, k))
            continue
        a, b = norm(notes[k - 1]["text"]), sections[k]
        if a == b:
            same += 1
            continue
        if loose(a) == loose(b):
            fmt.append("slide %d: wording identical, markup or cue notation differs (write cues the same way in both)" % k)
            continue
        d = next((x for x in range(min(len(a), len(b))) if a[x] != b[x]), min(len(a), len(b)))
        problems.append("slide %d differs at character %d: NOTES \"...%s\" / script \"...%s\""
                        % (k, d, a[max(0, d - 12):d + 24], b[max(0, d - 12):d + 24]))
    if problems:
        rep.add("h", "FAIL", "NOTES and %s differ in wording (%d of %d sections match)"
                % (os.path.basename(script_path), same, len(sections)), problems + fmt)
    elif fmt:
        rep.add("h", "WARN", "NOTES and %s use the same words but not the same markup (%d of %d sections identical)"
                % (os.path.basename(script_path), same, len(sections)), fmt)
    else:
        rep.add("h", "PASS", "%d NOTES entr%s match%s %s of %s word for word"
                % (same, "y" if same == 1 else "ies", "es" if same == 1 else "",
                   "its section" if same == 1 else "their sections", os.path.basename(script_path)))


def check_i(rep, corpus):
    hits = []
    for where, text in corpus:
        for m in RELATIVE.finditer(text):
            hits.append("%s: \"%s\" in %s" % (where, m.group(0), _ctx(text, m)))
    if hits:
        rep.add("i", "WARN", "relative time words go stale; give a date or cut them", hits)
    else:
        rep.add("i", "PASS", "no relative time words")


def check_j(rep, parser, deck_dir):
    missing = []
    for src, slide, line in parser.images:
        if re.match(r"^(?:[a-z][a-z0-9+.-]*:|//|#)", src, re.I):
            continue
        path = os.path.join(deck_dir, unquote(src.split("#")[0].split("?")[0]))
        if not os.path.isfile(path):
            missing.append("%s (slide %s, line %d)" % (src, slide["index"] if slide else "?", line))
    if missing:
        rep.add("j", "WARN", "%d referenced file%s missing; the frame shows its filename. List them on hand-back."
                % (len(missing), "" if len(missing) == 1 else "s"), missing)
    else:
        rep.add("j", "PASS", "every local image the slides point at exists")


def check_k(rep, parser, deck_dir):
    path = os.path.join(deck_dir, "README.md")
    if not os.path.isfile(path):
        rep.add("k", "PASS", "no README.md beside the deck, so nothing can be stale (new-deck.sh writes one)")
        return
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    n = len(parser.slides)
    counts = sorted({int(x) for x in re.findall(r"\b(\d+)\s+slides?\b", text, re.I)})
    wrong = [c for c in counts if c != n]
    if wrong:
        rep.add("k", "WARN", "README.md says %s slides; the deck has %d. Update the README." % (", ".join(map(str, wrong)), n))
    else:
        rep.add("k", "PASS", "README.md agrees with the deck (%d slide%s)" % (n, "" if n == 1 else "s") if counts else "README.md states no slide count")


def check_l(rep, deck_path, deck_dir):
    me = os.path.abspath(deck_path)
    h = hashlib.sha256(open(me, "rb").read()).hexdigest()
    same = []
    for name in sorted(os.listdir(deck_dir)):
        p = os.path.join(deck_dir, name)
        if name.endswith(".html") and os.path.abspath(p) != me and os.path.isfile(p):
            if hashlib.sha256(open(p, "rb").read()).hexdigest() == h:
                same.append(name)
    if same:
        rep.add("l", "WARN", "variant file%s byte-identical to this deck: collapse them and delete the duplicate PDF"
                % ("s" if len(same) > 1 else ""), same)
    else:
        rep.add("l", "PASS", "no identical variant files beside the deck")


def check_m(rep, corpus):
    hits = []
    for where, text in corpus:
        for m in PLACEHOLDER.finditer(text):
            hits.append("%s: %s" % (where, _ctx(text, m)))
    if hits:
        rep.add("m", "WARN", "placeholder text is still in the deck", hits)
    else:
        rep.add("m", "PASS", "no placeholder markers (TODO, <<<, REPLACE-WITH)")


def check_n(rep, lines):
    hits = []
    for where, text in lines:
        for rx, label in CONTRASTS:
            for m in rx.finditer(text):
                hits.append("%s: %s %s" % (where, label, _ctx(text, m)))
    if hits:
        rep.add("n", "WARN", "possible 'not this, not that' contrast; rewrite as a plain statement", hits)
    else:
        rep.add("n", "PASS", "no 'not X, not Y' contrasts found")


LAYOUT_JS = r"""
<script>
(function () {
  function run() {
    var st = document.createElement('style');
    st.textContent = '.slide .rv{opacity:1!important;transform:none!important;animation:none!important}';
    document.head.appendChild(st);
    var res = [];
    document.querySelectorAll('section.slide').forEach(function (s, i) {
      var r = s.getBoundingClientRect(), k = (r.width / 1920) || 1, mb = 0, mr = 0, clip = [];
      s.querySelectorAll('.pad *').forEach(function (e) {
        if (e.closest('svg') && e.tagName.toLowerCase() !== 'svg') return;
        if (e.closest('.photo') && !e.classList.contains('photo')) return;
        var b = e.getBoundingClientRect();
        if (!b.width && !b.height) return;
        mb = Math.max(mb, (b.bottom - r.top) / k); mr = Math.max(mr, (b.right - r.left) / k);
        if (getComputedStyle(e).overflow === 'hidden' && !e.classList.contains('photo') &&
            (e.scrollWidth > e.clientWidth + 1 || e.scrollHeight > e.clientHeight + 1)) clip.push(e.className || e.tagName);
      });
      res.push({i: i + 1, bottom: Math.round(mb), right: Math.round(mr), clip: clip});
    });
    var pre = document.createElement('pre'); pre.id = 'moi-layout';
    pre.textContent = JSON.stringify(res); document.body.appendChild(pre);
  }
  (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(function () { setTimeout(run, 300); });
})();
</script>
"""


def find_chrome(explicit):
    cands = [explicit, os.environ.get("CHROME"),
             "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
             "/Applications/Chromium.app/Contents/MacOS/Chromium"]
    for c in cands:
        if c and os.access(c, os.X_OK):
            return c
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        w = shutil.which(name)
        if w:
            return w
    return None


def check_o(rep, deck_path, src, chrome_path):
    chrome = find_chrome(chrome_path)
    if not chrome:
        rep.add("o", "SKIPPED", "Chrome not found: slide overflow was NOT measured. Set CHROME, or look at the PDF pages.")
        return
    base = "file://" + os.path.dirname(os.path.abspath(deck_path)).replace(" ", "%20") + "/"
    page = re.sub(r"(?i)<head>", "<head><base href=\"%s\">" % base, src, count=1)
    page = re.sub(r"(?i)</body>", lambda m: LAYOUT_JS + "</body>", page, count=1)
    fd, tmp = tempfile.mkstemp(suffix=".html", prefix="moi-deck-layout-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(page)
        try:
            r = subprocess.run([chrome, "--headless=new", "--disable-gpu", "--window-size=1920,1080",
                                "--virtual-time-budget=8000"] + shlex.split(os.environ.get("CHROME_FLAGS", ""))
                               + ["--dump-dom", "file://" + tmp],
                               capture_output=True, text=True, timeout=90)
        except subprocess.TimeoutExpired:
            rep.add("o", "SKIPPED", "Chrome did not finish within 90 seconds: slide overflow was NOT measured")
            return
    finally:
        os.unlink(tmp)
    m = re.search(r'<pre id="moi-layout">(.*?)</pre>', r.stdout, re.S)
    if not m:
        rep.add("o", "SKIPPED", "Chrome ran but returned no measurements: slide overflow was NOT measured")
        return
    import html as _h
    res = json.loads(_h.unescape(m.group(1)))
    fails, warns = [], []
    for x in res:
        if x["bottom"] > 1080 or x["right"] > 1920:
            fails.append("slide %d: content reaches y=%d, x=%d on a 1080 by 1920 slide, so it is cut off"
                         % (x["i"], x["bottom"], x["right"]))
        elif x["bottom"] > 990:
            warns.append("slide %d: content reaches y=%d, into the bottom margin (badge area starts near 1000)"
                         % (x["i"], x["bottom"]))
        for c in x["clip"]:
            fails.append("slide %d: text is clipped inside .%s" % (x["i"], str(c).split()[0]))
    if fails:
        rep.add("o", "FAIL", "slide content overflows", fails + warns)
    elif warns:
        rep.add("o", "WARN", "content runs into the bottom margin", warns)
    else:
        rep.add("o", "PASS", ("the slide fits" if len(res) == 1 else "all %d slides fit" % len(res))
                + " inside the 1920 by 1080 slide")


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


def main(argv):
    deck, script, stale, skip = None, None, [], set()
    quiet = require_node = layout = False
    chrome_arg = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("-h", "--help"):
            print(__doc__); return 0
        if a == "--script" and i + 1 < len(argv):
            script = argv[i + 1]; i += 2
        elif a == "--stale" and i + 1 < len(argv):
            stale.append(argv[i + 1]); i += 2
        elif a == "--skip" and i + 1 < len(argv):
            skip |= set(argv[i + 1].lower()); i += 2
        elif a == "--layout":
            layout = True; i += 1
        elif a == "--chrome" and i + 1 < len(argv):
            chrome_arg = argv[i + 1]; i += 2
        elif a == "--require-node":
            require_node = True; i += 1
        elif a == "--quiet":
            quiet = True; i += 1
        elif a.startswith("-"):
            print("unknown option %s (try --help)" % a, file=sys.stderr); return 2
        elif deck is None:
            deck = a; i += 1
        else:
            print("only one deck at a time", file=sys.stderr); return 2
    if not deck:
        print(__doc__, file=sys.stderr); return 2
    for named in (deck, script):
        if named and is_env_file(named):
            print("check-deck: refusing to read %s: an env file can hold keys and is never opened. "
                  "Pass the deck or the script instead." % os.path.basename(named), file=sys.stderr)
            return 2
    try:
        with open(deck, encoding="utf-8") as f:
            src = f.read()
    except (OSError, UnicodeDecodeError) as e:
        print("cannot read %s: %s" % (deck, e), file=sys.stderr); return 2

    p = DeckParser()
    p.feed(src)
    p.close()
    deck_dir = os.path.dirname(os.path.abspath(deck))

    titles = notes = None
    tprob, nprob = [], []
    for s in p.scripts:
        t, tp = parse_array(s["text"], "TITLES", s["line"])
        nn, npb = parse_array(s["text"], "NOTES", s["line"])
        if t is not None:
            titles, tprob = t, tp
        if nn is not None:
            notes, nprob = nn, npb
    corpus, lines = build_corpus(p, titles, notes)

    rep = Report(quiet)
    steps = [
        ("a", lambda: check_a(rep, p, require_node, tprob + nprob)),
        ("b", lambda: check_b(rep, p)),
        ("c", lambda: check_c(rep, p)),
        ("d", lambda: check_d(rep, p)),
        ("e", lambda: check_e(rep, p, titles, notes, tprob, nprob)),
        ("f", lambda: check_f(rep, corpus, p, stale)),
        ("g", lambda: check_g(rep, corpus, p)),
        ("h", lambda: check_h(rep, notes, script)),
        ("i", lambda: check_i(rep, corpus)),
        ("j", lambda: check_j(rep, p, deck_dir)),
        ("k", lambda: check_k(rep, p, deck_dir)),
        ("l", lambda: check_l(rep, deck, deck_dir)),
        ("m", lambda: check_m(rep, corpus)),
        ("n", lambda: check_n(rep, lines)),
    ]
    if layout:
        steps.append(("o", lambda: check_o(rep, deck, src, chrome_arg)))
    for letter, fn in steps:
        if letter in skip:
            rep.add(letter, "SKIPPED", "skipped by --skip")
        else:
            fn()
    print("%s: %d slide%s" % (deck, len(p.slides), "" if len(p.slides) == 1 else "s"))
    rep.show()
    f, w, s = rep.count("FAIL"), rep.count("WARN"), rep.count("SKIPPED")
    note = ""
    if any(r[0] == "a" and r[1] == "SKIPPED" for r in rep.rows):
        note = "  NOTE: check a did NOT run, so this deck's JavaScript is unverified."
    print("RESULT: %s (%d FAIL, %d WARN, %d SKIPPED, %d PASS)%s"
          % ("FAIL" if f else "ok", f, w, s, rep.count("PASS"), note))
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
