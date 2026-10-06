# MOI-Webinars — Complete Project Overview & Demo Runbook

One-stop reference for **everything in this repo** plus a **beat-by-beat live demo flow** for Session 3 (the OpenClaw × MOI Agent Registry demo).

> Audience: anyone picking this repo up cold — your boss, a teammate, your future self. Read top-to-bottom in order or jump straight to [Part 3 — Live demo flow](#part-3--live-demo-flow) if you're going on stage in the next ten minutes.

---

## Table of contents

- [Part 0 — TL;DR](#part-0--tldr)
- [Part 1 — What MOI is and why this repo exists](#part-1--what-moi-is-and-why-this-repo-exists)
- [Part 2 — Repo orientation (file by file)](#part-2--repo-orientation-file-by-file)
  - [Session 1 — CocoLab + SDK fundamentals](#session-1--cocolab--sdk-fundamentals)
  - [Session 2 — Native Assets (MAS0 + TaxToken)](#session-2--native-assets-mas0--taxtoken)
  - [Session 3 — On-chain Agent Registry × OpenClaw](#session-3--on-chain-agent-registry--openclaw)
- [Part 3 — Live demo flow (Session 3)](#part-3--live-demo-flow)
  - [What lives where (on this laptop)](#what-lives-where-on-this-laptop)
  - [Pre-flight checklist (5 min before)](#pre-flight-checklist-5-min-before)
  - [Pane layout](#pane-layout)
  - [Beat-by-beat narration](#beat-by-beat-narration)
  - [Failure modes & live recovery](#failure-modes--live-recovery)
- [Part 4 — Reference](#part-4--reference)
  - [Every config knob](#every-config-knob)
  - [Commands cheat sheet](#commands-cheat-sheet)
  - [On-chain state right now](#on-chain-state-right-now)
  - [Q&A backup](#qa-backup)

---

## Part 0 — TL;DR

**This repo holds three sessions of a webinar series** teaching developers to build on MOI, a public blockchain optimized for AI-agent identity, assets and coordination).

- **Session 1** — write a Coco smart contract (`Flipper`, `ContextFlipper`), deploy it from JavaScript, mint a vanilla native asset (preview of Session 2).
- **Session 2** — go deeper on native assets: vanilla `MAS0` token and a custom `TaxToken` (5% fee-on-transfer, written in Coco).
- **Session 3** — the headline demo: an **OpenClaw skill** called `moi-agent-dating` that lets a real third-party AI agent framework (OpenClaw, by Nous Research) register on MOI's on-chain agent registry, discover other agents, and message them — all driven through OpenClaw's natural-language chat UI.

**Right now on this laptop, the Session 3 demo is fully wired up:**

- Two OpenClaw profiles (`jack`, `jill`) already configured
- The skill installed in both, both showing `✓ Ready`
- `agent_12 (Jack)` and `agent_13 (Jill)` already on devnet from the last rehearsal
- A one-command launcher (`start-demo.sh`) that brings up the three background HTTP services needed for the live demo

If you only have 30 seconds: [jump to Part 3](#part-3--live-demo-flow).

---

## Part 1 — What MOI is and why this repo exists

### What MOI is (one paragraph)

MOI is a public blockchain whose value prop is **identity, ownership and coordination for AI agents**. Concretely it ships:

1. **Cocolang** — a contract language built around interactions (its txns) and participants, not gas-and-storage abstractions.
2. **Native assets** (`MAS0`, `MASX`) — first-class tokens with controllable supply, transfer rules, and fee-on-transfer logic, all without writing ERC-20 boilerplate.
3. **On-chain agent registry** — a canonical place where any AI agent can publish its identity (name, URL, capabilities, owner wallet) and any other agent can discover them. This is the central piece for Session 3.

### Why this repo exists

It's the live-demo repo for the **MOI Builders webinar series**. Each session is a self-contained sub-directory you can `cd` into, `npm install`, and run with plain `node`. No build system, no shared monorepo tooling — every script is meant to be readable end-to-end.

### How Session 3 fits in the bigger picture

Sessions 1 and 2 teach you to write contracts and mint assets. **Session 3 is where it gets interesting** — once agents can transact and own assets on MOI, they need an identity layer to find each other. The agent registry is that layer, and the `moi-agent-dating` OpenClaw skill is the proof that the registry works with a real third-party agent framework, not just our own SDK scripts.

---

## Part 2 — Repo orientation (file by file)

### Top-level layout

```
MOI-Webinars/
├── README.md             ← short pointer to each session
├── OVERVIEW.md           ← this file
├── .gitignore            ← ignores **/.env and **/.env.local everywhere
├── session-1/            ← CocoLab + SDK fundamentals
├── session-2/            ← Native Assets (MAS0 + TaxToken)
└── session-3/            ← Agent Registry × OpenClaw (the headline demo)
```

The whole repo is a public devnet playground — no production code, no production keys, every `.env` is gitignored.

### Session 1 — CocoLab + SDK fundamentals

**Purpose:** teach Coco basics (state, actor context) inside CocoLab (REPL), then deploy the same logic from JS via `js-moi-sdk`. Closes with a sneak peek of native assets.

```
session-1/
├── README.md                       ← runbook
├── package.json                    ← pins js-moi-sdk, dotenv, yaml
├── .env.example                    ← template for MOI_MNEMONIC + LOGIC_ID
├── flipper/
│   ├── flipper.coco                ← simplest stateful contract — toggles a bool
│   ├── flipper.json                ← compiled manifest (checked in)
│   └── coco.nut                    ← coco module manifest
├── context-flipper/
│   ├── context_flipper.coco        ← per-actor bool, demonstrates ctx.msg.sender
│   ├── context_flipper.json        ← compiled manifest
│   └── coco.nut
└── sdk/
    ├── deploy.js                   ← Demo 3a — deploys flipper.json, prints Logic ID
    ├── flip.js                     ← Demo 3b — calls Flip() on the deployed logic
    ├── mode.js                     ← Demo 3c — calls Mode() (read-only), prints value
    ├── asset.js                    ← Sneak peek of Session 2: creates an MAS0 asset
    ├── bulk-flip.js                ← Load-test helper — fires N flips with nonce mgmt
    └── ASSET_TASK.md               ← Notes for the live asset segment
```

**Demo arc:** open `flipper/` in CocoLab → walk REPL → exit → `node sdk/deploy.js` → paste interaction hash into voyage explorer → set `LOGIC_ID` in `.env` → `node sdk/flip.js` → `node sdk/mode.js` → `node sdk/asset.js` to tease Session 2.

### Session 2 — Native Assets (MAS0 + TaxToken)

**Purpose:** show MOI's native asset system in two flavors — out-of-the-box `MAS0` (Demo 1) and a custom Cocolang `TaxToken` with fee-on-transfer logic (Demo 2). Submissions feed a token bounty form.

```
session-2/
├── README.md                       ← runbook + bounty form link
├── package.json                    ← pins js-moi-sdk + dotenv
├── .env.example                    ← MOI_MNEMONIC template
├── coco/
│   ├── taxtoken.coco               ← 5% fee-on-transfer asset
│   ├── taxtoken.json               ← compiled manifest
│   └── coco.nut
└── sdk/
    ├── asset.js                    ← Demo 1 — creates a 1M-supply WEBINAR MAS0
    └── tax-deploy.js               ← Demo 2 — deploys TaxToken logic
```

**Demo arc:** `node sdk/asset.js` → prints Asset ID → `node sdk/tax-deploy.js` → prints another Asset ID → both go into the bounty form at <https://forms.gle/NNK58E3vAyF6EYw9A>.

### Session 3 — On-chain Agent Registry × OpenClaw

**Purpose:** the headline demo of the series. We take a real third-party AI agent framework (**OpenClaw**, by Nous Research) and give it on-chain identity by writing a single OpenClaw skill that wraps the `js-moi-agent-registry` SDK. Two OpenClaw agents (Jack and Jill) register, discover each other, and exchange a message — all through OpenClaw's natural-language chat UI, all backed by real on-chain reads/writes.

```
session-3/
├── README.md                       ← cheat sheet for the demo flow
├── README.md                       ← demo cheat sheet (Demo 1 SDK + Demo 2 OpenClaw)
└── moi-agent-dating/               ← the OpenClaw skill itself
    ├── SKILL.md                    ← agent-facing instructions (YAML frontmatter + body)
    ├── README.md                   ← install + Jack & Jill demo runbook
    └── scripts/
        ├── package.json            ← pinned: js-moi-sdk@0.7.0-rc16, js-moi-agent-registry@0.1.0
        ├── .env.example            ← template for standalone smoke tests
        ├── .env                    ← local mnemonic (gitignored)
        ├── register.mjs            ← Op 1: createAgent() + on-chain profile read-back
        ├── discover.mjs            ← Op 2: getAllAgentIds() + per-agent getAgentProfile()
        ├── say-hi.mjs              ← Op 3: resolve target URL via registry → POST /message
        ├── message-server.mjs      ← Tiny /message inbox each agent runs (dual-stack ::)
        ├── uploader.mjs            ← Shared data:-URI card uploader shim
        └── start-demo.sh           ← One-command launcher for all 3 background services
```

#### What each file actually does

**`SKILL.md`** — OpenClaw skill manifest. YAML frontmatter declares the skill needs `node` binary and `MOI_MNEMONIC` env. Body tells the LLM: "when the user says 'register', run `exec node {baseDir}/scripts/register.mjs`; when they say 'discover', run `discover.mjs`; etc." This is what makes OpenClaw's model pick the right script when the user types in plain English.

**`scripts/register.mjs`** — Builds a `VoyageProvider('devnet')` + `Wallet.fromMnemonic(...)`, calls `AgentRegistry.init({ wallet, uploader: buildHostedUploader(...) })`, then `registry.createAgent(spec, agentCard)` with the agent's name/url/skills. Prints the assigned `agent_id` plus the on-chain profile read back from devnet.

**`scripts/discover.mjs`** — Same wallet+registry setup, then `getAgentCount()` and `getAllAgentIds()`, then loops `getAgentProfile(id)` and prints each. No fuel needed (read-only).

**`scripts/say-hi.mjs`** — Takes `<targetAgentId>` plus an optional message as argv. Looks up the target via `registry.getAgentProfile()`, extracts the URL, then does an `HTTP POST {url}/message {from, text}`. Prints the reply.

**`scripts/uploader.mjs`** — Tiny HTTP server on port 7777. Accepts POSTed agent card JSON, returns `{ uri: "data:application/json;base64,..." }` so `register.mjs` has somewhere to "upload" the card. In production you'd swap this for IPFS or a real CDN.

**`scripts/message-server.mjs`** — Tiny HTTP server that listens on `$PORT` and implements `POST /message {from, text}` → `{ ok: true, text: "<reply>" }`. Each agent runs one of these so other agents have something to POST to. **Replies are generated by OpenAI** (Chat Completions API, default model `gpt-5.4-mini`) using a per-agent `AGENT_PERSONA` env var — `start-demo.sh` ships Jack as upbeat-and-helpful and Jill as thoughtful-and-sardonic, so the demo conversation actually feels like two distinct agents instead of an echo loop. If `OPENAI_API_KEY` isn't exported in the shell that ran `start-demo.sh`, the server transparently falls back to a dumb echo so the plumbing still demos offline. **Binds on `::` (dual-stack)** so Node 18+ `fetch('http://localhost:...')` reaches it whether DNS resolves to `127.0.0.1` or `::1`.

**`scripts/start-demo.sh`** — Brings up all three background services in one shot: uploader on `:7777`, Jack's inbox on `:3940`, Jill's inbox on `:3941`. Run this every time you reboot the laptop or kill the dev servers.

---

## Part 3 — Live demo flow

This is the **detailed step-by-step** for the Session 3 demo. Read this section in full before walking into the room.

### What lives where (on this laptop)

The demo touches files in three places — useful to know if anything breaks mid-demo:

| Lives at | What it is |
|---|---|
| `~/MOI-Webinars/session-3/moi-agent-dating/` | Source-of-truth skill (this repo) |
| `~/.openclaw-jack/openclaw.json` | Jack's profile config (model, OpenAI key ref, skill env) |
| `~/.openclaw-jill/openclaw.json` | Jill's profile config (same shape, different `AGENT_NAME`/`AGENT_URL`) |
| `~/.openclaw/workspace-jack/skills/moi-agent-dating/` | Skill installed for Jack (incl. `node_modules`) |
| `~/.openclaw/workspace-jill/skills/moi-agent-dating/` | Skill installed for Jill |
| `/tmp/uploader.log` | Card uploader stdout |
| `/tmp/jack-msgserver.log` | Jack's inbox stdout — every POST to him lands here |
| `/tmp/jill-msgserver.log` | Jill's inbox stdout — **this is the "money shot" tail during the demo** |

### Pre-flight checklist (5 min before)

In one terminal, run these in order. Every line should either print success or be silent:

```bash
# 1. Confirm env vars are baked into .zshrc so all panes inherit them
echo $OPENAI_API_KEY | head -c 20    # → sk-…
which openclaw                        # → /Users/adithyaganesh/.openclaw/bin/openclaw

# 2. Confirm both OpenClaw profiles see the skill as ready
openclaw --profile jack skills info moi-agent-dating | grep Ready
openclaw --profile jill skills info moi-agent-dating | grep Ready
# both should print: moi-agent-dating ✓ Ready

# 3. Bring up the 3 background HTTP services
~/MOI-Webinars/session-3/moi-agent-dating/scripts/start-demo.sh
# expect: three LISTEN lines + "All three servers up"

# 4. Confirm the on-chain registry is reachable (this is your last sanity check)
cd ~/.openclaw/workspace/skills/moi-agent-dating/scripts
node --env-file=.env discover.mjs | head -5
# expect: [discover] registry total: <N>   then a list of agents
```

If any of those four steps fails, see [Failure modes & live recovery](#failure-modes--live-recovery) **before** opening the chat panes.

### Pane layout

Open three terminal panes in this layout (split-view or three tmux windows — whichever you prefer):

```
┌──────────────────────────────────────┬──────────────────────────────────────┐
│                                      │                                      │
│   PANE 1 — Jack's chat               │   PANE 2 — Jill's chat               │
│                                      │                                      │
│   $ openclaw --profile jack chat     │   $ openclaw --profile jill chat     │
│   (cursor blinking at prompt)        │   (cursor blinking at prompt)        │
│                                      │                                      │
├──────────────────────────────────────┴──────────────────────────────────────┤
│                                                                             │
│   PANE 3 — Jill's inbox (live tail)                                         │
│                                                                             │
│   $ tail -F /tmp/jill-msgserver.log                                         │
│   [message-server] listening on http://localhost:3941 (dual-stack ::)       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Why this layout matters:** the "money moment" of the demo is when Jack says hi and the audience sees the inbound POST land in real time in pane 3. Without pane 3, the demo loses its visceral kick. Don't skip it.

### Beat-by-beat narration

Total runtime: **~7 minutes** (Beats 1–7) + Q&A.

#### Beat 1 — The problem you're solving (45 sec, no typing yet)

**What's on screen:** three idle panes — both chats showing a blank prompt, pane 3 showing only the message-server startup banner.

**Say:**
> "AI agents are everywhere now — OpenAI, Claude, Hermes, LangChain, OpenClaw, all of them shipping agents that take real actions on behalf of users. But every framework has its own private phone book. If an OpenClaw agent wants to talk to a LangChain agent, somebody has to hand-configure URLs and API keys out of band. There's no shared identity layer, no way to discover who's out there, no way to verify the agent on the other end is who they say they are.
>
> MOI's bet: build that identity layer **once**, on a public blockchain, and let any agent framework plug into it. That's the on-chain agent registry. Today I'm going to show you the first end-to-end proof that it works with a real third-party framework."

#### Beat 2 — What we built (30 sec, no typing yet)

**Say:**
> "We wrote a single OpenClaw skill called `moi-agent-dating`. Three operations: register on the MOI registry, discover other agents, say hi to one of them. About two hundred lines of code total. Once it's installed in an OpenClaw workspace, the OpenClaw agent — the same LLM-driven chat you'd use for anything else — can talk to the MOI registry in plain English.
>
> To prove that, I have two completely independent OpenClaw agents running on this laptop right now: **Jack** on the left, **Jill** on the right. Different profiles, different state directories, different chat sessions. They've never heard of each other."

#### Beat 3 — Jack registers (60 sec)

**Action:** click into **pane 1 (Jack)**. Type:

> please register me on the MOI agent registry

Press Enter. The agent will spend ~25–30 sec thinking + signing + confirming.

**Say while it runs:**
> "Jack just got a natural-language request. Under the hood, OpenClaw's model is reading the request, looking at the skills available to it, deciding `moi-agent-dating` is the right one, and calling its `register` operation. That operation is signing a real transaction with Jack's wallet and submitting it to the MOI devnet — no human in the loop after my one sentence."

**When Jack replies:**
> "Done. **Jack is now `agent_N` on the MOI registry.** Public, on-chain, anyone-can-query identity. Active, with his name, his endpoint URL, and his owner wallet all on chain."

(Point at the `agent_id / status / name / url` block in Jack's reply.)

#### Beat 4 — Jill registers (60 sec)

**Action:** click into **pane 2 (Jill)**. Type:

> register me on the MOI registry too

Press Enter, ~25–30 sec wait.

**Say while it runs:**
> "Same skill, different OpenClaw profile, different chat session. This is exactly what every OpenClaw operator in the world would do — one prompt, one line, and you exist on MOI."

**When Jill replies:**
> "Jill is now `agent_M`. Two agents, no shared config, both on the same public registry."

#### Beat 5 — Jack discovers Jill (60 sec)

**Action:** click back into **pane 1 (Jack)**. Type:

> who else is on the registry?

**Say while it runs:**
> "Jack has no idea Jill exists. He's never been told her URL, her name, anything. But the registry knows about both of them — and Jack can query it through the same skill."

**When the list comes back:**
> "There she is — `agent_M`, named Jill, at `localhost:3941`. Jack just learned about an agent he had no prior knowledge of, purely by reading the chain.
>
> **This is the whole point of the agent registry.** Two agents that have never met, finding each other through a public ledger. Today it's Jack and Jill on one laptop. Tomorrow it's an OpenClaw agent in Bangalore finding a LangChain agent in Berlin without anyone wiring them together by hand."

#### Beat 6 — Jack and Jill have a conversation (the money shot — 90 sec)

**Action:** still in **pane 1 (Jack)**. **Before pressing Enter**, say:

> "Watch the bottom pane."

(All eyes go to pane 3.)

**Type and Enter:**

> say hi to agent_M and ask what she can do

(where `agent_M` is Jill's actual id from Beat 4 — e.g. `agent_13`.)

**Say while it runs:**
> "Jack just resolved Jill's URL from the on-chain profile and is sending a real HTTP POST to her message endpoint. She's running her own LLM behind that endpoint, so this isn't a canned reply — she's actually generating a response in character."

**~3 sec later, pane 3 prints two lines:**
```
[Jill] 2026-06-17T21:18:42.123Z  IN   from=0x000000005188…  text="Hi Jill, what can you do?"
[Jill] 2026-06-17T21:18:43.090Z  OUT  text="Welcome aboard — I can help with on-chain coordination, regis…"
```

**Point at pane 3 and say:**
> "There it is. Jack's message hit Jill's inbox, Jill's server called her own LLM, and you can see the reply going back out. **No URLs exchanged out of band. No API keys shared between them. No coordination layer. Just two agent IDs and the MOI registry — and two independent LLMs talking through it.**"

**When Jack's chat shows Jill's reply, immediately type one follow-up:**

> tell her your name is Jack and ask her a fact about MOI testnet

**Say while it runs:**
> "And because Jill is a real LLM-backed agent, not a stub, Jack can actually have a conversation with her. Watch."

**~3 sec later, Jill replies in pane 1 with something like:**

> "Hey Jack — fun one: MOI testnet is built to let agents coordinate and transact on-chain before mainnet, so it's a great place to experiment safely."

**Land it:**
> "Two autonomous agents — different profiles, different chat sessions, different LLMs in their inboxes — discovered each other through the chain and just held a short conversation. That's what the MOI agent registry is for."

#### Beat 7 — Recap & roadmap (90 sec)

**Say (no panes, just speaker):**
> "Let me recap, because every piece of that flow matters.
>
> One — we took a **third-party agent framework**, OpenClaw, built by Nous Research, not by us. We did not modify OpenClaw. We wrote a skill.
>
> Two — two completely independent OpenClaw agents **registered themselves** with real on-chain identities, no manual configuration.
>
> Three — one agent **discovered** the other purely by reading the chain.
>
> Four — they **exchanged a message** end-to-end with no out-of-band coordination.
>
> Everything you saw is on devnet right now — `agent_N` and `agent_M`, queryable by anyone with a Voyage RPC endpoint.
>
> **What ships next on this track:**
>
> - **Reputation scores** on top of the registry — `agent_X has score Y, signed by N other agents`. Partially in the contract already, we just don't expose it in the demo yet.
> - **Multi-framework** — same skill pattern for LangChain, Hermes, Claude, etc. Any agent on any framework can talk to any other.
> - **Payments rail** — once agents have identity, they can also have wallets they receive payments to for completed work, all under the same on-chain umbrella.
> - **Capability negotiation** — discover agents by what skill they advertise, not just their id.
>
> Questions?"

### Failure modes & live recovery

| Symptom | What to say | What to do |
|---|---|---|
| Jack's chat replies "I need MOI_MNEMONIC" | "One sec — env got dropped, restarting." | `Ctrl+D` to exit chat, then `openclaw --profile jack chat` again. If still broken, `~/MOI-Webinars/session-3/moi-agent-dating/scripts/start-demo.sh` and re-export `OPENAI_API_KEY`. |
| Register hangs > 2 min | "Looks like the uploader died, restarting." | In a spare terminal: `~/MOI-Webinars/session-3/moi-agent-dating/scripts/start-demo.sh`. Retry the prompt. |
| `say hi` prints "fetch failed" | "Message server isn't up, hold on." | Same as above — `start-demo.sh` restarts all three. |
| Pane 3 stays silent during say-hi | "Tailing the wrong log — let me fix the pane." | `tail -F /tmp/jill-msgserver.log` (not jack's). |
| `which openclaw` says not found | "Path got dropped, one sec." | `export PATH="$HOME/.openclaw/bin:$PATH"` in that pane. |

**Worst-case backup:** if the OpenClaw chat refuses to cooperate live, fall back to **direct script invocation**:

```bash
cd ~/MOI-Webinars/session-3/moi-agent-dating/scripts
node --env-file=.env discover.mjs                          # show live on-chain agents
node --env-file=.env register.mjs                          # register a new one
node --env-file=.env say-hi.mjs agent_13 "hello from CLI"  # ping Jill
```

This bypasses OpenClaw entirely and shows the SDK working directly. You lose the "agent framework integration" angle but keep the "on-chain registry works" angle.

---

## Part 4 — Reference

### Every config knob

OpenClaw config lives in `~/.openclaw-<profile>/openclaw.json`. The pieces this demo touches:

| Key | What it does |
|---|---|
| `agents.defaults.model` | LLM the chat uses. Set to `"openai/gpt-5.4-mini"` — cheap + fast + tool-calling capable. |
| `models.providers.openai.apiKey` | OpenAI API key ref. Set as `{source: "env", provider: "default", id: "OPENAI_API_KEY"}` so each pane inherits it from the shell. |
| `env.vars.MOI_MNEMONIC` | 12-word funded devnet mnemonic. Injected into every exec'd subprocess. |
| `env.vars.MOI_DERIVATION_PATH` | BIP-44 path. Both Jack and Jill currently use `m/44'/6174'/7020'/0/0`. |
| `env.vars.UPLOADER_URL` | `http://localhost:7777` — pointing at the local `uploader.mjs` shim. |
| `env.vars.AGENT_NAME` | `"Jack"` / `"Jill"` per profile. Goes into the on-chain agent card. |
| `env.vars.AGENT_URL` | `http://localhost:3940` (Jack) / `http://localhost:3941` (Jill). Lands as the agent's url on chain. |
| `skills.entries.moi-agent-dating.enabled` | `true`. Gates whether OpenClaw exposes the skill to the model. |

> **Gotcha discovered during setup:** `skills.entries.<name>.env` is read for **gating** (`openclaw skills info` reports ✓ Ready when MOI_MNEMONIC is present there) but **does not always inject** into exec subprocesses. The deterministic injection path is `env.vars` at the top level. We set both — `skills.entries.*.env` for the gate, `env.vars` for actual injection.

### Commands cheat sheet

```bash
# === Pre-flight ===
~/MOI-Webinars/session-3/moi-agent-dating/scripts/start-demo.sh

# === Open chats ===
openclaw --profile jack chat
openclaw --profile jill chat

# === Open the live tail ===
tail -F /tmp/jill-msgserver.log

# === Inspect on-chain state without LLM ===
cd ~/.openclaw/workspace/skills/moi-agent-dating/scripts
node --env-file=.env discover.mjs

# === Teardown after the demo ===
pkill -f moi-agent-dating/scripts/uploader.mjs
pkill -f moi-agent-dating/scripts/message-server.mjs

# === Reset OpenClaw config if it gets corrupted ===
openclaw --profile jack doctor --fix
openclaw --profile jill doctor --fix

# === Reinstall the skill into a profile ===
openclaw --profile jack skills install ~/MOI-Webinars/session-3/moi-agent-dating
openclaw --profile jill skills install ~/MOI-Webinars/session-3/moi-agent-dating
```

### On-chain state right now

Last known state of the MOI devnet registry (run `node --env-file=.env discover.mjs` from `scripts/` for the live truth):

| agent_id | name | url | notes |
|---|---|---|---|
| agent_1 | (unnamed) | https://claw-bot.moi.technology | someone else's bot |
| agent_2 | Webinar S3 Demo Agent | https://example.com/webinar-s3-demo-agent | early dummy registration |
| agent_3 | Webinar S3 Live Agent | http://localhost:3939 | earlier dev session |
| agent_4 | Weather Agent | http://localhost:3939 | earlier weather demo |
| agent_5 | Weather Agent | http://localhost:3939 | earlier weather demo |
| agent_6 | OpenClaw Agent | https://example.com/openclaw-agent | early OpenClaw test |
| agent_7 | OpenClaw Agent B | http://localhost:3940 | early OpenClaw test |
| agent_8 | OpenClaw Test Agent | http://localhost:3940 | first successful openclaw register |
| agent_9 | Jack | http://localhost:3940 | direct-script test |
| agent_10 | Jack | http://localhost:3940 | first OpenClaw chat register |
| agent_11 | Jill | http://localhost:3941 | first OpenClaw chat register (Jill) |
| **agent_12** | **Jack** | **http://localhost:3940** | **last rehearsal — yours** |
| **agent_13** | **Jill** | **http://localhost:3941** | **last rehearsal — yours** |

Every demo run mints two new agent_ids. They never expire — the registry just keeps growing.

### Q&A backup

Likely questions and prepared answers:

| Question | Answer |
|---|---|
| **"Is `agents.moi.technology` showing these?"** | "There's indexer lag — the chain has them, the public explorer is a few minutes behind. We can `curl` the Voyage RPC right now to prove the on-chain state if needed (`node --env-file=.env discover.mjs`)." |
| **"What's the LLM doing here? Could we strip it out?"** | "The LLM is just OpenClaw's natural-language interface picking which skill to call. The skill itself — register / discover / say-hi — is deterministic Node code calling `js-moi-agent-registry`. You can run those scripts without OpenClaw at all (see `scripts/.env` + `node --env-file=.env ...`)." |
| **"Are Jack and Jill really separate?"** | "Separate OpenClaw profiles (`~/.openclaw-jack`, `~/.openclaw-jill`), separate workspaces, separate chat state, separate config files. Today they share a backing wallet for demo simplicity; trivial to split with a faucet-funded second derivation path." |
| **"Could this work cross-machine?"** | "Yes. Replace `http://localhost:3941` in Jill's profile with a public URL (ngrok, a deployed agent server, anywhere reachable) and the same flow works across the internet. The registry doesn't care about transport — it just stores the URL." |
| **"What does the on-chain card look like?"** | "Standard A2A agent card — name, description, URL, capabilities, skill list — stored either as a `data:` URI (this demo) or pinned to IPFS (production). Only the `card_uri` lands on chain; the card body sits off chain at that URI." |
| **"How does this differ from ENS or a centralized agent registry?"** | "ENS is for humans naming wallets, not agents naming themselves with capabilities. Centralized agent registries (e.g. AnthropicMCP discovery, OpenAI's GPT Store) live in one company's database — you can't query them from outside, can't audit them, can't migrate. MOI's registry is on a public chain — any framework can write to it, any client can read it, no gatekeeper." |
| **"Why OpenClaw specifically? Why not just demo your own SDK?"** | "Because the SDK-only demo proves we can do it. The OpenClaw demo proves a real, externally-maintained agent framework can do it. That's the deliverable: agnostic, third-party, plug-and-play." |
| **"What happens if the wallet is unfunded?"** | "Reads (`getAgentCount`, `getAllAgentIds`, `getAgentProfile`) require the wallet to exist on chain (the SDK constructs interaction objects). Writes (`createAgent`) require gas. So a fresh wallet must be funded via the devnet faucet at <https://voyage.moi.technology> before either works. For this demo we side-step funding by reusing one funded wallet for both agents." |
