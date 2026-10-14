# PR 1: `moi` namespace for the Chain Agnostic Standards Alliance

*Review document, 10 September 2026. Prepared for internal review before filing.*

## Page 1: what this PR is

**Target repository:** `ChainAgnostic/namespaces` (public). New directory `namespaces/moi/` with two files.

**PR title:** Add `moi` namespace (CAIP-104 profile + CAIP-2 chains profile)

**Why it exists:** x402 v2 names networks by CAIP-2 identifier (`moi:devnet`). Nothing can use that string with confidence until the `moi` namespace is registered with CASA. This PR is filed first; the scheme spec (PR 2) and the package (PR 3) reference it and wait for it.

### High-level requirements

CASA's `_template/` defines both files. Modelled on the accepted `stellar`, `aptos` and `neo` profiles.

| File | Purpose | Required sections |
|---|---|---|
| `namespaces/moi/README.md` | CAIP-104 namespace profile: what `moi` covers and who maintains it | YAML frontmatter (`namespace-identifier`, `title`, `author`, `status`, `type`, `created`, `requires`); introduction; Rationale; Governance; References; Copyright (CC0) |
| `namespaces/moi/caip2.md` | CAIP-2 chains profile: how a MOI network is identified | YAML frontmatter (adds `discussions-to`); Introduction; Specification with Semantics, Syntax, Well-known networks, Resolution Mechanics; Rationale; Backwards Compatibility; Test Cases (valid and invalid); Security Considerations; References; Copyright |

### Status

- Both files drafted and self-consistent; syntax regex, test cases and rationale corrected on 10 September.
- **Blocking:** Resolution Mechanics needs the network-identity RPC the protocol team is adding. No merged namespace has filed without one.
- **Blocking, same dependency:** the reference format. As of 10 September 2026 the reference is a name (`moi:devnet`); if the RPC exposes a stable numeric network ID, the reference becomes numeric (`moi:112`) and the changes listed in `DECISIONS.md` apply to this PR, to PR 2 and to `constants.ts` in PR 3.
- `discussions-to` is the PR's own URL, filled in once opened. Whoever owns it must watch it.
- As of 10 September 2026, MOI Wallet uses `moi:14`; the namespace must reconcile with the wallet before filing.

### Index

1. PR description (as it will be posted)
2. File: `namespaces/moi/README.md`, with context notes per section
3. File: `namespaces/moi/caip2.md`, with context notes per section
4. Open decisions (from `DECISIONS.md`)


---

## 1. PR description

### PR description: ChainAgnostic/namespaces

**Title:** Add `moi` namespace (CAIP-104 profile + CAIP-2 chains profile)

This PR adds a namespace profile for MOI, a participant-centric protocol in which each participant
account holds its own state and tesseract sequence. Because there is no chain-wide genesis
artefact, the CAIP-2 reference is a short network name (pending: the protocol team is adding a
network-ID RPC, and the reference format will be confirmed against it before this PR is opened).

Files follow `_template/`, modelled on the accepted `stellar`, `aptos` and `neo` profiles.

- [x] `author`: Adithya Ganesh (@sarvalabs-adithya), who answers CASA's comments
- [ ] `discussions-to` URL created and monitored
- [ ] Reference format confirmed against the protocol network-ID PR
- [ ] Internal review (Rahul) complete

Drafted with AI assistance; reviewed by the listed author.


---

## 2. File: `namespaces/moi/README.md`

**Frontmatter** (YAML header CASA parses):

```yaml
namespace-identifier: moi
title: MOI Ecosystem
author: ["Adithya Ganesh (@sarvalabs-adithya)"]
status: Draft
type: Informational
created: 2026-08-08
requires: ["CAIP-2"]
```


### Namespace for MOI Chains

> **Context.** This is the CAIP-104 namespace profile, the file CASA reads first. It has to say what the namespace covers and, for MOI, explain the one structural difference (participant-centric, no global chain) that every later choice depends on.


The namespace `moi` refers to the wider MOI ecosystem, including public networks such as the
Voyage devnet and any private deployment of the MOI protocol.

MOI differs from account-balance chains in one way that matters when reading the rest of these
profiles: it is **participant-centric**. There is no single global chain of blocks. Each participant
account holds its own sequence of *tesseracts*, and an *interaction* is the signed unit that moves
state. Consequently there is no chain-wide genesis block whose hash could serve as a network
reference, which is why the CAIP-2 profile uses a named reference rather than a hash.

This namespace currently profiles CAIP-2 (chain identification). Profiles for other CAIPs, such
as CAIP-10 (accounts) and CAIP-19 (assets), may be added later.

#### Rationale

> **Context.** Why `moi` cannot reuse the two common reference conventions (`eip155` chain id, `solana` genesis hash) and why identifiers are not EVM-shaped. Corrected on 10 September: the old text claimed no genesis artefact exists at all, which was too strong.


Most namespaces in this registry describe chains that keep one global ledger: a single ordered
chain of blocks, a genesis hash, and often a numeric chain id. MOI has none of these, and the
identifiers in this namespace reflect that.

MOI is participant-centric. Each participant account carries its own state and its own ordered
sequence of tesseracts (per-account state checkpoints) rather than a position in one shared
chain. State changes travel as interactions, envelopes signed whole by the submitting account
(ECDSA over secp256k1). Because tesseracts are per-account, there is no chain-wide genesis block
to hash. The protocol also exposes no network ID on the wire: the client SDK defines a numeric
`Chain` enum, but no RPC method or interaction field reads or emits it. Neither of the two most
common CAIP-2 reference conventions (`eip155`'s chain id or `solana`'s genesis hash) is usable
today, so the CAIP-2 profile uses a short, well-known network name, in the manner of the
`stellar` namespace.

Identifiers are likewise not EVM-shaped. A participant identifier is 32 bytes: a tag byte naming
the identifier kind and version, a flags byte, a 24-byte fingerprint taken directly from the
account's compressed public key, and a variant field carrying the sub-account index. Because it
is derived from the key rather than allocated by a network, the same identifier can exist on
every MOI network, which makes explicit network identification more important rather than less,
and is what this namespace provides. Assets are also protocol-native: a MAS0 asset is created by a protocol operation rather
than deployed as contract bytecode, and is addressed by its own 32-byte identifier.

#### Governance

> **Context.** CASA asks who maintains the namespace and how changes are made. Public repos and the explorer are named; the private node repo is not mentioned. New network references need no profile change, which is why the CAIP-2 profile uses a syntax rule plus a well-known table.


The MOI protocol is designed and developed by [Sarva Labs](https://github.com/sarvalabs). The
reference client libraries, including
[js-moi-sdk](https://github.com/sarvalabs/js-moi-sdk), are maintained in public repositories
under that organization, where changes are proposed and reviewed as issues and pull requests. The public Voyage networks, their RPC endpoints and the
[Voyage explorer](https://voyage.moi.technology) are operated under the same stewardship, with
the MOI Foundation supporting the wider ecosystem.

This namespace profile is maintained by its listed authors. Questions, corrections and proposed
changes should be raised at the `discussions-to` URL carried in each profile, and changes to the
profile itself are made by pull request to `ChainAgnostic/namespaces`, following CASA's own
process.

New network references do not require changes to this profile: any reference that follows the
syntax in `caip2.md` is valid, and a new public network becomes *well-known* by being added to
the table there. References for retired networks remain syntactically valid so that historical
data can still name the network it settled on: the reference format deliberately keeps working
for a chain that no longer runs.

#### References

> **Context.** Only public artefacts. A reviewer can open every link.


- [MOI Protocol](https://moi.technology): protocol overview
- [MOI documentation](https://docs.moi.technology): protocol fundamentals (assets, logics, interactions)
- [Voyage Explorer](https://voyage.moi.technology): public network explorer
- [Sarva Labs on GitHub](https://github.com/sarvalabs): protocol and SDK repositories
- [js-moi-sdk](https://www.npmjs.com/package/js-moi-sdk): reference client library

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-10]: https://chainagnostic.org/CAIPs/caip-10
[CAIP-19]: https://chainagnostic.org/CAIPs/caip-19
[CAIP-104]: https://chainagnostic.org/CAIPs/caip-104

#### Copyright

> **Context.** CC0 waiver is mandatory for every file in the namespaces repo.


Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).


---

## 3. File: `namespaces/moi/caip2.md`

**Frontmatter** (YAML header CASA parses):

```yaml
namespace-identifier: moi-caip2
title: MOI - Blockchain ID Specification
author: ["Adithya Ganesh (@sarvalabs-adithya)"]
discussions-to: https://github.com/ChainAgnostic/namespaces/pull/TODO
status: Draft
type: Informational
created: 2026-08-08
requires: ["CAIP-2"]
```


### CAIP-2

> **Context.** The chains profile. It follows CASA's `_template/caip2.md` section for section. `type: Informational` comes from the template; Neo and Stellar merged with `Standard`, which is a judgement call recorded in DECISIONS.


*For context, see the [CAIP-2][] specification.*

#### Introduction

> **Context.** One paragraph of context and the single sentence that matters to CASA: no chain-wide genesis, so the reference is a name, in the manner of `stellar`.


MOI is a participant-centric protocol.
Unlike chains that append blocks to one global ledger, each participant account on MOI holds its
own sequence of *tesseracts*, and state changes are carried by signed *interactions*.

A consequence of that design is that MOI has no chain-wide genesis block, and so no genesis hash
of the kind other namespaces use as a reference.
Networks are instead distinguished by name, in the manner of the [`stellar`][stellar-caip2]
namespace.

#### Specification

##### Semantics

> **Context.** What the two halves of `moi:<reference>` mean. This is the paragraph that changes if the protocol team decides on a numeric network ID (Option B in DECISIONS).


The `namespace` is `moi`.
The `reference` is the short, lowercase name of a MOI network.

##### Syntax

> **Context.** The regex is the normative rule; the prose restates it. It was fixed on 10 September: the previous version accepted a trailing hyphen that the prose and test cases forbade.


The reference is a lowercase alphanumeric string, optionally containing hyphens, between 1 and 32
characters:

```
^[a-z0-9]([a-z0-9-]{0,30}[a-z0-9])?$
```

The reference MUST NOT begin or end with a hyphen and MUST NOT contain uppercase characters,
whitespace, or separators other than `-`.

###### Well-known networks

> **Context.** Only devnet is live. `mainnet` is reserved so tooling can prepare and MUST NOT be treated as resolvable. Listing it before launch is the second judgement call; dropping the row is the alternative.


| Network | Reference | CAIP-2 identifier | Status |
| --- | --- | --- | --- |
| Voyage devnet | `devnet` | `moi:devnet` | live |
| MOI mainnet | `mainnet` | `moi:mainnet` | reserved; not yet launched |

At the time of writing, the Voyage devnet is the only live public MOI network. The `mainnet`
reference is reserved here so that tooling can prepare for it, and MUST NOT be treated as
resolvable until that network launches.

Private deployments SHOULD choose a reference that is unlikely to collide with the names above.

##### Resolution Mechanics

> **Context.** BLOCKING. CAIP-2 requires a real RPC call that tells a client which network a node is on, and every merged namespace has one. MOI had no such method as of 10 September 2026. The section states the requirement and will be written against the network-identity RPC the protocol team is adding (Rahul: network-ID PR in progress).


*To be completed.* This section requires a JSON-RPC method that reports which network a node
belongs to, shown as a request and its response, and the rule for turning that value into the
reference.

MOI exposes no such method today. Its RPC surface is 42 methods across `moi.*`, `ixpool.*` and
`net.*`; `net.Version` returns the node's software version, `net.Info` its own peer identifier,
and `moi.Tesseract` requires an account identifier. A network-identity method is planned, and
this section will be written against it.

#### Rationale

> **Context.** Explains why a name was chosen over a numeric network ID or a genesis hash, and commits to reconsidering if the planned RPC exposes a stable numeric id. Every knock-on change for a numeric reference is listed in DECISIONS.


MOI has no stable, RPC-readable network identifier today, so the reference is a short network
name pending one.

A numeric chain id, as `eip155` uses, is not available on the wire: the client SDK carries an
unused `Chain` enum, but no RPC method or interaction field reads or emits it. A genesis hash, as
`solana` uses, has no clean equivalent: tesseracts are per-account, so the nearest artefact is the
first tesseract of a genesis-era account, which would tie the identifier to an implementation
detail.

A name is human-legible, stable across protocol upgrades, and lets a client construct an
identifier without fetching anything, only verify one. If the planned network-identity method
exposes a stable numeric id, a numeric reference becomes available and this choice should be
reconsidered before the profile leaves Draft.

##### Backwards Compatibility

> **Context.** Template requires the section even when not applicable.


Not applicable. No prior CAIP-2 profile exists for MOI.

#### Test Cases

> **Context.** Four valid and eight invalid identifiers, each with a reason. Stronger than the Stellar profile this was modelled on. If Option B (numeric) is chosen, every example is rewritten.


##### Valid

```
# Voyage devnet
moi:devnet

# The reserved mainnet reference
moi:mainnet

# A private deployment
moi:acme-internal

# Minimum-length reference
moi:x
```

##### Invalid

```
moi:                 # empty reference
moi:DevNet           # uppercase characters
moi:dev net          # whitespace
moi:-devnet          # leading hyphen
moi:devnet-          # trailing hyphen
moi:dev_net          # underscore is not permitted
MOI:devnet           # uppercase namespace
moi:this-reference-is-far-too-long-to-be-valid   # exceeds 32 characters
```

#### Security Considerations

> **Context.** The point specific to MOI: participant identifiers derive from keys, not from a network, so the same identifier exists on every MOI network. This is why explicit network identification matters, and why PR 2 puts the network inside the signed claim.


A network reference is only as trustworthy as the endpoint reporting it.
Clients SHOULD authenticate their RPC endpoint and SHOULD NOT infer a network from an unverified
URL. Because MOI participant identifiers are derived from public keys rather than allocated per
network, the same identifier may exist on more than one MOI network, so a client that submits an
interaction to the wrong network may find it succeeds.

#### References

> **Context.** CAIP-2, CAIP-104 and public MOI links only.


- [CAIP-2][]: Blockchain ID Specification
- [CAIP-104][]: Chain Agnostic Namespaces
- [MOI Protocol](https://moi.technology)
- [Voyage Explorer](https://voyage.moi.technology)
- [js-moi-sdk](https://www.npmjs.com/package/js-moi-sdk)

[CAIP-2]: https://chainagnostic.org/CAIPs/caip-2
[CAIP-104]: https://chainagnostic.org/CAIPs/caip-104
[stellar-caip2]: https://namespaces.chainagnostic.org/stellar/caip2

#### Copyright

> **Context.** CC0, as CASA requires.


Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).


---

## 4. Open decisions

### Open decisions: PR 1

Four items are undecided. Two block the PR (items 1 and 2, the second depending on the first), one has no dependency and can be closed at any time (item 3), and one groups two judgement calls (item 4).
Each says who decides and exactly what changes.

---

#### 1. The reference format: BLOCKING

**Decides:** protocol team / Rahul.

The reference half of `moi:<reference>` is currently a network name (`moi:devnet`). The client SDK
also carries `enum Chain { TEST_NET = 111, DEV_NET = 112, MAIN_NET = 113 }`, unused as of 10 September 2026, and the
planned network-identity RPC may surface exactly those numbers. If it does, a numeric reference
becomes available and every other registered chain that has a chain id uses one.

**Option A: keep names.** `moi:devnet`, `moi:mainnet`. Human-legible, matches `stellar:pubnet`.
Nothing in the document changes.

**Option B: use the network ID.** `moi:112` for devnet. Matches `eip155` and `neo`. Changes:

| Section | Change |
| --- | --- |
| Semantics | reference becomes the network ID, not its name |
| Syntax | regex becomes `^(0\|[1-9][0-9]{0,9})$`, plus a range bound; copy Neo's wording |
| Well-known networks | table keys on ids: devnet `112`, mainnet `113` |
| Resolution Mechanics | reads the id from the new RPC |
| Rationale | the "numeric chain id was rejected" paragraph inverts; the "short network name" paragraph becomes the rejected option |
| Test Cases | every example is rewritten; the hyphen and case cases stop being meaningful |

Roughly an hour of editing, mechanical once the choice is made.

**Knock-on outside this PR:** `moi:*` appears in the scheme spec (PR 2) and in
`src/constants.ts` of the mechanism package (PR 3). Both follow whatever is decided here.

---

#### 2. Resolution Mechanics: BLOCKING, same dependency

**Decides:** protocol team ships it; nobody can write around it.

CAIP-2 requires a section showing how a client confirms which network a node is on. Every merged
namespace has one backed by a real call: Neo `getversion` → `protocol.network`, Stellar Horizon
`/` → `network_passphrase`, Klever `/node/status`, Tenzro `tenzro_getBlock` at genesis. There is
no precedent for filing without one.

As of 10 September 2026 MOI has nothing equivalent. Re-probed that day: `net.Network`, `net.ChainId`,
`net.NetworkInfo`, `moi.Network`, `moi.ChainId`, `moi.NetworkInfo`, `net.Chain` and `moi.Chain`
all return method-not-found. Nothing existing substitutes: `net.Info` returns a per-node peer id,
`net.Version` the node's software version, and `KMOI_ASSET_ID` is a hardcoded SDK constant
identical on every network.

The section states what it requires and nothing more: a method reporting which network a node is
on, its request and response, and the rule for deriving the reference. Nothing is invented. When
the method lands, write it in.

One finding worth recording. `commit_info.cluster_id` is network-wide at the latest tesseract
(two unrelated accounts return the same value), but it differs at tesseract 0, so it tracks the
current validator cluster and rotates. A CAIP-2 reference has to be stable for the life of the
network, so it cannot be used.

---

#### 3. `discussions-to`: no dependency, can be closed at any time

**Decides:** Adithya.

Currently `https://github.com/ChainAgnostic/namespaces/pull/TODO`, the CASA PR's own URL, with
the number filled in once the PR is opened. That is the simplest route and needs nothing set up
beforehand.

It does not have to be the CASA PR, though. Neo points at `neo-project/proposals/issues/238` and
Stellar at a CAIP pull request, so any monitored URL is acceptable. An issue on a public MOI repo
would give CASA somewhere to send questions that outlives the PR thread, if that is wanted later.

Whoever owns that URL has to actually watch it. The only namespace PR that has ever failed on
merit failed because its author went quiet for 587 days.

---

#### 4. Two judgement calls

**`type:` in the frontmatter.** Ours says `Informational`, following CASA's own `_template`.
Neo and Stellar both say `Standard` and merged anyway. Leave as is unless a reviewer objects; the
template is the better authority.

**Listing `mainnet` before it exists.** The well-known-networks table reserves `moi:mainnet` and
says it MUST NOT be treated as resolvable. The alternative is to list only `devnet` and add
mainnet when it launches. Reserving it is defensible and tells tooling authors what is coming;
dropping it removes a row a reviewer might question. Neo avoids the problem entirely by defining a
rule rather than a table, which is also what Option B in decision 1 would give us.

---

#### Verified while checking these

`moi.Tesseract` refuses to answer without an account identifier, and `tesseract_number: 0`
returns a different tesseract per account. There is genuinely no global chain.

The rationale previously claimed no genesis artefact exists at all. That was too strong: a
genesis-era account's first tesseract carries `timestamp: 0x0` and an empty `cluster_id`, and its
hash is plausibly stable and network-unique. Using it would tie the identifier to an
implementation detail, which is a reason to prefer a name, but not the reason the document gave.
Corrected.

#### What is not undecided

The author is set: Adithya Ganesh (@sarvalabs-adithya). The syntax regex is fixed (it previously
accepted a trailing hyphen that the prose and test cases forbade). The frontmatter `title` follows
the template's `<name> - Blockchain ID Specification` form. Test cases cover four valid and eight
invalid identifiers, each with a reason, which is stronger than the profile this was modelled on.
