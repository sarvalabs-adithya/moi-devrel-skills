# Where the handover rules come from

Compiled 29 September 2026 from four external sources and two internal documents. Each rule in
`SKILL.md` traces to something here.

## The sources

| Source | What it is | What it contributed |
| --- | --- | --- |
| Simple Thread, [Checklist for handing off a software project](https://www.simplethread.com/handing-off-a-software-project/) | a consultancy's list from handing projects to client teams | the inventory of things outside the code: accounts, external assets, history, housekeeping |
| OpsLevel, [Production readiness in depth](https://www.opslevel.com/resources/production-readiness-in-depth) | a production readiness review checklist | ownership and contact per service, on-call, logging and metrics locations, deploy automation, backups |
| Google Cloud, [Architecture decision records overview](https://docs.cloud.google.com/architecture/architecture-decision-records) | the ADR practice | the decisions module: context, options, decision, consequences; why newcomers need the *why* |
| OneUptime, [How to create effective runbooks](https://oneuptime.com/blog/post/2026-02-02-effective-runbooks/view) | SRE runbook guidance | copy-paste commands, expected outputs, rollback, ownership, the anti-patterns |
| `nno code agentapp/docs/HANDOFF.md` | the launchpad's own operator guide, written while building | the local exemplar: secrets recovery checklist, "learned the hard way" hosting economics, file map |
| `MOI-Webinars/session-8-policies/RUNBOOK.md` | a live-session run sheet | timed steps, "if it breaks live", likely questions with short answers |

## What every source agrees on

**Four things, not one document.** Orientation, runbook, decisions, inventory. The handoff checklist
is mostly inventory; the readiness review is mostly orientation and operations; the ADR practice is
decisions; the runbook guide is the runbook. Nobody covers all four, which is why handovers built
from one of them fail.

**Ownership is a field, not a feeling.** The readiness checklist's first item is "service owners
are identified, contact information and methods are provided". A repo with no named owner and no
escalation path is not handed over, whatever else is written.

**Runbooks are executed, not read.** The runbook guide's properties: step-by-step, copy-paste
ready without mental substitution, expected outputs for success and failure, clear escalation,
metadata so the reader knows they have the right document, tested, updated after every incident.
Its anti-patterns are the mirror image: passive voice, placeholder variables, no rollback, never
tested in staging, stale after infrastructure changed, so comprehensive it gathers dust, no owner.

**The why outlives the what.** ADRs exist so that "when someone leaves, their decisions stay" and
so newcomers do not reverse choices they do not understand. The launchpad's own guide shows this at
small scale: its hosting-economics section explains why the app left Vercel, and without it a
successor would put it back.

## What gets forgotten

The handoff checklist names it directly: historical project data and assets outside version
control. Sheets, dashboards, design files, discovery docs, chat logs, bug trackers, DNS and
registrar logins, bot accounts, third-party consoles. And in-progress work: the checklist says to
document it in pull request notes and delete dead branches before handing over.

The launchpad added one more: secrets that were stored write-only. Vercel's sensitive env vars and
GitHub Actions secrets cannot be read back, so a migration is a secret-recovery exercise. The guide
says to put every value in a shared vault. Ours were not, which is why the VM's env file is the
only readable copy.

## Why a skill rather than a document

A document is read once, at handover, then rots. A skill is loaded whenever the repo is touched.
Three properties make it the better container:

- **Progressive disclosure.** The orientation is a few hundred words and is always present when the
  repo comes up. The env inventory, runbook and decisions load only when the task needs them.
- **It can carry scripts.** `verify.sh` checks the env inventory against what the code actually
  reads, so drift is detected instead of trusted.
- **It triggers on the repo's own vocabulary.** Host names, env var names, directory names. A
  successor who types "why is launchpad.moi.technology returning 502" gets the runbook without
  knowing a handover exists.

## What our existing docs did well and badly

The launchpad guide is strong on status, secrets recovery and lessons, and it was written while the
work happened, which is the only time the why is still known. It is weak on structure: it accreted
chronologically, so "how is this deployed" is spread across five sections, and the README it sits
beside still describes a hosting setup the guide itself says was abandoned. That contradiction cost
a wrong handover draft on 29 September. The template splits orientation from history so the
current truth has one home.

## Rules derived

1. Four modules, always: orientation, env, runbook, decisions. Plus map and state.
2. Owner and escalation in the first table of the orientation.
3. Every command copy-pasteable with real values; secrets are the only placeholders, and each says where its readable copy is.
4. Expected output beside every command; rollback beside every deploy.
5. Every secret labelled: rotate freely, rotate with a step, or never.
6. Assets outside git and accounts get their own table.
7. State is dated and is expected to rot; the verify script says when it has.
8. Decisions keep the why, and "learned the hard way" entries are written the day they are learned.
9. Deploy workflows outrank READMEs when they disagree.
10. Read-only while preparing. No pushes, no PRs, no notifications to the team.
