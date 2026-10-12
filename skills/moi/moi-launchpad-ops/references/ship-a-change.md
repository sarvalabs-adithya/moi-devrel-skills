# Ship a change to the Launchpad

Facts are as of 2026-10-03. A merge to `master` of `sarvalabs/moi-agent-launchpad` is a production deploy, about 4 minutes later, with no test gate and no alert if it fails. Commit, PR and merge mechanics and the work identity are `moi-devrel/ship`; this file adds only what is specific to the Launchpad. Run every command from your working copy of that repo. The change checklist to fill in is `../templates/change-checklist.md`. Back to `../SKILL.md`.

Gate column: `read-only` and `local` need no yes. `GATE` needs the operator's explicit yes in this conversation, naming the action. `OPERATOR` means the operator types it and Claude never sees a value.

## Run table
| # | Step | Command or action | Done when | Gate |
|---|---|---|---|---|
| 1 | Baseline | `bash "$SKILLS/moi-launchpad-ops/scripts/launchpad-health.sh"`. Then, in the working copy, `git fetch origin` (writes only to your working copy) and `git log --oneline -5 origin/master` | The health result before your change is written in the checklist | read-only |
| 2 | Who may merge | Ask who approves a merge to `master`. Not on record, and branch protection is unknown. ASK: Rahul. For chain or protocol code, Gokul is the usual reviewer (`moi-devrel/references/people-and-teams.md`) | A named approver | read-only |
| 3 | Branch | `git fetch origin` (writes only to your working copy), then `git checkout -b <topic> origin/master`. Never work on `master` or on `feature/moi-agent-launchpad-cicd`: a push to either deploys | On a topic branch | local |
| 4 | Edit | Follow "Extra steps by kind of change" below | The diff holds only the intended files | local |
| 5 | Check | `npm ci` (downloads the packages in the lockfile: say so before the first run in a working copy), then `npm run typecheck`, `npm test`, `npm run build`. Stop any dev server before the build (a build under a running dev server corrupts `.next`) | All pass. CI will not run the first two | local |
| 6 | Strict install | If `package.json` or the lockfile changed: `rm -rf node_modules && npm ci` | No ERESOLVE. A lenient local `npm install` hid one on 2026-09-14 and every deploy after PR #24 failed until PR #27 | local |
| 7 | Database | If the change needs a migration, do `database.md` first | The migration is applied and checked, or the code degrades without it | see file |
| 8 | Push | `git push -u origin <topic>`, where `origin` is the org repo in a clone of `sarvalabs/moi-agent-launchpad`. Whether you push to a fork or to the org repo: ASK: Rahul. Recent PRs came from branches in the org repo; a branch other than the two above deploys nothing | The branch is on the remote the operator named | GATE |
| 9 | Pull request | `gh pr create -R sarvalabs/moi-agent-launchpad --base master --head <topic>`. Write the body as measured evidence: what you verified against the real chain, what you did not, test counts, as the commit bodies of 942827a and a02eb26 do | The PR is open | GATE |
| 10 | Review | Wait for the approver of step 2. Do not merge on silence | An approval in writing | read-only |
| 11 | Merge | Say first: "this merge deploys to production". Merge on the GitHub page or with `gh pr merge <number> -R sarvalabs/moi-agent-launchpad --merge` (the history uses merge commits) | The merge commit is on `master` | GATE |
| 12 | Watch | `gh run list -R sarvalabs/moi-agent-launchpad -L 3`, then `gh run watch <id> -R sarvalabs/moi-agent-launchpad --exit-status` | Green. Red means production still runs the old image: go to step 14 | read-only |
| 13 | Verify | Health script again (allow a minute for `chainStatus` to leave `pending`). Then the check for your kind of change below | Same or better than step 1, and your change is visible | read-only |
| 14 | If it failed | A red run: read the failed step (`gh run view <id> -R sarvalabs/moi-agent-launchpad --log-failed`) and match `troubleshoot.md`. A bad live change: `rollback.md` | A decision, written in the incident note | read-only |
| 15 | Close | Fill in `../templates/change-checklist.md`. Hand back with the format in `../SKILL.md` | The operator has read it | local |

A manual run of "MOI Agent Launchpad CI/CD" (`gh workflow run ci-cd.yml -R sarvalabs/moi-agent-launchpad --ref master`) builds and deploys the branch you choose as `:latest`, the same as a merge. It is a GATE, and it is also how a setting change is applied (`settings-and-secrets.md`).

## Extra steps by kind of change
| You changed | Also do | Why |
|---|---|---|
| `lib/templates/` or `agent-runtime/` | `npm run build:runtime` and commit the new `public/runtime.cjs` | The bundle users download is built from them. Its hash is served at `/api/runtime/version`, and installed agents compare themselves to it and warn that they are out of date |
| `package.json` or the lockfile | Step 6. Keep the `overrides` entry that points the registry package's SDK peer at the root SDK. Install `js-moi-sdk` and `js-moi-agent-registry` together with `--save-exact` | `js-moi-agent-registry` 0.3.0-rc1 declared an exact SDK peer. Installing one alone gives ERESOLVE |
| A new environment variable read by code | Add the name to `.github/workflows/deploy.yml` in the same PR, then set the Actions secret or variable (`settings-and-secrets.md`) | `deploy.yml` rewrites `.env` on every run from a fixed list. A name it does not list never reaches the app |
| A new `NEXT_PUBLIC_*` value | Add an `ARG` and `ENV` to `Dockerfile` and a `--build-arg` to `docker-build.yml` | These are fixed at image build. A restart cannot change them. `NEXT_PUBLIC_APP_URL` is also written into every downloaded agent and every on-chain card |
| `app/api/stats/route.ts` | Keep `export const dynamic = "force-dynamic"` | Losing it made Next prerender the route at build time with no database, and the Docker build failed (commit c69470f) |
| Anything that touches the KMOI asset id, fuel price or storage fund | Read them from the SDK. Never a literal | `tests/chain-constants.test.ts` fails on a retired id or a fuel price under the floor |
| Chain writes (registration, activation, listing) | Prove success from the receipt status, never from the broadcast | Activation reported "ready" while the chain reverted it (introduced by PR #28, fixed by PR #30 on 2026-09-15) |
| Registry id or any reset follow-up | `moi-devnet-reset` | It owns the sequence across products |
| Pages, metadata, sitemap, badges | `moi-docs/geo` owns the search layer | Same deploy path applies |

## Checks for your kind of change (step 13)
| Change | Check |
|---|---|
| Any | Health script exits 0 or WARN you can explain |
| Runtime bundle | `/api/runtime/version` shows a new value. The operator downloads a setup script for a test agent they own (a download: GATE) and prints only its web addresses with `grep -Eo 'https?://[A-Za-z0-9.:-]+' <the downloaded file> \| sort -u`: the Launchpad host must be the production host, not localhost and not the old vercel.app host. The file holds that agent's private key, so Claude does not open it, and the operator deletes it after the check |
| Registry or chain read | `chain-listing` PASS twice, 30 seconds apart. A single read is a sample (see `health.md`) |
| Wallet activation | A fresh wallet, with the operator at the keyboard (it spends registration-wallet funds on devnet: GATE): the page says ready, the receipt status is 0, and the wallet shows a balance. For the full pass use `moi-devrel/test-round` (case list: `moi-devrel/test-round/references/launchpad-pass.md`) with `docs/E2E-TESTING.md` sections 1 and 13 |
| Telegram | The operator runs `getWebhookInfo` (`health.md`): no new `last_error_message` |
| Something users see | Open the page in a private window with no console errors |
No endpoint reports the running commit. To see which image runs, ask DevOps which image tag the web container runs (ASK: Upendhar), or check a behaviour you changed.

## When a full test pass is needed
For a change to registration, activation, relay, templates or payments, run a structured pass: the method is `moi-devrel/test-round`, the recorded case list is `moi-devrel/test-round/references/launchpad-pass.md`, and the source document is `docs/E2E-TESTING.md` (private repo, on `master`). The rules to keep:
- Real devnet interactions only. Say plainly in the write-up when something is simulated. Spending devnet funds is a GATE.
- Two separate funded wallets: a creator cannot buy their own agent. The extension unlocked, a Telegram account, a free Groq key, and the commit id written down (`git rev-parse --short master`).
- Download the runtime again after a template change. Testing without it tests the old code.
- Record each result with the exact message. The durable record is `docs/QA-LEDGER.md`. A full final pass is 2 to 3 hours in one sitting (`docs/E2E-TESTING.md` section 13).
- The document header still names the old vercel.app host: test the production host. The payment sections cannot pass while the market read returns `onchain: null`.

## Not yet known
- Who approves a merge, and whether branch protection exists. ASK: Rahul.
- Whether DevOps is told when the workflow fails. The evidence says no.
- Whether to push to a fork or the org repo. ASK: Rahul.
