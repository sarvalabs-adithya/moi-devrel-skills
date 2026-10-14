# Points Program: ship a change

Updated 13 October 2026 for the pull request states (table below). Other facts are as of 2026-10-02 for the repo and 2026-10-03 for the live reads. The files were read from `sarvalabs/moi-project` as of the deploy branch `feature/ci-cd` at `92f9c48` (2026-09-16) and `main` at `d7e2955` (2026-08-03); since then PR #22 and #23 have been merged into `feature/ci-cd`, so re-read the tip before relying on a line. Back to `../SKILL.md`. Commits, pull requests and merges are `moi-devrel/ship`.

Points: A security finding is open on this product as of 2026-10-02. The handover note is the Open items of `project-handover-docs/POINTS-PROGRAM.md`; read it before touching its admin.

## The path from a change to the live site
- The repo `sarvalabs/moi-project` is private. Access comes from an org admin (it returned 404 until 2026-09-15). ASK: Rahul.
- The branch that deploys is `feature/ci-cd`, not `main`. `main` has not moved since 2026-08-03 and holds no workflow file. A pull request that targets `main` deploys nothing. Draft pull request #24 would move the trigger to `main`; it needs DevOps setup first (`points-health.md`).
- "MOI Project CI/CD" (`ci-cd.yml`) runs on a push to `feature/ci-cd` and on a manual run. `docker-build.yml` builds the image with BuildKit secrets and pushes `ghcr.io/sarvalabs/moi-project:latest`. `deploy.yml` logs in through Teleport, writes the non-secret variables into the box's `.env` (rewritten from scratch each deploy, so hand edits are lost), pulls the image, stops and removes the old container, then starts the new one with the secrets passed as environment. nginx on the box serves https. A run takes about 4 to 5 minutes (inferred from run timestamps on 2026-09-15).
- The old container is removed before the new one starts, so a bad image means downtime. There is no rollback input at the tip: only `latest` is pushed. Draft pull request #24 adds an `image_tag` input. Whether older images exist is unknown. ASK: Upendhar.
- No pull request runs any check (the workflows are `workflow_call` plus a push trigger). Nothing enforces `pnpm run ci`.
- On start the app refuses to boot in production if the database has fewer migrations than the build, or if an enabled task is missing an environment value (`lib/startup.ts`). A merge that adds a migration or enables a task without its environment takes the site down until it is fixed.
- The health route reports `sha: null`, so you cannot tell from the JSON which build is running (P-K1).

## Run: change code

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Baseline | `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" points`. `gh run list -R sarvalabs/moi-project --workflow "MOI Project CI/CD" --limit 5` (read-only) | Output saved, last run known |
| 2 | GATE | Get the code (a download) | In a folder the operator chooses: `git clone https://github.com/sarvalabs/moi-project.git`, `cd moi-project` (every command below runs from this clone root), `pnpm install`. `package.json` pins pnpm 10.34.5 and the `Dockerfile` uses 11.11.0; which one the image really uses is unknown (ASK: Upendhar). Say source and size first | Yes given |
| 3 | LOCAL | Branch from the deploy branch | In the clone: `bash "$SKILLS/moi-devrel/scripts/preflight.sh"`, then `git switch --no-track -c <name> origin/feature/ci-cd` | No preflight FAIL |
| 4 | LOCAL | The environment | `cp .env.example .env.local`; the operator fills it with local and test values. Claude never opens it. Never put the production `DATABASE_URL` in it: the next two commands would run against production. A local Postgres: `createdb moi_db`, then `pnpm db:migrate`, then `pnpm dev` (localhost:3000) | Local app runs against `moi_db` |
| 5 | LOCAL | Read the design context | `.impeccable.md` at the root of the deploy branch: bold, technical, optimistic; violet, lavender, deep violet and porcelain; light first with full dark mode; no generic gradients or neon crypto styling. Use the MOI logo with its lettering (a bare planet was fixed on 2026-09-15). Visual brand: `moi-devrel/design` | Read |
| 6 | LOCAL | Check, because CI will not | `pnpm run ci`, which the `ci` script defines as lint with zero warnings, typecheck, tests and `pnpm check:migrations` | Exit 0 |
| 7 | GATE | If the change adds a migration or enables a task | Stop. Do `points-settings-and-database.md` first: DevOps applies the migration to production before this pull request merges, because the merge is the deploy and the new build refuses to start on an older database. A task is enabled only after its environment names are wired (`points-tasks.md`) | The database is ahead of or equal to the build |
| 8 | GATE | Push and open one PR, base `feature/ci-cd` | "Ready to push `<branch>` (files: ...) to origin as `<login>` and open one PR against `feature/ci-cd`. Yes?" Body is part A of `templates/change-checklist.md` with the `pnpm run ci` result. Review tweaks go on one batch branch and one PR, not a PR per change (2026-09-15; #16 to #20 were folded into #21) | PR open |
| 9 | GATE | Merge (this builds and replaces the running container) | Name the PR, the branch `feature/ci-cd`, and "this deploys production now". Who approves is not recorded. ASK: Rahul | Merged |
| 10 | VERIFY | Read the live site | Wait for the run (step 1's command), then `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" points`. Read the numbers: `migrations.applied` equals `expected` and the origin is `https://points.moi.technology`. Sign in for real and open the page you changed | Healthy and the change is visible |

A manual run (GATE): `gh workflow run "MOI Project CI/CD" -R sarvalabs/moi-project --ref feature/ci-cd`, or Actions, "MOI Project CI/CD", Run workflow, branch `feature/ci-cd`. It rebuilds the image, replaces the container and rewrites the box's `.env`.

## Pull request states on 13 October 2026 (check with `gh pr list -R sarvalabs/moi-project --state all`)

| PR | What | State |
|---|---|---|
| #23 | The review batch: sign-in emails, leaderboard avatars, any active wallet key, X verify capped at 20 likes, no social audit job or clawbacks, a maintenance job | Merged, live |
| #22 | Webinar bounties (`points-tasks.md`) | Merged and deployed 13 October. The first deploy run failed on an expired `GHCR_PAT`; DevOps replaced it and the re-run went through |
| #21 | The first form of the review batch | Closed, replaced by #23 |
| #24 | CI/CD hardening: trigger moves to `main`, adds `ci.yml`, a rollback input and `CICD.md`, the only operator guide | Draft, for Upendhar. Needs DevOps setup first. `CICD.md` is on this PR's branch, not on `feature/ci-cd` |
| #15 | The earlier form of #24 | Closed |
| #1 | The original CI/CD from DevOps | Upendhar's to close |
| `sarvalabs/Points-Program` | The old repo for the session 8 challenge | Archived 13 October |

## Traps
- A merge to `feature/ci-cd` is production. There is no staging step.
- A new environment variable needs a pull request that edits `deploy.yml`, and a value in GitHub (`points-settings-and-database.md`).
- The README on the deploy branch may still describe the nightly social audit that #23 removed (`/api/jobs/social-audit` answers 404). Trust the health route and the code.
- A deploy that fails before the app starts: read the failed step. An expired `GHCR_PAT` made the first deploy of 13 October fail; DevOps replaces that token.
- Do not keep the box's `.env` or `DATABASE_URL` on a laptop.
- The old Vercel project and its schedule may still exist; retire it. Who owns it is not recorded. ASK: Rahul.

## Not yet known
- Which pnpm version the image uses. Whether older images exist. ASK: Upendhar.
- Who approves and merges. ASK: Rahul.
- Whether `sarvalabs/Points-Program` is still used. ASK: Rahul.
