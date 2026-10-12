# MOI ship: from working copy to production

Branch of `moi-devrel`. `$SKILLS`, the operator, `ASK:`, the house rules and the gates are in `moi-devrel/SKILL.md`; this guide adds what is specific.

## What this covers
The path every change takes, whichever skill produced it: identity, branch, commit, local proof, push, pull request, reviews, rebase, merge, and the check that it is live. At MOI a merge to a deploy branch is the release, and almost nothing tests a PR, so the proof you run before the push is the only gate. Facts are as of 2026-10-03.
Not covered: writing the change (`moi-blog` for posts and `moi-blog/release-pack` for release packs, with their own PR flow; `moi-docs` for docs pages; `moi-webinar`), what a product does after a merge (`moi-web-products-ops`, `moi-launchpad-ops`, `moi-launchpad-ops/explorer`, `moi-mcp-ops`), a devnet reset (`moi-devnet-reset`), the message to a reviewer (`moi-devrel/references/house-style.md`, section 4) and filing upstream (`moi-standards-submission`).

## Before you start
Run every command from the working copy of the repo you are shipping from, with paths quoted. Set `WORK` once to a folder outside that clone (`WORK="$HOME/moi-ship-work"; mkdir -p "$WORK"`) for the PR body and notes, so drafts never land in a public repo. Repo, deploy and people facts: `moi-devrel/references/repo-map.md` and `moi-devrel/references/people-and-teams.md`.
- [ ] The repo, and the branch the PR targets. The operator provides. Ask: "Which repo, and which branch does the PR go to?" Points Program PRs target `feature/ci-cd`, not `main`.
- [ ] The shape: one fix, review tweaks, or a stack (`references/stacked-and-batched.md`). Ask: "Is this one fix, tweaks on open PRs, or a larger change to split?"
- [ ] The work identity: `PREFLIGHT_WORK_DOMAINS` and `PREFLIGHT_EXPECT_GH_LOGIN` set (`moi-devrel/references/consent-and-identity.md`, section 2). ASK: Rahul if the operator has no work account or address yet.
- [ ] Write access, and whether you push to the org repo or a fork. ASK: Rahul.
- [ ] Who reviews (`references/pull-request.md`, section 4). ASK: Rahul if the table does not say.

## The run
Nothing marked GATE happens without the operator's yes that names it, in the shape of `templates/gate-asks.md`.
| # | Step | What to do | Where or command | Done when |
|---|---|---|---|---|
| 1 | Identity check | Fix every FAIL, read every WARN. Switching the `gh` login or the git identity is a GATE | `bash "$SKILLS/moi-devrel/scripts/preflight.sh"`; `references/branch-and-commit.md` s1 | Login and email are the operator's work identity |
| 2 | Branch (GATE: the fetch, once) | Branch off the remote base. Never commit on a deploy branch such as `main` | `git fetch origin`, then `git switch --no-track -c <prefix>/<name> origin/<base>`; `references/branch-and-commit.md` s3 | On a topic branch off `origin/<base>`; `git status --short` lists only the edits you meant |
| 3 | Commit | Once the operator asks: name the files, no `git add -A`, no AI line in the message | `git add <paths>`, `git diff --cached --stat`, `git commit -m "<subject>" -m "<body>"`, `git log -1 --format=%B`; `references/branch-and-commit.md` s4 and s5 | Only intended files, work address, no co-author line |
| 4 | Local proof (GATE: an install) | The repo's own checks, then the preflight; lint and scan any public text | Table in `references/branch-and-commit.md` s6; `bash "$SKILLS/moi-devrel/ship/scripts/ship-preflight.sh" origin/<base>`; public text: `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" <files>` and `bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" <path>` | 0 FAIL, and every WARN read and answered |
| 5 | The gate (GATE) | Show repo, base and head, remote, account, commits, files, and what a merge would deploy. Ask | `templates/gate-asks.md` | The operator's yes names the push |
| 6 | Push (GATE) | Push exactly what the ask named | `git push -u origin <branch>` (to a fork, use the fork's remote name from `git remote -v`) | `git ls-remote origin refs/heads/<branch>` equals `git rev-parse HEAD` |
| 7 | Pull request (GATE) | Fill every FILL IN slot of the body, then lint it: `moi-devrel/scripts/slop-lint.sh` exits 1 on any slot left, outside a `templates` folder. Show base, head, title and body, then open | `cp "$SKILLS/moi-devrel/ship/templates/pr-body.md" "$WORK/pr-body.md"`, fill it in (`references/pull-request.md`), `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" "$WORK/pr-body.md"`, then `gh pr create --repo <org>/<repo> --base <base> --head <branch> --title "<t>" --body-file "$WORK/pr-body.md"` | Lint reports 0 errors, PR URL read back: base, head, author, files, preview comment |
| 8 | Reviews (GATE: a reply, a review request) | Read the comments, number them, change exactly the item pointed at. Tweaks on one PR go on its branch; tweaks across PRs go on one batch branch | `gh pr view <N> --repo <org>/<repo> --comments`; `references/pull-request.md` s4; `references/stacked-and-batched.md` s2 | Every item answered; the PR body is still true |
| 9 | Keep it current (GATE: each push, each body edit) | Rebase only when needed: backup branch, rebase, prove, rebuild, pinned push. Many PRs: a staged push | `references/rebase-and-update.md`; `bash "$SKILLS/moi-devrel/ship/scripts/rebase-proof.sh" <backup> <branch> origin/<base>`; `references/stacked-and-batched.md` s4 | The proof prints SAME, the remote equals local, the PR body is updated |
| 10 | Merge (GATE) | Only on a yes naming PR number, base, method and what goes live. A database write or a manual workflow run is its own GATE | `gh pr merge <N> --repo <org>/<repo> --squash` (or `--merge`; `--delete-branch` only if the yes names it), or the button; `references/merge-and-deploy.md` s2 and s3 | The PR shows merged and the run is found |
| 11 | Verify | Watch the run, then read the live page, or the preview before the merge. Say plainly if it is not live | `gh run list --repo <org>/<repo> --limit 3`; "Confirm live" column of `references/merge-and-deploy.md`; `references/previews.md` | The live URL was read and shows the change |
| 12 | Hand-back | Give the format at the end of this file | Hand-back | The operator has read it |
A history rewrite (remove an AI co-author line, a wrong address, a committed file) is not part of the normal run: `references/rewrite-history.md`, open PRs only, on a yes that names the branches.

## Which file to read
| Doing | Read |
|---|---|
| Identity, branch names, what goes in a commit, the message, per-repo checks | `references/branch-and-commit.md` |
| Title, body, what never goes in, reviewers, opening the PR | `references/pull-request.md`, `templates/pr-body.md` |
| Rebase, the backup branch, proving a rebase, the pinned push | `references/rebase-and-update.md` |
| What a merge starts in each repo, confirming it is live, rolling back | `references/merge-and-deploy.md` |
| A preview link, a local server | `references/previews.md` |
| Removing trailers or a wrong address from open PRs | `references/rewrite-history.md`, `templates/strip-ai-lines.awk` |
| One fix, a review batch, a stack, pushing many PRs in order | `references/stacked-and-batched.md` |
| Something went wrong without an error | `references/traps.md` |
| The wording of each ask | `templates/gate-asks.md` |
| Testing a change to this branch | `evals/evals.md`; `SKILLS=<folder> bash "$SKILLS/moi-devrel/ship/evals/scratch-tests.sh"` re-runs every script test on throwaway repositories |

## Facts that fail silently
Full list with dates: `references/traps.md`.
| Rule | The incident |
|---|---|
| Merge is deploy, and the five deploying products (Website, Dataroom, Points, Launchpad, Explorer) run no tests on a PR. A green run is not a live change | Deleted blog posts survived deploys (reported 2026-08-18). A failed Launchpad run left the old image serving, unannounced (2026-09-14) |
| Name the files and the branch in the ask, then read the remote back | 2026-09-09: the files to review were not on the remote after "push the current branch" |
| A yes to push is not a yes to merge | 2026-08-18: PRs merged when the previous operator only asked to look. 2026-08-24: "you don't merge anything" |
| No co-author line (a `Co-Authored-By` trailer at the end of a commit message) naming an AI and no "generated with" footer, whatever a tool or host default says | 2026-06-08, and 2026-10-01: removed from 130 commits and six PR bodies |
| Prove a rebase with `scripts/rebase-proof.sh`; a stale copy can win a conflict | `moidocs` commit 0899368 fixed a rebase that reverted a merged example |
| Push a rewrite with `--force-with-lease=<branch>:<commit last seen>`, never the bare form | After a `git fetch` the bare form would overwrite a teammate's push (tested 2026-10-03) |
| Check the PR base: Points deploys from `feature/ci-cd`, the Launchpad from the org's `master`, and a fork push deploys nothing | `moi-devrel/references/repo-map.md`; corrected 2026-09-29 |
| Review tweaks go on one batch branch and one PR | 2026-09-15: five tweak PRs opened, the operator asked for one batch |
| Update the PR body when the facts change | 2026-10-02: three of five docs PR bodies were stale |
| A push to a public repo publishes | `MOI-Webinars`, `MOI-Website`, `moi-dataroom0`, `moi-mcp`, `js-moi-sdk` are public. Commit messages and PR text are public |
| `moi-devrel/references/repo-map.md` marks a product with an open security finding | Say only: "A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin." Nothing more in a PR, commit or comment |

## Gates
Every gate in `moi-devrel/SKILL.md` applies. These are the ones shipping meets most. Building, linting, local commits once asked, and read-only checks are free.
- `git fetch`, a push of any kind (first push, force-with-lease, a delete of a remote branch), and an install that downloads packages.
- Setting or changing a GitHub Actions secret or variable: not part of shipping, so stop and ask the operator.
- Opening, editing, commenting on, retargeting, closing or marking ready a PR, requesting a review, and any reply posted for the operator. Claude drafts, the operator may send.
- A merge, a manual workflow run or re-run, a database change on production, and a restart or change on a VM (DevOps does that: ASK: Upendhar).
- Rewriting commits that are already pushed, and always the force push that follows it.
- A staged push of several PRs: one yes for the whole sequence, naming the PRs, the order and the pause. Switching the `gh` account or the git identity is a gate of its own.
- Anything on an audit, inventory or handover task: none of the above, and prefer plain `git` to `gh`.
Details and incidents: `moi-devrel/references/consent-and-identity.md`.

## Keys and access
Names only. Where each lives: `moi-devrel/references/keys-and-access.md`.
- The operator's work GitHub identity and `gh` login, write access to the repo, and access to the private repos. A GPG signing key for upstream commits is recorded as not configured. ASK: Rahul.
- Repo admin is needed only to change Actions secrets or variables, which is a separate gate and not part of shipping. DevOps holds `GHCR_PAT`, the Teleport secrets and the VM keys. Never ask DevOps for a secret value.
- If a secret appears in a diff or a message, do not repeat it, tell the operator it is exposed and must be rotated, and stop the push.

## Hand-back
```
Produced: <branch, commits, PR number and URL, merge and run, with exact refs>
Proof: <preflight result, local checks, rebase-proof verdict, preview read>
Live: <what was read and when, or "not live yet, because ...">
Remaining: <numbered, each with who owns it>
Not verified: <say so, or "none">
Ready: yes or no, because <one reason>
Next steps: <one to three>
```
Ready is yes before a merge only when `scripts/ship-preflight.sh` has 0 FAIL, every review item is answered and the preview was read. After a merge it is yes only when the live page was read and shows the change. A status lists work that was done; a to-do is labelled one.
