# Fact-check a teammate's docs PR against source

The method of the recorded case, moidocs PR #120, and how to run it with this library. Facts are as of 2026-10-03. The method for checking any claim is `moi-devrel/claim-check` (`moi-devrel/claim-check/references/method.md`, `moi-devrel/claim-check/references/sources-of-truth.md`); this file adds what is specific to a docs PR. `$SKILLS`, "the operator" and `ASK:` are defined in `moi-devrel/SKILL.md`. Back to `../SKILL.md`.

## The recorded case
- **What**: moidocs #120, "docs: Access Policy and Storage Costing", by a teammate (Abhinav Agarwalla is named as the author in the previous operator's notes, which is secondhand; the squash commit on `main` is authored by Robert Špendl). Pages: storage cost, JSON-RPC, access policy, submit interaction, access control.
- **When**: 2026-08-21, while the PR was open. It merged on 2026-09-02 (commit `27d3713` on `main`). Whether the findings were applied before or after the merge is not recorded.
- **Against what**: go-moi v0.12.0 and js-moi-sdk v0.8.0, both on the previous operator's machine. The handlers named were `compute/ixstorage.go`, the SDK's `toRawOperation` and the `moi.StoragePricing` wire names.
- **How**: the previous operator built a "verified fact pack" of 52 facts already checked, had Haiku sub-agents (at his request, for cost) verify each claim in each changed file against source, then ran a refutation pass that tried to prove each finding wrong.
- **Result**: findings per file: storage cost 6, JSON-RPC 7, access policy 5, submit interaction 4, access control 3 (25 in all). The headline said "27 errors", the table said 8 breaking plus 18 minor (26), the numbered list had 25. The assistant flagged the mismatch and the counts were reconciled before anything went to the author.
- **Delivery**: a "simple md file", no artifact, nothing posted (the operator posts). The comment format was "Issue N: what the issue is, why it is an issue, where the issue is, suggested fix". The 8 breaking issues went first, the rest after review.
- **Not recorded**: where the report was saved, and whether the method was applied to the neighbouring PRs #123 and #126. Not recorded (the previous DevRel's notes); ASK: Rahul.

## The steps
GATE marks a step that needs the operator's yes.
| # | Step | How | Done when |
|---|---|---|---|
| 1 | Fix the scope | List the changed pages (`gh pr diff <N> --repo sarvalabs/<repo> --name-only`). Decide which release the pages document: the tag of go-moi and the version of js-moi-sdk. A PR written against v0.12.0 and merged after v0.13.0 is checked at the version it names, and the report also says what changed since | The report header names the repo, PR, base and head commits and each source ref |
| 2 | Get the head | GATE: `git fetch origin pull/<N>/head:pr-<N>` downloads and writes to the clone. Then `git switch pr-<N>` | The pages are on disk |
| 3 | Start the ledger | `mkdir -p claim-check-<slug> && printf '*\n' > claim-check-<slug>/.gitignore`, then `python3 "$SKILLS/moi-devrel/claim-check/scripts/extract-claims.py" --all <pages> > claim-check-<slug>/claims-candidates.csv && cp -n claim-check-<slug>/claims-candidates.csv claim-check-<slug>/ledger.csv`. Docs pages are mostly tables, parameter lists and code, so read the `--all` rows | One row per checkable claim |
| 4 | Pick the authority | Tagged source first, release note second, other docs last. The docs are the weakest source: its operation-code numbers were swapped against the node source at v0.12.0 (August 2026). Public sources: the js-moi-sdk package at its tag, the explorer, a live read. Private source (go-moi, go-pisa, cocolang) needs read access. ASK: Rahul who grants it. Without it, a claim about node behaviour stays `unverified` | Each row has a named source or an ASK |
| 5 | Verify | Read the source at the tag, not the tip: `git -C <clone> show <tag>:<path>` and `git -C <clone> grep -n "<name>" <tag> -- "<glob>"`. For wire names and fields, a read-only call to devnet (`moi-devrel/claim-check/references/live-reads.md`). Never submit an interaction | Each row has evidence |
| 6 | Refute | For every row you marked correct, try to prove it wrong by another route (the SDK instead of the node, another version). For every finding, ask "is there any way it could be correct": a different version, a different network, a documented default | Each finding survived or was dropped, with the reason in `note` |
| 7 | Tabulate | Fill `templates/fact-check-report.md` and save it as `claim-check-<slug>/fact-check-report.md`: that folder ignores itself (step 3), and the report may name private source and people, so it never goes into a public repo. Claim, result, evidence with file and line, severity, per file | A table per file |
| 8 | Reconcile | Count breaking, minor and verified in the headline, the table and the numbered list. They must be equal | One number, three places |
| 9 | Explain | For a finding that looks like a typo (a "ticker" where the code says "tick") write two lines without paragraphs: before and after, in plain words | The operator can say why it matters |
| 10 | Walk through | Present the findings one at a time, breaking first. For each, the operator may ask whether it could be correct; answer from the evidence | Every finding has an answer |
| 11 | Let the operator see it | Run the PR branch locally so the operator can open the page and judge: `npm run start` in the repo (GATE for `npm install` if not yet installed) | The operator has seen the pages |
| 12 | Draft the comments | `templates/review-comments.md`. The first batch holds the breaking items. Nothing is posted | A local file |
| 13 | Hand back | The report path, the counts, what stayed `unverified`, and "Ready to post: yes or no" | The operator has read it |

## Rules that came out of the case
- Sub-agents only when the operator asks, in that message, with the count and model first (house rule 7, `moi-devrel/claim-check/references/independent-check.md`). The default is the inline refuter pass of step 6.
- A count in a report is a claim. Recount after every edit.
- A finding without evidence is a question. Put it in the "could not verify" list with who can settle it.
- Check pages against the version they name. State the build you read.
- Private source informs the finding and never appears in page text. In a comment on a public repo, cite only public artefacts.
- Do not post. The report and the draft are local files.

## Pages worth re-checking now
The pages of #120 are on `main` of moidocs: the access policy and storage cost tutorials and concept pages, `submit-ixn.md`, `json-rpc.md` and `access-control.md`. #126 added `net.NetworkID` to the JSON-RPC page on 2026-10-01. Nobody has recorded a re-check against v0.13.0. A good first supervised task is to check the `net.NetworkID` section: on 2026-10-03 the page documents the method with network IDs 111, 112 and 113, and the live devnet answered error -32601, "the method net.NetworkID does not exist/is not available" (`moi-devrel/references/devnet.md` reports the same on 2026-10-02). The source may know it while the running build does not. ASK: Gokul which is right.

## Not yet known
- The report of 2026-08-21 and whether the findings reached the author. Not recorded (the previous DevRel's notes); ASK: Rahul.
- Who adjudicates when source and page disagree and the protocol team has not answered. Gokul is the protocol contact (inferred). ASK: Rahul.
