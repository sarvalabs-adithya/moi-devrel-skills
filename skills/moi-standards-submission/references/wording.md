# Wording: the public style rules for a standards document

Facts are as of 2026-10-03 unless dated. `ASK: <person>` is defined in `moi-devrel/SKILL.md`. The general house style is `moi-devrel/references/house-style.md` and the term table is `moi-devrel/references/terminology.md`; this file adds what a standards document needs. A line that quotes a wrong form on purpose ends with the ignore marker both linters read. Back to `../SKILL.md`. The package files this file cites by name (`BLOG-x402-on-moi.md`) are untracked and exist only on the previous operator's machine; ASK: Adithya for a copy (`umbrella.md`, generation 4).

## Who does what
Claude edits. The operator reads and strikes lines. For each automated pass, report the findings first and let the operator pick which to apply (the pattern on the September release post, 2026-09-11: "don't make any changes, just identify the changes", then "do all but the first"). Re-read the opening paragraph and the governance paragraph after every pass: on that post, later passes kept reintroducing phrasing the operator had rejected (2026-09-11).

## Rules, with the wrong form and the right form
| # | Rule | Wrong | Right | Date, lint rule |
|---|---|---|---|---|
| 1 | Participant-centric. The account is the vehicle that represents a participant's state | "MOI is an account-centric protocol", "each account has its own chain", "a per-account sequence of tesseracts" <!-- slop-lint: ignore --> | The MDAG block in `moi-devrel/references/terminology.md`: a Multi-Link Composite DAG of tesseracts; a tesseract is the joint state record of every participant that moved together and carries one back-link per participant; one participant's links give a logical, non-branching history that is a view of the DAG, not a separate chain. The clause "that account's" or "that participant's" is unconfirmed: ASK: Rahul | 2026-09-14. `account-centric`, `per-account-chain` |
| 2 | Governance, in one sentence | "Sarva Labs governs MOI", the Foundation left out | "Designed and developed by Sarva Labs, governed by MOI Foundation." Sarva Labs is one implementation partner: it builds the reference node and the SDKs. The Foundation makes protocol decisions. The model is Sui. No Foundation website exists, so moi.technology stands in. The call named governance "the most important aspect". The company is Sarva Labs, GitHub org `sarvalabs`, never "Serval" | 2026-09-14. `governance-inverted`, `serval-labs` | <!-- slop-lint: ignore -->
| 3 | Network ID for MOI's own identifier | "chain ID" for MOI's own <!-- slop-lint: ignore --> | "network ID". Keep "chain id" only for another chain's convention, such as `eip155`'s | 2026-09-14. `chain-id` (warn) |
| 4 | Do not overclaim | "MOI has no chain id", "no genesis block", and the unscoped "No RPC method or interaction field reads or emits a network ID" (the public docs list `net.NetworkID`) <!-- slop-lint: ignore --> | A dated statement of what was read: "On the devnet build read on 2026-10-03 (`net.Version` 0.13.0), `net.NetworkID` answered method not found; the public docs list it." Write it only with the date and build you read, or cut it. The SDK exports a numeric `Chain` enum: 111, 112, 113. ASK: Gokul. "No chain of blocks and no global height; one genesis tesseract seeds the founding accounts, is reachable only by naming one, and is re-created whenever a network is initialised" | 2026-09-09, 2026-09-14, 2026-10-03. `flat-negative` |
| 5 | Say devnet | "Voyage devnet" <!-- slop-lint: ignore --> | "devnet". Voyage is the explorer and tooling site | 2026-09-25. `voyage-devnet` |
| 6 | Only public artefacts | "go-moi is public", a go-moi path or line, a local path, a link to a private repo | js-moi-sdk, js-polo, the docs, the explorer, behaviour on the wire. Private clones are for checking, never for citing | 2026-09. `private-source`, `private-link`, `local-path` |
| 7 | No invented content | A curl example for a method that does not exist; an error-reason list; a `flow` key | In one or two lines, what the section requires. "A placeholder dressed as a specification" | 2026-09-10 (`5b2d089`). `to-be-completed`, `placeholder-*` |
| 8 | Frame `upfront` as a choice | "MOI can only do `upfront`" | "MOI can express all three flows; the first scheme settles in one interaction" | 2026-09-10 (`cd834b3`) |
| 9 | Benefits as before and after for a developer, specific to MOI | A story about another company | What a seller and a buyer write today and after, with the lines counted. The plan (`x402.md` section 4) has the table | 2026-08-27 |
| 10 | Plain-English context before jargon | Opens on CAIP-2 | "This is CASA, and they have a naming standard which x402 requires", then the section | 2026-08-31 |
| 11 | Delete a paragraph that keeps hedging | Rewriting it a fourth time | Delete it. "Which usually means the paragraph is the problem rather than the wording" (`ee4c1c4`) | 2026-09. `hedge` (warn) |
| 12 | Reserve, do not list as live | `moi:mainnet` in the well-known table as live | Marked reserved and "MUST NOT be treated as resolvable" until it launches, or leave it out (open: `open-decisions.md` 10) | 2026-09-09 (`269ab19`) |
| 13 | A live claim carries its source | "devnet is the only live public MOI network" with no date | "As of 2026-10-03, ..." with how it was read | `live-no-source` (warn) |
| 14 | Nothing internal in text that will be posted | "Internal review (<reviewer's name>) complete" ticked in a PR body; a reviewer's name; `#TODO` | Delete the internal line when the gate clears; fill the number or drop the line | `internal-checkbox`, `reviewer-name`, `placeholder-word` | <!-- slop-lint: ignore -->
| 15 | Concise, no filler | Verbose PR text, redundant tests, generic comments | Strip to what is useful. Upstream may close "cookie-cutter" AI-looking PRs without review | x402 `CONTRIBUTING.md`, 2026-10-03 |

## Rules that are still open
- AI-assistance wording: the upstream text asks for a disclosure and the house rule bans a co-author line and a "generated with" footer. The lint reports whether a sentence exists and never rules on it. `open-decisions.md` 8.
- Em dashes. Posts, scripts, social and status messages carry none, and the default for anything you author is none. Whether the ban covers specs and background documents is unsettled (`moi-devrel/references/terminology.md` Contested 7); the existing drafts use many. `spec-lint.py` treats an em dash as an error until Rahul rules. `open-decisions.md` 9.
- Governance detail: whether Sarva Labs "operates" the public networks. The 14 Sep draft flagged it to confirm and the README still says it. Use only the one-line governance sentence in public text until settled (`moi-devrel/references/terminology.md` Contested 3).

## CASA style (CONTRIBUTING, read 2026-10-03)
One sentence per line is preferred, not required. Define every external link as `[Name]: URL` at the end of References and use the alias in the text. Link CAIPs on chainagnostic.org, not the git repository. Link other sections as markdown heading links. The drafts wrap sentences at about 100 columns and use inline links.

## The pass, in order
1. Write the plain-English paragraph first. Then the section.
2. `python3 "$SKILLS/moi-standards-submission/scripts/spec-lint.py" <files>` from `$HOME/x402-review`; add `--kind source --source` for the PR 3 code and config, which the lint skips otherwise. It reads errors (placeholders, em dash, local paths, private source, retired terms, headings the upstream template requires, front matter, the Syntax regex against the test cases) and warnings (chain id, flat negatives, hedges, live claims without a source, a namespace described as filed, reviewer names, inline links in CASA files, unchecked boxes). Add `--stale '<string>'` for every string a decision made obsolete. <!-- slop-lint: ignore -->
3. `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" <files>`: the house floor.
4. Optional helpers, if installed on the machine (`humanizer`, then `stop-slop`): report only, the operator picks. They are not part of this library.
5. Grep the whole package for the old string after any decision (`--stale`), including the reviewer copies. The 10 Sep reviewer documents, the background documents (`FINDINGS.md`, `caip2-submission/NOTES.md`) and the spec appendix kept the old model wording after the 14 Sep correction.
6. The operator reads the final text once. Then the claims go to `moi-devrel/claim-check`.
7. The blog draft `BLOG-x402-on-moi.md` is `moi-blog`'s, not this skill's. It carries the same stale strings and "Voyage devnet" (`spec-lint.py --kind other` finds them). <!-- slop-lint: ignore -->

## Not yet known
- The final MDAG clause, the byline policy for the PR author, and whether a Foundation page will exist. ASK: Rahul.
