# Who to ask, and what these products need from DevOps

Updated 13 October 2026 from `project-handover-docs/` (`MOI-WEBSITE.md`, `DATAROOM.md`, `POINTS-PROGRAM.md`, `ENV-VARS.md`). Older rows are as of 2026-10-02 from `moi-devrel/references/people-and-teams.md`, `moi-devrel/references/keys-and-access.md` and the research notes. `ASK:` is defined in `moi-devrel/SKILL.md`. Writing the message uses `moi-devrel/templates/messages.md`; this file keeps only which requests these three products need. Back to `../SKILL.md`.

## Who owns each product
The handover documents record DevRel as the owner of the code and the content of all three products, and DevOps as the owner of each server. Rahul decides scope and approval.

| | Website and blog | Dataroom | Points Program |
|---|---|---|---|
| Wrote it | The previous operator wrote most of the commits; Srikar and Upendhar also committed | The previous operator wrote most; Srikar is the second contributor, knows the code and wrote the deploy workflow | Harsh Gupta wrote most of the app; Upendhar wrote the CI/CD; the previous operator ran the September audit and its fixes |
| Who decides content or scope | Rahul reviews public pieces and scope | Rahul | Rahul |
| Repo admins (can edit secrets) | Not recorded. ASK: Rahul | Not recorded. ASK: Rahul | gokul, chandra, git, adithya, upendhar (4 October) |
| Database owner | Supabase project: not recorded | Company Supabase organisation (moved 8 October). The plan should have backups; check | The Points email account, free plan, no backups |
| Security handover note | Open items of `MOI-WEBSITE.md` | Open items of `DATAROOM.md` | Open items of `POINTS-PROGRAM.md` |
| Who can act on its server | Srikar | DevOps. Srikar wrote the workflow; which of Srikar and Upendhar acts is not recorded. ASK: Rahul | Upendhar |

## Who can act on a server
- **Srikar** (also spelled Sreekar) owns the website server: nginx, the Express server under PM2, TLS and the deploy script, which lives on the server and not in the repo. He wrote the Dataroom's workflow. On 2026-08-18 he reported fixing the blog deploy cache. Go to him for anything on the website server: a deploy, a restart, a log, nginx.
- **Upendhar** owns the Points box: nginx, TLS, Teleport, the `GHCR_PAT` token, the container `moi-project` on host port 31000 and the CI/CD he wrote. He is also an org admin (with Rahul). On 13 October the first Points deploy failed on an expired `GHCR_PAT`; he replaced it.
- The Dataroom reaches its server by SSH key and the other two through Teleport (`SKILL.md`). Either way it is DevOps: ASK: Rahul which person if neither answers.
- Nobody else is recorded. A repo admin can set Actions secrets and run a workflow, but cannot read a secret back.

## The requests these products need
Use `templates/devops-request.md` for each. One task per message. Never ask for a secret value: secrets live in GitHub. The first column says which DevOps owner to write to.

| ID | Product (to) | Ask them to | When |
|---|---|---|---|
| R1 | Website (Srikar) | Put a copy of the website deploy script in the repo, or send a readable copy | Before relying on any claim about what a deploy does |
| R2 | Dataroom (DevOps) | The same for the Dataroom deploy script (`/root/scripts/deploy-moi-dataroom.sh`, on the server only) | Same |
| R3 | Website (Srikar) | Send the server log lines that begin `Fetch calls error:` (and `RPC error:` or `Chat error:`) for a time window | `website-database.md` step 2 |
| R4 | Website (Srikar) | Make nginx answer 404 for unknown addresses, send a discovery `Link` header on `/` (the value is the `Link` line of `public/_headers` on `main`, where PR #57 put it on 5 October 2026; the checks are in `moi-docs/geo/references/after-merge.md`), and add `Content-Disposition: attachment` for `/papers/*.pdf` | W-K3, W-K4, W-K5 |
| R5 | Website (Srikar) | Say what nginx forwards for `/api` on moi.technology and for dev.moi.technology, and confirm the value to use for `VITE_CHATBOT_API` | `website-settings.md`, before the secret changes |
| R6 | Website (Srikar) | Set `ALLOWED_ORIGINS` or `PORT` in the VM environment, or say whether the deploy script forwards a newly added name | `website-settings.md` |
| R7 | Dataroom (DevOps) | Set a chat-limit variable on the VM, or confirm a workflow `env:` change reaches the app | `dataroom-settings-and-database.md` |
| R8 | Points (Upendhar) | Apply a new migration to production before the pull request that carries it is merged, with the repo's `node scripts/migrate.mjs`, and send back the lines it prints | `points-settings-and-database.md` step 4 |
| R9 | Points (Upendhar) | Say what schedules `/api/jobs/maintenance` (nothing does today), whether older images exist for a rollback, and which pnpm version the image uses | `points-ship.md`, `points-health.md` |
| R10 | Any (the product's DevOps owner) | Send a log excerpt for a time window when the app is up and a page errors. On 2026-09-15 DevOps found a missing table from the container log | The health runbooks |
| R11 | Points (Upendhar) | Allow a tester's address through the box's firewall, if it has one (done on 2026-09-15 for testing) | Seen once (2026-09-15). Give the address in the message, not in this library |
| R12 | Points (Upendhar) | Do the setup that draft PR #24 (CI/CD hardening, it replaced the closed #15) needs: an `environment: production` with its secrets, a non-root VM user in the docker group, nginx on loopback | Before #24 can merge |

## How to write to DevOps (rules from past corrections)
- Short, human and specific: the problem, the solution, the exact action for them, how to check it worked. One task per message. Say what the request is about ("this is about delete"). No labels such as "Owner:", no em dashes. These were corrections on 2026-08-10, 2026-08-18 and 2026-09-10 (`moi-devrel/references/people-and-teams.md`).
- Do not reopen settled items. Read the Open items of the product's handover document first: what is settled is there.
- Claude drafts, the operator sends. The channel is not fixed: the previous operator used Discord and direct messages. Ask the person which they read. Response time is not recorded.
- A draft status line that claimed work not done was removed on 2026-09-10. List what was done, label what is to do.

## Everyone else

| Need | Ask |
|---|---|
| Whether DevRel owns a product, scope, approval | Rahul |
| History of any decision | `project-handover-docs/` first, then Rahul |
| Community call dates, the Luma address, the Luma, Google Meet and YouTube accounts | Vardan, confirmed by Rahul |
| Points app internals | Harsh Gupta (channel unknown) |
| Dataroom code, the website server and its chat | Srikar |
| Chain facts a Points challenge reads, the RPC address | Gokul |
| Create or change an Actions secret or variable | A repo admin of that repo, after the operator's yes |
| Google OAuth, the X app, the Discord app, the Telegram bots for Points and the blog, Reown, Resend, Google Analytics, Tag Manager, Search Console | The `sarvalabsdeveloper@gmail.com` login (`ENV-VARS.md`). ASK: Rahul for access |
| Supabase for the Dataroom and the Launchpad | The company Supabase organisation (moved 8 October). ASK: Rahul |
| Supabase for the website | Not recorded; probably the Dataroom's project. ASK: Rahul |
| Anthropic, OpenAI and Groq keys | No company account exists (October 2026). Create company accounts and keys first. ASK: Rahul |
| Buffer | Chandra |
| Cloudflare | Company-owned |

## Not yet known
- The channel DevOps reads and how fast it answers. ASK the person you write to.
- Who is paged when one of these products is down. ASK: Rahul.
- Repo admins of `MOI-Website` and `moi-dataroom0`. ASK: Rahul.
- Which DevOps person acts on the Dataroom server. ASK: Rahul.
