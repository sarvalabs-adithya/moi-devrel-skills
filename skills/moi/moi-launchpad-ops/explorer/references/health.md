# Check the Explorer's health

Facts are as of 2026-10-03 (the probes named below). `ASK:` is defined in `moi-devrel/SKILL.md`. Quote every URL in a shell: zsh reads an unquoted `?` as a pattern and stops with "no matches found". Back to `../GUIDE.md`.

"Up" is not enough. The API's `/health` says ok while the index is frozen, so read the data in each answer as well as the status code. No uptime monitor, alert route or log retention is documented for either host (ASK: Upendhar). No notice of a failed deploy run is recorded for the Explorer (ASK: Upendhar), so look at the Actions tab after every merge.

## 1. The script
`bash "$SKILLS/moi-launchpad-ops/explorer/scripts/explorer-health.sh" [--chain-count N] [--sync-hours H] [--skip-rpc]`
It needs no working copy and no key. It sends GET requests to the site and the API, and one HTTP POST that carries a read-only JSON-RPC call (`net.Version`) to the devnet RPC. It signs and submits nothing, reads and writes no file, times out each call after 15 seconds, and prints hosts, never full URLs. It prints PASS, WARN or FAIL per line and exits 0 with no FAIL, 1 with a FAIL, 2 on bad usage, a bad `EXPLORER_*` address or an internal error (one line, no traceback: treat the result as unknown).
| Level | Means |
|---|---|
| FAIL | An outage: the site or the API is unreachable or not 200, `/health` is not ok, or `/registry/agents` cannot be read. Go to `troubleshoot.md`, section 1 |
| WARN | Up, but something is stale or odd: a clock skew, rows on the retired Launchpad host, no reconcile code deployed, a reconcile that is old or failed, an index that differs from the chain. Go to `index-sync.md` |
| PASS | That check holds. It proves only what its line says |
On 2026-10-03 it printed 4 PASS, 2 WARN, 0 FAIL: the 23 rows on the retired host, and `/admin/sync` 404. That is the baseline until PR #5 is deployed and a sync has run.

## 2. The checks by hand
| # | Check | Command | Healthy answer | Proves | Observed 2026-10-03 |
|---|---|---|---|---|---|
| 1 | The site | `curl -s -o /dev/null -w '%{http_code}\n' https://agents.moi.technology/` | `200` | The frontend container and nginx answer | 200 |
| 2 | The API process | `curl -s https://api.agents.moi.technology/health` | `{"status":"ok","timestamp":<unix seconds>}` | The backend process is up. Nothing about the data | ok |
| 3 | The index | `curl -s https://api.agents.moi.technology/registry/agents` | `{"agents":[...],"total":N}` and N close to the chain's count | MySQL is reachable and the table has rows | total 49 |
| 4 | Verified rows | `curl -s 'https://api.agents.moi.technology/registry/agents?verified=true'` | Launchpad agents appear once a sync has run | The flag, not the audit | total 1 |
| 5 | The reconcile (PR #5) | `curl -s https://api.agents.moi.technology/admin/sync` | `{"running":false,"last":{"trigger":...,"onChain":...,"added":...,"refreshed":...,"failed":0,"verified":...,"error":null}}` | The last sync ran and what it saw | 404, so PR #5 is not deployed |
| 6 | The node | `curl -s -X POST https://dev.voyage-rpc.moi.technology/devnet/ -H 'content-type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"net.Version","params":[]}'` | A `result` such as `"0.13.0"` | The node the indexer reads answers. Compare the version with the release (`moi-devrel/references/devnet.md`) | 0.13.0 |
| 7 | The last deploy | `gh run list -R sarvalabs/agent-explorer --limit 3 --json databaseId,headSha,conclusion,status,createdAt` | `conclusion` is `success` for the latest merge | The build pushed and the VM's `/health` loop passed. A green run is not a live change | not run (needs repo access) |

## 3. On the VM (only Upendhar can)
ASK: Upendhar to run these and paste the output. Do not ask for `docker inspect` output: it prints every environment value, secrets included.
| Command | Healthy |
|---|---|
| The list of running containers, filtered to the Explorer's | Two containers, backend and frontend, both up. Their names end in `-test` in production; ASK: Upendhar for the names |
| The last 100 log lines of the backend container | `[db] Schema ready`, `[indexer] WS connected`, `[indexer] Subscription active, ID:`. After PR #5: `[reconcile] scheduled every 4h` and `[reconcile:schedule] done`, with `added`, `refreshed`, `failed` and `verified` counts |
Bad lines: repeated `[indexer] WS error:` or `[indexer] WS closed`, which means the node's WebSocket address moved or is down; `[reconcile:...] aborted:`; `[registry] GET /agents error:`; `[indexer] Failed to index agent`; `Failed to start server:`. `account not found` among them means the read caller is gone: `troubleshoot.md`.
The deploy job itself asks the backend's `/health` from the VM up to 12 times, 5 seconds apart, and fails the job when it never answers.

## 4. The run: after a deploy, a reset signal or a user report
| # | Kind | Step | Command or where | Done when |
|---|---|---|---|---|
| 1 | READ | All public checks at once | `bash "$SKILLS/moi-launchpad-ops/explorer/scripts/explorer-health.sh"` | You have PASS, WARN and FAIL lines |
| 2 | READ | Read each WARN against section 1 and the symptom table | `troubleshoot.md` | Each WARN has a cause or an owner |
| 3 | READ | The last deploy (check 7) | `gh run list ...` as above | You know whether the latest merge is the one running |
| 4 | READ | If a reset is suspected, the chain's own count | `index-sync.md`, section 4 | Compared, or an ASK to Gokul drafted |
| 5 | GATE | Anything that changes state (a redeploy, a sync, a variable) | The matching runbook | The operator's yes names the action |
| 6 | VERIFY | Run step 1 again after the change | the script | The result is in the hand-back |

## 5. Reading the numbers
- A 200 on the site shows the static frontend only. The page can load with an empty or stale list.
- The `/health` timestamp is the API's own clock in seconds. The script warns when it differs from the machine running it by more than 300 seconds.
- `total` equals the rows in MySQL, not the chain. Rows are never deleted, so `total` above the chain's count means extras, and below it means missing agents.
- A reconcile older than twice its interval means the schedule is not firing. Every deploy restarts the clock, so frequent deploys can starve it.

## Not yet known
- Whether any monitor watches the two hosts, and who gets a failed-run notice. ASK: Upendhar.
- How long the backend's logs are kept. ASK: Upendhar.
- Which commit of `main` is running. The API reports no version. A build id in `/health` would answer it; adding one is a change for the app owner (ASK: Gokul).
