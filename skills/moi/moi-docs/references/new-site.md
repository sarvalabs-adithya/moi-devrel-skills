# Stand up a new docs site

Done twice so far, in September 2026, for voyage-docs and coco-docs; both were already live and were brought up to standard. No site has been created from nothing under this process. Facts are as of 2026-10-03. The nine appendix steps of the style guide (`DOCS-STYLE-GUIDE.md`, only on PR #124's branch of `sarvalabs/moidocs`) are reproduced here in order, with an owner for each. The files that make a site visible to search engines and AI assistants are the `geo` branch's job (`geo/GUIDE.md`): this file names them and hands over. `$SKILLS`, "the operator" and `ASK:` are defined in `moi-devrel/SKILL.md`. Back to `../SKILL.md`.

## Decide first
1. Is a new site the right thing? Rahul's ruling of 2026-09-17: protocol docs hold protocol content, and an application's docs belong with the application (his reason: the Agent Launchpad is an app that uses MOI and could shut down), with use cases on moi.technology. ASK: Rahul for scope before anything is created.
2. Who owns the content and who reviews it (a named person), and who owns hosting and DNS. DNS records on MOI domains are DevOps (Upendhar, per `moi-devrel/references/people-and-teams.md`); the Cloudflare account owner is not on record. ASK: Rahul.
3. Which scaffold. The guide says copy `moidocs` (Docusaurus 2.1). The newer generator is in `coco-docs` (Docusaurus 3.9, `scripts/lib/docs.mjs`, handles components, absolute links in the markdown copies and a glossary). The two versions of the scripts differ and a fix in one is not a fix in the other. ASK: Gokul which to copy. Do not mix them.

## The steps
GATE marks a step that needs the operator's yes: creating a repository, a Pages project or a DNS record changes a shared system.
| # | Step | Owner | What to do and which file | Done when |
|---|---|---|---|---|
| 1 | Repository | Org admin. GATE | Create `sarvalabs/<name>`, visibility as decided, default branch `main`. Add `CODEOWNERS` naming the reviewer if the team wants one (only js-moi-sdk has one) | The repo exists and the operator can push to a branch |
| 2 | Scaffold | This skill | Copy the chosen site's files: `package.json`, `docusaurus.config.js`, `sidebars.js`, `babel.config.js`, `tailwind.config.js`, `src/`, `static/` | `npm run start` serves an empty site |
| 3 | Base URL | This skill | Set `url` in `docusaurus.config.js` to the real production domain. It feeds the canonical link on every page and every sitemap entry. Sphinx: do not use `html_baseurl`; the base address goes in `_templates/layout.html` | The config names the right host |
| 4 | Trailing slash | This skill | Set `trailingSlash` explicitly in `docusaurus.config.js` and the same value in `llms.config.json` | The two files agree |
| 5 | Template leftovers | This skill | Remove the `facebook/docusaurus` edit URL (point `editUrl` at the new repo), the sample blog folder and posts, `src/pages/markdown-page.md`, the placeholder tagline, the default favicon and logo, and any other project's sidebar files. Set the package `name` (voyage-docs is still named `moidocs`). Set `themeConfig.image` to a real branded image | A search of the repo for `facebook/docusaurus`, `Sui`, `Move Book` and `wiki.moi.technology` finds nothing |
| 6 | First pages | This skill | `write-docusaurus.md` and the templates. Mark every unfinished page as a stub (`page-standard.md` R6). Give each folder a `_category_.json` with a description | The lint is clean on every page |
| 7 | Machine layer | The `geo` branch | Copy `static/robots.txt` and change only its `Sitemap:` line; copy `scripts/generate-llms.mjs`, `scripts/inject-schema.mjs` and `llms.config.json` and edit `baseUrl`, `routeBase`, `docsDir`, `siteTitle`, `summary`; set the build script to `node scripts/generate-llms.mjs && docusaurus build && node scripts/inject-schema.mjs`; add `static/docs/`, `static/llms.txt` and `static/llms-full.txt` to `.gitignore`; copy the site-wide structured data block and keep the Organization `@id` exactly `https://moi.technology/#organization`; copy `static/_headers`; add the IndexNow key file; add `.well-known` entries | `geo/GUIDE.md` says so |
| 8 | Cross links | The `geo` branch | Add the new site to the `ecosystem` list in every other site's `llms.config.json` | Each site lists the others |
| 9 | Hosting | The Cloudflare owner (ASK: Rahul) and DevOps for DNS. GATE | A Cloudflare Pages project on the repo, production branch `main`, build command `npm run build`, a Node version that satisfies `engines`, the custom domain and its DNS record. Every branch then gets a preview. ASK: Rahul for the account, the project and the Node setting; ASK: Upendhar for the DNS record | The first deploy is green |
| 10 | First-deploy checks | The `geo` branch | The sitemap lists no stub and no sample page. `curl -A "GPTBot/1.0" -I https://<domain>/` answers 200, repeated with ClaudeBot and PerplexityBot. A Cloudflare setting that blocks AI crawlers at the zone level overrides every file (cocolang.dev returned 403 to them until the zone setting was switched off on 2026-09-09) | All three answer 200 |
| 11 | Registration | Property owners. GATE | Search Console and Bing Webmaster Tools (import from Search Console). Owners are unrecorded. ASK: Rahul | The sitemap is submitted |
| 12 | Make it known | This skill. GATE for the PR | Add the site to the style guide's "Find your site first" and "What differs on each site" tables (a PR to `sarvalabs/moidocs`), to `references/sites.md` of this skill and to `moi-devrel/references/repo-map.md` | Nobody has to ask where the site lives |

## What the sites looked like before they were brought up to standard
Observed in the repos' `main` branches on 2026-10-03 and in the September audit, so you know what to look for:
- moidocs and voyage-docs: `url` set to `https://wiki.moi.technology`, a host that no longer serves them. moidocs also had `editUrl` pointing at `facebook/docusaurus` and the tagline "Authority Layer for the Agentic Economy".
- coco-docs: `url` set to the mirror `https://cocolang.docs.moi.technology`, so canonical links pointed at the mirror; a template `blog/` folder; 15 sample-template URLs in the sitemap; Cloudflare blocking AI crawlers. It still carries files from another project: `sidebar-book.ts` imports a plugin that does not exist and `docs/book/sidebar.yml` still reads "The Move Book". Neither is used (`sidebarPath` is `./sidebars.js`), and both mislead.
- voyage-docs: a page title "Welcome to Voyage Docs" and the package name `moidocs`.
- Common Crawl had no coverage of cocolang.dev or voyage-docs: they were not blocked, just not linked from anywhere.

## If the site is not Docusaurus
| Setting | Sphinx | Plain React app |
|---|---|---|
| Base URL | the `page_url` logic in `_templates/layout.html` | hosting config and the tags in `index.html` |
| Static files such as `robots.txt` | `html_extra_path` in `conf.py` | `public/` |
| Per-page description | `.. meta::` at the top of the file | each route rendered to real HTML at build time (MOI-Website does this with `scripts/ssg.mjs`), because crawlers that do not run JavaScript see an empty page |
| Generated llms files | `docs/generate_llms.py`, run with `make llms`, committed | a build-time script |

## Not yet known
- Who creates repositories and Pages projects and who owns the Cloudflare account. ASK: Rahul. Who changes the DNS record. ASK: Upendhar.
- Whether any new site is planned. ASK: Rahul.
- Time to stand a site up: not recorded.
