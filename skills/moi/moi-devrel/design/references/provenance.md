# Provenance: where this branch came from and what was changed

Facts are as of 2026-10-03. This branch is a restructured copy of a skill folder on the previous operator's machine (last modified 2026-05-28). The old skill is kept for reference in the handover repo, under `others/legacy-skills/moi-design/`, together with the brand book PDF and the logo pack in its `uploads/` folder. Back to `../GUIDE.md`.

## What was copied and what was not
| Part | Old size | In this branch | Note |
|---|---|---|---|
| `colors_and_type.css` | 12,085 bytes | yes, repaired | See "Defects" 3, 4 |
| `fonts/` | 159,684 bytes, 2 files | yes | README rewritten with the licence finding (`../fonts/README.md`) |
| `assets/` | 11.7 MB, 49 files | 9.9 MB, 55 files | Left out `cosmic-purple.png`; moved `pip-glow.png` to `backgrounds/nebula-purple.png`; added repaired SVGs and two derived planetoid files (`../assets/README.md`) |
| `preview/` | 54,959 bytes, 37 files | yes, edited | `../preview/README.md` lists the edits |
| `ui_kits/marketing/` | 36,476 bytes, 4 files | yes, edited | Copy replaced with placeholders (`../ui_kits/marketing/README.md`) |
| `SKILL.md`, `README.md` | 2,743 and 15,064 bytes | rewritten into `../GUIDE.md` and `references/` | The old frontmatter key `user-invocable` is dropped; the standard has `name` and `description` only |
| `uploads/` | 9.3 MB, 26 files | no | Brand book PDF, logo zip, a screenshot of the book's font page, 23 background files. The PDF and the zip are in the handover repo, `others/legacy-skills/moi-design/uploads/` |
| `MOI Design System/` | 21.4 MB, 121 files | no | Byte-identical duplicate |
Total in this branch, counted at the end of the 2026-10-03 review: 112 files, about 10.3 MB, of which `assets/` is 9.9 MB (9,944,826 bytes).

## Evidence used on 2026-10-03
- The 23-page brand book was read page by page (cover, contents, A1 to A5, B1 and B2, C1 to C6, D1 to D4). Page labels in this branch are the book's.
- The logo PNGs were sampled for colour. The SVGs were rendered in headless Chrome on white and on MOI Black, before and after repair. The CSS font loading was tested in headless Chrome before and after the fix.
- `moi-webinar/deck/templates/template.html` was compared with the CSS by script.
- The website repo's brand files were read from `origin/main` (commit `5e91afa`, 2026-09-24) with read-only git commands.
- `moi-blog/references/assets.md` independently records the logo-variant and black-SVG faults on 2026-10-02.
- A second review the same day re-read the brand book pages as images, rebuilt the font-loading test (it showed that `document.fonts.check` returns true on the broken CSS), re-rendered the repaired SVGs against the official PNGs, rendered the UI kit and six logo cards, and ran `brand-check.py` on good and bad inputs. What it changed: the font check, the preview card copy, the script's attribute, shorthand and named-colour handling, the PNG size note and the brand-ownership wording.

## Defects found in the previous operator's folder
1. **Logo variants inverted.** The old README and his `SKILL.md` said "Use `Default - Dark.svg` for light backgrounds". The files, the PNG pixels and book pages A1 and A4 say the opposite. The preview cards and the UI kit followed the wrong rule. Fixed in the cards and kit.
2. **SVG logos render black.** The four files have no style block. Repaired copies are in `assets/logos/SVG/`; the originals are kept in `SVG-as-received/`.
3. **Fonts never loaded.** The Google Fonts `@import` followed the `@font-face` rule, so a browser ignored it and weights 500 to 700 were missing. Fixed.
4. **An undefined variable.** `.t-body-lg` used `--lh-normal`. Fixed.
5. **Two misleading images.** `backgrounds/cosmic-purple.png` is a portrait of one person. `mascot/pip-glow.png` is a nebula, not Pip. The first is left out, the second renamed.
6. **Wrong page labels.** The old files cited C4 for light backgrounds, C5 for dark, D1 for text colours. The book has C3, C4 and C5/C6.
7. **Tracking and body weight disagreed.** `fonts/README.md` said body text is Regular and big labels take -0.03em tracking. The CSS and the book (D2, D3) say body is Medium and tracking is unchanged. Cards and the kit used negative tracking. Fixed to the book.
8. **A promise with no file.** The README said two tiny side-by-side logos "ship with the system". None exists.
9. **A favicon with lettering.** The kit used a Padded PNG; the book (A3) says favicons are the planetoid alone.
10. **Unsupported claims.** Figures, partner names, a news anecdote, sample API code and positioning lines in the README and the kit. Replaced or marked unverified (`voice.md`).
11. **A file named and not shipped.** The README listed `pip-orbit.svg` ("Pip with one ring") under `assets/icons/`. The old folder holds only `soft-star.svg` there.
12. **Sources not in the folder's reach.** The README cited the PDF and the Figma file `MOI Protocol.fig` as sources. Neither is in this library.

## Not yet known
- Whether the Figma file is current and who can open it: not recorded (the previous DevRel's notes); ASK: Rahul.
- Whether the previous operator's copy was ever shared with another team, so that the same faults live elsewhere: not recorded (the previous DevRel's notes); ASK: Rahul.
