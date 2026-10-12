# Host Q&A prep

How to prepare an answer to a question the host plants. Facts are as of 2026-10-02. `SKILLS` is the folder that holds the `moi-*` skills; run every command from the working copy that holds `community-call-<N>/`. Back to `../GUIDE.md`.

## Why a planted question exists
A Slack message of 2026-09-25 to the previous operator said the host had noticed more traction when questions are asked to the audience and to the presenter, and might ask a planted question, partly "to also promote us getting some short 15 second clips". The message's author and the host's name are not in the record. A planted question is optional and the CC15 host is unknown. ASK: Vardan or Sai Kiran who the host is and who writes the questions.

Two consequences:
- The answer has to be right and short, because it may be cut into a clip.
- The answer has to make sense on its own, so its first clause names the subject.

## The five parts
| Part | What it is | Length |
|---|---|---|
| Fifteen-second answer | The answer, yes or no first, in complete sentences | About 35 words. At 140 words a minute that is 15 seconds |
| Second beat | The limit that makes the answer true | One or two sentences |
| The trap | The sentence a fast answer invites and the source does not support | One line, for the operator only |
| Honest fallback | What to say when the question goes beyond what is confirmed | One sentence |
| Source | The line in the note, post or code that backs each part | A reference |

The fifteen-second answer and the second beat go into the bracketed cue in the notes, where the presenter can read them off the screen. The trap, the fallback and the source live in the preparation, for the operator to read before the call.

## The fee delegation example (CC14, slide 2)
The host's question, as pasted: "If I'm completely new to MOI and I have zero KMOI, an application can essentially handle that fuel requirement for me?"

| Part | Text |
|---|---|
| Fifteen-second answer (31 words) | "Yes. You sign the interaction, the app's account signs alongside it and pays the fuel, so you can turn up with an empty wallet and your first action still goes through." |
| Second beat | "It signs each one separately, so there is no standing allowance, and it only ever covers fuel." The slide 2 script adds: if the user is sending value, they still fund that part themselves. The payer also pays when the interaction fails, which the release post states |
| The trap | Do not say the app pays for you without qualification. Fee delegation covers fuel and nothing else |
| Honest fallback | A suggested wording, because the CC14 line was not saved: "That goes beyond what I have confirmed, so I will check it with the protocol team and put the answer in the dev chat." It matches the close of the slide 3 script |
| Source | The release note: "An interaction can now specify a separate fee payer. The fee payer also signs the interaction and pays the fuel cost instead of the sender." The release post: the payer signs each interaction one at a time, covers only the fuel, and pays even when the interaction fails |

The cue as it stands in the CC14 notes, in the bracketed form:
`[If the host asks the zero-KMOI question here: yes. You sign the interaction, the app's account signs alongside it and pays the fuel, so you can turn up with an empty wallet and your first action still goes through. It signs each one separately, so there is no standing allowance, and it only ever covers fuel.]`

The cue carries the answer and the second beat. The trap and the fallback were kept out of it.

## Open edge of this answer
"Your first action still goes through" assumes nothing else stands between a brand-new participant and its first interaction. The record does not say whether a new participant needs to be created, registered or activated first, or whether that step costs fuel. If the host asks a follow-up on it, use the fallback. ASK: Gokul, before the call.

## Method for a new planted question
1. Get the question word for word, in writing, from the host. Ask which slide it will follow.
2. Find the claim in the release note, then the post, then source. Write the line you found.
3. Write the answer. Yes or no first, in complete sentences, around 35 words, with the subject in the first clause so the clip stands alone.
4. Write the second beat: the limit or scope that keeps the answer true.
5. Find the trap. Look in your own answer for a universal: everything, nobody, always, free, any. Each one needs a source. Delete it or add its limit.
6. Write the fallback. It says what you will do next and by when, and it promises nothing the team has not agreed.
7. Put the answer in a bracketed cue at the slide where the question lands. Put the cue in `SCRIPT.md`, then sync it into `NOTES` with `python3 "$SKILLS/moi-webinar/deck/scripts/sync-notes.py" community-call-<N>/deck/index.html community-call-<N>/SCRIPT.md --confirm` (a dry run until you add `--confirm`), so deck check h passes.
8. Read it aloud once with a timer. If it runs past 15 seconds, cut words.
9. Tell the human the preparation, not only the cue.

## After the question is asked
- Note whether it was asked and whether the host cut a clip. ASK: the host for both. As of 2026-10-02 neither is on record for CC14.
- Log every audience question for the Q&A follow-up. The January 2026 KRA document asks for Q&A and follow-ups logged with owners within 48 hours.

## Not yet known
- Whether the planted question was asked live at CC14, and whether a clip exists. ASK: the host.
- Who edits and posts the clips. See `after-the-call.md`.
- The answer to the new-participant question above. ASK: Gokul.
