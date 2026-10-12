# MOI Website

**Status: active.** The site and the blog are live. The chatbot and the community calendar are gone: the site is static files plus the blog, and the calls live on Luma.

moi.technology and the blog at blog.moi.technology. One repo, one deploy. The site is a React app whose marketing pages are prerendered at build time (since 5 October 2026); the blog is built with Astro from the same repo. There is no server: the chatbot and the calendar were removed in October 2026. I own the code and the content. DevOps owns the server.

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Codebase | DevRel | https://github.com/sarvalabs/MOI-Website, public. Merging to main deploys. I push branches to it, no fork |
| Server, nginx, TLS, DNS, the deploy script | DevOps (Srikar) | The deploy script lives on the server, not in the repo |
| Blog posts | DevRel | Markdown files under blog/src/content/posts |
| Community calls on the homepage | DevRel, dates from Vardan | A block that links to the MOI calendar on Luma. The link in the code is a placeholder (LUMA_URL_PLACEHOLDER in src/components/CommunityCalls.jsx) until the real calendar address goes in. The next call's date, title and link come from content/next-call.json; only the date is required, a past date hides the line |
| Papers | DevRel | PDFs the site serves under /papers |
| Analytics | The sarvalabsdeveloper@gmail.com account | Tag Manager and Analytics. The container id is written in the code. Search Console: confirm |
| Supabase project | DevRel. Transferred to the sarvalabsdeveloper@gmail.com account on 12 October 2026; Gokul notified | Held the calendar's events and the chatbot's documents. Nothing on the site reads it any more; keep or delete |

## Stack

| Piece | What it is |
|---|---|
| React 19 + Vite 7 + Tailwind 4 | The site. Four marketing routes, prerendered by scripts/ssg.mjs at build |
| Astro 5 | The blog, in blog/, with its own package.json |
| scripts/build-blog-index.js | Writes the site's /blog listing from the posts and copies the covers |
| GitHub Actions + Teleport | A merge to main runs the deploy script on the VM, which builds both and serves the files. Pull requests get a preview of each |
| Distribute and social-prepare workflows | Announce a post: draft copy as a PR, then Buffer drafts |
| Tag Manager | Measurement, with the container id in the code |

## Env vars

The index across every product, with the consoles and who holds each login, is ENV-VARS.md.

Where they live: GitHub Actions secrets and variables on sarvalabs/MOI-Website. Both sites build with none. What is left serves the deploy and the announcement workflow.

| Variable | What it is | Where the value comes from |
|---|---|---|
| BLOG_ORIGIN | Where the site's blog listing links to. Optional; defaults to https://blog.moi.technology | |
| BUFFER_ACCESS_TOKEN, BUFFER_CHANNEL_X, BUFFER_CHANNEL_LINKEDIN, DISCORD_WEBHOOK_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID | The "Distribute a post" workflow, one per channel. A missing one skips its channel. Only the three Buffer names are set today, so Discord and Telegram are skipped | Buffer (Chandra), Discord server settings, BotFather |
| TELEPORT_PROXY, TELEPORT_JOIN_TOKEN, TELEPORT_NODE, VM_USERNAME, PREVIEW_VM_HOST, PREVIEW_VM_USER | Deploy and preview access | DevOps |
| SUPABASE_URL, SUPABASE_KEY, ADMIN_API_KEY, VITE_CHATBOT_API, ANTHROPIC_API_KEY, OPENAI_API_KEY, DATA_ROOM_CHAT_URL, VITE_GA_ID, PUBLIC_GA_ID | Dead once the removal merges: nothing reads them | Delete them from the repo's secrets |

The example file is .env.example in the repo.

## Process

**Shipping a change**

- Work on a branch and push it to the repo.
- Run lint and both builds myself: the site and the blog. A pull request builds both for its preview links, but nothing runs lint.
- Open a pull request. It gets a preview link for the site and one for the blog.
- Merging to main deploys: GitHub Actions reaches the server and runs its script, which builds and serves the files. The workflow passes nothing but the branch name any more.
- Open the live page afterwards. A green run proves little.
- There is no rollback. Revert in a new pull request.
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
- To send for real, run it again with dry run set to false and the slug typed a second time in the confirm box; the workflow refuses to send if the two do not match. It then creates drafts in Buffer for X and LinkedIn from the post's social copy file. Drafts, not posts. Discord and Telegram would post straight away, but their secrets are not set, so those channels are skipped.
- Open Buffer and publish the two drafts by hand, at the time you want.

**Updating the next community call on the homepage**

- Edit content/next-call.json: `{ "date": "2026-11-18", "title": "Community call 16", "url": "https://lu.ma/..." }`. Only the date is required. Open a pull request, merge. If the date has passed or the file is empty, the block shows only the Luma button.

**Changing a setting or a secret**

- Set it in GitHub, under the repo's Actions secrets and variables, then redeploy.
- A new secret also needs a line in the deploy workflow, or it never reaches the server.

**Checking it is healthy**

- Open moi.technology, blog.moi.technology and one post.
- Check robots.txt, llms.txt and the sitemap answer.
- Check the homepage's community calls block links to Luma.

## Claude skill

The **moi-web-products-ops** skill covers running the site: shipping, settings and health. Its calendar and chatbot runbooks describe what was removed in October 2026 and are kept only for the history. The **moi-blog** skill covers posts: writing, publishing, announcing and the newsletter. The search and AI-visibility layer of the site is in **moi-docs** (its geo part).

| When | What to tell Claude | What the skill does |
|---|---|---|
| Something looks wrong | "Is the website healthy?" | Runs a read-only health check on the live site and blog, and names the known faults. |
| Shipping | "Ship this website change." | Walks the branch, the local checks and the pull request, and says what merging will deploy. |
| A post | "Write a blog post on ..." | Drafts it in the house style, checks every claim, and prepares the pull request. |
| Announcing | "Announce the post." | Rewrites the social copy and walks the Distribute run. I publish the drafts. |
| The next call | "Update the next community call on the homepage." | Edits content/next-call.json and opens the pull request for me to merge. |
| A setting | "I need to change this website setting: ..." | Says where it is set and whether it needs a rebuild. It never sees the secret's value. |

What the skills never do without my yes: push, merge (a merge deploys), run a workflow, post, send or change a secret.
