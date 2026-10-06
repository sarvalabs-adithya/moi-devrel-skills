# Merge and deploy: what a merge starts, and how to confirm it is live

Facts are as of 2026-10-02 from the ops research notes and the workflow files, re-read 2026-10-03 in the previous operator's clones as last fetched. For each product's full deploy path, accounts and health answers, `moi-devrel/references/repo-map.md` is the map ("How things deploy", "Read-only health checks"). Runbooks per product: `moi-web-products-ops` (Website, Dataroom, Points), `moi-launchpad-ops`, `moi-launchpad-ops/explorer`, `moi-mcp-ops`, `moi-docs` (docs sites). Posts: `moi-blog`. Back to `../GUIDE.md`.

## 1. The rule
Merging to a deploy branch is the release. There is no staging step in front of production. Of the five deploying products (Website, Dataroom, Points, Launchpad, Explorer), none runs tests on a pull request: the Website's PR workflow only builds a preview, and the other four run only on a push or by hand. `js-moi-sdk` runs its tests on a PR (`test.yml`) and `voyage` runs an audit scan on PRs to `develop` (`audit.yml`), as of the clones last fetched. A green run proves the script finished, not that the change is live: deleted blog posts survived deploys in August 2026 and the homepage calendar hides a dead API. Always read the live page.

## 2. What each merge starts
| Repo and PR base | A merge starts | Confirm live (GET only) | Roll back |
|---|---|---|---|
| `MOI-Website`, `main` | "Deploy MOI Website": Teleport, then the VM script. Both the site and the blog build. A merged post opens a second PR with social copy within about a minute (26 seconds on 2026-09-11); nothing is announced | `curl -sI https://moi.technology/`, `curl -s https://moi.technology/api/health`. A post: `python3 "$SKILLS/moi-blog/scripts/check-live.py" <slug>`. The apex answers 200 for any address, so read the page | Revert PR. Time not recorded |
| `moi-dataroom0`, `main` | "Deploy MOI Dataroom": SSH, then the VM script. No health check after | `curl -sI https://dataroom.moi.technology/` (307 to `/home`), `curl -s https://dataroom.moi.technology/api/documents` and read every `embedding_status` | Revert PR |
| `moi-project` (Points), `feature/ci-cd` | Image to GHCR, Teleport, then the old container is removed and the new one started. About 4 to 5 minutes (inferred from run times). Startup refuses to boot if migrations are behind or an enabled task lacks its env | `curl -s https://points.moi.technology/api/health`: healthy, database ok, `migrations.applied` equals `expected`. It reports `sha: null`, so it cannot tell which build runs | No rollback input at the branch tip (draft PR #15 adds `image_tag`). Revert PR. Apply a database change first |
| `moi-agent-launchpad`, `master` | "MOI Agent Launchpad CI/CD", about 4 minutes: image, Teleport, compose up. A red run leaves the old image serving and tells nobody. A docs-only merge deploys too (inferred from the trigger) | `curl -s https://launchpad.moi.technology/api/stats` shows `"chainStatus":"ok"`; it can say pending or stale for about a minute | `git revert -m 1 <merge commit>` PR, merge, about 5 to 10 minutes. Database changes and on-chain effects are not undone |
| `agent-explorer`, `main` | "Build Push and Deploy Agent Explorer", about 2 minutes. Old containers go first. Containers are named `-test` even in production | `curl -s https://api.agents.moi.technology/health`, then compare `/registry/agents` total with the chain; `ok` only proves the process is up | Revert PR on `main`. No automatic rollback |
| `moi-mcp`, `master` | Nothing deploys | n/a | n/a |
| `voyage-api`, `feat/moi-mcp` (the sync PR) | Nothing until someone runs the manual workflow "Deploy MOI MCP Gateway" (dev, production or both). A short outage per deploy | `curl -s https://mcp.voyage.moi.technology/health` and the same on `mcp-read.voyage.moi.technology`: `"ok":true` | Revert the sync commit on `feat/moi-mcp`, run the workflow again |
| `voyage`, `develop` | Image `voyage-ui` built through GitHub Actions and Teleport. Commits need a conventional type prefix such as `feat:` or `fix:` (commitlint) | Open voyage.moi.technology. A health read is not recorded | Not recorded |
| `moidocs`, `voyage-docs`, `coco-docs`, `main` | Cloudflare Pages publishes. Every branch gets a preview URL | Open the page on docs.moi.technology, voyage-docs.moi.technology or cocolang.dev. Machine files and crawler checks: `moi-docs/geo` | Revert PR |
| `js-moi-sdk`, `main` | A merge deploys nothing by itself. A published release goes to npm and uploads the skill zip (`publish.yml`, on a release or by hand). The docs pipeline is unknown | Check npm before you quote a version | n/a |
| `MOI-Webinars`, `awesome-moi`, `moi-sprint` | Nothing deploys. A push to the public repo publishes it | The file on GitHub | n/a |
Only the Launchpad has a documented rollback; the others are the same idea, inferred. Voyage workflows belong to Upendhar and Srikar and the app to Vinay, Gokul and Prakhar. Anything on a VM is Upendhar's. Never ask DevOps for a secret value.

## 3. Before you ask for the merge
1. The review items are all answered and the preview was read (`previews.md`). Read the PR's state and checks, read-only: `gh pr view <N> --repo <org>/<repo> --json state,isDraft,baseRefName,mergeable,reviewDecision` and `gh pr checks <N> --repo <org>/<repo>`. A red check is not a merge. Reviewer approval is not recorded as a rule. ASK: Rahul who may merge each repo.
2. The PR base is right and, in a stack, the PR below it is merged (`stacked-and-batched.md`).
3. A database change is applied before the code that needs it: Points refuses to start on a stale schema, and Launchpad migrations are applied by hand in the Supabase SQL editor. A write to a production database is a GATE on its own (`templates/gate-asks.md`). A migration is run by the person with the project login: the Launchpad's `docs/HANDOFF.md` (on `master` of the private `sarvalabs/moi-agent-launchpad`) records that its production database is not reachable through a Supabase connector and must be run by hand in the SQL editor.
4. Merge order across PRs: `moidocs` #124 before `MOI-Website` #57, because the site links to a file that #124 creates (as of 2026-10-01).
5. Pick the method with the repo in mind. PR #53 on the Website was a squash merge; the Launchpad's merge commits read "from sarvalabs/<branch>". The command is `gh pr merge <N> --repo <org>/<repo> --squash` or `--merge` (the operator may press the button instead). Add `--delete-branch` only if the yes names it: it deletes the remote branch, a gate of its own. The method decides the revert command: a merge commit needs `git revert -m 1 <sha>` (a plain revert fails; tested on git 2.50.1), a squash commit takes a plain `git revert <sha>`. Which method each repo wants is not recorded. ASK: Rahul.
6. The ask names the PR number, the base, the method and what goes live. A merge needs its own yes: a yes to push is not a yes to merge. On 2026-08-18 PRs were merged when the previous operator had only asked to look, and on 2026-08-24 he wrote "you don't merge anything".

## 4. Right after the merge
1. Find the run, read-only: `gh run list --repo <org>/<repo> --limit 3`. Times seen: Launchpad about 4 minutes, Explorer 1.8 to 2.4 minutes, Points 4 to 5 minutes (inferred). The Website's and the Dataroom's are not recorded.
2. Wait for it to finish, then run the "Confirm live" read for that repo. Read the data in the answer, not only the status code.
3. A blog merge: `check-live.py` and the apex listing at `moi.technology/blog` (`moi-blog`). The second PR with social copy belongs to the announce step; do not merge it as part of this ship.
4. If a run is red, say so and stop. Re-running a workflow or running one by hand is a GATE, on the deploy branch only: the Website's `deploy.yml` hands the branch name it runs from to the VM script, and a manual Explorer run with environment PROD deploys the branch you give it (inferred from the workflow). Run them on the deploy branch.
5. If GitHub Actions does not start runs at all (an outage or billing block hit 2026-08-28 to 2026-08-30), the merged change is not live. Retry about every four hours, not every ten minutes, and say plainly that it is not deployed.
6. After a revert, check the live page again. On prod a revert once hid that the fix was not deployed (2026-08, DevOps: "it was not deployed with the latest blog fixes").

## 5. Rolling back
1. Say first which parts cannot be rolled back: database changes (no down migrations), and on-chain registrations with the card address written into them (permanent).
2. Launchpad: on a branch from `origin/master`, `git revert -m 1 <merge commit>`, push, PR, merge (each its own yes), then the live check. The manual route is a DevOps edit of the compose file and is overwritten by the next deploy.
3. Others: a revert PR on the deploy branch. The Points deploy removes the running container before the new one starts, so a bad image means downtime until the revert deploys.
4. A revert is a new change: it needs the same gates and the same live check.

## Not yet known
- Time from merge to live for the Website, Dataroom and the docs sites. ASK: Upendhar.
- Branch protection, required reviews and who may merge, per repo. ASK: Rahul.
- Which merge method each repo wants. ASK: Rahul.
- What the two VM deploy scripts do with the branch name. ASK: Upendhar.
- How `js-moi-sdk` docs build and deploy after a merge. ASK: Gokul.
