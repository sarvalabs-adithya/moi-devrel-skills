# Writing a MOI blog post

Facts are as of 2026-10-02, read from `sarvalabs/MOI-Website` on `main` (commit `5e91afa`) and the live site. Back to `../SKILL.md`. Voice and wording rules shared with every skill live in `moi-devrel/references/house-style.md` and `terminology.md`. This file says what is specific to a post.

## Where the post goes
One Markdown file: `blog/src/content/posts/<slug>.md`. The file name is the slug and the URL is `https://blog.moi.technology/article/<slug>/`. A glob in `blog/src/content.config.ts` finds the file, and nothing else registers it. The listing at `https://moi.technology/blog` is generated from the same files by `scripts/build-blog-index.js`.
Slugs: lowercase words and hyphens that say what the post is (`what-is-moi-network`). A release post uses `moi-<month>-<year>-release` and the title `MOI <Month> 2026 Release: <what changed in plain words>`. The August title once led with the version and was changed to lead with the month (`3aacb49`). The `date` is the day the post goes live: "put date as today" in August, the release day (2026-09-11) in September.

## The six posts on main: pick the sibling to copy
Counts are body words (whitespace split, code included) and H2s, counted on 2026-10-02. Read one sibling end to end before you write.
| Slug | Genre | Date | Words | H2s as questions | Takeaways | FAQ | Em dashes |
|---|---|---|---|---|---|---|---|
| `what-is-moi-network` | Explainer | 2026-08-18 | 6987 | 17 of 18 | 8 | 13 | 0 |
| `how-to-give-an-ai-agent-authority-without-your-credentials` | Argument | 2026-08-19 | 6265 | 17 of 18 | 8 | 12 | 1 |
| `moi-august-2026-release` | Release, per package | 2026-08-21 | 3485 | 7 of 9 | 8 | 7 | 17 |
| `how-ai-agents-pay-each-other-moi` | Session write-up | 2026-08-21 | 3093 | 2 of 8 | none | 7 | 77 |
| `move-your-voyage-login-to-moi-wallet` | Short how-to | 2026-08-27 | 705 | 3 of 5 | 8 | 17 | 0 |
| `moi-september-2026-release` | Release, developer-first | 2026-09-11 | 2220 | 6 of 9 | 8 | 7 | 0 |
The September post is the latest release template (cleaned copy: `../examples/`). New posts carry no em dash, whatever the sibling does. Whether the older posts are edited to remove theirs is not decided. ASK: Rahul.

## Frontmatter
The contract is `blog/src/content.config.ts`. A violation fails `npm run build --prefix blog` and nothing ships broken.
```
title: string                     required
summary: string                   required
date: date                        required, write 2026-09-11
updated: date                     optional
author: { name, role?, url? }     optional, url must start with https://
tags: string[]                    default []
takeaways: string[]               optional
faq: { q, a }[]                   optional
cover: string                     optional
draft: boolean                    default false
```
A missing `date` fails with a confusing message about a Date (zod 4.4.3 in the blog's `node_modules` says "expected date, received Date"), not a "missing field" message. A string `author` and a bare-domain `author.url` fail too (checked 2026-10-02). Run `python3 "$SKILLS/moi-blog/scripts/post-lint.py" blog/src/content/posts/<slug>.md` first: it names the field.
| Field | Where it lands |
|---|---|
| `title` | The page title tag and `og:title` (title, a separator and "MOI Blog"), the H1, both listings, feeds, `llms.txt`, JSON-LD `headline` |
| `summary` | Meta description, `og:description`, the line under the H1, both listing cards, RSS description, `llms.txt`, JSON-LD `description` |
| `date` | Byline, sort order of every listing and feed, JSON-LD `datePublished`, RSS `pubDate` |
| `updated` | JSON-LD `dateModified`. The byline shows "Updated" only when it differs from `date` |
| `author` | Byline, the author line on the blog listing card, JSON-LD `author` (always typed `Organization`). `role` shows in the byline only |
| `tags` | Tag pages, RSS categories, JSON-LD keywords. Pills on the page for three slugs only |
| `takeaways` | The box above the body. Not in JSON-LD or the feeds |
| `faq` | A collapsible list at the bottom and a full `FAQPage` JSON-LD block |
| `cover` | `og:image` (after swapping `.svg` for `.png`) and the thumbnail on the `moi.technology/blog` listing. The blog's own listing never shows it |
| `draft: true` | Removes the post from the article route, listings, tag pages, feeds, `llms.txt` and the sitemap |

Gotchas, each silent:
- Only `agents`, `protocol` and `native-assets` show as pills (`NAV_TOPICS` in `Base.astro`). Any other tag still makes a `/tags/<tag>/` page and ships in feeds and keywords, and no link on the site reaches it. 19 tag pages exist for the 6 posts (local build of 2026-10-01).
- `updated` equal to `date` is a no-op in the byline. Set it only when the post changed after publication.
- `author.url` must parse as a URL. A bare domain fails the build.
- Dates are date-only and formatted in UTC. Write `date: 2026-09-11` and nothing more. The site does not hold back a future date: it publishes on merge.
- `author` is typed `Organization` in JSON-LD even for a person. Known defect. Do not fix it in a content PR.
- Fields the schema does not list (`description`, `authorRole`, `slug`) are ignored, and the missing `summary` then fails.
- Byline policy is open: "Sarva Labs, Engineering" (August, Voyage post) and "Adithya Ganesh, Ecosystem, Sarva Labs" (September) both shipped. ASK: Rahul.

## Body
- Start at `##`. The title is the H1, and a body `#` makes a second one. CONTENT.md says the opposite and is wrong.
- Make H2s questions where the section answers one: 52 of 67 H2s across the six posts end in a question mark. Answer in the section's first sentence. Do not turn every heading into a question (the docs standard says the same).
- Open with the claim, bold, in one declarative sentence. The September post opens "You can now pay fuel for another user." Three earlier openers were rejected in turn for being abstract, for vague nouns and for over-generalising (2026-09-11).
- Gloss every protocol term on first use. The August rewrite recorded a newcomer score moving from 61 to 87 after first-use glosses were added (the previous operator's skill; the six-lens jury is commit `90b7f8e`).
- Takeaways: exactly 8 or none. Five of six posts have 8. FAQ: 7 to 17 entries in the corpus. CONTENT.md's "2-4 questions" is wrong. Each answer goes verbatim into the `FAQPage` JSON-LD, so write it to stand alone.
- Close with `## Key takeaways, recap`: bullets with a bold lead clause. It is separate from the `takeaways` box. Write both.
- Do not put `<Subscribe />` in the body. The article page already renders the signup form after the FAQ, and in a `.md` file the tag is inert (a local build on 2026-10-01 rendered it as an inert `<subscribe>` element). The September post has one stray.
- Tables and code are styled. Code uses the `github-light` theme and there is no dark theme.
- Figures and images: `assets.md`.

## Voice
- Second person: "You scope what each agent can touch." Almost never "we". Declarative, short, one point per paragraph. Sentence-case headings. No emoji.
- Benefit first. Say what the developer can now do, put minimal code in, and link the docs for the how. August brief: "keep the blog explanatory, no need to have too much code, attach the docs link."
- Name the thing and use one word per concept: KMOI (defined once as the native token of the MOI network, then measured in anu), fuel (what is paid), fee payer (the role), fee delegation (the feature). Never "the token" or "the fee". <!-- slop-lint:ignore -->
- State no universal the protocol does not guarantee ("every action costs fuel" was removed, 2026-09-11). Say what the change covers: fee delegation pays fuel and nothing else. <!-- slop-lint:ignore -->
- Quote a release note verbatim where you use its words. Keep a release candidate as written (`0.9.0-rc2`) with no sentence about what a candidate is, and do not tell readers to upgrade to a version the operator has not confirmed as the latest compatible one.
- Say devnet, participant-centric, network ID, capped supply. Do not write "Voyage devnet". Wording tables: `moi-devrel/references/terminology.md`. The lint enforces most rows. <!-- slop-lint:ignore -->
- Positive framing: "mention it like that, don't use a negative" (2026-08-07, session 7 write-up). Keep claims inside what a check proves (a registry binds an identity to a wallet; it does not vouch for what an agent does with money).
- No cancelled plans, internal history, reviewer names or private repo paths in a public post (2026-08-31).
- Release posts: the inputs are the protocol team's note and the tagged versions. On 2026-08-14 Rahul asked every service owner to post `service:version:<github-link>` in Discord, because "the marketing team will use this to publish the release blog" (his words, as recorded). Cadence is one a month so far (inferred from two posts). No pictures and no cover (August decision). The September post cut its agents section to one line and dropped its x402 paragraph, and release posts make no x402 integration claim.

## Links and citations
- Link sibling posts by absolute URL, `https://blog.moi.technology/article/<slug>/`, with a trailing slash. Body links in a preview go to production too. A root-relative link resolves against whichever host serves the page, a preview included.
- Link on purpose: the SDK repo, the docs page for each tool, earlier posts. The 4 August 2026 strategy call asked for backlinks: "Don't load it up, but as much as possible."
- Cite public artefacts only: js-moi-sdk, `docs.moi.technology`, the explorer, behaviour you saw on the wire. `go-moi`, `go-pisa`, `cocolang` and the other private repos are for checking, never for linking.
- Open every external link before you open the PR. The September check found an access-policies link that returned 404.
- Descriptive link text, not "here". No UTM tags in the body: tagged links belong to the announcement (`distribution.md`).
- A transaction hash can link to the explorer. That was requested for the session 8 draft (`session-8-policies/BLOG.md`, a working branch of `moi-foundation/MOI-Webinars`), which still has plain code-fenced hashes.
- Posting to Medium first makes Medium the canonical copy. Is Medium still a channel? ASK: Rahul.

## Must contain, must not contain
Must: a `summary` of about 140 to 160 characters (the docs standard; the blog's own limit is not recorded, and the summary is also the meta description); a bold opening claim; first-use glosses; exact versions in a table for a release; a recap; links to docs and siblings; real output for any demo.
Must not: `<!--` comments (four were found once in the August post at `draft: false`, one a TODO inside a runbook step, and they blocked publishing until they were removed: commit `1d537dd`, 2026-08-19); `<<<`, `REPLACE-WITH`, `RELEASE_URL`, `TODO`; a `# ` heading; an em dash; "Voyage devnet"; a path from a local home folder; a hostname from a pull request preview; an unqualified "live". <!-- slop-lint:ignore -->

## Converting a session write-up
A Builders `BLOG.md` is a draft, not a blog file. The session 8 one was `session-8-policies/BLOG.md` on a working branch of `moi-foundation/MOI-Webinars`, not on `main`; it may no longer exist (not recorded; ASK: Rahul). Convert before it goes in `blog/src/content/posts/`:
| Webinar draft | Blog file |
|---|---|
| `description:` | `summary:` |
| `author: "Name"` and `authorRole:` | `author:` block with `name` and `role` |
| `slug:` | Delete. The file name is the slug |
| `tags: [access control, AI agents]` | Lowercase slugs: `["access-control", "agents"]` |
| `# Title` as the first body line | Delete. Start at `##` |
| An em dash in the title, `<<< EVIDENCE >>>` markers, `LUMA_URL` | Replace or remove. No cancelled-session mentions <!-- slop-lint:ignore --> |
Then run `python3 "$SKILLS/moi-blog/scripts/post-lint.py" blog/src/content/posts/<slug>.md`. The session itself belongs to `moi-webinar`. The target is a post within 48 hours of the session, and it was not shown met for session 8.

## CONTENT.md and the other guides are stale
The checked-in `CONTENT.md`, `DEPLOYMENT.md` and `blog/README.md` describe the blog wrongly. Corrected copies were never committed (not recorded: the previous DevRel's notes; ASK: Rahul). Until then trust the code.
| CONTENT.md says | The code does |
|---|---|
| `# This becomes h2` | `#` renders a second H1 |
| BlogPosting, BreadcrumbList and Organization schema with `wordCount` | `Article` and `FAQPage` only, author typed `Organization` |
| `author.role` makes a `Person` with role | Name and url only. `role` is in the byline only |
| Word count and reading time under the title | Reading time (`Math.round(words / 200)`, minimum 1) shows on the `moi.technology/blog` listing only |
| 2 to 4 FAQ items, 2 to 3 takeaways | Posts carry 7 to 17 and 8. Tags show only for three slugs |
| Text `#15102B`, muted `#5B5570` | `--ink #0a051a`, `--muted rgba(10, 5, 26, 0.62)`. Accent `--moi-main #4b17e5`, Poppins, light theme only |

## What checking has caught
Release notes were wrong in places, and the checks found it:
- 2026-08-19, `1d537dd`: `predictAssetId` and `predictLogicId` did not exist at v0.8.0 (`deriveAssetId` and `deriveLogicId` do), and `moi.Registry` was renamed `moi.Deeds`, not removed. Both errors came from the upstream release notes.
- 2026-08-21, `175a733`: 88 checking agents read 553 claims across two slicings, 521 were verified outright, and six narrow errors held up after adjudication (`VOLPAY` designates the storage payer, it does not charge; `AccessControl` is an interface). Two claims no check could settle were softened.
- 2026-09-11, `280ffb2`: 152 claims, three corrections (a link that returned 404, a paragraph that contradicted the participant-list rule, a recap bullet that dropped the notary exception).
When notes and source disagree and no one can rule, word the post so it contradicts neither and raise the difference separately (`5c0f763`). Do not silently pick a side.

## Not yet known
- The byline policy. ASK: Rahul.
- Whether and how a published post is amended (`updated`, a note, a new post). ASK: Rahul.
- Whether Medium is still a channel, and whether hashtags are used. ASK: Rahul.
- Whether the September post is amended for "Voyage devnet", the glossary line and the two sentences cut from the community call script on 2026-09-25. ASK: Rahul. <!-- slop-lint:ignore -->
- The October release date. None exists. ASK: Rahul.
