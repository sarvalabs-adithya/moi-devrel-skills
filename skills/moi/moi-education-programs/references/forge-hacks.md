# MOI Forge Hacks: running a campus mini-hackathon

Facts are as of 2026-10-03. One run is on record: Presidency College, kickoff Tuesday 2026-03-17, submissions due Tuesday 2026-03-31 at 11:59 PM. Sources: the public repo `sarvalabs-adithya/moi-forge-hacks-demo` (README, the deck PDF and the playbook PDF, read 2026-10-03), the Drive research of 2026-10-02 (Gemini notes of the kickoff call, the submission sheet's headers) and `DEPENDENCIES.md` section 22. Back to `../SKILL.md`.

## What it is
A two-week student hackathon that introduces participant-centric state. The prompt: each of three tracks already exists on Ethereum, so build it on MOI and show how participant-centric state changes it. No prior blockchain experience required. It is also the selection stage of the 12-week Forge cohort: winners are told they enter MOI Forge (`forge-cohort.md`).
Planned size: 50 to 70 students (playbook cover). The kickoff notes count 30 participants present.
Whether another campus will run it is not decided. No later run is on record. ASK: Rahul, and Sai Kiran for campus logistics. The demo repo's own to-do (2026-10-01) is "archive it, or move it to the org if the playbook is reused".

## What the Presidency run used
| Item | Content |
|---|---|
| Tracks | 1 DEX, 2 DAO (voting power from participation), 3 Bridge (MOI and another chain). Tracks are suggestions: combining or proposing is allowed if the participant-centric model is used (kickoff call) |
| Rubric | Use of participant-centric state 40%, Functionality 25%, Creativity 20%, Presentation 15%. "Even a partial working prototype beats a perfect slide deck" |
| Deliverables | A public GitHub repo with the Coco logic files; a README (problem, approach, how participant-centric state is used, setup and run, team members); a 2-minute demo video (YouTube or Loom). The form asked only for team name, GitHub link and team members, so the README and video were not enforced |
| Tooling rule | Hardhat and Foundry do not work. Use Coco and js-moi-sdk (kickoff call) |
| Materials | A kickoff deck (15 PDF pages), a 9-page playbook, the repo README as the event page, a demo dapp (`moi-dapp/`: a token logic and a deploy script) and a Solidity token file for contrast (`erc20-show-only/`) |
| Channels | A Discord server (kickoff day sign-up, team formation, office hours), a WhatsApp group, a Google Form for submissions |
| Outcome | Not documented: judges, winners, prizes, headcount, announcement. Nine form responses between 2026-03-31 and 2026-04-16 |

## Before the event
Work from `../templates/event-checklist.md`; the README skeleton, kickoff agenda and track brief are in `../templates/hackathon-pack.md`. The demo repo's first commit is dated 2026-03-16, the day before the kickoff, and the PDFs were rebuilt on the kickoff morning and again on 2026-03-20. Earlier planning may exist elsewhere. That is too little time to copy.
1. **Settle the facts with the owner first.** Campus, date, student count, who mentors, who judges, what is promised to winners. The playbook leaves judges and prizes blank. ASK: Rahul. Logistics: Sai Kiran, through the operator. Any college agreement (the PCCOE cohort had a draft MOU, shared 2025-12-22): the operator only; Claude drafts nothing legal.
2. **Run the devnet preflight** (`../SKILL.md` step 2) and run the demo once on today's devnet. The Presidency demo was last pushed 2026-03-20. Its token logic uses an `enlist` endpoint, which Coco v0.9.2 (2026-09-28) rejects; not compiled by me. Its SDK pin is `^0.7.0-rc10`.
3. **Rebuild the materials, do not reuse them.** Defects found in the March files are in the table below.
4. **One form per campus.** The Presidency form carries the college's name. A second campus needs a new form and a new README. Creating a form is a GATE.
5. **Decide the cut-off and the duplicate rule before announcing.** Rows kept arriving after the deadline (to 2026-04-16) and one team appeared twice with the same repo. Dedupe by repository link, and decide in writing whether a late row counts.
6. **Pick one support channel and one invite.** The README says Discord `#dev-chat`, the playbook says `#help`. Three Discord invite codes are in use across the programme repos. The kickoff call promised daily office hours; the README and playbook say "ad hoc". Decide, then make every document match. ASK: Rahul which server and channel are canonical.
7. **Send the invite and the README** (drafts in `../templates/onboarding-messages.md`). The operator sends. A message to students that mentions internships, jobs, prizes or payment needs Rahul's written yes first.

## During
| When | What |
|---|---|
| Kickoff (60 minutes, Presidency agenda) | 0 to 2 welcome; 2 to 7 what a blockchain is; 7 to 15 the contract-centric model on Ethereum; 15 to 22 participant-centric state with Coco side by side; 22 to 40 live demo (Coco walkthrough, SDK deploy, live deploy, frontend); 40 to 45 Voyage and faucet; 45 to 48 docs tour; 48 to 53 the three tracks; 53 to 58 timeline and rules; 58 to 60 join Discord |
| Build phase (14 days) | Students work remotely in teams. Mentors answer on Discord. Run the live demo from a funded devnet wallet that the presenter made in the MOI Wallet extension; Claude never handles the phrase (`moi-devrel/references/consent-and-identity.md` section 5) |
| Questions | Answer in the channel. A student who pastes a recovery phrase gets told at once that it is exposed and must stop using that wallet |
Spending devnet funds, deploying a logic or creating an asset for the live demo is a GATE: name the paying account. A kickoff on a Meet call that is recorded must never show or read out a recovery phrase (it reached Gemini notes on 2026-09-24).

## After (the evidence stops here; the rest is a proposed process)
Nothing is recorded after the form closed. Proposed, to be confirmed with Rahul:
1. Close the form on the deadline plus the agreed grace. Exporting the response sheet is a download (GATE). Save it only in `edu-work/`; it holds names and emails. Copy none of it into a repo, a note or a chat.
2. Dedupe by repo link. Open each repo: does it hold Coco logic files, a README and a demo video link?
3. Score with the published rubric, with two named judges (ASK: Rahul who).
4. Verify any on-chain claim by reading the chain (`moi-devrel/references/devnet.md`, "Before you say live").
5. Tell every team its result. The operator sends. Promise nothing that Rahul has not approved.
6. Write down the outcome: headcount, submissions, winners, what broke. This is the missing record.

## Defects in the March materials (read 2026-10-03)
| Where | Defect | Fix |
|---|---|---|
| Deck page 9 | "Free testnet COCO tokens". The fuel token is KMOI | Write KMOI |
| Deck, playbook | "testnet" (the README says "devnet") | Say devnet |
| Deck last page | The text "Replace with Discord invite QR" is in the PDF | Replace it |
| Deck page 10 | Links `github.com/moi-technology`; the README links `github.com/sarvalabs` | Pick the real org |
| Deck, playbook | A Coco logic called a "MAS0-style token". MAS0 is a protocol-native asset (Chapter 1 says native assets need no contract). The "ERC20 vs MAS0" table compares ERC-20 with that logic | Check against docs.moi.technology before reuse |
| Deck | Metaphors ("Google Docs, but for money", "the contract is the bank"). They predate the September rule of direct wording with no metaphors | Rewrite in plain terms from `moi-devrel/references/glossary.md`; `moi-devrel/explain` teaches the operator the idea first |
| Deck pages 13 to 14, kickoff call | Winners "enter MOI Forge" and top participants are "fast-tracked for internships and full-time positions". Approval is not recorded | Do not repeat without Rahul's yes |
| Playbook | Hack figures for Wormhole and Ronin; "Rbridge by Ronin" | Check every third-party figure (`moi-devrel/claim-check`) |
| README (twice) | `docs.moi.technology/docs/category/tutorials` answers 404 (read 2026-10-03) | Find the current tutorials page |
| Repo | `scripts/docs-to-pdf.sh` converts files that no longer exist. The source `.pptx` and `.docx` are only in git history (commit `e40e077`) | Keep the sources next to the PDFs |
| Repo | A "Security" note (15 low-severity transitive findings, and "Never commit `.env` or mnemonics") was added and removed on 2026-03-17, the kickoff day | Keep a recovery-phrase warning in every student document |

## Not yet known
- Judges, winners, prizes, headcount, how students were recruited, who mentored. ASK: Adithya, then Sai Kiran.
- Why commits in the student repos run to 2026-04-28 (an extension, or late commits).
- Whether another campus (Oxford was mentioned on the kickoff call) is planned. ASK: Rahul.
- The authoring tool of the deck and playbook, and the brand font and palette. ASK: Adithya. For brand, `moi-devrel/design`.
