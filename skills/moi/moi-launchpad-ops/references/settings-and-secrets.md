# Settings and secrets: names only

Facts are as of 2026-10-03, updated 2026-10-14 from `project-handover-docs/AGENT-LAUNCHPAD.md`, from `.github/workflows/deploy.yml`, `Dockerfile`, the code that reads each name (`git grep` on `origin/master`), the research notes and `moi-devrel/references/keys-and-access.md`. This file never holds a secret value, or the length or prefix of one; the numbers below are public defaults. Back to `../SKILL.md`.

## Where values live
- **GitHub Actions** on `sarvalabs/moi-agent-launchpad`, Settings, Secrets and variables, Actions. Secrets cannot be read back. Variables can. Only a repo admin can edit either (ASK: Rahul who the admins are for this repo; the list is not on record).
- **The VM file**, the app's env file (where: ASK: Upendhar), rewritten by every deploy. It is the only readable copy of the secrets, and only DevOps can reach it (Teleport). No vault exists. ASK: Rahul which one the org will use.
- **The image**: `NEXT_PUBLIC_*` values are inlined at build. Restarting the container cannot change them.
- **Never** open any `.env` file (`.env`, `.env.local`, `.env.production` and the like). A local one points at a local database and is not production. Read `.env.example` for names only.

## Rotation labels
**free**: change it and redeploy. **step**: change it, redeploy, and do the extra step. **never**: do not change it.

## Names, what they do, what breaks
Type: S is an Actions secret, V an Actions variable, B baked at build, N means `deploy.yml` does not write it (the app uses a code default; setting it needs a `deploy.yml` edit through `ship-a-change.md`).
| Name | Type | What it does | When wrong | Rule |
|---|---|---|---|---|
| `SUPABASE_URL` | V | Database endpoint. Names the project (company Supabase organisation since 8 October 2026) | Every API route errors | free |
| `SUPABASE_SERVICE_ROLE_KEY` | S | All database access | Same | free: reissue in the dashboard (Settings, API) |
| `SESSION_SECRET` | S | Signs the sign-in session | Everyone is signed out. A value below the minimum length is refused at request time (`lib/session.ts`) | free: generate with `openssl rand -hex 32`. If `TELEGRAM_WEBHOOK_SECRET` is unset, the webhook secret derives from this, so a change then needs the webhook step |
| `AGENT_KEY_ENCRYPTION_SECRET` | S | Decrypts every stored agent key | Every stored agent key becomes unreadable for good | **never**. Only the VM file holds a readable copy. See `host-move.md` |
| `MOI_RPC_URL` | V | Node URL. Ignored if it contains "voyage" or "devnet": the SDK's built-in devnet endpoint is used instead | Nothing changes for such a URL | As of October 2026 the Actions variable is set (`project-handover-docs/AGENT-LAUNCHPAD.md`): confirm it points at a host that resolves, or clear it. The documented example host did not answer when probed on 2026-10-02 |
| `MOI_AGENT_REGISTRY_LOGIC_ID` | V | The agent registry. Empty means the code default | Registrations fail with "account not found" | step: after a reset, with `moi-devnet-reset` |
| `MOI_AGENT_MARKET_LOGIC_ID` | N | The AgentMarket contract. Code default is the pre-wipe id | Market reads return `onchain: null` | step: redeploy the contract first |
| `NEXT_PUBLIC_PAYMENTS_ENABLED` | B, N | Paid features on only when exactly `1` | Paid routes answer `payments_disabled` | Do not set until the market contract works |
| `MOI_PLATFORM_MNEMONIC` | S | Funded platform wallet, for registry reads and the heartbeat (handover doc) | Reads fall back; unclear what else | `deploy.yml` reads it but it is not in the repo's secrets list: an org-level secret, or the VM gets an empty value. ASK: Upendhar |
| `MOI_REGISTRATION_MNEMONIC_1`, `_2`, `_3` | S | Wallets that create and fund new users | Activation answers 503 `faucet_unavailable` | DevOps holds them. Never copy them around |
| `MOI_REGISTRATION_API_URL`, `MOI_REGISTRATION_API_KEY` | V, S | Proxy mode for activation. Not in use | Wins over direct mode if both are set | DevOps |
| `MOI_REGISTRATION_GRANT`, `MOI_REGISTRATION_DERIVATION_PATH` | N | Starter grant (code default 10 KMOI; the floor is 1 KMOI) and the wallet path | A grant under 1 KMOI reverts on chain | Leave unset |
| `MOI_READ_CALLER_ADDRESS`, `MOI_KMOI_ASSET_ID`, `MOI_POOL_RPC_URL` | N | Chain plumbing overrides | A wrong value breaks reads | Leave unset unless the protocol changed |
| `TELEGRAM_BOT_TOKEN` | S | The delivery bot | All sends fail | step: reissue in BotFather (DevRel's Telegram account owns the bot until the transfer, `project-handover-docs/MIGRATION-LIST.md`) |
| `TELEGRAM_BOT_USERNAME` | V | Deep links (`moinetworkbot`) | Link buttons break | free |
| `TELEGRAM_WEBHOOK_SECRET` | S | Must equal the `secret_token` given to `setWebhook` | Telegram stops delivering, with no error | **step**: the webhook runbook below |
| `ADMIN_ALERT_TELEGRAM_CHAT_ID` | S | Where admin alerts go | Alerts are only logged | free. Like the platform mnemonic, not in the repo's secrets list: confirm with Upendhar |
| `GROQ_API_KEY` | S | Internal model calls only. Users bring their own key | Internal paths fail | free. No company Groq key exists (October 2026): the next owner creates one at console.groq.com and replaces the value |
| `GLOBAL_DAILY_SPEND_CAP_CENTS` | V | Daily platform spend cap (500 in the research) | Lower trips the kill switch sooner. Do not delete the variable: `deploy.yml` would write an empty value, and the code reads `?? 500`, which does not treat an empty string as unset (inferred from `lib/limits.ts`, untested) | free |
| `CRON_SECRET` | S | Bearer token for `/api/cron/cleanup` | Manual cleanup is refused | free |
| `INBOX_WAIT_MS` | fixed | `deploy.yml` writes 20000 itself | Long polls could outlast nginx | A `deploy.yml` edit |
| `DAILY_INTERACTION_CAP`, `MAX_AGENTS_PER_USER` | N | Limits | Code defaults apply | Leave unset |
| `MOI_SKIP_PAYMENT_VERIFY` | N | Emergency switch: trusts the buyer's word on a payment | Unsafe | Never set in production |
| `MOI_VERIFY_REGISTRATION` | N | Opt-in check that a registration transaction was sent by the owner. Off by default; a code comment says it was left off until tested against a real wallet | Unknown if turned on | Leave unset. Test against a real wallet before enabling |
| `NEXT_PUBLIC_APP_URL` | V, B | The app's own origin. Written into every downloaded agent and every on-chain card | The build fails unless it starts with `https://`. A wrong host is permanent for each agent registered | **never casually**: a rebuild fixes new agents only |
| `NEXT_PUBLIC_MOI_EXPLORER_URL`, `NEXT_PUBLIC_WALLET_INSTALL_URL` | V, B | Explorer links and the wallet install link (it must include the extension id) | Dead or generic store links | step: rebuild |
| `NEXT_PUBLIC_MOI_CHAIN_ID`, `NEXT_PUBLIC_WC_PROJECT_ID` | V, B | The phone QR sign-in (PR #32 and #33), live and tested on 13 October 2026. The first name keeps "CHAIN" but its value is the network ID, and the code falls back to `moi:14`. The project id comes from cloud.reown.com (the Reown projects are under sarvalabsdeveloper@gmail.com) | The QR sign-in breaks | step: rebuild |
| `NEXT_PUBLIC_DISCORD_INVITE_URL`, `DISCORD_WEBHOOK_URL` | N | The Discord link on the dashboard; a notification webhook | No link, no notices | Not recorded (the previous DevRel's notes); ASK: Rahul for the invite to point at |
| `GHCR_PAT`, `TELEPORT_PROXY`, `TELEPORT_JOIN_TOKEN`, `VM_HOST`, `VM_USER` | S, V | How the workflow reaches the registry and the VM | Deploys fail | DevOps only. ASK: Upendhar |
| `GEMINI_API_KEY`, `OPENAI_API_KEY`, `LLM_MODEL` | N | Optional model providers | Defaults apply | Leave unset |
Names the code reads that `moi-devrel/references/keys-and-access.md` does not list: `MOI_AGENT_MARKET_LOGIC_ID`, `NEXT_PUBLIC_PAYMENTS_ENABLED`, `INBOX_WAIT_MS`, `DAILY_INTERACTION_CAP`, `MAX_AGENTS_PER_USER`, `MOI_REGISTRATION_GRANT`, `MOI_REGISTRATION_DERIVATION_PATH`, `MOI_READ_CALLER_ADDRESS`, `MOI_KMOI_ASSET_ID`, `MOI_POOL_RPC_URL`, `MOI_SKIP_PAYMENT_VERIFY`, `MOI_VERIFY_REGISTRATION`, `NEXT_PUBLIC_DISCORD_INVITE_URL`, `DISCORD_WEBHOOK_URL`, `GEMINI_API_KEY`, `OPENAI_API_KEY`, `LLM_MODEL`. ASK: Rahul to add them there.

## Run: change a setting
| # | Step | Command or action | Done when | Gate |
|---|---|---|---|---|
| 1 | Name and rule | Find the row above. Is it free, step or never? Is it baked (B) or written by `deploy.yml`? `git grep -n NAME .github/workflows/deploy.yml` | You know the rule and whether a PR is needed | read-only |
| 2 | Current state | `gh variable list -R sarvalabs/moi-agent-launchpad --json name,updatedAt` and `gh secret list -R sarvalabs/moi-agent-launchpad --json name,updatedAt`. Do not request the `value` field: variables such as `VM_HOST` and `VM_USER` are private | The name exists and you know when it last changed | read-only |
| 3 | Safety | A secret cannot be read back. If you do not hold its old value and it is the only copy, stop and ask. For a variable, note the old value in the checklist (variables are readable) | The old value is recoverable, or the rule is free | read-only |
| 4 | Set a variable | `gh variable set NAME -R sarvalabs/moi-agent-launchpad --body "<value>"` (the value is not secret) | `gh variable list` shows a new `updatedAt` | GATE |
| 5 | Set a secret | The operator runs `gh secret set NAME -R sarvalabs/moi-agent-launchpad` and types the value at the hidden prompt, or for a generated value `openssl rand -hex 32 \| gh secret set NAME -R sarvalabs/moi-agent-launchpad`, which prints nothing. Claude never sees or repeats a value | `gh secret list` shows a new `updatedAt` | GATE, OPERATOR |
| 6 | Apply | The new value reaches the app only at a deploy: `gh workflow run ci-cd.yml -R sarvalabs/moi-agent-launchpad --ref master`. It rebuilds the image and rewrites the VM `.env` | A run is queued | GATE |
| 7 | Watch | `gh run list -R sarvalabs/moi-agent-launchpad -L 3 --json databaseId,displayTitle,status,createdAt` for the id of the run just queued, then `gh run watch <id> -R sarvalabs/moi-agent-launchpad --exit-status` | Green | read-only |
| 8 | Verify | Health script, then the check in the next table | Healthy, and the setting's own effect is seen | read-only |
| 9 | Record | Name, old and new (variables only), time, run id, in `../templates/change-checklist.md` | The note exists | local |

| Setting | Its own check |
|---|---|
| Registry id | `chain-listing` PASS on two reads 30 seconds apart; `stats` `chainStatus=ok` |
| `NEXT_PUBLIC_APP_URL` | The operator downloads a setup script for a test agent they own (GATE: a download; the file holds that agent's key, so Claude does not open it) and prints only its web addresses with `grep -Eo 'https?://[A-Za-z0-9.:-]+' <the downloaded file> \| sort -u` (the Launchpad host must be the production host; the operator deletes the file afterwards). Then registers a test agent (spends devnet funds: GATE) and reads its card at `/api/moi/card/<address>`; that is the card the app serves, and reading the `card_uri` stored on chain is in `troubleshoot.md` row 25 |
| Webhook secret | The `getWebhookInfo` block below |
| `GROQ_API_KEY`, limits | No visible check. Say so in the hand-back |

## Run: rotate the Telegram webhook secret
Telegram stops delivering, with no error, if the secret in the header differs from the one in the app. The sequence is the secret, the deploy, then `setWebhook`. Step 3 below points at steps 6 and 7 of "Run: change a setting". Between the deploy and `setWebhook` the app rejects Telegram's calls with 401 (inferred from the route). The exact `setWebhook` command is in no repo file; this is the Telegram Bot API form, and the previous operator ran an equivalent on 2026-08-03 and saw "Webhook was set". The operator types the commands below in one shell (zsh form; in bash use `read -rsp "Bot token: " T`). Claude never sees the bot token or the new secret.
| # | Step | Command | Done when | Gate |
|---|---|---|---|---|
| 1 | Read first | The `getWebhookInfo` block below, to see the state before | `url` is the production webhook, no `last_error_message` | OPERATOR |
| 2 | Secret | `read -rs "T?Bot token: " && echo` then `S=$(openssl rand -hex 20)` then `printf '%s' "$S" \| gh secret set TELEGRAM_WEBHOOK_SECRET -R sarvalabs/moi-agent-launchpad` | `updatedAt` is new | GATE, OPERATOR |
| 3 | Deploy | Step 6 and 7 of the table above. Keep the shell open | Green run | GATE |
| 4 | Set | `printf 'url = "https://api.telegram.org/bot%s/setWebhook"\ndata-urlencode = "url=https://launchpad.moi.technology/api/telegram/webhook"\ndata-urlencode = "secret_token=%s"\n' "$T" "$S" \| curl -sS -K -` then `unset T S` | The answer says the webhook was set | GATE, OPERATOR |
| 5 | Verify | The `getWebhookInfo` block, then the operator messages the bot | `pending_update_count` falls to 0 and no new error | OPERATOR |

`getWebhookInfo` is read-only. The operator runs this block in one shell; it asks for the bot token at a hidden prompt (zsh form; in bash use `read -rsp "Bot token: " T`). Where the bot token comes from: BotFather (DevRel's Telegram account owns `moinetworkbot` until the transfer is made, `project-handover-docs/MIGRATION-LIST.md`). If it is exposed, reissue it there and tell the operator.
```
read -rs "T?Bot token: " && echo
printf 'url = "https://api.telegram.org/bot%s/getWebhookInfo"\n' "$T" | curl -sS -K - | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
except ValueError:
    sys.exit("the answer was not JSON")
r = d.get("result") or {}
print({k: r.get(k) for k in ("url", "pending_update_count", "last_error_date", "last_error_message")} if d.get("ok") else {"ok": d.get("ok"), "description": d.get("description")})
'
unset T
```
The filter matters: the raw answer can include the IP address of the server, which must not be pasted anywhere. The `-K -` form keeps the bot token out of the process list and the shell history. Run it as written each time the rotation runbook names it: it asks for the bot token again, because step 4 unsets `T` and `S`.

## Not yet known
- Who can edit secrets today (the admin list), and whether any value exists outside GitHub and the VM file. ASK: Rahul, Upendhar.
- Which logins are company-owned: Supabase is (company organisation, 8 October 2026); the Reown projects sit under sarvalabsdeveloper@gmail.com; BotFather is not yet (transfer pending); no company Groq key exists. Anything else: ASK: Rahul.
- Whether `TELEGRAM_WEBHOOK_SECRET` is set in Actions today (`gh secret list` shows names only). If it is not, the webhook secret derives from `SESSION_SECRET`.
- How the kill switch row is reset by hand. The code keys it by UTC day, so it ends at midnight UTC; a manual reset is not on record, and raising `GLOBAL_DAILY_SPEND_CAP_CENTS` does not lift a flag already set for the day (`lib/guardrails.ts` checks `killed` first). Not recorded (the previous DevRel's notes); ASK: Rahul.
