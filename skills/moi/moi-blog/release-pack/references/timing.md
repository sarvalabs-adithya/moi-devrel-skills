# Timing: the order of events around a release, and the time trap

Facts are as of 2026-10-02. **One release is on record**, moipod v0.13.0, so every time below is from that one. `ASK:` is defined in `moi-devrel/SKILL.md`. `SKILLS` is set as in `../GUIDE.md`. Back to `../GUIDE.md`.

## What happened around v0.13.0
| When (UTC) | Event | Source |
|---|---|---|
| 2026-09-10, time not recorded | The note reaches the previous operator. The go-moi tag is dated 10 September. The upstream watch files "Upstream release: go-moi v0.13.0" | Research; the checklist of PR #53; `moi-devrel/references/calendar.md` |
| 2026-09-10 | Devnet still answers `net.Version` 0.12.0 and the field `payer` | `moi-devrel/references/devnet.md` |
| 2026-09-10, about 08:45 (12:45 Dubai time) | The time the research records for the pack, about 15 hours before the moment. Two wrong schedules were deleted by hand and a correction reply was drafted | Research, inferred from prompt order |
| 2026-09-10, 10:12 | The commit that adds `--thread-dir` to `buffer.mjs` is dated 14:12 +0400 | `git log` |
| 2026-09-10, 10:52 | The pack is committed locally, 14:52 +0400. It is not pushed | `git log` |
| 2026-09-10, 13:26 | PR #53 (release post) opened in `sarvalabs/MOI-Website` | Research |
| 2026-09-11, 00:00 (as the pack gave it) | The network update as announced. Devnet was wiped and the registry `c684f926` is gone, but the minute is not confirmed. The moment is from the correction reply and `moi-devrel/references/devnet.md`. No written confirmation is on record, and on 2026-10-02 the explorer's oldest listed interaction was dated 2026-09-10 13:18 UTC, with the list stopping at 355 entries, so it may be capped rather than complete (`moi-devrel/claim-check/references/live-reads.md`). ASK: Gokul when devnet moved to v0.13.0 | `moi-devrel/references/devnet.md`, `moi-devrel/claim-check` |
| 2026-09-11 | The Discord copy is written | Research |
| 2026-09-11, 13:04 | PR #53 merges, about 13 hours after the announced upgrade. The copy PR #56 opens 26 seconds later. As of 2026-10-02 it is still open | Research |
| 2026-09-15, 09-22, 09-23 | Launchpad moves to the new registry `2f3e9469` 4 days after the wipe and Explorer 11 days after. MCP pins it 12 days after, and the live MCP was still on the wiped registry on 2026-10-02 | `devnet.md` |
Not settled: the commit adding `--thread-dir` is dated after the 12:45 Dubai time, so the order in which the thread was scheduled is unclear. ASK: Adithya.

## The order to follow next time
No lead time and no standard sequence are on record. This order follows from what depends on what.
1. The note arrives. Save it and hash it. Put the questions in `the-note.md` to the protocol team.
2. The release moment is confirmed in writing as a date and a 24-hour UTC time.
3. Ledger rows, drafts, `thread-lint.py`, `slop-lint.sh`. The operator reads every post once.
4. The pack goes out before the moment, as drafts or scheduled. It says "scheduled for". v0.13.0 went out about 15 hours before. Why 12:45 Dubai was chosen is not recorded. ASK: Rahul for the lead time he expects.
5. The moment passes. Read the node: version, network ID, wire field name (`moi-devrel/references/devnet.md`, "Before you say live").
6. Only now may any text say "live". The v0.13.0 Discord copy said "is live" and no node read for it is on record.
7. The release post merges when its ledger is clean. Merging announces nothing. Step 9 of `moi-blog/SKILL.md` then announces the published post.
8. If devnet was wiped, the products need their redo. See below.

## Write the moment
Write the date, 24-hour UTC and India time in one phrase: "00:00 UTC on 11 September (05:30 IST)". Convert with the script and read its output to the operator before anything is scheduled:
`bash "$SKILLS/moi-devrel/scripts/time-table.sh" "2026-09-11 00:00" UTC`
| Do not write | Why | Write |
|---|---|---|
| "scheduled for today at 12:00 AM UTC" | The note's own wording. No date. "Today" had passed when the post ran. AM was read as noon | "scheduled for 00:00 UTC on 11 September (05:30 IST)" <!-- slop-lint:ignore --> |
| "12:00 AM", "00:00 AM UTC" | Read as midday | "00:00 UTC" <!-- slop-lint:ignore --> |
| "5:30 AM IST" | A 12-hour form again | "05:30 IST" |
| "today", "tonight", "tomorrow" | Stale once scheduled | The date |
| "9:15 EST" | EST is UTC-5 all year. In summer it is an hour wrong | Give the zone as `America/New_York` to `time-table.sh` |
For 2026-09-11 00:00 UTC the script gives: India Fri 05:30, US Eastern Thu 2026-09-10 20:00 EDT, US Pacific Thu 17:00 PDT, Central Europe Fri 02:00 CEST, Singapore Fri 08:00. Dubai is `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "2026-09-11 04:00" Asia/Dubai`, which prints 00:00 UTC. It is a Friday.

## The incident, 2026-09-10
1. The note said "scheduled for today at 12:00 AM UTC". The pack was scheduled about 08:45 UTC the same day, so that moment had apparently passed and many readers would take it for noon. <!-- slop-lint:ignore -->
2. The previous operator asked whether 12:00 UTC means 12:00 AM and whether "00:00 AM UTC" is the right form. Two wrong schedules were deleted by hand in Buffer. <!-- slop-lint:ignore -->
3. `SOCIAL.md` of the pack then said the time was "corrected to 12:00 UTC (noon)". That contradicts the real moment, 00:00 UTC on 11 September, and its own post text.
4. The rewritten posts say "11 September at 12:00 AM UTC (5:30 AM IST)", which keeps the AM form. <!-- slop-lint:ignore -->
5. The correction reply states "00:00 UTC on 11 September". That form, with the date, is the first one in the evidence. See `corrections.md`.
The date came from the correction reply and the later drafts, not from the note. ASK: Gokul to confirm it in writing.

## Scheduling rules
- A Buffer `--at` value ends in `Z`. Without it the machine's local zone is used.
- A scheduled post publishes with nobody reviewing it. Use a draft unless an exact time matters, and publish it yourself at the time.
- Echo the UTC and India times to the operator before `--confirm`, and again after, from Buffer.
- A text that says "scheduled for" is true only before the moment. Do not leave one scheduled to publish after it.

## What an upgrade does to devnet and the products
- The v0.13.0 note does not say devnet would be wiped. The release post says it was ("Devnet was reset for this release"). Ask the protocol team before the pack goes out, and tell the operator the answer.
- A wipe removes accounts, assets, contracts and registry ids. Three repos pin the registry id separately: the Launchpad moved 4 days after the wipe, the Explorer 11 and the MCP pinned the new id after 12 (not deployed on 2026-10-02). A go-moi release was followed by a wipe the next day, in one observation. ASK: Gokul whether that holds.
- Signs, earliest first: the upstream watch issue, a message from the protocol team with a new registry id, the nightly canary issue, the Launchpad stats showing "unreachable", a user's "account not found". The list and the first-hour outline are in `moi-devrel/references/devnet.md`.
- Whether the pack should warn developers that devnet state will be wiped is not recorded. ASK: Gokul.
- After a wipe, `moi-devnet-reset` holds the redo for each product (`moi-devnet-reset/references/order-of-work.md`). Grep every doc, deck and post for ids that changed.

## Not yet known
- The lead time Rahul expects, and whether a pre-release pack is standard. ASK: Rahul.
- Who confirms the release moment with the protocol team, and who reads the node afterwards. ASK: Rahul.
- Whether devnet was on v0.13.0 when the CC14 call ran. No read from that day is on record. ASK: Adithya whether he checked.
