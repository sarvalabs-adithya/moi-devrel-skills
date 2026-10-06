# Event checklist: a campus mini-hackathon or a cohort kickoff

Paths below that start with `templates/` or `references/` are inside the moi-education-programs skill. Make the private folder first (`mkdir -p edu-work && printf '*\n' > edu-work/.gitignore`), copy this file with `cp -n "$SKILLS/moi-education-programs/templates/event-checklist.md" edu-work/event-checklist.md`, fill the `{{...}}` fields and tick lines as they are done. The order follows the one run on record (Presidency College, kickoff 2026-03-17, due 2026-03-31) and adds the steps that run did not document, marked "proposed". GATE means the operator's explicit yes comes first. Nothing here is sent by Claude. The `.gitignore` in `edu-work/` keeps the filled copy out of git. Never commit it with names or contact details filled in.

Event: {{name}}   Campus: {{campus}}   Owner who approved it: {{name, date}}
Kickoff: {{YYYY-MM-DD HH:MM}} UTC, {{HH:MM}} IST (run `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "{{YYYY-MM-DD HH:MM}}" {{UTC or Asia/Kolkata}}`; the script reads the time in the zone you give and prints the other)
Deadline: {{YYYY-MM-DD HH:MM}} UTC, {{HH:MM}} IST   Grace rule for late rows: {{decided with Rahul, or "none"}}

## Before announcing
| # | Item | Owner | GATE | Done when |
|---|---|---|---|---|
| 1 | The programme is alive and Rahul has said yes to this event | Rahul | | His yes is in the conversation |
| 2 | Campus contact, faculty contact, any college agreement | Sai Kiran for logistics; ASK: Rahul for the agreement | The operator only | Terms are known. Claude drafts nothing legal |
| 3 | Student count, mentors (names and Discord roles), judges (two, named), what winners receive | Rahul | | Every prize and every promise has Rahul's written yes, or the text says "none announced" |
| 4 | One support channel and one invite. Office hours stated exactly as they will be kept (daily, or on request) | Rahul | | Every document says the same thing |
| 5 | Devnet preflight: `net.Version`, `npm view js-moi-sdk dist-tags`, newest Coco at cocolang.dev/docs/releases | Operator | | Versions written down; differences with the materials listed |
| 6 | The demo runs end to end on today's devnet, from a wallet the presenter made in the MOI Wallet extension | Presenter | Spends devnet funds: name the account | Exit 0 and the hashes are written down |
| 7 | Materials rebuilt, not reused: deck, playbook, README (`templates/hackathon-pack.md` in moi-education-programs) | Operator | | None of these remain: "testnet", "COCO tokens", "IOMe", `?network=babylon`, a faucet amount, a placeholder, an unapproved promise, a metaphor, "MAS0-style token" |
| 8 | Link check: `python3 "$SKILLS/moi-education-programs/scripts/link-check.py" <README.md>` | Operator | | Exit 0. Every CHECK opened by hand |
| 9 | Wording: `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" <each public file>`. Third-party figures through `moi-devrel/claim-check` | Operator | | 0 errors and a ledger with no unverified row |
| 10 | Submission form for this campus only, named for it. Fields: team name, repository link, member names, video link, one contact. Close date set | Operator | Creating a form | The form's name matches the campus. The owner of the Google account is known |
| 11 | Recovery-phrase paragraph on the first page of every student document (`references/students.md` in moi-education-programs) | Operator | | Present in README, playbook and the welcome message |
| 12 | Invite and README drafts (`templates/onboarding-messages.md`, messages 1 and 2) | Operator | Sending | The operator sent them. Nothing mentions a job, internship or prize without a yes |

## The week before (proposed)
| # | Item | Owner | GATE | Done when |
|---|---|---|---|---|
| 13 | Reminder (message 3). Mentor briefing (message 9) | Operator | Sending | Mentors know the channel, the hours and the recovery-phrase rule |
| 14 | A fallback for the live demo: a recorded run, and the room's network checked | Presenter | A recorded run spends devnet funds | The fallback plays |
| 15 | Decide who records and where it is stored. A recording must never show a phrase | Operator | Sharing a file | Known |

## Kickoff day
| # | Item | Done when |
|---|---|---|
| 16 | One hour before: Voyage opens, the presenter's wallet is registered and the faucet has funded it, `net.Version` answers | All three confirmed |
| 17 | Hide the `.env`, close the wallet's phrase screen, turn off notifications on the shared screen | Checked on the shared window |
| 18 | Run the agenda (`templates/hackathon-pack.md`, part 2). Stop at the recovery-phrase rule and say it aloud | The rule was said |
| 19 | Straight after: post the channel link and the brief (message 4) | The operator posted |
| 20 | Write down every question asked and who will answer it | A list exists |

## Build phase (14 days at Presidency)
| # | Item | Done when |
|---|---|---|
| 21 | Office hours kept as announced. A phrase pasted in the channel gets a reply at once (message 11) | Each pasted phrase answered |
| 22 | Watch for a devnet reset (`moi-devrel/references/devnet.md`, "Signs of a reset"). If one happens, tell students what was wiped and to redeploy | Students told the same day |
| 23 | Mid-way check-in (message 5) | Sent |

## Deadline and after
| # | Item | GATE | Done when |
|---|---|---|---|
| 24 | Reminder 24 hours before (message 6) | Sending | Sent |
| 25 | Close the form at the deadline plus the agreed grace. Export the responses into `edu-work/` | Editing the form; downloading a file | Counts known. No row copied into a repo, note or chat |
| 26 | Dedupe by repository link. Open each repo: Coco logic files, README, video | | One line per team in a ledger inside `edu-work/` |
| 27 | Score with the published rubric; two named judges | | Scores recorded with who and when |
| 28 | Verify any on-chain claim by reading the chain | | Receipts checked |
| 29 | Tell every team its result (message 8). Promise nothing without a yes | Sending | Sent |
| 30 | Write the outcome: headcount, submissions, winners, what broke, what to change | | The missing record now exists |
| 31 | Keep deck, playbook and README sources beside their PDFs; update the sheets described in `references/tracking.md` with counts and dates only | Sharing a file | Sources saved |
