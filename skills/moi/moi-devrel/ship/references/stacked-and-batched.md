# One fix, a review batch, or a stack

Facts are as of 2026-10-03. Sources: the request history (2026-09-15 and 2026-10-01), the memory note on the Points audit stack, the docs-sweep PRs of 2026-10-01. The tree checks and the `--onto` rebase below were run on a scratch repository on 2026-10-03 (`../evals/evals.md`). Back to `../GUIDE.md`.

## 1. Pick the shape before the first branch
| Shape | Use when | Rule and evidence |
|---|---|---|
| Isolated fix | One change that stands alone | One branch, one PR, nothing else on it. "Create a PR with just this fix, not the other stuff, isolate" (the previous operator, request history). Check: `git diff --stat origin/<base>...HEAD` lists only that fix. Move a fix off a busy branch with `git cherry-pick <commit>` on a fresh branch from `origin/<base>` |
| Review batch | The operator is reading PRs and asks for tweaks | Do not open a PR per tweak. On 2026-09-15 five tweaks became five PRs (#16 to #20) and the operator said to stop and do one batch. Put every tweak on one batch branch, publish it once as one PR, and ask before opening any other PR |
| Stack | One large change that is too big to review whole | The Points audit: one 106-file branch split into 13 stacked PRs (#3 to #15, 2026-09-15), grouped into sections the operator had approved. Each PR's base is the PR below it |
A tweak a reviewer asks for on a PR that is already open is not a batch: it goes on that PR's branch as a small commit (`MOI-Website` PR #53 took 24 commits and merged as one squash).

## 2. The review batch
1. A branch off the PR base, named for what it is (`review-batch`). Each tweak is a commit, so the operator can see them one by one. The 2026-09-15 batch folded five tweaks as five commits, 27 files, with typecheck, lint, tests, the migration check and a build all passing before it was published.
2. Verify there. Nothing is pushed while the operator is still reading.
3. When the review is done: push once and open one PR (two gates, `templates/gate-asks.md`). The body lists each tweak. Close the earlier per-tweak PRs with a pointer to the batch, each with its own yes.
4. Tweaks after the batch PR is open go on the same branch.

## 3. The stack
1. Plan it as a table before cutting anything: PR number, branch, base, what it holds, and what breaks without the PR below. Show it to the operator; a stack is only worth it if each layer has a reason to exist. The audit stack needed a shared core layer because that layer changed signatures used by nearly every route, and a compile-driven planner confirmed no smaller split compiled.
2. Cut it from the original branch: for each layer, `git switch -c <layer> <layer below>` and `git checkout <original> -- <paths of this layer>`, then commit. Name the layers in order (`audit/01-...`, `audit/02-...`).
3. Check each layer on its own with the repo's local proof (`branch-and-commit.md`, section 6). A worktree per stack keeps a clean copy with its own dependencies: `git worktree add "<folder outside the repo>" <layer>`, remove it with `git worktree remove`. Every audit layer passed typecheck, lint and tests, and the full build passed on #5 and #15.
4. Prove the layers add up to the original: `[ "$(git rev-parse <top layer>^{tree})" = "$(git rev-parse <original>^{tree})" ] && echo equal`. Tested: three layers equal the original, and a split that left one file out printed no match and `git diff --name-status <top> <original>` named the missing file. The audit's top layer equalled `audit/fixes` the same way.
5. Open the PRs bottom first, each with `--base` set to the layer below (`gh pr create`, `pull-request.md` section 5). Pushing the layer branches and opening the PRs are gates: one yes that names every branch, PR, base and the order covers the sequence, as in section 4. A PR that cannot merge until the one below does can be a draft (`--draft`).
6. Every merge to a deploy branch deploys. A stack of thirteen is thirteen deploys, so decide with the operator whether to merge one at a time (section 5).

## 4. Updating many PRs: a staged push with a pause
The previous operator's instruction on 2026-10-01 for the six docs PRs: commit and push `moidocs` first, then every four minutes update the next one. The reason is not recorded; the notes say it may be to avoid a burst of notifications or builds (inferred). It does not change the method.
1. List the PRs in the order to push: the one other PRs depend on first. `moidocs` #124 goes before `MOI-Website` #57 because the site links to a file that #124 creates (as of 2026-10-01).
2. Ask once for the whole sequence, naming the PRs, the order and the pause (`templates/gate-asks.md`). One yes covers a short sequence the ask spelled out. It does not cover a PR added later.
3. For each PR: the proof of the change that is being pushed (`rebase-proof.sh` SAME or the rewrite proof), then the pinned push, then read back its head commit and its checks.
4. Wait the pause before the next. Four minutes is the recorded figure; use another if the operator says so. A plain timed wait, not a loop that polls GitHub.
5. Stop at the first failure: a red check, a rejected push, a surprise on the timeline. Report which PRs are done and which are not.
6. Keep a table for the hand-back: PR, pushed at (UTC), head commit (12 characters), checks.
Retries have their own pace: when Actions stopped on 2026-08-28 to 2026-08-30 the operator asked for a retry every four hours, not every ten minutes.

## 5. Merging a stack
1. One PR at a time, in order, each on a yes that names the number (or one yes that names every number, the order and the check after each, as in section 4). Explain each PR first in plain words: what it changes, why, what could break. On 2026-09-15 the previous operator had PRs explained and questioned ("is that standard practice") one by one, and #4 and #5 were each merged on a yes that named the number; #6 to #14 were then merged in order on one request that named the sequence and asked for a check after each.
2. Check the preconditions that PR has. On 2026-09-15 #3 added migrations and they were applied right after it merged and before #5. Do not copy that order for a Points migration today: at the `feature/ci-cd` tip a build that finds the schema behind refuses to start, so DevOps applies the migration before the merge (`moi-web-products-ops/references/points-settings-and-database.md`). Before #5 the migration count, the `BETTER_AUTH_URL` setting and the deploy of #4 were checked. A database write is its own gate.
3. After each merge: wait for the deploy, run the live check for that repo (`merge-and-deploy.md`), and only then ask about the next. On 2026-09-15 a local script, `merge_stack.py`, merged #6 to #14 in order, waited for each deploy and ran 64 live checks, all passing. It was on the previous operator's machine only and is not recorded elsewhere (the previous DevRel's notes). Done by hand it is the same steps.
4. After the PR below merges, the next PR's base must change to the deploy branch. If the merge was a squash, the PR above no longer has its parent on the base: rebase it with `--onto`.
```
git fetch origin                                      # a yes, once
OLDTIP=$(git rev-parse <the merged layer's branch>)   # before anything moves
git branch backup/<layer>-before-rebase-<date> <layer>
git rebase --onto origin/<base> $OLDTIP <layer>
bash "$SKILLS/moi-devrel/ship/scripts/rebase-proof.sh" backup/<layer>-before-rebase-<date> <layer> origin/<base>
```
Tested 2026-10-03: after a two-commit bottom branch was squash-merged, a plain `git rebase origin/<base>` stopped on an add/add conflict, and `--onto` replayed only the layer's own commit and `rebase-proof.sh` printed SAME. Then push (pinned lease, a gate) and change the PR's base: `gh pr edit <N> --repo <org>/<repo> --base <base>` (a gate).
5. A PR that stays a draft because its base is not ready (#15 on 2026-09-15; closed on 13 October 2026 and replaced by draft #24) is not merged with the others.

## Not yet known
- Whether the operator or the Voyage team merges `voyage-api` sync PRs. ASK: Rahul.
- Where `merge_stack.py` and its 64 live checks are kept: not recorded (the previous DevRel's notes); the by-hand steps above replace it.
- Whether any repo limits the size of a PR or the number of open PRs. None is recorded.
