# Fonts

MOI uses Poppins and nothing else. The brand book (page D1) says "exclusively" and recommends four weights: Regular 400, Medium 500, SemiBold 600, Bold 700. It lists Thin, Extra Light, Light, Extra Bold and Black as weights not to use. Facts here are as of 2026-10-03.

## What is in this folder
| File | What |
|---|---|
| `Poppins-Regular.ttf` | Poppins Regular 400, version 4.004, 158,240 bytes. The only weight kept as a file |

## Licence
No licence note sits beside the font file: the previous operator's `fonts/README.md` did not mention one. The licence is therefore not recorded in this folder.

What the file says about itself (read with fontTools on 2026-10-03): copyright 2020 The Poppins Project Authors, designed by the Indian Type Foundry, and "licensed under the SIL Open Font License, Version 1.1" with the licence text at `https://scripts.sil.org/OFL`. The licence text itself is not in this folder. The Open Font License text (read at openfontlicense.org on 2026-10-03) lets a copy carry its copyright notice and licence as a text file, as a header, or in the font's own metadata fields, and this file carries both in its metadata. A separate text file beside it would be clearer.

ASK: Rahul whether the brand has any licence for Poppins beyond that line, and whether the licence text should be added here. Which download this file was is not recorded (the previous DevRel's notes).

## How the weights load
`../colors_and_type.css` loads Regular from this folder and Medium, SemiBold and Bold from Google Fonts. That needs a network. On a page with no network, or a machine with a blocked Google Fonts, 500, 600 and 700 fall back to a synthesised Regular.

To work offline the other three weights must be added here as files with matching `@font-face` blocks. Downloading them is a gate (name the file, source and size, then wait for a yes).

## Check that the weights loaded
Open the page in a browser and run the one-line weight listing in `../references/type.md` ("Loading the font"). Every weight the page uses must appear in it. Do not use `document.fonts.check`: it returns true even when only the Regular face exists (tested 2026-10-03). The previous operator's copy of the CSS never loaded 500, 600 or 700 because of a misplaced `@import` (fixed in this copy; `../references/type.md`).

## Roles
| Role | Weight | Source |
|---|---|---|
| Headings, display | Bold 700 | Brand book D2: "Headings use Bold fonts only" |
| Subheadings | SemiBold 600 | Brand book D2 |
| Body | Medium 500 | Brand book D2: "Body is always set to medium". Regular "may be used if necessary" |
| Over-line text, chips | SemiBold 600 or Bold 700, uppercase, 0.08em tracking | The book's example shows 10 percent tracking. This folder's CSS uses 0.08em |

The Figma file used IBM Plex Mono and Akira Expanded as placeholders (per the previous operator's notes). Neither is a brand font. Do not use a mono face for the chip look: use Poppins as above.
