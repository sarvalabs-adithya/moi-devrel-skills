#!/usr/bin/env bash
# web-health.sh: read-only health check of the MOI website (with its blog), the Dataroom and the Points Program.
#
# Usage:   bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" [website|dataroom|points|all] [--timeout SECONDS] [--list]
#          SKILLS is the folder that holds the moi-* skills. Default target: all. Default timeout: 20 seconds a request.
#          --list prints the checks and makes no request.
# Output:  one line per check: LEVEL, product, host, method and path, then the finding.
#            PASS   the check shows the healthy answer
#            WARN   something differs from the healthy answer and is not a recorded fault: look at it
#            KNOWN  a fault already recorded in references/<product>-health.md, shown with the date it was first
#                   recorded and the date it was seen again (today, UTC). Not a new problem. If the fault is gone the
#                   line says PASS and asks you to update the reference
#            FAIL   a check that should pass did not
#          A summary line goes last, then a line naming what this script does not check.
# Exit codes: 0 no FAIL (WARN and KNOWN allowed), 1 at least one FAIL, 2 bad usage, a bad override, or no way to
#             make a request.
#
# Read-only: HTTP GET and HEAD requests to public pages and public JSON endpoints only. It sends no body, no login, no
# key and follows no redirect. It writes no file. It never calls a chat, upload, admin or job route and never prints a
# file_url. Everything printed that came from a response is masked first (long hex, key prefixes, JWTs, long mixed
# tokens, recovery-phrase-shaped runs of 12 or more short words) and cut to length afterwards. It prints the host and
# path of each request and never a query string, because no check uses one.
#
# Test overrides (origins only, http or https, no user name, no path): WEB_HEALTH_WEBSITE, WEB_HEALTH_BLOG,
# WEB_HEALTH_DATAROOM, WEB_HEALTH_POINTS, WEB_HEALTH_POINTS_PREVIEW. They exist so the script can be tested against a
# local stand-in; leave them unset in real use.
# Needs Python 3.9 or newer (standard library only). Uses curl when installed, else urllib.

export PYTHONDONTWRITEBYTECODE=1
exec python3 - "$@" <<'PY'
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

TODAY = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
UA = "moi-devrel-web-products-web-health/1.0 (read-only)"
DEFAULT_ORIGINS = {
    "WEB_HEALTH_WEBSITE": "https://moi.technology",
    "WEB_HEALTH_BLOG": "https://blog.moi.technology",
    "WEB_HEALTH_DATAROOM": "https://dataroom.moi.technology",
    "WEB_HEALTH_POINTS": "https://points.moi.technology",
    "WEB_HEALTH_POINTS_PREVIEW": "https://preview.points.moi.technology",
}
POINTS_ORIGIN = "https://points.moi.technology"

# Faults already on record. since = first date the evidence records it. ref = where it is described.
KNOWN = {
    "W-K1": ("calendar API answers 500; the related GitHub issue 3 has been open since 2026-04-20", "2026-10-02", "website-health.md"),
    "W-K2": ("the site bundle has the dev host baked in as its API base", "2026-10-02", "website-health.md"),
    "W-K3": ("unknown addresses answer 200 (no real 404)", "2026-10-02", "website-health.md"),
    "W-K4": ("no discovery Link header on the home page", "2026-10-02", "website-health.md"),
    "W-K5": ("PDFs are served without a download header", "2026-10-02", "website-health.md"),
    "D-K1": ("document not fully embedded, so the chat may miss it or be unable to cite it", "2026-10-02", "dataroom-health.md"),
    "D-K2": ("home page shows hard-coded figures that nothing updates", "2026-10-03", "dataroom-health.md"),
    "P-K1": ("health JSON reports sha null, so the running build cannot be told", "2026-10-02", "points-health.md"),
}
KNOWN_STUCK_DOCS = {"gtm deck", "whitepaper", "im deck", "tokenomics overview",
                    "parallelism in shared spaces", "truth of happiness - the vision paper"}

# ---------------------------------------------------------------- masking
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
PHRASE_STOP = frozenset(
    "after and are been being both but could did does each every for from get got had has her here "
    "him his how its let many may most not our out per see she should some than the their them these "
    "those too using via was were which while who why with would yes your".split())
_PIECE = re.compile(r"[A-Za-z]+|[^A-Za-z]+")


def _mask_phrases(s):
    spans, run = [], []

    def close():
        if len(run) >= 12:
            spans.append((run[0][0], run[-1][1]))
        del run[:]

    for m in _PIECE.finditer(s):
        t = m.group(0)
        if t[0].isalpha():
            if 3 <= len(t) <= 8 and t.lower() not in PHRASE_STOP:
                run.append((m.start(), m.end()))
            else:
                close()
        elif re.fullmatch(r"[\s,;]+", t):
            continue
        else:
            close()
    close()
    for a, b in reversed(spans):
        s = s[:a] + "(masked: 12 or more short words, possible recovery phrase)" + s[b:]
    return s


def mask(s):
    s = str(s)
    s = LONG_HEX.sub(lambda m: m.group(0)[:6] + "...(masked)", s)
    for rx in SECRET_SHAPES:
        s = rx.sub(lambda m: m.group(0)[:4] + "...(masked)", s)
    return _mask_phrases(s)


def safe(s, width=90):
    """Mask the whole text first, then cut it: cutting first could leave the front half of a secret."""
    s = mask(" ".join(str(s).split()))
    return s if len(s) <= width else s[:width - 3] + "..."


# ---------------------------------------------------------------- output
COUNTS = {"PASS": 0, "WARN": 0, "KNOWN": 0, "FAIL": 0}
STATE = {"net_fail": 0, "requests": 0}


def emit(level, product, host, method, path, detail):
    COUNTS[level] += 1
    print("%-5s  %-8s  %s %s %s  %s" % (level, product, host, method, path, detail))


def known(kid, product, host, method, path, observed):
    text, since, ref = KNOWN[kid]
    emit("KNOWN", product, host, method, path,
         "%s [%s: %s; first recorded %s, seen again %s; see references/%s]" % (observed, kid, text, since, TODAY, ref))


def fixed(kid, product, host, method, path, observed):
    text, since, ref = KNOWN[kid]
    emit("PASS", product, host, method, path,
         "%s [%s looks fixed: update references/%s and KNOWN in this script]" % (observed, kid, ref))


# ---------------------------------------------------------------- http
class Net(Exception):
    pass


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def http(origin, path, method="GET", maxbytes=5_000_000):
    """One GET or HEAD. Returns (status, headers with lower-case names, body bytes). Never follows a redirect."""
    STATE["requests"] += 1
    url = origin + path
    T = ARGS.timeout
    if shutil.which("curl"):
        cmd = ["curl", "-sS", "--max-time", str(T), "--connect-timeout", str(min(T, 10)),
               "--proto", "=http,https", "--max-filesize", str(maxbytes), "-A", UA,
               "-I" if method == "HEAD" else "-i", url]
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=T + 10)
        except subprocess.TimeoutExpired:
            raise Net("timed out")
        if r.returncode != 0:
            why = {6: "host not found", 7: "connection refused", 28: "timed out", 35: "TLS failed", 60: "TLS certificate not trusted",
                   63: "response too large"}.get(r.returncode, "curl exit %d" % r.returncode)
            raise Net(why)
        raw = r.stdout
        head, sep, body = raw.partition(b"\r\n\r\n")
        if not sep:
            head, sep, body = raw.partition(b"\n\n")
        lines = head.decode("latin-1").splitlines()
        m = re.match(r"HTTP/\S+\s+(\d{3})", lines[0] if lines else "")
        if not m:
            raise Net("not an HTTP answer")
        headers = {}
        for ln in lines[1:]:
            if ":" in ln:
                k, v = ln.split(":", 1)
                headers[k.strip().lower()] = v.strip()
        return int(m.group(1)), headers, body
    opener = urllib.request.build_opener(_NoRedirect)
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
    try:
        try:
            resp = opener.open(req, timeout=T)
            status, hdrs, body = resp.status, {k.lower(): v for k, v in resp.headers.items()}, resp.read(maxbytes + 1)
        except urllib.error.HTTPError as e:
            status, hdrs, body = e.code, {k.lower(): v for k, v in e.headers.items()}, e.read(maxbytes + 1)
    except (urllib.error.URLError, OSError, ValueError) as e:
        why = str(getattr(e, "reason", e))
        if "CERTIFICATE_VERIFY_FAILED" in why:
            why = "TLS certificate not trusted by Python; install curl"
        raise Net(why[:60])
    if len(body) > maxbytes:
        raise Net("response too large")
    return status, hdrs, body


def get(prod, origin, path, method="GET", maxbytes=5_000_000):
    """http() that turns a network error into a FAIL line and returns None."""
    try:
        return http(origin, path, method, maxbytes)
    except Net as e:
        STATE["net_fail"] += 1
        emit("FAIL", prod, host_of(origin), method, path, "no answer: %s" % safe(e, 60))
        return None


def host_of(origin):
    return urllib.parse.urlsplit(origin).netloc


def as_json(body):
    try:
        return json.loads(body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None


# ---------------------------------------------------------------- checks
def check_status(prod, origin, path, want=(200,), method="GET", note=""):
    r = get(prod, origin, path, method)
    if r is None:
        return None
    st, hd, body = r
    h = host_of(origin)
    if st in want:
        emit("PASS", prod, h, method, path, "%d%s" % (st, note))
    else:
        emit("FAIL", prod, h, method, path, "%d, wanted %s" % (st, "/".join(str(w) for w in want)))
    return r


def website():
    O = ORIGINS["WEB_HEALTH_WEBSITE"]
    h = host_of(O)
    home = check_status("website", O, "/")
    for p in ("/why-moi", "/manifesto", "/papers"):
        check_status("website", O, p, note=" (the app shell; this host answers 200 for any address, see W-K3)")
    listing = check_status("website", O, "/blog", note=" (generated listing)")
    for p in ("/sitemap.xml", "/robots.txt"):
        check_status("website", O, p)

    r = get("website", O, "/api/health")
    if r:
        st, hd, body = r
        j = as_json(body)
        if st == 200 and isinstance(j, dict) and j.get("status") == "ok":
            emit("PASS", "website", h, "GET", "/api/health", "200 status ok (the Express server answers behind this host)")
        else:
            emit("FAIL", "website", h, "GET", "/api/health", "%d, body %s" % (st, safe(body[:80].decode("utf-8", "replace"), 60)))

    r = get("website", O, "/api/community-calls")
    if r:
        st, hd, body = r
        j = as_json(body)
        if st == 200 and isinstance(j, list):
            fixed("W-K1", "website", h, "GET", "/api/community-calls", "200 JSON list of %d events" % len(j))
        elif st == 500:
            known("W-K1", "website", h, "GET", "/api/community-calls", "500")
        else:
            emit("FAIL", "website", h, "GET", "/api/community-calls", "%d, not a JSON list and not the recorded 500" % st)

    # the API base baked into the bundle: the homepage calendar and the admin page read it
    if home and home[0] == 200:
        html = home[2].decode("utf-8", "replace")
        m = re.search(r"/assets/index-[A-Za-z0-9_-]+\.js", html)
        if not m:
            emit("WARN", "website", h, "GET", "/", "could not find the main script in the page, so the baked API base was not read")
        else:
            b = get("website", O, m.group(0))
            if b and b[0] == 200:
                text = b[2].decode("utf-8", "replace")
                bases = sorted(set(re.findall(r"https?://[A-Za-z0-9.-]+\.moi\.technology/api\b", text)))
                if any("//dev." in x for x in bases):
                    known("W-K2", "website", h, "GET", "main script", "API base baked in: %s" % safe(", ".join(bases), 80))
                else:
                    fixed("W-K2", "website", h, "GET", "main script", "API base baked in: %s" % (safe(", ".join(bases), 80) or "none, so the page calls its own host"))
            elif b:
                emit("WARN", "website", h, "GET", "main script", "%d, so the baked API base was not read" % b[0])

    r = get("website", O, "/zz-health-check-no-such-page")
    if r:
        st = r[0]
        if st == 404:
            fixed("W-K3", "website", h, "GET", "/zz-health-check-no-such-page", "404")
        elif st == 200:
            known("W-K3", "website", h, "GET", "/zz-health-check-no-such-page", "200 with the app shell")
        else:
            emit("WARN", "website", h, "GET", "/zz-health-check-no-such-page", "%d, neither the 404 nor the recorded 200" % st)

    r = get("website", O, "/", "HEAD")
    if r:
        if "link" in r[1]:
            fixed("W-K4", "website", h, "HEAD", "/", "Link header present")
        else:
            known("W-K4", "website", h, "HEAD", "/", "no Link header")

    r = get("website", O, "/papers/moi-white-paper.pdf", "HEAD")
    if r:
        st, hd, _ = r
        if st != 200:
            emit("FAIL", "website", h, "HEAD", "/papers/moi-white-paper.pdf", "%d, wanted 200" % st)
        elif "content-disposition" in hd:
            fixed("W-K5", "website", h, "HEAD", "/papers/moi-white-paper.pdf", "200 with Content-Disposition")
        else:
            known("W-K5", "website", h, "HEAD", "/papers/moi-white-paper.pdf",
                  "200, %s bytes, no Content-Disposition" % safe(hd.get("content-length", "?"), 12))

    blog(listing)


def blog(listing):
    B = ORIGINS["WEB_HEALTH_BLOG"]
    h = host_of(B)
    check_status("blog", B, "/")
    feed = None
    for p in ("/rss.xml", "/rss-email.xml", "/sitemap-index.xml", "/llms.txt"):
        r = check_status("blog", B, p)
        if r and p == "/rss.xml" and r[0] == 200:
            feed = r[2].decode("utf-8", "replace")
    r = get("blog", B, "/article/zz-health-check-no-such-post/")
    if r:
        if r[0] == 404:
            emit("PASS", "blog", h, "GET", "/article/zz-health-check-no-such-post/", "404 (an unknown article is a real 404 here)")
        else:
            emit("WARN", "blog", h, "GET", "/article/zz-health-check-no-such-post/", "%d, wanted 404: judge a deleted post by its page text" % r[0])
    if feed is not None and listing and listing[0] == 200:
        slugs = re.findall(r"<link>https?://[^<]*/article/([A-Za-z0-9_-]+)/?</link>", feed)
        page = listing[2].decode("utf-8", "replace")
        if not slugs:
            emit("WARN", "blog", h, "GET", "/rss.xml", "no article links found in the feed")
        else:
            miss = [s for s in slugs if s not in page]
            if miss:
                emit("WARN", "blog", h, "GET", "/rss.xml", "%d of %d posts in the feed are not in the apex /blog listing (live but unlisted; run again after the deploy finishes): %s"
                     % (len(miss), len(slugs), safe(", ".join(miss), 70)))
            else:
                emit("PASS", "blog", h, "GET", "/rss.xml", "all %d posts in the feed are in the apex /blog listing" % len(slugs))


def dataroom():
    O = ORIGINS["WEB_HEALTH_DATAROOM"]
    h = host_of(O)
    r = get("dataroom", O, "/")
    if r:
        st, hd, _ = r
        loc = hd.get("location", "")
        if st in (301, 302, 307, 308) and loc.rstrip("/").endswith("/home"):
            emit("PASS", "dataroom", h, "GET", "/", "%d to /home" % st)
        elif st == 200:
            emit("WARN", "dataroom", h, "GET", "/", "200, wanted a redirect to /home")
        else:
            emit("FAIL", "dataroom", h, "GET", "/", "%d, wanted a redirect to /home" % st)
    home = check_status("dataroom", O, "/home")
    r = get("dataroom", O, "/api/documents")
    if r:
        st, hd, body = r
        docs = as_json(body)
        if st != 200 or not isinstance(docs, list):
            emit("FAIL", "dataroom", h, "GET", "/api/documents", "%d, wanted a JSON list" % st)
        elif not docs:
            emit("WARN", "dataroom", h, "GET", "/api/documents", "200 but the list is empty")
        else:
            done = sum(1 for d in docs if isinstance(d, dict) and d.get("embedding_status") == "completed")
            emit("PASS", "dataroom", h, "GET", "/api/documents", "200, %d documents, %d completed" % (len(docs), done))
            bad = [d for d in docs if isinstance(d, dict) and d.get("embedding_status") != "completed"]
            for d in bad:
                title = " ".join(str(d.get("title", "(no title)")).split())
                stt = d.get("embedding_status", "missing")
                if title.lower() in KNOWN_STUCK_DOCS:
                    known("D-K1", "dataroom", h, "GET", "/api/documents", "%s: %s" % (safe(stt, 12), safe(title, 50)))
                else:
                    emit("WARN", "dataroom", h, "GET", "/api/documents",
                         "NEW: %s (status %s), the chat may miss it and it is not on the recorded list" % (safe(title, 50), safe(stt, 12)))
            if not bad:
                emit("PASS", "dataroom", h, "GET", "/api/documents", "every document is completed [D-K1 looks fixed: update references/dataroom-health.md and KNOWN in this script]")
    if home and home[0] == 200:
        page = home[2].decode("utf-8", "replace")
        shown = [x for x in ("4.3K", "14.4K", "50K+", "79.0M") if x in page]
        if shown:
            known("D-K2", "dataroom", h, "GET", "/home", "figures shown: %s" % ", ".join(shown))
        else:
            fixed("D-K2", "dataroom", h, "GET", "/home", "the recorded figures are no longer on the page")


def points():
    O = ORIGINS["WEB_HEALTH_POINTS"]
    h = host_of(O)
    enabled = None
    r = get("points", O, "/api/health")
    if r:
        st, hd, body = r
        j = as_json(body)
        if not isinstance(j, dict):
            emit("FAIL", "points", h, "GET", "/api/health", "%d, body is not JSON" % st)
        else:
            mg = j.get("migrations") if isinstance(j.get("migrations"), dict) else {}
            core = (st == 200 and j.get("healthy") is True and j.get("database") == "ok" and mg.get("upToDate") is True)
            a, e = mg.get("applied"), mg.get("expected")
            ahead = (isinstance(a, int) and isinstance(e, int) and not isinstance(a, bool)
                     and not isinstance(e, bool) and a > e)
            enabled = j.get("enabledTasks") if isinstance(j.get("enabledTasks"), list) else None
            facts = "healthy=%s database=%s migrations applied %s of %s" % (
                safe(j.get("healthy"), 8), safe(j.get("database"), 12), safe(a, 8), safe(e, 8))
            if core and a == e:
                emit("PASS", "points", h, "GET", "/api/health", "%d %s" % (st, facts))
            elif core and ahead:
                # The app allows a database that holds more migrations than the build (applied >= expected).
                # It is the state after a migration is applied and before the pull request that carries it is merged.
                emit("WARN", "points", h, "GET", "/api/health",
                     "%d %s: the database is ahead of the running build, which the app allows; expected only between "
                     "applying a migration and merging its code (points-settings-and-database.md)" % (st, facts))
            else:
                emit("FAIL", "points", h, "GET", "/api/health", "%d %s" % (st, facts))
            origin = j.get("origin")
            if origin != POINTS_ORIGIN:
                emit("FAIL", "points", h, "GET", "/api/health", "origin is %s, wanted %s (sign-in breaks when it differs)" % (safe(origin, 40), POINTS_ORIGIN))
            if j.get("environment") != "self-hosted":
                emit("WARN", "points", h, "GET", "/api/health", "environment is %s, production runs self-hosted" % safe(j.get("environment"), 20))
            if j.get("sha") is None:
                known("P-K1", "points", h, "GET", "/api/health", "sha null")
            else:
                fixed("P-K1", "points", h, "GET", "/api/health", "sha %s" % safe(j.get("sha"), 12))
            if enabled is not None:
                emit("PASS", "points", h, "GET", "/api/health", "enabled tasks: %s" % safe(", ".join(str(x) for x in enabled), 80))
    r = get("points", O, "/api/tasks")
    if r:
        st, hd, body = r
        j = as_json(body)
        tasks = j.get("tasks") if isinstance(j, dict) else None
        if st != 200 or not isinstance(tasks, list):
            emit("FAIL", "points", h, "GET", "/api/tasks", "%d, wanted JSON with a tasks list" % st)
        else:
            ids = sorted(str(t.get("id")) for t in tasks if isinstance(t, dict))
            if enabled is not None and ids != sorted(str(x) for x in enabled):
                emit("WARN", "points", h, "GET", "/api/tasks", "task list %s differs from enabledTasks in /api/health" % safe(", ".join(ids), 60))
            else:
                emit("PASS", "points", h, "GET", "/api/tasks", "200, %d tasks%s" % (len(ids), " (same as enabledTasks)" if enabled is not None else ""))
    check_status("points", O, "/leaderboard")
    check_status("points", O, "/api/leaderboard")
    r = get("points", O, "/")
    if r:
        st, hd, _ = r
        if st in (200, 301, 302, 307, 308):
            emit("PASS", "points", h, "GET", "/", "%d%s" % (st, " to " + safe(hd.get("location", ""), 40) if st != 200 else ""))
        else:
            emit("FAIL", "points", h, "GET", "/", "%d" % st)
    P = ORIGINS["WEB_HEALTH_POINTS_PREVIEW"]
    r = get("points", P, "/api/health")
    if r and r[0] != 200:
        # the first call already printed a FAIL for a network error; a status other than 200 is only a WARN here
        emit("WARN", "points", host_of(P), "GET", "/api/health", "%d: the preview host is the same box but not production" % r[0])
    elif r:
        emit("PASS", "points", host_of(P), "GET", "/api/health", "200 (preview host, same box)")


CHECKS = {
    "website": (website, "moi.technology pages, sitemap, robots, /api/health, calendar JSON, baked API base, 404 behaviour, Link header, PDF header; blog.moi.technology pages, feeds, 404 behaviour, feed against listing"),
    "dataroom": (dataroom, "dataroom.moi.technology redirect, /home, document list with embedding status, hard-coded figures on /home"),
    "points": (points, "points.moi.technology /api/health, /api/tasks, leaderboard, redirect, and the preview host"),
}
NOT_CHECKED = ("a chat answer, any upload or admin page, a deploy run's status, the database itself, the VM, DNS or "
               "certificates. See references/<product>-health.md for those.")


def valid_origin(name, value):
    sp = urllib.parse.urlsplit(value)
    if sp.scheme not in ("http", "https") or not sp.netloc or "@" in sp.netloc or sp.query or sp.fragment \
            or sp.path not in ("", "/"):
        # the value is not echoed: a bad override may hold a user name and password
        sys.stderr.write("web-health.sh: %s must be an origin like https://host (http or https, no user name, no path, no query)\n" % name)
        sys.exit(2)
    return value.rstrip("/")


def main():
    global ARGS, ORIGINS
    class Parser(argparse.ArgumentParser):
        def error(self, message):  # exit 2, and never echo a secret-shaped argument
            self.print_usage(sys.stderr)
            sys.stderr.write("web-health.sh: error: %s\n" % safe(message, 160))
            sys.exit(2)

    ap = Parser(prog="web-health.sh", description="Read-only health check of the MOI website, Dataroom and Points Program.",
                                 epilog="Exit: 0 no FAIL, 1 a FAIL, 2 bad usage.")
    ap.add_argument("target", nargs="?", default="all", choices=["website", "dataroom", "points", "all"])
    ap.add_argument("--timeout", type=int, default=20, help="seconds per request, 1 to 120 (default 20)")
    ap.add_argument("--list", action="store_true", help="print the checks and make no request")
    ARGS = ap.parse_args()
    if not 1 <= ARGS.timeout <= 120:
        sys.stderr.write("web-health.sh: --timeout must be between 1 and 120 seconds\n")
        sys.exit(2)
    ORIGINS = {k: valid_origin(k, os.environ.get(k, v)) for k, v in DEFAULT_ORIGINS.items()}
    names = list(CHECKS) if ARGS.target == "all" else [ARGS.target]
    if ARGS.list:
        for n in names:
            print("%-9s %s" % (n, CHECKS[n][1]))
        print("Known faults it reports as KNOWN: " + ", ".join(sorted(KNOWN)))
        return 0
    if not shutil.which("curl") and sys.version_info < (3, 9):
        sys.stderr.write("web-health.sh: needs curl or Python 3.9 or newer\n")
        return 2
    print("web-health %s, read-only, %s UTC date %s" % (ARGS.target, "GET and HEAD only", TODAY))
    for n in names:
        CHECKS[n][0]()
    print("summary: PASS %d, WARN %d, KNOWN %d, FAIL %d (%d requests)" % (COUNTS["PASS"], COUNTS["WARN"], COUNTS["KNOWN"], COUNTS["FAIL"], STATE["requests"]))
    if STATE["net_fail"] and STATE["net_fail"] >= STATE["requests"]:
        print("every request failed to get an answer: check this machine's network before reading any FAIL as an outage")
    print("not checked: " + NOT_CHECKED)
    return 1 if COUNTS["FAIL"] else 0


try:
    sys.exit(main())
except KeyboardInterrupt:
    sys.stderr.write("web-health.sh: interrupted\n")
    sys.exit(2)
PY
