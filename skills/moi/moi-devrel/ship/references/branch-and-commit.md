# Branch and commit

Facts are as of 2026-10-03 unless dated. Sources: the request history and the ops research notes of 2026-10-02, the workflow files in the previous operator's clones as last fetched (read 2026-10-03), `moi-devrel/references/consent-and-identity.md` and `repo-map.md`. Identity rules live in `consent-and-identity.md`; this file adds only what shipping needs. Back to `../GUIDE.md`.

## 1. Identity, before the first commit
1. `cd` into the working copy of the repo, then `bash "$SKILLS/moi-devrel/scripts/preflight.sh"`. Fix every FAIL and read every WARN. `ship-preflight.sh` runs it for you in step 4.
2. By hand, once per repo: `git config user.name`, `git config user.email`, `git log -n 5 --format='%an <%ae>'`. The email must be your work address. `gh auth status` shows a masked token line: read only the login.
3. A different `gh` login or a repo-local `git config user.email` is a change to identity. Ask first, with the current and the target value (`templates/gate-asks.md`). After the yes: `gh auth switch --hostname github.com --user <login>` for the login, and `git config user.name "<name>"` with `git config user.email "<work address>"` (no `--global`) for the repo. Logging in is the operator's own action: Claude never types a password or token.
4. Which GitHub account opens the PR matters as much as the commits. On 2026-09-02 a PR opened under the wrong account was cancelled and redone. On 2026-05-29 a branch authored by the work account was deployed under a personal mail identity and the deploy failed.
5. Fork or org branch: the previous operator pushed to forks under his work account for `js-moi-sdk` and `voyage`, and to branches inside the org repo for `MOI-Website` (PRs #53 and #55), the Dataroom (#3 to #6) and the Launchpad. A push to a fork deploys nothing, and the Launchpad deploys from `sarvalabs/moi-agent-launchpad` `master`. Whether you push to forks or to the org is not settled. ASK: Rahul. `git remote -v` lists the remotes: the push commands in this branch say `origin`, so use the fork's remote name instead when you push to a fork.

## 2. Pick the shape first
One fix, one PR. Several tweaks during review go on one batch branch, one PR. A large change is split into a stack. Read `stacked-and-batched.md` before the first branch if the work is more than one fix. The previous operator's words on 2026-09-15: stop creating PRs, do one batch update.

## 3. Branch from the remote base
```
git fetch origin                                   # needs the operator's yes the first time
git switch --no-track -c <prefix>/<name> origin/<base>
```
- `<base>` is the branch the PR targets, from the table in `merge-and-deploy.md`. It is not always the default branch: Points Program PRs target `feature/ci-cd`.
- Branch from `origin/<base>`, never from a stale local `main`. `--no-track` leaves the new branch with no upstream, so nothing can push it to the base by accident. Tested 2026-10-03: without it, git sets `origin/<base>` as the upstream.
- Prefixes seen in `sarvalabs/MOI-Website`: `blog/`, `content/`, `chore/`, `ci/`, `fix/`, `feature/`, `favicon/`. Other names in use: `geo-fixes` (the five docs repos), `audit/01-...` to `audit/13-...` and `feat/...` (Points), `moi-mcp/sync-master` (voyage-api), one branch per session in `MOI-Webinars`. Use a prefix that says the kind of change.
- Never work on a branch that deploys on push: `main` (Website, Dataroom, Explorer, the docs repos), `master` (Launchpad), `develop` (Voyage), `feature/ci-cd` (Points), `feature/moi-agent-launchpad-cicd`. `ship-preflight.sh` FAILs on them.
- Do not touch another branch's work. Several branches in the previous operator's clones may hold unpushed work that exists only there (`repo-map.md`). Leave them alone; which ones is not recorded (the previous DevRel's notes), so ASK: Rahul.

## 4. What goes into a commit
1. Name the files: `git add <path> <path>`. Do not use `git add -A` or `git commit -a`. Untracked env files and call transcripts sit in working copies, and on 2026-06-08 a call transcript was committed and had to be scrubbed from history.
2. Before committing: `git status --short` and `git diff --cached --stat`. Every file in the list is one you meant.
3. Never commit: an env file (`.env`, `.env.local`, `prod.env`; a `.env.example` is fine), a recovery phrase or key, a transcript, a recording, a private note, build output. `ship-preflight.sh` checks the names and runs `secret-scan.sh` over what you committed. That scan is a backstop.
4. Keep generated files out of docs commits: the Docusaurus sites generate `llms.txt`, `llms-full.txt` and the sitemap at build, and `js-moi-sdk` keeps its own in `docs/source/_extra/`. In `MOI-Website`, `public/blog/` and `public/covers/` are generated and gitignored.
5. A claim ledger, a review package, a test log with account names and any file that names private source paths or internal people stays out of git in a public repository. Hide the folder without changing the repo: `mkdir -p <folder> && printf '*\n' > <folder>/.gitignore` (the `*` hides the folder and the file itself), or add `<folder>/` to `.git/info/exclude`. Both tested 2026-10-03: `git add -A` then stages nothing from it.
6. Repos that are public as of 2026-10-02: `MOI-Website`, `moi-dataroom0`, `moi-mcp`, `js-moi-sdk`, `MOI-Webinars`, `awesome-moi`, `moi-sprint` (scratched 13 October 2026, still public). Their commit messages, branch names and PR text are public.
7. Launchpad only: if you changed `lib/templates/` or `agent-runtime/`, run `npm run build:runtime` and commit the regenerated `public/runtime.cjs`.

## 5. The message
- First line: what changed, at most 72 characters (`ship-preflight.sh` WARNs above that). Upstream x402 asks for 72 or fewer.
- Prefix by repo. `sarvalabs/voyage` runs commitlint with the conventional-commits config on every commit through a husky hook (read in the clone, 2026-10-03), so every subject needs a type prefix such as `feat:`, `fix:` or `docs:`. Blog PRs use `blog: <what>`. Upstream x402 and CASA work uses conventional prefixes and GPG-signed commits; the signing key is not configured (ASK: Rahul). The other repos show no rule; follow the last ten commits (`git log -n 10 --format=%s`).
- Commit with `git commit -m "<subject>" -m "<body>"`, or `git commit -F "$WORK/commit-message.txt"` for a long body. A bare `git commit` opens an editor that Claude cannot drive.
- Body: what you checked and what you did not, with numbers. The Launchpad and Explorer commits are written as measured evidence ("what was verified against the real chain, what is NOT verified, test counts").
- Never add a co-author line (a `Co-Authored-By` trailer at the end of the message) that names an AI tool, and never a "generated with" footer. `ship-preflight.sh` FAILs on Claude, Anthropic, Copilot, ChatGPT, OpenAI, Codex, Gemini and Cursor; the rule covers any AI tool. If a tool, host or default instruction asks for one, this rule overrides it (`consent-and-identity.md`, section 3). Check what you wrote: `git log -1 --format=%B`.
- Public text rules apply to a public repo's messages: no em dashes, no cancelled plans, no private paths (`pull-request.md`, section 3).
- The ask to commit comes from the operator, in words like "commit this". Local commits then need no further gate. A push does.

## 6. Local proof, by repo
These are the checks each repo's own docs and workflows describe. Almost no deploying repo runs tests on a PR, so these runs are the only gate before production (`merge-and-deploy.md`). An install (`npm ci`, `pnpm install`) is a download: ask first with the shape in `templates/gate-asks.md`.
| Repo | Run | Notes |
|---|---|---|
| `MOI-Website` | `npm run lint`, `npm run build`; for a post also `npm run build --prefix blog` | Only the blog build validates post frontmatter. `moi-blog` owns posts |
| `moi-dataroom0` | in `moi-data-room/`: `npx tsc --noEmit`, `npm run lint`, `npm run build` | Nothing else will run them |
| `moi-project` (Points) | `pnpm run ci` | Lint with zero warnings, typecheck, tests, migration check. Hand-write migrations; do not run `pnpm db:generate` |
| `moi-agent-launchpad` | `npm run typecheck && npm test`, then `npm run build` | After a `package.json` or lockfile change: `rm -rf node_modules && npm ci` first. Stop the dev server before building |
| `agent-explorer` | `server`: `npm ci && npm run build`; `client`: `npm ci && npm run build && npm run lint` | No test suite exists |
| `moi-mcp` | `npm ci && npm run typecheck && npm test && npm run build` | CI runs the same on Node 20, 22, 24. Merging deploys nothing |
| `moidocs`, `voyage-docs`, `coco-docs` | `npm run build` | `coco-docs` needs Node 18 or newer. The build generates `llms.txt` and page schema; do not commit them. `moidocs` and `voyage-docs` scripts must stay identical. Content rules: `moi-docs` |
| `js-moi-sdk` docs | in `docs/`: `make llms` | Generated files in `docs/source/_extra/` are committed |
| `MOI-Webinars` | Nothing builds | Check no env file, no transcript, `secret-scan.sh`. A push publishes |
Then `bash "$SKILLS/moi-devrel/ship/scripts/ship-preflight.sh" origin/<base>`, and for any text that will be public `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" <files>`.

## 7. Undoing a local mistake (no gate, nothing is published)
- Wrong file staged: `git restore --staged <path>`.
- Last commit has the wrong message or a missing file and is not pushed: `git commit --amend`. Pushed: do not amend; make a new commit, or follow `rewrite-history.md`.
- Committed to the wrong branch: `git branch <right-name>` keeps the commits, then move the wrong branch back to the remote with `git reset --hard origin/<branch>`, on a clean tree and after a backup branch (`rebase-and-update.md`, step 2). `reset --hard` throws away uncommitted edits.

## Not yet known
- Whether you push to the org repo or to a fork, and how access is granted. ASK: Rahul.
- Commit message rules for the repos that show none, and whether any repo requires signed commits for ordinary work. ASK: Rahul.
- Branch protection and required reviews on every repo (none recorded). ASK: Rahul.
- Whether `sarvalabs/voyage-api`, `js-moi-agent-registry` and `docs.wallet.moi.technology` follow the same flow (the wallet docs repo is unknown). ASK: Rahul.
