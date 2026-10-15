# Demo standard

Facts are as of 2026-10-02. The code standard for a live demo, taken from sessions 7 and 8 (the build log and scripts of `session-8-policies/`). Every demo is real devnet: nothing is mocked, and anything simulated is said aloud. Running any script below that spends devnet funds, deploys a logic or creates an asset needs the operator's yes (`moi-devrel/references/consent-and-identity.md`, section 1). Reading is free. Back to `../SKILL.md`.

## Rules

1. **The chain is always real.** "No mock mode for chain, chain always has to run" (the previous operator, August 2026). Session 7's README says "No offline mode". An early storyline claimed sessions were "green in mock mode"; that was stale, and neither session had then run on funded devnet.
2. **Say plainly when something is simulated or prepared in advance** (house rule 5). Session 7 was presented with two agents registered earlier and no tamper beat, because registry writes were down. Its transcript told the presenter to run the happy path only and never to say the retired agent ids.
3. **Prove before building.** A spike first, then the demo.
4. **Happy path, then one refusal that is not ours.** The refusal must come off the chain, with its own error text.
5. **Small files, shown whole.** A file on screen fits without scrolling: `identity-check.ts` was 42 lines when its deck was built (56 on 2026-10-02, after a later fix), `ticker.coco` is 30, `tick.ts` 27. Only the files being talked about are shown.
6. **A long "why" comment heads every script.** The code is read live and by students.
7. **Models get judgment, code gets money** (session 7). Model output is clamped by arithmetic in code.

## Build order

1. **Scaffold from the previous session.** Copy the folder forward, then rename. Fix the `.env.example` header: the first-design `session-8/` folder and `session-9/` still say "#7" (`session-preflight.sh` warns). Pin an SDK version that you have run against the current node: earlier sessions pin 0.7.x to ^0.8.0, and as of 13 October 2026 npm latest for `js-moi-sdk` is 0.9.0-rc2 (rc3 is on GitHub only), and the Launchpad, Explorer and MCP pin 0.9.0-rc2. Coco 0.9.3 targets PISA 0.8.2. Check npm for the published version before quoting one. ASK: Gokul which version targets node 0.13.0.
2. **Spike the mechanism alone.** `scripts/spike-<name>.ts` states in its header what it proves or kills. Session 8: `npm run spike:policy` creates, reads, updates and deletes one policy. A node can be probed without spending: a missing RPC method answers `-32601`, a present one answers a domain error.
3. **Verify SDK claims with keys the script generates itself.** Session 7's `verify-sdk.ts` produced every claim marked verified live (63 assertions per its README) and reports "unverifiable without funds" rather than assuming.
4. **Numbered, idempotent setup scripts that write ids back to `.env`.** Session 8: `00-fund-agent.ts` (the owner creates the agent with `ParticipantCreate` and sends KMOI), `01-deploy-ticker.ts` (deploys the logic, writes `LOGIC_ID`). A rerun reuses what exists. Compile first with `coco compile` (not `coco build`), which needs a `coco.nut` beside the source.
5. **`preflight.ts`, read-only.** It checks in dependency order (RPC up, accounts exist, fuel, asset, the feature's RPC method, `LOGIC_ID`), names the reset signature (the recovery phrase and the address are fine, the chain was wiped, and the SDK answers "account not found"), prints what to run next and exits non-zero on failure.
6. **`demo.ts`.** A banner per step, `DEMO_PAUSE_MS` for narration pace, an exit code that reflects pass or fail, and a summary box whose title flips to "DEMO DID NOT BEHAVE AS EXPECTED".
7. **An adversarial suite** when the claim is about refusals (`attack-test.ts`, sessions 7 and 9). Each forgery must fail for its own reason, and one honest control must pass, "because a verifier that rejected everything would otherwise pass". It makes real transfers and takes minutes.
8. **One small script per live action** (session 8: `tick.ts`, `grant.ts`, `revoke.ts`, `policy.ts`, 12 to 27 lines each), run with plain `node scripts/tick.ts`, the way a developer would. `npm run demo` stays as the rehearsal and the self-checking version. Session 8 presented the per-beat scripts, not the full run.
9. **Receipts into `NOTES.md`** (below). **A recorded clean run** for the fallback (`recording.md`).
10. **Presentation mode.** A `.vscode/settings.json` in the session folder hides everything but the code and the demo. `.vscode/` is ignored at the repo root, so each machine makes its own. Session 8's:
    ```json
    {
      "files.exclude": { "deck": true, "social": true, "recording": true, "*.md": true,
                         "**/.env": true, ".vscode": true, "node_modules": true, "package-lock.json": true },
      "search.exclude": { "deck": true, "social": true, "recording": true, "*.md": true },
      "editor.fontSize": 18
    }
    ```

## Where the code to copy lives

Session 8's code is on `main` as `session-8-policies/` since 2026-10-14 (session 7's is on both `main` and the branch). Read a file without switching branches: `git fetch origin claude/agent-payments-simple`, then `git show origin/claude/agent-payments-simple:session-8-policies/scripts/preflight.ts`. A fetch only reads from the remote.

| To copy | File in `session-8-policies/` |
|---|---|
| Read-only preflight with the feature probe | `scripts/preflight.ts` |
| A spike that creates, reads, updates and deletes | `scripts/spike-policy.ts` |
| Setup that funds the agent and deploys the logic, and writes `.env` | `scripts/00-fund-agent.ts`, `scripts/01-deploy-ticker.ts`, `scripts/env-file.ts` |
| The self-checking demo with the right-reason guard | `scripts/demo.ts` |
| One script per live action | `scripts/tick.ts`, `grant.ts`, `revoke.ts`, `policy.ts`, `counter-lib.ts` |
| Receipt and RPC helpers, banners and the pause setting | `packages/shared/src/chain.ts`, `config.ts`, `log.ts` |
| An adversarial suite with a control | `session-7/scripts/attack-test.ts` |
| Live verification of SDK claims | `session-7/scripts/verify-sdk.ts` |

## What "verified" means

Three levels. Label each claim with its level in `NOTES.md`; only the third may be stated as fact on stage without a qualifier.

| Level | Means | Example |
|---|---|---|
| Doc-derived | A docs page or note says it | "Foreign reads need no policy", before 1 Sep |
| Source-derived | Read in installed SDK or package source, with file and function | The `Access` builder exposes `.storage()`, `.allow()`, `.caller()`, `.origin()` |
| Receipt-proven | A devnet interaction shows it, hash kept | Origin pinning: a third account was refused with the same error while the agent wrote under the same policy |

Rules of evidence:
- **Success is the interaction-level `status: 0`.** Session 8 measured a failed policy attempt as `status: 1` with `ix_operations[0].status: 0`. A broadcast acknowledgement proves nothing, and a simulation accepts what the chain later refuses (`moi-devrel/references/devnet.md`).
- **A refused MAS0 pull returns an interaction hash and no error.** The only oracle is a balance difference. Show balances, never receipts.
- **A refusal counts only for the right reason.** In an early run on 31 Aug 2026 beat 3 "passed" because the agent had run out of KMOI. `isPolicyRefusal()` now requires `AccessError` in the text; anything else prints "stopped, but NOT by a policy" and exits non-zero.
- **Guard the guard.** The demo refuses to start if the agent cannot cover `FUEL_LIMIT * 3`. It was tested by forcing it: `FUEL_LIMIT=50000 npm run demo` stops at once. Rerun that now and then: a guard nobody has seen fire is not a guard.
- **Pin `fuel_limit` on a call that must be refused.** Without it `send()` runs a client-side simulation and throws before submission, which looks as if the SDK protected the owner. With it, the interaction is mined, charged and refused on chain.
- **Self-heal leftovers before beat 1** (a policy from a crashed run; a tampered registry entry, restored with up to four retries in session 7).
- **Keyed model calls.** Without `GROQ_API_KEY` the buyer matches keywords and can pick the wrong market on screen. Confirm that "decided by" shows the model name, never `local-fallback`. Session 7 measured 5 questions by 5 runs with zero drift before saying so.
- After any code change, **recount** every figure the docs quote (lines of code, number of forgeries).
- After any correction, **search every document and the deck notes** for the old claim (`traps.md`, item 12).

## Receipts: what to keep

Keep every interaction hash **in full**, with its status, fuel, date and the node version from `net.Version`. A reset wipes the hashes, and the date and version are what make an old hash meaningful. The session 8 build notes abbreviate hashes to ten characters, which cannot be looked up: do not copy that. The previous operator asked for each hash in the post to link to the explorer. The explorer URL pattern for an interaction is not on record, and the committed session 8 post file has plain code-fenced hashes. ASK: Gokul for the pattern.

## Constants and numbers

Everything here was measured on node 0.12.0 before v0.13.0, unless it says otherwise. Re-measure on the current node.

- **Take constants from the SDK, never from a literal:** `KMOI_ASSET_ID`, `DEFAULT_FUEL_PRICE` (`moi-devrel/references/devnet.md`, "Before you say live", step 4).
- **Numbers of record, session 8, node 0.12.0, 31 Aug to 4 Sep 2026:** a refused write 86 fuel, a permitted write 134, a policy create or delete about 100, a plain transfer 299, `ParticipantCreate` 399, a logic deploy 719. One full run cost 506 KMOI (agent 306, owner 200) per `GAMEDAY.md`; `RUNBOOK.md` said about 600. These predate v0.13.0. Quote none of them without re-measuring.
- **A policy write needs a well-funded owner.** `insufficient funds` appeared at about 10,000 KMOI and the write worked at about 109,000. The threshold was never measured, and the error reads like a fuel problem when it is a balance problem.
- **Fuel limits are checked against balance up front,** so a high `FUEL_LIMIT` fails as insufficient funds. The default was 1500.
- **A logic deploy bundles a storage fund.** The SDK default was 1,000,000, more than a devnet wallet holds, so session 8 passed 6,000. v0.13.0 raised the default, so re-measure.
- **You cannot transfer to an address that does not exist.** Create it with `ParticipantCreate` (minimum key weight 1000) and carry the opening balance in the same interaction.
- **Read another account's balance with the RPC `moi.Balance`.** The asset driver returns empty for any account but the signer.
- **Registry reads:** use `getAgentsByOwner`. `getAllAgentIds` reverts at about 135 agents and the SDK returns an empty list.
- **Derivation paths.** Faucet wallets use `m/44'/6174'/7020'/0/0`, the wallet extension account in session 8 used `m/44'/6174'/1'/0/0`. A wrong path gave "account not found" everywhere.
- **Runtime errors print as hex.** `decodeRuntimeError()` in `packages/shared/src/chain.ts` lifts the readable text so a refusal can be read on a projector.

## What is said when something is simulated or not live

- Say it in the script, the deck and the post, in the same plain words each time.
- The exact guardrail phrases of sessions 7 and 8: "the chain refuses the spend", never "the agent can't touch the money". "Only storage is live; asset, logic and key policies are reserved." The probabilities are invented, said before anyone asks. "Scan", not "search", for registry discovery. Do not call session 7 x402. Never write a shape you cannot demo (session 8 left `withinPrefix()` off because the network does not enforce it).
- Recorded fallback line: "Devnet's having a moment, so let me show you the recorded run. Every hash in it is on chain."
- A recording is a real run on a stated date. Say the date if it is not from today.

## Wallets and secrets

- `.env` comes from `.env.example`. Claude never opens it, and the operator types the recovery phrase into it. Claude never handles a recovery phrase, including a throwaway one.
- A script that loads the recovery phrase from `.env` is a wallet step: `npm run preflight`, the setup scripts, the demo and every per-beat script. The operator runs it in their own terminal and pastes the output. Claude reads output only and writes the scripts, never runs them.
- The faucet (voyage.moi.technology/faucet) funds only accounts that already exist, and documents quote its amount differently (20K KMOI in one, 100K in others): read it live before telling attendees how much they get.
- Session 8 derived the owner and the agent from one wallet by two derivation paths. The chain sees two unrelated accounts. Say so on stage, as the script did.
- Never read or confirm seed words on a recorded call (2026-09-24: a phrase reached Gemini notes).

## Not yet known

- Whether the session 8 demo passes on devnet 0.13.0 today. It needs a rehearsal and the operator's yes.
- Which Node versions run `node scripts/tick.ts`. The author's shell was Node 24 and `engines` says 20 or newer. Not recorded (the previous DevRel's notes): run the script on the Node version you will quote, in the rehearsal, before the event page names one.
- The explorer URL pattern for a hash. ASK: Gokul.
