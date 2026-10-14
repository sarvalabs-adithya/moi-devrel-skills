# Website: the next community call on the homepage (Luma)

Updated 13 October 2026 for website PR #60 (merged 13 October), which replaced the homepage calendar with a block that links to Luma. This file follows `project-handover-docs/MOI-WEBSITE.md`; where they differ, that document wins. Back to `../SKILL.md`.

Website: A security finding is open on this product as of 2026-10-02. The handover note is the Open items of `project-handover-docs/MOI-WEBSITE.md`; read it before touching its admin.

A step marked ADMIN needs the operator to confirm first that the handover note was read.

## How the block works
- The homepage block is built from `content/community-calls.json` in `sarvalabs/MOI-Website`: `{"lumaUrl": "", "nextCall": null}` today. The file is read at build time, so a change is a pull request, a merge (which deploys) and a rebuild.
- The block shows only when `lumaUrl` is a web link. With the empty value of 13 October the homepage shows no community section. That is correct, not a fault.
- `nextCall` is optional: `{ "date": "YYYY-MM-DDTHH:MM:SSZ", "title": "...", "url": "https://lu.ma/..." }`. Only the date is required. A date with no time counts for that whole UTC day. If the date has passed, or `nextCall` is null, the block shows only the Luma button.
- Luma is the event-calendar service the community calls are listed on. Its accounts are shared accounts held by Vardan (`ENV-VARS.md`), so he gives the address.
- The old calendar still exists on the server: the Supabase table `community_calls`, the calendar admin page and the Express route `/api/community-calls`. The homepage no longer reads any of them and no longer shows the schedule that was written in code. Retiring them is an open question (below).

## State on 13 October 2026

| Fact | Evidence |
|---|---|
| `lumaUrl` is empty, so the homepage shows no community section | `MOI-WEBSITE.md`, Open items |
| `nextCall` is null. Call 15 (CC15) is expected in the last week of October and its date is not set. Do not write a date until Vardan gives it | `MOI-WEBSITE.md`; ASK: Vardan |
| The old API answered 500 on 2026-10-03 and the health script still checks it as KNOWN fault W-K1. That does not affect the homepage any more | `website-health.md` |

## Run: set or change the Luma link and the next call

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Read the file as it is now | `gh api -H "Accept: application/vnd.github.raw" repos/sarvalabs/MOI-Website/contents/content/community-calls.json` (a read; needs `gh` signed in) | You can say what `lumaUrl` and `nextCall` hold |
| 2 | CHECK | Get the facts from the owner | The MOI Luma calendar or event address, and for a call its date, start time and title, from Vardan, then Rahul (`moi-devrel/references/people-and-teams.md`). Convert the time: `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "<YYYY-MM-DD HH:MM>" <area/city>` and read it back | The operator confirmed the UTC time and the address |
| 3 | GATE | Get the code (a download) and a branch | `website-ship.md` steps 2 and 3. Use the branch prefix `content/` | Clone and branch ready |
| 4 | LOCAL | Edit the file | Set `lumaUrl` to the Luma address, which must start with `https://`. Set `nextCall` to the object above, or leave it null. Keep the JSON valid: `python3 -m json.tool content/community-calls.json` | The command prints the file back with no error |
| 5 | LOCAL | Check, because CI will not | `npm run lint` and `npm run build`; `npm run dev` and read the homepage | The block shows, its button goes to Luma, the date and title are right |
| 6 | GATE | Push and open one PR | `website-ship.md` steps 7 and 8; read the preview | The operator has read the preview |
| 7 | GATE | Merge (this deploys the site and the blog) | `website-ship.md` step 9 | Merged |
| 8 | VERIFY | Read the live homepage | Wait for the run (`website-ship.md` step 10), then open `https://moi.technology/`. A green run alone proves nothing | The community block is there with the right link, and the next-call line is right or absent on purpose |

## Run: hide the block or clear a past call
Set `lumaUrl` to an empty string to hide the whole block, or `nextCall` to `null` to keep only the Luma button, then follow steps 3 to 8 above. A past `date` hides the call line by itself, so clearing it is tidiness, not a fix.

## The old calendar (server only)
- The table, the admin page and `GET /api/community-calls` are judged from the JSON: `curl -s https://moi.technology/api/community-calls`. Adding an event there changes nothing a visitor sees, so do not.
- The admin routes accept a default key written in the public source, because the deploy does not pass `ADMIN_API_KEY`. A fix is pending; see the Open items of `project-handover-docs/MOI-WEBSITE.md`.
- `supabase-community-calls.sql` is described in `website-database.md`. Never run its last statement.

## Traps
- An empty `lumaUrl` hides the block, and so does a value that is not a web link. Neither is a bug.
- The file is read at build time. Editing it on the server or in the browser changes nothing; only a merge and a rebuild do.
- A date with no time covers the whole UTC day. Write the time when the start matters.
- Do not write the date of call 15 before Vardan gives it. The date is a public statement.
- `web-health.sh` still checks the old calendar API and the baked API base. A KNOWN or FAIL line there is about the server, not the homepage block.

## Not yet known
- The Luma address to put in `lumaUrl`, and the date of call 15. ASK: Vardan.
- Whether to retire the old table, admin page and `/api/community-calls` routes. ASK: Rahul, then Srikar for the server.
- Who may use the old calendar admin page while it exists. ASK: Rahul.
