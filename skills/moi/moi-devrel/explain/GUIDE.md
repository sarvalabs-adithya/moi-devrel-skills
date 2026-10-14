# moi-devrel/explain: Teach a MOI concept

Branch of `moi-devrel`. `$SKILLS`, the operator, `ASK:`, the house rules and the gates are in `moi-devrel/SKILL.md`; this guide adds what is specific.

## What this covers
The operator is new to MOI and must present, build on, write up or file something that rests on a mechanism they cannot yet say in their own words. Claude teaches it top down from the end use, checks every sentence against a named source, and stops only when the operator can say it, walk an example and answer the likely questions or say "I will check". This is step 2 ("Teach") of the standing loop in `moi-devrel/SKILL.md`. Explaining before building was the most frequent kind of request in the previous operator's log as of 2026-10-02 (`moi-devrel/references/orientation.md`).
Not covered: the definitions, which live once in `moi-devrel/references/glossary.md` and `moi-devrel/references/terminology.md` (this branch points to them and never restates them). Checking text that will go public is `moi-devrel/claim-check`. Scripts and decks are `moi-webinar`, `moi-webinar/community-call` and `moi-webinar/deck`. Docs pages are `moi-docs`. A call transcript is `moi-devrel/call-digest`. Operating a product is `moi-launchpad-ops`, `moi-mcp-ops`, `moi-launchpad-ops/explorer` and `moi-web-products-ops`.

## Before you start
Run commands from the working copy of the repo the operator is working in. Teaching happens in the conversation; files are optional.
- [ ] The concept, in the operator's words, and what happens once they can explain it: present it, build on it, write it up, file it, or answer questions about it. The operator provides it. Ask: "Which concept, and what will you do with it next?"
- [ ] The artifact behind it, if any: a pull request, a docs page, a release note, a code file, a deck. The operator provides it. Ask: "Is there a page, pull request or file this comes from?"
- [ ] The depth: say it, present it or defend it. The operator and you agree it (`references/levels.md`). Ask: "Do you need to say it, present it or defend it?"
- [ ] Source access. Public docs, the SDK and read-only devnet reads need none. The node, runtime and compiler source are private as of 2026-10-02. The operator provides it. Ask: "Can you read go-moi, go-pisa and cocolang?" If not, ASK: Rahul who can grant read access. Without it, anything beyond the docs and the release note ends as "I will check".
- [ ] Whether the words will be repeated in text that leaves the team. The operator provides it. Ask: "Will any of this be said or written outside the team?" If yes, step 9 applies.

## The run
`SLUG` is a short lowercase name for the concept, for example `fee-delegation`. Step 10 uses it.
| # | Step | What to do | Where | Done when |
|---|---|---|---|---|
| 1 | Intake | Restate the concept and what the operator does next, in one line. Pick the depth | `references/levels.md` | The operator says yes to both |
| 2 | Their picture | Ask the operator to say what they think it is, in their own words, before you teach. If they know nothing of it, say so and go to step 3. Otherwise listen for the wrong pictures people bring, from other chains and from early MOI material | `references/misconceptions.md` | Each wrong picture is named, or none is found, or the operator has no picture yet |
| 3 | Read the sources | Open the authority for the concept and read it. For anything "live", read the node, read-only. Label each sentence you will say: doc-derived, source-derived, receipt-proven or "I will check" | `references/concept-paths.md`; live reads in `moi-devrel/claim-check/references/live-reads.md` | You can name the source of every sentence. A term the glossary lists as undefined is an ASK, not a guess. A concept with no block in that file: use its section "A concept with no block here" |
| 4 | End use | One or two sentences: who can now do what, and what changes for them. No term the operator has not met | `references/method.md` section 2 | The operator can say why it exists |
| 5 | Mechanism | Numbered steps, one idea each, one section per turn. Define each term at first use, in MOI words, with the sense of its glossary row | `references/method.md` section 3 | The operator says "next" or restates |
| 6 | Example with named actors | Two or three actors and what each holds before and after. Prefer a real interaction: read a hash that exists on the current devnet (free, read-only; take one from the explorer at voyage.moi.technology or follow check 4 of `moi-devrel/claim-check/references/live-reads.md`; hashes in older notes predate the 2026-09-11 wipe), otherwise say the example is constructed. Running a new one spends devnet funds and signs with a recovery phrase: GATE, and the operator runs it (a wallet step) | `references/worked-examples.md` | The operator can walk the example without notes |
| 7 | Restate check | The operator says it back, usually as "so ... right?" (ask for one if none comes). Answer yes or no first, then fix exactly what is wrong, checked against the source and not against your earlier answer | `references/method.md` section 5 | Every part of the restatement is marked right |
| 8 | Edges | Say what it does not do. Name the wrong pictures that bite here | `references/misconceptions.md`, `references/traps.md` | The operator states the limit without prompting |
| 9 | Defend it | Three likely questions with short answers, each with its limit and its source. List what is to be checked and who can settle it. If the words will be said or written outside the team (the blog, a deck, X, Discord, a call), run `moi-devrel/claim-check` before they go out. An explanation that stays in this conversation does not need a ledger, but every sentence still has its named source from step 3 | `references/defend-it.md` | The operator answered each question or said "I will check" and knows who settles it |
| 10 | Written copy | Only when the explanation is big or the operator asks. Index first. Local and self-ignoring. From the root of the working copy, set `SLUG` (for example `SLUG=fee-delegation`), then run `D="explain-${SLUG:?set SLUG}" && T="${SKILLS:?set SKILLS}/moi-devrel/explain/templates/explainer.md" && mkdir -p "$D" && printf '*\n' > "$D/.gitignore" && cp -n "$T" "$D/explainer.md"` (the two `:?` checks stop the command if a variable is empty; `cp -n` never overwrites a file you have filled in, so a rerun exits 1 on macOS and changes nothing) | `templates/explainer.md` | The file exists in the working copy and `git status --short` does not list it |
| 11 | Hand back | The format at the end of this file | none | The operator has read it |

## Which file to read
| Doing | Read |
|---|---|
| Teaching anything: the order of moves, the restate loop, pacing | `references/method.md` |
| Choosing how deep to go, one concept at three depths | `references/levels.md` |
| Which order to learn a concept in, and where its authority is | `references/concept-paths.md` |
| A model explanation, and what made it work | `references/worked-examples.md` |
| What the operator thinks it is, and the correction | `references/misconceptions.md` |
| Preparing for questions from an audience or a reviewer | `references/defend-it.md` |
| Anything that went wrong before | `references/traps.md` |
| Writing the explanation down | `templates/explainer.md` |
| Testing a change to this branch | `evals/evals.md` |

## Facts that fail silently
The full list is `references/traps.md`.
| Rule | The incident |
|---|---|
| Check each sentence against a named source before you say it. A fluent explanation can be wrong | 2026-08-26: the previous operator told the assistant it had been wrong about two things on x402 and ordered research first. 2026-09-11: drafts said an account pays in KMOI for "everything" |
| Test every universal (only, every, nobody, always, never, free) for one counterexample | 2026-08-07: "only the owner can move funds" was false, because MAS0 has Approve, TransferFrom, Lockup and Release |
| The source tip, the release note and devnet are three different things. Read the node before "live" | 2026-09-10: devnet answered `payer` and 0.12.0 while the tip had `fee_payer` |
| A correction must reach every copy, your own explainer included | The false custodian claim was proved false on 2026-08-07 and was still in six session 7 files on 2026-10-02 |
| Use MOI terms and MOI context. Generic analogies from other companies were rejected | 2026-08-27: "don't talk about Stripe". 2026-09-11: "the token" and "the fee" | <!-- slop-lint:ignore -->
| Short, one section per turn, the question asked. A wall of text gets asked again | 2026-08-21: paragraphs and a menu of options were rejected for brief answers and the actual decision |
| A term the glossary lists as undefined is not yours to define | 2026-09-09: a kill switch docs page was deleted because it did not say what the feature is |
| Say what is real and what is constructed | Demos run on real devnet interactions; a simulated step is said to be simulated (house rule 5) |
| Never read, confirm or repeat a recovery phrase in a walkthrough | 2026-09-24: a phrase read on a screen share reached the meeting notes |

## Gates
Every gate in `moi-devrel/SKILL.md` applies. Explaining, reading docs and read-only node reads are free. These are the ones teaching meets most:
- Running a demo, deploying a logic, creating an asset or any interaction that spends devnet funds. Name the paying account and the cost when you ask. Signing loads a recovery phrase, so the operator runs it in their own terminal and pastes the output.
- Sending any question to Gokul, Rahul or anyone else: Claude drafts, the operator sends. Telling anyone an explanation is "verified" before `moi-devrel/claim-check` says so.
- Committing or pushing an explainer: `moi-foundation/MOI-Webinars` is public as of 2026-10-02, so a push publishes. An explainer can name private source and reviewers, so step 10 keeps it self-ignoring.
- Sharing the explainer or a diagram file in Drive, Slack or any cloud storage. Downloading a file: name it, its source and its size first.
- Recovery phrases: a wallet step is the operator's. If a phrase is pasted or read aloud in a walkthrough, do not repeat it and say it is exposed.

## Keys and access
Names only. Explaining needs no key. Reading the node, runtime and compiler source needs GitHub read access to `sarvalabs/go-moi`, `sarvalabs/go-pisa` and `sarvalabs/cocolang` (private as of 2026-10-02; ASK: Rahul who grants it). A live demo needs a funded devnet account in the MOI Wallet extension. The operator creates and funds it (the faucet funds accounts that already exist, `moi-devrel/references/devnet.md`), and Claude never handles its recovery phrase. Where each credential lives: `moi-devrel/references/keys-and-access.md`.

## Hand-back
```
Taught: <concept> at depth <say it | present it | defend it>, for <what the operator does next>
Can say it: yes or no, with the operator's restatement marked right or wrong
Can walk the example: yes or no
Questions: <each likely question answered, or "I will check" with who settles it>
Sources read: <pages and files with dates>. Not read: <private source, live read not done>
Open: <numbered ASK lines>
Ready: yes or no, because <one reason>
```
Ready is yes only when the operator has restated the concept in their own words and every part was marked right, has walked the example, and has answered or parked each likely question. A to-do is labelled as one.
