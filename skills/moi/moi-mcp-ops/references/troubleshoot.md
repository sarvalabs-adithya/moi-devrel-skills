# Troubleshoot the MOI MCP server

Start with the one command that tells you where to look: `bash "$SKILLS/moi-mcp-ops/scripts/mcp-health.sh"`. Match its first FAIL or WARN to a row, run the "check first" column (read-only), and only then change anything. A fix marked GATE needs the operator's explicit yes naming the action. Rows come from the repo's own troubleshooting table (`docs/handoff-infra.md`), PR bodies and live reads. Every "DevOps:" fix below is a GATE: Claude drafts the ask and the operator sends it. Facts are as of 2026-10-02 and 2026-10-03; every symptom here happened at least once. Back to `../SKILL.md`.

Who can act on the VM (the processes, nginx, TLS, DNS, logs): DevOps. The VMs are `voyagedev` (dev) and `prod-voyage` (production); Srikar runs them and the deploy workflow, ASK: Srikar, and Upendhar is the other DevOps contact. Who decides anything else: ASK: Rahul. Which products DevRel owns is not settled. Claude never logs in to a VM.

MCP server: `project-handover-docs/MCP-SERVER.md` records no security finding for this product. The 2026-10-02 research note said one was open; its content is not recorded (the previous DevRel's notes); ASK: Rahul before touching sign-in or other admin code.

## The site is down

| # | Symptom | Check first (read) | Cause | Fix |
|---|---|---|---|---|
| 1 | Script: `health: unreachable` (name, TLS or timeout) | `curl -sI https://<host>/health`. Is it the right host? `mcp.moi.technology` does not exist; the live hosts end `.voyage.moi.technology` | DNS, certificate, nginx or the VM is down | VM, DNS, TLS and nginx are DevOps. Send one short message (Claude drafts, the operator sends, GATE): host, what you ran, the answer. ASK: Upendhar |
| 2 | `health: HTTP 502` | The script line; DevOps reads the pm2 status of `moi-mcp-write` (port 8788) and `moi-mcp-read` (port 8787) | The Node process is down, or nginx points at the wrong port | DevOps reads the write gateway's error log (ASK: Upendhar where it is). A fatal line about `WC_PROJECT_ID` means the id is missing or a placeholder |
| 3 | `health: HTTP 503`, `ok` false | The error log names the variable | The shared config failed to load: a bad `MOI_NETWORK`, or `custom` without `MOI_RPC_URL` | Correct the variable in the workflow (PR, GATE), deploy (GATE) |
| 4 | `health: redirect (HTTP 3xx)` | The `Location` host in the script line | A redirect sits in front of the gateway. It drops the `Authorization` header, so sign-in breaks silently | DevOps removes it. No redirect may precede either hostname, http to https included |
| 5 | `health: HTTP 504` | The script line | nginx timed out waiting for the process | DevOps |
| 6 | Health ok, `tools/list` count or names differ | `architecture.md` "What is live" | A deploy changed the surface | State which build is live. Not a fault by itself |
| 7 | Health ok, `ping` or a read tool fails | `curl` a `tools/call` of `ping`. Then the RPC lines of the script | The chain RPC is down or its path moved (the hosted read gateway uses `/babylon/`, the code default is `/devnet/`) | ASK: Gokul. If one path answers and the other does not, tell the Voyage team |

## Sign-in and connecting

| # | Symptom | Check first (read) | Cause | Fix |
|---|---|---|---|---|
| 8 | Script: oauth issuer is `http://localhost...` | `curl -s https://<host>/.well-known/oauth-authorization-server` | `PUBLIC_URL` never reached the process | Set it in the workflow (PR, GATE), deploy (GATE) |
| 9 | Consent completes, then the connector asks again | The issuer line; is the site plain http? | `PUBLIC_URL` differs from the host users reach, or http drops the Secure cookie | Exact https origin, TLS only, then a restart through a deploy (GATE) |
| 10 | claude.ai Connect spins forever though the curl steps pass | Script WARN "protected-resource metadata" | claude.ai compares `resource` with the URL typed, `/mcp` included. Before PR #18 the server returned the bare origin and served only the root document. Its `/register` limit of 10 a minute also locked out everyone, who share one egress range | Fixed on master since 2026-09-23 (limit now 120 a minute). Production showed the old form on 2026-10-03 and dev the new one. Ship a build that contains #18: `ship-a-change.md`. Whether Connect really fails on production is untested: the Connect step of `connect-and-verify.md` proves it |
| 11 | Everyone is locked out after a few Connect clicks | Same | The registration limit of 10 a minute (pre-#18) | Same |
| 12 | A second person on a shared browser cannot start as themselves | Does the build have PR #20? | The consent page did not allow it | Fixed in #20; needs a sync |
| 13 | Connector added with authentication None on the write host | The connector settings | Sign-in is impossible | Re-add with OAuth. None is only for the read host |
| 14 | claude.ai shows no QR | `moi_connect_wallet` output | claude.ai never renders the image | The tool returns a pairing page link (PR #19): open it |
| 15 | Scanning does nothing, "The WalletConnect relay refused the pairing" | The workflow passes `WC_PROJECT_ID`? | The id is missing, a placeholder or misshapen | Real 32-hex id in the voyage-api secret (GATE) and a deploy (GATE) |
| 16 | "The wallet pairing has expired" | `moi_wallet_status` | A pairing lasts a week (15 minutes or one approval with `remember: false`) | Call `moi_connect_wallet` again. Expected |
| 17 | Every write fails `NETWORK_MISMATCH` | `moi_wallet_status` and the server's network | The wallet is on another network than `MOI_NETWORK` | Align the wallet, disconnect and pair again |
| 18 | Everyone signed out after a deploy or a restore | Was `MOI_DATA_DIR` lost, or `auth/cookie-secret` changed? | A new cookie secret gives every browser a fresh identity | Restore the original file. If it is gone, users sign in and pair again |

## Tools and writes

| # | Symptom | Check first (read) | Cause | Fix |
|---|---|---|---|---|
| 19 | `moi_resolve_agent`: "Could not load the MOI agent registry ... account not found" | Script WARN. Production and dev both on 2026-10-03 | The registry id is the wiped one, or `MOI_READ_CALLER` is unset | `settings-and-secrets.md`, "the MCP part of a devnet reset". ASK: Gokul for the current id |
| 20 | "interaction underpriced" after the phone approval | Build has PR #15? | A fuel price literal of 1; the floor is 50 (as of v0.13.0). Simulation had accepted it | Fixed in #15 (price from the SDK); needs a sync |
| 21 | `moi_create_asset` refused, hint says visit the faucet, wallet is funded | Build has PR #13? | A storage fund default written when KMOI had no decimals | Fixed in #13 (SDK default; the minimum is `MIN_STORAGE_FUND`, 7 KMOI on master) |
| 22 | Launchpad tool: "Not signing: the sign-in message from <origin>..." | `MOI_LAUNCHPAD_URL` against the Launchpad's `NEXT_PUBLIC_APP_URL` | They differ | Make them equal (workflow PR, GATE) |
| 23 | Tool calls fail during a long phone wait | nginx `proxy_read_timeout` | Below 300 s, so nginx cuts the held connection | DevOps: `proxy_read_timeout 300s; proxy_send_timeout 300s;` |
| 24 | The service looks healthy but never answers a stream | nginx `proxy_buffering` | Buffering on: the stream is held back | DevOps: `proxy_buffering off` |
| 25 | All users share one rate-limit bucket | nginx `X-Forwarded-For $remote_addr`; does nginx connect from the same machine? | A proxy on another address makes the limiter key on that address | DevOps |
| 26 | Write gateway errored or looping after a deploy, log mentions `MOI_SESSION_KEY` | The write gateway's recent log, read by DevOps (ASK: Upendhar where) | Not read by `master` yet, so expect it only after the encryption-at-rest change is synced. The variable is missing, blank or too short, and the Voyage workflow does not pass it (inferred) | Pass it from the workflow (PR, GATE). Never put it in `ecosystem.config.cjs` |
| 27 | After a crash: "had broadcast before exit; recording it confirmed" or "cannot be safely re-broadcast; marking orphaned" | Log lines | Journal reconciliation at boot | None. The user retries in chat |

## Deploys and automation

| # | Symptom | Check first (read) | Cause | Fix |
|---|---|---|---|---|
| 28 | "Deploy MOI MCP Gateway" run is red | `gh run view <id> -R sarvalabs/voyage-api --log-failed` | Unknown: no run history was read. The job builds, tests, copies through Teleport and checks health | Read the failing step. A red deploy can leave the old processes stopped: re-check with the script, then `rollback.md`. ASK: Srikar |
| 29 | A sync PR shows no preview | The run list of `moi-mcp.preview.yml` | Unknown | ASK: Srikar |
| 30 | A `Chain canary failing` or `Upstream release` issue is open | `watch-and-canary.md` | An upstream moved | That file's runbooks |
| 31 | Claude Desktop config with `npx -y @moi-protocol/mcp-server` does nothing | `npm view @moi-protocol/mcp-server` says not found | Nothing is published | Use the hosted connector, or a local build (`connect-and-verify.md` part H) |

## What to tell a user (typical questions, answers from the repo's docs)

| Question | Answer |
|---|---|
| The connector will not connect | Add `https://mcp.voyage.moi.technology/mcp` with OAuth. None is for the read host only. Row 10 is the known stall |
| I see no QR | Open the pairing link the tool returns. The code lasts about 5 minutes; call `moi_connect_wallet` again if it expires |
| Is my key on your server? | No. The server never holds a private key. The phone signs every write, and every write is a preview then a confirm token valid 10 minutes, once |
| Can I run it with `npx`? | Not yet. Nothing is published |
| Agent lookup says not found | Known while the registry id is stale (row 19). Say so plainly: nothing is wrong with the user's wallet |

## Add to this file
When you solve a new failure, add a row with the date, the exact message, the cause and the fix commit or PR, as `docs/testing-plan.md` does. Reproduce before fixing, and add a test that would have caught it.

## Not yet known
- Where users report MCP faults, and who watches that channel. No support channel for the MCP is recorded (the Launchpad dashboard points to Discord). ASK: Rahul.
- Why a deploy run is red when it is: no run history was read. ASK: Srikar.
- Whether the workflow's health job fails the run when a gateway does not come up.
