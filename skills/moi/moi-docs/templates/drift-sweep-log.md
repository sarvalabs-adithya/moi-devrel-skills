# Docs drift sweep: FILL-IN date

Repos swept: FILL-IN list, each at its base commit. Triggered by: FILL-IN a merge, a release, a devnet reset, or a calendar date.

## Commands run and results

| Check | Command | Result |
|---|---|---|
| Pages vs the standard | `python3 "$SKILLS/moi-docs/scripts/docs-page-lint.py" docs` | FILL-IN errors, FILL-IN warnings, by rule |
| Build | `npm run build` | FILL-IN |
| Version strings | `grep -rn "FILL-IN old version" docs static src` | FILL-IN hits |
| Dead links | FILL-IN | FILL-IN |
| Live vs docs | `net.Version` and the methods the pages document | FILL-IN |

## Findings

| # | Page | What drifted | Fix | Owner |
|---|---|---|---|---|
| 1 | FILL-IN | FILL-IN | FILL-IN | FILL-IN |

## Not checked

FILL-IN

## Decision

FILL-IN one batch pull request for all fixes, or no change, and who approved it.
