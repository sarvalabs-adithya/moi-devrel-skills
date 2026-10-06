# Write a page on a Docusaurus site, from nothing to a pull request

For docs.moi.technology (`sarvalabs/moidocs`), voyage-docs.moi.technology (`sarvalabs/voyage-docs`) and cocolang.dev (`sarvalabs/coco-docs`). Facts are as of 2026-10-03. The rules a page must meet are in `page-standard.md`; the sites are in `sites.md`. `$SKILLS`, "the operator" and `ASK:` are defined in `moi-devrel/SKILL.md`. For the Sphinx site use `write-sphinx.md`. Back to `../SKILL.md`.

## Before the first command
1. Know which of two states you are in. The style guide, the schema components, the section cards, the `image` field, the llms scripts and (on coco-docs) the move of the Book from `/docs/book/` to `/book/` exist only on the open PR branches as of the last fetch (`sites.md`). On `main`, `npm run build` is a plain `docusaurus build`, and `HowToSchema` and `FaqSchema` do not exist, so a tutorial written from the template would fail to build there (the import cannot resolve; not run). On moidocs `main` the image `/img/moi-card-build.png` does not exist either, so leave `image` out there. On coco-docs `main` link to `/docs/book/...`, not `/book/...`. Read PR state first (`gh pr view <N> --repo sarvalabs/<repo> --json state,mergedAt`); if the PR has not merged, write for `main` and add the rest when it does, or base your branch on the PR branch with the operator's agreement. The lint reads the checkout it is in and says which form it wants (`link-route-prefix`, `image-card-missing`, `schema-component-missing`).
2. The three repos are private. Access comes from an org admin. ASK: Rahul.
3. No secrets are needed to build any docs site (`DEPENDENCIES.md` section 13, local to the previous operator's machine; ASK: Adithya for a copy). If a step asks for a key, stop.

## The steps
GATE marks a step that needs the operator's explicit yes first (`moi-devrel/references/consent-and-identity.md`).
| # | Step | Command or action | Done when |
|---|---|---|---|
| 1 | Clone or update | GATE: `git clone git@github.com:sarvalabs/<repo>.git` then `cd <repo>`, or in an existing clone `git fetch origin`, because both download. Then `git switch -c docs/<short-name> origin/main` | A branch off the current `main` exists |
| 2 | Identity | From inside the repo: `bash "$SKILLS/moi-devrel/scripts/preflight.sh"` | No FAIL, every WARN read |
| 3 | Install | GATE: `npm install` (downloads the dependencies from the npm registry). Node `>=16.14` for moidocs and voyage-docs, `>=18` for coco-docs | `npm run start` serves the site (voyage-docs binds port 6420, coco-docs is on http://localhost:3000). Stop only the server you started, by its port or PID, never by name |
| 4 | Find the neighbour | Open a page in the same folder and copy its conventions for the title and the H1 | You know whether this folder writes `# Title` |
| 5 | File and position | File name in lower-case words with hyphens (`account-tutorial.md`). List positions as in `page-standard.md` section 1. A new folder needs `_category_.json` (`templates/category.json`) | The page sits where you want it in the sidebar |
| 6 | Copy a template | `cp "$SKILLS/moi-docs/templates/page-moidocs-concept.md" docs/learn/fundamentals/<name>.md`, or the tutorial, FAQ, stub, voyage-docs or coco-docs template | A file with every blank marked `FILL-IN` | <!-- slop-lint:ignore -->
| 7 | Write | Opening paragraph first (rule R1). Names per the table. Headings per R2 to R4. Every technical statement has a source and a ref you can name | No `FILL-IN` left | <!-- slop-lint:ignore -->
| 8 | Components | Only those in the table below. For a tutorial or FAQ on moidocs, copy the import and the call from the template and change only the data | The page builds |
| 9 | Lint | `python3 "$SKILLS/moi-docs/scripts/docs-page-lint.py" docs/learn/fundamentals/<name>.md` (a new file counts as all added). For an existing page add `--added-lines-since origin/main` | 0 errors; every warning read and answered |
| 10 | Build | `npm run build`. Read the output (below). Look in `build/` for the page | Exit 0 and no `generate-llms:` warning |
| 11 | Preview | `npm run start`, open the page, click the links, check the sidebar position | The operator has seen the page |
| 12 | Check the claims | `mkdir -p claim-check-<slug> && printf '*\n' > claim-check-<slug>/.gitignore`, then `python3 "$SKILLS/moi-devrel/claim-check/scripts/extract-claims.py" --all docs/learn/fundamentals/<name>.md > claim-check-<slug>/claims-candidates.csv && cp -n claim-check-<slug>/claims-candidates.csv claim-check-<slug>/ledger.csv` (keep `claims-candidates.csv` untouched; `moi-devrel/claim-check` step 8 needs it for `--dropped`). Check each row against the tag or package version the page names (`moi-devrel/claim-check`), fix the text, then `python3 "$SKILLS/moi-devrel/claim-check/scripts/ledger-status.py" claim-check-<slug>/ledger.csv` | The status script exits 0. The folder ignores itself, so the ledger (which can name private source) stays out of git |
| 13 | Polish | `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" docs/learn/fundamentals/<name>.md`, then read the page aloud once | The operator has read the final text |
| 14 | Commit | Only after the operator asks for it. Work identity, no AI co-author line, no footer. Mechanics: `moi-devrel/ship` | A local commit; `git status` shows no generated file |
| 15 | PR | GATE: push and open the PR. `moi-devrel/ship` for the mechanics, `templates/pr-description.md` for the body | The Cloudflare preview comment is on the PR |
| 16 | After merge | Open the live page. If config or machine files changed, the post-merge steps in `geo/references/after-merge.md` | The live page shows the change |

## Components that are allowed
Counts are pages that use them on the PR branches, read 2026-10-03.
| Site | Allowed | Notes |
|---|---|---|
| moidocs | `Tabs` and `TabItem` (`import Tabs from '@theme/Tabs'`, 13 pages); admonitions `:::note`, `:::info`, `:::tip`, `:::caution`, `:::warning`; `HowToSchema` (6 tutorials) and `FaqSchema` (1 page), PR branch only; `Whitepapers` (1 page, the paper cards) | One page (`interactions.md`) puts an HTML paragraph with an `id` attribute where it needs an anchor that no heading gives |
| voyage-docs | `Tabs` and `TabItem` (1 page) | No schema components |
| coco-docs | `InstallGuide`, `VSCodeExtension` (from `@site/src/components/InstallSteps`), `DownloadGrid` (from `@site/src/components/DownloadButton`, releases page) | Admonitions such as `:::tip` are used on Book pages |
A new component also needs a line in the llms generator, or raw JSX leaks into `llms-full.txt` (265 lines did, fixed in commit `f639f41`): add its name to `DROPPED_COMPONENTS` in `scripts/generate-llms.mjs` (moidocs, voyage-docs) or to the `components` map in coco-docs. Change one repo's script and copy it to the other if they must stay identical (`diff` them). A new component is a code change: ask the maintainers first (Gokul for moidocs and voyage-docs, Robert Špendl for coco-docs).

## Writing a tutorial
- A tutorial walks the reader through actions in order. A reference page with numbered sections is not one.
- Copy the import and the `HowToSchema` call to the top of the body. No `# Title` line (the page would show two titles) and no blank line inside the call. Each step in the call describes what the page's own sections do, in its own words.
- Say what the reader will end with in the opening paragraph, then `## Prerequisites` with links to the pages that cover them.
- Code samples run as written against the SDK version the page names. Run them against devnet; spending devnet funds needs the operator's yes. Say plainly where a step is simulated. Use the MOI Wallet extension and the operator's own funded account for anything that signs. Claude never handles a recovery phrase.
- The SDK examples live in the tutorials as JavaScript. Take constants from the SDK, never from a literal (`moi-devrel/references/devnet.md`).

## What the build tells you
`npm run build` on a PR branch runs the generator, `docusaurus build`, then the injector. Read these lines:
- `generated static/llms.txt (N lines)` and `emitted per-route .md files`: N should grow by one line per page.
- `inject-schema: TechArticle + BreadcrumbList injected into N pages`: N equals the page count.
- `generate-llms: ... still has a JSX component`: a component the generator does not know. Fix it before the PR.
- A YAML error naming your file: an unquoted colon in the `description`.
- A broken route link stops the build (`onBrokenLinks: 'throw'`). A broken link to a `.md` file only warns, and anchors are not checked on Docusaurus 2.1 (inferred), so check anchors by hand.
Verifying the sitemap, canonical, JSON-LD, robots and `.well-known` is the `geo` branch's job (`geo/GUIDE.md`).

## Moving, renaming and deleting
Moving or renaming a page changes its address and gives old links a 404 unless a redirect exists. coco-docs keeps redirects in `static/_redirects` (PR branch only). moidocs and voyage-docs have no redirect file. Before moving a page, ask whoever manages the hosting how redirects are set up (the guide's instruction). The owner of the Pages projects is not on record: ASK: Rahul. After a rename, `grep -rn "<old-path>" .` and search the `sarvalabs` GitHub org, because other MOI sites link in.

## Images
Put the file in `static/img/` (moidocs, coco-docs) and write `![alt text](/img/<file>)`. Alt text names things by the naming table. Do not paste a screenshot that shows a key, a recovery phrase or a personal address. `static/guardian-tutorial/` and `static/monitor-guardian/` hold the Guardian screenshots on moidocs.

## Not yet known
- Which Node version the Pages projects build with, and whether the newest Node releases build the Docusaurus 2.1 sites: `engines` sets only a lower bound and nothing here tested it. ASK: Rahul who can read the Pages settings.
- Who reviews a page that is not about the protocol or Voyage. ASK: Rahul.
