# Keep the Explorer index in step with the agent registry

Facts are as of 2026-10-14 where a line says so, otherwise 2026-10-03 (probes of the public API) and 2026-10-02 (research, and the previous operator's clone of `sarvalabs/agent-explorer`). "The index" is the `agents` table that the API serves. "The registry" is the on-chain agent registry. A healthy `/health` says nothing about either. `ASK:` is defined in `moi-devrel/SKILL.md`. Run `git` commands from a working copy of `sarvalabs/agent-explorer`; `curl` and the script need none. Back to `../GUIDE.md`.

## 1. What "in step" means
Every agent the registry lists is a row, each row's profile and card fields match the chain, and `verified` follows the rule in `verify-agents.md`. A row that is not on the chain is out of step too, and nothing removes it.

## 2. How the index is filled
| Path | Trigger | What it does | Limits | Live |
|---|---|---|---|---|
| Full sync, `npm run sync` in `server/` | By hand. The server never does it at boot, so a restart cannot start a full walk | Creates the schema, reads every id from the registry page by page, reads each profile, fetches the card (IPFS gateways, or the URI itself), upserts, then seeds participants and their sessions and logs | Needs the database credentials and a node. On production that means running it inside the backend container (inferred, untested: the image installs dev dependencies). ASK: Upendhar | Available by hand. Causes 2 and 4 below were fixed by PR #5 (merged 7 October 2026) |
| WebSocket listener | Any new tesseract whose text holds the registry id. It waits 2 seconds, lists all ids, and indexes only ids that are not yet rows | Adds new agents | Never refreshes a row, never removes one. Its address is a code default that the workflow does not set. It reconnects every 5 seconds on its own timer, because the library's reconnect leaks until the process runs out of memory (commit `4618591`) | Presumably; not observable from outside |
| Reconcile (PR #5) | Every `SYNC_INTERVAL_HOURS` (default 4, first run one interval after boot), a signed `POST /admin/sync`, and `npm run sync` | Reads every on-chain agent and upserts it. One run at a time. `GET /admin/sync` reports the last run: trigger, `onChain`, `added`, `refreshed`, `failed`, `verified`, `error` | Still deletes nothing. A deploy restarts the container, so deploys more often than the interval mean the schedule never fires | Yes since PR #5 merged on 7 October 2026: `/admin/sync` answered 200 on 14 October (onChain 174, refreshed 174, failed 0, verified 120). It answered 404 on 2026-10-03, before the merge |

## 3. How it falls out of step
| # | Cause | What you see | Evidence |
|---|---|---|---|
| 1 | The registry moved at a devnet reset and the server still reads the old one. The package embeds an old id and reads the variable once at load; `main` sets it too late | Index frozen at old rows, `account not found` in the backend log | Commits `bb5d38e` (2026-09-22) and `508be01` (2026-10-02); reset history in `moi-devrel/references/devnet.md` |
| 2 | The node rejects reads built by `js-moi-sdk` 0.8.0, which `main` pins | Reads fail, so no sync can finish | PR #5 commit message |
| 3 | The read caller does not exist on the chain. `main` signs as the wallet of `MOI_MNEMONIC`; PR #5 never falls back when a mnemonic is set | `account not found` | `server/src/moi/registry.ts` on both branches |
| 4 | `main` advances its page by 100 while the registry returns at most 25 ids per call (50 in the draft, unconfirmed) | A full sync indexes only some ids | `listAllAgentIds` on `main`; PR #5 commit message. ASK: Gokul for the real cap |
| 5 | The WebSocket is down or its address moved | No new rows until someone syncs | `[indexer] WS error:` in the log |
| 6 | Nobody ran a full sync after a reset or downtime | The gap stays | The server never syncs at boot |
| 7 | A row changes on chain (status, card, score) | The row keeps its old values on `main` | The listener only adds unknown ids |
| 8 | A row leaves the chain, or never was on it | It stays, and shows in the list | No DELETE, TRUNCATE or DROP in `server/src` on `main` or PR #5 (2026-10-03) |
| 9 | A card host does not answer | The row has no card, so the page shows a raw id. `main` blanks stored card fields; PR #5 keeps them | `upsertAgent` on both branches |

Causes 1 to 4 and 9 describe `main` before PR #5 merged on 7 October 2026; the merge changed that code (SDK 0.9.0-rc2, id pinned first, read-only caller, page advance by what came back, stored card fields kept), so check which build runs before using them.

Reading of 2026-10-14: 176 rows, 120 verified, 75 on the retired Launchpad host, 34 with no card; the last reconcile saw 174 on chain, refreshed 174, failed 0. So the index is back in step apart from rows that left the chain or sit on the retired host, which nothing deletes. Reading of 2026-10-03, before the merge: 49 rows, 1 verified, 23 on the retired host, 10 with no card, far behind (inferred, not measured; PR #4 had reported 154 on chain, undated, and MOI imported 144 agents on 2026-09-11).

## 4. How to tell
| Check | Command or source | Reading |
|---|---|---|
| Public state | `bash "$SKILLS/moi-launchpad-ops/explorer/scripts/explorer-health.sh"` | WARNs name the stale markers. FAIL means an outage, not staleness |
| Is the reconcile deployed | `curl -s -o /dev/null -w '%{http_code}\n' https://api.agents.moi.technology/admin/sync` | 404: no (a rollback past PR #5, or a bad deploy). 200: read `last` |
| What the server saw on chain at its last run | `curl -s https://api.agents.moi.technology/admin/sync` (since PR #5) | `onChain` against the index total from `/registry/agents` |
| The chain's own count outside a reconcile | A standalone read-only script, `server/check-registry.mjs`, was used before; it is not in the repo: not recorded; ASK: Gokul. The script here cannot read the chain without the SDK | Pass the number to `explorer-health.sh --chain-count N` |
| The chain's count by asking | ASK: Gokul for the registry's agent count at a stated time, and the current registry id | Same |
| Launchpad's own agents on chain | `curl -s https://launchpad.moi.technology/api/stats`, field `registered`. It counts active registry agents on the Launchpad host, from the chain, or null (0 on 2026-10-03) | Compare only with the Launchpad rows. It cannot count other agents |
Do not use the Launchpad's default marketplace list as the chain's list: it is a database index (`moi-launchpad-ops/SKILL.md`, Facts that fail silently, item 8).

## 5. The run: bring the index back in step
Kinds: READ, GATE (needs the operator's yes naming the action), VERIFY. Nothing below is done by Claude without the yes.
| # | Kind | Step | Command or where | Done when |
|---|---|---|---|---|
| 1 | READ | State and markers | `bash "$SKILLS/moi-launchpad-ops/explorer/scripts/explorer-health.sh"` | Output saved as "before" |
| 2 | READ | Is PR #5 deployed | The `/admin/sync` row of section 4 | You know 404 or 200 |
| 3 | READ | The registry id the code pins against the id the protocol team gives | In the working copy: `git grep -n "AGENT_REGISTRY_LOGIC_ID" origin/main -- server client`. Run `git fetch origin` first if `origin/main` may be old (GATE: a download). The current id comes from Gokul; `moi-devnet-reset` owns the order of work across products | The ids agree, or you have the change to make |
| 4 | GATE | If the deployed build is older than PR #5 (merged 7 October 2026), or an id fix is not deployed, ship it first. A sync on the older build cannot finish (causes 1, 2, 4). A schema change migrates the production database at its first boot | `ship-a-change.md` | `/admin/sync` answers 200, or the id fix is live |
| 5 | READ | Decide about rows not on chain. List them from `/registry/agents` and compare with the chain. Pruning is not in PR #5. ASK: Gokul whether to prune, and whether inside the sync or separately (draft question 4) | `curl -s https://api.agents.moi.technology/registry/agents` | A written decision |
| 6 | GATE | Prune, only on Gokul's yes, as a database write by Upendhar, after a backup. No backup is documented. ASK: Upendhar | The database, through Upendhar | Skipped when no decision, or the rows are gone from `/registry/agents` |
| 7 | GATE | Run a reconcile: (a) an admin wallet signs `moi-explorer-admin:sync:<unix seconds>` in the wallet and the operator approves it, Claude never signs; (b) Upendhar runs `npm run sync` in the backend container and pastes the log; (c) wait for the schedule, up to one interval after the last boot | (a) `https://agents.moi.technology/admin`, button "Sync Registry Now"; (b) the VM | `running` is true, then false |
| 8 | VERIFY | Poll until it ends | `curl -s https://api.agents.moi.technology/admin/sync` every 30 seconds | `last.error` null, `failed` 0, `onChain` equals the chain's count |
| 9 | VERIFY | Compare and look | `bash "$SKILLS/moi-launchpad-ops/explorer/scripts/explorer-health.sh" --chain-count N`, then open the Agents page with the filter on All | No stale WARN. Known agents show |
| 10 | READ | Record before and after (totals, verified, date) in the hand-back | | The operator has it |
A full walk takes longer than an HTTP request, which is why `POST /admin/sync` answers 202 and runs in the background. How long it takes is not recorded.

## 6. Who fixes it
| Part | Who | Basis |
|---|---|---|
| Code, the registry, verification rules | Gokul | `project-handover-docs/LIST-OF-DEPENDENCIES.md` section 10: owns the app code, admin and verification rules; the registry |
| The container, its environment, `npm run sync`, the database, a backup | Upendhar | DevOps; deploy is by SSH |
| The new registry id and what changed on chain | The protocol team (Gokul named) | `devnet.md` |
| A signed admin sync or verify | The holder of an admin wallet. Whether any admin address is set in production is unknown. ASK: Gokul | `settings-and-secrets.md` |
| Detecting, measuring, drafting the messages (`moi-devrel/templates/messages.md`), running the gated steps once approved | DevRel, the operator with Claude | Whether DevRel may fix an Explorer fault itself is not settled. ASK: Rahul |

## 7. Wording while the index is stale
Do not write that the Explorer "lists every agent" or give its total as the registry's total. Give the date and say it is the directory's count. Check any public number with `moi-devrel/claim-check`.

## Not yet known
- The real page cap of the registry (25 in the PR #5 commit message, 50 in the draft). ASK: Gokul.
- Whether a full walk can list every agent when the registry holds more than about 135: `moi-devrel/references/devnet.md` says `getAllAgentIds` reverted there and returned an empty list. A walk that ends early looks like a short index. Not re-tested on the current registry; the reconcile of 14 October 2026 reported onChain 174, so a walk past 135 completed then. ASK: Gokul.
- Whether any admin address is set on the production container, so whether option (a) of step 7 can work. ASK: Gokul, Upendhar.
- Whether to prune, how, and whether a database backup exists. ASK: Gokul, Upendhar.
- How long a full reconcile takes on the current registry.
- The chain's own agent count at a stated time: the last reconcile saw 174 on 14 October 2026. ASK: Gokul for the registry's count.
