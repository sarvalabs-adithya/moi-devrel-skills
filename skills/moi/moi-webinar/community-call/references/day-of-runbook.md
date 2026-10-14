# Day-of runbook

Presenting the deck: browser, presenter window, sharing, the PDF fallback and the stale-content sweep. Facts are as of 2026-10-02. The live part has one source, the CC14 deck's own code and its README (now in `community-call-14/deck/` of the webinars repo). Per the handover note (2026-10-13) the room is a Riverside room run by Vardan and every call is recorded to the MOI YouTube playlist. `SKILLS` is the folder that holds the `moi-*` skills; run every command from the working copy that holds `community-call-<N>/`. Back to `../GUIDE.md`.

## The day before
1. Rehearse once aloud with the deck open and the presenter window up. The Wednesday before the call was rehearsal day for CC13. Whether CC14 had one is not recorded.
2. Run the checks again: `python3 "$SKILLS/moi-webinar/deck/scripts/check-deck.py" community-call-<N>/deck/index.html --script community-call-<N>/SCRIPT.md` and `python3 "$SKILLS/moi-webinar/community-call/scripts/ledger-check.py" community-call-<N>/deck/index.html community-call-<N>/numbers-ledger.csv --notes`. A FAIL on either gets fixed or put to the human as a decision. Rows the human kept as `accepted-unverified` are listed in the hand-back, not hidden.
3. Export the PDF with `bash "$SKILLS/moi-webinar/deck/scripts/render.sh" community-call-<N>/deck/index.html MOI_Community_Call_<N>.pdf` and keep it beside the HTML. Open it once and read every page.
4. Copy the deck folder to a second place. A new call folder exists only on your machine until it is merged (the old decks went in by PR #2 on 13 October 2026). A lost laptop loses the deck. A copy on another local disk needs no yes. A copy in Drive or other cloud storage is an upload and needs the human's yes. Saving to the repo is a push and needs a yes, and `moi-foundation/MOI-Webinars` is public. Where the second copy should live: ASK: Vardan or Rahul.

## One hour before: the sweep
Open the deck from the file you will present and look for anything that went stale since the build.

| Look for | Why |
|---|---|
| "last Friday", "since the last call", "this month", "this week" | Relative dates go stale. Replace with a date or cut |
| Any figure in the ledger with status other than `confirmed` | Do not say it aloud unless the human has decided to |
| "Voyage devnet", "Building in public", "Open Q&A" | Retired phrases | <!-- slop-lint:ignore -->
| A release version or status | Did anything ship or change since the build? Ask the protocol team. Read the live node for "live on devnet" (see `release-slide-checks.md`) |
| Names of speakers, hosts, guests | Confirm each is on the call. The 24 August plan was to speak to every presenter first |
| Photos and logos | They load, and the human has the right to show them |
| Teasers about the next call | Delete any that are not confirmed |
| A slide for a segment whose owner dropped out | Remove it and run `pruning-checklist.md` |

## Presenting
1. Open `deck/index.html` in Chrome. Arrow keys, space, Page Down or a click on the right half of the screen go forward. A click on the left half, the left arrow or Page Up go back. Home and End jump to the first and last slide. The dots at the bottom jump to a slide. The slide number is in the address, so a reload returns to the same slide.
2. Press `P` for the presenter window. It shows the script for the slide, the title of the next slide and a clock that starts when the window first opens. Arrow keys work in it too and drive the deck.
3. If `P` does nothing, the browser blocked the pop-up. The code opens the window and returns without a message when it is blocked. Allow pop-ups for the page and press `P` again.
4. In the meeting, share the deck window and keep the presenter window on your own screen. Share only the deck window, as the README says, so the script stays on your own screen. Platform: the handover note says Riverside; the CC14 README names Meet. Confirm with Vardan how the speakers join and how the audience watches.
5. Fonts load from Google Fonts when the page opens. With no network the deck falls back to a generic sans-serif and the layout shifts. Open the deck before the call, not during it.
6. The stage is 1920 by 1080 and scales to the window. A 16:9 window looks right. Other shapes show bars.
7. At the slide with a host cue, wait for the host. If the question comes, read the bracketed cue. If it does not come, move on. The cue is never read unprompted.
8. If a question is outside what is confirmed, use the fallback line from `host-qa-prep.md` and note it for the follow-up log.
9. Keep an eye on the clock. The presenter window runs from the first `P`, not from the start of the call.
10. At the close, the last slide is a logo and one line. Say the line and hand back to the host.

## If the deck breaks
| Symptom | Cause | Do |
|---|---|---|
| Arrow keys, dots and `P` all dead, slides still show | The inline script has a syntax error, usually a real line break inside a `NOTES` string | Share the PDF. Open `SCRIPT.md` on your own screen for the words. Fix the deck after the call. Check a of the deck checker finds this before the call |
| The last slides are cropped or unscaled when the window is not 1920 by 1080 | A stray closing `</div>` moved slides out of the stage | Same fallback. Check b finds it |
| A photo frame shows a filename | The photo file is missing | Say nothing about the photo and move on, or skip the slide |
| Presenter window shows an old script | The deck was reopened from an old file or tab | Close both windows, reopen the right file in a fresh tab, press `P` |

The PDF is slides only. It has no presenter window, no script and no animation. It prints correctly even when the script is broken, because the print styles need no JavaScript. That is why a PDF check alone never proves the deck works live.

## Screen and files
- On the previous operator's Mac, tools could not read `~/Downloads` (27 August 2026; this may no longer apply). If a file will not open, ask the human to copy it into the call folder with `cp`.
- A live demo that spends devnet funds or deploys on devnet needs the human's yes first, and it uses the MOI Wallet extension and the operator's own funded account. Claude never handles a recovery phrase, including a throwaway one. If one is pasted into the chat, do not repeat it, tell the operator it is exposed, and carry on with the wallet extension.
- Close private windows and tabs before sharing. The presenter window title reads "Presenter: " followed by the deck title in decks built from the current template.

## After the last slide
1. Stop the recording only when the host does. Vardan owns the recording.
2. Write down every audience question and who owns the follow-up. The January 2026 KRA document asks for them within 48 hours.
3. Go to `after-the-call.md`.

## Not yet known
- Start time, length and who admits guests. ASK: Vardan.
- Who starts the recording in the Riverside room. ASK: Vardan.
- Whether a backup presenter exists. ASK: Rahul or Vardan.
