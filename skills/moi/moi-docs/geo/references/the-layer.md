# The layer: each piece, what makes it, and where it stands

Facts are as of 2026-10-03 unless dated. Sources: the files on branch `geo-fixes` of each repo (read from the previous operator's clones, last fetched 2026-10-01), `DOCS-STYLE-GUIDE.md` (on `main` of `sarvalabs/moidocs` since #124 merged on 2026-10-13), and read-only requests to the live sites and to the pull request previews on 2026-10-03. The pull request states were refreshed on 2026-10-13; the live-site columns are from before the merges, so read them again. Back to `../GUIDE.md`.

"The layer" is the set of files, tags and headers that let a search engine or an AI assistant find a MOI page, read it without running JavaScript, and cite it. Page wording is the parent skill's job (`moi-docs`); a blog post's own rules are `moi-blog`.

## Where the work sits
On 2026-10-13 the new files had merged for the three Docusaurus docs sites (voyage-docs #5 and coco-docs #12 on 2026-10-05, moidocs #124 on 2026-10-13) and the marketing site (#57, 2026-10-05); for the Sphinx site (#150) and the Voyage app (#447) they merged on 2026-10-14: #150 is live, #447 is not (voyage.moi.technology/llms.txt still answers 404; the Voyage team deploys). What follows describes the clones as fetched on 2026-10-01, before the merges. Older versions of `robots.txt` and the sitemap are on `main` for the website and the Voyage app. The blog and the Launchpad have their layer on their default branch (their rows say so). Git was checked with `git cat-file -e origin/main:<path>` in each clone: `scripts/generate-llms.mjs`, `scripts/inject-schema.mjs`, `llms.config.json`, `static/robots.txt`, `static/_headers` and the `.well-known` files are absent from `origin/main` of `moidocs`, `coco-docs` and `voyage-docs`. The branch `geo-fixes` of those three repos and of `MOI-Website` is on GitHub (`origin/geo-fixes`); the `js-moi-sdk` and `voyage` branches are on the fork `sarvalabs-adithya`. A clone's `origin/main` is as of its last fetch, 2026-10-01, so run `git fetch` yourself (GATE: it writes to your clone and reads from GitHub, so say so first) before you say "not merged".

| Property | Repo (default branch) | Pull request carrying the layer (state 2026-10-13) | Live on 2026-10-03 (before the merges) |
|---|---|---|---|
| docs.moi.technology | `sarvalabs/moidocs` (private, `main`) | #124, merged 2026-10-13 (on 2026-10-02 Rahul's change request was met by commit 75f608b and not re-reviewed, and Gokul was requested). #127, the skills index to Coco 0.9.3, is open and needs review | `/robots.txt` and `/llms.txt` 404. Canonical and every sitemap address name `wiki.moi.technology`, which did not answer on 2026-10-03; the sitemap lists the template page `markdown-page`; no JSON-LD |
| voyage-docs.moi.technology | `sarvalabs/voyage-docs` (private, `main`) | #5, merged 2026-10-05 | `/robots.txt` and `/llms.txt` 404 |
| cocolang.dev | `sarvalabs/coco-docs` (private, `main`) | #12, merged 2026-10-05 (approved by Robert Špendl on 2026-09-29) | `/robots.txt` is Cloudflare's managed comment block and holds no rule; `/llms.txt` 404; the sitemap names `cocolang.docs.moi.technology`, a mirror that also answers 200, and lists sample pages |
| js-moi-sdk.docs.moi.technology | `sarvalabs/js-moi-sdk`, folder `docs/` (public, `main`) | #150, merged 2026-10-14 by Gokul and live, from the previous DevRel's fork (sarvalabs-adithya); no preview existed | Every path, including a missing one, answers 200 `text/html` |
| voyage.moi.technology (the Voyage network explorer app) | `sarvalabs/voyage` (private; deploys run from `develop`) | #447, merged 2026-10-14 by Gokul, not live: the Voyage team deploys, and the last Voyage deploy was 2026-10-06. It targeted `main` while deploys run from `develop`, so confirm what the deploy ships. ASK: Gokul | `robots.txt` and the sitemap name `voyage.ai`, another party's domain |
| moi.technology | `sarvalabs/MOI-Website` (public, `main`) | #57, merged 2026-10-05 | `robots.txt` has seven groups and no Content-Signal; `/llms.txt` answers 200 `text/html`; 5 sitemap addresses |
| blog.moi.technology | `sarvalabs/MOI-Website`, folder `blog/` | on `main` | `llms.txt`, `sitemap-index.xml`, `Article` and `FAQPage` JSON-LD present (`moi-blog/references/geo.md`) |
| launchpad.moi.technology | `sarvalabs/moi-agent-launchpad` (private, `master`) | PR #26 merged; docs PR #31 | On 2026-10-03 `llms.txt` pointed at `docs.moi.technology/docs/build/launchpad/`, which 404ed, and `/sitemap.xml` answered 500. The live `llms.txt` now points at `launchpad.moi.technology/docs` (the Launchpad docs, PR #31); re-check the sitemap |
| agents.moi.technology (the Agent Explorer), docs.wallet.moi.technology | `sarvalabs/agent-explorer`; wallet docs repo unknown | not in the sweep | The Agent Explorer answers 200 `text/html` to every file. Wallet docs: `robots.txt` and `llms.txt` 404. ASK: Rahul who owns the wallet docs |

Preview hosts (public, read on 2026-10-03): `geo-fixes.moichain-docs.pages.dev`, `geo-fixes.cocodocs.pages.dev`, `geo-fixes.voyage-docs.pages.dev` show the layer from the pull request branches (after the merges the production hosts carry it, so read those). A preview sends `x-robots-tag: noindex` and its robots and sitemap name the production host. Both are by design.

## The pieces
"Generated" means a script writes it on every build and git ignores it. Never hand-edit a generated file.

| Piece | What it is | On which sites | File that makes it | In git |
|---|---|---|---|---|
| `robots.txt` | Which crawlers may fetch, the sitemap address, and one `Content-Signal` line | Every site in the list above except the Agent Explorer and wallet docs | By hand: `static/robots.txt` (Docusaurus), `docs/source/_extra/robots.txt` (Sphinx), `public/robots.txt` (website), `blog/public/robots.txt` (blog). Generated by `next-sitemap.config.js` (Voyage app) and `app/robots.ts` (Launchpad) | Yes |
| `llms.txt` | One line per page: title, address, description, under a block "Instructions for AI agents" and a list of sibling sites | The four docs sites, the Voyage app, the website, the blog, the Launchpad | `scripts/generate-llms.mjs` reading each page's frontmatter and `llms.config.json`. Sphinx: `docs/generate_llms.py` (run `make llms`). By hand: `public/llms.txt` on the website, the Voyage app and the Launchpad. Blog: `blog/src/pages/llms.txt.js` | No on the Docusaurus sites. Yes for Sphinx and for the three hand-kept files |
| `llms-full.txt` | The full text of every page in one file | The four docs sites. The blog and the apps have none | The same script | Same |
| Markdown copy of each page | `<route>.md` and `<route>/index.md`, plain markdown | The four docs sites | The same script | Same |
| Site-wide structured data | `Organization` (id exactly `https://moi.technology/#organization`) and `WebSite` | The four docs sites, the Voyage app, the website (`index.html`), the Launchpad. The blog puts `Article` on each post | The `structuredData` plugin in `docusaurus.config.js`; `_templates/layout.html` (Sphinx); `src/pages/_document.js` (Voyage app) | Yes |
| Per-page structured data | `TechArticle` and `BreadcrumbList`, with `dateModified` from git | moidocs, voyage-docs, coco-docs by the injector; js-moi-sdk through `layout.html` | `scripts/inject-schema.mjs`, run after `docusaurus build`, editing the built HTML. `FaqSchema.jsx` and `HowToSchema.jsx` add `FAQPage` and `HowTo` on moidocs only | Script yes, output no |
| Sitemap | Every indexable page | Every site with a layer. The Launchpad's answers 500 today | Docusaurus writes it and leaves out pages marked `noindex`. By hand: `docs/source/_extra/sitemap.xml` (Sphinx), `public/sitemap.xml` (website). `next-sitemap` (Voyage), `@astrojs/sitemap` (blog), `app/sitemap.ts` (Launchpad) | Hand-kept ones yes |
| Response headers | A `Link` header on every response pointing at the API catalog, the skills index and `/llms.txt`; and `application/linkset+json` forced on the catalog, which has no file extension | moidocs, voyage-docs, coco-docs (no catalog line). The website's file works on Pages previews only | `static/_headers` (read by Cloudflare Pages only) | Yes |
| Redirects | 301 from old `/docs/...` addresses | coco-docs only | `static/_redirects` | Yes |
| Well-known catalog | `/.well-known/api-catalog`, a JSON linkset of API reference pages (RFC 9727) | moidocs, voyage-docs | `static/.well-known/api-catalog` | Yes |
| Agent skills index | `/.well-known/agent-skills/index.json`: name, download and documentation address of each skill package | moidocs, coco-docs | `static/.well-known/agent-skills/index.json` | Yes |
| Meta links | In the page head: canonical, `og:` and `twitter:` tags; on the website also `<link rel="llms-txt">` and `<link rel="service-meta">`, because its host ignores `_headers` | Every page of every site. The two `<link>` relations: the website | Docusaurus config, `layout.html`, `index.html`, `src/layouts/Meta.js` (Voyage app) | Yes |
| IndexNow key file | A text file at the site root whose name is its key (32 characters). Public by design, the same file everywhere | The docs sites, the Voyage app, the website and the Launchpad. Not the blog (whether it needs one: not recorded (the previous DevRel's notes); ASK: Rahul) | `static/<key>.txt`, `public/<key>.txt`, `docs/source/_extra/<key>.txt` | Yes |
| Share image | The card shown when a link is pasted; `themeConfig.image`, and on moidocs the `image` field of each page | Docs sites, Launchpad (`og-image.png`) | `static/img/`, `public/` | Yes |
| `404.html` | A real 404 where the host would otherwise answer 200 | js-moi-sdk docs | `docs/source/_extra/404.html` | Yes |

## What differs by framework
- Docusaurus 2.1 (moidocs, voyage-docs) and 3.9 (coco-docs): `npm run build` is `node scripts/generate-llms.mjs && docusaurus build && node scripts/inject-schema.mjs`. moidocs and voyage-docs share byte-identical scripts (checked with `diff` on 2026-10-03). coco-docs has a newer generator with `scripts/lib/docs.mjs`: it expands components, makes links absolute, orders pages as the sidebar does and adds a glossary `DefinedTermSet`. A fix in one generator is not a fix in the others.
- Sphinx (js-moi-sdk): nothing generates the sitemap; the generated files are committed (about 22,000 lines in PR #150), so review the script, not the output. The base address comes from `page_url` in `layout.html`. `html_baseurl` in `conf.py` makes every canonical point at a redirect, so it stays unset.
- Next.js (Voyage app): `next-sitemap` writes robots and the sitemap after each build. Its config emits one group per crawler, each repeating the private-path rules, and no Content-Signal line.
- React single-page app (website): crawlers that do not run JavaScript see an empty page, so `scripts/ssg.mjs` renders the four marketing routes to HTML after the build. The script came in with PR #57 (merged 2026-10-05); it was absent from `origin/main` on 2026-10-03. A new route needs an entry in `ROUTES` there, in `src/App.jsx` and in `public/sitemap.xml`.
- Astro (blog): see `moi-blog/references/geo.md`.

## Content signals
`Content-Signal: search=yes, ai-input=yes, ai-train=yes` states how content may be used: `search` for building a search index and results, `ai-input` for feeding content into an AI answer, `ai-train` for training. The docs sites carry all three as yes. `ai-train=yes` was set "per policy decision" (commit b4d4810, written 2026-09-09; the rebase of 2026-10-01 reset its committer date). Who decided is not recorded and whether it is still policy is unknown. ASK: Rahul before any change. Placement rules are in `crawlers.md`.

## A new docs site: what to copy
From the appendix of `DOCS-STYLE-GUIDE.md`, corrected where the committed files are newer. Do it in one pull request, then run `verify-locally.md`. Page rules for the new site are in `moi-docs/references/page-standard.md`.
1. `url` in `docusaurus.config.js` is the real production domain. It feeds every canonical and sitemap address. Sphinx: leave `html_baseurl` unset and set the base in `layout.html`.
2. Set `trailingSlash` in `docusaurus.config.js` and the same value in `llms.config.json`. If they differ, the `.md` addresses will not match the pages.
3. Copy `static/robots.txt` from moidocs and change only the `Sitemap:` line. The guide's list of named crawlers is out of date (`crawlers.md`).
4. Copy `scripts/generate-llms.mjs`, `scripts/inject-schema.mjs` and `llms.config.json` (Sphinx: `docs/generate_llms.py`; for the newer generator copy coco-docs' trio with `scripts/lib/docs.mjs`). Edit `baseUrl`, `routeBase`, `docsDir`, `siteTitle` and `summary`. Set the `build` script to the three steps. Add `static/docs/`, `static/llms.txt` and `static/llms-full.txt` to `.gitignore`. Copy the `structuredData` plugin and keep the `Organization` id exactly as it is.
5. Set `themeConfig.image` to a real branded image.
6. Copy `static/_headers`, and the `.well-known` files if the site has an API reference or a skill package. Copy the IndexNow key file.
7. Add the site to the `ecosystem` list of every other site and to the website's `public/llms.txt` (`discovery-files.md`).
8. Remove template leftovers: the `facebook/docusaurus` edit link, sample blog posts, the placeholder tagline, the default favicon and logo. coco-docs shipped 15 template addresses in its sitemap.
9. After the first deploy, `after-merge.md`.

## Not yet known
- Who owns the Cloudflare account and each Pages project, and the Search Console and Bing properties. ASK: Rahul.
- Whether Cloudflare's managed robots text on cocolang.dev will be added to the repo's file after the merge. ASK: Rahul, who can read the zone settings.
- How the js-moi-sdk docs site is built and deployed after a merge. ASK: Gokul.
