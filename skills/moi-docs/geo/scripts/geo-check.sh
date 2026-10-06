#!/usr/bin/env bash
# geo-check.sh: read-only check of the search and AI-visibility layer of one MOI site.
#
# Usage:   bash "$SKILLS/moi-docs/geo/scripts/geo-check.sh" <base-url> [options]
#          SKILLS is the folder that holds the moi-* skills. Run it from any folder: it reads no file.
#          <base-url>  the site root with its scheme, for example https://docs.moi.technology
#                      (http is accepted only for localhost). A page, a query or a user name in it is refused.
# Options: --page /path          the sample page for the head checks (default: a deep page from the sitemap)
#          --expect-host HOST    the host that canonicals, sitemap entries and llms.txt links must use.
#                                Default: the base host; for a *.pages.dev preview, the host in the robots
#                                Sitemap line (a preview points at production on purpose)
#          --forbid REGEX        a pattern no sitemap address may match, added to the built-in "markdown-page"
#          --indexnow-file NAME  the IndexNow key file name (a .txt in the repo's static folder); checks that
#                                it is served and matches its own name. The name is never printed
#          --pages N             how many pages to compare dateModified across (default 5, 1 to 10)
#          --follow              also request every link (up to 20) in the API catalog and the skills index.
#                                Only https links to public host names, or back to the checked host, are
#                                requested. A link that cannot be reached is a FAIL line, not the end of the run
#          --timeout SECONDS     per request (default 25, 1 to 120)
#
# Output:  one line per check, PASS, WARN or FAIL, then a totals line and a "not checked" line, all on stdout.
#          Only the host and path of an address are printed, never a query or a credential.
# Exit codes: 0 no FAIL (WARN allowed), 1 at least one FAIL, 2 bad input, or the host could not be reached.
#
# What it requests: HTTP GET only (a ranged GET or HEAD for --follow), through curl, with a timeout. It sends
# no cookie, no credential and no body, writes no file outside a temporary folder it deletes, and never
# submits, signs in or posts. Three requests to the home page use the user-agent names GPTBot/1.0,
# ClaudeBot/1.0 and PerplexityBot/1.0, as the documented crawler check does.
# What it cannot show: how the real crawlers (they come from their vendors' address ranges) are treated,
# what a search engine has indexed, what a page looks like when JavaScript runs, and headers that only a
# production edge adds. The "not checked" line says so on every run.
# It prints text taken from the site, so secret-shaped values (long hex, known token prefixes, JWTs,
# recovery-phrase-shaped runs of words) are masked before anything is clipped or printed.
# Python 3 standard library plus curl. Works under bash 3.2 and zsh.
# curl is started with -q, so a ~/.curlrc (which could add a header, a user name or a proxy) is ignored.

if ! command -v python3 >/dev/null 2>&1; then
  echo "geo-check: python3 was not found. Install Python 3 and run again" >&2
  exit 2
fi
exec python3 - "$@" <<'PY'
import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse

ORG_ID = "https://moi.technology/#organization"
UA_TOOL = "moi-geo-check/1.0 (read-only)"
CRAWLERS = [("GPTBot", "GPTBot/1.0"), ("ClaudeBot", "ClaudeBot/1.0"), ("PerplexityBot", "PerplexityBot/1.0")]

# ---------------------------------------------------------------- masking
SECRET_RULES = [re.compile(p) for p in (
    r"\bsk-ant-[A-Za-z0-9_-]{20,}", r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}", r"\bgsk_[A-Za-z0-9]{20,}",
    r"\bAIza[0-9A-Za-z_-]{35}\b", r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b", r"\b(?:sk|rk)_live_[0-9A-Za-z]{16,}",
    r"\bnpm_[A-Za-z0-9]{36}\b", r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}", r"\bgithub_pat_[A-Za-z0-9_]{22,}",
    r"\bxox[abprso]-[A-Za-z0-9-]{10,}", r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b",
    r"\beyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}",
    r"(?:0x)?[0-9A-Fa-f]{32,}", r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
)]
STOPWORDS = frozenset(
    "after and are been being both but could did does each every for from get got had has her here him "
    "his how its let many may most not our out per see she should some than the their them these those "
    "too using via was were which while who why with would yes your".split()
)
# Twelve or more words of 3 to 8 letters in a row, split by spaces, commas, semicolons or line breaks,
# each word optionally numbered ("1. word"). That is the shape of a recovery phrase. Ordinary prose
# almost always holds a short word ("of", "a", "to") that breaks the run, or a common word (STOPWORDS).
WORD_UNIT = r"(?:\d{1,2}[.):]?[ \t]+)?[A-Za-z]{3,8}"
WORD_RUN = re.compile(r"(?<![A-Za-z])" + WORD_UNIT + r"(?:[\s,;]+" + WORD_UNIT + r"){11,}(?![A-Za-z])")


def _phrase(m):
    # STOPWORDS are common English words that are not on the 2048-word list a recovery phrase is drawn
    # from (the same list moi-devrel/scripts/secret-scan.sh uses). A run that holds one is prose: keep it.
    words = re.findall(r"[A-Za-z]+", m.group(0))
    return m.group(0) if any(w.lower() in STOPWORDS for w in words) else "<masked>"


def mask(s):
    s = str(s)
    for rx in SECRET_RULES:
        s = rx.sub("<masked>", s)
    return WORD_RUN.sub(_phrase, s)


def clip(s, n=260):
    return s if len(s) <= n else s[: n - 3] + "..."


def where(url):
    """host + path of an address. The scheme, query, fragment and any user name are dropped."""
    try:
        sp = urllib.parse.urlsplit(url)
        host = sp.hostname or ""
        return mask(host + (sp.path or "/"))
    except ValueError:
        return "<unparsable address>"


class Bad(Exception):
    pass


class Unreachable(Exception):
    pass


def is_env_name(name):
    low = name.lower()
    return low in (".env", ".envrc") or low.startswith(".env.") or low.endswith(".env") or ".env." in low


# ---------------------------------------------------------------- input
def parse_base(arg):
    if re.search(r"[\s\x00-\x1f\x7f]", arg):
        raise Bad("the address holds a space or a control character")
    sp = urllib.parse.urlsplit(arg)
    if sp.scheme not in ("http", "https") or not sp.netloc:
        raise Bad("give the site root with its scheme, for example https://docs.moi.technology")
    if "@" in sp.netloc:
        raise Bad("the address holds a user name or password. Give the plain site address")
    if "?" in arg or "#" in arg:
        raise Bad("the address holds a query or a fragment. Give the plain site root")
    if sp.path not in ("", "/"):
        raise Bad("give the site root, not a page. Use --page /path to choose the sample page")
    try:
        host, port = sp.hostname, sp.port
    except ValueError:
        raise Bad("the port is not a number")
    if not host or not re.fullmatch(r"[A-Za-z0-9.:-]+", host):
        raise Bad("the host name holds characters a host name cannot hold")
    local = host in ("localhost", "127.0.0.1", "::1")
    if sp.scheme == "http" and not local:
        raise Bad("http is accepted only for localhost. Use https")
    netloc = ("[%s]" % host if ":" in host else host) + (":%d" % port if port else "")
    return sp.scheme, host.lower(), "%s://%s" % (sp.scheme, netloc.lower())


def clean_path(p, flag):
    if not p.startswith("/") or "//" in p or "?" in p or "#" in p or re.search(r"[\s\x00-\x1f\x7f]", p):
        raise Bad("%s must be a path that starts with / and holds no query, fragment, space or //" % flag)
    segs = [s for s in p.split("/") if s]
    if any(s in (".", "..") for s in segs):
        raise Bad("%s must not hold . or .. segments" % flag)
    if any(is_env_name(s) for s in segs):
        raise Bad("%s names an env file. This script never asks a site for one" % flag)
    return p


# ---------------------------------------------------------------- http
class Resp(object):
    status = 0
    ctype = ""
    headers = {}
    body = ""
    first_status = 0
    first_location = ""
    final = ""
    redirects = 0


def parse_header_blocks(raw):
    out = []
    for block in re.split(r"\r?\n\r?\n", raw.strip()):
        lines = block.strip().splitlines()
        if not lines or not lines[0].startswith("HTTP/"):
            continue
        m = re.match(r"HTTP/\S+\s+(\d{3})", lines[0])
        hd = {}
        for ln in lines[1:]:
            if ":" in ln:
                k, v = ln.split(":", 1)
                hd.setdefault(k.strip().lower(), []).append(v.strip())
        out.append((int(m.group(1)) if m else 0, hd))
    return out


class Http(object):
    def __init__(self, timeout):
        self.timeout = timeout
        self.tmp = tempfile.mkdtemp(prefix="geo-check-")
        self.n = 0

    def close(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def fetch(self, url, ua=UA_TOOL, follow=False, head=False, ranged=False):
        self.n += 1
        hdr = os.path.join(self.tmp, "h%d" % self.n)
        body = os.path.join(self.tmp, "b%d" % self.n)
        cmd = ["curl", "-q", "-sS", "--max-time", str(self.timeout), "--proto", "=http,https",
               "--proto-redir", "=http,https", "--max-filesize", "5000000", "-A", ua, "-D", hdr,
               "-o", os.devnull if head else body, "-w", "%{http_code}\t%{content_type}\t%{url_effective}\t%{num_redirects}"]
        if head:
            cmd.append("--head")
        if ranged:
            cmd += ["-H", "Range: bytes=0-0"]
        if follow:
            cmd += ["-L", "--max-redirs", "5"]
        cmd.append(url)
        try:
            p = subprocess.run(cmd, capture_output=True, timeout=self.timeout + 15)
        except (OSError, subprocess.SubprocessError) as e:
            raise Unreachable("%s: %s" % (where(url), mask(e)))
        if p.returncode != 0:
            msg = mask(p.stderr.decode("utf-8", "replace").strip().replace(url, where(url)))
            raise Unreachable("%s: curl exit %d: %s" % (where(url), p.returncode, clip(msg, 160)))
        r = Resp()
        parts = p.stdout.decode("utf-8", "replace").split("\t")
        try:
            r.status = int(parts[0] or 0)
        except ValueError:
            r.status = 0
        r.ctype = (parts[1] if len(parts) > 1 else "").strip()
        r.final = parts[2] if len(parts) > 2 else url
        try:
            r.redirects = int(parts[3]) if len(parts) > 3 else 0
        except ValueError:
            r.redirects = 0
        try:
            with open(hdr, "r", errors="replace") as fh:
                blocks = [b for b in parse_header_blocks(fh.read()) if b[0] >= 200]
        except OSError:
            blocks = []
        r.headers = blocks[-1][1] if blocks else {}
        r.first_status = blocks[0][0] if blocks else r.status
        r.first_location = (blocks[0][1].get("location", [""])[0]) if blocks else ""
        r.body = ""
        if not head:
            try:
                with open(body, "rb") as fh:
                    r.body = fh.read(5000000).decode("utf-8", "replace")
            except OSError:
                pass
        return r


# ---------------------------------------------------------------- parsing helpers
def parse_robots(text):
    groups, stray, sitemaps = [], [], []
    cur, last_agent = None, False
    for raw in text.lstrip("\ufeff").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        field, value = line.split(":", 1)
        field, value = field.strip().lower(), value.strip()
        if field == "user-agent":
            if cur is None or not last_agent:
                cur = {"agents": [], "rules": []}
                groups.append(cur)
            cur["agents"].append(value)
            last_agent = True
        elif field == "sitemap":
            sitemaps.append(value)
        else:
            (cur["rules"] if cur is not None else stray).append((field, value))
            last_agent = False
    return groups, stray, sitemaps


def meta(text, attr, value):
    for m in re.finditer(r"<meta\b[^>]*>", text, re.I):
        tag = m.group(0)
        a = re.search(r'\b%s\s*=\s*"([^"]*)"' % attr, tag, re.I) or re.search(r"\b%s\s*=\s*'([^']*)'" % attr, tag, re.I)
        if a and a.group(1).strip().lower() == value:
            c = re.search(r'\bcontent\s*=\s*"([^"]*)"', tag, re.I) or re.search(r"\bcontent\s*=\s*'([^']*)'", tag, re.I)
            if c:
                return html.unescape(c.group(1))
    return None


def link_rel(text, rel):
    for m in re.finditer(r"<link\b[^>]*>", text, re.I):
        tag = m.group(0)
        r = re.search(r'\brel\s*=\s*"([^"]*)"', tag, re.I)
        if r and rel in r.group(1).lower().split():
            h = re.search(r'\bhref\s*=\s*"([^"]*)"', tag, re.I)
            if h:
                return html.unescape(h.group(1))
    return None


def ld_items(obj):
    if isinstance(obj, list):
        for o in obj:
            for x in ld_items(o):
                yield x
    elif isinstance(obj, dict):
        if "@graph" in obj:
            for x in ld_items(obj["@graph"]):
                yield x
        else:
            yield obj


def deep_dicts(obj):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            for x in deep_dicts(v):
                yield x
    elif isinstance(obj, list):
        for v in obj:
            for x in deep_dicts(v):
                yield x


def strings_in(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, list):
        for o in obj:
            for s in strings_in(o):
                yield s
    elif isinstance(obj, dict):
        for o in obj.values():
            for s in strings_in(o):
                yield s


def host_of(url):
    try:
        return (urllib.parse.urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""


def path_of(url):
    try:
        return urllib.parse.urlsplit(url).path or "/"
    except ValueError:
        return "/"


def followable(url, base_host):
    """--follow reads links from the site it checks. Request only https links to public host names
    (or links back to the checked host), so a page cannot point this script at a machine on a local network."""
    try:
        sp = urllib.parse.urlsplit(url)
        h = (sp.hostname or "").lower()
    except ValueError:
        return False
    if h == base_host:
        return True
    if sp.scheme != "https" or "." not in h or h.endswith((".local", ".localhost", ".internal")):
        return False
    return not re.fullmatch(r"[0-9.]+|[0-9a-f:]+", h)


def is_xmlish(ctype):
    return "xml" in ctype.lower()


def is_texty(ctype):
    c = ctype.lower()
    return c.startswith("text/plain") or c.startswith("text/markdown")


def is_html(ctype):
    return "html" in ctype.lower()


# ---------------------------------------------------------------- the checks
class Parser(argparse.ArgumentParser):
    """argparse echoes a bad value in its message. Mask it and keep the exit code at 2."""

    def error(self, message):
        self.print_usage(sys.stderr)
        sys.stderr.write("geo-check: %s\n" % mask(message))
        sys.exit(2)


def main():
    ap = Parser(
        prog="geo-check.sh",
        description="Read-only check of the search and AI-visibility layer of one MOI site.",
        epilog="Exit 0 no FAIL, 1 at least one FAIL, 2 bad input or the host could not be reached.")
    ap.add_argument("base")
    ap.add_argument("--page")
    ap.add_argument("--expect-host")
    ap.add_argument("--forbid")
    ap.add_argument("--indexnow-file")
    ap.add_argument("--pages", type=int, default=5)
    ap.add_argument("--follow", action="store_true")
    ap.add_argument("--timeout", type=int, default=25)
    a = ap.parse_args()

    try:
        scheme, host, base = parse_base(a.base)
        if a.page:
            clean_path(a.page, "--page")
        expect_flag = None
        if a.expect_host:
            expect_flag = a.expect_host.strip().lower()
            if not re.fullmatch(r"[a-z0-9]([a-z0-9.-]*[a-z0-9])?", expect_flag):
                raise Bad("--expect-host must be a plain host name such as docs.moi.technology")
        forbid = re.compile(r"markdown-page" + ("|(?:%s)" % a.forbid if a.forbid else ""))
        key_name = None
        if a.indexnow_file:
            key_name = a.indexnow_file.strip()
            if is_env_name(key_name):
                raise Bad("--indexnow-file names an env file. This script never asks a site for one")
            if not re.fullmatch(r"[A-Za-z0-9_-]{8,128}\.txt", key_name):
                raise Bad("--indexnow-file must be the key file name, letters, digits, - or _, ending in .txt")
        if not 1 <= a.pages <= 10:
            raise Bad("--pages must be from 1 to 10")
        if not 1 <= a.timeout <= 120:
            raise Bad("--timeout must be from 1 to 120 seconds")
    except re.error as e:
        sys.stderr.write("geo-check: --forbid is not a valid regular expression: %s\n" % mask(e))
        return 2
    except Bad as e:
        sys.stderr.write("geo-check: %s\n" % e)
        return 2
    if not shutil.which("curl"):
        sys.stderr.write("geo-check: curl was not found. It ships with macOS and most Linux systems. Install it and run again\n")
        return 2

    http = Http(a.timeout)
    results = []

    def say(level, name, detail, notes=()):
        results.append(level)
        print("%s %s: %s" % (level, name, clip(mask(detail))))
        for n in notes:
            print("     note: %s" % clip(mask(n)))

    try:
        return run(a, http, say, results, host, base, expect_flag, forbid, key_name)
    except Unreachable as e:
        sys.stderr.write("geo-check: cannot reach the host: %s\n" % e)
        return 2
    finally:
        http.close()


def run(a, http, say, results, host, base, expect_flag, forbid, key_name):
    print("geo-check: %s" % where(base + "/").rstrip("/"))
    preview = host.endswith(".pages.dev")

    # -- home page and robots.txt first: the expected host may come from robots
    home = http.fetch(base + "/", follow=True)
    expect = expect_flag or host
    if home.status == 200 and is_html(home.ctype):
        say("PASS", "home", "200 %s%s" % (home.ctype.split(";")[0], "" if home.redirects == 0 else " after %d redirect(s) to %s" % (home.redirects, where(home.final))))
    else:
        say("FAIL", "home", "the home page answers %d %s" % (home.status, home.ctype.split(";")[0] or "no content type"))
    if host_of(home.final) and host_of(home.final) != host:
        say("WARN", "home-redirect", "the home page redirects to another host: %s" % where(home.final))

    rob = http.fetch(base + "/robots.txt", follow=True)
    groups, stray, sitemaps = parse_robots(rob.body) if rob.status == 200 and not is_html(rob.ctype) else ([], [], [])
    if preview and not expect_flag and sitemaps:
        expect = host_of(sitemaps[0]) or host
    notes = []
    if expect != host:
        notes.append("judging links against %s (%s)" % (expect, "the --expect-host option" if expect_flag else "the robots Sitemap line, because a preview points at production on purpose"))
    if rob.status != 200:
        say("FAIL", "robots", "/robots.txt answers %d. No file, so no Content-Signal and no sitemap line" % rob.status)
    elif is_html(rob.ctype):
        say("FAIL", "robots", "/robots.txt answers 200 %s: an HTML page standing in for the file (a soft 200). Content type should be text/plain" % rob.ctype.split(";")[0])
    else:
        sig_all = [(g, [v for f, v in g["rules"] if f == "content-signal"]) for g in groups]
        signal_lines = [v for g, vs in sig_all for v in vs] + [v for f, v in stray if f == "content-signal"]
        stray_rules = [f for f, v in stray if f in ("content-signal", "allow", "disallow")]
        named = [g for g in groups if g["agents"] != ["*"]]
        star = [g for g in groups if "*" in g["agents"]]
        if not is_texty(rob.ctype):
            say("WARN", "robots-type", "content type is %s, expected text/plain" % (rob.ctype.split(";")[0] or "empty"))
        if stray_rules:
            say("FAIL", "robots-placement", "%s line(s) sit before any User-agent line, so they attach to no crawler. Content-Signal must be inside a group" % ", ".join(sorted(set(stray_rules))))
        if not groups:
            if signal_lines:
                say("FAIL", "robots", "a Content-Signal line exists but there is no User-agent group to hold it", notes)
            else:
                say("WARN", "robots", "no User-agent group and no Content-Signal line: the file sets no rules (crawling is allowed by default, but no AI-use policy is stated)", notes)
        else:
            block_all = [g for g in star if ("disallow", "/") in g["rules"]]
            if block_all:
                say("FAIL", "robots-block", "the * group has Disallow: /, which blocks every crawler")
            if len(groups) == 1 and star:
                if signal_lines:
                    say("PASS", "robots", "one group (*) and the Content-Signal line is inside it: %s" % signal_lines[0], notes)
                else:
                    say("WARN", "robots", "one group (*) and no Content-Signal line. The repo files for the docs sites set one", notes)
            else:
                lacking = [g for g in named if not any(f == "content-signal" for f, v in g["rules"])]
                star_has = any(f == "content-signal" for g in star for f, v in g["rules"])
                names = ", ".join(a_ for g in lacking for a_ in g["agents"])[:120]
                if not signal_lines:
                    say("WARN", "robots", "%d groups and no Content-Signal line anywhere. The docs sites' files carry one, in a single * group" % len(groups), notes)
                elif lacking:
                    say("WARN", "robots", "%d groups; these named crawlers have no Content-Signal of their own and ignore the * group's: %s" % (len(groups), names), notes)
                else:
                    say("PASS", "robots", "%d groups and every one carries a Content-Signal line%s" % (len(groups), "" if star_has else " (none for *)"), notes)
            blocked = [a_ for g in named if ("disallow", "/") in g["rules"] for a_ in g["agents"]]
            if blocked:
                say("WARN", "robots-named-block", "these crawlers are blocked with Disallow: /: %s. Check that this is a decision" % ", ".join(blocked)[:120])
        if sitemaps:
            say("PASS", "robots-sitemap", "%d Sitemap line(s): %s" % (len(sitemaps), ", ".join(sorted(set(host_of(s) for s in sitemaps)))))
        else:
            say("WARN", "robots-sitemap", "no Sitemap line in robots.txt")

    # -- AI crawler access
    seen, bad = [], False
    for label, ua in CRAWLERS:
        r = http.fetch(base + "/", ua=ua, follow=True)
        seen.append("%s %d" % (label, r.status))
        bad = bad or r.status != 200
    codes = [s.split()[-1] for s in seen]
    blocked_codes = [c for c in codes if c in ("401", "403", "429", "503")]
    if not bad:
        say("PASS", "ai-crawlers", "the home page answers 200 to each user-agent name: " + ", ".join(seen))
    elif blocked_codes:
        say("FAIL", "ai-crawlers", "a crawler name is refused: " + ", ".join(seen), ["a Cloudflare bot or WAF setting can do this. cocolang.dev was blocked this way until 2026-09-09"])
    else:
        say("WARN", "ai-crawlers", "not all 200: " + ", ".join(seen))

    # -- llms.txt and llms-full.txt
    llms = http.fetch(base + "/llms.txt", follow=True)
    llms_paths = []
    if llms.status != 200:
        say("FAIL", "llms.txt", "/llms.txt answers %d" % llms.status)
    elif is_html(llms.ctype):
        say("FAIL", "llms.txt", "/llms.txt answers 200 text/html: an HTML page standing in for the file (a soft 200)")
    else:
        lines = llms.body.splitlines()
        first = next((l for l in lines if l.strip()), "")
        entries = [l for l in lines if re.match(r"\s*-\s*\[", l)]
        docs_at = next((i for i, l in enumerate(lines) if re.match(r"##\s+documentation\b", l, re.I)), None)
        if docs_at is not None:  # count the pages, not the sibling-site list that follows
            end = next((i for i in range(docs_at + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
            entries = [l for l in lines[docs_at + 1:end] if re.match(r"\s*-\s*\[", l)]
        if not is_texty(llms.ctype):
            say("WARN", "llms.txt-type", "content type is %s, expected text/plain" % (llms.ctype.split(";")[0] or "empty"))
        if not first.startswith("# "):
            say("WARN", "llms.txt", "200, but the first line is not a '# Title' heading")
        elif not entries:
            say("WARN", "llms.txt", "200 with a title but no '- [name](url)' entries")
        else:
            counts = {}
            for l in entries:
                m = re.search(r"\]\((https?://[^)\s]+)\)", l)
                if m:
                    counts[host_of(m.group(1))] = counts.get(host_of(m.group(1)), 0) + 1
                    if host_of(m.group(1)) in (host, expect):
                        llms_paths.append(path_of(m.group(1)))
            top = max(counts, key=counts.get) if counts else ""
            agent_block = bool(re.search(r"(?im)^#+\s*instructions for ai agents", llms.body))
            det = "%d entries, most point at %s; %s" % (len(entries), top or "no host", "has an 'Instructions for AI agents' block" if agent_block else "no 'Instructions for AI agents' block")
            if top and top != expect:
                say("WARN", "llms.txt", det + ". Expected " + expect + ". Fine for an index of other sites, wrong for a docs site")
            else:
                say("PASS" if agent_block else "WARN", "llms.txt", det)
    full = http.fetch(base + "/llms-full.txt", follow=True)
    if full.status != 200:
        say("WARN", "llms-full.txt", "answers %d (not every site has one)" % full.status)
    elif is_html(full.ctype):
        say("FAIL", "llms-full.txt", "answers 200 text/html: a soft 200")
    else:
        jsx = [l for l in full.body.splitlines() if re.match(r"\s*</?[A-Z][A-Za-z]*[\s/>]", l)]
        if jsx:
            say("WARN", "llms-full.txt", "%d KB, %d line(s) look like JSX (possibly inside a code sample): the generator's DROPPED_COMPONENTS list may need a name" % (len(full.body) // 1024, len(jsx)))
        else:
            say("PASS", "llms-full.txt", "%d KB, no raw JSX lines" % (len(full.body) // 1024))

    # -- sitemap
    cands, seen_c = [], set()
    for s in sitemaps[:5]:
        if host_of(s) in (host, expect, ""):
            p = path_of(s)
            if p not in seen_c:
                cands.append(p)
                seen_c.add(p)
    for p in ("/sitemap.xml", "/sitemap-index.xml"):
        if p not in seen_c:
            cands.append(p)
    sm, sm_path, tried = None, "", []
    for p in cands:
        r = http.fetch(base + p, follow=True)
        if r.status == 200 and is_xmlish(r.ctype) and "<loc" in r.body:
            sm, sm_path = r, p
            break
        tried.append("%s %d%s" % (p, r.status, " " + r.ctype.split(";")[0] if r.status == 200 else ""))
    locs = []
    if sm is None:
        say("FAIL", "sitemap", "no sitemap found (%s). A 200 text/html answer is a soft 200, not a sitemap" % ", ".join(tried[:4]))
    else:
        bodies = [sm.body]
        if "<sitemapindex" in sm.body:
            kids = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sm.body)[:5]
            bodies = []
            for k in kids:
                if host_of(k) in (host, expect):
                    kr = http.fetch(base + path_of(k), follow=True)
                    if kr.status == 200:
                        bodies.append(kr.body)
                else:
                    locs.append(k)  # a child on another host is not fetched, but it counts as a foreign address
        for b in bodies:
            locs += [html.unescape(x) for x in re.findall(r"<loc>\s*([^<]+?)\s*</loc>", b)]
        hosts = {}
        for l in locs:
            hosts[host_of(l)] = hosts.get(host_of(l), 0) + 1
        foreign = {h: c for h, c in hosts.items() if h != expect}
        stub = [path_of(l) for l in locs if forbid.search(l)]
        dup = len(locs) - len(set(locs))
        insecure = [l for l in locs if l.startswith("http://")]
        det = "%s: %d addresses" % (sm_path, len(locs))
        if not locs:
            say("FAIL", "sitemap", det + ", none readable")
        elif foreign:
            say("FAIL", "sitemap", det + ", but %d are on another host: %s. Expected %s" % (sum(foreign.values()), ", ".join("%s (%d)" % (h, c) for h, c in sorted(foreign.items()))[:150], expect))
        else:
            say("PASS", "sitemap", det + ", all on " + expect)
        if stub:
            say("FAIL", "sitemap-stubs", "a template sample or forbidden page is listed: %s" % ", ".join(stub[:4]))
        if dup:
            say("WARN", "sitemap-duplicates", "%d address(es) listed twice" % dup)
        if insecure:
            say("WARN", "sitemap-http", "%d address(es) use http" % len(insecure))

    # -- llms.txt against the sitemap: a page the sitemap leaves out (a noindex stub) should not be in llms.txt either
    if llms_paths and locs:
        in_map = set(path_of(l).rstrip("/") or "/" for l in locs)
        extra = [p for p in dict.fromkeys(llms_paths) if (p.rstrip("/") or "/") not in in_map]
        if extra:
            say("WARN", "llms-vs-sitemap", "%d page(s) are in llms.txt but not in the sitemap, for example %s. A noindex stub should be in neither" % (len(extra), ", ".join(extra[:3])))
        else:
            say("PASS", "llms-vs-sitemap", "every llms.txt page on this host is also in the sitemap")

    # -- sample pages
    def depth(p):
        return len([s for s in p.split("/") if s])

    pool = list(dict.fromkeys(path_of(l) for l in locs if depth(path_of(l)) >= 1 and not path_of(l).endswith(".xml")))  # paths only: they are requested from the base host
    # prefer a real page three levels deep over a section index, and never a generated /category/ or /tags/ index
    ranked = sorted(pool, key=lambda p: (bool(re.search(r"/(?:category|tags?)/", p)), -min(depth(p), 3)))
    sample = a.page or (ranked[0] if ranked else "/")
    others = []
    if pool and a.pages > 1:
        step = max(1, len(pool) // a.pages)
        others = [p for p in pool[::step] if p != sample][: a.pages - 1]
    if not a.page and not pool:
        say("WARN", "sample-page", "the sitemap gave no page to sample, so the home page is the sample")
    page = http.fetch(base + sample, follow=True)
    first_note = []
    if page.redirects and page.first_status in (301, 302, 307, 308):
        first_note.append("%s answers %d and redirects to %s" % (sample, page.first_status, where(page.first_location or page.final)))
    if page.status != 200 or not is_html(page.ctype):
        say("FAIL", "page", "sample %s answers %d %s" % (sample, page.status, page.ctype.split(";")[0]))
        text = ""
    else:
        say("PASS", "page", "sample %s answers 200 text/html" % sample, first_note)
        text = page.body
    final_path = path_of(page.final)
    if text:
        t = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
        title = html.unescape(t.group(1)).strip() if t else ""
        if not title:
            say("FAIL", "title", "no <title>")
        elif len(title) > 60:
            say("WARN", "title", "%d characters; the docs standard says up to 60" % len(title))
        else:
            say("PASS", "title", "%d characters" % len(title))
        d = meta(text, "name", "description")
        if not d or not d.strip():
            say("FAIL", "description", "no meta description")
        elif 130 <= len(d) <= 170:
            say("PASS", "description", "%d characters (140 to 160 is the target, 130 to 170 is tolerated)" % len(d))
        else:
            say("WARN", "description", "%d characters; the target is 140 to 160" % len(d))
        c = link_rel(text, "canonical")
        if not c:
            say("FAIL", "canonical", "no <link rel=canonical>")
        elif host_of(c) != expect:
            say("FAIL", "canonical", "points at %s, expected %s (%s)" % (host_of(c), expect, where(c)))
        elif path_of(c) == final_path:
            say("PASS", "canonical", "%s matches the address served" % where(c))
        elif path_of(c).rstrip("/") == final_path.rstrip("/"):
            say("WARN", "canonical", "differs from the address served only by a trailing slash: canonical %s, served %s. Set trailingSlash explicitly (the style guide, appendix step 2)" % (path_of(c), final_path))
        else:
            say("WARN", "canonical", "canonical path %s differs from the served path %s" % (path_of(c), final_path))
        mr = meta(text, "name", "robots")
        if mr and "noindex" in mr.lower():
            say("FAIL", "meta-robots", "a page listed in the sitemap says noindex (%s)" % mr)
        xr = " ".join(page.headers.get("x-robots-tag", []) + home.headers.get("x-robots-tag", []))
        if "noindex" in xr.lower():
            if preview:
                say("PASS", "x-robots-tag", "noindex header on a *.pages.dev preview, as Cloudflare Pages sends on previews (seen 2026-10-03). The real host must not send it")
            else:
                say("FAIL", "x-robots-tag", "an X-Robots-Tag noindex header is served on this host")
        ogt, ogi, tw = meta(text, "property", "og:title"), meta(text, "property", "og:image"), meta(text, "name", "twitter:card")
        missing = [n for n, v in (("og:title", ogt), ("og:image", ogi), ("twitter:card", tw)) if not v]
        if missing:
            say("WARN", "share-tags", "missing: " + ", ".join(missing))
        elif host_of(ogi) in (host, expect) or ogi.startswith("/"):
            img = http.fetch(base + path_of(ogi), follow=True, ranged=True)
            ok = img.status in (200, 206) and img.ctype.lower().startswith("image/")
            say("PASS" if ok else "FAIL", "share-image", "%s answers %d %s" % (path_of(ogi), img.status, img.ctype.split(";")[0]))
        else:
            say("PASS", "share-tags", "og:title, og:image and twitter:card present (image is on %s, not requested)" % host_of(ogi))
        blocks = re.findall(r"<script[^>]*type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>", text, re.S | re.I)
        types, dates, enc, bad_json, org_ids, has_org = [], [], 0, 0, [], False
        for b in blocks:
            try:
                obj = json.loads(b)
            except ValueError:
                bad_json += 1
                continue
            for s in strings_in(obj):
                if re.search(r"&(?:#x?[0-9a-fA-F]+|amp|quot|apos|lt|gt);", s):
                    enc += 1
            for it in ld_items(obj):
                tp = it.get("@type")
                types += tp if isinstance(tp, list) else [tp]
                if it.get("dateModified"):
                    dates.append(str(it["dateModified"]))
            for it in deep_dicts(obj):
                tp = it.get("@type")
                if tp == "Organization" or (isinstance(tp, list) and "Organization" in tp):
                    has_org = True
                    if it.get("@id"):
                        org_ids.append(it["@id"])
        types = [str(t) for t in types if t]
        if not blocks:
            say("FAIL", "json-ld", "no JSON-LD on the page")
        elif bad_json:
            say("FAIL", "json-ld", "%d of %d JSON-LD block(s) do not parse" % (bad_json, len(blocks)))
        else:
            say("PASS", "json-ld", "%d block(s) parse; types: %s" % (len(blocks), ", ".join(sorted(set(types))) or "none"))
        if blocks and not bad_json:
            if not has_org:
                say("WARN", "json-ld-org", "no Organization anywhere in the JSON-LD, so the page is not tied to the MOI entity")
            elif org_ids and ORG_ID not in org_ids:
                say("WARN", "json-ld-org", "Organization @id is %s, expected %s" % (org_ids[0], ORG_ID))
            if enc:
                say("WARN", "json-ld-encoding", "%d string(s) hold HTML entities such as &#x27; (the entity-encoding bug of 2026-09)" % enc)
        if dates:
            all_dates = [dates[0]]
            for p in others:
                r = http.fetch(base + p, follow=True)
                m = re.findall(r'"dateModified"\s*:\s*"([^"]+)"', r.body) if r.status == 200 else []
                if m:
                    all_dates.append(m[0])
            if len(all_dates) >= 3 and len(set(all_dates)) == 1:
                say("WARN", "date-modified", "all %d sampled pages share dateModified %s. Either the build ran on a shallow git clone, or one commit touched every page. Compare with git log -1 --format=%%cI -- <source file> (references/verify-locally.md)" % (len(all_dates), all_dates[0][:19]))
            else:
                say("PASS", "date-modified", "%d sampled page(s), %d distinct dateModified value(s)" % (len(all_dates), len(set(all_dates))))
        elif "TechArticle" in types:
            say("WARN", "date-modified", "TechArticle without dateModified. The injector leaves it out when git history is unavailable")
        # markdown copy
        stem = final_path.rstrip("/") or "/index"
        md_paths = [stem + ".md"] if stem != "/index" else ["/index.md"]
        md_paths.append((final_path.rstrip("/") + "/index.md") if final_path != "/" else "/index.md")
        found = []
        for mp in dict.fromkeys(md_paths):
            r = http.fetch(base + mp, follow=True)
            if r.status == 200 and is_html(r.ctype):
                say("FAIL", "markdown-copy", "%s answers 200 text/html: a soft 200, not a markdown file" % mp)
                found = None
                break
            if r.status == 200 and (r.ctype.lower().startswith("text/")):
                found.append(mp)
        if found:
            say("PASS", "markdown-copy", "served at " + ", ".join(found))
        elif found is not None:
            say("WARN", "markdown-copy", "no .md copy at %s. Docusaurus and Sphinx docs sites generate one; the apps do not" % " or ".join(dict.fromkeys(md_paths)))
        # discovery links
        link_hdr = " ".join(home.headers.get("link", []))
        home_text = home.body if is_html(home.ctype) else ""
        if "llms-txt" in link_hdr:
            say("PASS", "link-header", "the Link response header advertises llms-txt")
        elif link_rel(home_text, "llms-txt"):
            say("PASS", "link-header", "no Link header, but the home page carries a <link rel=llms-txt> element")
        else:
            say("WARN", "link-header", "no llms-txt link in the response headers or the page head. A _headers file only works on Cloudflare Pages")

    # -- well-known
    cat_urls, links = [], []
    r = http.fetch(base + "/.well-known/api-catalog", follow=True)
    if r.status == 404:
        say("WARN", "api-catalog", "absent. Only a site with an API reference needs one")
    elif is_html(r.ctype) or r.status != 200:
        say("FAIL" if r.status == 200 else "WARN", "api-catalog", "answers %d %s%s" % (r.status, r.ctype.split(";")[0], " (a soft 200)" if is_html(r.ctype) else ""))
    else:
        ct = r.ctype.split(";")[0].strip().lower()
        try:
            data = json.loads(r.body)
            ls = data.get("linkset") if isinstance(data, dict) else None
        except ValueError:
            ls = None
        if not isinstance(ls, list):
            say("FAIL", "api-catalog", "200 %s but the body is not a JSON object with a linkset array" % ct)
        else:
            for item in ls:
                for v in (item.values() if isinstance(item, dict) else []):
                    if isinstance(v, list):
                        links += [x["href"] for x in v if isinstance(x, dict) and isinstance(x.get("href"), str)]
            if ct == "application/linkset+json":
                say("PASS", "api-catalog", "application/linkset+json, %d link(s)" % len(links))
            else:
                say("FAIL", "api-catalog", "served as %s, RFC 9727 wants application/linkset+json (the _headers rule is missing or ignored)" % (ct or "no type"))
    r = http.fetch(base + "/.well-known/agent-skills/index.json", follow=True)
    if r.status == 404:
        say("WARN", "agent-skills", "absent. A site that offers no skill package does not need one")
    elif is_html(r.ctype) or r.status != 200:
        say("FAIL" if r.status == 200 else "WARN", "agent-skills", "answers %d %s%s" % (r.status, r.ctype.split(";")[0], " (a soft 200)" if is_html(r.ctype) else ""))
    else:
        try:
            data = json.loads(r.body)
            sk = data.get("skills") if isinstance(data, dict) else None
        except ValueError:
            sk = None
        if not isinstance(sk, list):
            say("FAIL", "agent-skills", "200 but the body is not a JSON object with a skills array")
        else:
            incomplete = [str(s.get("name", "?")) if isinstance(s, dict) else "?" for s in sk
                          if not (isinstance(s, dict) and s.get("download") and s.get("documentation"))]
            for s in sk:
                if isinstance(s, dict):
                    links += [s[k] for k in ("download", "documentation") if isinstance(s.get(k), str)]
            if incomplete:
                say("WARN", "agent-skills", "%d skill(s); these lack a download or documentation link: %s" % (len(sk), ", ".join(incomplete)))
            else:
                say("PASS", "agent-skills", "%d skill(s), each with a download and a documentation link" % len(sk))
    if a.follow:
        for u in list(dict.fromkeys(links))[:20]:
            if not re.match(r"^https?://", u):
                say("WARN", "link", "not an absolute address: %s" % where(u))
                continue
            if not followable(u, host):
                say("WARN", "link", "not requested (only https links to public host names are followed): %s" % where(u))
                continue
            try:
                lr = http.fetch(u, follow=True, head=True)
                if lr.status in (403, 405, 501):
                    lr = http.fetch(u, follow=True, ranged=True)
            except Unreachable as e:  # a dead link is a finding, not the end of the run
                say("FAIL", "link", "%s cannot be reached (%s)" % (where(u), clip(str(e), 120)))
                continue
            say("PASS" if lr.status in (200, 206) else "FAIL", "link", "%s answers %d" % (where(u), lr.status))

    # -- 404 behaviour
    probe = "/geo-check-probe-%d" % int(time.time())
    r = http.fetch(base + probe)
    if r.status == 404:
        say("PASS", "404-behaviour", "an unknown address answers 404")
    elif 300 <= r.status < 400:
        say("WARN", "404-behaviour", "an unknown address answers %d (redirect). Judge files by content type, not status" % r.status)
    else:
        say("WARN", "404-behaviour", "an unknown address answers %d: a soft-200 fallback. A status check proves little here; read content types and bodies" % r.status)

    # -- IndexNow
    if key_name:
        r = http.fetch(base + "/" + key_name, follow=True)
        stem = key_name[:-4]
        if r.status == 200 and not is_html(r.ctype) and r.body.strip() == stem:
            say("PASS", "indexnow-key", "the key file is served and its body matches its name (name not printed)")
        elif r.status == 200 and not is_html(r.ctype):
            say("FAIL", "indexnow-key", "the key file is served but its body does not match its name")
        else:
            say("FAIL", "indexnow-key", "the key file answers %d %s" % (r.status, r.ctype.split(";")[0]))

    n_fail, n_warn, n_pass = results.count("FAIL"), results.count("WARN"), results.count("PASS")
    print("geo-check: %d PASS, %d WARN, %d FAIL (%d requests)" % (n_pass, n_warn, n_fail, http.n))
    not_checked = ["what Google or Bing has indexed", "how the real crawlers are treated (this machine is not their address range)",
                   "pages that need JavaScript to show content", "Search Console and Bing submissions"]
    if not key_name:
        not_checked.append("the IndexNow key file (pass --indexnow-file NAME)")
    if not a.follow:
        not_checked.append("links inside the catalog and skills index (pass --follow)")
    print("not checked: " + "; ".join(not_checked))
    return 1 if n_fail else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.stderr.write("geo-check: interrupted\n")
        sys.exit(2)
    except SystemExit:
        raise
    except Exception as e:  # never a traceback
        sys.stderr.write("geo-check: unexpected error: %s: %s\n" % (type(e).__name__, mask(e)))
        sys.exit(2)
PY
