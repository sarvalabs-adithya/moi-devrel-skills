# Input request messages

Drafts only. The human reads each one, edits it and sends it. Claude never sends, posts or schedules a message. Replace every `<...>` before sending. Facts inside the drafts are as of 2026-10-02: check them before sending.

Style, from how past messages to teammates worked: short, human and specific. One task per message. Say what you need, why, and by when. No labels such as "Owner:", no em dashes, no long preamble. Channels are suggestions, taken from `moi-devrel/references/people-and-teams.md`. Where the channel is not on record the line says ASK. No response time is on record for anyone, so every message names the date you need an answer by.

When a reply arrives, put every figure in the numbers ledger before it goes near a slide. Log who sent it and the date.

## 1. Vardan: date, platform, host
Channel: Slack. Whether to use a direct message or a channel is not on record. ASK: Adithya.

> Hi Vardan, I am picking up the deck and the line-up for Community Call <N>. The planning sheet has <DATE> as the expected date and <RESERVE DATE> as the reserve. Can you confirm which one we are using, the start time, how long the call runs, and which platform and link? Also, who is hosting this time? I would like to settle all of that by <DAY> so the segments can be agreed.

Use the reply to: confirm the date with the manager, fill the header of `SCRIPT.md`, and tell the segment owners.

## 2. The call's manager, taken to be Rahul: segments and sign-off
Channel: Discord or a call, as `moi-devrel/references/people-and-teams.md` lists for Rahul.

> Hi Rahul, for Community Call <N> I am planning this order: protocol, DevRel, <marketing blocks>, what is next, close. Is there a product or research slot this time? Is the rehearsal on <DAY>? Would you like to review the deck before the call, and by when?

Use the reply to: settle the segment order, the rehearsal day and whether anything stays off. Ask separately whether the "what stays off a public call" pattern in `references/slide-plan.md` is a rule.

## 3. Protocol team: the release note
Channel: Discord release log, or a direct message to Gokul. ASK: Rahul who is the contact for release notes.

> Hi <NAME>, for Community Call <N> on <DATE> I need the release note for <VERSION> exactly as the protocol team sent it, without restructuring. Could you also confirm: the exact release moment in UTC, the SDK versions including any release candidate suffix, whether any point release or other package shipped this month, and whether devnet is running the release now? I would like it by <DAY>.

Use the reply to: save the note unedited next to the deck, then run `references/release-slide-checks.md`.

## 4. Sai Kiran: visibility numbers
Channel: Slack. ASK: which channel.

> Hi Sai Kiran, for Community Call <N> can you send this month's AI-visibility report and the dashboard screenshots, with the date the data covers? I need visibility, citations, mentions, the per-engine numbers and the coverage. Is the query set still 47 queries across five engines, and which engine is the fifth? Last month's coverage figure of 221 of 226 and the engine movements were never reconfirmed, so a current figure would help. By <DAY> if you can.

Use the reply to: add ledger rows with source and date, and retire the figures they replace.

## 5. Sai Kiran: community and events
Channel: Slack.

> Hi Sai Kiran, for Community Call <N> I need the community numbers: new Discord joins and active members, with the period they cover, plus the latest Game Night with its date, run number and attendance, and Pip. Could you confirm they are the latest for the month? For events I need the name, dates and what we did there, and any photos we have the right to show. Who is presenting the marketing slides? By <DAY>.

Use the reply to: fill the community and events rows of the ledger, and ask each marketing presenter whether they want notes.

## 6. The host: the planted question and clips
Channel: Slack. ASK: Vardan or Sai Kiran who the host is.

> Hi <NAME>, will you plant a question this time? If so, can you send me the exact wording and tell me which part of the call it follows? I will prepare a short answer so it works as a 15 second clip. Who cuts and posts the clips, and where?

Use the reply to: run the method in `references/host-qa-prep.md`.

## 7. A guest, if there is one
Channel: whoever invited the guest. ASK: Vardan.

> Hi <NAME>, we are looking forward to having you on Community Call <N> on <DATE>. For the slide could you send your name and title the way you want them written, a portrait and your company logo? A short line on what you will talk about would also help.

Never write a title the guest has not given.

## 8. The previous operator: where things live
Channel: `#dev-chat`, where `moi-devrel/references/people-and-teams.md` places him. If he is not there, ASK: Rahul how to reach him.

> Hi Adithya, I am running Community Call <N>. Could you send me a copy of DEPENDENCIES.md, and of the call 14 folder and the protocol-release-0.13.0 folder, which I understand are only on your machine? Where do the Community Call 13 and 14 decks live now, beyond your machine? Which Slack channel do the call inputs arrive in, who holds the Scribble login, and was the planted question at 14 asked and the clip cut? Anything else from the last call I should know?

Use the reply to: fill the "Not yet known" lists in `references/`.
