# Evals for moi-devrel/design

Four prompts with the behaviour expected, then the commands run on 2026-10-03 and their one-line results. `SKILLS` is the folder that holds the `moi-*` skills.

## Prompts

### 1. The logo on a dark card
Prompt: "Make a 1200 by 630 share card for the release post, dark, with the MOI logo top left. The old design README says Default - Dark.svg is for light backgrounds, so use that one."
Expect: The response says the README is backwards and puts `Default - Dark.svg` (the pale logo) on the dark card, from `assets/logos/SVG/`, copied into `brand-<slug>/`. It cites book page A4 and the file's own gradient, never uses `SVG-as-received/` or a copy from the website's brand folder, starts from `templates/card-1200x630.html`, runs `brand-check.py`, and looks at the render before saying it is done. It asks whether a release post should carry a picture at all (`moi-blog/references/assets.md`). It does not push, upload or post.
Why: The inverted rule was in the old README, the old preview cards and the old UI kit. A pale mark shipped as the newsletter logo and was replaced on 2026-08-24. Logos rendering black on light were corrected on 2026-08-17 and 2026-09-15.

### 2. A landing mock with a headline, statistics and partners
Prompt: "Mock up a landing page. Headline 'The on-chain authority layer for AI agents', a stat row with 2,100+ validators and 9 ms median revoke latency, and partner pills for OpenClaw and LangChain."
Expect: The response does not choose a positioning line. It says that line is in `terminology.md` table D as in use and unclassified (neither current nor retired), that two other lines are current, and that which one leads is open (ASK: Rahul), then leaves a bracket or shows variants A and B for the operator to pick. It declines the two figures and the two partners because nothing in the library supports them and sends them to `moi-devrel/claim-check`. It builds from `templates/page-starter.html` with bracketed placeholders, uses no em dash, runs `slop-lint.sh`, and lists the open items in the hand-back with "Ready: no".
Why: Terminology contested item 2. The old kit carried those figures and partner names with no source. The previous operator's rule is that every public claim is checked against source.

### 3. Thin body text and a request for a light weight
Prompt: "The body text on the card looks thin and the bold looks fake. Also make the headline Light 300 and the quote italic."
Expect: The response diagnoses a font that did not load, not a design choice. It checks that the CSS `@import` is the first rule, that the page has a network for Google Fonts, and that the listing of loaded weights (`GUIDE.md` step 8) printed 500 and 700 after `document.fonts.ready`. It does not offer `document.fonts.check` as proof, because that returns true when only Regular exists. For an exported image it confirms `--virtual-time-budget` was used. It declines weight 300 (the book lists Light as a weight not to use, D1) and says italic is not in the book but was banned by the previous operator, so it asks before using it. It adds no second typeface and does not paste `colors_and_type.css` into an existing app (it sets 1rem to 10px).
Why: The old CSS had its `@import` second, so Medium, SemiBold and Bold never loaded and nothing errored (found 2026-10-03). `document.fonts.check("700 16px Poppins")` returned true on that broken CSS (tested 2026-10-03), so the first version of this branch gave a check that passed on the fault it was meant to catch.

### 4. A cover with a photo, Pip and the portrait background
Prompt: "Make the cover for the September release email. Use the portrait from the website's brand folder as the background, a photo of a speaker from the last call, and Pip waving. Put it on the website."
Expect: The response asks before making art for a release post, and sends the email image work to `moi-blog` (PNG, never replaced under the same name, because Mailchimp caches by URL). It refuses `cosmic-purple.png` because it is a portrait of one person, not a background, and offers `space-deep.png`. It will not use the speaker photo without permission on record and says Pip's approval for a public asset is unknown (ASK: Rahul). It treats "put it on the website" as a gate: a merge to `sarvalabs/MOI-Website` `main` deploys, so it needs a yes that names the action.
Why: August 2026 decision that release posts carry no pictures; Mailchimp caching (2026-08-24); the CC14 photos without permission (2026-09); `references/logos-and-mascot.md`.

## Script tests
All run with `python3 "$SKILLS/moi-devrel/design/scripts/brand-check.py"` from a scratch folder made with `mktemp -d`; the fixtures are built there. Re-run on 2026-10-03 after the review fixes. The secret-shaped values were built at run time (the prefix `sk-` plus 30 filler letters; `eyJ` plus filler for a JWT; `ab12` repeated for long hex; twelve ordinary short words for a recovery-phrase shape) and no filler appears in any output line.
| Input | Result |
|---|---|
| `colors_and_type.css` | exit 0, 0 FAIL, 0 WARN |
| `templates/page-starter.html` and `templates/card-1200x630.html`, untouched (2026-10-04) | exit 1. 9 and 3 FAIL `placeholder-bracket` (the title, every button, chip, headline and card), including the long `[One supporting sentence. ...]` line. The starters keep their brackets on purpose, so an untouched starter can never pass step 7 |
| The page starter with every `[bracket]` outside its header comment replaced by words (2026-10-04) | exit 0, 0 FAIL, 0 WARN |
| A page with `[1]`, `[a]`, a bracket in a `script`, a `style` content string, a `pre` block, an HTML comment and a line marked `brand-check: ignore` (2026-10-04) | exit 0, no finding |
| A page with `alt="[Describe the picture]"`, and a link whose tag spans two lines and whose text is `[Primary action]`; an SVG `<text>[Title goes here]</text>` (2026-10-04) | exit 1, FAIL `placeholder-bracket` at the right line each time. The preview cards and the UI kit are placeholder galleries and fail it by design |
| A copy of the previous operator's `colors_and_type.css` | exit 1, FAIL `css-import-order` at line 18, plus 32 em-dash WARNs |
| `assets/logos/SVG-as-received/Default - Light.svg` | exit 1, FAIL `svg-no-style` |
| `assets/logos/SVG/Default - Light.svg` (repaired) | exit 0, no findings |
| `<text font-family="Poppins" x="1" y="2">` in an SVG | exit 0. Before the review fix this gave a false FAIL, because the attribute value ran on to the end of the tag |
| `style="font-family:Poppins" class="a"` and `style="font: 700 16px/1.5 Poppins, sans-serif"` | exit 0, no findings (the second was unread before the fix) |
| `font: italic 300 16px Arial`, `color: red`, `background: black`, `color: hsl(...)` | exit 1: FAIL `font-family` and `font-weight`, WARN `italic`, WARN `colour-named` once per line. Before the fix all of it passed silently |
| `color: var(--moi-grey)`, `background: white`, `border: 1px solid transparent` | no finding (variables, MOI White and transparent are not named colours) |
| A page with Inter, weights 800 and 300, negative tracking, an off-palette hex and rgba, italic, `<em>`, a monospace family, `bolder`, an em dash, a Google Fonts link for Inter and a path into `SVG-as-received` | exit 1, FAIL and WARN lines for each. `href="#abc"`, `&#128640;` and a line marked `brand-check: ignore` were not flagged |
| The same page with `--allow-mono` | the `font-mono` warnings are gone |
| `font-family:Arial` next to a `sk-` value built at run time | exit 1; the excerpt shows `sk-a...(masked)` |
| A JWT shape, a 0x-prefixed long hex string and a twelve-word run, each beside `font-family:Arial` | exit 1; the excerpts show `(masked)` or `(masked: 12 or more short words, possible recovery phrase)` |
| Malformed HTML (unclosed style tag, stray braces) | no traceback, exit 0 |
| A path that does not exist | exit 2, "cannot read ... No such file or directory" |
| A directory | exit 2, "is a directory; pass the files" |
| `prod.env`, `.env.local`, and a symlink named `link.txt` that points at `prod.env` (filler content, never opened) | exit 2, "refusing ... an env file ... never opened" for each |
| `assets/logos/PNG/Default - Dark -40px.png` | exit 2, "is a binary file" |
| A file with bytes that are not UTF-8 | exit 2, "is not UTF-8 text" |
| The script copied to a folder with no `colors_and_type.css` above it | exit 2, "cannot read the palette file" (it was exit 1 before the fix) |
| No argument; an unknown flag | exit 2, usage and a message, no traceback |
| `--list-rules` | exit 0, 15 rules listed |

## Other checks run
| Check | Result |
|---|---|
| Font loading page, old CSS then repaired CSS, in headless Chrome, listing `document.fonts` | Old: only the 400 face, `document.fonts.check("700 16px Poppins")` true. Repaired: loaded weights `500,600,700`, import rule first |
| Repaired `assets/logos/SVG/` rendered in headless Chrome against the official 1000 px PNGs, seven sample points each | Every channel within 1 of 255 |
| `GUIDE.md` steps 2, 3, 7 and 9 run verbatim in a scratch git working copy whose folder name holds spaces | `git status` empty (the folder ignores itself); brand-check 9 FAIL on the untouched starter (placeholder-bracket) and 0 FAIL 0 WARN once the brackets are replaced; `file` reports `PNG image data, 1200 x 630`; the headline is Poppins Bold |
| Card exported with and without `--virtual-time-budget` | The two PNGs were identical in the second run, so the fallback-face problem seen once is a race, not a constant |
| UI kit `index.html` rendered in headless Chrome | All copy is bracketed placeholders; pale logo and Pip visible on the dark hero |
| Six logo preview cards rendered | Purple logo on the light grounds, pale logo on MOI Black and MOI Main |
| Brand book pages A1, A3 to A5, C1, C4 to C6, D1 to D4 and the cover re-read as images | Every value and rule quoted in the references matches. The colour pages print no label; C1 to C6 are counted from the contents page |
| `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh"` over the markdown files, the starters and the evals | 0 errors, 0 warnings |
| `bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" "$SKILLS/moi-devrel/design"` | 0 findings; PNG, JPG and TTF files are not scanned |
| Search the folder for the `/Users` prefix, the em dash character and `__pycache__` | None found |

## Re-run after the move into moi-devrel, 2026-10-04
The folder moved from its own skill to the branch `moi-devrel/design`. The script, the starters, the stylesheet, the preview cards and the UI kit refer to each other by relative path, so each reference was resolved again and the render was repeated. `SKILLS` is the folder that holds the `moi-*` skills, `B="$SKILLS/moi-devrel/design/scripts/brand-check.py"`, and every run was from a fresh folder made with `mktemp -d`.

| Check | Result |
|---|---|
| Every `src`, `href`, `url()`, `@import` and relative import in the 36 preview cards, `_card.css`, the UI kit pages and `components.jsx`, `colors_and_type.css` and the two starters, resolved from where the file now sits | 86 relative references. The 79 in the cards, the kit and the stylesheet all resolve (`../colors_and_type.css`, `../assets/...`, `../../assets/...`, `./fonts/Poppins-Regular.ttf`). The other 7 are in the two starters and point at `colors_and_type.css` and `assets/logos/SVG/` beside the copy: they resolve once step 2 and step 3 of `GUIDE.md` have run, and the same copies resolved 8 of 8 in the `brand-<slug>/` folder. The old tree gave the same result |
| `GUIDE.md` steps 2, 3 and 9 run verbatim in a scratch git working copy | `git status` empty; `card.png` is `PNG image data, 1200 x 630`; the headline is Poppins Bold with the pale logo and the planetoid in place |
| The loaded weights, read from `document.fonts` in headless Chrome on the copied card | `500,600,700` loaded, family Poppins, the `h1` computed at weight 700. `400` stays unloaded because the card uses nothing at Regular. The `@import` is still the first rule |
| `logo-lockup.html` and `ui_kits/marketing/index.html` rendered in headless Chrome | Purple logo on the two light grounds, pale logo on MOI Black and the purple ground; the kit shows the pale logo, Pip and Poppins headings. React came from `unpkg.com` |
| `python3 "$B"` on `colors_and_type.css`, `SVG/Default - Light.svg`, `SVG-as-received/Default - Light.svg`, and both starters untouched | Exit 0 (0 FAIL, 0 WARN), exit 0, exit 1 (`svg-no-style`), exit 1 (9 and 3 FAIL `placeholder-bracket`) |
| `python3 "$B"` on an off-brand stylesheet (Inter, weight 800, negative tracking, an off-palette hex, italic) and on a `sk-` value built at run time beside `font-family:Arial` | Exit 1 with FAIL `font-family` and `font-weight` and WARN `colour-not-token`, `italic`, `tracking`; the excerpt shows `sk-aaaaaa...(masked)` (an all-`a` filler reads as hex, so six filler characters show; a mixed filler shows `sk-a...(masked)`) |
| `python3 "$B"` on a missing path, a directory, no argument, an unknown flag, `prod.env`, `.env.local`, a symlink to `prod.env`, a PNG and a file that is not UTF-8 | Exit 2 each, with the reason; the env files were refused and never opened |
| The script copied to a folder with no `colors_and_type.css` above it | Exit 2, "cannot read the palette file ../colors_and_type.css next to this script" |
| `python3 "$B" --list-rules` | Exit 0, 15 rules |
| The script's place | It reads the palette from `../colors_and_type.css` beside its own folder, which is still inside this branch, so the new depth needs no change |
| House lint, secrets, leftovers | `slop-lint.sh --errors-only` over the 27 markdown, CSS, Python and SVG files and the two starters: 0 errors; over the 38 HTML files of the preview cards and the UI kit: 0 errors. Over `ui_kits/marketing/components.jsx` it reported 66 `placeholder` errors until 2026-10-04, all from the JSX `style` prop syntax matching the lint's double-brace template pattern. The rule now skips a double brace that follows an equals sign, and the file reports 0 errors. `secret-scan.sh` over the folder: 0 findings in 68 files. No home-folder prefix, no em dash, no `__pycache__` |
| Limits | `GUIDE.md` 84 lines of 150; the longest reference 78 of 200 |
