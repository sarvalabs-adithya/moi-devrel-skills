# Points Program: tasks, X campaigns and webinar bounties

Updated 13 October 2026. The bounty section follows `project-handover-docs/POINTS-PROGRAM.md` ("Running a webinar bounty"; PR #22, deployed 13 October); where they differ, that document wins. Facts about the code are as of 2026-10-02 (branch `feature/ci-cd`, re-read 2026-10-03) unless a line says otherwise, and the live reads (`/api/health`, `/api/tasks`) are 2026-10-03. Back to `../SKILL.md`. The webinar a bounty belongs to is `moi-webinar`; its announcement and proof form are in `moi-webinar/references/after-the-session.md`.

Points: A security finding is open on this product as of 2026-10-02. The handover note is the Open items of `project-handover-docs/POINTS-PROGRAM.md`; read it before touching its admin.

A step marked ADMIN needs the operator to confirm first that the handover note was read. Everything here changes what members can earn, so each ADMIN or merge step is a GATE. Awarding points is permanent: the ledger cannot be edited and point clawbacks were removed in PR #23.

## What a task is
- A task is a row in the database table `tasks` (id, title, description, points, verification type, active, sort order, metadata) plus an entry in `config/reward-tasks.ts` that says whether it is `enabled` and which environment names it needs (`requiredEnv`). A task shows on the member dashboard only when both agree. A disabled task is hidden and its verification route rejects direct calls.
- Points are appended to `points_ledger`. A database trigger makes it append-only, so an award cannot be edited or deleted. A wrong points value only affects future awards.
- On 2026-10-03 `/api/health` lists four enabled tasks and `/api/tasks` shows the same four. Campaigns (`x_like_campaign:<uuid>`) and bounties (`bounty:<uuid>`) are created at run time and are not in that list.

| Task id | Points | State |
|---|---|---|
| `join_x_verified` | 50 | On. Needs `X_TARGET_URL`, `X_CLIENT_ID`, `X_CLIENT_SECRET` |
| `join_discord` | 50 | On. Needs the five Discord names |
| `join_telegram` | 50 | On. Needs the five Telegram names |
| `create_wallet` | 100 | On. Needs `MOI_NETWORK`, `REOWN_PROJECT_ID` |
| `join_x` | 50 | Off, legacy, replaced by `join_x_verified` (migration 0008 set it inactive) |
| `claim_faucet` | 100 | Off (config) |
| `deploy_agent` | 200 | Off, no working verifier ("keep disabled" in the config comment) |
| `challenge_access_policy` | 500 | Off. Session 8's code challenge, deployed but off |

Points are the `TASK_POINTS` values in `lib/rewards/tasks.ts`. The live API shows only enabled tasks, so the database value of an off task is not visible from outside.
- Admin access is an email in the `ADMIN_EMAILS` Actions variable (once Google has verified it) or a row in `admin_users`. On 13 October `admin_users` was empty, so `ADMIN_EMAILS` is the only source. To add an admin, put their Google email into `ADMIN_EMAILS` (keep the existing ones, comma separated), then redeploy: a GATE (`points-settings-and-database.md`). ASK: Rahul who may be an admin. A member without it who opens the admin page is sent to the dashboard, and an anonymous visitor to the sign-in page. That looks like a bug and is not.

## Run: an X "like" campaign (no code)

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Brief | Title (3 to 100 characters), description (3 to 500), points (a whole number from 1 to 100000), and 1 to 5 distinct post addresses of the form `https://x.com/<account>/status/<id>`. Check the posts are live and the points value with the owner of the campaign | The brief is written down (a table of these five fields) |
| 2 | GATE | ADMIN: create the draft | Sign in at `https://points.moi.technology` with an account that has admin access, open the admin page ("X campaign control"), Create draft. It is stored with `tasks.active = false` and the id `x_like_campaign:<uuid>` | The draft is listed |
| 3 | LOCAL | Read it back | Only a draft can be edited (Save draft). A closed campaign can never be republished | The operator approves the draft |
| 4 | GATE | ADMIN: Publish | Publishing closes the live campaign automatically: one campaign is live at a time. "Close campaign" ends one without replacing it | Status active |
| 5 | VERIFY | Read what members see | Sign in as a member with a verified X connection (`join_x_verified`) and open the dashboard: the campaign board shows the live campaign. `GET /api/tasks` does not list campaigns, because it returns only the tasks named in `config/reward-tasks.ts`; a missing campaign there is not a fault | The board shows the campaign with the right points |

Each action writes an `admin_audit_events` record. Verification needs X API budget; Verify reads the 20 most recent likes only (one request), a cap that is live since PR #23. The X developer app is under the sarvalabsdeveloper@gmail.com login (`ENV-VARS.md`).

## Run: a webinar bounty (no code, no deploy)
A bounty is a small hand-graded form that a Builders session ends with. It is a `tasks` row with the id `bounty:<uuid>`; the session, brief link, deadline and fields sit in its metadata, and each member's answers are an ordinary task completion. No new table, no migration. Nothing is awarded by a machine. No bounty has been created on production yet (13 October), so the first one is its own test: run it end to end with one real submission before a webinar relies on it. The operator does the clicks; Claude writes the brief and the values.

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Baseline and the brief | `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" points`. From the session's owner (`moi-webinar`): title, description, session number, brief link, an optional deadline, and one to six fields. Each field has a label, a type (interaction hash, link, number or text), its points, a required box and optional help text. The total across the fields is the bounty's points, at most 10,000. Check the operator's Google email is in `ADMIN_EMAILS` | The fields and points are written down |
| 2 | GATE | ADMIN: create it | Sign in as an admin, open `/admin`, Webinar bounties, fill the composer under What members send, Add field for each extra field, Create bounty. It starts closed | The bounty is listed as closed |
| 3 | LOCAL | Read it back | The fields and their points are locked while the bounty is open and once a submission is waiting or approved. Title, description, brief link, deadline and session can change at any time | The operator approves the values |
| 4 | GATE | ADMIN: Open it at the session end | Press Open when the session ends and announce the brief link (`moi-webinar`). Members with a linked wallet see it on their dashboard under Webinar bounties, one box per field | Status open, and the announcement went out |
| 5 | GATE | ADMIN: grade | Submissions appear under Waiting for review with the member's name, email, linked wallet and each answer under its field, with an Accept tick showing its points. A hash answer shows what the chain said and whether another bounty already holds it. Required answers are always ticked (a wrong one means Reject). Untick an optional answer to leave its points out, then Award, or Reject with a reason the member sees. One yes covers one member's submission | Each submission is awarded or rejected |
| 6 | GATE | ADMIN: Close it | Press Close when it is over. A bounty with submissions waiting cannot be closed, so review them first | Status closed |
| 7 | VERIFY | Read the result | `admin_audit_events` holds a row for each action. As a member, the dashboard total and the leaderboard show the awarded points | The numbers match what was awarded |

Rules of the bounty:
- Grader: an admin, the session host or DevRel. You cannot approve your own submission. Who grades beyond that is not settled. ASK: Rahul.
- Award pays the ticked answers' points at once, through the same path as every task, so a member is paid once per bounty. It is permanent. Never award without the operator's yes for that submission.
- Reject needs a reason, and the member can send new answers. If the member sent new answers after your page loaded, the action is refused and the page reloads.
- The deadline stops new submissions only. Approving needs the bounty open, so to approve a late submission re-open it first, then close it again.
- Approving records what was accepted, drops the text answers from the record and keeps the hashes, links and numbers as the evidence. Names, emails and wallets on this page are personal data: do not paste them anywhere.
- A hash answer is checked against the chain only when the server has `MOI_RPC_URL`. `deploy.yml` passes it since PR #22, but the Actions variable is not set (13 October), so that chain note is off and the hashes are judged by hand. Setting it is a GATE (`points-settings-and-database.md`) and needs a redeploy.
- The admin can also be driven from the browser console (documented in the `moi-project` README). There are no API tokens; the admin's session cookie protects every route. Claude never handles that cookie.

## Legacy: code dev challenge (session 8 style, deployed but off)
The older way to run a session bounty: a verifier, a registry entry, a task id, a brief page, a migration that seeds the task, and a flag. Session 8's challenge (`challenge_access_policy`, 500 points, four interaction hashes checked from chain reads) is built this way and is deployed but off. Bounties replace this for ordinary sessions; a code challenge is only worth it when the check is more than "called this logic". In order:

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Baseline and the brief | `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" points`; the rules of the challenge from the session's owner (`moi-webinar`); the devnet address its reads use (ASK: Gokul) | The rules are written down |
| 2 | LOCAL | The verifier | `lib/rewards/challenges/<name>.ts` with `parseSubmission` and a `verify` that decides from chain reads only. Model: `access-policy.ts` | Unit tests pass |
| 3 | LOCAL | Register it | `lib/rewards/challenges/index.ts`: `taskId`, `title`, `href`, `difficulty`, `estimate`, `session`, `fields`, `parse`, `verify` | Registered |
| 4 | LOCAL | Task ids | Add the id to `TASK_IDS` and `TASK_POINTS` in `lib/rewards/tasks.ts` (a test keeps the two equal). An entry in `config/reward-tasks.ts` with `enabled: false` and `requiredEnv: ["MOI_RPC_URL"]` | `pnpm run ci` passes |
| 5 | LOCAL | The brief page | `app/challenges/<name>/page.tsx`, modelled on `app/challenges/access-policy/page.tsx` | Page renders |
| 6 | LOCAL | Seed the task | A new hand-written migration that copies `drizzle/0009_dev_challenges.sql` (`templates/points-task-migration.sql`, Pattern A): `INSERT ... ON CONFLICT ("id") DO NOTHING` with `verification_type = 'onchain_challenge'`, 500 points for hours of work, and metadata `{"kind":"challenge","href":...,"session":N}` | `pnpm check:migrations` passes |
| 7 | GATE | One real submission end to end, in a local copy | A production task that is off rejects direct calls, so run the app locally with `enabled: true` and `MOI_RPC_URL` set in your local `.env.local`, and submit one real devnet run. A person with a wallet makes the run: Claude never handles a recovery phrase. The operator decides to spend the devnet funds | One accepted submission |
| 8 | GATE | Apply the migration to production first, then ship the code | `points-settings-and-database.md` (DevOps applies it before the merge), then `points-ship.md`, with `enabled: false` | Health shows applied equals expected |
| 9 | GATE | Give the container its chain address | `deploy.yml` passes `MOI_RPC_URL` since PR #22; set the Actions variable (`points-settings-and-database.md`) and redeploy | The variable reaches the container |
| 10 | GATE | Flip `enabled` in a later pull request | `points-ship.md` | Merged |
| 11 | VERIFY | Read the live task list | `curl -s https://points.moi.technology/api/tasks` lists the challenge, and `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" points` shows no WARN about the task list | It does |

`challenge_access_policy` asks for four interaction hashes and checks, from chain reads: a deploy from the linked wallet, a call refused under the policy, the grant, an accepted call from a different account the policy names, and a revoke after the grant. It was not live on game day (`moi-webinar`). Open it (set `MOI_RPC_URL`, one real submission, the flag) or drop it: ASK: Rahul.

## Run: switch a standard task on or off, or change its points

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Env first | Every name in the task's `requiredEnv` must be in `deploy.yml` and set in GitHub. Enabling a task whose environment is not passed stops the container at startup | Every name is wired |
| 2 | LOCAL | On or off | Flip `enabled` in `config/reward-tasks.ts` | `pnpm run ci` passes |
| 3 | LOCAL | New points value | A hand-written migration with `UPDATE "tasks" SET "points" = N, "updated_at" = now() WHERE "id" = '<id>'` (patterns in `0004` and `0008`), and the same number in `TASK_POINTS` in `lib/rewards/tasks.ts`. The database decides what is awarded; `TASK_POINTS` feeds displayed totals and a test | Both agree |
| 4 | GATE | Ship in the order of `points-settings-and-database.md` | A points change is a migration: DevOps applies it to production first, then the code merges | Healthy |
| 5 | VERIFY | Read the task list | `curl -s https://points.moi.technology/api/tasks` | The new points show |

## Decisions already taken (the previous operator, 2026-09-15; live with PR #23)
No after-the-fact enforcement: a member is checked once, at claim. X verify is capped at 20 likes. Profile pictures stay on the leaderboard. A wallet link accepts any active key. Point clawbacks and the nightly social audit are gone. Whether these stand is a Rahul decision. ASK: Rahul.

## Traps
- A task row can be `active` in the database while `enabled` is false in config. The task stays hidden. Both must say yes.
- Env names in `.env.example` that the deploy does not pass: `FAUCET_*`. Enabling a task that needs one without editing `deploy.yml` fails at startup. `MOI_RPC_URL` is passed since PR #22 but its Actions variable is unset.
- `TASK_IDS` and `TASK_POINTS` list tasks twice. A test fails if they differ.
- A bounty's fields and points are locked while it is open and once a submission is waiting or approved. Get them right while it is still closed.

## Not yet known
- Whether campaigns keep using the paid X API. ASK: Rahul.
- Whether another code challenge is planned. ASK: Rahul.
- Who may grade bounties beyond "an admin". ASK: Rahul.
