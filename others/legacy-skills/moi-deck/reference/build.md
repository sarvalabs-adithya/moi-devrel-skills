# Building, rendering and not breaking the deck

## Render

```bash
~/.claude/skills/moi-deck/scripts/render.sh <session>/deck/index.html                       # -> index.pdf
~/.claude/skills/moi-deck/scripts/render.sh deck/index.html MOI_Community_Call_14.pdf       # keep an existing name
~/.claude/skills/moi-deck/scripts/render.sh deck/index.html deck/index-no-guest.html        # both variants
```

It checks the deck's JavaScript, prints the PDF next to the HTML, and compares the slide count to the
page count. A mismatch means a malformed `<section>`.

Then look at the result. Read the PDF pages back as images and check the slides you touched. The PDF
is the only way to catch an overflowing slide, because the print stylesheet forces every slide onto
its own page and makes all the `rv` reveals visible.

## Two traps that have bitten

**Real newlines inside `NOTES`.** The array holds JavaScript strings. A literal line break inside one
is a syntax error, the whole inline script dies, and the deck still *looks* fine: the PDF prints
because print CSS needs no JavaScript. What breaks is arrow keys, the dots and the presenter window.
Write `\n`, or build the entry with `json.dumps(text)` in Python. `render.sh` fails loudly on this.

**A missing comma between entries.** Same symptom. Same check catches it.

## Editing an existing deck

Edit with a script that asserts before it writes, so a near-miss fails instead of silently doing
nothing:

```python
old = "exact text from the file"
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new, 1)
```

Match against the file, not against what you think is in the file. Attributes, `&middot;`, `&amp;` and
non-breaking spaces all differ from the rendered text.

After inserting, deleting or moving a slide: renumber every `slide-num` badge to its page number, and
move or drop the matching `TITLES` and `NOTES` entries by the same index. The badge and the page
number must agree, or "remove slide 6" becomes ambiguous for everyone afterwards.

## Variants

Two versions of one deck, say with and without a guest speaker, are two files in the same folder:
`index.html` and `index-no-guest.html`, each with its own PDF. They drift the moment someone edits
one, so edit the primary and re-cut the variant from it rather than repeating the change by hand.
Say which file is the primary on hand-back.

## Photos

Real files only, under `<session>/deck/assets/`. Name them for what they are: `futuremode-1.png`,
`mohit.webp`. Any web format works. A `photo` frame with no file shows the filename it wants, so a
deck can ship with holes and fill them later without touching the markup.

Never generate or substitute an image on a slide that claims to show a real event or person.

## Brand logos

Take them from the owner's own site, or from Wikimedia Commons:

```bash
curl -sSL -o assets/engines/gemini.svg \
  "https://commons.wikimedia.org/wiki/Special:FilePath/Google_Gemini_icon_2025.svg"
```

Find the exact filename first, because a wrong guess returns a 404 HTML page that `file --mime-type`
exposes:

```bash
curl -s "https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=<brand>%20logo%20filetype:drawing&srnamespace=6&srlimit=10&format=json"
```

Then look at the render. Wordmarks carry stray bounding boxes and mix badly with icon marks; prefer
the square icon when the label is already on the slide.

## The script

One `NOTES` entry per slide, in slide order, written to be spoken. Run the `humanizer` skill over it
before handing back. Save a copy as `<session>/SCRIPT.md` when the presenter wants it outside the deck.

Cues for live moments go in brackets inside the entry, e.g.
`[If the host asks the zero-KMOI question here: …]`.

## Hand-back

Send the HTML and the PDF, name the primary file, and list anything you left out and why: numbers
nobody supplied, photo slots still empty, claims you could not source. Presenting is `index.html` in
Chrome, arrow keys to move, `P` for the presenter window, share the deck window and keep the presenter
window on your own screen.

## A deck to copy from

`~/MOI-Webinars/community-call-14/deck/` is the reference build: 12 slides, four
backgrounds, cards, stats with brand logos, a comparison table, photo frames, a ghost numeral cover
and a two-file variant. `~/MOI-Webinars/intro-session/deck/` is the same framework at session length.
