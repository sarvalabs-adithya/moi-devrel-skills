# Points Program: secrets, variables and database changes

Updated 13 October 2026 for PR #22 and #23, the admin list and the console owners. Other facts are as of 2026-10-02 for the repo (branch `feature/ci-cd` at `92f9c48`: `deploy.yml`, `.env.example`, `scripts/migrate.mjs`, `scripts/check-migrations.ts`, `drizzle/TRIGGERS.md`, `lib/startup.ts`, `lib/db/migrations.ts`, re-read 2026-10-03) and the research notes of that date; 2026-10-03 for the live health read. Values are never written here: names only. Where each name lives and who grants it: `moi-devrel/references/keys-and-access.md`. Back to `../SKILL.md`.

Points: A security finding is open on this product as of 2026-10-02. The handover note is the Open items of `project-handover-docs/POINTS-PROGRAM.md`; read it before touching its admin.

A step marked ADMIN needs the operator to confirm first that the handover note was read.

## How a setting reaches the container
- Settings are repository secrets and variables of `sarvalabs/moi-project` (no environments are configured). Only a repo admin can edit them; the admins on 2026-09-15 were gokul, chandra, git, adithya and upendhar. GitHub secrets cannot be read back and no shared vault exists. ASK: Rahul which vault.
- At each deploy the non-secret variables are written into the app's `.env` on the box, rewritten from scratch each time, and the secrets are handed to the container as environment. A name that `deploy.yml` does not list never reaches the app, whatever is set in GitHub.
- Secrets in `deploy.yml`: `DATABASE_URL`, `BETTER_AUTH_SECRET`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `CRON_SECRET`, `DISCORD_CLIENT_SECRET`, `DISCORD_BOT_TOKEN`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_WEBHOOK_SECRET`, `X_CLIENT_SECRET`, `RESEND_API_KEY`, plus `GHCR_PAT` and `TELEPORT_JOIN_TOKEN` for the pipeline.
- Variables in `deploy.yml`: `TELEPORT_PROXY`, `VM_HOST`, `VM_USER`, `BETTER_AUTH_URL`, `X_TARGET_URL`, `MOI_NETWORK`, `VERIFICATION_WINDOW_MINUTES`, `VERIFICATION_LIMIT_PER_USER`, `VERIFICATION_LIMIT_PER_IP`, `SOCIAL_AUDIT_BATCH_SIZE`, `DISCORD_CLIENT_ID`, `DISCORD_GUILD_ID`, `DISCORD_INVITE_URL`, `TELEGRAM_BOT_USERNAME`, `TELEGRAM_CHAT_ID`, `TELEGRAM_INVITE_MODE`, `X_CLIENT_ID`, `ADMIN_EMAILS`, `REOWN_PROJECT_ID`, `EMAIL_FROM`, and, since PR #22, `MOI_RPC_URL`. `SOCIAL_AUDIT_BATCH_SIZE` is still set in GitHub and passed, but nothing reads it (the social audit job is gone): remove it with a pull request that deletes its line in `deploy.yml`, then delete the variable.
- In `.env.example` and passed by nothing: `X_TOKEN_ENCRYPTION_KEY`, `X_TOKEN_ENCRYPTION_KEY_PREVIOUS`, `CLIENT_IP_HEADER`, `DATABASE_SSL`, `PG_POOL_MAX`, `FAUCET_*`, `NEXT_PUBLIC_SITE_URL`.
- `MOI_RPC_URL` is passed by `deploy.yml` (PR #22) but the Actions variable is not set (13 October). Bounties work without it; with it the admin sees a chain note beside hash answers, and a code challenge needs it. The value is the devnet RPC address (`project-handover-docs/ENV-VARS.md`). Setting it is a GATE, then a redeploy. Moving one into the container is a pull request that edits `deploy.yml` plus a value in GitHub.
- Sign-in emails need both `RESEND_API_KEY` and `EMAIL_FROM`. With only one, the app logs a warning and sends none (`lib/startup.ts`).
- `BETTER_AUTH_URL` must be the public https address. It was `http://localhost:3000` on one failed run and `http://preview.points.moi.technology` on another, and a wrong value breaks sign-in and the health origin.
- Each provider's callback address must match `BETTER_AUTH_URL`. The list for Google, Discord, X and the Telegram webhook is section 8 of `CICD.md`, which lives on the branch of draft PR #24, not on `feature/ci-cd`. Google rejects a raw IP address as a redirect (2026-09-15, "400: invalid_request"), so use the domain.
- The provider apps (Google, X, Discord, Telegram, Reown, Resend) are under the `sarvalabsdeveloper@gmail.com` login (`project-handover-docs/ENV-VARS.md`). ASK: Rahul for access.
- Admin access comes only from `ADMIN_EMAILS` (the `admin_users` table was empty on 13 October). To add an admin, put their Google email into the `ADMIN_EMAILS` variable, keeping the existing ones, and redeploy. A GATE; ASK: Rahul who may be an admin.

## Run: change a secret or variable

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Is the name wired? | Compare it with the two lists above. A name in neither needs a pull request on `deploy.yml` first (`points-ship.md`) | A yes or no |
| 2 | CHECK | Read the set names | `gh secret list -R sarvalabs/moi-project` and `gh variable list -R sarvalabs/moi-project` (names only; needs access to the repository's settings, else ASK: Rahul) | The name is there |
| 3 | CHECK | Old value kept? | In the vault, or the operator accepts the loss | Written down |
| 4 | GATE | Set it | The operator runs `gh secret set <NAME> -R sarvalabs/moi-project` (or `gh variable set`) and types the value at the hidden prompt. New random values: the operator runs `openssl rand -hex 32`. Claude never sees or types a value | Listed by name |
| 5 | GATE | Redeploy | `gh workflow run "MOI Project CI/CD" -R sarvalabs/moi-project --ref feature/ci-cd`, or Actions, "MOI Project CI/CD", Run workflow, branch `feature/ci-cd`. It rebuilds the image, so the site is down for a short time while the container is replaced | The run finishes |
| 6 | VERIFY | Use it | `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" points`, then a real sign-in and the one feature that uses the setting | It works |

## The database
- Postgres on Supabase, through Drizzle. The production project is on the Points Program's own email account (stated by the previous operator, 2026-10-06), on the free plan with no backups. It holds every user and every point. Moving it to a company login and a paid plan is an open item (`project-handover-docs/POINTS-PROGRAM.md`). ASK: Rahul.
- Eleven migrations, `0000` to `0010`, and `/api/health` shows `applied 11, expected 11` (2026-10-03).
- Migrations are written by hand. `drizzle/TRIGGERS.md` says do not run `drizzle-kit generate` or `drizzle-kit push`: the snapshots stop at 0003 and a generated diff would try to recreate objects that exist. Follow the repo.
- Triggers are part of the design: `points_ledger` is append-only; a verified completion can only move to `rejected`; a linked social account cannot be reassigned; a bound wallet cannot change except inside the erasure transaction. People with points are anonymised (`eraseUser`) and not deleted. `pnpm db:reset:*` uses `TRUNCATE`, which skips the triggers: run it on a local database only.

## Run: add a migration (the database first, then the code)
The rule at the tip (`lib/startup.ts`, `lib/db/migrations.ts`): the build counts the entries in its own `drizzle/meta/_journal.json`, and in production the app refuses to start when the database holds fewer. A database that holds more is allowed (the check is `applied >= expected`). A merge to `feature/ci-cd` is the deploy, and the old container is removed first. So the migration has to reach production before any merge that carries its journal entry. The order of 2026-09-15 (a pull request with only the migration, merged, then DevOps ran it) worked before the startup checks arrived (they were merged later that day, in #14). Repeated now, it would probably leave the site down from the deploy until the run: the startup check throws in the new container, and the container's restart policy (`unless-stopped`) then retries it (inferred from the code, not tried).

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | LOCAL | Write it | In the clone (`points-ship.md` step 2): `drizzle/00NN_<name>.sql` by hand. End each statement with its terminator, then `--> statement-breakpoint` on its own line (the runner splits on that text). Start from `templates/points-task-migration.sql` for a task row | File on disk |
| 2 | LOCAL | Journal it | Add an entry to `drizzle/meta/_journal.json`: `idx` the next integer, `version` "7", `when` greater than the previous entry, `tag` equal to the file name without `.sql`, `breakpoints` true. Edit `lib/db/schema.ts` by hand to match | `pnpm check:migrations` prints `migrations ok` |
| 3 | LOCAL | Try it locally | `pnpm db:migrate` against `moi_db` only. Look at `DATABASE_URL` in `.env.local` first: it must point at the local database | Applies, and the app runs on it |
| 4 | GATE | Ask DevOps to apply it to production before the merge | Request R8 in `who-to-ask.md`. The runner is `node scripts/migrate.mjs` (`pnpm migrate`). It reads the `drizzle` folder of the current directory, or the folder named in `MIGRATIONS_DIR`, and `DATABASE_URL`, so it can run from a checkout of your branch. It applies every journal entry newer than the last, in one transaction, under a lock, and prints `migrations: applied <tag>` for each, then `migrations: N applied, M total`, or `migrations: up to date (N applied)`. A production database write. Whether DevOps can run it from a branch checkout, and how, is not recorded. ASK: Upendhar. If it cannot be done first, an announced outage is the only other order: ASK: Rahul | You have the printed lines |
| 5 | VERIFY | Health, database ahead | `curl -s https://points.moi.technology/api/health` shows `applied` one above `expected` and `healthy` true (`bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" points` prints a WARN) | The database is ahead of the running build, and healthy |
| 6 | GATE | Now ship the code that needs it | `points-ship.md` | The deploy finishes |
| 7 | VERIFY | Health, equal | `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" points` | `applied` equals `expected` and healthy |

## Traps
- A migration is one transaction: a failing statement rolls back the whole batch.
- Take a copy before a risky change: the database has no backup. A schema `backup.tasks_before_0008` made on 2026-09-15 still exists. Dropping it (`drop schema backup cascade`) is a production write. Ask first.
- A wrong `BETTER_AUTH_URL`, a missing task environment or a stale schema each make the site fail at startup or sign-in. Read `/api/health` and the origin after every deploy.
- Never put the production `DATABASE_URL` in a local `.env.local`: `pnpm db:migrate` and `pnpm db:reset:*` would run against production.

## Not yet known
- The command DevOps uses to run the migration on the box (probably inside the container; inferred), and whether DevOps does it on request or needs a ticket. ASK: Upendhar.
- What schedules `/api/jobs/maintenance` (live, 401 without `CRON_SECRET`): nothing does today. The social audit job is gone (`/api/jobs/social-audit` answers 404). `vercel.json` on `main` held the old schedule. ASK: Upendhar.
