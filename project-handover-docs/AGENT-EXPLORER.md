# Agent Explorer

**Status: active, deploys blocked.** agents.moi.technology is live. The build running is from 8 October 2026, deployed by hand. The deploy workflow fails at "Login to GHCR" (GHCR is GitHub's container registry) because its GH_TOKEN secret has expired. So PR #6 (merged 14 October) is not live yet. Upendhar has been asked to replace the token and re-run.

Video: none recorded. The Launchpad demo (AGENT-LAUNCHPAD.md) shows agents landing in the Explorer.

Marketing: How it works, Variables, Open items. Developers: Stack, Variables, Env vars, Process, Claude skill, Open items.

The Agent Explorer is the public directory of agents registered on MOI. It reads the agent registry on devnet and copies it into its own database. It lists every agent with its card and a "verified" mark. It is also where someone can register an agent by hand. Gokul owns the product: the app, its accounts and its decisions go to him. DevOps (Upendhar) owns the server and the deploy. Adithya (DevRel) made PRs #3, #5 and #6.

This doc replaces the Agent Explorer section of the old dependency list (Adithya's notes of 4 October 2026), updated to 14 October.

## How it works

- **From chain to site.** The registry on chain is the source of truth. The server's indexer copies it into MySQL, and the site reads MySQL. Since PR #5 (live since 7 October), the server re-syncs every 4 hours. An admin can also press "Sync Registry Now".
- **After a devnet reset.** The registry gets a new id. Gokul publishes it. You then change it here, in the Launchpad and in the MCP server. The Explorer's id is the one the others follow.
- **Rows are never deleted.** Nothing ever deletes a row. Agents that left the chain, test agents and agents on the retired Launchpad host stay listed until someone prunes the database.
- **What "verified" means.** Rules in the code set the mark. They look at where an agent's card is hosted. The mark does not mean audited or endorsed. On 14 October the index held 176 agents, 120 of them verified.
- **Deprecated agents.** PR #6 hides them and never auto-verifies them. Until it deploys, 70 deprecated agents still show as verified.

## Stack

| Piece | What it is |
|---|---|
| React 19, Vite, React Router 7, TanStack Query | The web client |
| Express 4, TypeScript, MySQL | The API and the indexer. The database host is DevOps' |
| js-moi-sdk 0.9.0-rc2 and js-moi-agent-registry | Chain access: registry reads and writes |
| WalletConnect (Reown) | Wallet sign-in, registering an agent and admin sign-off |
| Pinata | Agent card uploads. No key is passed in production, so uploads answer "not configured" |
| GitHub Actions, Docker, GHCR, nginx | The deploy. GitHub Actions builds two Docker images and pushes them to GHCR. It then replaces both containers on one VM over SSH, behind nginx. Hosts: agents.moi.technology and api.agents.moi.technology |

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Codebase | Gokul (app code, admin, verification rules) | The repo sarvalabs/agent-explorer, private. Merging to main deploys. It has no CODEOWNERS file, and main is not protected. Repo admins: Gokul, Upendhar, chandra, git, sarvalabs-adithya |
| Workflow, VM, nginx, SSH key, GH_TOKEN, DNS, MySQL | DevOps (Upendhar) | Upendhar wrote the CI/CD |
| The agent registry on devnet | Protocol team; Gokul publishes the id | New id after every reset |
| Server devnet wallet and agent identity, the Reown project, the Pinata account | Gokul (he owns the product) | |

## Env vars

The index across every product, with the consoles and who holds each login, is ENV-VARS.md.

Production settings live in GitHub, under sarvalabs/agent-explorer, Settings, Environments, PROD. One secret, GH_TOKEN, is set at repo level instead. To see names and dates, run `gh secret list -R sarvalabs/agent-explorer -e PROD` and `gh variable list -R sarvalabs/agent-explorer -e PROD --json name,updatedAt` (the bare variable list prints values). Locally, copy server/.env.example to server/.env. The client uses client/.env.local.

The server only gets the names that the workflow's docker run passes: ADMIN_ADDRESSES, DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASSWORD, MOI_RPC_URL, MOI_MNEMONIC, MOI_AGENT_ID, MOI_INTELLIGENCE_LOGIC_ID and PORT (5005). Everything else runs on code defaults, including MOI_READ_CALLER_ADDRESS, SYNC_INTERVAL_HOURS, the Launchpad host list and PINATA_JWT. The VITE_ variables are baked into the client image at build time. Changing one needs a deploy, not a restart.

| Name | Kind | What it is |
|---|---|---|
| DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASSWORD | Variables, password a secret | The MySQL database. Ask DevOps |
| MOI_RPC_URL | Variable | The devnet RPC |
| MOI_MNEMONIC, MOI_AGENT_ID, MOI_INTELLIGENCE_LOGIC_ID | Secrets | The server's devnet wallet and agent identity. Last set 17 June 2026, before the 11 September wipe. Ask Gokul whether they still exist on chain |
| ADMIN_ADDRESSES | Variable | Wallets allowed to verify agents and use the admin page. Holds one address (set 7 October 2026) that nobody is recorded as using, so in practice there is no admin (see Open items) |
| VITE_API_BASE_URL, VITE_WC_PROJECT_ID, VITE_TESSERACT_BASE_URL, VITE_MOI_NETWORK, VITE_MOI_CHAIN_ID, VITE_TRANSACTION_FUEL_LIMIT, VITE_AGENT_REGISTRY_LOGIC_ID | Variables, client build | The project id comes from the Reown dashboard |
| GH_TOKEN | Repo secret | GHCR login for the build. Expired: replace it with a token that has write:packages |
| SSH_PRIVATE_KEY, VM_HOST, VM_USER | Secret and variables | The deploy. Ask Upendhar |

## Process

**Shipping a change**

- Work on a branch in the org repo, not a fork. Run tsc and the Vite build, then open a PR to main.
- Nothing runs on a PR: no tests, no lint, no required review. Ask Gokul to review.
- A merge to main is a production deploy. The workflow builds both images and pushes them to ghcr.io/sarvalabs. It then replaces the containers over SSH, old ones first. Their names end in -test. There is no automatic rollback.
- The API reports no version. To prove a client change is live, find a new string in the live script. To prove a server change is live, call an endpoint that it changed.
- A local build may change server/dist, which is tracked in git. Restore it before you commit.

**After a devnet reset**

1. Get the new registry id from Gokul.
2. Change it in the code.
3. Check that the server wallet and agent ids still exist.
4. Deploy.
5. Press "Sync Registry Now".

## Claude skill

The **moi-launchpad-ops** skill (explorer branch) covers health, shipping a change, settings, index sync, verifying agents and rollback. The **moi-devnet-reset** skill covers what to redo after a reset.

| When | What to tell Claude |
|---|---|
| Something looks wrong | "Check the Agent Explorer's health." |
| Shipping | "Ship this change to the Agent Explorer and prove it is live." |
| After a reset | "The devnet was reset. Walk me through the Explorer." |

## Open items

Adithya's work on the Explorer is done. These are notes for Gokul (the product) and DevOps (the server), not DevRel tasks.

- No one is set up as an admin at the moment. The ADMIN_ADDRESSES variable in GitHub holds one wallet address (set 7 October 2026), but nobody is recorded as using it, and the live build was deployed by hand on 8 October. Until someone is an admin, nobody can verify agents or use the admin page.
- The "Sync Registry Now" button on the admin page has not been tested. The automatic sync every 4 hours runs (it reported on 14 October).
- PR #6 goes live once DevOps replaces GH_TOKEN and re-runs the deploy (Upendhar was asked on 14 October). Until then, 70 deprecated agents show as verified.
