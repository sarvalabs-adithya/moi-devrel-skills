# MOI MCP Server

**Status: active.** Production was redeployed on 14 October 2026 with the code review fixes: 33 tools on mcp.voyage.moi.technology (reads, wallet writes, the Launchpad and dapp tools) and 43 read tools on mcp-read.voyage.moi.technology, live on **devnet** (MOI's test network). Agent lookup (reading the **agent registry**, the on-chain list of registered agents) works since that deploy: the workflow now passes MOI_READ_CALLER to both gateways, and the registry id in the code is current. Inactive: the npm package (never published).

Video: MCP demo, recorded 13 October: https://drive.google.com/file/d/1NGdNHOIDr7VfghWqs58ufskWbVxHyvQL/view

Marketing: How it works (What the user sees, The tools), Process (Publishing to npm), Claude skill, Open items. Developers: How it works, Stack, Variables, Env vars, Process, Claude skill, Open items.

This server lets a chat assistant such as Claude use MOI. **MCP** (Model Context Protocol) is the standard by which an assistant calls tools on a server, and this server turns MOI reads and writes into those tools. A user adds it as a connector in claude.ai, pairs their MOI Wallet from their phone, and then asks in plain words: what is this account's balance, send 5 **KMOI** (MOI's native asset) to this address, create a test asset. The server never holds a private key, because every write is signed on the phone. Adithya wrote it. The Voyage team hosts the production copy inside their backend, and DevOps (Upendhar, Srikar) owns the VM it runs on. Everything runs on devnet only.

## How it works

**What the user sees**

- In claude.ai: Settings, Connectors, Add custom connector, URL https://mcp.voyage.moi.technology/mcp, authentication **OAuth** (the standard sign-in handshake between claude.ai and the server).
- A consent page opens. There is no account and no password. The identity is a cookie in that browser, so a different browser counts as a new identity and needs its own pairing.
- Reads work straight away: accounts, assets, **interactions** (MOI's transactions) and **logics** (smart contracts).
- To write, the user asks Claude to connect their wallet. The tool returns a link to a pairing page, because claude.ai never shows the QR image. They open the link, scan the QR with MOI Wallet within about 5 minutes, and approve on the phone. A pairing lasts a week.
- A write is two steps. The first call returns a preview with the numbers (amount, fee, **storage fund**, the KMOI a new asset sets aside for its own storage and execution fees) and a confirm token. The second call confirms. The token is bound to that user, that tool and those arguments, lasts 10 minutes and works once.
- The phone then shows a signing request. The phone cannot display what it signs, so the user reads the numbers in the chat preview before approving.
- The phone signs, the server broadcasts, and the answer carries the interaction hash. The receipt (moi_get_interaction says success) proves a write worked, not the broadcast. Devnet has accepted things in simulation that it later refused.

**Two gateways from one codebase**

| | Read gateway | Write gateway |
|---|---|---|
| Host | mcp-read.voyage.moi.technology | mcp.voyage.moi.technology |
| Sign-in | None | OAuth, run by the server itself |
| Tools live today | 43 read tools: ping, the chain reads, agent lookup and the other read-only tools | 33: the reads, the wallet tools, the writes, and the Launchpad and dapp tools |
| State | None. Any number of copies can run | Sign-ins, tokens, pairings and a journal of writes, as files in the data directory. Exactly one process, because two copies fight over the **WalletConnect** relay identity (WalletConnect is the open protocol that links a phone wallet to an app) |
| Dev copies | dev-mcp-read.voyage.moi.technology | dev-mcp.voyage.moi.technology |

The data directory (MOI_DATA_DIR, /var/lib/moi-mcp on both VMs) holds the sign-in clients and hashed tokens, the cookie secret, one pairing per user, the write journal (every write as proposed, signed, broadcast, confirmed, failed or orphaned) and WalletConnect scratch files. Losing the cookie secret or the tokens signs everyone out. Losing the pairings un-pairs every wallet. Losing the journal loses audit history only. Never delete or move the directory, not even during a rollback.

**The tools**

| Class | Tools | Phone needed | Live on production |
|---|---|---|---|
| Health | ping | No | Yes |
| Chain reads | moi_get_account, moi_get_asset, moi_get_interaction, moi_get_logic | No | Yes |
| Agent registry reads | moi_resolve_agent, moi_list_agents | No | Yes. Lookup answers since the 14 October deploy; list is deployed with master |
| Wallet | moi_connect_wallet, moi_wallet_status, moi_disconnect_wallet | A pairing tap | Yes |
| Writes, preview then confirm | moi_transfer, moi_create_asset, moi_mint, moi_call_logic (invoke), moi_create_account | Yes | Yes. Assets: **MAS0** (MOI's standard for ordinary fungible tokens), MAS1, MAS2 and MASX (added by PR #27) |
| Agent registry writes | moi_register_agent, moi_set_agent_status, moi_transfer_agent | Yes | Yes |
| Launchpad | moi_launchpad_templates, _sign_in, _status, _create_agent, _register_agent, _telegram_link, _setup_script, _sign_out | Sign-in is a message to sign; register is a write | Yes |
| Dapp | moi_dapp_sign_in, _api, _call, _sessions, _sign_out | Sign-in is a message to sign | Yes |

**Transfers to other people, through claude.ai.** Adithya reported (14 October 2026) that a newer Claude policy stops claude.ai from sending assets to someone else's address: a transfer or mint to your own account still goes through, a send to another address is refused by Claude. The refusal comes from Claude, not from this server, whose code still allows any recipient. The policy text was not saved; find it before relying on this, and test a 1 KMOI send to another address to see where it stands.

Creating a Launchpad agent through the connector ends with a one-time download link for setup-<name>.sh; the user runs it with bash from the folder it landed in (usually cd ~/Downloads). The reply says only "run it with bash"; printing those two lines in the reply is a small follow-up. The Launchpad tools reached production on 14 October with the voyage-api sync #320.

Since the 14 October deploy, production runs master (3ae48cc0): 33 tools on the write gateway and 43 on the read gateway. Every build reports version 0.1.0, so the tool count and the behaviour are how you tell which build is live.

**Two repos: where the code lives and where it runs**

- sarvalabs/moi-mcp (public, default branch master) is the source. CI runs typecheck, tests and build on Node 20, 22 and 24 on every PR. Merging there deploys nothing.
- sarvalabs/voyage-api (private, the Voyage backend) holds a copy of the server in the folder moi-mcp/ on the branch feat/moi-mcp, with two workflows: "Deploy MOI MCP Gateway" (manual, moi-mcp.deploy.yml) and a preview workflow that runs on every PR (moi-mcp.preview.yml).
- To update production, a **sync subtree** PR (copies the server's folder from moi-mcp into voyage-api) replaces that folder with master's tree, is merged into feat/moi-mcp (not develop), and then a person runs the deploy workflow by hand with deploy_target dev or production.
- The deploy builds on Node 22, copies the build to the VM through **Teleport** (the access gateway DevOps run in front of the VM), stops both processes and starts them again with their settings passed inline (there is no .env on the server), then checks /health. Every deploy is a short outage, and any sign-in or phone signing call in flight is lost.
- Production runs the 14 October sync: moi-mcp PR #27 (3ae48cc0) and the voyage-api sync PR #320 (237725c6), deployed to dev and production the same day. Before that, production ran the 23 September sync (voyage-api PRs #310 to #312) while master moved on with moi-mcp PRs #21 to #23 (registry tools, Launchpad tools, dapp tools); the sync that was meant to bring them, voyage-api #313, was closed as superseded by #320.

**The automatic checks**

Three things run on their own in sarvalabs/moi-mcp. The **chain canary** is a nightly test that simulates a write against live devnet. The **upstream watch** reports new releases of the libraries the server depends on. **Dependabot** proposes dependency updates. Each opens a GitHub issue or a PR, and nothing merges or deploys by itself, so a person has to read them.

| Check | When | What it asks | What it opens |
|---|---|---|---|
| Chain canary | Nightly, 02:43 UTC | Does live devnet still accept what this server builds? It only simulates: nothing is signed or spent | One issue "Chain canary failing", closed by the next green run |
| Upstream watch | Daily, 03:17 UTC | Did js-moi-sdk, go-moi or cocolang publish a GitHub release? | One issue "Upstream release: <name> <tag>" per release |
| Dependabot | npm daily, Actions weekly | Dependency updates, with the js-moi packages grouped together | Pull requests |

What they cannot see: the canary tests master's code against devnet, not the hosted server, the registry, sign-in or a phone (it was green all through the registry fault). The watch needs UPSTREAM_READ_TOKEN to read the two private repos and only logs a warning without it. No go-moi or cocolang issue has ever been filed, although go-moi v0.13.0 shipped on 10 September.

## Stack

| Piece | What it is |
|---|---|
| TypeScript 5, Node 20 or later, built with tsup | The server. Four commands: a local server for desktop clients, the HTTP read gateway, the hosted write gateway, and a CLI |
| @modelcontextprotocol/sdk | The protocol |
| js-moi-sdk 0.9.0-rc2, pinned exactly | Chain reads, building interactions, the KMOI id, the **fuel** floor (fuel is the per-interaction execution fee) |
| WalletConnect 2 (a Reown project id) | The phone wallet pairing and signing. The server holds no key |
| Express 5 | Both gateways. The write gateway runs its own OAuth server for claude.ai |
| Files in the data directory, or **Redis** (an in-memory data store; optional) | Sign-ins, tokens, pairings and the write journal |
| **pm2** (a Node process manager) behind **nginx** (the web server) on a Voyage VM | Two processes started by the deploy workflow: moi-mcp-read (dist/http.js, port 8787) and moi-mcp-write (dist/server.js, port 8788), from /opt/moi-mcp. The dev VM is voyagedev, production is prod-voyage. The workflow touches only these two processes. nginx ends TLS, with no buffering and 300 second timeouts |
| GitHub Actions + Teleport, in voyage-api | The manual deploy and the PR preview |
| vitest | Tests, 88 files. A Dockerfile exists for the read gateway; production does not use it |

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Codebase | DevRel | sarvalabs/moi-mcp, public. DevRel pushes branches to it |
| Production copy and the deploy workflow | Voyage team (Srikar) | sarvalabs/voyage-api, branch feat/moi-mcp, folder moi-mcp/. They own everything else in that repo |
| Server, nginx, TLS, DNS, Teleport, the data directory | DevOps (Upendhar, Srikar) | Only DevOps logs in to the VM |
| WalletConnect (Reown) project | sarvalabsdeveloper@gmail.com | A free project at cloud.reown.com. Its id is passed as WC_PROJECT_ID; losing it stops every pairing |
| Agent registry id and the read caller account | Protocol team (Gokul) | Both change on every devnet reset |
| The Launchpad | DevRel | The Launchpad tools sign in to it. MOI_LAUNCHPAD_URL must equal the Launchpad's own public URL |
| UPSTREAM_READ_TOKEN | Rahul decides the account | A fine-grained GitHub token, read-only on go-moi and cocolang, for the upstream watch |
| npm package name | Rahul decides | @moi-protocol/mcp-server in package.json. Nothing is published and neither scope is claimed |

## Env vars

The index across every product, with the consoles and who holds each login, is ENV-VARS.md.
Where they live: production values are passed inline by the deploy workflow in sarvalabs/voyage-api (the pm2 start lines in moi-mcp.deploy.yml on feat/moi-mcp). There is no .env on the server. Secrets come from the voyage-api repository secrets (repo level, not environment level: the production environment holds none) and plain values are written in the workflow file, so the only copies are in GitHub and in the running process. Only the names the workflow passes reach the processes; a new setting needs a line in the workflow and a deploy. Locally, a .env copied from .env.example in the repo, or the env block of the desktop client's connector config.

| Variable | What it is | Where the value comes from |
|---|---|---|
| WC_PROJECT_ID | The Reown project id, 32 hex characters. The write gateway refuses to start without one; a wrong one makes every pairing fail | voyage-api secrets MCP_PROD_WC_PROJECT_ID and MCP_DEV_WC_PROJECT_ID, from cloud.reown.com, the project, Project ID |
| PUBLIC_URL | The write gateway's public address, also the OAuth issuer. Must be the exact https origin or sign-in loops | Written in the workflow |
| MOI_NETWORK, MOI_RPC_URL | voyage today. The read gateway is given the /babylon/ path of dev.voyage-rpc.moi.technology; the code default is /devnet/. Both answer 0.13.0 | Written in the workflow |
| MOI_DATA_DIR, HOSTED_PORT, LOG_LEVEL, NODE_ENV | The data directory, the write gateway port, log level, Node mode | Written in the workflow |
| MOI_READ_CALLER | The account the server pretends to be when it reads the agent registry. On MOI, a contract's read routines are run as a simulated interaction, and every interaction needs a sender that exists on chain, even though nothing is signed, sent or paid. The server holds no account of its own, so this setting names one to use as that sender. Without it, agent lookup fails with "account not found". Any account that exists on devnet works; it needs no funds and no key. Since voyage-api PR #323 (14 October 2026) the workflow passes 0x000000001a46e49490bf4798eb0a09ac3a1fce7773d25ad53158320800000000 to both gateways, the same account the Agent Explorer uses for its registry reads. A devnet reset can wipe it: then pick any account that exists on the new chain | Any devnet account that exists (no funds, no key) |
| MOI_AGENT_REGISTRY_LOGIC_ID | Overrides the registry id written in the code. Not passed today | Protocol team, after each reset |
| MOI_LAUNCHPAD_URL | Used by the Launchpad tools once they are deployed. The code defaults to https://launchpad.moi.technology, so pass it only if the Launchpad moves | The Launchpad's NEXT_PUBLIC_APP_URL |
| MOI_SESSION_KEY | Not read by master yet. The encryption-at-rest change (split out of PR #27 into a later PR) makes it required at boot. The workflow must pass it before that change is synced, or the write gateway crash-loops. voyage-api already holds MCP_DEV_SESSION_KEY, MCP_PROD_SESSION_KEY and MCP_PREVIEW_SESSION_KEY as repository secrets; nothing passes them yet | Generate with: openssl rand -base64 32 |
| REDIS_URL, HOSTED_TIMEOUT_MS, MOI_EXPLORER_URL, PORT, MOI_MCP_HOME, REQUEST_TIMEOUT_MS, MOI_WC_PARAM_STYLE | Optional: Redis for pairings (carries a password), the hosted call budget (default 240000 ms; above 300000 claude.ai gives up first), explorer links, the read gateway port, the local state folder, the local phone wait, and the WalletConnect payload style (leave unset) | Defaults in the code |
| TELEPORT_PROXY, TELEPORT_JOIN_TOKEN, MCP_DEV_MACHINE, TELEPORT_PROD_PROXY, TELEPORT_PROD_JOIN_TOKEN, MCP_PROD_MACHINE | Deploy access, in voyage-api | DevOps |
| UPSTREAM_READ_TOKEN, NPM_TOKEN | In sarvalabs/moi-mcp: the upstream watch, and publishing on a v* tag. Neither is set on the repo (checked 10 October 2026), so the watch has never been able to read go-moi or cocolang | A fine-grained GitHub token with read-only Contents on go-moi and cocolang; the npm account owner |

The example file with comments is .env.example in the repo. Its default registry id is the wiped one.

## Process

**Shipping a change: the source**

- Work on a branch of sarvalabs/moi-mcp.
- Every bug fix gets a test that would have caught it.
- Run what CI runs: npm run typecheck, npm test, npm run build, node dist/cli.js help. Use Node 20 or later; the VM runs 20.14.
- If the change touched package.json, a bin or start-up, install from the packed tarball in a scratch folder and start the HTTP bin once. This caught a phantom dependency before.
- If the change reads a new setting, say so in the PR. The deploy workflow passes a fixed list, and a newly required setting crash-loops the write gateway.
- Open a PR to master. Body: what changed, how it was verified, what is not verified, "Deploy: not run".
- Merge once CI is green on all three Node versions. This deploys nothing.

**Shipping a change: the sync**

The moi-mcp/ folder in voyage-api is a **git subtree** (a copy of another repo kept inside this one, updated with git subtree pull). The steps below follow the Voyage team's gateway runbook ("MOI MCP Gateway: Development, Preview and Deployment Runbook", PDF, shared on 13 October 2026).

- In sarvalabs/voyage-api, branch from feat/moi-mcp: git checkout -b feat/update-moi-mcp (or fix/... or chore/...; the earlier syncs used moi-mcp/sync-master). Never change the subtree directly on the deployment branch.
- Add the upstream once: git remote add moi-mcp-upstream https://github.com/sarvalabs/moi-mcp.git
- Pull master into the folder: git fetch moi-mcp-upstream, then git subtree pull --prefix=moi-mcp moi-mcp-upstream master
- Check it: git diff --stat against feat/moi-mcp must list paths under moi-mcp/ only. Then cd moi-mcp, npm ci, npm run build; the build must pass before the PR. cd .. back to the root.
- Commit and push: git add moi-mcp, git commit -m "chore: update moi-mcp subtree", git push -u origin feat/update-moi-mcp.
- Open the PR against feat/moi-mcp, never develop. Title: chore(moi-mcp): sync subtree <date>. Body: what changed in moi-mcp and why, build and test results, what to test on the preview, the settings it adds or needs, what is unverified, "Deploy: not run".
- Opening or updating the PR runs moi-mcp.preview.yml, which starts an isolated pair for that PR on the dev VM, with its own ports and pm2 processes: write https://pr-<N>-mcp.preview.voyage.moi.technology, read https://pr-<N>-mcp-read.preview.voyage.moi.technology (PR 308 used ports 10616 and 10617). Both /health answers must be 200: the read one {"ok": true, "network": "voyage", "readOnly": true}, the write one with "readOnly": false and "pairingMounted": true. Check them with the health script (--write-host), then connect the preview's /mcp address in Claude and test what the PR changed.
- Get a review from the Voyage side and merge. Still nothing is deployed.

**Shipping a change: the deploy**

- Tell the Voyage team and DevOps: what ships, when, and that it is a short outage.
- Actions in voyage-api, "Deploy MOI MCP Gateway", Run workflow, branch feat/moi-mcp, deploy_target dev. Watch the run; its last job checks /health.
- Run the health script against dev (--env dev). Pass the expected tool counts if the sync added tools.
- Run the workflow again with deploy_target production. (deploy_target both runs dev and production in one go; use it only for a change already proven on dev.)
- Run the health script against production, then the connector checks below for every class the change touched, reads first. A write path change needs a phone-approved write and its receipt.
- Record: source commit, sync PR, run id, what was checked and what was not.
- If a check fails after the deploy, roll back (below) before trying a second deploy.

**Connecting and checking the connector** (after every production deploy, and for a new user)

- Health script first. Then one read through the wire: curl a tools/call of moi_get_asset against the read gateway with KMOI's id, taken from the SDK and never from a note.
- Add the connector in claude.ai: URL https://mcp.voyage.moi.technology/mcp, authentication OAuth. For read-only use, add https://mcp-read.voyage.moi.technology/mcp with authentication None. None on the write host makes sign-in impossible.
- Sign in on the consent page.
- Reads in the chat: KMOI's supply, the tester's balance, an interaction hash from the explorer. Agent lookup answers since the 14 October deploy; if it fails after a reset, see the reset steps below.
- Pair: "Connect my MOI wallet for a week." Open the link, scan, approve. "What is my wallet status?" shows the paired account.
- Cheapest write first: transfer 1 KMOI to the tester's own account. Preview, confirm, approve on the phone. Then moi_get_interaction on the hash: status success is the proof.
- Asset creation: "Create a test asset DEPLOYTEST with supply 100." Read the storage fund in the preview before approving. The minimum on master is 7 KMOI; the repo checklist's 20,000 predates v0.13.0.
- Failure paths, when the change touched them: reject on the phone (user_rejected), ignore it for 5 minutes (timeout), wallet on another network (network_mismatch, reads still work), disconnect then write (wallet_disconnected).
- You need MOI Wallet on a phone with a devnet account that exists on chain and holds KMOI. The faucet funds only accounts that already exist, so a brand-new wallet registers through the wallet app first. You also need a claude.ai plan that allows custom connectors.

**Changing a setting or a secret**

- Read what the workflow passes today: the pm2 start lines in moi-mcp.deploy.yml on feat/moi-mcp.
- A secret: set it in the voyage-api environment with gh secret set, typing the value at the hidden prompt. Nothing can read it back.
- A plain value: a PR into feat/moi-mcp that edits the pm2 start line. Merging deploys nothing.
- Run the deploy, dev then production. Only values the workflow passes reach the processes.
- Check with the health script. The OAuth issuer must equal PUBLIC_URL; http://localhost there means the environment never reached the process.
- Do not replace WC_PROJECT_ID casually, because it is the relay identity behind every pairing.

**After a devnet reset**

- Start with the devnet reset skill for the order across products. The MCP steps follow.
- Confirm the signature: the health script's RPC line, and agent lookup failing with "account not found".
- Get from the Protocol team: the new registry id, whether agents were re-imported, the SDK versions, and whether KMOI's id, the fuel floor or the RPC path changed.
- Check the id before using it: moi_get_logic on the new id through the read gateway must list the registry routines (RegisterAgent, GetAllAgentIds, GetAgentProfile, SetAgentStatus, TransferAgent and the rest).
- Point the server at it: either pass MOI_AGENT_REGISTRY_LOGIC_ID and MOI_READ_CALLER from the workflow (a PR), or change the default id in src/moi/registry.ts by PR to master and sync. The current id is already on master and in production (deployed 14 October), and the workflow passes MOI_READ_CALLER since PR #323.
- If the SDK constants moved, take the grouped Dependabot PR and run the canary by hand: MOI_E2E=1 npx vitest run test/e2e/chain-canary.test.ts. If KMOI's creator account is gone, the canary needs MOI_CANARY_ACCOUNT, which the nightly workflow does not pass: a workflow edit.
- Three repos pin the registry id separately (Launchpad, Explorer, this server). After the September reset their ids drifted apart by up to 12 days. The Agent Explorer's id is the source of truth after a reset.

**Checking it is healthy**

- bash "$SKILLS/moi-mcp-ops/scripts/mcp-health.sh" checks both production gateways and the chain RPC. Add --env dev for the dev pair, --github for the canary and watch runs and open issues, --write-host for a preview host.
- On 7 October the script gave 9 pass, 4 warn, 0 fail. A hand check on 13 October found both gateways ok with the same warnings. The warnings were that production served the OAuth metadata in the form it had before PR #18 (so claude.ai Connect could stall), and that agent lookup failed on every host with the stale registry id. Both were cleared by the 14 October deploys: the metadata fix is live, and dev gave 10 PASS, 0 FAIL with agent lookup answering. Production on the evening of 14 October gave 12 PASS, 0 WARN, 0 FAIL (33 tools on the main gateway, 43 on the read gateway).
- By hand: curl /health on both hosts, /.well-known/oauth-authorization-server (the issuer must equal the host), /.well-known/oauth-protected-resource, and a tools/list POST to /mcp with accept set to application/json, text/event-stream. The answer is server-sent events: the JSON follows a data: line.
- What green does not prove: health ok says the process is up, not that registry reads, pairing or a write work. A green canary says nothing about the hosted server. Only a person with a phone can prove the write path.
- On the VM (DevOps reads this): both processes online, the write gateway as a single instance; the error log with the [moi-mcp] prefix; the nginx block with proxy_buffering off, 300 second read and send timeouts, X-Forwarded-For set, and no redirect in front of either host (a redirect drops the Authorization header and breaks sign-in silently).
- No uptime monitor watches these hosts.

**When something is wrong**

| Symptom | Cause | Fix |
|---|---|---|
| Health unreachable, 502 or 504 | DNS, TLS, nginx, the VM or the process. mcp.moi.technology is not a real host; the live ones end .voyage.moi.technology | DevOps. For a 502 they read the write gateway's error log; a fatal line about WC_PROJECT_ID means the id is missing |
| Health 503 with ok false | The config failed to load: a bad MOI_NETWORK, or custom without MOI_RPC_URL | Fix the workflow value, deploy |
| OAuth issuer says http://localhost | PUBLIC_URL never reached the process | Set it in the workflow, deploy |
| Consent completes, then the connector asks again | PUBLIC_URL differs from the host users reach, or plain http drops the cookie | The exact https origin, then a deploy |
| claude.ai Connect spins forever while curl passes | The build predates PR #18: the protected-resource document names the bare origin, and a registration limit of 10 a minute locks out everyone behind claude.ai's shared address | Sync and deploy master |
| No QR in the chat | claude.ai never renders the image | Open the pairing link the tool returns |
| Scanning does nothing, "the relay refused the pairing" | WC_PROJECT_ID missing or wrong | A real id in the voyage-api secret, then a deploy |
| "The wallet pairing has expired" | A pairing lasts a week | Connect again. Expected |
| Every write fails network_mismatch | The wallet is on another network | Switch the wallet, disconnect, pair again |
| Everyone signed out after a deploy | The data directory or its cookie secret was lost | Restore it. If it is gone, everyone signs in and pairs again |
| Agent lookup: "Could not load the MOI agent registry ... account not found" | The stale registry id, or MOI_READ_CALLER unset | The reset steps above. Tell the user nothing is wrong with their wallet |
| "interaction underpriced" after the phone approved | A fuel price literal of 1; the floor is 50 since v0.13.0. Fixed on master in PR #15 | Check the live build has it; sync and deploy if not |
| Tool calls fail during a long phone wait, or a stream never answers | An nginx timeout under 300 seconds, or buffering on | DevOps edits the nginx block |
| Launchpad tool: "Not signing: the sign-in message from <origin>..." | MOI_LAUNCHPAD_URL differs from the Launchpad's URL | Make them equal in the workflow |
| The deploy run is red | Read the failing step. A red run can leave the old processes stopped | Health script, then roll back |
| Claude Desktop with npx -y @moi-protocol/mcp-server does nothing | Nothing is published | The hosted connector, or a local build |

**Rolling back**

- There is no documented rollback, and the VM keeps no previous build.
- Triggers: a FAIL on health, the issuer, tools/list or ping right after a deploy and again a minute later; the write gateway crash-looping; the tool count dropped; sign-in looping for everyone.
- What cannot be undone: anything broadcast to the chain, consents and signing calls in flight, and pairings if the bad release changed their stored format.
- Find the last good sync: the voyage-api run list and the merged sync PRs on feat/moi-mcp.
- Revert the bad sync commit on a branch from feat/moi-mcp, open a PR titled revert(moi-mcp): sync subtree <sha>, merge, then run the deploy for production again. Another short outage.
- Verify with the health script and the reads, and a Connect from a clean browser if sign-in was hit.
- Tell the Voyage team and DevOps, then fix forward through a new PR with a test.
- Never delete or move the data directory as part of a rollback.

**When an automatic check opens an issue**

An upstream release:
- Read the issue: which upstream, which tag, whether the pin differs, whether the version is on npm.
- js-moi-sdk on npm: review the grouped Dependabot PR and run the canary by hand before merging. Never merge an SDK bump unread, because it changes what a user signs. A GitHub-only release (rc3 was one): wait for npm, or ask Gokul.
- go-moi: read the release note, run the canary, and ask the Protocol team when devnet picks it up. A go-moi release can precede a reset.
- cocolang: read the notes for manifest or calldata changes. moi_get_logic reads the manifests Coco produces and moi_call_logic encodes calls against them.
- Comment what was checked and close the issue.

The chain canary failing:
- Read the issue for the failing check, then the health script's RPC line. A changed net.Version means a node upgrade.
- Reproduce in a working copy with the canary command above.
- Map the check to its cause: KMOI's id moved (SDK upgrade), a new asset standard (SDK upgrade), decimals or scaling changed, the storage fund or its floor too small, the fuel floor moved, or the sender account gone after a reset.
- Fix by PR with a test. Production changes only after a sync and a deploy.
- Let the next green run close the issue.

**Publishing to npm**

- Nothing is published. @moi-protocol/mcp-server and @sarvalabs/mcp-server are both unclaimed, and the README, the quickstart and the desktop example all tell users to run npx, which fails today.
- A pushed tag matching v* publishes to npm through publish.yml with NPM_TOKEN. Never push one until the name is decided.
- Before the first publish: Rahul picks the name and the npm owner, NPM_TOKEN is set, the packed tarball check passes, and the transfer and create-asset writes have passed once on a phone.
- Publish 0.1.0, not 1.0.0. The write path may change when the wallet's own sign-and-send call is fixed.
- After publishing: a working demo, the directory listings (drafts in docs/launch), then the announcement, through claim-check and the blog.
- Public wording: say devnet, make no mainnet claim.

## Claude skill

The **moi-mcp-ops** skill covers running the server: health, shipping, connecting, triaging the automatic checks, settings, rollback and the publishing questions. After a devnet reset, start with **moi-devnet-reset** for the order across products. A recorded test pass uses the case list in moi-mcp-ops/references/test-pass.md.

| When | What to tell Claude | What the skill does |
|---|---|---|
| Something looks wrong | "Is the MCP healthy?" | Runs the read-only health script on both gateways and the chain, and says what each warning means. |
| Shipping | "Ship this MCP change." | Walks the moi-mcp PR, the sync PR into voyage-api, the preview check and the two deploys, and says at each step what is and is not deployed. |
| A new user, or after a deploy | "Walk me through connecting the connector." | Gives the claude.ai steps, the reads to ask, the pairing and the first write, and checks each result. DevRel does the wallet steps. |
| An issue from the checks | "The canary opened an issue." or "There is an upstream release issue." | Reads the issue, reproduces, maps the failing check to its cause and drafts the fix or the closing comment. |
| A setting | "I need to change this MCP setting: ..." | Says whether the workflow passes it, where it is set and that a deploy follows. It never sees a secret's value. |
| Devnet reset | "Devnet was reset. What do I redo for the MCP?" | Confirms the reset, drafts the message to Gokul, checks the new id and lists the PRs needed. |
| A user reports a fault | "A user says the connector will not connect." | Finds the row above and drafts the reply. |
| A bad deploy | "Roll back the MCP." | Gives the revert and redeploy steps. |
| Publishing | "Can we publish the package?" | Lists what is still open and who decides each point. |
| A test pass | "Run the MCP test pass." | Walks the case list in test-pass.md and keeps a log. |

What the skill never does without DevRel's yes: push, open or comment on a PR or issue (the repo is public), merge, run the deploy workflow, change a secret, push a tag, or send a message. It never logs in to the VM, never calls a wallet or write tool itself, and never handles a recovery phrase.

## Open items

- Merged on 14 October 2026: moi-mcp PR #27 (the code review fixes: dapp security, the MAS0 guard, the read layer, more writes, MAS1, MAS2 and MASX creation, hardening; reviewed by Gokul) as 3ae48cc0, then the voyage-api sync PR #320 into feat/moi-mcp as 237725c6. Both were squash-merged with clean messages. The voyage-api moi-mcp/ folder now equals moi-mcp master (271 files). voyage-api #313 and moi-mcp #4 were closed as superseded (by #320 and #27). Both were deployed the same day (next items).
- Deployed on 14 October 2026: dev (first run 8 PASS, 0 FAIL), then production (first run 8 PASS, 4 WARN, 0 FAIL; the warnings were the new tool counts and agent lookup). Production now runs moi-mcp master at 3ae48cc0: 33 tools on mcp.voyage.moi.technology, 43 read tools on mcp-read.voyage.moi.technology, and the OAuth metadata fix, so claude.ai Connect no longer stalls. Production no longer runs the 23 September sync.
- voyage-api PR #323 merged on 14 October: the deploy workflow passes MOI_READ_CALLER (the account the Agent Explorer uses for the same reads) to both gateways, and both were deployed with it. Agent lookup works: moi_resolve_agent answers on dev (health 10 PASS, 0 FAIL) and production got the same setting. The registry id in the code (0x200000002f3e9469...) is the current one, the same as the Agent Explorer and the Launchpad; the Explorer's id is the source of truth after a reset. MOI_LAUNCHPAD_URL defaults correctly; MOI_SESSION_KEY is not needed yet (the encryption-at-rest change comes back as its own PR once the workflow can pass it).
- Dependabot PR #26 was closed on 12 October and #28 on 14 October; its replacement #29 (opened 14 October) fails the build because it bumps majors (zod 4, TypeScript 7, vitest 5, @types/node 26) and zod 4 breaks the types in the dapp, Launchpad and WalletConnect code. Do not merge it as is: split the majors out or ignore them in dependabot.yml.
- Decide the npm name and owner with Rahul, then publish in the order above.
- Find the Claude policy that refuses sends to another address (see The tools) and record its text and date. Run the transfer and create-asset writes once on a phone and record it. The last recorded phone check is from 1 September.
- UPSTREAM_READ_TOKEN is not set on sarvalabs/moi-mcp, so the upstream watch has never been able to read go-moi or cocolang. Create a fine-grained read-only token from an account that will stay (Rahul decides which) and set it. Issue #17 (js-moi-sdk v0.9.0-rc3) is still open; npm latest is still 0.9.0-rc2 on 13 October, so the pin matches npm.
- Agree who syncs the copy into voyage-api and who runs the deploy from now on, or replace the copy with an install of the published package once it exists.
- Fix docs/handoff-infra.md in moi-mcp: it clones github.com/sarvalabs-adithya/moi-mcp instead of sarvalabs/moi-mcp, and uses mcp.moi.technology, which does not exist, nine times (checked 14 October 2026). The README's tool counts were fixed by #27.
- Settle who is notified of moi-mcp issues. Issue #17 sat for two weeks with no comment.
