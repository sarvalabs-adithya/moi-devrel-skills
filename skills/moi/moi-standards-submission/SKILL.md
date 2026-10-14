---
name: moi-standards-submission
description: "Make MOI work under outside standards by filing pull requests upstream to x402 (a standard for paying for web requests with a blockchain) and to CASA, the Chain Agnostic Standards Alliance, whose CAIP-2 registry would list `moi:` as a chain name. Use for \"make MOI x402 compatible\", \"x402\", \"CAIP-2\", \"CASA namespace\", \"moi namespace PR\", \"scheme spec\", \"mechanism package\", \"@x402/moi\", \"upstream PR\", \"the review package for Rahul\", \"the CAIP-2 reference for MOI\", \"moi:devnet versus moi:112 versus moi:14 as the CAIP-2 name\", or \"AI disclosure in the PR\". Covers upstream research, drafting the three documents, the wording and verification passes, the internal review gate and the filing order. Nothing was filed upstream as of 2026-10-13. Commit and pull request mechanics are moi-devrel/ship, claim checks moi-devrel/claim-check, teaching x402 or CAIP-2 moi-devrel/explain, and the announcement post moi-blog."
---

# MOI standards submission

## What this covers
Making `moi:` a legal CAIP-2 name and MOI payable under x402 takes three upstream pull requests, filed in this order: the namespace to `ChainAgnostic/namespaces`, the `exact` scheme specification and then the TypeScript package `@x402/moi`, both to `x402-foundation/x402`. The documents are drafted and were verified against source up to 2026-09-10, and nothing was filed upstream as of 2026-10-13 (the package README; the upstream counts below were last read 2026-10-03): the reviewer has not cleared the package on record, the CAIP-2 reference format (`moi:devnet`, `moi:112` or `moi:14`) is undecided, and the AI-assistance disclosure conflicts with the house rule on attribution. The operator files; Claude researches, drafts, lints, verifies and explains. The terms (x402, facilitator, CAIP-2, CASA, `upfront`) are explained at the top of `references/umbrella.md` and in `moi-devrel/references/glossary.md`; if the operator cannot yet say them back, use `moi-devrel/explain` before step 1. For any other standard nothing is researched: use `references/umbrella.md` as the method (read the upstream rules first, find a merged precedent, list the open decisions) and ASK: Rahul which standard and who files.
Not covered: a plain question about devnet's network ID, which is a read of the node (`moi-devrel/references/devnet.md`, "Network IDs"); claim checking (`moi-devrel/claim-check`); the general mechanics of a commit, a push and a pull request (`moi-devrel/ship`, in `moi-devrel/ship/GUIDE.md` and `moi-devrel/ship/references/pull-request.md`), while the fork, identity, signing and push steps that these two upstreams add are in `references/umbrella.md`, "Filing mechanics"; messages to Rahul or Gokul (`moi-devrel/templates/messages.md`, checked with `moi-devrel/scripts/check-message.py`); the announcement post (`moi-blog`); explaining x402 or CAIP-2 until the operator can defend it (`moi-devrel/explain`); a structured devnet test pass (`moi-devrel/test-round`).

## Before you start
`SKILLS`, "the operator", "the previous operator" and `ASK: <person>` are defined in `moi-devrel/SKILL.md`. Steps 1 to 8 run in `$HOME/x402-review`, a folder that is not a repository; steps 9 and 11 to 13 run in the clone of the fork the step names; steps 10, 14 and 15 are done on GitHub. Quote `"$SKILLS"` every time.
- [ ] The package: `others/standards/x402-review-package/` in the handover repo you already cloned (README.md first; AUDIT-2026-09-10.md, ESCROW-RESEARCH-2026-09-10.md, FUTURE.md, BLOG-x402-on-moi.md, and docs/PR-1-CASA-namespace, PR-1-chain-id-edits, PR-2-x402-scheme-spec and PR-3-x402-moi-package as .md, .docx and .pdf). It is the newest text, written 13 October 2026. Not in the handover repo (the previous DevRel's local x402-compat folder): x402.md, FINDINGS.md, UPSTREAM.md, FIX-PLAN.md, DECISIONS.md, STATUS.md, caip2-submission/, escrow-poc/, the PR folders with their inner trees and the prototype moi-x402/. ASK: Rahul whether a copy exists. Without one, only an older generation 1 can be had, from the public branch (`umbrella.md`); a clone is a download (GATE: state its name, source and size first).
- [ ] The reviewer and the form of "approved": Rahul. Ask: "How do you want to clear the package in writing, and does Gokul review code separately?"
- [ ] The human who answers upstream (the CASA author field), the GitHub account that files, and a signing key: ASK: Rahul.
- [ ] Read access to go-moi, go-pisa and cocolang for protocol claims (private as of 2026-10-02). ASK: Rahul who grants it. Without it, a claim beyond the wire stays unverified.
- [ ] A devnet wallet used only for devnet, made in the MOI Wallet extension by the operator, and funded from the public Voyage faucet page by the operator (the amount quoted differs by source: check live). ASK: Gokul if the faucet is empty.
- [ ] A working folder that cannot be committed: `mkdir -p "$HOME/x402-review" && printf '*\n' > "$HOME/x402-review/.gitignore"`. Keep it outside every repository.

## The run
Nothing marked GATE happens without the operator's yes that names it.
| # | Step | What to do, and where | Done when |
|---|---|---|---|
| 1 | Place the package | Copy `others/standards/x402-review-package/` from your clone of the handover repo into `$HOME/x402-review/handover/` (a copy inside a clone you already have is not a download). The upstream files exist there only as listings inside `docs/PR-1-CASA-namespace.md`, `docs/PR-2-x402-scheme-spec.md` and `docs/PR-3-x402-moi-package.md`: rebuild the folders `PR-1-CASA-namespaces-moi/`, `PR-2-x402-scheme-spec/` and `PR-3-x402-mechanism-typescript/` from those listings (Claude splits them out, the operator checks one file against its document; inferred step). The background files (x402.md, FINDINGS.md, UPSTREAM.md, caip2-submission/) are not in the handover repo; ASK: Rahul | `ls "$HOME/x402-review"` shows `handover/` and the three PR folders |
| 2 | Read upstream first-hand | From any folder: the census commands and the rule files in `references/umbrella.md`. Print them, do not save them. Date every note | A dated list of what differs from this skill |
| 3 | List the open decisions | `references/open-decisions.md`, `templates/decisions-log.md`. State conflicts A (CAIP-2 reference format) and B (AI disclosure); resolve neither. Draft the questions, the operator sends | Each decision has an owner and a state |
| 4 | Draft or update the documents | `references/casa-namespace.md`, `references/x402-scheme-spec.md`, `references/x402-mechanism.md`. Copy the structure of a merged precedent, section by section | Each file sits at its mirrored upstream path |
| 5 | Wording pass | In `$HOME/x402-review`, on the folders rebuilt in step 1 (each `PR-DESCRIPTION.md` is the "PR description" section of its `docs/` file saved on its own): `python3 "$SKILLS/moi-standards-submission/scripts/spec-lint.py" PR-1-CASA-namespaces-moi PR-2-x402-scheme-spec PR-3-x402-mechanism-typescript/PR-DESCRIPTION.md`, then `python3 "$SKILLS/moi-standards-submission/scripts/spec-lint.py" --kind source --source PR-3-x402-mechanism-typescript/x402` (add `--stale '<old string>'` after a decision), then `find PR-1-CASA-namespaces-moi PR-2-x402-scheme-spec -name '*.md' -exec bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" {} +`. Rules: `references/wording.md` | 0 errors in each; every warning read |
| 6 | Verify | Seven rungs in `references/verification.md`; an install or `npm pack` is a GATE. Ledger and verdicts through `moi-devrel/claim-check`, in `$HOME/x402-review/ledger/` (the ignore rule above covers it). Recount every number | No unsupported claim; unrun items named |
| 7 | Build the index | `cp "$SKILLS/moi-standards-submission/templates/review-package-index.md" "$HOME/x402-review/START-HERE.md"` and fill it. PR texts from `templates/pr-description-x402.md` and `templates/pr-description-casa.md`. Generate the reviewer copies from the markdown (`references/review-gate.md` step 4) | Every count carries today's date |
| 8 | GATE: internal review | `references/review-gate.md`. Upload to Drive (a yes), the operator messages the reviewer | The clearance is pasted in the index with its date |
| 9 | GATE: CASA pull request | In a fork of `ChainAgnostic/namespaces`: `references/casa-namespace.md`, "Filing", and `references/umbrella.md`, "Filing mechanics" | PR open; `discussions-to` set to a URL someone watches |
| 10 | GATE: proposal issue | In `x402-foundation/x402` (issues on, Discussions off as of 2026-10-03): the outline in `references/x402-scheme-spec.md`. Ask Rahul first (`open-decisions.md` 13) | Issue open, or Rahul says it is not wanted |
| 11 | GATE: spec pull request | In a fork of `x402-foundation/x402`, after step 9 and step 10. It must not merge before CASA | PR open with the upstream template headings |
| 12 | GATE: round trip | The operator runs it in their own terminal, never Claude: `references/x402-mechanism.md`, "The round trip". It spends devnet funds | Result written down in `$HOME/x402-review/` (it names accounts, so it stays out of git), or the PR box left unticked |
| 13 | GATE: package pull request | After the spec merges; checklist in `references/x402-mechanism.md` | PR open; payment and signature code personally reviewed |
| 14 | GATE: after filing | Answer at `discussions-to` and in each PR thread the same day. Each reply and each push is a GATE. Put the changes a reviewer asks for in one push | No upstream question older than a day |
| 15 | GATE: after merge | Get MOI listed in the x402 docs (how: `references/umbrella.md`, "Listing and publishing"); publish `@x402/moi` (who runs the workflow is unknown); announce through `moi-blog` | Merged, listed, published |

## Which file to read
| Doing | Read |
|---|---|
| The path from "can MOI support this" to a merged PR, where each file is, upstream rules, recount commands, fork and signing | `references/umbrella.md` |
| The namespace files, the format candidates, Resolution Mechanics | `references/casa-namespace.md` |
| The scheme specification and the proposal issue | `references/x402-scheme-spec.md` |
| The TypeScript package, the round trip and what is outside it | `references/x402-mechanism.md` |
| The internal review package and what "approved" means | `references/review-gate.md` |
| What "verified" meant and the passes that were run | `references/verification.md` |
| Public wording and the lint | `references/wording.md`, `scripts/spec-lint.py` |
| Every open decision and who decides | `references/open-decisions.md` |
| Rules with their incidents | `references/traps.md` |
| Skeletons: PR text, decisions log, package index | `templates/` |
| The form of finished pieces (cleaned excerpts) | `examples/README.md` |
| Commit, push and pull request steps in general; the upstream disclosure rule against the no-footer rule | `moi-devrel/ship/GUIDE.md`, `moi-devrel/ship/references/pull-request.md` (section 6 returns here), then `references/umbrella.md`, "Filing mechanics" |
| A message to the reviewer or to Gokul | `moi-devrel/templates/messages.md` (drafts 9 to 11 for a reviewer, 6 to 8 for Gokul), `moi-devrel/scripts/check-message.py` |
| Testing a change to this skill | `evals/evals.md` |

## Facts that fail silently
| Rule | The incident |
|---|---|
| Recount before you quote a number, and date it | CASA namespaces were written as 55, then 50, then 49 (a listing includes six non-namespace folders). `moi:devnet` was in 6 files on 2026-09-10 and 15 on 2026-10-03 |
| Read the wire, not the source tip, before writing "live" | `fee_payer` was in the tip on 2026-09-07 while devnet answered `payer` on 2026-09-10. The network ID method is absent from devnet on 2026-10-03 and still on 14 October 2026: `net.NetworkID` returns -32601 while `net.Version` answers 0.13.0 |
| Never write a Resolution Mechanics example for a method that does not exist | A `net.Network` example was removed on 2026-09-10 |
| After a decision, search every copy for the old string | The 2026-09-14 correction did not reach the reviewer documents, the background notes or the spec appendix |
| A property the code does not enforce is not a property | The resource binding was signed and never checked (2026-09-09). `keyId` was called pinned while only documented (2026-09-10) |
| "Verified" never covers what has not run | The live round trip has never run |
| Public text carries no reviewer name, internal checkbox, placeholder, private repo, local path or untrue "filed" | All three PR descriptions carry "Internal review (<reviewer's name>) complete"; the CASA number is `TODO` in `caip2.md` and in the spec PR text; a code comment says the namespace was "filed" | <!-- slop-lint: ignore -->
| The linter reads Markdown only unless told otherwise | The package's code and config held "Voyage devnet" on 11 lines in 7 files on 2026-10-03; use `--source` | <!-- slop-lint: ignore -->
| The public branch already carries the first generation | A push to `moi-foundation/MOI-Webinars` publishes; the newest files cite private source |
| Name a human who answers upstream | The one real CASA failure was an author silent for 587 days |
More in `references/traps.md`.

## Gates
Nothing below happens without the operator's explicit yes in this conversation:
- Push, open or update a pull request, merge, comment or reply upstream. A push to `moi-foundation/MOI-Webinars` publishes.
- Fork a repository under the work account.
- Upload or share the review package in Drive; send any message to Rahul, Gokul or anyone (Claude drafts, the operator sends).
- Open a proposal issue or post in the x402 Slack.
- Spend devnet funds, submit an interaction, deploy or create an asset: the round trip is one.
- Change git configuration for signing, switch the `gh` account or the git identity, set a repository secret or variable.
- Download a file or install anything: `npm pack`, `npm install`, `pnpm install`, `gem install`, a clone, a fetch, the package from anyone. State name, source and size.
- Run the publish workflow or anything on a VM.
- Spawn sub-agents. The September sweeps used them only under a waiver; state the count first.
- Add an AI co-author line or "generated with" footer. How to word the upstream disclosure is open (`references/open-decisions.md` B).
- Recovery phrases: Claude never handles one, including a throwaway one. Wallet steps are the operator's.

## Keys and access
Names only; the single list is `moi-devrel/references/keys-and-access.md`. Needed: the work GitHub identity and forks; a commit-signing key (recorded "not configured", status TBD); read access to the private repos; a devnet wallet; Google Drive access for the review folder; the upstream `npm` environment (owner unknown). The env variable names `CLIENT_MOI_MNEMONIC`, `SERVER_MOI_ADDRESS`, `MOI_RPC_URL` and `MOI_ASSET_ID` (values never recorded), and the `npm` environment, have no row for the standards work in `moi-devrel/references/keys-and-access.md` (it lists `MOI_RPC_URL` only for the Launchpad): ASK: Rahul to add them. Never open an `.env` file or paste a key into a document.

## Hand-back
```
Produced: <files, with paths in $HOME/x402-review>
Gate: <reviewer clearance recorded with date, or "not yet">
Open decisions: <numbered from references/open-decisions.md, each with its owner>
Not verified or simulated: <unrun items, private source not read, wire not re-read>
Ready: yes or no, because <one reason>
Next steps: <one to three>
```
Ready is yes for filing a PR only when the clearance is on record, the linters report 0 errors, the counts are recounted today and the decision that PR depends on is settled. A status lists work that was done; a to-do is labelled one.
