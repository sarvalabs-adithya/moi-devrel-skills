#!/usr/bin/env python3
"""docs-page-lint.py: check pages of MOI's docs sites against references/page-standard.md.

Usage (SKILLS is the folder that holds the moi-* skills, quoted because a path can hold spaces; run it from
the working copy of the docs repo you are in):
    python3 "$SKILLS/moi-docs/scripts/docs-page-lint.py" [options] <page-or-folder>...
    python3 "$SKILLS/moi-docs/scripts/docs-page-lint.py" --list-rules

Pages: .md and .mdx (the three Docusaurus sites), .rst (the js-moi-sdk Sphinx site) and _category_.json. A
folder is searched for those files. These are skipped: folders named node_modules, static (it holds generated
markdown copies), .git and .docusaurus; folders whose name starts with an underscore (_extra, _static); a folder
named build that holds site output (index.html, html, sitemap.xml or llms.txt), though docs/build of moidocs is a
real section and is read; and files whose name starts with an underscore (except _category_.json).

Options:
    --site NAME             moidocs, voyage-docs, coco-docs or generic. Default: guessed from the path
                            (docs/learn|build|guard is moidocs, docs/getting-started|endpoint-docs|
                            wallet-authentication is voyage-docs, docs/book|install|releases is coco-docs).
                            A page outside those paths is checked as generic: no site-specific rule applies.
    --added-lines-since REF only report a finding about a line if git says the line was added or changed since
                            REF (git diff -U0 REF -- file, which includes uncommitted edits; an untracked file
                            counts as all added). A finding about something missing has no line and is always
                            shown. Also reports a heading whose anchor no longer exists after the change.
    --strict                every warning counts as an error
    --no-slop-lint          do not call moi-devrel's slop-lint.sh. Without this flag a missing slop-lint.sh is a
                            usage error, so the phrasing rules can never be skipped by accident.
    --verbose               print the site each page was checked as
    --list-rules            print every rule with its level and where it comes from, then exit

Output: <file>:<line>:<LEVEL>:<rule>: <message>, one line per finding (line 0 means the whole page), then a
summary on stderr. Anything a message quotes from the page has secret shapes, long hex strings and runs of 12 or
more short words masked first, so the lint never echoes a key or a recovery phrase that sits in a page. A line
that contains "slop-lint: ignore" is skipped by the line rules (use it only in this library's own files, to quote
a wrong form on purpose; do not add a comment to a site page).
Exit codes: 0 no error (warnings allowed), 1 at least one error, 2 usage error or unreadable input.
Python 3 standard library only. It reads the pages, runs slop-lint.sh and, with --added-lines-since, local git
reads. It also looks, read only, for docusaurus.config.js above a page and for src/components and
static/img/moi-card-learn.png beside it, to tell `main` from the PR branches that add the search layer (the
Book's route prefix on coco-docs, the section cards and the schema components on moidocs). With no such config
above the page every rule applies as written. It never writes, never uses the network, and refuses an env-named
file or a file inside an env-named folder (such folders are also skipped when it walks a folder).
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

EM_DASH = chr(0x2014)  # built from its code point so this file never holds the character itself
BOM = chr(0xFEFF)
ENTITY_DASH = re.compile("&" + r"mdash;|&#0*8212;|&#x0*2014;", re.I)  # the HTML spellings of the em dash
LOCAL_PATH = re.compile("/Us" + r"ers/|[A-Za-z]:\\Us" + r"ers\\")
MAX_BYTES = 2000000
DESC_MIN, DESC_MAX, TITLE_MAX = 130, 170, 60
SKIP_DIRS = {"node_modules", "static", ".git", ".docusaurus"}
PAGE_EXT = {".md", ".mdx", ".rst"}

# rule id -> (level, where it comes from, what it means). The source labels: guide = DOCS-STYLE-GUIDE.md (only on
# PR #124 of sarvalabs/moidocs as of 2026-10-03), house = moi-devrel house rules, build = the build fails or the
# metadata is dropped silently, derived = this library's reading, not stated in the guide.
RULES = {
    "fm-missing": ("ERROR", "guide step 1", "the page has no frontmatter block"),
    "fm-not-first": ("ERROR", "guide step 1", "frontmatter must start on line 1; anything above the first --- makes the site ignore the block"),
    "fm-unclosed": ("ERROR", "build", "the opening --- is never closed"),
    "fm-bom": ("ERROR", "derived", "the file starts with a byte order mark, so line 1 is not ---"),
    "fm-yaml": ("ERROR", "guide step 1, build", "a frontmatter line YAML cannot read (unquoted colon, stray quote, duplicate key)"),
    "crlf": ("WARN", "derived", "CRLF line endings: the llms generator of moidocs and voyage-docs reads frontmatter with an LF-only pattern"),
    "title-missing": ("ERROR", "guide step 1", "no title"),
    "title-long": ("WARN", "guide step 1", "title longer than 60 characters"),
    "title-version": ("WARN", "guide step 1", "version number or date in the title"),
    "title-site-name": ("WARN", "guide step 1", "the site appends its own name; do not write it in the title"),
    "description-missing": ("ERROR", "guide step 1", "no description"),
    "description-length": ("WARN", "guide step 1", "description outside 130 to 170 characters"),
    "description-multiline": ("WARN", "derived", "description spans several lines; the llms generator reads one line"),
    "description-teaser": ("WARN", "guide step 1", "description opens like a teaser; write a statement of what the page covers"),
    "description-same-as-title": ("WARN", "derived", "description repeats the title"),
    "sidebar-position-missing": ("ERROR", "guide step 1", "no sidebar_position (a warning on an index page)"),
    "sidebar-position-value": ("WARN", "derived", "sidebar_position is not a number"),
    "image-wrong": ("ERROR", "guide step 1", "moidocs: image missing or not the card for this section (a warning on a stub)"),
    "image-extra": ("WARN", "guide table", "voyage-docs and coco-docs leave image out"),
    "image-card-missing": ("WARN", "observed", "moidocs: the section cards (static/img/moi-card-*.png) are not in this checkout, they are on PR #124 only; leave image out until it merges"),
    "stub-unmarked": ("ERROR", "guide step 5", "a short page says it is coming soon but is not marked noindex or unlisted"),
    "stub-text": ("WARN", "guide step 5", "a longer page says coming soon or under development; if a whole section is a placeholder, the page is a stub"),
    "stub-marked-finished": ("WARN", "guide step 5", "the page is marked as a stub but has real content; remove the mark if it is finished"),
    "stub-wrong-marker": ("WARN", "guide table", "moidocs and voyage-docs use the noindex block, coco-docs uses unlisted: true"),
    "h1-multiple": ("ERROR", "guide step 3", "more than one # heading"),
    "h1-with-schema": ("ERROR", "guide step 6", "a # heading on a page with a HowToSchema or FaqSchema call shows two titles"),
    "h1-voyage": ("WARN", "guide table", "voyage-docs leaves the # heading out"),
    "heading-skip": ("WARN", "derived", "heading level skipped (## then ####)"),
    "anchor-lost": ("WARN", "guide rule 4", "a heading that changed no longer has its old anchor (needs --added-lines-since; the slug is approximate)"),
    "opening-missing": ("WARN", "guide step 2", "the page goes to a heading, list, table or code before any opening paragraph"),
    "opening-throat": ("WARN", "guide step 2", "the opening paragraph talks about the page before it says what the thing is"),
    "opening-short": ("WARN", "derived", "the opening paragraph is under 6 words"),
    "schema-no-import": ("ERROR", "build", "HowToSchema or FaqSchema is used but not imported"),
    "schema-component-missing": ("ERROR", "build", "HowToSchema or FaqSchema is imported but src/components has no such file in this checkout (PR #124 only), so the import cannot resolve"),
    "schema-blank-line": ("ERROR", "guide step 6", "a blank line inside a HowToSchema or FaqSchema call"),
    "schema-wrong-site": ("ERROR", "guide step 6", "HowToSchema and FaqSchema exist on moidocs only"),
    "schema-both": ("WARN", "derived", "both a HowToSchema and a FaqSchema on one page"),
    "tutorial-no-howto": ("WARN", "guide step 6", "moidocs tutorial without a HowToSchema call"),
    "faq-no-schema": ("WARN", "guide step 6", "moidocs FAQ page without a FaqSchema call"),
    "name-moi": ("ERROR", "guide step 4", "write MOI"),
    "name-moi-wallet": ("ERROR", "guide step 4", "write MOI Wallet"),
    "name-coco": ("ERROR", "guide step 4", "write Coco"),
    "name-js-moi-sdk": ("ERROR", "guide step 4", "js-moi-sdk is always lowercase"),
    "name-moipod": ("ERROR", "guide step 4", "write MOIPod in prose"),
    "name-sarva-labs": ("ERROR", "guide step 4", "write Sarva Labs"),
    "em-dash": ("ERROR", "house rule 6", "em dash"),
    "link-empty": ("ERROR", "derived", "a link with no target"),
    "link-no-scheme": ("ERROR", "derived", "an external address without https:// becomes a broken relative link"),
    "link-absolute-internal": ("WARN", "guide step 7", "link to a page of this site by its full URL; write the /address"),
    "link-form": ("WARN", "guide table", "coco-docs page addresses end with a slash"),
    "link-http": ("WARN", "derived", "http link"),
    "link-private-repo": ("WARN", "house rule 2", "link to a private MOI repo; readers cannot open it"),
    "link-route-prefix": ("WARN", "observed", "coco-docs: the Book is served under /docs/book/ on main and under /book/ after PR #12; this link uses the other form (read from docusaurus.config.js)"),
    "link-anchor-missing": ("WARN", "derived", "in-page link to an anchor no heading produces (the slug is approximate)"),
    "image-alt": ("WARN", "guide step 4", "image without alt text"),
    "placeholder": ("ERROR", "guide, Drive standard", "placeholder text must not ship"),
    "local-path": ("WARN", "house", "a path from someone's own machine"),
    "secret-shaped": ("ERROR", "house", "something shaped like a key or a token"),
    "recovery-phrase-shaped": ("WARN", "house rule 5", "a run of 12 or more short words, the shape of a recovery phrase"),
    "application-docs": ("WARN", "Rahul, 2026-09-17", "moidocs holds protocol docs; Launchpad and other app docs belong with the app (a backlink is fine)"),
    "fence-unclosed": ("ERROR", "derived", "a code fence is opened and never closed"),
    "duplicate-title": ("WARN", "derived", "two pages given to the lint have the same title"),
    "duplicate-description": ("WARN", "derived", "two pages given to the lint have the same description"),
    "category-json": ("ERROR", "build", "_category_.json is not valid JSON"),
    "category-description": ("WARN", "observed", "a generated-index category needs a description of 130 to 170 characters"),
    "meta-description-missing": ("ERROR", "guide, js-moi-sdk", "no .. meta:: :description: at the top of the .rst page"),
    "rst-title-missing": ("ERROR", "guide step 3", "no title"),
    "rst-title-multiple": ("ERROR", "guide step 3", "more than one top-level title"),
    "rst-underline-short": ("ERROR", "derived", "the title underline is shorter than the title (Sphinx warns)"),
    "toctree-missing": ("ERROR", "guide, js-moi-sdk", "the page is not listed in index.rst, so it builds but cannot be reached"),
    "sdk-pages-row-missing": ("ERROR", "guide, js-moi-sdk", "no row for the page in the PAGES table of docs/generate_llms.py"),
    "sdk-pages-desc-mismatch": ("ERROR", "guide, js-moi-sdk", "the description differs from the PAGES row of docs/generate_llms.py"),
    "sdk-sitemap-missing": ("ERROR", "guide, js-moi-sdk", "the page is not in docs/source/_extra/sitemap.xml"),
    "slop-lint": ("ERROR or WARN", "moi-devrel", "phrasing rules of slop-lint.sh, printed as slop-lint/<rule>"),
}
# Findings that name no line are about something missing. Everything else is filtered by --added-lines-since.

# ---------------------------------------------------------------- masking (same shapes as moi-devrel/claim-check)
LONG_HEX = re.compile(r"0x[0-9A-Fa-f]{17,}|[0-9A-Fa-f]{24,}")
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
PHRASE_MIN = 12
PHRASE_STOP = frozenset(
    "after and are been being both but could did does each every for from get got had has her here "
    "him his how its let many may most not our out per see she should some than the their them these "
    "those too using via was were which while who why with would yes your".split())
_PIECE = re.compile(r"[A-Za-z]+|[^A-Za-z]+")


def phrase_spans(s):
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
        elif re.fullmatch(r"[\s,;]+", text):
            continue
        else:
            close()
    close()
    return spans


def mask(s):
    """Mask secret shapes, long hex and phrase-shaped runs. Always applied before a string is shortened."""
    s = LONG_HEX.sub(lambda m: m.group(0)[:6] + "...(masked)", s)
    for rx in SECRET_SHAPES:
        s = rx.sub(lambda m: m.group(0)[:4] + "...(masked)", s)
    for a, b in reversed(phrase_spans(s)):
        s = s[:a] + "(masked: 12 or more short words, possible recovery phrase)" + s[b:]
    return s


def env_name(name):
    """True for .env, .envrc, .env.*, *.env and anything holding .env. in its name."""
    low = name.lower()
    return low in (".env", ".envrc") or low.startswith(".env.") or low.endswith(".env") or ".env." in low


def is_env_file(path):
    """An env-named file is never opened, nor is anything inside an env-named folder."""
    names = [os.path.basename(str(path))]
    parts = [p for p in Path(str(path)).parts[:-1]]
    try:
        real = os.path.realpath(str(path))
        names.append(os.path.basename(real))
        parts += list(Path(real).parts[:-1])
    except OSError:
        pass
    return any(env_name(n) for n in names) or any(env_name(p) for p in parts)


class InputError(Exception):
    pass


class Findings(object):
    def __init__(self):
        self.items = []

    def add(self, line, level, rule, msg):
        self.items.append((line, level, rule, msg))


# ---------------------------------------------------------------- site detection and small helpers
def detect_site(path, forced):
    if forced:
        return forced
    if path.suffix.lower() == ".rst":
        return "sphinx"
    p = "/" + str(path).replace("\\", "/").lstrip("/")
    try:
        p2 = "/" + str(path.resolve()).replace("\\", "/").lstrip("/")
    except OSError:
        p2 = p
    for cand in (p, p2):
        if re.search(r"/docs/(book|install|releases)/", cand):
            return "coco-docs"
        if re.search(r"/docs/(learn|build|guard)/", cand):
            return "moidocs"
        if re.search(r"/docs/(getting-started|endpoint-docs|wallet-authentication)/", cand):
            return "voyage-docs"
    return "generic"


SITE_HOST = {"moidocs": "docs.moi.technology", "voyage-docs": "voyage-docs.moi.technology", "coco-docs": "cocolang.dev"}
IMAGE_CARD = {"learn": "/img/moi-card-learn.png", "build": "/img/moi-card-build.png", "guard": "/img/moi-card-guard.png"}
FENCE_OPEN = re.compile(r"^\s*(`{3,}|~{3,})")
FENCE_CLOSE = re.compile(r"^\s*(`{3,}|~{3,})\s*$")
IGNORE = re.compile(r"slop-lint:\s*ignore")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
EXPLICIT_ID = re.compile(r"\{#([A-Za-z0-9_.:\-]+)\}\s*$")


def slugify(text):
    """Approximate the anchor Docusaurus builds from a heading (lowercase, no punctuation, hyphens)."""
    m = EXPLICIT_ID.search(text)
    if m:
        return m.group(1)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("`", "").replace("*", "").strip().lower()
    t = re.sub(r"[^\w\- ]", "", t)
    return t.replace(" ", "-")


def find_fences(lines):
    """Return (set of 1-based line numbers inside closed fences, list of line numbers of unclosed openers)."""
    inside, unclosed = set(), []
    i, total = 0, len(lines)
    while i < total:
        m = FENCE_OPEN.match(lines[i])
        if not m:
            i += 1
            continue
        marker = m.group(1)
        j = i + 1
        while j < total:
            c = FENCE_CLOSE.match(lines[j])
            if c and c.group(1)[0] == marker[0] and len(c.group(1)) >= len(marker):
                break
            j += 1
        if j < total:
            inside.update(range(i + 1, j + 2))
            i = j + 1
        else:
            unclosed.append(i + 1)
            i += 1
    return inside, unclosed


def prose_view(line):
    """A line with inline code, link targets, bare URLs and heading ids blanked, for the naming rules."""
    s = re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)
    s = re.sub(r"\]\([^)]*\)", "](...)", s)
    s = re.sub(r"https?://\S+", " ", s)
    s = re.sub(r"\{#[^}]*\}", " ", s)
    return s


# ---------------------------------------------------------------- what this checkout holds
_FACTS = {}


def repo_facts(path):
    """Read-only look at the repo around a page, so a rule can tell `main` from the PR branch that adds the search layer.
    Returns None when no docusaurus.config.js sits above the page (then every rule applies as written).
    coco_routes is "root" when the config sets routeBasePath '/' (PR #12) and "docs" when it does not (main)."""
    try:
        here = path.resolve().parent
    except OSError:
        return None
    root = None
    for d in [here] + list(here.parents)[:8]:
        if (d / "docusaurus.config.js").is_file():
            root = d
            break
        if (d / ".git").exists():
            break
    if root is None:
        return None
    if root in _FACTS:
        return _FACTS[root]
    cfg = ""
    try:
        cfg = (root / "docusaurus.config.js").read_text(encoding="utf-8", errors="replace")
    except OSError:
        pass
    comps = root / "src" / "components"
    facts = {
        "coco_routes": "root" if re.search(r"""routeBasePath\s*:\s*['"]/['"]""", cfg) else "docs",
        "cards": (root / "static" / "img" / "moi-card-learn.png").is_file(),
        "schema": {n: any((comps / (n + ext)).is_file() for ext in (".jsx", ".js", ".tsx")) for n in ("HowToSchema", "FaqSchema")},
    }
    _FACTS[root] = facts
    return facts


# ---------------------------------------------------------------- frontmatter
def scalar(raw, lineno, f):
    """Evaluate one frontmatter value. Returns (text, kind). Reports YAML problems to f."""
    s = raw.strip()
    if s == "":
        return "", "empty"
    if s[0] == '"':
        buf, j = [], 1
        esc = {"n": "\n", "t": "\t", '"': '"', "\\": "\\", "/": "/"}
        while j < len(s):
            c = s[j]
            if c == "\\" and j + 1 < len(s):
                buf.append(esc.get(s[j + 1], "\\" + s[j + 1]))
                j += 2
                continue
            if c == '"':
                break
            buf.append(c)
            j += 1
        else:
            f.add(lineno, "ERROR", "fm-yaml", "unterminated double-quoted value")
            return "".join(buf), "dq"
        rest = s[j + 1:].strip()
        if rest and not rest.startswith("#"):
            f.add(lineno, "ERROR", "fm-yaml", "text after the closing quote: an inner double quote needs a backslash")
        return "".join(buf), "dq"
    if s[0] == "'":
        buf, j = [], 1
        while j < len(s):
            c = s[j]
            if c == "'" and j + 1 < len(s) and s[j + 1] == "'":
                buf.append("'")
                j += 2
                continue
            if c == "'":
                break
            buf.append(c)
            j += 1
        else:
            f.add(lineno, "ERROR", "fm-yaml", "unterminated single-quoted value")
            return "".join(buf), "sq"
        rest = s[j + 1:].strip()
        if rest and not rest.startswith("#"):
            f.add(lineno, "ERROR", "fm-yaml", "text after the closing quote: an inner single quote must be doubled")
        return "".join(buf), "sq"
    if s[0] in "|>":
        return "", "block"
    if s[0] in "[{":
        return s, "flow"
    s = re.split(r"\s#", s, maxsplit=1)[0].rstrip()
    if s and s[0] in "@`%*&!":
        f.add(lineno, "ERROR", "fm-yaml", "a plain value cannot start with %s; wrap it in double quotes" % s[0])
    elif re.search(r":(\s|$)", s):
        f.add(lineno, "ERROR", "fm-yaml", "unquoted colon followed by a space: YAML reads a nested map and the build fails; wrap the whole value in double quotes")
    return s, "plain"


def parse_frontmatter(lines, f):
    """Return (fields, body_start_index, ok). fields maps key -> dict(line, value, kind, multi, raw). Reports structure errors."""
    n = len(lines)
    if n and lines[0] == "---":
        start = 0
    else:
        probe = 0
        while probe < min(n, 12) and lines[probe].strip() == "":
            probe += 1
        if probe and probe < n and lines[probe] == "---":
            f.add(1, "ERROR", "fm-not-first", "frontmatter starts on line %d. It must start on line 1: a blank line above the first --- makes the site ignore the whole block" % (probe + 1))
            start = probe
        else:
            f.add(0, "ERROR", "fm-missing", "no frontmatter block: every page starts with --- on line 1, then title, description and sidebar_position")
            return {}, 0, False
    end = None
    for i in range(start + 1, n):
        if lines[i].rstrip() == "---":
            end = i
            break
    if end is None:
        f.add(start + 1, "ERROR", "fm-unclosed", "the frontmatter is never closed with a second ---")
        return {}, n, False
    fields = {}
    i = start + 1
    while i < end:
        line = lines[i]
        if line.strip() == "" or line.lstrip().startswith("#"):
            i += 1
            continue
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:(.*)$", line)
        if not m:
            f.add(i + 1, "ERROR", "fm-yaml", "this line is not 'key: value'")
            i += 1
            continue
        key, raw = m.group(1), m.group(2)
        if key in fields:
            f.add(i + 1, "ERROR", "fm-yaml", "duplicate key %s" % key)
        j = i + 1
        cont = []
        while j < end and (lines[j].strip() == "" or lines[j][:1] in (" ", "\t") or lines[j].startswith("- ")):
            cont.append(lines[j])
            j += 1
        while cont and cont[-1].strip() == "":
            cont.pop()
        value, kind = scalar(raw, i + 1, f)
        multi = False
        if kind == "block":
            multi = True
            parts = [c.strip() for c in cont if c.strip()]
            value = " ".join(parts)
        elif kind in ("plain", "dq", "sq") and cont and key in ("title", "description"):
            multi = True
            value = (value + " " + " ".join(c.strip() for c in cont if c.strip())).strip()
        fields[key] = {"line": i + 1, "value": value, "kind": kind, "multi": multi, "raw": raw.strip()}
        i = j
    return fields, end + 1, True


# ---------------------------------------------------------------- markdown page
PLACEHOLDER_STRONG = re.compile(r"<<<|\[FILL IN\b|\bFILL-IN\b|REPLACE-WITH|\bTODO\b|\bTBD\b|\bFIXME\b")  # slop-lint:ignore
PLACEHOLDER_STRONG_ALWAYS = re.compile(r"<<<|\bFILL-IN\b|REPLACE-WITH")  # slop-lint:ignore
PLACEHOLDER_CI = re.compile(r"lorem ipsum|\[(?:link|url|insert[^\]]*)\](?!\()", re.I)
STUB_TEXT = re.compile(r"coming soon|under development|stay tuned", re.I)
NOINDEX = re.compile(r"""<meta\s+name=["']robots["']\s+content=["'][^"']*noindex""", re.I)
THROAT = re.compile(r"^(before (diving|we|you|getting|jumping)|welcome to|in this (guide|tutorial|section|page|article|document|chapter)|"
                    r"this (guide|tutorial|section|page|document|article|chapter) (will|walks|covers|explains|shows|describes|demonstrates)|let'?s )", re.I)
TEASER = re.compile(r"^(learn|discover|explore|find out|dive|welcome|get started|see how|join)\b", re.I)
NAMES = (
    ("name-moi-wallet", re.compile(r"\bMoi Wallet\b|\bMoiWallet\b"), "write MOI Wallet"),
    ("name-moi", re.compile(r"\bMoi\b(?! Wallet)"), "write MOI"),
    ("name-coco", re.compile(r"\bCoCo\b|\bCocoLang\b"), "write Coco, and Coco (also known as Cocolang) on first mention"),
    ("name-js-moi-sdk", re.compile(r"(?!js-moi-sdk\b)\b[Jj][Ss]-[Mm][Oo][Ii]-[Ss][Dd][Kk]\b"), "js-moi-sdk is always lowercase, even at the start of a sentence (rephrase the sentence)"),
    ("name-moipod", re.compile(r"\bMoipod\b"), "write MOIPod in prose (keep moipod in commands and package names)"),
    ("name-sarva-labs", re.compile(r"\bSarvaLabs\b|\bServal Labs\b"), "write Sarva Labs"),
)
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*:")
BARE_DOMAIN = re.compile(r"^(?:www\.)?[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:com|org|net|io|dev|ai|technology|xyz|co|app|gg|so|me|info|sh|tech|cloud|network)(?:[/?#:]|$)", re.I)
BARE_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$")
PRIVATE_REPO = re.compile(r"github\.com/sarvalabs/(?:go-moi|go-pisa|cocolang|moidocs|voyage-docs|coco-docs|voyage|voyage-api|moi-agent-launchpad|agent-explorer|moi-project)(?:[/?#)\s]|$)", re.I)
LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(\s*([^)\s]*)[^)]*\)")
IMAGE = re.compile(r"!\[([^\]]*)\]\(\s*([^)\s]*)[^)]*\)")
REFDEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(\S+)")
HREF = re.compile(r"""href=["']([^"']*)["']""")


def check_target(f, ln, target, site, facts=None):
    t = target.strip().strip("<>")
    if t == "":
        f.add(ln, "ERROR", "link-empty", "a link with no target")
        return
    if t.startswith("#"):
        return  # in-page anchors are checked once every heading is known
    if SCHEME.match(t):
        if t.lower().startswith("http://") and not re.match(r"http://(localhost|127\.0\.0\.1|\[::1\])", t, re.I):
            f.add(ln, "WARN", "link-http", "http link: use https (%s)" % mask(t)[:60])
        host = re.match(r"https?://([^/?#:]+)", t, re.I)
        if host and SITE_HOST.get(site) and host.group(1).lower() == SITE_HOST[site]:
            f.add(ln, "WARN", "link-absolute-internal", "link to this site by its full URL: write the /address instead, so a preview build stays on the preview (%s)" % mask(t)[:80])
        if PRIVATE_REPO.search(t + " "):
            f.add(ln, "WARN", "link-private-repo", "a private MOI repo: readers cannot open it (%s)" % mask(t)[:80])
        return
    if t.startswith(("/", "./", "../")):
        if site == "coco-docs" and t.startswith("/") and not t.startswith("//"):
            path = re.split(r"[?#]", t)[0]
            last = path.rstrip("/").rsplit("/", 1)[-1]
            mode = (facts or {}).get("coco_routes")
            if mode == "docs" and (path == "/book" or path.startswith("/book/")):
                f.add(ln, "WARN", "link-route-prefix", "this checkout serves the Book under /docs/book/ (routeBasePath '/' is on PR #12 only), so a /book/ link has no route and the build stops (inferred, not built): %s" % mask(t)[:70])
            elif mode == "root" and (path == "/docs/book" or path.startswith("/docs/book/")):
                f.add(ln, "WARN", "link-route-prefix", "this checkout serves the Book at /book/ (routeBasePath '/'); /docs/book/ only works through a redirect: %s" % mask(t)[:70])
            elif mode != "docs" and path != "/" and not path.endswith("/") and "." not in last:
                f.add(ln, "WARN", "link-form", "coco-docs page addresses end with a slash: %s" % mask(t)[:80])
        return
    if BARE_DOMAIN.match(t) or BARE_EMAIL.match(t):
        if BARE_EMAIL.match(t):
            f.add(ln, "ERROR", "link-no-scheme", "an email address needs mailto: in front, or the browser reads it as a path on this site (%s)" % mask(t)[:80])
        else:
            f.add(ln, "ERROR", "link-no-scheme", "no scheme, so the browser reads this as a path on this site: write https://%s" % mask(t)[:80])


def lint_markdown(text, path, site, f, opts):
    raw_lines = text.split("\n")
    if text.endswith("\n"):
        raw_lines = raw_lines[:-1]
    crlf = any(l.endswith("\r") for l in raw_lines)
    lines = [l.rstrip("\r") for l in raw_lines]
    if crlf:
        f.add(0, "WARN", "crlf", "CRLF line endings. scripts/generate-llms.mjs of moidocs and voyage-docs reads the frontmatter with an LF-only pattern, so title and description may be missing from llms.txt (inferred from the pattern)")
    if lines and lines[0].startswith(BOM):
        f.add(1, "ERROR", "fm-bom", "the file starts with a byte order mark; save it as plain UTF-8 so line 1 is ---")
        lines[0] = lines[0].lstrip(BOM)
    n_before = len(f.items)
    fields, body_start, fm_ok = parse_frontmatter(lines, f)
    yaml_bad = {it[0] for it in f.items[n_before:] if it[2] == "fm-yaml"}
    inside, unclosed = find_fences(lines)
    for opener in unclosed:
        f.add(opener, "ERROR", "fence-unclosed", "code fence opened here is never closed; the lines after it were checked as normal text")
    stem = path.stem
    is_index = stem.lower() in ("index", "readme")
    facts = repo_facts(path)

    # ---- frontmatter fields
    title = fields.get("title")
    desc = fields.get("description")
    unlisted = fields.get("unlisted", {}).get("value", "").lower() == "true"
    body_text = "\n".join(lines[body_start:])
    marked_noindex = bool(NOINDEX.search(body_text)) or unlisted
    stub_text = STUB_TEXT.search(prose_of(lines, body_start, inside))
    if fm_ok:
        if title is None or not title["value"].strip():
            f.add(0, "ERROR", "title-missing", "no title in the frontmatter")
        else:
            tv = title["value"].strip()
            shown = tv
            if site == "coco-docs":
                shown = re.sub(r"^\d+(?:\.\d+)*\s+", "", tv)  # the Book numbers its chapters in the title
            if len(tv) > TITLE_MAX:
                f.add(title["line"], "WARN", "title-long", "title is %d characters; search results cut near 60" % len(tv))
            if re.search(r"\bv\d+(?:\.\d+)*\b|\b\d+\.\d+\.\d+\b|\b(?:19|20)\d\d\b", shown):
                f.add(title["line"], "WARN", "title-version", "no version number or date in a title unless the page is a changelog entry (%s)" % mask(tv)[:60])
            if "|" in tv or re.search(r"MOI Documentation", tv):
                f.add(title["line"], "WARN", "title-site-name", "the site appends its own name; leave it out of the title")
        if desc is None or not desc["value"].strip():
            f.add(0, "ERROR", "description-missing", "no description in the frontmatter")
        else:
            dv = desc["value"].strip()
            n = len(dv)
            if desc["line"] in yaml_bad:
                pass  # the value could not be read, so its length means nothing
            elif n < DESC_MIN or n > DESC_MAX:
                f.add(desc["line"], "WARN", "description-length", "description is %d characters; aim for 140 to 160, 130 to 170 is accepted, and a few characters outside is fine if it reads well" % n)
            if desc["multi"]:
                f.add(desc["line"], "WARN", "description-multiline", "description spans several lines; scripts/generate-llms.mjs reads one line (inferred from its pattern)")
            if desc["line"] not in yaml_bad and (TEASER.match(dv) or dv.endswith(("...", "?"))):
                f.add(desc["line"], "WARN", "description-teaser", "write a statement of what the page covers, not a teaser (%s)" % mask(dv)[:50])
            if title and dv.lower() == title["value"].strip().lower():
                f.add(desc["line"], "WARN", "description-same-as-title", "the description repeats the title")
        sp = fields.get("sidebar_position")
        if sp is None:
            f.add(0, "WARN" if is_index else "ERROR", "sidebar-position-missing",
                  "no sidebar_position; the order falls back to the file name" + (" (an index page: its _category_.json may order it)" if is_index else ""))
        elif not re.fullmatch(r"-?\d+(\.\d+)?", sp["value"].strip()):
            f.add(sp["line"], "WARN", "sidebar-position-value", "sidebar_position should be a number")
        img = fields.get("image")
        if site == "moidocs":
            p = "/" + str(path).replace("\\", "/")
            section = next((s for s in IMAGE_CARD if re.search(r"/docs/%s/" % s, p)), None)
            if section:
                want = IMAGE_CARD[section]
                if facts is not None and not facts["cards"]:
                    if img is not None:
                        f.add(img["line"], "WARN", "image-card-missing",
                              "this checkout has no section cards in static/img (they are on PR #124 only), so the image does not exist yet; leave image out until it merges")
                elif img is None or img["value"].strip() != want:
                    f.add(img["line"] if img else 0, "WARN" if marked_noindex else "ERROR", "image-wrong",
                          "moidocs pages under docs/%s/ carry image: %s" % (section, want))
        elif site in ("voyage-docs", "coco-docs") and img is not None:
            f.add(img["line"], "WARN", "image-extra", "%s leaves the image field out" % site)

    # ---- stub marking
    words = len(re.findall(r"\w+", prose_of(lines, body_start, inside)))
    if stub_text and not marked_noindex:
        if words < 200:
            f.add(0, "ERROR", "stub-unmarked", "a page of %d words says '%s' but carries no noindex block or unlisted: true. An unmarked stub reaches the sitemap" % (words, stub_text.group(0).lower()))
        else:
            f.add(0, "WARN", "stub-text", "the page says '%s'. If a whole section is a placeholder, the page is a stub: mark it" % stub_text.group(0).lower())
    if marked_noindex and not stub_text and words >= 150:
        f.add(0, "WARN", "stub-marked-finished", "the page is marked as a stub but has %d words and no 'coming soon' text. If it is finished, remove the mark in this change" % words)
    if site == "coco-docs" and NOINDEX.search(body_text):
        f.add(0, "WARN", "stub-wrong-marker", "coco-docs marks a stub with unlisted: true in the frontmatter")
    if site in ("moidocs", "voyage-docs") and unlisted:
        f.add(fields["unlisted"]["line"], "WARN", "stub-wrong-marker", "%s marks a stub with the noindex block after the frontmatter" % site)

    # ---- walk the body
    heads = []          # (line, level, text)
    in_head_block = False
    schema_calls = {}   # name -> first line
    imported = set()
    anchors = set()
    for idx in range(0, len(lines)):
        ln = idx + 1
        line = lines[idx]
        if IGNORE.search(line):
            continue
        if EM_DASH in line or ENTITY_DASH.search(line):
            f.add(ln, "ERROR", "em-dash", "em dash: use a comma, a colon or a full stop")
        if idx < body_start:
            # frontmatter text is public too: the secret, phrase and path rules apply, as do the naming and placeholder rules
            # (the keywords list is exempt from names)
            for rx in SECRET_SHAPES[:-1]:
                if rx.search(line):
                    f.add(ln, "ERROR", "secret-shaped", "something here is shaped like a key or token (%s). Remove it; never publish one" % mask(line.strip())[:80])
                    break
            for a, b in phrase_spans(line):
                f.add(ln, "WARN", "recovery-phrase-shaped", "%d or more short words in a row, the shape of a recovery phrase. A documented sample is acceptable; a real phrase never is" % PHRASE_MIN)
                break
            if LOCAL_PATH.search(line):
                f.add(ln, "WARN", "local-path", "a path from someone's own machine")
            if re.match(r"^(title|description)\s*:", line):
                for rid, rx, msg in NAMES:
                    if rx.search(prose_view(line)):
                        f.add(ln, "ERROR", rid, msg)
            if PLACEHOLDER_STRONG.search(line) or PLACEHOLDER_STRONG_ALWAYS.search(line):
                f.add(ln, "ERROR", "placeholder", "placeholder text must not ship (FILL-IN, REPLACE-WITH, TODO, TBD, FIXME, lorem ipsum, [link])")  # slop-lint:ignore
            continue
        in_fence = ln in inside
        # secrets apply everywhere, fenced code included
        for rx in SECRET_SHAPES[:-1]:
            if rx.search(line):
                f.add(ln, "ERROR", "secret-shaped", "something here is shaped like a key or token (%s). Remove it; never publish one" % mask(line.strip())[:80])
                break
        for a, b in phrase_spans(line):
            f.add(ln, "WARN", "recovery-phrase-shaped", "%d or more short words in a row, the shape of a recovery phrase. A documented sample is acceptable; a real phrase never is" % PHRASE_MIN)
            break
        if LOCAL_PATH.search(line):
            f.add(ln, "WARN", "local-path", "a path from someone's own machine")
        if PLACEHOLDER_STRONG_ALWAYS.search(line) or (not in_fence and (PLACEHOLDER_STRONG.search(line) or PLACEHOLDER_CI.search(line))):
            f.add(ln, "ERROR", "placeholder", "placeholder text must not ship (FILL-IN, REPLACE-WITH, TODO, TBD, FIXME, lorem ipsum, [link])")  # slop-lint:ignore
        if in_fence:
            continue
        stripped = line.strip()
        if stripped.startswith("<head"):
            in_head_block = True
        if in_head_block:
            if "</head>" in stripped:
                in_head_block = False
            continue
        m = re.match(r"^import\s+(\w+)\s+from\s+['\"]@site/src/components/(\w+)['\"]", stripped)
        if m:
            imported.add(m.group(1))
        m = re.match(r"^import\s+\{\s*([^}]*)\}\s+from", stripped)
        if m:
            imported.update(x.strip() for x in m.group(1).split(",") if x.strip())
        for sname in ("HowToSchema", "FaqSchema"):
            if re.match(r"^<%s\b" % sname, stripped):
                schema_calls.setdefault(sname, ln)
        hm = HEADING.match(line)
        if hm:
            heads.append((ln, len(hm.group(1)), hm.group(2)))
            anchors.add(slugify(hm.group(2)))
            if not hm.group(2).strip():
                continue
        for mm in re.finditer(r"""\b(?:id|name)=["']([^"']+)["']""", line):
            anchors.add(mm.group(1))
        view = prose_view(line)
        for rid, rx, msg in NAMES:
            if rx.search(view):
                f.add(ln, "ERROR", rid, msg)
        if site == "moidocs" and re.search(r"\bLaunchpad\b", view):
            f.add(ln, "WARN", "application-docs", "moidocs holds protocol docs. Launchpad is an application: its docs belong with the app, and a backlink is fine (Rahul, 2026-09-17)")
        for mm in LINK.finditer(line):
            check_target(f, ln, mm.group(1), site, facts)
        for mm in IMAGE.finditer(line):
            if not mm.group(1).strip():
                f.add(ln, "WARN", "image-alt", "image without alt text")
            check_target(f, ln, mm.group(2), site, facts)
        rd = REFDEF.match(line)
        if rd:
            check_target(f, ln, rd.group(1), site, facts)
        for mm in HREF.finditer(line):
            check_target(f, ln, mm.group(1), site, facts)

    # in-page anchors need every heading first
    for idx in range(body_start, len(lines)):
        ln = idx + 1
        if ln in inside or IGNORE.search(lines[idx]):
            continue
        for mm in LINK.finditer(lines[idx]):
            t = mm.group(1).strip()
            if t.startswith("#") and len(t) > 1 and t[1:] not in anchors:
                f.add(ln, "WARN", "link-anchor-missing", "no heading on this page produces the anchor %s (the slug is approximate; confirm in a build)" % mask(t))

    # ---- headings
    h1 = [h for h in heads if h[1] == 1]
    if len(h1) > 1:
        f.add(h1[1][0], "ERROR", "h1-multiple", "a page has one main title; this is a second # heading")
    if h1 and schema_calls and site == "moidocs":
        f.add(h1[0][0], "ERROR", "h1-with-schema", "a # heading next to a HowToSchema or FaqSchema call shows two titles; let the frontmatter title be the only one")
    if h1 and site == "voyage-docs":
        f.add(h1[0][0], "WARN", "h1-voyage", "voyage-docs pages leave the # heading out; the site shows the frontmatter title")
    prev = 1  # the page title counts as level 1
    for ln, level, _ in heads:
        if level == 1:
            prev = 1
            continue
        if level > prev + 1:
            f.add(ln, "WARN", "heading-skip", "heading level jumps from %d to %d" % (prev, level))
        prev = level

    # ---- schema components
    for sname, first in schema_calls.items():
        if site in ("voyage-docs", "coco-docs"):
            f.add(first, "ERROR", "schema-wrong-site", "%s exists on moidocs only; write a FAQ or tutorial as an ordinary page here" % sname)
        elif sname not in imported:
            f.add(first, "ERROR", "schema-no-import", "%s is used but not imported: import %s from '@site/src/components/%s';" % (sname, sname, sname))
        elif facts is not None and not facts["schema"].get(sname, True):
            f.add(first, "ERROR", "schema-component-missing", "this checkout has no src/components/%s (it is on PR #124 only), so the import cannot resolve and the build fails. Write the page without it until the PR merges" % sname)
        end = first
        while end <= len(lines) and "/>" not in lines[end - 1]:
            end += 1
        for k in range(first, min(end, len(lines))):
            if lines[k].strip() == "" and k < end:
                f.add(k + 1, "ERROR", "schema-blank-line", "a blank line inside the %s call; every line of it needs content" % sname)
                break
    if len(schema_calls) == 2:
        f.add(0, "WARN", "schema-both", "both HowToSchema and FaqSchema on one page")
    pp = "/" + str(path).replace("\\", "/")
    if site == "moidocs":
        have_howto = facts is None or facts["schema"].get("HowToSchema", True)
        have_faq = facts is None or facts["schema"].get("FaqSchema", True)
        if have_howto and "/tutorials/" in pp and not is_index and "HowToSchema" not in schema_calls and not marked_noindex:
            f.add(0, "WARN", "tutorial-no-howto", "a tutorial walks through actions in order: add a HowToSchema call (see templates/page-moidocs-tutorial.md)")
        if have_faq and "faq" in stem.lower() and "FaqSchema" not in schema_calls:
            f.add(0, "WARN", "faq-no-schema", "an FAQ page carries a FaqSchema call (see templates/page-moidocs-faq.md)")

    # ---- the opening paragraph
    if not marked_noindex or not stub_text:
        check_opening(lines, body_start, inside, f)
    return fields


def prose_of(lines, start, inside):
    out = []
    for i in range(start, len(lines)):
        if (i + 1) in inside:
            continue
        s = lines[i].strip()
        if s.startswith("import ") or s.startswith("export "):
            continue
        out.append(lines[i])
    return "\n".join(out)


def check_opening(lines, start, inside, f):
    i, n = start, len(lines)
    skipping_head = False
    while i < n:
        ln = i + 1
        s = lines[i].strip()
        if ln in inside or FENCE_OPEN.match(lines[i]):
            f.add(ln, "WARN", "opening-missing", "the page opens with a code block; say what the thing is first")
            return
        if s == "":
            i += 1
            continue
        if s.startswith("<head"):
            skipping_head = "</head>" not in s
            i += 1
            while skipping_head and i < n:
                if "</head>" in lines[i]:
                    skipping_head = False
                i += 1
            continue
        if s.startswith(("import ", "export ")):
            i += 1
            continue
        if re.match(r"<(?:HowToSchema|FaqSchema)\b", s):
            while i < n and "/>" not in lines[i]:
                i += 1
            i += 1
            continue
        if re.match(r"<[A-Z]\w*", s):
            return  # another component first: not judged
        if s.startswith(":::"):
            return  # an admonition first: a stub or a notice, not judged
        hm = HEADING.match(lines[i])
        if hm:
            if len(hm.group(1)) == 1:
                i += 1
                continue
            f.add(ln, "WARN", "opening-missing", "the page goes to a heading ('%s') before any opening paragraph that says what the thing is" % mask(hm.group(2))[:50])
            return
        if re.match(r"^([-*+]|\d+[.)])\s", s) or s.startswith("|") or s.startswith(">"):
            f.add(ln, "WARN", "opening-missing", "the page opens with a list, table or quote; start with a paragraph that says what the thing is")
            return
        para = [s]
        j = i + 1
        while j < n and lines[j].strip() != "" and not HEADING.match(lines[j]) and not FENCE_OPEN.match(lines[j]):
            para.append(lines[j].strip())
            j += 1
        text = " ".join(para)
        if THROAT.match(text):
            f.add(ln, "WARN", "opening-throat", "the opening paragraph talks about the page before it says what the thing is (%s). Say what it is first (heuristic)" % mask(text)[:60])
        elif len(text.split()) < 6:
            f.add(ln, "WARN", "opening-short", "the opening paragraph is %d words" % len(text.split()))
        return


# ---------------------------------------------------------------- Sphinx page
def lint_rst(text, path, f, opts):
    lines = text.replace("\r\n", "\n").split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    # meta description
    desc, desc_line = None, 0
    for i, l in enumerate(lines):
        if re.match(r"^\.\.\s+meta::\s*$", l):
            j = i + 1
            while j < len(lines) and (lines[j].strip() == "" or lines[j].startswith(" ")):
                md = re.match(r"^\s+:description:\s*(.*)$", lines[j])
                if md:
                    desc, desc_line = md.group(1).strip(), j + 1
                    k = j + 1
                    while k < len(lines) and lines[k].startswith("      ") and not re.match(r"^\s+:\w", lines[k]):
                        desc += " " + lines[k].strip()
                        k += 1
                    break
                j += 1
            break
    if not desc:
        f.add(0, "ERROR", "meta-description-missing", "no '.. meta::' block with ':description:' at the top of the page")
    elif len(desc) < DESC_MIN or len(desc) > DESC_MAX:
        f.add(desc_line, "WARN", "description-length", "description is %d characters; aim for 140 to 160, 130 to 170 is accepted" % len(desc))
    if desc and TEASER.match(desc):
        f.add(desc_line, "WARN", "description-teaser", "write a statement of what the page covers, not a teaser")

    # code regions (literal blocks) are not prose
    code = set()
    base = None
    for i, l in enumerate(lines):
        s = l.strip()
        if base is not None:
            if s == "" or (len(l) - len(l.lstrip())) > base:
                code.add(i + 1)
                continue
            base = None
        if re.match(r"^\s*\.\.\s+(code-block|code|sourcecode|literalinclude|highlight)::", l) or (s.endswith("::") and not s.startswith("..") and len(s) > 2) or s == "::":
            base = len(l) - len(l.lstrip())
    # section titles
    adorn = re.compile(r"^([=\-~`#\"'^_*+<>.:])\1{2,}\s*$")
    titles = []  # (line, text, style)
    i = 0
    while i < len(lines):
        l = lines[i]
        if (i + 1) in code or l.startswith(" "):
            i += 1
            continue
        if adorn.match(l) and i + 2 < len(lines) and lines[i + 1].strip() and not adorn.match(lines[i + 1]) and adorn.match(lines[i + 2]) and lines[i + 2][0] == l[0]:
            text_line = lines[i + 1].strip()
            if len(lines[i + 2].rstrip()) < len(text_line) or len(l.rstrip()) < len(text_line):
                f.add(i + 2, "ERROR", "rst-underline-short", "the title adornment is shorter than the title")
            titles.append((i + 2, text_line, (l[0], True)))
            i += 3
            continue
        if l.strip() and not adorn.match(l) and i + 1 < len(lines) and adorn.match(lines[i + 1]):
            if len(lines[i + 1].rstrip()) < len(l.strip()):
                f.add(i + 2, "ERROR", "rst-underline-short", "the title underline is shorter than the title (Sphinx warns)")
            titles.append((i + 1, l.strip(), (lines[i + 1][0], False)))
            i += 2
            continue
        i += 1
    if not titles:
        f.add(0, "ERROR", "rst-title-missing", "no section title found")
    else:
        top = titles[0][2]
        tops = [t for t in titles if t[2] == top]
        if len(tops) > 1:
            f.add(tops[1][0], "ERROR", "rst-title-multiple", "a page has one main title; '%s' repeats the top-level style" % mask(tops[1][1])[:40])

    for idx, line in enumerate(lines):
        ln = idx + 1
        if IGNORE.search(line):
            continue
        if EM_DASH in line or ENTITY_DASH.search(line):
            f.add(ln, "ERROR", "em-dash", "em dash: use a comma, a colon or a full stop")
        for rx in SECRET_SHAPES[:-1]:
            if rx.search(line):
                f.add(ln, "ERROR", "secret-shaped", "something here is shaped like a key or token (%s). Remove it" % mask(line.strip())[:80])
                break
        for a, b in phrase_spans(line):
            f.add(ln, "WARN", "recovery-phrase-shaped", "%d or more short words in a row, the shape of a recovery phrase. A documented sample is acceptable; a real phrase never is" % PHRASE_MIN)
            break
        if LOCAL_PATH.search(line):
            f.add(ln, "WARN", "local-path", "a path from someone's own machine")
        if PLACEHOLDER_STRONG_ALWAYS.search(line) or (ln not in code and (PLACEHOLDER_STRONG.search(line) or PLACEHOLDER_CI.search(line))):
            f.add(ln, "ERROR", "placeholder", "placeholder text must not ship (FILL-IN, REPLACE-WITH, TODO, TBD, FIXME, lorem ipsum)")  # slop-lint:ignore
        if ln in code:
            continue
        view = re.sub(r"``[^`]*``", lambda m: " " * len(m.group(0)), line)
        view = re.sub(r"<[^>]*>", " ", view)
        view = re.sub(r"https?://\S+", " ", view)
        for rid, rx, msg in NAMES:
            if rx.search(view):
                f.add(ln, "ERROR", rid, msg)
        for mm in re.finditer(r"`[^`<]*<([^>`]+)>`__?", line):
            tgt = mm.group(1).strip()
            if SCHEME.match(tgt):
                if tgt.lower().startswith("http://") and not re.match(r"http://(localhost|127\.0\.0\.1)", tgt, re.I):
                    f.add(ln, "WARN", "link-http", "http link: use https")
                if PRIVATE_REPO.search(tgt + " "):
                    f.add(ln, "WARN", "link-private-repo", "a private MOI repo: readers cannot open it")
            elif BARE_DOMAIN.match(tgt) or BARE_EMAIL.match(tgt):
                f.add(ln, "ERROR", "link-no-scheme", "no scheme: write https://%s (mailto: in front of an address)" % mask(tgt)[:80])

    # toctree, PAGES row, sitemap
    stem = path.stem
    d = path.parent
    index = d / "index.rst"
    if stem != "index" and index.is_file() and not is_env_file(index):
        try:
            itext = index.read_text(encoding="utf-8", errors="replace")
        except OSError:
            itext = ""
        if "toctree::" in itext and not any(l.strip() == stem or l.strip().endswith("<%s>" % stem) for l in itext.split("\n")):
            f.add(0, "ERROR", "toctree-missing", "'%s' is not listed in index.rst, so the page builds but nothing links to it" % stem)
    if d.name == "source":
        gen = d.parent / "generate_llms.py"
        if gen.is_file() and not is_env_file(gen):
            try:
                gtext = gen.read_text(encoding="utf-8", errors="replace")
            except OSError:
                gtext = ""
            m = re.search(r'^\s*"%s":\s*\(\s*"((?:[^"\\]|\\.)*)"\s*,\s*"((?:[^"\\]|\\.)*)"\s*\)' % re.escape(stem), gtext, re.M)
            if not m:
                f.add(0, "ERROR", "sdk-pages-row-missing", "no row for '%s' in the PAGES table of docs/generate_llms.py" % stem)
            elif desc and m.group(2).replace('\\"', '"') != desc:
                f.add(0, "ERROR", "sdk-pages-desc-mismatch", "the description differs from the PAGES row of docs/generate_llms.py. They are checked by eye only")
        sm = d / "_extra" / "sitemap.xml"
        if sm.is_file() and not is_env_file(sm):
            try:
                stext = sm.read_text(encoding="utf-8", errors="replace")
            except OSError:
                stext = ""
            locs = [re.sub(r"^https?://[^/]+/?", "", loc).strip("/") for loc in re.findall(r"<loc>([^<]*)</loc>", stext)]
            want = "" if stem == "index" else stem
            if want not in locs:
                f.add(0, "ERROR", "sdk-sitemap-missing", "the page is not in docs/source/_extra/sitemap.xml, which is kept by hand")
    return {"description": {"value": desc or "", "line": desc_line}, "title": {"value": titles[0][1] if titles else "", "line": titles[0][0] if titles else 0}}


def lint_category(text, path, f):
    try:
        data = json.loads(text)
    except ValueError as e:
        f.add(0, "ERROR", "category-json", "not valid JSON: %s" % str(e)[:80])
        return {}
    link = data.get("link") if isinstance(data, dict) else None
    if isinstance(link, dict) and link.get("type") == "generated-index":
        d = link.get("description")
        if not d:
            f.add(0, "WARN", "category-description", "a generated-index category carries a description")
        else:
            if len(d) < DESC_MIN or len(d) > DESC_MAX:
                f.add(0, "WARN", "category-description", "description is %d characters; the existing categories are 143 to 150" % len(d))
            if EM_DASH in d:
                f.add(0, "ERROR", "em-dash", "em dash: use a comma, a colon or a full stop")
    return {}


# ---------------------------------------------------------------- slop-lint
def find_slop_lint():
    cands = []
    if os.environ.get("SKILLS"):
        cands.append(Path(os.environ["SKILLS"]) / "moi-devrel" / "scripts" / "slop-lint.sh")
    cands.append(Path(__file__).resolve().parents[2] / "moi-devrel" / "scripts" / "slop-lint.sh")
    for c in cands:
        if c.is_file():
            return c
    return None


SKIP_SLOP = {"em-dash", "coco-name", "moipod-caps", "js-moi-sdk-case", "sarvalabs-one-word", "serval-labs", "placeholder", "unclosed-fence", "ai-attribution"}


def run_slop(path, slop, f):
    try:
        r = subprocess.run(["bash", str(slop), str(path)], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise InputError("could not run slop-lint.sh: %s" % e)
    if r.returncode == 2:
        raise InputError("slop-lint.sh could not read %s" % path)
    for out in r.stdout.splitlines():
        m = re.match(r"^.*?:(\d+):([A-Za-z0-9-]+)(\(warn\))?:(.*)$", out)
        if not m or m.group(2) in SKIP_SLOP:
            continue
        f.add(int(m.group(1)), "WARN" if m.group(3) else "ERROR", "slop-lint/" + m.group(2), m.group(4).strip())


# ---------------------------------------------------------------- git
def run_git(d, args):
    try:
        r = subprocess.run(["git", "-C", str(d)] + args, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise InputError("git could not run: %s" % e)
    return r


def git_added(path, ref):
    """Return (set of added line numbers or None for all, list of removed lines)."""
    if ref.startswith("-"):
        raise InputError("--added-lines-since: %r is not a commit; a ref cannot start with a dash" % ref)
    d = path.resolve().parent
    name = path.name
    if run_git(d, ["rev-parse", "--verify", "--quiet", ref + "^{commit}"]).returncode != 0:
        raise InputError("--added-lines-since: %r is not a commit in the repo that holds %s" % (ref, path))
    if run_git(d, ["ls-files", "--error-unmatch", "--", name]).returncode != 0:
        return None, []
    r = run_git(d, ["diff", "--no-color", "--no-ext-diff", "-U0", ref, "--", name])
    if r.returncode != 0:
        raise InputError("git diff failed for %s: %s" % (path, r.stderr.strip()[:100]))
    added, removed, cur = set(), [], None
    for l in r.stdout.splitlines():
        m = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", l)
        if m:
            cur = int(m.group(1))
            continue
        if cur is None or l.startswith(("+++", "---")):
            continue
        if l.startswith("+"):
            added.add(cur)
            cur += 1
        elif l.startswith("-"):
            removed.append(l[1:])
    return added, removed


# ---------------------------------------------------------------- driver
def expand(args):
    files = []
    for a in args:
        p = Path(a)
        if not p.exists():
            raise InputError("no such file or folder: %s" % a)
        if p.is_dir():
            for root, dirs, names in os.walk(str(p)):
                dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS and not x.startswith("_") and not env_name(x)
                                 and not is_build_output(Path(root) / x))
                for nme in sorted(names):
                    q = Path(root) / nme
                    if nme == "_category_.json" or (q.suffix.lower() in PAGE_EXT and not nme.startswith("_")):
                        files.append(q)
        else:
            files.append(p)
    return files


def is_build_output(d):
    """A folder named build is skipped only when it holds site output. docs/build is a real section of moidocs."""
    return d.name == "build" and any((d / marker).exists() for marker in ("index.html", "html", "sitemap.xml", "llms.txt"))


def read_page(p):
    if is_env_file(p):
        if env_name(p.name):
            raise InputError("refusing to read %s: an env file can hold keys and is never opened" % p.name)
        raise InputError("refusing to read %s: it sits in an env-named folder, and an env file can hold keys" % p.name)
    if not p.is_file():
        raise InputError("not a file: %s" % p)
    if p.name != "_category_.json" and p.suffix.lower() not in PAGE_EXT:
        raise InputError("%s is not a page: the lint reads .md, .mdx, .rst and _category_.json" % p.name)
    try:
        raw = p.read_bytes()
    except OSError as e:
        raise InputError("cannot read %s: %s" % (p, e.strerror or e))
    if len(raw) > MAX_BYTES:
        raise InputError("%s is %d bytes: too large to be a page" % (p.name, len(raw)))
    if b"\x00" in raw[:4096]:
        raise InputError("%s looks like a binary file" % p.name)
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as e:
        raise InputError("%s is not UTF-8 text: %s" % (p.name, e))


def main(argv):
    ap = argparse.ArgumentParser(prog="docs-page-lint.py", description="Check pages of MOI's docs sites against references/page-standard.md.",
                                 epilog="Exit 0 no error, 1 at least one error, 2 usage error or unreadable input.")
    ap.add_argument("pages", nargs="*")
    ap.add_argument("--site", choices=["moidocs", "voyage-docs", "coco-docs", "generic"])
    ap.add_argument("--added-lines-since", metavar="REF")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--no-slop-lint", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--list-rules", action="store_true")
    try:
        args = ap.parse_args(argv[1:])
    except SystemExit as e:
        return 2 if e.code not in (0, None) else 0
    if args.list_rules:
        for rid, (level, src, msg) in RULES.items():
            print("%-26s %-13s %-22s %s" % (rid, level, src, msg))
        return 0
    if not args.pages:
        ap.print_usage(sys.stderr)
        print("docs-page-lint: give at least one page or folder", file=sys.stderr)
        return 2
    slop = None
    if not args.no_slop_lint:
        slop = find_slop_lint()
        if slop is None:
            print("docs-page-lint: moi-devrel/scripts/slop-lint.sh was not found, so the phrasing rules would be skipped. "
                  "Set SKILLS to the folder that holds the moi-* skills, or pass --no-slop-lint to skip them on purpose", file=sys.stderr)
            return 2
    try:
        files = expand(args.pages)
    except InputError as e:
        print("docs-page-lint: %s" % e, file=sys.stderr)
        return 2
    if not files:
        print("docs-page-lint: no .md, .mdx, .rst or _category_.json file found in %s" % ", ".join(args.pages), file=sys.stderr)
        return 2
    errors = warns = 0
    bad_input = False
    titles, descs = {}, {}
    for p in files:
        try:
            text = read_page(p)
            site = detect_site(p, args.site)
            f = Findings()
            if p.name == "_category_.json":
                fields = lint_category(text, p, f)
            elif p.suffix.lower() == ".rst":
                fields = lint_rst(text, p, f, args)
            else:
                fields = lint_markdown(text, p, site, f, args)
            if slop and p.name != "_category_.json":
                run_slop(p, slop, f)
            added = None
            if args.added_lines_since:
                added, removed = git_added(p, args.added_lines_since)
                if p.suffix.lower() in (".md", ".mdx"):
                    now = set()
                    for l in text.replace("\r", "").split("\n"):
                        hm = HEADING.match(l)
                        if hm:
                            now.add(slugify(hm.group(2)))
                    for old in removed:
                        hm = HEADING.match(old)
                        if hm and slugify(hm.group(2)) and slugify(hm.group(2)) not in now:
                            old_slug = slugify(hm.group(2))
                            shown_old = EXPLICIT_ID.sub("", hm.group(2)).strip()
                            f.add(0, "WARN", "anchor-lost", "the heading '%s' changed or went, and the anchor #%s no longer exists. Keep it with {#%s} after the new heading text, or update every link first (the slug is approximate; confirm in a build)" % (mask(shown_old)[:50], mask(old_slug)[:50], mask(old_slug)[:50]))
            if args.verbose:
                print("docs-page-lint: %s checked as %s" % (p, "sphinx" if p.suffix.lower() == ".rst" else site), file=sys.stderr)
            for key, store in (("title", titles), ("description", descs)):
                v = (fields.get(key) or {}).get("value", "").strip().lower() if fields else ""
                if v:
                    store.setdefault(v, []).append(str(p))
            shown = set()
            for line, level, rule, msg in sorted(f.items, key=lambda x: (x[0], x[2])):
                if added is not None and line != 0 and line not in added:
                    continue
                if args.strict and level == "WARN":
                    level = "ERROR"
                key = (line, rule, msg)
                if key in shown:
                    continue
                shown.add(key)
                print("%s:%d:%s:%s: %s" % (p, line, level, rule, mask(msg)))
                if level == "ERROR":
                    errors += 1
                else:
                    warns += 1
        except InputError as e:
            print("docs-page-lint: %s" % e, file=sys.stderr)
            bad_input = True
    for label, store in (("duplicate-title", titles), ("duplicate-description", descs)):
        for v, paths in store.items():
            if len(paths) > 1:
                level = "ERROR" if args.strict else "WARN"
                print("%s:0:%s:%s: the same %s as %s" % (paths[1], level, label, label.split("-")[1], paths[0]))
                if args.strict:
                    errors += 1
                else:
                    warns += 1
    print("docs-page-lint: %d error(s), %d warning(s) in %d file(s)" % (errors, warns, len(files)), file=sys.stderr)
    if bad_input:
        return 2
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except BrokenPipeError:
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as exc:  # a bug must never print a traceback that could quote a page
        print("docs-page-lint: internal error (%s). Re-run with one file to find the page; this is a bug in the lint" % type(exc).__name__, file=sys.stderr)
        sys.exit(2)
