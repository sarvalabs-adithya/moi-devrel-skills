# MOI Builders Webinar Series (Sessions 1-6): Research Note

> **What this file is.** A research note on how the MOI Builders webinar sessions 1 to 6 (the "early" series, before the newer format used from session 7) were built and run: for each session the purpose, the live demo steps, the inputs, the traps, and the shared patterns across sessions. Claude (an AI research assistant) compiled it from Adithya's work history to help design the Claude skills now in `skills/moi/`. This file does not say which skills it fed.
>
> **When it was written.** September and October 2026 (this file gives no date of its own). It describes the repo and devnet as they stood then; see "What may break now" near the end.
>
> **Who "I" and "the user" are.** "I", where it appears, is the research assistant. "The user" is Adithya (DevRel at MOI), who built and presented every session.
>
> **Evidence key.** "observed" means the fact was seen in one of the source files listed under "Sources read". "inferred" means the research assistant's reasoning, not confirmed by a source. A statement with neither tag comes from the sources read. "Unknown" and "unverified" mean nobody checked.
>
> **Paths and citations.** Paths starting `~/` or `WT/` are on Adithya's Mac. The session code is in https://github.com/moi-foundation/MOI-Webinars. Session transcripts are not in the repo. This file has no REQ cites; other research notes in this folder cite `REQ:<n>`, which points to a request log kept on Adithya's Mac (not in this repo).
>
> **People.**
> - Adithya: DevRel at MOI; the only real person named in this file. The notes call him the sole facilitator ("observed").
> - Jack and Jill (two demo agents), Alice and Bob (two demo wallets) and Pip (the Session 6 demo agent) are characters in the demos, not people.
> - Nobody else is named here. For the reviewers and teammates around the later sessions (Rahul and others), see `webinars-mature.md`.
>
> **How the file is laid out.** One "Process" section per session (1 to 6), then the shared skeleton (folders, `.env`, versions, code patterns), attendee prerequisites, what may break now, the stated plan, reusable assets, house style, accumulated traps, proposals for a skill, open questions, known inconsistencies, and a glossary of jargon at the end.

## Sources read

- `~/MOI-Webinars/OVERVIEW.md`: comprehensive repo orientation and Session 3 live demo flow
- `~/MOI-Webinars/README.md`: quick-start table for all sessions
- `~/MOI-Webinars/webinar-code-reference.md`: code walkthrough for Sessions 1-2, 4-5
- `~/MOI-Webinars/webinar-vibecode-plans.md`: alternative "skills-only" format (LLM vibecoding)
- `~/MOI-Webinars/session-1/README.md`, `package.json`: install, CocoLab + SDK flow, bounty framing
- `~/MOI-Webinars/session-2/README.md`, `package.json`: MAS0 + TaxToken flow, bounty form
- `~/MOI-Webinars/session-3/README.md`, `moi-agent-dating/SKILL.md`, `scripts/package.json`: OpenClaw setup, three operations (register/discover/say-hi)
- `~/MOI-Webinars/session-4/README.md`, `package.json`: two-wallet swap, setup/CLI/UI tiers, patch-package gotcha
- `~/MOI-Webinars/session-5/README.md`, `package.json`: NFT collection, Coco + SDK + UI, vibecode prompts
- `~/MOI-Webinars/session-6/README.md`, `package.json`: context inheritance, multi-agent budget enforcement
- `~/moi-agent-budget/README.md`, `WEBINAR-PLAN.md`, `TEACHING-GUIDE.md`: session 6 deep-dive (same content as session-6 README but with teaching notes)

All paths above are on Adithya's Mac. The `MOI-Webinars` files are the repo https://github.com/moi-foundation/MOI-Webinars (same relative paths in his checkout; which branch carries each file was not checked). `moi-agent-budget` is a separate folder on his Mac; these notes do not record whether it is published.

---

## Process: Session 1: CocoLab + SDK fundamentals

**Purpose:** Teach Coco basics (state, endpoints, message context) inside CocoLab REPL, then replicate the same logic from JavaScript using the SDK. Establish the pattern: write contract, compile, deploy, call.

In plain terms: first the audience types a small contract into CocoLab and watches it work, then the same contract is deployed and called from a JavaScript program using the MOI SDK.

**Trigger/cadence:** Live webinar, ~45 min. One-time session; served as foundation for all subsequent sessions.

**Who does it:** Adithya (observed as sole facilitator across all demos). Contract written live in CocoLab; SDK scripts pre-written but executed live.

**Inputs needed before starting:**
- Coco toolchain installed (0.7.0 verified in compile config)
- Node.js 20+ with npm
- One funded MOI devnet wallet (12-word mnemonic from Voyage faucet)
- Derivation path `m/44'/6174'/7020'/0/0` (faucet default, matches all session examples)

**Steps in order:**

1. **CocoLab fundamentals (Demo 1: Flipper)**
   - Open `session-1/flipper/` directory
   - Run `coco lab init` to start REPL
   - REPL presents a Coco prompt; user manually types `deploy`, `Flip()`, `Mode()` to demonstrate state toggle and read
   - Exit CocoLab

2. **CocoLab actor-context variant (Demo 2: ContextFlipper)**
   - Open `session-1/context-flipper/` directory
   - Run `coco lab init` again
   - Same three operations, but each actor (participant) sees its own bool value, not shared
   - This introduces Coco's `state actor` (vs `state logic`) and per-sender isolation
   - In plain terms: actor state is storage kept separately for each participant; logic state is one shared copy that everyone sees

3. **SDK deployment (Demo 3a)**
   - Copy `.env.example` to `.env`, paste funded mnemonic
   - Run `node sdk/deploy.js`
   - Script loads wallet from mnemonic, creates `LogicFactory` with the `flipper.json` manifest, calls `factory.deploy('Init').send()`, prints interaction hash + assigned logic_id
   - **Output:** Logic ID (copied into .env as `LOGIC_ID`)

4. **SDK invocation (Demo 3b)**
   - Run `node sdk/flip.js`
   - Script loads wallet, gets logic driver, calls `Flip().send()`, waits for result
   - **Output:** "Flipped" confirmation

5. **SDK read-only call (Demo 3c)**
   - Run `node sdk/mode.js`
   - Script calls `Get().call()` (read-only), prints the bool value
   - **Output:** `value: true` or `value: false`

6. **Sneak peek of Session 2 (Demo 3d)**
   - Run `node sdk/asset.js`
   - Creates a vanilla MAS0 token named "WEBINAR", mints some to manager
   - **Output:** Asset ID (teases next session)

**Deliverables and where they end up:**
- Logic ID (on-chain, searchable on Voyage explorer; also printed to console)
- Interaction hashes (on-chain at Voyage)
- Terminal output logs (local, ephemeral)

**Accounts and tools involved:**
- **Accounts:** One wallet (mnemonic from `.env`); no new accounts created
- **Tools:** VoyageProvider (devnet), Wallet.fromMnemonic(), LogicFactory, getLogicDriver
- **Keys/logins needed:** MOI_MNEMONIC (stored in `.env`, gitignored)

**Quality rules and house style:**
- Compiled manifests (`.json`) are checked in; recompilation optional after editing `.coco`
- Derivation path is always `m/44'/6174'/7020'/0/0` unless overridden
- Fuel limits capped to wallet balance (observed in later sessions; not explicit here but established practice)
- Error handling: prints user-friendly messages on missing LOGIC_ID or failed interactions
- Comments in code explain the diff between logic-state and actor-state, and between `.send()` (mutable) and `.call()` (read-only)

**Traps and things that failed silently:**
- Pre-compiled manifests were checked in late in development; ensure they match the checked-in `.coco` source or recompile
- Derivation path can be wrong if wallet was funded at a non-faucet path; `.env.example` includes an override comment
- Logic ID must be saved to `.env` manually after deploy; no auto-population
- CocoLab REPL is an interactive session; the script must walk through it live (not recorded in the `.coco` file)

**Duration:** ~45 min live (CocoLab ~15 min, SDK demos ~20 min, Q&A ~10 min)

**Open questions:**
- Were any logic IDs reused across multiple demo runs, or is each session a fresh deploy?
- How much of the CocoLab walk is narrated vs. silent exploration?

---

## Process: Session 2: Native Assets (MAS0 + TaxToken)

**Purpose:** Show MOI's dual asset model: SDK-native MAS0 tokens and custom logic-backed MASX assets (fee-on-transfer). Bounty drives completion.

**Trigger/cadence:** Follows Session 1. ~45 min. One-time webinar; bounty form collects submissions afterward (Google Form: https://forms.gle/NNK58E3vAyF6EYw9A).

**Who does it:** Adithya. Scripts pre-written; Coco contract pre-compiled (manifest checked in).

**Inputs needed before starting:**
- Node.js 20+, npm
- One funded devnet wallet
- Coco toolchain 0.7.0 (only if recompiling; pre-compiled `taxtoken.json` is checked in)

**Steps in order:**

1. **Session 2 setup**
   - Navigate to `session-2/`
   - Copy `.env.example` to `.env`, paste mnemonic
   - Run `npm install`

2. **Demo 1: Native MAS0 asset**
   - Run `node sdk/asset.js`
   - Script calls `MAS0AssetLogic.create(wallet, 'WEBINAR', 1_000_000, address, true)`
   - Then mints 100,000 of that asset to the manager
   - **Output:** Asset ID, manager address, interaction hashes

3. **Demo 2: Custom TaxToken asset**
   - Optional: recompile if `.coco` was edited: `cd coco && coco compile && coco manifest convert taxtoken.yaml -f json -o taxtoken.json && cd ..`
   - Run `node sdk/tax-deploy.js`
   - Script calls `AssetFactory.create(wallet, 'TaxToken', 1_000_000, manager, true, taxManifest, 'Init', treasury_addr, tax_bps, initial_supply)`
   - Treasury collects 5% (500 basis points) of every transfer
   - **Output:** Asset ID

4. **Bounty submission (offline)**
   - Fill Google Form: email, wallet address, MAS0 Asset ID, MASX Asset ID
   - Verify on https://voyage.moi.technology that both asset-creation interactions landed

**Deliverables and where they end up:**
- MAS0 Asset ID (on-chain)
- MASX (logic-backed TaxToken) Asset ID (on-chain)
- Google Form submission (external, timestamp recorded)

**Accounts and tools involved:**
- **Accounts:** One wallet
- **Tools:** VoyageProvider, Wallet.fromMnemonic, MAS0AssetLogic, AssetFactory, manifest loader
- **Keys/logins:** MOI_MNEMONIC (`.env`)

**Quality rules and house style:**
- Manifests in JSON format (per `coco.nut` `output` field)
- Asset supply as plain number (not bigint) to avoid signing issues
- Tax rate in basis points (500 = 5%)
- All assets deployed on devnet
- README includes troubleshooting for "account not found" (must fund wallet first) and derivation path variations

**Traps and things that failed silently:**
- TaxToken recompilation is optional but manifest must match source; if the `.coco` was edited, a stale `.json` will cause wrong behavior
- BigInt in `.send()` payload breaks signing in devnet (observed but not deeply documented; webinar-code-reference notes plain numbers only)
- Asset creation succeeds with a zero-amount initial mint, but minting to manager requires positive amount
- Google Form submissions are one-way; if an asset ID is wrong, no easy way to resubmit

**Duration:** ~30 min live (Demos 1-2 ~10 min, Q&A + submission help ~20 min)

**Open questions:**
- Were multiple Demo 1 / Demo 2 runs done, or was it one shot per webinar? (inferred: one shot; asset IDs are unique per run)
- How is the bounty form monitored and verified on-chain?

---

## Process: Session 3: On-chain Agent Registry × OpenClaw

**Purpose:** Prove that a real, third-party agent framework (OpenClaw, by Nous Research) can integrate with MOI's on-chain agent registry without modification. Two agents (Jack and Jill) register, discover each other, and message live.

**Trigger/cadence:** Follows Session 2. Headline demo of the series. ~50-60 min live, with pre-recorded fallback. Two bounty tracks (participation + open/competitive).

**Who does it:** Adithya. OpenClaw chat is interactive; SDK scripts pre-written; background HTTP services pre-configured.

**Inputs needed before starting:**
- Node.js 20+, npm
- OpenClaw 1.0.0+ (two separate profiles: `~/.openclaw-jack/` and `~/.openclaw-jill/`)
- Two funded devnet wallets (one mnemonic can be shared between Jack and Jill for simplicity)
- OpenAI API key (exported to shell, or in `openclaw.json`)
- MOI_MNEMONIC env var in each profile's `openclaw.json` under `env.vars.MOI_MNEMONIC` and `skills.entries.moi-agent-dating.env`

**Pre-flight steps (5 min before going live):**
1. Confirm `OPENAI_API_KEY` is exported: `echo $OPENAI_API_KEY | head -c 20`
2. Confirm both profiles see the skill: `openclaw --profile jack skills info moi-agent-dating | grep Ready` (expect ✓)
3. Start all three background services: `~/MOI-Webinars/session-3/moi-agent-dating/scripts/start-demo.sh` (expect three LISTEN lines)
4. Smoke test on-chain registry: `cd ~/.openclaw/workspace-jack/skills/moi-agent-dating/scripts && node --env-file=.env discover.mjs | head -5` (expect agent list)

**Steps in order (live demo beat-by-beat):**

1. **Problem statement (45 sec, narration only)**
   - Three idle panes on screen (two OpenClaw chats + tail of message-server log)
   - Adithya explains: agents are everywhere, but each framework has private phone book; MOI's registry is the proof of concept

2. **What we built (30 sec, narration)**
   - Introduce OpenClaw skill (`moi-agent-dating`): register, discover, say hi
   - Announce Jack and Jill: two independent profiles, never heard of each other

3. **Jack registers (60 sec)**
   - **Pane 1 (Jack's chat):** Type `please register me on the MOI agent registry`
   - OpenClaw's LLM reads the request, picks the skill, calls `exec node register.mjs`
   - Script builds `AgentRegistry` from `js-moi-agent-registry` SDK, calls `registry.createAgent(spec, card)`, prints assigned `agent_id` and on-chain profile
   - **Output in chat:** Agent ID (e.g. `agent_12`), status, name, URL, wallet
   - **Narration:** "Jack is now on the on-chain registry, public and queryable"

4. **Jill registers (60 sec)**
   - **Pane 2 (Jill's chat):** Type `register me on the MOI registry too`
   - Same flow, different profile
   - **Output:** Jill's assigned ID (e.g. `agent_13`)
   - **Narration:** "Two agents, no shared config, same public registry"

5. **Jack discovers Jill (60 sec)**
   - **Pane 1:** Type `who else is on the registry?`
   - Script calls `registry.getAllAgentIds()`, then per-agent `getAgentProfile(id)`, prints list
   - **Output:** List including Jill's ID, name, URL
   - **Narration:** "Jack has no idea Jill exists, but the registry knows: two agents finding each other through a public ledger"

6. **Jack and Jill message (90 sec, the money shot)**
   - **Pane 1:** Type `say hi to agent_M and ask what she can do` (where `agent_M` is Jill's ID from step 4)
   - Before typing, say "watch the bottom pane"
   - Script calls `registry.getAgentProfile(agent_M)`, extracts URL, does `HTTP POST {url}/message {from, text}`
   - Jill's `message-server.mjs` receives the POST, calls `completionClient.create()` with LLM prompt, generates reply
   - **Pane 3 (Jill's inbox tail):** Two lines appear in real time:
     - `[Jill] ...IN   from=0x000…  text="Hi Jill, what can you do?"`
     - `[Jill] ...OUT  text="Welcome aboard: I can help with on-chain coordination…"`
   - **Pane 1:** Jack receives Jill's reply
   - **Narration:** "Jack's message hit Jill's inbox, she generated a real LLM reply, no coordination layer. Two agents talking through the MOI registry."

7. **Follow-up exchange (optional)**
   - **Pane 1:** Type `tell her your name is Jack and ask her a fact about MOI testnet`
   - Jill replies conversationally
   - Drives home: this is a real agent-to-agent conversation, not canned replies

8. **Recap and roadmap (90 sec)**
   - No panes; speaker only
   - Recap the four pieces: third-party framework (OpenClaw unmodified), independent registration, discovery, end-to-end messaging
   - Roadmap: reputation scores, multi-framework (LangChain, Claude, Hermes), payments rail, capability negotiation

**Deliverables and where they end up:**
- Two live `agent_id` registrations (on-chain; searchable via `discover.mjs` or https://voyage.moi.technology)
- Message transcript (in pane 3 logs, ephemeral)
- Form submission (Bounty 1): agent_id, wallet, tx hash → Google Form
- GitHub repo or deployed agent (Bounty 2): for the open 500-MOI bounty

**Accounts and tools involved:**
- **Accounts:** One shared devnet wallet (optional: two separate wallets, one per agent)
- **Tools:** 
  - OpenClaw chat interface (LLM model: `openai/gpt-4-mini` or `gpt-5.4-mini` observed)
  - `js-moi-agent-registry` SDK (0.1.0 pinned in scripts/package.json)
  - `js-moi-sdk` (0.7.0-rc16 pinned)
  - OpenAI Completions API (for message-server LLM replies)
  - VoyageProvider (devnet)
- **Keys/logins:** 
  - OPENAI_API_KEY (export to shell OR set in openclaw.json)
  - MOI_MNEMONIC (in openclaw.json per-profile)

**Environment variables (per-profile in `~/.openclaw-{jack,jill}/openclaw.json`):**
- `MOI_MNEMONIC`: 12-word devnet mnemonic
- `MOI_DERIVATION_PATH`: `m/44'/6174'/7020'/0/0` (default)
- `UPLOADER_URL`: `http://localhost:7777`
- `AGENT_NAME`: "Jack" or "Jill"
- `AGENT_URL`: `http://localhost:3940` (Jack) or `http://localhost:3941` (Jill)

**Quality rules and house style:**
- OpenClaw config uses JSON5 (unquoted keys, trailing commas, `//` comments allowed)
- Skill SKILL.md has YAML frontmatter declaring `requires.bins: ["node"]` and `requires.env: ["MOI_MNEMONIC"]`
- Skill operations trigger on natural language: "register" → `register.mjs`, "discover" → `discover.mjs`, "say hi" → `say-hi.mjs`
- Message servers (uploader, Jack's inbox, Jill's inbox) bind on dual-stack `::` (not just 127.0.0.1) for Node 18+ fetch compatibility
- All logs to `/tmp/` (uploader.log, jack-msgserver.log, jill-msgserver.log)
- Fallback to echo replies if OPENAI_API_KEY is not set (demo still works offline)
- Agent cards uploaded as `data:` URIs (base64 JSON) via uploader.mjs; production would use IPFS

**Traps and things that failed silently:**
- OpenClaw skill env vars must be set in BOTH `env.vars` (for injection) AND `skills.entries.*.env` (for the ✓ Ready gate); discovered during setup
- Dual-stack binding (`::`) is required; single-stack `127.0.0.1` fails from Node's `fetch` on some systems
- Message-server OPENAI_API_KEY is read from the shell env, not from scripts/.env; must be exported before `start-demo.sh`
- If the uploader dies mid-demo, register hangs indefinitely (>2 min); recovery: restart uploader via `start-demo.sh`
- Agent card URIs must return valid JSON; if uploader crashes, the profile read fails silently on-chain
- Indexer lag: agent IDs land on-chain immediately but explorer (voyage.moi.technology) lags a few minutes
- OpenClaw chat can misinterpret prompts; best wording: "please register me on the MOI agent registry" or "register me on the MOI registry too" (not "publish", not "deploy")

**Duration:** ~50-60 min live (pre-flight 5 min, beats 1-8 ~50 min, Q&A + bounty pitch ~5 min)

**Failure recovery modes (documented in OVERVIEW.md):**
- Jack's chat replies "I need MOI_MNEMONIC": env got dropped; restart: `Ctrl+D` to exit chat, then `openclaw --profile jack chat` again
- Register hangs >2 min: uploader died; restart: `./start-demo.sh`
- `say hi` prints "fetch failed": message server isn't up; restart: `./start-demo.sh`
- Pane 3 stays silent during say-hi: wrong log file; fix: `tail -F /tmp/jill-msgserver.log`
- `which openclaw` not found: PATH got dropped; fix: `export PATH="$HOME/.openclaw/bin:$PATH"`

**Worst-case fallback (if OpenClaw chat fails):**
- Run scripts directly: `node discover.mjs`, `node register.mjs`, `node say-hi.mjs <id> "<msg>"`
- Loses the "agent framework integration" story but keeps "on-chain registry works"

**Open questions:**
- How often were the Jack and Jill profiles reset between rehearsals? (inferred: each rehearsal likely got fresh agent_ids; the registry never expires agents)
- Did the OPENAI_API_KEY ever get committed to the repo or baked into openclaw.json, or was it always shell-exported? (inferred: always shell-exported, as README emphasizes "do not put API keys in the repo")

---

## Process: Session 4: Account-to-Account Swap (Lockup + Release)

**Purpose:** Teach MAS0 native `Lockup` and `Release` operations for atomic-ish (trust-based, not chain-enforced) two-wallet swaps. Two tiers: CLI step-by-step and Vite UI with live on-chain state checks.

**Trigger/cadence:** Follows Sessions 1-3. ~50 min live. Bounty form collects submissions (Google Form: https://forms.gle/mM9Rf6dqxZQd1fuz6).

**Who does it:** Adithya. Scripts pre-written; UI pre-built. Live narration; UI clicks during demo.

**Inputs needed before starting:**
- Node.js 20+, npm
- **Two separate funded devnet wallets** (different mnemonics)
- `.env` with `VITE_ALICE_MNEMONIC` and `VITE_BOB_MNEMONIC`

**Steps in order:**

1. **Setup (one-time, before webinar)**
   - `npm install` (includes postinstall: `patch-package` to fix SDK's ESM build)
   - `npm run setup`
   - Script deploys TKA (Alice manager) and TKB (Bob manager), 1M supply each
   - Mints 500k TKA to Alice, 500k TKB to Bob
   - Writes `VITE_TKA_ASSET_ID` and `VITE_TKB_ASSET_ID` to `.env`
   - **Output:** Asset IDs, interaction hashes, starting balances

2. **Demo flow: CLI (step-by-step, ~20 min)**
   - Show starting balances: `node extras/swap-cli.js balances`
   - **Step 1:** Alice locks 100 TKA for Bob: `node extras/swap-cli.js lock-alice`
     - Calls `MAS0AssetLogic(tka, alice).lockup(bob_address, 100)`
     - Prints updated balances; Bob's balance unchanged (locked, not transferred)
   - **Step 2:** Bob locks 90 TKB for Alice: `node extras/swap-cli.js lock-bob`
     - Calls `MAS0AssetLogic(tkb, bob).lockup(alice_address, 90)`
     - Prints balances; Alice can now see her 90 TKB locked for her
   - **Step 3:** Alice claims her 90 TKB: `node extras/swap-cli.js claim-alice`
     - Calls `MAS0AssetLogic(tkb, alice).release(bob_address, alice_address, 90)`
     - Alice's TKB balance increases; her TKA balance still shows 500k (locked)
   - **Step 4:** Bob claims his 100 TKA: `node extras/swap-cli.js claim-bob`
     - Calls `MAS0AssetLogic(tka, bob).release(alice_address, bob_address, 100)`
     - Bob's TKA balance increases; Alice's TKA balance decreases
   - **Narration:** "Alice started with 100 TKA, ends with 90 TKB; Bob started with 90 TKB, ends with 100 TKA. No pool, no escrow contract, just two irrevocable offers and mutual claims."

3. **Demo flow: Vite UI (interactive, ~20 min)**
   - `npm run dev` (opens http://localhost:5174)
   - **Scenario:** Fresh swap (or rebalance first: `node extras/rebalance.js`)
   - **As Alice:**
     - Paste her mnemonic in "Connect" field
     - Verify balances load (500k TKA, 0 TKB)
     - Select TKA as "send", amount 100
     - Paste Bob's address
     - Click **Lock** button
     - Confirm tx hash in console; balances update (500k TKA, but now "locked for Bob")
     - **Claim button is disabled** with message: "Waiting for counterparty to lock 90 TKB…"
   - **Disconnect, connect as Bob:**
     - Paste Bob's mnemonic
     - Click **⇅ Flip** to swap sides (send = TKB)
     - Paste Alice's address
     - **Claim button is already enabled** (UI polled `moi.Lockups(alice)` on-chain, found her lock for Bob)
     - Click **Lock** to lock his 90 TKB for Alice
     - Click **Claim** to claim the 100 TKA Alice locked
     - Balances update
   - **Disconnect, connect as Alice:**
     - **Claim button is now enabled**
     - Click **Claim** to claim the 90 TKB
     - Swap complete; verify balances: Alice has 90 TKB, Bob has 100 TKA
   - **On-chain verification:** Open https://voyage.moi.technology, search both wallets, see Lockup/Release interaction hashes

**Deliverables and where they end up:**
- TKA Asset ID (on-chain)
- TKB Asset ID (on-chain)
- Four Lockup/Release interaction hashes (on-chain)
- Bounty form: email, wallet, asset IDs, one tx hash

**Accounts and tools involved:**
- **Accounts:** Two wallets (Alice and Bob), derived from separate mnemonics
- **Tools:** VoyageProvider, Wallet.fromMnemonic, MAS0AssetLogic (lockup/release/transfer), RPC `moi.Lockups` query
- **Keys/logins:** `VITE_ALICE_MNEMONIC`, `VITE_BOB_MNEMONIC` (`.env`)
- **UI tech:** Vite (build), ES modules, browser-safe swap.js logic (no dotenv, no process.env)

**Quality rules and house style:**
- Amounts are plain numbers (not bigint) to avoid signing issues
- Derivation paths default to `m/44'/6174'/7020'/0/0` for both wallets
- Fuel limits capped to each wallet's KMOI balance (via `cappedFuel()` helper)
- UI polls `moi.Lockups` every ~4 seconds to gate the Claim button
- UI shows per-step status: "Locking…", "Locked", "Claim available", "Claiming…", "Complete"
- Swap rate is display-only (not enforced on-chain): 1 TKA = 0.9 TKB in the demo
- `.env` is gitignored; `.squad.json` local state files are gitignored too

**Traps and things that failed silently:**
- `patch-package` must run (postinstall script) to fix SDK's ESM build; if UI is broken, re-run: `npm install`
- MAS0's `release()` has no on-chain guard, so calling it when nothing is locked "succeeds" but moves zero funds. The UI's `claim()` checks the balance delta and reports "nothing to claim yet" unless funds actually moved.
- `moi.Lockups` is a raw JSON-RPC method, not wrapped by SDK. Provider must call `provider.execute('moi.Lockups', ...)` directly.
- Swaps are trust-based, not atomic: nothing on-chain forces Bob to lock his side in return if Alice locks first. True atomicity needs an escrow contract.
- Balances are stale if the UI is open during a simultaneous on-chain transaction; no live refresh hook (inferred).
- BigInt in API payloads breaks signing; use plain numbers.

**Duration:** ~50 min live (setup 5 min, CLI demo ~20 min, UI demo ~20 min, Q&A ~5 min)

**Open questions:**
- How often do attendees get stuck on the `patch-package` step? (inferred: common enough to document in README)
- Did attendees use the rebalance script between rehearsals to reset to the 500k/0 baseline, or was it one-shot per run?

---

## Process: Session 5: NFT Marketplace (MAS1 mint + transfer + UI)

**Purpose:** Teach NFT minting (MAS1 with metadata) in Coco, SDK deployment and transfer, and a web UI that drives the flow. All vibecoded live (alternative mode, not read-only).

**Trigger/cadence:** Follows Sessions 1-4. ~45 min live. Bounty form (Google Form: https://forms.gle/PaUqk13GrbULYS928): baseline (500 KMOI) for mint + transfer, bonus for extras (images, UI, sell flow).

**Who does it:** Adithya (in vibecode mode: Claude Code agent writes contract and scripts from prompts, Adithya narrates). In traditional mode: scripts pre-written, executed live.

**Inputs needed before starting:**
- Node.js 20+, npm
- Coco toolchain 0.8.2+
- One funded devnet wallet
- Optional: Claude Code (for vibecode variant)

**Steps in order (traditional mode):**

1. **Setup**
   - `npm install` (root + ui/)
   - `cp .env.example .env`, paste mnemonic
   - Optional: verify skills: `node js-moi-sdk-skills/scripts/verify-sdk.cjs ./node_modules/js-moi-sdk` (expect 55/55)

2. **Coco compilation (optional, if `.coco` was edited)**
   - `cd coco && coco compile`
   - Pre-compiled `mas1.json` is checked in, so this step is often skipped

3. **CLI: mint (Demo 1)**
   - `npm run mint`
   - Script calls `AssetFactory.create(wallet, "ART", 10_000, owner, true, manifest, "Init")`
   - Runs `Init()` endpoint during deploy
   - Calls `driver.routines.Mint(owner, name, uri)` to mint token #0 with metadata
   - Writes `sdk/deployment.json` with `{ asset_id, token_id, owner }`
   - **Output:** Asset ID, Token ID, interaction hashes

4. **CLI: transfer (Demo 2)**
   - `npm run transfer -- 0xRECIPIENT_ADDRESS`
   - Script reads `deployment.json`, calls `MAS1AssetLogic(asset_id, wallet).transfer(tokenId, recipient)`
   - Verifies ownership moved via `getTDU()` (get token distributed units, inferred)
   - **Output:** Interaction hash, new owner

5. **Web UI (Demo 3)**
   - `npm run dev`
   - Opens http://localhost:3000
   - Express server in `ui/server.js` exposes:
     - `GET /api/status`: reads `sdk/deployment.json`
     - `POST /api/mint`: runs `sdk/mint.js`
     - `POST /api/transfer`: runs `sdk/transfer.js`
   - Browser UI shows:
     - **Mint NFT** button: creates asset, mints token #0
     - **Transfer NFT** form: input recipient address, click transfer
   - Each button click shells out to the SDK scripts, shows status (loading, success, error)

**Deliverables and where they end up:**
- MAS1 Asset ID (on-chain)
- Token ID (in deployment.json, on-chain via transfer)
- Interaction hashes (on-chain; searchable on Voyage)
- Bounty form: repo link, token ID or tx hash

**Accounts and tools involved:**
- **Accounts:** One wallet
- **Tools:** VoyageProvider, Wallet.fromMnemonic, AssetFactory (deploy + mint), MAS1AssetLogic (transfer), Vite UI
- **Keys/logins:** MOI_MNEMONIC (`.env`)

**Quality rules and house style:**
- Manifests in JSON format (Coco 0.8.2 default)
- Token IDs are U64, starting at 0
- Metadata stored as static token metadata (name, image_uri)
- Mint is manager-gated (only owner can mint in the demo)
- Transfer validation: recipient must exist on devnet (no bouncing checks)
- Fuel limits capped to KMOI balance (via `cappedFuel()` helper)
- Receipts checked for status before confirming success
- UI stateless (no Redux, no complex state machine; just button states: default, loading, done, error)

**Traps and things that failed silently:**
- MAS1 is logic-backed (MASX), not protocol-native; deploy via AssetFactory, not MAS1AssetLogic.create
- Metadata is stored as static (immutable); dynamic metadata would require a different pattern
- Transfer requires recipient to exist on devnet; no validity check in the script (fails at submit if recipient is invalid)
- Fuel capping to KMOI balance must happen on every call; if a script runs low on gas, later transfers fail
- The UI server must have read access to `sdk/deployment.json`; if it's deleted, mint must run again

**Duration:** ~45 min live (setup 5 min, mint 10 min, transfer 10 min, UI 15 min, Q&A 5 min)

**Vibecode variant (alternative):**
- Same overall flow, but contract + scripts are written live by Claude from prompts
- Prompts (from webinar-vibecode-plans.md):
  1. "Read coco-skills. Write a MAS1 NFT collection: manager-gated Mint with name + image_uri metadata, Transfer by token_id, Init that zeroes a token counter. Compile it."
  2. "With js-moi-sdk, deploy the manifest via AssetFactory (Init at create), mint one NFT to my wallet, print asset_id and token_id. Cap fuel to KMOI balance."
  3. "Add a transfer script: read the saved deployment state, transfer token #0 to a recipient address, verify ownership moved via getTDU."
  4. "Add a minimal Express UI: Mint button and Transfer form that shell out to those SDK scripts."
- Takes ~60 min (slower than pre-written scripts due to Claude's thinking time and prompt refinement)

**Open questions:**
- How is the bounty "bonus" tier judged? (inferred: visually, by judges; not automatic)
- Did attendees commonly add image uploads, or did most stop at baseline?

---

## Process: Session 6: Context Inheritance (One Wallet, Many Agents)

**Purpose:** Teach MOI's context inheritance: giving multiple AI agents their own derived sub-account identities and enforcing per-agent budgets on-chain. One primary wallet → many sub-accounts with independent state and enforced spend caps.

**Trigger/cadence:** Follows Sessions 1-5. ~60 min live. Two bounty tracks: completion (token) + bonus (500 MOI + $15 cash).

**Who does it:** Adithya. Squad manager (squad.js) and Pip agent (agent.js) pre-written. Live provisioning and spend attempts.

**Inputs needed before starting:**
- Node.js 20+, npm
- One funded devnet wallet
- Coco toolchain 0.8.0+ (only if recompiling; `agentbudget.json` is checked in)
- Anthropic API key (optional, for `run` command; `spend` works without it)

**Steps in order:**

1. **Setup**
   - `npm install`
   - `cp .env.example .env`, paste mnemonic and (optional) Anthropic API key
   - Note: `.env` values must be comment-free (inline `#` is not stripped)

2. **Deploy the logic (one-time)**
   - `npm run deploy`
   - Script calls `LogicFactory.deploy('Init')` for `AgentBudget` logic
   - Prints logic ID
   - Paste into `.env` as `LOGIC_ID`

3. **Provision agents**
   - `node squad.js provision trader 500`
   - Script:
     - Derives sub-account address = primary's first 28 bytes + 4-byte index (for `trader`)
     - Sends `AccountInherit` tx: create sub-account, link context to `AgentBudget` logic, seed with 1000 KMOI
     - Calls `SetBudget(500)` to write allowance into that agent's actor state
     - **Output:** Agent address, provision tx hash, budget confirmation
   - Repeat for other agents: `node squad.js provision scraper 200`

4. **Agents act, and can't overspend**
   - `node squad.js run trader "look up who won the last F1 race, then record a spend for the lookup"`
     - If `ANTHROPIC_API_KEY` is set: Claude agent does web_search, returns result, calls `RecordSpend(cost)` on-chain
     - **Output:** Agent result, spend amount, updated balance
   - `node squad.js spend trader 500 "bust the cap"`
     - Script calls `RecordSpend(500)` where agent only has 500 budget
     - **Expected:** Revert on-chain with "exceeds remaining budget" (the payoff: the contract enforces the cap)
   - `node squad.js report`
     - Reads each agent's actor state: budget, spent, remaining
     - **Output:** Table of agents with their ledgers (all read from chain)

5. **Optional: Pip chat demo**
   - `node agent.js`
   - Pip discovers itself: `who are you?` → compute sub-account addresses, check each with `getContextInfo()`
   - `provision yourself` → sends `AccountInherit` tx, confirms link on-chain
   - `who are you now?` → same math, now finds itself (**the aha moment**)
   - `inspect 0x...` → reads raw `getContextInfo`, prints `inherited_account` field

6. **Bounty submission (offline)**
   - Repo link with logic id in README
   - Agent address from provision output
   - Provision tx hash (for on-chain verification on Voyage)
   - Report output (showing agent in ledger)

**Deliverables and where they end up:**
- Logic ID (on-chain; in `.env` and repo README)
- Sub-account addresses (derived; printed on provision)
- `AccountInherit` tx hashes (on-chain; searchable on Voyage)
- `SetBudget` and `RecordSpend` tx hashes (on-chain)
- Agent ledger data (on-chain, in agent's actor state)
- Bounty submission (repo link + context)

**Accounts and tools involved:**
- **Accounts:** One primary wallet + many sub-accounts (derived per agent, all signing with same mnemonic)
- **Tools:** 
  - VoyageProvider, Wallet.fromMnemonic
  - LogicFactory, getLogicDriver
  - AccountInherit (create + link + fund in one tx)
  - `getContextInfo()` RPC call (check if sub-account is linked to a logic)
  - `Anthropic SDK` (optional, for real-agent `run` command)
- **Keys/logins:** USER_MNEMONIC, ANTHROPIC_API_KEY (optional, `.env`)

**Context inheritance mechanics (the core concept):**
- **Primary account:** `0x5f3a…e0d9` (derived from mnemonic path `m/44'/6174'/7020'/0/0`)
- **Sub-account address math:** primary's first 28 bytes + 4-byte index
  - Trader (index 1): `0x5f3a…e0d9 00000001`
  - Scraper (index 2): `0x5f3a…e0d9 00000002`
- **Actor state:** Lives on the account, not in the logic. A plain account has no slot for any logic → calls revert. Context inheritance creates that slot.
- **One `AccountInherit` tx does three things:**
  1. Create the sub-account at the index
  2. Link its context to the logic (allocates actor state storage)
  3. Seed it with KMOI for gas
- **No registry needed:** Addresses are pure math; status is one RPC call: `getContextInfo(addr)` → returns `inherited_account` field (logic_id or null)

**Quality rules and house style:**
- Derivation path always `m/44'/6174'/7020'/0/0` for the primary (Voyage faucet default)
- Sub-accounts are indexed sequentially (1, 2, 3…) per agent name
- Budget enforcement is the *logic's* job, not inheritance's (honest framing: it's identity + state allocation, not a sandbox)
- Sub-accounts share the primary's key (not enforced by chain; the agent's tool surface is the guard)
- To read an agent's stored budget, call a read-only endpoint as the agent itself (the endpoint uses the caller's identity, `Sender`). Do not pass the owner's address with `Actor(owner)` instead
- `.squad.json` (local name → index map) is gitignored; the chain needs no registry
- `.env` must not have inline `#` comments (parser doesn't strip them)

**Traps and things that failed silently:**
- `AccountInherit` must be signed by the primary; a sub-account can't create siblings
- Seed transfer can't be zero; must send at least 1 KMOI
- Transaction receipt ≠ success; must check `status` and per-op errors, then re-read `getContextInfo` to confirm link landed
- One primary can inherit the same logic at multiple indices; apps usually want exactly one, so detect-and-refuse (Pip does this)
- If `ANTHROPIC_API_KEY` is not set, `run` command fails (but `spend` works without it)
- Stale squad between rehearsals: `node squad.js reset` clears local `.squad.json` name map (on-chain accounts remain, reusable)
- Agent not provisioned: the script infers this from `getContextInfo` returning null; no error message, just "agent not provisioned"

**Duration:** ~60 min live (setup 5 min, deploy 3 min, provision 2 agents ~5 min, act + report ~20 min, Pip demo ~20 min, Q&A ~5 min)

**Teaching framing (from TEACHING-GUIDE.md):**
- **Idea 1:** Primary vs sub-account (primary is you, sub-account is an account at one bank)
- **Idea 2:** Actor state: why inheritance must exist (app-specific data lives on account, not app; plain account has no slot)
- **Idea 3:** Address is math, not lookup (28 bytes + index; no registry, just arithmetic + RPC)
- **Idea 4:** Provisioning is one atomic tx (AccountInherit does create + link + fund)
- **The aha moment:** Same question (step 1 vs step 4 in Pip demo), same math, different answer: identity computed, never stored

**Open questions:**
- How many attendees attempted the $15 cash bonus tier? (inferred: incentive structures matter but not tracked here)
- Was the "trust-based swap" comparison (Session 4) called back when teaching context inheritance?

---

## Common skeleton across all sessions

### Folder structure (observed pattern)

```
session-N/
├── README.md                  # install, demo flow, bounty instructions
├── package.json              # js-moi-sdk version pinned, dotenv, minimal deps
├── .env.example              # MOI_MNEMONIC template, optional overrides
├── .env                      # (gitignored) actual wallet(s)
├── .gitignore                # ignores **/.env, node_modules, **/.env.local
│
├── coco/                      # (S1-2, 5-6 only)
│   ├── *.coco                # source contract(s)
│   ├── *.json                # compiled manifest (checked in)
│   └── coco.nut              # compile config
│
├── sdk/                       # (S1-2, 5 use this; S4 uses logic/; S3 uses scripts/)
│   ├── *.js / *.mjs          # deploy, interact, mint, transfer scripts
│   ├── .env.example          # (S3 only) overrides MOI vars
│   ├── .env                  # (S3 only, gitignored)
│   ├── package.json          # (S3 only) pins js-moi-agent-registry
│   └── *.sh                  # (S3 only) start-demo.sh, etc.
│
├── logic/                     # (S4 only)
│   ├── *.js                  # shared by CLI + UI
│   └── wallets.js            # load Alice + Bob
│
├── extras/                    # (S4 only)
│   ├── setup.js              # deploy TKA/TKB, write .env
│   ├── swap-cli.js           # step-by-step or full swap
│   └── *.js                  # mint-to-bob, rebalance, fund-wallet
│
├── frontend/                  # (S4 only)
│   └── (Vite app)
│
├── ui/                        # (S5 only)
│   ├── server.js             # Express API
│   └── public/               # browser UI
│
├── budget-logic/             # (S6 only)
│   ├── agentbudget.coco      # logic source
│   ├── agentbudget.json      # compiled
│   └── coco.nut
│
├── moi-agent-dating/         # (S3 only, standalone skill)
│   ├── SKILL.md              # OpenClaw skill manifest
│   ├── README.md             # setup + demo flow
│   └── scripts/              # node scripts
│
├── *-skills/                 # (S5 only, for vibecode)
│   └── SKILLS.md / SKILL.md  # agent prompting reference
│
└── node_modules/             # (gitignored)
```

### `.env.example` template (pattern)

```env
# Always present
MOI_MNEMONIC=your twelve word mnemonic here

# Session 1-2, 5-6 optional
MOI_DERIVATION_PATH=m/44'/6174'/7020'/0/0

# Session 1, 3-4, 5 optional
LOGIC_ID=
ASSET_ID=
TAX_ASSET_ID=

# Session 3
UPLOADER_URL=http://localhost:7777
AGENT_NAME=Jack
AGENT_URL=http://localhost:3940
MOI_AGENT_DERIVATION_PATH=m/44'/6174'/7020'/0/0

# Session 4 (two wallets)
VITE_ALICE_MNEMONIC=
VITE_BOB_MNEMONIC=
VITE_ALICE_PATH=m/44'/6174'/7020'/0/0
VITE_BOB_PATH=m/44'/6174'/7020'/0/0
VITE_TKA_ASSET_ID=
VITE_TKB_ASSET_ID=

# Session 6
LOGIC_ID=
ANTHROPIC_API_KEY=
```

### `package.json` pattern

This is a pattern, not valid JSON: some version fields hold prose such as "or later" (and the dependency list merges what different sessions use). Pick one concrete version per package when copying.

```json
{
  "name": "moi-webinar-sN",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "description": "MOI Builders Webinar Session N",
  "scripts": {
    "deploy": "node deploy-budget.js",
    "setup": "node extras/setup.js",
    "dev": "vite"
  },
  "dependencies": {
    "dotenv": "^16.4.5 or later",
    "js-moi-sdk": "0.7.0-rc15 or 0.7.0 or later",
    "js-moi-agent-registry": "0.1.0",
    "js-moi-utils": "0.7.0-rc15",
    "@anthropic-ai/sdk": "^0.111.0"
  },
  "devDependencies": {
    "vite": "latest",
    "patch-package": "^8.0.1"
  }
}
```

### README.md structure (pattern)

1. **Short title + purpose**
2. **Install** (Node, toolchain, npm, wallet, coco compile if needed)
3. **Demo flow** (step-by-step commands)
4. **Bounty** (what to capture, form link, verification steps)
5. **Troubleshooting** (common errors + fixes)
6. **Repo layout** (folder description)
7. **Notes** (gotchas, house style)

### Shared environment variables

- **Always present:**
  - `MOI_MNEMONIC`: 12-word devnet seed (Voyage faucet default path is `m/44'/6174'/7020'/0/0`)
  - `MOI_DERIVATION_PATH`: BIP-44 path (optional override)

- **SDK-specific:**
  - `LOGIC_ID`: Deployed contract ID (optional, can pass as argv to scripts)
  - `ASSET_ID`, `TAX_ASSET_ID`: Created asset IDs (stored for reuse)

- **Session 3 (OpenClaw):**
  - `UPLOADER_URL`: HTTP endpoint for card uploads (default `http://localhost:7777`)
  - `AGENT_NAME`, `AGENT_URL`: Agent identity for on-chain registration
  - `OPENAI_API_KEY`: Shell export (not in `.env` per style rules)

- **Session 4 (two-wallet swap):**
  - `VITE_ALICE_MNEMONIC`, `VITE_BOB_MNEMONIC`: Two separate wallets
  - `VITE_TKA_ASSET_ID`, `VITE_TKB_ASSET_ID`: Test assets (written by setup)

- **Session 6 (agents + budget):**
  - `ANTHROPIC_API_KEY`: Claude SDK for real-agent `run` command (optional)
  - `LOGIC_ID`: AgentBudget logic ID (written by deploy)

### SDK versions (pinned in each session)

- Session 1-2, 4: `js-moi-sdk@0.7.0-rc15`
- Session 3: `js-moi-sdk@0.7.0-rc16`, `js-moi-agent-registry@0.1.0`
- Session 5-6: `js-moi-sdk@0.7.0` or `0.7.1`

### Coco versions (in `coco.nut`)

- Session 1-2, 4: Coco 0.7.0
- Session 5-6: Coco 0.8.0-0.8.2

### Common patterns in code

1. **Wallet loading:**
   ```js
   import { VoyageProvider, Wallet } from 'js-moi-sdk'
   const provider = new VoyageProvider('devnet')
   const wallet = await Wallet.fromMnemonic(process.env.MOI_MNEMONIC, "m/44'/6174'/7020'/0/0")
   wallet.connect(provider)
   ```

2. **Logic deploy + call:**
   ```js
   const factory = new LogicFactory(manifest, wallet)
   const ix = await factory.deploy('Init').send({ fuel_limit })
   const { logic_id } = await ix.result()
   const driver = await getLogicDriver(logic_id, wallet)
   await driver.routines.Flip().send({ fuel_limit })
   ```

3. **Asset create:**
   ```js
   const ix = await MAS0AssetLogic.create(wallet, symbol, supply, manager, true).send()
   const [{ asset_id }] = await ix.result()
   ```

4. **Fuel capping:**
   ```js
   const kmoi = BigInt(String(await provider.getBalance(address, KMOI_ASSET_ID)))
   const fuel = kmoi < wantFuel ? Number(kmoi) : Number(wantFuel)
   ```

5. **Error handling:**
   ```js
   const { error } = await ix.result()
   if (error) throw new Error(error)
   ```

### Quality rules across all sessions

- **Manifests:** Checked in as `.json` (Coco's default JSON output format); recompilation optional
- **Amounts:** Plain numbers (never bigint) in `.send()` payloads
- **Fuel:** Always capped to wallet balance
- **Derivation paths:** Default to Voyage faucet path unless overridden
- **Error messages:** User-friendly, suggest fixes (e.g., "Fund at https://voyage.moi.technology")
- **Comments:** Explain *why* (state vs actor, Lockup vs Transfer) not *what* (code is self-explanatory)
- **Bounty forms:** Google Forms with timestamp + email + on-chain identifiers
- **Verification:** On Voyage explorer (voyage.moi.technology) or via live `discover` / `report` commands

---

## Prerequisites for attendees (observed across all sessions)

### Must-have

1. **Node.js 20+**: LTS version, npm included
2. **One funded MOI devnet wallet**: create at https://voyage.moi.technology, get 12-word mnemonic
3. **Internet connection**: devnet access via Voyage RPC

### Should-have

4. **Coco toolchain**: only for Sessions 1-2, 5-6 if you want to edit `.coco` sources (pre-compiled `.json` manifests are checked in)
5. **Git**: to clone the repo
6. **Text editor or IDE**: to edit `.env` and view code

### Optional but recommended

7. **OpenClaw**: required for Session 3 (install: https://docs.openclaw.ai)
8. **OpenAI API key**: for Session 3 chat LLM + Session 6 agent search (fallbacks exist)
9. **Anthropic API key**: for Session 6 real-agent `run` command (scripted `spend` works without it)

---

## What may break now, and why (devnet changes, at the time of writing)

1. **Devnet has been reset**: wallet mnemonics fund on-demand at faucet, so sessions still work. Old agent_ids from Session 3 are stale (registry never expires agents; old IDs still exist but are orphaned).

2. **SDK versions have moved on**: Sessions 1-6 pin specific RC versions (0.7.0-rc15, 0.7.0-rc16, 0.7.0, 0.7.1). At the time of writing the mainnet SDK is likely 1.0.0+ (unsourced, see Known inconsistencies). Devnet compatibility unknown.

3. **Coco compiler versions**: Sessions 1-2 use 0.7.0, Sessions 5-6 use 0.8.0+. Installation docs point to latest, so fresh installs may get mismatched compiler + manifest.

4. **OpenClaw API has evolved**: Session 3 uses OpenClaw 1.0.0+ with JSON5 config. Config schema may have changed (unverified).

5. **OpenAI API changes**: Session 3 message servers use `gpt-5.4-mini` (observed in OVERVIEW.md); current API may deprecate older models.

6. **Voyage explorer indexer lag**: Sessions assume explorer is within a few minutes of on-chain state; if lag has increased, attendees may think their txs didn't land.

---

## Stated plan for the series

From README.md and OVERVIEW.md:

- **Sessions 1-6:** Core MOI Builders series
  - S1: fundamentals (Flipper, state)
  - S2: assets (MAS0, TaxToken)
  - S3: agents (agent registry, OpenClaw)
  - S4: swaps (Lockup + Release)
  - S5: NFTs (MAS1, UI)
  - S6: context inheritance (multi-agent budgets)

- **Session 7:** Agentic Payments (find + pay an agent on MOI)
  - Combines Sessions 3 (agent registry discovery) + 2/4 (settlement via MAS0)
  - Newer format (npm workspaces, TypeScript monorepo, always-on-chain)
  - Not part of the "early" series (Sessions 1-6)

- **Vibecode alternative:** All sessions can be taught with skills-only (agent writes contracts + scripts from prompts)
  - Requires coco-skills and js-moi-sdk-skills setup
  - Same learning outcomes, different delivery (interactive + agent-authored vs. pre-written)

---

## Reusable assets

Paths below start with `~/` and are on Adithya's Mac. The `MOI-Webinars/...` ones also exist at the same relative path in the repo (for example `session-4/logic/wallets.js`); `moi-agent-budget/...` is a separate folder on his Mac.

### Templates and configs

1. **`.env.example` template**: `~/MOI-Webinars/session-1/.env.example` (pattern for all sessions)
2. **`package.json` template**: pattern repeated in S1 (`moi-webinar-s1`), S2 (`moi-webinar-s2`), etc.
3. **`README.md` structure**: consistent across all sessions (Install → Demo flow → Bounty → Troubleshooting)

### Scripts and utilities

1. **Wallet loader**: `~/MOI-Webinars/session-4/logic/wallets.js` (load Alice + Bob from env)
2. **Fuel capping**: `~/MOI-Webinars/session-5/sdk/mint.js` `cappedFuel()` function
3. **Manifest loader**: Standard `import manifest from '../coco/flipper.json' with { type: 'json' }` (ES module import)
4. **Error handling**: Standard pattern: `const { error } = await ix.result(); if (error) throw new Error(error)`

### Coco contracts

1. **Flipper**: `~/MOI-Webinars/session-1/flipper/flipper.coco` (simplest contract, reused in vibecode examples)
2. **ContextFlipper**: `~/MOI-Webinars/session-1/context-flipper/context_flipper.coco` (per-actor state)
3. **TaxToken**: `~/MOI-Webinars/session-2/coco/taxtoken.coco` (5% fee-on-transfer)
4. **MAS1**: `~/MOI-Webinars/session-5/coco/mas1.coco` (NFT collection with metadata)
5. **AgentBudget**: `~/moi-agent-budget/budget-logic/agentbudget.coco` (actor-state budgets + enforcement)

### OpenClaw skill

1. **moi-agent-dating**: `~/MOI-Webinars/session-3/moi-agent-dating/` (complete skill with SKILL.md, three .mjs scripts, message server, uploader)

### UI components

1. **Swap card UI**: `~/MOI-Webinars/session-4/frontend/` (Vite app with lock/flip/claim buttons)
2. **NFT mint + transfer UI**: `~/MOI-Webinars/session-5/ui/` (Express server + browser form)

### Documentation

1. **webinar-code-reference.md**: `~/MOI-Webinars/webinar-code-reference.md` (code walkthrough with snippets)
2. **webinar-vibecode-plans.md**: `~/MOI-Webinars/webinar-vibecode-plans.md` (vibecode prompt flow for all sessions)
3. **OVERVIEW.md**: `~/MOI-Webinars/OVERVIEW.md` (Session 3 live demo flow, exhaustive)
4. **TEACHING-GUIDE.md**: `~/moi-agent-budget/TEACHING-GUIDE.md` (context inheritance teaching notes)

---

## Rules and house style

### Code style

- **Language:** Mostly JavaScript (Node.js `.js` or `.mjs`), Coco for contracts, HTML/CSS for UIs
- **Imports:** ES modules (`import ... from '...'`)
- **Error handling:** Early returns, user-friendly messages
- **Comments:** Explain why (conceptual) not what (code is clear)
- **Formatting:** Standard (no apparent lint config; manual tabs/spaces consistent within each file)

### Naming conventions

- **Wallets:** `alice`, `bob`, `primary`, `wallet`, `signer`
- **Contracts:** PascalCase (Flipper, TaxToken, MAS1, AgentBudget)
- **Functions:** camelCase (deploy, flip, lockup, release, claim)
- **Constants:** UPPER_SNAKE_CASE (SUPPLY, MINT_AMOUNT, TAX_BPS)
- **File names:** kebab-case scripts (`sdk/deploy.js`, `extras/swap-cli.js`, `squad.js`), snake_case Coco (`flipper.coco`, `taxtoken.coco`, `agentbudget.coco`)

### Devnet-specific conventions

- **Provider:** Always `new VoyageProvider('devnet')` (never hardcoded RPC URL)
- **Derivation path:** Default `m/44'/6174'/7020'/0/0` (Voyage faucet standard)
- **Addresses:** Hex strings starting with `0x`, 64 chars = 32 bytes
- **Asset/Logic IDs:** Also hex, printed with `0x` prefix
- **Amounts:** Plain numbers (not bigint) for `.send()`, BigInt for balance comparisons
- **Fuel limits:** Capped to wallet's KMOI balance, typical values 20k-500k

### Bounty style

- **Forms:** Google Forms (https://forms.gle/...) with timestamp + email collection
- **On-chain verification:** Voyage explorer (https://voyage.moi.technology) search by address or tx hash
- **Submission deadlines:** "Before the next session" (loose, soft-enforcement)
- **Rewards:** Token bounties (KMOI) for completion, cash bonuses ($15-500 MOI) for excellence

### Documentation style

- **README structure:** TL;DR → Install → Demo flow → Bounty → Troubleshooting → Repo layout → Notes
- **Code references:** File paths are relative to repo root (e.g. `sdk/deploy.js`, not `./sdk/deploy.js`)
- **External links:** Full URLs (https://voyage.moi.technology, https://forms.gle/..., https://cocolang.dev)
- **Emphasis:** Bold for paths and commands, inline code for variable names
- **Walkthroughs:** Step-by-step numbered lists with "say" bullets (what the presenter narrates) and expected outputs

---

## Traps and gotchas (accumulated from all sessions)

1. **Derivation path mismatch**: Voyage faucet uses `m/44'/6174'/7020'/0/0`; if wallet was funded at a different path, scripts fail silently on "account not found"

2. **BigInt in signing**: `.send()` payloads must use plain numbers, not bigint (breaks signing on devnet)

3. **Pre-compiled manifests**: Checked in for convenience, but if `.coco` source is edited, manifest must be recompiled or old manifest will be used

4. **CocoLab is interactive**: Can't be scripted or recorded; must be walked through live (or pre-recorded as demo)

5. **Session 3: env vars in multiple places**. `MOI_MNEMONIC` must be in both `openclaw.json` `env.vars` (for injection) AND `skills.entries.*.env` (for ✓ Ready gate); discovered during setup

6. **Session 3: dual-stack binding**. Message servers must bind on `::` (dual-stack), not just `127.0.0.1`, for Node 18+ `fetch` compatibility

7. **Session 3: message-server OPENAI_API_KEY**. Read from shell env, not from scripts/.env; must be exported before `start-demo.sh`

8. **Session 4: patch-package**. Postinstall script must run to fix SDK's ESM build; if broken, UI won't load

9. **Session 4: Lockup has no guard**. Calling `release()` when nothing is locked succeeds but moves zero funds; app must check balance delta

10. **Session 5: MAS1 is logic-backed**. Deploy via AssetFactory + manifest, not protocol-native MAS1AssetLogic.create

11. **Session 6: AccountInherit must be signed by primary**. Sub-account can't create siblings; only primary can mint sub-accounts

12. **Session 6: Seed transfer can't be zero**. Must send at least 1 KMOI; zero amount is rejected

13. **Session 6: `.env` value format**. Inline `#` comments are NOT stripped; must keep values comment-free on their own lines

14. **General: Devnet reset**. Agent IDs accumulate; old IDs from earlier runs still exist (registry never expires)

15. **General: Explorer lag**. Voyage may be minutes behind on-chain state; verify with CLI commands instead (discover.mjs, report)

---

## Proposals for a skill (not written out)

This section is an outline of what a skill for these webinars could contain. It is a proposal, not finished content: the per-session examples below were never written, and no code is included. The real material is under "Reusable assets".

### SKILL.md structure (for vibecode)

Outline only; the sections are headings with no content yet.

```yaml
---
name: moi-webinars-devrel
description: Teach MOI Builders webinar series topics
metadata:
  openclaw:
    requires:
      bins: [node, coco]
      env: [MOI_MNEMONIC, OPENAI_API_KEY]
---

# MOI Builders DevRel Skills

## Session 1: CocoLab + SDK Fundamentals

(Example not written.)

## Session 2: Native Assets

(Example not written.)

## Session 3: Agent Registry (contract + client)

(Example not written. Idea: write an Agent Registry class, then an OpenClaw skill that calls the SDK functions.)

## Session 4: Swap Logic

(Not written. Idea: teach Lockup/Release semantics.)

## Session 5: MAS1 NFT Collection

(Example not written.)

## Session 6: Context Inheritance

(Example not written. Idea: AgentBudget with actor state and budget enforcement.)
```

### SKILL.md reference files to bundle

1. **Coco reference:** Language syntax, state/endpoint patterns, asset standards (MAS0, MAS1, MASX)
2. **js-moi-sdk reference:** API docs (VoyageProvider, Wallet, LogicFactory, AssetFactory, getLogicDriver, getAssetDriver)
3. **Patterns reference:** Fuel capping, wallet loading, error handling, manifest loading
4. **Example outputs:** Sample compiled manifests, sample SDK call results, sample UI

### Scripts to include

1. **Utility script:** Fuel capper, wallet loader (copy from session-4/logic/wallets.js and session-5/sdk/mint.js)
2. **Validator script:** `verify-sdk.cjs` (from session-5/js-moi-sdk-skills/scripts/) to verify SDK installation
3. **Setup scripts:** Per-session setup.js (deploy assets, provision agents, etc.)

### Templates to bundle

1. `.env.example` (one for single wallet, one for two-wallet swaps)
2. `package.json` (pinned sdk versions)
3. `README.md` structure (Install → Demo → Bounty → Troubleshooting)
4. Coco `coco.nut` compile config (0.7.0 and 0.8.0+ variants)

### Prompts (for vibecode mode)

Structured as markdown with:
1. **Conceptual intro** (what we're building)
2. **Prompt for contract** (write Flipper, TaxToken, MAS1, etc.)
3. **Prompt for compile** (run coco compile)
4. **Prompt for SDK script** (deploy, mint, transfer, etc.)
5. **One-liner to land** (the point: "empty repo → working dapp")

Example (Session 1):
```markdown
## Session 1: Flipper (The fundamentals)

We're building a simple state-toggling contract and deploying it from JavaScript.

### Prompt 1: Write the contract
> Read the coco-skills. Write a Flipper contract: one boolean logic-state field, 
> a deploy endpoint that sets it false, a dynamic Flip endpoint that toggles it, 
> and a static Get endpoint that returns it.

### Prompt 2: Compile
> Compile it with `coco compile` and show me the manifest it produced.

### Prompt 3: Deploy and flip
> Now read js-moi-sdk-skills. Write a script that loads my wallet on Voyage devnet, 
> deploys that manifest, calls Flip, and prints the value before and after.

**One point to land:** "Empty repo → a deployed contract I flip on-chain, in two prompts."
```

### Pointers to reference implementations (no code included here)

The line counts below are rough sizes as given in these notes ("LOC" = lines of code); they were not counted or verified. The code itself is in the paths listed under "Reusable assets".

1. **Flipper** (S1): 30 LOC Coco + 20 LOC SDK
2. **TaxToken** (S2): 30 LOC Coco + 15 LOC SDK
3. **AgentRegistry + OpenClaw integration** (S3): 50 LOC Coco + 3 SDK scripts (100 LOC total)
4. **Swap logic** (S4): 0 LOC Coco (MAS0 native) + 80 LOC SDK (lockup/release) + 50 LOC UI
5. **MAS1 NFT** (S5): 100 LOC Coco + 60 LOC SDK + 30 LOC UI
6. **AgentBudget** (S6): 50 LOC Coco + 120 LOC SDK (squad manager) + 50 LOC Pip agent

---

## Open questions

1. **Devnet persistence:** Do agent IDs persist across devnet resets, or are they wiped? (observed: accumulating IDs suggest persistence, but unconfirmed)

2. **Bounty verification:** How are Google Form submissions verified on-chain? (inferred: manual spot-check by Adithya; no automation)

3. **SDK roadmap:** What versions of the SDK are still supported on current devnet? (observed: 0.7.0-rc15 through 0.7.1 used; current mainnet likely 1.0.0+)

4. **Coco compiler versions:** Which versions of the Coco toolchain are backward-compatible? (observed: 0.7.0 and 0.8.x coexist; no version matching enforced)

5. **OpenClaw schema changes:** Has the OpenClaw config format changed since the webinar was recorded? (observed: JSON5 format; unknown if schema has evolved)

6. **Vibecode track usage:** Were attendees actually prompted to use Claude Code for vibecoding, or was that an alternative mode for self-study? (inferred: alternative, not live in sessions)

7. **Replay videos:** Are the webinars recorded and uploaded? (not mentioned in docs; assume yes but unconfirmed)

8. **Attestation for bounties:** Do attendees provide public wallet addresses, or are submissions tied to email only? (observed: form asks email + wallet + tx hash; names are not collected)

9. **Session 7 maturity:** Is Session 7 (Agentic Payments) ready for live delivery, or is it still in development? (observed: repo exists but not part of the "early" series)

10. **Multi-language variants:** Are these materials translated or localized, or English-only? (observed: English only; no translation mentioned)

---

## Known inconsistencies in these notes

The notes disagree with themselves in the places below. They are listed, not resolved; check the source files before relying on either side. Line numbers refer to this file.

1. Agent IDs after a devnet reset: L879 says the old Session 3 IDs are "stale" and "orphaned"; L1031 says old IDs "still exist"; L1148 says whether IDs persist is unconfirmed.
2. Bounty amounts and units: L264 "open 500-MOI bounty", L427 "500 KMOI" baseline, L523 "500 MOI + $15 cash", L991 "$15-500 MOI". It is not clear whether "MOI" and "KMOI" mean the same asset, or what the cash and token amounts really were.
3. Model used by the Session 3 message servers: L269 gives `openai/gpt-4-mini` or `gpt-5.4-mini`; L887 says `gpt-5.4-mini`, both marked observed.
4. Session 3 derivation-path variable: L280 names `MOI_DERIVATION_PATH`; the `.env.example` pattern at L716 names `MOI_AGENT_DERIVATION_PATH`.
5. Session 6 mnemonic variable: L595 lists `USER_MNEMONIC`; every other place (L98, L166, L483, L774) uses `MOI_MNEMONIC`.
6. "Current mainnet SDK is likely 1.0.0+" (L881 and L1152) has no source and sits next to SDK versions of 0.7.x. Treat it as a guess.
7. Session 7's topic: L905 and L1164 call it "Agentic Payments" (find and pay an agent). `webinars-mature.md` describes the series arc as "S7 identity, S8 + authority, S9 + standard".
8. Coco versions: Session 5 needs "0.8.2+" (L433) and uses "0.8.2 default" (L486); Session 6 needs "0.8.0+" (L530); L803 gives a range "0.8.0-0.8.2" for both. L802 puts Session 4 under Coco 0.7.0, but L1140 says Session 4 has 0 lines of Coco (it uses the built-in MAS0 asset).
9. Session 3 timing: the timed beats (L220 to L256) add up to roughly 6 to 8 minutes, yet L303 says "beats 1-8 ~50 min".
10. Folder layout: L654 shows `coco/` as used by Sessions 1-2 and 5-6, while L682 shows Session 6's Coco source in `budget-logic/` instead.

---

## Glossary

Terms are defined as the MOI team uses them. Anything marked "(as used in these notes)" is the research assistant's reading, not an official definition.

- **Actor state**: Coco storage kept separately for each participant who calls a logic (declared `state actor`). Contrast with logic state.
- **AccountInherit**: the interaction that creates a sub-account, links it to a logic and funds it in one step (Session 6, as used in these notes).
- **AgentBudget**: the Session 6 demo logic that records a per-agent budget and refuses spending past it.
- **AssetFactory / LogicFactory**: SDK helper classes that deploy an asset (with a manifest) or a logic from a compiled manifest (as used in these notes).
- **Basis points (bps)**: hundredths of a percent; 500 bps = 5%.
- **BIP-44**: a standard that says how to derive wallet addresses from one mnemonic; `m/44'/6174'/7020'/0/0` is such a path.
- **Bounty**: a reward offered to attendees who finish the session task and submit a form, in these notes.
- **Coco**: MOI's contract language. **CocoLab**: Coco's playground, an interactive prompt (a REPL) where you type commands one at a time.
- **Context inheritance**: giving a sub-account its own storage slot for a logic so the logic can keep per-agent state (Session 6, as used in these notes).
- **Derivation path**: the part of a wallet address recipe that says which account to take from a mnemonic. The Voyage faucet default is `m/44'/6174'/7020'/0/0`.
- **Devnet**: MOI's test network; it is reset from time to time, so old assets, logics and agent IDs may disappear or become stale.
- **Dual-stack**: a server listening on both IPv4 and IPv6 (the `::` address).
- **ESM**: ECMAScript modules, JavaScript's `import`/`export` format.
- **Express**: a small Node.js web server library (used for the Session 5 UI server).
- **Faucet**: a service that gives free devnet funds; the Voyage faucet also issues a new wallet.
- **Fee-on-transfer**: a token that takes a cut on every transfer (the Session 2 TaxToken takes 5%).
- **Flipper / ContextFlipper**: the Session 1 demo contracts that toggle a true/false value, shared (Flipper) or per participant (ContextFlipper).
- **Fuel**: what an interaction pays to run; `fuel_limit` caps it.
- **Interaction / interaction hash**: MOI's word for a transaction, and its identifier.
- **IPFS / data URI**: IPFS is a decentralised file store; a data URI puts the file content inside the link itself. Session 3 used data URIs for agent cards and says production would use IPFS.
- **JSON5**: a relaxed form of JSON that allows comments, unquoted keys and trailing commas.
- **KMOI**: MOI's native asset; it pays for fuel.
- **LOC**: lines of code.
- **Lockup / Release**: MAS0 operations that set funds aside for a named counterparty and later let that party claim them (Session 4).
- **Logic / logic ID**: a deployed Coco contract on MOI, and its identifier. **Logic state** is one copy shared by all callers.
- **Manifest**: the compiled JSON description of a Coco contract that the SDK deploys.
- **MAS0**: an asset standard created without a contract. **MASX**: a logic-backed asset. **MAS1**: the NFT standard (in Session 5 it is deployed logic-backed, via AssetFactory).
- **Mnemonic**: the 12-word phrase from which a wallet's keys are derived. Devnet mnemonics only; never reuse real ones.
- **OpenClaw**: the third-party AI agent framework used in Session 3 (the notes attribute it to Nous Research; unverified here).
- **patch-package**: an npm tool that re-applies local fixes to a dependency; Session 4 uses it to fix the SDK's ESM build.
- **Pip**: the demo agent in Session 6 (`agent.js`) that works out and provisions its own sub-account.
- **Participant-centric**: MOI is participant-centric, not account-centric. "Actor" in these notes (as in "actor state") means a participant.
- **RPC**: the remote procedure call interface of a MOI node; `moi.Lockups` is a raw JSON-RPC method here.
- **SDK**: software development kit; here `js-moi-sdk`, the JavaScript library for MOI. **js-moi-agent-registry** is its companion package for the agent registry.
- **Squad**: the Session 6 script `squad.js` that provisions and runs named agents; `.squad.json` is its local name-to-index map.
- **TKA / TKB**: the two demo tokens in the Session 4 swap. **TaxToken**: the Session 2 fee-on-transfer demo.
- **Vibecode**: building by prompting an AI agent (here Claude Code) to write the contract and scripts, rather than running pre-written ones.
- **Vite**: a front-end build and dev-server tool (used for the Session 4 UI).
- **Voyage**: MOI's explorer and dev tooling site (voyage.moi.technology); `VoyageProvider` is the SDK class that connects to it.
- **Wallet / sub-account**: a key pair that signs interactions; a sub-account is an account derived from a primary one (Session 6, address = primary's first 28 bytes plus a 4-byte index).
