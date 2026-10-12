# MOI mini deck

A complete six-slide deck with neutral placeholder content. It claims no facts. Each main component appears once: cover, cards, steps with a code block, stats, a comparison table and a close. It passes every check of `check-deck.py`, including `--script` and `--layout`.

- `index.html` is the deck. Open it in Chrome, arrow keys to move, `P` for the presenter window.
- `SCRIPT.md` is the spoken script. Its blocks are word for word the `NOTES` array in `index.html`. It shows the `PRESS NEXT` headers and one bracketed cue.
- Check it (with `SKILLS` set as `moi-devrel/SKILL.md` describes): `python3 "$SKILLS/moi-webinar/deck/scripts/check-deck.py" "$SKILLS/moi-webinar/deck/examples/mini-deck/index.html" --script "$SKILLS/moi-webinar/deck/examples/mini-deck/SCRIPT.md" --layout`
- Render it from a scratch copy, so the PDF does not land in the library: `d=$(mktemp -d) && cp -R "$SKILLS/moi-webinar/deck/examples/mini-deck" "$d/mini" && bash "$SKILLS/moi-webinar/deck/scripts/render.sh" "$d/mini/index.html"` writes `index.pdf` beside the copy, 6 pages for 6 slides. The PDF is not stored here.

| | |
| --- | --- |
| flow | title, cards, steps and code, stats, comparison table, close |
| source | written for this branch, no outside material |
| photos | none |
| variants | none |
| script | `SCRIPT.md`, identical to `NOTES` |
| left out | photos and the beats, pills and diagram components; their markup is in `references/components.md` |
