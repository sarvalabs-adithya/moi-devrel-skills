# Dataroom: the admin page, adopters, events and leads

Updated 13 October 2026 for PR #7 and the 9 October decision on the Events page. Facts are as of 2026-10-03 from `sarvalabs/moi-dataroom0` `main` (`0f8e38b`: `app/(dashboard)/admin/page.tsx`, `lib/constants.ts`, `supabase/migration-add-calendar-events.sql`, `components/sidebar.tsx`) and the research note dated 2026-10-02. Back to `../SKILL.md`. Documents and embeddings are `dataroom-documents.md`; the papers are `dataroom-papers.md`.

Dataroom: A security finding is open on this product as of 2026-10-02. The handover note is the Open items of `project-handover-docs/DATAROOM.md`; read it before touching its admin.

This file is about the admin page itself. Every step that opens it is an ADMIN step and a GATE (an admin write on production). A step marked ADMIN needs the operator to confirm first that the handover note was read. The operator signs in, in a private window that is closed afterwards. Claude never sees a credential, and none goes in chat, a file or a message.

## What the page offers (labels as read on `main`)

| Section | What it does |
|---|---|
| Add Document (opens the Upload Document form) | `dataroom-documents.md` |
| Each document row | Edit (title, description, section, Home slot, external link), the Download and Email gate toggles, Re-index, Delete. Delete is one click with no confirmation |
| Captured Leads | Visitor emails captured for documents that ask for one |
| Calendar events | Add, edit and delete events for the Events page (needs the table from `migration-add-calendar-events.sql`) |
| Adopters Management | Add Adopter by form, edit, delete, or Import CSV |
| Summary figures | Counts of documents, indexed documents, views, chatbot questions and email leads |

## Run: add adopters
The Adopters page (`/adopters`) is in the menu and lists what is imported.

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Prepare the list | A CSV or TSV (the delimiter is detected). The header needs `Name` or `Project Name`. Optional columns: `Description` (or `Desc`), `Link` (or `URL`, `Website`), `Type`. `Type` is `business` or `dapp`; anything else becomes `dapp`. Rows without a name are skipped. Check each adopter's name and link with its owner; an adopter is a public claim about a partner (`moi-devrel/claim-check`) | The file is reviewed by the operator |
| 2 | GATE | ADMIN: import or add | Admin page, Adopters Management, Import CSV or the form. Each row is sent one at a time | A message "Imported N of M adopters." |
| 3 | VERIFY | Read the page | Open `https://dataroom.moi.technology/adopters` and find the new rows | They show with the right type |

Adopters can also be edited, and deleted, in the same section (GATE). A delete has no archive.

## Run: calendar events (the Events page)
The Events page has been hidden from the menu since 2026-08-22 (pull request #5, "hide Events from sidebar nav for now"). `https://dataroom.moi.technology/events` still answers 200 (2026-10-03). The page stays off for now (decided 9 October 2026); the steps to bring it back are in `project-handover-docs/DATAROOM.md`. Dates are plain dates with an optional end date that must not be before the start. Judge the list from `GET https://dataroom.moi.technology/api/events`, never from the page: when that call fails, the page shows three sample events written in the code (`CALENDAR_EVENTS_FALLBACK` in `src/lib/events.ts`).

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Read the list | `curl -s https://dataroom.moi.technology/api/events` (a JSON list; the page can show sample events instead) | You know the current list |
| 2 | GATE | ADMIN: add, edit or delete | Admin page, Calendar events. Title, start date, optional end date, description, link, location | The row appears |
| 3 | VERIFY | Read the JSON again | The same `curl` lists the change, then open `/events` | It does |

## Run: read the leads
Captured Leads are visitors' email addresses: personal data. Do not paste them into chat, a file in a repository or a message. Who may see them is not recorded. ASK: Rahul.

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Who needs them, and why | The operator names the person and the purpose, and Rahul agrees | A named purpose |
| 2 | GATE | ADMIN: open Captured Leads | Admin page. The operator reads them on screen. Any export or share needs its own yes | The operator has what they need |
| 3 | VERIFY | Nothing left behind | No copy in a repository, a chat or a shared drive unless the operator said so | Confirmed |

## Run: change an admin setting
The chat limits and the other settings are not page features: `dataroom-settings-and-database.md` has the table.

## Traps
- `adopters`, `document_leads` and the column `documents.require_email` were made by hand in Supabase. PR #7 (merged 13 October 2026) added `migration-add-adopters-leads-require-email.sql` for them. A project rebuilt from `schema.sql` and the older migrations alone would break uploads and these pages (`dataroom-settings-and-database.md`).
- The CSV import sends one request per row, and the general API limit is 60 a minute per IP (`middleware.ts`), so a list of more than about 60 rows can stop partway and report "Imported N of M". Split the file and import it in pieces a minute apart (inferred from the limit).
- The Re-index button and the toggles swallow errors silently. Re-read the state after every click.

## Not yet known
- Who may use the admin page, and who else should. ASK: Rahul.
- Who made `adopters`, `document_leads` and `require_email` by hand, and when: not recorded. PR #7 holds the SQL.
- Whether the Events page returns: it stays off for now (decided 9 October 2026). ASK: Rahul.
