# {{Standard}} review package: start here

Prepared {{date}} for internal review before anything is filed. Everything that goes to an external repository is in this package, one folder per pull request, in filing order. Inside each folder the directory tree mirrors the target repository, so a file at `PR-2-x402-scheme-spec/x402/specs/schemes/exact/scheme_exact_moi.md` lands at `specs/schemes/exact/scheme_exact_moi.md` upstream, and `PR-1-CASA-namespaces-moi/namespaces/moi/caip2.md` lands at `moi/caip2.md`. The first folder inside each PR folder is the repository's name and is not part of the upstream path.

**Process:** nothing is submitted upstream until {{reviewer}} reviews this package and the clearance below is recorded.

## Order
| Order | Folder | Target repo | State on {{date}} |
|---|---|---|---|
| 1 | `PR-1-CASA-namespaces-moi/` | `ChainAgnostic/namespaces` | {{state}} |
| 2 | `PR-2-x402-scheme-spec/` | `x402-foundation/x402` | {{state}} |
| 3 | `PR-3-x402-mechanism-typescript/` | `x402-foundation/x402` | {{state}} |
| 4 | `PR-4-x402-other-sdks/` | `x402-foundation/x402` | {{state, for example recommended skip}} |

Dependencies flow 1, 2, 3: the spec names the namespace, the package implements the spec. The order is enforced upstream, not just preferred.

## Live-state check ({{date}} {{HH:MM}} UTC)
Every line says what was read, from where, and when. Re-run before each share.
| Item | Result | How it was read |
|---|---|---|
| Devnet build (`net.Version`) | {{value}} | {{command, host}} |
| Network ID method | {{method names tried and their answers}} | {{command, host}} |
| Wire field names (`payer` or `fee_payer`) | {{keys}} | {{command, host}} |
| CASA namespace directories, `moi/` present | {{count, true or false}} | census command, `api.github.com` |
| x402 `exact` spec files, MOI present | {{count, true or false}} | census command |
| x402 TypeScript mechanisms, MOI present | {{count, true or false}} | census command |
| Latest `@x402/core`, `js-moi-sdk`, `js-polo` | {{versions}} | npm registry |
| Unit tests | {{count}} | {{command}} |
| Files that name the reference string | {{count}} | `spec-lint.py --stale` |

## What verification covered
{{One paragraph naming the primary sources: package source, upstream repositories, private source read read-only (not cited), the live network, the toolchain. Say which rungs ran, which did not, and what each refuted.}}

## Not run
{{Each item that has not run, for example the live round trip, with who can run it.}}

## Open decisions
{{Numbered list with the owner, from the decisions log.}}

## Background documents (context, not for submission)
{{The plan, the verified findings with their "Checked:" lines, the per-PR requirements.}}

## Clearance
| Reviewer | Scope | Message pasted below | Date |
|---|---|---|---|
| {{name}} | Whole package, version of {{date}} | {{text}} | {{date}} |
| {{name}} | Code of PR 3 | {{text}} | {{date}} |
A later change to a rule, a reference string or a claim reopens the clearance for that change. Send a delta, not a rewrite.
