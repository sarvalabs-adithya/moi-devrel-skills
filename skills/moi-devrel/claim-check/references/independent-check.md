# A second, independent pass

Facts are as of 2026-10-02. House rule 7 in `moi-devrel/SKILL.md` governs this file: sub-agents only when the operator asks for them, in that message. Spawning a run burns the operator's credits, so the default is to do the second pass inline. Back to `../GUIDE.md`.

## When a second pass is worth it
An independent pass was run on the session 7 post, both release posts, the CC13 deck, the x402 specs and a docs PR review, and each time it found things the first pass had missed:
| Date | Run | What the second look found |
|---|---|---|
| 2026-08-07 | Session 7 blog, three parallel readers against SDK source | Two claims FALSE and five OVERSTATED, in a post the author had already checked |
| 2026-08-21 | August release post, 88 agents on 553 claims in two slicings (per paragraph and per package), then adjudication | 521 verified outright. Six narrow errors held (`175a733`). Two claims that could not be verified either way were softened |
| 2026-08-21 | A teammate's docs PR (moidocs #120): Haiku agents verified each claim against go-moi v0.12.0 and js-moi-sdk v0.8.0, then a refutation pass | Findings per file, and a headline count ("27 errors") that disagreed with its own table (26) and list (25) |
| 2026-08-27 | CC13 deck, one Haiku agent per package, eight audited (accurate, imprecise or wrong) | A release candidate written up as shipped <!-- slop-lint: ignore --> |
| 2026-09-10 | September post: a first pass of 200 atomic claims, then 86 changed claims each with a checker and a refuter, then a sweep of 152 claims | The first pass: 187 true, 8 partly, 5 unverifiable, 0 false. The sweep: three corrections (`280ffb2`) |
| 2026-09-10 | Spec design claims, an adversarial sweep | A wrong statement about escrow overturned. Two citations produced by agents did not exist |
Worth it when any of these holds:
1. The text is public and states protocol behaviour: a release post, a spec filed upstream, a deck for a public call.
2. The first pass found any FALSE or OVERSTATED row. More are likely where one was.
3. The text was rewritten after the first pass. Check what changed, with a refuter.
4. Whoever wrote the draft also checked it. Independence needs a different route to the source.
5. A row rests on one source only, or on the release note alone.
Probably not worth it (a judgement, not a recorded rule): a short post that copies the release note verbatim, or a text whose rows are all `verified` from two routes.

## The second pass inline
This is the default. It costs time and no extra credits.
1. Refuter pass. For every `verified` row, try to prove it false by a different route: another file, another ref, the package instead of the node. Write what you tried in `note`.
2. Source to text. Read the release note or the tag's changes and list every item, then check that the text covers each one and says no more. Omissions fall off texts: non-headline packages, point releases, release candidates (CC13), and the recap bullet that left out the notarizing fee payer exception (2026-09-11).
3. Do not read the draft's own justification first. Form the answer from the source.
4. Reconcile every count in the text with every other, and with the ledger (the "27 errors" headline met 26 and 25 on 2026-08-21).
5. Open every citation and link. A link that 404s and a citation that does not exist are both on the record.
6. The operator spot-checks. Offer five rows chosen at random with their sources, and open the source for any the operator doubts. Show the source with every yes: on 2026-09-10 "are you 100% sure" was asked several times about the x402 spec, and a yes without a source did not settle it.
7. Run the companion checks: the reviewer's direction, style, links, internal consistency, code samples (`method.md`).

## When the operator asks for sub-agents
State this first, in one message, and wait for "yes" with a count:
```
Offer: a second pass with N <Haiku or Sonnet> agents, one per <package or paragraph slice>.
Each reads the source and returns ledger rows (claim, source, verdict). They write nothing and send nothing.
It spends your credits. Reply "yes, N" to approve, or "no" and I run the refuter pass myself.
```
- Models. Use Haiku for reading one package or paragraph each and Sonnet for judgement, in small numbers. Do not choose the most expensive model unless the operator names it for a one-off review (one such exception is on record). A run that reached 79 agents was rejected as too many (August 2026, request log). The count is the operator's call.
- One unit per agent: a package, a paragraph, a table. Give every agent the same ledger columns and the same verdict words.
- Agents read only. No push, post, message, download or `.env`. Secrets never go in a prompt.
- After they return: open every citation they give (two cited specs did not exist, 2026-09-10); reconcile counts; adjudicate each disagreement against source, because the six August errors were the ones that survived adjudication out of the flagged set (`175a733`); drop a finding you cannot reproduce.
- Put each agent's rows into the ledger with `checked_by` naming the pass ("Haiku pass 2, adjudicated by Claude"). Say in the hand-back how many agents ran and on what model.

## Not yet known
- The credit or budget limit for checks. Only reactions are on record, no number. ASK: Rahul.
- Who adjudicates a protocol dispute when source and note disagree. Gokul is the protocol contact (inferred from `moi-devrel/references/people-and-teams.md`). ASK: Rahul.
- Whether a standing second reviewer is wanted. A standing QA agent was proposed once and cancelled.
