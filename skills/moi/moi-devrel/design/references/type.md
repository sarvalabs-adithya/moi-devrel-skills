# Type

Facts are as of 2026-10-03. "The book" is the 23-page brand PDF (see `colours.md`); page labels D1 to D4 are its own. Back to `../GUIDE.md`.

## The rule
Poppins, exclusively (book D1). Install the latest Poppins from Google Fonts. Use Regular 400, Medium 500, SemiBold 600 and Bold 700. The book lists Thin, Extra Light, Light, Extra Bold and Black as weights not to use.
The book says nothing about italic. The website's `CONTENT.md` ("Styling", on `main` of `sarvalabs/MOI-Website`, commit `5e91afa`, read 2026-10-03) says "no serif and no italic", and the previous operator's skill said the same. So no italic is a house rule, not a book rule. The blog sets figure captions as an italic line (`moi-blog/references/assets.md`), so the rule is not applied there. `<em>` and `<i>` render italic by default: set `font-style: normal` on them if you use them. `brand-check.py` flags `italic`, `<em>` and `<i>`.

## Weights by use (book D2)
| Use | Weight |
|---|---|
| Headings | Bold 700 only |
| Subheadings | SemiBold 600 |
| Body | Medium 500: "always set to medium" |
| Emphasis inside body | Bold 700 on the word |
| Anything else | Other weights such as Regular "may be used if necessary". Avoid weights lighter than Light on small screens |
Tokens: `--wt-regular`, `--wt-medium`, `--wt-semibold`, `--wt-bold`.

## Tracking and leading (book D3)
| Rule | Value |
|---|---|
| Tracking | "Do not change letter-spacing/tracking for any text except Over-line text". The book's example for over-line text is 10 percent. `--tr-caps` is 0.08em |
| Title and heading leading | 1.1x to 1.3x, most common 1.25x (`--lh-heading`) |
| Body leading | 1.5x to 1.75x, most common 1.5x (`--lh-body`). Small text may use 1.75x (`--lh-small`) |
| Long documents | Paragraph spacing of at least 1.25x |
| Line length | 50 to 75 characters |
| Wrapping | Narrow the box when words per line are very uneven over 2 or 3 lines. Avoid orphans and widows |
The CSS has one token below the book's title range: `--lh-tight` (1.00, used by `.t-display`). `--lh-snug` (1.10) is the edge of the range. The deck's h1 is 1.08. See `deck-tokens.md`.
Over-line text is the small uppercase label above a heading or inside a chip. The chip look is Poppins SemiBold or Bold, uppercase, 0.08em tracking (`.t-cap`). The Figma file used IBM Plex Mono and Akira Expanded as placeholders; do not use a mono face for this look.

## Sizes (book D4)
The book says typography comes "from a type scale rhythm that is equivalent to a pythagorean musical ratio" and suggests multiplying a base size by 1.333, 1.414, 1.5 or 2. It gives no sizes.
The CSS ramp is the previous operator's reading of the Figma file: 33 steps from 7 to 304 px, about 1.125 per step (computed: 304/7 to the power 1/32 is 1.125). `--size-16` is the base, written as rem because the page root is 10px. The deck does not use the ramp (112 px and 76 px are not on it). Choose from the ramp for pages.
| Use | Token | Size |
|---|---|---|
| h1 | `--size-83` | 83 px |
| h2 | `--size-58` | 58 px |
| h3 | `--size-41` | 41 px |
| h4 and subhead | `--size-29` | 29 px |
| h5 | `--size-23` | 23 px |
| Body | `--size-18` (`p`), `--size-16` (`body`) | 18 or 16 px |
| Caption | `--size-13` | 13 px |

## Loading the font
- `../colors_and_type.css` must keep its Google Fonts `@import` as the first rule. A browser ignores an `@import` that follows any other rule. In the previous operator's copy the `@import` came after the `@font-face` block, so Medium, SemiBold and Bold never loaded (checked in headless Chrome 2026-10-03: the stylesheet's first rule was the font-face block and the page listed only the 400 face). Body text that should be Medium rendered Regular, and bold was synthesised. Nothing raised an error. This copy is fixed.
- Poppins Regular is a file in `../fonts/`. The other three weights need a network. For offline work add the files and `@font-face` blocks (downloading is a gate).
- After building a page, list the weights that loaded: `document.fonts.ready.then(() => console.log([...new Set([...document.fonts].filter(f => f.status === "loaded").map(f => f.weight))].sort().join(",")))`. Each weight the page uses must appear. A weight no text uses stays unloaded and is absent, which is normal. Do not use `document.fonts.check("700 16px Poppins")`: on the previous operator's broken CSS, where only the 400 face existed, it returned true for 400, 500, 600 and 700 (headless Chrome, 2026-10-03), because the browser matches the nearest face it has. On the repaired CSS the same page printed `500,600,700`.
- On a machine without Poppins, text falls back to `Inter` or the system sans-serif and the layout measures differently. Measure on a machine where the check passes.
- `colors_and_type.css` sets `html { font-size: 10px }`, so 1rem is 10px for the whole page and also restyles `body`, `a`, `p`, `h1` to `h5`, `code` and `::selection`. Use it on stand-alone pages. For an existing app or site, copy the values you need into its own stylesheet instead. The website has the same root: its blog routes add a `blog-root` class that restores a 16px root, because without it "every rem value in the blog renders at 62.5% size" (`CONTENT.md`, same commit).

## Code in type
The book is silent. The website's `CONTENT.md` says the only exception to Poppins is code, "where a system monospace stack is used because code needs character alignment". The blog stylesheet does the same (`moi-blog/references/assets.md`), and the deck template calls code "the one non-Poppins surface, because code is content". The previous operator's CSS says code is Poppins Medium with tabular numbers. Three live surfaces against one file. For sample code on a branded page use a system monospace stack, and say so in the hand-back. ASK: Rahul to settle it.

## Not yet known
- Whether the sizes in the CSS ramp match the Figma file; the Figma file is not in this library and is not recorded (the previous DevRel's notes); ASK: Rahul.
- Whether italic is banned or only unused. ASK: Rahul.
- Where to get the three weights as files, and under what licence (`../fonts/README.md`). ASK: Rahul.
