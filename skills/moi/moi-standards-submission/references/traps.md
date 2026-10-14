# Traps: facts that fail silently in a standards submission

Facts are as of 2026-10-03 unless dated. Each row is a rule with the incident or the evidence behind it. `ASK: <person>` is defined in `moi-devrel/SKILL.md`. Back to `../SKILL.md`. The package file this file cites by name (`AUDIT-2026-09-10.md`) is in the handover repo at `others/standards/x402-review-package/`. `FINDINGS.md`, `UPSTREAM.md`, `STATUS.md` and `caip2-submission/` are not in the handover repo (the previous DevRel's local x402-compat folder; the public branch holds an older copy); ASK: Rahul.

## Process
| # | Rule | Incident or evidence |
|---|---|---|
| 1 | Nothing is pushed, filed or posted before the operator says so and the internal gate has cleared | 2026-08-26: the research brief was "do not push anything anywhere". 2026-09-09: after "commit and push the current branch" the files meant for review were not on the remote, and the rule became that nothing is pushed unless the operator says so |
| 2 | Keep the filing order: CASA, then the spec, then the package. The spec may open while CASA is in review and must not merge first | `UPSTREAM.md`: the spec is reviewed and merged before any implementation is looked at. `AUDIT-2026-09-10.md`, Cross-PR |
| 3 | Name the target repo beside every PR number | The package numbers four submissions (CASA is 1). `UPSTREAM.md` numbers only x402's three (the spec is 1) |
| 4 | Name a human who answers upstream, and watch `discussions-to` | The only real CASA failure in 100 closed PRs was an author silent for 587 days (`FINDINGS.md` 8) |
| 5 | Work identity only on commits, forks and PRs; no personal account or mail anywhere | 2026-09-02 a PR opened under a personal account was cancelled and redone. Set `PREFLIGHT_EXPECT_GH_LOGIN` and run `moi-devrel/scripts/preflight.sh` before a commit |
| 6 | Keep the package out of a public repository | The pushed branch of `MOI-Webinars` holds the first generation with a reviewer's name in the PR descriptions and in `UPSTREAM.md`. The newest `STATUS.md` and the escrow note cite private source by path or line range. A push publishes |
| 7 | Upstream commits are new commits in a fork with no AI trailer | All 60 commits in `MOI-Webinars` that touch `x402-compat/` end with a `Co-Authored-By` trailer naming an AI (counted 2026-10-03, 4 unpushed). Do not copy their messages. The 2026-10-01 clean-up covered open PRs only, and rewriting pushed history is a gate |
| 8 | Audit and inventory work stays local and read-only; use plain GET requests, not `gh`, for public census reads | 2026-09-28: nothing may show in a teammate's feed. The census here calls `api.github.com` and `raw.githubusercontent.com` with no login |
| 9 | Do not use sub-agents by default | The September sweeps used them under an explicit waiver on 2026-09-10 ("62 sonnet agents"). Spend is the operator's call: state the count first |
| 10 | Do not copy the superseded prototype | `moi-x402/` targets x402 v1 and diverged from the spec in nine ways. Keep it for history only |
| 11 | The upstream repository is `x402-foundation/x402`, not `coinbase/x402` | `FINDINGS.md` 1: a Linux Foundation project since the 2026-07-14 launch |

## The text
| # | Rule | Incident or evidence |
|---|---|---|
| 12 | Recount every number after every edit, and write the date beside it | Namespaces 55, then 50, then 49. Unit tests 28, 13, 36. RPC methods 36, then 42. `moi:devnet` in six files on 2026-09-10 and 15 on 2026-10-03. `exact` specs "17" against 18 files. Mechanisms 12 against 13 |
| 13 | After a decision, grep every copy for the old string, including the reviewer copies | The 14 Sep correction reached the PR 1 files (1 Oct) and not the `.docx` and `.pdf` exports in `docs/` (6 Oct, still "account-centric"), `FINDINGS.md` line 145, `caip2-submission/NOTES.md` line 21, or the spec appendix. `UPSTREAM.md` says the spec is written in its header and not written in its last section | <!-- slop-lint: ignore -->
| 14 | State only what was verified, in its narrow form | "MOI has no chain id" was refuted by the SDK enum. "No genesis artefact" was refuted by probing | <!-- slop-lint: ignore -->
| 15 | Never write a placeholder dressed as a specification | A curl example for `net.Network`, a method that does not exist, was removed (`5b2d089`). A reviewer reads it as a claim |
| 16 | Public text names no private repo, no local path, no reviewer, no internal checkbox and no untrue "filed" | "The node software is in public repositories" was refuted (go-moi is not readable), and the CASA README draft still says it. All three PR description drafts carry "Internal review (<reviewer's name>) complete"; the `TODO` CASA number sits in `caip2.md` and in the spec PR text, not in the other two. A code comment in `constants.ts` says the namespace was "filed with" CASA (read 2026-10-03) | <!-- slop-lint: ignore -->
| 17 | Use the upstream PR template's headings | x402's template has Description, Tests and Checklist and says to fill it completely. None of the three drafts uses them (found 2026-10-03) |
| 18 | The link to the CASA page in the spec is dead until CASA merges | `namespaces.chainagnostic.org/moi/caip2` answered 404 on 2026-10-03; `stellar/caip2` answered 200 |
| 19 | Say "devnet" | The CASA drafts, the spec and the blog draft still say "Voyage devnet" (2026-09-25 correction) | <!-- slop-lint: ignore -->
| 20 | Place the `examples/` entries by the files on the day | The drafts say after `hedera` and before `near`; `keeta` now sorts between them |
| 21 | Overpayment is accepted by design | Rules 4 and 7 compare with `>=`. A seller that wants exact semantics compares for equality. Say so in the spec |
| 22 | Do not write a made-up reason vocabulary into the spec | `errorReason` is free-form upstream; only Stellar names reasons, namespaced. The package uses `moi_exact_*` |

## The chain
| # | Rule | Incident or evidence |
|---|---|---|
| 23 | Devnet is not the source tip | `fee_payer` was in the `develop` tip on 2026-09-07 and devnet answered `payer` and 0.12.0 on 2026-09-10. On 2026-10-03 devnet answers `fee_payer` and 0.13.0; `net.NetworkID` still returns -32601 on 14 October 2026. js-moi-sdk 0.9.0-rc2 was reported on 2026-09-10 to still send `payer`. Read the wire the day you write the line |
| 24 | A reset wipes state | Accounts, assets and receipts do not survive a wipe. `FINDINGS.md` 10 (written 9 Sep) records one; the moipod v0.13.0 release wiped devnet again on 2026-09-11 (`moi-devrel/references/devnet.md`). Refresh the `SETTLED` fixture in the integration test; keep the unit fixture self-contained |
| 25 | A hash is not a payment | A refused transfer still returns an interaction hash and a mined receipt. The facilitator must read `receipt.status` 0 |
| 26 | The same identifier exists on every MOI network | A participant identifier derives from the public key. A transfer sent to the wrong endpoint may succeed, which is why `network` sits inside the signed claim |
| 27 | A security property that the code does not enforce is not a property | The resource binding was signed and never checked (`7cd3f5d`). `STATUS.md` said `keyId` was pinned while the code only documented it (`03720c3`) |
| 28 | Use an atomic reserve for replay | A has-then-add store leaves a race under `upfront`. The in-memory store is for the e2e harness only |
| 29 | Agents invent citations and numbers | Two spec citations produced by agents did not exist (2026-09-10). Open every one |
| 30 | A passing check at one version says nothing about the next | The package was verified against `@x402/core` 2.25.0; npm `latest` was 2.28.0 on 2026-09-29 |
| 31 | The CAIP-2 reference candidates are `moi:devnet`, `moi:112` and `moi:14` | See `open-decisions.md`, conflict A (formats 1 to 3). All the files change together when one is chosen |

## Found when the skill was checked against upstream (2026-10-03)
| # | Rule | Incident or evidence |
|---|---|---|
| 32 | Lint code and config too, not only Markdown | `spec-lint.py` reads `.md` unless given `--source`; the PR 3 code held "Voyage devnet" on 11 lines and a false "filed" comment (2026-10-03) | <!-- slop-lint: ignore -->
| 33 | Do not assume every merged CASA namespace has a Resolution call | 39 of 48 `caip2.md` files have a code block there, 9 do not (2026-10-03). The package audit says "every". Say "most" and count on the day |
| 34 | Match the reason-string pattern before filing | Four merged specs use `invalid_exact_<chain>_<reason>`; the package uses `moi_exact_*` (`open-decisions.md` 21) |
| 35 | Listing and docs are separate small PRs upstream | #3578 (merged 2026-09-27) edited `docs/schemes/*.mdx`; do not assume the package PR lists MOI |

## Not yet known
- Whether the first generation on the public branch should stay there (`open-decisions.md` 16). ASK: Rahul.
