# Templates

Copy one, fill it in, then run the lint (`python3 "$SKILLS/moi-docs/scripts/docs-page-lint.py" <page>`). Every blank is marked `FILL-IN`, and the lint reports a leftover `FILL-IN` as an error, so a template that was not finished cannot pass. `$SKILLS` is defined in `moi-devrel/SKILL.md`. Facts are as of 2026-10-03.

| Template | For | Copy to | Change before use |
|---|---|---|---|
| `page-moidocs-concept.md` | a concept or reference page on docs.moi.technology | `docs/learn/...`, `docs/build/...` or `docs/guard/...` in `sarvalabs/moidocs` | The `image` line must match the folder: `/img/moi-card-learn.png` under learn, `/img/moi-card-build.png` under build, `/img/moi-card-guard.png` under guard. Those cards exist only on PR #124 as of 2026-10-01: on `main` delete the `image` line |
| `page-moidocs-tutorial.md` | a tutorial: actions in order | `docs/build/tutorials/` | Keep the import and the `HowToSchema` call at the top of the body and write no `# Title` line. Needs `HowToSchema`, which is on PR #124 of moidocs as of 2026-10-03 and not on `main` |
| `page-moidocs-faq.md` | a FAQ page | `docs/guard/` or the folder it belongs to | Needs `FaqSchema` (same note). Keep the old anchor on a heading you reword |
| `page-moidocs-stub.md` | a page that is not written yet | any moidocs folder | Remove the `<head>` block and the caution in the same change that adds the content |
| `page-voyage-docs.md` | a page on voyage-docs.moi.technology | `docs/getting-started/`, `docs/endpoint-docs/` or `docs/wallet-authentication/` in `sarvalabs/voyage-docs` | No `image`, no `# Title` |
| `page-coco-docs.md` | a page of the Coco Book | `docs/book/<chapter>/` in `sarvalabs/coco-docs` | For a stub add `unlisted: true` to the frontmatter. Chapter numbers go in `title` only. Link form: `/book/...` after PR #12, `/docs/book/...` on `main` |
| `page-sphinx.rst` | a page of the js-moi-sdk docs | `docs/source/` in `sarvalabs/js-moi-sdk` | Also add it to the toctree in `index.rst`; after PR #150 merges also the `PAGES` table and `sitemap.xml` (`references/write-sphinx.md`) |
| `category.json` | a new folder | `_category_.json` in the folder | Descriptions of existing categories are 143 to 150 characters |
| `pr-description.md` | the body of a docs pull request | the PR body field, after the operator's yes | Fill every section; delete none |
| `review-comments.md` | a drafted review of a docs PR | `docs-review-<N>/review.md`; make the folder with `mkdir -p docs-review-<N> && printf '*\n' > docs-review-<N>/.gitignore`; the operator posts it | None |
| `fact-check-report.md` | the report of a fact-check | `claim-check-<slug>/fact-check-report.md`, a folder that ignores itself | None |
| `drift-sweep-log.md` | one drift sweep | `docs-drift/<date>.md`, a folder that ignores itself (`references/drift.md`) | None |

The Docusaurus templates contain no comment lines on purpose: no page of moidocs or coco-docs holds an HTML comment (checked 2026-10-03), so do not add one.
