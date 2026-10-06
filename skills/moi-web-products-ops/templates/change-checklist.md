# Change checklist: <product>: <one-line change>

Two parts. Part A can go in a pull request body. Part B is the operator record: it names people, accounts and gate answers, and the website and Dataroom repos are public, so it never goes in a pull request, a commit or a public repo. Keep it outside the working copy, or make a self-ignoring folder inside it:
`mkdir -p web-ops-<slug> && printf '*\n' > web-ops-<slug>/.gitignore` (the `*` hides the folder, itself included, from `git add`).
Fill every `<...>`. Delete the lines for the other two products. No AI co-author line and no "generated with" footer. Never write a secret value, a key or a recovery phrase in either part.

# Part A: for the pull request body

## What and why
- Product and deploy branch: website `main` | Dataroom `main` | Points `feature/ci-cd`
- Change: <one sentence>
- Why: <the reason, with a date or an issue number>
- Files: <list>

## Checks run, because CI will not
- [ ] Website: `npm run lint`, `npm run build`, and `npm run build --prefix blog` if a post or the blog changed. Preview read on desktop and phone: <two URLs>
- [ ] Dataroom: `npx tsc --noEmit`, `npm run lint`, `npm run build` in `moi-data-room/`
- [ ] Points: `pnpm run ci` (lint with zero warnings, typecheck, tests, `pnpm check:migrations`)
- [ ] `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" <changed text files>` has no error
- [ ] `bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" <changed paths>` has no finding (a backstop, not proof)

## After the deploy
- Deploy run: <`gh run list` line, with its conclusion>
- Seen live: <URL> <what you saw, read from the data, not the status code>

# Part B: operator record (never in a public repo)

## Before
- `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" <product>` saved at <path>, taken <UTC time>
- KNOWN lines present before: <ids>
- Security: if the change touches a product's admin, the operator confirmed the handover note was read: <yes, date | not applicable>
- `bash "$SKILLS/moi-devrel/scripts/preflight.sh"` has no FAIL: <yes>

## Order of work
- [ ] Database change first? <none | yes: file, run by whom before the merge (Points: `applied` one above `expected`, healthy), then `applied` equals `expected` after the deploy>
- [ ] New secret or variable listed in the workflow? <none | yes: name, set by the operator, deploy run>
- [ ] Anything on the VM? <none | request R-number from `references/who-to-ask.md`, sent by the operator>

## Gates
| Gate | Asked in this shape | The operator's yes (quote) |
|---|---|---|
| Push and open the PR | "Ready to push `<branch>` (files) to origin as `<login>`. Yes?" | |
| Merge | "Merge `<PR>` into `<branch>`. This deploys <product>. Yes?" | |
| Manual deploy run | "Run `<workflow>` on `<branch>`. Yes?" | |
| Production database write | "Run `<file>` in the SQL editor of `<project>`. Yes?" | |
| Admin write | "Use the `<product>` admin to <action>. Yes?" | |
| Secret or variable | "Set `<NAME>` in `<repo>`; you type the value. Yes?" | |
| Spend | "Ask the chat one question, a few tokens. Yes?" | |

## After
- `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" <product>` taken <UTC time>: new FAIL <none | list>, KNOWN changed <none | list>

## Rollback
- <website and Dataroom: revert the merge in a new PR, which deploys. Points: revert on `feature/ci-cd`, which deploys; no older image is pulled at the tip>
- A database change: <how it is undone, or "cannot be undone, copy taken at <where>">

## Hand-back
```
Product and job: <...>
Produced: <what, with the URL or path>
Health: before <KNOWN ids, FAIL count> / after <...>
Remaining: <numbered, each with an owner>
Not verified or simulated: <say so, or none>
Ready: yes or no, because <one reason>
```
