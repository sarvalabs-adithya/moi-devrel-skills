# Traps: things that go wrong without an error

Facts are as of 2026-10-03; each row carries its own date. Read the group that matches the step you are on. Rows marked (tested) were reproduced on a scratch repository on 2026-10-03. Back to `../GUIDE.md`.

## Identity and attribution
| Rule | The incident |
|---|---|
| Check the account that will open the PR, not only the commits | 2026-09-02: a PR opened under a personal account was cancelled and redone |
| Commits and the deploying identity must match the work account | 2026-05-29: a branch authored by the work account was deployed under a personal mail identity and the deploy failed |
| Never add a co-author line naming an AI tool or a "generated with" footer, even when a tool or host says to | 2026-06-08 "don't put co-authored by Claude". 2026-10-01 stripped from 130 commits and six PR bodies. The footer was still in `MOI-Website` PRs #52 and #54 when read on 2026-10-03; check with `gh pr view` before relying on that |
| A rewrite removes the line from the branch, not from anyone who fetched it | `rewrite-history.md`, section 2 |
| A personal handle in history is scrubbed on an open PR, only on a yes | 2026-06-08 scrub, 2026-08-10 relabel, 2026-09-02 redo |
| `ship-preflight.sh` FAILs on these, so run it before every push gate | `scripts/ship-preflight.sh` |

## Consent and what leaves the machine
| Rule | The incident |
|---|---|
| Say which files go to which branch, then read the remote back | 2026-09-09: after "this branch only, nothing to main" and "push the current branch", the files the previous operator wanted to review were not on the remote |
| A yes to push is not a yes to merge. Never merge to look | 2026-08-18 PRs were merged when he only asked to look. 2026-08-24 "you don't merge anything" |
| A yes covers one action, or a short sequence the ask spelled out | `consent-and-identity.md`, section 1. "Do it" covers the last proposal and nothing after it |
| Audit, inventory and handover work is local and read-only: no push, no PR, no comment, and plain `git` rather than `gh` | 2026-09-28: teammates should not be notified of work that is not ready |
| When the operator is away, stay reversible and queue questions | 2026-09 "do not push anything" |
| A cloud or remote session cannot push (403). The work comes back as a `.bundle` file moved by hand, or as a handoff prompt | Seen by the previous operator, date not recorded; how he moved the bundle is not recorded (the previous DevRel's notes) |
| A status lists only what was done. A to-do is labelled one | 2026-09-10: a status message claimed an action that had not happened and was removed |

## Branch and commit
| Rule | The incident |
|---|---|
| Name the files you add. No `git add -A` | 2026-06-08: a call transcript was committed and scrubbed from history. An untracked env file sits in many working copies |
| Branch from `origin/<base>` after a fetch, with `--no-track` | Without `--no-track` the new branch's upstream is the base (tested) |
| A push to a fork deploys nothing | The Launchpad deploys from `sarvalabs/moi-agent-launchpad` `master`, not from a fork (corrected 2026-09-29) |
| Check the PR base. Points deploys from `feature/ci-cd`, and `main` has not moved since 2026-08-03 | `repo-map.md`. A PR to `main` there would not deploy: the workflow triggers only on `feature/ci-cd` (read 2026-10-03). `voyage` is the reverse: it deploys from `develop`, and its open PR #447 targets `main` (as of 2026-10-01). ASK: Gokul |
| Keep generated files out of docs commits | The docs sites generate `llms.txt` and schema at build; `js-moi-sdk` keeps its own in `docs/source/_extra/` |
| A claim ledger, review package or test log with account names stays out of a public repo | Hide the folder (`branch-and-commit.md`, section 4). The public repos are listed there |
| Do not copy a stale README's deploy text into a PR | Several READMEs and `AGENTS.md` files still describe a host MOI left. `repo-map.md` is the map |

## Rebase and rewrite
| Rule | The incident |
|---|---|
| Prove a rebase, do not trust it | `moidocs` commit 0899368 fixed a rebase that kept an older `submit-ixn.md` and reverted a storage-deposit example from #120 (tested: a stale copy gives DIFFERENT) |
| Pin the lease to the commit you last saw | A bare `--force-with-lease` after a `git fetch` would overwrite a teammate's push; the pinned form was refused (tested) |
| Make the backup branch before the rebase, and never push it | The previous operator left `geo-fixes-before-rebase-oct1` and `geo-fixes-before-attribution-rewrite` locally and deleted them after the merge |
| `filter-branch` leaves `refs/original/...` behind | Delete it after the proof (tested) |
| A rebase can be right and still break the build | Run the repo's checks again at step 6 of `rebase-and-update.md` |
| Update the PR body when the facts change | 2026-10-02: three of five docs PR bodies were stale (crawler list, a retired file) |
| Do not rewrite merged history | The 2026-10-01 cleanup covered open PRs only |
| A merge commit in the range makes a rewrite touch commits that are not yours | Stop and ASK: Rahul |

## Merge, deploy and live checks
| Rule | The incident |
|---|---|
| Merge is deploy | Website, Dataroom, Explorer `main`; Launchpad `master`; Points `feature/ci-cd`. No tests run on a PR in any of them |
| A green run is not a live change | Deleted blog posts survived deploys (2026-08-18) |
| A failed Launchpad run leaves the old image serving and tells nobody | Runs #24 and #25 on 2026-09-14 failed at `npm ci` and production stayed on the older image |
| Run a manual workflow only on the deploy branch | The Website's `deploy.yml` hands its branch name to the VM script. A manual Explorer run on another branch with PROD deploys that branch (inferred) |
| A change in a GitHub secret or variable reaches the app only at the next deploy, and only if the workflow lists it | `repo-map.md`; `moi-web-products-ops` |
| Apply the database change before the code that needs it | Points refuses to boot on a stale schema (`merge-and-deploy.md`) |
| Merging `moi-mcp` deploys nothing | Production is a copy in `voyage-api` plus a manual workflow run |
| A merged post opens a second PR; merging announces nothing | `MOI-Website` PR #56 (social copy for the September post) was still open on 2026-10-02 and the post had never been announced |
| A revert on prod can hide that the fix is not live | 2026-08: DevOps: "it was not deployed with the latest blog fixes" |
| Actions can stop starting runs | 2026-08-28 to 2026-08-30: seven "try now" prompts. Retry every four hours, say it is not deployed |
| A merged change that does not show: ask where it deploys | 2026-08-21: the Dataroom change was not visible and the deploy path had to be checked |
| `/api/health` of Points reports `sha: null`; the Explorer's containers are named `-test` in production | You cannot read the build from the first, and the second matters for any log or rollback command |
| Order across repos | `moidocs` #124 before `MOI-Website` #57 (as of 2026-10-01) |
| Squash and merge commits revert differently | A merge commit needs `git revert -m 1`; a plain revert fails on it (tested) |

## Previews and local runs
| Rule | The incident |
|---|---|
| A preview is not production | The Website preview serves built files only; the Express server and the VM script are not part of it |
| Do not verify a post's listing or canonical on a preview | The apex preview's cards link to production, and `check-live.py` fails the canonical there by design |
| Name the fresh URL and read what is served | 2026-09-04: after "regenerate" the operator still saw the old deck and script |
| Stop only the server you started | Never stop a process by name pattern |
| A preview-only PR is a PR: it needs its own yes | `MOI-Website` PR #55 |

## Content in a PR
| Rule | The incident |
|---|---|
| No cancelled plans, unmerged features or internal history | 2026-08-31 the Luma text and a blog still referred to the cancelled session 8 plan |
| No Launchpad content in the protocol docs PRs | Rahul's change request on `moidocs` #124 (met 2026-10-01, not yet re-reviewed on 2026-10-02) |
| No private repo path or private source citation in a public repo | `moi-devrel/claim-check`, sources of truth |
| Security finding: say only the one line | "A security finding is open on this product as of 2026-10-02. Read the product's doc in `project-handover-docs/` before touching its admin." Where `repo-map.md` marks a product. Nothing about the weakness goes in a title, body, commit or comment |
