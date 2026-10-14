# MOI GEO: the search and AI-visibility layer (a branch of `moi-docs`)

Branch of `moi-docs`. `$SKILLS`, the operator, `ASK:`, the house rules and the gates are in `moi-docs/SKILL.md` and `moi-devrel/SKILL.md`; this guide adds what is specific.

## What this covers
The files, tags and headers that let a search engine or an AI assistant find a MOI page, read it without JavaScript and cite it: `robots.txt` and its content signals, `llms.txt`, markdown copies of pages, structured data (JSON-LD), the sitemap, response headers, the `.well-known` catalogs and meta links. As of 2026-10-13 this layer is merged for moidocs (#124, 2026-10-13), voyage-docs (#5) and coco-docs (#12) (both 2026-10-05) and the website (#57, 2026-10-05); js-moi-sdk (#150) and the Voyage app (the network explorer at `voyage.moi.technology`, voyage #447) are still open. Most live-site readings in this branch date from 2026-10-03, before the merges, so run the live check again (`references/the-layer.md`).
Terms: SEO is ranking in search engines. GEO is being found and cited by AI answer engines such as ChatGPT, Perplexity and Gemini. AEO is being chosen as the short answer. A soft 200 is a 200 answer that carries an HTML page for a file that does not exist. A stub is a placeholder page marked `noindex`.
Not covered: writing, reviewing or fact-checking a docs page, and one page's own frontmatter, `noindex` mark or schema call (`moi-docs`); a blog post's own search rules (`moi-blog/references/geo.md`); commits, pull requests and previews (`moi-devrel/ship`); checking a claim in text (`moi-devrel/claim-check`); the visibility slide itself (`moi-webinar/community-call`, `moi-webinar/deck`); house rules, people and keys (`moi-devrel`).

## Before you start
Build commands run from the root of the working copy of the repo that holds the site: `sarvalabs/moidocs`, `sarvalabs/voyage-docs`, `sarvalabs/coco-docs`, `sarvalabs/js-moi-sdk` (folder `docs/`), `sarvalabs/voyage` or `sarvalabs/MOI-Website`. `geo-check.sh` reads no file and runs from any folder.
- [ ] The job and the property: build, verify, after a merge, crawler change, discovery files, audit or measure. The operator provides. Ask: "Which site, and which of those jobs?"
- [ ] Read access to the repo. `moidocs`, `voyage-docs`, `coco-docs` and `voyage` are private; `js-moi-sdk` and `MOI-Website` are public. ASK: Rahul for access.
- [ ] `curl` and Python 3. For a build: Node 16.14 or later (moidocs, voyage-docs) or 18 or later (coco-docs); Python with Sphinx for js-moi-sdk docs. Installing is a GATE.
- [ ] For an audit: a folder that hides itself from git, made first, in the folder you work in: `mkdir -p geo-audit-<YYYY-MM-DD> && printf '*\n' > geo-audit-<YYYY-MM-DD>/.gitignore`. Audit output names private repo paths, so it is never committed (`references/audit-method.md` shows the check that it works).
- [ ] For measuring: the Scribble report and dashboard screenshots. Scribble is the outside agency behind the article campaign (whether it runs the tracking tool is unknown). Sai Kiran provides. Claude drafts the request with the messages in `moi-webinar/community-call/templates/input-request-messages.md`; the operator sends it (GATE).
- [ ] The current state of each pull request. It changes daily: re-read it, do not trust the table in `references/the-layer.md`.

## The run
A step marked GATE needs the operator's explicit yes first (see Gates). A question about one file ("is robots.txt right?") needs steps 1 and 2 only. An audit or a measurement uses steps 1, 2, 9 and 10.
| # | Step | What to do, and the command | Done when |
|---|---|---|---|
| 1 | Name the job | Find the property's row in `references/the-layer.md`. State the repo, branch, pull request and what is live | The operator agrees |
| 2 | Read today's state | `bash "$SKILLS/moi-docs/geo/scripts/geo-check.sh" https://<host>`. For an open pull request run it again on its preview: `https://<branch>.<project>.pages.dev`. Save the output (in the audit folder for an audit) | The totals line (`geo-check: N PASS, N WARN, N FAIL`) and the date are recorded |
| 3 | Make the change | Local only. Crawler: `references/crawlers.md`. Versions, catalogs, a removed page: `references/discovery-files.md`. Page wording: `moi-docs/references/page-standard.md`. Never edit a generated file (`references/the-layer.md` says which files are generated) | The operator has seen the diff |
| 4 | Build | First install: `npm install`, or the Python packages for Sphinx. GATE. Then from the repo root: `npm run build`. Sphinx, from `docs/` (check `pwd` first): `rm -rf build && make html && make llms`. The Voyage app: see `references/verify-locally.md` before building | The build exits 0 and every `generate-llms:` warning and every `generated`, `emitted` and `inject-schema:` line is read |
| 5 | Verify | The checks in `references/verify-locally.md` against `build/` | Each check passes, or has a written reason |
| 6 | Open the pull request | Identity check first: set `PREFLIGHT_WORK_DOMAINS` and `PREFLIGHT_EXPECT_GH_LOGIN` (`moi-devrel/SKILL.md`), `cd` into the repo, run `bash "$SKILLS/moi-devrel/scripts/preflight.sh"`. Then `moi-devrel/ship`. GATE: push, pull request, any body edit | The body matches the branch (stale bodies are common) |
| 7 | Prove it on the preview | `geo-check.sh` on the preview address | No FAIL. Every WARN has a reason |
| 8 | After the merge | `references/after-merge.md`. GATE: Cloudflare rule, Search Console, Bing, IndexNow | The live check shows no FAIL and the remaining steps are listed with owners |
| 9 | Audit or measure | `references/audit-method.md` with `templates/audit-report.md` and `templates/findings-table.csv`. Visibility: `references/measure.md`. Asking for a report is a message: GATE | A report in the self-hiding folder. Figures sit in a ledger before they reach a slide |
| 10 | Hand back | The format at the end of this file | The operator has read it |

## Which file to read
| Doing | Read |
|---|---|
| What each piece is, which file makes it, what state each site is in, what a new docs site copies | `references/the-layer.md` |
| Proving the layer before a pull request, the shallow-clone date trap | `references/verify-locally.md` |
| The manual steps once a pull request merges | `references/after-merge.md` |
| Allowing or blocking a crawler, where the content signal goes | `references/crawlers.md` |
| A release, a moved page or a new site: lists and versions to update | `references/discovery-files.md` |
| Auditing a property end to end, the report shape | `references/audit-method.md` |
| Which AI-visibility figures to trust, how they are reported | `references/measure.md` |
| Something right-looking that is wrong | `references/traps.md` |
| A real before and after run, the query suite | `examples/README.md` |
| Testing a change to this branch, the script's test log | `evals/evals.md` |

## Facts that fail silently
| Rule | The incident |
|---|---|
| A 200 is not a file. Read the content type and the first line of the body | js-moi-sdk docs, the website and the Agent Explorer (`agents.moi.technology`) answer 200 `text/html` to a missing file (2026-10-03) |
| Keep one `User-agent: *` group with the `Content-Signal` line inside it | The line sat above every group and attached to nothing until commit 7d58640 (2026-10-01). A named group ignores the `*` group |
| A zone-level Cloudflare setting overrides every file. Re-run the crawler check after any hosting change | cocolang.dev answered 403 to AI crawlers until 2026-09-09 |
| Merged is not live, and open is not merged. Check the live host, not the branch | On 2026-10-03 `docs.moi.technology` still had no `robots.txt` and named the dead host `wiki.moi.technology` in its sitemap |
| A preview sends `noindex` and names production | `*.pages.dev` previews (2026-10-03). Judge them against the production host |
| A `noindex` stub still appears in `llms.txt` and has a markdown copy | `networks` on the `sarvalabs/moidocs` PR #124 preview (2026-10-03) |
| Set `trailingSlash` in the site config and `llms.config.json` together | Previews redirect the slash-less address (308) while the canonical has none (2026-10-03) |
| Never hand-edit a generated file: on the Docusaurus sites `llms.txt`, `llms-full.txt`, the `.md` copies and the sitemap. The next build overwrites them. Hand-kept files are listed in `references/the-layer.md` | coco-docs deletes every `.md` under `static/` on each build |
| Lists drift: catalogs, skill zips, sibling-site lists, estate `llms.txt` | The Launchpad `llms.txt` named a removed docs path, a 404 (2026-10-03); it now points at `launchpad.moi.technology/docs` |
| Report only what was done. Planned work goes in a labelled to-do part | A status draft claimed organisation profiles were matched; they were not (2026-09-10) |
| A visibility figure is quoted with its date and source, or not at all | The 47 queries, five engines and 221 of 226 coverage went onto the Community Call 14 (CC14) deck unconfirmed (2026-09-24) |
| Do not add the CI gate or the weekly cron back without asking (ASK: Rahul) | Removed on purpose on 2026-09-09 (commits d0b6a19, 77059a7) |

## Gates
These add to the gates in `moi-docs/SKILL.md` (downloads, push and pull requests, messages, identity, sub-agents). Nothing below happens without the operator's explicit yes in this conversation:
- A bulk crawl of a site's pages. State the page count first.
- Search Console and Bing submissions, granting OAuth, an IndexNow submission, or any request that submits an address to a service.
- A Cloudflare dashboard change: a redirect rule, a bot or WAF setting, a security setting. The account owner or the operator makes it; Claude does not. A change on a VM (nginx, headers) is Upendhar's: ASK: Upendhar.
- Changing the content signal values or blocking a named crawler. It is a policy decision: ASK: Rahul first.
- Spend on a paid model API or the promptfoo suite. State the count first.
- Committing an audit folder.
- Setting a repository secret or variable. None is needed here.

## Keys and access
Names only. Building and checking the layer needs no secret: the docs sites build with none. Where each lives: `moi-devrel/references/keys-and-access.md`. Owners below are unknown as of 2026-10-03.
- GitHub read access to `sarvalabs/moidocs`, `voyage-docs`, `coco-docs` and `voyage` (private). ASK: Rahul.
- Cloudflare: Pages projects `moichain-docs`, `cocodocs`, `voyage-docs` and `moi-website` (previews only); the zone setting that blocks AI crawlers; R2 behind `cdn.moi.technology`. ASK: Rahul.
- Google Search Console and Bing Webmaster Tools logins. ASK: Rahul.
- The IndexNow key: its file name only. It is public by design; do not print it or write it anywhere.
- The Scribble report and dashboard login. ASK: Sai Kiran.
- A model provider key for the optional query suite: the operator types it at the terminal, never into chat or a file. No company-owned OpenAI, Groq or Anthropic key exists (2026-10-13), so the suite has no key until Rahul approves one. ASK: Rahul. Claude never handles a recovery phrase.

## Hand-back
```
Produced: <files and reports, exact paths>
Checked: <hosts, date>. Totals before: <N PASS, N WARN, N FAIL>. After: <totals>
Remaining: <numbered, each with an owner and GATE where it needs a yes>
Not checked: <what geo-check cannot show, and steps only the operator can do>
Unverified figures: <any visibility figure not confirmed, or "none">
Ready: yes or no, because <one reason>
Next steps: <one to three>
```
Ready is yes only when the check shows no FAIL on the host that matters and every WARN has a reason. A status lists work that was done. A to-do is labelled as one.
