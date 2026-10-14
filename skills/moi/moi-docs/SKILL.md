---
name: moi-docs
description: "Write, review, fact-check and keep current the pages on MOI's four docs sites (docs.moi.technology, voyage-docs, cocolang.dev, js-moi-sdk docs), and the search and AI-visibility layer of every MOI site. Use for \"write a docs page\", \"docs PR\", \"review the docs PR\", \"fact-check the docs\", \"docs style guide\", \"frontmatter\", \"description length\", \"sidebar position\", \"stub page\", \"noindex\", \"HowToSchema\", \"new docs site\", \"docs drift\", \"update the docs after a release\". Also for the geo branch: \"GEO audit\", \"AI visibility\", \"SEO\", \"AEO\", \"show up in ChatGPT\", \"can AI read our content\", \"robots.txt\", \"llms.txt\", \"content signal\", \"sitemap\", \"JSON-LD\", \"structured data\", \"crawler\", \"GPTBot\", \"IndexNow\", \"Search Console\", \"Bing Webmaster\", \".well-known\", \"does the layer still work\", \"docs PR merged, what now\". Holds the page standard, a page lint, templates, traps and a site checker. A blog post's own search rules belong to moi-blog, claim checks to moi-devrel/claim-check, commits and PRs to moi-devrel/ship."
---

# MOI docs: write, review and keep current the pages on the docs sites, and the search layer of every site

## What this covers
A page from nothing to a pull request on any of the four docs sites, the review of someone else's docs PR, the fact-check of a teammate's technical page against source, keeping a long-lived PR current, standing up a new site, and the sweep for pages that have drifted from a version, an id or the standard. Facts are as of 2026-10-03 (repo contents from the previous operator's clones, last fetched 2026-10-01; live sites read on 2026-10-03), except the pull request states, which were re-read on 2026-10-13 and 2026-10-14: moidocs #124, voyage-docs #5, coco-docs #12 and MOI-Website #57 have merged; js-moi-sdk #150 (SEO/GEO layer for the SDK docs) merged on 2026-10-14 and is live; voyage #447 (SEO/GEO front door for the Voyage app) merged on 2026-10-14 but is not live (voyage.moi.technology/llms.txt still answers 404 until the Voyage team deploys; last Voyage deploy 2026-10-06); moidocs #127 is open, waiting for Rahul's approval. Fetch `main` before you rely on any file named here, because the clones predate the merges. The rules a page must meet are in `references/page-standard.md`, each with its source.
One branch lives inside this skill:
- `geo`: the search and AI-visibility layer of every MOI site (the docs sites, the Voyage app, the website): `robots.txt` and its content signal, `llms.txt`, structured data, the sitemap, response headers, crawler access, the steps after a merge, audits and measuring visibility. Its runbook is `geo/GUIDE.md`. A job on that layer: skip to the `geo` table below and read `geo/GUIDE.md`. The checklist and the run table here are for a docs page.

Not covered: checking every claim against source (`moi-devrel/claim-check`, which this skill calls); commits, PRs, rebases and merges (`moi-devrel/ship`); blog posts and a post's own search rules (`moi-blog`, `moi-blog/references/geo.md`); house wording (`moi-devrel/references/house-style.md`, sections 1 to 3, and `moi-devrel/references/terminology.md`). `docs.wallet.moi.technology` has no known repo or owner. ASK: Rahul.

## Before you start
`SKILLS`, "the operator", "the previous operator" and `ASK: <person>` are defined in `moi-devrel/SKILL.md`. Run every command from the working copy of the docs repo you are in, with paths quoted. A step marked GATE needs the operator's explicit yes first (see Gates). The style guide `DOCS-STYLE-GUIDE.md`, the llms scripts, the schema components, the section cards and `robots.txt` came in with moidocs PR #124 (merged 2026-10-13), so they are on `main` of `sarvalabs/moidocs` once you fetch it; a clone fetched earlier has none of them. coco-docs differs too: PR #12 merged on 2026-10-05, so its `main` serves the Book under `/book/`, while an older clone serves `/docs/book/`. `references/page-standard.md` carries the guide's rules, so you do not need the file, and the lint reads each checkout's config to tell the states apart.
- [ ] Which site, which page, and the change in one line. The operator provides it. Ask: "Which site and page, and what should the reader be able to do afterwards?"
- [ ] The source of truth for every claim and the version it is true at: a release tag, an SDK version, a live read. The operator and the protocol team provide it. ASK: Gokul where the release note is.
- [ ] Access to the repo. `moidocs`, `voyage-docs` and `coco-docs` are private; an org admin grants it. ASK: Rahul. `js-moi-sdk` is public.
- [ ] The state of the sweep PRs. On 2026-10-14 #124 (moidocs), #5 (voyage-docs), #12 (coco-docs) and #150 (js-moi-sdk) had merged, and #447 (voyage) had merged but was not live; #127 (moidocs, skills index to Coco 0.9.3) was open. Read it again (`gh pr view <N> --repo sarvalabs/<repo> --json state,mergedAt`, when the task allows a `gh` call), because it decides which files exist (`references/sites.md`).
- [ ] Tools: Node 16.14 or newer (18 or newer for coco-docs), or Python with Sphinx for the SDK. Installing them downloads packages: ask first.
- [ ] Identity: `bash "$SKILLS/moi-devrel/scripts/preflight.sh"` from inside the repo, with `PREFLIGHT_EXPECT_GH_LOGIN` (the work GitHub login) and `PREFLIGHT_WORK_DOMAINS` (the work email domains) set. The operator provides both; ASK: Rahul.
- [ ] A neighbouring page in the same folder, to copy its conventions.
- [ ] For a review, a fact-check or an upkeep job: the repo and the PR number, and the release the page documents.

## The run (write or change a page)
| # | Step | What to do, and the command | Done when |
|---|---|---|---|
| 1 | Get the repo | GATE (a clone downloads): `git clone git@github.com:sarvalabs/<repo>.git`, then `cd <repo>`. The SDK docs are the folder `docs/` of `sarvalabs/js-moi-sdk` | You are inside the working copy |
| 2 | Place it | Site and folder from `references/sites.md`. Read the neighbour page. Read the state of the sweep PRs | You can say where the file goes and which state the repo is in |
| 3 | Branch | GATE for the fetch: `git fetch origin`, then `git switch -c docs/<short-name> origin/main`. Do not push | A branch exists |
| 4 | Write | Copy a template: `cp "$SKILLS/moi-docs/templates/page-moidocs-concept.md" docs/learn/fundamentals/<name>.md` (others in `templates/README.md`). Steps in `references/write-docusaurus.md` or `references/write-sphinx.md` | No `FILL-IN` left <!-- slop-lint:ignore --> |
| 5 | Lint | `python3 "$SKILLS/moi-docs/scripts/docs-page-lint.py" <page>`; on an existing page add `--added-lines-since origin/main` | 0 errors, every warning answered |
| 6 | Build and preview | GATE: `npm install` (a download). Then `npm run build` and `npm run start`. SDK: from `docs/`, check that `pwd` ends in `/docs`, then `rm -rf build && make html` (it deletes `./build`) | The operator has seen the page |
| 7 | Check the claims | `mkdir -p claim-check-<slug> && printf '*\n' > claim-check-<slug>/.gitignore`, then `python3 "$SKILLS/moi-devrel/claim-check/scripts/extract-claims.py" --all <page> > claim-check-<slug>/claims-candidates.csv && cp -n claim-check-<slug>/claims-candidates.csv claim-check-<slug>/ledger.csv`. Keep `claims-candidates.csv` untouched: `moi-devrel/claim-check` step 8 needs it for `--dropped`. Give every row a verdict (method: `moi-devrel/claim-check`). Technical page from a teammate: `references/fact-check-a-pr.md` | `python3 "$SKILLS/moi-devrel/claim-check/scripts/ledger-status.py" claim-check-<slug>/ledger.csv` exits 0. The folder ignores itself, so the ledger stays out of git |
| 8 | Polish | `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" <page>`; read it aloud once | The operator has read the final text |
| 9 | Commit | Only when asked, with the work identity and no AI line. `moi-devrel/ship` | A local commit with no generated file |
| 10 | PR | GATE. `moi-devrel/ship`, body from `templates/pr-description.md`, then `references/pr-upkeep.md` | The preview comment is on the PR |
| 11 | After merge | Open the live page. A change to config or to a machine file (robots, llms, sitemap, `.well-known`) goes to the `geo` branch: `geo/GUIDE.md`, step 8 | The live page shows the change |
| 12 | Hand back | The format at the end | The operator has read it |

The other jobs, first move each (steps in the reference named in the next table):
| Job | First move |
|---|---|
| Review a docs PR | Read it with `gh pr view <N> --repo sarvalabs/<repo>` (read-only), fetch the head (GATE), lint the changed pages with `--added-lines-since` the merge base, draft in a self-ignoring `docs-review-<N>/` folder. The operator posts |
| Fact-check a teammate's page | Name the release the page documents, start a `moi-devrel/claim-check` ledger, read source at that tag, reconcile the counts |
| Keep a PR current | Rebase, diff the pages against `main`, re-read the PR body against the diff, draft the reply to the reviewer |
| Sweep for drift | Lint the changed pages and the whole tree, grep the version-coupled files, read the live network |
| Stand up a site | Decide scope with Rahul, then follow the twelve steps and hand the machine layer to the `geo` branch (`geo/GUIDE.md`) |

## Which file to read
This skill's own files:
| Doing | Read |
|---|---|
| Which repo, how it builds, who reviews, what is unknown | `references/sites.md` |
| A page on moidocs, voyage-docs or coco-docs | `references/write-docusaurus.md`, then `references/page-standard.md` |
| A page on the js-moi-sdk docs | `references/write-sphinx.md` |
| What a page must meet, with sources | `references/page-standard.md` |
| Reviewing someone's docs PR, drafting the comments | `references/review-a-pr.md`, `templates/review-comments.md` |
| Checking a teammate's page against source | `references/fact-check-a-pr.md`, `templates/fact-check-report.md` |
| Keeping a PR open for weeks; rebases; the PR body | `references/pr-upkeep.md`, `templates/pr-description.md` |
| A new docs site | `references/new-site.md` |
| Pages tied to a version or an id; the sweep after merges | `references/drift.md`, `templates/drift-sweep-log.md` |
| A term you do not know (frontmatter, stub, noindex, anchor, toctree, preview) | `references/page-standard.md`, section Terms |
| Something broke with no error | `references/traps.md` |
| Testing a change to this skill | `evals/evals.md` |

The `geo` branch takes over for anything about the search or AI-visibility layer of a whole site. One page's own frontmatter, description, `noindex` mark or schema call stays here.
| Asked to | Go to |
|---|---|
| Check that `robots.txt`, `llms.txt`, the sitemap, JSON-LD, headers and crawler access work on a site; "does the layer still work" | `geo/GUIDE.md` |
| Allow or block a crawler; where the content signal goes | `geo/GUIDE.md`, then `geo/references/crawlers.md` |
| The GEO pull request merged, what now; Search Console, Bing, IndexNow | `geo/GUIDE.md`, step 8 |
| Audit a property for search and AI visibility; "GEO audit"; why an assistant does not cite a site | `geo/GUIDE.md`, step 9 |
| Measure AI visibility, or put a visibility figure on a slide | `geo/GUIDE.md`, step 9 (`geo/references/measure.md`) |
| A release or a moved page changes a catalog, a skills index or a sibling-site list | `geo/GUIDE.md`, then `geo/references/discovery-files.md` |

## Facts that fail silently
| Rule | The incident |
|---|---|
| Quote a `description` that contains a colon and a space | The Docusaurus build fails with a YAML error |
| Start the file with `---` on line 1 | A blank line above it makes the site ignore the whole frontmatter |
| Keep a heading's old anchor with `{#old-anchor}` | Rewording changes the anchor and links land at the top; nothing reports it |
| Mark a stub, and unmark it in the change that finishes it | A finished page that kept the mark never appears in search; a template sample page reached the sitemap |
| Diff the pages against `main` after every rebase | Commit `0899368` (2026-09-17) restored a tutorial that a rebase had reverted to an older copy |
| Never edit a generated file; only js-moi-sdk commits them | The next build overwrites an edit; #150 is 22,549 added lines, mostly generated |
| Read the PR body against the diff before each push | Three of five sweep PR bodies were stale on 2026-10-02 |
| Know which state the checkout is in before you write | A clone fetched before the merges is stale. Before #12 (merged 2026-10-05) the Book of coco-docs was at `/docs/book/` and 27 of its 36 pages had no `description`; now it is at `/book/`. Before #124 (merged 2026-10-13) moidocs had no section cards and no `HowToSchema`, so a tutorial from the template would not resolve its import (lint run, 2026-10-03; not built). Fetch `main` first |
| On moidocs, voyage-docs and coco-docs a merge to `main` publishes. No manual deploy step is recorded | Cloudflare Pages builds `main` to production on every merge. The js-moi-sdk docs and wallet docs pipelines are unknown (`references/sites.md`); ASK: Gokul, Rahul |
| Check what the live network serves before you write "live" | `net.NetworkID` is in the JSON-RPC page and the devnet answered "method not available" on 2026-10-03; the state on 2026-10-13 is unknown, so read the wire again |
| Docs are the weakest source | Operation-code numbers on docs.moi.technology were swapped against the node source in August 2026 |
| No application docs in protocol docs | Rahul had the Launchpad section removed from #124 (2026-09-17) |
| Reconcile counts in a review | "27 errors" sat over a table of 26 and a list of 25 (2026-08-21) |
| Do not report work that was not done | A status line was removed on 2026-09-10 for claiming an action not taken |

## Gates
Nothing below happens without the operator's explicit yes in this conversation:
- Clone, fetch, `npm install`, `pip install`, `npx` anything and any other download. Say the source first.
- Push, open, update, comment on, review, approve, request changes on, merge or close a PR (`moi-devrel/ship`). A review or fact-check is drafted as a local file and the operator posts it.
- Creating a repository, a Cloudflare Pages project, a DNS record, or setting a repository secret or variable.
- A deploy or manual workflow run; a rebase or history rewrite of a pushed branch; deleting a remote branch.
- Spending devnet funds or deploying a logic while proving a sample. Reads (`net.Version`) are free.
- Sending a question to Gokul, Rahul or anyone: Claude drafts, the operator sends.
- Uploading or sharing a file in cloud storage (Drive, R2). Anything on a VM, a database migration or an admin write on production is not docs work: stop and ASK: Upendhar.
- Switching the git or `gh` identity; adding an AI co-author line or "generated with" footer (never).
- Sub-agents: only when the operator asks, with the count and model stated first.
- Audit and handover tasks stay local and read-only: plain `git`, and no `gh` call about pull requests unless the task allows it (`moi-devrel/references/consent-and-identity.md` section 1).
- The `geo` branch adds gates for search-engine submissions, Cloudflare dashboard changes and crawler policy: `geo/GUIDE.md`.

## Keys and access
Names only. Building and writing a docs page needs no secret: "Env vars: none. The site builds with no secrets" (the docs sites are not recorded in the handover docs: the 4 October dependency list (now only in git history) covers products, not docs sites). What you need is access: a work GitHub identity in `sarvalabs` and read access to the three private docs repos (ASK: Rahul); read access to go-moi, go-pisa and cocolang to check node claims (ASK: Rahul); the Cloudflare account owner is unrecorded (ASK: Rahul). The search-engine logins and the IndexNow key are in `geo/GUIDE.md`. `npm_token`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY` and `R2_ACCOUNT_ID`, `R2_BUCKET`, `R2_PREFIX` belong to the SDK team and DevOps and publish packages and the skill zip, not docs. Where each lives: `moi-devrel/references/keys-and-access.md`. Claude never handles a recovery phrase, including a throwaway one.

## Hand-back
```
Produced: <page paths, lint result, build result, preview link or "not run">
Checked against: <source and ref for each technical claim, ledger path>
Remaining: <numbered, each with who owns it>
Not verified or simulated: <say so, or "none">
Ready: yes or no, because <one reason>
Next steps: <one to three>
```
Ready is yes only when the lint has 0 errors, the build passed, the operator saw the preview and every claim has a verdict. A status lists work that was done; a to-do is labelled. Work on the `geo` branch hands back with the block in `geo/GUIDE.md`.
