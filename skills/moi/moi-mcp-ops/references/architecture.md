# Architecture: the server, where it runs, what is live

Facts are as of 2026-10-03 where they were read live (probes, public GitHub and npm reads, `git` on a clone) and as of 2026-10-02 where they come from the ops research note ("the research" in this skill: it read the private `voyage-api` workflows, which could not be re-read on 2026-10-03). `ASK: <person>` is defined in `moi-devrel/SKILL.md`. The VM facts, the sync method, the owners and the PR states were corrected on 2026-10-13 from `project-handover-docs/MCP-SERVER.md`, and the live build, tool counts and PR states again on 2026-10-14 from the verified end-of-day state (production runs moi-mcp master `3ae48cc0`). Back to `../SKILL.md`.

## Where the files named in this skill live
Every file of `sarvalabs/moi-mcp` named in this skill is on `master` on GitHub (checked 2026-10-03). Exceptions: the two voyage-api workflows (private repo; on branch `feat/moi-mcp` only, not on its default branch `develop`; known from the research note and not re-read), `DEPENDENCIES.md` (a local file on the previous operator's machine, not in git; its 4 October snapshot is now only in the handover repo's git history), and the unpushed branches listed at the end. Text that exists only on those local branches is labelled as such wherever this skill uses it.

## What it is
MCP (Model Context Protocol) lets a chat assistant such as claude.ai call typed tools on a server. This server turns MOI reads and writes into tools. A write is two tool calls (a preview, then a confirm token), the user's phone wallet signs it, and the server holds no private key (README "Security model"). Source: `sarvalabs/moi-mcp` (public, default branch `master`, TypeScript, Node 20 or later). `package.json` names it `@moi-protocol/mcp-server`, version 0.1.0. The server calls the network `voyage` in its settings (the `MOI_NETWORK` value); say "devnet" in anything public.

Terms. KMOI: the devnet test currency (no real value). A logic: a MOI smart contract. The agent registry: an on-chain logic that lists AI agents; the server finds it by its logic id, and the id changes when devnet is reset. Voyage: MOI's explorer and faucet product, and the backend repo `voyage-api` that hosts this server's production copy. pm2: a Node process manager. nginx: the web server in front that ends TLS. Teleport: the tool DevOps uses to let a workflow reach a VM. OAuth: the sign-in protocol claude.ai uses; here the server is its own issuer. WalletConnect: the relay that carries signing requests to the phone. Reown: the company that runs it and issues the project id (`WC_PROJECT_ID`). A gateway is one of the two Node processes.

## Forms and hosts

| Form | Host | Sign-in | Tools live 2026-10-14 | Deployed by |
|---|---|---|---|---|
| Write gateway, production | `mcp.voyage.moi.technology`, connector URL ends `/mcp` | OAuth run by the server itself: no account, no password | 33 | Manual workflow "Deploy MOI MCP Gateway" in `sarvalabs/voyage-api`, target production |
| Read gateway, production | `mcp-read.voyage.moi.technology`, URL ends `/mcp` | None | 43 (read tools) | The same workflow |
| Dev copies | `dev-mcp.voyage.moi.technology`, `dev-mcp-read.voyage.moi.technology` | Same as above | 33 and 43 (the same build, deployed 2026-10-14) | The same workflow, target dev |
| PR preview | write `pr-<N>-mcp.preview.voyage.moi.technology`, read `pr-<N>-mcp-read.preview.voyage.moi.technology` (confirmed by the Voyage gateway runbook, 2026-10-13); the read `/health` says `readOnly` true, the write one `readOnly` false and `pairingMounted` true | Same | Not read | `moi-mcp.preview.yml`, on every PR to voyage-api |
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
Where it runs (`project-handover-docs/MCP-SERVER.md`): the dev VM is `voyagedev`, production is `prod-voyage`; the app is in `/opt/moi-mcp` and the data in `/var/lib/moi-mcp`; two pm2 processes sit behind nginx, `moi-mcp-read` (`dist/http.js`, port 8787) and `moi-mcp-write` (`dist/server.js`, port 8788). The workflow touches only those two processes. Owner: DevOps (Srikar runs the Voyage VMs and the deploy workflow; Upendhar is the other DevOps contact). Claude never logs in to a VM.
Where it runs (`project-handover-docs/MCP-SERVER.md`): the dev VM is `voyagedev`, production is `prod-voyage`; the app is in `/opt/moi-mcp` and the data in `/var/lib/moi-mcp`; two pm2 processes sit behind nginx, `moi-mcp-read` (`dist/http.js`, port 8787) and `moi-mcp-write` (`dist/server.js`, port 8788). The workflow touches only those two processes. Owner: DevOps (Srikar runs the Voyage VMs and the deploy workflow; Upendhar is the other DevOps contact). Claude never logs in to a VM.

## What is live (2026-10-14, with the probes of 2026-10-03 as history)

| Fact | Value |
|---|---|
| Health | `ok` on all four hosts above (`/health`) |
| Tools | Write gateway 33 and read gateway 43 read tools, on production and dev, since the 2026-10-14 deploy (the classes are in the table below). On 2026-10-03 production listed 13 and 6: `ping`, the four chain reads and `moi_resolve_agent` on both, plus the wallet tools and four writes on the write gateway |
| Version | Every build answers 0.1.0, so the version cannot tell you which sync is live. Use the tool count and the behaviours below |
| Production build | `moi-mcp` master `3ae48cc0` (PR #27, the code review fixes), synced by voyage-api #320 into `feat/moi-mcp` as `237725c6` and deployed to dev and production on 2026-10-14. Production no longer runs the 2026-09-23 sync (voyage-api PRs #310 to #312), which it ran until then |
| Registry | Agent lookup works since the 2026-10-14 deploy: `moi_resolve_agent` answers on dev (health 10 PASS, 0 FAIL) and production got the same setting. The registry id in the code (`src/moi/registry.ts`, `0x200000002f3e9469...`) is the current one, the same as the Agent Explorer and the Launchpad; the Explorer's id is the source of truth after a reset. voyage-api #323 (merged 2026-10-14) makes the deploy workflow pass `MOI_READ_CALLER` (`0x000000001a46...`, the account the Agent Explorer uses for the same reads) to both gateways. History: on 2026-10-03 the tool failed on every host with "Could not load the MOI agent registry (logic 0x20000000c684f926...) ... account not found", the registry wiped on 2026-09-11 |
| OAuth metadata | The fix of PR #18 (commit `93d4d9d`) is live on production since 2026-10-14, so claude.ai Connect no longer stalls. History: until then production named the bare origin as the protected resource and 404ed the `/mcp` document |
| Chain RPC | `net.Version` answers 0.13.0 on both `/devnet/` and `/babylon/` paths of `dev.voyage-rpc.moi.technology` (the TLS certificate that expired on 2026-10-04 was renewed, valid 2026-10-05 to 2027-01-03; `net.Version` 0.13.0 again on 2026-10-13). The hosted read gateway is deployed with the `/babylon/` path, the code default is `/devnet/`. Whether they are one chain: ASK: Gokul |
| GitHub | `moi-mcp` has no git tag. PR states on 2026-10-14: moi-mcp #27 merged as `3ae48cc0`; #4 (code review, since 2026-09-11) closed, superseded by #27; #25 closed 5 October, #26 closed 12 October and #28 closed 14 October (Dependabot); #29 open since 2026-10-14 (Dependabot majors, replaces #28: do not merge as is). Open issue #17 (js-moi-sdk v0.9.0-rc3, since 2026-09-23). No `chain-canary` issue has ever been opened. voyage-api: #320 (sync of #27) merged into `feat/moi-mcp` as `237725c6`; #313 (the 23 September sync of the consent fix, registry and Launchpad tools) closed as superseded by #320; #323 (the deploy workflow passes `MOI_READ_CALLER`) merged |
| npm | `@moi-protocol/mcp-server` and `@sarvalabs/mcp-server` both return "Not found". The newest `js-moi-sdk` on npm is 0.9.0-rc2 (still, on 2026-10-13), which is what the server pins; rc3 is a GitHub release only |

## Tool classes
Since PR #27 master and production both run 33 tools on the write gateway and 43 read tools on the read gateway (2026-10-14). History: master's README table listed 28 tools and the source added three registry write tools the table omits (commit `2af858f`), 31 tool names in `src/` on 2026-10-03, when production listed 13.

| Class | Tools on master | Phone | On production (2026-10-14) |
|---|---|---|---|
| Health | `ping` | no | yes |
| Chain reads | `moi_get_account`, `moi_get_asset`, `moi_get_interaction`, `moi_get_logic` | no | yes |
| Registry reads | `moi_resolve_agent`, `moi_list_agents` | no | yes (lookup answers) |
| Wallet | `moi_connect_wallet`, `moi_wallet_status`, `moi_disconnect_wallet` | pairing tap | yes |
| Writes, preview then confirm | `moi_transfer`, `moi_create_asset`, `moi_mint`, `moi_call_logic` (invoke), `moi_create_account` | yes | yes |
| Registry writes | `moi_register_agent`, `moi_set_agent_status`, `moi_transfer_agent` | yes | yes |
| Launchpad | `moi_launchpad_templates`, `_sign_in`, `_status`, `_create_agent`, `_register_agent`, `_telegram_link`, `_setup_script`, `_sign_out` | sign-in is a message tap, register is a write | yes |
| Dapp | `moi_dapp_sign_in`, `_api`, `_call`, `_sessions`, `_sign_out` | sign-in is a message tap | yes |
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
| voyage-api and the deploy | The Voyage backend team owns everything but the `moi-mcp/` folder (`project-handover-docs/MCP-SERVER.md`). Srikar runs the deploy workflow and opened voyage-api PR #308 | Who may run the workflow, who reviews a sync PR, whether production has ever been deployed from `feat/moi-mcp`. The run history answers the last (`ship-a-change.md` step 1). ASK: Srikar, Rahul |
| The VM, nginx, TLS, DNS, Teleport | DevOps (Upendhar) | Who besides DevOps can log in. Only DevOps logs in to the VM (dev `voyagedev`, production `prod-voyage`). Claude never touches it. ASK: Upendhar |
| Reown project behind `WC_PROJECT_ID` | Free project at cloud.reown.com | Its owner. Losing the id stops pairing. ASK: Rahul |
| `UPSTREAM_READ_TOKEN` | A fine-grained token, read-only Contents on go-moi and cocolang. Not set on `sarvalabs/moi-mcp` as of 2026-10-10 | Which account owns it: Rahul decides |
| Registry id, read caller | The protocol team (Gokul) | The channel for reset announcements. ASK: Rahul |
| Issue notifications | None found | Who is subscribed to `moi-mcp` issues |

## On the previous operator's machine only (as of 2026-10-03)
- The clone's current branch `feat/agent-experience` was 19 commits ahead of `origin/master` and 20 of its 35 local branches held commits that `origin/master` lacks (read 2026-10-03; the clone is still being committed to, so the counts move). Some branches were squash-merged, so the counts overstate. `DEPENDENCIES.md` 12 lists 25 local branches no longer on GitHub and unpushed work from 2026-10-01. The restructure there moves files (the registry module is `src/capabilities/reads/registry.ts` on that branch, `src/moi/registry.ts` on master). Not recorded (the previous DevRel's notes); ASK: Rahul.
- `moi-mcp-go`, a read-only Go server: no remote, 2 commits, last 2026-09-02. Not recorded (the previous DevRel's notes); ASK: Rahul.
- Security: `project-handover-docs/MCP-SERVER.md` records no finding for this product. The 2026-10-02 research note said one was open; its content is not recorded (the previous DevRel's notes); ASK: Rahul before touching sign-in or other admin code.

## Not yet known
- Whether any monitor or alert watches the three hosts. None found.
- Whether claude.ai plans differ in allowing custom connectors. ASK: Rahul.
