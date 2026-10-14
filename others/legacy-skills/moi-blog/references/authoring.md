# Writing a MOI blog post

## Where the post goes

One Markdown file at `blog/src/content/posts/<slug>.md`. The filename is the slug; the URL is `https://blog.moi.technology/article/<slug>/`. Nothing registers the post anywhere else: `getCollection('posts', …)` picks it up from the glob loader in `blog/src/content.config.ts`.

Four published posts are the working reference corpus. Read at least one end to end before writing:

| Slug | Shape | Words |
|---|---|---|
| `what-is-moi-network` | Pillar / explainer, 18 H2s, 17 questions, 6 figures | ~7,950 |
| `how-to-give-an-ai-agent-authority-without-your-credentials` | Argument piece, 18 H2s, 17 questions, 3 figures | ~7,170 |
| `moi-august-2026-release` | Release post, tables + runbook | ~4,190 |
| `how-ai-agents-pay-each-other-moi` | Webinar write-up, narrative | ~3,520 |

## Frontmatter

The contract is `blog/src/content.config.ts`, enforced by Astro's content collection at build time:

```ts
schema: z.object({
  title: z.string(),
  summary: z.string(),
  date: z.coerce.date(),
  updated: z.coerce.date().optional(),
  author: z.object({
    name: z.string(),
    role: z.string().optional(),
    url: z.string().url().optional(),
  }).optional(),
  tags: z.array(z.string()).default([]),
  takeaways: z.array(z.string()).optional(),
  faq: z.array(z.object({ q: z.string(), a: z.string() })).optional(),
  cover: z.string().optional(),
  draft: z.boolean().default(false),
}),
```

`title`, `summary` and `date` are all required; `updated`, `author`, `takeaways`, `faq` and `cover` are optional, and `tags`/`draft` default to `[]`/`false`. Omitting `date` fails the build with `date: Invalid date`, not a missing-field message: `z.coerce.date()` coerces undefined to an Invalid Date first. A violation fails `npm run build --prefix blog`; it does not ship broken.

### What actually consumes each field

Trace before you decide a field is decorative. Renderers: `blog/src/pages/article/[...id].astro` (the article), `blog/src/components/PostList.astro` (blog's own listing), `scripts/build-blog-index.js` (the apex `moi.technology/blog` listing), `blog/src/pages/rss.xml.js`, `rss-email.xml.js`, `llms.txt.js`.

| Field | Where it lands |
|---|---|
| `title` | `<title>` and `og:title`, both as `${title}` followed by an em dash and `MOI Blog`; article `<h1>`, both listings, RSS titles, llms.txt and JSON-LD `headline` get the bare title |
| `summary` | `<meta name="description">`, `og:description`, the hero paragraph under the h1, both listing cards, RSS `description`, llms.txt, JSON-LD `description` |
| `date` | byline, sort key for every listing and feed, JSON-LD `datePublished`, RSS `pubDate` |
| `updated` | JSON-LD `dateModified`; byline "Updated …" **only if it differs from `date`** |
| `author.name` | byline; `.authors` line on the blog listing card; JSON-LD `author` |
| `author.role` | byline only (`· Engineering`). Not in any JSON-LD |
| `author.url` | wraps the name in a link; JSON-LD `author.url` |
| `tags` | tag pages `/tags/<tag>/`, RSS `categories`, JSON-LD `keywords`. **Visible pills only for three slugs**: see below |
| `takeaways` | the `.takeaways` box above the body. Not in JSON-LD, not in feeds |
| `faq` | `<details>` list at the bottom **and** a full `FAQPage` JSON-LD block |
| `cover` | `og:image` (after an extension swap) and the apex listing thumbnail. **Not** the blog's own listing |
| `draft: true` | removes the post from the article route, the blog index, tag pages, both RSS feeds, llms.txt, the sitemap, and the apex listing |

### Field gotchas

**Only three tags are visible anywhere.** `Base.astro` exports `NAV_TOPICS = [agents, protocol, native-assets]`, and both the article hero and `PostList.astro` filter tags through it. A tag outside that set still generates a real `/tags/<tag>/` page (`tags/[tag].astro` unions post tags with `NAV_TOPICS`) and still ships in RSS categories and JSON-LD keywords, but nothing on the site ever links to it. Right-looking-but-wrong: you tag a post `security` for discoverability, the build succeeds, the page exists, and no reader can reach it.

**`updated: <same value as date>` is a silent no-op in the byline.** `[...id].astro` guards on `updated.valueOf() !== date.valueOf()`. `moi-august-2026-release.md` sets both to `2026-08-21` and renders no "Updated" line. It still emits `dateModified`, identically valued. Set `updated` only when the post really changed after publication.

**`author.url` must parse as a URL** (`z.string().url()`). A bare domain fails the build.

**Dates are date-only and formatted in UTC.** Both renderers pass `timeZone: 'UTC'` precisely because a bare `2026-08-21` becomes UTC midnight; adding a time component will render a day early or late for someone. Write `date: 2026-08-21`, unquoted, nothing more.

**`author` is emitted as `@type: Organization` regardless.** `[...id].astro` hardcodes it, so a personal byline like "Adithya Ganesh" is published to search engines as an organization. Known defect; do not "fix" it in a content PR.

## Cover images and the social card

No post currently sets `cover`: it was removed from the release post in `902f78e` ("drop the release post's cover image"), leaving `blog/public/covers/moi-august-2026-release.{svg,png}` orphaned in the tree. As of `main`, **nothing on the blog emits `og:image`**.

If you add one, the mechanics are:

```js
// blog/src/pages/article/[...id].astro
const ogImage = cover ? new URL(cover.replace(/\.svg$/, '.png'), Astro.site).href : undefined;
```

1. Put both files in `blog/public/covers/`: `<name>.svg` and `<name>.png`.
2. Set `cover: "/covers/<name>.svg"`.
3. The `.png` **must be exactly 1200×630**: `Base.astro` hardcodes `og:image:width`/`height` to those values and sets `twitter:card: summary_large_image`. The existing pair is a 1200×630 SVG viewBox rasterized to a 1200×630 PNG.

What goes wrong if you get it right-looking-but-wrong:

- Ship only the SVG: the build passes, the apex thumbnail renders, and `og:image` points at a `.png` that 404s. X, LinkedIn and Slack fall back to a bare text preview: the exact failure `122494b` was written to fix. Nothing warns you.
- Set `cover` to a `.png` directly: the regex only strips a trailing `.svg`, so `og:image` is that same PNG. Works, but the apex listing then uses the PNG as its thumbnail too.
- Put the cover anywhere but `/covers/…`: `scripts/build-blog-index.js` resolves any other root-relative path against `BLOG_ORIGIN`, so it is fetched from the blog host instead of the apex host that copied it.

## Body

**Start at `##`.** `title` is rendered as the `<h1>`; a body `#` produces a second `<h1>` on the page. No post in the corpus contains a `#` heading. CONTENT.md's "`# This becomes h2`" is wrong: Astro renders `#` as `<h1>`, it does not demote it.

**Make H2s questions.** 43 of the 53 H2s across the four posts end in a question mark ("What changed in go-moi v0.12.0?", "Why can't ownership models fix this?"). The two reference-shaped posts run 17/18 and the release post 7/9; the narrative webinar write-up is the outlier at 2/8. CONTENT.md gives the reason: LLMs parse q→a pairs readily. Answer the question in the section's first sentence.

**Open with the claim, bolded.** `what-is-moi-network.md` line 50: `**MOI Network is the Participant Layer that provides on-chain authority.**`: one declarative sentence, first paragraph, before any setup.

**Figures.** Assets go in a per-post subdirectory of `blog/src/assets/` (the directory name need not match the slug: `agent-authority-without-credentials/` serves the post slugged `how-to-give-an-ai-agent-authority-without-your-credentials`). Reference them relatively so Astro hashes and optimizes them:

```markdown
![Long, load-bearing alt text describing what the diagram shows](../../assets/what-is-moi-network/image5.png)

*Figure 1. The MOI stack. Each rung is forced by the one above it rather than chosen.*
```

Alt text in this corpus is a full sentence, not a label. Captions are italic, numbered, and add a claim rather than repeating the alt text. `.prose img` caps height at `78vh`, so a tall portrait diagram is fitted, not stretched.

Files under `blog/public/` are served as-is from the root instead (`/covers/…`, `/brand/…`); use that only for covers and brand assets.

**Close with a recap.** Both long posts end with `## Key takeaways, recap`: a bullet list whose lead clause is bolded. This is separate from the `takeaways` frontmatter box at the top; write both.

**Tables and code** are styled and safe. Tables get `overflow-x: auto` at 13.5px. Code blocks use Shiki with `github-light` (`blog/astro.config.mjs`) on a near-white surface: there is no dark theme.

## Voice

The rules that matter, from `CONTENT.md` and confirmed by the corpus:

- Second person. "You scope what each agent can touch." Almost never "we".
- Declarative and short. State the fact, then the consequence.
- Sentence-case headlines. UPPERCASE only for small section labels.
- No emoji.
- Say `participant`, `authority`, `scope`, `revoke`, `on chain`, `agent`. Avoid `user`, `permissions`, `blockchain`, `AI assistant`.
- Gloss every protocol term on first use. Round 4 of the release-post rewrite added first-use glosses for KMOI, fuel, logic, interaction, tesseract, actor state, POLO, ICS and Cocolab, and that is what moved the newcomer score from 61 to 87.

The audience is protocol and agent-infrastructure developers. Copy that reads generated is a negative signal to them, which is also why `social/README.md` refuses to auto-generate social copy from `summary`.

### The humanizer / stop-slop conflict, resolved

Both skills are worth running. They disagree on dashes:

- `stop-slop/SKILL.md:25`: "No em dashes." Absolute.
- `humanizer/SKILL.md:38,183,193`: remove them *unless the writer's sample uses them*, in which case match the sample's rate.

**The published corpus is the sample, and it is not uniform:**

| Post | Em dashes | Per 1,000 words |
|---|---|---|
| `how-ai-agents-pay-each-other-moi` | 77 | 21.9 |
| `moi-august-2026-release` | 17 | 4.1 |
| `how-to-give-an-ai-agent-authority-without-your-credentials` | 1 | 0.1 |
| `what-is-moi-network` | 0 | 0 |

So humanizer's sample rule governs and stop-slop's flat ban does not. Match the register of the post you are writing: a narrative write-up tolerates them, a reference or argument piece drops to near zero. `90b7f8e` records the release post being cut from 33 to 19 "to match the house rate". Applying stop-slop's ban literally would make the new post the outlier against three of four published ones; applying humanizer with the wrong sibling as the sample makes it the other outlier. Pick the sibling that matches the genre.

## Verification discipline

This is the part that fails expensively. **A release post that misstates the protocol is worse than no post.**

**Rule: for any claim of the form "X does Y" about the protocol, find it in source at the released tag. Release notes are a lead, not evidence.** The notes for the August 2026 release were themselves wrong in at least two places.

What the checking actually caught, from the commit record on `main`:

| Commit | Wrong claim | Source truth |
|---|---|---|
| `1d537dd` | `predictAssetId` / `predictLogicId` | Do not exist at v0.8.0. The exports are `deriveAssetId(sender, standard)` and `deriveLogicId(sender)` from `js-moi-identifiers`. Copying the notes' names gives an import error |
| `1d537dd` | `moi.Registry` removed, `moi.Deeds` new | `moi.Deeds` is the *rename* of `moi.Registry`, same `{asset_id, asset_info}` shape. Only `Lockups` and `Mandates` are genuinely new |
| `90b7f8e` | Node upgrade sets a `ProtocolVersion` config key | No such key. The version is compiled into the binary; genesis is replaced wholesale |
| `175a733` | `VOLPAY` charges a write; `VOLRES` reports the remaining balance | `VOLPAY` designates the storage payer for a logic-state write; `VOLRES` reports volume added and released for an `(account, payer)` pair |
| `175a733` | `AccessControl` hook | It is an interface, in both go-pisa's notes and its source |
| `175a733` | The three RPCs "return a unified identifier type" | `moi.LogicIDs` and `debug.Accounts` return `identifiers.Identifier`; `net.Peers` returns `identifiers.KramaID`. One package, not one type |

Sources to check against, in order of authority: the tagged source (`github.com/sarvalabs/go-moi`, `go-pisa`, `js-moi-sdk`, `js-moi-identifiers`, `cocolang`, `vscode-coco`) → the tagged release notes → docs.moi.technology. **Operational note, unverifiable from this repo:** the live docs site had the interaction op-code numbers swapped relative to `common/ixtype.go` at v0.12.0. Treat docs.moi.technology as the weakest of the three.

The op-code table in `moi-august-2026-release.md:142` was built by diffing `IxOpType` across both tags, not transcribed. Do the same for anything a reader will decode against.

**When notes and source disagree and you cannot get a ruling:** word the post so it contradicts neither, and raise the discrepancy separately. `5c0f763` is the pattern: Registry/Deeds, the ID helpers and the MAS create flows were rewritten to the level of abstraction the notes use ("removed"/"new", "give you an ID before creation") without naming the specifics under dispute. Note that this leaves `moi.Registry` described as removed in the published post, which the tagged source contradicts; the post deliberately commits to neither reading. Do not silently pick a side.

**Do not ship HTML comments.** `1d537dd` found four `<!-- … -->` blocks, including a `TODO` inside step 2 of the operator runbook, in a post already at `draft: false`. They render as invisible markup in production. Grep for `<!--` before you open the PR.

## Build, preview, ship

```bash
npm run build --prefix blog     # Astro: validates frontmatter, renders, emits sitemap/RSS/llms.txt
npm run dev --prefix blog       # localhost:4321
npm run build                   # repo root: runs scripts/build-blog-index.js, then vite build
```

**The two builds validate differently, and the root one does not validate at all.** Root `npm run build` is `node scripts/build-blog-index.js && vite build`: the script parses frontmatter with `gray-matter` and never touches the zod schema. A post with a missing `summary` produces `undefined` in the apex listing card and exits 0. Always run the blog build too; that is the one that fails.

Both builds must be run to see a post in both places. The blog build never writes `public/blog/index.html`, and the root build never renders the article.

**Previews.** `.github/workflows/preview.yml` deploys two hosts per PR:

| | URL |
|---|---|
| Marketing site | `https://pr-<N>.preview.moi.technology` |
| Blog | `https://pr-<N>-blog.preview.moi.technology` |

Verify the post at `https://pr-<N>-blog.preview.moi.technology/article/<slug>/`. **Do not verify through the apex preview's `/blog` listing**: `BLOG_ORIGIN` is not set anywhere in the workflows, so `build-blog-index.js` falls back to `https://blog.moi.technology` and every card on the preview listing links to production, where an unpublished post 404s. The listing card itself (title, summary, date, tags, reading time) is still a valid check of the frontmatter.

Merging to `main` triggers `deploy.yml`, which authenticates via Teleport and runs `~/scripts/deploy-moi-website.sh` on the VM. The transfer mechanism is in that script, not in the repo: the `rsync` command in `blog/README.md:47` is documentation, not the workflow. Publishing and distribution are deliberately separate: merging opens a *Prepare social copy* PR at `social/<slug>.md` and sends nothing. See the distribution module and `social/README.md`.

## CONTENT.md is stale in five places

`CONTENT.md` is the checked-in author guide and is mostly right, but the repo contradicts it here. Trust the code.

| CONTENT.md says | The code does |
|---|---|
| "`# This becomes h2` (h1 is reserved for title)" | `#` renders as a second `<h1>`. Start the body at `##` |
| BlogPosting + BreadcrumbList + Organization schema, with `wordCount` | `[...id].astro` emits `@type: Article` and `FAQPage` only. No breadcrumb, no organization, no word count. (The apex listing separately emits `Blog` + `BlogPosting` + publisher `Organization`) |
| `author.name` + `author.role` → `Person` in JSON-LD "with role context" | `@type: Organization`, name and url only; `role` never reaches JSON-LD |
| "Word count and reading time displayed under the title … `3,247 words · 12 min read`" | The article byline is author · role · date only. Reading time appears on the apex listing only, as `N min read`, from `Math.round(words / 200)` (rounded, not up, floored at 1) |
| `cover` is the "listing thumbnail"; `blog/public/covers/` | True on the apex listing (`scripts/build-blog-index.js`). `PostList.astro` never reads `cover`, so the blog's own listing is text-only for every post regardless |

Palette: `CONTENT.md` names text `#15102B` and muted `#5B5570`. `blog/src/styles/global.css` defines `--ink: #0a051a` and `--muted: rgba(10, 5, 26, 0.62)`. The rest of the tokens match: `--moi-main #4b17e5`, `--moi-dark #320f99`, `--bg #fcfbff`, `--surface #f5f2ff`, `--pastel #d9ccff`, Poppins 400/500/600/700, light theme only.
