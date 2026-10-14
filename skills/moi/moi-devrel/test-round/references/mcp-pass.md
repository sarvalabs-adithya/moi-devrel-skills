# The MCP connector pass: a reusable case list

Facts are as of 2026-10-03. `ASK:` is defined in `moi-devrel/SKILL.md`. Source: `docs/testing-plan.md`, `docs/deploy-checklist.md` (section 7) and `docs/reviewer-guide.md` in `sarvalabs/moi-mcp`, which is public. These files and `docs/publishing.md` are on `master` of the public repo on GitHub (tip dated 2026-09-24, checked on 2026-10-03 with `git ls-remote` and a GET of each file), so anyone can read them. The live reads below were made on 2026-10-03 between 15:28 and 15:30 UTC and again between 17:35 and 17:38 UTC with the same answers. Back to `../GUIDE.md`.

As of 13 Oct 2026: production unchanged since 23 Sep; voyage-api sync PRs #313 and #320 open; moi-mcp #27 reviewed, merge planned 14 Oct. Re-record M0.3 after any sync.

MCP server: A security finding is open on this product as of 2026-10-02. See the Open items of project-handover-docs/MCP-SERVER.md before touching its admin; ASK: Rahul if unclear. This pass reads, and signs only through a phone. It touches no admin.

## What is being tested
A chat assistant (claude.ai) reads MOI through a connector and proposes writes. Each write is built and simulated by the server, shown as a preview with a single-use confirm token, and only a second call with that token reaches the phone, where MOI Wallet signs. The server holds no key. Reads go straight to the node. Hosted URLs: the write gateway `https://mcp.voyage.moi.technology` (OAuth) and the read gateway `https://mcp-read.voyage.moi.technology` (no sign-in). `mcp.moi.technology` does not exist.

Merging to `sarvalabs/moi-mcp` deploys nothing. Production is a copy in the private `sarvalabs/voyage-api` (`moi-mcp/` on branch `feat/moi-mcp`), deployed by a manual workflow (`moi-devrel/references/repo-map.md`; skill `moi-mcp-ops`). So this pass tests the hosted URLs and records which sync is live. Who may trigger a production deploy is not settled: ASK: Srikar (the `voyage-api` workflows), then Rahul.

## Rules for this pass
- **The operator runs every write case from a claude.ai chat** connected to the write gateway, with their own phone and funded account. The Claude Code session reads the read gateway, reads hashes back and writes the log. Claude never pairs a wallet, approves or signs. Phone approvals cannot be automated, and a write path must be approved by a human on a phone at least once before release (`docs/testing-plan.md`; `docs/publishing.md`).
- **Every write case spends devnet funds** (a gate): the operator's yes names the account.
- **Funding.** `deploy-checklist.md` asks for about 20,000 KMOI (10,000 storage fund plus 10,000 fuel reserve). That predates v0.13.0, and the research measured a storage-fund floor near 6 KMOI (inferred). Do not quote 20,000. The preview shows the storage fund and fuel: fund for what it shows, plus margin.
- **The identity is a browser cookie.** A different browser is a new identity and a fresh pairing.
- **Known upstream, not a regression:** the wallet's `moi.sendInteractions` crashes its database, so the server signs through `moi.signInteraction` and broadcasts itself.
- Every bug fixed gets a test that would have caught it (`docs/testing-plan.md`).

## M0. Preflight (reads; Claude can run these)
| id | kind | ask or do | must |
|---|---|---|---|
| M0.1 | read | `curl -sS -m 20 https://mcp.voyage.moi.technology/health`, then the same on the read host | `"ok":true`. Write: `"readOnly":false,"pairingMounted":true`. Read: `"readOnly":true`. A 503 with `ok` false means the config failed to load |
| M0.2 | read | `curl -sS -m 20 https://mcp.voyage.moi.technology/.well-known/oauth-authorization-server` | `issuer` equals the public write host exactly. `http://localhost` means the environment never reached the process |
| M0.3 | read | `tools/list` on both hosts (command below) | 13 tools on the write host and 6 on the read host (2026-10-03). Record the names: the list shows which sync is live |
| M0.4 | read | `tools/call` `ping`, then `moi_get_account` on the operator's account (ask for its public address) and `moi_get_asset` on the asset id in its `balances`, then `moi_resolve_agent` with `{"query":"agent"}` (call shape in `real-chain.md`) | `ping` answers. `moi_get_asset` answers `symbol` KMOI, `standard` MASN and `decimals` 9 (2026-10-03). `moi_resolve_agent` returns agents |
| M0.5 | read | `gh run list -R sarvalabs/moi-mcp --limit 8` (read-only; skip it if `gh` is not signed in, and never switch the account) | The chain canary and the upstream watch are green (observed 2026-10-02) |

```
curl -sS -m 30 -X POST https://mcp.voyage.moi.technology/mcp -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```
The write host answered 13 tools: `ping`, `moi_get_account`, `moi_get_asset`, `moi_get_interaction`, `moi_get_logic`, `moi_resolve_agent`, `moi_connect_wallet`, `moi_wallet_status`, `moi_disconnect_wallet`, `moi_transfer`, `moi_create_asset`, `moi_mint`, `moi_call_logic`. The read host answered the first six. The Launchpad and dapp tools are not in the live list.

**Expected failure today.** On 2026-10-03 at 15:28 UTC `moi_resolve_agent` failed with "Could not load the MOI agent registry (logic 0x20000000c684f926...). It may not be deployed on this network. account not found". The live copy still points at the registry wiped on 2026-09-11. Log M0.4 as `fail` with `fix` set to `accepted: known, live copy not yet updated to the new registry, <who>, <date>` once the operator has confirmed that (ASK: Gokul for the current registry id), and retest after the next sync.

## M1 to M13. The end-to-end check (about 10 minutes with a funded wallet)
Order matters. Cases marked chain spend funds.

| id | kind | ask or do (operator in claude.ai) | must |
|---|---|---|---|
| M1 | app | Settings, Connectors, Add custom connector, the write URL ending in `/mcp`, authentication **OAuth**. (Read-only alternative: the read URL, authentication None) | Connector added and tools listed. With None on the write URL sign-in never happens and every wallet tool returns an unsatisfiable prompt |
| M2 | read | "What is the supply of KMOI on devnet?" | Real chain data. Compare with a direct read |
| M3 | app | "Connect my MOI wallet, stay connected for a week." Sign in on the consent page. Open the pairing page link the tool returns. Scan the QR with MOI Wallet within 5 minutes and approve on the phone | `moi_wallet_status` shows the paired account. If the chat shows no QR image, use the link: the image was not displayed in claude.ai when last recorded (2026-10-02) |
| M4 | chain | "Create a test asset called <name> with supply 100." Read the preview (storage fund and fuel), confirm, approve on the phone | Deployment is done when this lands on chain. Hash, receipt status 0, `moi_get_interaction` shows success, `moi_get_asset` resolves the new asset |
| M5 | read | "What is my wallet status?" | The paired account, and when the pairing expires (a week, or 15 minutes for a one-shot pairing) |
| M6 | chain | Transfer 1 KMOI to yourself, approve | `{"status":"sent"}` and a hash; the interaction reads success |
| M7 | app | Transfer, then Reject on the phone | `{"status":"rejected","reason":"user_rejected"}`. Nothing submitted |
| M8 | app | Transfer, then ignore the phone for 5 minutes | `{"status":"rejected","reason":"timeout"}` |
| M9 | app | Switch the wallet's network, then ask for a write; then a read | `network_mismatch` on the write. Reads still work |
| M10 | app | Disconnect the wallet, then ask for a write | `wallet_disconnected` |
| M11 | app | Create an asset with the default storage fund | Refused before the phone, with the storage-fund hint. Nothing reaches the phone |
| M12 | app | Open the connector from a different browser | A new identity: sign in again and pair again |
| M13 | app | After the Launchpad tools are synced: `moi_launchpad_sign_in` | Passes only if the phone's message signature is the envelope the Launchpad expects. Recorded as the one step never verified live. `blocked` until the tools are in `tools/list` |

M4 and M6 to M11 are the repo's Tier 3 checks 3 and 2, 4, 5, 6, 7, 8 (`docs/testing-plan.md`) run against the hosted gateway. M4 is also step 7.3 of the deploy checklist. As of 2026-09-01 only checks 1, 4 and 8 were verified, and the tool had never returned `sent` after a real tap. No phone check has been recorded since (`project-handover-docs/MCP-SERVER.md`, Open items, gives 1 September as the last one).

## The repo's own tiers (from a working copy of `sarvalabs/moi-mcp`)
| Tier | Command | Kind | Note |
|---|---|---|---|
| 1 Unit | `npm run typecheck && npm test && npm run build` | simulated | An in-process fake node and a fake wallet client. 169 tests on 2026-09-01. `npm ci` downloads packages: say so and ask first |
| 2 Live read | `npm run test:e2e` (sets `MOI_E2E=1`) | read | RPC liveness, typed bad id, registry loads. Fixtures are live values dated 2026-09-01 and have moved |
| 2 Canary | `MOI_E2E=1 npx vitest run test/e2e/chain-canary.test.ts` | simulated | Builds an asset creation and asserts the node's simulated receipt status is 0, not that the node accepted the shape. Nothing is submitted, so a pass says nothing about a real broadcast. The canary account (KMOI's creator) can stop existing after a reset: override `MOI_CANARY_ACCOUNT` |
| 3 Wallet | M4 to M11 above | chain, app | A phone is required |
| Release | `npm pack`, install the tarball in a temp folder, run `moi-mcp help` and the HTTP bin through its symlink, `curl` the health route | app | Installing from the tarball caught a phantom dependency and a silently exiting bin. Not published to npm: the package name is undecided (ASK: Rahul) |

`npm run cross-check` compares this server with a Go implementation kept at `moi-mcp-go`. That folder has no remote and exists only on the previous operator's machine as of 2026-10-02: skip the check: that copy is not available after the handover.

## Not yet known
- Whether a claude.ai plan allows custom connectors for the tester. ASK: Rahul.
- Whether any Tier 3 phone check has passed since 2026-09-01. None is recorded; run M4 and M6 once on a phone and log them.
- Who triggers the production deploy, and which tools the next sync lists. ASK: Srikar (the `voyage-api` workflows), then Rahul; see the Open items of `project-handover-docs/MCP-SERVER.md`.
