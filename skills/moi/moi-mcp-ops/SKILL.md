---
name: moi-mcp-ops
description: "Run the MOI MCP server (sarvalabs/moi-mcp; as of 2026-10-14 live at mcp.voyage.moi.technology and mcp-read.voyage.moi.technology) in production. Check its health and find why it is down, ship a change to it, add the claude.ai connector and prove each class of tool once, triage the \"Upstream release\" and \"Chain canary failing\" issues, change a setting, roll back, and answer the npm and registry questions. Use for \"the MCP is down\", \"MOI MCP health\", \"MCP connector\", \"add the MOI connector to claude.ai\", \"Deploy MOI MCP Gateway\", \"voyage-api sync\", \"sync subtree\", \"moi-mcp deploy\", \"Chain canary failing\", \"Upstream release\", \"roll back the MCP\", \"publish moi-mcp to npm\". If the failure may be a devnet reset (\"moi_resolve_agent account not found\", \"Could not load the MOI agent registry\"), use moi-devnet-reset first. A recorded connector test pass with a log is moi-devrel/test-round, pull requests are moi-devrel/ship, the Launchpad and Explorer are moi-launchpad-ops, and posts are moi-blog."
---

# MOI MCP ops

## What this covers
The MOI MCP server lets a chat assistant such as claude.ai read MOI and propose writes that the user's phone wallet signs. The server holds no key. This skill checks its health, ships a change, connects the connector and proves each class of tool, triages the two automated issue sources (the daily upstream watch and the nightly chain canary), changes a setting, rolls back and keeps the publishing questions in one place. Facts are as of 2026-10-03 unless dated; the deploy path, the VM facts, the owners and the PR states were corrected on 2026-10-13 and the production state on 2026-10-14 (production runs moi-mcp master `3ae48cc0`: 33 tools, 43 read tools) from `project-handover-docs/MCP-SERVER.md` in the handover repo, which wins where the two differ.
**Woken by "the MCP is down"?** Run step 1 of The run, which is one read-only command, then open the row of `references/troubleshoot.md` that matches its first FAIL.
Not covered: the other chain products (`moi-launchpad-ops`, and its branch `moi-launchpad-ops/explorer`); the cross-product order after a devnet reset (`moi-devnet-reset`: use it first when the failure may be a reset, and come back here if its reads show none; this skill holds the MCP rows only); a recorded test pass with a plan and a log (`moi-devrel/test-round`, whose case list for this connector is `moi-devrel/test-round/references/mcp-pass.md`; this skill proves the connector once, as part of operating it); commits, pull requests and merges in general (`moi-devrel/ship`); posts and announcements (`moi-blog`); checking claims (`moi-devrel/claim-check`); messages to the Voyage team, DevOps or the protocol team (`moi-devrel/templates/messages.md`, checked with `moi-devrel/scripts/check-message.py`); house rules, people and keys (`moi-devrel`).

## Before you start
`SKILLS`, "the operator", "the previous operator" and `ASK: <person>` are defined in `moi-devrel/SKILL.md`. Set `SKILLS` to the folder that holds the `moi-*` skills and quote it. The health script runs from anywhere. For shipping, run each command from the working copy of the repo the step names (`sarvalabs/moi-mcp` or `sarvalabs/voyage-api`).
- [ ] The job in one line: health, ship, connect, triage, setting, rollback or publish. The operator provides. Ask: "What should be true at the end?"
- [ ] Tools: bash and python3 for the script; curl for the by-hand checks; Node 20 or later, git and `gh` for the rest. How to check and install them: `moi-devrel/references/environment.md`. The script was tested on Python 3.9.6 and 3.13.0; on a python.org build of macOS it falls back to the system CA list if Python ships none.
- [ ] GitHub access. `sarvalabs/moi-mcp` is public. `sarvalabs/voyage-api` is private and is needed to ship, deploy or roll back. ASK: Rahul who grants read and Actions access. Work identity: `moi-devrel/references/consent-and-identity.md`.
- [ ] For any write check: a phone with MOI Wallet and a funded devnet account. The operator provides both. Claude never handles a recovery phrase.
- [ ] Who can act on what. Which products DevRel owns: ASK: Rahul. The VMs (dev `voyagedev`, production `prod-voyage`), nginx, TLS, DNS and Teleport: DevOps; Srikar runs the Voyage VMs and the deploy workflow, Upendhar is the other DevOps contact (Claude never logs in to a VM). The deploy workflow lives in voyage-api, owned by the Voyage team; which people besides Srikar may run it: ASK: Srikar. The code: the previous operator wrote almost all of it; its owner now is not settled, ASK: Rahul. The registry id and read caller after a reset: ASK: Gokul. The Reown project: owner not recorded, ASK: Rahul. `UPSTREAM_READ_TOKEN`: not set on `sarvalabs/moi-mcp` as of 2026-10-10; Rahul decides which account owns it.
- [ ] Read `project-handover-docs/MCP-SERVER.md` first, and for the previous operator's 4 October snapshot `project-handover-docs/LIST-OF-DEPENDENCIES.md`. Unpushed branches on the previous operator's machine are not recorded (the previous DevRel's notes); ASK: Rahul.
- [ ] Product status. `project-handover-docs/MCP-SERVER.md` records no security finding for this product. The 2026-10-02 research note said one was open and its content is not recorded (the previous DevRel's notes); ASK: Rahul before touching sign-in or other admin code.

## The run
GATE marks a step that changes something: it needs the operator's explicit yes naming the action (see Gates).

| # | Step | What to do | Where or command | Done when |
|---|---|---|---|---|
| 1 | Measure | Read-only check of both gateways, the OAuth lines, the tool lists and the chain RPC | `bash "$SKILLS/moi-mcp-ops/scripts/mcp-health.sh"` (add `--env dev`, `--github`, or `--write-host H` for a PR preview) | Every FAIL is named, every WARN is explained. Exit 0 no FAIL, 1 a FAIL, 2 bad usage, 3 a script fault |
| 2 | Name the job | Pick the row of "Which file to read" | below | One reference file is open |
| 3 | Read first | Do the read-only checks the reference opens with, or step 1 again if it has none, and keep the output as the "before" reading | the reference | You can say what is live and what differs from master |
| 4 | Ask | For each GATE step state the exact action, the target and the consequence, then wait | `moi-devrel/references/consent-and-identity.md` section 1 | A yes naming that action. A yes covers one action |
| 5 | Change | One GATE at a time, in the order of the runbook. Merge is not deploy here | the reference | The step's own "done when" |
| 6 | Verify | Run step 1 again, then the connector classes the change touched, reads first | `references/connect-and-verify.md` | No FAIL. Every touched class has a pass or a named gap. A write is proved by its receipt |
| 7 | Record | Hand back in the block under Hand-back. For a new failure also add a row with the date, message, cause and fix | `references/troubleshoot.md` | The operator has read both |

## Which file to read

| Doing or seeing | Read |
|---|---|
| The site is down, a health FAIL, any symptom, what to tell a user | `references/troubleshoot.md`, then `references/health.md` |
| What is live, which repo deploys which, who owns what, the tool classes | `references/architecture.md` |
| Ship a change to production, sync into voyage-api, deploy dev or production | `references/ship-a-change.md` |
| Add the connector in claude.ai, prove reads, pairing and phone-approved writes | `references/connect-and-verify.md` |
| A recorded, repeatable connector pass with a plan and a log | `moi-devrel/test-round/GUIDE.md`, case list `moi-devrel/test-round/references/mcp-pass.md` |
| An "Upstream release" or "Chain canary failing" issue, or whether the watch is really watching | `references/watch-and-canary.md` |
| Change a variable or a secret, or the MCP part of a devnet reset | `references/settings-and-secrets.md` |
| A deploy went wrong | `references/rollback.md` |
| The npm name, the registry, directory listings, announcements | `references/publishing.md` |
| Every silent failure, with its evidence | `references/traps.md` |
| What each health line means, and the by-hand curl equivalents | `references/health.md` |
| Testing a change to this skill | `evals/evals.md` |

## Facts that fail silently

| Rule | The incident |
|---|---|
| Merging in `sarvalabs/moi-mcp` deploys nothing. Production runs a copy in `sarvalabs/voyage-api` and a person runs the deploy | The research found the live server to be the 2026-09-23 sync (2026-10-02) and it listed the same 13 tools on 2026-10-03, while master was at 2026-09-24; it stayed so until 2026-10-14, when master (`3ae48cc0`) was synced by voyage-api #320 and deployed to dev and production |
| `/health` ok does not mean the server works. Check a registry read | `moi_resolve_agent` failed on every host with health ok (2026-10-02, 2026-10-03), naming the registry wiped on 2026-09-11. Lookup answers since the 2026-10-14 deploy |
| A green canary does not prove the connector. It tests master against devnet, never the hosted server or the registry | The canary ran green on 2026-10-01 to 03. The registry read failed when read on 2026-10-02 and 2026-10-03 |
| A green upstream watch does not prove the private repos were read. A missing token is a log warning only | The only issue ever filed is #17 (js-moi-sdk); none exists for go-moi or cocolang |
| The Voyage workflow passes a fixed list of variables and has no `.env`. A sync that needs a new variable crash-loops the write gateway | Inferred from the workflow and `docs/handoff-infra.md`. `MOI_READ_CALLER` is passed since voyage-api #323 (2026-10-14); `MOI_SESSION_KEY`, the registry id and `MOI_LAUNCHPAD_URL` are not. voyage-api holds `MCP_DEV_SESSION_KEY`, `MCP_PROD_SESSION_KEY` and `MCP_PREVIEW_SESSION_KEY` since 2026-10-09; nothing passes them yet |
| Every deploy is a short outage and loses OAuth consents and phone signing in flight. Never run two write gateways or reload one | The Voyage workflow runs `pm2 delete` then `pm2 start` (research, 2026-10-02); the repo's `ecosystem.config.cjs` says why the write gateway stays one process |
| Prove a write by its receipt. Simulation accepts what the chain refuses | A fuel price of 1 simulated and bounced at broadcast (PR #15) |
| Every build says version 0.1.0 and `ping` says readOnly true on both gateways. Identify a build by its tool count and the OAuth metadata | Probes 2026-10-03 |
| claude.ai Connect needs the protected-resource `resource` to equal the typed URL with `/mcp`. Production showed the old form until 2026-10-14 | PR #18; probes 2026-10-03. The fix is live on production since 2026-10-14, so Connect no longer stalls |
| `mcp.moi.technology` does not exist and `npx -y @moi-protocol/mcp-server` fails | The repo's docs use both as examples. The name did not resolve and npm answered "Not found" on 2026-10-03 |
| The repo's docs go stale: trust the workflow file, then the code, then prose | `docs/handoff-infra.md` names the wrong repo and host; the README says 13 tools above a 28-row table |

## Gates
Nothing below happens without the operator's explicit yes in this conversation.
- Any push, pull request, comment, review request, merge or issue close in `sarvalabs/moi-mcp` or `sarvalabs/voyage-api`. Opening a voyage-api PR also deploys a preview.
- Running a workflow by hand: "Deploy MOI MCP Gateway" (dev, production or both), the watch dry run, the canary. A production deploy is a short outage.
- Setting a repository or environment secret or variable. The operator types a secret at a hidden prompt; Claude never sees it.
- Anything on a VM: a restart, an nginx or environment change, a log read. DevOps does it. Claude drafts the ask and the operator sends it.
- Spending devnet funds: every write through the connector (transfer, asset, mint, invoke, register). The operator's own wallet approves on the phone.
- Sending any message to the Voyage team, DevOps or the protocol team. Claude drafts, the operator sends.
- Publishing: pushing a `v*` tag (it publishes to npm), setting `NPM_TOKEN`, a directory submission, an announcement.
- Downloading: `git clone`, `git fetch`, `npm ci`, `npm pack`, installing a tarball. Say the name and the source first.
- Switching the git or `gh` identity. Sub-agents, unless the operator asks. An admin write on production.
- A yes covers one action. After a no, do not propose the same flow again.

## Keys and access
Names only; where each lives and who grants it is in `moi-devrel/references/keys-and-access.md` (status TBD until the owner settles access), and the MCP list with rotation rules is `references/settings-and-secrets.md`. Never open an `.env` file and never paste a value or a recovery phrase.
- Server settings: `WC_PROJECT_ID` (voyage-api secrets `MCP_PROD_WC_PROJECT_ID`, `MCP_DEV_WC_PROJECT_ID`), `PUBLIC_URL`, `MOI_NETWORK`, `MOI_DATA_DIR`, `MOI_RPC_URL`, `MOI_SESSION_KEY`, `MOI_READ_CALLER`, `MOI_AGENT_REGISTRY_LOGIC_ID`, `MOI_LAUNCHPAD_URL`, `REDIS_URL`.
- GitHub: `UPSTREAM_READ_TOKEN` and `NPM_TOKEN` on `sarvalabs/moi-mcp` (neither set as of 2026-10-10); the Teleport secrets and `MCP_DEV_MACHINE`, `MCP_PROD_MACHINE` on `sarvalabs/voyage-api` (DevOps); `MCP_DEV_SESSION_KEY`, `MCP_PROD_SESSION_KEY`, `MCP_PREVIEW_SESSION_KEY` there too (repo-level, created 2026-10-09, not passed by anything yet); `MOI_CANARY_ACCOUNT` for the canary.
- Missing from `moi-devrel/references/keys-and-access.md`: `REDIS_URL`, and who may edit the voyage-api `production` environment. ASK: Rahul to add them.
- Accounts: the Reown project at cloud.reown.com (owner unknown), the operator's MOI Wallet, and the claude.ai plan that allows custom connectors (unknown).

## Hand-back
```
Produced: <the health reading, PR, run id or note, with exact path or URL>
Checked: <script lines, connector classes passed, receipts>
Remaining: <numbered, each with who owns it>
Not verified or simulated: <phone writes not run, VM not read, registry still stale>
Ready: yes or no, because <one reason>
Next steps: <one to three>
```
Ready is yes only when the script shows no FAIL, every WARN is explained, and every class the change touched has a pass or a named gap. A status lists only work done; planned work is labelled as a to-do.
