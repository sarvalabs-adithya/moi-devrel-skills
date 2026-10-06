# Lifecycle: what is due when

Facts are as of 2026-10-02. **Observed** means a file, a commit or a Drive record shows it. **Inferred** means read from the evidence, not stated. **Library default** means this skill's own recommendation, built from two sessions. Only sessions 7 and 8 have enough record to build a timeline. In the tables, "main", "branch" and "local only" mean what `session-history.md` says they mean. Local only: ASK: Adithya for a copy. Back to `../SKILL.md`.

## The documents, in the order they were written

| Document | Reader | Job | Where it lives |
|---|---|---|---|
| `STORYLINE.md` (session 7) | the lead, who asked for it | The series arc: one idea per phase, the aha per phase, the exact language | local only |
| `PLAN.md` (session 8 first design, 9) | presenter and reviewer | Options with a recommendation, the holes in the old design, what must be proven live, build order | branch |
| `NOTES.md` (session 8) | the presenter | Build log: why the design changed, the verified-live table with hashes, live findings, claim audit | branch |
| `README.md` | students | The idea, run commands, limits stated plainly, files in reading order | main for 1 to 7, branch for 8 and 9 |
| `DEMO-PLAN.md` (7, 8, 9) | the presenter | Choreography, beats with "say" blocks, timing, if-it-breaks table | session 7 local only; 8 and 9 branch |
| `RUNBOOK.md` (session 8) | the presenter | Timed run-of-show, likely questions, recovery table | local only |
| `GAMEDAY.md` (session 8) | the presenter | T-1 day, T-60, T-10 checklist, running order, known state, after | branch |
| `SCRIPT.md` (session 8) | the presenter | Word-for-word speech, one block per slide. The deck notes come from it | branch |
| `LUMA.md`, `SOCIAL.md`, `social/` | event page and posts | Paste-ready copy | local only |
| `BLOG.md`, `blog-assets/` | search and AI engines | The write-up and its publishing files | branch |
| `TRANSCRIPT.md`, `FACILITATOR-NOTE.md` (session 7) | presenter, one reviewer | A pointer to the deck notes plus the "say precisely" list; a one-off brief | local only |

`run-of-show.md` says how the live plan documents differ and which to keep. The scaffold in `../scripts/new-session.sh` makes the set this skill recommends.

## Observed timelines

| Session 7 (Fri 2026-08-07, date inferred) | |
|---|---|
| Tue 4 Aug | Strategy call: one idea per talk, a blog per talk, the three-phase storyline asked for |
| 4 to 5 Aug | Spec, decisions handoff, first full build |
| 5 Aug | Deck written as slide notes. Two demo clips saved in Drive, probably fallback or promo clips (inferred; file times 22:11 and 22:33 UTC) |
| 6 Aug | Deck exported (Drive, 03:59 UTC). `devnet.md` dates a registry failure to this day. Registry writes were down, and the deck and transcript were rewritten around two existing agents. The research notes put that rewrite two days before the session, which is 5 Aug and does not match; no record settles it. ASK: Adithya |
| Fri 7 Aug | Live. The proof form was created at 11:50 UTC. The write-up was drafted and fact-checked the same day |
| 7 to 8 Aug | About 25 write-up commits. The text-only Medium path was chosen on 8 Aug |
| 7 Sep | The edited recording appears in the external editor's folder, a month later |

| Session 8 (Fri 2026-09-04, 16:00 IST) | |
|---|---|
| Mon 31 Aug | Call with the lead (9:47). The first design is dropped and the access-policy demo replaces it; the notes say the reviewer rejected it "on the 27th", which the call evidence does not show (ASK: Adithya). The new demo is spiked and verified end to end the same day. Event page copy, social copy, a first HTML deck, a rehearsal video and a voiceover are all made |
| Tue 1 Sep | Claim audit adds two live tests. A second pair of posts written |
| Wed 2 Sep | The reviewer's changes to the deck. Commit "the access policy demo, deck, blog and recording" |
| Thu 3 Sep | Game day plan and the full script |
| Fri 4 Sep | Script rewritten again. Live at 10:30 UTC |
| Wed 9 Sep | Commit "final script, per-beat demo scripts, deck and blog as presented" |

Both sessions went from the lead's call to live in three to four days. The write-up for session 8 was written before the event and dated 4 Sep. As of 2026-10-02 it is not published (`session-history.md`).

## Schedule

Held dates on record: session 2 Fri 2026-06-12, session 3 Thu 2026-06-18, session 7 Fri 2026-08-07 (inferred), session 8 Fri 2026-09-04 at 16:00 IST. Three of four were Fridays, so propose a Friday and let the topic lead and Rahul confirm it (library default, not a recorded rule). No calendar for Builders sessions is on file. ASK: Rahul.

## What is due when (library default)

T is the event start. Replace every date with one from `time-table.sh`.

| When | Due | Basis |
|---|---|---|
| T-5 days | Topic locked with the lead. Event page and first posts drafted the same day | Session 8: copy drafted 31 Aug for 4 Sep |
| T-5 to T-4 | Spike, then the demo verified end to end, receipts in `NOTES.md` | Both sessions: spike first |
| T-4 | Claim audit of script, deck, event page and posts | Session 8: 1 Sep |
| T-3 | The reviewer has the deck and the write-up draft and has answered | Session 8: 2 Sep. Who reviews: ASK: Rahul |
| T-3 to T-1 | Event page live. Posts scheduled once the operator has read each | Session 8 |
| 0 to 4 days before | Proof-of-completion form created | Drive: 3.5 days (II), 75 minutes (III), the day (VII) |
| T-1 day | Game day plan done. Script read aloud once and timed. Last call post | `GAMEDAY.md` |
| T-60 min | One real run of the demo | `GAMEDAY.md` |
| T+0 | Live. Recording started by whoever hosts the meeting | Host: unknown |
| T+48 hours | Write-up published. A target: session 8 did not meet it | `BLOG.md` footer of session 7, "within 48h" |
| After | Recording to the editor, submissions verified on chain, bounty opened when its deploy steps are done | `after-the-session.md` |

Inferred: the order inside T-5 to T-3 can change, but three dependencies hold. The event page needs a final title and time before any post links it. The script needs a verified demo before it states a number. A claim audit has to finish before anything is scheduled.

## Not yet known

- Who must approve before the event page goes public. ASK: Rahul.
- Whether the 24 and 48 hour follow-up targets from the January 2026 KRA document, written for community calls, apply to Builders sessions. ASK: Rahul.
- Whether any session had a run-of-show required 48 hours ahead. None is in Drive.
