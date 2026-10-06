# Points Program: tasks, X campaigns and dev challenges

Facts are as of 2026-10-02 for the code (branch `feature/ci-cd` at `92f9c48`, plus the branch `review-batch` of pull request #21 where a line says so, re-read 2026-10-03) and 2026-10-03 for the live reads (`/api/health`, `/api/tasks`). Back to `../GUIDE.md`. The webinar a challenge belongs to is `moi-webinar`; its bounty announcement and proof form are in `moi-webinar/references/after-the-session.md`.

Points: A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin.

A step marked ADMIN needs the operator to confirm first that the handover note was read. Everything here changes what members can earn, so each ADMIN or merge step is a GATE.

## What a task is
- A task is a row in the database table `tasks` (id, title, description, points, verification type, active, sort order, metadata) plus an entry in `config/reward-tasks.ts` that says whether it is `enabled` and which environment names it needs (`requiredEnv`). A task shows on the member dashboard only when both agree. A disabled task is hidden and its verification route rejects direct calls.
- Points are appended to `points_ledger`. A database trigger makes it append-only, so an award cannot be edited or deleted. A wrong points value only affects future awards.
- On 2026-10-03 `/api/health` lists four enabled tasks and `/api/tasks` shows the same four.

| Task id | Points | State |
|---|---|---|
| `join_x_verified` | 50 | On. Needs `X_TARGET_URL`, `X_CLIENT_ID`, `X_CLIENT_SECRET` |
| `join_discord` | 50 | On. Needs the five Discord names |
| `join_telegram` | 50 | On. Needs the five Telegram names |
| `create_wallet` | 100 | On. Needs `MOI_NETWORK`, `REOWN_PROJECT_ID` |
| `join_x` | 50 | Off, legacy, replaced by `join_x_verified` (migration 0008 set it inactive) |
| `claim_faucet` | 100 | Off (config) |
| `deploy_agent` | 200 | Off, no working verifier ("keep disabled" in the config comment) |
| `challenge_access_policy` | 500 | Off. Session 8's dev challenge |

Points are the `TASK_POINTS` values in `lib/rewards/tasks.ts`. The live API shows only enabled tasks, so the database value of an off task is not visible from outside.
- Admin access is granted by a setting or a database row. Either is a production change and a GATE (`points-settings-and-database.md`). ASK: Rahul who decides who is an admin. A member without it who opens the admin page is sent to the dashboard, and an anonymous visitor to the sign-in page. That looks like a bug and is not.

## Run: an X "like" campaign (no code)

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Brief | Title (3 to 100 characters), description (3 to 500), points (a whole number from 1 to 100000), and 1 to 5 distinct post addresses of the form `https://x.com/<account>/status/<id>`. Check the posts are live and the points value with the owner of the campaign | The brief is written down (a table of these five fields) |
| 2 | GATE | ADMIN: create the draft | Sign in at `https://points.moi.technology` with an account that has admin access, open the admin page ("X campaign control"), Create draft. It is stored with `tasks.active = false` and the id `x_like_campaign:<uuid>` | The draft is listed |
| 3 | LOCAL | Read it back | Only a draft can be edited (Save draft). A closed campaign can never be republished | The operator approves the draft |
| 4 | GATE | ADMIN: Publish | Publishing closes the live campaign automatically: one campaign is live at a time. "Close campaign" ends one without replacing it | Status active |
| 5 | VERIFY | Read what members see | Sign in as a member with a verified X connection (`join_x_verified`) and open the dashboard: the campaign board shows the live campaign. `GET /api/tasks` does not list campaigns, because it returns only the tasks named in `config/reward-tasks.ts`; a missing campaign there is not a fault | The board shows the campaign with the right points |

Each action writes an `admin_audit_events` record. Verification needs X API budget. The previous operator had none for large reads on 2026-09-15 ("keep it 20 only"), and PR #21 limits Verify to the 20 most recent likes (one request); that cap is not live until #21 merges. Who holds the X developer app is unknown. ASK: Adithya.

## Run: a dev challenge (a webinar bounty, needs code)
The registry file says it: adding one is writing `verify`, adding a row, seeding the task and flipping the flag. In order:

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Baseline and the brief | `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" points`; the rules of the challenge from the session's owner (`moi-webinar`); the devnet address its reads use (ASK: Gokul) | The rules are written down |
| 2 | LOCAL | The verifier | `lib/rewards/challenges/<name>.ts` with `parseSubmission` and a `verify` that decides from chain reads only. Model: `access-policy.ts` | Unit tests pass |
| 3 | LOCAL | Register it | `lib/rewards/challenges/index.ts`: `taskId`, `title`, `href`, `difficulty`, `estimate`, `session`, `fields`, `parse`, `verify` | Registered |
| 4 | LOCAL | Task ids | Add the id to `TASK_IDS` and `TASK_POINTS` in `lib/rewards/tasks.ts` (a test keeps the two equal). An entry in `config/reward-tasks.ts` with `enabled: false` and `requiredEnv: ["MOI_RPC_URL"]` | `pnpm run ci` passes |
| 5 | LOCAL | The brief page | `app/challenges/<name>/page.tsx`, modelled on `app/challenges/access-policy/page.tsx` | Page renders |
| 6 | LOCAL | Seed the task | A new hand-written migration that copies `drizzle/0009_dev_challenges.sql` (`templates/points-task-migration.sql`): `INSERT ... ON CONFLICT ("id") DO NOTHING` with `verification_type = 'onchain_challenge'`, 500 points for hours of work, and metadata `{"kind":"challenge","href":...,"session":N}` | `pnpm check:migrations` passes |
| 7 | GATE | One real submission end to end, in a local copy | A production task that is off rejects direct calls, so run the app locally with `enabled: true` and `MOI_RPC_URL` set in your local `.env.local`, and submit one real devnet run (inferred; no record shows how the previous operator tested). A person with a wallet makes the run: Claude never handles a recovery phrase. The operator decides to spend the devnet funds | One accepted submission |
| 8 | GATE | Apply the migration to production first, then ship the code | `points-settings-and-database.md` (DevOps applies it before the merge), then `points-ship.md`, with `enabled: false` | Health shows applied equals expected |
| 9 | GATE | Give the deploy its chain address | Add `MOI_RPC_URL` to `deploy.yml` (it is not passed today) and set it in GitHub (`points-settings-and-database.md`) | The variable reaches the container |
| 10 | GATE | Flip `enabled` in a later pull request | `points-ship.md` | Merged |
| 11 | VERIFY | Read the live task list | `curl -s https://points.moi.technology/api/tasks` lists the challenge, and `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" points` shows no WARN about the task list | It does |

The live example `challenge_access_policy` (session 8, 500 points) asks for four interaction hashes and checks, from chain reads: a deploy from the linked wallet, a call refused under the policy, the grant, an accepted call from a different account the policy names, and a revoke after the grant. It is disabled in production. The session 8 bounty was not live on game day (`moi-webinar`). Whether it ever went live is unknown. ASK: Adithya.

## Run: switch a standard task on or off, or change its points

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Env first | Every name in the task's `requiredEnv` must be in `deploy.yml` and set in GitHub. Enabling a task whose environment is not passed stops the container at startup | Every name is wired |
| 2 | LOCAL | On or off | Flip `enabled` in `config/reward-tasks.ts` | `pnpm run ci` passes |
| 3 | LOCAL | New points value | A hand-written migration with `UPDATE "tasks" SET "points" = N, "updated_at" = now() WHERE "id" = '<id>'` (patterns in `0004` and `0008`), and the same number in `TASK_POINTS` in `lib/rewards/tasks.ts`. The database decides what is awarded; `TASK_POINTS` feeds displayed totals and a test | Both agree |
| 4 | GATE | Ship in the order of `points-settings-and-database.md` | A points change is a migration: DevOps applies it to production first, then the code merges | Healthy |
| 5 | VERIFY | Read the task list | `curl -s https://points.moi.technology/api/tasks` | The new points show |

## Decisions already taken (the previous operator, 2026-09-15; most land with PR #21)
No after-the-fact enforcement: a member is checked once, at claim. X verify is capped at 20 likes. Profile pictures stay on the leaderboard. A wallet link accepts any active key. Whether these stand is a Rahul decision. ASK: Rahul.

## Traps
- A task row can be `active` in the database while `enabled` is false in config. The task stays hidden. Both must say yes.
- Env names in `.env.example` that the deploy does not pass: `MOI_RPC_URL`, `FAUCET_*`. Enabling a task that needs one without editing `deploy.yml` fails at startup.
- `TASK_IDS` and `TASK_POINTS` list tasks twice. A test fails if they differ.

## Not yet known
- Whether campaigns keep using the paid X API, and who holds the X app. ASK: Adithya.
- Whether another challenge is planned. ASK: Rahul.
