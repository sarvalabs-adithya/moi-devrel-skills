# Traps: facts that fail silently

Facts are as of 2026-10-02. Each entry is a rule with the incident behind it. They produce a wrong result with no error. Back to `../SKILL.md`.

## The demo

1. **A green demo can be green for the wrong reason.** A broke agent and a forbidden agent both stop, and on screen they look alike. On 31 Aug 2026 beat 3 "passed" because the agent had run out of KMOI. Require the refusal text, check the balance first, and force the guard once (`demo-standard.md`).
2. **A refused MAS0 pull returns a hash and no error.** Read a balance difference, not a receipt (sessions 7 to 9 READMEs).
3. **Fuel and balance are different limits.** A policy write failed with `insufficient funds` at about 10,000 KMOI and worked at about 109,000, and a fuel limit above the balance is refused up front (31 Aug 2026). The error reads like a fuel problem.
4. **A wrong derivation path gives "account not found" everywhere** for a funded wallet. The faucet path is `m/44'/6174'/7020'/0/0`, the wallet extension account used for session 8 was `m/44'/6174'/1'/0/0` (31 Aug 2026). The session 8 `.env.example` still shows 7020.
5. **A reset wipes accounts, assets, logics and agent registrations,** and the SDK says "account not found", which reads like a bug in your code. Run `npm run preflight` first (`moi-devrel/references/devnet.md`, reset history: 2026-08-15, and 2026-09-11 as announced).
6. **A recorded fallback ages.** Its hashes probably vanish at a reset, so "every hash in it is on chain" can become false (`recording.md`).
7. **A crashed run leaves state.** A leftover policy made beat 1 write; a tampered registry entry made the happy path refuse (session 7). Self-heal before beat 1 and rerun to completion.
8. **Registry limits.** Registry writes were failing around session 7's build (`devnet.md` dates a registry failure to 2026-08-06), which forced its pivot to two existing agents. `getAllAgentIds` reverts at about 135 agents and returns an empty list. Use `getAgentsByOwner`.
9. **A source-tip feature is not live.** Devnet lagged the source in September 2026. Check the wire fields, not the release notes (`devnet.md`, "Before you say live").
10. **Node.** The live scripts run `.ts` files with plain `node`, which needs a recent Node. The packages say `>=20` and the author used 24. Test on the presenting machine (`session-preflight.sh` warns).
11. **A keyless fallback picks the wrong market.** Without `GROQ_API_KEY` session 7's buyer matched keywords on screen. Confirm "decided by" names the model.

## Documents and claims

12. **A correction must be searched for in every file.** On 7 Aug 2026 the fact check proved "only the owner can move funds" false and fixed the post. The old sentence stayed in the README, the explainer, the demo plan, the transcript, the facilitator note and the notes of the presented deck.
13. **A pivot leaves stale documents.** The facilitator note described a package that was removed. The storyline said "mock mode". The demo plan pointed at a missing run sheet. The `.env.example` headers of the first-design `session-8/` folder and of `session-9/` still say "#7". Search after every pivot.
14. **Counts drift.** Forgeries were 11 in the README, ten in the post and twelve in session 9. Recount after every code change.
15. **Slide numbers drift.** The run sheet says 18 slides and the deck has 19 (read on 2026-10-02). Refer to slides by title. `session-preflight.sh` compares the stated count.
16. **A regenerated deck can look unchanged.** On 4 Sep 2026 the presenter notes stayed stale across at least six messages. Open the deck in a fresh tab and read one slide's notes back (the deck branch, `moi-webinar/deck`).
17. **Three talk lengths in three files** (about 30, about 24 and 60 minutes). Keep one clock, in the run sheet.
18. **Placeholders ship.** `<<< EVIDENCE >>>`, `REPLACE-WITH`, `LUMA_URL`, `EVENT_URL`, `CANONICAL_URL`, and the `FILL` markers of the templates. Search before anything is published or scheduled. <!-- slop-lint:ignore -->
19. **Do not claim a feature is live when only its type is declared.** Session 8: only storage policies are live, and asset, logic and key policies are reserved. Never write a shape you cannot demo.
20. **Do not say "published" about a draft.** Session 8's post returned 404 on 2026-10-02.

## Publishing, identity and secrets

21. **The event page numeral.** The page said VII for session 8 (by 2 Sep 2026). Read the live title the night before and again after any edit.
22. **A public branch shows its tracked files.** The branch `claude/agent-payments-simple` is readable by anyone as of 2026-10-02. Session 8's tracked `README.md` and `NOTES.md` name a reviewer and describe the dropped design. Strip both before anything is landed on `main`. The branch's root `.gitignore` keeps the run sheet, event page copy and social files out of git as instructor-only material. The `.gitignore` on `main` has no such lines (read on 2026-10-02), so a folder landed on `main` needs the ignore rules that `new-session.sh` writes into the session folder.
23. **Landing the folder.** All 95 commits on that branch carry an AI co-author trailer and 3 are authored under an AI identity, against house rule 4. The trailer cleanup of 2026-10-01 covered open pull requests only. Do not open a pull request from that branch without asking (`after-the-session.md`).
24. **Secrets in chat.** A Buffer key and a devnet recovery phrase were pasted into the chat on 31 Aug 2026, and the key was revoked. Secrets go in a gitignored `.env` the operator edits. Claude never handles a recovery phrase.
25. **Seed words on a recorded call.** A phrase read out on a screen share on 2026-09-24 reached the meeting notes. Never read or confirm one on a recording.
26. **Time notation.** The incident of 2026-09-10 is in `moi-devrel/references/terminology.md`, table C. Write a date, 24-hour UTC and IST, and use `time-table.sh` with `Asia/Kolkata`, never `IST`. <!-- slop-lint:ignore -->
27. **Medium first makes Medium canonical.** Decide the canonical copy before the first publish (`after-the-session.md`).
28. **Announce an unfinished bounty as coming.** On 3 Sep 2026 the checklist for the 4 Sep session said it was behind a flag and not live. The docs page was not merged either, so nobody was pointed at it.
29. **Notes mishear.** Gemini wrote "Moy" for MOI, "KOI" for KMOI and "Grock" for Groq. Check every name and amount.
30. **Hash links.** Requested for the post and not applied in session 8's committed file.
31. **Encoding.** An em dash became mojibake in a voiceover text file. Keep em dashes out of scripts.

## Reusing sessions 1 to 6

32. **BigInt in a `.send()` payload breaks signing.** Use plain numbers. An `.env` value with an inline `#` comment is not stripped. A stale compiled manifest runs the old logic after a `.coco` edit. `patch-package` must run after install in session 4. `release` on MAS0 with nothing locked "succeeds" and moves nothing. `AccountInherit` must be signed by the primary, and a zero seed transfer is rejected.
33. **Session 3 specifics.** The OpenClaw skill needs `MOI_MNEMONIC` in two places of its config. The message servers must bind dual-stack. The model key must be exported in the shell before the start script. A dead uploader makes registration hang. Run OpenClaw only in a container.
34. **Session III went wrong live twice,** from the wrong working directory and a discover script that did not load the list. Pre-flight every demo, and keep the fallback ready.

## Not yet known

- Why session 8's event page said VII, and whether the numerals ever matched the repo.
- Whether the reviewer's rejection of the first session 8 design was on the 27th, as the notes say, or on the 31 Aug call.
