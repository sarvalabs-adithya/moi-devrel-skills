# Ship a change to the Agent Explorer

Facts are as of 2026-10-14 where a line says so, otherwise 2026-10-03 (probe) and 2026-10-02 (research). As of 2026-10-14 the deploy run fails at "Login to GHCR" (expired `GH_TOKEN`), so a merge to `main` does not go live until Upendhar replaces the token and re-runs (`troubleshoot.md` row 17). A merge to `main` of `sarvalabs/agent-explorer` is a production deploy: the workflow has no test step, no lint step, and a pull request triggers nothing. Run every command from a working copy of that repo unless it names `$SKILLS`. `SKILLS`, `ASK:` and "the operator" are defined in `moi-devrel/SKILL.md`. The git and PR mechanics (identity, rebase, merge) are owned by `moi-devrel/ship`. Back to `../GUIDE.md`.

Kinds: READ changes nothing. EDIT changes the local working copy only. GATE needs the operator's explicit yes in this conversation, naming the action. VERIFY reads the result.

## 1. The run
| # | Kind | Step | Command or where | Done when |
|---|---|---|---|---|
| 1 | READ | State before the change. Keep the output | `bash "$SKILLS/moi-launchpad-ops/explorer/scripts/explorer-health.sh"` | The output is saved for the hand-back |
| 2 | READ | Identity and remote. Do not run `git remote -v`: a remote address can hold a token, and preflight prints the origin without credentials | `bash "$SKILLS/moi-devrel/scripts/preflight.sh"` | No FAIL. The origin it prints is `sarvalabs/agent-explorer`. The repo is private: ASK: Rahul for access |
| 3 | GATE | Get the code (a download: state source `github.com/sarvalabs/agent-explorer`). Branch from `main` | `git fetch origin` then `git switch --no-track -c <topic> origin/main` | The branch exists and `git log -1` shows the commit you expect |
| 4 | READ | Find every pinned value the change touches | `git grep -n -e AGENT_REGISTRY_LOGIC_ID -e LAUNCHPAD_ -e MOI_WS_URL -e SYNC_INTERVAL -- server client .github` | You can list each place that must change together |
| 5 | EDIT | Make the change. A new server variable needs an edit to the `docker run` block of the workflow. A new client variable needs a Dockerfile `ARG`, a `--build-arg` and code that reads that exact name. A schema change must be additive and safe to run twice (section 2) | `settings-and-secrets.md` | The diff holds the code and the pass-through |
| 6 | GATE | Install (a download of npm packages). Server and client are separate packages | `npm ci --prefix server`, then `npm ci --prefix client`, both from the root of the working copy | Both finish without error |
| 7 | EDIT | Build both exactly as the images do, and lint the client. No test suite exists in either package | `npm run build --prefix server`; `npm run build --prefix client`; `npm run lint --prefix client` | All exit 0. The lint was not run by the author of this branch: a failure that `origin/main` also has is not yours. The server build rewrites the files of `server/dist/`, which is tracked in git although the image rebuilds it. Run `git restore server/dist`, then `git status --short`, and stage files by name, never `git add -A` |
| 8 | READ | Check the commit message for an AI co-author trailer | `git log -1 --format=%B` | None. If one is there, `moi-devrel/ship` rewrites it, and a rewrite of a pushed branch is a GATE |
| 9 | GATE | Push the branch: remote, branch, files, the account that pushes | `git push -u origin <topic>` | The branch is on GitHub |
| 10 | GATE | Open the pull request: base `main`, title, body. The body states what was measured, what was not verified, and that the merge deploys to production | `gh pr create -R sarvalabs/agent-explorer --base main --head <topic> --title "<title>" --body-file <body file outside the repo>` | One PR, no AI footer |
| 11 | READ | Review. The app owner is Gokul per `project-handover-docs/LIST-OF-DEPENDENCIES.md` section 10. Whether his approval is required is not recorded. ASK: Rahul | The PR page | The operator has the reviewer's answer in writing |
| 12 | GATE | Merge. Name the PR number, the base branch and "this deploys to production". If the change edits `server/src/db/schema.ts`, say that the first boot runs it on the production database | `gh pr merge <N> -R sarvalabs/agent-explorer --merge` (the flag is needed outside a terminal prompt; PRs #1, #2 and #3 reached `main` as merge commits) | The merge commit is on `main` |
| 13 | READ | Watch the run. Successful runs took 1.8 to 2.4 minutes (2026-06-22 and 2026-09-24) | `gh run list -R sarvalabs/agent-explorer --limit 3 --json databaseId,headSha,conclusion,status,createdAt` | `conclusion` is `success` for your merge commit. A red run: `troubleshoot.md`, section 2, rows 9 and 10 |
| 14 | VERIFY | Health, then the proof that is specific to the change (section 3) | `bash "$SKILLS/moi-launchpad-ops/explorer/scripts/explorer-health.sh"` | No FAIL, and the change-specific proof holds. A green run alone proves nothing |
| 15 | VERIFY | If the change touches the index, the registry or verified flags | `index-sync.md`, section 5 | The index matches the chain |

## 2. A schema change runs on the production database
`initSchema()` runs at every boot of the backend. A new column or table is created the first time the new container starts. PR #5 (merged 7 October 2026) added `verified_by_admin` and ran `UPDATE agents SET verified_by_admin = TRUE WHERE verified = TRUE` at its first boot, so a change like it is a database migration and a write to a production table. That is a GATE in this branch: a write to a production database. Before the merge, tell Gokul, who owns the app, and Upendhar, whose team owns the database. The change cannot be undone by a rollback of the code (`rollback.md`, section 4). A change that is not additive has no mechanism here.

## 3. The proof that the change is live
The API reports no version and no commit (`/health` returns a status and a timestamp). A green run proves the build pushed, not that the site changed. Pick the proof:
| Change | Proof |
|---|---|
| PR #5, or a rollback past it | `GET /admin/sync` answers 200 with `running` and `last`. It answered 404 on 2026-10-03, before the merge, and 200 on 2026-10-14 |
| Any client change | Fetch the page, find the script file name in its HTML (it carries a hash, `index-<hash>.js` on 2026-10-03), fetch that file and search it for a string only the new build has. A changed hash alone shows a new build |
| A server route or a response field | Call it and read the new field |
| A server change with no visible effect | Add a log line in the change and ask Upendhar to read the backend container's log |
| A variable | `settings-and-secrets.md`, section 4, proof per setting |

## 4. Variants
- A manual run (GATE): `gh workflow run build-and-push.yml -R sarvalabs/agent-explorer -f branch=main -f environment=PROD`. Use it after changing a PROD variable or secret, since values reach the containers only at deploy. A manual run with another branch builds that branch, pushes it as `:latest` and deploys it to the environment you name. With PROD that is production (read from the workflow, 2026-10-03).
- A new registry id after a devnet reset: the id comes from the protocol team (Gokul), and `moi-devnet-reset` owns the order of work across products. Here, change the id in `server/src/config.ts` and `client/vite.config.ts` (PR #5 and later), set a read caller that exists on the new chain (`MOI_READ_CALLER_ADDRESS`, or unset `MOI_MNEMONIC`), check `MOI_INTELLIGENCE_LOGIC_ID`, `MOI_AGENT_ID` and `MOI_WS_URL`, ship by the table above, then run a sync (`index-sync.md`). Commit `bb5d38e` on 2026-09-22 is the worked example, eleven days after the wipe. A repository variable for the id would turn the next reset into a setting (the Launchpad does this), but the workflow passes none. PR #5 treats an empty value as unset, so adding the variable and a line in the workflow's `docker run` block is safe (confirm in `server/src/config.ts`).
- Writing the PR body: measured evidence first (what you ran against the real devnet, with numbers), then what is not verified. Public PR text cites only public artefacts and names no private path.

## Not yet known
- Whether `main` is protected or needs a review. ASK: Rahul, then Gokul.
- Whether the `DEV` and `TEST` environments exist, and what they deploy to. ASK: Upendhar.
- PR #5 was merged on 7 October 2026. The design issue the previous operator promised on 2026-09-24 (when closing PR #4) was never posted; a draft existed on his machine and is not in this repo (not recorded; ASK: Rahul).
