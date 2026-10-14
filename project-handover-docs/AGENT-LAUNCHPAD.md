# Agent Launchpad

**Status: active.** Live at launchpad.moi.technology. Inactive: paid agents (the **AgentMarket** contract, which moves the payment for a paid agent, is not redeployed). The phone QR sign-in works (tested 13 October 2026).

Video: https://drive.google.com/file/d/1FruKR8k6Wp_rplSFzIE8pZf8OBwBUfSI/view (recorded 12 October 2026).

Marketing: Variables, Process (including Presenting the Launchpad), Open items. Developers: Stack, Env vars, Process, Claude skill, Open items.

The Launchpad is the web app at launchpad.moi.technology where anyone can launch an AI agent on MOI: pick a template, register the agent on chain, and talk to it on Telegram. Adithya built it and DevRel runs it. DevOps owns the server it runs on.

## Stack

| Piece | What it is |
|---|---|
| Next.js 14 + React 18 + TypeScript + Tailwind | The whole product: landing, connect, create, dashboard, agent pages, marketplace, stats, and about 45 API routes |
| Supabase Postgres | All app state, server side only through the service-role key (Supabase's all-access key, never sent to the browser). Twelve SQL migration files in supabase/migrations |
| js-moi-sdk, js-moi-identifiers, js-polo (the encoder for **POLO**, MOI's binary format), js-moi-agent-registry | Chain reads and writes on devnet, in lib/moi |
| AgentMarket contract (a **logic**, MOI's word for a smart contract, written in **Coco**, MOI's contract language) | contracts/agent_market: each paid agent's price and the payment. Not redeployed since the devnet wipes |
| Wallet sign-in | The wallet signs a one-time code, the server issues a session cookie. WalletConnect adds the phone QR sign-in (PR #32; PR #33 lets it work even when the wallet extension is installed, merged 13 October) |
| Telegram through grammy (a Telegram bot library) | @moinetworkbot, the webhook route and account linking. The bot itself is created and managed in **BotFather** (Telegram's own bot for making bots), on Rahul Lenkala's Telegram account since 14 October 2026: that is where the token is reissued |
| Agent runtime | agent-runtime/index.ts bundled into public/runtime.cjs. Users download it and run it themselves; it polls the relay routes. Twelve templates in lib/templates |
| AI keys | Each agent uses its owner's own key (Groq, Google or OpenAI). The server holds no key in use: its shared free tier was retired |
| Docker + GitHub Actions + GHCR + Teleport | One container behind nginx on the DevOps box. Merging to master builds and deploys |
| Cleanup | Runs inside the app every six hours. The cron route guarded by CRON_SECRET is only the manual trigger |
| vitest | 28 test files. The atomicity tests need a database |

No worker runs in production on purpose: it would steal the Telegram webhook and run every agent twice.

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Codebase | DevRel | https://github.com/sarvalabs/moi-agent-launchpad deploys |
| Database (Supabase) | The company Supabase organisation, owned by sarvalabsdeveloper@gmail.com (transferred 8 October) | Holds all app state |
| Telegram bot and the alert chat | Currently Rahul Lenkala's Telegram account | @moinetworkbot delivers agent messages to users. Transferred from Adithya's Telegram account to Rahul (@p2pbuddy) on 14 October 2026; the token and the chat id did not change |
| AgentMarket contract on **devnet** (MOI's shared test network, wiped from time to time) | DevRel | Not redeployed since the devnet wipes, so paid agents are off. The code is there; the next owner redeploys it when it is needed |
| Server, CI/CD, container registry, **Teleport** (the gateway DevOps uses to reach the server) | DevOps | |
| Domain launchpad.moi.technology | DevOps | |
| Registration wallets that activate new users | DevOps | |
| Agent registry on devnet | Protocol team (Gokul) | Its id changes on every devnet reset |

## Env vars

The index across every product, with the consoles and who holds each login, is ENV-VARS.md.
Where they live: production values are GitHub Actions secrets and variables on sarvalabs/moi-agent-launchpad (secrets cannot be read back; the readable copy is the env file on the VM, reached through DevOps). Locally, .env.local copied from .env.example. Anything starting NEXT_PUBLIC_ is baked into the image at build time, so it needs a rebuild, and only the names with a build arg reach the build. A new variable needs a line in deploy.yml, and a new NEXT_PUBLIC_ one also needs an ARG in the Dockerfile and a build arg in the build workflow. Setting a value deploys nothing: run the workflow.

| Variable | What it is | Where the value comes from |
|---|---|---|
| SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY | The database | Supabase dashboard (sarvalabsdeveloper@gmail.com), the project, Settings, API |
| SESSION_SECRET | Signs the session cookie | Generate with: openssl rand -hex 32 |
| AGENT_KEY_ENCRYPTION_SECRET | Encrypts every stored agent key. Never generate a new one: every stored key would be lost | The VM env file, through DevOps |
| MOI_PLATFORM_MNEMONIC | The funded platform wallet, for registry reads and the heartbeat | deploy.yml reads it, but it is not in the repo's secrets list (checked 14 October 2026): an org-level secret (only an org admin can see those), or the VM gets an empty value. Confirm with DevOps. Same for ADMIN_ALERT_TELEGRAM_CHAT_ID |
| MOI_RPC_URL | Empty means the SDK's built-in devnet endpoint. The Actions variable is set to https://dev.voyage-rpc.moi.technology/devnet/, which answers (checked 14 October 2026) | The devnet RPC address |
| NEXT_PUBLIC_APP_URL | https://launchpad.moi.technology. Baked at build | |
| TELEGRAM_BOT_TOKEN, TELEGRAM_BOT_USERNAME, TELEGRAM_WEBHOOK_SECRET, ADMIN_ALERT_TELEGRAM_CHAT_ID | The bot, its webhook and the alert chat. After changing the webhook secret, run setWebhook again or messages stop. Unset, the secret is derived from SESSION_SECRET, so rotating that one would stop Telegram too | BotFather; the secret with openssl rand -hex 20 |
| MOI_AGENT_REGISTRY_LOGIC_ID | The agent registry. The one value that changes after a devnet reset. As of October 2026 no Actions variable exists, so the code default in lib/moi/registry.ts runs; deploy.yml already reads the name, so create the variable at the next reset | Protocol team (Gokul) |
| MOI_AGENT_MARKET_LOGIC_ID | The AgentMarket contract. deploy.yml does not pass it yet | Printed by contracts/agent_market/deploy.mjs |
| MOI_REGISTRATION_MNEMONIC_1, _2, _3 | The fallback for activating a new user's wallet. Since August 2026 new users register on Voyage's own Register Participant page (the Launchpad links there, and Voyage's faucet wallets create and fund the account). The in-page activation with these three wallets stays as a fallback for when Voyage strands a user. MOI_REGISTRATION_API_URL and MOI_REGISTRATION_API_KEY (a proxy mode) are not in use | DevOps. Never copy them around |
| GROQ_API_KEY | Not used. Every agent runs on its owner's own key; the server's shared free tier was retired, so the only route that read this key now answers with an error before calling a model. Still set in Actions | console.groq.com |
| GEMINI_API_KEY, OPENAI_API_KEY | Not used (same retired route). Not passed by the deploy either | |
| CRON_SECRET | The manual cleanup trigger | Generate with: openssl rand -hex 32 |
| INBOX_WAIT_MS, GLOBAL_DAILY_SPEND_CAP_CENTS | The inbox long-poll window (20000, written in deploy.yml) and the daily spend cap (an Actions variable, 500; an empty value reads as zero, so never blank it) | |
| NEXT_PUBLIC_MOI_EXPLORER_URL, NEXT_PUBLIC_WALLET_INSTALL_URL | Explorer and wallet links. Baked at build | Values in .env.example |
| NEXT_PUBLIC_WC_PROJECT_ID, NEXT_PUBLIC_MOI_CHAIN_ID | The phone QR sign-in (PR #32 and #33), works, tested on 13 October 2026. The variable name keeps "CHAIN", but its value is the network ID, and it falls back to moi:14 | cloud.reown.com, the project, Project ID (the Reown projects are under sarvalabsdeveloper@gmail.com); moi:14 |

The example file with comments is .env.example in the repo.

**What to hand over in person**

- Readable only from the VM env file, through DevOps: the Supabase service-role key, AGENT_KEY_ENCRYPTION_SECRET, MOI_PLATFORM_MNEMONIC, TELEGRAM_BOT_TOKEN.
- Safe to rotate instead of copying: SESSION_SECRET, CRON_SECRET, TELEGRAM_WEBHOOK_SECRET.
- Request from DevOps rather than copy: the three registration mnemonics, the Teleport and GHCR credentials, the VM host.

**Read first, in the repo**

- docs/HANDOFF.md, the operator guide, especially its secrets checklist and hosting economics.
- docs/E2E-TESTING.md before any launch.
- supabase/migrations: apply the files in order.

## Process

**Shipping a change**

- Work on a branch.
- Run typecheck and tests by hand. Nothing runs them on a pull request.
- If an agent template or the agent runtime (the one file users download and run on their own laptop) changed, rebuild that file and commit it. The repo serves the built copy.
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

- Get the new agent registry id from the Protocol team (Gokul).
- Update it in the repo variables.
- Run the deploy workflow by hand.
- Check with DevOps that the registration wallets are funded again.
- Redeploy the AgentMarket contract if it was wiped.
- Sign in as a new user and register an agent, to prove it works.

**Checking it is healthy**

- Open launchpad.moi.technology and sign in.
- Look at the stats: registered agents should not be zero.
- Send the Telegram bot a message.

### Presenting the Launchpad

The Launchpad is what new builders see first. DevRel presents it in the MOI Builders intro session, "Your first agent on MOI". Send anyone who has never touched MOI to that session. It ends with the audience launching an agent that lives on chain and messages them on Telegram, with no code.

**The deck**

- In the handover repo (sarvalabs/moi-devrel-skills): skills/moi/moi-webinar/past-sessions/intro-session-deck/. index.html is the deck (11 slides, 1920 by 1080, MOI branding), MOI_Builders_Intro.pdf the slides-only export. Built with the deck branch of the moi-webinar skill.
- Open index.html in Chrome. Arrow keys or space to move. Press P for the presenter window: the full talk script per slide, the next slide's title and a clock. In Meet, share the deck window and keep the presenter window on your own screen.
- The script lives in the NOTES array at the bottom of index.html, one entry per slide. Edit it there; the README in the folder has the command that regenerates the PDF.
- Every claim in it was read from the Launchpad source on 9 September 2026 (the sign-in message, the registration call, the relay and Telegram rules, the runtime, the AgentMarket logic). Re-check against the current code before presenting again.

**The flow**

1. Welcome: an intro session; newcomers start here, everyone else stays for the second half.
2. The problem: every agent today is a URL plus an API key. Nothing verifiable says who it is, a key hands over everything, and nobody can find or check it.
3. Four ideas, one breath each: **participants** (anyone or anything with an identity on MOI: a person, an agent, an app), **interactions** (the signed requests that change state), **native assets** (assets the protocol itself handles, not a contract's bookkeeping) and logics (smart contracts).
4. Why agents belong on MOI: what an agent needs to know about you lives with you, the participant, not in an app's database.
5. The Launchpad: a playground, not the protocol. Pick a template, register, link Telegram.
6. Live demo (below).
7. Two signatures: the sign-in message, free; the registration interaction, paid in **fuel** (the unit that pays for running an interaction). What landed on chain.
8. Where the agent runs: on your own machine, under **pm2** (a Node process manager that keeps it running), with its key. The server is a relay.
9. The marketplace: publish, price it, the AgentMarket logic moves the payment. Paid agents are switched off as of October 2026, so this slide describes the design, not something a visitor can use.
10. Full circle: the agent is a participant, registering was an interaction, the payment is a native asset, the registry and the market are logics.
11. Close: go and launch one. A wallet, a Telegram account, ten minutes.

**The live demo cue**

- Slide 6, switch to the browser at launchpad.moi.technology. The phone QR sign-in works (tested 13 October 2026), so the demo can also be done from a phone.
- Connect: the wallet pops up with the sign-in message. No transaction, no fee.
- Pick a template, fill the three fields.
- Register: the wallet signs the interaction and pays the fuel. Show the agent id.
- Link Telegram: the bot message arrives.
- Open the agent page, then the explorer for the registration interaction.
- Back to slide 7.

**Before a session**

- A wallet with devnet **KMOI** (the network's native token, which pays fuel) and a Telegram account you can show on screen.
- Pick the template in advance, and have one agent already created as the fallback if the live registration fails.
- Check the stats page: "The registry is not answering" means registration will fail. It can also be the RPC rate limit ("Too many requests", seen 14 October), so retry before assuming a stale id. If the id is stale, take the Agent Explorer's current id (After a devnet reset, above).
- Run through the demo once the day before. Devnet changes.
- Announce it like any Builders session (DEV-WEBINARS.md).

**Recordings and video material**

- The Launchpad launch video and its raw clips are in the Drive folder "Launchpad video": https://drive.google.com/drive/folders/1wlTotjRXeUpz9UNPp5T5qBBc-8QcZbwr
- Session recordings go to the YouTube playlist (COMMUNITY-CALL.md has the link).

## Claude skill

The **moi-launchpad-ops** skill covers running the Launchpad. After a devnet reset, start with the **moi-devnet-reset** skill, which gives the order of work across every product.

| When | What to tell Claude | What the skill does |
|---|---|---|
| Something looks wrong | "Is the Launchpad healthy?" | Runs a read-only health check on the live site and says what each failure means. |
| Shipping | "Ship this Launchpad change." | Walks the branch, the local checks and the pull request, and says what merging will deploy. |
| A setting or secret | "I need to change this Launchpad setting: ..." | Says where it is set and whether it needs a deploy or a rebuild. It never sees the secret's value. |
| The database | "I need a migration for ..." | Writes the SQL and says when to run it. DevRel runs it in Supabase. |
| Devnet reset | "Devnet was reset. What do I redo?" | Confirms the reset, then lists the steps in order. |
| A user reports a problem | "A user says ..." | Finds the cause among the known cases and drafts the reply. |
| A bad deploy | "Roll back the Launchpad." | Gives the rollback steps. |

What the skill never does without a yes from DevRel: push, merge (a merge deploys), change a secret, run a migration, or touch anything on the server. It never handles a wallet seed phrase.

## Open items

- The repo's README and docs/HANDOFF.md still describe Vercel. A PR with the fixes was opened on 14 October 2026 (README, HANDOFF, DEPLOY.md and the env examples); merge it.
- Paid agents cannot be switched on through the pipeline: NEXT_PUBLIC_PAYMENTS_ENABLED has no build argument in the Dockerfile or the build workflow. Add one before the AgentMarket contract is redeployed.
