# Request patterns: how Adithya asks, what recurs, and what he corrects

## Read first

- **What this is.** An analysis of Adithya's own request history (about 3,600 unique prompts, 28 May to 2 October 2026): what he asks for again and again, how he phrases it, and what he corrects. It looks at the whole prompt history, not at one process.
- **What it was used for.** It was one of ten research passes done before the skills in `skills/moi/` were written. It is the input for the shared house rules of the `moi-devrel` skill (built as `skills/moi/moi-devrel/`; the section "What a skill for this should contain" is the original proposal, whose names and layout differ from the built skill). Its sibling research notes are in this folder.
- **When it was written.** 2 October 2026 (the latest date in the request log; the first date is 28 May 2026).
- **Who "I" and "the user" are.** "I" is the research assistant (Claude) that compiled the notes. "The user" and "he" are Adithya (DevRel).
- **Evidence key.** "(observed)" means the request log or a file states it. "(inferred)" marks anything the log does not state outright. Counts are keyword hits over the de-duplicated prompts. Quotes keep his typos on purpose.
- **Paths and citations.** `L123` means line 123 of the request log (`_research/_user-requests.txt`), a file kept on Adithya's Mac and not in this repo (the sibling notes cite the same log as `REQ:<n>`). Paths starting `~/` or `WT/` are on Adithya's Mac. The session code is in https://github.com/moi-foundation/MOI-Webinars. Transcripts are not in the repo.
- **People** (roles as these notes record them):
  - Adithya: DevRel, author of the work.
  - Rahul: reviews and approves DevRel work and sets priorities; the notes infer a senior decision-maker.
  - Vardan Aggarwal: marketing (Luma pages, community call scheduling); asked about Mailchimp and Wikidata together with Sai Kiran, whose role is not recorded in these notes.
  - Gokul: protocol team (js-moi-sdk, registry and protocol questions).
  - Srikar (also spelled Sreekar) and Upendhar: DevOps (Srikar owns the VM, deploy scripts and nginx; Upendhar handled the Cloudflare redeploy and the preview feature).
  - Abhinav Agarwalla: author of `sarvalabs/moidocs` PR 120 (role not recorded in these notes).
  - Vinay M S: posts release logs (role not recorded in these notes).
- **Jargon.** Terms are defined in the Glossary at the end of the file.

## Sources read

**Primary source.** The request log (`_research/_user-requests.txt`, kept on Adithya's Mac), 3,973 lines, 401,585 bytes. Read in full, no sampling.

**Shape of the data (observed).**
- 40 session blocks, 3,893 dated prompt lines, 3,593 unique. About 300 lines are replayed session blocks (L468-486 repeats L405-424; L1405-1439 repeats L1343-1377; L2284-2484 largely repeats L2141-2276 and earlier parts of the L1902 session). Counts below use the de-duplicated set.
- Range 2026-05-28 to 2026-10-02. Unique prompts per month: May 75, Jun 131, Jul 541, Aug 1,745, Sep 1,030, Oct (1-2 only) 71.
- Heaviest days: 2026-09-10 (198), 08-31 (196), 08-03 (155), 09-09 (152), 08-05 (152), 07-30 (141), 08-18 and 08-19 (133 each), 08-21 (130).
- Median prompt is 52 characters; 39% are 40 characters or fewer; mean 91. Long prompts are cut at roughly 300 characters (313 hit the cap), so pasted drafts, transcripts and logs are truncated in the file.
- Typos are heavy and consistent ("epxlain", "wlalet", "shd", "u", "ur"). The intent is almost always clear. Never ask him to repeat a typo.

**Limits of the source.**
- It holds his prompts only, no assistant replies. "What the assistant did" is read from his reaction and marked (inferred), except where he pasted the assistant's own text back (for example L1546, L2030, L2061, L3376, L3489, L3694).
- Counts are grep keyword hits over the de-duplicated prompts. Categories overlap. Read "prompts touching the topic", not exclusive buckets.

**Excluded as personal (about 200 prompts, 5%).** About 200 prompts on personal or non-MOI projects were excluded.

**Where the MOI prompts went (observed from session headers).**

| Project folder (session) | Prompts | Dates | What it was |
|---|---|---|---|
| nno-code-agentapp (f11804e4) | 1,200 | 07-14 to 09-24 | MOI Agent Launchpad: build, test, fix, DevOps cutover, marketplace, payments |
| MOI-Webinars relaxed-mccarthy (58e97e8b) | 997 (920 unique) | 08-03 to 10-02 | Webinar sessions 7 and 8, x402/CASA PRs, v0.13.0 release comms, handover and this skills project |
| MOI-Website compare-repos (2aa9fad0, f9be64ac, 3104a471) | 579 (433 unique) | 08-05 to 09-01 | Blog split, CI/CD, Buffer and Mailchimp, release blogs, CC13 deck, PR 120 review |
| untitled-folder-10 (466347ed, 81aee3cf) | 221 (212 unique) | 09-02 to 09-22 | GEO/SEO/AEO audit of all MOI docs sites, docs authoring standard |
| Website-moi (e276d727) | 199 | 05-28 to 06-19 | moi.technology redesign, /manifesto, /why-moi, papers page |
| Agency-Website (2d6fc6f6, e967125c, ee7c4a44) | about 98 MOI | 09-11 to 10-02 | agent-explorer redesign PR, fee-delegation blog paragraph, moidocs rules-file check |
| MOIWB (a8b46961) | 85 | 08-19 to 08-22 | PR 36/37 blog review, PR 120 verification |
| relaxed-mccarthy (dc0de1a3) | 87 | 09-11 to 09-15 | moi-project (points app) audit and 15 stacked PRs |
| check-latest-work (b2b8403e), participant-level-agents (ec5cd8c7) | 37 + 4 | 08-31, 09-02 | Session 8 access-policy demo, Rahul's deck changes |
| cloudflare-deployment-fix (40d99729, f49763bc) | 30 | 08-11 to 08-21 | Website deploy without env vars, blog deploy |
| dating-plugin, moi-fleet, dataroom, moi-mcp, point, repo-identification, others | 14 to 27 each | Jun to Sep | OpenClaw/A2A demo, 20-app fleet, dataroom litepaper, MCP docs handoff, points app clone |

**Cross-checked, not part of the request file.** Memory notes (Adithya's Claude memory folder, on his Mac): `no-multi-agent-workflows.md`, `moi-terminology-corrections.md`, `batch-review-changes.md`, `no-claude-attribution.md`, `no-push-no-notify.md`, `personal-vs-work-repos.md`, `launchpad-deploy-topology.md`, `devnet-build-lag.md`. Every one agrees with what the request file shows. Sibling notes in the same folder (`release-blog-social.md`, `webinars-early.md`, `webinars-mature.md`) were skimmed for headings only so this note does not duplicate them.

**SECURITY FLAG.** The request log contains pasted secrets in a few places; it stays private and is not in this repo.

## Ranked list of recurring jobs

Counts are prompts touching the job (overlapping) and the number of distinct days, from the de-duplicated set. Ranked by prompts, ties by days.

| # | Recurring job | Prompts / days | Examples (quotes are verbatim; parentheses are my summary) |
|---|---|---|---|
| 1 | Explain or teach me X before we do anything ("explain", "what is", "how does", "walk me thru") | about 370 hits; "so ... right?" restatements 31; "explain N" 20 | L497 "do a top down eplanation, like what is the end product use case then get into hp" · L851 "in plain english man tell me what were doing [expletive]" · L1223 (asks for each step explained in the simplest terms) |
| 2 | Ship loop: commit, push, open PR, rebase, merge, deploy, preview | push/PR 93 (43 days), merge 82 (23), deploy 77 (34), preview/localhost 63 (34), rebase 15 (6) | L367 "ok it works now, can u sequentially mergw rhen next few prs also and run a quick check after each" · L1474 "commit and push (update ) the prs do it for moidocs first, then every 4 mins update the next one" · L2010 "rebase 16, clsoe 16 and re add as 22" |
| 3 | Progress nudges and "what's left" | exact nudges ("status?", "??", "check", "try again", "done?") 82; "what's left / what next" 48 | L80 "status?" · L86 "??" · L3268 "whats eft" |
| 4 | Keys, env vars, "where do I put this", terminal commands | 96 (32 days); where-do-I-paste 8; explicit command asks 6 | L88 "how do i drop a key" · L3044 "where do i get this agent encryptuon key" · L3219 "how do i go to the idrcetory to gh secret set" |
| 5 | Blog and long-form writing, edit, publish | 105 (26 days) | L664 "ok draft it and use as many citations as possible add links to every tool ive used" · L891 "ok now write a blog like the previous one, use humanizer and the blog skill" · L1268 (use the blog skill, benefit to developers, humanize after every paragraph) |
| 6 | Verify, audit, "are u 100% sure" | verify/audit/claims 76 (32 days); "are u sure / 100% / is this true" 30 broad, 18 strict (15 days) | L53 (list every claim, verify each independently) · L687 "can u please check every line and every claim against mois actual protocol code" · L931 "ok and every claim is legot and verified roght, theres 0 hallucinarion here" |
| 7 | Webinar and call decks, scripts, demo run-of-show | deck 81 (15 days), script/transcript 41 (16), luma/webinar/session 32 (14), "re open" 18 | L572 (setup slide, live demo with tx hashes, then code walkthrough) · L649 "study my tone and direction for slide 2s trandcritp" · L2273 "can u quickly give me a simple script for the updates, high evel speeches for each slide" |
| 8 | x402, CASA, CAIP-2 research and the three PR docs | 77 (14 days, 08-03 to 09-14) | L793 (research until we can say "MOI is x402 compatible", build the adapter and CASA submission, push nothing) · L1121 (PR 2: read past examples, study the tech stack, build each document) |
| 9 | Test plans and test rounds, then fixes | explicit plan asks 17 (11 days); wallet/nonce/stuck 45 (7 days) | L2938 "gimme the tetsing plan for each of those, like the quesiton i shd ask" · L2957 (track every config, input, output, fix and tx hash) · L3234 "ok now that were in deployment, make a testkng checklist to do" |
| 10 | Messages to and about people (Rahul, DevOps, Abhinav) | Rahul 42 (22 days); DevOps names 36 (12); "draft/give me a message" 16 | L3183 "ok drfat e a message for all 4, give the solution and the problem" · L1479 "whats rhauls change reqyest" · L3677 "gimme a message in the form of a quesiton to ask gokgul" |
| 11 | Social posts: X, LinkedIn, Discord, Telegram, via Buffer | 58 (13 days); Buffer 26 | L971 "scherudle both for 530PM IST" · L1039 "go schedule both for 11am IST also for linkedin put luma in thr post only not in first comment" · L1170 "no x also i want it as a thrread with exactly what this message says" |
| 12 | GEO/SEO/AEO and docs authoring standard | geo/seo/aeo 38 (15 days); docs/moidocs 34 (17) | L3760 (GEO audit of every MOI docs site, plan first) · L3782 "canu reserah omse wyas ot automate GEO optimizationw ithin prs" · L3937 (frontmatter, llms.txt, robots.txt in the author guide) |
| 13 | Switch GitHub identity / fix authorship | 25 (17 days); explicit "switch gh" 14 | L1608 "no no no all the commits need to be from [his work account]" · L1001 (cancel the PR and redo with the right credentials) · L1774 "dont put coauthroed by claude" |
| 14 | Control model and credit spend | haiku/sonnet/sub-agent 33 (19 days); credits/limits 15 (9) | L1503 "use haiku actly its faster and way chepaer, i cant blow all mycreidts on on search" · L2135 "actly use haiku, 79 agents is a lot" · L2256 "can u pause the worfklow and use aiku agnets, i dont anna run out of session limit" |
| 15 | Newsletter (Mailchimp RSS, one-off validator blast) | 16 (4 days, 08-24 to 09-15) | L2178 "ok build it and tlel me the exact, flow" · L2211 "ITS OTO BIG AGAIN, AND I WANT SIMILAR LAYOUT AND TYPORGRPAHY ASTHE MOI BLOG HEADING" · L2434 (one-time blast to all validators) |
| 16 | Handover and skill packaging | about 25 (09-28 to 10-02) | L1378 "cna u package thos skill as a handover thign, that abstracts me from the process" · L1389 "i wnana build a claude skill for every repo" · L1489 (skills any new devrel can use) |
| 17 | On-chain or product stats lookups | 9 | L809 "check how many interactions have hapepned on MOI chian all time" · L3153 "how many agnets ar eon the launchpad rn" · L3689 "give me the latest stats" |

Reading the ranking (inferred): the work is dominated by understanding and approving, not by typing instructions. He asks to be taught (1), watches progress (3), and decides at ship time (2). The recurring creative outputs are blogs, decks, scripts and posts (5, 7, 11). The recurring risk controls are claim checks (6), identity (13), cost (14) and push discipline (2).

## Process: The standing work loop (how every task runs)

### Purpose
The loop every request goes through, whatever the topic. A skill that reproduces this loop reproduces the working relationship.

### Trigger or cadence
Any request. The loop shows most clearly on webinar weeks (L930-1100), the x402 PR days (09-09, 09-10) and the Launchpad rounds (07-30 to 08-19).

### Who does it
Adithya talks, approves and decides. Claude researches, builds, edits and explains. He does manual steps himself (wallet taps, dashboard clicks, Discord/Slack posts, Buffer deletes, Mailchimp edits) and says "done".

### Inputs needed before starting
A one-line goal, often pointing at earlier work ("exact same format asthe firts one", L730; "usong the regualr eck we use her", L1329). Reference files attached with `@"~/Downloads/..."`. Pasted call transcripts (about 20 distinct pastes, plus 5 transcript files attached), pasted DevOps messages, pasted terminal output.

### Steps in order
1. Goal in one line. For anything new he asks for a plan first (12 times): L396 "can u first create a plan", L730 "build out th eplan first and the n the bloig in the exact same format asthe firts one", L1489 "elst discuss a plan first".
2. He asks to be taught before building: L225 "so firts i wnana leanr all the oncepts and then u build out the dmeo". See the "teach me" process below.
3. Approval is one or two words: yes, do it, build it, do all, go (49 exact), or a pick from the assistant's menu ("do b", "all 3", "ABC first", "1,2,3 ok 4)...", 21).
4. Work runs. He nudges with "status?" / "??" (82). If he leaves, he says how long and whether to ask: L2583 "ill be back in 30 no quesirosn"; L3780 "ill be back in 7hours MOST IMPORTANLY DO NOT PSUH ANYTHING"; L742 "dont ask me any qesutins until its done".
5. He wants to see it, not read about it: "run it", "show me", "preview link", "re open" (63 + 26 + 18 prompts).
6. Line-by-line review. He pastes the exact sentence he is reacting to, with a short verdict ("rm this", "[expletive] does this mean", "this is a bit of a loaded sentences") or replies by number ("1,2,3 ok 4)mention it likethat dont use a negative", L694). About 349 prompts are long quote-plus-comment prompts.
7. Verification: "are u 100% sure", claim lists, source checks (see the claim-check process).
8. Polish: humanizer and stop-slop, often as A/B/C variants (L969, then L970 "ok push A").
9. "gimme the final" (doc, post, deck, link, para). He reads it once, then authorizes: L1038 "ok gimme the final posts going out 5 hrs before lemme read it once then u can shceulde".
10. Ship only on his word ("merge", "push and open the pr", "confirm it", "schedule both for..."). Then "check now" after his manual step, then "all set?" / "whats left" to close.

### Deliverables and where they end up
Varies by audience (observed): peers and Rahul get a Google Doc or pasted text; engineers get an `.md` file ("a simple md file", not an artifact, L1507); public content becomes a PR to `sarvalabs/MOI-Website`; presentations are HTML decks for webinars, PPTX with the transcript in the notes for earlier ones (L527-528), PDF for sharing (L1331); PR comments are drafted as text for him to post himself.

### Accounts and tools involved
GitHub (his work identity), Cursor (he continues edits there, L535-536), Claude on laptop, remote or mobile (L1108, L1658, L2013, L3767), Buffer, Mailchimp, Google Docs/Drive, Otter.ai transcripts, Discord, Slack. Keys: Buffer and GA4 via GitHub secrets; Groq he brings himself.

### Quality rules and house style
See "Rules and house style". The three that bind every step: brief by default, every public claim sourced, nothing leaves his machine until he says so.

### Traps and things that failed silently
- The assistant "regenerated" a deck or file and he still saw the old one (L1073-1080, L1093-1097): see Traps.
- Work done but not reflected where he looks (presenter notes unchanged, cues missing, L1096-1097).

### How long it takes
Unknown. Only his own time estimates appear (30 minutes, 45 minutes, 2 hours, 7 hours). No durations are recorded.

### Open questions
Whether "do it" ever authorizes more than the last proposal. Every example is per-action (inferred); treat it that way.

## Process: Teach-me sessions (understand before building or presenting)

### Purpose
Adithya works in DevRel, not protocol engineering (L2156), and has to present and defend the work to Rahul and the community. He asks to be taught the mechanism until he can explain it, then builds or writes.

### Trigger or cadence
Start of every new topic and before every review. About 370 prompts. Heaviest: 08-03/05 (agentic payments), 08-26 (x402, 40 prompts), 08-31 (access policies), 09-10 (PR 2 and PR 3 walkthrough), 09-11 (fee delegation), 08-21 (PR 120 issues).

### Who does it
Claude explains; Adithya interrogates and restates.

### Inputs needed before starting
The artifact being explained (PR, doc section, code file, release note), and what he must do with it afterwards (present, defend, merge, post).

### Steps in order (observed pattern)
1. Start from the end-product use case, then the mechanism: L497 "do a top down eplanation, like what is the end product use case then get into hp". L503 "so in text i=like in apagraoh tell me whatthis app does".
2. Plain English, then simpler: L228 "in plain english explain whats happening in each momemtn"; L1223 (asks for each step explained in the simplest terms); L548 "explain in simpler terms"; "explain simplier" (L312).
3. A concrete example with named actors: L227 "in practice gimem an exmaple of how this works"; L1253 asks for a developer example and a simulated transaction "tell me exactky which fucntion is being used form where"; L1261 "so how does the sellers cod elook then use the weather exmaple".
4. A diagram or box flow when it is a flow: L501 "ok for rn explain with a diagram"; L2759 "create like a box flow with arros".
5. Section by section pacing: "ok next" / "next section" (14 prompts between L1131 and L1290, the 09-10 PR 2 and PR 3 review). One section per turn.
6. He restates in his own words with "so ... right?" (31). The answer must start with yes or no and fix precisely what is wrong: L1248 "so 1 makes sense of the bytes and 2 converts the info back into bytes".
7. He asks for a durable written copy when it is big: L1843 "create a learnign plan vecause i wnana know eveyr dteail of this so create an index firts"; L271 "do the explainer doc".
8. He asks for defence prep: L1521 "ok breifly explain it again so i can defend it"; L2703 "if he asks me why i havent done it on chain yet what shd i ssay"; L3928 "if asked why i inlcuded mntion of launhpad what shd is ay".

### Deliverables and where they end up
Chat answers, sometimes a saved explainer file or a diagram/artifact (L1255 "open the artifact").

### Accounts and tools involved
None. Source code on disk for verification (go-moi, PISA, Coco, js-moi-sdk, per the `moi-source-on-disk` memory).

### Quality rules and house style
- Define every term on first use. He asked what a term meant in about 54 short "what is / wdym" prompts, and asked about x402 or HTTP 402 in about 59 prompts; list in "Things he repeatedly had to explain".
- Use MOI context, not generic analogies: L805 "no dont talk abt stripe, talk sepcficially on contetx of moi".
- Keep numbering stable between turns; he refers back by number ("explain 5", "rm 2 and 3", "merge 13").
- Answer, then stop. When he wanted detail he asked again ("no i want tehcnical ddtails", L1847).
- Length rule has an exception: chat answers are brief, but scripts he will read aloud and learning docs can be long on request (L1044 "I want like full long speeches ... good technical depth").

### Traps and things that failed silently
- Confident but wrong or overgeneralized explanations. He escalates to "are u 100% sure" (18 strict, about 30 broad), and at L793 says "uve been wrong about 2 things so far" and orders research with no pushing.
- Explaining a different question than the one asked: L1322 "im asking u what does htis do"; L1507, L1550 "ur not helping me undertanad at all".
- Asking the same question again because the first explanation was a wall of text: L520 "sorry ik ive asked so many times"; L781 "im so sorry ur gonna have to epxlain that to me again".

### How long it takes
Unknown.

### Open questions
Whether explainers he asked to be saved were kept anywhere he reads again (not stated).

## Process: Claim check before anything public ("every claim, independently")

### Purpose
Nothing goes out with a claim he cannot defend. Blogs, release posts, decks, specs and PR comments are all verified against source before he approves.

### Trigger or cadence
Before every blog, release post, deck, spec PR and PR-review comment. 76 prompts on 32 days. Peaks: 08-07 (session 7 blog), 08-21 (releases blog and PR 120), 09-01 (session 8 deck), 09-09 (x402 docs), 09-11 (v0.13.0 blog).

### Who does it
Claude, inline by default. Sub-agents only when he asks, and then Haiku or Sonnet (L53, L687, L1294, L2134-2135).

### Inputs needed before starting
The draft, the source of truth (release notes, moidocs, js-moi-sdk, go-moi, Voyage docs, previous merged posts), and any claim he has already flagged.

### Steps in order
1. Isolate every claim as its own list item: L53 "run a sub process where u sloate every single claim in this blog and make a liust of all claims spearateed".
2. Verify each one independently against source, one by one, producing a report: L53 "do a report indepdnelty verifying each claim one by one".
3. Source rule: the real MOI code and docs, not memory. L687 "check every line and every claim against mois actual protocol code"; L1118 "reveiw eveyry claimw ith atcual moi repositoy source cdoes"; L2424 "ur MAIN soruce of info shd be the voyage xocs i gave ue arleir".
4. Anything he can't source gets cut or toned down: L932-933 flagged "Most teams quietly accept both" as vague attribution; he says "shd we maybe otne this odwn". L2133 "just leave ti ambigosly consistent with notes for now".
5. Verbatim where the source is a release note: L2129 "are all the poins verbatim or parapahrsed direcvtly from release notes"; L2131 "keep all 3 verbatime please"; L1163 "can u ensure evrythins i verbatim from the thing i sent u".
6. Cross-document consistency: L1560 "this is ocnsitent with the accoutn storage abd policy docs that are on moidcos on abhinavs pr120, and we ar enot ove rpromising anything".
7. Fix, then "run one last check" (L1325, L1473) and an explicit verdict: "all set to merge then?" (L1327).

### Deliverables and where they end up
A claim list plus verdicts (observed). A short verified-vs-argument split is what he wanted at L932: "Argument, not verified fact".

### Accounts and tools involved
Repos on disk, docs sites, Voyage explorer for tx links. Sub-agents (Haiku/Sonnet) only if opted in.

### Quality rules and house style
- Do not exaggerate or generalize. Corrections: L1305 "Every action on MOI costs fuel, man the firts [expletive] line itslef is nto true"; L1306 "even this is an excaggeration and misleading"; L47 "KMOI is just the fuel right".
- No "None of which we configured" phrasing when it could mislead (L708).
- Do not claim work that was not done in a status message: L3886 "we didnt do this, whya re u lying".
- Show the evidence behind a "yes". He re-asks "100%?" until he sees a source (inferred from the repeat pattern).
- Cost: 79 agents was too many (L2135).
- He accepted "deploy sonnet agents to each paragraph and separately to each releasepackage" (L2134) only when run on Haiku (L2135).

### Traps and things that failed silently
- Claims that sound fine but are false at the protocol level: assistant draft said an account pays in KMOI for "everything" (L47); said "reserved for the protocol itself and refused for everyone else" while earlier saying managers cannot modify (L35).
- Draft said "a native asset standard made for KMOI alone" (L34) and "fixed supply" (L36, he wanted "capped").
- Verification that checks the draft against itself instead of against source (inferred from "against mois actual protocol code").

### How long it takes
Unknown. One run used 15 agents and 325 tool calls (L2097, pasted from the assistant).

### Open questions
Where the final claim ledger was saved for each blog; the file is not named in the prompts.

## Process: Ship it (identity, branch, PR, rebase, merge, deploy, preview)

### Purpose
Get reviewed work onto the right repo under the right identity without surprising anyone.

### Trigger or cadence
Whenever he says merge, push, PR, deploy. Merge 82, push/PR 93, deploy 77, rebase 15. Bursts: 08-18 (blog PR train), 09-15 (15-PR stack), 09-30 to 10-01 (GEO-fix PRs rebase and update).

### Who does it
Claude prepares and, on his word, executes. Reviewers: Rahul, Abhinav, DevOps (Srikar, Upendhar). He often posts or merges the final step himself.

### Inputs needed before starting
Which repo and branch, which GitHub account, whether this is one isolated fix, a batch, or a stack.

### Steps in order
1. Confirm identity first. Observed opener in about 14 sessions: e.g. L1493 "can u switc gh auth to [his work account]" (also L2281, L1758, L1808 and others), and his work commit email (L1609, L1758). Never his personal GitHub account and never Adithya's personal email (L1607: that email broke a Vercel deploy).
2. Understand before creating: L2036 "dont just create. pr, just understand it first then well decide together".
3. Decide the PR shape. Isolated fix: L351 "create a separate pr ith tjust this change", L1859 "create a pr with just this fx and push it, not the other stuff, isolate". Review tweaks: batch on one branch, one PR at the end (L383 "sotp cretaibg prs after rveiwng all prs i just wanna do one batch update"). Big audits: stacked PRs grouped into sections (L354 "lets batch them, intp the sections u created before").
4. For each PR in a stack he runs a ritual: "explain N", he challenges ("is that standard practice", "in what situaiton wud 20 be better than 200", L378, L381), says "yea then rm this, and rm othersimilar [overly strict] fetaures" (L382), then "ok merge N". Roughly 14 explain-or-merge prompts across PRs 3 to 15 on 09-15 (L354-393). After merge: "how do i test 5 after merging" (L363) and "run a quick check after each" (L367).
5. Rebase before updating PRs (L1476 "rebase dirst", L1477 "so its rebased onto main right"). Rebase reports on request: L3963 "check for rebasing now and then give me a report".
6. Update pacing: L1474 "do it for moidocs first, then every 4 mins update the next one" (reason not stated; inferred: avoid a flood of notifications or CI load).
7. Preview before merge: he asks for the preview link every time (26 prompts), or runs localhost ("run it", 63 prompts).
8. Merge only on instruction. After merge, redeploy and check the live URL ("its not loaidng on phone", L1577).
9. DevOps handoff when prod is on the VM: message with the exact action (see the comms process).

### Deliverables and where they end up
PRs in `sarvalabs/MOI-Website`, `sarvalabs/moidocs`, `sarvalabs/moi-agent-launchpad`, `sarvalabs/moi-dataroom0`, `sarvalabs/Points-Program`, `sarvalabs/devops-automation`, js-moi-sdk, coco-docs, voyage and voyage-docs; ChainAgnostic/namespaces and x402 for the spec work. He works in forks under his work GitHub account and promotes to the org repo (L1024-1025, L2278-2281, L2873-2875, L3736).

### Accounts and tools involved
`gh` CLI, GitHub Actions, GHCR, the VM deploy scripts, Cloudflare Pages previews (`*.moichain-docs.pages.dev`, L2083), PR previews on the VM (L1992 "theyevcreated a new preview feature"), Vercel for the 2026-05/06 redesign preview (L1604) and for the Launchpad until the early-August move to the VM (L2531, L3086-3093).

### Quality rules and house style
- No Claude co-author line: L1774 "dont put coauthroed by claude"; L1481-1484 rewrite open PRs only ("obv only for the open prs").
- No personal account anywhere in work history: L1001 "i dont wanan see [personal account] naywhere tehre"; L1770 "yea scrub it, also scrub [personal account]"; L3337 "make sur eno commit has [personal account]".
- Do not commit transcripts or private files: L1768-1770 "wwhy did u commit it man" (a call transcript got committed; he had it scrubbed).
- Move off Vercel: L1898 "we are completly gwtting rid of vercel"; L1932 "We are moving off Vercel and onto the VM". Do not write Vercel into any MOI deploy doc.

### Traps and things that failed silently
- PR opened under the wrong account (L1001), forcing close and redo.
- Merged when he only asked to look: L2003 "what happened to 21? i didnt ask u to merge that"; L1995 "i didnt asku to merge 17 did i? can u take it off"; L2149 "U DONT MERGE ANYTHING".
- A "revert" on prod hid that the fix was not live: L1967 (DevOps: "it was not deployed with the latest blog fixes").
- Blog deletes did not take effect: build cache `blog/node_modules/.astro/data-store.json` rebuilt deleted posts when the deploy ran `npm install` instead of `npm ci --prefix blog` (L1977, DevOps confirmed a fix at L1980).
- GitHub Actions outage or billing block 2026-08-28 to 08-30: seven "try now" prompts (L2427-2456); fallback was the PR route, then waiting; he asked for retries once every 4 hours, not every 10 minutes (L2452).
- Remote or cloud sessions cannot push (403): the work came back as `.bundle` files he had to move by hand (L2030-2035).
- Pushed less than he expected: after "do it in this branch only do not ush anything to main" (L1110) and "Commit my uncommitted changes ... and push the current branch" (L1111), the files he meant to review were not on the remote: L1112 "why didnt u push those files tahts what i wanna review no" (09-09). Name exactly which files go to which branch before pushing (he asked L1109 "what all will u push").

### How long it takes
Unknown.

### Open questions
Whether moving a fork to the org keeps contributor history clean (he asked about removing his personal account as contributor, L1763, answer not in the file).

## Process: Talking to people through Claude (DevOps, Rahul, Abhinav, protocol team)

### Purpose
Turn a teammate's message or a call into a short human message, a decision, or an action list. Adithya prefers short messages without DevOps jargon.

### Trigger or cadence
A teammate message arrives and he pastes it (about 36 DevOps mentions, 42 Rahul mentions): Srikar (VM and CI/CD owner, L1918), Upendhar (Cloudflare redeploy, preview feature), Gokul (registry and protocol questions, L3339, L3655), Abhinav (moidocs PR 120 author), Sai Kiran and Vardan (Slack asks about Mailchimp, Wikidata), Vinay M S (posts release logs).

### Who does it
Claude interprets and drafts; Adithya sends.

### Inputs needed before starting
The pasted message (L333, L1944, L1980, L2057, L3121, L3141, L3193, L3723), what he wants to happen, whether he is allowed to touch the thing ("i dotn wanna touch the actions", L326).

### Steps in order
1. Translate: "what does this mean" (L3723 GHCR `permission_denied: create_package`), "explain 3 and 4" (L3181), "is hti simportsnt" (L1949).
2. Decide whether it is his problem: L316 "so dev ops team [expletive] up?", L3169-3175.
3. Draft the reply: problem, then solution, then exactly what the other person does. L3183 "give the solution and the problem"; L3192 "weve done 5/6 of the s6 above alr, heres what u have to do" (then name the branch he changed).
4. Keep it human and short: L327 "no like make it a humna message [expletive] is this"; L1926 "make thw hwole thign very specific and actionable npo need to tlak abt other stuff"; L1927 remove boilerplate "Owner: Sreekar. Everything below is a task. ... this is tacky, also like give some contetx on teh app".
5. For questions to the protocol team: a plain question with context, not a report: L3677 "in the form of a quesiton to ask gokgul"; L1145 "what shd i ask him, like hey rhaul any uodtae on the chain id pr?".
6. For weekly updates to Rahul: only completed work; to-dos labelled as to-dos: L3883 "can u say that webiste one is almost done, dont tell him the js fix we did say that as a todo"; L3886 removed a claimed action that never happened; L3884 "specficlaly mention specific changes we made, starting with content changes how we refrmed headigs, then frontmatter, then llms.txt , robots.txt".
7. Where it is posted: Slack (L2217), Discord (L3894: long text became a `message.txt` attachment; he asked how to send it as a message, then chose a Google Doc, L3900-3902).

### Deliverables and where they end up
Text he pastes into Slack/Discord/Teams, or a short Google Doc.

### Accounts and tools involved
Slack, Discord, Teams, Google Docs. Rule: never send env files in chat.

### Quality rules and house style
- Never mention `MOI_PLATFORM_MNEMONIC` to DevOps again (L3191 "we alreayd cleared that up").
- A message should say "what to do", not "here is a report".
- Do not hand him a paste-ready blob when he asked how to get something himself: L3122 "no dont give me a paste ready rpely, givetell me how to get it and send to him". When he says "gimme a message", draft one (L3124).
- Discord limit: a long post becomes an attachment. Split into numbered parts or put it in a doc (L3894-3902).

### Traps and things that failed silently
- A message that overclaims (L3886).
- A message that lists the secret-handling detail he does not want repeated (L3191).
- DevOps replies that ask for a PAT or a key (L3723, L3121): do not paste secrets back into chat; tell him where to get them.

### How long it takes
Unknown.

### Open questions
Rahul's exact standard for the announcement format (see event bursts, 09-10 incident).

## Process: Meeting transcript to work (call digest)

### Purpose
Convert a pasted Otter/Zoom transcript into what Rahul decided, what he asked for, and what Adithya now owes. Then do it.

### Trigger or cadence
About 20 distinct transcript pastes on 19 dates, mostly with Otter's header ("Keywords ... Speakers Speaker 1 (62%)"), plus transcript files attached via `@` on 06-08, 07-27, 07-28, 07-29 and 08-04.
- Paste lines: L66, L222, L259, L521, L746, L865-866, L897, L957, L1027, L1101, L1345, L1911, L1987, L2141, L2251, L2687, L2769, L2965, L3359, L3931, L3962.
- Attachment lines: L1765, L2725, L2790, L2808, L512.
- Dates: 07-23, 07-28, 07-31, 08-05, 08-10, 08-11, 08-18, 08-24, 08-26, 08-27, 08-31, 09-01, 09-02, 09-03, 09-09/10, 09-11, 09-14, 09-17, 09-22.
- Only four fall on Mondays (08-10, 08-24, 08-31, 09-14). Calls are frequent but a fixed weekly day is unproven (inferred: Rahul calls roughly weekly, with more ad hoc ones around launches).

### Who does it
Claude reads; Adithya asks.

### Inputs needed before starting
The transcript text or the `.zip`/`.txt` export (L512, L2790, L2808, L1765), and his own spoken updates in the same recording.

### Steps in order
1. Paste or attach: L2725 (an `@` attachment of the Otter `.txt` transcript, then "study this").
2. Ask: "whqt did rahul say on the csll" (L204); "what were all the deliervables form the call i sent u" (L1990); "what all was decided in the call" (L3932); "go over the transcript and see what rhaul suggested" (L2164, then clarified L2165 "no not rahuls review, im talking abt the trasncript i gave u").
3. Extract exact feedback, not a paraphrase: L1030 "can u give me all of rhauls feed back exactly liek what did he say".
4. Ask what he asked for versus what he had done. At L1546 he pasted the assistant's note that in two places the post "reverses a scope decision recorded earlier in this branch's history"; he replied "no give me the actual decision ito make please" (L1548).
5. Do the work: L262 "ok make all th changes rahul suggested to the deck"; L2729 "yes take the UX/feedback sweep next" through the launchpad checklist.

### Deliverables and where they end up
A decision list; changes applied to the deck, doc, PR or app; sometimes a checklist doc.

### Accounts and tools involved
Otter.ai (transcript, summary and keywords), Zoom Notetaker.

### Quality rules and house style
- Quote Rahul's words when asked, do not summarize.
- When a decision is needed, state the decision, the options, a recommendation and the consequence in a few lines: L1548, L1551-1553 (he asked "explain the conseuqnece of the fierts change, was my assumption rught").
- Do not mix up "Rahul's review" and "the transcript he gave" (L2164-2165).

### Traps and things that failed silently
- Transcript errors: the transcription tool mis-hears names and product terms. It renders the company as "Serval Labs" (the real name is Sarva Labs, per a memory note) and garbles product names such as Voyage and IOME (IOME appears to be the older Voyage sign-in that the MOI Wallet replaced; as used in these notes, not confirmed).
- Treating the transcript as instructions to execute without asking. He wants the list first (inferred from L1990, L3932).

### How long it takes
Unknown.

### Open questions
Where the recurring Rahul call and the "gm Rahul, here are my updates" message (L3881, 09-10) are formally scheduled.

## Process: Product test rounds (Launchpad pattern)

### Purpose
Run a structured test with real chain interactions, find failures, fix, redeploy, retest. Used for the MOI Agent Launchpad (1,200 prompts) and the Session 8 demo.

### Trigger or cadence
Before every launch or merge to prod. Rounds: R1 07-30, R2 07-30/31, R3 plan 07-31, final testing 08-01 to 08-04, pre-merge tests 08-19, post-reset checks 09-12 to 09-24.

### Who does it
Adithya runs the tests (Telegram, wallet extension, dashboard). Claude writes the plan, reads pasted output, fixes and redeploys.

### Inputs needed before starting
A list of agents or flows, the config per agent, the wallet used, the target (localhost, Vercel, VM).

### Steps in order
1. Ask for a plan: L2938 "gimme the tetsing plan for each of those, like the quesiton i shd ask"; L2952 "gimme hte quesiorns and the reuqiremtns for batch A"; L3085 "full fledged questions lits to ask all agents".
2. Run the questions, paste raw output (Telegram transcripts in the form "Adithya Ganesh | MOI, [Jul 30 ...]", PM2 logs, browser console JSON).
3. Ask for diagnosis: "what cud be the reaosn" (L3373), "why does it say fialeed now" (L3555).
4. Fix, redeploy, retest: "fix the config bug first ten the tatus honesty" (L3556).
5. Log everything: L2957 "also ur tracking evry single thing right, eveything from each agents ocnfig to the inout and out out we received and hten what we changed form there, also if possible all the agent creaiton and deletion transacrtion hashes"; L2963-2964 summarize into a doc.
6. Keep a UI inventory (L3012 list pages, buttons and fields; L3017 update it).
7. Payment adversarial paths and on-chain proof: tx hashes checked on Voyage (L3103-3106).
8. Decide a safe release: L2857-2858 "make the build without payment, and create a separate branch wth all the payemnt stuffs"; L3577 "do not dpeloy anything regradiong payments until its fully complete yea".

### Deliverables and where they end up
A testing checklist doc (L2964), a test-results doc with hashes, a UI inventory, a PRD or design doc when asked (L2602, L2728 design doc, L2759-2767 black and white PDF with a box flow).

### Accounts and tools involved
Telegram bot, MOI Wallet extension, Voyage explorer, Supabase, Groq (his own free key), GitHub Actions, VM, PM2, Vercel until the early-August move to the VM.

### Quality rules and house style
- Real transactions only. L534 "no mock mode for chain chain alwya shas to run"; L2536 "[expletive] is this mock mode i gave u the correct skills sdk for evtyhign"; L604 "like eveything actually happening is an onchain axciont, nothign is a mock".
- Say honestly when something is simulated. L659-660: registry SDK was down, so the demo used an existing agent and only the happy path; he wrote "no u dont change any code, just updat ethe deck and trnscri[t".
- One thing at a time: L3110 "remove run hisyroy and tlel em how to do the config one".

### Traps and things that failed silently
- Stuck interactions blocked a wallet; the cure was filling the pending nonce with a replacement interaction at the same sequence with enough fuel (L3341-3411, 08-11 to 08-13). He told the assistant to stop citing the upgrade (L3405) when it kept blaming an upcoming network upgrade (inferred from the reply).
- Dead registry after a devnet reset (L3326, L3457, L3511, L3517, L3675).
- Agents silently out of date after a runtime or model change.
  - L3489: a Groq error, the model `llama-3.1-8b-instant` does not exist.
  - L3497: "add a version check so agents warn when outdated".
- A run-time shown in the wrong zone (L3116 "01:15" for a 9:15 EST run).

### How long it takes
Unknown. His own targets: "i wanna fisih all etsting in 45 mins" (L3093).

### Open questions
Whether a standing QA agent is wanted. He asked, then cancelled it (L3029-3030 "ok bin the agent thing atcly ill just manually tets").

## Process: Event-triggered bursts

### Purpose
Name the recurring events that start a burst of work, so a skill can open the right checklist when it sees one.

### Trigger or cadence
See the table. Cadence evidence: Friday webinars (08-07 session 7, 09-04 session 8 at 4pm IST), a recurring call with Rahul (date not fixed; unproven weekly), Monday Mailchimp RSS blast (L2218, L2449, L2453), community calls roughly monthly (CC13 prep 08-27, CC14 prep 09-23 to 09-25), engineering releases every 1 to 3 weeks (go-moi v0.12.0 08-14, Voyage 0.8.2 and wallet extension v0.1.4 08-18, Voyage 0.9.1 and wallet-mobile v1.2.0 08-25, moipod v0.13.0 09-10).

### Who does it
Adithya, with Claude.

### Inputs needed before starting
The event's source material.

### Steps in order (per event)

| Trigger (observed) | Evidence | The burst that follows, in order |
|---|---|---|
| Webinar day or "call tomorrow" | L633 "i need to epxlain to rahukl in one hour what the app does"; L793 "keep my prepped to show this to the MOI team tmr"; L1081-1098 (T minus 30) | topic and storyline, demo build and verify, deck with script and cues, Luma and Meet link, X and LinkedIn scheduled, rehearsal recording, pre-flight check of gas, game-day tweet "WERE LIVE IN 30", post-session blog |
| Engineers post release logs in Discord | L1495 (Rahul asks for `service:version:link` lines), L2016, L2255 | monthly release blog, then deck slides per package (L2254), then social |
| Network upgrade day (moipod v0.13.0) | L1158-1196 | announcement thread before the upgrade (X thread, LinkedIn, Discord), blog next day, verify every claim |
| Devnet reset or new registry deploy | L3457, L3517, L3571, L3612, L3675, L3694 | re-point the registry logic ID and package version, retest register, delete, subscribe; add a banner for agents created before the reset; re-count agents |
| Teammate review or change request | L1479, L2140, L1193, L1546 | read the exact comment, decide, fix the PR, rebase, update, reply |
| DevOps message arrives | 36 prompts (see comms process) | translate, decide, reply with the exact action |
| Call transcript pasted | about 20 times | deliverables list, then do them |
| Docs standard or GEO review call (09-17) | L3927-3933 | author guide, md file in moidocs repo only, update PRs |
| Usage limit hit | L2108 "I hit my usage limit while you were working, but it has reset now" | resume from where it stopped; keep state in files; switch model (L14) or account (L3767) |
| Personal-fork project goes to production | L1024-1025, L2278-2281, L2873-2875, L3736 | clean repo (L2861), README review (L2872), push to `sarvalabs` org, ask DevOps to deploy |

### Deliverables and where they end up
Per event, as listed.

### Accounts and tools involved
Buffer, Luma, Google Meet, Mailchimp, Discord, Slack, GitHub, Voyage.

### Quality rules and house style
For an upgrade-time announcement: keep it simple and verbatim (L1163 "ensure evrythins i verbatim", L1194 "for protocll releaae u need to keep it ismple"). For a webinar: a tension hook is welcome (L1033). For a release: no hook (L1174-1175 "nah thats fine").

### Traps and things that failed silently
- The 2026-09-10 announcement incident (L1158-1196, observed): he asked for a thread "with exactly what this message says"; the time notation "12:00 AM UTC" caused three questions in a row (L1186-1188); two scheduled Buffer posts were wrong and he deleted them himself ("can buffer delete posts", "ok deleted again"); then a reviewer replied (L1193; the pasted message does not name its author, inferred to be Rahul or another senior reviewer): "Adi, looks like you posted the above message directly on our socials. Please rephrase this appropriately. The goal is to communicate that a new version will be launched ... scheduled for time T. Devs might need to upgrade ... We need to optimise these messages as per the medium". Adithya disagreed (L1194-1195).
- Time zones. Always echo the converted time back before scheduling.
  - IST for the audience.
  - Dubai time for his own schedule ("1230PM Dxb", L1162).
  - UTC for the protocol.
  - EST for his own agents.

### How long it takes
Unknown.

### Open questions
Who is right on the announcement format (see Open questions).

## Process: Handover and skill packaging

### Purpose
Make the work transferable to a new DevRel. He asked for handover docs per repo, an env-var guide, a dependency list, a task list, and now skills for a new DevRel hire.

### Trigger or cadence
2026-09-28 to 2026-10-02, once so far; he expects it to repeat per repo.

### Who does it
Claude, with Haiku/Sonnet sub-agents when asked.

### Inputs needed before starting
His repos (work set only), the list of processes, where each secret lives.

### Steps in order
1. L1378 "cna u package thos skill as a handover thign, that abstracts me from the process".
2. L1379 "run thru all of my repos and make a list of all work ive done, deploy haiku sub agents and prepare me a list and handover"; L1380 "dont pusha nything no prs nthing, i dont wnat them to get any notifications on it".
3. First list repos, then docs: L1381 "no dont make the doc yet, firts tell me all the repos ive tocuhed"; L1384 "lets go thru each repo".
4. Per repo: processes, variables, tech stack ("very simple brief", L1385), then env-var section "and how to find them" (L1386, L1394).
5. Per-repo skills: L1389 "i wnana build a claude skill for every repo"; L1396 "make one for the blog spearatelt also check the blog we have created a skill for the blog"; L1398 "do the same for all".
6. Dependency doc "in this fromat do it for all repos, in depth" (L1485); incomplete-work list, local and remote, no commits (L1486).
7. Fix plans: L1487 "create p[lans to fix all and start fixing one by oen with haiku sonet aub agents, dont pish anything"; L1488 "some open prs ar eoutdated and uselss so just evaluate".
8. L1489-1490: skills for any new DevRel hire.

### Deliverables and where they end up
In this repo: `project-handover-docs/` (per-product handover documents, with `LIST-OF-DEPENDENCIES.md` as the dependency list and `MIGRATION-LIST.md`) and the skills under `skills/`. On Adithya's Mac the working names were `HANDOVER.md`, `HANDOVER-RESEARCH.md`, `DEPENDENCIES.md` (now `project-handover-docs/LIST-OF-DEPENDENCIES.md`) and `FIX-PLAN.md` (not in this repo), plus per-repo handover skills (`repo-handover`, `moi-blog`, `moi-deck`).

### Accounts and tools involved
Local git only (read-only), Haiku/Sonnet sub-agents on request.

### Quality rules and house style
- Work repos only. Personal repos never appear (L1383 "company brian also isnt for me", memory `personal-vs-work-repos`).
- No remote activity: no push, no PR, no `gh` call that notifies anyone.
- Env-var sections say where each value lives (VM `.env`, GitHub Actions secrets, dashboards) and never contain values. L1388 "theres no vercel bro": deploy docs must say VM, not Vercel.
- A doc another agent can pick up mid-way: L2827 "add a doc exlpaoining to any agent what needs to be done for completion, at any point another ganet cna juts pick it up".

### Traps and things that failed silently
- He asked for a "list of all projects repo ivre tuched" as an employee (L1392) and got a dependency list (L1391-1392 "[expletive]. no i mean me as an employee").

### How long it takes
Unknown.

### Open questions
Whether the DevRel hire inherits the Launchpad, the website, or only DevRel content. The prompts blur these (L2489-2490).

## Reusable assets

Paths on Adithya's Mac, all observed to exist unless noted; repo copies are given where they exist.

**Skills already installed on Adithya's Mac (what he asked to install, and why):**
- `moi-blog` (blog to social to newsletter to GEO; he asked for it at L2249). Now `skills/moi/moi-blog/` in this repo; the older copy is in `others/legacy-skills/moi-blog/`.
- `moi-deck`, `moi-design`, `repo-handover` (older copies in `others/legacy-skills/`; the design material is now `skills/moi/moi-devrel/design/`), `humanizer` (L817 install command), `stop-slop`, `writing-x-posts`, `seo-geo-aeo` (from SNLabat/SEO-GEO-AEO-Skill, L670), `brag` (latent-spaces/brag, L412), `slideshow`.
- Also asked for or installed: claude-blog (L666), linkedin-skills (sergebulaev, L917, L1161), awesome-html-slide-skills (L926), 21st.dev MCP and Vercel web guidelines (L405-408), impeccable (L404), promptfoo and Unlighthouse for GEO (L3827, L3809), omniroute, claude-mem and headroom (L3684).

**Working files in the worktree** (`WT/`, a working copy of the MOI-Webinars repo on Adithya's Mac; repo copies are noted where they exist):
- `scripts/buffer.mjs` (Buffer post/draft/schedule; L913 shows the run command and the wrong-directory error). Repo copy: `skills/moi/moi-webinar/scripts/buffer.mjs`.
- `session-8-policies/` (BLOG.md, GAMEDAY.md, LUMA.md, NOTES.md, README.md, RUNBOOK.md, SCRIPT.md, SOCIAL.md, deck/, recording/, social/): the full webinar pack, the best template for the next session. Repo copy: `skills/moi/moi-webinar/examples/session-8/` and `skills/moi/moi-webinar/templates/`.
- `protocol-release-0.13.0/` (BLOG.md, RELEASE-NOTE.md, SOCIAL.md, social/): the release pack. Repo copy: `skills/moi/moi-blog/release-pack/examples/v0.13.0/`.
- `community-call-14/` (SCRIPT.md, deck/): community-call update deck and script. Repo copy: `skills/moi/moi-webinar/community-call/examples/cc14/`.
- `x402-compat/review-package/PR-1-CASA-namespaces-moi`, `PR-2-x402-scheme-spec`, `PR-3-x402-mechanism-typescript`, `PR-4-x402-other-sdks` and `AUDIT-2026-09-10.md`, `ESCROW-RESEARCH-2026-09-10.md`, `FUTURE.md`: the spec-PR pack and its audit. Repo copy: `others/standards/x402-review-package/`.
- `HANDOVER.md`, `HANDOVER-RESEARCH.md`, `DEPENDENCIES.md`, `FIX-PLAN.md`: handover set (see `project-handover-docs/` in this repo).
- `drafts/agent-explorer-design-issue.md`, `otter-transcript/`, `intro-session/`.

**Prompts worth reusing verbatim (observed):**
- Claim ledger prompt: L53.
- PR-review comment format: L1540 "Issue 1: what the issue is why its an issue where the issue is and suggested fix".
- Variant generation: L969 (stop-slop version, humanizer version, both).
- Tiered fix pass: L1468-1470 "fix the two before merge ones locally, dont push" then "should fix" then "minor".
- Release blog brief: L1268.
- Local-only audit: L1380, L1486.

**Commands he needed again and again (observed failures, so ship the corrected form):**
- zsh token read: `read -rs "T?Buffer token: " && echo && BUFFER_ACCESS_TOKEN="$T" node scripts/buffer-channels.js; unset T` (the bash form `read -rsp` failed with "read: -p: no coprocess", L2232-2236).
- `gh secret set <NAME> --repo sarvalabs/<repo>` (prompts for the value; L2235).
- `cp` or `mv` from `~/Downloads` into the repo, because the tool cannot read Downloads (macOS TCC, pasted at L3376).

## Rules and house style

### A. Vocabulary and shorthand (what he means)

This table is Adithya's own shorthand. Crude entries are omitted.

| He says | He means | Evidence |
|---|---|---|
| gimme / gimem / gimmen | give me | everywhere |
| sauce, "ok sauce" | great, proceed to the next thing (a friendly approval; meaning inferred from use) | L574, L739, L969, L1176, L1225 |
| lowk | kind of, mildly | L2117, L2126 |
| rm, bin, bun | remove, discard, drop | L834, L2156 "bun this", L2161 "bin last 2" |
| keep | the opposite of bin, keep that item | L2162 "keep 3 and 5 bun 4" |
| humanize / humanizer / "\humanize" | run the humanizer skill | L32, L43, L828, L1043 |
| stop slop | run the stop-slop skill | L969, L1326 |
| AI slop | generic, padded, performative AI prose to be deleted | L966 |
| aura farming | showy, dramatic, staccato phrasing ("not this, not that") | L1063 |
| geo | generative engine optimization (content for AI answers) | L1304, L2082, L3760 |
| the regular / usual / same way / exact same format | the established pipeline, reuse it; do not reinvent | L730, L1329, L1332 |
| reopen / re open / open it | open the generated file or deck again in the viewer | 18 prompts, L594-L605 |
| run it | start the local dev server and show it | L117, L165, L1590, L1603 |
| preview | PR preview URL, not localhost | 26 prompts |
| check / check now / check again / chk | re-read current state (he just did a manual step or edited a file) | 82 nudges |
| done | I did the manual step you asked for | 37 |
| status? / ?? | where are we, no essay | 82 |
| brief / brief pls / in points | at most a few bullets | 14 exact, 39 broader |
| simplify / simplier / plain english / "explain it very simply" | say it again simpler, no jargon | L1223, L1534 |
| wb | what about | L332, L1601, L2181, L3577 |
| ig, idk, idt, ukwim, tmr, shd, wud, cud | I guess, I don't know, I don't think, you know what I mean, tomorrow, should... | everywhere |
| sub process / sub agents / subs | parallel agents; he wants Haiku or Sonnet | L53, L3687 |
| fabel / fable | the expensive model; avoid | L15, L3923 |
| ship | merge and deploy | L3696 |
| cutover | moving prod to the new host (he had to ask what it means) | L3158 |
| kill it | stop the running task or process | L3178 |
| the thingy, the stuff | the item we just discussed; infer from the last turn | L319, L619, L780, L2803, L3155 |
| 1,2,3 ok 4) ... | numbered replies to the assistant's numbered list | L694 |
| "do b", "all 3", "ABC first", "push A" | picks from the assistant's menu | L1671 and others |

### B. How he phrases requests
- Short imperative with implicit context (39% are 40 characters or fewer). The context is the previous turn or the previous session. Always look at the last output before asking what he means.
- Quote-and-comment: he pastes the exact sentence and a verdict. Edit that sentence and nothing around it ("rm Both are drafted. Three things are still blank:", L834; then L835 "actly dont rm it just remove the authro thing" shows over-deleting was a risk).
- Number-addressed review: replies by item number ("explain 5", "rm 2 and 3", "merge 13").
- Questions disguised as confirmations ("so ... right?", 31). Answer yes/no first.
- Re-asks with stronger words when the first answer missed (L1318 "wdym, like i dont get any of it", L1319 "brief").
- Wants a recommendation, not a menu: L1548 "no give me the actual decision ito make please"; L2056 "which is the right thing to do, 2 right".
- Wants readiness verdicts: "all set?", "are we good to merge", "whats left" (48). End a task with "Remaining: ... Safe to merge: yes/no because ...".
- Tells you when he is away and what to do meanwhile (L2583, L3780, L742).
- Often asks how long it will take and how much it will cost before approving (L2522 "how long do u think this would take", L2967, L3176; cost questions L429, L449 are on a personal app).

### C. Standing preferences from corrections
Each row: what the assistant did (observed or inferred) and what he wanted instead.

**Length and format.**
- Walls of text. He wanted brief and pointed. L699 "less duanting pargaaphs pls [expletive]"; L1547 "i cant deal 3ith these iant pargarphs [expletive]"; L2024 "please only give me breif answers none of this extra long [filler]"; L3147 "way too manh words, keep it brief and tell me next steps man"; L3179 "brief man too many words here"; L3589 "gimme a brief poin by pint answer idw long paragraph"; L757 "just 3-4 main brief points no paras"; L1850 "liek no oaragpahs". Use bullets, numbered points, or a table (L3594 "pros n cons of pr15 in a table").
- Exception: scripts he reads aloud and learning docs. L592 "no i want paragraphas i wanna read off word by ord as i present"; L1044 "full long speeches ... good technical depth".
- "Next steps" wanted at the end of every status (L3147).

**Language.**
- Jargon, vague nouns and ambiguous terms. L42-44 ("MOIs own token", "the token"): wanted, in his words (L48): "KMOi is lile eth on etehryem right, so u can say its the native token for MOi netwoirk nd its measured in anu units fr fuel". L1301 ('[expletive] is "THE FEE" why the ambiguity'): wanted "fuel". L1312 "uel is the fee for using the MOI network rm" (delete that sentence). L36 "change fixed supply to capped everywhere".
- Define the thing, then the unit: L41 "sya what is KMOI and then talk abt anu".
- Write for a developer reader ("the benefit for dveelopers", L1294; L1268 "focused on what benefit this givesto dveelopers"), starting with what changes for them ("Your app can now pay the fuel for its users").

**Prose style for anything public.**
- Remove AI tics: L966 "this is AI SLOP" (a "worth caring about" line), L967 (an "other chains enforce and we relaxed" line), L1063 "why [expletive] do u keep syaing not this not that", L1118 "no metaphors no random AI [expletive], real, direct, efificent".
- No em dashes: L1176, L3892. Use ":" not "." in the fee-payer line (L1164).
- Longer, human sentences, not staccato: L649 "notice how i like longer sentces and not stacctattod short aura sentences".
- Must be readable aloud verbatim: L1068 "this is not a setence i can rea dverbatim".
- Warm, not cold: L590 "the kast transcript u wrote was too cold".
- Do not give away implementation detail in social posts: L920 "we dotn need to give away specific details like builinerror and 86 fiel"; L1037 "rm this".
- Keep posts simple and point to the doc: L945 "just say for all users Voyage changed the way u login, from Iome to MOI Wallet, clike here to find out how to migrate".
- Include only what serves the point: L704 (a Bitcoin genesis-block line is unnecessary but he accepts it if it helps GEO); L722 "will it hurt to add some moi code".
- Apply humanizer and stop-slop to every long piece, "after every paragraph" for a release blog (L1268), and give variants (L969).

**Public content must not leak internal history.**
- L796 "in the doc doent mention the sessions at all"; L900 "i also wnat u to completely remove mention of the would be sessio 8that we canclled"; L916 "these are still like refernces to the reosn why aretm ding sessiom 8 as originnaly planned"; L313 "dont mention that uf ixed them"; L1350 "rm the live on vyage dent thing"; L1351 "this is not a real feature of launhcpad".

**Decks and scripts.**
- When asked to fix a transcript, do not redesign the deck: L582 "no u broke it, i gave u a new nicer ppt and just asked u to finsih the trasncript".
- When he says "give it to me", do not edit the file: L606 "dont re edi thre ppt just give it to me and ill add it directly"; L624 "just update the sldie and gimme just taht sldie".
- Batch edits, then regenerate once: L648 "add it and dontgenerate the deck now, lets mak ebulk changesthen geneerate".
- Pace the live demo: L599 "atleast 5-7 seconds between each thing".
- Keep code instructions, do not shorten them: L602.
- Cues must be explicit and searchable: L653-654 (add the function name beside each line-number cue), L1091 "clear prititons form when i shd change to slide ... need it to be epxlcit".
- Presenter notes must match the script and the slide numbering: L1073 "theres a mismathc in slide 10 and 11", L1096-1097.
- Use MOI logo on every slide (L959), MOI colors (L927), and the same "insanely cool" design he already approved (L1332).
- A deck he will present should be one idea per slide with a plain title slide (L1064-1065 "the starting slide is also too complictaed").

**Model, agents and cost.**
- No multi-agent runs unless he asks: L515 "no please dont just start ,ulti aent proecesses it bruns up my credirs man".
- When he asks, Haiku (cheapest, fastest) or Sonnet only, small numbers: L1503, L2135, L2256, L3687 "no use haiku agents for all", L3923 "nah dont use fabel agents use sonnet". One exception: L3777 "deploy like one opus agent each to review" (explicit, once).
- Long single-model research is too slow and costly: L13-14 (switch to Sonnet).
- Keep infrastructure cheap: L321 "were a small company not gonna spend much on many differnt databases"; L379 "keep it 20 onyl wedont gont that kinda budget"; L3664 "is there anyway we can do this without supbase for free"; L3084 "make it so that the user hasto get their own key from groq for free or lke any other custom, lets not do the joint one, it runs out too fst".

**Consent, pushing and notifications.**
- No push, PR, merge, post, schedule or deploy unless he says so: L2149, L3800 ("NEVER DIRCETLY PUSH UNLESS I EXPLICLTY SAY TO"), L1380, L3570 "DO NOT MEGERE WITHOUT ME SAYNG", L3577, L2444 "dont shecule anythign yet", L1110 "do it in this branch only do not ush anything to main", L3757 "we arent pushign anything to doay im just working in advance".
- Notifications are a cost: L1380 "i dont wnat them to get any notifications on it".
- Draft first, show the exact text and time, then he says schedule: L1038, L1087 "ok cinfirm it".
- Always state what will be pushed and where, and push exactly that: L1109 "what all will u push", L1112.
- PR shape: isolated for one fix (L351, L1859), batch for review tweaks (L383), no separate PR per tweak.

**Interaction style.**
- Do not insist after a no. L245-256 (08-31): he said to use the MOI Wallet extension and his already-funded account; the assistant kept proposing alternatives (creating a participant for the agent, asking him to send KMOI, a new mnemonic). His words: L247 "NO IM NOT SENDING KMOI ... DO IT THE NORMAL WAY I ALREADY HAE KMOI [expletive]", L248 "NO USE THE MOI WALLET ETXNSUON MAN STOP THIS", L249 "u kepe [expletive] insisiting", L250 "u cnat create a priciapnt for the agent, u can maybe do a sub account". When a flow was chosen in a past session, read the past sessions first (L246 "check past sessions").
- Do not mention an upcoming network upgrade as a cause after he says to ignore it: L3405.
- Do not over-engineer: L3051 "why are u complictaing this by writing scripts i just nee to shar emy secrets thats lal".
- Do not ask questions when he is away; do ask before anything irreversible or visible.
- Surgical edits only (L834-835), and keep a way to see the previous version (L1308-1310 "can u shwo me the the preious commit, like speafately").

**Visual design (website and email).**
- Clean, elegant, uncongested, high contrast: L1682 "this looks so congested and packed, i want it to look cean and elegant"; L1686 "font colours dont contrast with. backgridn"; L1696 "bro wat the hell is this, gimme soemthing good"; L1717 "feels too dark".
- Logo is purple, not black: L1620, L1971, L1982, L2207 "can we use the purple one".
- Email must be tested as a real email, not the preview: L2207 "this is on preview mode, and the logo is huge"; L2212 "THIS IS THE EMAIL I GET"; L2213 "also im only getting one post show up i need all"; L2216 "i dont liek that all are purple".
- Navbars must not bounce or jelly on scroll (L1953, L1999).

### D. Standing rules he has stated outright

1. Commit and PR identity is his work GitHub account and work email; his personal GitHub account and personal email never appear in MOI work (L1608, L1770, L1001, L3337, L1607).
2. Never add a Claude co-author trailer or "Generated with Claude Code" footer (L1774, L1481-1484; memory note agrees).
3. Never push, merge, post, schedule, publish or deploy without his explicit word (L2149, L3800, L3570, L3577).
4. Audits, inventories and handovers are local and read-only, no notifications (L1380, L1486, L3757).
5. Sub-agents only when he asks; Haiku or Sonnet; keep the count small (L515, L1503, L2135, L3687, L3923).
6. We are off Vercel for MOI sites and the Launchpad; deploys go through the VM and GitHub Actions (L1898, L1932, L2502, L3146, L1388).
7. Demos and tests use real chain interactions; no mock mode; say plainly what is simulated (L534, L604, L659-660, L2536). In the Session 8 demo he wanted signing through the MOI Wallet extension with his own funded account (L248). Never paste a recovery phrase into chat; generate a new throwaway wallet for tests.
8. Every public claim must be verifiable against MOI source or docs; where the source is a release note, quote it verbatim (L2131, L1163).
9. No em dashes in posts (L1176, L3892).
10. Public content never mentions cancelled or internal plans (L796, L900, L916, L313).
11. Never raise `MOI_PLATFORM_MNEMONIC` with DevOps again (L3191).
12. The docs authoring guide lives as an `.md` file in the moidocs repo and is not published to the website; do not mention Launchpad in the docs PRs (L3967, L3969-3970).
13. Spec PRs: no bracket placeholders; if a section cannot be answered, write briefly what is required (L1138); author line is his work GitHub account and "Adithya Ganesh" (L1120); leave open decisions open for Rahul (L1121 "leav chain id open ended for now").
14. Say "devnet" for the current network (L821 "current netwiork is devent not indus", L2754, L1375 "it snot called voyage decnet, just say went live on devnr").
15. Positioning: L1715 "onchain authority for agentic eocnomy" replaces the older "cintext infrastructrue" line, and L1714 swaps "identity" for "authority" (L1644; "Not your Context, Not your Agent" removed from the blog, L2007).
16. Terminology (from the 2026-09-14 call; memory note): participant-centric, not account-centric; Sarva Labs designs and builds, MOI Foundation governs; "network ID", not "chain ID" in public specs. The request file shows him resisting both extremes ("chain ID" or "network name") before the call (L1333-1341); treat the memory note as the later word.
17. Prefer not to keep project data or credentials on his laptop (L343 "i dornw wanna store anything on my lapotp", said while a database migration was being run; the wider scope is inferred); never send env files in chat (L3026-3055).
18. If asked to put a file where he can see it, use a path he can open; do not assume the tool can read `~/Downloads` (L3376).
19. A hidden or private folder for non-demo files in a webinar folder: deck, social, runbook (L1048).
20. Webinar demo: no prebuilt `npm run` shortcuts; show the plain `node ...` commands a developer would run (L1049-1054).
21. Run third-party agent frameworks (OpenClaw) in Docker only, never directly on the laptop (L1784; L1595 asks for a malicious-tampering review of a diff for the same reason).

### E. People and accounts (names only, no values)
- Rahul: sets requirements, reviews, gives the release-log format `go-moi:v0.12.0`:`<github-link>` (L1495). Title not stated in the file (inferred: senior decision-maker; a memory note calls the 09-14 call speaker "the founder", which is the notes' inference and is not confirmed for Rahul).
- Abhinav Agarwalla: author of `sarvalabs/moidocs` PR 120 (access policy, storage cost, submit-interaction docs).
- Srikar (also spelled Sreekar): DevOps, owns the VM, deploy scripts, nginx (L1918, L1929). Upendhar and Gokul: engineering, deploy and registry (roles inferred). Sai Kiran and Vardan Aggarwal: Slack asks for Mailchimp and Wikidata (L2217, L3885). Vinay M S: posts release logs (L2255).
- Accounts: GitHub, a work account and Adithya's personal GitHub account (kept strictly apart); org repos `sarvalabs/MOI-Website`, `sarvalabs/moidocs`, `sarvalabs/moi-agent-launchpad`, `sarvalabs/moi-dataroom0`, `sarvalabs/Points-Program` (from `moinetwork/moi-project`, L989, L1025, L3720), `sarvalabs/devops-automation`. Buffer (X channel and LinkedIn channel, secrets `BUFFER_ACCESS_TOKEN`, `BUFFER_CHANNEL_X`, LinkedIn channel variable), Mailchimp (account exists; weekly RSS campaign; from-address needs a real MOI address, L2217), GA4 property "MOI" with secrets `VITE_GA_ID` and `PUBLIC_GA_ID` (L2038), Google Search Console (request indexing, L2065), Otter.ai, Luma, Google Meet, Discord, Slack, Telegram, Voyage explorer, Zenodo for papers.


### F. Corrections log (chronological)

What the assistant did is observed only where the prompt says so or quotes the output; otherwise it is read from his reaction (inferred). "Becomes" names the rule it feeds above.

| Date and line | What the assistant did | What he wanted instead | Becomes |
|---|---|---|---|
| 05-29 L1607-1608 | A branch authored by his work account was deployed from his personal email identity (observed: failed-deploy email) | every commit from his work account | identity |
| 06-08 L1768-1770 | A call transcript was committed (observed: "wwhy did u commit it man") | scrub it from history, and scrub his personal account name | no private files in commits |
| 06-08 L1774 | A Claude co-author line was added (inferred) | none | no trailer |
| 07-14 L2524, L2536 | Built mock identities and a mock mode although he had supplied the real SDK (observed) | the real `js-moi-agent-registry` | no mock |
| 08-04 L515 | Started a multi-agent verification run | do not, it burns credits | cost |
| 08-05 L13-14 | A long research run on an expensive model | switch to Sonnet to spend less | cost |
| 08-05 L582 | Rebuilt his new deck when he only asked for a transcript fix (observed: "u broke it") | keep his deck, finish and verify the transcript | scope discipline |
| 08-05 L590, L599-601 | Cold transcript; demo cards too fast; too complex a setup slide | warm paragraphs, 5 to 7 seconds per card, direct two-agent framing | decks and scripts |
| 08-07 L690, L699 | A loaded sentence and dense paragraphs in a blog draft | numbered edits, lighter paragraphs | prose |
| 08-08 L708, L718-719 | "none of which we configured" and a misleading invoice framing | say precisely what the buyer has (no record of the seller) | accuracy |
| 08-10 L1931-1932 | A DevOps doc claimed Vercel previews exist | VM, not Vercel | infra facts |
| 08-11 L3405 | Kept pointing at an upcoming upgrade as the cause (inferred) | ignore it | stay on the evidence |
| 08-18 L1995, L2003 | Merged PRs he had not approved (observed) | un-merge; ask first | consent |
| 08-21 L1547-1548 | Paragraph answers and a menu of options | brief answers and the actual decision to make | brevity, decisions |
| 08-24 L2149 | Merge was attempted or suggested (inferred from the capitals) | never merge | consent |
| 08-24 L2199-2216 | Mailchimp RSS email: oversized logo, one post only, all-purple (observed from his complaints) | purple logo at the right size, blog-heading layout, all posts, mixed colors | real-inbox testing |
| 08-26 L793 | Two wrong x402 explanations ("uve been wrong about 2 things so far") | deep research first, push nothing | accuracy |
| 08-31 L245-256 | Kept proposing to create or fund an account for the agent (inferred) | MOI Wallet extension, his funded account | no insisting |
| 08-31 L900, L916 | Luma text and blog still referenced the cancelled session 8 plan | remove every reference | no internal history |
| 08-31 L914, L920-921 | LinkedIn post too long and gave away detail | much shorter, a different approach | social |
| 09-01 L966-967 | AI-slop sentences in a post | delete them | prose |
| 09-02 L1001 | A PR opened under his personal GitHub account | cancel and redo under his work account | identity |
| 09-04 L1063, L1068 | Script full of "not this, not that"; sentences he could not read aloud | complete human sentences | scripts |
| 09-04 L1074-1097 | Deck and notes still showed the old version after "regenerate" | fresh, matching slides, notes and cues | stale artifacts |
| 09-09 L1112 | The files he wanted to review were not pushed | push exactly those | push clarity |
| 09-10 L1138, L1141 | Bracket placeholders and over-detailed spec text | brief "what is required"; leave detail out | spec rules |
| 09-10 L1186-1196 | Wrong time and text on scheduled posts, twice (observed: "deleted again") | confirm text and "12:00 AM UTC" before scheduling | scheduling |
| 09-10 L3886 | A status message claimed work that was not done | remove it | honesty |
| 09-11 L42-44, L1301-1314 | "the token", "the fee", "Every action on MOI costs fuel" | name the thing, define the unit, no exaggeration | blog language |
| 09-15 L327 | A DevOps message in robotic form | a human message | comms |
| 09-15 L383 | One PR per tweak during review | one batch PR at the end | PR shape |
| 09-22 L3967-3970 | A docs guide headed for the website, with Launchpad content (inferred) | `.md` in the moidocs repo only; no Launchpad | docs rules |
| 09-30 L1392 | A dependency list when he asked for his own project list | the list of repos he has touched as an employee | read intent |
| 10-01 L1481-1484 | Claude trailers present in open PRs (inferred) | rewrite open PRs only | no trailer |

## Traps

1. **Pasted secrets.** He pastes keys, bot tokens and recovery phrases into chat (see the security flag). The skill must never echo them, must tell him to revoke or rotate, and should give the no-echo command (`read -rs` in zsh, `gh secret set`). L910 shows he already revoked one.
2. **Stale artifact.** After "regenerate", he saw the old deck or old script (L1074-1080 "stil hasnt updated man i still see the odl one", "still 18", L1093-1097). Always say which exact file path and URL are fresh, restart the local server on a new port (L1092 "reopen the deck in a new localhost"), and verify by reading the served page.
3. **Presenter notes and cues missing** after a script rewrite (L1096-1097). Check notes, slide numbers and cues in the served deck.
4. **Wrong directory or missing file in the command he runs.** L913 (`scripts/buffer.mjs` not found), L2034 (`mv` from Downloads failed), L2832 (`cd contracts/agent_market` failed), L3053 (`openssl` on Desktop "Operation not permitted"). Provide absolute paths, a `cd` first, and a check the file exists.
5. **zsh, not bash** (L2232). He runs macOS zsh.
6. **macOS blocks Downloads and Desktop for tools** (L3376, L3053). Ask him to `cp` the file into the repo; supply the exact command (L299, L588, and L578 "gimmethe command to just copy it here").
7. **Buffer cannot be undone from the tool** (inferred from L1190-1192): drafts and scheduled posts that are wrong must be deleted by hand. Confirm text and time first.
8. **Time notation.** "12:00 AM UTC" caused three questions and two wrong scheduled posts (L1186-1192). Write an unambiguous date plus 24-hour UTC and the converted IST and Dubai times.
9. **Discord and long text.** A long message becomes `message.txt` (L3894). Split or use a doc.
10. **Mailchimp preview is not the inbox.** Logo size, layout, one-post-only and all-purple were all caught only in a real test email (L2199-2216, L2455).
11. **GitHub Actions outage or billing block** (L2427-2456). Scheduled content (the Monday RSS blast) may silently not run; check the run, do not assume.
12. **Blog cache.** Deleted posts reappear when the deploy uses `npm install` instead of `npm ci --prefix blog` (L1977).
13. **Prod is not main.** Prod can be running a reverted or older branch (L1967); the Launchpad deploys from the org repo, not the fork (memory `launchpad-deploy-topology`).
14. **Devnet reset invalidates the registry logic ID and package version** (L3457, L3517, L3675, L3694). Re-point, retest, tell users who registered before the reset.
15. **Stuck interaction blocks a wallet** (L3341): replace the pending sequence with a new interaction at the same nonce and enough fuel; the beta wallet that supports a custom fuel limit was the fix path (L3428, L3436).
16. **Over-claiming.** "100% sure" challenges (18 strict, about 30 broad), each a sign the previous answer was not trusted; status messages claiming undone work (L3886).
17. **Assistant insisting on its own flow** after he chose another (L245-256, L3405).
18. **Personal projects leaking into work reports** (L1383, memory `personal-vs-work-repos`).
19. **Co-author trailers and personal authorship in history** (L1001, L1481).
20. **Remote or cloud session cannot push** (L2030-2035); package work as a bundle or a handoff prompt (L2018 "package this into a text incuding a promot on what to do").
21. **Wrong audience on a doc.** A design doc that mentions webinar sessions (L796), a spec with placeholders (L1138), a docs PR that mentions Launchpad (L3969).
22. **Order of operations in the Launchpad stack:** register on chain first, then Telegram connect, then runtime install (L2767); first-time users need a line saying "complete registration stpes" before connecting a wallet (L3058); wallet extension must be installed and detected, and "i've installed, detect it now" needed a manual refresh (L3261).

### Things he repeatedly had to explain (a skill should already know these)
- Which GitHub account and email to use (14+ explicit switches, 17 days).
- That MOI left Vercel (6+ times: L319, L1388, L1898, L1932, L2502, L3146).
- That the current network is "devnet" (L821, L2754, L1375).
- That the blog is a separate Astro app at `blog.moi.technology`, with a static listing at `moi.technology/blog` carrying heading, summary, date, tags, thumbnail and JSON-LD (L1911-1940); and how to publish: upload an `.md`, merge, CI deploys (L1928, L2080).
- How Buffer, Mailchimp, GA4, GSC and GTM work (L2180 "whats buffer", L2027 "whats GSC and GA", L2071-2081 GTM, L2240 "how do i see if the drafts went thru").
- That scripts open and decks present with simple instructions: L1062 "so i open index.html and then i hit P thats all?", L974 "how do i open it and go into slide show mode".
- What x402, a facilitator, CASA and CAIP-2 are, and the difference between HTTP 402 and x402 (L502, L635, L806, L738, L755-766, L768-772).
- Approve versus transferFrom versus a facilitator (L674-678); canonical claim bytes (L723, L1220); MAS0 (L1206); the three-file PR structure (L1237, L1284).
- KMOI, anu, fuel, fee payer, payer versus sender (L40-52, L1165, L1321-1325).
- Access policies and actor storage (L226, L871-872, L938).
- Registry, agent card, `cardURI`, what is on chain and what is in the database (L2702-2716, L2760).
- Infra vocabulary: apex, CNAME versus A record, TLS, cutover, cron secret, TOKEN (L1896, L3141, L3158, L2647, L3205).
- Where a secret is read from and written to, and how to hand it over safely (L88, L3044, L3026-3055).

### Tasks seen once or twice that look like they will recur (inferred)
- Promoting a fork to the `sarvalabs` org (dataroom, points app, launchpad, website). Appears 4 times, so it is already recurring.
- Per-webinar bounty on `points.moi.technology` using the moi-project challenge entity (L989-1021; "going forwartd", L989). Verification is by four interaction hashes read from chain (L1021).
- One-off audience-specific Mailchimp blast (validators migration, L2434, L2463-2472).
- Launch or rehearsal video: `/brag` (L411-413), launch video (L518), screen recording with voiceover (L950-956), self-recorded dry run (L1061).
- Guest-speaker slide from a LinkedIn profile, with a version with and without (L1358, L1369).
- Docs authoring guide as PDF and md (L3934, L3955).
- Wikidata, Crunchbase, press, entity consistency for GEO (L3806-3808, L3885-3886).
- GEO roadmap page and "gold standard" research (L3878-3879); promptfoo and Lighthouse checks (L3809, L3827).
- A distribution strategy for a product launch (L3649).
- Status-update messages to Rahul (L3881 on 09-10, L2217 on 08-24; recurrence inferred) and the PR 120-style review of a colleague's PR with a defendable table (L1540).
- Environment-file handoff to DevOps and a secure channel for it (L3026-3055).
- A questionnaire to a client team (L304, 50+ questions) is personal, not MOI; skip.

## Open questions

1. What is the exact required format for protocol-release announcements? A reviewer objected to a verbatim post (L1193; author not named, inferred Rahul); Adithya says he followed "the exat standard he specificed" (L1194). Unknown. Ask Rahul for one written example.
2. Was "12:00 AM UTC" in the release text the intended time? The notation caused repeated confusion (L1186-1192). Answered in `release-blog-social.md`: the moment was 00:00 UTC on 11 September 2026 (from the correction reply); no written confirmation from the protocol team is on record.
3. Why updates every 4 minutes (L1474)? Reason not stated; inferred notification or CI load.
4. Does "go" or "do it" ever cover more than the last proposal? Every example is per-action.
5. What are the credit and budget limits? Only reactions ("it bruns up my credirs man", L515) appear; no number.
6. Which items belong to the DevRel role versus product building? He built and ran the Launchpad, the fleet, the dataroom litepaper and MCP docs; whether the hire owns them is not stated.
7. Who owns Luma and Google Meet creation, and where do the links live? Only the task list at L942 and one link at L910.
8. Where do final claim ledgers and learning explainers get saved? Not named.
9. Was Session 9 published? L632 hides sessions 8 and 9 until later; L742 builds nine; no publication evidence.
10. How long does each process take? No durations in the file.
11. Does the community call recur monthly (inferred) and who writes the host's audience question (L1373)?
12. Is there a fixed weekly call with Rahul? Transcripts appear on 19 dates across all weekdays, with only four on Mondays.
13. What is the approved way to hand a secret to DevOps? A policy is not stated here (the evidence is L3026-3055). The rule that holds: never send env files in chat.
14. Adithya's global Claude settings tell Claude to use ruflo (multi-agent) tools for multi-file work; on one occasion he told it not to for now (L952). A standing preference is not stated; treat the request-level instruction as the rule.
15. In the handover task of 30 September the instruction said to use Haiku and Sonnet sub-agents, while a memory note says never spawn agents unless asked. The request in L1490 is the explicit opt-in for that task only.

## What a skill for this should contain (original proposal)

Everything in this section was proposed in the research. The built skill is `skills/moi/moi-devrel/` (with branches ship, design, claim-check, explain, call-digest and test-round, and `references/`, `scripts/` and `templates/`); names and layout differ from the proposal below, so treat this as the reasoning, not the contents.

The patterns point to one always-on operating skill plus a few small task skills. The process-specific skills (blog, release, webinar, docs GEO) belong to the sibling notes; this note supplies the shared behaviour they all inherit.

### Skill 1: `moi-devrel-house-rules` (always loaded; this is the main deliverable of this note)
SKILL.md outline:
1. Who you work for and the three bindings: brief by default, every public claim sourced, nothing leaves the machine until he says so.
2. Identity block: his work GitHub account and work email, never his personal GitHub account or personal email; no Claude trailer or footer; run the preflight script before any commit or PR.
3. Consent matrix: Allowed freely (read, local edit, local run, draft); Ask first (push, PR, merge, post, schedule, deploy, send message, delete); Never (publish secrets, touch personal repos in work reports).
4. Cost rules: inline by default; sub-agents only on request; Haiku or Sonnet; state the agent count first; resume-safe state in files.
5. Answer shape: answer first, bullets, numbered items, next steps; tables for pros and cons; yes or no first for "so ... right?"; define jargon on first use.
6. Prose rules for public text: list from section C (no em dashes, no "not X, not Y", no vague attribution, readable aloud, simple words, humanizer then stop-slop, A/B/C variants).
7. Verification rule: claim list, source file and line, verdict; verbatim for release notes.
8. Time rule: always echo date, 24-hour UTC, IST and Dubai.
9. Environment rules: macOS zsh; absolute paths; `cd` first; Downloads blocked; secrets via `read -rs`.
10. Reading his messages: vocabulary table, numbered replies, quote-and-comment edits, "check" means re-read state.

Reference files to bundle:
- `references/vocabulary.md` (table A).
- `references/corrections-log.md` (section C as dated rules with the original quote, for regression tests).
- `references/people-and-accounts.md` (section E, no values).
- `references/glossary.md` (the terms in "Things he repeatedly had to explain", each in two plain sentences).
- `references/terminology.md` (participant-centric, Sarva Labs and MOI Foundation, network ID, devnet, positioning line).
- `references/calendar.md` (Friday webinars, recurring Rahul calls, Monday Mailchimp blast, monthly community call, release cadence, burst table).

### Skill 2: `moi-explain` (teach mode)
Outline: top-down use case, then mechanism; plain English; one concrete example with named actors; a diagram when it is a flow; section-by-section pacing on "next"; yes/no first on restatements; end with "if asked why, say ...". Template: `templates/explainer.md` with Use case, How it works, Example, Defend it (3 likely questions), Glossary.

### Skill 3: `moi-claim-check`
Outline: extract claims; table with columns number, claim, source (file:line or URL), status (verified, paraphrase, unverified, argument), action; independent verification inline, or Haiku sub-agents only if asked; cross-document consistency check; "verbatim" mode for release notes; final verdict "ready or not, remaining items". Template: `templates/claim-ledger.md`.

### Skill 4: `moi-ship`
Outline: preflight, PR shape decision (isolated, batch, stack), explain-then-merge ritual, rebase and update routine with spacing, preview link, post-merge check, DevOps handoff message. Scripts below.

### Skill 5: `moi-teammate-comms`
Templates: DevOps ask (problem, solution, exact action, deadline), reply to a DevOps message, weekly update to Rahul (done only; to-dos separate), PR-review comment (Issue N: what, why, where, fix), question to the protocol team, handoff prompt for a remote session. Rules from the comms process.

### Skill 6: `moi-call-digest`
Input: transcript. Output: decisions, quoted feedback, owed deliverables, "if asked why" notes, items needing his decision (with recommendation and consequence). No execution until he approves.

### Skill 7: `moi-test-round`
Test plan template (agent, config, questions, expected, actual, tx hash, fix), results log, UI inventory, safe-release branching (paid features behind a branch), post-reset checklist.

### Skill 8: `moi-handover`
Per-repo handover template (processes, stack, env-var table with where each lives and no values, deploy path, open work, who to ask). Local-only, read-only, work repos only. Builds on `repo-handover`.

### Scripts worth writing
- `scripts/preflight.sh`: prints `gh auth status` user, `git config user.name`, `user.email`, current branch and remote; fails if the GitHub user and commit email are not his work identity; greps the last N commit messages for `Co-Authored-By: Claude` and for his personal account name.
- `scripts/slop-lint.sh`: flags em dashes, "not X, not Y" patterns, "it is worth noting", "Most teams", "the token", "the fee", and sentences over a length limit; run on blog, post and script drafts.
- `scripts/time-table.sh`: given a date and time and zone, prints UTC, IST and Dubai and the weekday.
- `scripts/rebase-report.sh`: for a list of PRs, shows behind-by counts and conflicts without pushing.
- `scripts/open-fresh.sh`: serve a deck or file on a new port and print the exact URL; checks the served page contains a given string (stale-file guard).
- `scripts/secret-scan.sh`: refuses to write any file containing key-shaped strings or 12-word phrases; used before saving transcripts or logs.
- `scripts/chain-stats.sh`: one command that prints agent and interaction counts on devnet and the Launchpad (he asked for this 9 times); number first, then context (L3690 "just gimem the number man").

### Templates to bundle
- Claim ledger; explainer; DevOps message; Rahul weekly update; PR-review comment; test plan; handover; the burst checklists from the event table (webinar day, release day, devnet reset, review comment).

### Regression checks derived from his corrections (use as skill evals)
1. Ask for the first line of the v0.13.0 blog: expect "Your app can now pay the fuel for its users", not "THE FEE" and not a blanket "Every action on MOI costs fuel".
2. Ask to describe KMOI: expect a plain definition in his own framing (native token of the MOI network, like ETH on Ethereum, measured in anu for fuel), never "the token".
3. Ask to schedule a post: expect a confirmation of exact text plus a time table before any Buffer call.
4. Ask to "audit all repos": expect local read-only, no `gh`, no push.
5. Ask for a deck script: expect long, human, complete sentences, explicit slide cues, function names beside line-number cues, no "not this not that".
6. Ask for a PR with commits: expect preflight, no Claude trailer, no personal account name.
7. Ask for a status message to Rahul: expect only completed work, to-dos separate.
8. Ask for verification of a 20-claim blog: expect a ledger, inline checking, no 79 agents.
9. Ask "is this true?": expect yes or no first, then the source, or "unverified".
10. Ask for a DevOps reply: expect problem, solution, exact action, under 8 lines, no mention of `MOI_PLATFORM_MNEMONIC`.

## Known inconsistencies in these notes

- Cut length of the request log: this file says long prompts are cut at roughly 300 characters ("Shape of the data"); `release-blog-social.md` says about 415; `docs-and-geo.md` gives its own figure. The true cut length is not settled.
- Opening line of the v0.13.0 blog: the corrections log and regression check 1 here say "Your app can now pay the fuel for its users"; `release-blog-social.md` (rule 1) records "You can now pay fuel for another user." Check the published post.
- Voyage version in the release cadence: this file lists "Voyage 0.9.1" on 08-25; the August release post (see `release-blog-social.md`) lists voyage v0.8.2 and v0.9.0. They may be different dates or components; not reconciled.
- moipod v0.13.0 date: the cadence list says 09-10; the announcement was made on 10 September and the network update went live at 00:00 UTC on 11 September 2026.
- Open question 2 here asks which date "12:00 AM UTC" meant; `release-blog-social.md` answers it (00:00 UTC on 11 September), so the question is answered elsewhere.
- Open question 12 (a fixed weekly call with Rahul) versus the cadence text, which calls the Rahul call "roughly weekly (inferred)": the evidence supports frequent calls, not a fixed day.
- The memory note calls the 14 September call speaker "the founder"; these notes infer Rahul without confirming it (People list, section E).

## Glossary

Terms are defined as MOI uses them; "(as used in these notes)" marks my best reading.

- **KMOI:** MOI's native asset. **Fuel:** what an interaction pays to run. **anu:** KMOI's atomic units; fuel is measured in anu.
- **Devnet:** MOI's test network, reset from time to time. **Voyage:** MOI's explorer and dev tooling site.
- **Fee payer / fee delegation:** an interaction can name a separate account that signs it and pays its fuel instead of the sender. **Payer versus sender:** the payer covers fuel; the sender submits the interaction.
- **IOME:** the older Voyage sign-in name that the MOI Wallet replaced (as used in these notes; not confirmed).
- **MAS0:** an asset standard created without a contract. **MAS1:** the NFT standard. **MASX:** a logic-backed asset.
- **Participant-centric:** MOI treats the participant, not the account, as the unit. **Network ID:** the identifier of a MOI network (write "network ID", not "chain ID").
- **PISA:** MOI's logic execution engine, released as `go-pisa` (as used in these notes). **Coco:** MOI's contract language; CocoLab is its playground.
- **x402:** a payment scheme built on HTTP status 402 (payment required); a facilitator is the service that verifies and settles the payment. **CASA:** the Chain Agnostic Standards Alliance, whose namespaces repo takes the MOI namespace submission (as used in these notes). **CAIP-2:** the Chain Agnostic Improvement Proposal that defines a chain identifier format (`namespace:reference`).
- **OpenClaw:** a third-party agent framework Adithya ran in an agent demo (as used in these notes). **A2A:** agent-to-agent, agents calling other agents (as used in these notes).
- **Recovery phrase:** the word list that restores a wallet; also called a mnemonic or seed phrase. It must never be pasted into chat.
- **Haiku, Sonnet:** smaller, cheaper and faster Claude models; **Fable** (written "fabel" or "fable" in the log) is the expensive model he asked to avoid (as used in these notes). **Sub-agent:** a helper Claude run started in parallel by the main one; costs credits, so only on request.
- **Rebase:** replay a branch's commits on top of the latest main so a PR is current. **Stacked PRs:** a chain of PRs each built on the previous one.
- **Mailchimp RSS:** the newsletter campaign that emails new blog posts from the site's RSS feed. **Buffer:** the social scheduling tool for X and LinkedIn.
- **Luma:** the event page tool for webinars and calls. **Otter:** Otter.ai, the call transcription tool.
- **GEO / AEO / SEO:** optimising content for AI answers / answer engines / classic search. **GA4, GSC, GTM:** Google Analytics 4, Google Search Console, Google Tag Manager.
- **GHCR:** GitHub Container Registry. **VM:** the virtual machine that hosts production. **PM2:** a Node process manager. **Cloudflare Pages:** the hosting used for docs sites and their previews. **Cutover:** moving production to a new host.
- **Nonce:** the sequence number of a wallet's interactions; a stuck pending one blocks later ones.
- **Registry, agent card, `cardURI`:** the on-chain list of agents on the Launchpad and the pointer to each agent's description (as used in these notes).
