# Session 4 Live Demo: Account-to-Account Native Swap

> **What this is:** the runbook for MOI Builders Session 4, a live swap of two test tokens between two wallets using MOI's native lock and release. MOI Builders is the developer webinar series DevRel runs. The held date is not recorded in these notes (a bounty form was created on 2026-07-03, per `skills/moi/moi-webinar/references/session-history.md`).
>
> **Status:** delivered, with the scope settled as described below (a trust-based swap, not an atomic one). A later plan, `session-7/STORYLINE.md` in this folder, builds conditional settlement on the same lock and release calls; see the note under "Still not atomic" for how that sits with this file.
>
> **Where the code is:** the code and commands below (`session-4/`, `extras/swap-cli.js`, `logic/swap.js`, the Vite UI) live in https://github.com/moi-foundation/MOI-Webinars, not in this repo. Run everything from that repo's `session-4/` folder.
>
> **Terms:** *TKA* and *TKB* are the two throwaway test tokens created for the demo. *Alice* and *Bob* are the two demo wallets. *MAS0* is MOI's native fungible-token standard, so no token contract is written. *Lockup* sets part of your balance aside for a named beneficiary; *Release* is the beneficiary pulling it. *Devnet* is MOI's public test network and *Voyage* (voyage.moi.technology) is its explorer and faucet. *Gas*, when it appears, means fuel, the cost of running an interaction (MOI's word for a transaction). A *bounty* is a reward for viewers who complete the session task and submit proof.

90-minute MOI Builders webinar: Alice and Bob swap **TKA ↔ TKB** directly (no pool, no deposit).
Flow: each side **Locks** its leg *for the counterparty*, an irrevocable on-chain offer
that only the beneficiary can pull, then each side **Claims** what was locked for them.
All MAS0-native (`Lockup` / `Release`), no custom contracts.

**This is a trust-based swap, not a chain-enforced atomic swap.** Locking is irrevocable
and beneficiary-only (verified on devnet), so once Alice locks she can't take it back and
only Bob can pull it, but nothing on-chain forces Bob to lock his side in return. That's
the final, settled scope for this demo; true atomicity needs an escrow contract or
multi-party interaction (explicitly out of scope, see "future session" note below).

**The Claim button is gated by a real on-chain check.** `moi.Lockups(accountId)`, a raw
JSON-RPC method, returns every lockup an account has created, including the beneficiary.
Unlike `BalanceOf` (which only lets you query your own balance), this has no such
restriction: any wallet can look up any account's outstanding lockups. So before Claim is
clickable, the UI actually asks the chain "has the counterparty locked this for me?" and
only enables the button once the answer is yes, verified live on devnet.

(Two checks work together here: the UI enables **Claim** from the `moi.Lockups` read described above, and the claim itself is also checked by the app against the balance change, as set out under "Enforced by the app" further down. The first is what the audience sees; the second is what makes a claim with nothing locked report failure.)

---

## Before the webinar (once)

```bash
cd session-4
npm install
cp .env.example .env
# Edit .env: VITE_ALICE_MNEMONIC and VITE_BOB_MNEMONIC: two separate
# faucet-funded Voyage wallets (devnet-only, gitignored)
npm run setup
```

The `VITE_` mnemonic variables are for devnet test wallets only: Vite bundles every `VITE_` variable into the browser code, so never put a mnemonic that holds real funds in them.

**Fund both wallets** at [voyage.moi.technology](https://voyage.moi.technology) if balances are empty.
Both use the default Voyage faucet derivation path, so any faucet-created wallet works as-is.

- **Alice** must exist on devnet (setup deploys assets from Alice).
- **Bob** must exist on devnet before Bob can sign his lock/claim.

If setup skipped minting TKB to Bob (Bob unfunded):

```bash
# Fund Bob's address (printed by setup), then:
npm run mint-tkb
```

Setup writes `VITE_TKA_ASSET_ID` and `VITE_TKB_ASSET_ID` into `.env`.

---

## Demo path A: CLI (milestone; works even if UI is cut)

Fixed rate (display only): **1 TKA = 0.9 TKB** → Alice sends **100 TKA**, receives **90 TKB**.

### Step-by-step commands

```bash
# 0. Show starting balances
node extras/swap-cli.js balances

# 1. Alice locks 100 TKA for Bob (irrevocable offer)
node extras/swap-cli.js lock-alice

# 2. Bob locks 90 TKB for Alice
node extras/swap-cli.js lock-bob

# 3. Alice claims her 90 TKB from Bob's lock
node extras/swap-cli.js claim-alice

# 4. Bob claims his 100 TKA from Alice's lock
node extras/swap-cli.js claim-bob
```

Or run the full sequence:

```bash
npm run swap
# same as: node extras/swap-cli.js full
```

After each step the CLI prints all four balances (Alice/Bob × TKA/TKB).

---

## Demo path B: Swap card UI

```bash
npm run dev
# Opens http://localhost:5174
```

### Live clicks (mirror the CLI flow)

1. **Log in as Alice**: paste Alice's mnemonic, click **Connect wallet**
   - Narrate: the mnemonic derives the keypair in the browser; the address is your identity
   - Amount: `100` TKA → receive shows `90 TKB`; paste Bob's address as counterparty
   - Notice **Claim is disabled** with the hint "Waiting for counterparty to lock 90 TKB…"
   - Click **Lock** → 100 TKA locked *for Bob*. Her balance drops by 100.
   - Narrate: this is irrevocable, Alice cannot take it back; only Bob can claim it.

2. **Disconnect → log in as Bob**: paste Bob's mnemonic
   - Click **⇅ Flip** so the send side is TKB; amount `90`; paste Alice's address
   - Notice **Claim is already enabled**, the app checked `moi.Lockups(Alice)` and found
     her 100 TKA lock for Bob. Narrate: this is a real chain read, not a guess.
   - Click **Claim** → Bob pulls his 100 TKA from Alice's lock.
   - Click **Lock** → 90 TKB locked for Alice. Both offers are now on-chain.

3. **Disconnect → log in as Alice again**
   - Claim is now enabled (the app detected Bob's lock automatically, or within ~4s via
     the polling check)
   - Click **Claim** (amount `100`, counterparty Bob) → she pulls her 90 TKB from Bob's lock
   - **Refresh balances**: swap complete; verify hashes on Voyage.

Keep both mnemonics and both addresses in a notes file for fast pasting during the demo (devnet test wallets only).

---

## What each on-chain call does (one line each)

| Step | Who | Call | What it does |
|------|-----|------|--------------|
| 1 | Alice | `Lockup(beneficiary=Bob, 100 TKA)` | Irrevocable offer: 100 TKA leaves Alice's spendable balance; only Bob can pull it. |
| 2 | Bob | `Lockup(beneficiary=Alice, 90 TKB)` | Bob's counter-offer: 90 TKB locked, only Alice can pull it. |
| 3 | Alice | `Release(benefactor=Bob, beneficiary=Alice, 90 TKB)` | Alice claims her TKB from Bob's lock (signed by her, the beneficiary). |
| 4 | Bob | `Release(benefactor=Alice, beneficiary=Bob, 100 TKA)` | Bob claims his TKA from Alice's lock, swap complete. |

**Protocol facts (verified on devnet):** the locker *cannot* reclaim a beneficiary-lock
(a release back to self is accepted but moves nothing), and only the named beneficiary's
signature actually pulls the funds.

**Enforced by the app:** MAS0's `release()` has no on-chain guard, calling
it when nothing is locked still "succeeds" but moves zero funds. `logic/swap.js`'s `claim()`
checks the balance delta itself and reports failure ("nothing to claim yet") unless funds
actually moved. That's what makes "Claim only goes through once the counterparty has
locked" true in this demo, it's an app-level check, not a protocol-level one.

**Still not atomic:** Alice locks first, and Bob could simply never lock his side, Alice's
100 TKA sits locked for him indefinitely with nothing forcing reciprocation. Making both
legs execute together or not at all needs an escrow contract or multi-party interaction
(future session). Note: `session-7/STORYLINE.md` and `session-7/FACILITATOR-NOTE.md` describe lock and release as the basis for escrow-style, pay-on-delivery settlement in a later session. Whether a lockup alone counts as escrow, or still needs the extra contract named here, is not settled in these notes.

**Not in this demo:** AMM math (the pricing formula pool-based exchanges use), atomic settlement contracts, Coco contracts, resolver/intents (systems where a solver finds the best route for a stated goal), a backend, or a wallet extension.

---

## SDK calls used (verified against `js-moi-sdk@0.7.0` type defs)

```js
import { VoyageProvider, Wallet, MAS0AssetLogic, getAssetDriver } from 'js-moi-sdk'

const provider = new VoyageProvider('devnet')
const wallet = await Wallet.fromMnemonic(mnemonic, path)
wallet.connect(provider)
const address = (await wallet.getIdentifier()).toHex()

// Deploy / mint (setup only)
await MAS0AssetLogic.create(wallet, 'TKA', 1_000_000, address, true).send()
await new MAS0AssetLogic(assetId, wallet).mint(address, amount).send()

// The swap ops (ASSET_INVOKE callsites: Lockup / Release)
// Lock FOR the counterparty (irrevocable offer):
await new MAS0AssetLogic(assetId, alice).lockup(bobAddress, amount).send()
// Claim, must be signed by the beneficiary:
await new MAS0AssetLogic(assetId, bob).release(aliceAddress, bobAddress, amount).send()

// Read balance
const driver = await getAssetDriver(assetId, wallet)
const { output } = await driver.routines.BalanceOf(address) // output.balance

// Read a counterparty's outstanding lockups, raw RPC, not restricted to
// your own account like BalanceOf is. Docs: https://docs.moi.technology/docs/build/json-rpc#moilockups
const response = await provider.execute('moi.Lockups', {
  id: counterpartyAddress,
  options: { tesseract_number: -1 },
})
const lockups = provider.processResponse(response)
// each entry: { id: beneficiary, asset_id, token_id, amount, expiry }
```

Use **numbers** (not bigint) for amounts in `.send()` payloads, bigint supply broke signing in our devnet tests with this SDK version. (`webinar-vibecode-plans.md` in this folder shows bigint literals such as `100n`; that file is a plan that was not run, so this runbook's rule is the tested one.)

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `VITE_ALICE_MNEMONIC is not set` | Copy `.env.example` → `.env` |
| `account not found` (Bob) | Fund Bob at [voyage.moi.technology](https://voyage.moi.technology), run `npm run mint-tkb` |
| `Failed to sign interaction` on deploy | Ensure amounts are plain numbers, not bigint |
| Lock or Claim fails | Counterparty account must exist on devnet |
| Claim says "nothing to claim yet" | Counterparty hasn't locked their side, wait, then retry |
| `insufficient funds` on any call | Wallet is low on devnet native fuel (gas), fund it at [voyage.moi.technology](https://voyage.moi.technology) |
| Balances look reset after a swap but a redeploy fails on `insufficient funds` | Don't redeploy, run `node extras/rebalance.js` to cheaply restore the starting balances via plain transfers on the existing tokens (the original note said "500000/0"; setup creates each token with 1,000,000 supply, and how that maps to 500000/0 is not explained in these notes) |
| UI broken after fresh `npm install` | `patch-package` must run (postinstall), it fixes the SDK's broken ESM build |

---

## Verify on Voyage

Open [voyage.moi.technology](https://voyage.moi.technology), search Alice/Bob addresses, confirm the Lockup and Release interaction hashes match the CLI/UI status line.
