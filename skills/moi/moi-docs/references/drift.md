# Drift: pages coupled to a version or an id, and the sweep after upstream merges

Nobody has run this as a routine. Each of the steps below is derived from the September audit and from what was found on 2026-10-03; none is a recorded procedure. Facts are as of 2026-10-03. `$SKILLS`, "the operator" and `ASK:` are defined in `moi-devrel/SKILL.md`. Back to `../SKILL.md`.

## Why pages drift, and what was decided
- Other authors keep merging pages after a sweep, and the sweep's rules decay. On 2026-09-09 the previous operator deliberately removed the CI gate (`docs-geo.yml` with `scripts/lint-docs-geo.mjs`, commit `d0b6a19`) and the weekly health-check cron (`geo-health-check.yml`, commit `77059a7`): "no automated PR policing", "no scheduled monitoring: live-site issues get handled as they surface", "keep regular docusaurus and deal with issues case by case". So the check is by hand, on demand.
- Do not add a CI job, a cron or a scheduled agent for docs without asking. ASK: Rahul. If he wants a routine, the cadence is open (proposal: after each docs merge and at each release).
- `docs-page-lint.py` covers most of what the retired lint checked (description band, quoted colons, version-free titles, one main title, stubs without a mark) and adds names, links, schema calls and Sphinx pages. The retired live check, a curl matrix over the sites, is in the `geo` branch (`geo/GUIDE.md`).

## What is coupled to what
| Changes | Also change | Where | Check |
|---|---|---|---|
| A Coco release | The release section and download links; the version quoted in pages; the skill pointers | coco-docs: `docs/releases/index.md` (a `## vX.Y.Z` section with `<DownloadGrid version="X.Y.Z" />`) and `src/components/DownloadButton/downloads.mjs`, which builds `https://cdn.moi.technology/cocolang/coco-<version>-<os>.tar.gz`; pages that quote the version; `static/.well-known/agent-skills/index.json`. moidocs: `docs/build/skills/coco-skill.md` (three lines) and `static/.well-known/agent-skills/index.json` (`download`) | `grep -rn "<version>" docs static src` in both repos. "0.9.2" appeared in 12 files of coco-docs on the PR branch and 11 on `main` (2026-10-03); the current Coco release is 0.9.3, so grep for the old version too and tell "current version" apart from "added in 0.9.2" notes. Commit `bcbcbf8` did the moidocs half for 0.9.2; moidocs #127 (open, needs review on 2026-10-13) does it for 0.9.3 |
| An SDK release | `version` and `release` in `docs/source/conf.py`; the pages the release changed; after PR #150 the `PAGES` table, `sitemap.xml` and the regenerated llms files; the skill page; `static/downloads/js-moi-sdk-skills.zip` and `docs/build/skills/js-moi-sdk-skill.md` in moidocs | js-moi-sdk (the SDK team edits `docs/` inside the release PR), moidocs | `grep -rn "0\.9\.0" docs`; compare `npm view js-moi-sdk dist-tags` with the page. The Launchpad, Explorer and MCP pin 0.9.0-rc2 while the repo is at 0.9.0-rc3 and npm `latest` is 0.9.0-rc2 (`moi-devrel/references/repo-map.md`) |
| A go-moi release or a devnet change | Constants, field names, method lists and network IDs that pages state | moidocs `json-rpc.md`, tutorials, `learn/fundamentals/*` | Read-only calls to devnet (`net.Version`; the methods a page documents). Source tip is not live (`moi-devrel/references/devnet.md`) |
| A devnet reset | Any id the docs name (asset ids, and a registry id if a page quotes one) and the network ID table in `json-rpc.md` (111, 112, 113) | docs pages | `grep -rn "<old id>" docs static` in all four repos, then any deck or Drive document that quotes it, by hand |
| A new API reference page or skill package | `static/.well-known/api-catalog` or `agent-skills/index.json` | moidocs, voyage-docs, coco-docs | The new page appears in the file. The `geo` branch owns the files |
| A moved page | Redirects, the `.well-known` entries, the `ecosystem` lists in each `llms.config.json`, links on other MOI sites | all | `grep -rn "<old path>" .` and a search of the `sarvalabs` org |
| A new docs site | The `ecosystem` list in every other site's `llms.config.json` | all | `new-site.md` |
`agentInstructions` in each `llms.config.json` tell agents where to verify versions (npm for js-moi-sdk, `/releases/` for Coco). Keep them true.

## The sweep (derived)
Run it from the working copy of one docs repo at a time, on a fresh branch off `main`. A fetch is a download: ask first.
| # | Step | How | Done when |
|---|---|---|---|
| 1 | Update | GATE: `git fetch origin` and `git switch -c docs/drift-<date> origin/main`. Note the commit and the date | You know what you swept |
| 2 | What merged since the last sweep | `git log --since=<last sweep date> --format='%h %an %s' origin/main -- docs`. The authors of the merges are who to ask about a page | A list of pages that changed |
| 3 | Lint what changed | `python3 "$SKILLS/moi-docs/scripts/docs-page-lint.py" --added-lines-since <last sweep commit> <changed pages>`. For the first sweep there is no last commit: use the commit from which you want to look back | Each finding is fixed or listed |
| 4 | Lint the whole tree for the standing list | `python3 "$SKILLS/moi-docs/scripts/docs-page-lint.py" docs`. Most hits are old em dashes, so record the count per rule (command below the table) and compare it with the last log | The counts per rule are in the log |
| 5 | Build | `npm run build` (GATE for `npm install`). Read the warnings (`write-docusaurus.md`) | Exit 0, no `still has a JSX component` |
| 6 | Version greps | The table above, for every release since the last sweep | No stale version left |
| 7 | Live against docs | Read methods only, never an interaction. `net.Version` on devnet, and each read method the changed pages document: `curl -s -X POST https://dev.voyage-rpc.moi.technology/devnet/ -H 'content-type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"net.Version","params":[]}'` | Every documented method answers, or the page says it is not live yet |
| 8 | Dead links | `curl -s -o /dev/null -w "%{http_code}\n" -I <url>` for each external link you touched. A link checker (`linkinator`) found the dead one in September; `npx` downloads it, so ask first | No dead link in the changed pages |
| 9 | Fix in one batch | One branch, one PR for all fixes (2026-09-15 rule). `templates/pr-description.md` | The operator approved the batch |
| 10 | Log | `mkdir -p docs-drift && printf '*\n' > docs-drift/.gitignore`, then `cp "$SKILLS/moi-docs/templates/drift-sweep-log.md" docs-drift/<date>.md`. The log can name people and pages, and js-moi-sdk is public, so it ignores itself | The next sweep starts from it |

Counting findings per rule (step 4), from the repo root:
```
python3 "$SKILLS/moi-docs/scripts/docs-page-lint.py" docs 2>/dev/null | cut -d: -f4 | sort | uniq -c | sort -rn
```

## What the first lint run found (2026-10-03)
Run before the merges, on the PR branches (`geo-fixes`) of moidocs, voyage-docs and coco-docs and the previous operator's local `geo-fixes` of js-moi-sdk. Counts are findings, not pages. The same run reproduces the September audit: five moidocs descriptions outside the band (127, 118, 122, 123 and 68 characters), four newer tutorials without `HowToSchema`, two moidocs pages without `sidebar_position`, six "JS-MOI-SDK" link texts. <!-- slop-lint: ignore -->
| Site | Errors | Warnings | Largest groups |
|---|---|---|---|
| moidocs (42 files) | 185 | 52 | em dash 145; `CoCo` or `CocoLang` 23 (18 in `logics.md`, 5 in `execution-and-fuel.md`); `JS-MOI-SDK` 6; `image` missing or wrong 8 (one a stub); `sidebar_position` missing 2 <!-- slop-lint: ignore --> |
| voyage-docs (8 files) | 26 | 4 | em dash 26; `getting-started.md` opens with a heading and a teaser description |
| coco-docs (48 files) | 89 | 50 | em dash 88; links without a trailing slash 29; `compiler.md` has no `title` |
| js-moi-sdk (10 files) | 22 | 5 | em dash 20; "Voyage devnet" in `agent-skill.rst` (2); sample recovery phrases in `signer.rst` (5, documented samples, confirm) <!-- slop-lint: ignore --> |
Other findings from the same day:
- Before the merges, the same lint on `main` (a checkout that includes `docusaurus.config.js`, so it knows the PR layer is absent) reported 27 coco-docs pages with no `description` and 31 moidocs descriptions outside the band. The PR branches fixed those and #124, #5 and #12 have merged, so run the lint on a fresh `main` and expect lower counts.
- `docs/guard/setup-guardian.md` links `https://moichain-pub.s3.amazonaws.com/genesis.json`, which answered 404 on 2026-09-09 (linkinator), 2026-10-02 and again on 2026-10-03. The right link is unknown. ASK: Gokul.
- moidocs `json-rpc.md` documents `net.NetworkID` with IDs 111 (Local), 112 (Devnet) and 113 (Babylon), added by #126 on 2026-10-01. The live devnet answered error -32601 for the method on 2026-10-03. The label "Babylon" is a contested name (`moi-devrel/references/terminology.md`, Contested 6). ASK: Gokul. <!-- slop-lint: ignore -->
- "Indus TestNet" in `build/index.md` and `pnapi.md`, and "Babylon TestNet" in the Guard pages, name networks the current wording calls devnet or retires. Whether the Guardian pages still describe a live network is unknown. ASK: Gokul. <!-- slop-lint: ignore -->
- `slop-lint.sh` flags the phrase "a specific account based on the provided account" in `json-rpc.md` as `account-centric`: a false hit on plain English. Leave the sentence; the rule's pattern is `account based`. <!-- slop-lint: ignore -->
- `static/downloads/coco-0.8.2-skills.zip` is still in moidocs and stale; the `.well-known` index points at the CDN for 0.9.2 until #127 (open) lands, and the current Coco release is 0.9.3 (`https://cdn.moi.technology/cocolang/coco-0.9.3-skills.zip`). Whether to remove the 0.8.2 zip is open. ASK: Robert Špendl.
- coco-docs has an untracked `static.md` at the repo root left by an old build (previous operator's machine; `.gitignore` does not cover it). Delete it there, never commit it.

## Not yet known
- Whether anyone wants this as a routine, and its cadence. ASK: Rahul.
- Whether #150 (js-moi-sdk) and #127 (moidocs) have merged since 2026-10-13. #124, #5 and #12 had merged by then; the machine layer changes what the build and the lint can check.
- The right replacement for the dead genesis link; whether the four newer moidocs tutorials should get `HowToSchema`, `image` and in-band descriptions now or in a follow-up (the #124 body leaves four such pages "as-is here for a small follow-up"). ASK: Rahul.
