# Example: Community Call 14, September 2026

A cleaned copy of the one deck built in the current HTML framework for a community call. As of 2026-10-02 the original folder (`community-call-14/`) is untracked and exists only on the previous operator's machine, so this copy is the one a newcomer can open. ASK: Adithya for the original. Use this to see what a finished call looks like, and what to avoid. Do not copy its sentences without reading the table at the end. CC14 was held on 2026-09-25 (inferred from announcement copy pasted on 2026-09-24).

## What is here
| File | What it is |
|---|---|
| `deck/index.html` | The 12-slide deck, with three fixes (below). Open it in Chrome, press `P` for the presenter window |
| `deck/index-guest.html` | The same deck with a guest slide as slide 12 and the close as 13: the worked example of the deck branch's guest component (`moi-webinar/deck/references/guest-slide.md`). The guest is Mohit Bansal of Krexa, the CC14 guest whose slide was removed before the call. Only his name and company are on record, so his role and topic are dashed slots and both image frames are empty (`assets/guest/headshot.jpg`, `assets/guest/logo.svg`). Built 2026-10-13 by adding the slide, its `TITLES` and `NOTES` entries and the component CSS to a copy of `index.html`; nothing else differs |
| `deck/assets/engines/` | The four AI engine logos used on slide 6 |
| `deck/assets/` (no photos) | The two event photos of slide 10 are not here. They show identifiable third parties and no permission to show them is on record, so they were deleted from this copy. Slide 10 shows two empty frames that read their filenames (`assets/futuremode-1.png`, `assets/futuremode-2.png`), the deck framework's accepted pattern (`moi-webinar/deck/references/build.md`, "Photos and logos"). Check j of the deck checker warns about them, as intended. To restore real photos, ASK: Sai Kiran whether the event organisers allow reuse |
| `SCRIPT.md` | The script for slides 2 to 4, the slides the previous operator presented. Text unchanged, headers changed to the `PRESS NEXT` banner format |
| `numbers-ledger.csv` | Every figure on the slides, with source, date and status. 42 rows: 17 confirmed, 16 unverified, 9 retired |
| `sources/RELEASE-NOTE.md` | The protocol team's release note for moipod v0.13.0, copied on 2026-10-02 from the previous operator's machine with one change, a lint marker at the end of line 5 (the note's own wording trips the lint's midnight-time rule), where it is untracked. Its first line says "as sent by the protocol team, unedited". It is not: it carries the restructured sentences of the X thread, and the text first pasted on 2026-09-10 is not available (per the 2026-10-02 research). ASK: Adithya or Gokul for the original. The ledger and `references/release-slide-checks.md` point here |

The September release post is published in `sarvalabs/MOI-Website` as `blog/src/content/posts/moi-september-2026-release.md` (file name confirmed by the library research on 2026-10-02). It is not copied here: open it in that repo. The ledger cites it by section.

Left out on purpose: the guest portrait and the guest company logo (no permission to republish is on record; drop the files into `deck/assets/guest/` to see them), the "no guest" variant (byte-identical to the main file), both PDFs and the old README. To render a PDF into a scratch folder, with `SKILLS` set as `moi-devrel/SKILL.md` describes:
`d=$(mktemp -d) && bash "$SKILLS/moi-webinar/deck/scripts/render.sh" --force "$SKILLS/moi-webinar/community-call/examples/cc14/deck/index.html" "$d/MOI_Community_Call_14.pdf"`
The renderer refuses this deck while check d fails, so the example passes `--force`. On a real call, fix the backgrounds first. `--force` needs the human's yes.

## What was changed from the original
Only three things in the deck, each proved below. No slide content was changed. Separately, the two photos were deleted and the ledger sources were rewritten to point at files a newcomer can open.
1. **Slide 10 had one closing `</div>` too many.** The browser closed the stage early, so slides 11 and 12 became children of the viewport instead of the scaled stage and slide 10's badge was stranded outside its slide. In a window that is not 1920 by 1080 slide 11 was unscaled and cropped. The PDF looked fine and the page count matched. One line was deleted.
2. **The presenter window title was hard-coded** as "Presenter" followed by the intro session's name. It now reads "Presenter: " plus the page title.
3. **Em dashes** in the page `<title>` and two CSS comments became colons. None were in slide text.

Proof, run on 2026-10-02, with `SKILLS` as above and `EX="$SKILLS/moi-webinar/community-call/examples/cc14"` (so none of the commands depends on the working directory):
- The slide 10 fault, in a real Chrome DOM dump (`--headless=new --dump-dom`) of the original deck, parsed with Python's `html.parser`: before, slides 11 and 12 had parent `div.deck-viewport` and 9 of 10 badges were inside a section. After, all 12 slides have parent `div#stage.deck-stage` and 10 of 10 badges are inside their section. The same result holds on the raw file. The original deck is not in this library.
- `node --check` on the extracted inline script passes. A copy with a real line break inside a `NOTES` string fails with "Invalid or unexpected token", which shows the check can fail.
- `python3 "$SKILLS/moi-webinar/deck/scripts/check-deck.py" "$EX/deck/index.html" --script "$EX/SCRIPT.md"`: a, b, c, e, f, g, h, k, l, m and n PASS. d FAILs. i and j WARN. These are content faults left in on purpose: slides 7 and 8 are both `lav`, slides 9 and 10 are both `dark grad`, five relative-time phrases remain ("Since the last call", "last Friday" twice, "this month", "since the last call"), and the two photo files are absent.
- `bash "$SKILLS/moi-webinar/deck/scripts/render.sh" --force "$EX/deck/index.html" <scratch>/cc14.pdf` wrote 12 slides and 12 pages, a match, and added a WARN from its own check o: slide 10 content reaches y=1026, into the bottom margin where the badge sits. The page image shows the two empty frames.
- `python3 "$SKILLS/moi-webinar/community-call/scripts/ledger-check.py" "$EX/deck/index.html" "$EX/numbers-ledger.csv" --notes` exits 1: no figure is missing from the ledger, and 16 rows are `unverified`. That is the honest state of the call.

## What this run got right
- A first deck in four minutes from a pasted draft, rebuilt in the house framework with every figure kept as written.
- The person's numbers won. When the dashboard figures arrived, the older report figures were replaced and the replacement was stated. Three figures that could not be refreshed were flagged out loud.
- Real photos only. No stand-in image for the event and no guest title guessed. This copy ships the frames empty.
- The release took two slides, with the action-required slide holding versions, what to search for and what to rewrite. Versions, `-rc2` and `parseKmoi` were copied exactly from the release note.
- The new material got the room. The developer update was condensed on instruction.
- A public-call prune: competitor comparison, an unresolved metric, a tender story, per-engine arrows and a guest slide were removed.
- Slides 2 to 4 have a script in complete sentences, a bracketed host cue with a fifteen-second answer, and notes identical to the script file.
- The close is a logo and one line.

## What went wrong
1. The stray `</div>` on slide 10, found only by dumping the browser DOM. No check caught it at the time.
2. Neighbouring slides share backgrounds after the prune (7 and 8, 9 and 10), and slide 10's content runs into the bottom margin.
3. Residue from the cuts: slide 1's note says "what our campaign is doing"; slide 11 still says "Verify the campaign click-through"; slide 8 still lists "MOI versus Lit Protocol"; slide 6 still quotes movements after the arrows were removed.
4. Three figures never reconfirmed (47 queries, five engines, 221 of 226 responses) and one number used twice (12.8). 47 queries times 5 engines is 235, not 226.
5. The notes for slides 1 and 5 to 12 are first-draft machine text. No request to polish them is on record, so they appear to have had no voice pass (inferred).
6. The original README said "13 slides (with the guest speaker)" and "figures unchanged" after both stopped being true, and two identical variant files were kept.
7. A line break inside a `NOTES` string killed the inline script on 24 September. It was found and fixed the same day.
8. "Live on devnet" was not read from the node on the call day, and no check of the wire field name is on record. `moi-devrel/references/devnet.md` supports the claim as of 2026-10-02, so the ledger row is `unverified`. See `references/release-slide-checks.md`.
9. The script file used plain headers, so slide changes were not explicit. The copy here uses the banner format.
10. The deck took about 45 hours of wall clock against a two-hour cap, most of it waiting for inputs and changing decisions.
11. No post-call artefact is on record. See `references/after-the-call.md`.
12. The draft guest slide was a column of text with a 380 px portrait under it and a 86 px logo tile. On 9 October 2026 the previous operator called it poor and asked for a large headshot with role, company and a logo placeholder. `index-guest.html` shows the replacement.

## Sentences that must not be copied
| Where | Sentence | Why |
|---|---|---|
| Slide 2 | "the standard reserved for the fuel token" | Not in the release note, and not in the release post. See the worked table in `references/release-slide-checks.md` |
| Slide 2 | "So a new user, or an agent, can start with zero KMOI" | The release post says a new user can start without holding KMOI for fuel, and that an agent no longer needs to hold KMOI for its fuel. The post covers new users and agents for fuel only; keep that limit. The release note says neither |
| Slide 2 script | "every interaction paid its own fuel, so an account holding no KMOI could not do anything at all" | A universal of the kind removed from the release post. Needs the protocol team |
| Slides 2 and 3 | "live on devnet", "it is on devnet now" | Not read from the node on the call day. Supported as of 2026-10-02, so re-read it before each call |
| Slide 3 script | "errors that do not point at the cause" | Stated in no source |
| Slide 3 | The old id and the max supply and decimals limits | In the release post only. Trace to source |
| Slide 6 | "Gemini moved the most, up 12.8 points, while ChatGPT slipped 4.3" | Arrows were removed, the figures are unverified and 12.8 is also ChatGPT's level |
| Slide 6 | "221 of 226 responses, or 97.8%, so Claude is the room left to grow" | Never reconfirmed, and no Claude figure appears anywhere in the deck |
| Slide 7 | "Nobody is asking about the parts we discuss internally" | Not in the Scribble report. Added by the assistant |
| Slide 8 | "MOI versus Lit Protocol" | Competitor content, and the slide it belonged to was cut |
| Slide 9 | "Since the last call", "played last Friday" | Relative dates go stale |
| Slide 9 | 120+, 60+, 42, 20, "seventh" | Not reconfirmed since they were supplied. See the ledger |
| Slide 10 | "the people we met there are the ones we are now bringing onto these calls" and its note "several of those people are joining these calls as guests" | Carried over from an earlier slide with no source, and the final deck has no guest |
| Slide 11 | "Verify the campaign click-through and its attribution" | The campaign slide was cut. The metric is unresolved |
| Slide 11 | "A discussion about bringing the University of Hong Kong onto MOI" | A third-party discussion with no confirmed source. ASK: Sai Kiran whether it can be said publicly |
| Slide 1 note | "what our campaign is doing" | The campaign slide was cut |
