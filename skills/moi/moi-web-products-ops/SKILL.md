---
name: moi-web-products-ops
description: "Operate MOI's three web products: the website (moi.technology, with its chatbot, the homepage community call block that links to Luma, and the blog build), the Dataroom (dataroom.moi.technology, the investor document room whose chat answers from uploaded papers) and the Points Program (points.moi.technology, where members earn points for tasks, X campaigns and webinar bounties). Use for \"moi.technology is down\", \"health check\", \"ship a website change\", \"update the next community call on the homepage\", \"Luma link\", \"turn the chatbot back on\", \"add a paper\", \"replace the whitepaper\", \"upload to the Dataroom\", \"embedding failed\", \"add an adopter\", \"add a points task\", \"X campaign\", \"webinar bounty\", \"grade a bounty\", \"dev challenge\", \"rotate a secret\", \"what do I ask DevOps\". Holds one runbook per job, a read-only health script, the traps and the gates. Writing a post is moi-blog; the session itself and its bounty brief are moi-webinar; commits and merges are moi-devrel/ship."
---

# MOI web products: operations

`$SKILLS`, the operator, `ASK:`, the house rules and the general gates are defined in `moi-devrel/SKILL.md`, the main skill; this skill adds what is specific to the three products.

## What this covers
Three live products with one shape: a repo in the `sarvalabs` org, a Supabase database, a deploy that fires on merge, and a VM that DevOps owns. Files marked "updated 13 October 2026" are current to that day; the others are as of 2026-10-03 (live reads) and 2026-10-02 (research) unless dated. In all three, merging to the deploy branch is the release, and no pull request runs tests.

| Product | Live | Repo | Deploys on | Reaches the VM by |
|---|---|---|---|---|
| Website, chatbot, Luma community block, blog build | moi.technology, blog.moi.technology | `sarvalabs/MOI-Website` (public) | merge to `main` | Actions, Teleport, a script on the VM |
| Dataroom | dataroom.moi.technology | `sarvalabs/moi-dataroom0` (public) | merge to `main` | Actions, SSH, a script on the VM |
| Points Program | points.moi.technology | `sarvalabs/moi-project` (private) | push to `feature/ci-cd`, not `main` | Actions, image, Teleport, one container |

Not covered: writing and announcing a post (`moi-blog`), search and AI visibility (`moi-docs/geo`), commits, pull requests and merges (`moi-devrel/ship`), the message to DevOps (drafts in `moi-devrel/templates/messages.md`, checker `moi-devrel/scripts/check-message.py`; the requests these products need are in `references/who-to-ask.md`), visual brand (`moi-devrel/design`), claims on a page (`moi-devrel/claim-check`), what to redo after a devnet reset (`moi-devnet-reset`).
**Ownership.** DevRel owns the code and the content of all three; DevOps owns the servers: Srikar the website server, Upendhar the Points box, and for the Dataroom server ASK: Rahul which of them acts (the full table is `references/who-to-ask.md`). Open per product:
- Website: the repo admins and the Supabase project (not recorded). No company-owned OpenAI, Anthropic or Groq key exists.
- Dataroom: the repo admins. Its Supabase project is in the company organisation since 8 October (check the plan has backups).
- Points: the database sits on the Points Program's own email account (free plan, no backups). Its five repo admins are known. Google, X, Discord, Telegram, Reown, Resend, Analytics, Tag Manager and Search Console are under the `sarvalabsdeveloper@gmail.com` login.

## Before you start
Run every command from the working copy of the repo you are changing, with the path quoted. The health script needs no repo and no key.
Terms. *Luma*: the event-calendar service the community calls are listed on. *Express*: the small Node web server behind the website's `/api` routes (chatbot included). *VM*: the server a product runs on. *Teleport*: how a GitHub workflow reaches a VM. *GHCR*: GitHub's container registry, where the Points image is stored. *Supabase*: the hosted Postgres database each product uses. *Embedding*: the numeric index of a document's text that the Dataroom chat searches. *Hero slot*: one of the seven document tiles on the Dataroom home page. *PASS, WARN, KNOWN, FAIL*: the health script's levels (a KNOWN line is a recorded fault).
- [ ] The product and the job in one line. The operator. Ask: "Which product, and what should be true at the end?"
- [ ] A health baseline, run by Claude from any folder: `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" all`. KNOWN lines are recorded faults, not new ones.
- [ ] `gh` installed and signed in with read access to the sarvalabs repos. ASK: Rahul.
- [ ] Work identity: `bash "$SKILLS/moi-devrel/scripts/preflight.sh"` from inside the working copy of the repo, before any commit.
- [ ] Access. Repo access and repo admin (for secrets) come from an org admin; the Supabase dashboards and vendor logins belong to owners who are mostly unrecorded (`moi-devrel/references/keys-and-access.md`). ASK: Rahul. Claude never signs in to GitHub settings, Supabase or a vendor console, and never opens an `.env`.
- [ ] Security. Each product carries the sentence below, and nothing more is written down here. A step marked ADMIN needs the operator to confirm first that the handover note was read.
  - Website: A security finding is open on this product as of 2026-10-02. The handover note is the Open items of `project-handover-docs/MOI-WEBSITE.md`; read it before touching its admin.
  - Dataroom: A security finding is open on this product as of 2026-10-02. The handover note is the Open items of `project-handover-docs/DATAROOM.md`; read it before touching its admin.
  - Points: A security finding is open on this product as of 2026-10-02. The handover note is the Open items of `project-handover-docs/POINTS-PROGRAM.md`; read it before touching its admin.

## The run
Runbook tables use four kinds of step: CHECK (read-only, always first), LOCAL (changes only files on this machine), GATE (needs the operator's yes, see Gates) and VERIFY (read-only, last).
If you were woken, start with the script and the right table:

| Someone says | Run first | Then read |
|---|---|---|
| "moi.technology is down or slow", "the blog is missing a post" | `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" website` | "The site is down" table in `references/website-health.md` |
| "the community call is missing or wrong on the homepage", "the Luma link" | `gh api -H "Accept: application/vnd.github.raw" repos/sarvalabs/MOI-Website/contents/content/community-calls.json` | `references/website-calendar.md` (the block is hidden while `lumaUrl` is empty) |
| "the Dataroom is down", "the chat does not know the new deck" | `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" dataroom` | "The Dataroom is down or wrong" table in `references/dataroom-health.md` |
| "Points will not load", "sign-in fails", "points are missing" | `curl -s https://points.moi.technology/api/health` | "Points is down" table in `references/points-health.md` |
| "a deploy just ran and something changed" | `gh run list -R <org/repo> --limit 3` (the repo from the first table), then `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" <product>` | The product's `*-ship.md`, VERIFY row |

The run, for every job:

| # | Step | What to do | Where | Done when |
|---|---|---|---|---|
| 1 | Name the job | Product, job, and the one line of what should be true after | The table under "Which file to read" | One runbook file is chosen |
| 2 | Baseline | Run the health script from any folder and keep the output in the conversation (step 4 copies it into the checklist) | `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" <website\|dataroom\|points\|all>` | Output read, KNOWN ids noted |
| 3 | Read before touching | The runbook, its "Not yet known", then `references/traps.md` for any change | The chosen file | Each unknown that touches the job is an ASK for the operator |
| 4 | Prepare | A code or copy change gets a branch of a working copy (the product's `*-ship.md` says how to get one); an admin-only job has no branch. Fill the checklist: part A goes in the PR body, part B (gate answers, people, accounts) stays out of any public repo, in a folder made from the root of the working copy, or from a folder outside any repo, with `mkdir -p web-ops-<slug> && printf '*\n' > web-ops-<slug>/.gitignore` | `templates/change-checklist.md` | The checklist shows the order of work |
| 5 | Ask at each GATE | `Ready to <action> on <product>: <object>. Yes?` One yes covers one action | The runbook's GATE rows | The yes is quoted in the checklist |
| 6 | Wait for the deploy | A merge deploys. Read the run, not the clock | `gh run list -R <org/repo> --workflow "<name>" --limit 3` | The run finished |
| 7 | Verify from data | The runbook's VERIFY rows, then the script again. A 200 or a green run proves little | The health script (step 2 command) and the runbook | No new FAIL, and the change seen live |
| 8 | Record | When something broke, fill the incident note. A DevOps ask uses the skeleton | `templates/incident-note.md`, `templates/devops-request.md` | The operator has both |
| 9 | Hand back | The format below | Hand-back | Ready: yes or no, with the reason |

## Which file to read

| Asked to | Product | Read |
|---|---|---|
| Ship a code or copy change; a manual deploy run | Website | `references/website-ship.md` |
| Set the Luma link or the next community call on the homepage; "the community block is missing" | Website | `references/website-calendar.md` |
| Update what the chatbot knows; turn it back on | Website | `references/website-chatbot.md` |
| Add a page, a paper or a PDF; edit the sitemap | Website | `references/website-content.md` |
| Change a key, a variable, the API address | Website | `references/website-settings.md` |
| Supabase tables and SQL; the old calendar API answers 500 | Website | `references/website-database.md` |
| "The site is down"; health after a deploy; known faults | Website, blog | `references/website-health.md` |
| Ship a change | Dataroom | `references/dataroom-ship.md` |
| Add, replace, unpublish or re-index a document | Dataroom | `references/dataroom-documents.md` |
| Replace the whitepaper or litepaper everywhere | All three places | `references/dataroom-papers.md` |
| Admin page: adopters, events, leads | Dataroom | `references/dataroom-admin.md` |
| A secret, a chat limit, SQL | Dataroom | `references/dataroom-settings-and-database.md` |
| "The Dataroom is down or wrong"; embeddings | Dataroom | `references/dataroom-health.md` |
| Ship a change | Points | `references/points-ship.md` |
| A task, an X campaign, a webinar bounty (create, open, grade, close), the legacy dev challenge | Points | `references/points-tasks.md` |
| A secret, a variable, a migration | Points | `references/points-settings-and-database.md` |
| "Points is down"; member errors | Points | `references/points-health.md` |
| Who owns it, who acts on a VM, what to ask DevOps | All | `references/who-to-ask.md`, `templates/devops-request.md` |
| Every trap in one list | All | `references/traps.md` |
| Testing a change to this skill | | `evals/evals.md`, `examples/README.md` |

## Facts that fail silently

| Rule | The incident |
|---|---|
| Merging is deploying. Open the live page and read the data | Deleted blog posts survived deploys in August 2026 while the run was green (2026-08-18) |
| A setting the workflow does not list never reaches the app, and secrets travel only at deploy | `VITE_GA_ID` and `PUBLIC_GA_ID` are passed and read by nothing; the website server reads `ALLOWED_ORIGINS` and `PORT`, which the workflow does not pass |
| The homepage community block is built from `content/community-calls.json` and hidden while `lumaUrl` is empty | An empty block is correct on 13 October 2026; the old `/api/community-calls` is not what visitors see (PR #60) |
| The website host answers 200 for any address | `/zz-no-such-page` answers 200 with the app shell (2026-10-03) |
| Read `embedding_status` after an upload and ask one question only the file answers | Six of 23 Dataroom documents are not fully embedded (2026-10-03); the chat answers even when search fails |
| Points: the database first, the code second. A merge that carries a migration is the deploy | A build ahead of the database refuses to start, and the old container is already removed |
| The SQL files in the repos do not describe production | Two Dataroom tables and a column were made by hand; the website's Supabase project may be Dataroom-shaped (inferred) |
| A paper has up to four copies that drift | The litepaper copies are two different files (259,385 and 175,872 bytes) |

## Gates
The gates in `moi-devrel/SKILL.md` apply. These are specific to the web products, and none happens without the operator's explicit yes in this conversation. A merge to a deploy branch is a deploy.
- Push, open, update or close a pull request, merge, and any manual workflow run (the website's only on `main`).
- Any download: a clone, `npm ci`, `pnpm install`.
- Setting or changing a GitHub Actions secret or variable. The operator types the value at a hidden prompt.
- Any write to a production database: a SQL run, a migration, `npm run ingest`, a Re-index, and a Dataroom chat question (the app logs each question in `chat_queries`).
- Any admin write on production: document upload or delete, adopters, campaigns, tasks, `set-whitepaper.mjs`.
- Opening, awarding, rejecting or closing a bounty, or any action that pays points: members see it and the ledger cannot be edited.
- Any request that is not a GET or HEAD to a live product, even one rejected before a model call (the empty-body chat checks).
- Uploading or sharing a file in cloud storage; deleting a document, an event, an adopter or a table.
- Anything on a VM (restart, nginx, environment, deploy script, migration run). Only DevOps does it. Claude drafts the request and the operator sends it.
- Spend: a chat question, an ingest, any bulk model run. State the count first.
- Spending devnet funds or deploying on devnet for a challenge test. The end-to-end test needs a wallet: its steps are the operator's, and Claude never handles a recovery phrase, a throwaway one included.
Details: `moi-devrel/references/consent-and-identity.md`.

## Keys and access
Names only; values never. Where each lives, who grants it and its status: `moi-devrel/references/keys-and-access.md` (status TBD until the owner settles access, ASK: Rahul).
- Website: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`, `VITE_CHATBOT_API`, `ADMIN_API_KEY` (a fix is pending; see `project-handover-docs/MOI-WEBSITE.md` open items), `ALLOWED_ORIGINS`, `PORT`, `TELEPORT_*`. The model keys are not company keys: none exists yet. (`DATA_ROOM_API_KEY` and `DATA_ROOM_CHAT_URL` are read only by the old host's function and the dev proxy.)
- Dataroom: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `ADMIN_SECRET`, `ADMIN_TOKEN` (a fix is pending; see `project-handover-docs/DATAROOM.md` open items), `CLAUDE_*` limits, `VM_HOST`, `VM_USERNAME`, `VM_SSH_KEY`.
- Points: `DATABASE_URL`, `BETTER_AUTH_SECRET`, `CRON_SECRET`, `GOOGLE_*`, `X_*`, `DISCORD_*`, `TELEGRAM_*`, `RESEND_API_KEY`, `EMAIL_FROM`, `ADMIN_EMAILS` (the only source of admins), `MOI_RPC_URL`, `GHCR_PAT`, `TELEPORT_JOIN_TOKEN`.

## Hand-back
```
Product and job: <...>
Produced: <what, with the URL or path>
Health: before <KNOWN ids, FAIL count> / after <...>
Remaining: <numbered, each with an owner>
Not verified or simulated: <say so, or none>
Ready: yes or no, because <one reason>
Next steps: <one to three>
```
A status lists only work that was done. Planned work is labelled as a to-do.
