# Agent Explorer

**Status: active, deploys blocked.** agents.moi.technology is live, but the build running is from 8 October 2026 (deployed by hand). The deploy workflow fails at "Login to GHCR" because its GH_TOKEN secret has expired, so PR #6 (merged 14 October) is not live yet. Upendhar has been asked to replace the token and re-run.

Video: none recorded. The Launchpad demo (AGENT-LAUNCHPAD.md) shows agents landing in the Explorer.

Marketing: How it works, Open items. Developers: Stack, Variables, Env vars, Process, Claude skill, Open items.

The Agent Explorer is the public directory of agents registered on MOI. It reads the agent registry on devnet, copies it into its own database, and lists every agent with its card and a "verified" mark. It is also where someone can register an agent by hand. Gokul owns the app; DevOps (Upendhar) owns the server and the deploy. Adithya made PRs #3, #5 and #6. Whether DevRel owns the Explorer is not settled: ask Rahul.

This doc replaces the Agent Explorer section of the old dependency list (Adithya's notes of 4 October 2026), updated to 14 October.

## How it works

- The registry on chain is the source of truth. The server's indexer copies it into MySQL, and the site reads MySQL. Since PR #5 (live since 7 October) the server re-syncs every 4 hours, and an admin can press "Sync Registry Now".
- After a devnet reset the registry gets a new id. Gokul publishes it; it has to be changed here, in the Launchpad and in the MCP server. The Explorer's id is the one the others follow.
- Nothing ever deletes a row. Agents that left the chain, test agents and agents on the retired Launchpad host stay listed until someone prunes the database.
- "Verified" is set by rules in the code that look at where an agent's card is hosted. It does not mean audited or endorsed. On 14 October the index held 176 agents, 120 of them verified.
- Deprecated agents: PR #6 hides them and never auto-verifies them. Until it deploys, 70 deprecated agents still show as verified.

## Stack

- Web client: React 19, Vite, React Router 7, TanStack Query.
- API and indexer: Express 4, TypeScript, MySQL (the database host is DevOps').
- Chain: js-moi-sdk 0.9.0-rc2 and js-moi-agent-registry for registry reads and writes.
- WalletConnect (Reown) for wallet sign-in, registering an agent and admin sign-off.
- Pinata for agent card uploads, but no key is passed in production, so uploads answer "not configured".
- Deploy: GitHub Actions builds two Docker images, pushes them to GHCR, then replaces both containers on one VM over SSH, behind nginx. Hosts: agents.moi.technology and api.agents.moi.technology.

## Variables

| What | Owner | Notes |
|---|---|---|
| The repo sarvalabs/agent-explorer (private, main deploys) | Gokul (app code, admin, verification rules) | No CODEOWNERS, main not protected. Repo admins: Gokul, Upendhar, chandra, git, sarvalabs-adithya |
| Workflow, VM, nginx, SSH key, GH_TOKEN, DNS, MySQL | DevOps (Upendhar) | Upendhar wrote the CI/CD |
| The agent registry on devnet | Protocol team; Gokul publishes the id | New id after every reset |
| Server devnet wallet and agent identity, the Reown project, the Pinata account | Not settled; ask Gokul | Move them to a shared vault |

## Env vars

Production settings live in GitHub: sarvalabs/agent-explorer, Settings, Environments, PROD, plus one repo-level secret, GH_TOKEN. Names and dates: gh secret list -R sarvalabs/agent-explorer -e PROD and gh variable list -R sarvalabs/agent-explorer -e PROD --json name,updatedAt (the bare variable list prints values). Locally, copy server/.env.example to server/.env; the client uses client/.env.local.

The server only gets the names the workflow's docker run passes: ADMIN_ADDRESSES, DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASSWORD, MOI_RPC_URL, MOI_MNEMONIC, MOI_AGENT_ID, MOI_INTELLIGENCE_LOGIC_ID and PORT (5005). Everything else runs on code defaults, including MOI_READ_CALLER_ADDRESS, SYNC_INTERVAL_HOURS, the Launchpad host list and PINATA_JWT. The VITE_ variables are baked into the client image at build time, so changing one needs a deploy, not a restart.

| Name | Kind | What it is |
|---|---|---|
| DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASSWORD | Variables, password a secret | The MySQL database. Ask DevOps |
| MOI_RPC_URL | Variable | The devnet RPC |
| MOI_MNEMONIC, MOI_AGENT_ID, MOI_INTELLIGENCE_LOGIC_ID | Secrets | The server's devnet wallet and agent identity. Last set 17 June 2026, before the 11 September wipe. Ask Gokul whether they still exist on chain |
| ADMIN_ADDRESSES | Variable | Wallets allowed to verify agents. Set 7 October and passed by the workflow |
| VITE_API_BASE_URL, VITE_WC_PROJECT_ID, VITE_TESSERACT_BASE_URL, VITE_MOI_NETWORK, VITE_MOI_CHAIN_ID, VITE_TRANSACTION_FUEL_LIMIT, VITE_AGENT_REGISTRY_LOGIC_ID | Variables, client build | The project id comes from the Reown dashboard |
| GH_TOKEN | Repo secret | GHCR login for the build. Expired: replace with a token that has write:packages |
| SSH_PRIVATE_KEY, VM_HOST, VM_USER | Secret and variables | The deploy. Ask Upendhar |

## Process

1. Work on a branch in the org repo (no fork), run tsc and the Vite build, and open a PR to main. Nothing runs on a PR: no tests, no lint, no required review. Ask Gokul to review.
2. A merge to main is a production deploy. The workflow builds both images, pushes them to ghcr.io/sarvalabs and replaces the containers over SSH (their names end in -test), old ones first, with no automatic rollback.
3. The API reports no version. Prove a client change is live by finding a new string in the live script. Prove a server change through an endpoint it changed.
4. After a devnet reset: get the new registry id from Gokul, change it in the code, check the server wallet and agent ids still exist, deploy, then press "Sync Registry Now".
5. If a local build changes server/dist (it is tracked), restore it before committing.

## Claude skill

moi-launchpad-ops, explorer branch: health, shipping a change, settings, index sync, verifying agents and rollback. moi-devnet-reset covers what to redo after a reset.

- "Check the Agent Explorer's health."
- "Ship this change to the Agent Explorer and prove it is live."
- "The devnet was reset. Walk me through the Explorer."

## Open items

- Replace GH_TOKEN and re-run the deploy so PR #6 goes live (asked of Upendhar, 14 October). Until then 70 deprecated agents show as verified.
- Security, as of 4 October: some server routes need no sign-in, and a test script in server/ has a recovery phrase written in it, on every branch. Env files were committed on 2 April 2026 and deleted soon after; they stay in git history. No fix exists. Treat that wallet and those files as exposed, and raise it with Gokul.
- Pass PINATA_JWT, or Register an Agent cannot upload a card.
- Prune the index (old-chain, test and retired-host rows): a database write by Upendhar after a backup, with Gokul's yes. No backup is on record.
- Settle the owners of the server wallet, the Reown project, the Pinata account and GH_TOKEN, and move the secrets to a shared vault.
- Add a PR check and write down a rollback. Fill or delete the empty DEV and TEST environments.
