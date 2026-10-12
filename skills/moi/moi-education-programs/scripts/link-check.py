#!/usr/bin/env python3
"""Report dead and redirected links in markdown files, by line. Read-only.

Usage (SKILLS is the folder that holds the moi-* skills, quoted because a path can hold spaces):
    python3 "$SKILLS/moi-education-programs/scripts/link-check.py" <file.md> [more.md ...] [options]

Options:
    --timeout SECONDS   per request, default 10 (1 to 60)
    --delay SECONDS     pause between two requests to the network, default 0.3 (0 to 10)
    --max-links N       unique web links checked in one run, default 300. More than that: exit 2
    --include-code      also check URLs inside fenced code blocks and `code spans` (off by default,
                        because a code sample may hold a JSON-RPC endpoint that refuses a GET)
    --root DIR          folder that a leading-slash link such as /docs/x.md is resolved against
                        (GitHub resolves it against the repo root). Without it such links are skipped
    --offline           check relative file links only; no network at all
    --verbose           also list the links that are fine

What it checks, per link:
    web link (http or https)  an HTTP HEAD, then a GET when HEAD gets a 4xx or 5xx. The GET reads the
                              status line and headers only and closes; no body is downloaded.
                              Up to 5 redirects are followed by hand, each one checked as below.
    relative file link        the file or folder must exist, with the same letter case (GitHub paths
                              are case-sensitive, a Mac is not). Only existence is tested, nothing is read.
Verdicts:
    DEAD       404 or 410, any other 4xx, a 5xx (may be transient: run again), a host that does not
               resolve, a refused connection, a timeout, a redirect loop, a missing local file
    REDIRECT   the final answer is 2xx after one or more redirects. The new address is printed
    CHECK      the script cannot tell: 401, 403, 405, 429, 999, a certificate this machine does not
               accept, a 3xx with no Location. Open it in a browser. If every https link comes back
               CHECK with a certificate message, this Python has no CA bundle: set SSL_CERT_FILE to
               your system bundle (/etc/ssl/cert.pem on macOS) and run again
    SKIPPED    mailto, tel, anchors, other schemes, a link with a password in it, a link that looks like
               it carries a credential, a non-standard port, and any non-public host (see below)
Safety:
    It never requests a non-public host. A host is non-public when its name is a single label or ends in
    .local, .localhost, .internal, .lan, .home, .corp, .intranet, .test, .example or .invalid, or when
    its address is not a global address (loopback, private, link-local, shared, multicast, reserved,
    including an IPv4 address written inside an IPv6 one). The name is resolved once, every address is
    tested, and the connection goes to the tested address, so a name that changes its answer cannot
    redirect the request. A redirect to a non-public host is not followed. Only ports 80 and 443 are used.
    It never sends a cookie, a credential or a POST, and it never writes a file.
    A link with user:password in it, with a token-shaped value, or with a query key such as token, key,
    secret, signature or password is not requested at all.
    Output shows the host and the path, never the query string. Secret shapes (long hex, known token
    prefixes, JWTs, runs of 12 or more short words joined by spaces, commas, slashes, hyphens, underscores,
    plus signs or %20, which is the shape of a recovery phrase) are masked before anything is truncated.
    A link that is skipped for any of these reasons is counted, and the run ends with a note to open
    those links by hand.
    An env-named input file (.env, .env.*, *.env) is refused and never opened.
Limits you should know (a status code proves the page answers, not that its content is right):
    a JSON-RPC endpoint answers a GET with 404, so it reads as DEAD when --include-code is on
    (test an endpoint with the JSON-RPC read net.Version instead); a Discord invite redirects to
    discord.com whether or not the invite code is valid; a Google Form link is skipped because its id
    looks like a token, so open it by hand; a web app that answers 200 for a path that does not exist
    (the MOI website, the js-moi-sdk docs host) never reads as DEAD, and Voyage answers 200 whatever the
    query string says, so a stale ?network= value is not caught.
Exit codes: 0 no dead link; 1 at least one dead link; 2 bad usage or unreadable input.
CHECK links never change the exit code. Read them.
Python 3 standard library only.
"""
import argparse
import html
import http.client
import ipaddress
import os
import re
import signal
import socket
import ssl
import sys
import time
from urllib.parse import unquote, urljoin, urlsplit

sys.dont_write_bytecode = True

MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_URL_LEN = 2000
MAX_REDIRECTS = 5
USER_AGENT = "moi-link-check/1.0 (read-only link audit; no body download)"
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
CREDENTIAL_KEYS = frozenset((
    "token", "access_token", "id_token", "refresh_token", "auth", "authorization", "key", "api_key",
    "apikey", "secret", "client_secret", "password", "passwd", "pwd", "signature", "sig", "code",
    "x-amz-signature", "x-amz-credential", "x-amz-security-token", "session", "sessionid", "jwt"))
PRIVATE_SUFFIXES = (".local", ".localhost", ".internal", ".lan", ".home", ".corp", ".intranet",
                    ".test", ".example", ".invalid", ".home.arpa")

# Link syntax. Group 1 is the target.
INLINE_LINK = re.compile(r"!?\[[^\]]*\]\(\s*(<[^>]*>|(?:[^()\s]|\([^()\s]*\))+)(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)")
REF_DEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(<[^>]*>|\S+)")
AUTOLINK = re.compile(r"<((?:https?:)?//[^<>\s]+)>")
HTML_ATTR = re.compile(r"""\b(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)
BARE_URL = re.compile(r"https?://[^\s<>\"'`\[\]]+", re.I)


def _mask_phrases(s):
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
        elif re.fullmatch(r"[\s,;/_+\-]+|(?:%20)+", text):
            continue   # a phrase can be joined by spaces, commas, slashes, hyphens, underscores, plus or %20
        else:
            close()
    close()
    for a, b in reversed(spans):
        s = s[:a] + "(masked: 12 or more short words, possible recovery phrase)" + s[b:]
    return s


def mask(s):
    s = LONG_HEX.sub(lambda m: m.group(0)[:6] + "...(masked)", s)
    for rx in SECRET_SHAPES:
        s = rx.sub(lambda m: m.group(0)[:4] + "...(masked)", s)
    return _mask_phrases(s)


def is_env_name(name):
    low = os.path.basename(name).lower()
    return low in (".env", ".envrc") or low.startswith(".env.") or low.endswith(".env") or ".env." in low


def is_env_file(path):
    names = [path]
    try:
        names.append(os.path.realpath(path))
    except OSError:
        pass
    return any(is_env_name(n) for n in names)


CA_FALLBACKS = ("/etc/ssl/cert.pem", "/private/etc/ssl/cert.pem", "/etc/ssl/certs/ca-certificates.crt",
                "/etc/pki/tls/certs/ca-bundle.crt")


def make_ssl_context():
    """Default TLS checks. Some Python builds ship no CA bundle: then use the system one if there is one."""
    ctx = ssl.create_default_context()
    try:
        have = ctx.cert_store_stats().get("x509_ca", 0)
    except (AttributeError, ssl.SSLError):
        have = 1
    if have == 0:
        for cafile in CA_FALLBACKS:
            if os.path.isfile(cafile):
                try:
                    ctx.load_verify_locations(cafile=cafile)
                    break
                except (ssl.SSLError, OSError):
                    continue
    return ctx


def fail_input(msg):
    print("link-check: " + msg, file=sys.stderr)
    return 2


# ---------------------------------------------------------------- extracting links from markdown

def extract_links(text, include_code):
    """Yield (line_number, target) for every link in the text."""
    found = []
    in_fence = None
    for n, line in enumerate(text.splitlines(), 1):
        stripped = line.lstrip()
        fence = re.match(r"(`{3,}|~{3,})", stripped)
        if fence:
            marker = fence.group(1)[0]
            if in_fence is None:
                in_fence = marker
                continue
            if in_fence == marker:
                in_fence = None
                continue
        if in_fence and not include_code:
            continue
        work = line
        if not include_code:
            work = re.sub(r"`[^`\n]*`", lambda m: " " * len(m.group(0)), work)
        seen = set()

        def take(rx, grp=1):
            nonlocal work
            for m in list(rx.finditer(work)):
                tgt = m.group(grp).strip()
                if tgt.startswith("<") and tgt.endswith(">"):
                    tgt = tgt[1:-1].strip()
                if tgt and tgt not in seen:
                    seen.add(tgt)
                    found.append((n, tgt))
            work = rx.sub(lambda m: " " * len(m.group(0)), work)

        take(INLINE_LINK)
        take(REF_DEF)
        take(AUTOLINK)
        take(HTML_ATTR)
        for m in BARE_URL.finditer(work):
            tgt = m.group(0)
            while tgt and tgt[-1] in ".,;:!?*_":
                tgt = tgt[:-1]
            while tgt.endswith(")") and tgt.count(")") > tgt.count("("):
                tgt = tgt[:-1]
            if tgt and tgt not in seen:
                seen.add(tgt)
                found.append((n, tgt))
    return found


# ---------------------------------------------------------------------------- public host test

def addr_is_public(ip_text):
    try:
        ip = ipaddress.ip_address(ip_text.split("%")[0])
    except ValueError:
        return False
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped is not None:
        ip = ip.ipv4_mapped
    return ip.is_global and not ip.is_multicast


def host_name_is_public(host):
    h = host.lower().rstrip(".")
    if not h:
        return False
    try:
        ipaddress.ip_address(h.strip("[]"))
        return addr_is_public(h.strip("[]"))
    except ValueError:
        pass
    if "." not in h or h == "localhost":
        return False
    return not any(h.endswith(s) for s in PRIVATE_SUFFIXES)


def looks_like_credential(url, parts):
    if parts.username is not None or parts.password is not None:
        return "has a user or password in it"
    if mask(url) != url:
        return "has a secret-shaped value in it"
    if parts.query:
        for pair in parts.query.replace(";", "&").split("&"):
            key = unquote(pair.split("=", 1)[0]).lower()
            if key in CREDENTIAL_KEYS and "=" in pair and pair.split("=", 1)[1]:
                return "has a credential-style query key"
    return None


class Skip(Exception):
    pass


CALLED = set()   # hosts a request was really sent to


def resolve_public(host, port):
    """Resolve once. Return a list of (family, ip). Raise Skip for non-public, OSError for no answer."""
    if not host_name_is_public(host):
        raise Skip("non-public host, not requested")
    try:
        infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except UnicodeError:
        raise OSError("malformed host name")
    addrs = []
    for fam, _t, _p, _c, sa in infos:
        if fam in (socket.AF_INET, socket.AF_INET6):
            addrs.append((fam, sa[0]))
    if not addrs:
        raise OSError("no address")
    for _fam, ip in addrs:
        if not addr_is_public(ip):
            raise Skip("the name resolves to a non-public address, not requested")
    addrs.sort(key=lambda a: 0 if a[0] == socket.AF_INET else 1)
    return addrs


def one_request(method, parts, timeout, ctx):
    """One HTTP request to the tested address. Returns (status, location_or_None)."""
    host = parts.hostname
    https = parts.scheme == "https"
    port = parts.port or (443 if https else 80)
    if not host_name_is_public(host):
        raise Skip("non-public host, not requested")
    if port not in (80, 443):
        raise Skip("non-standard port, not requested")
    addrs = resolve_public(host, port)
    CALLED.add(host.lower())
    sock = None
    last = None
    for fam, ip in addrs:
        try:
            sock = socket.create_connection((ip, port), timeout=timeout)
            break
        except OSError as e:
            last = e
    if sock is None:
        raise last or OSError("connection failed")
    try:
        if https:
            sock = ctx.wrap_socket(sock, server_hostname=host)
            conn = http.client.HTTPSConnection(host, port, timeout=timeout, context=ctx)
        else:
            conn = http.client.HTTPConnection(host, port, timeout=timeout)
        conn.sock = sock
        path = parts.path or "/"
        if parts.query:
            path += "?" + parts.query
        conn.request(method, path, headers={"User-Agent": USER_AGENT, "Accept": "*/*",
                                            "Connection": "close"})
        resp = conn.getresponse()
        status = resp.status
        loc = resp.getheader("Location")
        conn.close()   # the body is never read
        return status, loc
    finally:
        try:
            sock.close()
        except OSError:
            pass


def check_web(url, timeout, ctx):
    """Return (verdict, code, detail). verdict in OK, REDIRECT, DEAD, CHECK, SKIPPED."""
    current = url
    hops = 0
    first_code = None
    while True:
        try:
            parts = urlsplit(current)
            parts.port
        except ValueError:
            return "DEAD", 0, "malformed link"
        if parts.scheme not in ("http", "https") or not parts.hostname:
            return "DEAD", 0, "malformed link"
        why = looks_like_credential(current, parts)
        if why:
            return "SKIPPED", 0, ("redirect target " if hops else "link ") + "%s, not requested" % why
        status = None
        for method in ("HEAD", "GET"):
            attempt = 0
            while True:
                try:
                    status, loc = one_request(method, parts, timeout, ctx)
                    break
                except Skip as e:
                    return "SKIPPED", 0, ("redirect target: " if hops else "") + str(e)
                except ssl.SSLCertVerificationError as e:
                    return "CHECK", 0, "certificate not accepted by this machine (%s); open it in a browser" % \
                        mask(str(getattr(e, "verify_message", "") or "verify failed"))[:60]
                except ssl.SSLError as e:
                    return "DEAD", 0, "TLS error: " + mask(str(e.reason or e.__class__.__name__))[:60]
                except socket.gaierror:
                    return "DEAD", 0, "the host name does not resolve"
                except (socket.timeout, TimeoutError):
                    attempt += 1
                    if attempt < 2:
                        time.sleep(1.0)
                        continue
                    return "DEAD", 0, "timed out after %ss (twice)" % timeout
                except (ConnectionError, OSError, http.client.HTTPException) as e:
                    attempt += 1
                    if attempt < 2:
                        time.sleep(1.0)
                        continue
                    return "DEAD", 0, "connection failed (%s)" % e.__class__.__name__
            if method == "HEAD" and status >= 400:
                continue   # some servers refuse HEAD: ask again with GET (headers only)
            break
        if first_code is None:
            first_code = status
        if status in (301, 302, 303, 307, 308):
            if not loc:
                return "CHECK", status, "redirect with no Location header"
            hops += 1
            if hops > MAX_REDIRECTS:
                return "DEAD", status, "more than %d redirects (loop?)" % MAX_REDIRECTS
            nxt = urljoin(current, loc)
            if urlsplit(nxt).scheme not in ("http", "https"):
                return "SKIPPED", status, "redirects to a non-web address, not followed"
            current = nxt
            continue
        if 200 <= status < 300:
            if hops:
                return "REDIRECT", first_code, current
            return "OK", status, ""
        if status in (401, 403, 405, 429, 999):
            return "CHECK", status, "the server refused an automated request; open it in a browser"
        if status in (404, 410):
            return "DEAD", status, "not found" + (" (after %d redirect%s)" % (hops, "" if hops == 1 else "s") if hops else "")
        if status >= 500:
            return "DEAD", status, "server error (may be transient: run again)"
        return "DEAD", status, "HTTP %d" % status


# ------------------------------------------------------------------------- relative file links

def exact_case_exists(base, full):
    """full is a normalised path below or beside base (an existing folder). Return (ok, wrong_case).
    Every component below the common ancestor must exist with exactly this spelling."""
    try:
        common = os.path.commonpath([base, full])
    except ValueError:
        return os.path.exists(full), False
    rel = os.path.relpath(full, common)
    if rel == ".":
        return os.path.exists(full), False
    cur = common
    wrong_case = False
    for comp in rel.split(os.sep):
        try:
            names = os.listdir(cur)
        except OSError:
            return os.path.exists(full), False   # cannot list this folder: fall back to a plain test
        if comp in names:
            cur = os.path.join(cur, comp)
            continue
        close = [n for n in names if n.lower() == comp.lower()]
        if close:
            wrong_case = True
            cur = os.path.join(cur, close[0])
            continue
        return False, False
    return (not wrong_case), wrong_case


def check_file(md_path, target, root):
    raw = target.split("#", 1)[0].split("?", 1)[0]
    if not raw:
        return "SKIPPED", 0, "anchor only"
    raw = unquote(raw)
    if raw.startswith("/"):
        if not root:
            return "SKIPPED", 0, "root-relative link; pass --root to check it"
        base = root
        full = os.path.join(root, raw.lstrip("/"))
    else:
        base = os.path.dirname(os.path.abspath(md_path))
        full = os.path.join(base, raw)
    full = os.path.normpath(full)
    if any(is_env_name(p) for p in full.split(os.sep) if p):
        return "SKIPPED", 0, "env-named target, not checked"
    ok, wrong_case = exact_case_exists(base, full)
    if ok:
        return "OK", 0, ""
    if wrong_case:
        return "DEAD", 0, "the file exists with different letter case (GitHub paths are case-sensitive)"
    return "DEAD", 0, "file not found"


# ------------------------------------------------------------------------------------ reporting

def show(url):
    """Host and path of a URL, never the query string, masked before it is cut."""
    try:
        p = urlsplit(url)
        p.port
    except ValueError:
        return "(malformed link)"
    if looks_like_credential(url, p):
        return "%s/(path hidden)" % mask(p.hostname or "?")
    path = mask(p.path or "/")
    if len(path) > 70:
        path = path[:67] + "..."
    return "%s%s" % (mask(p.hostname or "?"), path)


def classify_target(tgt):
    t = html.unescape(tgt).strip()
    if len(t) > MAX_URL_LEN:
        return "skip", "link longer than %d characters" % MAX_URL_LEN
    if t.startswith("#"):
        return "skip", "anchor"
    if t.startswith("//"):
        return "web", "https:" + t
    m = re.match(r"([A-Za-z][A-Za-z0-9+.-]*):", t)
    if m:
        scheme = m.group(1).lower()
        if scheme in ("http", "https"):
            return "web", t
        return "skip", "not a web link (%s:)" % scheme
    return "file", t


def main():
    ap = argparse.ArgumentParser(
        description="Dead and redirected links in markdown files, by line. Read-only.",
        epilog="Exit 0 no dead link, 1 at least one dead link, 2 bad usage or unreadable input.")
    ap.add_argument("files", nargs="+", help="markdown files")
    ap.add_argument("--timeout", type=float, default=10.0)
    ap.add_argument("--delay", type=float, default=0.3)
    ap.add_argument("--max-links", type=int, default=300)
    ap.add_argument("--include-code", action="store_true")
    ap.add_argument("--root", default=None)
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    try:
        args = ap.parse_args()
    except SystemExit as e:
        return 2 if e.code not in (0, None) else 0
    if not (1 <= args.timeout <= 60):
        return fail_input("--timeout must be between 1 and 60 seconds")
    if not (0 <= args.delay <= 10):
        return fail_input("--delay must be between 0 and 10 seconds")
    if not (1 <= args.max_links <= 2000):
        return fail_input("--max-links must be between 1 and 2000")
    root = None
    if args.root is not None:
        if is_env_name(args.root):
            return fail_input("refusing an env-named --root")
        if not os.path.isdir(args.root):
            return fail_input("--root is not a folder: " + mask(args.root))
        root = os.path.abspath(args.root)

    texts = []
    for path in args.files:
        if is_env_file(path):
            return fail_input("refusing to open an env-named file: " + mask(os.path.basename(path)))
        if not os.path.exists(path):
            return fail_input("no such file: " + mask(path))
        if os.path.isdir(path):
            return fail_input("this is a folder, give a markdown file: " + mask(path))
        try:
            if os.path.getsize(path) > MAX_FILE_BYTES:
                return fail_input("file is larger than 2 MB: " + mask(path))
            with open(path, "rb") as fh:
                data = fh.read()
        except OSError as e:
            return fail_input("cannot read %s: %s" % (mask(path), e.strerror or e.__class__.__name__))
        if b"\x00" in data[:4096]:
            return fail_input("not a text file: " + mask(path))
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            return fail_input("not UTF-8 text: " + mask(path))
        texts.append((path, text))

    ctx = make_ssl_context()
    cache = {}
    counts = {"OK": 0, "REDIRECT": 0, "DEAD": 0, "CHECK": 0, "SKIPPED": 0}
    total = 0
    not_requested = 0
    last_net = 0.0
    for path, text in texts:
        links = extract_links(text, args.include_code)
        name = mask(path)
        for n, tgt in links:
            total += 1
            kind, val = classify_target(tgt)
            if kind == "skip":
                verdict, code, detail = "SKIPPED", 0, val
                shown = mask(html.unescape(tgt))[:60]
            elif kind == "file":
                verdict, code, detail = check_file(path, val, root)
                shown = mask(html.unescape(val).split("#", 1)[0].split("?", 1)[0])[:70]
            else:
                shown = show(val)
                key = val.split("#", 1)[0]
                if args.offline:
                    verdict, code, detail = "SKIPPED", 0, "offline run, web link not requested"
                elif key in cache:
                    verdict, code, detail = cache[key]
                else:
                    if len([k for k in cache]) >= args.max_links:
                        return fail_input("more than %d unique web links; raise --max-links or split the file"
                                          % args.max_links)
                    wait = args.delay - (time.time() - last_net)
                    if last_net and wait > 0:
                        time.sleep(wait)
                    verdict, code, detail = check_web(key, args.timeout, ctx)
                    last_net = time.time()
                    cache[key] = (verdict, code, detail)
            counts[verdict] += 1
            if verdict == "SKIPPED" and "not requested" in detail and not args.offline:
                not_requested += 1
            if verdict == "OK" and not args.verbose:
                continue
            if verdict == "SKIPPED" and not args.verbose:
                continue
            tail = detail
            if verdict == "REDIRECT":
                tail = "now %s" % show(detail)
            code_txt = str(code) if code else "-"
            line = "%s:%d: %-8s %3s %s" % (name, n, verdict, code_txt, shown)
            if tail and tail != shown:
                line += "  (%s)" % tail
            print(line)
    print("Checked %d link(s) in %d file(s): ok %d, redirected %d, dead %d, check by hand %d, skipped %d."
          % (total, len(texts), counts["OK"], counts["REDIRECT"], counts["DEAD"], counts["CHECK"],
             counts["SKIPPED"]))
    if CALLED:
        print("Hosts called: " + ", ".join(sorted(mask(h) for h in CALLED)))
    else:
        print("Hosts called: none")
    if counts["CHECK"]:
        print("CHECK links need a person: the script could not tell if they are alive.")
    if not_requested:
        print("%d link(s) were not requested (a Google Form, a long id, a credential-style value, a "
              "non-public host or a non-standard port). Open the ones that matter by hand." % not_requested)
    return 1 if counts["DEAD"] else 0


if __name__ == "__main__":
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)   # a closed pipe such as | head ends quietly
    except (AttributeError, ValueError):
        pass
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("link-check: interrupted", file=sys.stderr)
        sys.exit(2)
    except Exception as exc:   # never a traceback
        print("link-check: unexpected %s; the run is incomplete" % exc.__class__.__name__, file=sys.stderr)
        sys.exit(2)
