# Traps: every way these three products give a wrong answer without an error

Facts are as of 2026-10-03 unless a row carries another date. Each row is a rule, the evidence behind it, and the file with the steps. Security findings are not listed here: see the sentence in `../GUIDE.md`. `DEPENDENCIES.md`, quoted in a few rows, is the previous operator's file: it is untracked and exists only on his machine (ASK: Adithya for a copy). Back to `../GUIDE.md`.

## All three products

| # | Rule | Evidence | Steps in |
|---|---|---|---|
| 1 | Merging to the deploy branch is the release: `main` for the website and the Dataroom, `feature/ci-cd` for Points. There is no staging step | `deploy.yml` of each, read 2026-10-03 | `*-ship.md` |
| 2 | No pull request runs lint or tests. Run the checks yourself and paste the result into the PR | The website runs only a preview build; the Dataroom has one workflow; Points has push triggers only | `*-ship.md` |
| 3 | A green workflow run is not a working change. Open the live page and read the data | Website: deleted blog posts survived deploys in August 2026 (2026-08-18) and a dead API hides behind a fallback calendar. Dataroom: no check after deploy. Points: `sha` is null | `*-health.md` |
| 4 | A setting the workflow does not list never reaches the app, whatever GitHub holds | All three deploy workflows hand over an explicit list | `*-settings*.md` |
| 5 | Secrets reach the VM only at deploy. Change one, then run the deploy on the right branch | Same lists | `*-settings*.md` |
| 6 | GitHub secrets cannot be read back and no shared vault exists. Put the old value in a vault before overwriting | `moi-devrel/references/keys-and-access.md` | `*-settings*.md` |
| 7 | The operator types a secret at a hidden prompt. Claude never sees, types or stores one, never opens an `.env`, and treats a pasted value as exposed | `moi-devrel/references/consent-and-identity.md` section 4 | `../GUIDE.md` |
| 8 | A manual workflow run takes the ref you pick. The website exports that ref name to its VM script. Run it on the deploy branch only | `deploy.yml` of the website passes `BRANCH=${{ github.ref_name }}` | `website-ship.md` | <!-- slop-lint:ignore -->
| 9 | The guides in the repos contradict the code. Trust workflow files, the code and live reads | `DEPLOYMENT.md` says the blog host does not exist; the website `CLAUDE.md` and `DESIGN_SYSTEM.md` describe the old look; the Dataroom `AGENTS.md` is boilerplate; the Points README describes a nightly audit that PR #21 removes; `DEPENDENCIES.md` says `pnpm db:generate` where the repo says not to | each file |
| 10 | Leftovers from the old host do nothing on the VMs: `vercel.json`, `api/`, the Vercel text in `AGENTS.md` and READMEs. Never write that host into a deploy note | An older copy of the website still answers 200 at moi-website.vercel.app; the Dataroom's old project answers 404 | `website-health.md` | <!-- slop-lint: ignore -->
| 11 | The corrected guides and templates exist only on the previous operator's machine, so ask for a copy before assuming `main` has them | `README.md`, `DEPLOYMENT.md`, `CONTENT.md`, a Dataroom README and env template, the Points operator notes | `who-to-ask.md` |
| 12 | Do not store connection strings or keys on a laptop. The one job that needs production values locally is the website ingest, and it uses a hidden prompt | The previous operator, 2026-09-15 | `*-settings*.md`, `website-chatbot.md` |
| 13 | Commit with the work identity and no AI trailer or footer. Run `bash "$SKILLS/moi-devrel/scripts/preflight.sh"` first, inside the working copy | 2026-05-29, 2026-06-08, 2026-09-02, 2026-10-01 in `moi-devrel/references/consent-and-identity.md` | `*-ship.md` |
| 14 | Never push, open a PR, merge or deploy without a yes that names the action | 2026-09-09, 2026-08-18 in `moi-devrel/references/consent-and-identity.md` | `../GUIDE.md` |
| 15 | Free Supabase plans have no downloadable backups. Points is on one; the others are unknown | `moi-devrel/references/keys-and-access.md` | `points-settings-and-database.md` |
| 16 | Install and clone steps are downloads. Ask first | Gate in `../GUIDE.md` | `*-ship.md` |

## Website and blog

| # | Rule | Evidence | Steps in |
|---|---|---|---|
| 17 | Judge the calendar from `GET /api/community-calls`, never from the homepage. The page shows a schedule written in code when the API fails or is empty | `CommunityCalendar.jsx` `buildScheduledEvents`; the API answers 500 (W-K1) | `website-calendar.md` |
| 18 | Fixing Supabase alone will not fix the homepage. The bundle calls `dev.moi.technology`, which answers HTML | Bundle `index-BBpe5QGW.js` on 2026-10-03 (W-K2) | `website-settings.md` |
| 19 | The first database row replaces the fallback, AMAs included. The table cannot hold an AMA category | `if (data.length) setEvents(data)`; the CHECK in `supabase-community-calls.sql` | `website-calendar.md` |
| 20 | The built-in schedule is a public statement. It shows a call on 2026-10-23 and an AMA on 2026-10-17 that nobody has confirmed, and it runs out after 2026-12-18 | Code read 2026-10-03; `moi-devrel/references/calendar.md` | `website-calendar.md` |
| 21 | Never run all of `supabase-community-calls.sql`: its last statement inserts seven placeholder events | The file | `website-database.md` |
| 22 | Never run `supabase-setup.sql` before you know which Supabase project the server uses. It may be Dataroom-shaped | GitHub issue 3 (open since 2026-04-20) | `website-database.md` |
| 23 | `npm run ingest` duplicates chunks when re-run. `ingest:clear` deletes every row first, before it looks for files, so with an empty `docs/` it empties the store | The website's `scripts/ingest.js` | `website-chatbot.md` |
| 24 | Ingesting changes nothing visitors see: the chat is hidden (`{false && (`, commit `6450d21`, 2026-06-08) and the widget file is imported nowhere | `HomePage.jsx` on `main` | `website-chatbot.md` |
| 25 | `docs/MOILitePaper.pdf` is not the file the site serves. Three paper paths drift | Git blob sizes 175,872 and 259,385 on `main` | `website-content.md` |
| 26 | Both builds must run. Only the blog build checks frontmatter; the root build exits 0 with a bad post | `moi-blog` | `website-ship.md` |
| 27 | After a delete, the blog URL must answer 404. The apex answers 200 for any address | `moi-blog` `check-live.py --expect-gone`; W-K3 | `website-health.md` |
| 28 | `public/sitemap.xml` is by hand. A new page needs a line | Its header comment | `website-content.md` |
| 29 | `VITE_GA_ID` and `PUBLIC_GA_ID` do nothing; measurement is Google Tag Manager | `git grep` on `main` | `website-settings.md` |
| 30 | The chat limiter allows 20 requests a minute per address and the app does not set `trust proxy`, so behind nginx visitors may share one address | `server/index.js` (inferred effect) | `website-chatbot.md` |
| 31 | A preview's `/blog` cards link to production, so a new slug 404s there. Read the post at its own preview URL | `moi-blog/references/publishing.md` | `website-ship.md` |
| 32 | PDFs are served without a download header, though `vercel.json` has the rule | HEAD read 2026-10-03 (W-K5) | `website-content.md` |
| 33 | PR #57 needs `moidocs` #124 merged first: the site links to a file that PR creates | `DEPENDENCIES.md` section 4 | `website-health.md` |

## Dataroom

| # | Rule | Evidence | Steps in |
|---|---|---|---|
| 34 | Embeddings fail silently: a failed batch is only logged, so a document can be `completed` with chunks missing; a PPTX is read with a library whose warning says it does not support PPTX; the job runs in the web process and is lost on restart (inferred) | `lib/embeddings.ts`, `documents/route.ts` | `dataroom-documents.md` |
| 35 | The chat hides search errors and still answers. Judge it by a question only the new file can answer | `app/api/chat/route.ts` | `dataroom-health.md` |
| 36 | Editing a document's file does not re-embed it. Re-index afterwards | `documents/[id]/route.ts` | `dataroom-documents.md` |
| 37 | Delete in the admin page is one click, with no confirmation, and removes the file, the row and the embeddings. There is no Unpublish button, and a draft's chunks may still be quoted by the chat | `admin/page.tsx`, `schema.sql` cascade, `migration-add-embedding-status.sql` | `dataroom-documents.md` |
| 38 | Two whitepaper rows and a Litepaper exist. `/home` tiles pick by slot, then by title. Read `/home` after any change | Document list 2026-10-03 | `dataroom-papers.md` |
| 39 | `set-whitepaper.mjs` has no dry run and renames the pinned document to "Litepaper" on every run | The script | `dataroom-papers.md` |
| 40 | The figures on `/home` are literals in `constants.ts` | Live page and source | `dataroom-health.md` |
| 41 | The repo SQL omits `adopters`, `document_leads` and `documents.require_email`. `schema.sql` fails on a second run. `seed.sql` deletes every document | The SQL files | `dataroom-settings-and-database.md` |
| 42 | Chat limits are in memory and reset on every restart, so every deploy resets them. `NEXT_PUBLIC_*` need a rebuild | `claude-budget.ts`; build-time variables | `dataroom-ship.md` |
| 43 | Per-address rate limits: 60 a minute on API routes, 20 on chat, 10 on upload, 30 on admin. A loop gets 429 | `middleware.ts` | `dataroom-admin.md` |
| 44 | The Events page is hidden from the menu since 2026-08-22 but `/events` answers 200, and it shows three sample events when `/api/events` fails. Judge it from the JSON | PR #5; GET 2026-10-03; `src/lib/events.ts` | `dataroom-admin.md` |
| 45 | Visitor emails in the admin page are personal data. Never paste them | Rule of this skill | `dataroom-admin.md` |

## Points Program

| # | Rule | Evidence | Steps in |
|---|---|---|---|
| 46 | The deploy branch is `feature/ci-cd`. `main` is stale since 2026-08-03 and has no workflow | `git ls-tree` of both | `points-ship.md` |
| 47 | The old container is removed before the new one starts, and there is no rollback at the tip | `deploy.yml` | `points-ship.md` |
| 48 | The app refuses to start when the database is behind the build, or when an enabled task lacks its environment. A merge that carries a migration is the deploy, so DevOps applies the migration before the merge. The 2026-09-15 order (migration-only pull request first) predates these checks | `lib/startup.ts`, `lib/db/migrations.ts`; git history of `lib/startup.ts` | `points-settings-and-database.md` |
| 49 | Write migrations by hand and journal them. Never run `pnpm db:generate`, `drizzle-kit push` or `pnpm db:reset:*` against anything but a local database | `drizzle/TRIGGERS.md` | `points-settings-and-database.md` |
| 50 | `.env` on the box is rewritten at every deploy, so hand edits are lost | `deploy.yml` (`cat > .env`) | `points-settings-and-database.md` |
| 51 | `sha` is null in `/api/health`, so the running build cannot be told. Read `migrations.applied` against `expected` instead of the status code | `/api/health` 2026-10-03 | `points-health.md` |
| 52 | A wrong `BETTER_AUTH_URL` breaks sign-in and the health origin. Google rejects a raw IP as a redirect | Failed runs and the 2026-09-15 error | `points-settings-and-database.md` |
| 53 | Sign-in emails need both `RESEND_API_KEY` and `EMAIL_FROM` | `lib/startup.ts` | `points-settings-and-database.md` |
| 54 | A task shows only when the database row is active and `config/reward-tasks.ts` says enabled. Points live in the database; `TASK_POINTS` is for display. An X campaign is not in `GET /api/tasks`; it shows on the member dashboard | `config/reward-tasks.ts`, `tasks.ts`, `app/api/tasks/route.ts` | `points-tasks.md` |
| 55 | A member without admin access who opens the admin page is sent to the dashboard. It looks like a bug and is not | `lib/admin.ts`; the redirect chain | `points-tasks.md` |
| 56 | `points_ledger` is append-only; `TRUNCATE` skips its trigger | `drizzle/TRIGGERS.md` | `points-settings-and-database.md` |
| 57 | Review tweaks go on one batch branch and one PR, not a PR per change | 2026-09-15; #16 to #20 folded into #21 | `points-ship.md` |
| 58 | X verification costs API budget; the previous operator had none for large reads | 2026-09-15 | `points-tasks.md` |

## Not yet known
- Whether any of these rows has been fixed since 2026-10-03. Re-run `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" all` and re-read the row's file before you rely on it.
