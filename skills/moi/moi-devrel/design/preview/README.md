# Preview cards

36 small HTML files, one design rule or token each, plus `_card.css`, the shared frame. Open one in a browser to see it. Each loads `../colors_and_type.css`, so the cards need a network for Poppins 500, 600 and 700. Facts are as of 2026-10-03.

| Group | Cards |
|---|---|
| Colour | `colors-brand`, `colors-bg-light`, `colors-bg-dark`, `colors-status`, `gradients` |
| Type | `type-display`, `type-headings`, `type-body`, `type-caps`, `type-scale`, `type-usecase`, `type-settings`, `type-emphasis-light`, `type-emphasis-dark` |
| Logo and shape | `logo-lockup`, `logo-padded`, `logo-rules-do`, `logo-rules-dont`, `planetoid-usage`, `watermark-corner`, `mascot-pip`, `soft-star` |
| Layout and surface | `background-patterns`, `orb`, `hairline-dot`, `cards`, `radii`, `shadows`, `spacing-tokens` |
| Components | `buttons`, `buttons-dark`, `chips-pills`, `inputs`, `code-callout`, `motion` |
| Voice | `voice` |

## Changed from the previous operator's copy
- Logo files are swapped to the correct variant for each ground (the old cards had the pale and purple logos on the wrong grounds). The tiny lockup and the "switch placement" example use the derived `Planetoid` shape, as brand book A3 asks.
- `planetoid-usage` no longer uses `cosmic-purple.png` (a portrait, left out of this library); the mask demo is an inline SVG clip path over `space-deep.png`.
- Page labels now match the brand book: light backgrounds are C3, dark backgrounds C4, text on light C5, text on dark C6.
- Negative tracking on headings and display text is removed, because book page D3 allows tracking changes on over-line text only. `type-caps` no longer shows tracking on handles and addresses, and its sample address is `0x1234...abcd`.
- `type-emphasis-light` says the 55 percent Low Emphasis tier has no swatch in the book.
- The rocket in the "don't" line of `voice` is an HTML entity, so no emoji character sits in the file. Em dashes became hyphens.
- Claim-bearing copy replaced with placeholders (last section).

## What the cards are not
The cards show the previous operator's reading of the Figma file next to the book. The book covers logo, shapes, colour and type only (`../references/colours.md` lists the pages). Radii, shadows, spacing, motion, buttons, inputs and the mascot have no brand-book page: treat those cards as house choices.

The previous operator's cards carried product copy that no source in this library supports: a validator count, sample API code with a latency figure, "in real time" and "at machine speed" card lines, the contested positioning line, the Pip tagline and three headline lines from his README. They are now bracketed placeholders in `chips-pills`, `code-callout`, `hairline-dot`, `cards`, `mascot-pip` and `type-headings` (changed 2026-10-03). The `voice` card keeps one real example line, "You scope what each agent can touch.", which is the voice example in the website's `CONTENT.md` (`sarvalabs/MOI-Website`, `main`, read 2026-10-03). Do not reuse a line from any card without `moi-devrel/claim-check` and `../references/voice.md`.
