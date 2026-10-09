# MOI DevRel handover

Everything a new developer-relations hire at MOI needs, in one private repo: the Claude skills that do the work, and the docs that say how each product is run. Start with the install below, then open `skills/moi-devrel/SKILL.md`.

## Where to go

| You want to | Open |
|---|---|
| Start doing the job | `skills/moi-devrel/SKILL.md`. It holds the house rules, who is who, and points to every other skill |
| Run a webinar or a community call | `skills/moi-webinar/` (branches `deck`, `community-call`) |
| Write, ship or announce a blog post | `skills/moi-blog/` (branch `release-pack`) |
| Work on the docs sites | `skills/moi-docs/` (branch `geo`) |
| Operate the Agent Launchpad or the Explorer | `skills/moi-launchpad-ops/` (branch `explorer`) |
| Operate the MCP server | `skills/moi-mcp-ops/` |
| Operate the website, the Dataroom or the Points Program | `skills/moi-web-products-ops/` |
| Recover every product after a devnet reset | `skills/moi-devnet-reset/` |
| File a standards submission | `skills/moi-standards-submission/` |
| Run an education program | `skills/moi-education-programs/` |
| Read how a product is run: status, owners, settings, process, open items | `docs/COMMUNITY-CALL.md`, `docs/DEV-WEBINARS.md`, `docs/BLOG.md`, `docs/MOI-WEBSITE.md`, `docs/DATAROOM.md`, `docs/AGENT-LAUNCHPAD.md`, `docs/MCP-SERVER.md`, `docs/POINTS-PROGRAM.md` |
| See every dependency by name, with its owner and to-dos | `docs/LIST-OF-DEPENDENCIES.md` |
| See what still moves to a company login, and how | `docs/MIGRATION-LIST.md` |
| Read the Launchpad's long-form handover | `docs/HANDOVER.md` |
| Reuse past webinar material (demo plans, cheat sheets, the intro deck) | `docs/webinars/` |
| Read the x402 standards submission package | `docs/standards/x402-review-package/` |
| Understand how the library is shaped and how it was checked | `ARCHITECTURE.md` |
| Change a skill | `SKILL-STANDARD.md` first |
| See the research the skills were built from | `_research/` (provenance, not for installing) |
| Find the old `moi-blog`, `moi-deck` and `moi-design` skills | `legacy-skills/` (superseded; kept for reference only) |
| Turn any other repo into a handover skill | `extra-skills/repo-handover/` |

## Install

Skills load from `~/.claude/skills/` (every project) or `<repo>/.claude/skills/` (one project). Link each skill folder and set `SKILLS`, which every skill expects:

```bash
for s in ~/moi-devrel-skills/skills/*/; do ln -s "$s" ~/.claude/skills/"$(basename "$s")"; done
export SKILLS=~/moi-devrel-skills/skills
```

Older skills may already be there under the same or a retired name (`moi-blog`, `moi-deck`, `moi-design`). List them with `ls -ld ~/.claude/skills/moi-*` and move any real folder aside first: an old `moi-blog` would stop the link, and an old `moi-deck` or `moi-design` would load beside the new branches and contradict them.

## Use

Say what you need in plain words: "I'm new to MOI DevRel, where do I start", "I own Community Call 15", "check this deck". Claude loads the matching skill, and the skill routes to the branch. Each skill ends with a hand-back: what was made, what remains, and whether it is ready.
