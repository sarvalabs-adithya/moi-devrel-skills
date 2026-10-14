# Points health: is it up, is the schema current, what is already broken

Updated 13 October 2026 for the pull request states and the faults below. Other facts are as of 2026-10-03 for the live reads and 2026-10-02 for the repo. Back to `../SKILL.md`.

Points: A security finding is open on this product as of 2026-10-02. The handover note is the Open items of `project-handover-docs/POINTS-PROGRAM.md`; read it before touching its admin.

## "Points is down or members report errors"

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Read the state | `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" points`. A single FAIL is not an outage: run it once more | You know which lines FAIL |
| 2 | CHECK | Read the numbers, not the status | `curl -s https://points.moi.technology/api/health`. Healthy is `healthy` true, `database` "ok", and `migrations.applied` equal to `expected` (above `expected` is allowed by the app and shows as a WARN: it is the state between applying a migration and merging its code). The route answers 503 while unhealthy, so a monitor and the body agree | You can say which of the three is wrong |
| 3 | CHECK | Which case | `database` "error": the database is unreachable or the login changed, so the Supabase owner (ASK: Rahul). `applied` below `expected`: a build ahead of the database, so `points-settings-and-database.md` and DevOps at once. No answer at all: the container is down or crash-looping on startup, so DevOps. `origin` not the production address: `BETTER_AUTH_URL` is wrong (`points-settings-and-database.md`) | One sentence |
| 4 | CHECK | Was it a deploy? | `gh run list -R sarvalabs/moi-project --workflow "MOI Project CI/CD" --limit 5`. The old container is removed before the new one starts | Known |
| 5 | LOCAL | Record it | `templates/incident-note.md` | Note exists |
| 6 | GATE | Ask DevOps for the container log | `templates/devops-request.md`, request R10 in `who-to-ask.md`. On 2026-09-15 DevOps found "the x_campaigns table is missing" from the container log. The operator sends it to Upendhar | A log excerpt |
| 7 | GATE | Do not redeploy to "see if it helps" | A redeploy replaces the container again. Do it on a yes, after the cause is known (`points-ship.md`) | |
| 8 | VERIFY | Confirm recovery | Step 1 again, then a real sign-in | Healthy |

## What each check proves

| Check | Healthy | Reads |
|---|---|---|
| `GET /api/health` | 200, `healthy` true, `database` "ok", `migrations` applied equals expected (applied above expected: WARN), `origin` `https://points.moi.technology`, `environment` "self-hosted" | The app, the database link and the schema against the build. `sha` is null (P-K1) |
| `enabledTasks` in that JSON | The tasks switched on. 2026-10-03: `join_x_verified`, `join_discord`, `join_telegram`, `create_wallet` | Compare with `GET /api/tasks` (the script does) |
| `GET /api/tasks` | 200, the same four with 50, 50, 50 and 100 points | The public task list |
| `GET /leaderboard`, `GET /api/leaderboard` | 200 | The public pages |
| `GET /` | 307 to `/login` when anonymous | The app routes |
| Preview host `GET /api/health` | 200 | `preview.points.moi.technology` is the same box, not production |

Observed health on 2026-10-03: `healthy` true, `database` "ok", `migrations` applied 11 of 11, `sha` null, `environment` "self-hosted". On 13 October, after PR #22 and #23: applied 11 of 11, healthy, the same four tasks (`project-handover-docs/POINTS-PROGRAM.md`).

## Known faults (as of 13 October 2026 unless dated)

| ID | Fault | Fix path | Who |
|---|---|---|---|
| P-K1 | `sha` is null, so you cannot tell which build runs. The deploy sets neither `GIT_SHA` nor a hosting variable. Draft PR #24 (CI/CD hardening) is meant to fix it | A pull request on `deploy.yml` | Rahul decides, Upendhar |
| (none) | Production runs `feature/ci-cd`, with PR #22 and #23 deployed on 13 October. `main` is stale since 2026-08-03. Draft PR #24 moves the trigger to `main` and adds `ci.yml`, a rollback input and `CICD.md`; it replaced the closed #15 and needs DevOps setup first: an `environment: production` with its secrets, a non-root VM user in the docker group, nginx on loopback | `points-ship.md` | Upendhar, Rahul |
| (none) | Pull request states on 13 October: #23 (review batch) and #22 (webinar bounties) are merged and live; #21 is closed; #15 is closed and replaced by draft #24; #1 is Upendhar's to close. The repo `sarvalabs/Points-Program` was archived on 13 October | `points-ship.md` | Upendhar |
| (none) | `/api/jobs/maintenance` is live (401 without `CRON_SECRET`) and nothing schedules it. `/api/jobs/social-audit` answers 404 (the job is gone) | ASK: Upendhar what runs on the box and who schedules it | Upendhar |
| (none) | `SOCIAL_AUDIT_BATCH_SIZE` is still set in Actions and passed by `deploy.yml`, but nothing reads it | Remove the variable and its line in `deploy.yml` (`points-settings-and-database.md`) | Rahul |
| (none) | `MOI_RPC_URL` is passed by `deploy.yml` (PR #22) but the Actions variable is not set (13 October), so the chain note beside a bounty's hash answers is off | `points-settings-and-database.md` | Rahul |
| (none) | The devnet RPC certificate expired on 4 October and was renewed by 5 October. Test a wallet link: the server reads wallet keys from that host | Trap 60 in `traps.md` | Rahul |
| (none) | The database is on the Points email account, free plan, no backups | Put it on a paid plan with backups. ASK: Rahul | Rahul |
| (none) | The schema `backup.tasks_before_0008` still exists. Drop it once the project has backups | `points-settings-and-database.md` | Rahul |
| (none) | `Dockerfile` pins pnpm 11.11.0 and `package.json` pins 10.34.5 | ASK: Upendhar which wins | Upendhar |
| (none) | `X_TOKEN_ENCRYPTION_KEY` and `CLIENT_IP_HEADER` are not passed by the deploy | `points-settings-and-database.md` | Rahul |
| (none) | The old Vercel project may still exist (`points.moi.technology` is on the box, not there). Retire it; its owner is not recorded | ASK: Rahul | Rahul |

## Not yet known
- The command DevOps uses to run the migration, and any schedule on the box. ASK: Upendhar.
- How long a deploy takes: about 4 to 5 minutes (inferred). Whether anything alerts when it fails. ASK: Upendhar.
- Who is told when Points is down. ASK: Rahul.
