# Rebase and keep a pull request current

Facts are as of 2026-10-03. The sequence below was run on a scratch repository with a local bare repository as its remote on 2026-10-03; the results are in `../evals/evals.md`. It is the practice the previous operator recorded, spelled out: a backup branch before any rebase, proof that only the base changed, and a push pinned to the remote commit last seen. The exact commands he used are not recorded. ASK: Adithya if you need them. Back to `../GUIDE.md`.

## 1. When to rebase, and when not
A rebase takes your branch's commits and replays them on top of the current tip of the base, so the branch looks as if you had started from it today. Every replayed commit gets a new id.
- Rebase when the base moved and the PR conflicts, when `ship-preflight.sh` says the branch is behind and the base changed files you touched, or before you push a branch that has sat for days. The previous operator rebased the docs PRs on 2026-09-30 and 2026-10-01 ("audit and check for rebase").
- Do not rebase merged history, and do not rebase a branch another person also pushes to. After a fetch, `git log <branch>..origin/<branch>` must be empty, or those commits are not yours: stop and read them.
- Tell the operator what a push will do before asking: it changes every commit id after the first rewritten one, reruns the PR's workflows, and everybody watching the PR sees it. `MOI-Website`'s preview workflow runs on every push to a PR, and `js-moi-sdk` runs its tests on one. Whether a push dismisses an approval depends on a repository setting nobody has recorded. ASK: Rahul.

## 2. The sequence
`<b>` is your branch, `<base>` the PR's base, for example `main` or `feature/ci-cd`.
| # | Do | Command |
|---|---|---|
| 0 | Right branch, clean tree | `git switch <b>`, then `git status --short` prints nothing. Commit or set aside first |
| 1 | Fetch and note what the remote has | `git fetch origin` (a yes, once). Then `LAST_SEEN=$(git rev-parse origin/<b>)`. If `git log <b>..origin/<b>` lists commits, someone else pushed: stop |
| 2 | Backup branch | `git branch backup/<b>-before-rebase-<YYYY-MM-DD> <b>`. Local only. The previous operator's were named `geo-fixes-before-rebase-oct1` and the like. Never push a backup |
| 3 | Rebase | `git rebase origin/<base>`. Not `git pull`: depending on configuration it makes a merge commit, and a merge commit in the range makes every later rewrite harder |
| 4 | Conflicts | Resolve file by file, `git add`, `git rebase --continue`. `git rebase --abort` returns to step 2's state. Read both sides: a conflict is exactly where an older copy of a page can win |
| 5 | Prove | `bash "$SKILLS/moi-devrel/ship/scripts/rebase-proof.sh" backup/<b>-before-rebase-<date> <b> origin/<base>` |
| 6 | Local proof again | The repo's checks (`branch-and-commit.md`, section 6) and `bash "$SKILLS/moi-devrel/ship/scripts/ship-preflight.sh" origin/<base>`. A new base can break a build the old one passed |
| 7 | Push (GATE) | `git push --force-with-lease=<b>:$LAST_SEEN origin <b>` after a yes (`templates/gate-asks.md`) |
| 8 | Read back | `git ls-remote origin refs/heads/<b>` equals `git rev-parse <b>`. The PR shows the new head, its checks and its preview ran again |
| 9 | Update the PR (GATE) | Add or edit the "Rebased" section of the body, and any fact that changed, on a yes (`templates/gate-asks.md`). A body goes stale: on 2026-10-02 three of five docs PR bodies were wrong |
| 10 | Clean up | After the PR merges, `git branch -D backup/<b>-before-rebase-<date>` (the previous operator left such backups until merge) |
A first push of a new branch needs no lease: `git push -u origin <b>`. Use the lease only to replace commits you already pushed.

## 3. Why the lease is pinned
`--force-with-lease` refuses to overwrite a remote branch that is not where git expects. A bare `--force-with-lease` expects the remote-tracking ref, and `git fetch` moves that ref. Tested 2026-10-03: a teammate's clone pushed a commit to the branch, the first clone then ran `git fetch`, and a bare lease push (checked with `--dry-run`) reported a forced update that would have wiped the teammate's commit. The pinned form `--force-with-lease=<b>:<commit>` was refused (stale info) in every case, with and without the fetch. A 12-character abbreviation of the commit works as the pin.
So: capture `LAST_SEEN` in step 1 from a ref you have looked at, and keep it until the push. If you fetch again and the remote moved, stop and integrate, do not re-pin to the new value without reading it.

## 4. Reading `rebase-proof.sh`
It replays the backup's changes onto the new base with a three-way merge and compares that tree with the rebased branch. Read-only; exit 0 SAME, 1 anything else, 2 bad input.
| Verdict | Meaning | Do |
|---|---|---|
| SAME (exit 0) | The rebase added nothing, dropped nothing, kept no stale copy | Go on to step 6 |
| DIFFERENT (1) | Listed files differ from what the backup's changes should give. `D` is a change missing from the rebased branch, `A` is extra, `M` is changed. Tested: a dropped file, a stale copy of a file the base had updated, and an extra file each gave DIFFERENT | Read each file against the base and the backup. The usual cause is a stale copy that won a conflict: commit 0899368 in `moidocs` fixed a rebase that kept an older `submit-ixn.md` and reverted a storage-deposit example from #120 |
| UNPROVEN (1) | Replaying conflicts, so a merge cannot check your hand resolution. The conflicted files are listed, and it says whether anything else differs | Read the listed files yourself: `git diff <backup> <b> -- <file>` |
| NOT ON THE NEW BASE (1) | The rebased branch does not contain the base | You rebased onto something else, or the base moved. Rebase again |
A DIFFERENT result is a prompt to look, not proof of a bad rebase: a rebase replays commit by commit and the proof replays the sum, and they can differ when a later commit undoes an earlier one. Bad input (a ref that does not resolve, no common history, git older than 2.38) exits 2 with the reason.
After a rebase, also diff the pages against the base: `git diff origin/<base> -- <path>` should show only your change.

## 5. A report on several branches (read-only)
For "check for rebasing now and then give me a report" (2026-09-30). It writes nothing to the repository, because the merge's objects go to a temporary folder. Tested in zsh and bash.
```
TMPO="$(mktemp -d)"
for b in <branch-one> <branch-two>; do
  set -- $(git rev-list --left-right --count "origin/<base>...$b")
  if GIT_OBJECT_DIRECTORY="$TMPO" GIT_ALTERNATE_OBJECT_DIRECTORIES="$(git rev-parse --absolute-git-dir)/objects" git merge-tree --write-tree "origin/<base>" "$b" >/dev/null 2>&1; then c=clean; else c=CONFLICT; fi
  echo "$b behind=$1 ahead=$2 merge=$c"
done
rm -rf "$TMPO"
```
`behind` is how far the base has moved, `merge=CONFLICT` means a rebase will stop. The counts are as of your last fetch. This is local and read-only, so it is allowed on an audit task as long as you do not fetch.

## 6. Many PRs
Updating several PRs is a staged push with a pause between them: `stacked-and-batched.md`, section 4.

## Not yet known
- The exact commands of the 2026-09-30 and 2026-10-01 rebases. ASK: Adithya.
- Whether a force-push dismisses approvals or re-runs required checks on any repo (branch protection is not recorded). ASK: Rahul.
- Why the previous operator updated one PR every four minutes: the notes say "possibly a notification or build burst" (inferred). ASK: Adithya.
