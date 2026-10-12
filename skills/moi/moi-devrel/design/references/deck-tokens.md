# The deck framework against this branch

Facts are as of 2026-10-03, read from `moi-webinar/deck/templates/template.html` and `../colors_and_type.css`, with the values below extracted by script on that date. The deck is built by `moi-webinar/deck`; this file only states where its tokens agree with this branch and where they differ. It does not rule on the differences. The brand book (see `colours.md`) is cited where it speaks. Back to `../GUIDE.md`.

## Use
1. A deck: start from `moi-webinar/deck/templates/template.html` and change only what was asked. The previous operator rejected a PPTX and a differently styled HTML deck for the intro session and asked for the session 8 look exactly (`moi-webinar/deck/references/rules.md`, rule 10).
2. Any other surface: use this branch's CSS. If you carry a deck component onto a page, convert its variables with the map below.

## Variable map
| Deck variable | This branch's token | Same value |
|---|---|---|
| `--moi-main`, `--moi-dark`, `--moi-white`, `--moi-grey`, `--moi-black` | the same names | Yes |
| `--bg-almost-lavender`, `--bg-certainly-lavender`, `--bg-pastel-purple` | the same names | Yes |
| `--lav-accent` `#BCA6FF` | `--fg-on-dark-accent` | Yes |
| `--ink-hi`, `--ink-mid`, `--ink-low` (`rgba(10,5,26,...)` at .85, .69, .55) | `--fg-1`, `--fg-2`, `--fg-3` | Yes |
| `--snow-hi`, `--snow-mid` (white at .85, .69) | `--fg-on-dark-1`, `--fg-on-dark-2` | Yes |
| `--snow-low` (white at .55) | none: the CSS third tier on dark is 30% (`--fg-on-dark-3`) and book page C6 shows 85, 69 and 30 | No |
| `--stage-bg` `#0A0026`, `--slide-bg` `#FCFBFF` | `--moi-black`, `--bg-almost-lavender` | Yes |

## Where they agree
- The five brand colours, the three light backgrounds and MOI Black as the dark ground, with the same hex values.
- Poppins at 400, 500, 600 and 700 only for the interface, loaded from Google Fonts. The deck loads it with a `<link>` in the page head, which works. The CSS in this branch used an `@import` that browsers ignored until it was moved (`type.md`).
- The chip: SemiBold, uppercase, 0.08em tracking, a pill with a Pastel Purple border.
- The logo gradients: the deck's inline `moiOnDark` runs `#DBCEF9` to white and `moiOnLight` runs `#320F99` to `#4B17E5`, the same stops as the logo files. The deck draws the logo as an inline `<symbol>`, so the black-SVG fault in `logos-and-mascot.md` cannot happen there.
- Slides alternate light, lavender and dark backgrounds, using the same hex values as the light and dark surfaces here.

## Where they differ
| Thing | Deck | This branch and the book |
|---|---|---|
| Slide title weight | `h2` at 600; `h1` at 700 | Headings Bold 700 only, subheadings SemiBold (book D2; CSS `h1` to `h3` are 700) |
| Body weight | `.sub` and card detail at 400; card value and table cells at 500 | Body Medium 500; Regular "if necessary" (book D2) |
| Tracking | -0.01em on `h1` and `h2`; -0.02em on `.stat .n`; -0.06em on `.ghost-num`; 0.06em on `.pill`; 0.08em on `.slide-num` | Tracking changes on over-line text only (book D3); the CSS sets 0 except `--tr-caps` |
| Heaviest weight | `.ghost-num` at 800 | Extra Bold is a weight not to use (book D1) |
| Monospace | `ui-monospace` stack in `.code`, `.mono`, `.step .c`, `.photo .ph` | Poppins only (book D1 "exclusively"); book silent on code. The deck calls code "the one non-Poppins surface" |
| Colours not in the CSS | `#14063F` (start of the dark gradient), `#9EE8C1` (code strings), `#DBCEF9` (logo gradient start; the CSS lavender scale has `#D9CEFA`), `rgba(10,5,26,.62)` (diagram colour), many white alphas (.05, .06, .09, .14, .25, .35, .42, .7, .8) | The CSS has none of these |
| Lettering on the pale logo | `#4B17E5` | `#320F99` in the logo files and the official PNG |
| Corner radii | 28 (cards, stats, beats, photos), 24 (code, table corners), 6 (`.mono`) | 8, 12, 20, 32, 48, 999; none of 28, 24, 6 |
| Shadows | none | Inner highlight and indigo outer shadows (house choice) |
| Leading | `h1` 1.08, `h2` 1.12 | Titles 1.1 to 1.3 (book D3); CSS headings 1.25 |
| Type sizes | Pixels on a 1920 x 1080 stage (112, 76, 36, 30, 24, 22 and so on) | The `--size-*` ramp in rem, 7 to 304 px; 112 and 76 are not on it |
| Easing | `cubic-bezier(.2,.7,.2,1)`, 0.7 s reveals | `cubic-bezier(0.22, 0.61, 0.36, 1)` |
| Font fallback | `sans-serif` | `Inter`, `system-ui` |
The blog's stylesheet is a third set (`--muted` at 62%, `--ink #0A051A`, `--bg #FCFBFF`): `moi-blog/references/assets.md`.

## What to do with the differences
Nothing in the deck is changed by this branch. Several differences break a rule in the book (the h2 weight, the tracking, the 800 weight, the lettering colour), and one is a stricter reading than the book (monospace). Whether the deck's choices are accepted, or the template should change, is not recorded. ASK: Rahul. If the template is changed, `moi-webinar/deck` owns the change and its checker (`check-deck.py`) and example deck must be re-run.
