#!/usr/bin/env bash
# new-session.sh: scaffold a MOI Builders session folder from this skill's templates.
#
# Usage:   bash "$SKILLS/moi-webinar/scripts/new-session.sh" <session-folder> "<title>"
#          e.g. bash "$SKILLS/moi-webinar/scripts/new-session.sh" session-10 "MOI Builders #10: Topic in plain words"
#          Run it from the root of a working copy of moi-foundation/MOI-Webinars.
#          SKILLS is the folder that holds the moi-* skills.
# Folder:  session-<N> or session-<N>-<slug>: lower-case letters, digits and hyphens, a plain name with no slash.
# Makes:   <folder>/README.md STORYLINE.md NOTES.md RUNBOOK.md GAMEDAY.md LUMA.md SOCIAL.md .gitignore,
#          an empty social/ folder, ledger.csv (copied from the moi-devrel/claim-check template when that skill is found),
#          and, through moi-webinar/deck's new-deck.sh, deck/ and SCRIPT.md.
#          Placeholders in the templates: {{TITLE}} {{NUMBER}} {{PREV}} {{ROMAN}} {{FOLDER}}.
# Finds:   the deck branch and the claim ledger template under $SKILLS when it is set, else beside this
#          skill (one folder up from here). The session templates always come from this skill.
# Refuses: a folder that already exists (nothing is changed); an empty title; a title with an em dash, a
#          line break, a control character or "{{"; a title over 120 characters; a folder name that does
#          not fit the pattern; a working directory that is inside a git repository but is not its root.
#          Every check runs before anything is created, so a refusal leaves nothing behind.
# Writes:  only inside the new folder (staged in a temporary folder first). It does not commit, push, post
#          or call the network. The .gitignore it writes keeps the internal documents out of git: that is
#          a default for the operator to confirm before any commit, because the repo is public.
# Exit:    0 created, 1 refused, 2 bad usage.
# Works under bash 3.2 and zsh (run it with bash). Python 3 standard library only.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
export SCRIPT_DIR
if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  sed -n '2,24p' "${BASH_SOURCE[0]:-$0}" | sed 's/^# \{0,1\}//'
  exit 0
fi
if [ $# -ne 2 ]; then
  echo 'usage: new-session.sh <session-folder> "<title>"   e.g. new-session.sh session-10 "MOI Builders #10: Topic"' >&2
  exit 2
fi
exec python3 - "$1" "$2" <<'PY'
import os
import re
import shutil
import subprocess
import sys
import tempfile

folder, title = sys.argv[1], sys.argv[2]
script_dir = os.environ["SCRIPT_DIR"]
skill_dir = os.path.dirname(script_dir)
tdir = os.path.join(skill_dir, "templates")
library = os.path.dirname(skill_dir)


def sibling(rel):
    """A file of another skill or branch: under $SKILLS when set, else beside this skill."""
    for base in (os.environ.get("SKILLS", ""), library):
        if base and os.path.isfile(os.path.join(base, rel)):
            return os.path.join(base, rel)
    return os.path.join(library, rel)


def refuse(msg):
    print("REFUSED: " + msg + " Nothing was created.", file=sys.stderr)
    sys.exit(1)


def roman(n):
    out = ""
    for v, s in ((1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
                 (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while n >= v:
            out += s
            n -= v
    return out


# 1. the folder name
m = re.fullmatch(r"session-([0-9]{1,3})(-[a-z0-9]+)*", folder)  # fullmatch: "$" would let a trailing line break through
if not m:
    refuse("the folder name %r must look like session-10 or session-10-topic "
           "(lower case letters, digits and hyphens, no slash)." % folder)
number = int(m.group(1))
if number < 1:
    refuse("the session number must be 1 or more.")

# 2. the title
if not title.strip():
    refuse("the title is empty.")
if chr(0x2014) in title:
    refuse("the title has an em dash. Use a colon or a comma.")
if any(ord(c) < 32 or ord(c) == 127 for c in title):
    refuse("the title has a line break or another control character.")
if "{{" in title or "}}" in title:
    refuse("the title has a template marker.")
title = " ".join(title.split())
if len(title) > 120:
    refuse("the title is %d characters; keep it to 120 or fewer." % len(title))

# 3. templates present
names = ["README.md", "STORYLINE.md", "NOTES.md", "RUNBOOK.md", "GAMEDAY.md", "LUMA.md", "SOCIAL.md"]
for n in names + ["gitignore.txt"]:
    if not os.path.isfile(os.path.join(tdir, n)):
        refuse("template %s is missing from %s." % (n, tdir))

# 4. where we are
try:
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=10)
    top = top.stdout.strip() if top.returncode == 0 else ""
except (OSError, subprocess.SubprocessError):
    top = ""
if top and os.path.realpath(top) != os.path.realpath(os.getcwd()):
    refuse("run this from the root of the working copy (%s), not from a subfolder." % top)
if not top:
    print("WARN  not inside a git repository: the folder is created in the current directory.")

# 5. no overwrite
if os.path.lexists(folder):
    refuse("%s already exists. Edit that folder, or pick another name." % folder)

# 6. render in memory
subs = {
    "{{TITLE}}": title,
    "{{NUMBER}}": str(number),
    "{{PREV}}": str(number - 1) if number > 1 else "none",
    "{{ROMAN}}": roman(number),
    "{{FOLDER}}": folder,
}
docs = {}
for n in names:
    text = open(os.path.join(tdir, n), encoding="utf-8").read()
    for k, v in subs.items():
        text = text.replace(k, v)
    left = re.findall(r"\{\{[A-Z]+\}\}", text)
    if left:
        refuse("template %s still has %s after substitution (a bug in the template)." % (n, left[0]))
    docs[n] = text
docs[".gitignore"] = open(os.path.join(tdir, "gitignore.txt"), encoding="utf-8").read()

ledger_src = sibling("moi-devrel/claim-check/templates/claim-ledger.csv")
new_deck = sibling("moi-webinar/deck/scripts/new-deck.sh")

# 7. stage, then move into place
stage = tempfile.mkdtemp(prefix="new-session-")
made = []
try:
    root = os.path.join(stage, folder)
    os.makedirs(os.path.join(root, "social"))
    for n, text in docs.items():
        with open(os.path.join(root, n), "w", encoding="utf-8") as f:
            f.write(text)
    have_ledger = os.path.isfile(ledger_src)
    if have_ledger:
        shutil.copyfile(ledger_src, os.path.join(root, "ledger.csv"))
    shutil.move(root, folder)
finally:
    shutil.rmtree(stage, ignore_errors=True)

for n in sorted(docs):
    made.append(os.path.join(folder, n))
made.append(os.path.join(folder, "social") + "/")
if have_ledger:
    made.append(os.path.join(folder, "ledger.csv"))

# 8. the deck, through moi-webinar/deck
deck_note = ""
if os.path.isfile(new_deck):
    r = subprocess.run(["bash", new_deck, folder, title], capture_output=True, text=True)
    if r.returncode != 0:
        shutil.rmtree(folder, ignore_errors=True)
        print("REFUSED: moi-webinar/deck new-deck.sh failed, so the new folder was removed again.", file=sys.stderr)
        print((r.stderr or r.stdout).strip(), file=sys.stderr)
        sys.exit(1)
    for line in r.stdout.splitlines():
        if line.startswith("created ") or line.startswith("kept existing "):
            made.append(line.split(" ", 1)[1].replace("existing ", "", 1))
else:
    deck_note = "moi-webinar/deck was not found under $SKILLS or inside this skill, so no deck and no SCRIPT.md were made."

for p in made:
    print("created", p)
if not have_ledger:
    print("note: moi-devrel/claim-check was not found under $SKILLS or beside this skill, so ledger.csv was not made.")
if deck_note:
    print("note: " + deck_note)
print("")
print("Next, in this order:")
print("  1. Fill %s/STORYLINE.md and get the lead's yes before building anything (references/topic-and-storyline.md)." % folder)
print("  2. Run: bash \"$SKILLS/moi-webinar/scripts/session-preflight.sh\" %s" % folder)
print("  3. Nothing is committed. %s/.gitignore keeps the internal documents out of git by default; the repo is" % folder)
print("     public, so a push publishes everything else. Confirm the ignore list with the operator before any commit.")
PY
