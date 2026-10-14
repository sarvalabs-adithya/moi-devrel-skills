# Handover videos

**Status: in progress.** Recorded: the Community Call skill video, the Launchpad video (12 October), the Dataroom product demo (13 October) and the MCP server demo (13 October). None on record: any video for the Points Program, and the skill videos for the Launchpad, Dataroom and MCP server. Decided on 13 October: no videos for the MOI Website, the Blog or Dev Webinars; their docs carry those processes. The website is not a product, and the blog and the Builders sessions are process work.

Two videos per product, each with its own link: a product demo (the workflow end to end, the tools and logins it needs) and a skill video (the Claude skill that runs the product, used on screen). A **Claude skill** is a folder of instructions Claude loads for a kind of task. Screen plus voice, 5 to 10 minutes, no editing. They live in the Google Drive folder https://drive.google.com/drive/folders/1AVuEBGUHnuXPKwqRoFNAcSUdxQg97dKY (owner adithya@moinetwork.io, Adithya's company Google account, which may close after he leaves: move the folder to a shared company Drive before 14 October), and each one is linked under the Status line of its product doc as "Video: <link>".

| Product | Doc | Product demo | Skill video |
|---|---|---|---|
| Community Call | COMMUNITY-CALL.md | None on record | https://drive.google.com/file/d/14SSJ1bCHjiOu4d_J1_UDcsk3VNQZVkKP/view (the moi-webinar skill, deck branch; recorded 9 October) |
| Agent Launchpad | AGENT-LAUNCHPAD.md | https://drive.google.com/file/d/1FruKR8k6Wp_rplSFzIE8pZf8OBwBUfSI/view (recorded 12 October) | None on record (moi-launchpad-ops) |
| Dataroom | DATAROOM.md | https://drive.google.com/file/d/1FoOifehdhrH3hfrRJcbmim1WnRRBEXH5/view (recorded 13 October) | None on record (moi-web-products-ops) |
| MCP server | MCP-SERVER.md | https://drive.google.com/file/d/1NGdNHOIDr7VfghWqs58ufskWbVxHyvQL/view (recorded 13 October) | None on record (moi-mcp-ops) |
| Points Program | POINTS-PROGRAM.md | None on record | None on record (moi-web-products-ops) |

Reference: the community call recordings, https://www.youtube.com/playlist?list=PL4-oiZj2acUPhBkDGm-8ue9jIVxh-NXvs. Watch one before recording, for the pace and the segments.

The outlines below are for the product demos. The Points Program has no outline yet.

## Community Call (target 8 minutes)

1. What it is: monthly, Friday, Vardan owns the event, DevRel builds the deck and presents the DevRel segment; the protocol content comes from Rahul's team. Show the Variables table.
2. The timeline: scroll the Process section from Wednesday of the week before to the day of the call. Say out loud what is due on Friday and who sends it.
3. **Luma** (the event-page service): open the MOI calendar, a past call's page, the two mailing lists, and where the announcement to signed-up guests is sent from.
4. **Riverside** (the recording platform): open the room, the description with the links, where speakers are invited.
5. The deck: open the community-call-14 folder in the moi-foundation/MOI-Webinars repo. Run the deck build with the moi-webinar skill, deck branch: the HTML deck, the checker, the PDF export. Show one slide with a figure and its source line.
6. The release check: open the release note next to the release slides.
7. YouTube description: show a past description built from the agenda.
8. Day of: the stale-wording sweep, present from the HTML, PDF open as fallback.
9. After: the post-call tweets and shorts (Vardan), the audience questions note.
10. Logins needed: Luma admin, Riverside, YouTube. Say who holds each today.

## Agent Launchpad (target 10 minutes)

Reference: the intro session deck in others/webinars/intro-session-deck/ in the handover repo (press P for the script) and the launch video folder on Drive. Beat 2 is the same demo cue the deck uses (beats are the numbered demo cues in the deck's script).

1. What it is: open launchpad.moi.technology, the templates, create, dashboard, marketplace, stats. Say what is inactive (paid agents). The phone QR sign-in is live now (tested 13 October), so the demo can also be done from a phone.
2. Sign in with the wallet, create an agent from a template, register it on chain, link Telegram, download the runtime and start it. Send the bot a message.
3. The repo: the fork and the org repo, app/, lib/templates, agent-runtime, contracts/agent_market, supabase/migrations.
4. Shipping: a branch on the fork, typecheck and tests locally, the PR to the org repo, merge builds and deploys. Show the Actions run from 7 October and the image on **GHCR** (GitHub's container registry).
5. Settings: the Actions secrets and variables page, names only. Which ones are baked at build. Setting a value deploys nothing.
6. **Supabase** (the hosted database): the company organisation, the project, the SQL editor where migrations run by hand. The project moved there on 8 October.
7. Telegram: the bot in **BotFather** (Telegram's bot-setup bot), the alert chat, the webhook secret rule.
8. After a **devnet** (MOI's test network) reset: the registry id, the deploy, the registration wallets, the **AgentMarket** contract (the marketplace contract), the proof sign-in.
9. Health: stats not zero, the bot answers, the skill's health check: "Is the Launchpad healthy?"
10. Logins: GitHub, Supabase (company), Telegram bot (transfer pending), the VM (DevOps only).

## Dataroom (target 8 minutes)

1. What it is: open dataroom.moi.technology, the home tiles (whitepaper, litepaper, decks), a document page, the email gate. Say what is inactive (the chat, the Events page).
2. The admin page: unlock with the secret, the document list with its statuses (pending, processing, completed), Re-index.
3. Add a document: category first, upload a PDF, watch it go pending, processing, completed. Then replace a file inside a document, and the one-click permanent delete warning.
4. The home page: the seven slots, "Show on home" pinning, the title-match fallback, where the figures live in the code.
5. Adopters, events and leads: where they are edited and what shows on the site.
6. The repo: the moi-data-room folder, the API routes, the migrations (the Dataroom tables and the require_email column now have one in the repo, PR #7, merged 13 October), the deploy workflow.
7. Settings: the Actions secrets by name, the manual deploy run after any change. Show today's run.
8. Supabase: the company organisation (the project moved there on 8 October), the documents table, the private bucket, the **vector index** (the search index over the documents).
9. Health: the site, an upload that indexes, the Supabase advisors.
10. Logins: GitHub, Supabase (company), the VM (DevOps only), the admin secret (in the password manager).

## Open items

- Record the Points Program demo, and write its outline (the admin page, an X like campaign, a webinar bounty, shipping, health).
- Record the skill videos: Launchpad (moi-launchpad-ops), Dataroom (moi-web-products-ops), MCP server (moi-mcp-ops), Points (moi-web-products-ops).
- Record a Community Call product demo if the new owner wants one beside the skill video.
- Confirm what the Launchpad video (12 October) covers: it is listed as the product demo, and the Launchpad outline above also includes the skill's health check.
