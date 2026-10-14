# Blog

**Status: active.** Six posts live; the monthly newsletter runs on the 15th.

Marketing: Variables, Process (step 8 Announce and step 9 Newsletter of Writing a post, and The monthly newsletter), Open items. Developers: How it works, Stack, Env vars, Process (Writing a post, Other kinds of post, Images, Editing or deleting a published post), Claude skill.

blog.moi.technology, a separate site from moi.technology that lives in the same repo and deploys with it. Every post is one markdown file, and the blog is built with **Astro** (a tool that turns the files into a static website). Two kinds of post recur: the write-up after a **Builders session** (MOI's live developer webinar, covered in DEV-WEBINARS.md), and the monthly release post written from the protocol team's release note. DevRel writes the posts, Rahul reviews them, and the announcement goes out through a workflow in the same repo. As of October 2026 there are six posts live; the September release post is the one to copy.

## How it works

**Two sites, one repo**

- moi.technology is the marketing site, a React app at the root of sarvalabs/MOI-Website.
- blog.moi.technology is a separate site, an Astro app in the blog/ folder of the same repo, with its own build.
- Both live in one repo and deploy together: a merge to main builds both and the server serves them as two hosts.
- The main site has a /blog page, but it is only a listing. It is static HTML generated from the same markdown files, and every card links across to the article on blog.moi.technology.
- The blog builds with no secrets. The marketing site needs only the blog address at build time (BLOG_ORIGIN). The secrets in the repo belong to the deploy and to the announcing workflow.

**Where a post lives**

- The file: blog/src/content/posts/<slug>.md in sarvalabs/MOI-Website. The file name is the slug and the URL is blog.moi.technology/article/<slug>/.
- The same file feeds everything: the article page, the listing at moi.technology/blog, the two RSS feeds, the sitemap and llms.txt (the plain-text list of posts for AI assistants).
- Images go in blog/src/assets/<slug>/. A cover image goes in blog/public/covers/. The rules are under "Images" below.

**The header fields (frontmatter)**

| Field | What it does |
|---|---|
| title | Page title, H1, listing cards, feeds, structured data. Plain and specific, ideally 60 characters or fewer; the page adds "MOI Blog" after it |
| summary | The meta description, the line under the H1, the feed text, the llms.txt line, and what the newsletter shows. One answer-shaped sentence, about 140 to 160 characters |
| date | Publish date, written as 2026-09-11. The site publishes on merge; a future date does not hold a post back |
| updated | Set only if the post changed after it went live |
| author | Name, role and a full https URL |
| tags | Only agents, protocol and native-assets show as pills on the site; any other tag still gets a page |
| takeaways | The box above the body. Eight, or none |
| faq | Question and answer pairs. Seven to seventeen. Each answer also becomes structured data, so it must stand alone |
| cover | The social share image. No post on main sets one yet |
| draft | true hides the post everywhere |

Only the blog build checks these fields: its content schema rejects a missing title or summary, a date that does not parse, an author link that is not a full URL, or a malformed FAQ. The website build reads the same file with no checks and renders a listing card from whatever it finds. So a header the blog build rejects still produces a card at moi.technology/blog, pointing at an article that does not exist. Run both builds before merging. The preview build does.

**How it deploys**

- A pull request gets two preview links in a comment: the site (pr-<N>.preview.moi.technology) and the blog (pr-<N>-blog.preview.moi.technology). They are rebuilt on every push and deleted after 7 days or when the pull request closes.
- Read the post on the blog preview at /article/<slug>/. Do not judge it from the site preview's /blog listing: its cards link to production, where a new post does not exist yet.
- The preview build runs both builds, so a bad header field fails it.
- Merging to main runs the deploy workflow: GitHub Actions reaches the server through Teleport and runs a script there that builds both sites. Nothing is deployed by hand.
- There is no rollback button. The deploy builds whatever is on main and overwrites the live files; no earlier build is kept to switch back to. If a merge breaks something, open a pull request that reverts the merge commit and merge that. The deploy runs again and the live sites go back to the previous state a few minutes later.
- Merging announces nothing and sends no email. Announcing is a separate step, on purpose, because a post often needs a correction in its first hour. The newsletter picks the post up by itself on the 15th.

**Search and AI visibility**

- Each page carries a **canonical URL** (the one official address of the page), **Open Graph** tags (the tags that set the preview card when a link is shared), Article structured data, and FAQ structured data when the post has an FAQ.
- The site serves robots.txt, a sitemap and llms.txt. Google Tag Manager runs on both hosts.
- The listing at moi.technology/blog is static HTML with its own structured data, so AI crawlers that do not run JavaScript still see it.
- Every announcement link carries **UTM** tags (query parameters such as utm_source that Analytics reads), and so does every link in the newsletter, so Analytics can tell X, LinkedIn, email and search apart.

## Stack

| Piece | What it is |
|---|---|
| Astro 5 | Builds the blog from the markdown files, in blog/ of the website repo. Node 22 |
| Markdown with a header block | One file per post. The header fields are checked by the blog build |
| Astro sitemap plugin, two RSS feeds, **llms.txt** (a plain-text list of posts for AI assistants) | Generated at build time from the same files |
| scripts/build-blog-index.js | Builds the static listing at moi.technology/blog for the React site |
| GitHub Actions + **Teleport** (the gateway DevOps uses to reach the server) | The deploy: a merge to main runs a script on the server that builds both sites |
| GitHub Actions workflows | "Prepare social copy" drafts the announcement file; "Distribute a post" sends it: X and LinkedIn to **Buffer** (a post-scheduling service) as drafts, Discord and Telegram straight to the channel |
| Buffer | Where the X and LinkedIn announcements land as drafts for a person to approve and publish. The same account the webinar posts go through; the login is Chandra's and the setup is in DEV-WEBINARS.md |
| Mailchimp | An RSS campaign: on the 15th of every month it reads the email feed and sends the posts that are new. No code in the repo |
| Google Tag Manager and Analytics | Measurement on both hosts. Both are under the sarvalabsdeveloper@gmail.com account |

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Posts | DevRel | blog/src/content/posts in sarvalabs/MOI-Website |
| Review | Rahul | Every post before it merges |
| Release note | Protocol team | The source for a release post. Kept exactly as sent |
| Social copy | DevRel | social/<slug>.md, drafted by a workflow, rewritten by hand. Marketing owns the company channels, so check with them before anything goes out |
| Newsletter (**Mailchimp**, the email service) | Vardan | Has the Mailchimp login. An **RSS** campaign (RSS is a standard feed format that other tools can poll for new posts), the 15th of every month |
| Server and deploy script | DevOps | Shared with the website |

## Env vars

The index across every product, with the consoles and who holds each login, is ENV-VARS.md. The blog has no secrets of its own: the Astro build, the listing script, the feeds and llms.txt run with none, and Mailchimp holds its own settings. These are the only values that touch a post. All of them live on the website repo, and the full table for that repo, including the deploy access, is in MOI-WEBSITE.md.

| Variable | What it is | Where the value comes from |
|---|---|---|
| BLOG_ORIGIN | Where the listing at moi.technology/blog links to. Optional; defaults to https://blog.moi.technology | Actions variable on sarvalabs/MOI-Website |
| BUFFER_ACCESS_TOKEN, BUFFER_CHANNEL_X, BUFFER_CHANNEL_LINKEDIN | The "Distribute a post" workflow: X and LinkedIn, queued in Buffer as drafts | Buffer (Chandra). Set as of October 2026 |
| DISCORD_WEBHOOK_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID | The same workflow: Discord and Telegram, posted directly. A missing one skips its channel | Discord server settings, BotFather. Not set as of October 2026, so both channels are skipped |
| Tag Manager container id | Measurement on both hosts | In the code, not a variable. The container is under sarvalabsdeveloper@gmail.com |
| Mailchimp (feed address, schedule, sender, audience) | The monthly newsletter | Settings on the RSS campaign in Mailchimp (Vardan), nothing in the repo |

## Process

### Writing a post, step by step

**How the AI fits in, and what worked**

- Before asking the AI to write anything, write down every claim and every message the post will make, in a doc, in your own words. Understand each one. Where you do not, ask Rahul and the protocol team. If DevRel does not understand a claim, nobody can hold the AI accountable for it.
- Hand that claims doc to the moi-blog skill and let it consolidate the claims into a draft. The skill carries the **humanizer** and **stop-slop** rules (two Claude skills that strip AI-sounding patterns from prose), so it runs a couple of polish rounds on its own and gives feedback on tone and language. Iterate until you are happy with how it reads.
- Then run the skill the other way: have it break the finished post back down into its individual claims, and compare them with the claims doc. This catches a message that got lost or turned ambiguous while the prose was being written.
- The same pass fact-checks the post. Load the skill with the release note for a release post, or point it at the session codebase for a webinar write-up, so every claim is checked against the source and not against memory. Doing this at the very end, after the polish, is what worked.

**1. Brief and angle**

- One line: what the developer can do after reading this.
- Decide which kind of post this is: an explainer (What is MOI Network), an argument, a release post (MOI September 2026 Release), a session write-up, or a short how-to (Move your Voyage login to MOI Wallet; **Voyage** is MOI's explorer and faucet product). Then read the most recent live post of that same kind from start to finish, so the new one takes the same shape, length and tone instead of inventing a new one.
- Check no post already covers it.

**2. Sources**

- For a release: the protocol team's note, kept exactly as sent, plus the tagged versions.
- For a session write-up: the session folder and the real output of the demo.
- For anything called "live": a read from **devnet** (MOI's shared test network), not the source code.
- Write every claim and message into the claims doc first, and clear the ones you do not understand with Rahul or the protocol team before drafting.

**3. Draft**

- Give the claims doc to the moi-blog skill and start from the post template (or the release post template).
- Open with the claim, in one bold declarative sentence that stands alone. It is the paragraph an answer engine quotes.
- Second person, plain words, one point per paragraph, sentence-case headings, no emoji, no em dashes.
- Make a heading a question where the section answers one, and answer it in the first sentence. Not every heading.
- Define every protocol term the first time it appears, and bold the term there.
- Names: MOI, Sarva Labs, **KMOI** (the network's native token), js-moi-sdk in lowercase, **Coco** (MOI's contract language; write Cocolang on first mention in a post). One name per concept in every post.
- Exact versions in a table, full dates, and "as of" on anything that moves.
- Link to the docs pages for every concept, and to the sibling posts.
- End with the takeaways, the FAQ, and a "Key takeaways, recap" section. The counts and the rules for each field are in the header table above.

**4. Check every claim**

- Have the skill list every sentence that states a fact, a number, a version or a date, and compare the list with the claims doc: every claim still there, none ambiguous.
- Give each one a source and a verdict: verified, true only with a limit, an opinion, or cut. The source is the release note or the session codebase loaded into the skill.
- Change the text to match the verdicts. Nothing unverified ships.

**5. Polish, in this order**

- Facts first: the claim check is done before polish starts, and a rewrite that changes a claim sends it back for a check.
- Read-alone test: every sentence makes sense on its own.
- Plain-language pass: short sentences, one point per paragraph, the thing named, no universals.
- humanizer, then stop-slop: paragraph by paragraph. When the wording is contested, make three variants and pick one.
- Newcomer read: could someone who has never read the docs follow it?
- Search check: title length, summary, takeaways, FAQ, question headings, links to the docs.
- Lint, zero errors: the post linter (`post-lint.py --strict` in the moi-blog skill, which also runs the house lint) and the house lint (`slop-lint.sh` in the moi-devrel skill, a check for rejected wording).
- Re-read the opener after every automated pass. Passes keep bringing back phrasing that was already rejected.
- Read the whole post once on the preview link before review.

**6. Build and open the pull request**

- Run both builds locally.
- Branch from main, commit under your work identity (as of October 2026 the current one is sarvalabs-adithya with adithya@sarva.ai; the next owner uses their own work account) with no AI co-author line, push, open one pull request with the template body.
- Review changes go on the same branch in small commits. One post, one pull request, one squash merge.

**7. Review and merge**

- Rahul reviews.
- Merge on a yes that names the pull request. The post is live a few minutes later.
- Open the live page and read it. Check the listing card at moi.technology/blog. Click every link and open every image.
- Request indexing of the new URL in Search Console. The property is under the sarvalabsdeveloper@gmail.com account.

**8. Announce**

- The announcing flow below exists and works, but check with marketing before running it for a post: they own what goes out on the company channels. In practice DevRel used it mainly for the Dev Webinars posts (the Buffer side is in DEV-WEBINARS.md), not for every blog post.
- About a minute after the merge, the "Prepare social copy" workflow opens a pull request with social/<slug>.md: one text block per channel, seeded from the summary.
- Rewrite the X and LinkedIn blocks by hand, leave Discord and Telegram empty, and merge that pull request.
- Run the "Distribute a post" workflow by hand. It is a dry run by default. To send for real, switch dry run off and type the slug again in the confirm box; with the box empty or wrong, nothing is sent. There is no undo on the real run.
- What the real run does: X and LinkedIn land in Buffer as drafts for a person to approve. Discord and Telegram post straight to the channel the moment the workflow runs, which is why their blocks are left empty: an empty block is skipped.
- Publish the X and LinkedIn drafts in Buffer (the account used for webinars; the Buffer setup itself is in the webinar doc), adding an image there.
- Record what went out where.

**9. Newsletter**

- Nothing to do. If the post is live at least three hours before the 15th's send, the monthly email includes it. See "The monthly newsletter" below.

### Other kinds of post

**The protocol release post**

- Once a month the protocol team ships a release, and a post follows it: "MOI <Month> 2026 Release: <what changed in plain words>", from the release post template.
- Keep the release note exactly as sent and quote it. Pin the release moment as a date and a 24 hour UTC time, never "today" or "12:00 AM".
- Before the upgrade, draft the announcements: the X thread, the LinkedIn post and the Discord post. Every line not in the note gets checked.
- Merge the post only once the upgrade has run and devnet answers with the new version. Then announce it as any post.
- If a posted statement turns out wrong, post a correction reply. Do not delete.
- Published before the 15th, it is in that month's newsletter.

**A session write-up**

- Work from the session folder: the storyline, the code, the demo's real output.
- The session's own BLOG.md is not a blog file: its header has to be rewritten to the blog's fields or the build fails.
- Link the recording and the repo folder.

### The monthly newsletter

One email a month, on the 15th, with every post published since the last one. Nobody writes it and nobody sends it. It is a Mailchimp RSS campaign, a standing automation inside Mailchimp with a feed address and a schedule. On the schedule Mailchimp fetches the feed, compares the items with what it sent last time, and if anything is new it builds one email from those items and sends it to the audience. If nothing is new, it sends nothing that month. Vardan has the Mailchimp login. Nothing about the newsletter lives in the repo, so a new DevRel needs that login, not a secret.

**What is set up, once**

- In Mailchimp there is one automation of the type "Share blog updates via RSS" (an RSS campaign). It is given the blog's email feed, https://blog.moi.technology/rss-email.xml, a schedule (monthly, the 15th, at a set hour; this doc does not record the hour, so read it in the campaign's schedule settings in Mailchimp), a subject line, a sender (a MOI address), an audience, and MOI's email design.
- The design is three template parts, header, body and footer, pasted into Mailchimp's editor once. The body part holds Mailchimp's RSS placeholders, which Mailchimp replaces with one block per new post: title, summary, link. The parts live in the moi-blog skill under templates/mailchimp.
- The audience is the Mailchimp list. People join it through the Subscribe box at the bottom of every article, which posts straight to Mailchimp's signup endpoint for that list, so the Mailchimp account is what lets people subscribe at all, not only what sends the email. About 5,500 addresses as of October 2026.

**How the feed feeds Mailchimp**

- The connection is pull, not push. The blog never calls Mailchimp and holds no Mailchimp key. The blog build writes a public file, blog.moi.technology/rss-email.xml, and the campaign in Mailchimp is configured with that address. At the scheduled hour Mailchimp fetches the file over plain HTTP, like any feed reader would.
- The file is a standard RSS feed, generated by blog/src/pages/rss-email.xml.js on every build from the post files, newest first, drafts left out. Each post is one item with four fields: title (the title field), description (the summary field, not the body), pubDate (the date field) and link (the article URL with the newsletter tags added). The tags are also carried as categories.
- Mailchimp reads the items, decides which ones it has not sent before by their link and date, and if there are any, fills the body template with them. The body template holds a loop, an RSSITEMS block, and inside it four placeholders: RSSITEM:TITLE, RSSITEM:URL, RSSITEM:DATE and RSSITEM:CONTENT. Mailchimp repeats the block once per new post and fills the placeholders from the item's title, link, pubDate and description. So the summary field is exactly what appears under each title in the email.
- The link in each item is not the bare article address. It has three tracking parameters on the end, the standard ones Google Analytics reads: utm_source=newsletter, utm_medium=email and utm_campaign=<the post's slug>. So the link for the September release post is blog.moi.technology/article/moi-september-2026-release/?utm_source=newsletter&utm_medium=email&utm_campaign=moi-september-2026-release. Mailchimp copies the link into the email exactly as it is. When a subscriber clicks it, the browser opens the article with those parameters still on the address, Analytics reads them, and the visit is recorded as newsletter traffic for that post. The announcement links use the same scheme with source x, linkedin, discord or telegram, so in Analytics you can compare how many readers each channel sent to one post.
- The normal feed, /rss.xml, has the same posts with plain links and is what feed readers use. The two are separate on purpose: feed readers are not the newsletter, and labelling their traffic as email would be wrong. Point Mailchimp at the email feed only.

**What happens on the 15th**

1. At the scheduled hour Mailchimp fetches the email feed.
2. It compares the items with what it sent last time, by each item's id and date. Everything published since the last send is "new".
3. If there is at least one new post, it builds one email from the design: header, then one block per new post with the title, the summary and the tagged link, then the footer. The newest post comes first.
4. It sends that email to the whole audience from the MOI sender address.
5. If nothing new was published since the last send, it sends nothing that month.

**What this means for publishing**

- A post is in the month's email only if it is live, meaning merged and deployed, at least three hours before the 15th's send hour (read from the campaign's schedule settings in Mailchimp; see Open items). That is Mailchimp's own guidance for RSS campaigns: a post published inside those three hours may not be picked up and then waits for the next month's email. A post that goes live on the 16th waits a month too.
- The email shows the summary, so the summary field of each post is what subscribers read.
- Never rename a published post's slug or change the link tagging. The feed's item id is the tagged link, so a change makes old posts look new and they would be sent again. The same rule is under "Editing or deleting a published post".
- An edit to a published post does not re-send it. Only a new post makes a new email.

**Checking and changing it**

- To see whether a month's email went out: Mailchimp, the RSS campaign, its reports (sent, opens, clicks). The 15 September send went out with the September release post.
- To change anything on the running campaign (schedule, subject, sender, design), open it in Mailchimp, choose Pause and Edit, make the change, then go to the Confirm step and press Start RSS to resume. Do this well before the 15th: posts published while it is paused queue up for the next send, a campaign that was recently resumed can take a day before it sends again, and it never sends more than once a day. The audience of a running RSS campaign cannot be changed; to change it, stop the campaign and build it again.
- Keep Mailchimp's own Google Analytics link tracking off. The links are already tagged, and Mailchimp's tracking would rename the campaign on every link.
- The design is changed by pasting new template parts into the campaign, through the same Pause and Edit.

**One-off emails**

- An email outside the monthly schedule (the August validator notice about the Voyage login was one) is a separate regular campaign: drafted from the same template parts, sent to a chosen segment, after a test send to the team. Sent by hand from Mailchimp.

### Images

- Body images go in blog/src/assets/<slug>/ and are referenced from the post as ../../assets/<slug>/<file>, with alt text.
- The cover image goes in blog/public/covers/. It is the picture shown when the link is shared on X or LinkedIn, and the thumbnail on the moi.technology/blog listing. If the cover is an SVG, a PNG with the same name must sit beside it, or the share image points at a missing file.
- An image that changes gets a new filename. Email clients and social caches keep the old file under the old name for a long time.
- No post on main sets a cover, so shares carry no picture as of October 2026. That is by choice; there is nothing to backfill.

### Editing or deleting a published post

- An edit goes through the same flow: branch, pull request, review, merge. Set the updated field only if the post changed after publication. An edit never re-announces and never re-sends the newsletter.
- Never rename a published slug. The slug is the URL, the canonical address, and the id in both feeds; renaming breaks every link and makes the newsletter treat the post as new.
- To delete, remove the file (or set draft to true), merge, and after the deploy check that the page is really gone. Deleted posts survived deploys once, in August 2026.
- The main site answers 200 for any address, so a page that looks like it exists there proves nothing. Check on blog.moi.technology, which answers 404 for an unknown article.

## Claude skill

| Skill | Used for | How |
|---|---|---|
| moi-blog | The whole post: brief, draft, publish, announce, newsletter | "Write a blog post on ..." or "Write up session 10." Then "Check every claim", "Open the pull request", "Announce the post" |
| moi-blog, release pack | A protocol release: the note, the announcements, the release post | "The release note for 0.14 arrived." It keeps the note verbatim, drafts the thread and posts, lints them, drafts the post |
| moi-devrel, claim check | Every claim against source | Run inside step 4. It lists the claims, DevRel settles the verdicts, it fixes the text |
| humanizer and stop-slop | The polish passes | Separate skills, not part of the library. Run paragraph by paragraph; the rules they apply are written into moi-blog so it works without them |
| moi-devrel, ship | The pull request, the merge, the identity check | Runs under moi-blog's publish step |
| moi-webinar | The source material for a session write-up | The session folder it produced |

Claude loads moi-blog on phrases like "write a blog post", "publish the post", "announce the post", "release note" or "newsletter".

What the skills never do without a yes from DevRel: push, merge (a merge deploys), run a workflow, create or publish a draft, post anywhere, or send an email.

## Open items

- The newsletter's send hour is not recorded anywhere in this doc, and the three-hour cutoff for a post depends on it. Read it from the RSS campaign's schedule in Mailchimp (Vardan has the login) and write it here.
- The Discord and Telegram announcement values (DISCORD_WEBHOOK_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID) are not set as of October 2026, so the "Distribute a post" workflow skips both channels. Decide with marketing whether to set them or leave those channels to a person.
- No post on main sets a cover image, so shares carry no picture. Decide with marketing whether to add covers.
- The Mailchimp login is Vardan's and the Buffer organisation is Chandra's. The next DevRel needs access to both; ask them before the first post.
- The announcing flow is used mainly for Dev Webinars posts. Agree with marketing which posts it should cover.
