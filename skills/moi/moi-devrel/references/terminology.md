# Terminology: the words MOI insists on

Facts are as of 2026-10-02. Each row is a wording the founder or the previous operator corrected, with the date. Quoted words are the previous operator's, cleaned of typos. `slop-lint.sh` enforces the rows that name a lint rule (`bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" --list-rules` prints them all; `$SKILLS` is defined in `../SKILL.md`). Back to `../SKILL.md`.

How to use this file:
1. Before you write about MOI's model, governance, networks, money words or release times, read tables A to E.
2. After drafting, run `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" <file>`. Errors must be zero. A `(warn)` hit is a prompt to look, not a ban.
3. A row marked CONTESTED has no settled answer. Use the safe form and ASK the person named. When that person settles one, record the decision here with its date.
4. A document that quotes a wrong form on purpose ends that line with an HTML comment reading `slop-lint: ignore`. This file does so.

## A. Names and models
| Wrong form | Right form | Why | Source date | Lint rule |
|---|---|---|---|---|
| "account-centric", "MOI is account-based" | "participant-centric". The account is only the vehicle that represents a participant's state. | Founder's correction. The first CAIP draft got it wrong. | 2026-09-14 | account-centric <!-- slop-lint: ignore --> |
| "each account has its own chain", "a per-account sequence of tesseracts" | The MDAG wording in the block under this table. | A participant's links are a view of the DAG, not a separate chain. | 2026-09-14 | per-account-chain <!-- slop-lint: ignore --> |
| "Serval Labs", "SarvaLabs" | "Sarva Labs" (GitHub org `sarvalabs`, site sarva.ai). | Auto-notes write Serval or Server. The docs naming table spells it Sarva Labs. | 2026-09-14 | serval-labs, sarvalabs-one-word <!-- slop-lint: ignore --> |
| "Sarva Labs governs MOI", "the MOI Foundation builds MOI", or the Foundation left out | "designed and developed by Sarva Labs, governed by MOI Foundation" | The founder called governance "the most important aspect". The Foundation makes protocol decisions. Sarva Labs is one implementation partner: it builds the reference node and the SDKs. The model is Sui Foundation and Mysten Labs. No Foundation website exists, so moi.technology stands in. | 2026-09-14 | governance-inverted <!-- slop-lint: ignore --> |
| "chain ID" for MOI's own identifier | "network ID". Every network has its own. CONTESTED: format and RPC, see Contested 1. | A chain or network ID already exists in the protocol. | 2026-09-14 | chain-id (warn) <!-- slop-lint: ignore --> |
| "Voyage devnet" | "devnet". Voyage is the explorer and tooling site. The network is devnet. | "It is not called Voyage devnet, just say went live on devnet." The September release post, the Discord copy and the CASA README draft still carry the old form as of 2026-10-02. | 2026-09-25 | voyage-devnet <!-- slop-lint: ignore --> |
| "Indus" or "Babylon" as the current network | "devnet" | "The current network is devnet, not Indus." Babylon is a retired network name, see Contested 6. | 2026-08, day not recorded | old-network-name (warn) <!-- slop-lint: ignore --> |
| "CocoLang", "CoCo" | "Coco". First mention on a page: "Coco (also known as Cocolang)". | Docs naming table. | 2026-09-22 | coco-name (warn) <!-- slop-lint: ignore --> |
| "Moipod" | "MOIPod" in docs prose. Keep `moipod` in commands, package names and a quoted release note. CONTESTED for release posts, which use lowercase. | Docs naming table. | 2026-09-22 | moipod-caps (warn) <!-- slop-lint: ignore --> |
| "JS-MOI-SDK", "Js-moi-sdk" | "js-moi-sdk", always lowercase, even at the start of a sentence (rephrase the sentence). | Docs naming table. | 2026-09-22 | js-moi-sdk-case (warn) <!-- slop-lint: ignore --> |
| "Participant: an account on MOI" | CONTESTED. Safe form: "A participant is a person, a company or an agent. Its state is held in an account." | The September release post (the website repo copy) still carries the account wording. It predates the correction. | 2026-09-11 post, 2026-09-14 correction | participant-is-account (warn) <!-- slop-lint: ignore --> |
| "log in with IOME" | "log in with MOI Wallet" | Voyage moved its login from IOME to MOI Wallet. | Rule recorded 2026-08-31. The public Voyage post is dated 2026-08-27 and the move date is not recorded | none |

MDAG wording, to reuse: "MOI's ledger is a Multi-Link Composite DAG (MDAG) of tesseracts. A tesseract is the joint state record of every participant that moved together, and it carries one back-link per participant to that account's previous tesseract. Following one participant's links gives a logical, non-branching history, but that is a view of the DAG, not a separate chain." These are the founder's words as the previous operator recorded them, including "that account's". The research copies say "that participant's" in that one clause. ASK: Rahul to confirm the clause against docs.moi.technology/docs/learn/fundamentals/tesseract before the wording goes into public text. Canonical pages: docs.moi.technology/docs/learn/fundamentals/account and /tesseract. Do not write "no genesis" or "no chain id" as flat claims; say only what is verified (standards review rule, 2026-09). <!-- slop-lint: ignore -->

## B. Money and fuel words
| Wrong form | Right form | Why | Source date | Lint rule |
|---|---|---|---|---|
| "the token", "MOI's own token" | "KMOI", defined once as the native token of the MOI network, then "measured in anu". An optional analogy the previous operator used: ETH and wei. | Names the thing. The strongest complaint of the session. | 2026-09-11 | the-token (warn) <!-- slop-lint: ignore --> |
| "the fee" | "fuel" for what is paid, "fee payer" for the role, "fee delegation" for the feature. One word per concept, every time. | "What is THE FEE" asked for a name. | 2026-09-11 | the-fee (warn) <!-- slop-lint: ignore --> |
| "fixed supply" | "capped supply", everywhere. | The previous operator's instruction. | 2026-09-11 | fixed-supply <!-- slop-lint: ignore --> |
| "Every action on MOI costs fuel", "every interaction sent to MOI costs fuel" | No universal. Say what the release changes: "You can now pay fuel for another user." | Called an exaggeration and misleading. Removed from the post. | 2026-09-11 | fuel-universal <!-- slop-lint: ignore --> |
| Defining fuel in the opening line ("fuel is the fee for using the MOI network") | Define fuel where it is first needed, not in the opener. | Removed from the opener. | 2026-09-11 | none <!-- slop-lint: ignore --> |
| "an app pays for you" with no qualifier | "The fee payer covers fuel and nothing else. The sender still funds any value it sends. The payer signs each interaction." | The CC14 script carried this trap for the host's zero-KMOI question. | 2026-09-25 | none |
| "a native asset standard made for KMOI alone" | The release note's words: "KMOI now uses MASN, a new native asset standard." | The research lists this draft line among claims that sound right and are wrong at protocol level. It records the line and its removal, not the stated reason (inferred; the reason is not recorded). The CC14 script says MASN is "the standard reserved for the fuel token", the same shape: check it against source before reuse. | 2026-09-11 | none |
| "the manager can mint KMOI in an emergency" | "On MASN, Mint, MintWithMetadata, Burn, SetStaticMetadata and SetDynamicMetadata are reserved for protocol code, for every account including the asset manager." | Probed with "is this 100% true" and answered from source. | 2026-09-11 | none |

## C. Time and release words
| Wrong form | Right form | Why | Source date | Lint rule |
|---|---|---|---|---|
| "12:00 AM UTC", "00:00 AM UTC" | "00:00 UTC on 11 September (05:30 IST)": date, 24-hour UTC, India time. Run `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "2026-09-11 00:00" UTC`. | Read as noon. Three questions in a row and two wrongly scheduled posts, deleted by hand. | 2026-09-10 | twelve-am-utc, am-pm-utc (warn) <!-- slop-lint: ignore --> |
| "today", "last Friday", "since the last call" in scheduled or recorded text | An explicit date. | The release pack was scheduled at about 08:45 UTC on 2026-09-10 with the note's "today at 12:00 AM UTC", which on that day had apparently already passed (inferred from the scheduling time; not recorded elsewhere). Relative words go stale in decks. | 2026-09-10 | none <!-- slop-lint: ignore --> |
| A release candidate presented as shipped, stable or the default | Quote the version as tagged, with its suffix (js-moi-sdk 0.9.0-rc2). Add no sentence explaining what a release candidate is. Do not tell readers to upgrade to a version the operator has not confirmed as the latest compatible one. | August: rc1 kept, upgrade sentences dropped. | 2026-08-21, inferred from position | rc-as-shipped (warn) <!-- slop-lint: ignore --> |
| "live on devnet" for something found only in the source tip | "planned" until you have read a live interaction and checked the field names. On 2026-09-10 devnet still returned `payer`, not `fee_payer`. `net.Version` returned 0.13.0 on 2026-10-02, and an interaction read on 2026-10-03 carried `fee_payer` (`devnet.md`). | Source capability is not live capability. | 2026-09-10 | none |

## D. Positioning
| Status | Line | Where it applies | Source date |
|---|---|---|---|
| Current | "on-chain authority for the agentic economy" | moi.technology headline | 2026-06-02 |
| Current | "The participant layer for AI agents." Use it word for word where space allows. | docs sites (Documentation Standard) | 2026-09-22 |
| In use, unclassified | "the on-chain authority layer for AI agents" | the previous design skill's README, description and UI kit title (files dated 2026-05-28). ASK: Rahul | 2026-05-28 |
| In use, unclassified | "Authority Layer for the Agentic Economy" | the tagline in the moidocs site config (`moi-docs/references/new-site.md`, read 2026-10-03). ASK: Rahul | 2026-10-03 |
| Retired | "context infrastructure" (lint: context-infrastructure) <!-- slop-lint: ignore --> | replaced by the authority line | 2026-06 |
| Retired | "Not Your Context, Not Your Agent" (lint: retired-positioning) <!-- slop-lint: ignore --> | removed from the blog | 2026-08-18, inferred from position |
| Retired | "identity" as the headline word. The instruction was "replace identity with authority". The word still names an agent's on-chain identity in product text. | positioning lines | 2026-06-02 |
| Retired | "Building in Public" as the call's name (lint: building-in-public). The call is The Campfire Chat, tagline "Ideas. Updates. Community. Conversations." <!-- slop-lint: ignore --> | community call title chip | 2026-09, CC14 |

Website vocabulary (`CONTENT.md`, section "Voice", on `main` of `MOI-Website` since 2026-08-25, read in a clone fetched 2026-09-11; the previous operator's other corrections to that file were uncommitted and are not recorded elsewhere): use participant, authority, scope, revoke, on chain, agent. Avoid user, permissions, blockchain, AI assistant. "Contextual Compute" stays as a paper title.

## E. Other claims that came back wrong
| Wrong form | Right form | Why | Source date | Lint rule |
|---|---|---|---|---|
| "deployed on Vercel", "Vercel previews" | MOI sites and the Launchpad run on VMs deployed by GitHub Actions and Teleport. Docs previews are Cloudflare Pages. Points left Vercel too (as of 2026-10-01). | Corrected at least six times. | 2026-08-10, 2026-09-29 | vercel (warn) <!-- slop-lint: ignore --> |
| "nobody holds your money", "only the owner can move funds" | "Value moves only under the holder's own signature, and our agents never grant one." | The session 7 fact-check proved the blanket claim false. It survived in other files of that session. | 2026-08-07 | none |

## Contested (no settled answer)
1. **Network ID.** The CAIP-2 reference format (`moi:devnet`, `moi:112` and `moi:14` were all candidates, and no docs page names any of them), the RPC method that returns it (the docs document `net.NetworkID`, the running node answered method-not-found on 2026-10-03) and whether the node reports 112. Nothing has been filed upstream as of 2026-10-02. ASK: Rahul, then Gokul.
2. **Positioning.** Two current lines and two unclassified lines are in use (table D). The sources do not say which leads on the blog, social posts and decks, or whether the unclassified two are current or retired. The white paper subtitle "MOI Authority Layer" (MAL, `glossary.md`) is a fifth form. ASK: Rahul.
3. **Governance detail.** Whether Sarva Labs "operates" the public networks is flagged to be confirmed in the 14 September CASA draft. Public text uses only the one-line governance sentence. ASK: Rahul.
4. **"Participant" definition**, table A. ASK: Rahul whether the glossary line in the September post is rewritten.
5. **MOIPod versus moipod** in release posts.
6. **Babylon.** The x402 research calls it a retired network. The MCP read gateway still uses a `/babylon/` RPC path that returned 0.13.0 on 2026-10-02. Whether it is the same chain as `/devnet/` is unknown. ASK: Gokul. <!-- slop-lint: ignore -->
7. **Em dashes in specs and background docs.** Posts, scripts, social and status messages carry none. Specs are unsettled. Default: none in anything you author.
8. **Hashtags, a colon after section labels in social posts, link placement on X.** No decision is recorded. ASK: Rahul.

## Not yet known
- Who settles canonical wording when two sources disagree. ASK: Rahul.
- Whether a MOI Foundation public page will exist. None existed on 2026-09-14.
