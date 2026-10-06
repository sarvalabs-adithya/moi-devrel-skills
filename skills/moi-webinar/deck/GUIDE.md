# MOI decks

Branch of `moi-webinar`. `$SKILLS`, the operator, `ASK:`, the house rules and the gates are in `moi-webinar/SKILL.md` and `moi-devrel/SKILL.md`; this guide adds what is specific.

## What this covers

One HTML file is the whole deck: slides, CSS, the speaker script and the presenter window. Headless Chrome prints the PDF, and there is no build step and no framework. A checker (`check-deck.py`) finds the faults a PDF hides, because a deck can print a perfect PDF while its arrow keys, presenter window and scaling are broken. This branch builds the deck for a Builders session, for the monthly call or for anything else, and holds the single set of rules for text read aloud.

Not covered: what a community call contains (`moi-webinar/community-call`); planning a Builders session (`moi-webinar`); checking claims against source (`moi-devrel/claim-check`); commits, pull requests and pushes (`moi-devrel/ship`). The material for a deck comes from those.

## Before you start

File names such as `references/build.md` are inside this branch's folder. Every command is written in full with `$SKILLS` and is run from the working copy of the repo you are working in. `<s>` below is a session folder, `session-<N>` or `community-call-<N>`, at the root of the working copy. Whether session folders get committed, and on which branch, is the open policy in `moi-devrel/SKILL.md`.

- [ ] Raw material: report, Slack dump, release note, screenshots. From the content owner; ask the operator who that is. For a community call the segment owners are in `moi-webinar/community-call/references/segments-and-roles.md`.
- [ ] Deck title, series label and month for the cover chip. From the operator: ask for all three in one message.
- [ ] Every figure with its source, its date and who confirmed it. From whoever owns the number; ask the operator to put the question to them. Anything unconfirmed is flagged, not hidden.
- [ ] Photos and logos as real files, or the plain fact that none exist yet. From the operator or the speaker, copied into the working copy. A download is a gate (below).
- [ ] Which slides the presenter speaks. From the operator. Scripts are written only for those.
- [ ] Tools: python3 and Chrome are required; node and poppler (`pdfinfo`) make the checks complete. Test with `python3 --version`, `node --version`, `pdfinfo -v`, and ask the operator before installing anything.

## The run

| # | Step | Do this | Done when |
| --- | --- | --- | --- |
| 1 | Scaffold | `bash "$SKILLS/moi-webinar/deck/scripts/new-deck.sh" <s> "Deck title"` makes `<s>/deck/index.html`, `deck/assets/`, `deck/README.md` and `<s>/SCRIPT.md`. It refuses an empty title and a deck that exists (then edit that one, `references/build.md`) | it prints `created` lines |
| 2 | Slide plan | List each slide: title, one component, the source of each figure. One idea per slide. Show it to the operator in chat as a short table | every figure has a named source and every slide one idea |
| 3 | Write slides | One `<section class="slide ...">` each, from `references/components.md`. Alternate backgrounds. Badge equals page number. The last slide is the close and carries no badge, so end every deck with one: check c fails a badge on the last slide, and the fix is a close slide after it. For every slide you add, add one string to `TITLES` and one to `NOTES` (`""` for a slide with no script) in the inline script at the bottom of `index.html`, in slide order. Replace the three TODO strings from the scaffold | checks b, c, d, e and m pass | <!-- slop-lint:ignore -->
| 4 | Notes and script | Write `SCRIPT.md` by `references/spoken-script.md`. Run `python3 "$SKILLS/moi-webinar/deck/scripts/sync-notes.py" <s>/deck/index.html <s>/SCRIPT.md` (a dry run: read the slide list), then the same with `--confirm`. It adds `""` for any slide still missing a `NOTES` entry; `TITLES` stays by hand | checks e and h pass |
| 5 | Check | `python3 "$SKILLS/moi-webinar/deck/scripts/check-deck.py" <s>/deck/index.html --script <s>/SCRIPT.md --layout` | no FAIL; each WARN fixed or listed for the hand-back |
| 6 | Render | `bash "$SKILLS/moi-webinar/deck/scripts/render.sh" <s>/deck/index.html [Name.pdf]`. A bare name is written beside the deck. Pass the name when a PDF already has one | it prints `wrote <path> (new): N slides, N pages, match`, or `(replaced)` for `(new)` |
| 7 | Look | Read the PDF pages back as images and view every slide you touched and its neighbours (`references/build.md`, "Look at the pages") | nothing cut off, empty or out of order |
| 8 | Hand back | Use the hand-back section below | the operator has the list of what was left out and why |

After any step that deletes, inserts or moves a slide, do the checklist in `references/build.md` and repeat steps 5 to 7. Batch edits and render once. If step 6 says REJECTED, the page count was wrong: the old PDF is untouched and the bad render sits beside it as `<name>.pdf.rejected`.

## Which file to read

| Doing | Read |
| --- | --- |
| The rules every deck follows (sources, photos, badges, one idea per slide) | `references/rules.md` |
| Writing slides: every component, the spacing budget | `references/components.md` |
| Checking, rendering, editing an existing deck, variants, photos, logos, presenting live | `references/build.md` |
| Writing the script, cues, keeping `NOTES` and `SCRIPT.md` identical | `references/spoken-script.md` |
| Something looks wrong, or before editing a deck built earlier | `references/traps.md` |
| A small synthetic deck that passes every check | `examples/mini-deck/` |
| A real finished call deck, and what was good about it | `moi-webinar/community-call/examples/cc14` (its slide 10 and presenter-title defects are fixed there; two content faults are left in on purpose) |
| Starting a deck by hand | `templates/template.html`, `templates/SCRIPT.md` |
| Testing a change to this branch | `evals/evals.md` |

## Facts that fail silently

Each is a real incident or a measured fault; the full table is in `references/traps.md`.

- A deck whose inline script has a syntax error still prints a correct PDF. Only the arrow keys, dots and presenter window die (community call 14, 24 Sep 2026). Check a catches it. If node is missing the checker says SKIPPED: that is not a pass.
- A stray `</div>` puts later slides outside the scaled stage (community call 14, slide 10). The page count and `node --check` stay green. Check b catches it.
- Badges one behind the pages once got the wrong slide deleted. Say the slide's title back before deleting.
- On 4 Sep 2026 the presenter window kept showing an old script across at least six messages; the cause was not found. Keep `NOTES` and `SCRIPT.md` identical with `sync-notes.py`, and after every regenerate open the deck in a fresh tab and read one slide's notes.
- Content past the slide edge, or a clipped code line, is invisible until someone looks (session 8, slide 10). Use `--layout` and look.
- A feature in source is not live on devnet (the fee payer, as of 2026-09-10). Say "went live on devnet" only when told; never "Voyage devnet". <!-- slop-lint:ignore -->
- Sentences carried over from an earlier draft with no source (community call 14). Ask of each: which source says this?
- Figures from different sources disagree (community call 14). Use the newest named source and say which figures are old.

## Gates

Nothing below happens without a clear yes from the operator in this conversation. Building and rendering locally needs no yes.

- Committing, pushing, opening a pull request, merging, posting, scheduling or sending the deck, uploading or sharing the PDF in cloud storage. A push to `moi-foundation/MOI-Webinars` publishes: that repo is public (as of 2026-10-02). When a commit is approved: work identity only, no AI co-author line, no "generated with" footer, and no switching the git or `gh` identity (`moi-devrel/references/consent-and-identity.md`).
- Downloading any file, such as a logo or a photo: name the file and its source, then wait for a yes.
- `render.sh --force`, which renders over a failed check.
- Deleting a slide (say its title back first), a variant file or a PDF. Replacing a PDF that already exists and may have been shared: name it and ask first.
- Using a figure, a guest's title or an event outcome that no one supplied.
- Running a demo cue (`[RUN: ...]`) that spends devnet funds or deploys on devnet. This branch never runs a demo; a cue is text for the presenter.

Do the work yourself in the conversation. Sub-agents, bulk model runs and paid APIs: only when the operator names them, with the count and model stated first.

## Keys and access

No keys. Chrome and python3 run locally; node and poppler are optional. Poppins loads from Google Fonts, so the machine needs a network to match the design. Where each account and key lives is in `moi-devrel/references/keys-and-access.md`.

## Hand-back

Give the operator, briefly:

- The primary file (`<s>/deck/index.html`), the PDF path, and the script path. Name which file is primary if variants exist. Say whether anything was committed or pushed (nothing is without a yes).
- Check results: the last line of `check-deck.py`, and any WARN you chose to leave.
- What was left out and why: figures nobody supplied, claims you could not source, empty photo slots, slides without a script, anything stale you cut.
- How to present: open `index.html` in Chrome, arrows to move, `P` for the presenter window, share the deck window.
- A plain `Ready: yes` or `Ready: no, because ...`.
