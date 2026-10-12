# x402 scheme specification: `specs/schemes/exact/scheme_exact_moi.md`

Facts are as of 2026-10-03 unless dated. `ASK: <person>` is defined in `moi-devrel/SKILL.md`. Folder in the review package: `PR-2-x402-scheme-spec/`, whose inner tree `x402/specs/schemes/exact/` mirrors the target repo. Back to `../SKILL.md`. The package files this file cites by name (`ESCROW-RESEARCH-2026-09-10.md` and `AUDIT-2026-09-10.md`) are untracked and exist only on the previous operator's machine; ASK: Adithya for a copy (`umbrella.md`, generation 4).

## What it is
The first x402 pull request, and specification only, no code. It documents what a MOI payment payload contains, how a seller or facilitator verifies it and how settlement works. Upstream reviews the spec before it looks at any code.

## Upstream rules (x402 `CONTRIBUTING.md` and `specs/CONTRIBUTING.md`, read 2026-10-03)
1. Path `specs/schemes/<scheme>/scheme_<scheme>_<chain>.md`; follow `scheme_exact_evm.md`. It "must include" the payload structure, the verification logic and the settlement logic.
2. Step 1 of the spec guide is an issue or discussion that states the problem, the approach and why existing schemes do not suffice. No such draft exists in the package: `open-decisions.md` 13.
3. Wording: MUST, MUST NOT, SHOULD, MAY used precisely; a concrete example in every section; reference core types instead of redefining them; a security section covering replay prevention, authorization scope and settlement atomicity.
4. Templates (`scheme_impl_template.md`, first heading `# Scheme: <name> <network kind>`): Summary, Payment header payload, Verification, Settlement, Appendix. The merged specs add more, and the MOI draft follows them. Five merged specs (Canton, Concordium, Hedera, SVM, XRPL) open with `# Exact Payment Scheme for ...` instead; the lint follows the template and reports the first heading as missing for such a file (read 2026-10-03).
5. The PR text and signing rules are in `umbrella.md` ("Upstream rules for every x402 PR").

## The section set
| Source | Headings |
|---|---|
| Upstream template (the lint's error list) | Summary; a heading naming the payload; a heading for verification or settlement; Appendix |
| Merged specs, studied 9 Sep (stellar, cardano, evm, aptos, near, ton; the lint's warning list) | Versions supported; Supported Networks with a scope callout; Summary; Protocol Flow (numbered, actor-prefixed); `PaymentRequirements` for exact (example JSON and field definitions); `PAYMENT-SIGNATURE` header payload; Facilitator Settlement Rules (MUST); `PAYMENT-RESPONSE` header payload; Duplicate Settlement Mitigation (vulnerability and mitigation); Security Considerations; Appendix |
`spec-lint.py` reads the file as kind `x402-spec`. Copy the structure of the closest merged spec; do not invent one.

## How the MOI spec is built
| Choice | What the draft says | Why, and the source |
|---|---|---|
| Flow | `upfront`: the buyer settles a native asset transfer, then proves it with a signed claim bound to one resource. `/verify` is omitted; every rule runs in `/settle` | Core's `PaymentFlowName` is `"authorization"`, `"upfront"` or `"escrow"` (`@x402/core` 2.23.0 types). MOI declares `upfront`. `FINDINGS.md` 4 |
| Framing | `upfront` is a choice, not a limit. MOI can express `authorization` (a relayed interaction with a fee payer from moipod v0.13.0, or `Approve`/`TransferFrom`) and `escrow` (`Lockup`/`Release`, or a Coco escrow logic). Both are named as follow-ups | The earlier wording "makes us sound weak" (2026-09-10, `cd834b3`). Logic-held escrow is expressible; an earlier statement that it was not was refuted by an adversarial sweep (`ESCROW-RESEARCH-2026-09-10.md`, local) |
| Headers | `PAYMENT-REQUIRED`, `PAYMENT-SIGNATURE`, `PAYMENT-RESPONSE` | The first draft said `X-PAYMENT`; every merged spec uses the three. The lint flags `X-PAYMENT` |
| Reserved keys | `extra.paymentFlow` is written by core, not by the scheme. `extra.assetTransferMethod` is absent because MOI declares `"default"` and core strips it. `extra.resource` is copied from `ResourceInfo` by the server half so the buyer can sign it | Three inventions were caught and removed: a `flow` key, a `mas0-transfer` method, an error-reason list (`1fd897b`) |
| Claim | Positional JSON array, domain separator first: `["moi-x402-payment-claim-v1", from, network, to, asset, value, txHash, resource, validAfter, validBefore, nonce]`, UTF-8 bytes, ECDSA secp256k1. String escaping pinned to what `JSON.stringify` produces so Go and Python match | `network` was added to the claim on 2026-09-10 (`4cebd07`) because the same identifier exists on every MOI network |
| Rules | Eight MUST rules: shape; signature; key controls payer (`keyId` MUST be 0); claim matches quote including `network`; resource binding (compare against `paymentPayload.resource.url`, fail closed if absent); freshness within `maxTimeoutSeconds`; the transfer settled on chain; replay | Rule 7 reads `moi.InteractionByHash` and `moi.InteractionReceipt`, needs `receipt.status` 0, sender equals `from`, an op of type 5 `ASSET_INVOKE` whose callsite is exactly `Transfer`, and a POLO-decoded `beneficiary` and `amount` |
| Real data | The interaction and receipt bodies in rule 7 were copied from a settled KMOI transfer on devnet, not inferred from the SDK schema | `d3a0218`. The spec shows only truncated ids |
| Scope | Protocol-native fungible assets only (MAS0, and MASN for KMOI). Supported Networks lists only networks that are live; the CAIP profile may reserve more | `AUDIT-2026-09-10.md` |
| Reasons | `errorReason` is free-form upstream, so the spec defines no vocabulary and says implementations SHOULD namespace their reasons as the Stellar scheme does. The package uses `moi_exact_*` strings (eight, listed in `x402-mechanism.md`) | On 2026-09-09 only Stellar named reasons. On 2026-10-03 the Stellar, Canton, Hedera and LNBTC specs name them in the form `invalid_exact_<chain>_<reason>`, so `moi_exact_*` departs from the pattern the draft cites: a reviewer may ask (`open-decisions.md` 21) |
| Appendix | Wire-visible behaviour only. The node and VM are not public, so a reviewer cannot check claims about them | Rule: only public artefacts |

## Precedents and the proposal issue (read 2026-10-03)
Three merged spec-only pull requests to `x402-foundation/x402`, as samples and not as a statistic:
| PR | Title | Opened | Merged | Days |
|---|---|---|---|---|
| #2741 | `docs(specs): add exact scheme spec for Casper Network` | 2026-06-29 | 2026-07-08 | 9 |
| #2849 | `specs(exact): propose Starknet exact scheme for x402 v2 (spec-only)` | 2026-07-14 | 2026-07-24 | 10 |
| #2634 | `Specs(exact): propose Canton exact scheme for x402 (spec-only)`, "Closes #2632" | 2026-06-15 | 2026-08-07 | 53 |
The MOI draft title, `specs: add exact scheme for MOI (moi:*), upfront flow`, matches none of these shapes; use `specs(exact): propose MOI exact scheme for x402 v2 (spec-only)` or ask the maintainers.
The proposal issue (`specs/CONTRIBUTING.md` step 1) needs three parts, each already answered in the package: the problem (a seller cannot name or verify a MOI payment under x402: `FINDINGS.md` 7 and 9), the approach (`exact` on the `upfront` flow with a signed claim bound to one resource and one network, "Summary" of the spec), and why existing schemes do not suffice (the `authorization` flow needs ERC-3009-style detached signing, which MOI does not have: `FINDINGS.md` 4, and the other `exact` specs name their own chain's transfer method, as the table in `docs/core-concepts/network-and-token-support.mdx` shows). Keep it short. Claude drafts it, Rahul approves, the operator posts it (GATE).

## Rules for editing it
1. Every rule is testable and in MUST wording. No invented vocabulary.
2. Spec and code agree on field names and order. Compare the array in the spec with `canonicalClaim` in `src/shared.ts` of PR 3 whenever either changes.
3. The RPC spells fields differently from the signing schema: `sender.sequence_id` (not `sequence`), `ix_participants` (not `participants`), receipt `tx_type` as a hex string. Implementations must use the RPC spelling (`540f53b`).
4. The identifier is 32 bytes: a tag byte, a flags byte, two standard bytes, a 24-byte fingerprint sliced from the compressed public key (no hash) and a 4-byte variant. The first draft listed 30 of 32 bytes.
5. Overpayment is accepted because rules 4 and 7 compare with `>=`. A seller that wants exact semantics compares for equality. Say so; do not hide it.
6. A fee-payer line must match the wire. On 2026-10-03 15:32 UTC `moi.InteractionByHash` on devnet returned the key `fee_payer` and no `payer`, so "named `payer` before moipod v0.13.0" holds. js-moi-sdk 0.9.0-rc2 (npm `latest` on 2026-10-03) was reported on 2026-09-10 to still send `payer`: re-check before the PR, because the spec's anatomy line depends on it (`traps.md` 23). <!-- slop-lint: ignore -->
7. Describe `fee_payer` as a possibility, not a feature in use: an interaction nobody sponsored carries an all-zero `fee_payer` (`moi-devrel/claim-check/references/live-reads.md`).

## State (as of 2026-10-03)
- Rebuilt 9 Sep in one day (about eight commits) and corrected 10 Sep. The latest text is in generation 3 of `umbrella.md` (uncommitted). Run `spec-lint.py` on it first; the checks below are what it reported on the local copy.
- Known defects in that copy: the Appendix paragraph "MOI in brief" still calls MOI account-centric, with a per-account sequence of tesseracts (the text that would go upstream contradicts the 14 Sep correction); "Voyage devnet" in Supported Networks and in rule 7; em dashes throughout; "live" and "in production" sentences without a source marker; the link to `namespaces.chainagnostic.org/moi/caip2` answers 404 until the CASA PR merges (2026-10-03). <!-- slop-lint: ignore -->
- `moi:devnet` appears in the Supported Networks, the examples and the `PAYMENT-RESPONSE` example. It changes with `open-decisions.md` 1.
- The PR description `PR-DESCRIPTION.md` lacks the upstream headings Description, Tests and Checklist, carries an internal-review checkbox and a `TODO` CASA number, and names the pending namespace PR. Use `templates/pr-description-x402.md`. <!-- slop-lint: ignore -->

## What remains
Reference format; CASA opened (the spec may be opened while CASA is in review, never merged first); the proposal issue or discussion; wording defects; upstream headings in the PR text; reviewer clearance; re-check of the `payer` line; GATE: signed commits and the PR.

## Not yet known
- Whether `authorization` and `escrow` follow-up sections are wanted in this PR (not requested). ASK: Rahul.
- Whether the em dash ban covers specs. ASK: Rahul (`open-decisions.md` 9).
- Whether upstream wants the link to the CASA page before it exists. ASK: Rahul, then the x402 maintainers through the proposal discussion.
