# Keys by product: variable names

Names only. This file never holds a value, a length or a prefix. Shared accounts and keys, and the rules for handling them, are in `keys-and-access.md`. Facts are as of 2026-10-02 from `project-handover-docs/LIST-OF-DEPENDENCIES.md` (the 4 October snapshot), the ops research notes and the repos' `.env.example` files, updated from `project-handover-docs/ENV-VARS.md` (13 October 2026), with changes dated where a row says so. Status is TBD for every row. "ASK" has the meaning defined in `../SKILL.md`. For anything that sits on a VM: ASK: Upendhar. Back to `../SKILL.md`.

## Website and blog (`sarvalabs/MOI-Website`)
| Name | Unlocks | Used by | Lives in | Who grants | Status |
|---|---|---|---|---|---|
| `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` | Chat answers and embeddings | Express server, `npm run ingest` | Actions secrets | No company-owned key exists; the keys now set are not company keys (`ENV-VARS.md`). The chat stays hidden until company keys exist | TBD |
| `SUPABASE_URL`, `SUPABASE_KEY` | The Supabase project holding `documents` and `community_calls` | Server, ingest (needs a local `.env`) | Actions secrets | Not recorded (`project-handover-docs/MOI-WEBSITE.md`); ASK: Srikar | TBD |
| `ADMIN_API_KEY` | Calendar admin | Server | Actions secret | A repo admin creates it | TBD |
| `VITE_CHATBOT_API` | API base baked into the site bundle. Its live value points at the dev host | Vite build | Actions secret | ASK: Srikar | TBD |
| `ALLOWED_ORIGINS`, `PORT` | Server settings the workflow does not pass | Server on the VM | The VM (ASK: Srikar) | Srikar | TBD |
| `VITE_GA_ID`, `PUBLIC_GA_ID` | Nothing: the workflow passes them but no code on `main` reads them. Measurement runs through Google Tag Manager | None | Actions secrets | The GA4 property of the sarvalabsdeveloper@gmail.com account (`ENV-VARS.md`); leave as is | TBD |
| `DATA_ROOM_API_KEY`, `DATA_ROOM_CHAT_URL` | Nothing in production. `DATA_ROOM_API_KEY` is read only by `api/chat.js`, the old Vercel function (`git grep` on `main`, clone fetched 2026-09-11); `DATA_ROOM_CHAT_URL` only by the dev proxy and that function | None per the 2026-09-11 code read; `MOI-WEBSITE.md` (13 October) says the chatbot and the Express server use `DATA_ROOM_CHAT_URL`, so check with `git grep` before relying on either | Actions secret | Srikar | TBD <!-- slop-lint: ignore --> |
| `BUFFER_ACCESS_TOKEN`, `BUFFER_CHANNEL_X`, `BUFFER_CHANNEL_LINKEDIN` | Draft X and LinkedIn posts in Buffer | `distribute.yml` | Actions secrets | Buffer organisation owner creates an API token. Channel ids come from `npm run buffer:channels` | TBD |
| `DISCORD_WEBHOOK_URL` | Immediate post to Discord | `distribute.yml` | Actions secret | A Discord server admin (Integrations, Webhooks) | TBD |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | Immediate post to the Telegram channel. The bot must be channel admin | `distribute.yml` | Actions secrets | BotFather owner: the blog channel bot is under the sarvalabsdeveloper@gmail.com account (`ENV-VARS.md`) | TBD |
A channel with no secret is skipped without an error. The 31 August decision was X and LinkedIn only.

## MOI-Webinars scripts
| Name | Unlocks | Used by | Lives in | Who grants | Status |
|---|---|---|---|---|---|
| `BUFFER_API_KEY` | Scheduled X and LinkedIn posts | `scripts/buffer.mjs` in `moi-foundation/MOI-Webinars` (branch `claude/agent-payments-simple`, not `main` as of 2026-10-02) | `.env` at the repo root, last line wins | Buffer organisation owner | TBD |
| Per-session `MOI_MNEMONIC` and `OPENAI_API_KEY` or `GROQ_API_KEY` | A funded devnet demo wallet, model calls in demos | `session-N/` code | Each session's `.env` from `.env.example` | The presenter | TBD |
This is a different name from `BUFFER_ACCESS_TOKEN`. The two pipelines do not share a variable.

## Dataroom (`sarvalabs/moi-dataroom0`)
| Name | Unlocks | Used by | Lives in | Who grants | Status |
|---|---|---|---|---|---|
| `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Browser access to Supabase, baked at build | App | Actions secrets | The company Supabase organisation (moved 8 October 2026) | TBD |
| `SUPABASE_SERVICE_ROLE_KEY` | Server access that bypasses row-level security | App | Actions secret | Same | TBD |
| `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` | Chat and embeddings | App | Actions secrets | No company-owned key exists; the keys now set are not company keys (`ENV-VARS.md`). The chat widget is hidden | TBD |
| `ADMIN_SECRET` | Dataroom admin | App | Actions secret, set on the VM at deploy | DevOps (Srikar) can read the copy on the server (`project-handover-docs/DATAROOM.md`) | TBD |
| `CLAUDE_PER_IP_HOURLY_LIMIT`, `CLAUDE_DAILY_TOKEN_BUDGET`, `CLAUDE_MAX_INPUT_TOKENS`, `CLAUDE_MAX_OUTPUT_TOKENS` | Chat spend limits | App | The VM environment, optional | Upendhar | TBD |
| `ADMIN_TOKEN`, `DATAROOM_URL` | Names the app code reads | App, whitepaper script | Set by no deploy (`DATAROOM.md`) | See that doc | TBD |

## Points Program (`sarvalabs/moi-project`)
| Name | Unlocks | Used by | Lives in | Who grants | Status |
|---|---|---|---|---|---|
| `DATABASE_URL` | The Supabase Postgres holding every user and point. On the Points email account, free plan, no backups | App, migrations | Actions secret and the container env | The Points email account (stated 2026-10-06). ASK: Rahul who holds that login | TBD |
| `BETTER_AUTH_SECRET`, `CRON_SECRET`, `TELEGRAM_WEBHOOK_SECRET` | Sessions, job auth, webhook auth | App | Actions secrets | A repo admin generates them (`project-handover-docs/POINTS-PROGRAM.md`) | TBD |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | Google sign-in | App | Actions secrets | The sarvalabsdeveloper@gmail.com account (Google Cloud console) | TBD |
| `X_CLIENT_SECRET`, variable `X_CLIENT_ID` | X developer app (paid API) for verification | App | Actions | The sarvalabsdeveloper@gmail.com account (X developer portal) | TBD |
| `DISCORD_CLIENT_SECRET`, `DISCORD_BOT_TOKEN`, variables `DISCORD_CLIENT_ID`, `DISCORD_GUILD_ID`, `DISCORD_INVITE_URL` | Discord app and bot | App | Actions | The sarvalabsdeveloper@gmail.com account (Discord developer portal) | TBD |
| `TELEGRAM_BOT_TOKEN`, variables `TELEGRAM_BOT_USERNAME`, `TELEGRAM_CHAT_ID`, `TELEGRAM_INVITE_MODE` | Telegram bot | App | Actions | The sarvalabsdeveloper@gmail.com account (BotFather) | TBD |
| `RESEND_API_KEY`, variable `EMAIL_FROM` | Sign-in emails. Both must be set or none are sent | App | Actions | The sarvalabsdeveloper@gmail.com account (Resend) | TBD |
| `GHCR_PAT`, `TELEPORT_JOIN_TOKEN` | Image and VM access | Workflows | Actions secrets | Upendhar | TBD |
| `ADMIN_EMAILS` (variable). The `admin_users` table is empty, so only this variable grants admin (13 October 2026); add the webinar hosts' Google emails here | Points admin pages, including Webinar bounties | App | Actions | A repo admin | TBD |
| Other variables: `BETTER_AUTH_URL`, `MOI_NETWORK`, `REOWN_PROJECT_ID`, `VERIFICATION_*`, `SOCIAL_AUDIT_BATCH_SIZE` (still set and passed, read by nothing since PR #23), `X_TARGET_URL` | Public settings | App | Actions variables | Repo admin | TBD |
Read in `.env.example` at the tip of `feature/ci-cd` (commit dated 2026-09-16, read 2026-10-03), and not passed by the deploy: `X_TOKEN_ENCRYPTION_KEY`, `X_TOKEN_ENCRYPTION_KEY_PREVIOUS`, `CLIENT_IP_HEADER`, `DATABASE_SSL`, `PG_POOL_MAX`, `FAUCET_URL`, `FAUCET_API_KEY`, `FAUCET_TOKEN_ADDRESS`, `FAUCET_VERIFY_MODE` and `NEXT_PUBLIC_SITE_URL`. Enabling a task whose env is not passed stops the container at startup. The `MOI_AGENT_*` names in older notes are not in that file at the tip. Changed 13 October 2026: `deploy.yml` passes `MOI_RPC_URL`, but the Actions variable is not set, so the webinar bounty page cannot add the chain's note next to hash answers.

## Agent Launchpad (`sarvalabs/moi-agent-launchpad`)
| Name | Unlocks | Used by | Lives in | Who grants | Status |
|---|---|---|---|---|---|
| `SUPABASE_SERVICE_ROLE_KEY`, variable `SUPABASE_URL` | The Launchpad database. Migrations are run by hand in the SQL editor | App | Actions, the VM | The company Supabase organisation (moved 8 October 2026) | TBD |
| `SESSION_SECRET`, `CRON_SECRET` | Sessions, manual cleanup route | App | Actions, the VM | Generate; rotate freely | TBD |
| `AGENT_KEY_ENCRYPTION_SECRET` | Decrypting every stored agent key. Never rotate | App | Actions secret and the VM | Copy from the VM. Check with `scripts/verify-encryption-secret.mjs` in `sarvalabs/moi-agent-launchpad` | TBD |
| `GROQ_API_KEY` | Internal model calls. Users bring their own key | App | Actions | No company-owned Groq key exists; the key now set is not a company key. Create one at console.groq.com/keys (`ENV-VARS.md`) | TBD |
| `GEMINI_API_KEY`, `OPENAI_API_KEY`, `LLM_MODEL` | Optional model providers and model choice | App | Actions | Optional. No company-owned OpenAI key exists; a Gemini key is not recorded. ASK: Rahul | TBD |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_WEBHOOK_SECRET`, `ADMIN_ALERT_TELEGRAM_CHAT_ID`, variable `TELEGRAM_BOT_USERNAME` | Bot `moinetworkbot` and admin alerts | App | Actions | Adithya's Telegram account (BotFather) until the transfer in `MIGRATION-LIST.md` is done | TBD |
| `NEXT_PUBLIC_DISCORD_INVITE_URL`, `DISCORD_WEBHOOK_URL` | The Discord link on the dashboard; a notification webhook | App | Actions | A Discord server admin (Integrations, Webhooks). ASK: Rahul | TBD |
| `MOI_PLATFORM_MNEMONIC` | The funded platform wallet. README calls it optional, `.env.example` says required | App | Actions | Settled with DevOps by 2026-08-03; do not raise it again (`house-style.md` section 4) | TBD |
| `MOI_REGISTRATION_MNEMONIC_1`, `_2`, `_3` | The wallets that create and fund new users. Wiped by each reset | App | Actions | DevOps | TBD |
| `MOI_REGISTRATION_GRANT`, `MOI_REGISTRATION_DERIVATION_PATH` | Starter grant and wallet path for the registration wallets | App | Actions | DevOps | TBD |
| `MOI_DEPLOYER_MNEMONIC`, `MOI_SPONSOR_MNEMONIC` | Deploy the market contract, recreate registration wallets | Scripts | Never stored: command line or hidden prompt | The person running the script | TBD |
| `MOI_AGENT_REGISTRY_LOGIC_ID`, `MOI_AGENT_MARKET_LOGIC_ID`, `MOI_KMOI_ASSET_ID`, `MOI_READ_CALLER_ADDRESS`, `MOI_RPC_URL`, `MOI_POOL_RPC_URL` | Chain ids, the read caller and node addresses. A reset changes them | App | Actions variables | Repo admin | TBD |
| `GLOBAL_DAILY_SPEND_CAP_CENTS`, `DAILY_INTERACTION_CAP`, `MAX_AGENTS_PER_USER`, `INBOX_WAIT_MS` | Caps and a poll wait | App | Actions variables | Repo admin | TBD |
| `NEXT_PUBLIC_APP_URL`, `NEXT_PUBLIC_MOI_EXPLORER_URL`, `NEXT_PUBLIC_WALLET_INSTALL_URL`, `NEXT_PUBLIC_PAYMENTS_ENABLED` | Baked URLs and the paid-features switch. `NEXT_PUBLIC_APP_URL` is permanent in every on-chain card | App | Actions variables | Repo admin | TBD |
| `MOI_VERIFY_REGISTRATION`, `MOI_SKIP_PAYMENT_VERIFY` | Verification switches. Leave unset (`moi-launchpad-ops`) | App | Actions | Nobody sets them: leave unset | TBD |
| `MOI_REGISTRATION_API_KEY`, `MOI_REGISTRATION_API_URL` | Nothing: not in use today | None | Actions | DevOps | TBD |
| `NEXT_PUBLIC_MOI_CHAIN_ID`, `NEXT_PUBLIC_WC_PROJECT_ID` | The phone QR sign-in. Live since PRs #32 and #33 (merged 13 October 2026); the WalletConnect project id is the Launchpad's Reown project (`ENV-VARS.md`) | App | Actions variables | Repo admin | TBD |

## Agent Explorer (GitHub environment `PROD` of `sarvalabs/agent-explorer`)
| Name | Unlocks | Used by | Lives in | Who grants | Status |
|---|---|---|---|---|---|
| `DB_PASSWORD`; variables `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` | The Explorer MySQL | Server | PROD environment | Upendhar | TBD |
| `MOI_MNEMONIC`, `MOI_AGENT_ID`, `MOI_INTELLIGENCE_LOGIC_ID` | The server's own devnet identity. If `MOI_MNEMONIC` is set it signs reads and never falls back, even if the wallet is gone | Server | PROD environment | Not recorded (`MIGRATION-LIST.md`: the server devnet wallet's owner is not on record). ASK: Gokul | TBD |
| `VITE_API_BASE_URL`, `VITE_WC_PROJECT_ID`, `VITE_MOI_NETWORK`, `VITE_MOI_CHAIN_ID`, `VITE_TESSERACT_BASE_URL`, `VITE_TRANSACTION_FUEL_LIMIT` | Client build settings | Client | PROD variables | A repo admin. The WalletConnect project owner is not recorded (`MIGRATION-LIST.md`). ASK: Gokul | TBD |
| `VITE_AGENT_REGISTRY_LOGIC_ID` | Nothing: passed as a build arg, read by no client code | None | PROD variable | A repo admin | TBD |
| `MOI_RPC_URL`, `MOI_AGENT_REGISTRY_LOGIC_ID`, `MOI_DERIVATION_PATH`, `PORT` | Node address, registry id (server setting), faucet wallet path, listening port. Read on `main` (clone fetched 2026-09-24) | Server | Code defaults; the workflow sets `PORT` | Gokul | TBD |
| `LAUNCHPAD_ORIGIN` on `main` before PR #5, `LAUNCHPAD_HOSTS` from PR #5 (merged 2026-10-07) | Which Launchpad hosts the server trusts. Empty disables the rule | Server | Code default | Gokul | TBD |
| `VITE_INTELLIGENCE_LOGIC_ID`, `VITE_PARTICIPANT_BASE_URL`, `VITE_PUBLIC_URL` | Client build values. The second and third are read but never passed | Client | Build args | A repo admin | TBD |
| `VITE_MOI_AGENT_REGISTRY_LOGIC_ID` | Registry id at client build. Arrived with PR #5, merged 2026-10-07 | Client | PROD variable | A repo admin | TBD |
| `ADMIN_ADDRESSES`, `SYNC_INTERVAL_HOURS`, `MOI_READ_CALLER_ADDRESS`, `MOI_WS_URL`, `PINATA_JWT` | Server settings the workflow does not pass | Server | Code defaults | Gokul | TBD |
`LAUNCHPAD_ORIGINS` and `LAUNCHPAD_CONFIRM_ORIGIN` come from the closed PR #4 and nothing on `main` reads them (read 2026-10-03 in a clone).

## MCP server (`sarvalabs/moi-mcp`, production copy in `sarvalabs/voyage-api`)
| Name | Unlocks | Used by | Lives in | Who grants | Status |
|---|---|---|---|---|---|
| `WC_PROJECT_ID` (voyage-api secrets `MCP_PROD_WC_PROJECT_ID`, `MCP_DEV_WC_PROJECT_ID`) | Wallet pairing relay. The write gateway will not start without it | `moi-mcp` | voyage-api secrets; self-host `.env` on a VM (ASK: Srikar) | The sarvalabsdeveloper@gmail.com account (Reown, `ENV-VARS.md`) | TBD |
| `MOI_SESSION_KEY`, `PUBLIC_URL`, `MOI_READ_CALLER`, `MOI_AGENT_REGISTRY_LOGIC_ID`, `MOI_LAUNCHPAD_URL`, `MOI_CANARY_ACCOUNT` | Sign-in cookies, OAuth issuer, read simulations, registry id. `MOI_CANARY_ACCOUNT` is for the canary only. Which of them the Voyage workflow passes: `moi-mcp-ops/references/settings-and-secrets.md` | `moi-mcp` | `.env` on the VM or inline process env | Whoever deploys (the Voyage team and Srikar, `project-handover-docs/MCP-SERVER.md`) | TBD |
| `REDIS_URL` | Optional. Moves wallet pairings to Redis. It carries a password. If it is unreachable at boot the write gateway refuses to start | `moi-mcp` | Deploy environment | ASK: Srikar, then Rahul | TBD |

## Docs sites
No secrets build any docs site. The IndexNow key file is committed and public by design. The js-moi-sdk publish workflow uses `npm_token`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY` and variables `R2_ACCOUNT_ID`, `R2_BUCKET`, `R2_PREFIX`: SDK team and DevOps, status TBD.

## Forge demo (`moi-forge-hacks-demo`; MOI Sprint was scratched on 13 October 2026)
| Name | Unlocks | Used by | Lives in | Who grants | Status |
|---|---|---|---|---|---|
| `ADMIN_MNEMONIC`, `MOI_RPC_URL`, `TOKEN_NAME`, `TOKEN_SYMBOL` | The Forge demo's settings | `moi-forge-hacks-demo` | The presenter's gitignored `.env` | The presenter | TBD |

## Standards work (x402 mechanism package)
| Name | Unlocks | Used by | Lives in | Who grants | Status |
|---|---|---|---|---|---|
| `CLIENT_MOI_MNEMONIC`, `SERVER_MOI_ADDRESS`, `MOI_RPC_URL`, `MOI_ASSET_ID` | The live round trip of the end-to-end test: a funded client wallet, the seller's address, the node address and the asset | `@x402/moi` end-to-end test | The tester's gitignored `.env` | The tester. Values never recorded | TBD |
| The `npm` environment of `x402-foundation/x402` | Publishing `@x402/moi` | Upstream workflow | Upstream repo settings | Owner unknown. ASK: Rahul | TBD |
