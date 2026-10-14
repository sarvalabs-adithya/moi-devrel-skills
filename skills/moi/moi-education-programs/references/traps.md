# Traps: what fails silently in the education programmes

Facts are as of 2026-10-03. Each row is a thing that gives a wrong result with no error, with the evidence and the rule. Dates are when it was found or read. Detail for each programme is in its own reference. Back to `../SKILL.md`.

## A. Across all programmes
| # | Trap | Evidence | Rule |
|---|---|---|---|
| 1 | Treating a programme as alive because its repo exists | Last dated traces: Sprint repos 2026-02-13, awesome-moi 2026-01-16, Forge Hacks 2026-03-20, cohort review call 2026-05-07, content bounty sheet 2026-09-09. The previous operator's own list (2026-10-01) says "decide if it is alive" | Ask Rahul before building, announcing or recruiting for any of them |
| 2 | "MOI Sprint" and "MOI Forge" used for one thing | The folder `awesome-moi/resources/moi-sprint/` held the Sprint README on GitHub and holds the Forge guide in a local rewrite | Sprint is the challenge track. Forge is the campus programme. One name, one meaning |
| 3 | Student material that ran once and was never rerun | Scaffolds pin `js-moi-sdk` `^0.7.0-rc6` (npm 2026-01-28); the newest on npm is `0.9.0-rc2` (2026-09-09). The previous operator wrote that both Sprint repos "will not run against today's devnet" (2026-10-01) | Run the whole student path on today's devnet before telling a student to start |
| 4 | The compiler moved | Coco 0.9.3 (targets PISA 0.8.2) is the newest as of 2026-10-13; 0.9.2 (2026-09-28) rejected `enlist` endpoints when tested, and the Forge demo token logic and the Sprint progress logic use one (read in source, not compiled, not retested on 0.9.3) | Compile with the version students will install. ASK: Gokul which fits devnet |
| 5 | Ids die at a reset | Full wipes on 2026-08-15 and 2026-09-11. A deployed logic, an asset id or the progress logic's id is gone | Keep deploy scripts. Tell students before day one (`students.md`) |
| 6 | An amount or a name copied from an old document | Faucet: 20K (Forge guide, awesome-moi), around 100k (Chapter 1), 100K (calls 2026-01-30 and 2026-09-24). "IOMe" predates MOI Wallet (late August 2026). "testnet" and "COCO tokens" in the March deck. `?network=babylon` in playground links | Never quote a faucet amount. Say devnet, KMOI, MOI Wallet. Open the links by hand |
| 7 | The retired model in teaching text | Chapter 1: "Global State Machines", "Interaction State Machine", a "temporary, localized consensus lane". Founder's wording of 2026-09-14: participant-centric, MDAG | Re-read every explainer against `moi-devrel/references/terminology.md`. `moi-devrel/explain` for rewrites |
| 8 | Metaphors in student decks | "Google Docs, but for money" and "the contract is the bank" (March 2026) predate the September rule of direct wording | Plain terms. No metaphor the operator has not approved |
| 9 | Promises to students | The March kickoff deck and call promised that winners enter Forge and top participants are fast-tracked for internships and full-time roles. No approval is recorded | No internship, job, prize, grant or payment in any message without Rahul's written yes |
| 10 | Student and creator data in the wrong place | Forms hold names, emails, wallets, GitHub links, Telegram and Discord ids, one phone number. The kickoff notes list dozens of invitees by personal email | Read headers and counts only. Copy no row into a repo, note or chat. Keep ledgers out of git |
| 11 | A photo of identifiable students | The CC14 example's event photos had no permission on record and were removed from the library (`moi-webinar/community-call`). No programme photo has a permission record either | Show one only with permission to show it |
| 12 | A recovery phrase on a recorded call | Seed words reached Gemini notes on 2026-09-24. A student document lost its warning on 2026-03-17 | Never read, show or confirm a phrase on a call. Warning paragraph in every student document (`students.md`) |
| 13 | A "200" taken as "alive" | The MOI website and the js-moi-sdk docs host answer 200 for a path that does not exist, and Voyage answers 200 whatever the query string says (read 2026-10-03). A made-up Discord invite code also ends in 200. A closed Google Form is a link the script skips | A link check is a floor. Open what matters by hand |
| 14 | A JSON-RPC address read as a page | `dev.voyage-rpc.moi.technology/devnet/` answers a GET with 404 and answers `net.Version` correctly | Test an endpoint with the JSON-RPC read, not with a GET |
| 15 | Work that exists on one machine | The Forge guide (an uncommitted rewrite in the awesome-moi clone), the Sprint site redesign (18 modified files and an untracked folder), 4 modified files and an ignored handover doc in the scaffold clone, the Sprint prototype, the deck sources (git history only) | Not recorded (the previous DevRel's notes); ASK: Rahul before relying on any of them |
| 16 | Repos in an individual account | `tSwapper`, `moisprint` and `moi-forge-hacks-demo` are in `sarvalabs-adithya`, not an org. Chapter 1 tells students to clone from there | Decide with Rahul whether they move to `moi-foundation` before any new student is sent to them |
| 17 | A push to a `moi-foundation` repo publishes | `awesome-moi` and `moi-sprint` have no deploy: a merge is publication. `MOI-Webinars` is public | GATE every push, pull request and merge |
| 18 | An AI footer in a pull request | House rule 4 forbids it. The x402 project asks for AI-assistance disclosure in its PRs (`moi-devrel/references/consent-and-identity.md`) | None in any commit or PR here. ASK: Rahul how to word a disclosure if a project requires it |

## B. MOI Sprint (scratched 13 October 2026; kept for the record)
| # | Trap | Evidence | Rule |
|---|---|---|---|
| 19 | Students sent to a programme nobody has confirmed is alive | `moisprint.com` does not resolve and the challenge pages' clone address answers 404 (2026-10-03). The marker for this product is in `sprint.md`, "Before you touch anything" | Do not send students until Rahul says the programme is live. ASK: Rahul |
| 20 | The live challenge pages tell students to clone `aspect-build/moisprint` | That address answers 404 (2026-10-03) | Do not send the page to anyone until fixed |
| 21 | Guides cited at `moisprint.com` | The host does not resolve. The site is at moisprint.vercel.app | Fix the domain or the links together |
| 22 | The finished solution is public | `origin/solution` of `tSwapper` has zero stub markers, and so does commit `79de8e4` in the history of `main` (both read 2026-10-03). A local branch called `solution` holds the stubs in its files and the answers in its history | Never link the solution from student material. Branch names mislead; read the content. ASK: Rahul whether the answers may stay public |
| 23 | Chapter 1 and the scaffold disagree | Chapter 1 opens `src/lib/logic.js` at the root; `main` keeps it under `Swap/` and `SoulBound/` | Fix both together |
| 24 | A test command that switches TLS checks off | `NODE_TLS_REJECT_UNAUTHORIZED=0` in both READMEs, no reason recorded | Do not copy it. Why is not recorded (the previous DevRel's notes); ASK: Rahul |
| 25 | The handover doc disagrees with the code | `PROGRESS_PLUMBING.md` is ignored by git and describes the flow differently from the code | Trust the code |
| 26 | A challenge counted as built | The third challenge is locked with a 400 XP label and no code | Say "planned" |
| 27 | A broken link in the official repo | The `moi-sprint` README points to a Discussions page; Discussions are off | Fix or enable |

## C. Forge Hacks and the cohort
| # | Trap | Evidence | Rule |
|---|---|---|---|
| 28 | One channel, two names | README: `#dev-chat`. Playbook: `#help`. Three Discord invite codes across the repos | Choose one and make every document match |
| 29 | Office hours: daily or "ad hoc" | The kickoff call promised daily; README and playbook say "ad hoc" | Decide, then say one thing |
| 30 | A form named for one college | "Presidency College MOI Forge submission" | A new campus needs a new form and README |
| 31 | The form does not enforce the contract | The call required a README and an optional video; the form asked for team, GitHub link, members | Ask for what the rules require, or relax the rules |
| 32 | Late and duplicate rows | Responses ran to 2026-04-16 against a 2026-03-31 deadline. One team appeared twice with the same repo | Decide the cut-off and dedupe by repository link |
| 33 | A placeholder in a PDF | "Replace with Discord invite QR" is on the deck's last page | Search every PDF for placeholders before sending |
| 34 | A dead build script | `docs-to-pdf.sh` converts files that no longer exist. Sources are only in git history | Keep sources beside outputs |
| 35 | MAS0 mislabelled | The demo calls a Coco logic a "MAS0-style token"; MAS0 is a protocol-native asset | Check against docs.moi.technology before reuse |
| 36 | Third-party figures in the playbook | Bridge hack figures and "Rbridge by Ronin" | Check each with `moi-devrel/claim-check` |
| 37 | Gemini mishears the programme | "My Forge", "Server Labs" | Check every name taken from the notes |
| 38 | The onboarding guide was only partly read | The Drive text stopped at Step 2 | Open the document itself before relying on its end |

## D. awesome-moi, bounties and tracking
| # | Trap | Evidence | Rule |
|---|---|---|---|
| 39 | Links that point at files that are gone | Chapter 1 file, the tswap tutorial, the Coco GitHub releases page, a docs path (all 404 or missing, 2026-10-03) | Run the link check before every pull request (`awesome-moi.md`) |
| 40 | "Coming Soon" that never came | `solved-patterns/` and `web3-reimagined/` since January 2026 | Remove or date it |
| 41 | A code sample that is not run | The JS SDK sample uses the old `/babylon/v0` address | Run every sample on devnet before it stays |
| 42 | 217 rows read as 217 pieces | One piece on up to three platforms; creators on several rows | Count distinct pieces and creators |
| 43 | A bounty announced as open | The session 8 game day checklist of 2026-09-03 said the bounty was not live | Say "coming" until it works end to end |
| 44 | A response form edited after launch | Session II's sheet has two tabs with different questions | Read every tab |
| 45 | Payout assumed | No payout record exists in any source | Claude never pays. The operator pays after Rahul's yes |
| 46 | Plans mistaken for programmes | The Sprint plan's reward tiers, Bounty Board and Hero App are January 2026 proposals | Call them proposals. Do not offer them to anyone |
| 47 | Two calendars, two numbers | KRAs: 2 events a month. Programs: 1 call and 1 AMA. Events Calendar: 39 | Name the sheet and date beside every figure |
