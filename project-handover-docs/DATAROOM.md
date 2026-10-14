# Dataroom

**Status: active.** The site and the documents are live. Inactive: the chat (widget hidden since August 2026; the route is still deployed) and the Events page (hidden since August 2026).

Video: product demo https://drive.google.com/file/d/1FoOifehdhrH3hfrRJcbmim1WnRRBEXH5/view (recorded 13 October 2026). The skill video (moi-web-products-ops) is not recorded yet.

Marketing: How it works, Variables, Open items. Developers: Stack, Env vars, Process, Claude skill, Open items.

dataroom.moi.technology is the investor document room: the whitepaper, litepaper, decks and papers, with a chat that answers questions from those documents. Anyone can open it; there is no login. Adithya built it and DevRel runs it. DevOps owns the server.

## How it works

### The admin page

- Sign in at the admin page with the admin secret, in a private window that you close afterwards. There is no user login anywhere else on the site; the admin page is the only gate.
- The page offers: Add Document; a row per document with Edit, the Download and **Email gate** toggles (the email gate makes visitors leave an email before they can download), Re-index and Delete; Captured Leads; Calendar events; Adopters Management (a form, or Import CSV); and summary figures (documents, indexed, views, chat questions, leads).
- The toggles and the Re-index button swallow errors, so re-read the state after every click.

### How the home page works, and how to edit it

- The home page has seven hero **tiles** (the large cards at the top), one per **home slot** (a named place on the page): foundation (the Math paper), paradigm (Contextual Compute), network (the Whitepaper), pitch-deck (the IM deck), two-pager (the CC intro), litepaper, and gtm-deck.
- What a tile shows is written in the code, not in the database. Its title, tag and the italic line under it come from the HERO_CARDS array in moi-data-room/src/lib/constants.ts. The document's own title and description never appear on the tile. To change a tile's wording, edit that array, open a PR and merge (that deploys).
- What a tile opens is decided by pinning. "Show on home" in a document's form pins it to a slot; one document per slot, and pinning a new one clears the old holder. A tile with nothing pinned falls back to a title match (the matchCategory and matchTitleHint fields of the same array), which is why two documents with similar titles can swap places. Pin, do not rely on the match.
- Below the tiles, documents are listed by section: Contextual Compute, Engineering, Business & GTM, Tokenomics, Research, Use cases. The section is the document's category.
- A document's title and description show in that list and on its own page. Edit them in the admin page: click Edit on the row, change the title, description, category, link, the download and email toggles or the home slot, and Save. Editing never re-indexes the file. Changing the category clears the title and description, so pick it first.
- The headline figures under "Network & Community" (Accounts, Interactions, Consensus Nodes, Community, KMOI TVL, each with a value and a delta) are the STATS array in moi-data-room/src/lib/constants.ts. They are typed by hand, not computed. Change them in the code, source them, or drop them.
- The Adopters page lists what the admin Adopters section holds.

### How Supabase is used

- One Supabase project, in the company organisation since 8 October 2026. The plan should be a paid one so the daily backups exist; check.
- One Postgres database. Tables: documents (one row per document, with its category, home slot, toggles and index status), document_embeddings (the chunks and their vectors, through the vector extension), analytics (views and downloads), chat_queries (the questions asked), calendar_events, adopters, document_leads (the emails visitors leave for a gated document) and profiles.
- One private storage bucket, investor-docs, for the files. The browser uploads straight into it with the anon key; everything else goes through the server with the service-role key, which never reaches the browser.
- The schema is supabase/schema.sql plus the migration files beside it. There is no migration runner: run a new file by hand in the SQL editor before the code that needs it merges. PR #7 (merged 13 October 2026) added the file for the three objects that had been made by hand.
- The dashboard is also where to look when something is wrong: Table editor for a document's row and status, Storage for the file, Logs for failed queries.

## Stack

| Piece | What it is |
|---|---|
| Next.js 16 + React 19 + TypeScript + Tailwind 4 | The site, the admin page and every API route, in the moi-data-room folder of the repo |
| Supabase | A hosted Postgres database with the vector extension (it stores the document index), and a private bucket for the files |
| pdf-parse, mammoth, OpenAI embeddings | Read each upload (PDF or Word; PowerPoint cannot be read), cut the text into **chunks** (short passages) and index them for the chat with **embeddings** (numbers that let the chat find the passages closest to a question) |
| Claude | The chat, inactive: its widget is hidden since August 2026, the route is still deployed. It answers only from the indexed documents |
| GitHub Actions + SSH | A merge to main runs a script on the server that builds and restarts |

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Codebase | DevRel | https://github.com/sarvalabs/moi-dataroom0, public. Merging to main deploys. DevRel pushes branches to it. The fork sarvalabs-adithya/MOI-dataroom holds only the unmerged security branch |
| Supabase project and bucket | Company Supabase organisation (transferred 8 October) | Holds the documents (whitepaper, litepaper, decks, papers) and their index |
| Server, nginx, the SSH key, the deploy script | DevOps | The deploy script lives on the server, not in the repo |
| Domain dataroom.moi.technology | DevOps | |

## Env vars

The index across every product, with the consoles and who holds each login, is ENV-VARS.md.

Production values are GitHub Actions secrets on sarvalabs/moi-dataroom0. They cannot be read back; the readable copy is on the server, through DevOps. Locally, the values live in moi-data-room/.env.local, copied from the example file. A changed secret needs a manual run of the deploy workflow. Anything starting NEXT_PUBLIC_ is baked in at build, so it needs a rebuild.

| Variable | What it is | Where the value comes from |
|---|---|---|
| NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY | The database and bucket, from the browser. The **anon key** is Supabase's public key, safe to ship to the browser | Supabase dashboard, the project, Settings, API |
| SUPABASE_SERVICE_ROLE_KEY | The same, server side only. The **service-role key** is Supabase's all-access key and must never reach the browser | Same page |
| ANTHROPIC_API_KEY | The chat (inactive). Not a company key: no company-owned Anthropic key exists as of October 2026, so create one before relying on the chat | console.anthropic.com, API keys |
| OPENAI_API_KEY | The document index. Missing, every upload ends failed and the chat answers without document text. Not a company key: no company-owned OpenAI key exists as of October 2026, so create one before relying on the index | platform.openai.com, API keys |
| ADMIN_SECRET | The admin page. Never leave it empty | Generate with: openssl rand -hex 32 |
| CLAUDE_PER_IP_HOURLY_LIMIT, CLAUDE_DAILY_TOKEN_BUDGET, CLAUDE_MAX_INPUT_TOKENS, CLAUDE_MAX_OUTPUT_TOKENS | Chat limits. Optional; defaults in the code (30, 500000, 8000, 2048), reset on every restart | Set by nothing as of October 2026 |
| VM_HOST, VM_USERNAME, VM_SSH_KEY | Deploy access | DevOps |
| ADMIN_TOKEN, DATAROOM_URL | Read by the code, set by no deploy. ADMIN_TOKEN is a second admin check in the stats route on main; unset, that route answers any caller (the fix is on the fork branch). DATAROOM_URL is the whitepaper script's target, defaulting to the live site | Set ADMIN_TOKEN once the security fix merges (see Open items); until then the stats route answers anyone. Leave DATAROOM_URL unset |

The example file with comments is moi-data-room/.env.local.example (added by PR #7, merged 13 October 2026).

## Process

**Shipping a change**

- Work on a branch and push it to the repo.
- Run the type check, lint and the build by hand. No pull request runs them.
- Open a pull request and merge it. No reviewer is on record.
- Merging to main deploys: GitHub Actions reaches the server over SSH and runs its script.
- Open the site afterwards, on a phone too. Nothing checks it for you.
- There is no rollback. Revert in a new pull request.

**Adding a document**

- Prepare a PDF or Word file under 50 MB. PowerPoint is accepted but cannot be read, so convert a deck to PDF first.
- In the admin page, click Add Document. Pick the category first (changing it later clears the title and description), then fill in the title, description, the file or an external link (an https address such as a Zenodo record), allow download, require email, and the home slot if it should be a tile.
- Upload. The browser sends the file straight to the storage bucket, then the row is created.
- Indexing starts on its own: the server extracts the text, cuts it into chunks and embeds them, and the status goes pending, processing, completed. Wait for completed. If it stays at processing or ends failed, press Re-index on its row, one document at a time, and read the status again.
- If the document has a tile, check the home page afterwards, on a phone too.
- Uploads are limited to 10 a minute.

**Replacing the file inside a document**

- Editing a document does not re-index its file. Upload the new version as a new document with the same section, title and home slot (pinning moves the tile), wait for completed, then retire the old row.
- For the whitepaper and litepaper, use the swap script in the repo. It replaces the paper everywhere it is referenced; check the tile and the download afterwards. The script renames the old tile document to "Litepaper" on every run, which was right once and is wrong now, so fix or skip that step first.

**Deleting a document**

- Delete is one click on the row, with no confirmation, and it is permanent: the stored file, the row and its index all go.
- There is no unpublish button. Keep a copy of the file somewhere else before deleting, or rename the row instead.
- After a delete, open the home page. A tile that pointed at the deleted document must not be left broken.

**Adopters, events and leads**

- Adopters: add one by form, or use Import CSV. The header needs Name (or Project Name); Description, Link and Type (business or dapp) are optional. Each row is sent one at a time and the API allows 60 calls a minute, so split a long list. Adopters show on the Adopters page.
- Calendar events: add, edit and delete in the admin page. The Events page itself has been hidden from the menu since August 2026.
- Captured Leads: the emails visitors leave to download a gated document. They are personal data: read them on screen, do not copy them anywhere, and settle who may see them.

**Re-enabling the chat**

The chat was hidden on 21 August 2026 by the commit "chore: hide chat assistant widget for now" (a5544a8), which removed the widget from the page. The widget component and the chat route are still deployed. To bring it back:

1. Settle the Anthropic key. ANTHROPIC_API_KEY is in the repo's Actions secrets. No company-owned Anthropic key exists as of October 2026, so this is not a company key: create a company Anthropic account with billing, make a key, replace the secret, and check in the console that the key is live. OPENAI_API_KEY, which embeds the question and the documents, is in the same position: replace it with a company key too. Which account holds the current keys is an open question (Open items).
2. Make sure every document says completed in the admin page. As of October 2026 six do not: one failed (likely no text in the file) and five are stuck at processing, the whitepaper among them. Re-index them one at a time from the admin page, and re-read the status after each click, because the button swallows errors. The chat answers only from the index, so with the whitepaper unindexed it cannot answer the most basic questions.
3. Update the model. The chat route (moi-data-room/src/app/api/chat/route.ts) pins claude-sonnet-4-20250514, which is old. Move it to a current model id and run one question locally.
4. Put the widget back: revert commit a5544a8 on a branch.
5. Set the limits if the defaults do not suit (30 questions per address per hour, 500,000 tokens a day, 8,000 input and 2,048 output tokens): the four CLAUDE_ names as Actions variables plus a line for each in deploy.yml, because the deploy passes none of them as of October 2026.
6. Open the PR and merge (deploys).
7. Test on the live site: one question the whitepaper answers, one it cannot. The first should cite documents, the second should refuse cleanly. Watch the "Chatbot Questions" figure in the admin page, and the usage in the Anthropic console the next day.
8. Change the Status line of this doc.

**Re-enabling the Events page**

The Events page is off for now (decided 9 October 2026). The commit "chore: hide Events from sidebar nav for now" (5952d9a) hid it on 22 August by removing one line from the NAV_ITEMS list in moi-data-room/src/lib/constants.ts. Everything else is still there: the page at /events answers, its API routes, the admin Calendar events section and the calendar_events table. To bring it back:

1. Get the dates from Vardan and enter them in the admin page under Calendar events, so the page is not empty on day one.
2. Put the nav line back: revert commit 5952d9a, or add `{ id: "events", label: "Events", icon: "▦", href: "/events" }` after the Home entry in NAV_ITEMS.
3. Open a PR and merge (deploys).
4. Open /events and the sidebar on a phone.
5. Change the Status line of this doc.

**Changing a setting or a secret**

- Set it in GitHub, under the repo's Actions secrets and variables, then run the deploy workflow by hand. Setting a value deploys nothing on its own.
- Values that start with NEXT_PUBLIC_ are baked in at build, so they need a rebuild, not a restart.
- Rotating the admin secret, done on 9 October 2026: `openssl rand -hex 32 | gh secret set ADMIN_SECRET -R sarvalabs/moi-dataroom0`, then `gh workflow run "Deploy MOI Dataroom" -R sarvalabs/moi-dataroom0 --ref main`. Keep the value in the password manager; GitHub cannot show it back. Every admin browser signs in again afterwards.

**Changing the database**

- Write the SQL file and run it by hand in the Supabase SQL editor before the code that needs it merges.

**Checking it is healthy**

- Open the home page and one document.
- A wrong admin key must be refused: `curl -s -X POST https://dataroom.moi.technology/api/admin/unlock -H 'content-type: application/json' -d '{"key":"x"}'` answers 403 with "Invalid key".
- In the admin page, every document should say completed.
- The chat is inactive, so there is nothing to ask it. Check that uploads still index.

## Claude skill

The **moi-web-products-ops** skill covers the Dataroom with its dataroom runbooks: shipping, documents, the papers swap, admin, settings and database, health.

| When | What to tell Claude | What the skill does |
|---|---|---|
| Something looks wrong | "Is the Dataroom healthy?" | Runs a read-only health check on the live site, including which documents are indexed, and names the known faults. |
| Shipping | "Ship this Dataroom change." | Walks the branch, the local checks and the pull request, and says what merging will deploy. |
| A document | "Add this paper to the Dataroom." | Gives the upload steps and the check that it is indexed. The upload itself is DevRel's. |
| The whitepaper | "Replace the whitepaper." | Walks the swap script and the checks after it. |
| A setting | "I need to change this Dataroom setting: ..." | Says where it is set and whether it needs a rebuild. It never sees the secret's value. |
| The database | "I need a table for ..." | Writes the SQL and says when to run it. DevRel runs it in Supabase. |

Without a yes from DevRel, the skill never pushes, merges (a merge deploys), runs a workflow, runs SQL against production, changes a secret, or touches anything on the server. It does not touch admin until the person running it has read the security note (the first Open item).

## Open items

- The admin check is weak. The cookie carries the secret itself and scripts can read it, the comparison is not timing-safe, and the admin stats route on main accepts a built-in cookie value written in the source (the repo is public). With ADMIN_TOKEN unset, that route answers any caller with the question count and the top documents. The fix (a safe comparison, an httpOnly cookie, empty secret means no admin) sits on the fork branch claude/security-vulnerability-analysis-dWvYu from 23 March, 62 files behind the current main: rebase it, keep the auth changes, open the PR, merge (deploys). The branch is on Adithya's fork; copy it to sarvalabs/moi-dataroom0 first, so it survives if his GitHub account goes. ADMIN_SECRET was rotated and redeployed on 9 October; rotate it once more after that merge.
- There are two whitepaper rows, one on the home tile and one indexed. Find which is current and keep one. The swap script renames the tile's document on every run; fix that first.
- The figures on the home page are typed into the code with no source. Source them or drop them.
- PR #7 (the README, the env template and the migration for the adopters and document_leads tables and the require_email column) merged on 13 October 2026. Run the migration file once in the SQL editor if it has not been run; on production it changes nothing.
- The deploy runs /root/scripts/deploy-moi-dataroom.sh, a file that exists only on the server, so nobody can read or review what a deploy does. Put a copy in the repo and make the workflow run that copy. Then add a step after it that opens the site and checks a wrong admin key is refused, so a broken deploy turns the run red instead of green.
- The Events page stays off for now; the steps to bring it back are under Process.
- Which account owns the Anthropic and OpenAI keys now in the repo's Actions secrets is not recorded. Find out, then replace both with company keys (see the chat steps and the Env vars table).
