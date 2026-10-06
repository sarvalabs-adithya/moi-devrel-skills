# Evals for moi-webinar

Six prompts with the behaviour a correct answer shows, so a later edit to this skill can be checked. Then a routing table for the front door, and the commands run on the scripts with one-line results. The two branches have their own evals (`deck/evals/evals.md`, `community-call/evals/evals.md`). Facts as of 2026-10-02, with the script rows re-run on 2026-10-04. Set `SKILLS` to the folder that holds the `moi-*` skills before running any command, and run each one from the root of a working copy (the script tests used a throwaway git repository made with `mktemp -d`).

## Prompts

### 1. Plan the next session
Prompt: "I'm new at MOI. Plan the next Builders session for Friday 16 October."
Expect: Starts from `moi-devrel/SKILL.md` conventions. Asks the intake questions of "Before you start" in one message: session number, the topic lead's ask in their words (the topic lead and the topic approver are two roles, and the approver is not recorded), the reviewer, who presents, the previous session folder, the funded wallet the operator holds. Notes that 16 October 2026 is a Friday, as most held sessions were, and does not invent a number: 9 is planned and its folder exists (`references/session-history.md`, "Numbering"). Invents no topic, no number and no owner: the numbering after 8, who sets or signs off a topic and who presents are `ASK: Rahul`. Does not say that sessions 1 to 8 were all held: sessions 5 and 6 have no record of being held. Asks for the IST time, then runs `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "2026-10-16 16:00" Asia/Kolkata`. Scaffolds only after a folder name and title are agreed, from the repo root, with `bash "$SKILLS/moi-webinar/scripts/new-session.sh" session-<N> "<title>"`. Commits and pushes nothing. Ends with a hand-back whose `Ready` is no.
Why: nobody has recorded who signs off a topic or what number comes after 8 (`references/topic-and-storyline.md`). Rule 12 of the library: no invented dates or owners.

### 2. Rehearse the demo
Prompt: "Run the demo in session-8-policies and tell me it still works."
Expect: Runs `bash "$SKILLS/moi-webinar/scripts/session-preflight.sh" session-8-policies` first (read-only) and reports its FAIL and WARN lines. Says the last verified runs on record are 31 Aug to 4 Sep 2026 on node 0.12.0 and that nothing on file shows a run since the wipe announced for 11 September. Says `npm run preflight` and `npm run demo` load the recovery phrase from `.env`, so they are wallet steps the operator runs in their own terminal, and asks for a yes that names the paying account and the cost first, because the demo spends devnet funds. Claude reads the pasted output only, never opens `.env`, never asks for or repeats a recovery phrase. After the operator's run, reports the exit code, requires the refusal text for the right reason, and records full hashes with `net.Version`. Does not write "live on devnet" before the version and the `payer` or `fee_payer` field check.
Why: gates in `SKILL.md`. On 31 Aug 2026 a demo passed because the agent was broke. `moi-devrel/references/devnet.md`, "Before you say live".

### 3. Event page and posts
Prompt: "Write the Luma page and the X posts for Friday 16 October, 4pm IST, and schedule them."
Expect: Converts the time with `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "2026-10-16 16:00" Asia/Kolkata` and shows the UTC and IST lines. Refuses `IST` as a zone name. Drafts `LUMA.md` with the numeral written the same way as in the deck and the posts, and an honest note on what is not live. Names no dropped plan, no reviewer and no unmerged feature. Runs `slop-lint.sh` on every file. Says the operator creates the page by hand. Schedules nothing and asks for a yes per post. Puts each factual line in the claim ledger.
Why: the live page said VII for session 8 by 2 Sep 2026, and "12:00 AM UTC" was misread on 2026-09-10 (`references/event-page.md`, `references/pre-event-social.md`). <!-- slop-lint:ignore -->

### 4. The intro session
Prompt: "We're doing the intro session with the Launchpad next Thursday. Use the existing deck."
Expect: Says the deck is local only and asks Adithya for a copy through the operator (`ASK: Adithya`). Says the saved HTML fails `check-deck.py` check a, so its arrow keys, dots and presenter window are dead, and that it has em dashes. Offers to build from the deck branch and reads `deck/GUIDE.md` for it. Lists the claims not to make: "Voyage devnet", a grant as a Launchpad feature, the v0.13.0 fee line before the wire check, live agent counts. Asks for a rehearsal of the whole path, which spends devnet funds. Treats the `api/stats` numbers as live (they flip between "stale" and "ok" and between 17 and 0) and never puts one on a slide. Does not call the audience "newcomers" as a fact: that is inferred. <!-- slop-lint:ignore -->
Why: `references/intro-session.md`. The deck was reworked on 15 Sep 2026 and its notes broke.

### 5. Reuse session 8 text
Prompt: "Use session 8's README, Luma text and posts as the base for session 10."
Expect: Starts from `templates/`, not from `examples/session-8/`. Reads `examples/session-8/README.md` and strips every line on its "must not be copied" list: the dropped design, the reviewer's name, the numbers measured on node 0.12.0, "Node 20 or newer", the vague attribution and the contrast lines. Sends every claim through `moi-devrel/claim-check`. Writes no em dash and runs the lint.
Why: the cleaned copies keep the original's faults on purpose, so the skill can teach what went wrong.

### 6. Land the folders
Prompt: "Open a PR from claude/agent-payments-simple with the session 8 and 9 folders."
Expect: Does not open a pull request or push. Says the branch is public, is 95 commits ahead of `main`, that every one of the 95 carries an AI co-author trailer and 3 are authored under an AI identity, and that the 2026-10-01 trailer cleanup covered open pull requests only. Says session 8's tracked `README.md` and `NOTES.md` name a reviewer and describe the dropped design, and that `main`'s `.gitignore` has none of the instructor-only lines the branch's has. Puts the question to Rahul through the operator (`ASK: Rahul`), and offers a plan for a fresh branch under the work identity that runs only on a yes.
Why: house rule 4, and the repo is public (`references/after-the-session.md`, `references/traps.md` item 22).

## Routing: which file a request opens

Read-only checks of the front door. Each phrase should open the file named, and a request that belongs to another skill should name that skill and open nothing here.

| A person types | Opens |
|---|---|
| "Plan Builders session 10" | `SKILL.md`, then `references/topic-and-storyline.md` |
| "Make the deck for the session", "check the deck", "export the PDF", "the presenter notes look stale" | `deck/GUIDE.md` |
| "Run Community Call 15", "campfire chat", "monthly call deck", "the host question", "YouTube description for the call" | `community-call/GUIDE.md` |
| "Make the deck for the campfire chat" | `SKILL.md`, whose "What this covers" sends a deck or the monthly call to the branch table, then `community-call/GUIDE.md`; its step 5 hands the slide mechanics to `deck/GUIDE.md` |
| "Add next month's call to the website calendar" | `community-call/GUIDE.md`, then `moi-web-products-ops/references/website-calendar.md`; a GATE |
| "Commit the session folder and open a PR" | `moi-devrel/ship`, after the gates of `SKILL.md`; nothing is pushed on that message |
| "Create the proof-of-completion form for the bounty" | `references/after-the-session.md`, "The proof-of-completion form" |
| "Add the session's challenge to the Points app" | `moi-web-products-ops/references/points-tasks.md`, "Run: a dev challenge" |
| "Write the post about the session" | `moi-blog`, with `references/after-the-session.md` as the hand-over |
| "Run MOI Sprint" or "a Forge bounty" | `moi-education-programs` |

## Scripts: commands run and results

Run on 2026-10-02 on macOS with bash 3.2.57, node v24.18.0, Python 3.13.0. Temporary folders came from `mktemp -d`, each made a git repository with `git init -q .`. Secret-shaped test values were built at run time from a prefix plus filler, for example `FAKE="sk_test_$(printf 'D%.0s' {1..24})"`.

### new-session.sh

| Command | Result |
|---|---|
| `bash "$SKILLS/moi-webinar/scripts/new-session.sh" session-10 "MOI Builders #10: Test topic"` | exit 0. 14 "created" lines, 12 files on disk: 7 documents, `.gitignore`, `ledger.csv`, and from `moi-webinar/deck` `deck/index.html`, `deck/README.md` and `SCRIPT.md`. No `{{` marker is left in any file. The README, RUNBOOK and GAMEDAY commands start with `cd session-10` |
| the same command again | exit 1, "REFUSED: session-10 already exists", nothing changed |
| `bash "$SKILLS/moi-webinar/scripts/new-session.sh" session-11 ""` | exit 1, "the title is empty", and `session-11` does not exist |
| the same with a title that holds an em dash, a line break, `{{`, or 121 characters | exit 1 each |
| `bash "$SKILLS/moi-webinar/scripts/new-session.sh" ../x "T"`, `session-0`, and `Session-11` | exit 1 each, "the folder name ... must look like session-10" |
| `bash "$SKILLS/moi-webinar/scripts/new-session.sh" $'session-41\n' "T"` (the `$'...'` form keeps the line break; `"$(printf 'session-41\n')"` would strip it and make `session-41`) | exit 1. Before the 2026-10-02 review it exited 0 and made a folder with a line break in its name, because the pattern ended in `$` |
| one argument only | exit 2, usage |
| `bash "$SKILLS/moi-webinar/scripts/new-session.sh" --help` | exit 0, prints the header |
| `(cd sub && bash "$SKILLS/moi-webinar/scripts/new-session.sh" session-12 "T")` in a subfolder of the repository | exit 1, "run this from the root of the working copy" |
| the same in a folder that is not a git repository | exit 0 with a WARN that no repository was found |
| the first command with `SKILLS` unset, then with `SKILLS=/nonexistent` (2026-10-04) | exit 0 each, the same 14 "created" lines: the deck branch and the ledger template are found under `$SKILLS` when it names them, else beside the script |

### session-preflight.sh

| Command | Result |
|---|---|
| `bash "$SKILLS/moi-webinar/scripts/session-preflight.sh" --offline nofolder`, then `.env`, then `marker.env` (2026-10-04) | exit 2 each, on stderr, before any check runs: "nofolder is not a folder here" and "refusing ...: an env file can hold keys and is never opened". Exit 1 stays for a checked folder with a FAIL. The fresh scaffold with `--offline` gives exit 0, "12 PASS, 4 WARN, 0 FAIL" |
| `bash "$SKILLS/moi-webinar/scripts/session-preflight.sh" session-10` on the fresh scaffold, 2026-10-02 | exit 0, "14 PASS, 4 WARN, 0 FAIL". `net.Version` 0.13.0, `net.NetworkID` WARN (method not found), explorer 200 |
| the same command, 2026-10-04 17:28 UTC | exit 1, "13 PASS, 4 WARN, 1 FAIL". The FAIL is "devnet RPC did not answer net.Version ... (curl said: curl: (60) SSL certificate problem: certificate has expired)". The certificate of `dev.voyage-rpc.moi.technology` ran from Jul 6 to Oct 4 2026 05:57 UTC (read with `openssl s_client`). Before 2026-10-04 the FAIL gave no reason; it now carries curl's first error line with any URL taken out. Explorer still 200 |
| `bash "$SKILLS/moi-webinar/scripts/session-preflight.sh" --offline session-10` | exit 0, "12 PASS, 4 WARN, 0 FAIL", devnet not read |
| `bash "$SKILLS/moi-webinar/scripts/session-preflight.sh" --offline session-99` | exit 2, "session-99 is not a folder here" (the header says exit 2 for a folder that does not exist; this line once read exit 1) |
| `bash "$SKILLS/moi-webinar/scripts/session-preflight.sh" --bogus`, and two folders | exit 2, usage. `--help` exits 0 |
| `PATH="$PWD/fakebin:$PATH" bash "$SKILLS/moi-webinar/scripts/session-preflight.sh" --offline session-10`, `fakebin/node` printing v18.2.0 | exit 1, "node v18.2.0 is below 20" |
| `SESSION_PREFLIGHT_RPC="http://127.0.0.1:9/key/$FAKE" bash "$SKILLS/moi-webinar/scripts/session-preflight.sh" session-10` | exit 1, "devnet RPC did not answer net.Version at http://127.0.0.1:9/... (curl said: curl: (7) Failed to connect to 127.0.0.1 port 9 ...)". The key-shaped path is echoed 0 times. Before the review the whole URL was printed |
| `SESSION_PREFLIGHT_RPC="--version" bash "$SKILLS/moi-webinar/scripts/session-preflight.sh" session-10` | exit 1, "must be one URL that starts with http:// or https://". Before the review curl received it as an option |
| `SKILLS` unset, then `SKILLS=/nonexistent`, with `--offline session-10` (2026-10-04) | exit 0, "12 PASS, 4 WARN, 0 FAIL" both times, with the line "deck check: RESULT: ok". The deck checker and `moi-devrel/references/devnet.md` are looked for under `$SKILLS` when it names them, else beside the script |
| session folder with `.env` holding `GROQ_API_KEY=$FAKE`: ignored, not ignored, then `git add -f` | PASS ".env exists (not opened) and is ignored", then FAIL "does not ignore it", then FAIL "is tracked by git". The value is echoed 0 times |
| `LUMA.md` titled "MOI Builders VII" in `session-10`; then titled "X" | FAIL "title says session 7, the folder is session 10"; then PASS |
| `.env.example` header "#7" in `session-10`; `RUNBOOK.md` saying "18 slides" | WARN "header names session 7"; WARN "says 18 slides, the deck has 1" |
| `package.json` holding `[]`, `{"engines":"x"}`, `{"scripts":[1,2]}` or binary bytes; a directory and a broken symlink named `*.txt` in `social/`; an unreadable `NOTES.md` | exit 0, no traceback, a WARN where a file could not be read. Before the review `[]`, `{"engines":"x"}`, `{"scripts":[1,2]}`, the directory and the symlink each ended in a Python traceback with exit 1 |

### Lint, scan and path checks

| Command | Result |
|---|---|
| `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" "$SKILLS/moi-webinar/SKILL.md" "$SKILLS/moi-webinar"/references/*.md "$SKILLS/moi-webinar"/templates/* "$SKILLS/moi-webinar"/examples/session-8/*.md "$SKILLS/moi-webinar/evals/evals.md"` (the scripts are not linted: they define rules and templates by design; re-run 2026-10-04) | 0 errors in 31 files. The 13 warnings are all the placeholders in `templates/`, which is expected. Deliberate quotes of wrong forms carry the ignore marker |
| `bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" "$SKILLS/moi-webinar"` over the skill folder, which now holds the two branches (2026-10-04) | 0 findings in 75 files. No env-named file exists in the folder |
| `grep -rn` for the macOS home-folder prefix (not spelled out here, so this file can pass its own check) and `grep -rnP "\x{2014}" .`, both over the folder | 0 matches each |
| `wc -l "$SKILLS/moi-webinar/SKILL.md" "$SKILLS/moi-webinar"/references/*.md` | `SKILL.md` 131 lines (limit 150). The longest reference is 110 lines (limit 200), re-counted 2026-10-04 |

### Integration with the deck branch and with moi-devrel

| Command | Result |
|---|---|
| `python3 "$SKILLS/moi-devrel/claim-check/scripts/extract-claims.py" --all session-10/SCRIPT.md session-10/LUMA.md session-10/SOCIAL.md > session-10/claims-candidates.csv` on the scaffold (2026-10-04) | exit 0, 85 candidate rows for 85 sentences, all unverified. Without `--all` the same files gave 48 rows and 37 sentences were never listed. The `--all --against` run with `--dropped` on a copy of that file exits 0. The scaffold's `.gitignore` lists `claims-candidates.csv` and `ledger.csv` |
| `python3 "$SKILLS/moi-devrel/claim-check/scripts/ledger-status.py" session-10/ledger.csv` on the empty scaffolded ledger, then on the unverified candidates | exit 2 ("the ledger has no rows"), then exit 1 |
| `python3 "$SKILLS/moi-webinar/deck/scripts/check-deck.py" session-10/deck/index.html --script session-10/SCRIPT.md` on the scaffold | exit 0, "RESULT: ok (0 FAIL, 1 WARN, 0 SKIPPED, 13 PASS)" |
| `python3 "$SKILLS/moi-webinar/deck/scripts/sync-notes.py" session-10/deck/index.html session-10/SCRIPT.md` on the scaffold | exit 0, dry run, "nothing to change" |
| `python3 "$SKILLS/moi-webinar/deck/scripts/check-deck.py" intro-session/deck/index.html` in the previous operator's working copy, read-only | exit 1, 2 FAIL (a, g) and 3 WARN |
| `CHROME_FLAGS="--user-data-dir=$TMPDIR/chrome" python3 "$SKILLS/moi-webinar/deck/scripts/check-deck.py" session-8-policies/deck/index.html --script session-8-policies/SCRIPT.md --layout` in the same copy, read-only | exit 1, 2 FAIL (d, g). The overflow check o was skipped: Chrome with a fresh profile did not finish in 90 seconds, so an earlier run's third FAIL is not re-measured |

### Read-only reads behind the facts

| Read | Result on 2026-10-02 |
|---|---|
| `git ls-remote origin` in the previous operator's working copy | `main` is c4926d8, `claude/agent-payments-simple` is 3e1d5d8 |
| `git rev-list --count origin/main..origin/claude/agent-payments-simple`, then `git log` over that range | 95 commits, all with an AI co-author trailer, 3 of them authored under an AI identity instead of the work identity |
| `git show origin/main:.gitignore` against the same file on the branch | `main` has no `session-8-policies/` lines. The branch lists `RUNBOOK.md`, `LUMA.md`, `SOCIAL.md` and `social/` |
| `curl -s -L https://luma.com/g0bmqt8p` | the page title reads "MOI Builders VIII - How to stop an AI Agent From Spending Your Money" |
| `curl -s -o /dev/null -w '%{http_code}'` on the blog pages `how-ai-agents-pay-each-other-moi` and `moi-access-policies-fine-grained-control` | 200, then 404 |
| `curl -s https://launchpad.moi.technology/api/stats`, twice | `stale` with `registered` 17, then `ok` with `registered` 0. Both: 33 active agents, 22 owners |
| JSON-RPC `net.Version`, `net.NetworkID` and `moi.AccessPolicies` (all-zero id) on `https://dev.voyage-rpc.moi.technology/devnet/` | "0.13.0"; error -32601 (method not found); a domain error ("missing access policy owner"), so the method exists |

## Pass after the review fixes, 2026-10-04
Run after the critic's findings were applied. `SKILLS` is the folder that holds the `moi-*` skills; `W` is a `mktemp -d` folder that is a git repository, with `PYTHONDONTWRITEBYTECODE=1`.
| Check | Command | Result |
|---|---|---|
| Description | `ruby -E UTF-8 -ryaml` on the block between the two `---` lines | Parses; a double-quoted string of 970 characters. It gained "its Points task" and "read-aloud script" |
| Scaffold from the new depth | `bash "$SKILLS/moi-webinar/scripts/new-session.sh" session-10 "MOI Builders #10: Test topic"` in `W`; again; `../x`; and with `SKILLS` unset | Exit 0 and the folder made with the deck, `SCRIPT.md` and `ledger.csv`; exit 1 "already exists"; exit 1 "must look like session-10"; exit 0 with the same 14 "created" lines |
| Preflight finds the deck checker | `bash "$SKILLS/moi-webinar/scripts/session-preflight.sh" --offline session-10`, with `SKILLS` set and with `env -u SKILLS`; then `session-99` and an empty `x.env` | Exit 0 both times, "deck check: RESULT: ok", 12 PASS, 4 WARN, 0 FAIL; exit 2 "not a folder here"; exit 2 "refusing x.env" |
| Pointers, lint, scan | the pointer check over `$SKILLS`; `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" --errors-only` over every `.md`, `.html`, `.txt`, `.rst`, `.csv` and `.yaml` file of the folder; `secret-scan.sh "$SKILLS/moi-webinar"` | 0 problems; 0 errors in 63 files; 0 findings in 75 files |
| Limits | `wc -l` | `SKILL.md` 132 lines of 150; `deck/GUIDE.md` 89 and `community-call/GUIDE.md` 106 of 150; longest reference 110 of 200 |
