# Order of work, and who does each step

Facts are as of 2026-10-03 (owners, Supabase and the Explorer PR corrected on 2026-10-13). Step numbers are the rows of the run table in `../SKILL.md`. `ASK:` is defined in `moi-devrel/SKILL.md`. Back to `../SKILL.md`.

## The order and why
Two things set the pace. The protocol team must supply the new registry id (the blocking dependency: four days in September), and a wallet that exists on the new chain must fund the Launchpad's wallets (a wiped account cannot recreate itself). Everything else follows from those two.
| Step | Needs | Why it sits here | Who does it |
|---|---|---|---|
| 1 Detect and confirm | nothing | Cheap and read-only. It decides whether anything below applies | Operator and Claude |
| 2 Open the log, record old ids | 1 | `id-grep.sh` (`bash "$SKILLS/moi-devnet-reset/scripts/id-grep.sh" ...`, step 2 of `../SKILL.md`) finds every place that must change, so run it before editing anything | Claude |
| 3 Freeze | 1 | Nothing may spend funds or announce "live" against a state that may be replaced. In August the registry failed on 2026-08-06, was replaced on 08-10 and 08-13, and the chain was wiped on 08-15 | Operator decides, Claude lists |
| 4 Facts from the protocol team | 1 | The new registry id, the package versions and what else moved exist nowhere else. Nobody can finish without them | Protocol team (Gokul). The operator sends message 1 |
| 5 Verify the new registry | 4 | Pointing a product at a registry that lacks a routine, or is replaced again, costs a deploy and a user-visible outage. The Launchpad did this check before switching on 2026-09-15 | Claude, read-only |
| 6 Constants and SDK | the constants known (can start before the registry id: the SDK upgrade was done within a day of the wipe, on 2026-09-12) | All three repos must build with the same SDK pair, because `js-moi-agent-registry` pins its SDK peer exactly | Operator and Claude, locally |
| 7 Wallets and funds | 4, 6 | New users cannot onboard until the Launchpad's registration wallets exist. A human with a wallet on the new chain funds a sponsor, and the faucet funds only accounts that exist | Sponsor: the operator or another person with a MOI Wallet. The three registration mnemonics: DevOps. Claude never handles a phrase |
| 8 Launchpad | 5, 7 | Users are blocked here first ("nobody has been able to onboard for three days", 2026-09-14). It also holds the read-caller logic the other two can borrow, and the other two depend on its host: the MCP's Launchpad tools need `MOI_LAUNCHPAD_URL` equal to its `NEXT_PUBLIC_APP_URL`, and the Explorer verifies agents by their Launchpad card host | Operator (repo admin), DevOps for the VM |
| 9 MCP | 5, 6 | Start its pull request early: the production copy lives in `sarvalabs/voyage-api` and needs another team's review (PR #313 had no review from 2026-09-23 to at least 2026-10-13). Deploy after the Launchpad | Operator, Voyage team, DevOps |
| 10 Explorer | 5, 6 | Last, because its sync writes the production database and should read the final registry | Operator, Gokul (app), Upendhar (CI/CD, database) |
| 11 Drift check | 8 to 10 | The three repos pin the id separately and moved 4, 11 and 12 days after the September wipe | Claude |
| 12 Content and demos | 11 | Ids are final, products work, and a demo needs the wallets of step 7 | Operator and Claude |
| 13 Tell people | drafts from step 1 | "Fixed" is said only after step 14. The first message goes out at step 1 | Operator sends, Claude drafts |
| 14 Verify and log | all | A health check is not enough. A fresh-wallet pass is the proof | Operator and Claude |
The order of steps 8 to 10 is a judgement from these dependencies. The September order was Launchpad (4 days), Explorer (11), MCP (12), and no rule was recorded. ASK: Gokul if a different order is wanted.
Do in parallel while waiting for step 4: steps 2, 3 and 6, the draft messages, and reading the new SDK release.

## Freeze: what would write to a dead chain
No product is recorded as writing to the chain on its own: the writes are what users trigger (inferred from the code and workflows read). No maintenance switch is recorded for any product (ASK: Rahul for the Launchpad and the MCP, Upendhar for anything at the web server). So the freeze is mostly a list of things people must not do.
| Do not | Why | How |
|---|---|---|
| Run a demo, `npm run setup:*`, `npm run demo`, a webinar rehearsal, an x402 live round trip or a test round | It spends funds on a state that may be replaced, and the result means nothing | Tell the operator. GATE to spend funds once step 5 is done |
| Fund a sponsor or test wallet from the faucet, or recreate registration wallets | A replacement within days kills them (August) | Wait for step 4 to say the state is final |
| Point a product at a registry that step 5 has not checked | Cost of a wrong deploy | Step 5 first |
| Delete or edit Launchpad agent rows, or empty the Explorer `agents` table, to "fix" the lists | Owners re-register by themselves. The Launchpad's stranded check compares chain and database, so it clears itself | Leave rows alone |
| Leave scheduled or published text that says "live" or quotes an id or a hash | It goes false at the reset | List Buffer posts, the monthly newsletter (it goes out on the 15th: `project-handover-docs/BLOG.md`), Luma pages, call decks. The operator edits or deletes by hand in each service. Claude cannot, and `buffer.mjs` cannot delete |
| Tell users it is fixed | It is not until step 14 | Message 4 says what is wrong, not when it will be fixed |
What continues and cannot be stopped from here: Launchpad activations fail with 503 `faucet_unavailable`, and the admin Telegram chat is alerted at most once an hour per process; phone approvals of MCP writes fail; the Explorer keeps indexing from its node address.

## Who can act, per product
Which products DevRel owns now is not settled. ASK: Rahul. Until he answers, do the read-only steps yourself and hand the facts, the drafts and the exact change to the owner. Do not change a product you do not own.
What to do once Rahul has answered, per product (this decides steps 8 to 10 of `../SKILL.md`):
| Answer | What you do |
|---|---|
| DevRel owns it | The operator opens the pull request through `moi-devrel/ship`; each push, PR and merge is its own GATE. The VM, DNS and database steps still go to DevOps |
| Another team owns it | Claude drafts the exact change and a message (`../templates/messages.md`, or `moi-devrel/templates/messages.md` for a shape the reset drafts lack); the operator sends it to the people the table below names for that product. No pull request from you |
| No answer yet | The same as "another team". Steps 8 to 10 wait, and 11 and 14 wait with them; steps 1 to 7 go on |
| Product | Code and settings | VM, deploy, database | Not known |
|---|---|---|---|
| Agent Launchpad (`sarvalabs/moi-agent-launchpad`, `master`) | The previous operator wrote 301 of 338 commits and holds the Telegram bot and the model API key (`project-handover-docs/LIST-OF-DEPENDENCIES.md`, the 4 October snapshot, and `project-handover-docs/AGENT-LAUNCHPAD.md`). Gokul publishes the registry id | DevOps (Upendhar): VM, DNS, Teleport, GHCR. DevOps holds the three registration mnemonics. The database is a Supabase project in the company organisation since 2026-10-08 | Whether DevRel owns it. Who holds the mnemonics outside GitHub (ASK: Upendhar). Who may merge (ASK: Rahul). Whether a maintenance switch exists: none is recorded (ASK: Rahul) |
| MCP server (`sarvalabs/moi-mcp`, production copy in `sarvalabs/voyage-api` branch `feat/moi-mcp`) | The previous operator wrote nearly all commits. The Voyage team owns `voyage-api` (Srikar opened PR #308) | The Voyage VMs (`voyagedev`, `prod-voyage`) through Teleport (Srikar runs them and the deploy workflow; Upendhar is the other DevOps contact) | Which people besides Srikar may trigger the production deploy (ASK: Srikar). The MCP secrets in `voyage-api` are repo-level, not environment-level. Whether DevRel owns it (ASK: Rahul) |
| Agent Explorer (`sarvalabs/agent-explorer`, `main`) | Gokul owns the app and the registry logic. The previous operator wrote 10 of 62 commits (`project-handover-docs/LIST-OF-DEPENDENCIES.md`, as above) | Upendhar: CI/CD, SSH deploy, the MySQL database | Whether `MOI_MNEMONIC` is set in production. The WalletConnect project owner. Whether DevRel owns it (ASK: Rahul) |

MCP server: `project-handover-docs/MCP-SERVER.md` records no security finding. The 2026-10-02 research note said one was open; its content is not recorded (the previous DevRel's notes); ASK: Rahul before touching sign-in or other admin code.

Agent Explorer: a security finding is open, recorded in `project-handover-docs/LIST-OF-DEPENDENCIES.md` (Agent Explorer, ToDo 1). Read it and ask Gokul before touching the server's admin.

Who can act on a VM: DevOps. Srikar runs the website server, the Voyage VMs and the MCP deploys; Upendhar runs the Points box, CI/CD and GHCR, and the Launchpad and Explorer deploys (Teleport, nginx, TLS, DNS). Do not ask either of them for a secret value; secrets live in GitHub (`moi-devrel/references/people-and-teams.md`).

## What only a human can do
| Task | Why |
|---|---|
| Register a wallet in the MOI Wallet app on the new chain and fund it from the faucet | The faucet funds only accounts that exist. Claude never handles a recovery phrase, including a throwaway one |
| Give `MOI_SPONSOR_MNEMONIC` and `MOI_DEPLOYER_MNEMONIC` through a no-echo prompt (`moi-devrel/references/consent-and-identity.md` section 4, rule 6), not on the command line | These are never stored, and never given to Claude. A command line lands in shell history |
| Approve an MCP write on the phone | Phone approvals cannot be automated |
| Set a repository variable or secret, run a deploy workflow | A GATE, and only a repo admin can edit Actions secrets |
| Edit a copy in a shared service (Buffer, Luma, Drive, a YouTube description) | The operator's own action |

## Not yet known
- Whether DevRel owns any of the three products. ASK: Rahul.
- Who holds the registration mnemonics, and the approved way to hand them to whoever runs the script. ASK: Upendhar, then Rahul.
- Which people besides Srikar may trigger the production MCP deploy. ASK: Srikar.
- Whether another order of steps 8 to 10 is wanted. ASK: Gokul.
