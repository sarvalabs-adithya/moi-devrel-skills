# Webinar S1: Cheatsheet

> **What this is:** the on-screen cheat sheet for MOI Builders Session 1 ("CocoLab and the SDK"): two Coco contracts (`Flipper`, `ContextFlipper`) run in CocoLab, then the same Flipper deployed to devnet from JavaScript. Written to be kept on a second screen during the show. The code and commands refer to the session code in https://github.com/moi-foundation/MOI-Webinars (folder `session-1/`, run from that folder's root), not to this repo.
>
> **Status:** delivered. The held date of Session 1 is not recorded in these notes. Treat the commands as a rehearsal script: devnet has been reset since, so the ids deployed at the show and the funded wallet probably no longer exist.
>
> **Terms:** *Coco* is MOI's smart-contract language and *CocoLab* is its local sandbox (a REPL, no network). A *logic* is a deployed Coco program; a *participant* is any account that holds state on MOI; *devnet* is MOI's public test network; *Voyage* is its explorer (voyage.moi.technology); an *interaction* is MOI's word for a transaction. *MAS0* is the native fungible-token standard. More in `OVERVIEW.md` (same folder), Glossary.

---

## Pre-show: Compile both modules

From the repo root, once before the show (and after any `.coco` edit):

```bash
npm run compile
```

That's just shorthand for: in each module folder, run `coco compile` (produces `*.yaml`), then `coco manifest convert *.yaml -f json -o *.json` so the SDK can load it.
You should end up with `flipper/flipper.json` and `context-flipper/context_flipper.json`.

---

## Demo 1: Flipper (shared state) in CocoLab

The whole module, `flipper/flipper.coco`:

```coco
coco Flipper

state logic:
    values Map[Identifier]Bool

endpoint deploy Init():
    mutate values <- Flipper.Logic.values:
        values[Sender] = true

endpoint dynamic Flip():
    mutate values <- Flipper.Logic.values:
        values[Sender] = !values[Sender]

endpoint static Mode() -> (value Bool):
    observe values <- Flipper.Logic.values:
        value = values[Sender]
```

Two things to call out while it's on screen:
- `state logic`: one shared state. Every caller reads and writes the same `values` map.
- The map is keyed by `Identifier`, so each sender gets their own slot, but the *container* is global. We'll change exactly that in Demo 2.

Working dir: `flipper/`

1. `coco lab init`
   *"Boots a local CocoLab sandbox, no network, our module is preloaded."*
2. `deploy Flipper.Init()`
   *"Init writes `true` into the sender's slot of the shared map."*
3. `observe Flipper.Logic.values[default_user]`
   *"And there it is, `true`. Note the path: `Flipper.Logic`, one shared logic state."*
4. `invoke Flipper.Flip()`
   *"Flip toggles that same slot."*
5. `invoke Flipper.Mode()`
   *"Mode reads it back. Now it's false. Same map, same caller, mutated in place."*

---

## Demo 2: ContextFlipper (actor context)

Same program as Flipper, with three lines changed (`context-flipper/context_flipper.coco`). The two participants used in the CocoLab walk-through are named Adi and Robert (the original notes called this "the Robert demo" without saying why):

```coco
coco ContextFlipper

state actor:                                      // was: state logic
    value Bool

endpoint enlist Init():                           // was: endpoint deploy Init()
    mutate true -> ContextFlipper.Sender.value    // was: Flipper.Logic.values[Sender] = true

endpoint dynamic Flip():
    mutate value <- ContextFlipper.Sender.value:  // was: Flipper.Logic.values
        value = !value
```

What that diff actually means:
- `state actor`: every participant gets their **own** state slot. No shared map.
- The state path is now `ContextFlipper.Sender` (the caller), not `ContextFlipper.Logic`.
- `endpoint enlist` (instead of `deploy`), each participant *joins* the logic separately.
That one keyword (`logic` → `actor`) is what unlocks per-actor isolation and parallel execution.

Working dir: `context-flipper/`

1. `coco lab init`
   *"Same idea, but the state declaration is `actor`, not `logic`."*
2. `register Adi`
   *"Register Adi as a named participant in this environment."*
3. `wipe default.sender` then `set default.sender Adi`
   *"`coco lab init` auto-binds the sender to `default_user`, so we wipe and re-point it at Adi. From here on, calls run as Adi."* (`default.sender` is CocoLab's setting for who the current caller is.)
4. `enlist ContextFlipper.Init()`
   *"Notice the verb, `enlist`, not `deploy`. We're joining an actor-scoped logic as Adi."*
5. `observe ContextFlipper.Adi.value` → `true`
   *"Path is `ContextFlipper.<sender>`, Adi's own slot."*
6. `register Robert`
   *"Now I'll add a second participant, Robert, to demonstrate isolation."*
7. `wipe default.sender` then `set default.sender Robert`
   *"Same handshake, wipe, then switch the designated sender to Robert."*
8. `enlist ContextFlipper.Init()`
   *"Robert enlists separately. He gets his own state."*
9. `invoke ContextFlipper.Flip()`
   *"Robert flips his slot."*
10. `observe ContextFlipper.Robert.value` → `false`
    *"Robert is false."*
11. `observe ContextFlipper.Adi.value` → `true` (unchanged)
    *"And Adi is still true. State is isolated per actor, this is what unlocks parallel execution."*

---

## Demo 3: SDK against public devnet

Working dir: repo root.

1. `npm run deploy`
   *"This deploys the same Flipper manifest, but to MOI's real devnet."*
   Output prints two lines: `Interaction hash: 0x...` and `Logic ID       : 0x...`.
2. Copy the `ix_hash` and paste into <https://voyage.moi.technology>
   *"And there's our interaction on the public explorer, same logic we just ran in CocoLab, now live."*
3. Copy the `Logic ID` into `.env` as `LOGIC_ID=0x...` (or keep it on the clipboard to pass as an argv).
4. `npm run flip`
   *"Same `Flip` endpoint we hit in CocoLab, now over the SDK against devnet. Under the hood: `getLogicDriver(LOGIC_ID, wallet).routines.Flip().send()`."*
5. `npm run mode` → prints `value: true` or `value: false`
   *"And `Mode` reads it back. `routines.Mode().call()`, read-only, nothing is written to the chain, instant."*
   Re-run `npm run flip` then `npm run mode` to show the value toggling.
6. `npm run asset`: **sneak peek of Session 2 (native assets)**
   *"On most chains, launching a token means deploying an ERC-20, wiring approvals, all that ceremony. On MOI, assets are a primitive. Watch."*
   Two SDK calls in one script:
   - `MAS0AssetLogic.create(wallet, 'WEBINAR', 1_000_000, manager, true).send()`: creates the asset, prints the Asset ID.
   - `new MAS0AssetLogic(asset_id, wallet).mint(manager, 100_000).send()`: mints 100k WEBINAR to ourselves.
   *"Two calls, create and mint. No contract, no approvals. That's where we'll pick up in the next session: native assets, transfers, approvals, and what it means for the participant model."*
7. Paste the printed Asset ID into Voyage to show it landed (and the manager balance moved).

### How `.coco` endpoints map to the SDK

| Endpoint kind in `.coco`        | Manifest `kind / mode` | SDK call                                      | CocoLab verb |
| ------------------------------- | ---------------------- | --------------------------------------------- | ------------ |
| `endpoint deploy Init()`        | `deploy / dynamic`     | `factory.deploy('Init').send()`               | `deploy`     |
| `endpoint enlist Init()`        | `enlist / dynamic`     | `driver.routines.Init().send()` *(per actor)* | `enlist`     |
| `endpoint dynamic Flip()`       | `invoke / dynamic`     | `driver.routines.Flip().send()` *(mutates)*   | `invoke`     |
| `endpoint static Mode() -> ...` | `invoke / static`      | `driver.routines.Mode().call()` *(read-only)* | `invoke`     |

### Without `npm run`

`npm run X` just shells the matching `scripts` entry in `package.json`. Plain Node works the same:

```bash
node sdk/deploy.js
node sdk/flip.js                  # or: node sdk/flip.js 0xLOGIC_ID
node sdk/mode.js                  # or: node sdk/mode.js 0xLOGIC_ID
node sdk/asset.js
```

Run from the repo root so `dotenv` finds `.env`. If you must run from elsewhere, use Node's built-in flag: `node --env-file=.env sdk/flip.js`.
