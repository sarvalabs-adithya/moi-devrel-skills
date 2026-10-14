# Tracking: the plans, weekly metrics and content calendar that were kept, and where

Facts are as of 2026-10-02 (the Drive research), re-dated where checked on 2026-10-03. Everything here lives in the previous operator's Google Drive or in sheets shared with him. None of it is in git, and none was opened by the tools used for this skill except where noted. The sheets hold other people's data and some are owned by personal accounts. The links are not recorded (the previous DevRel's notes); ASK: Rahul for the links and for access. Back to `../SKILL.md`.

## What exists, and where
| Artefact | Type, owner | What it holds | Last dated trace |
|---|---|---|---|
| MOI Programs | Sheet, shared by Rahul | One row per programme (columns: Program Name, Category, Owner, Objective, Description, Outcome, Metrics, Start Date, End Date, Resources Required, Estimated Budget, Comments). Tabs WEEKLY METRICS and CONTENT CALENDAR | Weekly metrics run from week 5 (2026-01-26) to week 15 (2026-04-06), mostly blank after week 9 |
| MOI Socials | Sheet, shared by Sai Kiran | Weekly themes for Moinkee and MOI (weeks 3 to 12), planned versus actual post counts, an intern resource plan, a Metrics tab | The Metrics tab runs weekly from 2025-12-29 and is filled through the week of 2026-09-28 |
| Community Call + AMA Calender 2026 | Sheet, Vardan | Call and AMA dates, 12 rows (`moi-devrel/references/calendar.md`) | Topic, guest and speaker blank for 11 of 12 months |
| Marketing Events Calendar | Sheet | 39 events planned for 2026: 20 game nights, 10 Telegram AMAs, 9 community calls | Not opened in detail |
| MOI Annual Calendar | Drive file, Sujatha | The annual calendar | Listed by title only (355 KB). Its type was not recorded |
| Adithya KRAs | Doc, January 2026 | The previous operator's goals document (the title says "KRAs"): weekly KPIs and 90-day outcome goals per programme. The call timings: run-of-show 48 hours before, notes and recording 24 hours after, Q&A log 48 hours after | No run-of-show document was found in Drive |
| MOI Sprint: Strategic Launch Plan | Doc, January 2026 | Three proposals: the Sprint reward tiers, a Bounty Board, a Forge "Hero App" incubator (`bounties.md`, `forge-cohort.md`) | No evidence any launched |
| DevRel Planning Document Template | Doc, July 2025 | Sections: Executive Summary; Goals and Objectives; Initiative 1, hackathon sponsorships (target events, sponsorship details, outcomes); Initiative 2, a university grant programme (a sum per recipient group paid in two stages, a mentor, output requirements); Resources and Budget; Metrics | A template. No evidence the grant programme ran |
| Marketing Questionnaire | Doc | Who wanted to own what (the previous operator listed Forge, Sprint, awesome-moi, the academia collaboration and general DevRel) | Undated in the research |

## Who owned which programme in the MOI Programs sheet (early 2026)
| Owner | Programmes |
|---|---|
| Adithya (the previous operator, left 14 October 2026) | MOI Forge, Advance; MOI Community Updates (one call and one X AMA a month); MOI DevX monthly hackathon; MOI Sprint (scratched 13 October 2026) |
| Sai Kiran | MOI Forge, Basic; Moinkee |
| Vardan | The podcast; KOL outreach with Louis |
| Rahul | Tech Spotlight |
| Harsh | Galxe |
These are the sheet's own row labels. The research did not record what the Moinkee, Tech Spotlight, Galxe, podcast or KOL rows contain (KOL is the sheet's own term and the research does not define it). Who owns each row now is not known. ASK: Rahul. Which of the rows are still active is not known either (`../SKILL.md`, "State of each programme").

## The metrics each programme tracked
- Every programme: content production, audience growth, engagement.
- Forge, Basic: colleges executed, wallets created, Discord joins, forms submitted, X impressions.
- Forge, Advance: projects onboarded and the pipeline. Its KPIs in the sheet: 1 project onboarded a month, 1,000 interactions a day, 1 demo day a month, 1 Builders newsletter a month, 1 video per project per week.
- Socials Metrics tab: X impressions and engagement, LinkedIn impressions, visitors, clicks, reactions. A second tab stub lists developer-funnel labels: downloaded SDK or CLI, number of technical queries, made a first API call, deployed to testnet (the sheet's word; say devnet in public text), GitHub activity.
- The principle in the Sprint plan: measure outcomes tied to network usage, not completion.

## How the tracking was run (observed)
1. Write the programme plan: summary, mechanism or user journey, requirements, resources, KPIs.
2. Add the programme as a row in MOI Programs, with an owner.
3. Add weekly rows in WEEKLY METRICS.
4. Plan posts in CONTENT CALENDAR. Columns: weekday, date, content theme, assets, content review, asset review.
   Then one column for each channel: LinkedIn, X, Instagram, Telegram, Discord, Other.
   Week 13 had a theme per weekday. In order: App-centric problem; Internet evolution; Missing WHO dimension; AI agents; AK's Insight; Builders Proof; Meme / Community.
5. A parallel plan in MOI Socials, filled weekly by the social team.
Every sheet is edited by hand. Nothing reads them automatically.

## What went wrong
| Gap | Consequence |
|---|---|
| Weekly metrics blank after week 9 and the content calendar carries only "Link" placeholders from week 14 | The structure exists and the data does not. Do not quote a trend from it |
| The KRAs say two events a month, the Programs sheet says one call and one AMA, the Events Calendar plans 39 | A number depends on which calendar it came from. Name the sheet and the date next to every figure |
| Ownership and the sheets sit on personal and individual accounts | A departure removes access. ASK: Rahul to move them to a shared company drive |
| Some figures are never refreshed | Keep a numbers ledger: `cp "$SKILLS/moi-webinar/community-call/templates/numbers-ledger.csv" <your-folder>/numbers-ledger.csv` and give each figure a source and an "as of" date (`moi-webinar/community-call`) |

## A weekly routine (proposed; none is recorded)
1. One owner and one canonical sheet per programme. Write the owner's name in the sheet.
2. Fill the week on a fixed day. A "-" needs a reason in the comment.
3. Write the source next to each figure (a platform export, the explorer, a form count) and the date it was read.
4. Never copy a participant's name, email or wallet into the tracking sheet. Counts only.
5. Before a number goes on a public slide or post, check it with `moi-devrel/claim-check`.
6. Keep the sheets and any export of them out of git (`edu-work/`, `../SKILL.md` Before you start). If a summary is committed, commit counts and dates only.

## Not yet known
- Which programmes are still active, who fills the weekly metrics now and whether they moved elsewhere after April 2026. ASK: Rahul, Sai Kiran.
- Whether the DevX monthly hackathon ran at all. Nothing found. ASK: Rahul.
- Whether the KRAs are still the targets. ASK: Rahul.
- Who holds the Drive folders and the Google account behind forms and Meet. See `moi-devrel/references/keys-and-access.md`.
