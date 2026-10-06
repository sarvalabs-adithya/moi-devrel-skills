# Rollback

Facts are as of 2026-10-03, from `docker-build.yml`, `deploy.yml`, `docker-compose.yml`, `docs/POST-CUTOVER-CHECKLIST.md` section 6 and `docs/HANDOFF.md`. The pipeline has no rollback of its own: a rollback is a new deploy of older code. Every image is tagged `:latest` and `:<short commit id>`. `:latest` is mutable. Back to `../SKILL.md`.

## Decide first
Stop taking new users and roll back when any of these appears (the checklist's own stop-and-rollback triggers; what "stop taking new users" can mean, with no switch in the app, is in step 5 of `../SKILL.md`):
- A newly registered agent's on-chain `card_uri` is not the production host. It is permanent for that agent, so every further registration adds one.
- Installed agents' polls return 502 or 504.
- The container restarts in a loop.
- `getWebhookInfo` shows a `last_error_date` that keeps advancing.
Also roll back when the health script was green before a deploy and FAIL after it, and the failing line is something that deploy touched (a judgement call, not a recorded rule).

A red deploy run needs no rollback: production still serves the old image. Fix forward through `ship-a-change.md`.

## What a rollback cannot undo
- On-chain effects: registrations, `card_uri` values, listings, activation grants.
- Migrations. There is no down migration (`database.md`).
- A secret or variable already changed, a Telegram webhook already re-set, and `NEXT_PUBLIC_*` values (only a rebuild changes them).
- Runtime bundles already downloaded by users.
Say which of these apply in the incident note.

## Run: Route A, revert on master (preferred; about 5 to 10 minutes)
| # | Step | Command or action | Done when | Gate |
|---|---|---|---|---|
| 1 | Find the change | `gh run list -R sarvalabs/moi-agent-launchpad -L 10 --json databaseId,displayTitle,headSha,conclusion,createdAt` and `git log --merges --oneline -10 origin/master` | You hold the merge commit of the bad change and know the last good state | read-only |
| 2 | Branch | `git fetch origin` (writes only to your working copy), then `git checkout -b revert-<topic> origin/master` | On a new branch | local |
| 3 | Revert | `git revert -m 1 <merge commit>`. The history shows merge commits ("Merge pull request #N"); for a squashed PR use `git revert <commit>` without `-m` | A revert commit exists | local |
| 4 | Check | `npm ci && npm run typecheck && npm test`. In a live outage you may leave `npm run build` to the Docker build and say so | Pass | local |
| 5 | Push | `git push -u origin revert-<topic>` | It is on the remote the operator named | GATE |
| 6 | Pull request | `gh pr create -R sarvalabs/moi-agent-launchpad --base master --head revert-<topic>`; the title says Revert and why, the body lists what the revert does not undo | PR open | GATE |
| 7 | Merge | Say first: "this merge deploys to production". Merge on the GitHub page or with `gh pr merge <number> -R sarvalabs/moi-agent-launchpad --merge`. Whether an emergency revert needs the normal approval is not on record. ASK: Rahul | Merged | GATE |
| 8 | Watch | `gh run list -R sarvalabs/moi-agent-launchpad -L 3 --json databaseId,displayTitle,status` for the id of the run the merge started, then `gh run watch <id> -R sarvalabs/moi-agent-launchpad --exit-status` | Green, about 4 minutes | read-only |
| 9 | Verify | Health script, then the check that showed the problem | The symptom is gone | read-only |
| 10 | Record | `../templates/incident-note.md` | The note exists and names the follow-up | local |

## Run: Route B, DevOps pins the previous image (fast and temporary)
Use it only when Route A will take too long, and freeze merges while it is in place.
| # | Step | Command or action | Done when | Gate |
|---|---|---|---|---|
| 1 | Pick the tag | The short commit id of the last good build, from `gh run list` | You hold a tag | read-only |
| 2 | Ask | Draft from `moi-devrel/templates/messages.md`, one task: run the web container from the image `ghcr.io/sarvalabs/moi-agent-launchpad:<tag>` on the VM and send back the container status (ASK: Upendhar how the image is set there). ASK: Upendhar whether the old tag still exists in GHCR (retention is not on record) | The message is sent by the operator | GATE |
| 3 | Verify | Health script | Healthy | read-only |
| 4 | Land Route A | The next deploy copies the repo's `docker-compose.yml` back over it (back to `:latest`) and prunes local images, so the pin lasts only until the next merge. Do Route A before anyone merges | `master` and production agree again | GATE |

## Run: Route C, run the workflow from an older ref (inferred; not on record as used)
`ci-cd.yml` has a manual trigger that builds the ref you pick and deploys it as `:latest`. If the last good commit is a tag or a branch on the remote, `gh workflow run ci-cd.yml -R sarvalabs/moi-agent-launchpad --ref <ref>` redeploys it without a revert. Creating that ref is a push, which is a GATE; the manual run is a second GATE. Afterwards `master` still holds the bad change, so Route A must follow before anyone merges.

## After any rollback
- Read the incident note back to the operator: cause if known, what was not undone, what users saw.
- If users were affected, the operator decides whether to tell them in Discord. Claude drafts, the operator sends.
- A tested fix goes through `ship-a-change.md`; it needs its own measured evidence.

## Not yet known
- Whether GHCR keeps old tags, and whether DevOps keeps VM snapshots. ASK: Upendhar.
- Who approves an emergency revert. ASK: Rahul.
- Whether any rollback has ever been done: none is on record.
