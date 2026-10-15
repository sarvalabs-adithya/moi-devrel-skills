# MOI Website

**Status: active.** moi.technology and the blog at blog.moi.technology are live. The homepage's community calls block links to **Luma** (the event page service the calls are listed on) since PR #60 (13 October 2026), but it stays hidden until the Luma address is set. Not running: the chatbot and the old calendar routes. Their server code is still in the repo, but the live site does not reach it (checked 14 October 2026), and the Supabase project they used no longer exists.

Marketing: How it works, Variables, Process (Publishing a blog post, Announcing a post, Updating the next community call), Open items. Developers: How it works, Stack, Env vars, Process, Claude skill, Open items.

This is MOI's main website and its blog, built from one repo and shipped in one deploy. DevRel owns the code and the content. DevOps (Srikar) owns the server.

## How it works

- **The site** is a React app. Its marketing pages are **prerendered**: written out as finished HTML at build time, so search engines and AI tools can read the text (since 5 October 2026).
- **The blog** is a separate site built with **Astro** (a static site builder) from the blog/ folder of the same repo. Every post is one markdown file. The blog build also writes the sitemap, the RSS feed and **llms.txt** (a plain-text map of the site for AI tools). BLOG.md covers writing and the newsletter.
- **One deploy ships both.** A merge to main runs a script on the DevOps server that builds the site and the blog and serves the files. Each pull request gets its own preview links.
- **The community calls block** on the homepage reads content/community-calls.json at build time: a link to the MOI calendar on Luma, and optionally the next call's date. It shows nothing until the Luma link is set.
- **What is not running.** server/index.js is a small Express server for the chatbot (/api/chat) and the old calendar (/api/community-calls). On 14 October 2026 the live site answered every /api address with the normal web page, so the server is not reached, and the chatbot is hidden on the homepage anyway. The Supabase project it used no longer exists. Treat both as switched off.
- **Measurement** is Google Tag Manager, whose container id is written in the code.

## Stack

| Piece | What it is |
|---|---|
| React 19, Vite 7, Tailwind 4 | The site. Four marketing routes, prerendered by scripts/ssg.mjs at build |
| Astro 5 | The blog, in blog/, with its own package.json |
| scripts/build-blog-index.js | Builds the site's /blog listing from the posts and copies the cover images |
| GitHub Actions and **Teleport** | The deploy. Teleport is the secure gateway the workflow uses to reach the server. Workflows: "Deploy MOI Website" (merge to main) and "MOI Website PR Preview" (pull requests) |
| "Prepare social copy" and "Distribute a post" workflows | Announce a post. The first drafts the social copy as a pull request; the second creates drafts in **Buffer** (a social media scheduling service) |
| Google Tag Manager | Loads Analytics on every page |
| server/index.js (Express) | Chatbot and old calendar routes. Not running on the live site (see How it works) |

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Codebase | DevRel | https://github.com/sarvalabs/MOI-Website, public. Merging to main deploys. Push branches straight to it |
| Server, **nginx** (the web server in front of the files), TLS, DNS, the deploy script | DevOps (Srikar) | The deploy script lives on the server, not in the repo |
| Blog posts | DevRel | Markdown files in blog/src/content/posts |
| Community calls block | DevRel, with the dates from Vardan | content/community-calls.json. `lumaUrl` is empty today, so the block is hidden |
| Papers | DevRel | PDFs the site serves under /papers |
| Analytics, Tag Manager and Search Console | The sarvalabsdeveloper@gmail.com account | The Tag Manager container id is written in the site's index.html and the blog's Analytics component, so changing containers means editing those two files |

## Env vars

The index across every product, with the consoles and who holds each login, is ENV-VARS.md.

The values are GitHub Actions secrets and variables on sarvalabs/MOI-Website. GitHub cannot show a secret back once set. The example file is .env.example in the repo.

| Variable | What it is | Where the value comes from |
|---|---|---|
| BUFFER_ACCESS_TOKEN, BUFFER_CHANNEL_X, BUFFER_CHANNEL_LINKEDIN | The "Distribute a post" workflow's Buffer token and the X and LinkedIn channels. Set | Buffer (Chandra creates the token) |
| DISCORD_WEBHOOK_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID | Would let the same workflow post to Discord and Telegram. Not set, so those channels are skipped | Discord server settings, BotFather |
| TELEPORT_PROXY, TELEPORT_JOIN_TOKEN, TELEPORT_NODE, VM_USERNAME, PREVIEW_VM_HOST, PREVIEW_VM_USER | Deploy and preview access. VM_HOST and VM_SSH_KEY are also still set from before the Teleport deploy | DevOps |
| BLOG_ORIGIN | Where the site's blog listing links to. Not set; the default https://blog.moi.technology is right | Not needed |
| VITE_GA_ID, PUBLIC_GA_ID | Passed by the deploy, read by nothing (Tag Manager does the measuring) | Leave them |
| SUPABASE_URL, SUPABASE_KEY, VITE_CHATBOT_API, ANTHROPIC_API_KEY, OPENAI_API_KEY, DATA_ROOM_CHAT_URL, ADMIN_API_KEY | For the chatbot and the old calendar server, which is not running. The deploy still passes most of them. Nothing needs them today | Not needed |

## Process

**Shipping a change**

- Work on a branch and push it to the repo.
- Run lint and both builds (the site and the blog) yourself. A pull request builds both for its preview links, but nothing runs lint.
- Open a pull request. It gets a preview link for the site and one for the blog.
- Merging to main deploys.
- Open the live page afterwards. A green run does not prove the page is right.
- There is no rollback button. To undo, revert in a new pull request.
- A new page also needs a line in the sitemap file in the repo.

**Changing a setting or a secret**

- Change it in GitHub, under the repo's Actions secrets and variables, then redeploy: `gh workflow run "Deploy MOI Website" -R sarvalabs/MOI-Website --ref main`. Changing a value deploys nothing by itself.
- A new secret also needs a line in the deploy workflow, or it never reaches the server.

**Checking it is healthy**

- Open moi.technology, blog.moi.technology and one post.
- Check that robots.txt, llms.txt and the sitemap load.
- Once `lumaUrl` is set, check the homepage block links to Luma. Until then, no block is correct.

**Publishing a blog post**

- Write the post as a markdown file in the blog folder, starting from the post template.
- Check every claim against its source.
- Run the blog build: `cd blog && npm install && npm run build`. It is the only check of a post's header (title, summary and date are required; a misspelt optional field is silently ignored). A failing build names the file and the field.
- Open a pull request, read the preview and get Rahul's review.
- Merge. The post is live a few minutes later. Merging does not announce it.

**Announcing a post**

- After the merge, the "Prepare social copy" workflow opens a pull request with draft social copy. Rewrite it by hand and merge it.
- Run "Distribute a post": GitHub, Actions, Distribute a post, Run workflow. Give it the slug: the post's file name without .md (for example moi-september-2026-release), which is also the end of the post's address. Dry run is on by default, so the first run only prints what it would send. Read it.
- Run it again with dry run off and the slug typed a second time in the confirm box (the run refuses if the two differ). It creates drafts in Buffer for X and LinkedIn. Discord and Telegram are skipped.
- Open Buffer and publish the two drafts by hand, when you want them out.

**Updating the next community call**

- Edit content/community-calls.json: `{ "lumaUrl": "https://lu.ma/...", "nextCall": { "date": "YYYY-MM-DDTHH:MM:SSZ", "title": "...", "url": "https://lu.ma/..." } }`.
- `lumaUrl` must be a web link, or the whole block stays hidden. In `nextCall` only the date is required; a date with no time counts for that whole day (UTC). Once the date passes, or if `nextCall` is null, the block shows just the Luma button.
- Open a pull request and merge it. The file is read at build time, so the merge's deploy shows the change.

## Claude skill

The **moi-web-products-ops** skill runs the site: shipping, settings and health. The **moi-blog** skill covers posts: writing, publishing, announcing and the newsletter. The search and AI-visibility layer of the site is in **moi-docs** (its geo part).

| When | What to tell Claude | What the skill does |
|---|---|---|
| Something looks wrong | "Is the website healthy?" | Runs a read-only check on the live site and blog and names the known faults. |
| Shipping | "Ship this website change." | Walks through the branch, the local checks and the pull request, and says what merging will deploy. |
| A post | "Write a blog post on ..." | Drafts it in the house style, checks every claim and prepares the pull request. |
| Announcing | "Announce the post." | Rewrites the social copy and walks through the Distribute run. You publish the drafts. |
| The next call | "Update the next community call on the homepage." | Edits content/community-calls.json and opens the pull request for you to merge. |
| A setting | "I need to change this website setting: ..." | Says where it is set and whether it needs a rebuild. It never sees the secret itself. |

Without your yes, the skills never push, merge (merging deploys), run a workflow, post, send or change a secret.

## Open items

- Set the Luma address. `lumaUrl` in content/community-calls.json is empty, so the homepage shows no community calls block. Ask Vardan for the MOI calendar link (and the CC15 date, expected the last week of October 2026), then open a pull request.
