# Call script rules

What is specific to the community call. The voice rules for any text read aloud (complete sentences, readable verbatim, no "not this, not that", no applause lines, warm and flowing) are in `moi-webinar/deck/references/spoken-script.md`. Read that first. Facts are as of 2026-10-02. `SKILLS` is the folder that holds the `moi-*` skills; run every command from the working copy that holds `community-call-<N>/`. Back to `../GUIDE.md`. <!-- slop-lint:ignore -->

## Which slides get a script
- The slides the operator presents. At CC14 the previous operator presented slides 2 to 4, the protocol release (2 and 3) and DevRel (4), and asked for a script for those slides only.
- Slides presented by other people do not need the operator's script. At CC14 the notes for slides 1 and 5 to 12 are first-draft machine text. No request to polish them is on record, so they appear to have had no voice pass (inferred), and some are stale. Slide 1's note still says "what our campaign is doing" after the campaign slide was cut.
- Decide who presents each slide before writing. ASK: Sai Kiran for the marketing slides. If another person presents a slide, ask them whether they want notes. If nobody does, leave the note empty so that no stale machine text appears in the presenter window.
- Every `NOTES` entry still has to exist, empty or not, because the deck needs one entry per slide.

## File and format
- The script lives at `community-call-<N>/SCRIPT.md` and in the deck's `NOTES` array. The two hold identical text. Edit `SCRIPT.md` first, then copy it into the deck with `python3 "$SKILLS/moi-webinar/deck/scripts/sync-notes.py" community-call-<N>/deck/index.html community-call-<N>/SCRIPT.md --confirm`. `sync-notes.py` is a script of the deck branch (`moi-webinar/deck`) and is a dry run that writes nothing until you add `--confirm`. Never edit `NOTES` by hand.
- Use the header format in `../templates/SCRIPT.md`: a banner line, then `## PRESS NEXT --> SLIDE N · <title>`, then the words. The cue is explicit and searchable, as the previous operator asked on 2026-09-04. CC14's own file used plain headers ("## Slide 2, the September release") and is weaker. The cleaned copy in `../examples/cc14/SCRIPT.md` uses the banner format with the text unchanged.
- A line in square brackets is a cue and is not read aloud. Write cues in capitals when they are stage directions, for example `[SWITCH TO THE TERMINAL]`.
- Check with `python3 "$SKILLS/moi-webinar/deck/scripts/check-deck.py" community-call-<N>/deck/index.html --script community-call-<N>/SCRIPT.md`. Check h compares each `NOTES` entry with its section, word for word.
- `NOTES` strings are JavaScript. Use `\n`, never a real line break, or the inline script dies and the keys and presenter window stop working. The PDF still prints, which hides the fault.

## The host's planted question
- Put the cue in the notes of the slide where the question will land, in brackets, in this form: `[If the host asks <the question in a few words> here: <the fifteen-second answer>]`. CC14 slide 2 has one.
- Write the full preparation in `host-qa-prep.md`. Keep the spoken answer and the second beat in the cue, so the presenter reads them straight off the screen. The trap and the fallback stay in the preparation.

## How long each segment runs
Observed word counts of the CC14 notes, at 140 words a minute (a pace inferred from CC14, so time a read-through aloud before relying on it):

| Slide | Words | About |
|---|---|---|
| 1 Title | 43 | 18 seconds |
| 2 September release | 239 (183 without the host cue) | 1 minute 40 |
| 3 Upgrading | 199 | 1 minute 25 |
| 4 DevRel | 122 | 50 seconds |
| 5 to 11 marketing slides | 54 to 85 each, 474 in all | about 3 minutes 20 |
| 12 Close | 14 | 6 seconds |
| Whole deck | 1,091 | about 8 minutes |

Slides 2 to 4 (the previous operator's) came to 560 words, about four minutes. The total length of the call is not on record. ASK: Vardan. A segment that grows past its slot gets cut by deleting a paragraph, not by speaking faster.

## Rules that come from this call's corrections
| Rule | Where it lives |
|---|---|
| MOI wording: devnet ("went live on devnet"), KMOI, capped supply, fuel and fee payer, the release time as a date and 00:00 UTC, participant-centric, network ID | `moi-devrel/references/terminology.md`, the one home. The CC14 corrections of 2026-09-14 and 2026-09-25 are in its tables |
| No closers that hand over the floor, and a date instead of "last Friday", "since the last call" or "this month" | `moi-webinar/deck/references/spoken-script.md`. Both were cut from CC14 on 24 to 25 September 2026 (slide 9 still carried the stale words) |
| Say what the change covers. Fee delegation pays fuel and nothing else | Over-claims were removed from the release post. See `release-slide-checks.md` |
| Do not read figures that are not confirmed in the ledger | See `../templates/numbers-ledger.csv` |
| Do not carry a sentence between drafts without a source | CC14 carried "the people we met there are the ones we are now bringing onto these calls" and "so Claude is the room left to grow" with no source |

## Finishing a script
1. Read every sentence aloud once. Rewrite any sentence you stumble on. A longer flowing sentence is fine; a short one is for emphasis (`moi-webinar/deck/references/spoken-script.md`).
2. Run the prose passes named in `moi-webinar/deck/references/spoken-script.md`.
3. Run the `sync-notes.py` command above with `--confirm` (without it nothing is written), then the deck checker with `--script`.
4. Open the deck in a fresh browser tab, press `P`, and read the notes of the slide you changed back. On 2026-09-04 the presenter window kept showing an old script, in message after message, after a "regenerate".
5. Show the final text to the human once. They read it before the rehearsal.

## Not yet known
- Who writes and checks the scripts for the marketing slides. ASK: Sai Kiran.
- Whether the planted question was asked live at CC14. ASK: the host.
