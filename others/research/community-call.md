# Community Call ("The Campfire Chat") and the Builders intro session

> **What this file is.** A research note on how the monthly MOI Community Call (called "The Campfire Chat" from call 14 on) and the one-off Builders intro session were planned, built, scripted and checked. The evidence is community calls 13 and 14 (CC13, CC14) and the intro session. Claude (an AI research assistant) compiled it from Adithya's work history to design Claude skills for the MOI DevRel handover. The last section ("Proposals for skills") proposes `moi-community-call`, a small `moi-builders-intro`, and fixes to the existing `moi-deck` skill. This file does not say whether those proposals were built.
>
> **When it was written.** Late September to October 2026. The evidence runs from 24 August to 1 October 2026. Words such as "now", "still" and "today" mean at the time of writing, unless a line says "Update" with a date.
>
> **Who "I" and "the user" are.** "I" is the research assistant. "The user" is Adithya (DevRel at MOI); "the request file" means the request log `REQ`.
>
> **Evidence key.** "Observed" means seen in a file, a transcript or a request line. "(inferred)" means the research assistant's reading, not something a file or a request says. "Unknown" means the evidence is silent; those items are repeated under "Open questions".
>
> **Paths and citations.**
> - `REQ <n>` or `REQ:<n>` cites line n of a request log kept on Adithya's Mac (`~/moi-devrel-skills/_research/_user-requests.txt`; not in this repo). "REQ ~n", "REQ near n" and "REQ about n" mean the exact line is approximate.
> - `WT` is Adithya's working copy of the webinar repo on his Mac: `~/MOI-Webinars/.claude/worktrees/relaxed-mccarthy-368dbc`.
> - `TX13`, `TX13b` and `TX14` are saved Claude Code session transcripts on Adithya's Mac (full paths in the appendix at the end). "TX14 line n" is a line of that file; times are UTC. They are not in the repo.
> - A "memory note" is a note in Claude's own memory folder on Adithya's Mac (under `~/.claude/projects/.../memory/`), not a file in this repo.
> - Paths starting `~/` or `WT/` are on Adithya's Mac. The session code is in https://github.com/moi-foundation/MOI-Webinars. Session transcripts are not in the repo.
> - Where the original text had an em dash inside a quoted title or UI string, it is shown here with a colon.
>
> **People.**
> - Adithya: DevRel at MOI; builds the deck and presents the protocol and DevRel slides.
> - Rahul: reviews and approves DevRel work and sets priorities. The notes call him "the manager" (inferred from REQ 2164).
> - Prateek, Rishal, Piyush, Sai Kiran: speakers or content owners; roles not recorded in these notes (see "Who does it").
> - The host of the call: not named in these notes.
> - "The founder": the label these notes use for whoever gave the 14 Sep terminology corrections. That label is the research assistant's inference; the person is not named.
> - Not named here but relevant: Vardan (marketing, community call scheduling).
>
> **Reading guide.** One "Process" section per stage (planning, content sourcing, deck build, script, release checks, live and after the call, intro session), then reusable assets, rules, traps, open questions, proposals for skills, known inconsistencies, a glossary of jargon, and an appendix with the transcript paths.
>
> **Update, 13 October 2026.** The CC14 deck (`community-call-14/deck/`) has been merged into https://github.com/moi-foundation/MOI-Webinars. Statements below that it is "untracked" or exists "only on this Mac" were true when written and are now out of date for that deck.

## Sources read

Assigned reading, all read in full:

- `WT/community-call-14/SCRIPT.md` (37 lines, slides 2 to 4 only)
- `WT/community-call-14/deck/README.md`
- `WT/community-call-14/deck/index.html` (478 lines: CSS, 12 slides, `TITLES` at lines 368-381, `NOTES` at 382-395, presenter window at 398-436)
- `WT/community-call-14/deck/index-no-guest.html` (byte-identical to `index.html`, checked with `diff`)
- `WT/community-call-14/deck/MOI_Community_Call_14.pdf` and `MOI_Community_Call_14_no_guest.pdf` (read by name, plus `pdfinfo`, `pdftotext` and a rendered contact sheet to check them; both 12 pages, identical text)
- `WT/community-call-14/deck/assets/` (listed: `futuremode-1.png`, `futuremode-2.png`, `mohit.webp`, `krexa-logo.webp`, `engines/{chatgpt,copilot,gemini,perplexity}.svg`)
- `WT/intro-session/deck/index.html` (476 lines, `TITLES` at 360-372, `NOTES` at 373-393), `README.md`, `MOI_Builders_Intro.pdf` (11 pages, by name and `pdfinfo`)
- `~/.claude/skills/moi-deck/` in full: `SKILL.md`, `reference/build.md`, `reference/components.md`, `scripts/new-deck.sh`, `scripts/render.sh`, `assets/template.html`
- `REQ`: every hit for the suggested grep, plus the surrounding lines (1325-1380 for the intro deck and CC14, 2250-2280 for CC13, 924-1100 for the deck/script voice feedback, 524-660 for the earliest script-tone feedback)

Extra evidence I went and found, because the request log is only the user's typed text (it truncates long pastes and omits images and attachments):

- `TX14` lines 24686 (the pasted first-draft deck), 24851 (the pasted Scribble report and Slack thread), 25251 (the pasted announcement), and the assistant replies from 22804 to 26254 (intro build, CC14 edits, script rounds, skill packaging).
- `TX13` lines 6702 (Zoom transcript of the 24 Aug planning call), 9567 (27 Aug call notes), 10119/10166 (CC13 YouTube description), 10207 (CC13 slide scripts), and the CC13 deck-verification replies (TX13 lines 9598-9868; TX13b lines 1897-2032).
- Memory notes: `~/.claude/projects/-Users-...-mw-MOI-Website/memory/moi-weekly-comms-cadence.md`, `.../-Users-...-MOI-Webinars/memory/devnet-build-lag.md`, `moi-terminology-corrections.md`, `no-push-no-notify.md`.
- Repo files used as content sources for the protocol slides: `WT/protocol-release-0.13.0/RELEASE-NOTE.md`, `BLOG.md`, `social/discord.txt`, `social/x-correction-reply.txt`.
- For comparison: `WT/session-8-policies/SCRIPT.md` and `LUMA.md` (the dev-webinar sibling), `WT/DEPENDENCIES.md` section 4 and 19.
- I ran three read-only checks: a JavaScript parse of each deck's inline script, a headless-Chrome DOM dump of the CC14 deck, and a 1280x720 headless screenshot of slides 9 and 11. Scratch images went to the session scratchpad only.

No `.env` file was opened. No secret value appears in this note.

---

## Process: Plan the monthly Community Call and line up speakers

### Purpose

Run one public call a month that shows what shipped, what DevRel, product and marketing did, and who the community
is meeting. Adithya's job is the deck and the speaker line-up (TX13 line 6702; memory note `moi-weekly-comms-cadence.md`).

### Trigger or cadence

- Observed: the call is monthly. The CC13 script opens "This is our monthly look at what actually shipped" (TX13 line 10207, written by Claude and not
  contradicted by the user). CC13 was Thursday 27 Aug 2026 (TX13 line 9567: "the community call scheduled for today"). CC14's deck chip says
  "September 2026".
- Observed: memory note says rehearsal on Wednesday and live call on Thursday, "as set on the 2026-08-24 planning call".
- Observed: on 24 Sep 14:02 UTC the user pasted announcement copy that begins "MOI Community Call #14 is happening tomorrow" (TX14 line 25251). So the call was on
  Friday 25 Sep (inferred). Script edits were still happening at 25 Sep 12:37 UTC, which fits a call later that day or later (inferred).
- Unknown: the start time and length of either call. CC13 started about 6 hours after 04:47 UTC on 27 Aug ("communtiy call is in 6 hrs", REQ near 2251, exact line not recorded; TX13 line 9567),
  which is about 16:15 IST (inferred; the dev webinars run at 4pm IST, `WT/session-8-policies/SCRIPT.md` line 3).

### Who does it

- Adithya: builds the deck, confirms speakers, presents protocol and DevRel updates. On 24 Aug the transcript says "I'll do Devrel updates" and "do protocol updates" (TX13 line 6702; the speaker of "do protocol updates" is not labelled). For CC14 he only asked for a script for slides 2 to 4 (September release, upgrading from August, DevRel), the protocol and DevRel slides (REQ 1371, 1374), so those are his slides (inferred).
- Prateek (role not recorded in these notes): product update, Proofly, on CC13 and in the CC14 first draft (TX13 line 6702; draft slide 8). Dropped from the CC14 final deck by the user (REQ 1357).
- Rishal (role not recorded in these notes): research segment, pushed to a later call (TX13 line 6702, memory note). Whether it ran on CC14 is unknown.
- Piyush (role not recorded in these notes): the marketing roadmap slide in the CC14 first draft says "Presented by Piyush" (TX14 line 24686). The final CC14 deck keeps that content on slide 11. So marketing slides are probably presented by marketing, not Adithya (inferred).
- Sai Kiran (role not recorded in these notes): wrote the "Scribble report (Community Call Prep)" and the "Community Growth - Key Pointers" in Slack for the call (TX14 line 24851). Adithya asked him to confirm the all-hands numbers were the latest for the month.
- Manager (Rahul, inferred from REQ 2164) capped the deck at about two hours: "just like couple of hours of work. Yeah, nothing more than that" (TX13 line 6702). He set priorities on the 24 Aug call; the user asked "see what rhaul suggested" right after pasting that call (REQ 2164).
- A host who is not Adithya: a Slack message to Adithya says the host "started to track that we get more traction when I ask questions to the audience and to the presenter" and may ask a planted question, "to also promote us getting some short 15 second clips" (REQ 1373). The host's name is unknown.

### Inputs needed before starting

- The agreed segment order and speakers (below).
- The protocol team's release note for the month (the "as sent, unedited" copy kept in `WT/protocol-release-0.13.0/RELEASE-NOTE.md`).
- The marketing segment inputs from Slack (Scribble report, community numbers, event photos).
- Anything the user attaches: screenshots of dashboards, event photos, guest portrait. These are not in the repo until Claude saves them under `deck/assets/`.

### Steps, in order

1. Weekly or monthly planning call with the manager sets segments, speakers and the rehearsal day. Evidence: 24 Aug call, TX13 line 6702.
   Agreed order for 27 Aug: protocol updates, DevRel updates, product updates (Prateek, Proofly), marketing, partnerships, close. Research deferred.
2. Speak to every presenter to confirm they are on the call (Adithya's own plan, TX13 line 6702).
3. Collect each segment's inputs (see "Turn raw inputs into a slide plan").
4. Build the deck (see "Build, check and export the deck"), keeping to the manager's "couple of hours" cap.
5. Rehearse on the Wednesday. CC13: stated in the memory note. CC14: unknown whether a rehearsal happened.
6. Present live (see "Present live and after the call").

### Deliverables and where they end up

- `deck/index.html` and `deck/MOI_Community_Call_14.pdf` under `community-call-14/deck/`. In the worktree they are untracked (`git status` shows `?? community-call-14/`), and `WT/DEPENDENCIES.md` section 19 says
  both decks exist only on Adithya's Mac and nothing is committed. Update, 13 October 2026: the CC14 deck has since been merged into https://github.com/moi-foundation/MOI-Webinars under `community-call-14/deck/`. For the intro-session deck no update is recorded.
- Who receives the PDF and HTML: unknown. In the sessions Claude "sent" both files to Adithya in chat.

### Accounts and tools involved

- Slack (inputs arrive there; login needed, workspace not named in the note).
- Google Meet: the README says "In Meet, share the deck window and keep the presenter window on your own screen" (`WT/community-call-14/deck/README.md` line 8).
- Chrome (deck, presenter window, PDF export).
- YouTube (recording description, CC13 only; see post-call).
- Scribble dashboard and a "Campaign Insight dashboard" are named in the report; access, owner and login are unknown.

### Quality rules and house style

- Keep the dev update to one or two slides and make the new material the centre: "condense dev update to just 1 or 2 slides and focus on these" (TX14 line 24851).
- The deck is for the community, so no per-engine movement arrows, no competitor comparison slide, no enterprise or tender content, no unresolved metric (see Rules).

### Traps and silent failures

- The memory note calls the cadence "weekly comms cadence" in its file name but the call itself is monthly. Do not schedule four calls a month.
- The weekday drifted: CC13 Thursday, CC14 apparently Friday (inferred). Confirm the day rather than trusting the memory note.

### Time

- Manager's cap: about two hours of deck work. Actual CC14: about 45 hours wall clock between the first request (23 Sep 15:31 UTC) and the last script edit (25 Sep 12:37 UTC), roughly 25 user requests. Most of that was waiting for inputs and changing minds, not building: the first 14-slide deck came back four minutes after the first request (TX14 lines 24686 to 24788).

### Open questions

- Who hosts, who moderates Q&A, and who presents slides 5 to 11 (AI visibility through what is next) at CC14.
- Start time, length, and whether Wednesday rehearsal still happens.
- Who owns the Scribble tool login and the Slack channel where inputs are posted.

---

## Process: Turn raw inputs into a slide plan (content sourcing and curation)

### Purpose

Decide which facts go on which slide, where each number comes from, and what to leave out.

### Trigger or cadence

Every call. For CC14 it started 23 Sep with a pasted draft deck and was reshaped on 24 Sep when the Scribble report arrived.

### Who does it

Adithya, with Claude doing the assembly. Content owners: protocol team (release note), Sai Kiran (Scribble report, community numbers), marketing (Game Night, Pip, events), the user (DevRel).

### Inputs needed

1. A first-draft deck. CC14's was a pasted 40,756-character HTML deck titled "MOI Community Call #14: Building in Public" in a different design system (Sora and JetBrains Mono, its own palette).
   The user's request was "make this deck in our webinar deck format, like this content for community call" (TX14 line 24686). I could not find who produced that draft (unknown).
2. The protocol release note and release blog.
3. The Scribble report text and Slack thread (TX14 line 24851), later dashboard screenshots ("use this", TX14 line 25399/25403).
4. Event photos, engine logos, a title-slide template image (the user said "make the first slide like the template i gave u", REQ 1355; the image is not on disk).

### Steps, in order

1. Convert the draft into the MOI Builders deck framework. Claude dropped the second design system and recast panels as deck components, and "kept every figure as written" (TX14 line 24788).
   Result, 23 Sep: 14 slides, notes for every slide. First-draft order (from the pasted draft text):
   1. cover
   2. September release
   3. first-run problem
   4. KMOI nine decimals / prices in anu
   5. what breaks
   6. everything that shipped
   7. DevRel
   8. Proofly
   9. Game Night and Pip
   10. content on X
   11. Coinfest Asia Bali (with "live guests from Bali this Friday")
   12. Algix and MeitY tender
   13. what is next
   14. thank you with Open Q&A
2. Rebuild the title slide as a plain title with a huge ghost "14" (REQ 1355; TX14 lines 24809 to 24839).
3. Paste the Scribble report and the community numbers; instruction: protocol update to one or two slides, focus on the new material (TX14 line 24851).
   Claude restructured to 15 slides (TX14 line 24924):
   - protocol, in 2 slides
   - AI visibility: baseline, by engine, what people ask, MOI vs Lit, content plan
   - campaign performance
   - community
   - DevRel
   - Proofly
   - events and enterprise
   - what is next
   - close
4. Prune. In this order (REQ 1356-1363; TX14 lines 24928 to 25395):
   - "What people ask AI about MOI" removed by mistake (the user said "slide 6" but meant the MOI vs Lit slide; see Traps)
   - campaign slide removed
   - Proofly removed
   - Algix and MeitY removed
   - MOI vs Lit slide removed
   - "What people ask AI about MOI" restored
   - Coinfest replaced by Futuremode with real photos
5. Update numbers from the dashboard screenshot and typed figures (see numbers table).
6. Reorder: "move devrel slide to slide 4 like after action require" (REQ 1367).
7. Remove the up and down trend arrows from the by-engine slide (REQ 1368).
8. Closing slide: "Thanks for building in public" with takeaway lines became only "Thanks for building with us." (REQ 1370, 1372).
9. Add and then remove the guest speaker (see Variants under Build).

### Where each section of the final deck comes from

| Slide | Content | Source | Observed or inferred |
| --- | --- | --- | --- |
| 1 | "The Campfire Chat · September 2026", "Community Call #14", "Ideas. Updates. Community. Conversations." | Announcement copy the user pasted plus his correction "its claled campfire chat" (TX14 line 25251). The first draft was titled "Building in Public". Ghost "14" from the title template image. | Observed |
| 2 | September release: fee delegation, KMOI on MASN, prices in anu, live on devnet 11 Sept | `WT/protocol-release-0.13.0/RELEASE-NOTE.md` (protocol team's note, unedited) and `BLOG.md` lines 10, 14-17, 40. "Zero KMOI" bullet comes from first-draft slide 3. | Observed |
| 3 | Upgrading from August: three-package install, old id `0x108000004cd973c4` search, storage a millionth, fuel under 50 anu, participant lists, notary exception, max supply 0 or over 18 decimals | Release note for versions and participant list. `BLOG.md` lines 15-17, 159-163 for the old id and the asset limits (the unedited release note does not contain those two). | Observed |
| 4 | DevRel: MCP server (in progress), MOI and x402, the blog | First-draft slide 7, text almost unchanged. Underlying work: `WT/x402-compat/` and the blog pipeline. | Observed (draft); work itself outside this note |
| 5 | AI visibility baseline: 47 queries, 5 engines, 17.3%, 1,203 citations, 650 mentions | Dashboard screenshot attached 24 Sep and figures typed by the user ("also visibility 17.3% / 1203 citation and growing / ... 650 mentions"). Claude had first used the user's "18%" and switched to 17.3% as "more precise" (TX14 line 25534). "47 queries, 5 engines" is from the Scribble report text, which Claude flagged as older. | Observed |
| 6 | By engine: Perplexity 20, Gemini 19.1, Copilot 19, ChatGPT 12.8 (the sources give no unit; visibility percentages, inferred); 221 of 226 responses, 97.8% | Dashboard screenshot for Perplexity, Gemini, ChatGPT; "copilot - 19%" typed (REQ 1365). Coverage 221 of 226 is from the Scribble report text and was never reconfirmed (TX14 line 25534). Logos fetched from Wikimedia Commons. | Observed |
| 7 | What people ask AI about MOI | Scribble report section 3, with the Lit Protocol query dropped (TX14 line 25170). The sentence "Nobody is asking about the parts we discuss internally" is not in the Scribble report. | Observed; that sentence is Claude's addition (inferred) |
| 8 | Content plan: core education, product led, comparison | Scribble report section 6, near verbatim. | Observed |
| 9 | Community: 120+ new Discord joins, 60+ active, Game Nights biggest contributor; Game Night seventh run, 42 at peak up from 20, Gartic, poker next; Pip live in Discord | Sai Kiran's "Community Growth - Key Pointers" (Slack, TX14 line 24851) for the first card; Game Night and Pip details from first-draft slide 9. | Observed |
| 10 | Futuremode, Taipei, 4 to 6 Sept, Taipei Expo Dome, Building AI-Native Crypto Products panel | Two photos the user attached 24 Sep. Dates, venue and description fetched by Claude from the event's own site (TX14 line 25395). Panel name read from the photo backdrop (TX14 line 25721). Claude said it would not name who attended or claim outcomes; the sentence "the people we met there are the ones we are now bringing onto these calls" was carried over from the Coinfest slide with no Futuremode source. | Observed; that sentence is unsourced (inferred) |
| 11 | What is next, two cards | Scribble report section 10 ("Fix/verify campaign CTR and attribution" became "Verify the campaign click-through"), first-draft slide 13 (Humanised podcast, Game Night, Pip, University of Hong Kong). | Observed |
| 12 | "Thanks for building with us." | The user's rewrite (REQ 1370, 1372). | Observed |

### Slide order and why

Final order (`index.html` lines 204-354, `TITLES` lines 368-381): title, September release, upgrading, DevRel, AI visibility, by engine, the questions, content plan, community, Futuremode, what is next, close.

- Protocol and DevRel come first. This is the original segment order from the 24 Aug plan (protocol, DevRel, product, marketing, partnerships, close).
  The user moved DevRel to slide 4, "after action required", so all developer material sits together up front (REQ 1367; TX14 line 25762 says the same).
- The AI visibility block runs in the same order as the Scribble report's numbered sections: baseline (1), engines (2), what people ask (3), content plan (6). It then ties back to DevRel through the blog card on slide 4. Report sections 4 (coverage) is folded into slide 6; 5 (Lit), 7 and 8 (campaign) and 9 were cut; 10 became slide 11.
- Community and events (marketing and partnerships) follow, then "what is next", then close.
- Why this order beyond the DevRel move: the order of segments is observed; the reasoning that urgent upgrade material goes first is (inferred).

### Deliverables and where they end up

The deck folder, the README flow line, `SCRIPT.md`. See "Build, check and export".

### Accounts and tools

Slack for inputs; Wikimedia Commons for brand logos; the Futuremode site for facts; LinkedIn and the guest's own site for guest details (guest later removed). None needed a key from Claude's side.

### Quality rules and house style

- The user's numbers win. Claude reports which figures it could not refresh: after the dashboard update it said "the 47 queries and five engines, and the 221 of 226 coverage, are still the older figures. Send the current ones" (TX14 line 25534). The user never replied in the logged requests, so those three figures are unverified.
- Do not guess a guest's title ("his public profile lists Krexa but no job title, so I left the title off", TX14 line 25121).
- Real photos only. Claude searched the disk and Drive for Bali photos, found none and built empty frames rather than stand-ins (TX14 line 25057).
- Drop a claim you cannot source: Claude declined to say who spoke at Futuremode or claim outcomes (TX14 line 25395).

### Traps and silent failures

- A removed slide leaves references behind (see Traps section).
- The first-draft figures (42 people, 64K impressions, $100K demo day, MeitY details) were "kept as written" and Claude warned "the numbers date from the original call, so check them" (TX14 line 24788). Several were later deleted with their slides.

### Time

First rebuild 4 minutes; restructure around the Scribble report 3 minutes (TX14 lines 24851 to 24924). The slow part was the user deciding what to cut over about 30 hours.

### Open questions

- Origin of the first-draft HTML deck, and who owns its content.
- Are 47 queries, 5 engines and 221 of 226 current? (47 x 5 = 235, not 226; the deck does not explain the gap.)
- Gemini is "up 12.8 points" in the slide 6 sentence and ChatGPT's level is also 12.8%. It may be real or a transcription slip; check against the dashboard before the next call (inferred concern).

---

## Process: Build, check and export the deck (moi-deck)

### Purpose

Produce a single-file HTML deck with a presenter window and a slides-only PDF, with no build tooling.

### Trigger or cadence

Every call and every builders session. The framework was first made for session 8 (`WT/session-8-policies/deck/index.html`), reused unchanged for the intro session, then reused for CC14 and packaged as the `moi-deck` skill on 28 Sep (REQ 1378; TX14 lines 26172 to 26254).

### Who does it

Claude, from raw material handed over by Adithya. Adithya asked for the skill so the process is abstracted from him: "package those skill as a handover thing, that abstracts me from the process" (REQ ~1378).

### Inputs needed

Raw material: report, Slack dump, screenshots, photos, a title-slide template image; the deck title and chip text.

### Steps, in order

Commands and files are from `moi-deck/SKILL.md`, `reference/build.md`, and what Claude actually did on CC14.

1. Make the folder: `<session>/deck/` (for example `community-call-14/deck/`). Scaffold with
   `~/.claude/skills/moi-deck/scripts/new-deck.sh <session-folder> "<Deck title>"`, which copies `assets/template.html` to `<session>/deck/index.html`, creates `deck/assets/`, and sets the `<title>`.
   (For CC14 and the intro deck the template did not exist yet; they were copied from session 8.)
2. Write one `<section class="slide ...">` per slide. Backgrounds: `light`, `lav`, `dark grad`, `dark`; neighbours should differ. Components and the spacing budget are in `reference/components.md`. Each slide: chip, `h2` with one `accent` span, optional `sub`, one component (cards, stats, `cmp` table, steps, code, photos). Cards at most three.
3. Number the corner badge `slide-num` to equal the page number. Cover and close carry no badge.
4. Write one entry per slide in the `TITLES` and `NOTES` arrays near the bottom of the file (see Script process).
5. Edit through a Python script that asserts the target text occurs exactly once before replacing (`reference/build.md` "Editing an existing deck"). This was learned in CC14: an edit that did not match the alt text "Coinfest Asia, Bali" aborted and left the deck untouched (TX14 lines 25361 to 25367).
6. Render: `~/.claude/skills/moi-deck/scripts/render.sh <session>/deck/index.html [output.pdf]`. It extracts the first `<script>`, runs `node --check` on it, runs headless Chrome
   `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=8000 --print-to-pdf=<pdf> file://<html>`,
   then compares `grep -c '<section class="slide'` with the PDF page count from `pdfinfo` and prints MISMATCH if they differ. Pass the PDF name when one already exists (CC14: `render.sh deck/index.html MOI_Community_Call_14.pdf`).
   Page setup is in the print CSS: `@page { size: 1920px 1080px; margin: 0 }`, reveals forced visible.
7. Check by eye: read the PDF pages back as images and look at the slides you changed (`build.md`). On CC14 Claude also opened the deck in a browser and confirmed the script built 13 dots for 13 slides and arrow keys worked (TX14 lines 25505 to 25513).
8. Update `README.md` in the deck folder (flow line, photo slots, variants) after each change (done on CC14 throughout).
9. Hand back: send the HTML and the PDF, name the primary file, and list what was left out and why (`build.md` "Hand-back").
10. Presenting: open `index.html` in Chrome, arrow keys or click to move, `P` for the presenter window, share the deck window.

Variants (CC14): the user asked for "one version with and one without" the guest speaker (REQ 1369). Claude cut `index-no-guest.html` from `index.html` by deleting the guest slide and renumbering, and exported two PDFs.
Rule from `build.md`: edit the primary and re-cut the variant, never edit both by hand.

Logos: from the owner's own site or Wikimedia Commons: `curl -sSL -o assets/engines/gemini.svg "https://commons.wikimedia.org/wiki/Special:FilePath/Google_Gemini_icon_2025.svg"`; find the exact filename first with the Commons search API shown in `build.md`.

### Deliverables and where they end up

`index.html`, `index-no-guest.html`, `MOI_Community_Call_14.pdf`, `MOI_Community_Call_14_no_guest.pdf`, `README.md`, `assets/`. Sent to the user in chat. Not committed (untracked) when written; see the update in Deliverables above for the CC14 deck.

### Accounts and tools involved

Chrome (installed locally, no login), Python 3, Node (for `node --check`), `pdfinfo`/`pdftotext` (poppler). Wikimedia Commons (no key). Fonts load from Google Fonts at open time, so the deck needs network for Poppins or falls back to `sans-serif` (inferred from `index.html` line 9).

### Quality rules and house style

From `SKILL.md`: every number comes from the person; photos are real files only; the corner badge equals the page number; say what the source says; one idea per slide.
Brand tokens in `:root` (`index.html` lines 39-59): `--moi-main #4B17E5`, `--moi-dark #320F99`, `--moi-black #0A0026`, lavender backgrounds, `--lav-accent #BCA6FF`. Poppins for everything except code. Fixed 1920x1080 stage scaled to the window. Cover: big logo, chip, `h1`, one `sub`, ghost numeral. Close: logo and one line.
The rule that was ignored in CC14: neighbours must not share a background. CC14 slides 7 and 8 are both `lav`, and 9 and 10 are both `dark grad` (`<section class="slide ...">` list; checked).

### Traps and silent failures

In plain terms, two defects can break the live deck while the PDF still looks fine, because printing to PDF does not run the deck's JavaScript or its screen scaling:

- A typing slip in the speaker-notes text (a real line break, or a missing comma) stops the deck's JavaScript, so the arrow keys, the slide dots and the presenter window all stop working.
- A stray closing tag on CC14 slide 10 pushes slides 11 and 12 out of the scaled slide area, so on any window that is not 1920x1080 they are cropped and slide 10 loses its number badge.

The numbered list gives the technical detail.

1. Real newlines inside a `NOTES` string, or a missing comma between entries, are JavaScript syntax errors. The whole inline script dies: arrow keys, dots and the presenter window stop, but the PDF still prints because print CSS needs no JavaScript.
   Hit on CC14 (found and fixed 24 Sep, TX14 line 25451), and **still present in `WT/intro-session/deck/index.html`**: the slide 4 notes entry (lines 377-385) has literal line breaks. I confirmed with a parse of the extracted script: CC14 parses OK, intro deck fails with "Invalid or unexpected token".
2. **A stray `</div>` on CC14 slide 10 (`index.html` lines 332-333) breaks the live deck and no current check catches it.** In a real Chrome DOM dump, slides 11 and 12 become children of `.deck-viewport` instead of `.deck-stage`, and slide 10's `slide-num` is outside its section.
   Effect: in a window that is not 1920x1080 (I tested 1280x720), slide 11 is unscaled and cropped on the right and bottom while slide 9 scales correctly. The PDF is fine because print CSS makes the stage static, and the page count still matches 12. In the PDF, slide 10 has no "10" badge (`pdftotext` page 10 shows no number). Same defect is in `index-no-guest.html`.
3. Edits that do not match the file abort silently or apply nothing; use asserted replacements and re-check the result (TX14 lines 25361, 25424, 25441).
4. `README.md` goes stale: CC14's says "13 slides (with the guest speaker)", describes slide 12 photos "both in place", and says "figures unchanged". The deck is now 12 slides with no guest, and the figures changed on 24 Sep.
5. The two variant files are now byte-identical, so the "variant" setup has no purpose; the `no_guest` PDF (25 Sep 08:00 EDT) is older than the HTML (08:37 EDT) but has identical text. The `MOI_Community_Call_14.pdf` timestamp of 28 Sep 14:30 EDT is Claude's test of `render.sh` while packaging the skill, not a call-time export (inferred from TX14 line 26254: "re-rendering community call 14 gives 12 slides and 12 pages under its existing filename").
6. The presenter window title is hard-coded "Presenter: MOI Builders · Intro" in the template and in the CC14 deck (`index.html` line 404; `template.html` line 240).
7. `build.md` tells you to run `render.sh deck/index.html deck/index-no-guest.html` for both variants, but with two non-PDF arguments the script writes `index.pdf` and `index-no-guest.pdf`, not the existing `MOI_Community_Call_14*.pdf` names.
8. The skill's "A deck to copy from" points at `~/MOI-Webinars/community-call-14/deck/`. When checked, that path did not exist in the main checkout (`ls` fails); the folder existed only inside this worktree and was untracked. Update, 13 October 2026: the CC14 deck is now in https://github.com/moi-foundation/MOI-Webinars under `community-call-14/deck/`.
9. `render.sh` writes its parse check to a fixed `/tmp/moi-deck-check.js` and silently skips the check if `node` is missing.
10. Gemini's Wikimedia file was a wordmark with a stray bounding box; a wrong Commons filename returns an HTML 404 page; `svgl` search returned nothing (TX14 lines 25584 to 25635).

### Time

First build 4 minutes; a typical single edit and re-render 20 to 60 seconds of Claude time. The CC14 deck went through about 18 edit rounds between 23 and 25 Sep (counted from the assistant replies in TX14 lines 24782 to 26142).

### Open questions

- Should the two variant files be deleted? Claude offered ("Say the word and I'll delete the no-guest pair", TX14 line 26116); no answer in the requests.
- Should the skill live in the repo? Claude asked; `DEPENDENCIES.md` section 19 item 6 says "Put the moi-deck skill in the repo" as a ToDo.

---

## Process: Write the spoken script and presenter notes

### Purpose

Give the presenter a word-for-word script, one entry per slide, that appears in the presenter window (`P`) and as `SCRIPT.md`.

### Trigger or cadence

Per call, only for the slides the user presents. CC14: "gimme a script fro sldies 2 3 4" (REQ 1371, 1374). CC13: "a simple script for the updates, high level speeches for each slide", slides 2 to 6 (REQ 2273, 2275).

### Who does it

Claude drafts; Adithya corrects wording; the host may feed in questions.

### Inputs needed

The final slides; any question the host will plant; the user's earlier scripts as a voice sample; the humanizer and stop-slop skills.

### Steps, in order (CC14, 25 Sep 11:41 to 12:37 UTC)

1. Version 1 of slides 2 to 4, about a minute per slide, saved to `community-call-14/SCRIPT.md` and into `NOTES` in both deck files (TX14 line 25949).
2. User pastes the host's heads-up and asks for the answer to the planted question "If I'm completely new to MOI and I have zero KMOI, an application can essentially handle that fuel requirement for me?" (REQ 1373).
   Claude gave a 15-second answer plus a second beat, one trap ("don't say the app pays for you without qualification, because fee delegation covers fuel and nothing else"), and an honest fallback line (TX14 line 25999).
3. Version 2 adds a bracketed cue on slide 2 for that question: `[If the host asks the zero-KMOI question here: yes. ...]` (TX14 line 26024).
4. User: "use humanize, and it snot called voyage decnet, just say went live on devnr" (REQ 1375). Version 3 is rewritten in a spoken voice and "Voyage devnet" becomes "devnet" on the slide and the notes (TX14 line 26090).
5. User trims two phrases (REQ 1377): "Not save a setting, not call your logic." and ", and in practice that second account is yours. Your app holds one funded account and names it as the payer." Version 4 is the file on disk (TX14 line 26142). The slide bullet "Your app holds one funded account and names it as the payer" stayed on slide 2 (`index.html` line 220); only the script lost it.
6. Keep `NOTES` and `SCRIPT.md` identical. I verified slides 2, 3 and 4 appear verbatim in `SCRIPT.md`. `NOTES` strings are JavaScript: use `\n`, never a real newline.

### Deliverables and where they end up

`WT/community-call-14/SCRIPT.md` (slides 2 to 4) and the `NOTES` array in both HTML files (all 12 slides). The `NOTES` for slides 1 and 5 to 12 are the first-draft machine-written notes. The record shows no request to polish or humanize them, so they probably never got the voice pass (inferred).
Word counts (`NOTES`): slide 1: 43, 2: 239, 3: 199, 4: 122, 5: 59, 6: 60, 7: 85, 8: 55, 9: 83, 10: 54, 11: 78, 12: 14; total 1,091 words, about 8 minutes at 140 words a minute (inferred pace). Slides 2 to 4 alone are 560 words, about 4 minutes.

### Accounts and tools involved

`humanizer` skill (strips AI tells without changing meaning) and `stop-slop` skill (REQ 1070: "use stop slop across"). No keys.

### Quality rules and house style (script voice)

All rules below come from corrections the user made. Dates and request lines are given.

- Speak in complete sentences as a human giving a presentation. On 4 Sep (REQ 1063, dev webinar 8) the user rejected a draft in strong words: he called the script horrible, asked why it kept using "not this, not that" lines, told Claude to talk in complete sentences as if he were a human giving a presentation, and to stop "aura farming" (the user's slang for showy, impressive-sounding lines).
- Every line must be readable aloud verbatim. "this is not a setence i can rea dverbatim" (REQ about 1066-1068, 4 Sep, in reply to a sample line about booking flights with aisle seats).
- No "not this, not that" constructions. Reapplied on CC14: "rm Not save a setting, not call your logic." (REQ 1377).
- Longer flowing sentences, not staccato short ones; warm, not cold. "notice how i like longer sentces and not stacctattod short aura sentences" (REQ 649, 7 Aug); "the last transcript you wrote was too cold" (REQ 590, 5 Aug).
  (The moi-deck skill says "short sentences"; see the open question below.)
- Run `humanizer` and `stop-slop` over the whole script (REQ 1043: "run a few rounds of humanization"; REQ 1375).
- Explicit slide-change cues must be in the file, not buried in a paragraph: "in the file can u add clear prititons form when i shd change to slide ... need it to be epxlcit" (REQ 1091, 4 Sep). The session 8 `SCRIPT.md` does this with headers like `## PRESS NEXT --> SLIDE 2 · The use case`. The CC14 `SCRIPT.md` uses plain headers ("## Slide 2, the September release") with no "press next" cue, so it is weaker than the standard the user asked for.
- Presenter notes in the HTML must match the script file: "fix the presenter notes to match the script" (REQ 1030) and "the presenter notes are unchanged" (around REQ 1097).
- Use the product names as the user does: "went live on devnet", never "Voyage devnet" (REQ 1375).
- No em dashes in script or slide copy. I counted zero in `SCRIPT.md` and in slide text; the only em dashes in the HTML are in the `<title>`, the presenter title and comments.
- Cut closers that invite applause or hand over the floor: "Open Q&A. The floor is yours." was removed (REQ 1372); the closing note is now one line.
- Terminology (the 14 Sep corrections from the person these notes call "the founder", an inference by the research assistant; memory `moi-terminology-corrections.md`): participant-centric, not account-centric; MDAG not per-account chain; Sarva Labs builds, MOI Foundation governs; say network ID. These are applied in the intro deck (slide 3 card) and were not needed in the CC14 slides.
- Technical wording must stay inside what the protocol does: the payer covers fuel only, signs each interaction separately, and the user still funds any value they send (`SCRIPT.md` lines 11, 13).

### Traps and silent failures

- Editing `SCRIPT.md` but not `NOTES` (or the reverse) leaves two scripts. On 4 Sep the user saw an old script in the presenter window three times in a row (REQ 1093-1097).
- The slide 1 note says "what our campaign is doing" and slide 11 says "verify the campaign click-through", but the campaign slide was deleted. Slide 6 and its note still state "Gemini moved the most, up 12.8 points, while ChatGPT slipped 4.3" after the user removed the movement arrows from the tiles; Claude flagged this and the user did not answer (TX14 line 25800).
- Relative time words go stale: "last Friday" (slide 9 and its note), "since the last call".

### Time

About one hour for slides 2 to 4 across four versions (11:41 to 12:37 UTC on 25 Sep).

### Open questions

- Who writes and checks the scripts for slides 5 to 12, and who presents them.
- Whether the planted host question was asked live and whether the clip was cut.
- Which wins when the moi-deck skill says "short sentences" and the user asks for longer flowing ones? The CC14 script is mixed, with some short punches ("One new thing, and two that break."). (inferred) Treat "short sentences" in `SKILL.md` as softer than the user's own words.

---

## Process: Verify the release and dev-update slides against source

### Purpose

Make sure every version, price, id and "what breaks" line on the dev-update slides is true and complete.

### Trigger or cadence

Every call that carries protocol news. CC13 (27 Aug) was the first run of this, CC14 the second.

### Who does it

Claude checks; Adithya decides. The protocol team's note is the authority for what shipped.

### Inputs needed

The protocol team's release note (kept unedited), the release blog, GitHub release pages, SDK source on disk. CC14: `WT/protocol-release-0.13.0/RELEASE-NOTE.md`, `BLOG.md`.

### Steps, in order

1. Keep the team's note verbatim next to the blog (`RELEASE-NOTE.md` header: "as sent by the protocol team, unedited").
2. For each package on the deck, compare the line to its GitHub release notes and local source. Only if Adithya asks for parallel agents: one Haiku agent per package, as in the CC13 method (TX13b line 1955: `audited: 8`, verdicts accurate / imprecise / wrong). The user's saved preference now says not to run multi-agent workflows unless he explicitly asks (memory `no-multi-agent-workflows`); the CC13 run was at his request ("can u pause the worfklow and use aiku agnets, i dont anna run out of session limit", REQ 2256).
3. Catch the items that fall off decks: non-headline packages, point releases and release candidates. CC13 example: `js-moi-agent-registry v0.3.0-rc1` is an RC pinned to an exact SDK peer, so a deck line saying it "shipped" was wrong (TX13 lines 9598, 9642; TX13b line 1955).
4. A release gets its own slide only if it carries a breaking change, an action for the audience, or a concept that needs explaining (Claude's rule in TX13 line 9642; the user answered "we can have a slide individually for each package" REQ 2254 and then "the first slide shd be this, then we can talk abt the specific changes, and then end off with a specific slide for validators explaining the IOME change" REQ 2260). CC14 compressed the release to two slides on the user's instruction.
5. State what is live. CC14: Claude flagged on 15, 23 and 25 Sep (TX14 lines 24406, 24788, 25999) that its saved note said devnet was running a pre-September build. The user's answer was to write "went live on devnet" (REQ 1375). The release pack says "live on Voyage devnet since 11 September 2026" (`BLOG.md` line 40, `social/discord.txt` line 3).
6. Re-use the exact strings from the blog for ids and counts, for example the old KMOI id `0x108000004cd973c4` (`BLOG.md` line 159).

### Deliverables and where they end up

Slides 2 and 3 and their notes; for CC13 a one-paste deck-update prompt (TX13 lines 9774, 9820; TX13b lines 2004, 2032) because the CC13 deck was built outside the repo and updated through a prompt, not by Claude editing a file.

### Accounts and tools involved

GitHub (read), npm, local clones of the repos (readable per memory `moi-source-on-disk`), Chrome.

### Quality rules and house style

- Never present an RC as shipped.
- Use the SDK helper wording ("use parseKmoi, do not work out anu by hand") exactly as the release note says: "Do not calculate these conversions manually."
- Say exactly what a change does and does not cover (fee delegation pays fuel only).

### Traps and silent failures

- The unedited note says "scheduled for today at 12:00 AM UTC"; a correction went out on X because "12:00 AM UTC" was read as midday. The correct time is 00:00 UTC on 11 Sept (`social/x-correction-reply.txt`).
- Do not copy features that exist only in source onto a slide for a live demo or network (memory `devnet-build-lag.md`). At the time of writing the intro deck still has the exact problem (see the intro-session process).
- The CC13 deck once had a slide titled "Everything That Shipped" that showed breaking changes only, and a Coinfest slide in future tense next to a slide of photos from it. Both were caught by Claude on the day (TX13 line 10165).

### Time

CC13: about 5 hours before the call from the call notes to a verified deck prompt (04:47 to about 10:00 UTC on 27 Aug). CC14: protocol slides were already written; the changes were prunes.

### Open questions

- Was devnet actually on v0.13.0 when the call ran?
- Who from the protocol team confirms "live" status before each call?

---

## Process: Present live, and what happens after the call

### Purpose

Deliver the call from the deck, and publish the recording and links afterwards.

### Trigger or cadence

Each call. For the live part only CC14 and the README are evidence. For the after part only CC13 is evidence.

### Who does it

Adithya presents his slides; the host moderates and asks planted questions; marketing handles announcements (X drafts for the call were composed natively in X by someone else, TX13b line 1790, inferred to be marketing).

### Inputs needed

The deck HTML open in Chrome, the presenter window, the PDF as a fallback, the host's question list.

### Steps, in order

Live (observed in `WT/community-call-14/deck/README.md`):

1. Open `deck/index.html` in Chrome. Arrow keys, space or a click to move; dots at the bottom jump.
2. Press `P` to open the presenter window with the script, next-slide title and a clock. It drives the deck.
3. Share the deck window in Meet and keep the presenter window on your own screen.
4. If the host asks the zero-KMOI question at the fee-delegation slide, use the bracketed cue in slide 2's notes.

After the call (observed for CC13 only; TX13 lines 9567, 10119 to 10172):

5. Write the YouTube description. Structure Claude used: title "MOI Community Call #13: Building in Public"; a three-sentence summary; "Recorded [DATE]" (to be filled); CHAPTERS with `00:00 Welcome` first and `[__:__]` placeholders for the rest (YouTube needs the first chapter at 00:00 and chapters must match what was actually said);
   "IF YOU ARE UPGRADING" with one line per package; "VALIDATORS" block; "READ THE FULL WRITE-UPS" with blog backlinks (the SEO point the manager asked for: "include backlinks for SEO optimization in YouTube descriptions", TX13 line 9567); "BUILD ON MOI" links; community links; a one-line description of MOI; a "Next up: Community Call #14, with live guests from Coinfest Asia, Bali." teaser; hashtags. Kept under YouTube's 5,000-character limit (Claude counted: TX13 line 10172). 18 of 20 links checked live; one dead because a post's pull request was unmerged.
6. Distribution: "publishing a blog is not the end of the task; every post must also go out across MOI's social accounts and to the mailing list" (manager, 24 Aug; memory `blog-distribution-is-part-of-done.md`). Whether this applies to the call recap is unknown.

For CC14 there is no evidence of a YouTube description, recording, recap post, social post or follow-up. A search of TX14 lines 24686 to 27620 (23 Sep to 1 Oct) for YouTube, recording, recap and chapters finds nothing about the call.

### Deliverables and where they end up

CC13: a YouTube description (pasted in chat, not saved to the repo; the scratchpad copy no longer exists). CC14: nothing known.

### Accounts and tools involved

Google Meet, YouTube (channel owner unknown), Chrome. For announcements: X, LinkedIn, Discord, Telegram through Buffer or natively (the Buffer pipeline creates drafts only and never publishes, TX13b line 1785).

### Quality rules and house style

- Chapters must match the order actually presented (TX13 line 10126).
- Descriptive anchor text on links, not "read more" (TX13 line 10126).
- Date the video (TX13 line 10126).

### Traps and silent failures

- A teaser written into one description can promise something the next call drops: CC13's description promised "live guests from Coinfest Asia, Bali" for CC14; the final CC14 deck has neither Coinfest nor a guest.
- A screenshot saved to `~/Downloads` could not be read by Claude's process on 27 Aug: macOS blocked it (EPERM) four times and the fix was `mv ~/Downloads/<file> /tmp/<file>` (TX13 lines 9593, 10115, 10145). Whether this still applies is unknown.

### Time

CC13 YouTube description: about 15 minutes from the call to a link-checked draft (TX13 lines 10119 to 10172, inferred from timestamps).

### Open questions

- Is the call recorded and posted for every edition? Who uploads? Which channel?
- Is there a Luma, Discord event or website calendar entry? The website has a `community_calls` Supabase table behind the homepage calendar, edited at `/admin/calendar` with an admin key, and `WT/DEPENDENCIES.md` section 4 says the calendar fails in production (at the time of writing) and falls back to a hard-coded schedule. Whether anyone adds each call there is unknown.
- Are the 15-second clips produced, by whom, and posted where?

---

## Process: Builders intro session (the "MOI Builders · Intro session" deck and live launchpad demo)

### Purpose

Teach a new audience what MOI is in four ideas, then have them launch a real agent through the Agent Launchpad. Slide 1 says: "What MOI is, in four ideas. Then a live agent: on chain, on your laptop, in your Telegram." (`intro-session/deck/index.html` line 195).

### Trigger or cadence

A one-off request on 12 Sep: "Ok i need to make an intro to MOI webinar session, like a few slides on basics of MOi and then using the agent laucnhpad itself" (REQ 1329). It belongs to the MOI Builders webinar series (chip "MOI Builders · Intro session"). Not clearly recurring. Date held: unknown (the final PDF is 15 Sep 09:01 EDT).
Audience: the user said "launchpad is just a way for students to get exposed to agents" (REQ 1351), so students or newcomers (inferred).

### Who does it

Adithya presents (the notes open "I'm Adi, I work on ecosystem at Sarva Labs", `index.html` line 374). Claude builds.

### Inputs needed

The launchpad source (`sarvalabs/moi-agent-launchpad`, master as of 9 Sep 2026; the README lists the files), the live site, a wallet and Telegram account for the demo. The 14 Sep terminology corrections (see "the founder" in the header).

### Steps, in order

1. Study the launchpad end to end first: "can u first study the launchpad end to end and then help me build a deck" (REQ 1329). Claude read every page, the ten templates, the Sign-In With MOI message, the owner-signed registration, the downloadable runtime, relay auth, the AgentMarket Coco logic and the live site (TX14 line 23031). The README names the source files: `lib/siwm.ts`, `lib/moi/real.ts`, `lib/moi/registry.ts`, `docs/how-it-works.md`, `agent-runtime/`, `contracts/agent_market/agent_market.coco`.
2. Draft the 11-slide flow in two halves: basics, then launchpad. Final flow (`README.md`): title, start here, four ideas, why agents on MOI, the launchpad, live demo, under the hood, where it runs, the marketplace, full circle, close.
3. Build it in the same deck framework as session 8. The first attempt was a PPTX in a different design, then an HTML in the same different design; the user rejected it: "make it us the same insnaely vool loojing thing we had for th eats demo, i wnat teh exact same deck deisfn man" (REQ 1332). Claude then lifted the session 8 CSS, logo symbols, planetoid path and presenter script verbatim (TX14 line 23358). ("eats demo" is probably session 8, inferred; the README says "the same deck framework as session 8".)
4. Export HTML and PDF with the same Chrome command as the other decks (`intro-session/deck/README.md`).
5. Refresh live numbers before presenting (TX14 line 24280): `curl -s https://launchpad.moi.technology/api/stats`, use the `registered` field (20 on 15 Sep) not `activeAgents` (22, which the code says overcounts). The user then removed the stats row entirely (REQ 1354, "rm"; TX14 line 24631).
6. Correct claims the user rejects on review (15 Sep, REQ 1350-1352):
   - "rm the live on vyage dent thing": removed "Live on Voyage devnet" from the title.
   - "this is not a real feature of launhcpad": a slide presenting a scoped grant as a launchpad feature was replaced by "Why agents belong on MOI", framing the launchpad as a playground.
   - "add a visual for why agenst belong on moi": two inline SVG diagrams side by side (everywhere else vs on MOI).
7. Run the live demo from slide 6: switch to the browser at `launchpad.moi.technology`, wallet popup, Telegram, agent page, back to slide 7 (README demo cue). The four beats on the slide: connect (Sign In With MOI, no fee), pick Weather Brief and deploy, register (approve in wallet, agent on chain), link Telegram, run the setup script, first message. Then read the agent back off the chain (owner, agent wallet, status, card).
8. Pre-flight: dry-run the demo on devnet; devnet was reset on 11 Sep so wallets may need re-activating (TX14 lines 23031, 23358; assistant statements, not user rules).

### Deliverables and where they end up

`WT/intro-session/deck/index.html`, `MOI_Builders_Intro.pdf`, `README.md`. Untracked in git. Notes total 1,439 words (about 10 minutes at 140 wpm, inferred), with explicit demo cues written as `⟶ [SWITCH TO THE BROWSER, launchpad.moi.technology]` inside the slide 6 notes.

### Accounts and tools involved

- MOI Wallet (extension) and a funded or activated account on devnet; a Telegram account; `@moinetworkbot`; launchpad site (login is Sign In With MOI, no password); pm2 on the presenter's laptop for the agent runtime.
- Chrome, Meet.

### Quality rules and house style

- Same design as session 8, exactly. The user wants consistency, not a new look.
- Only claim what the launchpad source shows; present the launchpad as a playground, not the protocol.
- Do not claim a protocol feature that devnet does not run.
- Participant-centric wording on the four-ideas slide.
- Slide backgrounds alternate correctly in this deck (dark, light, dark, lav, light, dark, light, lav, light, lav, dark) and badges run 02 to 10.

### Traps and silent failures

1. `intro-session/deck/index.html` slide 4 `NOTES` entry has real line breaks (lines 377-385). The extracted script fails to parse, so in the saved HTML the arrow keys, dots and presenter window are dead. The PDF is fine. The break was introduced by the slide 4 rewrite on 15 Sep (inferred from the 12:39 UTC edit, TX14 line 24406) and Claude's checks that day looked only at the rendered PDF pages (TX14 lines 24406, 24525). No request in the history complains about it, so I do not know whether the session was presented from this file.
2. Slide 3's note still says "Since v0.13.0 someone else can pay that fuel for you, and you will see why that matters for agents." On 15 Sep Claude flagged this sentence as possibly wrong because devnet then ran an older build and "nothing later in the deck shows it. It's worth cutting that sentence before you present" (TX14 line 24406). It is still in the file at the time of writing.
3. Slide 9's note says "Eleven agents are listed right now, one of them paid." This is a live number that goes stale; the user removed the stats row for the same reason. Check or cut before every run.
4. The demo slide heading still says "On devnet" (Claude pointed this out; the user's request removed only the title-slide phrase, TX14 line 24324).
5. The presenter window title says "Presenter: MOI Builders · Intro" (fine here, wrong when copied).
6. The first build was the wrong design (PPTX with Inter), costing one round trip. Start from the session 8 framework or `moi-deck/assets/template.html`.
7. After a session the dev-webinar flow expects a blog post and distribution. On 15 Sep the user asked whether the last webinar's blog had been pushed; it had not (PR #52 on the website repo was stale and carried an overclaiming draft, TX14 line 24590). Whether the intro session got a blog is unknown.

### Time

First full deck in about 8 minutes (12 Sep 15:56 to 16:04 UTC); redesign in session 8's look in about 50 minutes; two review rounds on 15 Sep took about 30 minutes (12:33 to 13:01 UTC).

### Open questions

- Date, platform, audience and size of the intro session; whether it was recorded; whether it is meant to repeat.
- Whether it was presented from the HTML (broken script) or the PDF.
- Whether the session was announced on Luma like the dev webinars (REQ 898-910 show Luma used for session 8).

---

## Reusable assets

Deck framework and skill:

- `~/.claude/skills/moi-deck/SKILL.md`
- `~/.claude/skills/moi-deck/assets/template.html` (framework with one title slide; stale presenter title)
- `~/.claude/skills/moi-deck/reference/components.md` (copy-paste markup for every component, spacing budget)
- `~/.claude/skills/moi-deck/reference/build.md` (render, variants, photos, logos, traps)
- `~/.claude/skills/moi-deck/scripts/new-deck.sh`
- `~/.claude/skills/moi-deck/scripts/render.sh`

Worked examples:

- `WT/community-call-14/deck/index.html` (final 12-slide CC14 deck; has the slide 10 nesting defect, fix before reuse)
- `WT/community-call-14/deck/MOI_Community_Call_14.pdf`
- `WT/community-call-14/deck/README.md` (stale; see traps)
- `WT/community-call-14/SCRIPT.md` (slides 2 to 4 script in the user's approved voice; the best voice sample on disk)
- `WT/community-call-14/deck/assets/engines/{perplexity,gemini,copilot,chatgpt}.svg` (four AI engine logos)
- `WT/community-call-14/deck/assets/futuremode-1.png`, `futuremode-2.png`; unused: `mohit.webp`, `krexa-logo.webp`
- `WT/intro-session/deck/index.html` (11-slide builders intro; two inline SVG diagram cards on slide 4; the `.code` block for the Coco logic on slide 9; `.beats` demo slide; `.steps` close). Fix the slide 4 `NOTES` newlines before reuse.
- `WT/intro-session/deck/README.md`, `MOI_Builders_Intro.pdf`
- `WT/session-8-policies/deck/index.html` (the framework's origin), `WT/session-8-policies/SCRIPT.md` (script format with `PRESS NEXT --> SLIDE N` cues), `WT/session-8-policies/LUMA.md`

Inputs and sources for the protocol segment:

- `WT/protocol-release-0.13.0/RELEASE-NOTE.md`, `BLOG.md`, `SOCIAL.md`, `social/`

Evidence-only assets (exist only in transcripts, worth extracting into skill reference files):

- The Scribble "Community Call Prep" report and Sai Kiran's community pointers: TX14 line 24851 (the best example of the marketing segment's raw input).
- The first-draft 14-slide HTML deck: TX14 line 24686 (the earlier structure with Proofly, X content, Coinfest, Algix, and speaker attributions).
- CC13 YouTube description with the final character-trimmed text: TX13 lines 10119, 10166, 10172.
- CC13 deck-update prompt and slide scripts: TX13 lines 9774, 9820, 10207 (TX13b lines 2004, 2032).
- The 24 Aug planning call transcript: TX13 line 6702.
- The 15-second answer to the host's zero-KMOI question: TX14 line 25999.

Memory notes worth bundling into a skill: `moi-weekly-comms-cadence.md`, `blog-distribution-is-part-of-done.md`, `moi-terminology-corrections.md`, `devnet-build-lag.md`.

---

## Rules and house style

1. One HTML file is the deck; fixed 1920x1080 stage; Poppins; MOI tokens; four backgrounds alternating; chip, one-accent `h2`, one component; three cards at most. (`moi-deck/SKILL.md`)
2. Use the same design as session 8, exactly. Do not introduce another design system (REQ 1332; TX14 line 24788).
3. The corner badge equals the page number; renumber after every insert or delete; cover and close have none.
4. Every number is supplied by a person or a named source. Never invent a figure, date, attendance, outcome or a guest's title.
5. Real photos only; empty frames that read their filename are acceptable; no stand-ins on an event slide.
6. Keep competitors, unresolved metrics and third-party enterprise stories off the community call. Evidence of what the user removed: the Lit Protocol comparison slide (REQ 1360), the campaign slide with the 0 CTR (TX14 line 25000; the CTR "needs investigation" in the source), Proofly and Algix/MeitY (REQ 1357), the trend arrows (REQ 1368), the guest (REQ 1369, 1376). The user gave no reason for any of these cuts; the pattern is (inferred).
7. The dev update is one or two slides; the new material gets the room (TX14 line 24851).
8. The closing slide is a logo and one line. No recap bullets, no "Open Q&A" line (REQ 1370, 1372).
9. Name the call "The Campfire Chat" on the title chip, with the tagline "Ideas. Updates. Community. Conversations." The earlier "Building in Public" branding is retired (REQ 1370; TX14 line 25251).
10. Say "devnet", not "Voyage devnet" (REQ 1375).
11. Script: complete spoken sentences, readable verbatim, no "not X, not Y", no applause lines, humanizer and stop-slop applied to all of it, slide-change cues explicit, notes identical to the script file, no em dashes.
12. Scripts only for the slides Adithya presents; slides by other speakers do not need his script (inferred from REQ 1371, 1374).
13. Terminology: participant-centric, MDAG, Sarva Labs builds and MOI Foundation governs, network ID (memory note).
14. Cap deck effort at about two hours when the content is already in hand (manager, 24 Aug).
15. Any content that could go stale (counts, "last Friday") must be refreshed or cut on the day.
16. Hand back with a list of what was left out and why (`build.md`); when the source is vague, the slide stays vague.
17. Stay local and read-only when auditing; no pushes or PRs without being asked (memory `no-push-no-notify.md`). The deck folders were untracked when written (the CC14 deck has since been merged, see the update in Deliverables); pushing is a separate ask.

---

## Traps

1. NOTES newline or comma error kills the deck's JS while the PDF still prints. Intro deck is still broken; CC14 was broken on 24 Sep and fixed.
2. Stray closing `</div>` (CC14 slide 10) re-parents slides 11 and 12 outside the scaled stage and strands slide 10's badge. The page count and `node --check` do not catch it.
3. Slide numbering off by one caused the wrong slide to be deleted: the badges were one behind the pages, so "rm slide 6" removed "What people ask AI about MOI" while the user meant the MOI vs Lit slide. Claude had to restore and swap (TX14 lines 24935, 25132, 25170). The skill rule "badge equals page number" exists because of this.
4. After removing slides, search for dangling references: slide 1 note ("what our campaign is doing"), slide 11 bullet and note (campaign click-through), slide 8 bullet and note ("MOI versus Lit Protocol", which the user may have meant to drop; Claude asked and got no answer, TX14 line 25170), slide 6 sentence with deltas after the arrows were removed.
5. Adjacent slides sharing a background after deletions (CC14 slides 7-8 and 9-10).
6. Figures from three places disagreed: Scribble report text (13.5% visibility, 1,187 citations, 639 mentions, ChatGPT 17%, Perplexity 17%, Gemini 6.4%), the later dashboard screenshot and typed figures (17.3%, 1,203, 650; 20, 19.1, 12.8), and an offhand "18%" from the user. Claude used the most precise and latest. The README still says "figures unchanged", which is wrong. Keep a numbers ledger with source and date.
7. Unsourced sentences carried between drafts: "the people we met there are the ones we are now bringing onto these calls" (from the Coinfest slide), "Nobody is asking about the parts we discuss internally", "so Claude is the room left to grow" (no Claude figure appears anywhere on the slides).
8. Teasers and promises in earlier materials (CC13 description: guests from Bali) outlive the plan.
9. Devnet may be behind the release: check the wire before saying "live" (memory `devnet-build-lag.md`); Claude raised this on 15, 23 and 25 Sep; the user's final instruction was "just say went live on devnet".
10. Stale README and duplicate variant files and PDFs: the guest variants are now identical; README says 13 slides.
11. Two copies of the script (HTML `NOTES` and `SCRIPT.md`) drift. Edit both in the same step.
12. `render.sh` and `build.md` disagree on multi-file naming; `render.sh` uses a shared `/tmp` file.
13. The skill points to a deck path that did not exist in the main checkout; the deck folders were untracked and existed only on this Mac (`DEPENDENCIES.md` section 19), so a lost laptop would lose both decks. Update, 13 October 2026: the CC14 deck is now in the GitHub repo; the intro-session deck is not recorded as merged.
14. Wikimedia logo fetches: wordmarks carry a stray box; wrong filenames return a 404 HTML page; check the file with `file --mime-type`.
15. Release time written as "12:00 AM UTC" was misread; use "00:00 UTC".
16. ~/Downloads may be unreadable to Claude's process (EPERM); move the file to `/tmp` or the repo first (CC13 sessions).
17. The CC13 deck was built outside the repo and updated through a pasted prompt; CC14 was the first call built in the HTML framework (inferred: the CC13 deck is a PDF named `MOI_Community_Call_13_PPTX.pdf` in `~/Downloads`). Do not assume a PPTX or other source file exists for CC13 in the repo.

---

## Open questions

Scheduling, hosting, promotion:

1. What day and time is the call? Thursday (memory, CC13) or Friday (CC14, inferred)? Local timezone of the audience? How long does it run?
2. Which platform is the public call on? Google Meet is named only in the deck README for presenting. Is there a webinar link, Luma event or Discord stage for the community call?
3. Who hosts and moderates? Who is the Slack author asking for planted questions and 15-second clips?
4. Who announces the call, on which channels, and with what copy? The pasted line "MOI Community Call #14 is happening tomorrow: The Campfire Chat..." suggests a marketing post; origin unknown.
5. Is the call added to the website's homepage calendar (`/admin/calendar`, `community_calls` table, failing in production at the time of writing)?
6. Is the rehearsal on Wednesday real for CC14?
7. Is the call recorded, uploaded to YouTube, and given a description with chapters for every edition? CC14 evidence is silent.

Content and numbers:

8. Who produced the first-draft HTML deck and who owns its content for each segment?
9. Which presenters take slides 5 to 11 (AI visibility through what is next) at CC14?
10. Are 47 queries, 5 engines, and 221 of 226 responses current? What is the fifth engine's number (Claude)? Is "12.8" correct for both ChatGPT's level and Gemini's movement?
11. Should the "MOI versus Lit Protocol" bullet on slide 8 and in its note stay?
12. Was devnet actually on v0.13.0 when the call ran?
13. Should Mohit Bansal and Krexa ever return? The assets are kept; his title was never supplied.
14. What is Scribble, who pays for it, and who can log in? Where is the Campaign Insight dashboard and who owns the CTR investigation?

Intro session:

15. When was it held, for whom, on what platform, and was it recorded?
16. Was it presented from the HTML or the PDF, given the broken script?
17. Did it get a Luma page, a blog, or social posts?

Housekeeping:

18. Should the skill and both deck folders be committed and pushed, and to which repo?
19. Should the two identical CC14 variant files be collapsed to one?

---

## Proposals for skills (not built from this note)

This section is a set of proposals, not a description of existing material: none of the reference files, scripts or templates listed here are in this repo. At the time of writing a skill called `moi-community-call` was available in Adithya's Claude setup; this note did not check whether it follows these proposals.

The research assistant recommended two skills and one fix.

### Skill 1: `moi-community-call` (new)

`SKILL.md` outline:

1. When to use: preparing, building, scripting, running or following up the monthly Community Call (The Campfire Chat).
2. The month's calendar: monthly, confirm day and time (open question), rehearsal the day before, two-hour cap on the deck.
3. Segments and speakers: protocol, DevRel, product, marketing, partnerships, close; who owns each; what to ask each owner for and by when (Wednesday lead).
4. Inputs checklist (see reference file) and "who to ask": protocol team for the release note, Sai Kiran for the Scribble report and community numbers, marketing for events.
5. Slide plan template: the CC14 order and the rule for what earns a slide.
6. Provenance rule: every number in a ledger with source, date, confirmed by.
7. What to leave off the public call (competitor benchmarks, unresolved metrics, unverified third-party claims, event outcomes without a source).
8. Hand off to `moi-deck` for build, then script, then checks.
9. Day-of runbook: Chrome, `P`, Meet share, the host's question cue, PDF fallback.
10. After the call: YouTube description, links, distribution (mark clearly as "confirm with Adithya" until the open questions are answered).
11. Hand-back format: what was left out and why.

`reference/` files to bundle:

- `segments-and-roles.md`: the segment order, speakers, memory-note cadence.
- `inputs-checklist.md`: per segment, the artifact, owner and where it arrives (Slack thread names, release note path).
- `cc14-worked-example.md`: the slide-by-slide source table above, plus the first-draft structure and the prune history.
- `numbers-ledger-template.csv`: columns `slide,figure,value,source,as_of,confirmed_by,status`; pre-filled from CC14 with the flagged ones (47, 5, 221 of 226, 12.8).
- `script-voice.md`: the rules under "Script" above with the exact user quotes; link to `community-call-14/SCRIPT.md` as the approved sample; the `PRESS NEXT` cue format from session 8.
- `release-slide-checks.md`: the per-package audit method, the "easy to forget" categories, the RC rule, the "live on devnet" check, the 00:00 UTC rule.
- `host-qa-prep.md`: how to answer a planted question in 15 seconds plus a second beat, with the zero-KMOI example and the "fuel only" trap.
- `youtube-description-template.md`: the CC13 structure (chapters first at 00:00, write-ups, upgrade lines, links, hashtags, 5,000-character limit, "Recorded [DATE]", teaser caution).
- `pruning-checklist.md`: after deleting a slide, search for dangling references; renumber badges; re-alternate backgrounds; update README, TITLES, NOTES, SCRIPT.md, and the by-name filename.

Scripts worth writing (put in the skill's `scripts/`):

- `check-deck.py <deck.html>`: (a) extract the script and run `node --check`; (b) parse the DOM and assert every `<section class="slide">` is a direct child of `#stage` and every `.slide-num` is inside its section (this catches the CC14 slide 10 defect; verified by DOM dump); (c) assert badge equals page number; (d) assert no two adjacent slides share a background class; (e) assert `TITLES` and `NOTES` lengths equal the slide count; (f) grep for stale phrases ("Voyage devnet", "Building in public", "Open Q&A", "Presenter: MOI Builders · Intro" when the deck is not an intro); (g) grep for em dashes in slide and notes text; (h) for each `NOTES` entry check it is present in `SCRIPT.md` when that file exists.
- `variant-diff.sh`: fail if the two variant HTML files are identical or if one is older than the other.
- `youtube-description.py <deck.html> --chapters`: draft the description from `TITLES` and the blog links, leaving `[__:__]` timestamps.
- `numbers-ledger-check.py`: compare the figures found in the deck's text with the ledger CSV, so a stale figure fails loudly.

Templates to bundle: a CC14-shaped deck skeleton (12 slides with empty text) copied from the fixed `index.html`, a `SCRIPT.md` skeleton with `PRESS NEXT` headers and a bracketed `[If the host asks ...]` cue, the YouTube description template, the numbers ledger CSV.

### Skill 2: `moi-builders-intro` (new, small) or a section of a general `moi-builders-session` skill

- When to use: preparing the Builders intro session with the Agent Launchpad demo.
- Study list: the launchpad source files named in `intro-session/deck/README.md`, the live `/api/stats` endpoint, the ten templates.
- Slide outline: the 11 slides and their jobs; the four-ideas slide wording with the participant-centric correction; the demo slide's four beats and the read-back-from-chain step.
- Demo runbook and pre-flight: wallet activation on devnet after resets, Telegram link, pm2 setup script, what to say if the wallet popup does not appear (unknown, to add).
- Claims checklist: do not say "Live on Voyage devnet"; do not present a grant as a launchpad feature; cut the v0.13.0 fee-payer line unless devnet runs it; do not quote live agent counts without refreshing.
- Reference: `intro-session/deck/index.html` as the worked example (after fixing the slide 4 `NOTES`), and the session 8 script format.

### Fix to the existing `moi-deck` skill

- Add the DOM nesting check from `check-deck.py` to `render.sh` and make it fail the render. At the time of writing `render.sh` passes the CC14 deck.
- Replace the hard-coded presenter title with the deck title in `template.html` and `new-deck.sh`.
- Replace "short sentences" with the user's actual preference in the Script section, and add the slide-change cue format.
- Fix the example path in "A deck to copy from" and add the deck folders to the repo, or say where they live.
- Make `render.sh` write its parse check to a `mktemp` file, and reconcile its multi-file naming with `build.md`.
- Add the "after deleting a slide" checklist and the background alternation rule to the verify step.
- Note in `SKILL.md` that two variant files that become identical should be collapsed.

---

## Known inconsistencies in these notes

These are places where this file disagrees with itself or with a sibling note. They are listed, not resolved. Line numbers refer to this file unless another file is named.

1. Hours spent on CC14: L129 says about 45 hours of wall clock between the first request (23 Sep 15:31 UTC) and the last script edit (25 Sep 12:37 UTC). L254 says the slow part was the user deciding what to cut "over about 30 hours" without saying which hours it counts. The two may measure different spans.
2. Coverage arithmetic: L213 and L214 give 47 queries across 5 engines and 221 of 226 responses; L259 notes that 47 x 5 is 235, not 226, and the deck does not explain the gap.
3. Number of engines: L213 says 5 engines, but L214 lists values for four (Perplexity, Gemini, Copilot, ChatGPT), L640 lists four engine logos, and L723 asks what the fifth engine's number (Claude) is.
4. The 12.8 figure: L214 gives ChatGPT's level as 12.8; the slide 6 sentence (L412) says Gemini is "up 12.8 points" and ChatGPT "slipped 4.3"; L260 flags this as possibly a slip. Using the older values at L692 (Gemini 6.4, ChatGPT 17) against the newer ones gives roughly 12.7 and 4.2, so the sentence does not match exactly either.
5. "Live on Voyage devnet": L451 quotes the release pack as "live on Voyage devnet since 11 September 2026", while the script rules at L403 and L674 say to write "devnet", never "Voyage devnet" (the user's instruction, REQ 1375).
6. Buffer: L526 says the Buffer pipeline creates drafts only and never publishes; `webinars-mature.md` (L435) says its Buffer tool schedules posts when given `--confirm` and saves drafts with `--draft`. They may be two different tools.
7. Rahul's role: L83 calls the person who set priorities on the 24 Aug call "the manager" (Rahul, inferred); L406 and L568 attribute the 14 Sep terminology corrections to "the founder"; `webinars-mature.md` (L44) records Rahul only as a reviewer. The notes do not say whether these labels name the same person.
8. Slide count of the CC14 deck: L37, L384 and L783 say 12 slides, while L297 records a browser check of "13 dots for 13 slides" on 24 Sep, and L335 and L696 say the README still says 13 slides (with the guest speaker). The guest slide was removed later, which explains the difference but is not stated in one place.
9. The "no guest" variant: L302 describes `index-no-guest.html` as cut from `index.html` by deleting the guest slide; L38 and L336 find the two files byte-identical (the guest was later removed from both); L738 asks whether to collapse them.
10. Intro-session agent counts: L576 uses `registered` (20 on 15 Sep) because `activeAgents` (22) overcounts, while the slide 9 note (L605) says "Eleven agents are listed right now". These may be different measures or a stale number.
11. Untracked decks: L105-L106, L309, L339, L681 and L699 describe the decks as untracked and only on Adithya's Mac. That is out of date for the CC14 deck (merged 13 October 2026, see the header).

---

## Glossary

Terms are defined as the MOI team uses them. "(as used in these notes)" marks the research assistant's reading, not an official definition.

- **AI visibility**: how often AI answer engines (ChatGPT, Perplexity, Gemini, Copilot) mention or cite MOI for a set of tracked questions.
- **Algix / MeitY**: a third-party enterprise tender story in the CC14 first draft, removed later (MeitY is India's electronics and IT ministry).
- **anu**: the atomic units of KMOI. **KMOI**: MOI's native asset; fuel is paid in it.
- **Campfire Chat**: the name of the community call from call 14 on (tagline "Ideas. Updates. Community. Conversations."); the earlier name was "Building in Public".
- **CC13 / CC14**: Community Call 13 (27 Aug 2026) and Community Call 14 (25 Sep 2026, inferred).
- **Coinfest Asia (Bali)**: an event whose guests were promised for CC14 in the CC13 description; dropped from the final CC14 deck.
- **CTR**: click-through rate, the share of people who click a link; the campaign's CTR was reported as 0 and "needs investigation".
- **Devnet**: MOI's test network, reset from time to time; it can lag the released protocol version.
- **EPERM**: the macOS "operation not permitted" error, seen when Claude's process tried to read a file in `~/Downloads`.
- **Fee delegation**: lets another account (the payer) pay the fuel for someone's interaction; it covers fuel only, and the payer signs each interaction separately.
- **Fuel**: what an interaction pays to run.
- **Futuremode**: the Taipei event (4 to 6 September) shown with real photos on CC14 slide 10.
- **Game Night**: the community game events run in Discord (the seventh run had 42 at peak, up from 20, per the draft).
- **Host (of the call)**: the person who moderates the call and may ask a planted question; not named in these notes.
- **humanizer / stop-slop**: Claude skills that strip AI-sounding patterns from text.
- **IOME**: a protocol change that affects validators, given its own CC13 slide; these notes do not explain it (as used in these notes).
- **Krexa**: the company of the removed CC14 guest (Mohit Bansal); not described in these notes.
- **Lit Protocol**: a third-party protocol; a "MOI vs Lit" comparison slide was cut from CC14.
- **MASN, notary exception, participant lists**: release-note details listed on slides 2 and 3 that these notes do not explain (as used in these notes).
- **MDAG**: MOI's structure used instead of a "per-account chain"; say MDAG, not per-account chain (as used in these notes).
- **Memory note**: a note in Claude's memory folder on Adithya's Mac; see the header.
- **moi-deck**: the Claude skill (in `~/.claude/skills/moi-deck/`) that builds the single-file HTML decks and PDFs.
- **Network ID**: MOI's term for what other chains call a chain ID; say network ID.
- **parseKmoi**: an SDK helper that converts KMOI amounts to anu; use it instead of calculating by hand.
- **Participant-centric**: MOI is participant-centric, not account-centric.
- **Pip**: a MOI community item listed as live in Discord on slide 9; what it does is not described in these notes (as used in these notes).
- **Planted question**: a question the host asks on purpose so the presenter can give a prepared answer, partly to produce short clips.
- **Presenter window**: the second browser window (opened with `P`) that shows the script, the next slide title and a clock.
- **Proofly**: a product presented by Prateek on CC13 and in the CC14 first draft; not described in these notes.
- **RC**: release candidate, a pre-release version; never present one as shipped.
- **Scribble**: the tool that produced the "Community Call Prep" AI visibility report; what it is, who pays and who can log in are open questions (as used in these notes).
- **Supabase**: the hosted database service behind the website's homepage calendar (`community_calls` table).
- **TITLES / NOTES arrays**: two lists inside the deck's HTML holding each slide's title and its presenter notes; one entry per slide.
- **TX13 / TX13b / TX14**: saved Claude Code session transcripts on Adithya's Mac (paths in the appendix).
- **Voyage**: MOI's explorer and dev tooling site; the user wants "devnet", not "Voyage devnet", in deck copy.
- **x402**: a web payment standard built on the HTTP 402 "Payment Required" status (as used in these notes).

---

## Appendix: Source transcripts

Full paths of the transcripts cited as TX13, TX13b and TX14. All are on Adithya's Mac and not in the repo.

- `TX14` = `~/.claude/projects/-Users-...-MOI-Webinars--claude-worktrees-relaxed-mccarthy-368dbc/58e97e8b-f23d-4b3d-aa62-d3ddefd7068b.jsonl` (the session that built the intro deck, the CC14 deck and the moi-deck skill; line numbers are jsonl lines, times are UTC).
- `TX13` = `~/.claude/projects/-Users-...-mw-MOI-Website--claude-worktrees-compare-repos-main-4ec89e/2aa9fad0-da96-4692-b568-37f1de9f7028.jsonl` (the session that prepared Community Call 13 and recorded the 24 Aug planning call).
- `TX13b` = `~/.claude/projects/-Users-...-mw-MOI-Website--claude-worktrees-compare-repos-main-4ec89e/f9be64ac-1d0f-4a0b-8482-53dbdbbed0cc.jsonl` (a later session in the same worktree that repeats the 24 and 27 Aug history at different line numbers; used for the Haiku audit result, the Buffer draft IDs and the deck-update prompt).
