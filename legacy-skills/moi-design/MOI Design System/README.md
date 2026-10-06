# MOI Design System

> **MOI is the on-chain authority layer for AI agents.**
> You exist once, on chain, as a coherent participant. Your authority stays
> anchored to you, wherever your agents go.

A design system for marketing surfaces, social content, and product UI for
MOI (moi.technology).

---

## What MOI is

Today, an AI agent that acts on your behalf is given **copies** of your
credentials — an API key to your bank, an OAuth token to your email, a JWT
to whatever it needs to touch. Those copies aren't information; they're
**value**, and anyone holding the copy can use it.

MOI is the **participant layer** that sits underneath your AI stack. You
exist once, on chain, as a coherent participant. Authority is anchored to
you. You can **monitor** what your agents do, **scope** what they can
touch, and **revoke** their access in real time. MOI doesn't replace
OpenAI, Claude, LangChain, or any of your tools — it makes them
trustworthy.

The four-step product promise — used across hero pages, social, and decks:

1. **Exist on-chain** — one coherent participant, your authority anchored to you.
2. **Monitor** — see every action in real time.
3. **Scope** — choose what each agent can touch.
4. **Revoke** — cut access at machine speed.

MOI currently works with **@openclaw**, with **@LangChain** support coming next.

## Sources used to build this system

This system was reconstructed from materials the user attached. The
**Figma** file is design-authoritative; the codebase was not provided.

- **Figma:** `MOI Protocol.fig` (mounted as virtual filesystem). Pages
  read: `/Work-Space-Background/Shades`, `Typography`, `X-Banner-Logo`,
  `X-Posts`, `Backgrounds`, `Space-Backgrounds`, `Mascot`.
- **Brand Guidelines PDF:** `uploads/MOI Brand Guidelines.pdf` (23 pages, sections A–D). This is the **authoritative** source for colour, type, and logo rules; the Figma fills in marketing and social treatments. Rendered pages are saved alongside the PDF.
- **Logo pack:** `uploads/MOI Logos.zip` — extracted to `assets/logos/`
  with SVG, PNG, and JPG variants at six sizes, light and dark.
- **No website codebase or GitHub repo was attached.** Production
  components below are recreations from Figma intent and the brand book, not from source.

---

## Index — files in this system

| Path | What |
|---|---|
| `README.md` | This file. |
| `SKILL.md` | Agent-Skill front-matter so this folder can be dropped into Claude Code. |
| `colors_and_type.css` | All design tokens — colors, type, radii, shadow, spacing, gradients. |
| `fonts/README.md` | Font roster + paid-face substitutions to flag. |
| `assets/logos/` | Official MOI logos — SVG / PNG / JPG, light + dark, 40px → 1400px. |
| `assets/mascot/` | **Pip** — the MOI mascot (purple ringed planet, several expressions). PNG. |
| `assets/backgrounds/` | Hi-res cosmic backgrounds extracted from the Figma. |
| `preview/` | Cards rendered into the Design System tab. |
| `ui_kits/marketing/` | Marketing-site UI kit + click-through prototype (`index.html`). |

---

## CONTENT FUNDAMENTALS

MOI writes like a security researcher who has stopped explaining and
started declaring. Confident, terse, slightly cosmic. The voice is
**short, declarative, second-person.** Sentences are often single lines,
broken hard.

### Voice & tone

- **Declarative, not promotional.** "Your authority stays anchored to you."
  Not "We help anchor your authority."
- **Second person, never first.** "You exist once, on chain." Almost no
  "we" or "our." When MOI does appear, it is as a noun: "MOI currently
  works with @openclaw."
- **Cause → consequence.** Set up a fact, hit return, name the
  consequence. Example: "Anyone holding the copy can use it." Then a
  blank line. Then a story.
- **Quiet menace, then exit.** Posts often reach a turn where the stakes
  land in a single short line — *"Used it and deleted a production
  database in 9 seconds. Wrote an apology after."* — then resolve flat.

### Casing

- **Sentence case** for headlines and titles. ("You have Independent
  Existence." — capital I on Independent and Existence is *intentional
  emphasis*, not a Title-Case rule.)
- **UPPERCASE** for section labels (the giant "TYPOGRAPHY", "BACKGROUNDS"
  display headers), tagged callouts (`OFFICIAL STATEMENT`), and short
  verbs in the product story (MONITOR / SCOPE / REVOKE).
- **lowercase** for handles, URLs, and `moi.technology` whenever it
  appears as a wordmark.

### "I" vs "You"

- "You" is the participant — the human, the developer, the founder. Almost
  every public sentence is addressed to "you."
- "Your agent" is the actor that needs authority.
- MOI never says "I." It refers to itself as MOI, or as "the participant
  layer."

### Emoji

- **Almost never.** No emoji on the site or in social hero cards. A
  single `>` is used as a quoting marker in long posts (see the
  "@VitalikButerin / @ChristopherA / @a16zcrypto" thread).
- Unicode arrow `→` is acceptable as a cue between steps
  (`Exist on-chain → Monitor → Scope → Revoke`).

### Vocabulary — say / don't say

| Say | Don't say |
|---|---|
| participant | user, account, identity |
| authority | permissions, role |
| scope, revoke | configure, manage |
| credentials are **Value** | tokens are sensitive |
| on chain | blockchain, web3, crypto |
| agent | AI assistant, bot |
| the participant layer | our platform, our product |

### Specific copy examples (verbatim from Figma & brief)

> **You haven't met the participant yet.**

> **The Internet Has 12 Versions of You.**

> **Your authority, four ways.** — *Exist on-chain · Monitor · Scope · Revoke*

> **Not your Context, Not your KitKat.** *Become a Participant.* —
> Posted under an `OFFICIAL STATEMENT` chip.

> **Pip.** *Your participant. On-chain.* — Sub-line under the mascot.

> **Monitor, scope and revoke AI Agents in real time.** —
> Hero sub-line for `moi.technology`.

### Punctuation tics

- Heavy use of em-dash em-dash style lists in long-form, line breaks in short.
- Period after fragments: "Anchored. Yours." is fine.
- Numbers stay numerals always: "2,100+ Validators", "9 seconds", "Seven years."

---

## VISUAL FOUNDATIONS

### Palette

The brand book ships **five** named colours. Everything in MOI is built from these and their tints.

| Token | Hex | Where it's used |
|---|---|---|
| **MOI Main** | `#4B17E5` | Primary brand purple. Buttons, accents, the planet body. Print: `#3E308C`. |
| **MOI Dark** | `#320F99` | Top end of the official Purple Gradient; also used as a flat dark surface. Print: `#221460`. |
| **MOI White** | `#FFFFFF` | The first half of brand contrast — "white against purple". |
| **MOI Grey** | `#BFBFBF` | Bottom of the White Gradient. Neutral. |
| **MOI Black** | `#0A0026` | The **only** flat dark background MOI uses. Elevations come from white overlays at 5 / 7 / 8.25 / 9.75 / 11 / 13 %. |

Light backgrounds (brand book C4) come in four kinds, in order of strength: **Pure White** `#FFFFFF`, **Almost Lavender** `#FCFBFF`, **Certainly Lavender** `#F5F2FF`, **Pastel Purple** `#D9CCFF`.

Two official gradients (page C2):
- **Purple Gradient** — `MOI Dark → MOI Main` (`#320F99 → #4B17E5`). Used everywhere "purple" is.
- **White Gradient** — `MOI Grey → MOI White` (`#BFBFBF → #FFFFFF`). Used for soft mono surfaces.

### Type

- **Poppins, exclusively.** Allowed weights: **Regular 400 · Medium 500 · SemiBold 600 · Bold 700**. Do not use Thin, Light, ExtraBold, Black, or any italic variant.
- **Headings use Bold (700) only.** Subheadings may use SemiBold (600). **Body is always Medium (500).** Body-emphasis (`<b>`, `<strong>`) jumps to Bold within the Medium paragraph.
- **Tracking is 0%.** Do not change letter-spacing on any text **except over-line / chip text**, where uppercase + 0.08em is allowed (the `@MOI_Tech` chip look).
- **Leading:** 1.25× on headings and titles. 1.5× on body. 1.75× on small print.
- **Text colours** are opacity-on-`#0A051A` (light bg) or opacity-on-white (dark bg): Accent · High Emphasis 85% · Medium 69% · Low 55% · Disabled 30%. On dark backgrounds, the accent shifts to `#BCA6FF`.
- A 33-step modular ramp (ratio ≈ 1.125) from 7px to 304px. See the `--size-*` tokens.

### Spacing

- 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96. Multiples of 4.
- Hero compositions are extremely **generous** with negative space.
  Notice the Figma banners: huge mascot or orb on the right, headline
  bottom-left, watermark hugging a corner.

### Backgrounds

- **Three classes of surface** dominate:
  1. **Cosmos** — `--grad-cosmos` (`#0A0026 → #4B17E5`) — dark hero,
     mascot moments, drama.
  2. **Lavender Haze** — `--grad-lavender` (`#F5F2FF → #D9CCFF`) — soft
     content surfaces, secondary heroes.
  3. **Plain white** — neutral, when the photography or chart is the
     star.
- **Heavily decorated with motion-static elements** on hero surfaces:
  - Floating gradient **orbs** (circles with `--shadow-inner-bright`).
  - **Soft-Star quasars** — a 4-point "+" bloom shape (`assets/icons/`).
  - **Dot grids** at low contrast.
  - **Concentric radar rings.**
  - **Hairline streaks** — gradient hairlines used as orbital arcs.
- **No photography of people.** Imagery is either Pip the mascot, an
  abstract cosmic field, or product UI.
- **Imagery vibe:** cool purple, dimly glowing, never warm. Slight
  film-grain noise allowed on dark cosmic gradients.

### Borders & radii

- **8 / 12 / 20 / 32 / 48 / 999.** Cards usually `20px`. Pills `999px`.
- Borders are typically `1px solid var(--border-soft)`
  (`rgba(217,204,255,0.5)`) — barely-there hairlines, almost always on
  light surfaces only.
- On dark surfaces the equivalent is `1px solid rgba(217,204,255,0.15)`.

### Shadows

The signature is **inset highlight** — an inner top-light glow that
makes orbs and chips look like 3D objects:

```css
box-shadow: inset 0 1.45px 33px rgba(255, 255, 255, 0.25);  /* signature */
```

Outer shadows are soft and indigo-tinted, not grey:

```css
box-shadow: 0 12px 32px rgba(50, 15, 153, 0.07);
```

Glow shadows live on hover for CTAs:

```css
box-shadow: 0 0 40px rgba(75, 23, 229, 0.40);
```

### Hover & press

- **Buttons:** hover = `--shadow-glow`, background unchanged. Press =
  scale 0.97, glow halves, 80ms.
- **Cards:** hover = lift 2px + `--shadow-card-lg`. 200ms ease-out.
- **Links:** hover = `border-bottom: 1px solid currentColor` appears.
  No colour shift. 160ms.
- **Icon buttons:** hover = background `rgba(75,23,229,0.08)`, no scale.

### Animation

- **Easings:** `cubic-bezier(0.22, 0.61, 0.36, 1)` (the "out-quart"
  default), `cubic-bezier(0.65, 0, 0.35, 1)` (in-out for orbital loops).
- **Durations:** 80ms (press), 160ms (link), 200ms (card lift),
  400–800ms (page enter), **8–16s** (orbital loops, mascot ring spin).
- **Style:** *gliding,* never bouncy. The mascot ring drifts in 12s
  loops. Glow pulses on `pulse 6s ease-in-out infinite alternate`.
- **No spring bounces.** No overshoot.

### Layout rules

- **Fixed nav** at top, transparent over hero, blurred over content.
- **Watermark at corner.** The `@MOI_Tech` mono-handle is almost always
  in the top-left of hero cards. `moi.technology` lives bottom-right.
- **Bleed.** Hero artwork (mascot, orbs) bleeds **off-frame** at the
  edge — Pip's planet body extends past the canvas.
- **Hairline + dot lockup.** Many compositions include a tiny
  `•———` motif: a dot + a gradient hairline — see the X-banner subhead
  underline. Use as separator or signature.

### Use of transparency & blur

- Glass surfaces (`backdrop-filter: blur(20px)` + 6% lavender fill) are
  used on **dark cosmic** backgrounds — never on white.
- Hairlines & gradients use opacity heavily — `rgba(217,204,255, 0.10–0.50)`.

---

## LOGO RULES (brand book section A)

The MOI logo is the **planetoid shape with the letters "MOI" inside it.** This is the primary lockup.

- **Two versions:** Dark (purple gradient planet, white MOI) for light backgrounds. Light (lavender gradient planet, dark MOI) for dark backgrounds.
- **Minimum size:** 24 × 20 px. Scale in whole-number ratios for crisp screen reproduction (e.g. 72 × 60, 120 × 100). For print, scale freely — proportions intact.
- **Tiny logo (mobile, small print):** when MOI no longer fits inside the planetoid, switch to the **side-by-side lockup**: planet shape **left**, "MOI" wordmark **right**. Two versions (light/dark) ship with the system. Minimum size for tiny logo is 10 × 10 px.
- **Favicons** use the planet shape **alone** — this is the only place "MOI" is allowed to be missing.
- **The MOI wordmark is NEVER used by itself.** "moi.technology" (the URL) is *not* the wordmark and may appear with the logo as a nav lockup — but the bare letters "MOI" must always sit inside or beside the planet.
- **Do not:** rotate, warp, change typeface inside the planet, change the colour / gradient / direction, add any visual effect (shadow, emboss, engrave), switch the placement of planet vs. MOI, outline-only versions, additional strokes.

## ICONOGRAPHY

MOI does not ship a custom icon font, and the Figma file does not contain
a finalised icon library yet — so this system standardises on a free,
linkable set.

- **Standard set: Lucide** (`lucide-react` / `lucide.svg`), at
  **1.5px stroke** to match MOI's hairline aesthetic, rendered at 20–24px.
  Linked from CDN: `<script src="https://unpkg.com/lucide@latest"></script>`.
  → Flagged as a **substitution** — confirm with the user whether to swap
  for a specific brand-licensed set.
- **Brand symbols** (custom, copied from Figma into `assets/icons/`):
  - `soft-star.svg` — the signature 4-point bloom used decoratively on
    banners and as a starburst accent. Solid-fill SVG, scales to any size.
  - `pip-orbit.svg` — Pip with one ring (small mark, used as accent).
- **Logos** live in `assets/logos/` (SVG + PNG + JPG, Light + Dark, six
  sizes). Use `Default - Dark.svg` for light backgrounds and
  `Default - Light.svg` for dark backgrounds.
- **Mascot** illustrations (the friendly purple planet **Pip**) live in
  `assets/mascot/` as PNG. Several expressions: `pip-classic`,
  `pip-smile`, `pip-wink`, `pip-large`, `pip-glow`, `pip-banner`.
- **Emoji are not used.** Unicode `→` for step flows is acceptable.
- **Inline glyphs** in code (`{ }`, `→`, `·`) are common — these are
  characters, not icons.

When in doubt: ship a **Lucide line icon at 1.5px stroke in
`var(--moi-main)` or `var(--moi-dark)`**. If the surface is dark, switch
to `var(--moi-haze)`.

---

## See also

- The **`preview/`** folder renders every system card in the Design
  System tab. Each card is its own HTML file — open one to copy its
  approach into a new design.
- The **`ui_kits/marketing/`** folder is a hi-fi recreation of the
  moi.technology marketing surface as a single click-through HTML
  prototype, with the Pip mascot, hero animation, "Your authority, four
  ways" feature panel, validator counter, and footer.
