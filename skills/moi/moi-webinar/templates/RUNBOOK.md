<!-- TEMPLATE NOTES (delete this comment when the file is filled in)
Derived from the session 8 run sheet. Reader: the presenter, during the talk. It owns the clock, what
to do per block, the likely questions and the recovery table. It does not restate the script: the
words are in SCRIPT.md. Refer to slides by TITLE, not number, because numbers drift when a slide is
inserted (session 8: the sheet said 18 slides and the deck had 19). Ignored by git in the scaffold.
-->
# Session {{NUMBER}} run sheet: FILL topic

FILL minutes, FILL slides. Deck at `deck/index.html`, terminal in `{{FOLDER}}/`. FILL One sentence on how the demo relates to the idea.

---

## Before going live (T-30 min, do all of it)

From the root of the working copy. The setup commands and the demo spend devnet funds, so each needs the operator's yes.

```bash
cd {{FOLDER}}
npm run preflight          # FILL what it checks
FILL setup commands that top things up
npm run demo               # ONE full rehearsal, leaves state clean
```

- [ ] All exit 0. If the rehearsal fails there are 30 minutes to debug. Do not skip it.
- [ ] Owner balance printed at least FILL (the measured threshold and its date)
- [ ] Open `deck/index.html`, full screen, arrow through once
- [ ] Terminal font at presentation size, about 100 columns so banners do not wrap
- [ ] The pause variable (`DEMO_PAUSE_MS`) ready on the demo command: at full speed the run is unwatchable
- [ ] The event page title carries the right numeral ({{ROMAN}} or #{{NUMBER}})

FILL Say what the demo heals by itself (a leftover from a crashed run) and what it refuses to start without.

---

## The talk (times are cumulative)

### 0:00, FILL slide titles: WHY this exists (FILL min)

FILL The block's purpose in a line. Then one short paragraph per slide, by title: what to do, what to ask the room, what to land. Mark the slide the whole session hangs on.

### FILL time, FILL slide titles: the mechanism (FILL min)

FILL

### FILL time, FILL slide titles and terminal: THE DEMO (FILL min)

FILL Each beat: the command, the line to read aloud from the output, the sentence to say.

If someone asks to see it again: FILL say whether a rerun is idempotent and what it costs.

### FILL time, FILL slide titles: what you just saw (FILL min)

FILL

### FILL time, FILL slide title: the honest part (FILL min)

FILL What is not live, said plainly. Name the question that must not walk you into a claim.

### FILL time, FILL slide title and Q&A (FILL min)

FILL Repo, faucet, what one funded wallet is enough for.

Cut rule: FILL (for example, cut beat 4 when short, never beat 2).

---

## Likely questions, short answers

**"FILL question?"** FILL two-sentence answer, with the limit stated.

**"Can I do the headline thing, today?"** FILL answer it with what is live, not what is declared.

---

## If it breaks live

| Symptom | Cause | Do |
|---|---|---|
| `insufficient funds` on FILL | FILL | FILL |
| RPC timeouts | devnet down | FILL fall back to the receipts in `NOTES.md` |
| whole node dead | none | the deck stands alone; present it as what the demo does, and offer a recorded run after |

The single rule: never claim more than the screen shows. If the demo dies, the session becomes a talk with receipts, which is still honest.
