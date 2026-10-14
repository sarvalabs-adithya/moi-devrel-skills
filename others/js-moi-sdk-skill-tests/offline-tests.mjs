// Offline checks of every SDK call the skill examples use, against the installed js-moi-sdk@0.9.0-rc2.
// No interaction is sent: ixData() is called with a pinned sender so no nonce/estimate RPC is needed.
import { MNEMONIC } from "./env.mjs";
import {
  VERSION, Wallet, VoyageProvider, LogicFactory, LogicDriver, getLogicDriver, RoutineOption,
  MAS0AssetLogic, MAS1AssetLogic, MAS2AssetLogic, MASNAssetLogic, AssetFactory, AssetDriver,
  InteractionContext, ParticipantCreate, AccountInherit, StorageDeposit, StorageWithdraw, Access, access,
  OpType, LockType, AssetStandard, AccessAction, ResourceType, KMOI_ASSET_ID, SARGA_ADDRESS, ZERO_ADDRESS,
  DEFAULT_FUEL_PRICE, DEFAULT_FUEL_LIMIT, DEFAULT_STORAGE_FUND, KMOI_DECIMALS, MIN_STORAGE_DEPOSIT_AMOUNT,
  deriveAssetId, deriveLogicId, formatKmoi, parseKmoi, formatAmount, ManifestCoder, ContextStateKind,
  toRawInteractionObject, processInteractionObject, validateAssetCreate, validateAssetAction, AssetId, Identifier,
} from "js-moi-sdk";
import { readFileSync } from "node:fs";
import { Depolorizer, documentEncode } from "js-polo";
import { hexToBytes } from "js-moi-sdk";

const flipper = JSON.parse(readFileSync("./flipper.json", "utf8"));
const taxtoken = JSON.parse(readFileSync("./taxtoken.json", "utf8"));
const results = [];
const check = async (name, fn) => { try { const r = await fn(); results.push(["PASS", name, r ?? ""]); } catch (e) { results.push(["FAIL", name, e?.message ?? String(e)]); } };
const eq = (a, b, m) => { if (a !== b) throw new Error(`${m}: ${String(a)} !== ${String(b)}`); };

const provider = new VoyageProvider("devnet");
const wallet = await Wallet.fromMnemonic(MNEMONIC, "m/44'/6174'/7020'/0/0"); wallet.connect(provider);
const other = await Wallet.fromMnemonic(MNEMONIC, "m/44'/6174'/7020'/0/1"); other.connect(provider);
const me = String(await wallet.getIdentifier());
const bob = String(await other.getIdentifier());
const sender = { id: me, sequence: 7, key_id: 0 };
const sigAlgo = wallet.signingAlgorithms.ecdsa_secp256k1;
const FAKE_LOGIC = deriveLogicId(sender).toHex();
const FAKE_ASSET = deriveAssetId(sender, AssetStandard.MAS0).toHex();

await check("constants", () => { eq(VERSION, "0.9.0-rc2", "VERSION"); eq(DEFAULT_FUEL_PRICE, 50, "price"); eq(DEFAULT_FUEL_LIMIT, 100000, "limit"); eq(DEFAULT_STORAGE_FUND, 10_000_000_000, "fund"); eq(KMOI_DECIMALS, 9, "dec"); eq(AssetStandard.MASN, 65534, "MASN"); eq(OpType.ACCESS_DELETE, 20, "op"); eq(new AssetId(KMOI_ASSET_ID).getStandard(), 65534, "kmoi std"); eq(formatKmoi(1_500_000_000n), "1.5", "fmt"); eq(parseKmoi("0.25"), 250_000_000n, "parse"); return KMOI_ASSET_ID; });

// devnet read-only
await check("devnet getVersion", async () => await provider.getVersion());
await check("devnet getAssetInfoByAssetID(KMOI)", async () => { const i = await provider.getAssetInfoByAssetID(KMOI_ASSET_ID); eq(i.symbol, "KMOI", "symbol"); return `decimals=${i.decimals} supply=${i.max_supply}`; });
await check("devnet getAccountMetaInfo(SARGA)", async () => (await provider.getAccountMetaInfo(SARGA_ADDRESS)).height);
await check("devnet getAccountMetaInfo(me) -> account not found (post-reset)", async () => { try { await provider.getAccountMetaInfo(me); throw new Error("exists"); } catch (e) { eq(e.message ?? e.reason, "account not found", "msg"); return me; } });
await check("devnet getStoragePricing", async () => JSON.stringify(await provider.getStoragePricing()));
await check("devnet getLogicManifest(KMOI, JSON) (asset manifest read)", async () => { const m = await provider.getLogicManifest(KMOI_ASSET_ID, "JSON"); return `kind=${m.kind} elements=${m.elements?.length}`; });

// flipper example: deploy + invoke + static + state
await check("flipper: LogicFactory.deploy('Init') bundles funding transfer to deriveLogicId", async () => {
  const ctx = new LogicFactory(flipper, wallet).deploy("Init");
  const ix = await ctx.ixData({ sender, fuel_limit: 1_000_000 });
  eq(ix.ix_operations.length, 2, "ops"); eq(ix.ix_operations[0].type, OpType.LOGIC_DEPLOY, "op0"); eq(ix.ix_operations[1].type, OpType.ASSET_INVOKE, "op1");
  eq(ix.ix_operations[1].payload.asset_id, KMOI_ASSET_ID, "fund asset"); eq(ix.ix_operations[0].payload.callsite, "Init", "callsite");
  const fund = new Depolorizer(hexToBytes(ix.ix_operations[1].payload.calldata)).depolorize({ kind: "struct", fields: { beneficiary: { kind: "bytes" }, amount: { kind: "integer" } } });
  eq(Buffer.from(fund.beneficiary).toString("hex"), FAKE_LOGIC.slice(2), "fund beneficiary = predicted logic id"); eq(Number(fund.amount), DEFAULT_STORAGE_FUND, "fund amount");
  eq(ix.fuel_price, DEFAULT_FUEL_PRICE, "price default"); eq(ix.participants.length, 0, "sender not listed");
  const signed = await wallet.signInteraction(ix, sigAlgo); return `ix_args ${signed.ix_args.length / 2} bytes, sigs ${signed.signatures.length / 2} bytes`;
});
await check("flipper: deploy() without builder name throws MISSING_ARGUMENT", () => { try { new LogicFactory(flipper, wallet).deploy(); throw new Error("no throw"); } catch (e) { if (!/builder name is required/.test(e.message)) throw e; return e.message; } });
await check("flipper: RoutineOption storageFund override", async () => { const ix = await new LogicFactory(flipper, wallet).deploy("Init", new RoutineOption({ storageFund: parseKmoi("25") })).ixData({ sender }); const fund = new Depolorizer(hexToBytes(ix.ix_operations[1].payload.calldata)).depolorize({ kind: "struct", fields: { beneficiary: { kind: "bytes" }, amount: { kind: "integer" } } }); eq(BigInt(fund.amount), 25_000_000_000n, "25 KMOI"); return String(fund.amount); });
await check("flipper: LogicDriver routines Flip/Get, isMutable, logicState, no actorState", async () => {
  const d = new LogicDriver(FAKE_LOGIC, flipper, wallet);
  eq(d.routines.Flip.isMutable(), true, "flip mutable"); eq(d.routines.Get.isMutable(), false, "get static"); eq(!!d.logicState, true, "logicState"); eq(d.actorState, undefined, "actorState"); eq(d.persistentState, undefined, "persistentState gone");
  const ix = await d.routines.Flip().ixData({ sender, fuel_limit: 60_000 }); eq(ix.ix_operations.length, 1, "one op"); eq(ix.ix_operations[0].payload.logic_id, FAKE_LOGIC, "logic id"); eq(ix.participants.length, 0, "sender not listed (logic id added at serialization)");
  const raw = toRawInteractionObject(structuredClone(ix)); eq(raw.participants.length, 1, "logic auto participant"); eq(raw.participants[0].lock_type, LockType.MUTATE_LOCK, "mutate");
  const [ptr, has] = d.hasLogicState(); return `hasLogicState=${has} ptr=${ptr}`;
});
await check("flipper: decodeOutput('Get') round trip via js-polo documentEncode", () => { const c = new ManifestCoder(flipper); const doc = documentEncode({ value: true }, { kind: "struct", fields: { value: { kind: "bool" } } }); const out = c.decodeOutput("Get", "0x" + Buffer.from(doc.bytes()).toString("hex")); eq(out.value, true, "value"); return JSON.stringify(out); });
await check("manifest: ContextStateKind renamed", () => { eq(ContextStateKind.LogicState, 0, "LogicState"); eq(ContextStateKind.ActorState, 1, "ActorState"); eq(ContextStateKind.PersistentState, undefined, "old gone"); return "ok"; });

// native assets example
await check("MAS0AssetLogic.create(... decimals) bundles funding to deriveAssetId(MAS0)", async () => {
  const ix = await MAS0AssetLogic.create(wallet, "WEBINAR", 1_000_000n, me, true, 0).ixData({ sender, fuel_limit: 200_000 });
  eq(ix.ix_operations.length, 2, "ops"); eq(ix.ix_operations[0].payload.standard, AssetStandard.MAS0, "std"); eq(ix.ix_operations[0].payload.decimals, 0, "decimals");
  const fund = new Depolorizer(hexToBytes(ix.ix_operations[1].payload.calldata)).depolorize({ kind: "struct", fields: { beneficiary: { kind: "bytes" }, amount: { kind: "integer" } } });
  eq(Buffer.from(fund.beneficiary).toString("hex"), FAKE_ASSET.slice(2), "fund -> predicted asset id");
  await wallet.signInteraction(ix, sigAlgo); return FAKE_ASSET;
});
await check("MAS0 create with number supply also serializes", async () => { const ix = await MAS0AssetLogic.create(wallet, "N", 1_000_000, me, true).ixData({ sender }); await wallet.signInteraction(ix, sigAlgo); return "ok"; });
await check("MAS0 create max_supply 0 rejected", async () => { const ix = await MAS0AssetLogic.create(wallet, "Z", 0, me, true).ixData({ sender }); try { await wallet.signInteraction(ix, sigAlgo); throw new Error("no throw"); } catch (e) { if (!/max_supply must be greater than zero/.test(e.message)) throw e; return e.message.slice(0, 80); } });
await check("MAS0 decimals 19 rejected", () => { try { MAS0AssetLogic.create(wallet, "D", 1n, me, true, 19); throw new Error("no throw"); } catch (e) { if (!/decimals/.test(e.message)) throw e; return e.message; } });
await check("MAS0 mint/transfer/lockup/release participants", async () => {
  const a = new MAS0AssetLogic(FAKE_ASSET, wallet);
  const mint = await a.mint(me, 100_000n).ixData({ sender }); eq(mint.ix_operations[0].payload.callsite, "Mint", "mint");
  const lock = await a.lockup(bob, 100n).ixData({ sender }); eq(lock.participants.some(p => p.id === SARGA_ADDRESS && p.lock_type === LockType.MUTATE_LOCK), true, "sarga");
  const rel = await a.release(bob, me, 90n).ixData({ sender }); eq(rel.ix_operations[0].payload.callsite, "Release", "release");
  const tr = await a.transfer(bob, 100n).ixData({ sender }); const raw = toRawInteractionObject(structuredClone(tr)); eq(raw.participants.length, 2, "bob + asset"); eq(raw.participants.find(p => p.lock_type === LockType.NO_LOCK) != null, true, "asset NO_LOCK kept");
  await wallet.signInteraction(tr, sigAlgo); return "ok";
});
await check("MAS0 balanceOf().call() shape is a context; decode schema documented", async () => { const ix = await new MAS0AssetLogic(FAKE_ASSET, wallet).balanceOf(me).ixData({ sender }); eq(ix.ix_operations[0].payload.callsite, "BalanceOf", "cs"); eq(typeof MAS0AssetLogic.prototype.decodeResult, "undefined", "decodeResult is rc3-only"); return "ok"; });
await check("AssetFactory.create(TaxToken, manifest, 'Init', calldata) encodes calldata + funding (MASX)", async () => {
  const id = await wallet.getIdentifier();
  const ix = await AssetFactory.create(wallet, "TaxToken", 1_000_000n, me, true, taxtoken, "Init", id.toBytes(), 500n, 1_000_000n).ixData({ sender, fuel_limit: 2_000_000 });
  eq(ix.ix_operations.length, 2, "ops"); eq(ix.ix_operations[0].payload.standard, AssetStandard.MASX, "MASX"); eq(ix.ix_operations[0].payload.logic_payload.callsite, "Init", "callsite");
  const args = new ManifestCoder(taxtoken).decodeArguments("Init", ix.ix_operations[0].payload.logic_payload.calldata); eq(BigInt(args[1]), 500n, "bps"); eq(BigInt(args[2]), 1_000_000n, "supply");
  const fund = new Depolorizer(hexToBytes(ix.ix_operations[1].payload.calldata)).depolorize({ kind: "struct", fields: { beneficiary: { kind: "bytes" }, amount: { kind: "integer" } } });
  eq(Buffer.from(fund.beneficiary).toString("hex"), deriveAssetId(sender, AssetStandard.MASX).toHex().slice(2), "fund -> predicted MASX id");
  await wallet.signInteraction(ix, sigAlgo); return "ok";
});
await check("AssetFactory.create without callsite throws (manifest has deploy routine)", () => { try { AssetFactory.create(wallet, "T", 1n, me, true, taxtoken); throw new Error("no throw"); } catch (e) { if (!/callsite is required/.test(e.message)) throw e; return e.message.slice(0, 70); } });
await check("AssetFactory.create missing calldata throws", () => { try { AssetFactory.create(wallet, "T", 1n, me, true, taxtoken, "Init", me); throw new Error("no throw"); } catch (e) { if (!/required arguments are missing/.test(e.message)) throw e; return e.message; } });
await check("AssetDriver(taxtoken) routines + logicState, Transfer mutable", () => { const d = new AssetDriver(FAKE_ASSET, taxtoken, wallet); eq(typeof d.routines.Transfer, "function", "Transfer"); eq(d.routines.Transfer.isMutable(), true, "mutable"); eq(!!d.logicState, true, "logicState"); eq(d.persistentState, undefined, "old gone"); return Object.keys(d.routines).join(","); });

// nft example
await check("MAS1AssetLogic.create(signer, symbol, manager, enableEvents) max_supply 1, no decimals", async () => { const ix = await MAS1AssetLogic.create(wallet, "NFT", me, true).ixData({ sender }); eq(ix.ix_operations[0].payload.max_supply, 1, "supply"); eq(ix.ix_operations[0].payload.decimals, undefined, "no decimals"); eq(ix.ix_operations[0].payload.logic_payload.callsite, "Init", "Init"); await wallet.signInteraction(ix, sigAlgo); return "ok"; });
await check("MAS1 transfer(tokenId, beneficiary)", async () => { const ix = await new MAS1AssetLogic(FAKE_ASSET, wallet).transfer(0, bob).ixData({ sender, fuel_limit: 100_000 }); eq(ix.ix_operations[0].payload.callsite, "Transfer", "cs"); await wallet.signInteraction(ix, sigAlgo); return "ok"; });
await check("MAS2 create(... decimals) + transfer(tokenId, to, amount)", async () => { const ix = await MAS2AssetLogic.create(wallet, "SFT", 1000n, me, true, 2).ixData({ sender }); eq(ix.ix_operations[0].payload.decimals, 2, "dec"); const t = await new MAS2AssetLogic(FAKE_ASSET, wallet).transfer(1, bob, 5n).ixData({ sender }); eq(t.ix_operations[0].payload.callsite, "Transfer", "cs"); return "ok"; });
await check("PARTICIPANT_CREATE via InteractionContext (nft example recipient registration) signs", async () => {
  const ctx = new InteractionContext({ opType: OpType.PARTICIPANT_CREATE, payload: { id: bob, keys_payload: [{ public_key: other.getPublicKey(), weight: 1000, signature_algorithm: 0 }], value: { asset_id: KMOI_ASSET_ID, callsite: "Symbol" } }, participants: [{ id: KMOI_ASSET_ID, lock_type: LockType.NO_LOCK }], signer: wallet });
  const ix = await ctx.ixData({ sender, fuel_limit: 200_000 }); await wallet.signInteraction(ix, sigAlgo);
  const b = new ParticipantCreate(wallet).id(bob).addKey(other.getPublicKey(), 1000).value(KMOI_ASSET_ID, bob, 0n).build(); const ix2 = await b.ixData({ sender }); eq(ix2.ix_operations[0].payload.value.callsite, "Transfer", "builder uses Transfer"); return "ok";
});
await check("AccountInherit builder", async () => { const ix = await new AccountInherit(wallet).target(FAKE_LOGIC).index(1).value(KMOI_ASSET_ID, me.slice(0, -8) + "00000001", 1_000_000n).build().ixData({ sender }); eq(ix.ix_operations[0].type, OpType.ACCOUNT_INHERIT, "op"); return "ok"; });

// 0.9.0 features
await check("MASNAssetLogic transfer targets KMOI; no mint", async () => { const m = new MASNAssetLogic(wallet); eq(m.mint, undefined, "no mint"); const ix = await m.transfer(bob, parseKmoi("1.5")).ixData({ sender }); eq(ix.ix_operations[0].payload.asset_id, KMOI_ASSET_ID, "kmoi"); await wallet.signInteraction(ix, sigAlgo); return "ok"; });
await check("KMOI Mint rejected client-side", async () => { const ix = await new MAS0AssetLogic(KMOI_ASSET_ID, wallet).mint(me, 1n).ixData({ sender }); try { await wallet.signInteraction(ix, sigAlgo); throw new Error("no throw"); } catch (e) { if (!/reserved for protocol code/.test(e.message)) throw e; return "rejected"; } });
await check("validateAssetCreate rejects MASN", () => { try { validateAssetCreate({ symbol: "X", standard: AssetStandard.MASN, enable_events: true, manager: me, max_supply: 1 }); throw new Error("no throw"); } catch (e) { if (!/MASN is reserved/.test(e.message)) throw e; return "rejected"; } });
await check("StorageDeposit / StorageWithdraw / Access build + participants", async () => {
  const dep = await new StorageDeposit(wallet).target(FAKE_LOGIC).amount(MIN_STORAGE_DEPOSIT_AMOUNT).build(); const ix = await dep.ixData({ sender }); eq(ix.ix_operations[0].type, OpType.STORAGE_DEPOSIT, "dep"); eq(ix.ix_operations[0].payload.deposit_for, me, "deposit_for defaults to signer");
  const raw = toRawInteractionObject(structuredClone(ix)); eq(raw.participants[0].lock_type, LockType.MUTATE_LOCK, "target mutate"); await wallet.signInteraction(ix, sigAlgo);
  const wd = new StorageWithdraw(wallet).target(FAKE_LOGIC).build(); eq((await wd.ixData({ sender })).ix_operations[0].payload.bytes_to_release, 0, "release all");
  const a = new Access(wallet).storage(FAKE_LOGIC).allow(AccessAction.STORAGE_MUTATE).caller(access.callers(bob)).create(); eq(typeof a.send, "function", "pending op"); eq(a.build, undefined, "no build on access op");
  try { new Access(wallet).storage(FAKE_LOGIC).create(); throw new Error("no throw"); } catch (e) { if (!/at least one action/.test(e.message)) throw e; }
  return "ok";
});
await check("fee payer: payer must be participant; signRawInteractionObject merges; missing payer sig throws", async () => {
  const ctx = new MASNAssetLogic(wallet).transfer(bob, 1n);
  const ix = await ctx.ixData({ sender, payer: bob, fuel_limit: 60_000 }); eq(ix.payer, bob, "payer field (rc2 name)");
  const sigs = await other.signRawInteractionObject(ix, sigAlgo); eq(sigs.length, 1, "one payer sig"); eq(sigs[0].id, bob, "payer id");
  const signed = await wallet.signInteraction(ix, sigAlgo, sigs); 
  const bad = await ctx.ixData({ sender, payer: FAKE_LOGIC }); try { await wallet.signInteraction(bad, sigAlgo); throw new Error("no throw"); } catch (e) { if (!/Payer must be a participant/.test(e.message)) throw e; }
  // gotcha: a non-notary payer is dropped from participants even when it is also a touched account (the beneficiary here)
  const raw = toRawInteractionObject(structuredClone(ix)); eq(raw.participants.some(p => Buffer.from(p.id).toString("hex") === bob.slice(2)), false, "payer-as-beneficiary dropped from participants");
  const notary = toRawInteractionObject(await ctx.ixData({ sender, payer: bob, participants: [{ id: bob, lock_type: LockType.MUTATE_LOCK, notary: true }] })); eq(notary.participants.some(p => Buffer.from(p.id).toString("hex") === bob.slice(2) && p.notary === true), true, "kept when notary");
  // Signer.sendInteraction's "Payer signature is missing." check runs after prepareInteraction (an RPC nonce read), so it cannot be reached offline with a non-existent account.
  return `signatures ${signed.signatures.length / 2} bytes; payer dropped unless notary`;
});
await check("notary payer must be MUTATE_LOCK", async () => { const ix = await new MASNAssetLogic(wallet).transfer(me, 1n).ixData({ sender, payer: bob, participants: [{ id: bob, lock_type: LockType.NO_LOCK, notary: true }] }); try { toRawInteractionObject(ix); throw new Error("no throw"); } catch (e) { if (!/notary payer must hold a mutate lock/.test(e.message)) throw e; return "rejected"; } });
await check("formatAmount / Identifier helpers", () => { eq(formatAmount(1234500n, 4), "123.45", "fmt"); eq(new Identifier(me).getVariant(), 0, "variant"); return "ok"; });

const pad = (s, n) => String(s).padEnd(n);
let fails = 0;
for (const [st, name, info] of results) { if (st === "FAIL") fails++; console.log(`${st}  ${pad(name, 92)} ${String(info).slice(0, 140)}`); }
console.log(`\n${results.length - fails}/${results.length} passed`);
process.exit(fails ? 1 : 0);
