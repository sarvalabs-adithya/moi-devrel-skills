<!-- TEMPLATE NOTES (delete this comment when the file is filled in)
Derived from the session 8 game day checklist. Reader: the presenter, the day before and the hour
before. A checklist, not a script. Times: write the date, 24-hour UTC and IST, from
`bash "$SKILLS/moi-devrel/scripts/time-table.sh" "YYYY-MM-DD HH:MM" Asia/Kolkata`.
Tracked in the session 8 branch, so a push publishes it: no reviewer names, no secrets.
-->
# Game day: FILL weekday date, FILL time IST (FILL time UTC)

## Tonight (T-1 day)

1. **Check the event page title.** It must say the right numeral ({{ROMAN}} or #{{NUMBER}}). In session 8 it said the wrong one the night before.
2. **Last-call post.** Drafts are in `social/`. State what is scheduled and what is not. The operator reads it once and posts or schedules it, after a yes for that post.
3. **Send the reviewer the deck and the write-up draft** if they asked for both. The operator sends it.
4. **Read `SCRIPT.md` once out loud, end to end, and time it.** Expected length without the demo: FILL minutes.

## T-60 minutes

5. **Run the demo once, for real.** The run spends devnet funds, so it needs the operator's yes that names the paying account and the cost. From the root of the working copy:
   ```
   cd {{FOLDER}}
   npm run preflight && npm run demo
   ```
   Say what a clean preflight prints (for example "4/4"), and what a leftover from the last run looks like.
6. **Check fuel.** One full run costs FILL (with the date it was measured). Say how many runs the agent holds and the command that tops it up.
7. **Open the deck** and press `P` for the presenter window. Share the deck window in the meeting, keep the presenter window on your own screen.
8. **Have the recording open in a tab**, one click away, not one search away.

## T-10 minutes

9. **Terminal ready.** Big font, in the session folder, command typed but not entered. Clear the scrollback.
10. **Close everything else.** Notifications off. No `.env` open anywhere, nothing with a recovery phrase on screen.
11. **Run the demo one final time** so the node is known to respond. It spends funds: say how much, and get the operator's yes.

## Running order

| | Slides (by title) | Roughly |
|---|---|---|
| FILL block | FILL | FILL min |

## If something breaks

**Demo fails or the node hangs.** Do not debug live. Read the fallback line in `SCRIPT.md`, play the recording, carry on from the receipt slide. Every hash in the recording is on chain.

**Node is slow.** FILL the pause setting that helps.

**Someone asks about the thing that is not live.** Answer with what is live. FILL name the slide that already says it.

**Someone asks whether the agent can get around it.** FILL name the slide, and the one-sentence answer.

## Known state, so nothing surprises you

Fill this in the day before, each line dated. These are the things that were wrong on the last game day:

- The bounty: live or not, and if not, the steps still open. Announce an unfinished bounty as coming, never as open.
- The docs: which pages exist on docs.moi.technology today. Do not point people at a page that is not merged.
- The repo link on the closing slide: open it and confirm it loads.
- The write-up: published or not. Do not say "published" about a post that is a draft.

## After

- The recording and the deck PDF: where they go, and who uploads them (an upload needs the operator's yes).
- The write-up: hand to `moi-blog`. Target: within 48 hours.
- The bounty: open it once its deploy steps are done.
- The proof-of-completion form: link it from the event page and the recap.
