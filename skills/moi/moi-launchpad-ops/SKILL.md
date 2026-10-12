---
name: moi-launchpad-ops
description: "Run the MOI Agent Launchpad (launchpad.moi.technology, repo sarvalabs/moi-agent-launchpad) and, as its explorer branch, the Agent Explorer (agents.moi.technology, repo sarvalabs/agent-explorer). Use for \"the launchpad is down\", \"launchpad health\", \"agents fail to register\", \"chainStatus\", \"account not found\", \"faucet_unavailable\", \"ship a launchpad change\", \"change a launchpad setting or secret\", \"MOI_AGENT_REGISTRY_LOGIC_ID\", \"setWebhook\", \"AGENT_KEY_ENCRYPTION_SECRET\", \"roll back the launchpad\", \"move the launchpad host\"; and for \"the explorer is down\", \"the explorer shows old agents\", \"agent index\", \"explorer index is stale\", \"verify an agent\", \"admin/sync\", \"explorer rollback\". Runbooks: read-only check first, GATE on any change. If \"account not found\" or \"faucet_unavailable\" shows in several products, or old agents appear after a wipe or upgrade, use moi-devnet-reset first and return if it shows no reset. Elsewhere: the hosted MCP server (moi-mcp-ops), a recorded test pass (moi-devrel/test-round)."
---

# MOI Agent Launchpad: operations

## What this covers
Running the Launchpad: ship a change, change a setting or secret, apply a database migration, check health, troubleshoot, roll back, answer users, and recover secrets before a host move. Production is a Docker container on a DevOps VM, deployed by GitHub Actions when a PR merges to `master`, with Supabase for data and MOI devnet for chain state. Facts are as of 2026-10-03.
Branch `explorer` (`explorer/GUIDE.md`): running the Agent Explorer, the public directory of agents on the on-chain registry. Health, ship a change, change a setting, bring its index back in step with the registry, verify agents, roll back.
Who owns the Launchpad is not settled. Whether DevRel owns it: ASK: Rahul. The previous operator wrote 301 of its 338 commits (his handover file `DEPENDENCIES.md` is local to his machine: ASK: Adithya for a copy). Only DevOps can act on the VM, DNS, TLS and the image registry: Upendhar holds them, and which of Upendhar or Srikar owns this VM today is unknown. No VM access is recorded for the operator, so every VM step is a message to DevOps.
Not covered: what to redo in every product after a devnet reset is `moi-devnet-reset`; a recorded test pass is `moi-devrel/test-round` (the Launchpad case list is `moi-devrel/test-round/references/launchpad-pass.md`); commits, PRs, merges and git identity are `moi-devrel/ship`; drafts of messages to DevOps or the protocol team are `moi-devrel/templates/messages.md`; the MCP server is `moi-mcp-ops`; the Launchpad's search and AI-visibility layer is `moi-docs/geo`; where Launchpad docs belong is `moi-docs`. The Voyage explorer (voyage.moi.technology) is a different product with no skill in this library: ASK: Gokul.

## Before you start
`SKILLS`, "the operator", "the previous operator" and `ASK: <person>` are defined in `moi-devrel/SKILL.md`. Run every command from your working copy of `sarvalabs/moi-agent-launchpad`, with paths quoted. The health script works from any folder. An Explorer job starts at `explorer/GUIDE.md`, which has its own checklist; this one is for the Launchpad. Terms used below: KMOI is the native token, measured in anu (1 KMOI is 1,000,000,000 anu); pm2 keeps an agent running on a user's computer; GHCR is GitHub's container registry; Teleport is the access tool the GitHub workflow uses to reach the VM; BotFather is Telegram's tool for managing a bot. More in `moi-devrel/references/glossary.md`.
- [ ] `SKILLS` set, and the repo checked out (private; access: ASK: Rahul). From inside it, run `bash "$SKILLS/moi-devrel/scripts/preflight.sh"` before any commit.
- [ ] One line on what is wrong or what should change, and whether users see it now. The operator provides. Ask: "What is wrong, or what should change, and who is affected?"
- [ ] `gh` signed in with the work login, with write access to the repo. Push to a fork or to the org repo: ASK: Rahul. A push to `master` or to `feature/moi-agent-launchpad-cicd`, or a manual workflow run, deploys. A push to any other branch does not.
- [ ] A notes folder that git cannot publish, made in the working copy: `mkdir -p launchpad-notes && printf '*\n' > launchpad-notes/.gitignore` (the folder ignores itself). Notes can name accounts and people. Copy a template into it with `cp "$SKILLS/moi-launchpad-ops/templates/incident-note.md" "launchpad-notes/incident-<YYYY-MM-DD>-<slug>.md"` or `cp "$SKILLS/moi-launchpad-ops/templates/change-checklist.md" "launchpad-notes/change-<YYYY-MM-DD>-<slug>.md"`.
- [ ] Who to ask: VM, DNS, TLS, the image registry (GHCR): Upendhar. The agent registry id and chain facts: Gokul. Product calls: Rahul. Who approves a merge to `master` is not on record: ASK: Rahul. History and accounts the previous operator holds (Telegram bot, Groq, Reown, Supabase login): Adithya. Channels and message style: `moi-devrel/references/people-and-teams.md`, and the drafts in `moi-devrel/templates/messages.md`; the DevOps channel is not fixed.

## The run: first five minutes, then the right runbook
This run is for the Launchpad. A report about the Explorer (agents.moi.technology, the directory of agents) goes to `explorer/GUIDE.md` at step 4, and that guide's run table takes over.
| # | Step | What to do | Done when |
|---|---|---|---|
| 1 | Measure | `bash "$SKILLS/moi-launchpad-ops/scripts/launchpad-health.sh"` (add `--with-rpc` to read the devnet node too). Read-only | A `RESULT:` line with the UTC time |
| 2 | Read the lines | `references/health.md` explains each. A WARN is a finding, not a pass. Chain figures swing: run it again after 30 seconds, not in a loop (each run makes a live registry read, and the chain listing failed with "Too many requests" after a burst of runs on 2026-10-03) | Each line has a cause or a reason to ignore it |
| 3 | Check the pipeline | `gh run list -R sarvalabs/moi-agent-launchpad -L 5`. Did a deploy just run or fail? | You know whether production is old |
| 4 | Find the row | Match what you see in the tables below, open that file, run its read-only check first. An Explorer report goes to its branch row | You hold a cause or an ASK |
| 5 | Stop users if needed | A wrong `card_uri` on a new agent, polls returning 502 or 504, a restart loop, or a webhook error that keeps advancing: stop taking new users, then `references/rollback.md`. The app has no switch that closes sign-ups (none found in the code read on 2026-10-03), so stopping means the operator sends no one to the site and asks DevOps whether they can block it. ASK: Upendhar, Rahul | The operator has decided |
| 6 | Change | Only through the runbook, one GATE at a time, each with the operator's yes naming the action | Each GATE has a yes written in the notes |
| 7 | Verify | The health script again, then the runbook's own check | Same as before the change or better |
| 8 | Record | Fill the copy of `incident-note.md` (a failure) or `change-checklist.md` (a change) made in "Before you start" | The note exists |
| 9 | Hand back | The format at the end of this file | The operator has read it |

## Which file to read
The Launchpad's own files (paths relative to this folder):
| You see or are doing | Read |
|---|---|
| "The site is down", 5xx, a red deploy run, a user error message, `account not found`, `faucet_unavailable`, agents that fail to register, Telegram silent | `references/troubleshoot.md` (28 rows by symptom) |
| Checking health, what a script line means, `chainStatus` | `references/health.md` |
| Shipping a code change, a manual workflow run | `references/ship-a-change.md` |
| Changing a variable or secret, rotating the Telegram webhook secret | `references/settings-and-secrets.md` |
| A new migration, "is migration N applied" | `references/database.md` |
| A bad deploy, the stop-and-rollback triggers | `references/rollback.md` |
| A user asks something | `references/support.md` |
| Moving or rebuilding the host, a lost VM, a handover of secrets | `references/host-move.md` |
| What runs where, the deploy path, who owns what, which docs are wrong | `references/architecture.md` |
| Before you trust any number or rule | `references/traps.md` |
| A devnet reset | `moi-devnet-reset`; the Launchpad-only steps are in `references/troubleshoot.md` ("when the cause is a reset") |
| A full recorded test pass | `moi-devrel/test-round/references/launchpad-pass.md`, with the method in `moi-devrel/test-round/GUIDE.md` |
| Testing a change to this skill | `evals/evals.md` |

The branch (asked to do X, read the guide, then follow its own table):
| Asked to do | Read |
|---|---|
| "The explorer is down", a 5xx on agents.moi.technology or its API, a red Agent Explorer deploy run | `explorer/GUIDE.md` |
| "The explorer shows old agents", the directory is small, `/admin/sync` is 404, the index is out of step with the registry | If it began after a wipe, a new registry id or a network upgrade, run `moi-devnet-reset` first (`bash "$SKILLS/moi-devnet-reset/scripts/reset-detect.sh"` only reads) and return here if it shows no reset. Then `explorer/GUIDE.md` |
| Mark an agent verified, or say what "verified" means | `explorer/GUIDE.md` |
| Ship, configure or roll back an Agent Explorer change; test its health script | `explorer/GUIDE.md` |

## Facts that fail silently
1. **Merge is deploy, with no test and no alert.** A red run leaves the old image serving. Watch `gh run list` after every merge (on 2026-09-14 every run after PR #24 failed at `npm ci` until PR #27 merged five minutes later, and production kept the image from before PR #23).
2. **Success is the receipt.** Activation said "ready" while the chain reverted it (a grant under the 1 KMOI floor; fixed by PR #30 on 2026-09-15). Simulation and a broadcast prove nothing.
3. **`/api/stats` after idle says `stale`** because the refresh runs only on request. Read twice, 30 seconds apart. Chain figures also swing between reads (2026-10-03): quote none without its time.
4. **`AGENT_KEY_ENCRYPTION_SECRET` is never rotated.** No vault holds it and GitHub secrets are write-only. A different value makes every stored agent key unreadable.
5. **Rotating `TELEGRAM_WEBHOOK_SECRET` without `setWebhook`** stops delivery with no error.
6. **`NEXT_PUBLIC_*` is baked at build** and `NEXT_PUBLIC_APP_URL` is permanent in every on-chain card.
7. **`deploy.yml` writes a fixed list into `.env`.** A name it does not list never reaches the app.
8. **The default marketplace listing is a database index.** Use `?source=chain` to test the chain. `onchain: null` means unavailable, not unlisted.
9. **Several repo documents are wrong** (README deploy text and its "payments are always on" line, `DEPLOY.md`, parts of `docs/HANDOFF.md`). Trust the workflow files, then the code. The list is in `references/architecture.md`.
10. **Payments are probably off in production** (`lib/payments.ts` defaults off and nothing sets the switch). Do not promise paid agents.
All Launchpad traps with their incidents: `references/traps.md`. The Explorer's are in `explorer/GUIDE.md`.

## Gates (an explicit yes in this conversation, naming the action)
Every run table has a Gate column. `read-only` and `local` need no yes. `GATE` needs the yes below. `OPERATOR` means the operator types it and Claude never sees a secret value. The Explorer branch inherits these and adds its own.
- Push a branch, open or update a PR, merge to a deploy branch (`master` here, `main` for the Explorer; say "this deploys to production"), run the workflow by hand.
- Set or change an Actions secret or variable. The operator types secret values at a hidden prompt.
- Run a migration or any write to the production database. Claude does not run SQL against production.
- Re-run `setWebhook`, restart or change anything on the VM (a message to DevOps), send any message to DevOps, the protocol team or users. Claude drafts, the operator sends.
- Spend devnet funds, deploy a contract or create wallets. Wallet and recovery-phrase steps are performed by the operator; Claude never handles a phrase, including a throwaway one.
- Switch the git or `gh` identity; download a file (name, source, size first). `npm ci` and `supabase start` download packages and images: say what and from where before the first run in a working copy. No AI co-author line or footer on commits or PRs.
- Upload or share a file in cloud storage (a note from `launchpad-notes` can name accounts and people).
A yes covers the one action it names. Details: `moi-devrel/references/consent-and-identity.md`.

## Keys and access
Names only. Where each lives, who grants it and its status: `moi-devrel/references/keys-and-access.md` (Launchpad rows); the full list with rotation rules: `references/settings-and-secrets.md`. The Explorer's names: `explorer/references/settings-and-secrets.md`.
- GitHub work login with write access; a repo admin to edit Actions secrets and variables (admin list for this repo not on record: ASK: Rahul).
- The Supabase project named by `SUPABASE_URL`, its dashboard login and SQL editor (owner unknown: ASK: Adithya, Rahul); `SUPABASE_SERVICE_ROLE_KEY`.
- `AGENT_KEY_ENCRYPTION_SECRET` (never rotate), `SESSION_SECRET`, `CRON_SECRET`, `TELEGRAM_WEBHOOK_SECRET`, `TELEGRAM_BOT_TOKEN` (BotFather, `moinetworkbot`, Adithya), `GROQ_API_KEY`.
- `MOI_REGISTRATION_MNEMONIC_1` to `_3` (DevOps), `MOI_PLATFORM_MNEMONIC`, and the operator's own sponsor and deployer wallets for the one-off scripts.
- `GHCR_PAT`, `TELEPORT_PROXY`, `TELEPORT_JOIN_TOKEN`, `VM_HOST`, `VM_USER`: DevOps only.
- Names the code reads that the keys file does not list are in `references/settings-and-secrets.md`: ASK: Rahul to add them.

## Hand-back
```
Produced: <what, with the PR number, run id or note path>
Health: before <RESULT line>, after <RESULT line>
Not undone or not verified: <say so, or "none">
Open ASK lines: <each with the person>
Ready: yes or no, because <one reason>
Next steps: <one to three>
```
A status message lists only work that was done. Planned work is labelled as a to-do. An Explorer job uses the hand-back in `explorer/GUIDE.md`.
