# MOI Builders developer webinars, sessions 7, 8, 8-policies and 9 (the mature format)

> **What this file is.** A research note on how one MOI Builders developer webinar is planned, built, rehearsed, delivered and written up, in the "mature" format. "Mature format" means sessions 7 onward (the early sessions 1 to 6 are in `webinars-early.md`). It covers session 7, session 8 (a design that was dropped), session 8-policies (the session that replaced it) and session 9 (planned, not delivered as written). Claude (an AI research assistant) compiled it from Adithya's work history to design a Claude skill for running a webinar. The last section proposes that skill (`moi-webinar`) and says which existing skills (`moi-deck`, `moi-blog`) it should hand off to. This file does not say whether `moi-webinar` was built.
>
> **When it was written.** September and October 2026. The evidence runs from 3 August 2026 to 15 September 2026.
>
> **Internal use only.** This note names internal reviewers and quotes internal feedback. Trap 13 below says reviewer names must be stripped from tracked files before they reach `main` of the public repo; the same applies here. Do not publish this file.
>
> **Who "I" and "the user" are.** "I" is the research assistant. "The user" is Adithya (DevRel at MOI), who built and presented the sessions.
>
> **Evidence key.** Anything without a tag was OBSERVED in a file, a commit or a request line. Anything the research assistant concluded is marked `(inferred)`. Gaps are marked `unknown` and repeated under "Open questions". No secret values are reproduced; variable names and where they live are named. Two secret leaks that happened in chat are mentioned as incidents only (see Traps).
>
> **Paths and citations.**
> - `REQ:<n>` cites line n of a request log kept on Adithya's Mac (`~/moi-devrel-skills/_research/_user-requests.txt`). It is not in this repo.
> - `WT` is Adithya's working copy of the webinar repo on his Mac: `~/MOI-Webinars/.claude/worktrees/relaxed-mccarthy-368dbc` (branch `claude/agent-payments-simple`). Repo paths below are relative to `WT` unless they start with `/`.
> - Paths starting `~/` or `WT/` are on Adithya's Mac. The session code is in https://github.com/moi-foundation/MOI-Webinars. Session transcripts are not in the repo.
> - Several documents named here (anything marked "gitignored", and the session 8, 8-policies and 9 folders, which were on a branch rather than `main`) exist only on Adithya's Mac. This is said once here and not repeated.
> - Commit hashes (for example `6a4de4e`) are from that repo's history.
>
> **People.**
> - Adithya: DevRel at MOI (the blog byline reads "Adithya Ganesh, Ecosystem, Sarva Labs"); does nearly all of the work, mostly through Claude Code.
> - Rahul: reviews and approves DevRel work and sets priorities. In these notes he receives the deck and the blog and supplied the narrative framing for session 8.
> - Ram: role not recorded in these notes. His feedback ended the first session-8 design.
> - "A lead" who ran the 4 August and 31 August calls: not named in these notes.
> - Not named here but relevant to the processes below: Vardan (marketing, Luma pages) and Chandra (owns the Buffer organisation).
>
> **Reading guide.** One "Process" section per stage (lifecycle, topic and storyline, demo build, run-of-show, deck and script, Luma page, social campaign, game day, rehearsal recording, blog, bounty), then reusable assets, rules and house style, traps, open questions, a proposal for the skill, known inconsistencies, a glossary of jargon, and an appendix listing the sources read.

---

## Process: One webinar session, end to end (the master lifecycle)

### Purpose
Turn one idea about MOI into five linked things: a verified live demo, a spoken talk with a deck, an event page and social campaign, a game-day plan, and a post-event blog. Each session also feeds a repo folder students can clone and a bounty. (`WT/README.md` series table; `WT/session-8-policies/GAMEDAY.md`)

### Trigger or cadence
- The trigger is a call with a lead, recorded and transcribed (Otter), whose transcript Adithya pastes into Claude. Session 7: the 4 Aug call (`WT/otter-transcript/…_summary.txt`; `WT/session-7/STORYLINE.md` line 7). Session 8-policies: the 31 Aug 9:47am call, titled "Refining Agent Demo and Access Policies", 7 min (`REQ:219-224`, `REQ:866`, `REQ:897`).
- Intended cadence is weekly on Fridays: `STORYLINE.md` says V1 "this Friday", V2 "+1", V3 "+2" (V1, V2 and V3 are the three phases of the series; this file ties V2 to session 8 and V3 to session 9 under "Traps" of the storyline process, and V1 to session 7 by inference). Actual: session 7 on Friday 7 Aug 2026 (inferred from `REQ:663` "were done sesh went great" dated 7 Aug), session 8-policies on Friday 4 Sep 2026 at 4:00pm IST (`WT/session-8-policies/LUMA.md`). Roughly monthly in practice (inferred).
- A topic is only valid if it fits one idea. The call that set the series said: "If you give everything in a single dev talk, everyone will lose it" (quoted in `STORYLINE.md` line 9).

### Who does it
- Adithya (ecosystem, Sarva Labs; the blog byline is "Adithya Ganesh, Ecosystem, Sarva Labs") does all of it, mostly through Claude Code in this worktree.
- Two reviewers appear by first name only:
  - **Rahul** reviews and approves DevRel work and sets priorities. In these notes he asked to receive the deck and the blog and supplied the narrative framing for session 8; his role is otherwise not recorded in these notes.
  - **Ram** (role not recorded in these notes) killed the first session-8 design, see below.
- Sub-agents were used twice, each on Adithya's explicit instruction:
  - Haiku agents for the 24 Aug build of sessions 8 and 9 (`REQ:731`, `REQ:742`).
  - Parallel readers for the 7 Aug protocol-claim verification (`REQ:687` "deploy a few agents if you wanna"; `factcheck-report.md` "three parallel readers").
- His rule otherwise: do not start multi-agent runs unprompted because they burn credits (`REQ:515`).

### Inputs needed before starting
A recorded call transcript or an explicit instruction from Rahul/Ram; the previous session's folder (each session is built by copying the previous one forward); a funded Voyage devnet wallet (faucet https://voyage.moi.technology); reference docs for the new mechanism (session 8: `sarvalabs/moidocs` PR 120, files `access-control.md`, `access-policy-tutorial.md`, per `NOTES.md` end).

### Steps, in the order they actually happened (session 8-policies, the cleanest example), with the document each step produces
1. **Call, then restate the ask.** Paste the transcript. Ask Claude to explain the plan and the demo "in plain English" before anything is built (`REQ:848-853`, `REQ:870`). Output: none in the repo.
2. **Write the storyline or the plan.** Session 7: `STORYLINE.md` (series arc, phase one/two/three, one "aha" per phase). Sessions 8 and 9 (first attempt): `PLAN.md` with options and a recommendation. Session 8-policies has no PLAN.md; its reasoning is in `NOTES.md` "Why the design changed".
3. **Read the sources, not memory.** "Read all webinar sessions and all MOI SDKs and docs to make sure you are up to speed" (`REQ:237`); read the docs PR as the reference (`REQ:224`); read installed packages before writing types (`session-9/PLAN.md` build step 2).
4. **Spike on devnet before building.** `scripts/spike-allowance.ts` (session 7/8/9) and `scripts/spike-policy.ts` (8-policies) prove or kill the mechanism first. `session-8/PLAN.md` §6: "Spike … on devnet before writing any agent code. If it doesn't behave, the whole plan changes."
5. **Build the demo and verify it live** (see "Process: Build and verify the demo"). Keep `NOTES.md` as a running log with interaction hashes.
6. **Write the event page copy and the pre-event social copy the same day the topic locks** (`LUMA.md`, `SOCIAL.md`, `social/*.txt`). For session 8, both were drafted on 31 Aug, five days before the event (file mtimes 08-31 08:16 to 10:15).
7. **Create the Luma page by hand**, plus the Google Meet link (see "Process: Event page and registration").
8. **Write the blog** with the blog skills, then humanizer and stop-slop, then a claim audit (see "Process: Post-session blog and social pack"). For session 7 this came after the live session; for session 8 it was drafted before and dated the event day (`BLOG.md` frontmatter `date: "2026-09-04"`).
9. **Build the deck and the spoken script** (see "Process: Deck and speaking script"). Send the deck and blog to Rahul; apply his narrative changes (`REQ:1029-1030`, `GAMEDAY.md` "Send Rahul the deck and the blog. He asked for both on the call.").
10. **Claim audit.** Every claim in blog, deck and posts is checked against docs, SDK source, and live receipts (`REQ:976-981`, `NOTES.md` "Claim audit, 1 Sept", `session-7/blog-assets/factcheck-report.md`).
11. **Schedule social through Buffer** (see "Process: Pre-event social campaign").
12. **Game day** (see "Process: Game day and live run").
13. **After:** push the recording and deck PDF, post the blog, open the bounty, repost (`GAMEDAY.md` "After"; session-7 `BLOG.md` footer comment: "Publish within 48h of the session; embed the session recording when live").

### What each document is for (the answer to "which documents, in what order")

| Doc | Written (observed order) | Audience | Job | Tracked in git? |
|---|---|---|---|---|
| `STORYLINE.md` (session-7 only) | first, from the 4 Aug call | Rahul (it was "sent out" for review) | series arc: one idea per phase, the aha per phase, language that must be exact, deliverables around each talk | gitignored (`WT/.gitignore`) |
| `PLAN.md` (8, 9) | before build | Adithya + reviewer | working title, what already exists, holes in the old design, design options with a recommendation, demo beats, "what must be proven live" checklist, build sequence, open questions | tracked |
| `NOTES.md` (8-policies) | during build | Adithya | build log: why the design changed, verified-live table with interaction hashes, live findings, dead ends, decisions | tracked |
| `README.md` | with the code | students cloning the repo | the idea in one paragraph, run commands, limits stated plainly, honesty guardrails, reading order of files | tracked |
| `EXPLAINER.md` (7) | with the code | non-engineers | plain-words version of the demo | tracked |
| `DEMO-PLAN.md` (7, 8, 9) | after the demo works | the presenter | live choreography: pre-flight, beats with "Say" blockquotes, timing, if-it-breaks table, things to say precisely | session-7 gitignored; 8 and 9 tracked |
| `TRANSCRIPT.md` (7) | after the deck | the presenter | pointer to the deck notes (the canonical script) plus what does not fit in notes: the pivot, the "say these precisely" list, likely questions, pre-flight | gitignored |
| `FACILITATOR-NOTE.md` (7) | in answer to one question | Rahul | one-off internal brief answering "can we still call it x402 without a facilitator?" | gitignored; stale (see Traps) |
| `RUNBOOK.md` (8-policies) | before the session | the presenter | timed run-of-show with slide ranges, what to say per block, likely questions, if-it-breaks table | gitignored |
| `GAMEDAY.md` (8-policies) | day before | the presenter | the checklist: tonight, T-60, T-10, running order, if something breaks, known state, after | tracked |
| `SCRIPT.md` (8-policies) | day before, rewritten on the day | the presenter | word-for-word speech, one block per slide, cues to switch window, "if the demo dies", "likely questions" | tracked; the deck's presenter notes are generated from it |
| `LUMA.md` | first marketing doc | the event page | paste-ready title, subtitle, description, practical table, repost blurb | gitignored |
| `SOCIAL.md` + `social/*.txt` | with `LUMA.md` | X and LinkedIn | first-draft pack, then one file per scheduled post | gitignored |
| `BLOG.md` | before (8) or after (7) the session | search engines, AI engines, developers | the canonical write-up, GEO-structured | tracked |
| `blog-assets/` (7) | with the blog | publishing | `PUBLISH.md`, `factcheck-report.md`, `social-pack.md`, `MEDIUM.md`, `schema.jsonld`, hero and chart | tracked |

"Gitignored" means the file never left Adithya's Mac. "Tracked" means it is committed on the branch, which is not the same as being on `main` (see Deliverables).

### Deliverables and where each ends up
Repo folder `WT/session-N/` on branch `claude/agent-payments-simple` (pushed to `origin`). On `origin/main` only session-7's `README.md`, `EXPLAINER.md` and `deck/` exist (read via `git ls-tree origin/main`); sessions 8, 8-policies, 9 and all blogs are branch-only (observed). Luma page, Google Meet, Buffer posts, Medium story, bounty form: external (see their processes).

### Accounts and tools involved
- Claude Code.
- Voyage devnet and faucet (no key; a funded mnemonic in `.env`).
- Luma (login, manual).
- Google Meet.
- Buffer (API key in `WT/.env` as `BUFFER_API_KEY`).
- Medium (login).
- Groq (`GROQ_API_KEY`, free): the "brains" of the session-7 agents and the text-to-speech voiceover.
- GitHub (`moi-foundation/MOI-Webinars`); gh auth must be the `sarvalabs-adithya` account (`REQ:978`, `REQ:1001`).

### Quality rules and house style
See "Rules and house style".

### How long it takes (from dates)
- Session 7: call 4 Aug; build spec, decisions handoff and first full build 4-5 Aug; deck and transcript reworked 5-7 Aug; live Fri 7 Aug; blog drafted and audited 7-8 Aug (about 25 blog commits, `git log`); Medium path decided 8 Aug. About 4 days to live, 1-2 more to publish.
- Session 8-policies: pivot call 31 Aug; demo verified end to end the same day (`NOTES.md` "Status: the demo runs end to end, 31 Aug"); luma, social, html deck, recording and voiceover all made 31 Aug (file mtimes); claim audit 1 Sep; Rahul's deck changes 2 Sep; game-day plan and full script 3 Sep; script rewrites and live 4 Sep; consolidating commit `6a4de4e` dated 9 Sep. About 4 days from pivot to live.
- Demo run time: 37 seconds standalone, plus about 7 seconds of narration pauses (`recording/demo.tape` comment).

### Traps
See "Traps". The biggest lifecycle trap: the first design for session 8 was built twice and thrown away (allowance on 24 Aug, context inheritance on 31 Aug morning) before Ram's feedback killed it; the pivot cost one day only because the spike-first habit exposed the holes early. `NOTES.md` calls shipping a known hole "with a line of narration covering it" "the actual mistake".

### Open questions
See "Open questions".

---

## Process: Choose the topic and write the storyline or plan

### Purpose
Fix the one idea, its aha, and what is deliberately not said yet.

### Trigger
A lead call (4 Aug for session 7; 31 Aug for session 8-policies). New session folder = copy of the previous one.

### Steps
1. Paste the call transcript to Claude and ask for the plan in plain English (`REQ:848-853`). Adithya rejects jargon repeatedly ("in plain english man tell me what were doing", `REQ:851`).
2. State the one-line story and the per-phase "aha". Pattern in `session-7/STORYLINE.md`: table of Phase | Dev talk | The idea | The "aha", then a story and an on-stage list per phase, then "language that must be exact".
3. Decide scope by subtraction: "the call landed on 'just do a value transfer' as the floor for V1"; V2 "deliberately deferred" the budget machinery until it is the point (`STORYLINE.md`).
4. For a build plan, write options with a recommendation and a fall-back (`session-8/PLAN.md` §3: Option A allowance, Option B budget logic, "If we have to pick one: A").
5. List what has to be proven live as a checkbox list (`session-8/PLAN.md` §5).
6. List open questions and send to the reviewer (`STORYLINE.md` "Open question for review"; `session-8/PLAN.md` §7).
7. When a reviewer rejects a design, keep the old build "intact … rather than deleted" and record why (`NOTES.md` "Why the design changed").

### Inputs, deliverables, tools
Inputs: call transcript, previous session, SDK and docs. Deliverable: `STORYLINE.md` or `PLAN.md` (or `NOTES.md` section). No external tool.

### Quality rules
- One idea per session; "Nothing before its turn" (`STORYLINE.md`).
- Say which phase this is and that the platform has a bigger scope coming (`STORYLINE.md` "Positioning").
- Each session builds on the last. In short: session 7 is about identity (who the agent is), session 8 adds authority (what the agent is allowed to do), session 9 adds a standard (x402). Slide 6 of the session-7 deck, which predates the move from context inheritance to access policies, shows "session 7, then 8 is 7 + context inheritance, then 9 is 8 + x402" (`REQ:655`, deck notes).
- Honesty guardrails are written before the build and constrain stage copy (`session-8/PLAN.md` §1).

### Traps
- Sessions 8 and 9 as planned (V2 allowance/context-inheritance, V3 x402) were superseded by session-8-policies. `session-9/PLAN.md`, `README.md` and `.env.example` still depend on session 8's allowance (`setup:authority`, `AGENT_ALLOWANCE`), and `session-9/BLOG.md` links to `/blog/agent-budget-on-chain-moi`, a post for a session that was not delivered. Anyone resuming session 9 must re-plan on the policies work.
- `STORYLINE.md` is stale against the build. It describes an older demo: a seller of books, "green in mock mode" (mock mode means a pretend run that does not touch the chain). The demo as built has no mock mode (Adithya: "no mock mode for chain, chain always has to run", `REQ:534`) and sells bitcoin probabilities.
- Reviewer rejection can land late. "Ram killed it on the 27th" (`NOTES.md`) and "Ram's phrasing on the 27th" (`README.md`) do not match the 31 Aug call evidence (`REQ:866`, `REQ:897`); unknown whether there was a separate call.

### Open questions
What is session 9 now? Who signs off a topic?

---

## Process: Build and verify the demo (the code standard)

### Purpose
Produce a demo that runs against the real devnet, cannot go green for the wrong reason, and is short enough to read on screen.

### Trigger
After the plan or storyline is agreed; before any marketing copy is final.

### Who
Adithya with Claude; Haiku sub-agents for the bulk 24 Aug build only.

### Inputs
Funded devnet mnemonic in `.env` (`USER_MNEMONIC`, `USER_DERIVATION_PATH`; agent path `AGENT_DERIVATION_PATH`); `GROQ_API_KEY` for sessions 7-9; Node (package.json says `>=20`); the previous session's `packages/shared`.

### Steps (the pattern, with exact commands)
1. **Scaffold from the previous session.** Copy the folder forward (`session-8: scaffold from session 7`, `git log`). Rename the headers. (Trap: `.env.example` headers in sessions 8 and 9 still say "MOI Builders #7".)
2. **Spike the mechanism alone.** Session 8-policies: `npm run spike:policy` runs create, read, update, delete of a policy (`scripts/spike-policy.ts`). Session 7/8/9: `npm run spike:allowance`. Header comment states what it proves or kills.
3. **Verify SDK claims live with throwaway keys.** `npm run verify-sdk` (`scripts/verify-sdk.ts`): "Every claim in SDK_NOTES.md marked VERIFIED LIVE is produced here", needs no funded wallet, reports `UNVERIFIABLE-WITHOUT-FUNDS` rather than assuming. 63 assertions in session 7 README.
4. **Write numbered setup scripts that are safe to run again (idempotent) and write ids back to `.env`.**
   - Session 7: `npm run setup:asset` (`00-setup-asset.ts`: creates MAS0 asset USDM, mints 100,000 to buyer, writes `SETTLEMENT_ASSET_ID`; reuses an existing asset and skips mint if funded), `npm run setup:registry` (`01-register-agents.ts`: writes `SELLER_AGENT_ID`, `BUYER_AGENT_ID`).
   - Session 8-policies: `npm run setup:fuel` (`00-fund-agent.ts`: owner creates the agent with `ParticipantCreate` and sends KMOI; tops up when below 6,000), `npm run setup:logic` (`01-deploy-ticker.ts`: `LogicFactory.deploy` with `RoutineOption({ storageFund: 6000 })`, writes `LOGIC_ID`; reuses existing). `.env` writing is done by `scripts/env-file.ts` `updateEnv`.
   - Compile the logic first: `coco compile` (not `coco build`, which is not a subcommand), needs a `coco.nut` beside the source (`ticker-logic/coco.nut`, coco 0.8.0).
5. **Write `preflight.ts`.** `npm run preflight`: reads only, spends nothing, checks in dependency order (RPC up, accounts exist, fuel, asset, registrations / policy RPC, `LOGIC_ID`), names the devnet-reset signature, prints "what to run next", exits non-zero on failure. Session-8 version probes `moi.AccessPolicies` for `-32601` to learn whether the node supports the feature without spending anything.
6. **Write the demo** (`demo.ts`): a banner per step (`banner`, `detail`, `ok`, `fail`, `say`, `summary` in `packages/shared/src/log.ts`), `DEMO_PAUSE_MS` for narration pace, an exit code that reflects pass or fail, and a summary box whose title flips to "DEMO DID NOT BEHAVE AS EXPECTED" on failure.
7. **Make the demo prove the right thing.** See "Quality rules" below.
8. **Adversarial suite.** Session 7/9: `npm run attack-test` forges payments and asserts each is rejected for its specific reason, plus an honest control "because a verifier that rejected everything would otherwise pass". Makes real transfers, so needs about 12 base units and minutes of time.
9. **Split the live demo into one small script per action.** Session 8-policies final form: `node scripts/tick.ts`, `node scripts/grant.ts`, `node scripts/revoke.ts`, `node scripts/policy.ts` (20-30 lines each), run with plain node "how a developer would normally" (`REQ:1049-1053`). `npm run demo` is kept as the rehearsal and the self-checking version.
10. **Record the receipts.** Put every interaction hash, fuel number and finding into `NOTES.md`; label which claims are doc-derived versus receipt-proven (`NOTES.md` "Claim audit, 1 Sept": two live tests added to convert "foreign reads need no policy" and "origin pinning excludes everyone else" from doc-derived to receipt-proven).
11. **Presentation mode for the editor.** `.vscode/settings.json` hides `deck`, `social`, `recording`, `*.md`, `.env`, and sets font size 18 (`REQ:1048`). `.vscode/` is gitignored at the root.
12. **Record a clean run** as the fallback (see "Process: Rehearsal recording and voiceover").

### Deliverables
Runnable folder; `.env.example`; `NOTES.md`; recording.

### Accounts and tools
- Voyage devnet RPC `https://dev.voyage-rpc.moi.technology/devnet/` (in `session-7/scripts/verify-sdk.ts`) and the faucet https://voyage.moi.technology.
- `js-moi-sdk` (^0.7.1 in sessions 7-9; ^0.8.0 in 8-policies), `js-moi-agent-registry` 0.1.1, `js-polo`.
- The `coco` 0.8.0 compiler.
- Groq (`GROQ_API_KEY`): the key is optional because there is a fallback (see Traps for why the fallback must not be demoed). The Groq model's name is not recorded in these notes.
- A funded mnemonic is needed.

### Quality rules (the standard)
- **Chain always real.** No mock mode: "no mock mode for chain, chain always has to run" (`REQ:534`); "the integrity of the demo is correct, everything is an onchain action, nothing is a mock" (`REQ:604`). Session 7 README: "No offline mode: every run settles on Voyage devnet."
- **Prove before building**: spike first (above).
- **MAS0 fails silently.** When a MAS0 transfer is refused (for example a payment pulled from an account that did not allow it), the chain still returns an interaction hash and no error. The only way to know what happened is to compare balances before and after (a "balance diff"). "Show balances, never receipts" (`session-8/README.md`, `session-9/DEMO-PLAN.md`, `spike-allowance.ts` header).
- **A refusal only counts for the right reason.** `isPolicyRefusal()` in `session-8-policies/scripts/demo.ts` requires the text `AccessError`; anything else prints "stopped, but NOT by a policy" and exits non-zero. Reason: an out-of-fuel agent and a forbidden agent look identical, and an early run showed beat 3 "passing" because the agent was broke (`NOTES.md`).
- **Guard the guard.** Pre-run balance check (`FUEL_LIMIT * 3`), and the guard was tested by forcing it: `FUEL_LIMIT=50000 npm run demo` must stop immediately. "A guard nobody has seen fire is not a guard." (`NOTES.md`)
- **Include an honest control** in any adversarial suite.
- **Self-heal leftovers** from a crashed run before beat 1 (leftover policy; leftover tampered registry entry, `session-7/scripts/_fix2.ts` retries restore four times).
- **Show failures that are not ours.** Rhythm: "happy path, then one refusal that isn't ours" (`session-8/PLAN.md` §4).
- **Small files on screen.** `identity-check.ts` 42 lines, shown whole without scrolling; `ticker.coco` 30 lines; `tick.ts` about 25 lines. "Only two pieces of this touch MOI" (session 7 deck slide 4). The README for session 7 lists "the seven files, in demo order".
- **Long "why" header comments** in every script (the code is read live and by students).
- **Models get judgment, code gets money** (session 7). Model output is clamped by arithmetic bounds computed in code (`pricing.ts`, `worth.ts`).
- **Measure, do not assume**: "5 questions x 5 runs each, zero drift, all four markets reachable" for the model called with the Groq key (model name not recorded in these notes) (`session-7/DEMO-PLAN.md`).
- **Numbers of record** in the demo cost sheet: refused write 86 fuel, permitted write 134, policy create/delete 100, deploy 719, ParticipantCreate 399 (`NOTES.md`); a full run costs 506 KMOI, agent 306 plus owner 200 (`GAMEDAY.md`; `RUNBOOK.md` says about 600).

### Traps (build-time)
- `insufficient funds` on a policy write is a balance problem, not fuel: 10,000 KMOI failed, about 109,000 worked, exact threshold unmeasured (`NOTES.md`, `README.md`). Give the owner about 100k KMOI.
- A fuel limit is checked against balance up front, so a high `FUEL_LIMIT` is rejected as insufficient funds (`NOTES.md`). Default 1500.
- `send()` without a `fuel_limit` runs a client-side fuel simulation, and a call the protocol would refuse throws before submission. The demo pins `fuel_limit` so the refusal happens on chain (`demo.ts`, `RUNBOOK.md` likely questions).
- You cannot MAS0-transfer to an address that does not exist ("account not found"). Create it with `ParticipantCreate`, minimum key weight 1000, and carry the opening balance in the same interaction (`NOTES.md`, `00-fund-agent.ts`).
- `LogicFactory.deploy` default storage fund is 1,000,000 (`DEFAULT_STORAGE_FUND`), more than a devnet wallet holds; override to about 6,000 (`01-deploy-ticker.ts`).
- Derivation path: the faucet path is `m/44'/6174'/7020'/0/0`, but the wallet-extension owner account used for session 8 was `m/44'/6174'/1'/0/0`; wrong path produced "account not found" everywhere (`NOTES.md` "Live findings"). `.env.example` still shows the 7020' path.
- Reading another account's balance needs the RPC (`moi.Balance`), not the asset driver, which returns empty for non-signers (`NOTES.md`).
- Devnet reset: accounts, asset ids, `LOGIC_ID`, agent registrations all vanish and the SDK says "account not found" (`preflight.ts` in every session).
- Registry: `getAllAgentIds()` reverts `MeterExhausted` at about 135 agents and the SDK returns `[]` instead of an error; code uses `getAgentsByOwner` (`session-7/scripts/showcase-discover-all.ts` header). Registry writes were also down on 7 Aug, forcing the pivot (see Deck process).
- Same-nonce stuck interactions needed manual unsticking (`session-7/scripts/_unstick2-tmp.ts`, `_replace2.ts`, `_fix2.ts`, and a 12 Aug handoff `REQ:3419`). Root cause `unknown`.
- Encoded runtime errors print as hex; `decodeRuntimeError()` in `packages/shared/src/chain.ts` lifts the ASCII so the refusal is readable on a projector.
- `node scripts/tick.ts` relies on Node running TypeScript directly; `engines` says `>=20`, which cannot do that (inferred; the author's shell was Node v24, `REQ:913`).

### Time
Session-8-policies demo built and verified in one day (31 Aug).

### Open questions
Is the `engines` floor wrong? Does the demo still run on devnet after the v0.13.0 network update (`REQ:1158`; Adithya's memory notes the devnet lags releases)?

---

## Process: Write the live run-of-show (DEMO-PLAN, RUNBOOK)

### Purpose
Give the presenter the choreography, timing, exact phrasing and recovery moves so the demo can be run without re-deriving anything.

### Trigger
Demo works end to end; deck exists or is being built.

### Inputs
A passing `npm run demo`; the list of beats; the failure modes seen while building.

### Steps (the skeleton shared by `session-7/DEMO-PLAN.md`, `session-8/DEMO-PLAN.md`, `session-9/DEMO-PLAN.md`)
1. **One line.** The idea in one sentence ("session 7's agent obeyed its limit. This one cannot disobey it"; "our agents stop speaking a private language").
2. **Pre-flight block** with exact commands (`cd session-N; npm install; npm run preflight; …; npm run demo` once as rehearsal; then `clear`).
3. **Window layout**: editor left, terminal right, both visible; 18-20pt font; about 100 columns (banners are 78 wide); `export DEMO_PAUSE_MS=1200`; no `.env` open; nothing with the mnemonic in the window title (`session-7/DEMO-PLAN.md`). Browser UI: `http://localhost:4000?gap=1200` (default 700; deck uses `?gap=7000`).
4. **Beats**, each with: the command, a "Read the output" table (point at / say), a quoted "Say" paragraph, and the line to land.
5. **Timing table** with a cut rule: "Cut beat 4 if short. Never beat 2." (`session-8/DEMO-PLAN.md`); "Beat 2 is the session. If short on time, cut 4, never 2." (`session-9/DEMO-PLAN.md`).
6. **If it breaks** table: Symptom | Cause | Say/do.
7. **Things to say precisely** (session 7) and **The three sentences** if only three things land.
8. Session 8-policies adds `RUNBOOK.md`: cumulative clock ("0:00 slides 2-6 WHY … 0:53 slide 18 + Q&A"), a block per slide range, "Likely questions, short answers", "If it breaks live". It is gitignored; `SCRIPT.md` is the tracked, definitive spoken text.

### Deliverables
`DEMO-PLAN.md` (and `RUNBOOK.md`) in the session folder.

### Quality rules
- "Show code, run it, read the output. Three loops of that, each one idea." (`session-7/DEMO-PLAN.md`)
- "Run first, explain after": do not open code before the audience has seen it work.
- Pause between cards: Adithya asked for 5-7 seconds so he can narrate (`REQ:599`); default became 6s per card (commit `9c736ad`), deck uses `?gap=7000`.
- "Never claim more than the screen shows." If the demo dies the session degrades to a talk with receipts (`RUNBOOK.md`).
- Exact-phrase list for honesty (see Rules).

### Traps
- Slide numbers in `RUNBOOK.md` and `GAMEDAY.md` are one off from the deck: the deck has 19 slides (`grep -c '<section class="slide' deck/index.html` gives 19; `TITLES` array has 19), the docs speak of 18 (RUNBOOK "60 minutes, 18 slides"; "slide 17 honest part", "slide 12 where the check happens", "slide 18 repo"). In the deck the check-location slide is 13, the receipt is 15, the honest-scope slide is 18, the close is 19.
- `session-7/DEMO-PLAN.md` points at a `RUNBOOK.md` that no longer exists (folded into README and gitignored in commit `f892c64`).
- `RUNBOOK.md` still prescribes `DEMO_PAUSE_MS=1500 npm run demo` as the live demo; `SCRIPT.md` runs the four per-beat scripts with plain node. The latter is what was presented (commit message of `6a4de4e`).
- Talk length disagrees: `SCRIPT.md` "about 30 minutes of talk including the demo", `GAMEDAY.md` "around 24 minutes without the demo", `RUNBOOK.md` "60 minutes, 18 slides". Luma says 60 minutes. Which was used live: `unknown`.

### Time
`unknown` per document; written within the same day as the build in session 8.

### Open questions
Is RUNBOOK meant to be superseded by GAMEDAY plus SCRIPT?

---

## Process: Deck and speaking script

### Purpose
A short deck whose speaker notes are the script, with explicit cues to switch to the browser, editor or terminal.

### Trigger
Demo built; storyline fixed. Session 7: 5 Aug. Session 8-policies: 31 Aug (first HTML deck), reworked 2-4 Sep.

### Who
Adithya writes or edits the style; Claude drafts and rewrites. Rahul reviews narrative.

### Inputs
- Brand source, session 7: a PowerPoint (`session-7/deck/MOI_Builders_S7-new.pptx`, 7 slides, then `MOI_Builders_S7new1f.pptx`, 8 slides, the one presented per `TRANSCRIPT.md`); palette sampled from `MOI_Builders_S5_2.pptx` (gitignored).
- Brand source, session 8-policies: a single-file HTML deck (`session-8-policies/deck/index.html`, 19 slides, 1920x1080, Poppins font, MOI tokens `--moi-main:#4B17E5`, `--moi-dark:#320F99`, `--moi-black:#0A0026`, lavender backgrounds).
- Skills used for the HTML deck: `ToseaAI/awesome-html-slide-skills` (`REQ:926`).
- MOI logo on every slide (`REQ:959`).

### Steps
1. Decide slide count small: "the slide deck doesn't need to be too long" (`REQ:575`); session 7 ended at 7-8 slides.
2. Slide 1 title must be uncomplicated (`REQ:1064-1065`). Slide 2 sets up the cast or the use case with a diagram (`REQ:574`).
3. Order the code slide by demo order: "explain every bit of the previous demo", first registry, then how it contacts the agent, then 402 (`REQ:618`); later cut to "only the files we are actually talking about" (`REQ:661`, commit `00fe08b`).
4. Put the honest-limits slide near the end ("Every guardrail here is self-imposed" in 7; "Honest scope" in 8).
5. Roadmap slide shows the series split (7, then 7+X, then +Y). Session 7 also has a bounty slide with the form link (`https://forms.gle/NToEMG47QHro9SiB8`).
6. Write the script per slide as paragraphs to read word for word. Cue grammar in session-7 notes: `[ DECK · slide 1 ]`, `[ >>> SWITCH TO BROWSER: http://localhost:4000 ]`, `[ FILE 1: open scripts/showcase-discover-all.ts ]`, `[ L22: const TAG = "sells-books" ]`, `[ point at … ]` (the originals use an em dash where these have a colon). Adithya asked for line numbers and function names together "so if the number fails I can just search the header" (`REQ:654`). Session 8-policies cue grammar in `SCRIPT.md`: banner `==== ## PRESS NEXT --> SLIDE N · title ====`, italic stage directions in parentheses `*(switch to Cursor, ticker.coco)*`, bold beat labels.
7. Generate the deck's presenter notes from the script: "Presenter notes are generated from SCRIPT.md, cues included, so the teleprompter and the printed script cannot drift" (commit message `6a4de4e`). The generator itself is not in the repo (`unknown`); the `moi-deck` skill now owns this (`~/.claude/skills/moi-deck/SKILL.md` step 4, `NOTES` array).
8. Open the presenter window with `P` (`index.html` `openPresenter`, keys: arrows, space, PageUp/PageDown, Home, End). Share the deck window in Meet, keep the presenter window private (`GAMEDAY.md` item 7).
9. Export PDF via print (`@page { size: 1920px 1080px }`), file `deck/MOI_Builders_S8.pdf`. A PDF does not keep animations (Adithya asked, `REQ:985`).
10. Humanize: run `humanizer` and `stop-slop` over the script, several rounds (`REQ:1043`, `REQ:1070`).
11. Rahul review: apply narrative changes to deck and notes (`REQ:1029-1030`); Adithya also asked for Rahul's feedback verbatim (`REQ:1030`).
12. Session 7 only: a deliberate "pivot" two days before the show. The registry SDK write path was down, so no new agents could be registered and tamper could not be restored; the deck and `TRANSCRIPT.md` were rewritten to use the pre-existing agents `agent_132` (seller) and `agent_133` (buyer), tag `sells-books`, product name "Probability Book Desk", happy path only, no tamper (`REQ:659-660`, `TRANSCRIPT.md`). Code was not changed; only deck and transcript. `agent_134` and tag `sells-signals` are retired and must never be said.

### Deliverables
`deck/index.html` (or `.pptx`), `deck/*.pdf`, `SCRIPT.md` (8) or notes in the pptx plus `TRANSCRIPT.md` (7).

### Accounts and tools
PowerPoint or a browser; headless Chrome for the PDF; no keys. Existing skill: `moi-deck`.

### Quality rules (voice), all from Adithya's corrections
- Warm and spoken, not cold: "the last transcript you wrote was too cold" (`REQ:590`).
- Paragraphs to read verbatim, not bullets (`REQ:592`).
- Longer sentences, not "staccato short aura sentences" (`REQ:649`).
- No "not this, not that" contrast constructions and no "aura farming": "just talk with complete sentences like a human giving a presentation" (`REQ:1063`).
- Each sentence must be speakable: "this is not a sentence I can read verbatim" (`REQ:1068`).
- Technical depth and a good walkthrough of the demo; full long speeches (`REQ:1044`).
- Explicit slide-change partitions in the file, not buried in a paragraph (`REQ:1091`).
- Simple for the listener: "everyone knows what a registry is, be direct" (`REQ:600`).
- Do not shrink the code instructions when simplifying (`REQ:602`).
- Say why the product is worth paying for before the hook (commit `f2c04e6`).
- Keep one canonical script: session 7's is the pptx notes; session 8's is `SCRIPT.md`.

### Traps
- Stale deck on screen: on 4 Sep Adithya reported the presenter notes "still unchanged", "still 18", "slide 10 and 11 transcript mismatch the slide", "none of the cues are there" in at least six messages in a row (`REQ:1073-1097`). Root cause `unknown` (inferred: regenerated file not reloaded, or served from another path). Rule for the skill: after regenerating, reopen the deck in a fresh tab and read slide 10's notes back before telling the user it is done.
- Slide numbers inside RUNBOOK/GAMEDAY drift when slides are inserted.
- The pptx note on session-7 slide 5 says `MAX_PRICE_PER_ANSWER=999999 npm run ask …`: run the command first, then talk over the slide.
- A pptx edited by hand cannot be regenerated: `deck/README.md` "there is no generator; regenerating would overwrite hand-made design and pasted notes."
- `recording/vo/01.txt` shows mojibake ("â" for an em dash).

### Time
Session 8: first deck 31 Aug; final script and notes 4 Sep.

### Open questions
Where is the SCRIPT-to-notes generator? Was PDF or HTML shared with attendees?

---

## Process: Event page and registration (Luma)

### Purpose
A public registration page and a joinable meeting.

### Trigger
Topic locked; date and time agreed. Session 8: drafted 31 Aug, page link `https://luma.com/g0bmqt8p` in use by 31 Aug (`REQ:910`).

### Who
Claude drafts `LUMA.md`; Adithya pastes it into Luma by hand. There is no Luma automation. Adithya asked in chat whether a Claude Code Luma MCP or skill existed, then withdrew the question ("nvm its not luma plus", `REQ:902-903`). (inferred) He meant that the Luma API needs a paid plan.

### Inputs
Date, time zone, duration, repo URL, prerequisites.

### Steps
1. Draft `LUMA.md` in the fixed shape (observed in `session-8-policies/LUMA.md`):
   - **Title**: `MOI Builders #N: <outcome in plain words>`; two flatter alternates below it.
   - **Subtitle**: one question or line.
   - **Description**: hook paragraph(s) in short sentences, "What we will cover" (five bullets), "Bring" (Node 20 or newer; a devnet wallet funded at voyage.moi.technology; code at github.com/moi-foundation/MOI-Webinars), "One honest note" (the limits, said up front).
   - **Practical** table: Date (Friday 4 September 2026), Time (4:00pm IST = 10:30 UTC), Duration 60 minutes, Format "Live, online. Free", Page.
   - **Short version, for a repost**: three short lines ending "Friday. Free."
2. Shorten and humanize the description (`REQ:901` "shorten the luma and run humanizer").
3. Create the Luma event manually, with the Google Meet link ("4) Luma + Google meeting link", `REQ:942`).
4. Confirm the Roman numeral in the title (see Traps), date and time.
5. Put the Luma URL into every pre-event post (`SOCIAL.md` Notes: "Both link to the Luma, not the blog").

### Deliverables
Luma event page; `LUMA.md` in the repo (gitignored).

### Accounts and tools
Luma login (manual); Google Meet; no key.

### Quality rules
- The Luma carries the hook and the honesty note; Rahul's participant-centric narrative was for the main blog and deck, not Luma (`REQ:899-900`).
- No mention of the cancelled session-8 plan anywhere public (`REQ:900`, `REQ:916`).
- The description discloses what is not live ("Policies cover storage today … Better said now than discovered later").

### Traps
- The live Luma title said "MOI Builders VII" for session 8. `LUMA.md`, `GAMEDAY.md` ("Tonight … Fix the Luma title") and `RUNBOOK.md` ("Luma page title says VIII, not VII") all carry the reminder. Cause `unknown` (inferred: the page was duplicated from session 7's event).
- Confirm date and time before publishing (`LUMA.md` line 3).

### Time
Same day as the topic lock.

### Open questions (registration flow beyond the page)
`unknown`: approval or capacity settings, how the Meet link reaches registrants, reminder emails, whether a post-event recording link is sent, how attendance is tracked. The only registration-adjacent facts: free, live, online, 60 minutes, Luma page, Google Meet used for the session (`GAMEDAY.md` "Share the deck window in Meet").

---

## Process: Pre-event social campaign (X and LinkedIn via Buffer)

### Purpose
Drive registrations to the Luma page and, after the event, drive readers to the blog.

### Trigger
Luma link exists. Observed cadence for session 8 (from `social/` filenames, file mtimes and `REQ`):

| Batch | Files | Written (file mtimes) | Notes |
|---|---|---|---|
| Announcement pair, Mon 31 Aug | `x.txt`, `linkedin.txt`, plus `x-reply.txt` and `linkedin-comment.txt` carrying the link | 08-31 08:16 to 08:45 | |
| Daily pair, Tue / Wed / Thu | `tue-*`, `wed-*`, `thu-*` | 08-31 10:15, except `tue-linkedin.txt` at 09-01 12:47 | |
| "Why"-focused pair, written 1 Sep | `mon-x.txt`, `mon-linkedin.txt`, `mon-x-reply.txt`, `mon-linkedin-comment.txt` | 09-01 01:59 to 02:30 | The `mon-` prefix is not a reliable post day. `REQ:960`: "schedule a post for today, focus on the why". |
| Day-of posts, Fri 4 Sep | `fri-linkedin-t5h.txt` (five hours out), `fri-x.txt` (locked as "Option 3", 273 chars), `fri-linkedin-t1h.txt`, `fri-x-t30.txt` ("WE'RE LIVE IN 30."), `fri-x-live.txt`, `fri-linkedin-live.txt` | not recorded | |

- Scheduling times mentioned: 10am IST next morning for the Voyage posts (not session 8), 5:30pm IST on 1 Sep, 11am IST on 4 Sep, 3:30pm IST on 4 Sep (`REQ:946`, `REQ:971`, `REQ:1039`, `REQ:1081`).
- Whether every file went out as scheduled is `unknown`.
- `voyage-x.txt` and `voyage-linkedin.txt` in the same folder are an unrelated Voyage login-migration announcement.

### Who
Claude drafts (using the `writing-x-posts` and `linkedin-skills` skills, `REQ:917`, `REQ:1161`), Adithya reads every post once before scheduling ("lemme read it once then u can schedule", `REQ:1038`).

### Inputs
Luma URL; the narrative angle (Rahul's participant-centric "why"); verified claims list.

### Steps
1. Draft `SOCIAL.md`: one X single post (two variants), a 5-post X thread, one LinkedIn post, a Notes block (e.g. "The LinkedIn post carries the storage caveat … Do not cut it").
2. Rewrite with a different approach if the framing is wrong. Session 8's first pack in `SOCIAL.md` (framed as "a gate with no fence" and an argument about lockups, whose exact content is not recorded in these notes) was replaced by the `social/*.txt` posts after Adithya said "these are still references to the reason why we're [not] doing session 8 as originally planned" (`REQ:916`) and "rewrite both of them, use a different approach" (`REQ:921`); that the lockup argument is what he objected to is (inferred). Note that `SOCIAL.md` and `LUMA.md` still carry the old lockup framing (at the time of writing), while the posts in `social/` do not.
3. Split each approved post into its own file `social/<day>-<platform>[-reply|-comment|-t1h|-live].txt`.
4. Run stop-slop and humanizer, producing variants A (stop-slop only), B (humanizer only), C (both) in `social/variants/`; Adithya picked A ("ok push A", `REQ:970`).
5. Verify every factual claim (`REQ:931-933`): remove vague attributions like "most teams quietly accept both" because it cannot be cited.
6. Schedule or draft through Buffer (see command below). On LinkedIn put the Luma link in the post body, not a first comment (`REQ:1039`). On X, link in a reply or thread second post (`--follow`).
7. Day-of posts: five hours out, one hour out, 30 minutes out ("WE'RE LIVE IN 30."), live.

Command surface of `WT/scripts/buffer.mjs` (no key printed):
```
node scripts/buffer.mjs channels
node scripts/buffer.mjs post --file <path> --channel <id> [--at <iso8601>] [--draft] [--confirm]
node scripts/buffer.mjs post --text "..." --channel <id> ...
node scripts/buffer.mjs post --thread-dir <dir> --channel <id> ...   # X thread from 1.txt, 2.txt …
  --follow <file>   # X: second post of a thread; LinkedIn: first comment
```
Nothing is scheduled without `--confirm`; `--draft` saves for a human to publish. Run from the repo root (the failed `node scripts/buffer.mjs` from inside `session-8-policies/`, `REQ:913`, is the usual mistake).

### Deliverables
`social/*.txt`; scheduled or drafted Buffer posts.

### Accounts and tools
Buffer account with channels for X and LinkedIn; `BUFFER_API_KEY` in `WT/.env` (key, secret). Skills: `writing-x-posts`, `linkedin-skills:*`, `humanizer`, `stop-slop`.

### Quality rules (observed in the files)
- Zero em dashes and zero emoji in all 25 `social/*.txt` (counted); `SOCIAL.md` states "No emoji, per brand voice". (Session 7's `social-pack.md` still had an emoji and em dashes, so this tightened after 7.)
- Pre-event posts should not give away specifics: on 31 Aug Adithya called the first LinkedIn post too long and said "we don't need to give away specific details like builtin error and 86 fuel, signed, mined" (`REQ:920`), and a 4 Sep draft quoting "86 fuel" was removed (`REQ:1037`). The Tuesday pair (`tue-x.txt`, `tue-linkedin.txt`) does quote the error string, so the rule is a preference about the first announcement and the day-of posts, not an absolute; unknown whether he later approved the Tuesday pair.
- Hook first, tension, then the point; the access-policies post had to name "access policies" and "participant-centric" explicitly (`REQ:1033-1034`).
- Link the Luma before the event; link the canonical blog after (`SOCIAL.md` Notes; session-7 `social-pack.md` "Always link the moi.technology canonical, never the Medium mirror").
- No hashtags decision `unknown` (asked, `REQ:972`).
- Release-post lesson, not session-specific: a protocol post that sounded like the release notes pasted verbatim was rejected by a lead; keep announcements short and point at the notes (`REQ:1193`, `REQ:1204`).

### Traps
- API key pasted in chat on 31 Aug and revoked (`REQ:909-910`); `buffer.mjs` reads `.env` with last occurrence wins so a rotated key appended below a dead one works (header comment).
- Posts out of order: a Buffer post deleted by mistake required redraft (`REQ:1190-1192`; release post, same tool).
- Scheduling time zones: IST versus Dubai versus UTC; "12:00 AM UTC" ambiguity (`REQ:1186-1188`).

### Time
Drafts: hours. Review loop: about a day across 31 Aug and 1 Sep.

### Open questions
Final per-day schedule actually used; hashtag policy; who else approves.

---

## Process: Game day and live run

### Purpose
Run a 60-minute live session where the demo can fail without the session failing.

### Trigger
The day before and the hour before the session. Observed for session 8: `GAMEDAY.md`, `RUNBOOK.md` "Before going live (T-30)".

### Who
Adithya, alone on stage (inferred: no co-host is mentioned in any doc).

### Inputs
Working demo, deck, script, recording, Luma, funded accounts.

### Steps

**Tonight (T-1 day), from `GAMEDAY.md`**
1. Fix the Luma title numeral.
2. Post the last-call social (drafts in `social/`; "Nothing is scheduled" at the time of writing).
3. Send Rahul the deck and the blog.
4. Read `SCRIPT.md` aloud once, end to end, and time it.

**T-60 minutes**
5. `npm run preflight && npm run demo`. Preflight should say 4/4 and "owner has 0 storage policies"; a leftover policy is deleted by the demo before beat 1.
6. Check fuel: a full run costs 506 KMOI (agent 306, owner 200); the agent held about 18,885 so about 60 runs; if low, `npm run setup:fuel`.
7. Open the deck, press `P`, share the deck window in Meet, keep the presenter window private.
8. Have `recording/demo.mp4` open in a tab, one click away.

**T-30 (RUNBOOK)**
9. `npm run preflight; npm run setup:fuel; npm run demo`. All three must exit 0. Owner balance at least 30,000 (about 88k at last check). Terminal font at presentation size, about 100 columns. `DEMO_PAUSE_MS=1500` ready.

**T-10**
10. Terminal ready, command typed but not entered, scrollback cleared. Close everything else, notifications off.
11. One final run so the counter is warm and the node is known to respond.

**Live**
12. Run order (GAMEDAY): why this exists, slides 1-5, 8 min; the problem it creates, 6-8, 5 min; the code, 9-12, 6 min; demo, 13, 4 min; receipt, revocation, scope, 14-17, 4 min; close and questions, 18 (slide numbers are the pre-insert numbering, see Traps).
13. Demo beats: `node scripts/tick.ts` (refused), `node scripts/grant.ts` (optionally `node scripts/policy.ts` to read it back), `node scripts/tick.ts` (lands, counter +1), `node scripts/revoke.ts`, `node scripts/tick.ts` (refused again). If asked to see it again: rerun, it is idempotent and about 600 KMOI.
14. Session 7 live: browser console `http://localhost:4000/?gap=7000` for the demo, editor for two files, terminal for `MAX_PRICE_PER_ANSWER=999999 npm run ask -- "should i be worried about a crash"`; warm-up: restart `npm run ui` fresh (resets demand counters so the first quote lands at list price) and run two throwaway asks on the drawdown market (`TRANSCRIPT.md` pre-flight).

**If it breaks** (`GAMEDAY.md`, `RUNBOOK.md`, `SCRIPT.md`): do not debug live; say "Devnet's having a moment, so let me show you the recorded run. Every hash in it is on chain" (`SCRIPT.md`), play `recording/demo.mp4`, resume at the receipt slide. Table of symptoms in `RUNBOOK.md`: `insufficient funds` on grant (owner thin: show recording or receipts in `NOTES.md`), agent insufficient funds (`npm run setup:fuel`), beat 1 writes (leftover policy; let the run finish, exits non-zero, rerun once), RPC timeouts (receipts), whole node dead (deck stands alone).

**After** (`GAMEDAY.md`): push the recording and the deck PDF; post the blog; open the bounty once its deploy steps are done.

### Deliverables
A completed session; recording; PDF; blog; bounty.

### Accounts and tools
Google Meet (screen share), Cursor editor (`SCRIPT.md` says "switch to Cursor"), terminal, browser, the Voyage explorer in a tab to open hashes live (`REQ:1060-1061`).

### Quality rules
- "Never claim more than the screen shows." (`RUNBOOK.md`)
- Do not let a Q&A question walk you into claiming spend caps work (`RUNBOOK.md` slide 17 note; `GAMEDAY.md`).
- Recording is the contingency; there is no mock mode.

### Traps
- Known state at the time: the bounty was **not live** (needs a migration, `MOI_RPC_URL` in the deploy environment, and the flag flipped; announce it as coming), the Points repo moved to `sarvalabs/Points-Program` (PR `#1` unmerged), nothing about access policies on `docs.moi.technology` because PR 120 had not merged, so do not point people at docs (`GAMEDAY.md` "Known state"). Whether `docs.moi.technology` later had it: `REQ:978` asked Claude to check.
- Session 7: Ctrl-C during `--tamper` leaves the registry pointed at the attacker and the happy path then refuses at step 7; rerun tamper to completion (`session-7/DEMO-PLAN.md`). Tamper was removed from the live path after the 7 Aug registry outage.
- Without `GROQ_API_KEY` the buyer matches keywords and a vague audience question buys the wrong market on screen; only do `npm run ask` with the key and confirm `decided by` shows the model name, not `local-fallback` (`session-7/DEMO-PLAN.md`).
- Session 7 (live on 7 Aug): the browser demo on slide 3 is the longest piece of the running order, and the cues in the pptx speaker notes were rewritten at least six times (`git log` `deck:` commits on 5 and 7 Aug).

### Time
Setup about an hour; a full rehearsal run about 45 seconds plus pauses.

### Open questions
Was the session recorded by Meet, and where was the recording published? Who moderated Q&A?

---

## Process: Rehearsal recording and narrated voiceover

### Purpose
A fallback video of the live demo, and a narrated dry run for the presenter to learn from.

### Trigger
After the demo and deck exist. Session 8: 31 Aug. Adithya asked "No I want you to record a demo for me so I can learn" (`REQ:951`), then for a voiceover of the presentation (`REQ:953`).

### Steps
1. Write a VHS tape: `recording/demo.tape` (Output `recording/demo.mp4` and `demo.gif`; zsh; font 16; 1500x950; theme Catppuccin Mocha; types `DEMO_PAUSE_MS=1200 npm run demo`; sleeps 100s, measured run 37s plus 7s of pauses).
2. Run `vhs recording/demo.tape` (tool and invocation `unknown`; inferred from the `.tape` format).
3. Voiceover: one text file per slide (`recording/vo/01.txt` … `13.txt`), text-to-speech through Groq with three Orpheus voices (files `orpheus-austin.m4a`, `orpheus-hannah.m4a`, `orpheus-troy.m4a`; Adithya chose "austin", `REQ:953-956`; Gemini TTS was rejected because it is no longer free; a terms acceptance in Groq was required, `REQ:955`).
4. Assemble: `recording/build-vo.sh` concatenates `vo/slide-NN.wav` with 1.2s gaps into `narration.m4a` and writes `timings.txt` (`ffmpeg`, `ffprobe`). It stops if a slide wav is missing. Wavs exist only for slides 1-9 and 13 (the rest missing), so the narrated video is incomplete as stored.

### Deliverables
`recording/demo.mp4`, `demo.gif`, `vo/*`, `narration.m4a` (not present), `timings.txt` (not present).

### Accounts and tools
`vhs`, `ffmpeg`, Groq API key (secret, not in the repo).

### Traps
Mojibake in `vo/01.txt`; incomplete wav set; the video only proves one run on one day (inferred).

### Open questions
Was the narrated video ever shared or just for learning?

---

## Process: Post-session blog and social pack

### Purpose
The canonical write-up for search and AI engines, plus the posts that point at it.

### Trigger
Origin: the 4 Aug call: "everything that you do, a dev talk … write down the blog, get your blog published on moi technology, and take that blog link"; "aha first, how-to second"; backlinks to `js-moi-sdk`, the registry SDK, native assets docs and earlier blogs; keep it Markdown, GEO-optimized (`otter-transcript/…_transcript.txt` lines 53-143, 176-200). Observed outcome: session 7 blog drafted the same day as the live session (`REQ:663-664`, 7 Aug) and finalized 8 Aug; session 8 blog written before the event, dated 4 Sep, polished 9 Sep.

### Who
Claude writes, Adithya edits sentence by sentence (16-change editorial pass, commit `f5299c0`; he questions each claim, e.g. `REQ:690-720`).

### Inputs
`README.md`, the demo output (real hashes and terminal output), the call's framing, the previous session's blog, protocol sources.

### Steps
1. Ask for a structure first (`REQ:663` "suggest me a structure").
2. Install and use the blog skills: `claude-blog` (`/blog`), `SNLabat/SEO-GEO-AEO-Skill` (`REQ:665-671`); later `humanizer` (blader/humanizer, installed 31 Aug, `REQ:817`) and `stop-slop`.
3. Draft in the fixed shape (observed in all three blogs):
   - YAML frontmatter: `title`, `description` (about 160 chars), `date` (S8), `author: "Adithya Ganesh"`, `authorRole: "Ecosystem, Sarva Labs"`, `slug`, `tags` (six).
   - H1 = title; hero image.
   - **"What is X?"** H2: bold term, a two-to-three sentence definition, one proof sentence (a real run on devnet). This is the answer-first GEO block. Keep the exact phrase "agentic payments" in the H1, first paragraph and one H2 (session-7 checklist comment).
   - Link the previous session's post.
   - "The problem": the concrete failure.
   - What changed or the two agents.
   - Numbered step walk-through with evidence blocks (real hashes in code fences, terminal output).
   - "The honest part": what is self-imposed, not live, or unsolved (S7: "every guardrail here is self-imposed"; S8: "most of this isn't finished").
   - Comparison with other chains (S8 only; Adithya asked for "comparable prerequisites like comparing with other chains", `REQ:892`): Ethereum allowance, Solana delegate, ERC-7715/7710, as a table.
   - Outside evidence (Gartner June 2025 and the Forbes article, same two links in S7 and S8).
   - "Under the hood": every tool linked (`js-moi-sdk`, `js-moi-agent-registry`, `js-polo`, Groq, Node, TypeScript, tsx, Express, SSE, dotenv), line counts or fuel numbers, and the one-line design rule ("models get judgment, code gets money." / "code gets execution, the protocol gets permission.").
   - FAQ of 7-8 questions (the answers go verbatim into FAQPage JSON-LD).
   - Footer: "Built at Sarva Labs for the MOI Builders series. Earlier sessions cover …" with links.
   - Session 7 also embeds an HTML-comment publishing checklist (slug, title tag 58 chars, meta description 159 chars, canonical, schema, hero alt text, second image, 48h rule) to delete before publish.
   - Session 8 and 9 drafts use `<<< EVIDENCE: … >>>` placeholders for hero, hashes, terminal output and "FAQ: write after the session, matching the questions actually asked", so the blog can be written before the demo output exists and filled after.
4. **Fact-check pass.** Two layers in `session-7/blog-assets/factcheck-report.md`: (a) every link and external claim fetched, verdicts VERIFIED / SUPPORTED / FIXED / INTERNAL; (b) claims checked against SDK sources by "three parallel readers" with verdicts TRUE / FALSE / OVERSTATED / ARGUABLE / SCOPED / UNVERIFIABLE and an action per row. Example corrections: "only the owner can move funds, there can't be a custodian" was FALSE (MAS0 has Approve/TransferFrom and Lockup/Release); "registry is an on-chain listing of capabilities" was FALSE (skills live in the off-chain card); "eleven forgeries" was OVERSTATED (ten hit the verifier). Adithya's own request: "check every line and every claim against MOI's actual protocol code" (`REQ:687`).
5. Run the blog-skill scoring and fix: session 7 ended at AI citation readiness 80/100 and blog quality 69/100, with 3,193 words (~13.7 min) and 27 resolving external links (`PUBLISH.md`).
6. Humanizer, stop-slop. In session 8 this pass removed most em dashes (commit `6a4de4e` diff).
7. Assets: chart as SVG for the site and PNG for Medium; hero image; `schema.jsonld` with BlogPosting plus FAQPage (and TechArticle per the checklist); `MEDIUM.md` is the same body with frontmatter and H1 stripped and image slots removed.
8. Publish. Session 7 path actually chosen: **Medium only, text-only, 8 Aug** (`REQ:726-728`, commits `b18113f`, `ed1f1e1`; `PUBLISH.md`). Steps: paste `MEDIUM.md`, check the five code blocks survived, keep the numbering and blockquotes, pick five tags (`AI Agents`, `Agentic AI`, `Blockchain`, `Payments`, `Web3`), and replace `CANONICAL_URL` in `social-pack.md` with the Medium URL.
9. Post-event social: X thread of 9, LinkedIn, Reddit (plain tone); they link the canonical (`blog-assets/social-pack.md`).
10. Newer path: blog now lives at `blog.moi.technology` and is handled by the `moi-blog` skill (PR into `blog/src/content/posts/<slug>.md`, distribution workflow, Buffer, Mailchimp RSS), `~/.claude/skills/moi-blog/SKILL.md`. The `blog.moi.technology/article/<slug>/` pattern appears in the 31 Aug Voyage post (`social/voyage-x.txt`).

### Deliverables
`BLOG.md`, `blog-assets/*` or equivalent, published post, social pack.

### Accounts and tools
Medium login; moi.technology blog (deploy via PR); Buffer; skills `blog*`, `seo-geo-aeo`, `humanizer`, `stop-slop`; the fetch tool for link checks; `npm view` for package versions (npmjs.com blocks anonymous fetch with 403).

### Quality rules
- Every tool used is linked; claims checked against protocol source and receipts; internal counts recounted after each code change (713 lines across six files, 56-line identity check; recounted after the `payToAgentId` fix, commit `7ffaf91`).
- Positive framing: "mention it like that, don't use a negative, 'there is no'" (`REQ:694`). No metaphor-heavy intros: "open the explanation on the mechanism, not on a label" (commit `83cc3ae`). Short plain paragraphs: "explain with less daunting paragraphs pls" (`REQ:699`, commit `6a5f16c`).
- Remove claims that distract from the point (BEC figure cut from the blog; "x402 comparison" section cut, `REQ:680-681`).
- State exactly what a check does and does not prove (registry binds an identity to a wallet; it does not vouch for what the agent does with money; commit `429b28d`).
- Hash links: Adithya asked for each tx hash to link to the Voyage explorer (`REQ:896`); the shipped `session-8-policies/BLOG.md` still has plain code-fenced hashes (observed).
- Remove any mention of the cancelled session-8 plan (`REQ:900`).

### Traps
- Medium-first makes Medium the canonical; moi.technology later arrives as the duplicate unless Medium's canonical link is set (`PUBLISH.md` "The one thing to decide now"). Conflict: the blog's checklist comment says canonical on moi.technology and Medium syndication only; `PUBLISH.md` and `REQ:726` chose Medium only.
- `schema.jsonld` is not usable on Medium (strips custom JSON-LD).
- The social pack's hook still leads on the $2.9B BEC stat that the blog cut (`PUBLISH.md` step 5).
- Corrections made in the blog were not propagated to the other docs (see Traps below).
- On 15 September 2026 Adithya asked "did we ever push the last webinars blog" (`REQ:1353`, `REQ:1415`). His next message was just "rm" (`REQ:1354`). `community-call.md` reads that as an instruction to remove the stats row from the intro deck, so the log shows no answer to the blog question and the published state of the session-8 blog is `unknown`.

### Time
Session 7: about 25 commits over 7-8 Aug; session 8: written 31 Aug to 4 Sep, polished 9 Sep.

### Open questions
Publication status and URLs of the three blogs; whether the S8 blog moved to `blog.moi.technology`.

---

## Process: Bounty attached to each session

### Purpose
Give attendees a task that reproduces the demo, with a way to submit and be checked.

### Observed
- Session 7: a Google Form (`https://forms.gle/NToEMG47QHro9SiB8`) with three fields, wallet, email, repo link; assignment on a slide and in the blog FAQ: both agents registered on MOI, a 402 quote, the identity check before payment, a real transfer hash (`REQ:658`, deck slide 8 notes). Reward and review process `unknown`.
- Session 8-policies: moved to a challenge on `points.moi.technology` (the Points app), built in a fork under `sarvalabs/Points-Program` (PR `#1`, unmerged), where entrants submit interaction hashes and the server checks them by reading the chain (`REQ:1021`, `GAMEDAY.md`). The first spec required four hashes (deploy a logic that writes to actor state, call it from a second account and see it refused, grant a policy, identical call lands, revoke); Adithya corrected it ("we changed this, it is just grant an access policy and then if you want you can try …", `REQ:1022`); the final wording is `unknown`.
- Status on game day: ships disabled behind a flag, needs a migration, `MOI_RPC_URL`, and the flag flipped (`GAMEDAY.md`).

### Traps
Announce as "coming", not "open", until the deploy steps are done.

---

## Reusable assets

Paths are on Adithya's Mac. `WT` expanded: `~/MOI-Webinars/.claude/worktrees/relaxed-mccarthy-368dbc`. A path starting with `…/` is shortened: read `…/` as `WT/` (for example `…/session-8-policies/GAMEDAY.md` is `WT/session-8-policies/GAMEDAY.md`). In the GitHub repo drop that prefix, but see the header: not every session folder was on `main`.

**Templates in all but name (copy the skeleton, replace the content)**
- `~/MOI-Webinars/.claude/worktrees/relaxed-mccarthy-368dbc/session-8-policies/GAMEDAY.md` (day-before, T-60, T-10, running order, if-breaks, known state, after)
- `…/session-8-policies/RUNBOOK.md` (timed run-of-show, likely questions, if-breaks table)
- `…/session-8-policies/SCRIPT.md` (per-slide speech with PRESS NEXT banners, cues, "If the demo dies", "Likely questions")
- `…/session-8-policies/LUMA.md` (event page copy shape)
- `…/session-8-policies/SOCIAL.md` (X single plus thread plus LinkedIn plus notes)
- `…/session-8-policies/NOTES.md` (build log with verified-live table)
- `…/session-8-policies/README.md` (student README for a short mechanism)
- `…/session-7/README.md` (student README for a long flow: idea, two agents, setup, ten-step flow, run it, limitations, where each claim is enforced, read in this order, tested table, layout)
- `…/session-7/DEMO-PLAN.md`, `…/session-8/DEMO-PLAN.md`, `…/session-9/DEMO-PLAN.md` (choreography; 8 and 9 are the compact form)
- `…/session-8/PLAN.md`, `…/session-9/PLAN.md` (plan with options and holes)
- `…/session-7/STORYLINE.md` (series arc)
- `…/session-7/TRANSCRIPT.md` (script pointer plus say-precisely plus pre-flight)
- `…/session-7/FACILITATOR-NOTE.md` (one-off stakeholder Q&A brief shape)
- `…/session-7/EXPLAINER.md` (plain-words walkthrough)
- `…/session-7/BLOG.md`, `…/session-8-policies/BLOG.md` (finished posts), `…/session-8/BLOG.md`, `…/session-9/BLOG.md` (drafts with `<<< EVIDENCE >>>` placeholders)
- `…/session-7/blog-assets/PUBLISH.md` (Medium checklist), `factcheck-report.md` (verdict table format), `social-pack.md` (X thread, LinkedIn, Reddit), `MEDIUM.md`, `schema.jsonld`

**Scripts**
- `…/session-7/scripts/preflight.ts` and `…/session-8-policies/scripts/preflight.ts` (read-only chain readiness)
- `…/session-7/scripts/verify-sdk.ts` (live SDK claim verification with throwaway keys)
- `…/session-7/scripts/spike-allowance.ts` and `…/session-8-policies/scripts/spike-policy.ts` (prove-or-kill spikes; balance-diff oracle)
- `…/session-7/scripts/attack-test.ts`, `…/session-9/scripts/attack-test.ts` (adversarial suite with control)
- `…/session-9/scripts/x402-probe.ts` (a deliberately ignorant client that demonstrates "legible but not payable")
- `…/session-8-policies/scripts/demo.ts` (right-reason guards, self-heal, summary box)
- `…/session-8-policies/scripts/{tick,grant,revoke,policy,counter-lib}.ts` (one script per live action)
- `…/session-8-policies/scripts/{00-fund-agent,01-deploy-ticker}.ts`, `…/session-7/scripts/{00-setup-asset,01-register-agents}.ts` (idempotent numbered setup)
- `…/session-8-policies/scripts/env-file.ts` (`updateEnv`)
- `…/session-8-policies/packages/shared/src/{chain,config,log}.ts` (receipt helpers: `waitReceipt`, `receiptError`, `decodeRuntimeError`, `rawRpc`, `kmoiBalance`, `existsOnChain`; banner logging with `DEMO_PAUSE_MS`)
- `…/session-7/scripts/ui.ts` (agent console on port 4000 with `?gap=` pacing), `ask.ts` (terminal question), `showcase-discover-all.ts` (stage-only registry scan)
- `…/session-7/scripts/_fix2.ts`, `_unstick2-tmp.ts`, `_replace2.ts` (recovery for tamper and stuck sequence numbers; ad hoc)
- `…/scripts/buffer.mjs` (Buffer CLI with dry-run default)
- `…/session-8-policies/recording/demo.tape`, `build-vo.sh`

**Contracts**
- `…/session-8-policies/ticker-logic/ticker.coco`, `coco.nut`, `ticker.json` (30-line actor-state logic)
- `…/session-8/budget-logic/agentbudget.coco` (the superseded budget ledger, kept intact)

**Decks**
- `…/session-8-policies/deck/index.html` and `MOI_Builders_S8.pdf` (HTML deck with presenter view); `…/session-7/deck/MOI_Builders_S7new1f.pptx`, `MOI_Builders_S7-new.pptx`, `deck/assets/{moi-logo.svg,moi-mark.png,pip.png}`
- Existing skill: `~/.claude/skills/moi-deck/` (`assets/template.html`, `scripts/new-deck.sh`, `scripts/render.sh`, `reference/{build,components}.md`)

**Example outputs worth bundling as references**
- `…/session-8-policies/social/*.txt` and `social/variants/{A-stopslop,B-humanizer,C-both}.txt` (before/after of a humanizer and stop-slop pass on one post)
- `…/session-7/blog-assets/factcheck-report.md` (claims audit)
- `…/session-8-policies/NOTES.md` (what a verified-live log looks like)
- Existing skill: `~/.claude/skills/moi-blog/` (publish, distribute, Buffer, GEO)

---

## Rules and house style

**Voice and spoken script** (all from Adithya's corrections; see the Deck process for line cites): warm, spoken sentences read word for word; longer sentences, not staccato; no "not this, not that" contrast, no "aura farming"; real technical depth; cues for every window switch; explicit slide partitions.

**Public copy**
- No emoji and no em dashes in social posts (zero of each across all 25 `social/*.txt`); `SOCIAL.md`: "No emoji, per brand voice". Session 7 social pack and blog still used both; the rule tightened after.
- Run humanizer and stop-slop on every blog, script and post; vary results (A/B/C) and pick.
- Remove unverifiable generalisations: "Most teams quietly accept both", "AI SLOP" lines (`REQ:966`).
- Do not mention the cancelled session 8 in public copy (`REQ:900`, `REQ:916`).
- Pre-event posts link the Luma; post-event posts link the blog.
- The social post is the hook and the crawler follows the link (`social-pack.md` first line; 4 Aug call).
- Terminology from Adithya's memory (not in these files): participant-centric not account-centric; say network ID. (Observed in the S8 script: "participant-centric".)

**Honesty guardrails, exact phrases**
- "The chain refuses the spend", never "the agent can't touch the money" (`STORYLINE.md`, `session-8/README.md`, `session-8/PLAN.md`).
- Sub-accounts share the primary's key; inheritance is not key isolation (same files).
- "A limit the agent consults is a preference. A limit the chain applies is authority." (session 7 close; quoted at the top of `session-8/PLAN.md`)
- "Only storage is live; asset, logic and key policies are reserved." Do not claim spend caps (`RUNBOOK.md`, `GAMEDAY.md`, blog).
- Say "scan", not "search", for registry discovery (O(n) client-side) (`TRANSCRIPT.md`, `DEMO-PLAN.md`).
- The probabilities are invented; say it before anyone asks (`TRANSCRIPT.md`).
- Do not claim the model chose the market unless `decided by` shows the model name (`session-7/DEMO-PLAN.md`).
- Do not call the session-7 demo x402 (`session-7/DEMO-PLAN.md`); in session 9: "Any x402 client can read our invoice. Only a client that implements our scheme can pay it." Say both halves or neither.
- Seller prices per request; it does not decline (refusing is not implemented) (`TRANSCRIPT.md`).
- Identity check runs before the money moves; the ordering is the point.
- "Nobody holds your money" is, per the audit, only true as "value moves only under the holder's own signature, and our agents never grant one" (`factcheck-report.md`, row 1).
- Never write a shape you cannot demo: `withinPrefix()` left off because the network does not enforce it (`NOTES.md`).

**Structure habits**
- Each session adds one idea and removes nothing; the closing slide lists three questions across three sessions.
- Each blog links the previous blog and the earlier session folders.
- Every blog has an honest section and a one-line design rule.
- Every demo has a failure beat that is not ours and a cut rule for timing.
- Docs are written to be read by a stranger: "define the product up front, drop the metaphors" (commit `c4926d8`).

**Process habits**
- Spike before build; verify claims live; recount numbers after code changes.
- Keep old designs on disk, note why they were dropped.
- Do not push or publish without an explicit yes: Buffer `--confirm`, `--draft`; "DO NOT PUSH ANYTHING ANYWHERE" for the x402 docs (`REQ:793`); gh must be the `sarvalabs-adithya` identity.
- No unprompted multi-agent runs (`REQ:515`).

---

## Traps

1. **Corrections not propagated.** The session-7 factcheck (`blog-assets/factcheck-report.md`, row 1, 7 Aug) proved "only the owner can move funds / there can't be a custodian" FALSE and rewrote the blog, but the same claim survives in `session-7/README.md` lines 85 and 154 ("On MOI only the owner of funds can move them"), `session-7/EXPLAINER.md` line 46 ("only you can move your own funds"), `session-7/DEMO-PLAN.md` lines 63 and 248 ("on MOI nobody can move it for you"; "not a design choice: on MOI only the owner can move their own funds"), `session-7/TRANSCRIPT.md` line 23, `session-7/FACILITATOR-NOTE.md` line 57, and the speaker notes of slide 3 in the presented deck `session-7/deck/MOI_Builders_S7new1f.pptx` ("on MOI only the owner can move their own funds"). Fix by search-and-replace across all docs and the deck notes whenever a claim is corrected; the `check-claims.sh` script proposed in the skill section (not yet written) would do this.
2. **Stale docs after a pivot.** `session-7/FACILITATOR-NOTE.md` describes a `packages/facilitator` that was removed in commit `bc5f509`; `STORYLINE.md` says mock mode and books; `session-7/DEMO-PLAN.md` references a missing RUNBOOK; `session-8/README.md` and `DEMO-PLAN.md` describe context inheritance while `session-8/BLOG.md` and `session-9/*` describe an allowance; `session-8/.env.example` and `session-9/.env.example` still say "#7".
3. **Counts drift.** Forgeries: session-7 README says 11 forgeries plus one control; the blog says ten (after audit); session-9 says twelve; `attack-test.ts` says ten of twelve make real transfers. Deck line counts and blog line counts must be recounted after every code change.
4. **Green for the wrong reason.** Broke agent versus forbidden agent; keyless Groq fallback picks the wrong market; MAS0 fails silently. Defences are listed in the Build process.
5. **Fuel versus balance confusion**, and a fuel limit that exceeds balance.
6. **Devnet reset** (accounts, assets, logics and registrations all vanish). `preflight` first.
7. **Registry outages and limits.** Writes down on 7 Aug; `getAllAgentIds` reverts at about 135 agents and returns `[]`.
8. **Wrong derivation path** produced "account not found" for a funded wallet (`m/44'/6174'/7020'/0/0` versus `m/44'/6174'/1'/0/0`).
9. **Luma title numeral wrong** (VII for session 8).
10. **Slide-number drift** between deck and RUNBOOK/GAMEDAY; presenter notes not refreshing in the browser on 4 Sep.
11. **Leftover state from a crashed run** (policy, tampered registry entry): self-heal before beat 1.
12. **Secrets in chat.** A Buffer API key and a devnet mnemonic were pasted into chat on 31 Aug (`REQ:883`, `REQ:909`); the key was revoked (`REQ:910`). Values are not reproduced here. The new skill must say: secrets only in `.env`, never in the conversation, and never pass a mnemonic to Claude to "authorize" a deploy.
13. **Internal names in tracked docs.** `session-8-policies/README.md` (line about "Ram's phrasing on the 27th") and `NOTES.md` ("Ram killed it") are tracked while `RUNBOOK.md`, `LUMA.md`, `SOCIAL.md`, `social/` are gitignored. The repo is public at `moi-foundation/MOI-Webinars` (blog links to it as open). Whether branch contents were ever made public: `unknown`. (inferred) Strip reviewer names from tracked files before merge to `main`.
14. **Medium canonical** (see Blog process).
15. **Publishing before a feature is live**: the bounty and `docs.moi.technology` pages were not live on game day; announce as coming.
16. **Leftover drafts that point at a cancelled or unfinished session.** `session-9/BLOG.md` links a post for a cancelled session; `session-8/BLOG.md` embeds `<<< EVIDENCE >>>` placeholders. A publish gate must grep for `<<<` and `REPLACE-WITH`.
17. **Hash links.** Requested but not present in the shipped S8 blog.
18. **Node version.** Live scripts need a Node that runs `.ts` directly, but `engines` says `>=20`.
19. **Encoding.** Mojibake in `recording/vo/01.txt`.
20. **Timing drift**: three different talk lengths in three docs.

---

## Open questions

1. What is the status and URL of each blog (session 7 on Medium: URL? session 8-policies; sessions 8 and 9 drafts)? `REQ:1353` asked and the answer is not in the evidence.
2. What is session 9 now that session-8-policies replaced session 8? Does x402 continue as a webinar or only as the CASA/x402 PR work in `WT/x402-compat/`?
3. Luma: who creates it, which template, why "VII"; are approval, capacity or reminders configured; how does the Meet link reach registrants; is there a registration form beyond Luma?
4. Was each session recorded, where is the recording hosted, and who receives the PDF?
5. Who are Rahul and Ram (roles), and what is the formal approval gate? What exactly did Rahul say about narrative (`REQ:1030` asks for it verbatim; the answer is not captured)?
6. Is the date "the 27th" in `README.md` and `NOTES.md` wrong, or was there a separate call?
7. Where is the generator that builds the deck's presenter notes from `SCRIPT.md`? (Not in the repo; the `moi-deck` skill may have absorbed it.)
8. What was the final bounty spec and reward for session 8 (and reward and review for session 7)?
9. Which social files were actually scheduled and posted, at what times, and were the hash-bearing Tuesday posts used?
10. Hashtag policy and UTM tagging for webinar posts (`moi-blog` has UTM tooling; not applied in the `social/*.txt` files, which use bare Luma URLs).
11. Does the demo still run on the current devnet after the v0.13.0 update (fee payer)? What is the policy for re-verifying a prior session before reuse?
12. Does the live demo need Node 22.6+ and should `engines` be corrected?
13. Is the squashed public repo supposed to show sessions 8 and 8-policies on `main`? `WT/README.md` series table lists 1-7 only.
14. How long does the post-event step actually take? "Within 48h" is the stated target; no evidence it was met for session 8.
15. Did the hash hyperlinks requested for the blog get applied anywhere?
16. Was there any attendee data (count, questions) captured and used? The session-8 FAQ in the blog was written pre-event; session 8/9 blog placeholders say "write after the session, matching the questions actually asked", but no after-session FAQ exists.

---

## Proposal for a skill: what it should contain

This section is a proposal written during the research, before the skill existed. The reference files, scripts and templates listed here are proposals, not files that exist in this repo.

### Shape
One orchestrating skill, `moi-webinar`, that owns the lifecycle and hands off to existing skills rather than duplicating them: `moi-deck` for deck, presenter window and PDF; `moi-blog` for publish, distribute, Buffer, Mailchimp, GEO; `humanizer` and `stop-slop` for prose; `blog-factcheck`, `blog-geo`, `blog-write` for the post. Do not tell the skill to spawn sub-agents unless the user asks (Adithya's stated rule); if the user opts in, Haiku for bulk drafting and Sonnet for judgment is what he has used.

### SKILL.md outline
1. Description (trigger words): planning, building, promoting, running or writing up a MOI Builders session; "webinar", "dev talk", "MOI Builders #N", "Luma", "game day", "demo plan".
2. The lifecycle table (13 steps from this note, with the document each step produces and the skill or reference that owns it).
3. Intake questions: session number and Roman numeral, date and time zone, one idea, source call, reviewer, previous session folder, funded wallet status.
4. The honesty guardrails (exact phrases above) as a must-read before writing any copy.
5. The five gates, each with a command: spike passes; `preflight` exits 0; demo exits 0 with right-reason guards; claim audit complete; publish gate (no `<<<`, no `REPLACE-WITH`, Luma numeral equals session number, slide count equals RUNBOOK references).
6. Handoff table: what to give the user to do by hand (Luma page creation and Meet link, Medium paste, Buffer confirm), what Claude does.
7. Secret handling: `.env` only; never ask for a mnemonic or a key in chat; `buffer.mjs` dry-run default.

### Reference files to bundle (`references/`)
- `lifecycle.md`: the table of documents and their order, with who reads each and which are gitignored.
- `demo-standard.md`: the Build-process quality rules, receipts policy, balance-diff rule, right-reason rule, numbered idempotent setup, one-script-per-action live form, presentation-mode `.vscode/settings.json`.
- `honesty-guardrails.md`: exact phrases and the "do not say" list, with the factcheck verdict vocabulary.
- `script-voice.md`: Adithya's corrections to spoken scripts, cue grammar for both formats, and a before/after example from `SCRIPT.md`.
- `luma.md`: the page shape and the Practical table, the numeral check.
- `social.md`: day-by-day cadence, file naming, variant workflow A/B/C, Buffer commands, the no-emoji and no-em-dash rules, "link the Luma before and the blog after".
- `gameday.md`: the T-1 day, T-60, T-30, T-10 checklist and the if-it-breaks tables (merge GAMEDAY and RUNBOOK).
- `blog-template.md`: frontmatter, the answer-first block, the section list, FAQ rules, the Under-the-hood closer, the `<<< EVIDENCE >>>` placeholder convention and its removal gate, Medium checklist and canonical decision.
- `traps.md`: the 20 traps above.
- `known-limits-of-this-evidence.md`: the open questions, so a hire knows what to ask.

### Scripts worth writing
- `new-session.sh <N> <slug>`: copy the previous session folder, rename headers and package name, blank `.env` values, rewrite `.env.example` headers (fixes the "#7" carry-over), create `NOTES.md`, `GAMEDAY.md`, `LUMA.md`, `SOCIAL.md` from templates.
- `preflight.template.ts` and `spike.template.ts`, `attack-test.template.ts`: the read-only readiness check, the prove-or-kill spike with a balance-diff helper, and the adversarial suite with an honest control.
- `check-claims.sh`: grep every doc in the session folder for known-FALSE or banned phrases ("only the owner can move", "the agent can't touch the money", "search" near "registry", "x402" in session-7 copy, "sells-signals", "agent_134"), for `<<<`, `REPLACE-WITH`, em dashes and emoji in `social/`.
- `check-consistency.sh`: slide count in `deck/index.html` versus slide numbers referenced in `RUNBOOK.md` and `GAMEDAY.md`; Luma numeral versus session number; talk length stated in each doc; count of forgeries across docs.
- `schedule-social.sh`: wraps `scripts/buffer.mjs` over `social/*.txt` with a dry-run default and a table of time, channel, file.
- `verify-hash.ts`: reads back an interaction hash and prints status, fuel and error so blog hashes are checked, and builds the explorer link once the URL pattern is confirmed (unknown today).
- `vhs-record.sh`: wraps `recording/demo.tape` and `build-vo.sh`, failing if a slide wav is missing.

### Templates to bundle (`assets/`)
`PLAN.md`, `DEMO-PLAN.md`, `GAMEDAY.md`, `RUNBOOK.md`, `SCRIPT.md` (with `PRESS NEXT -->` banners), `LUMA.md`, `SOCIAL.md`, `NOTES.md`, `README.md` (student), `BLOG.md` (with evidence placeholders), `PUBLISH.md` (Medium checklist), `factcheck-report.md` (verdict table), `schema.jsonld` (BlogPosting and FAQPage), `.vscode/settings.json` (presentation mode), `demo.tape`.

### Decisions the skill must make the user confirm, not assume
Date and time zone; whether the demo has a failure beat; whether a bounty is live; where the blog is canonical (Medium versus `blog.moi.technology`); whether to post or only draft (Buffer `--draft`); which reviewer approves before the Luma goes public.

---

## Known inconsistencies in these notes

These are places where this file, or this file and a sibling note, disagree. They are listed, not resolved. Line numbers refer to this file unless another file is named.

1. Narration pause default: L248 sets `DEMO_PAUSE_MS=1200` and says the browser `gap` default is 700; L261 says the default became 6 seconds per card and the deck uses `gap=7000`; L268 and L493 say the runbook uses `DEMO_PAUSE_MS=1500`; L542 records the recording tape using 1200.
2. Ram's feedback: L113 says it killed the first session-8 design; L149 (and L756, L774) say "Ram killed it on the 27th" does not match the 31 Aug call evidence. Whether there was a separate call on the 27th is open.
3. Owner's KMOI balance for the demo: L213 says give the owner about 100k KMOI (10,000 failed, about 109,000 worked); L493 says at least 30,000, "about 88k at last check".
4. KMOI per full run: L210 and L488 say 506 KMOI (agent 306 plus owner 200) and that the runbook says about 600; L501 says a rerun costs about 600 KMOI.
5. What the Buffer tooling does: L435 says nothing is scheduled without `--confirm` and `--draft` saves for a human to publish. `community-call.md` (L479) says the Buffer pipeline creates drafts only and never publishes. These may be two different tools; the notes do not say.
6. What session 7 is about: L143 says identity; `webinars-early.md` (L905) calls session 7 "Agentic Payments"; the blog checklist at L561 onward keeps the exact phrase "agentic payments" for it. The notes do not reconcile "identity" with "agentic payments".
7. Slide count and talk length: L266 says the deck has 19 slides and the runbook and gameday docs speak of 18; L269 gives three talk lengths (about 30 minutes, about 24 minutes, 60 minutes); L292 says 19 slides. Which was used live is unknown.
8. When the registry went down for session 7: L221 and L750 say writes were down on 7 Aug and forced the pivot; L108 says the live session was Friday 7 Aug; L308 says the pivot was made two days before the show. If the show was 7 Aug the pivot was about 5 Aug, before the outage date given.
9. Rahul's role: L44 and L773 treat it as unknown beyond reviewing the deck and blog; other notes in this folder (`community-call.md`) describe him as the manager (marked inferred there). The header of this file uses the team's known role (reviews and approves DevRel work, sets priorities).

---

## Glossary

Terms are defined as the MOI team uses them. "(as used in these notes)" marks the research assistant's reading, not an official definition.

- **Access policy**: an on-chain rule about who may read or write an account's storage (session 8-policies). Only storage policies are live; asset, logic and key policies are reserved (as used in these notes).
- **Actor state**: Coco storage kept separately for each participant who calls a logic.
- **Allowance**: the mechanism in the first session-8 design that let an agent spend up to a set amount (as used in these notes).
- **anu**: the atomic units of KMOI.
- **BEC**: business email compromise, the kind of fraud behind the "$2.9B" statistic the blog cut (as used in these notes).
- **Balance diff**: comparing an account's balance before and after an action; the only reliable way to see a refused MAS0 transfer.
- **Buffer**: a social-media scheduling service; Chandra owns MOI's Buffer organisation.
- **CASA**: the name of an x402-related compatibility effort tracked in `WT/x402-compat/`; these notes do not expand it (as used in these notes).
- **Canonical URL**: the one official address of a post, which search engines should credit when the post is also published elsewhere (for example on Medium).
- **Claim audit**: checking every claim in the blog, deck and posts against docs, SDK source and live receipts.
- **Coco**: MOI's contract language (`coco.nut` is the compiler config beside a source file). **Logic**: a deployed Coco contract on MOI.
- **Context inheritance**: giving a sub-account its own storage slot for a logic so the logic can keep per-agent state; the dropped session-8 design used it.
- **Demand counters / list price / drawdown market**: the session-7 seller raises its quote as demand grows; restarting the UI resets the counters so the first quote is the base "list price"; "drawdown" is one of the demo's four markets (as used in these notes).
- **Devnet**: MOI's test network; it is reset from time to time and can lag the released protocol version.
- **ERC-7715 / ERC-7710**: Ethereum proposals for granting and redeeming scoped permissions to another account; the session-8 blog compares MOI policies with them (as used in these notes).
- **Facilitator**: in x402, a service that checks and settles payments; session 7 had one (`packages/facilitator`) and removed it.
- **Fuel**: what an interaction pays to run. **KMOI**: MOI's native asset, which pays for fuel.
- **GEO**: generative engine optimisation, writing so that AI answer engines can find and cite a page.
- **FAQPage / JSON-LD**: JSON-LD is structured data embedded in a page for search and AI engines; FAQPage is the type that marks up questions and answers.
- **Game day**: the day of a live session; `GAMEDAY.md` is its checklist. **T-60, T-30, T-10**: minutes before the start.
- **Gitignored / tracked**: gitignored files are never committed (they live only on Adithya's Mac); tracked files are committed on the branch.
- **Groq**: an AI service used for the session-7 agents' model calls and for text-to-speech; it has a free tier.
- **Haiku / Sonnet**: Claude model sizes; Haiku is the smaller, cheaper one and Sonnet the mid-sized, more capable one.
- **Humanizer / stop-slop**: Claude skills that strip AI-sounding patterns from text.
- **Idempotent**: safe to run more than once with the same result.
- **Interaction / interaction hash**: MOI's word for a transaction, and its identifier.
- **Luma**: the event-page and registration service used for the webinars; the page is made by hand.
- **MAS0**: an asset standard created without a contract. **MASX**: a logic-backed asset. **MAS1**: the NFT standard.
- **MeterExhausted**: the error from the registry call `getAllAgentIds()` at roughly 135 agents (as used in these notes).
- **Medium**: a blogging platform; session 7's post went out there first.
- **Mojibake**: garbled characters caused by a text-encoding mix-up.
- **Otter**: a service that records and transcribes calls.
- **Orpheus**: the text-to-speech voices offered through Groq (austin, hannah, troy) used for the rehearsal voiceover.
- **ParticipantCreate**: the interaction that creates a new account (participant) on MOI.
- **Participant-centric**: MOI is participant-centric, not account-centric.
- **Points**: the Points program and app (`points.moi.technology`) that hosts the session-8 bounty challenge (as used in these notes).
- **Preflight**: a read-only script that checks the chain, accounts and fuel are ready before a demo.
- **Receipts**: interaction receipts read back from the chain, used as proof that something happened.
- **Registry (agent registry)**: the on-chain list where agents register; `js-moi-agent-registry` is its SDK.
- **Roman numeral session numbers**: webinars are titled "MOI Builders #N" or with a Roman numeral (VII for 7); the live Luma title for session 8 wrongly said VII.
- **RPC**: the remote procedure call interface of a MOI node.
- **Spike**: a quick throwaway experiment to prove or kill a mechanism before building on it.
- **Squashed repo**: a repository whose history was flattened into few commits, so earlier commits are not visible (as used in these notes).
- **Tamper / forgery**: the attack steps of the session-7 demo and `attack-test` suite, which try to fake a payment or alter a registry entry.
- **VHS**: a tool that turns a script file (`.tape`) into a recorded terminal video or GIF.
- **Voyage**: MOI's explorer and dev tooling site (voyage.moi.technology); the devnet faucet and RPC are reached through it.
- **WT (worktree)**: a second checked-out working folder of a git repo; see the header.
- **x402**: a payment standard built on the HTTP 402 "Payment Required" status code (as used in these notes).

---

## Appendix: Sources read

These are the sources the research assistant read. `WT` and `REQ` are explained in the header.

Read in full:

- `WT/session-7/`: `README.md`, `DEMO-PLAN.md`, `STORYLINE.md`, `EXPLAINER.md`, `FACILITATOR-NOTE.md`, `TRANSCRIPT.md`, `BLOG.md`, `deck/README.md`, `blog-assets/PUBLISH.md`, `blog-assets/factcheck-report.md`, `blog-assets/social-pack.md`, `blog-assets/schema.jsonld` (head), `blog-assets/MEDIUM.md` (head + diff against BLOG.md). `blog-assets/*.png|svg` and `deck/*.pptx` read by name; both pptx files had their slide text and speaker notes extracted read-only with `python3 zipfile`.
- `WT/session-8/`: `PLAN.md`, `DEMO-PLAN.md`, `README.md`, `BLOG.md`, `package.json`, `.env.example`, `scripts/demo.ts` (head), `scripts/02-provision-agents.ts` (head), `budget-logic/agentbudget.coco`, package layout.
- `WT/session-8-policies/`: `README.md`, `NOTES.md`, `RUNBOOK.md`, `GAMEDAY.md`, `LUMA.md`, `SOCIAL.md`, `SCRIPT.md`, `BLOG.md`, `scripts/{preflight,demo,tick,grant,revoke,policy,counter-lib,spike-policy,00-fund-agent,01-deploy-ticker}.ts`, `ticker-logic/coco.nut`, `packages/shared/src/{chain,config,log}.ts` (greps), `deck/index.html` (structure, slide titles, presenter-view code), `recording/{demo.tape,build-vo.sh,vo/01.txt}`, all 25 files in `social/` and 3 in `social/variants/`, `.vscode/settings.json`, `.gitignore`, `.env.example`. `.env` was never opened.
- `WT/session-9/`: `PLAN.md`, `DEMO-PLAN.md`, `README.md`, `BLOG.md`, `package.json`, `.env.example`, `scripts/x402-probe.ts`, `scripts/02-grant-authority.ts` (head), `scripts/attack-test.ts` (head).
- Cross-cutting: `WT/.gitignore`, `WT/README.md` (series table), `WT/scripts/buffer.mjs` (CLI surface), `WT/otter-transcript/Project Launch and Blog Strategy_{summary,transcript}.txt` (the 4 Aug call), read-only `git log` / `git ls-files` / `git ls-tree` / `git show --stat 6a4de4e`, session-7 scripts `preflight.ts`, `verify-sdk.ts` (head), `spike-allowance.ts` (head), `attack-test.ts` (head), `_fix2.ts`, `_unstick2-tmp.ts`, `showcase-discover-all.ts`.
- `REQ`: lines 219-262 (worktree sessions on session 8), 493-1100 (the main session, 3 Aug to 4 Sep), 1325-1430 (later webinar mentions). Prompts in `REQ` are truncated by the extractor at roughly 300 characters, so the long pasted call transcripts (e.g. `REQ:866`, `REQ:897`, `REQ:957`) cannot be read past their opening.
- Existing skills inspected for overlap: `~/.claude/skills/moi-deck/SKILL.md` and `~/.claude/skills/moi-blog/SKILL.md`.

Not read (out of scope or skipped by rule): `node_modules`, lock files, `.env` files, session-8-policies `recording/vo/*.wav|m4a`, `recording/demo.mp4|gif`, `deck/MOI_Builders_S8.pdf`, the `session-9/packages` and `session-8/packages` source (only layout and a few file heads), personal projects.
