# MOI Forge: the campus cohort lifecycle and onboarding

Facts are as of 2026-10-03. Confidence is low: the evidence is Drive titles and Gemini notes read on 2026-10-02, one uncommitted README, and the sheet "MOI Programs". No syllabus for weeks 2 to 12, no cohort roster and no outcome record was found. Everything marked "proposed" is a process the evidence implies, not one that is recorded. Back to `../SKILL.md`.

## What it is
MOI Forge is the campus programme. The sheet "MOI Programs" (Drive, shared by Rahul) lists two rows:
| Row | Owner in the sheet | What |
|---|---|---|
| MOI Forge, Basic | Sai Kiran | Campus roadshow and logistics. Weekly metrics: colleges executed, wallets created, Discord joins, forms submitted, X impressions |
| MOI Forge, Advance | Adithya (the previous operator) | A 12-week builder cohort, start December 2025. KPIs in the sheet: 1 project onboarded a month, 1,000 interactions a day, 1 demo day a month, 1 Builders newsletter a month, 1 video per project per week |
The hackathon (`forge-hacks.md`) is the selection stage between them. The owner of both rows today is not settled. ASK: Rahul. The Marketing Questionnaire (Drive) records that the previous operator wanted to own Forge, Sprint, awesome-moi and the academia collaboration.

## Cohorts on record
| Campus (as titled in Drive) | Dated trace |
|---|---|
| First cohort (the sign-up form is titled "Boiler Blockchain"; a Purdue link is inferred) | Sign-ups 2025-10-15 to 10-18. Launch 2025-10-20. Concept workshop (day 2) 10-28, day 2.5 on 10-29, Intro to Coco 10-30, JS SDK workshop (day 4) 10-31. Idea demo day 11-24, office hours 11-26 |
| PCCOE (the college's name as Drive titles abbreviate it) | Planning call 2025-12-23. Launch 2026-01-14. Follow-up 01-22. Onboarding workshop 01-30. Review call 2026-05-07 |
| Presidency College | Kickoff 2026-03-17 (30 participants present). Submission form created 03-16, due 03-31. Responses to 04-16 |
| Oxford and others | Named as upcoming on the Presidency kickoff call. Nothing else found |
The most recent dated trace of any Forge activity is the PCCOE review call on 2026-05-07. Whether any cohort is running now is not known. ASK: Rahul and Sai Kiran. Recordings sit in the Drive folders "MOI Forge Recordings" and "Meet Recordings" (who can open them is not recorded; ASK: Rahul). Gemini writes MOI Forge as "My Forge" and Sarva Labs as "Server Labs": check every name taken from those notes.

## The lifecycle (from the Presidency and PCCOE calls)
| # | Stage | What happens | Who | GATE |
|---|---|---|---|---|
| 1 | Agreement | A draft college agreement existed for PCCOE (an MOU, shared 2025-12-22). Its terms are unknown. A faculty contact is needed | Unknown. ASK: Rahul who signs and who holds the contact | Any contact with the college and anything legal: the operator only. Claude drafts nothing legal |
| 2 | Kickoff call | Whole cohort, about 28 minutes at Presidency: blockchain basics, why participant-centric, resources (docs, Coco, JS SDK, GitHub), the hackathon tracks, submission rules, timeline, what the 12-week Forge offers | The previous operator presented; Rahul co-presented technical parts at onboarding | Recorded Meet: no recovery phrase on screen or aloud |
| 3 | Channels | Share the Discord (office hours) and a WhatsApp group; share the brief and examples right after the call | Sai Kiran posted the Discord link; the previous operator sent the examples and the brief | Posting or sending |
| 4 | Onboarding workshop | About an hour for admitted cohorts (PCCOE, 2026-01-30): wallet set-up on the call, faucet claim, Voyage tour, asset playground, a simple Coco logic, deploy with the JS SDK, interact, a soulbound asset whose transfer fails on purpose. Everyone fills the onboarding form during the call | The previous operator, Rahul | The wallets are the students' own; funds are faucet funds |
| 5 | Onboarding guide | The 12-week cohort document (below) | The previous operator | Sending |
| 6 | Hackathon | Two weeks, daily office hours promised on the Presidency call (`forge-hacks.md`) | Mentors | Form creation |
| 7 | Selection | "Select top teams for interview", per the Presidency notes. How interviews and selection ran is not recorded | unknown | Any promise of an interview, internship or job |
| 8 | The 12 weeks | Demo days and one video per project per week, per the sheet's KPIs. The Sprint plan of January 2026 proposed a "Hero App" incubator: 5 to 10 teams a batch, an engineering residency, a fast track to investors, co-marketing, 3 to 5 office-hour hours a week. It is a proposal. No evidence it launched | unknown | |
The campus roadshow decks ("MOI Campus Road Show", a doc and a PDF in Drive) were listed by title only and not opened.

## The onboarding guide
The Drive document "MOI Forge Developer Onboarding Guide" is the "12-Week MOI University Developer Cohort" guide. The text read stopped at Step 2 (the document is large; the read may be incomplete). An uncommitted rewrite of `resources/moi-sprint/README.md` in the previous operator's clone of `moi-foundation/awesome-moi` carries the same guide. It is not on GitHub: a `git checkout .` there would lose it. Not recorded (the previous DevRel's notes); ASK: Rahul.
What it says:
1. First things first: fill the onboarding form (it "helps us track your progress"), join Discord (daily chatter, mentor DMs) and Telegram (announcements).
2. Step 1, Voyage: create a wallet ("Generate IOMe Id", save the 12-word mnemonic), claim the faucet (stated as 20K KMOI), explore the network.
3. Step 2, the sandboxes: the Logic Playground and the Asset Playground (links use `?network=babylon`).
4. A documentation hub and papers. 5. The Week 1 checklist: form, Discord, wallet, faucet, first logic in the playground, test asset in the playground. 6. "Ready to build?" points to Chapter 1 of `moi-foundation/moi-sprint`, which suggests the Sprint chapters are the curriculum (inferred).
The Drive version also holds a personal phone number and invite links. Copy neither.

## Check before you send it (all read 2026-10-03)
| Item | Finding |
|---|---|
| Wallet | "IOMe" predates the move of Voyage's login to MOI Wallet (late August 2026; the announcement post is dated 2026-08-27). Check what Voyage shows today |
| Network | The links use `?network=babylon`, a retired network name (`moi-devrel/references/terminology.md`, Contested 6). Voyage answers 200 for any query, so a link check cannot tell. Open them by hand |
| Faucet | 20K in the guide (2026-01-13), 100K on the 2026-01-30 call and on 2026-09-24. Check live. Never quote a number |
| Wording | "Testnet" for devnet. "Think of it as your home base" and similar metaphors. Direct wording since September |
| Links | Run the link check on the final file (`../SKILL.md` step 2). The Medium paper link answers 403 to a script: open it by hand |
| Safety | Keep the sentence that a recovery phrase controls the whole identity and is never shared. The cohort guide has it. A line telling students never to commit `.env` or mnemonics was added to the Forge Hacks README and removed the same morning, on its kickoff day (2026-03-17) |
| Promises | No internship, job, prize or payment wording without Rahul's yes. The kickoff material promised an internship fast track |

## Records and privacy
- The sign-up and submission forms hold names, emails, GitHub links, Telegram and Discord ids. One sign-up sheet has a phone number in the Telegram column; its columns are free text in mixed formats. Read headers and counts only. Copy no row.
- The Presidency kickoff notes list dozens of invitees by personal email. A photo of identifiable students needs their permission before it goes on a slide or a post.
- Student repositories contain student work. Cloning one is a download: say its name and source first (GATE). Do not list student names in a public file.

## Not yet known
- Whether the 12-week cohort is real, planned or abandoned; weeks 2 to 12; the deliverable rubric; selection and interviews. ASK: Rahul.
- Who owns Forge now, and whether any campus is in progress. ASK: Rahul, Sai Kiran.
- The terms of the MOU, and who signs. ASK: Rahul.
- Which Discord invite and channel are canonical. ASK: Rahul.
- What the PCCOE onboarding form asks (Drive forms cannot be read through the tools used). ASK: Rahul who can open it.
