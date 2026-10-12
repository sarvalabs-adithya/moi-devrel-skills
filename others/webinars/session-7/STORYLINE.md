# X402 on MOI — storyline & phase plan  (AGREED, and now built)

*Internal. Gitignored.*

**Status: sessions 7 and 8 are built and green in mock mode. Session 9 is a plan.**

Written against the 4 Aug call. The ask was: **"Write down the storyline. Phase one, phase two,
phase three. Send it out to me."** — and the framing constraint: *"If you give everything in a
single dev talk, everyone will lose it."*

---

## The one-line story

**An agent finds another agent on MOI, and pays it — without a human, an account, or an API key.**

Each phase adds one idea. Nothing before its turn.

| Phase | Dev talk | The idea | The "aha" |
| --- | --- | --- | --- |
| **V1** | this Friday | **Identity + payment** | I can *find* an agent by what it sells, and pay it, with no prior relationship |
| **V2** | +1 | **Authority** | The chain refuses a payment my agent shouldn't make |
| **V3** | +2 | **Conditional settlement** | Money only moves once the goods actually arrive |

---

## V1 — Register, discover, pay

**Story:** I want to buy a book. I don't know who sells books. I ask MOI's agent registry for an
agent with the skill `sells-books`, it quotes me a price over HTTP 402, I pay, I get the book.

**On stage:**
1. Register two agents on MOI — a buyer and a book seller. *(Reuses the agent registry from
   session 3.)*
2. The buyer searches the registry **by skill**, not by URL. It has never been told where the
   seller lives.
3. `GET /book/:title` → **402 Payment Required** with a price and an address.
4. Buyer reads the seller's `agent_wallet` **from the registry** and checks it matches the address
   in the invoice. This is the beat: *x402 gives you an address; MOI tells you whose it is.*
5. Buyer pays — a native MAS0 transfer, sub-cent.
6. Seller confirms the payment landed and returns the book.

**What we claim:** identity + payment. Nothing about permissions.

**Failure beat to run live:** repoint the seller's registry wallet at an attacker → the buyer
refuses to pay. Nothing about this is possible on a chain without an agent registry.

---

## V2 — Authority

**Story:** the same purchase, but now my agent has a budget I set, and it cannot exceed it — even
if it wants to, even if it's compromised.

**On stage:** the agent tries to buy something over its cap. The **chain** rejects the spend. The
agent never gets the chance to be well-behaved or badly-behaved; the rule isn't in the agent.

**Deliberately deferred to here, not V1:** the sub-account / `AgentBudget` machinery. Per the call —
*"When my authority comes into picture, that is the exact point you're trying to make."*

**Language that must be exact** (this was pushed back on directly, and the pushback was right):
sub-accounts are technically just accounts, and they **share the parent's key**. Isolation is *not*
the selling point. The selling point is that **a logic specifies the rules of trade and the chain
enforces them**. Say *"the chain refuses the spend"* — never *"the agent can't touch the money."*

---

## V3 — Conditional settlement

**Story:** pay-on-delivery. Funds are committed up front but only release once the seller actually
delivers; the buyer is made whole if they don't.

**On stage:** the seller fails to deliver → the buyer gets refunded, on chain, with no arbiter.

Built on MOI's native `lockup` / `release` — already proven on devnet in session 4. This is the
payoff of the whole arc: *the payment protocol never changed; the settlement layer just got
better.*

---

## Where the build sits — DONE

| | Folder | State |
| --- | --- | --- |
| **V1** | `session-7/` | ✅ built, green in mock mode. Book seller, registry discovery, identity check, `--tamper`. **Zero** inheritance. |
| **V2** | `session-8/` | ✅ built, green in mock mode. Same story + inherited sub-accounts, `AgentBudget` cap, `--overspend`. |
| **V3** | `session-9/` | 📋 plan only — the full commerce flow (enquire → quote → delivery details → pay → deliver). |

Both built sessions run with **no wallet at all** (`CHAIN_MODE=mock npm run demo`) and pass an
11-forgery adversarial suite. Neither has been run against a funded devnet wallet yet.

The seller now sells **books**, per the call. Prediction markets are gone.

---

## Deliverables around this

- **Blog per dev talk**, in Markdown, published to moi.technology + Medium, then linked from
  Twitter/LinkedIn (the post is just the hook; the crawler follows the link).
- **Structure:** aha first — *why* we did this and what it unlocks — then the how-to guide.
- **Backlinks** into `js-moi-sdk`, the agent registry SDK, and the native assets docs. Each blog
  should also link the previous phase's blog, so the three build one web of content.
- **Positioning:** always say which phase this is, and that the platform has a bigger scope
  coming.

---

## Open question for review

The call landed on *"just do a value transfer"* as the floor for V1. What's built goes further —
registry discovery by skill, plus the identity check. I believe that is the right V1: the identity
check is the only part that is uniquely MOI, and a bare transfer doesn't show it. The `--tamper`
beat is the whole reason the audience should care.

But it is more than the agreed minimum. Confirm before Friday.

## V3 note

Rahul left V3 open on the call ("v3 you do something else"). `session-9/README.md` builds it around
the one concrete richer thing he *did* describe — the full book purchase, with availability,
delivery details and a real quote — with escrow as the recourse mechanism. Worth confirming that
reading.
