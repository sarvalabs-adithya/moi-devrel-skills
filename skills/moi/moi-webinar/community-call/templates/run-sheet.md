<!-- TEMPLATE NOTES (delete this comment when the file is filled in)
The shape of the first reply to a call's agenda (`../references/agenda-intake.md`). Shown in chat
first; saved as community-call-<N>/RUN-SHEET.md when the human starts the first item. Rows come
from the catalogue in agenda-intake.md, oldest due date first. Drop a row the agenda makes
irrelevant and say so under the table. Paths in "With" are relative to $SKILLS/moi-webinar/.
Status is one of: open, started, drafted (waiting for the owner's yes), done, LATE, dropped.
-->
# Community Call #<N>: run sheet

Call: <Weekday YYYY-MM-DD>, <HH:MM> IST (<HH:MM> UTC). Host: <name, or ASK>. Room: Riverside. Page: Luma.

Agenda as understood:
1. <Segment>: <presenter>
2. <Segment>: <presenter>
Guest: <name, company, as given; or "none">

ASK: <anything the agenda leaves open>

| # | Due | Item | Owner | Claude produces | With | Status |
|---|---|---|---|---|---|---|
| 1 | <T-9, Wed date> | Input requests to each owner, due <T-7 date>; guest's due <T-3 date> | DevRel | One draft per owner | `community-call/templates/input-request-messages.md`, messages <list> | open |
| 2 | <T-9> | Luma page: agenda, date, Riverside link | Vardan | Page copy | `community-call/templates/LUMA.md`, "Page" | open |
| 3 | <T-9> | First announcement, with the Luma link | Vardan | X and LinkedIn drafts | `community-call/templates/SOCIAL.md`, "T-9" | open |
| 4 | <T-7, Fri> | Numbers ledger | DevRel | `community-call-<N>/numbers-ledger.csv` | `community-call/templates/numbers-ledger.csv`, `community-call/scripts/ledger-check.py` | open |
| 5 | <T-7> | Slide plan | DevRel, manager signs off | Plan table | `community-call/references/slide-plan.md` | open |
| 6 | <T-7 to T-3> | Deck (guest slide if any) | DevRel | `community-call-<N>/deck/index.html`, PDF | `deck/GUIDE.md`, `deck/references/guest-slide.md`, `deck/scripts/render.sh` | open |
| 7 | <T-7 to T-3> | Release-slide check | DevRel | A verdict per line | `community-call/references/release-slide-checks.md` | open |
| 8 | <T-7 to T-3> | Script for the operator's slides | DevRel | `community-call-<N>/SCRIPT.md` | `community-call/templates/SCRIPT.md`, `deck/scripts/sync-notes.py` | open |
| 9 | <T-4, Mon> | Second post; both Luma lists invited | Vardan | X and LinkedIn drafts | `community-call/templates/SOCIAL.md`, "T-4" | open |
| 10 | <T-3, Tue> | Guest details final | <who invited the guest> | Guest slide filled | `community-call/references/inputs-checklist.md`, "The guest slide" | open |
| 11 | <T-3> | App and page links into Luma and the Riverside description | Vardan | Links block | `community-call/templates/LUMA.md`, "Links block" | open |
| 12 | <T-3> | YouTube description draft | DevRel | `community-call-<N>/description.txt` | `community-call/scripts/youtube-description.py` | open |
| 13 | <T-2, Wed> | Speakers invited to Riverside | Vardan | Speaker list for Vardan | `community-call/templates/input-request-messages.md`, message 9 | open |
| 14 | <T-2> | Third post | Vardan | X and LinkedIn drafts | `community-call/templates/SOCIAL.md`, "T-2" | open |
| 15 | <T-1, Thu, HH:MM IST> | Luma announcement, 24 hours before | Vardan | Text | `community-call/templates/LUMA.md`, "Announcement, 24 hours" | open |
| 16 | <T-1> | Host's planned question | <host> | Answer, follow-up, what not to say | `community-call/references/host-qa-prep.md` | open |
| 17 | <T-0, HH:MM IST> | Last post and Luma announcement, 1 hour before | Vardan | Both texts | `community-call/templates/SOCIAL.md`, "T-0"; `community-call/templates/LUMA.md`, "Announcement, 1 hour" | open |
| 18 | <T-0> | Day-of check and PDF | DevRel | Sweep, PDF | `community-call/references/day-of-runbook.md` | open |
| 19 | <After> | Description timestamps, Q&A log, recap posts, shorts | DevRel; Vardan for posts | Drafts | `community-call/references/after-the-call.md`; `community-call/templates/SOCIAL.md`, "After" | open |

Dropped: <rows removed, and why>

Claude drafts; nothing is sent, posted, scheduled, uploaded or pushed, and nothing is changed in Luma or Riverside, without your yes for that item. Speaker and guest details come only from the speakers.

Which of these should I start?
