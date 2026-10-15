# Agent Explorer: the app, the index, the registry, the deploy path

Facts are as of 14 October 2026 where a line says so, as of 2026-10-03 where a probe is named, otherwise as of 2026-10-02 (the library's ops research of that date and the previous operator's clone of `sarvalabs/agent-explorer`, whose branch refs were last fetched on 2026-10-02). `ASK: <person>` is defined in `moi-devrel/SKILL.md`. Back to `../GUIDE.md`.

## 1. What it is
A public directory of the agents registered on MOI's on-chain agent registry. People browse agents, owners register and manage theirs from the browser with a wallet over WalletConnect, and an admin wallet marks agents verified. UI: https://agents.moi.technology. API: https://api.agents.moi.technology. Repo: `sarvalabs/agent-explorer` (private, default branch `main`). It is not the Voyage explorer (voyage.moi.technology, repo `sarvalabs/voyage`), which shows interactions and hosts the faucet. No skill covers Voyage yet; ASK: Gokul.

Terms. The index is the Explorer's own MySQL copy of the registry. A reconcile is one pass that reads every agent from the registry and upserts it (since PR #5, merged 7 October 2026). GHCR is GitHub's container image registry, `ghcr.io`. Tesseract, agent registry and logic id are in `moi-devrel/references/glossary.md`.

## 2. The parts
| Part | What it is | Where |
|---|---|---|
| Client | React 19, Vite, React Router 7, TanStack Query. Built into a static image served by nginx. Routes include `/`, `/agents`, `/agents/:agentId`, `/participants/:id`, `/interactions/:hash`, `/admin` | `client/` |
| API server | Express 4 and TypeScript, node 20 image. Serves `/health`, `/registry/agents`, `/admin/*`, and participant, interaction and upload routes | `server/` |
| Indexer | Inside the API process. Listens on the node's WebSocket for new tesseracts, and copies agents from the registry into MySQL. Also indexes participants, sessions and logs for the intelligence logic | `server/src/indexer/` |
| MySQL | Tables `agents`, `participants`, `sessions`, `participant_logs`. Created and extended at every boot by `initSchema()`: `CREATE TABLE IF NOT EXISTS` and guarded `ALTER TABLE ... ADD COLUMN`. Owner: DevOps. Host not recorded | `server/src/db/schema.ts` |
| Registry | The agent registry logic on devnet. Its id changes after a reset. The server reads it through the `js-moi-agent-registry` package (0.3.0-rc1) and `js-moi-sdk` | chain |
| Node | JSON-RPC (`https://dev.voyage-rpc.moi.technology/devnet`) and a WebSocket address that the code hard-codes as a default | chain |

`client/README.md` is the unmodified Vite template. The Explorer's handover doc is `project-handover-docs/AGENT-EXPLORER.md`.

## 3. The index
The `agents` table is a copy of the registry plus two fields the chain does not hold: `verified`, and on PR #5 `verified_by_admin` (NULL means no admin has decided). `GET /registry/agents?owner=&verified=` returns `{agents: [...], total: N}`. Nothing in `server/src` deletes a row (no DELETE, TRUNCATE or DROP on `main` or on PR #5, checked 2026-10-03), so a row that left the chain stays. How the table is filled and how it drifts: `index-sync.md`.

## 4. The registry it reads
- The registry id changes at a devnet reset (`moi-devrel/references/devnet.md`, reset history). Registry `2f3e9469`, which MOI redeployed after the 2026-09-11 wipe, is the one the code pins as of 2026-10-02 (`0x200000002f3e9469...`, still current on 2026-10-14). After a reset the Explorer's id is the source of truth: the Launchpad and the MCP server follow it.
- The package embeds an old id and reads the environment variable `MOI_AGENT_REGISTRY_LOGIC_ID` once, when it loads. Setting the variable later, inside `getRegistryClient()` as `main` did before PR #5, is too late. PR #5 (merged 7 October 2026) pins it at the top of `server/src/config.ts`, which is imported first.
- Where the id sits (grep all of them): `server/src/config.ts`; `client/vite.config.ts` (since PR #5, override name `VITE_MOI_AGENT_REGISTRY_LOGIC_ID`); the example in `server/.env.example`; the workflow build argument `VITE_AGENT_REGISTRY_LOGIC_ID`, which no client code reads. The Launchpad and the MCP server pin it separately: `moi-devnet-reset`.
- A registry read still names a caller account, and the caller must exist on the current chain. Before PR #5, `main` signed as the wallet of `MOI_MNEMONIC`. Since the merge the server uses a read-only signer for `MOI_READ_CALLER_ADDRESS` when no mnemonic is set, and the code never falls back when a mnemonic is set, though `.env.example` says it does.
- The node rejects reads built by `js-moi-sdk` 0.8.0 (the PR #5 commit message, 2026-10-02). Before PR #5, `main` pinned `^0.8.0`; the merge moved server and client to `^0.9.0-rc2` with an override so the registry package accepts it.
- The registry returns at most 25 ids per call (the PR #5 commit message). The unposted draft design says 50 and marks it unconfirmed; ASK: Gokul. Before PR #5, `main` advanced its page by 100 and so skipped ids for any cap below 100; since the merge it advances by what came back.

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
| `origin/main` | PR #5 merged on 7 October 2026 (18:57 UTC), on top of `4458c0d`, 2026-09-24 (PR #3: restyle and registry tracking) | PR #3's admin verify panel and `npm run sync`, plus PR #5: SDK 0.9.0-rc2, id pin, read-only caller, reconcile (schedule, admin trigger, script), host-based verify rule, `verified_by_admin`, Sync button. The older Launchpad card-origin rule and the absence of a scheduled reconcile are history |
| `origin/fix/registry-sync` | `508be01`, 2026-10-02 (PR #5) | The branch of PR #5, merged |
| `fix/launchpad-origins` | closed PR #4 (2026-09-24) | A different design with `LAUNCHPAD_ORIGINS` and `LAUNCHPAD_CONFIRM_ORIGIN`. The 4 October dependency snapshot still lists those names. They are not read by `main` or PR #5 |
Live proof, 14 October 2026: `GET /admin/sync` answers 200 (the reconcile ran: onChain 174, refreshed 174, failed 0, verified 120) and the client holds "Sync Registry Now", so PR #5 is live. On 2026-10-03, before the merge, it answered 404. The API still reports no version or commit, so which commit runs is read from these markers. Index on 14 October: 176 rows, 120 verified, 75 on the retired Launchpad host, 34 with no card.

## 7. Who owns it
What the evidence says. `project-handover-docs/AGENT-EXPLORER.md`: Gokul owns the app code, admin and verification rules; DevOps (Upendhar) the workflow, VM, nginx, SSH key, GHCR token and DNS. The MySQL database is DevOps's. The registry id comes from the Protocol team. Non-merge commits on `origin/main` (`git shortlog -sn --no-merges`, local ref fetched 2026-10-02, read 2026-10-03): Gokul 28, Upendhar 24, the previous operator 8, of 60. The 65 commits on `main` include 5 merge commits, so counting them would credit Gokul with 32 and Upendhar with 25. The previous operator's 1 October count was 62 (28, 24, 10), most likely because it adds the two commits that sit only on `fix/launchpad-origins` (inferred: the sums match). The previous operator wrote the restyle, the registry tracking and the Launchpad verification, and authored PR #5; PR #3 reached `main` as a merge commit under Gokul's name.
Who can act on the VM: Upendhar (DevOps). Nobody else is recorded. `moi-devrel/references/people-and-teams.md` lists as open whether Upendhar or Srikar owns the VM today. ASK: Rahul.

## Not yet known
- Who must approve a merge. No branch protection or required review is recorded. Gokul owns the product (settled 14 October 2026), so ask him.
- Which VM, nginx configuration and MySQL host serve it. ASK: Upendhar. The `DEV` and `TEST` environments exist but are empty (4 October 2026 snapshot).
- Who owns the server's devnet identity (`MOI_MNEMONIC`, `MOI_AGENT_ID`, `MOI_INTELLIGENCE_LOGIC_ID`) and the WalletConnect project. ASK: Gokul.
- PR #5 is merged (7 October 2026). To confirm the state at any time: `gh pr view 5 -R sarvalabs/agent-explorer --json state,mergedAt,headRefOid`.
- Any uptime monitor, alert routing or log retention for the two hosts. None is documented.
