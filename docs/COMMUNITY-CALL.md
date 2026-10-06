# Community Call

The monthly public call where MOI shows what shipped and what the team did. Calls usually happen on a Friday. I own the deck and the protocol and DevRel segments. Vardan owns the event.

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Slide deck | Me | Built with the moi-deck skill, in our branding |
| Luma page | Vardan | Must contain the agenda, the date and the Riverside link |
| Riverside room | Vardan | Every speaker is invited 2 days before the call |
| Announcement posts and shorts | Vardan | Schedule below |
| Host | Ruta | |

Luma already holds two large mailing lists: a developer list that Piyush provided and a general list. Both are invited to every community call.

What the deck needs, and by when:

| Input | From | Due |
|---|---|---|
| Protocol updates | Protocol team | Friday of the week before |
| DevRel updates | Me | Friday of the week before |
| Marketing updates | Marketing team (Sai Kiran) | Friday of the week before |
| Partnerships updates | Piyush | Friday of the week before |
| Product updates (not every call) | Pratik | Friday of the week before |
| Guest speaker | Discuss on cadence call | Tuesday before the call |

## Process

**Wednesday of the week before (9 days before)**

- A rough agenda is ready.
- The Luma page and the Riverside link are ready.
- The first announcement goes out, with the Luma link.

**Friday of the week before (7 days before)**

- All updates for the deck are in: protocol, DevRel, marketing, partnerships, and product when there is one.
- The only thing still open is the guest speaker.
- Keep the release note exactly as the protocol team sent it.
- Write every figure down with its source and date before it goes on a slide.
- Plan the slides: one idea per slide, the developer update in one or two slides.
- Build the deck (moi-deck skill).
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

The deck is built with the **moi-deck** skill. The rest of the call (inputs, numbers, the release check, the recording description) is the community call guide in the **moi-webinar** skill. Say what you need in plain words: Claude loads them on phrases like "community call" or "make the deck".

| When | What to tell Claude | What the skill does |
|---|---|---|
| Asking for updates | "Draft the messages asking each owner for their update by Friday." | Drafts one message per owner. I send them; Claude never does. |
| Friday, updates in | "Here are the updates. Start the numbers ledger and plan the slides." | Records each figure with its source and date, flags anything unconfirmed, and proposes the slide order. |
| Building | "Build the deck." | Makes the deck in our branding, runs the checker and exports the PDF. The checker catches faults the PDF hides. |
| Release slides | "Check the release slides against the note." | Compares every line with the release note. |
| Tuesday, deck finished | "Draft the YouTube description." | Builds it from the slide titles and the links in the deck. |
| Thursday | "Ruta may ask this: ..." | Gives a short answer, a follow-up line and what not to say. |
| Day of the call | "Do the day-of check." | Sweeps the deck for stale wording and confirms the PDF matches. |

What the skill never does without my yes: send a message, post anything, upload a file, or push the call folder (the webinars repo is public).

## Open items

- Several figures on the September deck were never confirmed. Check them before reusing them.
- No recording description exists for the September call.
- The skills are not in a repo yet.
