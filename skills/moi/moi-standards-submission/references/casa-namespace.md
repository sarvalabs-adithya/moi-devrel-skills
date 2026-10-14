# CASA namespace: the `moi` pull request to `ChainAgnostic/namespaces`

Facts are as of 2026-10-03 unless dated. `ASK: <person>` is defined in `moi-devrel/SKILL.md`. Folder in the review package: `PR-1-CASA-namespaces-moi/`. Back to `../SKILL.md`.

## What it is
CASA publishes the CAIP specifications: conventions for naming chains, accounts and assets across blockchains. CAIP-2 names a chain `namespace:reference` (`eip155:1`, a Solana genesis hash). Registering `moi` is one pull request that adds a folder with two files; once merged, `moi:<reference>` is official and x402 v2, wallets and explorers can name a MOI network. The grammar (CAIP-2, read 2026-10-03): namespace `[-a-z0-9]{3,8}`, reference `[-_a-zA-Z0-9]{1,32}`, at most 41 characters. A profile may restrict the reference further, and the MOI draft does (lowercase, no underscore).

## Upstream rules (CASA `CONTRIBUTING.md`, `_template/`, CAIP-104; read 2026-10-03)
1. Copy `_template/`, fill `README.md` first (CAIP-104), rename the folder to the short lowercase abbreviation, then fill `caip2.md` (CAIP-2). The first PR should be a complete draft of the README with at least CAIP-2 addressed.
2. An editor reviews the first PR for a new namespace by hand and assigns the number before merging.
3. Include a `discussions-to` header with one or more URLs (it may be an array; an issue on a fork also helps). The listed author is who gets chased.
4. Front matter: keys in the CAIP-104 order (`namespace-identifier`, `title`, `author`, `discussions-to`, `status`, `type`, `created`, `requires`); lists as `["a", "b"]`; dates `yyyy-mm-dd`; `status` one of Draft, Last Call, Accepted, Active, Abandoned, Rejected, Superseded; `type` one of Standards Track, Informational, Meta; author as `Name (@handle)` or `Name <email>`. The merged `caip2.md` files of neo, stellar and aptos say `type: Standard`, and their `README.md` files say Informational.
5. Style: one line per sentence is preferred, not required. Define links as `[Name]: URL` at the end of References and use the alias in the text. Link the rendered form on chainagnostic.org, not the git repository. Link to other sections with markdown heading links, not HTML anchors.
6. Optional: render locally with `bundle exec jekyll serve`. That needs Ruby gems installed on the operator's machine (GATE: an install), so it is the operator's call.
No PR template file was found in the namespaces repo at the two usual `.github` paths (404 on 2026-10-03), so the body in `PR-DESCRIPTION.md` is the project's own.

## The two files
| File | Template sections | MOI draft |
|---|---|---|
| `namespaces/moi/README.md` (CAIP-104 profile) | H1 "Namespace for ...", Rationale (~200 words), Governance (~200 words), References, Copyright (CC0) | `namespace-identifier: moi`, `title: MOI Ecosystem`, `status: Draft`, `type: Informational`, `created: 2026-08-08`, `requires: ["CAIP-2"]` |
| `namespaces/moi/caip2.md` (CAIP-2 profile) | H1 "CAIP-2"; Introduction; Specification with Semantics, Syntax, Resolution Mechanics; Rationale; Backwards Compatibility; Test Cases; References; Copyright. The merged profile of Neo also has Security Considerations | `namespace-identifier: moi-caip2`, `title: MOI - Blockchain ID Specification`, `discussions-to` set to the CASA PR's own URL with a `TODO` number | <!-- slop-lint: ignore -->
The author in both is the previous operator, set on 2026-09-09: "CASA chases the listed author on the PR, so this is a commitment to answer". Whether the next operator replaces the name is open (`open-decisions.md` 4).

## The decision that blocks it: the reference format
Do not resolve it here. The formats are numbered 1 to 3 here so they are not confused with conflicts A and B of `open-decisions.md`. Candidates, with what each means (`docs/PR-1-chain-id-edits.md` of 2026-09-14 and the package README's "Decide before filing" table are in `others/standards/x402-review-package/`; `DECISIONS.md` 1 and `FIX-PLAN.md` "New decisions" 1 are not in the handover repo (the previous DevRel's local x402-compat folder); ASK: Rahul): <!-- slop-lint: ignore -->
| Format | Identifier | Where it comes from | Regex | Test cases |
|---|---|---|---|---|
| 1. Names | `moi:devnet`, `moi:mainnet` (reserved) | The draft. Matches `stellar:pubnet` | `^[a-z0-9]([a-z0-9-]{0,30}[a-z0-9])?$` | 4 valid, 8 invalid |
| 2. Numeric network ID | `moi:112` for devnet | The node's internal network ID for devnet is 112; the SDK `Chain` enum has TEST_NET 111, DEV_NET 112, MAIN_NET 113 | `^(0\|[1-9][0-9]{0,9})$` plus a 32-bit bound, copied from Neo's wording | 3 valid, 10 invalid |
| 3. The wallet's string | `moi:14` | MOI Wallet and `wallet-connect-dapp` use it for devnet | not drafted | not drafted |
Three values would split the ecosystem, so the wallet's value has to be reconciled before filing. `FIX-PLAN.md` of 2026-10-01 says the method documented today is `net.NetworkID` (111 local, 112 devnet, 113 Babylon) and that it makes about a dozen sentences of the draft false; the SDK enum labels 111 and 113 differently. Only 112 has two independent sources. If format 2 is chosen, every file that names `moi:devnet` changes together. The audit of 2026-09-10 counted six; on 2026-10-03 the string is in 15 files of the review package (16 with `x402.md`): `caip2.md`, the spec, `constants.ts`, the e2e catalog, the package `README.md`, two test files, `EXAMPLES-ENTRIES.md`, `DECISIONS.md`, the blog draft, the audit, and four files in `docs/` (plus their `.docx` and `.pdf` copies). Run `spec-lint.py --stale 'moi:devnet' <package folder>` after the decision and recount. <!-- slop-lint: ignore -->

## Resolution Mechanics: never a made-up method
Most merged namespaces show a real request and response here: of the 48 `caip2.md` files in the repo on 2026-10-03, 39 have a Resolution section with a code block (Neo `getversion` to `protocol.network`, Stellar Horizon `/` to `network_passphrase`, Klever `/node/status`, Tenzro `tenzro_getBlock`), 4 describe it in a line of prose or inline code, and 5 have no such section (Qubic has no `caip2.md`). The older template calls the section "Resolution Method"; the current template and the lint use "Resolution Mechanics". The package's own audit and `DECISIONS.md` say "every merged namespace" and "no precedent for filing without one": the count above contradicts that, but the rule stands, because a stub is worse than a short honest section. A curl example for a method that did not exist was removed on 2026-09-10 (`5b2d089`): "a placeholder dressed as a specification". The section now says what is required and what MOI exposes (42 RPC methods in js-moi-sdk 0.9.0-rc2; `net.Version` is the software version, `net.Info` is the node's own peer id, `moi.Tesseract` needs an account). Do not file a stub: write the real call when it exists.
Read-only probe, host `dev.voyage-rpc.moi.technology`, method names only:
```
for m in net.Version net.NetworkID net.ChainId net.ChainID net.Network net.NetworkInfo; do printf "%-16s " "$m"; curl -sS -m 20 -X POST "https://dev.voyage-rpc.moi.technology/devnet/" -H 'content-type: application/json' -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"$m\",\"params\":[]}" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("result", d.get("error",{}).get("code")))'; done
```
Result on 2026-10-03 (read at 15:26 UTC and again at 17:34 UTC): `net.Version` answered 0.13.0 and the other five answered error -32601. The public docs list the method: `docs.moi.technology/docs/build/json-rpc` documents `net.NetworkID` as returning an integer, with 111 for Local, 112 for Devnet and 113 for Babylon (read 2026-10-03). So the documented method is absent from the running build, and the page and the node disagree. On 2026-09-09 and 10 the probes of `net.Network`, `net.NetworkInfo`, `net.ChainId`, `moi.Network`, `moi.ChainId`, `moi.NetworkInfo`, `net.Chain` and `moi.Chain` were also method-not-found. The placeholder in the 14 September edit set is `net.ChainId` with result field `chain_id`; it is a placeholder, not a fact. ASK: Gokul for the method, the result field and the integer type (it sets the 32-bit bound), and whether the docs page describes a build that has not shipped. <!-- slop-lint: ignore -->
Not usable as a reference: `commit_info.cluster_id` (rotates with the validator cluster and differs at tesseract 0), `KMOI_ASSET_ID` (a constant identical on every network), the genesis tesseract hash (changes whenever a network is re-initialised, reachable only through a founding account, and 32 bytes against a 32-character limit).

## Test cases and the checks the audit ran
Each case carries a reason, as in Neo's table (5 valid, 10 invalid). Run `python3 "$SKILLS/moi-standards-submission/scripts/spec-lint.py" PR-1-CASA-namespaces-moi/namespaces/moi/*.md` from `$HOME/x402-review`. It checks the front matter order and values, the headings the template lists, and the Syntax regex against every case, in code blocks or tables. The audit's other checks stay by hand: no private-repo or local-path citation (the lint catches those too) and that every link opens.

## Wording that was corrected here
Participant-centric, the MDAG sentence, the governance sentence, network ID, the genesis tesseract correction (14 Sep) and "devnet" not "Voyage devnet" are in `wording.md`. As of 2026-10-03 the drafts still carry: "no genesis block" and "no chain id" statements, "Voyage devnet", em dashes, inline links, and the claim that the public networks are "operated under Sarva Labs' stewardship", which the 14 Sep draft flagged to confirm (`moi-devrel/references/terminology.md` Contested 3). The README says the node is built in public repositories; go-moi is not public (`traps.md` 16). <!-- slop-lint: ignore -->

## Filing (each step marked GATE needs a yes)
1. GATE: fork `ChainAgnostic/namespaces` under the work account, then follow `umbrella.md`, "Filing mechanics" (clone, identity, signing). 2. Copy the two files into `moi/` and run `spec-lint.py`. 3. Fill `discussions-to` with the URL that will be monitored; the draft's route is the PR's own URL, which exists only after step 5. 4. Tick no box that is not true. 5. GATE: open the PR with the title `Add moi namespace (CAIP-104 profile + CAIP-2 chains profile)`. 6. Answer at `discussions-to` the same day questions arrive: the only real CASA failure was an author silent for 587 days.

## State of the work (as of 2026-10-03)
Text complete except: Resolution Mechanics, `discussions-to` number, the reference format, and the wording defects above. The 2026-10-01 corrections are in `docs/PR-1-CASA-namespace.md` of the handover package (the markdown, dated 13 October 2026, says participant-centric). Its `.docx` and `.pdf` exports (6 October) were not regenerated and still say "account-centric" (checked in the `.docx`, 14 October 2026): regenerate them before anyone reviews them. Internal review is not recorded. Nothing is filed. <!-- slop-lint: ignore -->

## Not yet known
- The RPC method, result field and type; whether devnet reports 112. ASK: Gokul.
- Which of formats 1, 2 or 3 Rahul chose after the 14 Sep call. ASK: Rahul.
- Who owns MOI Wallet's `moi:14` and whether it will move. ASK: Rahul.
