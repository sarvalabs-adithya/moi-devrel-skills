# Prove the layer works before a pull request

Facts are as of 2026-10-03. Run every command from the root of the working copy of the repo you are changing, with the branch checked out. Nothing here pushes, posts or deploys. CI does not check any of it: the docs-geo gate and the weekly geo-health cron were removed on purpose on 2026-09-09 ("no automated PR policing"). Do not add them back without asking (ASK: Rahul whether the preference still stands). Back to `../GUIDE.md`.

## Before the first build
1. `git status` is clean, or you can say what is not yours.
2. `git rev-parse --is-shallow-repository` prints `false`. If it prints `true`, read "The shallow-clone date trap" below first.
3. Node 16.14 or later for `moidocs` and `voyage-docs`, 18 or later for `coco-docs`. `npm install` once. GATE: it downloads the packages named in the lock file from the npm registry. Say so and ask once.
4. The docs sites need no secret and no environment variable; they build with none (sections 13.3, 14.3, 15.3 and 16.3 of `DEPENDENCIES.md`, the previous operator's handover file, which is on his machine only; ASK: Adithya for a copy). If a build asks for a key, stop and ASK: Adithya.

## Docusaurus sites (moidocs, voyage-docs, coco-docs)
Run `npm run build`. For coco-docs the README says `npm run build -- --no-minify` locally (a Tailwind minification problem); Cloudflare runs the plain command. The build runs three steps in order:
1. `scripts/generate-llms.mjs` deletes what it wrote last time (moidocs and voyage-docs: `static/docs/`; coco-docs: every `.md` under `static/`, so never keep a hand-written `.md` there), then writes `static/llms.txt`, `static/llms-full.txt` and a markdown copy of each page.
2. `docusaurus build`. Broken route links stop the build. Links to `.md` files only warn, and heading anchors are not checked on Docusaurus 2.1 (inferred).
3. `scripts/inject-schema.mjs` adds `TechArticle` and `BreadcrumbList` to each built page and skips a page that already has `TechArticle`.

Read the messages. Expected lines: `generated static/llms.txt (N lines) and static/llms-full.txt`, `emitted per-route .md files under static/`, `inject-schema: TechArticle + BreadcrumbList injected into N pages` (coco-docs words the first two differently). Any `generate-llms:` warning is a finding. A warning "still has a JSX component" means a new component must be added to `DROPPED_COMPONENTS` (moidocs, voyage-docs) or the `components` map (coco-docs), or raw JSX leaks into the markdown copies (it did, 265 lines of `llms-full.txt`, fixed in commit f639f41).

Then check the output in `build/`. Each line says what a good result looks like.

| Check | Command | Good |
|---|---|---|
| Index line count | The two commands under the table | The two numbers are equal (36 on moidocs and on coco-docs, 2026-10-03) |
| Agent block first | `sed -n 1,12p build/llms.txt` | Title, summary, "Instructions for AI agents", then the pages |
| Sitemap | `grep -o '<loc>[^<]*</loc>' build/sitemap.xml` | One host, the production one; no stub; no `markdown-page` |
| Stub in the index | Compare the sitemap with `build/llms.txt` | A page marked `noindex` is in neither. On 2026-10-03 the PR #124 preview listed the stub `networks` in `llms.txt` and `llms-full.txt` and served its `.md`, while the sitemap left it out |
| Page head | `grep -o 'rel="canonical" href="[^"]*"' build/docs/<path>/index.html` | Production host |
| Description | `grep -o '<meta[^>]*name="description"[^>]*>' build/docs/<path>/index.html` | Present, 140 to 160 characters |
| Structured data | `grep -o '"@type":"[A-Za-z]*"' build/docs/<path>/index.html` | `Organization`, `WebSite`, `TechArticle`, `BreadcrumbList`, plus `FAQPage` or `HowTo` on those pages |
| Markdown copy | `ls build/docs/<path>.md build/docs/<path>/index.md` | Both exist (coco-docs: root page only at `index.md`) |
| No raw JSX | `grep -c '^<[A-Z]' build/llms-full.txt` | 0, or only lines inside code samples |
| Root files | `ls build/robots.txt build/_headers build/.well-known/api-catalog build/.well-known/agent-skills/index.json` | Present where the site has them (`the-layer.md`) |
| Key file | `ls build/*.txt` | The 32-character IndexNow file is there |

The two commands of the first row, from the repo root. The first counts the pages listed in the built index, the second counts the page files:
```
sed -n '/^## Documentation/,/^## MOI ecosystem/p' build/llms.txt | grep -c '^- \['
find docs -type f \( -name '*.md' -o -name '*.mdx' \) | wc -l
```
`<path>` is the page route without the domain, for example `learn/fundamentals/account` on moidocs.

## js-moi-sdk docs (Sphinx), from the `docs/` folder
Needs Python with `sphinx`, `sphinx_js`, `sphinx_rtd_theme` and `jsdoc` (GATE: a download).
1. `rm -rf build && make html`. The clean build matters: otherwise other pages' navigation misses a new page.
2. `make llms` rewrites `docs/source/_extra/llms.txt`, `llms-full.txt`, `index.md` and each page's `.md`. These are committed. Run `git status` and review the script, not the 22,000 generated lines.
3. A new page needs three matching entries and nothing enforces it: the `.. meta:: :description:` in the `.rst`, a row in the `PAGES` table of `docs/generate_llms.py`, and a line in `docs/source/_extra/sitemap.xml` (no `.html`). The page must also be in the `toctree` of `index.rst`, or it builds and cannot be reached.
4. `grep -o '<title[^>]*>[^<]*' build/html/<page>.html`, then the description and `rel="canonical"` the same way. The canonical must have no `.html`.

## Voyage app and website
- Voyage app (`sarvalabs/voyage`): the Voyage team builds it. Its `build` script runs `next build` through `env-cmd` with a file under `env/`, and `next-sitemap` runs after it (the `postbuild` script) to regenerate robots and the sitemap from `next-sitemap.config.js` (its default output folder is `public/`, inferred). Claude does not open the `env/` files, and whether a build works on a newcomer's machine without the secrets the team passes at deploy is not recorded. ASK: Gokul before building it. To keep a private area out, add its path to `PRIVATE_PATHS` in the config. A `Disallow` alone does not keep an address out of the index. The `X-Robots-Tag: noindex, nofollow` header for `/admin` and `/setting` exists only as an uncommitted edit in the previous operator's clone. ASK: Adithya for a copy.
- Website (`sarvalabs/MOI-Website`): on the branch of PR #57, `npm run build` runs the blog index, `vite build`, the server build and `scripts/ssg.mjs`. On `main` it stops after the blog index and `vite build`, and there is no `ssg.mjs` (checked 2026-10-03). Its `package.json` records no Node version. Open `dist/manifesto/index.html` and look for the page's headline inside `<div id="root">`. If the root is empty, crawlers that run no JavaScript see nothing. The build fails loudly if a pattern in the template stops matching.

## The shallow-clone date trap
`dateModified` in the structured data is the committer date of the last commit that touched the page (`git log -1 --format=%cI -- <file>`). Cloudflare Pages builds from a shallow clone, where every file looks last changed in the newest commit. `inject-schema.mjs` tries `git fetch --unshallow`, and if that fails it leaves `dateModified` out and prints a warning.
- Your own clone is usually full, so a local build cannot show the trap. The preview can: `geo-check.sh` samples pages and warns when they all share one date.
- A warning is not proof of the trap. Rewriting history sets new committer dates. The commits of `geo-fixes` in `moidocs` all carry `2026-10-01T10:33:34` or `:35`, the day the AI co-author lines were removed from the history and the branch rebased (inferred cause). The PR #124 preview served `2026-10-01T10:33:35-04:00` on five sampled pages, and `git log` in a full clone gave the same value on 2026-10-03. So the preview did not show the trap there. Compare one page that the sweep did not touch.
- If your clone is shallow, `inject-schema.mjs` runs a network fetch during the build. Run `git fetch --unshallow` yourself first (GATE: it writes to your clone and reads from GitHub), or accept pages without `dateModified`.

## What a local build cannot show
| Not visible locally | Why | Where to see it |
|---|---|---|
| The `Link` header, the catalog's content type, redirects | `_headers` and `_redirects` are read by Cloudflare Pages. A local static server does not apply them (inferred; the preview shows them) | The preview URL, with `geo-check.sh` |
| Trailing-slash behaviour | On the moidocs and voyage-docs previews the host answers 308 from `/docs/build/json-rpc` to `/docs/build/json-rpc/` while the canonical has no slash (2026-10-03). coco-docs sets `trailingSlash: true` and matches | The preview. See `traps.md` |
| Whether crawlers are blocked | A zone-level Cloudflare setting blocked AI crawlers on cocolang.dev until 2026-09-09. A `pages.dev` preview sits outside the production zone (inferred) | The production host after the merge (`after-merge.md`) |
| A soft 200 | js-moi-sdk's host answers 200 to unknown paths | The live host. Check content types, never only status |
| Indexing, citations, rankings | They happen weeks later and elsewhere | Search Console, Bing, the visibility report (`measure.md`) |

## Prove it on the preview
1. After the pull request is open (GATE, `moi-devrel/ship`), Cloudflare comments with `<branch>.<project>.pages.dev`. The projects are `moichain-docs`, `cocodocs` and `voyage-docs`.
2. `bash "$SKILLS/moi-docs/geo/scripts/geo-check.sh" https://<branch>.<project>.pages.dev`. It finds the production host from the robots `Sitemap:` line and judges links against it.
3. Fix every FAIL. Read every WARN and write a reason next to the ones you keep. Paste the totals line in the pull request description.
4. js-moi-sdk has no preview. Its layer is first visible after the merge.

## Not yet known
- How the js-moi-sdk docs are built and where they are previewed. ASK: Gokul.
- Whether `trailingSlash` should be set explicitly on moidocs and voyage-docs, as the style guide's appendix says. Neither config sets it. ASK: Gokul, then the PR #124 author's reply.
