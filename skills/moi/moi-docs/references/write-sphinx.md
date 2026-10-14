# Write a page on the js-moi-sdk docs (Sphinx)

For js-moi-sdk.docs.moi.technology, the folder `docs/` of `sarvalabs/js-moi-sdk` (public). Facts are as of 2026-10-03. The page rules are in `page-standard.md` (rule R12 and the lint's `rst-*` and `sdk-*` rules). Run every command from the working copy of `sarvalabs/js-moi-sdk`. `$SKILLS`, "the operator" and `ASK:` are defined in `moi-devrel/SKILL.md`. Back to `../SKILL.md`.

## Know which state the repo is in
- On `main` as of 2026-10-03 (still true on 2026-10-13, because #150 is open) `docs/` holds `Makefile`, `source/conf.py`, ten `.rst` pages and a stylesheet and favicon. There is no `generate_llms.py`, no `source/_extra/` and no `_templates/layout.html`. Adding a page there is two steps: write the `.rst`, add it to the toctree.
- PR #150 (from the previous DevRel's fork, sarvalabs-adithya; open as of 2026-10-13) adds the search and AI layer: `docs/generate_llms.py`, `docs/source/_extra/` (robots, sitemap, llms files, a markdown copy of every page, a 404 page, the IndexNow key file), `docs/source/_templates/layout.html` and a `make llms` target. About 22,000 of its lines are generated files. After it merges, a new page is five steps (below).
- Check which state you are in before you start: `git ls-tree origin/main docs/generate_llms.py` (after the operator agreed to a fetch). Empty output means #150 has not merged.
- The SDK team updates the docs inside each release pull request (#133, #136, #143 and #148 touched `docs/`, read from `git log`). Pages written between releases are DevRel's. Reviewers: `CODEOWNERS` names `@sarvalabs-gokul` and `@sarvalabs-manish` for every file. ASK: Gokul for the build and deploy route, which no workflow in the repo shows.

## Set up once
1. GATE: install the toolchain, which downloads packages: Python with `sphinx`, `sphinx_js`, `sphinx_rtd_theme` and `sphinx-autobuild` (the `watch` target), and `jsdoc` from npm. No requirements file is committed and no version is pinned. ASK: Gokul for the versions that work.
2. GATE: at the repo root, `npm install` and `npm run build`. `conf.py` reads `packages/*/lib.cjs`, so the packages must be built before the API pages render (inferred from `conf.py`). `npm run build` first deletes every `lib.cjs` and `lib.esm` folder (`prebuild` runs `clean`).
3. `bash "$SKILLS/moi-devrel/scripts/preflight.sh"` for the identity.

## The steps
| # | Step | Command or action | Done when |
|---|---|---|---|
| 1 | Branch | `git switch -c docs/<short-name> origin/main`. Fork or org: ASK: Rahul | A branch off `main` exists |
| 2 | Copy the template | `cp "$SKILLS/moi-docs/templates/page-sphinx.rst" docs/source/<page>.rst` | A file with every blank marked `FILL-IN` <!-- slop-lint:ignore --> |
| 3 | Write the page | The first lines are the `.. meta::` block with `:description:`: plain text, 140 to 160 characters, a colon needs no quotes. Then the title with an overline and underline at least as long as the title, then the opening paragraph that says what the thing is. API blocks come from source comments through `sphinx_js`, so to change an API section edit the comment in the package source, not the `.rst` | No `FILL-IN` left <!-- slop-lint:ignore --> |
| 4 | Add to the toctree | Add the page name without `.rst` to the `toctree` in `docs/source/index.rst`. A page left out builds but nothing links to it | The lint's `toctree-missing` is quiet |
| 5 | After #150 only: the PAGES row | In `docs/generate_llms.py` add `"<page>": ("Title", "same description")` to `PAGES`. The file's own comment says the table "is checked by eye in PR review". Description, `PAGES` row and sitemap line are three copies that nothing keeps in step | The lint's `sdk-pages-*` rules are quiet |
| 6 | After #150 only: generate | From `docs/`, `make llms`. It runs `python3 generate_llms.py`: a Sphinx text build into a temporary folder, then `llms.txt`, `llms-full.txt`, `index.md`, `<page>.md` and `<page>/index.md` in `source/_extra/`. Run `git status` and commit them all: on this site the generated files are committed. Never edit one by hand | `git status` shows the regenerated files |
| 7 | After #150 only: the sitemap | Add `<url><loc>https://js-moi-sdk.docs.moi.technology/<page></loc></url>` to `docs/source/_extra/sitemap.xml` by hand, with no `.html`. Nothing generates it on this site | The lint's `sdk-sitemap-missing` is quiet |
| 8 | Lint | `python3 "$SKILLS/moi-docs/scripts/docs-page-lint.py" docs/source/<page>.rst` (add `--added-lines-since origin/main` on an existing page) | 0 errors, every warning read |
| 9 | Clean build | From `docs/` (check that `pwd` ends in `/docs` first, because the command deletes `./build`): `rm -rf build && make html`. The clean build matters: without it the navigation of other pages does not pick up the new page. Pages land in `docs/build/html/<page>.html`. Open `build/html/index.html` and confirm the page is in the navigation | The page is in the navigation and the build printed no warning about it |
| 10 | Check the head (after #150) | `grep -o '<title[^>]*>[^<]*' build/html/<page>.html`, `grep -o 'content="[^"]*" name="description"' build/html/<page>.html`, `grep -o 'rel="canonical" href="[^"]*"' build/html/<page>.html` | Title, description and a canonical without `.html` |
| 11 | Claims and phrasing | From the repo root: `mkdir -p claim-check-<slug> && printf '*\n' > claim-check-<slug>/.gitignore`, then `python3 "$SKILLS/moi-devrel/claim-check/scripts/extract-claims.py" --all docs/source/<page>.rst > claim-check-<slug>/claims-candidates.csv && cp -n claim-check-<slug>/claims-candidates.csv claim-check-<slug>/ledger.csv` (keep `claims-candidates.csv` untouched; `moi-devrel/claim-check` step 8 needs it for `--dropped`). Give every row a verdict (`moi-devrel/claim-check`), then `python3 "$SKILLS/moi-devrel/claim-check/scripts/ledger-status.py" claim-check-<slug>/ledger.csv` and `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" docs/source/<page>.rst` | The status script exits 0 (the folder ignores itself, so the ledger stays out of this public repo), lint 0 errors |
| 12 | Commit and PR | After the operator's yes: `moi-devrel/ship`. Review the script and the `PAGES` change, not the generated files | PR open with Gokul requested |
| 13 | After merge | Open the live page. Then `curl -sI https://js-moi-sdk.docs.moi.technology/nonexistent-page` should answer 404 once the 404 page is deployed, and `curl -s -o /dev/null -w "%{http_code} %{content_type}\n" https://js-moi-sdk.docs.moi.technology/robots.txt` should answer `200 text/plain`. The host answered `200 text/html` for both on 2026-10-03, which is the soft-200 fallback. Full checks: `geo/GUIDE.md` | The live page shows the change |

## Rules that bite on this site
- Keep an old anchor when you reword a heading by putting a target above it: `.. _installing:` then `How do I install js-moi-sdk?` with an underline as long as the title. The old anchor is the old heading in lowercase with hyphens.
- Do not set `html_baseurl` in `conf.py`: it adds `.html` to every address and points each canonical at a redirect. The base address lives in `_templates/layout.html`. The page title (`html_title`) is version free on purpose.
- `docs/source/conf.py` carries `version` and `release` (`v0.9.0-rc3`). They move at each SDK release; the SDK team changes them. A page that names a version quotes it as tagged, with the `-rc` suffix. A release candidate is not shipped: the npm `latest` tag of `js-moi-sdk` is 0.9.0-rc2 and rc3 exists on GitHub only (2026-10-13). <!-- slop-lint: ignore -->
- The agent-skill page says the skill targets the current SDK, while the skill itself says it was checked against 0.7.1 (the SDK docs build and this claim are not recorded in the handover docs; `project-handover-docs/AGENT-SKILLS.md` has the skill stamps). Do not repeat either claim until Gokul says which is true.
- Sphinx pages carry the same naming and wording rules. The lint and `slop-lint.sh` read `.rst`. The `agent-skill` page still says "Voyage devnet" in its body, and on the PR branch also in its description (read 2026-10-03); the right word is "devnet". <!-- slop-lint: ignore -->
- A page in `source/_extra/` is generated. Fix its source page and run `make llms`.

## Not yet known
- How the site is built and published after a merge, how a change is previewed, and whether the generated files should stay committed (moving to a build step, as the other sites did, is an option; the SDK docs build is not recorded in the handover docs). ASK: Gokul.
- Which Python and Node versions build the docs. ASK: Gokul.
- Whether PR #150 has merged since 2026-10-13, when it was open. Read it before you start.
