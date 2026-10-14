> **Not a pull request:** a list of edits to apply to PR-1 once the network-ID decision is made. Do not file.
> For status and a glossary of the terms used here, see the folder README (`../README.md`).

# PR 1 review doc: edits for the numeric network-ID reference

Copy-paste replacements, 14 September 2026. Devnet's network ID is 112 (the value the SDK's
`Chain` enum carries; the node config agrees). The RPC method name and result field are
placeholders until the protocol team's network-ID PR lands.

## Section 3, caip2.md

### Introduction, second paragraph

A consequence of that design is that MOI has no chain-wide genesis block, and so no genesis hash of the kind other namespaces use as a reference. Networks are instead distinguished by a numeric network ID, which every node reports over JSON-RPC, in the manner of the eip155 and neo namespaces.

### Semantics

The namespace is moi. The reference is the network ID of a MOI network: an unsigned integer that every node of that network reports, written in canonical decimal form. Two nodes that report the same network ID belong to the same CAIP-2 chain by definition.

### Syntax

The reference is the network ID in unsigned decimal form, between 1 and 10 digits, with no leading zeroes:

```
^(0|[1-9][0-9]{0,9})$
```

The parsed value MUST additionally be in the unsigned 32-bit integer range, 0 through 4294967295 inclusive. The regular expression alone does not enforce the upper bound. The reference MUST NOT carry a sign, a base prefix, digit separators, surrounding whitespace or leading zeroes. The value zero is written as 0.

### Well-known networks

Delete "To be completed". Table header "Reference" becomes "Network ID"; the devnet row becomes:

| Network | Network ID | CAIP-2 identifier | Status |
| --- | --- | --- | --- |
| MOI devnet | 112 | moi:112 | live |

Under the table:

This table is informative; the resolution method below remains authoritative. At the time of writing, the MOI devnet is the only live public MOI network. Further public networks are added to this table as they launch.

### Resolution Mechanics (whole section)

To resolve the network ID reported by a MOI JSON-RPC endpoint, call the net.ChainId method with no parameters:

```
{"jsonrpc": "2.0", "id": 1, "method": "net.ChainId", "params": []}
```

The response carries the network ID as an unsigned integer. The following is the response from a devnet node:

```
{"jsonrpc": "2.0", "id": 1, "result": {"chain_id": 112}}
```

Serialize the returned value in canonical unsigned decimal form and prefix it with moi:. The example response therefore resolves to moi:112. A client MUST treat a mismatch between the expected and the reported reference as an error and MUST NOT submit interactions to a node it cannot identify.

[Method name and result field are placeholders until the protocol team's network-ID PR lands. The rule above does not change. Remove this line before filing.]

### Rationale (whole section)

Every MOI network carries a numeric network ID. It is the value the client SDK exposes as its Chain enum, 112 for the devnet, and the value a node reports over JSON-RPC, so a client can both construct a reference and verify it against the node it is talking to. That is the convention eip155 and neo use, and it needs no registry and no transformation.

Two alternatives were considered. A genesis hash, as solana uses, has no clean equivalent: tesseracts are per-account, so the nearest artefact is the first tesseract of a genesis-era account, which would tie the identifier to an implementation detail. A short network name, as stellar uses, is human-legible but is not something a node reports; a client could construct one but never check it.

Decimal encoding matches the JSON-RPC representation and leaves one textual form for each value, ruling out hexadecimal, signed or zero-padded spellings of the same id.

### Backwards Compatibility

Unchanged.

### Test Cases

Valid:

```
# MOI devnet
moi:112

# Single-digit reference
moi:1

# Upper bound of the range
moi:4294967295
```

Invalid:

```
moi:                 # empty reference
moi:devnet           # a name, not a network ID
moi:0112             # leading zero
moi:-112             # signed value
moi:+112             # explicit sign
moi:0x70             # hexadecimal
moi:1 12             # whitespace
moi:1_12             # digit separator
moi:4294967296       # above the 32-bit maximum
MOI:112              # uppercase namespace
```

### Security Considerations (whole section)

Resolving a network ID through JSON-RPC only establishes what the queried endpoint reports. It does not authenticate that endpoint. Clients SHOULD authenticate their RPC endpoint and SHOULD NOT infer a network from an unverified URL.

MOI participant identifiers are derived from the account's public key rather than allocated by a network, so the same identifier exists on every MOI network. A client that submits an interaction to the wrong network may therefore find that it succeeds. Clients SHOULD resolve and check the network ID of an endpoint before signing or submitting an interaction.

### References

Delete the line "Context. CAIP-2, CAIP-104 and public MOI links only." The five links stay.

## Everywhere else in the doc

- Page 1, "Why it exists": `(moi:devnet)` becomes `(moi:112)`.
- Page 1, Status, third bullet, replace with: "Decided: the reference is the numeric network ID, moi:112 for the devnet. The same string replaces moi:devnet in the scheme spec (PR 2) and in constants.ts of the package (PR 3)."
- Page 1, Status, last bullet: "As of 14 September 2026, MOI Wallet uses moi:14; it must move to moi:112 before filing."
- Section 1, PR description, second sentence: "Because there is no chain-wide genesis artefact, the CAIP-2 reference is the numeric network ID that each node reports over JSON-RPC, in the manner of eip155 and neo."
- Section 2, README intro, last sentence of paragraph 2: "…which is why the CAIP-2 profile uses the numeric network ID that each node reports rather than a genesis hash."
- Section 2, README Rationale, paragraph 2, replace the last two sentences (from "The protocol also exposes no network ID on the wire…" to "…stellar namespace.") with: "Each MOI network carries a numeric network ID, the value the client SDK exposes as its Chain enum and that a node reports over JSON-RPC. A genesis hash, as solana uses, has no equivalent, so the CAIP-2 profile uses the network ID in canonical decimal form, in the manner of the eip155 and neo namespaces."
- Section 2, README References: delete "Context. Only public artefacts. A reviewer can open every link."
- Section 4, opening paragraph: "Of the four items recorded on 10 September, the reference format and the mainnet listing are decided. Resolution Mechanics still waits on the RPC; discussions-to is filled in when the PR opens."
- Section 4, decision 1: retitle "The reference format: decided (Option B)" and replace the body with: "The reference is the network ID, moi:112 for the devnet. The changes in the table are applied in section 3 and carry to PR 2 and constants.ts in PR 3." Keep the table as the record of what changed.
- Section 4, decision 4, second paragraph: "Decided: list only the devnet; add further networks when they launch."
- Section 4, "What is not undecided": "Test cases cover three valid and ten invalid identifiers, each with a reason."

## Comments to update

- Semantics: "Context. What the two halves of moi:<reference> mean. The reference is the numeric network ID, the value the node reports and the SDK's Chain enum already carries."
- Syntax: "Context. The regex is the normative rule; the prose restates it. Modelled on the neo profile: canonical decimal, no sign or prefix, 32-bit bound."
- Well-known networks: "Context. Only devnet is live. The table is informative; resolution is authoritative. Further networks are added when they launch."
- Resolution Mechanics: "Context. BLOCKING. Written against the network-identity RPC the protocol team is adding; method name and result field are placeholders until that PR lands. Every merged namespace has a real call here."
- Rationale: "Context. Why the network ID was chosen over a genesis hash or a name, and why decimal."
- Test Cases: "Context. Three valid and ten invalid identifiers, each with a reason, modelled on neo."
- Security Considerations (new): "Context. The MOI-specific point: identifiers derive from keys, so the same identifier exists on 112 and every other network. This is why PR 2 puts the network in the signed claim."

## To confirm with Rahul

1. The RPC method name and the result field.
2. That the devnet reports 112.
3. The integer type of the id, which decides the 32-bit bound in Syntax.
4. MOI Wallet's `moi:14`.

## Correction, 14 September: MOI does have a genesis tesseract

Source and live devnet both show one genesis tesseract, created once from the genesis file
with every founding account as a participant (view 0, timestamp 0, interactions hash =
blake2b-256("Genesis_ixns"), no seal). Tesseract 0 of every founding account is that same
tesseract; on devnet its hash is 0x4529116966dd8c85624177c04345c4d084ebbf9994ea68e98bbcb1ccf58bc1a0
for the KMOI asset account and three other founding accounts alike. What MOI does not have is
a chain of blocks: tesseracts are per account, there is no global height, and the genesis
tesseract is reachable only by naming a founding account. Its hash also changes whenever a
network is re-initialised (devnet was reset for v0.13.0); the network ID does not.

Replace the "no genesis block" sentences:

- caip2 Introduction, paragraph 2: "A consequence of that design is that MOI has no chain of blocks and no global height. Its genesis is a single tesseract shared by the founding accounts, reachable only by naming one of them, and re-created whenever a network is initialised. Networks are therefore distinguished by a numeric network ID, which every node reports over JSON-RPC, in the manner of the eip155 and neo namespaces."
- caip2 Rationale, paragraph 2, first sentence: "A genesis hash, as solana uses, exists but is a poor fit: the genesis tesseract can only be fetched by naming a founding account, its hash is 32 bytes where a CAIP-2 reference allows 32 characters, and it changes whenever a network is re-initialised, which the network ID survives."
- README intro, paragraph 2, last sentence: "Consequently there is no chain-wide block height, and the genesis tesseract is reachable only through the founding accounts it seeds, which is why the CAIP-2 profile uses the numeric network ID that each node reports."
- README Rationale, paragraph 2: replace "Because tesseracts are per-account, there is no chain-wide genesis block to hash." with "Because tesseracts are per-account, there is no chain-wide height; the genesis is a single tesseract seeding the founding accounts, addressable only through one of them."
- PR description, sentence 2: "Because MOI has no chain of blocks and its genesis tesseract is addressable only through a founding account, the CAIP-2 reference is the numeric network ID that each node reports over JSON-RPC, in the manner of eip155 and neo."
- Section 4, "Verified while checking these", paragraph 2: "The rationale previously claimed no genesis artefact exists. Wrong: there is one genesis tesseract, and tesseract 0 of every founding account is that tesseract (identical hash for four founding accounts on devnet). It is retrievable only by naming a founding account and changes on every network reset, which is why the network ID is the better reference. Corrected."
