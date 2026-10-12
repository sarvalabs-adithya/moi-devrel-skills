# Audit a property: the September 2026 sweep method

Facts are as of 2026-10-03. The method is the one the previous operator used from 2026-09-02 to 2026-09-09 on the properties in the score table below (the record says six properties; scores for five are on file; ASK: Adithya for the sixth), written down from the session record and re-run in part on 2026-10-03. The scores it produced are the auditor's own rubric, not an external measurement. Page-level frontmatter and naming checks belong to the parent skill (`moi-docs`). Back to `../GUIDE.md`.

## Rules for an audit
1. Local and read-only. No push, no pull request, no comment, no message. A finding that notifies someone is the operator's to send (`moi-devrel/references/consent-and-identity.md`, section 6).
2. Keep the output out of git. It names private repo paths and people. In the folder you work in, `mkdir -p geo-audit-<YYYY-MM-DD> && printf '*\n' > geo-audit-<YYYY-MM-DD>/.gitignore` makes the folder hide itself, and `.gitignore` included, from `git add`. Do this before you write anything, even if the working copy is private. `moi-foundation/MOI-Webinars` and `sarvalabs/MOI-Website` are public. If the folder sits inside a repo, check it: `git status --short` must not list it, and `git check-ignore -v geo-audit-<YYYY-MM-DD>/report.md` must print the rule (tested 2026-10-03). `git add -f` overrides the rule, so never use `-f` on this folder. Committing it is a GATE.
3. Tie every finding to something fetched: a path, a status, a content type, a line. No evidence, no finding.
4. Report only what was done. On 2026-09-10 a status draft said the organisation descriptions were standardised across Crunchbase, LinkedIn and GitHub. That had not been done, and the previous operator had the line removed. Planned work goes in a separate "next steps" part, labelled as such.
5. Spend: no sub-agents and no paid tool unless the operator names it, with the count stated first. The September sweep used sub-agents because the previous operator asked for them.

## Where the rules and the past reports live
- `DOCS-STYLE-GUIDE.md`, at the root of the private `sarvalabs/moidocs`. It is only on branch `geo-fixes` (open PR #124) and is not on `main`. ASK: Rahul for access.
- Two Google Docs in the previous operator's Drive: "MOI Documentation Standard" (two versions; v2, the longer one made about 40 minutes after v1, is canonical, inferred) and "MOI SEOGEOAEO Sweep Status" (per-change rationale, scores and status per property, dated 10 Sep 2026). Neither was opened in full while this branch was written. ASK: Adithya for access, and Rahul which Standard version is canonical.
- The standard says questions on it go to the previous operator in `#dev-chat`. The standard does not name the platform of that channel. ASK: Adithya.

## The run
| # | Step | How | Done when |
|---|---|---|---|
| 1 | Scope | List the properties from `the-layer.md`. Add `docs.wallet.moi.technology` only if the operator asks; it was deferred on 2026-09-02 and its repo is unknown | A table of hosts, each with its repo and the state of its pull request |
| 2 | Baseline | For each host: `bash "$SKILLS/moi-docs/geo/scripts/geo-check.sh" https://<host> > geo-audit-<date>/<host>.txt`. Add the preview of any open pull request. This is the "before" | One file per host, plus the totals line of each |
| 3 | Crawl without JavaScript | GATE: a bulk download, so state the host and the page count first. Fetch the raw HTML of every sitemap page with `curl` into the audit folder: that is what GPTBot, ClaudeBot and PerplexityBot see. `geo-check.sh` does not do this. It checks one sample page in full and compares `dateModified` across up to ten pages (`--pages 10`). For the per-page table Claude writes a throwaway read-only script in a folder made with `mktemp -d` (the 2026-09 scripts were not found on disk; ASK: Adithya for copies) | A table with one row per page |
| 4 | Extract per page | Title length and uniqueness, description, canonical, `og:` and `twitter:` tags, robots meta, hreflang, H1 count and order, word count, internal links, JSON-LD types, and the GEO signals below | No page without a row |
| 5 | Site-level checks | Crawler access by user-agent name, including a WAF block; `llms.txt` and the `.md` copies; sitemap against the navigation; canonical and redirect sanity; the `Organization` `@id` and `sameAs` on every property | Each check has a result |
| 6 | Optional tools | GATE for each: it is a download or a run that Claude names and the operator approves. linkinator (dead links), a Playwright render with and without JavaScript, Vale, markdownlint, a JSON-LD validator, Pa11y, Lighthouse | The operator chose which; results saved |
| 7 | Score | Score SEO, GEO and AEO from 1 to 10 per property. The `seo-geo-aeo` skill rubric was used (repo `SNLabat/SEO-GEO-AEO-Skill`); use it if it is installed, and say which rubric you used. Sort fixes into Critical, High, Medium and Quick win | A findings table (`templates/findings-table.csv`) and a score row |
| 8 | Locate each fix | Search the repo for the cause only after the site scan. Fixes are made through `moi-docs` and `moi-devrel/ship` | Each finding has a repo and a file |
| 9 | Re-verify | After a fix, rebuild (`verify-locally.md`) and re-run step 2 against the preview. Mark the finding `verified` with the date | The "after" column is filled from fresh output |
| 10 | Report | `templates/audit-report.md`. The operator reads it once before it goes anywhere | Report path stated |

GEO signals in step 4: a definition in the first paragraph that stands alone; question headings only where the section answers the question; entity names spelled as the naming table says and matching the JSON-LD; anchors preserved. AEO signals: an answer-shaped description, FAQ markup where the page is a FAQ, steps markup where it is a tutorial.

## Site-level checks that need a human
- Common Crawl coverage. In September cocolang.dev and voyage-docs had none: not blocked, only not linked from anywhere. Linking from sites that are crawled (the website, the blog, the other docs) is the fix.
- Entity presence: Wikidata items for MOI and Sarva Labs, Crunchbase, LinkedIn, GitHub. Wikidata was being prepared by Sai Kiran; whether the items exist is unknown. ASK: Sai Kiran. Matching descriptions across those profiles was not done as of 2026-09-10.
- A checklist titled "Diagnostics (Beta): Improve your domain for AI agents", pasted on 2026-09-09 and inferred to come from Cloudflare's dashboard, drove the discovery layer. Its levels, as pasted:
  - Level 1: robots.txt, AI crawler rules, Content Signals, Markdown Negotiation, Sitemap.
  - Level 2: API Catalog, Link Headers, Auth.md.
  - Level 3: OAuth discovery, A2A agent card, Skills Index, MCP server card, Web Bot Auth, WebMCP.
  - Commerce items such as x402.
  In the files read, Level 1, the API catalog, Link headers and the Skills Index exist, and no file for the rest was found. Whether the checklist still reads this way is unknown.

## What the September sweep found and scored
Scores are SEO, GEO and AEO out of 10, reported to Rahul on 2026-09-10 and describing the fixed branches. The "after" scores for docs.moi.technology and moi.technology were recorded as "so far". On 2026-10-03 the live sites still show the before state (`the-layer.md`).
| Property | Before | After |
|---|---|---|
| docs.moi.technology | 3 / 4 / 3 | 8.5 / 9 / 8.5 |
| voyage-docs.moi.technology | 3 / 3 / 3 | 9 / 9 / 9 |
| cocolang.dev | 3 / 2 / 3 | 9 / 9.5 / 9 |
| js-moi-sdk.docs.moi.technology | 3 / 4 / 3 | 9 / 9 / 9 |
| moi.technology | 5 / 4 / 3 | 7 / 6 / 5 |
The 2 on cocolang.dev was Cloudflare answering 403 to AI crawlers. The stated gap to 10 was external authority: mentions and third-party listings. Other results from 2026-09-09: linkinator found one dead link, the guardian genesis file in `docs/guard/setup-guardian.md` (still 404 on 2026-10-03); the docs sites were 99 to 116 percent visible without JavaScript and the website's home page 15 percent (the way the percentage was computed is unknown, so do not quote it); Vale found 0 violations in 104 files; 135 of 135 JSON-LD blocks validated; Lighthouse SEO was 100, 100 and 92 on three properties. PR #57 renders the marketing routes to HTML for the website's low figure; the header of its `scripts/ssg.mjs` says crawlers now receive the page content.
Coverage finding: of 216 campaign pieces, none linked to `docs.moi.technology`, and 54 percent were about the Agent Launchpad. Rahul's answer on 2026-09-17: application docs do not belong in protocol docs, so Launchpad questions are answered by the Launchpad's own docs and the use-case pages on moi.technology. Backlinks are fine.

## Report shape
Use `templates/audit-report.md`. The sections of the 2026-09-10 status message, in order: Content changes, Frontmatter and metadata, `llms.txt`, `robots.txt`, Entity presence, Analytics, Audit scores, Status per property. The template keeps that order and puts a summary and the properties table at the top. Then "Next steps", separate and labelled as to-dos. State the date of every fetch.

## Repeating the audit
Nobody scheduled a repeat. The weekly live check was removed on purpose (commit 77059a7: "no scheduled monitoring - live-site issues get handled as they surface", per maintainer preference; the maintainer is not named). Run it on request, after a major change to hosting, Cloudflare or a generator, and after each release that changes a version-coupled file (`discovery-files.md`). One batch pull request per round, not one per fix (`moi-devrel/ship`).

## Not yet known
- Where the scored reports of September are saved. ASK: Adithya.
- Whether the audit will be repeated on a schedule. ASK: Rahul.
- Whether a Wikidata item exists for MOI and for Sarva Labs, and their identifiers. ASK: Sai Kiran.
