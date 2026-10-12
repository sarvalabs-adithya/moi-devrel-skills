# Launchpad incident note

From your working copy of `sarvalabs/moi-agent-launchpad`, make the folder ignore itself first, then copy this file in and fill it in: `mkdir -p launchpad-notes && printf '*\n' > launchpad-notes/.gitignore` and `cp "$SKILLS/moi-launchpad-ops/templates/incident-note.md" "launchpad-notes/incident-<YYYY-MM-DD>-<slug>.md"`. Do not commit it or paste it into a public place. Never write a secret, an IP address, a VM login name or the detail of a security weakness in it. Label every cause "known", "suspected" or "unknown". Troubleshooting: `references/troubleshoot.md`. Rollback: `references/rollback.md`.

Title: <what broke, in plain words>
Detected (UTC): <time>   By: <health script / a user report / DevOps / an alert>   Operator: <name>

## What we saw
Exact message or symptom: <word for word>
Health output at detection: <paste the lines, not secrets>
Since when, and who is affected: <times, user count if known, or "unknown">

## Cause
<known / suspected / unknown>: <text>. Evidence: <the row in `troubleshoot.md`, the log line, the run id>

## What we did
| Time (UTC) | Action | Who did it | Operator's yes (for a gate) |
|---|---|---|---|
| | | | |

## What was not undone
<on-chain effects, data, secrets, installed agents, or "nothing">

## Verification
Health output after: <paste>   Second read 30 seconds later: <paste>
The symptom's own check: <what you saw>

## Follow-ups
| What | Owner | By when |
|---|---|---|
| | | |

## Open ASK lines
<each question and the person: Adithya for history, Rahul for roles and policy, Upendhar for anything on the VM, Gokul for chain facts>

## Not verified
<say so, or "none">
