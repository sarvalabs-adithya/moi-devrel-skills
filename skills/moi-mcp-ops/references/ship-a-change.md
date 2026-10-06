# Ship a change to the MOI MCP server

Merging in `sarvalabs/moi-mcp` deploys nothing. Production runs a copy kept in `sarvalabs/voyage-api` and a person starts the deploy by hand (`architecture.md`). Facts are as of 2026-10-02 (research) and 2026-10-03 (live reads). Back to `../SKILL.md`.

**Column "Gate".** `read` changes nothing. `local` changes only files in your own working copy. `GATE` needs the operator's explicit yes that names the action (`moi-devrel/references/consent-and-identity.md`, section 1): Claude states the exact action, waits, then does that and nothing more. Example: "Ready to run workflow 'Deploy MOI MCP Gateway' in sarvalabs/voyage-api on feat/moi-mcp with deploy_target=dev. Short outage on the dev copy. Yes?"

**Access you need before step 1.** A GitHub login that can read `sarvalabs/voyage-api` (private) and run its Actions, and a work identity (`moi-devrel/references/consent-and-identity.md`, section 2). ASK: Rahul who grants both. Whether you push to a fork or to `sarvalabs/moi-mcp` directly: ASK: Rahul. **How the `moi-mcp/` folder is copied into voyage-api is written nowhere** (no script, no doc): ASK: Adithya.

## Part 0: read what is live before changing anything

| # | Step | Do this | Done when | Gate |
|---|---|---|---|---|
| 1 | What production runs | `bash "$SKILLS/moi-mcp-ops/scripts/mcp-health.sh" --github`. Then, with voyage-api access: `gh run list -R sarvalabs/voyage-api --branch feat/moi-mcp --limit 15`, and for a deploy run `gh api repos/sarvalabs/voyage-api/actions/runs/<id> --jq '.triggering_actor.login, .created_at, .conclusion'`. And `gh pr list -R sarvalabs/voyage-api --base feat/moi-mcp --state all --limit 15` | You can say who last deployed, when, which sync PR is merged and which is open (#313 was open and unreviewed on 2026-10-02). This also answers "who triggers the production deploy", unknown in the research | read |
| 2 | What master has that production lacks | Read master's recent commits without a clone, with the command under this table. Compare with the sync PRs of step 1. Production reports 0.1.0 for every build, so use the tool count and the OAuth lines of the script | A list of merged-but-undeployed changes | read |

```
gh api "repos/sarvalabs/moi-mcp/commits?sha=master&per_page=20" --jq '.[] | .commit.committer.date[:10] + " " + (.commit.message | split("\n")[0])'
```

## Part A: change and test in `sarvalabs/moi-mcp`
Run every command of this part from your working copy of `sarvalabs/moi-mcp`. If you have none, `git clone https://github.com/sarvalabs/moi-mcp.git` makes one; a clone is a download and is covered by the yes of step 3.

| # | Step | Do this | Done when | Gate |
|---|---|---|---|---|
| 3 | Clone or fetch, and install | `git clone` or `git fetch origin`, and `npm ci`, download from GitHub and npm. One yes covers them: "Ready to clone or fetch sarvalabs/moi-mcp and install its locked dependencies in <folder>. Yes?" | Clean tree on the latest `master` | GATE |
| 4 | Branch | `git switch -c <branch> origin/master` | On your branch | local |
| 5 | Change, with a test | Every bug fixed gets a test that would have caught it (`docs/testing-plan.md`). Do not add a write path nobody has approved on a phone (`docs/publishing.md`) | The test fails without the change and passes with it | local |
| 6 | Run what CI runs | `npm run typecheck && npm test && npm run build && node dist/cli.js help`. CI does this on Node 20, 22 and 24 (`.github/workflows/ci.yml`); use Node 20 at least, the VM runs 20.14.0 | All pass. `npm audit` is non-blocking by design (a known advisory comes through js-moi-sdk) | local |
| 7 | Packed install | If you touched `package.json`, a bin or start-up: repeat CI's step "HTTP bin starts through the npm symlink" by hand in a scratch folder (`npm pack`, install the tarball there, start `moi-mcp-http`, GET `/health`). The install downloads from npm | `/health` says `"ok":true` with nothing configured | GATE (the install), then local |
| 8 | New variable? | Read `git diff origin/master -U0 -- src` for added lines that read `process.env`. Any name that is new, or newly required, must reach the VM: the Voyage workflow passes only a fixed list (`settings-and-secrets.md`) | A list of names, each marked "workflow already passes it" or "part B must edit the workflow" | read |
| 9 | Open the PR | Push the branch and open a PR to `master`. Body: what changed, how verified, what is not verified, "Deploy: not run". No AI footer | PR open, CI running | GATE |
| 10 | Merge | CI green on all three Node versions, review done, then merge. Say aloud: this deploys nothing | Merged, the commit id noted | GATE |

## Part B: sync the copy into `sarvalabs/voyage-api`

| # | Step | Do this | Done when | Gate |
|---|---|---|---|---|
| 11 | Branch | In a working copy of `sarvalabs/voyage-api` (private; a clone is a download, so GATE with the ask of step 3): a branch from `feat/moi-mcp`, for example `moi-mcp/sync-master` (the name used for #310 to #313) | On that branch | GATE (clone), then local |
| 12 | Replace the folder | Make `moi-mcp/` equal master's tree at the commit from step 10. Method unknown: ASK: Adithya. Whatever the method, check it: `git diff --stat feat/moi-mcp` lists paths under `moi-mcp/` only, and the tree matches `git ls-tree -r <sha>` of moi-mcp | Only `moi-mcp/` changed, and you can name the source commit | local |
| 13 | Open the sync PR | Title `chore(moi-mcp): sync subtree <date or sha>`, **base `feat/moi-mcp`** (not `develop`). Body: what it brings, deployment notes (variables added or required, pairing format changes), what is unverified, "Deploy: not run" (the layout of #313). Opening it starts `moi-mcp.preview.yml`, which deploys a preview on the dev VM. Say so in the ask | PR open, the preview run started | GATE |
| 14 | Check the preview | `bash "$SKILLS/moi-mcp-ops/scripts/mcp-health.sh" --write-host pr-<N>-mcp.preview.voyage.moi.technology --no-read --no-rpc` (host pattern from the research: confirm it in the run log) | PASS on health, issuer, tool list. A WARN on the registry is expected until the registry id is updated | read |
| 15 | Review | Someone on the Voyage side reviews. #313 sat open and unreviewed from 2026-09-23 to at least 2026-10-02. ASK: Rahul who reviews, ASK: Srikar | Approved | GATE if you request review |
| 16 | Merge the sync PR | Into `feat/moi-mcp`. This deploys nothing | Merged | GATE |

## Part C: deploy to dev

| # | Step | Do this | Done when | Gate |
|---|---|---|---|---|
| 17 | Run the workflow | GitHub, voyage-api, Actions, "Deploy MOI MCP Gateway", Run workflow, branch `feat/moi-mcp`, `deploy_target` = `dev`. Command form (inferred, the Actions page is the observed route): `gh workflow run moi-mcp.deploy.yml -R sarvalabs/voyage-api --ref feat/moi-mcp -f deploy_target=dev`. If the page does not offer the workflow: ASK: Srikar (the evidence does not say whether it must exist on `develop`) | Run started | GATE |
| 18 | Watch it | `gh run list -R sarvalabs/voyage-api --workflow moi-mcp.deploy.yml --limit 1` for the run id, then `gh run watch <id> -R sarvalabs/voyage-api`. The last job checks the local and public `/health` URLs | Run green | read |
| 19 | Verify dev | `bash "$SKILLS/moi-mcp-ops/scripts/mcp-health.sh" --env dev`. If the sync added tools, pass `--expect-write N --expect-read M` | No FAIL, and every WARN explained | read |

## Part D: deploy to production

| # | Step | Do this | Done when | Gate |
|---|---|---|---|---|
| 20 | Tell people | A short note to the Voyage team and DevOps: what ships, when, that it is a short outage. Claude drafts from `moi-devrel/templates/messages.md` (the DevOps shapes) and checks the draft with `python3 "$SKILLS/moi-devrel/scripts/check-message.py" --to devops <draft>`; the operator sends. `moi-devrel/references/people-and-teams.md` says who is who | Sent, or the operator chose not to | GATE |
| 21 | Run the workflow | As step 17 with `deploy_target` = `production` (or `both`). It stops both gateway processes and starts them again: the server is down for a short time, and any OAuth consent or phone signing call in flight is lost | Run started | GATE |
| 22 | Verify | `bash "$SKILLS/moi-mcp-ops/scripts/mcp-health.sh"` with the expected counts, then the classes the change touches in `connect-and-verify.md` (reads first). A write path change needs a phone-approved write: GATE, the operator's wallet | No FAIL. Every class touched has a pass or a named gap | read, then GATE |
| 23 | Record | Hand-back (`../SKILL.md`): source commit, sync PR, run id, checks run, checks not run. A comment on the PR is a post: GATE | The operator has read it | read |
If a check fails after step 21, go to `rollback.md` before trying a second deploy.

A note for step 20, short and specific (`moi-devrel/references/people-and-teams.md`: one task per message, the exact action, how it will be verified). Claude drafts it, the operator sends it:
```
I am deploying the MOI MCP gateway to <dev or production> at <date, 24-hour UTC and IST>.
It restarts both processes, so it is down for a short time.
What ships: <sync PR link>.
What I need from you: <nothing, or one named action>.
I will check with the health script and a tool call and report back here.
```

## Self-hosted variant (documented in `docs/handoff-infra.md`; the evidence shows production does not use it)

| # | Step | Do this | Gate |
|---|---|---|---|
| a | Read | The process list shows the read gateway process and the write gateway process online, the write gateway as a single instance | GATE (DevOps reads it; the operator sends the ask; VM access: ASK: Upendhar) |
| b | Update | On the VM, in the running folder (ASK: Upendhar which): `git pull && npm ci && npm run build`. Never deploy an unmerged branch to the box. If the release adds `MOI_SESSION_KEY` (local branch only, not in the guides on `master`), DevOps puts it in `.env` first and nobody prints it | GATE (DevOps does it) |
| c | Restart | Reload the read gateway process, then restart the write gateway process. Restart, never reload, for the write gateway (ASK: Upendhar for the commands) | GATE (DevOps does it) |
| d | Verify | The issuer must equal `PUBLIC_URL`: `curl -s https://<host>/.well-known/oauth-authorization-server`, then the script with `--write-host` | read |

## Why each rule exists
- Merge is not deploy here: the live server matched the 2026-09-23 sync on 2026-10-03 while master was at 2026-09-24 (`architecture.md`).
- The Voyage workflow has no `.env`. It passes `WC_PROJECT_ID`, `PUBLIC_URL`, `MOI_NETWORK`, `MOI_DATA_DIR`, `HOSTED_PORT`, `LOG_LEVEL`, `NODE_ENV`, and for the read gateway `MOI_RPC_URL`. A change that makes another variable mandatory (`MOI_SESSION_KEY` is the known case, on unmerged work that is local branch only) crash-loops the write gateway after the sync unless the workflow passes it first (inferred from `docs/handoff-infra.md` plus the workflow, research 2026-10-02).
- Install from the packed tarball before a release: it caught a phantom dependency and a bin that exited silently (`docs/testing-plan.md`).
- Simulation accepts what the chain later refuses (fuel price 1 simulated and bounced at broadcast). Prove a write by its receipt (`connect-and-verify.md`).
- `ecosystem.config.cjs` in the repo is for the self-hosted guide only. The Voyage workflow does not read it.

## Not yet known
- The copy method for step 12. ASK: Adithya.
- Who triggers production deploys today, and whether production was ever deployed from `feat/moi-mcp`: step 1 answers it. ASK: Srikar.
- How long a deploy takes. Three sync PRs merged within 90 minutes on 2026-09-23 (15:57, 16:38 and 17:20 UTC); no deploy run history was read.
- Which Voyage environment holds `MOI_READ_CALLER`. ASK: Srikar.
