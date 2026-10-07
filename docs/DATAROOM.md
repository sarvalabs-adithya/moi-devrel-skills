# Dataroom

**Status: active.** The site and the documents are live. Inactive: the chat (widget hidden since August 2026; the route is still deployed) and the Events page (hidden since August 2026).

dataroom.moi.technology. The investor document room: the whitepaper, litepaper, decks and papers, with a chat that answers questions from those documents. Anyone can open it; there is no login. I built it and run it. DevOps owns the server.

## Stack

| Piece | What it is |
|---|---|
| Next.js 16 + React 19 + TypeScript + Tailwind 4 | The site, the admin page and every API route, in the moi-data-room folder of the repo |
| Supabase | Postgres with the vector extension for the document index, and a private bucket for the files |
| pdf-parse, mammoth, OpenAI embeddings | Read each upload (PDF or Word; PowerPoint cannot be read) and index it for the chat |
| Claude | The chat, inactive: its widget is hidden since August 2026, the route is still deployed. It answers only from the indexed documents |
| GitHub Actions + SSH | A merge to main runs a script on the server that builds and restarts |

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Codebase | Me | sarvalabs/moi-dataroom0, public. Merging to main deploys. I push branches to it |
| Supabase project and bucket | Me, to migrate to DevOps | Holds the documents (whitepaper, litepaper, decks, papers) and their index |
| Server, nginx, the SSH key, the deploy script | DevOps | The deploy script lives on the server, not in the repo |
| Domain dataroom.moi.technology | DevOps | |

A second, static data room (sarva-dataroom.vercel.app) exists on Vercel, with its code not in any repo. Push it to an org repo or take it down.

## Env vars

Where they live: production values are GitHub Actions secrets on sarvalabs/moi-dataroom0 (they cannot be read back; the readable copy is on the server, through DevOps). Locally, moi-data-room/.env.local, copied from the example file. A changed secret needs a manual run of the deploy workflow. Anything starting NEXT_PUBLIC_ is baked in at build, so it needs a rebuild.

| Variable | What it is | Where the value comes from |
|---|---|---|
| NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY | The database and bucket, from the browser | Supabase dashboard, the project, Settings, API |
| SUPABASE_SERVICE_ROLE_KEY | The same, server side only | Same page |
| ANTHROPIC_API_KEY | The chat (inactive) | console.anthropic.com, API keys |
| OPENAI_API_KEY | The document index. Missing, every upload ends failed and the chat answers without document text | platform.openai.com, API keys |
| ADMIN_SECRET | The admin page. Never leave it empty | Generate with: openssl rand -hex 32 |
| CLAUDE_PER_IP_HOURLY_LIMIT, CLAUDE_DAILY_TOKEN_BUDGET, CLAUDE_MAX_INPUT_TOKENS, CLAUDE_MAX_OUTPUT_TOKENS | Chat limits. Optional; defaults in the code (30, 500000, 8000, 2048), reset on every restart | Set by nothing today |
| VM_HOST, VM_USERNAME, VM_SSH_KEY | Deploy access | DevOps |
| ADMIN_TOKEN, DATAROOM_URL | Read by the code but set by no deploy: an old admin check (nothing reads it after the fix) and the whitepaper script's target, which defaults to the live site | Leave unset |

The example file with comments is moi-data-room/.env.local.example (not pushed yet, see Open items).

## Process

**Shipping a change**

- Work on a branch and push it to the repo.
- Run the type check, lint and the build myself. No pull request runs them.
- Open a pull request and merge it. No reviewer is on record.
- Merging to main deploys: GitHub Actions reaches the server over SSH and runs its script.
- Open the site afterwards, on a phone too. Nothing checks it for you.
- There is no rollback. Revert in a new pull request.

**The admin page**

- Sign in at the admin page with the admin secret, in a private window that you close afterwards. There is no user login anywhere else on the site; the admin page is the only gate.
- The page offers: Add Document; a row per document with Edit, the Download and Email gate toggles, Re-index and Delete; Captured Leads; Calendar events; Adopters Management (a form, or Import CSV); and summary figures (documents, indexed, views, chat questions, leads).
- The toggles and the Re-index button swallow errors, so re-read the state after every click.

**How the home page works**

- The home page has seven hero tiles, one per slot: foundation (the Math paper), paradigm (Contextual Compute), network (the Whitepaper), pitch-deck (the IM deck), two-pager (the CC intro), litepaper, and gtm-deck.
- A tile shows the document pinned to its slot. Pinning is the "Show on home" field in a document's form; one document per slot, and pinning a new one clears the old holder. A tile with nothing pinned falls back to a title match, which is why two documents with similar titles can swap places on the home page.
- Below the tiles, documents are listed by section: Contextual Compute, Engineering, Business & GTM, Tokenomics, Research, Use cases.
- The headline figures on the home page are typed into the code, not computed. Change them in the code, or source them, or drop them.

**Adding a document**

- Prepare a PDF or Word file under 50 MB. PowerPoint is accepted but cannot be read, so convert a deck to PDF first.
- Admin page, Add Document. Pick the category first (changing it later clears the title and description), then title, description, the file or an external link (an https address such as a Zenodo record), allow download, require email, and the home slot if it should be a tile.
- Upload. The browser sends the file straight to the storage bucket, then the row is created.
- Indexing starts on its own: the server extracts the text, cuts it into chunks, embeds them, and the status goes pending, processing, completed. Wait for completed; if it stays at processing or ends failed, press Re-index on its row, one document at a time, and read the status again.
- Check the home page afterwards, on a phone too, if the document has a tile.
- Uploads are limited to 10 a minute.

**Replacing the file inside a document**

- Editing a document does not re-index its file. Upload the new version as a new document with the same section, title and home slot (pinning moves the tile), wait for completed, then retire the old row.
- For the whitepaper and litepaper use the swap script in the repo, which replaces the paper everywhere it is referenced; check the tile and the download afterwards. The script renames the old tile document to "Litepaper" on every run, which was right once and is wrong now; fix or skip that step first.

**Deleting a document**

- Delete is one click on the row, with no confirmation, and it is permanent: the stored file, the row and its index all go.
- There is no unpublish button. Keep a copy of the file somewhere else before deleting, or rename the row instead of deleting it.
- After a delete, open the home page: a tile that pointed at the deleted document must not be left broken.

**Adopters, events and leads**

- Adopters: add one by form, or Import CSV. The header needs Name (or Project Name); optional Description, Link, Type (business or dapp). Each row is sent one at a time and the API allows 60 calls a minute, so split a long list. They show on the Adopters page.
- Calendar events: add, edit and delete in the admin page. The Events page itself has been hidden from the menu since August 2026.
- Captured Leads: the emails visitors leave to download a gated document. Personal data: read on screen, do not copy them anywhere, and settle who may see them.

**Changing a setting or a secret**

- Set it in GitHub, under the repo's Actions secrets and variables, then run the deploy workflow by hand.
- Values that start with NEXT_PUBLIC_ are baked in at build, so they need a rebuild, not a restart.

**Changing the database**

- Write the SQL file and run it by hand in the Supabase SQL editor before the code that needs it merges.

**Checking it is healthy**

- Open the home page and one document.
- In the admin page, every document should say completed.
- The chat is inactive, so there is nothing to ask it; check that uploads still index.

## Claude skill

The **moi-web-products-ops** skill covers the Dataroom with its dataroom runbooks: shipping, documents, the papers swap, admin, settings and database, health.

| When | What to tell Claude | What the skill does |
|---|---|---|
| Something looks wrong | "Is the Dataroom healthy?" | Runs a read-only health check on the live site, including which documents are indexed, and names the known faults. |
| Shipping | "Ship this Dataroom change." | Walks the branch, the local checks and the pull request, and says what merging will deploy. |
| A document | "Add this paper to the Dataroom." | Gives the upload steps and the check that it is indexed. The upload itself is mine. |
| The whitepaper | "Replace the whitepaper." | Walks the swap script and the checks after it. |
| A setting | "I need to change this Dataroom setting: ..." | Says where it is set and whether it needs a rebuild. It never sees the secret's value. |
| The database | "I need a table for ..." | Writes the SQL and says when to run it. I run it in Supabase. |

What the skill never does without my yes: push, merge (a merge deploys), run a workflow, run SQL against production, change a secret, or touch anything on the server. It does not touch admin until I have read the security note.

## Open items

- The admin check is unsafe. The fix is written, not merged. Merge it, redeploy, then treat the old admin password as leaked and change the admin secret.
- Decide whether the site, the repo and the chat stay open to anyone. Today there is no login, the repo is public, and three documents skip the email gate.
- Six documents are not indexed: one failed (likely no text in the file) and five are stuck at processing, the whitepaper among them. Re-index them one at a time.
- There are two whitepaper rows, one on the home tile and one indexed. Find which is current, keep one. The swap script renames the tile's document on every run; fix that first.
- The figures on the home page are typed into the code with no source. Source them or drop them.
- Push the README, the env template and the new AGENTS.md, and add a migration for the three tables and the column that were made by hand.
- Get the deploy script into the repo, and add a check after each deploy.
- Decide on the Events page, hidden since August, and on the second data room on Vercel.
- Migrate the Supabase project to DevOps.
