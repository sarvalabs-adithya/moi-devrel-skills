# Blog

**Status: active.** Six posts live; the monthly newsletter runs on the 15th.

blog.moi.technology, a separate site from moi.technology that lives in the same repo and deploys with it. Every post is one markdown file, and the blog is built with Astro. Two kinds of post recur: the write-up after a Builders session, and the monthly release post written from the protocol team's release note. I write the posts, Rahul reviews them, and the announcement goes out through a workflow in the same repo. As of October 2026 there are six posts live; the September release post is the one to copy.

## Stack

| Piece | What it is |
|---|---|
| Astro 5 | Builds the blog from the markdown files, in blog/ of the website repo. Node 22 |
| Markdown with a header block | One file per post. The header fields are checked by the blog build |
| Astro sitemap plugin, two RSS feeds, llms.txt | Generated at build time from the same files |
| scripts/build-blog-index.js | Builds the static listing at moi.technology/blog for the React site |
| GitHub Actions + Teleport | The deploy: a merge to main runs a script on the server that builds both sites and restarts |
| GitHub Actions workflows | "Prepare social copy" drafts the announcement file; "Distribute a post" sends it to the channels as drafts |
| Mailchimp | An RSS campaign: on the 15th of every month it reads the email feed and sends the posts that are new. No code on our side |
| Google Tag Manager and Analytics | Measurement on both hosts. Both are under the sarvalabsdeveloper@gmail.com account |

## How the blog works

**Two sites, one repo**

- moi.technology is the marketing site, a React app at the root of sarvalabs/MOI-Website.
- blog.moi.technology is a separate site, an Astro app in the blog/ folder of the same repo, with its own build.
- Both live in one repo and deploy together: a merge to main builds both and the server serves them as two hosts.
- The main site has a /blog page, but it is only a listing. It is static HTML generated from the same markdown files, and every card links across to the article on blog.moi.technology.
- The blog builds with no secrets. Only the marketing site's server needs any.

**Where a post lives**

- The file: blog/src/content/posts/<slug>.md in sarvalabs/MOI-Website. The file name is the slug and the URL is blog.moi.technology/article/<slug>/.
- The same file feeds everything: the article page, the listing at moi.technology/blog, the two RSS feeds, the sitemap and llms.txt (the plain-text list of posts for AI assistants).
- Images go in blog/src/assets/<slug>/. A cover image goes in blog/public/covers/.

**The header fields (frontmatter)**

| Field | What it does |
|---|---|
| title | Page title, H1, listing cards, feeds, structured data |
| summary | The meta description, the line under the H1, the feed text, the llms.txt line. One answer-shaped sentence, about 140 to 160 characters |
| date | Publish date, written as 2026-09-11. The site publishes on merge; a future date does not hold a post back |
| updated | Set only if the post changed after it went live |
| author | Name, role and a full https URL |
| tags | Only agents, protocol and native-assets show as pills on the site; any other tag still gets a page |
| takeaways | The box above the body. Eight, or none |
| faq | Question and answer pairs. Seven to seventeen. Each answer also becomes structured data, so it must stand alone |
| cover | The social share image. No post on main sets one yet |
| draft | true hides the post everywhere |

Only the blog build checks these fields. The website build does not, so a bad header can ship a post that is live but missing from the listing. Run both builds.

**How it deploys**

- A pull request gets two preview links in a comment: the site (pr-<N>.preview.moi.technology) and the blog (pr-<N>-blog.preview.moi.technology). They are rebuilt on every push and deleted after 7 days or when the pull request closes.
- Read the post on the blog preview at /article/<slug>/. Do not judge it from the site preview's /blog listing: its cards link to production, where a new post does not exist yet.
- The preview build runs both builds, so a bad header field fails it.
- Merging to main runs the deploy workflow: GitHub Actions reaches the server through Teleport and runs a script there that builds both sites and restarts. Nothing is deployed by hand.
- There is no rollback. Revert in a new pull request.
- Merging announces nothing. Announcing is a separate step, on purpose, because a post often needs a correction in its first hour.

**How a post is announced**

- About a minute after the merge, the "Prepare social copy" workflow opens a pull request with social/<slug>.md: one text block per channel, seeded from the summary.
- I rewrite the blocks by hand (X and LinkedIn; Discord and Telegram are left empty) and merge that pull request.
- The "Distribute a post" workflow, run by hand, sends the file to the channels as drafts. Dry run first, then once for real. There is no undo on the real run.
- A person publishes the drafts (they land in the Buffer account used for webinars; the Buffer setup itself is in the webinar doc), adding an image there.
- Each channel's link carries UTM tags, so Analytics can tell the channels apart.

**The newsletter**

- One email a month, on the 15th, with every post published since the last one. A Mailchimp RSS campaign built from the email feed; nobody writes or sends it. The whole mechanism is under "Monthly blog release" below.

**Search and AI visibility**

- Each page carries a canonical URL, Open Graph tags, Article structured data, and FAQ structured data when the post has an FAQ.
- The site serves robots.txt, a sitemap and llms.txt. Google Tag Manager runs on both hosts.
- The listing at moi.technology/blog is static HTML with its own structured data, so AI crawlers that do not run JavaScript still see it.

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Posts | DevRel | blog/src/content/posts in sarvalabs/MOI-Website |
| Review | Rahul | Every post before it merges |
| Release note | Protocol team | The source for a release post. Kept exactly as sent |
| Social copy | DevRel | social/<slug>.md, drafted by a workflow, rewritten by hand |
| Newsletter (Mailchimp) | Vardan has access | An RSS campaign, the 15th of every month |
| Server and deploy script | DevOps | Shared with the website |

## Env vars

The index across every product, with the consoles and who holds each login, is ENV-VARS.md.
The blog itself needs none: the Astro build, the listing script, the feeds and llms.txt run with no secret, and Mailchimp holds its own settings. The Tag Manager container id is in the code. The only variables that touch a post are the announcing workflow's channel secrets, which belong to the website repo and are listed in the website doc (BUFFER_ACCESS_TOKEN and the two channel ids, DISCORD_WEBHOOK_URL, TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID).

## My process for a post

**1. Brief and angle**

- One line: what the developer can do after reading this.
- Pick the kind of post and read the latest sibling end to end: an explainer, an argument, a release post, a session write-up or a short how-to.
- Check no post already covers it.

**2. Sources**

- For a release: the protocol team's note, kept exactly as sent, plus the tagged versions.
- For a session write-up: the session folder and the real output of the demo.
- For anything called "live": a read from devnet, not the source code.

**3. Draft**

- Start from the post template (or the release post template).
- Open with the claim, in one bold declarative sentence.
- Second person, plain words, one point per paragraph, sentence-case headings, no emoji, no em dashes.
- Make a heading a question where the section answers one, and answer it in the first sentence.
- Define every protocol term the first time it appears.
- End with eight takeaways, an FAQ, and a "Key takeaways, recap" section.

**4. Check every claim**

- List every sentence that states a fact, a number, a version or a date.
- Give each one a source and a verdict: verified, true only with a limit, an opinion, or cut.
- Change the text to match the verdicts. Nothing unverified ships.

**5. Polish, in this order**

- Facts first: the claim check is done before polish starts, and a rewrite that changes a claim sends it back for a check.
- Read-alone test: every sentence makes sense on its own.
- Plain-language pass: short sentences, one point per paragraph, the thing named, no universals.
- humanizer, then stop-slop: paragraph by paragraph. When the wording is contested, make three variants and pick one.
- Newcomer read: could someone who has never read the docs follow it?
- Search check: summary, takeaways, FAQ, question headings, links to the docs.
- Lint: the post linter and the house lint, zero errors.
- Re-read the opener after every automated pass. Passes keep bringing back phrasing that was already rejected.
- Read the whole post once on the preview link before review.

**6. Build and open the pull request**

- Run both builds locally.
- Branch from main, commit under my work identity with no AI co-author line, push, open one pull request with the template body.
- Review changes go on the same branch in small commits. One post, one pull request, one squash merge.

**7. Review and merge**

- Rahul reviews. Fix what he asks for.
- Merge on a yes that names the pull request. The post is live a few minutes later.
- Open the live page and read it. Check the listing card at moi.technology/blog. Click every link and open every image.

**8. Announce**

- Rewrite the social copy the workflow drafted, merge it, run Distribute as a dry run, then once for real.
- Publish the drafts by hand.
- Record what went out where.

**9. Newsletter**

- Nothing to do: if the post is live before the 15th, the monthly email picks it up. See "Monthly blog release".

## Monthly blog release (the newsletter)

Once a month, one email goes to every subscriber with all the posts published since the last email. Nobody writes it and nobody sends it: it is a Mailchimp RSS campaign, and this is exactly how it works.

**What is set up, once**

- In Mailchimp there is one automation of the type "Share blog updates via RSS" (an RSS campaign). It is given the blog's email feed, https://blog.moi.technology/rss-email.xml, a schedule (monthly, the 15th, at a set hour), a subject line, a sender (a MOI address), an audience, and our email design.
- The design is our three template parts, header, body and footer, pasted into Mailchimp's editor. The body part holds Mailchimp's RSS placeholders, which Mailchimp replaces with one block per post. The parts live in the moi-blog skill under templates/mailchimp.
- The audience is the Mailchimp list that the signup form at the bottom of every article page adds people to. About 5,500 addresses at the last count. Vardan has access to the Mailchimp account.

**What the blog does on its side**

- Every build of the blog generates the email feed from the post files. Each post is one item in the feed: its title, its summary (not the full body), its publish date, and its link.
- The link in the email feed carries tags (source newsletter, medium email, campaign the post's slug), so when a reader clicks through, Analytics files the visit as newsletter traffic, separate from X, LinkedIn and search.
- The normal feed, /rss.xml, has the same posts with plain links and is what feed readers use. The two are separate on purpose, so feed-reader clicks are not counted as email.
- There is no newsletter code and no Mailchimp key anywhere in the repo. The feed is the whole interface.

**What happens on the 15th**

1. At the scheduled hour Mailchimp fetches the email feed.
2. It compares the items with what it sent last time, by each item's id and date. Everything published since the last send is "new".
3. If there is at least one new post, it builds one email from our design: header, then one block per new post with the title, the summary and the tagged link, then the footer. The newest post comes first.
4. It sends that email to the whole audience from the MOI sender address.
5. If nothing new was published since the last send, it sends nothing that month.

**What this means for publishing**

- A post is in the month's email only if it is live, meaning merged and deployed, before the 15th's run. A post that goes live on the 16th waits for the next month's email.
- The email shows the summary, so the summary field of each post is what subscribers read. Write it as one answer-shaped sentence.
- Never rename a published post's slug or change the link tagging. The feed's item id is the tagged link, so a change makes old posts look new and they would be sent again.
- An edit to a published post does not re-send it. Only a new post makes a new email.

**Checking and changing it**

- To see whether a month's email went out: Mailchimp, the RSS campaign, its reports (sent, opens, clicks). Whether the September post went out in the October send has not been checked. Ask Vardan.
- The schedule, the subject and the sender are changed in the campaign's settings. The audience of a running RSS campaign cannot be changed; to change it, stop the campaign and build it again.
- Keep Mailchimp's own Google Analytics link tracking off. Our links are already tagged, and Mailchimp's tracking would rename the campaign on every link.
- The design is changed by pasting new template parts into the campaign.

**One-off emails**

- An email outside the monthly schedule (the August validator notice about the Voyage login was one) is a separate regular campaign: drafted from the same template parts, sent to a chosen segment, after a test send to ourselves. Sent by hand from Mailchimp.

## Other posts

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

## Images

- Body images go in blog/src/assets/<slug>/ and are referenced from the post as ../../assets/<slug>/<file>, with alt text.
- The cover image goes in blog/public/covers/. It is the picture shown when the link is shared on X or LinkedIn, and the thumbnail on the moi.technology/blog listing. If the cover is an SVG, a PNG with the same name must sit beside it, or the share image points at a missing file.
- An image that changes gets a new filename. Email clients and social caches keep the old file under the old name for a long time.
- No post on main sets a cover yet, so shares carry no picture today.

## Editing or deleting a published post

- An edit goes through the same flow: branch, pull request, review, merge. Set the updated field only if the post changed after publication. An edit never re-announces and never re-sends the newsletter.
- Never rename a published slug. The slug is the URL, the canonical address, and the id in both feeds; renaming breaks every link and makes the newsletter treat the post as new.
- To delete, remove the file (or set draft to true), merge, and after the deploy check that the page is really gone. Deleted posts survived deploys once, in August 2026.
- The main site answers 200 for any address, so a page that looks like it exists there proves nothing. Check on blog.moi.technology, which answers 404 for an unknown article.

## Search rules for a post

- Title: plain and specific, ideally 60 characters or fewer; the page adds "MOI Blog" after it.
- Summary: one answer-shaped sentence, about 140 to 160 characters. It is the meta description, the line under the title, the feed text, the llms.txt line, and what the newsletter shows.
- First paragraph: one declarative sentence that states the claim and stands alone. It is the paragraph an answer engine quotes.
- Headings: a question where the section answers one, answered in the first sentence. Not every heading.
- Eight takeaways and an FAQ of seven to seventeen entries. Each FAQ answer goes verbatim into the structured data, so it must stand alone.
- Names: MOI, Sarva Labs, KMOI, js-moi-sdk in lowercase, Coco (Cocolang on first mention). One name per concept in every post.
- Exact versions in a table, full dates, and "as of" on anything that moves.
- Link to the docs pages for every concept, and to the sibling posts.
- After publishing, request indexing of the new URL in Search Console. Ask who holds that property first.

## Claude skills, and how I use them

| Skill | Used for | How |
|---|---|---|
| moi-blog | The whole post: brief, draft, publish, announce, newsletter | "Write a blog post on ..." or "Write up session 10." Then "Check every claim", "Open the pull request", "Announce the post" |
| moi-blog, release pack | A protocol release: the note, the announcements, the release post | "The release note for 0.14 arrived." It keeps the note verbatim, drafts the thread and posts, lints them, drafts the post |
| moi-devrel, claim check | Every claim against source | Run inside step 4. It lists the claims, I settle the verdicts, it fixes the text |
| humanizer and stop-slop | The polish passes | Separate skills on my Mac, not part of the library. Run paragraph by paragraph; the rules they apply are written into moi-blog so it works without them |
| moi-devrel, ship | The pull request, the merge, the identity check | Runs under moi-blog's publish step |
| moi-webinar | The source material for a session write-up | The session folder it produced |

Claude loads moi-blog on phrases like "write a blog post", "publish the post", "announce the post", "release note" or "newsletter".

What the skills never do without my yes: push, merge (a merge deploys), run a workflow, create or publish a draft, post anywhere, or send an email.

