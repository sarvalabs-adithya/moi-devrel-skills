# Example: MOI Builders session 8, access policies (Fri 2026-09-04)

The one finished run on file that has the full document set: the cleanest example of the mature format. Read it to learn the shape, then follow `../../references/`. Do not copy its sentences. Facts are as of 2026-10-02.

The session: an agent makes the same call three times and it is refused, allowed, then refused, because the only thing that changes is an access policy on the owner's account. 60 minutes at 16:00 IST (10:30 UTC), live on devnet, one funded wallet. Source folder: `session-8-policies/` on the branch `claude/agent-payments-simple`. Where each document lives is in `../../references/session-history.md`.

"Local only" below means the original exists only on the previous operator's machine (ASK: Adithya for a copy).

## What is in this folder

| File here | Original | Reader | Template in `../../templates/` |
|---|---|---|---|
| `session-README.md` | `README.md` | students | `README.md` |
| `NOTES.md` | `NOTES.md` | the presenter | `NOTES.md` |
| `RUNBOOK.md` | `RUNBOOK.md` (local only) | the presenter | `RUNBOOK.md` |
| `GAMEDAY.md` | `GAMEDAY.md` | the presenter | `GAMEDAY.md` |
| `SCRIPT.md` | `SCRIPT.md` | the presenter, read aloud | `moi-webinar/deck/templates/SCRIPT.md` |
| `LUMA.md` | `LUMA.md` (local only) | the event page | `LUMA.md` |
| `SOCIAL.md`, `social-posts.md` | `SOCIAL.md`, 13 of 25 files in `social/` (local only) | X and LinkedIn | `SOCIAL.md` |

Not copied: the code, `.env.example`, the deck, the recording and voiceover, and `BLOG.md` (the post belongs to `moi-blog`, and as of 2026-10-02 it is not published). No `.env` was read.

## What was changed in these copies

1. Em dashes became hyphens, because no document in this library carries an em dash.
2. Two reviewer names became "the reviewer" or "a reviewer". The original `README.md` and `NOTES.md` named one reviewer, and `GAMEDAY.md` and `RUNBOOK.md` named another. The words "on the 27th" went with the first name.
3. The three account and logic addresses in `NOTES.md` were left out.
4. "Voyage devnet" became "devnet" in one line of `NOTES.md`. The network is called devnet. <!-- slop-lint:ignore -->
5. `SOCIAL.md` lines that were kept on purpose carry a lint ignore marker.

Nothing else was edited (checked against the originals on 2026-10-02), so the faults below are the original's.

## What this run got right

1. **Spike first.** The first design was dropped on 31 Aug 2026. The new demo was verified end to end the same day, which the research reads as the spike showing the holes early (inferred). The old build was kept on disk with its reason written down.
2. **The demo was verified end to end the same day** and its receipts are in `NOTES.md`, each labelled by how it is known. The claim audit on 1 Sep turned two doc-derived claims into receipt-proven ones with live tests.
3. **It cannot go green for the wrong reason.** A refusal counts only when its text names the access error, and the demo will not start if the agent cannot afford three calls. The guard was forced once and its result written down.
4. **One small script per live action,** run with plain node, so the code a developer reads is the code that ran.
5. **A game day checklist with a recorded fallback,** a dated "known state" block, and a fallback line written into the script.
6. **An honest-scope slide near the end,** so the answer to "can I cap spending?" was already on screen. The run sheet's single rule is not to claim more than the screen shows.
7. **A run sheet with a cumulative clock, a cut rule, likely questions and a recovery table.**
8. **A script of complete spoken sentences** with a banner line per slide change and stage directions that are not read out. The voice rules are the deck branch's (`moi-webinar/deck/references/spoken-script.md`).
9. **Posts that escalate** from announcement to "we're live", with no emoji and no em dash in all 25 files.
10. **The event page said up front what was not live.**

## What went wrong

1. **The event page said VII before game day.** The run sheet, `LUMA.md` and the checklist each carried a reminder to fix it (1, 2 and 3 Sep, by file times). As of 2026-10-02 the live page reads "MOI Builders VIII - How to stop an AI Agent From Spending Your Money", so it was fixed, and it no longer matches `LUMA.md`.
2. **Slide numbers are off by one.** The run sheet and checklist say 18 slides and "slide 12" for the check. The deck has 19 and the check is slide 13.
3. **Three talk lengths:** about 30 minutes in the script, about 24 in the checklist, 60 in the run sheet. The run sheet prescribes the full `npm run demo` as the live command, while the script runs four per-beat scripts, which is what was presented.
4. **The dropped design leaked into public copy.** On 31 Aug 2026 the previous operator rejected the first posts because they still referred to why session 8 was not run as first planned, and the posts in `social/` were rewritten. `LUMA.md` and `SOCIAL.md` were not: both still argue from a budget contract and a lockup. The live page's description begins with the opening of `LUMA.md`, so the lockup paragraph is probably still on it (inferred).
5. **A reviewer's name and the dropped design sit in tracked files.** The original `README.md` and `NOTES.md` are on a public branch. They also say the reviewer rejected the first design "on the 27th", while the call on file is 31 Aug (`../../references/lifecycle.md`).
6. **The write-up is not published.** The post's address returned 404 on 2026-10-02, and a pull request holds an old draft.
7. **The bounty and the docs page were not live when the checklist was written (3 Sep),** and it told the presenter to announce the bounty as coming.
8. **Receipts are abbreviated.** `NOTES.md` shows hashes cut to ten characters, which cannot be looked up. Keep them whole.
9. **`.env.example` still shows the faucet derivation path,** while the owner account actually used was another path.
10. **The deck as pushed fails the deck branch's checker today** (`moi-webinar/deck/scripts/check-deck.py`, run read-only on 2026-10-02): 2 FAIL (neighbouring slides share a background, and em dashes) and a warning about an unbalanced tag. An earlier run with `--layout` also reported overflowing slide content, which the re-run could not measure.
11. **Numbers are from node 0.12.0.** Every figure (86 fuel, 134, 506 KMOI a run, 88,000 balance) predates v0.13.0.
12. **"Node 20 or newer" on the page** was not the version the live scripts needed (`../../references/demo-standard.md`).
13. **`SCRIPT.md` writes its cues in italics,** for example `*(wait for the refusal)*`. The presenter window shows plain text and the two copies must match word for word, so a new script writes each cue in square brackets without markdown: `[WAIT FOR THE REFUSAL]` (`moi-webinar/deck/references/spoken-script.md`, "Cues"). Four of this script's 19 sections differ in cue notation from the deck notes.

## Lines that must not be copied

| Where | The line, in short | Why |
|---|---|---|
| `session-README.md`, "Why this session exists" | The two paragraphs on the budget contract and the reviewer's phrasing | The dropped design and a reviewer. Public copy names neither |
| `NOTES.md`, "Why the design changed" | The whole section | The same, and it is internal |
| `LUMA.md`, description | The paragraph beginning "Lock the asset up" | Argues from the dropped design |
| `LUMA.md`, bring | "Node 20 or newer" | Not the tested version |
| `SOCIAL.md`, thread posts 2 and 3, and the LinkedIn paragraphs on a budget contract and lockup | "a gate with no fence" and the lockup argument | The dropped design, replaced by the posts in `social-posts.md` |
| `SOCIAL.md`, LinkedIn opening | "Most teams building AI agents set spending limits in a config file" | Vague attribution that cannot be cited. The previous operator cut the same shape on 31 Aug 2026 | <!-- slop-lint:ignore -->
| `SOCIAL.md` and `social-posts.md` | "Not its key, not its code, not one line of the program", "You're not constraining it. You're asking it nicely", "Not inside the program, not inside the agent" | Contrast constructions. House style bans them | <!-- slop-lint:ignore -->
| `social-posts.md`, the LinkedIn post | "You quietly accept both" | Close to a line already cut as vague |
| `RUNBOOK.md`, `GAMEDAY.md` | Every slide number, "18 slides", "about 24 minutes" | Off by one, and the lengths conflict |
| `RUNBOOK.md` | `DEMO_PAUSE_MS=1500 npm run demo` as the live command | Not what was presented |
| `RUNBOOK.md`, `GAMEDAY.md`, `SCRIPT.md` | The numbers 86, 134, 506, about 600, 88,000 | Measured on node 0.12.0 |
| `SCRIPT.md`, slide 6 | "The ethereum.org documentation states it directly" | An external claim no one checked for this copy. Put it in the ledger |
| `SCRIPT.md`, slide 17 | "Ethereum's allowances genuinely bind. Solana's runtime genuinely enforces" | A comparison with other chains: claim-check it |
| `SCRIPT.md`, the questions | "Getting past it would require the network's validators to run a different VM" | An absolute claim the demo never showed |
| `SCRIPT.md`, slide 14 | "node runs TypeScript directly these days" | Version dependent, and a relative time word |
| `SCRIPT.md`, slide 18 | "Everything I demoed is reproducible today" | Depends on devnet today. Rehearse before saying it |

## How to use this example

1. Read `RUNBOOK.md` and `GAMEDAY.md` beside the templates to see which sentences became placeholders.
2. Read `SCRIPT.md` for rhythm: how a long script carries a demo with cues, then `moi-webinar/deck/references/spoken-script.md` for the rules.
3. Read `NOTES.md` to see a verified-live log, then keep your hashes whole.
4. Write your own claims. Run each through `moi-devrel/claim-check` before it is said or posted.
