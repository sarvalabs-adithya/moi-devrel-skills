# Community Call

**Status: active.** Monthly, on a Friday. The next call is CC15 (community call 15), expected in the last week of October 2026. The date is not set yet: ask Vardan.

Video: https://drive.google.com/file/d/14SSJ1bCHjiOu4d_J1_UDcsk3VNQZVkKP/view (the moi-webinar skill, deck branch, recorded 9 October 2026).

Marketing: How it works, Variables, Announcement schedule (inside Process), Open items. Developers: Process, Claude skill.

The monthly public call where MOI shows what shipped and what the team did. DevRel builds the deck and the DevRel segment. The Protocol team (Rahul) supplies the content of the protocol segment. Vardan owns the event.

## How it works

### Where things live

- Decks: the public repo moi-foundation/MOI-Webinars, one folder per call, with the deck in community-call-N/deck/ for calls 2 to 14. Each deck folder holds the PDF; from call 14 on, the HTML source is there too. Call 1 has no deck on file, and call 3 was the beta mainnet launch. The decks were merged in PR #2 on 13 October 2026.
- Recordings: every call is on the MOI YouTube channel, in one playlist: https://www.youtube.com/playlist?list=PL4-oiZj2acUPhBkDGm-8ue9jIVxh-NXvs. Past recordings show how a call runs and are the reference for the shorts.
- Logins: Luma, Riverside and YouTube are shared accounts held by Vardan.

### What the deck needs

The inputs, and by when:

| Input | From | Due |
|---|---|---|
| Protocol updates | Protocol team (Rahul) | Friday of the week before |
| DevRel updates | DevRel | Friday of the week before |
| Marketing updates | Marketing team (Sai Kiran) | Friday of the week before |
| Partnerships updates | Piyush | Friday of the week before |
| Product updates (not every call) | Pratik | Friday of the week before |
| Guest speaker | Discuss on the weekly marketing sync (confirm the name; earlier notes called it the cadence call) | Tuesday before the call |

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Slide deck | DevRel | Built with the deck branch of the moi-webinar skill, in MOI branding |
| **Luma** page (the event page and sign-up service) | Vardan | For community calls. It must hold the agenda, the date and the Riverside link. Builders sessions are different: DevRel owns their Luma page (DEV-WEBINARS.md) |
| **Riverside** room (the studio the speakers join) | Vardan | Every speaker is invited 2 days before the call |
| Announcement posts and **shorts** (short clips cut from the recording) | Vardan | Schedule in Process, under Announcement schedule |
| Host | Ruta | |

Luma already holds two large mailing lists: a developer list that Piyush provided and a general list. Both are invited to every community call.

## Env vars

None. The call has no app and no variables. Luma, Riverside and YouTube are shared logins held by Vardan, not variables (ENV-VARS.md lists the other consoles).

## Process

**Wednesday of the week before (9 days before)**

- Have a rough agenda ready.
- Have the Luma page and the Riverside link ready.
- Send the first announcement, with the Luma link.

**Friday of the week before (7 days before)**

- All updates for the deck are in: protocol, DevRel, marketing, partnerships, and product when there is one. Only the guest speaker is still open.
- Keep the release note exactly as the protocol team sent it.
- Write every figure down with its source and date before it goes on a slide. That sheet is the **numbers ledger**.
- Plan the slides: one idea per slide, and the developer update in one or two slides.
- Build the deck (the deck branch of the moi-webinar skill).
- Check the release slides against the release note.

**Monday of the call week (4 days before)**

- Send the second post.
- Invite both Luma mailing lists.

**Tuesday (3 days before)**

- Make the guest speaker's details final.
- Finish the deck.
- If the deck mentions an app or public page, such as the blog or the Launchpad, put its link in both the Luma page and the Riverside description.
- Write the YouTube description from the agenda, with the same links.

**Wednesday (2 days before)**

- Invite all speakers to Riverside.
- Send the third post.

**Thursday (1 day before)**

- Send a Luma announcement to everyone who signed up, 24 hours before the call.
- Ask the host (Ruta) whether a question is planned, and prepare a short answer.

**Friday, the day of the call**

- One hour before: send the last post and a second Luma announcement to everyone who signed up.
- Re-read the deck for anything that went stale, such as "last Friday" or old counts.
- Present from the deck. Keep the PDF open as a fallback.

**After the call**

- Send the post call tweets and the shorts.
- Note the questions the audience asked and who owes an answer.

### Announcement schedule

| When | What |
|---|---|
| Wednesday, 9 days before | First post, with the Luma link |
| Monday, 4 days before | Post, and both Luma mailing lists are invited |
| Wednesday, 2 days before | Post |
| Thursday, 24 hours before | Luma announcement to everyone signed up |
| Friday, 1 hour before | Post, and a Luma announcement to everyone signed up |

## Claude skill

The deck is built with the deck branch of the **moi-webinar** skill. The rest of the call (inputs, numbers, the release check, the recording description) is the community call guide in the same skill. Say what you need in plain words: Claude loads the skill on phrases like "community call" or "make the deck".

| When | What to tell Claude | What the skill does |
|---|---|---|
| Friday, updates in | "Here are the updates. Start the numbers ledger and plan the slides." | Records each figure with its source and date, flags anything unconfirmed, and proposes the slide order. |
| Building | "Build the deck." | Makes the deck in MOI branding, runs the checker and exports the PDF. The checker catches faults the PDF hides. |
| Release slides | "Check the release slides against the note." | Compares every line with the release note. |
| Tuesday, deck finished | "Draft the YouTube description." | Builds it from the slide titles and the links in the deck. |
| Thursday | "Ruta may ask this: ..." | Gives a short answer, a follow-up line and what not to say. |
| Day of the call | "Do the day-of check." | Sweeps the deck for stale wording and confirms the PDF matches. |

Without a yes from DevRel, the skill never sends a message, posts anything, uploads a file, or pushes the call folder (the webinars repo is public).

## Open items

- CC15 has no date. Ask Vardan; it is expected in the last week of October 2026.
- Luma, Riverside and YouTube are shared logins held by Vardan. The next DevRel needs access to all three before the first call.
- The guest speaker is agreed in a regular meeting, called the cadence call in the earlier notes. Confirm its name and who runs it.
- Call 1 has no deck on file. Ask Vardan whether one exists.
