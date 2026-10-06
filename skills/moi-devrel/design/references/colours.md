# Colours

Facts are as of 2026-10-03. "The book" is the 23-page PDF "Brand Guidelines for MOI Ecosystem" in the previous operator's old design skill folder; it was read page by page on 2026-10-03 and is not in this library (ASK: Adithya for a copy). The A, B and D pages print their labels; the colour pages print none, so C1 to C6 are counted from the book's contents page (Brand Colours, Brand Gradients, Backgrounds Light, Backgrounds Dark, Typography Light, Typography Dark). The PDF's own creation date is 2023-03-31 (file metadata, read 2026-10-03). Tokens named `--like-this` are in `../colors_and_type.css`. Back to `../GUIDE.md`.

## Source order
1. The book is authoritative for colour, type and logo. The previous operator's README said so; the pages bear it out.
2. `../colors_and_type.css` holds the book's values plus tokens the previous operator took from the Figma file.
3. Surfaces built from these (the deck, the blog, the website) are derived. `deck-tokens.md` compares the deck.
4. Where a value is on no book page it is a house choice. The last table lists them.
Who settles a conflict between the book and a live surface is not recorded. ASK: Rahul.

## The five brand colours (book C1, C4)
| Name | Token | Screen hex | RGB | Print hex | CMYK |
|---|---|---|---|---|---|
| MOI Main | `--moi-main` | `#4B17E5` | 75 23 229 | `#3E308C` | 93 100 0 0 |
| MOI Dark | `--moi-dark` | `#320F99` | 50 15 153 | `#221460` | 95 100 0 40 |
| MOI White | `--moi-white` | `#FFFFFF` | 255 255 255 | `#FFFFFF` | 0 0 0 0 |
| MOI Grey | `--moi-grey` | `#BFBFBF` | 191 191 191 | `#BFBFBF` | 25 20 20 0 |
| MOI Black | `--moi-black` | `#0A0026` | 10 0 38 | `#0A0026` | 86 84 51 71 |
The book: the brand "represents itself visually by contrasting white against purple" and the colours are to be used "exactly as prescribed". For digital work use the screen colours. MOI Main "does not translate directly to paper", so print uses the CMYK or the alternative hex.

## Gradients (book C2)
| Name | Runs | Token |
|---|---|---|
| Purple Gradient | MOI Dark to MOI Main (`#320F99` to `#4B17E5`) | `--grad-purple`, top to bottom |
| White Gradient | MOI Grey to MOI White (`#BFBFBF` to `#FFFFFF`) | `--grad-white` |
The book gives no direction for a gradient. Its rule of thumb: eyes follow a gradient from dark to light, so use the axis to steer the eye. `--grad-cosmos` (Black to Dark), `--grad-lavender` (Certainly Lavender to Pastel Purple) and `--grad-orb` are the previous operator's, not the book's.

## Backgrounds
The book: four light backgrounds and only one dark background.
| Surface | Token | Hex | Book |
|---|---|---|---|
| Pure White | `--bg-pure-white` | `#FFFFFF` | C3 |
| Almost Lavender | `--bg-almost-lavender` | `#FCFBFF` | C3 |
| Certainly Lavender | `--bg-certainly-lavender` | `#F5F2FF` | C3 |
| Pastel Purple | `--bg-pastel-purple` | `#D9CCFF` | C3 |
| MOI Black (the only dark) | `--moi-black` | `#0A0026` | C4 |
The C3 swatch for Pure White prints the hex of MOI Main by mistake; its RGB and print hex say white.
Layers on dark: "boxes of white set to opacities between 3-15%". C4 shows steps of white at 0, 5, 7, 8.25, 9.75, 11 and 13 percent. Do not add a second dark colour.

## Text colours (book C5 on light, C6 on dark)
| Tier | On light | On dark | Use (book) |
|---|---|---|---|
| Accent | `#4B17E5` at 96% (`--fg-accent`) | `#BCA6FF` at 96% (`--fg-on-dark-accent`) | Headings and other high-visibility text |
| High Emphasis | `#0A051A` at 85% (`--fg-1`) | white at 85% | Text that needs to stand out |
| Medium Emphasis | `#0A051A` at 69% (`--fg-2`) | white at 69% | Slightly more prominent than body, less than high |
| Low Emphasis | described, no swatch on the page | not shown | De-emphasised or supplementary text |
| Disabled | `#0A051A` at 30% (`--fg-mute`) | white at 30% | Inactive elements |
| Pure | `#0A0026` | `#FFFFFF` | Marked "Not recommended" |
The text base `#0A051A` is not MOI Black `#0A0026`. Do not use either at full strength for text.
The CSS also has a 55% Low Emphasis tier (`--fg-3`). The book describes Low Emphasis but shows no value for it, so 55% is the previous operator's value. The deck uses it too.

## Used in this library but on no book page
| Value | Where | What is known |
|---|---|---|
| `--main-*`, `--lav-*`, `--tint-*` scales | CSS | The old CSS says they came from Figma. Not checked here |
| `#E20FBF`, `#009EF7` (`--signal-*`) | CSS, "used rarely" | Source not recorded |
| `#1FAE6B`, `#F2A742`, `#E2336B` (`--status-*`) | CSS, preview | Source not recorded |
| `#9871F2` | Orbs in the UI kit and cards. A token holds the same RGB only inside `--shadow-glow-soft` | Not a hex token |
| `#E2E2E2` (`--border`) | CSS | Source not recorded |
| `#14063F`, `#9EE8C1` | The deck template (gradient start, code strings) | Not in the CSS |
| `rgba(10,5,26,.62)` | The blog's muted text, per `moi-blog/references/assets.md` | A third value between the book's 69% and the CSS's 55% |
| `#15102B` (text) and `#5B5570` (muted) | The website's `CONTENT.md` "Styling", which also says "Do not introduce new hues". The blog stylesheet uses `#0A051A` and 62% per `moi-blog/references/assets.md`, so the document and the stylesheet disagree | Neither is on a book page |
| `#4DDB97` (mint), `#0A0526` (dark text) | The previous operator's own spec of 2026-05-29 in the research notes | `#0A0526` differs from the book's `#0A051A` by one digit. Treat as a typo until Rahul says otherwise |
The old README said "do not invent new hues". These are the exceptions that already exist. Do not add another.

## Rules for use
1. Reach for a token. A hex typed into a page is a review flag; `scripts/brand-check.py` lists them.
2. White against purple is the identity. Dark purple text on lavender, white on purple, pale lavender on MOI Black.
3. Accent on a light surface is MOI Main. On a dark surface the book gives `#BCA6FF` (C6).
4. A pale logo on white nearly disappears, and a purple logo on MOI Black is hard to see. See `logos-and-mascot.md` for which file goes where.
5. Feedback given repeatedly on the website redesign, 2026-05-29 to 2026-06-02: keep screens clean and uncongested, and make text contrast with its background. Check every page at its final size on its real ground.
6. The website's `DESIGN_SYSTEM.md` and `CLAUDE.md` still describe an older cream and serif look (`#F5F3EE`, Instrument Serif). The live brand is Poppins, `#4B17E5` and `#FCFBFF` (research note on the web products, 2026-10-02). Do not copy from those two files.

## Not yet known
- Who owns the palette and approves a new tint. ASK: Rahul.
- Where the 55% tier, the status colours and the signal colours came from. ASK: Adithya.
- Whether the book has a newer edition than the 23-page one read here, which the file metadata dates 2023-03-31. ASK: Rahul.
