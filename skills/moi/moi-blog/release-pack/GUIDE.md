# MOI release pack: from the protocol team's note to the posts

Branch of `moi-blog`. `$SKILLS`, the operator, `ASK:`, the house rules and the gates are in `moi-blog/SKILL.md` and `moi-devrel/SKILL.md`; this guide adds what is specific.

## What this covers
A protocol release has two deliverables in different repos with different tools: the announcement pack (X thread, LinkedIn, Discord), written from the protocol team's note and sent before the network upgrade, and the release post "MOI <Month> 2026 Release", a blog post that is claim-checked and shipped by pull request. The one worked example is moipod v0.13.0 (moipod is the software that runs a MOI node), kept in `examples/v0.13.0/`, whose update the pack gave as 00:00 UTC on 11 September 2026; that moment is not in the note and no written confirmation is on record (ASK: Gokul). Whether every release gets a pre-release pack is not settled (ASK: Rahul), and every fact here is as of 2026-10-02.
Where this run meets the blog run: this branch drafts `BLOG.md` in the pack folder of a working copy of `moi-foundation/MOI-Webinars`. Publishing it is the run table of `moi-blog/SKILL.md`, which runs in a clone of `sarvalabs/MOI-Website`. Step 10 below is the hand-over: the blog run takes `BLOG.md` in at its step 3 and re-uses this pack's ledger at its step 4.
Not covered: writing a post in house style, the publish pull request, announcing a published post and the newsletter are `moi-blog`, which takes over once `BLOG.md` is finished. Checking claims in general is `moi-devrel/claim-check`. The release slides of a community call are `moi-webinar/community-call` (`moi-webinar/community-call/references/release-slide-checks.md`). After a devnet reset, the order of work is `moi-devnet-reset`.

## Before you start
Unlike the rest of `moi-blog`, which runs from the website clone, run every command in this guide from the root of a working copy of `moi-foundation/MOI-Webinars`, where pack folders `protocol-release-<version>/` sit. The repo is public, so a push publishes. A pack folder holds an unannounced release note and a ledger whose source column may name private repositories, so the scaffold makes the folder ignore itself and nothing in it is staged, committed or pushed without the operator's yes. Whether pack folders are ever committed, and on which branch, is a policy nobody has written down (ASK: Rahul). As of 2026-10-02 the v0.13.0 folder exists only on the previous operator's machine: 11 files in one of 6 unpushed local commits (the other 5 are x402 and `buffer.mjs` work) and 3 untracked (`BLOG.md`, `RELEASE-NOTE.md`, `social/discord.txt`). ASK: Adithya for a copy. Those unpushed commits carry an AI co-author trailer: copy the files out and never push that branch. A cleaned copy is in `examples/v0.13.0/`.
- [ ] The release note exactly as the protocol team sent it, and who sent it and where. The protocol team provides it, through the operator. How it reaches DevRel is not recorded. ASK: Rahul. Ask the operator: "Please paste the note exactly as you received it, and say who sent it."
- [ ] The release moment as a date and a 24-hour UTC time, in writing. A note that says "today" has no date. ASK: Gokul.
- [ ] Whether the upgrade wipes devnet, and what "full release notes" should link to. ASK: Gokul.
- [ ] The announcement format. The reviewer who asked for a different one after v0.13.0 is unnamed. ASK: Rahul for one written example.
- [ ] To schedule in Buffer (the service that holds drafts and scheduled posts for X and LinkedIn): `scripts/buffer.mjs` at the root of the working copy (the repo's own script, not one of this branch's) and `BUFFER_API_KEY` in a local `.env`. The operator sets the key. Claude never opens `.env`. The script is on branch `claude/agent-payments-simple`, not `main` (`main` has no `scripts/` folder), and its `--thread-dir` option is unpushed. ASK: Adithya for a copy. Without it the operator posts by hand.
- [ ] Read access to go-moi and go-pisa source for the post's claims. ASK: Gokul.

Who to go to (from `moi-devrel/references/people-and-teams.md`):
| Who | For |
|---|---|
| Gokul, protocol team | The note's facts, the release moment, whether devnet is wiped, "live", source access |
| Rahul | Review of any public piece, the announcement format, who owns an account. The first person to ask when nothing else names an owner |
| Vinay | New SDK, go-moi or Voyage versions, and the release logs he posts in Discord |
| Adithya, previous operator | History, and files that exist only on his machine |

## The run
| # | Step | What to do, and where | Done when |
|---|---|---|---|
| 1 | Receive the note | `bash "$SKILLS/moi-blog/release-pack/scripts/new-release-pack.sh" <version>` (for example 0.13.0) makes the folder, which ignores itself, and refuses to overwrite. Claude saves the pasted note in `RELEASE-NOTE.md`, exactly, with nothing else. Then `shasum -a 256 protocol-release-<version>/RELEASE-NOTE.md`. In `SOCIAL.md` record the hash, who sent the note, where and when. Draft the questions in `references/the-note.md` for the operator to send | The file is the note character for character, its hash is recorded, and the operator compared it with what was sent |
| 2 | Read what is live | `curl -s -X POST https://dev.voyage-rpc.moi.technology/devnet/ -H 'content-type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"net.Version","params":[]}'` (a read; it returned "0.13.0" on 2026-10-02). `net.NetworkID` answered "does not exist" the same day: record what you get and ASK: Gokul which call returns the network ID. The wire field name (`payer` or `fee_payer`) is in `moi-devrel/references/devnet.md`, "Before you say live". For each version in the note, `npm view <package>@<version> version`. Until the upgrade has run, every post says "scheduled for" | Each status word has a read or a protocol-team confirmation. The moment is a date and UTC time in writing |
| 3 | Start the claim ledger | `python3 "$SKILLS/moi-devrel/claim-check/scripts/extract-claims.py" --all protocol-release-<version>/RELEASE-NOTE.md > protocol-release-<version>/claims-candidates.csv`, then `cp -n protocol-release-<version>/claims-candidates.csv protocol-release-<version>/ledger.csv`. `--all` lists every sentence, because the default run skips plain statements. `cp -n` never overwrites a ledger that holds verdicts. Extract once. Delete rows that state nothing checkable. Sources in order: tagged source, the note, docs.moi.technology | Every sentence of the note has a row or was dropped on purpose |
| 4 | Announcement per channel | `references/announcement-pack.md`. Draft A (verbatim: thread, `linkedin.txt`), then B (channel-native: `x.txt`, `linkedin.native.txt`, `discord.txt`). Show both. Record the pick. Delete unused files and renumber the thread. Log each difference from the note in `SOCIAL.md`. Add ledger rows for new sentences: `python3 "$SKILLS/moi-devrel/claim-check/scripts/extract-claims.py" --all --against protocol-release-<version>/ledger.csv --dropped protocol-release-<version>/claims-candidates.csv <draft files>` prints the rows that are missing (append them without its header line) | `python3 "$SKILLS/moi-blog/release-pack/scripts/thread-lint.py" protocol-release-<version>/social --note protocol-release-<version>/RELEASE-NOTE.md` has no error, and every `not-in-note` line has a ledger row |
| 5 | Release post | `references/release-post.md`. Write `BLOG.md` (the scaffold copied `moi-blog/templates/release-post-skeleton.md` into it), then run the same `--all --against ... --dropped ...` command on it. Writing mechanics are `moi-blog/references/authoring.md`; the publish pull request and distribution are the `moi-blog` run table | The operator read it once. Every claim has a ledger row |
| 6 | Polish and verify | `find protocol-release-<version> -type f \( -name '*.txt' -o -name 'BLOG.md' \) -exec bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" {} +`. Read every post alone. Re-read the opener and the KMOI (the native token) and anu (its smallest unit) paragraphs after every automated pass. `bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" protocol-release-<version>` is a backstop only | Lint 0 errors, `thread-lint.py` 0 errors, `python3 "$SKILLS/moi-devrel/claim-check/scripts/ledger-status.py" protocol-release-<version>/ledger.csv` exits 0, and `grep -rn -e '{{' -e 'FILL IN' protocol-release-<version>` prints nothing |
| 7 | Final read | Show the exact text of each post, its channel, tool, fate and time in one place. `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "<YYYY-MM-DD HH:MM>" UTC` for each time (`references/timing.md`) | The operator read it once and said yes to each action by name |
| 8 | GATE: the human posts or schedules | `references/announcement-pack.md`, "Sending through Buffer". Running `scripts/buffer.mjs` in any form is a gate, a dry run included. Drafts by default. Discord by hand. After each action open the live post and read it | `SOCIAL.md` shows each channel as not sent, drafted, scheduled or sent by hand, with proof |
| 9 | The network moves | Read the node again (step 2). Only then write "live". If devnet was wiped, see `references/timing.md` | Every status word is true on the day |
| 10 | Publish the post | Hand over to the `moi-blog` run table. In its step 3, make the branch in the website clone and copy the finished `BLOG.md` to `blog/src/content/posts/<slug>.md` in place of a skeleton. Copy this pack's `ledger.csv` to `$WORK/<slug>/ledger.csv`, outside the clone, so that `cp -n` in step 4 keeps its verdicts. Then follow `moi-blog/SKILL.md` through the pull request, merge, live check and announcement. GATE: each of those, namely the push and PR, the merge to `main` of `sarvalabs/MOI-Website` (it deploys) and every Buffer or Distribute run. After the merge, follow the copy PR (the pull request that its Prepare workflow opens to add `social/<slug>.md`) to its end | `python3 "$SKILLS/moi-blog/scripts/check-live.py" <slug>` exits 0 (the slug is the post's file name without `.md`, for example `moi-september-2026-release`). The copy PR is merged or dropped on purpose |
| 11 | GATE: correct | `references/corrections.md`, if a posted statement is wrong. A reply, edit or deletion on a live channel needs a yes | The operator has the correction text. Nothing is posted without a yes |
| 12 | Hand-back | The format at the end of this file | The operator has read it |

Exit codes. `thread-lint.py`: 0 no error (warnings allowed; a `not-in-note` warning needs a ledger row, not a block), 1 an error such as a placeholder, a length over the limit or a retired term (do not ship), 2 bad input, an env file or no post found. `ledger-status.py`: 0 every row stands, 1 rows are still open, 2 unreadable or empty ledger. Ship only on 0 from both.

## Which file to read
| Doing | Read |
|---|---|
| Receiving, keeping and quoting the note, the questions for the protocol team | `references/the-note.md` |
| X thread, single post, LinkedIn, Discord, the format dispute, Buffer commands | `references/announcement-pack.md` |
| The release post: structure, rules, ledger, the pull request | `references/release-post.md` |
| The order of events, writing the time, what an upgrade does to devnet | `references/timing.md` |
| A posted statement is wrong | `references/corrections.md` |
| Every trap in one list | `references/traps.md` |
| A finished pack to learn from, and the lines never to reuse | `examples/v0.13.0/README.md` |
| Starting a pack, the social skeletons (the post skeleton is `moi-blog/templates/release-post-skeleton.md`) | `templates/` |
| Testing a change to this branch | `evals/evals.md` |

## Facts that fail silently
| Rule | The incident |
|---|---|
| Write the moment as a date and 00:00-style UTC, then India time. Never "today", "12:00 AM", "12.00 AM" or "midnight" | The note said "today at 12:00 AM UTC". It was read as noon and two scheduled posts were deleted by hand (2026-09-10) <!-- slop-lint:ignore --> |
| A scheduled Buffer post publishes with nobody reviewing it. Use drafts. End `--at` in `Z` | A team reviewer objected after the v0.13.0 posts went out directly on the socials (the date is inferred from the order of requests: 2026-09-10) |
| Keep one copy of each text. Hash the note | `SOCIAL.md` said the time was noon while its text said 12:00 AM, and `RELEASE-NOTE.md` said "unedited" and was not |
| No placeholder ships. `thread-lint.py` and `slop-lint.sh` report `{{...}}`, only `slop-lint.sh` reports `[FILL IN`, `buffer.mjs` reports none | `RELEASE_URL` ended two v0.13.0 drafts <!-- slop-lint:ignore --> |
| Read the node before "live". Before the upgrade write "scheduled" | On 2026-09-10 devnet still answered 0.12.0 and `payer` |
| Say devnet, capped supply, KMOI. State no universal | "Voyage devnet" and "fixed supply" stayed in the pack and the post <!-- slop-lint:ignore --> |
| Keep `-rc` as tagged. "Latest" is only what npm says | As of 2026-10-02 the npm `latest` tag of `js-moi-sdk` is 0.9.0-rc2 |
| Ask whether the upgrade wipes devnet | The note was silent. After the wipe announced for 2026-09-11 the Launchpad took 4 days to move to the new registry and the Explorer 11. The MCP pinned it after 12 days and was still on the old one on 2026-10-02 |
| Keep the ledger and the pack out of git until the operator says so. The scaffold's `.gitignore` does it | The ledger's source column may name private repositories, the note is unannounced, and the repo is public (`moi-devrel/claim-check` keeps its ledger untracked for the same reason) |
| Follow the copy PR to its end | PR #56 opened 26 seconds after the September post merged and is still open (2026-10-02) |

## Gates
The gates of `moi-blog/SKILL.md` apply in full: a push, a pull request and a merge, every workflow run (a dry run is a run), every form of `scripts/buffer.mjs` (a dry run included, it sends the key to Buffer), cloud storage, downloads, secrets, devnet funds, the git identity and sub-agents. Specific to this branch, nothing below happens without the operator's explicit yes in this conversation:
- Any `git add` (it takes removing the pack folder's own `.gitignore` first), commit or push of the pack folder: `moi-foundation/MOI-Webinars` is public, so a push publishes it. A merge to `main` of `sarvalabs/MOI-Website` deploys.
- Posting, scheduling or saving a draft in Buffer (`--confirm` in any form), and posting in Discord, Telegram, X or LinkedIn. A reply, edit or deletion on a live channel.
- Sending any message, including the questions to the protocol team. Claude drafts, the operator sends. Telling anyone a time or a status is confirmed.
- A commit or a PR with an AI co-author line or a "generated with" footer.
A yes covers the one action it names. Reads are allowed: `net.Version`, `npm view`, a GET of a public page.

## Keys and access
Names only. Where each lives: `moi-devrel/references/keys-and-access.md`. The scripts of this branch need no key.
- `BUFFER_API_KEY`: `scripts/buffer.mjs`. A local `.env`, never pasted into chat. Only a Buffer organisation owner can create it: Chandra.
- The website pipeline's secrets (`BUFFER_ACCESS_TOKEN`, `BUFFER_CHANNEL_X`, `BUFFER_CHANNEL_LINKEDIN`, `DISCORD_WEBHOOK_URL`) are GitHub Actions secrets, listed in `moi-blog/SKILL.md`.
- Read access to the private go-moi and go-pisa repositories. ASK: Gokul.
- Recovery phrases: Claude never handles one, including a throwaway one.

## Hand-back
```
Produced: <the pack folder, each file, the post draft, with exact paths>
Status per channel: <not sent, drafted, scheduled or sent by hand, with proof>
Ledger: <rows by verdict, and every row still unverified with who can settle it>
Remaining: <numbered, each with an owner>
Not verified or simulated: <say so, or "none">
Ready: yes or no, because <one reason>
Next steps: <one to three>
```
Ready is no while a lint error stands, a ledger row is `unverified`, the moment has no written date, or a status word was not read from the node.
