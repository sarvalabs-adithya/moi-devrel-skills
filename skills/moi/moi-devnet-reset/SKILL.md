---
name: moi-devnet-reset
description: "After the MOI devnet (the test network) is reset or wiped, tell a real reset from an outage or an upgrade with read-only reads, then redo what it broke, in order, in every MOI product and in decks, posts and demos. Use this first, before the product's own ops skill, for \"devnet was reset\", \"devnet wipe\", \"new registry id\", \"account not found\" in more than one place, \"faucet_unavailable\", \"agents need registering again\", \"Could not load the MOI agent registry\", chainStatus stale or unreachable, \"the Explorer shows old agents\", a go-moi release or network upgrade that may wipe state, or a demo, deck or post that quotes an id or hash that may be dead. Orders the work across the Launchpad, MCP server, Explorer, demos and docs, drafts the messages and keeps a reset log. If the reads show no reset, continue in moi-launchpad-ops (Explorer: moi-launchpad-ops/explorer) or moi-mcp-ops. Pull requests are moi-devrel/ship, claims moi-devrel/claim-check, other teammate messages moi-devrel/templates/messages.md."
---

# MOI devnet reset: what to redo, in order

## What this covers
A reset wipes accounts, assets, contracts, registrations and the registry id on devnet (`moi-devrel/references/devnet.md`). Three products pin the registry id separately, and every demo, deck and post that quotes an id or a hash goes stale with no error. This skill holds the order of work, the hand-offs between products, the reset steps of each, and the log. Recorded: full wipes on 2026-08-15 and 2026-09-11, and registry failures or replacements on 08-06, 08-10 and 08-13 (`references/history.md`).
Not covered: shipping, health and secrets of one product are `moi-launchpad-ops` (its Explorer is the branch `moi-launchpad-ops/explorer`) and `moi-mcp-ops`; website, Dataroom and Points are `moi-web-products-ops`; docs pages `moi-docs`; claims `moi-devrel/claim-check`; webinar demos `moi-webinar` and decks `moi-webinar/deck`; a release note `moi-blog/release-pack`; commits, PRs and merges `moi-devrel/ship`; teammate messages other than the reset drafts in `templates/messages.md` are `moi-devrel/templates/messages.md`, checked with `moi-devrel/scripts/check-message.py`.

## Before you start
`SKILLS`, "the operator", "the previous operator" and `ASK: <person>` are defined in `moi-devrel/SKILL.md`. Facts are as of 2026-10-03 unless dated; Explorer PR #5 (merged 2026-10-07), the owners, the MCP sync method and the Supabase move were corrected on 2026-10-13; the MCP production state and the Explorer deploy failure on 2026-10-14. Terms: `moi-devrel/references/glossary.md`. Here, the registry is the on-chain list of agents and its logic id is what the products pin; a short id is the 8 hex digits after `0x20000000` (`c684f926`), and only `id-grep.sh` accepts it, while `reset-detect.sh` needs the full id (`0x` then 64 hex digits); a stranded agent is one registered on a registry that is gone: its owner's dashboard shows "N agents need registering again", the owner re-registers from the dashboard button, and nobody deletes the row (`references/launchpad.md`, L10; `moi-launchpad-ops/references/troubleshoot.md`, row 26); the registration wallets are the Launchpad's three wallets that create and fund a new user's account, and the sponsor is a funded wallet that pays to recreate them; the faucet gives devnet KMOI to accounts that already exist; the market contract (AgentMarket) holds the price of each paid agent; a fresh-wallet pass is a new wallet activated and an agent registered, end to end, checked by receipts. Woken by an alert: read "First five minutes" in `references/detect.md` first.
- [ ] The trigger: the alert text, the user report or the release, with its UTC time. The operator provides it. Ask: "What did you see, where, and at what UTC time?"
- [ ] A reset folder at the root of any working copy you hold (one folder for the whole reset), out of git because the log names accounts and people. Claude makes it. The self-ignoring file also protects a public repository: `mkdir -p "devnet-reset-<YYYY-MM-DD>" && printf '*\n' > "devnet-reset-<YYYY-MM-DD>/.gitignore"`
- [ ] A baseline file `devnet-reset-<date>/state.txt` of values that predate the event. Claude builds it with the operator's working copies. None exists as of 2026-10-03: `references/detect.md`, "First baseline".
- [ ] Working copies of `sarvalabs/moi-agent-launchpad` (private), `sarvalabs/agent-explorer` (private), `sarvalabs/moi-mcp` (public) and, for the MCP deploy, `sarvalabs/voyage-api` (private). The operator provides them; cloning is a download, so ask first. Ask: "Which folders hold these four?" ASK: Rahul who grants access.
- [ ] Which of the three products DevRel owns. Not settled. ASK: Rahul. Until he answers, treat a product as not yours: it gets the facts and a draft, not your change. The rule for each answer is in `references/order-of-work.md`, "Who can act".
- [ ] Identity before any commit or pull request: the operator provides the work login and domain; set `PREFLIGHT_WORK_DOMAINS` and `PREFLIGHT_EXPECT_GH_LOGIN` once, `cd` into the repo, run `bash "$SKILLS/moi-devrel/scripts/preflight.sh"`. Commits carry the work identity and no AI co-author line or "generated with" footer.
- [ ] Who has a MOI Wallet account on the new chain to act as sponsor, and who holds the three Launchpad registration mnemonics outside GitHub. The operator asks. ASK: Upendhar (DevOps holds the registration mnemonics), Rahul.

## The run
GATE means stop and ask the operator for an explicit yes naming the action. Per-product tables with the read-only check first, the change second and the verification last: `references/launchpad.md`, `mcp.md`, `explorer.md`. Why this order and who does each step: `references/order-of-work.md`. Commands run from any folder unless a reference file names a working copy.
| # | Step | What to do | Where or command | Done when |
|---|---|---|---|---|
| 1 | Detect and confirm | Read only. Compare with the baseline (a run without one cannot show a reset). Decide: reset, registry moved, upgrade, outage or unknown. GATE: the operator sends message 1 to the protocol team. If the reads show no reset, stop here and continue in the product's own skill (`moi-launchpad-ops`, `moi-mcp-ops`, or for the Explorer its branch `moi-launchpad-ops/explorer`) | `bash "$SKILLS/moi-devnet-reset/scripts/reset-detect.sh" --state "devnet-reset-<date>/state.txt"`; `references/detect.md` | A verdict and its supporting lines are in the log, and message 1 is sent or its GATE is waiting |
| 2 | Open the log, record the old ids | Copy the log. For each dead id (the registry and KMOI ids in `state.txt`, and the market contract if you know it) list every file that pins it, before editing anything. The script never opens `.env.example`: use the grep in `references/content-and-demos.md` | `cp "$SKILLS/moi-devnet-reset/templates/reset-log.md" "devnet-reset-<date>/LOG.md"`; `bash "$SKILLS/moi-devnet-reset/scripts/id-grep.sh" --files <old id> <working copies>` | Old ids and their pins are in the log |
| 3 | Freeze | Nothing may spend funds, deploy a demo or say "live" against a state that may be replaced. Check what is scheduled or posted. GATE for anything in a shared service, which the operator edits | `references/order-of-work.md`, "Freeze" | The operator confirmed the freeze |
| 4 | Facts from the protocol team | New registry id, package versions, which constants moved, whether the faucet wallets live, and whether the state is final. Wait for the reply to message 1 (sent at step 1). Steps 2, 3 and 6 do not need it: do them meanwhile. Steps 5 and later do | `templates/messages.md` message 1 | The reply is logged with who and when |
| 5 | Verify the new registry | Read only. The script checks that it exists and exposes all 10 routines. An unsigned register call is optional: it needs the Launchpad code installed (GATE: download) and its throwaway code is not in the repo, so if you skip it list it under "Not verified". Nothing is sent | `bash "$SKILLS/moi-devnet-reset/scripts/reset-detect.sh" --no-products --registry <full registry id: 0x then 64 hex digits, not the 8-digit short id>`; `references/launchpad.md` L3 | Both registry lines PASS (the `net.NetworkID` WARN is expected); nothing was sent |
| 6 | Constants and SDK, if they moved | One SDK pair for all three repos, on local branches. GATE: installing downloads packages; push, PR and merge | `references/launchpad.md` L4, `mcp.md` M4, `explorer.md` E4 | Typecheck, tests, build and a strict install pass locally |
| 7 | Wallets and funds | A human with a wallet funds a sponsor. DevOps holds the registration mnemonics. The operator runs the script in their own terminal. GATE: spends devnet funds. Claude never handles a recovery phrase | `references/launchpad.md` L5 and L6 | A dry run shows the wallets, and each creation receipt is status 0 |
| 8 | Redo the Launchpad | Point it, deploy, redeploy the market contract if gone, fix the banners. GATE: setting a variable, a workflow run, a merge, a devnet deploy | `references/launchpad.md` L7 to L10 | `/api/stats` says `ok` |
| 9 | Redo the MCP server | Read caller, registry id, sync the copy in `voyage-api`, run its deploy. GATE: a PR, a workflow run | `references/mcp.md` M3 to M8 | `moi_resolve_agent` answers with no "account not found" |
| 10 | Redo the Explorer | Registry id in code, server identity, deploy, then the sync. GATE: a PR, a merge, a write to the production database | `references/explorer.md` E2 to E7 | Every agent of the new registry is listed by `/registry/agents`; leftover rows of the old registry are Gokul's decision |
| 11 | Drift check | Search the new and the old id across the three repos and compare with what the protocol team published | `bash "$SKILLS/moi-devnet-reset/scripts/id-grep.sh" <new id> <working copies>` | The old id remains only where a test or a history file pins it out |
| 12 | Content and demos | Decks, posts, docs, READMEs, session demos and demo repos that quote an id, a hash or "live". GATE for anything pushed, posted or in a shared service | `references/content-and-demos.md` | Each item is fixed or handed to its owner as a draft |
| 13 | Tell people | Drafts only; the operator sends. "Fixed" only after step 14. Check each filled draft with `check-message.py` (kind in `templates/messages.md`) | `references/telling-people.md`, `templates/messages.md`; `python3 "$SKILLS/moi-devrel/scripts/check-message.py" --to protocol "devnet-reset-<date>/<draft>.txt"` | The checker shows 0 errors and the operator has read and sent each one |
| 14 | Verify and log | Run the detector with the new ids, not the old baseline (which would report the reset again); do a fresh-wallet pass on the Launchpad (GATE: spends funds); fill the log; save the new baseline, keeping the old file as `state-before.txt`; a dated note in the repos' docs (GATE: PR) | `bash "$SKILLS/moi-devnet-reset/scripts/reset-detect.sh" --registry <full registry id> --genesis-account <new KMOI id> --version <new version> --print-state`; `references/launchpad.md` L11 | The hand-back below is written |

## Which file to read
| You see, or you are doing | Read |
|---|---|
| An alert in the first five minutes; a site is down and nothing says reset; reset, outage or upgrade | `references/detect.md` |
| Launchpad `chainStatus` `stale` or `unreachable`, 503 `faucet_unavailable`, "N agents need registering again", users cannot activate | `references/launchpad.md` |
| claude.ai connector or `moi_resolve_agent`: "Could not load the MOI agent registry ... account not found" | `references/mcp.md` |
| agents.moi.technology lists old agents, or `/health` is ok and the list is frozen | `references/explorer.md` |
| A demo, setup script or preflight says "account not found"; a post, deck or doc quotes an id | `references/content-and-demos.md` |
| Order of steps, who can act on the VM, who owns what | `references/order-of-work.md` |
| Who to tell and what to say; drafts | `references/telling-people.md`, `templates/messages.md` (other teammate messages: `moi-devrel/templates/messages.md`) |
| What happened last time and how long it took | `references/history.md` |
| Something failed silently | `references/traps.md` |
| The log to fill during a reset | `templates/reset-log.md` |
| Testing a change to this skill | `evals/evals.md` |

## Facts that fail silently
1. A health answer proves the process, not the data. Explorer `/health` was `ok` with a frozen index, and the MCP `/health` was `ok` while its registry reads failed (2026-10-03). Read the data.
2. A frozen registry reads fine. On 2026-08-06 registry writes stopped executing and reads kept working, unnoticed for four days. Only a registration receipt shows it.
3. Three repos pin the registry id separately (the Explorer in two places since its PR #5 merged on 2026-10-07: the server config and the client build config), and the registry package embeds an old one. They moved 4, 11 and 12 days after the 2026-09-11 wipe, and the live MCP was still on the dead id on 2026-10-03 and 2026-10-13: production is a copy in `voyage-api` that had been synced before the pin reached `moi-mcp`. It was synced and deployed on 2026-10-14 and lookup answers now.
4. The receipt, not the broadcast. Wallet activation said "Wallet is ready" while the chain reverted it (2026-09-15).
5. A wiped account cannot recreate itself. The faucet funds only accounts that exist, so a person with a wallet on the new chain must start the funding.
6. Wait for "final". The registry failed on 2026-08-06, was replaced on 08-10 and 08-13, and the chain was wiped on 08-15.
7. An old SDK prints the retired KMOI id, which looks like a wipe. Check the SDK version before believing a genesis alarm (`references/detect.md`).
8. Never delete rows to fix a reset. Owners re-register; the stranded check works it out.
9. `net.NetworkID` does not exist on the running build (-32601 on 2026-10-03). Publish no network ID.
Every other trap, with dates: `references/traps.md`.

## Gates
Nothing below happens without the operator's explicit yes in this conversation, naming the action:
- Sending any message, to anyone. Claude drafts, the operator sends. No pull request or issue comment that notifies a teammate.
- Push, pull request, merge (a merge to the Launchpad `master`, Explorer `main` deploys), post or schedule, and any edit of a copy in a shared service.
- A deploy or a manual workflow run, including "MOI Agent Launchpad CI/CD", "Build Push and Deploy Agent Explorer" and "Deploy MOI MCP Gateway".
- Setting or changing a GitHub Actions secret or variable, such as `MOI_AGENT_REGISTRY_LOGIC_ID`.
- A database migration or any write to a production database, including the Explorer sync and removing its rows. An admin write on production.
- Restarting or changing anything on a VM. That is DevOps's. ASK: Upendhar.
- Spending devnet funds, deploying a contract or creating an account on devnet, including the faucet, the registration wallets, the market contract and the fresh-wallet pass.
- Downloading a file, including a clone, `npm install` and `npm ci`: state what, from where. Uploading or sharing a file in cloud storage. Switching the git or `gh` identity.
- Recovery phrases: Claude never handles one, including a throwaway one. If one is pasted, do not repeat it and tell the operator it is exposed.
A yes covers the one action it names. Details: `moi-devrel/references/consent-and-identity.md`.

## Keys and access
Names only; none is needed to read. `moi-devrel/references/keys-and-access.md` says where each lives and who grants it (status TBD for every entry). Reset-specific: repo admin on the Launchpad and Explorer repos (to set a variable or secret); `MOI_AGENT_REGISTRY_LOGIC_ID` (a variable, not a secret); `MOI_REGISTRATION_MNEMONIC_1` to `_3` (DevOps); `MOI_PLATFORM_MNEMONIC`; `MOI_SPONSOR_MNEMONIC` and `MOI_DEPLOYER_MNEMONIC` (never stored, typed at a hidden prompt: `moi-devrel/references/consent-and-identity.md` section 4, rule 6); `MOI_READ_CALLER` (MCP), `MOI_READ_CALLER_ADDRESS` (Launchpad, Explorer); `MOI_CANARY_ACCOUNT`; the Explorer's `MOI_MNEMONIC`; `UPSTREAM_READ_TOKEN`; Teleport and SSH (DevOps). Never open an `.env` file.
Two of the three products have a security note. Read it before any step that touches their admin (the Explorer sync, the MCP deploy):
- MCP server: `project-handover-docs/MCP-SERVER.md` records no finding. The 2026-10-02 research note said one was open; its content is not recorded (the previous DevRel's notes); ASK: Rahul before touching sign-in or other admin code.
- Agent Explorer: a security finding is open, recorded in `project-handover-docs/LIST-OF-DEPENDENCIES.md` (Agent Explorer, ToDo 1). Read it and ask Gokul before touching the server's admin.

## Hand-back
```
Produced: <log path, new baseline path, drafts>
Reset: <verdict, old ids, new ids, the protocol team's confirmation>
Per product: Launchpad <state>, MCP <state>, Explorer <state>, each with its proof
Content and demos: <fixed, handed to whom, left>
Told: <who, which message, sent by the operator when>
Remaining: <numbered, each with who owns it, and every ASK still open>
Not verified or simulated: <say so, or "none">
Ready: yes or no, because <one reason>
```
Ready is yes only when `reset-detect.sh` shows no CHANGED line the log does not explain, each product's verify row passed, a fresh-wallet pass has a receipt, and the old id remains only where a test or a history file pins it out. A status lists work that was done; a to-do is labelled one.
