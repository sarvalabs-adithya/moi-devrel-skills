# Website health: is moi.technology up, and what is already broken

Facts are as of 2026-10-03 (GET and HEAD reads taken that day) unless a line carries another date. Sources: `sarvalabs/MOI-Website` `main` at commit `5e91afa`, the public GitHub API, the research note dated 2026-10-02. Back to `../GUIDE.md`.

Website: A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin.

## "The site is down": the first ten minutes

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Read the state | `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" website`. A single FAIL is not an outage: run it once more and read the host and the status | You know which lines FAIL. KNOWN lines are old news (table below) |
| 2 | CHECK | Narrow it | Static pages FAIL: the web server or the VM. Pages PASS but `/api/health` FAILS: the Express server on the VM. Only the blog FAILS: the blog host. Everything PASSES: it is the viewer's network or a cache | One sentence naming the layer |
| 3 | CHECK | Was it a deploy? | `gh run list -R sarvalabs/MOI-Website --workflow "Deploy MOI Website" --limit 3` (read-only) | You know whether a run failed or finished in the last hour |
| 4 | LOCAL | Record it | Copy `templates/incident-note.md`, fill what you saw, the UTC time and the run | The note exists |
| 5 | GATE | Ask DevOps | Draft with `templates/devops-request.md`; the operator sends it to Upendhar (`who-to-ask.md`). Include URL, status, UTC time, last run. Do not ask for a secret | The operator sent it |
| 6 | GATE | Do not redeploy to "fix" it | A manual run of "Deploy MOI Website" runs the same VM script. Run it only on `main`, on a yes (`website-ship.md`) | Only if the cause was a failed run |
| 7 | VERIFY | Confirm recovery | Step 1 again | No FAIL that was not there before you started |

There is no rollback input in `deploy.yml` (read 2026-10-03). To go back, revert the merge in a new PR (`moi-devrel/ship`); merging it deploys.

## What each check proves

| Check | Healthy | Reads |
|---|---|---|
| `GET /`, `/why-moi`, `/manifesto`, `/papers` | 200 | The app shell. This host answers 200 for any address, so these prove little (W-K3) |
| `GET /blog` | 200 | The generated post listing, a static file. It proves the root build ran |
| `GET /api/health` | 200 `{"status":"ok"}` | The Express server answers behind nginx (`X-Powered-By: Express`) |
| `GET /api/community-calls` | 200 and a JSON list, `[]` allowed | The calendar's database. Judge the calendar here, never from the homepage (it falls back to a schedule in code) |
| Main script | no `dev.` host in the baked API base | Whether the browser can reach the API (W-K2) |
| Blog `/`, `/rss.xml`, `/rss-email.xml`, `/sitemap-index.xml`, `/llms.txt` | 200 | The Astro build and its feeds |
| Blog unknown article | 404 | The blog host gives a real 404. Use it to judge a deleted post (`moi-blog`, `check-live.py --expect-gone`) |
| Feed against listing | every feed slug is in apex `/blog` | A post live on the blog and missing from the listing means the root build did not run |

## Known faults (the script prints these as KNOWN)

| ID | Fault | Fix path | Who |
|---|---|---|---|
| W-K1 | `GET /api/community-calls` answers 500 `{"error":"Internal server error"}`. GitHub issue 3 (opened 2026-04-20, still open; the public text is about the chat's Supabase function name) | `website-database.md`, "Find the right project" | Upendhar (log), the Supabase owner (ASK: Rahul) |
| W-K2 | The live bundle `index-BBpe5QGW.js` has `https://dev.moi.technology/api` baked in as the API base. The code appends `/api/community-calls`, so the browser asks a host that answers HTML. That host answers 200 text/html for any path (2026-10-03). The homepage then shows its built-in schedule, and the calendar admin page cannot save | `website-settings.md`, "Fix the baked API base" | Upendhar |
| W-K3 | Unknown addresses answer 200 with the app shell | An nginx change on the VM. `DEPENDENCIES.md` section 4 ToDo 4 (ASK: Adithya for a copy) | Upendhar |
| W-K4 | No discovery `Link` header on `/` | Same nginx change | Upendhar |
| W-K5 | `/papers/moi-white-paper.pdf` has no `Content-Disposition`. `vercel.json` has the rule and nginx does not apply it. On 2026-08-18 the previous operator noted "ask srikar about the papers nginx fix"; no fix is live | nginx on the VM | Upendhar (Srikar asked first, ASK whether he still owns it) |
| (none) | The chat is hidden in the UI since 2026-06-08 and its widget file is imported nowhere | `website-chatbot.md` | Rahul decides |
| (none) | Open PRs on 2026-10-03: #57 (prerender, performance, metadata; merge `sarvalabs/moidocs` #124 first, the site links to a file that PR creates), #56 (September release social copy, never merged), #54 (x402 post, draft), #52 (access policies post, open since 2026-08-31), #8 (Cloudflare preview test, open since 2026-08-10) | `moi-blog` for #56, #54, #52. ASK: Rahul what to do with #8 | Rahul |
| (none) | `vercel.json` and `api/` are leftovers from the old host. An older copy of the site is still live at moi-website.vercel.app (200 on 2026-10-03). It is the previous operator's own copy (`sarvalabs-adithya/moi-website`, per `DEPENDENCIES.md`) and is to be taken down | ASK: Adithya | Adithya |
| (none) | Stale guides on `main`: `DEPLOYMENT.md` says the blog host does not exist yet, `CLAUDE.md` and `DESIGN_SYSTEM.md` describe the old look, `README.md` names a `CHATBOT_PROCESS.md` that does not exist. Corrected copies are uncommitted on the previous operator's machine | ASK: Adithya for a copy | Adithya |

## By hand, because the script cannot

| Check | How | Note |
|---|---|---|
| The chat endpoint validates input (GATE: it is a POST, so ask first) | `curl -s -X POST https://moi.technology/api/chat -H 'content-type: application/json' -d '{}'` | One POST with an empty body, rejected before any model call. The server code (`server/index.js`) answers 400 `{"error":"message is required"}`; no one has recorded running it. If it answers, it proves the route exists, not that answers work |
| A deploy run | `gh run list -R sarvalabs/MOI-Website --workflow "Deploy MOI Website" --limit 3` | Green proves only that the VM script returned |
| A new post is live | `python3 "$SKILLS/moi-blog/scripts/check-live.py" <slug>` | `moi-blog` owns it |
| A preview | Open the two URLs in the PR comment | `website-ship.md` |
| Measurement | Google Tag Manager container `GTM-M4BR46Z2` is in `index.html`; the GA4 tag lives inside it | ASK: Rahul who owns Analytics and Tag Manager |

## Not yet known
- Whether a Supabase project or a code path is the cause of W-K1. The handler logs `Fetch calls error:` with the reason. ASK: Upendhar for that line.
- What the VM script does, and how long a deploy takes. ASK: Upendhar for a copy of the website deploy script (it is not in git).
- Who is paged when the site is down, and whether anything watches it. ASK: Rahul.
