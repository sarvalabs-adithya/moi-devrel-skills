# Website: the chatbot, what it knows, and turning it back on

Facts are as of 2026-10-03 from `sarvalabs/MOI-Website` `main` (`5e91afa`: `server/index.js`, `scripts/ingest.js`, `src/pages/HomePage.jsx`), and the public text of GitHub issue 3. Back to `../GUIDE.md`.

## State
- The chat is hidden. The homepage "Ask the protocol" section sits inside `{false && (` in `src/pages/HomePage.jsx` since commit `6450d21` (2026-06-08, "home: temporarily hide 'Ask the protocol' chat section"), and the widget file `src/components/MOIChatbot.jsx` is imported by no file. Ingesting documents changes nothing a visitor can see.
- The server route should be live. A POST to `/api/chat` with `{}` is answered 400 `{"error":"message is required"}` by the code, before any model call; no one has recorded running it, and it is a GATE (a POST to production). Even if it answers, that proves the route and not that answers work.
- Whether answers work is unknown. GitHub issue 3 (opened 2026-04-20, still open) says every chat request failed with "Could not find the function public.match_documents(...)", because the Supabase project holds `match_document_embeddings`, which has no `match_threshold`. That is the Dataroom's function name and shape (`dataroom-settings-and-database.md`), so the website's `SUPABASE_URL` probably points at a Dataroom-shaped project (inferred). The alternative fix in the issue (call the other function) was never merged.
- How an answer is made: the server embeds the question with OpenAI `text-embedding-3-small`, calls the Supabase function `match_documents` (threshold 0.3, 6 chunks), and streams `claude-sonnet-4-20250514` (max 2048 tokens) as server-sent events: `text`, then `sources`, then `done`. A search error returns 500, so unlike the Dataroom this chat does not hide a broken store.
- The system prompt tells the model to answer only from the supplied context and to keep answers short. Wording that MOI insists on (participant-centric, network ID) is in `moi-devrel/references/terminology.md`; check the prompt against it before turning the chat on.
- The Vercel-era proxy to the Dataroom's chat (`api/chat.js`, `lib/websiteChat.js`, the variable `DATA_ROOM_CHAT_URL`) is not on the VM path as far as the code shows. `DEPENDENCIES.md` (the previous operator's file, local; ASK: Adithya for a copy) says the site's chat calls the Dataroom; the code says otherwise, and the code wins. ASK: Upendhar what nginx forwards. <!-- slop-lint: ignore -->
- The limiter allows 20 chat requests a minute per IP. The app does not set `trust proxy`, so behind nginx every visitor may share one address (inferred).

## Run: put new knowledge in the store (ingest)
Do not start until `website-database.md` has told you which Supabase project `SUPABASE_URL` points at.

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Right project and function | `website-database.md`, "Find the right project" | The project has `documents` and `match_documents` as `supabase-setup.sql` defines them |
| 2 | LOCAL | Put the source in `docs/` of a clone made as in `website-ship.md` steps 2 and 3 (with `npm ci`) | `.pdf`, `.md` or `.txt`. Use the same file the Papers page serves (`website-content.md`: the `docs/` litepaper differs from the served one) | The file is in `docs/` |
| 3 | LOCAL | The operator supplies the three names, in their own terminal, from the clone root | `OPENAI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`, typed at a hidden prompt into the shell session (zsh: `read -rs "OPENAI_API_KEY?OPENAI_API_KEY: "; echo; export OPENAI_API_KEY`, and the same for the other two), or in a local `.env` deleted afterwards. The script reads `process.env` first. This is the one job that puts production values on a laptop, and GitHub cannot be read back, so where the values come from is not recorded. ASK: Rahul. Claude never opens or prints them | The operator confirms the names are set |
| 4 | GATE | Write to the production store and spend OpenAI tokens | From the clone root: `npm run ingest` adds chunks. `npm run ingest:clear` deletes every row in `documents` first (`delete ... neq("id", 0)`) and only then looks for files, so with an empty or missing `docs/` it empties the store and then exits with an error. Re-running `ingest` duplicates every chunk, so use `ingest:clear` to replace. Say the file count first. A `.md` file is cut by headings and paragraphs into chunks of about 2000 characters with 200 overlap; a PDF or header-less text is cut by words, 400 words per chunk with 40 overlap. Chunks under 50 characters are dropped. Embedded in batches of 20 | Output ends with a stored count |
| 5 | GATE | Ask one real question (spends a few tokens) | `curl -N -X POST https://moi.technology/api/chat -H 'content-type: application/json' -d '{"message":"<a question only the new file answers>"}'` | The stream has `text` that uses the new content, then `sources` naming the file |

## Run: turn the chat back on
Do the steps in order. The fault list is in `website-health.md`.

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Decide the backend and the model | Own store with Sonnet 4 as now, or the Dataroom's chat. On 2026-06-19 the previous operator asked what monthly budget the chat needs "for embedding and haiku"; the outcome is unknown. ASK: Rahul | A written decision |
| 2 | CHECK | The store answers | Step 5 above succeeds against production | Sources come back |
| 3 | GATE | The browser reaches the API | `website-settings.md`, "Fix the baked API base" (W-K2) | The bundle no longer holds the dev host |
| 4 | LOCAL | Remove the switch | In `src/pages/HomePage.jsx` take the `{false && (` wrapper off the `s-ask` section (around line 771), keep the section | `npm run lint` and `npm run build` pass |
| 5 | GATE | Ship | `website-ship.md` | Merged and deployed |
| 6 | VERIFY | Use it as a visitor | Ask two questions on the live page, one broad ("What is MOI?") and one only a new document answers. Read the sources | Answers use the documents. A 500 or an answer with no sources means stop |

## Traps
- Ingesting before the chat is shown helps nobody, and ingesting into the wrong project can damage the Dataroom's data (`website-database.md`).
- `docs/MOILitePaper.pdf` (175,872 bytes) is not the file the site serves (259,385 bytes, identical to `public/papers/moi-lite-paper.pdf`). An ingest from `docs/` would load the older file (what the store holds today is unknown).
- The system prompt says "whitepaper, docs, blog posts" but `docs/` holds one PDF. Posts and the whitepaper are not among the files `docs/` holds, so an ingest cannot put them in the store.
- The three names above are the whole list the script reads. Never print or commit their values.

## Not yet known
- Which Supabase project the store is in, and whether the chat answers today. ASK: Upendhar (server log), Rahul (project owner).
- Whether the chat should return at all, and on which model. ASK: Rahul.
- What nginx forwards for `/api` and for `dev.moi.technology`. ASK: Upendhar.
