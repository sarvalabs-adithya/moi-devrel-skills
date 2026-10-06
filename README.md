# MOI DevRel skills

Claude skills that let a new developer-relations hire at MOI do the job without the history, plus the info docs they were built alongside. Private repository: keep it that way — see "Held back" below for what was deliberately left out.

## What is here

| Path | What |
|---|---|
| `skills/` | The skills. This is the part people install. |
| `ARCHITECTURE.md` | The design: every skill, why it is shaped this way, build order. |
| `SKILL-STANDARD.md` | The bar every skill meets. Read before changing one. |
| `_research/` | Ten research notes (111 processes) the skills were built from. Provenance, not for installing. |
| `docs/` | The info docs: Community Call, Dev Webinars, Agent Launchpad, MOI Website, migration list, Launchpad handover; `docs/webinars/` (runbooks, session notes, the intro deck); `docs/standards/` (the x402 / CASA review package). |
| `extra-skills/` | Other skills built along the way that aren't part of the DevRel library — `repo-handover`. |
| `legacy-skills/` | The older `moi-blog`, `moi-deck`, `moi-design`, superseded by branches in `skills/`. Kept for reference; do **not** install them beside the new ones (see Install). |

## Status, as of 2026-10-04

Ten skills, each with its branches inside it. All of it was built, hostile-reviewed, fixed and tested as a whole.

| Skill | Branches inside it |
|---|---|
| `moi-devrel` (start here; points to all the others) | `ship`, `design`, `claim-check`, `explain`, `call-digest`, `test-round` |
| `moi-webinar` | `deck`, `community-call` |
| `moi-blog` | `release-pack` |
| `moi-docs` | `geo` |
| `moi-launchpad-ops` | `explorer` |
| `moi-mcp-ops` | |
| `moi-web-products-ops` (website, Dataroom, Points) | |
| `moi-devnet-reset` | |
| `moi-standards-submission` | |
| `moi-education-programs` | |

A branch is a folder with a `GUIDE.md`, for example `skills/moi-webinar/deck/GUIDE.md`. `ARCHITECTURE.md` says what each does.

## Install

Skills load from `~/.claude/skills/` (every project) or `<repo>/.claude/skills/` (one project). Link each skill folder:

```bash
for s in ~/moi-devrel-skills/skills/*/; do ln -s "$s" ~/.claude/skills/"$(basename "$s")"; done
```

Older skills may already be there under the same or a retired name (`moi-blog`, `moi-deck`, `moi-design`). List them with `ls -ld ~/.claude/skills/moi-*` and move any real folder aside first: an old `moi-blog` would stop the link, and an old `moi-deck` or `moi-design` would load beside the new branches and contradict them. Then set `SKILLS` once, as every skill expects:

```bash
export SKILLS=~/moi-devrel-skills/skills
```

## Use

Say what you need in plain words. "I'm new to MOI DevRel, where do I start", "I own Community Call 15", "check this deck". Claude loads the matching skill, and the skill routes to the branch. Each skill ends with a hand-back: what was made, what remains, and whether it is ready.

## How the library was checked

1. Every skill: a hostile reviewer tried to refute each statement against `_research/` and the source repos, ran every script on good and bad input, and fixed what it found.
2. The whole library: a consistency critic read all the skills against each other, two simulated new hires ran real tasks using only `skills/`, and a routing test put 30 plain requests against the descriptions.
3. Findings were applied or rejected with a written reason, then every script was run again.

About 530 findings in all, 38 of them marked blocker. Most blockers were scripts that could print a secret-shaped value, examples holding a key-shaped id, and steps with no gate: those are fixed. Six came from a simulated new hire and were questions only a person can answer; they are carried as `ASK:` lines.

## Open before this is shared

- Keys and accounts: `skills/moi-devrel/references/keys-and-access.md` lists every one by name with status TBD.
- The `ASK:` lines. Each names who can answer. Search for `ASK:` to list them.
- Several source files exist only on the previous operator's machine (the community call 14 folder, the release pack, the handover notes). The skills say so wherever they point at one.
- The examples in `moi-claim-check/examples` and `moi-community-call/examples` are cleaned of private paths and names, but nobody has yet said they may be published.
- Seven products carry a one-line note that a security finding is open. The detail is deliberately not in the library.

## Held back

Deliberately not in this repository, because they spell out how to reach security problems that were still open when it was created (2026-10-06). The library's own rule is that this detail stays out; the one-line notes in the skills remain. The originals live only on the author's machine:

- `_research/ops-web-products.md`, `_research/ops-chain-products.md`, `_research/standards-and-programs.md`, `_research/_summaries.json`
- `docs/DEPENDENCIES.md`, `docs/LIST-OF-DEPENDENCIES.md`, `docs/FIX-PLAN.md`, the Agent Explorer design-issue draft

Also never committed: `.env` files, the `_backup-*` snapshots (taken before secret-shaped values were cleaned), and third-party skills installed alongside these.
