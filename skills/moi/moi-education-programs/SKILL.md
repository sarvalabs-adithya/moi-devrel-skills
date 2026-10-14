---
name: moi-education-programs
description: "Run or maintain MOI's developer education programmes and keep the library's record of them: MOI Forge Hacks (a campus mini-hackathon), the Forge university cohort (a 12-week onboarding), the awesome-moi resource list, and the bounties and weekly tracking around them. MOI Sprint (self-paced challenges) was scratched on 13 October 2026; kept for the record only. Works alongside moi-webinar: what feeds a Builders session and what a session hands back (recordings, bounties). Use for \"Forge\", \"Forge Hacks\", \"campus hackathon\", \"university cohort\", \"student onboarding\", \"what students need before day one\", \"awesome-moi\", \"resource list\", \"bounty submissions\", \"content bounty\", \"MOI Programs sheet\" or \"programme metrics\". Says what is alive, what is broken, what needs a yes and who to ask. Running a Builders session or the community call is moi-webinar, the Points app and its webinar bounties is moi-web-products-ops, claim checks are moi-devrel/claim-check."
---

# MOI education programmes

## What this covers
Three programmes: MOI Forge Hacks (a campus hackathon), the Forge cohort (12 weeks) and the awesome-moi list. Also the bounties and the tracking sheets that serve them. MOI Sprint (challenge scaffolds, a guide site and a chapter repo) was scratched from the handover on 13 October 2026: `references/sprint.md` is kept for the record and nobody is routed to it. Claude reads, checks and drafts. The operator sends, posts, pays, merges and talks to colleges and students.
Not covered: running a Builders session, its proof form and the monthly call (`moi-webinar` and `moi-webinar/community-call`; the section "Works with the webinar skill" below says where the two meet); devnet facts (`moi-devrel/references/devnet.md`) and what breaks after a reset (`moi-devnet-reset`); teaching the operator a MOI concept so they can present it to students (`moi-devrel/explain`; it has no student-audience path, so write the student text plainly from `moi-devrel/references/glossary.md` and run `moi-devrel/claim-check` on it); the Points app and its challenge tasks (`moi-web-products-ops`); decks (`moi-webinar/deck`), posts (`moi-blog`), docs pages (`moi-docs`), claims (`moi-devrel/claim-check`), commits and pull requests (`moi-devrel/ship`), messages to teammates (`moi-devrel/templates/messages.md`, checked with `moi-devrel/scripts/check-message.py`), visuals (`moi-devrel/design`).

## Before you start
`$SKILLS`, "the operator", "the previous operator" and `ASK: <name>` are defined in `moi-devrel/SKILL.md`. Terms such as logic, Coco, MAS0, KMOI, Voyage, faucet and devnet are in `moi-devrel/references/glossary.md`. Quote `$SKILLS` in every command. Run a command from the working copy of the repo it concerns: the list is `moi-foundation/awesome-moi`; the Forge Hacks material is `sarvalabs-adithya/moi-forge-hacks-demo` (the previous DevRel's account). Treat the Forge Hacks repo as read-only. A clone is a download, so say its name, source and size first (GATE).
- [ ] A private working folder for filled checklists, scoring sheets and ledgers, which name students, creators and wallets: `mkdir -p edu-work && printf '*\n' > edu-work/.gitignore`. The `*` hides the folder from `git add`, so a stray commit cannot publish it, and `moi-foundation/awesome-moi` and `moi-foundation/MOI-Webinars` are public. The rule does not hide a file git already tracks.
- [ ] The programme and what should exist at the end, in one line. The operator provides it. Ask: "Which programme, and what exists at the end?"
- [ ] Whether the programme is alive and who owns it now. ASK: Rahul. Draft: "Is <programme> still running, and who owns it?" Campus logistics: Sai Kiran, through the operator.
- [ ] For an event: campus, date, student count, mentors, judges, what winners get, the support channel. ASK: Rahul. Ask the operator for each in one numbered list.
- [ ] Work identity check before any commit: `bash "$SKILLS/moi-devrel/scripts/preflight.sh"` (see `moi-devrel/SKILL.md`).
- [ ] A funded devnet wallet that the operator made in the MOI Wallet extension. Claude never handles a recovery phrase.
- [ ] The files that exist only on the previous operator's machine (`references/traps.md`, row 15) are not recorded (the previous DevRel's notes); ASK: Rahul.
- [ ] Access to the Drive sheets "MOI Programs" and "MOI Socials". ASK: Rahul.

State of each programme (as of 2026-10-03; none is confirmed active; Sprint scratched 13 October 2026):
| Programme | Last dated trace | Read |
|---|---|---|
| MOI Sprint | Scratched 13 October 2026. Scaffold and site repos last pushed 2026-02-13 | `references/sprint.md` (for the record) |
| Forge Hacks | One run: kickoff 2026-03-17, due 2026-03-31 | `references/forge-hacks.md` |
| Forge cohort | PCCOE review call 2026-05-07 | `references/forge-cohort.md` |
| awesome-moi | `main` pushed 2026-01-16 | `references/awesome-moi.md` |
| Bounties | Content campaign sheet 2026-09-09 | `references/bounties.md` |
| Tracking | Socials metrics filled to the week of 2026-09-28 | `references/tracking.md` |

## The run
GATE means the operator's explicit yes comes first (see Gates).
| # | Step | What to do, where or the command | Done when |
|---|---|---|---|
| 1 | State | Read the programme's reference, its "Not yet known" list and `references/traps.md`. Give the operator the ASK lines as a numbered list | The operator knows whether the programme is alive and has the open questions |
| 2 | Devnet and versions (read-only) | `curl -s -X POST https://dev.voyage-rpc.moi.technology/devnet/ -H 'content-type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"net.Version","params":[]}'`, then `npm view js-moi-sdk dist-tags` and the newest Coco at cocolang.dev/docs/releases. Coco 0.9.3 (targets PISA 0.8.2) is the newest release as of 13 October 2026. Compare with the pins in the material: from the root of the clone of that repo, `grep -rn "js-moi-sdk" --include=package.json . | grep -v node_modules` | The node version, SDK and Coco versions are written down, with every difference |
| 3 | Links | `python3 "$SKILLS/moi-education-programs/scripts/link-check.py" <file.md> [more.md]` on each file you will publish or send. Relative links resolve against the file. Run it from the repo root and add `--root .` for links that start with a slash. It only reads and asks public hosts | Exit 0. Each REDIRECT replaced by its new address. Each CHECK opened by hand |
| 4 | Student needs | `references/students.md`: the prerequisites, the day-one check, the recovery-phrase paragraph | Every student document has the paragraph and no stale name or amount |
| 5 | The work | Forge Hacks, cohort, awesome-moi, bounty, tracking: follow that reference. Work in `edu-work/` or a branch of a working copy. A commit uses the work identity (`moi-devrel/ship`); a push, pull request or merge is a GATE | A draft exists at a path you state |
| 6 | Wording and claims | `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" <file>`. Any figure or promise about MOI goes through `moi-devrel/claim-check`. Wording rules: `moi-devrel/references/terminology.md` | Lint shows 0 errors. Rahul has approved any promise to students |
| 7 | Messages | `cp -n "$SKILLS/moi-education-programs/templates/onboarding-messages.md" edu-work/onboarding-messages.md`, then fill one draft. Claude drafts, the operator sends. GATE | The operator has read the text, channel and time once |
| 8 | An event | `cp -n "$SKILLS/moi-education-programs/templates/event-checklist.md" edu-work/event-checklist.md`, and the same for `hackathon-pack.md`. A form, an event page, a channel post and any devnet spend are each a GATE | Every checklist line is done or an ASK |
| 9 | Submissions and rewards | Verify on chain or by link, one line per row in a ledger inside `edu-work/` (`references/bounties.md`). The operator pays after Rahul's yes. GATE | A verdict per row, none paid by Claude |
| 10 | Track and hand back | Numbers go in with a source and an "as of" date (`references/tracking.md`). Hand back in the format at the end | The operator has read it |

## Which file to read
| Doing | Read |
|---|---|
| MOI Sprint (scratched 13 October 2026): the record of the challenge track, kept for the record only | `references/sprint.md` |
| Running a campus mini-hackathon, before, during, after | `references/forge-hacks.md`, `templates/hackathon-pack.md` |
| The cohort lifecycle, the onboarding guide | `references/forge-cohort.md`, `templates/onboarding-messages.md` |
| Adding to or fixing the resource list | `references/awesome-moi.md`, `templates/list-entry-format.md` |
| A bounty, its grading, verifying submissions | `references/bounties.md`, `moi-web-products-ops/references/points-tasks.md` |
| The sheets, the goals document (KRAs), weekly metrics, content calendar | `references/tracking.md` |
| What a student needs before day one | `references/students.md` |
| Anything that failed silently before | `references/traps.md` |
| Event run list | `templates/event-checklist.md` |
| Testing a change to this skill | `evals/evals.md` |

## Works with the webinar skill
`moi-webinar` runs a Builders session. This skill is the library's record of the programmes around it, so open both when a session touches a programme. As of 2026-10-03 no document says a programme schedules a session: each row is what the record shows, and the rest is an ASK: Rahul. Running the session itself (deck, run of show, game day, event page, write-up) is `moi-webinar/SKILL.md`.
| Direction | What the record shows | Read here | Read in `moi-webinar` |
|---|---|---|---|
| Feeds a session: the Forge cohort | Its row "MOI Forge, Advance" in the "MOI Programs" sheet lists a demo day and a Builders newsletter every month as KPIs, and the cohort guide sends students on to the Sprint chapters (inferred; Sprint is now scratched). Whether cohort students are invited to a session or propose its topic is not recorded | `references/forge-cohort.md`, `references/tracking.md` | `moi-webinar/references/topic-and-storyline.md`, `moi-webinar/references/lifecycle.md` |
| Feeds a session: Sprint (scratched 13 October 2026) | Only an idea: the Sprint plan's principle, that a reward depends on verified on-chain activity and not on completion, is the one session 8's chain-checked challenge followed. Send no student to Sprint | `references/sprint.md`, `references/bounties.md` (kinds 1, 3, 4) | `moi-webinar/references/demo-standard.md` |
| Gives back: recordings | A session's live recording and its rehearsal video. Where either is published is not recorded for any session, so neither is student material until the operator and Rahul say where it lives | `references/forge-cohort.md` (the Forge recording folders) | `moi-webinar/references/recording.md`, section 3 |
| Gives back: proof of completion | Sessions 2 to 7 used one Google Form each. Since 13 October 2026 a webinar bounty is a hand-graded form in the Points app (interaction hash, link, number or text fields, points per field). Check every answer before any reward, and copy no name, email or wallet into a repo, note or chat | `references/bounties.md`, "1. Builders session bounty", "How to verify a submission" | `moi-webinar/references/after-the-session.md` |
| Gives back: bounties | The task per session and its reward. Claude never pays. The host creates the bounty in `/admin`, Webinar bounties (PR #22, live 13 October 2026); no bounty has been created on production yet. The chain-checked dev challenge of session 8 is deployed but off | `references/bounties.md`, "The four kinds" | `moi-webinar/references/after-the-session.md`, the bounty section; the Points runbook: `moi-web-products-ops/references/points-tasks.md` |

## Facts that fail silently
The full list is `references/traps.md`.
| Rule | The incident |
|---|---|
| Ask before you build: a repo existing does not make a programme alive | The previous operator's dependencies list of 2026-10-01 (not in the handover repo; `project-handover-docs/LIST-OF-DEPENDENCIES.md` is the 4 October snapshot and has no section for these programmes) said of Sprint "Decide if it is alive" (it was then scratched, 13 October 2026) and of the Forge Hacks demo repo "archive it, or move it to the org if the playbook is reused". No source says any programme is running now |
| Rerun the whole student path on today's devnet before anyone starts | The Forge demo pins `js-moi-sdk` `^0.7.0-rc10`; the newest on npm is `0.9.0-rc2`. Coco 0.9.3 (targets PISA 0.8.2) is the newest as of 13 October 2026; Coco 0.9.2 (tested 2026-09-28) rejected `enlist` endpoints, which the Forge demo contract uses. Not retested on 0.9.3 |
| Run the clone command on the page you are about to send | The live Sprint challenge pages said to clone a repo that answered 404 (2026-10-03). Check every clone address in student material |
| Do not quote a faucet amount, "IOMe", "testnet" or `?network=babylon` | Amounts differ across documents (20K, 100K). Voyage moved its login to MOI Wallet in late August 2026 (the announcement post is dated 2026-08-27). Voyage answers 200 whatever the query string says (read 2026-10-03), so the link check cannot catch a stale network name |
| No internship, job, prize or payment promise without Rahul's written yes | The March 2026 deck promised an internship fast track. No approval is recorded |
| Copy no student, creator or wallet data into a repo, note or chat | Forms hold names, emails, wallets and a phone number |
| A recovery phrase never goes on a call, a form or a page | It reached Gemini notes on 2026-09-24. A student warning was removed from a README on 2026-03-17 |
| Count distinct pieces, not rows | The content sheet says 217 submissions from 103 creators; one piece can sit on three platforms |
| A work-in-progress copy exists only on one machine | The Forge guide and the deck sources are not on GitHub |

MOI Sprint (scratched 13 October 2026; the guide site and the tSwapper scaffolds): a security finding was open on this product as of 2026-10-02. The previous DevRel's note on it is not recorded; ASK: Rahul before touching its admin.

## Gates
Nothing below happens without the operator's explicit yes in this conversation.
- Push, pull request, merge or any change to `moi-foundation/awesome-moi` or another public repo. A merge there is publication.
- Posting, scheduling or sending anything: Discord, Telegram, WhatsApp, X, LinkedIn, email, a college or faculty contact. Claude drafts, the operator sends.
- Creating or editing a Google Form, a sheet or an event page. Uploading, moving or sharing a file in Drive, including a PDF or any file with student data. Downloading a file or cloning a student repo: name, source and size first.
- Spending devnet funds, deploying a logic or creating an asset (a rehearsal, a live demo). Name the paying account.
- Any change to the Sprint site, its Vercel project, its domain or its environment. Any admin write. Any deploy, manual workflow run, database migration or production write. Anything on a VM (none of it belongs to this skill: ASK: Upendhar). <!-- slop-lint: ignore -->
- Paying a bounty. Claude never pays. Telling anyone a submission is accepted or a prize is won.
- Any promise about internships, jobs, prizes or grants. Any agreement with a college.
- Setting a repository secret or variable. Switching the git or `gh` identity. Sub-agents.
- Deleting a recording or a notes document: the operator's own action, after asking the file's owner.

## Keys and access
Names only. Where each lives: `moi-devrel/references/keys-and-access.md`. The rows below are not in that file yet, so each is an ASK.
- The Sprint site (it ran on Vercel as of 2026-10-03; the project was deleted on 2026-10-14): the Vercel project, its environment variables and the wallet that deployed its on-chain logic. The names are not recorded (the previous DevRel's notes); ASK: Rahul. <!-- slop-lint: ignore -->
- The scaffold's `.env.example` names `RPC_URL`, `POOL_OWNER_MNEMONIC` and `POOL_OWNER_ADDRESS`. The Forge demo reads `ADMIN_MNEMONIC`, `MOI_RPC_URL`, `TOKEN_NAME` and `TOKEN_SYMBOL`. Each is a student's or presenter's own.
- The Discord server admin and mentor roles, the Telegram announcement channel, the WhatsApp group admin. ASK: Rahul, Sai Kiran.
- The owner of the content-bounty sheet, and the Google account behind the forms and Meet. ASK: Rahul.
- A recovery phrase goes in a gitignored `.env` that its owner edits. Claude never opens an `.env` and never handles a phrase, including a throwaway one.

## Hand-back
```
Produced: <what, with exact path or URL>
Remaining: <numbered, each with who owns it>
Not verified or simulated: <say so, or "none">
Open ASK lines: <numbered, each with the person>
Ready: yes or no, because <one reason>
Next steps: <one to three>
```
Ready is no while a link check shows DEAD, a figure or promise has no source or approval, or a draft has not been run on today's devnet. A status lists work that was done. A to-do is labelled as one.
