# Architecture: the server, where it runs, what is live

Facts are as of 2026-10-03 where they were read live (probes, public GitHub and npm reads, `git` on a clone) and as of 2026-10-02 where they come from the ops research note ("the research" in this skill: it read the private `voyage-api` workflows, which could not be re-read on 2026-10-03). `ASK: <person>` is defined in `moi-devrel/SKILL.md`. Back to `../SKILL.md`.

## Where the files named in this skill live
Every file of `sarvalabs/moi-mcp` named in this skill is on `master` on GitHub (checked 2026-10-03). Exceptions: the two voyage-api workflows (private repo; on branch `feat/moi-mcp` only, not on its default branch `develop`; known from the research note and not re-read), `DEPENDENCIES.md` (a local file on the previous operator's machine, not in git; ASK: Adithya for a copy), and the unpushed branches listed at the end. Text that exists only on those local branches, such as the `MOI_SESSION_KEY` rows of the deploy guides, is marked "local branch only" wherever this skill uses it.

## What it is
MCP (Model Context Protocol) lets a chat assistant such as claude.ai call typed tools on a server. This server turns MOI reads and writes into tools. A write is two tool calls (a preview, then a confirm token), the user's phone wallet signs it, and the server holds no private key (README "Security model"). Source: `sarvalabs/moi-mcp` (public, default branch `master`, TypeScript, Node 20 or later). `package.json` names it `@moi-protocol/mcp-server`, version 0.1.0. The server calls the network `voyage` in its settings (the `MOI_NETWORK` value); say "devnet" in anything public.

Terms. KMOI: the devnet test currency (no real value). A logic: a MOI smart contract. The agent registry: an on-chain logic that lists AI agents; the server finds it by its logic id, and the id changes when devnet is reset. Voyage: MOI's explorer and faucet product, and the backend repo `voyage-api` that hosts this server's production copy. pm2: a Node process manager. nginx: the web server in front that ends TLS. Teleport: the tool DevOps uses to let a workflow reach a VM. OAuth: the sign-in protocol claude.ai uses; here the server is its own issuer. WalletConnect: the relay that carries signing requests to the phone. Reown: the company that runs it and issues the project id (`WC_PROJECT_ID`). A gateway is one of the two Node processes.

## Forms and hosts

| Form | Host | Sign-in | Tools live 2026-10-03 | Deployed by |
|---|---|---|---|---|
| Write gateway, production | `mcp.voyage.moi.technology`, connector URL ends `/mcp` | OAuth run by the server itself: no account, no password | 13 | Manual workflow "Deploy MOI MCP Gateway" in `sarvalabs/voyage-api`, target production |
| Read gateway, production | `mcp-read.voyage.moi.technology`, URL ends `/mcp` | None | 6 | The same workflow |
| Dev copies | `dev-mcp.voyage.moi.technology`, `dev-mcp-read.voyage.moi.technology` | Same as above | 13 and 6 | The same workflow, target dev |
| PR preview | `pr-<N>-mcp.preview.voyage.moi.technology` (research, 2026-10-02) | Same | Not read | `moi-mcp.preview.yml`, on every PR to voyage-api |
| Local server | The user's machine, `node dist/index.js` from a clone, started by a desktop client | No sign-in; a wallet pairing | Not read | The user |
| Self-hosted VM guide | `docs/handoff-infra.md` in the repo | Same | n/a | The evidence shows production does not use it |
| Read gateway image | `Dockerfile` in the repo, with a HEALTHCHECK | None | n/a | Not used by the Voyage workflow, which starts pm2 apps |
`mcp.moi.technology` does not exist (the name did not resolve on 2026-10-03). The repo docs use it as an example host: do not give it to anyone. The npm package is not published (below).

## Which repository deploys which

| Repository | Role | What a merge does |
|---|---|---|
| `sarvalabs/moi-mcp` (public) | The source. CI on Node 20, 22 and 24 (typecheck, tests, build, `node dist/cli.js help`, a packed-tarball start). Nightly canary, daily upstream watch, Dependabot | Nothing is deployed |
| `sarvalabs/voyage-api` (private, default `develop`), branch `feat/moi-mcp`, folder `moi-mcp/` | A copy of the server, plus the workflows `moi-mcp.deploy.yml` (manual) and `moi-mcp.preview.yml` (every PR) | A merged "sync subtree" PR changes the copy and deploys nothing. A person runs the deploy |
The production deploy job (research, from the workflow file): build on Node 22, tar `dist`, `package.json` and `package-lock.json`, copy to the VM through Teleport, `npm ci --omit=dev`, `pm2 delete` both apps, `pm2 start` both with the environment passed inline, `pm2 save`, then a health job. No `.env` is involved. Every deploy is a short outage. The VM runs Node 20.14.0, CI tests 20, 22 and 24.

## What is live (probes 2026-10-03)

| Fact | Value |
|---|---|
| Health | `ok` on all four hosts above (`/health`) |
| Tools | Write gateway 13: `ping`, `moi_get_account`, `moi_get_asset`, `moi_get_interaction`, `moi_get_logic`, `moi_resolve_agent`, `moi_connect_wallet`, `moi_wallet_status`, `moi_disconnect_wallet`, `moi_transfer`, `moi_create_asset`, `moi_mint`, `moi_call_logic`. Read gateway 6: the first six. Same on dev |
| Version | Every build answers 0.1.0, so the version cannot tell you which sync is live. Use the tool count and the behaviours below |
| Production build | The 2026-09-23 sync (voyage-api PRs #310 to #312, merged 15:57, 16:38 and 17:20 UTC), per the research of 2026-10-02; the 13-tool surface and old behaviours of 2026-10-03 agree. PR #18 landed in `moi-mcp` at 16:35 UTC the same day and production lacks it, so the live build may be the first sync, not the last (inferred; which sync: ASK: Srikar). Master has moved on: last commit `b38343d` on 2026-09-24 |
| Registry | `moi_resolve_agent` fails on every host with "Could not load the MOI agent registry (logic 0x20000000c684f926...) ... account not found". That is the wiped registry. Master's default (`src/moi/registry.ts`, commit `731a808`, 2026-09-24 00:00 UTC, pushed to GitHub master) is the redeployed one, so no host runs it (inferred) |
| OAuth metadata | Production names the bare origin as the protected resource and 404s the `/mcp` document, the form before PR #18 (commit `93d4d9d`). Dev serves the new form. So dev is newer than production, and Connect in claude.ai may still spin on production (inferred, untested: ASK: Adithya) |
| Chain RPC | `net.Version` answers 0.13.0 on both `/devnet/` and `/babylon/` paths of `dev.voyage-rpc.moi.technology`. The hosted read gateway is deployed with the `/babylon/` path, the code default is `/devnet/`. Whether they are one chain: ASK: Gokul |
| GitHub | `moi-mcp` has no git tag. Open PRs: #25 (Dependabot, 2026-10-01) and #4 (code review, since 2026-09-11). Open issue #17 (js-moi-sdk v0.9.0-rc3, since 2026-09-23). No `chain-canary` issue has ever been opened. voyage-api PR #313 (consent fix, registry and Launchpad tools) was open with no review on 2026-10-02: re-check |
| npm | `@moi-protocol/mcp-server` and `@sarvalabs/mcp-server` both return "Not found". The newest `js-moi-sdk` on npm is 0.9.0-rc2, which is what the server pins; rc3 is a GitHub release only |

## Tool classes
Master's README table lists 28 tools and the source adds three registry write tools the table omits (commit `2af858f`): 31 tool names in `src/` on 2026-10-03. Production lists 13.

| Class | Tools on master | Phone | On production |
|---|---|---|---|
| Health | `ping` | no | yes |
| Chain reads | `moi_get_account`, `moi_get_asset`, `moi_get_interaction`, `moi_get_logic` | no | yes |
| Registry reads | `moi_resolve_agent`, `moi_list_agents` | no | resolve fails (stale id), list absent |
| Wallet | `moi_connect_wallet`, `moi_wallet_status`, `moi_disconnect_wallet` | pairing tap | yes |
| Writes, preview then confirm | `moi_transfer`, `moi_create_asset`, `moi_mint`, `moi_call_logic` (invoke), `moi_create_account` | yes | all but `moi_create_account` |
| Registry writes | `moi_register_agent`, `moi_set_agent_status`, `moi_transfer_agent` | yes | absent |
| Launchpad | `moi_launchpad_templates`, `_sign_in`, `_status`, `_create_agent`, `_register_agent`, `_telegram_link`, `_setup_script`, `_sign_out` | sign-in is a message tap, register is a write | absent |
| Dapp | `moi_dapp_sign_in`, `_api`, `_call`, `_sessions`, `_sign_out` | sign-in is a message tap | absent |
`tools/list`, `ping` and the read tools need no token. Wallet and write tools answer 401 without one.

## The two gateways
- Read gateway: stateless, no wallet code, no secrets, any number of copies.
- Write gateway: exactly one process. OAuth authorization codes live only in memory, and one WalletConnect client holds the relay identity. Two copies, or a reload that overlaps old and new, break pairings and sign-in. A restart or a Voyage deploy loses consents and signing calls in flight.
- State of the write gateway, under `MOI_DATA_DIR` (files, mode 0600): `auth/clients`, `auth/tokens` (hashed), `auth/cookie-secret`, `sessions/` (one pairing per user), `journal.jsonl` (every write: proposed, signed, broadcast, confirmed, failed, orphaned), `wc-relay-scratch/`. Losing the cookie secret or the tokens signs everyone out; losing `sessions/` un-pairs every wallet; losing the journal loses audit history only. Optional Redis holds pairings instead (needs a password and persistence).
- Identity is a browser cookie, `moi_uid`. A different browser is a new identity and needs a fresh pairing.

## Ownership: what the evidence settles and what it leaves open
Which products DevRel owns is not settled. ASK: Rahul.

| Piece | Evidenced | Unknown, and who knows |
|---|---|---|
| `moi-mcp` code | `master` has 127 commits, the last on 2026-09-24 (`git ls-remote` and `git log origin/master`, read 2026-10-03). 118 of them carry the previous operator's two author names. The figure 129 in `DEPENDENCIES.md` counted his local clone, which holds unpushed commits | Who owns it now. ASK: Rahul |
| voyage-api and the deploy | The Voyage backend team owns everything but the `moi-mcp/` folder (`DEPENDENCIES.md` 18, a local file: ASK: Adithya for a copy). Srikar opened voyage-api PR #308 | Who may run the workflow, who reviews a sync PR, whether production has ever been deployed from `feat/moi-mcp`. The run history answers the last (`ship-a-change.md` step 1). ASK: Srikar, Rahul |
| The VM, nginx, TLS, DNS, Teleport | DevOps (Upendhar) | Which VM hosts the MCP and who can log in. Claude never touches it. ASK: Upendhar |
| Reown project behind `WC_PROJECT_ID` | Free project at cloud.reown.com | Its owner. Losing the id stops pairing. ASK: Rahul |
| `UPSTREAM_READ_TOKEN` | A fine-grained token, read-only Contents on go-moi and cocolang | Owner, expiry, whether it is set at all. ASK: Adithya |
| Registry id, read caller | The protocol team (Gokul) | The channel for reset announcements. ASK: Gokul |
| Issue notifications | None found | Who is subscribed to `moi-mcp` issues |

## On the previous operator's machine only (as of 2026-10-03)
- The clone's current branch `feat/agent-experience` was 19 commits ahead of `origin/master` and 20 of its 35 local branches held commits that `origin/master` lacks (read 2026-10-03; the clone is still being committed to, so the counts move). Some branches were squash-merged, so the counts overstate. `DEPENDENCIES.md` 12 lists 25 local branches no longer on GitHub and unpushed work from 2026-10-01. The restructure there moves files (the registry module is `src/capabilities/reads/registry.ts` on that branch, `src/moi/registry.ts` on master). ASK: Adithya for a copy, or to push what should live.
- `moi-mcp-go`, a read-only Go server: no remote, 2 commits, last 2026-09-02. ASK: Adithya.
- A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin.

## Not yet known
- Which sync production runs, as a commit. ASK: Srikar (the deploy run log).
- Whether any monitor or alert watches the three hosts. None found.
- Whether claude.ai plans differ in allowing custom connectors. ASK: Rahul.
