# After the round: failures into fixes and issues (drafts only)

Facts are as of 2026-10-03. `ASK:` is defined in `moi-devrel/SKILL.md`. Claude drafts and the operator sends, files, pushes and merges. Nothing on this page is done without a yes (`../GUIDE.md`, Gates). Drafts live in `test-round-<slug>/drafts/`. Back to `../GUIDE.md`.

## 1. Sort each fail
Do this before writing anything. Write the class in the `note` cell.

| Class | Sign | What to do |
|---|---|---|
| Product defect | Reproduces, and the plan's `must` was right | Finding, issue draft, fix, retest (sections 2 to 4) |
| Test defect | The plan was wrong or out of date | Correct the plan. `fix` says "plan corrected". The Launchpad plan expected "I don't keep price history" in one section and a real dated price in another |
| Environment | A reset, an empty wallet, a stale document, a drained shared quota, a stuck interaction | Fix the environment and rerun. No issue. "Only 3 messages" in July 2026 was a shared pool drained by earlier testing |
| Not ours | The wallet, the chain, a third party | Say so in the log and draft a message to the owner (section 5). "Another request is already in progress" on 2026-08-01 was a stale popup in the wallet, cleared by answering or toggling the extension. The registry call `GetAllAgentIds` reverting was recorded as the protocol team's to fix |
| Known and accepted | Someone with authority chose to live with it | `fix` holds `accepted: <who>, <date>`. The July 2026 plan listed two accepted gaps: a new wallet that cannot register until funded (closed by wallet activation on 2026-08-01) and mobile being desktop-only. Who accepts now: ASK: Rahul |

## 2. Write the finding
Follow the Launchpad's test report. Per failure: a three-column table of input, output and verdict with the output verbatim; a Diagnosis paragraph that separates what was observed from what is suspected; and a Changed paragraph with the commit once there is one. The log rows are the source: copy `input`, `output`, `evidence` and the hashes. Add the scoreboard at the top: cases run, passes on the real devnet, passes on something simulated, fails, blocked.

If a defect class repeats, say so and add cases for the siblings. In July 2026 the same defect (the message ignored) appeared in four templates, and the report called it a pattern and not a bug.

## 3. Draft the issue
One file per failure: `drafts/issue-<case_id>.md`.
```
Title: <what is wrong, in the product's words>
Seen on: <product, live host, version or commit, node version, UTC date and time>
Steps: <the case's input, repeatable by someone else>
Expected: <the plan's must>
Actual: <the exact output>
Evidence: <case id, full hash, balances, the receipt status>
Suspected cause: <observed or hypothesis, labelled as one>
Found by: test round <slug>, case <id>
```
Rules:
- The repo's owner triages. Which repo takes Launchpad issues and who reads them: ASK: Rahul.
- Public repos get public text. `sarvalabs/moi-mcp` is public: no private source paths, no reviewer names, no internal plans. Say what the product does, not where the private code is.
- No keys, no addresses of personal wallets, no recovery phrase, no pasted chats with real names.
- **A case that exposes what looks like a security weakness:** stop that case. Do not write the detail into the log, the issue draft or a pull request. Tell the operator in the conversation and ASK: Rahul who receives it.
- Filing is a gate. `gh issue create` notifies people. Do not call `gh` for pull requests or issues unless the operator allows it.

## 4. Fix and retest
1. Hand the change to `moi-devrel/ship` for the commit, the pull request and the preview. A fix lands with a test that would have caught it (the Launchpad and MCP rule). Product mechanics (deploy, migrations, secrets, reset response) belong to `moi-launchpad-ops`, `moi-mcp-ops` and `moi-launchpad-ops/explorer`.
2. Look for the same shape elsewhere. The double charge of 2026-08-02 came from an idempotency check placed after an irreversible step. The lesson recorded was to re-read the other payment guards with that lens: the protection has to sit before the wallet opens.
3. Verify on the real chain before the pull request is opened, and say in it what was and was not verified.
4. Shipping is a gate. A merge to the Launchpad's `master` deploys it. Merging to `sarvalabs/moi-mcp` deploys nothing: production changes through a sync pull request and a manual workflow (`mcp-pass.md`). A database migration on the Launchpad is run by hand in the SQL editor and is a gate.
5. Retest on the live host, after the deploy, as a new row with `retest_of` and the id suffix `-r1`. Recreate or re-download the thing under test first when the plan says to. Change one thing per retest.
6. Run `python3 "$SKILLS/moi-devrel/test-round/scripts/test-log-check.py" "test-round-$SLUG/test-log.csv"`. A fail with a fix and no passing retest shows in its WARN list.

## 5. Close the loop (all drafts)
- **Messages.** Draft from `moi-devrel/templates/messages.md` (the shapes are in `moi-devrel/references/house-style.md`, section 4); the operator sends. To DevOps: short, human and specific; the problem, then the solution, then exactly what they do; no boilerplate labels such as "Owner:"; never a request for a secret value, and never paste one back. To the protocol team about a chain-side finding: a plain question with context, carrying the case id, the full hash, the node version and the UTC time. To Rahul: the weekly update lists completed work only, and to-dos are labelled as to-dos.
- **The plan.** Propose edits for every stale case you found (a header that names an old host, a count that changed, a retired feature). Do not edit a private repo's document without a yes.
- **Public text.** If a post, deck or script quotes the round, run `moi-devrel/claim-check` and cite the case id, the full hash, the node version and the date in the ledger `source` cell. Never cite a private file in the public text.
- **The durable record.** The Launchpad pasted payment hashes into `docs/QA-LEDGER.md` in its private repo. Do that only after a yes, with names removed. ASK: Rahul where the record belongs.
- **The sign-off table.** Fill it in the plan: area, pass, fail or blocked, with case ids. Name who read it.

## 6. The write-up in four lines
```
Round: <product>, <target>, <version>, node <net.Version>, <date>
Result: <N> passes on the real devnet or live product, <M> on something simulated, <F> fails, <B> blocked
Open: <each fail or blocked case, with its fix, draft path or owner>
Not covered: <what the plan left out>
```
This is also the first part of the hand-back in `../GUIDE.md`.

## Not yet known
- Which tracker takes Launchpad and MCP defects, and who triages. ASK: Rahul.
- Whether a support channel is monitored. The dashboard links to Discord for users who need a person. ASK: Rahul.
