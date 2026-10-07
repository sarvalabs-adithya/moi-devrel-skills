# Dev Webinars

**Status: active.** Nine sessions so far; the next one is not scheduled.

The MOI Builders sessions: a live session where we build one project on MOI in front of developers. I own the session end to end. Vardan provides the Google Meet link.

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Project to build | Me, with Rahul | Agreed a week before, final 5 days before |
| Slide deck | Me | Built with the moi-deck skill, in our branding |
| Luma page | Me | Created 5 days before, once the project is final |
| Pre session posts | Me | X and LinkedIn, scheduled on Buffer |
| Session bounty | Me | Runs on the Points Program |
| Google Meet link | Vardan | |
| Post session blog | Me | |
| Codebase | Me | moi-foundation/MOI-Webinars, one folder per session |

## Process

**A week before**

- Meet with Rahul and discuss ideas for a project to build.

**5 days before**

- Finalize the project.
- Get the Google Meet link from Vardan.
- Create the Luma page.
- Schedule a LinkedIn post and an X post for the same day, with the Luma link.

**5 to 2 days before**

- Build the project and test it on devnet.
- Plan the lesson: what the session teaches, in what order.
- Build the deck (moi-deck skill).
- Set the session bounty.

**2 days before**

- A LinkedIn post and an X post go out.

**1 day before**

- A LinkedIn post and an X post go out.
- Run the project once more, start to finish.

**Session day**

- One hour before: a LinkedIn post and an X post go out.
- Run the session on Google Meet.
- Share the bounty at the end.

**After the session**

- Write the post session blog and publish it.
- Push the session's code to the repo.

## Announcement schedule

| When | What |
|---|---|
| 5 days before, the day the Luma page is created | LinkedIn and X post, with the Luma link |
| 2 days before | LinkedIn and X post |
| 1 day before | LinkedIn and X post |
| 1 hour before | LinkedIn and X post |

## Claude skill

The **moi-webinar** skill covers the session: lesson planning, the Luma text, the pre session posts and the day itself. The deck is built with the **moi-deck** skill, and the post session blog with the **moi-blog** skill. Say what you need in plain words: Claude loads them on phrases like "builders session", "make the deck" or "write the blog".

| When | What to tell Claude | What the skill does |
|---|---|---|
| A week before | "Help me plan a Builders session on ..." | Proposes what to build and the order to teach it in. |
| 5 days before | "Write the Luma page." | Drafts the page text, with the time converted for each region. |
| 5 days before | "Draft the four posts and schedule them." | Drafts the X and LinkedIn posts for the four slots. Schedules them on Buffer only after I approve. |
| Building | "Build the deck." | Makes the deck in our branding, runs the checker and exports the PDF. |
| 1 day before | "Run the session check." | Checks the project's setup and that devnet is reachable. |
| After the session | "Draft the post session blog." | Writes the post from the session's code and notes, ready for the website. |

What the skills never do without my yes: schedule or post anything, publish the blog, or push code (the webinars repo is public).

Scheduling on Buffer needs a Buffer API key, set up once by whoever runs the sessions:

1. Ask Chandra, who owns the Buffer organisation, for an API key. Only the owner can create one.
2. Put it in a file called .env at the root of your clone of moi-foundation/MOI-Webinars, as BUFFER_API_KEY=<the key>. Never commit it and never paste it in chat.
3. The script is scripts/buffer.mjs on the branch claude/agent-payments-simple (not main). Run it from the repo root with Node. Check it works: `node scripts/buffer.mjs channels` lists the X and LinkedIn channels and their ids.
4. Draft a post: `node scripts/buffer.mjs post --file <post.txt> --channel <id> --draft`. Without --confirm it only prints what it would do; add --confirm to send. Without --draft a scheduled post publishes by itself, with nobody reviewing it, so use --draft unless the exact time matters. A time for --at must end in Z (UTC).
5. The Claude skill drives the same script after you approve each post.

## Open items

- Finalize the existing bounty list and the bounty system on the Points Program.
- Make the session bounty extensible: whoever runs a webinar should be able to create its bounty on the Points site themselves, without a code change. Today each one needs a developer to add a task and deploy.
