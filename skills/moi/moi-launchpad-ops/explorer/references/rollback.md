# Roll back a bad Explorer deploy

Facts are as of 2026-10-02 (the workflow file and the library's ops research) and 2026-10-03 (probes), updated 2026-10-14 where a line says so (PR #5 merged on 7 October 2026). No rollback procedure is documented for the Explorer. The three options below are read from the workflow and are inferred; none has been run. Nothing here is a yes: every step marked GATE needs the operator's explicit yes naming the action. `ASK:` is defined in `moi-devrel/SKILL.md`. Run `git` commands from a working copy of `sarvalabs/agent-explorer`; the `gh` commands carry `-R`. Back to `../GUIDE.md`.

## 1. What the deploy does to you
- The deploy job pulls `:latest`, removes both old containers, then starts the new ones. If the new backend never answers `/health`, the job goes red and nothing starts the old ones again. The API stays down until someone acts.
- Each build pushes `:<7-character commit id>` and `:latest` to `ghcr.io/sarvalabs`. `:latest` is mutable; the commit-id tags stay unless something prunes them. GHCR retention is unknown. ASK: Upendhar.
- A failure before the deploy job (a build error) leaves production untouched.
- Secret values cannot be read back from GitHub. The environment of a removed container is gone with it. So a restart on the VM works only if someone holds the values.
When not to roll back: a stale index with `/health` ok, or a WARN-only script result. Rolling back code fixes neither. Go to `index-sync.md`.

Triggers (inferred; none is documented for the Explorer): `/health` not ok after a deploy; the deploy job red at "Backend failed health check after 60 seconds"; `/registry/agents` answering 500; a blank site after a client change; a new `error` in `GET /admin/sync` right after a change to registry code.

## 2. The run
Kinds: READ, EDIT (local only), GATE, VERIFY.
| # | Kind | Step | Command or where | Done when |
|---|---|---|---|---|
| 1 | READ | The state now. Keep the output | `bash "$SKILLS/moi-launchpad-ops/explorer/scripts/explorer-health.sh"` | You know what is down |
| 2 | READ | The last good commit. The latest run with `conclusion` `success` before the bad one. Its image tags are the first 7 characters of `headSha` | `gh run list -R sarvalabs/agent-explorer --limit 10 --json databaseId,headSha,conclusion,createdAt,event,displayTitle` | You have one `headSha` and its run number |
| 3 | READ | What the bad deploy changed that a code rollback cannot undo (section 4). Did it touch `server/src/db/schema.ts`? If either commit is missing from the working copy, `git fetch origin` first (GATE: a download) | `git diff <good>..<bad> --stat -- server/src/db` | You can say what stays |
| 4 | READ | Choose an option (section 3) and tell the operator its cost | | The operator picked one |
| 5 | GATE | Option A: revert. Fetch (a download), then branch, revert the merge, push, open the PR and merge it. Name each action, the PR number and "this deploys to production" | `git fetch origin`; `git switch --no-track -c revert-<N> origin/main`; `git revert -m 1 <merge commit>`; then `moi-devrel/ship` for push, PR and merge | The merge is on `main` and the run starts |
| 6 | GATE | Option B: a manual run of the last good ref. Name the ref and the environment | `gh workflow run build-and-push.yml -R sarvalabs/agent-explorer -f branch=<good ref> -f environment=PROD` | The run starts |
| 7 | GATE | Option C: Upendhar pulls the earlier images and recreates the two containers. Only if GitHub Actions is unavailable and he holds the environment values | ASK: Upendhar. Draft it from `moi-devrel/templates/messages.md` (the DevOps drafts) | He confirms both containers are up |
| 8 | READ | Watch the run (A or B) | `gh run list -R sarvalabs/agent-explorer --limit 3 --json databaseId,headSha,conclusion,status` | `success` for the ref you chose |
| 9 | VERIFY | Health, then the proof that the old behaviour is back (section 5) | the script | No FAIL, and the proof holds |
| 10 | READ | Hand back the cause as far as known, what stays (section 4), and the next step. Do not merge the bad change again until it is fixed | | The operator has it |

## 3. The options
| Option | How | Time | Cost and risk |
|---|---|---|---|
| A. Revert on `main` | Revert the merge commit, PR, merge. The push redeploys | About 2 minutes of workflow once merged, plus review time | The cleanest: `main` then matches production. Needs push, PR and merge yeses. Successful runs on 2026-06-22 and 2026-09-24 took 1.8 to 2.4 minutes |
| B. Manual run of an older ref | The workflow passes `branch` to the checkout as `ref`, so a tag or commit id likely works (inferred, untested). It builds that ref and deploys it as `:latest` | Same | Fast, but `main` still holds the bad commit, so the next merge or push to `main` redeploys it. Follow with option A |
| C. The VM, by hand | Pull `ghcr.io/sarvalabs/agent-explorer-backend:<sha>` and `agent-explorer-frontend:<sha>`, remove both old containers (DevOps knows their names; ASK: Upendhar), start both again with the options of the workflow's `docker run` block at that commit | Unknown | Needs the secret values, which only the holder has. A mistake takes the site down further. Never paste `docker inspect` output: it prints the values. The frontend image carries its `VITE_*` values from its own build, so it needs none |

## 4. What stays after a rollback
| Stays | Why |
|---|---|
| Rows the bad build wrote to MySQL | A sync adds and updates rows and nothing deletes them. Admin verify decisions persist |
| New columns | `initSchema()` only adds. PR #5 added `verified_by_admin` and set it to true wherever `verified` was true. An earlier build ignores the column (inferred) |
| On-chain registrations users made through the client | They are interactions on devnet. The Explorer neither made nor holds them |
| The mutable `:latest` tag | It points at whatever was built last. Option A or B moves it |
Removing rows is a separate decision: `index-sync.md`, section 5, step 6, with Gokul's yes and a backup from Upendhar.

## 5. Proof the old behaviour is back
| Rolled back past | Proof |
|---|---|
| PR #5 | `GET /admin/sync` answers 404 again |
| A client change | The page names a different script file, and a string only the bad build had is gone |
| A server route or field | Call it and read the old shape |
| A variable | `settings-and-secrets.md`, section 4, proof per setting |

## Not yet known
- GHCR retention for the Explorer images. ASK: Upendhar.
- Whether Upendhar or anyone else holds the environment values for option C. ASK: Upendhar.
- Whether a VM snapshot or a database backup exists. None is documented. ASK: Upendhar.
- Who may trigger a rollback, and whether anyone's approval is needed first. Nobody is named. ASK: Rahul.
