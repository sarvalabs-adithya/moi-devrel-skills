# Brand assets and images

Covers three consumers with three different constraints: the blog itself (SVG fine), email
(SVG never renders), and social scrapers (SVG never renders, and the card is cached forever).

Paths below are relative to the repo root unless marked otherwise.

## Where things live

| Path | What | Tracked? |
|---|---|---|
| `blog/public/brand/logos/SVG/default-light.svg` | Purple-planet mark, the one the blog nav and favicon use | yes |
| `blog/public/brand/logos/SVG/default-dark.svg` | Pale-lavender mark, for dark grounds | yes |
| `blog/public/brand/moi-mark-purple.png` | Email masthead mark, 160×123, 11 KB | yes |
| `blog/public/brand/social/*-colour.png` | Email footer social icons, 48×48 | yes |
| `blog/public/covers/<slug>.svg` | Cover art, 1200×630 | yes |
| `blog/public/covers/<slug>.png` | Raster sibling for `og:image` | yes |
| `blog/src/assets/<slug>/` | In-article images, referenced from the post body | yes |
| `public/brand/` (marketing site) | Full logo pack, Pip mascot, backgrounds, `soft-star.svg` | yes |
| `public/covers/`, `public/blog/` | **Generated** by `scripts/build-blog-index.js` | **gitignored** |

`.gitignore:35-36` lists `public/blog/` and `public/covers/`. Editing anything in those two
directories is wasted work — the next `build-blog-index.js` run overwrites them from
`blog/public/covers/`. Author covers in `blog/public/covers/` only.

## Design tokens

Verified at `blog/src/styles/global.css:4-14`:

```css
:root {
  --moi-main: #4b17e5;
  --moi-dark: #320f99;
  --ink: #0a051a;
  --bg: #fcfbff;      /* Almost Lavender */
  --surface: #f5f2ff; /* Certainly Lavender */
  --pastel: #d9ccff;
  --muted: rgba(10, 5, 26, 0.62);
  --line: rgba(10, 5, 26, 0.08);
  --font: 'Poppins', system-ui, -apple-system, sans-serif;
}
```

These agree with the `moi-design` skill's `colors_and_type.css`. One apparent conflict that is
not one: `moi-design` names MOI Black as `#0A0026`, while `--ink` is `#0a051a`. `#0a051a` is
`rgb(10,5,26)`, which is exactly the text colour `moi-design` mandates on light grounds
(`rgba(10,5,26, X%)`). The blog is following the text rule, not diverging from it. `--muted`
at `.62` sits between `moi-design`'s medium (69%) and low (55%) tiers; the nav's secondary
"Blog" label uses `.55`, which is the documented low tier exactly.

Poppins for all UI and prose. The one exception is code: `.prose code` in
`[...id].astro:280-282` uses `ui-monospace, 'SF Mono', Menlo, Consolas, monospace`.

## The logo variant trap

**`default-light.svg` is the purple planet with white MOI. `default-dark.svg` is the pale
lavender planet.** The name refers to the background it is meant to sit on, not to the colour
of the mark.

Verified from the gradient stops:

| File | Gradient stops | Mark reads on |
|---|---|---|
| `default-light.svg` | `#4b17e5` → `#320f99`, letters filled `#ffffff` | light / white |
| `default-dark.svg` | `#dbcef9` → `#fff` | dark |

Two independent things make this easy to get backwards, and both have already caused a
wasted PR:

**1. The `moi-design` skill documents the mapping inverted.** Its `README.md:301-302` says
"Use `Default - Dark.svg` for light backgrounds and `Default - Light.svg` for dark
backgrounds." Its own asset files say the opposite — `moi-design/assets/logos/SVG/Default -
Dark.svg` carries the `#dbcef9 → #fff` pale gradient. Trust the gradient stops, not the
sentence. If you pick the file by reading that line, you ship a mark that nearly vanishes
against white; this is what happened in `85629a5`, which had to correct `b8c3dea`.

**2. Every logo SVG in the brand pack renders black except one.** The exported SVGs reference
CSS classes (`.cls-1`, `.cls-2`) whose `<style>` block was stripped on export, leaving an
empty `<defs>`. With no rule for those classes, the paths fall back to default fill — solid
black. Only `default-light.svg` (1808 bytes) has a repaired `<style>` block:

```html
<defs>
  <style>
    .cls-1 { fill: url(#linear-gradient); }
    .cls-2 { fill: #ffffff; }
  </style>
  <linearGradient id="linear-gradient" ...>
```

`default-dark.svg` and all four space-named variants (`Default - Dark.svg`, `Default -
Light.svg`, `Padded - *.svg`) are 1691–1717 bytes with zero `<style>` blocks. So are all four
SVGs inside the `moi-design` skill. `Base.astro:33-36` documents this:

> the only file under brand/logos/SVG whose stylesheet is intact; the rest render black

**Copying a logo SVG out of the `moi-design` skill gives you a black square.** Copy from
`blog/public/brand/logos/SVG/default-light.svg` instead, or repair the `<style>` block by
hand. The blog and marketing-site copies of `default-light.svg` are byte-identical, so either
origin is fine.

## Blog masthead spec

`global.css:193-220`. Match this for anything that should read as the same masthead:

| Element | Spec |
|---|---|
| `.nav-brand` | flex, `gap: 9px` |
| `.nav-brand img` | `height: 30px`, `width: auto` |
| `.nav-wordmark` | `16px` / `700` / `letter-spacing: -0.01em` / `var(--ink)` |
| `.nav-wordmark span` ("Blog") | `font-weight: 400`, `rgba(10, 5, 26, 0.55)` |

## Email images

`Subscribe.astro` is only the signup form (a bare POST to Mailchimp's hosted endpoint at
`blog/src/components/Subscribe.astro:18-20`, deliberately without their embed's jQuery and
600 lines of SMS country-code handling). **The campaign template itself is not in this repo** —
it lives in Mailchimp. The repo's job is to *host* the images the template references by
absolute URL off `https://blog.moi.technology/brand/…`. That is also why they sit under
`blog/public/` rather than the marketing site: newsletter and blog share one origin.

### Rules

- **Rasterise everything.** Gmail strips SVG, Outlook never supported it. `b8c3dea` added the
  first PNG for exactly this reason.
- **Serve at 2× the display size**, and set `width`/`height` as HTML *attributes* as well as
  inline styles. Outlook ignores the CSS and will render at intrinsic size otherwise.
- **Always set `alt`.** Many clients block images by default; the alt text is the entire
  message until the reader clicks "show images".
- **No spaces in filenames** — the space-named brand files would need URL escaping in a
  template. `b8c3dea`'s message states the rule for `logo-email.png`. (It is not why the
  lowercase SVG copies exist — those predate the newsletter by three months and serve the
  blog's own nav and favicon.)

### The cache rule

**Never change an image in place under the same filename.** Mailchimp fetches by URL and
caches indefinitely, in both its template designer and the public campaign archive, and offers
no purge. Once it has fetched a URL, the origin can serve anything it likes and the old bytes
keep going out.

This cost three PRs to learn (`b8c3dea` → `85629a5` → `b150873`). `logo-email.png` was
replaced in place — dark variant, then light — and the purple mark never appeared. From
`b150873`:

> A new path is the only reliable way out; image caches are keyed on URL and Mailchimp gives
> you no way to purge one.

The fix was a rename to `moi-mark-purple.png` — **named for its variant, so the next change is
naturally a new file rather than an overwrite**. Follow that convention. `17bcf5a` did:
recolouring the icon set shipped five *new* `-colour.png` files rather than overwriting the
originals.

Corollary: the superseded monochrome icons (`x.png`, `discord.png`, …) are still in the tree
and should stay. Campaigns already sent point at those URLs, and deleting them breaks the
archive for every past send.

### Current asset inventory

| Asset | File | Size | Display | Colour |
|---|---|---|---|---|
| MOI mark | `brand/moi-mark-purple.png` | 160×123 | 39px wide (39×30 in the header lockup) | purple gradient, white MOI |
| MOI | `brand/social/moi.png` | 62×48 | 24px tall | purple gradient `#4B17E5` → `#320F99`, white MOI |
| X | `brand/social/x-colour.png` | 48×48 | 24px | `#000000` |
| LinkedIn | `brand/social/linkedin-colour.png` | 48×48 | 24px | `#0A66C2` |
| Discord | `brand/social/discord-colour.png` | 48×48 | 24px | `#5865F2` |
| Telegram | `brand/social/telegram-colour.png` | 48×48 | 24px | `#26A5E4` |
| GitHub | `brand/social/github-colour.png` | 48×48 | 24px | `#181717` |

Every icon is transparent. The five service marks are all under 1.2 KB; `moi.png` is 4 KB,
being a gradient rather than a flat fill. It is also **62×48, not square** — it is
height-matched to the row so the planet sits level with the circular marks. Setting
`width="24" height="24"` on it squashes the planet into an egg; set the height and let the
width follow.

The masthead mark is served at 160×123 for a 39×30 display — closer to 4× than 2×. The **2×** rule
above is a floor, not a description of this asset.

There is no `moi-colour.png`. The MOI mark was already brand-purple in `22e4456` and was not
reissued in `17bcf5a`; it stays first in the row so the row opens on ours.

Brand colours rather than a single tint, per `17bcf5a`:

> A single purple tint made the row read as five variations of one mark rather than five
> destinations. The shapes are recognisable; the colour is what makes them scannable.

The icon paths are rasterised from **the same SVG paths the marketing site footer uses**
(`src/components/LandingFooter.jsx`, 24×24 viewBox, `fill="currentColor"`), so the two sets
cannot drift. The email row is a subset: the footer also carries Medium and YouTube, which the
newsletter row omits.

## Cover images and `og:image`

Contract, from `blog/src/pages/article/[...id].astro:15-18`:

```js
// The listing thumbnail is the SVG cover; social cards are not. X, LinkedIn
// and Slack do not render SVG og:images, so a raster sibling with the same
// name ships beside every SVG cover (public/covers/<slug>.png, 1200x630).
const ogImage = cover ? new URL(cover.replace(/\.svg$/, '.png'), Astro.site).href : undefined;
```

So: `cover` is an **optional** frontmatter field (`content.config.ts:23`) holding the SVG
path. The `og:image` is derived by swapping the extension to `.png`. It is *not* inferred from
the slug — a PNG sitting on disk with no `cover:` in frontmatter is invisible to the build.

`Base.astro:41-51` emits `og:image`, `og:image:width`, `og:image:height`, `twitter:card` and
`twitter:image` as a block, or nothing at all. The rationale sits with the props destructure at
`Base.astro:9-11`:

> Pages without one emit no og:image at all rather than a placeholder — a missing card
> degrades to a text preview, a wrong one misrepresents the page.

**Current state: no post sets `cover:`.** `grep '^cover:' blog/src/content/posts/*.md` returns
nothing across all four posts, and `grep og:image blog/dist/article/*/index.html` returns
nothing. A cover pair exists for `moi-august-2026-release` but is unreferenced, so that post
ships with no social card. The listing tile is also gated on the same field
(`build-blog-index.js:122-138` — "No cover means no tile"), and `PostList.astro` on the Astro
blog does not render covers at all; its cards are text-only. Adding `cover:
/covers/<slug>.svg` to frontmatter is what lights up both the tile and the card.

Cover SVGs are hand-authored, 1200×630, using the tokens directly and with a real font
fallback stack (`font-family:Poppins,'Helvetica Neue',Arial,sans-serif`). Keep the fallback —
see below for why it matters.

## Rasterising SVG → PNG

**`sharp` is available** at `blog/node_modules/sharp` (v0.34.5, pulled in by Astro's image
service). Run it from the `blog/` directory:

```js
// cd blog && node -e '...'
const sharp = require('sharp');
sharp('public/covers/my-slug.svg').png().toFile('public/covers/my-slug.png');
```

Verified working — it renders the existing 1200×630 cover correctly.

Nothing else is installed. `cairosvg`, `rsvg-convert`, `inkscape`, `magick` and `convert` are
all absent from PATH, and there is no `sharp` at the repo root, only under `blog/`.

### The font caveat

**sharp will not use Poppins.** Poppins is not installed as a system font — it exists only as
a webfont in `blog/node_modules/@fontsource/poppins/`, and sharp's SVG renderer has no webfont
loader. Text in a rasterised cover falls back down the stack to Helvetica Neue.

This is not hypothetical and it is not currently fixed: rendering
`covers/moi-august-2026-release.svg` through sharp produces type visually identical to the
committed `moi-august-2026-release.png`. **The shipped cover PNG is already in Helvetica Neue,
not Poppins**, while the page around it renders Poppins. If brand type in the card matters,
either install Poppins system-wide before rasterising, or use the browser route below. If it
does not, sharp matches what already shipped.

For pure-shape assets — the logo mark, the social icons, anything with no `<text>` — sharp is
correct and the caveat does not apply.

### Headless-browser fallback

When the SVG carries text and the real webfont is required, render in a headless browser (the
`Claude_Browser` preview tools work), draw to a canvas at the target size, and read out
`canvas.toDataURL('image/png')`. The browser loads the actual `@fontsource` face, so type
comes out in Poppins. Slower and fiddlier than sharp; reach for it only for text-bearing
covers.

## Operational notes — external services

Not verifiable from the repo. Treat as learned-the-hard-way, not as checked fact.

- **X and LinkedIn cache the preview card on first scrape of a URL.** LinkedIn especially: if
  you post before `og:image` resolves, the broken card sticks to that URL more or less
  permanently. Run LinkedIn's Post Inspector to force a re-scrape *before* sharing, not after
  someone reports the card looks wrong.
- **Mailchimp offers no cache purge** for fetched images — the basis of the naming rule above.

## MOI social destinations

From `src/components/LandingFooter.jsx:1-80`, in footer order:

| Label | URL | In email row? |
|---|---|---|
| Telegram | `https://t.me/moi_tech` | yes |
| Discord | `https://discord.gg/5gG6efFN4s` | yes |
| Twitter | `https://twitter.com/moi_tech` | yes (as X) |
| Medium | `https://medium.com/moi-technology` | no |
| YouTube | `https://www.youtube.com/channel/UCit7h30bhrwxBd1Yt_bmPvg` | no |
| GitHub | `https://github.com/sarvalabs` | yes |
| LinkedIn | `https://www.linkedin.com/company/moi-tech` | yes |

The footer link is still `twitter.com/moi_tech` even though the icon is the X glyph. Leave it;
`twitter.com` redirects, and changing it is not an assets task.
