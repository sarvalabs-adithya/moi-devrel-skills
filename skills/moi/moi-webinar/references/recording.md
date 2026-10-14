# Recording: the rehearsal video, the voiceover and the live recording

Facts are as of 2026-10-02. Three different things are called a recording. The evidence is thin for the third. Uploading, sharing or deleting any recording needs the operator: an upload or share is a gate, and deleting a recording or a notes document is the operator's own action, after asking the file's owner (`moi-devrel/SKILL.md`, Gates). Back to `../SKILL.md`.

## 1. The rehearsal video: the fallback for a dead demo

A clean run of the demo, recorded in a terminal, kept one click away on game day (`game-day.md`). Session 8's lives in `recording/` (`demo.tape`, `demo.mp4`, `demo.gif`, tracked on the branch).

- **Tool.** `vhs` reads a `.tape` file. The invocation was not recorded. The usual form is `vhs recording/demo.tape` run from inside `session-<N>/`, because the tape's paths are relative to that folder (inferred). `session-preflight.sh` found `vhs` and `ffmpeg` on the previous operator's machine on 2026-10-02, and it warns when they are missing.
- **The tape.** Session 8's, without its comments:
  ```
  Output recording/demo.mp4
  Output recording/demo.gif
  Set Shell zsh
  Set FontSize 16
  Set Width 1500
  Set Height 950
  Set Theme "Catppuccin Mocha"
  Set Padding 22
  Set TypingSpeed 50ms
  Type "# Same call. Same key. Three times."
  Enter
  Sleep 1500ms
  Type "DEMO_PAUSE_MS=1200 npm run demo"
  Enter
  Sleep 100s
  ```
  The standalone run measured 37 seconds plus about 7 seconds of pauses, so 100 seconds is a safe sleep. Change the typed lines to your demo.
- **It is a real run.** The tape's own header says every interaction in it is real. Recording spends devnet funds, so it needs the operator's yes with the paying account and cost shown.
- **It dates itself.** A reset wipes devnet (`moi-devrel/references/devnet.md`), so the hashes in an old video probably no longer exist on chain (inferred). Session 8's was recorded on 31 Aug 2026 (file times), before the wipe announced for 11 September 2026 (`moi-devrel/references/devnet.md`, reset history). Record again after any reset, or drop the line "every hash in it is on chain" from the fallback, and say the date of the run.
- **Check the video** before game day: play it through once, with the sound off, and confirm the refusal text is readable at the size it will be shown.

## 2. The narrated voiceover: a learning aid

Made on 31 Aug 2026 after the presenter asked for a recording "so I can learn" and then for a voiceover of the presentation. Whether it was ever shared is unknown.

1. One text file per slide under `recording/vo/` (`01.txt` and so on), taken from `SCRIPT.md`.
2. Text to speech through Groq. Three voices were tried (`orpheus-austin`, `orpheus-hannah`, `orpheus-troy`) and the previous operator picked Austin. Gemini speech was rejected because it is no longer free. Groq required accepting its terms first (a step for the operator, not Claude). The key is `GROQ_API_KEY`: a secret, never in the repo or the chat.
3. `recording/build-vo.sh` (zsh) joins `vo/slide-NN.wav` with 1.2 seconds of gap into `narration.m4a` and writes `timings.txt`, using `ffmpeg` and `ffprobe`. It stops when a wav is missing.

Known defects in what is stored. Wavs exist only for slides 1 to 9 and 13, so the narrated video is incomplete. The script loops over slides 1 to 13 while the deck has 19, so its slide list is probably from an earlier deck (inferred). `vo/01.txt` shows mojibake: an em dash became a garbled character. Em dashes must not be in the script at all (`moi-webinar/deck/references/spoken-script.md`).

## 3. The live session recording

- **Platform and host.** Sessions II, III and 8 are on record as Google Meet calls (the Gemini notes of II and III, and session 8's checklist). The Gemini notes of Builders II and III, and the recording of II, sit in Drive under the shared account `info@moi.technology`, shared into the previous operator's Drive. Gemini notes or a Meet recording for IV to VII were not found in Drive (an edited session VII video exists, see below). Vardan provides the Google Meet link (`project-handover-docs/DEV-WEBINARS.md`). Who starts the recording, and whether it was started for IV to VIII, is not recorded. ASK: Rahul.
- **Gemini notes.** They mishear names and amounts ("Moy" for MOI, "KOI" for KMOI, "Grock" for Groq, "Open Claw", "Server Labs"). Never copy a name, figure or token amount from them without checking. A Meet started twice makes two notes documents: use the longer one.
- **Seed words.** Never read recovery words on a recorded call. They end up in the notes (2026-09-24).
- **Where it is published.** Not recorded for any session.
- **The external editor.** An editor outside the org domain cuts the videos from a personal account. A standup on 7 Aug names an editor, "Krishna" (the match is inferred). The edit of session 7 appears as `Builder series/MOI BUILDERS SEARIES VII.mp4` (866 MB, 2026-09-07), inside a folder named for another project (`Launchpad video`), owned by the editor. The file name has a typo. It took about a month. Raw clips and finals are hundreds of megabytes: do not copy them into other folders, and do not search only `owner = 'me'` in Drive, because the editor owns them.
- **The brief.** No brief format is on record. For the launch video the editor needed a script and numbered screen clips. The editor's contact and what was sent are not recorded (the previous DevRel's notes). ASK: Rahul.
- **YouTube.** A 7 Aug 2026 standup decided to post video AMA clips only. Whether that covers Builders recordings is unknown. Vardan holds the YouTube login (`DEV-WEBINARS.md`).

## Checklist

- [ ] The rehearsal video is recorded on the current node, the date is known, and the operator has played it.
- [ ] The operator knows who starts the live recording and where the file lands.
- [ ] After the session the recording's owner has it, and the editor has the files and a brief (a share needs a yes).
- [ ] Any name or figure taken from notes was checked against the source.
- [ ] Nothing with a recovery phrase was shown or read.

## Not yet known

- Whether Builders sessions are recorded every time, where they are published, and whether a link goes to registrants. ASK: Rahul.
- Whether sessions I and IV to VIII were all edited: not recorded (the previous DevRel's notes). ASK: Rahul.
- Whether the voiceover was ever used by anyone but the presenter.
