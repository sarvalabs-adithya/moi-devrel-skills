# Real and simulated: what counts, and how to say which

Facts are as of 2026-10-03. `ASK:` is defined in `moi-devrel/SKILL.md`. House rule 5 (`moi-devrel/SKILL.md`): demos and tests use real devnet interactions, and anything simulated is said plainly. Back to `../GUIDE.md`.

## The rule and where it came from
- The chain is always real. "No mock mode for chain, chain always has to run" (the previous operator, during the Launchpad build). On 2026-07-14 mock identities and a mock mode were built although the real SDK had been supplied; the previous operator asked for the real `js-moi-agent-registry` instead.
- When the real path is down, say so and do not dress up a stand-in. On 2026-08-07 registry writes were down, so session 7 ran with two agents registered earlier and only the happy path, and said so.

## The four kinds
| Kind | What it is | What proves it |
|---|---|---|
| `chain` | A signed interaction was submitted to devnet in this case | Full hash, receipt status, node version, time, balances before and after |
| `read` | A read of the node, or of the live product, with nothing submitted | The command or URL, the answer and the UTC time. A read proves now, never since |
| `app` | Product behaviour with no interaction submitted: a screen, a chat reply, an API refusal, a cancelled wallet prompt | The message as it appeared, and the page value or balance that shows nothing moved |
| `simulated` | Anything standing in for the real thing | `simulated_what` says what, and the case never counts as real |

Signing a login message in the wallet submits no interaction, so it is `app`. A wallet prompt the operator cancels is `app`: nothing reached the chain.

## What is simulated (each one has bitten)
- **The node's own simulation.** The SDK's `send()` without a `fuel_limit` runs a client-side fuel simulation, and the MCP server simulates before it shows a preview. Simulation accepts what the chain later refuses: a fuel price of 1 simulated fine and bounced at broadcast (MCP issue 7), and the nightly canary once passed while asset creation failed because it asserted acceptance and not the receipt.
- **A fake node or a fake wallet client in a unit test.** The MCP unit tier (`docs/testing-plan.md`, Tier 1) runs against an in-process fake JSON-RPC node and a fake WalletConnect client. A pass there is `simulated`. It is the right tool for guard order and encoding, and it says nothing about devnet.
- **A fallback path.** Without a model key, session 7's buyer matched keywords and could pick the wrong market on screen. A "decided by" label showing `local-fallback` marks it.
- **An existing record standing in for a new one.** Session 7 reused agents registered earlier.
- **A database number standing in for a chain number.** The Launchpad's default marketplace listing is a database index and can show agents as on-chain from a dead chain; `?source=chain` reads the registry. An `onchain: null` answer means the read failed, not that the agent is unlisted.
- **A recording.** A recorded run is a real run on a stated date. Say the date when it is not today.
- **Localhost.** A local build with a local database tests the code, not the product. Record the target as localhost and keep it out of the production pass.

Prepared in advance is a separate thing: state that existed before the case (an agent registered yesterday). Put it in `config` and name it in `simulated_what` only if it stands in for the step under test.

## Reading the chain (read-only)
Params are an array holding one object. `RPC=https://dev.voyage-rpc.moi.technology/devnet/`.
```
curl -sS -m 20 -X POST "$RPC" -H 'content-type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"net.Version","params":[]}'
curl -sS -m 20 -X POST "$RPC" -H 'content-type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"moi.InteractionReceipt","params":[{"hash":"0x<64 hex>"}]}'
```
On 2026-10-03 the first answered `0.13.0` at 15:23 UTC and again at 17:35 UTC. The second returned the keys `from`, `fuel_used`, `ix_hash`, `ix_operations`, `participants`, `status`, `ts_hash` for recent interactions, with `status` 0 and `fuel_used` in hex. `moi.InteractionByHash` returns the interaction itself (sender, operations, `fee_payer`). More reads, and what they mean, are in `moi-devrel/claim-check/references/live-reads.md`. If `curl` exits 60 (it did on both paths on 2026-10-04 at 18:01 UTC: the certificate of dev.voyage-rpc.moi.technology had expired, `moi-devrel/references/devnet.md`), a case that needs these reads cannot be `read` or `chain`. Record it as blocked with the exit code and the UTC time, not as a failure of the product.

The read gateway of the MCP server is an easier path for balances and status, and needs no sign-in. Its `moi_get_account` tool takes `address` and returns the nonce, `isRegistered` and the balance in every asset. Its `moi_get_interaction` tool takes `hash` and returns `status` (pending, success or failed), `fuelUsed`, the sender and the operations. Balances come back in base units (anu). `moi_get_asset` (argument `assetId`) returns `symbol`, `standard`, `decimals` and `dimension`: for KMOI it answered `decimals` 9 and `dimension` 0 on 2026-10-03, so 1 KMOI is 1000000000 base units (the Launchpad's 10 KMOI activation grant is 10000000000). Take the KMOI asset id from the `balances` of a funded account and confirm `symbol` is KMOI; do not copy an id from an old document, because it changed at v0.13.0 (`moi-devrel/references/devnet.md`). All three tools answered with these fields on 2026-10-03, again at 17:38 UTC.
```
curl -sS -m 30 -X POST https://mcp-read.voyage.moi.technology/mcp -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"moi_get_account","arguments":{"address":"0x<64 hex>"}}}'
```
The `address` is the account's public address: ask the operator for it from the wallet, use it for the read, and write the label (A, B) in the log, not the address. Write the balance pair into `evidence` as you read it: they move, and cannot be re-read later.

What the receipt shows:
- **Success is the receipt `status`, not the broadcast.** Session 8 (31 August to 4 September 2026, before the v0.13.0 upgrade) measured a failed policy attempt as interaction `status` 1. Re-measure on the current node before you rely on a number.
- **A refused pull of the standard asset returns a hash and no error.** The only oracle is a balance difference. Show balances, never receipts (`moi-webinar/references/demo-standard.md`).
- **HTTP 200 is not success.** Wallet activation answered 200 on a reverted interaction and said "Wallet is ready" (PR #30, September 2026: the grant was under the 1 KMOI floor).
- **A refusal counts only for the right reason.** On 2026-08-31 a policy demo "passed" because the agent was out of fuel. Check the error text names the rule under test.

## Hashes and the explorer
Write each hash in full into `interaction_hash`. The explorer can lag by minutes (`moi-devrel/references/devnet.md`); read the node first. A hash from before a reset is not found. The explorer's hash-page URL pattern is not settled (`log-format.md`, Not yet known).

## Wallet and funds
- The operator performs every wallet and phone step. Claude never signs. Claude never handles a recovery phrase, including a throwaway one, even when the operator offers one for a test: continue with the MOI Wallet extension and the operator's funded account (`moi-devrel/references/consent-and-identity.md`, section 5).
- The faucet (`https://voyage.moi.technology/faucet/`) funds accounts that already exist, and asking it for funds is a write: the operator does it. The amount is quoted as 20K KMOI in one document and 100K in others; read it live.
- Derivation paths differ and a wrong one gives "account not found": faucet wallets `m/44'/6174'/7020'/0/0`, SDK-only wallets `m/44'/6174'/0'/0/N`, the Launchpad registration default and the wallet-extension owner in session 8 `m/44'/6174'/1'/0/0` (`moi-devrel/references/devnet.md`; `moi-webinar/references/demo-standard.md`).
- A brand-new wallet cannot sign until it is registered on the chain: the extension refused ("couldn't retrieve nonce") on 2026-07-31. That is a precondition, not a defect.
- Never read or confirm seed words on a recorded call (2026-09-24: a phrase reached Gemini notes).

## How to say which
| Where | Say |
|---|---|
| The log | `kind`, and `simulated_what` in plain words. `none` plus a reason when a word like "simulation" appears in a real case |
| The checker output | Two numbers: passes on the real devnet or live product, passes on something simulated |
| The hand-back | "Not verified or simulated:" with every simulated case and every blocked one |
| Any public text drawing on the round | "Tested on devnet on <date>, node <version>" only for chain and read passes. Check it with `moi-devrel/claim-check`. Same plain words every time |

If the real path is blocked, log `blocked` with the reason, or add a `simulated` case that says what it is. Do not log a simulated pass as a real one.

## Not yet known
- Whether `/babylon/` and `/devnet/` are the same chain. Read `/devnet/` unless a product uses the other path. ASK: Gokul.
- Whether the interaction `status` has other values than 0 and 1 on the current node. ASK: Gokul.
