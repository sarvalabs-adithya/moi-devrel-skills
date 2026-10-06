# The announcement pack, per channel

The pack is the set of short posts that tell developers a network upgrade is coming, at what time, what changes and what to update. Facts are as of 2026-10-02. **Evidence exists for one pack only**, moipod v0.13.0 (`../examples/v0.13.0/`). No pack for v0.12.0 is on record. Whether a pre-release pack is standard for every release is not settled. ASK: Rahul. `ASK:` is defined in `moi-devrel/SKILL.md`. Back to `../GUIDE.md`.

## The pack at a glance
| Channel | File | How it goes out | Limit | v0.13.0 |
|---|---|---|---|---|
| X thread | `social/thread/<n>.txt` | `buffer.mjs --thread-dir`, X channel "MOI_Tech" | 280 per post, each URL counted as 23 | 7 posts, 150 to 248 characters |
| X single post | `social/x.txt` | `buffer.mjs --file` | 280 | 275 |
| LinkedIn | `social/linkedin.txt` (verbatim shape), `social/linkedin.native.txt` | `buffer.mjs --file`, company page "moi-tech" | 3,000 | 961 (the native one) |
| Discord | `social/discord.txt` | by hand. `buffer.mjs` cannot post to Discord | 2,000 | 1,321 |
The limits are in `scripts/lib/social.js` of `sarvalabs/MOI-Website` (the X link rule is its `measure()`). `thread-lint.py` applies them.

## Which text: verbatim or channel-native
*Verbatim* means the note's own sentences in the note's order, restructured only so each post stands alone, with no fact added. *Channel-native* means a shorter text written for the channel (a single X post, a short LinkedIn post, a Discord message with bold lead-ins) that carries the same facts, the moment and the action required. Both must say only what the note says. This is contested. Two packs exist for v0.13.0.
- **A, verbatim.** The 7-post thread and a LinkedIn post that is the whole note. Sentences were restructured only for clarity and no fact was added. It followed the standard the previous operator was given, and `SOCIAL.md` of the pack records it as sent to Buffer.
- **B, channel-native.** `x.txt`, a shorter LinkedIn post and `discord.txt`. In the v0.13.0 folder the shorter LinkedIn post is `linkedin.txt`, which overwrote the verbatim one (inferred from the file times and `SOCIAL.md`, which says `linkedin.txt` was the file sent). In this branch's templates (`templates/social/`) it is `linkedin.native.txt`, so both can exist until one is chosen. They say a version launches at a time, what it adds and that developers update. After the posts went out an unnamed team reviewer asked for exactly that: communicate that a new version will launch with certain capabilities at time T, that developers may need to upgrade, and write it "optimised as per the medium". The previous operator answered that he had followed the standard he was given and that protocol releases must be kept simple.
- Whether B or the correction reply was ever posted is not recorded. ASK: Adithya. Who decides next time is not recorded. ASK: Rahul.
- Procedure: draft A first, because it only restructures the note. Draft B. Show both. Record the pick in `SOCIAL.md`. Ask Rahul, through the operator, for one written example of the format he wants.

## The X thread
v0.13.0, one post per section of the note, characters counted after trimming:
| File | Section | Characters |
|---|---|---|
| 1.txt | Title and release moment | 196 |
| 2.txt | Fee Payer | 150 |
| 3.txt | KMOI Native Asset | 162 |
| 4.txt | Participant List | 248 |
| 5.txt | ANU, with the two changed prices | 211 |
| 6.txt | Action required | 236 |
| 7.txt | SDK Versions | 179 |
- **Order:** the note's order. The first post carries the title and the moment. The last carries the exact versions.
- **Shape of a post:** the section name on its own line, a blank line, then the note's sentence or sentences. Each post must make sense alone.
- **No hook.** A protocol release is an announcement that points to the notes (decided 2026-09-10 by the previous operator, after asking whether a hook belongs).
- **Plain text:** no emoji, no backticks, no bold markers, hyphen bullets, no em dash. X and LinkedIn show backticks literally.
- **Files:** `1.txt` to `N.txt` with no gap. `buffer.mjs` reads names matching `^\d+\.txt$` in numeric order, the first is the root post, it works for the X channel only and cannot be combined with `--follow`. A file with any other name is skipped without a message.
- **Number of posts:** one per section. A note with three changes gives six posts. Delete the spare template files and renumber.
- **Label punctuation:** the thread uses a bare label line. The previous operator once asked for a colon after a label ("Fee payer:"). Which is canonical is not decided. ASK: Rahul.

## The single X post
`x.txt` for v0.13.0 is 275 characters, which leaves 5. A link would add 23, so a link does not fit. It holds the version and moment, one clause per change, and "Breaking release. Update to js-moi-sdk 0.9.0-rc2 before then."

## LinkedIn
- **A:** the whole note as one post, headings as plain lines, hyphen bullets, no backticks.
- **B:** the first line gives the moment. Then "What it adds:" and one paragraph per change. Then "This is a breaking release. If you build on MOI:" and three hyphen actions. Then "Full release notes:" with the URL on the next line.
- Shorter is better. Cut implementation detail (a webinar LinkedIn draft was cut for a builtin error name and a fuel figure; the exact date is not recorded).
- Link placement is not decided. `buffer.mjs --follow` puts the link as the second X post or the first LinkedIn comment, because links in the body suppress reach (the script's comment). The website pipeline puts the link in the body. The 4 August strategy meeting wanted the link in the post so AI crawlers follow it. ASK: Rahul.

## Discord
- Shape in v0.13.0: a bold title line, the moment, a sentence that the release is breaking, one bold lead-in per change, "If you build on MOI:" with hyphen actions, then "Full release notes:" and a link. That copy used bold and backticks, so `thread-lint.py` allows both on Discord.
- Delivery: the copy was written on 11 September, the day after the thread. How it was sent is not recorded. The website pipeline can post to Discord through a webhook but is built for blog posts and needs a merged `social/<slug>.md` copy file (`moi-blog/references/distribution.md`). In this branch Claude drafts it and the operator posts it by hand. Which Discord channel is not recorded. ASK: Rahul.

## Other channels
- Telegram: the website pipeline has it. Discord and Telegram were dropped from the August blog announcements on 2026-08-31. No release pack file exists for it. ASK: Rahul.
- Medium: only the first blog post (8 August) went there. No release used it. Whether it is still a channel is not recorded. ASK: Rahul.
- The newsletter is built from the blog feed (`moi-blog/references/newsletter.md`). Whether the September post went out in a newsletter is not recorded. ASK: Rahul.

## What every announcement carries
1. The name and version as the note writes them (moipod v0.13.0).
2. The moment as a date, 24-hour UTC and India time. "Scheduled for" before the upgrade. "Live" only after a node read (`timing.md`).
3. That the release is breaking, once, if the note says so.
4. One line per change, in the note's words.
5. The action required and the exact SDK versions, with any `-rc` suffix.
6. A real https:// link, or no link line. `RELEASE_URL` shipped in two v0.13.0 drafts. <!-- slop-lint:ignore -->
7. Nothing the note does not say, unless the ledger holds a verdict for it.

## What was contested
| Question | Positions | Status |
|---|---|---|
| Verbatim or channel-native | See above | Open. ASK: Rahul |
| A hook | None, decided 2026-09-10 | Settled for protocol releases |
| Colon after a label | Asked 2026-09-10, bare labels shipped | Open |
| Hashtags | The previous operator asked if they help. No answer recorded. No hashtag appears in the pack | Open |
| Emoji | None used | Whether banned or only unused is not recorded |
| Link placement | See LinkedIn | Open |
| A pack for every release | None on record for v0.12.0 | Open |

## Sending through Buffer
The tool, its key, its flags, the branch it lives on and what it does not do are in `moi-blog/references/buffer.md`, the one home. Running `scripts/buffer.mjs` in any form, a dry run included (it sends the key to Buffer), is a GATE, and so is every `--confirm`. From the root of the working copy that holds the script, and with the channel ids from `node scripts/buffer.mjs channels`:
```
node scripts/buffer.mjs post --thread-dir protocol-release-<version>/social/thread --channel <X channel id> --draft
node scripts/buffer.mjs post --file protocol-release-<version>/social/linkedin.txt --channel <LinkedIn channel id> --draft
```
- Pack points only. `--thread-dir` is in a commit that is not pushed (ASK: Adithya for a copy). Without it the operator posts the thread by hand in X from the numbered files, and `thread-lint.py` still applies. That fallback is this library's design, not a recorded practice.
- The script checks no length and no placeholder. `thread-lint.py` does both. Discord is by hand.
- Check any `--at` value against `time-table.sh` and end it in `Z`. There is no delete command.
- After `--confirm`, open Buffer and read what is there. Record the id it printed in `SOCIAL.md`.

## Not yet known
- The announcement format, who decides it, and the reviewer's name. ASK: Rahul.
- What was posted for v0.13.0 on LinkedIn and Discord, and by what means. ASK: Adithya.
- Whether a pack goes out for every release, and the lead time. See `timing.md`.
