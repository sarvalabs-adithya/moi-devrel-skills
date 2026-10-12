#!/usr/bin/env python3
"""copy-lint.py: check an announcement copy file (social/<slug>.md) before its pull request merges.

Usage (SKILLS is the folder that holds the moi-* skills; run from the working copy of sarvalabs/MOI-Website):
    python3 "$SKILLS/moi-blog/scripts/copy-lint.py" [--post PATH] [--no-slop-lint] social/<slug>.md

    --post PATH     the post the copy announces. Default: blog/src/content/posts/<slug>.md next to the repo root,
                    if it exists. Used to catch copy that is still the seeded title and summary.
    --no-slop-lint  skip moi-devrel's slop-lint.sh (a missing slop-lint.sh is otherwise an error)

The distribute pipeline measures length and skips empty channels, and checks nothing else. This script adds:
    - a leftover placeholder ([FILL IN, <<<, TODO, RELEASE_URL, REPLACE-WITH)                    ERROR  # slop-lint:ignore
    - a block that is still the seeded scaffold, or still holds the post's summary word for word  ERROR / WARN
    - length: X 280 with every URL counted as 23, LinkedIn 3000, Discord 2000, Telegram 4096     ERROR
    - backticks or bold markers in X, LinkedIn or Telegram copy (they render literally)         ERROR / WARN
    - a bare domain in X copy (the pipeline counts it literally, X may count 23)                  WARN
    - a block for Discord or Telegram (they post immediately; the 2026-08-31 decision was X
      and LinkedIn only)                                                                          WARN
    - a missing {{link}} token (the pipeline appends the link), a hashtag, an emoji, a relative word such as
      today or tomorrow, a slug that is not the file name, no X or LinkedIn block at all
    - the phrasing rules of slop-lint.sh (em dash, retired terms, 12:00 AM UTC and the rest)  # slop-lint:ignore

Output: <file>:<line>:<LEVEL>:<rule>: <message>, then a summary on stderr. Anything key-shaped that a message quotes
from the file (a webhook address, a token) is replaced by <masked>.
It refuses an env file (.env, .env.*, *.env, .envrc): those can hold keys and are never opened.
Exit codes: 0 no error, 1 at least one error, 2 usage error, unreadable file or env file.
Python 3 standard library only. Reads files and runs slop-lint.sh. It never writes and never uses the network.
"""
import argparse
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # importing post-lint.py must not leave a cache folder in the skill
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("post_lint", str(HERE / "post-lint.py"))
pl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pl)

LIMITS = {"x": 280, "linkedin": 3000, "discord": 2000, "telegram": 4096}
MEDIUM = {"x": "social", "linkedin": "social", "discord": "community", "telegram": "community"}
RELATIVE_WORDS = re.compile(r"\b(?:today|tonight|tomorrow|yesterday|last week|this week|this morning)\b", re.I)


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


def rendered_length(text, channel, slug):
    """Length the way the pipeline measures it: {{link}} becomes the tagged URL, and X counts any URL as 23."""
    url = "https://blog.moi.technology/article/%s/?utm_source=%s&utm_medium=%s&utm_campaign=%s" % (slug, channel, MEDIUM[channel], slug)
    body = text.strip()
    body = body.replace("{{link}}", url) if "{{link}}" in body else body + "\n\n" + url
    if channel == "x":
        body = re.sub(r"https?://\S+", "x" * 23, body)
    return len(body)


def main():
    ap = argparse.ArgumentParser(description="Check an announcement copy file.", epilog="Exit 0 no error, 1 error, 2 usage.")
    ap.add_argument("copy")
    ap.add_argument("--post")
    ap.add_argument("--no-slop-lint", action="store_true")
    a = ap.parse_args()
    path = Path(a.copy)
    for named in (path, Path(a.post) if a.post else None):
        if named is not None and pl.is_env_file(named):
            pl.refuse_env("copy-lint", named)
            return 2
    try:
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    except (OSError, UnicodeDecodeError) as e:
        sys.stderr.write("copy-lint: cannot read %s: %s\n" % (path, e))
        return 2
    rep = pl.Report(False)
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        rep.add(1, "ERROR", "frontmatter-missing", "the file must start with a line of three dashes")
        return finish(rep, path, 0, a)
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        rep.add(1, "ERROR", "frontmatter-missing", "the frontmatter is never closed with a line of three dashes")
        return finish(rep, path, 0, a)
    try:
        data = pl.Parser([(k + 2, lines[1 + k]) for k in range(0, end - 1)]).parse()
    except pl.YamlError as e:
        rep.add(e.line, "ERROR", "frontmatter-yaml", e.msg + " (a continuation line indented less than the block ends it)")
        return finish(rep, path, 0, a)

    for k in range(0, end - 1):
        raw = lines[1 + k]
        if not raw.lstrip().startswith("#") and not raw.startswith(" ") and (pl.PLACEHOLDER_CS.search(raw) or pl.PLACEHOLDER_CI.search(raw)):
            rep.add(k + 2, "ERROR", "placeholder", "placeholder text in the frontmatter must not ship")
    slug = data.get("slug") if isinstance(data.get("slug"), str) else ""
    if slug != path.stem:
        rep.add(data.lines.get("slug", 1), "ERROR", "slug-mismatch", "slug %r is not the file name %r" % (slug, path.stem))
    for key in ("slug", "title", "published"):
        v = data.get(key)
        if not isinstance(v, str) or not v.strip():
            rep.add(1, "ERROR", "missing-field", "`%s` is required" % key)

    post_path = Path(a.post) if a.post else None
    if post_path is None:
        for parent in [path.resolve().parent] + list(path.resolve().parents):
            cand = parent / "blog" / "src" / "content" / "posts" / (path.stem + ".md")
            if cand.is_file():
                post_path = cand
                break
    title = summary = ""
    if post_path is not None and post_path.is_file():
        try:
            # read only the frontmatter of the post
            plines = post_path.read_text(encoding="utf-8").split("\n")
            pend = next(i for i in range(1, len(plines)) if plines[i].strip() == "---")
            pdata = pl.Parser([(k + 2, plines[1 + k]) for k in range(0, pend - 1)]).parse()
            title, summary = str(pdata.get("title") or ""), str(pdata.get("summary") or "")
        except (StopIteration, pl.YamlError, OSError):
            rep.add(1, "WARN", "post-unreadable", "could not read the post's frontmatter, so seeded text was not checked")
    else:
        rep.add(1, "WARN", "post-not-found", "the post was not found (give --post), so seeded text was not checked")

    seeded = {}
    if title and summary:
        seeded = {"discord": "**%s**\n\n%s\n\n{{link}}" % (title, summary), "telegram": "%s\n\n%s\n\n{{link}}" % (title, summary),
                  "x": "%s\n\n{{link}}" % summary, "linkedin": "%s\n\n%s\n\n{{link}}" % (title, summary)}

    sent_any = False
    for ch in ("x", "linkedin", "discord", "telegram"):
        v = data.get(ch)
        ln = data.lines.get(ch, 1)
        if v is None or (isinstance(v, str) and not v.strip()):
            continue
        if not isinstance(v, str):
            rep.add(ln, "ERROR", "block-type", "%s must be a literal block (key: |)" % ch)
            continue
        if ch in ("x", "linkedin"):
            sent_any = True
        else:
            rep.add(ln, "WARN", "immediate-channel", "%s posts immediately when its secrets are set. The 2026-08-31 decision was X and LinkedIn only: empty this block unless the operator said otherwise" % ch)
        if pl.PLACEHOLDER_CS.search(v) or pl.PLACEHOLDER_CI.search(v):
            rep.add(ln, "ERROR", "placeholder", "%s block still holds placeholder text" % ch)
        if seeded and norm(v) == norm(seeded[ch]):
            rep.add(ln, "ERROR", "unrewritten-scaffold", "%s block is still the seeded title and summary. Rewrite it by hand" % ch)
        elif summary and norm(summary) in norm(v):
            rep.add(ln, "WARN", "summary-copied", "%s block repeats the post summary word for word, which reads generated" % ch)
        if "{{link}}" not in v:
            rep.add(ln, "WARN", "no-link-token", "%s block has no {{link}}; the pipeline appends the tagged link to the end" % ch)
        n = rendered_length(v, ch, slug or "slug")
        if n > LIMITS[ch]:
            rep.add(ln, "ERROR", "too-long", "%s copy is %d characters with its link; the limit is %d. The send is blocked, never cut" % (ch, n, LIMITS[ch]))
        if ch in ("x", "linkedin") and re.search(r"`|\*\*|__", v):
            rep.add(ln, "ERROR", "markup", "%s renders backticks and bold markers literally. Plain text only" % ch)
        elif ch == "telegram" and re.search(r"`|\*\*|__", v):
            rep.add(ln, "WARN", "markup", "telegram is sent HTML-escaped, so markers show literally")
        if pl.EMOJI.search(v):
            rep.add(ln, "WARN", "emoji", "%s copy holds an emoji or pictograph: the house voice has none" % ch)
        if ch == "x" and re.search(r"(?<![/\w.@])(?:www\.)?[a-z0-9-]+\.(?:technology|com|io|org|net|dev|ai)\b(?!/)", re.sub(r"https?://\S+", "", v)):
            rep.add(ln, "WARN", "bare-domain", "a bare domain in X copy is counted at its literal length by the pipeline, and X may charge 23. Write https://")
        if re.search(r"(?<!\w)#[A-Za-z]\w+", v):
            rep.add(ln, "WARN", "hashtag", "hashtags are not recorded as used. ASK: Rahul before keeping one")
        m = RELATIVE_WORDS.search(v)
        if m:
            rep.add(ln, "WARN", "relative-word", "%r goes stale once the post is scheduled or read later. Write a date" % m.group(0))
    if not sent_any:
        rep.add(1, "WARN", "nothing-to-send", "no X or LinkedIn block has text, so Distribute would send nothing")
    return finish(rep, path, len(lines), a)


def finish(rep, path, n, a):
    if not a.no_slop_lint:
        sl = pl.find_slop_lint()
        if sl is None:
            rep.add(1, "ERROR", "slop-lint-missing", "moi-devrel/scripts/slop-lint.sh was not found, so the phrasing rules were not checked. Set SKILLS or pass --no-slop-lint")
        else:
            try:
                r = subprocess.run(["bash", str(sl), str(path)], capture_output=True, text=True, timeout=120)
                prefix = str(path) + ":"
                for out in r.stdout.splitlines():
                    if out.startswith(prefix):
                        m = re.match(r"(\d+):([a-z0-9-]+)(\(warn\))?:(.*)$", out[len(prefix):])
                        if m and m.group(2) != "placeholder":
                            rep.add(int(m.group(1)), "WARN" if m.group(3) else "ERROR", "slop-lint/" + m.group(2), m.group(4).strip())
            except (OSError, subprocess.SubprocessError) as e:
                rep.add(1, "ERROR", "slop-lint-failed", "could not run slop-lint.sh: %s" % e)
    sys.stdout.flush()
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    for line, level, rule, msg in sorted(rep.items, key=lambda x: (x[0], order[x[1]], x[2])):
        print("%s:%d:%s:%s: %s" % (path, line, level, rule, msg))
    sys.stderr.write("copy-lint: %d error(s), %d warning(s)\n" % (rep.count("ERROR"), rep.count("WARN")))
    return 1 if rep.count("ERROR") else 0


if __name__ == "__main__":
    sys.exit(main())
