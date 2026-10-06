# Corrections: when a posted statement turns out wrong

Facts are as of 2026-10-02. **One correction case is on record**, the release time of 2026-09-10. Steps 1 to 9 below are built from that case and are marked as this library's design where the record is silent. `ASK:` is defined in `moi-devrel/SKILL.md`. `SKILLS` is set as in `../GUIDE.md`. Back to `../GUIDE.md`.

## The recorded case
1. The note said "scheduled for today at 12:00 AM UTC". The pack was scheduled the same day, about 08:45 UTC (`timing.md`, inferred from the order of the previous operator's requests). The text was read as noon. <!-- slop-lint:ignore -->
2. Two wrong scheduled posts were deleted by hand in Buffer. `buffer.mjs` has no delete command.
3. A correction reply for X was drafted in `social/x-correction-reply.txt`. Its text, in full: "Correction: the moipod v0.13.0 network update is scheduled for 00:00 UTC on 11 September, not 12:00 UTC today."
4. A template of it is `../templates/social/x-correction-reply.txt`.
5. Not recorded: whether the reply was ever posted, on which account, and whether LinkedIn or Discord needed one. ASK: Adithya.

## Kinds of wrong statement, and what is on record
| Kind | What is on record |
|---|---|
| A wrong time in a scheduled post | The case above. The cost was two deletions by hand and a correction draft |
| A wrong claim in the release post, caught before it published | The September post had five: the MAS0 versus MASN class for the KMOI code sample, failed interactions still charge the payer, an access-policies link that returned 404, a paragraph that contradicted the participant-list rule, and a recap bullet that left out the notary exception. All were fixed before the merge: they are listed in the message of the squashed merge commit 280ffb2 in `sarvalabs/MOI-Website` |
| Retired wording in a published post | As of 2026-10-02 the live September post still has "Voyage devnet" twice, "a native asset standard made for KMOI alone" and "Participant: an account on MOI" (read from the live page that day). Whether to amend a published post, and how, is not recorded. ASK: Rahul <!-- slop-lint:ignore --> |

## Steps
1. **Stop.** Tell the operator which statements are wrong, where each was posted, and whether each is still scheduled or already published.
2. **Delete nothing yourself.** A scheduled Buffer post is deleted by hand in Buffer. A published post is the operator's to delete or leave. This library's design: whether to delete a published post is not in the record, so ask Rahul.
3. **Get the right fact in writing** from the protocol team, with a date and a 24-hour UTC time. If the claim was "live", read the node again (`moi-devrel/references/devnet.md`, "Before you say live").
4. **Draft the correction.** Copy the template: `cp "$SKILLS/moi-blog/release-pack/templates/social/x-correction-reply.txt" protocol-release-<version>/social/x-correction-reply.txt`. One sentence. It says "Correction:", gives the right fact with its date and 24-hour UTC time, then names the wrong one with its date. The template says "is scheduled for", which is true only before the moment: after it, say what the protocol team confirmed and do not write "live" without a node read. The recorded reply says "today", which goes stale, so write the date. The v0.13.0 reply is 110 characters.
5. **Check it:** `python3 "$SKILLS/moi-blog/release-pack/scripts/thread-lint.py" protocol-release-<version>/social/x-correction-reply.txt`.
6. **The operator chooses the channels.** The recorded draft is a reply under the wrong X post. Whether a wrong LinkedIn or Discord post gets a correction, an edit or a deletion is not recorded. ASK: Rahul.
7. **Gate.** A reply, an edit or a deletion on any live channel needs an explicit yes that names the text and the channel.
8. **Fix the sources.** Correct the pack files and the post draft. Log each change under "Differences from the note" in `SOCIAL.md`. Run the lints and the ledger check again.
9. **Record it.** Add a row under "Corrections" in `SOCIAL.md`: date, what was wrong, channel, what was done. Keep the wrong text there. Do not rewrite the files to hide it.

## What prevents the next one
- Write the moment as a date and 00:00-style UTC from the first draft (`timing.md`).
- Run `thread-lint.py`. It stops `12:00 AM`, "today" beside a time, and a missing scheme or a placeholder.
- Use drafts, so a person reads the post in Buffer before it publishes. A scheduled post goes out with nobody reviewing it.
- Keep one copy of each text. The v0.13.0 folder held the same sentences in four places and they disagreed (`traps.md`).

## Not yet known
- Whether the v0.13.0 correction reply was posted, and where. ASK: Adithya.
- How a published post is amended after the merge, whether it carries an `updated` date, and who approves. ASK: Rahul.
- Whether the live September post should lose its retired wording. ASK: Rahul.
- Who may delete a published post on each channel. ASK: Rahul.
