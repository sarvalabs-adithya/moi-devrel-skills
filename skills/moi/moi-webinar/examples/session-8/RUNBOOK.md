# Session 8 run sheet - access policies

60 minutes, 18 slides. Deck at `deck/index.html`, terminal in `session-8-policies/`.
The demo is three beats and the whole session is built so the demo cannot upstage
the idea: the idea IS the demo.

---

## Before going live (T-30 min, do all of it)

```bash
cd session-8-policies
npm run preflight          # node up, both accounts live, LOGIC_ID set
npm run setup:fuel         # tops the agent up if below 6,000 KMOI
npm run demo               # ONE full rehearsal - leaves state clean
```

- [ ] All three exit 0. If the rehearsal fails, you have 30 minutes to debug; do not skip it.
- [ ] Owner balance printed ≥ 30,000 (policy writes need headroom; ~88k as of last check)
- [ ] Open `deck/index.html` in the browser, full-screen it, arrow through once
- [ ] Terminal font at presentation size, window ~100 cols so banners don't wrap
- [ ] `DEMO_PAUSE_MS=1500` ready on the demo command - at full speed the run is unwatchable
- [ ] Luma page title says VIII, not VII

The demo self-heals a leftover policy from a crashed run, so a broken rehearsal
does not poison the live run. It also refuses to start if the agent cannot afford
all three calls - if you see that, run `setup:fuel` again.

---

## The talk (times are cumulative)

### 0:00 - Slides 2 to 6: WHY this exists (14 min)

This block is the change the reviewer asked for, and it is the most important twelve
minutes of the hour. Do not rush to the feature.

Slide 2 (*where does the record live?*): open on a job someone actually gives an
agent. Books, buys, researches, reports. Each leaves a trace about **them**. Ask
the room where they think that trace is kept.

Slide 3 (*the app keeps its own copy of you*): Ethereum contracts own their
storage; off chain the service owns the row. Scattered, not yours, not
revocable. Say: "you are a row in ten different systems."

Slide 4 (*your record lives on your account*): the participant-centric model.
Say it is the data model, not a feature.

Slide 5 (*why that is worth doing*): three benefits, and the middle one is the
agentic payoff. Agents compose. A new agent picks up where the last left off
because they read the same account, with no integration built between two
vendors who have never heard of each other. Say that one slowly.

Slide 6 - **the slide the whole session hangs on.** If data lives on your
account, programs must be able to write to accounts they do not own. Every other
chain forbids exactly that. MOI had to open it, because participant-owned data
nobody can update is read-only data. And the moment you open it you owe an answer
nobody else owes: who may write to my account, and for what?

> The reviewer's framing, verbatim: "why did we even open up the capability for other
> people to write to your account? That's where the storyline is."

### 0:14 - Slides 7 to 11: the mechanism (11 min)

Slide 7: why a rule in code does not hold. The agent has its own key. "You are
not constraining it, you are asking it nicely."

Slide 8: the three questions a policy answers. Don't rush origin vs caller.

Slide 9 (Ticker): **the point is what is absent.** Thirty lines, no guard.

Slide 10 (the attempt): everything the agent sends. The participants line is a
declaration, not a request - this exact interaction was accepted and charged 86
fuel with no policy in place, and the hash on the slide is real.

Slide 11 (the grant): walk the builder. Then the contrast: the OWNER signs this
one, not the agent.

### 0:25 - Slides 12 to 13 + terminal: THE DEMO (14 min)

Slide 12 (*where the check happens*) is the new diagram: signed, mined, charged,
program runs - and only at the store instruction does the runtime read the policy
on the target account. Walk it left to right; it answers "where is this enforced"
before anyone asks.

Then slide 13 (refused / allowed / refused), and switch to the terminal:

```bash
DEMO_PAUSE_MS=1500 npm run demo
```

**Beat 1 - refused.** When the AccessError prints, stop and read it aloud:

> builtin.AccessError: actor is not allowed to write into other actor's storage

Say: "that did not come from our script. The interaction was accepted, signed,
mined, and charged for. The runtime refused the write at the instruction."

**Beat 2 - the grant, then the identical call lands.** Say: "same call, same
key, same code. The only thing that changed is a record on the OWNER's account.
Counter goes up by one."

**Beat 3 - revoke, refused again.** Say: "and the taking-back is one
interaction too. No redeploy, no key rotation. The agent finds out by being
refused."

Close on the summary box - point at the last line: *one policy on the owner's
account. Not one line of logic.*

If someone asks to see it again: run it again. It's idempotent and cheap
(~600 KMOI a run). A second run is more convincing than any slide.

### 0:39 - Slides 14 to 16: what you just saw (9 min)

Slide 14: the receipt. "Refusal is not an error message. It is a mined,
permanent, public record - and it cost the agent 86 fuel to be told no."

Slide 15: grant one interaction, revoke one. The revocation angle is the
strongest single idea for this audience - dwell here.

Slide 16: the ladder table. Be fair to the other chains - "Ethereum's
allowances genuinely bind. Solana's runtime genuinely enforces. The difference
is the unit: contract code, per program, per account. We're at the bottom rung
of granularity."

### 0:48 - Slide 17: the honest part (5 min)

Storage live, Asset/Logic/Key reserved. Say it plainly: **"the thing you all
want - 'this agent may spend at most 500' - is not something you can write
today. What you saw is the mechanism, on the one resource where it works. The
mechanism is the part that carries over."** Do not let a question walk you into
claiming spend caps work.

### 0:53 - Slide 18 + Q&A (7 min)

Repo, faucet, run it yourself: one funded wallet is enough.

---

## Likely questions, short answers

**"Can't the agent just delete the policy?"** No. A policy can only be written
or deleted by the account it sits on. The delete must be signed by the owner.

**"Is the agent a sub-account?"** No - its own account, its own key. On purpose:
a sub-account shares the parent's key, and a key the agent holds cannot be the
thing that limits the agent.

**"What if the agent calls a different logic?"** Then that logic tries to write
to the owner's storage and hits the same wall. The policy names which program
MAY write; everything else is refused by default.

**"So can I cap spending?"** Not yet - that's an asset policy, reserved but not
live. Storage only today. (Slide 17 exists so this answer is already on screen.)

**"Does a refused call cost money?"** Yes - mined and charged. Refusal is a
receipt, not a rejection.

**"I ran it and it failed BEFORE submission?"** You used the SDK's default flow.
`send()` without a fuel_limit runs fuel estimation first - a client-side
simulation - and the simulated revert throws before anything is submitted. The
demo pins `fuel_limit` to skip estimation so the refusal happens on chain, where
it belongs. Both behaviors are real; the chain's is the one that matters.

**"Wallet extension?"** The protocol side works from any signer; the missing
piece is an extension-backed signer in the SDK. The owner's role - approving
grants - is exactly the shape a wallet popup wants to be.

---

## If it breaks live

| Symptom | Cause | Do |
|---|---|---|
| `insufficient funds` on the grant | owner balance too thin | you have ~88k; if this fires anyway, say "devnet being devnet", show the rehearsal recording or the receipts in NOTES.md |
| `insufficient funds` from the agent | agent below 3× fuel limit | `npm run setup:fuel`, rerun - 30 seconds |
| beat 1 WRITES | leftover policy - should be impossible (self-heal) | let the run finish; it exits non-zero; rerun once |
| RPC timeouts | devnet down | fall back to the receipts: every beat's hash is in NOTES.md and readable on voyage once it's back |
| whole node dead | - | the deck stands alone: slides 9 to 12 carry real code and slide 11's diagram shows the enforcement path and the real error string. Present it as "here is what it does", offer a recorded run after |

The single rule: **never claim more than the screen shows.** If the demo dies,
the session degrades to a talk with receipts - which is still honest, and
honesty is the entire theme.
