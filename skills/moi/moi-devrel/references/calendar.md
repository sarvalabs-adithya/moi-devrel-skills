# Calendar: the recurring rhythm

Facts are as of 2026-10-02. "Observed" means a file, log or sheet shows it. "Inferred" means the research reads it from the evidence and no source states it. Where sources disagree the table says so. Convert every time with `time-table.sh` (the command is in the Time zones section; `$SKILLS` is defined in `../SKILL.md`). Back to `../SKILL.md`.

## At a glance
| Rhythm | Cadence | Status |
|---|---|---|
| Community call "The Campfire Chat" | Monthly. Call 13 on Thu 2026-08-27, call 14 on Fri 2026-09-25 (inferred; ASK: Vardan for the sheet). CC15: last week of October 2026, date not set (Vardan) | Observed monthly. Weekday disputed, see below |
| X and Telegram AMA | Monthly, with a weekly slot plan | Observed in Drive sheets and a standup decision |
| MOI Builders webinar | Intended weekly on Fridays, about monthly in practice | Observed |
| Engineering releases | Every 1 to 3 weeks | Observed 14 Aug, 18 Aug, 25 Aug, 10 Sep |
| Release blog "MOI <Month> 2026 Release" | Monthly | Two posts, monthly inferred (ASK: Rahul) |
| Devnet reset | No schedule | `devnet.md` |
| Mailchimp RSS newsletter | Monthly, on the 15th, with every post published since the last one | `project-handover-docs/BLOG.md`, see Weekly and daily comms |
| Update to Rahul | Ad hoc, completed work only | Seen 24 Aug and 10 Sep |
| Marketing standup | About 3 to 5 weekdays a week until 31 Jul, then unclear | Observed |
| AI-visibility numbers | Monthly, same 47 queries | Stated on the call 14 deck |

## Community call
Weekday sources disagree:
| Source | Says |
|---|---|
| Notes from the 2026-08-24 planning call | Rehearsal Wednesday, live Thursday |
| Call 13 | Thu 2026-08-27 (observed) |
| Call 14 | Announcement text pasted 2026-09-24 says "happening tomorrow", so Fri 2026-09-25 (inferred; ASK: Vardan for the sheet) |
| Drive sheet "Community Call + AMA Calender 2026" | Old expectations from early 2026, not a plan for CC15: Fridays, third or fourth of the month: 23 Jan, 20 Feb, 20 Mar, 17 Apr, 22 May, 19 Jun, 24 Jul, 21 Aug, 18 Sep, 23 Oct, 20 Nov, 18 Dec, each with a reserve day a week later |
| Past calls | Call 7 Sat 2026-02-28 at 19:50 IST. Call 8 Fri 2026-03-20. So the sheet drifts |
| Old website homepage fallback and SQL seed (the homepage calendar became a Luma block on 13 October 2026, PR #60) | 14:00 UTC in the code fallback; 18:00 UTC from 2026-05-16 (a Saturday) in the seed file |
Start time is not recorded. Call 13 began about 16:15 IST (inferred). CC15 is expected in the last week of October 2026 and the date is not set (Vardan, `project-handover-docs/COMMUNITY-CALL.md`). The sheet's old expectation was Fri 2026-10-23, reserve Fri 2026-10-30. The sheet has topic, guest and speaker blank for 11 of 12 months, so a reserved date is not a confirmed event. ASK: Vardan for the date, time and platform of call 15.

| When | What | Evidence |
|---|---|---|
| Planning call | Sets segments, speakers and the rehearsal day (24 Aug for 27 Aug) | Observed |
| T-5 to T-2 days | Collect inputs: protocol release note, marketing numbers from Slack, guest details | Observed |
| T-48 hours | Run-of-show and speaker brief. No such document exists in Drive. ASK: Rahul if still required | KRAs, Jan 2026 |
| T-1 day | Rehearsal on Wednesday for Thursday calls. Unknown for call 14 | Planning call notes |
| Deck effort | The call's manager capped it at about two hours. The manager is inferred to be Rahul (ASK: Rahul). Call 14 took about 45 hours over 25 requests | Observed 24 Aug, 23 to 25 Sep |
| Live | Share the deck window in Meet, keep the presenter window (key `P`) on your own screen | Deck README |
| T+24 hours | Notes, recording, resources, action items. Call 13 got a YouTube description with chapters and blog backlinks | KRAs, call 13 |
| T+48 hours | Q&A log and follow-ups with owners | KRAs |
Call 14 has no evidence of a recording, description, recap or follow-up. Skill: `moi-webinar/community-call`.

## AMA, game night and weekly slots
- AMA tab of the same sheet: 9 Jan, 13 Feb, 13 Mar, 10 Apr, 15 May, 12 Jun, 17 Jul, 14 Aug, 11 Sep, 17 Oct, 13 Nov, 11 Dec, with a Wednesday reserve. 17 Oct is a Saturday. Check the sheet.
- Marketing Events Calendar: 39 events planned for 2026 (20 game nights, 10 Telegram AMAs, 9 community calls). The KRAs say two events a month and the programme sheet says one call and one AMA, so check which calendar a number comes from.
- Decision at the 6 and 7 Aug 2026 standups: Wednesday AMA, Thursday AI or developer session (the previous operator's slot), Friday game night. AMAs overran into game night, so schedule the next AMA on Wednesday or Thursday. On YouTube post video AMA clips only (7 Aug).

## MOI Builders webinars
| Session | Date and time | Source |
|---|---|---|
| II Native Assets | Fri 2026-06-12, about 18:22 IST | Gemini notes |
| III Agents on MOI | Thu 2026-06-18, about 18:22 IST, about 50 minutes | Gemini notes |
| IV Swaps | Form created 2026-07-03, session date not recorded | Drive |
| VII Agentic Payments | Fri 2026-08-07 | Drive form dated that day, 6 Aug standup |
| VIII (8-policies) | Fri 2026-09-04, 4:00 pm IST = 10:30 UTC, 60 minutes | `session-8-policies/LUMA.md`, which is gitignored and was local to the previous operator's machine (not recorded elsewhere; the previous DevRel's notes) |
| IX x402 | Planned. Status not recorded (the previous DevRel's notes); ASK: Rahul | |
Roman numerals appear in Drive form names and Luma titles; the repo uses session numbers. The Luma title for session 8 once said VII, so confirm the numeral before publishing.
Per-session pattern (sessions 7 and 8-policies): a call with a lead sets the topic, then a spike on devnet, then the demo is built and verified, about 4 days from topic to live. The Luma page, Meet link and social copy are made the day the topic locks. The proof-of-completion Google Form is created 0 to 4 days before. Buffer posts go out on announcement day, daily Tuesday to Thursday, then T-5h, T-1h and T-30m ("we're live in 30"). Game day checklist runs T-1 day, T-60, T-30, T-10. After: blog within 48 hours (a target; not shown met for session 8), recording to the editor (the session 7 edit took about a month), submissions verified on chain.

## Releases
- Engineering releases (observed): go-moi v0.12.0 Fri 2026-08-14; Voyage 0.8.2 and wallet extension v0.1.4 Tue 08-18; Voyage 0.9.1 and wallet-mobile v1.2.0 Tue 08-25; moipod v0.13.0 announced Thu 09-10 for a network upgrade at 00:00 UTC Fri 09-11.
- On 2026-08-14 Rahul asked in Discord for each service owner to post `service:version:<github-link>`. The marketing team builds the release blog from that list. Vinay posts release logs.
- Release blog: August post merged 2026-08-21, September post merged 2026-09-11 13:04 UTC. No October date exists. ASK: Rahul.
- A pre-release social pack (X thread, LinkedIn, Discord) exists only for v0.13.0, scheduled about 08:45 UTC on 09-10. None for v0.12.0. Whether it is standard is unknown, and the announcement format is disputed. ASK: Rahul for one written example.
- Write the release moment as "11 September, 00:00 UTC (05:30 IST)". Never write "today". The incident behind that rule is in `terminology.md`, table C.
- Early warning of a reset: the daily upstream watch files "Upstream release: go-moi <tag>" in `sarvalabs/moi-mcp`. v0.13.0 came on 09-10 and the wipe was announced for 09-11 (a gap of about a day, inferred; not confirmed to the minute, `devnet.md`; ASK: Gokul).

## Weekly and daily comms
- Mailchimp: the RSS newsletter goes out monthly, on the 15th, with every post published since the last one (`project-handover-docs/BLOG.md`; Vardan holds the login). A post that is live at least three hours before the send is included. Earlier notes say weekly or per post (a weekly blast was set up 2026-08-24); BLOG.md is right. One-off blast to validators 2026-08-28 to 31. ASK: Vardan whether the September post went out.
- Calls with Rahul: transcripts exist for 19 dates across every weekday, only four on a Monday. No fixed weekly day is shown.
- Marketing standup: about 35 recordings from 2026-05-05 to 07-31, about 19:56 to 20:03 IST, about 23 minutes. After 07-31 only Gemini notes exist (Thu 08-06 at 22:00 IST, Fri 08-07 at 18:30 IST). Governance call: Tue 04-14 at 20:29 IST and Mon 07-27 at 21:59 IST; the 08-07 standup calls it a Monday call.
- Metrics: the Metrics tab of the MOI Socials sheet is filled weekly through the week of 2026-09-28. The weekly metrics in MOI Programs are mostly blank after week 9.

## What runs without you
| What | When | Where it shows |
|---|---|---|
| Upstream watch | Daily 03:17 UTC | Issue "Upstream release: ..." in `sarvalabs/moi-mcp` |
| Chain canary | Nightly 02:43 UTC | Issue "Chain canary failing" there |
| Dependabot | npm daily (max 5 PRs, SDK packages grouped), Actions weekly | PRs in `moi-mcp` |
| Launchpad cleanup | 60 s after start, then every 6 hours, inside the app | Log line `[cleanup]` |
| Explorer reconcile | Every 4 hours since PR #5 merged (2026-10-07); whether production runs it was not re-read, so check. Before that `npm run sync` by hand | `GET /admin/sync` |
| Website PR previews | Deleted after 7 days or on PR close | Preview comment |
A GitHub Actions outage or billing block on 2026-08-28 to 08-30 blocked workflows for three days, so scheduled content such as the newsletter may silently not have run. Open the run itself to confirm it happened. Whether anything calls the Points nightly job on its box is unknown.

## Time zones
The audience is announced in IST, the protocol runs in UTC, and operators differ. Write the date, 24-hour UTC and IST, plus the operator's zone, using `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "2026-09-11 00:00" UTC` (time, then zone). The zone is `UTC` or an area/city name such as `America/New_York`. Never write `EST` or `PST`: the script rejects them, because EST is UTC-5 all year and a US Eastern summer time would come out an hour wrong. Example: 4:00 pm IST is 10:30 UTC. A Buffer `--at` value must end in `Z`, or the machine's local zone is used. Read the printed UTC string before confirming. A scheduled Buffer post publishes with nobody reviewing it. Use a draft unless an exact time matters.

## Not yet known
- The real community call weekday, time, platform and host, and whether each call is recorded and posted. ASK: Rahul.
- Whether the Wednesday rehearsal still happens, and whether a run-of-show is still required.
- Whether a release pack is standard, and who confirms the release moment with the protocol team.
- Session 9 status. Who runs the governance call now.
