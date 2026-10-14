# MOI Sprint: the self-paced challenge track

> Scratched from the handover on 13 October 2026; kept for the record. Do not route anyone to it and do not send students to it. The rest of this file describes what existed on 2026-10-03.

Facts are as of 2026-10-03. Sources: the research notes of 2026-10-02, the public GitHub repos and the live site read on 2026-10-03, and the previous operator's dependencies list of 2026-10-01 (section 21; not in the handover repo, and `project-handover-docs/LIST-OF-DEPENDENCIES.md` has no section for Sprint). Where they disagree the newer reading wins. Back to `../SKILL.md`.

## Before you touch anything
MOI Sprint: A security finding was open on this product as of 2026-10-02. The previous DevRel's note on it is not recorded; ASK: Rahul before touching its admin.

Do not send a student to the challenges or the guide site until Rahul says the programme is live (ASK: Rahul): `moisprint.com` does not resolve and the challenge pages tell students to clone an address that answers 404 (2026-10-03). A change to the site, its hosting or its on-chain logic is a GATE. Reading, linting and fixing text in a local copy are free.

## What it is
"Learn MOI by building. Complete challenges. Ship code." A mission-based path "inspired by Speedrun Ethereum". Each challenge is a standalone scaffold with stubs the student fills in, a guide page, checkpoints with a verify action, and XP. Built January and February 2026 by the previous operator (the Chapter 1 tutorial is signed "By: Adithya Ganesh (DevRel)"). No cadence: challenges were added one at a time. Not to be confused with MOI Forge (`forge-cohort.md`): in January 2026 the folder `awesome-moi/resources/moi-sprint/` was the Sprint home, and a local rewrite of its README now holds the Forge onboarding guide.

## The pieces
| Piece | Where | State |
|---|---|---|
| Chapter repo | `moi-foundation/moi-sprint` (public, `main`) | 3 commits, last 2026-01-13. Holds a README and `01-native-assets/README.md` (Chapter 1, 881 lines, Missions 1 to 7, added by a commit from `moi-rahul`). No Chapter 2 or 3 |
| Challenge scaffolds | `sarvalabs-adithya/tSwapper` (public, `main`, last push 2026-02-13) | Folders `SoulBound/` and `Swap/`. Each has a `.coco` contract with stubs, `deploy.js`, `src/lib/logic.js`, `test.js` and a Vite app on port 5173. Pins `js-moi-sdk` `^0.7.0-rc6` |
| Full solutions | branch `solution` of the same repo (public, 2026-01-12) | Zero stub markers in its contract and deploy script (read 2026-10-03; `main` has 3 to 6 per file). The history of `main` holds them too: commit `79de8e4` (2026-01-12) has contracts with zero stub markers. A different branch also called `solution` exists only on the previous operator's machine; its files carry the stubs but its history holds the answers |
| Guide site | `sarvalabs-adithya/moisprint` (public, `main`, last push 2026-02-13). Live at moisprint.vercel.app (answered 200 on 2026-10-03) <!-- slop-lint: ignore --> | Next.js 14.2. Pages: home, `/challenges`, `/challenges/soulbound`, `/challenges/swap`. Vercel project owner: not recorded (the previous DevRel's notes); ASK: Rahul. `moisprint.com`, which the READMEs cite, does not resolve (read 2026-10-03) |
| Progress logic | `contracts/SprintProgress` in the site repo | One logic per network, 20 per-participant completion flags. Its id lives in the site's environment and does not survive a devnet reset |
| Earlier prototype | `Sprint/` on the previous operator's machine | Not in git. A Next.js page and a first challenge. Not recorded (the previous DevRel's notes); ASK: Rahul |
| Local-only work | the site clone: 18 modified files (a redesign) and an untracked `contracts/AssetLogic/`; the scaffold clone: 4 modified files and the ignored `docs/PROGRESS_PLUMBING.md` (216 lines, in no commit) | Lost with the laptop. Not recorded (the previous DevRel's notes); ASK: Rahul |

## The challenge track (read on the live site, 2026-10-03)
| # | Challenge | Folder | Level | Time shown | XP | Checkpoints |
|---|---|---|---|---|---|---|
| 01 | Soulbound Badge | `SoulBound/` | Beginner | 1 to 2 hours | 100 | Understand the contract, deploy the asset, `getBadgeBalance()`, `issueBadge()`, try a transfer (it must fail), final verification |
| 02 | Simple Swap | `Swap/` | Intermediate | 2 to 4 hours | 250 | Read the contract, deploy assets and contract, `getSwapBalances()`, implement `transfer()`, implement `executeSwap()`, final verification |
| 03 | NFT Marketplace | none | Advanced | 4 to 6 hours, locked, "Coming Soon" | 400 | Planned, no code in the scaffold repo |
Chapter 1 is a longer tutorial for the same ground: wallet and provider, `getTDU()`, create two MAS0 assets, transfer, verify on Voyage, a soulbound token in Coco, then a fixed-rate swap.

## How a challenge was built (reconstructed from history; the order is inferred)
1. Write the complete solution first. 2. Strip it to a scaffold with stubs in three places: the contract, `deploy.js`, `src/lib/logic.js`. Keep the UI expecting `{ wallet, address }`. 3. Write `test.js` as pass/fail checks on the live network. 4. Write the guide page with checkpoints and collapsible hints. 5. Add the challenge to the site's card list, its verification rules and its XP map (`src/app/challenges/page.tsx`, `src/lib/challenges.ts`, `src/context/ProgressContext.tsx`) and to the server code that records progress. 6. Deploy the progress logic once per network. That is a deploy on devnet: a GATE that names the paying account. The hold above applies.
The pitch on the site is "no videos, no slides" and "checkpoint verified". The January 2026 Sprint plan wanted rewards tied to verified network activity, not completion (`bounties.md`).

## What the student does
Clone the scaffold, `cd SoulBound` or `cd Swap`, `npm install`, `npm run dev`, read the guide, fill the stubs, deploy, paste the ids into `test.js` and `logic.js`, run `test.js`. A student needs a funded devnet wallet and the recovery phrase of their own wallet in a gitignored `.env` (`students.md`). The operator never handles it.

## What is wrong today (each read or run on 2026-10-03 unless stated)
| # | Defect | Evidence | What to do |
|---|---|---|---|
| 1 | The live challenge pages tell students to clone `github.com/aspect-build/moisprint` | That address answers 404. It is not under `sarvalabs`, `moi-foundation` or the previous operator's account | Do not send the page to anyone. Which repo the page meant is not recorded (the previous DevRel's notes); ASK: Rahul |
| 2 | READMEs point to `moisprint.com` for guides | The host does not resolve | The live site is moisprint.vercel.app. Decide the real domain: ASK: Rahul |
| 3 | Chapter 1 setup does not match `main` | It says clone `tSwapper` and open `src/lib/logic.js` at the root; on `main` the file is under `Swap/` and `SoulBound/`. The root layout is on the `solution` branch | Do not point students at Chapter 1 and the scaffold together until fixed |
| 4 | Old SDK | Scaffolds pin `^0.7.0-rc6` (npm, 2026-01-28). the newest on npm is `0.9.0-rc2` (2026-09-09). The previous operator wrote on 2026-10-01 that both repos "will not run against today's devnet" | Run the whole path once on today's devnet before any student starts |
| 5 | Coco | Coco 0.9.3 (targets PISA 0.8.2) is the newest release as of 13 October 2026. Tested on 0.9.2 (cocolang.dev/docs/releases, 2026-09-28): `enlist` endpoints were rejected. The progress logic has one. The two challenge contracts do not. Not compiled by me, and not retested on 0.9.3 | Compile with the Coco version students will install. ASK: Gokul which version fits devnet |
| 6 | Stale model in Chapter 1 | It explains MOI as "Global State Machines" and an "Interaction State Machine" with "temporary, localized consensus lane". The founder's wording of 2026-09-14 is participant-centric and MDAG | Rewrite against `moi-devrel/references/terminology.md` before reuse |
| 7 | Faucet amount | Chapter 1 says "around 100k"; awesome-moi and the Forge onboarding guide say 20K | Do not quote an amount. Check live |
| 8 | Test command | Both READMEs run `test.js` with TLS certificate checks switched off (`NODE_TLS_REJECT_UNAUTHORIZED=0`). No reason is recorded | Do not copy it into new material. Why it was used is not recorded (the previous DevRel's notes); ASK: Rahul |
| 9 | Node | `moi-sprint` README and Chapter 1 say v16+, the scaffold READMEs v18+ | `students.md` |
| 10 | Wallet name | "IOMe" is used throughout; Voyage moved its login to MOI Wallet in late August 2026 (announcement post dated 2026-08-27) | Check what Voyage shows today |
| 11 | The `moi-sprint` README links GitHub Discussions | The repo has Discussions off; the link answers 404 | Remove it or enable Discussions |
| 12 | Handover | `docs/PROGRESS_PLUMBING.md` describes the flow differently from the code and is ignored by git | Trust the code. The file itself is not recorded (the previous DevRel's notes); ASK: Rahul |

## Naming
"MOI Sprint" is the challenge track. "MOI Forge" is the campus programme. Use each name for one thing. The folder `awesome-moi/resources/moi-sprint/` on GitHub `main` is a short Sprint README; the Forge guide there is an uncommitted local rewrite (`forge-cohort.md`).

## Not yet known
- Whether the Sprint site and both repos are archived or moved to the org. The 2026-10-01 dependencies list said "Decide if it is alive. If so, move both to the org." Sprint was then scratched (13 October 2026); what happens to the site and repos is open. ASK: Rahul.
- How many students used it, and whether any completion was ever recorded. Not recorded (the previous DevRel's notes); ASK: Rahul.
- Who owns the Vercel project and the admin wallet that deployed the progress logic. Not recorded (the previous DevRel's notes); ASK: Rahul. Neither is in `moi-devrel/references/keys-and-access.md`. <!-- slop-lint: ignore -->
- What `moi-sprint` should hold beyond Chapter 1, and whether it is canonical over `tSwapper`. ASK: Rahul.
- Whether Sprint relates to the challenges on the Points app (`moi-web-products-ops`).
