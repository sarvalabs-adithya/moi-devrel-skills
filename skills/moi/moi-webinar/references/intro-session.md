# The Builders intro session: MOI in four ideas, then the Agent Launchpad live

Facts are as of 2026-10-02. A one-off session whose deck was built on 12 to 15 Sep 2026, probably for students or newcomers (inferred from the previous operator calling the Launchpad "a way for students to get exposed to agents"). Whether it was held, and its date, platform, size and whether it was recorded or announced, are not recorded. ASK: Adithya. Everything about the Launchpad as a product is `moi-launchpad-ops` (planned): until it exists ASK: Adithya for the app and Upendhar for anything on its VM. Back to `../SKILL.md`.

## Where it lives, and its state

- **Local only.** `intro-session/` (a deck `index.html`, `MOI_Builders_Intro.pdf` and a `README.md`) is untracked and exists only on the previous operator's machine. ASK: Adithya for a copy, and keep a second one.
- **Do not present from it as it stands.** `check-deck.py` on the file, run read-only on 2026-10-02, reports 2 FAIL.
  - Check a: slide 4's `NOTES` entry has real line breaks, so the inline script does not parse. The arrow keys, the dots and the presenter window are dead. The PDF still prints. The break probably came from the 15 Sep rewrite of slide 4 (inferred).
  - Check g: em dashes in the document title, the presenter title and a code comment on slide 9.
  - Warnings: a hard-coded presenter title, "right now" in two notes, and two contrast constructions.
  - Whether the session was given from the HTML or the PDF is unknown.
- **Start a new one with the deck branch** (`moi-webinar/deck`, `new-deck.sh`). The first build used a different design and was rejected: the previous operator wanted the same deck framework as session 8, exactly.

## The outline: 11 slides in two halves

| # | Title | Job |
|---|---|---|
| 1 | Your first agent on MOI | "What MOI is, in four ideas. Then a live agent: on chain, on your laptop, in your Telegram." |
| 2 | Start here | An agent today is a URL and an API key: nothing says who it is, there is no smaller unit of authority than the key, and no way to find or check one |
| 3 | Four ideas | Participants, interactions, native assets, logics, one breath each |
| 4 | Why agents on MOI | Two diagrams side by side. Elsewhere the app or the agent holds a copy of you. On MOI your account holds you, and a policy on it decides who may write |
| 5 | The launchpad | A no-code playground: pick a template, register it with your wallet, run it on your laptop and hear from it in Telegram |
| 6 | Live demo | Four beats, below, then a read-back from the chain |
| 7 | Under the hood | Two signatures happened and only one cost fuel: sign-in, then registration |
| 8 | Where it runs | The laptop holds the key and runs the runtime, a relay holds the bot token, Telegram delivers only to the owner |
| 9 | The marketplace | The AgentMarket Coco logic: `List` and `Subscribe`, with no amount parameter, so the buyer cannot underpay |
| 10 | Full circle | Each of the four ideas mapped to something the audience just did |
| 11 | Close | "Launch one today", the four steps, and that a new wallet is activated on chain by the site |

Slide 4 replaced an earlier slide that presented a scoped grant as a Launchpad feature. The previous operator rejected that on 15 Sep 2026 ("this is not a real feature of launchpad"), so the Launchpad is framed as a playground, not the protocol.

## The demo beats (slide 6)

The cue in the notes is to switch to the browser at `launchpad.moi.technology`.

1. **Connect.** The wallet shows a sign-in message. No transaction and no fee. The site checks that the signature recovers to the address.
2. **Pick.** The Weather Brief template: a city, a delivery time, a name. Deploy. The server creates a keypair for the agent, and that key is to end up on the presenter's laptop, not on the server.
3. **Register.** A second wallet popup, this one costing fuel: a `RegisterAgent` interaction on the registry logic. The owner is the presenter.
4. **Run.** Link Telegram and press Start, download the setup script and run it (pm2 starts the runtime), and the first message arrives.
5. **Read it back.** Open the agent page or the explorer and read the owner, the agent wallet, the status and the card URI off the chain. Then back to the slides.

Needs: the MOI Wallet extension with an account that exists on devnet, a Telegram account, `@moinetworkbot`, pm2 and node on the laptop. Never show or read a recovery phrase on the call.

## Before every run

1. **Rehearse the whole path on devnet.** A reset wipes the Launchpad's registration wallets, the platform wallet and every user wallet (`moi-devrel/references/devnet.md`). The Launchpad moved to the post-wipe registry on 2026-09-15, four days after the wipe announced for 11 September. A rehearsal that registers an agent spends devnet funds: the operator's yes first.
2. **Health check, read-only:** `curl -s https://launchpad.moi.technology/api/stats`. On 2026-10-02 one call answered `chainStatus` "stale" with `registered` 17, and a call a few minutes later answered "ok" with `registered` 0. Both showed 33 active agents and 22 owners. An idle site refreshes only when it is asked, so its first call can be stale: call again after 20 to 60 seconds, and trust only an "ok" answer. These numbers move: never put one on a slide. The previous operator used `registered` and not `activeAgents`, because the Launchpad code says the second overcounts.
3. **Re-read the Launchpad source** that the deck states: the sign-in message (`lib/siwm.ts`), the registration signature check (`lib/moi/real.ts`), the owner-signed `RegisterAgent` (`lib/moi/registry.ts`), the relay rules (`docs/how-it-works.md`), the runtime (`agent-runtime/`) and the market logic (`contracts/agent_market/agent_market.coco`), all in `sarvalabs/moi-agent-launchpad`. The deck was built from `master` as of 9 Sep 2026.
4. **What to say if the wallet popup does not appear** is not on record. Rehearse it and write it into the notes.

## Claims that must not be made

| Do not say | Why |
|---|---|
| "Live on Voyage devnet" | Corrected 15 Sep 2026. Say devnet. Voyage is the explorer and faucet product  <!-- slop-lint:ignore --> |
| A grant or policy as a Launchpad feature | The Launchpad does not offer one. It is a playground (15 Sep 2026) |
| "Since v0.13.0 someone else can pay that fuel for you" | Flagged 15 Sep, when devnet ran an older build, and still in the slide 3 notes. `net.Version` read 0.13.0 on 2026-10-02, but the `payer` or `fee_payer` field check has no record since the wipe. Run step 3 of `devnet.md` first. When said, add that the fee payer covers fuel and nothing else |
| "Eleven agents are listed right now, one of them paid" | A live number that went stale. Refresh it or cut it |
| "Storage policies are enforced today, and session 8 shows one live" | True only while the session 8 demo still passes. Rehearse it first (`session-history.md`) |
| "Ten templates", "10 AI calls a day" | Read from source on 9 Sep. Check each against `master` before use |
| "The site never saw a seed phrase" | A claim about the product, read from source on 9 Sep. Check it, and never invite anyone to type a phrase |
| That a new account is activated with starter KMOI | It depends on the Launchpad's registration wallets, which a reset wipes. Test with a fresh wallet |
| "A wallet, a Telegram account, ten minutes" | No timing was measured. Time it in rehearsal |

Wording: say participant-centric, never account-centric, and say devnet and network ID (`moi-devrel/references/terminology.md`). Define fuel where it is first needed, not in the opening line. <!-- slop-lint:ignore -->

## Not yet known

- When it was held, for whom, on what platform, whether recorded, and whether it repeats. ASK: Adithya.
- Whether it had an event page, a post or social copy. Nothing on file says so.
- Whether it was presented from the HTML or the PDF.
- What the demo does when the wallet popup does not appear.
