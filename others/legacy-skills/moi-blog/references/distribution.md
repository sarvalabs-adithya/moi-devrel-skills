# Social distribution

Publishing a post and announcing it are two separate acts in this repo, and the split is load-bearing. A post merges to `main`, CI ships it, and **nothing is sent**. Sending is a copy file a human writes plus a workflow a human triggers.

Two reasons, both from the commit that introduced the split (`23e92d8`): a post often needs a correction in the hour after it ships, and if distribution fired on merge the announcement is already gone; and copy auto-generated from the post's `summary` field reads generated, which is a negative signal to this audience.

## The loop

| Step | Who | What | Sends anything? |
| --- | --- | --- | --- |
| 1 | CI (`social-prepare.yml`) | Post file added to `main` → opens a PR adding `social/<slug>.md`, one editable block per channel | No |
| 2 | Human | Rewrites the copy in that PR, merges it | No |
| 3 | Human | Actions → **Distribute a post** → Run workflow | Yes (dry run defaults on) |

Steps 1 and 3 never touch each other. `distribute.yml` has **no push trigger**: `workflow_dispatch` only (`.github/workflows/distribute.yml:16-37`).

## Files

| Path | Role |
| --- | --- |
| `social/README.md` | The contributor-facing version of this document |
| `social/<slug>.md` | Per-post copy, one YAML literal block per channel |
| `scripts/social-init.js` | Creates the copy file (scaffold) |
| `scripts/distribute.js` | The CLI that plans and sends |
| `scripts/lib/social.js` | Channel registry, copy file read/write, `{{link}}`, length measurement, `planFor()` |
| `scripts/lib/senders.js` | The four transports (Discord, Telegram, Buffer ×2) |
| `scripts/lib/share.js` | Post frontmatter reader + `shareUrl()`; re-exports the UTM convention |
| `blog/src/lib/utm.js` | The UTM convention itself: single definition |
| `scripts/share-links.js` | Prints tagged links for a post (no sending) |
| `scripts/buffer-channels.js` | One-off: prints Buffer channel IDs for the secrets |
| `.github/workflows/social-prepare.yml` | Step 1 |
| `.github/workflows/distribute.yml` | Step 3 |

## The copy file

`social/what-is-moi-network.md`, verbatim shape:

```yaml
---
slug: what-is-moi-network
title: "What Is MOI Network? The Participant Layer That Provides On-Chain Authority"
published: 2026-08-18

# Discord and Telegram post immediately. X and LinkedIn are queued in
# Buffer as drafts for you to approve. Empty a channel to skip it.

discord: |
  **What Is MOI Network? ...**

  MOI Network makes participants native to computation: ...

  {{link}}

telegram: |
  ...
# X allows 280 characters. The link counts as 23 whatever its length.
x: |
  ...
linkedin: |
  ...
---

<!-- ... -->

Notes: none yet.
```

Blocks are emitted as YAML **literal** style (`|`), never folded and never through a YAML dumper (see `scripts/lib/social.js:97-98`):

```js
const block = (key, text) =>
  `${key}: |\n` + String(text).split('\n').map((l) => (l ? `  ${l}` : '')).join('\n');
```

Folded style collapses the blank lines between paragraphs, and this file exists to be edited by hand.

The markdown body after the closing `---` is parsed into `social.notes` (`scripts/lib/social.js:88`) and **never read by anything**. It is a human scratchpad; do not put machine-relevant state there.

### Format rules that bite

- **Empty a channel to skip it.** `renderCopy` trims and returns `''` for blank; `planFor` then marks the channel `no copy` (`social.js:76-82`, `:174`). Deleting the key does the same. There is no `enabled:` flag.
- **Indentation ends the block.** A continuation line indented less than the first content line terminates the literal block. YAML will either throw in `gray-matter` (the run dies with a parse error before anything sends) or silently hand you truncated copy. Keep every non-blank line at exactly two spaces.
- **`#` inside a block is content, not a comment.** Only `#` lines at frontmatter top level are comments.
- **`{{link}}` is optional but always present in the output.** If the token is absent, the tagged URL is appended with a blank line (`social.js:81`). You cannot ship a link-less post by deleting it: that failure mode is defended against on purpose.

## Channels

Registry: `scripts/lib/social.js:23-58`.

| id | Label | kind | On send | Limit | Required env |
| --- | --- | --- | --- | --- | --- |
| `discord` | Discord | `direct` | Posts immediately via webhook | 2000 | `DISCORD_WEBHOOK_URL` |
| `telegram` | Telegram | `direct` | Posts immediately via Bot API | 4096 | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` |
| `x` | X | `buffer` | Created in Buffer as a **draft** | 280 | `BUFFER_ACCESS_TOKEN`, `BUFFER_CHANNEL_X` |
| `linkedin` | LinkedIn | `buffer` | Created in Buffer as a **draft** | 3000 | `BUFFER_ACCESS_TOKEN`, `BUFFER_CHANNEL_LINKEDIN` |

Discord and Telegram are announcement channels where a bot posting is expected. X and LinkedIn are not, so the pipeline stops at a draft and a person approves in Buffer.

### The draft guarantee

`scripts/lib/senders.js:81-93`: the draft state rides on the API call, not on Buffer's per-channel approval toggle:

```js
const input = {
  text: copy,
  channelId,
  schedulingType: 'automatic',
  mode: 'addToQueue',
  saveToDraft: true,
};

// Belt and braces: if a refactor ever drops saveToDraft or reaches for a
// publishing mode, fail loudly here rather than quietly posting.
if (input.saveToDraft !== true || input.mode !== 'addToQueue') {
  throw new Error('Refusing to send: Buffer posts must be drafts.');
}
```

Buffer's `shareNow`/`shareNext` modes are not reachable from this code and are not exposed as an env var or workflow input. Enabling one is meant to cost a code change and a PR. Do not "helpfully" add a `--publish` flag.

The `createPost` mutation selects `__typename` plus every error member of the union (`senders.js:62-75`), so an unrecognised Buffer error surfaces as itself rather than as a silent success.

### Discord and Telegram transport details

- Discord posts `content` (not an embed) with `allowed_mentions: { parse: [] }` (`senders.js:17`): `@everyone` in your copy will render but will **not** ping. Discord markdown (`**bold**`) works.
- Telegram HTML-escapes the whole message and then sets `parse_mode: 'HTML'` (`senders.js:25-40`). Net effect: **plain text only**. `<b>` arrives as literal `&lt;b&gt;` and `**bold**` arrives as literal asterisks. Write the Telegram block unstyled.

## Character limits

Over-length copy **blocks** the send; it is never truncated (`distribute.js:69-75`). Silently cutting someone's sentence is worse than making them shorten it. A blocked channel makes the process exit 1.

X's limit is measured the way X measures it: every URL costs 23 characters regardless of length (`social.js:148-154`):

```js
const T_CO_LENGTH = 23;
export function measure(copy, channel) {
  if (channel.id !== 'x') return copy.length;
  return copy.replace(/https?:\/\/\S+/g, 'x'.repeat(T_CO_LENGTH)).length;
}
```

The regex only matches URLs carrying a scheme, so `{{link}}` output, always `https://…`, is measured correctly at 23. A hand-typed bare domain is measured at its literal length instead: `measure('moi.technology', channelById('x'))` returns 14 while X charges 23 for it (`.technology` is a valid gTLD, so X extracts the bare domain as a URL). Short schemeless URLs are therefore **under**-counted and the check can pass copy X will reject; long ones are over-counted. Do not treat the X check as conservative when the copy contains schemeless URLs, write links with `https://`, or leave them to `{{link}}`.

## UTM tagging

`blog/src/lib/utm.js` is the single definition, imported by the Astro blog (through Vite) **and** by the root scripts (plain Node, no bundler). It is dependency-free for exactly that reason: adding a `node:fs` import or an npm dependency breaks one of the two consumers.

```js
export const CHANNELS = [
  { source: 'x',          medium: 'social',      label: 'X' },
  { source: 'linkedin',   medium: 'social',      label: 'LinkedIn' },
  { source: 'discord',    medium: 'community',   label: 'Discord' },
  { source: 'telegram',   medium: 'community',   label: 'Telegram' },
  { source: 'newsletter', medium: 'email',       label: 'Newsletter' },
  { source: 'devto',      medium: 'syndication', label: 'dev.to' },
  { source: 'reddit',     medium: 'social',      label: 'Reddit' },
];
```

Rules encoded there:

- `utm_medium` is a property of the channel, never a per-post choice.
- **`utm_campaign` is always the slug.** That is what lets one post be compared across channels and one channel across posts from a single GA4 report. Anything else and the report stops being comparable.
- Casing is the contract, not style: GA4 treats `linkedin` and `LinkedIn` as different channels.
- `utm_content` separates a day-7 push from the day-0 one. **The distribution pipeline never sets it**: `linkFor()` calls `shareUrl(slug, channel)` with no `content` (`social.js:70-72`). Only `scripts/share-links.js` emits a `day7` variant. A repost sent through `npm run distribute` therefore lands in the same GA4 bucket as day 0; paste the `day7` link by hand if you need them separated.

Base URL: `ORIGIN` is `process.env.BLOG_ORIGIN || 'https://blog.moi.technology'` (`scripts/lib/share.js:17`); links are `${ORIGIN}/article/${slug}/?utm_...`. Neither workflow sets `BLOG_ORIGIN`, so it is only a local-testing lever: set it locally and your dry run shows staging URLs. It reaches exactly two things: URLs rendered at send time, and the output of `build-blog-index.js` (`scripts/build-blog-index.js:32`), which lands in `dist/` and `public/blog/`: both gitignored. Copy files are unaffected: `scaffold()` writes the literal `{{link}}` token and never calls `shareUrl()`, so a copy file is byte-identical whatever `BLOG_ORIGIN` was set to.

Real output for `what-is-moi-network`:

```
X           https://blog.moi.technology/article/what-is-moi-network/?utm_source=x&utm_medium=social&utm_campaign=what-is-moi-network
Discord     https://blog.moi.technology/article/what-is-moi-network/?utm_source=discord&utm_medium=community&utm_campaign=what-is-moi-network
X (day 7)   https://blog.moi.technology/article/what-is-moi-network/?utm_source=x&utm_medium=social&utm_campaign=what-is-moi-network&utm_content=day7
```

## The workflow route

### Prepare social copy (`social-prepare.yml`)

Triggers on push to `main` touching `blog/src/content/posts/**.md`, plus manual dispatch with optional `slug` and `force` inputs. Permissions: `contents: write`, `pull-requests: write`.

- On push it diffs `--diff-filter=A` over `blog/src/content/posts/*.md` (`:61-63`): **only newly added files count**. Editing a published post never produces a copy file, and never re-announces.
- It runs `node scripts/social-init.js <slugs>`, which writes `created=` and `slugs=` to `$GITHUB_OUTPUT` (`social-init.js:44-48`); the PR step is gated on `created != '0' && created != ''`.
- Branch is `social/<first-slug>-<run_id>`; the PR is opened with `gh pr create` using `secrets.GITHUB_TOKEN`.
- No loop risk: the path filter matches only post files, and the PR only touches `social/`.

### Distribute a post (`distribute.yml`)

`workflow_dispatch` only. Inputs:

| Input | Type | Default |
| --- | --- | --- |
| `slug` | string, required | none |
| `channels` | choice: `all`, `discord`, `telegram`, `x`, `linkedin`, `discord,telegram`, `x,linkedin` | `all` |
| `dry_run` | boolean | **`true`** |

The run step (`:62-70`):

```bash
# Without pipefail the exit code is tee's, and a failed send would
# show as a green run.
set -o pipefail
FLAGS=""
[ "${{ inputs.dry_run }}" = "true" ] && FLAGS="$FLAGS --dry-run"
[ "${{ inputs.channels }}" != "all" ] && FLAGS="$FLAGS --only=${{ inputs.channels }}"

node scripts/distribute.js "${{ inputs.slug }}" $FLAGS | tee run.log
```

`set -o pipefail` is present and is the whole reason a failed send turns the run red. If you ever refactor this step, the pipe into `tee` is what makes it necessary: dropping `pipefail` while keeping `tee` restores the green-on-failure bug. A `Summary` step (`if: always()`) dumps `run.log` into `$GITHUB_STEP_SUMMARY`.

Permissions: `contents: read`. Secrets are injected as env on that step only.

## Locally

```bash
npm run social:init  <slug>                      # create the copy file
npm run social:init  <slug> -- --force           # overwrite an existing one
npm run social:init  -- --all                    # every published post missing one
npm run distribute   <slug> -- --dry-run
npm run distribute   <slug> -- --only=discord,telegram
npm run social:links <slug>                      # tagged links, no sending
npm run social:links <slug> -- --md              # markdown checklist
BUFFER_ACCESS_TOKEN=... npm run buffer:channels  # print Buffer channel IDs
```

All four scripts exist in `package.json` under those exact names. Passing the slug before `--` works: npm forwards both.

Real dry-run output on a machine with the secrets present:

```
What Is MOI Network? The Participant Layer That Provides On-Chain Authority
social/what-is-moi-network.md   [dry run: nothing will be sent]

– Discord   would send 360/2000  "**What Is MOI Network? The Participant Layer That Provides On-…"
– Telegram  would send 357/4096  "What Is MOI Network? The Participant Layer That Provides On-Ch…"
– X         would send 173/280  "MOI Network makes participants native to computation: authorit…"
– LinkedIn  would send 354/3000  "What Is MOI Network? The Participant Layer That Provides On-Ch…"

0 sent, 4 skipped, 0 blocked, 0 failed
```

The real script prints an em dash after `dry run` in that header; it is shown here as a colon.

Status marks: `✓` sent, `–` skipped, `!` blocked (over length), `✗` failed. Exit code is 1 if anything was blocked or failed, 0 otherwise (`distribute.js:104`).

### `buffer:channels`

Buffer surfaces channel IDs nowhere in its web UI; the GraphQL API is the only route. Two shapes were wrong on the first attempt and are documented in the file header (`scripts/buffer-channels.js:7-9`): `organizations` hangs off `account`, not the root, and `channels(input:)` types `organizationId` as `OrganizationId!`, not `String!`. The script also selects `isDisconnected`, so a channel that has quietly dropped its connection shows up rather than failing later at send time. It maps Buffer's `service` value (`twitter` **or** `x`) to `BUFFER_CHANNEL_X`.

## Secrets

Repository secrets, not a local `.env`. Documented in `.env.example:11-27`.

| Secret | Channel | Where it comes from |
| --- | --- | --- |
| `DISCORD_WEBHOOK_URL` | Discord | Server Settings → Integrations → Webhooks → New Webhook |
| `TELEGRAM_BOT_TOKEN` | Telegram | @BotFather `/newbot` |
| `TELEGRAM_CHAT_ID` | Telegram | Bot must be added to the channel as an admin |
| `BUFFER_ACCESS_TOKEN` | X + LinkedIn | Only a Buffer **organisation owner** can create one |
| `BUFFER_CHANNEL_X` | X | `npm run buffer:channels` |
| `BUFFER_CHANNEL_LINKEDIN` | LinkedIn | `npm run buffer:channels` |

A channel whose secrets are absent is **skipped and named**, not failed (`social.js:158-177`, `planFor`). A half-configured setup is a usable state: switch channels on one at a time.

## Gotchas

- **A local dry run without secrets tells you nothing about length.** `planFor` computes `skip` (no copy / missing creds) before `distribute.js` ever evaluates `over` or the dry-run preview, so with no env set you get four `missing …` lines and exit 0. That looks like a clean dry run and is not one. To actually rehearse locally, set the six vars to dummy values: the dry run never issues a request:
  ```bash
  DISCORD_WEBHOOK_URL=x TELEGRAM_BOT_TOKEN=x TELEGRAM_CHAT_ID=x \
  BUFFER_ACCESS_TOKEN=x BUFFER_CHANNEL_X=x BUFFER_CHANNEL_LINKEDIN=x \
  node scripts/distribute.js <slug> --dry-run
  ```
- **A dry run in CI *does* catch over-length**, because `over` is checked before the dry-run branch and forces exit 1. Trust a red dry run; do not trust a green local one done without env.
- **`social:init` requires the post to exist.** `scaffold()` throws `No post found for slug: …` if `blog/src/content/posts/<slug>.md` is missing (`social.js:101-102`). The slug is the filename minus `.md`, nothing else.
- **`--all` and `distribute` both respect `draft: true`.** `readPosts()` filters drafts out (`share.js:42`); `distribute.js:39-42` exits 0 with "still a draft" followed by an em dash and "nothing to distribute". A draft post silently produces no announcement, which is correct but looks like a bug if you were expecting one.
- **Re-running Distribute re-sends.** There is no idempotency, no "already sent" record. Discord and Telegram will post a second time; Buffer will create a second draft. The dry-run default is the only guard.
- **Editing a published post never regenerates copy.** `--diff-filter=A` sees adds only. Use the manual dispatch on `social-prepare.yml` with `force: true`, or `npm run social:init <slug> -- --force`, which overwrites your hand-written copy without asking.
- **Unknown channel names fail fast.** `--only=twitter` exits 1 with `Unknown channel(s)`: the ids are `discord, telegram, x, linkedin`.
- **`utm_source=newsletter`, `devto` and `reddit` have links but no sender.** They exist in `utm.js` for `share-links.js` output and for the newsletter feed; asking `distribute` for them is an unknown-channel error.
- **Per-channel failures do not stop the run.** Each send is wrapped in try/catch (`distribute.js:84-91`); a Discord 429 still lets Telegram through, and the exit code carries the failure.

## The newsletter is not in this pipeline

Deliberately out of scope: Mailchimp runs an RSS campaign against `blog/src/pages/rss-email.xml.js` on its own schedule. No code path, no secrets, no workflow step here.

`rss-email.xml` exists as a **second** feed rather than tagging `rss.xml` in place, because feed readers are not the newsletter and filing their traffic under `medium=email` would be worse than leaving it untagged. Its `<link>` values are pre-tagged with `utm_source=newsletter&utm_medium=email&utm_campaign=<slug>` because Mailchimp copies each item's link verbatim, and Mailchimp's own Google Analytics option names `utm_campaign` after the Mailchimp campaign, which breaks the slug convention rather than serving it. Point Mailchimp at `/rss-email.xml`, leave `/rss.xml` for readers.

## Operational notes (not verifiable from the repo)

Treat these as institutional memory, not facts checked against code:

- Buffer is used instead of the platform APIs for reasons specific to 2026, recorded in `cc6ddf1`'s commit message: X ended its free tier in February and bills per post containing a link (every post here contains one), and LinkedIn company-page posting requires approval under the Marketing Developer Platform partner programme, which takes months. Buffer's free tier carries approved integrations for both and holds the X connection, which otherwise means sharing a password, since X has no per-person roles.
- The Mailchimp list is stated in `cc6ddf1` as roughly 5.5k subscribers. Not checkable here.
- The cadence has two in-repo statements and they disagree. `social/README.md:96` says Mailchimp polls `/rss-email.xml` **weekly**; `cc6ddf1` says an RSS campaign "mails each new post automatically", i.e. **per post on publish**. Neither is checkable here, and the send schedule lives in the Mailchimp campaign settings: check there before quoting either.
- Buffer's API key can only be created by an organisation owner. If `buffer:channels` returns 401, that is the likely cause, not a typo.
- The Telegram bot must be an admin of the target channel for `sendMessage` to succeed with a channel `chat_id`.
