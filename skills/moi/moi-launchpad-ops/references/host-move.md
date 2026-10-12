# Host move: verify or recover the secrets first

Facts are as of 2026-10-03, from `docs/HANDOFF.md` ("Migrating off Vercel"), `scripts/verify-encryption-secret.mjs`, `deploy.yml`, `docs/POST-CUTOVER-CHECKLIST.md` and the research. Use this before moving or rebuilding the Launchpad's hosting, after losing the VM, or at a handover. The reason is one secret: `AGENT_KEY_ENCRYPTION_SECRET` encrypts every stored agent key and can never be regenerated. Back to `../SKILL.md`. <!-- slop-lint:ignore -->

## What happened last time, and why it matters
- The Launchpad left Vercel for the DevOps VM in early August 2026 (the always-on polling used up the free compute allowance). On 2026-08-03 the VM was started with a newly generated encryption secret (Vercel sensitive variables are write-only, per `docs/HANDOFF.md`). Agents created on Vercel can no longer decrypt their keys. The previous operator accepted that breakage; a crash would not have been accepted. <!-- slop-lint:ignore -->
- Today the readable copies are the Actions secret of the same name (write-only) and the app's env file on the VM (ASK: Upendhar where), which only DevOps can read. No vault exists. The Vercel-era value is not the current one. If both remaining copies are lost, every agent key created since 2026-08-03 is lost with them. This is the first thing a new owner should close: confirm the two copies match, then vault it. <!-- slop-lint:ignore -->
- The old Vercel host answered 404 on 2026-10-03. Whether the Vercel project is deleted or only paused is not on record (ASK: Adithya). Until it is deleted, an old deployment could still point at the same database. <!-- slop-lint:ignore -->

## Run: verify, recover, move
| # | Step | Command or action | Done when | Gate |
|---|---|---|---|---|
| 1 | Inventory | In your working copy: `git grep -ho "process\.env\.[A-Z_0-9]*" -- app lib instrumentation.ts middleware.ts next.config.mjs \| sort -u`, then `gh secret list -R sarvalabs/moi-agent-launchpad --json name,updatedAt` and `gh variable list -R sarvalabs/moi-agent-launchpad --json name,updatedAt` | Every name the app needs has a source below or an ASK | read-only |
| 2 | Get a candidate | The only readable copy of the encryption secret is the VM file. DevOps reads it; the value reaches the operator by a route DevOps and Rahul approve. Claude never receives it. ASK: Upendhar, Rahul for the route (the message to them is a GATE; the operator sends it). Do not ask DevOps for a value in chat | The operator holds a candidate without it passing through Claude | GATE (the message), OPERATOR |
| 3 | Get one ciphertext | The operator runs in the SQL editor of the production project: `select moi_key_ciphertext from agents where moi_key_ciphertext is not null limit 1;` and copies the value. A ciphertext is worthless without the key, but do not paste it into chat | The operator has an `iv.tag.data` string | OPERATOR |
| 4 | Verify the secret | In the Launchpad working copy, with the candidate typed at a hidden prompt (zsh form; bash uses `read -rsp "Candidate: " S`): `read -rs "S?Candidate: " && echo`, then `AGENT_KEY_ENCRYPTION_SECRET="$S" node scripts/verify-encryption-secret.mjs --ciphertext "<iv.tag.data>"`, then `unset S`. Exit 0 and "MATCH" means it is the one production used. Exit 1 and "MISMATCH" means stop: moving with it makes every key unreadable. The script prints the candidate's length: do not repeat it. Without the environment value the script falls back to a local `.env` file: Claude never opens it | MATCH, written in the checklist | OPERATOR |
| 5 | Recover the rest | See the table below | Each name has a new or confirmed value | OPERATOR |
| 6 | Vault | Put every value in the org vault before you change anything. ASK: Rahul which vault and who creates the first entries | The vault holds them | GATE |
| 7 | Stand up the new host | DevOps builds the box, proxy and certificate. The pipeline writes `.env` from Actions on each deploy, so set the Actions values first (`settings-and-secrets.md`) and then deploy | A deploy to the new host is green | GATE |
| 8 | Webhook | If the secret changed or the public URL did, the operator re-sets the Telegram webhook (`settings-and-secrets.md`) | `getWebhookInfo` shows the right URL and no error | GATE, OPERATOR |
| 9 | Verify | `bash "$SKILLS/moi-launchpad-ops/scripts/launchpad-health.sh" --origin https://<temporary name>` before DNS moves (the script needs a name with a valid certificate: ASK: Upendhar for one), then without `--origin` after DNS moves. Then the post-cutover checklist sections 1 to 3 (written for the Vercel to VM move; the domain and commit lines are old). For its check 2.1 the operator downloads a setup script for a test agent they own and prints only its web addresses with `grep -Eo 'https?://[A-Za-z0-9.:-]+' <the downloaded file> \| sort -u`; the file holds that agent's private key, so Claude does not open it and the operator deletes it afterwards | Healthy, and the Launchpad host in that list is the production host | read-only; the download is GATE, OPERATOR | <!-- slop-lint:ignore -->
| 10 | Old host | Decide what happens to the old host and write the decision down (checklist section 5). Two deployments writing one database is the risk | Decision and date recorded | GATE |

## Recover the other values
| Name | How |
|---|---|
| `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` | The Supabase dashboard, Settings, API. Needs the project login (owner unknown: ASK: Adithya, Rahul) |
| `GROQ_API_KEY` | Issue a fresh key in the Groq console (ASK: Adithya for the account) |
| `TELEGRAM_BOT_TOKEN` | BotFather for `moinetworkbot` (ASK: Adithya). Reissuing revokes the old token |
| `SESSION_SECRET`, `CRON_SECRET` | Cannot be recovered. Generate new ones; everyone is signed out |
| `TELEGRAM_WEBHOOK_SECRET` | Cannot be recovered. Generate a new one, then `setWebhook` |
| `MOI_REGISTRATION_MNEMONIC_1`, `_2`, `_3` | DevOps holds them. Do not copy them around |
| `MOI_PLATFORM_MNEMONIC` | A funded devnet wallet. Holder unclear: ASK: Adithya, Upendhar |
| Variables (`MOI_AGENT_REGISTRY_LOGIC_ID`, `MOI_RPC_URL`, `NEXT_PUBLIC_*`, `GLOBAL_DAILY_SPEND_CAP_CENTS`, `TELEGRAM_BOT_USERNAME`) | Not secret. Read only these with the command under this table, because `VM_HOST` and `VM_USER` are variables too and are private |
| `GHCR_PAT`, `TELEPORT_*`, `VM_HOST`, `VM_USER` | DevOps |

The command for the variables row:
```
gh variable list -R sarvalabs/moi-agent-launchpad --json name,value --jq '.[] | select(.name | test("^(MOI_AGENT_REGISTRY_LOGIC_ID|MOI_RPC_URL|GLOBAL_DAILY_SPEND_CAP_CENTS|NEXT_PUBLIC_.*|TELEGRAM_BOT_USERNAME)$")) | .name + "=" + .value'
```

Do not treat a local `.env` as a production source. The local one points at a local database, and Claude never opens any `.env` file.

## If the domain changes
`NEXT_PUBLIC_APP_URL` is written permanently into every on-chain agent card and into every setup script users have downloaded. Moving to a new domain leaves all of them pointing at the old host. The old name must keep answering (cards at `/api/moi/card/<address>` and the relay routes) until nothing uses it, or those agents break. Treat a domain change as its own project and ASK: Rahul first.

## Not yet known
- Whether the Actions secret and the VM file hold the same encryption value. Step 4 is how to find out.
- Which vault, and who creates the first entries. ASK: Rahul.
- Whether the Vercel project still exists. ASK: Adithya. <!-- slop-lint:ignore -->
