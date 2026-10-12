# The ask for each gate

Use one of these shapes, with every blank filled from what is on screen, and then do exactly that and nothing more. A yes names one action, or one short sequence that the ask spelled out. It never carries over to the next action (`moi-devrel/references/consent-and-identity.md`, section 1). After a no, do not offer the same thing again.

Each ask ends with what you will read back afterwards. Say it, so the operator knows how the action is checked.

| Gate | Ask | Read back afterwards |
|---|---|---|
| Fetch, branch and commit (step 2 and 3) | "Ready to fetch `origin` in `<repo>`, branch `<name>` from `origin/<base>`, and commit `<file list>` as `<git email>`. Yes?" | `git status --short`, `git show --stat`, `git log -1 --format=%B` has no AI line |
| Download for the local proof | "Ready to run `npm ci` in `<repo>`. It downloads the packages in `package-lock.json` from the npm registry. Yes?" | The command's exit code |
| Push, first time (step 6) | "Ready to push branch `<name>` (`<N>` commits, files: `<list>`) to `origin` (`<org>/<repo>`) as `<login>`. Yes?" | `git ls-remote origin refs/heads/<name>` equals `git rev-parse HEAD` |
| Open the pull request (step 7) | "Ready to open a PR in `<org>/<repo>`: base `<base>`, head `<name>`, title `<title>`, body from `<path>`, as `<login>`. Yes?" | The PR page: base, head, title, files changed, the preview comment |
| Reply on a review (step 8) | "Ready to post this reply on PR `<N>` as `<login>`: `<text>`. Yes?" | The thread on the PR page |
| Ask for a review | "Ready to request review on PR `<N>` from `<reviewer>` (they get a notification). Yes?" | The reviewers list on the PR page |
| Push a rebase or a rewrite | "Ready to force-push branch `<name>` to `origin` with the lease pinned to `<12 characters>`, the remote commit I last saw. Backup branch: `<backup>`. Proof: `<SAME or the output>`. Yes?" | `git ls-remote` equals local `HEAD`, the PR shows the new head |
| Update the PR body | "Ready to replace the body of PR `<N>` with `<path>`. Changes: `<list>`. Yes?" | `gh pr view <N> --json body` or the PR page |
| Retarget a PR | "Ready to change the base of PR `<N>` from `<old>` to `<new>`. Yes?" | The base on the PR page |
| Push a staged sequence | "Ready to push these in order with a pause of `<minutes>` between and a check of each PR before the next: `<list>`. Yes?" | After each push, that PR's checks and head commit |
| Merge (step 10) | "Ready to merge PR `<N>` (`<title>`) into `<base>` of `<org>/<repo>` by `<squash or merge commit>`. That starts `<workflow or nothing>` and goes live on `<URL>`. Yes?" | The PR state, the workflow run, the live URL (step 11) |
| Run a workflow by hand | "Ready to run workflow `<name>` on branch `<branch>` in `<org>/<repo>` with inputs `<list>`. It changes `<what>`. Yes?" | The run's result and the live check |
| Database change | "Ready to run `<migration file>` on `<product>`'s production database through `<tool>` before merging PR `<N>`. Yes?" | The verification query from the product's runbook |
| Switch the `gh` account | "Ready to switch `gh` from `<current login>` to `<target login>`. Yes?" | `gh auth status`, login name only |
| Delete a remote branch | "Ready to delete branch `<name>` on `origin`. PR `<N>` is `<merged or closed>`. Yes?" | `git ls-remote origin refs/heads/<name>` is empty |
| Remove AI lines from a PR's commits | "PR `<N>` is open and has `<K>` commits with an AI co-author line. Ready to rewrite them, keeping the backup `<backup>`, and force-push as above. Merged history stays as it is. Yes?" | The proof lines of `references/rewrite-history.md` |
