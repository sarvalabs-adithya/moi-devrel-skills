# Glossary: MOI concepts in plain words

Facts are as of 2026-10-02, and entries marked 2026-10-03 were re-read from the public docs or the network on that date. Each entry is two sentences and a pointer to the page that is authoritative. Where the sources do not define a term, it is listed at the end with who to ask. Wording rules are in `terminology.md`. Back to `../SKILL.md`.

Sources under `session-8-policies/` and `x402-compat/` in `moi-foundation/MOI-Webinars` are on branch `claude/agent-payments-simple`, not `main`, as of 2026-10-02. Page names: "docs" is docs.moi.technology. "release post" is blog.moi.technology/article/moi-september-2026-release/. "SDK docs" is js-moi-sdk.docs.moi.technology. "Voyage docs" is voyage-docs.moi.technology. "Coco docs" is cocolang.dev.

## The protocol
| Term | In two sentences | Authoritative source |
|---|---|---|
| Participant | A person, a company or an agent that holds state on MOI. Its data sits on its own account, and the ledger links each change to every participant it touched. | docs `/docs/learn/fundamentals/account` |
| Account | The vehicle that represents a participant's state, controlled by that participant's key. Say participant-centric. | docs `/docs/learn/fundamentals/account` |
| Interaction | MOI's word for a transaction: a signed request to change the state of one or more participants. Its fuel is paid by the sender, or by a fee payer when the interaction names one. | docs fundamentals; release post |
| Logic | A program deployed on MOI, written in Coco, that reads and writes participant state. The agent registry and the Launchpad's AgentMarket contract are logics. | Coco docs; docs fundamentals |
| Asset | A protocol-native token, such as KMOI, that protocol operations create, transfer, lock and release, with no token contract to write. MAS0 is the fungible standard, and KMOI runs on MASN. An asset reports its own `decimals` (`moi.AssetInfoByAssetID`). | docs fundamentals (assets); release post |
| MAS1 | MOI Asset Standard 1, the standard for non-fungible assets: each unit is unique and indivisible, and each token ID can carry its own metadata. The docs list MAS0, MAS1 and MAS2 as recognized, first-class protocol standards and MASX as custom (2026-10-03). | docs `/docs/learn/fundamentals/assets`, section 4.3 |
| MASN | The native asset standard KMOI moved to in moipod v0.13.0. On it, Mint, MintWithMetadata, Burn, SetStaticMetadata and SetDynamicMetadata are reserved for protocol code, so no account, including the asset manager, can create or destroy KMOI. | release post FAQ |
| KMOI | The native token of the MOI network. Since v0.13.0 it has a capped supply and a new asset id, exported by js-moi-sdk as `KMOI_ASSET_ID`. | release post |
| anu | The smallest unit of KMOI: 1 KMOI = 1,000,000,000 anu. The network reports KMOI with 9 decimals (read 2026-10-03), so the two agree. Convert with the SDK's `parseKmoi` and `formatKmoi`, never by hand. | release post; SDK docs; `devnet.md` |
| Fuel | What running an interaction costs, paid in KMOI and priced in anu. As of v0.13.0 the lowest fuel price is 50 anu and storage costs 1,000,000 anu per byte. | release post |
| Storage collateral | MOI charges no fee for storage. An account must hold KMOI in proportion to the bytes it occupies: `Balance[KMOI] >= StorageConsumed x StorageMultiplier x ANUPerByte`, checked after every interaction, and the KMOI stays in the account as a floor under its spendable balance. A shared Logic or Asset account takes writes through `IxStorageDeposit`, and `IxStorageWithdraw` releases unused capacity and returns the KMOI (2026-10-03). | docs `/docs/learn/fundamentals/storage-cost` |
| Sub-account | An application-specific account that the `AccountInherit` operation creates for a primary participant. It inherits the execution context of a target application and keeps the primary account's signing credentials. The docs say a page on inherited accounts is coming soon (2026-10-03). | docs `/docs/learn/fundamentals/interactions` |
| Fee delegation | An interaction can name a fee payer, an account that signs it too and pays only the fuel, while the sender still funds any value it sends. The payer signs each interaction separately, so an app can cover fuel for users who hold no KMOI without leaving an open tab. A read of an interaction returns the field as `fee_payer` (all zeros when nobody sponsored it), and the docs Interactions page names the optional submission field `payer` (2026-10-03, `devnet.md`). | release post, "What is fee delegation?"; docs Interactions page |
| Notary | A co-signer whose signature covers the operations as well as the fuel. A fee payer goes in the participant list only when it also acts as a notary. | release post |
| Participant list | The list of participants an interaction touches. Since v0.13.0 the node reads the sender and the fee payer from the interaction header, so you leave them out, except a fee payer that also acts as a notary. | release post |
| MDAG | Multi-Link Composite DAG, MOI's ledger: a graph of tesseracts, not a chain of blocks. There is no chain per account, and one participant's history is a view of the DAG. | docs `/docs/learn/fundamentals/account` and `/tesseract` |
| Tesseract | The joint state record of every participant that moved together. It carries one back-link per participant to that account's previous tesseract (the founder's wording; the clause is unconfirmed, see `terminology.md`). | docs `/docs/learn/fundamentals/tesseract` |
| Access policy | A standing rule on a participant's account about which programs may write to its data. In Builders session 8 (2026-09-04) only storage policies were live, and asset, logic and key policies were reserved. | docs access-policy pages (moidocs PR 120); `session-8-policies/` in moi-foundation/MOI-Webinars |
| Network ID | MOI's own identifier for a network, one per network, and 112 is the number the docs, the SDK and the previous operator's notes give for devnet. The docs document an RPC method `net.NetworkID`, but the running node answered method-not-found on 2026-10-03, and the CAIP-2 format is undecided. ASK: Rahul or Gokul. | `references/devnet.md`; `terminology.md` Contested 1 |
| Devnet | The current public MOI network, with RPC at dev.voyage-rpc.moi.technology/devnet/. A reset wipes every account and contract: full wipes were recorded on 2026-08-15 and around 2026-09-11 (announced for 00:00 UTC on 11 September, not confirmed to the minute; see the reset history in `devnet.md`), and each one forces registry ids, wallets and demos to be redone. | `references/devnet.md` |
| Babylon, Indus | Babylon is the name of a retired MOI network, and Indus is another network name that Voyage carries. Neither is the current network; see `terminology.md` Contested 6 for the `/babylon/` RPC path that still answers. | `terminology.md` <!-- slop-lint: ignore --> |

## Software and tooling
| Term | In two sentences | Authoritative source |
|---|---|---|
| Coco | MOI's smart-contract language, an interaction-oriented language whose compiler turns `.coco` files into manifests for the PISA runtime. Write "Coco (also known as Cocolang)" on first mention. | Coco docs; repo `sarvalabs/coco-docs`; maintainer Robert Spendl |
| PISA | The runtime that executes Coco logics. It is built into the Coco compiler and exists as the Go module go-pisa (v0.8.0 in the August release list), and a Coco project names its target PISA version in `coco.nut`. Coco compiler 0.9.3 targets PISA 0.8.2 (`project-handover-docs/AGENT-SKILLS.md`). | Coco docs (compiler pages). go-pisa source is private. |
| moipod | The software that runs a MOI node. Version 0.13.0 added fee delegation, moved KMOI to MASN and priced fuel and storage in anu. The docs' Guardian FAQ shows a node operator pulling the `sarvalabs/moipod` Docker image and restarting with a clean-db flag after a network reset (2026-10-03). | release post; protocol team release note; docs `/docs/guard/guardian-faq` |
| Guardian, validator | A guardian is a node operator. In the docs' operations table, `GuardianRegister` registers a node as a network validator and locks its initial stake, and it is marked not yet active (2026-10-03). The setup guide targets the retired Babylon TestNet, so treat its steps as old. ASK: Gokul. | docs `/docs/learn/fundamentals/interactions`; `/docs/guard/setup-guardian` | <!-- slop-lint: ignore -->
| go-moi | The reference node repository built by Sarva Labs, private as of 2026-10-02, so public text cites only wire-visible behaviour, js-moi-sdk, docs and the explorer. August release logs used go-moi tags such as v0.12.0, and how the go-moi and moipod names relate is not recorded. | ASK: Gokul |
| js-moi-sdk | The public JavaScript SDK for MOI (`sarvalabs/js-moi-sdk`, npm `js-moi-sdk`). Version 0.9.0-rc2, a release candidate, is the version the release post pairs with moipod v0.13.0. | SDK docs |
| js-polo | The library that encodes MOI data. Version 0.1.5 pairs with js-moi-sdk 0.9.0-rc2. | release post |

## Products and surfaces
| Term | In two sentences | Authoritative source |
|---|---|---|
| Voyage | MOI's public explorer and tooling site at voyage.moi.technology, with the explorer, a faucet and the Logic and Asset Playgrounds. It is a product name, so say devnet for the network. | Voyage docs: getting-started, `endpoint-docs/faucet`, `wallet-authentication` |
| Faucet | The Voyage service that sends test KMOI on devnet. It no longer creates accounts: register the account on chain first, then fund it. A claim needs a faucet token from the Voyage dashboard, and an account can claim once per fixed cooldown (2026-10-03). | Voyage post of 2026-08-27; Voyage docs `endpoint-docs/faucet` |
| MOI Wallet | MOI's wallet, a browser extension and a mobile app, that signs interactions and sign-in messages for the user. The site never sees a seed phrase. | docs `/docs/build/moi-wallet` |
| Sign In With MOI | A login method: the wallet signs one message, and the server recovers the public key and checks that it derives to your address. It happens off chain and costs no fee. | Launchpad `lib/siwm.ts`; MCP `docs/dapp-conventions.md` |
| IOME | An identity platform (iome.ai) behind the earlier Voyage login ("Generate IOMe Id"); it still holds the recovery phrase of accounts created there. Voyage moved its login to MOI Wallet, announced in a public post dated 2026-08-27 (the move date itself is not recorded), and some older student material (the Forge guide, awesome-moi) still mentions it, probably stale. | blog post `move-your-voyage-login-to-moi-wallet`; ASK: Gokul what the letters stand for |
| Agent Launchpad | A no-code product at launchpad.moi.technology: connect MOI Wallet, pick a template, sign one on-chain registration, then run the agent on your own machine with messages through Telegram. It is an application built on MOI, so it does not belong in protocol docs. | `sarvalabs/moi-agent-launchpad` `docs/HANDOFF.md` and the deploy workflows; the README is stale |
| Agent registry | An on-chain logic that lists registered agents, each with an owner, an agent wallet, a status and a `card_uri` that points to a card describing the agent. Its logic id changes after a devnet reset, and every product that pins it must be updated. | npm `js-moi-agent-registry`; `references/devnet.md` |
| Agent Explorer | A public directory at agents.moi.technology of every agent on the registry. Owners manage theirs through WalletConnect, and an admin can mark agents verified. | repo `sarvalabs/agent-explorer` |
| MCP server | A server that lets a chat assistant such as claude.ai or Claude Desktop read MOI and propose writes, while the user's phone wallet signs every write and the server holds no key. The source is the public `sarvalabs/moi-mcp`, and production runs from a copy in `sarvalabs/voyage-api`. | `sarvalabs/moi-mcp` README |

## Standards and visibility
| Term | In two sentences | Authoritative source |
|---|---|---|
| x402 | A standard for paying over HTTP 402: an agent meets a resource that needs payment, pays, and receives it with nobody approving each step. For MOI, "x402 compatible" means a CASA namespace, a scheme specification and a TypeScript mechanism package, and nothing had been filed upstream as of 2026-10-02. | `x402-compat/x402.md` and `UPSTREAM.md` in moi-foundation/MOI-Webinars |
| Facilitator | In x402, the service that verifies a payment and settles it on chain for the seller. A facilitator must read the receipt status, because a refused transfer still has a hash. | `x402-compat/review-package/PR-2-x402-scheme-spec/` |
| CAIP-2 and CASA | CAIP-2 is the standard way to identify a chain or network. CASA is the Chain Agnostic Standards Alliance (chainagnostic.org, 2026-10-03), whose repository `ChainAgnostic/namespaces` holds one profile per namespace. MOI's draft profile is the namespace `moi`, and it was not yet filed on 2026-10-02. | `x402-compat/review-package/PR-1-CASA-namespaces-moi/` |
| GEO | Generative engine optimization: making content easy for AI answer engines to read and cite. MOI measures it monthly and fixes it in the docs sites. | `DOCS-STYLE-GUIDE.md` in `sarvalabs/moidocs` (committed in PR #124, merged on 13 October 2026) |

## Not yet defined here
Each of these appears in the sources without a definition. ASK before you explain it to anyone.
- What PISA stands for, and what MERU is (an engine kind listed beside PISA in js-moi-sdk constants). ASK: Gokul.
- What the letters of IOME stand for. ASK: Gokul or Vinay.
- How the names go-moi and moipod relate. ASK: Gokul.
- Kill switch: its docs page was deleted on 2026-09-09 because it did not explain the feature (the Launchpad's AI-spend kill switch is a different thing). ASK: Gokul.
- Storage fund: it appears as `storageFund` in deploy options and as a default in the Launchpad. The storage page of the docs describes collateral and does not use the term for MOI (its comparison table uses it for Sui). Whether the release post's 1,000,000 anu per byte equals ANUPerByte times StorageMultiplier is not stated. ASK: Gokul.
- Inherited accounts in full: the docs promise a dedicated page, "coming soon" on 2026-10-03. ASK: Gokul.
- MAL, the MOI Authority Layer, which appears in the research only in the white paper's subtitle. ASK: Rahul.
