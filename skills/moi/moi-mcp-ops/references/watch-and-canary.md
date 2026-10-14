# The upstream watch and the chain canary

Two scheduled workflows in `sarvalabs/moi-mcp` open GitHub issues when something outside this repo moves. A person has to read those issues: nothing merges or deploys on its own. Facts are as of 2026-10-03 (public GitHub reads, workflow files at `master`) unless dated. Back to `../SKILL.md`.

## What the two checks are

| | Upstream watch | Chain canary |
|---|---|---|
| File | `.github/workflows/upstream-watch.yml`, `scripts/upstream-watch.mjs` | `.github/workflows/chain-canary.yml`, `test/e2e/chain-canary.test.ts` |
| Schedule | Daily at 03:17 UTC (08:47 IST). Manual run takes a `dry_run` input | Nightly at 02:43 UTC (08:13 IST). Manual run allowed |
| Asks | Did js-moi-sdk, go-moi or cocolang publish a release? | Does the live devnet still accept what this server builds? |
| Opens | An issue titled `Upstream release: <name> <tag>`, label `upstream-release`, one per release. The same title, open or closed, is never filed twice | One issue titled `Chain canary failing`, label `chain-canary`, or a comment on the one already open. The first green run closes it with "Canary green again" |
| Needs | `UPSTREAM_READ_TOKEN` (fine-grained, read-only Contents on go-moi and cocolang, both private). Without it those two are skipped with a log warning and the run stays green | Nothing secret. It only simulates: nothing is signed or sent and no fuel is spent |
| Real start times | 03:34 to 03:43 UTC on 2026-10-01 to 03 | 02:55 to 03:03 UTC on the same days (both start late) |

Dependabot (`.github/dependabot.yml`) is the third watcher: npm daily (up to 5 PRs, the `js-moi-*` and `js-polo` packages in one group, everything else in another) and Actions weekly. Nothing merges automatically, because an SDK change can change what a user signs.

## What each check cannot see (read this before trusting a green run)
- The canary tests the code at `master` against live devnet. It does not touch the hosted server, the registry, OAuth or a phone. The canary ran green on 2026-10-01 to 03, and `moi_resolve_agent` failed on every host when read on 2026-10-02 and 2026-10-03. Green canary does not mean the connector works.
- The watch lists GitHub **releases**, not tags, and only the newest one per upstream. Two releases between runs file one issue. A repo that publishes tags without a Release is invisible to it.
- As of 2026-10-03 the only `upstream-release` issue ever filed is #17 (js-moi-sdk v0.9.0-rc3, open since 2026-09-23). No go-moi or cocolang issue exists, although go-moi v0.13.0 was tagged on 2026-09-10 and `moi-devrel/references/devnet.md` lists that issue as the first sign of a reset. `UPSTREAM_READ_TOKEN` was not set on `sarvalabs/moi-mcp` as of 2026-10-10 (`project-handover-docs/MCP-SERVER.md`), so the watch has never been able to read those two private repos; Rahul decides which account owns the token. Whether those repos also publish no GitHub Releases is unknown: steps 3 to 5 of the first runbook below find out. ASK: Rahul (token), Gokul (releases).
- No `chain-canary` issue has ever been opened. That is expected while the checks pass. It also means the issue path has not run in anger.
- The canary's header comment says a receipt that would revert counts as a pass. The code beneath it asserts receipt status 0 for the three simulations. Trust the code.

## Runbook: check that the watch is really watching

| # | Step | Do this | Done when | Gate |
|---|---|---|---|---|
| 1 | Recent runs | `bash "$SKILLS/moi-mcp-ops/scripts/mcp-health.sh" --github --no-rpc`, or `gh run list -R sarvalabs/moi-mcp --limit 8` | Both scheduled runs green in the last day | read |
| 2 | Open issues | `gh issue list -R sarvalabs/moi-mcp --label upstream-release --state open` and the same with `--label chain-canary` | You know what is waiting | read |
| 3 | Does the secret exist | `gh secret list -R sarvalabs/moi-mcp` lists names and dates only, and needs access to the repo's Actions secrets (a repo admin: ASK: Rahul). `UPSTREAM_READ_TOKEN` should appear. A value is never shown | Present or absent | read |
| 4 | Can the private repos be seen | `gh release list -R sarvalabs/go-moi --limit 3` and the same for `cocolang` (needs read access to both: ASK: Rahul who grants it). Empty means the watch can never fire for that repo | You know whether Releases exist | read |
| 5 | What does the watch say | Prefer the log of a recent scheduled run in the Actions tab. To run one: `gh workflow run upstream-watch.yml -R sarvalabs/moi-mcp -f dry_run=true`, then read the log. "skip go-moi: private repo and UPSTREAM_READ_TOKEN is not set" means the secret is missing; "would file: ..." means it works and nothing is filed | The sentence from the log | GATE (a manual workflow run) |
| 6 | Report | One message to Rahul (who owns the token) and Gokul (Releases), drafted by Claude and sent by the operator | Sent | GATE |

## Runbook: an `Upstream release` issue
Read the issue body first: it names the release, whether this repo's pin differs (`js-moi-sdk` is pinned exactly, `0.9.0-rc2` on 2026-10-03), whether the version is on npm, and a "What to check" list.

| # | Upstream | Do this | Done when | Gate |
|---|---|---|---|---|
| 1 | All | `gh issue view <N> -R sarvalabs/moi-mcp` | You can say which upstream and which tag | read |
| 2 | js-moi-sdk | Is it on npm? `npm view js-moi-sdk dist-tags`. rc3 was a GitHub release only and the newest version on npm was 0.9.0-rc2 on 2026-10-03, so Dependabot cannot offer it. Read the release notes for changes to participants, asset ids, amount scaling and the interaction shape: those change what a user signs. Whether to install an rc from GitHub: ASK: Gokul | A decision: wait for npm, or plan the bump | read |
| 3 | js-moi-sdk, on npm | Review the grouped Dependabot PR (all `js-moi-*` and `js-polo` move together). Never merge it unread (a merge is a GATE). Run the canary by hand (below; the install it needs is a download, GATE) | CI green, canary green, release notes read | GATE for the install and any merge, else local |
| 4 | go-moi | Nothing changes in this repo, but validation rules may. Read the release note (ASK: Gokul where it is), run the canary (step 3 of the canary runbook below), then ask the protocol team when devnet picks the version up. The canary fails on the first night something breaks. A go-moi release can precede a devnet reset: hand to `moi-devnet-reset` | Canary result and a question to Gokul drafted | local, then GATE to send |
| 5 | cocolang | Release notes for manifest or calldata encoding changes: `moi_get_logic` reads manifests Coco produces and `moi_call_logic` encodes calls against them | Notes read, a verdict written in the issue | read |
| 6 | Close | Comment what you checked and close: "Checked <date>: <what>, <result>." The issue says to close it once the release is checked | Closed | GATE (a public comment) |

## Runbook: a `Chain canary failing` issue

| # | Step | Do this | Done when | Gate |
|---|---|---|---|---|
| 1 | Read the issue | `gh issue view <N> -R sarvalabs/moi-mcp`: run link, failing lines, usual causes (a go-moi upgrade on devnet, or a js-moi-sdk release not yet taken) | The failing check is named | read |
| 2 | Confirm from outside | `bash "$SKILLS/moi-mcp-ops/scripts/mcp-health.sh" --no-read` and the RPC line. If `net.Version` changed, a node upgrade happened | You know if the chain moved | read |
| 3 | Reproduce | In a working copy of `sarvalabs/moi-mcp`, after `npm ci` (a download: GATE, wording in `ship-a-change.md` step 3): `MOI_E2E=1 npx vitest run test/e2e/chain-canary.test.ts`. It sends read requests and simulates; nothing is signed or spent | The same check fails | GATE for the install, then local |
| 4 | Map the failure | Table below | A cause and a fix | read |
| 5 | Fix | A branch, a test, a PR to `master`: `ship-a-change.md` part A. Production changes only after the sync and deploy | PR merged | GATE |
| 6 | Let it close | The next green nightly run closes the issue by itself. Do not close it by hand unless you are also fixing it | Issue closed by the bot | read |

A failing check, its likely cause, and the fix (check names are the test titles in `chain-canary.test.ts`):

| Check that failed | Likely cause | Fix |
|---|---|---|
| The RPC endpoint answers | Endpoint or path moved, node down | Check the RPC line of the script, ASK: Gokul |
| KMOI exists at the id this SDK carries | KMOI's asset id moved and the SDK constant is old | Upgrade the SDK packages together; ids come from the SDK, never a literal |
| Every asset standard is one this SDK can name | The chain grew a standard (KMOI becoming MASN looked like this) | SDK upgrade |
| Decimals and scaling | A field changed meaning (`dimension` was split in two at v0.13.0) | Fix the read and the scaling |
| Storage fund this server picks still creates an asset | Storage was repriced; the default fund became too small | Fix the fund choice (`chooseStorageFund`) |
| The floor is still enough | `MIN_STORAGE_FUND` (7 KMOI on master) is stale | Raise it, with a test |
| The transfer would succeed | Fuel price floor or a participant rule changed | Take the price from the SDK |
| Any check, after a devnet reset | KMOI's creator account, which the canary uses as sender, no longer exists | Set `MOI_CANARY_ACCOUNT`. **The nightly workflow does not pass it**, so this needs a workflow edit or a new code default (a PR) |

## Not yet known
- Which account will own `UPSTREAM_READ_TOKEN` (not set as of 2026-10-10). Rahul decides.
- Whether go-moi and cocolang publish GitHub Releases. ASK: Gokul.
- Who is subscribed to `moi-mcp` issues. A 10-day-old issue (#17) is open with no comment on 2026-10-03.
- Dependabot: #25 was closed 2026-10-05 and #26 on 2026-10-12. Its replacement #28 bumps majors (zod 4, TypeScript 7, vitest 5, @types/node 26) and fails the build, because zod 4 breaks the types in `src/dapp`, `src/launchpad` and `src/wc`. Do not merge it as is: split the majors out or ignore them in `dependabot.yml` (a PR: GATE).
