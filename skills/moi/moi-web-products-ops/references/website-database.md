# Website: the Supabase tables behind the calendar and the chat

Updated 13 October 2026: since website PR #60 the homepage no longer reads `community_calls`; only the Express server's `/api/community-calls` routes do. Facts are as of 2026-10-03 from `supabase-setup.sql`, `supabase-community-calls.sql` and `server/index.js` on `sarvalabs/MOI-Website` `main` (`5e91afa`), the public text of GitHub issue 3 (open since 2026-04-20), and the research note dated 2026-10-02. Back to `../SKILL.md`.

## What the server stores

| Table or function | Used by | Defined in |
|---|---|---|
| `community_calls` (id, title, description, date, duration_minutes, timezone, meeting_link, meeting_link_label, category with a CHECK of four values, max_attendees, created_at, updated_at) and an index on `date` | The old calendar routes of the server (`website-calendar.md`); the homepage does not read it any more | `supabase-community-calls.sql`. Its last statement inserts seven placeholder events: never run it |
| `documents` (id bigserial, content, metadata, embedding vector(1536)), the function `match_documents(query_embedding, match_threshold, match_count)`, and an `ivfflat` index with 100 lists | The chat (`website-chatbot.md`) | `supabase-setup.sql` |

There is no migrations folder. Nothing applies SQL for you: the two files are run by hand in the Supabase SQL editor, and they are the only description of the schema. The Dataroom keeps the same pattern (`dataroom-settings-and-database.md`).

## Find the right project
Which Supabase project `SUPABASE_URL` points at is not known. Issue 3's text says the project holds a function named `match_document_embeddings` without `match_threshold`, which is the Dataroom's. So the website may share a Dataroom-shaped project (inferred). In such a project the Dataroom's own `documents` table already exists with other columns. Then:
- `create table if not exists documents` in `supabase-setup.sql` does nothing, and the ingest script fails or writes into the wrong shape.
- `npm run ingest:clear` runs `delete ... neq("id", 0)` against a table whose `id` is a uuid in the Dataroom. It should error. Do not test it.
- An older local note told operators to run both SQL files and then ingest. That is not safe as written; `project-handover-docs/MOI-WEBSITE.md` and `ENV-VARS.md` say the website's project is probably the Dataroom's and is not recorded.

## Run: find out why the calendar API answers 500, and fix it

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Confirm the fault | `curl -s https://moi.technology/api/community-calls` | `{"error":"Internal server error"}` (still so on 2026-10-03) |
| 2 | GATE | Ask DevOps for the reason | The handler logs `Fetch calls error:` plus the Supabase message. Use `templates/devops-request.md`, request R3 in `who-to-ask.md`. The operator sends it to Srikar, who owns the website server | A log line, such as a missing table or a failed key |
| 3 | CHECK | Find the project | The Supabase owner opens the project behind `SUPABASE_URL` and lists its tables and functions. Owner unknown. ASK: Rahul. Claude does not sign in to Supabase | A list of tables and functions |
| 4 | CHECK | Choose the case | A: the project has no `community_calls`. B: it has the table and the error is something else (a key, a permission). C: it is Dataroom-shaped | One letter |
| 5 | GATE | Case A: create the table only | In the SQL editor, run the `create table if not exists community_calls (...)` and `create index ...` statements of `supabase-community-calls.sql`, and nothing after them. This writes to the production database | The statements ran |
| 6 | GATE | Case C: do not run `supabase-setup.sql` there | Either a separate Supabase project for the website (a decision and a cost, ASK: Rahul), or change `server/index.js` to call the Dataroom's function, which is Issue 3's alternative and was never merged. Either needs `website-ship.md` and a new `SUPABASE_URL` and `SUPABASE_KEY` (`website-settings.md`) | A written decision |
| 7 | VERIFY | Read the JSON | `curl -s https://moi.technology/api/community-calls` | A JSON list. `[]` passes. Then continue with the baked API base in `website-settings.md` (the homepage no longer needs this table; `website-calendar.md`) |

## Run: change the schema later

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Read the live shape | The Supabase owner lists the table's columns in the dashboard. Claude does not sign in | The live columns are known |
| 2 | LOCAL | Edit the `.sql` file in the repo | Use `if not exists` forms and a comment saying when to run it | The file is the full description |
| 3 | GATE | Run the changed statements by hand, before the code | The Supabase owner, in the SQL editor. This writes to the production database | The statements ran |
| 4 | GATE | Ship the file and the code | `website-ship.md` | Merged |
| 5 | VERIFY | Read the JSON or ask a chat question | As above | The feature works |

## Traps
- Never run the final INSERT of `supabase-community-calls.sql`. It puts placeholder events on the homepage.
- Never run `supabase-setup.sql` before you know the project.
- Free Supabase plans have no downloadable backups. The plan of this project is unknown.
- The server caches the calendar list for 5 minutes and empties the cache on any write through the API. A change made in the SQL editor shows up within 5 minutes.

## Not yet known
- Which project and which plan. Who can open it. ASK: Rahul.
- Whether the project is shared with anything else. ASK: Rahul.
