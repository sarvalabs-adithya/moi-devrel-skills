# Env vars

Every environment variable across the products, names only. Production values are GitHub Actions secrets and variables on each product's repo (Settings, Secrets and variables, Actions). GitHub cannot show a secret back once set; changing one deploys nothing until the deploy workflow runs. NEXT_PUBLIC_ and VITE_ values are built into the site, so they need a rebuild.

| Product (repo) | Variable | What it is | Where the value comes from (who holds the login) | In use |
|---|---|---|---|---|
| Launchpad (sarvalabs/moi-agent-launchpad) | SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY | The database | Supabase, the company organisation (sarvalabsdeveloper@gmail.com) | Yes |
| Launchpad | SESSION_SECRET | Signs the session cookie | `openssl rand -hex 32` | Yes |
| Launchpad | AGENT_KEY_ENCRYPTION_SECRET | Encrypts every stored agent key. Never replace it | The server's env file, through DevOps | Yes |
| Launchpad | TELEGRAM_BOT_TOKEN, TELEGRAM_BOT_USERNAME, TELEGRAM_WEBHOOK_SECRET, ADMIN_ALERT_TELEGRAM_CHAT_ID | The bot, its webhook check and the alert chat | BotFather (Rahul Lenkala's Telegram account) | Yes |
| Launchpad | MOI_PLATFORM_MNEMONIC | The platform wallet for registry reads | DevOps | Yes |
| Launchpad | MOI_REGISTRATION_MNEMONIC_1, _2, _3 | Wallets that activate new users, the fallback after Voyage's own registration | DevOps | Yes |
| Launchpad | MOI_RPC_URL | The devnet RPC | https://dev.voyage-rpc.moi.technology/devnet/ | Yes |
| Launchpad | MOI_AGENT_REGISTRY_LOGIC_ID | The agent registry id. Changes after a devnet reset | Protocol team (Gokul). Not set; the code default runs | Default |
| Launchpad | CRON_SECRET | The manual cleanup trigger | `openssl rand -hex 32` | Yes |
| Launchpad | GLOBAL_DAILY_SPEND_CAP_CENTS, INBOX_WAIT_MS | Daily spend cap (500, never blank it) and inbox wait (20000, in deploy.yml) | Plain numbers | Yes |
| Launchpad | NEXT_PUBLIC_APP_URL, NEXT_PUBLIC_MOI_EXPLORER_URL, NEXT_PUBLIC_WALLET_INSTALL_URL | Site, explorer and wallet links | .env.example | Yes |
| Launchpad | NEXT_PUBLIC_WC_PROJECT_ID, NEXT_PUBLIC_MOI_CHAIN_ID | Phone QR sign-in; network ID (defaults to moi:14) | Reown (sarvalabsdeveloper@gmail.com) | Yes |
| Launchpad | GHCR_PAT, TELEPORT_PROXY, TELEPORT_JOIN_TOKEN, VM_HOST, VM_USER | Deploy access | DevOps | Yes |
| Launchpad | GROQ_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY, MOI_AGENT_MARKET_LOGIC_ID, MOI_REGISTRATION_API_URL, MOI_REGISTRATION_API_KEY | Old server AI keys (agents use their owners' own keys), the paid-agent contract (off), the unused registration proxy | | No |
| Points (sarvalabs/moi-project, branch feature/ci-cd) | DATABASE_URL | The database | Supabase, the points@moinetwork.io account (Sai Kiran) | Yes |
| Points | BETTER_AUTH_SECRET, BETTER_AUTH_URL | Signs sessions; the site address (https://points.moi.technology) | `openssl rand -hex 32` | Yes |
| Points | GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET | Google sign-in | Google Cloud console (sarvalabsdeveloper@gmail.com) | Yes |
| Points | X_CLIENT_ID, X_CLIENT_SECRET, X_TARGET_URL | The X task and campaigns | X developer portal (sarvalabsdeveloper@gmail.com) | Yes |
| Points | DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET, DISCORD_BOT_TOKEN, DISCORD_GUILD_ID, DISCORD_INVITE_URL | The Discord task | Discord developer portal (sarvalabsdeveloper@gmail.com) | Yes |
| Points | TELEGRAM_BOT_TOKEN, TELEGRAM_BOT_USERNAME, TELEGRAM_CHAT_ID, TELEGRAM_INVITE_MODE, TELEGRAM_WEBHOOK_SECRET | The Telegram task | BotFather (sarvalabsdeveloper@gmail.com) | Yes |
| Points | MOI_NETWORK, REOWN_PROJECT_ID | Wallet linking (devnet) | Reown (sarvalabsdeveloper@gmail.com) | Yes |
| Points | ADMIN_EMAILS | Who can open the admin page, comma separated | sarvalabsdeveloper@gmail.com, points@moinetwork.io and Harsh Gupta's Gmail today | Yes |
| Points | RESEND_API_KEY, EMAIL_FROM | Sign-in emails | Resend (sarvalabsdeveloper@gmail.com) | Yes |
| Points | CRON_SECRET, VERIFICATION_WINDOW_MINUTES, VERIFICATION_LIMIT_PER_USER, VERIFICATION_LIMIT_PER_IP | The maintenance job route; attempt limits (10, 6, 30) | `openssl rand -hex 32`; plain numbers | Yes |
| Points | MOI_RPC_URL | Chain reads for bounty hash checks. Not set; bounties work without it | https://dev.voyage-rpc.moi.technology/devnet/ | No |
| Points | SOCIAL_AUDIT_BATCH_SIZE | Leftover from a removed job | | No |
| Points | GHCR_PAT, TELEPORT_PROXY, TELEPORT_JOIN_TOKEN, VM_HOST, VM_USER | Deploy access | DevOps | Yes |
| Website (sarvalabs/MOI-Website) | BUFFER_ACCESS_TOKEN, BUFFER_CHANNEL_X, BUFFER_CHANNEL_LINKEDIN | Announcing a post on X and LinkedIn | Buffer (Chandra) | Yes |
| Website | TELEPORT_PROXY, TELEPORT_JOIN_TOKEN, TELEPORT_NODE, VM_USERNAME, PREVIEW_VM_HOST, PREVIEW_VM_USER | Deploy and preview access | DevOps (Srikar) | Yes |
| Website | DISCORD_WEBHOOK_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID | Would post announcements to Discord and Telegram. Not set | | No |
| Website | SUPABASE_URL, SUPABASE_KEY, VITE_CHATBOT_API, ANTHROPIC_API_KEY, OPENAI_API_KEY, DATA_ROOM_CHAT_URL, ADMIN_API_KEY, VITE_GA_ID, PUBLIC_GA_ID, VM_HOST, VM_SSH_KEY | The old chatbot and calendar server (not running), unused analytics ids, the old SSH deploy | | No |
| Dataroom (sarvalabs/moi-dataroom0) | NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY | The database and file bucket | Supabase, the company organisation (sarvalabsdeveloper@gmail.com) | Yes |
| Dataroom | ADMIN_SECRET | The admin page password | Chandrasekhar holds it | Yes |
| Dataroom | OPENAI_API_KEY, ANTHROPIC_API_KEY | Document indexing and the chat (the chat is off) | platform.openai.com, console.anthropic.com. Not company keys | Partly |
| Dataroom | VM_HOST, VM_USERNAME, VM_SSH_KEY | Deploy access | DevOps | Yes |
| MCP server (deployed from sarvalabs/voyage-api) | MCP_PROD_WC_PROJECT_ID, MCP_DEV_WC_PROJECT_ID | The Reown project for wallet pairing | Reown (sarvalabsdeveloper@gmail.com) | Yes |
| MCP server | MOI_READ_CALLER | Any existing devnet account, used as the sender for registry reads | Written in the deploy workflow | Yes |
| MCP server | PUBLIC_URL, MOI_NETWORK, MOI_RPC_URL, ports, log level | Written inline in the deploy workflow | The workflow | Yes |
| MCP server | TELEPORT_PROXY, TELEPORT_JOIN_TOKEN, TELEPORT_PROD_PROXY, TELEPORT_PROD_JOIN_TOKEN, MCP_DEV_MACHINE, MCP_PROD_MACHINE | Deploy access | DevOps (Upendhar, Srikar) | Yes |
| Agent Explorer (sarvalabs/agent-explorer) | DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASSWORD | The MySQL database | DevOps | Yes |
| Agent Explorer | MOI_RPC_URL, MOI_MNEMONIC, MOI_AGENT_ID, MOI_INTELLIGENCE_LOGIC_ID, ADMIN_ADDRESSES | Chain access, the server's wallet and identity, admin wallets | Gokul | Yes |
| Agent Explorer | VITE_ values (API URL, Reown project, network) | The web client's build settings | Gokul; Reown (sarvalabsdeveloper@gmail.com) | Yes |
| Agent Explorer | GH_TOKEN, SSH_PRIVATE_KEY, VM_HOST, VM_USER | Deploy access. GH_TOKEN has expired | DevOps (Upendhar) | Yes |
| Moinkee (sarvalabs/moinkee-nft-minter) | ADMIN_MNEMONIC, NEXT_PUBLIC_ASSET_ID, PINATA_JWT, NEXT_PUBLIC_FOLDER_CID, RECOVERY_SECRET | Minting wallet, the collection, the Pinata key. The site is not hosted | Pinata (sarvalabsdeveloper@gmail.com) | No |
| Contextual Compute site | SUBSCRIBE_WEBHOOK_URL | Where the join form sends emails. Not set | | No |
| Dev Webinars | BUFFER_API_KEY | The webinar skill's Buffer script, in a local .env | Buffer (Chandra) | When posting |
