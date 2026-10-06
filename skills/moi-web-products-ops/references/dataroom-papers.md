# Replace the whitepaper or litepaper everywhere

Facts are as of 2026-10-03 from `sarvalabs/moi-dataroom0` `main` (`0f8e38b`: `moi-data-room/scripts/set-whitepaper.mjs`), `sarvalabs/MOI-Website` `main` (`5e91afa`), the public Dataroom document list and HEAD reads. Back to `../GUIDE.md`.

Dataroom: A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin.

A paper lives in up to four places, and they drift. A new version must reach every one, or investors and visitors read different versions. A step marked ADMIN needs the operator to confirm first that the handover note was read.

## The places

| # | Place | What holds it | Replaced by |
|---|---|---|---|
| 1 | Dataroom | A document row, a stored file and its embeddings. The whitepaper tile on `/home` is the `network` slot; the litepaper tile is the `litepaper` slot | `set-whitepaper.mjs`, or the admin page (`dataroom-documents.md`) |
| 2 | Website Papers page | `public/papers/moi-white-paper.pdf`, `public/papers/moi-lite-paper.pdf`, the blurbs in `src/pages/PapersPage.jsx`, and a second path `public/MOILitePaper.pdf` | A pull request (`website-content.md`) |
| 3 | Website chat store | `docs/MOILitePaper.pdf` in the repo, ingested into the Supabase `documents` table | `npm run ingest:clear` (`website-chatbot.md`). Pointless while the chat is hidden |
| 4 | External records | Zenodo and DOI records behind the tech, math and PIC entries of the Papers page | Out of scope here. ASK: Rahul who owns the Zenodo records |

Anything else that links a paper (docs sites, blog posts, Drive, decks) is not catalogued. Search the repos you hold: `git grep -n "moi-white-paper\|moi-lite-paper\|MOILitePaper" -- .`. ASK: Adithya whether other places exist.

## Known state on 2026-10-03
- The website whitepaper is 2,245,957 bytes on `main` and on the live site, last modified 2026-09-23 per the server header.
- The two website litepaper paths are the same file (259,385 bytes). `docs/MOILitePaper.pdf` is a different file (175,872 bytes).
- The Dataroom has a `Whitepaper` row pinned to `network` (embedding stuck in `processing`), an unpinned `White Paper` row (completed) and a `Litepaper` row pinned to `litepaper` (completed). Which of the two whitepaper rows holds the current file is unknown. ASK: Adithya.
- On 2026-08-21 the previous operator supplied `MOI_Foundations_v2_1_WP_latex_source.pdf` as the new whitepaper, and the old litepaper-as-whitepaper became "Litepaper". The script writes the description "MOI Foundations v2.1" after a title and subtitle for the paper (read it in the script, step 3 below). Check that text against the new abstract before every run.

## Run: swap the whitepaper

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Baseline and the new file | `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" dataroom`; confirm the new PDF is final, its version, and that its text selects. Compare with the live one: `curl -sI https://moi.technology/papers/moi-white-paper.pdf` (size) | Version and size written down |
| 2 | CHECK | Which row holds the old one | `curl -s https://dataroom.moi.technology/api/documents` and read the titles, slots and statuses. Decide by hand which row the new file replaces | The operator names the row |
| 3 | GATE | Get the code (a download), then read the script before running it | Clone as in `dataroom-ship.md` step 2, then read `moi-data-room/scripts/set-whitepaper.mjs`. It writes to production and has no dry run. It finds the document pinned to `network`, uploads the PDF into that document's category, creates a new "White Paper" pinned to `network`, then renames the previous pinned document to "Litepaper", then waits up to 5 minutes for the embedding and exits non-zero on `failed` | Read |
| 4 | LOCAL | Fix the rename for a second swap | The rename to "Litepaper" was right once (2026-08-21). Run again unchanged, it renames the current White Paper to "Litepaper" next to the real Litepaper. Edit step 4 of the script, or skip it and rename by hand | The operator decided what happens to the old row |
| 5 | GATE | ADMIN: run it | The operator runs this in their own terminal, from the root of a Dataroom clone made as in `dataroom-ship.md` step 2 (no `npm ci` needed; Node 18 or newer, because the script uses the built-in `fetch`), and types the secret at a hidden prompt: `read -rs "T?Value for ADMIN_SECRET: " && echo && ADMIN_SECRET="$T" node moi-data-room/scripts/set-whitepaper.mjs <path-to-pdf>; unset T` (zsh; in bash use `read -rsp`). The base address defaults to the live site (`DATAROOM_URL` overrides it). After 5 minutes the script stops waiting and still prints "Done", so read the status line | It prints `Embedding status: completed` |
| 6 | VERIFY | Read the Dataroom | `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" dataroom`; open `/home` on desktop and on a phone (on 2026-08-22 `/home` did not load on a phone; the cause is unknown); ask the chat a question only the new version answers (`dataroom-documents.md` step 6) | The tile shows the new paper and the chat cites it |
| 7 | LOCAL | Website copy, in a clone and branch made as in `website-ship.md` steps 2 and 3 (the clone is a GATE) | Replace `public/papers/moi-white-paper.pdf` and, for a litepaper, `public/papers/moi-lite-paper.pdf` and `public/MOILitePaper.pdf` with the same file. Re-read the blurbs in `PapersPage.jsx` against the new abstract | `shasum -a 256` shows identical copies |
| 8 | GATE | Ship the website | `website-ship.md` | Live |
| 9 | GATE | Chat store, only if the chat is on | Replace `docs/MOILitePaper.pdf`, then `npm run ingest:clear` (`website-chatbot.md`). Skip while the chat is hidden and say so in the hand-back | Done or skipped |
| 10 | VERIFY | Compare every place | `curl -sI https://moi.technology/papers/moi-white-paper.pdf`: `Content-Length` equals the new file's size in bytes; `/home` on the Dataroom shows the new paper; `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" dataroom` has no new WARN | All equal |

## Traps
- The script has no dry run and the first thing that can fail is a rejected sign-in value. On 2026-08-22 the live app held an outdated one; the fix was to set a new secret and run the deploy workflow again (`dataroom-settings-and-database.md`).
- An untracked `whitepaper.pdf` at the root of the previous operator's Dataroom clone has the same checksum as the website's whitepaper. It is local only.
- Paper blurbs describe the paper from its own abstract, never a MOI brief (`website-content.md`).

## Not yet known
- Whether the Dataroom's Litepaper and the website's should be the same file. ASK: Rahul.
- Which Dataroom row is the current whitepaper. ASK: Adithya.
