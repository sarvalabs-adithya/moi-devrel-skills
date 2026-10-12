# Google Drive: what Drive shows about how MOI DevRel processes run

Research note for the DevRel skills project. Area: Adithya's Google Drive (adithya@moinetwork.io), read through the Drive MCP tools, read-only. Observed facts carry a Drive file id or title. Everything I could not see directly is marked "(inferred)" or "unknown".

Date of research: 2026-10-02. The most recent Drive item I saw was modified 2026-09-30.

## Sources read

### How I searched (read-only)

All calls were `search_files`, `read_file_content`, `get_file_metadata` or `list_recent_files`. I did not create, copy, share, update, trash or download anything, and I did not open any video.

Queries run (title/fullText/parent/owner filters, paging each to the end where a page token came back):

- Title contains: `MOI Builders`, `Builders`, `Webinar`, `Forge`, `x402`, `MOI` (3 pages), `Responses`, `Community Call`, `Calendar`, `Standup`, `Marketing Standup`, `Governance`, `Annual Calendar`/`Content Calendar`, `part 2 of 4`/`3 of 4`/`4 of 4`.
- Title contains OR-lists: `Run of Show / run-of-show / Speaker / Checklist / Agenda / Brief / Newsletter / Template`; `Hackathon / Demo Day / Office Hours / Bounty / Launchpad / Feedback / Survey`; `Registration / Feedback / Survey / Sign up / Signup / RSVP` with `owner = 'me'`.
- `mimeType = 'application/vnd.google-apps.form'` (all forms); `mimeType = folder and owner = 'me'` (all my folders).
- fullText contains: `run of show`, `run-of-show`, `speaker brief` (noisy: it matched every file with "run" or "show", so I do not rely on it); `MOI Builders`; `hacks playbook`, `hackathon brief`.
- `parentId = <id>` for each folder named in this note (Webinar 7, the three x402 folders plus the x402 review package, DevRel, Academic Outreach and Emails, JS MOI Docs, Launchpad video, MOI Content and its Week 11 to 19 folders, Community Call, Community Call 6, Google Meet).
- `sharedWithMe = true` clauses: `... and mimeType = form` (no results), `... and (Webinar | Checklist | Template | Run of show | Speaker | Feedback | Registration)` (no results), `... and title contains 'Programs'` (found MOI Programs, so the clause works). Owned and shared items also come back mixed in the plain title queries, marked by `owner` versus `sharedWithMeTime`.
- `list_recent_files orderBy=lastModified` (to see the most recent traces).

### Read in full (content)

| Item | Drive id |
|---|---|
| MOI Documentation Standard (v1, 14 Sep 06:24, 17 KB) | `1HEmf2p4-V3vuoLHMJlChfEIvTmTzSKISlWVmVKuAn8Q` |
| MOI Documentation Standard (v2, 14 Sep 07:31, 23.7 KB) | `1dyecUYxkslB5wbbbYI7nAfGFcROY-gyLbRJzNCmzrKg` |
| MOI SEOGEOAEO Sweep Status | `1ecNM7E9vYd5BgZmKQcLxncMYMg9_RStdtsUdc2N7fkM` |
| x402 review package: 00 START HERE, BG1, BG2, BG3, PR1a, PR2a, PR3, PR4, zz-convert-test | ids in "Reusable assets" |
| x402 10 Sep review docs: PR 1 (snippet only), PR 2 (full), PR 3 part 1 of 4 (snippet only) | ids in "Reusable assets" |
| PR-1-CASA-namespace (14 Sep, participant-centric + governance) | `18_L_ffYPAk_d-Ms8NXlt3MxAKOcliuxGohjd9vetjeI` |
| MOI_Builders_S7Deck.pptx (text and speaker notes) | `1NqODoRaFl_jwFy-Suf3rtTzvk2_k4sJw` |
| MOI Builders III - Agent Registry, Notes by Gemini (incl. transcript) | `1wvf3_lc4FPVPogceqjpAsZdMXSYoSkhvjV0okLcQMNc` |
| MOI Builders II - Native Assets (Responses) (headers only recorded) | `1cF9MBVlni614U53XowpAw9q3IwAgY11vzliIRS6RF88` |
| Presidency College MOI Forge submission (Responses) (headers only recorded) | `1beRta2H-sey-5OA8U2L84AtXOHKkbyMbReAyVmydD90` |
| Boiler Blockchain (Responses) (headers only recorded) | `1-kH1kt7fJtTnwNOlYRLf7I-6Wv2jtQ9OKJRcCR9Ez7g` |
| MOI Forge Developer Onboarding Guide | `10gIG8cbwH9BdI7OEHC36xWn4HkvYax1SyE-ncaH-oTU` |
| MOI Forge <> PCCOE Onboarding, Notes by Gemini (30 Jan 2026) | `1A2L22Xl48duYnmHmlwWybP2sCKbd1UIQWx2rSI_WZ5k` |
| Join Us Today: MOI Forge Kickoff at Presidency, Notes by Gemini (17 Mar 2026) | `1ACG9DDKZbXx52vaSX7zW8-dvbkQ5zr_yTKco1S_5vPc` |
| Adithya KRAs | `16fDyfr4o84N4OWYmXWQW1qn7lm45Cj0hbbzPg-rPMNI` |
| Marketing Questionnaire | `1T2AmGpTX5yNKLtA0JhkSzjM3cRZ14w0gVq-dOBY_TJw` |
| MOI Sprint: Strategic Launch Plan (Sprint, Bounty Board, Forge "Hero App" proposals) | `1HA-vUP8NhDj5lBEFlFFcX2CcQULdcYvWqKmleDOfP58` |
| DevRel Planning Document Template | `1Wuji90KkFXRfOUu3Dbi9gRnFNdxAi_0YGBmBFeWSSl0` |
| MOI Programs (sheet, shared by Rahul) | `1q9rsWhWqMdCDO0XdI1i46ap22n4UkkSRFH6Bb2U-hlk` |
| MOI Socials (sheet, shared by Sai Kiran) | `19f5gOIlU5ksusXxCdPr-kCD7F-_Kyrv_AJ87FgO3UoY` |
| Community Call + AMA Calender 2026 (sheet) | `1iNsT9pHoSnA8eysz2-Iq9y3iSBwNk_anPpkeFwC2U6Q` |
| Marketing Events Calendar (sheet) | `1DKzB60lXAA43nMAiJQtBORoDjeljcL6nNxlGzB4sp_c` |
| Community call script (Sep 2025), Community Call - Agentic Economy Boom (Mar 2026), Community call (Mar 2026) | `1J1-UiQyUzK-Xdm2hu0OeWOLxARCkJdktuKIkRo1qMOE`, `1jj0NUPRndgBlTEY7RdPyEhAI7gOoP-neUH5ZJIW3_d4`, `1wJT7kjxgjj18YKWZmWFmY-avw_1Ga3ceI5zFXAbakFU` |
| Marketing Standup Notes by Gemini, 6 Aug and 7 Aug 2026 | `1sEX8h1T9eXagK7_pIaR2WfkCfWTRNknaCupVMWejZHM`, `1GMNrbH-zOw1NcedEtdTqyE44l9T6h1G1YIOuO6tMXjE` |
| MOI Marketing Governance Call Notes by Gemini, 14 Apr 2026 | `1wZJLJBf9LUe4u08ETd0u3Rho1oTG3k_qFAlleSlpvwQ` |
| MOI Technology - Bounty Content Submissions (structure only) | `1cYfpOXmD8KF9vevaD_HOwSi5lVQEKJgt7g5WNyZNK34` |
| Points progam issues (audit findings list) | `1lChj6-Z25hUwY3WHlDZbHAxfGMbqR02v9T9C0yZJ_a0` |
| Meeting started 2026/09/24 13:53 EDT, Notes by Gemini | `1Kd5-M-7XgwaOvUZpwcvBYkX3RdcCdIMlvp35lOE_70M` |
| List of dependencies (2026-09-30, empty) | `1-Eg-NHaDHWcwii6DSW9f_9sJS8RoIZRkalWQWr_5lS4` |

### Seen by title and metadata only (not opened)

- All videos (Builders II recording, the standup recordings, Forge recordings, Launchpad clips). Titles and dates only, per the brief.
- MOI Annual Calendar (355 KB, owned by Sujatha), Cocolang docs feedback (1.5 MB), MOI Campus Road Show (doc and PDF), Builders II Gemini notes (two docs), the Forge planning, launch, kickoff and demo-day Gemini notes other than the two above, the Jan and Feb marketing standup transcripts.
- The Google Forms themselves (see next paragraph).

### What I could not read

`read_file_content` refuses Google Forms (unsupported mime type). The error suggested `download_file_content`; I did not use it because downloading is outside the read-only list I was given. So **I could not see the question lists of any Google Form**. Where I describe form fields below, the source is the form's linked response sheet headers (the headers are the question titles) or what Adithya said on a recorded call. Forms without a readable response sheet are marked "questions unknown".

### Privacy handling

The response sheets I opened contain other people's names, emails, wallet addresses and (in one sheet) a phone number. I recorded only column headers, row counts and date ranges. I did not copy any name, email, wallet address, asset id, hash, GitHub URL or social handle. Gemini notes of the Presidency Forge kickoff list dozens of invitees by personal email; none are recorded here. The Forge Developer Onboarding Guide contains a personal phone number and a Discord and Telegram invite; I recorded none. The 24 Sep Gemini notes captured the seed-phrase confirmation words read out on a screen share; I did not copy them (see Traps).

### Which processes leave a trace in Drive, and what the trace looks like

| Process | Trace in Drive |
|---|---|
| Builders webinar session | One Google Form per session in My Drive root (`MOI Builders <Roman numeral> - <Topic>`), Gemini notes and a recording in Drive shared from the `info@moi.technology` account, one session folder (`Webinar 7`) holding a pptx deck and two raw `.mov` demo clips. |
| Builders proof-of-completion collection | Forms plus (for session II only) a `(Responses)` sheet. |
| Webinar and launch video production | Raw numbered clips `1.MOV` to `11.mov` in `Launchpad video`, edited outputs owned by an external editor, an editor-owned `Builder series/MOI BUILDERS SEARIES VII.mp4`. |
| Community calls and AMAs | A 12-row calendar sheet, one agenda doc per call, a spoken script doc, a call folder with a PDF deck and recap videos, Meet recordings under the shared `info@moi.technology` account. |
| Marketing standups and governance calls | Daily-ish `MOI Marketing Standup - <date> <time> IST - Recording` mp4s from `marketing@moinetwork.io` (about 35 between 2026-05-05 and 2026-07-31), Gemini notes docs, a Monday-ish governance call. |
| MOI Forge campus cohorts | Forms (onboarding, submission), response sheets, Gemini notes for launch, planning, onboarding, kickoff and review calls, recordings in `MOI Forge Recordings` and `Meet Recordings`, an onboarding guide, an MOU draft. |
| x402 and CASA submission packaging | Three generations of Google Doc packages and one docx set across four folders. |
| SEO/GEO/AEO docs sweep | A status doc and a mandatory standard (two versions). |
| Bounty content campaign | A shared sheet of 217 submissions from 103 creators (as the sheet's own header counts them). |
| Programme design and tracking | MOI Programs, MOI Sprint Strategic Launch Plan, DevRel Planning Document Template, Adithya KRAs, MOI Socials weekly metrics. |
| Meeting capture itself | Every calendar event produces a `Notes - <event title>` doc in My Drive root, and every recorded Meet produces a recording plus `Notes by Gemini` plus a `Chat` text file in `Meet Recordings`. |

### In Drive but, as far as I could check, not on disk

My disk check was weak: a filename `find` (depth 5) and a time-limited grep over `*.md` for distinctive phrases. Findings:

- **On disk and in Drive (same content, different state):** the x402 review package (`x402-compat/review-package-gdocs/*.docx`, 11 files whose names match the 9 Sep Google Docs; the on-disk PR3 file is titled "STATUS (not this round)" while the Drive PR3 doc is titled "(built)", so the Drive copy was uploaded after the build) and the Builders session 7 deck (Drive: `MOI_Builders_S7Deck.pptx` in `Webinar 7`; disk: `MOI-Webinars/session-7/deck/MOI_Builders_S7-new.pptx`, a different file name).
- **Drive-only as far as I could tell:** every Google Form and response sheet; the Gemini transcripts of Builders II and III and of all Forge, standup and governance calls; the Forge Developer Onboarding Guide; Adithya KRAs and the Marketing Questionnaire; MOI Programs, MOI Socials, both calendars; the community call docs and the Community Call 6/8 folders; the MOI Documentation Standard and the SEO sweep status doc (a grep for their distinctive phrases found nothing on disk, but the grep was time-limited and not exhaustive); the Bounty Content Submissions sheet; the 14 Sep revision of the CASA PR doc.

### What I looked for and did not find

- A standard blank form that gets copied for each webinar. There is no file titled template or master. See Process 2.
- Registration forms. The Builders forms are not registrations (Process 2). Registration appears to be on Luma (inferred, from Gemini notes of Builders III). No Luma export is in Drive.
- Feedback or survey forms of any kind, for webinars or Forge (title searches for Feedback, Survey, RSVP, Signup returned only `Cocolang docs feedback`, a docs review doc).
- Forms, decks, folders or Gemini notes for Builders I, V and VI; response sheets for Builders III, IV and VII; Gemini notes or recordings for Builders IV, V, VI and VII in My Drive. Only Builders II and III have Gemini notes and only II has a recording in Drive. Only session 7 has a per-session folder (no Webinar 1 to 6 folders by title).
- A run-of-show or speaker briefing doc, although the KRAs require one 48 hours before each call. The nearest items are `Community Call - Agentic Economy Boom` (per-speaker bullet agenda) and `Community call` (slide content plus fireside questions).
- The Forge hackathon brief and the "MOI Forge hacks playbook" mentioned on the 17 Mar kickoff call (searched by title and fullText).
- Parts 2 to 4 of "PR 3 - @x402/moi package - review doc part 1 of 4 (10 Sep)".
- A newsletter, a checklist doc, or a named content calendar owned by Adithya (the calendars are owned by teammates).

## Process: MOI Builders webinar session (the live developer webinar series)

### Purpose

A recurring live developer webinar in which Adithya demonstrates one MOI capability end to end on Voyage devnet, then sets a challenge so attendees repeat it. Series arc seen in Drive: II Native Assets (2026-06-12), III Agents on MOI / Agent Registry (2026-06-18), IV Swaps (form created 2026-07-03), VII Agentic Payments (form created 2026-08-07, deck exported 2026-08-06). The 18 Jun transcript says "session three of the MOI builder series", with session one on deploying a first logic and session two on minting native assets. Session numbers I/V/VI have no Drive items (see Open questions).

### Trigger or cadence

Weekly in June (II on Fri 12 Jun, III on Thu 18 Jun; III's transcript says "last week we minted native assets") but irregular after: IV form in early July, VII in early August. The 6 Aug standup records the marketing team keeping Thursday free for "Adi" sessions (weekly cadence decision: Wednesday AMA, Thursday AI/developer session, Friday game night). Start time 18:22 to 18:23 IST on the two sessions with Gemini notes (2026-06-12 and 2026-06-18). Observed length: transcription ended at 00:51:51 for session III.

### Who does it

Adithya presents. A colleague watches chat ("Bertan's going to be helping me out here... drop questions in the chat", III transcript). The meeting is held from the shared org account `info@moi.technology` (the Gemini notes list "MOI Technology" and Adithya as invitees; recording and notes are owned by that account and shared into Adithya's Drive). Video editing is done by an external editor (Process 3).

### Inputs needed before starting

- A working demo against Voyage devnet and a public repo ("the repo link's in the description. Everything I run today is in there", S7 deck slide 1).
- A funded devnet wallet (one covers the whole demo per S7 slide 7; funded from the Voyage faucet at voyage.moi.technology). The mnemonic is held in the demo repo's `.env` (never record its value).
- A deck with the spoken script in the notes (see Steps).
- A bounty or challenge for attendees (III: 500k and 1M token challenges; amounts as Gemini heard them, verify before reuse).

### Steps in order

1. Pick the topic as the next step of the arc. III opens with callbacks to the two previous sessions; S7 closes with a teaser table "three questions, three sessions" (07 Who am I paying? done; 08 What may I spend? next; 09 What if you don't deliver? after).
2. Build the demo repo with setup scripts. S7 slide 7 lists the attendee run-book: `npm install`, `cp .env.example .env`, paste a funded mnemonic, `npm run setup:asset` (mint the settlement asset), `npm run setup:registry` (put both agents on chain), `npm run ui` (agent console on `http://localhost:4000`).
3. Create the registration page on Luma (inferred: III next steps say "attach the agent submission form to the Luma event page"; no Luma artifact in Drive) and schedule the Meet from `info@moi.technology` (inferred from who owns the recordings and notes).
4. Create the session's Google Form (Process 2) so submissions can open at the end of the session.
5. Build the deck as a script. S7 deck, 7 slides, each with a bracketed speaker script: `[ DECK · slide N ]` spoken text, `[ >>> SWITCH TO BROWSER — http://localhost:4000 ]` cues, `[ CAREFUL: ... ]` and `[ DON'T say ... ]` guardrails, a typed demo prompt, per-card narration lines, a "LIKELY QUESTIONS" block (Q and A pairs), a close with next-session teaser. The pptx's first text element is "index.html", so the deck was probably authored as HTML and exported (inferred).
6. Record fallback demo clips. `Webinar 7` holds `Vid1.mov` and `Vid2.mov` (modified 2026-08-05 22:11 and 22:33 UTC), created the day before the session (inferred to be backup or promo clips; I did not open them).
7. Rehearse the failure paths. S7's notes contain operational lore that only comes from rehearsal, for example: "If a normal run refuses: an interrupted tamper run left the registry dirty. Rerun it, let it finish."
8. Run the session. Observed order in III: recap of previous sessions, what the session will do, concept, demo 1 (bare SDK, one script, one transaction, verified on Voyage), demo 2 (same thing through an agent framework via a `skill.md`), questions, challenge announcement, roadmap, close. S7 order: identity setup slide, setup/cast, live demo in the browser with cards arriving about 6 seconds apart, a "refusal" demo (tick "Simulate a compromised listing"), a code slide, a "what's missing" slide run with a terminal command first, "where this goes", "go build".
9. Verify the demo live on the Voyage explorer ("Voyage generally sees it before cursor does", III), because the audience can look up every hash.
10. After the call: send attendees a summary with links to the bounty and the GitHub repo; add the submission form to the Luma page; upload step-by-step instructions to the repo (all three are the next steps recorded in the III Gemini notes, assigned to Adithya).
11. Verify submissions on chain by hand ("I'm going to verify each and every agent myself", III).
12. Hand the recording to the editor (Process 3).

### Deliverables and where each ends up

- Live session on Meet: recording, Gemini notes, chat log in the shared account's Drive (shared to Adithya).
- Deck: `MOI_Builders_S7Deck.pptx` in `Webinar 7` (id `15XuMwgDXdqsKvx_OdL0G0cWs6f1OeoYC`).
- Form (and sometimes a response sheet) in My Drive root.
- Public repo and the recap message (not in Drive).
- An edited recording for YouTube or socials (Process 3).

### Accounts and tools

Google Meet and Gemini notes (login: `info@moi.technology`), Luma (login; not in Drive), Google Forms (login), GitHub (public repo), Voyage explorer and faucet (no login for browsing; a wallet to claim), Discord (challenge submissions were also collected in Discord chat, III), Cursor shown on screen in III, a local Node app. No API key is named in Drive; the S7 demo uses a model for pricing and judgment, the key source is unknown.

### Quality rules and house style

From the S7 deck notes:
- "No code on screen, concepts." Each concept card states the problem, how the file solves it, why it is built that way.
- Run the command first, then talk over the slide (slide 5).
- Say the honest caveat out loud: the demo's forecast is made up, the payment is real.
- Do not overclaim: "DON'T say the env var makes it pay anything".
- Land one clear idea per session ("Models decide preferences. Code decides validity.") and set up the next session.
- Q&A answers prepared for the likely hard questions, including the unflattering ones (seller takes the money and does not deliver: you lose it, session nine fixes that).
- From III: open with callbacks so each session stands on the last.

### Traps and things that failed silently

- III's live demo failed twice on camera: running the script from the wrong directory, and a `discover` script that should list ~15 agents but did not load. The presenter apologised ("technical difficulties") and cut a prompt for time. The S7 deck's defensive notes read like a response to this (inferred).
- Gemini mangles names: "Moy" or "MOY" for MOI, "KOI" for KMOI, "Open Claw", "Hermes", "Grock" for Groq, "My Forge" for MOI Forge, "Server Labs" for Sarva Labs. Do not copy token amounts or names from Gemini notes without checking.
- The II session produced two Gemini note docs 9 minutes apart (18:14 IST, 4 KB; 18:23 IST, 26 KB), i.e. a Meet was started twice (inferred false start). Use the longer one.
- The S7 deck's replay-protection claim in Q&A depends on an in-memory set, so restarting the seller resets it. Say so, as the deck notes do.

### How long it takes

Session about 50 minutes (III). Deck preparation time is unknown. For VII the deck was exported on 2026-08-06 (03:59 UTC), the 6 Aug standup (Thu, 22:00 IST) says "tomorrow Adi is doing the session" (a Builders session on Fri 7 Aug, inferred), and the form was created at 11:50 UTC on 7 Aug, the day of the session.

### Open questions

- Where the registration list lives (Luma?) and who sends the reminder emails.
- Where decks and recordings for I and IV to VI are kept.
- Whether V and VI happened under those numbers.
- Which model and key the S7 demo uses for pricing and the judgment step.

## Process: Per-session Builders form (proof-of-completion and bounty submission)

### Purpose

Collect on-chain proof that an attendee did the session's exercise, so bounties can be paid. The forms are not signup forms. The evidence is the headers of the only response sheet that exists, plus what Adithya says about the challenge on the III recording.

### Trigger or cadence

One per session, created on or just before the session day. Created: II 2026-06-08 23:37 UTC (about 3.5 days before the webinar), III 2026-06-18 11:37 UTC (session day, about 75 minutes before the 18:22 IST start; note the Meet title is "Agent Registry" while the form is titled "Agents on MOI"), IV 2026-07-03 04:03:36 UTC, VII 2026-08-07 11:50:58 UTC.

### Who does it

Adithya.

### Inputs needed before starting

A decision on what proof demonstrates the exercise (wallet address plus an asset id, a transaction hash, or an agent id plus owner wallet).

### Steps in order

1. Create the form (probably by copying the previous session's form and renaming it; see below).
2. Set questions to the proof for this session. Observed fields (from the II response sheet, which has two tabs):
   - `Form responses 1` (5 responses, 13 to 17 Jun 2026): Timestamp, Email, Wallet Address, `MAS0 Asset ID(Demo 1)`, `MASX Asset ID (Demo 2)`.
   - `Form responses 2` (2 responses, 19 and 22 Jun 2026): Timestamp, Email, `wallet address`, `Transaction Hash`.
   - III's challenge (from the transcript): agent id plus the wallet that owns it ("submit your agent ID plus the wallet that owns it"); questions unknown.
   - IV and VII: questions unknown (no response sheet in Drive).
3. Attach the form link to the Luma event page and to the post-session recap message (III next steps).
4. After submissions arrive, verify each on chain (explorer or SDK) and pay the bounty (mechanism for payment is not in Drive).

### Deliverables and where each ends up

The form in My Drive root. A `<form title> (Responses)` sheet exists only for II (created 2026-07-10 14:30 UTC, after the sheet's data dated 13 to 22 Jun, so the destination was probably linked or relinked after the fact (inferred)).

### Accounts and tools

Google Forms and Sheets (login). Voyage explorer for verification.

### Quality rules and house style

None written down. The only observable rule is that proof must be verifiable on chain without trusting the submitter ("everything's on chain. So I'm going to verify each and every agent myself").

### Traps and things that failed silently

- Only the II form has any response sheet in Drive. For III, IV and VII the form either has responses attached to a destination I cannot see, or collects nothing, or the destination was deleted. Unknown.
- The II sheet's second tab shows the form was reconfigured after the first batch (new question set, new tab, only 2 responses). If a form is edited after launch, Google creates a new tab; reconcile both.
- "Is there a standard form that gets copied?" Observed timestamps are consistent with copy-and-rename, not proof: forms II and III were both modified at 2026-07-03 04:02 UTC and form IV was created at 04:03:36; an `Untitled form` was created 2026-07-16 13:25:26 UTC, six seconds after the II form's `viewedByMeTime` of 13:25:20 (typical of "Make a copy", inferred). Three `Untitled forms` exist (2025-09-12, 2026-07-10, 2026-07-16) and are never renamed, so a copy that is not renamed is indistinguishable from a stray form.

### How long it takes

Unknown. VII's form was created and then last modified 42 seconds later.

### Open questions

- What the questions are in each form (need the form editor or a download).
- Where III, IV and VII responses go.
- Which prior form is the copy source for the next one.

## Process: Webinar and launch video production (raw clips, external editor, final)

### Purpose

Turn recorded sessions and demo clips into publishable videos (Launchpad launch video; Builders VII recording).

### Trigger or cadence

Per launch or per session; seen for the Launchpad launch (4 to 6 Aug 2026), podcast episodes (31 Aug), and Builders VII (edited file dated 2026-09-07, a month after the session).

### Who does it

Adithya records raw clips; an editor outside the org domain edits (a personal Gmail account owns the output files; address not recorded; the 7 Aug standup names an editor "Krishna", the match is inferred). The 7 Aug standup says the editor edited this kind of video "for the first time" and the recording session took 3 hours with "a lot of iterations on the frame, the script and everything" (said by a teammate).

### Inputs needed before starting

Script and screen recordings.

### Steps in order

1. Record clips (QuickTime `.mov`, so probably a Mac, inferred) and upload them to `Launchpad video` (`1wlTotjRXeUpz9UNPp5T5qBBc-8QcZbwr`): ten numbered `.MOV`/`.mov` files in the range `1` to `11` (no `8` seen; uploaded 4 to 5 Aug 2026), plus a `Launch Video` shortcut (observed).
2. The editor posts versions into the same folder: `VIDEO.mp4` (5 Aug), `Final video.mp4` (6 Aug), `F_outro` and `Without-outro-F` (6 Aug, 740 to 754 MB each).
3. For a Builders session, the editor creates `Builder series/MOI BUILDERS SEARIES VII.mp4` (editor-owned, 866 MB, 7 Sep), nested under the Launchpad video folder. Podcast episodes go in `POD` in the same folder (`PODCAST--2.mp4`, 2.1 GB).
4. The edit is discussed in the 7 Aug standup; where it is posted is not recorded in Drive.

### Deliverables and where each ends up

Mp4s in editor-owned subfolders of the Launchpad video folder.

### Accounts and tools

Google Drive upload; editor's own tools (unknown).

### Quality rules and house style

From the 7 Aug standup decision: on YouTube, post video AMA clips only; voice-only AMA clips "didn't work well" and should be dropped.

### Traps and things that failed silently

- The Builders VII video file name has a typo ("SEARIES").
- Outputs are in a folder named for a different project (Launchpad), and the editor owns them, so they are not under Adithya's quota or `owner = 'me'` searches.
- Raw clips and finals are multi-hundred-MB; do not copy them into other folders.

### How long it takes

Launch video: raw clips 4 to 5 Aug, finals 5 to 6 Aug, discussed as done on 7 Aug. Builders VII: a month from session to edited file.

### Open questions

Who the editor's contact is, the brief format, and whether Builders I to VI were all edited.

## Process: Community call and Twitter/Telegram AMA programme

### Purpose

An official, regular communication layer: monthly community call (dev updates plus guest) and monthly AMA. Defined as programme "MOI Community Updates" (owner Adithya) in MOI Programs: 1 community call and 1 X AMA per month, tracking engagement rate and click-through to website and docs.

### Trigger or cadence

- KRAs (Jan 2026): "2 per month" (community call plus Twitter AMA), prepare a run-of-show and speaker briefing doc 48 hours before the call, publish notes, recordings, resources and action items within 24 hours, log Q&A and follow-ups within 48 hours with owners, agenda per week, one internal sync per week with engineering, BD and marketing.
- Calendar sheet `Community Call + AMA Calender 2026` (owner Vardan, shared): Community Calls tab, one row per month with EXPECTED DATE and RESERVE DAY a week later (3rd/4th Friday pattern: 23 Jan, 20 Feb, 20 Mar, 17 Apr, 22 May, 19 Jun, 24 Jul, 21 Aug, 18 Sep, 23 Oct, 20 Nov, 18 Dec); columns CORE TOPIC, TARGET GUEST, SPEAKERS (almost entirely blank; only January has a topic: "Community Campaigns + Dev Updates"). AMA (Twitter & Telegram) tab: 2nd Friday with a Wednesday reserve (9 Jan, 13 Feb, 13 Mar, 10 Apr, 15 May, 12 Jun, 17 Jul, 14 Aug, 11 Sep, 17 Oct, 13 Nov, 11 Dec), core topic only for January ("Community + Messaging").
- Marketing Events Calendar (shared): 39 planned 2026 events (20 Game Nights, 10 Telegram AMAs, 9 Community Calls), Events tab columns Date, Day, Event Type, Topic, Guest Speaker, Team, Event Details, Communities to tag, plus monthly grids.
- Actual: Community Call #7 on Sat 2026-02-28 19:50 IST (recording), Community Call 8 "Agentic Economy" on 2026-03-20 (deck PDF in `Community Call 8`); CC 6 recap videos filed 2026-02-05. The Aug 7 standup plans the next call after an all-hands call, roughly two weeks later.

### Who does it

Adithya owns the programme per the KRAs and MOI Programs. A host (the "Rutha"/"Ruta" opening and closing the call, per scripts) and a guest. The Aug 2026 standups show teammates (Vardan, Sai Kiran, Piyush) coordinating the next community call, so ownership may have moved (inferred; see Open questions).

### Inputs needed before starting

A topic and guests; dev update content (versions shipped); slide deck; fireside questions.

### Steps in order

1. Reserve the date from the calendar sheet (expected or reserve day).
2. Draft the agenda doc, one block per speaker. Example: `Community Call - Agentic Economy Boom` (`1jj0NUPRndgBlTEY7RdPyEhAI7gOoP-neUH5ZJIW3_d4`): Opener, Dev updates (Adi, "waiting on content"), a speaker block with five talking points, a guest block with four, community updates.
3. Write the dev update as three slides. Template in `Community call` (`1wJT7kjxgjj18YKWZmWFmY-avw_1Ga3ceI5zFXAbakFU`): Slide 1 language updates (Coco version and a Coco Skills reference pack), Slide 2 VS Code extension (features and validation counts), Slide 3 SDK and infrastructure (js-moi-sdk and go-moi versions, wallet beta, docs overhaul). In Sep 2025 the dev update was a spoken script (`Community call script`, `1J1-UiQyUzK-Xdm2hu0OeWOLxARCkJdktuKIkRo1qMOE`) with three headings: execution and interoperability layers, the main client, research and network rollout.
4. For a fireside guest, write exactly three questions and a rewritten pair. The Mar 2026 doc carries 3 questions twice (a plain version and a longer version for the host).
5. Note where deck slides come from (the doc points at a Canva deck, "slides 2-8 directly as is and then slide 12").
6. Hold the call in Meet (recording under `info@moi.technology`); the AMA runs on Twitter and Telegram (the calendar tab is named "AMA (Twitter & Telegram)").
7. Post-call: publish notes, recording, resources, action items within 24 hours; log Q&A within 48 hours (KRAs). Recap videos are cut and filed in the call folder (CC 6: `CC 6 Recap.mp4`, `The Onboarding Begins.mp4`, `This Is How Real Adoption Actually Starts.mp4`).

### Deliverables and where each ends up

Agenda docs and script docs in My Drive root; recording in Meet Recordings (shared account); deck PDF and recap videos in `Community Call/<Community Call N>` under a folder `1kUKlbCTgpGcE-UBs010LIirQGuhDbvN4`.

### Accounts and tools

Google Meet (`info@moi.technology`), Luma, X (X Spaces/AMA), Telegram, Canva (login), Google Sheets.

### Quality rules and house style

Timing rules from the KRAs (48h/24h/48h). Guest questions limited to three. Dev updates written as versions plus one-line impact per item.

### Traps and things that failed silently

- The calendar is almost empty: dates are reserved but topic, guest and speaker are blank for 11 of 12 months. CC #7 happened on 28 Feb, not on the expected 20 or reserve 27 Feb, so the calendar drifts.
- No doc titled run-of-show or speaker brief exists, although the KRAs require one.
- The Mar 2026 `Community call` doc says "(For Lou intro slide add CM and DAIAA logo)": logos for guests need to be gathered and are easy to forget.
- The Sep 2025 script promises "Go-Moi v0.12.0 to the public devNet by the end of September" and the Mar 2026 doc lists go-moi v0.11.0; the x402 START HERE doc says devnet answered `0.12.0` on 9 Sep 2026 and a v0.13.0 is awaited. Version statements in scripts age fast; check the live version before saying one on a call.

### How long it takes

Unknown.

### Open questions

Who runs the next calls; whether the Q&A log and notes were published within the 24/48-hour targets; where recordings for CC 1 to 5 and 9 onward are.

## Process: Marketing standup and governance call (cadence, decisions)

### Purpose

A shared standup where social, content, partnership and developer updates are aligned; a separate governance call hosts longer demos. DevRel inputs (Adithya's Thursday session slot, community call timing) are decided here.

### Trigger or cadence

Observed from titles (all recordings are owned by `marketing@moinetwork.io` and shared in):

- About 35 recordings from `2026-05-05` to `2026-07-31` (last recording in Drive is 2026-07-31). Start time almost always 19:56 to 20:03 IST; a few at 19:30 or 20:19. Roughly 3 to 5 weekdays per week (for example the week of 6 Jul has 8, 9, 10 Jul; the week of 20 Jul has 21, 22, 23, 24 Jul).
- Earlier transcripts exist for 2026-01-30 and 2026-02-03 (about 19:54 to 19:56 GMT+05:30).
- After 31 Jul only Gemini notes exist (6 Aug 22:00 IST, 7 Aug 18:30 IST, owned by Sai Kiran): a time shift.
- A `MOI Marketing Governance Call` (14 Apr, Tue, 20:29 IST titled "8:30 PM IST"; 27 Jul, Mon, 21:59 IST transcript; and the 7 Aug standup refers to "Monday... governance call").
- A calendar `Notes - Daily Standup` (18 Jun 2026) and `Notes - Ecosystem growth standup` (5 Jan 2026) docs also exist (auto-created calendar notes).

### Who does it

SaiKiran, Sujatha, Piyush, Ruta, Vardan (invited per the Gemini notes) and Adithya.

### Inputs needed before starting

Weekly numbers (see the MOI Socials `Metrics` sheet) and campaign status.

### Steps in order

1. Calendar invite from the marketing account creates the Meet and a `Notes - <title>` doc.
2. Meet runs ~23 minutes (transcription ended 22:55 and 23:32 on the two examples).
3. Gemini writes Summary, Decisions, Next steps (assigned by name) and Details; the notes doc lands in the owner's Drive and is shared.
4. Next steps are carried into the next day.

### Deliverables and where each ends up

Recording and Gemini notes in the marketing account; copies shared to Adithya (`sharedWithMeTime`).

### Accounts and tools

Google Calendar/Meet (marketing account), Gemini notes, shared sheets.

### Quality rules and house style (decisions that affect DevRel)

From the 6 and 7 Aug standups: weekly cadence AMA on Wednesday, AI/dev session on Thursday (Adithya's slot, with the host to coordinate "so the Thursday slot is utilized effectively"), game night on Friday; AMAs sometimes overran into game night; schedule the next AMA on Wed or Thu to avoid a clash; use video AMA clips only on YouTube; create a dummy LinkedIn employee account to repost into groups; keep a general (uncategorised) email approach until segments exist.

### Traps and things that failed silently

Gemini notes name people and projects imprecisely ("Scribble", "KL or PR", "LMS"); check before acting. Cross-platform metric disagreements (quote tweet views versus base tweet) were noted without resolution.

### How long it takes

About 23 minutes per standup.

### Open questions

Who runs the governance call now; whether a standup recording after 31 Jul exists outside this Drive.

## Process: MOI Forge campus cohort lifecycle

### Purpose

Move a college cohort from awareness to a 12-week builder programme: kickoff, hackathon, selection, incubation (MOI Programs: "MOI Forge - Basic" (campus roadshow, owner Sai Kiran) and "MOI Forge - Advance" (owner Adithya, start Dec 2025, KPIs: 1 project onboarded per month, 1,000 interactions per day, 1 demo day per month, 1 Builders newsletter per month, 1 video per project per week)).

### Trigger or cadence

Per college. Observed: first cohort run Oct to Nov 2025 (launch 20 Oct 2025, Day 2 concept workshop 28 Oct, Day 2.5 on 29 Oct, Intro to Coco 30 Oct, Day 4 JS MOI workshop 31 Oct, idea demo day 24 Nov, office hours 26 Nov; all recordings in `MOI Forge Recordings` `1lYu0aL-Yv1jI6b2hvhtni4z95fxmFa8g` or `Meet Recordings`). PCCOE: planning 23 Dec 2025, launch 14 Jan 2026, follow-up 22 Jan, onboarding 30 Jan, review 7 May 2026. Presidency College: kickoff 17 Mar 2026 (a large invite list; the notes say 30 participants were present), submission form created 16 Mar, deadline 31 Mar, review thereafter. Oxford and others are mentioned as upcoming on the kickoff call.

### Who does it

Adithya runs content and office hours; Sai Kiran organises campus logistics and the WhatsApp/Discord groups; Rahul co-presents technical concepts at onboarding.

### Inputs needed before starting

An MOU or agreement with the college (draft `Draft MOI-PCCOE - MOU.docx`, shared, 22 Dec 2025); a faculty contact; the onboarding guide; the hackathon brief and Forge hacks playbook (not found in Drive).

### Steps in order

1. Kickoff call with the whole cohort (Presidency, 28 minutes): blockchain basics, why participant-centric, resources (docs, Coco, JS SDK, GitHub), the three hackathon tracks (a DEX, a DAO, a bridge), submission requirements, timeline, and what the 12-week Forge offers (internship fast track).
2. Share the Discord (office hours), a WhatsApp group, the hackathon brief and examples right after the call (Sai posts the Discord link; Adi sends examples and brief).
3. Onboarding workshop for admitted cohorts (PCCOE, 30 Jan): wallet setup on the call, faucet claim, Voyage tour, asset playground, a simple Coco logic, deploy with the JS SDK, interact, a soulbound-asset demo that deliberately fails a transfer. Everyone fills the onboarding form during the call to be added to Discord groups.
4. Send the Forge Developer Onboarding Guide (12-week cohort doc): "First Things First" = fill the onboarding form, join Discord and Telegram; Step 1 familiarise (a four-video library of the first Forge sessions, documentation hub, papers); Step 2 Voyage (create wallet, claim faucet tokens, explore the network). The document is cut off at Step 2 in the text I read (the Drive text may be incomplete for this 371 KB doc).
5. Run daily Discord office hours during the two-week hackathon (promise on the kickoff call).
6. Collect submissions via the form (Team name, Project Link (github), Team members names; 9 responses between 31 Mar and 16 Apr 2026).
7. Select top teams for interview; top teams enter the 12-week Forge; run demo days and a weekly video per project (MOI Programs KPIs). Hero-app incubator pitch in the Sprint plan: 5 to 10 teams per batch, engineering residency, VC fast-track, co-marketing, 3 to 5 office-hour hours per week per cohort.

### Deliverables and where each ends up

Gemini notes and recordings (Meet Recordings), forms and response sheets (My Drive root), onboarding guide (My Drive root), MOU draft.

### Accounts and tools

Google Meet, Forms, Discord, WhatsApp, Telegram, Voyage, Notion (a "Notion Email" field in the `Boiler Blockchain` signup form suggests a Notion workspace, inferred), Luma.

### Quality rules and house style

- The kickoff states the submission contract as a GitHub link and a detailed README plus an optional two-minute demo video; the form only asks Team name, GitHub link, team members (a mismatch: the README is not enforced).
- Hardhat and Foundry will not work; use Coco and js-moi-sdk (and the Coco testing tool).
- Tracks are suggestions; combining or proposing is allowed as long as the participant-centric model is used.
- Hackathon winners are fast-tracked to interviews and the 12-week programme; hiring and internships are mentioned as outcomes.

### Traps and things that failed silently

- Submissions kept arriving after the stated 31 Mar deadline (rows up to 16 Apr), and one team appears twice with the same repository (case variants of the team name). Dedupe by repo link.
- The faucet amount quoted differs by source: 20K KMOI in the guide (13 Jan), 100K on the 30 Jan call, 100K on 24 Sep. Verify live.
- The Presidency responses sheet was created 2026-05-05, after the submissions were dated, so the destination was attached later (inferred).
- Free-text fields in the `Boiler Blockchain` signup form (6 responses, 15 to 18 Oct 2025; columns Name, Email, Github, Telegram, Discord Id, Notion Email; probably the first, Purdue-based cohort's signup, inferred from the name and the Presidency call's mention of a completed Purdue cohort) hold mixed formats (URL versus bare handle, and one phone number in the Telegram field).
- Gemini renders MOI Forge as "My Forge" and Sarva Labs as "Server Labs".

### How long it takes

Kickoff 28 minutes; PCCOE onboarding workshop about an hour (30 Jan notes); hackathon 2 weeks; Forge 12 weeks.

### Open questions

Where the hackathon brief, the Forge hacks playbook and the judging rubric live; what the PCCOE onboarding form asks; how interviews and selection were run; which cohort the "Oxford" Forge is.

## Process: Packaging an external technical submission for internal review (x402 and CASA)

### Purpose

Prepare public-repo contributions (a CASA namespace for MOI, an x402 payment scheme spec and its TypeScript mechanism) as reviewable documents so the whole content package clears an internal review before anything is filed upstream.

### Trigger or cadence

One-off in Sept 2026 but repeated three times in the same fortnight (see iterations); the process is meant to be reused for further upstream submissions ("PR4 other SDKs: recommended skip" shows the decision record).

### Who does it

Adithya (author named in the CASA files; "answers CASA's comments") and Rahul (internal reviewer). Process rule recorded in START HERE: "nothing is submitted upstream until Rahul reviews this package" (agreed 9 Sep).

### Inputs needed before starting

A verified live state (devnet RPC probes, upstream repos' contents and counts, SDK/npm versions); the on-disk review package (`x402-compat/review-package/PR-*`, one folder per PR mirroring the target repo's directory tree); the decision log (`DECISIONS.md`).

### Steps in order

Observed generations in Drive:

1. 9 Sep 12:20 to 12:27 UTC: a package of 12 small Google Docs uploaded within 7 minutes into `x402 — review package (MOI)` (`1YfCuNQYBmy83EJ_5UmAmKt5JBV13rJ-s`): `00 — START HERE — Review order and live-state check`, `PR1a` (PR description), `PR1b` (namespaces/moi/README), `PR1c` (caip2), `PR2a` (PR description), `PR2b` (the spec), `PR3` (mechanism, built), `PR4` (other SDKs, recommended skip), and background `BG1` (the plan), `BG2` (verified findings), `BG3` (per-PR requirements). The titles and file order match `x402-compat/review-package-gdocs/*.docx` on disk (conversion of docx to Google Docs on upload, inferred from the matching names).
2. 10 Sep 06:19 UTC: `zz-convert-test` (1.5 KB): a conversion test doc with bold, a table and bullets, created before the full re-upload. This is the only evidence of how the conversion was validated.
3. 10 Sep 16:01 to 16:06 UTC: consolidated review docs, one per PR, in `x402 — PR review docs (10 Sep 2026)` (`1zQRqGDBTzPahEPZ-BD5idr_p5m9Fl7JC`): `PR 1 — CASA namespace — review doc`, `PR 2 — x402 scheme spec — review doc`, `PR 3 — @x402/moi package — review doc part 1 of 4`. Parts 2 to 4 are not in Drive.
4. 10 Sep 16:07 to 16:15 UTC: a folder `x402` (`1QzBT2hefN3FyGMcbGBrlcd0DAvvPiNxx`) with `PR-1-CASA-namespace.docx`, `PR-2-x402-scheme-spec.docx`, `PR-3-x402-moi-package.docx` (the docx versions; PR 3 is a single 55 KB file instead of four parts). A third similarly named folder `x402 PR review docs` (`1LYoRzt8aQaUAB9OoYgTl8TYRuQyVcrkC`) is empty.
5. 14 Sep 17:02 UTC: a revised Google Doc `PR-1-CASA-namespace (14 Sep, participant-centric + governance)` in the `x402` folder; the PR-1 docx was modified 15 Sep.

Document anatomy:

- **START HERE**: one-paragraph definition ("Everything that goes to an external repository, one document per PR, in submission order... each PR folder mirrors the target repository's directory tree exactly"), the process rule, an order table (Order, Document, Target repo, State), the list of background docs, the dependency chain (1 to 2 to 3, "the order is enforced rather than preferred"), a dated **Live-state check** (RPC methods probed, upstream counts, versions), and a "What verification covered" paragraph naming the primary sources.
- **Per-PR review doc** (10 Sep): title "PR N: <what>", "Review document, <date>. Prepared for internal review before filing.", then `Page 1: what this PR is` (Target repository, PR title, Why it exists, High-level requirements table, Status bullets, Index), `1. PR description (as it will be posted)`, `2. File: <path>` with a bold `Context.` paragraph under every section of the file, then the exact file text. Open decisions copied from `DECISIONS.md`.
- **Background docs**: BG1 explains and plans (numbered steps 1 to 7); BG2 lists findings each with a "Checked:" line naming how it was verified (npm pack, live curl, GitHub API, a settled devnet transfer read back); BG3 lists per-PR requirements and "Applies to every PR".

### Deliverables and where each ends up

Review docs in Drive for the reviewer; the actual PR files stay on disk in the review package until filed upstream.

### Accounts and tools

Google Drive (upload), GitHub (read-only calls against `x402-foundation/x402` and `ChainAgnostic/namespaces`), npm, MOI devnet RPC (`curl`), docx generator (unknown tool).

### Quality rules and house style

- Every claim is checked against a primary source and the check is named.
- The CASA doc may reference only public artefacts ("A reviewer can open every link").
- Commits GPG-signed, conventional prefixes, subject 72 characters or less; AI assistance disclosed in each PR description; payment and signature logic personally reviewed (their contributing guide singles it out).
- Specs land first; mechanism after; a spec naming an unregistered namespace will not merge.
- Name the human who answers upstream comments in the author field and create and watch the `discussions-to` URL (CASA evidence: 91 of the last 100 closed PRs merged, median 24 days; the one real chain that failed was chased for 587 days and closed as stale).
- Terminology corrected on 14 Sep: PR 1a (9 Sep) says "account-centric protocol"; the 14 Sep revision says "participant-centric" and adds a Governance section (MOI Foundation governs the protocol; Sarva Labs is the implementation partner that builds the reference node and maintains the SDKs and operates the public networks, with a flagged "TBC: confirm the operator is Sarva Labs and not the MOI Foundation").

### Traps and things that failed silently

- **Stale copies after a change of reference format.** The 14 Sep PR 1 uses `moi:112`, a numeric network id, in a well-known networks table and test cases; the 10 Sep PR 2 and PR 3 review docs and the BG docs still use `moi:devnet` (and the PR 2 appendix still says "MOI is an account-centric protocol"). The 10 Sep PR 1 doc itself says MOI Wallet uses `moi:14` and that the namespace "must reconcile with the wallet before filing". When the reference format changes, grep every doc for the old strings.
- Four similarly named folders (`x402 — review package (MOI)`, `x402 — PR review docs (10 Sep 2026)`, `x402 PR review docs` (empty), `x402`). Use the most recent (`x402`, last viewed 14 Sep) as canonical (inferred); the others are earlier generations.
- Bold inside table cells may not convert. In `zz-convert-test` the header cells read `**A**` and `**B**` literally, and table header rows in START HERE, BG2 and the review docs show the same literal asterisks in the text the Drive tool returns (this could be a read-tool artifact). Open the rendered doc and look at a table header row before sending it to a reviewer.
- PR 3's review doc was split "part 1 of 4" but only part 1 was uploaded; the docx replaced it.
- The Drive docs are snapshots; the on-disk review package is newer (git status shows uncommitted edits to the same files). Do not treat Drive as current.
- Live facts age: devnet was reset ("previously created accounts, a MAS0 asset... no longer resolve"), the chain-id RPC was "not live yet" on 9 Sep, and the fee payer field is `fee_payer` (formerly `payer`) once moipod v0.13.0 is live.

### How long it takes

Document generation is minutes (seven-minute upload bursts). The review, per the plan, is gated on a human; the CASA merge median is 24 days.

### Open questions

Which Drive generation Rahul actually reviewed; whether the review happened; whether the final PRs have been filed (PR numbers are `TODO` in these docs).

## Process: SEO/GEO/AEO documentation sweep and the MOI Documentation Standard

### Purpose

Make every MOI web property citable by search and AI answer engines, and make that a definition of done for documentation work.

### Trigger or cadence

A one-off sweep (status doc dated 10 Sep 2026) turned into a standing standard (14 Sep). Status doc scope: docs.moi.technology, voyage-docs.moi.technology (Voyage docs), docs.wallet.moi.technology, cocolang.dev, js-moi-sdk docs, moi.technology, launchpad.moi.technology.

### Who does it

Adithya ("questions or proposed changes to this standard go to Adithya in #dev-chat"); Sai Kiran is preparing the Wikidata entry.

### Inputs needed before starting

An audit of each property scored before and after in the format SEO/GEO/AEO out of 10 (scores recorded: docs 3/4/3 to 8.5/9/8.5 so far; voyage docs 3/3/3 to 9/9/9; cocolang.dev 3/2/3 to 9/9.5/9; js-moi-sdk docs 3/4/3 to 9/9/9; moi.technology 5/4/3 to 7/6/5 so far).

### Steps in order

1. Audit each property (scores above).
2. Content: question-form H2s keeping existing anchors; answer-first opening paragraph (2 to 3 lines) so an engine can lift the answer; fix generic or broken site metadata (a docs site had "Welcome to Voyage Docs" as its title and its URL pointing at a dead host).
3. Metadata: hand-written description of 140 to 160 characters per page; fix canonical URLs; add Open Graph and Twitter cards; add JSON-LD (Organization, article, breadcrumb, FAQ, glossary) with one shared organisation id.
4. `llms.txt` and `llms-full.txt` generated at build time, plus a markdown variant of every page (append `.md`).
5. Agent discovery layer: `.well-known` catalogs.
6. `robots.txt`: allow every AI crawler explicitly, add Content-Signal directives, correct sitemap references.
7. Entity presence: Wikidata entry spec for MOI and Sarva Labs, then standardise org descriptions across Crunchbase, LinkedIn and GitHub.
8. Analytics: Bing Webmaster Tools (feeds ChatGPT search and Copilot) and Google Search Console.
9. One PR per property: status as of 10 Sep: js-moi-sdk docs PR #150, cocolang.dev PR #12, voyage explorer PR #447, voyage docs PR #5 up for review; moi docs mostly done; moi.technology almost done (the key to-do is making page content visible to non-JS crawlers); launchpad.moi.technology done locally. Re-score after the fixes.

### Deliverables and where each ends up

Branch PRs in the property repos; the status doc and the standard in My Drive root (two versions of the standard).

### Accounts and tools

GitHub, Cloudflare (crawler access), Bing Webmaster Tools, Google Search Console, `curl`.

### Quality rules and house style

The standard's rules (full text in the v2 doc `1dyecUYxkslB5wbbbYI7nAfGFcROY-gyLbRJzNCmzrKg`):
- Every content page: exactly one H1 (no manual H1 if the file has a top-of-body import such as a `<Tabs>` or schema component); title `Page Name | Site Name`, up to 60 characters, no version numbers; description hand-written, 140 to 160 characters, answer-shaped, quoted if it contains a colon; the first paragraph is the citable paragraph (answer first, no throat-clearing); entity names per the naming table; no placeholder text; stubs are `noindex` and out of the sitemap.
- Entity naming: MOI, MOI Wallet, Coco ("Coco (also known as Cocolang)" on first mention; never "CocoLang"), js-moi-sdk (always lowercase), Voyage, Sarva Labs. Tagline: "The participant layer for AI agents." The spelling in the JSON-LD must match the visible heading.
- PRs touching config, hosting or Cloudflare: production `url` correct, no template scaffolding (editUrl, sample posts, default favicon), and `curl -A "GPTBot/1.0" -I <url>` returns 200 (repeat for ChatGPT-User, OAI-SearchBot, ClaudeBot, Claude-User, Claude-SearchBot, PerplexityBot, Perplexity-User, Applebot-Extended; Google-Extended is robots.txt-only so read robots.txt instead).
- `llms.txt` is generated, never hand-edited (Docusaurus: `npm run build`; js-moi-sdk Sphinx: `make llms` from `docs/`).
- Docs reviewers: use the "PR Review Checklist for Docs Reviewers" and do not approve a PR that fails any item.
- Rewriting a heading as a question changes its slug; add an explicit anchor with the old slug (`## How do I create an account? {#account-creation}`).
- Do not write raw JSON-LD script tags in MDX; use the wrapper components on a single unbroken line.
- Count description length with `pbpaste | wc -m`.

### Traps and things that failed silently

- Two docs titled "MOI Documentation Standard" exist (v1 `1HEmf2p4-...`, 17 KB; v2 `1dyecUYxkslB5wbbbYI7nAfGFcROY-gyLbRJzNCmzrKg`, 23.7 KB, created about 40 minutes after v1's last edit). v2 is a superset with corrections: v1 "50-60 characters" or "under 60" for titles becomes "up to 60, no enforced minimum"; v1's ten rules are split into content-page rules and site-config rules; v2 adds MDX schema, noindex per framework, llms regeneration, Content-Signal placement, `Link` header discovery, an IndexNow key file, the Sphinx `html_baseurl` pitfall (turns canonicals into 308 redirect targets) and the MOI-Website SSG route list. The last view time is later on v1 (17 Sep), so v1 may still be the one people open (inferred). Treat v2 as canonical (inferred) and confirm.
- The most common failure named in the standard: a stub or sample page appearing in the sitemap unnoticed. Another: Cloudflare blocking AI crawlers (cocolang.dev scored 2 on GEO because Cloudflare 403-blocked AI crawlers).
- Common Crawl showed zero crawl coverage for cocolang and Voyage docs: not blocked but not linked.
- A client-rendered SPA is invisible to non-JS crawlers; head libraries do not fix that.

### How long it takes

Unknown per property; audit scores moved by 5 to 6 points on four properties.

### Open questions

Which version of the standard is canonical, whether the standard has been circulated to authors, and the final PR numbers for the moi docs and moi.technology.

## Process: Bounty content campaign tracking

### Purpose

Track content creators submitting articles and posts for a paid content bounty.

### Trigger or cadence

A campaign in Sept 2026 (sheet created 2026-09-08, modified 2026-09-09; shared in 9 Sep).

### Who does it

A teammate compiles; owner is a personal Gmail account (not recorded). Adithya has view access.

### Inputs needed before starting

A bounty brief naming the topic; submitters post publicly.

### Steps in order (as the sheet reveals)

1. Creators submit a link. The sheet is headed "217 submissions across 103 creators".
2. Rows hold Creator Name, Content Link, Platform (X, Medium, Paragraph, Substack).
3. The topic list is visible from titles: delegated authority for AI agents versus API keys, runtime scoping, x402 and payment authorisation, MOI versus other agent-identity projects, "know your agent".

### Deliverables and where each ends up

One shared sheet. Payout records are not in this sheet.

### Accounts and tools

X, Medium, Paragraph, Substack links; Google Sheets.

### Quality rules and house style

Not recorded in the sheet. The earlier Sprint plan (Jan 2026) records manual KMOI settlement and acceptance criteria for a bounty board (50,000 KMOI total, about 2,500 KMOI per accepted dApp).

### Traps and things that failed silently

- One creator appears on several rows (multiple submissions); a creator can submit the same piece on up to three platforms (Medium, Paragraph, Substack), so 217 submissions is not 217 distinct pieces.
- One creator name carries a "(probably)" annotation: names were typed by a person, not parsed.

### How long it takes

Unknown.

### Open questions

Who owns the bounty, how winners are scored, where payouts are recorded, whether this is the same bounty as the Sprint plan.

## Process: Programme design and weekly tracking (plans, KRAs, weekly metrics, content calendar)

### Purpose

Define each DevRel programme (Forge, Sprint, DevX hackathon, community updates), assign an owner, set metrics, and track them weekly.

### Trigger or cadence

Programmes defined Dec 2025 to Mar 2026; weekly metrics from week 5 (26 Jan 2026) to week 15 (6 Apr 2026) in MOI Programs; the MOI Socials Metrics tab runs weekly from 29 Dec 2025 and is filled through the week of 28 Sep 2026.

### Who does it

Each programme has an owner in the sheet (Adithya owns MOI Forge - Advance, MOI Community Updates, MOI DevX monthly hackathon, MOI Sprint; Sai Kiran owns Forge - Basic and Moinkee; Vardan owns the podcast; Rahul owns Tech Spotlight; Harsh owns Galxe; Vardan and Louis own KOL outreach). The Metrics tab in MOI Socials is updated by the social team.

### Inputs needed before starting

An objective, description, outcome, metrics, dates, resources and budget per programme.

### Steps in order

1. Write the programme plan: executive summary, mechanism, user journey or operations, requirements, resources, KPIs (Sprint plan: two-tier "liveness" rewards: 100 KMOI for a verified deployment, 1,000 KMOI for 500 interactions and 10 unique wallets within 30 days; Bounty Board: wanted reference apps listed on DoraHacks, Superteam Earn and Gitcoin with manual settlement; Forge: "Hero App" incubator). Earlier template (Jul 2025): `DevRel Planning Document Template` with sections Executive Summary, Goals and Objectives, Initiative 1 hackathon sponsorships (target events, sponsorship details, outcomes), Initiative 2 university grant programme ($3,000 per recipient group, $1,000 on approval and $2,000 on deliverables, mentor, output requirements), Resources and Budget, Metrics.
2. Put the programme into MOI Programs (columns Program Name, Category, Owner, Objective, Description, Outcome, Metrics, Start Date, End Date, Resources Required, Estimated Budget, Comments).
3. Add weekly rows in the WEEKLY METRICS tab (per programme: Content Production, Audience Growth, Engagement; Forge Basic: colleges executed, wallets created, Discord joins, forms submitted, X impressions; Forge Advanced: projects onboarded, pipeline).
4. Schedule content in the CONTENT CALENDAR tab (day-of-week, date, content theme, assets, content review, asset review, then LinkedIn, X, Instagram, Telegram, Discord, Other columns). Week 13 themes by weekday: App-centric problem, Internet evolution, Missing WHO dimension, AI agents, AK's Insight, Builders Proof, Meme / Community.
5. A parallel plan lives in MOI Socials: weekly themes for Moinkee and MOI (weeks 3 to 12), planned versus actual post counts, an intern Resource Plan, and a `Metrics` tab (X impressions and engagement, LinkedIn impressions, visitors, clicks, reactions; a `Sheet2` stub of developer-funnel labels: Downloaded SDK/CLI, # of Technical Queries, Made First API Call, Deployed to Testnet, GitHub Activity).

### Deliverables and where each ends up

MOI Programs and MOI Socials (shared with Adithya), the Sprint plan and KRAs (Adithya's Drive).

### Accounts and tools

Google Sheets/Docs.

### Quality rules and house style

Program plans are measured by outcomes tied to network usage, not completion: the Sprint plan says standard education platforms "result in high deployment numbers but low network utilization", so rewards depend on verified activity. KRAs frame each programme with weekly KPIs plus 90-day outcome goals.

### Traps and things that failed silently

- The weekly metrics are mostly blank beyond week 9 (many cells "-"), and the content calendar from week 14 on only carries "Link" placeholders. The structures exist; the data does not.
- KRAs and MOI Programs agree on volume (2 events per month: KRAs "2 per month" for calls plus AMAs, MOI Programs 1 call plus 1 X AMA); the Marketing Events Calendar plans far more (39 events including 20 game nights), so check which calendar a number comes from.
- The Marketing Questionnaire records ownership: Adithya wants to own MOI Forge, MOI Sprint (eventually a gamified site), Awesome MOI, the Academia collab and general DevRel (docs, Discord).

### How long it takes

Unknown.

### Open questions

Which programmes are still active (Sprint, DevX hackathon), who now fills the weekly metrics, and whether the weekly metrics moved elsewhere after April.

## Process: Meeting capture (Meet recording, Gemini notes, calendar notes doc)

### Purpose

Every call leaves the same trio of artifacts without manual work. This is how most Drive traces above come into existence.

### Trigger or cadence

Every Google Calendar event with a Meet.

### Who does it

Automatic; the organiser's account decides where files land.

### Steps in order

1. Calendar event creation produces a `Notes - <event title>` Google Doc in My Drive root (about 2.5 KB; e.g. `Notes - MOI Forge Day 4- JS MOI Workshop`, `Notes - Daily Standup`).
2. When the meeting records, the recording (mp4), a `Notes by Gemini` doc (summary, decisions, next steps, details, full transcript) and a `Chat` text file are saved. For calls Adithya organises they go to `Meet Recordings` (`1jn9ybwa_b6SF5XvKsxVDUDWCtXgO6VGj`) under `Google Meet`; for calls organised by `info@moi.technology` or `marketing@moinetwork.io` they stay in that account and are shared in.
3. Spontaneous Meets create a dated folder (e.g. `wfh-dhtd-sbi - 2026/09/24 13:53 EDT`) holding recording and notes.

### Deliverables and where each ends up

As above.

### Accounts and tools

Google Meet, Gemini notes (needs the Workspace feature on).

### Quality rules and house style

Gemini notes ask the user to review them; treat as drafts.

### Traps and things that failed silently

- Gemini notes can capture secrets read aloud. The 24 Sep notes include the wallet seed-phrase confirmation words requested on a screen share (values not recorded here). Never read, display or confirm a seed phrase on a recorded call.
- Large transcripts (Docs 340 KB) are easy to paste into other tools; prefer the Summary and Decisions blocks.
- Names are misrecognised ("Moy", "Grock"); numbers may be wrong.

### How long it takes

Automatic. The notes appear within about 5 to 90 minutes of the call (observed spread).

### Open questions

Whether `Meet Recordings` and `Google Meet` folders are meant to be treated as archives.

## Reusable assets

Drive ids given so a skill can point at them. "Template (inferred)" means no file says it is a template.

| Asset | Type | Drive id | Notes |
|---|---|---|---|
| DevRel Planning Document Template | Doc, explicit template | `1Wuji90KkFXRfOUu3Dbi9gRnFNdxAi_0YGBmBFeWSSl0` | Hackathon sponsorship plus university grant plan; sections and budget lines |
| MOI Documentation Standard v2 | Doc, rulebook plus checklists | `1dyecUYxkslB5wbbbYI7nAfGFcROY-gyLbRJzNCmzrKg` | Canonical (inferred); v1 `1HEmf2p4-V3vuoLHMJlChfEIvTmTzSKISlWVmVKuAn8Q` |
| MOI SEOGEOAEO Sweep Status | Doc, status format | `1ecNM7E9vYd5BgZmKQcLxncMYMg9_RStdtsUdc2N7fkM` | Per-change rationale, scores, per-property status |
| MOI_Builders_S7Deck.pptx | Deck with speaker script | `1NqODoRaFl_jwFy-Suf3rtTzvk2_k4sJw` | The best exemplar of a Builders session script; folder `Webinar 7` `15XuMwgDXdqsKvx_OdL0G0cWs6f1OeoYC` |
| MOI Builders II - Native Assets (form) | Form, template (inferred) | `1ky7Y4WeNz56fSfxpM-pXqdDOh2GxwhAsLs-Z3XOmSi8` | Likely copy source for later forms; questions unreadable via tool |
| MOI Builders III - Agents on MOI / IV - Swaps / VII - Agentic Payments (forms) | Forms | `1MdAlR_k7ji42PLs_LPjCihj47DAjygVBCTdQfyA5Yac` / `1lpr8391uQq5z7utaMz9TjTRo8jhPCSwQpAlMdx_rbHg` / `1Gh0m7h0M9Rg-Ruv0g6SF2iNUMw2hh34farVTmJLozTU` | |
| MOI Builders II (Responses) | Sheet | `1cF9MBVlni614U53XowpAw9q3IwAgY11vzliIRS6RF88` | Header layout: Timestamp, Email, Wallet Address, asset id columns or Transaction Hash |
| MOI Forge PCCOE Onboarding (form) | Form | `1r1YgBWpcuX6Fe_P78VQvYpaDGsRi1ZR1zAh_rDAObs8` | Questions unknown; used to add people to Discord |
| Presidency College MOI Forge submission (form) and (Responses) | Form, sheet | `14Kj5YyPJdluj4n_kRxmQ4QIKlofwdLelf0231aEemp8`, `1beRta2H-sey-5OA8U2L84AtXOHKkbyMbReAyVmydD90` | Three fields: Team name, Project Link (github), Team members names |
| Boiler Blockchain (form) and (Responses) | Form, sheet | `1t350WxOq6nF2LXgnqXdwQJXCskvKOB5xD5we2Z77lOg`, `1-kH1kt7fJtTnwNOlYRLf7I-6Wv2jtQ9OKJRcCR9Ez7g` | Cohort signup fields: Name, Email, Github, Telegram, Discord Id, Notion Email |
| MOI Forge Developer Onboarding Guide | Doc | `10gIG8cbwH9BdI7OEHC36xWn4HkvYax1SyE-ncaH-oTU` | Cohort onboarding doc structure; remove the personal phone number before reuse |
| x402 START HERE, BG1-3, PR1a/b/c, PR2a/b, PR3, PR4 | Docs | `1PGapkKTBHMMpDi4RRC_QcdogSpkJ9_DjMmsMarJx4as`, `1JvCrWC8W7lQfieiljA4t-6OBfjQzoockc_Kvc0OcsCI`, `1RIjVDeU1BguVqf612xHx7buaM4flO2TqYYDaFnxs6aE`, `1izgDTw8RFPYSDS7gLYsiMEdgGM2ovZGzl3fh6F8UlZ0`, `14MC6e5GJ5iXtfyODnCO7M1pZYgGlSIKitTlPRq5emzQ`, `1onMZCoxav9ZYzW-LLGFY8f1qmUoVdvtjvL4GSAdd1iE`, `15efZ3J9PU_eXPd1tStvMOCOiR6kUzB-5cSSnZnXvjuw`, `1rxnhTFRQMHC60hJr_LHPsD_lXZLy1OzWWK-kJNC6Ucc`, `1SaIurIbT6-esNIy1v3Q7ZVSYT9b4CTR0HP9Bpo5NLow`, `1CQs4CfWFbXk992x9KCCcwH2j2dkMctdMUsZoIYtBm38`, `166dyjDtqI8E1bpGC0mO1uY91YNBMVeMzy2ZZYoFNIDQ` | The 9 Sep package; folder `1YfCuNQYBmy83EJ_5UmAmKt5JBV13rJ-s` |
| x402 PR review docs (10 Sep) | Docs, exemplar of the review-doc format | PR 1 `1kRfX07pdVEw3rhz9huNgOUtt6_s-XcC3MA28bjJAUDQ`, PR 2 `1dHzFs4FMM_Odkx0Zc-kVqRqfsm2nd6cYjc5dGIMW2QY` (best exemplar), PR 3 part 1 `1UqMZvBMumKypM2lb4Cfxf9Nmk97DJ9yZjGsrwO7Bv4Y` | Folder `1zQRqGDBTzPahEPZ-BD5idr_p5m9Fl7JC` |
| x402 folder docx set and 14 Sep CASA revision | docx, doc | `19xecidyf5QpTnyYE8Koiavd9AdYimw3m`, `1OCWYF4r_w-rJY5vdZU3PiMu1qMo8emJA`, `11W90NyMopoAT8_WurW0o-Vm3weqjLQtH`, `18_L_ffYPAk_d-Ms8NXlt3MxAKOcliuxGohjd9vetjeI` | Folder `1QzBT2hefN3FyGMcbGBrlcd0DAvvPiNxx` |
| zz-convert-test | Test doc | `1RecMEH8lNtp8KJJto9pYJ033HGhk56_RczheqIIjLmg` | Shows what a docx-to-Doc conversion must preserve (bold, table, bullets) |
| Adithya KRAs | Doc | `16fDyfr4o84N4OWYmXWQW1qn7lm45Cj0hbbzPg-rPMNI` | Source of the 48h/24h/48h call timings |
| MOI Sprint: Strategic Launch Plan | Doc, three proposals | `1HA-vUP8NhDj5lBEFlFFcX2CcQULdcYvWqKmleDOfP58` | Sprint two-tier rewards, Bounty Board, Forge Hero App |
| MOI Programs | Sheet | `1q9rsWhWqMdCDO0XdI1i46ap22n4UkkSRFH6Bb2U-hlk` | PROGRAMS, WEEKLY METRICS, CONTENT CALENDAR tabs |
| MOI Socials | Sheet | `19f5gOIlU5ksusXxCdPr-kCD7F-_Kyrv_AJ87FgO3UoY` | Weekly themes, resource plan, weekly Metrics (filled to week 40) |
| Community Call + AMA Calender 2026 | Sheet | `1iNsT9pHoSnA8eysz2-Iq9y3iSBwNk_anPpkeFwC2U6Q` | 12-row monthly planner; copy for 2027 |
| Marketing Events Calendar | Sheet | `1DKzB60lXAA43nMAiJQtBORoDjeljcL6nNxlGzB4sp_c` | Event table plus yearly view and monthly grids |
| Community call (agenda/slides), Community Call - Agentic Economy Boom, Community call script | Docs | `1wJT7kjxgjj18YKWZmWFmY-avw_1Ga3ceI5zFXAbakFU`, `1jj0NUPRndgBlTEY7RdPyEhAI7gOoP-neUH5ZJIW3_d4`, `1J1-UiQyUzK-Xdm2hu0OeWOLxARCkJdktuKIkRo1qMOE` | Agenda per speaker; dev-update 3-slide template; spoken script |
| Builders III Gemini notes | Doc | `1wvf3_lc4FPVPogceqjpAsZdMXSYoSkhvjV0okLcQMNc` | Full transcript of a complete Builders session, the best reference for the talk track |
| Forge kickoff notes (Presidency) | Doc | `1ACG9DDKZbXx52vaSX7zW8-dvbkQ5zr_yTKco1S_5vPc` | Kickoff talk track, hackathon contract, timeline |
| Forge onboarding workshop notes (PCCOE) | Doc | `1A2L22Xl48duYnmHmlwWybP2sCKbd1UIQWx2rSI_WZ5k` | Hands-on onboarding sequence |
| Marketing Standup notes 6 and 7 Aug 2026 | Docs | `1sEX8h1T9eXagK7_pIaR2WfkCfWTRNknaCupVMWejZHM`, `1GMNrbH-zOw1NcedEtdTqyE44l9T6h1G1YIOuO6tMXjE` | Decision and next-step format |
| Points progam issues | Doc | `1lChj6-Z25hUwY3WHlDZbHAxfGMbqR02v9T9C0yZJ_a0` | Audit findings of the rewards app, grouped by area with `[CRITICAL]` to `[INFO]` tags and `file:line` anchors; format exemplar for audit write-ups; belongs to the rewards-app audit, not covered here |

## Rules and house style

Pulled from Drive evidence only; each line names its source.

- Entity names: MOI, MOI Wallet, Coco (first mention "Coco (also known as Cocolang)"), js-moi-sdk (lowercase), Voyage, Sarva Labs; tagline "The participant layer for AI agents." (Documentation Standard).
- Say participant-centric, not account-centric. The 9 Sep CASA description said "account-centric"; the 14 Sep rewrite fixed it and described the ledger as a graph of tesseracts, not a chain of blocks, with "no per-account chain and no single global chain" (CASA PR 1 revision). The 10 Sep PR 2 appendix still has the old wording.
- Governance wording: the MOI Foundation governs the protocol; Sarva Labs designs and develops, builds the reference implementation and maintains the SDKs, and (flagged TBC) operates the public networks (14 Sep CASA doc).
- Docs: one H1, hand-written 140 to 160 character description, answer-first first paragraph, question-phrased H2s where they answer a question, anchors preserved, stubs `noindex` (Documentation Standard v2).
- Titles: `Page Name | Site Name`, up to 60 characters, no version numbers; no enforced minimum (v2 correction of v1).
- `llms.txt` generated, never hand-edited; verify crawler access with `curl -A "<UA>/1.0" -I <url>` after every Cloudflare or hosting change.
- Builders sessions: concepts on screen, not code; run the command first and then talk; admit what is fake; close with the next session's question; prepare likely-hard-question answers (S7 deck).
- Run-of-show and speaker briefing 48 hours before; notes, recording, resources, actions within 24 hours; Q&A and follow-ups within 48 hours with owners (KRAs).
- Internal review gate before any upstream filing (START HERE).
- Primary-source verification for every claim in a package, with the check named (BG2).
- PR hygiene for upstream repos: GPG-signed commits, conventional prefixes, subject 72 characters or fewer, disclose AI assistance in the PR description, personally review payment and signature logic (BG3).
- YouTube: video AMA clips only (7 Aug standup).
- Weekly slots: Wednesday AMA, Thursday AI/developer session, Friday game night (6 Aug standup).
- Rewards should depend on verified on-chain activity, not completion (Sprint plan).
- Do not state the faucet amount without checking it live (20K versus 100K appear in different Drive docs).

## Traps

1. **Form contents are invisible to the Drive read tool.** Do not assume the questions; read the response sheet headers or open the form.
2. **Builders forms are completion-proof forms, not registration or feedback forms.** No feedback form exists in Drive. Registration is on Luma (inferred).
3. **Only session II has a response sheet.** Do not look for III, IV, VII sheets in Drive; check the form's Responses tab in the browser.
4. **Gemini mis-hears names and amounts** ("Moy" for MOI, "KOI" for KMOI, "Grock" for Groq, "Server Labs", "My Forge"). Never copy values from Gemini notes without verification.
5. **Seed phrases leak into Gemini transcripts** when a wallet setup is screen-shared (24 Sep notes). Do not read or confirm seed words on a recorded call; if it happens, delete the notes doc and recording.
6. **Two copies of the Documentation Standard** with different rules (title length). Use v2 and retire v1.
7. **Stale x402 docs after a reference change** (`moi:devnet` versus `moi:112`; "account-centric" wording). Grep all docs when a decision changes; Drive is behind disk.
8. **Duplicate folder names for x402 packages.** One is empty.
9. **Dates in scripts age.** The Sep 2025 script promised go-moi v0.12.0 on public devnet by end of September; on 9 Sep 2026 devnet still reported 0.12.0. The devnet reset also wiped earlier demo state (BG2 finding 10): demos must be rebuilt after a reset.
10. **Live demo failure modes:** wrong working directory, script that does not load the list, interrupted tamper runs leaving the registry dirty, a mnemonic with no funds. Pre-flight the demo and keep the fallback clips.
11. **Presidency submissions:** duplicates and post-deadline rows; README not enforced by the form.
12. **Calendar sheets are mostly empty** (topic, guest, speaker). A reserved date is not a confirmed event.
13. **Video files and editor-owned folders:** the Builders VII edit sits in an editor-owned folder under a Launchpad folder, with a typo in its name.
14. **Drive doc truncation:** very large docs (the Forge guide, 371 KB) may come back truncated through the API; verify in the browser before treating a doc as complete.
15. **The sharedWithMe filter works but `owner = 'me'` hides shared copies:** most standup, call and Forge-notes artifacts are owned by other accounts (`info@moi.technology`, `marketing@moinetwork.io`, Sai Kiran), so searching only `owner = 'me'` misses them.

## Open questions

1. What questions do the Builders II, III, IV and VII forms ask, and is there a master or blank form? (Needs the form editor.)
2. Where do registration (Luma export, attendee lists) and any post-webinar feedback live? None in Drive.
3. Where are the Builders I, V and VI materials, and the IV to VII recordings, Gemini notes and decks?
4. Where do III, IV and VII form responses go?
5. Which version of the MOI Documentation Standard is canonical (v1 or v2)?
6. Where are PR 3 review doc parts 2 to 4, and what exactly did Rahul review?
7. Who runs the community calls and AMAs now, and where are run-of-show and speaker brief docs (required by the KRAs)?
8. Where are the Forge hackathon brief, hacks playbook and judging rubric? What does the PCCOE onboarding form ask?
9. Contents of `Vid1.mov`/`Vid2.mov` in `Webinar 7`, MOI Annual Calendar (355 KB), Cocolang docs feedback (1.5 MB), the Campus Road Show doc, the Forge planning and demo-day notes (not opened).
10. What is `List of dependencies` (empty, created 2026-09-30) for?
11. Who is the video editor's contact and what is the brief format?
12. Who pays and records bounties for the Builders challenges and the content bounty?
13. Is the 24 Sep Launchpad onboarding walkthrough a one-off or a repeated "onboard an ambassador to Agent Launchpad" process? (One occurrence in Drive.)
14. Which model and key powers the Session 7 demo's pricing and judgment step?
15. What is the status of the Sprint two-tier reward scheme, the Bounty Board and the Forge Hero App proposals (proposals dated Jan 2026; no evidence of launch)?

## What a skill for this should contain

Split by process rather than one monolith, with a shared `references/drive-map.md` that lists the ids above.

### Skill 1: moi-builders-session

`SKILL.md` outline: when to use; the series arc and numbering (II Native Assets, III Agents on MOI, IV Swaps, VII Agentic Payments; teasers 08 and 09); the session timeline (T-4 days form, T-1 deck export, day-of verify and go); the run-of-show scaffold; the post-session checklist (recap message, form on Luma, repo instructions, verify submissions, send recording to the editor); the Gemini caveats; escalation to Adithya for bounty amounts.

References to bundle: `session-script-conventions.md` (the S7 bracket conventions with a worked slide), `demo-preflight.md` (wrong directory, dirty registry, funded wallet, fallback clips, Voyage explorer open), `likely-questions.md` pattern, `form-spec.md` (proof fields observed: wallet plus asset ids, wallet plus tx hash, agent id plus owner wallet).

Scripts worth writing: `verify_submissions.py` (read a responses sheet as CSV, check each wallet, asset id, tx hash or agent id on the Voyage RPC, emit pass/fail without exporting personal data); `new_session_scaffold.sh` (create `session-N/` with deck, repo README, form-spec); a docx or pptx script-from-HTML exporter if the deck is authored as HTML.

Templates: deck skeleton with `[ DECK · slide N ]` notes and `LIKELY QUESTIONS`; form question list; recap message with repo and bounty links.

### Skill 2: moi-forge-cohort

Outline: stages (kickoff, onboarding workshop, two-week hackathon with daily office hours, submissions, selection, 12-week Forge, demo days); inputs (MOU, faculty contact); each stage's artifact.

References: `forge-onboarding-guide-structure.md` (First Things First, Step 1, Step 2), `kickoff-talk-track.md` (from the Presidency kickoff), `hackathon-contract.md` (repo plus README plus optional two-minute video, tracks DEX, DAO, bridge, no Hardhat or Foundry), `forms.md` (the three-field submission form and the cohort signup fields), `kpis.md` (from MOI Programs).

Scripts: `dedupe_submissions.py` (dedupe by repo URL, flag post-deadline); a faucet and wallet pre-check script.

### Skill 3: moi-upstream-submission-review-package

Outline: the three-layer package (START HERE, per-PR review doc, background docs), the document anatomy, the review gate, live-state check, conversion and upload to Drive, revision hygiene.

References: `review-doc-template.md` (Page 1 block, PR description, per-section Context notes), `live-state-check.md` (what to probe and how to date it), `bg-findings-format.md` (claim plus "Checked:" line), `pr-hygiene.md` (GPG, prefixes, AI disclosure, human review of payment code).

Scripts: `stale_term_scan.sh` (grep the package for strings that a decision made obsolete, for example `moi:devnet`, `account-centric`, `payer`); `build_gdocs.sh` (md to docx with tables and bullets preserved, mirroring `zz-convert-test`); `check_links_public.py` (only public links in CASA docs).

### Skill 4: moi-docs-geo-standard

Outline: apply the Documentation Standard v2 to a page, to a site and in a PR review; run the verification commands; produce a sweep status doc.

References: the standard's tables as `entity-naming.md`, `metadata-rules.md`, `new-page-checklist.md`, `new-site-checklist.md`, `pr-review-checklist.md`, `framework-matrix.md` (Docusaurus, Sphinx, SPA), plus `sweep-status-template.md` (sections: Content changes, Frontmatter/metadata, llms.txt, Agent discovery, robots.txt, Entity presence, Analytics, Audit scores, Status per property).

Scripts: `check_page.py` (one H1, title format and length, description length 140-160, colon quoting, entity spellings), `crawler_access.sh` (the curl loop over the UAs plus a robots.txt read for Google-Extended), `sitemap_stub_check.py`, `llms_regen_reminder.sh` (Docusaurus build or `make llms`).

### Skill 5: moi-community-call

Outline: calendar, agenda, speakers, dev update, post-call; honour the 48h/24h/48h timings; fix the calendar blanks.

References: `agenda-template.md` (one block per speaker), `dev-update-3-slides.md`, `fireside-3-questions.md`, `calendar-columns.md`, `weekly-slots.md` (Wed AMA, Thu dev session, Fri game night), `video-ama-rule.md`.

Scripts: `call_checklist.py` (date math for T-48h and T+24h and T+48h), `fill_calendar_row.py`.

### Skill 6 (reference only): moi-marketing-cadence

A read-only reference: standup cadence, governance call, who owns what in MOI Programs, the weekly metrics structure, and how to read Gemini notes. No automation.

### Shared bundle

`drive-map.md` listing every id in "Reusable assets"; `gemini-notes-caveats.md`; `no-secrets-on-calls.md` (seed phrases, `.env`); and a short `drive-search-recipes.md` (use `owner = 'me'` plus `sharedWithMe = true`, search forms with `mimeType = application/vnd.google-apps.form`, response sheets with `title contains 'Responses'`, remember that forms are unreadable and need the browser).
