# Dev Webinars

**Status: active.** Nine sessions so far (see Open items). The next one is not scheduled.

Marketing: How it works, Variables, Process (Posting with Buffer, Announcement schedule). Developers: Env vars, Process, Claude skill, Open items.

The MOI Builders sessions are live sessions where DevRel builds one project on MOI in front of developers. DevRel owns each session end to end. Vardan provides the Google Meet link.

## How it works

- **Planning.** DevRel and Rahul finalize the project 9 days before the session. DevRel picks a date that does not clash with Game Night (the community's Friday games night on Discord) or the Community Call.
- **Building.** From 9 days to 2 days before, DevRel builds the project, tests it on **devnet** (MOI's shared test network), plans the lesson, builds the deck and sets the session **bounty** (something attendees do for points).
- **Announcing.** DevRel creates the **Luma** page (the event page and sign-up service) on the Monday of the session week. Four rounds of posts go out, each a LinkedIn post and an X post: on that Monday, 2 days before, 1 day before and 1 hour before. DevRel schedules them on **Buffer** (a post-scheduling service) after consulting marketing.
- **The session.** DevRel runs it on Google Meet and shares the bounty at the end.
- **After.** DevRel writes and publishes the post session blog and pushes the session's code to the MOI-Webinars repo, which has one folder per session.

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Project to build | DevRel, with Rahul | Finalized with Rahul 9 days before the session |
| Slide deck | DevRel | Built with the deck branch of the moi-webinar skill, in MOI branding |
| Luma page | DevRel | For Builders sessions. Created on the Monday of the session week, with the Meet link. Community calls are different: Vardan owns their Luma page (COMMUNITY-CALL.md) |
| Pre session posts | DevRel | X and LinkedIn posts, scheduled on Buffer after consulting marketing. See Posting with Buffer, under Process |
| Session bounty | DevRel | DevRel creates it on the admin page of the **Points site** (points.moi.technology, the MOI Community Points app), with no code change. Bounties went live with PR #22 on sarvalabs/moi-project, merged and deployed on 13 October 2026. A test bounty ran end to end on 14 October 2026: created, opened, answered, awarded, closed. See POINTS-PROGRAM.md. Before that, proofs came in through a Google Form per session (Builders II, III, IV and VII). They were checked by hand, and Adithya awarded those points. The old points are in the Google Sheet "MOI Builders bounties - consolidated" (https://docs.google.com/spreadsheets/d/1r5MRZddaqasygl0Bm5E078EyCmzaZwzJpnhPJUeVvP8), beside the per-session response sheets ("MOI Builders II - Native Assets (Responses)", "MOI Builders IV - Swaps (Responses)"). All of them are in a shared drive, so they stay when Adithya's account goes |
| Google Meet link | Vardan | |
| Post session blog | DevRel | Written with the moi-blog skill and published on the website repo. See BLOG.md |
| Codebase | DevRel | https://github.com/moi-foundation/MOI-Webinars, one folder per session: the README with the steps, the code, and the session notes. Event pages and forms number sessions in Roman numerals, but the folders use plain numbers. Builders II is session-2, III is session-3, IV is session-4, VII is session-7, and VIII is session-8-policies. session-8-policies is the fullest example (README, LUMA.md, RUNBOOK.md, GAMEDAY.md, NOTES.md, BLOG.md). On 14 October 2026 main holds sessions 1 to 7 only. session-8, session-8-policies, session-9 and intro-session are on the branch claude/agent-payments-simple (95 commits ahead of main; see Open items) |

## Env vars

The index across every product, with the consoles and who holds each login, is ENV-VARS.md.

| Variable | What it is | Where the value comes from |
|---|---|---|
| BUFFER_API_KEY | The key for the Buffer script that schedules the session posts. It is not the BUFFER_ACCESS_TOKEN that the blog's announcing workflow uses (BLOG.md): the two keys belong to different tools | Chandra, who owns the Buffer organisation, creates it |

Luma, Google Meet and YouTube are shared logins held by Vardan. They are not variables.

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
- Plan the lesson: what the session teaches, and in what order.
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

Every pre session post goes out through Buffer, from the X and LinkedIn channels in the MOI organisation. Chandra owns the organisation. Marketing owns what goes out on the company channels, so consult the marketing team before using Buffer.

- Ask Chandra for a Buffer API key once. Only the owner can create one.
- Put it in a file called .env at the root of the moi-webinar skill folder, as BUFFER_API_KEY=<the key>. Never commit it and never paste it in chat.
- The script is scripts/buffer.mjs inside the moi-webinar skill: skills/moi/moi-webinar/scripts/buffer.mjs in the handover repo (sarvalabs/moi-devrel-skills), or `$SKILLS/moi-webinar/scripts/buffer.mjs` once installed. Check that it works from the skill folder: `node scripts/buffer.mjs channels` lists the X and LinkedIn channels and their ids.
- Draft a post: `node scripts/buffer.mjs post --file <post.txt> --channel <id> --draft`. Without --confirm the script only prints what it would do. Add --confirm to send. Without --draft, a scheduled post publishes by itself, so use --draft unless the exact time matters. A time for --at must end in Z (UTC).
- The moi-webinar skill drafts the four posts and drives this script after you approve each one.

**Announcement schedule**

| When | What |
|---|---|
| Monday of the session week, the day the Luma page is created | LinkedIn and X post, with the Luma link |
| 2 days before | LinkedIn and X post |
| 1 day before | LinkedIn and X post |
| 1 hour before | LinkedIn and X post |

## Claude skill

The **moi-webinar** skill covers the session: lesson planning, the Luma text, the pre session posts and the day itself. Its deck branch builds the deck. The **moi-blog** skill writes the post session blog. Say what you need in plain words: Claude loads the skills on phrases like "builders session", "make the deck" or "write the blog".

| When | What to tell Claude | What the skill does |
|---|---|---|
| A week before | "Help me plan a Builders session on ..." | Proposes what to build and the order to teach it in. |
| Monday of the session week | "Write the Luma page." | Drafts the page text, with the time converted for each region. |
| Monday of the session week | "Draft the four posts and schedule them." | Drafts the X and LinkedIn posts for the four slots. Schedules them on Buffer, through the script above, only after DevRel approves. |
| Building | "Build the deck." | Makes the deck in MOI branding, runs the checker and exports the PDF. |
| 1 day before | "Run the session check." | Checks the project's setup and that devnet is reachable. |
| After the session | "Draft the post session blog." | Writes the post from the session's code and notes, ready for the website. |

Without a yes from DevRel, the skills never schedule or post anything, publish the blog, or push code (the webinars repo is public).

## Open items

- Bounties are live (PR #22, 13 October 2026). Whoever runs a webinar creates its bounty on the Points site, with no code change. A bounty is a small form that the host designs and grades by hand. Its field types are an **interaction hash** (the identifier of a signed request on the chain, shown in the explorer), a link, and number or text fields, each worth its own points. The moi-webinar skill walks the flow (create, test, grade, close) in references/after-the-session.md.
- Merge the session work into main: sessions 8 and 9, session-8-policies, intro-session and the x402 work sit on the branch claude/agent-payments-simple of moi-foundation/MOI-Webinars (95 commits ahead of main, 2 behind, on 14 October 2026). The repo is public, so review before merging, and squash so the branch's commit names do not land on main.
- Status says nine sessions. Folders exist for sessions 1 to 9. The session history in the moi-webinar skill (as of 2 October 2026) records sessions 1 to 4, 7 and 8 as held, has no record that 5 and 6 were, and lists 9 as planned. Confirm the count with Rahul.
