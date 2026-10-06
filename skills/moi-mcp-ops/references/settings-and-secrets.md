# Settings and secrets, by name

Names only. This file never holds a value. Facts are as of 2026-10-02 (research: the Voyage workflow, `docs/handoff-infra.md`, `.env.example`) unless dated. Where each credential lives and who grants it: `moi-devrel/references/keys-and-access.md`. Back to `../SKILL.md`.

Rules. Never open an `.env` file and never paste a value into chat, a file or a commit. GitHub secrets cannot be read back. The Voyage deploy has no `.env` at all: it passes values inline when it starts the processes, so the only copy of a value is in GitHub or in the running process. If a value is pasted anyway, do not repeat it, say it is exposed, and name who can rotate it. Rotation labels used below: **free** (no side effect), **step** (a follow-up is needed), **never**.

## Passed by the Voyage workflow (`moi-mcp.deploy.yml` in `sarvalabs/voyage-api`, branch `feat/moi-mcp`)

| Name | Kind | Where it comes from | What it does, and what goes wrong |
|---|---|---|---|
| `WC_PROJECT_ID` | secret | voyage-api secrets `MCP_PROD_WC_PROJECT_ID` and `MCP_DEV_WC_PROJECT_ID` | The Reown (WalletConnect) project id, a public identifier of 32 hex characters. The write gateway refuses to start without a valid one. Wrong: pairing does nothing ("The WalletConnect relay refused the pairing"). Owner of the Reown project: unknown, ASK: Rahul. Effect of replacing it on live pairings: unknown, ASK: Adithya |
| `PUBLIC_URL` | plain, inline | The `pm2 start` line | Must equal the public host exactly. It is the OAuth issuer, and an `http://` value drops the cookie. Wrong: sign-in loops. Changing the host means every connector is added again (inferred) |
| `MOI_NETWORK` | plain, inline | Same | `voyage` today. `custom` also needs `MOI_RPC_URL` or `/health` answers 503 |
| `MOI_DATA_DIR` | plain, inline | Same | Where the write gateway keeps sign-ins, tokens, pairings and the journal. Losing it signs everyone out |
| `HOSTED_PORT`, `LOG_LEVEL`, `NODE_ENV` | plain, inline | Same | Listen port of the write gateway, log level, Node mode |
| `MOI_RPC_URL` | plain, read gateway only | Same | The `/babylon/` path of `dev.voyage-rpc.moi.technology`. The code default is `/devnet/` |

## Read by the server and NOT passed by that workflow (defaults apply, or the feature fails)

| Name | Needed when | What it does | Rotation |
|---|---|---|---|
| `MOI_READ_CALLER` | Required on devnet for registry reads | Any account that exists on the network, used as the caller of read-only logic simulation. Unset: registry tools fail with an error that names it | free. Must be re-chosen after a reset |
| `MOI_AGENT_REGISTRY_LOGIC_ID` | After a reset, unless the code default is changed | Overrides the registry id; the default is `DEFAULT_REGISTRY_LOGIC_ID` in `src/moi/registry.ts` | The one value that changes on a reset |
| `MOI_SESSION_KEY` | Local branch only: not read by `master`. Required on the write gateway once the unmerged work on the previous operator's machine is synced (ASK: Adithya for a copy) | A server-side key. Generate with `openssl rand -base64 32`, put it in the secret store and never print it | **step**: changing it signs users out of what uses it, and there is no previous-key setting |
| `MOI_LAUNCHPAD_URL` | Launchpad tools | Must equal the Launchpad's own `NEXT_PUBLIC_APP_URL` or the tool refuses to sign | free |
| `REDIS_URL` | Optional | Moves pairings to Redis. It carries a password. Unreachable at boot: the write gateway refuses to start. Not in `moi-devrel/references/keys-and-access.md`: ASK: Rahul to add it | step |
| `HOSTED_TIMEOUT_MS` | Optional | Budget for one hosted tool call, default 240000. Above 300000 claude.ai abandons calls the server still serves | free |
| `MOI_EXPLORER_URL`, `PORT` (read gateway), `MOI_MCP_HOME` and `REQUEST_TIMEOUT_MS` (local server), `MOI_WC_PARAM_STYLE` | Optional | Explorer links, the read gateway port, local state folder, local phone-wait budget. Leave `MOI_WC_PARAM_STYLE` unset | free |

## GitHub-side names

| Repo | Name | Used by | Owner |
|---|---|---|---|
| `sarvalabs/moi-mcp` | `UPSTREAM_READ_TOKEN` | The upstream watch, for go-moi and cocolang | Unknown, expiry unknown. ASK: Adithya |
| `sarvalabs/moi-mcp` | `NPM_TOKEN` | `publish.yml` on a `v*` tag. Unused so far | ASK: Rahul |
| `sarvalabs/voyage-api` | `TELEPORT_PROXY`, `TELEPORT_JOIN_TOKEN`, `MCP_DEV_MACHINE` (dev); `TELEPORT_PROD_PROXY`, `TELEPORT_PROD_JOIN_TOKEN`, `MCP_PROD_MACHINE` (production) | The deploy workflow reaches the VM | DevOps, Upendhar |
| `sarvalabs/voyage-api` | `MCP_DEV_WC_PROJECT_ID`, `MCP_PROD_WC_PROJECT_ID` | Source of `WC_PROJECT_ID` | Who may edit the `production` environment: ASK: Srikar |
Test-only names: `MOI_E2E` (switches on the live canary, set to 1 in the nightly workflow) and `MOI_CANARY_ACCOUNT` (the canary's sender; **not passed** by the nightly workflow).

## Runbook: change a setting or a secret (Voyage-hosted)

| # | Step | Do this | Done when | Gate |
|---|---|---|---|---|
| 1 | Read what is passed today | Open the workflow in the GitHub UI, or `gh api -H "Accept: application/vnd.github.raw" "repos/sarvalabs/voyage-api/contents/.github/workflows/moi-mcp.deploy.yml?ref=feat/moi-mcp"` (private repo: needs access, ASK: Rahul). Names only matter; the research found no value in the file. Copy no host, address or login you see into a note | You know if the name is passed | read |
| 2 | Decide the kind | A secret (a value nobody should see) or a plain value written inline in the workflow | One of the two | read |
| 3a | A secret | The operator sets it, typing the value at a hidden prompt: `gh secret set <NAME> --env production -R sarvalabs/voyage-api`. The research names the `production` environment; the name of the dev one is not recorded, ASK: Srikar. Claude never sees the value. Who may edit it: ASK: Srikar | Set | GATE |
| 3b | A plain value | Edit the `pm2 start` environment in `moi-mcp.deploy.yml` on `feat/moi-mcp`: a PR into that branch, then merge. Merging deploys nothing | Merged | GATE |
| 4 | Deploy dev, then production | `ship-a-change.md` parts C and D. Only variables the workflow passes reach the processes | Both runs green | GATE |
| 5 | Verify | `bash "$SKILLS/moi-mcp-ops/scripts/mcp-health.sh"`: the OAuth issuer must equal `PUBLIC_URL`; if it says `http://localhost` the environment never reached the process. Then the behaviour the variable controls | The behaviour changed as intended | read |

## Runbook: the MCP part of a devnet reset
The cross-product order is `moi-devnet-reset`. The server reads the registry id, a read caller and SDK constants from the chain; three repos (Launchpad, Explorer, this server) pin the registry id separately and drifted by up to 12 days after 2026-09-11 (`moi-devrel/references/devnet.md`).

| # | Step | Do this | Done when | Gate |
|---|---|---|---|---|
| 1 | Confirm | The script: the RPC line, and the `moi_resolve_agent` WARN with "account not found" | Reset signature seen | read |
| 2 | Get the facts | One message to the protocol team: new registry id, whether agents were re-imported, new SDK versions, whether KMOI's id, the fuel floor or the RPC path changed. Claude drafts, the operator sends. ASK: Gokul | Answer in hand | GATE |
| 3 | Check the id before use | `moi_get_logic` for the new id through the read gateway: it must list the registry routines the code calls (`RegisterAgent`, `GetAllAgentIds`, `GetAgentsByOwner`, `GetAgentProfile`, `SetAgentStatus`, `TransferAgent`, `GetAgentCount`; read from `src/moi/registry.ts` and `src/tools/registry-writes.ts` on `master`) | Routines listed | read |
| 4 | Point the server | Either pass `MOI_AGENT_REGISTRY_LOGIC_ID` and `MOI_READ_CALLER` from the workflow (a PR; the workflow passes neither today), or change `DEFAULT_REGISTRY_LOGIC_ID` in `src/moi/registry.ts` by PR to master (commit `731a808`, 2026-09-24 UTC, did this for the September registry and is already on `master`; production still lacks a sync, a deploy and a `MOI_READ_CALLER`) and sync. `MOI_READ_CALLER` needs the first route either way | PR merged | GATE |
| 5 | SDK constants | If KMOI's id, the fuel floor or the storage fund moved, take the grouped SDK PR (a merge: GATE) and run the canary (`watch-and-canary.md`; the install is a download: GATE); set `MOI_CANARY_ACCOUNT` if KMOI's creator is gone (the nightly workflow does not pass it, so that is a workflow PR: GATE) | Canary green | GATE, then local |
| 6 | Deploy and verify | `ship-a-change.md` parts B to D, then `moi_resolve_agent` returns an agent | The script shows no registry WARN | GATE |
| 7 | Close out | Grep the id across the three repos; update the stale comment in `.env.example` (it still names the wiped id's prefix as the default) | One id everywhere | local |

## Not yet known
- Who owns the Reown project and `UPSTREAM_READ_TOKEN`. ASK: Rahul, Adithya.
- Which Voyage environment holds `MOI_READ_CALLER` today, if any. ASK: Srikar.
- Whether editing the voyage-api `production` environment needs an approval rule. ASK: Srikar.
