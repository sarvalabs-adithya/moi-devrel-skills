# Example: the moipod v0.13.0 release pack, September 2026

A cleaned copy of the one release pack on record. The network update was set for 00:00 UTC on 11 September 2026. That moment comes from the previous operator's correction reply, not from the note, and no written confirmation is on record (ASK: Gokul). Use it to see the shape of a pack and the defects to avoid. **Do not copy a sentence without reading the table "Lines that must not be reused".** Facts are as of 2026-10-02. `ASK:` is defined in `moi-devrel/SKILL.md`. Back to `../../GUIDE.md`.

## What is here
| File | What it is | Where the original is |
|---|---|---|
| `RELEASE-NOTE.md` | The note as saved. Its header says "as sent by the protocol team, unedited". It is not (see defect 14) | Committed locally on the MOI-Webinars session branch (4bdbe8e), never pushed. A second copy is in `moi-webinar/community-call/examples/cc14/sources/` |
| `BLOG.md` | The release post draft. The published post is `blog/src/content/posts/moi-september-2026-release.md` in `sarvalabs/MOI-Website`, at `https://blog.moi.technology/article/moi-september-2026-release/` (answered HTTP 200 on 2026-10-02) | Committed locally (4bdbe8e), never pushed |
| `SOCIAL.md` | The pack's record. It repeats the thread and LinkedIn text and contradicts itself | Local commit 27efaa3 (2026-09-10), not pushed |
| `social/thread/1.txt` to `7.txt` | The X thread, version A, verbatim | Local commit 27efaa3, not pushed |
| `social/x.txt`, `social/linkedin.txt`, `social/x-correction-reply.txt` | The channel-native single post, the shorter LinkedIn post, the correction reply | Local commit 27efaa3, not pushed |
| `social/discord.txt` | The Discord copy | Committed locally (4bdbe8e), never pushed |
Every original is committed locally on the MOI-Webinars session branch (4bdbe8e, 27efaa3) and was never pushed. Do not push them: the repo is public and those commits carry an AI co-author trailer. Whether the Discord and rewritten posts and the correction reply were ever posted is not recorded (the previous DevRel's notes). ASK: Rahul.

## What was changed from the original
1. Two em dashes in the headings of `SOCIAL.md` (lines 1 and 10) became colons. They were the only two in the pack.
2. The ignore marker `<!-- slop-lint:ignore -->` was added at the end of the 16 lines that `slop-lint.sh` flags (a YAML comment, `# slop-lint:ignore`, on `BLOG.md` line 10). It makes the lint skip the line, so this folder passes the lint while keeping its defects. The marker is not in the original. Strip it before reuse. It adds 26 characters, so `social/x.txt` measures 301 here and 275 in the original. `thread-lint.py` reports the marker as an error on purpose.
3. The KMOI asset id in `BLOG.md` (lines 24 and 112) is shortened to `0x1080fffe4cd973c4...00000000`. The full id is 64 hex digits, public in the live post, and has the shape of a private key, so it is not kept here. Read the real one from the live post or from `KMOI_ASSET_ID` in `js-moi-sdk`.
4. Nothing else. On 2026-10-02 the markers were removed, the two dashes and the full id restored, and every file then matched its original exactly. No path, key or personal detail needed removal.
5. "The user" in the example's `SOCIAL.md` means the previous operator.
Defects are not fixed. Lines are listed by their line numbers in these copies, which equal the originals.

## What was good
1. **The thread's shape.** One post per section of the note, in the note's order. Each post has its section name on its own line and stands alone. The longest is 248 characters. There is no hook, no emoji, no backtick and no em dash. Exact SDK versions, `-rc` kept, close the thread.
2. **Verbatim sentences.** The thread holds the note's sentences, merged only where two said the same thing. Nothing was added.
3. **The correction reply.** One sentence of 110 characters that gives the right moment, with its date, in the 00:00 UTC form.
4. **The channel-native pack** (`x.txt`, `linkedin.txt`, `discord.txt`). It answers the reviewer's list: the version, the moment with India time, what it adds, that it is breaking and what to update. LinkedIn is 961 characters. The Discord copy has bold lead-ins and an action list.
5. **The post.** It opens with what a developer can now do. It names the breaking changes before the detail. It has a table headed "Can it break your code?", question headings, numbered breakages with the most likely first, a table of exact versions, a runbook that starts with `npm i`, 8 takeaways and 7 FAQ entries. The original has no cover, no em dash and no HTML comment.
6. **Verification.** PR #53 records an independent pass of 200 claims (187 true, 8 partly, 5 unverifiable, 0 false). Those are the previous operator's numbers and were not re-checked here.

## What was wrong
Every defect found. Rules named are `slop-lint.sh` or `thread-lint.py` rules where one catches it.
| # | Where | Defect |
|---|---|---|
| 1 | `RELEASE-NOTE.md:5`, `SOCIAL.md:15` and `:61`, `social/thread/1.txt:3` | "scheduled for today at 12:00 AM UTC". No date, "today" had passed when it was scheduled, AM read as noon (`twelve-am`, `relative-day`) <!-- slop-lint:ignore --> |
| 2 | `social/x.txt:1`, `social/linkedin.txt:1`, `social/discord.txt:3` | "12:00 AM UTC (5:30 AM IST)". The AM form again, and a 12-hour India time (`twelve-am`, `am-pm`). The first two say "goes live" before the upgrade and the Discord copy says "is live" with no node read on record <!-- slop-lint:ignore --> |
| 3 | `SOCIAL.md:6` | "release time corrected to 12:00 UTC (noon)". Wrong, and it contradicts the post text on lines 15 and 61 |
| 4 | `social/discord.txt:3`, `BLOG.md:10` and `:40` | "Voyage devnet". Retired on 2026-09-25 (`voyage-devnet`) <!-- slop-lint:ignore --> |
| 5 | `social/discord.txt:7`, `social/linkedin.txt:7` | "fixed supply". The word is capped supply (`fixed-supply`). The post says the protocol burns the fuel each interaction uses (`BLOG.md:103`), so the supply does not stay fixed <!-- slop-lint:ignore --> |
| 6 | `social/discord.txt:7`, `social/linkedin.txt:7`, `social/x.txt:3` | "a native asset standard of its own", "its own MASN standard". The note says "a new native asset standard". Same shape as the line `moi-devrel/references/terminology.md` lists as rejected (`unverified-phrase`) |
| 7 | `BLOG.md:103` | "a native asset standard made for KMOI alone". The same phrase. It is still in the live post on 2026-10-02 |
| 8 | `social/discord.txt:5`, `social/linkedin.txt:5` | "Apps can now cover fuel for their users." Not in the note. It comes from the post, and it needs "fuel only" and a ledger row |
| 9 | `BLOG.md:46` | "Participant: an account on MOI". It predates the 2026-09-14 correction (`participant-is-account`) <!-- slop-lint:ignore --> |
| 10 | `BLOG.md:66` | "not save a setting, not call your logic" (`not-x-not-y`). The flat "an account with no KMOI could do nothing". "Now your app can hold one funded account and name it as the payer", cut from the CC14 script on 2026-09-25. Whether the post changes is not recorded <!-- slop-lint:ignore --> |
| 11 | `BLOG.md:45` | "Fuel: the fee for running an interaction" (`the-fee`, advisory) <!-- slop-lint:ignore --> |
| 12 | `BLOG.md:38`, `:51`, `:157` | Three breaking changes, four changes and five things that break. Each counts something different and the post does not say what |
| 13 | `social/discord.txt:18`, `social/linkedin.txt:18` | `RELEASE_URL` shipped as a placeholder (`placeholder`). What it should be is not recorded <!-- slop-lint:ignore --> |
| 14 | `RELEASE-NOTE.md:1` | "unedited" is false. The first note had an em dash and other sentences. The original is lost |
| 15 | `SOCIAL.md:99` | "Text is the release note as sent, unedited". Its own header says the sentences were restructured |
| 16 | `SOCIAL.md:6` | Says `social/linkedin.txt` was sent to Buffer. The file now holds the rewrite. The LinkedIn text sent is probably the inline text in `SOCIAL.md` (inferred) |
| 17 | `SOCIAL.md` | It repeats the thread and LinkedIn text. The same sentences sit in four places and the places disagree |
| 18 | `social/thread/5.txt:1` and `:3` | "ANU" in capitals, "anu" elsewhere. The note itself mixes them. The post uses "anu" |
| 19 | `social/thread/5.txt:6` and `:7` | The arrow character is outside plain ASCII. How X counts it is not on record (`non-ascii`) |
| 20 | `social/x.txt` | 275 of 280 characters in the original. No room for an edit and none for a link (23) (`length-near`) |
| 21 | `social/x-correction-reply.txt:1` | "today" goes stale (`relative-day`) |
| 22 | The pack | No post gives a working link to the full release notes, and none says devnet would be wiped |
| 23 | `BLOG.md:202` | `<Subscribe />` at the end. The article page already renders the signup form and the tag is inert in a `.md` file (`moi-blog/scripts/post-lint.py`, rule `stray-subscribe`) |
| 24 | `BLOG.md:2` and `:3` | The title is 82 characters and the summary 240. `moi-blog/scripts/post-lint.py` warns above 60 and outside 130 to 170 (as of 2026-10-02) |
Open in PR #53 on the day: "Confirm the go-live date", because the go-moi tag is dated 10 September. No owner is on record.

## Lines that must not be reused
| Line | Write instead |
|---|---|
| "scheduled for today at 12:00 AM UTC" | "scheduled for 00:00 UTC on 11 September (05:30 IST)" <!-- slop-lint:ignore --> |
| "goes live on 11 September at 12:00 AM UTC (5:30 AM IST)" | "scheduled for 00:00 UTC on 11 September (05:30 IST)", and "live" only after a node read <!-- slop-lint:ignore --> |
| "is live on Voyage devnet" | "went live on devnet", only after the node was read <!-- slop-lint:ignore --> |
| "with a fixed supply: no mint, no burn, including by the manager" | The note's sentence: "You cannot mint or burn KMOI, and neither can the asset manager." <!-- slop-lint:ignore --> |
| "a native asset standard of its own", "made for KMOI alone" | The note's: "a new native asset standard" |
| "Apps can now cover fuel for their users." | "An interaction can name another account to pay its fuel", with a ledger row |
| "Full release notes: RELEASE_URL" | A real https:// URL from the protocol team, or no line <!-- slop-lint:ignore --> |
| "Participant: an account on MOI" | "A participant is a person, a company or an agent. Its state is held in an account." <!-- slop-lint:ignore --> |
| "not save a setting, not call your logic" | Cut it <!-- slop-lint:ignore --> |

## Run the lint on it
`python3 "$SKILLS/moi-blog/release-pack/scripts/thread-lint.py" "$SKILLS/moi-blog/release-pack/examples/v0.13.0" --note "$SKILLS/moi-blog/release-pack/examples/v0.13.0/RELEASE-NOTE.md"` exits 1 and fires most rules. `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh"` on the same files exits 0, because of the markers. The thread files raise no `not-in-note` line, because the note file seems to have been regenerated from them (inferred).
