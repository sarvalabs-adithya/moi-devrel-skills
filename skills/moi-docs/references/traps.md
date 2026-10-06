# Traps: what goes wrong without an error

Facts are as of 2026-10-03. Each row is a defect that was met, with its date or its source. "Inferred" marks a reading of code that nobody ran. `$SKILLS` and `ASK:` are defined in `moi-devrel/SKILL.md`. Back to `../SKILL.md`.

## Frontmatter and the build
| Trap | What happens | Do this | Source |
|---|---|---|---|
| A `description` with a colon and a space, unquoted | The Docusaurus build fails with a YAML error | Wrap the whole value in double quotes. The lint reports `fm-yaml` | Guide, common mistakes |
| A blank line above the first `---` | The site ignores the whole frontmatter: no title, no description | Line 1 is `---`. The lint reports `fm-not-first` | Guide step 1 |
| A multi-line `description`, CRLF line endings or a byte order mark | The llms generator reads frontmatter line by line, with an LF-only pattern in moidocs and voyage-docs, so title and description may be missing from `llms.txt` (inferred from the code) | Keep both fields on one line, save as plain UTF-8 with LF | `scripts/generate-llms.mjs` read 2026-10-03 |
| A broken `.md` link or a broken anchor | `onBrokenLinks` is `throw` for routes only. `onBrokenMarkdownLinks` is `warn`, and anchors are not checked on Docusaurus 2.1 (inferred) | Open each new link on the preview | Configs read 2026-10-03; guide says the build fails on any |
| `docs/build/index.md` and `docs/build/index.mdx` both on moidocs `main` | Two pages claim the same route; the PR branch deleted the `.mdx` | Check for a twin before you add an index page | `git ls-tree` 2026-10-03 |
| `npm run build` on `main` of moidocs | It is a plain `docusaurus build`; none of the llms or schema steps run, and `HowToSchema` does not exist | Read `sites.md` before you copy a tutorial template | `package.json` on `main` |
| A tutorial or an `image` line copied from a template onto `main` of moidocs | `HowToSchema` is not in `src/components` and `/img/moi-card-*.png` is not in `static/img`, so the import cannot resolve and the share image does not exist | Write without them until #124 merges. The lint reports `schema-component-missing` and `image-card-missing` | `git ls-tree origin/main`, 2026-10-01 fetch |
| A `/book/...` link on `main` of coco-docs | `main` serves the Book under `/docs/book/`; `/book/` exists only with `routeBasePath: '/'` on PR #12. `onBrokenLinks` is `throw`, so the build probably stops (inferred, not built). The live site answers 404 for `/book/` and 200 for `/docs/book/` (2026-10-03) | Link to the form the checkout uses. The lint reports `link-route-prefix` | `docusaurus.config.js` on both branches |
| A commit hash quoted in these notes | The open branches were rewritten on 2026-10-01 (attribution lines removed), and a squash merge changes hashes again | Find the commit by its message with `git log --grep` | `git reflog`, 2026-10-01 |

## Headings, stubs and components
| Trap | What happens | Do this | Source |
|---|---|---|---|
| Rewording a heading | Its anchor changes and every link to it lands at the top of the page. Nothing reports it | Add `{#old-anchor}`; for a deliberate change `grep -rn` the repo and search the `sarvalabs` org first. The lint's `anchor-lost` (with `--added-lines-since`) finds it | Guide rule 4 |
| `# Title` on a page with a `HowToSchema` or `FaqSchema` call | Two titles | Let the frontmatter be the only title | Guide, common mistakes |
| A blank line inside a schema call | The page may fail to parse | The call may span lines, but every line needs content | Guide step 6 |
| Finishing a stub and keeping its mark | The finished page never appears in search | Remove the mark in the same change | Guide step 5 |
| An unfinished page with no mark, or a template sample page | It reaches the sitemap. The September build still listed `markdown-page`, the template sample, until commit `bcbcbf8` removed it | Mark stubs. Look at `build/sitemap.xml` after a build | Research, 2026-09-22 |
| A new JSX component in a page | Raw JSX leaks into the markdown copies (265 lines of `llms-full.txt` once, fixed in `f639f41`) | Handle it in the generator (`write-docusaurus.md`) | Research |

## Generated files
| Trap | What happens | Do this | Source |
|---|---|---|---|
| Editing `llms.txt`, `llms-full.txt`, a `.md` copy or the sitemap | The next build overwrites it | Edit the page's title or description | Guide rule 7 |
| Three generator variants | moidocs and voyage-docs share one older pair of scripts (identical); coco-docs has a newer pair with `scripts/lib/docs.mjs`; js-moi-sdk uses `generate_llms.py`. A fix in one is not a fix in all | `diff` the scripts after any change; ask before touching one | `DEPENDENCIES.md` section 15 (the previous operator's file, local to his machine; ASK: Adithya for a copy); research |
| js-moi-sdk commits its generated files | A 22,549-line PR where almost every line is generated | Review the script and the `PAGES` change, not the output | PR #150 |
| Cloudflare builds from a shallow clone | Every page's `dateModified` shows the head commit's date unless history is deepened. The injector tries `git fetch --unshallow` and omits the date if that fails | None for authors; do not hand-set dates | `inject-schema.mjs` |
| `trailingSlash` differs between `docusaurus.config.js` and `llms.config.json` | The `.md` addresses in `llms.txt` do not match the pages. moidocs and voyage-docs do not set it in the config and rely on the default | Do not change it without the owners. ASK: Rahul | Guide appendix; configs |

## Git and pull requests
| Trap | What happens | Do this | Source |
|---|---|---|---|
| A rebase resolved toward the old copy | Someone else's merged content is silently reverted. Commit `0899368` (2026-09-17) restored `submit-ixn.md` after a rebase had kept an older copy | After every rebase, diff the pages against `main` | `pr-upkeep.md` |
| A PR body that no longer matches the diff | Three of five bodies were stale on 2026-10-02 | Re-read the body against the diff before each push | `pr-upkeep.md` |
| A push, PR, comment or review you were not told to make | Teammates are notified of work that is not ready (2026-09-28); the previous operator wrote "never directly push unless I explicitly say so" (2026-09-09) | Draft, show, wait for a yes naming the action | `moi-devrel/references/consent-and-identity.md` |
| An AI co-author line or a "Generated with" footer | Removed from 130 commits on six open PRs on 2026-10-01 | Never add one | `moi-devrel/references/consent-and-identity.md` section 3 |
| One PR per review tweak | Too many small PRs (2026-09-15) | One batch branch, one PR | Rule of 2026-09-15, set during the Points audit stack |
| Backup branches left behind | Local clutter and the risk of pushing one | Delete after the PR merges | DEPENDENCIES sections 13 to 15 |

## Hosting and sites
| Trap | What happens | Do this | Source |
|---|---|---|---|
| A Cloudflare zone setting that blocks AI crawlers | Overrides every file. cocolang.dev returned 403 to them until 2026-09-09 | After any hosting change, run the crawler check in `geo/GUIDE.md` | Research |
| js-moi-sdk's host answers 200 with HTML for paths that do not exist | A status check passes for a file that is not there. `/robots.txt`, `/llms.txt` and `/sitemap.xml` all gave `200 text/html` on 2026-10-03 | Check the content type and the body | Live GET |
| `html_baseurl` in Sphinx `conf.py` | Every canonical points at a redirect | Leave it unset | Guide appendix |
| The README of moidocs says `develop` deploys to `moichain-docs.pages.dev` | `develop` ends in July 2023 and is an ancestor of `main` | Treat the README table as stale. Which branch each Pages project builds is not on record. ASK: Rahul | `git log` 2026-10-03 |
| The README of coco-docs: `npm runs start`, and `cd cocodocs` after cloning `coco-docs` | The commands fail | `npm run start`; `cd coco-docs` | README on `main` |
| `main` configs still carry the old `url` (`wiki.moi.technology`, the `cocolang.docs` mirror) | Canonical links and sitemap entries name a host that does not serve the page | Do not copy a config from `main` into a new site | `git show` 2026-10-03 |
| Merge is publish on three of the sites | Cloudflare builds `main` to production on every merge of moidocs, voyage-docs and coco-docs, and the guide records no manual deploy step. A rollback route is not recorded. ASK: Rahul. The js-moi-sdk docs and wallet docs pipelines are unknown. ASK: Gokul, Rahul | Merge only on a yes naming the PR number and base branch | `moi-devrel/SKILL.md` fact 1; guide |

## Content
| Trap | What happens | Do this | Source |
|---|---|---|---|
| Version strings in many places | Coco 0.9.2 sits in 12 files of coco-docs on the PR branch (11 on `main`) plus the skill page and the index; a stale 0.8.2 zip is still in moidocs `static/downloads/` | `drift.md` coupling table | Grep 2026-10-03 |
| A page documents what the live network does not serve | `net.NetworkID` is in the JSON-RPC page and absent on devnet (2026-10-03) | Read the wire before writing "live" (`moi-devrel/references/devnet.md`) | Live read |
| The docs as a source | Operation-code numbers on docs.moi.technology were swapped against the node source at v0.12.0 (August 2026) | Check the node or SDK source at the tag; docs are rank 4 (`moi-devrel/claim-check/references/sources-of-truth.md`) | Claim-check notes |
| Application content in protocol docs | Rahul sent the Launchpad section out of #124 (2026-09-17) | Link to the app's own docs | `page-standard.md` R14 |
| A page nobody can ground | The kill-switch page was deleted on 2026-09-09 | Do not publish a page you cannot ground in source | Research |
| A report that counts three ways | "27 errors" over a table of 26 and a list of 25 (2026-08-21) | Recount after every edit | `fact-check-a-pr.md` |
| A status that claims work that was not done | A line about standardising org descriptions across Crunchbase, LinkedIn and GitHub was removed on 2026-09-10 | Report done work only; label plans as to-dos | `moi-devrel/references/house-style.md` |
| A sample recovery phrase in a page | The lint flags it (`recovery-phrase-shaped`); the SDK signer page has five | The operator confirms each is a documented sample and never a real phrase; Claude does not open or repeat the flagged lines | `moi-devrel/references/consent-and-identity.md` section 5 |
| Old em dashes | 145 lines in moidocs. A whole-file lint reports them as errors | `--added-lines-since` | Lint run 2026-10-03 |

## Limits of the tools here
- `docs-page-lint.py` finds the shape of a problem, never its truth. A page can pass and be wrong.
- Its heading slug is an approximation of Docusaurus's; `anchor-lost` and `link-anchor-missing` are warnings for that reason.
- `slop-lint.sh` reads `account based` in plain English as the wrong model name (a false hit in `json-rpc.md`). <!-- slop-lint: ignore -->
- None of the repos' own checks runs on a PR except the Pages build (and "Run Tests" on js-moi-sdk). A green check means the site built.
