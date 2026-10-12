---
name: {{repo-slug}}-ops
description: Operating, debugging, deploying or changing {{Repo name}} ({{remote}}) — the {{one-line what}}. Use this whenever a task mentions {{repo-slug}}, {{public host}}, {{a distinctive env var}}, {{a distinctive dir or service}}, or anything that runs on {{where it runs}}, even if the repo is not named.
---

# {{Repo name}}

{{Two or three sentences: what it is, who it is for, what it talks to. Written for someone who has never opened the repo.}}

## Where things are

| Thing | Where |
| --- | --- |
| Source of truth | `{{remote}}`, branch `{{prod branch}}` deploys; `{{work remote}}` is where work happens |
| Local clone | `{{path}}` |
| Runs at | {{host / container / platform}}, public at `{{url}}` |
| Data | {{database and where it lives}} |
| Secrets | {{vault / CI secrets / env file on host}}. See `references/env.md` |
| Logs and metrics | {{where to look when it misbehaves}} |
| Owner and escalation | {{person or team}}, {{how to reach them}} |

## Run it

```bash
{{copy-pasteable local run, with concrete values, no placeholders except secrets}}
```

Expected: {{what you should see when it is working}}.

## Deploy it

{{One paragraph: what triggers a deploy, what it builds, where it lands. Then the exact rollback.}}

Rollback: {{command or steps}}.

## Before you change anything

- {{The one rule that breaks things if ignored, e.g. a secret that cannot be rotated}}
- {{The second}}
- Run `scripts/verify.sh` first. It is read-only and tells you whether this skill still matches the repo.

## Modules

| Need | Read |
| --- | --- |
| Every environment variable, what it does, where the value comes from, whether it can be rotated | `references/env.md` |
| Deploy, rollback, the failures seen so far and what fixed them | `references/runbook.md` |
| Why it is built this way, including things learned the hard way | `references/decisions.md` |
| File map, external assets outside git, accounts and who holds them | `references/map.md` |
| Branch state, unpushed work, open threads, as of a date | `references/state.md` |

Keep this skill honest: when you change a deploy target, an env var or a decision, change the matching reference in the same commit. A handover that drifts from the code is worse than none, because it is trusted.
