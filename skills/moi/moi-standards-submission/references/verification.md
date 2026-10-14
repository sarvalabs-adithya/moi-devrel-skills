# Verification: what "verified" meant, and the passes that were run

Facts are as of 2026-10-03 unless dated. `ASK: <person>` is defined in `moi-devrel/SKILL.md`. The claim ledger and its verdicts belong to `moi-devrel/claim-check`; this file says what to check in a standards package and how the September 2026 passes went. Back to `../SKILL.md`. The package files this file cites by name (`AUDIT-2026-09-10.md` and `ESCROW-RESEARCH-2026-09-10.md`) are in the handover repo at `skills/moi/moi-standards-submission/x402-review-package/`. `FINDINGS.md`, `STATUS.md` and `escrow-poc/` are not in the handover repo (the previous DevRel's local x402-compat folder); ASK: Rahul.

## What "verified" means
The brief on 2026-09-09 was: build the documents properly first, then review every claim against actual MOI source, then run verification until satisfied. Three rules came out of it.
1. Say what is verified and how. Every finding in `FINDINGS.md` ends with "Checked: ...", naming the tool or source.
2. "Verified" never covers what has not run. The one unrun item (the live round trip with a funded wallet) is stated in the README, the audit and `STATUS.md` every time, and its PR checkbox stays unticked.
3. A refuted claim is fixed everywhere it appears, and the commit says so. A claim that only an invented example supports is removed.

For a specification, verified means:
- Each MUST rule traces to a source: public package types, the live wire, or private source read read-only and then phrased without private paths.
- The interaction and receipt bodies in rule 7 were transcribed from a real settled transfer on devnet, not inferred from the SDK schema (`d3a0218`).
- The spec and the code agree on field names, order and rules (the canonical claim array equals `canonicalClaim` in `src/shared.ts`).
- Every citation was opened. Two spec citations produced by agents did not exist and were discarded.
- Every count is recounted on the day (`umbrella.md` census).
For the package, verified means `tsc --noEmit` clean, ESLint with upstream's own config (copied from `@x402/stellar`) at 0 errors and 0 warnings, Prettier clean, unit tests passing above the 70% coverage threshold, and an integration read-back of a settled devnet transfer. It does not mean the round trip ran (`x402-mechanism.md`).

## The seven rungs
Each rung catches what the one before cannot. Run them in order, again after any change of dependency version or a devnet reset. Ledger rows, verdicts and the independent second pass are `moi-devrel/claim-check`; the order of authority is `moi-devrel/claim-check/references/sources-of-truth.md`.
| # | Rung | How | Caught in September |
|---|---|---|---|
| 1 | Public package source | GATE (a download): in a scratch folder made with `mktemp -d`, run `npm install --ignore-scripts @x402/core js-moi-sdk js-polo` and read the shipped `.d.ts`; or `npm pack` and read. State the package names, source and size and ask first. Public readers: `cdn.jsdelivr.net/npm/<package>@<version>/` lists the files without installing anything | `PaymentFlowName` and `SpendControls` found (`FINDINGS.md` 4, 5). `areFeesSponsored` is not a `SchemeNetworkFacilitator` member (`2499d30`) |
| 2 | Upstream live state | The census commands in `umbrella.md`; quote docs verbatim | 55 became 49; the v1 enum has 17 entries, not 16; cardano landed, so 12 mechanisms (`2499d30`, `269ab19`) |
| 3 | Private source, read-only | `moi-devrel/claim-check/references/sources-of-truth.md`, "Private source": `git show <ref>:<path>` at a tag, never a checkout or fetch. Then write the public text without private paths | Four claims refuted (`269ab19`): the identifier layout, "go-moi is public", `moi:mainnet` listed as live, 36 RPC methods against 42. The numbers in `STATUS.md` were checked at go-moi `develop` tip `01b0ae58` of 2026-09-07 and go-pisa v0.8.0, not at the v0.13.0 tag |
| 4 | Live network | `moi-devrel/claim-check/references/live-reads.md`: `net.Version`, the network ID method, a real `moi.InteractionByHash`. Ground truth beats the source tip | The RPC spells `sender.sequence_id`, `ix_participants`, hex `tx_type` (`d3a0218`, `540f53b`); `net.Network` does not exist (`5b2d089`); devnet answered `payer` and 0.12.0 on 2026-09-10 while the tip had `fee_payer` |
| 5 | Mechanical | In the clone of the fork of `x402-foundation/x402`, with the PR 3 tree copied in (`umbrella.md`, "Filing mechanics"). GATE (an install): `cd typescript`, `pnpm install --frozen-lockfile --ignore-scripts`, `pnpm build`. Then `cd packages/mechanisms/moi`: `pnpm exec tsc --noEmit`, `pnpm lint:check`, `pnpm format:check`, `pnpm test`, and `pnpm test:integration` without the wallet variables set (read-only) | `keyId` documented but not enforced (`03720c3`); a test passing `undefined` to a defaulted parameter did not test the fail-closed case it claimed |
| 6 | Comparison with the closest merged package | Diff `@x402/stellar` against `@x402/moi`: file list, `package.json` keys, workflow, changeset, e2e schema | `getExtra()` used `feesSponsored` where Stellar and its spec say `areFeesSponsored`; unpinned `@v4` actions in the workflow; the changeset sat at the repo root |
| 7 | Adversarial sweep | Attack the design claims ("is `upfront` the only production-grade flow?") and open every citation | Logic-held escrow is expressible, overturning an earlier claim (`ESCROW-RESEARCH-2026-09-10.md`, local) |
The September sweeps used sub-agents ("62 sonnet agents" in the escrow note), which the previous operator allowed explicitly on 2026-09-10 and does not allow by default. Use them only when the operator asks, with the count and model stated first (`moi-devrel/claim-check/references/independent-check.md`).

## The passes that were run (all 2026-09-09 and 2026-09-10)
| Date | Pass | Result | Where recorded |
|---|---|---|---|
| 09-09 | CASA docs against js-moi-sdk, js-polo, the registry and the ChainAgnostic repo | 4 refuted claims corrected; the numeric `Chain` enum exists, so "MOI has no chain id" was rewritten as a narrower negative about the RPC. That narrower negative is itself contested since the docs list `net.NetworkID` (`wording.md` row 4) | `269ab19`, `2a7cda9` | <!-- slop-lint: ignore -->
| 09-09 | Template conformance of the CAIP-2 profile | Regex accepted a trailing hyphen the prose forbade; `type` and `title` aligned to the template; `requires` made an array | `18b10e2` |
| 09-09 | Upstream and CASA live-state pass | CASA: zero refutations. x402: five fixes | `2499d30` |
| 09-09 | Review of the spec | Five gaps: resource binding signed but never checked; `maxTimeoutSeconds` never enforced; `keyId` and `nonce` inert; asset transfer method and reserved keys invented | `f770c88`, `1fd897b`, `d3a0218` |
| 09-09 | Rebuild of the package | Nine divergences from the spec, the worst a dead resource binding | `7cd3f5d` |
| 09-10 | Probing the profile | Invented `net.Network` example removed; "no genesis artefact" overturned | `5b2d089` |
| 09-10 | End-to-end audit, then the Stellar comparison, then a second pass | 36 of 36 tests, lint clean; chain reader added; `keyId` enforced | `AUDIT-2026-09-10.md`, `STATUS.md`, `03720c3` |
| 09-10 | Escrow research | Logic-held escrow is expressible; proof of concept compiles, never executed | `ESCROW-RESEARCH-2026-09-10.md`, `escrow-poc/` |
Pattern across all of them: the refuted claims were counts, absolute negatives, descriptions of what code does that it did not do, invented names, and citations that did not exist. The full table with corrected forms is `moi-devrel/claim-check/references/caught-claims.md`, section E.

## Not re-run since 2026-09-10
- Rungs 1, 5 and 6 against the current dependencies: `@x402/core` is 2.28.0 (published 2026-09-29) against the verified 2.25.0, and upstream has 13 mechanisms.
- Rung 3 at the v0.13.0 tag: the checks used the `develop` tip. `moi-devrel/claim-check/references/sources-of-truth.md` records that the tag exists in a second clone only.
- The round trip. Rung 4 for the network ID: re-probed on 2026-10-03, the method is still absent.

## Silent failures
1. A refused transfer still returns an interaction hash and a mined receipt. Possession of a hash proves nothing: the receipt status must be 0.
2. Simulation accepts what the chain later refuses; read the receipt (`moi-devrel/references/devnet.md`).
3. A devnet reset wipes accounts, assets and receipts. A fixture settled before the reset stops resolving. Keep unit fixtures self-contained.
4. The Coco optimiser at `-O 2` dropped a bare extern call with no return value (found while building the escrow proof of concept; a report to the Coco team is pending).
5. cocolab loads balances only for registered user actors, so a cocolab pass proves nothing about a logic's own balance.
6. Agents invent citations, names and numbers. Open every one.

## Not yet known
- Whether the Coco finding and the `XBIND` stability question reached Gokul and the Coco team. ASK: Gokul.
- Whether any private-source claim holds at the v0.13.0 tag. Needs read access: ASK: Rahul who grants it.
