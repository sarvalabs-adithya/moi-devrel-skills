# Webinar session notes (archive)

Only the material worth reusing is kept: the intro session deck and session 7. The older notes (the sessions 1 to 4 runbooks and the vibecode plan) were removed on 14 October 2026 and are in the handover repo's git history.

Archived working notes for **MOI Builders**, the developer webinar series that MOI DevRel runs: a live session in which one project is built on MOI in front of developers. MOI is a blockchain protocol built by Sarva Labs and governed by MOI Foundation. Adithya (DevRel) wrote these files over several months and left on 14 October 2026.

Read this page first. The files were written at different times for different purposes, so some of them disagree. Each one now starts with a short header saying what it is, which session it belongs to, and its status (delivered, plan or superseded). Where a later file overrides an earlier one, the earlier file says so in its header. Where the notes do not settle the question, the file says "not settled in these notes" instead of choosing.

## Where the code is

The code for the sessions is not in this repo. It lives in https://github.com/moi-foundation/MOI-Webinars, one folder per session (`session-1/`, `session-2/`, and so on). Paths such as `session-4/`, `packages/agent-buyer/...` or `extras/swap-cli.js` in these notes are paths inside that repo. Sessions 8 and 9 and the x402 work are on the branch `claude/agent-payments-simple`, not on `main` (as recorded in `skills/moi/moi-webinar/references/session-history.md`).

## What is here

| File | Session | What it is | Status |
| --- | --- | --- | --- |
| [intro-session-deck/README.md](./intro-session-deck/README.md) | Intro session (not numbered) | How to open, present and re-export the deck "Your first agent on MOI" (`index.html`, `MOI_Builders_Intro.pdf`). | Deck built 12 to 15 September 2026. Whether it was held is not recorded. `index.html` had two known faults when checked on 2026-10-02 (see its header). |
| [session-7/TRANSCRIPT.md](./session-7/TRANSCRIPT.md) | 7 | The short script for session 7, "agentic payments, part 1": a buyer agent finds a seller on the registry, checks who it is paying, then pays. The full script is in the deck's speaker notes. Despite the name, it is a script, not a transcript. | Delivered (Friday 7 August 2026, inferred). **Latest and canonical for session 7.** |
| [session-7/DEMO-PLAN.md](./session-7/DEMO-PLAN.md) | 7 | Terminal version of the demo plus the break-glass table (what to do when something fails). | Delivered in part; superseded in part by TRANSCRIPT.md (product name, tamper beat, browser gap). |
| [session-7/STORYLINE.md](./session-7/STORYLINE.md) | 7, 8, 9 | The three-phase plan (identity and payment, authority, conditional settlement) written after the 4 August 2026 strategy call. | Plan, superseded in part (session 8 became access policies; session 9 is still only a plan). |
| [session-7/FACILITATOR-NOTE.md](./session-7/FACILITATOR-NOTE.md) | 7 and 9 | Internal note for Rahul: "can we still call it x402 without a facilitator?". | Analysis, superseded in part: later files place x402 in session 9, not session 7. |

## Open points the notes do not settle

These are the contradictions left marked in the files. Do not guess; ask Rahul or Gokul, or check against devnet.

- **Escrow on MOI.** Whether MOI's native lock and release counts as escrow-style settlement: the session 4 runbook (removed 14 October 2026, in git history) said true atomicity still needs a contract; `TRANSCRIPT.md`, `STORYLINE.md` and `FACILITATOR-NOTE.md` call it native; `DEMO-PLAN.md` says escrow-style settlement is not available.
- **What session 9 is.** Conditional settlement or escrow (`STORYLINE.md`, `FACILITATOR-NOTE.md`) or the x402 envelope (`TRANSCRIPT.md`, `session-history.md`). The numbering after session 8 is also open (see `skills/moi/moi-webinar/SKILL.md`).
- **Mock mode.** `STORYLINE.md` says the built demos run with `CHAIN_MODE=mock`; `DEMO-PLAN.md` says there is no offline mode.

## Related files elsewhere in this repo

- `project-handover-docs/DEV-WEBINARS.md`: how a Builders session is run end to end (who owns what, the schedule, posting, the bounty).
- `skills/moi/moi-webinar/`: the skill that plans and runs a session. `references/session-history.md` has one row per session with dates and where each lives; `templates/` has blank runbook, Luma, social and game-day files; `examples/session-8/` is a filled-in set from the most recent held session.
- `skills/moi/moi-devrel/references/glossary.md`: the full MOI glossary.

## Glossary

| Term | Meaning |
| --- | --- |
| MOI Builders | The developer webinar series DevRel runs. |
| Devnet | MOI's public test network. Funds are test funds. A reset wipes every account, asset and contract. |
| Voyage | MOI's explorer and tooling site (voyage.moi.technology). It also hosts the devnet faucet, which sends test tokens. |
| Coco (Cocolang) | MOI's smart-contract language. |
| CocoLab | A local sandbox, started with `coco lab init`, for running Coco modules without a network. |
| Logic | A program deployed on MOI, written in Coco. |
| Interaction | MOI's word for a transaction: a signed request to change state. |
| Fuel | What running an interaction costs, paid in MOI's native token (KMOI). |
| KMOI | The native token of the MOI network. |
| MAS0 | MOI's standard fungible-token asset. No token contract is written; protocol calls (create, mint, transfer, lock, release) do the work. |
| MAS1 | MOI's standard non-fungible (NFT) asset. |
| MASX | A custom asset whose behavior is written in Coco (for example the Session 2 `TaxToken`). |
| Mnemonic | The 12-word phrase that derives a wallet's keys. Demos use devnet test wallets only. |
| TKA / TKB | The two test tokens created for the Session 4 swap. |
| Lockup / Release | MAS0 calls: the first sets funds aside for a named beneficiary; the second is the beneficiary pulling them. |
| Agent registry | An on-chain list where AI agents publish an identity (owner, wallet, a link to a card) so others can find them. |
| OpenClaw | A third-party AI agent framework used in Session 3. A *skill* is a folder with a `SKILL.md` that tells the agent which scripts it may run. |
| x402 | An open standard for paying over HTTP 402 (Payment Required). |
| Facilitator | In x402, the service that verifies a payment and settles it so the seller never touches a blockchain. |
| Bounty | A reward for viewers who complete a task from the session and submit proof (asset ids, a transaction hash). |
| Vibecode | To build software by describing it to an AI coding agent and running what it writes. |
