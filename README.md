# MOI DevRel handover

Everything the next DevRel person at MOI needs, in one place: the docs that say how each product is run, and the Claude skills that do the work. Read the docs first. Install the skills when you are ready to act.

## The docs

Each one follows the same shape: status, owners, settings, the process step by step, the Claude prompts to use, and what is still open.

| Doc | What it holds |
|---|---|
| `project-handover-docs/COMMUNITY-CALL.md` | The monthly call. Who owns what, the nine-day timeline, the announcement schedule, where the decks and recordings live. |
| `project-handover-docs/DEV-WEBINARS.md` | The Builders sessions. From the planning meeting with Rahul to the post-session blog, posting through Buffer, the session bounty, how a session folder is laid out. |
| `project-handover-docs/BLOG.md` (draft) | How the blog is built and deployed, the writing process, the monthly newsletter, images, editing a published post, the search rules. |
| `project-handover-docs/MOI-WEBSITE.md` | The website repo and the blog it carries: settings, deploys, publishing a post, the parked chatbot and calendar. |
| `project-handover-docs/DATAROOM.md` | The investor document room: the admin page, adding and replacing documents, how the home page picks its tiles, Supabase, and the steps to switch the chat and the Events page back on. |
| `project-handover-docs/AGENT-LAUNCHPAD.md` | The Agent Launchpad: stack, settings, shipping, what to redo after a devnet reset, and how to present it with the intro session deck. |
| `project-handover-docs/MCP-SERVER.md` (draft) | The MOI MCP server: how a chat assistant reads and writes MOI through it, the two repos, deploys, health, troubleshooting, the open publishing questions. |
| `project-handover-docs/POINTS-PROGRAM.md` (draft) | The Points Program: tasks, X campaigns, webinar bounties, deploys, settings, the database rules. |
| `project-handover-docs/ENV-VARS.md` | Every environment variable across the products in one index, with where each value comes from, the consoles, and who holds each login. |
| `project-handover-docs/LIST-OF-DEPENDENCIES.md` | Every dependency by name, with its owner, its settings and its to-dos, in Adithya's own words. |
| `project-handover-docs/MIGRATION-LIST.md` | What still moves to a company login, with the transfer steps, and what has already moved. |
| `project-handover-docs/VIDEOS.md` (draft) | The recorded walkthroughs, one per product, with the links. |
| `others/webinars/` | Past session material worth reusing: the session 7 storyline and the intro deck. |
| `others/standards/` | The x402 standards submission package. |

## The skills

The folder `skills/` holds the ten MOI skills under `skills/moi/`, the generic repo-handover skill under `skills/extra/`, and the two notes that describe the library.

Ten skills. Each is a folder under `skills/moi/` with a `SKILL.md`; a branch is a sub-folder with a `GUIDE.md`. Say what you need in plain words and Claude loads the right one.

| Skill | What it does | Branches |
|---|---|---|
| `moi-devrel` | Start here. The house rules, who is who, and the map of every other skill. | `ship`, `design`, `claim-check`, `explain`, `call-digest`, `test-round` |
| `moi-webinar` | Builders sessions and community calls, from planning to the day itself. Posting goes through its Buffer script. | `deck`, `community-call` |
| `moi-blog` | Write, polish, ship and announce a post. | `release-pack` |
| `moi-docs` | The docs sites and their search visibility. | `geo` |
| `moi-launchpad-ops` | Run the Launchpad, and the Explorer beside it. | `explorer` |
| `moi-mcp-ops` | Run the MCP server: health, shipping, connecting, rollback. | |
| `moi-web-products-ops` | Run the website, the Dataroom and the Points Program. | |
| `moi-devnet-reset` | The order of work across every product after a devnet reset. | |
| `moi-standards-submission` | File a standards submission, such as a CAIP or the x402 scheme. | |
| `moi-education-programs` | Run an education program with a university or a cohort. | |

## Also here

- `skills/ARCHITECTURE.md`: how the library is shaped and how it was checked.
- `skills/SKILL-STANDARD.md`: the bar every skill meets. Read it before changing one.
- `others/research/`: the notes the skills were built from. Provenance, not for installing.
- `others/legacy-skills/`: the old blog, deck and design skills. Superseded, kept for reference.
- `skills/extra/repo-handover/`: a generic skill for turning any repo into a handover skill like these.

## Install

Skills load from `~/.claude/skills/`. Link each folder and set `SKILLS`, which every skill expects:

```bash
for s in ~/moi-devrel-skills/skills/moi/*/; do ln -s "$s" ~/.claude/skills/"$(basename "$s")"; done
export SKILLS=~/moi-devrel-skills/skills/moi
```

If older skills with the same names are already there (`moi-blog`, `moi-deck`, `moi-design`), move them aside first, or they will load beside the new ones and contradict them.
