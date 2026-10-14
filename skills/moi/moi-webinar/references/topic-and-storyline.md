# Topic and storyline

Facts are as of 2026-10-02. How two topics were chosen and turned into a storyline, the series plan on file, and what has been covered. Sessions 1 to 6 have no record of how their topics were chosen. Back to `../SKILL.md`.

## How a topic was chosen (observed)

- **Session 7.** A strategy call on 4 Aug 2026 set the rules. A dev talk carries one idea ("if you give everything in a single dev talk, everyone will lose it"). Every dev talk gets a blog post, aha first and how-to second. The lead asked for the storyline in writing as phase one, two and three, and for it to be sent for review.
- **Session 8.** A short call with the lead on 31 Aug 2026 (9:47, 7 minutes) replaced the first design. The new topic came from a docs pull request on access policies (`sarvalabs/moidocs` PR 120, files `access-control.md` and `access-policy-tutorial.md`). Its status on 2026-10-02 was not checked. ASK: Gokul.
- **The lead** in this skill is the person who sets the topic on a call. The 4 Aug call summary calls that person "the manager", and session 7's own `STORYLINE.md` says Rahul left part 3 open on that call. The record names nobody for session 8's call. ASK: Rahul who sets the topic now. The timing is fixed: DevRel and Rahul finalise the project idea 9 days before the session (`project-handover-docs/DEV-WEBINARS.md`).
- **Who signs off a topic** is not recorded. Two reviewers appear by first name: Rahul, who supplied the narrative framing and asked for the deck and the post, and Ram, who rejected the first session 8 design (role not stated). ASK: Rahul.

## The procedure

1. Restate the call in plain words before anything is built. Ask for the plan "in plain English" and reject jargon. Show it to the operator.
2. Write the one-line story, and for each session the idea it adds and the aha. Use `../templates/STORYLINE.md`. Say what is deliberately not said yet.
3. Decide scope by subtraction. Session 7 took "just do a value transfer" as the floor for part 1 and deferred the budget machinery until it was the point.
4. Read the sources, not memory: the docs pull request, the installed SDK package, the earlier session folders. Read installed types before writing code against them.
5. Write the design as options with a recommendation and a fall-back (session 8, first design: allowance as the spine, a budget logic on top, "if we have to pick one: A").
6. List what must be proven live as a checkbox list. Nothing ships as "reasoned".
7. Spike on devnet before any agent code. A spike proves or kills the mechanism in one small script (`demo-standard.md`). If it does not behave, the plan changes on day one.
8. List the open questions and send them to the reviewer through the operator.
9. When the reviewer rejects a design, keep the old build on disk and write down why in `NOTES.md`. Do not delete it.

## Rules

- **One idea per session, and nothing before its turn.** Say which phase this is and that the platform has a bigger scope coming.
- **Each session adds one idea and removes none.** Session 7 was identity and payment, session 8 added authority, session 9 was to add a standard. Close each session with the next session's question.
- **State the honesty guardrails before the build.** They constrain every line of stage copy. Examples in `demo-standard.md`.
- **A hole the narration has to cover is a reason to change the design.** On session 8 the first design carried a known hole ("hole 2") into the build with a line of narration over it. The notes call that "the actual mistake". The reviewer's objection stood: a rule an agent can route around is voluntary.
- **Spiking first probably made the pivot cheap (inferred).** The new demo was verified end to end on the day of the pivot, 31 Aug 2026, and the research reads that as the spike habit having exposed the holes early. The first design was built twice (24 Aug and the morning of 31 Aug) before it was dropped.
- **Aha first, how-to second** is the order for the write-up and, in practice, for the talk (`moi-blog` owns the post).
- **Positioning words** and the corrected terms come from `moi-devrel/references/terminology.md`, and only from there.

## The series so far

| Phase | Session | Idea | Aha |
|---|---|---|---|
| Fundamentals | 1 to 6 | Coco and the SDK, native assets, the agent registry, swaps, NFTs, context inheritance | No aha statement is on record |
| Part 1 | 7 | Identity and payment | You can find an agent by what it sells and pay it with no prior relationship, and the registry tells you whose address it is |
| Part 2 | 8 | Authority | The chain refuses what the owner never permitted: the same call, refused, allowed, refused |
| Part 3 | 9 | A standard (planned) | Any x402 client can read the invoice. Only a client that implements the scheme can pay it |

The first plan for part 3 was conditional settlement: money moves only when the goods arrive, built on MOI's native lockup and release, with the buyer made whole if the seller fails to deliver. The lead had left part 3 open on the 4 Aug call ("you do something else"). The plan on file for session 9 is the x402 envelope instead. It rests on session 8's allowance, which was dropped, so it needs a new plan before anyone builds it. Which plan is current: ASK: Rahul. Session 7's storyline and facilitator note, which hold the conditional settlement plan, are in the handover repo at `others/webinars/session-7/`.

## What has been covered, and what has not

Built on file (whether each was held is in `session-history.md`): Coco and the SDK; native assets (MAS0, a logic-backed TaxToken, MAS1 NFTs); the agent registry and a third-party framework; swaps with lockup and release; context inheritance; agentic payments; access policies; an intro to MOI with the Agent Launchpad. File locations are in `session-history.md` too.

Not covered anywhere on file: conditional settlement as a talk, and x402 as a talk. No topic list for later sessions exists. ASK: Rahul for the next topic and for a session number: the numbering after 8 is not settled, because 9 is only planned.

## Notes for the lead's review

Send the storyline, then the open questions, before building. The 4 Aug storyline went out for review and its open question was an honest one: the build did more than the agreed floor. Say plainly where the build goes beyond what was agreed, and ask.

## Not yet known

- Who signs off a topic, and Ram's role. ASK: Rahul.
- Whether a topic backlog exists. None is in Drive or the repo.
- Whether the weekly cadence is still intended. The plan said Fridays, the practice was about monthly, and the 6 Aug standup kept Thursday free for the developer session (`moi-devrel/references/calendar.md`). ASK: Rahul.
