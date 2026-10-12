# Website: the homepage community calendar

Facts are as of 2026-10-03 from `sarvalabs/MOI-Website` `main` (`5e91afa`: `src/components/CommunityCalendar.jsx`, `server/index.js`, `supabase-community-calls.sql`) and GET reads. Back to `../GUIDE.md`.

Website: A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin.

A step marked ADMIN needs the operator to confirm first that the handover note was read.

## How the calendar works
- The "Community" section of the homepage shows 3 rows: it mounts the compact view with `limit={3}`, and nothing else mounts the component. (The component can also list 4 rows, expandable to 16, but no page uses that.) An event drops off one hour after it starts.
- Rows live in the Supabase table `community_calls` and are read from `GET /api/community-calls`, which any visitor can call. The server keeps the list for 5 minutes and empties that cache on every write.
- If that call fails, or returns an empty list, the page shows a schedule written into the code (`CommunityCalendar.jsx`). That fallback holds eight community calls at 14:00 UTC and eight "Twitter AMA" rows at 16:00 UTC from May to December 2026. The month numbers in the file are zero-based: `[9, 23]` is 23 October. It is empty after 2026-12-18.
- The first row the database returns replaces the whole fallback, AMAs included. The table only allows the categories `dev_call`, `office_hours`, `workshop` and `announcement` (a CHECK in `supabase-community-calls.sql`), and the admin form offers the same four. So an AMA exists only in the fallback, and the first real row makes every AMA disappear. Where AMAs should live is undecided. ASK: Rahul.

## State on 2026-10-03

| Fact | Evidence |
|---|---|
| The API answers 500 | The health script, fault W-K1 |
| The browser asks the dev host, so it never sees the database even when the API works | W-K2, `website-health.md` |
| So the homepage shows the fallback: next community call 2026-10-23 14:00 UTC with no link, next AMA 2026-10-17 16:00 UTC. These are dates in code, not confirmed events. `moi-devrel/references/calendar.md` marks call 15 as unconfirmed | Code read 2026-10-03 |
| Zoom account that makes the meeting links: owner unknown | ASK: Rahul |

## Run: add an event
Needs the table to work first. If the check in step 1 answers 500, stop and go to `website-database.md`, then `website-settings.md`.

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Is the API alive? | `curl -s https://moi.technology/api/community-calls` | A JSON list (`[]` is fine). `{"error":"Internal server error"}` means stop |
| 2 | CHECK | Confirm the event | Date, start time, length, category and link from the owner of the event: Vardan for calls and AMAs, then Rahul (`moi-devrel/references/people-and-teams.md`). Convert the time: `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "<YYYY-MM-DD HH:MM>" <area/city>` and read it back | The operator confirmed UTC time, India time and the link |
| 3 | GATE | ADMIN: add it on the admin page | Open the calendar admin page. The operator signs in, in a private window that is closed afterwards (Claude never sees a credential). Signing in writes one test row and deletes it; if a row titled `__ping__` is left, delete it. Fill the form below, then Add Event | The row appears under All Events |
| 4 | VERIFY | Read the JSON | `curl -s https://moi.technology/api/community-calls` and find the title and the `date` | The row is in the list with the right UTC date and category |
| 5 | VERIFY | Read the homepage | Only meaningful once W-K2 is fixed: the cache is emptied on a write, so the row shows at once. Until then the page shows the fallback and proves nothing | The row is in the Community section, or the operator was told it cannot be yet |

The form fields:

| Field | Rule |
|---|---|
| Title | Required |
| Category | Community Call `dev_call`, Office Hours `office_hours`, Workshop `workshop`, Announcement `announcement` |
| Description | Free text |
| Date and Time (UTC) | Required, UTC. The component shows each visitor their own time |
| Duration | Minutes, default 60 |
| Meeting Link | A URL, or empty. Empty or `#` shows "Link TBA", and the compact view puts rows with a real link first |
| Link Label | Default "Join on Zoom" |

## Run: move or remove an event

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Find the row | `curl -s https://moi.technology/api/community-calls` and note the row's title and UTC date. The page shows what you need to edit under All Events | You can name the row |
| 2 | GATE | ADMIN: edit or delete it | The calendar admin page, Edit or Delete on that row. Delete is permanent. Confirm the new UTC time first with `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "<YYYY-MM-DD HH:MM>" <area/city>` | The operator said yes naming the row |
| 3 | VERIFY | Read the JSON | The same `curl`: the row has the new values, or is gone. The list can lag by 5 minutes only if the change was made in the SQL editor | The list is right |

## Run: update the built-in schedule
The fallback is code, so a change is an edit shipped through `website-ship.md`. Do it when the dates in the code no longer match the confirmed ones, and before 2026-12-18 if the database is still down.

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Read the code and the confirmed dates | `COMMUNITY_CALL_DATES` and `TWITTER_AMA_DATES` in `src/components/CommunityCalendar.jsx` (months are zero-based) against the dates Vardan and Rahul confirmed (`moi-devrel/references/calendar.md`) | The differences are listed |
| 2 | LOCAL | Edit the arrays | Keep `SCHEDULE_YEAR` right. Remove a date nobody confirmed | `npm run lint` and `npm run build` pass |
| 3 | GATE | Ship | `website-ship.md` steps 7 to 9 | Merged |
| 4 | VERIFY | Read the page | The Community section shows the new dates. It is the fallback only while the API fails, so say which one you are reading | The dates match the confirmed list |

## Traps
- "The calendar shows events" does not prove the database works. Judge from the JSON.
- Do not run all of `supabase-community-calls.sql`. Its last statement inserts seven placeholder events (every 4 weeks from 2026-05-16, 18:00 UTC, link `#`) that differ from the fallback schedule. Run the table and index statements only.
- The first database row replaces the AMAs (above).
- A failed sign-in test can leave a `__ping__` row (inferred).
- The form has no field for `max_attendees`; the column exists in the table.

## Not yet known
- The real cadence. The fallback follows the Drive sheet (calls on 22 May, 19 Jun, 24 Jul, 21 Aug, 18 Sep, 23 Oct, 20 Nov, 18 Dec); the SQL seed does not. ASK: Vardan.
- Where AMAs should live given the CHECK. ASK: Rahul.
- Who may use the calendar admin page. ASK: Adithya.
