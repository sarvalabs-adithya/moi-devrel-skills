---
name: moi-deck
description: Building or editing a MOI webinar, community call or session deck (the fixed 1920×1080 HTML deck with MOI brand tokens, a presenter window, a spoken script and a PDF export). Use when someone hands over raw material (meeting notes, a Slack dump, a report, dashboard screenshots, event photos) and wants slides, or when changing any deck under `<session>/deck/`.
---

> **Legacy: superseded.** Kept for reference. The deck workflow now lives in `skills/moi/moi-webinar/deck/` (`GUIDE.md`, `templates/template.html`). Do not install both, since they claim the same deck work.

# MOI decks

One HTML file is the whole deck: slides, CSS, speaker script and presenter window. A headless Chrome
print makes the PDF. No build step, no dependencies, no framework.

Hand this skill raw material and it returns a deck. The person handing over should not need to know
any of what follows.

## End to end

| # | Do | How |
| --- | --- | --- |
| 1 | Put the deck in its own folder | `<session>/deck/index.html`, e.g. `community-call-14/deck/` |
| 2 | Start from the template | `cp ~/.claude/skills/moi-deck/assets/template.html <session>/deck/index.html` |
| 3 | Write the slides | One `<section class="slide …">` each. Components: `reference/components.md` |
| 4 | Write the script | One entry per slide in the `NOTES` array, same order as the slides |
| 5 | Render | `scripts/render.sh <session>/deck/index.html [output.pdf]` (pass the PDF name when one already exists) |
| 6 | Verify | Read the PDF pages back and check the count. The script runs `node --check` for you |
| 7 | Hand back | Send the HTML and the PDF. Write `SCRIPT.md` beside the deck if a spoken script was asked for |

`reference/build.md` covers rendering, variants, photos, logos and every trap that has bitten before.
Read it before editing an existing deck.

## Slide vocabulary

Four backgrounds: `light`, `lav`, `dark grad`, and `dark`. Alternate them so no two neighbours match.
Inside a slide: a `chip` for the section label, an `h2` title with one `accent` span, a `sub` line,
then one of `cards`, `stats`, `cmp` table, `steps` or `photos`. Full markup in
`reference/components.md`.

House rules that matter more than the markup:

- **Every number comes from the person.** Never invent a figure, a date, an attendance count or an
  outcome. If a slide needs one and nobody supplied it, leave it off and say so on hand-back.
- **Photos are real files only.** No stand-in images on a slide that claims to show an event. Drop
  frames that read the filename until the file exists (`reference/build.md`).
- **The corner badge equals the page number.** Renumber every slide after any insert or delete.
- **Say what the source says.** If the hand-over is vague about who spoke or what happened, the slide
  stays vague too. Flag it rather than filling the gap.
- **One idea per slide.** Three cards, three stats, four at a push. If it needs more, it is two slides.

## Script

The `NOTES` array is the spoken script, one string per slide, shown in the presenter window on `P`.
Write it to be read aloud: short sentences, no bullet fragments, no stage directions except bracketed
cues such as `[If the host asks …]`.

Run the `humanizer` skill over the script before handing it back. It strips the tells that make a
script sound written rather than spoken.

Escaping matters: those strings are JavaScript. Newlines must be `\n`, never a real line break, or the
whole deck script dies silently and the presenter window and arrow keys stop working. The render
script checks this every time.

## Modules

| Doing | Read |
| --- | --- |
| Writing slides: every component with copy-paste markup, spacing budget, when to use which | `reference/components.md` |
| Rendering, verifying, deck variants, photos and brand logos, known traps | `reference/build.md` |
| Starting a brand new deck | `scripts/new-deck.sh <session-folder> "<Deck title>"` |
