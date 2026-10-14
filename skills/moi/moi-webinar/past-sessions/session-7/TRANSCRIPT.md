# Session 7: the script (short form, canonical)

> **What this is:** the script for MOI Builders Session 7, "agentic payments, part 1": two AI agents on devnet, a buyer and a seller, where the buyer finds the seller in MOI's on-chain agent registry, checks who it is paying, and pays with a native transfer. MOI Builders is the developer webinar series DevRel runs. Despite the file name, this is a short script and cheat sheet, not a transcript of what was said; the file name is kept so links keep working. Session 7 was held on Friday 7 August 2026 (inferred, per `skills/moi/moi-webinar/references/session-history.md`).
>
> **Status:** delivered. **This is the latest file for session 7 and the canonical one.** Where `DEMO-PLAN.md`, `STORYLINE.md` or `FACILITATOR-NOTE.md` in this folder differ (product name, tamper beat, x402, escrow, mock mode, what session 8 covers), this file wins, and each of those files carries a note saying so. Where this file and those files disagree on escrow, see the note under "Likely questions": not settled in these notes.
>
> **Where things are:** the full script is the speaker notes of the deck `deck/MOI_Builders_S7new1f.pptx`. That deck is not in this repo: it is in the `session-7/deck/` folder of https://github.com/moi-foundation/MOI-Webinars, on the branch `claude/agent-payments-simple` (per `session-history.md`). The code paths below (`npm run ui`, `showcase-discover-all.ts`, `pay.ts`, `.env`) are in that repo's `session-7/` folder.
>
> **Terms:** *x402* is an open standard for paying over HTTP 402 (Payment Required). *Lockup / release* are MOI's native calls to set funds aside for a named beneficiary and for that beneficiary to pull them. *Devnet* is MOI's public test network. A *bounty* is a reward for viewers who complete the session task and submit proof. *Groq* is the hosted language-model service the buyer uses to pick a market. *Context inheritance* is the idea, planned for session 8, of an agent working through an inherited sub-account of its owner.

**The speaker notes in the deck `deck/MOI_Builders_S7new1f.pptx` (see above for where it is) are the
canonical script.** Present from presenter view; this file keeps only what doesn't fit in notes.

Flow (8 slides): title → the two agents → live demo (browser, `?gap=7000`: the browser console reveals each step on a 7-second beat) → the code
(showcase + pay.ts, line-cued) → self-imposed guardrails → roadmap (8 = +context inheritance,
9 = +x402) → bounty → close. (Session 8 as held covered access policies, not context inheritance; this roadmap was the plan at the time.)

## The pivot (the registry SDK's write path was down at the time)

The pivot was a late change of plan: because writes to the registry were failing, the demo used two agents that were already registered, and the product and skill tag changed to match.

- Product: the seller sells **bitcoin probability books**. Say "Probability Book Desk".
- Skill tag: **`sells-books`**. Agents: seller **agent_132**, buyer **agent_133**.
- **Never say** `sells-signals` or `agent_134`, that pair is retired (134's entry is tampered
  and could not be restored while registry writes were down).
- **Happy path only. No tamper anywhere**: the tamper toggle in the browser UI (it repoints the seller's registry entry at an attacker to show the buyer refusing to pay) calls a registry write, which was down.
- `.env` must carry `SELLER_AGENT_ID=agent_132`, `BUYER_AGENT_ID=agent_133` before the demo.
- `showcase-discover-all.ts` line 22 still reads `sells-signals` in code, change that one string
  before showing it, or the screen contradicts the notes.

## Say these precisely

- **Nobody holds your money.** On MOI only the owner can move their own funds.
- **The seller prices per request. It does not decline**: refusing isn't implemented.
- **The identity check runs before the money moves.** The ordering is the point.
- **The probabilities are invented.** Say it before anyone asks.
- Say **"scan"**, not "search", discovery is an O(n) client-side scan.
- x402 is **session nine**, already built once on a branch.

## Likely questions

**Seller doesn't deliver?** In this demo you lose it, same as handing over cash. Escrow-style
pay-on-delivery is native to MOI (lockup/release), on the roadmap beyond these sessions.
(Not settled in these notes: `DEMO-PLAN.md` says escrow-style settlement isn't available on MOI, and `STORYLINE.md` and `FACILITATOR-NOTE.md` plan session 9 around it.)

**Really two agents?** Two wallets, two on-chain identities, two independent decisions, one
machine and one mnemonic at the time of the session. The transfer is real either way.

**Why not x402?** Session nine. Buys interoperability; the identity check is identical in both.

**Replay?** The transfer hash is recorded as spent after one use, in memory only, so a seller restart resets it. (A replay is someone submitting the same proof of payment twice.)

**Is the product real?** No, invented numbers, disclaimed on every response. The payment
machinery is the real part.

## Pre-flight

- restart `npm run ui` fresh (resets demand counters, first quote lands at list price)
- warm-up: two throwaway asks on the drawdown market (one of the demo's four markets) so the pricing model engages on stage
- GROQ_API_KEY set; `.env` agent ids = 132/133
