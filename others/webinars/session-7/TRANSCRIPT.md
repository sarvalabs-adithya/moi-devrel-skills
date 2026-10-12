# Session 7 — script

**The speaker notes in [deck/MOI_Builders_S7new1f.pptx](./deck/MOI_Builders_S7new1f.pptx) are the
canonical script.** Present from presenter view; this file keeps only what doesn't fit in notes.

Flow (8 slides): title → the two agents → live demo (browser, `?gap=7000`) → the code
(showcase + pay.ts, line-cued) → self-imposed guardrails → roadmap (8 = +context inheritance,
9 = +x402) → bounty → close.

## The pivot (registry SDK write path is down)

- Product: the seller sells **bitcoin probability books**. Say "Probability Book Desk".
- Skill tag: **`sells-books`**. Agents: seller **agent_132**, buyer **agent_133**.
- **Never say** `sells-signals` or `agent_134` — that pair is retired (134's entry is tampered
  and cannot be restored while registry writes are down).
- **Happy path only. No tamper anywhere** — the toggle calls a registry write, which is down.
- `.env` must carry `SELLER_AGENT_ID=agent_132`, `BUYER_AGENT_ID=agent_133` before the demo.
- `showcase-discover-all.ts` line 22 still reads `sells-signals` in code — change that one string
  before showing it, or the screen contradicts the notes.

## Say these precisely

- **Nobody holds your money.** On MOI only the owner can move their own funds.
- **The seller prices per request. It does not decline** — refusing isn't implemented.
- **The identity check runs before the money moves.** The ordering is the point.
- **The probabilities are invented.** Say it before anyone asks.
- Say **"scan"**, not "search" — discovery is an O(n) client-side scan.
- x402 is **session nine**, already built once on a branch.

## Likely questions

**Seller doesn't deliver?** Today you lose it — same as handing over cash. Escrow-style
pay-on-delivery is native to MOI (lockup/release), on the roadmap beyond these sessions.

**Really two agents?** Two wallets, two on-chain identities, two independent decisions — one
machine and one mnemonic today. The transfer is real either way.

**Why not x402?** Session nine. Buys interoperability; the identity check is identical in both.

**Replay?** The transfer hash is burned after one use — in memory, so a seller restart resets it.

**Is the product real?** No — invented numbers, disclaimed on every response. The payment
machinery is the real part.

## Pre-flight

- restart `npm run ui` fresh (resets demand counters — first quote lands at list price)
- warm-up: two throwaway asks on the drawdown market so the pricing model engages on stage
- GROQ_API_KEY set; `.env` agent ids = 132/133
