# The standard every skill in this library meets

Read this before writing or changing any skill here.

## Who a skill is for

Claude, working beside a MOI developer-relations person who has never done this task before. Assume the human is new: they do not know the repos, the people, the accounts or the history. The skill carries the process so they do not have to ask anyone.

The skill is not written for Adithya. His name appears only where he is a fact (author of a past artefact, a person to ask). Never write "the user prefers"; write the rule.

## Folder shape

```
skills/<skill-name>/
  SKILL.md          entry point, 150 lines at most
  references/       one topic per file, 200 lines at most, read on demand
  templates/        files to copy and fill in
  scripts/          executable, tested, safe by default
  examples/         one real past run, cleaned up
  evals/evals.md    test prompts with the behaviour expected
```

Only `SKILL.md` is required. Add the others when they earn their place.

## Branches

The library has ten skills. Everything else is a branch: a sub-tool that lives inside the skill that uses it most.

```
skills/<skill>/<branch>/
  GUIDE.md        the branch's runbook: same anatomy as a SKILL.md, no frontmatter, 150 lines at most
  references/  templates/  scripts/  examples/  evals/
```

- Only the skill has a `SKILL.md` and a description. The description carries the words that should load any of its branches, in 1,024 characters at most, written as a double-quoted YAML string.
- The skill's `SKILL.md` routes: a table of "asked to do X" to the branch's `GUIDE.md`. It does not restate a branch.
- A branch is named as a path, `moi-webinar/deck`, and its commands are written in full: `python3 "$SKILLS/moi-webinar/deck/scripts/check-deck.py" ...`.
- Inside a branch, a relative name (`references/x.md`, `scripts/y.py`) is relative to the branch folder.
- A branch inherits its skill's "Before you start" (`$SKILLS`, the operator, `ASK:`), house rules and gates, and restates only what is specific to it. Its first line says which skill it belongs to.
- A branch's script that needs another skill finds it from its own location and from `$SKILLS`, never from the current directory.

| Skill | Branches |
|---|---|
| `moi-devrel` (the main one; it points to every other skill) | `ship`, `design`, `claim-check`, `explain`, `call-digest`, `test-round` |
| `moi-webinar` | `deck`, `community-call` |
| `moi-blog` | `release-pack` |
| `moi-docs` | `geo` |
| `moi-launchpad-ops` | `explorer` |
| `moi-mcp-ops`, `moi-web-products-ops`, `moi-devnet-reset`, `moi-standards-submission`, `moi-education-programs` | none |

## SKILL.md anatomy, in this order

1. **Frontmatter.** `name` (same as the folder) and `description`. The description says what the skill does and when to use it, with the words a person would actually type ("community call", "campfire chat", "monthly call deck"). It is the only thing Claude sees before deciding to load the skill, so be concrete.
2. **What this covers.** Two or three sentences. Then one line on what it does not cover and which skill does.
3. **Before you start.** The inputs needed, as a checklist: what, who provides it, how to ask for it.
4. **The run.** A numbered table: step, what to do, where or the exact command, done when. A newcomer should be able to follow it top to bottom.
5. **Which file to read.** A table mapping "doing X" to the reference file.
6. **Facts that fail silently.** The traps that produce a wrong result with no error. Each one is a real incident, stated as a rule.
7. **Gates.** What must not happen without the human's explicit yes in this conversation.
8. **Keys and access.** Names only. Point to `moi-devrel/references/keys-and-access.md` for where each lives.
9. **Hand-back.** What to give the human at the end: what was produced and where, what remains, and a plain "ready: yes or no, because".

## Rules for content

- **Evidence or nothing.** Every factual statement must be supported by the research notes in `_research/`, by `DEPENDENCIES.md`, or by a file you read yourself. If the evidence is silent, do not guess. Write an `ASK:` line naming who would know.
- **Date volatile facts.** Anything that changes (versions, ids, URLs that are up, who owns what, open pull requests) carries "as of 2026-10-02".
- **No secrets.** Never a key, token, password or seed phrase. Names of variables and where they are stored are fine.
- **No paths from one person's Mac.** Nothing under `/Users/`. Refer to a GitHub repo and a path inside it (`sarvalabs/MOI-Website`, `blog/src/content/posts/`). Anything a skill needs at run time is copied into the skill's own `templates/`, `examples/` or `scripts/`.
- **Do not duplicate another skill or branch.** Point to it. Decks are built by `moi-webinar/deck`. Posts are published by `moi-blog`. Claims are checked by `moi-devrel/claim-check`. House rules live in `moi-devrel`.
- **Real examples beat description.** Where a past run exists, bundle a cleaned copy and say what was good about it.
- **Unknowns are listed, not hidden.** A short "Not yet known" list at the end of the relevant reference file, each with who to ask.

## House rules every skill inherits (from `moi-devrel`)

1. Brief by default. Answer first, then bullets. Long text only for scripts read aloud and for learning documents.
2. Every public claim is checked against MOI source or docs before it goes out. A release note is quoted verbatim.
3. Nothing leaves the machine without an explicit yes: no push, pull request, merge, post, schedule, send or deploy.
4. Work identity only on commits and pull requests. No AI co-author line, no "generated with" footer.
5. Demos and tests use real devnet interactions. Say plainly when something is simulated.
6. Public text has no em dashes, no "not this, not that" constructions, no vague attribution, and reads aloud naturally.
7. Sub-agents only when the human asks for them.

A skill restates one of these only where the task makes it bite.

## Scripts

- Bash that also runs under zsh, or Python 3 with the standard library only. First lines: what it does, usage, exit codes.
- Read-only by default. A script that changes something outside its own output file needs a `--confirm` flag and says what it will do first.
- Never prints a secret. Never calls a service that posts, sends or publishes unless that is its stated purpose and it was confirmed.
- Tested before it ships: run it on a real input and on a bad input. Put the commands you ran in `evals/evals.md`.

## Evals

`evals/evals.md` holds three to six test prompts with the behaviour expected, so a later edit can be checked. Take them from real corrections where you can. Format:

```
### 1. <name>
Prompt: <what a person would type>
Expect: <what a correct response does and does not do>
Why: <the incident or rule behind it>
```

## Done means

- A fresh reader, given only this library, can run the process without asking a question the skill could have answered.
- A fact-checker finds no unsupported claim.
- Every script runs.
- No secret, no `/Users/` path, no em dash in the skill's own text.
