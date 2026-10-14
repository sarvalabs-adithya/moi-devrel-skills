---
name: moi-webinar
description: "Run a MOI Builders session (a live developer webinar where the presenter runs a devnet demo) from topic to bounty, build or check any MOI deck, or run the monthly community call. Use for \"Builders session\", \"webinar\", \"dev talk\", \"Luma event page\", \"registration page\", \"game day\", \"run of show\", \"RUNBOOK\", \"GAMEDAY\", \"demo plan\", \"rehearsal recording\", \"intro session\", and the \"webinar bounty\" on the Points site. Deck branch: \"make the deck\", \"check the deck\", \"export the PDF\", \"presenter notes\", \"SCRIPT.md\", \"slide numbers\", \"read-aloud script\", slides from a Slack dump or report. Community call branch: \"campfire chat\", \"community call\", \"call agenda\", \"monthly call deck\", \"line-up\", \"speakers for the call\", \"host question\", \"YouTube description for the call\", pruning a call deck. The write-up post is moi-blog, the Forge bounties are moi-education-programs, and checking a claim is moi-devrel/claim-check."
---

# MOI webinar

## What this covers
One MOI Builders session: a live developer webinar where the presenter runs one idea on devnet, attendees repeat it afterwards, and a write-up is published. The folder `session-<N>/` sits at the root of a working copy of `moi-foundation/MOI-Webinars`. As of 2026-10-02 sessions 1 to 4, 7 and 8 have a record of being held, sessions 5 and 6 do not (`project-handover-docs/DEV-WEBINARS.md` says nine sessions so far: ASK: Rahul to confirm the count), session 9 is only planned, and a one-off intro session exists (`references/session-history.md`). Claude researches, builds, verifies and explains, and the operator approves every step that leaves the machine.
A deck or the monthly call: skip to the branch table below and read `deck/GUIDE.md` or `community-call/GUIDE.md`. The checklist and the run table are for a Builders session.
Two branches live inside this skill and are read as their own guides:
- `deck`: any MOI deck, for a session, the monthly call or anything else. One HTML file, the presenter window, the read-aloud script, the checker and the PDF.
- `community-call`: the monthly public call, The Campfire Chat. Line-up, numbers ledger, release slides, the host's planted question, the day and the recording description.

Not covered: commits, pull requests, rebases and merges (`moi-devrel/ship`); writing, publishing and announcing the write-up post and the newsletter (`moi-blog`, which takes a session folder as its source), a protocol release pack (`moi-blog/release-pack`), checking claims in general (`moi-devrel/claim-check`), the Forge bounties and awesome-moi (`moi-education-programs`; MOI Sprint was scratched on 13 October 2026), the Points Program as a product (`moi-web-products-ops`), the Agent Launchpad as a product (`moi-launchpad-ops`).

## Before you start
Get the working copy first: `gh repo clone moi-foundation/MOI-Webinars`, then `cd MOI-Webinars`. The schedule, owners and posting rules are in `project-handover-docs/DEV-WEBINARS.md` (the handover repo): read it with this file.
`$SKILLS`, "the operator", "the previous operator" and `ASK: <name>` are defined in `moi-devrel/SKILL.md`. MOI terms (participant, logic, KMOI, fuel) are in `moi-devrel/references/glossary.md`. Set `SKILLS`, quote it, and run every command from the working copy of `moi-foundation/MOI-Webinars`. That repo is public: a push publishes. The scaffold makes the session folder keep its internal files out of git; whether session folders are committed, and on which branch, is a policy nobody has written down. ASK: Rahul. File names like `references/x.md` are inside this skill; in a branch guide they are inside that branch's folder. T is the event start, so T-60 is 60 minutes before it.
- [ ] `references/session-history.md` read: which sessions exist, where their files live and what breaks on today's devnet. The operator provides nothing here; Claude reads it.
- [ ] The session number and its Roman numeral. The numbering after 8 is not settled: session 9 is only planned and its folder already holds a plan on the branch (`references/session-history.md`, "Numbering"). Ask: "Which number does this session take?" ASK: Rahul.
- [ ] Date and start time. Pick a day that avoids Game Night (the community's Friday games night on Discord) and the Community Call, and check the Luma calendar for clashes; Rahul confirms (`references/lifecycle.md`, "Schedule"). Do not default to a Friday. Ask for the IST time, then run `time-table.sh` (step 6).
- [ ] The one idea, with two roles kept apart. The *topic lead* is whoever sets the topic on a call (`references/topic-and-storyline.md`). The *topic approver*, who says the topic goes ahead, is not recorded. ASK: Rahul for the name of each. Ask the lead: "What did you ask for, in your words?"
- [ ] The reviewer who sees the deck and the post before they go public. ASK: Rahul.
- [ ] Who presents. The previous operator presented every session on record. Whether the operator or someone else presents the next one is not settled. ASK: Rahul.
- [ ] The previous session folder to copy forward (`references/demo-standard.md`, "Where the code to copy lives"), and the source for the new mechanism (a docs pull request, the SDK source). The operator provides them.
- [ ] A devnet wallet created and funded by the operator, with its recovery phrase typed by the operator into the session's `.env`. Wallet and mnemonic steps are the operator's. Claude never handles a recovery phrase.
- [ ] The Meet link: Vardan holds the Luma, Google Meet and YouTube logins and provides the Meet link, which is needed on the Monday of the session week.
- [ ] Tools: `bash "$SKILLS/moi-webinar/scripts/session-preflight.sh"` lists what is missing. Work identity: run the identity check in `moi-devrel/SKILL.md` before any commit.

## The run
The rule is nine days from the topic to the session (`project-handover-docs/DEV-WEBINARS.md`); both example sessions went from the lead's call to live in three to four days (`references/lifecycle.md`). `<N>` is the session number. The deck branch takes over at step 4. The monthly call is not a Builders session: it has its own run in `community-call/GUIDE.md`.

| # | Step | What to do | Where or command | Done when |
|---|---|---|---|---|
| 1 | Topic and storyline | Restate the call in plain words and name who set the topic (the topic lead). If nobody has, stop: draft the question to Rahul from `moi-devrel/templates/messages.md` and do not scaffold yet. Then scaffold with `bash "$SKILLS/moi-webinar/scripts/new-session.sh" session-<N> "<title>"` (refuses to overwrite; it also makes the deck through the deck branch's `new-deck.sh`). Fill `STORYLINE.md` | `references/topic-and-storyline.md` | The topic lead has said yes to one idea. Open questions are ASK lines |
| 2 | Demo built and verified | Spike on devnet first, then setup scripts, the demo and one script per live action. A script that loads the recovery phrase from `.env` is a wallet step: the session's `npm run preflight`, the setup scripts, the demo, the per-beat scripts and every rehearsal. The operator runs it in their own terminal and pastes the output. Claude reads output only. GATE: anything that spends devnet funds needs a yes that names the paying account and the cost. Every hash in full in `NOTES.md` | `references/demo-standard.md` | The operator's pasted output shows `preflight` and `demo` exit 0 on the current node. Each claim is labelled doc-derived, source-derived or receipt-proven |
| 3 | Run of show | Write `RUNBOOK.md` and `GAMEDAY.md`. Refer to slides by title | `references/run-of-show.md` | One clock. The operator has read both |
| 4 | Deck and script | `SCRIPT.md` holds the words. Build, sync, check and render the deck with the deck branch, where `<s>` is `session-<N>` and the scaffold has already made `session-<N>/deck/` and `SCRIPT.md` | `deck/GUIDE.md`, from its step 2 | The deck checker has no FAIL. The PDF page count matches the slide count |
| 5 | Claim check | `python3 "$SKILLS/moi-devrel/claim-check/scripts/extract-claims.py" --all session-<N>/SCRIPT.md session-<N>/LUMA.md session-<N>/SOCIAL.md > session-<N>/claims-candidates.csv`. `--all` lists every sentence, because the default run skips plain statements. Copy the rows you keep into `session-<N>/ledger.csv` (the scaffold made it from `$SKILLS/moi-devrel/claim-check/templates/claim-ledger.csv`), delete its `#` line, then check each claim. After every text change re-run it with `--all --against session-<N>/ledger.csv --dropped session-<N>/claims-candidates.csv` and the same three files | `moi-devrel/claim-check/GUIDE.md` | The `--against` run exits 0 and `python3 "$SKILLS/moi-devrel/claim-check/scripts/ledger-status.py" session-<N>/ledger.csv` exits 0 |
| 6 | Event page | Draft `LUMA.md`. The operator makes the page by hand, on the Monday of the session week, with the Meet link from Vardan. `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "<YYYY-MM-DD HH:MM>" Asia/Kolkata` | `references/event-page.md` | The live page's title numeral, date and time match the plan, and its URL is in `LUMA.md` |
| 7 | Pre-event posts | GATE: consult the marketing team first; then running `"$SKILLS/moi-webinar/scripts/buffer.mjs"` in any form, scheduling or saving a Buffer draft, and every post. Draft `SOCIAL.md` (four slots: Monday of the session week, T-2 days, T-1 day, T-1 hour), then one file per post. `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" session-<N>/SOCIAL.md session-<N>/social/*.txt` (zsh stops with "no matches found" until `social/` holds a `.txt` file: leave the glob out until then) | `references/pre-event-social.md`; Buffer: `moi-blog/references/buffer.md` | The operator has read each post once. Nothing is scheduled without a yes |
| 8 | Rehearsal | `bash "$SKILLS/moi-webinar/scripts/session-preflight.sh" session-<N>` (read-only, never opens `.env`). Read the script aloud once and time it. One full demo run is a wallet step (step 2) and spends devnet funds: GATE, a yes first | `references/game-day.md` | No FAIL. The operator's pasted run exits 0 on the current node |
| 9 | Game day | The T-1 day, T-60, T-30 and T-10 checklists and the fallbacks. GATE: each real run of the demo needs a yes, and the operator runs it (wallet step) | `references/game-day.md` | The session ran. Questions and their owners are written down |
| 10 | Recording | A rehearsal video for the fallback. GATE: a recorded run spends devnet funds and is a wallet step, and handing a file to the editor is a share. Who records the live session | `references/recording.md` | The operator knows where each file is |
| 11 | Write-up | Hand the folder to `moi-blog`, which writes, ships and announces the post. GATE: every push, merge and announcement there | `references/after-the-session.md` | Published, or the blocker is named. Target: 48 hours |
| 12 | Webinar bounty | Draft the bounty brief for the host to approve: the task, one to six fields (interaction hash, link, number or text), points per field, a total of at most 10,000, a deadline, the brief link. The host creates it closed on the Points admin page, tests it once, opens it at the session end and grades it by hand, checking each hash on the explorer. Claude never signs in to the admin page or presses Create, Open, Award, Reject or Close. GATE: the host's admin access (`ADMIN_EMAILS`), the announcement, and every Award, which is permanent | `references/after-the-session.md`, "The webinar bounty"; the clicks are in `moi-web-products-ops/references/points-tasks.md` | The brief is approved, the bounty was created closed and tested once, and nothing is awarded before each hash is checked by hand |
| 13 | Hand-back | The format at the end of this file | none | The operator has read it |

## Which file to read
| Doing | Read |
|---|---|
| Choosing a topic, the series plan, what was covered | `references/topic-and-storyline.md` |
| What is due when, which documents exist | `references/lifecycle.md` |
| The code standard, what "verified" means, hashes | `references/demo-standard.md` |
| The run sheet, the game day checklist, how the plan documents differ | `references/run-of-show.md` |
| The registration page | `references/event-page.md` |
| Posts before the event | `references/pre-event-social.md` |
| The day itself and what to do when it breaks | `references/game-day.md` |
| Rehearsal video, voiceover, the live recording | `references/recording.md` |
| The write-up and the webinar bounty | `references/after-the-session.md` |
| What each session was, where its files are, what breaks today | `references/session-history.md` |
| The intro session with the Launchpad demo | `references/intro-session.md` |
| Anything that went wrong before | `references/traps.md` |
| A finished run to learn from | `examples/session-8/README.md` |
| Starting the documents | `templates/` |
| Scaffolding a folder, or checking before a rehearsal | `scripts/new-session.sh`, `scripts/session-preflight.sh` (each header says what it does and what it never does) |
| Testing a change to this skill | `evals/evals.md` |

The branches, with paths relative to this folder:
| Asked to | Read |
|---|---|
| Make, check, change or export any deck; presenter notes; slide numbers; rules for a script read aloud | `deck/GUIDE.md` |
| Run the monthly community call, The Campfire Chat, starting from its agenda (a dated checklist, then one item at a time): line-up, numbers ledger, release slides, host question, Luma and post drafts, the day, the YouTube description | `community-call/GUIDE.md` |

## What a session touches
| Part of a session | Where it lives |
|---|---|
| The deck and the spoken script | `deck/GUIDE.md` (a branch of this skill) |
| The write-up post, its announcement and the newsletter | `moi-blog`; what the session folder hands over is `references/after-the-session.md` |
| The webinar bounty (the Google proof form is superseded, 13 October 2026) | `references/after-the-session.md`, "The webinar bounty" |
| The Points site side of a session's bounty | `moi-web-products-ops/references/points-tasks.md` ("Run: a webinar bounty"; a code dev challenge is the legacy way), `points-settings-and-database.md` for `ADMIN_EMAILS` and the `MOI_RPC_URL` variable, `points-health.md` to check it, all in the same folder |
| The programmes that feed and follow sessions (Forge, awesome-moi, other bounties; MOI Sprint scratched 13 October 2026) | `moi-education-programs`; `moi-education-programs/references/bounties.md` covers the four kinds of bounty and verifying submissions |
| Claims in the script, event page and posts | `moi-devrel/claim-check` (step 5) |
| The brand: slides, event page art, share images | `moi-devrel/design` |

## Facts that fail silently
The full list is `references/traps.md`. The deck traps are `deck/references/traps.md`.

| Rule | The incident |
|---|---|
| A refusal counts only for the right reason. Require its error text and check the balance first | 31 Aug 2026: beat 3 "passed" because the agent had run out of KMOI |
| Read the live event page title the night before | By 2 Sep 2026 the page said VII for session 8, and the checklist of 3 Sep still listed the fix |
| Refer to slides by title in the run sheet | Read on 2026-10-02: the run sheet says 18 slides and the deck has 19 |
| After a correction, search every document and the deck notes | 7 Aug 2026: "only the owner can move funds" was found false and survived in six files |
| A reset wipes accounts, assets, logics and registrations. Rehearse any old session before reuse | The wipe announced for 11 September 2026 (`moi-devrel/references/devnet.md`, reset history). No run of any session is on record since |
| Announce an unfinished bounty as coming | 3 Sep 2026: the game day checklist said the bounty and the docs page were not live |
| Search for placeholders before publishing | Session 9's draft has `<<< EVIDENCE >>>` markers and a link to an undelivered post <!-- slop-lint:ignore --> |
| The public branch shows its tracked files, and its 95 commits carry an AI trailer | Read on 2026-10-02. Do not open a pull request from it unasked |
| `main`'s `.gitignore` does not list session 8's internal files. Only the branch's does | Read on 2026-10-02. Landing the folder without the scaffold's own `.gitignore` would publish the run sheet, event page copy and social files |
| Do not copy session 8 lines that refer to the dropped design | See `examples/session-8/README.md` |
| Never paste or read a recovery phrase, in chat or on a recorded call | 31 Aug 2026 and 2026-09-24 |

## Gates
Nothing below happens without the operator's explicit yes in this conversation. Building, linting and reading are free. The deck and community-call guides add their own gates to these.
- Push, pull request, merge, or any change to the public repo. A push to `moi-foundation/MOI-Webinars` publishes.
- Posting to Discord, Telegram, X or LinkedIn. Use Buffer only after consulting the marketing team (`DEV-WEBINARS.md`). Running `"$SKILLS/moi-webinar/scripts/buffer.mjs"` in any form, a dry run included (it sends the key to Buffer), is a GATE, and so is scheduling or saving a draft in Buffer. Sending a recap to attendees. Claude drafts, the operator sends.
- The bounty: Claude drafts the brief only. Signing in to the Points admin page, creating, opening or closing a bounty, and pressing Award or Reject are the host's own actions, never Claude's. Award is permanent, so each one needs the host's yes for that submission. Opening the bounty and announcing its brief link each need a yes.
- Member data: the Points admin page shows names, emails and wallets. Copy none of it into notes, the repo, a chat or a post. Record the bounty id, counts, points and hashes only.
- Creating or editing the event page or the meeting invite. Uploading or sharing a recording, a PDF or any file in cloud storage. Downloading a file: name it, its source and its size first.
- Spending devnet funds, deploying a logic or creating an asset: the rehearsal run, the T-60 and T-30 runs, a top-up script, recording a demo run. Show the paying account and the cost.
- Setting a repository secret or variable. Switching the git or `gh` identity.
- Running any script that loads the recovery phrase from `.env` (a wallet step): the operator runs it, Claude never does.
- Sub-agents, bulk model runs and paid APIs: only when the operator names them, with the count and model stated first.
- Deleting a recording or a notes document. That is the operator's own action, after asking the file's owner.
- Telling the lead, the reviewer or an attendee that something is confirmed.

## Keys and access
Names only. Where each lives: `moi-devrel/references/keys-and-access.md`.
- The session's `.env`: the recovery phrase variable (`USER_MNEMONIC` or `MOI_MNEMONIC`), derivation paths, `LOGIC_ID`, and a model key where a demo calls a model (`GROQ_API_KEY`, `OPENAI_API_KEY`). The operator edits it. Claude never opens it.
- `BUFFER_API_KEY` for `scripts/buffer.mjs`, which ships in this skill (a copy also sits in the webinars repo). The key goes in a gitignored `.env` next to the script's parent folder (`$SKILLS/moi-webinar/.env`) or in the environment. Chandra, who owns the Buffer organisation, creates it. It is not the website pipeline's `BUFFER_ACCESS_TOKEN`.
- The Luma, Google Meet and YouTube logins are held by Vardan, who also provides the Meet link (`DEV-WEBINARS.md`). The recordings of past sessions sit under the shared account `info@moi.technology`.
- The Google Forms of earlier sessions sit on the previous DevRel's company Drive. Moving them to a shared Drive is an open item in `project-handover-docs/DEV-WEBINARS.md`. New sessions use the webinar bounty, not a form.
- The Points admin page, for a webinar bounty: the host's Google email must be in the `ADMIN_EMAILS` Actions variable of `sarvalabs/moi-project`. DevOps (Upendhar) sets it.
- Points: security findings are open on this product. Read `project-handover-docs/POINTS-PROGRAM.md`, Open items, before touching its admin.

## Hand-back
```
Produced: <files with exact paths, the event page URL, posts drafted>
Remaining: <numbered, each with who owns it>
Not verified or simulated: <say so, or "none">
Ready: yes or no, because <one reason>
Next steps: <one to three>
```
Ready is no while `session-preflight.sh` has a FAIL, the demo has not run on the current node, a claim row is unverified, a placeholder remains, or the live event page differs from the plan.
