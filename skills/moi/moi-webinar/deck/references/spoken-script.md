# The spoken script: NOTES array and SCRIPT.md

This is the library's single home for read-aloud rules. The community call branch (`moi-webinar/community-call`) and the Builders session guide (`moi-webinar`) point here. It covers any text a person will read out loud from a screen: deck notes, `SCRIPT.md`, a host's planted answer.

## The two copies

A script lives in two places that must say the same thing:

| Copy | What it is | Who reads it |
| --- | --- | --- |
| `SCRIPT.md` in the session folder | the source, one block per slide | the presenter before the session, and anyone reviewing |
| the `NOTES` array in `deck/index.html` | the same words, one string per slide | the presenter window (`P`) during the session |

Edit `SCRIPT.md` first, then copy it into the deck with `sync-notes.py` (full command under "Writing `NOTES`"), and never edit `NOTES` by hand and leave `SCRIPT.md` behind: two hand-edited copies can drift, and as of 2026-10-02 four of session 8's 19 sections differ in cue notation between the two. On 4 September 2026 the presenter window kept showing an old script across at least six messages: notes unchanged, cues missing, the text of slides 10 and 11 not matching the slides. The root cause was not found (inferred: the regenerated file was not the one on screen), so keeping the copies identical is a precaution, not a known fix. After every regenerate, open the deck in a fresh tab and read one slide's notes. `check-deck.py --script SCRIPT.md` compares the copies (check h): it fails when the words differ and warns when only markup or cue notation differs.

Only write a script for the slides the presenter speaks. A slide handled by another speaker needs a `NOTES` entry (the checker wants one per slide) but not a script. An empty string `""` is a valid entry.

## Voice rules

Each rule comes from a correction the previous operator made on a real script. The right-hand column paraphrases what was said. Apply all of them.

| Rule | The correction behind it |
| --- | --- |
| Complete sentences that a person would say, readable aloud word for word | 4 Sep 2026, session 8: a sample line could not be read verbatim, and he asked for complete sentences spoken as if giving a presentation |
| Longer flowing sentences, with a short one only for emphasis | 7 Aug: he asked for longer sentences rather than short staccato ones |
| Warm, not cold | 5 Aug: the last transcript was too cold |
| Paragraphs to read off, never bullet fragments | early Aug: he asked for paragraphs to read word for word |
| No "not this, not that" constructions | 4 Sep, and again 25 Sep on community call 14, where a line of the form "Not save a setting, not call your logic." was cut | <!-- slop-lint:ignore -->
| No showy, dramatic phrasing | 4 Sep, the same correction: he named "aura farming" as the fault |
| No applause lines and no handing over the floor | 25 Sep: an "Open Q&A, the floor is yours" close was removed; the close is one line |
| Real technical depth, and keep code instructions whole | 5 Aug and 4 Sep: he asked for long speeches with good technical depth and for code instructions not to be shrunk |
| Simple for the listener | early Aug: everyone knows what a registry is, so be direct |
| Say the product the way the audience knows it | 25 Sep: "went live on devnet", never "Voyage devnet" | <!-- slop-lint:ignore -->

MOI wording is in `moi-devrel/references/terminology.md`, the one home. Apply it to every sentence of a script.

Say only what the protocol does. When fee delegation was explained, the careful wording was that the payer covers fuel and nothing else, signs each interaction separately, and the user still funds any value they send. Run `moi-devrel/claim-check` over each technical sentence before the script is final, and ASK: Gokul for anything it leaves unconfirmed.

## Pace, and what goes stale

- Planning pace: about 140 words a minute. This is a rough working figure, not a measured one. The three script slides of community call 14 total about 560 words, roughly four minutes at that pace.
- A live demo needs a pause of 5 to 7 seconds between each thing the audience should see.
- Run the command first, then talk over the result.
- Cut or refresh anything that goes stale: live counts ("eleven agents are listed right now"), "last Friday", "since the last call", "this week". Check i of the checker warns on these.
- Never script a number nobody supplied. Say plainly when something in the demo is simulated.
- A line that promises something to the audience ("guests next time") must be true on the day. A teaser in one description outlived its plan once.

## Cues

Anything that is not spoken goes on its own line in square brackets, in plain text. No markdown emphasis or backticks anywhere in a script: the presenter window shows plain text, so markup would appear as typed and the two copies would no longer match.

| Cue | Written as |
| --- | --- |
| Change window | `[SWITCH TO THE BROWSER: launchpad.moi.technology]` then later `[BACK TO SLIDES]` |
| Open a file | `[CURSOR: example.coco, line 12, function Example]`. Give the function name beside the line number so the presenter can search the header if the number moves |
| Type a command | `[RUN: node scripts/tick.ts]` |
| Wait for something on screen | `[WAIT FOR THE REFUSAL]` |
| A question the host may ask | `[If the host asks the zero-KMOI question here: yes, and it only ever covers fuel. You sign the interaction ...]` The words after the colon are spoken if the question comes |
| A guardrail for the presenter | `[CAREFUL: fee delegation covers fuel only]` or `[DO NOT SAY: ...]` |

## SCRIPT.md layout

Copy `templates/SCRIPT.md`. One header per slide, so the presenter can see where to press next:

```
==============================================================
## PRESS NEXT --> SLIDE 3 · Short title
==============================================================
```

Slide 1 uses `## OPENING SLIDE 1 · Title`. The header must contain `SLIDE` and the page number, because the checker and `sync-notes.py` find sections by it. Text outside a slide block (a reading guide, `## If the demo dies`, `## Likely questions`) is ignored. Put a recorded fallback and the likely hard questions with short answers after the last slide, as the session 8 script did. The community call 14 script, before its headers were changed, used plain "## Slide 2, the September release" headers, which the checker also reads, but they carry no "press next" cue, which is weaker than what the previous operator asked for.

## Writing `NOTES`

1. Write or edit the block in `SCRIPT.md`.
2. `python3 "$SKILLS/moi-webinar/deck/scripts/sync-notes.py" <s>/deck/index.html <s>/SCRIPT.md` prints which entries would change. Add `--confirm` to write them. Entries for slides the script does not cover stay as they are, and a slide with no `NOTES` entry at all gets `""`. It never writes `TITLES`: add one title per slide by hand.
3. `python3 "$SKILLS/moi-webinar/deck/scripts/check-deck.py" <s>/deck/index.html --script <s>/SCRIPT.md`. Checks a, e and h must pass.

Why not edit by hand: `NOTES` entries are JavaScript strings. A real line break inside one, a missing comma between two, or an unescaped double quote is a syntax error that kills the whole inline script. The deck still looks fine and the PDF still prints, because print CSS needs no JavaScript, but the arrow keys, the dots and the presenter window stop. As of 2026-10-02 the intro session deck (`skills/moi/moi-webinar/past-sessions/intro-session-deck/` in the handover repo) is in exactly this state. `sync-notes.py` writes each entry with `json.dumps`, so line breaks become `\n` and quotes are escaped. If you must edit by hand, write `\n` for a break and `\"` for a quote. Save files as UTF-8: a script once reached a voiceover tool with an em dash turned into `â`.

## Before you hand the script back

1. Read it aloud once at pace. Rewrite any sentence you stumble on.
2. Run the `humanizer` and `stop-slop` skills over it if they are installed, and apply the changes. The previous operator asked for several rounds on session 8. The checker catches the mechanical part (check g em dashes, check i stale words, check n contrasts) but not the tone.
3. Search for ideas the slides no longer carry. Deleting a slide leaves its words behind in neighbouring notes ("what our campaign is doing" after the campaign slide was cut).
4. Confirm `NOTES` and `SCRIPT.md` match, then reopen the deck in a fresh browser tab and read one slide's notes in the presenter window. Say which file you checked.

## Not yet known

- Who writes and checks scripts for slides presented by other speakers on a community call. ASK: Rahul (inferred to manage the call; the sources name no owner).
- Whether the planted host question was asked on call 14 is not recorded (the previous DevRel's notes); ASK: Vardan.
