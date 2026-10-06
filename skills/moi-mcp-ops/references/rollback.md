# Roll back a bad MCP deploy

**There is no documented rollback for this server.** The research found none (2026-10-02). Facts are as of 2026-10-02 (research) and 2026-10-03 (live reads). Everything below is built from how the deploy works and is labelled "inferred" where it goes beyond a file. Who may run a rollback: unknown. ASK: Srikar (the Voyage deploy), ASK: Upendhar (the VM). Back to `../SKILL.md`.

Column "Gate": `read` changes nothing, `GATE` needs the operator's explicit yes naming the action.

## When to roll back (triggers proposed by this skill, not documented)
- The script shows a FAIL on `health`, the OAuth issuer, `tools/list` or `ping` right after a deploy, and a second look a minute later shows the same.
- The write gateway is crash-looping (DevOps sees the process in an errored state with rising restarts).
- The tool count dropped below the count before the deploy, or sign-in loops for every user.
A single WARN that was already there before the deploy is not a trigger. Compare against the reading you saved at step 1 of `ship-a-change.md`.

## What cannot be rolled back
- Anything already broadcast to the chain: a transfer, an asset, a mint. It is permanent. The write journal (`journal.jsonl` in the data directory) records each write as proposed, signed, broadcast, confirmed, failed or orphaned; DevOps can read it.
- OAuth consents and phone-signing calls in flight. Every deploy loses them, a rollback deploy included.
- Pairings, if the bad release changed the stored pairing format. The repo's checklist says old session records are then dropped and the journal is kept, so users pair again after a rollback too. Before you roll back past a release that changed the data directory format: ASK: Adithya.
- Never delete or move the data directory (`MOI_DATA_DIR`) as part of a rollback: it signs everyone out and un-pairs every wallet.

## Runbook: Voyage-hosted (production)

| # | Step | Do this | Done when | Gate |
|---|---|---|---|---|
| 1 | Measure | `bash "$SKILLS/moi-mcp-ops/scripts/mcp-health.sh"`, and `--env dev` to see whether dev is fine. Keep the lines | You know what is broken and what still works | read |
| 2 | Find the last good build | `gh run list -R sarvalabs/voyage-api --branch feat/moi-mcp --limit 15` for the previous successful production run, and `gh pr list -R sarvalabs/voyage-api --base feat/moi-mcp --state merged --limit 10` for the sync PRs. The last good build is the sync before the bad one | A commit on `feat/moi-mcp` you can name | read |
| 3 | Option A: revert the sync (inferred) | In a voyage-api working copy, branch from `feat/moi-mcp`, `git revert` the bad sync commit (add `-m 1` if it is a merge commit; the merge style of #310 to #313 is not recorded), push, open a PR into `feat/moi-mcp` titled `revert(moi-mcp): sync subtree <sha>`, merge | The branch holds the old `moi-mcp/` folder | GATE (push and PR), GATE (merge) |
| 3b | Option B: deploy an older ref (inferred) | Make a branch at the last good commit and run the workflow with that branch. Whether the workflow accepts another branch, or an environment rule blocks it, is not in the evidence. ASK: Srikar before relying on it | The run starts on that ref | GATE |
| 4 | Redeploy production | `ship-a-change.md` step 21: "Deploy MOI MCP Gateway", `deploy_target` production. It stops both gateway processes and starts them again: another short outage | Run green | GATE |
| 5 | Verify | The script; the reads of `connect-and-verify.md` part C. If sign-in was affected, a Connect from a clean browser | Back to the step 1 reading of the last good build | read |
| 6 | Tell people and record | A short message to the Voyage team and DevOps (Claude drafts, the operator sends), then a row in `troubleshoot.md` with the date, message, cause and fix | Sent, row added | GATE for the send |
| 7 | Fix forward | The bad change goes back through `ship-a-change.md` with a test that would have caught it | A new PR | GATE |

## Runbook: self-hosted guide (inferred; the guide has no rollback section)

| # | Step | Do this | Gate |
|---|---|---|---|
| a | Read | The process list and the last five commits of the running folder on the VM (`git log --oneline -n 5` there). DevOps reads it and answers; the operator sends the ask. VM access and the folder: ASK: Upendhar | GATE (a message to DevOps) |
| b | Check out and rebuild | `git checkout <sha> && npm ci && npm run build` in the running folder, done by DevOps on the VM. The install downloads from npm | GATE |
| c | Restart | Reload the read gateway process, then restart the write gateway process, done by DevOps (ASK: Upendhar for the commands). Restart, never reload, for the write gateway | GATE |
| d | Verify | The script with `--write-host` | read |
The data directory is untouched by these steps.

## Not yet known
- Whether any earlier MCP deploy was rolled back, and how. ASK: Adithya.
- Whether voyage-api keeps previous builds on the VM, or builds only from the branch each time (the workflow builds each time, so a rollback means a rebuild). ASK: Srikar.
- Whether DevOps snapshots the VM. ASK: Upendhar.
- How long a deploy or a rollback takes. Not measured.
