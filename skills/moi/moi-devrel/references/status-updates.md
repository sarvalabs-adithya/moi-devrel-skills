# Status updates

Facts are as of 2026-10-02 (the date of the evidence) unless dated. Sources: the people-and-comms process and corrections log of the request-patterns research, the docs and standards research, `consent-and-identity.md` and `calendar.md` (in this folder). Quoted words are the previous operator's, cleaned of typos. `ASK:`, `$SKILLS` and "the operator" are defined in `../SKILL.md`. The shapes are in `house-style.md` section 4; draft 12 of `../templates/messages.md` is the status. Back to `../SKILL.md`.

## Who gets one, and how
- **Rahul** gets updates ad hoc. Two are seen, on 2026-08-24 and 2026-09-10. No fixed day is recorded. ASK: Rahul whether he wants a regular update and on which day.
- After a devnet reset the people to tell are DevOps (wallets, the VM), the protocol team (to confirm) and users in Discord (`devnet.md`, "First hour after a reset", and `moi-devnet-reset/references/telling-people.md`). Whether Rahul gets a status then is not recorded. ASK: Rahul. The wording rules here apply to each. The order of work is in `moi-devnet-reset`.
- Channel: the 2026-09-10 update went through Discord, where a long message was turned into an attachment, and a Google document was chosen instead (the text was probably the status update; inferred). The 2026-08-24 update may have gone through Slack (the research cites the same prompt for both). ASK: Rahul which channel he wants. Putting the detail in a document is right when it will not fit one screen. Uploading or sharing the document is a GATE. Send a short message with the link.
- A status to the community or in public is public copy (`moi-blog`). Not here.

## The rule
List only work that was done. Label every to-do as a to-do. Say what was not verified.
Incident (recorded): on 2026-09-10 a draft status line said the organisation descriptions on Crunchbase, LinkedIn and GitHub had been standardised, to match verbatim. They had not been. The previous operator: "we didn't do this, why are you lying". The line was removed and planned work went in a separate next-steps part. Whether the draft had been sent is not recorded.
Related corrections of the same day:
- The website's JavaScript fix went in as a to-do, and the website itself as almost done. Read as: work that has not landed is a to-do (inferred). The fix is read as the one that makes page content visible to crawlers that do not run JavaScript (inferred).
- Be specific about what changed, in the reader's order: content changes and the headings that were reframed, then frontmatter, then `llms.txt`, then `robots.txt`. "Improved the docs" says nothing.
- "Almost done" is allowed when the same sentence names what remains (inferred from the two corrections above).

## Building it from the record
1. Make the list from the record, never from memory or from the plan. Use plain `git log` and `git status` in each repo and the files themselves. A read-only look at a pull request page is fine for a status update. Leave no comment and make no call that notifies anyone. On audit and handover work use plain git only.
2. Give each item its evidence: a PR number with its state, a commit id, a URL you read today with the UTC time. An item with no evidence is a to-do or not verified.
3. Choose the word. Merged, deployed and live are three states. Merging deploys Website, Dataroom and Explorer (`main`), Launchpad (`master`) and Points (`feature/ci-cd`); merging `moi-mcp` deploys nothing (as of 2026-10-02, `repo-map.md`). Write "live" only after you read the live address. A green workflow run proves little.
4. Give the review state: open, changes requested, approved, or waiting on a named person since a date.
5. Reconcile the counts. A report on 2026-08-21 said 27 errors, held 26 in its table and 25 in its list. Recount after every edit.
6. Label each to-do: not started, started, or blocked on a named person.
7. Fill "Not verified" with what you assumed or did not read, including anything simulated.
8. "Needs from you" holds decisions (shape 7 in `house-style.md` section 4) or questions (shape 4), each with your recommendation.
9. Read it as Rahul would. He should be able to answer each point in one line.
10. Run `python3 "$SKILLS/moi-devrel/scripts/check-message.py" --to status comms-drafts/<file>`. It warns on future tense outside a To do section, on a Done line with no PR, commit, URL or date, and on a draft with no To do or Not verified line.

## The shape (draft 12)
Done, with evidence. Partly done, with what remains. To do, with who and by when. Not verified. Needs from you. Plain text, no em dash, no emoji. Omit an empty heading.

## What past updates looked like (recorded)
- The docs sweep status of 2026-09-10 used these sections: Content changes, Frontmatter and metadata, llms.txt, robots.txt, Entity presence, Analytics, Audit scores, Status per property. Its property list on that date: js-moi-sdk docs PR #150, cocolang.dev PR #12, voyage explorer PR #447 and voyage docs PR #5 up for review, the moi docs mostly done, moi.technology almost done.
- The daily update that carried the x402 review link on 2026-09-10 opened with how many pull requests the package held, then how accepted chains had been researched (Stellar was named), then the Drive link. Plain text, no em dashes. Whether it was the same message as the docs status is not recorded.

## Words that overclaim
| Say | Not | Because |
|---|---|---|
| "written" or "changed" | "fixed" | A fix is proven by a read or a run |
| "merged, deploying" | "live" | Live needs a live read (`devnet.md`, "Before you say live", for the chain) |
| The count and the list | "all", "every" | Recount, and test a universal with one counterexample |
| "read in source" or "run on devnet" | "verified" | "Verified" never covers what has not run (standards research) |
| "simulated" | nothing | Demos and tests use real devnet interactions. Say plainly when something is not one |

## When a status was wrong
Correct it at once and plainly, in the same channel: what you said, what is true, what happens next (draft 14). Do not delete the first message. No past wording of a correction is recorded.

## Not yet known
- Whether Rahul wants a regular update, its day, a fixed format and a channel. ASK: Rahul.
- Where long updates should live. A Google document was chosen once.
- Whether the 2026-08-24 update still exists: not recorded (the previous DevRel's notes); ASK: Rahul, who received it.
