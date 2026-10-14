# Documentation sites and AI visibility (SEO, GEO)

## Read first

- **What this is.** Working notes on MOI's four docs sites (docs.moi.technology from `sarvalabs/moidocs`, cocolang.dev from `sarvalabs/coco-docs`, `sarvalabs/voyage-docs`, and the js-moi-sdk docs): how to write and review a page, the machine-readable layer (llms.txt, robots.txt, sitemap, JSON-LD), the open PRs, and how AI visibility is measured and reported.
- **What it was used for.** It fed the docs skill `skills/moi/moi-docs/` and its search and AI-visibility branch `skills/moi/moi-docs/geo/`. The last section is the original proposal (two skills named `moi-docs` and `moi-geo`); the built skill keeps the `moi-docs` name and puts the GEO material in a branch.
- **When it was written.** 2 October 2026. The events it covers run from 2 September to 2 October 2026; statements about PRs and live sites are as of 2 October 2026.
- **Who "I" and "the user" are.** "I" is the research assistant (Claude) that compiled the notes. "The user" is Adithya (DevRel).
- **Evidence key.** "(observed)" means a file, command or log shows it. "(inferred)" is my reading, not something the evidence states. "unknown" means the evidence does not say; the item is in Open questions.
- **Paths and citations.** Paths starting `~/` or `WT/` are on Adithya's Mac. Repo paths such as `moidocs/docs/...` are inside the local clones of the GitHub repos named above. Session-log and request-log cites (for example "session 466347ed", "user request 2026-09-22") point to files kept on Adithya's Mac and not in this repo; the session code is in https://github.com/moi-foundation/MOI-Webinars; transcripts are not in the repo. "DEPENDENCIES" and "FIX-PLAN" mean earlier working files on Adithya's Mac; their section numbers (for example "DEPENDENCIES 13.6.3") refer to that earlier layout. The current dependency list is `project-handover-docs/LIST-OF-DEPENDENCIES.md`, which is a rewrite with a different layout and does not carry those numbers, so check it for the current state. "Process N" refers to the numbered process headings in this file.
- **People.**
  - Adithya: DevRel, wrote most of the sweep and is the reference implementer.
  - Rahul: reviews and approves DevRel work and sets priorities; he reviewed moidocs #124 and sets direction on docs and releases (job title not stated).
  - Gokul: protocol team (js-moi-sdk); requested as reviewer on several PRs and owns Voyage content.
  - Robert Spendl: maintains Coco and its docs; approved coco-docs #12.
  - Abhinav Agarwalla: wrote the access-policy and storage-cost docs (moidocs #120); role not recorded in these notes.
  - Sai Kiran: asked to set up Wikidata; role not recorded in these notes.
  - Harsh Rastogi and Vinay: named as SDK team members; roles not recorded in these notes.
  - Scribble: the agency or campaign partner that wrote the article wave and the AI-visibility report (as used in these notes).
- **Jargon.** Terms are defined in the Glossary at the end.

Date of research: 2026-10-02. All four docs repos are on a local branch `geo-fixes` whose PR is still OPEN. The live sites are therefore still in their pre-sweep state (checked with curl, see Process 6).

## Sources read

Repos (local clones of `sarvalabs/moidocs`, `sarvalabs/coco-docs`, `sarvalabs/voyage-docs`, `sarvalabs/js-moi-sdk` and `sarvalabs/voyage`; paths below are relative to each repo):
- `moidocs/DOCS-STYLE-GUIDE.md` (419 lines, read in full; committed only in PR #124, commit 52f428e, 2026-09-22; it sits at the repo root, outside `docs/`, so the site does not publish it).
- `moidocs/scripts/generate-llms.mjs`, `moidocs/scripts/inject-schema.mjs`, `moidocs/llms.config.json`, `moidocs/static/robots.txt`, `moidocs/static/_headers`, `moidocs/static/.well-known/api-catalog`, `moidocs/static/.well-known/agent-skills/index.json`, `moidocs/package.json`, `moidocs/docusaurus.config.js`, `moidocs/sidebars.js`, `moidocs/README.md`, `moidocs/.gitignore`, `moidocs/src/components/FaqSchema.jsx`, `moidocs/src/components/HowToSchema.jsx`.
- moidocs pages read: concept `docs/learn/fundamentals/account.md`; tutorial `docs/build/tutorials/account-tutorial.md`; reference `docs/build/json-rpc.md`; plus `docs/guard/guardian-faq.md` (FAQ schema), `docs/learn/fundamentals/networks.md` (stub), `docs/build/moi-wallet.md`, `docs/build/skills/coco-skill.md`, category files.
- `coco-docs/` (same key files, plus `scripts/lib/docs.mjs`, `static/_redirects`, `docusaurus.config.js`, `sidebars.js`, `sidebar-book.ts`, `docs/book/glossary.md`, `docs/book/index.md`, `docs/book/getting-started/first.md`, `docs/book/language/state/state.md`, `docs/book/cli/compiler/compiler.md`, `docs/releases/index.md`, `src/components/DownloadButton/downloads.mjs`).
- `voyage-docs/` (same key files, plus pages `getting-started/getting-started.md`, `endpoint-docs/faucet.md`, `wallet-authentication/wallet-authentication.mdx`, both `_category_.json`).
- `js-moi-sdk/docs/generate_llms.py`, `docs/Makefile`, `docs/source/conf.py`, `docs/source/_templates/layout.html`, `docs/source/_extra/robots.txt`, `sitemap.xml`, `llms.txt`, `docs/source/getting-started.rst`, `index.rst`.
- `voyage/next-sitemap.config.js`, `voyage/public/llms.txt`, `voyage/next.config.js` (grep only) for the explorer app's GEO layer.
- `promptfooconfig.yaml` (the AI-visibility test suite, kept outside the repos on Adithya's Mac; secret lines excluded) and the promptfoo error logs (redacted).
- Git history of moidocs read-only: `git log main..geo-fixes`, and the retired files `742a2c2:DOCS-GEO-STANDARD.md`, `638258b:scripts/lint-docs-geo.mjs`, `ba13b20:.github/workflows/geo-health-check.yml`.

Other:
- The earlier `DEPENDENCIES.md` (sections 0, 13, 14, 15, 16, 17) and `FIX-PLAN.md` (section E), working files on Adithya's Mac (see Read first for the repo's current list).
- Community Call 14 deck and script: the cleaned copy in `skills/moi/moi-webinar/community-call/examples/cc14/` (`deck/index.html`, `README.md`, `SCRIPT.md`).
- `gh pr view` (read-only) on sarvalabs/moidocs #124, coco-docs #12, voyage-docs #5, js-moi-sdk #150, voyage #447: bodies, reviews, checks.
- The request log (kept on Adithya's Mac; grepped and read around the hits; each line is cut to about 413 characters, so long pasted messages are truncated there).
- The full session log of the docs sweep session (466347ed, 2026-09-02 to 09-22; kept on Adithya's Mac): the full 17 Sept call transcript with Rahul, the audit method, the tool-run results, the post-merge instructions, the draft status message. And the session log a8b46961 for the PR #120 verification report.
- The existing blog skill's `references/geo.md` (now `skills/moi/moi-blog/references/geo.md`), only to separate the blog's GEO from the docs' GEO.
- Read-only live checks with curl against the four docs hosts (2026-10-02).
- My own read-only audit scripts (python, no writes) over all frontmatter in the three Docusaurus repos and the `PAGES` table in `js-moi-sdk`.

I did not run any build (rule). Statements about build output come from the scripts' code, from the older local `build/` folders (dated 2026-09-22, stale), and from the PR bodies.

## Orientation: what exists

| Site | Repo | Framework | Pages live in | Address looks like | Cloudflare Pages project | Node |
|---|---|---|---|---|---|---|
| docs.moi.technology | sarvalabs/moidocs | Docusaurus 2.1.0 | `docs/learn`, `docs/build`, `docs/guard` (36 pages) | `/docs/learn/fundamentals/account` (no trailing slash) | `moichain-docs` | >= 16.14 |
| voyage-docs.moi.technology | sarvalabs/voyage-docs | Docusaurus 2.1.0 (package is still named "moidocs") | `docs/getting-started`, `endpoint-docs`, `wallet-authentication` (6 pages) | `/docs/endpoint-docs/faucet` | `voyage-docs` | >= 16.14 |
| cocolang.dev | sarvalabs/coco-docs | Docusaurus 3.9, `routeBasePath: '/'` | `docs/book`, `docs/install`, `docs/releases` (36 pages) | `/book/language/state/` (trailing slash) | `cocodocs` | >= 18 |
| js-moi-sdk.docs.moi.technology | sarvalabs/js-moi-sdk, folder `docs/` | Sphinx + sphinx_js + sphinx_rtd_theme | `docs/source/*.rst` (10 pages) | `/getting-started` | Cloudflare Pages per PR #150 text; project name and build pipeline unknown | Python |

Sources: style guide table; DEPENDENCIES sections 13 to 16; configs. docs.wallet.moi.technology was in the original sweep list but the user said "forget wallet for now" (2026-09-02), its repo is not on disk and the style guide does not cover it. Its status is unknown.

Related but not a docs site: the Voyage explorer app (`voyage` repo, PR #447) got a "front door" GEO layer built with next-sitemap and a meta component.

Who (observed):
- Adithya wrote the largest share of the sweep (17% to 46% of each repo's commits: moidocs 38 of 154, coco-docs 38 of 83, voyage-docs 22 of 128; DEPENDENCIES sections 13 to 15).
- Reviewers named in evidence: Rahul (moidocs #124, CHANGES_REQUESTED 2026-09-17, "We should not include Lauchpad docs here lauchpad is just an app which uses moi"); Gokul (requested on moidocs #124, js-moi-sdk #150, voyage #447; owns Voyage content); Robert Spendl (maintains Coco and its docs; APPROVED coco-docs #12 on 2026-09-29 after rebasing it to v0.9.2). Abhinav Agarwalla wrote the access-policy and storage-cost docs (moidocs #120) and other tutorials; Sai Kiran was asked to set up Wikidata. Rahul's job title is not stated; he sets direction on docs and releases (a memory file calls the 2026-09-14 corrections "the founder's"; the notes infer this means Rahul, which is unconfirmed).
- Hosting, Cloudflare, Search Console and Bing owners: "owner: confirm" in DEPENDENCIES.

Timeline (observed from user requests and commits): audit 2026-09-02 to 09-09; standard drafted 09-08/09; PRs raised 09-09 to 09-14; call with Rahul 09-17 (rework the guide); guide rewritten and committed 09-22; Robert's approval 09-29; fixes, rebase and push 10-01.

Current PR state (observed via `gh pr view`, 2026-10-02):

| PR | State | Review | Check |
|---|---|---|---|
| moidocs #124 "SEO/GEO/AEO pass" (52 files, +1083 -135, 33 commits) | open | Rahul CHANGES_REQUESTED (met by commit 75f608b but not yet re-reviewed), Gokul requested | Cloudflare Pages green |
| coco-docs #12 "GEO overhaul" (65 files) | open | Robert APPROVED | Cloudflare Pages green |
| voyage-docs #5 (21 files) | open | none requested | Cloudflare Pages green |
| js-moi-sdk #150 (40 files, 22,549 added lines, mostly generated) | open | Gokul requested | "Run Tests" green; no preview exists |
| voyage #447 (7 files) | open | Gokul requested | no checks |

---

## Process 1: Write or edit a page on a Docusaurus site (moidocs, voyage-docs, coco-docs)

### Purpose
Publish documentation that a reader, a search engine and an AI assistant can all use: one citable definition paragraph, hand-written metadata, stable anchors, canonical names.

### Trigger or cadence
Any time a protocol, SDK or product change needs documenting; a new Coco release (Process 9); a review comment. No fixed cadence. Release-driven (inferred).

### Who
Any author (DevRel, SDK team, Voyage team). Adithya is the reference implementer. The style guide is "for anyone who writes, edits, or reviews a page".

### Inputs needed before starting
- Which site and folder (table above).
- The source of truth for every claim (go-moi, js-moi-sdk, PISA/Coco source; see Process 4 and the rule "verify every claim against the repository source", user request 2026-09-09).
- Node installed (16.14+ for moidocs and voyage-docs, 18+ for coco-docs) and `npm install` run once in the repo.
- A neighbouring page in the same folder to copy conventions from (the guide tells authors to do this for the title choice).

### Steps in order
1. Locate the file. moidocs and voyage-docs: `docs/<section>/<page>.md`. coco-docs: `docs/book/<chapter>/<page>.md` (plus `docs/install`, `docs/releases`). The guide says coco pages live under `docs/book/` only; `docs/install/index.md` and `docs/releases/index.md` also exist (observed).
2. Choose `sidebar_position`. Pages and subfolders share one list.
   - List the numbers in use: `grep -h "^sidebar_position:" docs/<folder>/*.md*` and `grep -h '"position"' docs/<folder>/*/_category_.json`. Numbers need not be consecutive.
   - If you create a folder, add `_category_.json` (the guide only says "add a `_category_.json`").
   - In practice the folders use `link.type` `doc` or `generated-index`; a `generated-index` carries a `link.description` of 140 to 160 characters (moidocs guard 143, fundamentals 144; voyage-docs 150 and 146) (observed; this category-description rule is NOT in the guide).
3. Write the frontmatter. The file must start with `---` on line 1; a blank line above it makes the site ignore the whole block. Contract:

   | Field | Needed | Rule |
   |---|---|---|
   | `title` | yes | Page's own name, a few words, no version number, no date (unless a changelog entry). Site appends its name; results truncate near 60 characters. coco-docs exception: Book pages carry chapter numbers, e.g. `2.7 Logic and Actor State`, and the `# H1` omits them. |
   | `description` | yes | 140 to 160 characters (130 to 170 acceptable; never pad or cut to hit a number). Statement, not teaser. If it contains a colon followed by a space, wrap the whole value in double quotes or the build fails (YAML). Count with `wc -m`. |
   | `sidebar_position` | yes | see step 2 |
   | `image` | moidocs only | `/img/moi-card-learn.png` under `docs/learn/`, `/img/moi-card-build.png` under `docs/build/`, `/img/moi-card-guard.png` under `docs/guard/`; elsewhere omit |
   | `keywords` | no | Google ignores it. Keep existing ones; on a new page 5 to 10 searchable terms are allowed |

4. Write the opening paragraph: one paragraph saying what the thing is, before prerequisites or history, readable alone. Good example: first paragraph of `moidocs/docs/learn/fundamentals/account.md`. Bad example in the guide: "Before diving into accounts, it's worth understanding...".
5. Title and headings. One main title. Two valid ways (both exist): first body line `# Title` equal to the frontmatter title, or none and let the site show the frontmatter title; copy the neighbours. voyage-docs leaves the H1 out; coco-docs writes `# Title`. Use `##` and `###`. Phrase a heading as a question only where the section answers that question (`## What is an Account ID? {#account-id}`), not for "Prerequisites" or "Anatomy of an Account".
6. Preserve anchors when rewording a heading: `## How do I upgrade MOIPod to the latest version? {#upgrading-moipod-to-the-latest-version}`. Docusaurus derives the anchor from the heading text, so changing the text changes the anchor. If you must change an anchor: `grep -rn "old-anchor" .` from the repo root, fix every hit in the same change, and search the `sarvalabs` GitHub org for the old anchor (other MOI sites link in).
7. Use the naming table in titles, headings, body and alt text: MOI; MOI Wallet; Coco (first mention on a page "Coco (also known as Cocolang)", then "Coco"; never CoCo or CocoLang); js-moi-sdk (always lowercase, even at sentence start, rephrase instead); MOIPod (not Moipod); Voyage; Sarva Labs (not SarvaLabs). Commands, package names, URLs and code keep their real spelling (`moipod`, `npm install js-moi-sdk`). Tagline word for word where space allows: "The participant layer for AI agents."
8. Decide whether the page is a stub (the reader finishes with the question unanswered, or there is any placeholder or TODO; if unsure, say so in the PR description).
   - Mark a stub directly after the frontmatter: `<head><meta name="robots" content="noindex" /></head>` (moidocs, voyage-docs; multi-line form in the guide) or `unlisted: true` in frontmatter (coco-docs). This keeps the page out of search and out of the sitemap.
   - Remove the mark in the same change that adds content; nothing warns you if you forget.
   - Real example: `moidocs/docs/learn/fundamentals/networks.md` (reset to a "Coming Soon" stub on 2026-09-09 until the team writes the real content).
9. moidocs only, FAQ or tutorial pages: add structured data components.
   - Tutorial: `import HowToSchema from '@site/src/components/HowToSchema';` then `<HowToSchema name="..." steps={[{"name": "...", "text": "..."}, ...]} />` (example: `docs/build/tutorials/account-tutorial.md`).
   - FAQ: `import FaqSchema from '@site/src/components/FaqSchema';` then `<FaqSchema faqs={[{q: "...", a: "..."}, ...]} />` (example: `docs/guard/guardian-faq.md`).
   - Put import and call at the top of the body; do NOT also write a `# Title` line (two titles appear); no blank line inside the call (it may span lines but every line needs content).
   - A tutorial means a page that walks through actions in order, not a reference page with numbered sections.
   - voyage-docs and coco-docs have no such components; write FAQs and tutorials as ordinary pages there.
10. Link to other pages by site-root address starting with `/`, e.g. `/docs/build/tutorials/account-tutorial`, never with the domain (a preview build would send readers to the live site). Per-site forms: moidocs `/docs/build/json-rpc`; voyage-docs `/docs/endpoint-docs/faucet`; coco-docs `/book/language/state/` with trailing slash. Existing relative links that work stay as they are.
11. If the page is an API reference: add an entry to `static/.well-known/api-catalog` (moidocs, voyage-docs), copying the shape of the existing entries. If it is an agent skill package: add to `static/.well-known/agent-skills/index.json` (moidocs, coco-docs). Otherwise skip (Process 9).
12. Preview locally: `npm run start` (voyage-docs binds port 6420; coco-docs says http://localhost:3000). To see the generated machine files and schema, run `npm run build` (which is `node scripts/generate-llms.mjs && docusaurus build && node scripts/inject-schema.mjs`) and open `build/llms.txt`. coco-docs README says to run `npm run build -- --no-minify` locally because of a Tailwind minification problem; Cloudflare runs plain `npm run build`.
13. Open a PR (Process 12). Cloudflare Pages comments on it with a preview URL (`<hash>.moichain-docs.pages.dev` and `<branch>.moichain-docs.pages.dev`, observed on #124). Merging to `main` publishes; there is no manual deploy.

When UPDATING an existing page (the guide's list): description still describes the page; opening paragraph still true; names in the lines you touched follow the table; reworded headings kept their anchors; a finished stub lost its mark. You never edit llms.txt, the sitemap, the sidebar or structured data; `dateModified` comes from git history.

Moving or renaming a page changes its address and 404s old links unless a redirect exists; before moving, "ask whoever manages the site's hosting how redirects are set up". coco-docs has `static/_redirects`; moidocs and voyage-docs have none (observed).

### Deliverables and where they end up
The `.md` source in the repo; a PR with a Cloudflare preview; after merge the live page. Build also produces (not committed): `llms.txt`, `llms-full.txt`, the page's `.md` copies, the sitemap entry, JSON-LD.

### Accounts and tools
GitHub (his work GitHub account; `gh` signed in as that account), Node and npm, Cloudflare Pages (builds automatically; no login needed to author). No secrets: "Env vars: none. The site builds with no secrets." (DEPENDENCIES 13.3).

### Quality rules and house style
Seven rules (the guide's core): (1) hand-written title and 140 to 160 character description; (2) one opening paragraph that says what the thing is; (3) one main title, question headings only where honest; (4) keep old anchors; (5) exact product names; (6) mark unfinished pages, unmark when finished; (7) never hand-edit generated files. Plus: every claim checked against the source repo; short, direct sentences without metaphors (user 2026-09-09: "no metaphors no random AI shit, real, direct, efficient"); run the humanizer and stop-slop skills on prose and only identify changes when asked (user 2026-09-11 "for the latter 2 dont make any changes just identify").

### Traps and silent failures
See Traps section. The big ones: unquoted colon in description fails the build; blank line before `---` silently drops metadata; reworded heading silently breaks inbound anchors (Docusaurus 2.1 does not check anchors, inferred); a finished page still marked noindex never appears in search; manual `# Title` plus schema component shows two titles.

### Time
Unknown for one page. The five-site sweep took about a week of elapsed time with sub-agents (2026-09-02 to 09-09 audit and fixes).

### Open questions
Which pages should get HowToSchema retroactively (Open questions 9); trailingSlash configuration (Open questions 7).

---

## Process 2: Write or edit a page on js-moi-sdk docs (Sphinx)

### Purpose
Same seven rules, different files. The site is Sphinx with autodoc (sphinx_js + jsdoc), so API blocks come from source comments.

### Trigger or cadence
SDK releases and doc changes. The repo version is `v0.9.0-rc3` in `docs/source/conf.py` (`version` and `release`; `release` feeds the SoftwareApplication `softwareVersion` JSON-LD on the index page).

### Who
SDK team (Gokul, Harsh Rastogi, Vinay) plus Adithya for the GEO layer.

### Inputs
Python with sphinx, sphinx_js, sphinx_rtd_theme and jsdoc (same toolchain as the HTML build). Run all commands from `docs/`.

### Steps in order (from the guide, verified against the files)
1. Create `docs/source/<page>.rst`. First lines: `.. meta::` then `   :description: Your 140 to 160 character description.` (plain text; a colon needs no quotes).
2. Add the page name (no `.rst`) to the `toctree` in `docs/source/index.rst`. A page left out builds but is unreachable.
3. Add a row to the `PAGES` dict at the top of `docs/generate_llms.py`: `"name": ("Title", "same description")`. The file's own comment says the table "is checked by eye in PR review".
4. Run `make llms` (runs `python3 generate_llms.py`: a Sphinx text-builder pass into a temp dir, then writes `docs/source/_extra/llms.txt`, `llms-full.txt`, `index.md`, `<page>.md` and `<page>/index.md`). Run `git status` and commit them all: on this site generated files ARE committed (about 22,000 lines in PR #150).
5. Add the page's address to `docs/source/_extra/sitemap.xml` by hand (`<url><loc>https://js-moi-sdk.docs.moi.technology/<page></loc></url>`, no `.html`).
6. To keep an old anchor, put a target above the heading: `.. _installing:` then the new question heading with its underline. The old anchor is the old heading lowercased with hyphens.
7. Check: `rm -rf build && make html` (the clean build matters, otherwise navigation on other pages does not pick up the new page). Then `grep -o '<title[^>]*>[^<]*' build/html/<page>.html`; `grep -o 'content="[^"]*" name="description"' build/html/<page>.html`; `grep -o 'rel="canonical" href="[^"]*"' build/html/<page>.html`; open `build/html/index.html` and confirm the page is in the nav.
8. Deploy and preview: "Ask the SDK maintainers" (guide). PR #150 has no preview; Test workflow is the only check.

I verified on 2026-10-02 that `PAGES`, each `.rst` `.. meta::` description, the `toctree` and `sitemap.xml` agree exactly for all 10 pages (description lengths 142 to 160).

### Deliverables
`.rst`, regenerated `_extra/*`, the sitemap line.

### Accounts and tools
GitHub; the main repo is public (`sarvalabs/js-moi-sdk`), PRs come from a fork under his work GitHub account. No secrets for docs. The publish workflow (npm, R2 skill zip) uses `npm_token`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ACCOUNT_ID`, `R2_BUCKET`, `R2_PREFIX`, owned by the SDK team and DevOps, not DevRel.

### Quality rules
As above. `layout.html` builds canonicals without `.html`: do NOT use `html_baseurl` in `conf.py` because it appends `.html` and points every canonical at a 308 redirect. `html_title` is version-free on purpose so titles do not go stale each release.

### Traps
Description in the `.rst`, the `PAGES` row and the sitemap line are three places that must agree and nothing enforces it. Hosting soft-200s unknown paths (see Process 6). The generated files make the PR huge, so review the script not the output.

### Open questions
How the site is built and deployed after merge (unknown); whether to stop committing generated files like the other sites (DEPENDENCIES 16.6.2 offers this as a choice).

---

## Process 3: Review a docs PR (a derived checklist: the style guide's own review section was removed on 22 September 2026)

### Purpose
Catch the mistakes that the build cannot catch, before merge.

### Trigger
Every docs PR.

### Who
Observed: Rahul (reviewed #124), Gokul (requested on #124, #150, #447; owns Voyage content), Robert (reviewed and fixed #12). Authors may use AI but "should know whether the outcome that they produce is right or wrong" (Rahul, 2026-09-17 call).

### Inputs
The PR diff, the Cloudflare preview link, `DOCS-STYLE-GUIDE.md`.

### Steps (inferred: assembled from the guide's rules, its "Update an existing page" list and its "Common mistakes" table; the guide itself has no reviewer section)
Evidence that the review section was removed: user request 2026-09-22 "rm step 7 and 10 When you review a docs PR / How to check your page". The guide now ends with "Common mistakes" and an appendix.
1. Open the preview and click the changed pages.
2. In the diff check each page: frontmatter first line is `---`; `title` short, no version; `description` present, 140 to 160 characters (130 to 170 tolerated), quoted if it has `: `; `sidebar_position` set; `image` correct on moidocs; stub marks present or removed correctly.
3. Opening paragraph defines the thing and stands alone.
4. Headings: one main title; no `# Title` next to a Faq or HowTo schema component; reworded headings carry `{#old-anchor}`; if an anchor changed on purpose, check that every inbound link was updated.
5. Names follow the table (quick grep: `grep -rnE "Moipod|MoiWallet|Moi Wallet|JS-MOI-SDK|CocoLang|SarvaLabs" docs`).
6. Links start with `/` and match the site's form.
7. New API reference or skill package has its `.well-known` entry.
8. If config or hosting changed: `curl -A "GPTBot/1.0" -I https://<domain>/` still returns 200 (retired standard's rule; the guide keeps it only for after a crawler change).
9. Generated files are not edited and not committed (except js-moi-sdk).
10. Facts: spot-check every changed claim against the source repo (Process 4).

### Deliverables
Review comments on the PR, approval or CHANGES_REQUESTED.

### Quality rules from reviewers (corrections)
- Rahul 2026-09-17: do not put an application (Agent Launchpad) into protocol docs ("tomorrow launch pad may shut down"); application docs belong with the app, with use cases on the moi.technology website; backlinks are fine. Result: commit 75f608b removed the Launchpad section.
- Rahul 2026-09-17: the guide must be written for humans, explain what to do and why, cover "creating a new page" and "updating a page", and explain how llms.txt gets generated. Result: the 2026-09-22 rewrite.
- Robert 2026-09-29: page titles "Coco - Context-Oriented Programming Language for MOI" were too long for browser tabs; changed back to "Coco"; the long form stays on the home page (`docs/book/index.md` overrides `<title>` in a `<head>` block).

### Time
Unknown.

### Open questions
Who has merge rights and who must approve each repo (unknown). Whether Gokul has reviewed #124 (DEPENDENCIES says requested, not yet reviewed).

---

## Process 4: Fact-check a teammate's docs PR against source (the PR #120 pattern)

### Purpose
Defend review findings with evidence, line by line.

### Trigger
A teammate's docs PR touching technical claims (observed: Abhinav's moidocs #120 access policy and storage costing, 2026-08-21; also used as a double check for the release blog).

### Who
Adithya with Haiku sub-agents (user: "use haiku actually its faster and way cheaper, I cant blow all my credits"). Note: memory says "no multi-agent workflows" except when the user asks, and he did ask for Haiku/Sonnet here.

### Inputs
The PR head ref; go-moi v0.12.0 and js-moi-sdk v0.8.0 source on disk (memory: MOI source is local and readable); links the PR cites.

### Steps (observed from requests and the pasted verdict; some orchestration steps are inferred)
1. Check out the PR head locally; build a "verified fact pack" of already-verified facts (the assistant extracted 52).
2. Fan out sub-agents (Haiku) to verify each claim in each changed file against source (Go handlers such as `compute/ixstorage.go`, SDK `toRawOperation`, `moi.StoragePricing` wire names).
3. Run a refutation pass ("refute was already done"): try to prove each finding wrong.
4. Produce a per-file table: claim, result, evidence with file and line (example verdict at the 2026-08-21 message: storage-cost 6 findings, json-rpc 7, access-policy 5, submit-ixn 4, access-control 3).
5. Reconcile counts before reporting: the headline "27 errors" did not match the write-up (table 8 breaking + 18 minor = 26; numbered list 25). The assistant flagged it. Counts must match.
6. Walk the user through findings one at a time, breaking vs minor, with "is there any way it could be correct" for each.
7. Run the branch locally on localhost so the user can check claims himself.
8. Draft the PR comment in the user's format: `Issue N: what the issue is, why it is an issue, where the issue is, suggested fix`; send the 8 critical issues first, then the next 16 after review.
9. Deliver as "just a simple md file", no artifact, "dont post anything" (user posts himself).

### Deliverables
A local markdown report; a drafted PR comment. I did not find the report file on disk (unknown path).

### Traps
Count mismatches; typos that look like bugs (ticker vs tick) need a plain-language "before and after without paragraphs" explanation; never post or push for him.

### Open questions
Where the report lives; whether the same method was applied to #123 or #126 (unknown).

---

## Process 5: Build and verify the GEO layer locally ("check it still works")

### Purpose
Prove that the machine-readable layer (llms files, markdown copies, sitemap, JSON-LD, robots, headers, `.well-known`) is intact after a content or config change.

### Trigger
Before opening or updating a docs PR; after any config, hosting or Cloudflare change; after a rebase.

### Who
DevRel author. No automation: the CI gate (`docs-geo.yml` plus `scripts/lint-docs-geo.mjs`) and the weekly `geo-health-check.yml` cron were deliberately removed on 2026-09-09 ("no automated PR policing", "no scheduled monitoring: live-site issues get handled as they surface", commits d0b6a19 and 77059a7; user: "no rm this lets just keep regular docusaurus and deal with issues case by case"). Do not re-add them without asking.

### Inputs
Repo checked out, `npm install` done.

### Steps in order (Docusaurus sites)
1. `npm run build` in the repo root. It runs, in order: `scripts/generate-llms.mjs`, `docusaurus build`, `scripts/inject-schema.mjs`.
   - Generator:
     - deletes `static/docs/` (coco-docs: every `.md` under `static/`), reads `llms.config.json`, walks `docs/`;
     - writes `static/llms.txt`, `static/llms-full.txt`, and each page's markdown at `static/<route>.md` and `static/<route>/index.md`;
     - reads title and description by a simple line-based frontmatter parser (`^([\w-]+):\s*(.*)$`), so multi-line YAML for those two fields would break it (inferred; all current pages use one-line values);
     - strips MDX imports and dropped components only outside code fences, turns Tabs into labelled blocks, and warns "still has a JSX component" if any capitalized component remains.
   - Injector:
     - needs `build/<routeBase>/` and reads each built `index.html`;
     - skips pages that already contain `"@type":"TechArticle"` (idempotent);
     - decodes HTML entities and escapes `<` in JSON;
     - takes `dateModified` from `git log -1 --format=%cI -- <file>`; if the clone is shallow it runs `git fetch --unshallow`, and if that fails it omits `dateModified` and warns.
2. Read the build output messages: `generated static/llms.txt (N lines)`, `emitted per-route .md files`, `inject-schema: TechArticle + BreadcrumbList injected into N pages`, and any `generate-llms:` warning. The build also fails on `onBrokenLinks: 'throw'` (route links). Markdown-file links only warn (`onBrokenMarkdownLinks: 'warn'`), and broken heading anchors are not checked on Docusaurus 2.1 (inferred).
3. Open `build/llms.txt`: one line per page, `- [Title](URL): description`; the "Instructions for AI agents" block precedes "Documentation"; "MOI ecosystem" follows.
4. Check the sitemap: `grep -o "<loc>[^<]*</loc>" build/sitemap.xml`. It must contain no stub, no sample page, no other domain. (The older local moidocs build dated 2026-09-22 still listed `https://docs.moi.technology/markdown-page`, the template sample; commit bcbcbf8 removed that page.) A stub marked noindex must be absent (observed: `networks` absent).
5. Check one page's head: `grep -o 'rel="canonical" href="[^"]*"' build/docs/<path>/index.html`, `grep -o 'name="description" content="[^"]*"' ...`, `grep -o '"@type":"[A-Za-z]*"' ...` (expect Organization, WebSite from the site-wide plugin, TechArticle, BreadcrumbList, plus HowTo or FAQPage on those pages).
6. Check the markdown copy exists: `build/docs/<path>.md` and `build/docs/<path>/index.md` (coco-docs: `build/<route>.md`, root page only at `/index.md`).
7. Check `build/robots.txt`, `build/_headers`, `build/.well-known/api-catalog`, `build/.well-known/agent-skills/index.json`, and the IndexNow key file at the build root.
8. Source-side checks I ran as read-only audits (use as a script; the drift sweep, Process 13, and the proposed `check_pages.py` describe it): description length band, unquoted colons, missing `image` on moidocs, `# H1` next to schema components, stubs.
9. On js-moi-sdk: `rm -rf build && make html`, then `make llms`, then `git status`, then Process 2 step 7.
10. On the live site, after deploy: Process 6.

### Deliverables
Local `build/` folder (git-ignored). Nothing committed except js-moi-sdk's `_extra/`.

### Quality rules
One generated file never edited by hand; `trailingSlash` in `docusaurus.config.js` and `llms.config.json` must match or the `.md` addresses in llms.txt will not match the pages.

### Traps
- `static/docs/`, `static/llms.txt`, `static/llms-full.txt` are git-ignored (moidocs and voyage-docs). coco-docs ignores `static/**/*.md`, `static/*.md`, `static/llms.txt`, `static/llms-full.txt`; a stray untracked `static.md` sits in the coco-docs repo ROOT (left by an older build; DEPENDENCIES 14.6.3 says delete it). `.gitignore` does not cover it.
- Adding a new JSX component to a page: also add it to `DROPPED_COMPONENTS` in `scripts/generate-llms.mjs` (moidocs, voyage-docs) or to the `components` map in coco-docs, otherwise raw JSX leaks into the markdown copies (this happened: 265 lines in llms-full.txt, fixed in f639f41).
- The two generator versions differ: moidocs and voyage-docs share the older single-file scripts (identical, verified with `diff`); coco-docs has a newer version with `scripts/lib/docs.mjs` (handles components, absolute links in the markdown copies, glossary DefinedTermSet, sidebar-order). If you change one, copy to the others (DEPENDENCIES 15.5).
- Cloudflare builds from a shallow clone; without the unshallow step every page shows the head commit's date as `dateModified`.
- The generated header comment in `generate-llms.mjs` still names "DOCS-GEO-STANDARD.md", which was retired (observed line 4).

### Time
Not recorded. Post-merge checks are described as "2 minutes" in PR #150.

### Open questions
None specific beyond Open questions 7 and 8.

---

## Process 6: After a GEO or docs PR merges (manual steps nothing automates)

### Purpose
Make search engines and AI crawlers actually see the change.

### Trigger
Each merge to `main` of a docs repo, and especially the first merge of the sweep PRs.

### Who
Adithya (and the owners of the Search Console, Bing and Cloudflare accounts, "owner: confirm").

### Steps in order (observed from the PR bodies, DEPENDENCIES, and the session)
1. Let Cloudflare Pages finish the production build (no action).
2. Confirm AI crawlers get 200 and not a Cloudflare challenge: `curl -A "GPTBot/1.0" -I https://<domain>/` then `ClaudeBot/1.0` and `PerplexityBot/1.0`. I ran this on 2026-10-02: all four live hosts return 200 to all three UAs.
3. Confirm the machine files are real files and not the SPA fallback. Check status AND content type: `curl -s -o /dev/null -w "%{http_code} %{content_type}\n" https://<domain>/robots.txt` expecting `200 text/plain`, and `/llms.txt`. On 2026-10-02 (pre-merge): docs.moi.technology and voyage-docs return 404 for both; cocolang.dev returns 200 `text/plain` for robots.txt (24 lines that are only a content-signals comment block, inferred to be Cloudflare's managed text; no `User-agent` rules, no sitemap line) and 404 for llms.txt; js-moi-sdk returns 200 `text/html` for robots.txt, llms.txt and a nonexistent path (the soft-200 fallback).
4. Confirm 404 behaviour on js-moi-sdk: `curl -sI https://js-moi-sdk.docs.moi.technology/nonexistent-page` should return 404 once `404.html` is deployed (PR #150).
5. View source on a page: canonical on the right host and JSON-LD present.
6. coco-docs only: `curl -sI https://cocolang.dev/docs/book/` returns 301 to `/book/`; `curl -s https://cocolang.dev/ | grep rel="canonical"` shows `https://cocolang.dev/`.
7. coco-docs only: add the Cloudflare redirect rule `cocolang.docs.moi.technology/*` to `https://cocolang.dev/*` with 301 (dashboard action; the cocolang.docs.moi.technology mirror serves a duplicate).
8. Resubmit the sitemap in Google Search Console for each property (js-moi-sdk: replaces the stale v0.7.0-rc1 index).
9. Bing Webmaster Tools: "Import from Google Search Console" (one OAuth click, brings verification). The user reported he finished Bing on 2026-09-09. Bing's index feeds ChatGPT search and Copilot.
10. IndexNow: the key file (a 32-hex-character filename at the site root, same file on all six sites, public by design) is committed. "Nothing submits the IndexNow key automatically either" (DEPENDENCIES 13.6.3). The assistant said the ping is a "one-command step"; the exact command is not recorded (unknown). The standard endpoint is `https://api.indexnow.org/indexnow` (inferred).
11. Update the PR descriptions that went stale (Process 12).
12. Delete the local backup branches left from rebases (`geo-fixes-before-rebase-oct1`, `geo-fixes-before-attribution-rewrite` in moidocs; DEPENDENCIES lists backups in each repo).

### Deliverables
Evidence in the terminal (status codes), Search Console and Bing submissions.

### Accounts and tools
Cloudflare dashboard (login), Google Search Console (login), Bing Webmaster Tools (Microsoft or Google login), `curl`. No key beyond logins. Search Console property owner for docs.moi.technology, cocolang.dev, voyage-docs: "owner: confirm".

### Quality rules
Never trust a bare 200 on js-moi-sdk; check content type and body.

### Traps
Merge order: merge moidocs #124 before the MOI-Website PR #57 (DEPENDENCIES 13.6.2). After coco-docs merges, 15 old addresses return not found on purpose: the sample blog and sample page. A Cloudflare WAF or bot-fight setting can silently block AI crawlers: cocolang.dev was returning 403 to AI crawlers until the user switched the zone setting off on 2026-09-09 (user: "i switched cocolang.dev btw its no longer blocking").

### Time
"2 minutes" (PR #150 text); Bing about 5 minutes (assistant estimate).

### Open questions
Exact IndexNow command; which Search Console properties exist; whether Cloudflare's managed robots.txt on cocolang.dev will prepend its own content-signal block to the repo's file and override `ai-train=yes` after merge (the live file on 2026-10-02 is only that managed block; unknown).

---

## Process 7: Allow or block an AI crawler (edit robots.txt)

### Purpose
Control which crawlers may read a docs site.

### Trigger
A policy decision; a crawler change by an AI vendor; setting up a new site.

### Who
DevRel with whoever owns the policy (the `ai-train=yes` signal was set "per policy decision", commit b4d4810; who decided is unknown).

### Inputs
`static/robots.txt` of each site (moidocs, voyage-docs, coco-docs); `docs/source/_extra/robots.txt` (js-moi-sdk); `voyage/next-sitemap.config.js` (explorer).

### Steps
1. Current file (identical across the three Docusaurus sites except the comment header and `Sitemap:` line; verified with `diff`):
   ```
   User-agent: *
   Content-Signal: search=yes, ai-input=yes, ai-train=yes
   Allow: /
   Sitemap: https://<domain>/sitemap.xml
   ```
   It is deliberately ONE group. The file's comment explains: Content-Signal must sit inside a User-agent group, and a crawler obeys only the most specific group that names it, so a per-crawler group would take that crawler out of the `*` group and drop the signals for it (commit 7d58640, 2026-10-01).
2. To create the file for a new site: copy `moidocs/static/robots.txt` into the new site's `static/`, change only the `Sitemap:` line.
3. To block or allow one named crawler (inferred procedure, see discrepancy below): add a new group with the crawler's `User-agent:` line, its `Disallow: /` or `Allow: /`, and copy the `Content-Signal:` line into that group, since the named group replaces `*` for that crawler. Do this in every site that should change.
4. After deploy: `curl -A "<crawler name>" -I https://<domain>/` returns 200 for an allowed crawler (guide).
5. js-moi-sdk keeps the same content in `docs/source/_extra/robots.txt` (served through `html_extra_path`).

### Discrepancy to resolve before writing the skill
The guide's "Allowing or blocking a crawler" section and Appendix step 3 still describe "a list of blocks, one per crawler, each two lines" and say the file "allows the AI crawlers we care about (GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot, Claude-User, Claude-SearchBot, PerplexityBot, Perplexity-User, Google-Extended, Applebot-Extended, CCBot)". The committed file has one `*` group and names no crawler (observed). The file and commit 7d58640 are newer than the guide text (the guide was committed 2026-09-22; the robots change 2026-10-01). DEPENDENCIES 13.6.4 flags the PR description as outdated but not the guide. Trust the file.
The voyage explorer is different on purpose: `next-sitemap.config.js` generates one group per crawler with its own copy of the private-path `Disallow` rules (`/admin/`, `/setting/`), because a named group must repeat them. It emits no Content-Signal line (inferred from the config).

### Deliverables
Edited robots.txt in each repo, in a PR.

### Quality rules
Leave `Content-Signal` and `Sitemap:` lines as they are unless that is the change.

### Traps
A robots Disallow alone does not keep a URL out of the index; the explorer repo also needs `X-Robots-Tag: noindex, nofollow` headers for `/admin` and `/setting` (uncommitted change on `voyage` geo-fixes, FIX-PLAN E4).

### Time
Minutes.

---

## Process 8: Stand up a new docs site (the Appendix, 9 steps)

### Purpose
Give a new site the whole GEO layer on day one.

### Trigger
A new docs property joins (done in September for voyage-docs and coco-docs).

### Steps (from the guide's appendix; each names the file)
1. `url` in `docusaurus.config.js` = real production domain (feeds canonical and every sitemap entry). Sphinx: do not use `html_baseurl`; set `page_url` in `_templates/layout.html`.
2. Set `trailingSlash` explicitly in `docusaurus.config.js` AND the same value in `llms.config.json`.
3. Copy `moidocs/static/robots.txt`, change only `Sitemap:`.
4. Copy `scripts/generate-llms.mjs`, `scripts/inject-schema.mjs`, `llms.config.json` from moidocs (Sphinx: `docs/generate_llms.py`). Edit `llms.config.json`: `baseUrl`, `routeBase`, `docsDir`, `siteTitle`, `summary`. Set `package.json` build to `node scripts/generate-llms.mjs && docusaurus build && node scripts/inject-schema.mjs`. Add `static/docs/`, `static/llms.txt`, `static/llms-full.txt` to `.gitignore`. Copy the site-wide structured-data plugin from `moidocs/docusaurus.config.js`; keep the Organization `@id` exactly `https://moi.technology/#organization`.
5. `themeConfig.image` = a real branded image.
6. Copy `static/_headers` (adds a `Link` header to every response pointing at `/llms.txt`, `/.well-known/api-catalog`, `/.well-known/agent-skills/index.json`; and forces `application/linkset+json` on the extension-less api-catalog).
7. Add the new site to the `ecosystem` list in every other site's `llms.config.json`.
8. Remove template leftovers: `facebook/docusaurus` edit URL, sample blog posts, placeholder tagline, default favicon and logo.
9. After first deploy: sitemap lists no stub or sample page; `curl -A "GPTBot/1.0" -I https://<domain>/` returns 200, repeat with ClaudeBot and PerplexityBot.
Also the IndexNow key file and Search Console and Bing registration (Process 6, steps 8 to 10).

### Deliverables
The copied files and edited configs, in a PR.

### Traps (observed in real sites before the sweep)
voyage-docs had `url` set to the dead host `wiki.moi.technology`; moidocs had a dead-domain `url`; coco-docs canonicalized to the `cocolang.docs.moi.technology` mirror and shipped 15 sample-template URLs in its sitemap, and had Cloudflare blocking AI crawlers. coco-docs still has Sui/Mysten leftovers: `sidebar-book.ts` imports a plugin that does not exist (`./src/plugins/yaml-sidebar`) and `docs/book/sidebar.yml` still reads "The Move Book" and "Install Sui"; neither is used (`sidebarPath` is `./sidebars.js`), but they mislead (observed). Also `voyage-docs/package.json` is still named "moidocs".

### Time
Unknown.

### Non-Docusaurus note (guide's table)
Sphinx: base URL in `_templates/layout.html`; static files via `html_extra_path`; per-page description via `.. meta::`. Plain React app: render routes to HTML at build time (MOI-Website does this with `scripts/ssg.mjs`), because crawlers that do not run JavaScript see an empty page.

---

## Process 9: Keep agent-discovery files and version-coupled pages in sync

### Purpose
The `.well-known` lists, skill pages, download links and llms config all name versions and addresses that go stale.

### Trigger
A new Coco release; a new js-moi-sdk release or skill zip; a new API reference page; a moved page; a new site.

### Who
DevRel with the Coco maintainer (Robert) and the SDK team.

### Steps (observed couplings; the order is my suggestion, inferred)
1. Coco release: add a `## vX.Y.Z` section in `coco-docs/docs/releases/index.md` with `<DownloadGrid version="X.Y.Z" />`; `src/components/DownloadButton/downloads.mjs` builds the download links (`https://cdn.moi.technology/cocolang/coco-<version>-<os>.tar.gz` etc., shared by the component and the markdown generator, so the Releases page and its `.md` copy match). Update the version string in the pages that quote it (`docs/book/language/module.mdx`, `docs/book/cli/compiler/compiler.md` show `version = "0.9.2"`).
2. Skill pointers to the same version: `moidocs/static/.well-known/agent-skills/index.json` (`download`), `coco-docs/static/.well-known/agent-skills/index.json`, `moidocs/docs/build/skills/coco-skill.md` (three occurrences of the zip name and version). Commit bcbcbf8 did exactly this for 0.9.2. `moidocs/static/downloads/coco-0.8.2-skills.zip` is still in the repo and is stale (observed).
3. js-moi-sdk: `docs/source/conf.py` `version`/`release` (v0.9.0-rc3 on 2026-10-02), `docs/generate_llms.py` PAGES, the skill page `agent-skill.rst`, `moidocs/static/downloads/js-moi-sdk-skills.zip` and its page `docs/build/skills/js-moi-sdk-skill.md`. DEPENDENCIES 16.2.4 notes the skill says it was checked against SDK v0.7.1 while the page says it targets the current version.
4. Skill zips are hosted on R2 behind `cdn.moi.technology/cocolang/`; the SDK publish workflow uploads the SDK skill zip (owned by the SDK team and DevOps).
5. A new API reference: add an entry to `static/.well-known/api-catalog` (moidocs lists JSON-RPC, WebSocket, pNet and two Voyage pages; voyage-docs lists its three). A moved page breaks these entries and the cross-site `ecosystem` lists in each `llms.config.json`.
6. Each `llms.config.json` carries `agentInstructions` that tell agents where to verify versions (npm for js-moi-sdk; `/releases/` for Coco; Voyage API-key note). Keep them true.

### Deliverables
Edited JSON, markdown and components in a PR.

### Traps
No check ties these files together; they drift silently.

### Open questions
Whether the SDK skill needs a refresh to match the current SDK (DEPENDENCIES 16.6.4).

---

## Process 10: Run a GEO audit of a docs property (the September sweep method)

### Purpose
Find and fix everything that stops a site being found and cited, and score it before and after.

### Trigger
One-off for each property in the sweep (2026-09-02 start; "run another audit" re-runs on 09-09). Repeat after major changes (inferred).

### Who
Adithya with Claude (Sonnet 5.5 and sub-agents). User asked whether Haiku sub-agents help; the assistant answered scripts for extraction, the model for scoring, sub-agents only for cross-site discovery and reading at volume, and Haiku skipped for judgement.

### Inputs
List of properties: docs.moi.technology, voyage docs, docs.wallet.moi.technology (deferred), cocolang.dev, js-moi-sdk docs, the JS agent docs, moi.technology, plus launchpad and agents sites (09-09).

### Steps in order (observed: assistant's stated method at session message 50, then results)
1. Discovery per site: fetch homepage, `robots.txt`, `sitemap.xml`, `llms.txt`; identify generator.
2. Crawl: download the raw HTML of every sitemap page with `curl` (no JS, so you see what GPTBot, ClaudeBot and PerplexityBot see).
3. Programmatic extraction per page (Python script): title length and uniqueness, meta description, canonical, og and twitter tags, robots meta, hreflang, H1 count and hierarchy, word count, internal links, JSON-LD types, and GEO signals (definitional opening, question-phrased headings, entity consistency).
4. Site-level checks: crawler access with real user-agents (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot) including WAF blocks; `llms.txt` and markdown endpoints; sitemap versus nav; canonical and redirect sanity; cross-property Organization and `sameAs` linking.
5. Score each site 1 to 10 on SEO, GEO and AEO with the `seo-geo-aeo` skill rubric (repo SNLabat/SEO-GEO-AEO-Skill, which the user told Claude to use on 2026-08-07), tying every finding to a fetched page; produce a prioritized fix matrix (Critical, High, Medium, Quick Win).
6. Locate each fix in source (repo scan only after the site scan), apply, rebuild, re-verify against the live site or preview.
7. Extra tool run (2026-09-09):
   - linkinator found one dead link: the guardian genesis file URL, still at `moidocs/docs/guard/setup-guardian.md` line 270.
   - A Playwright no-JS diff: docs properties 99 to 116 percent visible to non-JS crawlers (a figure above 100 percent is as recorded and not explained, see Known inconsistencies); the moi.technology homepage 15 percent.
   - Vale: 0 violations in 104 files. markdownlint, Pa11y and a robots audit were also run.
   - JSON-LD validation: 135 of 135 valid.
   - Lighthouse: SEO 100/100/92; performance 82/59/82 where 59 is moi.technology.
   - A dashboard checklist the user pasted on 2026-09-09 ("Diagnostics (Beta): Improve your domain for AI agents", a Cloudflare dashboard, inferred from context) drove the discovery layer: Level 1 robots.txt, AI crawler rules, Content Signals, Markdown Negotiation, Sitemap; Level 2 API Catalog, Link Headers, Auth.md; Level 3 OAuth discovery, A2A agent card, Skills Index, MCP server card, Web Bot Auth, WebMCP; commerce items (x402 etc.).
8. Scores reported to Rahul on 2026-09-10 (SEO/GEO/AEO, order inferred): docs.moi.technology 3/4/3 to 8.5/9/8.5; voyage docs 3/3/3 to 9/9/9; cocolang.dev 3/2/3 to 9/9.5/9 (the 2 was Cloudflare 403-blocking AI crawlers); js-moi-sdk docs 3/4/3 to 9/9/9; moi.technology 5/4/3 to 7/6/5. "The remaining gap to 10s is external authority (mentions, third-party listings)."
8b. Common Crawl check: cocolang and voyage docs had zero crawl coverage (not blocked, just not linked from anywhere).

### Deliverables
Scored report and fix matrix (not found on disk; unknown location), the five PRs, a promptfoo suite (Process 11), a Wikidata draft (Process 11), a coverage audit of about 216 campaign articles (below), a status message to Rahul (Google doc).

### Accounts and tools
curl, Python, Node; npx tools above (no keys); Cloudflare dashboard; Search Console (service account needed for an MCP, not done). Not run for lack of credentials: Semrush MCP, GA4 MCP, DataForSEO, geo-aeo-tracker (needs a Bright Data key).

### Quality rules
Report only what was done: on 2026-09-10 the user rejected a draft line "standardizing our org descriptions across Crunchbase/LinkedIn/GitHub to match verbatim" ("we didnt do this, why are you lying") and had it removed. Put planned work in a separate "next steps" part.

### Traps
Audit scores are the assistant's own rubric, not an external measurement; the user asked how to reach 10/10/10 and the answer was external authority.

### Time
About a week elapsed for six properties with sub-agents.

### Coverage finding that shaped the docs (observed, session message 2525)
Of 216 campaign pieces, none linked to docs.moi.technology; 54 percent discussed the Agent Launchpad, which then had no official docs; so the assistant proposed Launchpad and kill-switch docs. Rahul then decided Launchpad does not belong in protocol docs (the campaign with Scribble "has about 500 articles talking about MOI" about the Launchpad, and Rahul wanted answers to "how do I create an agent on MOI" to be handled by Launchpad docs and the moi.technology use-cases pages instead). The Launchpad section was removed from #124.

### Open questions
Where the scored audit reports went; whether the audit will be repeated on a schedule (no).

---

## Process 11: Measure AI visibility and report it to the community call

### Purpose
Know whether AI engines mention and cite MOI, and which questions people ask, so content (docs and blog) can be aimed at them.

### Trigger or cadence
"This is the baseline we measure every month from here" (Community Call 14 deck, slide 5). Re-run "the same 47 queries every month" (slide 11 and speaker notes). Community calls look roughly monthly (inferred: the CC13 deck was prepared 2026-08-27, the CC14 deck script 2026-09-25).

### Who
Source of the numbers: "the Scribble AI-visibility report" (deck README, dated 24 Sept). Scribble is the agency or campaign partner that wrote the article wave ("the campaign we did with Scribble", Rahul). Whether Scribble also runs the tracking tool is unknown. Adithya turns the numbers into slides and a spoken script.

### Inputs
The Scribble report: 47 queries, 5 AI engines, same set each month.

### What is measured (observed, CC14 deck `index.html` slides 5 to 8, 11)
- Visibility 17.3 percent: how often MOI shows up in the answers to the 47 queries.
- Citations 1,203: times our pages were cited as a source inside answers.
- Mentions 650: times MOI was named in an answer, cited or not.
- By engine: Perplexity 20 percent, Gemini 19.1, Copilot 19, ChatGPT 12.8 (four logos shown; the fifth engine is not named in the deck, presumably Claude, inferred). Movement: Gemini up 12.8 points, ChatGPT down 4.3. Coverage of the tracked set 221 of 226 responses, 97.8 percent. Script line: "Claude is where the room is now".
- Strongest tracked queries (first questions): What is MOI Network? Is MOI a blockchain? What is the MOI Agent Launchpad? Is MOI compatible with other chains? How MOI Technology is perceived by visitors.
- The conclusion given on stage: "a content problem before it is a product one"; plan: core education, product-led, comparison content; "documentation an AI system can read and cite"; re-run the same 47 queries monthly.

### Steps to produce the slides (observed process, inferred order)
1. Get the new monthly report from Scribble (how: unknown).
2. Compare with last month's baseline: visibility, citations, mentions, per-engine, coverage.
3. Edit the slides in the deck `deck/index.html` (in the cc14 example folder): AI visibility (cards), by engine (logos in `deck/assets/engines/*.svg`), the questions, what we do about it, what is next; speaker notes live in the `NOTES` array at the bottom of the file; presenter window opens with key `P`.
4. Run the script text through the humanizer (user 2026-09-25 "use humanize"); keep sentences plain.
5. Export PDF with headless Chrome (command in the cc14 `README.md`), once per HTML file; re-cut the no-guest version so the two never drift.
6. Present on the call; questions from the audience feed the content plan.

Corrections on the deck (observed in requests, 2026-09-24):
- restore the "What people ask AI about MOI" slide that had been removed;
- delete "MOI vs Lit Protocol";
- "copilot - 19% also add each logo";
- "remove the up and down trends on where we show up".

Still in the committed deck (as read on 2026-10-02):
- the "Where we show up" slide says "Gemini moved the most, up 12.8 points, while ChatGPT slipped 4.3", and the notes repeat it;
- the content-plan card still lists "MOI versus Lit Protocol";
- whether those were meant to go is unclear (open question 3);
- the two HTML files in the working deck folder are byte-identical (12 slides, no guest slide) and its README still describes 13 slides with a guest: stale (but see Known inconsistencies).

### Other measurement sources
- Bing Webmaster Tools: "first-party AI Performance report showing when Copilot actually cites us" (the assistant's claim to Rahul, from the status draft; not verified by me). Set up 2026-09-09 by importing from Search Console.
- Google Search Console: indexing and queries (property status unknown for docs sites; the blog has its own property; see `moi-blog/references/geo.md`).
- Cloudflare AI Crawl Control dashboard: per-crawler hit counts (suggested by the assistant, not shown as used).
- promptfoo suite `promptfooconfig.yaml`: 25 queries in four groups (direct entity, problem space, disambiguation/drift, competitive framing) with `icontains` assertions, designed to run across providers "weekly, pass-rate trend is your GEO score". Only `groq:openai/gpt-oss-120b` is active; the other providers are commented out and need keys. It ran three times on 2026-09-09 and never completed (`timed out after 300000ms in queue`); the user stopped it. So there are no promptfoo results (observed in the promptfoo logs).
- GA4 referrers from chatgpt.com and perplexity.ai were proposed, not set up (unknown).
- Wikidata and entity consistency: items for Sarva Labs and MOI drafted; "someone is doing wikidata" (Sai Kiran); Q-numbers to be added to `sameAs` in all repos; status unknown.

### Deliverables
CC14 deck (HTML, PDFs), script (the cc14 `SCRIPT.md` covers slides 2 to 4 only), a content plan.

### Accounts and tools
Scribble report access (unknown); Bing and Search Console logins; promptfoo needs at least one provider key (OpenAI, Anthropic, Google or Groq) typed into the terminal by the user, never into chat; `npx promptfoo eval -c promptfooconfig.yaml` then `npx promptfoo view`. API keys are explicitly an open item the user will settle last.

### Quality rules
Numbers are quoted exactly; trends are the contested part; do not claim a measurement that was not run (the promptfoo baseline does not exist).

### Time
Wikidata about 20 minutes, promptfoo about 10, Bing about 5 (assistant estimates, 2026-09-09).

### Open questions
Where the Scribble report lives, how it computes visibility, and who refreshes it; what the fifth engine is; whether the docs team gets the monthly query list before the call.

---

## Process 12: Open and keep a docs PR current

### Purpose
Deliver a docs change without breaking trust or surprising reviewers.

### Steps (observed)
1. Work on a branch (`geo-fixes` on all five repos). Do not push or open a PR until the user says so ("NEVER DIRECTLY PUSH UNLESS I EXPLICITLY SAY TO", 2026-09-09; "dont push anything" on 2026-09-17 and 10-02; memory `no-push-no-notify`).
2. Before creating a PR, confirm that git and `gh` identity is his work GitHub account (user 2026-09-14: "check if its [his work account] then create the pr"; 2026-08-19 asked to switch `gh` auth to it). PRs for js-moi-sdk and voyage come from a fork under that account.
3. Rebase onto the latest `main` before pushing ("audit and check for rebase", 2026-09-30; 2026-10-01). Check ordering against other open PRs (user asked whether #126 lands before or after; #126 was already in main). After a rebase, diff the pages against main: commit 0899368 fixed a rebase that had kept an older copy of `submit-ixn.md` and reverted the storage-deposit example from #120.
4. Keep generated files out of the commit (all Docusaurus sites).
5. Write the PR body in the established shape: What this is, Why, What changed (site identity, content pass, crawler access, discovery layer, style guide), Rebased note, Verification (`npm run build` green, number of pages, no broken links), Post-merge checks as a checklist of curl commands, and Review notes ("review the two scripts, spot-check outputs, do not read generated text").
6. Update the body when facts change. On 2026-10-02 three bodies are stale: moidocs #124 says each AI crawler is listed in robots.txt (now one group); voyage-docs #5 says the same; js-moi-sdk #150 says it adds `docs/DOCS-GEO-STANDARD.md` (retired, commit 2c6c861 removed it).
7. Reply to reviewers and re-request review after fixing their change request (moidocs: Rahul's request is met but not answered).
8. No Claude attribution: do not add a `Co-Authored-By: Claude` trailer or a "Generated with Claude Code" footer (memory `no-claude-attribution`; user 2026-10-01 asked how to remove Claude as co-author and had open PR histories rewritten, leaving backup branches such as `geo-fixes-before-attribution-rewrite`). Note: the session's system-level attribution reminder conflicts; the user's own instruction wins.
9. On 2026-10-01 the user asked to "commit and push the PRs, moidocs first, then every 4 minutes update the next one" (staggered pushes; reason unknown; possibly to avoid a notification or build burst, inferred).
10. Batch tweaks on one branch instead of one PR per change (memory `batch-review-changes`).

### Deliverables
Open PR with green Cloudflare check.

### Traps
Stale PR descriptions; rebase conflicts silently reverting someone else's merged content; pushing without being told; attribution trailers; opening a PR from the wrong GitHub account.

### Time
A rebase plus checks took one working session per repo (inferred).

---

## Process 13: Drift sweep after upstream merges (derived; not yet a routine anyone ran)

### Purpose
The sweep's rules decay as other authors merge pages. Because the CI lint was removed, a DevRel has to check by hand.

### Evidence of drift found on 2026-10-02 (observed by my read-only audit)
- moidocs pages merged from other PRs after the sweep carry no `image`, and some have descriptions outside the band: `docs/learn/fundamentals/access-control.md` (127 characters), `docs/build/moi-wallet.md` (118), `docs/build/tutorials/sponsored-ix-tutorial.md` (122), `docs/build/tutorials/storage-cost-tutorial.md` (123), `docs/build/tutorials/access-policy-tutorial.md` (68, and its H1 is `# Managing Access Policies in MOI`). PR #124's body says four such pages are "left as-is here for a small follow-up".
- The four newer tutorials (`sponsored-ix`, `storage-cost`, `multi-sig`, `access-policy`) have no `HowToSchema` although the guide says tutorials get it.
- The naming rule is broken in the same pages: "Setting up JS-MOI-SDK" link text in `multi-sig.md` (2), `sponsored-ix-tutorial.md`, `storage-cost-tutorial.md`, `multi-sig-tutorial.md`, `access-policy-tutorial.md`, even though the style guide's Rule 5 (exact product names) uses a heading of that form as its bad example.
- `docs/guard/setup-guardian.md` line 270 links `https://moichain-pub.s3.amazonaws.com/genesis.json`, reported dead by linkinator on 2026-09-09 and still returning HTTP 404 when I checked on 2026-10-02.
- Two more moidocs pages lack `sidebar_position`: `learn/fundamentals/logics.md` and `execution-and-fuel.md`; coco-docs `releases/index.md` and `install/index.md` too (order falls back to name).
- voyage-docs `getting-started/getting-started.md` opens with "## 1. Sign up with Voyage" and has no definition paragraph (rule 2).

### Steps (suggested; inferred)
1. After each merge to main on a docs repo: pull; run the frontmatter audit script (to be written; spec in the last section).
2. `npm run build` and the checks in Process 5.
3. Fix with one small PR (batch, Process 12).
4. Quarterly or per release: re-run the `curl -A` matrix and the promptfoo suite when keys exist.

### Open questions
Whether the user wants this as a routine; he explicitly declined scheduled automation.

---

## Reusable assets

Paths are relative to the local clone of the named repo unless noted.

Authoring and review
- `moidocs/DOCS-STYLE-GUIDE.md`: the rule set, naming table, frontmatter contract, per-site differences table, appendix for new sites (on branch `geo-fixes`; not on `main` yet).
- `moidocs/src/components/FaqSchema.jsx` and `HowToSchema.jsx`: schema components (uses `@docusaurus/Head`; plain JSX because MDX v1 drops raw `<script>`).
- `moidocs/static/img/moi-card-learn.png`, `moi-card-build.png`, `moi-card-guard.png`, `moi-social-card.png`: section share images used by the `image` field.
- Examples: `.../moidocs/docs/learn/fundamentals/account.md` (concept page, answer-first, `{#anchors}`), `.../docs/build/tutorials/account-tutorial.md` (HowToSchema), `.../docs/guard/guardian-faq.md` (FaqSchema and preserved anchors), `.../docs/build/json-rpc.md` (reference, quoted description), `.../docs/learn/fundamentals/networks.md` (stub), `voyage-docs/docs/endpoint-docs/faucet.md` (question headings with anchors), `.../coco-docs/docs/book/language/state/state.md`, `.../coco-docs/docs/book/getting-started/first.md`.

GEO layer
- `moidocs/scripts/generate-llms.mjs` and `inject-schema.mjs`, `moidocs/llms.config.json` (identical in voyage-docs).
- `coco-docs/scripts/generate-llms.mjs`, `inject-schema.mjs`, `scripts/lib/docs.mjs`, `llms.config.json` (newer generator; baseUrl `https://cocolang.dev`, `routeBase` empty, trailing slash true, glossary path), `static/_redirects`, `static/_headers`.
- `js-moi-sdk/docs/generate_llms.py`, `docs/Makefile` (target `llms`), `docs/source/_templates/layout.html`, `docs/source/conf.py` (the `html-page-context` hook), `docs/source/_extra/{robots.txt,sitemap.xml,404.html}`.
- `moidocs/static/robots.txt`, `static/_headers`, `static/.well-known/api-catalog`, `static/.well-known/agent-skills/index.json`; `docusaurus.config.js` (the `structuredData` plugin, `themeConfig.image`).
- `voyage/next-sitemap.config.js`, `public/llms.txt`, `src/layouts/Meta.js`, `next.config.js`.
- IndexNow key file in each repo (name equals the key; public by design).

Retired but useful, in moidocs git history (`git show <rev>:<path>`)
- `638258b:scripts/lint-docs-geo.mjs`: zero-dependency lint (description 140 to 160, quoted colons, version-free titles, one H1, scaffolding strings, stub without noindex). Removed from CI on purpose; usable as an on-demand local script.
- `ba13b20:.github/workflows/geo-health-check.yml`: the curl matrix (GPTBot, ClaudeBot, PerplexityBot on six properties; robots.txt and llms.txt content type; homepage canonical host). Removed on purpose; its body is the model for an on-demand live check.
- `742a2c2:DOCS-GEO-STANDARD.md`: the old 10-rule standard with a PR reviewer checklist and framework quick reference.

Measurement
- `promptfooconfig.yaml` (outside the repos, on Adithya's Mac): 25-query AI-visibility suite.
- `skills/moi/moi-webinar/community-call/examples/cc14/deck/index.html` and `README.md`: AI-visibility slide pattern (baseline cards, per-engine stats with logos, questions, content plan, next steps) and the PDF export command.
- `skills/moi/moi-webinar/community-call/examples/cc14/SCRIPT.md`: example of a spoken script.

Status writing
- The 2026-09-10 status message to Rahul (draft in the session log at line 4657, session 466347ed): structure Content changes, Frontmatter and metadata, llms.txt, robots.txt, Entity presence, Analytics, Audit scores, Status per property.

---

## Rules and house style

Docs content
1. Hand-written `title` and 140 to 160 character `description` on every page; quote it if it contains `: `.
2. First paragraph defines the thing and stands alone.
3. Question headings only where the section answers the question. Do not turn every heading into a question.
4. Keep old anchors (`{#old-anchor}`); grep and search the org before changing one deliberately.
5. Names: MOI, MOI Wallet, Coco (also known as Cocolang on first mention), js-moi-sdk (always lowercase), MOIPod, Voyage, Sarva Labs.
6. Stubs are `noindex` (or `unlisted: true`) until real; remove the mark in the same change.
7. Never hand-edit llms.txt, llms-full.txt, the `.md` copies or the sitemap, with one exception: on js-moi-sdk the sitemap is kept by hand (Process 2, step 5).
8. Link by `/address`, not full URL.
9. Prose: brief, direct, no metaphors, no "AI" filler; every claim verified against source; run humanizer and stop-slop; no em dashes in outgoing copy and status messages (the style guide and `llms.config.json` contain none). Older page bodies contain 156 em dashes; 11 were added in the sweep (observed), so this is a preference, not an enforced rule.
10. Do not overstate: the user caught "Every action on MOI costs fuel" in the release blog as untrue and "exaggeration and misleading" (2026-09-11); the same standard applies to docs.
11. Use the user's terminology: participant-centric (not account-centric), MDAG (not a per-account chain), "designed and developed by Sarva Labs, governed by MOI Foundation", say network ID not chain ID (memory `moi-terminology-corrections`; stated for specs and PRs, applies to docs).

Scope
12. Protocol docs hold protocol content. No application docs (Launchpad) inside moidocs (Rahul). Use cases live on moi.technology.
13. Do not publish a page you cannot ground in source: the kill-switch page was deleted on 2026-09-09 because it "doesnt properly talk about what MOI kill switch is".
14. The style guide stays in the repo root and is NOT published on the site ("let it just be on the repo as rules", Rahul via the user 2026-09-22).

Process
15. No CI policing and no scheduled monitoring for docs (maintainer preference, 2026-09-09). Verify by hand, on demand.
16. Stay local until told: no push, no PR, no comments on audit or handover tasks.
17. The guide is for humans: say what to do, why, with one real example per rule.
18. Report only completed work; keep next steps separate.
19. Keep generated files out of git except js-moi-sdk's `_extra/`.
20. Keep moidocs and voyage-docs scripts byte-identical.
21. After any Cloudflare, WAF or hosting change re-run the crawler curl matrix.

---

## Traps

1. Unquoted `: ` in a Docusaurus description fails the build (YAML). Quote the value.
2. A blank line before the first `---` makes the site ignore the frontmatter. The generator's parser also requires `---` at position 0.
3. Rewording a heading changes its anchor; inbound links land at the top of the page and nothing reports it.
4. `# Title` plus `HowToSchema` or `FaqSchema` renders two titles; a blank line inside the component call can break parsing.
5. A finished stub still marked noindex never appears in search; an unmarked stub or the sample `markdown-page` appears in the sitemap.
6. Content-Signal outside a User-agent group attaches to nothing; per-crawler groups do not inherit the `*` group's signals (fixed 2026-10-01).
7. The api-catalog file has no extension, so it was served as `application/octet-stream`; `_headers` now forces `application/linkset+json` (RFC 9727).
8. JSON-LD built from built HTML came out entity-encoded ("MOI&#x27;s"); fixed by decoding; `<` must be escaped; `dateModified` was the head commit time on shallow clones (fixed; omitted if history is unavailable).
9. llms-full.txt carried raw JSX (265 lines) and stripped `import` lines from code samples; fixed by only rewriting outside code fences and by `DROPPED_COMPONENTS`.
10. Rebase resolution can restore an older copy of a page that another PR already updated (commit 0899368). Diff against main after any rebase.
11. js-moi-sdk's host serves 200 with HTML for unknown paths (including `/robots.txt` before the file exists); a status check alone passes. Check content type and body.
12. `html_baseurl` in Sphinx makes every canonical point at a 308 redirect.
13. `trailingSlash` must match between `docusaurus.config.js` and `llms.config.json`. The guide says to set it explicitly, but `moidocs/docusaurus.config.js` and `voyage-docs/docusaurus.config.js` do not set it (they rely on the default, which currently yields no trailing slash, consistent with `false` in `llms.config.json`).
14. The guide says the build "fails if" a link "points nowhere". Only route links throw; `.md`-file links are `warn`, and Docusaurus 2.1 does not check anchors (inferred).
15. Cloudflare AI-crawler blocking at the zone level (cocolang.dev until 2026-09-09) overrides every file change.
16. Generator drift: three variants of the same job (moidocs and voyage-docs identical old version; coco-docs newer; js-moi-sdk Python). A fix in one is not a fix in all.
17. Version strings in many places (Coco 0.9.2 in five files; stale `coco-0.8.2-skills.zip` still in `moidocs/static/downloads/`).
18. `static.md` stray file in the coco-docs repo root; Sui "Move Book" sidebar leftovers; `voyage-docs/package.json` name "moidocs"; generator comment still cites the retired DOCS-GEO-STANDARD.
19. The guide's robots.txt section no longer matches the committed file (see Allow or block).
20. PR bodies go stale (three of five on 2026-10-02).
21. Promptfoo on a free Groq model queues and times out; no baseline exists.
22. The deck folder: both HTML files identical, README stale (13 slides with guest), trend text still present after a request to remove it.
23. Never copy secrets: none are needed for docs; the IndexNow key is public; promptfoo and MCP tools need provider keys that belong in the user's terminal, never in chat or notes.

---

## Open questions

1. Who owns (and can log into) the Cloudflare Pages projects `moichain-docs`, `cocodocs`, `voyage-docs` and the domains, and the Search Console and Bing properties? DEPENDENCIES says "owner: confirm" for each.
2. Where does the Scribble AI-visibility report live, who refreshes it monthly, how is "visibility" computed, which five engines, and how are the 47 queries chosen? Is a CSV or dashboard available to the new DevRel?
3. Was the request to remove trend text and "MOI versus Lit Protocol" from CC14 meant to cover the "where we show up" slide, the notes and the content-plan card? They remain in the deck.
4. Who decided `ai-train=yes` ("per policy decision")? Is it still the policy? Will Cloudflare's managed robots.txt on cocolang.dev (on 2026-10-02 the only content served) override or prepend to the repo's file after merge?
5. The exact IndexNow submission command and whether it was ever run for the five sites.
6. Merge authority and order: who merges each repo; is moidocs #124 waiting only on a reply to Rahul and Gokul's review; the MOI-Website PR #57 must follow it.
7. Should `trailingSlash` be set explicitly in moidocs and voyage-docs configs as the guide says?
8. Does Docusaurus 2.1 on moidocs and voyage-docs fail on broken anchors or markdown-file links? (config says `warn` for the latter.)
9. Should the four newer moidocs tutorials get `HowToSchema`, `image` and in-band descriptions now, or in a follow-up as PR #124 says? Which correct URL replaces the dead guardian `genesis.json` link?
10. js-moi-sdk docs: how is the site built and deployed after merge, how does a change get previewed, and should generated `_extra/` files stay committed?
11. The docs.wallet.moi.technology site: repo, owner and whether it follows the guide (not covered anywhere).
12. Does the moidocs breadcrumb generator produce items for intermediate URL segments that are not real pages? (The coco-docs version only lists real pages; inferred difference.)
13. Wikidata items for MOI and Sarva Labs and their Q-numbers: created? Added to `sameAs`?
14. Whether `static/downloads/coco-0.8.2-skills.zip` and `js-moi-sdk-skills.zip` in moidocs should be removed or still served (the `.well-known` index points at the CDN for Coco).
15. Whether the audit scoring reports (3/4/3 to 9/9/9 etc.) are saved anywhere.
16. Where the PR #120 fact-check report was saved.

---

## What a skill for this should contain (original proposal)

This section is the original proposal. The built skill is `skills/moi/moi-docs/` with its GEO branch `skills/moi/moi-docs/geo/` (one skill with a branch, not the two skills proposed here); the reference and script names below were not all built as written.

Recommended split into two skills so each stays small.

### Skill 1: `moi-docs` (writing, reviewing, maintaining docs pages)

SKILL.md outline (description triggers: "docs.moi.technology", "write a docs page", "docs PR", "frontmatter", "style guide", "cocolang.dev", "voyage docs", "js-moi-sdk docs", "llms.txt", "sitemap"):
1. Find the site (table).
2. The seven rules, each with the real example from the guide.
3. New page: steps 1 to 13 above, with the frontmatter template per site.
4. Update a page: the five checks.
5. Review a docs PR: the derived checklist, plus how to run the fact-check (Process 4).
6. Open and maintain the PR (Process 12), including the identity, rebase, no-push and no-attribution rules (as configurable house rules, since a new hire's setup differs).
7. When to stop and ask: moving a page (redirects), Launchpad or application content, anything not groundable in source.

Reference files to bundle:
- `references/sites.md` (table, node versions, preview URLs, Cloudflare projects).
- `references/frontmatter.md` (contract, quoting rule, per-site differences, `_category_.json` description rule).
- `references/names.md` (naming table plus terminology corrections).
- `references/anchors.md` (preserve and migrate anchors, grep commands, Sphinx target syntax).
- `references/stubs.md`.
- `references/review-checklist.md` (derived; mark as derived).
- `references/js-moi-sdk-sphinx.md` (the five steps and the sync check).
- `references/factcheck-pr.md` (PR #120 pattern, issue comment format, report format).
- `references/house-style.md` (the prose rules above and the corrections list).

Templates to bundle (`assets/`): frontmatter templates for moidocs (with `image`), voyage-docs, coco-docs (with `# Title` and `unlisted`), Sphinx `.rst` header; a HowTo and a FAQ page skeleton copied from `account-tutorial.md` and `guardian-faq.md`; the PR description template (Why, What changed, Verification, Post-merge checks, Review notes) taken from #124, #12, #150; the issue-comment template ("Issue N: what, why, where, suggested fix").

Scripts worth writing (read-only, on demand, no CI):
- `scripts/check_pages.py <repo>`: frontmatter audit (the logic of my 2026-10-02 audit and of `638258b:lint-docs-geo.mjs`): first line `---`, description present, band 130 to 170 and exact 140 to 160 report, unquoted colon, title without version, `image` present on moidocs, `sidebar_position`, one H1, `HowToSchema` or `FaqSchema` plus H1, stub detection without noindex, naming-table regex over prose outside code fences.
- `scripts/check_sdk_docs.py`: compare `.. meta::` descriptions, `PAGES`, `toctree` and `sitemap.xml` (the check I ran).
- `scripts/check_build.sh <repo>`: after a build, assert sitemap has no stub or `markdown-page`, llms.txt line count equals page count, every `index.html` has a canonical on `baseUrl` and a TechArticle, `.md` copies exist, no raw JSX in `llms-full.txt`.
- `scripts/compare_generators.sh`: `diff` moidocs vs voyage-docs scripts.

### Skill 2: `moi-geo` (the machine-readable layer, post-merge, audit, visibility)

SKILL.md outline: 1. What each file is for and who writes it (table: llms.txt, llms-full.txt, `.md` copies, sitemap, robots.txt, `_headers`, `.well-known`, JSON-LD, IndexNow, share image). 2. Verify locally (Process 5). 3. After merge (Process 6). 4. Allow or block a crawler (Process 7) with the corrected one-group procedure. 5. New site (Process 8). 6. Keep lists and versions in sync (Process 9). 7. Audit method (Process 10). 8. Measure and report (Process 11). 9. Hard "no" list: no CI gate, no cron.

References: `references/files-and-generators.md` (inputs and outputs of the three generators, the DROPPED_COMPONENTS rule, shallow-clone dateModified), `references/robots.md`, `references/post-merge.md`, `references/new-site.md`, `references/version-coupling.md`, `references/audit-method.md` (steps, tool list, score table, Cloudflare Diagnostics levels), `references/measurement.md` (Scribble numbers definitions, Bing, GSC, promptfoo, what to say on the call), `references/framework-table.md` (Docusaurus, Sphinx, React).

Scripts:
- `scripts/live_check.sh <domain...>`: the curl matrix (GPTBot, ClaudeBot, PerplexityBot; status plus content type for `/`, `/robots.txt`, `/llms.txt`, `/sitemap.xml`, a nonexistent path, `/.well-known/api-catalog` content type `application/linkset+json`, `Link` header present). Base it on `ba13b20:geo-health-check.yml` and my 2026-10-02 run.
- `scripts/audit_site.py <url>`: discovery plus no-JS crawl plus extraction (the method in Process 10), output JSON and a scorecard markdown.
- `scripts/indexnow_ping.sh` (to be written once the command is confirmed; takes the key file name, never prints the key).
- `scripts/visibility_delta.py`: given last and current Scribble numbers (visibility, citations, mentions, per engine), print the deltas and the slide text (needs the report format; unknown at the time of writing).

Templates: the promptfoo config (`assets/promptfooconfig.yaml`, with providers list for the user to trim, no keys); a 3-slide AI-visibility block (baseline, by engine, questions) and its speaker-note format; a status-message template (Content changes, Frontmatter, llms.txt, robots.txt, Entity presence, Analytics, Audit scores, Status per property) with the "only what was done" rule.

Open items for the skill author to resolve with Adithya before writing: Open questions 2, 4, 5, 10.

---

## Known inconsistencies in these notes

- **Site and repo counts.** The date line says "all four docs repos" are on `geo-fixes`; Process 12 step 1 says "all five repos" (the four docs repos plus the `voyage` explorer repo); Process 1 time says a "five-site sweep"; Process 6 step 10 says the IndexNow key file is on "all six sites"; Process 10 time and the retired `geo-health-check.yml` entry say "six properties". The sets differ (docs sites, repos, properties including moi.technology) and are not reconciled.
- **Number of AI engines.** Process 11 says the Scribble report covers 5 AI engines, but the deck names only four (Perplexity, Gemini, Copilot, ChatGPT); the fifth is guessed as Claude (inferred).
- **Non-JS visibility above 100 percent.** Process 10 step 7 records docs properties as "99 to 116 percent visible to non-JS crawlers"; a share above 100 percent has no explanation in the notes.
- **Count of out-of-band pages.** Process 13 lists five moidocs pages with descriptions outside the band, while PR #124's body (as quoted there) says four such pages are left for a follow-up.
- **Who edits the sitemap.** Process 1 says you never edit the sitemap; Process 2 step 5 says js-moi-sdk's sitemap is edited by hand. This is a real exception, now stated in Rules item 7.
- **js-moi-sdk version.** The docs say `v0.9.0-rc3` (Process 2 and Process 9), the skill says it was checked against SDK v0.7.1 (Process 9 step 3), and the stale sitemap index is v0.7.0-rc1 (Process 6 step 8). The August release post (see `release-blog-social.md`) names js-moi-sdk v0.8.0. These are different artefacts and are not reconciled.
- **Robots.txt.** The style guide's robots.txt section still describes a block per crawler while the committed file is one group (see "Discrepancy to resolve" in Process 7). The notes say to trust the file.
- **Request-log cut length.** This file says the request log cuts lines at about 413 characters; `request-patterns.md` says about 300 and `release-blog-social.md` says about 415.
- **Deck folder.** Process 11 says the two HTML files in the working deck folder are byte-identical with no guest slide; the cleaned copy in `skills/moi/moi-webinar/community-call/examples/cc14/deck/` has an `index.html` and an `index-guest.html` that differ. Follow that folder's README.
- **Docs reviewer checklist and component wording (cross-file).** `drive.md` records the 14 September Documentation Standard v2 as telling reviewers to use a "PR Review Checklist for Docs Reviewers" and to call the schema wrapper components "on a single unbroken line". The style guide committed on 22 September (this file, Process 3 and Process 1 step 9) removed the review steps and allows a multi-line call with no blank line inside. `drive.md` also lists the older robots.txt policy that Process 7 here supersedes.
- **Process 3 steps.** The review checklist is assembled from the guide's rules and "Common mistakes" table because the guide itself has no reviewer section (inferred, as stated there).

---

## Glossary

Terms are defined as MOI uses them; "(as used in these notes)" marks my best reading.

- **SEO / GEO / AEO:** search engine / generative engine / answer engine optimisation. GEO means making pages findable and citable by AI assistants; AEO means being the direct answer (featured snippets, voice).
- **llms.txt / llms-full.txt:** machine-readable lists of a site's pages (and their text) written for AI agents.
- **JSON-LD:** structured data embedded in a page's HTML. **TechArticle, BreadcrumbList, HowTo, FAQPage, Organization, WebSite:** the schema types used (HowToSchema and FaqSchema are the moidocs components that emit HowTo and FAQPage).
- **Canonical:** the one address a page declares as its main address, so duplicates do not compete.
- **noindex:** a robots meta tag that keeps a page out of search; used on stub pages.
- **Sitemap:** the XML list of pages for crawlers. **robots.txt:** the file telling crawlers what they may read. **Content-Signal:** a robots.txt line stating how content may be used (search, ai-input, ai-train).
- **IndexNow:** a protocol to tell search engines a page changed; it needs a public key file at the site root.
- **Docusaurus / Sphinx / MDX:** the doc-site frameworks (Docusaurus for moidocs, voyage-docs and coco-docs; Sphinx for js-moi-sdk) and the Markdown-plus-JSX format Docusaurus pages use.
- **Frontmatter:** the metadata block between `---` lines at the top of a page (title, description, sidebar position, image).
- **Anchor:** the `#fragment` a heading creates, which inbound links rely on.
- **Stub:** an unfinished page marked noindex (or unlisted) until it has real content.
- **Cloudflare Pages:** the hosting that builds each docs repo on merge and makes previews. **R2:** Cloudflare's object storage, behind `cdn.moi.technology`. **WAF:** the web application firewall, which can block AI crawlers.
- **Soft 200:** a server returning status 200 with an HTML page for addresses that do not exist.
- **`.well-known/api-catalog`, `agent-skills/index.json`:** discovery files that list a site's APIs and downloadable agent skills.
- **MOIPod:** MOI's node software (as used in these notes). **go-moi:** the Go implementation of the MOI protocol. **PISA:** MOI's logic execution engine (as used in these notes). **Coco:** MOI's contract language (also called Cocolang); CocoLab is its playground. **Voyage:** MOI's explorer and dev tooling site.
- **MDAG:** the structure MOI uses instead of a per-account chain (as used in these notes). **Participant-centric:** MOI treats the participant, not the account, as the unit.
- **A2A, MCP, x402:** agent-to-agent protocol, Model Context Protocol (tools for AI agents) and a payment scheme on HTTP 402; they appear only in the discovery checklist.
- **promptfoo:** a tool that runs a fixed set of questions against AI models and checks the answers. **linkinator:** a broken-link checker. **Playwright:** browser automation (used here for a no-JS rendering diff). **Vale:** a prose linter. **markdownlint:** a Markdown linter. **Pa11y:** an accessibility checker. **Lighthouse:** Google's page quality audit.
- **Common Crawl:** the public web crawl many AI models train on; zero coverage means a site is not in it.
- **CC13 / CC14:** the thirteenth and fourteenth monthly community calls (CC14 was in late September 2026).
- **Wikidata:** the open knowledge base whose entries for MOI and Sarva Labs help AI systems recognise them as entities.
- **Scribble:** the campaign partner behind the AI-visibility report (as used in these notes).
- **Shallow clone:** a git clone with truncated history, which makes every page's last-modified date look like the latest commit.

