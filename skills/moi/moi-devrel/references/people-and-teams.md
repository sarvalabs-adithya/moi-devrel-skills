# People and teams

Facts are as of 2026-10-02. Roles are only what the evidence shows. "ASK:" has one meaning, defined in `../SKILL.md` ("Before you start"): the evidence does not settle it, so put the question to the named person through the operator and do not guess meanwhile. Work handles appear only where the research gives them. Back to `../SKILL.md`.

## People you will deal with
| Name | Role as evidenced | Go to them for | Channel |
|---|---|---|---|
| Rahul (Lenkala) | Sets direction and reviews decks, blog posts and docs scope. Internal gate for anything filed upstream (agreed 2026-09-09). Decides the MCP npm package name. Title not stated. ASK: confirm title and what he formally approves | Review of any public piece, narrative and scope calls, the written format for release announcements, who owns an account | Discord `@rahullenkala`. Calls on Meet. GitHub handles `moi-rahul` and `sarvalabs-rahul` appear in CODEOWNERS (same person, inferred; ASK: Rahul which he uses) |
| Gokul | Protocol and Voyage side (inferred). Publishes the registry logic id after a reset, owns the Agent Explorer app and registry, owns Voyage docs content, sits on the SDK team, reviews code (the x402 package "goes through Gokul's review"). ASK: title | Chain and protocol questions, the network ID RPC, reset facts, review of SDK, Voyage and docs PRs | Channel unknown. ASK |
| Upendhar | DevOps (`project-handover-docs/LIST-OF-DEPENDENCIES.md`, 4 October snapshot, and the product docs). Holds Teleport, the Points box and CI/CD, GHCR (`GHCR_PAT`), nginx, TLS, DNS. Wrote the Points and Explorer CI/CD | Anything on a VM: deploys, nginx, DNS, running a migration in a container, a firewall allow-list, Teleport tokens | Discord and direct messages were used. The channel is not fixed. ASK |
| Srikar (also spelled Sreekar) | DevOps: owns the website server (`MOI-WEBSITE.md`), the Voyage VMs and the MCP deploys (`MCP-SERVER.md`) as of 13 October 2026. Wrote the Dataroom deploy workflow and website issue #3, fixed the blog deploy cache. `LIST-OF-DEPENDENCIES.md` lists him as author of earlier workflows. The company Pinata account holds the Moinkee files since 14 October 2026 (`ENV-VARS.md`) | The website server, the blog host and deploy history, papers nginx fix, Dataroom and the website chatbot server, Voyage VMs, MCP deploys | ASK: Rahul |
| Vinay (M S) | Posts engineering release logs in Discord. On the SDK and Voyage teams | Release logs and versions, review of js-moi-sdk and Voyage PRs | Discord |
| Prakhar | Voyage team | Voyage app questions | ASK |
| Harsh Gupta | Wrote most of the Points app | Points internals | ASK |
| Harsh Rastogi | SDK team. ASK: whether he is the Harsh who owns Galxe in the programme sheet | SDK questions | ASK |
| Abhinav Agarwalla | Author of moidocs PR #120 (access policy, storage cost, submit-interaction docs) and PR #116 (`context_hash` rename) | The meaning of what he documented; his PRs get fact-checked against source | ASK |
| Robert Špendl | Maintains Coco and its docs. Approved coco-docs #12 on 2026-09-29 | Coco compiler and cocolang.dev | GitHub review |
| Chetna, Manish, Shameer | Wrote moidocs content | History of a docs page | ASK |
| Sai Kiran | Marketing and community. Wrote the "Scribble report" and community pointers for community calls, runs campus logistics for Forge Basic, owns the MOI Socials sheet, prepares the Wikidata entry, shares Gemini notes of standups | Community numbers and growth, social calendar, campus logistics, entity pages, Mailchimp sender identity | Slack, where call inputs arrive |
| Vardan (Aggarwal) | Owns the Community Call and AMA calendar sheet, the podcast and, with Louis, KOL outreach | Call and AMA dates, guests, podcast | Slack |
| Piyush | Marketing; presents the marketing roadmap slide (CC14 first draft) | Marketing segment content | ASK |
| Sujatha | Owns the MOI Annual Calendar (Drive) | The annual calendar | ASK |
| Prateek, Rishal | Prateek gave the product update (Proofly) at CC13 and was dropped from CC14. Rishal's research segment was deferred | Their segments, if they return | ASK |
| Ram | Reviewer who rejected the first session 8 design. Role not stated. ASK | Direction on webinar topics | ASK |
| The call host | Opens, closes and moderates the community call, may ask a planted question. Drive scripts name "Ruta" (also "Rutha"); the research note says the name is unknown. ASK | The host's question list and clip plan | Slack |
| Adithya Ganesh | Previous DevRel operator, Sarva Labs, until 14 October 2026. Git identity `sarvalabs-adithya`. Wrote the handover docs (`project-handover-docs/` in the handover repo). Ran almost all of the work in this library | After 14 October 2026 nothing: use the handover docs, and where they are silent ASK: Rahul. The accounts still under him are listed in `MIGRATION-LIST.md` (the Launchpad Telegram bot, whose transfer to Rahul Lenkala Telegram refused on 14 October; he retries once Telegram allows). Questions on the docs standard went to him in `#dev-chat` | `#dev-chat` (unverified). Only the Forge README places `#dev-chat` on Discord; the docs standard does not name the platform. ASK: Rahul |
| The video editor | External, works from a personal account. "Krishna" is named in a standup (match inferred). ASK: contact and brief format | Edits of Builders recordings and launch videos | ASK |
| Scribble | Outside agency or partner: the article wave and the monthly AI-visibility report | The monthly report, query list | ASK who holds the login |

## Teams
| Team | Members seen | What they own |
|---|---|---|
| Protocol | Gokul, others unnamed | go-moi releases and network upgrades, the registry, chain constants. Writes the release note |
| Voyage | Vinay, Gokul, Prakhar | The explorer app and `voyage-api`; Upendhar and Srikar own its workflows |
| SDK | Gokul, Harsh Rastogi, Vinay | `js-moi-sdk`, npm publishing, R2 skill zip |
| DevOps | Upendhar, Srikar | VMs, Teleport, GHCR, DNS, nginx, deploy scripts |
| Marketing | Sai Kiran, Vardan, Piyush, Sujatha, Louis, Harsh (Galxe) | Socials, events calendar, standups, KOLs, podcast, Wikidata |
| Reviewers | Rahul, Gokul, Robert Špendl | Sign-off per area: Rahul public pieces and standards, Gokul code and protocol, Robert Coco |
GitHub org admins on `sarvalabs/moi-project` (2026-09-15): gokul, chandra, git, adithya, upendhar. Only repo admins can edit Actions secrets.

## Who to ask for what
| Need | Ask |
|---|---|
| Anything on a VM, DNS, TLS, deploy script, Teleport, GHCR | Upendhar (Points box, CI/CD, GHCR); Srikar (website server, Voyage VMs, MCP deploys) |
| Chain facts after a reset, the registry id, the network ID RPC | Gokul |
| New SDK, go-moi or Voyage release versions | Vinay, or the Discord release log |
| Approval of a public piece or an upstream filing | Rahul |
| Community numbers, social calendar | Sai Kiran |
| Call dates and guests | Vardan, then confirm with Rahul |
| Create or change an Actions secret | An org admin of that repo, and the operator's yes first (`consent-and-identity.md` section 1) |
| Who owns a vendor account | Unknown for most. Rahul, then `keys-and-access.md` |
| History of the previous operator's work | The handover docs in `project-handover-docs/`. Where they are silent: not recorded (the previous DevRel's notes); ASK: Rahul |

## How people are reached
- Discord: the release log, DevOps asks, community. Slack: marketing inputs for the call. Google Meet: calls, with Gemini or Otter notes. GitHub: review requests. One env file was once sent over Teams.
- Past DevOps messages worked as short, human, specific notes: the problem, the solution, the exact action for them, how to verify. One task per message. No labels such as "Owner:". No em dashes. Do not ask DevOps for a secret value; secrets live in GitHub.
- Do not reopen settled items. The Launchpad platform wallet variable (`MOI_PLATFORM_MNEMONIC`) was cleared with DevOps by 2026-08-03. Read `message-traps.md` trap 2 and `house-style.md` section 4 ("Never raise") before you write to DevOps; for anything else that may be settled, ASK: Rahul.
- Weekly updates to Rahul list completed work only. To-dos are labelled as to-dos.
- Send nothing without the operator's yes (`consent-and-identity.md`).

## Not yet known
- Titles and reporting lines for Rahul, Gokul, Upendhar, Srikar. ASK: Rahul.
- Which of Upendhar or Srikar owns the Dataroom and Launchpad servers (Srikar: website server, Voyage VMs, MCP deploys; Upendhar: Points box, CI/CD, GHCR). ASK: Rahul.
- The channel the protocol team uses to announce a reset and a new registry id, and who the named contact is besides Gokul.
- How a protocol release note reaches DevRel (Discord, Slack or email) and who writes it.
- Who currently hosts and moderates the community call.
- The video editor's contact. Whether any support channel is monitored, and by whom.
