Branch of `moi-launchpad-ops` (front door: `../SKILL.md`).

# MOI Agent Explorer: operate it

`$SKILLS`, the operator, `ASK:`, the house rules and the gates are in `moi-launchpad-ops/SKILL.md` and `moi-devrel/SKILL.md`; this guide adds what is specific.

## What this covers
The Agent Explorer is the public directory of agents on MOI's on-chain agent registry: a React client, an Express and MySQL server, built from `sarvalabs/agent-explorer` (private) by GitHub Actions and deployed to a VM. This branch holds six runbooks (health, ship a change, change a setting, bring the index back in step, verify agents, roll back) and a symptom table. Facts are as of 2026-10-03, updated 2026-10-14: PR #5 was merged on 7 October 2026 and is live. PR #6 (deprecated agents never listed, never auto-verified; the Deprecated filter was dropped) was merged on 14 October as `aa9488c6` but is not live: the deploy fails at "Login to GHCR" (see the first row below).
Who owns it, plainly. `project-handover-docs/LIST-OF-DEPENDENCIES.md` (section 10, the 4 October snapshot) says Gokul owns the app code, admin and verification rules and the registry, DevOps (Upendhar) the workflow, VM, nginx, SSH key, GHCR token and DNS, and that the database is DevOps's. The non-merge commits on `main` (local ref, 2026-10-03) are Gokul 28, Upendhar 24 and the previous operator 8, of 60. PR #5, the previous operator's, was merged on 7 October 2026 (18:57 UTC). Whether DevRel owns the Explorer is not settled. ASK: Rahul. Only Upendhar is recorded as able to act on the VM. The rest is in `references/architecture.md`, section 7.
Not covered: the Launchpad itself (`moi-launchpad-ops/SKILL.md`), the MCP server (`moi-mcp-ops`), the website, Dataroom and Points (`moi-web-products-ops`), the order of work across products after a devnet reset (`moi-devnet-reset`), commits, PRs and merges (`moi-devrel/ship`), drafts of messages to Gokul or Upendhar (`moi-devrel/templates/messages.md`), claims in public text (`moi-devrel/claim-check`). The Voyage explorer is a different product with no skill in this library; ASK: Gokul.

## Before you start
Run commands from a working copy of `sarvalabs/agent-explorer` with every path quoted, unless the command names `$SKILLS`. The health script needs no working copy and no key. File names such as `references/x.md` are inside this branch (`moi-launchpad-ops/explorer/`); the Launchpad's own `references/` holds files with seven of the same names.
- [ ] What was seen, in the operator's words, and where. The operator provides it. Ask: "What did you see, on which page or address, and when?"
- [ ] Whether the old agents or the frozen directory began after a wipe, a new registry id or a network upgrade. The operator provides it. Ask: "When did it start, and did a devnet wipe or upgrade come first?" If it may have, run `moi-devnet-reset` first (its script `bash "$SKILLS/moi-devnet-reset/scripts/reset-detect.sh"` only reads) and come back here if it shows no reset.
- [ ] For a change: the PR number or branch. Ask: "Which change, and is it merged?"
- [ ] A work GitHub login with read access to the private repo. ASK: Rahul. Then, with `PREFLIGHT_WORK_DOMAINS` and `PREFLIGHT_EXPECT_GH_LOGIN` set as `moi-devrel/SKILL.md` says, run `bash "$SKILLS/moi-devrel/scripts/preflight.sh"` from inside the repo.
- [ ] A working copy of `sarvalabs/agent-explorer`, for any step that reads or edits code. If there is none, `gh repo clone sarvalabs/agent-explorer` is a GATE (a download: state the source). Health and symptom work need none.
- [ ] Who approves the change. No required review is recorded. ASK: Rahul, then Gokul.
- [ ] For anything on the VM, Upendhar, through the operator. The channel is not fixed. ASK: Upendhar.
- [ ] For an admin action, the operator's own MOI Wallet, and whether its address is an admin address on the server (unknown). ASK: Gokul.
- [ ] For a chain comparison, the registry's current id and agent count. ASK: Gokul.

## The run
Woken by "the site is down": do step 1, read the FAIL lines, then step 2. Every runbook below is a numbered table: read-only check first, the change second, the verification last, GATE on every step that changes anything.

| # | Step | What to do | Where or command | Done when |
|---|---|---|---|---|
| 1 | Read the state | Run the read-only check and keep the output | `bash "$SKILLS/moi-launchpad-ops/explorer/scripts/explorer-health.sh"` | You have PASS, WARN and FAIL lines. FAIL is an outage, WARN a stale or odd state |
| 2 | Pick the runbook | Match the output or the report to the table under "Which file to read" | `references/` | One runbook is chosen |
| 3 | Check who acts | The app and registry are Gokul's. The VM and database are DevOps's, and Upendhar is the recorded contact. A step for either is a drafted message, sent by the operator | `references/architecture.md` section 7 | Each step has an owner or an ASK |
| 4 | Draft locally | Edit, build and read in a working copy. Nothing leaves the machine | the runbook | A diff or a plan exists |
| 5 | Ask for each GATE | Show the exact action: repo, branch or PR, what it deploys, the account. Wait for a yes that names it | Gates below, and in `moi-launchpad-ops/SKILL.md` | The yes is in this conversation |
| 6 | Do the gated step | Claude runs only what the yes covers. A wallet signature is the operator's own act in the browser | the runbook | The step finished without error |
| 7 | Verify | Run step 1 again, then the proof specific to the change. A green workflow run proves nothing | `references/ship-a-change.md` section 3 | No FAIL, the proof holds, the result is saved |
| 8 | Hand back | Use the format at the end | Hand-back | The operator has read it |

Where to keep things. Keep saved outputs and drafted messages in a scratch folder outside every repository: they name private repo paths and internal people. If one must sit inside a working copy, add its name to `.git/info/exclude` (a local ignore rule nobody else sees) and never stage it.

## Which file to read
| Doing or symptom | Read |
|---|---|
| Site or API down, 5xx, a red deploy run, an error message | `references/troubleshoot.md`, then `references/rollback.md` |
| What a check proves, WARN lines, checks on the VM | `references/health.md` |
| Directory old or small, `/admin/sync` 404 (a rollback past PR #5), after a devnet reset | `references/index-sync.md` |
| Merge a PR, deploy a change, point at a new registry id | `references/ship-a-change.md` |
| Mark an agent verified, what "verified" means | `references/verify-agents.md` |
| Undo a bad deploy | `references/rollback.md` |
| A variable, a secret, a setting | `references/settings-and-secrets.md` |
| What the app is, where the registry id sits, what is on which branch | `references/architecture.md` |
| Why something failed with no error | `references/traps.md` |
| Testing a change to this branch or to the script | `evals/evals.md`, then `python3 "$SKILLS/moi-launchpad-ops/explorer/scripts/selftest.py"` |

## Facts that fail silently
| Rule | The incident |
|---|---|
| A merge to `main` is a production deploy, and a pull request runs nothing | The workflow runs on a push to `main` or by hand, with no test or lint step. PR #3 merged on 2026-09-24 and a successful run is recorded that day |
| A merged PR is not live until the deploy run is green | The `GH_TOKEN` secret (set 31 July) is expired or revoked, so the run fails at "Login to GHCR" (failed 7 October and 14 October; the 24 September run worked). The live site is a build from 8 October, deployed by hand, so PR #6 is not live and 70 deprecated agents still show as verified. Upendhar has been asked to replace `GH_TOKEN` and re-run |
| `/health` ok and a green run prove little. The API reports no version | On 2026-10-03 `/health` was ok, the index held 49 rows and `GET /admin/sync` was 404 |
| PR #5 is merged (7 October 2026) and live. A schema change in `initSchema()` still migrates the production database at the first boot of the new container | `GET /admin/sync` answered 404 on 2026-10-03 and 200 on 14 October (the reconcile ran: onChain 174, refreshed 174, failed 0, verified 120); the client has "Sync Registry Now". PR #5 added a column and updated rows at its first boot |
| The registry id is pinned in several places, and the package reads it once at load | The Explorer's code moved to the new registry 11 days after the 2026-09-11 wipe, and a server built from `main` probably still loaded the old id (inferred from the code; `references/traps.md`, rows 9 and 10) |
| The server gets only the variables the workflow lists | `MOI_WS_URL`, `MOI_READ_CALLER_ADDRESS` and `SYNC_INTERVAL_HOURS` are not passed, so the server runs on code defaults unless the VM differs |
| No code deletes a row | Old-chain and test rows stay until a database write removes them |
| The old containers are removed before the new ones start, and nothing rolls back | The production containers carry names that end in `-test`. ASK: Upendhar for the names before any command that names one |
| Verified is not audited, and the rule keeps changing | Four different rules were written between 2026-09-22 and 2026-10-02, the last in PR #5, merged on 7 October 2026 (`references/verify-agents.md`) |
| PR #5's commit carried an AI co-author trailer, against house rule 4 | Commit `508be01`, 2026-10-02. PR #5 is merged, so merged history is not rewritten; keep the trailer out of new commits |

The full list is `references/traps.md`.

Agent Explorer: A security finding is open on this product as of 2026-10-02. The handover note is not recorded (the previous DevRel's notes); ASK: Rahul before touching its admin.

## Gates
The gates in `moi-launchpad-ops/SKILL.md` apply here: push, PR, secrets and variables, database writes, the VM, messages, downloads, identity. Nothing below happens without the operator's explicit yes in this conversation, naming the action. What this branch adds or sharpens:
- A merge to `main` is a production deploy. A manual workflow run, any deploy and any rollback are gated. Rewriting pushed history is gated.
- Deleting an Actions secret or variable in the repo or the `PROD` environment: GitHub cannot return a secret's value, so a deletion cannot be undone. The operator types a value at a hidden prompt.
- A database migration or any write to the production database: a schema change at the first boot of a new container, pruning rows, `npm run sync`.
- An admin write on production: verifying or un-verifying an agent, a signed sync, changing the server's admin list. The operator signs in the wallet; Claude never signs. The Agent Explorer line above comes first.
- Anything on the VM: Claude drafts the message, the operator sends it to Upendhar.
- Download: `git clone`, `gh repo clone`, `git fetch`, `npm ci`, an installed package. State source and size.
- A message to Gokul, Upendhar, Rahul or anyone else, and any post or upload (a PR or issue comment, a new issue, a file in cloud storage): Claude drafts, the operator sends.
- A browser registration test, which spends devnet fuel.
A yes covers the one action it names.

## Keys and access
Names only: `moi-devrel/references/keys-and-access.md`, and `references/settings-and-secrets.md` for this product. The health script needs none. A change needs a GitHub login with access to the private repo, a repo admin for any secret or variable, DevOps for the SSH key, GHCR token and database, and an admin wallet for verification. Access is TBD for all; the owner settles it (ASK: Rahul). Never open an `.env` file. Claude never handles a recovery phrase, including a throwaway one. If one is pasted, do not repeat it, tell the operator it is exposed, and use the MOI Wallet extension and the operator's own account.

## Hand-back
```
Produced: <what, with exact path or URL>
State before and after: <the health script's PASS/WARN/FAIL counts and the index total, with the date>
Remaining: <numbered, each with its owner>
Not verified or simulated: <say so, or "none">
Ready: yes or no, because <one reason>
Next steps: <one to three>
```
A status lists only work that was done. A to-do is labelled as one.
