# MOI DevRel handover

Everything the next DevRel person at MOI needs, in one place: the docs that say how each product is run, and the Claude skills that do the work. Read the docs first. Install the skills when you are ready to act.

## The docs

The product and program docs follow the same shape: status, owners, settings, the process step by step, the Claude prompts to use, and what is still open. ENV-VARS, LIST-OF-DEPENDENCIES, MIGRATION-LIST and VIDEOS are index and inventory docs instead: they list things and do not follow that shape. The docs are grouped by who reads them. The three programs both teams run sit under Everyone, and each of those docs says near the top which sections are whose.

**Everyone: the programs marketing and developers run together**

| Doc | What it holds |
|---|---|
| `project-handover-docs/COMMUNITY-CALL.md` | The monthly call. Who owns what, the nine-day timeline, the announcement schedule, where the decks and recordings live. |
| `project-handover-docs/DEV-WEBINARS.md` | The Builders sessions. From the planning meeting with Rahul to the post-session blog, posting through **Buffer** (a social media scheduling service), the session bounty, how a session folder is laid out. |
| `project-handover-docs/BLOG.md` | How the blog is built and deployed, the writing process, the monthly newsletter (sent through **Mailchimp**, an email marketing service), images, editing a published post, the search rules. |
| `project-handover-docs/VIDEOS.md` | The recorded walkthroughs, a product demo and a skill video per product, with the links and what is still to record. |

**Marketing**

| Doc | What it holds |
|---|---|
| `project-handover-docs/BLOG.md` | Announcing a post (check with marketing first), the Mailchimp newsletter, images. |
| `project-handover-docs/COMMUNITY-CALL.md`, `DEV-WEBINARS.md` | The **Luma** (event page service) pages, the posting schedule, Buffer, the deck. |
| `project-handover-docs/MOI-WEBSITE.md` | Publishing and announcing a post, and switching on the community calls block with the Luma link. |
| `others/webinars/` | Past session material worth reusing: the session 7 storyline and the intro deck. |

**Developers and DevOps**

| Doc | What it holds |
|---|---|
| `project-handover-docs/AGENT-LAUNCHPAD.md` | The Agent Launchpad: stack, settings, shipping, what to redo after a **devnet** (MOI's test network) reset, and how to present it with the intro session deck. |
| `project-handover-docs/MCP-SERVER.md` | The MOI **MCP** (Model Context Protocol) server: how a chat assistant reads and writes MOI through it, the two repos, deploys, health, troubleshooting, the open publishing questions. |
| `project-handover-docs/POINTS-PROGRAM.md` | The Points Program: tasks, X campaigns, webinar bounties, deploys, settings, the database rules. |
| `project-handover-docs/DATAROOM.md` | The investor document room: the admin page, adding and replacing documents, how the home page picks its tiles, **Supabase** (a hosted database), and the steps to switch the chat and the Events page back on. |
| `project-handover-docs/MOI-WEBSITE.md` | The website repo: settings, deploys, the server and the chatbot, which both stay as they are. |
| `project-handover-docs/AGENT-SKILLS.md` | The **Coco** (MOI's smart contract language) and **js-moi-sdk** (the JavaScript SDK) agent skills: who builds each, where they are published, how to re-check one when a release lands. |
| `project-handover-docs/ENV-VARS.md` | Every environment variable across the products in one index, with where each value comes from, the consoles, and who holds each login. |
| `project-handover-docs/LIST-OF-DEPENDENCIES.md` | Every dependency by name, with its owner, its settings and its to-dos, in Adithya's own words. It is a snapshot from 4 October; the product docs supersede it. |
| `project-handover-docs/MIGRATION-LIST.md` | What still moves to a company login (the Telegram bot), with the transfer steps, and what has already moved. |
| `project-handover-docs/OTHER-PROJECTS.md` | Moinkee, Agent dating and MOI Sprint: inactive side projects, now in the sarvalabs org (moved 14 October 2026), and how Moinkee's Pinata files were moved to the company account. |
| `others/standards/` | The **x402** (an HTTP payment standard) standards submission package. |

## The skills

The folder `skills/` holds the ten MOI skills under `skills/moi/`, the generic repo-handover skill under `skills/extra/`, and the two notes that describe the library.

Ten skills. Each is a folder under `skills/moi/` with a `SKILL.md`; a branch is a sub-folder with a `GUIDE.md`. Say what you need in plain words and Claude loads the right one.

| Skill | What it does | Branches | For |
|---|---|---|---|
| `moi-devrel` | Start here. The house rules, who is who, and the map of every other skill. | `ship`, `design`, `claim-check`, `explain`, `call-digest`, `test-round` | Everyone |
| `moi-webinar` | Builders sessions and community calls, from planning to the day itself. Posting goes through its Buffer script. | `deck`, `community-call` | Everyone |
| `moi-blog` | Write, polish, ship and announce a post. | `release-pack` | Everyone |
| `moi-docs` | The docs sites and their search visibility. | `geo` | Developers |
| `moi-launchpad-ops` | Run the Launchpad, and the Explorer beside it. | `explorer` | Developers |
| `moi-mcp-ops` | Run the MCP server: health, shipping, connecting, rollback. | | Developers |
| `moi-web-products-ops` | Run the website, the Dataroom and the Points Program. | | Developers |
| `moi-devnet-reset` | The order of work across every product after a devnet reset. | | Developers |
| `moi-standards-submission` | File a standards submission, such as a **CAIP** (a Chain Agnostic Improvement Proposal) or the x402 scheme. | | Developers |
| `moi-education-programs` | Run an education program with a university or a cohort. | | Everyone |

## Also here

- `skills/ARCHITECTURE.md`: how the library is shaped and how it was checked.
- `skills/SKILL-STANDARD.md`: the bar every skill meets. Read it before changing one.
- `others/README.md`: what each folder under others/ holds and where to start.
- `others/research/`: the notes the skills were built from. Provenance, not for installing.
- `others/legacy-skills/`: the old blog, deck and design skills. Superseded, kept for reference.
- `skills/extra/repo-handover/`: a generic skill for turning any repo into a handover skill like these.

## Install

Skills load from `~/.claude/skills/`. The repo is private, so clone it with the GitHub CLI (`gh auth login` first if `gh auth status` fails). Link each folder, and make `SKILLS` permanent, because every skill expects it:

```bash
gh repo clone sarvalabs/moi-devrel-skills ~/moi-devrel-skills
mkdir -p ~/.claude/skills
for s in ~/moi-devrel-skills/skills/moi/*/; do ln -sfn "$s" ~/.claude/skills/"$(basename "$s")"; done
echo 'export SKILLS="$HOME/moi-devrel-skills/skills/moi"' >> ~/.zshrc
source ~/.zshrc
echo "$SKILLS"
```

The last line should print the path ending in `skills/moi`. `ln -sfn` makes a re-run safe: it replaces the links instead of failing. Add the `export` line to `~/.zshrc` once only.

If older skills with the same names are already there (`moi-blog`, `moi-deck`, `moi-design`), move them aside first, or they will load beside the new ones and contradict them.
