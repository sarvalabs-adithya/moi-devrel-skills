# Agent Explorer: the app, the index, the registry, the deploy path

Facts are as of 2026-10-03 where a probe is named, otherwise as of 2026-10-02 (the library's ops research of that date and the previous operator's clone of `sarvalabs/agent-explorer`, whose branch refs were last fetched on 2026-10-02). `ASK: <person>` is defined in `moi-devrel/SKILL.md`. Back to `../GUIDE.md`.

## 1. What it is
A public directory of the agents registered on MOI's on-chain agent registry. People browse agents, owners register and manage theirs from the browser with a wallet over WalletConnect, and an admin wallet marks agents verified. UI: https://agents.moi.technology. API: https://api.agents.moi.technology. Repo: `sarvalabs/agent-explorer` (private, default branch `main`). It is not the Voyage explorer (voyage.moi.technology, repo `sarvalabs/voyage`), which shows interactions and hosts the faucet. No skill covers Voyage yet; ASK: Gokul.

Terms. The index is the Explorer's own MySQL copy of the registry. A reconcile is one pass that reads every agent from the registry and upserts it (PR #5 only). GHCR is GitHub's container image registry, `ghcr.io`. Tesseract, agent registry and logic id are in `moi-devrel/references/glossary.md`.

## 2. The parts
| Part | What it is | Where |
|---|---|---|
| Client | React 19, Vite, React Router 7, TanStack Query. Built into a static image served by nginx. Routes include `/`, `/agents`, `/agents/:agentId`, `/participants/:id`, `/interactions/:hash`, `/admin` | `client/` |
| API server | Express 4 and TypeScript, node 20 image. Serves `/health`, `/registry/agents`, `/admin/*`, and participant, interaction and upload routes | `server/` |
| Indexer | Inside the API process. Listens on the node's WebSocket for new tesseracts, and copies agents from the registry into MySQL. Also indexes participants, sessions and logs for the intelligence logic | `server/src/indexer/` |
| MySQL | Tables `agents`, `participants`, `sessions`, `participant_logs`. Created and extended at every boot by `initSchema()`: `CREATE TABLE IF NOT EXISTS` and guarded `ALTER TABLE ... ADD COLUMN`. Owner: DevOps. Host not recorded | `server/src/db/schema.ts` |
| Registry | The agent registry logic on devnet. Its id changes after a reset. The server reads it through the `js-moi-agent-registry` package (0.3.0-rc1) and `js-moi-sdk` | chain |
| Node | JSON-RPC (`https://dev.voyage-rpc.moi.technology/devnet`) and a WebSocket address that the code hard-codes as a default | chain |

`client/README.md` is the unmodified Vite template. No handover document for the Explorer exists besides this branch (`DEPENDENCIES.md` section 11, item 4; the previous operator's file, local to his machine; ASK: Adithya for a copy).

## 3. The index
The `agents` table is a copy of the registry plus two fields the chain does not hold: `verified`, and on PR #5 `verified_by_admin` (NULL means no admin has decided). `GET /registry/agents?owner=&verified=` returns `{agents: [...], total: N}`. Nothing in `server/src` deletes a row (no DELETE, TRUNCATE or DROP on `main` or on PR #5, checked 2026-10-03), so a row that left the chain stays. How the table is filled and how it drifts: `index-sync.md`.

## 4. The registry it reads
- The registry id changes at a devnet reset (`moi-devrel/references/devnet.md`, reset history). Registry `2f3e9469`, which MOI redeployed after the 2026-09-11 wipe, is the one the code pins as of 2026-10-02.
- The package embeds an old id and reads the environment variable `MOI_AGENT_REGISTRY_LOGIC_ID` once, when it loads. Setting the variable later, inside `getRegistryClient()` as `main` does, is too late. PR #5 pins it at the top of `server/src/config.ts`, which is imported first.
- Where the id sits (grep all of them): `server/src/config.ts`; `client/vite.config.ts` (PR #5 only, override name `VITE_MOI_AGENT_REGISTRY_LOGIC_ID`); the example in `server/.env.example`; the workflow build argument `VITE_AGENT_REGISTRY_LOGIC_ID`, which no client code reads. The Launchpad and the MCP server pin it separately: `moi-devnet-reset`.
- A registry read still names a caller account, and the caller must exist on the current chain. `main` signs as the wallet of `MOI_MNEMONIC`. PR #5 uses a read-only signer for `MOI_READ_CALLER_ADDRESS` when no mnemonic is set, and the code never falls back when a mnemonic is set, though `.env.example` says it does.
- The node rejects reads built by `js-moi-sdk` 0.8.0 (the PR #5 commit message, 2026-10-02). `main` pins `^0.8.0`; PR #5 moves server and client to `^0.9.0-rc2` with an override so the registry package accepts it.
- The registry returns at most 25 ids per call (the PR #5 commit message). The unposted draft design says 50 and marks it unconfirmed; ASK: Gokul. `main` advances its page by 100, so it skips ids for any cap below 100; PR #5 advances by what came back.

## 5. The deploy path
Workflow "Build Push and Deploy Agent Explorer", file `.github/workflows/build-and-push.yml`.
| Stage | What happens |
|---|---|
| Trigger | A push to `main` (a merge), or a manual run with inputs `branch` (default `main`) and `environment` (DEV, TEST or PROD, default PROD) |
| Build | Checks out `inputs.branch` or the pushed ref. Builds two images and pushes each as `:<7-character commit id>` and `:latest` to `ghcr.io/sarvalabs`: `agent-explorer-backend` and `agent-explorer-frontend`. The frontend gets its `VITE_*` values as build arguments, so they are fixed at build |
| Deploy | Over SSH (a key held as a secret, not Teleport): logs in to GHCR, pulls both `:latest` images, removes the old containers, starts the new ones with `--restart unless-stopped`, then asks the backend's `/health` from the VM up to 12 times, 5 seconds apart. If it never answers, the job fails. Nothing rolls back |
| Containers | One per image. Their names end in `-test`, in production too. ASK: Upendhar for the names |
| Server environment | Only the names listed in `settings-and-secrets.md`, section 1, reach the backend |
| Time | 1.8 to 2.4 minutes for the successful runs on 2026-06-22 and 2026-09-24; one older run took 8.8 minutes |
The job sits behind the GitHub environment `PROD`. The workflow runs no tests and no lint, and a pull request triggers nothing.

## 6. What is on which branch (refs as of 2026-10-02)
| Branch | Commit | What it holds |
|---|---|---|
| `origin/main` | `4458c0d`, 2026-09-24 (PR #3: restyle and registry tracking) | Admin verify panel, a Launchpad rule that verifies an agent whose card sits on `LAUNCHPAD_ORIGIN` and is served, `npm run sync`, no scheduled reconcile |
| `origin/fix/registry-sync` | `508be01`, 2026-10-02 (PR #5, open as of 2026-10-02) | SDK 0.9.0-rc2, id pin, read-only caller, reconcile (schedule, admin trigger, script), host-based verify rule, `verified_by_admin`, Sync button |
| `fix/launchpad-origins` | closed PR #4 (2026-09-24) | A different design with `LAUNCHPAD_ORIGINS` and `LAUNCHPAD_CONFIRM_ORIGIN`. DEPENDENCIES.md still lists those names. They are not read by `main` or PR #5 |
Live proof (2026-10-03): `GET /admin/sync` answers 404, so PR #5 is not deployed. The API reports no version or commit, so which commit of `main` runs the server is not readable from outside. The client is: its public script held the string "Install the MOI wallet to connect", which only the PR #3 restyle added, and not "Sync Registry Now", which only PR #5 adds (read 2026-10-03). So the client is at PR #3 or later and is not PR #5.

## 7. Who owns it
What the evidence says. DEPENDENCIES.md section 11 (the previous operator's file of 2026-10-01; local to his machine, not in git; ASK: Adithya for a copy): "Gokul owns the app and the registry; Upendhar the CI/CD." The MySQL database is DevOps's. The registry id comes from the Protocol team. Non-merge commits on `origin/main` (`git shortlog -sn --no-merges`, local ref fetched 2026-10-02, read 2026-10-03): Gokul 28, Upendhar 24, the previous operator 8, of 60. The 65 commits on `main` include 5 merge commits, so counting them would credit Gokul with 32 and Upendhar with 25. DEPENDENCIES.md counts 62 (28, 24, 10) most likely because it adds the two commits that sit only on `fix/launchpad-origins` (inferred: the sums match). The previous operator wrote the restyle, the registry tracking and the Launchpad verification, and authored PR #5; PR #3 reached `main` as a merge commit under Gokul's name.
Who can act on the VM: Upendhar (DevOps). Nobody else is recorded. `moi-devrel/references/people-and-teams.md` lists as open whether Upendhar or Srikar owns the VM today. ASK: Rahul.

## Not yet known
- Whether DevRel owns the Explorer, and who must approve a merge. No branch protection or required review is recorded. ASK: Rahul, then Gokul.
- Which VM, nginx configuration and MySQL host serve it, and whether the `DEV` and `TEST` environments exist. ASK: Upendhar.
- Who owns the server's devnet identity (`MOI_MNEMONIC`, `MOI_AGENT_ID`, `MOI_INTELLIGENCE_LOGIC_ID`) and the WalletConnect project. ASK: Gokul.
- Whether PR #5 is still open and unchanged. A read, no fetch needed: `gh pr view 5 -R sarvalabs/agent-explorer --json state,mergedAt,headRefOid`.
- Any uptime monitor, alert routing or log retention for the two hosts. None is documented.
