# moi-webinar/deck evals

Seven prompts with the behaviour expected, then the test log of the scripts. Test date 2026-10-02, Google Chrome 154, node 24, python 3.13, poppler `pdfinfo`, macOS. In the log `$SKILLS` is the folder that holds the skill folders, `$W` a `mktemp -d` scratch folder, and commands are run from `$W`. Paths in the output are trimmed to relative or `$W`. After the folder moved into `moi-webinar` (2026-10-04) the good-input checks, the cc14 example, `render.sh` (the six-slide render, the refusal, `--force`, the page-count rejection), `new-deck.sh` and `sync-notes.py` were run again from `moi-webinar/deck/scripts/` with the same results; none of these scripts locates another skill, only its own `templates/`.

## Prompts

### 1. Deck from a raw dump
Prompt: Here is the Slack thread and the release note for community call 15. Make the deck.
Expect: sets or asks for `SKILLS` and runs every command in full from the working copy; runs `new-deck.sh` for a new session folder; shows a short slide plan with the source of each figure before building; uses components from `references/components.md`, alternates backgrounds and adds one `TITLES` and one `NOTES` entry for every slide; invents no figure, guest title or event outcome and says what it left out; writes `SCRIPT.md` only for slides the presenter speaks; ends with `check-deck.py --script --layout`, `render.sh`, a look at the PDF pages, and a hand-back with `Ready: yes` or `Ready: no, because ...`. Does not commit, push, download a logo or send anything without a yes.
Why: the community call 14 build ran about 18 edit rounds, and its unsourced sentences and unconfirmed figures were found afterwards.

### 2. Remove a slide
Prompt: Remove slide 6.
Expect: says back the title of slide 6 and waits for a yes. Then removes the slide, the same-index `TITLES` and `NOTES` entries and the `SCRIPT.md` section, renumbers every badge and every `PRESS NEXT --> SLIDE N` header, re-alternates backgrounds, searches the other slides and notes for words about the removed topic, updates the README count, re-runs the checker, re-renders and looks at the pages.
Why: badges once ran one behind the pages and the wrong slide was deleted. Community call 14 kept notes about a deleted campaign slide, and slides 7-8 and 9-10 ended up with equal backgrounds.

### 3. Script for slides 2 to 4
Prompt: Write the script for slides 2 to 4.
Expect: long, warm, complete sentences that can be read aloud verbatim; no "not this, not that"; no em dashes; no applause or hand-the-floor closers; a `PRESS NEXT --> SLIDE N` header for each block and bracketed cues on their own line; plain text with no markdown emphasis. Writes `SCRIPT.md` first, then runs `sync-notes.py` (dry run, then `--confirm`), then `check-deck.py --script` so check h passes. Does not describe the voice as "short sentences". Calls the author of the corrections "the previous operator", never "the operator". <!-- slop-lint:ignore -->
Why: the previous operator corrected cold, staccato and contrastive scripts on 5 Aug and 4 Sep 2026 and again on 25 Sep.

### 4. Keys do nothing but the PDF looks fine
Prompt: The deck arrow keys and the presenter window do not work. The PDF looks fine.
Expect: runs `check-deck.py`, finds check a (or b), quotes the line it reports, fixes the cause (a real line break or missing comma in `NOTES`, repaired by `sync-notes.py --confirm`, or a stray `</div>`), and re-runs until clean. Does not only re-render the PDF.
Why: the intro session deck (held by the previous operator; ASK: Adithya for a copy) has this fault in the slide 4 notes as of 2026-10-02, and community call 14 had it on 24 Sep. The PDF cannot show it.

### 5. Render over a failed check, and a wrong page count
Prompt: Render it.   (the deck has a FAIL)
Expect: `render.sh` refuses, and the reply shows the FAIL lines and fixes them. It uses `--force` only if the operator says to render anyway. If a render reports REJECTED, it says the old PDF is untouched, names the `.pdf.rejected` file and finds the malformed `<section>` or the slide that spills.
Why: the stray `</div>` on community call 14 slide 10 passed the old render script, node check and page count.

### 6. A guest speaker, and a version without
Prompt: Our guest this month is Priya from Acme. Add a guest slide, and give me one version with the guest speaker and one without.
Expect: builds the slide from the guest component in `references/guest-slide.md` (large headshot, name, role, company, logo, topic), not from `photos`; points the images at `assets/guest/headshot.jpg` and `assets/guest/logo.svg` and asks for both with the sizes, plus the role, company as written and topic; leaves role and topic as dashed slots until supplied and never looks them up; lists the missing files from check j on hand-back. Then edits `index.html` as the primary and cuts `index-no-guest.html` from it, renumbering badges and `NOTES`; renders each to its own named PDF one at a time (`render.sh <s>/deck/a.html Name.pdf`, which lands beside the deck); names the primary on hand-back. If the two files later become identical it says so (check l) and asks before deleting.
Why: community call 14 shipped two byte-identical HTML files and two PDFs with identical text, and its README still said "13 slides". Its draft guest slide, a small portrait under a column of text, was rejected on 2026-10-09 in favour of a large headshot with role, company and a logo placeholder.

### 7. A deck of three slides fails check c
Prompt: check-deck.py says "slide 3 (close) carries badge 03" on my community call deck of a cover and two content slides. That is expected for a call deck, right?
Expect: Says no. The last slide is the close and carries no badge, so the checker is right and the deck has no close slide. Adds a close slide (logo and one line) after the last content slide, one `TITLES` entry and one `NOTES` entry for it, and re-runs the checker. Does not remove the badge, does not render with `--force` over the FAIL, and does not tell the reader that a FAIL is expected.
Why: A new-hire test on 2026-10-04 took this FAIL for a fault in the checker. A copy of the mini-deck cut to its cover and its first two content slides fails check c; the same cut with the close kept instead (cover, one content slide, close) gives `RESULT: ok (0 FAIL, 0 WARN, 1 SKIPPED, 13 PASS)`. The community-call slide plan ends in a close (`moi-webinar/community-call/references/slide-plan.md`).

## Test log

Commands are written as typed. Output is trimmed to the lines that matter.

### check-deck.py on good inputs

```
python3 "$SKILLS/moi-webinar/deck/scripts/check-deck.py" "$SKILLS/moi-webinar/deck/templates/template.html" --script "$SKILLS/moi-webinar/deck/templates/SCRIPT.md" --layout
RESULT: ok (0 FAIL, 0 WARN, 0 SKIPPED, 15 PASS)
python3 "$SKILLS/moi-webinar/deck/scripts/check-deck.py" "$SKILLS/moi-webinar/deck/examples/mini-deck/index.html" --script "$SKILLS/moi-webinar/deck/examples/mini-deck/SCRIPT.md" --layout
RESULT: ok (0 FAIL, 0 WARN, 0 SKIPPED, 15 PASS)
```

### check-deck.py on the real decks (2026-10-02, the previous operator's working copy)

| Deck | Result | What it found |
| --- | --- | --- |
| community call 14 (with its `SCRIPT.md`) | 4 FAIL, 5 WARN | FAIL b (a stray `</div>` on slide 10), c (slide 10 has no badge), d (slides 7-8 and 9-10 share backgrounds), f (the presenter title reads "MOI Builders · Intro"). WARN: em dash in the document title, relative words, README says 13 slides, `index-no-guest.html` identical, content near the bottom margin |
| intro session | 2 FAIL, 3 WARN | FAIL a (a real line break in the slide 4 notes), g (an em dash in a code comment). WARN f, i, n |
| session 8 (with its `SCRIPT.md`) | 3 FAIL, 4 WARN | FAIL d (slides 10 to 13 are all `light`), g (em dashes on slides 2, 3, 9 to 12, 15, 17 and in the slide 14 notes), o (the last line of the slide 10 code block is clipped). WARN b (two `</div>` missing before `</body>`), f (hard-coded presenter title), h (15 of 19 sections identical, the rest use a different cue notation), i |

Community call 14 and the intro session are not in a repository; only the previous operator has them. A cleaned community call 14 is `moi-webinar/community-call/examples/cc14`.

### check-deck.py on bad inputs (copies of the mini-deck, each broken one way, `--skip o`)

| Break | Result |
| --- | --- |
| an extra `</div>` at the end of slide 3 | FAIL b "slides 4, 5, 6: parent is div.deck-viewport, not the stage", with the line of the stray tag; exit 1 |
| a real line break inside the first `NOTES` string | FAIL a `SyntaxError: Invalid or unexpected token (deck line 299)` and FAIL h |
| slide 4's `lav` changed to `light` | FAIL d "slides 4 and 5 are both 'light'" |
| the last `NOTES` entry deleted | FAIL e "NOTES has 5 entries, the deck has 6 slides", FAIL h |
| badge 04 changed to 05 | FAIL c "slide 4 carries badge "05"" |
| the mini-deck cut to its first three slides (cover, two content slides, badge 03 on the last), run without `--layout` (2026-10-04) | FAIL c "slide 3 (close) carries badge 03; cover and close carry none"; `RESULT: FAIL (1 FAIL, 0 WARN, 1 SKIPPED, 12 PASS)`, exit 1. The cut of slides 1, 2 and 6 (cover, content, close) gives `RESULT: ok (0 FAIL, 0 WARN, 1 SKIPPED, 13 PASS)`. The checker is right: the last slide is the close |
| an em dash, "Voyage devnet" and "last Friday" in slide text | FAIL f, FAIL g, WARN i | <!-- slop-lint:ignore -->
| one word changed in `SCRIPT.md` | FAIL h "slide 4 differs at character 42" |
| `env PATH=/nonexistent <python3> ... check-deck.py` | `SKIPPED a  node not found: the script was NOT syntax-checked`; the RESULT line ends "check a did NOT run". With the line-break copy: FAIL a from the fallback scan. With `--require-node`: FAIL a |
| no argument, and a missing file | usage and exit 2; "cannot read" and exit 2 |
| `.env`, `marker.env`, and an env file given as `--script` (2026-10-04) | exit 2 each: "check-deck: refusing to read ...: an env file can hold keys and is never opened." Before the fix `.env` was opened and gave "0 slides" and exit 1 |

Check f split (copies of the mini-deck with one phrase added to slide 4):

```
"Open Q&A"                          WARN f  check by eye: a phrase removed from an earlier deck
                                     slide 4: "Open Q&A" (removed from the community call 14 close, 2026-09-24/25; ...)   exit 0
"Building in Public"                WARN f  (same shape, with its own reason)   exit 0
"Voyage devnet"                     FAIL f  retired phrase or stale presenter title   exit 1
"Open Q&A" and "12:00 AM UTC"       FAIL f  lists "12:00 AM UTC" and, under it, the Open Q&A reason   exit 1
```

`$CHROME_FLAGS` in check o: with `CHROME` pointing at a wrapper that logs its arguments and then runs Chrome, and `CHROME_FLAGS="--lang=en-GB --no-first-run"`, the logged command line was `--headless=new --disable-gpu --window-size=1920,1080 --virtual-time-budget=8000 --lang=en-GB --no-first-run --dump-dom file://...`.

### render.sh

```
cd $W && bash "$SKILLS/moi-webinar/deck/scripts/render.sh" mini/index.html Name.pdf
wrote $W/mini/Name.pdf (new): 6 slides, 6 pages, match          # beside the deck; $W itself held only mini/
bash "$SKILLS/moi-webinar/deck/scripts/render.sh" mini/index.html Name.pdf
wrote $W/mini/Name.pdf (replaced): 6 slides, 6 pages, match
bash "$SKILLS/moi-webinar/deck/scripts/render.sh" mini/index.html out/x.pdf     # a name with a slash, out/ exists
wrote $W/out/x.pdf (new): 6 slides, 6 pages, match
bash "$SKILLS/moi-webinar/deck/scripts/render.sh" rr/stray.html                 # the stray </div> copy
FAIL b ...                                                            # exit 1, no PDF written, REFUSED line
bash "$SKILLS/moi-webinar/deck/scripts/render.sh" --force rr/stray.html         # WARNING line, then wrote ... stray.pdf (new): 6 slides, 6 pages, match
bash "$SKILLS/moi-webinar/deck/scripts/render.sh" rr/index.html rr/stray.html   # first rendered, second refused, exit 1
bash "$SKILLS/moi-webinar/deck/scripts/render.sh" rr/index.html rr/stray.html x.pdf     # "a .pdf name is only allowed with exactly one deck", exit 2
CHROME=/nonexistent bash "$SKILLS/moi-webinar/deck/scripts/render.sh" rr/index.html     # "CHROME is set to ... not an executable file", exit 2
bash "$SKILLS/moi-webinar/deck/scripts/render.sh"                               # usage, exit 2
bash "$SKILLS/moi-webinar/deck/scripts/render.sh" nope.html                     # "no such file: nope.html", exit 2 (2026-10-04; it was 1)
bash "$SKILLS/moi-webinar/deck/scripts/render.sh" .env                          # "render.sh: refusing .env: an env file can hold keys and is never opened.", exit 2
bash "$SKILLS/moi-webinar/deck/scripts/render.sh" rr/index.html /nonexistent/x.pdf   # "output folder does not exist: /nonexistent", exit 2
zsh "$SKILLS/moi-webinar/deck/scripts/render.sh" rr/index.html                  # (replaced): 6 slides, 6 pages, match
/bin/bash "$SKILLS/moi-webinar/deck/scripts/render.sh" rr/index.html            # macOS bash 3.2.57, same result
```

Page-count mismatch (a copy with a nested `<section class="slide">`, so the script counts 7 slides and Chrome prints 6 pages), with a good `index.pdf` already there:

```
md5 -q mini/index.pdf > before.md5
bash "$SKILLS/moi-webinar/deck/scripts/render.sh" --force mini/mm.html index.pdf
REJECTED: 7 slides but 6 pages, MISMATCH. A malformed <section> or an overflowing slide is the usual cause.
          The bad render is kept as $W/mini/index.pdf.rejected. The existing index.pdf was left untouched.      # exit 1
md5 -q mini/index.pdf   equals before.md5; pdfinfo mini/index.pdf: Pages 6
bash "$SKILLS/moi-webinar/deck/scripts/render.sh" --force mini/mm.html fresh.pdf
          The bad render is kept as $W/mini/fresh.pdf.rejected. No fresh.pdf was written.                       # exit 1
bash "$SKILLS/moi-webinar/deck/scripts/render.sh" mini/index.html index.pdf
wrote $W/mini/index.pdf (replaced): 6 slides, 6 pages, match
note: an older rejected render is still there: $W/mini/index.pdf.rejected
```

Chrome with a temporary `--user-data-dir` (the flag `render.sh` does not use): `"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=8000 --user-data-dir="$(mktemp -d)" --print-to-pdf=t1.pdf file://.../index.html`, watched by process id: the 85 KB PDF existed and the process was still running after 45 seconds, so it was stopped by id. With the default profile, `render.sh` finished a six-slide deck, layout check included, in about 9 seconds. A restricted shell is not covered: a reviewer saw Chrome hang there and that run was not reproduced.

### new-deck.sh (bash, zsh and bash 3.2)

```
bash "$SKILLS/moi-webinar/deck/scripts/new-deck.sh" s1 "  Community   Call 15  "   created deck/index.html, deck/assets/, deck/README.md, SCRIPT.md,
                                  then a "next:" line that names check-deck.py as python3 "$SKILLS/moi-webinar/deck/scripts/check-deck.py" ...
                                  <title>Community Call 15</title>, h1 "Community Call <accent>15</accent>"
bash "$SKILLS/moi-webinar/deck/scripts/new-deck.sh" s1 "Again"                REFUSED: s1/deck/index.html already exists. Nothing was changed.   # exit 1
bash "$SKILLS/moi-webinar/deck/scripts/new-deck.sh" s2 ""                     REFUSED: the title is empty. Nothing was created.                   # exit 1
bash "$SKILLS/moi-webinar/deck/scripts/new-deck.sh" s2 "   "                  same message, exit 1
bash "$SKILLS/moi-webinar/deck/scripts/new-deck.sh" s2 "<tab only>"           same message, exit 1
bash "$SKILLS/moi-webinar/deck/scripts/new-deck.sh" s2 "<non-breaking space>" same message, exit 1
bash "$SKILLS/moi-webinar/deck/scripts/new-deck.sh" s2 "Bad <em dash> title"  REFUSED: the title has an em dash or a line break.                  # exit 1
ls -A after the five refused runs                                    nothing: no folder was created
bash "$SKILLS/moi-webinar/deck/scripts/new-deck.sh" s9                        usage, exit 2
zsh and /bin/bash                                                    created the same files
```

### sync-notes.py

A scaffold deck with three slides added by hand, `TITLES` and `NOTES` still holding one entry each, and a `SCRIPT.md` block for slide 2:

```
check-deck.py <deck> --script SCRIPT.md     FAIL e (TITLES 1 of 4, NOTES 1 of 4), FAIL h, WARN k, WARN m
sync-notes.py <deck> SCRIPT.md              slides to update: 1, 2
                                            empty NOTES entries to add for slides 3, 4 (no script for them yet)
                                            note: TITLES has 1 entries for 4 slides. Add the missing titles by hand (check e).
                                            dry run: nothing written.
sync-notes.py <deck> SCRIPT.md --confirm    rewrote the NOTES array (4 entries, 2 updated, 2 empty added)
check-deck.py <deck> --script SCRIPT.md     FAIL e, now only "TITLES has 1 entries, the deck has 4 slides"
                                            (TITLES added by hand and README count fixed)   RESULT: ok (0 FAIL, 0 WARN, 0 SKIPPED, 15 PASS)
sync-notes.py <deck> SCRIPT.md              nothing to change: NOTES already match the 2 sections of SCRIPT.md
a script with a section for slide 7         the script has a section for slide 7 but the deck has only 4 slides; add the slide to the deck first   # exit 1
no deck argument                            usage, exit 2
missing script file, or .env / marker.env   "cannot read: ..." exit 2 (was 1); "sync-notes: refusing to read ..." exit 2
a deck with no NOTES array                  "no 'var NOTES = [ ... ]' array found" exit 2 (was 1)
a script with no SLIDE N headings           "no slide sections found" exit 2 (was 1)
```

A mini-deck copy with a real line break inserted in its first `NOTES` string: check a FAIL; `sync-notes.py --confirm` printed "repairing: entry 1 (line 299) has a real line break inside the string; use \n"; check a then passed.

### components.md spacing budget (re-measured 2026-10-02)

A scratch page held the template's own CSS and its Google Fonts link, and one slide per piece built from the markup in `components.md`. Heights were read with `getBoundingClientRect` after `document.fonts.ready` and a 500 ms wait. Poppins was confirmed loaded: its 400, 500, 600 and 700 faces reported `loaded`, `document.fonts.check` was true for each weight, and a 40px test string measured 1126px in Poppins, 1025px in `sans-serif` and 941px in `serif`. The same pieces were also measured with the font forced to `sans-serif`: that run reproduced the old table (chip 47, three cards 227, three stats 160, table 61 and 91, steps 149), which shows the old numbers came from a fallback font. Text pieces were fitted to an exact line count by adding words until the next word would wrap. One old row, "beats 333", could not be reproduced with the documented markup under either font (fallback 265 and 326, Poppins 274 and 349). The old "two cards, three-line `d`" figure of 263 equals the fallback height of two lines (three lines measured 299, and each line is 36); the new table states the line counts it measured.

### Guest component (2026-10-13)

A scratch copy of `templates/template.html` with a cover, five guest slides (`light`, `dark grad`, `lav` with `mark`, `dark grad`, `light` with `mark`; one-line and two-line names; text slots and real text) and a close, built once with no image files and once with a stand-in square image and a wordmark SVG. `render.sh` on each: `RESULT: ok`, 7 slides, 7 pages, match; check o PASS; the no-image copy warned j for the missing files, as intended. The CC14 example `index-guest.html` through `check-deck.py --layout`: a, b, c, e, f, g, h, k, l, m, n PASS; d FAIL and o WARN only for slides 7 to 10 (the faults kept on purpose); j WARN lists the two guest files and the two event photos. `render.sh --force` on it: 13 slides, 13 pages, match. The PDF pages were read back as images: the glow, the top alignment and both images print. Heights in `references/guest-slide.md` were read in Chrome with `document.fonts.check('600 96px Poppins')` true. The stage was also opened at 1280 by 800 in a browser and scaled to fit with the slide intact.

### Not yet tested

- Linux Chrome or Chromium (the `$CHROME` discovery paths are written but untested).
- A deck opened through a local web server; the checker reads files, not URLs.
- A person pressing `P` in a visible browser window, and the key navigation and presenter window in headless Chrome: that was simulated when the skill was written (a stub `window.open` and key events), and the template has not changed since, but it was not re-run on 2026-10-02.
- The markup blocks of `components.md` through `render.sh` as one deck: done when the page was written, not re-run after the spacing table changed.
