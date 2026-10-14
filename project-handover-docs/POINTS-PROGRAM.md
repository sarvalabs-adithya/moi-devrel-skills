# Points Program

**Status: active.** Live at points.moi.technology with four tasks on: join X (verified), join Discord, join Telegram, create wallet. Inactive: the faucet task, the deploy-agent task, and session 8's dev challenge (deployed, switched off). Webinar bounties are live (PR #22, deployed 13 October), tested end to end with a test bounty on 14 October; no real webinar bounty yet.

Video: webinar bounties walkthrough (create, open, submit, award, close) https://drive.google.com/file/d/1MOs61CECZt6SRQhH9Zro0t2avq0-XPsy/view (recorded 14 October 2026).

Marketing: How it works (What a member sees, Tasks, X like campaigns, Webinar bounties, Admin), Process (Running an X like campaign, Running a webinar bounty), Claude skill, Open items. Developers: How it works, Stack, Variables, Env vars, Process, Claude skill, Open items.

MOI Community Points. Members sign in with Google, link their X, Discord and Telegram accounts and a MOI wallet, complete tasks to earn points, and see where they stand on a public leaderboard. Admins run X like campaigns and webinar bounties from an admin page. The Points team built the app (Harsh Gupta wrote the first version, Upendhar the CI/CD). The webinar bounties (PR #22) are the only functional change DevRel (Adithya) made to the app; PR #23 was review fixes to existing code, with no new behaviour. Questions about anything other than the webinar bounties go to the Points team: connect with Piyush. DevOps (Upendhar) owns the box it runs on.

## How it works

**What a member sees**

- Sign in with Google, the only login. A sign-in email goes out through **Resend** (an email-sending service) when both email names are set.
- The dashboard shows the task board. Each task is a card with its points and a button that verifies it.
- Join X: an X sign-in, then the app checks the member follows the account in X_TARGET_URL. The X connection stays linked and is what campaigns use later.
- Join Discord: a Discord sign-in, then the bot checks the member is in the guild.
- Join Telegram: the member joins the group through the bot (invite mode join_request or direct), and the bot's webhook confirms it.
- Create wallet: the member links a MOI wallet through **Reown** (the WalletConnect service that connects wallets to apps). The server reads the wallet's keys from the **devnet** (MOI's test network) RPC and accepts any active key.
- Points land in a ledger the moment a task is verified. The leaderboard and the member's total both read from it.
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
- Members with a verified X connection see it on their dashboard and press Verify. The app reads their recent likes through the X API (capped at the 20 most recent likes, PR #23) and awards the points.
- Close ends it. A closed campaign cannot be republished.

**Webinar bounties (PR #22)**

The only functional change DevRel made to the app: Adithya built this feature; everything else is the Points team's.

Every **Builders session** (MOI's live-build webinar for developers) can end with a bounty: something attendees do for points. The host creates it on the Points site, with no code change and no deploy. A bounty is a small form: one to six fields, each an **interaction hash** (the ID of a transaction on MOI), a link, a number or a line of text, required or optional, and each worth its own points; the bounty's points are the sum. Members with a linked wallet fill it in, the answers wait in a queue, and the host grades them by hand, ticking the answers that earn their points. For example, "100 for the interaction, 100 for a demo video, 100 for the write-up" is three fields with the video optional: a member can earn up to 300 and must send the interaction. Nothing is awarded automatically.

- It is a tasks row with the id bounty:<uuid>, its settings (session, brief link, deadline, fields) in the row's metadata, and each member's answers in an ordinary task completion. No new table, no migration.
- The fields and their points are locked while the bounty is open and once a submission is waiting or approved. Title, description, brief link, deadline and session can change any time.
- When the server has MOI_RPC_URL, a hash answer is checked against the chain (did the member's wallet send it, did it succeed) and the result is shown to the host as advice. It is not set on production as of 13 October, so that note is off. A hash another bounty already holds is flagged. Neither blocks the submission; the host decides.
- Approve pays the ticked answers' points at once through the same path as every task, so a member is paid once per bounty. Required answers are always ticked (a wrong one means Reject); untick an optional answer to leave its points out. Reject needs a reason the member sees, and the member can send new answers. Approving records what was accepted. It drops the text answers from the record and keeps the hashes, links and numbers as the evidence.

Members see open bounties on their dashboard under Webinar bounties, one box per field.

**Admin**

- An admin is an email in ADMIN_EMAILS (once Google has verified it) or a row in the admin_users table. On 13 October the admin_users table was empty, so access comes only from ADMIN_EMAILS. Since 14 October the admins are sarvalabsdeveloper@gmail.com (the shared company developer login), points@moinetwork.io (the Points account, managed by Sai Kiran) and Harsh Gupta's personal Gmail. Add the next DevRel's company Google email before the next bounty.
- To add an admin, append their Google email to the ADMIN_EMAILS Actions variable (keeping the existing ones), redeploy, then check the count. The change reaches the app only after the redeploy (about 4 minutes):

```bash
gh variable set ADMIN_EMAILS --repo sarvalabs/moi-project --body "$(gh variable get ADMIN_EMAILS --repo sarvalabs/moi-project),name@example.com"
```

```bash
gh workflow run ci-cd.yml --repo sarvalabs/moi-project --ref feature/ci-cd
```

```bash
gh variable get ADMIN_EMAILS --repo sarvalabs/moi-project | tr ',' '\n' | grep -c @
```

  To remove someone, set the variable to the full list without them (gh variable set ADMIN_EMAILS --repo sarvalabs/moi-project --body "a@x.com,b@y.com") and redeploy. The person signs out and in again after the redeploy.
- There is one admin role. An admin can run campaigns and bounties, erase a member and unlink a member's social accounts.
- Every admin action writes a row in admin_audit_events.
- A member without admin access who opens /admin is sent to the dashboard, by design.

**Why the database stays in the points@moinetwork.io Supabase account**

Launchpad and Dataroom moved into the company Supabase organisation on 8 October, but Points did not. The company organisation is on the free plan, which allows two active projects, and those two slots are taken. Moving Points would need the company organisation on a paid plan, which is Rahul's call. Until then the project stays in the points@moinetwork.io account, which Sai Kiran manages. The cost is that the free plan has no automatic backups. For access, ask Sai Kiran to add people (DevOps, Rahul) to that Supabase organisation so nothing depends on one login.

**The database rules** (drizzle/TRIGGERS.md; **Drizzle** is the database toolkit behind the schema and migrations)

- The points ledger is append-only. An award cannot be edited or deleted; a wrong points value only affects future awards.
- A verified completion can only move to rejected. The moves pending to verified, pending to rejected and rejected to pending are allowed.
- A linked social account cannot be reassigned to another member. A bound wallet cannot change except inside an erasure.
- Members with points are anonymised on erasure, never deleted. What a member sent to a bounty is cleared unless the proof was approved, because then it is the evidence for the points.

**How a deploy works**

- A push to feature/ci-cd (not main) runs the CI/CD workflow: build the Docker image, push it to **GHCR** (GitHub's container registry) as latest, log in to the box through **Teleport** (the secure access gateway to the box), rewrite the app's env file from the GitHub variables, hand the secrets straight to the container, remove the old container and start the new one.
- A deploy takes about 4 minutes. There is no staging and no rollback, because only latest is pushed.
- On start, in production, the app refuses to boot if the database has fewer migrations than the build, or if an enabled task is missing a setting. A merge that adds a migration or enables a task without its settings takes the site down until someone fixes it.
- No pull request runs any check, so whoever ships runs pnpm run ci (**pnpm** is the Node package manager; ci is lint, typecheck, tests and the migration check).
- The social audit job is gone (/api/jobs/social-audit answers 404). /api/jobs/maintenance, a purge-and-totals job, is live (401 without CRON_SECRET), but no scheduler calls it; confirm with Upendhar. PR #23 also removed point clawbacks.

## Stack

| Piece | What it is |
|---|---|
| Next.js 16 + React 19 + TypeScript + Tailwind 4, pnpm | The web app and every API route |
| Postgres on **Supabase** (hosted Postgres), through Drizzle | All state: members, linked accounts, tasks, completions, the points ledger, campaigns, audit events. 11 hand-written migrations |
| **Better Auth** (a sign-in library) | Google sign-in, the only login |
| X, Discord and Telegram APIs | Task verification and campaigns. The X API is the paid tier |
| Reown + **js-moi-signer** (MOI's JavaScript signer library) | Wallet linking. Keys are read from the devnet RPC |
| Resend | Sign-in emails from no-reply@moi.technology |
| Docker + GitHub Actions + GHCR + Teleport | Build and deploy to the DevOps box, one container behind **nginx** (the web server) |
| /api/health and /api/jobs/maintenance | The health route (database and migration state) and the maintenance job (live, not scheduled). The social audit job is gone |
| vitest | 23 test files on feature/ci-cd |

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Codebase | DevRel | sarvalabs/moi-project, private. The branch feature/ci-cd deploys, not main. Repo admins on 4 October: gokul, chandra, git, adithya, upendhar |
| Supabase project | points@moinetwork.io, managed by Sai Kiran | Free plan, no backups. It holds every member and every point. Kept in that account on purpose (see below) |
| Google OAuth client, X developer app (paid API), Discord app and bot, Telegram bot and group, Reown project, Resend account | sarvalabsdeveloper@gmail.com | Each provider's callback must match BETTER_AUTH_URL |
| The box, nginx, TLS, Teleport, DNS, the GHCR image | DevOps (Upendhar) | Container moi-project on host port 31000. preview.points.moi.technology is the same box |
| Devnet RPC address | Protocol team | Written in config/moi-networks.ts; a move is a PR |
| Who is an admin | DevRel, through ADMIN_EMAILS | The admin_users table is empty (13 October), so only the ADMIN_EMAILS Actions variable gives access |

## Env vars

The index across every product, with the consoles and who holds each login, is ENV-VARS.md.
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
| MOI_RPC_URL | Chain reads for dev challenges, and the advisory check on a bounty's hash answers. Bounties work without it. deploy.yml passes it (PR #22), but the Actions variable is not set (13 October), so the chain note beside hash answers is off | https://dev.voyage-rpc.moi.technology/devnet/ |
| RESEND_API_KEY, EMAIL_FROM | Sign-in emails. Both, or none is sent | resend.com, API keys; the sender MOI Points <no-reply@moi.technology> |
| CRON_SECRET | The maintenance job | Generate with: openssl rand -hex 32 |
| ADMIN_EMAILS | Who gets the admin pages | Comma-separated emails |
| VERIFICATION_WINDOW_MINUTES, VERIFICATION_LIMIT_PER_USER, VERIFICATION_LIMIT_PER_IP | Plain numbers for the attempt limits | Defaults 10, 6, 30 |
| GHCR_PAT, TELEPORT_PROXY, TELEPORT_JOIN_TOKEN, VM_HOST, VM_USER | Deploy access | DevOps |
| X_TOKEN_ENCRYPTION_KEY, X_TOKEN_ENCRYPTION_KEY_PREVIOUS, CLIENT_IP_HEADER, DATABASE_SSL, PG_POOL_MAX, NEXT_PUBLIC_SITE_URL, FAUCET_URL, FAUCET_API_KEY, FAUCET_TOKEN_ADDRESS, FAUCET_VERIFY_MODE | In the template, read by the code, passed by nothing. With CLIENT_IP_HEADER unset the per-address limit does nothing | Leave unset until wired |

The full list with comments is .env.example in the repo.

## Process

**Shipping a change**

- Branch from feature/ci-cd, not main.
- Run pnpm run ci: lint with zero warnings, typecheck, tests and the migration check. No check runs on a PR.
- If the change adds a migration or enables a task, do the database or settings steps below first. The merge is the deploy and the new build refuses to start on an older database.
- Open one PR against feature/ci-cd. Put review tweaks on the same branch, not in a PR each.
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

**Running a webinar bounty**

- Sign in with an admin account and open /admin, Webinar bounties.
- Fill the composer: title, description, session number, brief link, an optional deadline, and the fields under What members send. Each field has a label, a type (interaction hash, link, number, text), its points, a required box and optional help text; the total across the fields is the bounty's points, at most 10,000. Add field adds another, up to six. Create bounty. It starts closed.
- When the session ends, press Open and announce the brief link (moi-webinar skill). Members see the bounty on their dashboard.
- Grade: submissions appear under Waiting for review with the member's name, email, linked wallet and every answer under its field, each with an Accept tick showing its points. A hash answer shows what the chain said about it and whether another bounty already holds it. Untick an optional answer to leave its points out; Award pays the ticked answers' points at once; Reject needs a reason. You cannot approve your own submission. If the member sent new answers after your page loaded, the action is refused and the page reloads.
- When it is over, press Close. A bounty with submissions waiting cannot be closed, so review them first.
- Rules: the fields and their points cannot change while the bounty is open or once a submission is waiting or approved. Title, description, brief link, deadline and session can change at any time. The deadline stops new submissions only. Approving needs the bounty open, so to approve a late submission re-open it first. Approving is permanent for the member's ledger.
- The same can be done from the browser console with the admin API (documented in the moi-project README). There are no API tokens; the admin's session cookie protects every route.

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

- curl -s https://points.moi.technology/api/health: healthy true, database ok, migrations applied equals expected, origin https://points.moi.technology, the four enabled tasks. On 13 October: applied 11 of 11, healthy, the four tasks. The sha is null, so the JSON cannot tell you which build runs.
- curl -s https://points.moi.technology/api/tasks lists the same four tasks with their points.
- The leaderboard loads. The home page sends an anonymous visitor to /login.
- Sign in and press one verify button.

**When something is wrong**

- database error in health: the database is unreachable or the login changed. The Supabase owner.
- applied below expected: a build ahead of the database. Apply the migration (DevOps) now.
- No answer at all: the container is down or crash-looping at startup, usually a missing task setting or a wrong BETTER_AUTH_URL. Ask DevOps for the container log.
- Sign-in loops or the health origin is wrong: BETTER_AUTH_URL.
- A member's verify fails for everyone on one provider: that provider's app or callback. Check the provider console.
- Do not redeploy to see if it helps before you know the cause, because a redeploy replaces the container again.
- There is no rollback. Revert in a new PR and merge.

## Claude skill

The **moi-web-products-ops** skill covers the Points Program with its points runbooks: tasks and campaigns, shipping, settings and database, health. The bounty announcement and the proof form for a session are in the **moi-webinar** skill.

| When | What to tell Claude | What the skill does |
|---|---|---|
| Something looks wrong | "Is Points healthy?" | Reads the health route, the task list and the public pages, and names the known faults. |
| Shipping | "Ship this Points change." | Walks the branch from feature/ci-cd, pnpm run ci and the PR, and says that merging deploys production. |
| A campaign | "Set up an X like campaign for these posts." | Writes the brief and the steps. DevRel does the admin clicks. |
| A bounty | "Create the bounty for session N." | Writes the brief, the composer values and the announcement. DevRel creates and opens it. |
| A task | "Switch the faucet task on." | Checks the settings it needs, writes the config change and the migration if points change. |
| A setting | "I need to change this Points setting: ..." | Says whether deploy.yml passes it, where it is set and that a workflow run follows. It never sees a value. |
| The database | "I need a migration for ..." | Writes the SQL and the journal entry, and gives DevOps the apply-first steps. |

What the skill never does without DevRel's yes: push, merge (a merge deploys production), run the workflow, change a secret, run SQL against production, or touch the admin page.

## Open items

- Admin access (14 October 2026): adithya@moinetwork.io was removed from ADMIN_EMAILS, and sarvalabsdeveloper@gmail.com and points@moinetwork.io were added (redeployed the same day). So the admins are sarvalabsdeveloper@gmail.com (the shared company developer login), points@moinetwork.io (the Points account, managed by Sai Kiran) and Harsh Gupta's personal Gmail. Add the next DevRel person's company Google email before the next webinar bounty (commands under Admin), and ask the Points team (Piyush) whether the personal address should stay.

- Webinar bounties shipped: PR #22 merged and deployed on 13 October (the first deploy run failed on an expired GHCR_PAT; DevOps replaced the token and the re-run went through). Tested end to end on 14 October 2026: adithya@moinetwork.io was added to ADMIN_EMAILS (redeployed), and a test bounty "Test, ignore" (session 9, two 1-point fields) was created, opened, answered from a second account, awarded 2 points and closed; the 2 points were then reversed by hand with a -2 ledger entry (reason bounty_test_reversal) and the cached total corrected, so the test left no points behind. It stays in the admin list because awarded bounties cannot be deleted; closed bounties are hidden from members. adithya@moinetwork.io was taken out of ADMIN_EMAILS later the same day (first item above). Left to do: add each session host's Google email to ADMIN_EMAILS, and optionally set MOI_RPC_URL as an Actions variable and redeploy for the chain's note next to hash answers. The local branch feature/bounty-form is merged and can be deleted.
- Backups: either the company Supabase organisation moves to a paid plan and Points transfers into it, or the points@moinetwork.io account goes paid (Rahul decides). Until then there are no automatic backups. Only after a backup exists, drop the leftover table backup.tasks_before_0008.
- The review batch shipped as #23 and is live (#21 is closed). #15 is closed, replaced by draft #24 (CI/CD hardening) for Upendhar. #1 (Upendhar's first CI/CD, base feat/dev-challenges) is Upendhar's to close. The repo sarvalabs/Points-Program was archived on 13 October.
- Schedule the maintenance job (/api/jobs/maintenance, called with CRON_SECRET): nothing calls it. Ask Upendhar what runs on the box and who schedules it.
- Remove SOCIAL_AUDIT_BATCH_SIZE from deploy.yml and from the Actions variables: it is still set and passed, but nothing reads it.
- Session 8's challenge is deployed but off. Open it (MOI_RPC_URL, one real submission, the flag) or drop it.
- Move every secret into a shared vault. A secret was exposed in an old build record in September; the exposure was reviewed and the risk accepted on 15 September; delete those records and rotate before a real launch or if repo access widens.
- The deploy logs in to the box as root and the container port answered over http from outside on 4 October. Draft #24 fixes both after DevOps setup; confirm the firewall meanwhile.
- Pass X_TOKEN_ENCRYPTION_KEY (read lib/integrations/x-credentials.ts first; today the key falls back to BETTER_AUTH_SECRET), CLIENT_IP_HEADER (nginx must set it; without it the per-address limit is skipped) and GIT_SHA from the deploy.
- Match the Dockerfile's pnpm version to package.json.
- Test a wallet link. The devnet RPC certificate expired on 4 October and was renewed by 5 October; the server reads wallet keys from that host.
- main is stale since August and nothing deploys from it. Merge feature/ci-cd into main and deploy from main.
- Retire the old Vercel project.
- Put an operator guide in the repo. The bounty section in the README on feature/ci-cd is a start.
