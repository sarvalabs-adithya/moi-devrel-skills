# Logos, the planetoid and Pip

Facts are as of 2026-10-03. "The book" is the 23-page brand PDF (see `colours.md`); page labels A1 to A5 and B1 to B2 are its own. File names have spaces: quote them in a shell and keep the exact case. Back to `../GUIDE.md`.

## What the logo is (book A1, A2)
The logo is the MOI shape (the planetoid) with the letters MOI inside it. It exists in two versions, one for light backgrounds and one for dark. Smallest size 24 x 20 px; scale in whole-number ratios on screen (72 x 60, 120 x 100). For print it scales freely with proportions kept. The book says the logo files are in JPEG, PNG, SVG and Ai formats behind a "Logo Files" link; this library holds PNG, JPG and SVG only. ASK: Rahul for the Ai files and who owns the link.
The wordmark MOI is never used by itself.

## Which file goes where
**The word in the file name is the ground, not the colour.** `Dark` = pale lavender planet, dark purple MOI, for dark grounds. `Light` = purple planet, white MOI, for light grounds. The book's A4 says "use the dark version of the logo for low-light backgrounds" and "the light version for light coloured backgrounds". The previous operator's README and cards said the reverse. Confirmed by the pixels of the PNGs on 2026-10-03 and by `moi-blog/references/assets.md`.
| Ground | File in `../assets/logos/SVG/` or `PNG/` |
|---|---|
| White, Almost Lavender, Certainly Lavender, Pastel Purple | `Default - Light` (purple) |
| MOI Black, the cosmos gradient, MOI Main, any dark or low-light ground | `Default - Dark` (pale) |
| An avatar or tile that must keep its clear space | `Padded - Light` or `Padded - Dark`, by the same rule. Do not crop |
| A watermark, a favicon, the planet beside the word MOI | `Planetoid - Light` or `Planetoid - Dark` (derived files) |
| Email, social images, anywhere SVG is not shown | The PNG of the same name at twice the display size or more |
The book also says a black and white logo is acceptable "to reduce contrast" (A4). This library has no such file. ASK: Rahul.

## Render the SVGs correctly
- The four SVG files as received have no style block, so they render solid black (the lettering is invisible on the black planet). Seven of the eight SVG files in the website's `public/brand/logos/SVG/` have the same fault (`moi-blog/references/assets.md`, checked 2026-10-02). This folder's `assets/logos/SVG/` has the repair. `SVG-as-received/` is kept as a record. `brand-check.py` fails any file that points at it.
- Set a size in CSS: the files declare 26 x 20 (Default) or 32 x 28 (Padded).
- The logo incident log: a pale mark shipped as the newsletter logo and was replaced on 2026-08-24 because it nearly disappears on white; the previous operator asked on 2026-08-17 and 2026-09-15 that the logo never render black on light backgrounds, and fixed a sign-in email logo that was a bare planet without the lettering (2026-09-15).
- The website's repaired `blog/public/brand/logos/SVG/default-light.svg` on `origin/main` (commit `5e91afa`, read 2026-10-03) lists its gradient stops the other way round: `#4B17E5` at the top and `#320F99` at the bottom. The official PNG and the original file have dark at the top. Book A4 forbids changing the direction of the gradient. Not changed here. ASK: Rahul who owns the website's brand folder.
- Book A1 draws the dark-ground logo with a grey-to-white planet (`#BFBFBF` to white, sampled from the PDF). The shipped dark files use `#DBCEF9` to white. The shipped files are what the deck, the website and the emails use. ASK: Rahul which is canonical.

## Tiny logo and favicon (book A3)
Below the size where MOI no longer fits inside the planet, the planetoid sits on the left and the wordmark MOI to its right. Smallest 10 x 10 px; use whole-number ratios such as 30 x 30 or 50 x 50. Favicons use the planetoid alone, no lettering.
This library has no tiny-logo file. The previous operator's README said two versions "ship with the system", but nothing of the kind is in the old folder. The preview cards build the lockup from `Planetoid` plus the word MOI set in Poppins Bold. ASK: Rahul for the official files.

## Do not (book A4)
1. Rotate it. 2. Warp it. 3. Change the typeface of the lettering. 4. Make it too small to see. 5. Add shadows, embossing or engraving. 6. Crowd it against other logos or graphics. 7. Use the wordmark by itself. 8. Swap the sides of the planet and the word. 9. Change the spacing between them. 10. Change the colours, the gradient or its direction. 11. Add any other effect or colour scheme. 12. Outline it or add strokes. `../preview/logo-rules-dont.html` draws each one.
Spacing (A5): the files carry a default minimum padding that must be kept when tiling the logo with other elements.

## The planetoid (book B1, B2)
The planetoid is the shape on its own. It "subtly references" the brand where a logo is not needed, can take other fill colours or strokes, and can mask images or patterns. Three uses: a solid watermark, a mask for other media, an outline on a background. Use it the same way across the website, social, print and collateral. `moi-webinar/deck/references/components.md` has the outline watermark snippet for decks. `../preview/planetoid-usage.html` shows all three.

## Pip, the mascot
Pip is not in the book (23 pages: logo, shapes, colour, type). The previous operator's README placed it on the Figma "Mascot" page. Five PNGs are in `../assets/mascot/` (see `../assets/README.md` for what each looks like).
- The old rules: use Pip where personality is needed; do not redraw it; the planet body may bleed off the edge of the frame.
- The old tagline "Pip. Your participant. On-chain." and the idea that Pip is the participant are unverified.
- "Pip" also names a demo agent in Builders session 6 (AgentBudget) and an item "Pip live in Discord" in community call 14, owned by marketing (research notes). Whether the Discord Pip is this mascot is not recorded. ASK: Sai Kiran.
- Whether the mascot is approved for external use, and who owns the artwork. ASK: Rahul.
Default until Rahul answers: internal mocks only, and ask before putting Pip on a public asset.

## Not yet known
- The official tiny-logo, black-and-white and Ai files; the owner of the "Logo Files" link. ASK: Rahul.
- Which dark-logo gradient is canonical (grey or lavender).
- Who owns the website's `public/brand/` copy and the reversed gradient in its repaired SVG.
