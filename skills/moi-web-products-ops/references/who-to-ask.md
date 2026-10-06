# Who to ask, and what these products need from DevOps

Facts are as of 2026-10-02 from `moi-devrel/references/people-and-teams.md`, `moi-devrel/references/keys-and-access.md` and the research notes. `ASK:` is defined in `moi-devrel/SKILL.md`. Writing the message uses `moi-devrel/templates/messages.md`; this file keeps only which requests these three products need. Back to `../GUIDE.md`.

## Who owns each product: what is not known
Which of these products DevRel owns is not settled. ASK: Rahul. The previous operator built or ran them; nothing recorded says the new hire inherits them.

| | Website and blog | Dataroom | Points Program |
|---|---|---|---|
| Wrote it | The previous operator wrote most of the commits; Srikar and Upendhar also committed (`git log` on `main`, read 2026-10-03) | The previous operator wrote most; Srikar is the second contributor, knows the code and wrote the deploy workflow | Harsh Gupta wrote most of the app; Upendhar wrote the CI/CD; the previous operator ran the September audit and its fixes |
| Who decides content or scope | Rahul reviews public pieces and scope | Not recorded. ASK: Rahul | Not recorded. ASK: Rahul |
| Repo admins (can edit secrets) | Not recorded. ASK: Rahul | Not recorded. ASK: Rahul | gokul, chandra, git, adithya, upendhar (2026-09-15) |
| Database owner | Supabase project: unknown | Supabase project: unknown | Supabase project on the previous operator's personal login, free plan |
| Security handover note | Adithya | Adithya | Adithya |
| Who can act on its VM | Upendhar | Upendhar | Upendhar |

## Who can act on a VM
- **Upendhar** (DevOps) holds Teleport, the VMs, nginx, TLS certificates, DNS for `*.moi.technology`, `GHCR_PAT` and the deploy scripts. He wrote the Points CI/CD. Go to him for anything on a VM: a deploy, a restart, a log, nginx, DNS, a firewall, running a migration in a container.
- **Srikar** (also spelled Sreekar) wrote earlier workflows, including the Dataroom's, and was described on 2026-08-10 as the person in charge of the VM. On 2026-08-18 he reported fixing the blog deploy cache. Whether he still owns a VM is not recorded. ASK: Rahul, then Upendhar.
- Nobody else is recorded. A repo admin can set Actions secrets and run a workflow, but cannot read a secret back.
- The Dataroom reaches its VM by SSH key, the other two through Teleport (`SKILL.md`). Both need Upendhar either way.

## The requests these products need
Use `templates/devops-request.md` for each. One task per message. Never ask for a secret value: secrets live in GitHub.

| ID | Product | Ask Upendhar to | When |
|---|---|---|---|
| R1 | Website | Put a copy of the website deploy script in the repo, or send a readable copy | Before relying on any claim about what a deploy does |
| R2 | Dataroom | The same for the Dataroom deploy script | Same |
| R3 | Website | Send the server log lines that begin `Fetch calls error:` (and `RPC error:` or `Chat error:`) for a time window | `website-database.md` step 2 |
| R4 | Website | Make nginx answer 404 for unknown addresses, send a discovery `Link` header on `/` (the value is the `Link` line of `public/_headers` on the branch of open PR #57 in `sarvalabs/MOI-Website`, read 2026-10-03, and in `main` once it merges; the checks are in `moi-docs/geo/references/after-merge.md`), and add `Content-Disposition: attachment` for `/papers/*.pdf` | W-K3, W-K4, W-K5 |
| R5 | Website | Say what nginx forwards for `/api` on moi.technology and for dev.moi.technology, and confirm the value to use for `VITE_CHATBOT_API` | `website-settings.md`, before the secret changes |
| R6 | Website | Set `ALLOWED_ORIGINS` or `PORT` in the VM environment, or say whether the deploy script forwards a newly added name | `website-settings.md` |
| R7 | Dataroom | Set a chat-limit variable on the VM, or confirm a workflow `env:` change reaches the app | `dataroom-settings-and-database.md` |
| R8 | Points | Apply a new migration to production before the pull request that carries it is merged, with the repo's `node scripts/migrate.mjs`, and send back the lines it prints | `points-settings-and-database.md` step 4 |
| R9 | Points | Say whether a schedule calls the nightly housekeeping job, whether older images exist for a rollback, and which pnpm version the image uses | `points-ship.md`, `points-health.md` |
| R10 | Any | Send a log excerpt for a time window when the app is up and a page errors. On 2026-09-15 DevOps found a missing table from the container log | The health runbooks |
| R11 | Points | Allow a tester's address through the box's firewall, if it has one (done on 2026-09-15 for testing) | Seen once (2026-09-15). Give the address in the message, not in this library |
| R12 | Points | Do the setup draft PR #15 needs: an `environment: production` with its secrets, a non-root VM user in the docker group, nginx on loopback | Before #15 can merge |

## How to write to DevOps (rules from past corrections)
- Short, human and specific: the problem, the solution, the exact action for them, how to check it worked. One task per message. Say what the request is about ("this is about delete"). No labels such as "Owner:", no em dashes. These were corrections on 2026-08-10, 2026-08-18 and 2026-09-10 (`moi-devrel/references/people-and-teams.md`).
- Do not reopen settled items. ASK: Adithya what was settled before you write.
- Claude drafts, the operator sends. The channel is not fixed: the previous operator used Discord and direct messages. ASK: Upendhar which he reads. Response time is not recorded.
- A draft status line that claimed work not done was removed on 2026-09-10. List what was done, label what is to do.

## Everyone else

| Need | Ask |
|---|---|
| Whether DevRel owns a product, scope, approval, who owns a vendor account | Rahul |
| History of any decision, the security handover note, the personal Points database login, local-only files | Adithya |
| Community call and AMA dates | Vardan, confirmed by Rahul |
| Points app internals | Harsh Gupta (channel unknown) |
| Dataroom code, the website chat server | Srikar |
| Chain facts a Points challenge reads, the RPC address | Gokul |
| Create or change an Actions secret or variable | A repo admin of that repo, after the operator's yes |
| Owners of Supabase, Anthropic, OpenAI, Google Analytics, Tag Manager, Search Console, Google OAuth, X, Discord, Telegram, Reown, Resend, Cloudflare, Zoom | Unknown for all. ASK: Rahul |

## Not yet known
- The channel DevOps reads and how fast it answers. ASK: Upendhar.
- Who is paged when one of these products is down. ASK: Rahul.
- Repo admins of `MOI-Website` and `moi-dataroom0`. ASK: Rahul.
