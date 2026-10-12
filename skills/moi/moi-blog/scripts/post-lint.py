#!/usr/bin/env python3
"""post-lint.py: check one MOI blog post before it goes into a pull request.

Usage (SKILLS is the folder that holds the moi-* skills; run from the working copy of sarvalabs/MOI-Website):
    python3 "$SKILLS/moi-blog/scripts/post-lint.py" [options] blog/src/content/posts/<slug>.md

Options:
    --repo DIR        working copy of sarvalabs/MOI-Website. Needed to check images, the cover and sibling
                      post links when the file is not already under blog/src/content/posts/. If the file is
                      under that path, or the current folder holds it, the repo is found without this flag.
    --strict          turn the title and summary length warnings into errors
    --no-slop-lint    do not call moi-devrel's slop-lint.sh. Without this flag a missing slop-lint.sh is an
                      error, so the phrasing rules can never be skipped by accident.
    --verbose         also print INFO lines
    --today YYYY-MM-DD  the date to compare `date` with (default: today, UTC)

What it checks (the contract is blog/src/content.config.ts on main as of 2026-10-02, plus the corpus conventions):
    frontmatter   title, summary and date present; date valid; author an object with a name and an https url;
                  tags are lowercase slugs; takeaways 8 or none; faq entries have q and a; cover files exist;
                  unquoted colons (YAML fails the build); fields the build ignores (description, authorRole, slug)
    lengths       title over 60 characters and summary outside 130 to 170 (WARN; ERROR with --strict). The numbers
                  come from the docs standard, because no limit is recorded for the blog itself
    headings      no H1 in the body (the title is the H1), start at H2, no skipped level, no duplicate H2
    links         no scheme (a bare domain becomes a broken relative link), root-relative, relative file links,
                  http, generic link text, private repo links, UTM tags in the body, in-page anchors
    images        the file exists, alt text present, lives under ../../assets/
    text          em dash (also as an entity), HTML comments, placeholders ([FILL IN, <<<, TODO, {{x}} and the
                  other tokens; {{x}} is allowed in fenced code and in inline code), stray <Subscribe />, local paths
    phrasing      moi-devrel's slop-lint.sh (retired terms, contrast frames, 12:00 AM UTC and the rest)  # slop-lint:ignore
    emoji         an emoji or pictograph anywhere in the file (WARN)

Output: <file>:<line>:<LEVEL>:<rule>: <message>, then a summary on stderr. A message that quotes a value from the
file (a tag, a date, a link) has anything shaped like a key, a token or a webhook, every query value in a URL and every
long unbroken letter-and-digit run replaced by <masked>, so the lint never echoes a secret that sits in a post.
It refuses an env file (.env, .env.*, *.env, .envrc): those can hold keys and are never opened.
Exit codes: 0 no error (warnings allowed), 1 at least one error, 2 usage error, unreadable file or env file.
Python 3 standard library only. Reads files and runs slop-lint.sh. It never writes, never uses the network.
"""
import argparse
import datetime
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

KNOWN_FIELDS = {"title", "summary", "date", "updated", "author", "tags", "takeaways", "faq", "cover", "draft"}
NAV_TOPICS = ("agents", "protocol", "native-assets")  # the only tags a reader can see on the site
TITLE_LIMIT = 60
TITLE_TAG_EXTRA = 11  # the article page appends a separator and "MOI Blog" to the title tag
SUMMARY_MIN, SUMMARY_MAX = 130, 170
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FILE_EXTS = {"md", "json", "js", "mjs", "cjs", "ts", "tsx", "jsx", "html", "htm", "css", "png", "jpg", "jpeg",
             "svg", "gif", "webp", "txt", "csv", "pdf", "yml", "yaml", "xml", "py", "sh", "toml", "lock"}
GENERIC_LINK_TEXT = {"here", "click here", "this link", "link", "this", "read more", "more", "this post"}
PRIVATE_REPOS = ("go-moi", "go-pisa", "cocolang", "moidocs", "voyage-docs", "coco-docs", "voyage", "voyage-api",
                 "moi-agent-launchpad", "agent-explorer", "moi-project")
LOCAL_PATH = re.compile("/Us" + r"ers/|(?<![\w/])~/[A-Za-z]")  # a path from someone's home folder
EM_DASH = chr(0x2014)  # built from its code point so this file never holds the character itself
EMOJI = re.compile("[" + chr(0x1F000) + "-" + chr(0x1FAFF) + chr(0x2600) + "-" + chr(0x27BF) + chr(0x2B50) + chr(0x2B55) + chr(0xFE0F) + "]")  # brand voice: no emoji
LENGTH_RULES = {"title-length", "summary-length"}
PLACEHOLDER_CS = re.compile(r"<<<|\[FILL IN\b|REPLACE-WITH|\b(?:RELEASE|LUMA|CANONICAL)_URL\b|\bTODO\b|\bFIXME\b|\bTBD\b")  # slop-lint:ignore
PLACEHOLDER_CI = re.compile(r"lorem ipsum|\[(?:link|url|insert[^\]]*)\](?!\()", re.I)
# {{x}} is the placeholder style of the skeletons in release-pack/templates/. It is a post-only rule: an announcement copy
# file keeps {{link}} as its legal link token, so copy-lint.py does not use this pattern.
PLACEHOLDER_BRACES = re.compile(r"\{\{[^}\n]+\}\}")
VOCAB = (re.compile(r"\bAI assistant\b", re.I), re.compile(r"\bblockchain\b", re.I))

# Shapes of a key, a token or a webhook. A message that quotes the file never prints one (see redact).
SECRET_SHAPES = (
    re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{12,}"),
    re.compile(r"\bgsk_[A-Za-z0-9]{12,}"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{16,}"),
    re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{12,}"),
    re.compile(r"\b(?:sk|rk)_live_[0-9A-Za-z]{10,}"),
    re.compile(r"\bnpm_[A-Za-z0-9]{16,}"),
    re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{12,}|\bgithub_pat_[A-Za-z0-9_]{12,}"),
    re.compile(r"\bxox[abprso]-[A-Za-z0-9-]{8,}"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"),
    re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{30,}"),
    re.compile(r"/api/webhooks/\d+/[A-Za-z0-9_-]{12,}|hooks\.slack\.com/services/[A-Za-z0-9/]+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
)
QUERY_VALUE = re.compile(r"([?&][A-Za-z0-9_.-]+=)[^&\s)\]<>'\"]+")
URL_USERINFO = re.compile(r"(https?://)[^/\s:@]+:[^/\s@]+@")
LONG_RUN = re.compile(r"(?<![A-Za-z0-9_+/=])[A-Za-z0-9_+/=]{32,}(?![A-Za-z0-9_+/=])")


def redact(text):
    """Replace anything key-shaped in a message that quotes the file, so a lint run never echoes a secret."""
    s = str(text)
    for rx in SECRET_SHAPES:
        s = rx.sub("<masked>", s)
    s = URL_USERINFO.sub(r"\1<masked>@", s)
    s = QUERY_VALUE.sub(r"\1<masked>", s)
    return LONG_RUN.sub(lambda m: "<masked>" if re.search(r"\d", m.group(0)) and re.search(r"[A-Za-z]", m.group(0)) else m.group(0), s)


class YamlError(Exception):
    def __init__(self, line, msg):
        Exception.__init__(self, msg)
        self.line = line
        self.msg = msg


class Map(dict):
    def __init__(self):
        dict.__init__(self)
        self.lines = {}


class Seq(list):
    def __init__(self):
        list.__init__(self)
        self.lines = []


class Inline(object):
    def __init__(self, raw):
        self.raw = raw


def parse_scalar(s, ln, in_list=False):
    s = s.strip()
    if s == "":
        return None
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
            raise YamlError(ln, "unterminated double-quoted string")
        rest = s[j + 1:].strip()
        if rest and not rest.startswith("#"):
            raise YamlError(ln, "text after the closing quote")
        return "".join(buf)
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
            raise YamlError(ln, "unterminated single-quoted string")
        rest = s[j + 1:].strip()
        if rest and not rest.startswith("#"):
            raise YamlError(ln, "text after the closing quote")
        return "".join(buf)
    if s[0] == "[":
        return parse_flow_list(s, ln)
    if s[0] == "{":
        return Inline(s)
    if s[0] in "@`%":
        raise YamlError(ln, "a plain value cannot start with %s; wrap it in double quotes" % s[0])
    s = re.split(r"\s#", s, maxsplit=1)[0].rstrip()
    if not in_list and re.search(r":(\s|$)", s):
        raise YamlError(ln, "unquoted colon: YAML reads it as a nested map and the build fails; wrap the value in double quotes")
    if s == "true":
        return True
    if s == "false":
        return False
    return s


def parse_flow_list(s, ln):
    if not s.rstrip().endswith("]"):
        raise YamlError(ln, "inline list is not closed on the same line")
    inner = s.strip()[1:-1]
    parts, cur, q, i = [], "", None, 0
    while i < len(inner):
        c = inner[i]
        if q:
            cur += c
            if c == "\\" and q == '"' and i + 1 < len(inner):
                cur += inner[i + 1]
                i += 1
            elif c == q:
                q = None
        elif c in "\"'":
            q = c
            cur += c
        elif c == ",":
            parts.append(cur)
            cur = ""
        else:
            cur += c
        i += 1
    if q:
        raise YamlError(ln, "unterminated quote inside the inline list")
    parts.append(cur)
    out = Seq()
    for p in parts:
        if p.strip() == "":
            continue
        out.append(parse_scalar(p.strip(), ln, in_list=True))
        out.lines.append(ln)
    return out


class Parser(object):
    """A small YAML subset parser: maps, lists, nested blocks, quoted and block scalars. Enough for this contract."""

    def __init__(self, lines):
        self.lines = list(lines)  # (file line number, raw text)
        self.i = 0

    def cur(self):
        while self.i < len(self.lines):
            ln, raw = self.lines[self.i]
            if raw.strip() == "" or raw.lstrip().startswith("#"):
                self.i += 1
                continue
            lead = raw[:len(raw) - len(raw.lstrip())]
            if "\t" in lead:
                raise YamlError(ln, "tab used for indentation; YAML needs spaces")
            return ln, len(lead), raw.strip()
        return None

    def parse_node(self, indent):
        c = self.cur()
        if c[2] == "-" or c[2].startswith("- "):
            return self.parse_list(indent)
        return self.parse_map(indent)

    def parse_map(self, indent):
        d = Map()
        while True:
            c = self.cur()
            if c is None:
                break
            ln, ind, text = c
            if ind < indent:
                break
            if ind > indent:
                raise YamlError(ln, "unexpected indentation")
            if text == "-" or text.startswith("- "):
                break
            m = re.match(r"""^([A-Za-z_][\w.-]*|"[^"]+"|'[^']+')\s*:(?:\s+(.*))?$""", text)
            if not m:
                raise YamlError(ln, "expected 'key: value'")
            key, val = m.group(1).strip("\"'"), m.group(2)
            if key in d:
                raise YamlError(ln, "duplicate key '%s'" % key)
            d.lines[key] = ln
            self.i += 1
            if val is None or val.strip() == "" or val.strip().startswith("#"):
                nxt = self.cur()
                if nxt and (nxt[1] > indent or (nxt[1] == indent and (nxt[2] == "-" or nxt[2].startswith("- ")))):
                    d[key] = self.parse_node(nxt[1])
                else:
                    d[key] = None
            elif val.strip() in ("|", "|-", "|+", ">", ">-", ">+"):
                d[key] = self.parse_block_scalar(indent, val.strip())
            else:
                d[key] = parse_scalar(val, ln)
        return d

    def parse_list(self, indent):
        out = Seq()
        while True:
            c = self.cur()
            if c is None:
                break
            ln, ind, text = c
            if ind != indent or not (text == "-" or text.startswith("- ")):
                break
            rest = text[1:].lstrip(" ")
            if rest == "":
                self.i += 1
                nxt = self.cur()
                item = self.parse_node(nxt[1]) if nxt and nxt[1] > indent else None
            elif re.match(r"^[A-Za-z_][\w.-]*\s*:(\s|$)", rest):
                col = ind + (len(text) - len(rest))
                self.lines[self.i] = (ln, " " * col + rest)
                item = self.parse_map(col)
            else:
                self.i += 1
                item = parse_scalar(rest, ln)
            out.append(item)
            out.lines.append(ln)
        return out

    def parse_block_scalar(self, parent_indent, style):
        buf, blk = [], None
        while self.i < len(self.lines):
            ln, raw = self.lines[self.i]
            if raw.strip() == "":
                buf.append("")
                self.i += 1
                continue
            ind = len(raw) - len(raw.lstrip(" "))
            if ind <= parent_indent:
                break
            if blk is None:
                blk = ind
            buf.append(raw[blk:] if ind >= blk else raw.strip())
            self.i += 1
        while buf and buf[-1] == "":
            buf.pop()
        if style.startswith("|"):
            return "\n".join(buf)
        return " ".join(x if x else "\n" for x in buf)

    def parse(self):
        c = self.cur()
        if c is None:
            return Map()
        d = self.parse_map(c[1])
        if self.cur() is not None:
            ln = self.cur()[0]
            raise YamlError(ln, "could not read this line as part of the frontmatter")
        return d


class Report(object):
    def __init__(self, strict):
        self.items = []
        self.strict = strict

    def add(self, line, level, rule, msg):
        if self.strict and level == "WARN" and rule in LENGTH_RULES:
            level = "ERROR"
        self.items.append((line, level, rule, redact(msg)))

    def count(self, level):
        return sum(1 for x in self.items if x[1] == level)


def find_repo(post, repo_arg):
    """Return the repo root (a Path) or None."""
    if repo_arg:
        r = Path(repo_arg).resolve()
        return r if (r / "blog" / "src" / "content" / "posts").is_dir() else None
    for parent in [post.resolve().parent] + list(post.resolve().parents):
        if (parent / "blog" / "src" / "content" / "posts").is_dir():
            return parent
    cwd = Path.cwd()
    if (cwd / "blog" / "src" / "content" / "posts").is_dir():
        return cwd
    return None


def find_slop_lint():
    cands = []
    if os.environ.get("SKILLS"):
        cands.append(Path(os.environ["SKILLS"]) / "moi-devrel" / "scripts" / "slop-lint.sh")
    cands.append(Path(__file__).resolve().parents[2] / "moi-devrel" / "scripts" / "slop-lint.sh")
    for c in cands:
        if c.is_file():
            return c
    return None


def github_slug(text):
    t = re.sub(r"[*_`]", "", text.strip().lower())
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"[^\w\- ]", "", t, flags=re.UNICODE)
    return t.replace(" ", "-")


def classify(url):
    u = url.strip()
    if u == "":
        return "empty"
    if u.startswith("#"):
        return "anchor"
    if u.startswith("//"):
        return "protocol-relative"
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", u):
        scheme = u.split(":", 1)[0].lower()
        if scheme == "https":
            return "https"
        if scheme == "http":
            return "http"
        if scheme == "mailto":
            return "mailto"
        return "bad-scheme"
    if u.startswith("/"):
        return "root-relative"
    if u.startswith(("./", "../")):
        return "relative"
    m = re.match(r"^(?:www\.)?[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.([A-Za-z]{2,})(?:[/:?#].*)?$", u)
    if m and m.group(1).lower() not in FILE_EXTS:
        return "no-scheme"
    return "relative"


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


def refuse_env(tool, path):
    sys.stderr.write("%s: refusing to read %s: an env file can hold keys and is never opened. "
                     "Pass the post file instead.\n" % (tool, os.path.basename(str(path))))


def main():
    ap = argparse.ArgumentParser(description="Check a MOI blog post before the pull request.",
                                 epilog="Exit 0 no error, 1 error, 2 usage, unreadable file or env file.")
    ap.add_argument("post")
    ap.add_argument("--repo")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--no-slop-lint", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--today")
    args = ap.parse_args()

    post = Path(args.post)
    if is_env_file(post):
        refuse_env("post-lint", post)
        return 2
    try:
        text = post.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        sys.stderr.write("post-lint: cannot read %s: %s\n" % (post, e))
        return 2
    if text.startswith("﻿"):
        text = text[1:]
    try:
        today = datetime.date.fromisoformat(args.today) if args.today else datetime.datetime.now(datetime.timezone.utc).date()
    except ValueError:
        sys.stderr.write("post-lint: --today must be YYYY-MM-DD\n")
        return 2

    rep = Report(args.strict)
    lines = text.split("\n")
    repo = find_repo(post, args.repo)
    if args.repo and repo is None:
        sys.stderr.write("post-lint: --repo %s has no blog/src/content/posts folder\n" % args.repo)
        return 2
    posts_dir = (repo / "blog" / "src" / "content" / "posts") if repo else None
    public_dir = (repo / "blog" / "public") if repo else None

    # ---- split the frontmatter ------------------------------------------------------------------
    fm, body_start = None, 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                fm = [(k + 2, lines[1 + k]) for k in range(0, i - 1)]
                body_start = i + 1
                break
    data = Map()
    yaml_ok = True  # when the YAML cannot be read, the field checks would only report fields that are in fact present
    if fm is None:
        rep.add(1, "ERROR", "frontmatter-missing", "the file must start with a line of three dashes, the frontmatter, then another line of three dashes")
    else:
        try:
            data = Parser(fm).parse()
        except YamlError as e:
            rep.add(e.line, "ERROR", "frontmatter-yaml", e.msg + " (fix this first: the field checks were skipped, because the frontmatter could not be read)")
            data = Map()
            yaml_ok = False

    def fl(key):
        return data.lines.get(key, 1)

    # ---- frontmatter fields ----------------------------------------------------------------------
    if fm is not None and yaml_ok:
        for key in ("title", "summary", "date"):
            v = data.get(key)
            if v is None or (isinstance(v, str) and v.strip() == ""):
                hint = ""
                if key == "summary" and data.get("description"):
                    hint = " (this file has `description`; the blog field is `summary`)"
                rep.add(fl(key) if key in data else 1, "ERROR", "missing-field", "`%s` is required and is empty or absent%s" % (key, hint))
        for key in data:
            if key not in KNOWN_FIELDS:
                rep.add(fl(key), "WARN", "unknown-field", "`%s` is not in the blog schema; the build ignores it" % key)
        title, summary = data.get("title"), data.get("summary")
        if isinstance(title, str) and title.strip():
            n = len(title)
            if n > TITLE_LIMIT:
                rep.add(fl("title"), "WARN", "title-length", "title is %d characters; the docs standard says up to %d and search results truncate near 60 (the title tag is %d with the site suffix). The blog has no limit of its own on record" % (n, TITLE_LIMIT, n + TITLE_TAG_EXTRA))
        elif title is not None and not isinstance(title, str):
            rep.add(fl("title"), "ERROR", "title-type", "`title` must be text")
        if isinstance(summary, str) and summary.strip():
            n = len(summary.strip())
            if n < SUMMARY_MIN or n > SUMMARY_MAX:
                rep.add(fl("summary"), "WARN", "summary-length", "summary is %d characters; it is also the meta description, and the docs standard asks for 140 to 160 (130 to 170 tolerated)" % n)
        elif summary is not None and not isinstance(summary, str):
            rep.add(fl("summary"), "ERROR", "summary-type", "`summary` must be text")

        dv = data.get("date")
        d_parsed = None
        if isinstance(dv, str) and dv.strip():
            if re.match(r"^\d{4}-\d{2}-\d{2}$", dv.strip()):
                try:
                    d_parsed = datetime.date.fromisoformat(dv.strip())
                except ValueError:
                    rep.add(fl("date"), "ERROR", "date-invalid", "`date: %s` is not a real calendar date" % dv)
            elif re.match(r"^\d{4}-\d{2}-\d{2}[T ]", dv.strip()):
                rep.add(fl("date"), "WARN", "date-has-time", "write the date only (2026-09-11); a time part can show a day early or late in some zones")
                try:
                    d_parsed = datetime.date.fromisoformat(dv.strip()[:10])
                except ValueError:
                    rep.add(fl("date"), "ERROR", "date-invalid", "`date: %s` is not a real calendar date" % dv)
            else:
                rep.add(fl("date"), "ERROR", "date-invalid", "`date: %s` is not a date; the build fails with Invalid Date" % dv)
        if d_parsed and d_parsed > today:
            rep.add(fl("date"), "WARN", "date-future", "date is after %s; the site does not hold back future-dated posts, so it publishes on merge with that date" % today.isoformat())
        up = data.get("updated")
        if isinstance(up, str) and up.strip():
            m = re.match(r"^(\d{4}-\d{2}-\d{2})", up.strip())
            if not m:
                rep.add(fl("updated"), "ERROR", "date-invalid", "`updated: %s` is not a date" % up)
            elif d_parsed and m.group(1) == d_parsed.isoformat():
                rep.add(fl("updated"), "WARN", "updated-same-as-date", "`updated` equals `date`, so no Updated line shows; set it only when the post changed after publication")
            elif d_parsed and m.group(1) < d_parsed.isoformat():
                rep.add(fl("updated"), "WARN", "updated-before-date", "`updated` is earlier than `date`")

        au = data.get("author")
        if au is None and "author" not in data:
            rep.add(1, "WARN", "author-missing", "no author: the page has no byline and the JSON-LD has no author. Byline policy is open: ASK: Rahul")
        elif isinstance(au, Map):
            nm = au.get("name")
            if not isinstance(nm, str) or not nm.strip():
                rep.add(fl("author"), "ERROR", "author-name", "`author.name` is required when `author` is given")
            url = au.get("url")
            if url is not None and not (isinstance(url, str) and re.match(r"^https?://\S+$", url)):
                rep.add(au.lines.get("url", fl("author")), "ERROR", "author-url", "`author.url` must be a full URL with https://; a bare domain fails the build")
            for k in au:
                if k not in ("name", "role", "url"):
                    rep.add(au.lines.get(k, fl("author")), "WARN", "unknown-field", "`author.%s` is not in the schema" % k)
        elif isinstance(au, Inline):
            rep.add(fl("author"), "WARN", "inline-map", "`author` is written as an inline map; this lint did not check it. Use the block form")
        else:
            rep.add(fl("author"), "ERROR", "author-type", "`author` must be a block with name, role and url; a plain string fails the build")

        tags = data.get("tags")
        if tags is not None and not isinstance(tags, Seq):
            rep.add(fl("tags"), "ERROR", "tags-type", "`tags` must be a list")
        elif isinstance(tags, Seq):
            for t in tags:
                if not isinstance(t, str) or not SLUG_RE.match(t):
                    rep.add(fl("tags"), "ERROR", "tag-not-slug", "tag %r must be a lowercase slug such as native-assets; tags become URLs under /tags/" % (t,))
            if tags and not any(t in NAV_TOPICS for t in tags if isinstance(t, str)):
                rep.add(fl("tags"), "WARN", "tags-not-visible", "none of agents, protocol, native-assets is a tag here; those are the only tags a reader can see or click")
            if not tags:
                rep.add(fl("tags"), "WARN", "tags-empty", "no tags: the post has no tag page and no JSON-LD keywords")
        elif "tags" not in data:
            rep.add(1, "WARN", "tags-empty", "no tags: the post has no tag page and no JSON-LD keywords")

        tk = data.get("takeaways")
        if tk is not None:
            if not isinstance(tk, Seq) or any(not isinstance(x, str) or not x.strip() for x in tk):
                rep.add(fl("takeaways"), "ERROR", "takeaways-type", "`takeaways` must be a list of text lines")
            elif len(tk) != 8:
                rep.add(fl("takeaways"), "WARN", "takeaways-count", "%d takeaways; the corpus convention is exactly 8, or none (the schema does not enforce it)" % len(tk))
        faq = data.get("faq")
        if faq is not None:
            if not isinstance(faq, Seq):
                rep.add(fl("faq"), "ERROR", "faq-type", "`faq` must be a list of q and a pairs")
            else:
                for k, item in enumerate(faq):
                    ln = faq.lines[k] if k < len(faq.lines) else fl("faq")
                    if not isinstance(item, Map) or not isinstance(item.get("q"), str) or not isinstance(item.get("a"), str) or not item.get("q").strip() or not item.get("a").strip():
                        rep.add(ln, "ERROR", "faq-entry", "each faq entry needs a `q` and an `a`; the build fails otherwise")
                    elif not item["q"].strip().endswith("?"):
                        rep.add(ln, "WARN", "faq-question", "faq question does not end with a question mark")
                if len(faq) < 7:
                    rep.add(fl("faq"), "WARN", "faq-count", "%d faq entries; the posts on main carry 7 to 17" % len(faq))
        dr = data.get("draft")
        if dr is not None and not isinstance(dr, bool):
            rep.add(fl("draft"), "ERROR", "draft-type", "`draft` must be true or false")
        elif dr is True:
            rep.add(fl("draft"), "WARN", "draft-true", "draft: true removes the post from the site, feeds, sitemap and llms.txt; set it to false when it is ready to publish")

        cv = data.get("cover")
        if cv is not None:
            if not isinstance(cv, str) or not cv.startswith("/covers/"):
                rep.add(fl("cover"), "WARN", "cover-path", "`cover` should be /covers/<name>.svg or .png, a path under blog/public/covers")
            elif public_dir:
                f = public_dir / cv.lstrip("/")
                if not f.is_file():
                    rep.add(fl("cover"), "ERROR", "cover-missing", "cover file %s does not exist" % cv)
                if cv.endswith(".svg") and not f.with_suffix(".png").is_file():
                    rep.add(fl("cover"), "ERROR", "cover-png-missing", "an SVG cover needs a 1200x630 PNG with the same name; og:image points at the .png and X, LinkedIn and Slack show nothing without it")
            else:
                rep.add(fl("cover"), "WARN", "cover-not-checked", "cover files not checked: no repo found. Give --repo")

    if fm is not None:
        for fln, fraw in fm:
            if fraw.lstrip().startswith("#"):
                continue
            if PLACEHOLDER_CS.search(fraw) or PLACEHOLDER_CI.search(fraw) or PLACEHOLDER_BRACES.search(fraw):
                rep.add(fln, "ERROR", "placeholder", "placeholder text in the frontmatter must not ship")

    # ---- body ------------------------------------------------------------------------------------
    body_lines = lines[body_start:]
    first_ln = body_start + 1
    in_fence, fence_ch, fence_len = False, "", 0
    headings, link_n, img_n, words = [], 0, 0, 0
    slugs = set()
    anchors_to_check = []
    images_unchecked = False
    siblings_unchecked = False
    siblings = None
    if posts_dir:
        siblings = set(p.stem for p in posts_dir.glob("*.md"))
    post_slug = post.stem

    def strip_inline_code(s):
        return re.sub(r"(`+)(.+?)\1", lambda m: " " * len(m.group(0)), s)

    def sibling_link_seen(u):
        nonlocal siblings_unchecked
        if siblings is None and re.match(r"^https?://blog\.moi\.technology/article/", u.strip()):
            siblings_unchecked = True

    for k, raw in enumerate(body_lines):
        ln = first_ln + k
        fence_m = re.match(r"^\s{0,3}(`{3,}|~{3,})", raw)
        if fence_m:
            ch, n = fence_m.group(1)[0], len(fence_m.group(1))
            if not in_fence:
                in_fence, fence_ch, fence_len = True, ch, n
                continue
            if ch == fence_ch and n >= fence_len and raw.strip().strip(ch) == "":
                in_fence = False
                continue
        if in_fence:
            if "<<<" in raw or "REPLACE-WITH" in raw:  # slop-lint:ignore
                rep.add(ln, "ERROR", "placeholder", "placeholder text must not ship")
            continue
        line = strip_inline_code(raw)
        words += len(re.findall(r"\S+", raw))

        if PLACEHOLDER_CS.search(line) or PLACEHOLDER_CI.search(line) or PLACEHOLDER_BRACES.search(line):
            rep.add(ln, "ERROR", "placeholder", "placeholder text must not ship ([FILL IN, {{x}}, <<<, REPLACE-WITH, TODO, TBD, RELEASE_URL, LUMA_URL, CANONICAL_URL)")  # slop-lint:ignore
        for vre in VOCAB:
            vm = vre.search(line)
            if vm:
                rep.add(ln, "WARN", "vocabulary", "the blog voice avoids %r; say agent, participant or network (CONTENT.md vocabulary)" % vm.group(0))
        if "<!--" in line:
            rep.add(ln, "ERROR", "html-comment", "an HTML comment ships as invisible markup in production; delete it")
        if re.search(r"<Subscribe\b", line):
            rep.add(ln, "WARN", "stray-subscribe", "do not put <Subscribe /> in a post: the article page already renders the signup form, and in a .md file this tag is inert")
        elif re.search(r"</?[A-Z][A-Za-z]+[\s/>]", line):
            rep.add(ln, "WARN", "component-tag", "a capitalised tag in a .md file is not a component; it renders as an unknown element")
        if LOCAL_PATH.search(line):
            rep.add(ln, "ERROR", "local-path", "a local file path in public text")

        hm = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if hm:
            lvl, txt = len(hm.group(1)), hm.group(2).strip()
            headings.append((ln, lvl, txt))
            slugs.add(github_slug(txt))
        for m in re.finditer(r"(!?)\[([^\]]*)\]\(\s*(<[^>]*>|(?:[^()\s]|\([^()\s]*\))*)(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)", line):
            is_img, label, url = m.group(1) == "!", m.group(2), m.group(3).strip("<>")
            if is_img:
                img_n += 1
                check_image(rep, ln, url, label, posts_dir, public_dir)
                if posts_dir is None:
                    images_unchecked = True
            else:
                link_n += 1
                sibling_link_seen(url)
                check_link(rep, ln, url, label, siblings, post_slug, anchors_to_check)
        for m in re.finditer(r"<(https?://[^>\s]+)>", line):
            link_n += 1
            sibling_link_seen(m.group(1))
            check_link(rep, ln, m.group(1), m.group(1), siblings, post_slug, anchors_to_check)
        for m in re.finditer(r"\b(href|src)\s*=\s*[\"']([^\"']+)[\"']", line):
            if m.group(1) == "src":
                img_n += 1
                check_image(rep, ln, m.group(2), "x", posts_dir, public_dir)
                if posts_dir is None:
                    images_unchecked = True
            else:
                link_n += 1
                sibling_link_seen(m.group(2))
                check_link(rep, ln, m.group(2), "x", siblings, post_slug, anchors_to_check)

    if in_fence:
        rep.add(first_ln, "ERROR", "unclosed-fence", "a code fence is opened and never closed; everything after it renders as code")
    if images_unchecked:
        rep.add(first_ln, "WARN", "images-not-checked", "images were not checked against the files: this file is not under blog/src/content/posts and no repo was found. Give --repo")
    if siblings_unchecked:
        rep.add(first_ln, "WARN", "siblings-not-checked", "links to other blog posts were not checked against blog/src/content/posts: no repo was found. Give --repo")

    # headings
    prev, seen_h2 = 0, {}
    for idx, (ln, lvl, txt) in enumerate(headings):
        if lvl == 1:
            rep.add(ln, "ERROR", "h1-in-body", "the title is already the page H1; a body # heading makes a second one. Start at ##")
        elif idx == 0 and lvl != 2:
            rep.add(ln, "ERROR", "heading-order", "the first heading is H%d; start at H2" % lvl)
        elif prev and lvl > prev + 1:
            rep.add(ln, "ERROR", "heading-order", "H%d follows H%d; do not skip a level" % (lvl, prev))
        if txt == "":
            rep.add(ln, "ERROR", "heading-empty", "empty heading")
        if lvl == 2:
            key = txt.lower()
            if key in seen_h2:
                rep.add(ln, "WARN", "duplicate-h2", "same H2 as line %d" % seen_h2[key])
            seen_h2[key] = ln
        ws = [w for w in re.findall(r"[A-Za-z][A-Za-z'-]*", txt)[1:] if len(w) >= 3 and not w.isupper()]
        if lvl <= 3 and len(ws) >= 3 and sum(1 for w in ws if w[0].isupper()) / float(len(ws)) >= 0.75:
            rep.add(ln, "WARN", "title-case-heading", "headings are sentence case; this reads as Title Case")
        prev = lvl if lvl > 1 else prev
    for ln, anc in anchors_to_check:
        if anc and github_slug(unquote(anc)) not in slugs and unquote(anc).lower() not in slugs:
            rep.add(ln, "WARN", "anchor-missing", "no heading produces the anchor #%s" % anc)

    # emoji: the house voice has none (a warning, because a symbol in a table can be deliberate)
    for k, raw in enumerate(lines):
        if EMOJI.search(raw):
            rep.add(k + 1, "WARN", "emoji", "an emoji or pictograph: the blog voice has none")
    # em dash everywhere (the rule is for every character of public text, frontmatter and code included)
    for k, raw in enumerate(lines):
        if EM_DASH in raw or re.search(r"&mdash;|&#8212;|&#x2014;", raw, re.I):
            rep.add(k + 1, "ERROR", "em-dash", "em dash (or its HTML entity). Use a comma, a colon or a full stop")

    # ---- phrasing: moi-devrel's slop-lint -------------------------------------------------------
    if not args.no_slop_lint:
        sl = find_slop_lint()
        if sl is None:
            rep.add(1, "ERROR", "slop-lint-missing", "moi-devrel/scripts/slop-lint.sh was not found, so the phrasing rules were not checked. Set SKILLS to the folder that holds the moi-* skills, or pass --no-slop-lint to skip them on purpose")
        else:
            try:
                r = subprocess.run(["bash", str(sl), str(post)], capture_output=True, text=True, timeout=120)
            except (OSError, subprocess.SubprocessError) as e:
                rep.add(1, "ERROR", "slop-lint-failed", "could not run slop-lint.sh: %s" % e)
                r = None
            if r is not None:
                if r.returncode == 2:
                    rep.add(1, "ERROR", "slop-lint-failed", "slop-lint.sh could not read the file")
                prefix = str(post) + ":"
                for out in r.stdout.splitlines():
                    if not out.startswith(prefix):
                        continue
                    m = re.match(r"(\d+):([a-z0-9-]+)(\(warn\))?:(.*)$", out[len(prefix):])
                    if not m or m.group(2) in ("em-dash", "placeholder"):
                        continue
                    rep.add(int(m.group(1)), "WARN" if m.group(3) else "ERROR", "slop-lint/" + m.group(2), m.group(4).strip())
    # ---- output ----------------------------------------------------------------------------------
    sys.stdout.flush()
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    for line, level, rule, msg in sorted(rep.items, key=lambda x: (x[0], order[x[1]], x[2])):
        if level == "INFO" and not args.verbose:
            continue
        print("%s:%d:%s:%s: %s" % (post, line, level, rule, msg))
    h2 = [h for h in headings if h[1] == 2]
    q = sum(1 for h in h2 if h[2].endswith("?"))
    tk_n = len(data.get("takeaways")) if isinstance(data.get("takeaways"), Seq) else 0
    fq_n = len(data.get("faq")) if isinstance(data.get("faq"), Seq) else 0
    sys.stderr.write("post-lint: %d error(s), %d warning(s). %d body words (about %d min), %d H2 (%d as questions), %d takeaways, %d faq, %d links, %d images\n"
                     % (rep.count("ERROR"), rep.count("WARN"), words, max(1, int(round(words / 200.0))), len(h2), q, tk_n, fq_n, link_n, img_n))
    return 1 if rep.count("ERROR") else 0


def check_link(rep, ln, url, label, siblings, post_slug, anchors):
    kind = classify(url)
    if kind == "empty":
        rep.add(ln, "ERROR", "link-empty", "a link with no address")
        return
    if kind == "no-scheme":
        rep.add(ln, "ERROR", "link-no-scheme", "%r has no https://, so it becomes a broken relative link on the page" % url)
    elif kind == "http":
        rep.add(ln, "WARN", "link-http", "%r is http; use https" % url)
    elif kind == "bad-scheme":
        rep.add(ln, "ERROR", "link-scheme", "%r uses a scheme a post must not carry" % url)
    elif kind == "root-relative":
        rep.add(ln, "WARN", "link-root-relative", "%r resolves against whichever host serves it (the blog, a preview, an email); use the absolute https URL" % url)
    elif kind == "protocol-relative":
        rep.add(ln, "WARN", "link-protocol-relative", "%r should start with https://" % url)
    elif kind == "relative":
        rep.add(ln, "WARN", "link-relative", "%r is relative to the article URL, not to this file" % url)
    elif kind == "anchor":
        anchors.append((ln, url[1:]))
    if kind in ("https", "http"):
        if re.match(r"^https?://(?:localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\])", url):
            rep.add(ln, "ERROR", "local-link", "%r is a local address; readers cannot open it" % url)
        if re.search(r"\.preview\.moi\.technology", url):
            rep.add(ln, "ERROR", "preview-link", "%r is a pull request preview; previews are deleted after 7 days" % url)
        m = re.match(r"^https?://github\.com/sarvalabs/([A-Za-z0-9._-]+)", url)
        if m and m.group(1) in PRIVATE_REPOS:
            rep.add(ln, "WARN", "private-repo-link", "sarvalabs/%s is private: readers get a 404, and public posts cite public artefacts only" % m.group(1))
        if re.search(r"[?&]utm_", url):
            rep.add(ln, "WARN", "utm-in-body", "do not tag links in the post body; tagged links belong to the announcement ({{link}})")
        sm = re.match(r"^https?://blog\.moi\.technology/article/([^/?#]+)", url)
        if sm and siblings is not None and sm.group(1) not in siblings and sm.group(1) != post_slug:
            rep.add(ln, "WARN", "sibling-not-found", "no post %s in blog/src/content/posts; check the slug or that the post is merged first" % sm.group(1))
    if label.strip().lower() in GENERIC_LINK_TEXT:
        rep.add(ln, "WARN", "link-text", "link text %r says nothing; name what the link is" % label.strip())
    elif label.strip() == "" and kind != "empty":
        rep.add(ln, "WARN", "link-text", "a link with no text")


def check_image(rep, ln, url, alt, posts_dir, public_dir):
    kind = classify(url)
    if alt.strip() == "":
        rep.add(ln, "WARN", "image-alt", "image has no alt text; write a full sentence that says what the picture shows")
    if kind in ("https", "http"):
        rep.add(ln, "WARN", "image-remote", "remote image %r is not hashed, cached or checked by the build; keep it under blog/src/assets/<post>/" % url)
        return
    if "agent-flow.svg" in url:
        rep.add(ln, "WARN", "image-agent-flow", "agent-flow.svg is the documented example but is drawn in the old cream and purple palette; do not copy it")
    if kind == "root-relative":
        if public_dir is not None:
            f = public_dir / unquote(re.split(r"[?#]", url)[0]).lstrip("/")
            if not f.is_file():
                rep.add(ln, "ERROR", "image-missing", "%s does not exist under blog/public" % url)
        return
    if kind in ("relative", "no-scheme"):
        if not url.startswith("../../assets/"):
            rep.add(ln, "WARN", "image-location", "post images live in blog/src/assets/<post>/ and are referenced as ../../assets/<post>/<file>")
        if posts_dir is not None:
            f = (posts_dir / unquote(re.split(r"[?#]", url)[0])).resolve()
            if not f.is_file():
                rep.add(ln, "ERROR", "image-missing", "%s does not exist (looked for %s)" % (url, f.name))


if __name__ == "__main__":
    sys.exit(main())
