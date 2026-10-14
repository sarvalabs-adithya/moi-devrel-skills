# GEO / SEO and measurement

Everything below is already built and shipping. This module is for keeping it correct, and for the
measurement layer that only half exists in code.

## What emits what

| File | Emits | Host |
|---|---|---|
| `blog/astro.config.mjs:8` | `site: 'https://blog.moi.technology'`: the origin every canonical, sitemap entry, RSS link and `llms.txt` line is resolved against | blog |
| `blog/src/layouts/Base.astro:22,32` | `<link rel="canonical">` for every page | blog |
| `blog/src/layouts/Base.astro:37-51` | `og:title/description/type/url`, and `og:image` + `twitter:card` **only when an `image` prop is passed** | blog |
| `blog/src/pages/article/[...id].astro:28-51` | `Article` JSON-LD, plus `FAQPage` JSON-LD when the post has `faq` | blog |
| `blog/src/pages/llms.txt.js` | `/llms.txt`: title, absolute URL, summary per published post, newest first | blog |
| `blog/public/robots.txt` | static `robots.txt`, allowlist below | blog |
| `@astrojs/sitemap` (`astro.config.mjs:9`) | `/sitemap-index.xml` → `/sitemap-0.xml`, every built page | blog |
| `blog/src/pages/rss.xml.js` | `/rss.xml`, untagged links, for feed readers | blog |
| `blog/src/pages/rss-email.xml.js` | `/rss-email.xml`, newsletter-tagged links, for Mailchimp only | blog |
| `scripts/build-blog-index.js` | `public/blog/index.html`: real static listing with `Blog` + `BlogPosting` JSON-LD | apex |
| `public/robots.txt` | apex robots, cross-submits the blog sitemap | apex |
| `public/sitemap.xml` | apex sitemap, 5 hand-maintained marketing routes | apex |
| `blog/src/components/Analytics.astro`, `index.html:19-27` | GTM `GTM-M4BR46Z2` on both hosts | both |
| `blog/src/lib/utm.js` | the UTM convention, imported by the blog and by `scripts/lib/share.js` | both |

## The two-host split

`moi.technology` is the React SPA; `blog.moi.technology` is a separate Astro build rsynced to its own
Nginx vhost (`blog/README.md:50-58`). Both builds read the same `blog/src/content/posts/`, which is why
`DEPLOYMENT.md:36-39` insists both run on every deploy: ship one and a post is live-but-unlisted or
listed-and-404ing.

`scripts/build-blog-index.js` exists because of that split, and its header says why in one line: the
marketing site renders client-side, so a React `/blog` route "would be an empty div to any crawler that
does not execute JavaScript, which is most of the AI ones" (lines 9-11). It runs *before* Vite in both
`npm run dev` and `npm run build` (`package.json:7,10`), writes `public/blog/index.html`, and copies
`blog/public/covers/*` into `public/covers/` so thumbnails resolve on the apex host too.

**Search Console treats the subdomain as a separate property.** Registering `moi.technology` gives you no
query data for `blog.moi.technology`: different property, different verification, different sitemap
submission. *(Operational note: not verifiable from the repo. `blog/README.md:61` points at
`DEPLOYMENT.md` for "DNS, certbot, vhost, Search Console", but DEPLOYMENT.md has no Search Console
section: that setup is undocumented and must be confirmed in the console itself.)*

Submit `https://blog.moi.technology/sitemap-index.xml` in the blog property and
`https://moi.technology/sitemap.xml` in the apex property. The apex `robots.txt:24-26` cross-submits the
blog sitemap for crawler discovery, but cross-submission is not a substitute for a property: it gets the
URLs crawled, it does not get you the query report.

## Per-article markup: what is actually emitted

Article JSON-LD (`blog/src/pages/article/[...id].astro:28-51`) is:

```js
'@type': 'Article',
headline, description: summary,
datePublished: date, dateModified: (updated ?? date),
author: { '@type': 'Organization', name, url },   // only when frontmatter has author
keywords: tags.join(', '),
mainEntityOfPage: <canonical>
```

plus a second `FAQPage` object built from `faq` when present. `.filter(Boolean)` drops the FAQ node, so a
post without `faq` emits a one-element array, which is valid.

**`CONTENT.md:137,140-149` is wrong about this.** It claims every post generates `BlogPosting` with
`wordCount`, a `Person` author, `BreadcrumbList`, and standalone `Organization` schema. The code emits
`Article` with an `Organization` author, no `wordCount`, and no breadcrumb. Trust the code. If a task asks
you to "verify the BreadcrumbList", the answer is that there isn't one: adding it is a change, not a fix.

### og:image is currently emitted on zero articles

`Base.astro:41-51` gates every image tag behind the `image` prop. The article page derives it at line 18:

```js
const ogImage = cover ? new URL(cover.replace(/\.svg$/, '.png'), Astro.site).href : undefined;
```

No post in `blog/src/content/posts/` sets `cover`, so no article in `blog/dist/article/*/index.html`
contains `og:image` or `twitter:card`. Every share renders as a text-only card. `blog/public/covers/`
already holds `moi-august-2026-release.{svg,png}`: the file exists, the frontmatter line that would use
it does not.

The `.svg → .png` swap is the trap: the *listing* thumbnail may be the SVG, but X, LinkedIn and Slack do
not render SVG og:images (comment at lines 15-17). So a raster sibling with the same basename must exist
in `blog/public/covers/` at 1200×630. Setting `cover: "/covers/x.svg"` without shipping `x.png` produces
a syntactically perfect `og:image` pointing at a 404: a broken preview looks identical to a
correctly-configured one until someone shares the link.

## Crawler access

`blog/public/robots.txt` is static (not generated, despite the comment on line 23: that comment refers to
the sitemap file, not to robots.txt). `public/robots.txt` on the apex is byte-identical through line 21
and then differs in its `Sitemap:` lines.

| User-agent | Allowed | Belongs to |
|---|---|---|
| `*` | `/` | everyone |
| `GPTBot` | `/` | OpenAI, model training |
| `ClaudeBot` | `/` | Anthropic |
| `PerplexityBot` | `/` | Perplexity |
| `CCBot` | `/` | Common Crawl |
| `Google-Extended` | `/` | Gemini training and Gemini-app grounding, *not* AI Overviews |
| `anthropic-ai` | `/` | Anthropic (legacy token) |

`GPTBot` is training only. ChatGPT's search results are crawled by `OAI-SearchBot` and user-initiated
browsing by `ChatGPT-User`: neither token is named in either file, so both fall through to the `*` group.
Nothing is blocked today, but read the table as an inventory of what the file names, not of what reaches
ChatGPT.

`Google-Extended` governs training of future Gemini models and grounding inside Gemini apps and the
Vertex AI generative APIs. It does **not** control AI Overviews: that is a Google Search surface, governed
by Googlebot and the snippet controls (`nosnippet`, `max-snippet`, `data-nosnippet`). Blocking
`Google-Extended` to stay out of AI training would not drop you out of AI Overviews, and per Google's own
crawler docs it is not a Search ranking signal either.

Both hosts allow everything. Because `robots.txt` is a static file copied verbatim into `blog/dist/`, the
PR preview hosts (`pr-<N>-blog.preview.moi.technology`) serve the same permissive file. What keeps
previews out of the index is that `Astro.site` is hardcoded to production, so a preview page's canonical
and its sitemap entries all point at `blog.moi.technology`. Do not "fix" that by making `site` dynamic
per-preview without also adding `noindex` to previews: you would turn every open PR into an indexable
duplicate of the production article.

`/llms.txt` is a hand-rolled endpoint, not an integration. It excludes drafts by the same
`({ data }) => !data.draft` filter as every other collection query, so a draft cannot leak through it.

## Sitemap contents

The built sitemap has 18 URLs: the index, 4 articles, and **13 tag pages**.

`blog/src/pages/tags/[tag].astro:5-19` generates a page for the union of every tag any post carries and
the three masthead topics. Only `agents`, `protocol` and `native-assets` are linked from the nav
(`Base.astro:17-21`) or shown on articles (`[...id].astro:61-65`). The other ten (`access-control`,
`agent-registry`, `agentic-payments`, `authority`, `go-moi`, `http-402`, `release`, `safe-agents`,
`security`, `storage-costing`) are in the sitemap and reachable from nothing; nine are single-post
pages and `authority` carries two.

That is thin content submitted for indexing at a 13:4 ratio against real articles. It is not urgent at
this size, but if Search Console starts reporting "Crawled – currently not indexed" in volume, this is the
first place to look. The fix is a `filter` on the sitemap integration, not deleting tags.

## Measurement

### What is wired

One GTM container, `GTM-M4BR46Z2`, on both hosts:

- Blog: `blog/src/components/Analytics.astro:10`, injected from `Base.astro:58`, with the `noscript`
  iframe at `Base.astro:62-63`.
- Apex SPA: `index.html:19-27`.
- Apex `/blog` listing: `scripts/build-blog-index.js:180-184,445-446` (hand-copied into the generated
  HTML because it is produced outside the React app).

GA4 is a tag *inside* the container, not in code. Both `Analytics.astro:2-9` and `src/lib/analytics.js:8-10`
say the same thing: there is deliberately no hostname check in code, because the `noscript` iframe cannot
be gated, so the guard lives once as a **Page Hostname condition on the GA4 tag's trigger in GTM**. If
preview traffic shows up in the production property, that trigger condition is what to check, not the
code.

The SPA pushes its own page views (`src/lib/analytics.js:11-19`, called from `src/App.jsx:17`), because
React Router changes the URL without a page load:

```js
window.dataLayer.push({ event: "spa_page_view", page_path, page_location, page_title });
```

A GTM trigger on `spa_page_view` fires the GA4 page_view. Remove that trigger and the marketing site
records only the entry URL per session. The blog needs none of this: it is real page loads.

`.github/workflows/deploy.yml:36-37,47-48` exports `VITE_GA_ID` and `PUBLIC_GA_ID` to the VM. **Nothing in
the repo reads either variable.** They are leftovers from a pre-GTM setup; setting them changes nothing.

### The UTM convention: the load-bearing part

GA4 attributes a click to a channel only when the link carries UTM parameters, so an untagged post is
indistinguishable from direct traffic however the property is configured: that is
`scripts/share-links.js:3-6`, near enough verbatim. This is not reporting hygiene; it is the difference
between having channel data and having none.

One definition, `blog/src/lib/utm.js`, imported by the Astro build through Vite *and* by
`scripts/lib/share.js:12-13` in plain Node. That is why the file has no dependencies: adding an import of
`node:fs` or any package breaks one of the two consumers.

| `utm_source` | `utm_medium` | label |
|---|---|---|
| `x` | `social` | X |
| `linkedin` | `social` | LinkedIn |
| `discord` | `community` | Discord |
| `telegram` | `community` | Telegram |
| `newsletter` | `email` | Newsletter |
| `devto` | `syndication` | dev.to |
| `reddit` | `social` | Reddit |

Rules that are contracts, not style:

- **Casing is lowercase, always.** GA4 treats `linkedin` and `LinkedIn` as two channels
  (`utm.js:8-9`). Hand-typing a link with a capital splits one channel's numbers across two rows and
  nothing warns you.
- **`utm_campaign` is always the post slug** (`utm.js:24-25`, `share.js:19-21`). That single choice is
  what lets one post be compared across channels and one channel across posts from the same report.
  Deviate for one post and it silently drops out of both comparisons.
- **`utm_content` separates a re-share from the original.** `share-links.js:42,50` emits exactly one:
  `day7` on X. Note that `scripts/lib/social.js:71` (`linkFor`) passes no `content`, so everything the
  Distribute workflow sends is day-0; the day-7 link is copy-pasted from `share-links.js` by hand.
- `devto` and `reddit` exist in the convention but in no automation: `social.js:23-57` only knows
  Discord, Telegram, X, LinkedIn. Syndicating to either means taking the link from `share-links.js`.

Get the links:

```bash
node scripts/share-links.js <slug>          # every channel, printed
node scripts/share-links.js <slug> --md     # markdown checklist to commit
node scripts/share-links.js                 # every published post
```

```
https://blog.moi.technology/article/what-is-moi-network/?utm_source=x&utm_medium=social&utm_campaign=what-is-moi-network
https://blog.moi.technology/article/what-is-moi-network/?utm_source=x&utm_medium=social&utm_campaign=what-is-moi-network&utm_content=day7
```

Override the host with `BLOG_ORIGIN` (`scripts/lib/share.js:17`) when generating links against a preview.

### The two RSS feeds

`/rss.xml` links are bare. `/rss-email.xml` links are newsletter-tagged. **Mailchimp must point at
`rss-email.xml`.** The header comment (`rss-email.xml.js:1-12`) records both failure modes:

- Point Mailchimp at `rss.xml` and every newsletter reader lands in GA4 as direct or referral.
- Turn on Mailchimp's own Google Analytics option instead and links *are* tagged, but `utm_campaign`
  becomes the Mailchimp campaign name rather than the post slug, which breaks the cross-channel
  comparison more subtly than no tagging at all, because the data looks fine.

Feed readers stay on the untagged `rss.xml` deliberately: labelling their traffic as `email` would be
worse than leaving it untagged.

### Worth adding in GTM (no deploy needed)

*Operational notes: these are container changes, unverifiable from this repo.*

| Add | Why it earns its place |
|---|---|
| Scroll depth trigger (25/50/75/90%) | Separates a read from a bounce. Without it a 3,000-word post and a mis-click are the same event. |
| Outbound click trigger (`docs.moi.technology`, `voyage.moi.technology`, `github.com`) | Clicks off to docs/Voyage/GitHub are the closest thing the blog has to a conversion. |
| Referral exclusion / cross-domain config for `moi.technology` ↔ `blog.moi.technology` | Without it, a reader crossing between the listing and an article starts a *new* GA4 session attributed to the other host as a referral, inflating sessions and destroying the original attribution. |
| Segment for AI referrers (`chatgpt.com`, `perplexity.ai`, `copilot.microsoft.com`, `gemini.google.com`) | These arrive as ordinary referral traffic. The posts are built for citation (`llms.txt`, FAQ schema, takeaways): isolating the segment is the only way to tell whether that work is paying. |

## Publish checklist

1. `npm run build --prefix blog`: frontmatter is zod-validated (`blog/src/content.config.ts`), so a bad
   post fails the build rather than shipping broken.
2. `grep -o 'og:image[^>]*' blog/dist/article/<slug>/index.html`: expect a hit. Empty means no `cover` in
   frontmatter, or a `cover` whose `.png` sibling is missing.
3. `grep -o 'application/ld+json.\{0,200\}' blog/dist/article/<slug>/index.html`: confirm `Article` and,
   if the post has `faq`, `FAQPage`.
4. `grep '<loc>' blog/dist/sitemap-0.xml | grep <slug>`: confirm the article is in the sitemap.
5. `grep <slug> blog/dist/llms.txt`: confirm it is in the AI index.
6. `node scripts/build-blog-index.js && grep <slug> public/blog/index.html`: confirm the apex listing has
   it. Both builds, every deploy.
7. `node scripts/share-links.js <slug> --md`: generate the tagged links before anything is sent.
8. In Search Console (blog property), request indexing for the new URL.

## Gotchas

| Looks right | Actually wrong | Symptom |
|---|---|---|
| Post is live, sitemap has it, apex Search Console shows nothing | The blog subdomain is a separate property | Zero query data, indefinitely, with no error anywhere |
| `cover: "/covers/post.svg"` set, listing thumbnail renders | The og:image points at `post.png`, which was never created | Share previews are blank; only visible when someone shares |
| Link shared as `?utm_source=LinkedIn` | GA4 splits it from `linkedin` | Two half-sized rows in the channel report, neither obviously wrong |
| Mailchimp RSS campaign wired to `rss.xml` | Newsletter clicks arrive untagged | Email shows as direct/referral; the newsletter looks like it drives nothing |
| Preview build looks correct in the browser | `BLOG_ORIGIN` is never set by `preview.yml`, so the preview listing's cards link to **production** articles and the preview blog's canonical/sitemap point at production | You "verify" a new post on the preview by clicking a card and land on the live site, or on a 404 for an unpublished slug |
| GA4 sessions climbing after a launch | No referral exclusion between the two hosts | One reader crossing hosts counts as two sessions, and the original source is lost at the hop |
| One post outperformed another | At four posts and a small following, week-to-week movement is noise | Strategy tuned on a single post's numbers. Search Console impressions in particular lag: judge at 4–8 weeks, not weekly |
