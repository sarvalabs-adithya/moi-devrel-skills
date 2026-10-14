# Env vars, every product

**Status: index.** Checked on 10 October 2026 against each repo's example file, its workflows and its code. The console ownership and the points flagged below were updated on 13 October 2026.

Marketing: The consoles, and who holds them; Dev Webinars and Community Call. Developers: every product section, and Open items.

This is the index. Each product doc keeps its own table; this one puts them side by side, says where every value comes from, and lists the consoles and who holds each login. Names only, never values. Agent Explorer, the Agent dating plugin, the Moinkee NFT Minter and the Contextual Compute website have no section here. Their variables are in LIST-OF-DEPENDENCIES.md, a snapshot from 4 October.

Rules that hold everywhere:

- Production values are GitHub Actions secrets and variables on the deploying repo (Settings, Secrets and variables, Actions). A secret cannot be read back once set. The only readable copy is on the server (ask DevOps) or inside the running container.
- Setting a value deploys nothing. After any change, run the deploy workflow by hand or merge.
- Anything starting NEXT_PUBLIC_ or VITE_ is baked into the build. Changing it needs a rebuild, not a restart, and it reaches the build only if the workflow passes it as a build argument.
- A name the deploy workflow does not pass never reaches the app, whatever GitHub holds.
- Never paste a value into chat, a doc or a commit. New random values come from `openssl rand -hex 32` unless a row says otherwise.
- There is no shared vault. No company password manager or secrets store holds these values, and none of the production secrets sits in DevRel's own password manager. That is an open item on every product.

## The consoles, and who holds them

| Service | What it gives | Where | Who holds the login (October 2026) |
|---|---|---|---|
| GitHub Actions secrets and variables | Every production value | Each repo, Settings, Secrets and variables, Actions | The repo admins. Org-level secrets: the org admins (Rahul, Upendhar) |
| Supabase | Database URLs and keys | supabase.com, the organisation, the project, Settings, API (or Connect for the Postgres URL) | Launchpad and Dataroom: the company organisation (moved 8 October). Points: the points@moinetwork.io account (managed by Sai Kiran; kept there because the company organisation is at its free-plan limit, see POINTS-PROGRAM.md). The website's Supabase project (the old calendar's events and the chatbot's documents) is not recorded; the documents probably sit in the Dataroom's project |
| Google Cloud console | The Points Google **OAuth** client (the "Sign in with Google" credentials) | console.cloud.google.com, APIs and Services, Credentials | The sarvalabsdeveloper@gmail.com account |
| X developer portal | The Points X app (paid API) | developer.x.com | The sarvalabsdeveloper@gmail.com account |
| Discord developer portal | The Points Discord app and bot | discord.com/developers | The sarvalabsdeveloper@gmail.com account |
| BotFather (Telegram) | Bot tokens and usernames | Telegram, @BotFather, /mybots | Launchpad bot: Adithya's Telegram account, transfer pending (steps in MIGRATION-LIST.md). Points bot and the blog channel bot: the sarvalabsdeveloper@gmail.com account |
| Reown (WalletConnect) | Project ids for wallet pairing (Reown runs the relay that connects a phone wallet to a site) | cloud.reown.com, the project, Project ID | Launchpad, MCP, Points: the sarvalabsdeveloper@gmail.com account |
| Resend | Sign-in emails for Points | resend.com, API keys; domain moi.technology verified | The sarvalabsdeveloper@gmail.com account |
| Groq console | The Launchpad server's own key | console.groq.com/keys | No company account exists. The key now set is not a company key; the next owner creates a company key before relying on it |
| Anthropic console, OpenAI platform | Chat and embedding keys for the website and the Dataroom | console.anthropic.com, platform.openai.com | No company account exists. The keys now set for the website and the Dataroom are not company keys; the next owner creates company keys before relying on them |
| **Buffer** | A social media scheduling service; the owner creates API keys | publish.buffer.com | Chandra |
| Mailchimp | The monthly newsletter | mailchimp.com | Vardan |
| Google Analytics and Tag Manager | Measurement | analytics.google.com, tagmanager.google.com | The sarvalabsdeveloper@gmail.com account |
| **Teleport**, the VMs, SSH keys, **GHCR** tokens | Deploy access. Teleport is the secure-access gateway to the servers; GHCR is GitHub's container registry, where the built app images are stored | DevOps | DevOps (Upendhar, Srikar) |
| Cloudflare | DNS zones, including the Contextual Compute website's | dash.cloudflare.com | Company-owned |
| Pinata | **IPFS** pinning, which keeps files online under fixed content addresses (CIDs); the Moinkee NFT Minter's images are pinned here, and Agent Explorer also lists a Pinata account, whose owner is not recorded | pinata.cloud | Adithya's account today; Srikar is creating a company Pinata account to move it to |
| The **devnet** RPC (the shared MOI test network and the address programs use to talk to it), the agent registry id (the on-chain list of registered agents) | Network settings | The Protocol team | Gokul |
| npm | The **MCP** (Model Context Protocol, the standard for plugging tools into AI assistants) package, unpublished | npmjs.com | Nobody yet. Rahul decides the name and the account |

## Agent Launchpad

Repo sarvalabs/moi-agent-launchpad. Values live in that repo's Actions secrets and variables; deploy.yml writes the ones it lists into the env file on the VM (the file the running app reads). NEXT_PUBLIC_ names reach the build only through a build argument in docker-build.yml and an ARG in the Dockerfile; five have one.

| Name | Kind | What it is | Where the value comes from | Set for production |
|---|---|---|---|---|
| SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY | Variable, secret | The database, server side only | Supabase, company organisation, the project, Settings, API | Set; written to the VM |
| SESSION_SECRET | Secret | Signs the session cookie; the Telegram **webhook** secret derives from it when that is unset (a webhook is the address Telegram posts new messages to) | openssl rand -hex 32 | Set; written to the VM |
| AGENT_KEY_ENCRYPTION_SECRET | Secret | Encrypts every stored agent key. Never generate a new one | The VM env file, through DevOps | Set; written to the VM |
| GROQ_API_KEY | Secret | The server's own key, first in the LLM fallback order (the order the app tries the model providers in: Groq, then Gemini, then OpenAI) | console.groq.com | Set; written to the VM |
| GEMINI_API_KEY, OPENAI_API_KEY | Secret | Second and third in the LLM fallback order | Google AI Studio, platform.openai.com | Not passed by the deploy; unset in production |
| TELEGRAM_BOT_TOKEN, TELEGRAM_BOT_USERNAME, TELEGRAM_WEBHOOK_SECRET | Secret, variable, secret | The bot, its username, the webhook check. After changing the webhook secret run setWebhook again | BotFather; the secret with openssl rand -hex 20 | Set; written to the VM |
| ADMIN_ALERT_TELEGRAM_CHAT_ID | Secret | The alert chat | The chat id, from the bot | Read by deploy.yml but not in the repo's secrets list: either an org-level secret or the VM gets an empty value. Confirm |
| MOI_PLATFORM_MNEMONIC | Secret | The funded platform wallet, for registry reads and the heartbeat | DevOps | Same as above: read by deploy.yml, not in the repo list. Confirm |
| MOI_RPC_URL | Variable | The JSON-RPC endpoint; empty means the SDK's devnet default | The devnet RPC address | Set to a non-empty value (the doc said leave it empty). Confirm it points at a host that resolves |
| MOI_AGENT_REGISTRY_LOGIC_ID | Variable | The agent registry. Changes on every devnet reset | Protocol team | No Actions variable exists, so the code default runs. After a reset, create the variable (deploy.yml already reads it) or change the constant in lib/moi/registry.ts |
| MOI_AGENT_MARKET_LOGIC_ID | Variable | The AgentMarket contract | Printed by contracts/agent_market/deploy.mjs | Not passed by deploy.yml; paid agents are off |
| MOI_REGISTRATION_MNEMONIC_1, _2, _3 | Secret | The wallets that activate new users | DevOps. Never copy them around | Set; written to the VM |
| MOI_REGISTRATION_API_URL, MOI_REGISTRATION_API_KEY | Variable, secret | The proxy registration service, not in use | DevOps | Read by deploy.yml, not set, so proxy mode is off |
| CRON_SECRET | Secret | The manual cleanup trigger only | openssl rand -hex 32 | Set; written to the VM |
| INBOX_WAIT_MS | Literal | The agent inbox **long-poll** window (how long an inbox request waits for a message before it returns empty) | Written as 20000 in deploy.yml | In deploy.yml |
| GLOBAL_DAILY_SPEND_CAP_CENTS | Variable | The daily platform spend cap | A plain number | Set, 500. An empty value would read as zero, so never blank it |
| NEXT_PUBLIC_APP_URL | Variable, build | https://launchpad.moi.technology, baked into agent scripts and the registry card | The site's own address | Set; build argument |
| NEXT_PUBLIC_MOI_EXPLORER_URL, NEXT_PUBLIC_WALLET_INSTALL_URL | Variable, build | Explorer and wallet links | Values in .env.example | Set; build argument |
| NEXT_PUBLIC_WC_PROJECT_ID | Variable, build | The phone QR sign-in; empty keeps it off | cloud.reown.com, the project, Project ID | Set on 7 October at 04:48 UTC, after that day's build at 03:15. The phone QR sign-in works (tested 13 October) |
| NEXT_PUBLIC_MOI_CHAIN_ID | Variable, build | The network ID for pairing | moi:14 for devnet | Not set; the code falls back to moi:14 |

Read by the code, not passed by the deploy, so unset in production with their defaults: LLM_MODEL, DAILY_INTERACTION_CAP (40), MAX_AGENTS_PER_USER (off), DISCORD_WEBHOOK_URL (off), MOI_KMOI_ASSET_ID, MOI_POOL_RPC_URL, MOI_READ_CALLER_ADDRESS, MOI_REGISTRATION_GRANT, MOI_REGISTRATION_DERIVATION_PATH, MOI_SKIP_PAYMENT_VERIFY, MOI_VERIFY_REGISTRATION. Four NEXT_PUBLIC_ names have no build argument at all, so setting them changes nothing: NEXT_PUBLIC_DISCORD_INVITE_URL, NEXT_PUBLIC_PAYMENTS_ENABLED (the paid-agent switch), NEXT_PUBLIC_WALLET_VIDEO_URL, NEXT_PUBLIC_GROQ_KEY_VIDEO_URL. Local scripts only: MOI_DEPLOYER_MNEMONIC, MOI_DEPLOYER_SCAN, MOI_DERIVATION_PATH, MOI_SPONSOR_MNEMONIC, MOI_SPONSOR_DERIVATION_PATH.

Deploy and CI only, held by DevOps: GHCR_PAT, TELEPORT_PROXY, TELEPORT_JOIN_TOKEN, VM_HOST, VM_USER.

## Points Program

Repo sarvalabs/moi-project; the branch feature/ci-cd deploys. It has 13 secrets and 20 variables (SOCIAL_AUDIT_BATCH_SIZE among them), and the deploy passes exactly those. The variables are written into the env file on the box, and the secrets go straight into the container. The Docker build gets five of them as build secrets (DATABASE_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET).

| Name | Kind | What it is | Where the value comes from | Set for production |
|---|---|---|---|---|
| DATABASE_URL | Secret | Postgres | Supabase, the Points project, Connect | Set; container and build |
| BETTER_AUTH_SECRET | Secret | Signs sessions; the X token key falls back to it. Replacing it signs everyone out and makes stored X tokens unreadable | openssl rand -hex 32 | Set; container and build |
| BETTER_AUTH_URL | Variable | https://points.moi.technology. Must be https; every provider callback matches it | The site's own address | Set; env file and build |
| GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET | Secret | Google sign-in | Google Cloud console, APIs and Services, Credentials | Set; container and build |
| X_CLIENT_ID, X_TARGET_URL, X_CLIENT_SECRET | Variable, variable, secret | The X task and campaigns; the profile to follow | developer.x.com, the app | Set |
| DISCORD_CLIENT_ID, DISCORD_GUILD_ID, DISCORD_INVITE_URL, DISCORD_CLIENT_SECRET, DISCORD_BOT_TOKEN | Variables and secrets | The Discord task | Discord developer portal | Set |
| TELEGRAM_BOT_USERNAME, TELEGRAM_CHAT_ID, TELEGRAM_INVITE_MODE, TELEGRAM_BOT_TOKEN, TELEGRAM_WEBHOOK_SECRET | Variables and secrets | The Telegram task. Invite mode is direct or join_request. Set the webhook again after changing the secret | BotFather and the group; the secret with openssl rand -hex 32 | Set |
| MOI_NETWORK, REOWN_PROJECT_ID | Variable | Wallet linking. devnet is the only network the code accepts | Reown dashboard, the project | Set |
| MOI_RPC_URL | Variable | Reads from the network for challenges and bounties | https://dev.voyage-rpc.moi.technology/devnet/ | deploy.yml has passed it since PR #22 (merged and deployed 13 October), but the Actions variable is not set as of 13 October. Create the variable, then run the deploy |
| ADMIN_EMAILS | Variable | Who gets the admin pages. The admin_users table on the Points database is empty (13 October), so this variable is the only source of admin access | Comma-separated Google emails of the admins | Set |
| CRON_SECRET | Secret | The job route /api/jobs/maintenance, live (401 without the secret) and called by nothing today; the social audit job is gone | openssl rand -hex 32 | Set |
| VERIFICATION_WINDOW_MINUTES, VERIFICATION_LIMIT_PER_USER, VERIFICATION_LIMIT_PER_IP | Variable | Attempt limits | Plain numbers (10, 6, 30) | Set. The per-address limit only works once CLIENT_IP_HEADER is passed |
| SOCIAL_AUDIT_BATCH_SIZE | Variable | The batch size of the social audit job, which is gone | A plain number (50) | Still set and passed by deploy.yml, but nothing reads it. Remove the variable and its line in deploy.yml |
| RESEND_API_KEY, EMAIL_FROM | Secret, variable | Sign-in emails. Both, or none is sent | resend.com, API keys; MOI Points <no-reply@moi.technology> | Set |

In the template, read by the code, passed by nothing: X_TOKEN_ENCRYPTION_KEY and X_TOKEN_ENCRYPTION_KEY_PREVIOUS (the key falls back to BETTER_AUTH_SECRET), CLIENT_IP_HEADER (nginx must set the header), DATABASE_SSL, PG_POOL_MAX, NEXT_PUBLIC_SITE_URL (falls back to BETTER_AUTH_URL), FAUCET_URL, FAUCET_API_KEY, FAUCET_TOKEN_ADDRESS, FAUCET_VERIFY_MODE (the faucet task is off). Read by the code and in neither: DATABASE_CA_CERT, GIT_SHA (why the health route shows a null sha), ALLOW_INSECURE_AUTH_URL and SKIP_STARTUP_CHECKS (leave unset), MIGRATIONS_DIR (the migration script only).

Deploy and CI only, held by DevOps: GHCR_PAT, TELEPORT_PROXY, TELEPORT_JOIN_TOKEN, VM_HOST, VM_USER.

## MOI Website and Blog

Repo sarvalabs/MOI-Website. Four workflows: deploy.yml (merge to main), preview.yml (pull requests), distribute.yml (announcing a post), social-prepare.yml. The blog builds with no variables. The names below serve the **Express server** (the small Node web server that answers the site's /api routes, chatbot included), the announcement workflow and the deploy, and VITE_CHATBOT_API is baked into the site's build. The chatbot and the Express server stay as they are (decided 13 October). The blog has one optional name, BLOG_ORIGIN, which defaults to https://blog.moi.technology.

| Name | Kind | What it is | Where the value comes from | Set for production |
|---|---|---|---|---|
| SUPABASE_URL, SUPABASE_KEY | Secret | The chatbot's documents and the old calendar's events (the homepage calendar is now a Luma block, PR #60, but the server's calendar routes remain) | Supabase, the project (which one: probably the Dataroom's, confirm), Settings, API | Set; deploy.yml passes them |
| ANTHROPIC_API_KEY, OPENAI_API_KEY | Secret | The chatbot (hidden on the site; the route still calls both). Not company keys | The two consoles; the next owner creates company keys | Set; deploy.yml passes them |
| VITE_CHATBOT_API | Build value | The address the browser calls for the API. Empty sends the chatbot to localhost, so set the origin | https://moi.technology | Set; deploy.yml passes it. The live value is believed to be the dev host; confirm what it holds |
| ADMIN_API_KEY | Secret | The calendar admin routes. When unset, the routes accept a built-in default written in the source, and the repo is public | openssl rand -hex 32 | Not passed by the deploy. Pass it and remove the fallback |
| ALLOWED_ORIGINS, PORT | Variable | The Express server's CORS list and port | Values in .env.example | Not passed by the deploy; set on the server by DevOps, confirm |
| DATA_ROOM_CHAT_URL, DATA_ROOM_API_KEY | Secret | A proxy to the Dataroom chat in api/chat.js, from the Vercel days | The Dataroom | The URL is passed, the key is not. Whether the VM serves that route: confirm, probably not |
| BUFFER_ACCESS_TOKEN, BUFFER_CHANNEL_X, BUFFER_CHANNEL_LINKEDIN, DISCORD_WEBHOOK_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID | Secret | The announcement workflow, one per channel; a missing one skips its channel | Buffer (Chandra creates the token; the channel ids from node scripts/buffer-channels.js), Discord server settings, BotFather | distribute.yml passes them. The three Buffer names are set; for Discord and Telegram this doc says set but MOI-WEBSITE.md says not set. Confirm in the repo's Actions secrets |
| VITE_GA_ID, PUBLIC_GA_ID | Secret | Analytics ids that nothing in the repo reads (Tag Manager measures instead) | The GA4 property | Passed by deploy.yml, read by nothing. Leave |
| TELEPORT_PROXY, TELEPORT_JOIN_TOKEN, TELEPORT_NODE, VM_USERNAME, PREVIEW_VM_HOST, PREVIEW_VM_USER | Secrets and variables | Deploy and preview access | DevOps (Srikar) | Set |

## Dataroom

Repo sarvalabs/moi-dataroom0. It has ten secret names (nine set, one unset: ADMIN_TOKEN) and no variables. deploy.yml passes six into the server script and uses three to reach the VM. The code reads the chat limits, and nothing sets them.

| Name | Kind | What it is | Where the value comes from | Set for production |
|---|---|---|---|---|
| NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY | Public values stored as secrets, baked at build | The database and bucket from the browser | Supabase, company organisation, the project, Settings, API | Set; passed |
| SUPABASE_SERVICE_ROLE_KEY | Secret | The same, server side only | Same page | Set; passed |
| OPENAI_API_KEY | Secret | The document index. Missing, every upload ends failed | platform.openai.com, API keys. Not a company key | Set; passed |
| ANTHROPIC_API_KEY | Secret | The chat (hidden since August 2026) | console.anthropic.com, API keys. Not a company key | Set; passed |
| ADMIN_SECRET | Secret | The admin page. Never leave it empty: an empty value opens the admin to everyone | openssl rand -hex 32. Rotated on 9 October 2026 | Set; passed |
| ADMIN_TOKEN | Secret | A second admin check in the stats route on main. Unset today, and the route then answers any caller; the fix is on the fork branch | Leave unset until the fix lands | Not set |
| CLAUDE_PER_IP_HOURLY_LIMIT, CLAUDE_DAILY_TOKEN_BUDGET, CLAUDE_MAX_INPUT_TOKENS, CLAUDE_MAX_OUTPUT_TOKENS | Variable | Chat limits; defaults 30, 500000, 8000, 2048, reset on restart | Plain numbers | Not set; a line each in deploy.yml is needed before they can be |
| DATAROOM_URL | Variable | The whitepaper script's target; defaults to the live site | Leave unset | Not set |
| VM_HOST, VM_USERNAME, VM_SSH_KEY | Secret | Deploy access | DevOps | Set |

## MCP server

Source sarvalabs/moi-mcp; production deployed from sarvalabs/voyage-api, branch feat/moi-mcp, workflow moi-mcp.deploy.yml. There is no env file on the server: secrets are repository-level secrets on voyage-api (the Voyage backend repo, which runs the deploy), plain values are written inline in the workflow, and only the names the workflow passes reach the processes.

| Name | Kind | What it is | Where the value comes from | Set for production |
|---|---|---|---|---|
| WC_PROJECT_ID | Secret | The Reown project id, the relay identity behind every pairing | cloud.reown.com, the project, Project ID | voyage-api secrets MCP_PROD_WC_PROJECT_ID and MCP_DEV_WC_PROJECT_ID; passed to the write gateway |
| PUBLIC_URL | Inline | The write gateway's exact https origin and OAuth issuer | The host | Written in the workflow |
| MOI_NETWORK, MOI_RPC_URL | Inline | voyage; the read gateway gets the /babylon/ path of dev.voyage-rpc.moi.technology | The workflow | Written in the workflow |
| MOI_DATA_DIR, HOSTED_PORT, PORT, LOG_LEVEL, NODE_ENV | Inline | The data directory, the two ports, the log level, production | The workflow | Written in the workflow |
| MOI_READ_CALLER | Variable | A funded devnet account for read-only simulation; registry reads need it | A devnet account that exists | Not passed. One reason agent lookup fails |
| MOI_AGENT_REGISTRY_LOGIC_ID | Variable | Overrides the registry id | Protocol team, after each reset | Not passed; the code default (stale) runs |
| MOI_LAUNCHPAD_URL | Variable | The Launchpad tools' target; defaults to https://launchpad.moi.technology | The Launchpad's NEXT_PUBLIC_APP_URL | Not passed; the default is right today |
| MOI_SESSION_KEY | Secret | Required at boot once the encryption-at-rest change ships | openssl rand -base64 32 | Not read by master yet. voyage-api already holds MCP_DEV_SESSION_KEY, MCP_PROD_SESSION_KEY and MCP_PREVIEW_SESSION_KEY; the workflow does not pass them |
| REDIS_URL (**Redis** is an in-memory store; here it keeps pairings across restarts), HOSTED_TIMEOUT_MS, MOI_EXPLORER_URL, MOI_MCP_HOME, REQUEST_TIMEOUT_MS, MOI_WC_PARAM_STYLE | Optional | Redis for pairings, call budget, explorer links, local state, local phone wait, payload style | Defaults in the code | Not passed |
| UPSTREAM_READ_TOKEN, NPM_TOKEN | Secret on moi-mcp | The upstream watch's read access to go-moi and cocolang; publishing on a v* tag | A fine-grained GitHub token; the npm account owner | Neither is set. The watch has never read the two private repos |
| TELEPORT_PROXY, TELEPORT_JOIN_TOKEN, MCP_DEV_MACHINE, TELEPORT_PROD_PROXY, TELEPORT_PROD_JOIN_TOKEN, MCP_PROD_MACHINE | Secret on voyage-api | Deploy access to the dev and production VMs | DevOps (Upendhar, Srikar) | Set |

Test and CI names, not production: MOI_E2E, MOI_CANARY_ACCOUNT (the nightly canary does not pass it), TEST_REDIS_URL, DRY_RUN, MOI_MCP_GO_DIR, MOI_MCP_GO_BIN.

## Dev Webinars and Community Call

There is no app, and one key: BUFFER_API_KEY, for the Buffer script that schedules the session posts. The script ships inside the moi-webinar skill and in the webinars repo. The value goes in a gitignored .env at the skill root or the repo root. Chandra, who owns the Buffer organisation, creates the key. It is not the website's BUFFER_ACCESS_TOKEN. Everything else here is a login, not a variable: Luma (event pages and sign-up), Riverside (call recording), Google Meet and YouTube are shared accounts held by Vardan.

## Open items

- No shared vault holds any production secret. This is open on every product.
- No company Groq, Anthropic or OpenAI account exists. The keys now set (Launchpad Groq; website and Dataroom Anthropic and OpenAI) are not company keys. The next owner creates company keys.
- Pinata: the Moinkee files are pinned in the company account (sarvalabsdeveloper@gmail.com) since 14 October 2026. The BotFather transfer of the Launchpad bot is pending (steps in MIGRATION-LIST.md). The npm package has no owner yet: Rahul decides the name and the account.
- Agent Launchpad: confirm ADMIN_ALERT_TELEGRAM_CHAT_ID and MOI_PLATFORM_MNEMONIC (read by deploy.yml, not in the repo's secrets list), and confirm MOI_RPC_URL points at a host that resolves. After the next devnet reset, create the MOI_AGENT_REGISTRY_LOGIC_ID variable or change the constant in lib/moi/registry.ts.
- Points Program: create the MOI_RPC_URL Actions variable, then run the deploy. Remove SOCIAL_AUDIT_BATCH_SIZE and its line in deploy.yml. Pass CLIENT_IP_HEADER so the per-address limit works.
- MOI Website: confirm which Supabase project SUPABASE_URL points at (probably the Dataroom's), what VITE_CHATBOT_API holds (believed to be the dev host), whether the DATA_ROOM_CHAT_URL route is served by the VM (probably not), and whether the Discord and Telegram secrets are set (this doc says set, MOI-WEBSITE.md says not). Confirm what DevOps set for ALLOWED_ORIGINS and PORT. Pass ADMIN_API_KEY and remove the source fallback.
- Dataroom: ADMIN_TOKEN stays unset until the fix on the fork branch lands; the stats route answers any caller until then.
- MCP server: MOI_READ_CALLER and MOI_AGENT_REGISTRY_LOGIC_ID are not passed, which is one reason agent lookup fails. UPSTREAM_READ_TOKEN and NPM_TOKEN are not set, so the upstream watch has never read the two private repos. The workflow does not pass the three session keys voyage-api already holds.
