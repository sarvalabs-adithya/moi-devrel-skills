# Traps: ways this product fails with no error

Each row is a rule and the real thing behind it. Dates are when it was seen. The top rows are repeated in `../SKILL.md`. Facts are as of 2026-10-02 (research) and 2026-10-03 (live reads); the sync method and the VM facts were corrected on 2026-10-13 from `project-handover-docs/MCP-SERVER.md`. Back to `../SKILL.md`.

## The deploy path

| Rule | Evidence |
|---|---|
| Merging in `sarvalabs/moi-mcp` deploys nothing. Production is a copy in `sarvalabs/voyage-api` (branch `feat/moi-mcp`, folder `moi-mcp/`) that a person deploys by hand | The research (2026-10-02) found the live server to be the 2026-09-23 sync; it showed the same surface on 2026-10-03, with master at 2026-09-24. Production runs master `3ae48cc0` since the 2026-10-14 deploy (`architecture.md`) |
| Open the sync PR against `feat/moi-mcp`, not `develop` | PRs #310 to #313 and #320; `project-handover-docs/MCP-SERVER.md` |
| The `moi-mcp/` folder is a git subtree, updated with `git subtree pull --prefix=moi-mcp moi-mcp-upstream master` (steps: `ship-a-change.md` Part B) | The Voyage team's gateway runbook, shared 2026-10-13. Before that the method was written nowhere |
| The Voyage workflow passes a fixed list of variables and has no `.env`. It does not read `ecosystem.config.cjs` | It passes `WC_PROJECT_ID`, `PUBLIC_URL`, `MOI_NETWORK`, `MOI_DATA_DIR`, `HOSTED_PORT`, `LOG_LEVEL`, `NODE_ENV` and, for the read gateway, `MOI_RPC_URL`. `MOI_READ_CALLER` is also passed since voyage-api #323 (2026-10-14). `MOI_SESSION_KEY`, `MOI_AGENT_REGISTRY_LOGIC_ID` and `MOI_LAUNCHPAD_URL` are not passed. voyage-api holds `MCP_DEV_SESSION_KEY`, `MCP_PROD_SESSION_KEY` and `MCP_PREVIEW_SESSION_KEY` (created 2026-10-09); nothing passes them yet |
| A sync that makes another variable mandatory crash-loops the write gateway until the workflow passes it | Inferred from `docs/handoff-infra.md` plus the workflow |
| Every Voyage deploy is `pm2 delete` then `pm2 start`: a short outage, and consents and signing calls in flight are lost. It touches only `moi-mcp-read` and `moi-mcp-write` | The workflow file (research); `project-handover-docs/MCP-SERVER.md` |
| On the self-hosted guide, restart the write gateway, never reload, and keep one instance. Two copies fight over the WalletConnect relay identity and a code issued by one is unknown to the other | `ecosystem.config.cjs`, `docs/handoff-infra.md` |
| Never deploy an unmerged branch to the box | `docs/handoff-infra.md` |
| Opening a PR in voyage-api deploys a preview on the dev VM | `moi-mcp.preview.yml` runs on every PR |
| `npm audit` is non-blocking on purpose: a known advisory comes through js-moi-sdk and the server never uses it for key material | `ci.yml` comment |
| Node differs by place: the VM runs 20.14.0, CI tests 20, 22 and 24, the deploy builds on 22 | Workflows (research) |

## Docs that are wrong
Trust the workflow file first, then the code, then prose.

| Rule | Evidence |
|---|---|
| `docs/handoff-infra.md` names the repo `sarvalabs-adithya/moi-mcp` and the host `mcp.moi.technology`. Neither is real. `README.md` and `docs/deploy-checklist.md` give the same repo name in their clone lines, and `docs/deploy-vm.md` uses the same host | The repo is `sarvalabs/moi-mcp`; the name `mcp.moi.technology` did not resolve on 2026-10-03 |
| The README says the hosted server lists 13 tools while its own table lists 28 | Read 2026-10-03 |
| `HANDOFF.md` is dated 2026-09-01, `READY-TO-TEST.md` too, and `docs/deploy-vm.md` is superseded by `docs/handoff-infra.md`. `docs/deploy-voyage.md` covers the read gateway only | Read 2026-10-03 |
| `docs/deploy-checklist.md` wants about 20,000 KMOI for the test asset. That predates v0.13.0 | `MIN_STORAGE_FUND` is 7 KMOI on master |
| `.env.example` still gives the wiped registry id's prefix as the default registry | Read 2026-10-03 |
| `docs/publishing.md` says to create the GitHub repo. It exists | Read 2026-10-03 |

## What the live server says

| Rule | Evidence |
|---|---|
| `/health` ok does not mean registry reads work | `moi_resolve_agent` failed on every host with health ok (2026-10-02 and 2026-10-03) |
| Every build reports version 0.1.0. Identify a build by its tool count and behaviour | Probes 2026-10-03 |
| `ping` says `readOnly` true on the write gateway. Read the kind from `/health` | Probe 2026-10-03 |
| The hosted read gateway talks to the `/babylon/` RPC path, the code default is `/devnet/`. Both answered 0.13.0. Whether they are one chain is unknown | Research and probe. ASK: Gokul |
| Production serves the OAuth metadata in the form before PR #18, dev in the new form | Probes 2026-10-03 |
| After a reset the registry id, `MOI_READ_CALLER` and the canary account go stale. Three repos pin the registry id separately and drifted 7 to 12 days after 2026-09-11 | `moi-devrel/references/devnet.md` |

## The automatic checks

| Rule | Evidence |
|---|---|
| A green canary says nothing about the hosted server, the registry, OAuth or a phone | The canary ran green 2026-10-01 to 03. The registry read failed when read on 2026-10-02 and 2026-10-03 |
| The canary once passed while asset creation was broken, because it asserted acceptance and not receipt status 0. Its header comment still describes the old rule | Research; file read 2026-10-03 |
| After a reset the canary's sender account can vanish, and the nightly workflow does not pass `MOI_CANARY_ACCOUNT` | `chain-canary.yml` |
| A green watch run does not prove go-moi and cocolang were read. A missing `UPSTREAM_READ_TOKEN` is a log warning only | `upstream-watch.mjs`. The only issue ever filed is #17 |
| The watch reads GitHub Releases, newest only, and files one issue per exact title | `upstream-watch.mjs` |
| js-moi-sdk is pinned exactly at 0.9.0-rc2. rc3 is a GitHub release only, so Dependabot cannot offer it | Issue #17; npm read 2026-10-03 |
| Scheduled runs start 12 to 26 minutes after their cron time | Run list 2026-10-01 to 03 |
| Nothing from Dependabot merges by itself. A person reads an SDK bump | `dependabot.yml` |

## Wallet, writes and claude.ai

| Rule | Evidence |
|---|---|
| Prove a write by its receipt, not its broadcast. Simulation accepted a fuel price of 1 that the chain refused, and a storage fund written before KMOI had decimals | Upstream issue 7; PRs #13 and #15 |
| The wallet's combined sign-and-send crashes its own database, so the server asks the phone to sign and broadcasts itself. The phone cannot show what it signs, so the chat preview carries the numbers | `docs/upstream-issues.md` sections 1 and 6 |
| claude.ai needs the protected-resource `resource` to equal the URL typed, `/mcp` included. It never shows the QR image. Its users share one egress range, so a per-address limit of 10 a minute locked everyone out. A shared browser needs a consent that lets a second person start as themselves | PRs #18, #19, #20, 2026-09-23 |
| The identity is the `moi_uid` cookie. A different browser is a new identity and a new pairing | `docs/deploy-checklist.md` |
| A pairing lasts a week, or 15 minutes or one approval with `remember: false`. A confirm token lasts 10 minutes and works once | README |
| The faucet funds only accounts that already exist. The payout is quoted as 20K and as 100K KMOI | `moi-devrel/references/devnet.md` |
| The Reown project behind `WC_PROJECT_ID` has no known owner. Losing the id stops pairing | Research |
| No phone check of the write path is recorded after 2026-09-01 | `docs/testing-plan.md` |

## Packaging and people

| Rule | Evidence |
|---|---|
| `npx -y @moi-protocol/mcp-server` fails. Nothing is published and the name is undecided | npm read 2026-10-03 |
| A pushed tag matching `v*` publishes to npm | `publish.yml` |
| Unpushed work exists only on the previous operator's machine (not recorded, the previous DevRel's notes; ASK: Rahul), and file paths differ there (a restructure moves the registry module). Read GitHub's `master`, not that clone's working branch | 19 commits ahead on 2026-10-03, and still growing |
| Do not push, open a PR, comment on or close an issue without an explicit yes: each notifies maintainers of a public repo | `moi-devrel/references/consent-and-identity.md` |
| GitHub secrets cannot be read back and no vault exists | `moi-devrel/references/keys-and-access.md` |
| Never claim a fix works without a live check and a receipt | `moi-devrel/references/devnet.md`, "Silent failures on devnet" |
