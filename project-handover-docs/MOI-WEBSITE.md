# MOI Website

**Status: active.** The site and the blog are live. The homepage's community calendar was replaced by a block that links to **Luma** (the event-calendar service the community calls are listed on), in PR #60, merged on 13 October 2026; the block stays hidden until the Luma address is set. The chatbot and the **Express server** (the small Node web server in server/ that answers the site's /api routes) stay as they are, decided on 13 October.

Marketing: Variables, Process (Publishing a blog post, Announcing a post, Updating the next community call on the homepage), Open items. Developers: Stack, Env vars, Process (Shipping a change, Changing a setting or a secret, Checking it is healthy), Claude skill, Open items.

This is moi.technology and its blog at blog.moi.technology, built from one repo and shipped in one deploy. The site is a React app whose marketing pages are **prerendered** at build time (written out as finished HTML files, so crawlers and AI tools see the text; since 5 October 2026). The blog is built with **Astro** (a static site builder) from the same repo. The Express server runs beside the static files and holds the chatbot route and the old calendar routes. DevRel owns the code and the content. DevOps (Srikar) owns the server.

## Stack

| Piece | What it is |
|---|---|
| React 19 + Vite 7 + Tailwind 4 | The site. Four marketing routes, prerendered by scripts/ssg.mjs at build |
| Astro 5 | The blog, in blog/, with its own package.json. Its build also writes the sitemap, the RSS feed and **llms.txt** (a plain-text map of the site for AI tools) |
| Express server | server/index.js. Serves /api/chat (the chatbot), /api/community-calls (the old calendar, with admin routes behind ADMIN_API_KEY) and /api/health. Run by **PM2** (a process manager that restarts a Node app if it stops) behind nginx's /api location, both set up by DevOps |
| Chatbot | The "Ask the protocol" chat. Hidden on the homepage (a comment in HomePage.jsx says it is temporarily hidden because the backend is not responding). The route and its keys stay |
| scripts/build-blog-index.js | Writes the site's /blog listing from the posts and copies the covers |
| GitHub Actions + **Teleport** | Teleport is the secure-access gateway the deploy goes through. A merge to main runs the deploy script on the VM, which builds both and serves the files. Each pull request gets a preview of the site and the blog |
| Distribute and social-prepare workflows | Announce a post. The first workflow drafts the copy as a PR, then the second creates drafts in **Buffer** (a social media scheduling service) |
| Tag Manager | Measurement, with the container id in the code |

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Codebase | DevRel | https://github.com/sarvalabs/MOI-Website, public. Merging to main deploys. DevRel pushes branches to it, no fork |
| Server, **nginx** (the web server in front of the files), TLS, DNS, the deploy script | DevOps (Srikar) | The deploy script lives on the server, not in the repo |
| Blog posts | DevRel | Markdown files under blog/src/content/posts |
| Community calls on the homepage | DevRel, dates from Vardan | A block that links to the MOI calendar on Luma (PR #60). It is off until `lumaUrl` in content/community-calls.json holds the real calendar address; today it is empty, so the homepage shows no community section. The same file takes an optional `nextCall` (date, title, link); only the date is required, and a past date hides the line |
| Papers | DevRel | PDFs the site serves under /papers |
| Analytics | The sarvalabsdeveloper@gmail.com account | Google Tag Manager is the script on every page that loads Analytics. Its container id is typed into the code (the site's index.html and the blog's Analytics component), so that account decides what runs on the site, and changing containers means editing those two files. Google Search Console (indexing and sitemaps for moi.technology) is under the same account |
| Supabase project | Not recorded | Holds the old calendar's events (the community_calls table, used only by the Express server's /api/community-calls routes now that the homepage uses Luma) and the chatbot's documents. Which project, and under which login, is not recorded; the documents probably sit in the Dataroom's project |

## Env vars

The index across every product, with the consoles and who holds each login, is ENV-VARS.md.

Where they live: GitHub Actions secrets and variables on sarvalabs/MOI-Website. They serve the Express server, the announcement workflow and the deploy.

| Variable | What it is | Where the value comes from |
|---|---|---|
| BLOG_ORIGIN | Where the site's blog listing links to. Optional; defaults to https://blog.moi.technology | Not needed. The code default is used |
| BUFFER_ACCESS_TOKEN, BUFFER_CHANNEL_X, BUFFER_CHANNEL_LINKEDIN, DISCORD_WEBHOOK_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID | The "Distribute a post" workflow, one per channel. A missing one skips its channel. Only the three Buffer names are set (checked 14 October 2026), so Discord and Telegram are skipped | Buffer (Chandra), Discord server settings, BotFather |
| TELEPORT_PROXY, TELEPORT_JOIN_TOKEN, TELEPORT_NODE, VM_USERNAME, PREVIEW_VM_HOST, PREVIEW_VM_USER | Deploy and preview access. VM_HOST and VM_SSH_KEY are also set (April 2026), from before the Teleport deploy | DevOps |
| SUPABASE_URL, SUPABASE_KEY, VITE_CHATBOT_API, ANTHROPIC_API_KEY, OPENAI_API_KEY, DATA_ROOM_CHAT_URL | Live. The chatbot and the Express server use them, and the deploy passes them to the server script | Supabase, the two model consoles, the Dataroom (see ENV-VARS.md) |
| ADMIN_API_KEY | The calendar admin routes on the Express server. The deploy does not pass it, so the routes accept a default written in the source, and the repo is public | `openssl rand -hex 32`; pass it in the deploy and remove the fallback |
| VITE_GA_ID, PUBLIC_GA_ID | Passed by the deploy and read by nothing, because Tag Manager does the measuring. Leave them | The GA4 property |

The example file is .env.example in the repo.

## Process

**Shipping a change**

- Work on a branch and push it to the repo.
- DevRel runs lint and both builds, the site and the blog. A pull request builds both for its preview links, but nothing runs lint.
- Open a pull request. It gets a preview link for the site and one for the blog.
- Merging to main deploys: GitHub Actions reaches the server and runs its script, which builds and serves the files. The workflow passes the branch name and the Express server's values (the live row under Env vars) to that script.
- Open the live page afterwards, because a green run proves little.
- There is no rollback. To undo a change, revert it in a new pull request.
- A new page also needs a line in the sitemap file in the repo.

**Publishing a blog post**

- Write the post as a markdown file in the blog folder, from the post template.
- Check every claim against the source.
- Run the blog build: `cd blog && npm install && npm run build`. It is the only check of the post's header fields (title, summary and date are required; a misspelt optional field is silently ignored). A failing build names the file and the field.
- Open a pull request, read the preview, get Rahul's review.
- Merge. The post is live a few minutes later. Merging announces nothing.

**Announcing a post**

- After the merge, a workflow opens a pull request with draft social copy. Rewrite it by hand and merge it.
- Run the Distribute workflow: GitHub, Actions, "Distribute", Run workflow. It asks for the slug: the post's file name without .md, for example moi-september-2026-release, which is also the end of the post's address. Dry run is on by default: the run prints what it would send and sends nothing. Read that output.
- To send for real, run it again with dry run set to false and the slug typed a second time in the confirm box; the workflow refuses to send if the two do not match. It then creates drafts in Buffer for X and LinkedIn from the post's social copy file. These are drafts, not posts. Discord and Telegram would post straight away, but their secrets are not set, so those channels are skipped.
- Open Buffer and publish the two drafts by hand, at the time you want.

**Updating the next community call on the homepage**

- Edit content/community-calls.json: `{ "lumaUrl": "https://lu.ma/...", "nextCall": { "date": "YYYY-MM-DDTHH:MM:SSZ", "title": "...", "url": "https://lu.ma/..." } }`. `lumaUrl` must be a web link or the whole block stays hidden. In `nextCall` only the date is required; a date with no time counts for that whole UTC day. Open a pull request, merge: the file is read at build time. If the date has passed or `nextCall` is null, the block shows only the Luma button.

**Changing a setting or a secret**

- Set it in GitHub, under the repo's Actions secrets and variables, then redeploy.
- A new secret also needs a line in the deploy workflow, or it never reaches the server.

**Checking it is healthy**

- Open moi.technology, blog.moi.technology and one post.
- Check robots.txt, llms.txt and the sitemap answer.
- Check that the homepage's community calls block links to Luma. This applies once `lumaUrl` is set; until then the homepage correctly shows no such block.

## Claude skill

The **moi-web-products-ops** skill covers running the site: shipping, settings and health. Its calendar runbook was updated for PR #60 on 13 October, and its chatbot runbook still applies, since the chatbot and the server stay. The **moi-blog** skill covers posts: writing, publishing, announcing and the newsletter. The search and AI-visibility layer of the site is in **moi-docs** (its geo part).

| When | What to tell Claude | What the skill does |
|---|---|---|
| Something looks wrong | "Is the website healthy?" | Runs a read-only health check on the live site and blog, and names the known faults. |
| Shipping | "Ship this website change." | Walks the branch, the local checks and the pull request, and says what merging will deploy. |
| A post | "Write a blog post on ..." | Drafts it in the house style, checks every claim, and prepares the pull request. |
| Announcing | "Announce the post." | Rewrites the social copy and walks the Distribute run. DevRel publishes the drafts. |
| The next call | "Update the next community call on the homepage." | Edits content/community-calls.json and opens the pull request for DevRel to merge. |
| A setting | "I need to change this website setting: ..." | Says where it is set and whether it needs a rebuild. It never sees the secret's value. |

What the skills never do without DevRel's yes: push, merge (a merge deploys), run a workflow, post, send or change a secret.

## Open items

- Set the Luma address. `lumaUrl` in content/community-calls.json is empty, so the homepage shows no community section. Ask Vardan for the calendar address, then open a pull request. The date of the next call (CC15, expected the last week of October) is not set either; ask Vardan.
- The chatbot answers: unknown. It is hidden on the homepage, and GitHub issue 3 on the repo (opened 20 April) reports the retrieval query failing against the Supabase project. Whether the route works today, and which Supabase project SUPABASE_URL points at, is for DevOps (Srikar) to confirm.
- VITE_CHATBOT_API is believed to hold the dev host, not https://moi.technology (ENV-VARS.md). Confirm what it holds.
- ADMIN_API_KEY is not passed by the deploy, so the calendar admin routes accept the default written in the public source. Pass the key and remove the fallback, or remove the routes.
- Optional: set DISCORD_WEBHOOK_URL, TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID if posts should also go to Discord and Telegram. They are not set today.
