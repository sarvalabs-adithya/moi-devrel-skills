# Session 7: live demo plan (terminal variant + mechanics)

> **What this is:** the live-choreography plan for MOI Builders Session 7, "agentic payments, part 1": a buyer AI agent finds a seller agent on MOI's on-chain agent registry, checks that the seller's quoted payment address matches the wallet the registry lists for it, then pays with a native transfer. MOI Builders is the developer webinar series DevRel runs. Session 7 was held on Friday 7 August 2026 (inferred, per `skills/moi/moi-webinar/references/session-history.md`). This file is the terminal-only variant plus the break-glass table; the browser show is covered in TRANSCRIPT.md.
>
> **Status:** delivered in part, and **superseded in part** by [TRANSCRIPT.md](./TRANSCRIPT.md), which is the latest file and canonical for session 7. Where this file differs, TRANSCRIPT.md wins:
> - **Product name.** This file says "Signal Desk" and the skill tag `sells-signals`. The delivered session used the "Probability Book Desk" and the skill tag `sells-books` (agents 132 and 133), because the registry's write path was down. Read this file's names that way. (`STORYLINE.md` describes a seller of books in another sense; see its status note.)
> - **No tamper beat.** Loop 2 below runs `--tamper`, which makes a registry write. TRANSCRIPT.md says to do no tamper in the delivered session. Loop 2 is kept as the full-version plan.
> - **Browser gap.** This file suggests `?gap=1200` for a big room; TRANSCRIPT.md uses `?gap=7000`.
> - **Escrow and "nobody holds your money".** See the note under "Things to say precisely": this file and TRANSCRIPT.md do not agree on whether escrow-style settlement exists on MOI, and that is not settled in these notes.
> - **Session 8.** This file says session 8 is about budgets and spend limits; TRANSCRIPT.md's roadmap says session 8 adds context inheritance; session 8 as held (4 September 2026) was about access policies. The notes do not reconcile the three.
>
> **Where the code is:** every path below (`packages/...`, `npm run demo`, `npm run ui`) is in the session 7 folder of https://github.com/moi-foundation/MOI-Webinars, not in this repo. Run commands from that folder. Terms are defined in the Glossary at the end of this file.

**The canonical show is the deck's speaker notes + `npm run ui`**: see [TRANSCRIPT.md](./TRANSCRIPT.md).
This file keeps the terminal-only variant (for rehearsal, or if the browser dies) and the break-glass table.

Note the numbering difference: the browser shows the identity check as **card 7** (it has an extra
price-judgment card); the terminal banners call it **step 6**. The narration below uses terminal numbers.

Show code → run it → read the output. Three loops of that, each one idea.

Schedule and talking points: session 7's own `RUNBOOK.md` is not in this repo. The blank template for one is `skills/moi/moi-webinar/templates/RUNBOOK.md`, and a filled-in example is `skills/moi/moi-webinar/examples/session-8/RUNBOOK.md`. This file is only the live choreography.

---

## Before you start

Two windows. **Editor** on the left, **terminal** on the right, both visible at once, you will be
pointing from one to the other constantly and alt-tabbing kills that.

```bash
cd session-7
npm install
npm run demo            # confirm green BEFORE anyone is watching
clear
```

- terminal 18 to 20pt, dark, ~100 columns (banners are 78 wide, narrower and they wrap)
- `export DEMO_PAUSE_MS=1200`: the demo runs in 1.2s otherwise, which is unnarratable
- no `.env` open in the editor, nothing with your mnemonic in the window title
- buyer balance ≥ ~30 base units (the settlement asset's smallest indivisible units) if you plan to run `attack-test` (it spends ~12; elsewhere in this file it is described as ~11 real transfers plus an honest control payment, so the exact figure is not settled in these notes)

**Open these four tabs in the editor now**, in this order. You will move down them as the session
goes:

1. `packages/shared/src/payment-proof.ts`
2. `packages/agent-buyer/src/identity-check.ts` ← the one that matters
3. `packages/agent-seller/src/verify-proof.ts`
4. `packages/agent-buyer/src/pay.ts`

---

## Loop 1: the whole thing works (≈8 min)

### Run first, explain after

Resist opening code here. Let them watch it work with no idea how, then earn the explanation.

```bash
npm run demo
```

~25 seconds at `DEMO_PAUSE_MS=1200`. Say almost nothing while it runs. Then scroll back to the top
and walk it.

### Read the output

| Point at | Say |
| --- | --- |
| `BUYER · step 1` → `scanned` / `agents selling signals` (the delivered session said "selling books") | "It was never given a URL. It scanned the registry and filtered on a skill tag." |
| `BUYER · step 2` | "The questions are free. The answers are not. That's the seam the paywall sits on." |
| `BUYER · step 3` → `decided by` | "It picked the drawdown market for the question. That choice is the agent's." Check `decided by` says the model name, if it says `local-fallback`, the key isn't loaded and you should not claim the agent reasoned. |
| `SELLER · step 5` | "HTTP 402, Payment Required. Reserved in 1997, basically unused until agents needed it." |
| `BUYER · step 7` → `ix hash` | "That's a real interaction on devnet. The buyer moved its own money, on MOI nobody can move it for you." |
| `SELLER · step 9`, the seven ticks (the seven checks in `verify-proof.ts`, each printed with a tick) | "The seller checked this itself. All seven are reads. Nobody was trusted." |
| the closing box | "About a second. No human, no account, no API key." |

### The line to land

> "Two strangers just transacted. Neither of them had ever heard of the other before this ran."

If anyone asks about the numbers: **they are placeholders.** They are not market data and there is no
real forecasting model behind them (the agent's market choice does use a language model, see below, which
is a different thing). Every response carries a `disclaimer` field saying so, point at it rather than
letting someone assume otherwise.

---

## Optional opener: the agent console (browser)

```bash
npm run ui                       # http://localhost:4000
open http://localhost:4000?gap=1200   # slower reveal, for a big room
```

Steps are revealed one at a time on a steady beat rather than in bursts, the work itself is lumpy
(the registry scan, then the transfer landing) and rendering as fast as events arrive dumps half
the run on screen at once. `?gap=` sets the millisecond spacing; default 700. A pulsing "working"
row shows whenever the agent is genuinely waiting on the chain, so a pause reads as work rather
than as a hang.

A page that narrates the agent's reasoning as it happens, it realises it can't answer, scans the
registry, shows the seller's advertised skills, gets quoted, checks who it's about to pay, pays on
chain, watches the seller verify, and unlocks the answer. Balance ticks down at the top.

This is the strongest opener if you have a projector: it shows the *decision process*, not just a
log. Terminal version below if you'd rather stay in one window.

⚠️ Same Groq caveat as `ask`, see below. (Groq is the hosted language-model service the buyer agent uses to choose a market; it needs `GROQ_API_KEY`.)

---

## Optional opener: let the room drive it (terminal)

If you want the "agentic" idea to land before any code, take a question from the audience:

```bash
npm run ask
```

Type what someone shouts out. The agent finds a seller it was never told about, checks who they
are, pays, and answers, and the balance line drops by 1 each time.

⚠️ **Only do this with `GROQ_API_KEY` set.** Without it the agent matches keywords, and a vague
question like *"should i be worried about a crash"* falls through to `no strong match; defaulting
to btc-100k-2026`, it buys the wrong market, on screen, from a question someone in the room just
gave you. The catalog says "draw down"; nobody says "draw down".

With the key it is reliable: 5 questions x 5 runs each, zero drift, all four markets reachable.
Measured, not assumed, so you can safely say "watch it pick the drawdown market" before it does.

---

## Loop 2: the part that only works on MOI (≈12 min) ← **the session**

> Full-version plan. The delivered session skipped the `--tamper` run (see the status note at the top): the Loop 2 explanation of the identity check was given, but the attack was not run live.

Everything so far is setup for this. Slow down.

### Show the code

Open **`identity-check.ts`**. The whole file is 42 lines, put it on screen at once, don't scroll.

Point at exactly one line:

```ts
if (normalizeAddress(registryWallet) !== normalizeAddress(quote.payTo)) {
```

> "The seller said *pay me at this address*. That address is 32 bytes. It tells you **where** to
> send money, it doesn't tell you **whose** address it is.
>
> So before paying, the agent goes back to the registry and asks: is this actually the Signal Desk's
> registered wallet? Nothing in a payment protocol can answer that. It needs an identity that lives
> somewhere both parties can check, and that's the chain."

Then scroll up 8 lines to `approve()` in `pay.ts` and make the timing point:

> "This runs **before** the transfer. Not after. There's no escrow here and nothing to claw back:
> once it's sent, it's sent. So every question worth asking gets asked here."

### Run the attack

```bash
npm run demo -- --tamper
```

> "I've repointed the seller's registry entry at an attacker, as if someone compromised the
> listing. The seller still asks to be paid at its real address. Watch what the buyer does."

### Read the output

Three things, in order:

1. `DEMO · 1b`: the registry now says `0xdededede…`
2. `BUYER · step 7`: red ✗, `registry says` vs `quote says` side by side
3. **It stops at step 7.** There is no step 8, no transaction was ever built.

> "It never reached the payment. **Money moved: none.** And notice it's the buyer that caught this
> that, not the seller, not a middleman. The party with something to lose is the one that checks."

Let the silence sit before moving on. This is the beat people remember.

---

### The strongest version of this beat

Run the same question twice, keyless then keyed:

```bash
GROQ_API_KEY="" npm run ask -- "should i be worried about a crash"   # picks btc-100k-2026, wrong
npm run ask -- "should i be worried about a crash"                   # picks btc-drawdown-20, right
```

Identical input, visibly different reasoning: `no strong match; defaulting to` versus `Directly
related to crash risk`. That is what "the agent decided" actually looks like.

---

## Loop 3: why you should believe any of it (≈8 min)

A green happy path proves nothing, a verifier that accepts everything also goes green.

### Show the code

Open **`verify-proof.ts`**. Don't read all seven. Show two:

**Check 3, `key_binds_to_payer`**: and explain why it isn't redundant:

> "Transfers are public. Anyone can watch the chain and see that transfer land. So what stops
> someone else quoting *my* transaction hash and collecting the estimate I paid for?
>
> The proof is signed, and this check derives the participant ID back out of the public key. You
> can't claim a payment you didn't make."

**Check 6, `transfer_landed_on_chain`**: and what it costs:

> "The seller doesn't take the buyer's word that it paid. It reads the interaction off the chain and
> decodes it: right sender, right recipient, right amount. That's the price of not having a
> middleman, the seller has to do this itself."

### Run the suite

```bash
npm run attack-test
```

⚠️ **This makes ~11 real transfers and is slow, budget a few minutes.** Start it, then keep
talking over it; don't stand in silence watching a spinner. If you're tight on time, skip it and
show a screenshot instead.

### Read the output

Don't read all twelve lines aloud. Pick three:

| Line | Say |
| --- | --- |
| `control: an honest payment IS accepted` | "This one has to pass, or the suite proves nothing." |
| `underpayment → quote_mismatch` | "Signed honestly, for less than asked." |
| `replayed payment → already_spent` | "One transfer buys one thing." |

> "Eleven forgeries, each rejected for the *right* reason, not just rejected."

---

## If it breaks

| Symptom | Do this |
| --- | --- |
| **Happy path refuses at step 7** | You Ctrl-C'd a `--tamper` run and the registry is still pointed at the attacker. Run `npm run demo -- --tamper` again and **let it finish**, it restores on the way out. |
| `SETTLEMENT_ASSET_ID is not set` | `npm run setup:asset` |
| `agents are not registered` | `npm run setup:registry` |
| Devnet unreachable | There is no offline mode. Go to the recording. |
| `attack-test` says balance too low | `npm run setup:asset` tops the buyer up |

**Record a clean run of all three before the session and have it one keystroke away.** There is no
mock mode, if devnet is down during your slot, the video is the whole contingency. (`STORYLINE.md` says the built demos could run with `CHAIN_MODE=mock`; this file and the session 7 README say there is no offline mode. Not settled in these notes; the delivered session ran on devnet.)

---

## Things to say precisely

- **"Nobody holds your money."** Not a design choice, on MOI only the owner can move their own
  funds, so escrow-style settlement isn't available. The buyer pays, the seller confirms by reading.
  *Not settled in these notes:* TRANSCRIPT.md says escrow-style pay-on-delivery is native to MOI (lock and release) and on the roadmap, and `STORYLINE.md` builds its session 9 on lock and release. This file says escrow is not available. Until someone checks, do not state either as a flat fact; the safe claim is the one all the files share: in this demo nobody holds the money, and if the seller does not deliver the buyer cannot get it back.
- **Don't call this x402.** It isn't. (x402 is an open standard for paying over HTTP 402 Payment Required.) If asked: the x402 version is on a branch, does the same demo,
  buys interoperability, costs twice the code. Both have the identical identity check. TRANSCRIPT.md agrees and places x402 in session 9; the earlier `STORYLINE.md` and `FACILITATOR-NOTE.md` treated session 7 as x402.
- **Don't say "search".** Registry discovery is an O(n) client-side scan (the buyer walks every registry entry, so the cost grows with the number of agents).
- **Don't claim budgets or spend limits.** Nothing here constrains what the agent may spend. This file calls
  that session 8 (see the status note about what session 8 actually covered), and it's a good answer to the question, not a dodge.
- **Don't claim the LLM picked the market** unless `decided by` says the model name. With no key
  it prints `local-fallback` and someone will read it.
- **The probabilities are made up.** Say it out loud. With the model running they read as analysis;
  the `basis` field is forced to end "model guess, no market data", but don't rely on anyone noticing.

## The three sentences

If only three things get across:

1. Two agents transacted with no human, no account and no prior relationship.
2. Before paying, the buyer asked the chain **who** it was paying, and refused when the answer was
   wrong.
3. Nobody held anybody's money at any point.

---

## Glossary

| Term | Meaning |
| --- | --- |
| Agent registry | An on-chain list of agents. Each entry has an owner, an agent wallet, a status and a link to a card describing the agent and its skills. |
| Skill tag | A label on a registry entry (for example `sells-books`) that a buyer filters on to find sellers without being told a URL. |
| HTTP 402 | "Payment Required", the web status code a seller returns with a price and a pay-to address. |
| Quote | The seller's 402 response: price, asset and address to pay. |
| Interaction (`ix`) | MOI's word for a transaction. `ix hash` is its identifier on devnet. |
| Participant ID | The 32-byte identifier of an account on MOI; the buyer derives it from the public key in a signed proof. |
| Devnet | MOI's public test network. Funds are test funds, and resets wipe accounts and contracts. |
| Tamper | The demo toggle that repoints the seller's registry entry at an attacker to show the buyer refusing to pay. It needs a registry write. |
| Groq | The hosted language-model service the buyer uses to pick a market (`GROQ_API_KEY`). Without it the agent falls back to keyword matching (`local-fallback`). |
| Settlement asset | The test token the buyer pays with (`SETTLEMENT_ASSET_ID`). |
