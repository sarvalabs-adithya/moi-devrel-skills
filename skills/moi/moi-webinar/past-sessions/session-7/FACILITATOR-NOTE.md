# "Can we still call it x402 without a facilitator?"

*Internal note for Rahul, following a call (the notes do not date it). Not for publication. In the public MOI-Webinars repo this file was kept out of git; it is stored in this handover repo.*

> **What this is:** an internal answer to the question "can we still call it x402 without a facilitator?". Rahul (Lenkala) is the MOI lead who sets direction for DevRel and reviews its public pieces. *x402* is an open standard for paying over HTTP 402 (Payment Required); in it, a *facilitator* is a third service that verifies a payment and settles it so the seller never touches a blockchain. MOI Builders is the developer webinar series DevRel runs.
>
> **Status:** an analysis of the x402 build as it stood at the time, and **superseded in part**. It treats session 7 as the x402 session. The later notes (TRANSCRIPT.md, the latest and canonical for session 7, and DEMO-PLAN.md) say the delivered session 7 was not x402 and should not be called that; x402 moved to session 9, "built once on a branch". So read the facilitator described here as that branch's work, and "session 7" in this file as the earlier plan. Section 5 also describes session 9 as escrow (hold and release); `skills/moi/moi-webinar/references/session-history.md` records the plan on file for session 9 as the x402 envelope with MOI settlement. Which is current is not settled in these notes.
>
> **Where the code is:** `packages/facilitator` and the other paths below are in https://github.com/moi-foundation/MOI-Webinars, not in this repo.
>
> **Other terms:** *MAS0* is MOI's native fungible-token standard. *EIP-3009* is an Ethereum token feature that lets a third party submit a transfer using the owner's off-chain signature. *Lockup / release* are MAS0's calls to set funds aside for a named beneficiary and for that beneficiary to pull them. *Devnet* is MOI's public test network.

**Short answer: we do have a facilitator. It's a real service, it implements the standard x402
facilitator API, and the seller talks to it using x402's own client library, unmodified.**

The thing we can't do on MOI is have it *hold* the money. That's a smaller difference than it
sounds, and it's worth being precise about where the line actually falls.

---

## 1. What a facilitator is, per the spec

In x402 the facilitator is a **third service** that the resource server delegates to, so the server
never has to touch a blockchain. It exposes two endpoints:

```
POST /verify   "is this payment authorization good?"
POST /settle   "make it final, and give me a receipt"
```

That's the role. It is defined by the **interface**, not by whether it custodies funds.

## 2. What we built

An Express (Node web server) service at `packages/facilitator`:

```
POST /verify     -> { isValid, invalidReason?, payer?, checks[] }
POST /settle     -> { success, transaction, network, payer }
GET  /supported  -> { kinds: [{ x402Version, scheme, network }] }
```

Request bodies are `{ x402Version, paymentPayload, paymentRequirements }`, byte-identical to what
x402 sends.

**The strongest evidence it's genuinely x402:** the seller does not hand-roll those HTTP calls. It
imports x402's own facilitator client and points it at us:

```ts
import { useFacilitator } from "x402/verify";
const facilitator = useFacilitator({ url: config.facilitatorUrl });
await facilitator.verify(payload, requirements);
await facilitator.settle(payload, requirements);
```

That is upstream code, unmodified, talking to our service and getting valid responses. If our
service weren't a conforming facilitator, that call would fail.

## 3. Where we genuinely differ

On EVM chains, the facilitator can **pull** the buyer's funds. That works because of EIP-3009
(`transferWithAuthorization`): the *token contract itself* verifies an off-chain signature, so
someone else can submit the transfer on the buyer's behalf.

**MAS0 has no equivalent, and on MOI only the owner can move their own funds.** No amount of
engineering on our side changes that, it's a property of the asset standard.

So the flow inverts:

| | EVM x402 | Ours |
| --- | --- | --- |
| Who moves the money | the facilitator pulls it | the buyer sends it |
| What `/verify` does | checks the signature | checks the signature **+ reads the chain** |
| What `/settle` does | submits the transfer | **confirms** the transfer landed, marks the replay nonce as spent |
| Facilitator signs? | yes | **no, every check is read-only** |

Our facilitator is a **referee rather than a cashier**. It independently reads the interaction off
chain, decodes the transfer, and confirms sender, recipient, asset and amount match what was
signed, then marks that payment as spent (a replay is a second attempt to redeem the same payment) so it can't be redeemed twice.

## 4. So is it x402?

**The protocol: yes, unambiguously.** The 402 response, the `accepts[]` body, the base64
`X-Payment` header, the `X-Payment-Response` receipt, the facilitator API and its envelopes are all
the spec's. We reuse x402's own client. We changed nothing about the protocol.

**Two honest caveats, worth saying out loud rather than being caught on:**

1. **We define a new scheme.** x402 ships one scheme, `"exact"`, which is EVM/SVM-specific. We use
   `scheme: "moi-transfer"`, `network: "moi-voyage-devnet"`. The spec is built to carry multiple
   schemes, that field exists precisely so chains can add their own, but ours is not one the
   x402 Foundation has published. Wire-compatible ≠ officially registered.

2. **Two of the three reference npm packages don't work for any non-EVM/SVM chain.**
   `x402-express` throws `Unsupported network` at runtime; `x402-fetch` rejects our 402 body before
   it even signs, because its schema is a closed enum. We reimplemented just those two shims
   (~200 lines) and reused everything else. This isn't a MOI limitation, it's true of any chain
   outside their allow-list today.

**My recommendation for how to say it on stage:** *"x402 is chain-agnostic at the protocol layer
and chain-specific only at the facilitator, so adding MOI meant writing one service, not forking a
protocol."* That's accurate, it's the interesting engineering point, and it doesn't overclaim.

## 5. The gap closes in session 9

The escrow behaviour a stock facilitator provides, hold funds, release on delivery, refund on
failure, is exactly what MOI's native `lockup` / `release` gives us, and session 4 already proved
those work on devnet with real funds.

*Caution:* the session 4 runbook (removed from the handover repo on 14 October 2026) said the session 4 lock-and-release swap was trust-based, not atomic, and that atomic settlement would still need an escrow contract. TRANSCRIPT.md calls escrow-style pay-on-delivery native to MOI and "on the roadmap beyond these sessions"; DEMO-PLAN.md says escrow-style settlement is not available. Whether lock and release alone is escrow is not settled in these notes.

So the arc is:

- **Session 7**: facilitator verifies (what we have)
- **Session 9**: facilitator holds and releases conditionally, without ever taking custody of a key

At that point we're doing something stock x402 can't: escrow as a chain primitive rather than a
trusted intermediary.

---

## Bottom line

We are not missing a facilitator, we built one, and it speaks the real API. What we're missing is
the ability for it to move someone else's money, which MOI deliberately doesn't allow. For session
7 that's a footnote; by session 9 it becomes the advantage.
