#!/usr/bin/env python3
"""Draft a YouTube description for a Community Call recording from the deck.

Usage (SKILLS is the folder that holds the moi-* skills; run from the working copy):
    python3 "$SKILLS/moi-webinar/community-call/scripts/youtube-description.py" \
        community-call-<N>/deck/index.html [--template PATH] > community-call-<N>/description.txt

Reads (never writes a file):
    deck.html   the <title> in the <head> (for the call name and number; the
                placeholder [CALL TITLE] when there is none) and the TITLES array
                in the inline script (one chapter per slide)
    template    templates/youtube-description.md next to this script, unless
                --template is given. Only the text between the BEGIN and END
                markers is used.

Prints the draft to stdout. Warnings go to stderr, so `> draft.txt` keeps the
draft clean. The draft always has:
    - a first chapter at 00:00 (YouTube needs one)
    - blank timestamps [__:__] for every other chapter, to be filled from the
      recording, because chapters must match what was actually said
    - the structure of the one description on record (Community Call 13), with
      [PLACEHOLDERS] for everything a person has to supply

Warns when the draft is over 5,000 characters, the length limit used for the
record, and says how many [PLACEHOLDERS] are still open. Neither warning
changes the exit code.

An env file (.env, .env.*, *.env, .envrc) is refused as the deck or the template and never opened.

Exit codes: 0 draft printed; 2 deck, TITLES or template could not be read, or an env file was named.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

LIMIT = 5000
BEGIN, END = "<!-- BEGIN DESCRIPTION -->", "<!-- END DESCRIPTION -->"


def read_titles(html):
    m = re.search(r"var\s+TITLES\s*=\s*\[(.*?)\]\s*;", html, re.S)
    if not m:
        return None
    out = []
    for lit in re.finditer(r'"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\'', m.group(1)):
        body = lit.group(1) if lit.group(1) is not None else lit.group(2)
        try:
            out.append(json.loads('"' + body.replace('\\\'', "'") + '"'))
        except ValueError:
            out.append(body)
    return out or None


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
    ap = argparse.ArgumentParser(description="Draft a YouTube description from a deck.",
                                 epilog="Exit 0 draft printed, 2 bad input.")
    ap.add_argument("deck")
    ap.add_argument("--template", help="override templates/youtube-description.md")
    args = ap.parse_args()

    for named in (args.deck, args.template):
        if named and is_env_file(named):
            print("youtube-description: refusing to read %s: an env file can hold keys and is never opened. "
                  "Pass the deck instead." % os.path.basename(named), file=sys.stderr)
            return 2
    try:
        html = Path(args.deck).read_text(encoding="utf-8")
    except OSError as e:
        print(f"youtube-description: cannot read deck: {e}", file=sys.stderr)
        return 2
    titles = read_titles(html)
    if not titles:
        print("youtube-description: no TITLES array found in the deck's script", file=sys.stderr)
        return 2

    tpath = Path(args.template) if args.template else \
        Path(__file__).resolve().parent.parent / "templates" / "youtube-description.md"
    try:
        template = tpath.read_text(encoding="utf-8")
    except OSError as e:
        print(f"youtube-description: cannot read template: {e}", file=sys.stderr)
        return 2
    if BEGIN not in template or END not in template:
        print(f"youtube-description: template lacks the {BEGIN} / {END} markers", file=sys.stderr)
        return 2
    body = template.split(BEGIN, 1)[1].split(END, 1)[0].strip("\n")

    # Read the title from the <head> only. A <title> string inside the inline script
    # (the presenter window builds one) is not the call title.
    hm = re.search(r"<head\b[^>]*>(.*?)</head>", html, re.S | re.I)
    tm = re.search(r"<title[^>]*>(.*?)</title>", hm.group(1), re.S | re.I) if hm else None
    title = " ".join(tm.group(1).split()) if tm and tm.group(1).strip() else ""
    if not title:
        title = "[CALL TITLE]"
        print("note: the deck has no <title> in its <head>, so the title is the placeholder "
              "[CALL TITLE] and the next number is [N+1].", file=sys.stderr)
    nm = re.search(r"#\s*(\d+)", title)
    next_n = str(int(nm.group(1)) + 1) if nm else "[N+1]"

    chapters = []
    for k, t in enumerate(titles):
        if k == 0:
            chapters.append("00:00 Welcome")
        else:
            chapters.append(f"[__:__] {t}")

    draft = (body.replace("{{TITLE}}", title)
                 .replace("{{NEXT_NUMBER}}", next_n)
                 .replace("{{CHAPTERS}}", "\n".join(chapters)))
    print(draft)

    n = len(draft)
    ph = len(re.findall(r"\[[^\]\n]+\]", draft))
    if n > LIMIT:
        print(f"WARNING: the draft is {n} characters, over the {LIMIT} limit. "
              "Cut link blocks or upgrade lines before posting.", file=sys.stderr)
    else:
        print(f"note: {n} of {LIMIT} characters, counted with placeholders in place. "
              "Count again after filling them.", file=sys.stderr)
    print(f"note: {ph} bracketed placeholder(s) still open, including the {len(titles) - 1} "
          "blank chapter timestamps. Chapters must match the order actually presented.",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
