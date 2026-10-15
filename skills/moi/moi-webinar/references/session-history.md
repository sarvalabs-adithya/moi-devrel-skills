# Session history: sessions 1 to 9 and the intro session

Facts are as of 2026-10-02. Where a file lives was read with git on that date: `origin/main` is commit `c4926d8` (2026-08-06; by 13 October 2026 it had moved to `54974c8` with the community call decks, and the branch is still 95 commits ahead of it), and the branch `claude/agent-payments-simple` is `3e1d5d8`. Both matched `git ls-remote` on the public remote. **Main** means `origin/main`. **Branch** means that branch on origin, which is public, so every tracked file on it is readable by anyone. **Local only** means ignored by git or untracked: it is not in the repo. Session 7's plan documents and the intro deck are now in the handover repo under `skills/moi/moi-webinar/past-sessions/`; the other originals are not recorded in the handover, and cleaned copies of session 8's are in `../examples/session-8/`. Roman numerals appear in Drive form names and event page titles, session numbers in the repo. Back to `../SKILL.md`.

## The sessions

| # | Held | Topic and demo | Where it lives |
|---|---|---|---|
| 1 | no date recorded (session III's transcript refers to it) | CocoLab and the SDK. A Flipper logic toggled in CocoLab, then deployed, flipped and read from the SDK. A MAS0 asset as a teaser | main: `session-1/` |
| 2 | Fri 2026-06-12, about 18:22 IST | Native assets. A MAS0 asset, then a TaxToken (a logic-backed asset taking 5% on transfer). Bounty: both asset ids | main: `session-2/` |
| 3 | Thu 2026-06-18, about 50 minutes | The on-chain agent registry with OpenClaw, a third-party agent framework. Two agents register, discover each other and message. Two bounties | main: `session-3/` |
| 4 | date not recorded; form created 2026-07-03 | Swaps with MAS0 Lockup and Release between two wallets, as a CLI and a Vite UI. Bounty form | main: `session-4/` |
| 5 | held (date not recorded; confirmed by the previous operator, 2026-10-14) | NFTs: a MAS1 collection minted and transferred, CLI and a small web UI. Bounty section in its README | main: `session-5/` (added to main 2026-08-03) |
| 6 | held (date not recorded; confirmed by the previous operator, 2026-10-14) | Context inheritance. One wallet, sub-accounts under an AgentBudget logic, a squad script and a chat agent | main: `session-6/` (added to main 2026-08-03) |
| 7 | Fri 2026-08-07 (inferred from the form and the 6 Aug standup) | Agentic payments, part 1. A buyer agent finds a seller on the registry, checks the registered wallet against the quote, then pays with a native transfer | main: README, EXPLAINER, code, deck `MOI_Builders_S7-new.pptx`. Branch adds `BLOG.md`, `blog-assets/`, the presented deck `MOI_Builders_S7new1f.pptx`, `preflight.ts`. Local only (now in the handover repo, `skills/moi/moi-webinar/past-sessions/session-7/`): `STORYLINE.md`, `DEMO-PLAN.md`, `TRANSCRIPT.md`, `FACILITATOR-NOTE.md` |
| 8, first design | not held | A budget logic on an inherited sub-account, with an allowance planned as the fix. Built, then dropped on 31 Aug 2026 after review | branch: `session-8/` (kept intact on purpose) |
| 8 | Fri 2026-09-04, 16:00 IST (10:30 UTC), 60 minutes | Access policies: the same call made three times, refused, allowed, refused. A 30-line Ticker logic, four per-beat scripts | branch: `session-8-policies/` (63 files). Local only: `RUNBOOK.md`, `LUMA.md`, `SOCIAL.md`, `social/`. A cleaned copy is in `../examples/session-8/` |
| 9 | not held (planned and built only) | Agentic payments, part 3: the x402 envelope with MOI settlement. Built on session 8's allowance, which was dropped | branch: `session-9/` (plan, draft blog, scripts). ASK: Rahul |
| Intro | not recorded | "Your first agent on MOI": four ideas, then the Agent Launchpad live. See `intro-session.md` | handover repo: `skills/moi/moi-webinar/past-sessions/intro-session-deck/` |

Session 6's content also exists in the previous operator's private repo `moi-agent-budget` (3 commits, 15 July), which adds a teaching guide and a webinar plan. His dependency notes said that repo's contract was wiped by the devnet resets and needs a redeploy and an SDK upgrade. The repo is not in the 4 October dependency list (now only in git history) or `MIGRATION-LIST.md`; ASK: Rahul whether it moves to the org.

## Numbering

Numbers on record: 1 to 8 are used, and 9 is planned (a plan, a draft post and scripts on the branch, `session-9/`). Whether the next session takes 9, because 9 was never held, or 10, because the 9 folder already exists, is not recorded. Inferred: a new session cannot reuse 9 without first dropping that plan. ASK: Rahul. Roman numerals in the event page title and Drive form names must follow whatever is chosen (`event-page.md`).

## What breaks on today's devnet

No run of any session is on record after the wipe announced for 11 September 2026 (`moi-devrel/references/devnet.md`, reset history, which also says that date is not confirmed to the minute), so "it works" is unknown for all of them. Rehearse before reusing one. A rehearsal spends devnet funds and needs the operator's yes.

- **All sessions.** Accounts, assets, logics and agent ids are wiped by a reset (`moi-devrel/references/devnet.md`, reset history: 2026-08-15, and 2026-09-11 as announced). Any id saved in an old `.env` is dead. Devnet answered `net.Version` 0.13.0 on 2026-10-02, and v0.13.0 changed the KMOI asset id, the fuel price floor (50), the default storage fund and the minimum grant when creating a participant.
- **Sessions 1 to 6** pin `js-moi-sdk` between 0.7.0-rc15 and ^0.7.1. The SDK repo is at 0.9.0-rc3. Whether 0.7.x still signs and sends against 0.13.0 is unknown. Their fuel helper reads the KMOI balance by an asset id from the SDK, so a stale id could read the wrong asset (inferred). ASK: Gokul.
- **Session 3** uses `js-moi-agent-registry` 0.1.0 and `getAllAgentIds`. That package embeds an old registry id, and the call reverts at about 135 agents. The registry restored on 2026-09-11 held 144 agents, so the list is probably empty (inferred). OpenClaw must run only in a container (`moi-devrel/references/consent-and-identity.md`, section 7). A deployed demo called `agent-dating` is a separate thing in the previous operator's GitHub account.
  Before touching that demo's admin, read its entry in `moi-devrel/references/repo-map.md`.
- **Session 7** was presented with two pre-existing agents (ids 132 and 133), because registry writes were failing at the time (`devnet.md` dates a registry failure to 2026-08-06). The resets of 2026-08-15 and the one announced for 2026-09-11 probably removed them (inferred: the registry restored after that reset holds an old snapshot of 144 agents, and whether these two carried over is not recorded). ASK: Gokul. A new setup needs the registry package that matches the registry restored on 2026-09-11. ASK: Gokul for the version.
- **Session 8** needs the node method `moi.AccessPolicies`. A read-only call on 2026-10-02 answered with a domain error for an all-zero id, which means the method exists. The last verified runs on record are of 31 Aug to 4 Sep 2026 on node 0.12.0 (`NOTES.md` on 31 Aug, and the 9 Sep commit "verified live against devnet before the session"). Its numbers (86 fuel for a refusal, 506 KMOI a run, a storage fund of 6,000, a minimum key weight of 1,000) predate v0.13.0 and are unmeasured since.
- **Session 9 and session 8's first design** depend on the allowance. Do not reuse them without a new plan.

## Per-session facts worth keeping

- **Folder shape.** Sessions 1 to 6 vary but share `README.md`, `package.json`, `.env.example` and, where a logic is used, `coco/` with the source and a compiled `.json` manifest that is checked in. Sessions 7 to 9 are npm-workspace TypeScript monorepos, and the session 7 README says there is no offline mode. Details: `demo-standard.md`.
- **Derivation path.** The faucet wallet is `m/44'/6174'/7020'/0/0`. The wallet-extension account used in session 8 was `m/44'/6174'/1'/0/0`, and the wrong path gave "account not found" everywhere on 31 Aug 2026. The session 8 `.env.example` still shows 7020.
- **Bounties.** Sessions 2, 3 and 4 are in the root README. Sessions 5 and 6 carry a bounty section in their own README. Session 7 used a form. Session 8 moved to the Points app. Since 13 October 2026 a session ends with a webinar bounty on the Points site (`after-the-session.md`). Reward amounts are written in those files. Who pays and who verifies is not on record. See `after-the-session.md`.
- **Series arc.** Each session adds one idea. Session 7 closed on three questions across three sessions: who am I paying (7), what may I spend (8), what if you do not deliver (9). Session 8 shipped the second as access policies. The third was never built: the plan on file ties session 9 to x402 instead. See `topic-and-storyline.md`.
- **Write-ups.** A post with the slug `how-ai-agents-pay-each-other-moi` returned 200 on blog.moi.technology on 2026-10-02. Whether its text matches `session-7/BLOG.md` was not compared. Session 8's slug `moi-access-policies-fine-grained-control` returned 404 on the same day, and the previous operator's dependency notes said PR 52 on the website repo holds an old draft. State unknown as of 13 October 2026; check with `gh pr view 52` in the website repo. Session 9's post is a draft with placeholders.

## Not yet known

- Sessions 1 to 8 were held (confirmed by the previous operator on 2026-10-14); 9 was not. The held dates for sessions 1, 4, 5 and 6, and whether a recording of 1, 3 to 6 or 8 exists, are not recorded.
- Whether session 9 is still planned, and under which number the next session runs. ASK: Rahul.
- Whether 0.7.x SDK sessions run on 0.13.0. Rehearse one.
