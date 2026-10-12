# Architecture: what runs where, and how a merge becomes a container

Facts are as of 2026-10-03. Sources: the workflow files, `Dockerfile`, `docker-compose.yml` and code on `origin/master` of `sarvalabs/moi-agent-launchpad` (private), read from the previous operator's clone, which is shallow and was last fetched on 2026-10-01, so its newest merge is PR #30 of 2026-09-15 and anything newer is not seen; the research notes; `DEPENDENCIES.md` (the previous operator's handover file, local to his machine and not in git; ASK: Adithya for a copy); and read-only requests to the live site on 2026-10-03. Where a repo document disagrees with a workflow file, the workflow file wins. Back to `../SKILL.md`.

## The product
A no-code platform for personal agents on MOI devnet. A participant connects the MOI Wallet extension (desktop only; phone sign-in is on an unmerged branch), picks a template, signs one on-chain registration, then runs the agent on their own machine from a downloaded bundle. Messages reach them through the Telegram bot `moinetworkbot`. A marketplace lists public agents; paid agents use the AgentMarket contract. Production is https://launchpad.moi.technology. Say "devnet", not "Voyage devnet". The old host moi-agent-launchpad.vercel.app answered 404 on 2026-10-03. <!-- slop-lint:ignore -->

## What runs where
| Part | Where | What it does | Who can change it |
|---|---|---|---|
| Web app | A Docker container on a DevOps VM (its name, folder and port: ASK: Upendhar). Image `ghcr.io/sarvalabs/moi-agent-launchpad`, command `npm start`, `restart: unless-stopped`. Next.js 14, Node 22 | Pages, 36 API route files under `app/api`, the Telegram webhook, the relay, an in-app cleanup timer | Code: a PR to `master`. The box: DevOps only |
| Proxy and certificate | nginx and a Let's Encrypt certificate on the VM. Not in git. The port map is private: ASK: Upendhar | Terminates TLS, proxies to the container | DevOps only |
| Database | Supabase Postgres, the project named by the `SUPABASE_URL` variable. Reached only by server routes with the service-role key. Row-level security is on with no policies | Users, agents, runs, relay messages, subscriptions | Whoever holds the project login. Unknown: ASK: Adithya, Rahul |
| Agent runtime | `public/runtime.cjs`, a bundle built from `agent-runtime/` and `lib/templates/`. Runs under pm2 on each user's own computer | Polls `/api/relay/inbox`, answers through `/api/relay/deliver`, reports to `/api/relay/run-report`, signs every relay call | The user. The code of an installed copy never updates itself: it warns in its log when its bundle is out of date and prints a one-line update (fetch `runtime.cjs` from the site, then `pm2 restart`). Settings edits do reach a running copy (config sync, migration 0011, about 30 seconds); a copy installed before config sync (2026-08-02) needs one re-download first |
| Telegram bot | `moinetworkbot`, webhook at `/api/telegram/webhook`, secret in the header `x-telegram-bot-api-secret-token` | Links a chat to a profile, routes direct messages to the owner's focused agent | The BotFather owner: Adithya (ASK) |
| Chain | MOI devnet, read through `VoyageProvider("devnet")` unless `MOI_RPC_URL` is a URL without "voyage" or "devnet" in it | Registry reads and writes, wallet activation, market reads | The protocol team resets it (ASK: Gokul) |
Not running, on purpose: the worker (`npm run worker` would delete the Telegram webhook and re-run every agent on the server), a crontab (the cleanup runs inside the app; `DEPENDENCIES.md` (the previous operator's file, local to his machine; ASK: Adithya for a copy) says nothing runs from a crontab, but nobody has looked on the VM, because check 4.4 has no result), Vercel. <!-- slop-lint:ignore -->

## What talks to what
```
browser + MOI Wallet extension -> nginx -> web container -> Supabase (service-role key)
                                                        -> devnet RPC (registry, registration, market)
Telegram -> /api/telegram/webhook -> web container -> inbound_messages (DB)
agent runtime on the user's computer -> GET /api/relay/inbox (holds up to 20 s) -> reply -> /api/relay/deliver -> Telegram
```
`INBOX_WAIT_MS=20000` is written by `deploy.yml`, and the post-cutover checklist (check 2.2) warns that an nginx read timeout shorter than that cuts the poll. Whether it does was never recorded: the check has no result.

## From merge to a running container
| # | Step | File | What happens |
|---|---|---|---|
| 1 | Trigger | `.github/workflows/ci-cd.yml`, "MOI Agent Launchpad CI/CD" | A push to `master` or to `feature/moi-agent-launchpad-cicd`, or a manual run (`workflow_dispatch`, any branch chosen) |
| 2 | Build | `docker-build.yml` | Tag is `git rev-parse --short HEAD`. Login to `ghcr.io` with `GHCR_PAT`. `docker build` with three build args from variables: `NEXT_PUBLIC_APP_URL`, `NEXT_PUBLIC_MOI_EXPLORER_URL`, `NEXT_PUBLIC_WALLET_INSTALL_URL`. Pushes `:latest` and `:<sha>` |
| 3 | Image | `Dockerfile` | `npm ci` (strict), a guard that fails the build unless `NEXT_PUBLIC_APP_URL` starts with `https://`, then `npm run build` (this is the only compile check CI runs) |
| 4 | Deploy | `deploy.yml`, job `deploy`; `ci-cd.yml` runs it with `needs: build` | Teleport machine-ID login, then over `tsh`: make the folder, copy `docker-compose.yml`, write `.env` (mode 600) from Actions secrets and variables, `docker login ghcr.io`, `docker compose pull`, `docker compose up -d --remove-orphans`, `docker image prune -af`, `docker compose ps` |
| 5 | Boot | the container | `[cleanup] scheduled, first sweep in 60s, then every 6h` is the boot line. `/api/stats` says `pending` for about a minute |
About 4 minutes end to end (3.6 to 4.0 minutes on 2026-09-14 and 2026-09-15, from the research). Not in the pipeline, as of the workflow files read: no test, no typecheck, no lint, no health check after the deploy, no rollback, no alert on failure, no `concurrency` setting (two close merges can run two deploys at once; the outcome is untested), no protected environment. A red run leaves the old container serving and no alert is wired up (a failed-run email from GitHub depends on each person's notification settings and is not on record). The trigger has no path filter, so a docs-only merge to `master` deploys too.

## The chain side (a devnet reset wipes all of it)
| Part | Setting | State as of 2026-10-03 |
|---|---|---|
| Agent registry | Variable `MOI_AGENT_REGISTRY_LOGIC_ID`; empty means the default in `lib/moi/registry.ts`, `2f3e9469` since PR #29 (2026-09-15). The npm package `js-moi-agent-registry` embeds a dead address and reads the variable once at load | Live reads work (chainStatus ok). Counts are unstable, see `health.md` |
| AgentMarket contract | `MOI_AGENT_MARKET_LOGIC_ID`, which `deploy.yml` does not write. The code default is the pre-wipe id | `lib/payments.ts` says it did not survive the 2026-08-15 wipe and a redeploy on 2026-08-18 reverted. The listing read returned `onchain: null` on 2026-10-03. Whether it was redeployed after 2026-09-11 is unknown: ASK: Adithya |
| Payments switch | `NEXT_PUBLIC_PAYMENTS_ENABLED`, on only when exactly `1` at image build. No workflow, Dockerfile or env example on master sets it | By the code, paid routes answer `payments_disabled` in production. Inferred, not tested live. `docs/HANDOFF.md` section 1b says the opposite and is stale |
| Registration wallets | `MOI_REGISTRATION_MNEMONIC_1`, `_2`, `_3`, held by DevOps | Funded wallets that create and fund new users. Wiped by each reset |
| Constants | SDK names `KMOI_ASSET_ID`, `DEFAULT_FUEL_PRICE`. Never a literal | `tests/chain-constants.test.ts` fails on a retired asset id or a fuel price under the floor |
| Platform wallet | `MOI_PLATFORM_MNEMONIC` | Its role is described three ways (README: optional, `.env.example`: required, the previous operator's local `HANDOVER.md`: reads the registry and runs the heartbeat; ASK: Adithya for a copy). ASK: Adithya |

## Jobs inside the app
- Cleanup: `instrumentation.ts` removes expired nonces and claimed inbound messages 60 seconds after boot and every 6 hours. `GET /api/cron/cleanup` with `Authorization: Bearer <CRON_SECRET>` runs it by hand; without the header it answers 401, and 503 `cron_secret_unset` means the secret is missing.
- Spend kill switch: `platform_state` holds one row per UTC day with `killed`. When platform spend crosses `GLOBAL_DAILY_SPEND_CAP_CENTS` (500 in the research) the row flips, internal model calls stop and an admin Telegram alert goes out; the alert text says "until UTC midnight". Users run on their own model key, so only internal paths feel it.
- Admin alerts go to `ADMIN_ALERT_TELEGRAM_CHAT_ID`: the kill switch, and all registration wallets missing (once per hour per process). Nobody else is told of anything.

## Where each file is (read on 2026-10-03 with read-only git from a clone last fetched on 2026-10-01)
| On GitHub `master` | Only on a branch or open PR | Only on the previous operator's machine (ASK: Adithya for a copy) |
|---|---|---|
| The three workflows, `Dockerfile`, `docker-compose.yml`, 12 migrations, `scripts/` (three files), `probe-registry.mjs`, `docs/HANDOFF.md`, `POST-CUTOVER-CHECKLIST.md`, `E2E-TESTING.md`, `QA-LEDGER.md`, `REGISTRY-C684F926-CUTOVER.md`, `tests/` | Phone sign-in branch `walletconnect-qr-signin`: per `DEPENDENCIES.md` (2026-10-01) 3 commits not in master, its only PR is #2 on the previous operator's fork, and the clone read here does not hold the branch. PR #10 (market deploy budget) and PR #31 (docs links) were open as of 2026-10-01 per the same file | Uncommitted corrections to `README.md`, `DEPLOY.md`, `docs/HANDOFF.md`, `.env.example`, `.env.production.example` (branch `local/sweep-oct1`). A second clone (branch `fix-agentmarket-storage-fund`) with five modified contract files and an untracked progress note, for PR #10. `DEPENDENCIES.md` also lists untracked `app/labs`, `app/api/labs` and four scripts; they were not in the clone read on 2026-10-03, so whether they still exist is open (ASK: Adithya) |

## Documents that are wrong on master (trust the workflow, then the code, then prose)
README "Deploy" and its line "Marketplace payments are always on", and `DEPLOY.md` (Vercel plus a worker; do not follow). README also names a connect-page button ("New wallet? Activate it on-chain first") that the page on `master` does not have: it auto-detects a new wallet (`support.md` has the current wording). `docs/HANDOFF.md` opening (production on the vercel.app host, push to `master` by hand), section 1b (payments always on) and section 3 (grant default 100000 KMOI; the code default is 10 KMOI). `POST-CUTOVER-CHECKLIST.md` check 4.4 (a crontab entry that does not exist) and its target. `E2E-TESTING.md` header and check 0.1 (name the vercel.app host and Vercel env). `how-it-works.md` (a shared model tier retired on 2026-08-02). <!-- slop-lint:ignore -->

## Who owns what (ASK lines are open)
| Question | Answer |
|---|---|
| Does DevRel own the Launchpad? | Not settled. ASK: Rahul |
| Who built it | Adithya wrote 301 of 338 commits per `DEPENDENCIES.md`. History questions: ASK: Adithya |
| Who acts on the VM, DNS, TLS, GHCR | DevOps. Upendhar holds Teleport, VMs, nginx, DNS, `GHCR_PAT`. Srikar wrote earlier workflows. Which of the two owns this VM today is unknown. ASK: Upendhar |
| Who may merge to `master` | Unknown whether branch protection or a required review exists. ASK: Rahul |
| Chain and registry facts | Gokul |
| Support channel | The dashboard sends unknowns to a Discord invite link. No monitored channel is on record. ASK: Rahul |

## Not yet known
- Whether the VM comes back unattended after a reboot, whether the certificate renews (checks 4.3, 4.6, 4.7 were never filled in), container memory after 24 hours. ASK: Upendhar.
- Branch protection on `master`; who gets a failed-run email. ASK: Rahul.
- Whether any uptime monitor or log retention exists. ASK: Upendhar.
- Who is on call for the VM and how to reach them out of hours. No response time or rota is on record. ASK: Rahul, Upendhar.
