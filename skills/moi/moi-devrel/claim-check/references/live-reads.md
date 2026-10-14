# Live reads: is it live on devnet

Facts are as of 2026-10-04: the results below were recorded on 2 to 4 October 2026, so re-read them on the day you rely on them. Every result marked 2026-10-02 was read between 20:43 and 21:08 UTC and read again from 21:24 to 21:30 UTC with the same answers, from a laptop, with plain `curl` and no account. The commands come from `moi-devrel/references/devnet.md` ("Before you say live"), with the parts that did not work as that file expected corrected here. Back to `../GUIDE.md`.

## Rules
- Read methods only. Never call `moi.SendInteractions` or anything that submits, funds, deploys or creates an account. Never ask the faucet for funds: that writes. Spending devnet funds needs the operator's yes (`../GUIDE.md`, Gates).
- Params go in an array that holds one object: `"params":[{"hash":"..."}]`. The same call with an object, `"params":{"hash":"..."}`, answers `-32602 Invalid Params` (check 4b below). A method with no arguments takes `[]` or `null`.
- Say "devnet", not "Voyage devnet". Write the UTC time of every read in the ledger `source` cell (`date -u +"%Y-%m-%d %H:%M UTC"` right after the read). <!-- slop-lint: ignore -->
- Run the checks again on the day of the post or the call. A devnet reset changes every answer, and the one reset on record after a release followed it by about a day (`devnet.md`).
- Set once: `RPC=https://dev.voyage-rpc.moi.technology/devnet/` and `BAB=https://dev.voyage-rpc.moi.technology/babylon/`.
- If `curl` exits 60, the certificate of that host has expired. It did on 2026-10-04 (read 18:01 UTC) and was renewed (valid 5 October 2026 to 3 January 2027; `moi-devrel/references/devnet.md`), so expect it again after 3 January 2027 unless it is renewed first. Checks 1 to 4 and 7 cannot run. Put that in the ledger `source` cell and leave the row `unverified`; do not call devnet live or down, and do not turn certificate checking off.

## The checks
Result column: what came back on 2026-10-02 (recorded 2 to 4 Oct 2026; re-run on the day).
| # | Question | Command | Result |
|---|---|---|---|
| 1 | Which build does devnet run? | `curl -sS -m 20 -X POST "$RPC" -H 'content-type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"net.Version","params":[]}'` | `{"jsonrpc":"2.0","id":1,"result":"0.13.0"}` at 21:24 UTC |
| 2 | Does the babylon path agree? | the same with `"$BAB"` | `"0.13.0"` at 21:24 UTC |
| 3 | What is the network ID? | the same with `"method":"net.NetworkID"` | Error `-32601`, "the method net.NetworkID does not exist/is not available" at 21:24 UTC, and the same again on 2026-10-03 at 18:45 UTC and in the handover check of 14 October 2026. The docs page `docs.moi.technology/docs/build/json-rpc` documents the method (an integer: 111 Local, 112 Devnet, 113 Babylon; read 2026-10-03) |
| 4 | Which field names does an interaction carry? | `HASH=$(curl -sS -m 20 https://api-voyage.moi.technology/api/interaction \| python3 -c 'import json,sys; print(json.load(sys.stdin)["data"][0]["hash"])')` then `curl -sS -m 20 -X POST "$RPC" -H 'content-type: application/json' -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"moi.InteractionByHash\",\"params\":[{\"hash\":\"$HASH\"}]}" \| python3 -c 'import json,sys; print(sorted(json.load(sys.stdin)["result"].keys()))'` | `['fee_payer', 'fuel_limit', 'fuel_price', 'funds', 'hash', 'ix_index', 'ix_operations', 'ix_participants', 'participants_state', 'sender', 'signatures', 'ts_hash']`. The newest listed interaction was created 2026-10-01 13:29:44 UTC. No `payer` key. Same keys on the babylon path |
| 4b | Does an object in `params` work? | check 4 with `"params":{"hash":"$HASH"}` | `-32602 "Invalid Params"` |
| 5 | Is the fuel floor visible? | `curl -sS -m 20 https://api-voyage.moi.technology/api/interaction \| python3 -c 'import json,sys,collections; d=json.load(sys.stdin)["data"]; print(len(d), collections.Counter(str(r["fuel_price"]) for r in d).most_common(3))'` | `355 [('0x32', 354), ('0x64', 1)]`: 354 of 355 listed interactions carry fuel price 0x32 (50), one carries 0x64 (100), none is below 50 |
| 6 | How far back does the list go? | `curl -sS -m 20 "https://api-voyage.moi.technology/api/interaction?limit=5000" \| python3 -c 'import json,sys,datetime; d=json.load(sys.stdin)["data"]; print(len(d), datetime.datetime.fromtimestamp(int(d[-1]["created_at"]), datetime.timezone.utc))'` (`created_at` is Unix seconds) | `355 2026-09-10 13:18:24+00:00`. `limit` is honoured up to 355 and `page` is ignored, so the list holds at most the 355 newest interactions and its oldest entry is not shown to be the oldest on the chain. A tesseract read by hash (below) gave 13:18:27 UTC for that oldest entry and 13:19:27 UTC for the second oldest |
| 7 | Are `/devnet/` and `/babylon/` one chain? | check 4 on both paths for three different hashes | The results were identical for all three, and a made-up hash failed the same way on both ("error fetching interaction") |
| 8 | Do the other named endpoints answer? | `curl -sS -m 20 -o /dev/null -w "%{http_code}\n" <url>` | https://voyage.moi.technology 200, https://voyage.moi.technology/faucet/ 200, https://voyage-docs.moi.technology 200. `rpc.devnet.moi.technology` does not resolve. `https://voyage-rpc.moi.technology/babylon/v0` timed out after 15 s |
Tesseract by hash, used for check 6: take `ts_hash` from the interaction of check 4 and call `moi.Tesseract` with `"params":[{"with_interactions":false,"with_commit_info":true,"options":{"tesseract_hash":"<ts_hash>"}}]`. `time_stamp` is hexadecimal nanoseconds since 1970.
The explorer list in checks 4 to 7 (`api-voyage.moi.technology/api/interaction`) is the API the explorer page calls itself: the `_app` script of https://voyage.moi.technology names `https://api-voyage.moi.technology/api/` (read 2026-10-02). The research notes do not name it, and it is not a documented interface. If it changes, take a hash from https://voyage.moi.technology in a browser instead.
Check 4c, is a field a feature in use: with `$HASH` from check 4, `curl -sS -m 20 -X POST "$RPC" -H 'content-type: application/json' -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"moi.InteractionByHash\",\"params\":[{\"hash\":\"$HASH\"}]}" \| python3 -c 'import json,sys; r=json.load(sys.stdin)["result"]; print(set(r["fee_payer"][2:]) == {"0"})'` prints True for an interaction nobody sponsored. All 346 of the 355 listed interactions that answered were True on 2026-10-02 (9 did not answer).

## Reading the answers
| Observation | Meaning |
|---|---|
| `net.Version` equals the release | The node build is that release. It does not say when it arrived |
| An interaction has `fee_payer` and no `payer` | The build knows fee delegation. `payer` was the older build (devnet on 2026-09-10) |
| A key the claim needs is missing, or a method answers `-32601` | An older build, or not shipped. Do not write "live" |
| Fuel price of every listed interaction is at or above the floor | Consistent with the floor. It does not prove the node rejects lower prices |
| A key is present | The field exists. It does not show that anyone used it. An interaction nobody sponsored carries an all-zero `fee_payer` (check 4c), so a `fee_payer` that differs from `sender.id` proves nothing. A sponsored one carries a non-zero id. No listed interaction was sponsored on 2026-10-02 |
| A hash from before the reset is not found | The chain was wiped. Do not use an old hash as a fixture |
| A balance or supply read in base units | Divide by 10 to the power of the asset's `decimals`. The asset reports it (`moi.AssetInfoByAssetID`, and the MCP read tool `moi_get_asset`): 9 for KMOI on 2026-10-03, so 1 KMOI is 1,000,000,000 base units (`moi-devrel/references/devnet.md`). Read it, do not assume it |
What a read cannot show, and the fix:
- "Since 11 September": a read shows now. Cite the announcement's time as the protocol team gave it, name who confirmed it, or write "now live". The explorer's oldest listed interaction is dated 2026-09-10 13:18 UTC, before the 00:00 UTC on 2026-09-11 that `devnet.md` records for the upgrade. The go-moi `v0.13.0` tag commit is dated 2026-09-10 07:20 UTC (read 2026-10-02 in a clone), so a devnet started on that build the same afternoon would fit (inferred, not shown). ASK: Gokul when the devnet was re-initialised.
- "A user can do X": that needs a real interaction. It spends funds and is a gate. Ask the operator, and say in the text what was simulated.
- A claim about the explorer, faucet or docs pages: open the page.

## Writing it down
A ledger row for a live claim, as filled for `../examples/september-release/ledger.csv` row C002:
```
source: net.Version = 0.13.0 on /devnet/ and /babylon/, read 2026-10-02 21:24 UTC (references/live-reads.md checks 1 and 2)
verdict: unverified, note: the sentence names no network, and a read proves now, not since. Proposed: "moipod v0.13.0 is live on devnet."
```
The verdict is `verified` for "live on devnet" once check 1 (the version) is in the `source` cell, plus check 4 when the claim is about a feature, and the sentence has no "since". For a feature, check 4 shows the build carries the field and check 4c shows whether anyone has used it. "Fee delegation works on devnet" needs a real interaction with a sponsor: a gate, so the row stays `unverified` until the operator says yes and the result is in `source`. "Live" with a date range stays `unverified` until the protocol team confirms the date.

## Not yet known
- Why `net.NetworkID` does not exist on the running build (0.13.0) when the docs page documents it and `devnet.md` expected 112 from it. The page may describe an unreleased build, or the method was renamed. ASK: Gokul. Do not publish a network ID.
- Why the oldest listed interaction is dated 2026-09-10 13:18 UTC, and whether the explorer list is capped (it returned 355 entries for every `limit` from 355 to 5000). A re-initialisation before the scheduled moment, a cap, or a different meaning of "00:00 UTC on 11 September". ASK: Gokul.
- Whether `/babylon/` and `/devnet/` are the same chain. Three hashes were identical on both, which is consistent with one chain and is not proof. ASK: Gokul.
- Whether a faucet still funds 20K or 100K KMOI (`devnet.md` quotes both). Not read: a faucet call writes.
