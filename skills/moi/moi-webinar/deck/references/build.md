# Building, checking, rendering and not breaking the deck

Commands assume `SKILLS` is set and you are in the working copy of the repo (see `../GUIDE.md`, "Before you start"). `<s>` is the session folder, such as `community-call-15`. Every path is written in full, so no command depends on any other working directory.

## Check

```
python3 "$SKILLS/moi-webinar/deck/scripts/check-deck.py" <s>/deck/index.html --script <s>/SCRIPT.md --layout
```

One line per check, PASS, WARN, FAIL or SKIPPED. Exit 1 on any FAIL. Letters are stable.

| | Checks | Fails when |
| --- | --- | --- |
| a | the inline script parses (`node --check`) | a real line break or a missing comma in `NOTES`: arrow keys, dots and presenter window die while the PDF still prints. If node is missing the line says SKIPPED in capitals. It is not a pass |
| b | every slide is a direct child of the stage; every badge sits inside its slide | a stray `</div>` re-parents later slides outside the scaled stage |
| c | badge equals page number; cover and close carry none | a slide has the wrong, a missing or an extra badge |
| d | no two neighbours share a background | `lav` next to `lav`; warns for `dark` next to `dark grad` |
| e | `TITLES` and `NOTES` have one entry per slide | the counts differ from the slide count |
| f | retired phrases; presenter title matches the document title | FAIL: "Voyage devnet", "account-centric", "12:00 AM UTC", or a hard-coded presenter title that names another deck. WARN with the reason: "Open Q&A" and "Building in Public", which were removed from the community call 14 close and title on 2026-09-24/25 and which another deck may still want. Add FAIL phrases with `--stale "phrase"` | <!-- slop-lint:ignore -->
| g | no em dash in slide text, notes or titles | warns when only the document title has one |
| h | `NOTES` equal `SCRIPT.md` sections | the words differ; warns when only markup or cue notation differs |
| i, j, k, l, m, n | stale time words, missing files, stale README count, identical variants, TODO markers, "not X, not Y" | all WARN only | <!-- slop-lint:ignore -->
| o | `--layout`: no content runs off the slide (measured in Chrome, `$CHROME_FLAGS` honoured) | content passes y=1080 or x=1920, or text is clipped inside a code block; warns below y=990 |

`--skip LETTERS` skips checks (shown as SKIPPED). `--require-node` turns a missing node into a FAIL. A WARN is a question for a person, not a block: read it and decide.

What it said about the real decks on 2026-10-02, run on the previous operator's copies. Community call 14's deck is now in `moi-foundation/MOI-Webinars` under `community-call-14/deck/` (merged 13 October 2026; a cleaned copy is in `moi-webinar/community-call/examples/cc14`), and the intro session deck is in the handover repo at `others/webinars/intro-session-deck/`. Session 8 is in `session-8-policies/` on branch `claude/agent-payments-simple` of `moi-foundation/MOI-Webinars`. Community call 14 failed b, c, d and f (a stray `</div>` on slide 10, slides 7-8 and 9-10 sharing backgrounds, a presenter title reading "MOI Builders · Intro"). The intro session failed a (a real line break in the slide 4 notes) and g. Session 8 failed d, g and o (the last line of the slide 10 code block is clipped) and warned on b, f, h and i; its `NOTES` use a different cue notation from its `SCRIPT.md`. Details in `references/traps.md`.

## Render

```
bash "$SKILLS/moi-webinar/deck/scripts/render.sh" <s>/deck/index.html                      # writes <s>/deck/index.pdf
bash "$SKILLS/moi-webinar/deck/scripts/render.sh" <s>/deck/index.html Name.pdf             # a bare name: writes <s>/deck/Name.pdf
bash "$SKILLS/moi-webinar/deck/scripts/render.sh" <s>/deck/index.html out/Name.pdf         # a name with a slash: exactly there
bash "$SKILLS/moi-webinar/deck/scripts/render.sh" <s>/deck/index.html <s>/deck/index-b.html  # two PDFs, each beside its HTML
bash "$SKILLS/moi-webinar/deck/scripts/render.sh" --force <s>/deck/index.html             # renders even though a check FAILed
```

Exactly what it does:

1. Runs `check-deck.py` on each deck, with `--layout`, and with `--script` if a `SCRIPT.md` sits beside the deck or in the folder above it. It prints only the lines that are not PASS.
2. Refuses to render a deck with any FAIL and says so. `--force` overrides this. Use it only when the operator has said to render anyway.
3. Prints the deck to PDF with headless Chrome, into a temporary file (print CSS puts one 1920 by 1080 slide on each page and forces every reveal visible). The PDF is slides only: no animation, no notes.
4. Counts slides and the pages of that temporary file (`pdfinfo`). On a match it moves the file into place and prints `wrote <full path> (new)` or `(replaced)`. On a mismatch it exits 1, leaves any existing PDF untouched, writes no PDF under the asked name, and keeps the bad render as `<name>.pdf.rejected` beside it (an older `.rejected` file is overwritten, and a later good render prints a note that one is still there). A mismatch means a malformed `<section>` or a slide that spills onto a second page.
5. Names the output: with one deck and one `.pdf` argument, a bare name goes beside the deck and a name with a slash is used as given (its folder must exist). With one deck and no name, or with several decks, each PDF goes beside its HTML as `<html name>.pdf`. To keep existing PDF names for several decks, render them one at a time with a name each.

If Chrome wrote nothing, an existing PDF is left as it was. A render that finds a different page count leaves the old PDF in place.

Chrome is found through `$CHROME`, then `Google Chrome` or `Chromium` in `/Applications`, then `google-chrome`, `chromium` on the path. `$CHROME_FLAGS` adds flags (for example `--no-sandbox` in a container) for both the render and check o. `$RENDER_TIMEOUT` (default 60 seconds) stops a Chrome that wrote the PDF but did not exit; check o gives up after 90 seconds and says SKIPPED. Tested with Google Chrome 154 on macOS on 2026-10-02; not tested on Linux. Exit codes: 0 all good, 1 refused, failed or page-count mismatch, 2 bad usage or no Chrome.

What was observed with Chrome 154 on macOS, 2026-10-02. In a shell that let Chrome run normally, the default profile exits on its own: a six-slide deck rendered with the layout check in about 9 seconds. Started with a temporary `--user-data-dir`, Chrome wrote the PDF and was still running 45 seconds later (reproduced that day, cause not isolated), so `render.sh` passes no profile directory and stops a lingering Chrome. A reviewer's sandboxed shell saw headless Chrome hang even with the default profile, and check o took 90 seconds to print SKIPPED; that was not reproduced where Chrome ran normally. In a sandboxed shell, run `render.sh` and check o outside it, or inspect the PDF pages by hand and say that check o was SKIPPED. Chrome also writes its own state under the user's profile folders (on macOS `~/Library/Application Support/Google/`); that is Chrome, not the scripts.

Needs: python3, Chrome. Optional: node (check a), poppler (`pdfinfo`, `pdftoppm`). Fonts: Poppins loads from Google Fonts when the deck is opened or rendered, so the machine needs a network, or the text falls back to a plain sans-serif.

## Look at the pages

The checker cannot judge how a slide looks. Read the PDF pages back as images and look at every slide you touched and its neighbours:

```
d=$(mktemp -d) && pdftoppm -r 40 -png <s>/deck/index.pdf "$d/p" && ls "$d"
```

Look for cut-off text, a vanished last code line, empty photo frames, the right badge, and a background that matches its neighbours' alternation. Compare the page count with the slide count you expect.

## After deleting, inserting or moving a slide

Do all of these, then run the checker again.

1. Move, drop or add the same-index entry in `TITLES` and `NOTES`, and the section in `SCRIPT.md`. Renumber its `PRESS NEXT --> SLIDE N` headers.
2. Renumber every badge (check c).
3. Re-alternate backgrounds (check d).
4. Search the other slides and notes for the removed topic's key words. Community call 14 kept "what our campaign is doing" and "verify the campaign click-through" after the campaign slide was cut, and a sentence about movement after the arrows were removed.
5. Update `README.md`: slide count, flow line, photo slots, variants (check k).
6. Re-cut variants, delete PDFs that no longer match any HTML (a gate), re-render.

Before deleting on "remove slide 6", say back "slide 6 is titled X" and wait for a yes. Badges once ran one behind the pages and the wrong slide was deleted.

## Editing an existing deck safely

- Edit with a script that asserts before it writes, so a near miss fails instead of doing nothing:

```python
old = "exact text from the file"
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new, 1)
```

- Match the file, not the rendered text: attributes, `&middot;`, `&amp;` and non-breaking spaces all differ.
- Do notes through `sync-notes.py`, not by hand (`references/spoken-script.md`).
- Batch the edits and render once.
- Asked to fix a script, fix the script; do not redesign the deck. Asked for one slide's text, hand over the text and leave the file alone.
- After regenerating, say the exact file path that is fresh, reopen it in a new browser tab, and read one slide's notes in the presenter window. On 4 Sep 2026 the presenter window showed an old script across at least six messages after regenerates; the cause was not found.
- Find the cause of a b failure from the line number the checker prints: the extra `</div>` is on or just above it.

## Variants

Two versions of one deck, for example with and without a guest, are two files in the same folder, each with its own PDF. Edit the primary and re-cut the variant from it, so they never drift. Name the primary on hand-back. When check l warns that they are byte-identical, collapse them to one deck and one PDF. On the previous operator's machine on 2026-10-02, community call 14's two HTML files were byte-identical and its two PDFs had identical text, 12 pages each. Ask before deleting a file.

## Photos and logos

- Real files only, under `deck/assets/`, named for what they are (`futuremode-1.png`). Any web format works. A frame with no file shows its filename, so a deck can ship with holes. Check j lists them: put them in the hand-back.
- Never generate or substitute an image on a slide about a real event or person. Do not guess a guest's job title; leave it off.
- A guest's headshot and company logo go in `deck/assets/guest/` as `headshot.jpg` and `logo.svg`, the names the guest component reads (`guest-slide.md`).
- Gather guest and partner logos early. They are easy to forget.
- On macOS a tool can be blocked from reading `~/Downloads` or the Desktop. Ask the operator to `cp` the file into the session folder first.
- Brand logos come from the owner's own site or Wikimedia Commons. Downloading a logo is a gate: name the file and its source and wait for a yes. Find the exact file name first, because a wrong guess saves an HTML 404 page as the logo. The search prints and saves nothing; the second command saves a file, so it needs the yes:

```
curl -s "https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=<brand>%20logo%20filetype:drawing&srnamespace=6&srlimit=10&format=json"
curl -sSL -o <s>/deck/assets/engines/name.svg "https://commons.wikimedia.org/wiki/Special:FilePath/<exact file name>"
file --mime-type <s>/deck/assets/engines/name.svg
```

Look at the render. Wordmarks carry stray bounding boxes and mix badly with icon marks; prefer the square icon when the label is on the slide.

## Presenting live

Open `<s>/deck/index.html` in Chrome. Arrow keys, space or a click to move, Home and End to jump, the dots at the bottom to pick a slide, and `index.html#7` opens at slide 7. Press `P` for the presenter window (script, next-slide title, clock); it also drives the deck. Allow pop-ups for the file if it does not open. In the video call share the deck window and keep the presenter window on your own screen. Keep the PDF as a fallback: it has no animation and no notes. Do a dry run the day before.

## Not yet known

- Which repo and branch the session folders belong in. Community call decks 2 to 14 are in `moi-foundation/MOI-Webinars` under `community-call-N/deck/` (merged 13 October 2026). The intro session deck is in the handover repo (`others/webinars/intro-session-deck/`); whether it also belongs in the webinars repo is not recorded (the previous DevRel's notes); ASK: Rahul. Those notes list putting the deck tooling in the repo as a to-do; they are not in this library.
- Whether macOS still blocks tools from reading `~/Downloads`. It did in August and September 2026.
