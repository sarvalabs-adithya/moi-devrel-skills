# Explorer settings and secrets, by name

Names only. This file never holds a value, a length or a prefix. Facts are as of 2026-10-02 (updated 2026-10-14 where a line says so) from the workflow file `.github/workflows/build-and-push.yml`, the code and the `server/.env.example` of `sarvalabs/agent-explorer` (the previous operator's clone), and `moi-devrel/references/keys-and-access.md`. Status is TBD for every row: the owner settles access at the end. Never open an `.env` file; an `.env.example` may be read for names. Never ask for a value in chat. If the operator pastes one, say so, tell them to rotate it, and do not repeat it. Claude never handles a recovery phrase, including a throwaway one. `ASK:` is defined in `moi-devrel/SKILL.md`. Back to `../GUIDE.md`.

The workflow declares the GitHub environment `PROD` (Settings, Environments, PROD) and `moi-devrel/references/keys-and-access.md` says the names live there. `project-handover-docs/LIST-OF-DEPENDENCIES.md` (section 10, the 4 October snapshot) agrees: GitHub, Settings, Environments, PROD (5 secrets, 14 variables), plus one repo-level secret, `GH_TOKEN`; the `DEV` and `TEST` environments exist but are empty. Look at the environment first. ASK: Upendhar which level holds which name. Only a repo admin can edit them; the admins of this repo are not recorded. ASK: Rahul.

## 1. Passed by the workflow
| Name | Kind | Reaches | Used for | Who holds it |
|---|---|---|---|---|
| `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_NAME` | variables | Backend container, at runtime | The MySQL connection | DevOps (Upendhar) |
| `DB_PASSWORD` | secret | Backend, runtime | MySQL | DevOps |
| `MOI_RPC_URL` | variable | Backend, runtime | Node JSON-RPC. The code default is `https://dev.voyage-rpc.moi.technology/devnet` | ASK: Upendhar |
| `MOI_MNEMONIC` | secret | Backend, runtime | The server's own devnet wallet. If set, it signs registry reads and never falls back, even when the wallet is gone from the chain | ASK: Gokul |
| `MOI_AGENT_ID`, `MOI_INTELLIGENCE_LOGIC_ID` | secrets (network IDs, not really secret) | Backend, runtime. The second is also a frontend build argument, `VITE_INTELLIGENCE_LOGIC_ID` | The server's agent identity and the intelligence logic. A reset wipes both (inferred) | ASK: Gokul |
| `GH_TOKEN` | secret | The workflow | Login to `ghcr.io` to push and pull images | ASK: Upendhar |
| `SSH_PRIVATE_KEY`, `VM_HOST`, `VM_USER` | secret, variables | The deploy job | The SSH deploy. Plain SSH, not Teleport | DevOps (Upendhar) |
| `VITE_API_BASE_URL`, `VITE_WC_PROJECT_ID`, `VITE_TESSERACT_BASE_URL`, `VITE_MOI_NETWORK`, `VITE_MOI_CHAIN_ID`, `VITE_TRANSACTION_FUEL_LIMIT` | variables | Frontend image, as build arguments | The browser app's API address, WalletConnect project, links to the explorer, network and fuel limit. Fixed at build | A repo admin. The WalletConnect project owner is unknown. ASK: Gokul |
| `VITE_AGENT_REGISTRY_LOGIC_ID` | variable | Frontend build argument | Nothing. No client code reads this name | A repo admin |
The workflow also sets `PORT` itself.

## 2. Read by the code, not passed by the workflow
Defaults apply, so changing the GitHub value does nothing until the workflow is edited.
| Name | Side | Default and effect |
|---|---|---|
| `MOI_AGENT_REGISTRY_LOGIC_ID` | Server | A code default, the registry current at the last edit. PR #5 treats an empty value as unset |
| `MOI_READ_CALLER_ADDRESS` | Server, PR #5 | A code default, the account that imported agents into one registry. Goes stale at the next reset |
| `MOI_WS_URL` | Server | A hard-coded node WebSocket address. If the node moves, the listener fails |
| `MOI_DERIVATION_PATH` | Server | The faucet wallet path (`devnet.md`, derivation paths) |
| `LAUNCHPAD_ORIGIN` | Server, before PR #5 | `https://launchpad.moi.technology`. Empty disables the rule |
| `LAUNCHPAD_HOSTS` | Server, PR #5 | `launchpad.moi.technology` and the retired Launchpad host. Replaces `LAUNCHPAD_ORIGIN` |
| `SYNC_INTERVAL_HOURS` | Server, PR #5 | 4. 0 disables the schedule |
| `PINATA_JWT` | Server | Empty. Pinning a card to IPFS answers an error without it |
| `VITE_PARTICIPANT_BASE_URL`, `VITE_PUBLIC_URL` | Client | Read by pages and the wallet hook, never passed. Links built from the first likely render with `undefined` (inferred) |
| `VITE_MOI_AGENT_REGISTRY_LOGIC_ID` | Client, PR #5 | Read by `vite.config.ts` through `process.env` at build, otherwise a code default |
Names from older designs that nothing reads on `main` or PR #5: `LAUNCHPAD_ORIGINS`, `LAUNCHPAD_CONFIRM_ORIGIN` (the closed PR #4, still listed in the 4 October dependency snapshot), `AUTO_VERIFY_OWNERS`, `LAUNCHPAD_API_KEY`, `LAUNCHPAD_POLL_SECONDS` (removed 2026-09-23). A name nothing reads is ignored without a warning.

## 3. How a change reaches the app
- A server variable reaches the backend only if the workflow's `docker run` block lists it. Adding one is an edit to the workflow (ship it by `ship-a-change.md`).
- A client variable is baked into the image. It needs a Dockerfile `ARG`, a `--build-arg` in the workflow, and code that reads that exact name. A restart changes nothing.
- Values reach the containers only at deploy. After any change, a deploy must run, on a push to `main` or a manual run.
- A variable that is deleted may reach the container as an empty string rather than vanish (inferred from the workflow). On `main`, `config.ts` uses `??`, which keeps an empty string, so an empty `DB_HOST` or `MOI_RPC_URL` would break the server instead of using its default.
- GitHub secrets cannot be read back. A removed container's environment is gone. Keep a copy of any value in an org vault before changing it. ASK: Rahul which vault. Deleting a secret cannot be undone unless someone else holds the value, so ask its owner (section 5) before a deletion.

## 4. The run: change a setting
| # | Kind | Step | Command or where | Done when |
|---|---|---|---|---|
| 1 | READ | Names in the environment. Never run a bare `gh variable list`: it prints values, the VM host among them | `gh variable list -e PROD -R sarvalabs/agent-explorer --json name,updatedAt`; `gh secret list -e PROD -R sarvalabs/agent-explorer --json name,updatedAt` | You see whether the name exists |
| 2 | READ | Which path the name takes: section 1 or 2 | This file | You know if the workflow passes it and if code reads it |
| 3 | EDIT | If the name is not passed, change the workflow, Dockerfile or code | `ship-a-change.md` | A merged change passes it |
| 4 | GATE | Set the value. The operator types a secret at the hidden prompt; Claude never sees or sends it | Secret: `gh secret set NAME -e PROD -R sarvalabs/agent-explorer`. Variable: `gh variable set NAME -e PROD -R sarvalabs/agent-explorer` | The name's `updatedAt` changed |
| 5 | GATE | Deploy so the value reaches the containers | `gh workflow run build-and-push.yml -R sarvalabs/agent-explorer -f branch=main -f environment=PROD` | The run is `success` |
| 6 | VERIFY | The proof below, then the script | `bash "$SKILLS/moi-launchpad-ops/explorer/scripts/explorer-health.sh"` | The proof holds |
Proof per setting: `SYNC_INTERVAL_HOURS`, the boot log line `[reconcile] scheduled every Nh` (Upendhar). `LAUNCHPAD_HOSTS`, `verified` rows after a sync. The registry id, `onChain` in `GET /admin/sync` after a sync. `DB_*`, `/registry/agents` answers 200. A `VITE_*` value, a changed bundle and the behaviour it controls.

## 5. The accounts behind the names
| Account | Behind | Owner |
|---|---|---|
| GitHub org `sarvalabs`, repo `sarvalabs/agent-explorer`, environment `PROD` | Every name above | Org admin. ASK: Rahul |
| GHCR, `ghcr.io/sarvalabs` | `GH_TOKEN`, the two images | DevOps. ASK: Upendhar who holds the GHCR token |
| The VM and its SSH login | `SSH_PRIVATE_KEY`, `VM_HOST`, `VM_USER` | DevOps (Upendhar). Not recorded which VM |
| The MySQL database | `DB_*` | DevOps |
| The server's devnet wallet and agent identity | `MOI_MNEMONIC`, `MOI_AGENT_ID`, `MOI_INTELLIGENCE_LOGIC_ID` | Owner "confirm" in `project-handover-docs/LIST-OF-DEPENDENCIES.md`. ASK: Gokul |
| The WalletConnect (Reown) project | `VITE_WC_PROJECT_ID` | Owner "confirm". ASK: Gokul |
| A Pinata account, if one is used | `PINATA_JWT`, not set by the workflow | Not recorded. ASK: Gokul |
| Admin wallets | the server's admin list (`verify-agents.md`, section 2) | Whoever holds them. ASK: Gokul. Each person uses their own MOI Wallet; there is no key to hand over |

## 6. Names missing from `keys-and-access.md`
That file lists most of the above. It lacks: `MOI_RPC_URL`, `MOI_AGENT_REGISTRY_LOGIC_ID` as a server setting, `MOI_DERIVATION_PATH`, `LAUNCHPAD_ORIGIN`, `VITE_INTELLIGENCE_LOGIC_ID`, `VITE_PARTICIPANT_BASE_URL`, `VITE_PUBLIC_URL`, `VITE_MOI_AGENT_REGISTRY_LOGIC_ID` and `PORT`. ASK: Rahul to add them when access is settled.

## Not yet known
- Who is admin on the repo and can edit the environment. ASK: Rahul.
- The rotation rule for each secret. None is recorded for the Explorer. ASK: Upendhar (DB, SSH, GHCR), Gokul (the devnet identity).
- Whether the production container sets anything beyond the workflow, such as the admin list. ASK: Upendhar.
- The owner of the WalletConnect project behind `VITE_WC_PROJECT_ID`. ASK: Gokul.
