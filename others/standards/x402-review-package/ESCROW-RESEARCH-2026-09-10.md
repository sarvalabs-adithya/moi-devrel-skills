# Can MOI do code-enforced escrow without a custodian? (research note, 2026-09-10)

Question asked: is `upfront` definitely the only production-grade way to do x402 on MOI, and is
there a compromise that gets closer to Ethereum's trustless flows? This note records the answer
and the evidence. Private repos are referenced by repo-relative path only.

## Bottom line

1. **I was wrong earlier.** I told you a logic cannot move its own asset balance, so any escrow on
   MOI would be custodial. At source level that is false. PISA lets a logic bind *itself* as the
   origin of an extern call, and the asset engine then treats the logic's account as the
   sender of the transfer.
2. **Programmable escrow is expressible today.** A Coco logic can hold a buyer's deposit in its
   own account and release it to the seller by code. No third party holds a key. The
   proof-of-concept is in `escrow-poc/escrow.coco`; it compiles, and the `Release` endpoint emits
   `XBIND` with the logic as origin followed by `CALLX` into the asset's `Transfer`.
3. **What is proven and what is not.** Every gate between "buyer calls Release" and "seller's
   balance rises" is verified by reading go-pisa v0.8.0 and go-moi `origin/develop`. The path has
   not been executed on a node yet. cocolab cannot model it, and I did not submit anything to
   devnet (standing rule). A devnet run needs a funded wallet and your go-ahead.
4. **`upfront` stays the right first scheme.** It is one interaction, final on commit, nothing
   pending, and it is what the three PRs describe. Escrow moves from "custodial only" to
   "programmable, follow-up spec". Wording in `FUTURE.md`, the spec Summary, the PR 2
   description and the briefing artifact has been corrected.

## The mechanism

```
endpoint dynamic Release(amount U256):
    observe seller, kmoi <- Escrow.Logic.seller, Escrow.Logic.kmoi:
        memory A = KMOI(kmoi, Escrow)        # interface bound with Escrow as origin
        A.Transfer(beneficiary: seller, amount: amount)
```

`KMOI(kmoi, Escrow)` compiles to `LOGIC $4; XBIND $3 $5 $3 $4`. The second argument is the
identity that becomes the origin of every call made through `A`. Passing the logic's own
identifier is allowed by the runtime rule below, and from then on the asset's `Transfer` sees
the escrow logic as the account paying out.

## Gate-by-gate trace

| # | Gate | Where | What it requires | Result for the escrow logic |
|---|---|---|---|---|
| 1 | Who may become an extern origin | go-pisa `instructset.go` `opXBIND` (~2463) | "the logic itself or any participant, who has signed the transaction, can become the new origin" | The logic itself qualifies. No signature needed. |
| 2 | Access level of the new origin | go-moi `compute/pisa/compiler.go` 644-650; go-pisa `opCALLX` (~545) | A `dynamic` endpoint gives `Origin: AccessWrite`; `opCALLX` builds the extern action with `SetAccess(extern.Origin(), scope.access.Origin)` | Escrow enters the asset's action with write access (0 = MutateLock). |
| 3 | Who the asset engine treats as sender | go-pisa `opCALLM` (~445) | `sender = FindActor(action.Origin(), requiresWriteAsset)` | Origin is the escrow logic, so sender = escrow. |
| 4 | Access map handed to the asset engine | go-pisa `machine.go` `callAssetMethod` (160); go-moi `common/interaction.go` `IxOp.AccessList` | Interaction participants' lock types, plus the overrides from gate 2 | Escrow: write (gate 2). Seller: must be listed as a `MutateLock` participant of the Release interaction. |
| 5 | Transfer validation | go-moi `compute/asset_engine.go` `Transfer` (~498) → `compute/ixasset.go` `validateAssetTransfer` (~183) | amount ≥ 1; `hasMutateAccess(access, benefactor, beneficiary)`; beneficiary registered in Sarga; benefactor holds the balance. No check on the benefactor's account kind. | Passes when 4 holds and the deposit exists. |
| 6 | Can a logic account hold the deposit at all | go-moi `compute/ixlogicdeploy.go` 55 → `compute/manager.go` `addNewAccountsToSargaAccount` | A deployed logic's account is registered in Sarga at deploy time | Yes. The buyer's deposit is a plain `Transfer` with the logic id as beneficiary. |
| 7 | Does the seller have to sign the Release interaction | go-moi tip `ixpool/ixpool.go` `verifySignatures` (919-945) | Only the sender, the fee payer and *notary* participants are signature-checked | No. A non-notary `MutateLock` participant needs no signature. |
| 8 | Endpoint may call a write asset method | go-pisa `asset.go` `AllowedAccessLevel` | Asset `TRANSFER` needs `AccessWrite`; a `dynamic` endpoint supplies it | Passes. |

Gates 1, 2, 3 and 5 were each read in full; gates 4, 6 and 7 were confirmed on the tip of
`origin/develop` (`IxOp.AccessList` is unchanged there).

## What each interaction must contain

- **Deposit.** Buyer → `ASSET_INVOKE` `Transfer(beneficiary: <escrow logic id>, amount)`. Same
  shape the `@x402/moi` client already sends; the SDK adds the beneficiary as a participant.
- **Release.** Anyone → `LOGIC_INVOKE` `Release(amount)` with participants: the escrow logic
  (`MutateLock`, added by the SDK), the seller (`MutateLock`, added by the caller) and the KMOI
  asset (for the descriptor read). The seller does not sign. Fuel is the caller's, or a fee
  payer's from v0.13.0.
- **Refund (not in the PoC).** A `Refund` endpoint gated on a tesseract timestamp deadline,
  calling the same `A.Transfer` back to the buyer. Tesseract timestamps are deterministic
  (genesis + view × timeout), which is fine for a deadline.

## Trust model compared with Ethereum

| | Ethereum escrow contract | MOI escrow logic (this note) | MOI `Lockup`/`Release` |
|---|---|---|---|
| Who can release | Contract code | Logic code | The releaser account named at lock time |
| Third-party key required | No | No | Yes |
| Buyer refund path | Contract code | Logic code (to add) | None; no expiry exists |
| Extra interactions | 2 (deposit, release) | 2 | 2 |
| Exists today | Yes | Compiles; execution pending | Yes |

## A compiler bug found on the way

The first `Release` (a bare `A.Transfer(...)` statement, nothing after it) compiled to `XBIND`
and the call arguments but **no `CALLX`**: the transfer was silently deleted. Bisected across
18 variants and three optimizer levels:

| Form | `-O 0` | `-O 1` | `-O 2` (coco default) |
|---|---|---|---|
| Bare `A.Transfer(...)` in straight-line code | kept | kept | **dropped** |
| Same, with an `if ... throw` before it | | | kept |
| Same, followed by `A.BalanceOf(...)` into a return | | | kept |
| `mountain_trail.coco` reference (has branches) | | | kept |

The pass is one of the two that only run at level 2 (`replace_copied_destinations`,
`remove_disposable_instructions` in `pisa/codegen/src/function/optimize.rs`). It treats an
extern call with unused return registers as disposable. Self-origin is not the trigger:
`Sender` as origin drops the same way, and the reference example with `MountainTrail` as its
own origin keeps all four calls. Any Coco logic whose last statement in a straight run is an
asset transfer is affected. This should go to the Coco team independently of escrow.

## Why cocolab could not prove it

cocolab (`pisa/engine/src/engine/execute.rs`) assembles each run's asset store from registered
*user* actors only. Minting 1000 KMOI to the escrow logic raised circulating supply to 2000 but
`BalanceOf(escrow)` read 0, and `Release` ran with no transfer event. The lab has no way to
load a logic's balance, so its result says nothing either way. The user-to-user control test in
the same session behaved normally (mint 1000, transfer 20, balances 980/20).

## The rest of the sweep, in brief

The adversarial sweep (62 sonnet agents, prior to this trace) also found:

- `upfront` is production-safe as specified: settle first, prove second, nothing pending.
- **Authorization compromise:** `Approve(cap, expires_at)` + facilitator `TransferFrom`, with
  unilateral `Revoke`. Cap and expiry are enforced at consume time. Costs the buyer one grant
  interaction, then per-request pulls need no buyer signature. Closest thing to EIP-3009 without
  a relayed signed interaction.
- **Cancellation of a relayed interaction:** the buyer can burn the sequence number
  (`ErrSequenceIDTooLow`), so a held interaction is cancellable, though not by expiry.
- `settleOnCancel` in x402 core covers the seller-side abort after a before-handler settle.
- Two x402 spec citations produced by agents did not exist; they were discarded.

## Next steps

1. Devnet execution of `escrow-poc` (deploy, deposit 1000, `Release(400)`, read both balances).
   I will not submit interactions without your go-ahead; you or I can run it with a funded
   wallet in `.env`.
2. One question for Gokul: is `XBIND` to the logic's own identifier an intended, stable rule?
   The comment in go-pisa says so; confirming it protects a future scheme from a silent change.
   And one bug report for the Coco team: `-O 2` drops a no-return extern call (section above).
3. If both hold, a `scheme_exact_moi` escrow variant becomes a real follow-up rather than a
   custodial one.
