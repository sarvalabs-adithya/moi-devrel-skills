#!/usr/bin/env python3
"""check-live.py: read-only check that a MOI blog post is live and listed, after the merge and the deploy.

Usage (SKILLS is the folder that holds the moi-* skills):
    python3 "$SKILLS/moi-blog/scripts/check-live.py" <slug> [--origin URL] [--apex URL] [--expect-cover] [--expect-gone]

    <slug>          the post's filename without .md, for example moi-september-2026-release
    --origin URL    the blog host (default https://blog.moi.technology)
    --apex URL      the marketing site that carries the /blog listing (default https://moi.technology)
    --expect-cover  fail when the page has no og:image (use it when the post sets `cover`)
    --expect-gone   the opposite check, for a deleted post: it passes only when the article answers 404 and
                    the slug is absent from llms.txt, the sitemap, both feeds and the listing

Checks, each printed as PASS, FAIL, WARN or INFO:
    the article answers 200 with one H1, a canonical URL on the blog host, a description, Article JSON-LD
    (and FAQPage when the page has a FAQ), no placeholder text; og:image, and that the image itself loads
    the slug is in llms.txt, the sitemap, rss.xml, rss-email.xml (tagged utm_campaign=<slug>) and the
    listing at <apex>/blog. A post that is live but missing from the listing means the root build did not run.
    an unknown address on the blog host answers 404 (WARN if it answers 200: then judge a delete by the page text)

It sends HTTP GET requests only (through curl when it is installed, else urllib), and only to http or https
addresses. It never posts, logs in, or writes a file, and it needs no key. A query string in any address it prints is
replaced by <query hidden>.
On a pull request preview (--origin https://pr-<N>-blog.preview.moi.technology) the canonical check fails by design,
because the site hardcodes the production host as canonical, and the apex listing check reads production. Use this
script after the merge. Read a preview by hand (references/publishing.md).
Exit codes: 0 no FAIL, 1 at least one FAIL, 2 bad usage or the host could not be reached.
Python 3 standard library only.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

UA = {"User-Agent": "moi-blog-check-live/1.0 (read-only)"}


class Unreachable(Exception):
    pass


def mask(s):
    """Hide the query string and any user:password part of an address before it is printed."""
    s = re.sub(r"(https?://)[^/\s:@]+:[^/\s@]+@", r"\1<masked>@", str(s))
    return re.sub(r"\?[^\s]*", "?<query hidden>", s)


def get(url):
    """GET one URL. Uses curl when it is installed (the system certificate store, and macOS ships it), else urllib."""
    if shutil.which("curl"):
        mark = "__CHECK_LIVE_META__"
        try:
            r = subprocess.run(["curl", "-sS", "-L", "--max-redirs", "5", "--max-time", "25",
                                "--proto", "=http,https", "--proto-redir", "=http,https", "-A", UA["User-Agent"],
                                "-w", "\n" + mark + "%{http_code}|%{content_type}", url],
                               capture_output=True, timeout=40)
        except (OSError, subprocess.SubprocessError) as e:
            raise Unreachable("%s: %s" % (mask(url), mask(e)))
        if r.returncode != 0:
            raise Unreachable("%s: curl exit %d: %s" % (mask(url), r.returncode, mask(r.stderr.decode("utf-8", "replace").strip())))
        out = r.stdout.decode("utf-8", "replace")
        body, _, meta = out.rpartition("\n" + mark)
        code, _, ctype = meta.partition("|")
        return int(code or 0), ctype.strip(), body
    req = urllib.request.Request(url, headers=UA, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.headers.get("Content-Type", ""), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8", "replace")
        except Exception:
            body = ""
        return e.code, e.headers.get("Content-Type", "") if e.headers else "", body
    except (urllib.error.URLError, OSError) as e:
        raise Unreachable("%s: %s" % (mask(url), mask(getattr(e, "reason", e))))


def main():
    ap = argparse.ArgumentParser(description="Read-only live check of a MOI blog post.",
                                 epilog="Exit 0 no FAIL, 1 a FAIL, 2 bad usage or host unreachable.")
    ap.add_argument("slug")
    ap.add_argument("--origin", default="https://blog.moi.technology")
    ap.add_argument("--apex", default="https://moi.technology")
    ap.add_argument("--expect-cover", action="store_true")
    ap.add_argument("--expect-gone", action="store_true")
    a = ap.parse_args()
    if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", a.slug):
        sys.stderr.write("check-live: the slug is the file name without .md, lowercase with hyphens\n")
        return 2
    origin, apex = a.origin.rstrip("/"), a.apex.rstrip("/")
    for flag, value in (("--origin", origin), ("--apex", apex)):
        if not re.match(r"^https?://[^/\s]+", value):
            sys.stderr.write("check-live: %s must be an http:// or https:// address\n" % flag)
            return 2
    path = "/article/%s/" % a.slug
    url = origin + path
    results = []

    def say(level, name, detail):
        results.append(level)
        print("%s %s: %s" % (level, name, mask(detail)))

    try:
        status, ctype, html = get(url)
        in_files = {}
        for label, u in (("llms.txt", origin + "/llms.txt"), ("rss.xml", origin + "/rss.xml"),
                         ("rss-email.xml", origin + "/rss-email.xml"), ("listing", apex + "/blog")):
            st, _, txt = get(u)
            in_files[label] = (st, txt)
        st, _, idx = get(origin + "/sitemap-index.xml")
        sitemap_hit, sitemap_status = False, st
        if st == 200:
            for loc in re.findall(r"<loc>([^<]+)</loc>", idx):
                if not re.match(r"^https?://", loc.strip()):
                    continue
                st2, _, sm = get(loc.strip())
                if st2 == 200 and path in sm:
                    sitemap_hit = True
        soft_status, _, _ = get(origin + "/article/%s-no-such-page/" % a.slug)
    except Unreachable as e:
        sys.stderr.write("check-live: cannot reach the host: %s\n" % e)
        return 2

    if a.expect_gone:
        say("PASS" if status == 404 else "FAIL", "article-gone", "%s answers %d (want 404)" % (url, status))
        for label, (st, txt) in in_files.items():
            if st != 200:
                say("WARN", label, "answered %d, so absence cannot be judged" % st)
            else:
                say("FAIL" if path in txt else "PASS", label, "slug %s" % ("still listed" if path in txt else "absent"))
        say("PASS" if not sitemap_hit else "FAIL", "sitemap", "slug %s" % ("still listed" if sitemap_hit else "absent"))
        return 1 if "FAIL" in results else 0

    if status != 200:
        say("FAIL", "article", "%s answers %d (want 200)" % (url, status))
    else:
        say("PASS", "article", "200 %s" % ctype.split(";")[0])
        h1 = len(re.findall(r"<h1[\s>]", html))
        say("PASS" if h1 == 1 else "FAIL", "h1", "%d H1 on the page (want 1)" % h1)
        m = re.search(r'<link rel="canonical" href="([^"]+)"', html)
        say("PASS" if m and m.group(1) == url else "FAIL", "canonical", "%s (want %s)" % (m.group(1) if m else "none", url))
        d = re.search(r'<meta name="description" content="([^"]*)"', html)
        say("PASS" if d and d.group(1).strip() else "FAIL", "description", "%d characters" % (len(d.group(1)) if d else 0))
        blocks = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S)
        types = []
        for b in blocks:
            try:
                j = json.loads(b)
            except ValueError:
                say("FAIL", "json-ld", "a JSON-LD block does not parse")
                continue
            for item in (j if isinstance(j, list) else [j]):
                if isinstance(item, dict):
                    types.append(item.get("@type"))
        say("PASS" if "Article" in types else "FAIL", "json-ld", "types found: %s" % (", ".join(map(str, types)) or "none"))
        if 'class="faq"' in html or 'aria-label="Frequently asked questions"' in html:
            say("PASS" if "FAQPage" in types else "FAIL", "faq-json-ld", "the page shows a FAQ; FAQPage %s" % ("present" if "FAQPage" in types else "missing"))
        if re.search(r"<<<|&lt;&lt;&lt;|REPLACE-WITH|RELEASE_URL|LUMA_URL|CANONICAL_URL|\bTODO\b", html):  # slop-lint:ignore
            say("FAIL", "placeholder", "placeholder text is on the live page")
        else:
            say("PASS", "placeholder", "none found")
        og = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        if og:
            try:
                ist, ict, _ = get(og.group(1))
            except Unreachable as e:
                ist, ict = 0, str(e)
            ok = ist == 200 and ict.lower().startswith("image/")
            say("PASS" if ok else "FAIL", "og:image", "%s answers %d %s" % (og.group(1), ist, ict.split(";")[0]))
        elif a.expect_cover:
            say("FAIL", "og:image", "none on the page, but --expect-cover was given")
        else:
            say("INFO", "og:image", "none: no `cover` is set, so shares show a text-only card")

    for label, (st, txt) in in_files.items():
        if st != 200:
            say("FAIL", label, "answered %d" % st)
            continue
        ok = path in txt
        if label == "rss-email.xml" and ok:
            tagged = "utm_campaign=%s" % a.slug in txt and "utm_source=newsletter" in txt
            say("PASS" if tagged else "FAIL", label, "slug listed, newsletter tags %s" % ("present" if tagged else "missing"))
        elif label == "listing" and not ok and status == 200:
            say("FAIL", label, "%s/blog does not link the post: it is live but unlisted; the root build did not run on the deploy" % apex)
        else:
            say("PASS" if ok else "FAIL", label, "slug %s" % ("listed" if ok else "missing"))
    if sitemap_status != 200:
        say("FAIL", "sitemap", "sitemap-index.xml answered %d" % sitemap_status)
    else:
        say("PASS" if sitemap_hit else "FAIL", "sitemap", "slug %s" % ("listed" if sitemap_hit else "missing"))
    say("PASS" if soft_status == 404 else "WARN", "404-behaviour", "an unknown article address answers %d%s" % (soft_status, "" if soft_status == 404 else " (a deleted post would not return 404 here; read the page text instead)"))

    sys.stdout.flush()
    print("check-live: %d FAIL, %d WARN" % (results.count("FAIL"), results.count("WARN")), file=sys.stderr)
    return 1 if "FAIL" in results else 0


if __name__ == "__main__":
    sys.exit(main())
