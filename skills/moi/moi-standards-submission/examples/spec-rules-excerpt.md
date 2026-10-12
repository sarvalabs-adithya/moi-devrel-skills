# Settlement rules: the form

Two of the eight MUST rules of the draft `scheme_exact_moi.md`. Each rule says what must hold, why it exists and what a later version may change. Every rule is testable.

### 3. Key controls payer

The participant identifier derived from `publicKey` MUST equal `claim.from`. A valid signature
alone could still merely claim someone else's transfer; this rule defeats a lifted hash.

Because the identifier derives from one key, the claim MUST be signed with that key (`keyId`
`0`). Accepting the account's other keys would require checking `publicKey` against the
account's registered keys on chain instead of deriving; a later version MAY add that. The
derivation uses variant `0`, so a sub-account identifier (non-zero variant) fails this rule; a
later version MAY derive with the variant the claim names.

### 8. Replay

`claim.txHash` MUST NOT have been redeemed before. On success the facilitator MUST record it in
a spent-store before returning. The spent-store is the replay boundary and MUST be durable
across process restarts in production.

The transfer hash, not the `nonce`, is what makes a payment single-use: one settled transfer can
be redeemed once. The `nonce` exists so that two claims over the same transfer are distinguishable
as messages, and facilitators MAY ignore it.
