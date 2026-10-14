# Dataroom

**Status: active.** The site and its documents are live. Two parts are switched off: the chat (its widget has been hidden since August 2026, though the route is still deployed) and the Events page (hidden since August 2026).

Video: product demo https://drive.google.com/file/d/1FoOifehdhrH3hfrRJcbmim1WnRRBEXH5/view (recorded 13 October 2026).

Marketing: How it works, Variables, Open items. Developers: Stack, Env vars, Process, Claude skill, Open items.

dataroom.moi.technology is MOI's investor document room. It holds the whitepaper, the litepaper, the decks and the papers, and has a chat that answers questions from those documents. Anyone can open it; there is no login for visitors. Adithya built it and DevRel runs it. DevOps owns the server.

## How it works

**The admin page**

- The admin page is the only locked part of the site. Sign in with the admin secret (Chandrasekhar has it), in a private window, and close the window when you are done.
- From the admin page you can add a document and, for each document, edit it, switch downloads on or off, switch the **email gate** on or off (visitors must leave an email before they can download), re-index it or delete it. It also shows Captured Leads, Calendar events, Adopters (added by form or by CSV) and summary figures: documents, indexed, views, chat questions and leads.
- The toggles and the Re-index button do not show errors. After every click, look again to check it took.

**The home page, and how to change it**

- The top of the home page has seven large **tiles**, one for each **home slot** (a named place on the page): foundation (the Math paper), paradigm (Contextual Compute), network (the Whitepaper), pitch-deck (the IM deck), two-pager (the CC intro), litepaper and gtm-deck.
- The words on a tile come from the code, not from the document. Its title, tag and the italic line under it are in the HERO_CARDS list in moi-data-room/src/lib/constants.ts. To change them, edit that list, open a PR and merge it (merging deploys).
- Which document a tile opens is set by pinning. "Show on home" in a document's form pins it to a slot. Each slot holds one document, and pinning a new one unpins the old one. A tile with nothing pinned guesses by title (the matchCategory and matchTitleHint fields in the same list), so two documents with similar titles can swap places. Always pin.
- Under the tiles, documents are listed by section: Contextual Compute, Engineering, Business & GTM, Tokenomics, Research and Use cases. A document's section is its category.
- A document's title and description appear in that list and on its own page. To change them, click Edit on its row in the admin page, change what you need and Save. Editing never re-indexes the file. Changing the category wipes the title and description, so set the category first.
- The figures under "Network & Community" (Accounts, Interactions, Consensus Nodes, Community, KMOI TVL) are typed by hand into the STATS list in moi-data-room/src/lib/constants.ts. Nothing calculates them. Update them in the code, add a source, or remove them.
- The Adopters page shows whatever the admin Adopters section holds.

**How Supabase is used**

- There is one Supabase project. Since 8 October 2026 it sits in the company Supabase organisation, owned by sarvalabsdeveloper@gmail.com. That organisation is on the free plan, so there are no automatic backups.
- One Postgres database. Its tables: documents (one row per document, with its category, home slot, toggles and index status), document_embeddings (the indexed passages), analytics (views and downloads), chat_queries (questions asked), calendar_events, adopters, document_leads (emails left for gated documents) and profiles.
- One private storage bucket, investor-docs, holds the files. The browser uploads straight into it with the public anon key. Everything else goes through the server with the service-role key, which never reaches the browser.
- The schema is supabase/schema.sql plus the migration files next to it. Nothing runs migrations automatically: run a new file by hand in the Supabase SQL editor before merging the code that needs it.
- When something is wrong, the Supabase dashboard is where to look: Table editor for a document's row and status, Storage for the file, Logs for failed queries.

## Stack

| Piece | What it is |
|---|---|
| Next.js 16, React 19, TypeScript, Tailwind 4 | The site, the admin page and every API route, in the moi-data-room folder of the repo |
| Supabase | The database (with the vector extension that stores the document index) and the private bucket for the files |
| pdf-parse, mammoth, OpenAI embeddings | Read each upload (PDF or Word; PowerPoint cannot be read), cut the text into short passages called **chunks**, and turn each into **embeddings** (numbers that let the chat find the passages closest to a question) |
| Claude | The chat. Switched off: the widget is hidden, the route is still deployed. It answers only from the indexed documents |
| GitHub Actions and SSH | A merge to main runs a script on the server that builds and restarts the site |

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Codebase | DevRel | https://github.com/sarvalabs/moi-dataroom0, public. Merging to main deploys. Push branches straight to it. Adithya's fork, sarvalabs-adithya/MOI-dataroom, holds only the unmerged security branch |
| Supabase project and bucket | The company Supabase organisation, owned by sarvalabsdeveloper@gmail.com (moved there on 8 October 2026) | Holds the documents and their index |
| Admin secret | Chandrasekhar holds it | The only way into the admin page |
| Server, nginx, the SSH key, the deploy script | DevOps | The deploy script lives on the server, not in the repo |
| Domain dataroom.moi.technology | DevOps | |

## Env vars

The index across every product, with the consoles and who holds each login, is ENV-VARS.md.

Production values are GitHub Actions secrets on sarvalabs/moi-dataroom0. GitHub cannot show a secret back once set; the readable copy is on the server, through DevOps. Locally, values go in moi-data-room/.env.local, copied from moi-data-room/.env.local.example. After changing a secret, run the deploy workflow by hand. Anything starting with NEXT_PUBLIC_ is built into the site, so it needs a rebuild, not a restart.

| Variable | What it is | Where the value comes from |
|---|---|---|
| NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY | The database and bucket, used from the browser. The **anon key** is Supabase's public key and is safe in the browser | Supabase dashboard, the project, Settings, API |
| SUPABASE_SERVICE_ROLE_KEY | The same, from the server only. The **service-role key** is Supabase's all-access key and must never reach the browser | Same page |
| ANTHROPIC_API_KEY | The chat (switched off). Not a company key, and no company Anthropic account exists yet: create one before switching the chat back on | console.anthropic.com, API keys |
| OPENAI_API_KEY | Builds the document index. Without it every upload fails to index. Not a company key either | platform.openai.com, API keys |
| ADMIN_SECRET | The admin page. Never leave it empty | `openssl rand -hex 32`; Chandrasekhar holds the current value |
| CLAUDE_PER_IP_HOURLY_LIMIT, CLAUDE_DAILY_TOKEN_BUDGET, CLAUDE_MAX_INPUT_TOKENS, CLAUDE_MAX_OUTPUT_TOKENS | Chat limits. Optional; the code defaults are 30, 500000, 8000 and 2048 | Not set |
| VM_HOST, VM_USERNAME, VM_SSH_KEY | Deploy access | DevOps |
| ADMIN_TOKEN, DATAROOM_URL | Read by the code, set by nothing. ADMIN_TOKEN is a second admin check on the stats route; while it is unset, that route answers anyone (see Open items). DATAROOM_URL is where the whitepaper script points, and defaults to the live site | Set ADMIN_TOKEN once the security fix is merged. Leave DATAROOM_URL unset |

## Process

**Shipping a change**

- Work on a branch and push it to the repo.
- Run the type check, lint and build yourself. Nothing runs them on a pull request.
- Open a pull request and merge it. No reviewer is set.
- Merging to main deploys: GitHub Actions logs in to the server over SSH and runs its deploy script.
- Open the site afterwards, on a phone too. Nothing checks it for you.
- There is no rollback button. To undo, revert in a new pull request.

**Changing a setting or a secret**

- Change it in GitHub, under the repo's Actions secrets and variables, then run the deploy workflow by hand. Changing a value deploys nothing by itself.
- A NEXT_PUBLIC_ value needs a rebuild, which the deploy does.
- To rotate the admin secret: `openssl rand -hex 32 | gh secret set ADMIN_SECRET -R sarvalabs/moi-dataroom0`, then `gh workflow run "Deploy MOI Dataroom" -R sarvalabs/moi-dataroom0 --ref main`. Give the new value to Chandrasekhar, because GitHub cannot show it again. Every admin has to sign in again afterwards. It was last rotated on 9 October 2026.

**Changing the database**

- Write the SQL file and run it by hand in the Supabase SQL editor, before the code that needs it is merged.

**Checking it is healthy**

- Open the home page and one document.
- Check that a wrong admin key is refused: `curl -s -X POST https://dataroom.moi.technology/api/admin/unlock -H 'content-type: application/json' -d '{"key":"x"}'` should answer 403 with "Invalid key".
- If the chatbot is enabled: every document should say completed in the admin page, and a new upload should get indexed. While the chat is off, indexing does not matter.

**Adding a document**

- Use a PDF or Word file under 50 MB. PowerPoint uploads but cannot be read, so convert decks to PDF first.
- In the admin page, click Add Document. Choose the category first (changing it later wipes the title and description), then fill in the title, the description, the file or an https link (such as a Zenodo record), whether it can be downloaded, whether it needs an email, and a home slot if it should be a tile.
- Upload. The file goes straight to the storage bucket, then the row is created.
- Indexing only matters if the chatbot is enabled (it is off today); the document is live for visitors either way. Indexing starts by itself and the status moves from pending to processing to completed. If the chatbot is on, wait for completed. If it stays on processing or ends in failed, press Re-index on that row, one document at a time, and check the status again.
- If the document has a tile, check the home page afterwards, on a phone too.
- You can upload at most 10 files a minute.

**Replacing the file inside a document**

- Editing a document does not re-index its file. Upload the new version as a new document with the same section, title and home slot (pinning moves the tile over), wait for completed, then delete the old row.
- For the whitepaper and litepaper, use the swap script in the repo. It replaces the paper everywhere it is linked; check the tile and the download afterwards. Each run also renames the old tile document to "Litepaper", which was right once and is wrong now, so fix or skip that step first.

**Deleting a document**

- Delete is one click, with no confirmation, and it is permanent: the file, the row and its index all go.
- There is no unpublish. Keep a copy of the file elsewhere before deleting, or rename the row instead.
- After a delete, open the home page and make sure no tile points at the deleted document.

**Adopters, events and leads**

- Adopters: add one with the form, or use Import CSV. The CSV needs a Name (or Project Name) column; Description, Link and Type (business or dapp) are optional. Rows are sent one at a time and the API allows 60 a minute, so split long lists. Adopters show on the Adopters page.
- Calendar events: add, edit and delete them in the admin page. The Events page itself is hidden from the menu (since August 2026).
- Captured Leads: emails that visitors leave to download a gated document. These are personal data: read them on screen, do not copy them anywhere, and agree who may see them.

**Switching the chat back on**

The chat was hidden on 21 August 2026 by the commit "chore: hide chat assistant widget for now" (a5544a8), which took the widget off the page. The widget and the chat route are still deployed. To bring it back:

1. Get company keys. Create a company Anthropic account with billing, make a key, replace ANTHROPIC_API_KEY in the repo's Actions secrets and check in the console that the key works. Do the same for OPENAI_API_KEY, which indexes the documents and the questions.
2. Make sure every document says completed. In October 2026 six did not: one failed (probably no text in the file) and five were stuck at processing, the whitepaper among them. Re-index them one at a time and check the status after each click. The chat only answers from indexed documents, so without the whitepaper it cannot answer basic questions.
3. Update the model. The chat route (moi-data-room/src/app/api/chat/route.ts) uses claude-sonnet-4-20250514, which is old. Change it to a current model and try one question locally.
4. Put the widget back: revert commit a5544a8 on a branch.
5. If the default limits do not suit (30 questions per address per hour, 500,000 tokens a day, 8,000 input and 2,048 output tokens), set the four CLAUDE_ values as Actions variables and add a line for each to deploy.yml, which passes none of them today.
6. Open the PR and merge it (merging deploys).
7. Test on the live site with one question the whitepaper answers and one it cannot. The first should cite documents and the second should be politely refused. Watch the "Chatbot Questions" figure in the admin page and the usage in the Anthropic console the next day.
8. Update the Status line of this doc.

**Switching the Events page back on**

The Events page is off for now (decided 9 October 2026). The commit "chore: hide Events from sidebar nav for now" (5952d9a) hid it on 22 August by removing one line from the NAV_ITEMS list in moi-data-room/src/lib/constants.ts. Everything else still works: /events answers, and its API routes, the admin Calendar events section and the calendar_events table are all there. To bring it back:

1. Get the event dates from Vardan and add them in the admin page under Calendar events, so the page is not empty on day one.
2. Put the menu line back: revert commit 5952d9a, or add `{ id: "events", label: "Events", icon: "▦", href: "/events" }` after the Home entry in NAV_ITEMS.
3. Open a PR and merge it (merging deploys).
4. Check /events and the menu on a phone.
5. Update the Status line of this doc.

## Claude skill

The **moi-web-products-ops** skill covers the Dataroom: shipping, documents, swapping the papers, admin, settings, the database and health.

| When | What to tell Claude | What the skill does |
|---|---|---|
| Something looks wrong | "Is the Dataroom healthy?" | Runs a read-only check on the live site, including which documents are indexed, and names the known faults. |
| Shipping | "Ship this Dataroom change." | Walks through the branch, the local checks and the pull request, and says what merging will deploy. |
| A document | "Add this paper to the Dataroom." | Gives the upload steps and how to check it is indexed. You do the upload. |
| The whitepaper | "Replace the whitepaper." | Walks through the swap script and the checks after it. |
| A setting | "I need to change this Dataroom setting: ..." | Says where it is set and whether it needs a rebuild. It never sees the secret itself. |
| The database | "I need a table for ..." | Writes the SQL and says when to run it. You run it in Supabase. |

Without your yes, the skill never pushes, merges (merging deploys), runs a workflow, runs SQL on production, changes a secret or touches the server. It does not touch the admin page until you have read the security note (the first Open item).

## Open items

- The admin check is weak. The admin cookie carries the secret itself and page scripts can read it, the secret is not compared safely, and the stats route on main accepts a fixed cookie value written in the public source. While ADMIN_TOKEN is unset, that route shows anyone the question count and the top documents. A fix (safe comparison, an httpOnly cookie, and no admin at all if the secret is empty) is on the branch claude/security-vulnerability-analysis-dWvYu of Adithya's fork, from 23 March and 62 files behind main. Copy the branch to sarvalabs/moi-dataroom0, rebase it, keep the login changes, open a PR and merge it, then rotate ADMIN_SECRET once more.
- There are two whitepaper rows, one on the home tile and one indexed. Work out which is current and keep one. Fix the swap script's rename step first.
- The home page figures are typed into the code with no source. Add sources or remove them.
- PR #7 (merged 13 October 2026) added a migration for the adopters and document_leads tables and the require_email column. Run it once in the SQL editor if nobody has; on production it changes nothing.
- The deploy runs /root/scripts/deploy-moi-dataroom.sh, which exists only on the server, so nobody can review what a deploy does. Copy it into the repo and have the workflow run that copy. Then add a step that opens the site and checks a wrong admin key is refused, so a broken deploy shows red instead of green.
- Nobody has recorded which account owns the Anthropic and OpenAI keys now in the repo's secrets. Find out, then replace both with company keys.
