# Concept paths: the order to learn each concept in, and where its authority is

Facts are as of 2026-10-03. Docs pages at docs.moi.technology were read on that date. A block holds an order, the authority, a test question and the wrong pictures that attach to it (numbers refer to `misconceptions.md`). The test is a question the operator answers at depth 2 (`levels.md`); the answers live in the authority, not here, because the definitions are in `moi-devrel/references/glossary.md` and `terminology.md` and this file never restates them. Page paths below are under `docs.moi.technology/docs/`. `devnet.md` and `consent-and-identity.md` are in `moi-devrel/references/` beside the glossary. "The operator" and `ASK:` are defined in `moi-devrel/SKILL.md`. Back to `../GUIDE.md`.

A proposed order for an operator new to MOI: 1, 3, 2, 10, then by need (4 to 9, 11). Fuel and KMOI come early because moipod v0.13.0 is the latest release on record as of 2026-10-03, so most questions touch it. Teach one block per sitting.

## 1. Participant-centric state, the account, the interaction
- **Order:** how state is anchored today (to the application, to the object); the participant, with the account as the vehicle for its state; the interaction, which names the participants it touches; why participants with disjoint state run at once; the Context-Superstate last, at depth 3.
- **Authority:** `learn/fundamentals/account` ("State Models"), `learn/fundamentals/interactions`; glossary rows Participant, Account, Interaction; `terminology.md` section A.
- **Test:** If two people use the same app, whose account holds each person's data?
- **Wrong pictures:** M1, M2, M30.

## 2. The tesseract and the MDAG
- **Order:** a block, one global sequence; why one sequence is a bottleneck; the tesseract, the joint state record of the participants that moved together; one back-link per participant; the MDAG as a partial order, where one participant's history is a view; genesis and the Sarga account, depth 3.
- **Authority:** `learn/fundamentals/tesseract`; the MDAG block in `terminology.md`. The page says each back-link points "at that account's own previous tesseract" (read 2026-10-03). That is the founder's recorded wording, and `terminology.md` still asks Rahul to confirm the clause, so ASK: Rahul before it goes into public text.
- **Test:** Does each participant have its own chain? Is there a genesis?
- **Wrong pictures:** M2, M3. **Ask:** Rahul for wording, Gokul for mechanics.

## 3. Fuel, KMOI, anu, the fee payer
- **Order:** an interaction costs fuel to run; KMOI, what fuel is paid in; anu, the unit, converted with the SDK; who pays, the sender or a fee payer; what the payer covers and what it does not; the notary and the participant list, depth 3; MASN and the capped supply, depth 3. Define fuel where it is first needed, not in the opener (2026-09-11).
- **Authority:** the protocol team's release note, verbatim (ASK: Gokul where this version's note is); the release post at blog.moi.technology/article/moi-september-2026-release/ (answered 200 on 2026-10-03; as of 2026-10-02 it carried wording that the cleaned copy in `moi-blog/examples/` corrects); `learn/fundamentals/interactions`, `execution-and-fuel`, `storage-cost`; `build/tutorials/sponsored-ix-tutorial`; SDK exports `KMOI_ASSET_ID`, `DEFAULT_FUEL_PRICE`, `parseKmoi`, `formatKmoi`; glossary rows Fuel, KMOI, anu, Fee delegation, Notary, MASN.
- **Test:** An app is the fee payer and the user sends 5 KMOI. Whose account loses the 5?
- **Wrong pictures:** M4 to M7. **Live check:** `devnet.md` "Before you say live", step 4.
- **Two names for the fee payer field.** A read of an interaction returns `fee_payer`. The docs Interactions page names the optional submission field `payer`, and which name a submission accepts has not been read (`devnet.md`, "Before you say live", step 3; ASK: Gokul). Say which of the two you mean every time you teach it.

## 4. Assets: MAS0, MASN, Lockup and Release
- **Order:** an asset is protocol-native, created and moved by operations with no token contract; MAS0, the fungible standard, and its routines (Transfer, TransferFrom, Approve, Revoke, Lockup, Release); a swap with Lockup and Release, trust-based and not atomic; MASN, where KMOI moved; assets backed by a logic (session 2's fee-on-transfer asset); NFTs.
- **Authority:** `learn/fundamentals/assets` (it covers MAS0 and MAS1 and has no MASN section as of 2026-10-03); the session 2, 4 and 5 READMEs (`moi-foundation/MOI-Webinars`, on `main`); the release post for MASN. Session 4's README says release called with nothing locked "succeeds" and moves zero funds. Lockup and Release semantics (who is debited, who may release) are node-side: the 2026-08-07 audit could not verify them from the SDK, and no later check is on record for the README's "irrevocable" and "only the beneficiary can pull". The Assets page words Lockup more loosely (the amount stays owned but cannot be transferred until released). Treat both README phrases as "I will check". ASK: Gokul.
- **Unresolved:** the docs list MAS1 as the non-fungible standard, session 5 builds its collection as a Coco logic, and the glossary lists MAS1 as undefined. ASK: Gokul before you teach MAS1.
- **Test:** Is "only the owner can move funds" true?
- **Wrong pictures:** M7, M8, M24.

## 5. Logics, Coco and actor state
- **Order:** a logic is a program deployed on MOI; written in Coco, compiled to a manifest for the PISA runtime; two kinds of state, the logic's own and each participant's; endpoints that change state and endpoints that only read; deploy and call from the SDK; fuel and the storage fund.
- **Authority:** `learn/fundamentals/logics` ("Dual-State Architecture", "Endpoint Qualifiers"); `execution-and-fuel` (sections 6.2 and 6.3); Coco docs at cocolang.dev; the session 1 README and code (`main`); glossary rows Logic, Coco, PISA.
- **Undefined in the glossary:** what PISA stands for, MERU, the storage fund rule. The docs do not expand PISA either (read 2026-10-03). The docs Storage page (`storage-cost`, read 2026-10-03) now describes the collateral model and the deposit and withdraw interactions, which the glossary row does not yet cite; teach the rule from that page and leave the 1,000,000 anu figure to the release post. ASK: Gokul. Coco questions: Robert Spendl.
- **Test:** Where do the bytes of a participant's counter live, in the logic or on the participant's account?
- **Wrong pictures:** M9, M24.

## 6. Access policies
- **Order:** where a participant's data lives; so a logic often writes to storage it does not own; why a rule inside a program is only a request; the policy (resource, action, caller and origin); who may write it (only the account it sits on); where the check runs (the runtime, at the write); grant and revoke as interactions on the owner's account; what is enforced today; how other designs do it.
- **Authority:** `learn/fundamentals/access-control` ("Why Writes Need Authorization", "Ground Rules", "Current Scope") and `build/tutorials/access-policy-tutorial`. The session 8 pack is on branch `claude/agent-payments-simple` of `moi-foundation/MOI-Webinars`, not `main`: `session-8-policies/SCRIPT.md`, `README.md`, `NOTES.md`. Its `RUNBOOK.md` is gitignored and local to the previous operator's machine (ASK: Adithya for a copy).
- **Say today:** only storage writes are enforced; asset, logic and key policies are rejected at submission (docs "Current Scope", read 2026-10-03). Re-read that section before you say "today".
- **Test:** One file is run three times and is refused, allowed, refused. What changed between the runs?
- **Wrong pictures:** M9 to M12.

## 7. Context inheritance and sub-accounts
- **Order:** app data lives on the account, not in the logic; a plain account has no slot for a logic, so the call reverts; inheriting creates a sub-account, links it to one logic and seeds it, in one interaction signed by the primary; its address is computed and its status is one read; what it is not, because the sub-account shares the primary's key; why the session 8 design built on it was dropped.
- **Authority:** `learn/fundamentals/account` ("Inherited Accounts", which says a dedicated document is coming, read 2026-10-03); `interactions` (AccountInherit); `build/tutorials/account-tutorial`; the session 6 README (`main`), whose closing notes say inheritance is not a permission sandbox; the session 6 teaching guide in `sarvalabs-adithya/moi-agent-budget` (private, the previous operator's account; ASK: Adithya for access); `session-8-policies/NOTES.md`, "Why the design changed" (branch). Check any byte count against the identifier layout in the x402 spec draft before you say it.
- **Undefined in the glossary:** sub-accounts, though the docs Interactions page describes AccountInherit as creating an application-specific sub-account that keeps the primary's signing credentials (read 2026-10-03). Quote the page and mark the rest "I will check". ASK: Gokul.
- **Test:** Does a sub-account stop an agent from spending the primary's funds?
- **Wrong pictures:** M10, M12.

## 8. The agent registry and the products built on it
- **Order:** an agent has an owner and its own wallet; the registry is an on-chain logic holding identity, wallet, status, url and `card_uri`; the card at that address, normally off chain, says what the agent does; discovery is a client-side scan and there is no search; registering is an owner action, and the identity check proves a binding, not behaviour; a reset changes the registry id; Launchpad, Explorer and MCP are applications on MOI.
- **Authority:** npm `js-moi-agent-registry` (ASK: Gokul where the repo is); the session 3 and 7 READMEs (`main`); the registry row of `session-7/blog-assets/factcheck-report.md` (branch); glossary rows Agent registry, Agent Launchpad, Agent Explorer, MCP server; `moi-devrel/references/repo-map.md`. Product questions: `moi-launchpad-ops`, `moi-launchpad-ops/explorer`, `moi-mcp-ops`.
- **Test:** Where is an agent's list of skills stored?
- **Wrong pictures:** M16, M22, M27.

## 9. Wallets, signing and Sign In With MOI
- **Order:** a key signs an interaction; the MOI Wallet holds keys and signs for the user, and a site never sees a recovery phrase; a new wallet is a keypair the chain has not heard of until its account exists; Sign In With MOI is one signed message checked off chain, with no fee; derivation paths decide which account a phrase opens. Every step that touches a recovery phrase is the operator's.
- **Authority:** `build/moi-wallet` ("Security Model"); glossary rows MOI Wallet, Sign In With MOI; `devnet.md` "Silent failures"; `consent-and-identity.md` section 5; `docs/dapp-conventions.md` on `master` of `sarvalabs/moi-mcp` (public).
- **Test:** A funded wallet shows "account not found". Name the causes.
- **Wrong pictures:** M13.

## 10. Devnet, resets and the network ID
- **Order:** say "devnet"; a reset wipes accounts, assets, contracts and registrations; the release note, the source tip and the running node are three things; how to read the node (version, network ID, field names); network ID, not chain ID, and a CAIP-2 format that is undecided. <!-- slop-lint:ignore -->
- **Authority:** `devnet.md`; `moi-devrel/claim-check/references/live-reads.md`; `terminology.md` Contested 1; `learn/fundamentals/networks`, a stub on 2026-10-03. Read on 2026-10-03: `net.Version` answered 0.13.0 (15:32 UTC) and `net.NetworkID` answered -32601, method not found. Do not publish a network ID. ASK: Rahul, then Gokul.
- **Test:** How do you know a feature is live on devnet?
- **Wrong pictures:** M20, M21, M25, M26.

## 11. x402, HTTP 402, the facilitator, CAIP-2 and CASA
- **Order:** HTTP 402 is a status code; x402 is the agreement about what goes inside the response; the two-request flow with a named example; who verifies and who settles, the facilitator; the three flows (authorization, upfront, escrow), of which MOI's first scheme declares upfront; why a chain needs a CAIP-2 name and what CASA is; what "x402 compatible" means for MOI (a namespace, a scheme spec and a mechanism package, filed in that order); why network identification matters on MOI.
- **Authority:** on branch `claude/agent-payments-simple` of `moi-foundation/MOI-Webinars`: `x402-compat/x402.md`, `FINDINGS.md`, `UPSTREAM.md`, `review-package/`. The package has uncommitted edits dated 2026-10-01 that exist only on the previous operator's machine (ASK: Adithya for a copy). Upstream and public: `x402-foundation/x402` (`specs/schemes/exact/`) and `ChainAgnostic/namespaces`. Glossary rows x402, Facilitator, CAIP-2 and CASA. The filing process: `moi-standards-submission`.
- **CASA:** chainagnostic.org names it the Chain Agnostic Standards Alliance (read 2026-10-03), which the glossary still lists as undefined. Nothing was filed upstream as of 2026-10-02.
- **Test:** Any x402 client can read a MOI seller's invoice. Can any x402 client pay it?
- **Wrong pictures:** M17 to M19, M29. **Ask:** Rahul for the review gate.

## 12. How MOI's own sites ship
- **Order:** merge to the default branch is deploy for the website, Dataroom, Explorer and Launchpad; workflow, image, Teleport, VM script; the moidocs, voyage-docs and coco-docs sites publish through Cloudflare Pages with a preview per branch (the js-moi-sdk docs pipeline is unknown, ASK: Gokul); then the words people asked about.
- **Authority:** `moi-devrel/references/repo-map.md` ("How things deploy"), `moi-devrel/SKILL.md` fact 1, `moi-devrel/ship`, the ops skills. The terms the previous operator asked about (apex, CNAME against A record, TLS, cutover, cron secret) have no glossary row. ASK: Upendhar for MOI's actual setup before you explain them.
- **Test:** A pull request is merged and the run is green. Is the change live?

## 13. Visibility and marketing tools
- GEO has a glossary row. Buffer, Mailchimp, GA4, Search Console and Tag Manager were each asked about ("what's Buffer", "what's GSC and GA", 2026-08). They belong to `moi-docs/geo` and `moi-blog`. Who holds each account: `moi-devrel/references/keys-and-access.md`, ASK: Rahul.

## A concept with no block here
The docs list ten Fundamental Concepts pages: Accounts, Assets, Access Control, Execution, Interactions, Logics, Multi-Sig, Networks, Storage and Tesseracts, plus a Whitepapers page and a Guard section (read 2026-10-03). Multi-sig, storage cost, events and the guard section (guardians) have no block above.
1. Read the page for the concept and take the order from its headings, shallowest first.
2. Check the glossary. A term it lists as undefined (guardian, validator) is an ASK for Gokul, not a guess.
3. Use the same test: one question the operator answers at depth 2. Name the authority and the date you read it in the hand-back.
4. If the concept recurs, tell the operator it deserves a block, and write down the order you used.

## Not yet known
- The dedicated docs page on inherited accounts ("coming soon" on the Accounts page).
- Whether MAS1 is protocol-native, and what PISA and MERU stand for. ASK: Gokul.
- Where the repo for `js-moi-agent-registry` is. ASK: Gokul.
