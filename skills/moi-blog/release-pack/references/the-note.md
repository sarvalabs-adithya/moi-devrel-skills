# The release note: receiving it, keeping it, quoting it

The protocol team's note is the one source every other text in the pack leans on. Facts are as of 2026-10-02. `ASK:` is defined in `moi-devrel/SKILL.md`. Back to `../GUIDE.md`.

## How the note arrives
| Release | What is on record |
|---|---|
| v0.13.0, September 2026 | The previous operator pasted the note into chat on 2026-09-10 and asked for X and LinkedIn posts. Who at the protocol team wrote it, and in which channel it was sent, is not recorded |
| v0.12.0, August 2026 | No single note is on record. On 2026-08-14 Rahul asked in Discord for every service owner to post `service:version:<github-link>` (for example `go-moi:v0.12.0`), because marketing builds the release post from that list. Vinay posts engineering release logs in Discord |
- Early warning: a daily upstream watch (03:17 UTC) files "Upstream release: go-moi <tag>" in `sarvalabs/moi-mcp`. The v0.13.0 issue came on 2026-09-10 and the devnet wipe followed, announced for 2026-09-11 (`moi-devrel/references/devnet.md`, reset history).
- Engineering releases seen so far: 2026-08-14, 08-18, 08-25 and 09-10. A release note is on record only for v0.13.0.
- Not recorded: the channel the protocol team uses to send a note, and a named contact besides Gokul. ASK: Rahul.
- If the note comes as a file or a link, downloading it needs a yes. Say its name, source and size first.

## Keep it unedited
Rule: `RELEASE-NOTE.md` holds the note exactly as received and nothing else. No header, no label, no fix.
- Incident: the v0.13.0 file was headed "as sent by the protocol team, unedited". It was not. The note first pasted on 2026-09-10 had an em dash in its title, the sentence "We are rolling out moipod v0.13.0 with several important updates", and separate sentences saying the sender does not pay. The file held the restructured sentences of the X thread. The original text is lost as of 2026-10-02. ASK: Gokul or Rahul whether it is posted anywhere.
- Paste first. Then take the hash: `shasum -a 256 protocol-release-<version>/RELEASE-NOTE.md`. Write it in `SOCIAL.md` with who sent the note, in which channel, and when. A file whose hash no longer matches was edited.
- Never fix the note. A typo, an em dash or a merged sentence is changed in the pack text, and the change is logged under "Differences from the note" in `SOCIAL.md`.
- The note may keep an em dash. `slop-lint.sh` and `thread-lint.py` run on the texts that ship, not on the note.
- If the note arrives in several messages, paste them in order, with a blank line between messages, and say so in `SOCIAL.md`.
- Show the saved file to the operator once, so a person has compared it with what the protocol team sent.

## What the saved copy of the v0.13.0 note contains
Read it in `../examples/v0.13.0/RELEASE-NOTE.md`. That file is the restructured text the pack used, not the note as first pasted (see the incident above), so the list below is what the saved copy holds. The original may have held more.
- A title with the version, and one sentence with the release moment: "scheduled for today at 12:00 AM UTC", with no date. A sentence that the release has breaking changes. <!-- slop-lint:ignore -->
- Four sections: Fee Payer, KMOI Native Asset, Participant List, ANU. The ANU section gives two changed prices: minimum fuel price 1 anu to 50 anu, storage price per byte 1 anu to 1,000,000 anu.
- Action required (check fixed storage funding values), SDK Versions (`js-moi-sdk` 0.9.0-rc2, `js-polo` 0.1.5), and a closing line: update before the network moves.

## What the saved copy leaves out
Each item is visible by reading the saved copy. A pack or a post that states one needs a source and a ledger row.
| Left out | Where the pack got it | Status |
|---|---|---|
| The date of the release moment | The correction reply in the previous operator's pack: 00:00 UTC on 11 September | Not in the note. ASK: Gokul to confirm in writing |
| A link to fuller release notes | The drafts ended in the placeholder `RELEASE_URL` | What it should point to is not recorded. ASK: Gokul or Rahul <!-- slop-lint:ignore --> |
| Whether devnet is wiped | The release post: "Devnet was reset for this release" | The note is silent. See `timing.md` |
| The old and the new KMOI asset id | The release post gives the new id in full and the start of the old one | Post only. Trace to source |
| Any instruction for node operators | Nowhere in the pack | Every action item addresses application developers |
| The go-moi tag, and who wrote the note | Nowhere | The post's PR checklist said the tag is dated 10 September. The author is not recorded. ASK: Rahul |

## Quote it exactly
1. Copy ids, versions and amounts character for character: `0.9.0-rc2`, `js-polo` 0.1.5, "1 KMOI = 1,000,000,000 anu". Keep an `-rc` suffix and add no sentence about what a release candidate is.
2. Keep product names as the note writes them (`moipod` in lower case). The docs prefer MOIPod in prose. Posts quote the note's form.
3. "Do not calculate these conversions manually" is the note's sentence. Quote it. Do no anu arithmetic in the announcement pack. The release post names `parseKmoi` and `formatKmoi` and gives its own worked prices, each with a ledger row.
4. Merge two sentences only when they say the same thing, and log the merge. Add no fact. A sentence that is not in the note needs a source and a ledger row.
5. Replace the note's "today" with the date, and write the time as in `timing.md`. Log that as a difference too.
6. To find what the pack added, run `python3 "$SKILLS/moi-blog/release-pack/scripts/thread-lint.py" protocol-release-<version>/social --note protocol-release-<version>/RELEASE-NOTE.md`. Each `not-in-note` line is a sentence the note does not hold. A channel-native rewrite will have many. That is expected, and each one is checked in the ledger.

## Questions to put to the protocol team with the note
One message, plain, with context. Claude drafts it and the operator sends it. The shape is draft 6 in `moi-devrel/templates/messages.md`, and `python3 "$SKILLS/moi-devrel/scripts/check-message.py" --to protocol <draft>` is the last check on it; how people are reached is in `moi-devrel/references/people-and-teams.md`. The list is inferred from what broke in August and September 2026.
1. What is the release moment, as a date and a 24-hour UTC time?
2. Does the upgrade wipe devnet? If so, will the registry be redeployed, with which id, and when?
3. Do KMOI's asset id, the fuel-price floor, the participant-creation minimum or the RPC path change?
4. What should "full release notes" link to?
5. Who tells DevRel when the network is live?
6. Which call returns the network ID? `net.NetworkID` answered "the method does not exist" on the devnet RPC on 2026-10-02.
Record each answer in `SOCIAL.md` with who gave it and when.

## Not yet known
- How a note reaches DevRel and who writes it. ASK: Rahul.
- Whether a note exists for every release. Only v0.13.0 has one on record. ASK: Rahul.
- What the full-release-notes link is. ASK: Gokul or Rahul.
