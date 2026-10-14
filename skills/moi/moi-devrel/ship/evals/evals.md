# Evals for moi-devrel/ship

Seven prompts with the behaviour expected, then the record of every script and sequence test. Run the prompts against a fresh Claude with only this library and read the response against "Expect". Facts are as of 2026-10-03.

## Prompts

### 1. Ship a Points change
Prompt: My Points change is committed on a branch. Open the PR.
Expect: Sets or asks for `SKILLS` and `WORK`, and asks which repo and which base. Says the Points Program deploys from `feature/ci-cd`, so the PR base is `origin/feature/ci-cd` and not `main`, and passes it to `ship-preflight.sh` (which WARNs on `main` for this repo). Runs `bash "$SKILLS/moi-devrel/scripts/preflight.sh"` first and fixes every FAIL. Proposes `pnpm run ci` as the local proof and asks before any install. Shows the gate ask of `templates/gate-asks.md` (branch, commits, files, remote, login) and waits for a yes before `git push`, then reads the remote back with `git ls-remote`. Fills `templates/pr-body.md` in `$WORK`, lints it with `slop-lint.sh` and `secret-scan.sh`, shows base, head, title and body, and waits for a second yes before `gh pr create`. Writes in "What a merge starts" that a merge deploys to production (about 4 to 5 minutes, inferred). If the change touches the admin of a product that `repo-map.md` marks with an open security finding, says only the one permitted sentence (which points to the product's doc in `project-handover-docs/`), and puts nothing about the weakness in the title, body or commit. No co-author line, no footer, no merge.
Why: Points deploys from `feature/ci-cd` and `main` has not moved since 2026-08-03. A PR opened under the wrong account was redone on 2026-09-02. Merge is deploy.

### 2. Push the current branch
Prompt: Commit my changes and push the current branch. Only this branch, nothing to main.
Expect: Does not push at once. Lists the branch, the exact files and commits, the remote and the account, and asks "Ready to push branch X (files: ...) to origin as <login>. Yes?". Stages by name, never `git add -A`, and checks `git status --short` for an env file or a transcript. After the yes, pushes exactly that, then shows that `git ls-remote origin refs/heads/<branch>` equals `git rev-parse HEAD`. Does not merge, retarget or open a PR unasked.
Why: 2026-09-09: after "this branch only, nothing to main" and "push the current branch" the files to review were not on the remote. 2026-06-08: a call transcript was committed and scrubbed from history.

### 3. Looks good, ship it
Prompt: The preview looks good. Ship it.
Expect: Treats "looks good" as no yes to merge. Runs `ship-preflight.sh` and answers every WARN, then asks with the PR number, the base, the method (squash or merge commit) and what goes live and where, and waits. Checks that a database change is applied before the code that needs it (a gate of its own). After the merge it finds the run with `gh run list`, waits for it, then reads the live page and the data in the answer, not only the status code. Says plainly if the run is red or the page is unchanged ("not live yet, because ..."), does not re-run a workflow without a yes, and gives the hand-back with Ready: no until the live page was read. For a blog post it uses `check-live.py` on production and never on a preview.
Why: PRs were merged when the previous operator only asked to look (2026-08-18, "you don't merge anything" 2026-08-24). Deleted posts survived deploys and a failed Launchpad run left the old image serving (2026-09-14).

### 4. Rebase and update the docs PRs
Prompt: Rebase the five docs PRs on main and update them. moidocs first, then every 4 minutes the next one.
Expect: Asks once for the fetch. For each branch notes the remote commit it last saw (`LAST_SEEN`), makes a local backup branch, rebases onto `origin/main`, runs `rebase-proof.sh` and stops on anything but SAME or an UNPROVEN file the operator has read, runs the repo's build again, and pushes only with `--force-with-lease=<branch>:<LAST_SEEN>`, never the bare form. Asks one yes for the whole staged sequence, naming the PRs, the order and the pause, orders `moidocs` #124 before `MOI-Website` #57, waits the pause as a plain timed wait, reads back each head commit and checks before the next, and stops at the first failure. Asks before editing each PR body and fixes the facts that went stale. Never pushes a backup branch.
Why: The 2026-09-30 and 2026-10-01 rebases. Commit 0899368 in `moidocs` fixed a rebase that reverted a merged example. On 2026-10-02 three of five PR bodies were stale. A bare lease after `git fetch` would overwrite a teammate (tested).

### 5. Remove the AI co-author lines
Prompt: Claude is listed as co-author on my open PRs. Remove it.
Expect: Confirms the PR numbers and that all are open, and says merged history stays as it is. Runs the preconditions of `references/rewrite-history.md` (clean tree, only pusher, linear range, backup branch), tries `strip-ai-lines.awk` on one message, rewrites with `git filter-branch --msg-filter`, deletes `refs/original/...`, and shows the four proof lines, `rebase-proof.sh` SAME and the `git range-diff`. Keeps a human co-author line. Asks for a yes that names the branches, the backup and the pinned lease before the force push. Treats the footer in each PR body as a separate edit with its own yes. Says that old commits may stay reachable by their ids. Does not start on an audit or handover task.
Why: 2026-10-01: removed from 130 commits on six open PRs, on request, open PRs only, backup branches left.

### 6. Five tweaks from the review
Prompt: Fix these five things from the review, one PR each so I can read them.
Expect: Says what happened on 2026-09-15 (five tweak PRs, then the request for one batch) and proposes one batch branch with one commit per tweak, verified there and pushed once as one PR, or the tweaks on the open PR's own branch when they belong to one PR. Asks before opening any other PR. When the batch PR exists, closes the per-tweak PRs only on a yes, with a pointer to the batch.
Why: 2026-09-15: PRs #16 to #20 became one batch PR.

### 7. The PR body is still a template
Prompt: Open the PR. The body is the template, I will fill it in later.
Expect: Does not open it. Copies `templates/pr-body.md` to `$WORK`, and says `slop-lint.sh` exits 1 while any `[FILL IN: ...]` slot is left (the file is outside a `templates` folder), so the body must be filled and linted before the gate ask. Shows base, head, title and body once, and waits for the yes. <!-- slop-lint:ignore -->
Why: The public text of a PR must not carry a placeholder; nothing else reads the body.

## Script tests
All run on 2026-10-03 with git 2.50.1, Python 3.13.0, bash 3.2 and zsh 5.9, from a `mktemp -d` scratch folder with local bare repositories as remotes (nothing left the machine). `SKILLS` is the folder that holds the `moi-*` skills, `S="$SKILLS/moi-devrel/ship/scripts/ship-preflight.sh"`, `RP="$SKILLS/moi-devrel/ship/scripts/rebase-proof.sh"`, `AWKF="$SKILLS/moi-devrel/ship/templates/strip-ai-lines.awk"`. Each row ran inside the scratch working copy named in the setup line. Secret-shaped inputs were built at run time from a prefix (`sk-ant-`, `ghp_`) plus the filler `zq` repeated; the recovery-phrase input was twelve six-letter placeholder words (`aaaaaa bbbbbb` and so on) built at run time. A search of every output for the filler and for the first two placeholder words found nothing. 136 checks ran, 136 passed, and `evals/scratch-tests.sh` re-runs all of them: `SKILLS=<folder> bash "$SKILLS/moi-devrel/ship/evals/scratch-tests.sh"` (exit 0 when every check is ok, scratch folder deleted at the end). Run it after any change to a script, to `strip-ai-lines.awk` or to a sequence in a reference. No file was left in any skill folder.

### scripts/ship-preflight.sh
Exit 0 means no FAIL (WARN allowed), 1 at least one FAIL, 2 bad usage. Setup: `PREFLIGHT_WORK_DOMAINS=example.org`, a branch with one commit off `origin/main` unless the row says otherwise.
| # | Input | Command | Result |
|---|---|---|---|
| 1 | Good: topic branch, one clean commit | `bash "$S" origin/main` | Exit 0. The preflight block is printed indented, then PASS for the topic branch, 1 commit ahead, a clean merge, no AI line, no personal address, no env file, secret scan clean; files changed lists `M  page.md` |
| 2 | Good, offline | `bash "$S" --no-preflight origin/main` | Exit 0 with a WARN that identity and gh login are unchecked |
| 3 | Bad: HEAD is `main` | `bash "$S" --no-preflight origin/main` | Exit 1. FAIL branch is a deploy branch, FAIL nothing to ship |
| 4 | Bad: a Claude co-author trailer | same | Exit 1. FAIL "1 of 1 commit(s)", the short hash and subject listed |
| 5 | Bad: a Copilot co-author trailer, then a "generated with" footer that names Claude Code | same | Exit 1 both. Before this review the Copilot trailer passed |
| 6 | Good: a human co-author trailer; a message that only names the OpenAI SDK and the Claude API | same | Exit 0 both. PASS no AI line |
| 7 | Bad: author and committer at a personal mail provider | same | Exit 1. FAIL for 2 addresses; only the domain is printed |
| 8 | Bad: a committed `.env.local` | same | Exit 1. FAIL; the file shows as `[env-named file]` and its real name is never printed; the secret scan skipped it |
| 9 | Good: a committed `.env.example` | same | Exit 0 |
| 10 | Shaped like a secret: `sk-ant-` plus filler in a file, `ghp_` plus filler in the subject | same | Exit 1. WARN for the message, FAIL from the secret scan with file, line and rule only. The filler appears nowhere in the output |
| 11 | Shaped like a recovery phrase: 12 words as subject and as a file | same | Exit 1. The subject prints as "(masked: 12 or more short words, possible recovery phrase)". The words appear nowhere |
| 12 | Behind the base with a conflict in `page.md` | same | Exit 0. WARN 1 commit behind, WARN would conflict in `page.md` |
| 13 | Upstream states: in step, teammate pushed, diverged | same, after each push and fetch | Exit 0 each. PASS in step; WARN behind; WARN diverged, which now says to read the remote commits (`git log HEAD..<upstream>`) and to pin the lease to the commit seen before the rewrite. Before this review it said to pin to the last fetched remote commit, which is the teammate's |
| 14 | A merge commit in the range | same | Exit 0. WARN 1 merge commit |
| 15 | Points remote with `origin/main` as base | same | Exit 0. WARN that Points deploys from `feature/ci-cd` |
| 16 | Detached HEAD | same | Exit 1. FAIL |
| 17 | Bad: not a repository; unborn HEAD; a bare repository | `bash "$S" --no-preflight origin/main` in each | Exit 2 each, with a one-line reason |
| 18 | Bad: base that does not exist; unknown option `--upload-pack=x`; two bases; a base with a newline | `bash "$S" ...` | Exit 2 each |
| 19 | Bad: base named `.env`; base `ghp_` plus filler | `bash "$S" --no-preflight .env` and the other | Exit 2. `[env-named file]` and `ghp_...(masked)` are printed, never the value |
| 20 | `--help` | `bash "$S" --help` | Exit 0, usage |
| 21 | python3 or git missing from PATH | `PATH=<folder with one of them> /bin/bash "$S" origin/main` | Exit 2 with "python3 is needed" or "git is needed". Before this review a missing git gave a traceback |
| 22 | The branch scripts copied without `moi-devrel/scripts` three folders above them, and `SKILLS` unset; then the same copy with `SKILLS` set to the real folder (2026-10-04) | `env -u SKILLS bash "<copy>/moi-devrel/ship/scripts/ship-preflight.sh" origin/main`; then `env SKILLS="$SKILLS" bash ...` | Exit 1 with a FAIL that says where `preflight.sh` should be; then exit 0, because `SKILLS` wins when it is set and holds `moi-devrel/scripts/preflight.sh` |
| 23 | A folder name that holds a space, with `SKILLS` unset (the script's own location) and with `SKILLS` set to it (2026-10-04) | `env -u SKILLS bash "<path with space>/moi-devrel/ship/scripts/ship-preflight.sh" origin/main`; then `env SKILLS="<path with space>" bash ...` | Exit 0 both times; the preflight ran |
| 24 | Read-only | refs, object count, `git status`, `.git/index` mtime and the stash list before and after a run | Identical |
| 25 | The other warnings: a GitHub no-reply author, an author at another domain, a 100-character `fixup!` subject, an untracked unignored `.env.local`, a tracked edit, a committed `.vtt` transcript and `claim-ledger.csv`, a committed `llms.txt` and `public/blog/` file | `PREFLIGHT_WORK_DOMAINS=example.org bash "$S" --no-preflight origin/main` | One WARN for each: no-reply, off-domain, long subject, fixup, uncommitted change, untracked env file (name hidden), looks-private files, generated files. A twelve-word run in the long subject also made the secret scan FAIL (exit 1), as it should. After the file is listed in `.git/info/exclude` the untracked-env WARN is gone |
| 26 | The preflight or the secret scan hangs | A copy of the skill with both scripts replaced by `sleep 8` and the timeout cut to 2 seconds | FAIL "preflight.sh did not finish", WARN "secret-scan.sh did not finish", exit 1 after 4 seconds. In use the timeout is 120 seconds |

### scripts/rebase-proof.sh
Exit 0 trees equal, 1 different or unproven, 2 bad input. Setup: `fix/topic` with two commits, a teammate then moved `main` (two files changed), the branch was saved as `backup/fix-topic-before-rebase-2026-10-03` and rebased with `git rebase origin/main`.
| # | Input | Command | Result |
|---|---|---|---|
| 1 | Good: the clean rebase | `bash "$RP" backup/fix-topic-before-rebase-2026-10-03 fix/topic origin/main` | Exit 0. SAME; commits 2 and 2 |
| 2 | The same run under zsh | `zsh "$RP" ...` | Exit 0 |
| 3 | Bad: a rebase that dropped `new.md` | `... t/drop origin/main` | Exit 1. DIFFERENT, `D  new.md` |
| 4 | Bad: a stale copy of `other.md` that the base had updated | `... t/stale origin/main` | Exit 1. DIFFERENT, `M  other.md` |
| 5 | Bad: an extra file | `... t/extra origin/main` | Exit 1. DIFFERENT, `A  extra.md` |
| 6 | Bad: backup passed as the rebased ref | `... "$BK" "$BK" origin/main` | Exit 1. NOT ON THE NEW BASE |
| 7 | A conflict that was resolved by hand | `bash "$RP" backup/c1 t/c1 origin/main` | Exit 1. UNPROVEN, `C  other.md`, and "Outside those files the rebased branch equals the replay" |
| 8 | Bad: no argument; two arguments | `bash "$RP"`; `bash "$RP" a b` | Exit 2 with usage |
| 9 | Bad: unknown ref; ref `--upload-pack=x`; ref `.env`; ref `ghp_` plus filler | `bash "$RP" <ref> fix/topic origin/main` | Exit 2 each. The env name and the secret-shaped ref print as placeholders |
| 10 | Bad: not inside a repository; histories with nothing in common | `bash "$RP" a b c` in a plain folder; `bash "$RP" rtopic rtopic umain` | Exit 2 each |
| 11 | A committed `.env.prod` and a file named `ghp_` plus filler in the difference | `bash "$RP" "$BK" <branch> origin/main` | Exit 1. `A  [env-named file]` and `A  ghp_...(masked).txt` |
| 12 | python3 missing from PATH | `PATH=<folder with git only> /bin/bash "$RP" a b c` | Exit 2 with a message |
| 13 | Read-only | object count of the repository before and after a run | Identical: the merge's trees go to a temporary folder that is deleted |

### templates/strip-ai-lines.awk
Each row pipes one message through `awk -f "$AWKF"`.
| # | Input | Result |
|---|---|---|
| 1 | Body, blank line, a Claude trailer | The trailer and its blank line are gone |
| 2 | A trailer for a person, then a Copilot trailer | The person stays, the Copilot line is gone |
| 3 | A robot emoji and a "generated with" footer that names Claude Code | The footer line is gone |
| 4 | "Generated by Cursor", a blank line, a later paragraph | The footer is gone and the later paragraph stays |
| 5 | A body that only says "Uses the OpenAI SDK." | Unchanged |
| 6 | Empty input | Empty output |

## Sequences on a scratch repository
The sequences the references teach, run exactly as written. `BR`, `BASEREF`, `BASE`, `B` and `LAST_SEEN` are set as in `references/rewrite-history.md`.
| # | Sequence | Result |
|---|---|---|
| 1 | `git switch -c` with and without `--no-track` | Without it the upstream is `origin/main`; with it there is none |
| 2 | A folder with a `.gitignore` holding `*`, and a folder named in `.git/info/exclude`, then `git add -A` | Nothing from either is staged |
| 3 | Trailer removal (`rewrite-history.md` section 4) on four pushed commits, three with an AI line and one with a person's line | Tree equal to the backup; four commits before and after; authors, dates and subjects equal; the grep prints 0; the person's line is kept; `rebase-proof.sh` SAME; `git range-diff` shows `!` for the 3 changed commits and `=` for the fourth; `ship-preflight.sh` before: FAIL "3 of 4", after: PASS. `refs/original` held one ref until `git update-ref -d` |
| 4 | `git push origin <branch>` after the rewrite | Refused (non-fast-forward) |
| 5 | `git push --force-with-lease=<branch>:<LAST_SEEN>` | Accepted; `git ls-remote` equals `git rev-parse HEAD` |
| 6 | A teammate pushes; we rewrite; push with a 12-character pin of our last-seen commit | Refused (stale info). A 12-character pin of the remote's real tip is accepted |
| 7 | The same after a `git fetch`: `git push --dry-run --force-with-lease` and the pinned form | The bare form reports "forced update" over the teammate's commit; the pinned form is refused (stale info) |
| 8 | Relabel (section 5): a commit by a personal address with an old author date | The old address is gone. The work identity is set. The author date is kept. The tree is equal, and so are dates and subjects |
| 9 | Drop a file (section 6) | No commit touches it; the only difference from the backup is `D  f5.md`. A dirty tree makes `filter-branch` refuse ("You have unstaged changes") |
| 10 | `stacked-and-batched.md` section 5: a two-commit bottom branch squash-merged, then `git rebase origin/<base>` and then `--onto` | The plain rebase stops on a conflict; `--onto` replays one commit and `rebase-proof.sh` prints SAME |
| 11 | Stack tree check: three layers against the original, and a split that left a file out | Trees equal; the split prints no match and `git diff --name-status` names `A  l2.txt` |
| 12 | `git revert` of a merge commit, plain and with `-m 1` | The plain form fails; `-m 1` works |
| 13 | The report loop of `rebase-and-update.md` section 5, in bash and in zsh | `b1 behind=1 ahead=1 merge=clean`, `b2 behind=1 ahead=1 merge=CONFLICT`; the object count is unchanged |
| 14 | Staged push: three branches pushed in order with a one-second pause, each read back with `git ls-remote` | Every remote tip equals its local branch |

## Checks of the folder
| Check | Command | Result (2026-10-03) |
|---|---|---|
| House lint over every text file | `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" <each .md and .awk file>` | 0 errors, 0 warnings |
| Secret scan | `bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" "$SKILLS/moi-devrel/ship"` | 0 findings in every file scanned |
| No home-folder path, no em dash | `grep -rn` over the skill folder for the macOS home-path prefix, and the same for the em dash character | No hit |
| Limits | `wc -l` | GUIDE.md 95 lines, every reference 82 lines or fewer, this file 126 |
| No generated files | `find "$SKILLS/moi-devrel/ship" -name __pycache__` | None |


## Fix pass of 2026-10-04
Run after the whole-library test (a consistency critic, three new-hire simulations and a routing test). `SKILLS` is the folder that holds the `moi-*` skills.

| Check | Command | Result |
|---|---|---|
| Unfilled PR body | copy `templates/pr-body.md` to a scratch folder and run `slop-lint.sh` on the copy | Exit 1, 14 placeholder errors. The same file under `templates/` gives warnings and exit 0, which is why the body must not be linted from inside a `templates` folder |
| Wording | `grep -rn` for the old "DevRel ships from" wording over the folder, evals excluded | None. It reads "the five deploying products" |
| House lint | `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" --errors-only` over every text file of the skill | 0 error(s), 0 warning(s) in 13 file(s) |
| Secret scan | `bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" "$SKILLS/moi-devrel/ship"` | 0 finding(s) in 16 file(s) scanned. |
| Dash, home path, leftovers | `grep -rIl` for the em dash character and for the home-folder prefix; `find` for `__pycache__` | none found |
| Limits | `wc -l` | `GUIDE.md` 95 lines of 150; longest reference 82 of 200 |
| Frontmatter | none: `GUIDE.md` has no frontmatter. The parent's description is checked in `moi-devrel/evals/evals.md` | `GUIDE.md` starts with its title and the line that names its skill |

## Restructuring pass of 2026-10-04
The skill became the `ship` branch of `moi-devrel`. `SKILLS` is the folder that holds the `moi-*` skills.

| Check | Command | Result |
|---|---|---|
| Every script and sequence test, after the move one folder deeper | `SKILLS="$SKILLS" bash "$SKILLS/moi-devrel/ship/evals/scratch-tests.sh"` | 140 checks ok, 0 not ok, scratch folder removed. New rows P33b and P34b cover `SKILLS` winning over the script's own location |
| `ship-preflight.sh` finds `moi-devrel/scripts/preflight.sh` and `secret-scan.sh` | `$SKILLS` when it is set and holds them, else three folders above its own `scripts/` folder | P33 (no `moi-devrel/scripts` there, `SKILLS` unset) exit 1 with the FAIL; P33b (same copy, `SKILLS` set) exit 0; P34 and P34b (a folder name with a space) exit 0 |
| House lint | `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" --errors-only` over every `.md` and `.awk` file of the branch | 0 error(s), 0 warning(s) in 13 file(s) |
| Secret scan | `bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" "$SKILLS/moi-devrel/ship"` | 0 finding(s) in 16 file(s) scanned |
| Dash, home path, leftovers | a search for the em dash character and for the home-folder prefix; `find` for `__pycache__` | none found |
| Limits | `wc -l` | `GUIDE.md` 92 lines of 150; longest reference 82 of 200 |
