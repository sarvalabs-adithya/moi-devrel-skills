# Bounties: the four kinds, how they were tracked, what nobody has written down

Facts are as of 2026-10-03, updated 13 October 2026 for the Points webinar bounty (PR #22). Sources: the Drive research of 2026-10-02 (the content-bounty sheet, read for structure only; the response sheet of Builders session II; the January 2026 Sprint plan), the webinar research and `moi-webinar/references/after-the-session.md`. No payout record exists in any source. Back to `../SKILL.md`.

## Rule one: Claude never pays
Claude does not send a reward, a transfer or a payment, and does not hold a wallet. It prepares the verified list. The operator pays from their own account, after Rahul's yes, and a payment of devnet funds is a GATE that names the paying account. Real money is outside this skill.

## The four kinds
| Kind | What | Tracked in | Rules owned by | State |
|---|---|---|---|---|
| 1. Builders session bounty | A task that reproduces the session's demo | Sessions 2 to 7: one Google Form each, in the previous operator's Drive. Since 13 October 2026: a hand-graded form in the Points app (fields of type interaction hash, link, number or text, points per field), made in `/admin`, Webinar bounties | `moi-webinar` (`moi-webinar/references/after-the-session.md`) and `moi-web-products-ops/references/points-tasks.md` | Live since 13 October 2026 (PR #22). No bounty has been created on production yet |
| 2. Content campaign | Creators publish articles and posts on a topic and submit links | The Drive sheet "MOI Technology - Bounty Content Submissions" | unknown. ASK: Rahul | Sheet created 2026-09-08, modified 2026-09-09, shared on 2026-09-09. Most recent trace of any bounty |
| 3. Sprint-plan proposals | A two-tier "liveness" reward and a Bounty Board of wanted reference apps | The Drive doc "MOI Sprint: Strategic Launch Plan" (January 2026) | unknown. ASK: Rahul | Proposals. No evidence any launched |
| 4. Points dev challenge | Session 8's task: four interaction hashes checked from chain reads, 500 points | The Points database | `moi-web-products-ops` | Deployed but off (13 October 2026). Webinar bounties (kind 1) replace it for ordinary sessions |

Points: a security finding is open on this product as of 2026-10-02. The previous DevRel's note on it is not recorded; ASK: Rahul before touching its admin.

## 1. Builders session bounty
- **Now (since 13 October 2026).** The host creates a webinar bounty in the Points app: `/admin`, Webinar bounties, one to six fields (interaction hash, link, number or text), points per field, required or optional. Members with a linked wallet fill it in, the answers wait in a queue and the host grades them by hand; nothing is awarded by a machine. Steps: `moi-web-products-ops/references/points-tasks.md`, "Run: a webinar bounty". The brief and the announcement: `moi-webinar/references/after-the-session.md`. Not tried end to end on production yet: run one with a real submission before a webinar relies on it.
- **Before (sessions 2 to 7).** The rest of this section describes the Google Form proof form, kept because old response sheets still exist.
- **Purpose (old form).** On-chain proof that an attendee did the session's exercise, so a reward can be checked. It is not a sign-up form. Registration is on the event page.
- **Created** by the previous operator: session II about 3.5 days before the session (2026-06-08), III about 75 minutes before it, IV on 2026-07-03, VII on the day (2026-08-07). Create it by the day of the event at the latest and link it from the event page. Creating a form is a GATE.
- **Fields observed** in the one response sheet that exists (session II, two tabs): timestamp, email, wallet address, then asset ids (tab 1) or a transaction hash (tab 2). Session III asked for an agent id and the owning wallet. Questions of IV and VII are unknown; the tools used could not read Google Forms.
- **Tabs.** A form edited after launch gets a new response tab. Session II's second tab holds a different question set. Read both.
- **No master form was found.** Later forms were probably copies, renamed (timestamps suggest it, nothing proves it). Three untitled forms exist, so an un-renamed copy looks like a stray. A new session does not need one: use the Points webinar bounty.
- **Responses went missing.** Only session II has a response sheet in Drive. For III, IV and VII the destination is not recorded (the previous DevRel's notes); ASK: Rahul.
- **Rewards** are written in the session READMEs and slides (token amounts, one cash bonus). Whether they are still current is not known. Do not quote an amount in a new announcement.

## 2. The content campaign
- **The sheet.** Its own header counts "217 submissions across 103 creators". Columns: creator name, content link, platform (X, Medium, Paragraph, Substack). Names were typed by hand (one carries a "(probably)" note).
- **The brief** is visible only from the titles: delegated authority for AI agents versus API keys, runtime scoping, x402 and payment authorisation, MOI versus other agent-identity projects, "know your agent". No written brief, deadline or reward was found.
- **Counts mislead.** One creator has several rows, and one piece can be posted on up to three platforms, so 217 rows is not 217 pieces and not 103 winners.
- **Ownership.** A teammate compiled it and its owner is a personal Gmail account that the research did not name. The previous operator had view access. A sheet of MOI creators' data should sit on a company account. ASK: Rahul who owns the campaign, who compiled the sheet and whether to move it.
- **Not in the sheet:** scoring, winners, payouts.

## 3. The Sprint-plan proposals (January 2026; quoted as proposals only)
- Two-tier liveness reward: 100 KMOI for a verified deployment, 1,000 KMOI for 500 interactions and 10 unique wallets within 30 days.
- Bounty Board: wanted reference apps listed on DoraHacks, Superteam Earn and Gitcoin, settled by hand, 50,000 KMOI in total and about 2,500 KMOI per accepted app.
- The plan's argument: standard education platforms give "high deployment numbers but low network utilization", so rewards should depend on verified activity, not completion. Which network's KMOI is meant is not stated. Never present these figures to anyone outside the team as an offer. ASK: Rahul whether any of it is live.

## How to verify a submission (proposed: no verifier script exists, and the record shows only manual checks)
**On-chain proof (kinds 1 and 4)**
For a Points webinar bounty the grading happens in `/admin`: a hash answer shows what the chain said about it only when the server has `MOI_RPC_URL`, which is not set on production (13 October 2026), so read the receipt yourself. The steps below are the manual check and apply to old forms too.
1. Read the response tabs for headers and counts. Copy no name, email or wallet into a note, a repo or a chat.
2. For each row, look the id up on the explorer (voyage.moi.technology) or through the SDK. Read the receipt status: a refused transfer still has a hash. "I'm going to verify each and every agent myself" is the previous operator's rule from session III.
3. Check the thing the task asked for: the asset exists, the wallet that submitted it owns or created it, the hash is in the window, one asset is not claimed by two wallets.
4. Record one line per row in a ledger inside `edu-work/` (`../SKILL.md`, Before you start, makes the folder and its ignore rule): row, verdict (verified, rejected, unclear), reason, checked by, date. The ledger names people and wallets, so it never goes in git.

**A content link (kind 2)**
1. Open it. Is it public, on a listed platform, on the brief's topic, original, dated inside the window?
2. Match by link, not by name. Collapse the same piece posted on several platforms to one.
3. Count distinct pieces and distinct creators separately.
4. A piece that says something false about MOI is a policy question. ASK: Rahul. Check its MOI claims with `moi-devrel/claim-check` before anything is praised or reposted.
5. Record as above.

**Announcing a bounty**: say "coming" until its deploy steps are done (the 2026-09-03 checklist). A brief states the task, the proof and where to send it, the deadline as a date with UTC and India time (`bash "$SKILLS/moi-devrel/scripts/time-table.sh" "<YYYY-MM-DD HH:MM>" Asia/Kolkata`; it reads the time as India time, so give `UTC` as the zone if you decided it in UTC), the reward and its currency, who verifies, how and when it is paid, what disqualifies a submission, and how the data is handled. No bounty on record states all of these. Posting it is a GATE.

## Not yet known
- Who owns bounties now, and the budget. ASK: Rahul.
- Reward amounts that still stand, who pays, from what account, and where payouts are recorded. ASK: Rahul.
- How the content campaign scored entries, who won and whether anyone was paid. ASK: Rahul.
- What the forms of sessions III, IV and VII asked and where their answers went. Not recorded (the previous DevRel's notes); ASK: Rahul.
- Whether the Sprint-plan proposals and the content campaign are one programme.
- Whether eligibility rules, tax or identity checks exist. Nothing in the sources mentions them. ASK: Rahul.
