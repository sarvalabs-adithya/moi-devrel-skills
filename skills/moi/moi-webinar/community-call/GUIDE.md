# MOI community call: The Campfire Chat

Branch of `moi-webinar`. `$SKILLS`, the operator, `ASK:`, the house rules and the gates are in `moi-webinar/SKILL.md` and `moi-devrel/SKILL.md`; this guide adds what is specific.

## What this covers
The monthly public call, from the line-up and the deck to the host's planted question, the day-of run and the recording description. CC14 (25 September 2026, inferred; ASK: Adithya for history, or Vardan for the sheet) is the worked example in `examples/cc14/`. The operator owns the deck and the line-up and approves every step that leaves the machine; facts are as of 2026-10-02.
Not covered: deck mechanics are the deck branch, `moi-webinar/deck`; a Builders session is `moi-webinar`; publishing and announcing posts is `moi-blog`; checking claims in general is `moi-devrel/claim-check`; house rules, people and keys are `moi-devrel`.

## Before you start
File names such as `references/x.md` are inside this branch's folder. Run every command from the working copy of `moi-foundation/MOI-Webinars` you are working in. Call folders (`community-call-<N>`) sit at its root. Whether they are committed, and on which branch, is the open policy in `moi-devrel/SKILL.md`, and nothing is pushed without a yes (Gates). People and channels are in `moi-devrel/references/people-and-teams.md`. Ask with message N of `templates/input-request-messages.md`.
- [ ] The call number and month. The planning sheet expects CC15 on Friday 2026-10-23, reserve 2026-10-30. Unconfirmed. Vardan owns the sheet: ASK: Vardan, then the call's manager (the record points to Rahul, inferred). Message 1.
- [ ] The line-up signed off by the call's manager (taken to be Rahul, inferred; ASK): the segments and who presents each. Message 2.
- [ ] The month's release note as the protocol team sent it. Owner: the protocol team (Gokul for chain facts). Message 3.
- [ ] The marketing inputs: the AI-visibility report and community numbers (Sai Kiran, via Slack). Event photos: ASK: Sai Kiran who holds them; the CC14 photos came from the previous operator. Messages 4 and 5.
- [ ] The host's name and any planted question. Owner: ASK: Vardan or Sai Kiran who hosts, then the host. Message 6.
- [ ] A call folder `community-call-<N>/` in the working copy (step 3 creates it). Do not push it without a yes: the repo is public.
- [ ] Read `references/segments-and-roles.md` for what is unknown. Ask the questions it lists before relying on a guess.

## The run
Budget: about two hours of deck work once inputs are in hand (the manager's cap on 2026-08-24). CC14 took about 45 hours of wall clock, most of it waiting for inputs and changing decisions.

| # | Step | What to do, and where | Done when |
|---|---|---|---|
| 1 | Confirm date and segments | Draft messages 1 and 2 (GATE to send: the operator sends). Settle date, start time, length, platform, host, segment order and rehearsal day | The manager has said yes to the order. Every open item is an ASK line |
| 2 | Collect inputs per segment | `references/inputs-checklist.md`, messages 3 to 8 (GATE to send: the operator sends). Save photos under `community-call-<N>/deck/assets/` | Each segment has its artefact or is dropped |
| 3 | Numbers ledger | `mkdir -p community-call-<N>` then `cp "$SKILLS/moi-webinar/community-call/templates/numbers-ledger.csv" community-call-<N>/numbers-ledger.csv`. One row per figure: slide, figure, value, source, as_of, confirmed_by, status. Write why in `confirmed_by` for an unverified row | Every figure has a row. Unverified rows are shown to the human |
| 4 | Slide plan | `references/slide-plan.md`: order, what earns a slide, what stays off a public call | The human approved the plan |
| 5 | Build with the deck branch | `bash "$SKILLS/moi-webinar/deck/scripts/new-deck.sh" community-call-<N> "MOI Community Call #<N>: The Campfire Chat"`. Title chip: "The Campfire Chat · <Month> <Year>". Then add every slide of the plan (`moi-webinar/deck/GUIDE.md`, steps 3 and 4), or step 6 stops with "the deck has only 1 slide" | `python3 "$SKILLS/moi-webinar/deck/scripts/check-deck.py" community-call-<N>/deck/index.html` has no FAIL |
| 6 | Script the operator's slides | Overwrite the `SCRIPT.md` that step 5 made: `cp "$SKILLS/moi-webinar/community-call/templates/SCRIPT.md" community-call-<N>/SCRIPT.md`. Write it by `references/call-script.md` and `moi-webinar/deck/references/spoken-script.md`; host question by `references/host-qa-prep.md`. Copy it into the deck with `python3 "$SKILLS/moi-webinar/deck/scripts/sync-notes.py" community-call-<N>/deck/index.html community-call-<N>/SCRIPT.md --confirm` (a dry run without `--confirm`) | `python3 "$SKILLS/moi-webinar/deck/scripts/check-deck.py" community-call-<N>/deck/index.html --script community-call-<N>/SCRIPT.md` passes check h |
| 7 | Release-slide checks | `references/release-slide-checks.md` against the note and source | Every release line has a verdict. "Live" was read from the node |
| 8 | Prune checks | After every cut or move: `references/pruning-checklist.md`. Then `python3 "$SKILLS/moi-webinar/community-call/scripts/ledger-check.py" community-call-<N>/deck/index.html community-call-<N>/numbers-ledger.csv --notes` | Checklist done. Page count equals slide count. Ledger exits 0: every row `confirmed`, or kept by the human as `accepted-unverified` with who and when in `confirmed_by` (shown as a WARN) |
| 9 | Rehearsal | Read aloud with the presenter window open, once, timed. The human reads the final text once | Timing known. Changes made in `SCRIPT.md`, then copied with the `sync-notes.py` command of step 6, which writes only with `--confirm` |
| 10 | Day-of | `references/day-of-runbook.md`: the sweep, `P`, share the deck window, the PDF fallback | PDF exported with `bash "$SKILLS/moi-webinar/deck/scripts/render.sh" community-call-<N>/deck/index.html MOI_Community_Call_<N>.pdf`, and a second copy of the folder exists. GATE: a copy in cloud storage |
| 11 | After the call | `references/after-the-call.md` (GATE: uploading the recording or its description, and any post). `python3 "$SKILLS/moi-webinar/community-call/scripts/youtube-description.py" community-call-<N>/deck/index.html > community-call-<N>/description.txt` | The human has the draft, the Q&A log and the open questions. `grep -n '\[' community-call-<N>/description.txt` prints nothing before the description is posted |
| 12 | Hand-back | The format at the end of this file | The human has read it |

`sync-notes.py` is a script of the deck branch (`moi-webinar/deck/scripts/`) and is a dry run: without `--confirm` it prints what it would change and writes nothing.

## Which file to read
| Doing | Read |
|---|---|
| Who presents, the date, what is unknown | `references/segments-and-roles.md` |
| Asking each owner for their part, ledger columns and statuses | `references/inputs-checklist.md`, `templates/input-request-messages.md` |
| Deciding what goes on slides and what stays off | `references/slide-plan.md` |
| Writing the words to be read aloud | `references/call-script.md`, then `moi-webinar/deck/references/spoken-script.md` |
| Checking protocol and release slides | `references/release-slide-checks.md` |
| Preparing for the host's planted question | `references/host-qa-prep.md` |
| After removing or moving a slide | `references/pruning-checklist.md`, then `moi-webinar/deck/references/build.md` |
| The day of the call | `references/day-of-runbook.md` |
| The recording and what follows | `references/after-the-call.md`, `templates/youtube-description.md` |
| Put the call on the website calendar | `moi-web-products-ops/references/website-calendar.md` (GATE: an admin write to a public page) |
| A finished call to learn from | `examples/cc14/README.md` |
| Testing a change to this branch | `evals/evals.md` |

## Facts that fail silently
| Rule | The incident |
|---|---|
| A deck can print a perfect PDF and be dead live. Run the deck check of step 5 and step 6 before every export | A real line break in a `NOTES` string killed the inline script on CC14 while the PDF printed. A stray `</div>` on slide 10 pushed slides 11 and 12 out of the scaled stage |
| Name a slide by its title before deleting it | The badges were one behind, so "remove slide 6" deleted the wrong slide |
| Keep a numbers ledger and write each figure in it before it goes on a slide | Three sources gave three sets of figures. The README still said "figures unchanged" |
| Ask for any figure you cannot refresh, by name | 47 queries, five engines and 221 of 226 were never reconfirmed and went on a public slide |
| After any cut, search for what it leaves behind | Four cuts left sentences about a campaign, a competitor and trend arrows that no longer existed |
| Write the release time as a date and "00:00 UTC". "Today" and "12:00 AM" are ambiguous. The note itself says "today at 12:00 AM UTC" | "12:00 AM UTC" was read as midday and two scheduled posts were wrong | <!-- slop-lint:ignore -->
| Read the node before saying "live on devnet". The network is called devnet | Devnet lagged the source in September 2026 |
| Never present a release candidate as shipped. Keep the `-rc` suffix | At CC13 an RC was written up as shipped |
| Say what a change covers. Fee delegation pays fuel and nothing else | Universals such as "every action costs fuel" were removed from the release post | <!-- slop-lint:ignore -->
| Edit `SCRIPT.md`, then run `sync-notes.py` with `--confirm` to copy it into `NOTES` | The presenter window kept showing an old script after a "regenerate". Without `--confirm` the tool writes nothing |
| Replace "last Friday" and "since the last call" with a date or cut them | They went stale on slide 9 |
| Promise a guest or topic for the next call only when it is confirmed | The CC13 draft description named guests that the CC14 deck did not have. Whether it was posted is unknown |
| Show a photo of identifiable people only with permission to show it | The CC14 example's two event photos had no permission on record and were removed from this library |
| Copy the deck folder somewhere safe | The CC14 folder is untracked and on the previous operator's machine only (as of 2026-10-02; ASK: Adithya for a copy) |
| Ask the human to `cp` a file out of `~/Downloads` | On the previous operator's Mac, tools could not read it (27 August 2026; may no longer apply) |

## Gates
Nothing below happens without the human's explicit yes in this conversation:
- Sending any message, including the input requests. Claude drafts, the human sends.
- Pushing, opening a pull request or merging the call folder. `moi-foundation/MOI-Webinars` is public as of 2026-10-01: say that a push publishes `SCRIPT.md`, the ledger and the host prep, and ask whether to keep the host prep out of the pushed copy.
- Posting, scheduling or announcing anything, and uploading the recording or its description. Running `"$SKILLS/moi-webinar/scripts/buffer.mjs"` in any form, a dry run included (it sends the key to Buffer), is a GATE.
- Uploading, moving or sharing any file in Drive or other cloud storage, including the PDF and the second copy of the call folder.
- Adding the call to the website calendar (`moi-web-products-ops/references/website-calendar.md`; an admin write to a public page), and setting or changing a repository secret or variable.
- Downloading a file. Say the filename, source and size when asking.
- Spending devnet funds or deploying on devnet, for example in a live demo: a wallet step, so the operator signs and runs it.
- Telling the host or a guest that something is confirmed.
- Setting a ledger row to `accepted-unverified`. Only the human decides, and the row names who and when.
- Switching the git or gh identity, or adding an AI co-author line or "generated with" footer. See `moi-devrel/references/consent-and-identity.md`.
- Sub-agents, bulk model runs and paid APIs: only when the operator names them, with the count and model stated first.
- Deleting a recording or a notes document. That is the operator's own action, after asking the file's owner. Claude does not delete it.

## Keys and access
Names only. Building and checking the deck needs no key. For where each lives, see `moi-devrel/references/keys-and-access.md`.
- The website's community calendar takes admin writes. The holder of that access is not on record: `moi-devrel/references/keys-and-access.md`. ASK: a repo admin of `sarvalabs/MOI-Website`.
- Website: A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin.
- `BUFFER_API_KEY`: scheduled posts through `scripts/buffer.mjs` in the `moi-webinar` skill. It stays in a gitignored `.env` at `$SKILLS/moi-webinar/.env` and is never pasted into chat.
- Slack and Drive access for the inputs and the planning sheet. ASK: Rahul.
- The Scribble report login. Holder unknown. ASK: Sai Kiran.
- The meeting account and the YouTube channel login. Owners unknown. ASK: Rahul.
- Recovery phrases: Claude never handles one, including a throwaway one. If one is pasted, do not repeat it, tell the operator it is exposed, and continue with the MOI Wallet extension and the operator's own funded account.

## Hand-back
Give the human:
1. What was produced and where: the deck, `SCRIPT.md`, the ledger, the PDF, the description draft.
2. What was left out and why: each cut slide, each figure not used.
3. Every ledger row still `unverified` or `pending`, with who can settle it, and every `accepted-unverified` row with who accepted it and when.
4. Every ASK line still open.
5. What remains, and the next action for the human.
6. "Ready: yes or no, because". No while a deck-checker FAIL stands, or a ledger row is `unverified` or `pending` and the human has not decided to keep it, or a release line has no verdict. Yes only with every `accepted-unverified` row named in item 3.
