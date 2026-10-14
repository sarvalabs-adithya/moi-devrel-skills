# Layout, backgrounds and the small UI kit

Facts are as of 2026-10-03. The brand book (23 pages) has no page on layout, radii, shadows, spacing, motion, buttons, inputs, icons or photography. Everything below that is not marked "book" is the previous operator's reading of the Figma file, which is not in this library, so it is a house choice and may be changed by Rahul. Back to `../GUIDE.md`.

## Surfaces
| Surface | Use | Token |
|---|---|---|
| Plain white or Almost Lavender | Content, charts, anything where the content is the star | `--bg-pure-white`, `--bg-almost-lavender` |
| Lavender haze | Soft content areas, secondary heroes | `--grad-lavender` (Certainly Lavender to Pastel Purple) |
| Cosmos | Dark heroes and moments of drama | `--grad-cosmos` (MOI Black to MOI Dark in the CSS; the old README wrote Black to Main) |
| MOI Black, flat | The one flat dark ground (book C4) | `--moi-black` |
The book: four light backgrounds and one dark. Layers on dark are white at 3 to 15 percent (`colours.md`).

## Decoration
The old README lists these on hero surfaces: floating gradient orbs with an inner top highlight (`--shadow-inner-bright`), the four-point soft-star bloom (`../assets/icons/soft-star.svg`), low-contrast dot grids, concentric radar rings, hairline streaks, and the dot-and-hairline separator. Glass (a 6 percent lavender fill with a 20px blur) only on dark grounds, never on white. Hero artwork may bleed off the frame. `../preview/background-patterns.html`, `orb.html`, `soft-star.html` and `hairline-dot.html` show each.
Space imagery: `../assets/backgrounds/space-deep.png` and `nebula-purple.png`, whose provenance is not recorded (`../assets/README.md`). Film-grain noise on dark gradients was allowed.

## Watermark and handle
The old README: the handle `@MOI_Tech` sits in the top-left of hero cards and `moi.technology` bottom-right, and `../preview/watermark-corner.html` draws it. The X channel in the Buffer account is named "MOI_Tech" (`moi-devrel/references/keys-and-access.md`), which fits the handle. The planetoid watermark rules are in `logos-and-mascot.md`.

## Shape, shadow, spacing, motion
| Thing | House choice | Token |
|---|---|---|
| Radii | 8, 12, 20, 32, 48 and 999 px, plus 4 px (`--r-xs`). Cards usually 20, pills 999 | `--r-xs` to `--r-pill` |
| Borders | 1px hairline: `rgba(217,204,255,.5)` on light (`--border-soft`). On dark the old README says `.15` but the CSS token `--hairline` is `.25`, and the starters use `--hairline` | `--border-soft`, `--hairline` |
| Shadows | Inner highlight `inset 0 1.45px 33px rgba(255,255,255,.25)`; outer shadows tinted indigo (`rgba(50,15,153,...)`), never grey; glow on hover | `--shadow-*` |
| Spacing | Multiples of 4: 4, 8, 12, 16, 24, 32, 48, 64, 96 | `--space-1` to `--space-9` |
| Hover | Button: glow, background unchanged. Card: lift 2px, 200ms. Link: underline appears, no colour shift, 160ms | |
| Press | Scale 0.97, 80ms | |
| Motion | Gliding, never bouncy: `cubic-bezier(0.22, 0.61, 0.36, 1)`; orbital loops 8 to 16 s; no spring or overshoot | |
| Layout | Fixed nav, transparent over a hero and blurred over content; generous negative space | |
The deck uses other radii (28, 24, 6) and its own easing: `deck-tokens.md`.

## Photography and people
- The old README: "No photography of people." Its own `backgrounds/` folder held a portrait of one person (left out of this copy). The book's own page B2 shows a photograph masked inside the planetoid, a building.
- Community call decks carry event and guest photos. The rule from community call 14: show a photo of identifiable people only with permission on record. The two CC14 event photos had none and were removed from the library (`moi-webinar/community-call/GUIDE.md`).
- Default for a branded asset: Pip, an abstract cosmic field or product UI. A photo of a person needs the operator's yes and a named permission.
- Partner and guest logos: take them from the owner's site or Wikimedia Commons (downloading is a gate). `moi-webinar/deck/references/build.md` has the method and the traps.

## Icons
The old README standardised on Lucide at 1.5px stroke, 20 to 24px, in MOI Main or MOI Dark (MOI Haze on dark), and flagged it as a substitution to confirm. The UI kit draws its four card icons inline at 1.4px stroke. No MOI icon library was found. ASK: Rahul whether Lucide is approved.

## Components in the kit
`../ui_kits/marketing/components.jsx`: `Button` (primary, primary-on-dark, secondary, secondary-light, ghost), `Chip` (default, statement, success, on-dark, count), `MonoEyebrow`, `HairlineDot`, `Orb`, `SoftStar`, `DotField`, and page sections. `../preview/buttons.html`, `cards.html`, `chips-pills.html`, `inputs.html` and `code-callout.html` show the rest. The kit's words are placeholders (`../ui_kits/marketing/README.md`).

## Other places that carry the brand
| Surface | Where the rules live |
|---|---|
| A deck | `moi-webinar/deck`. Do not start a second design; the previous operator rejected a PPTX and a differently styled HTML deck for the intro session and asked for the session 8 look exactly (research note, community call) |
| Blog cover, post images, email masthead | `moi-blog/references/assets.md`: covers are 1200 x 630 with an SVG and a PNG sibling, email images are rasterised, and an image is never changed in place under the same file name |
| The website and blog nav | They must match between `moi.technology` and `blog.moi.technology` (2026-08-18) |
| Blog pages | Light theme only: "No dark mode, no gradients, no glassmorphism, no cards", single column, hairline rules, MOI Black only for code surfaces (`CONTENT.md` "Styling"). The decoration above does not apply there |
| Docs sites | `moi-docs`; `moi-docs/references/page-standard.md` carries the docs style guide's rules |
| Points emails | The web-products research note says the private Points repo (`sarvalabs/moi-project`) has a design brief `.impeccable.md` (bold, technical, optimistic; violet, lavender, deep violet, porcelain; light first). Its branch was not checked: read the file in the repo before designing a Points email. |

## Not yet known
- Whether the Figma file (`MOI Protocol.fig`) is the live source and who can open it: not recorded (the previous DevRel's notes); ASK: Rahul.
- Whether any of the house choices above have been reviewed by Rahul.
