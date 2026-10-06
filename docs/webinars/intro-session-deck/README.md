# Intro session deck

`index.html` — 11 slides, the same deck framework as session 8: fixed 1920×1080 stage, Poppins,
MOI brand tokens, chips, cards, beats, the planetoid watermark, staggered reveals.

- Open `index.html` in Chrome. Arrow keys, space, or click to move; dots at the bottom jump.
- **Press `P` for the presenter window.** It holds the full talk script per slide, the next-slide
  title and a clock, and it drives the deck. In Meet, share the deck window and keep the presenter
  window on your own screen.
- `MOI_Builders_Intro.pdf` is the slides-only export (no script). Regenerate after any edit:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --no-pdf-header-footer --virtual-time-budget=8000 \
  --print-to-pdf="$PWD/MOI_Builders_Intro.pdf" "file://$PWD/index.html"
```

| | |
| --- | --- |
| flow | title → start here → four ideas → why agents on MOI → the launchpad → **live demo** → under the hood → where it runs → the marketplace → full circle → close |
| demo cue | slide 6 → browser (`launchpad.moi.technology`) → wallet popup → Telegram → agent page → back to slide 7 |
| script | lives in the `NOTES` array at the bottom of `index.html`, one entry per slide |

Everything in the deck was read from the launchpad source at `sarvalabs/moi-agent-launchpad`
(`master`, 9 Sept 2026): the sign-in message (`lib/siwm.ts`), the SIWM recovery check
(`lib/moi/real.ts`), owner-signed `RegisterAgent` (`lib/moi/registry.ts`), the relay auth and the
Telegram isolation rules (`docs/how-it-works.md`), the runtime under pm2 (`agent-runtime/`), and
the `AgentMarket` Coco logic (`contracts/agent_market/agent_market.coco`).
