# Fonts — MOI

**MOI uses Poppins exclusively.** Allowed weights: **Regular 400 · Medium 500 · SemiBold 600 · Bold 700**.

Do **not** use Thin, Extra Light, Light, Extra Bold, Black, or any **italic** variant. No display alternate. No mono alternate. No serif alternate.

| Role | Weight | Notes |
|---|---|---|
| Body, captions | Regular 400 | local file `Poppins-Regular.ttf` |
| UI labels, eyebrows | Medium 500 | Google Fonts |
| Subheads, "mono-style" caps | SemiBold 600 | Google Fonts — used uppercase with 0.08em letter-spacing for the @handle / OFFICIAL STATEMENT look |
| Headings, display, posters | Bold 700 | Google Fonts |

## Loading

- **Poppins Regular (400)** loads from the local file `fonts/Poppins-Regular.ttf` via `@font-face` at the top of `colors_and_type.css`.
- **Poppins Medium / SemiBold / Bold (500/600/700)** load from Google Fonts via `@import`.

> Drop additional Poppins `.ttf`/`.woff2` files into this folder if you want fully offline weights — then add matching `@font-face` blocks in `colors_and_type.css`.

## How to get the "section label / chip / @handle" look without a mono face

The Figma was using IBM Plex Mono and Akira Expanded as placeholders. The real brand achieves the same hierarchy with **Poppins SemiBold + uppercase + 0.08em tracking** for chips, and **Poppins Bold + uppercase + −0.03em tracking** for big section labels. See `.t-cap` and `.t-display` in `colors_and_type.css`.
