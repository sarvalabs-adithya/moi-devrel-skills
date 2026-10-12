# Launchpad change checklist

From your working copy of `sarvalabs/moi-agent-launchpad`, make the folder ignore itself first, so a stray `git add` cannot publish it, then copy this file in and fill it in: `mkdir -p launchpad-notes && printf '*\n' > launchpad-notes/.gitignore` and `cp "$SKILLS/moi-launchpad-ops/templates/change-checklist.md" "launchpad-notes/change-<YYYY-MM-DD>-<slug>.md"`. Never commit this file or paste it into a public place: it can name accounts and people. Never write a secret, an IP address or a VM login name in it. Runbook: `references/ship-a-change.md`. Settings: `references/settings-and-secrets.md`. Migrations: `references/database.md`.

Change: <one line>
Date (UTC): <YYYY-MM-DD HH:MM>   Operator: <name>   Who approves the merge: <name, or "unknown: ASK: Rahul">
Kind (tick): [ ] code  [ ] setting  [ ] secret  [ ] migration  [ ] runtime bundle  [ ] workflow or Dockerfile

## Before
- [ ] Health before. RESULT line from `launchpad-health.sh`: <paste>
- [ ] Last deploy runs read (`gh run list -R sarvalabs/moi-agent-launchpad -L 5`): <last green commit and time>
- [ ] Extra steps for this kind done (table in `ship-a-change.md`): <which>
- [ ] Typecheck, tests and build pass locally; strict install proven if the lockfile changed
- [ ] Migration needed? [ ] no  [ ] yes: file <name>, applied and checked first (`database.md`), time <UTC>
- [ ] Setting changes: name <NAME>, old value (variables only, never a secret) <value or "n/a">, rule <free / step / never>
- [ ] What this change cannot undo: <on-chain effects, data, secrets>
- [ ] How I will know it is live (no endpoint reports the commit): <the behaviour or value I will look at>

## Gates (each needs the operator's yes in this conversation; note when)
| Action | Operator's yes (quote or time) |
|---|---|
| Push branch <name> to <remote> | |
| Open pull request | |
| Merge to `master` (this deploys to production) | |
| Manual workflow run | |
| Set variable or secret <NAME> | |
| Run migration <file> in the SQL editor | |
| Re-run `setWebhook` (the operator types it) | |
| Spend devnet funds or deploy on devnet | |
| Download a file (name, source, size) | |
| Any message sent to DevOps, the protocol team or users | |

## After
- [ ] Deploy run green: <run id, duration>
- [ ] Health after. RESULT line: <paste>
- [ ] The change is visible: <what you saw>
- [ ] A second health read 30 seconds later agrees (chain figures are samples)
- [ ] Anything that stayed red or WARN, and why: <text>

## Hand-back
Produced: <what, with the PR number or run id>
Remaining: <numbered, each with an owner>
Not verified: <say so, or "none">
Ready: <yes or no, because ...>
