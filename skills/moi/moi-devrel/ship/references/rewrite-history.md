# Rewriting pushed history

Facts are as of 2026-10-03. A rewrite changes commit ids that others may have fetched. It is rare, it is never a tidy-up, and it needs an explicit yes that names the branches. The sequences below were run on a scratch repository with a local bare repository as its remote on 2026-10-03 (git 2.50.1, record in `../evals/evals.md`). The previous operator's own commands for the 2026-10-01 cleanup are not recorded; these are tested ones that give the same result. Back to `../GUIDE.md`.

## 1. When a rewrite is justified
| Reason | Scope | Evidence |
|---|---|---|
| An AI co-author line or "generated with" footer on the commits of an open PR | The branch's own commits, open PRs only | 2026-10-01: removed from 130 commits on six open PRs (`moidocs`, `coco-docs`, `voyage-docs`, `MOI-Website`, `js-moi-sdk`, `voyage`), on request, backup branches left. Merged history was not rewritten |
| A personal address or handle on the commits of an open PR | The branch's own commits | 2026-06-08 the personal handle was scrubbed from history; 2026-08-10 all commits were relabelled; 2026-09-02 a PR opened under the wrong account was redone |
| A file that should never have been committed (a call transcript) | The branch's own commits | 2026-06-08: the transcript was committed and scrubbed from history. A secret in a file is different: rotate it first, because a rewrite does not un-expose it (`consent-and-identity.md`, section 4) |
Not justified: merged history, `main` or any deploy branch, tidying commit order, squashing a long branch (the merge squashes it: PR #53 had 24 commits and landed as one), a branch that others also push to, and a branch whose range holds merge commits. In those cases stop and ASK: Rahul.
The ask is one the operator makes. If the operator only notices the problem, name it, give the count (`ship-preflight.sh` prints it) and offer the rewrite; do not start. Never on an audit, inventory or handover task: those are local and read-only.

## 2. What a rewrite does
- The tree is unchanged and every commit from the first changed one on gets a new id. Author, committer and dates are kept (tested).
- It needs a force push. Everybody watching the PR sees one, the PR's workflows run again (`MOI-Website` previews rebuild, `js-moi-sdk` tests run), and review comments pinned to the old commits may show as outdated. Whether it dismisses approvals depends on a repository setting nobody has recorded. ASK: Rahul. Those last two are general GitHub behaviour that was not tested here: read the PR timeline after the push and tell the operator what you see.
- Treat everything already pushed as seen. Others may have fetched it, and old commits may stay reachable by their ids. A rewrite fixes the branch, not the exposure.
- It does not touch the PR body. A footer in the description is removed by editing the body (a gate). Open PRs #52 and #54 of `MOI-Website` still carried the footer in the body, and one trailer on their single commit each, when read on 2026-10-03. Neither was among the six cleaned on 2026-10-01. Their state may have changed since: check with `gh pr view` before relying on this.

## 3. Preconditions (stop if any fails)
1. The operator's yes names the branches and the change, and says "open PRs only" if that is the scope. Each PR is open (`gh pr view <N> --repo <org>/<repo> --json state`, read-only).
2. Clean tree: `git status --short` prints nothing. `filter-branch` refuses a dirty tree ("You have unstaged changes", tested).
3. You are the only pusher: `git fetch origin`, then `git log <branch>..origin/<branch>` prints nothing. Note `LAST_SEEN=$(git rev-parse origin/<branch>)`.
4. The range is linear: `BASE=$(git merge-base origin/<base> <branch>)` and `git rev-list --merges $BASE..<branch>` prints nothing. Rewriting the range of a branch with merge commits would rewrite commits that are not yours.
5. A backup branch exists: set `BR`, `BASEREF`, `BASE` and `B` as in the first line of section 4, then `git branch "$B" "$BR"`. Local only, never pushed. The previous operator's were `geo-fixes-before-attribution-rewrite` and the like.
`git filter-branch` is built in and prints a warning recommending `git filter-repo`. That tool is not installed by default (installing it is a download: a yes first) and rewrites a whole clone, so it is not used here. Set `FILTER_BRANCH_SQUELCH_WARNING=1` after you have read the warning.

## 4. Remove AI co-author lines (tested)
```
BR=<branch>; BASEREF=origin/<base>; BASE=$(git merge-base $BASEREF $BR); B=backup/$BR-before-rewrite-<YYYY-MM-DD>
export AWKFILE="$SKILLS/moi-devrel/ship/templates/strip-ai-lines.awk"
git log -1 --format=%B $BR | awk -f "$AWKFILE"        # try the filter on one message first
git switch $BR
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --msg-filter 'awk -f "$AWKFILE"' -- "$BASE"..HEAD
git update-ref -d refs/original/refs/heads/$BR         # filter-branch leaves its own backup ref here
```
The filter drops a co-author line that names Claude, Anthropic, Copilot, ChatGPT, OpenAI, Codex, Gemini or Cursor and a "generated with" or "generated by" line that names one of them, and the blank line each leaves behind. A co-author line for a person stays (tested: `Real Person` survived). A person whose name contains one of those words would lose their line too: the `range-diff` below shows every removed line, so read it.
Prove it, all four must hold:
```
[ "$(git rev-parse $B^{tree})" = "$(git rev-parse HEAD^{tree})" ] && echo "tree equal"
echo "$(git rev-list --count $BASE..$B) commits before, $(git rev-list --count $BASE..HEAD) after"
F='%an|%ae|%aI|%cn|%ce|%cI|%s'; [ "$(git log --format="$F" $BASE..$B)" = "$(git log --format="$F" $BASE..HEAD)" ] && echo "authors, dates, subjects equal"
git log --format=%B $BASE..HEAD | grep -ciE 'co-authored-by:.*(claude|anthropic|copilot|chatgpt|openai|codex|gemini|cursor)|generated (with|by).*(claude|anthropic|copilot|chatgpt|openai|codex|gemini|cursor)'   # slop-lint:ignore  (prints 0)
```
Then `bash "$SKILLS/moi-devrel/ship/scripts/rebase-proof.sh" $B $BR $BASEREF` must print SAME, and `git range-diff $BASE..$B $BASE..HEAD` shows a `!` for each commit that lost a line, with only the message lines removed, and `=` for a commit that had none (tested). Run `bash "$SKILLS/moi-devrel/ship/scripts/ship-preflight.sh" $BASEREF`: the AI line check now passes.

## 5. Relabel commits made under the wrong address (tested)
`ship-preflight.sh` FAILs on a personal-provider author or committer address. Set `BR`, `BASEREF`, `BASE` and `B` as in section 4 first: an empty `BASE` turns the range below into nothing. Put the old address and your work identity in variables (never in a file), and rewrite only the commits that carry the old address, so dates and other people's commits stay.
```
export OLD_EMAIL="<the old address>" NEW_NAME="$(git config user.name)" NEW_EMAIL="$(git config user.email)"
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --env-filter '
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]; then export GIT_AUTHOR_NAME="$NEW_NAME"; export GIT_AUTHOR_EMAIL="$NEW_EMAIL"; fi
if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]; then export GIT_COMMITTER_NAME="$NEW_NAME"; export GIT_COMMITTER_EMAIL="$NEW_EMAIL"; fi
' -- "$BASE"..HEAD
```
Prove it with the tree check of section 4, with the dates and subjects alone (`F='%aI|%cI|%s'`, then the same `[ "$(git log --format="$F" $BASE..$B)" = "$(git log --format="$F" $BASE..HEAD)" ]` test, because names and addresses are meant to differ), and that `git log --format='%ae%n%ce' $BASE..HEAD` no longer holds the old address.

## 6. Drop a file from the branch's commits (tested)
Set the variables of section 4 first.
```
export DROP_PATH="<path in the repo>"
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --index-filter 'git rm --cached --ignore-unmatch -q -- "$DROP_PATH"' --prune-empty -- "$BASE"..HEAD
```
`git log --format=%H $BASE..HEAD -- "$DROP_PATH"` must print nothing, and `git diff --name-status $B HEAD` must list only that file. A commit that held only the file disappears. If the file held a secret or private text, tell the operator it is exposed (`consent-and-identity.md`, section 4); the file stays visible to anyone who already fetched it.

## 7. Push it (GATE), then finish
1. Ask with the backup name, the proof lines and the pin (`templates/gate-asks.md`). Then: `git push --force-with-lease=$BR:$LAST_SEEN origin $BR`. The lease is pinned to the commit you last saw, so a teammate's push in the meantime is refused (`rebase-and-update.md`, section 3).
2. Read back: `git ls-remote origin refs/heads/$BR` equals `git rev-parse HEAD`, and the PR shows the new head.
3. Edit the PR body if it carries a footer (a gate), and say what the timeline shows.
4. Keep the backup until the PR merges, then delete it locally.
To undo before the push: `git reset --hard $B`. After the push, undoing it is another force push of the backup, with its own yes.

## Not yet known
- The previous operator's exact commands and whether he rewrote bodies with `gh`: not recorded (the previous DevRel's notes). The tested sequences above replace them.
- Whether any repo dismisses approvals on a push. ASK: Rahul.
- How to meet an upstream AI-disclosure rule once the footer is banned. ASK: Rahul.
