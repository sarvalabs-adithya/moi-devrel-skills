# Telling people

Facts are as of 2026-10-03. Claude drafts and the operator sends. Claude never messages anyone, and never comments on a pull request or issue that notifies a teammate. Every send is a GATE. The drafts are in `../templates/messages.md`, numbered as below. Wording rules and tone are `moi-devrel/references/house-style.md`; the shapes for other teammate messages (a review request, a single question, a status update) are in `moi-devrel/templates/messages.md`, and `moi-devrel/scripts/check-message.py` checks any draft. `ASK:` is defined in `moi-devrel/SKILL.md`. Back to `../SKILL.md`.

## Who needs to hear what
| Who | Why they need it | What they need to hear | When | Draft | Channel |
|---|---|---|---|---|---|
| The protocol team (Gokul) | They hold the facts nobody else has, and they redeploy the registry | What we read, then six questions: the new registry id, whether agents were re-imported and from which snapshot, the new `js-moi-sdk` and `js-moi-agent-registry` versions, whether KMOI's id, the fuel floor, the participant-creation minimum or the RPC path moved, whether the faucet wallets are alive, and whether this state is final | At step 1, as soon as the reads show a signal | 1 | Not known. ASK: Rahul |
| The protocol team, after | They should know the products moved and where | The new id now pinned in each product, what was checked, what is not done | At step 14 | 2 | Same |
| DevOps (Upendhar: CI/CD, GHCR, the Points box and the Launchpad and Explorer deploys; Srikar: the website server, the Voyage VMs and the MCP deploys) | They hold the VMs, the Teleport access, the registration mnemonics and the production database | One task per message: the problem, the solution, the exact action for them, how to verify. Registration wallets (3a). A deploy or a container task (3b). The Explorer sync (3c) | Only when a step needs them | 3a, 3b, 3c | Discord and direct messages have been used. Not fixed. ASK: Upendhar |
| The Voyage team (reviewers of `sarvalabs/voyage-api`) | Production MCP is a copy in their repo and a pull request there needs their review | The pull request, what it changes, that nothing deploys until the workflow is run, and who will run it | At MCP step M6 | 6 | GitHub. Names: ASK: Rahul |
| Rahul | Decides scope, reviews every public piece, and answers who owns what | Status that lists only work done, with to-dos labelled as to-dos; the decisions waiting on him; the ownership questions this skill leaves open | At step 1 in two lines, then at step 14 | 5 | Discord; the handle is in `moi-devrel/references/people-and-teams.md` |
| Launchpad users and self-hosted agent owners | They cannot activate a wallet or register, and agents made before the reset show "need registering again" | What happened, what to do (re-register from the dashboard; re-download the setup script), and that nothing is wrong with their wallet. No promise of a time | A first notice at the operator's call (rule 8); the "fixed" notice only after step 14 | 4a, 4b | The Discord server behind the dashboard's "reach out on Discord" link, and the dashboard banner (a code change: `launchpad.md` row L9). Which channel: ASK: Rahul, Sai Kiran |
| MCP users | Their wallets must exist on the new chain and the server must read the new registry | Nothing until MCP step M9 has passed. What a user must redo is not known (`mcp.md`). ASK: Gokul | After M9 | 4b, adapted | Same |
| Explorer visitors | None | Nothing is said to them. The list catches up after the sync; rows of the old registry may remain until Gokul decides (`explorer.md` E7) | n/a | n/a | n/a |
| Owners of content that quotes an id, a hash or "live" (Sai Kiran for the social calendar, Vardan for call dates, the next call's host, the next session's presenter, and whoever made a Luma page: not recorded, ASK: Rahul) | Their copies are not on disk. Only they can edit them | The exact sentence to change and what replaces it, or that a demo must be rehearsed again | At step 12 | 7 | Slack for marketing inputs, per `moi-devrel/references/people-and-teams.md` |

## Rules
1. Say what is wrong and whose side it is on. For wallet failures the product already says nothing is wrong with the user's wallet; keep that.
2. Never give an ETA. Past recovery took 4 days for the Launchpad and 11 to 12 for the others (`history.md`), and the first step is outside DevRel.
3. Do not name a cause (an upgrade, a wipe) until the protocol team has confirmed it.
4. Say "devnet" and name Voyage only as the explorer. Say "network ID". Use participant-centric wording (`moi-devrel/references/terminology.md`). Public text has no em dashes, no emoji and no vague attribution.
5. Write dates as a date, 24-hour UTC and India time: `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "<YYYY-MM-DD HH:MM>" UTC`. Never "EST", never "today".
6. Do not ask DevOps for a secret value. Secrets live in GitHub. Do not reopen items already settled with them; the settled items are in the handover docs (`project-handover-docs/`), and if unsure, ASK: Rahul.
7. Do not say "live" or "fixed" before step 14 and the live reads of that day.
8. One audience per message. Rahul reviews public pieces, so ASK: Rahul whether a notice to users needs his review before it goes.
9. Run `python3 "$SKILLS/moi-devrel/scripts/check-message.py" --to <kind> <draft>`, `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" <draft>` and `bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" <draft>` on every filled draft before the operator reads it. The kind of each draft is in `../templates/messages.md`.

## Not yet known
- The channel where the protocol team announces and where it wants questions. ASK: Rahul.
- The Discord channel names for users, who posts there, and who may. ASK: Rahul, Sai Kiran.
- Whether any support channel is monitored, and by whom. ASK: Rahul.
- Whether an announcement template for reset notices ever existed. None is recorded.
