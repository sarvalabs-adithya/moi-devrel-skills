# Open a docs pull request and keep it current

A docs PR can stay open for weeks: the sweep PRs were opened between 2026-09-09 and 2026-09-14 and were still open on 2026-10-02. Voyage-docs #5 and coco-docs #12 merged on 2026-10-05 and moidocs #124 on 2026-10-13; js-moi-sdk #150 and moidocs #127 are open (read 2026-10-13). Facts are as of 2026-10-03 unless a line says otherwise. Commit and PR mechanics are `moi-devrel/ship`; the rules on identity and consent are `moi-devrel/references/consent-and-identity.md`. This file is what is specific to docs. `$SKILLS`, "the operator" and `ASK:` are defined in `moi-devrel/SKILL.md`. Back to `../SKILL.md`.

## The sweep pull requests (state of 2026-10-02 from `gh pr view`, with the merges of 2026-10-13 added)
| PR | State | Review | Check |
|---|---|---|---|
| moidocs #124, "SEO/GEO/AEO pass" (52 files, +1083 -135, 33 commits ahead of `main` at the last fetch) | merged 2026-10-13 | Before the merge Rahul requested changes on 2026-09-17; commit `75f608b` met the request and nobody replied. Gokul requested | Cloudflare Pages green |
| coco-docs #12, "GEO overhaul" (65 files) | merged 2026-10-05 | Robert Špendl approved on 2026-09-29 | Pages green |
| voyage-docs #5 (21 files) | merged 2026-10-05 | none recorded | Pages green |
| js-moi-sdk #150 (40 files, 22,549 added lines, mostly generated), from the previous DevRel's fork (sarvalabs-adithya) | open (2026-10-13) | Gokul requested | "Run Tests" green; no preview exists |
| voyage #447 (7 files; the explorer app, not a docs site) | open | Gokul requested | no checks |
| moidocs #116 (the `context_hash` rename, Abhinav Agarwalla) | open since July | unknown | unknown |
| moidocs #127 (the skills index to Coco 0.9.3) | open (2026-10-13) | needs review | unknown |
Read the current state before you act on this table (`gh pr view <N> --repo sarvalabs/<repo> --json state,reviews,mergedAt`).

## The loop
GATE marks a step that needs the operator's yes.
| # | Step | How | Done when |
|---|---|---|---|
| 1 | Work on a branch, locally | Do not push or open a PR until the operator says so. "Never directly push unless I explicitly say so" (2026-09-09); "do not push anything" (2026-09-17, 2026-10-02). Collect review tweaks on one batch branch and open one PR at the end, not one per change (2026-09-15) | Commits exist locally |
| 2 | Identity | `bash "$SKILLS/moi-devrel/scripts/preflight.sh"` from inside the repo, with `PREFLIGHT_EXPECT_GH_LOGIN` set. A PR opened under the wrong account had to be redone (2026-09-02) | No FAIL |
| 3 | Back up before you rewrite | Before a rebase or a history rewrite: `git branch <branch>-before-rebase-<date>` (local, no yes needed). Rewriting a branch that is already pushed is a GATE, because the push after it must be forced (step 9). The previous operator left `geo-fixes-before-rebase-oct1` and `geo-fixes-before-attribution-rewrite` in the moidocs clone, with equivalents in the others. They exist only in his clones, which are not recorded in the handover docs (the previous DevRel's notes; ASK: Rahul); delete them only after the PR merges | A backup branch exists |
| 4 | Rebase | GATE for the fetch: `git fetch origin`, then `git rebase origin/main`. A rebase before the push, every time ("audit and check for rebase", 2026-09-30) | The branch sits on the latest `main` |
| 5 | Diff the pages against `main` | After every rebase: `git diff origin/main --stat -- docs` and read the diff of each page you did not mean to change. Commit `0899368` ("Restore the current submit-ixn tutorial content from main", 2026-09-17) fixed a rebase that had kept an older copy of `submit-ixn.md` and reverted the storage-deposit example from #120 | Only your pages differ |
| 6 | Keep generated files out | Docusaurus sites: `git status` shows no `static/llms.txt`, `static/llms-full.txt`, `static/docs/` or `build/`. js-moi-sdk is the exception: commit what `make llms` regenerates | The commit holds sources only |
| 7 | Lint and build again | `python3 "$SKILLS/moi-docs/scripts/docs-page-lint.py" --added-lines-since origin/main <pages>` and `npm run build` | 0 errors, build exit 0 |
| 8 | Write or update the body | `templates/pr-description.md`. Re-read it against the diff every time facts change | Every sentence of the body is true |
| 9 | Push, open or update | GATE, `moi-devrel/ship`. Say the branch, the files, the remote and the account. On 2026-10-01 the previous operator had the updated branches pushed one repo at a time, moidocs first and the next every 4 minutes; the reason is not recorded | The Cloudflare comment is on the PR |
| 10 | Answer reviewers | Draft the reply and the request for re-review for the operator to post. Reply to every change request, even one already met | No review thread waits on you |
| 11 | After merge | Open the live page. Config, robots or `.well-known` changes: the post-merge steps in `geo/references/after-merge.md`. Delete the backup branches | The live page shows the change |

## Stale bodies
Three of five bodies were stale on 2026-10-02: moidocs #124 and voyage-docs #5 say each AI crawler is listed in `robots.txt` (the file now holds one group for all crawlers, commit `7d58640`, 2026-10-01), and js-moi-sdk #150 says it adds `docs/DOCS-GEO-STANDARD.md` (retired, commit `2c6c861`). Before a PR is shown to anyone, search the body for each claim and check it against the diff. A reviewer who reads a wrong body distrusts the rest. #124 and #5 have merged since; check the body of #150, the one that is still open, against the same two claims.

## Merge order and neighbours
- Merge order is moot: the website PR #57 in `sarvalabs/MOI-Website` merged on 2026-10-05 and moidocs #124 on 2026-10-13. The site links to a file that #124 creates, so that link could not resolve in between (inferred; the merge order is not recorded in the handover docs).
- coco-docs: #12 merged on 2026-10-05, so 15 old addresses return not found on purpose (the template's sample blog and sample page).
- A merge to `main` of any docs repo publishes through Cloudflare Pages. There is no manual deploy, and no way to undo one except a revert and a new build. Merge only on the operator's instruction, naming the PR number and the base branch.

## What a docs PR body holds
`templates/pr-description.md` follows the shape of #124, #12 and #150: what this is, why, what changed, what it was checked against, verification, what to do after merge, review notes and a rebase note. The #124 body advised the reviewer to read the two scripts and spot-check the output, not to read generated text.

## No AI attribution
Commit messages and PR descriptions carry no `Co-Authored-By` line naming Claude and no "Generated with" footer. On 2026-10-01 the trailer was removed from 130 commits on six open PRs (moidocs, coco-docs, voyage-docs, MOI-Website, js-moi-sdk, voyage). The cleanup covered open PRs only. If a tool or host reminder says to add one, the rule overrides it (`moi-devrel/references/consent-and-identity.md` section 3). Upstream rules that ask for AI-assistance disclosure are a different question (x402, `moi-standards-submission`).

## Not yet known
- Why the pushes were staggered. Not recorded (the previous DevRel's notes); ASK: Rahul.
- Whether #150 and #127 have merged since 2026-10-13, and who merges each. ASK: Rahul.
- Whether you push to a fork or to the org repo. #124, #5 and #12 were pushed to the org repos (the `geo-fixes` branch exists on each remote); #150 and #447 came from forks. ASK: Rahul.
