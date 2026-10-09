# Points Program

**Status: active.** Live at points.moi.technology with four tasks on: join X (verified), join Discord, join Telegram, create wallet. Inactive: the faucet task, the deploy-agent task, session 8's dev challenge (deployed, switched off), and the webinar bounties (PR #22, open, not merged yet).

MOI Community Points. Members sign in with Google, link their X, Discord and Telegram accounts and a MOI wallet, complete tasks and earn points, and see where they stand on a public leaderboard. Admins run X like campaigns and, once the bounty branch ships, webinar bounties from an admin page. Harsh Gupta wrote the first version and Upendhar the CI/CD; I run it. DevOps owns the box it runs on.

## How it works

**What a member sees**

- Sign in with Google. It is the only login. A sign-in email goes out through Resend when both email names are set.
- The dashboard shows the task board. Each task is a card with its points and a button that verifies it.
- Join X: an X sign-in, then the app checks the member follows the account in X_TARGET_URL. The X connection stays linked and is what campaigns use later.
- Join Discord: a Discord sign-in, then the bot checks the member is in the guild.
- Join Telegram: the member joins the group through the bot (invite mode join_request or direct), and the bot's webhook confirms it.
- Create wallet: the member links a MOI wallet through Reown. The server reads the wallet's keys from the devnet RPC and accepts any active key.
- Points land in a ledger the moment a task is verified. The leaderboard and the member's total read from it.
- Verification attempts are limited per member and per address (defaults: 6 per member and 30 per address in 10 minutes).

**Tasks**

A task is a row in the tasks table (id, title, description, points, verification type, active, sort order, metadata) plus an entry in config/reward-tasks.ts that says whether it is enabled and which settings it needs. A task shows only when both agree. An enabled task whose settings are missing stops the container at startup.

| Task | Points | State |
|---|---|---|
| join_x_verified | 50 | On. Needs the three X names |
| join_discord | 50 | On. Needs the five Discord names |
| join_telegram | 50 | On. Needs the five Telegram names |
| create_wallet | 100 | On. Needs MOI_NETWORK and REOWN_PROJECT_ID |
| join_x | 50 | Off, legacy, replaced by join_x_verified |
| claim_faucet | 100 | Off |
| deploy_agent | 200 | Off, no working verifier |
| challenge_access_policy | 500 | Off. Session 8's dev challenge |

The database value decides what is awarded. TASK_POINTS in lib/rewards/tasks.ts feeds the displayed totals and a test keeps the two lists equal. Campaign and bounty tasks are created at run time with their own id prefixes (x_like_campaign:<uuid>, bounty:<uuid>) and never count towards the fixed total.

**X like campaigns (no code)**

- An admin creates a draft on the admin page: title, description, points, and 1 to 5 X post links.
- Publishing makes it live and closes the previous one. One campaign is live at a time.
- Members with a verified X connection see it on their dashboard and press Verify. The app reads their recent likes through the X API (capped at the 20 most recent once PR #21 merges) and awards the points.
- Close ends it. A closed campaign cannot be republished.

**Webinar bounties (PR #22)**

Every Builders session can end with a bounty: something attendees do for points. The host creates it on the Points site, with no code change and no deploy. It is a tasks row with the id bounty:<uuid>, its settings (session, brief link, deadline, logic id) in the row's metadata, and each member's submission is an ordinary task completion. No new table, no migration.

Two ways to verify, chosen per bounty:
- Review: the member sends a link, an interaction hash or both, plus a note. It waits as pending until a host approves (points awarded then) or rejects with a reason the member sees. A rejected member may send a new proof. When a hash comes with the proof, the server asks the chain whether the member's linked wallet sent it and shows the host the answer, with a warning if another bounty already holds that hash. The host decides.
- On-chain: the member sends one interaction hash. The server reads it from the chain and awards straight away when the member's linked wallet sent it, it succeeded, and it called or deployed the bounty's logic. The logic id is required, because the chain gives no timestamp to tie an interaction to the webinar: deploy a logic for the session and use its id. One interaction pays one bounty.

Members see open bounties on their dashboard under Webinar bounties.

**Dev challenges (code)**

The older way to run a session bounty: a verifier file, a registry entry, a task id, a brief page, a migration that seeds the task, and a flag. Session 8's challenge (challenge_access_policy, 500 points, four interaction hashes checked from chain reads) is built this way and is deployed but off. Bounties replace this for ordinary sessions; a challenge is only worth it when the check is more than "called this logic".

**Admin**

- An admin is an email in ADMIN_EMAILS (once Google has verified it) or a row in the admin_users table.
- There is one admin role. An admin can run campaigns and bounties, erase a member and unlink a member's social accounts.
- Every admin action writes a row in admin_audit_events.
- A member without admin access who opens /admin is sent to the dashboard. That is by design.

**The database rules** (drizzle/TRIGGERS.md)

- The points ledger is append-only. An award cannot be edited or deleted; a wrong points value only affects future awards.
- A verified completion can only move to rejected. Pending to verified, pending to rejected and rejected to pending are allowed.
- A linked social account cannot be reassigned to another member. A bound wallet cannot change except inside an erasure.
- Members with points are anonymised on erasure, never deleted. What a member sent to a bounty is cleared unless the proof was approved, because then it is the evidence for the points.

**How a deploy works**

- A push to feature/ci-cd (not main) runs the CI/CD workflow: build the Docker image, push it to GHCR as latest, log in to the box through Teleport, rewrite the app's env file from the GitHub variables, hand the secrets straight to the container, remove the old container and start the new one.
- About 4 minutes. No staging. No rollback: only latest is pushed.
- On start, in production, the app refuses to boot if the database has fewer migrations than the build, or if an enabled task is missing a setting. A merge that adds a migration or enables a task without its settings takes the site down until it is fixed.
- No pull request runs any check. pnpm run ci is run by whoever ships.
- A maintenance job route exists (/api/jobs/maintenance, called with CRON_SECRET). Nothing is known to call it.

## Stack

| Piece | What it is |
|---|---|
| Next.js 16 + React 19 + TypeScript + Tailwind 4, pnpm | The web app and every API route |
| Postgres on Supabase, through Drizzle | All state: members, linked accounts, tasks, completions, the points ledger, campaigns, audit events. 11 hand-written migrations |
| Better Auth | Google sign-in, the only login |
| X, Discord and Telegram APIs | Task verification and campaigns. The X API is the paid tier |
| Reown + js-moi-signer | Wallet linking. Keys are read from the devnet RPC |
| Resend | Sign-in emails from no-reply@moi.technology |
| Docker + GitHub Actions + GHCR + Teleport | Build and deploy to the DevOps box, one container behind nginx |
| /api/health and /api/jobs/maintenance | The health route (database and migration state) and the housekeeping job |
| vitest | 22 test files on the bounty branch, 190 tests |

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Codebase | Me | sarvalabs/moi-project, private. The branch feature/ci-cd deploys, not main. Repo admins on 4 October: gokul, chandra, git, adithya, upendhar |
| Supabase project | The Points email account | Free plan, no backups. It holds every member and every point |
| Google OAuth client, X developer app (paid API), Discord app and bot, Telegram bot and group, Reown project, Resend account | Confirm who | Each provider's callback must match BETTER_AUTH_URL |
| The box, nginx, TLS, Teleport, DNS, the GHCR image | DevOps (Upendhar) | Container moi-project on host port 31000. preview.points.moi.technology is the same box |
| Devnet RPC address | Protocol team | Written in config/moi-networks.ts; a move is a PR |
| Who is an admin | Confirm who | ADMIN_EMAILS plus the admin_users table |

## Env vars

Where they live: GitHub, sarvalabs/moi-project, Settings, Secrets and variables, Actions (13 secrets and 20 variables on 4 October; secrets cannot be read back). At each deploy the variables are written into the app's env file on the box, rewritten from scratch, and the secrets go straight into the container, so the only readable copy of a secret is inside the running container (DevOps). Locally, .env.local copied from .env.example. A changed value needs a workflow run. A name that deploy.yml does not list never reaches the app, whatever is set in GitHub.

| Variable | What it is | Where the value comes from |
|---|---|---|
| DATABASE_URL | The database | Supabase dashboard, the project, Connect |
| BETTER_AUTH_SECRET | Session signing. Replacing it signs everyone out and makes every stored X connection unreadable until members reconnect | Generate with: openssl rand -hex 32 |
| BETTER_AUTH_URL | https://points.moi.technology. https required; a wrong value breaks sign-in and the health origin | The site's own address |
| GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET | Google sign-in. The redirect must match BETTER_AUTH_URL; Google rejects a raw address | Google Cloud console, APIs and Services, Credentials |
| X_CLIENT_ID, X_CLIENT_SECRET, X_TARGET_URL | The X task and campaigns. X_TARGET_URL is the profile members must follow | developer.x.com, the app |
| DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET, DISCORD_BOT_TOKEN, DISCORD_GUILD_ID, DISCORD_INVITE_URL | The Discord task | Discord developer portal |
| TELEGRAM_BOT_TOKEN, TELEGRAM_BOT_USERNAME, TELEGRAM_CHAT_ID, TELEGRAM_INVITE_MODE, TELEGRAM_WEBHOOK_SECRET | The Telegram task. Set the webhook again after a change | BotFather and the group; the secret with openssl rand -hex 32 |
| MOI_NETWORK, REOWN_PROJECT_ID | Wallet linking. devnet is the only network the code accepts | Reown dashboard, the project |
| MOI_RPC_URL | Chain reads for dev challenges and bounties. Not passed by the deploy on feature/ci-cd today; the bounty branch adds it to deploy.yml | The devnet RPC address |
| RESEND_API_KEY, EMAIL_FROM | Sign-in emails. Both, or none is sent | resend.com, API keys; the sender MOI Points <no-reply@moi.technology> |
| CRON_SECRET | The maintenance job | Generate with: openssl rand -hex 32 |
| ADMIN_EMAILS | Who gets the admin pages | Comma-separated emails |
| VERIFICATION_WINDOW_MINUTES, VERIFICATION_LIMIT_PER_USER, VERIFICATION_LIMIT_PER_IP, SOCIAL_AUDIT_BATCH_SIZE | Plain numbers for the attempt limits and the audit batch | Defaults 10, 6, 30, 50 |
| GHCR_PAT, TELEPORT_PROXY, TELEPORT_JOIN_TOKEN, VM_HOST, VM_USER | Deploy access | DevOps |
| X_TOKEN_ENCRYPTION_KEY, X_TOKEN_ENCRYPTION_KEY_PREVIOUS, CLIENT_IP_HEADER, DATABASE_SSL, PG_POOL_MAX, NEXT_PUBLIC_SITE_URL, FAUCET_URL, FAUCET_API_KEY, FAUCET_TOKEN_ADDRESS, FAUCET_VERIFY_MODE | In the template, read by the code, passed by nothing. With CLIENT_IP_HEADER unset the per-address limit does nothing | Leave unset until wired |

The full list with comments is .env.example in the repo.

## Process

**Shipping a change**

- Branch from feature/ci-cd, not main.
- Run pnpm run ci myself: lint with zero warnings, typecheck, tests, migration check. No check runs on a PR.
- If the change adds a migration or enables a task, do the database or settings steps below first. The merge is the deploy and the new build refuses to start on an older database.
- Open one PR against feature/ci-cd. Review tweaks go on the same branch, not a PR each.
- Merge. This builds the image and replaces the running container: production changes now.
- Wait for the run, then read /api/health: healthy true, applied equals expected, origin https://points.moi.technology. Sign in and open the page that changed.
- A redeploy without a code change: Actions, "MOI Project CI/CD", Run workflow, branch feature/ci-cd.

**Running an X like campaign**

- Write the brief: title, description, points, and the post links (https://x.com/<account>/status/<id>, up to five). Check the posts are live.
- Sign in with an admin account, open /admin, X campaign control, Create draft.
- Read it back. Only a draft can be edited.
- Publish. The previous live campaign closes by itself.
- Check as a member with a verified X connection: the campaign shows on the dashboard. It does not appear in /api/tasks, which lists only the fixed tasks.
- Close it when it is over.

**Running a webinar bounty** (once the bounty branch is merged)

- Before the session, if the bounty is on-chain: deploy a logic for the session on devnet and keep its id.
- Sign in with an admin account and open /admin, Webinar bounties.
- Fill the composer: title, description, points (1 to 10,000), session number, brief link, an optional deadline, and how it is verified. For on-chain, the logic id. Create bounty. It starts closed.
- When the session ends, press Open. Members see it on their dashboard. Opening an on-chain bounty first checks that the node answers, so a node that cannot answer is reported to you now, not to every member later.
- Announce it (moi-webinar skill) with the brief link.
- Review bounties: proofs appear under Waiting for review with the member's name, email, linked wallet, link, hash, note and what the chain said about the hash. Approve awards the points at once. Reject needs a reason. You cannot approve your own submission. If the member sent a new proof after your page loaded, the action is refused and the page reloads.
- On-chain bounties award by themselves and need no review.
- When it is over, press Close. A bounty with proofs waiting cannot be closed, so review them first.
- Rules: points, verification type and logic id cannot change while the bounty is open or once a proof is waiting or approved. Title, description, brief link, deadline and session can change at any time. The deadline stops new submissions only. Approving needs the bounty open, so to approve a late proof re-open it first. Approving is permanent for the member's ledger.
- The same can be done from the browser console with the admin API (documented in the README on the branch). There are no API tokens; the admin's session cookie protects every route.

**Switching a task on or off, or changing its points**

- Check that every setting the task needs is in deploy.yml and set in GitHub. Enabling a task whose settings are not passed stops the container.
- On or off: flip enabled in config/reward-tasks.ts and ship it.
- New points value: a hand-written migration that updates the tasks row, and the same number in TASK_POINTS. The database decides what is awarded.
- Ship in the database-first order below.
- Read /api/tasks: the new state shows.

**Changing a setting or a secret**

- Check the name is listed in deploy.yml. If not, a PR that adds the line comes first.
- Set it in GitHub with gh secret set or gh variable set, typing the value at the hidden prompt.
- Run the deploy workflow by hand. Setting a value deploys nothing on its own.
- Read /api/health, then sign in and use the one feature the setting controls.
- Every provider callback (Google, Discord, X, the Telegram webhook) must match BETTER_AUTH_URL.

**Changing the database**

- Write the migration by hand in drizzle/, statements separated by the breakpoint line, and add the journal entry. Never run drizzle-kit generate or push: the snapshots stop at 0003 and a generated diff would recreate objects that exist.
- Edit lib/db/schema.ts to match. pnpm check:migrations must print ok.
- Try it on a local database only. Never put the production DATABASE_URL in .env.local.
- Ask DevOps to apply it to production first (node scripts/migrate.mjs with the production DATABASE_URL, from a checkout of the branch). /api/health then shows applied one above expected, which is allowed.
- Merge the code that needs it. Health shows applied equals expected.
- A migration is one transaction: a failing statement rolls the whole batch back. The database has no backups, so take a copy before a risky change.

**After a devnet reset**

- Members need a fresh account on the new chain before they can link a wallet; linked wallets stay bound, and only an admin erase clears one.
- A moved RPC address is a PR on config/moi-networks.ts (and the MOI_RPC_URL variable).
- Any on-chain bounty or challenge that points at a wiped logic is closed or re-created with the new id.

**Checking it is healthy**

- curl -s https://points.moi.technology/api/health: healthy true, database ok, migrations applied equals expected, origin https://points.moi.technology, the four enabled tasks. On 7 October: applied 11 of 11, healthy. The sha is null, so the JSON cannot tell you which build runs.
- curl -s https://points.moi.technology/api/tasks lists the same four tasks with their points.
- The leaderboard loads. The home page sends an anonymous visitor to /login.
- Sign in and press one verify button.

**When something is wrong**

- database error in health: the database is unreachable or the login changed. The Supabase owner.
- applied below expected: a build ahead of the database. Apply the migration (DevOps) now.
- No answer at all: the container is down or crash-looping at startup, usually a missing task setting or a wrong BETTER_AUTH_URL. Ask DevOps for the container log.
- Sign-in loops or the health origin is wrong: BETTER_AUTH_URL.
- A member's verify fails for everyone on one provider: that provider's app or callback. Check the provider console.
- Do not redeploy to see if it helps until the cause is known: a redeploy replaces the container again.
- Rollback: none. Revert in a new PR and merge.

## Claude skill

The **moi-web-products-ops** skill covers the Points Program with its points runbooks: tasks and campaigns, shipping, settings and database, health. The bounty announcement and the proof form for a session are in the **moi-webinar** skill.

| When | What to tell Claude | What the skill does |
|---|---|---|
| Something looks wrong | "Is Points healthy?" | Reads the health route, the task list and the public pages, and names the known faults. |
| Shipping | "Ship this Points change." | Walks the branch from feature/ci-cd, pnpm run ci and the PR, and says that merging deploys production. |
| A campaign | "Set up an X like campaign for these posts." | Writes the brief and the steps. The admin clicks are mine. |
| A bounty | "Create the bounty for session N." | Writes the brief, the composer values and the announcement. I create and open it. |
| A task | "Switch the faucet task on." | Checks the settings it needs, writes the config change and the migration if points change. |
| A setting | "I need to change this Points setting: ..." | Says whether deploy.yml passes it, where it is set and that a workflow run follows. It never sees a value. |
| The database | "I need a migration for ..." | Writes the SQL and the journal entry, and gives DevOps the apply-first steps. |

What the skill never does without my yes: push, merge (a merge deploys production), run the workflow, change a secret, run SQL against production, or touch the admin page.

## Open items

- Ship the webinar bounties: PR #22 (branch feature/admin-bounties, 7 commits, 190 tests passing, no migration) is open against feature/ci-cd since 8 October. Merging deploys. Then set MOI_RPC_URL as an Actions variable once the devnet host is confirmed to serve the interaction methods, redeploy, and run one on-chain bounty as a dry run with my own hashes: one that calls the logic, one that reverted, one sent by someone else. The chain reader has not been proven live. The checklist is in the PR.
- Put the Supabase project on a paid plan with backups. Then drop the schema backup.tasks_before_0008.
- Decide the open PRs: #21 (emails, leaderboard avatars, wallet keys, X likes cap, no nightly audit; clean to merge, no migration), #15 (CI/CD hardening, draft, conflicts with the tip: rebuild or close), #1 (Upendhar's first CI/CD, base feat/dev-challenges: retarget or close). Close sarvalabs/Points-Program #1 if that repo is unused.
- Nothing is known to call the maintenance job. Ask Upendhar what calls it and who schedules the new one from #21.
- Session 8's challenge is deployed but off. Open it (MOI_RPC_URL, one real submission, the flag) or drop it.
- Move every secret into a shared vault. A secret was exposed in an old build record in September and accepted on 15 September; delete those records and rotate before a real launch or if repo access widens.
- The deploy logs in to the box as root and the container port answered over http from outside on 4 October. #15 fixes both after DevOps setup; confirm the firewall meanwhile.
- Pass X_TOKEN_ENCRYPTION_KEY (read lib/x-credentials.ts first), CLIENT_IP_HEADER (nginx must set it) and GIT_SHA from the deploy.
- Match the Dockerfile's pnpm version to package.json.
- Test a wallet link. The devnet RPC certificate expired on 4 October and was renewed by 5 October; the server reads wallet keys from that host.
- main is stale since August and nothing deploys from it. Merge feature/ci-cd into main and deploy from main.
- Retire the old Vercel project.
- Put an operator guide in the repo. The bounty section in the branch's README is a start.
