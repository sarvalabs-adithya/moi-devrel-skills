# Game day: the day itself

Facts are as of 2026-10-02. The sources are session 8's `GAMEDAY.md` and `RUNBOOK.md` and session 7's pre-flight notes. At session 8 only the presenter is on record, and no co-host appears in any document (inferred). At session III a colleague watched the chat. Deck mechanics (the browser, the `P` key, sharing a window, the PDF fallback) are `moi-webinar/deck/references/build.md`, "presenting live", and `moi-webinar/community-call/references/day-of-runbook.md`: they are not repeated here. Back to `../SKILL.md`. The checklist to copy is `../templates/GAMEDAY.md`.

## Gates for the day

A real run of the demo spends devnet funds. Each of these needs the operator's yes that names it, with the paying account and the cost shown: the rehearsal run, the T-60 run, the T-30 run, the final run, a top-up script, and recording a run. Claude never types a recovery phrase and never asks for one. The operator funds the accounts with their own wallet.

**Wallet steps are the operator's.** `npm run preflight`, the top-up script, the demo and each per-beat script load the recovery phrase from `.env`. The operator runs them in their own terminal and pastes the output. Claude reads the output only. `session-preflight.sh` is different: it never opens `.env`, and Claude may run it.

## The day before (T-1)

1. **Open the live event page and read its title.** Check the numeral, date and time against the plan. In session 8 the title was wrong the night before (`event-page.md`).
2. **Last-call post.** Say what is scheduled and what is not. The operator reads it once.
3. **Send the reviewer the deck and the write-up draft,** if they asked for both. The operator sends.
4. **Read `SCRIPT.md` aloud once, end to end, and time it.** Compare with the length the RUNBOOK states. The session 8 documents gave three different lengths.
5. **Run `bash "$SKILLS/moi-webinar/scripts/session-preflight.sh" session-<N>`.** Fix every FAIL, read every WARN. It runs the deck branch's check (`moi-webinar/deck`), which finds a dead script that a printed PDF hides.
6. **Export the PDF and keep a second copy of the folder.** `bash "$SKILLS/moi-webinar/deck/scripts/render.sh" session-<N>/deck/index.html`. A copy on another local disk needs no yes. A copy in Drive is an upload and needs one. Internal documents are local only and are lost with the laptop.
7. **Fill the "known state" block** of `GAMEDAY.md`, each line dated.

## T-60 minutes

8. **The operator runs `npm run preflight` and then the demo once, for real** (wallet steps; Claude reads the pasted output). Preflight prints which checks passed, and a leftover from the last run shows as a count. The demo deletes a leftover policy before beat 1.
9. **Check fuel.** Session 8's `GAMEDAY.md` (written 3 Sep 2026): one run cost 506 KMOI (agent 306, owner 200) and the agent held about 18,885, so about 60 runs. Measure again on the current node.
10. **Open the deck, press `P`, share the deck window,** keep the presenter window on your own screen.
11. **Have the recording open in a tab,** one click from the screen, not one search away. Have the explorer open in another tab, to look up a hash live. The explorer can lag the chain by minutes.

## T-30 and T-10

12. **T-30.** The operator runs preflight, the top-up script and one full demo. All three must exit 0. Owner balance at least the measured threshold (session 8: 30,000 required, about 88,000 at last check). The pause variable ready: at full speed the run is unwatchable.
13. **T-10.** Terminal at presentation size, about 100 columns so banners do not wrap. The command typed, not entered. Scrollback cleared so beat 1 starts at the top of a clean screen. Everything else closed, notifications off, no `.env` open anywhere, nothing with a recovery phrase on screen. One final run so the node is known to respond.

## The live run

- **Run order.** Follow the RUNBOOK's clock and its cut rule. Session 8: why this exists, the mechanism, the code, the demo, what you saw, the honest part, questions.
- **Read the refusal aloud.** When the error prints, stop and read it. Say that it came off the chain, not out of the script.
- **Pause between beats** by the pause variable, not by talking over output.
- **Never claim more than the screen shows.** Do not let a question walk you into claiming a feature that is reserved. Answer with what is live, and point at the slide that already says so.
- **If asked to see it again,** rerun it. Say whether a rerun is idempotent and what it costs.
- **If someone says their own run failed before submission,** they used the SDK's default flow, which simulates first. The demo pins the fuel limit so the refusal happens on chain (`demo-standard.md`).
- **After the last slide,** stop the recording only when the host does, and write down every audience question with an owner for the follow-up.

## If something breaks

Do not debug live. The recording is the contingency and there is no mock mode.

| Symptom | Likely cause | Do |
|---|---|---|
| The demo fails, or the node hangs | devnet slow or down | Say the fallback line, play the recording, resume at the receipt slide |
| `insufficient funds` on an owner action | owner balance too thin (a policy write needs a large balance) | Show the recording or the receipts in `NOTES.md` |
| `insufficient funds` from the agent | agent below 3 times the fuel limit | Run the top-up script, rerun. About 30 seconds |
| Beat 1 writes instead of refusing | a leftover from a crashed run | Let the run finish, it exits non-zero, rerun once |
| "account not found" everywhere | devnet reset, or the wrong derivation path | A reset cannot be fixed live. Fall back (`moi-devrel/references/devnet.md`) |
| A wallet will not send | a stuck interaction at the same sequence number | The cure needs a replacement interaction with enough fuel. Do not try it live. Fall back |
| RPC timeouts | devnet down | Receipts. Every beat's hash is in `NOTES.md` |
| The explorer shows nothing yet | explorer lag | Read the hash through the script, and open the explorer later |
| The whole node is dead | none | The deck stands alone. Present it as what the demo does and offer a recorded run after |
| Arrow keys and `P` dead, slides still show | a syntax error in the deck script | Share the PDF, read from `SCRIPT.md`. The deck check finds this beforehand |
| The presenter window shows an old script | an old file or tab | Close both windows, open the right file in a fresh tab, read one slide's notes back |

The fallback line (`SCRIPT.md`, session 8): "Devnet's having a moment, so let me show you the recorded run. Every hash in it is on chain, and you can verify all of it yourself afterwards."

## Known state, so nothing surprises you (dated example)

On 3 Sep 2026, in the checklist written the night before the 4 Sep session: the bounty was not live (it shipped behind a flag and needed a migration, `MOI_RPC_URL` in the deploy environment and the flag flipped), so it was to be announced as coming. The Points repo had moved to `sarvalabs/Points-Program` with PR 1 unmerged. Nothing on access policies existed on docs.moi.technology because PR 120 had not merged, so nobody was pointed at the docs. The repo link on the closing slide loaded. Write the same four lines for your session.

## Wallets on a shared screen

- Never read, confirm or show recovery words on a recorded call. On 2026-09-24 a phrase read out during a screen-shared wallet setup reached the Gemini notes of the meeting. If it happens, tell the operator, treat that wallet as exposed and stop using it. Deleting the notes or the recording is the operator's own action, after asking the file's owner.
- Use the MOI Wallet extension and the operator's own funded account.

## Not yet known

- Who admits guests to the Meet, who starts the recording and where it lands. The notes of two sessions sit under `info@moi.technology`. ASK: Rahul.
- Whether a co-host watches the chat at every session. Session III's transcript names a colleague who helped with chat, and nothing says it was routine.
- What to do if the wallet extension popup does not appear during a demo that needs one. No evidence. Rehearse it.
