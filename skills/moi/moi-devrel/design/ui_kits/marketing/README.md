# MOI marketing UI kit

A one-page layout built from React components: top navigation, hero with Pip, a four-card row, a dark story band with a code box, a three-figure band with partner pills, a closing call to action, a footer and a toast. The previous operator's README calls it a visual reconstruction from the Figma file's hero compositions and says no production codebase was provided. It is not a port of moi.technology. Facts are as of 2026-10-03.

## Run it
Open `index.html` in a browser. It loads React 18.3.1, ReactDOM and Babel standalone 7.29.0 from `unpkg.com` (each with an integrity hash), so it needs a network. If the browser blocks `components.jsx` on a `file://` page, the operator serves the `moi-devrel/design` folder from their own terminal (Claude does not start a server): `python3 -m http.server 8000 --bind 127.0.0.1 --directory "$SKILLS/moi-devrel/design"`, then opens `http://localhost:8000/ui_kits/marketing/index.html` and stops the server with Ctrl-C. Serve the design folder, not the kit folder, because the page reads `../../colors_and_type.css` and `../../assets/`. `index-print.html` is the same page with print rules and calls `window.print()` when it loads.

## All the copy is placeholder text
Every line of words in the kit is now a bracketed placeholder such as `[Section headline]` or `[Figure]`. The previous operator's version carried marketing lines and figures that no source in this library supports, and some conflict with the wording rules:
- three figures (a validator count, a number of years, a revoke latency) and a version label;
- a list of named partners with LIVE, NEXT and ALIGNED status;
- a story about a coding agent deleting a database in 9 seconds;
- sample code for an API (`moi.participant(...)`, `.scope(...)`, `.revoke()`) that this library has no evidence of;
- the closing line "Not your Context, Not your KitKat" and the line "Identity, not intelligence, is the bottleneck". The first is in the family of a line the blog retired, and "identity" is a retired headline word (`moi-devrel/references/terminology.md`, table D); <!-- slop-lint: ignore -->
- a page title, a hero eyebrow and a footer line that quoted a positioning statement, which is contested (`../../references/voice.md`).

Put real copy in only after `moi-devrel/claim-check` has passed it. Numbers need a source and a date.

## Other changes from the previous operator's copy
- Nav and footer use `Default - Dark.svg` (the pale logo) on the dark grounds. The old kit used `Default - Light.svg` there, which is the purple logo.
- The favicon is `Planetoid - Light.svg` (the planetoid shape alone, brand book A3). The old favicon was a Padded PNG with the lettering.
- Negative letter spacing on the large headings and figures is removed and line height is 1.1, because book page D3 allows tracking changes on over-line text only and gives titles 1.1 to 1.3.
- Em dashes became colons or plain text.

## Files
| File | What |
|---|---|
| `index.html` | The page |
| `index-print.html` | The page with print rules; prints on load |
| `components.jsx` | `MonoEyebrow`, `HairlineDot`, `Button`, `Chip`, `Orb`, `SoftStar`, `DotField`, `Nav`, `Hero`, `FourWays`, `StoryBand`, `ValidatorsBand`, `CtaBand`, `Footer`, `RevokedToast` |

Colour comes from `../../colors_and_type.css`, plus `#9871F2` in the orbs, which is not a token (`../../references/colours.md`). Assets come from `../../assets/`.
