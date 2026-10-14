# Input request messages

Drafts only. The human reads each one, edits it and sends it. Claude never sends, posts or schedules a message. Replace every `<...>` before sending. Facts inside the drafts are as of 2026-10-02: check them before sending.

Style, from how past messages to teammates worked: short, human and specific. One task per message. Say what you need, why, and by when. No labels such as "Owner:", no em dashes, no long preamble. Channels are suggestions, taken from `moi-devrel/references/people-and-teams.md`. Where the channel is not on record the line says ASK. No response time is on record for anyone, so every message names the date you need an answer by.

When a reply arrives, put every figure in the numbers ledger before it goes near a slide. Log who sent it and the date.

## 1. Vardan: date, platform, host
Channel: Slack. Whether to use a direct message or a channel is not recorded; a direct message to Vardan is the safe default.

> Hi Vardan, I am picking up the deck and the line-up for Community Call <N>. The planning sheet has <DATE> as the expected date and <RESERVE DATE> as the reserve. Can you confirm which one we are using, the start time, how long the call runs, and which platform and link? Also, who is hosting this time? I would like to settle all of that by <DAY> so the segments can be agreed.

Use the reply to: confirm the date with the manager, fill the header of `SCRIPT.md`, and tell the segment owners.

## 2. The call's manager, taken to be Rahul: segments and sign-off
Channel: Discord or a call, as `moi-devrel/references/people-and-teams.md` lists for Rahul.

> Hi Rahul, for Community Call <N> I am planning this order: protocol, DevRel, <marketing blocks>, what is next, close. Is there a product or research slot this time? Is the rehearsal on <DAY>? Would you like to review the deck before the call, and by when?

Use the reply to: settle the segment order, the rehearsal day and whether anything stays off. Ask separately whether the "what stays off a public call" pattern in `references/slide-plan.md` is a rule.

## 3. Protocol team: the release note
Channel: Discord release log, or a direct message to Gokul. The handover note names the protocol team (Rahul) as the source of the protocol update; ASK: Rahul who sends the release note.

> Hi <NAME>, for Community Call <N> on <DATE> I need the release note for <VERSION> exactly as the protocol team sent it, without restructuring. Could you also confirm: the exact release moment in UTC, the SDK versions including any release candidate suffix, whether any point release or other package shipped this month, and whether devnet is running the release now? I would like it by <DAY>.

Use the reply to: save the note unedited next to the deck, then run `references/release-slide-checks.md`.

## 4. Sai Kiran: visibility numbers
Channel: Slack. ASK: Sai Kiran which channel.

> Hi Sai Kiran, for Community Call <N> can you send this month's AI-visibility report and the dashboard screenshots, with the date the data covers? I need visibility, citations, mentions, the per-engine numbers and the coverage. Is the query set still 47 queries across five engines, and which engine is the fifth? Last month's coverage figure of 221 of 226 and the engine movements were never reconfirmed, so a current figure would help. By <DAY> if you can.

Use the reply to: add ledger rows with source and date, and retire the figures they replace.

## 5. Sai Kiran: community and events
Channel: Slack.

> Hi Sai Kiran, for Community Call <N> I need the community numbers: new Discord joins and active members, with the period they cover, plus the latest Game Night with its date, run number and attendance, and Pip. Could you confirm they are the latest for the month? For events I need the name, dates and what we did there, and any photos we have the right to show. Who is presenting the marketing slides? By <DAY>.

Use the reply to: fill the community and events rows of the ledger, and ask each marketing presenter whether they want notes.

## 6. The host: the planted question and clips
Channel: Slack. The host is Ruta (handover note); confirm each call with Vardan.

> Hi <NAME>, will you plant a question this time? If so, can you send me the exact wording and tell me which part of the call it follows? I will prepare a short answer so it works as a 15 second clip. Who cuts and posts the clips, and where?

Use the reply to: run the method in `references/host-qa-prep.md`.

## 7. A guest, if there is one
Channel: whoever invited the guest. The guest is agreed on the weekly marketing sync (handover note). ASK: Vardan.

> Hi <NAME>, we are looking forward to having you on Community Call <N> on <DATE>. For your slide, could you send these by <DATE>?
> 1. A headshot: square, at least 1200 by 1200 pixels, face centred, head and shoulders.
> 2. Your company logo: SVG, or a PNG with a transparent background, at least 600 by 200 pixels (a square mark is fine at 400 by 400). The version for a light background, please.
> 3. Your name, your role and your company, exactly as you want them written.
> 4. One line on what you will talk about.
> Is it all right for your photo to appear in the recording and in the slides we share afterwards?

Never write a title the guest has not given. Save the files as `deck/assets/guest/headshot.jpg` and `deck/assets/guest/logo.svg` (`moi-webinar/deck/references/guest-slide.md`).

## 8. Vardan: access and what the last calls left behind
Channel: Slack. Send it once, before the first call, then fold it into message 1 or 9 if you prefer.

> Hi Vardan, I am taking over the deck and the line-up for the community calls. Could you give me access to Luma, Riverside and the MOI YouTube channel before Community Call <N>, or tell me who can? Which Slack channel do the call inputs arrive in? Was the planted question at call 14 asked, and were the shorts cut? Anything else from the last call I should know?

Use the reply to: fill the "Not yet known" lists in `references/`. The 4 October dependency list was removed; the product docs replace it, and the call's handover note is `project-handover-docs/COMMUNITY-CALL.md`; nobody needs to be asked for those.

## 9. Vardan: the Luma page, the Riverside room, the posts and the speaker list
Channel: Slack. Send at T-9, with the run sheet's dates filled in.

> Hi Vardan, here is the agenda for Community Call <N> on <DATE> at <TIME> IST: <one line per segment, with the presenter><, and our guest <NAME> from <COMPANY> if confirmed>. Could you send me the Luma link and the Riverside link once they are up? I can draft the Luma text, the four posts and the two Luma announcements if that helps; tell me if you would rather write them. For the Riverside invites on <T-2 DATE>, the speakers are <NAMES>. Do you need their emails from me?

Use the reply to: put the Luma and Riverside links in `community-call-<N>/LUMA.md` and `SOCIAL.md`, and mark the Vardan rows of the run sheet as his or as drafts for him.
