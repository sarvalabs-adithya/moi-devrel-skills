## What this is

FILL-IN One or two sentences: which pages, on which site, and what they now say.

## Why

FILL-IN The reason, with a source a reviewer can open: a release, a request from a named person, a defect found on a dated read of the live page.

## What changed

- FILL-IN Page, then the change in one line. One line per page.
- FILL-IN Anything in config, scripts or static files. Say "none" if nothing.

## Checked against

- FILL-IN The source for each technical claim, with the ref it was read at (a release tag, a package version, a live read with its date). Public artefacts only in a public repo.
- FILL-IN Claim ledger: kept locally, not in the repo.

## Verification

- FILL-IN `python3 "$SKILLS/moi-docs/scripts/docs-page-lint.py" --added-lines-since origin/main <pages>`: result.
- FILL-IN `npm run build` (or `rm -rf build && make html`): result, and the number of pages.
- FILL-IN Preview link, and the pages opened on it.

## After merge

- [ ] FILL-IN Open the live page and confirm the change is there.
- [ ] FILL-IN Search and AI visibility checks, if config or machine files changed: `geo/GUIDE.md`.

## Review notes

FILL-IN What the reviewer should read and what they can skip (for example: generated files).

## Rebased

FILL-IN The date, the base commit, and "pages diffed against main after the rebase: no content lost".
