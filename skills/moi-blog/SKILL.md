---
name: moi-blog
description: "Write, publish and announce a post on blog.moi.technology, run its Mailchimp newsletter, and announce a MOI protocol release from the protocol team's note. Use for \"write a blog post\", \"post-session blog\", \"write-up of a Builders session\", \"publish the post\", \"blog pull request\", \"announce the post\", \"social copy for the post\", \"Distribute a post\", \"Buffer draft\", \"Mailchimp newsletter\", \"RSS campaign\", \"weekly email blast\", \"cover image for a post\", \"make the post findable by search and AI assistants\", or any edit under blog/src/content/posts in sarvalabs/MOI-Website. Also for \"release note\", \"protocol release\", \"moipod v0.13.0\", \"release thread\", \"announce the release\", \"announce an upgrade\", \"release announcement\", \"release post\", \"wrong release time\" and \"correction reply\": the release-pack branch drafts the X thread, LinkedIn and Discord posts and the release post, then this skill publishes the post. A session is moi-webinar, art outside a post moi-devrel/design, site-wide search moi-docs/geo."
---

# MOI blog

## What this covers
One post on `blog.moi.technology`, from the brief to the newsletter: write it, check every claim, polish it, ship it as a pull request to `sarvalabs/MOI-Website`, check the live page, announce it on X and LinkedIn as drafts a person publishes, and check the email that Mailchimp builds from the feed (a one-off email is drafted here and sent by the operator). Merging a post deploys it and announces nothing. Every later step is a separate action that needs the operator's yes. Facts are as of 2026-10-02.
Branch: `moi-blog/release-pack` takes a protocol release from the protocol team's note to the announcement pack (X thread, LinkedIn, Discord) and the release post, and handles a wrong release time. It runs in a working copy of `moi-foundation/MOI-Webinars`, not here, and hands its finished post to the run below (`release-pack/GUIDE.md`). A protocol release starts in that guide, not at the checklist below.
Not covered here: a Builders session from topic to write-up (`moi-webinar`), claim ledgers (`moi-devrel/claim-check`), commits, pull requests, rebases and merges in general (`moi-devrel/ship`), decks (`moi-webinar/deck`), art outside a post (`moi-devrel/design`), docs pages (`moi-docs`), the search layer of every site (`moi-docs/geo`; `references/geo.md` here holds what a post needs), and the website's own ship, health, content and calendar runbooks (`moi-web-products-ops`). House rules, terminology, people and keys are `moi-devrel`.

## Before you start
"The operator", "the previous operator" (Adithya Ganesh) and `ASK:` are defined in `moi-devrel/SKILL.md`. `$SKILLS` is the folder that holds the `moi-*` skills. Run every command from your working copy of `sarvalabs/MOI-Website`, the website repo, except `scripts/buffer.mjs`, which is in a clone of `moi-foundation/MOI-Webinars` (`references/buffer.md`). The website repo is public: a push publishes. `<slug>` is the post's file name without `.md`, lowercase words and hyphens, and the last part of its URL. Set `WORK` once to a folder outside the clone (`WORK="$HOME/moi-blog-work"; mkdir -p "$WORK"`) for the claim ledger and the announcement record: a ledger's source column may name private repos, and the clone is public.
Terms. *Frontmatter*: the settings block at the top of a post, between two lines of three dashes. *Ledger*: a CSV with one row per claim and a verdict (`moi-devrel/claim-check`). *Preview*: a copy of the site that GitHub Actions builds for each pull request. *Prepare* and *Distribute*: the GitHub Actions workflows "Prepare social copy" and "Distribute a post". *Buffer*: the service that holds X and LinkedIn drafts. *Feed*: the `rss-email.xml` file Mailchimp reads to email new posts. *UTM tags*: link parameters that Google Analytics reads to name the channel. *GEO*: making a post readable and citable by search engines and AI assistants. *JSON-LD*: structured data in a page that search engines read. *Canonical*: the page's official address. *llms.txt*: a plain-text list of posts for AI assistants. Protocol words (KMOI, fuel, anu, MASN): `moi-devrel/references/glossary.md`.
- [ ] The brief: audience, what the reader can do after reading, the genre, the day it goes live. The operator. Ask: "Who is this for, and what can they do afterwards?"
- [ ] Sources: the tagged versions and docs pages the post names; for a session write-up, the session folder and its real demo output; for a release, the pack's inputs (`release-pack/GUIDE.md`).
- [ ] Reviewer: the September pull request names Rahul as the internal reviewer and says the post was framed per the internal review. Who else approves and who merges is not recorded. ASK: Rahul.
- [ ] Byline: "Sarva Labs, Engineering" and a named author have both shipped. ASK: Rahul which to use.
- [ ] A clone of `sarvalabs/MOI-Website`, Node 22 (`node --version`), your work identity (`bash "$SKILLS/moi-devrel/scripts/preflight.sh"` from inside it). A clone and `npm ci` download files: say the source and wait for a yes. ASK: Rahul how write access is granted.
- [ ] To announce: Buffer access and the Actions secrets for the channels you will use (`references/buffer.md`). For the newsletter: a Mailchimp login that the operator holds. Claude never types a password. Owners of both accounts are not recorded. ASK: Rahul.

## The run
Time: the September release post took about 24 hours from opening the PR to the merge, and the August one about 2.5 days, mostly review-driven rewrites (the PR record). Plan for review rounds, not for typing.
Where the branch takes over: a protocol release starts in `release-pack/GUIDE.md` and joins this table at step 3. Its finished `BLOG.md` replaces the skeleton there, its `ledger.csv` is put at `$WORK/<slug>/ledger.csv` before step 4 so `cp -n` keeps its verdicts, and steps 4 to 11 are the same.

| # | Step | What to do | Where or command | Done when |
|---|---|---|---|---|
| 1 | Brief and angle | One line: what the developer can now do. Pick a genre and read its sibling post. Check no post already covers it | `references/authoring.md`, `templates/post-skeleton.md` or `templates/release-post-skeleton.md` | The operator approves angle and title |
| 2 | Sources | List the tagged versions and docs links the post names (a release pack has already saved the note: `release-pack/GUIDE.md`, steps 1 and 2). For any "live" claim read the node | `moi-devrel/references/devnet.md` "Before you say live" | Every claim has a source in hand |
| 3 | Draft | GATE: `git fetch origin` and, once, `npm ci` then `npm ci --prefix blog` download files: name the source and wait for a yes. Then `git switch --no-track -c blog/<slug> origin/main`. Copy a skeleton in (a release post: the pack's finished `BLOG.md`), fill every marker, frontmatter first. Local only | `cp "$SKILLS/moi-blog/templates/post-skeleton.md" blog/src/content/posts/<slug>.md` (a release: `release-post-skeleton.md`); `references/authoring.md`, `references/assets.md` | `npm run dev --prefix blog` shows it at localhost:4321 |
| 4 | Claim check | Follow `moi-devrel/claim-check`, with the ledger in `$WORK`, not in the clone (a stray `git add` would publish it). `--all` lists every sentence, because the default run skips plain statements. Extract once, delete rows that state nothing checkable, give each kept row a source and a verdict, change the text to match, run the re-check | `mkdir -p "$WORK/<slug>"`; `python3 "$SKILLS/moi-devrel/claim-check/scripts/extract-claims.py" --all blog/src/content/posts/<slug>.md > "$WORK/<slug>/claims-candidates.csv"`; `cp -n "$WORK/<slug>/claims-candidates.csv" "$WORK/<slug>/ledger.csv"`; then `python3 "$SKILLS/moi-devrel/claim-check/scripts/extract-claims.py" --all --against "$WORK/<slug>/ledger.csv" --dropped "$WORK/<slug>/claims-candidates.csv" blog/src/content/posts/<slug>.md` and `python3 "$SKILLS/moi-devrel/claim-check/scripts/ledger-status.py" "$WORK/<slug>/ledger.csv"` | Both exit 0: nothing new in the text, no row unverified or unsourced |
| 5 | Polish | The passes in order. Re-read the opener after every automated pass | `references/polish.md` | `python3 "$SKILLS/moi-blog/scripts/post-lint.py" --strict blog/src/content/posts/<slug>.md` exits 0. Strict mode fails a title over 60 characters or a summary outside 130 to 170: no limit is recorded for the blog, so keep one on purpose only with Rahul's yes (ASK: Rahul) |
| 6 | Local builds | Both builds, then the operator reads the whole post once | `npm run build --prefix blog`, then `npm run build` | Both exit 0 and the operator has read it |
| 7 | Pull request | Commit under the work identity with no AI trailer: `git add blog/src/content/posts/<slug>.md` (and `blog/src/assets/<slug>/`), `git commit -m "blog: <what>"`. Show branch, files, remote and account. GATE: push and open one PR (a push to the public repo publishes the branch). Wait for the preview | `templates/pr-body.md`, `references/publishing.md`; the general mechanics are `moi-devrel/ship` | The preview at `pr-<N>-blog.preview.moi.technology` is read and Rahul has reviewed |
| 8 | Merge and live check | GATE: merge, only on a yes that names the PR (this deploys). Wait for the deploy run to finish, then check the page itself. The website's own deploy path and health script: `moi-web-products-ops/references/website-ship.md`, `website-health.md` | `gh run list --repo sarvalabs/MOI-Website --workflow "Deploy MOI Website" --limit 3`; then `python3 "$SKILLS/moi-blog/scripts/check-live.py" <slug>` | Exit 0. A green deploy run proves nothing |
| 9 | Announce | Find the copy PR that Prepare opened after the merge and rewrite its copy by hand. GATE: merging the copy PR; each Distribute run, a dry run included, then one real run (no undo); running `scripts/buffer.mjs` in any form; the Buffer drafts. A person publishes | `references/distribution.md`, `references/buffer.md`, `templates/announce/`; `python3 "$SKILLS/moi-blog/scripts/copy-lint.py" social/<slug>.md` from that PR's branch | The lint shows no error, drafts exist, the operator published, the record is filled |
| 10 | Newsletter | Find out whether the weekly feed campaign is running before building anything. One-off sends are separate. GATE: anything in Mailchimp, a test send included | `references/newsletter.md` | The campaign state is written down |
| 11 | Hand-back | The format at the end of this file | Hand-back | The operator has read it |

## Which file to read
| Doing | Read |
|---|---|
| Structure, voice, frontmatter, links, what a post must and must not hold | `references/authoring.md` |
| The passes run on real posts, and the rules without any helper skill | `references/polish.md` |
| Branch, PR, previews, build and deploy path, live checks, what is broken | `references/publishing.md` |
| The website's own ship path, health after a deploy, a page or paper, the calendar | `moi-web-products-ops/SKILL.md` |
| Images, covers, logos, the cache rule | `references/assets.md` |
| Search and AI-visibility rules for a post, measurement | `references/geo.md` |
| Announcing: copy file, workflows, every gate | `references/distribution.md` |
| Buffer: the two tools, the two key names, what `scripts/buffer.mjs` does not do | `references/buffer.md` |
| The weekly email and one-off sends, templates, what is confirmed | `references/newsletter.md` |
| Every trap in one list | `references/traps.md` |
| Testing a change to this skill | `evals/evals.md`, then `python3 "$SKILLS/moi-blog/scripts/selftest.py"` |
| A finished post to learn from | `examples/README.md` |

**Branch `release-pack`**, read its `GUIDE.md` first:

| Asked to | Read |
|---|---|
| Turn a protocol team release note into the announcement pack and the release post; "release thread", "announce the release", "release post" | `release-pack/GUIDE.md` |
| Keep the note verbatim, or draft the questions for the protocol team | `release-pack/GUIDE.md`, then `release-pack/references/the-note.md` |
| Schedule or draft the pre-release X thread, LinkedIn and Discord posts | `release-pack/GUIDE.md`, then `release-pack/references/announcement-pack.md` |
| A release time or any posted statement was wrong; "correction reply" | `release-pack/GUIDE.md`, then `release-pack/references/corrections.md` |
| Testing a change to the release pack | `release-pack/evals/evals.md` |
| Publish a finished release post, announce it, the newsletter | The run above, from step 3 |

## Facts that fail silently
| Rule | The incident |
|---|---|
| Run both builds. Only the blog build checks frontmatter | `scripts/build-blog-index.js` reads frontmatter with `gray-matter` and never runs the schema, so a missing `summary` becomes `undefined` in the listing card and the build exits 0. A post can then be live but unlisted, or listed and missing |
| Merge deploys and announces nothing. After any merge or delete, read the live page | August 2026: deleted posts survived deploys because the VM script ran `npm install` instead of `npm ci --prefix blog` (2026-08-18). Run `python3 "$SKILLS/moi-blog/scripts/check-live.py" <slug> --expect-gone` after a delete |
| Merge the Prepare PR before you run Distribute | `distribute.yml` reads `main` and stops with "No copy file". PR #56, the September copy, is still open as of 2026-10-02 and no announcement of that post is on record |
| Run Distribute for real once | Another run posts to Discord and Telegram again and makes a second Buffer draft. There is no undo |
| Empty the Discord and Telegram blocks by hand | The scaffold seeds all four channels with the post summary. The previous operator decided on 2026-08-31 on X and LinkedIn only |
| A post scheduled with `scripts/buffer.mjs` publishes unreviewed. The website pipeline only drafts | 2026-09-10: a midnight release time was misread as noon and two scheduled posts were deleted by hand |
| Two Buffer key names: `BUFFER_ACCESS_TOKEN` and `BUFFER_API_KEY` | A Buffer key was pasted in chat on 2026-08-31 and revoked. Never open an `.env` |
| A release note is a lead, not evidence | August 2026: the checks found wrong API names and a wrong "removed" claim (commit `1d537dd`, 2026-08-19) |
| Read "live on devnet" from the node, never from the source tip | 2026-09-10: devnet still ran 0.12.0 and `payer` while the source had `fee_payer` |
| Wording the previous operator rejected: "the token", "the fee", "every action costs fuel", "Voyage devnet", "fixed supply" | 2026-09-11 and 2026-09-25. As of 2026-10-02 the published September post still holds "Voyage devnet" and an old glossary line <!-- slop-lint:ignore --> |
| `utm_campaign` is the slug in lowercase. Mailchimp's own Google Analytics option stays off | GA4 files `LinkedIn` and `linkedin` as two channels |
| An image used in email or a share card gets a new filename every time it changes | 2026-08-24: three pull requests to learn it (`b8c3dea`, `85629a5`, `b150873`) |
| No `cover` means no social card. An SVG cover without its PNG points `og:image` at a missing file | No post on `main` sets `cover` as of 2026-10-02 |
| A webinar `BLOG.md` is not a blog file | Its frontmatter (`description`, `authorRole`, string `author`) fails the build, and its `# ` heading doubles the H1 |
| The checked-in guides `CONTENT.md`, `DEPLOYMENT.md`, `blog/README.md` are stale. Trust the code and this skill | Corrected copies are uncommitted on the previous operator's machine. ASK: Adithya for a copy |
| Never commit the ledger, the announcement record or a draft that names a private repo | `sarvalabs/MOI-Website` is public |
More in `references/traps.md`. The release traps are in `release-pack/references/traps.md`.

## Gates
Nothing below happens without the operator's explicit yes in this conversation, naming the action:
- Push, open, update or close a pull request, merge. A pull request preview is a URL that lasts until the PR closes or 7 days pass. Whether it is restricted is not recorded. ASK: Upendhar.
- Run any workflow: Prepare social copy, Distribute a post, Deploy MOI Website. A dry run is a run. The real Distribute run needs its own yes.
- Running `scripts/buffer.mjs` in any form, a dry run included (it sends the key to Buffer), is a GATE. So is creating, editing or scheduling anything in Buffer, and every post to X, LinkedIn, Discord, Telegram or Medium. The reasons are in `references/buffer.md`.
- Anything in Mailchimp: building or starting a campaign, "Send now", a test send, a change of audience.
- Request indexing in Search Console or Bing, or an IndexNow ping.
- Uploading or sharing a file in cloud storage. Downloading a file, which includes `git clone`, `git fetch` and `npm ci`: say its name, source and size.
- Setting or changing an Actions secret or variable. The operator types the value at a hidden prompt.
- Spending devnet funds or deploying on devnet to check a claim: a wallet step, so the operator signs and runs it. Switching the git or `gh` identity.
- Sub-agents, bulk model runs and paid APIs: only when the operator names them, with the count and model stated first.
- Sending a message to Rahul or anyone else: Claude drafts, the operator sends.

## Keys and access
Names only. Writing and building a post needs no key. Where each lives, who grants it and its status: `moi-devrel/references/keys-and-access.md`.
- Actions secrets on `sarvalabs/MOI-Website`: `BUFFER_ACCESS_TOKEN`, `BUFFER_CHANNEL_X`, `BUFFER_CHANNEL_LINKEDIN`, `DISCORD_WEBHOOK_URL`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`. Used by "Distribute a post".
- `BUFFER_API_KEY`: a local `.env` at the root of `moi-foundation/MOI-Webinars`, for `scripts/buffer.mjs` only. A different tool and a different name.
- Logins with no repo secret: Mailchimp, Google Analytics and Tag Manager, Search Console, Bing, Buffer, Medium. Owners are not recorded. ASK: Rahul. The operator logs in and reads the screen to you. Claude never types a password.
- Website admin, which is not part of the blog's work:
  - Website: A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin.
- Recovery phrases: Claude never handles one, including a throwaway one.

## Hand-back
```
Produced: <post path, PR number and URL, live URL, ledger path, announcement record path>
Remaining: <numbered, each with who owns it>
Not verified or simulated: <ledger rows not verified, anything not read on the live page, or "none">
Ready: yes or no, because <one reason>
Next steps: <one to three>
```
Ready is no while a ledger row is unverified, `post-lint.py --strict` or `copy-lint.py` shows an error, the preview was not read, or `check-live.py` shows a FAIL. List every open `ASK:` line. A release also gives the pack's own hand-back (`release-pack/GUIDE.md`).
