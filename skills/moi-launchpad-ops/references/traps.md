# Traps: failures that give no error

Facts are as of 2026-10-03. Each row is a rule with the incident or the code behind it. Dates are from commits, the code and the research. Back to `../SKILL.md`.

## Deploy and pipeline
| # | Rule | Why |
|---|---|---|
| 1 | A merge to `master` is a production deploy and CI runs no test. Read the diff as if it ships in 4 minutes | The only compile check is `next build` inside the Docker build. Docs-only merges deploy too |
| 2 | A red deploy run alerts nobody and production keeps the old image. Look at `gh run list` after every merge | Runs after PR #24 failed in under a minute at `npm ci` on 2026-09-14 and production served the older image (e640338) |
| 3 | Only a push to `master` or to `feature/moi-agent-launchpad-cicd` deploys. A fork or any other branch does not | `ci-cd.yml` triggers. Never push to the second branch by accident |
| 4 | A manual run of the workflow deploys whichever ref you pick as `:latest` | `workflow_dispatch` on `ci-cd.yml`; the build tags the picked commit |
| 5 | `deploy.yml` rewrites the whole `.env` from a fixed list on every run. A name not listed never arrives, and an unset variable is written as empty | The code treats an empty registry id as unset (942827a). `MOI_AGENT_MARKET_LOGIC_ID`, `DAILY_INTERACTION_CAP`, `MAX_AGENTS_PER_USER`, `GEMINI_API_KEY` and `OPENAI_API_KEY` are read by code and not written |
| 6 | `NEXT_PUBLIC_*` values are fixed when the image is built. A restart changes nothing | The `Dockerfile` ARGs. The build fails unless `NEXT_PUBLIC_APP_URL` starts with `https://` |
| 7 | `NEXT_PUBLIC_APP_URL` is permanent in every on-chain card and every downloaded setup script | A wrong value cannot be undone per agent: stop and roll back |
| 8 | `/api/stats` must keep `export const dynamic = "force-dynamic"` | Losing it broke the Docker build once (c69470f) |
| 9 | Prove a lockfile change with `rm -rf node_modules && npm ci`, not `npm install` | A lenient install hid an ERESOLVE (e640338) |
| 10 | The deploy runs `docker image prune -af` and copies the repo's `docker-compose.yml` over the VM's | A manual image pin on the VM lasts until the next deploy, and the old image must be pulled again |
| 11 | Do not run the worker in production | `npm run worker` long-polls Telegram, which deletes the webhook, and would re-run every agent twice (compose comment) |
| 12 | Nobody verified that nginx allows a 20 second poll, that the VM returns after a reboot, or that the certificate renews | Post-cutover checks 2.2, 4.3, 4.6 and 4.7 have no result |

## Secrets and settings
| # | Rule | Why |
|---|---|---|
| 13 | `AGENT_KEY_ENCRYPTION_SECRET` is never rotated and no vault holds it | A different value makes every stored agent key unreadable for good. On 2026-08-03 the VM started with a new one and earlier agents broke |
| 14 | GitHub secrets are write-only. The VM `.env` is the only readable copy | A secret nobody holds elsewhere cannot be recovered |
| 15 | Rotating `TELEGRAM_WEBHOOK_SECRET` without re-running `setWebhook` stops all delivery with no error | The exact command is in no repo file |
| 16 | `getWebhookInfo` output can include the server's IP address. Filter it before pasting anything | `settings-and-secrets.md` gives the filter |
| 17 | `MOI_RPC_URL` is ignored when it contains "voyage" or "devnet" | `provider()` in `lib/moi/registry.ts` falls back to the SDK's devnet endpoint. The documented example host did not answer |
| 18 | Never open any `.env` file and never treat a local one as production | A local copy points at a local database and a mock mode (`docs/HANDOFF.md`) |
| 19 | A recovery phrase is the operator's to type, at a hidden prompt, never in chat or a file | A deployer phrase pasted in chat once is to be treated as exposed (`docs/HANDOFF.md` section 5) |

## Chain and data
| # | Rule | Why |
|---|---|---|
| 20 | Success is the receipt, not the broadcast. A simulation can pass what the chain later rejects | Activation said "ready" while the chain reverted it: grant under the 1 KMOI floor, callsite `Transfer!` instead of `Transfer`, HTTP 200 on a revert. Introduced by PR #28, fixed by PR #30 on 2026-09-15 (a02eb26; the commit gives no duration) |
| 21 | The registration script's default grant (0.5 KMOI) is under the floor and it counts a visible account as success | Set `MOI_REGISTRATION_GRANT` to at least 1 KMOI and read the receipt |
| 22 | Chain constants come from the SDK, never from a literal | v0.13.0 moved the KMOI asset id and raised the default storage fund 10,000 times. `tests/chain-constants.test.ts` enforces it |
| 23 | The wrong derivation path gives "account not found" on a funded wallet | Faucet wallets use `m/44'/6174'/7020'/0/0`, SDK-only wallets `m/44'/6174'/0'/0/N`, the Launchpad registration default is `m/44'/6174'/1'/0/0` |
| 24 | `js-moi-agent-registry` embeds a dead registry address and reads the variable once at load. npm "latest" follows publish time, not the version number | A bumped package may carry the wrong address (comment in `lib/moi/registry.ts`) |
| 25 | `probe-registry.mjs` and `_map.mjs` carry pre-reset ids and wallets | Set the id and the caller explicitly before trusting a probe |
| 26 | The default marketplace listing is a database index. `?source=chain` reads the chain | After the 2026-09-11 reset the database listing kept showing agents as on-chain. A forced chain read now says `chain_unreachable` instead |
| 27 | `onchain: null` on a listing means the read is unavailable, not that the agent is unlisted | Route comment in `app/api/marketplace/[address]/listing/route.ts` |
| 28 | Chain figures swing between reads. Quote none without the read time | On 2026-10-03 `registered` read 0 then 6 and `?source=chain` listed 8, 4, 0 and 7 agents with `chainStatus` ok |
| 29 | Never delete agent rows to repair a reset | MOI re-imported an old snapshot (144 agents; 1 of 11 listed agents carried over). Owners re-register |
| 30 | The dashboard banners and storage keys name the 2026-08-15 and 2026-08-19 events | Edit them for the next reset or dismissed notices hide the new one |
| 31 | The wallet's active account differs from the signed-in account: the most common confusing failure | Log out and reconnect |
| 32 | The code of an installed agent never updates itself; its settings do | The log of an out-of-date copy prints an update line (fetch `runtime.cjs`, `pm2 restart`), or the owner downloads a new setup script. Settings edits sync in about 30 seconds (migration 0011) once the copy has been re-downloaded after 2026-08-02. Scripts made on the old Vercel host fail with a 404 | <!-- slop-lint:ignore -->

## Migrations and documents
| # | Rule | Why |
|---|---|---|
| 33 | Migrations are applied by hand, have no tracking table, and 0001 to 0005, 0007 and 0008 are not safe to run twice | `database.md`. 0008 rewrites agent names on its first run |
| 34 | Payments are probably off in production, whatever `docs/HANDOFF.md` section 1b says | `lib/payments.ts` defaults off, and nothing in the deploy sets `NEXT_PUBLIC_PAYMENTS_ENABLED`. Inferred, not tested live |
| 35 | Read the workflow, then the code, then prose. Several documents are wrong | `architecture.md` lists them |
| 36 | Work exists only on the previous operator's machine: doc corrections, a second clone for PR #10, an unreviewed `app/labs`, the phone sign-in branch's missing org PR | ASK: Adithya for a copy before anyone assumes it is lost or done |
| 37 | Three products pin the registry id separately and drifted by up to 12 days after the 2026-09-11 reset | Launchpad 2026-09-15, Explorer 2026-09-22, MCP 2026-09-23. `moi-devnet-reset` |
