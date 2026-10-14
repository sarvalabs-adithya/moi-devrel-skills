# Agenda intake: from the agenda to a dated run sheet

Step 0 of the run. When the host or the operator gives the call's agenda, the first reply is a dated checklist of everything the call needs and one question. Nothing else is drafted, written or run until the human picks an item. Back to `../GUIDE.md`.

The timeline and the owners come from the handover note for the call (`project-handover-docs/COMMUNITY-CALL.md` in `sarvalabs/moi-devrel-skills`, as of 2026-10-13). They are copied here so the branch does not depend on that file. Where the note and an older reference in this branch disagree, the note is newer.

## The input

- **The agenda:** the segments in order, who presents each, and the guest if there is one. Take names, roles and topics only as given. A guest's role, company and topic come from the guest (`inputs-checklist.md`, "The guest slide").
- **The call date** and the start time, in IST. The call is usually a Friday. CC15 has no date yet (expected in the last week of October 2026): ASK: Vardan. With no agenda at all, ASK: Vardan too.
- **The call number.** If it is missing, ASK: Vardan (message 1 of `../templates/input-request-messages.md`).

If no date is given, the reply lists the items with their offsets only (T-9, T-7 and so on) and asks for the date as well as the closing question.

## The reply, and nothing else

1. One line that restates the agenda as understood: segments, presenters, guest. Anything unclear is an `ASK:` line under it.
2. The run sheet, in the shape of `../templates/run-sheet.md`: every item of the catalogue below, oldest due date first, with its date, owner, what Claude can produce and the exact tool. Drop an item the agenda makes irrelevant (no guest, no product segment) and say so in one line.
3. A line that items owned by Vardan or the host are drafts for them: Claude never sends, posts, schedules or edits Luma or Riverside.
4. The closing question, word for word: "Which of these should I start?"

Do not draft a message, a post, the Luma copy or a slide in this reply. Do not create the call folder or run any script except the date command below. When the human names an item, do that item only, by the tool named in its row, then show the sheet again with the item ticked. The first item started also saves the sheet as `community-call-<N>/RUN-SHEET.md`.

## Dates

Count back from the call day. Use this command for the weekdays, with the call date as `YYYY-MM-DD` in place of `<call date>`; do not work them out by hand:

```
python3 -c 'import datetime as d,sys; c=d.date.fromisoformat(sys.argv[1]); [print("T-%d" % k, (c-d.timedelta(days=k)).strftime("%a %Y-%m-%d")) for k in (9,7,4,3,2,1,0)]' <call date>
```

If the call is not on a Friday, keep the day offsets and say the weekdays moved. An item whose date has already passed is marked `LATE` and listed first. For a Luma announcement at 24 hours and 1 hour before, and the last post, write the clock time in IST and UTC from `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "<YYYY-MM-DD HH:MM>" Asia/Kolkata`. Write "ASK: start time" when the time is unknown.

## The catalogue

"DevRel" is the operator. Owners other than DevRel are from the handover note. Every "With" path is relative to `$SKILLS/moi-webinar/`.

| Due | Item | Owner | Claude produces | With | Gate |
|---|---|---|---|---|---|
| T-9 | Request every input, due T-7; the guest's due T-3 | DevRel | One draft per owner | `community-call/templates/input-request-messages.md`, messages 1 to 7 and 9 | Sending |
| T-9 | Luma page: agenda, date, Riverside link | Vardan | The page copy | `community-call/templates/LUMA.md`, "Page"; rules in `references/event-page.md` | Creating or editing the page |
| T-9 | First announcement, with the Luma link | Vardan | X and LinkedIn drafts | `community-call/templates/SOCIAL.md`, "T-9"; rules in `references/pre-event-social.md` | Posting, scheduling, any run of `scripts/buffer.mjs` |
| T-7 | Updates in; every figure in the numbers ledger | DevRel | `community-call-<N>/numbers-ledger.csv` | `community-call/templates/numbers-ledger.csv`, `community-call/scripts/ledger-check.py` | None, local |
| T-7 | Slide plan | DevRel; sign-off by the call's manager | The plan table | `community-call/references/slide-plan.md` | The manager's yes |
| T-7 to T-3 | The deck, with a guest slide if there is a guest | DevRel | `community-call-<N>/deck/index.html` and its PDF | `deck/scripts/new-deck.sh`, `deck/GUIDE.md`, `deck/references/guest-slide.md`, `deck/scripts/check-deck.py`, `deck/scripts/render.sh` | Pushing the folder |
| T-7 to T-3 | Release slides checked against the note | DevRel | A verdict per line | `community-call/references/release-slide-checks.md` | None |
| T-7 to T-3 | Script for the operator's slides | DevRel | `community-call-<N>/SCRIPT.md`, copied into the notes | `community-call/templates/SCRIPT.md`, `community-call/references/call-script.md`, `deck/scripts/sync-notes.py` | None, local |
| T-4 | Second post; both Luma lists invited | Vardan | X and LinkedIn drafts | `community-call/templates/SOCIAL.md`, "T-4" | Posting; the invite is Vardan's in Luma |
| T-3 | Guest details final | Whoever invited the guest | The guest slide filled | `community-call/references/inputs-checklist.md`, "The guest slide"; message 7 | Telling the guest anything is confirmed |
| T-3 | Links to any app or page the deck shows go in the Luma page and the Riverside description | Vardan | The links block, taken from the deck | `community-call/templates/LUMA.md`, "Links block" | Editing Luma or Riverside |
| T-3 | YouTube description drafted from the agenda, same links | DevRel | `community-call-<N>/description.txt` | `community-call/scripts/youtube-description.py`, `community-call/templates/youtube-description.md` | Uploading |
| T-2 | Every speaker invited to Riverside | Vardan | The speaker list with each segment, for Vardan | `community-call/templates/input-request-messages.md`, message 9 | Sending |
| T-2 | Third post | Vardan | X and LinkedIn drafts | `community-call/templates/SOCIAL.md`, "T-2" | Posting |
| T-1 | Luma announcement to everyone signed up, 24 hours before | Vardan | The text | `community-call/templates/LUMA.md`, "Announcement, 24 hours" | Sending |
| T-1 | The host's planned question | Host | A short answer, a follow-up line, what not to say | `community-call/references/host-qa-prep.md`; message 6 | Telling the host anything is confirmed |
| T-0, 1 hour before | Last post and a Luma announcement to everyone signed up | Vardan | Both texts | `community-call/templates/SOCIAL.md`, "T-0"; `community-call/templates/LUMA.md`, "Announcement, 1 hour" | Posting, sending |
| T-0 | Day-of check: stale words, the PDF | DevRel | The sweep result, the PDF | `community-call/references/day-of-runbook.md`, `deck/scripts/render.sh` | Uploading the PDF |
| After | Description with timestamps, Q&A log, recap posts and shorts | DevRel for the description and the log; Vardan for posts and shorts | Drafts | `community-call/references/after-the-call.md`; `community-call/templates/SOCIAL.md`, "After" | Uploading, posting |

A write-up post about the call is `moi-blog`, not this branch.

## Owners (handover note, as of 2026-10-13)

| Thing | Owner |
|---|---|
| Deck, protocol and DevRel segments | DevRel (the operator) |
| The event, Luma page, Riverside room, posts and shorts | Vardan. Luma, Riverside and YouTube are shared accounts he holds |
| Host | Ruta |
| Protocol updates | Protocol team (Rahul) |
| Marketing updates | Marketing (Sai Kiran) |
| Partnerships updates | Piyush |
| Product updates, not every call | Pratik (spelled Prateek in `segments-and-roles.md`; the spelling is open) |
| Guest speaker | Agreed on the weekly marketing sync (confirm the name; earlier notes called it the cadence call). Final by the Tuesday before the call |

## Not yet known

- Whether Vardan wants post and Luma drafts from DevRel, or writes his own. Ask before drafting them (message 9). ASK: Vardan.
- How Riverside invites are sent and whether each speaker gets their own link. ASK: Vardan.
- Whether Ruta (the host, per the handover note) hosts every call. Confirm it each call.
- How the audience watches (Riverside live, or the Luma page). ASK: Vardan.
