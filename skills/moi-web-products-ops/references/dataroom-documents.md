# Dataroom: add, replace, unpublish and re-index a document

Facts are as of 2026-10-03 from `sarvalabs/moi-dataroom0` `main` (`0f8e38b`: `admin/page.tsx`, `upload-modal.tsx`, `lib/embeddings.ts`, `lib/constants.ts`, `app/api/documents/*`, `app/api/chat/route.ts`) and the public document list read that day (titles, categories, slots and statuses only). Back to `../GUIDE.md`.

Dataroom: A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin.

A step marked ADMIN needs the operator to confirm first that the handover note was read. The operator signs in, in a private window that is closed afterwards; Claude never sees a credential.

## What a document is
- Fields in the upload form: category (the section), title, description, a file or an external link (an https address such as a Zenodo record), allow download, require email, and "Show on home" (a hero slot).
- Sections: `contextual_compute`, `engineering`, `business` (shown as "Business & GTM"), `tokenomics`, `research`, `usecases`.
- Hero slots on `/home`: `foundation` (Math paper), `paradigm` (Contextual Compute), `network` (Whitepaper), `pitch-deck` (IM deck), `two-pager` (CC Intro), `litepaper`, `gtm-deck`. One document per slot: assigning a slot clears the previous holder. A tile with no pinned document falls back to a case-insensitive title match among the unpinned documents of the tile's category (or those flagged for the overview), so titles matter: "Math", "Contextual", "Network" (also "White Paper", "Whitepaper", "Foundations"), "Slide", "2 Pager", "Litepaper" (also "Lite Paper"), "GTM" (also "go-to-market").
- How the chat learns it: the file goes to the private storage bucket `investor-docs`, the server extracts text (PDF and DOCX only), cuts it into 2000-character chunks with 200 overlap, embeds them with OpenAI `text-embedding-3-small` and stores them. The document's `embedding_status` goes `pending`, `processing`, then `completed` or `failed`. The search function does not look at the status, so a document that is not `completed` may have no chunks or only some, and the chat may miss it. Do not rely on a document being quoted until it is `completed`.

## State on 2026-10-03
23 published documents, 17 completed, 5 `processing` and 1 `failed` (D-K1). `GTM Deck` failed: its `embedding_error` reads "No text could be extracted from the document" (read 2026-10-03), so its file probably has no text layer (inferred). Stuck in `processing`: `Whitepaper` (pinned to `network`), `IM Deck`, `Tokenomics  Overview`, `Parallelism in shared spaces`, `Truth of Happiness - The vision paper`. Why is unknown. The embedding runs as a background task inside the web server, so a restart or deploy during it can leave the status at `processing` for good (inferred). Three title rows concern the papers: `Whitepaper` (pinned to `network`, stuck), `White Paper` (unpinned, completed) and `Litepaper` (pinned to `litepaper`, completed). Which of the two whitepaper rows is the current v2.1 file is unknown. ASK: Adithya.

## Run: add a document

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Baseline | `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" dataroom` | The KNOWN D-K1 lines are the six above and nothing is new |
| 2 | CHECK | Prepare the file | A PDF or DOCX under 50 MB. Convert a deck to PDF: a PPTX is accepted, but it is read with mammoth, and the code's own warning in `lib/embeddings.ts` says mammoth does not support PPTX. By the code, such an upload ends with the error "No text could be extracted from the document", the same message `GTM Deck` carries. Choose the section, a title that matches the tile you want, a description | The file opens and its text selects |
| 3 | GATE | ADMIN: upload | Open the admin page, Add Document, fill the fields (pick the Category first: changing it clears the title and description), Upload. The browser sends the file straight to the bucket, then creates the row | The document is in its section |
| 4 | VERIFY | Watch the status | `curl -s https://dataroom.moi.technology/api/documents` and read `embedding_status` for your title, or `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" dataroom` (a new title shows as NEW until it completes). `set-whitepaper.mjs` waits up to 5 minutes; a normal time is not recorded | `completed`. Anything else means the chat may miss it |
| 5 | GATE | ADMIN: Re-index if it is not completed | The Re-index button on its row in the admin page. The button swallows errors, so read the status again after | `completed` |
| 6 | GATE | Spend and a database write: ask the chat one question that only the new file answers | The chat widget is hidden in the UI (commit `a5544a8`), the route is live: `curl -N -X POST https://dataroom.moi.technology/api/chat -H 'content-type: application/json' -d '{"messages":[{"role":"user","content":"<question>"}]}'`. A few tokens of Anthropic and OpenAI, and the app logs the question in `chat_queries` (the admin page counts it under Chatbot Questions). The route answers even when search fails, with "(No relevant excerpts found...)" as its context, so read the answer for content from the new file | The answer uses the file |
| 7 | VERIFY | Read `/home` | Open it on desktop and on a phone. A tile that should show the document must | The tile shows it |

## Run: replace the file inside a document
Editing a document's file does not re-embed it. For the whitepaper and litepaper use `dataroom-papers.md`.

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Read the row | `curl -s https://dataroom.moi.technology/api/documents`: its title, section, slot and status | You know what the new file replaces |
| 2 | GATE | ADMIN: upload the new file as a new document | As "add a document" above, with the same section and title, and the same Home slot (assigning it clears the old holder) | The new row is `completed` |
| 3 | GATE | ADMIN: retire the old row | Delete is permanent (below). Rename it instead if the operator wants to keep it | The operator named the row |
| 4 | VERIFY | Read `/home` and ask a question | "Add a document" steps 6 and 7 | The tile and the chat use the new file |

## Run: unpublish without losing it
The admin page has Delete and no Unpublish button (read 2026-10-03). Delete is one click with no confirmation and is permanent: it removes the stored file and the row, and the embeddings go with it. The document API can set a document's status to `draft` (`restricted` also exists in the code); how the previous operator did it is not recorded. ASK: Adithya. A draft is hidden from the lists, but the search function joins the chunks to the document with no status test (`migration-add-embedding-status.sql`; the repo SQL may differ from production), so the chat may still quote a draft. Only Delete removes the chunks. If a document must stop being quoted, say so to the operator before choosing.

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Is the file kept elsewhere? | The operator confirms a copy of the file exists outside the Dataroom | A copy exists |
| 2 | GATE | ADMIN: Delete, only on the operator's explicit yes naming the document | The Delete button on its row | The row is gone |
| 3 | VERIFY | Read the list and `/home` | `curl -s https://dataroom.moi.technology/api/documents`; open `/home` | The title is absent and no tile shows a broken link |

## Run: fix a stuck or failed embedding

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Which and why | `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" dataroom`; for `failed`, the document's `embedding_error` field in the same JSON (`curl -s https://dataroom.moi.technology/api/documents`) names the reason | Reason read. A PPTX means convert it |
| 2 | GATE | ADMIN: Re-index each | The Re-index button, one document at a time | Status `completed` |
| 3 | VERIFY | Ask a question | Step 6 above for that document | The answer cites it |

A bulk re-index of every non-completed document exists in the API and runs them one after another inside one request, so a proxy may time out while the server keeps going (inferred). Prefer one at a time.

## Traps
- A failed insert of one batch of chunks is only logged. If one batch worked, the document is marked `completed` with chunks missing. Always ask a question that only the file answers.
- The chat ignores errors from the search step and still replies. A wrong OpenAI key or a missing function makes it look alive and know nothing.
- A restart or deploy during embedding leaves `processing` forever (inferred). Do not deploy while a big upload embeds.
- Titles drive the home tiles. Two whitepaper rows plus "Litepaper" exist. Check what `/home` shows after any change.
- `seed.sql` is `delete from public.documents;`. Never run it.
- Uploads are limited to 10 a minute per IP and admin calls to 30 a minute.

## Not yet known
- Why six documents are stuck. ASK: Upendhar (server log) and Adithya.
- Whether `restricted` is used. ASK: Adithya.
