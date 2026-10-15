# Troubleshoot the Agent Explorer

Facts are as of 2026-10-14 where a row says so, otherwise 2026-10-03 (probes) and 2026-10-02 (research, and the previous operator's clone of `sarvalabs/agent-explorer`). Start with the script, then find the line below. Every fix that changes anything is a GATE (needs the operator's yes naming the action). A VM action is Upendhar's: the operator asks, Claude drafts. `ASK:` is defined in `moi-devrel/SKILL.md`. Back to `../GUIDE.md`.

Reproduce before fixing, and measure the result live before saying it is fixed. This table was built from the products' own messages and commit bodies, not from a log of past support replies, so a row is typical by construction.

## 1. Start here
`bash "$SKILLS/moi-launchpad-ops/explorer/scripts/explorer-health.sh"`
| Output | Meaning | Go to |
|---|---|---|
| FAIL: the site is unreachable, or `GET /` not 200 | The frontend container or nginx is down, or the VM is | Section 2 row 10, then ASK: Upendhar |
| FAIL: the API is unreachable, or `/health` not ok | The backend container is down or crash-looping | Section 2 rows 9 and 10 |
| FAIL: `/registry/agents` HTTP 500 | The database is unreachable or the credentials changed. The answer holds `error` and `detail` | Section 2 row 11 |
| WARN: `/admin/sync` 404 | The reconcile code is not deployed. PR #5 merged on 7 October 2026 and answered 200 on 14 October, so a 404 now means a rollback past PR #5 or a bad deploy | `rollback.md`, then `index-sync.md` |
| WARN: rows on the retired Launchpad host | Old rows. Not new damage | `index-sync.md`, section 3 |
| WARN: reconcile old, failed or aborted | The schedule is not firing, or the registry cannot be read | Section 2 rows 1 to 3 |
| PASS everywhere and a user still reports a fault | Ask for the exact message and the wallet's active account | Section 3 |

## 2. Symptom, cause, fix
Kinds in the Fix column: READ, GATE. The owner of a code fix is Gokul; of anything on the VM, Upendhar.
| # | Symptom | Likely cause (evidence) | Read-only check | Fix |
|---|---|---|---|---|
| 1 | `/health` ok, the list is old or small | No full sync since a reset; an older build than PR #5 is running; the registry id or the SDK is wrong (`index-sync.md`, section 3) | The script; `curl -s -o /dev/null -w '%{http_code}\n' https://api.agents.moi.technology/admin/sync` | `index-sync.md`, section 5 |
| 2 | `account not found` in the backend log | The read caller is gone from the chain. With `MOI_MNEMONIC` set, the server signs as that wallet and never falls back, even if the wallet is wiped. `server/.env.example` says otherwise; the code does not | Upendhar reads the log. Names only: `gh secret list -e PROD -R sarvalabs/agent-explorer --json name` shows whether `MOI_MNEMONIC` exists | GATE, and only after Gokul says who holds that wallet: since PR #5 (merged 7 October 2026), delete the `MOI_MNEMONIC` secret in PROD and redeploy, so the read-only caller is used. GitHub cannot return the value, so a deletion cannot be undone. Keeping the secret needs a funded wallet that exists on the chain. Check `MOI_READ_CALLER_ADDRESS`: its code default is the wallet that imported agents into one registry, so it goes stale at the next reset |
| 3 | `[indexer] WS error:` repeating | The node's WebSocket address moved or is down. The address is a code default and the workflow does not pass it | Upendhar reads the log | GATE: pass `MOI_WS_URL` through the workflow (`settings-and-secrets.md`), or change the default, and redeploy. Do not turn on the library's own `reconnect` option: it leaks until the process runs out of memory, which is why the code reconnects itself |
| 4 | Admin page: "This wallet is not authorized", or 403 `not_an_admin_address` | The wallet's address is not on the server's admin list, or no list is set | `verify-agents.md`, section 2 | ASK: Gokul whether any admin address is set and which belong there. Changing the list is an admin write on production (`../GUIDE.md`, Gates): GATE |
| 5 | Browser registrations land in a dead registry | The client was built with the package's embedded id (before PR #5 `main` had no pin in `client/vite.config.ts`; PR #5 added one, so check the deployed build) | `ship-a-change.md`, section 4 | GATE: ship an id fix, then rebuild the client (`ship-a-change.md`) |
| 6 | Participant links read `undefined` in the address | `VITE_PARTICIPANT_BASE_URL` is read by three pages and never passed (inferred, not checked in a browser) | Open an agent page and read a link | GATE: add a Dockerfile `ARG`, a `--build-arg` and the variable |
| 7 | The wallet will not connect, or the QR does nothing | `VITE_WC_PROJECT_ID` is missing, or the WalletConnect project is gone. Its owner is unknown | `gh variable list -e PROD -R sarvalabs/agent-explorer --json name` (names only: a bare `gh variable list` prints values, VM host included) | ASK: Gokul who owns the project |
| 8 | Rows show a raw id instead of a name | The card host does not answer. The retired Launchpad host stopped serving cards. `main` also blanks stored card fields on a failed fetch | Open the row's `card_uri` | PR #5 (merged) keeps stored fields and retries the other Launchpad host. GATE: run a sync (`index-sync.md`) and check the deployed build |
| 9 | Deploy run red at the build | A type error (`tsc` in the server image) or a lockfile mismatch (`npm ci` in the client image). A variable value with a space would break the unquoted `--build-arg` lines of the workflow (inferred) | The run log | Fix on a branch and ship by `ship-a-change.md` (its GATE steps apply). Production is untouched: a failure before the deploy job leaves the old containers running |
| 10 | Deploy run red at "Deploy to VM" with "Backend failed health check after 60 seconds" | The new backend does not start or cannot reach MySQL. The old containers were removed first, so the API is down | The run log; then the script | GATE: `rollback.md`. ASK: Upendhar to read the backend log |
| 11 | `/registry/agents` answers 500, "Failed to fetch agents" | MySQL unreachable, or credentials changed (`DB_*` values) | The `detail` field of the answer | ASK: Upendhar. The database is DevOps's |
| 12 | The run is green and the site did not change | Nothing in the run proves liveness; or a manual run chose another branch or environment | `ship-a-change.md`, section 3 | Re-run the proof. If the manual run named the wrong branch, `rollback.md` |
| 13 | The scheduled reconcile never fires (since PR #5) | Deploys come more often than the interval, or `SYNC_INTERVAL_HOURS` is 0 | Log: `[reconcile] schedule disabled` or `scheduled every Nh` | GATE: trigger one by hand, `index-sync.md`, section 5, step 7 |
| 14 | A second sync trigger returns the run already in flight | By design: one reconcile at a time | `GET /admin/sync` | Wait for `running` to be false |
| 15 | Admin call 401 or 403 | The table in `verify-agents.md`, section 3 | The page's error text, and the clock of the machine with the wallet | `verify-agents.md`, section 3 |
| 16 | The API answers but a user says their new agent is missing | The listener adds new ids only after a registry interaction reaches it, and a missed event needs a sync | `index-sync.md`, section 4 | `index-sync.md`, section 5 |
| 17 | A merged PR is not live; the deploy run is red at "Login to GHCR" | The `GH_TOKEN` secret (set 31 July) is expired or revoked. Failed 7 October and 14 October; the 24 September run worked. The live site is a build from 8 October, deployed by hand; PR #6 (`aa9488c6`) is merged but not live, and 70 deprecated agents still show as verified | The failing step of `gh run list -R sarvalabs/agent-explorer -L 5` and its log | ASK: Upendhar to replace `GH_TOKEN` (a token that can push and pull packages) and re-run the deploy. Upendhar has been asked (2026-10-14). Do not rebuild by hand without his yes (Fixed on 15 October 2026: DevOps replaced GH_TOKEN, the re-run passed and PR #6 is live; no deprecated agent shows as verified.) |

## 3. A user report
Ask for the exact on-screen message, the page and the wallet's active account. Run the script first: if the product is unhealthy it is not the user's fault. The answers below are typical by construction, not recorded replies. They are drafts for the operator, not text to paste: a reply to a user names no PR number, branch, repo path or unmerged feature (`moi-devrel/SKILL.md`, public text leaks), and promises no fix date.
| Question | Answer |
|---|---|
| "My agent is not in the directory." | New registrations are meant to reach the directory through a listener on the node (presumed working, not observable from outside), and a reconcile runs every 4 hours and by hand (live since PR #5 merged on 7 October 2026). The index showed 176 rows on 2026-10-14 against 174 on chain at the last reconcile. Say that the list can lag the chain by up to one interval, give the date and the count, ask for the agent's id and owner address, and say it has been passed on only after the operator has told Gokul |
| "Why is my Launchpad agent not verified?" | Verification is an admin decision, plus a Launchpad rule that has not reached every row. `verify-agents.md` |
| "Is the Explorer the same as the Voyage explorer?" | No. The Voyage explorer shows interactions and has the faucet. This directory lists agents |
Keep replies short and plain. Say whose side the fault is on, and what was and was not changed.

## 4. Escalate
| To | For | How |
|---|---|---|
| Upendhar | The VM, containers, nginx, MySQL, DNS, TLS, the SSH key, the GHCR token, `docker exec` | One task per message: the problem, the proposed action, how to verify. No labels, no em dashes. Never ask for a secret value. The channel is not fixed. ASK: Upendhar |
| Gokul | The app, the registry, the id, the admin list, pruning, review of PR #5 | Same shape. Channel unknown. ASK |
| Rahul | Whether DevRel may fix it, who approves a merge, access to the repo | Same |
Claude drafts from `moi-devrel/templates/messages.md`; the operator sends. Past DevOps messages worked as short human notes (`moi-devrel/references/people-and-teams.md`).

## 5. Close out
Add the fault to the hand-back with its date, the symptom, the measured cause and the fix. Whether the note also goes into the repo as a "Failures seen so far" file is the operator's call; no such file exists yet.

## Not yet known
- How the production container was started beyond what the workflow passes. ASK: Upendhar.
- Whether any user-facing support channel for the Explorer exists. None is documented.
- The status of the WalletConnect project. ASK: Gokul.
