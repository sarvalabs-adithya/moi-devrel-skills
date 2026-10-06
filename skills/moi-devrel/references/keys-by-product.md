# Keys by product: variable names

Names only. This file never holds a value, a length or a prefix. Shared accounts and keys, and the rules for handling them, are in `keys-and-access.md`. Facts are as of 2026-10-02 from `DEPENDENCIES.md` (the previous operator's local file, not in git; ASK: Adithya for a copy), the ops research notes and the repos' `.env.example` files, with changes dated where a row says so. Status is TBD for every row. "ASK" has the meaning defined in `../SKILL.md`. For anything that sits on a VM: ASK: Upendhar. Back to `../SKILL.md`.

## Website and blog (`sarvalabs/MOI-Website`)
| Name | Unlocks | Used by | Lives in | Who grants | Status |
|---|---|---|---|---|---|
| `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` | Chat answers and embeddings | Express server, `npm run ingest` | Actions secrets | ASK | TBD |
| `SUPABASE_URL`, `SUPABASE_KEY` | The Supabase project holding `documents` and `community_calls` | Server, ingest (needs a local `.env`) | Actions secrets | Project owner. ASK | TBD |
| `ADMIN_API_KEY` | Calendar admin | Server | Actions secret | A repo admin creates it | TBD |
| `VITE_CHATBOT_API` | API base baked into the site bundle. Its live value points at the dev host | Vite build | Actions secret | ASK: Upendhar | TBD |
| `ALLOWED_ORIGINS`, `PORT` | Server settings the workflow does not pass | Server on the VM | The VM (ASK: Upendhar) | Upendhar | TBD |
| `VITE_GA_ID`, `PUBLIC_GA_ID` | Nothing: the workflow passes them but no code on `main` reads them. Measurement runs through Google Tag Manager | None | Actions secrets | ASK | TBD |
| `DATA_ROOM_API_KEY`, `DATA_ROOM_CHAT_URL` | Nothing in production. `DATA_ROOM_API_KEY` is read only by `api/chat.js`, the old Vercel function (`git grep` on `main`, clone fetched 2026-09-11); `DATA_ROOM_CHAT_URL` only by the dev proxy and that function | None | Actions secret | Upendhar | TBD <!-- slop-lint: ignore --> |
| `BUFFER_ACCESS_TOKEN`, `BUFFER_CHANNEL_X`, `BUFFER_CHANNEL_LINKEDIN` | Draft X and LinkedIn posts in Buffer | `distribute.yml` | Actions secrets | Buffer organisation owner creates an API token. Channel ids come from `npm run buffer:channels` | TBD |
| `DISCORD_WEBHOOK_URL` | Immediate post to Discord | `distribute.yml` | Actions secret | A Discord server admin (Integrations, Webhooks) | TBD |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | Immediate post to the Telegram channel. The bot must be channel admin | `distribute.yml` | Actions secrets | BotFather owner. ASK | TBD |
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
| `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Browser access to Supabase, baked at build | App | Actions secrets | Project owner. ASK | TBD |
| `SUPABASE_SERVICE_ROLE_KEY` | Server access that bypasses row-level security | App | Actions secret | Same | TBD |
| `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` | Chat and embeddings | App | Actions secrets | ASK | TBD |
| `ADMIN_SECRET` | Dataroom admin | App | Actions secret, set on the VM at deploy | Whoever knows it. ASK | TBD |
| `CLAUDE_PER_IP_HOURLY_LIMIT`, `CLAUDE_DAILY_TOKEN_BUDGET`, `CLAUDE_MAX_INPUT_TOKENS`, `CLAUDE_MAX_OUTPUT_TOKENS` | Chat spend limits | App | The VM environment, optional | Upendhar | TBD |
| `ADMIN_TOKEN`, `DATAROOM_URL` | Names the app code reads | App, whitepaper script | Unknown | ASK | TBD |

## Points Program (`sarvalabs/moi-project`)
| Name | Unlocks | Used by | Lives in | Who grants | Status |
|---|---|---|---|---|---|
| `DATABASE_URL` | The Supabase Postgres holding every user and point. Personal free plan, no backups | App, migrations | Actions secret and the container env | The previous operator's personal login. ASK: Rahul to move it to a company login | TBD |
| `BETTER_AUTH_SECRET`, `CRON_SECRET`, `TELEGRAM_WEBHOOK_SECRET` | Sessions, job auth, webhook auth | App | Actions secrets | Adithya | TBD |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | Google sign-in | App | Actions secrets | ASK | TBD |
| `X_CLIENT_SECRET`, variable `X_CLIENT_ID` | X developer app (paid API) for verification | App | Actions | ASK | TBD |
| `DISCORD_CLIENT_SECRET`, `DISCORD_BOT_TOKEN`, variables `DISCORD_CLIENT_ID`, `DISCORD_GUILD_ID`, `DISCORD_INVITE_URL` | Discord app and bot | App | Actions | ASK | TBD |
| `TELEGRAM_BOT_TOKEN`, variables `TELEGRAM_BOT_USERNAME`, `TELEGRAM_CHAT_ID`, `TELEGRAM_INVITE_MODE` | Telegram bot | App | Actions | ASK | TBD |
| `RESEND_API_KEY`, variable `EMAIL_FROM` | Sign-in emails. Both must be set or none are sent | App | Actions | ASK | TBD |
| `GHCR_PAT`, `TELEPORT_JOIN_TOKEN` | Image and VM access | Workflows | Actions secrets | Upendhar | TBD |
| `ADMIN_EMAILS` (variable) or the `admin_users` table | Points admin pages | App | Actions, database | A repo admin | TBD |
| Other variables: `BETTER_AUTH_URL`, `MOI_NETWORK`, `REOWN_PROJECT_ID`, `VERIFICATION_*`, `SOCIAL_AUDIT_BATCH_SIZE`, `X_TARGET_URL` | Public settings | App | Actions variables | Repo admin | TBD |
Read in `.env.example` at the tip of `feature/ci-cd` (commit dated 2026-09-16, read 2026-10-03), and not passed by the deploy: `X_TOKEN_ENCRYPTION_KEY`, `X_TOKEN_ENCRYPTION_KEY_PREVIOUS`, `CLIENT_IP_HEADER`, `DATABASE_SSL`, `PG_POOL_MAX`, `MOI_RPC_URL`, `FAUCET_URL`, `FAUCET_API_KEY`, `FAUCET_TOKEN_ADDRESS`, `FAUCET_VERIFY_MODE` and `NEXT_PUBLIC_SITE_URL`. Enabling a task whose env is not passed stops the container at startup. The `MOI_AGENT_*` names in older notes are not in that file at the tip.

## Agent Launchpad (`sarvalabs/moi-agent-launchpad`)
| Name | Unlocks | Used by | Lives in | Who grants | Status |
|---|---|---|---|---|---|
| `SUPABASE_SERVICE_ROLE_KEY`, variable `SUPABASE_URL` | The Launchpad database. Migrations are run by hand in the SQL editor | App | Actions, the VM | Project owner's login. ASK | TBD |
| `SESSION_SECRET`, `CRON_SECRET` | Sessions, manual cleanup route | App | Actions, the VM | Generate; rotate freely | TBD |
| `AGENT_KEY_ENCRYPTION_SECRET` | Decrypting every stored agent key. Never rotate | App | Actions secret and the VM | Copy from the VM. Check with `scripts/verify-encryption-secret.mjs` in `sarvalabs/moi-agent-launchpad` | TBD |
| `GROQ_API_KEY` | Internal model calls. Users bring their own key | App | Actions | Adithya, console.groq.com | TBD |
| `GEMINI_API_KEY`, `OPENAI_API_KEY`, `LLM_MODEL` | Optional model providers and model choice | App | Actions | ASK: Adithya | TBD |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_WEBHOOK_SECRET`, `ADMIN_ALERT_TELEGRAM_CHAT_ID`, variable `TELEGRAM_BOT_USERNAME` | Bot `moinetworkbot` and admin alerts | App | Actions | Adithya, via BotFather | TBD |
| `NEXT_PUBLIC_DISCORD_INVITE_URL`, `DISCORD_WEBHOOK_URL` | The Discord link on the dashboard; a notification webhook | App | Actions | ASK: Adithya | TBD |
| `MOI_PLATFORM_MNEMONIC` | The funded platform wallet. README calls it optional, `.env.example` says required | App | Actions | Adithya or DevOps. ASK | TBD |
| `MOI_REGISTRATION_MNEMONIC_1`, `_2`, `_3` | The wallets that create and fund new users. Wiped by each reset | App | Actions | DevOps | TBD |
| `MOI_REGISTRATION_GRANT`, `MOI_REGISTRATION_DERIVATION_PATH` | Starter grant and wallet path for the registration wallets | App | Actions | DevOps | TBD |
| `MOI_DEPLOYER_MNEMONIC`, `MOI_SPONSOR_MNEMONIC` | Deploy the market contract, recreate registration wallets | Scripts | Never stored: command line or hidden prompt | The person running the script | TBD |
| `MOI_AGENT_REGISTRY_LOGIC_ID`, `MOI_AGENT_MARKET_LOGIC_ID`, `MOI_KMOI_ASSET_ID`, `MOI_READ_CALLER_ADDRESS`, `MOI_RPC_URL`, `MOI_POOL_RPC_URL` | Chain ids, the read caller and node addresses. A reset changes them | App | Actions variables | Repo admin | TBD |
| `GLOBAL_DAILY_SPEND_CAP_CENTS`, `DAILY_INTERACTION_CAP`, `MAX_AGENTS_PER_USER`, `INBOX_WAIT_MS` | Caps and a poll wait | App | Actions variables | Repo admin | TBD |
| `NEXT_PUBLIC_APP_URL`, `NEXT_PUBLIC_MOI_EXPLORER_URL`, `NEXT_PUBLIC_WALLET_INSTALL_URL`, `NEXT_PUBLIC_PAYMENTS_ENABLED` | Baked URLs and the paid-features switch. `NEXT_PUBLIC_APP_URL` is permanent in every on-chain card | App | Actions variables | Repo admin | TBD |
| `MOI_VERIFY_REGISTRATION`, `MOI_SKIP_PAYMENT_VERIFY` | Verification switches. Leave unset (`moi-launchpad-ops`) | App | Actions | ASK: Adithya | TBD |
| `MOI_REGISTRATION_API_KEY`, `MOI_REGISTRATION_API_URL` | Nothing: not in use today | None | Actions | DevOps | TBD |
| `NEXT_PUBLIC_MOI_CHAIN_ID`, `NEXT_PUBLIC_WC_PROJECT_ID` | Nothing on `master`: only the unmerged phone sign-in branch reads them | None | Actions variables | Adithya | TBD |

## Agent Explorer (GitHub environment `PROD` of `sarvalabs/agent-explorer`)
| Name | Unlocks | Used by | Lives in | Who grants | Status |
|---|---|---|---|---|---|
| `DB_PASSWORD`; variables `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` | The Explorer MySQL | Server | PROD environment | Upendhar | TBD |
| `MOI_MNEMONIC`, `MOI_AGENT_ID`, `MOI_INTELLIGENCE_LOGIC_ID` | The server's own devnet identity. If `MOI_MNEMONIC` is set it signs reads and never falls back, even if the wallet is gone | Server | PROD environment | ASK | TBD |
| `VITE_API_BASE_URL`, `VITE_WC_PROJECT_ID`, `VITE_MOI_NETWORK`, `VITE_MOI_CHAIN_ID`, `VITE_TESSERACT_BASE_URL`, `VITE_TRANSACTION_FUEL_LIMIT` | Client build settings | Client | PROD variables | A repo admin. The WalletConnect project owner is unknown. ASK | TBD |
| `VITE_AGENT_REGISTRY_LOGIC_ID` | Nothing: passed as a build arg, read by no client code | None | PROD variable | A repo admin | TBD |
| `MOI_RPC_URL`, `MOI_AGENT_REGISTRY_LOGIC_ID`, `MOI_DERIVATION_PATH`, `PORT` | Node address, registry id (server setting), faucet wallet path, listening port. Read on `main` (clone fetched 2026-09-24) | Server | Code defaults; the workflow sets `PORT` | Gokul | TBD |
| `LAUNCHPAD_ORIGIN` on `main`, `LAUNCHPAD_HOSTS` on PR #5 | Which Launchpad hosts the server trusts. Empty disables the rule | Server | Code default | Gokul | TBD |
| `VITE_INTELLIGENCE_LOGIC_ID`, `VITE_PARTICIPANT_BASE_URL`, `VITE_PUBLIC_URL` | Client build values. The second and third are read but never passed | Client | Build args | A repo admin | TBD |
| `VITE_MOI_AGENT_REGISTRY_LOGIC_ID` | Registry id at client build. Only on the PR #5 branch | Client | PROD variable once PR #5 merges | A repo admin | TBD |
| `ADMIN_ADDRESSES`, `SYNC_INTERVAL_HOURS`, `MOI_READ_CALLER_ADDRESS`, `MOI_WS_URL`, `PINATA_JWT` | Server settings the workflow does not pass | Server | Code defaults | Gokul | TBD |
`LAUNCHPAD_ORIGINS` and `LAUNCHPAD_CONFIRM_ORIGIN` come from the closed PR #4 and nothing on `main` reads them (read 2026-10-03 in a clone).

## MCP server (`sarvalabs/moi-mcp`, production copy in `sarvalabs/voyage-api`)
| Name | Unlocks | Used by | Lives in | Who grants | Status |
|---|---|---|---|---|---|
| `WC_PROJECT_ID` (voyage-api secrets `MCP_PROD_WC_PROJECT_ID`, `MCP_DEV_WC_PROJECT_ID`) | Wallet pairing relay. The write gateway will not start without it | `moi-mcp` | voyage-api secrets; self-host `.env` on a VM (ASK: Upendhar) | Reown project owner. ASK | TBD |
| `MOI_SESSION_KEY`, `PUBLIC_URL`, `MOI_READ_CALLER`, `MOI_AGENT_REGISTRY_LOGIC_ID`, `MOI_LAUNCHPAD_URL`, `MOI_CANARY_ACCOUNT` | Sign-in cookies, OAuth issuer, read simulations, registry id. `MOI_CANARY_ACCOUNT` is for the canary only. Which of them the Voyage workflow passes: `moi-mcp-ops/references/settings-and-secrets.md` | `moi-mcp` | `.env` on the VM or inline process env | Whoever deploys. ASK | TBD |
| `REDIS_URL` | Optional. Moves wallet pairings to Redis. It carries a password. If it is unreachable at boot the write gateway refuses to start | `moi-mcp` | Deploy environment | ASK: Srikar, then Rahul | TBD |

## Docs sites
No secrets build any docs site. The IndexNow key file is committed and public by design. The js-moi-sdk publish workflow uses `npm_token`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY` and variables `R2_ACCOUNT_ID`, `R2_BUCKET`, `R2_PREFIX`: SDK team and DevOps, status TBD.

## MOI Sprint (guide site `moisprint`, scaffolds in `tSwapper`)
| Name | Unlocks | Used by | Lives in | Who grants | Status |
|---|---|---|---|---|---|
| `MOI_RPC_URL`, `NEXT_PUBLIC_MOI_RPC_URL`, `SPRINT_PROGRESS_LOGIC_ID`, `NEXT_PUBLIC_SPRINT_PROGRESS_LOGIC_ID`, `ADMIN_MNEMONIC` | The guide site's chain settings and the wallet that deployed its progress logic | Guide site | Vercel project environment and `.env.local` | Owner unknown. ASK: Adithya, Rahul | TBD | <!-- slop-lint: ignore -->
| `MOISPRINT_URL` | Optional address the scaffold's test script reports to | `tSwapper` | The student's shell | The student | TBD |
| `RPC_URL`, `POOL_OWNER_MNEMONIC`, `POOL_OWNER_ADDRESS` | A student's own devnet settings in a scaffold's `.env.example` | `tSwapper` | The student's gitignored `.env` | The student | TBD |
| `ADMIN_MNEMONIC`, `MOI_RPC_URL`, `TOKEN_NAME`, `TOKEN_SYMBOL` | The Forge demo's settings | `moi-forge-hacks-demo` | The presenter's gitignored `.env` | The presenter | TBD |

## Standards work (x402 mechanism package)
| Name | Unlocks | Used by | Lives in | Who grants | Status |
|---|---|---|---|---|---|
| `CLIENT_MOI_MNEMONIC`, `SERVER_MOI_ADDRESS`, `MOI_RPC_URL`, `MOI_ASSET_ID` | The live round trip of the end-to-end test: a funded client wallet, the seller's address, the node address and the asset | `@x402/moi` end-to-end test | The tester's gitignored `.env` | The tester. Values never recorded | TBD |
| The `npm` environment of `x402-foundation/x402` | Publishing `@x402/moi` | Upstream workflow | Upstream repo settings | Owner unknown. ASK: Rahul | TBD |
