# Devnet: what to know before you say anything is "live"

Facts are as of 2026-10-02 unless dated; reads of 2026-10-03 carry their time. The full redo list per product is the skill `moi-devnet-reset`. Back to `../SKILL.md`.

## The rule
- Say "devnet". Do not say "Voyage devnet" (Voyage is the explorer and faucet product) or "Indus" (another network name the explorer lists). The previous operator corrected both: on 2026-09-25 "it's not called Voyage devnet, just say went live on devnet". <!-- slop-lint:ignore -->
- Say "network ID". Do not say "chain ID" (`terminology.md`). <!-- slop-lint: ignore -->
- Write "live on devnet" only after the checks in "Before you say live".

## Network IDs
`FIX-PLAN.md` was the previous operator's file. It is not in git or in the handover repo (not recorded elsewhere; the previous DevRel's notes), so what it said is copied into this table.
| ID | Name in the documents | Where it is written |
|---|---|---|
| 111 | "local" in `FIX-PLAN.md` (2026-10-01) and in the public docs; TEST_NET in the SDK `Chain` enum | `FIX-PLAN.md`; the `Chain` enum in js-moi-sdk (`origin/main` read 2026-10-03) |
| 112 | "devnet"; DEV_NET | The two above, the public docs, and the 2026-09-10 audit: the node's internal NetworkID for devnet is 112 |
| 113 | "Babylon" in `FIX-PLAN.md` and in the public docs; MAIN_NET in the SDK enum | The sources disagree on the label <!-- slop-lint: ignore --> |
- The public docs page https://docs.moi.technology/docs/build/json-rpc (read 2026-10-03 18:10 UTC) documents `net.NetworkID`: no parameters, an integer result, a table of 111 Local, 112 Devnet and 113 Babylon, and an example answer of 112. The node does not agree, and it still did not on 14 October 2026. Read-only, 2026-10-03 18:10 UTC: `curl -s -X POST https://dev.voyage-rpc.moi.technology/devnet/ -H 'content-type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"net.NetworkID","params":[]}'` answered error -32601, "the method net.NetworkID does not exist/is not available", and so did `/babylon/`. `net.Version` answered 0.13.0 on both. The same docs page shows `net.Version` as 0.11.1 in its example, so its examples come from an older build. The documented method is therefore not on the running build, or the page describes a build that has not shipped. Do not publish a network ID from either source. ASK: Gokul. <!-- slop-lint: ignore -->
- The public docs table and `FIX-PLAN.md` give the same three labels. The SDK enum labels 111 and 113 differently (TEST_NET, MAIN_NET). Only 112 agrees across all three sources. Treat the 111 and 113 labels as unconfirmed. ASK: Gokul.
- Babylon: `x402-compat/x402.md` (MOI-Webinars) calls it a retired network that the Voyage explorer still names. The public Voyage post of 2026-08-27 (blog.moi.technology, "Move your Voyage login to MOI Wallet") says the network is now called Devnet in the selector and in URLs and that old links containing babylon will not resolve. The Voyage-hosted MCP read gateway still uses the `/babylon/` RPC path, which answered `net.Version` 0.13.0 on 2026-10-02 and 2026-10-03. Whether `/babylon/` and `/devnet/` are the same chain is unknown (three interactions read the same on both on 2026-10-02: `moi-devrel/claim-check/references/live-reads.md`). ASK: Gokul. <!-- slop-lint: ignore -->
- The CAIP-2 reference for MOI is undecided between `moi:devnet`, `moi:112` and `moi:14` (the string MOI Wallet and `wallet-connect-dapp` use for devnet). They are candidates, not ids any docs page names. Do not publish any of them as final. ASK: Rahul.

## Endpoints the research names
| What | URL | Note |
|---|---|---|
| JSON-RPC, devnet | https://dev.voyage-rpc.moi.technology/devnet/ | `net.Version` returned 0.13.0 on 2026-10-02 and again on 2026-10-03 at 18:10 UTC. Its certificate expired on 2026-10-04 and was renewed (below) |
| JSON-RPC, babylon path | https://dev.voyage-rpc.moi.technology/babylon/ | Also 0.13.0 on both dates. Used by the hosted MCP read gateway. Same certificate as `/devnet/` (below) |
| Explorer | https://voyage.moi.technology | Verify hashes here. It can lag by minutes |
| Faucet | https://voyage.moi.technology/faucet/ | Funds only accounts that already exist on chain: register on chain first, then fund (Voyage post of 2026-08-27). The Faucet API page of voyage-docs (read 2026-10-03) says a faucet token from the Voyage dashboard goes in the URL path, an account can claim once per fixed cooldown, and an invalid token or an exceeded limit returns an error. It states no amount. The public moi-mcp deploy checklist says about 20,000 KMOI (read 2026-10-03) and other notes say 100K. ASK: Gokul. A claim writes, so never make one without the operator's yes |
| Voyage docs | https://voyage-docs.moi.technology | JSON-RPC, faucet, wallet sign-in |
| SDK default | `new VoyageProvider('devnet')` | Webinar code never hardcodes the URL |
| Launchpad variable example | `https://rpc.devnet.moi.technology` | Did not answer from the research machine. The Launchpad ignores a URL containing "voyage" or "devnet" in `MOI_RPC_URL` |
| Old README link | `https://voyage-rpc.moi.technology/babylon/v0` | In the js-sdk section of the uncommitted Forge onboarding README (`awesome-moi/resources/moi-sprint/README.md`, local to the previous operator's machine and not recorded elsewhere; MOI Sprint was scratched 13 October 2026). Probably stale |

Certificate. Read 2026-10-04 18:01 UTC with `openssl s_client`: the TLS certificate of dev.voyage-rpc.moi.technology had expired (notBefore 2026-07-06 05:57:06 GMT, notAfter 2026-10-04 05:57:05 GMT, issuer Let's Encrypt), and `curl` exited 60 on `/devnet/` and on `/babylon/`. It was renewed: the new certificate is valid from 5 October 2026 to 3 January 2027, and `net.Version` answers 0.13.0 again. If `curl` exits 60 again, the certificate has lapsed again and every read of the RPC in this file fails verification until it is renewed. The same read the same day found api-voyage.moi.technology, mcp-read.voyage.moi.technology, voyage.moi.technology and docs.moi.technology valid until December 2026. An expired certificate says nothing about a reset or about the build. Renew before 3 January 2027: ASK: Upendhar (TLS), then Gokul.

## Before you say "live"
1. Version: `curl -s -X POST https://dev.voyage-rpc.moi.technology/devnet/ -H 'content-type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"net.Version","params":[]}'`. Compare with the release. Both paths read 0.13.0 on 2026-10-02 and on 2026-10-03. If `curl` exits 60 (as on 2026-10-04 18:01 UTC, before the renewal), the certificate has expired: write that as the finding, do not call devnet live or down, and do not switch certificate checking off to get an answer.
2. Network ID: the call above with `net.NetworkID`. The docs promise 112; the running build answered -32601 on 2026-10-03 and again on 14 October 2026. Write down what you get and publish no ID.
3. Field names on the wire: fetch a recent interaction with `moi.InteractionByHash` and read the keys (the full command is check 4 in `moi-devrel/claim-check/references/live-reads.md`). `payer` is an older build, `fee_payer` the one that carries fee delegation. On 2026-09-10 devnet still answered `payer` and `net.Version` 0.12.0 while the source tip already had `fee_payer`. On 2026-10-03 18:10 UTC an interaction read from `/devnet/` carried `fee_payer` and no `payer`, and its `fee_payer` was all zeros, which is what an unsponsored interaction carries. The docs Interactions page (read 2026-10-03) still names the optional submission field `payer`, which defaults to the sender. Which name a submission accepts has not been read. ASK: Gokul.
4. Constants come from the SDK, never from a literal: KMOI asset id (the release moved it to the MASN standard), the fuel price floor (50 as of v0.13.0), the default storage fund (raised 10,000 times at v0.13.0), the minimum grant when creating a participant (1 KMOI measured in September). The SDK names are `KMOI_ASSET_ID` and `DEFAULT_FUEL_PRICE`. On 2026-10-03 18:11 UTC the id that js-moi-sdk exports as `KMOI_ASSET_ID` (`origin/main` of the clone) was the id devnet returned as symbol KMOI through `moi.AssetInfoByAssetID`, and it is the id the public moi-mcp deploy checklist uses, so that id is not stale. The older id in the docs JSON-RPC example answered "account not found". Read the asset before you call an id stale.
   Decimals: `moi.AssetInfoByAssetID` returns `decimals` for an asset. It was 9 for KMOI on 2026-10-03, so 1 KMOI is 1,000,000,000 anu and `max_supply` read 10^19 base units, which is 10,000,000,000 KMOI. Read `decimals` from the asset instead of assuming it, and convert with the SDK helpers (`glossary.md`, anu).
5. A feature found only in the go-moi `develop` tip or only in release notes is "planned" until steps 1 to 3 show it.
6. If any step of a demo is simulated, say so in the text.

## The build-lag trap
The network can run an older build than the release notes or the source describe. v0.13.0 was tagged 2026-09-10 and reached devnet with the upgrade announced for 00:00 UTC on 2026-09-11 (not confirmed to the minute; see the reset history). The intro-session deck (now in the handover repo, `skills/moi/moi-webinar/past-sessions/intro-session-deck/`; re-read it before reuse) carried "Since v0.13.0 someone else can pay that fuel for you", flagged on 2026-09-15 when devnet ran the older build. For community call 14 the same caution was raised on 15, 23 and 25 September, and the previous operator chose the wording "went live on devnet". A claim in a spec, deck or post that a facilitator or developer can act on must be tested against devnet. Passing against the source tip does not count.

## Reset history
| Date (UTC) | What happened | Lag in products |
|---|---|---|
| 2026-08-06 | A registry failure without a wipe: `b97ce717` stopped executing writes but still served reads. Registrations hung about 127 seconds, unnoticed for four days | |
| 2026-08-10 | Registry replaced by `f5b0c7af` | |
| 2026-08-13 | Registry replaced by `09ce50ba` | |
| 2026-08-15, about 23:38 | Full wipe. New registry `c684f926`, agents re-imported | |
| 2026-09-11 (announced for 00:00 UTC; not confirmed to the minute: the explorer's oldest listed interaction is dated 2026-09-10 13:18 UTC and its list is capped at 355 entries, ASK: Gokul) | The moipod v0.13.0 upgrade wiped devnet and killed `c684f926`. MOI redeployed the registry as `2f3e9469`, importing an old snapshot (144 agents, 1 of 11 listed agents carried over) | Launchpad moved 09-15 12:21 UTC (users could not onboard for three days), Explorer 09-22, MCP pinned 09-23 but not deployed until 10-14 |
Five events in just over five weeks, two of them full wipes. Earlier resets before August are not catalogued. A reset follows a go-moi release by about a day (one observation; ASK: Gokul).

## What a reset breaks
| Where | Breaks |
|---|---|
| Everywhere | Accounts, assets, contracts, registrations, test wallets, faucet-funded balances |
| Launchpad | Registry id, AgentMarket contract id, KMOI asset id, the three registration wallets, the platform wallet, every user wallet. Agents registered earlier show "need registering again" |
| Explorer | Registry id (in `server/src/config.ts`; the client pin in `client/vite.config.ts` came with PR #5, merged 2026-10-07), read-caller address, intelligence logic id, node WebSocket address. Nothing deletes old rows: no DELETE, TRUNCATE or DROP statement is in the server code on `main` or in PR #5 (clone read 2026-10-03, before the merge). Whether that is intended: ASK: Gokul |
| MCP | Registry id, `MOI_READ_CALLER`, the canary account |
| Webinar and demo repos | Deployed assets and logics, session agent ids. Run the demo's preflight first |
| Docs and Drive | Text that names ids, `moi:devnet` versus `moi:112`, and model wording corrected on 2026-09-14. Grep every copy after a change |
Three repos pin the registry id separately. After the wipe of about 2026-09-11 they moved 4 days later (Launchpad, 09-15), 11 days later (Explorer, 09-22) and 12 days later (MCP, 09-23). `js-moi-agent-registry` embeds an old id and reads the override once at load.

## Signs of a reset, earliest first
1. A go-moi release: the upstream watch opens "Upstream release: go-moi <tag>".
2. A message from the protocol team (Gokul) with a new registry id and package version. Channel unknown.
3. The nightly canary opens "Chain canary failing".
4. Launchpad `/api/stats` shows `unreachable` or `stale` with "account not found".
5. A user reports "account not found".

## First hour after a reset
Use the skill `moi-devnet-reset`. Its first five minutes are `moi-devnet-reset/references/detect.md` (read-only: confirm the wipe with `net.Version`, the wire field names and a registry read). Every step after that which sends a message, sets a variable, deploys or spends devnet funds is a gate, and Claude never handles a recovery phrase (`consent-and-identity.md` section 5).

## Silent failures on devnet
- A funded wallet on the wrong derivation path gives "account not found". Faucet wallets use `m/44'/6174'/7020'/0/0`, SDK-only wallets `m/44'/6174'/0'/0/N`, the Launchpad registration default is `m/44'/6174'/1'/0/0`.
- Simulation accepts what the chain later refuses. Read the receipt status. A broadcast acknowledgement does not prove success.
- A stuck interaction blocks a wallet. Replace the pending sequence with a new interaction at the same nonce and enough fuel.
- The registry call `getAllAgentIds` reverts at about 135 agents and returns an empty list.
- The faucet funds only accounts that already exist on chain. A new wallet shows "account does not exist" until it is registered, then the faucet works. A student-facing step list needs that order.
- Seed words read out on a screen share end up in Gemini transcripts (seen 2026-09-24). Never read or confirm a recovery phrase on a recorded call.

## Not yet known
- Why the running build answers -32601 for `net.NetworkID` while the docs document it, whether `/babylon/` and `/devnet/` are one chain, and what network 113 is. ASK: Gokul.
- Which field name a submitted interaction takes for the fee payer (`payer` in the docs, `fee_payer` on reads). ASK: Gokul.
- Why the certificate of dev.voyage-rpc.moi.technology lapsed on 2026-10-04 (05:57:05 GMT), and who renews it before 3 January 2027. ASK: Upendhar.
- The faucet amount, and where the protocol team announces a reset and a new registry id. Whether the AgentMarket contract was redeployed after 2026-09-11. ASK: Gokul.
