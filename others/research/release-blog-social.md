# Protocol release communications, the blog, and social distribution

Researcher note for the MOI DevRel skills project. Everything here is OBSERVED (with a path, and a line or section where useful) unless marked "(inferred)". "unknown" means the evidence does not say; each unknown is repeated under Open questions.

Short version of the area: there are two release deliverables that are easy to confuse and live in different repos with different tooling.

1. A **release announcement pack** (X thread, LinkedIn post, Discord post) written from the protocol team's release note and **scheduled** through `scripts/buffer.mjs` in the MOI-Webinars repo, before the network upgrade lands.
2. A **release blog post** ("MOI <Month> 2026 Release") written, fact-checked and shipped by PR into the MOI-Website repo, after or around the release, and announced through the website repo's draft-only Prepare/Distribute pipeline.

The existing `moi-blog` skill covers the second one in depth and the first one not at all.

---

## Sources read

Release folder (all in `/Users/adithyaganesh/MOI-Webinars/.claude/worktrees/relaxed-mccarthy-368dbc/`, the "worktree" below):

- `protocol-release-0.13.0/RELEASE-NOTE.md`, `BLOG.md`, `SOCIAL.md`
- `protocol-release-0.13.0/social/discord.txt`, `linkedin.txt`, `x.txt`, `x-correction-reply.txt`, `thread/1.txt` to `thread/7.txt`
- `scripts/buffer.mjs` (232 lines, read in full)
- `otter-transcript/Project Launch and Blog Strategy_summary.txt` and `..._transcript.txt` (4 Aug 2026; read in full)
- Also read for comparison: `session-8-policies/SOCIAL.md` (webinar social pack), `session-7/blog-assets/PUBLISH.md`, `session-7/blog-assets/social-pack.md`, `session-7/blog-assets/factcheck-report.md`
- `git log` for `protocol-release-0.13.0` and `scripts/buffer.mjs` in the worktree (commits `5bcfbcd`, `27efaa3`, `a28bbfc`)
- Env variable NAMES only (never values) in the worktree `.env` files

Existing skill (`/Users/adithyaganesh/.claude/skills/moi-blog/`): `SKILL.md` and `references/authoring.md`, `distribution.md`, `buffer.md`, `geo.md`, `mailchimp.md`, `assets.md`, `mailchimp-header.html`, `mailchimp-body.html`, `mailchimp-footer.html`, head of `mailchimp-template.html`.

Website repo (`/Users/adithyaganesh/untitled folder 10/MOI-Website`, branch `local/sweep-oct1`; `scripts/`, `social/`, `blog/src/content/` have no uncommitted changes, `.github/workflows/deploy.yml` does and I did not read it):

- `social/README.md`, `social/moi-august-2026-release.md`, `social/move-your-voyage-login-to-moi-wallet.md`
- `scripts/social-init.js`, `scripts/distribute.js`, `scripts/lib/social.js`, `scripts/lib/senders.js`, `scripts/lib/share.js`
- `.github/workflows/social-prepare.yml`, `.github/workflows/distribute.yml`
- `blog/src/content/posts/moi-september-2026-release.md` (byte-identical to the worktree `BLOG.md`, verified with `diff`), `moi-august-2026-release.md` (read to line 175 plus all headings), `move-your-voyage-login-to-moi-wallet.md` (head)
- `git log` and read-only `gh pr view` / `gh pr diff` on PRs #53, #55, #56 of `sarvalabs/MOI-Website`; `gh pr list` for the PR timeline

User requests: `/Users/adithyaganesh/moi-devrel-skills/_research/_user-requests.txt`, grep hits and the context around them (release session lines 1150-1345, 2013-2125; Agency-Website session lines 28-66; webinar/social lines 888-1110; distribution-pipeline build lines 2283-2486).

User memory notes read for rules: `devnet-build-lag.md`, `moi-terminology-corrections.md`, `no-claude-attribution.md`, `no-multi-agent-workflows.md`, `moi-source-on-disk.md`, `batch-review-changes.md` (all under `/Users/adithyaganesh/.claude/projects/-Users-adithyaganesh-MOI-Webinars/memory/`).

Limits of the evidence:

- Every prompt in `_user-requests.txt` is cut at about 415 characters, so long pasted messages (the Rahul Discord message, the 11 Sep review-call transcript, the reviewer's critique) are truncated.
- The Otter transcript has speaker numbers, not names. Speaker 3 is Adithya ("Adi"). Speaker 2 is the person who reviews and directs (inferred: Rahul, who is named elsewhere as the internal reviewer).
- File mtimes in the worktree appear to be in a different timezone from the git commit times (inferred: the Mac clock was US Eastern; commits are +0400 and +0530). I treat mtime-based timings as approximate.

---

## Process: Protocol release announcement pack (X thread, LinkedIn, Discord)

### Purpose
Tell developers that a breaking network upgrade is coming at a stated time, what changes, and what they must update, in short channel-native posts that point at the release notes. Observed instance: moipod v0.13.0, network update at 00:00 UTC on 11 September 2026.

### Trigger or cadence
- Trigger: the protocol team issues a release note for a scheduled network upgrade. For v0.13.0 the user pasted the note into chat on 10 Sep 2026 and asked for X and LinkedIn posts (`_user-requests.txt:1158`).
- Cadence: per protocol release. Two releases are evidenced (v0.12.0 in August, v0.13.0 in September). For August there is NO evidence of a pre-release social pack, only a blog. "Monthly" is inferred from the post titles "MOI August 2026 Release" and "MOI September 2026 Release".
- Timing: the pack was scheduled for 12:45 PM Dubai on 10 Sep (about 08:45 UTC, inferred from `_user-requests.txt:1189-1192`), about 15 hours before the release moment.

### Who does it
Adithya writes, schedules and confirms. The protocol team writes the release note (author unknown). An unnamed team reviewer commented after it went out (`_user-requests.txt:1193`). Rahul is the named internal reviewer for the blog (PR #53 body, "Internal review (Rahul)").

### Inputs needed before starting
- The protocol team's release note text, including: version, exact release moment, list of changes, "action required" items, SDK versions.
- The exact release moment in UTC, confirmed with the protocol team (see Traps: the 12:00 AM confusion).
- Buffer: the two channel IDs (X channel "MOI_Tech", LinkedIn company page "moi-tech") and an API key (see accounts). Channel IDs come from `node scripts/buffer.mjs channels`; do not hardcode them in notes.
- A decision on verbatim versus rewritten (see Open questions: the user and a reviewer disagreed).

### Steps in order
Reconstructed from the prompt sequence at `_user-requests.txt:1158-1204` and the files in `protocol-release-0.13.0/`. The exact `buffer.mjs` command lines for the thread are not in the evidence; the only literal command in the logs is the LinkedIn one at `_user-requests.txt:913` (`node scripts/buffer.mjs post --file <path>/linkedin.txt --channel <id> --draft --confirm`). The commands below are built from the script's own usage text and flags.

1. Save the release note as `protocol-release-<version>/RELEASE-NOTE.md`.
2. Draft X and LinkedIn from it. First attempt used the brand-voice and `linkedin-post-writer` skills to produce rewritten posts; the user dropped those and required the text to be verbatim from what he had sent (`SOCIAL.md` Notes, lines 99-100; `_user-requests.txt:1163`).
3. Sentence-level edits the user asked for, in this order (`_user-requests.txt:1163-1176`):
   - keep everything verbatim from the note;
   - question whether "fee payer" needs "(fuel)" after it, and whether each sentence makes sense read alone;
   - merge two sentences that said the same thing ("The fee payer signs the interaction and pays the fuel cost. The sender does not have to pay..." became "The fee payer also signs the interaction and pays the fuel cost instead of the sender.");
   - drop "We are rolling out moipod v0.13.0 with several important updates." (it duplicates the next sentence);
   - add the asset id line ("KMOI also has a new Asset ID.");
   - no em dashes (title became "MOI Protocol Release: v0.13.0");
   - ask whether a hook belongs at the start of a protocol release; the user concluded no.
4. Split into the X thread, one post per release-note section, as numbered files `social/thread/1.txt` to `7.txt`:
   - 1 title and release time; 2 Fee Payer; 3 KMOI Native Asset; 4 Participant List; 5 ANU (with the two changed prices); 6 Action required; 7 SDK Versions.
   - Each post begins with the section name on its own line, then a blank line, then the sentence(s). Longest post is 248 characters (`thread/4.txt`), so every post is under 280.
5. LinkedIn: the whole note as one post, headings as plain lines, hyphen bullets, no backticks (X and LinkedIn render backticks literally, `SOCIAL.md` lines 3-6).
6. Settle the release time wording (see Traps). The final scheduled text says "scheduled for today at 12:00 AM UTC".
7. Dry run each post (no `--confirm`; nothing reaches Buffer):
   - `node scripts/buffer.mjs channels`
   - `node scripts/buffer.mjs post --thread-dir protocol-release-0.13.0/social/thread --channel <X channel id> --at "2026-09-10T08:45:00Z"`
   - `node scripts/buffer.mjs post --file protocol-release-0.13.0/social/linkedin.txt --channel <LinkedIn channel id> --at "2026-09-10T08:45:00Z"`
   - Read the printed `fate` line. It says `PUBLISHES AUTOMATICALLY at <UTC string>, nobody reviews it` for scheduled posts and `DRAFT` for drafts. For a thread it also prints `thread of N posts: 196 / 150 / ... chars`.
8. Send: re-run the same command with `--confirm`; add `--draft` to park it in Buffer for a human instead (`--draft` ignores `--at`).
9. Check Buffer (`publish.buffer.com`, channel, Drafts or Scheduled). Deleting a wrong post is done in the Buffer UI; `buffer.mjs` has no delete command (the user did this twice on 10 Sep, `_user-requests.txt:1190-1192`).
10. Optional correction reply: `social/x-correction-reply.txt` ("Correction: the moipod v0.13.0 network update is scheduled for 00:00 UTC on 11 September, not 12:00 UTC today.") for an X reply if the time was misread. Whether it was ever posted is unknown.
11. Record what was sent: `protocol-release-0.13.0/SOCIAL.md`, committed as `27efaa3` ("release: social pack for moipod v0.13.0") at 14:52 +0400, about two hours after the posts went out.
12. Discord version (written the next day, `_user-requests.txt:1292`): the same content as a Discord message with bold lead-ins and a final "Full release notes: RELEASE_URL" line. `buffer.mjs` cannot post to Discord; the website repo's `scripts/lib/senders.js` can, through a webhook, but that needs `social/<slug>.md` (see the distribution process). How the Discord post was actually sent is unknown.

### Deliverables and where they end up
- Buffer-scheduled X thread on the MOI_Tech X account and a LinkedIn post on the moi-tech company page.
- Files: `protocol-release-0.13.0/social/thread/1-7.txt`, `linkedin.txt`, `x.txt`, `discord.txt`, `x-correction-reply.txt`, plus `SOCIAL.md` as the record.

### Accounts and tools
- Buffer: needs an API key. `scripts/buffer.mjs` reads `BUFFER_API_KEY` from a `.env` at the root of the repo that holds the script (`ROOT` is the parent of `scripts/`), or from the process environment. Last occurrence in `.env` wins (so appending a rotated key works); an already-set environment variable beats the file. Only a Buffer organisation owner can create a key (`moi-blog/references/buffer.md`). The user said the API key question is one he will deal with at the end of the DevRel handover.
- X and LinkedIn: connected inside Buffer; no direct login is used by the script.
- Node (v24 was used). No other dependency; the script is dependency free.
- In the worktree, `BUFFER_API_KEY` appears (twice) only in `session-8-policies/.env`; the root `.env` has `DATABASE_URL` only. Not checked: where the key was when the posts were sent.

### Quality rules and house style applied
- Verbatim from the protocol team where the user said so; restructure only for clarity; add no facts (`SOCIAL.md` line 4: "no facts added").
- Each sentence must make sense read alone (the user asked for that check on every sentence, `_user-requests.txt:1167`).
- Plain text only: no backticks, no bold markers, hyphen bullets, no emoji, no em dashes.
- Announcement only, pointing at the release notes; not a detailed write-up. The user asked whether "serious protocols" post monotone release notes and concluded these posts should not carry much detail (`_user-requests.txt:1203-1204`).
- No hook for a protocol release (decided at `_user-requests.txt:1174-1175`).
- The unnamed team reviewer wanted: "communicate that a new version will be launched and with x, y, z capabilities and it is scheduled for time T. Devs might need to upgrade to the latest version" and messages "optimised as per the medium" (`_user-requests.txt:1193`). The user's answer was that he had followed the exact standard he was given and that protocol releases must be kept simple (`:1194`). The rewritten pack (`x.txt`, `linkedin.txt`) matches the reviewer's ask. The conflict is unresolved (Open questions).

### Traps and things that failed silently
- **Release time ambiguity.** The note says "today at 12:00 AM UTC". The post was scheduled on 10 Sep, roughly 08:45 UTC, so "today at 12:00 AM UTC" had already passed and many readers would read it as noon. The user himself asked whether 12:00 UTC means 12:00 AM and whether "00:00 AM UTC" is the correct form (`_user-requests.txt:1186-1188`); two wrong schedules were deleted by hand (`:1190-1192`). The correction reply file states the real moment: 00:00 UTC on 11 September. The rewritten pack uses "11 September at 12:00 AM UTC (5:30 AM IST)".
- **`SOCIAL.md` is internally inconsistent.** Its header says the time was "corrected to 12:00 UTC (noon) per the user" while its own post text says 12:00 AM UTC. It also says `social/linkedin.txt` was sent to Buffer, but `linkedin.txt` now holds the shorter rewrite (mtime 04:46, four minutes after `SOCIAL.md` and `thread/1.txt` at 04:42). The text actually sent is the LinkedIn text inline in `SOCIAL.md` (inferred). Do not trust the folder as a record of what went out.
- **`RELEASE-NOTE.md` is labelled "as sent by the protocol team, unedited" but is not.** The note the user pasted had an em dash in the title and the sentence "We are rolling out moipod v0.13.0 with several important updates", plus separate sentences about the sender not paying (`_user-requests.txt:1158, 1169`). `RELEASE-NOTE.md` has the restructured sentences from the thread. The original is not in the repo (file mtime Sep 11 01:31, after the post; inferred: regenerated from the thread).
- **Placeholders ship literally.** `discord.txt` and `linkedin.txt` end with `RELEASE_URL`. `buffer.mjs` does not check for placeholders. The same family exists in the webinar packs (`LUMA_URL`, `CANONICAL_URL`).
- **`--at` without a timezone is local time.** `Date.parse("2026-09-10T08:45:00")` uses the machine's zone. Always end in `Z`, and read the printed UTC string before `--confirm`.
- **A scheduled post publishes with nobody reviewing it.** `buffer.mjs` is the opposite of the website pipeline's draft-only guarantee. The reviewer's complaint (the user "posted directly on our socials") is the cost of that. Use `--draft` unless an exact publish time matters.
- **No length check in `buffer.mjs`.** It prints characters per post but does not stop at 280 (the website pipeline does, counting URLs as 23).
- **Thread files must be named `<n>.txt`** (regex `^\d+\.txt$`, numeric sort). The first file is the root post and is also repeated in the thread metadata. `--thread-dir` works only for the `twitter` service and cannot be combined with `--follow`.
- **Run from the repo root.** On 31 Aug the command failed because the user ran it from inside `session-8-policies/`, where `scripts/buffer.mjs` does not exist (`_user-requests.txt:913`).
- **A Buffer API key was pasted into chat on 31 Aug** and then revoked (`_user-requests.txt:910`, "i revoked the key i accidentally posted"). Keys go into `.env` only. A stale revoked key left above the new one in `.env` is harmless only because of the last-wins rule; the symptom of a stale key is "access token is not valid".
- "Voyage devnet" wording: the user later corrected this (see Rules). `discord.txt` still says "live on Voyage devnet".

### How long it takes
About one to two hours from receiving the note to a scheduled post, including the wording and time-confusion loops (inferred from prompt order and file mtimes; scheduled 12:45 PM Dubai).

### Open questions
See the consolidated list. Key ones: was the rewrite pack or the correction reply ever sent; verbatim versus rewritten; Discord delivery mechanism; what `RELEASE_URL` should be.

---

## Process: Release blog post ("MOI <Month> 2026 Release")

### Purpose
One text artifact per release that developers, AI crawlers and the team can cite: what changed, what breaks, what to do, with exact versions. Published at `https://blog.moi.technology/article/<slug>/`.

### Trigger or cadence
- August: Rahul asked in Discord (14 Aug 2026, 12:27 and 14:28) for every service owner to post `service:version:<github-link>` (for example `go-moi:v0.12.0`) because "the marketing team will use this to publish the release blog" (`_user-requests.txt:1495, 2016`; the message is truncated). The post was drafted from 18 Aug and merged 21 Aug 2026 (PR #36).
- September: the protocol team's release note (above). PR #53 was opened 10 Sep 13:26 UTC and merged 11 Sep 13:04 UTC, about 13 hours after the network upgrade moment.
- Cadence: one per month so far (inferred).

### Who does it
Adithya writes and ships it (byline "Adithya Ganesh, Ecosystem, Sarva Labs" in September; "Sarva Labs, Engineering" in August). Rahul does the internal review and gives framing direction. Abhinav Agarwalla's docs PR #120 on `sarvalabs/moidocs` (access policy and storage-cost tutorials) was cross-checked for the August post (`_user-requests.txt:2093`). Srikar did the blog hosting and deploy workflow.

### Inputs needed before starting
- Per component: the GitHub release page and tag (August had 12 entries: go-moi v0.12.0, go-pisa v0.8.0, cocolang v0.9.0, vscode-coco v0.4.0, js-moi-sdk v0.8.0, js-moi-agent-registry v0.3.0-rc1, voyage v0.8.2 and v0.9.0, voyage-api v0.8.2, moi-wallet-extension v0.1.4 and v0.1.5; from the post's `takeaways`).
- Source at the tagged versions. The private repos are cloned locally and readable (`~/go-moi-1`, tip via `git show origin/develop:<path>`; `~/go/pkg/mod/github.com/sarvalabs/go-pisa@v0.8.0`; published npm packages for js-moi-sdk). Never cite private paths in the public post (memory `moi-source-on-disk.md`).
- The previous release post as the genre sibling.
- Docs links for implementation detail (docs.moi.technology, the Sponsor Interactions tutorial, GitHub release pages).
- The live devnet state if the post says "live on devnet".

### Steps in order
1. Write `blog/src/content/posts/<slug>.md`, frontmatter first. Slug pattern: `moi-<month>-<year>-release` (`moi-september-2026-release`). Title pattern: `MOI <Month> 2026 Release: <what changed in plain words>`; August's title originally led with the version and was changed to lead with the month (`3aacb49`).
2. Frontmatter (contract in `moi-blog/references/authoring.md`): `title`, `summary` (kept short for the meta description; a PR #53 commit is titled for exactly that), `date` (the day it goes live; for August the user said "put date as today", `_user-requests.txt:1561, 1571`; September's date is the release day, 2026-09-11), `author`, `tags` (September: `protocol, native-assets, release, moipod, fee-delegation, kmoi`; only `agents`, `protocol`, `native-assets` are visible tags), exactly 8 `takeaways`, 7 to 13 `faq` entries (September has 7), `draft: false`. No `cover`.
3. Body shape used in September (`blog/src/content/posts/moi-september-2026-release.md`): bold one-sentence opening; a plain-language glossary list ("Four terms come up throughout"); `## What changed in moipod v0.13.0?` with a table (What you get, Can it break your code?); one question-H2 section per change; `## What do developers need to change?` (numbered list, most likely break first); `## Everything shipped` (component, exact version, what it carries); `## What to do now` (ordered runbook, starts with the `npm i` line); `## Key takeaways, recap`; closing `<Subscribe />`. August used the same skeleton with per-package subsections and an operator section.
4. Verify every claim (process below). Run the polish passes (process below).
5. `npm run build --prefix blog` (validates frontmatter) and `npm run build` at the root; `npm run dev --prefix blog` to read it at localhost:4321. Grep for `<!--` and em dashes first (PR #53 states "No em dashes, no HTML comments, no cover").
6. Open a PR from `blog/<slug>`. Title: `blog: MOI September 2026 release (moipod v0.13.0, fee delegation)`. Body used in #53: Summary (who it is for, framing, slug and URL); Shape (word count, H2 count, takeaways, FAQ, runbook); Verification (what was checked against which tags, packages and how many claims, build results); "Before marking ready" checkboxes (including the unresolved "Confirm the go-live date ... the go-moi tag is dated 10 September" and "Internal review (Rahul)"); "Nothing is announced by merging".
7. Read it on the preview: `https://pr-<N>-blog.preview.moi.technology/article/<slug>/`.
8. To compare an earlier text version against the current one, open a preview-only PR of the earlier commit (PR #55: "preview only: release post before the 16:18 edit (9de7ee3), do not merge", closed after comparing; the user asked for this at `_user-requests.txt:1309-1310`).
9. Apply review direction in small commits (PR #53 had 24 commits, squashed on merge; see Rules for what was changed).
10. Merge. `deploy.yml` publishes; merging announces nothing. The Prepare social copy workflow opened PR #56 (`social: copy for moi-september-2026-release`) 26 seconds after the merge (13:04:56 to 13:05:22 UTC).
11. Announce and measure (distribution process). Request indexing in Search Console for the new URL.

### Deliverables and where they end up
The post at `blog.moi.technology/article/<slug>/`, in `/rss.xml`, `/rss-email.xml`, `/llms.txt`, the sitemap, and the apex `moi.technology/blog` listing (after the root build). Feeds the Mailchimp RSS newsletter on its next cycle.

### Accounts and tools
GitHub (repo `sarvalabs/MOI-Website`; the user switched `gh` auth to the sarvalabs account on 11 Sep, `_user-requests.txt:30`). No keys needed to write or build. Search Console and GA4 need logins (covered by the existing skill).

### Quality rules and house style
See Rules and house style. The two that mattered most in September: lead with what the developer can now do, and say each thing in plain words with no vague nouns.

### Traps
- The two builds validate differently; run both (existing skill).
- Count consistency: the September post says "three breaking changes" in the opening, "Four changes for developers" in the table, and "Five things break" in the checklist (granularity differs: changes versus code breakages). Pick one framing per audience or label the granularity (inferred risk; the commit "soften breaking-change count" shows the user already touched this).
- "Participant: an account on MOI" in the glossary may conflict with the founder's 14 Sep correction that MOI is participant-centric and the account is only the vehicle for a participant's state (memory `moi-terminology-corrections.md`). The post predates that call. (inferred; needs a decision)
- "Voyage devnet" (post line 40 and a takeaway) versus the user's 25 Sep correction "it's not called Voyage devnet, just say went live on devnet" (`_user-requests.txt:1375`; the correction was made on a deck script, not on the post).
- The published post still contains "not save a setting, not call your logic" and "Your app holds one funded account and names it as the payer" in places; on 25 Sep the user removed those from the community-call deck script (`_user-requests.txt:1377`). Whether to change the post is unknown.
- PR #53 body and commits carry the Claude co-author trailer and the "Generated with Claude Code" footer. The user later ruled that no attribution lines go on commits or PRs (memory `no-claude-attribution.md`, 1 Oct 2026). Do not add them.

### How long it takes
September: about 24 hours wall clock from PR open to merge, 24 commits, most of it review-driven rewrites. August: about 2.5 days, more than 30 commits (`git log` on `moi-august-2026-release.md`, 19 to 21 Aug).

### Open questions
Byline and role policy; whether the post is ever amended after publication and how (`updated`); whether a Medium copy is still expected (Medium is in the footer list; the first blog on 8 Aug went to Medium only).

---

## Process: Claim ledger and independent verification of a release post

### Purpose
A release post that misstates the protocol is worse than no post (existing skill, `authoring.md`). Release notes are a lead, not evidence. This is the step that turned the August and September posts from drafts into publishable ones.

### Trigger or cadence
Every release post, after the draft exists and again after any substantive rewrite. The user triggers it explicitly: "isolate every single claim in this blog and make a list of all claims separated, then do a report independently verifying each claim one by one" (`_user-requests.txt:53`) and "test every claim from the release" (`:1294`).

### Who does it
The assistant, at the user's explicit request. In September the user allowed Haiku or Sonnet sub-agents for it; in August "only Haiku agents" (`_user-requests.txt:2114`). Memory rule: never spawn sub-agents or workflows unless the user asks in that message; when asked, Haiku or Sonnet only and keep the agent count small (`no-multi-agent-workflows.md`).

### Inputs
The draft post; the release note; source at tags; published packages; the live devnet; the docs.

### Steps in order
1. Split the post into atomic claims, one per line, numbered.
2. Verify each against source in this authority order: tagged source (go-moi `v0.12.0`/`v0.13.0`, go-pisa, js-moi-sdk published package), then release notes, then docs.moi.technology (weakest; it had op-code numbers swapped in August).
3. Record a verdict per claim. Vocabulary used in `session-7/blog-assets/factcheck-report.md`: VERIFIED, TRUE, SUPPORTED, OVERSTATED, ARGUABLE, SCOPED, UNVERIFIABLE, FALSE, FIXED, INTERNAL, SECTION CUT, with an Evidence column.
4. Run an adversarial refuter on every claim that was changed in a rewrite (September: 86 changed claims, each with a checker and a refuter).
5. Run companion checks: reviewer-direction compliance, style, links resolve, internal consistency, code samples compile or match the published SDK.
6. Fix every flagged item, then re-run on what changed. September counts: first independent pass 200 atomic claims (187 true, 8 partly, 5 unverifiable, 0 false); a later sweep logged 152 claims and three corrections (`280ffb2` commit message).
7. Where notes and source disagree and there is no ruling, word the post so it contradicts neither and raise the discrepancy separately (existing skill, commit `5c0f763`).
8. For "live on devnet", check the live node: `net.Version` and the wire field name (`payer` versus `fee_payer`); tip-of-develop features are not live until devnet redeploys (memory `devnet-build-lag.md`; the post later says "live since 11 September", checked after the upgrade).
9. Anything that rests only on the release note gets softened (`280ffb2`: "soften the two claims that rest only on the release note").

### Deliverables
A verdict table kept in the PR body or a report (August: a 15-agent run; September: counts in the PR #53 "Verification" section). The existing example of the table format is `session-7/blog-assets/factcheck-report.md`.

### Quality rules
Corrections the check actually caught: see `moi-blog/references/authoring.md` table (August) and, for September, the commit message of `280ffb2`: the MAS0 versus MASN class for the KMOI sample, failed interactions still charge the payer, an access-policies link that 404ed, a paragraph that contradicted the participant-list rule, and a recap bullet that omitted the notarizing-fee-payer exception.

### Traps
- Asking the assistant "is this 100% true" is the user's normal behaviour; he asked it of at least five September sentences (`_user-requests.txt:31-38`). A confident answer must come from source, and a "yes" that rests on the release note alone is not enough. Examples he probed: whether a manager can mint KMOI (no, MASN reserves Mint/Burn for the protocol), whether `MAS0AssetLogic` keeps working for transfers, whether a payer must be a regular account, whether signing the raw interaction object is part of this release.
- Unresolved at PR time: the go-live date versus the go-moi tag date (10 September).

### How long it takes
Not recorded; the August run was one multi-agent workflow plus follow-up; September was spread across the 24 commits.

---

## Process: Polish passes on release prose (humanizer, stop-slop, readability jury, GEO)

### Purpose
Make the post plain and unmistakably human to a developer audience that reads generated copy as a negative signal.

### Trigger or cadence
Every post and every social draft. The user says "use humanize after every paragraph" (`_user-requests.txt:1268`), "run it through the blog skills and humanizer" (`:1296`), and "check one last time for GEO and stop slop and humanized; for the latter two don't make any changes, just identify the changes" (`:1325-1326`).

### Steps in order
1. Draft, then run the `humanizer` skill per paragraph or section.
2. Run the `stop-slop` skill. On 11 Sep the user said to apply "all but the first" of its suggestions (`:1326`).
3. For release posts, a readability jury of agents was used in August (`_user-requests.txt:2104`; the existing skill records newcomer score 61 to 87 after first-use glosses were added, and a "six-lens jury" in commit `90b7f8e`).
4. Read-alone test on every sentence (social copy: each post must stand alone).
5. GEO check: summary, takeaways, FAQ schema, question H2s, backlinks, absolute sibling URLs (existing skill `geo.md`). In "identify only" mode, list the proposed changes without applying them.
6. Final read-through by the user on the preview URL.

### Quality rules
See Rules and house style.

### Traps
- The existing skill's humanizer versus stop-slop em dash analysis is out of date (see below): the user's current rule is no em dashes.
- The final 11 Sep stop-slop commit made "active voice in ten places, one rhetorical question turned into a statement, one meta-joiner dropped" (`280ffb2`); more passes after the user's read-through keep reintroducing the vague phrasing the user rejected earlier. Re-read the opener and the KMOI/anu sections after every automated pass.

---

## Process: Announcing a published post (Prepare, Distribute, Buffer draft, human publish)

This is already documented thoroughly in `moi-blog/references/distribution.md` and `buffer.md`, and it matches the code I read. Summary of what I confirmed, then the deltas.

### Purpose
Announce a merged blog post on X, LinkedIn (and optionally Discord and Telegram) with hand-written copy and UTM-tagged links, without anything auto-publishing to a timeline.

### Trigger or cadence
A new post file added to `main` (the workflow uses `--diff-filter=A`, so edits never re-announce). Per post.

### Steps in order (confirmed against `.github/workflows/*.yml` and `scripts/`)
1. Merge the post PR. `social-prepare.yml` opens a PR adding `social/<slug>.md` (observed: PR #56, branch `social/moi-september-2026-release-34602311546`, 26 seconds later).
2. Rewrite every block by hand. The seeded text is the post's `summary` repeated (observed in PR #56: all four channels carry the same summary sentence). Empty a channel to skip it. Keep `{{link}}`; it renders the UTM-tagged URL.
3. Merge that copy PR. (`distribute.yml` checks out `main`; running it earlier dies with "No copy file at social/<slug>.md".)
4. Actions, Distribute a post, inputs `slug`, `channels`, `dry_run: true`; read the output; re-run with `dry_run: false`.
5. In Buffer, open the X and LinkedIn drafts, add an image (the API attaches none), rewrite the hook, publish.
6. `npm run social:links <slug> -- --md` for tagged links; measure in GA4 by `utm_campaign=<slug>` and in Search Console.

### Deliverables
Buffer drafts for X and LinkedIn; immediate posts to Discord and Telegram if their secrets are set. Copy files in `social/`.

### Accounts and tools
GitHub Actions secrets `BUFFER_ACCESS_TOKEN`, `BUFFER_CHANNEL_X`, `BUFFER_CHANNEL_LINKEDIN`, `DISCORD_WEBHOOK_URL`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`. Note the naming split: the website pipeline uses `BUFFER_ACCESS_TOKEN`; `scripts/buffer.mjs` uses `BUFFER_API_KEY`.

### Quality rules applied to copy (from `social/*.md` and the 31 Aug commit `f99e348`)
- One written X post and one written LinkedIn post per article, drafted from the article with the house voice rules, passed through stop-slop and humanizer, every specific claim re-checked against the post. X 213-259 of 280 with the link at 23 characters; LinkedIn about 1,058-1,373 of 3,000.
- X and LinkedIn only: on 31 Aug the user decided no Discord or Telegram for the August posts ("no need for discord and tg", `_user-requests.txt:2461`), and `f99e348` removed those blocks from all copy files because those channels "were never configured".
- Hooks are written to the reader's likely ignorance (the Voyage copy notes: "X/LinkedIn hooks assume the reader may not know what Voyage is").

### Traps (beyond the existing skill)
- `scaffold()` still seeds all four channels including Discord and Telegram, even after the 31 Aug X-and-LinkedIn-only decision (observed in PR #56). Empty them by hand or a configured webhook will post the unrewritten summary.
- As of 2 Oct 2026 PR #56 is still OPEN, so no evidence shows the September release post was announced through the pipeline (or at all). Unknown whether it was announced by hand.
- The pre-release pack above went out through a different tool with different guarantees (scheduled, no UTM, no reviewer gate). A new hire needs to know there are two paths and which to use when.

### How long it takes
Not recorded.

---

## Process: Newsletter (Mailchimp weekly RSS and one-off segment blasts)

Documented in `moi-blog/references/mailchimp.md`; I confirm the evidence and add the one-off blast.

- Weekly RSS blast set up by Adithya on 24 Aug ("sends a weekly mail blast if and only if any new blogs have gone up in that duration"), with Sai Kiran and Vardan Aggarwal asked for three things about the sender identity (message at `_user-requests.txt:2360`, truncated).
- One-off blast to all MOI validators for the Voyage-to-MOI-Wallet login migration (28 to 31 Aug, `_user-requests.txt:2434-2475`). The user asked for subject line, the HTML to paste, and the MOI logo; he removed a line about the faucet and the network rename from the email copy. The steps given by the assistant are not in the evidence. The user asked to keep everything ready but not schedule or post anything until GitHub was back (`:2444-2445`).
- Confidence is lower than for the other processes because the evidence is the existing skill plus the user's prompts, not artifacts.

---

## Adjacent (owned by the webinar researcher; evidence noted so it is not lost)

- Launch-day X and LinkedIn posts for each webinar, scheduled through `buffer.mjs --at`, with a "we're live in 30" X post 30 minutes before start (`_user-requests.txt:1081, 1084`).
- Webinar link rules: the Luma link goes in the LinkedIn post body, not in the first comment (`:1039`).
- Webinar social packs (`session-8-policies/SOCIAL.md`): single X post, 5-post thread, LinkedIn; "No emoji, per brand voice"; replace `LUMA_URL` before scheduling; link the Luma before the session and the blog after.
- Medium cross-posting (`session-7/blog-assets/PUBLISH.md`): publishing on Medium first makes Medium the canonical version unless the canonical link is later pointed at the site.

---

## Reusable assets

Release pack (worktree = `/Users/adithyaganesh/MOI-Webinars/.claude/worktrees/relaxed-mccarthy-368dbc`):

| Asset | Path | Use |
|---|---|---|
| Release-note intake and X/LinkedIn/Discord text | `<worktree>/protocol-release-0.13.0/RELEASE-NOTE.md`, `SOCIAL.md`, `social/x.txt`, `linkedin.txt`, `discord.txt` | Worked example of a release pack. Mind the Traps (stale header, `RELEASE_URL`, mislabelled "unedited") |
| Thread skeleton (7 posts) | `<worktree>/protocol-release-0.13.0/social/thread/1.txt` to `7.txt` | Section-per-post thread: title and time, one post per change, Action required, SDK versions |
| Correction reply | `<worktree>/protocol-release-0.13.0/social/x-correction-reply.txt` | Template for correcting a wrong time |
| Buffer scheduler | `<worktree>/scripts/buffer.mjs` | `channels`, `post --file`, `--thread-dir`, `--follow`, `--at`, `--draft`, `--confirm`; dry run by default |
| Webinar social pack format | `<worktree>/session-8-policies/SOCIAL.md`, `<worktree>/session-7/blog-assets/social-pack.md` | Single post, thread, LinkedIn layouts with notes |
| Fact-check report format | `<worktree>/session-7/blog-assets/factcheck-report.md` | Verdict table with Evidence column |
| Medium publish checklist | `<worktree>/session-7/blog-assets/PUBLISH.md`, `MEDIUM.md`, `schema.jsonld` | Cross-posting steps and the canonical URL warning |
| Strategy meeting | `<worktree>/otter-transcript/Project Launch and Blog Strategy_summary.txt` and `_transcript.txt` | Source for the content strategy decisions (this is gitignored; internal) |

Website repo (`/Users/adithyaganesh/untitled folder 10/MOI-Website`):

| Asset | Path | Use |
|---|---|---|
| September release post | `blog/src/content/posts/moi-september-2026-release.md` | Latest release post, the template to copy; PR #53 |
| August release post | `blog/src/content/posts/moi-august-2026-release.md` | Per-package release post, includes operator section and op-code table |
| Voyage migration post | `blog/src/content/posts/move-your-voyage-login-to-moi-wallet.md` | Short how-to with a 7-plus-question FAQ |
| Copy files | `social/moi-august-2026-release.md`, `social/move-your-voyage-login-to-moi-wallet.md`, `social/README.md` | Hand-written X and LinkedIn copy examples |
| Pipeline | `scripts/social-init.js`, `scripts/distribute.js`, `scripts/lib/social.js`, `scripts/lib/senders.js`, `scripts/lib/share.js`, `scripts/share-links.js`, `scripts/buffer-channels.js` | Draft-only distribution |
| Workflows | `.github/workflows/social-prepare.yml`, `.github/workflows/distribute.yml`, `.github/workflows/preview.yml` | Prepare, Distribute, per-PR previews |
| Example PRs | `https://github.com/sarvalabs/MOI-Website/pull/53` (release post, with Verification and Before marking ready sections), `/pull/55` (preview-only comparison PR), `/pull/56` (seeded copy PR) | PR body template and conventions |

Existing skill (`/Users/adithyaganesh/.claude/skills/moi-blog/`): `SKILL.md`, `references/authoring.md`, `distribution.md`, `buffer.md`, `geo.md`, `mailchimp.md`, `assets.md`, `mailchimp-header.html`, `mailchimp-body.html`, `mailchimp-footer.html`. Do not paste `mailchimp-template.html` (documented as broken).

---

## Rules and house style

All user-stated or user-enforced unless marked "(inferred)". Sources in brackets.

Release posts:

1. **Open with what the developer can now do.** The accepted September opening is "You can now pay fuel for another user." Three earlier openings were rejected in sequence for being abstract, for using vague nouns ("the fee"), and for overgeneralising (`_user-requests.txt:1298-1312`). Final structure: new capability first, then "Outside of that, there are three breaking changes that affect developers", then name them, then "Each of these is covered in detail later in this post." (`:1313-1314`).
2. **Plain words, short sentences, one point per paragraph.** The commit sequence says it: "release post in plain language", "split three long sentences", "one point per paragraph" (`280ffb2`).
3. **Name the thing; never "the token" or "the fee".** Objections to the phrase "MOI's own token" and to a bare "the token" were the strongest complaints of the session, paraphrased here without the profanity (`_user-requests.txt:42-44`). Write KMOI by name, define it once ("the native token of the MOI network, like ETH on Ethereum"), then say what it is measured in (anu, the way Ethereum counts ETH in wei).
4. **Define a term before using it, and use the same word every time.** Fee delegation is the feature; fee payer is the role; fuel is what is paid (the user asked whether to write "fee payer (fuel)", `:1165-1166`). Say "capped supply" and not "fixed supply" anywhere (`:36`).
5. **Never state a universal the protocol does not guarantee.** "Every action on MOI costs fuel" and "every interaction sent to MOI costs fuel" were both removed as exaggerations (`:1305-1306`).
6. **Do not define fuel in the opener** (`:1307-1312`, "fuel is the fee for using the MOI network, rm").
7. **Benefit for developers is the frame; code is minimal; link to docs for implementation.** August: "keep the blog explanatory, no need to have too much code, attach the docs link, this blog should just be high-level releases" (`:2122`). September: developer-focused, one three-call code sample, a runbook.
8. **No pictures, no cover image in release posts** (August, `:2117` "rm the pictures"; `902f78e`). September has no cover.
9. **Cut scope the user cuts.** The agents section and the x402 paragraph were removed from the September post (`:55`, commit message). Release posts do not claim an x402 integration.
10. **Keep release candidate versions as written.** "0.9.0-rc2" stays as the version, with no explanatory sentence about what an RC is (August `8157fbb` "the rc1 suffix speaks for itself"; user at `_user-requests.txt:1564` "drop the explicit sentences, keep the rc1").
11. **Decide per release which version is "the default" and do not tell readers to upgrade to something the user has not confirmed is the latest compatible one.** August: the user first said to drop the agent-registry rc1 and keep js-moi-sdk 0.8.0 as the default "don't tell them to upgrade" (`:1552`), then said the agent-registry release should be in the post (`:1555`); the outcome was rc1 kept, upgrade-instruction sentences dropped (`:1564`).
12. **Structure for GEO** (existing skill, confirmed in September): question H2s (6 of 9), bold opening claim, glossary list near the top, 8 takeaways, 7 to 13 FAQ entries, exact versions in a table, recap section, absolute `https://blog.moi.technology/article/<slug>/` links to siblings, links to the SDK repo, docs and earlier posts.
13. **Em dashes: none.** September post has zero; the Voyage post has zero; the user said "no em dashes" for the social posts (`:1176`). The August post has 17. This supersedes the existing skill's "match the sibling's rate" guidance.
14. **Headings and labels in social copy:** the user asked for a colon after section labels ("Fee payer:", `:1164`); the final thread files use a bare label line instead. Which is canonical is unclear (Open questions).
15. **Terminology** (memory `moi-terminology-corrections.md`, 14 Sep): participant-centric, not account-centric; Sarva Labs designs and develops, the MOI Foundation governs; say "network ID", not "chain ID". And: "Devnet" is the network's name; do not write "Voyage devnet" (`:1375`, 25 Sep).
16. **Source authority order:** tagged source, then release notes, then docs.moi.technology (existing skill).

Social copy:

17. **Release announcements stay simple and point to the release notes** (`:1203-1204`). No hook (`:1174-1175`).
18. **Verbatim when the user says verbatim.** Restructure only for clarity, add nothing (`SOCIAL.md` line 4).
19. **Each post must stand alone** (read-alone test, `:1167`).
20. **No emoji, no hashtags are recorded as used.** "No emoji, per brand voice" appears in `session-8-policies/SOCIAL.md`. The user asked whether hashtags help reach (`:972`); the answer is not in the evidence.
21. **Shorter is better on LinkedIn, and do not leak implementation trivia.** The user cut a LinkedIn draft as too long and removed specifics like a builtin error name and "86 fuel" (`:914, 920, 1037`).
22. **AI-slop sentences get cut on sight.** Examples rejected: "and it is the part worth caring about." (`:966`), "That is not a rule other chains enforce and we relaxed." (`:967`), "Most teams quietly accept both" (vague attribution; the assistant itself flagged it, `:932-933`), "not this, not that" constructions in speech and posts (`:1063`).
23. **Plain English over jargon in comparisons:** "Off chain, the service owns the row" was rewritten as an entry in the app's backend service (`:965`).
24. **Links:** webinar Luma link goes in the LinkedIn post body, not the first comment (`:1039`). Whether to put the blog link in the X post body or as the second post is unresolved; the website pipeline puts `{{link}}` in the body, `buffer.mjs --follow` puts it second "because links in the post body suppress reach" (script comment), and the strategy meeting wanted the link in the post so AI crawlers follow it (see decisions).
25. **Verification gating for posts:** every specific claim in a social post is re-checked against its source article before commit (`f99e348`).
26. **No attribution lines** on commits or PRs (memory, 1 Oct).

Process rules the user enforces:

27. **Do not publish without a human read.** Drafts for X and LinkedIn by default; the user reads the final text and the preview before anything goes out ("gimme the final posts going out 5 hrs [before] ... lemme read it once then you can schedule", `:1038`).
28. **Never schedule on a guess about time.** Confirm the UTC moment and print the UTC string before `--confirm`.
29. **Brief answers.** The user repeatedly asks "brief" and objects to long paragraphs (`:1210, 1273, 1278, 1295, 1317, 1319, 1547, 2024`); explanations to him must be short and in plain language.
30. **One batch of review tweaks, one PR** (memory `batch-review-changes.md`), and nothing pushed that notifies others when told "no PRs" (memory `no-push-no-notify`).

### What the strategy meeting (4 Aug 2026) decided that should shape the skills
(Source: the Otter summary and transcript. Speaker 3 is Adithya; Speaker 2 directs.)

1. **Everything done becomes text content.** All activity must come out as text so LLMs can index it and "improve our scoring"; there was an audit report, "we're doing a lot of stuff but nothing is visible online". Every dev talk, AMA, and any video content is accompanied by a blog.
2. **The blog link is the announcement.** Publish the blog, then tell people "here is the blog, these are the highlights". Adithya does not need to be on every call; the blog is also a testimonial for his work. The manager reviews the blog and says what to highlight.
3. **Structure:** big picture first (the "aha": why we did this), then how-tos; a college student should get the high-level idea, then "what can I do now". Same for DevX content. Phase framing: phase one is identity (register and discover agents), phase two is authority.
4. **Backlinks on purpose:** link the JS SDK, the agent registry SDK, earlier blogs, the native assets docs. "Don't load it up, but as much as possible." The goal is "a comprehensive web of information" for ranking and for AI crawlers.
5. **Markdown, GEO-optimized,** published on the MOI website's blog section, which "should be very simple: take a Markdown file, render it". Also post on Twitter and LinkedIn with the link, because AI systems scanning LinkedIn see only the (short) post content and follow the link to crawl the detail.
6. **Storyline across talks:** break demos into phases (V1 register, discover, facilitate; V2 add authority; V3 more) so each dev talk adds one idea; do not give everything in one day.
7. **Plan a month of content ahead** to avoid last-minute rush ("a one month plan should be ahead"). Adithya managed the process.
8. Product decisions that are not DevRel: integrate the agent dating plugin as a demand driver via points; keep X42 demo to a simple value transfer; use an existing x402 service if one exists.

How these show up in the skills (inferred but direct): a blog per release or event is mandatory; social copy must link the blog (UTM-tagged); every blog follows aha-then-how-to with backlinks; a monthly content calendar exists (the `blog-calendar` skill is available); the manager's review is a gate before promotion.

---

## Traps

1. Release time wording and the word "today" (above). Use date + 24-hour UTC + IST/Dubai conversion in one line, never "today" in a post that is scheduled hours earlier.
2. `buffer.mjs` schedules for automatic publish; the website pipeline only drafts. Know which one you are in.
3. `--at` without `Z` is machine-local time.
4. Placeholders (`RELEASE_URL`, `LUMA_URL`, `CANONICAL_URL`) are not checked by any tool.
5. Folder-as-record drift: `SOCIAL.md`, `linkedin.txt`, and `RELEASE-NOTE.md` disagree with each other and with what was sent.
6. Buffer cannot delete from `buffer.mjs`; deleting is manual in Buffer.
7. Seeded copy repeats the summary and still includes Discord and Telegram blocks; PR #56 for September is still open.
8. Distribute has no idempotency; re-running re-posts to Discord/Telegram and duplicates Buffer drafts (existing skill).
9. Two Buffer variable names: `BUFFER_ACCESS_TOKEN` (website pipeline, GitHub secrets) and `BUFFER_API_KEY` (`buffer.mjs`, local `.env`).
10. Do not paste keys into chat; the Buffer key was revoked once after being pasted. `.env` is gitignored (`**/.env`).
11. Tip-of-develop is not what devnet runs. Verify "live" claims on the wire.
12. Vague nouns and universals ("the token", "the fee", "every action costs fuel") get rejected.
13. The post's three-versus-four-versus-five breaking-change counts.
14. `Participant: an account` glossary versus the participant-centric rule; "Voyage devnet" versus "Devnet".
15. No Claude attribution on commits and PR bodies.
16. The existing skill's repo-wide gotchas still apply: both builds, `<!--` comments, only three visible tags, image caching, `utm_campaign` = slug in lowercase.
17. Sub-agents only when the user asks, Haiku or Sonnet only.
18. A Medium-first post becomes the canonical copy.

---

## Open questions

1. What does `RELEASE_URL` resolve to for a release (the blog post URL, a GitHub release, a docs page)? "Full release notes" is the wording used.
2. Was the rewritten pack (`x.txt`, `linkedin.txt`) or the correction reply (`x-correction-reply.txt`) ever posted? Was the Discord copy ever posted, and through what?
3. Verbatim or rewritten announcement: the reviewer asked for a rewrite "optimised as per the medium"; the user held that the exact standard had been followed. Who decides next time? Who was the reviewer?
4. Canonical wording for the release time: "12:00 AM UTC", "00:00 UTC", or both with IST; and the rule for "today".
5. How does the protocol team deliver the release note (Discord, Slack, email) and who is the named contact? For August the evidence is Rahul's Discord request; for September the user pasted the note.
6. Is a pre-release social pack expected for every release, or was September a one-off? There was no such pack for v0.12.0.
7. Why was PR #56 (social copy for the September post) never merged? Was the blog announced at all, and where?
8. Byline policy: "Sarva Labs, Engineering" (August, Voyage post) or "Adithya Ganesh, Ecosystem, Sarva Labs" (September).
9. Should the published September post change "Voyage devnet" to "Devnet" and the glossary line "Participant: an account on MOI"? Should it drop the lines the user cut from the deck script?
10. Is Medium still a channel? The first blog went to Medium only on 8 Aug; no later release used it.
11. Colon after section labels in social posts (the user's request at `_user-requests.txt:1164`) versus bare label lines in the sent thread.
12. Link placement on X: body versus second post, and the LinkedIn first-comment rule (the user reversed the first-comment rule for Luma links on 4 Sep).
13. Is the weekly Mailchimp RSS blast live and did it include the September post? The in-repo statements conflict (weekly versus per-post).
14. Hashtags: the user asked whether they help; no answer is recorded.
15. Where should `BUFFER_API_KEY` live for a new hire, and who creates it (org owner only)? The user said the API key question comes at the end.
16. Posting-time convention: why 12:45 Dubai (2 PM IST) for a 00:00 UTC release; is there a standard lead time?
17. How long does the claim-verification step take, and is there a budget the user wants stated (credit-cost concern is recorded in memory)?
18. Does the go-live date confirmation (open checkbox in PR #53) have an owner?

---

## What a skill for this should contain

Recommendation: a new skill `moi-release-pack` for the announcement and the release post, plus a refresh of `moi-blog` so the two do not contradict each other. Keep `moi-blog` as the blog/distribution/measurement reference; make `moi-release-pack` the playbook for "a protocol release just happened or is about to".

### What the existing moi-blog skill covers well (keep)
- Publish versus distribute split, and the reasons (`distribution.md`).
- Frontmatter contract and what consumes each field; question H2s; bold opening claim; recap; takeaways = 8; FAQ 7 to 13 (`authoring.md`).
- The verification discipline table with real catches, source authority order, "word it so it contradicts neither".
- Prepare and Distribute workflows, UTM convention, channel limits, X 23-character URLs, no idempotency, `--force` danger.
- Buffer API shape and the introspection debugging lessons; the draft guarantee and why.
- GEO emit table, robots, sitemap, measurement, Mailchimp feed, templates, image caching rule.
All of the sampled facts I re-checked in code and PRs held (Prepare opens the PR within seconds; `social:init` seeds four channels; distribute is dispatch-only).

### What in it is out of date
- Corpus: "four published posts" and "18 URLs, 4 articles, 13 tag pages"; there are now six posts (adds the Voyage migration post, 27 Aug, and the September release, 11 Sep) and open PRs #52 and #54 for two more.
- Em dash guidance (the genre-matching table): the last two posts have zero and the user said no em dashes; make zero the default.
- Channels: it assumes four channels in the loop and the description; the 31 Aug decision is X and LinkedIn only, with Discord and Telegram blocks emptied (the scaffold still seeds them).
- Silence on `scripts/buffer.mjs` (the scheduler), threads, `--follow`, `--at`, delete-by-hand, and the fact that real release announcements were scheduled to publish automatically; "do not add a publish path; answer is a PR" describes only the website pipeline.
- No release-announcement process, no time-zone rules, no correction process.
- No claim-ledger method beyond a table of past catches (no atomic-claim step, no adversarial refuter, no devnet live check, no sub-agent policy).
- Author guidance does not say which byline to use for releases.
- No terminology corrections from 14 Sep and 25 Sep; no "no attribution" rule.
- The distribution step's expectation that a Prepare PR is merged and a distribute run follows is not tracked: PR #56 shows it can stall unnoticed.
- `SKILL.md` end-to-end table has no "T-minus" announcement step, and its description does not trigger on "release note", "protocol release", "thread" or "announcement".

### What a release-pack skill needs that the blog skill lacks
1. A release-note intake step with a fixed list of things to get from the protocol team: version, exact release moment in UTC, change list, breaking list, action-required list, SDK versions, link for "full release notes".
2. Time handling: write the moment as date + 24-hour UTC + IST + Dubai in one line; forbid "today" and bare "12:00 AM"; a converter script; the correction-reply template.
3. The pre-release pack format: X thread of N posts (title and time; one post per change; Action required; SDK versions), a single-post version, LinkedIn, Discord; plain text only; verbatim-or-rewrite decision recorded up front; the read-alone check.
4. A scheduling runbook for `buffer.mjs`: list channels, dry run, read the UTC string, `--draft` first, then `--at ...Z --confirm`, verify in Buffer, how to delete.
5. A pre-send checklist: placeholders replaced, character counts, no em dashes, no backticks, release time re-confirmed with the protocol team, a human has read the final text, reviewer sign-off for public posts.
6. The release blog template and PR body template (Summary, Shape, Verification, Before marking ready, "Nothing is announced by merging").
7. The claim-ledger procedure with verdict vocabulary and source priority, including the live devnet check and when sub-agents are allowed.
8. The voice rules above, with the rejected-phrase list.
9. A record-keeping step so the folder shows what was sent, with a "sent / not sent" field per file.

### SKILL.md outline for `moi-release-pack`
1. When to use (trigger phrases: protocol release, release note, network upgrade, breaking release, announce a release, release thread, correction).
2. The three deliverables and their order: T-minus pack (X thread, LinkedIn, Discord) -> release post PR -> post-publish announcement via the website pipeline.
3. Decision table: which tool for which channel (scheduler vs draft pipeline), and who must approve.
4. Gates (must pass before anything public): time confirmed in UTC, placeholders gone, claims ledger clean, reviewer approval, human read.
5. Steps for each deliverable with exact commands.
6. Voice rules (short, pointing to `references/voice.md`).
7. What never to do: guess the time, schedule without a printed UTC check, auto-publish unreviewed, paste keys, add attribution, spawn sub-agents unasked.
8. Handover notes: who to ask for what (protocol team for note and time; Rahul for review).

### Reference files to bundle
- `references/release-note-intake.md`: the question list, and a worked example from v0.13.0.
- `references/announcement-pack.md`: the thread, LinkedIn, Discord, single X formats with the v0.13.0 text as examples; length limits (X 280 with URLs counted as 23, LinkedIn 3,000, Discord 2,000); plain-text rules.
- `references/time-and-corrections.md`: the 12:00 AM trap, conversion table (12:00 AM UTC = 5:30 AM IST = 4:00 AM Dubai, computed), correction reply template, how to delete in Buffer.
- `references/buffer-mjs.md`: every flag, the `.env` rules (root-level, last wins, env beats file), run-from-root, thread file naming, `--draft` ignores `--at`, no delete, no placeholder check, no length check.
- `references/release-blog.md`: slug and title patterns, frontmatter template with 8 takeaways and 7 FAQs, section skeleton, PR body template, preview-comparison PR trick.
- `references/verification.md`: claim ledger, verdict vocabulary, source order, devnet check, Haiku or Sonnet only when asked, the catches list from August and September.
- `references/voice.md`: the rules and rejected phrases above, plus terminology.
- `references/strategy.md`: the 4 Aug decisions in one page, so the "why" is available.
- `references/past-releases.md`: a table of releases with dates, versions, post slugs, PR numbers, what was announced where, and what is unknown.

### Scripts worth writing
- `release-pack-init`: from a pasted release note create `protocol-release-<ver>/` with `RELEASE-NOTE.md`, thread files split on section headings, `linkedin.txt`, `discord.txt`, `x-correction-reply.txt`, and a `STATUS.md` with sent/not-sent fields.
- `check-pack`: fail on unreplaced `[A-Z_]+_URL`, em dashes, backticks, over-280 posts (X counting URLs as 23), a release time that lacks UTC and a date, the words "today" or "tonight" near a time, and any file without a matching `STATUS.md` entry.
- `utc-times <ISO>`: print UTC, IST, Dubai, and "in N hours from now"; exit non-zero if the moment is in the past.
- `buffer.mjs` hardening (small PR, in the worktree repo): require `Z` or an offset on `--at`, refuse placeholders, enforce 280 per thread post, add `list` and `delete` commands, print the local-time equivalents in the dry run.
- `claims-ledger`: take a post, emit a numbered claim table (claim, source to check, verdict, evidence) as markdown, to be filled in by the verifier; plus a count summary for the PR body.
- `preflight-release-post`: frontmatter checks (8 takeaways, FAQ count, title pattern, `draft: false`, date), grep for `<!--`, em dashes, `# ` headings, "fixed supply", "the token", "the fee", "Voyage devnet"; run both builds; print the preview URL for the PR number.
- `devnet-live-check`: read-only `net.Version` and a sample interaction's field names so "live on devnet" is not asserted blind.

### Templates to bundle
- Release-note intake form.
- X thread skeleton (7 posts), single X post, LinkedIn, Discord, correction reply.
- Release blog post skeleton with frontmatter, glossary list, change table, per-change question H2s, developer checklist, versions table, runbook, recap.
- PR body for a release post (the #53 structure) and the preview-only comparison PR body (#55).
- Claim ledger table and verdict vocabulary.
- Reviewer handoff message (what to check, link to preview).
- The `STATUS.md` for a release folder.

### Changes to make to `moi-blog` at the same time
Update the corpus and counts; replace the em dash genre rule with "none"; add the X-and-LinkedIn-only decision and the Prepare-seeding caveat; add a pointer from `distribution.md` and `buffer.md` to `moi-release-pack` for scheduled posts and threads; add the terminology corrections and "no attribution" rule; add the strategy-meeting rationale as a short "why" section.
