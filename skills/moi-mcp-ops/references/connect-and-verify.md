# Connect a client and prove each class of tool

Run this after every production deploy and when onboarding a new user. Reads come first and cost nothing. Anything that signs or spends is a GATE and is done by the operator's own wallet on the operator's phone. Facts are as of 2026-10-02 (research) and 2026-10-03 (live reads). A recorded, repeatable pass with a plan and a log is the branch `moi-devrel/test-round`; its case list for this connector is `moi-devrel/test-round/references/mcp-pass.md`. Back to `../SKILL.md`.

**Column "Who".** `Claude` runs a read-only command. `Operator` means the operator does it in their own claude.ai and wallet; Claude explains and checks the result. These steps write only the operator's own connector, sign-in and pairing records, and Claude does not drive them. `GATE` needs the operator's explicit yes naming the action, and then the operator does the wallet step. Claude never handles a recovery phrase, including a throwaway one (`moi-devrel/references/consent-and-identity.md`, section 5). If one is pasted, do not repeat it, say it is exposed, and carry on with the wallet extension or phone app.

**What you need.** MOI Wallet on a phone, with a devnet account that exists on chain and holds KMOI (the devnet test currency). The faucet (https://voyage.moi.technology/faucet/) funds only accounts that already exist; a brand-new wallet is registered through the wallet app first. The amount it pays out is quoted as 20K and as 100K KMOI in different docs: read it live (`moi-devrel/references/devnet.md`). A claude.ai plan that allows custom connectors: unknown, the Connectors page shows it. ASK: Rahul.

## Part A: prove the server before any client

| # | Step | Do this | Done when | Who |
|---|---|---|---|---|
| 1 | Health from outside | `bash "$SKILLS/moi-mcp-ops/scripts/mcp-health.sh"` | No FAIL. Known WARNs on 2026-10-03: the registry read, and the OAuth metadata form on production (`health.md`) | Claude |
| 2 | One read through the wire | A `tools/call` of a read tool. Arguments by tool: `moi_get_account` `{"address":"0x..."}`, `moi_get_asset` `{"assetId":"0x..."}`, `moi_get_interaction` `{"hash":"0x..."}`, `moi_get_logic` `{"logicId":"0x..."}` | `isError` is absent and the text holds chain data | Claude |

```
curl -s -X POST https://mcp-read.voyage.moi.technology/mcp -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"moi_get_asset","arguments":{"assetId":"<KMOI asset id>"}}}'
```
Take KMOI's asset id from the SDK, never from a note: in a working copy of `sarvalabs/moi-mcp` after `npm ci`, run `node -e "import('js-moi-sdk').then(m=>console.log(m.KMOI_ASSET_ID))"`. `git clone` and `npm ci` are downloads: GATE (ship-a-change.md step 3 has the wording of the ask). The id moved at v0.13.0 (`moi-devrel/references/devnet.md`).

## Part B: connect claude.ai

| # | Step | Do this | Done when | Who |
|---|---|---|---|---|
| 3 | Add the write connector | claude.ai, Settings, Connectors, Add custom connector. URL `https://mcp.voyage.moi.technology/mcp`, authentication **OAuth**. The labels may have moved since the repo's checklist was written | The connector card shows connected | Operator |
| 4 | Or the read-only connector | URL `https://mcp-read.voyage.moi.technology/mcp`, authentication **None**. The read gateway has no wallet tools | Six tools listed | Operator |
| 5 | Sign in | The consent page opens. There is no account or password: the identity is the `moi_uid` cookie, so a different browser is a new identity and needs a new pairing | Back in the chat with the connector on | Operator |
Wrong auth mode on the write gateway (None) makes sign-in impossible. If Connect spins forever while step 1 passes, that is the PR #18 symptom: `troubleshoot.md`. `mcp.moi.technology` is not a real host. A Claude Desktop config with `npx -y @moi-protocol/mcp-server` fails because nothing is published (`publishing.md`).

## Part C: reads in a chat (no phone, no funds)

| # | Ask Claude | Expected | Who |
|---|---|---|---|
| 6 | "What is the supply of KMOI on devnet?" (give the asset id from the SDK) | Real chain data from `moi_get_asset` | Operator |
| 7 | "Show the balance of <the operator's address>" | `moi_get_account`: nonce, registered flag, balances | Operator |
| 8 | "Look up this interaction" with a hash from the explorer | `moi_get_interaction`: status, sender, fuel | Operator |
| 9 | "Find the agent named <name>" | `moi_resolve_agent`. On 2026-10-03 this fails on every host with "Could not load the MOI agent registry ... account not found". That is a known fault, not a fault in your setup. Pass only once the registry id is updated and deployed (`settings-and-secrets.md`) | Operator |

## Part D: pair the wallet (the operator's phone, no funds spent)

| # | Step | Do this | Done when | Who |
|---|---|---|---|---|
| 10 | Ask to connect | The operator types, in their own chat: "Connect my MOI wallet for a week." Claude never calls `moi_connect_wallet`. The tool returns a pairing page link, because claude.ai never renders the QR image (PR #19) | A link in the chat | Operator |
| 11 | Scan and approve | Open the link, scan the QR with MOI Wallet within 5 minutes, approve the pairing on the phone. If it expires, call `moi_connect_wallet` again | The page says paired | Operator |
| 12 | Check | "What is my wallet status?" (`moi_wallet_status`) | Shows the paired account. A pairing lasts a week by default, or one approval or 15 minutes with `remember: false` | Operator |

## Part E: writes (each one spends devnet funds: GATE, operator's wallet)
Every write is two calls: a preview, then a confirm token that is bound to you, the tool and the arguments, lives 10 minutes and works once. The phone cannot show what is being signed, so the chat preview carries the numbers: read them before you approve.

| # | Step | Do this | Done when | Who |
|---|---|---|---|---|
| 13 | Cheapest write first | "Transfer 1 KMOI to my own account." Preview, confirm, approve on the phone. Ask: "Ready to send a 1 KMOI transfer to yourself on devnet, paid by <account>. Yes?" | `{"status":"sent","hash":...}` | GATE |
| 14 | Prove it by receipt | `moi_get_interaction` on that hash. The broadcast answer is not proof: simulation accepted a fuel price the chain later refused | Status `success` | Claude or Operator |
| 15 | Asset creation | "Create a test asset DEPLOYTEST with supply 100." The preview states the storage fund and fuel. The repo's checklist says about 20,000 KMOI, which predates v0.13.0; the code's minimum is `MIN_STORAGE_FUND`, 7 KMOI on master. Decline if the preview is more than the operator will spend. Put the paying account and the previewed amount in the ask | The asset resolves with `moi_get_asset`. The repo's checklist counts a deployment done when this transaction lands on chain | GATE |
| 16 | Other writes | `moi_mint`, `moi_call_logic` with `invoke`: only if the change touched them, same pattern. `moi_call_logic` with `view` is a read | Receipt `success` | GATE |

## Part F: failure paths (each is a phone interaction)

| # | Do this | Expect | Who |
|---|---|---|---|
| 17 | Start a transfer and press Reject | `{"status":"rejected","reason":"user_rejected"}` | GATE |
| 18 | Start a transfer and ignore the phone for 5 minutes | `{"status":"rejected","reason":"timeout"}` | GATE |
| 19 | Switch the wallet to another network, then write | `network_mismatch`, and reads still work | Operator |
| 20 | `moi_disconnect_wallet`, then write | `wallet_disconnected` | Operator |
| 21 | `moi_create_asset` with the default fund on a thin balance | Refused locally with the storage-fund hint, nothing reaches the phone | GATE |
Status of this table in the repo's testing plan on 2026-09-01: pair, reject and the local refusal were verified; the transfer and create-asset approvals, the timeout, the network switch and the disconnect were not. Whether any has been run since is unknown. ASK: Adithya. Do not call a write path release-ready until rows 13 to 15 pass once on a phone (`docs/testing-plan.md`, `docs/publishing.md`).

## Part G: after the next sync (not live on 2026-10-03)
Launchpad tools (`moi_launchpad_*`) and dapp tools (`moi_dapp_*`) are in master and not on production. After a sync that brings them: `MOI_LAUNCHPAD_URL` must equal the Launchpad's `NEXT_PUBLIC_APP_URL` or the tool refuses to sign ("Not signing: the sign-in message from <origin>..."). `moi_launchpad_sign_in` is, in voyage-api PR #313's words, the one step not yet verified live: whether the phone's message signature is the envelope the Launchpad expects. Product checks of the Launchpad itself belong to `moi-launchpad-ops`.

## Part H: the local server (a desktop client)
Build from a working copy of `sarvalabs/moi-mcp` (`git clone`, `npm ci` and `npm run build`; the downloads are a GATE), point the client at `node dist/index.js` with `MOI_NETWORK` and your own free `WC_PROJECT_ID` from cloud.reown.com (a public identifier, still not for chat or commits). `npm run pair` and `npm run status` pair and check the wallet. All tools register locally.

## Record the result
```
Connector check <date UTC>: host <name>, build evidence <tool count, OAuth metadata form>
Passed: <part and row numbers>
Failed or not run: <numbers, and why>
Transactions: <hash and receipt status for each write, or "none">
Ready to hand to users: yes or no, because <one reason>
```
Nothing persists on the server except the pairing and the write journal, so this note is the record. It names an account and transaction hashes, so keep it out of any public repository: if it sits inside a working copy, add `connector-check-*.md` to that copy's `.git/info/exclude` (a local ignore file that is never pushed).

## Not yet known
- Whether any phone check of the write path has passed since 2026-09-01. ASK: Adithya.
- Which tools the hosted server lists after the next sync.
- After a reset, whether MCP users need more than re-activating their account. ASK: Gokul.
