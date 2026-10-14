# Internal review gate: the review package

Facts are as of 2026-10-03 unless dated. `ASK: <person>` is defined in `moi-devrel/SKILL.md`. Back to `../SKILL.md`.

## The rule
Nothing goes to an external repository until the whole content package has been reviewed internally. It was set on the 9 September 2026 call: "That is the process now, not a suggestion" (`UPSTREAM.md`, "Internal gate"). The package goes into Google Drive, the reviewer reads it there, and the pull requests go out only after the review clears. The gate applies before every filing and again whenever the package changes materially (the numeric-ID edit set of 14 Sep is the example).
Who: the author prepares. Rahul reviews the package as a whole (title not recorded; ASK: Rahul). Gokul reviews every code change in PR 3, and "the package leaves the org only after Rahul's" review (`docs/PR-3-x402-moi-package.md`, page 1).

## What "approved" means
The evidence says: the review "clears" and then the PRs go out; code goes through Gokul; the package leaves after Rahul. It does not record the form of the clearance, what Rahul said on 9 to 15 Sep, or which Drive generation he read. Until Rahul says otherwise, use this working definition (a proposal, not a recorded rule):
1. Approved means a written message from Rahul that names the package date, the three PRs, and any decision he settled. The operator pastes it into the index (`templates/review-package-index.md`, "Clearance").
2. It covers the version he read. A later change to a rule, a reference string or a claim reopens the gate for that change; give him a delta, not a rewrite.
3. It is not Gokul's code review, and it is not the verification record. Each is a separate line in the index.
ASK: Rahul to confirm this form and to say what else he approves formally.

## What goes in the package
| Part | What it is | Source of the form |
|---|---|---|
| Index ("START HERE") | One paragraph defining the package, the process rule, an order table (order, document, target repo, state), the dependency chain 1 to 2 to 3 ("enforced rather than preferred"), a dated live-state check, and a paragraph naming what verification covered | 9 Sep Word set |
| One folder per PR, in filing order | Inner tree mirrors the target repo path for path: `PR-2.../x402/specs/schemes/exact/scheme_exact_moi.md` lands at `specs/schemes/exact/scheme_exact_moi.md`. Each folder holds the PR description as it will be posted | `review-package/README.md` |
| One review document per PR (10 Sep) | Page 1: target repo, PR title, why it exists, a high-level requirements table, status bullets, an index. Then "1. PR description (as it will be posted)". Then "2. File: <path>" with a bold **Context.** note under every section, then the exact file text. Then the open decisions (PR 1) or the verification record (PR 3) | `docs/` |
| Background documents | The plan with Needs and Done when per step; verified findings, each ending "Checked: <how>"; per-PR requirements and an "applies to every PR" list | `x402.md`, `FINDINGS.md`, `UPSTREAM.md` |
| Decisions | One place, plus an instruction inline where a decision is needed. No placeholder: where a section cannot be answered, say in one or two lines what it requires (2026-09-10) | `DECISIONS.md` |
| Live-state check | What was probed and when: RPC methods, upstream counts, versions | `umbrella.md` census |
Every document after page 1 is the exact content that will be filed, so the reviewer reads the real artefact. Write for a reader who has never seen MOI.

## The run
| # | Step | Where | Done when |
|---|---|---|---|
| 1 | Recount and refresh the live-state check | census commands in `umbrella.md`; the probe in `casa-namespace.md` | Every number in the index has today's date |
| 2 | Lint every file in the package | From `$HOME/x402-review`: `python3 "$SKILLS/moi-standards-submission/scripts/spec-lint.py" --source .` | 0 errors; each warning read; each `--stale` term of a settled decision gone. The background and `docs/` files are internal, so their private-source and reviewer-name hits are expected; the files that go upstream must be clean |
| 3 | Mirror check | From `$HOME/x402-review`: `find PR-1-CASA-namespaces-moi/namespaces PR-2-x402-scheme-spec/x402 PR-3-x402-mechanism-typescript/x402 -type f -not -path '*/node_modules/*'`, set beside the upstream tree (the first folder of each is the repo name, dropped upstream) | Each path lands where upstream expects it (CASA at `moi/`); files that already exist upstream are described as edits, not copied |
| 4 | Generate the reviewer copy from the markdown, never the reverse | `pandoc` to `.docx` (commit `29d83f1`: "generated with pandoc from the markdown sources"; the options are not recorded) | The reviewer copy is newer than every source file |
| 5 | Open the rendered copy | A table header row and a code block | No literal `**` in a header cell (the 10 Sep conversion test read as literal asterisks; that may have been the read tool) |
| 6 | GATE: upload to Drive | One folder, only the review documents: Calibri, clear hierarchy, no bookmarks, no PDF, no markdown (instruction of 2026-09-10) | The operator said yes to the file, the folder and who can open it |
| 7 | GATE: message the reviewer | The operator sends. Plain text, short, completed work first, one request. Draft from `moi-devrel/templates/messages.md` (draft 9, "Ask for a review") and check it with `python3 "$SKILLS/moi-devrel/scripts/check-message.py" --to reviewer <draft>` | The operator read the final text once |
| 8 | Record the clearance | The index | The message is pasted with its date |
A change after clearance: write a delta document (copy-paste replacements per section, a "Comments to update" list, a "To confirm with" list), as `docs/PR-1-chain-id-edits.md` does. The Drive connector could not edit a Google Doc directly on 14 Sep (inferred from the fallback to "tell me what to find and replace"), so the reviewer or the operator applies it. <!-- slop-lint: ignore -->
While the reviewer sends tweaks, keep them on one working set and regenerate once. Open one pull request at the end, not one per tweak (house practice since 2026-09-15; `moi-devrel/ship` owns the mechanics).

## Keep the package out of a public repository
The package names internal people and, in its newest files, private source. `moi-foundation/MOI-Webinars` is public, and a push to it publishes. Keep the working package in a folder outside any repository, or make the folder ignore itself:
`mkdir -p x402-review && printf '*\n' > x402-review/.gitignore`
An ignore rule does not hide a file already tracked. As of 2026-10-03 the first generation (including `Internal review (<reviewer's name>) complete` lines) is tracked on a pushed branch. Removing it is a push and a decision for the operator. ASK: Rahul.

## Traps
1. The Drive copy goes stale. The 9 Sep index said "50 namespaces", "js-moi-sdk 0.9.0-rc1", "typechecks against 2.23.0 - retest" and PR 3 "~1/3 built". The package then moved to 49, rc2, 2.25.0 and a finished PR 3. Regenerate and recount before every share.
2. Four similarly named Drive folders exist: `x402 review package (MOI)` (9 Sep), `x402 PR review docs (10 Sep 2026)`, an empty `x402 PR review docs`, and `x402` (10 Sep, with three `.docx` and a Google Doc of 14 Sep for PR 1). The one named `x402` was last viewed 14 Sep and is taken as current (inferred). No link is recorded in this library: ASK: Rahul.
3. In the handover package the `docs/*.md` were corrected (13 Oct) but the `.docx` and `.pdf` exports of 6 Oct were not regenerated and still say "account-centric" (checked in the PR 1 `.docx`). The old `review-package/README.md` on the public branch still says 28 and 13 unit tests. <!-- slop-lint: ignore -->
4. A review document for PR 3 was split "part 1 of 4" and only part 1 was uploaded; the later `.docx` replaced it.
5. Drive documents are snapshots. The on-disk package is newer, except possibly the 14 Sep Google Doc for PR 1 (`umbrella.md`, Drive row): read both and say which is current.
6. STATUS and the escrow note cite private source by path or line range. They are internal-only and stay out of the upstream tree and out of public git.

## Not yet known
- Whether Rahul read the package, which generation, and what he answered. ASK: Rahul.
- The Drive folder link and who has access: not recorded (the previous DevRel's notes); ASK: Rahul.
- The exact pandoc options and reference document used for the Word copies: not recorded (the previous DevRel's notes); ASK: Rahul. The `.docx` exports are in the handover package.
