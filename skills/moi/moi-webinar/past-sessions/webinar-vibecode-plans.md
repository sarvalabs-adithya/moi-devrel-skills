# MOI Builders: vibecode every session from prompts (skills-only)

> **What this is:** a planning document for an idea: run MOI Builders sessions 1 to 5 by *vibecoding* them live, meaning the presenter builds each session's contract and client by prompting an AI coding agent that has only two skill folders to work from, instead of presenting prewritten code. MOI Builders is the developer webinar series DevRel runs.
>
> **Status:** plan, not delivered as written. The sessions that were actually held used prewritten code in https://github.com/moi-foundation/MOI-Webinars (see `OVERVIEW.md`, `session-1-cheatsheet.md`, `session-4-DEMO.md` in this folder). The notes do not say when this plan was written or whether any session was run this way.
>
> **Where the pieces are:** the two skills named below are agent-skill packages, not folders of this repo. `coco-skills` is the Coco language skill (source in `sarvalabs/cocolang`, shipped as a zip on MOI's CDN) and `js-moi-sdk-skills` is the SDK skill (zip published with each `js-moi-sdk` release); both are described in `project-handover-docs/AGENT-SKILLS.md`. The `verify-sdk.cjs` script is part of `js-moi-sdk-skills`. Paths below such as `examples/flipper.coco`, `standards/mas0/mas0.coco` and `reference/13-common-patterns.md` are inside the Coco skill; `logic.md`, `assets.md` and `patterns.md` are inside the SDK skill.
>
> **Where this plan differs from what was delivered (not reconciled, because the plan was never run):**
> - Session 1: the plan's Flipper starts at `false` with a `Get` endpoint; the delivered cheat sheet's Flipper starts at `true` (`Init` sets the sender's slot to `true`) and reads with `Mode`.
> - Session 2: the plan uses a token `TKA` and a fee of 100 basis points (1%); `OVERVIEW.md` has a `WEBINAR` token and a 5% `TaxToken`. Which is right for the held session is not settled in these notes (the held session was Friday 12 June 2026 per `session-history.md`).
> - Session 3: the plan builds a toy `AgentRegistry` contract; the delivered session used MOI's existing on-chain agent registry through `js-moi-agent-registry`.
> - Session 4: the plan swaps 100 TKA for 100 TKB with bigint amounts and calls it "atomic-ish"; `session-4-DEMO.md` swaps 100 TKA for 90 TKB, uses plain numbers (bigint broke signing) and says plainly that the swap is not atomic.
>
> **Terms:** *Coco*: MOI's contract language. *Logic*: a deployed Coco program. *Fuel*: what running an interaction (MOI's word for a transaction) costs; `fuel_limit` caps it. *KMOI*: the native token of the MOI network, which pays fuel. *MAS0 / MAS1*: the native standards for fungible tokens and NFTs. *MASX / logic-backed asset*: a custom asset whose behavior is written in Coco. *Basis points (bps)*: hundredths of a percent. *SARGA*: named in these notes only as the thing that "escrows" a lockup; not defined here. *getTDU*: an SDK call used to check who owns a token; not explained in these notes. *Bounty*: a reward for viewers who complete the session task and submit proof. *OpenClaw*: a third-party AI agent framework (see `OVERVIEW.md`). *Voyage*: MOI's explorer and faucet; *devnet* is the public test network.

**The demo premise:** the repo starts with **nothing but two skill folders**:
`coco-skills/` (write + compile Coco contracts) and `js-moi-sdk-skills/` (deploy
+ drive them from JS). No contracts, no scripts, no manifests. You build each
session's **contract AND client live, entirely by talking.** The two skills
compose: Coco skill → `.coco` source → `coco compile` → manifest; SDK skill →
deploy that manifest → call routines → read state.

```
demo-repo/
├── coco-skills/          ← Coco language skill (only thing here at start)
└── js-moi-sdk-skills/    ← SDK skill (only thing here at start)
```

Everything else, the agent writes from prompts.

**Setup, said once:** Voyage devnet (`new VoyageProvider("devnet")`), funded
12-word mnemonic (a devnet test wallet), `coco` toolchain + Node 20. Skills installed. Optional trust
beat: `node js-moi-sdk-skills/scripts/verify-sdk.cjs ~/js-moi-sdk` (a local clone of the SDK repo) → **55/55** checks.

**The rhythm each session:** ① prompt the Coco contract → ② prompt "compile it"
→ ③ prompt the SDK deploy+interact script → ④ run on devnet → ⑤ make one teaching point.
The story is never the code, it's that **you spoke English and got a working
on-chain dapp, contract and client, from an empty repo.**

---

## Session 1: Flipper (fundamentals, the full stack in miniature)

**Build from zero:** a stateful Flipper contract + a script that deploys, flips,
and reads it. (Coco skill has `examples/flipper.coco` as the reference.)

**Prompts, in order:**
1. > Read the coco-skills. Write a Flipper contract: one boolean logic-state
     field, a deploy endpoint that sets it false, a dynamic Flip endpoint that
     toggles it, and a static Get endpoint that returns it.
2. > Compile it with `coco compile` and show me the manifest it produced.
3. > Now read js-moi-sdk-skills. Write a script that loads my wallet on Voyage
     devnet, deploys that manifest, calls Flip, and prints the value before and
     after. Cap fuel to my balance and verify the deploy returned a logic_id.

**Coco half the agent writes (from `flipper.coco` pattern):**
```coco
coco Flipper
state logic:
    value Bool
endpoint deploy Init():
    mutate false -> Flipper.Logic.value
endpoint dynamic Flip():
    mutate v <- Flipper.Logic.value:
        v = !v
endpoint static Get() -> (value Bool):
    observe value <- Flipper.Logic.value
```

**SDK half (from `logic.md`):**
```js
const factory = new LogicFactory(manifest, wallet);   // parsed compiled manifest
const { logic_id } = await (await factory.deploy("Init").send({ fuel_limit })).result();
if (!logic_id) throw new Error("committed but no logic_id");
const driver = await getLogicDriver(logic_id, wallet);
const before = await driver.persistentState.get(b => b.entity("value"));
await (await driver.routines.Flip().send({ fuel_limit: 20000 })).wait(60);
const after  = await driver.persistentState.get(b => b.entity("value"));
```

**The one point to make:** "Empty repo → a deployed contract I flip on-chain, in two
prompts. The Coco skill knew logic-state + observe/mutate; the SDK skill knew
deploy→driver→state, and that committed isn't created."

---

## Session 2: Native Assets: MAS0 + fee-on-transfer TaxToken  **(bounty)**

**Build from zero:** mint a plain MAS0 token (SDK-native), then write + compile a
**TaxToken** Coco asset that skims a fee on transfer, deploy it as a logic-backed
asset. **Bounty:** submit both asset IDs.
(Coco skill: `standards/mas0/mas0.coco`, `examples/asset_token.coco`.)

**Prompts:**
1. > With js-moi-sdk, create a MAS0 token "TKA", 1,000,000 supply, me as
     manager, events on. Print the asset ID, then mint 500 more to myself.
2. > Read coco-skills. Write a TaxToken: a MAS0-style fungible asset where
     Transfer sends amount minus a fee (in basis points, set at deploy) and
     routes the fee to the manager. Compile it.
3. > With js-moi-sdk, deploy that TaxToken as a logic-backed asset (symbol TAX,
     supply 1,000,000, feeBps 100) and print its asset ID.

**SDK half (from `assets.md`):**
```js
const tka = await MAS0AssetLogic.newAsset(wallet, "TKA", 1_000_000n, me, true);
await new MAS0AssetLogic(tkaId, wallet).mint(me, 500n).send({ fuel_limit });
// logic-backed / MASX asset with the compiled TaxToken manifest:
const ix = AssetFactory.create(wallet, "TAX", 1_000_000n, me, true, taxManifest, "Deploy", 100n);
const taxResp = await ix.send({ fuel_limit });
```

**The one point to make:** "A native token in one line, then a *custom* token whose
transfer logic I wrote in Coco, deployed as a first-class asset. The SDK skill
knew `newAsset` for the simple case and `AssetFactory` + manifest for the
logic-backed one."

**Bounty:** capture TKA id + TAX id → Session 2 form.

---

## Session 3: On-chain Agent Registry  **(bounty)** *(agent track: contract only)*

> The **OpenClaw agent runtime** is a separate track, don't vibecode the whole
> agent live. Vibecode the **registry contract + its client** with the skills;
> narrate that OpenClaw calls these same SDK functions inside a plugin tool.

**Build from zero:** a CRUD Agent Registry (classes, map, events) + a script to
register and list agents. (Coco skill: `examples/crud_registry.coco`.)

**Prompts:**
1. > Read coco-skills. Write an AgentRegistry: an Agent class (name String,
     endpoint String, owner Identifier), a logic-state map from id→Agent, a
     dynamic Register endpoint that adds one and emits AgentRegistered, and a
     static Get by id. Compile it.
2. > With js-moi-sdk, deploy the registry and print its logic_id.
3. > Register my agent ("agent-38", its endpoint), then list all registered
     agents by decoding the AgentRegistered events.

**SDK half (from `logic.md` + `patterns.md`):**
```js
const driver = await getLogicDriver(registryId, wallet);
await (await driver.routines.Register("agent-38", endpoint).send({ fuel_limit })).wait(60);
// events decode from log.data, NOT topics:
const logs = await provider.getLogs({ id: registryId, height: [0, head], topics: [] });
const evt  = coder.decodeEventOutput("AgentRegistered", logs[0].data);
```

**The one point to make:** "The registry contract and its client, both from prompts.
The Coco skill knew classes + maps + `emit`; the SDK skill knew events decode
from the data document, not the topic hashes. OpenClaw just runs this same code
inside an agent."

**Bounty:** register via OpenClaw → submit the result on the session's Google Form.

---

## Session 4: Account-to-account swap: Lockup + Release  **(bounty)**

**Build from zero:** two tokens, two wallets, a swap that is "atomic-ish" (the legs are not guaranteed to execute together; see `session-4-DEMO.md`) using MAS0
`Lockup`/`Release`. Mostly SDK, the tokens can be plain MAS0, so little/no Coco
needed (or write a custom swap-escrow logic if you want a Coco half).
**Bounty:** asset IDs + a swap tx hash.
(Coco skill: `reference/13-common-patterns.md` swap section, if you go custom.)

**Prompts:**
1. > With js-moi-sdk on Voyage devnet, load two wallets from
     VITE_ALICE_MNEMONIC and VITE_BOB_MNEMONIC.
2. > Create TKA owned by Alice and TKB owned by Bob, 1,000,000 each. Print both
     asset IDs.
3. > Swap: Alice locks up 100 TKA for Bob, Bob locks up 100 TKB for Alice, then
     release both legs. Serialize each wallet's sends so their nonces don't
     collide, cap fuel per wallet, and print the swap tx hashes + final
     balances.

**SDK half (from `assets.md` + `patterns.md`):**
```js
const a = await new MAS0AssetLogic(tka, alice).lockup(bobAddr,   100n).send({ fuel_limit });
const b = await new MAS0AssetLogic(tkb, bob  ).lockup(aliceAddr, 100n).send({ fuel_limit });
await new MAS0AssetLogic(tka, alice).release(aliceAddr, bobAddr,   100n).send({ fuel_limit });
await new MAS0AssetLogic(tkb, bob  ).release(bobAddr,   aliceAddr, 100n).send({ fuel_limit });
```

**The one point to make:** "Two-sided value swap, no custom contract needed, the
SDK skill knew `lockup` sets the funds aside (the original notes say "escrows via SARGA", a term they do not define), the `release(benefactor, beneficiary,
amount)` arg order, and to serialize each signer's sends so the two wallets
don't self-collide on nonce."

**Bounty:** TKA/TKB ids + one swap `resp.hash` → Session 4 form.

---

## Session 5: NFT Marketplace: MAS1 mint + transfer + UI

**Build from zero:** a MAS1 NFT collection in Coco, SDK scripts that deploy +
mint + transfer on devnet, and a minimal web UI that drives the same flow.
(Coco skill: `standards/mas1/mas1.coco`. SDK skill: `assets.md` + `AssetFactory`.)

**Prompts, in order:**
1. > Read coco-skills. Write a MAS1 NFT collection: manager-gated Mint with
     name + image_uri metadata at mint time, Transfer by token_id, Init that
     zeroes a token counter, and static getters for name/uri. Compile it.
2. > With js-moi-sdk, deploy the manifest via AssetFactory (Init at create),
     mint one NFT to my wallet, print asset_id and token_id. Cap fuel to KMOI.
3. > Add a transfer script: read the saved deployment state, transfer token #0
     to a recipient address, verify ownership moved via getTDU.
4. > Add a minimal Express UI, Mint button and Transfer form that shell out to
     those SDK scripts.

**Coco half (from `mas1.coco` pattern):**
```coco
coco asset MAS1
endpoint deploy Init():
    set_token_count(token_count: 0)
endpoint dynamic Mint(beneficiary Identifier, name String, image_uri String) -> (token_id U64):
    RequireManager()
    asset.MintWithMetadata(token_id: new_token_id, beneficiary, amount: U256(1), static_metadata: meta)
endpoint Transfer(token_id U64, beneficiary Identifier):
    asset.Transfer(token_id, beneficiary, amount: U256(1))
```

**SDK half (from `assets.md`):**
```js
const createIx = AssetFactory.create(wallet, "ART", 10_000, owner, true, manifest, "Init");
const { asset_id } = (await (await createIx.send({ fuel_limit })).result())[0];
const driver = await getAssetDriver(asset_id, wallet);
await (await driver.routines.Mint(owner, name, uri).send({ fuel_limit })).wait(120);
await new MAS1AssetLogic(asset_id, wallet).transfer(tokenId, recipient).send({ fuel_limit });
```

**The one point to make:** "Flipper taught logic, Session 2 taught fungible assets,
Session 4 taught two-sided value, Session 5 is a product-shaped NFT dapp:
Coco asset + SDK + UI, all vibecoded from prompts."

---

## The webinar one-slide summary

| Session | Coco skill writes | SDK skill writes | You just say |
|---|---|---|---|
| 1 Flipper | bool logic-state + Flip/Get | deploy → flip → read | "make it, flip it, read it" |
| 2 Assets | fee-on-transfer TaxToken | newAsset + AssetFactory | "mint a token, then a tax token" |
| 3 Registry | Agent class + map + events | deploy → register → list | "registry, register, list" *(agent glue = OpenClaw)* |
| 4 Swap | (optional escrow logic) | lockup → release ×2 | "lock both sides, release" |
| 5 NFT | MAS1 collection + metadata | AssetFactory → mint → transfer + UI | "mint an NFT, transfer it" |

**The through-line:** an empty repo with two skills becomes five working MOI
dapps, contract + client, built entirely by describing them.

---

## Prep before rehearsing (skills-only demo)

- [ ] `coco` toolchain installed and `coco compile` works, test Flipper end to
      end once (write → compile → deploy → flip) so the compile step is smooth.
- [ ] **Manifest handoff confirmed:** be sure how the compiled manifest lands (JSON
      vs YAML) and that the SDK loads it into `LogicFactory` / `AssetFactory`
      (`ManifestCoderFormat` supports JSON + YAML). Parse-and-pass, verified live.
- [ ] Voyage devnet wallet(s) funded, one for 1 to 3, **two** for session 4.
- [ ] Run each session's prompt chain once beforehand; agents are
      non-deterministic, lock the wording that yields clean code.
- [ ] **Backup screen recording** of all five, contract + client, ready to cut to.
- [ ] Anything new from Coco's Discord folded into the SDK skill and re-verified (the original line does not say which additions).
- [ ] Session 3: keep OpenClaw agent runtime OUT of the live vibecode, narrate it.
