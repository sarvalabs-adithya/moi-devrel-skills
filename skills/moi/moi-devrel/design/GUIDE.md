# moi-devrel/design: the MOI visual brand

Branch of `moi-devrel`. `$SKILLS`, the operator, `ASK:`, the house rules and the gates are in `moi-devrel/SKILL.md`; this guide adds what is specific.

## What this covers
The MOI brand for pages, mocks, share images, covers and one-off art: colour and type tokens (`colors_and_type.css`), Poppins, the logo files and which one sits on which ground, the planetoid shape, the mascot Pip, space backgrounds, a placeholder-copy UI kit, two starters and `brand-check.py`. It says which rules come from the 23-page brand book and which are the previous operator's own. Facts are as of 2026-10-03.
Not covered: decks (`moi-webinar/deck`, which has its own colour and type tokens; `references/deck-tokens.md` compares them); blog posts, covers in the blog repo and the newsletter (`moi-blog`, which owns the email image rules); docs pages (`moi-docs`); checking a claim (`moi-devrel/claim-check`); house wording (`moi-devrel/references/house-style.md`).

## Before you start
Design work has no repo of its own. Run every command from the working copy the operator is already in (a scratch folder outside any repo also works), with paths quoted: logo file names contain spaces. `<slug>` is a short lower-case name for the piece, for example `release-card`. `brand-<slug>/` sits at the root of that folder, or in a folder the operator names; step 2 makes it ignore itself so Git never picks a draft up by accident.
- [ ] What is being made, where it will be seen, its size, light or dark. The operator provides it. Ask: "What is it, where will it be seen, and at what size?"
- [ ] Who approves it. Rahul approves public pieces (`moi-devrel/references/people-and-teams.md`). ASK: Rahul if unsure.
- [ ] The words, or the fact that none exist yet. The operator provides them. Positioning is contested: do not supply a line yourself (`references/voice.md`).
- [ ] A browser with a network, python3, and Chrome for a PNG export. Opening a page makes the browser request Poppins 500 to 700 from Google Fonts (the UI kit also requests React from `unpkg.com`). That is a page load, not a saved download.
- [ ] Photos of people, with permission on record; partner logos (a download is a gate). Neither is in this folder.

## The run
Say "dark" or "light" for the ground, never for the colour of the logo.
| # | Step | What to do, and the command | Done when |
|---|---|---|---|
| 1 | Frame | Restate the thing in one line. A deck goes to `moi-webinar/deck`, a post, cover or email to `moi-blog` | The operator says yes |
| 2 | Set up | `mkdir -p brand-<slug>/assets/logos && printf '*\n' > brand-<slug>/.gitignore`, then `cp "$SKILLS/moi-devrel/design/colors_and_type.css" brand-<slug>/`, `cp -R "$SKILLS/moi-devrel/design/fonts" brand-<slug>/fonts`, `cp -R "$SKILLS/moi-devrel/design/assets/logos/SVG" brand-<slug>/assets/logos/SVG`. Add a mascot or PNG only if needed | The folder holds copies, so nothing points back into `moi-devrel/design` |
| 3 | Start | `cp "$SKILLS/moi-devrel/design/templates/page-starter.html" brand-<slug>/index.html`, or `card-1200x630.html` as `card.html` | The starter opens in a browser |
| 4 | Tokens and logo | Colours and weights from `references/colours.md` and `references/type.md`, only as `var(--token)`. Logo by ground from `references/logos-and-mascot.md` | No typed hex, one typeface, each logo chosen by its ground |
| 5 | Words | `references/voice.md`. Replace every `[bracket]`: `brand-check.py` fails a page that still has one. A figure needs a source and a date | `slop-lint.sh` is clean and `moi-devrel/claim-check` passed any claim |
| 6 | Build | Static HTML or SVG. Edit the starter in place. Name the path | A file on disk |
| 7 | Check | `python3 "$SKILLS/moi-devrel/design/scripts/brand-check.py" brand-<slug>/index.html`, then `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" brand-<slug>/index.html`, then `bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" brand-<slug>` | 0 FAIL, 0 lint errors, each WARN read |
| 8 | Look | Open the page at its final size and at phone width. In the browser console (Chrome: View, Developer, JavaScript Console; on macOS Cmd+Option+J) run `document.fonts.ready.then(() => console.log([...new Set([...document.fonts].filter(f => f.status === "loaded").map(f => f.weight))].sort().join(",")))`. Do not use `document.fonts.check`: it says true when a weight is missing. Check no logo is black or lost on its ground | Every weight the page uses (700 headings, 600 subheads, 500 body) is in the printed list, and the operator has seen the real output |
| 9 | Export | A PNG: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars --allow-file-access-from-files --virtual-time-budget=8000 --window-size=1200,630 --screenshot=brand-<slug>/card.png "file://$PWD/brand-<slug>/card.html"`. Linux: `google-chrome` or `chromium` | `file brand-<slug>/card.png` says 1200 x 630 and the headline looks like the Poppins Bold in `$SKILLS/moi-devrel/design/preview/type-display.html` |
| 10 | Ship (GATE) | Only on a yes that names the action: add to a repo, upload to Drive, Canva or Figma, post, send, hand to `moi-blog`, or draft the message that sends it (`moi-devrel/templates/messages.md`). The folder ignores itself, so copy the one finished file to where it belongs; do not delete the `.gitignore` to commit the whole folder | The destination has been opened after the action |
| 11 | Hand back | The format at the end | The operator has read it |

## Which file to read
| Doing | Read |
|---|---|
| A colour, a text tint, a background, a gradient | `references/colours.md` |
| Weights, sizes, tracking, loading Poppins, code in type | `references/type.md` |
| A logo, the tiny logo, the planetoid, Pip | `references/logos-and-mascot.md` |
| Backgrounds, shapes, spacing, motion, photos, icons, the kit | `references/layout-and-backgrounds.md` |
| Words on an image, positioning, vocabulary | `references/voice.md` |
| Carrying deck tokens onto a page, or comparing | `references/deck-tokens.md` |
| What each asset file is, what was left out | `assets/README.md` |
| The font licence and the weights | `fonts/README.md` |
| The cards, the UI kit | `preview/README.md`, `ui_kits/marketing/README.md` |
| What changed from the previous operator's folder | `references/provenance.md` |
| Testing a change to this branch | `evals/evals.md` |

## Facts that fail silently
| Rule | The incident |
|---|---|
| The word in a logo file name is the ground. `Dark` is the pale logo for dark grounds, `Light` the purple logo for light grounds | The old README said the reverse. A pale mark shipped as the newsletter logo and was replaced on 2026-08-24. The previous operator asked on 2026-08-17 and 2026-09-15 that the logo never render black on light |
| Use `assets/logos/SVG/`, never `SVG-as-received/`. A copy from the website folder may be black or have its gradient reversed | The exported SVGs lost their style block and render solid black. Seven of eight in the website repo are the same (2026-10-02) |
| Keep the `@import` as the first rule of the CSS | The old CSS had it second, so Medium, SemiBold and Bold never loaded and nothing errored (found 2026-10-03) |
| Read the loaded weights from `document.fonts` (step 8), never `document.fonts.check`. Export with `--virtual-time-budget` | `check("700 16px Poppins")` returned true on the previous operator's CSS when only weight 400 had loaded (headless Chrome, 2026-10-03). A card exported without the budget once rendered its headline in a fallback face (2026-10-03); a second run the same day did not, so it depends on how fast the font request is |
| `colors_and_type.css` makes 1rem equal 10px for the whole page | Pasted into an existing app it shrinks every rem. The blog needed a `blog-root` class for the same reason. Copy token values instead |
| On a dark ground a small label is `#BCA6FF`. `.t-cap` is MOI Main, contrast 2.5 to 1 on MOI Black | Found in the starter on 2026-10-03. The accent on dark is 9.6 to 1 |
| Do not invent a hue. A typed hex is a flag | The old README: "don't invent new hues". The list of existing exceptions is in `references/colours.md` |
| Positioning is contested and none is chosen: use the lines in `terminology.md` table D, and the unclassified ones listed in `references/voice.md`, only as the operator picks. The kit and old README lines are not approved | `terminology.md` Contested 2. Figures and partner claims in the old kit had no source |
| `backgrounds/cosmic-purple.png` is a portrait of a person. It is not in this folder | It is in the website repo's brand folder too. A photo of a person needs permission on record (CC14, 2026-09) |
| No tiny-logo file exists. Build it from `Planetoid` plus the word MOI, and ask for the official files | The old README said they ship with the system. They do not |
| Email images are PNG, never replaced in place under the same name | Mailchimp caches by URL (2026-08-24). Rules: `moi-blog/references/assets.md` |
| A release post carries no picture unless the approver says otherwise. ASK: Rahul before making art for one | August 2026 decision, `moi-blog/references/assets.md` |

## Gates
The gates in `moi-devrel/SKILL.md` apply. These are specific to this branch, and none happens without the operator's explicit yes in this conversation:
- Pushing a branch or opening a PR with brand files, or editing `public/brand/` in `sarvalabs/MOI-Website` (a merge there deploys). A push to `moi-foundation/MOI-Webinars` publishes.
- Uploading or sharing a file in Drive, Canva or Figma. Sending, posting or scheduling anything that carries the art.
- Downloading a file: the other Poppins weights, a partner logo, a photo. Say the name, source and size first.
- Using a photo of an identifiable person, or Pip on a public asset (approval unknown, `references/logos-and-mascot.md`).
- Changing a logo file, the palette or the CSS tokens in this branch. Who owns the brand is not recorded (ASK: Rahul); change nothing until he says.
- Image generation is a paid API: the operator names it, with the count and model stated first.

## Keys and access
None needed to build or check. Names only: the brand book PDF (`MOI Brand Guidelines.pdf`) and the logo pack (`MOI Logos.zip`) are in this skill, under `assets/brand-book/`. The "Logo Files" link on the book's page A1 and the Figma file `MOI Protocol.fig` are in neither; which Figma account holds the file is not recorded (the previous DevRel's notes), and Rahul is the brand's owner to ask (ASK: Rahul). Shipping uses accounts listed in `moi-devrel/references/keys-and-access.md` (Buffer, Mailchimp, Drive, Canva, and its Figma row). Google Fonts needs none.

## Hand-back
```
Produced: <files with exact paths, and the PNG if exported>
Checked: brand-check <0 FAIL or list>, slop-lint <errors>, fonts loaded <weights>, looked at <sizes>
Open: <unverified copy, ASK lines, photos without permission, contested positioning>
Not verified: <logo-on-ground by eye, contrast, anything simulated>
Ready: yes or no, because <one reason>
```
A status lists work that was done. Planned work is labelled as a to-do.
