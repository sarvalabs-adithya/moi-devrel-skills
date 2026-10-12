# Dev Webinars

**Status: active.** Nine sessions so far; the next one is not scheduled.

The MOI Builders sessions: a live session where we build one project on MOI in front of developers. DevRel owns the session end to end. Vardan provides the Google Meet link.

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Project to build | DevRel, with Rahul | Finalized with Rahul 9 days before the session |
| Slide deck | DevRel | Built with the deck branch of the moi-webinar skill, in our branding |
| Luma page | DevRel | Created on the Monday of the session week, with the Meet link |
| Pre session posts | DevRel | X and LinkedIn, scheduled on Buffer after consulting marketing (see Posting with Buffer below) |
| Session bounty | DevRel | Created on the Points site admin page, no code change (PR #22 on the Points repo, once merged). See POINTS-PROGRAM.md. Until then, proofs came in through a Google Form per session (Builders II, III, IV and VII), checked by hand; the responses sheet "MOI Builders II - Native Assets (Responses)" and the forms are on the adithya@moinetwork.io Drive. Who awarded the points for those: confirm |
| Google Meet link | Vardan | |
| Post session blog | DevRel | Written with the moi-blog skill and published on the website repo. See BLOG.md |
| Codebase | DevRel | https://github.com/moi-foundation/MOI-Webinars, one folder per session: the README with the steps, the code, and the session notes. session-8-policies is the fullest example (README, LUMA.md, RUNBOOK.md, GAMEDAY.md, NOTES.md, BLOG.md) |

## Process

**9 days before**

- Meet with Rahul and finalize the project idea.
- Pick the date. **It must not clash with Game Night or the Community Call.** Check the Luma calendar before fixing it.

**Monday of the session week**

- Get the Google Meet link from Vardan.
- Create the Luma page.
- Schedule a LinkedIn post and an X post for the same day, with the Luma link.

**From 9 days to 2 days before**

- Build the project and test it on devnet.
- Plan the lesson: what the session teaches, in what order.
- Build the deck (the deck branch of the moi-webinar skill).
- Set the session bounty on the Points admin page (POINTS-PROGRAM.md, "Running a webinar bounty").

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

- Write the post session blog and publish it (BLOG.md).
- Push the session's code to the repo.

**Posting with Buffer**

Every pre session post goes out through Buffer, from the X and LinkedIn channels in the MOI organisation. Chandra owns the organisation. Marketing owns what goes out on the company channels, so only use Buffer after consulting the marketing team.

- Ask Chandra for a Buffer API key once. Only the owner can create one.
- Put it in a file called .env at the root of your clone of https://github.com/moi-foundation/MOI-Webinars, as BUFFER_API_KEY=<the key>. Never commit it and never paste it in chat.
- The script is scripts/buffer.mjs. It ships inside the moi-webinar skill (`$SKILLS/moi-webinar/scripts/buffer.mjs`, with the .env at the skill root) and the same file is in this repo on the branch claude/agent-payments-simple until it is merged. Check it works: `node scripts/buffer.mjs channels` lists the X and LinkedIn channels and their ids.
- Draft a post: `node scripts/buffer.mjs post --file <post.txt> --channel <id> --draft`. Without --confirm it only prints what it would do; add --confirm to send. Without --draft a scheduled post publishes by itself, so use --draft unless the exact time matters. A time for --at must end in Z (UTC).
- The moi-webinar skill drafts the four posts and drives this script after you approve each one.

## Announcement schedule

| When | What |
|---|---|
| Monday of the session week, the day the Luma page is created | LinkedIn and X post, with the Luma link |
| 2 days before | LinkedIn and X post |
| 1 day before | LinkedIn and X post |
| 1 hour before | LinkedIn and X post |

## Claude skill

The **moi-webinar** skill covers the session: lesson planning, the Luma text, the pre session posts and the day itself. The deck is built with its deck branch, and the post session blog with the **moi-blog** skill. Say what you need in plain words: Claude loads them on phrases like "builders session", "make the deck" or "write the blog".

| When | What to tell Claude | What the skill does |
|---|---|---|
| A week before | "Help me plan a Builders session on ..." | Proposes what to build and the order to teach it in. |
| Monday of the session week | "Write the Luma page." | Drafts the page text, with the time converted for each region. |
| Monday of the session week | "Draft the four posts and schedule them." | Drafts the X and LinkedIn posts for the four slots. Schedules them on Buffer, through the script above, only after I approve. |
| Building | "Build the deck." | Makes the deck in our branding, runs the checker and exports the PDF. |
| 1 day before | "Run the session check." | Checks the project's setup and that devnet is reachable. |
| After the session | "Draft the post session blog." | Writes the post from the session's code and notes, ready for the website. |

What the skills never do without a yes from DevRel: schedule or post anything, publish the blog, or push code (the webinars repo is public).

## Open items

- Finalize the existing bounty list and the bounty system on the Points Program.
- Make the session bounty extensible: whoever runs a webinar creates its bounty on the Points site themselves, without a code change. Built, in sarvalabs/moi-project PR #22 (open since 8 October) and the rule-engine branch on top of it. Once that ships, add the bounty flow to the moi-webinar skill: create, test, open, review, close.
