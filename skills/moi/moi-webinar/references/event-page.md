# Event page: the registration page

Facts are as of 2026-10-02. The public page for a session is made by hand on Luma. Claude drafts the copy in `LUMA.md`, and the operator pastes it in. No Luma automation exists: the previous operator asked on 31 Aug 2026 whether a Luma connector or skill existed and then dropped the idea (the API is probably a paid feature, inferred). Creating or editing the page is an edit to a shared system and needs the operator's explicit yes. Back to `../SKILL.md`.

## The fixed shape

Taken from session 8's `LUMA.md` (local only: ASK: Adithya for the original; a cleaned copy is in `../examples/session-8/LUMA.md`, template in `../templates/LUMA.md`).

| Field | Rule |
|---|---|
| Title | `MOI Builders #N: <outcome in plain words>`, plus two flatter alternates below it for the operator to pick from |
| Subtitle | One question or one line |
| Description | A hook in short sentences (what goes wrong today, then what the session shows), a second paragraph that lets the reader picture the demo, then three blocks below |
| What we will cover | Five bullets. Each is something the viewer will see or learn |
| Bring | Node and the version that was tested, a devnet wallet funded at voyage.moi.technology, the repo `github.com/moi-foundation/MOI-Webinars` |
| One honest note | What is not live yet, said up front. Session 8: "Better said now than discovered later" |
| Practical | A table: date, time, duration, format ("Live, online. Free"), page |
| Short version | Three short lines for a repost, ending "Friday. Free." |

## Copy rules

1. **Carry the hook and the honest note.** The page discloses what is not live. Session 8 said policies cover storage only, and that assets, logic and keys were declared but not live.
2. **Name no cancelled plan, no reviewer, no unmerged feature.** The previous operator rejected posts whose framing still referred to the dropped design (31 Aug 2026). `moi-devrel/references/house-style.md`, section 2.
3. **A narrative angle meant for the deck and the post is not automatically for the page.** Session 8's participant-centric framing was for the main post and the deck, not for the event page.
4. **No emoji, no em dashes, no "not X, not Y".** Run `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" session-<N>/LUMA.md`. The optional helper `humanizer` was used to shorten the description (31 Aug); it is not part of this library. <!-- slop-lint:ignore -->
5. **Every factual line is a claim.** Put it in the claim ledger (`moi-devrel/claim-check`) and check it against `NOTES.md`.
6. **Do not state a Node version you have not tested.** Session 8's page said "Node 20 or newer", while the live demo scripts are run as plain `node scripts/tick.ts` and their author's shell had Node 24. The two are not the same promise (`demo-standard.md`, "Not yet known").

## Time

The audience is told the time in IST, the protocol runs in UTC. Write the date, the 24-hour time and both zones. Run:

```
bash "$SKILLS/moi-devrel/scripts/time-table.sh" "2026-09-04 16:00" Asia/Kolkata
```

For session 8 that printed Fri 2026-09-04 16:00 IST, 10:30 UTC, and an ISO UTC string for scheduling. The zone is `Asia/Kolkata`: the script rejects `IST`, because the abbreviation is ambiguous. Echo the converted time back to the operator before anything is published or scheduled (`moi-devrel/SKILL.md`, step 8).

## The numeral

The title numeral has been wrong once, and it is written in two forms.

- **By 2 Sep 2026.** The live page for session 8 said "MOI Builders VII". `RUNBOOK.md` (1 Sep), `LUMA.md` (2 Sep) and `GAMEDAY.md` (3 Sep) each carried a reminder to fix it, by their file times. The cause was not found; the page was probably duplicated from session 7's event (inferred). Whether it was fixed before the session on 4 Sep is not recorded.
- **2026-10-02.** The live page's title reads "MOI Builders VIII - How to stop an AI Agent From Spending Your Money" (read from the public page). `LUMA.md` says "MOI Builders #8: Stop an AI Agent From Spending Your Money". The page uses a Roman numeral and a hyphen, the repo uses `#8`. The page description begins with the opening lines of `LUMA.md`, so it probably still carries the lockup framing that was cut from the posts (inferred).
- **Rule.** Pick one form per session and use it on the page, in every post and on the deck cover. `session-preflight.sh` fails when the `LUMA.md` numeral does not match the folder. Open the live page and read its title yourself: the file and the page can differ.

## Steps

1. Draft `LUMA.md` the day the topic locks. Show it to the operator with the date, the UTC and IST times and the numeral written out.
2. The operator creates the event and the meeting link, pastes the copy, and sends back the page URL. Confirm date, time, numeral and duration on the page before it circulates.
3. Put the URL in `LUMA.md`, in `SOCIAL.md` (every pre-event post links the page) and in `GAMEDAY.md`.
4. After the session, add the proof-of-completion form and the repo instructions to the page, and send the recap (`after-the-session.md`). Both are next steps recorded for session III.

## Not yet known

The account behind the page is the biggest gap. None of this is in the repo or in Drive.

- Who owns the Luma login, and whether the page sits under a personal or an organisation account. `moi-devrel/references/keys-and-access.md` lists Luma with the owner unknown. ASK: Rahul.
- Which Google account hosts the meeting. Session 8's checklist names a Meet, and the recordings and Gemini notes of two sessions sit under `info@moi.technology`, so that account probably hosts (inferred). ASK: Rahul.
- Whether the page uses approval or a capacity limit, how the meeting link reaches registrants, whether reminder emails go out, and where the registration list is exported to. No Luma export is in Drive. ASK: Adithya.
- Whether a recording link is sent afterwards, and how attendance is tracked. Nothing records either.
- Who may approve the page before it goes public. ASK: Rahul.
