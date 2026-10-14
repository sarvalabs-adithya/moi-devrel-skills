# Traps

Most rows come from real runs, mostly with no error message. A row marked (preventive) does not: it states a rule that follows from how the files work. Each row gives the symptom, the cause, and how it is caught: by a letter of `check-deck.py` (see `build.md` for what the letters mean) or by hand. States are as of 2026-10-02. "CC13" and "CC14" are community calls 13 and 14. The original CC14 deck is in `moi-foundation/MOI-Webinars` (`community-call-14/deck/`, merged 13 October 2026) and the intro session deck is in the handover repo (`skills/moi/moi-webinar/past-sessions/intro-session-deck/`); a cleaned CC14 is in `moi-webinar/community-call/examples/cc14`.

## The script and the presenter window

| # | Symptom | Cause | Catch |
| --- | --- | --- | --- |
| 1 | Arrow keys, dots and the `P` window are dead; the PDF is fine | A real line break, or a missing comma, inside a `NOTES` string kills the whole inline script. Hit on CC14 (fixed 24 Sep); the intro session deck still has it in the slide 4 notes | check a. Write notes with `sync-notes.py` |
| 2 | The presenter window shows an old script, no cues, or text that does not match the slide after a regenerate | On 4 Sep 2026 the previous operator reported this in at least six messages in a row. The root cause was not found (inferred: the regenerated file was not the one on screen) | By hand: name the exact path you regenerated, open it in a fresh tab, read one slide's notes in the presenter window |
| 3 | `NOTES` and `SCRIPT.md` disagree | Two copies edited separately. Seen on session 8: four of its 19 sections use a different cue notation in `NOTES` than in `SCRIPT.md`. Row 2 is not shown to be this | check h. Edit `SCRIPT.md`, then `sync-notes.py` |
| 4 | The presenter window says "MOI Builders · Intro" on a community call | The presenter title was hard-coded in the old template and copied into CC14 | check f. The new template reads `document.title` |
| 5 | The script has no clear "change slide now" points | Plain "Slide 2" headers, no PRESS NEXT cue (the CC14 `SCRIPT.md` before its headers were changed) | By hand: every slide block has a `PRESS NEXT --> SLIDE N` header |
| 6 | The script sounds cold, staccato or showy | Short punchy sentences, "not this, not that", applause closers | check n (partial), then read it aloud. Rules in `spoken-script.md` | <!-- slop-lint:ignore -->
| 7 | Some slides' notes were never polished | CC14 notes for slides 1 and 5 to 12 are first-draft machine text; no request to polish them is on record, so they appear to have had no voice pass (inferred) | By hand: read every presented slide's notes aloud |
| 8 | A run-of-show or checklist points at the wrong slide | Slide numbers in session 8's `GAMEDAY.md` (in `session-8-policies/`) and `RUNBOOK.md` (gitignored, so not in the repo; a cleaned copy is in `moi-webinar/examples/session-8/`) drift when slides move | By hand: search those files for "slide" after any insert or delete |
| 9 | A corrected claim reappears | A claim proved false in the session 7 blog survived in the README, the explainer, the demo plan and the deck notes | By hand: search every document and `NOTES` for the old wording after each correction |
| 10 | (preventive) The presenter says more than the protocol does | The CC14 host-answer prep carried a guard: do not say the app "pays for you" without qualification, because fee delegation covers fuel and nothing else | By hand: check each technical sentence against source (`spoken-script.md`) |

## Structure and layout

| # | Symptom | Cause | Catch |
| --- | --- | --- | --- |
| 11 | In a window that is not 1920 by 1080, one slide is unscaled and cropped; its badge is missing in the PDF; the page count is still right | A stray `</div>` closed the stage early (CC14 slide 10, in both variant files), so later slides sit outside the scaled stage | checks b and c. `node --check` and the page count cannot see it |
| 12 | "Remove slide 6" deleted the wrong slide | Badges ran one behind the pages | check c. Say the title back before deleting |
| 13 | Two neighbouring slides look the same | A deletion left equal backgrounds (CC14 slides 7-8 and 9-10; session 8 slides 10 to 13) | check d |
| 14 | Two `</div>` missing before `</body>` | Session 8's deck never closes the stage and viewport. Browsers repair it, so nothing visible | check b warns |
| 15 | A slide's last line or code line is cut off | Content past the slide edge, or code clipped inside its box (session 8 slide 10 loses the last line of the code block; CC14 slide 10 runs into the badge area) | check o with `--layout`, and look at the PDF page |
| 16 | (preventive) The PDF has more pages than the deck has slides | A malformed `<section>`, or a slide that spills. Reproduced with a nested section on 2026-10-02; no real deck is known to have it | `render.sh` compares the counts, keeps the old PDF and writes `<name>.pdf.rejected` |
| 17 | (preventive) The presenter window shows nothing or the wrong title for a slide | `TITLES` or `NOTES` has a different number of entries than the deck has slides, for example after adding slides without entries (reproduced on 2026-10-02) | check e. Add one `TITLES` and one `NOTES` entry per slide |
| 18 | (preventive) Two variants of one deck drift | Both edited by hand. On CC14 the two files ended up byte-identical instead | Edit the primary, re-cut the variant. check l warns when they are identical |

## Content and claims

| # | Symptom | Cause | Catch |
| --- | --- | --- | --- |
| 19 | Figures disagree across drafts | CC14 had three sources (report text 13.5%, dashboard 17.3%, an offhand "18%"). The 47 queries, 5 engines and 221 of 226 responses were flagged as older figures, with no fresh confirmation on record | By hand: keep a numbers ledger with source, date and who confirmed it. Ask for fresh figures; say which are old |
| 20 | A sentence has no source | Carried over between drafts: "the people we met there...", "Nobody is asking about the parts we discuss internally", "so Claude is the room left to grow" | By hand: for each sentence ask which source says it, then cut it or flag it |
| 21 | A slide is wrong by the next week | Relative words and live counts: "last Friday", "since the last call", "eleven agents are listed right now" | check i |
| 22 | A promise outlives its plan | CC13's video description promised guests for CC14; CC14 had none | By hand: search earlier announcements for teasers |
| 23 | Retired names on a slide | "Voyage devnet" and "account-centric" are wrong everywhere. "Building in Public" and "Open Q&A" were removed from the CC14 title and close | check f: FAIL for the first two, WARN for the others. Terminology is in `moi-devrel/references/terminology.md` | <!-- slop-lint:ignore -->
| 24 | A launch time is misread | Write 00:00 UTC with the date, never a 12-hour form (`moi-devrel/references/terminology.md`, table C) | check f |
| 25 | A feature is claimed that devnet does not run | Source-only features: the fee payer was in source but not live on devnet (as of 2026-09-10). The intro deck's slide 3 note still says "since v0.13.0 someone else can pay that fuel" | By hand: check the wire, or say "went live on devnet" only when told |
| 26 | A release candidate is presented as shipped | CC13: `js-moi-agent-registry v0.3.0-rc1` | By hand: check each package's release page |
| 27 | A slide title says more than the slide shows | CC13: "Everything That Shipped" held breaking changes only; a future-tense event slide sat next to photos of the event | By hand: read each title against its content |
| 28 | A product feature is invented | A slide presented a scoped grant as a launchpad feature | By hand: present only what the source shows; the launchpad is a playground, not the protocol |
| 29 | Words remain for a slide that was cut | "what our campaign is doing", "verify the campaign click-through", a sentence about moves after the arrows were removed | By hand: search for the cut topic's words (`build.md` checklist) |
| 30 | Content the previous operator removed | Removed from CC14, reasons not given (inferred pattern): competitor comparisons, unresolved metrics, third-party enterprise stories, trend arrows, event outcomes, a guest | By hand: ask the operator before including any |
| 31 | (preventive) A guest's title or a speaker's role is wrong | CC14's guest had no title in the material and the guest's public profile gave none, so the title was left off rather than guessed | By hand: leave it off unless the person supplied it |
| 32 | (preventive) Draft markers shipped | The blog drafts for sessions 8 and 9 carry `<<< EVIDENCE >>>` placeholders. `new-deck.sh` writes TODO markers in the same spirit | check m must be clean before hand-back | <!-- slop-lint:ignore -->
| 33 | An em dash on a slide or in notes | Em dashes typed into slide text and notes, one of them in a code comment on the intro session's slide 9 (session 8: slides 2, 3, 9 to 12, 15 and 17, and the notes of slide 14) | check g |
| 34 | History leaks into public material | On 2026-08-31 the Luma text and the blog still mentioned the cancelled session 8 plan, and were corrected. | By hand: read a deck as a stranger would, and cut cancelled plans and internal names |

## Files, process and tools

| # | Symptom | Cause | Catch |
| --- | --- | --- | --- |
| 35 | The README is wrong | CC14's said "13 slides", "both in place", "figures unchanged" after all three changed | check k (the count only). Update the README with every change |
| 36 | An edit silently did nothing | The search text did not match (CC14: alt text "Coinfest Asia, Bali") | Use the assert-before-write edit in `build.md` |
| 37 | The wrong design was built | For the intro session deck a PPTX, then a different HTML design, was rejected; the previous operator wanted exactly the session 8 look. Another time a transcript fix turned into a deck rebuild | Start from `templates/template.html`. Change only what was asked |
| 38 | Older decks have no HTML source | CC13 appears to exist only as a PDF built outside the repo (inferred); Builders session 7's deck is a PPTX edited by hand, with no generator | By hand: do not assume a source file. Whether one exists is not recorded (the previous DevRel's notes); ASK: Vardan for CC13, Rahul for session 7 |
| 39 | A deck lives on one machine | As of 2026-10-02 `community-call-14/` and `intro-session/` were untracked in the previous operator's working copy. Since 13 October 2026 community call decks 2 to 14 are in `moi-foundation/MOI-Webinars` and the intro deck is in the handover repo (`skills/moi/moi-webinar/past-sessions/intro-session-deck/`) | Check `git status` before trusting a new deck is saved anywhere. A push to the public repo needs a yes. Never push unasked |
| 40 | A logo is a web page, or has a stray box | A wrong Wikimedia file name returns an HTML 404; wordmarks carry bounding boxes (CC14) | `file --mime-type`, then look at the render |
| 41 | A tool cannot read a file | macOS blocked reads from `~/Downloads` and the Desktop | Ask the operator to `cp` it into the session folder |
| 42 | An em dash became `â` in a text file | Probably a file read or written in the wrong encoding (inferred; the cause was not found) | Use UTF-8 everywhere |
| 43 | Chrome writes the PDF but does not exit | On 2026-10-02 Chrome 154 on macOS, started with a temporary `--user-data-dir`, wrote the PDF and was still running 45 seconds later (reproduced; cause not isolated) | `render.sh` passes no profile directory and stops Chrome after `$RENDER_TIMEOUT`. In a sandboxed shell see `build.md` |
| 44 | (preventive) Text falls back to a plain font | Poppins loads from Google Fonts at open time, so an offline machine falls back. A fallback run measured 7 to 33px shorter blocks (`components.md`) | Render and present on a machine with a network |
| 45 | A PDF lands somewhere unexpected | Until 2026-10-02 `render.sh` resolved a bare PDF name against the current directory (found in review that day, fixed) | Read the `wrote <full path>` line. A bare name goes beside the deck |
