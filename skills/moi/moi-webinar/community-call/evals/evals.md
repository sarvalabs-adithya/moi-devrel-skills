# Evals for moi-webinar/community-call

Seven prompts with the behaviour expected, then the record of every script test. Run the prompts against a fresh Claude with only this library, and read the response against "Expect". Facts are as of 2026-10-02, updated on 2026-10-13 from the handover note `project-handover-docs/COMMUNITY-CALL.md`.

## Prompts

### 1. Taking over the call
Prompt: You own the deck and the line-up for Community Call 15. Where do I start?
Expect: Starts with the "Before you start" setup: sets `SKILLS`, works from a working copy of `moi-foundation/MOI-Webinars`, and says "the operator" is the human and Adithya is the previous operator. Opens the run table at step 0 and, with no agenda given, asks for it (ASK: Vardan). Says CC15 is expected in the last week of October 2026 and that the date is not set yet (ask Vardan); it does not offer a specific date as fact. If the operator gives a date, it computes the T-minus dates from that date with the command in `references/agenda-intake.md`. Asks for the start time, length and platform, and names Vardan for them, Ruta as the host (handover note; confirm each call) and Rahul as the call's manager, saying that is inferred. Adds that Luma, Riverside and YouTube logins are held by Vardan and the new operator needs access before the first call, and that read access to go-moi and go-pisa is a question for Gokul. Lists the inputs by segment from `references/inputs-checklist.md` with owners. Offers the draft messages in `templates/input-request-messages.md` and does not send them. Says the deck takes about two hours once inputs are in hand. Does not invent a time, a platform, a host, a speaker or a Slack channel. Points to `project-handover-docs/COMMUNITY-CALL.md` and the 4 October dependency list (now only in git history) instead of a `DEPENDENCIES.md` file, and says the old decks are in `moi-foundation/MOI-Webinars` under `community-call-N/deck/` (PR #2, 13 October 2026). It does not tell the newcomer to ask the previous operator for a copy. Does not start building slides before the inputs and the sign-off exist. Ends with ASK lines for what the record does not settle.
Why: The role was handed over with almost nothing recorded about the day, platform or host. CC14 took about 45 hours of wall clock, mostly waiting for inputs. The manager's identity is an inference.

### 2. Script and the planted question
Prompt: Write the script for the protocol slides. The host says they will ask whether someone with zero KMOI can use an app that pays their fuel.
Expect: Overwrites the `SCRIPT.md` made by `new-deck.sh` with `templates/SCRIPT.md`, then writes a `PRESS NEXT --> SLIDE N` banner for every slide the operator presents and for the close, and the same text in `NOTES`. Copies it in with `sync-notes.py ... --confirm` and says the tool is a dry run without the flag. Writes complete spoken sentences, no em dashes and no "not this, not that". Puts a bracketed `[If the host asks ...]` cue on the slide, with a fifteen-second answer of about 35 words and the second beat. Gives the trap (fuel only, nothing else) and an honest fallback in the preparation, not in the cue. Notes that "your first action still goes through" assumes nothing else stands in the way and offers to ask Gokul. Runs `python3 "$SKILLS/moi-webinar/deck/scripts/check-deck.py" community-call-<N>/deck/index.html --script community-call-<N>/SCRIPT.md` and reports check h. Writes the release time as 00:00 UTC on the date, and says the note itself reads "today at 12:00 AM UTC". Does not read out figures whose ledger row is not confirmed. Says SCRIPT.md holds the trap and the fallback, so a push to the public repo would publish them. <!-- slop-lint:ignore -->
Why: CC14 (25 September 2026, inferred). The first script was rejected for its tone, the planted question needed a short answer that works as a clip, and the notes and script file must match. The presenter window kept an old script when the sync did not write.

### 3. Removing and moving slides
Prompt: Remove slide 6 and move DevRel up to slide 3.
Expect: Repeats the title of slide 6 back and asks which slide is meant before deleting. Runs the deck checker first to confirm the badges equal the page numbers. Does the checklist in `moi-webinar/deck/references/build.md`, then `references/pruning-checklist.md`: a grep of the removed slide's names, figures and short forms across the deck, `SCRIPT.md`, the ledger and the README; dangling references between segments; the host cue; teasers; ledger rows retired and `ledger-check.py` run; `SCRIPT.md` renumbered and synced with `sync-notes.py ... --confirm` (a dry run without the flag); README updated; re-render under the chosen PDF name and the changed notes read back in a fresh tab. Asks the human about each leftover reference instead of deciding. Reports what was removed. Does not restate the deck mechanics from memory.
Why: On CC14 the badges were one behind the pages, so the wrong slide was deleted. Four cuts left residue on slides 1, 6, 8 and 11, and two pairs of neighbours share a background.

### 4. A "live" claim on a release slide
Prompt: Slide 2 says "live on devnet on 11 September". Is that right?
Expect: Does not answer from the release note alone. Says the version is verified against the note and the post, that the note reads "scheduled for today at 12:00 AM UTC" with no date, and that 00:00 UTC on 11 September comes from the correction reply in the release pack (never pushed to the public repo, so not available in this library) and from `moi-devrel/references/devnet.md`. Says `devnet.md` supports "live" as of 2026-10-02 and that no read from the call day is on record. May add that on 14 October 2026 `net.Version` answered 0.13.0 and `net.NetworkID` returned method-not-found (-32601), so the live-build check is still open. Proposes reading the live node for its version and the field name on a recent interaction (`payer` means the old build, `fee_payer` the new one), points to `moi-devrel/references/devnet.md` for the endpoint, and names Gokul as the person to ask. Says the 2026-09-25 instruction fixed the wording ("devnet", never "Voyage devnet") and did not verify the claim. Writes the time as 00:00 UTC on 11 September. Does not call a release candidate shipped. Marks anything it can only find in the post as UNVERIFIABLE until Gokul gives read access to the private source. <!-- slop-lint:ignore -->
Why: Devnet lagged the source in September 2026. The release time "12:00 AM UTC" was misread. At CC13 a release candidate was written up as shipped. An earlier draft of this skill said the note holds the 00:00 UTC date. It does not. <!-- slop-lint:ignore -->

### 5. This month's visibility numbers
Prompt: Sai Kiran sent this month's AI-visibility report. Update slides 5 and 6.
Expect: Adds a ledger row for every figure with its source and date, and retires the figures it replaces as `superseded`. Compares only like with like: same query set, with each month's figure dated. Says plainly that last month's 47 queries, five engines and 221 of 226 coverage were never reconfirmed and asks Sai Kiran for the current ones. Notes that 12.8 appeared twice with different meanings. Removes the movement sentence if no source supports the change. Runs `python3 "$SKILLS/moi-webinar/community-call/scripts/ledger-check.py" community-call-<N>/deck/index.html community-call-<N>/numbers-ledger.csv --notes` and shows the unverified rows. Does not guess a missing figure and does not name a fifth engine without a source. At hand-back says "Ready: no" while a row is `unverified` and the human has not decided. If the human decides to keep a figure, sets it to `accepted-unverified` with "accepted by <name> on <date>" in `confirmed_by`, shows the check exit 0 with a WARN, and says "Ready: yes" only with those rows named. Never accepts a figure on its own.
Why: At CC14 three sources disagreed and the README said "figures unchanged" when they had changed. The baseline was promised for monthly comparison. Step 8 and the hand-back once disagreed on what "ready" means.

### 6. After the call
Prompt: The call is done. Write the YouTube description, put the deck in Drive, push the call folder and add the call to the website calendar.
Expect: Says the description evidence covers one call only (CC13), and that every recording is on the MOI YouTube playlist, owned by Vardan. Runs `python3 "$SKILLS/moi-webinar/community-call/scripts/youtube-description.py" community-call-<N>/deck/index.html` and fills only what it can support. Leaves every `[__:__]` for a person who has watched the recording, with the first chapter at 00:00. Keeps "Next up" out unless the line-up is confirmed. Counts characters against 5,000 and opens every link. Shows the final text to the human. Does not upload, post, push or message anyone. Asks before uploading to Drive. Says the repo is public and a push publishes `SCRIPT.md`, the ledger and the host prep, and asks whether to keep the host prep out. For the website, says the old calendar was replaced by a Luma block (MOI-Website PR #60, 13 October 2026), hidden until `lumaUrl` is set in `content/community-calls.json`, that setting it is a pull request to a public site (a gate), and points to `moi-web-products-ops/references/website-calendar.md`. It gives for the website's admin only the sentence in `GUIDE.md` ("Website: A security finding is open on this product as of 2026-10-02. Not recorded (the previous DevRel's notes); ASK: Rahul before touching its admin."). It gives no detail of the finding and no route names. Lists the Q&A follow-ups with owners and the 48-hour target.
Why: The CC13 draft description named guests the next call dropped. A link to an unmerged post was dead. Nothing leaves the machine without a yes. Drive is shared and the repo is public.

### 7. The agenda first
Prompt: Community Call 15 is on Friday 23 October 2026. Agenda: protocol update and DevRel (me), AI visibility and community (Sai Kiran), then a guest, Priya from Acme Labs. What do we need?
Expect: Replies with the run sheet of `references/agenda-intake.md` in the shape of `templates/run-sheet.md`, and nothing else. Restates the agenda in one line. Gets the dates from the command in `agenda-intake.md`: T-9 Wed 2026-10-14 (input requests, Luma page, first post), T-7 Fri 2026-10-16 (updates in, ledger, slide plan), T-4 Mon 2026-10-19 (second post, both Luma lists), T-3 Tue 2026-10-20 (guest final, deck finished, links into Luma and Riverside, YouTube description), T-2 Wed 2026-10-21 (Riverside invites, third post), T-1 Thu 2026-10-22 (Luma announcement 24 hours before, host question), T-0 Fri 2026-10-23 (last post and Luma announcement 1 hour before, day-of check), then after the call. Each row names its owner (Vardan for Luma, Riverside and posts; Ruta as host, per the handover note, confirm each call; DevRel for the deck), what Claude can produce and the exact file or script. Writes "ASK: start time" for the clock times. Notes that the catalogue has no product or partnerships item, so none is listed. Asks for Priya's role, company as written, topic, headshot and logo through message 7, and does not look her up. Says the Vardan rows are drafts for him and nothing is sent, posted, scheduled or changed in Luma or Riverside without a yes. Ends with "Which of these should I start?". Does not draft a message, a post, Luma text or a slide, does not create the call folder, and does not run any script but the date command.
Why: On 2026-10-13 the previous operator asked for the call to start from the agenda: a checklist first, then one item at a time. The timeline is his handover note's. CC14 took about 45 hours of wall clock, mostly waiting on inputs that were asked for late.

## Script tests

All run on 2026-10-02 with Python 3 and the standard library, from a scratch folder (not from a skill folder), so the commands do not depend on the working directory. They were run again on 2026-10-04 from `moi-webinar/community-call/scripts/`: every result below held, except that the character count in test 1 of `youtube-description.py` is 1,199 (it read 1,159 here; the script's output is the same before and after the move, so the old figure was stale). Set up as follows:

```
SKILLS=<the folder that holds the moi-* skills>
EX="$SKILLS/moi-webinar/community-call/examples/cc14"
T=$(mktemp -d)
lc() { python3 "$SKILLS/moi-webinar/community-call/scripts/ledger-check.py" "$@"; }
yt() { python3 "$SKILLS/moi-webinar/community-call/scripts/youtube-description.py" "$@"; }
```

The scratch inputs in `$T` were built with a few lines of Python from `$EX/deck/index.html` and `$EX/numbers-ledger.csv`, as each row describes. The long hex id in test 18 was built at run time as `0x` plus `ab12` repeated ten times.

### scripts/ledger-check.py
Exit 0 means no FAIL list has an entry (list 5, the WARN list, may), 1 means a FAIL list has an entry, 2 means bad input.

| # | Input | Command | Result |
|---|---|---|---|
| 1 | The example as filled | `lc "$EX/deck/index.html" "$EX/numbers-ledger.csv"` | Exit 1. 12 slides, 42 rows (9 retired). List 1 empty. List 2 has 16 `unverified` rows: the devnet date, the old id, the asset limits, 47 queries, five engines, both movements, 221, 226, 97.8%, 120+, 60+, the three Game Night figures and "last Friday". Lists 3, 4 and 5 empty |
| 2 | Same, with `--notes` | add `--notes` | Same result, "notes checked: yes". The notes hold no figure the ledger lacks |
| 3 | Good: every live row set to `confirmed` | `lc "$EX/deck/index.html" "$T/ledger-all-confirmed.csv" --notes` | Exit 0. "PASS, every figure is in the ledger and confirmed" |
| 4 | Good: the 16 unverified rows set to `accepted-unverified`, `confirmed_by` "accepted by Test Person on 2026-10-01: ..." | `lc "$EX/deck/index.html" "$T/ledger-accepted.csv" --notes` | Exit 0. List 5 has 16 rows. "PASS WITH WARNINGS ... 16 accepted without verification and must be named in the hand-back" |
| 5 | Bad: same rows `accepted-unverified` but `confirmed_by` still "nobody: ..." | `lc "$EX/deck/index.html" "$T/ledger-accepted-nowho.csv" --notes` | Exit 1. List 4 has 16 rows: no "accepted by <name>" and date. List 5 empty |
| 6 | Bad: 3 rows accepted, 13 left `unverified` | `lc "$EX/deck/index.html" "$T/ledger-mixed.csv" --notes` | Exit 1. List 2 has 13 rows, list 5 has 3 |
| 7 | Bad: the 17.3% row deleted | `lc "$EX/deck/index.html" "$T/ledger-missing-visibility.csv" --notes` | Exit 1. List 1: `slide 5: 17.3%` and `slide 5: 17.3 (in notes)` |
| 8 | Bad: deck edited so slide 5 shows 712 instead of 650 | `lc "$T/deck-new-figure.html" "$T/ledger-all-confirmed.csv"` | Exit 1. List 1: `slide 5: 712 ...Mentions 712 Times MOI was named...` |
| 9 | Bad: slide 5 shows 13.5%, a `superseded` figure | `lc "$T/deck-retired-figure.html" "$T/ledger-all-confirmed.csv"` | Exit 1. List 3: `slide 5: 13.5%` |
| 10 | Bad: the 1,203 row has no source | `lc "$EX/deck/index.html" "$T/ledger-no-source.csv"` | Exit 1. List 4: `slide 5 \| Citations = 1,203 \| status=confirmed` |
| 11 | Bad: ledger with only three columns | `lc "$EX/deck/index.html" "$T/ledger-bad-header.csv"` | Exit 2. "ledger is missing column(s): source, as_of, confirmed_by, status" |
| 12 | Bad: deck file does not exist | `lc nope.html "$EX/numbers-ledger.csv"` | Exit 2. "cannot read deck" |
| 13 | Bad: an unquoted comma gives a row one cell too many (`...,dashboard, screenshot,...`) | `lc "$EX/deck/index.html" "$T/ledger-extra-cells.csv"` | Exit 2. "ledger line 17 has more cells than the header; quote any cell that contains a comma". Before the fix: an AttributeError traceback and exit 1 |
| 14 | Good: the ledger saved with a UTF-8 byte order mark | `lc "$EX/deck/index.html" "$T/ledger-bom.csv"` | Runs, same lists as test 1 (exit 1 for the 16 unverified rows). Before the fix: exit 2 "missing column(s): slide" |
| 15 | Bad: `NOTES` written with single quotes, and a new figure 99.9 in the slide 1 note | `lc "$T/deck-single-quote-notes.html" "$T/ledger-all-confirmed.csv" --notes` | Exit 1. List 1: `slide 1: 99.9 (in notes)`. Before the fix: "PASS", exit 0 |
| 16 | Bad: `var NOTES = [];` | `lc "$T/deck-empty-notes.html" "$T/ledger-all-confirmed.csv" --notes` | Exit 2. "the NOTES array has no entries this script can read; the notes were NOT checked". No PASS line |
| 17 | Bad: `NOTES` has 11 entries for 12 slides | `lc "$T/deck-notes-mismatch.html" "$T/ledger-all-confirmed.csv" --notes` | Exit 2. "NOTES has 11 entries for 12 slides" |
| 18 | A long hex id on slide 5 | `lc "$T/deck-hex.html" "$T/ledger-all-confirmed.csv"` | Exit 1. List 1 prints `0xab12...(masked)`, never the full id |
| 19 | The blank template against the example deck | `lc "$EX/deck/index.html" "$SKILLS/moi-webinar/community-call/templates/numbers-ledger.csv"` | Exit 1. 35 figures with no row, 2 rows `pending` |
| 20 | A different deck: the six-slide example in `moi-webinar/deck` | `lc "$SKILLS/moi-webinar/deck/examples/mini-deck/index.html" "$SKILLS/moi-webinar/community-call/templates/numbers-ledger.csv"` | Runs to the end. Lists the three placeholder stats (10, 20, 30) as missing |
| 21 | Env-named input (2026-10-04) | `lc .env "$EX/numbers-ledger.csv"`, `lc "$EX/deck/index.html" marker.env` | Exit 2 each: "ledger-check: refusing to read ...: an env file can hold keys and is never opened." Neither file is opened |

Excerpt, test 7:

```
1. FIGURES ON SLIDES WITH NO LEDGER ROW (2)
  slide 5: 17.3%    ...e. Visibility 17.3% How often MOI shows up in t...
  slide 5: 17.3 (in notes)    ...each month. The baseline: 17.3 percent visibility, 1,203 c...
RESULT: FAIL, resolve every FAIL list above before the call (exit 1)
```

### scripts/youtube-description.py
Exit 0 means a draft was printed. Warnings go to stderr. Exit 2 means bad input.

| # | Input | Command | Result |
|---|---|---|---|
| 1 | Good: the example deck | `yt "$EX/deck/index.html"` | Exit 0. Title "MOI Community Call #14: The Campfire Chat". Chapters `00:00 Welcome` then 11 lines of `[__:__] <title>`. stderr: 1199 of 5000 characters, 27 placeholders open |
| 2 | Good: a deck titled #15 | `yt "$T/deck-15.html"` | Exit 0. Title "#15". The teaser reads "Next up: Community Call #16" |
| 3 | Over the limit: template padded past 5,000 characters | `yt "$EX/deck/index.html" --template "$T/template-long.md"` | Exit 0. stderr: "WARNING: the draft is 6736 characters, over the 5000 limit" |
| 4 | Bad: deck with no `TITLES` array | `yt "$T/deck-no-titles.html"` | Exit 2. "no TITLES array found in the deck's script" |
| 5 | Bad: deck file does not exist | `yt nope.html` | Exit 2. "cannot read deck" |
| 6 | Bad: template without the BEGIN and END markers | `yt "$EX/deck/index.html" --template "$T/template-nomarkers.md"` | Exit 2. "template lacks the ... markers" |
| 7 | A different deck: the six-slide example in `moi-webinar/deck` | `yt "$SKILLS/moi-webinar/deck/examples/mini-deck/index.html"` | Exit 0. Title "MOI mini deck", five blank chapters |
| 8 | Bad: no `<title>` in the head, and a presenter-window string `'<title>Presenter: ' + document.title ...` in the inline script | `yt "$T/deck-no-head-title.html"` | Exit 0. Title `[CALL TITLE]`, next number `[N+1]`, and a stderr note saying so. Before the fix the title was `Presenter: ' + document.title.replace(/</g, '&lt;') + '` |
| 9 | Good: a head `<title>` and the same script string | `yt "$T/deck-title-and-script-string.html"` | Exit 0. Title "MOI Community Call #14: The Campfire Chat", read from the head only |
| 10 | Env-named input (2026-10-04) | `yt .env`, `yt marker.env`, and `yt "$EX/deck/index.html" --template marker.env` | Exit 2 each: "youtube-description: refusing to read ...: an env file can hold keys and is never opened." |

### The deck fix and the example deck
Commands and results are in `examples/cc14/README.md`, run on 2026-10-02: a real-Chrome DOM dump of the original deck (slides 11 and 12 under `div.deck-viewport`, 9 of 10 badges in a section), the same dump of the fixed deck (all 12 under `div#stage.deck-stage`, 10 of 10), `node --check` passing on the fixed script and failing on a copy with a line break in a `NOTES` string. After the two photos were deleted, `check-deck.py` with `--script` gave: a, b, c, e, f, g, h, k, l, m and n PASS, d FAIL, i and j WARN (the two photo files are absent, which is intended). `render.sh --force` wrote 12 slides and 12 pages, a match, and the page image of slide 10 shows two empty frames that read their filenames.
