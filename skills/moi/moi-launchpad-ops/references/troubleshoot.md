# Troubleshoot: symptom, cause, fix

Facts are as of 2026-10-03 (updated 2026-10-14 where a row says so), from the recorded incidents (commit ids and dates are given), the code on `origin/master` and the research. Start with the health script (`health.md` step 1), find the row by what you see, run the read-only check first, then the fix. A fix that changes anything is marked GATE and needs the operator's yes. `OPERATOR` means the operator types it. VM work is DevOps: draft the message from `moi-devrel/templates/messages.md`; the operator sends it. The app now shows machine codes and wallet errors verbatim, so the exact on-screen message usually names the cause: ask for it. Back to `../SKILL.md`.

## A. The site and the deploy
| # | You see | Read-only check first | Cause | Fix, then verify |
|---|---|---|---|---|
| 1 | `site` FAIL, no answer | `gh run list -R sarvalabs/moi-agent-launchpad -L 3`: did a deploy just run or fail? | DNS, TLS, nginx or the container. Only DevOps can act | GATE: message Upendhar with the script output and the last run. If a deploy just ran, `rollback.md`. Verify with the script |
| 2 | `site` 5xx or nginx 502 or 504 | The script's `stats` line; the last run | The container is down, restarting or still starting (allow about a minute after a deploy) | Wait a minute, then as row 1 |
| 3 | `/api/stats` answers 500, or DevOps reports the container restarting in a loop | Ask DevOps for the web container's last 100 log lines | A 500 usually means a required value is missing or the database is unreachable: the code checks values per request and fails closed ("Set TELEGRAM_WEBHOOK_SECRET (or SESSION_SECRET)", "cron_secret_unset", "SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY not set"). A restart loop is not explained by those checks, which run per request and not at boot; its cause is unknown (ASK: Upendhar for the log) | GATE: set the missing secret (`settings-and-secrets.md`) and deploy. A rollback does not help if the secret was lost |
| 4 | Run red at `npm ci` with ERESOLVE | `gh run view <id> -R sarvalabs/moi-agent-launchpad --log-failed` | The registry package's SDK peer clashes with the root SDK (e640338, 2026-09-14: every run after PR #24 failed until PR #27 merged five minutes later) | Keep the `overrides` entry in `package.json`. Prove it with `rm -rf node_modules && npm ci`. Ship through `ship-a-change.md` |
| 5 | Run red at the Docker build; Next tries to prerender `/api/stats` | Same log | `export const dynamic = "force-dynamic"` was lost in that route (c69470f) | GATE: restore the line through `ship-a-change.md` |
| 6 | Run red: "NEXT_PUBLIC_APP_URL must be the public https origin" | Same log; `gh variable list -R sarvalabs/moi-agent-launchpad --json name,updatedAt` | The variable is unset or not `https://` | GATE: `settings-and-secrets.md`. Never point it at localhost |
| 7 | Merged, run green, nothing changed | `gh run list`; the `runtime` version if you changed the bundle | The run was for another branch or commit; the change was not in the image; an older run finished last (possible, inferred: no `concurrency` setting) | GATE: a manual run of the workflow on `master`. Ask DevOps which image tag runs |
| 8 | Run red at a Teleport, GHCR login or `tsh` step | The log for the failed step | A DevOps credential expired or changed (inferred from the steps) | GATE: message Upendhar. Do not try to fix a credential yourself |

## B. The chain side
| # | You see | Read-only check first | Cause | Fix, then verify |
|---|---|---|---|---|
| 9 | `stats` `unreachable` or `stale` with "account not found" in `chainError` | Script with `--with-rpc`; compare the id in `lib/moi/registry.ts` on `master` with the id the protocol team published (ASK: Gokul) | A devnet reset wiped the registry, or the registry id is wrong | `moi-devnet-reset` owns the sequence. Launchpad side: "Run: when the cause is a reset" below |
| 10 | `chain-listing` 502 `chain_unreachable` | Same | Same, or the RPC rate limit: "Too many requests" in the error or in `chainError` is the node refusing a burst of reads, not an outage (seen 2026-10-03, and on 2026-10-14 when 144 of 174 agent profile reads failed that way). The default listing (no `source`) hides it | Wait a minute and read again; otherwise as row 9 |
| 11 | `stats` says `stale` once, on an idle site | Run the script again after 30 seconds | The refresh runs only on request | None if the second read is `ok` |
| 12 | `chain-listing` shows 0 agents, or counts and `registered` swing between reads | Read three times, 30 seconds apart; note the times | Unknown (see `health.md`). The registry holds an imported snapshot of 144 agents (a database count such as `activeAgents` is a different number). The registry call `getAllAgentIds` is recorded as running out of meter at about 135 agents in August and returning an empty list. 144 is above that, so it may apply, but nobody has tested it on this registry | Do not fix by guessing. ASK: Gokul. Do not quote the numbers publicly |
| 13 | Market `onchain=null`, or paid routes answer `payments_disabled` | Read one listing (`health.md`) | Paid agents are off: the AgentMarket contract is not redeployed (fact as of 13 October 2026) and the payments switch has no build argument | Not an incident. Turning payments on needs a redeployed contract and a build argument for `NEXT_PUBLIC_PAYMENTS_ENABLED` first: operator task, row R5 below |

## C. Wallets and sign-in
| # | You see | Read-only check first | Cause | Fix, then verify |
|---|---|---|---|---|
| 14 | Activation answers 503 `faucet_unavailable` and the admin gets an alert | Script: if `stats` is fine, the chain is alive | All three registration wallets are missing from the chain. The user did nothing wrong | `moi-devnet-reset`; row R3 below |
| 15 | Activation answers 502 `registration_reverted` | Ask the user for the message; DevOps can read the log line | The network rejected the setup: a grant under 1 KMOI, a wrong callsite, or an SDK mismatch (PR #30, 2026-09-15) | Check `MOI_REGISTRATION_GRANT` is unset or at least 1 KMOI and the SDK is current. GATE: fix through `ship-a-change.md` |
| 16 | The message "The registration wallets are out of KMOI" | Ask DevOps for the wallet balances | The funded wallets ran dry | DevOps or the wallet holder tops up. ASK: Upendhar who holds them |
| 17 | New wallet: "couldn't retrieve nonce" | Ask for the wallet address; the user sees it in the extension | A new wallet is only a keypair. The chain has never heard of it, so the extension refuses to sign | Tell the user to click Connect on `/connect`: the page detects a new wallet and shows "One-time wallet setup" (wording in `support.md`; the connect page wording changed after 13 October (one-time wallet setup, Register it on Voyage, Come back here): confirm with a real sign-in before quoting it) |
| 18 | "invalid sender's signature", or a purchase blocked after switching accounts | Ask which account the extension shows | The wallet's active account differs from the signed-in account. The most common confusing failure | Log out and reconnect with the matching account |
| 19 | A user on a phone cannot connect | Ask the device, the browser and the exact message | The phone QR sign-in works (PR #32, 7 October 2026; PR #33, 13 October, which makes it work even when the extension is installed; tested 13 October). A failure is a real fault, for example a wrong or missing `NEXT_PUBLIC_WC_PROJECT_ID`, which is baked at build | Walk them through the QR sign-in on `/connect`; if it fails, check the two `NEXT_PUBLIC_` values in `settings-and-secrets.md` |

## D. Telegram and agents on user machines
| # | You see | Read-only check first | Cause | Fix, then verify |
|---|---|---|---|---|
| 20 | Telegram stops delivering | OPERATOR: `getWebhookInfo` (`settings-and-secrets.md`). Look for `last_error_message` such as 401 | The webhook secret does not match, or something deleted the webhook (a running worker would) | GATE, OPERATOR: `setWebhook` with the current secret. Check nobody runs `npm run worker` against production |
| 21 | An agent's log shows 502 or 504 on its polls | Ask for the log | The risk named in post-cutover check 2.2: nginx's read timeout shorter than the 20 second hold. It was never observed or ruled out | GATE: message Upendhar to check and raise it. Every installed agent is affected until then |
| 22 | An agent behaves old, or errors after a provider change | The `runtime` version versus what the agent logs | The code of an installed copy never updates itself. Its log says when it is out of date and prints the update line | The owner runs that line (it fetches `runtime.cjs`, then `pm2 restart`), or downloads a new setup script. Settings edits do not need this (config sync) |
| 23 | "Download failed: could not download the runtime" from the old vercel.app host | Read the script's relay URL | The script was made on the old host, which answers 404 | Download a fresh script from the production site |
| 24 | An old agent cannot decrypt its key | Ask when it was created | Created before 2026-08-03, under the old encryption secret. Accepted breakage: it must fail cleanly, not crash the app | Create a new agent |
| 25 | A new agent's on-chain `card_uri` is not the production host | Read `/api/moi/card/<address>` (the card the app serves). The `card_uri` stored on chain is read from the registry profile, as post-cutover check 0.4 did; how that was done is not recorded (the previous DevRel's notes); ASK: Gokul | `NEXT_PUBLIC_APP_URL` was wrong at build. It is permanent for each agent registered | STOP taking users. `rollback.md`, then rebuild with the right variable |
| 26 | "N agents need registering again" or a re-download banner | Date of the last reset | By design after a reset (the stranded check) | Owners re-register. Never delete their rows |

## E. Limits
| # | You see | Read-only check first | Cause | Fix, then verify |
|---|---|---|---|---|
| 27 | Internal model calls refused, with an admin alert | Read the alert | Platform spend crossed `GLOBAL_DAILY_SPEND_CAP_CENTS`; the flag is per UTC day and the alert says until UTC midnight | Wait for midnight UTC. Raising the variable does not lift today's flag (`lib/guardrails.ts` checks `killed` first). A manual reset is not recorded (the previous DevRel's notes); ASK: Rahul |
| 28 | A user is refused a name | Ask the name | Names are unique across all live agents, ignoring case (migration 0008) | Choose another name |

## Run: when the cause is a reset (Launchpad side)
The multi-product sequence, the message to the protocol team and the checks are `moi-devnet-reset`. These are the Launchpad-only steps; run every command from your working copy of `sarvalabs/moi-agent-launchpad`.
| # | Step | Command or action | Done when | Gate |
|---|---|---|---|---|
| R1 | Confirm | Row 9 check. Ask Gokul for the new registry id, whether agents were re-imported, new package versions, and whether the KMOI id, fuel floor or participant minimum moved | You hold the id and the answers in writing | read-only |
| R2 | Point at the id | Set the variable `MOI_AGENT_REGISTRY_LOGIC_ID` and run the workflow (`settings-and-secrets.md`). Also a PR that changes `DEFAULT_AGENT_REGISTRY_LOGIC_ID` in `lib/moi/registry.ts` and the ids pinned in `tests/registry-id.test.ts` and `tests/chain-constants.test.ts` | `chain-listing` PASS twice | GATE |
| R3 | Registration wallets | The operator, from the working copy after `npm ci`, with a sponsor account (a wallet registered in the MOI Wallet app on the new chain and funded at https://voyage.moi.technology/faucet/). The script also needs `MOI_REGISTRATION_MNEMONIC_1` to `_3` in the environment of whoever runs it, and it loads a `.env` from the folder it runs in. DevOps holds those three; how they reach the operator, never through chat, is open (ASK: Upendhar). Commands in the block under this table. The grant is in anu (1 KMOI is 1000000000 anu): set `MOI_REGISTRATION_GRANT` to at least 1000000000; the app's own default is 10000000000. The script default, 500000000 (0.5 KMOI), is rejected by the chain, and the script counts "account visible" as success, so read the receipt | Three funded accounts exist and a fresh wallet activates with receipt status 0 | GATE, OPERATOR |
| R4 | Tell DevOps | The registration wallets' balances are not in their alerts. Draft from `moi-devrel/templates/messages.md` | DevOps knows | GATE (the message) |
| R5 | Market | Only if payments are to come back. The operator, on the machine that has the Coco compiler (`~/.coco/bin/coco`; install the Coco compiler from its release, 0.9.3 targeting PISA 0.8.2 as of 13 October 2026; where the release is published: ASK: Gokul), runs `cd contracts/agent_market`, `~/.coco/bin/coco compile`, `~/.coco/bin/coco manifest convert`, then from the repo root `bash contracts/agent_market/deploy-local.sh` (bash, not zsh: it asks for the deployer phrase at a hidden prompt with `read -s -p`). It prints a `MOI_AGENT_MARKET_LOGIC_ID`. Then, as GATE steps, a PR that adds `MOI_AGENT_MARKET_LOGIC_ID=${{ vars.MOI_AGENT_MARKET_LOGIC_ID }}` to `deploy.yml` and updates the default in `lib/moi/registry.ts`; the variable; and the payments switch, which needs the `Dockerfile` and `docker-build.yml` edit for a new `NEXT_PUBLIC_*` value (`ship-a-change.md`). The August attempt reverted, and whether the compiled manifest is valid on the current chain is unknown. PR #10 (the deploy budget) was closed on 13 October 2026: the redeploy is blocked on the transfer error, not the budget, so redeploy against the devnet of the day | A purchase verifies with `node scripts/verify-purchase.mjs 0x<subscribe tx hash>` | GATE, OPERATOR | <!-- slop-lint:ignore -->
| R6 | Users | The dashboard banners and their storage keys are written for the 2026-08-15 and 2026-08-19 events (`app/dashboard/page.tsx`). Edit them for the new date or people who dismissed the old notice never see the new one | A PR is merged | GATE |

Commands for R3, zsh form (in bash use `read -rsp "Sponsor phrase: " M`, and likewise for the others). Each phrase is typed at a hidden prompt, never in chat:
```
cd "<your working copy of sarvalabs/moi-agent-launchpad>" && npm ci
read -rs "M?Sponsor phrase: " && echo
read -rs "W1?Registration wallet 1 phrase: " && echo
read -rs "W2?Registration wallet 2 phrase: " && echo
read -rs "W3?Registration wallet 3 phrase: " && echo
MOI_SPONSOR_MNEMONIC="$M" MOI_REGISTRATION_MNEMONIC_1="$W1" MOI_REGISTRATION_MNEMONIC_2="$W2" MOI_REGISTRATION_MNEMONIC_3="$W3" node scripts/recreate-registration-wallets.mjs --dry-run
```
If the dry run says "ready", repeat the last line with `MOI_REGISTRATION_GRANT=<anu>` added and without `--dry-run`, then `unset M W1 W2 W3`. If the sponsor address shows a zero balance, the phrase was funded at the faucet path: add `MOI_SPONSOR_DERIVATION_PATH="m/44'/6174'/7020'/0/0"`.

Never delete agent rows to fix a reset. The registry was re-imported from an old snapshot (144 agents, 1 of 11 listed agents carried over in September), so most owners must re-register.

## Not yet known
- The channel where the protocol team announces a reset. ASK: Gokul.
- How the kill switch is reset by hand: not recorded (the previous DevRel's notes); ASK: Rahul. The market contract is not redeployed (fact as of 13 October 2026).
