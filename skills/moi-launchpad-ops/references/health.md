# Health: the checks, what healthy looks like, what each failure means

Facts are as of 2026-10-03: the live answers below were read on that date, the meanings come from the code on `origin/master` (`app/api/stats/route.ts`, `lib/chain-status.ts`, `app/api/marketplace/`) and the research. Run these after every deploy, after any reset signal, and on every user report. No scheduled monitor is on record. Back to `../SKILL.md`.

## Run: check health
| # | Step | Command or action | Done when | Gate |
|---|---|---|---|---|
| 1 | The script | `bash "$SKILLS/moi-launchpad-ops/scripts/launchpad-health.sh"`. Add `--with-rpc` to also read `net.Version` from the public devnet node (one POST of a read method). It reads no file and works from any folder | A `RESULT:` line with the UTC time | read-only |
| 2 | Read every line | Use the table below. A WARN is not a pass: say what it means in the hand-back | Each line has a cause or a reason to ignore it | read-only |
| 3 | Read twice | Chain figures are samples. On a WARN or a surprise, run the script again after 30 seconds | Two reads agree, or the disagreement is written down | read-only |
| 4 | Last deploys | `gh run list -R sarvalabs/moi-agent-launchpad -L 5 --json displayTitle,headSha,conclusion,createdAt` | You know whether a red run is why production is old | read-only |
| 5 | Telegram | The operator runs the self-contained `getWebhookInfo` block in `settings-and-secrets.md` (it asks for the bot token at a hidden prompt) | `url` is the production webhook, no `last_error_message`, `pending_update_count` 0 | OPERATOR |
| 6 | Smoke, 5 minutes | The operator, in a private window, uses the product as an ordinary user: landing page without console errors; sign in with the MOI Wallet extension; open an existing agent (on-chain history shows); open the marketplace; message the bot. Sign-in and the bot message write ordinary session and message rows | All five work | OPERATOR |
| 7 | Inside the box | Only DevOps can read the state of the web container and its last 100 log lines on the VM (ASK: Upendhar how and where). Draft the ask from `moi-devrel/templates/messages.md`; the operator sends it | The container is up and the log holds the boot line | GATE (the message) |
| 8 | Record | The output of step 1 and what you decided, in `../templates/incident-note.md` if anything was wrong | The note exists | local |

## What each script line means
| Line | Healthy (read 2026-10-03) | When it is not |
|---|---|---|
| `site` | `GET /` answers 200 in under a second | FAIL with no answer: DNS, TLS, nginx or the container. Only DevOps can act. 5xx: the proxy is up and the app is not |
| `stats` | `chainStatus=ok`, `activeAgents=33 owners=22 registered=<N> runs=5802`, a chain read under 15 minutes old. `registered` is the chain's count and the others are database counts (definitions under "Reading /api/stats"); `registered=0` is not by itself a reset, because it read 0 and then 6 with `chainStatus` ok on 2026-10-03 | `pending` or `stale`: WARN, the script re-reads after `--wait` seconds. `unreachable`: FAIL, the registry read is failing, usually "account not found" (`troubleshoot.md` rows 9 to 11). A 500 means the database or the environment, not the chain |
| `chain-listing` | 200 with `source` chain and a count | 502 `chain_unreachable` with the real error: FAIL. "Too many requests" in that error is the chain read being rate-limited (seen on 2026-10-03 after several runs within minutes): wait a minute and read again before calling it an incident. 200 with 0 agents: WARN, read again |
| `market` | `onchain` is an object | `onchain=null` is WARN: the market read is unavailable, which is not the same as unlisted. It was null on 2026-10-03 |
| `runtime` | A 12-character version | It is a hash of the served bundle. It changes only when `public/runtime.cjs` changes |
| `rpc` | `net.Version` 0.13.0 on 2026-10-03 | No answer: the node is down or the path moved. Ask Gokul |

## Reading /api/stats
- `chainStatus`: `pending` means the chain has never been read since boot (about a minute after a deploy). `stale` means the last good read is over 15 minutes old or a newer read failed. `unreachable` means it was never read and keeps failing. `ok` means a good read, with `chainAsOf` saying when.
- The refresh runs only when someone asks. After the site has been idle, the first call says `stale`. Call again after 20 to 60 seconds before you call it an incident.
- `registered` is the chain's count of active registry agents whose URL host is a Launchpad host, or null before any read. It is never a database number. `activeAgents` and `owners` are database counts, so they differ from it by design.
- `registered` by state (from `lib/chain-status.ts` and `app/api/stats/route.ts` on `origin/master`, commit `c49afb7` of 2026-09-15, read in the previous operator's clone): with `ok` it is the latest good read; with `stale` it is the last good read, kept with its age (`chainAsOf`) so that a dead registry is not shown as live; with `pending` or `unreachable` it is null, because nothing has been read. A registry that answers but holds none of this Launchpad's agents reads 0 with `ok` (inferred from the count in the code). So `registered=0` alone does not tell an outage or a reset from an empty registry: read `chainStatus`, then `troubleshoot.md` rows 9 to 12. ASK: Gokul.
- Do not quote any of these as "agents on MOI" without saying which one it is and when it was read. On 2026-10-03 within about an hour, `chainStatus` stayed `ok` while `registered` read 0 and then 6, and `?source=chain` listed 8, 4, 0 and 7 agents. The cause is not known. The registry holds an imported snapshot of 144 agents (a comment in `lib/moi/registry.ts`), and `moi-devrel/references/devnet.md` records that the registry call `getAllAgentIds` reverts at about 135 agents and returns an empty list. Whether that explains it is untested. ASK: Adithya, Gokul.
- `GET /api/marketplace` with no `source` is a database index (18 agents on 2026-10-03). It answers in under a second and can show agents from a dead chain. Use `?source=chain` to test the chain. A forced chain read that fails must say so, and it does.

## Checks the script does not make
| Check | How | Healthy |
|---|---|---|
| Cleanup route is deployed and gated | `curl -s -o /dev/null -w '%{http_code}\n' https://launchpad.moi.technology/api/cron/cleanup` with no header | 401. 503 `cron_secret_unset` means the secret never reached the container. The script leaves this route out because it changes data when called with the right header |
| One market listing | `curl -s https://launchpad.moi.technology/api/marketplace/<agent address>/listing` with an address from the chain listing | `onchain` an object. `null` is unavailable, not unlisted |
| Agent long poll | The operator downloads a setup script for a test agent they own (a download, and registering that agent spends devnet funds: both GATE), runs it under pm2 for 3 minutes and reads its log | No 502 or 504. Never recorded as done |
| Reboot, certificate renewal, memory after 24 hours | Post-cutover checks 4.3, 4.6, 4.7 | Never filled in. ASK: Upendhar |
| Fresh-wallet journey | `moi-devrel/test-round`, case list in `moi-devrel/test-round/references/launchpad-pass.md`, with `docs/E2E-TESTING.md` sections 1 and 13 (spends devnet and registration-wallet funds: GATE) | A new wallet reaches an active agent and a receipt with status 0 |

## What is watched, and what is not
- Telegram admin alerts exist for two things only: the spend kill switch, and every registration wallet missing (once an hour per process).
- A red deploy run alerts nobody and leaves the old image serving. Check `gh run list` yourself after every merge.
- No uptime monitor, no log retention policy and no DevOps notification on failure are on record. ASK: Upendhar, Rahul.

## Not yet known
- Why `registered` and the chain listing swing between reads (above).
- Whether the platform wallet is needed for reads. ASK: Adithya.
- Whether any external monitor watches launchpad.moi.technology. ASK: Upendhar.
