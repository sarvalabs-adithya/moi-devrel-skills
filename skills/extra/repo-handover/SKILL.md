---
name: repo-handover
description: "Turn one repository into a handover skill: a `<repo>-ops` skill a successor (or Claude) can run the project from without the original author. Use this whenever someone asks to hand over, document for a successor, offboard, write a runbook, capture \"how this is deployed\", inventory env vars, or \"make a skill for this repo\", even if they do not say the word handover. Read-only on the repo; never pushes or opens PRs."
---

# Repo handover

A handover is not a document, it is a set of things a successor can *run*. The research behind this
skill (see `references/research.md`) says the same four pieces keep appearing in every checklist,
runbook guide and decision-record practice, and a handover fails when one is missing:

1. **Orientation**: what it is, where it runs, where the data and secrets live, who owns it.
2. **A runbook**: deploy, rollback, health checks, failures already seen. Copy-pasteable, with
   expected output.
3. **Decisions**: why it is built this way, including what was learned the hard way, so the
   successor does not reverse it.
4. **The inventory**: every env var with its source, every asset outside git, every account.

A Claude skill is the right container because it is consulted at the moment of action, carries
runnable checks, and loads progressively: the orientation is always in context, the references only
when needed.

## Process

| # | Do | How |
| --- | --- | --- |
| 1 | Inventory the repo, read-only | `bash ~/moi-devrel-skills/skills/extra/repo-handover/scripts/inventory.sh <repo>` (the library clone from the root README). Gives branch state, deploy files, env names, and the names the code reads that no template documents |
| 2 | Read what already exists | any `HANDOFF.md`, `RUNBOOK.md`, `docs/`, workflow files under `.github/`, the Dockerfile and compose file. **Trust workflows over READMEs**: READMEs describe where a project started, workflows describe where it deploys today |
| 3 | Ask the owner the unknowables | who owns it, who to escalate to, which accounts exist and who holds them, what is outside git, what was scratch versus intended. Nothing in the repo answers these. The owner is the person recorded in the repo's README or CODEOWNERS; if neither names one, ASK: Rahul |
| 4 | Fill the template | copy `~/moi-devrel-skills/skills/extra/repo-handover/assets/template/` to `~/.claude/skills/<repo-slug>-ops/`, replace every `{{placeholder}}`, delete sections that do not apply rather than leaving them hollow |
| 5 | Verify | `bash ~/moi-devrel-skills/skills/extra/repo-handover/scripts/verify.sh <repo> <skill dir>` compares documented env vars to the ones the code reads and prints the branch state, so the first draft is already checked against reality |
| 6 | Hand back | the skill path plus a list of what you could not source. Say which claims came from the author, which from the code |

## What the template enforces

- **Concrete values, not placeholders**, everywhere except secrets. A runbook that says
  `<your-host>` is not a runbook. Where a value is secret, say where the readable copy lives.
- **Expected output next to every command.** A successor at 2am needs to know what healthy looks
  like, not just what to type.
- **Rollback beside every deploy.** A change procedure without its reverse is half written.
- **Every secret marked rotate-freely, rotate-with-a-step, or never.** The never ones are the
  handover's most important lines.
- **Assets outside git get their own table.** Sheets, dashboards, DNS, bot accounts, third-party
  consoles. These are what every checklist says people forget.
- **State is dated.** `state.md` opens with "as of <date>", because branch state rots within days.
- **Decisions keep the why.** Context, options, decision, consequences. "Learned the hard way"
  entries are the most valuable in the whole skill.

## Rules from the first handover

Stay local and read-only. Never push, open a PR, or run a `gh` command against the repo; the point
is to prepare, not to announce. Keep personal repos out of work handovers. When the README and the
deploy workflow disagree, the workflow wins and the README gets a note.

## Files

| File | Purpose |
| --- | --- |
| `assets/template/SKILL.md` | the per-repo skill, orientation plus module table |
| `assets/template/references/env.md` | the env inventory format |
| `assets/template/references/runbook.md` | deploy, rollback, health, failures |
| `assets/template/references/decisions.md` | ADR-style log |
| `assets/template/references/map.md` | file map, outside-git assets, accounts, history |
| `assets/template/references/state.md` | dated branch and work state |
| `scripts/inventory.sh` | read-only seed data for a new skill |
| `scripts/verify.sh` | drift check between a skill and its repo |
| `references/research.md` | where these rules come from |
