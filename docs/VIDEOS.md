# Handover videos

One video per product, recorded after its doc is reviewed. Screen plus voice, 5 to 10 minutes, no editing. Each shows the workflow end to end, the tools and logins it needs, and the Claude skill in use. They live in the Google Drive folder https://drive.google.com/drive/folders/1AVuEBGUHnuXPKwqRoFNAcSUdxQg97dKY (owner adithya@moinetwork.io, a company account), and each one is linked under the Status line of its product doc as "Video: <link>".

| Product | Doc | Video |
|---|---|---|
| Community Call | COMMUNITY-CALL.md | https://drive.google.com/file/d/14SSJ1bCHjiOu4d_J1_UDcsk3VNQZVkKP/view (the deck skill) |
| Dev Webinars | DEV-WEBINARS.md | |
| Blog | BLOG.md | |
| MOI Website | MOI-WEBSITE.md | |
| Dataroom | DATAROOM.md | |
| Agent Launchpad | AGENT-LAUNCHPAD.md | |
| MCP server | MCP-SERVER.md | |
| Points Program | POINTS-PROGRAM.md | |

Reference: the community call recordings, https://www.youtube.com/playlist?list=PL4-oiZj2acUPhBkDGm-8ue9jIVxh-NXvs. Watch one before recording, for the pace and the segments.

## Community Call (target 8 minutes)

1. What it is: monthly, Friday, Vardan owns the event, I own the deck and the protocol and DevRel segments. Show the Variables table.
2. The timeline: scroll the Process section from Wednesday of the week before to the day of the call. Say out loud what is due on Friday and who sends it.
3. Luma: open the MOI calendar, a past call's page, the two mailing lists, and where the announcement to signed-up guests is sent from.
4. Riverside: open the room, the description with the links, where speakers are invited.
5. The deck: open the community-call-14 folder in the webinars repo. Run the deck build with the moi-webinar deck branch: the HTML deck, the checker, the PDF export. Show one slide with a figure and its source line.
6. The release check: open the release note next to the release slides.
7. YouTube description: show a past description built from the agenda.
8. Day of: the stale-wording sweep, present from the HTML, PDF open as fallback.
9. After: the post-call tweets and shorts (Vardan), the audience questions note.
10. Logins needed: Luma admin, Riverside, YouTube. Say who holds each today.

## Dev Webinars (target 10 minutes)

1. What it is: a live build of one project on MOI, I own it end to end, Vardan gives the Meet link. Show the Variables table.
2. The repo: open session-8-policies as the model session folder. README with the steps, LUMA.md, RUNBOOK.md, GAMEDAY.md, NOTES.md, BLOG.md. Then a code session like session-6.
3. The timeline: scroll the Process from a week before to after the session. Say what happens on each of the four post days.
4. Luma: create a page from a past one, the time zones line, the Meet link.
5. Buffer: run the channels command, draft one post with --draft, show it in Buffer. Say the key comes from Chandra.
6. Building the project: run one session's README steps on devnet, up to the first interaction. Show where devnet facts come from (the node, not a note).
7. The deck, if the session has one: the deck branch build, checker, PDF.
8. The bounty: open the Points admin page, the composer, Create, Open after the session (POINTS-PROGRAM.md).
9. After: the blog draft with the moi-blog skill, the PR to the website repo, push the session folder.
10. Logins: Luma, Google Meet, Buffer, YouTube. Say who holds each.

## Agent Launchpad (target 10 minutes)

Reference: the intro session deck in intro-session/deck (press P for the script) and the launch video folder on Drive. Beat 2 is the same demo cue the deck uses.

1. What it is: open launchpad.moi.technology, the templates, create, dashboard, marketplace, stats. Say what is inactive (paid agents, QR sign-in).
2. Sign in with the wallet, create an agent from a template, register it on chain, link Telegram, download the runtime and start it. Send the bot a message.
3. The repo: the fork and the org repo, app/, lib/templates, agent-runtime, contracts/agent_market, supabase/migrations.
4. Shipping: a branch on the fork, typecheck and tests locally, the PR to the org repo, merge builds and deploys. Show the Actions run from 7 October and the image on GHCR.
5. Settings: the Actions secrets and variables page, names only. Which ones are baked at build. Setting a value deploys nothing.
6. Supabase: the company organisation, the project, the SQL editor where migrations run by hand.
7. Telegram: the bot in BotFather, the alert chat, the webhook secret rule.
8. After a devnet reset: the registry id, the deploy, the registration wallets, the AgentMarket contract, the proof sign-in.
9. Health: stats not zero, the bot answers, the skill's health check: "Is the Launchpad healthy?"
10. Logins: GitHub, Supabase (company), Telegram bot (transfer pending), the VM (DevOps only).

## Dataroom (target 8 minutes)

1. What it is: open dataroom.moi.technology, the home tiles (whitepaper, litepaper, decks), a document page, the email gate. Say what is inactive (the chat, the Events page).
2. The admin page: unlock with the secret, the document list with its statuses (pending, processing, completed), Re-index.
3. Add a document: category first, upload a PDF, watch it go pending, processing, completed. Then replace a file inside a document, and the one-click permanent delete warning.
4. The home page: the seven slots, "Show on home" pinning, the title-match fallback, where the figures live in the code.
5. Adopters, events and leads: where they are edited and what shows on the site.
6. The repo: the moi-data-room folder, the API routes, the migrations that were made by hand, the deploy workflow.
7. Settings: the Actions secrets by name, the manual deploy run after any change. Show today's run.
8. Supabase: the company organisation, the documents table, the private bucket, the vector index.
9. Health: the site, an upload that indexes, the Supabase advisors.
10. Logins: GitHub, Supabase (company), the VM (DevOps only), the admin secret (in the password manager).

## MOI Website (target 10 minutes)

1. What it is: moi.technology and blog.moi.technology, one repo, one deploy. Show the Variables table and what is inactive.
2. The repo: src (the React site and its prerendered routes), server (the Express app behind /api), blog (Astro), scripts, the four workflows.
3. Shipping: branch, lint, both builds, the PR with its two preview links, merge, the Actions run reaching the server. Open the live page afterwards.
4. Publishing a post: the markdown file, the header fields, the preview, Rahul's review, merge. Point at the Blog video for the writing process.
5. Announcing: the social copy PR the workflow opens, the Distribute dry run, the Buffer drafts.
6. The calendar: /admin/calendar with the admin key, and why the homepage shows the fallback dates today.
7. Settings: the Actions secrets by name, the VITE_ rule, a new secret needs a line in the workflow.
8. The chatbot: off on the server, the four steps to bring it back.
9. Health: the three pages, /api/health, robots and llms and the sitemap.
10. Logins: GitHub, Supabase (confirm which project), the Analytics account, DevOps for the server.

