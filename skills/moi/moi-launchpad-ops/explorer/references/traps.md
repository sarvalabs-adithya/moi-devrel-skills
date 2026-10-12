# Facts that fail silently on the Agent Explorer

Each row is a rule with the evidence behind it. Facts are as of 2026-10-03 (probes and a re-read of the code in the previous operator's clone of `sarvalabs/agent-explorer`) and 2026-10-02 (research). `ASK:` is defined in `moi-devrel/SKILL.md`. Back to `../GUIDE.md`.

Agent Explorer: A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin.

## Deploy
| # | Rule | The incident or evidence |
|---|---|---|
| 1 | A merge to `main` is a production deploy, and a pull request runs nothing | `build-and-push.yml` triggers on a push to `main` and on a manual run. It has no test and no lint step. PR #3 merged on 2026-09-24 and a successful run is recorded that day |
| 2 | A manual run with another branch and the environment PROD builds that branch, pushes it as `:latest` and deploys it to production | The checkout uses `inputs.branch`, and the deploy job always pulls `:latest` (read from the workflow, 2026-10-03; not run) |
| 3 | The production containers carry names that end in `-test` | Any log, stop or rollback command must use their real names. ASK: Upendhar for them |
| 4 | The old containers are removed before the new ones start, and nothing starts them again | `docker rm -f` precedes `docker run`. A failed health loop turns the job red and the API stays down |
| 5 | A green run proves the images were pushed, not that the site changed | The API reports no version. Prove a change with the proof of `ship-a-change.md`, section 3 |
| 6 | A failed build leaves production alone, a failed deploy step does not | The deploy job needs the build job. A failure in the deploy step leaves the containers replaced |
| 7 | `server/dist/` is tracked in git, but the image rebuilds it | Never edit it. The server image copies the tree then runs `npm run build`. A local server build rewrites those tracked files (the copy on `main` was last committed 2026-09-08), so `git add -A` would commit build output. Run `git restore server/dist` and stage by name |

## Config
| # | Rule | The incident or evidence |
|---|---|---|
| 8 | The registry id lives in several places, and the workflow's build argument for it is dead | `server/src/config.ts`; `client/vite.config.ts` on PR #5; the example in `.env.example`; and `VITE_AGENT_REGISTRY_LOGIC_ID`, which the workflow passes and no client code reads |
| 9 | The registry package embeds an old id and reads the variable once at load | `main` sets it inside `getRegistryClient()`, too late, so a server built from `main` reads the package's embedded id, the wiped `c684f926` (inferred from the code and commit `bb5d38e`). PR #5 pins it at the top of `config.ts`, imported first (`508be01`) |
| 10 | After a devnet reset the Explorer moved to the new registry 11 days late | Wipe 2026-09-11, Launchpad moved 2026-09-15, Explorer 2026-09-22, MCP 2026-09-23 (`moi-devrel/references/devnet.md`) |
| 11 | The server gets only the variables the workflow lists | `MOI_WS_URL`, `MOI_READ_CALLER_ADDRESS`, `SYNC_INTERVAL_HOURS`, `LAUNCHPAD_*` and `PINATA_JWT` fall back to code defaults |
| 12 | A client variable needs three things: a Dockerfile `ARG`, a `--build-arg`, and code that reads that exact name | `VITE_PARTICIPANT_BASE_URL` and `VITE_PUBLIC_URL` are read and never passed |
| 13 | With `MOI_MNEMONIC` set, the server never falls back to the read-only caller, even if the wallet is gone | `makeSigner()` on PR #5 checks only that the mnemonic is non-empty. `.env.example` says the fallback also covers a missing wallet. The code does not |
| 14 | The read caller default is an address chosen for one registry | `MOI_READ_CALLER_ADDRESS` and the WebSocket address are code defaults and go stale after a reset |
| 15 | Setting names changed across branches, and an unknown name is ignored silently | `main`: `LAUNCHPAD_ORIGIN`. PR #5: `LAUNCHPAD_HOSTS`. Closed PR #4 and DEPENDENCIES.md: `LAUNCHPAD_ORIGINS`, `LAUNCHPAD_CONFIRM_ORIGIN`. Removed 2026-09-23: `AUTO_VERIFY_OWNERS`, `LAUNCHPAD_API_KEY`, `LAUNCHPAD_POLL_SECONDS` |

## The index
| # | Rule | The incident or evidence |
|---|---|---|
| 16 | `/health` ok proves the process only | On 2026-10-03 `/health` was ok while the index held 49 rows and `GET /admin/sync` was 404 |
| 17 | No code deletes a row | No DELETE, TRUNCATE or DROP in `server/src` on `main` or PR #5. Old-chain rows and test rows stay until someone removes them with a database write |
| 18 | The WebSocket listener adds unknown ids only | It never refreshes a row. A status or card change needs a full sync or, on PR #5, a reconcile |
| 19 | The library's own WebSocket reconnect leaks until the process dies | Commit `4618591`: the code drives reconnection with one timer. Do not turn the option on |
| 20 | The registry returns at most 25 ids per call (50 in the unposted draft, unconfirmed) | `main` advances its page by 100 and so skips ids. PR #5 advances by what came back |
| 21 | The node rejects reads built by `js-moi-sdk` 0.8.0 | Said in the PR #5 commit message. `main` pins `^0.8.0`, so a sync on `main` cannot finish against the current devnet (inferred) |
| 22 | The scheduled reconcile starts its clock at boot | The first run is one interval after the container starts, so deploys more often than that mean it never fires (PR #5) |
| 23 | A schema change in `initSchema()` runs on the production database at the first boot | PR #5 adds `verified_by_admin` and updates every verified row. That is a migration and a write to a production table |
| 24 | Do not run `npm run sync` from a laptop against production | It needs the database credentials and writes to the table. On the VM it runs in the backend container (inferred). ASK: Upendhar |

## Verification and words
| # | Rule | The incident or evidence |
|---|---|---|
| 25 | Verified is not audited | Four different rules were written between 2026-09-22 and 2026-10-02, the last on the unmerged PR #5 (`verify-agents.md`, section 1). Say "marked verified by the admins or by the Launchpad rule", with a date |
| 26 | On `main` an admin un-verify of a Launchpad-card agent is undone at the next upsert | The update is `verified OR new` (`agents.ts`). PR #5 keeps an admin choice in `verified_by_admin` |
| 27 | There are two explorers | The Agent Explorer lists agents (agents.moi.technology). The Voyage explorer (voyage.moi.technology) shows interactions and hosts the faucet, and it can lag by minutes |
| 28 | Say "devnet" and "network ID" in prose | `moi-devrel/references/terminology.md`. The variable names `VITE_MOI_NETWORK` and `VITE_MOI_CHAIN_ID` stay as written |
| 29 | A count of agents in public text carries a date and its source | 49 rows on 2026-10-03 is the directory's index, not the registry's count. `moi-devrel/claim-check` |

## Files and history
| # | Rule | The incident or evidence |
|---|---|---|
| 30 | DEPENDENCIES.md section 11 is partly stale | It lists `js-moi-sdk` 0.9.0-rc2 (probably written from the PR #5 branch, inferred; `main` pins `^0.8.0`) and the `LAUNCHPAD_ORIGINS` names of a closed PR. It is the previous operator's file, untracked and local to his machine. ASK: Adithya for a copy |
| 31 | The design issue promised on 2026-09-24 was never posted | PR #4 was closed with a promise to open an issue first. A draft exists on the previous operator's machine, untracked. It predates PR #5 |
| 32 | `server/check-registry.mjs` is untracked | It exists only in the previous operator's clone. ASK: Adithya for a copy (`index-sync.md`, section 4) |
| 33 | PR #5's commit message carries an AI co-author trailer | Commit `508be01` (2026-10-02) came after the 2026-10-01 cleanup of six other repos' open PRs. House rule 4 applies. Merged commits such as `bb5d38e` carry one too, and merged history is not rewritten. A rewrite of PR #5 is a GATE (`moi-devrel/ship`) |
| 34 | There is no handover document | `client/README.md` is the unmodified Vite template. This branch is the first written runbook |

## Not yet known
- Whether the production container sets variables beyond the workflow. ASK: Upendhar.
- Whether PR #5 changed after 2026-10-02. ASK: Adithya, or `gh pr view 5 -R sarvalabs/agent-explorer`.
