# Handover: MOI Agent Launchpad

Two remotes matter. `sarvalabs-adithya/moi-agent-launchpad` is where the work happened (working
clone `~/nno code agentapp`, 334 commits, 14 July to 24 September 2026). `sarvalabs/moi-agent-launchpad`
is the org copy that production deploys from. Pushing to the first deploys nothing.

Production is **not on Vercel**. It was, until early August, when the always-on inbox polling burned
the Hobby compute allowance with a handful of agents. It now runs as a Docker container on a MOI
DevOps VM, deployed by GitHub Actions. The old `moi-agent-launchpad.vercel.app` host still appears in
the code because agents registered under it are still counted as launchpad agents.

---

## 1. Environment variables

### Where the values live

| Place | What it holds | Who can read it |
| --- | --- | --- |
| `.env.local` in the repo | local dev values, Supabase at `127.0.0.1`, mock mode | you |
| GitHub Actions on `sarvalabs/moi-agent-launchpad` | every production value: Secrets for the sensitive ones, Variables for the rest | secrets are **write-only**, variables are readable |
| `/opt/moi-agent-launchpad/.env` on the VM | the same production values, written fresh by every deploy, `chmod 600` | anyone with a Teleport session on the box |
| The Docker image | the five `NEXT_PUBLIC_*` values, baked in at build time as `ARG`s | rebuild to change them, a restart is not enough |

Because Actions secrets cannot be read back, **the only readable copy of production secrets is the
`.env` on the VM**. The operator guide's advice stands: put every value in a shared vault, or one
person leaving makes a secret unrecoverable.

### How production gets deployed

Push to `master` on the org repo. `ci-cd.yml` builds the image with `docker-build.yml`, tags it
`ghcr.io/sarvalabs/moi-agent-launchpad:<short sha>` and `:latest`, then `deploy.yml` authenticates
to Teleport with Machine ID, SSHes to `VM_USER@VM_HOST`, rewrites the `.env` from Actions, and runs
`docker compose pull` and `up -d`. One container, `web`, on port 3008 mapped to 3000. Public host is
`launchpad.moi.technology`; the proxy from that name to the port lives on the VM, not in the repo.

Infrastructure values in Actions, separate from the app's own: secrets `TELEPORT_PROXY`,
`TELEPORT_JOIN_TOKEN`, `GHCR_PAT`; variables `VM_HOST`, `VM_USER`. These belong to DevOps.

**There is no worker in production, on purpose.** `npm run worker` long-polls Telegram, which deletes
the webhook the web container serves, and its tick would re-run every agent server-side. Agents run
on their owners' machines. The worker is a local-dev tool only.

### Required to boot

| Variable | What it does | Where to get it | Actions type |
| --- | --- | --- | --- |
| `SUPABASE_URL` | Postgres endpoint | Supabase dashboard, the project, Settings, API | variable |
| `SUPABASE_SERVICE_ROLE_KEY` | All database access. Row-level security denies everything, so every route uses this | same page, service role or `sb_secret` key. Never reaches the browser | secret |
| `SESSION_SECRET` | Signs the Sign-In With MOI session token | `openssl rand -hex 32`. Rotating only logs everyone out | secret |
| `AGENT_KEY_ENCRYPTION_SECRET` | AES-256-GCM key over every stored agent private key | `openssl rand -hex 32` **once**. Cannot be rotated: a different value makes every stored key permanently undecryptable and the plaintext exists nowhere else. Verify a candidate with `scripts/verify-encryption-secret.mjs` before any migration | secret |
| `MOI_RPC_URL` | Which node to talk to | `https://rpc.devnet.moi.technology` | variable |
| `MOI_PLATFORM_MNEMONIC` | Funded wallet that reads the registry and runs the heartbeat. Never signs a user's registration | make a wallet, fund it from the Voyage faucet | secret |
| `NEXT_PUBLIC_APP_URL` | The app's own public URL | `https://launchpad.moi.technology` | variable, baked into the image |

### Chain identifiers

| Variable | What it does | Where to get it |
| --- | --- | --- |
| `MOI_AGENT_REGISTRY_LOGIC_ID` | The deployed agent registry. Unset means the default in `lib/moi/registry.ts`. **After a devnet reset this is the one value to change**, then redeploy | the logic id printed when the registry is redeployed; ask whoever redeployed it |
| `MOI_AGENT_MARKET_LOGIC_ID` | The marketplace payment contract. Built-in default is correct unless the contract is redeployed | `node contracts/agent_market/deploy.mjs` prints it |
| `MOI_KMOI_ASSET_ID` | Override for the fuel asset id | only after a protocol change; the SDK constant is the default |
| `NEXT_PUBLIC_MOI_CHAIN_ID` | CAIP-2 id the phone pairing asks for | defaults to `moi:14` |

### Telegram

| Variable | What it does | Where to get it | Actions type |
| --- | --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | The delivery bot | BotFather, `/token` for the existing bot | secret |
| `TELEGRAM_BOT_USERNAME` | Deep links. Production is `moinetworkbot` | BotFather | variable |
| `TELEGRAM_WEBHOOK_SECRET` | Shared secret on the webhook route | `openssl rand -hex 20`. If you rotate it, **re-run `setWebhook`** with the new value or Telegram silently stops delivering | secret |
| `ADMIN_ALERT_TELEGRAM_CHAT_ID` | Where alerts go | message the bot, read your chat id from `getUpdates` | secret |

### Model provider

Every completion goes through `lib/llm.ts`. First key set wins: `GROQ_API_KEY`, then
`GEMINI_API_KEY`, then `OPENAI_API_KEY`. In production only Groq is set, and since 2 August it backs
internal paths only: every agent runs on its owner's own key, saved on their machine by the setup
script (`BYOKEY`). `LLM_MODEL` overrides the model name.

| Variable | Where to get it | Note |
| --- | --- | --- |
| `GROQ_API_KEY` | console.groq.com/keys, free, no card | no retention or training on inputs |
| `GEMINI_API_KEY` | aistudio.google.com/apikey | free tier trains on inputs, so users' own keys only |
| `OPENAI_API_KEY` | platform.openai.com | paid fallback |

### Wallet activation, one of two modes

New wallets cannot get on chain without one of these. Proxy mode wins when both are set. **Direct
mode is what runs today.**

| Variable | Mode | Where to get it |
| --- | --- | --- |
| `MOI_REGISTRATION_API_URL`, `MOI_REGISTRATION_API_KEY` | proxy: MOI's hosted registration service, the one behind Discord `/register` | MOI DevOps. The service ships bound to localhost on MOI's VM and has to be exposed first |
| `MOI_REGISTRATION_MNEMONIC_1`, `_2`, `_3` | direct: the launchpad signs `PARTICIPANT_CREATE` from funded wallets | MOI DevOps holds these. Actions secrets only, never in the repo, don't re-share |
| `MOI_REGISTRATION_GRANT` | KMOI per activation | defaults to 100000 |
| `MOI_REGISTRATION_DERIVATION_PATH` | path for those wallets | defaults to `m/44'/6174'/1'/0/0`. The faucet path `7020'` differs, override only if the sender account cannot be found |

### Tunables and switches

| Variable | What it does | Default |
| --- | --- | --- |
| `INBOX_WAIT_MS` | how long the server holds an inbox long-poll | 2000 in code, **20000 on the VM** where a long hold is free |
| `GLOBAL_DAILY_SPEND_CAP_CENTS` | platform-wide daily spend cap | 500 |
| `DAILY_INTERACTION_CAP`, `MAX_AGENTS_PER_USER` | per-user guardrails in `lib/limits.ts` | see file |
| `CRON_SECRET` | bearer token on the hourly `/api/cron/cleanup` job | `openssl rand -hex 32`; rotate freely, then update whatever calls the job |
| `NEXT_PUBLIC_WC_PROJECT_ID` | phone sign-in by WalletConnect QR; unset just hides the option | cloud.reown.com, create a project, copy the 32-character id. Public, baked into the image |
| `NEXT_PUBLIC_PAYMENTS_ENABLED` | marketplace payments switch | on |
| `DISCORD_WEBHOOK_URL`, `NEXT_PUBLIC_DISCORD_INVITE_URL` | Discord notifications and the invite link on the dashboard | Discord server settings |
| `NEXT_PUBLIC_MOI_EXPLORER_URL` | explorer links | `https://voyage.moi.technology` |
| `NEXT_PUBLIC_WALLET_INSTALL_URL` | wallet install link. **Must include the extension id** or it opens a generic store page | Chrome Web Store |
| `MOI_POOL_RPC_URL`, `MOI_READ_CALLER_ADDRESS` | alternate RPC for pool reads, and the caller address used for reads | leave unset |
| `MOI_SKIP_PAYMENT_VERIFY`, `MOI_VERIFY_REGISTRATION` | test toggles in the API routes | never set in production |

### Not server config

`AGENT_HOME` and `AGENT_CONFIG` are read by the runtime on the user's laptop. `MNEMONIC`,
`MOI_DERIVATION_PATH`, `MOI_SPONSOR_MNEMONIC` and `MOI_SPONSOR_DERIVATION_PATH` are inputs to the
one-off scripts under `scripts/`, passed on the command line, never stored.

### What to hand over in person

Readable now, from the VM `.env` or the source service: the Supabase service role key,
`AGENT_KEY_ENCRYPTION_SECRET`, `MOI_PLATFORM_MNEMONIC`, `TELEGRAM_BOT_TOKEN`, `GROQ_API_KEY`. Safe
to rotate instead: `SESSION_SECRET`, `CRON_SECRET`, `TELEGRAM_WEBHOOK_SECRET`. Request from DevOps
rather than copy: the three registration mnemonics, the Teleport and GHCR credentials, the VM host.

Local files on this Mac holding real values, none in git: `.env`, `.env.local`, `.env.production`,
`.env.vercel`. The local `.env` is **not** a production source: it points at a local Supabase and
mock mode.

---

## 2. What it is

A no-code platform on MOI. A participant connects MOI Wallet, picks one of ten agent templates,
approves one on-chain registration, and owns the agent. The agent runs on their own machine under
pm2 and delivers to them on Telegram through the platform relay. No seed phrase is typed anywhere
on the site.

## 3. Stack and processes

Next.js 14, React 18, Tailwind, TypeScript, Postgres on Supabase, `js-moi-sdk`, grammy for
Telegram, jose for sessions, noble for crypto, zod for validation, Vitest for tests. The marketplace
contract is Coco. Node 22 in the image.

| Process | Runs where | Job |
| --- | --- | --- |
| `web` container, `npm start` | the DevOps VM, port 3008 | pages, API routes, the Telegram webhook, the relay |
| `public/runtime.cjs` under pm2 | each user's own laptop | runs their agent, signs every relay call |
| `npm run worker` | local dev only | never in production, see above |

Build the runtime with `npm run build:runtime`. Tests: `npm test`, and `npm run test:atomicity` for
the database guardrails.

## 4. Where it stands

Working clone on branch `walletconnect-qr-signin`, **9 commits not pushed** and **8 files
uncommitted**: an unreviewed `app/labs/` and `app/api/labs/`, plus one-off chain scripts for
clearing stuck nonces, counting installed agents and finding the first blocked nonce. Someone taking
over decides what ships and what was scratch.

Late-September numbers: 20 agents on chain, 16 owners, 5,405 completed runs.

## 5. Read first

`docs/HANDOFF.md`, the operator guide, especially its secrets checklist and hosting economics.
`docs/E2E-TESTING.md` before any launch. `supabase/migrations/` applies in order.
