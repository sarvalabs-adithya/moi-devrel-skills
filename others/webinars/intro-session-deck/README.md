# Intro session deck

> **What this is:** the README for the deck of the MOI Builders *intro session*, "Your first agent on MOI": four ideas about MOI, then a live demo of the Agent Launchpad (a no-code site where you pick an agent template, register it on MOI with your wallet and run it on your laptop). MOI Builders is the developer webinar series DevRel runs; this one-off session is not numbered in the Session 1 to 9 series.
>
> **Status:** deck built 12 to 15 September 2026. Whether and when the session was held is not recorded in these notes (`skills/moi/moi-webinar/references/intro-session.md` says the same). That file also records that, when checked on 2026-10-02, `index.html` had two failures (the notes entry for slide 4 breaks the inline script, which kills the arrow keys, dots and presenter window; and there are em dashes in the title and one code comment). The PDF still prints. Fix those before presenting from the HTML.
>
> **Where things are:** `index.html` and `MOI_Builders_Intro.pdf` are in this folder. The session 8 deck whose framework this one copies is described in `skills/moi/moi-webinar/examples/session-8/` (the session 8 run sheet and notes), and its code is in https://github.com/moi-foundation/MOI-Webinars.
>
> **Terms:** *Meet* is Google Meet, where the session runs. *SIWM* is Sign In With MOI, a login where the wallet signs one message off chain and the server checks it against your address. *Relay* is the server that holds the Telegram bot token. *pm2* is a Node process manager that keeps the agent runtime alive. *AgentMarket* is the Coco logic (on-chain contract) behind the Launchpad's marketplace.

`index.html`: 11 slides, the same deck framework as session 8: fixed 1920×1080 stage, Poppins,
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
| script | lives in the `NOTES` array (a JavaScript list of per-slide speaker notes) at the bottom of `index.html`, one entry per slide |

Everything in the deck was read from the launchpad source at `sarvalabs/moi-agent-launchpad`
(`master` branch as read on 9 Sept 2026): the sign-in message (`lib/siwm.ts`), the SIWM recovery check
(`lib/moi/real.ts`), owner-signed `RegisterAgent` (`lib/moi/registry.ts`), the relay auth and the
Telegram isolation rules (`docs/how-it-works.md`), the runtime under pm2 (`agent-runtime/`), and
the `AgentMarket` Coco logic (`contracts/agent_market/agent_market.coco`).
