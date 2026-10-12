# Method: from a transcript to decisions, owed work and open questions

Facts are as of 2026-10-03. The rules in this file are this branch's method. The incident behind each is in `traps.md` or in the row it names. "The operator" is the human working with Claude now. Adithya Ganesh is the previous operator. `ASK: <person>` is defined in `moi-devrel/SKILL.md`. Back to `../GUIDE.md`.

## 1. Read all of it first
1. Work from the clean copy (`transcript.clean.txt`), never from the original. The line numbers are the same in both.
2. Read from the first line to the last before you write a single entry. Then a point settled early and changed later appears once, in its final form. Note the order of topics, one line each.
3. Compare the last timecode in the report with the end of the call. If the file stops before the call did, say so in the digest under "Not captured". Large Drive documents can come back truncated.
4. A Gemini notes document has an auto summary above the transcript. The report names the section lines ("Summary at line 3, Transcript at line 61"). Read the summary after the transcript, as an index. Each item in Summary, Decisions or Next steps must have a line in the transcript, or be labelled "auto summary only" in the digest. Gemini asks the reader to review its notes and assigns next steps by name, so those names are guesses until you find the words.
5. Two documents for one meeting: Gemini made two notes documents nine minutes apart for Builders II (2026-06-12), probably a Meet started twice (inferred). Use the longer one, and say which.
6. A recorded Meet also saves a Chat text file. It is not part of the transcript, and the research does not record what it holds. Ask the operator for it and read it as what was typed during the call (inferred).
7. If the operator was on the call, ask which parts they spoke. Their own spoken updates are in the same recording and become their commitments.

## 2. Decisions before tasks
A decision is something chosen that changes what will be done, said, built or owned: a scope, an order, a date, a name, a wording rule, an owner. A task is something a named person will do. Talk that is neither goes in neither list.

Every decision gets one status:
| Status | Use it when | Example of the words |
|---|---|---|
| decided | A person with authority for that area states it as chosen, or the group agrees aloud and nothing later in the transcript reverses it | "OK, we do X" followed by agreement |
| proposed | Said once, no agreement heard, or said by someone whose authority you cannot tell | "maybe we should", a suggestion with no answer |
| deferred | The call parks it: "later", "next time", "after the release", or the topic stops with no outcome | "let's come back to it" |

Before you mark something decided, search the rest of the transcript for its key word or number. A reversal after the decision turns it into the later form, and you quote both.

Authority is by area, as far as `moi-devrel/references/people-and-teams.md` shows it (titles are not stated there: ASK: Rahul): Rahul sets direction and reviews public pieces, Gokul answers chain and protocol questions, Upendhar anything on a VM, Sai Kiran community numbers, Vardan call dates and guests. A suggestion from the person who reviews your work is a request, and often work. It is still a request until the transcript shows it was agreed or the operator says so. Write "asked for" for a request, "decided" for a decision. The previous operator asked for these separately: what a person said, what was asked for against what had been done, and what was decided.

A decision about how MOI is described (participant-centric, network ID, who builds and who governs) is recorded in the digest with its date and speaker. The digest does not edit `moi-devrel/references/terminology.md`; a contested row there is settled by Rahul (ASK: Rahul).

## 3. Feedback, requests and quotes
1. When the operator asks "what did X say", answer from the transcript only, in the speaker's words, with the line number and timecode. Do not summarise. Name the source first: "From the transcript you gave me, not from the review."
2. Quote exactly what the clean copy says. Do not tidy grammar. If the words look mis-heard, quote them as written and add the check in brackets: `"the Moy network" [transcript reads Moy; MOI?]`.
3. Quote for anything contested, any decision that changes a plan, any figure, any date and any name of a person or product. Keep a quote to the sentence or two that carries the point.
4. Keep the speaker's label with the quote: `Speaker 2 (inferred: Rahul), 0:21, line 12`.
5. Feedback is a list: one numbered line per point, in the order said, each with its quote. Do not merge two points.

## 4. When the speaker is not labelled
Labels come in three kinds: a name, a number ("Speaker 3"), or nothing. A number is not a person. Do this in order:
1. Read the Speakers part of the report: which labels exist, how many turns, and what share of the talk. An Otter file may carry its own shares in the header ("Speaker 1 (62%)"). A share is a hint, not an identity.
2. Ask the operator who was on the call, and which label is theirs. Their own turns are the fastest anchor. Ask for a role or a first line for the others: "Who opens at 0:21?" If the operator was not on the call, they cannot answer: ASK: Adithya (or Rahul, if he was on it) and leave the label unmapped until then.
3. Look for evidence in the text: a person addressed by name who answers next, an introduction, "I'll do the DevRel updates" said by the one who presents. Write the evidence beside the mapping and label it inferred. Example: in the 2026-08-04 Otter file the research took Speaker 3 to be the previous operator and Speaker 2 the person who directs (inferred to be Rahul). Both were inferences. That file exists only on the previous operator's machine, in an ignored folder, not on GitHub (checked 2026-10-03). ASK: Adithya for a copy.
4. Keep the original label in every quote, as in section 3.
5. For a decision, task or figure from a speaker you cannot map: owner "unlabelled speaker", status proposed, and an open question "who said this" with the operator as the one to ask (ASK: Adithya if the operator was not on the call). Never fill in a name from style, or from who usually decides.
6. If the file has no labels at all (the report says so), every "I" is unattributed. List the work as "owner not stated" and ask the operator to read the lines and name the speaker. On 2026-08-24 the speaker of "do protocol updates" had no label. `moi-webinar/community-call` records that speaker as unlabelled and takes the slide owner from other requests (inferred there).
7. Names that repeat or look alike: the roster holds Harsh Gupta and Harsh Rastogi, plus a Harsh tied to Galxe who may be Rastogi, and Rahul, Ram and Rishal share a first letter, so a transcript can swap them (no mix-up is on record). Ask which one before assigning anything. `mishearings.md` section E.

## 5. Owners
1. "I will", "I'll", "I can take that": the speaker, once mapped.
2. "X will", "X is going to": X. "X, can you": a request to X. It is a task only if X agrees in the transcript.
3. "We should", "someone needs to", "we need": unassigned. Do not give it to the operator because they were there.
4. "You" is the person addressed, only when the transcript shows who. Otherwise unassigned and an open question.
5. Direction: mark each task as owed by the operator, owed by someone else to the operator (waiting on), or unassigned. Work promised by another team is real work to track. Example: on 2026-09-14 an endpoint to expose the network ID was promised the same day. On 2026-10-03 a read-only `net.NetworkID` call to the devnet RPC returned error -32601 (method does not exist) while `net.Version` returned 0.13.0, so it was not live (`moi-devrel/references/devnet.md` has the call). ASK: Gokul.
6. One verb and one object per task. Split a sentence that carries two.
7. Do not invent a task the call implied but nobody said. Put it in open questions.
8. Work already done on the call goes in a short "done already" line, not in the owed list.

## 6. Dates and times
1. Write the date the speaker gave, as a calendar date from the call date (`YYYY-MM-DD`), with their words in quotes: `2026-10-09 ("by Friday")`. Say the call date and its zone at the top of the digest. A weekday is computed, then both are written.
2. If the speaker gave no date, write `no date given`. Never infer a deadline from urgency or tone.
3. A time of day is written as a date, 24-hour UTC and IST. Run `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "<YYYY-MM-DD HH:MM>" <area/city>` and echo its result. A zone is `UTC` or an area/city such as `America/New_York`, never `EST`. `time-table.sh` rejects 12-hour forms (the incident behind that is in `moi-devrel/references/terminology.md`, table C). It also rejects abbreviations such as EST, because a fixed-offset name ignores daylight saving. <!-- slop-lint: ignore -->
4. The title of a Gemini document carries a zone ("Meeting started 2026/09/24 13:53 EDT"). A governance call titled "8:30 PM IST" started at 20:29 IST. Convert before comparing two calls.
5. A date said on a call is a plan until its owner confirms it. Call dates belong to Vardan, who owns the call calendar sheet; confirm with Rahul. A reserved date is not a confirmed event.
6. Do not copy "today", "tomorrow", "last Friday" or "since the last call" into anything that outlives the day. Replace each with a date.

## 7. Open questions
List, with who could answer each:
- a question asked on the call and not answered;
- a disagreement left standing;
- a figure given twice differently in one call (quote both and name neither as right);
- an "I'll check" with no result;
- a name, product or amount that the check could not settle;
- a task the call implied and nobody took.
For a person or role the library does not settle, write `ASK: <person>` using `moi-devrel/references/people-and-teams.md`. For history, `ASK: Adithya`. Never send the operator a question a new person cannot answer.

## 8. Names and figures: the check mark
Everything taken from auto-notes starts as "check" in the digest. Take it off only when its source is named.
| Item | Check against |
|---|---|
| A person | `moi-devrel/references/people-and-teams.md`; for anyone not on it, the operator if they were on the call, otherwise ASK: Rahul |
| A MOI product or term | `moi-devrel/references/terminology.md`, `glossary.md`, `mishearings.md` |
| A version or "is it live" | `moi-devrel/references/devnet.md`, section "Before you say live". Keep an `-rc` suffix. A source tip is not live |
| An amount | The live source (the faucet amount is quoted as 20K and as 100K in different documents). Recompute any sum. Check the unit: 1 KMOI is 1,000,000,000 anu |
| A date or time | Section 6 |
| A repo, PR or file | The repo itself, read-only |
Do not change the transcript silently. The digest says what was heard and what it was read as. Anything that will be said in public, in a post, a deck or a filing, goes through `moi-devrel/claim-check` before it is used. Do not put a private source path or an unmerged feature into public text.

## 9. What to do with the work
Only after the operator says what to do, and with a yes for each step that leaves the machine:
| Work from the call | Skill or branch that owns it |
|---|---|
| Change a deck, line-up or call script | `moi-webinar/community-call` or `moi-webinar/deck` |
| A webinar topic, demo or session write-up | `moi-webinar` |
| A blog post, a social post or the newsletter | `moi-blog` (its release pack for a release) |
| A docs page | `moi-docs` |
| Check a claim before it goes out | `moi-devrel/claim-check` |
| A commit, pull request, rebase or merge | `moi-devrel/ship` |
| A message to DevOps, the protocol team or a reviewer | `moi-devrel/references/house-style.md` section 4, `moi-devrel/templates/messages.md` |
| Something to redo after a devnet reset | `moi-devnet-reset` |
| A product's operations | `moi-launchpad-ops`, `moi-mcp-ops`, `moi-launchpad-ops/explorer`, `moi-web-products-ops` |
| A decision the operator does not follow | `moi-devrel/explain` |
All of these skills and branches exist as of 2026-10-04 (the tables in `moi-devrel/SKILL.md` list each). Point to one by name and by what it owns; name a file in it only when you have checked that the file exists.

## 10. When a decision needs the operator
State the actual decision, never a description that one exists. In a few lines: the decision, the options, a recommendation, and the consequence of each. On 2026-08-21 the previous operator answered a note about a post that "reverses a scope decision recorded earlier" with "give me the actual decision to make". Write it so:
```
Decide: <the question, in one sentence a person could answer yes or no to>.
Options: A <...>. B <...>.
Recommendation: <A or B>, because <one reason from the transcript>.
Consequence: A <...>. B <...>.
```

## 11. Before you hand over
1. Every decision has an ID, a status and a quote.
2. Every task has an owner (or "unassigned"), a date (or "no date given"), a direction and a source line.
3. Every name, version, amount and date is marked check or has its source named.
4. The privacy findings of the report were told to the operator, and the digest holds no secret and no recovery word. Run `secret-scan.sh` over it.
5. The Brief fits on one screen and the "Needs your decision" list is complete.
6. The digest says which document it came from, so the review is not confused with the transcript.

## Not yet known
- Whether the calls with Rahul have a formal schedule or a standing agenda. ASK: Rahul.
- Whether Otter or Gemini keeps a list of attendees with the transcript. The research saw invite lists in Gemini notes, which are not the people who spoke.
- Who owns the recordings and notes in the shared accounts. ASK: Rahul.
