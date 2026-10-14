# Examples: cleaned excerpts that show the form

Not the whole package. Each file is a short excerpt of a real draft from the review package (`x402-compat/review-package/` on the previous DevRel's machine, as of 2026-10-03; the newest documents are in `others/standards/x402-review-package/`, and the folders named in the Source column are not in the handover repo; ASK: Rahul), taken to show a form worth copying. Lint them with `--kind other` if you lint them at all; they are excerpts, so the headings the lint requires are not there on purpose.

| File | What it shows | Source | Why it is worth copying |
|---|---|---|---|
| `caip2-test-cases-excerpt.md` | The Test Cases section of the CAIP-2 profile | `PR-1-CASA-namespaces-moi/namespaces/moi/caip2.md` | Every case carries its reason. The section a CASA reviewer reads first |
| `spec-rules-excerpt.md` | Rules 3 and 8 of the scheme specification | `PR-2-x402-scheme-spec/x402/specs/schemes/exact/scheme_exact_moi.md` | Each rule says what MUST hold, why, and what a later version MAY change. Testable wording |
| `decisions-excerpt.md` | Two blocks of a decisions log | `PR-1-CASA-namespaces-moi/DECISIONS.md` | Who decides, the options, a table of exactly what changes, the knock-on outside the PR |
| `audit-summary-excerpt.md` | The summary table of the end-to-end audit | `AUDIT-2026-09-10.md` | One line per PR: state, and what blocks filing. Its PR 3 row says 28 of 28 tests, while the same audit says 36 of 36 further down: a count that drifted inside one file (`references/traps.md` 12) |
| `pr-description-before-after.md` | The drafted PR body against the form to post | `PR-2-x402-scheme-spec/PR-DESCRIPTION.md` | Shows the internal lines and placeholders that must not be posted |

`decisions-excerpt.md` keeps the package's own labels: it calls the two reference formats Option A (names) and Option B (numeric network ID). The skill's references call the same two formats 1 and 2, because A and B there name the two conflicts.

## What was changed when the excerpts were made
- Em dashes were replaced with colons or commas.
- "Voyage devnet" became "devnet". <!-- slop-lint: ignore -->
- Reviewer and author names were replaced by their roles ("the reviewer", "the author named in the front matter").
- A placeholder PR number was removed from one sentence.
- Nothing else was edited: counts and dates are as the source had them, including the stale 28 in the audit summary.
- Nothing in these files is a key, a recovery phrase, a personal address, an account id or a photograph. The spec excerpt contains no identifier from the chain.

## What was left out on purpose
- The `STATUS.md` table "Claims checked against source". Its second column names private source symbols and a commit of a private repository, so it stays out of any public repository. Keep that table in the internal copy. The form is two columns: the claim in the spec or code, and where it holds (public source first, private source named only in the internal copy, a live read with its UTC time).
- The reviewer-facing documents (`docs/`), the blog draft, and the escrow research. They are long, and they name private source or reviewers.

## Rule on git
A review package names internal people and private source. It stays out of a public repository. The ignore rule for a working folder is in `../SKILL.md` ("Before you start"): a `.gitignore` containing `*` inside the folder.
