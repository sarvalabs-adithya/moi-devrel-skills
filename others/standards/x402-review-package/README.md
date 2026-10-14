# x402 review package: start here

Written 13 October 2026, the day before Adithya (DevRel) leaves, for the next DevRel person at MOI. MOI is a blockchain protocol built by Sarva Labs and governed by the MOI Foundation. This folder holds draft documents, not filed pull requests. Read this page first: it says what each file is, what state it is in, what must be decided before anything is filed, and what the terms mean.

## What the package is

Three proposed contributions to outside projects, so that an AI agent can pay for an HTTP request on MOI using the x402 standard:

| # | Contribution | Where it would go | Draft |
|---|---|---|---|
| a | The CAIP-2 `moi` namespace (CAIP-104 profile plus CAIP-2 chains profile), so `moi:<reference>` is a legal chain identifier | `ChainAgnostic/namespaces` (CASA) | `docs/PR-1-CASA-namespace.md` |
| b | The `exact` payment scheme specification for MOI, using the `upfront` flow | `x402-foundation/x402`, `specs/schemes/exact/scheme_exact_moi.md` | `docs/PR-2-x402-scheme-spec.md` |
| c | The `@x402/moi` TypeScript package (client, server and facilitator halves) | `x402-foundation/x402`, `typescript/packages/mechanisms/moi/` | `docs/PR-3-x402-moi-package.md` |

Around them, four supporting files:

| File | What it is |
|---|---|
| `AUDIT-2026-09-10.md` | The end-to-end check of the three drafts on 10 September 2026. Useful, but a snapshot: its "Not yet done" items are still open (see Status). |
| `ESCROW-RESEARCH-2026-09-10.md` | Research note: can MOI do code-enforced escrow without a custodian? Sound; it is the evidence behind the `escrow` follow-up. |
| `FUTURE.md` | Seven follow-up improvements, none blocking the three drafts. |
| `BLOG-x402-on-moi.md` | Draft announcement post for blog.moi.technology. Readable, not publishable yet. Front matter is `draft: true` on purpose. |

`docs/PR-1-chain-id-edits.md` is not a pull request. It is a list of replacement text to apply to PR 1 once the network-ID decision is made. Do not file it.

The `.docx` and `.pdf` copies in `docs/` are exports of the markdown files of the same name. The markdown is the source. If you edit a markdown file, the exports are out of date until someone regenerates them.

## Status as of 13 October 2026

Nothing has been filed. No pull request, issue or discussion exists upstream for any of the three drafts.

Blockers, in the order they bite:

1. **Reference-format decision.** `moi:devnet`, `moi:112` or `moi:14`. Owner: protocol team and Rahul. See C1 below.
2. **Network-ID RPC from the protocol team.** CAIP-2 needs a real JSON-RPC call that tells a client which network a node is on, and PR 1's Resolution Mechanics section is still "To be completed" without it. No merged namespace has been filed without one. Owner: protocol team (Rahul).
3. **Filing order.** CASA merges first, then the spec, then the package. The repositories enforce this. The spec may be opened while CASA is in review, but it will not merge first.
4. **Live round trip not recorded.** The package's pay, prove, settle test has been written and skips without credentials. It was last recorded as never run against a live network. It needs a funded devnet wallet on moipod v0.13.0, then `pnpm test:integration` with `CLIENT_MOI_MNEMONIC` and `SERVER_MOI_ADDRESS` set. The new KMOI asset ID and fuel pricing may need fixes once it runs.
5. **Blog approval not recorded.** There is no record that anyone approved the post. Keep `draft: true` until someone does, and until the three pieces it describes are filed.

Also open, from `skills/moi/moi-standards-submission/SKILL.md`: the upstream pull request templates ask for an AI-assistance disclosure, and the drafts include one, but that conflicts with the house rule against Claude attribution. Rahul decides how the disclosure is worded.

Also decide who takes over as the named CASA author. PR 1's front matter and checklist name Adithya Ganesh (@sarvalabs-adithya) as the person who answers CASA's comments and watches the `discussions-to` URL. He leaves on 14 October 2026. Ask Rahul who replaces him before PR 1 is opened, and update the `author` field and the PR description.

## Who decides

| Person or group | Role |
|---|---|
| Adithya (DevRel) | Drafted the package and is the named CASA author in the drafts. Leaves 14 October 2026. |
| Rahul | Internal review of all three drafts, and owner of the network-ID decision (reference format, RPC method, result field). Also the default owner of every "decide before filing" item below unless a row says otherwise. |
| Gokul | Code review of the package. Also asked whether `XBIND` to a logic's own identifier is an intended, stable rule (ESCROW note, next steps). |
| Protocol team (Sarva Labs) | Ships the network-ID RPC and settles protocol facts the drafts depend on. |
| CASA maintainers | Approve PR 1 upstream. |
| x402 maintainers | Approve PR 2 and PR 3 upstream. |

## Reading order

1. This README.
2. `docs/PR-2-x402-scheme-spec.md`, the clearest of the three: it defines the flow and the eight rules everything else follows.
3. `BLOG-x402-on-moi.md`, the plain-language version of the same story, with a glossary.
4. `docs/PR-1-CASA-namespace.md`, then `docs/PR-1-chain-id-edits.md` for how it changes if the reference becomes numeric.
5. `docs/PR-3-x402-moi-package.md`. It is large (over 3,000 lines, mostly source listings). Read the Page 1 summary and the PR description, then the sections you need.
6. `AUDIT-2026-09-10.md` for what was checked and how.
7. `ESCROW-RESEARCH-2026-09-10.md` and `FUTURE.md` when you start on follow-ups.

## What is posted and what is internal

Each PR draft is a review document, not the text to file. Only part of it goes upstream. The rest is for internal review and must be stripped before filing.

Posted upstream: the PR description body, and the content of each file the PR adds or changes (the namespace files, the spec file, the package files and the small edits to existing e2e and example files).

Internal, strip before filing:

- The "Page 1" block at the top of each draft (what the PR is, requirements, status, index).
- Every "Context" blockquote under a section heading.
- The checklists in each PR description (author, `discussions-to`, internal review, AI disclosure and the like). Keep only what the upstream repository's own template asks for.
- Status and "Open decisions" sections (PR 1 section 4).
- Verification records and revision history (PR 3 section 5, "Verified", "Second pass", "Third pass", "What the rebuild fixed").

Private source citations. The node, the VM and the compiler repositories are not public, and the upstream text must not cite them:

- PR 2: a Context note near line 490 says the node and VM repositories are private and cites go-moi source; the Status block (line 34) and a Context note near line 356 also name go-moi. All three are in internal blocks and go with them. Check that no go-moi citation survives into the posted spec text.
- PR 3: the "Claims checked against source" table and the notes around it (about lines 3048 to 3116) cite go-moi source and commit hashes. This is inside the verification record and must be removed before filing.

## Files referenced but not in this repo

The drafts point at files that live on the previous operator's machine and were never committed here:

- `escrow-poc/` (the proof-of-concept Coco escrow logic, `escrow-poc/escrow.coco`)
- `DECISIONS.md` (the open-decisions log PR 1 refers to)
- `E2E-REGISTRATION.md` (the three e2e registration edits for PR 3; PR 3 section 3 reproduces them)
- `EXAMPLES-ENTRIES.md` (the example-file entries for PR 3; PR 3 section 4 reproduces them)
- `STATUS.md` (the PR 3 verification record; PR 3 section 5 reproduces it)
- `../../moi-x402/` (the earlier draft of the package that was rebuilt)
- The "walkthrough artifact" (AUDIT) and the "briefing artifact" (ESCROW note)

The templates for a decisions log, the PR descriptions and the review-package index are in `skills/moi/moi-standards-submission/templates/` in this repository, and that skill describes the method and the filing mechanics. Start with its `SKILL.md`.

## Decide before filing

The drafts contradict each other, or depend on facts that are not settled, in the places below. These are technical decisions for the protocol team and Rahul, not wording fixes, so the drafts were deliberately left as they are. Settle each one, then make every file agree.

| ID | Question | Where it shows up | Owner |
|---|---|---|---|
| C1 | Reference format: `moi:devnet` (name), `moi:112` (numeric network ID the node holds and the SDK `Chain` enum carries) or `moi:14` (what MOI Wallet and `wallet-connect-dapp` use for devnet) | PR 1, PR 2, PR 3 (`constants.ts`), BLOG, `PR-1-chain-id-edits.md`, FUTURE row 6. About six files change together. | Protocol team / Rahul |
| C2 | Mainnet listing: PR 1 reserves `moi:mainnet` in the well-known networks table; PR 2, PR 3 and the edits file list only the devnet | PR 1 table, `PR-1-chain-id-edits.md` (decision 4), PR 2 Supported Networks, BLOG | Protocol team / Rahul |
| C3 | Genesis wording: PR 1 says MOI has no chain-wide genesis block or artefact; the edits file (correction of 14 September) says there is one genesis tesseract shared by the founding accounts | PR 1 README and caip2 text, `PR-1-chain-id-edits.md` last section | Protocol team / Rahul |
| C4 | The RPC method and result field for the network ID: the edits file uses `net.ChainId` and `chain_id` as placeholders, while PR 1 records that `net.ChainId` returned method-not-found on 10 September | `PR-1-chain-id-edits.md` Resolution Mechanics, PR 1 section 4 | Protocol team |
| C9 | Reason codes: the `moi_exact_*` vocabulary is defined in PR 3 and the post, but PR 2 says `errorReason` is free-form and does not list the codes. Decide whether the spec names them | PR 2 rules section and `PAYMENT-RESPONSE`, PR 3 README table, BLOG rule table | Rahul (spec owner) |
| C10 | `assetTransferMethod`: PR 2 says the key is absent and the scheme declares the SDK's `"default"`; PR 3 sets `defaultAssetTransferMethod = "default"` and notes core strips the key | PR 2 `PaymentRequirements` field list, PR 3 server scheme and verification record | Rahul / Gokul |
| C11 | Fee-payer status: PR 2 still says to re-check the wire once moipod v0.13.0 is live; the post says the fee payer shipped; FUTURE row 2 says it is live on devnet | PR 2 Status, PR 3 "Before filing" step 5, BLOG, FUTURE | Protocol team |
| C12 | Fee-payer field name: `fee_payer` (v0.13.0) against `payer` (before it); js-moi-sdk 0.9.0-rc2 still sends `payer` | PR 2 Appendix and Status, PR 3 verification record | Protocol team |
| C13 | KMOI asset ID: the old ID (`0x108000004cd973c4...`) against the new one that moves KMOI to MASN (`0x1080fffe4cd9...`), and which one each example and default uses | PR 2 anatomy example, PR 3 `MOI_ASSET_ID` and e2e catalog, BLOG | Rahul |
| C14 | Environment variable names: the post uses `MOI_MNEMONIC` and `SELLER_ID`; PR 3 uses `CLIENT_MOI_MNEMONIC`, `SERVER_MOI_ADDRESS`, `MOI_RPC_URL` and `MOI_ASSET_ID` | BLOG code samples, PR 3 integration test, examples and e2e registration | Rahul |
| C15 | Participant identifier layout: PR 1 lists four parts (tag, flags, 24-byte fingerprint, variant); PR 2 lists the two extra standard bytes. The layout is 32 bytes: tag 1, flags 1, standard 2, fingerprint 24, variant 4 | PR 1 README Rationale, PR 2 Appendix, PR 3 verification record | Protocol team |

The IDs are labels only; the numbers are not contiguous.

Placeholders to fill or delete before filing:

- PR 1, line 179: `discussions-to` is `.../pull/TODO`. It becomes the real PR URL once opened (or another monitored URL).
- PR 1, line 428: the same `pull/TODO` in the open-decisions text (internal, goes with the section).
- PR 1, line 254: Resolution Mechanics reads "To be completed". It cannot be written until the network-ID RPC exists.
- PR 2, line 83: `ChainAgnostic/namespaces#TODO` in the PR description. It becomes the real CASA PR number.

## Glossary

**x402**: an open standard that puts a payment inside an HTTP 402 (Payment Required) response. A client that gets 402 pays, retries with proof, and receives the resource. No account, API key or card.

**Facilitator**: the x402 component that checks (and, on some chains, submits) a payment on the seller's behalf. On MOI's `upfront` flow it only reads from the network and holds no keys.

**Scheme**: one way of paying under x402 on a given network. The one here is `exact`, a fixed price per request.

**Upfront, authorization and escrow flows**: the three x402 v2 payment flows. `authorization`: verify, serve, then settle, using a signed authorization from the buyer (most chains). `upfront`: the buyer settles first and proves it with a signed claim (the MOI scheme here). `escrow`: funds are held, then released.

**CAIP**: Chain Agnostic Improvement Proposal, a standard published by CASA.

**CASA**: the Chain Agnostic Standards Alliance. It maintains the CAIPs and the `ChainAgnostic/namespaces` repository where each chain registers a namespace.

**CAIP-2**: the chain identifier format `namespace:reference`, for example `eip155:8453`. x402 v2 names every network this way.

**CAIP-10**: the account identifier format. CAIP-19: the asset identifier format. The `moi` namespace profiles neither yet; they may be added later.

**CAIP-104**: the document format for a namespace profile (the `README.md` in `namespaces/moi/`).

**Network ID**: the number that identifies a MOI network. The SDK carries it as the `Chain` enum (devnet 112, test net 111, main net 113); the node does not yet report it over RPC. It is the candidate for the CAIP-2 reference (C1). External field and enum names (`chain_id`, `net.ChainId`, `Chain`) keep their own spelling.

**Voyage devnet**: MOI's public development network and the only live public network as of 10 September 2026.

**KMOI**: the native token of MOI. It pays fuel and, in these drafts, the quoted price. It has nine decimals. From moipod v0.13.0 it runs on the MASN standard.

**MAS0**: MOI's native fungible asset standard for developer tokens. A MAS0 asset is created by a protocol operation, not deployed as contract bytecode.

**MASN**: the native asset standard KMOI moves to in v0.13.0.

**Participant**: the unit MOI is built around. Each participant (a buyer, a seller or an agent) holds its own state and its own ordered sequence of tesseracts. MOI is participant-centric: there is no single global chain of blocks.

**Interaction**: MOI's transaction. A signed envelope holding one or more operations, such as an `ASSET_INVOKE` that calls `Transfer` on an asset.

**Fuel**: what an interaction costs to run, paid in KMOI. A fee payer (from moipod v0.13.0) can co-sign and pay it for the sender.

**Logic**: a program deployed on MOI that holds its own state and has its own account, the nearest MOI equivalent of a smart contract.

**Coco**: the language logics are written in. A Coco escrow logic is the proposed way to hold a deposit and release it by code (see the ESCROW note).

**PISA**: the virtual machine that runs logics. Its source (go-pisa) is private.

**Tesseract**: a per-participant state checkpoint. There is no chain-wide height. Each tesseract carries a timestamp.

**moipod**: the MOI node release. v0.13.0 introduced the fee payer and moved KMOI to MASN.

**core**: `@x402/core`, the x402 TypeScript library that drives the HTTP exchange around the client, server and facilitator halves of a package.

**anu**: the smallest unit of an asset. With nine decimals, 0.10 KMOI is 100,000,000 anu. Quantities in the scheme are always in anu.

**Sub-account**: a further participant identifier derived from the same public key and told apart by the variant field. The scheme does not support sub-accounts paying yet.

**EIP-3009**: the Ethereum standard for a token transfer authorized by a signed message and submitted by someone else. It is what the `authorization` flow looks like on EVM chains, and why MOI's `upfront` flow differs.
