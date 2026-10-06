# MOI Website

moi.technology and the blog at blog.moi.technology. One repo, one deploy. The site is a React app with its marketing pages prerendered (since 5 Oct 2026), a small Express server behind /api for the chatbot and the community calendar, and the blog built with Astro from the same repo. I own the code and the content. DevOps owns the server.

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Codebase | Me | sarvalabs/MOI-Website, public. Merging to main deploys. I push branches to it, no fork |
| Server, nginx, TLS, DNS, the deploy script | DevOps | The deploy script lives on the server, not in the repo |
| Supabase project | Confirm who | Holds the chatbot's documents and the calendar's events. It may be the Dataroom's project |
| Blog posts | Me | Markdown files under blog/src/content/posts |
| Community calendar | Me, dates from Vardan | Edited at /admin/calendar. Broken in production today |
| Chatbot | Me | Hidden on the live site since June 2026 |
| Papers | Me | PDFs the site serves under /papers |
| Analytics | Marketing (confirm) | Tag Manager, Analytics, Search Console |

The full list of settings and secrets, by name, is in the dependencies doc and in `.env.example` in the repo.

## Process

**Shipping a change**

- Work on a branch and push it to the repo.
- Run lint and both builds myself: the site and the blog. No pull request runs them.
- Open a pull request. It gets a preview link for the site and one for the blog.
- Merging to main deploys: GitHub Actions reaches the server and runs its script, which builds and restarts.
- Open the live page afterwards. A green run proves little.
- There is no rollback. Revert in a new pull request.
- A new page also needs a line in the sitemap file in the repo.

**Publishing a blog post**

- Write the post as a markdown file in the blog folder, from the post template.
- Check every claim against the source.
- Run the blog build. Only it checks the post's header fields.
- Open a pull request, read the preview, get Rahul's review.
- Merge. The post is live a few minutes later. Merging announces nothing.

**Announcing a post**

- After the merge, a workflow opens a pull request with draft social copy. Rewrite it by hand and merge it.
- Run the Distribute workflow as a dry run, then once for real. It makes Buffer drafts for X and LinkedIn.
- Publish the drafts in Buffer by hand.
- The newsletter is built by Mailchimp from the blog feed. Check whether the weekly campaign is running before relying on it.

**Adding a community call to the calendar**

- Sign in to /admin/calendar with the admin key and add the date, time and link.
- Today this fails: the calendar API returns an error and the live site calls the wrong host, so the homepage shows dates written in the code.

**Changing a setting or a secret**

- Set it in GitHub, under the repo's Actions secrets and variables.
- Redeploy. Values that start with VITE_ are baked in at build, so they need a rebuild.
- A new secret also needs a line in the deploy workflow, or it never reaches the server.

**Checking it is healthy**

- Open moi.technology, blog.moi.technology and one post.
- Check the homepage calendar shows real dates, not the fallback.
- Check robots.txt, llms.txt and the sitemap answer.

## Claude skill

The **moi-web-products-ops** skill covers running the site: shipping, the calendar, the chatbot, settings and health. The **moi-blog** skill covers posts: writing, publishing, announcing and the newsletter. The search and AI-visibility layer of the site is in **moi-docs** (its geo part).

| When | What to tell Claude | What the skill does |
|---|---|---|
| Something looks wrong | "Is the website healthy?" | Runs a read-only health check on the live site and blog, and names the known faults. |
| Shipping | "Ship this website change." | Walks the branch, the local checks and the pull request, and says what merging will deploy. |
| A post | "Write a blog post on ..." | Drafts it in the house style, checks every claim, and prepares the pull request. |
| Announcing | "Announce the post." | Rewrites the social copy and walks the Distribute run. I publish the drafts. |
| The calendar | "Add the October call to the calendar." | Gives the steps, and says plainly that the calendar is broken today and what fixes it. |
| A setting | "I need to change this website setting: ..." | Says where it is set and whether it needs a rebuild. It never sees the secret's value. |
| The chatbot | "What do I do about the chatbot?" | Lays out the two choices, bring it back or remove it, and the steps for each. |

What the skills never do without my yes: push, merge (a merge deploys), run a workflow, post, send or change a secret.

## Open items

- Fix the calendar: the API returns an error in production and the live site calls the wrong host. Find the Supabase project first.
- The calendar admin check is unsafe. The fix is written, not merged. It needs the admin key created in GitHub and DevOps to pass it to the server.
- Decide the chatbot: bring it back with a fresh index of the litepaper, or remove it.
- Ask DevOps for the nginx changes: a real 404 for unknown pages, the discovery header, a download header for the papers.
- Open pull requests to merge or close: #56 (September social copy, never announced), #54, #52, #8.
- Push the corrected README and deploy and content guides. The ones in the repo still describe the old setup.
- Take down the old copy at moi-website.vercel.app.
- Move the Supabase project and the API keys to company logins.
- The skills are not in a repo yet.
