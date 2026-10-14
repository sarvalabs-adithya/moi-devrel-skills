# Search and AI visibility for a post

Facts are as of 2026-10-02, from `sarvalabs/MOI-Website` on `main` (commit `5e91afa`), a local build of 2026-10-01 and read-only requests to the live site. This file covers what a post needs and what is already built. The search layer of every site (docs, robots, `llms.txt` generators, audits) is `moi-docs/geo`; the docs sites themselves are `moi-docs`. Back to `../SKILL.md`.

## Why a post exists
The 4 August 2026 strategy call decided that everything the team does becomes text that search engines and AI systems can read, and that each dev talk and video comes with a blog. The blog link is the announcement: publish, then point to it. AI systems that scan LinkedIn see only the short post and follow the link to the detail. The shape agreed there: the big picture first, then the how-to, with backlinks "as much as possible" without loading the post up. The transcript is not in the repo (not recorded: the previous DevRel's notes; ASK: Rahul).

## What is already built
| Output | Where it comes from |
|---|---|
| `<link rel="canonical">`, `og:title`, `og:description`, `og:type`, `og:url` | `blog/src/layouts/Base.astro`. The canonical is built from `Astro.site`, which is hardcoded to `https://blog.moi.technology` |
| `og:image` and `twitter:card` | Only when the post sets `cover` (`assets.md`). None does |
| `Article` JSON-LD, plus `FAQPage` when the post has `faq` | `blog/src/pages/article/[...id].astro`. The author is typed `Organization` |
| `/llms.txt` | `blog/src/pages/llms.txt.js`: title, absolute URL and summary of each published post, newest first. Drafts are excluded |
| `/sitemap-index.xml` and `/sitemap-0.xml` | `@astrojs/sitemap`: every built page, tag pages included |
| `/rss.xml` | Untagged links, for feed readers |
| `/rss-email.xml` | Newsletter-tagged links, for Mailchimp only. Not advertised and not in the sitemap |
| `/robots.txt` | A static file in `blog/public/` |
| The listing at `moi.technology/blog` | `scripts/build-blog-index.js`: static HTML with `Blog` and `BlogPosting` JSON-LD, because the marketing site renders client side and a React route would be an empty page to most AI crawlers |
| Google Tag Manager on both hosts | `blog/src/components/Analytics.astro`. The container id is in that file |
The old checked-in guide says every post also gets BlogPosting with `wordCount`, a Person author and a BreadcrumbList. It does not. Adding a breadcrumb is a change, not a fix.

## Rules a post follows
1. Title: plain and specific, ideally 60 characters or fewer. The docs standard says results truncate near 60, and the page title tag adds a separator and "MOI Blog". No limit for the blog is recorded and the release pattern runs longer. ASK: Rahul.
2. Summary: it is the meta description, the line under the H1, the feed text and the `llms.txt` line. One statement, about 140 to 160 characters, answer-shaped, not a teaser. (Docs standard. The September summary was cut for the meta description at review, and its 240 characters shipped anyway.)
3. First paragraph: one declarative sentence that states the claim and stands alone, because it is the paragraph an answer engine quotes.
4. Headings: question H2s where the section answers the question, answered in the first sentence. 52 of 67 H2s on the six posts are questions.
5. Takeaways (8) and FAQ (7 to 17): bullet summaries and question and answer pairs are what language models lift most reliably (CONTENT.md's reasoning). Each FAQ answer goes verbatim into the JSON-LD, so it must stand alone.
6. Names: MOI, Sarva Labs, KMOI, js-moi-sdk (always lowercase), Coco (also known as Cocolang on first mention). The docs write MOIPod and release posts write moipod, which `moi-devrel/references/terminology.md` marks contested. Keep one name per concept in every post. Wikidata items for MOI and Sarva Labs were being prepared (Sai Kiran said someone is doing Wikidata), and their status is unknown. Matching organisation descriptions across Crunchbase, LinkedIn and GitHub was not done as of 2026-09-10, so never write that it was. ASK: Sai Kiran.
7. Dates and versions: exact versions in a table, full dates, "as of" for anything that moves.
8. Links: the SDK repo, the docs page for each tool, sibling posts by absolute URL. Link text says what the link is.
9. Say only what you can defend. Do not claim a measurement that was not run.
10. All the text is in the HTML. The blog is statically generated, so crawlers that do not run JavaScript read the full article.

## Crawler access
`blog/public/robots.txt` allows `*`, `GPTBot`, `ClaudeBot`, `PerplexityBot`, `CCBot`, `Google-Extended` and `anthropic-ai`, and declares the sitemap. The apex `robots.txt` carries the same group and cross-submits the blog sitemap, because a sitemap cannot list URLs on another host. On 2026-10-02 the live article answered 200 to user agents named GPTBot, ClaudeBot, PerplexityBot and OAI-SearchBot.
- OpenAI's crawler page (read 2026-10-02) lists `OAI-SearchBot` for search results, `GPTBot` for training and `ChatGPT-User` for pages a ChatGPT user asks it to open, each set separately. Only `GPTBot` is named in the file, so the other two fall under `*`. Nothing is blocked. Read the list as what the file names, not as what reaches ChatGPT.
- Google's crawler page (read 2026-10-02) says `Google-Extended` controls use of content for training future Gemini models and for grounding in Gemini apps and the Vertex AI API, and has no effect on Google Search. So blocking it would not remove a page from AI Overviews.
- The same permissive file is served on pull request previews. `Astro.site` is hardcoded, so a preview's canonical and sitemap entries point at production, which is what keeps previews from being indexed as duplicates (the previous operator's reading). Do not make `site` dynamic without adding `noindex` to previews, or every open PR becomes an indexable duplicate.
- A Cloudflare WAF or bot-fight setting can silently block AI crawlers. It did on `cocolang.dev` until 2026-09-09. Re-run the user-agent check after any Cloudflare, WAF or hosting change: `curl -sI -A "GPTBot/1.0" https://blog.moi.technology/`.

## Two hosts, two properties
`blog.moi.technology` is a separate host from `moi.technology`. Search Console treats them as separate properties, so registering the apex gives no query data for the blog. `project-handover-docs/LIST-OF-DEPENDENCIES.md` (the 4 October 2026 snapshot) lists the properties. The Search Console property is under the shared company developer account (`project-handover-docs/BLOG.md`). Submit `https://blog.moi.technology/sitemap-index.xml` in the blog property. Requesting indexing for a new URL is the operator's yes. Bing was imported from Search Console on 2026-09-09. Whether the blog is in that import is not recorded. ASK: Rahul.

## Tag pages in the sitemap
The sitemap has 26 URLs: the blog home page, 6 articles and 19 tag pages (read 2026-10-02). Only `agents`, `protocol` and `native-assets` are linked from the site, so 16 tag pages exist that no link reaches. That is thin content submitted for indexing at about 3 to 1 against articles. If Search Console reports "Crawled, currently not indexed" in volume, look here first. The fix is a filter on the sitemap integration, not deleting tags (the previous operator's advice).

## Measurement
- Analytics: GA4 is a tag inside the Tag Manager container. The previous operator's account is that a Page Hostname condition on its trigger keeps previews out of the production property, so if preview traffic shows up, check that trigger, not the code. Tag Manager is not readable from the repo and this was not re-checked on 2026-10-02. The container is under the shared company developer account (`moi-devrel/references/keys-and-access.md`). `VITE_GA_ID` and `PUBLIC_GA_ID` are passed by the deploy and read by nothing.
- UTM, one definition in `blog/src/lib/utm.js`:
| `utm_source` | `utm_medium` |
|---|---|
| `x`, `linkedin`, `reddit` | `social` |
| `discord`, `telegram` | `community` |
| `newsletter` | `email` |
| `devto` | `syndication` |
- `utm_campaign` is always the post slug. `utm_content` separates a day-7 repost, and only `scripts/share-links.js` emits one (`day7`). Print the links with `npm run social:links <slug> -- --md`.
- Casing is the contract: GA4 files `linkedin` and `LinkedIn` as two channels. `reddit` and `devto` have links and no sender.
- Mailchimp must read `/rss-email.xml`, and its own Google Analytics tracking stays off, because it would rename `utm_campaign` after the campaign (`newsletter.md`).
- AI visibility: slide 5 of the community call 14 deck (script dated 2026-09-25) called the Scribble AI-visibility figures the baseline to measure every month, and Sai Kiran passed the report on for that call. Whether it has been re-run is not recorded. Of the deck figures, visibility (17.3 percent), citations (1,203) and mentions (650) were confirmed in the call ledger. The 47 queries, the five engines and the 221 of 226 coverage were not (`moi-webinar/community-call/references/inputs-checklist.md`). Do not quote any of them in a post. No promptfoo baseline exists (the run timed out on 2026-09-09). Whether Scribble's report can be read directly is unknown. ASK: Sai Kiran.
- Ideas never built, each a Tag Manager change that needs no deploy: scroll-depth triggers, outbound-click triggers for docs and GitHub, a referral exclusion between the two hosts, and a segment for referrers such as `chatgpt.com` and `perplexity.ai`. The previous operator's reasoning: without the cross-host exclusion, a reader who crosses hosts counts as two sessions.
- Judge results at 4 to 8 weeks. At six posts, week-to-week movement is noise (the previous operator's advice).

## Local checks before the PR
After `npm run build --prefix blog`, on the built files:
```
grep -o 'application/ld+json.\{0,200\}' blog/dist/article/<slug>/index.html   # Article, and FAQPage if the post has faq
grep '<loc>' blog/dist/sitemap-0.xml | grep <slug>                            # in the sitemap
grep <slug> blog/dist/llms.txt                                                # in the AI index
grep -o 'og:image[^>]*' blog/dist/article/<slug>/index.html                   # a hit only when cover is set
node scripts/build-blog-index.js && grep <slug> public/blog/index.html        # on the apex listing
```
After the deploy: `python3 "$SKILLS/moi-blog/scripts/check-live.py" <slug>`.

## Gotchas
| Looks right | Actually wrong | Symptom |
|---|---|---|
| The post is live and in the sitemap | The blog is a separate Search Console property | Zero query data, no error |
| `cover` set to an SVG and the thumbnail renders | `og:image` points at a PNG that was never made | Blank share previews, seen only when someone shares |
| A link shared as `?utm_source=LinkedIn` | GA4 splits it from `linkedin` | Two half-sized rows in the channel report |
| The newsletter campaign wired to `rss.xml` | Clicks arrive untagged | Email looks like direct traffic |
| A preview looks right | `BLOG_ORIGIN` is not set, so its listing cards link to production | You click a card and land on the live site or a 404 |

## Not yet known
- Whether the blog has an IndexNow key file, and who submits it. The docs sites do. Not recorded (the previous DevRel's notes). ASK: Rahul.
- Who owns Bing. Search Console, Analytics and Tag Manager are on the shared company developer account (`moi-devrel/references/keys-and-access.md`). ASK: Rahul for Bing.
- Whether the Wikidata items for MOI and Sarva Labs exist. ASK: Sai Kiran.
