# Defend it: the questions that were asked, and how to answer or say "I will check"

Facts are as of 2026-10-03. The research notes hold no record of an audience's real questions for any Builders session or community call as of 2026-10-02. Each question below was asked by a reviewer or the previous operator, sent ahead by a host, written into an FAQ, prepared in a runbook, or anticipated from a correction or a review item. The Provenance column says which, and a prepared or anticipated answer was not tested by an audience. `terminology.md` is in `moi-devrel/references/`, `caught-claims.md` in `moi-devrel/claim-check/references/` and `host-qa-prep.md` in `moi-webinar/community-call/references/`. Each answer is for the shape of the reply: check the limit and the source before you use the words. "The operator" and `ASK:` are defined in `moi-devrel/SKILL.md`. Back to `../GUIDE.md`.

## How to answer
1. A yes or no question gets "Yes." or "No." first, then the limit that keeps it true, then the source if asked. At depth 1 that is about 35 words (`levels.md`).
2. Claim only what the screen or the source shows. "Never claim more than the screen shows" is the rule of the session 8 run sheet (local only, ASK: Adithya).
3. Do not be walked into a claim. Three claims that questions invited: spend caps (not enforced, `misconceptions.md` M11), calling the session 7 demo x402, and "since 11 September" (a read proves now, not since).
4. A feature found only in a release note or the source tip is "planned" until the wire shows it (`moi-devrel/references/devnet.md`).
5. When the answer needs private source, say what the wire shows ("Observed on the wire: ...") or say "I will check". Never cite a private path.
6. Say "I will check" in full. The wording suggested for the community call is: "That goes beyond what I have confirmed, so I will check it with the protocol team and put the answer in the dev chat." (`moi-webinar/community-call/references/host-qa-prep.md`). Name the place where you will actually post the answer.
7. Then do three things. Add the question to the open list with a name next to it. Draft the question for the operator to send, as a plain question with context and not a report. Claude never sends it. Put the answer in the Q&A log when it arrives (section F).

## A. Fee delegation and KMOI
| Question | Provenance | Answer | Limit and source |
|---|---|---|---|
| Does the fee payer pay for the value being sent too? | Written FAQ, September post | "No. It pays only the fuel. If the sender sends 5 KMOI, those 5 KMOI still leave the sender's account." | Cleaned post in `moi-blog/examples/`, checked against the tag 2026-09-11 |
| Can someone name my account as their fee payer without asking? | Written FAQ | "No. The node rejects an interaction that names a payer unless the payer has signed it." | The payer signs each interaction one at a time, so there is no standing allowance |
| If I hold zero KMOI, can an app handle my fuel? | Host question sent ahead, in a heads-up of 2026-09-25 for CC14 (whether it was asked live is not on record) | The 35-word answer and second beat are in `host-qa-prep.md` | Open edge: a brand-new participant's first action. ASK: Gokul |
| Who pays if the interaction fails? | Not asked; stated in the post | "The payer. The release post states it." | `host-qa-prep.md`; `caught-claims.md` B, commit `280ffb2` |
| Can the manager mint KMOI in an emergency? | Probed by the previous operator (2026-09-11, inferred from position) and answered from source | "No. On MASN, Mint, MintWithMetadata, Burn, SetStaticMetadata and SetDynamicMetadata are reserved for protocol code, for every account including the asset manager." | Transfer, TransferFrom, Lockup, Release, Approve and Revoke still work. Post FAQ |
| Does `MAS0AssetLogic` still move KMOI? | Probed (same session) | "Yes for moving it. Its mint, burn and metadata methods are now refused for KMOI." | Post, "What changed for KMOI?" |
| Must a payer be a regular account? | Probed (same session) | "Only a participant account can be a payer. The SDK refuses a logic id or an asset id in the payer field." | Docs sponsor tutorial. Whether the node enforces it too is not on record. ASK: Gokul |
| Is it live, and since when? | Raised in review (the open go-live box on the September post's PR, and CC14 preparation) | "Read the node." | A read proves now, never since. `moi-devrel/claim-check/references/live-reads.md` |
| Why did storage go from 1 anu to 1,000,000 anu a byte? | Written FAQ | The post's answer: prices are set in anu at v0.13.0, and the deposit comes back when the data is withdrawn | The docs Storage page (read 2026-10-03) describes storage as collateral: KMOI is held back in proportion to the bytes stored and becomes spendable again when the storage is freed. On a Logic or Asset account `IxStorageWithdraw` returns the KMOI deposited, settled against the amount recorded when it was paid in. The price per byte is a governance parameter (`ANUPerByte` times `StorageMultiplier`). Whether the post's 1,000,000 anu per byte equals that product is not stated. ASK: Gokul |

## B. The model, governance, the node
| Question | Provenance | Answer | Limit and source |
|---|---|---|---|
| Who governs MOI? | Anticipated, from the founder's correction of 2026-09-14 | "Designed and developed by Sarva Labs, governed by MOI Foundation." | Whether Sarva Labs operates the public networks is flagged to be confirmed. Public text uses only this sentence. ASK: Rahul |
| Is the node open source? | Anticipated, from a CASA draft claim corrected 2026-09-09 | "The SDKs are public. go-moi is not." | Private as of 2026-10-02. Cite wire-visible behaviour |
| Does each account have its own chain? | Anticipated, from the founder's correction of 2026-09-14 | The MDAG wording in `terminology.md` | `misconceptions.md` M2 |
| Does MOI have a chain ID, or a genesis? | Anticipated, from the standards review of 2026-09-09 and 09-10 | The narrow, verified wording in M3 | `net.NetworkID` was not available on 2026-10-03. ASK: Rahul, then Gokul | <!-- slop-lint:ignore -->
| Why is the Launchpad not in the protocol docs? | Anticipated, from Rahul's change request on moidocs PR 124, 2026-09-17 | "It is an application that uses MOI." | M22 |

## C. Access policies and authority
| Question | Provenance | Answer | Limit and source |
|---|---|---|---|
| Can the agent delete the policy? | Prepared, session 8 | "No. A policy can be created, modified or deleted only by the account it is stored on." | Docs Access Control, "Ground Rules" |
| Can the agent work around the policy? | Prepared | "Not for storage writes. The check runs in the runtime when the write happens, not in the agent's code, imports or client." | The demo showed a refusal for storage only. The prepared answer also says what validators would have to do, which is a design claim no demo can show: leave it out unless it is sourced |
| What if the agent has more fuel than me? | Prepared | "Fuel buys computation, not permission." | In the demo the agent spent 86 fuel getting refused (node 0.12.0, 2026-08-31) |
| Can I cap what it spends? | Prepared | "Not yet. Only storage writes are enforced." | Docs "Current Scope", read 2026-10-03. Re-read it before you answer |
| Does a refused call cost money? | Prepared | "Yes. It is mined and charged. A refusal is a receipt, not a rejection." | Same run. Re-measure on the current node |
| Is the agent a sub-account? | Prepared | "No. It has its own account and its own key. A sub-account shares its parent's key." | Session 6 README, notes |
| Why not use allowances, like Ethereum? | Prepared | Allowances control the spending of an asset. Policies control writes to a participant's storage | MOI's own MAS0 has Approve and TransferFrom, so never say MOI has no allowances. Asset policies are reserved |
| I ran it and it failed before submission. | Prepared | "You used the SDK default, which simulates first. Pin the fuel limit to see the refusal on chain." | M15 |

## D. The registry, agents and demos
| Question | Provenance | Answer | Limit and source |
|---|---|---|---|
| What if the seller takes the payment and delivers nothing? | Prepared, session 7 | "Today you lose it, as with cash. MOI exposes lockup and release primitives that a pay-on-delivery flow could be built on." | The prepared line said "native to MOI", which the audit rated unverifiable on 2026-08-07 |
| Are those really two agents? | Prepared, sessions 7 and 8 | Say how it is staged: one machine, one phrase, two accounts the chain treats as unrelated | M27 |
| Why not x402? | Prepared, session 7 | "This demo is not x402, so do not call it that." | The guardrail written for session 9: "Any x402 client can read our invoice. Only a client that implements our scheme can pay it." Say both halves or neither. Session 9 is only planned (`moi-webinar`) |

## E. Standards and reviewers
| Question | Provenance | Answer | Limit and source |
|---|---|---|---|
| Can we still call it x402 without a facilitator? | Put by Rahul after a call; the answering note is undated, session 7 era (inferred) | The role is defined by its interface, verify and settle, not by custody. On MOI's upfront flow the buyer submits its own transfer and the facilitator only reads the chain | PR 2 spec and PR 3 `STATUS.md` (branch). The note that first answered it (session 7 `FACILITATOR-NOTE.md`, local only) describes a facilitator package that was removed, so do not reuse it |
| Is MOI x402 compatible today? | Anticipated, from the standards review | "Not yet publicly. Nothing was filed as of 2026-10-02." | M19. ASK: Rahul for the review gate |
| Why does MOI need a CASA namespace? | Anticipated, from the standards review | "x402 v2 names networks by CAIP-2 identifier, so a chain with none cannot be named correctly in a payment." | `x402-compat/x402.md`, `FINDINGS.md` (branch) |
| Why does network identification matter on MOI? | Anticipated, from the standards review | "Participant identifiers derive from the public key, so the same identifier exists on every MOI network, and a transfer sent to the wrong endpoint may succeed. The spec puts the network inside the signed claim." | `x402-compat/x402.md` section 2 and the PR 2 spec (branch) |
| What is MOI's network identifier? | Anticipated, from the standards review | "That is not decided." Candidates were `moi:devnet`, `moi:112` and `moi:14` | "I will check." ASK: Rahul, then Gokul |
| How does the AI-assistance disclosure fit the no-footer rule? | Anticipated, from the upstream rules | "Unresolved." x402 asks for disclosure and house rule 4 bans the footer | ASK: Rahul, before anything is filed |

## F. The Q&A log
After any session, call or review, write each real question word for word, who asked it, the answer given, the owner of any follow-up and the date. The January 2026 KRA document asks for Q&A and follow-ups within 48 hours (`moi-webinar/community-call/references/after-the-call.md`, step 10); whether that target still applies is not known. ASK: Rahul. A question that came from a real audience can become a row in this file once the asker's name and any private path are removed. The log names people and may name private source, so it stays out of git: keep it in the self-ignoring `explain-<slug>/` folder from step 10 of `../GUIDE.md` (a `.gitignore` holding one line, `*`), and never in a tracked file of a public repository.

## Not yet known
- What attendees asked. No log is in the library. ASK: Adithya for any chat or Discord record.
- Whether the prepared answers in sections C and D were ever asked live.
