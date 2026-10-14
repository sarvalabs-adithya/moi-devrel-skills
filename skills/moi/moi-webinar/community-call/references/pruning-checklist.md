# Pruning checklist

What is specific to a community call after a slide is removed, moved or added. The mechanics (badges, `TITLES` and `NOTES`, backgrounds, asserted edits, variants, render) are in `moi-webinar/deck/references/build.md`, sections "After deleting, inserting or moving a slide" and "Editing an existing deck safely". Do that checklist first, then this one. CC14 went through about 18 edit rounds in three days and most of its faults were left behind by a prune. Facts are as of 2026-10-02. Back to `../GUIDE.md`.

Run the checklists once per batch of edits, not once per edit. Batch the changes the human asked for, then re-render once. Say the slide's title back before deleting it (the CC14 incident is in the table in `../GUIDE.md`).

`SKILLS` is the folder that holds the `moi-*` skills. Run every command from the working copy that holds `community-call-<N>/`.

## Before the edit
1. **List what the slide said.** Write down its names, figures, key words and their short forms ("Lit Protocol" and "Lit", "campaign" and "click-through"). They are the search terms below.
2. **Note who it hands over to.** A segment's script often leads into the next one. CC14's slide 4 ends "that is the next slide", pointing at the AI visibility slide. Cutting or moving either breaks the pair.

## After the edit
3. **Search for dangling references.** For each term from step 1, search the deck, `SCRIPT.md`, the ledger and the deck README. Grep each key word and its short form:
   `grep -n -i "<term>" community-call-<N>/deck/index.html community-call-<N>/SCRIPT.md community-call-<N>/numbers-ledger.csv community-call-<N>/deck/README.md`
   CC14 residue after four cuts:

   | Left behind | Where | Cause |
   |---|---|---|
   | "what our campaign is doing" | Slide 1 notes | The campaign slide was cut |
   | "Verify the campaign click-through" | Slide 11 bullet and notes | Same |
   | "MOI versus Lit Protocol" (bullet) and "MOI against Lit" (note) | Slide 8 | The comparison slide was cut |
   | "Gemini moved the most, up 12.8 points, while ChatGPT slipped 4.3" | Slide 6 sentence and notes | The trend arrows were removed from the tiles |

   Ask the human whether each hit stays. Do not decide for them.
4. **Dangling references between segments.** Read the last sentence of each segment's script and the first of the next. Fix any that point at a slide that is gone, moved or reworded.
5. **The host cue.** If the slide that carried the `[If the host asks ...]` cue was cut or moved, move the cue to where the question now lands. The host needs to know the new slide: that is a message, so the human sends it.
6. **Teasers.** A "What is next" slide, the description's "Next up" line and any announcement can promise something a cut dropped. Check each against the final line-up. CC13's draft description named guests for CC14 that CC14 did not have.
7. **The ledger.** Retire the rows of removed figures (`dropped`), renumber the `slide` column, then run:
   `python3 "$SKILLS/moi-webinar/community-call/scripts/ledger-check.py" community-call-<N>/deck/index.html community-call-<N>/numbers-ledger.csv --notes`
   It lists any figure left on a slide without a row and any retired figure still showing.
8. **`SCRIPT.md`.** Delete the section and renumber the `PRESS NEXT --> SLIDE N` headers. Then copy it into the deck. `sync-notes.py` is a script of the deck branch and is a dry run unless you add `--confirm`:
   `python3 "$SKILLS/moi-webinar/deck/scripts/sync-notes.py" community-call-<N>/deck/index.html community-call-<N>/SCRIPT.md --confirm`
   Check h of `check-deck.py` then compares the two.
9. **The deck README.** Update the flow line and slide count. CC14's README said "13 slides (with the guest speaker)" after the deck had 12, and "figures unchanged" after the figures changed.
10. **Variants.** Do not keep a variant file for a removed guest. CC14 kept a "no guest" pair that was byte-identical to the main pair. `moi-webinar/deck/references/build.md` covers variants; deleting a file needs the human's yes.

## Render and read back
11. Run `python3 "$SKILLS/moi-webinar/deck/scripts/check-deck.py" community-call-<N>/deck/index.html --script community-call-<N>/SCRIPT.md`. Fix every FAIL. Read every WARN.
12. Render with the PDF's existing name so it lands where you expect: `bash "$SKILLS/moi-webinar/deck/scripts/render.sh" community-call-<N>/deck/index.html MOI_Community_Call_<N>.pdf`. The page count must equal the slide count.
13. Open the HTML in a fresh browser tab. Press `P`. Step through the slides you touched and read their notes.
14. Tell the human what was removed, what was left in and why, and what still needs their decision.

## Moving a slide
Moving a slide means the deck branch's checklist (`moi-webinar/deck/references/build.md`) plus steps 4 to 8 here, and renumbering the `PRESS NEXT` headers. On CC14 the previous operator moved DevRel to slide 4, "after action required". The "next slide" line in the presenter window comes from `TITLES`, so moving a slide without moving its title gives the presenter the wrong preview.

## Not yet known
- Whether the CC14 residue (slide 8 bullet, slide 11 bullet, slide 6 sentence) was meant to stay. The previous operator was asked about the Lit Protocol bullet and the slide 6 sentence and did not answer; not recorded. Decide it with the call's manager (Rahul).
