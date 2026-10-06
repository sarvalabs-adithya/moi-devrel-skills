# Assets

Facts are as of 2026-10-03. Everything here came from the previous operator's own design skill folder, except the files marked "derived". Use the table to pick a file; `../references/logos-and-mascot.md` says when to use each.

## Logos (`logos/`)
Each logo exists as Default and Padded, each in a pale and a purple version. **The word in the file name is the ground the logo sits on, not its colour.** `Dark` is the pale lavender planet with dark purple lettering, for dark grounds. `Light` is the purple planet with white lettering, for light grounds (brand book A1 and A4, checked against the PNG pixels on 2026-10-03).

| Folder | Files | Use |
|---|---|---|
| `SVG/` | `Default - Dark`, `Default - Light`, `Padded - Dark`, `Padded - Light` | Repaired copies: the style block the export lost is put back, so they render in an `<img>` tag. Colours match the official PNGs to within 1 of 255 at six sample points |
| `SVG/` | `Planetoid - Dark`, `Planetoid - Light` | **Derived.** The planetoid shape and gradient with the lettering removed, for watermarks and favicons (brand book B1, B2, A3). Not in the brand pack as received. ASK: Rahul for the official file |
| `SVG-as-received/` | the same four names | Byte-identical to the previous operator's files. They have no style block, so they render solid black. Kept only to show the repair. Never use them |
| `PNG/` | 18 files, transparent | Default at 40, 80, 200, 400 and 1000; Padded at 56, 280, 560 and 1400; each in Dark and Light. For email, social images and anywhere SVG is not accepted |
| `JPG/` | 18 files | The same sizes as the PNGs, not transparent: the Dark files sit on a solid purple background (corner pixel `#310f99`) and the Light files on white (read 2026-10-03) |

The number in a PNG or JPG file name is the height in pixels, except the 1000 Default files, where it is the width (read 2026-10-03). So `Default - Dark - 200px.png` is 260 x 200, `Default - Dark - 1000px.png` is 1000 x 770 and `Padded - Dark - 1400px.png` is 1600 x 1400. Padded files add transparent margin around the mark. The book (A5) says the files in the brand library carry a default minimum padding that must be respected when tiling. Do not crop them.

## Mascot (`mascot/`)
Pip, five PNGs with transparent backgrounds: `pip-classic` (1254 x 1254, open eyes, small smile, no ring), `pip-smile` (open eyes, small smile, with ring), `pip-wink` (raised brow and half-closed eyes, with ring, not a wink), `pip-banner` (closed happy eyes, open smile, with ring), `pip-large` (2570 x 2030, closed happy eyes, no ring). The names are the previous operator's. The expressions were read by looking at the files on 2026-10-03.

## Backgrounds (`backgrounds/`)
| File | What |
|---|---|
| `space-deep.png` | Dark star field, 1672 x 941 |
| `nebula-purple.png` | Purple nebula, 1881 x 836. It was called `pip-glow.png` and sat in `mascot/` in the old folder, but it is not Pip |

The provenance and licence of these two space images are not recorded. ASK: Rahul.

## Icons (`icons/`)
`soft-star.svg`: the four-point bloom, 1500 x 1500, filled with `currentColor`. As an `<img>` it renders black; set `color` on an inline `<svg>` or use a CSS filter (the UI kit does).

## Left out of the copy
- `uploads/` (9.3 MB, 26 files): the 23-page brand book PDF, the logo zip, a screenshot of the brand book's font page (its file name carries the date 2026-05-20) and 23 background files named `_bg-01.png` to `_bg-23.png`. The PDF and the zip are the sources of the logos and rules; they stay with the previous operator. ASK: Adithya for the PDF, and ASK: Rahul who owns the master and the "Logo Files" link on page A1.
- The nested folder `MOI Design System/` (21.4 MB, 121 files), a byte-identical duplicate of the folder itself (checked with `diff -rq` on 2026-10-03).
- `backgrounds/cosmic-purple.png` (1.8 MB). Despite its name it is a stylised portrait of one person, not a background. It is not a brand asset and the person is identifiable. The identical file (same git blob) is in `sarvalabs/MOI-Website` under `public/brand/backgrounds/` on `origin/main` (read 2026-10-03). ASK: Rahul who is pictured and whether there is a release.
