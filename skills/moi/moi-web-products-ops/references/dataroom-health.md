# Dataroom health: is it up, can the chat cite the documents, what is already broken

Updated 13 October 2026 for PR #7 and the company Supabase move. Facts are as of 2026-10-03 (GET reads taken that day) unless a line carries another date. Sources: `sarvalabs/moi-dataroom0` `main` at commit `0f8e38b`, the research note dated 2026-10-02. Back to `../SKILL.md`.

Dataroom: A security finding is open on this product as of 2026-10-02. The handover note is the Open items of `project-handover-docs/DATAROOM.md`; read it before touching its admin.

## "The Dataroom is down or wrong"

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Read the state | `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" dataroom`. A single FAIL is not an outage: run it once more | You know which lines FAIL. KNOWN lines are old news |
| 2 | CHECK | Narrow it | `/` and `/home` FAIL: the web server or the VM, so DevOps. `/home` passes but a page errors: ask DevOps for the container or process log (request R10 in `who-to-ask.md`). Documents list fine but the chat is wrong: step 3 | One sentence naming the layer |
| 3 | CHECK | Is the chat real? | Judge the chat by asking a question, never by a status code: `dataroom-documents.md` step 6 (spends a few tokens, GATE). An answer with no content from the documents means search is failing silently | You know whether answers use documents |
| 4 | CHECK | Was it a deploy? | `gh run list -R sarvalabs/moi-dataroom0 --workflow "Deploy MOI Dataroom" --limit 3` | Known |
| 5 | LOCAL | Record it | `templates/incident-note.md` | Note exists |
| 6 | GATE | Ask DevOps | `templates/devops-request.md`; the operator sends it to the DevOps owner of the Dataroom server (`who-to-ask.md`). Never ask for a secret | Sent |
| 7 | VERIFY | Confirm recovery | Step 1 again, and one chat question | Nothing new FAILS |

There is no `/health` route on the Dataroom and nothing checks it after a deploy. A restart resets the chat limits and can leave an embedding at `processing`.

## What each check proves

| Check | Healthy | Reads |
|---|---|---|
| `GET /` | 307 to `/home` | The Next.js app answers |
| `GET /home` | 200 | The dashboard renders |
| `GET /api/documents` | 200 and a JSON list of published documents | The database and the list. The script prints titles and statuses only, never file addresses |
| `embedding_status` of each document | `completed` | Whether the document is fully in the search index. With `pending`, `processing` or `failed` it may have no chunks or only some, so the chat may miss it |
| Hard-coded figures on `/home` | none | See D-K2 |

## Known faults (the script prints these as KNOWN)

| ID | Fault | Fix path |
|---|---|---|
| D-K1 | Six of 23 documents are not fully embedded (2026-10-03): `GTM Deck` is `failed` with the error "No text could be extracted from the document" (probably a file with no text layer, inferred); `Whitepaper`, `IM Deck`, `Tokenomics  Overview`, `Parallelism in shared spaces` and `Truth of Happiness - The vision paper` are stuck in `processing`. The `Whitepaper` row is the one pinned to the `network` tile. Cause of the five stuck ones unknown | `dataroom-documents.md`, "fix a stuck or failed embedding". Any other title that is not `completed` shows as a WARN named NEW |
| D-K2 | `/home` shows five hard-coded figures from `src/lib/constants.ts` (`STATS`): accounts 4.3K, interactions 14.4K, consensus nodes 100, community 50K+, KMOI TVL $79.0M, each with a change label. Nothing updates them and no source is recorded for them. The page is for investors | Check each against a source with `moi-devrel/claim-check`, then edit `constants.ts` through `dataroom-ship.md`, or remove the block. ASK: Rahul which figures may stand |
| (none) | The chat widget inside the Dataroom is hidden (commit `a5544a8`, 21 August 2026, "hide chat assistant widget for now"); the chat route is live | Nothing to fix; know it when someone says "the chat is gone" |
| (none) | The route ignores a `system_override` field in the request body. The website's old proxy sends one, and only the `[CONTEXT: ...]` prefix on the last user message reaches the model | Matters only if the website chat is pointed at this route (`website-chatbot.md`) |
| (none) | `adopters`, `document_leads` and `documents.require_email` were made by hand. PR #7 (merged 13 October 2026) added `moi-data-room/supabase/migration-add-adopters-leads-require-email.sql` for them; run it once in the SQL editor if it has not been run (on production it changes nothing) | `dataroom-settings-and-database.md` |
| (none) | The committed `AGENTS.md` is leftover boilerplate for the old host. PR #7 added a root `README.md` and `moi-data-room/.env.local.example` | Do not rely on `AGENTS.md` |

## By hand, because the script cannot

| Check | How |
|---|---|
| Chat validation, spends nothing | `curl -s -X POST https://dataroom.moi.technology/api/chat -H 'content-type: application/json' -d '{"messages":[]}'` should answer 400 `messages array is required` by the code (`app/api/chat/route.ts`); no one has recorded running it, and it is a GATE because it is a POST |
| A deploy run | `gh run list -R sarvalabs/moi-dataroom0 --workflow "Deploy MOI Dataroom" --limit 3`. Green proves only that the SSH script returned |
| A phone | Open `/home` on a phone. On 2026-08-22 it did not load there; cause unknown |

## Not yet known
- Why six documents are stuck. ASK: DevOps for the server log.
- How long a deploy takes and what restarts. ASK: DevOps.
- Where the five figures came from: not recorded (Open items of `project-handover-docs/DATAROOM.md`). ASK: Rahul.
- Who is told when the Dataroom is down. ASK: Rahul.
