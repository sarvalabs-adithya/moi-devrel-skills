# Community Call

**Status: active.** Monthly, on a Friday. The next call is CC15 (community call 15), expected in the last week of October 2026. The date is not set yet: ask Vardan.

Marketing: Variables, Where things live, What the deck needs, Announcement schedule, Open items. Developers: Process, Claude skill.

Video: https://drive.google.com/file/d/14SSJ1bCHjiOu4d_J1_UDcsk3VNQZVkKP/view (the moi-webinar skill, deck branch, recorded 9 October 2026).

The monthly public call where MOI shows what shipped and what the team did. Calls usually happen on a Friday. DevRel builds the deck and the DevRel segment. The content of the protocol segment comes from the Protocol team (Rahul). Vardan owns the event.

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Slide deck | DevRel | Built with the deck branch of the moi-webinar skill, in MOI branding |
| **Luma** page (the event page and sign-up service) | Vardan | For community calls. Must contain the agenda, the date and the Riverside link. Builders sessions are different: DevRel owns their Luma page (DEV-WEBINARS.md) |
| **Riverside** room (the studio the speakers join) | Vardan | Every speaker is invited 2 days before the call |
| Announcement posts and **shorts** (short clips cut from the recording) | Vardan | Schedule below |
| Host | Ruta | |

Luma already holds two large mailing lists: a developer list that Piyush provided and a general list. Both are invited to every community call.

## Where things live

- Decks: the public repo moi-foundation/MOI-Webinars, one folder per call with the deck in community-call-N/deck/, for calls 2 to 14 (the PDF in each deck folder; call 1 has no deck on file; call 3 was the beta mainnet launch). From call 14 on, the HTML source is there too. They were merged in PR #2 on 13 October 2026.
- Recordings: every call is on the MOI YouTube channel, in one playlist: https://www.youtube.com/playlist?list=PL4-oiZj2acUPhBkDGm-8ue9jIVxh-NXvs. Past recordings are the reference for the shorts and for how a call runs.
- Logins: Luma, Riverside and YouTube are shared accounts held by Vardan.

## What the deck needs

The inputs, and by when:

| Input | From | Due |
|---|---|---|
| Protocol updates | Protocol team (Rahul) | Friday of the week before |
| DevRel updates | DevRel | Friday of the week before |
| Marketing updates | Marketing team (Sai Kiran) | Friday of the week before |
| Partnerships updates | Piyush | Friday of the week before |
| Product updates (not every call) | Pratik | Friday of the week before |
| Guest speaker | Discuss on the weekly marketing sync (confirm the name; earlier notes called it the cadence call) | Tuesday before the call |

## Env vars

None. The call has no app and no variables. Luma, Riverside and YouTube are shared logins held by Vardan, not variables (ENV-VARS.md lists the other consoles).

## Process

**Wednesday of the week before (9 days before)**

- A rough agenda is ready.
- The Luma page and the Riverside link are ready.
- The first announcement goes out, with the Luma link.

**Friday of the week before (7 days before)**

- All updates for the deck are in: protocol, DevRel, marketing, partnerships, and product when there is one.
- The only thing still open is the guest speaker.
- Keep the release note exactly as the protocol team sent it.
- Write every figure down with its source and date before it goes on a slide. That sheet is the **numbers ledger**.
- Plan the slides: one idea per slide, the developer update in one or two slides.
- Build the deck (the deck branch of the moi-webinar skill).
- Check the release slides against the release note.

**Monday of the call week (4 days before)**

- The second post goes out.
- Both Luma mailing lists are invited.

**Tuesday (3 days before)**

- The guest speaker's details are final.
- The deck is finished.
- If the deck mentions any app or public page, such as the blog or the Launchpad, its link goes in both the Luma page and the Riverside description.
- Write the YouTube description from the agenda, with the same links.

**Wednesday (2 days before)**

- All speakers are invited to Riverside.
- The third post goes out.

**Thursday (1 day before)**

- A Luma announcement goes to everyone who signed up, 24 hours before the call.
- Ask the host (Ruta) whether a question is planned, and prepare a short answer.

**Friday, the day of the call**

- One hour before: the last post goes out, and a second Luma announcement goes to everyone who signed up.
- Re-read the deck for anything that went stale, such as "last Friday" or old counts.
- Present from the deck. Keep the PDF open as a fallback.

**After the call**

- The post call tweets and the shorts go out.
- Note the questions the audience asked and who owes an answer.

## Announcement schedule

| When | What |
|---|---|
| Wednesday, 9 days before | First post, with the Luma link |
| Monday, 4 days before | Post, and both Luma mailing lists are invited |
| Wednesday, 2 days before | Post |
| Thursday, 24 hours before | Luma announcement to everyone signed up |
| Friday, 1 hour before | Post, and a Luma announcement to everyone signed up |

## Claude skill

The deck is built with the deck branch of the **moi-webinar** skill. The rest of the call (inputs, numbers, the release check, the recording description) is the community call guide in the **moi-webinar** skill. Say what you need in plain words: Claude loads them on phrases like "community call" or "make the deck".

| When | What to tell Claude | What the skill does |
|---|---|---|
| Friday, updates in | "Here are the updates. Start the numbers ledger and plan the slides." | Records each figure with its source and date, flags anything unconfirmed, and proposes the slide order. |
| Building | "Build the deck." | Makes the deck in MOI branding, runs the checker and exports the PDF. The checker catches faults the PDF hides. |
| Release slides | "Check the release slides against the note." | Compares every line with the release note. |
| Tuesday, deck finished | "Draft the YouTube description." | Builds it from the slide titles and the links in the deck. |
| Thursday | "Ruta may ask this: ..." | Gives a short answer, a follow-up line and what not to say. |
| Day of the call | "Do the day-of check." | Sweeps the deck for stale wording and confirms the PDF matches. |

What the skill never does without a yes from DevRel: send a message, post anything, upload a file, or push the call folder (the webinars repo is public).

## Open items

- CC15 has no date. Ask Vardan; it is expected in the last week of October 2026.
- Luma, Riverside and YouTube are shared logins held by Vardan. The next DevRel needs access to all three before the first call.
- The guest speaker is agreed in a regular meeting, called the cadence call in the earlier notes. Confirm its name and who runs it.
- Call 1 has no deck on file. Ask Vardan whether one exists.
