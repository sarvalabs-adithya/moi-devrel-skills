# Dataroom: ship a change

Facts are as of 2026-10-03 from `sarvalabs/moi-dataroom0` (public) `main` at commit `0f8e38b`, its one workflow file, `git ls-remote` and the public GitHub API (no open pull requests on 2026-10-03). Back to `../GUIDE.md`. Commits, pull requests and merges are `moi-devrel/ship`.

Dataroom: A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin.

## The path from a change to the live site
- `main` deploys. "Deploy MOI Dataroom" (`.github/workflows/deploy.yml`) runs on a push to `main` and on a manual run. It uses `appleboy/ssh-action` with the secrets `VM_HOST`, `VM_USERNAME` and `VM_SSH_KEY`, hands the VM six app secrets (`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `ADMIN_SECRET`) and runs a deploy script that is not in git. This is the one product that reaches its VM by SSH key, not Teleport. ASK: Upendhar for a copy of the script.
- No pull request runs any check, and nothing checks the site after the deploy. A green run only means the SSH script returned success (inferred).
- No rollback exists. Revert the merge in a new PR (merging it deploys).
- The app is not on its old host: `moi-dataroom0.vercel.app` answers 404 (2026-10-03). `AGENTS.md` on `main` is leftover boilerplate for that host.
- The app lives in the `moi-data-room/` folder, Next.js 16, and `/` redirects to `/home`.
- Chat spending limits are held in memory and reset at every restart, so each deploy resets them.

## Run: change code

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Baseline | `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" dataroom`. Note the KNOWN lines | Output saved |
| 2 | GATE | Get the code (a download) | In a folder the operator chooses: `git clone https://github.com/sarvalabs/moi-dataroom0.git`, then `cd moi-dataroom0` (the clone root, where git commands run), then `cd moi-data-room` for `npm ci` and the app commands below. Say source and size first | Yes given. `moi-data-room/package.json` exists |
| 3 | LOCAL | Identity and branch | In the clone: `bash "$SKILLS/moi-devrel/scripts/preflight.sh"`, then `git switch --no-track -c <name> origin/main` | No preflight FAIL |
| 4 | LOCAL | The environment | The operator creates `moi-data-room/.env.local` from the names in `dataroom-settings-and-database.md`. The template `.env.local.example` and a root `README.md` exist only on the previous operator's machine (ASK: Adithya for a copy). Claude never opens `.env.local` | The operator confirms it exists |
| 5 | LOCAL | Edit and run | `npm run dev` in `moi-data-room/` (localhost:3000). Note the PID and stop only that one | The operator has seen it |
| 6 | LOCAL | Check, because CI will not | `npx tsc --noEmit`; `npm run lint`; `npm run build` | All exit 0 |
| 7 | GATE | If the change needs SQL | Run it first and by hand: `dataroom-settings-and-database.md`. Code that needs a column fails until the column exists | The SQL ran, or no SQL is needed |
| 8 | GATE | Push and open one PR | "Ready to push `<branch>` (files: ...) to origin as `<login>` and open one PR against `main`. Yes?" Body is part A of `templates/change-checklist.md`. Past PRs came from branches pushed to the org repo (ASK: Rahul if you may) | PR open |
| 9 | GATE | Merge (this deploys) | Name the PR and "this deploys the Dataroom". Who approves is not recorded. ASK: Rahul | Merged |
| 10 | VERIFY | Read the live site | `gh run list -R sarvalabs/moi-dataroom0 --workflow "Deploy MOI Dataroom" --limit 3`, then `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" dataroom`, then open `/home` on desktop and on a phone, and the page you changed | The change is visible. Same KNOWN lines as step 1, no new FAIL |

A manual run: `gh workflow run "Deploy MOI Dataroom" -R sarvalabs/moi-dataroom0 --ref main` (GATE). It is how a changed secret reaches the VM.

## Quality rules the code sets
- Every admin API route must start with an admin check and return 403 without it (the rule in the previous operator's rewritten `AGENTS.md`, local only).
- Uploads are PDF, DOCX or PPTX under 50 MB (`upload/route.ts`, `upload-allowed.ts`). A PPTX is accepted and cannot be read (`dataroom-documents.md`).
- Chat copy leads with what MOI does for participants (people, businesses, AI agents) before internals such as TESSERACTs or Coco (system prompt in `chat/route.ts`). Terms: `moi-devrel/references/terminology.md`.
- Per-IP rate limits in `middleware.ts`: 60 requests a minute on API routes, 20 on chat, 10 on upload, 30 on admin. A script that loops will get 429.

## Traps
- `NEXT_PUBLIC_*` values are fixed at build. Changing one needs a redeploy, not a restart.
- A merged change was once not visible on 2026-08-21 and the previous operator had to find where it deployed. The SSH workflow above is the live path. Read the live site after every merge.
- `/` redirects to `/home`; `/events` still answers although the Events page was hidden from the menu on 2026-08-22.
- The home page shows hard-coded figures (`dataroom-health.md`, D-K2). A change to `src/lib/constants.ts` changes what investors read.
- Do not add a Vercel step to any deploy note. <!-- slop-lint: ignore -->

## Not yet known
- What the Dataroom deploy script on the VM does: build, restart, env file. ASK: Upendhar (Srikar wrote the workflow; ASK whether he still owns the VM).
- How long a deploy takes. ASK: Upendhar.
- Who reviews Dataroom pull requests. ASK: Rahul.
