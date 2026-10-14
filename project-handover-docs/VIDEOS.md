# Handover videos

**Status: in progress.** Recorded: the Community Call skill video, the Launchpad video (12 October), the Dataroom product demo (13 October) and the MCP server demo (13 October). Points Program: the webinar bounties walkthrough (14 October). None on record: the skill videos for the Launchpad, Dataroom and MCP server.

Marketing: the table of videos and the Reference line below it. Developers: the three outlines (Community Call, Agent Launchpad, Dataroom) and Open items.

Each product gets two videos, each with its own link. The product demo shows the workflow end to end, with the tools and logins it needs. The skill video shows the Claude skill that runs the product, used on screen. A **Claude skill** is a folder of instructions Claude loads for a kind of task. Record screen plus voice, 5 to 10 minutes, no editing. The videos live in the Google Drive folder https://drive.google.com/drive/folders/1AVuEBGUHnuXPKwqRoFNAcSUdxQg97dKY (owner adithya@moinetwork.io, Adithya's company Google account, which may close after he leaves: move the folder to a shared company Drive before 14 October). Each video is linked under the Status line of its product doc as "Video: <link>".

Decided on 13 October: no videos for the MOI Website, the Blog or Dev Webinars. The website is not a product, and the blog and the Builders sessions are process work, so their docs carry those processes.

| Product | Doc | Product demo | Skill video |
|---|---|---|---|
| Community Call | COMMUNITY-CALL.md | None on record | https://drive.google.com/file/d/14SSJ1bCHjiOu4d_J1_UDcsk3VNQZVkKP/view (the moi-webinar skill, deck branch; recorded 9 October) |
| Agent Launchpad | AGENT-LAUNCHPAD.md | https://drive.google.com/file/d/1FruKR8k6Wp_rplSFzIE8pZf8OBwBUfSI/view (recorded 12 October) | None on record (moi-launchpad-ops) |
| Dataroom | DATAROOM.md | https://drive.google.com/file/d/1FoOifehdhrH3hfrRJcbmim1WnRRBEXH5/view (recorded 13 October) | None on record (moi-web-products-ops) |
| MCP server | MCP-SERVER.md | https://drive.google.com/file/d/1NGdNHOIDr7VfghWqs58ufskWbVxHyvQL/view (recorded 13 October) | None on record (moi-mcp-ops) |
| Points Program | POINTS-PROGRAM.md | https://drive.google.com/file/d/1MOs61CECZt6SRQhH9Zro0t2avq0-XPsy/view (webinar bounties walkthrough, recorded 14 October) | None on record (moi-web-products-ops) |

Reference: the community call recordings, https://www.youtube.com/playlist?list=PL4-oiZj2acUPhBkDGm-8ue9jIVxh-NXvs. Watch one before recording to get the pace and the segments.

The outlines below are for the product demos. The Points Program video covers the webinar bounty flow only and has no outline here.

## Community Call (target 8 minutes)

1. What it is: monthly, on a Friday. Vardan owns the event, DevRel builds the deck and presents the DevRel segment, and the protocol content comes from Rahul's team. Show the Variables table.
2. The timeline: scroll the Process section from Wednesday of the week before to the day of the call. Say out loud what is due on Friday and who sends it.
3. **Luma** (the event-page service): open the MOI calendar, a past call's page and the two mailing lists. Show where the announcement to signed-up guests is sent from.
4. **Riverside** (the recording platform): open the room, the description with the links, and where speakers are invited.
5. The deck: open the community-call-14 folder in the moi-foundation/MOI-Webinars repo. Run the deck build with the moi-webinar skill, deck branch, and show the HTML deck, the checker and the PDF export. Show one slide with a figure and its source line.
6. The release check: open the release note next to the release slides.
7. YouTube description: show a past description built from the agenda.
8. Day of: the stale-wording sweep. Present from the HTML, with the PDF open as a fallback.
9. After: the post-call tweets and shorts (Vardan) and the audience questions note.
10. Logins needed: Luma admin, Riverside, YouTube. Say who holds each today.

## Agent Launchpad (target 10 minutes)

Reference: the intro session deck in others/webinars/intro-session-deck/ in the handover repo (press P for the script) and the launch video folder on Drive. Beat 2 is the same demo cue the deck uses (beats are the numbered demo cues in the deck's script).

1. What it is: open launchpad.moi.technology and show the templates, create, dashboard, marketplace and stats. Say what is inactive (paid agents). The phone QR sign-in is live now (tested 13 October), so the demo can also be done from a phone.
2. Sign in with the wallet, create an agent from a template, register it on chain, link Telegram, download the runtime and start it. Send the bot a message.
3. The repo: the fork and the org repo, app/, lib/templates, agent-runtime, contracts/agent_market, supabase/migrations.
4. Shipping: a branch on the fork, typecheck and tests locally, the PR to the org repo, and the merge that builds and deploys. Show the Actions run from 7 October and the image on **GHCR** (GitHub's container registry).
5. Settings: the Actions secrets and variables page, names only. Say which ones are baked in at build. Setting a value deploys nothing.
6. **Supabase** (the hosted database): the company organisation, the project, and the SQL editor where migrations run by hand. The project moved there on 8 October.
7. Telegram: the bot in **BotFather** (Telegram's bot-setup bot), the alert chat, and the webhook secret rule.
8. After a **devnet** (MOI's test network) reset: the registry id, the deploy, the registration wallets, the **AgentMarket** contract (the marketplace contract) and the proof sign-in.
9. Health: stats not zero, the bot answers, and the skill's health check: "Is the Launchpad healthy?"
10. Logins: GitHub, Supabase (company), the Telegram bot (transfer pending) and the VM (DevOps only).

## Dataroom (target 8 minutes)

1. What it is: open dataroom.moi.technology and show the home tiles (whitepaper, litepaper, decks), a document page and the email gate. Say what is inactive (the chat, the Events page).
2. The admin page: unlock with the secret, then show the document list with its statuses (pending, processing, completed) and Re-index.
3. Add a document: pick the category first, upload a PDF, and watch it go pending, processing, completed. Then replace a file inside a document and show the one-click permanent delete warning.
4. The home page: the seven slots, "Show on home" pinning, the title-match fallback, and where the figures live in the code.
5. Adopters, events and leads: where they are edited and what shows on the site.
6. The repo: the moi-data-room folder, the API routes, the migrations (the Dataroom tables and the require_email column now have one in the repo, PR #7, merged 13 October) and the deploy workflow.
7. Settings: the Actions secrets by name, and the manual deploy run after any change. Show today's run.
8. Supabase: the company organisation (the project moved there on 8 October), the documents table, the private bucket and the **vector index** (the search index over the documents).
9. Health: the site, an upload that indexes, and the Supabase advisors.
10. Logins: GitHub, Supabase (company), the VM (DevOps only) and the admin secret (in the password manager).

## Open items

- Optional: a fuller Points Program demo (an X like campaign, shipping, health). The webinar bounty walkthrough is recorded (14 October).
- Record the skill videos: Launchpad (moi-launchpad-ops), Dataroom (moi-web-products-ops), MCP server (moi-mcp-ops), Points (moi-web-products-ops).
- Record a Community Call product demo if the new owner wants one beside the skill video.
- Confirm what the Launchpad video (12 October) covers. It is listed as the product demo, and the Launchpad outline above also includes the skill's health check.
