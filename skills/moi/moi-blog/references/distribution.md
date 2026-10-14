# Announcing a published post

Facts are as of 2026-10-02, confirmed against `.github/workflows/` and `scripts/` in `sarvalabs/MOI-Website` on `main` (commit `5e91afa`). Back to `../SKILL.md`. Publishing a post and announcing it are two separate acts, on purpose: a post often needs a correction in the hour after it ships, and copy generated from the `summary` field reads generated, which this audience notices. So nothing is sent by merging, and a person writes the words and a person presses publish.
A manager rule from 24 August 2026, recorded in `moi-webinar/community-call/references/after-the-call.md`, says publishing a blog is not the end of the task: every post also goes out across MOI's social accounts and to the mailing list. Whether it covers every post type is not recorded. ASK: Rahul.

## Two tools, two paths
| | Website pipeline (this file) | `scripts/buffer.mjs` (`buffer.md`) |
|---|---|---|
| Repo | `sarvalabs/MOI-Website`, branch `main` | This library: `$SKILLS/moi-webinar/scripts/buffer.mjs` |
| Does | A copy file, then a manual workflow | Schedules or drafts X and LinkedIn posts and X threads |
| X and LinkedIn | Always a Buffer draft | Publishes by itself unless you pass `--draft` |
| Discord and Telegram | Post immediately when their secrets exist | Cannot post there |
| Key | `BUFFER_ACCESS_TOKEN` and channel ids, as Actions secrets | `BUFFER_API_KEY`, in a local `.env` at `$SKILLS/moi-webinar/.env` |
| Use it for | A published blog post | The pre-release X thread (`release-pack/GUIDE.md`) and webinar day-of posts (`moi-webinar`) |

## The loop
Before step 1: check with the marketing team (Vardan). They own what goes out on the company channels, and in practice this flow was used mainly for Builders-session posts, not for every blog post.
| # | Who | What | Sends anything |
|---|---|---|---|
| 1 | The operator, on a yes | Merge the post PR | No |
| 2 | CI | "Prepare social copy" opens a PR that adds `social/<slug>.md`, one block per channel, within a minute | No |
| 3 | You | Find the PR and check out its branch: `gh pr list --repo sarvalabs/MOI-Website --search "social: copy for <slug>"`, then `gh pr checkout <N> --repo sarvalabs/MOI-Website` (commit or stash your own changes first). Rewrite every block by hand. `../templates/announce/social-copy.md` shows the end state. From the clone run `python3 "$SKILLS/moi-blog/scripts/copy-lint.py" social/<slug>.md`. Commit locally. Pushing the edit to that PR needs a yes | No |
| 4 | The operator, on a yes | Merge the copy PR. This must come before step 5 | No |
| 5 | The operator, on a yes | Actions, "Distribute a post", inputs `slug`, `channels` (`x,linkedin`), `dry_run` left true. Read the output | No |
| 6 | The operator, on a separate yes | Run it again with `dry_run` false. Once | Yes: X and LinkedIn drafts in Buffer |
| 7 | A person | Open `publish.buffer.com`, the channel, Drafts. Add an image (the API attaches none), fix the hook, publish or schedule | The post goes out here |
| 8 | You | Copy and fill the record: `cp "$SKILLS/moi-blog/templates/announce/status.md" "$WORK/<slug>/status.md"`. Keep it outside the clone | No |
To run a workflow from the command line: `gh workflow run "Distribute a post" --repo sarvalabs/MOI-Website --ref main -f slug=<slug> -f channels=x,linkedin -f dry_run=true`, then `gh run list --repo sarvalabs/MOI-Website --workflow "Distribute a post" --limit 1` and `gh run view <run id> --repo sarvalabs/MOI-Website --log`. The Actions tab does the same.
Steps 2 and 5 never trigger each other. `distribute.yml` has no push trigger. It reads `main`, so before step 4 it stops with "No copy file at social/<slug>.md". PR #56, the September copy, opened on 2026-09-11 and was closed without merging (read 13 October 2026), so no announcement of that post through this pipeline is on record. Whether anyone announced it by hand, or distributed the copy files already on `main`, is not recorded (the previous DevRel's notes). ASK: Rahul.
Prepare only looks at added files, so editing a published post never creates copy. To redo one post: `npm run social:init <slug> -- --force`, or run "Prepare social copy" with that slug and Force ticked (without Force an existing copy file is left alone, and the run opens a pull request, so it needs a yes). A run with `force` ticked and no slug now refuses (commit `bc7a489`), because it would overwrite every post's copy. `--all --force` also needs `--yes-overwrite-all`.

## The copy file
```
---
slug: <slug>
title: "<title>"
published: 2026-09-11

x: |
  <the post>

  {{link}}

linkedin: |
  <the post>

  {{link}}
---
```
- One literal YAML block (`|`) per channel. Keep every non-blank line indented exactly two spaces. A line indented less ends the block, and the run either dies with a parse error or sends truncated text.
- Empty a channel, or delete its key, to skip it. There is no `enabled` flag.
- `{{link}}` becomes that channel's tagged URL: `?utm_source=<channel>&utm_medium=<medium>&utm_campaign=<slug>`. Delete `{{link}}` and the link is appended to the end. You cannot send a post without its link. <!-- slop-lint:ignore -->
- `#` inside a block is text, not a comment. Text after the closing `---` is a scratchpad that nothing reads.
- The scaffold seeds all four channels with the post's title and summary. Empty Discord and Telegram by hand: the previous operator decided on 2026-08-31 on X and LinkedIn only, and commit `f99e348` removed those blocks from the August copy. If their secrets are set, an unrewritten block posts immediately. As of October 2026 `DISCORD_WEBHOOK_URL`, `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are not set, so both channels are skipped (`project-handover-docs/BLOG.md`). Confirm with `gh secret list --repo sarvalabs/MOI-Website`, and decide with marketing whether to set them.

## What to write
- Plain text. No emoji, no backticks and no bold markers on X and LinkedIn (they render literally), no em dashes. Hashtags: none are recorded as used, and the question was never answered. ASK: Rahul.
- Every post stands alone. Write the hook for a reader who may not know MOI (the Voyage copy notes say so). A blog announcement may carry a hook. A release announcement does not: it is simple and points to the notes (`release-pack/references/announcement-pack.md`).
- Real copy on `main` runs 213 to 259 characters on X and about 1,058 to 1,373 on LinkedIn. Shorter is better on LinkedIn. Leave out implementation trivia: a built-in error name and "86 fuel" were cut from a draft on 2026-08-31.
- Check every specific claim against the post before the copy PR merges, as `f99e348` did. Put a time as a date, 24-hour UTC and India time, from `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "<YYYY-MM-DD HH:MM>" <area/city>`. Never write "today".
- Link placement is unsettled. The pipeline puts `{{link}}` in the body. The `buffer.mjs --follow` comment says "links in the post body suppress reach", so it puts the link second. The 4 August call wanted the link in the post so crawlers follow it. A webinar LinkedIn post keeps its link in the body, not the first comment (2026-09-04). ASK: Rahul. <!-- slop-lint:ignore -->
- No placeholder survives. Nothing in the pipeline checks for one. `copy-lint.py` does.

## Channels
| id | On send | Limit | Needs |
|---|---|---|---|
| `x` | A Buffer draft | 280, every URL counts 23 | `BUFFER_ACCESS_TOKEN`, `BUFFER_CHANNEL_X` |
| `linkedin` | A Buffer draft | 3000 | `BUFFER_ACCESS_TOKEN`, `BUFFER_CHANNEL_LINKEDIN` |
| `discord` | Posts now. Sent as content with mentions switched off | 2000 | `DISCORD_WEBHOOK_URL` |
| `telegram` | Posts now. HTML-escaped, so plain text only | 4096 | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` |
A channel with no secret is skipped and named, not failed. Over-length copy blocks the send and the run exits 1: it is never cut. X measures a link with a scheme at 23, and a bare domain at its literal length, which can under-count what X charges, so always write `https://`.

## Rehearse and read the output
- In CI, the dry run reads the real secrets, so it reports lengths: `would send 173/280`. A red dry run means over-length. Trust it.
- On your machine a dry run with no secrets prints "missing" for every channel and exits 0. That is not a rehearsal. A local dry run with throwaway secrets needs the operator's yes first. Set the six names to throwaway text and keep `--dry-run` on the line:
  `DISCORD_WEBHOOK_URL=x TELEGRAM_BOT_TOKEN=x TELEGRAM_CHAT_ID=x BUFFER_ACCESS_TOKEN=x BUFFER_CHANNEL_X=x BUFFER_CHANNEL_LINKEDIN=x npm run distribute <slug> -- --dry-run`
  Without `--dry-run` that line would try to post. Never drop the flag.
- Marks in the output: sent, skipped, blocked (over length), failed. Each channel is wrapped separately, so one failure does not stop the others, and the exit code carries it. `--only=twitter` is an error: the ids are `discord`, `telegram`, `x`, `linkedin`.
- A draft post is not distributed: the script exits 0 with "still a draft".
- `npm run social:links <slug> -- --md` prints the tagged links without sending.

## Mistakes and corrections
- Distribute has no memory. A second real run posts to Discord and Telegram again and makes a second Buffer draft. There is no undo in the repo. A wrong draft is deleted by hand in Buffer.
- A post that went out wrong on X or LinkedIn is corrected by hand or with a reply. The v0.13.0 release pack held a correction reply for a wrong time (a cleaned copy is `release-pack/examples/v0.13.0/social/x-correction-reply.txt`). Whether it was ever posted is not recorded (the previous DevRel's notes; ASK: Rahul).
- Drafts live on Buffer's servers. X's own drafts screen will be empty, and that is normal.

## After the announcement
- Request indexing for the URL in the blog's Search Console property (the operator's yes).
- A day-7 repost uses a `utm_content=day7` link from `npm run social:links`. The pipeline never sets it.
- The newsletter picks the post up from the feed by itself (`newsletter.md`).
- A community call description or a recap links the post. Those links are the backlinks the 27 August 2026 call notes ask for.
- Medium: the first write-up went to Medium only (2026-08-08), and a Medium-first post makes Medium the canonical copy. No later post is recorded there. ASK: Rahul if it is still a channel.
- Reddit and dev.to have UTM sources but no sender. Take the link from `social:links`.

## Gates
Each needs the operator's explicit yes that names the action, none carries over to the next, and the marketing team (Vardan) is asked before the first:
1. Pushing the branch of the copy PR, and opening, updating or merging that PR.
2. Running "Prepare social copy" by hand, and running "Distribute a post", dry run included. The real run has its own yes.
3. Creating, editing, scheduling or publishing anything in Buffer, and every post to X, LinkedIn, Discord, Telegram or Medium.
4. Requesting indexing, and setting or changing any Actions secret or variable (the operator types the value at a hidden prompt).
5. Uploading an image to cloud storage or any host, and downloading a file (name, source and size first).
6. Sending a message to a person about the announcement: Claude drafts, the operator sends.
See `SKILL.md` for the full list.

## Not yet known
- Whether the August posts were distributed, and whether the September post was announced by hand. Not recorded (the previous DevRel's notes). ASK: Rahul.
- Who may press publish in Buffer. Chandra owns the Buffer organisation and marketing owns the company channels (`project-handover-docs/BLOG.md`). ASK: Vardan.
- A posting-time convention. The 2026-09-10 release pack went at about 08:45 UTC, with no rule recorded.
