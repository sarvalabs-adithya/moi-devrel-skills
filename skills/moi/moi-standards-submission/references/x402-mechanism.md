# x402 mechanism package: `@x402/moi`

Facts are as of 2026-10-03 unless dated. `ASK: <person>` is defined in `moi-devrel/SKILL.md`. Folder in the review package: `PR-3-x402-mechanism-typescript/`, whose inner tree `x402/` mirrors the target repo. Back to `../SKILL.md`. The package files this file cites by name are in the handover repo at `skills/moi/moi-standards-submission/x402-review-package/` (`AUDIT-2026-09-10.md`, `FUTURE.md`, `ESCROW-RESEARCH-2026-09-10.md`), except `E2E-REGISTRATION.md`, `EXAMPLES-ENTRIES.md`, `STATUS.md` and `escrow-poc/`: not in the handover repo (the previous DevRel's local x402-compat folder); ASK: Rahul. `docs/PR-3-x402-moi-package.md` sections 3 to 5 reproduce the first three.

## What it is
The code that implements the scheme spec, as `typescript/packages/mechanisms/moi` in `x402-foundation/x402`: a client half, a server half and a facilitator half for core's `SchemeNetworkClient`, `SchemeNetworkServer` and `SchemeNetworkFacilitator`. After merge a seller registers one scheme and a buyer registers one scheme, with no per-seller client code. It files after the spec merges. `@x402/moi` is not on npm (404 on 2026-10-03).

## Upstream rules (x402 `CONTRIBUTING.md` and `typescript/CONTRIBUTING.md`, read 2026-10-03)
1. Create `typescript/packages/mechanisms/<chain>/`. "Do not modify core packages." Implement in one SDK.
2. Tests: unit (isolated), integration (client, server and facilitator flow) and e2e (`config/mechanisms_<id>.json` plus a scheme registration in each language's shared server, client and facilitator module).
3. Examples: add the chain, in alphabetical order by network prefix, to `examples/<sdk>/*/advanced/all_networks` for server, client and facilitator.
4. A package publishing workflow in `.github/workflows/` following existing patterns; a README for the package; a Changesets file under `typescript/.changeset/`.
5. Toolchain: Node 22 or newer and pnpm 11.1.1 or newer; `pnpm build`, `pnpm test`, `pnpm test:integration`, `pnpm lint:check`, `pnpm format:check`.
6. Constants: never hardcode chain IDs, token addresses or decimals "from memory"; reference the constants in the codebase. `src/constants.ts` of the package holds a KMOI asset id, decimals and symbol as literals with a comment that they match the SDK. Check each against the installed SDK before filing (my reading of the rule against the file, not a recorded review comment).
7. The contributing text singles out payment and signature code: a human reviews it personally. The package also passes through the code reviewer: "Every code change goes through Gokul's review; the package leaves the org only after Rahul's" (`docs/PR-3-x402-moi-package.md`, 10 Sep).

## Layout (mirrors `@x402/stellar`, the closest merged non-EVM package)
```
typescript/packages/mechanisms/moi/
  package.json tsconfig.json tsup.config.ts vitest.config.ts vitest.integration.config.ts
  eslint.config.js .prettierrc .prettierignore README.md CHANGELOG.md
  src/ constants.ts types.ts utils.ts shared.ts signer.ts reader.ts defaultAssets.ts index.ts
       exact/ index.ts client/ server/ facilitator/
  test/ unit/ (facilitator, reader, server)  integrations/
e2e/config/mechanisms_moi.json
typescript/.changeset/moi-exact-mechanism.md
.github/workflows/publish_npm_scoped_x402_moi.yml
```
Outside the package, three edits to files that already exist upstream (written out in section 3 of `docs/PR-3-x402-moi-package.md`; `E2E-REGISTRATION.md` is not in the handover repo): the e2e server `config.ts`, client `client.ts` and facilitator `index.ts`; and three `all_networks` files (written out in section 4 of the same document; `EXAMPLES-ENTRIES.md` is not in the handover repo). The e2e README requires four edits for a new network, not one: an earlier note that the catalog alone suffices was wrong. It also asks for the new `SERVER_*` and `CLIENT_*` names in `e2e/.env-local` (a public template of placeholders) and in its Environment Variables section (read 2026-10-03); the package does not carry those two edits yet. Names only: `SERVER_MOI_ADDRESS` and `CLIENT_MOI_MNEMONIC`, as `CLIENT_KEETA_MNEMONIC` is the precedent for a phrase-based client.

## How it behaves
- Client: submits its own `Transfer`, waits for the receipt (`interaction.wait()`), checks the interaction-level status, then signs the claim with key 0. It refuses to build a payload without `extra.resource`.
- Server: copies `ResourceInfo.url` into `extra.resource` through `enrichPaymentRequiredResponse`; prices in atomic units or `"0.10 KMOI"`; dollar prices are refused unless the developer calls `registerMoneyParser`.
- Facilitator: reads only. `getSigners()` returns an empty list, `getExtra()` returns `{ areFeesSponsored: false }`, and replay uses one atomic `reserve` on a spent store. The in-memory store is for e2e only; production needs a durable one. A chain reader ships (`createMoiChainReader`) so a facilitator runs with no glue.
- Reason strings (8; the spec's "namespace as Stellar does" and the `invalid_exact_<chain>_*` pattern of four merged specs differ from this `moi_exact_*` form: `open-decisions.md` 21): `moi_exact_already_spent`, `moi_exact_chain_read_failed`, `moi_exact_invalid_payload`, `moi_exact_invalid_signature`, `moi_exact_payment_expired`, `moi_exact_requirements_mismatch`, `moi_exact_transfer_mismatch`, `moi_exact_transfer_not_found`.
- Env names the tests and e2e use: `CLIENT_MOI_MNEMONIC`, `SERVER_MOI_ADDRESS`, `MOI_RPC_URL`, `MOI_ASSET_ID`. Values are never recorded. `keys-and-access.md` in `moi-devrel/references/` has no row for them in the standards work (it lists `MOI_RPC_URL` for the Launchpad only): ASK: Rahul to add them.

## What "verified" covers here (10 Sep) and what it does not
Run against dependencies installed fresh from npm: `@x402/core` 2.25.0, `js-moi-sdk` 0.9.0-rc2, `js-polo` 0.1.5, with upstream's `tsconfig.base.json`: `tsc --noEmit` clean; ESLint with Stellar's exact plugin set 0 errors and 0 warnings; Prettier clean; 36 unit tests with a 70% coverage threshold; a live read-back of a settled devnet transfer. The 36 is the total of `it(` and `test(` calls in the three unit files on 2026-10-03 (11 reader, 17 facilitator, 8 server); `AUDIT-2026-09-10.md` splits it 14, 14 and 8. Quote the total only, after a recount.
Not run: the full pay, prove, settle round trip. It needs `CLIENT_MOI_MNEMONIC` for a funded devnet wallet and `SERVER_MOI_ADDRESS`, and it has never executed. The PR checkbox stays unticked until it has. How it is run, by whom, and why it is a GATE: "The round trip" below. `moi-devrel/test-round` structures a test pass.
Re-verify before filing, because the ground moved: `@x402/core` is 2.28.0 on npm (2026-09-29) against the verified 2.25.0; upstream added a `casper` mechanism; a devnet reset wipes the fixtures; `net.Version` is 0.13.0.

## Before filing: the checklist
1. Spec merged (or at least open), CASA open. 2. Re-run the verification ladder against the current `@x402/core` (`verification.md`). 3. `MOI_ASSET_ID` defaults to the SDK's KMOI id, already the post-0.13.0 id; against an older node pass the old one. 4. Fuel price: the SDK default 50 anu equals the node's minimum as of v0.13.0 (50 as of 2026-09-10 STATUS; re-read). 5. If devnet was reset, refresh the `SETTLED` fixture in `exact-moi.test.ts` with any settled `Transfer`; the reader unit fixture is self-contained. 6. The round trip (GATE; the operator runs it: "The round trip" below). 7. `payer` versus `fee_payer`: the package sets no fee payer, so nothing depends on it, but the spec line does (`x402-scheme-spec.md` rule 6). 8. Changeset at `typescript/.changeset/` in the x402 repo (the repo root is not read by Changesets). 9. Publish workflow copies Stellar's pattern (pinned action SHAs, OIDC trusted publishing, `environment: npm`, Node 24, `pnpm publish --provenance --access public`). 10. `spec-lint.py` on the README and the PR text. 11. Examples entries in alphabetical order of network prefix. The drafts say `moi` goes after `hedera` and before `near`, but the upstream clients example (`examples/typescript/clients/advanced/all_networks.ts`, read 2026-10-03) imports `@x402/keeta` before `@x402/near` and puts `@x402/hedera` after `@x402/stellar`, so the file is not strictly alphabetical: place `moi` where the order of the files on the day puts it. 12. Docs entries: other chains' entries arrived as separate small docs pull requests in at least two cases (`umbrella.md`, "Listing and publishing"); ask before assuming this PR lists MOI. 13. Add the two names above (`SERVER_MOI_ADDRESS`, `CLIENT_MOI_MNEMONIC`) to `e2e/.env-local` and to the e2e README's Environment Variables section in the x402 repo.

## Known defects in the PR 3 copy (read 2026-10-03)
- "Voyage devnet" on 11 lines of 7 files: the e2e catalog name, `constants.ts`, `reader.ts`, `signer.ts`, both test files that name it, the package `README.md`. Say devnet (`wording.md` 5). <!-- slop-lint: ignore -->
- `src/constants.ts` says the namespace profile was "filed with" CASA. Nothing was filed. Reword to what is true on the day of filing.
- The PR text carries the internal-review line and unticked boxes (`templates/pr-description-x402.md` replaces it).
- `python3 "$SKILLS/moi-standards-submission/scripts/spec-lint.py" --kind source --source <the x402/ folder>` finds the first two; it reads code and config only with `--source`.

## The round trip
`pnpm test:integration` (run in `typescript/packages/mechanisms/moi` of the fork) reads a settled devnet transfer back with the network alone, and runs the full pay, prove, settle cycle only when `CLIENT_MOI_MNEMONIC` and `SERVER_MOI_ADDRESS` are set. With them set it submits an interaction and spends devnet funds (GATE). The operator runs it in their own terminal: Claude never sees, asks for or repeats the phrase (`moi-devrel/references/consent-and-identity.md` sections 4 and 5). Use a wallet made only for devnet in the MOI Wallet extension, set the variable at a hidden prompt (item 6 of section 4 there), and unset it afterwards. The operator pastes back the pass and fail lines only; Claude checks them for secret-shaped text first. `SETTLED` in `exact-moi.test.ts` names a transfer of 2026-09-10; the devnet was re-initialised around 2026-09-10 to 11 (`moi-devrel/claim-check/references/live-reads.md`), so that read-back probably fails now (inferred, not run): refresh the fixture with any settled `Transfer`.

## Publishing is not in MOI's hands (inferred)
The draft workflow runs only when `github.repository == 'x402-foundation/x402'` on `main`, from `workflow_dispatch`, with `environment: npm`. So the upstream repository, not a MOI fork, runs it, and someone with rights to that environment must trigger it. Who that is, and whether MOI owns an npm organisation, is not recorded. ASK: Rahul. The package version in `package.json` was set to 2.25.0, the core version: confirm upstream's rule for a new package's first version with the maintainers.

## State (as of 2026-10-03)
Built 9 Sep, rebuilt and verified 10 Sep. The reader, `keyId` enforcement and 28 unit tests (17 facilitator, 11 reader at the local head, counted 2026-10-03) are in local commits; the 8 server tests that make 36, the default assets, the workflow and the changeset move are uncommitted or untracked (`umbrella.md`, generations 2 to 4). Known stale items in the reviewer docs: `review-package/README.md` (committed) says 28 and 13 unit tests, while the audit says 36.

## Not yet known
- How MOI gets its docs and network-page entries (`umbrella.md`, "Listing and publishing"). ASK: Rahul, then the maintainers in the proposal issue.
- Whether the live round trip ran, with which wallet, and who authorised the spend. ASK: Rahul. The operator funds a devnet-only wallet from the public Voyage faucet page; ASK: Gokul if it is empty.
- Who runs the publish workflow and owns the `npm` environment. ASK: Rahul.
- Whether the hosted facilitator with a free tier (`FUTURE.md` 4) will exist. ASK: Rahul.
- Whether the Coco compiler finding and the `XBIND` stability question went to the Coco team and to Gokul (`escrow-poc/README.md`; `ESCROW-RESEARCH-2026-09-10.md`). ASK: Gokul, Robert Špendl.
