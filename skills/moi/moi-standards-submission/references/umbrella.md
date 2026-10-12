# Umbrella: from "can MOI support this standard" to a merged upstream pull request

Facts are as of 2026-10-03 unless dated. `ASK: <person>` is defined in `moi-devrel/SKILL.md`. Back to `../SKILL.md`.

## What "MOI is x402 compatible" means
x402 is a standard for paying over HTTP: a server answers `402 Payment Required` with a machine-readable price, the client pays, repeats the request with proof in a header and gets the resource. A facilitator is an optional service a seller points at to verify and settle payments; on MOI the seller can read the chain itself, so no third-party facilitator is needed and the facilitator half runs inside the seller's own process, which x402 calls self-facilitation (`x402-compat/x402.md` sections 1 and 2; `FINDINGS.md` 6). x402 v2 names every network by a CAIP-2 identifier (`namespace:reference`), and CAIP-2 identifiers are registered with the Chain Agnostic Standards Alliance (CASA) in a public repository. MOI has no namespace, so `moi:*` cannot be named correctly yet. Three upstream contributions fix that:

| Package folder | Target repo | Adds | Must wait for |
|---|---|---|---|
| `PR-1-CASA-namespaces-moi` | `ChainAgnostic/namespaces` | `moi/README.md`, `moi/caip2.md` at the repo root (the package keeps them under a folder named for the repo: `namespaces/moi/`) | Nothing. An editor reviews the first PR for a new namespace by hand |
| `PR-2-x402-scheme-spec` | `x402-foundation/x402` | `specs/schemes/exact/scheme_exact_moi.md` | May be opened while PR 1 is in review (its text carries a pending-namespace line). Must not merge first |
| `PR-3-x402-mechanism-typescript` | `x402-foundation/x402` | `typescript/packages/mechanisms/moi/` plus e2e catalog and registrations, examples, a changeset, a publish workflow | The spec merged. Upstream reviews the spec before any code |
| `PR-4-x402-other-sdks` | `x402-foundation/x402` | Go and Python mechanisms | Recommended skip: nine of the twelve TypeScript mechanisms (9 Sep) had no Go or Python counterpart. The decision is recorded in `PR-4-x402-other-sdks/STATUS.md` |

Layout trap: inside each PR folder the first directory is the repo's name (`namespaces/`, `x402/`), so `PR-2-x402-scheme-spec/x402/specs/...` lands at `specs/...` in the fork. The package keeps the repo's name as a folder; the fork does not.

Numbering trap: the review package numbers the four submissions 1 to 4 (CASA first). `UPSTREAM.md` numbers only x402's own PRs 1 to 3 (spec, package, other SDKs). Always write the target repo beside a PR number.

## Where the files are (as of 2026-10-03)
Four generations of the same work exist in git and on disk, plus the Drive copies, and the freshest sits only on the previous operator's machine. ASK: Adithya for a copy of the whole folder `x402-compat/`.
| Generation | Where | Holds | Read how |
|---|---|---|---|
| 1. On GitHub | Public `moi-foundation/MOI-Webinars`, branch `claude/agent-payments-simple`, head `3e1d5d8` of 2026-09-10 (not on `main`; no PR is open from it, and PR #1 from the same branch name was merged on 2026-08-06, before any of this work) | `x402.md`, `FINDINGS.md`, `UPSTREAM.md`, `caip2-submission/NOTES.md`, the earlier prototype `moi-x402/`, `review-package/` with PR folders 1 to 4 and its `README.md`, the 9 Sep Word files in `review-package-gdocs/` | GitHub contents API, 2026-10-03 |
| 2. Local commits | Previous operator's machine only (ASK: Adithya for a copy): 4 commits touching `x402-compat/`, all 2026-09-10 (`cd834b3`, `4cebd07`, `540f53b`, `03720c3`) | The rebuilt spec (upfront as a choice, claim bound to the network, identifier layout, RPC field names), the chain reader, `keyId` enforced, 28 unit tests (17 facilitator and 11 reader at the local head, counted 2026-10-03; the 8 server tests that make 36 are untracked) | `git log origin/claude/agent-payments-simple..HEAD` |
| 3. Uncommitted | Same machine: 17 tracked files edited 2026-09-10 after the last commit (spec, PR 2 and 3 descriptions, package source, `STATUS.md`, publish workflow, changeset moved to `typescript/.changeset/`) and 4 PR 1 files edited 2026-10-01 (terminology corrections) | The newest text | `git status`, file dates |
| 4. Untracked | Same machine: `AUDIT-2026-09-10.md`, `FUTURE.md`, `ESCROW-RESEARCH-2026-09-10.md`, `BLOG-x402-on-moi.md`, `escrow-poc/`, `PR-3.../E2E-REGISTRATION.md`, `server.test.ts`, `docs/` (three review documents as `.md`, `.docx`, `.pdf`, written 2026-09-10, and `PR-1-chain-id-edits.md` of 2026-09-14) | Audit, follow-ups, the reviewer-facing documents | `git status -uall` | <!-- slop-lint: ignore -->
| Drive | Several generations from 9 to 14 Sep: a set of Google Docs of 9 Sep, three review documents of 10 Sep, a folder named `x402` holding the three `.docx` of 10 Sep, and a Google Doc of 14 Sep for PR 1 ("participant-centric + governance"). No link is recorded in this library; the previous operator holds them | Mostly older snapshots, but the 14 Sep PR 1 document may hold wording that exists nowhere on disk: read it before assuming the local 1 Oct edits are the newest | ASK: Adithya for the folder link; see `review-gate.md` |

`FIX-PLAN.md` (items D1 and D2, and "New decisions" 1) and `DEPENDENCIES.md` (its MOI-Webinars section) are also local to that machine; ASK: Adithya for a copy. The pushed branch is public, so the package already shows reviewer names there, and the newest files cite private source: do not push them (`traps.md` 6).

## State of the filing (read 2026-10-03)
Nothing was filed upstream. Evidence: `ChainAgnostic/namespaces` has 49 namespace directories and no `moi/`; `x402-foundation/x402` has 18 files in `specs/schemes/exact/` (the overview and 17 networks) and 13 TypeScript mechanism directories, none for MOI; a GitHub search for "moi" in titles returns 0 in both repos; `@x402/moi` is not on npm (404). Every PR description in the package still carries unchecked boxes, and the CASA PR number is `TODO` in the namespace file and in the spec description. <!-- slop-lint: ignore -->

## The seven stages
| # | Stage | Done when |
|---|---|---|
| 1 | Research upstream and record what is true: `FINDINGS.md` is the model, each finding ends "Checked: <how>" | Every finding names its check and its date |
| 2 | Decide what identifies a MOI network (`open-decisions.md` 1 and 2) | The reference string and the RPC that returns it are written down by the people who decide |
| 3 | Draft each artefact in its PR folder. The inner tree mirrors the target repo path for path | `mirror` check in `review-gate.md` passes |
| 4 | Verification passes until nothing is refuted (`verification.md`) | Every claim has a named check; the unrun items are stated |
| 5 | Wording pass (`wording.md`) | `spec-lint.py` 0 errors, `slop-lint.sh` 0 errors, warnings read |
| 6 | Internal gate (`review-gate.md`) | The reviewer's clearance is on record |
| 7 | File in order, answer upstream, then list, publish and announce | CASA merged, spec merged, package merged and published |
The plan is a sequence of steps, each with "Needs" and "Done when", not a list of problems (`x402.md` section 3). Keep it that way.

## Upstream rules for every x402 PR (read first-hand 2026-10-03)
Source: `CONTRIBUTING.md`, `specs/CONTRIBUTING.md`, `typescript/CONTRIBUTING.md` and `.github/pull_request_template.md` of `x402-foundation/x402`, read by public GET. Re-read them before filing: they change. Print them to the terminal and do not save them (saving a file is a download). Host `raw.githubusercontent.com`; add the path after `.../main/`:
```
curl -sS -m 25 "https://raw.githubusercontent.com/x402-foundation/x402/main/CONTRIBUTING.md"
```
Paths to read in `x402-foundation/x402`: `CONTRIBUTING.md`, `specs/CONTRIBUTING.md`, `typescript/CONTRIBUTING.md`, `.github/pull_request_template.md`, `specs/scheme_impl_template.md`, `e2e/README.md`, `docs/core-concepts/network-and-token-support.mdx`. In `ChainAgnostic/namespaces`: `CONTRIBUTING.md`, `_template/README.md`, `_template/caip2.md`. For CAIP-2 and CAIP-104 the repo is `ChainAgnostic/CAIPs`, path `CAIPs/caip-2.md` and `CAIPs/caip-104.md`.

| Rule | What the text says |
|---|---|
| Signed commits | "All commits must be signed"; it shows `git config --global commit.gpgsign true`. The PR template says signing is required for merge. A key is not configured (`moi-devrel/references/keys-and-access.md`). GATE: the operator changes git configuration, not Claude |
| AI-assisted contributions | Acceptable if you review the output before requesting review, strip verbosity, verify payment and signature logic yourself, do not batch-generate PRs, and "disclose significant AI usage" in the PR description when most of a PR was AI-generated. Unreviewed AI output "may be closed without detailed review". How MOI words the disclosure is open: `open-decisions.md` 8 |
| PR text | "Fill out the PR template completely": headings Description, Tests, Checklist (four boxes). The drafts in the package do not use these headings; `spec-lint.py` reports it |
| Conventional commits | The sample AI prompt asks for `feat:`, `fix:`, `docs:`, `chore:` and a subject under 72 characters. Merged spec PRs are titled `specs(exact): propose Starknet exact scheme for x402 v2 (spec-only)` (#2849), `Specs(exact): propose Canton exact scheme for x402 (spec-only)` (#2634) and `docs(specs): add exact scheme spec for Casper Network` (#2741), read 2026-10-03 |
| Proposal first | `specs/CONTRIBUTING.md` step 1: open an issue or discussion with the problem, the approach and why existing schemes do not suffice, before writing a spec. `x402-foundation/x402` has Issues on and Discussions off (read 2026-10-03), so it is an issue; the main `CONTRIBUTING.md` says issues are for bug reports and concrete feature proposals and questions go to the x402 Slack. The package has no such draft: `open-decisions.md` 13. The Canton spec PR (#2634, merged 2026-08-07) says "Closes #2632", an issue opened first |
| Changelog | A Changesets file under `typescript/.changeset/*.md` for user-facing changes (`pnpm -C typescript changeset`) |
| New chain | PR 1 spec only; PR 2 one SDK; PR 3 other SDKs. "Do not modify core packages". The foundation "will re-audit" a scheme whose mechanism differs from the reference |

## Upstream census: recount, do not trust the old numbers
Plain GET requests with no login, so nothing shows in anyone's activity feed (`moi-devrel/references/consent-and-identity.md` 1.6). The host called is `api.github.com`. The unauthenticated limit is 60 requests an hour, shared by every command in this skill.
```
curl -sS -m 25 https://api.github.com/repos/ChainAgnostic/namespaces/contents/ | python3 -c 'import json,sys; d=json.load(sys.stdin); n=[x["name"] for x in d if x["type"]=="dir" and x["name"][0] not in "_." and x["name"]!="assets"]; print(len(n), "moi" in n)'
curl -sS -m 25 https://api.github.com/repos/x402-foundation/x402/contents/specs/schemes/exact | python3 -c 'import json,sys; n=[x["name"] for x in json.load(sys.stdin)]; print(len(n), any("moi" in x for x in n))'
curl -sS -m 25 https://api.github.com/repos/x402-foundation/x402/contents/typescript/packages/mechanisms | python3 -c 'import json,sys; n=[x["name"] for x in json.load(sys.stdin)]; print(len(n), "moi" in n)'
curl -sS -m 25 "https://api.github.com/search/issues?q=repo:ChainAgnostic/namespaces+moi+in:title" | python3 -c 'import json,sys; print(json.load(sys.stdin)["total_count"])'
curl -sS -m 25 "https://api.github.com/search/issues?q=repo:x402-foundation/x402+moi+in:title" | python3 -c 'import json,sys; print(json.load(sys.stdin)["total_count"])'
```
The five answers on 2026-10-03: `49 False`, `18 False`, `13 False`, `0`, `0`. If a command prints a rate-limit message instead, the one-liner fails with a key error: wait and run it again.

| Count | 2026-09-09 (package) | 2026-10-03 (read) | Why it drifted or was wrong |
|---|---|---|---|
| CASA namespaces | "55", then "50", then 49 | 49 | Today's contents listing has 55 directories; six are not namespaces (`.github`, `_data`, `_includes`, `_layouts`, `_template`, `assets`). The earlier 55 is probably that count (inferred). Corrected in `269ab19`, `265a858` |
| x402 `exact` specs | 17 | 18 files (overview plus 17 networks) | Say what you counted |
| x402 TypeScript mechanisms | 12 | 13 (`casper` added) | Upstream moves |
CASA review odds were 91 of the last 100 closed PRs merged, median 24 days to merge, six days for Hive, 30 for Neo, 33 for BSV, 40 for Aptos, 48 for Flow (`FINDINGS.md` 8, 9 Sep). Of the nine unmerged, eight were duplicates, drafts or stray files; one real chain failed because its author stopped replying for 587 days. Recount before quoting.

## Filing mechanics (fork, identity, signing, push)
`moi-devrel/ship` owns commits and pull requests in general (`moi-devrel/ship/references/pull-request.md`, whose section 6 sends you back here for the steps below); these upstreams need the extra steps below. Each GATE needs the operator's yes that names it. Both upstream default branches are `main` (read 2026-10-03).
| # | Step | Command or action | Done when |
|---|---|---|---|
| 1 | GATE: fork | In the browser under the work account, or `gh repo fork ChainAgnostic/namespaces --default-branch-only` (the same for `x402-foundation/x402`) after `gh auth status` shows the work login. Forking creates a repository under that account | The fork exists under the work account |
| 2 | GATE: clone the fork | `git clone` of the fork into a folder outside `$HOME/x402-review`. A clone is a download | A clean working copy |
| 3 | Identity | In the clone: `bash "$SKILLS/moi-devrel/scripts/preflight.sh"`. Fix every FAIL | Work name, work address, work login |
| 4 | Branch | `git switch --no-track -c <topic> origin/main` (the branch step of `moi-devrel/ship`; `--no-track` leaves the branch with no upstream, so nothing can push it to `main` by accident) | Clean tree on a topic branch |
| 5 | Copy the files | Drop the package's inner tree minus its first folder onto the clone: for CASA `namespaces/moi/*.md` into `moi/`; for the spec the contents of `x402/` into the clone root | `git status` lists only the intended paths |
| 6 | GATE: signing | Upstream asks for signed commits and shows `git config --global commit.gpgsign true`. That line changes every repository on the machine; run it without `--global` inside the clone to change this one (a safer variant with the same effect there; inference). The signing key is the operator's to create and register with GitHub. ASK: Rahul which kind | `git log -1 --show-signature` shows a good signature, and GitHub marks the pushed commit Verified |
| 7 | Commit | Conventional subject of 72 characters or fewer, no `Co-Authored-By`, no "generated with" footer (`moi-devrel/ship`; the upstream disclosure is `open-decisions.md` B) | `git log -1 --format=%B` is clean |
| 8 | GATE: push and open the PR | The push gate and the pull request steps of `moi-devrel/ship`. For a fork the head is `<fork owner>:<branch>` and the base repo is the upstream | PR URL read back: base, head, author, files |
`ChainAgnostic/namespaces` has Discussions on (read 2026-10-03), so a discussion there could serve as the `discussions-to` URL; creating one is a post (GATE).

## Listing and publishing after the package merges
Docs entries for other chains arrived as small separate pull requests in at least two cases: #3578 "docs: link the merged Bitcoin Lightning exact spec" (merged 2026-09-27) touched `docs/schemes/exact.mdx` and `docs/schemes/overview.mdx`, and #3484 (opened by a bot, merged 2026-09-15) added Casper setup docs to `docs/schemes/exact.mdx`. `docs/core-concepts/network-and-token-support.mdx` carries the network identifiers and a table of supported tokens (read 2026-10-03), and the main `CONTRIBUTING.md` says the Gitdocs in `docs/` are updated automatically by Mintlify. Whether MOI adds its own entries in the package PR or in a follow-up is not recorded. Ask the maintainers in the proposal issue; ASK: Rahul. Publishing `@x402/moi` runs a workflow in the upstream repository (`x402-mechanism.md`).

## Timeline observed
Research 26 to 31 Aug 2026; the internal gate was set on the 9 Sep call; the package was assembled 9 Sep; the spec and package were rebuilt and audited 9 to 10 Sep; the numeric-ID edit set was written 14 Sep; terminology corrections to PR 1 were made 1 Oct. About five weeks, no filing. The blocker throughout is the network ID, not drafting.

## Not yet known
- Whether the reviewer cleared the package and which Drive generation was read. ASK: Rahul.
- Who files, from which account, with which signing key, and who watches `discussions-to`. ASK: Rahul.
- Whether the numeric-ID edit set of 14 Sep was accepted. ASK: Rahul.
