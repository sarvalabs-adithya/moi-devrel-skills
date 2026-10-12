# Website: change a secret, a variable or an API address

Facts are as of 2026-10-03 from `.github/workflows/deploy.yml` and `preview.yml` on `sarvalabs/MOI-Website` `main` (`5e91afa`), `.env.example`, `server/index.js`, and the research note dated 2026-10-02. Values are never written here: names only. Where each name lives and who grants it: `moi-devrel/references/keys-and-access.md`. Back to `../GUIDE.md`.

Website: A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin.

A step marked ADMIN needs the operator to confirm first that the handover note was read.

## How a setting reaches the site
- GitHub Actions secrets of `sarvalabs/MOI-Website` cannot be read back. No shared vault exists. Put the value in an org vault before you change it. ASK: Rahul which vault.
- `deploy.yml` lists what it hands the VM script, as `export` lines, at deploy time only: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`, `VITE_CHATBOT_API`, `DATA_ROOM_CHAT_URL`, `VITE_GA_ID`, `PUBLIC_GA_ID`. Access: secrets `TELEPORT_PROXY`, `TELEPORT_JOIN_TOKEN`, `TELEPORT_NODE`, `VM_USERNAME`. The preview workflow uses the variables `PREVIEW_VM_HOST` and `PREVIEW_VM_USER` and the same Teleport secrets.
- Read by the server (`server/index.js`) but not passed by the workflow, so they must be set on the VM by DevOps: `ALLOWED_ORIGINS` and `PORT`. The server's CORS default allows only the local dev address, so a browser on another origin needs `ALLOWED_ORIGINS`.
- `VITE_*` values are compiled into the JavaScript at build time. Changing one needs a rebuild, which a redeploy does.
- A secret that is set in GitHub but not listed in the workflow does nothing. A name the workflow lists but no code reads (`VITE_GA_ID`, `PUBLIC_GA_ID`: nothing on `main` outside the workflows mentions them) also does nothing. Measurement runs through Google Tag Manager `GTM-M4BR46Z2`, written in `index.html` and `blog/src/components/Analytics.astro`; the GA4 tag and its hostname trigger live in the GTM account (`src/lib/analytics.js` header). Changing the GA secrets changes nothing (inferred).
- `DATA_ROOM_CHAT_URL` and `DATA_ROOM_API_KEY` are read by the dev proxy and by `api/chat.js`, the old host's function, only (`git grep` on `main`, 2026-10-03). Nothing on the VM path reads them, so setting either does nothing.

## Run: change a setting

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Read what is set (names only) | `gh secret list -R sarvalabs/MOI-Website` and `gh variable list -R sarvalabs/MOI-Website`. Needs access to the repository's settings; an error means ASK: Rahul | You can compare the names with the lists above |
| 2 | CHECK | Is the name wired? | With no clone: `gh api -H "Accept: application/vnd.github.raw" repos/sarvalabs/MOI-Website/contents/.github/workflows/deploy.yml \| grep -n "<NAME>"` (a read). With a clone made as in `website-ship.md` step 2: `git grep -n "<NAME>" origin/main -- .github server src scripts`. If no workflow line passes it, step 5 is needed | A yes or no |
| 3 | CHECK | Where is the old value kept? | The vault. If nowhere, stop and ASK: Rahul before overwriting | The old value is recoverable |
| 4 | GATE | Set it | The operator runs `gh secret set <NAME> -R sarvalabs/MOI-Website` and types the value at the hidden prompt, or uses the GitHub settings page. Claude never sees or types it | The name is set (`gh secret list` shows it, with no value) |
| 5 | LOCAL | New name only | In a clone made as in `website-ship.md` steps 2 and 3, add it to the `env:` block and the `export` lines of `.github/workflows/deploy.yml`. The VM script must also pass it to the server or the build, and that script is not in git. ASK: Upendhar | The edit is on disk |
| 6 | GATE | Ship the workflow edit, if any | `website-ship.md` | Merged |
| 7 | GATE | Redeploy | `gh workflow run "Deploy MOI Website" -R sarvalabs/MOI-Website --ref main` (a merge to `main` also deploys) | The run finishes |
| 8 | VERIFY | Use it | `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" website`, then the specific read for the setting (below) | The setting shows its effect |

## Fix the baked API base (W-K2)
The live bundle has `https://dev.moi.technology/api` baked in from the secret `VITE_CHATBOT_API`. The component builds `${VITE_CHATBOT_API}/api/community-calls`, so the browser asks `https://dev.moi.technology/api/api/community-calls`. That host answers 200 text/html for any path (2026-10-03).
- The apex already forwards `/api` to the Express server (`/api/health` answers there with `X-Powered-By: Express`). So the fix is to set `VITE_CHATBOT_API` to `https://moi.technology`, or to empty (the component then uses `""`, the same origin), and redeploy so the bundle is rebuilt. This is inferred from the code and the probes, and no one has tried it. Confirm with Upendhar before step 4.
- The calendar admin page uses the same base, so it cannot save events until this is fixed.
- Verify: `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" website` shows `API base baked in: none` or the apex, not the dev host, and `website-calendar.md` step 5 shows a database row on the homepage.
Whether `dev.moi.technology` was meant to be the live API is unknown. ASK: Upendhar.

## Other settings

| Setting | Note |
|---|---|
| `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` | Chat answers and embeddings. Owners unknown. ASK: Rahul. A new key takes effect at the next deploy |
| `SUPABASE_URL`, `SUPABASE_KEY` | Decide the project first (`website-database.md`). Pointing them at a different project changes where the calendar and chat read |
| `ALLOWED_ORIGINS`, `PORT` | VM environment. A request for Upendhar (`who-to-ask.md`, R6), not a GitHub change |
| Blog distribution names (`BUFFER_ACCESS_TOKEN`, `BUFFER_CHANNEL_X`, `BUFFER_CHANNEL_LINKEDIN`, `DISCORD_WEBHOOK_URL`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`) | `moi-blog`. A channel with no secret is skipped without an error |

## Traps
- A manual run from a branch other than `main` hands that branch name to the VM script (`website-ship.md`).
- Secrets travel only at deploy. Setting one and not redeploying changes nothing.
- Do not store keys on a laptop (a rule since 2026-09-15). The one exception is the website ingest, which takes its three names at a hidden prompt (`website-chatbot.md`).
- Nothing in the repo records the live values. The only copy of the old value is the vault, if anyone put it there.

## Not yet known
- Who owns each key and the Supabase project (all "owner: confirm" in `DEPENDENCIES.md`, which is local to the previous operator; ASK: Adithya for a copy, Rahul for owners).
- Whether the VM script forwards a new name to the server. ASK: Upendhar.
