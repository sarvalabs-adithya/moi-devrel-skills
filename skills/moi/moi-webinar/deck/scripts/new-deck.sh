#!/usr/bin/env bash
# new-deck.sh: scaffold a new MOI deck.
#
# Usage:  new-deck.sh <session-folder> "<Deck title>"
# Makes:  <session-folder>/deck/index.html   the framework with one title slide
#         <session-folder>/deck/assets/      for photos and logos
#         <session-folder>/deck/README.md    the deck's notes file, kept current as you edit
#         <session-folder>/SCRIPT.md         the script skeleton (kept if one already exists)
# Sets:   the document title and the cover title. The presenter window title is read from the
#         document title at run time, so nothing else needs renaming.
#         The three scaffold strings you must still replace (cover chip, cover sub-line, slide 1
#         notes) are prefixed TODO, and check-deck.py warns until they are gone.
# Refuses to overwrite: if <session-folder>/deck/index.html already exists, nothing is written.
# Refuses a title that is empty or only white space, or has an em dash or a line break. It does so
# before it creates any folder.
# Exit:   0 created; 1 refused (deck exists, or the title is empty, or has an em dash or line break);
#         2 bad usage.
set -eu
if [ $# -ne 2 ] || [ -z "$1" ]; then
  echo 'usage: new-deck.sh <session-folder> "<Deck title>"   e.g. new-deck.sh community-call-15 "Community Call 15"' >&2
  exit 2
fi
folder=$1; title=$2
if [ -z "$(printf '%s' "$title" | tr -d '[:space:]')" ]; then
  echo "REFUSED: the title is empty. Nothing was created." >&2; exit 1
fi
dash=$(printf '\342\200\224')
case "$title" in
  *"$dash"*|*$'\n'*) echo "REFUSED: the title has an em dash or a line break. Use a colon or a comma." >&2; exit 1 ;;
esac
# the deck branch folder (one level above scripts/): the template sits in its templates/
skill_dir=$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)
deck="$folder/deck"
if [ -e "$deck/index.html" ]; then
  echo "REFUSED: $deck/index.html already exists. Nothing was changed." >&2
  echo "         Edit that deck, or pick another folder." >&2
  exit 1
fi
python3 - "$skill_dir" "$folder" "$title" <<'PY'
import html, os, sys
skill, folder, title = sys.argv[1:4]
if not title.strip():
    print("REFUSED: the title is empty. Nothing was created.", file=sys.stderr)
    sys.exit(1)
if chr(0x2014) in title or "\n" in title:
    print("REFUSED: the title has an em dash or a line break. Use a colon or a comma.", file=sys.stderr)
    sys.exit(1)
title = " ".join(title.split())

def rep(s, old, new):
    assert s.count(old) == 1, "template changed: %r not found once" % old
    return s.replace(old, new)

t = open(os.path.join(skill, "templates", "template.html"), encoding="utf-8").read()
words = title.split()
h1 = html.escape(" ".join(words[:-1]) + " " if len(words) > 1 else "") + \
     '<span class="accent">%s</span>' % html.escape(words[-1])
t = rep(t, "<title>MOI deck</title>", "<title>%s</title>" % html.escape(title))
t = rep(t, 'Deck <span class="accent">title</span>', h1)
t = rep(t, "Chip label &middot; Month Year", "TODO chip label &middot; Month Year")
t = rep(t, "One line under the title.", "TODO one line under the title.")
t = rep(t, '"Speaker script for slide 1."', '"TODO speaker script for slide 1."')

s = open(os.path.join(skill, "templates", "SCRIPT.md"), encoding="utf-8").read()
s = rep(s, "# DECK TITLE: speaking script", "# %s: speaking script" % title)
s = rep(s, "\nSpeaker script for slide 1.\n", "\nTODO speaker script for slide 1.\n")

readme = """# %(t)s deck

`index.html` is the deck: 1 slide so far. Update this count whenever slides are added or removed.

- Present: open `index.html` in Chrome. Arrow keys, space or a click to move. Press `P` for the presenter window (script, next-slide title, clock). Share the deck window and keep the presenter window on your own screen.
- Check and export: set SKILLS to the folder that holds the moi-* skill folders, work from the repo root, then run `python3 "$SKILLS/moi-webinar/deck/scripts/check-deck.py" %(f)s/deck/index.html --script %(f)s/SCRIPT.md --layout` and `bash "$SKILLS/moi-webinar/deck/scripts/render.sh" %(f)s/deck/index.html`. The PDF is slides only, with no script.

| | |
| --- | --- |
| flow | title |
| source | who supplied the material, and when |
| photos | none yet; files go in `assets/` and a slot shows its filename until the file exists |
| variants | none. If a variant is needed, edit `index.html` first and re-cut the variant from it |
| script | `../SCRIPT.md`, identical to the `NOTES` array in `index.html` |
| left out | numbers nobody supplied, claims that could not be sourced, empty photo slots |
""" % {"t": title, "f": folder}

deck = os.path.join(folder, "deck")
os.makedirs(os.path.join(deck, "assets"), exist_ok=True)   # first write, after every check and substitution
open(os.path.join(deck, "index.html"), "w", encoding="utf-8").write(t)
made = [os.path.join(deck, "index.html"), os.path.join(deck, "assets") + "/"]
for path, text in ((os.path.join(deck, "README.md"), readme), (os.path.join(folder, "SCRIPT.md"), s)):
    if os.path.exists(path):
        print("kept existing", path)
    else:
        open(path, "w", encoding="utf-8").write(text)
        made.append(path)
for m in made:
    print("created", m)
PY
echo "next: add the slides (one TITLES entry and one NOTES entry for each), then run python3 \"\$SKILLS/moi-webinar/deck/scripts/check-deck.py\" \"$deck/index.html\" --script \"$folder/SCRIPT.md\""
