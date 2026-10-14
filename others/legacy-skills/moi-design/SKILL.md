---
name: moi-design
description: Use this skill to generate well-branded interfaces and assets for MOI (moi.technology, the on-chain authority layer for AI agents), either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, the Pip mascot, logos, and UI kit components.
user-invocable: true
---

> **Legacy: superseded.** Use `skills/moi/moi-devrel/design/` (`GUIDE.md`), a restructured copy of this folder with fixes. Do not trust this copy's logo rule (`README.md` lines 301-302 are inverted), its SVG logos (they render black) or its Google Fonts `@import` (it is ignored by browsers); `skills/moi/moi-devrel/design/references/provenance.md` lists every defect. The `MOI Design System/` subfolder is a duplicate of this folder from before these notes were added; do not use it.

Read the `README.md` file within this skill, and explore the other available files (especially `colors_and_type.css`, `ui_kits/marketing/`, and `assets/`).

If creating visual artifacts (slides, mocks, throwaway prototypes), copy assets out and create static HTML files for the user to view. Reference `colors_and_type.css` for every design token. Do not invent new colors, type sizes, or radii.

If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design (marketing page, slide deck, product UI, social post). Ask a few questions, and act as an expert designer who outputs HTML artifacts *or* production code, depending on the need.

Voice rules to enforce in any copy you write:
- Second person ("you"), almost never "we".
- Declarative, short, line-broken.
- Sentence case headlines; UPPERCASE only for section labels and small mono chips.
- No emoji.
- Specific vocabulary: `participant`, `authority`, `scope`, `revoke`, `on chain`, `agent`. Avoid `user`, `permissions`, `blockchain`, `AI assistant`.

Visual rules to enforce:
- The brand has **five named colours**: MOI Main `#4B17E5`, MOI Dark `#320F99`, MOI White `#FFFFFF`, MOI Grey `#BFBFBF`, MOI Black `#0A0026`. Two gradients: Purple (Dark→Main), White (Grey→White). Light bgs: Pure White, Almost Lavender `#FCFBFF`, Certainly Lavender `#F5F2FF`, Pastel Purple `#D9CCFF`. **Don't invent new hues.**
- Text colour on light is `rgba(10,5,26, X%)`; on dark it's `rgba(255,255,255, X%)`. Tiers: 85% high · 69% medium · 55% low · 30% disabled. Accent on light = MOI Main; accent on dark = `#BCA6FF`.
- Use Pip (the friendly purple planet mascot in `assets/mascot/`) for any place where personality is needed. Do **not** redraw Pip.
- Use the logos from `assets/logos/` directly. **Never use the wordmark by itself.** When the logo gets tiny, switch to the side-by-side lockup (planet left, MOI right). Do not warp, rotate, recolour, or shadow the logo.
- The planetoid shape may be used decoratively as a watermark, mask, or outline behind content.
- **Poppins is the only typeface.** Use weights 400 / 500 / 600 / 700, never Thin, Light, ExtraBold, Black, or italic. The mono / chip look is Poppins SemiBold + uppercase + 0.08em tracking.
