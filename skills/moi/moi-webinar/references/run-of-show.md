# Run of show: the live plan documents and how they differ

Facts are as of 2026-10-02. Sessions 7 to 9 produced five kinds of live plan. They overlap, and the overlap caused drift. This file says what each one is, where the real ones disagree, and which set a new session writes. The words of the talk are not here: they belong to `SCRIPT.md`, written by `moi-webinar/deck/references/spoken-script.md`. "Local only" below means the file exists only on the previous operator's machine (ASK: Adithya for a copy). Back to `../SKILL.md`.

## The five documents

| Document | Sessions | Job | Differs from the others by |
|---|---|---|---|
| `DEMO-PLAN.md` | 7, 8 (first design), 9 | Choreography for the demo: pre-flight commands, window layout, beats each with a "read the output" table and a quoted "say" paragraph, a timing table with a cut rule, an if-it-breaks table, "things to say precisely" | Demo only. No slides. Session 7's is long (267 lines), the others are compact |
| `TRANSCRIPT.md` | 7 | A pointer to the deck notes, which were the canonical script, plus what does not fit in notes: the pivot, the "say these precisely" list, likely questions, pre-flight | Short (49 lines). Exists because the script lived in a PowerPoint |
| `RUNBOOK.md` | 8 | The whole hour: a cumulative clock, a block per slide range with what to do and ask, likely questions, an if-it-breaks table | Owns time and recovery. Local only |
| `GAMEDAY.md` | 8 | The checklist: tonight, T-60, T-10, running order, if something breaks, known state, after | A checklist with tick boxes, not prose. Tracked on the branch |
| `SCRIPT.md` | 8 | The speech, one block per slide, with cues to switch windows, "if the demo dies" and "likely questions" | Owns the words. The deck notes are generated from it |

Also seen: `FACILITATOR-NOTE.md` (session 7), a one-off brief answering one reviewer's question, now stale because it describes a package that was removed. Do not write one unless a reviewer asks a question that needs an answer in writing.

## Where the real ones disagree (session 8, as of 2026-10-02)

- **Slide numbers are off by one.** `RUNBOOK.md` says "60 minutes, 18 slides" and refers to "slide 12" for where the check happens. The deck has 19 slides, and the check is on slide 13. `GAMEDAY.md` has the same numbering.
- **Three talk lengths.** `SCRIPT.md` says about 30 minutes including the demo, `GAMEDAY.md` says about 24 without it, `RUNBOOK.md` says 60 minutes. The event page says 60. Which one was used live is not recorded.
- **The live command differs.** `RUNBOOK.md` prescribes `DEMO_PAUSE_MS=1500 npm run demo`. `SCRIPT.md` runs four per-beat scripts with plain node, and the commit message of 2026-09-09 ("as presented") says the demo became one small script per action, verified live before the session.
- **Session 7's plan points at a `RUNBOOK.md` that no longer exists.** It was folded into the README and ignored by git.

## What a new session writes (library default)

Inferred from the above, not a recorded practice. Three documents plus the deck:

1. **`RUNBOOK.md`** owns time, recovery and likely questions. It refers to slides by title, never by number, and never restates a sentence of the script. One line says which command is the live one.
2. **`GAMEDAY.md`** owns the checklist. It does not describe the talk.
3. **`SCRIPT.md`**, built with the deck branch (`moi-webinar/deck`), owns every spoken word. Edit it, then copy it into the deck: `python3 "$SKILLS/moi-webinar/deck/scripts/sync-notes.py" session-<N>/deck/index.html session-<N>/SCRIPT.md` shows what it would change, and `--confirm` writes it. Do not hand-edit the deck notes.
4. No separate `DEMO-PLAN.md`: its beats, timing and recovery table are the RUNBOOK's demo block. Write one only for a session that has no RUNBOOK.

The scaffold makes `RUNBOOK.md` and `GAMEDAY.md` from `../templates/`. A cleaned example is in `../examples/session-8/`.

## What goes in the RUNBOOK

1. **A header line:** minutes, slide count, where the deck and the terminal are, and one sentence tying the demo to the idea.
2. **Before going live (T-30):** the exact commands, a tick list, and what the demo heals or refuses on its own.
3. **The talk, cumulative.** Session 8: 0:00 why it exists (14 minutes), 0:14 the mechanism (11), 0:25 the demo (14), 0:39 what you saw (9), 0:48 the honest part (5), 0:53 close and questions (7). Mark the block the whole session hangs on and say not to rush it. State the cut rule ("cut beat 4 if short, never beat 2").
4. **Likely questions, short answers.** Include the awkward ones and the limit in each answer. Session 8 had seven, from "can't the agent delete the policy?" to "so can I cap spending?" (not yet: that policy type is reserved).
5. **If it breaks live:** a table of symptom, cause, what to do. End with the single rule: never claim more than the screen shows.

## Rules

- **Run first, explain after.** Do not open code before the audience has seen it work. Show code, run it, read the output: three loops, each one idea.
- **Pace.** Leave 5 to 7 seconds between beats so the presenter can narrate (asked for in August 2026 during session 7's build). Session 7's browser view used `?gap=7000`, and session 8's terminal demo pauses with `DEMO_PAUSE_MS`.
- **One line when time is short.** Name which beat is cut and which never is.
- **The honest part sits near the end** and is on a slide, so the answer to "can I cap spending?" is already on screen.
- **A live number goes stale.** Refresh it before the run or cut it (`intro-session.md`).
- **Cue grammar** for the script is the deck branch's (`moi-webinar/deck/references/spoken-script.md`). Session 8 used a banner line `PRESS NEXT --> SLIDE N` and italic stage directions. Session 7 used bracketed cues with function names beside line numbers, "so if the number fails I can just search the header".

## Not yet known

- Which talk length was real for session 8, and whether the session was recorded and by whom. ASK: Adithya.
- Who moderated Q&A, and whether a co-host exists. The documents mention none, so the presenter was probably alone (inferred). ASK: Rahul.
