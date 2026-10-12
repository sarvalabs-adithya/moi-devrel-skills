# Agent Launchpad

**Status: active.** Live at launchpad.moi.technology. Inactive: paid agents (the AgentMarket contract, not redeployed) and the phone QR sign-in (merged, switched off until its variables are set).

Video: https://drive.google.com/file/d/1FruKR8k6Wp_rplSFzIE8pZf8OBwBUfSI/view (recorded 12 October 2026).

The web app at launchpad.moi.technology where anyone can launch an AI agent on MOI: pick a template, register the agent on chain, and talk to it on Telegram. I built it and run it. DevOps owns the server it runs on.

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Codebase | DevRel | https://github.com/sarvalabs/moi-agent-launchpad deploys. I work in my fork, sarvalabs-adithya/moi-agent-launchpad |
| Database (Supabase) | Company Supabase organisation (transferred 8 October) | Holds all app state |
| Telegram bot and the alert chat | DevRel, transfer pending | @moinetworkbot delivers agent messages to users. Moves to DevOps or a company account in BotFather (steps in MIGRATION-LIST.md) |
| AgentMarket contract on devnet | DevRel | Not redeployed since the devnet wipes, so paid agents are off. The code is there; the next owner redeploys it when it is needed |
| Server, CI/CD, container registry, Teleport | DevOps | |
| Domain launchpad.moi.technology | DevOps | |
| Registration wallets that activate new users | DevOps | |
| Agent registry on devnet | Protocol team | Its id changes on every devnet reset |

## Stack

| Piece | What it is |
|---|---|
| Next.js 14 + React 18 + TypeScript + Tailwind | The whole product: landing, connect, create, dashboard, agent pages, marketplace, stats, and about 45 API routes |
| Supabase Postgres | All app state, server side only through the service-role key. Twelve SQL migration files in supabase/migrations |
| js-moi-sdk, js-moi-identifiers, js-polo, js-moi-agent-registry | Chain reads and writes on devnet, in lib/moi |
| AgentMarket contract (Coco) | contracts/agent_market: each paid agent's price and the payment. Not redeployed since the devnet wipes |
| Wallet sign-in | The wallet signs a one-time code, the server issues a session cookie. WalletConnect adds the phone QR sign-in (PR #32) |
| Telegram through grammy | @moinetworkbot, the webhook route and account linking |
| Agent runtime | agent-runtime/index.ts bundled into public/runtime.cjs. Users download it and run it themselves; it polls the relay routes. Twelve templates in lib/templates |
| AI keys | Each agent uses its owner's own key (Groq, Google or OpenAI). The server's Groq key serves internal paths only |
| Docker + GitHub Actions + GHCR + Teleport | One container behind nginx on the DevOps box. Merging to master builds and deploys |
| Cleanup | Runs inside the app every six hours. The cron route guarded by CRON_SECRET is only the manual trigger |
| vitest | 28 test files. The atomicity tests need a database |

No worker runs in production on purpose: it would steal the Telegram webhook and run every agent twice.

## Env vars

The index across every product, with the consoles and who holds each login, is ENV-VARS.md.
Where they live: production values are GitHub Actions secrets and variables on sarvalabs/moi-agent-launchpad (secrets cannot be read back; the readable copy is the env file on the VM, reached through DevOps). Locally, .env.local copied from .env.example. Anything starting NEXT_PUBLIC_ is baked into the image at build time, so it needs a rebuild, and only the names with a build arg reach the build. A new variable needs a line in deploy.yml, and a new NEXT_PUBLIC_ one also needs an ARG in the Dockerfile and a build arg in the build workflow. Setting a value deploys nothing: run the workflow.

| Variable | What it is | Where the value comes from |
|---|---|---|
| SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY | The database | Supabase dashboard, the project (company organisation), Settings, API |
| SESSION_SECRET | Signs the session cookie | Generate with: openssl rand -hex 32 |
| AGENT_KEY_ENCRYPTION_SECRET | Encrypts every stored agent key. Never generate a new one: every stored key would be lost | The VM env file, through DevOps |
| MOI_PLATFORM_MNEMONIC | The funded platform wallet, for registry reads and the heartbeat | deploy.yml reads it, but it is not in the repo's secrets list: an org-level secret, or the VM gets an empty value. Confirm with DevOps. Same for ADMIN_ALERT_TELEGRAM_CHAT_ID |
| MOI_RPC_URL | Empty means the SDK's built-in devnet endpoint. The Actions variable is set to a value today: confirm it points at a host that resolves, or clear it | The devnet RPC address |
| NEXT_PUBLIC_APP_URL | https://launchpad.moi.technology. Baked at build | |
| TELEGRAM_BOT_TOKEN, TELEGRAM_BOT_USERNAME, TELEGRAM_WEBHOOK_SECRET, ADMIN_ALERT_TELEGRAM_CHAT_ID | The bot, its webhook and the alert chat. After changing the webhook secret, run setWebhook again or messages stop. Unset, the secret is derived from SESSION_SECRET, so rotating that one would stop Telegram too | BotFather; the secret with openssl rand -hex 20 |
| MOI_AGENT_REGISTRY_LOGIC_ID | The agent registry. The one value that changes after a devnet reset. No Actions variable exists today, so the code default in lib/moi/registry.ts runs; deploy.yml already reads the name, so create the variable at the next reset | Protocol team |
| MOI_AGENT_MARKET_LOGIC_ID | The AgentMarket contract. deploy.yml does not pass it yet | Printed by contracts/agent_market/deploy.mjs |
| MOI_REGISTRATION_MNEMONIC_1, _2, _3, or MOI_REGISTRATION_API_URL and MOI_REGISTRATION_API_KEY | The wallets that activate new users (the API pair is not in use) | DevOps. Never copy them around |
| GROQ_API_KEY | The server's own key, internal paths only | console.groq.com |
| GEMINI_API_KEY, OPENAI_API_KEY | Second and third in the LLM fallback order. Not passed by the deploy, so unset in production | Google AI Studio, platform.openai.com |
| CRON_SECRET | The manual cleanup trigger | Generate with: openssl rand -hex 32 |
| INBOX_WAIT_MS, GLOBAL_DAILY_SPEND_CAP_CENTS | The inbox long-poll window (20000, written in deploy.yml) and the daily spend cap (an Actions variable, 500; an empty value reads as zero, so never blank it) | |
| NEXT_PUBLIC_MOI_EXPLORER_URL, NEXT_PUBLIC_WALLET_INSTALL_URL | Explorer and wallet links. Baked at build | Values in .env.example |
| NEXT_PUBLIC_WC_PROJECT_ID, NEXT_PUBLIC_MOI_CHAIN_ID | The phone QR sign-in (PR #32). The project id was set on 7 October after that day's build, so one more run of the CI/CD workflow switches it on. The chain id falls back to moi:14 | cloud.reown.com, the project, Project ID; moi:14 |

The example file with comments is .env.example in the repo.

**What to hand over in person**

- Readable only from the VM env file, through DevOps: the Supabase service-role key, AGENT_KEY_ENCRYPTION_SECRET, MOI_PLATFORM_MNEMONIC, TELEGRAM_BOT_TOKEN, GROQ_API_KEY.
- Safe to rotate instead of copying: SESSION_SECRET, CRON_SECRET, TELEGRAM_WEBHOOK_SECRET.
- Request from DevOps rather than copy: the three registration mnemonics, the Teleport and GHCR credentials, the VM host.

**Read first, in the repo**

- docs/HANDOFF.md, the operator guide, especially its secrets checklist and hosting economics.
- docs/E2E-TESTING.md before any launch.
- supabase/migrations applies in order.

## Process

**Shipping a change**

- Work on a branch in my fork.
- Run typecheck and tests myself. Nothing runs them on a pull request.
- If I changed an agent template or the agent runtime (the one file users download and run on their own laptop), rebuild that file and commit it. The repo serves the built copy.
- Open a pull request on the org repo.
- Merging to master builds a Docker image and deploys it to the server. Nothing is deployed by hand.
- Check the deploy run and the live site. A failed run leaves the old version serving, with no alert.

**Changing a setting or a secret**

- Set it in GitHub, under the repo's Actions secrets and variables.
- Run the deploy workflow by hand. Setting a value deploys nothing on its own.
- A new setting also needs a line in the deploy workflow.
- Never replace the agent key encryption secret: every stored agent key would be lost.

**Changing the database**

- Write the migration file.
- Run it by hand in the Supabase SQL editor, in order, before the code that needs it is merged.

**After a devnet reset**

- Get the new agent registry id from the Protocol team.
- Update it in the repo variables.
- Run the deploy workflow by hand.
- Check with DevOps that the registration wallets are funded again.
- Redeploy the AgentMarket contract if it was wiped.
- Sign in as a new user and register an agent, to prove it works.

**Checking it is healthy**

- Open launchpad.moi.technology and sign in.
- Look at the stats: registered agents should not be zero.
- Send the Telegram bot a message.

## Presenting the Launchpad

The Launchpad is what new builders see first. It is presented in the MOI Builders intro session, "Your first agent on MOI": the session to send anyone to who has never touched MOI. It ends with the audience launching an agent that lives on chain and messages them on Telegram, with no code.

**The deck**

- In this repo: intro-session/deck. index.html is the deck (11 slides, 1920 by 1080, our branding), MOI_Builders_Intro.pdf the slides-only export. Built with the deck branch of the moi-webinar skill.
- Open index.html in Chrome. Arrow keys or space to move. Press P for the presenter window: the full talk script per slide, the next slide's title and a clock. In Meet, share the deck window and keep the presenter window on your own screen.
- The script lives in the NOTES array at the bottom of index.html, one entry per slide. Edit it there; the README in the folder has the command that regenerates the PDF.
- Every claim in it was read from the Launchpad source on 9 September 2026 (the sign-in message, the registration call, the relay and Telegram rules, the runtime, the AgentMarket logic). Re-check against the current code before presenting again.

**The flow**

1. Welcome: an intro session; newcomers start here, everyone else stays for the second half.
2. The problem: every agent today is a URL plus an API key. Nothing verifiable says who it is, a key hands over everything, and nobody can find or check it.
3. Four ideas, one breath each: participants, interactions, native assets, logics.
4. Why agents belong on MOI: what an agent needs to know about you lives on your account, not in an app's database.
5. The Launchpad: a playground, not the protocol. Pick a template, register, link Telegram.
6. Live demo (below).
7. Two signatures: the sign-in message, free; the registration interaction, paid in fuel. What landed on chain.
8. Where the agent runs: on your own machine, under pm2, with its key. The server is a relay.
9. The marketplace: publish, price it, the AgentMarket logic moves the payment.
10. Full circle: the agent is a participant, registering was an interaction, the payment is a native asset, the registry and the market are logics.
11. Close: go and launch one. A wallet, a Telegram account, ten minutes.

**The live demo cue**

- Slide 6, switch to the browser at launchpad.moi.technology.
- Connect: the wallet pops up with the sign-in message. No transaction, no fee.
- Pick a template, fill the three fields.
- Register: the wallet signs the interaction and pays the fuel. Show the agent id.
- Link Telegram: the bot message arrives.
- Open the agent page, then the explorer for the registration interaction.
- Back to slide 7.

**Before a session**

- A wallet with devnet KMOI and a Telegram account you can show on screen.
- Pick the template in advance, and have one agent already created as the fallback if the live registration fails.
- Check the stats page: "The registry is not answering" means registration will fail. Fix the registry id first (After a devnet reset, above).
- Run through the demo once the day before. Devnet changes.
- Announce it like any Builders session (DEV-WEBINARS.md).

**Recordings and video material**

- The Launchpad launch video and its raw clips are in the Drive folder "Launchpad video" (owner adithya@moinetwork.io): clips 1 to 11, the edits Final video.mp4 and VIDEO.mp4 with and without the outro, and the Builder series and POD subfolders, made with the editor Krishna in August 2026. https://drive.google.com/drive/folders/1wlTotjRXeUpz9UNPp5T5qBBc-8QcZbwr
- Session recordings go to the YouTube playlist (COMMUNITY-CALL.md has the link).

## Claude skill

The **moi-launchpad-ops** skill covers running the Launchpad. After a devnet reset, start with the **moi-devnet-reset** skill, which gives the order of work across every product.

| When | What to tell Claude | What the skill does |
|---|---|---|
| Something looks wrong | "Is the Launchpad healthy?" | Runs a read-only health check on the live site and says what each failure means. |
| Shipping | "Ship this Launchpad change." | Walks the branch, the local checks and the pull request, and says what merging will deploy. |
| A setting or secret | "I need to change this Launchpad setting: ..." | Says where it is set and whether it needs a deploy or a rebuild. It never sees the secret's value. |
| The database | "I need a migration for ..." | Writes the SQL and says when to run it. I run it in Supabase. |
| Devnet reset | "Devnet was reset. What do I redo?" | Confirms the reset, then lists the steps in order. |
| A user reports a problem | "A user says ..." | Finds the cause among the known cases and drafts the reply. |
| A bad deploy | "Roll back the Launchpad." | Gives the rollback steps. |

What the skill never does without my yes: push, merge (a merge deploys), change a secret, run a migration, or touch anything on the server. It never handles a wallet seed phrase.

## Open items

- Phone sign-in (PR #32) merged and deployed on 7 October after Upendhar rotated the registry login token. The QR sign-in is still off because NEXT_PUBLIC_WC_PROJECT_ID was set after that build: run the CI/CD workflow once to switch it on. Test a real scan and a brand-new wallet first.
- Move every secret into a shared vault. Today the server's env file is the only readable copy.
- Transfer the Telegram bot to DevOps or a company Telegram account (steps in the migration list). The Supabase project was transferred on 8 October.
- The live stats page says the registry is not answering (the registry id is stale since the September reset). Registration may fail for new users. Get the current id from the Protocol team and run the reset steps.
- Push the README and handover doc fixes. The ones in the repo still describe Vercel.
- Still unpushed from the fork: the labs folder (app/labs and its API routes) and the one-off chain scripts for clearing stuck nonces, counting installed agents and finding a blocked nonce. Whoever takes over decides what ships and what was scratch.
- Paid agents cannot be switched on through the pipeline: NEXT_PUBLIC_PAYMENTS_ENABLED has no build argument in the Dockerfile or the build workflow. Add one before the AgentMarket contract is redeployed.
- PR #31 (the Launchpad docs hosted on the site at /docs, with the Docs link and llms.txt pointing at it) merged on 12 October. The next CI/CD run deploys it; after that, check launchpad.moi.technology/docs. PR #10 (AgentMarket deploy budget for the storage fund, blocked since August) is still open: close it or keep it with the contract.
