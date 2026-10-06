# Keep agent-discovery files and version-coupled pages in step

Facts are as of 2026-10-03, from the files on branch `geo-fixes` of each repo. Nothing ties these files together, so they drift without an error. Fix the cause and every file it touches in the same pull request. Page wording is in `moi-docs/references/page-standard.md`; pull request mechanics are `moi-devrel/ship`. Back to `../GUIDE.md`.

## What names what
| File | Names | Goes stale when |
|---|---|---|
| `static/.well-known/api-catalog` (moidocs, voyage-docs) | API reference pages. moidocs lists JSON-RPC, WebSocket, pNet (the Provenance Network API page) and two Voyage pages; voyage-docs lists its three | An API page is added, moved or renamed |
| `static/.well-known/agent-skills/index.json` (moidocs: `js-moi-sdk` and `coco`; coco-docs: `coco`) | For each skill: a `download` address and a `documentation` address | A Coco or SDK release; a skill page moves |
| `llms.config.json`, key `ecosystem` | The sibling sites, one line each. Every site lists the others | A site is added, moved or retired |
| `llms.config.json`, key `agentInstructions` | Where an agent should verify a version: npm for js-moi-sdk, `/releases/` for Coco | That place changes |
| `static/_headers` | The three targets of the `Link` header | One of them moves |
| `public/llms.txt` on the website and on the Launchpad | The docs sites and, on the website, the Launchpad | A docs page or section is removed |
| Skill pages: `docs/build/skills/coco-skill.md`, `js-moi-sdk-skill.md` (moidocs) | The zip name and version (the Coco page names it three times) | A release |
| `docs/releases/index.md`, `src/components/DownloadButton/downloads.mjs` (coco-docs) | The release section and the download links built from the version | A Coco release |
| `docs/source/conf.py` (`version`, `release`), `docs/generate_llms.py` `PAGES`, `agent-skill.rst` (js-moi-sdk) | The SDK version, which feeds the `softwareVersion` in structured data on the index page | An SDK release |

## What to touch when
| Event | Touch | Who confirms |
|---|---|---|
| New Coco release `X.Y.Z` | In coco-docs: a `## vX.Y.Z` section in `docs/releases/index.md` with `<DownloadGrid version="X.Y.Z" />`; the version strings in the book pages that quote it (`grep`, below). The `download` address in both skills indexes. The three mentions in `coco-skill.md`. The zip itself sits on `cdn.moi.technology/cocolang/` (Cloudflare R2). Commit bcbcbf8 (in moidocs) did the skills index and `coco-skill.md` half of this for 0.9.2. The coco-docs files are already at 0.9.2 on the branch, which Robert Špendl rebased onto v0.9.2 | Robert Špendl for the release. For the zip, DevOps is the likely publisher (inferred). ASK: Upendhar |
| New js-moi-sdk release | `conf.py`, `PAGES` if titles change, the skill page and the zip in `moidocs/static/downloads/`. The repo is at 0.9.0-rc3 while the Launchpad, Explorer and MCP pin 0.9.0-rc2, so check npm before quoting a version | The SDK team. ASK: Gokul |
| New API reference page | An entry in `api-catalog`, copying an existing entry's shape | Page author |
| A page is moved, renamed or deleted | Every entry above that names it; `grep` for the old address in every clone and search the `sarvalabs` organisation on GitHub, because other sites link in. Moving a page 404s old links unless a redirect exists: coco-docs has `static/_redirects`, moidocs and voyage-docs have none | ASK: Rahul how redirects are set up on the hosting. The style guide says to ask whoever manages it |
| A whole section is removed | The same, plus the estate `llms.txt` files | The person who removed it |
| A new site joins | Add it to the `ecosystem` list of every other site, and to the website's `public/llms.txt` | Rahul, who reviews docs scope (`moi-devrel/references/people-and-teams.md`) |

## Checks
Checks 1 and 5 run from any folder. Checks 2 and 4 run from one clone, or from the folder that holds your clones. Check 3 needs `moidocs` and `voyage-docs` cloned side by side, and runs from the folder that holds both.
1. Dead links in the catalog and skills index: `bash "$SKILLS/moi-docs/geo/scripts/geo-check.sh" https://<domain> --follow`. It requests each address once, up to 20, and only https links to public host names (a HEAD request, or a one-byte ranged GET), and prints host and path. A dead link is a FAIL line.
2. A version in every file: `grep -rIn --exclude-dir=node_modules --exclude-dir=build --exclude-dir=.docusaurus --exclude-dir=.git '0\.9\.2' .` with the version you are changing. coco-docs quotes it in many book pages (`module.mdx`, `compiler.md` and others).
3. The shared scripts are still identical, with the `geo-fixes` branch checked out in both (the scripts are not on `main` yet): `diff moidocs/scripts/generate-llms.mjs voyage-docs/scripts/generate-llms.mjs` and the same for `inject-schema.mjs`. No output means identical (true on 2026-10-03). If you change one, copy it to the other. coco-docs differs on purpose; carry a fix across by hand.
4. An old address still linked: `grep -rn '<old path>' .` in each clone.
5. Pages in `llms.txt` that the sitemap leaves out: `bash "$SKILLS/moi-docs/geo/scripts/geo-check.sh" https://<domain>` prints `llms-vs-sitemap`.

## Drift on 2026-10-03
| Where | What | Fix | Ask |
|---|---|---|---|
| `launchpad.moi.technology/llms.txt` | Tells agents the official Launchpad docs are at `docs.moi.technology/docs/build/launchpad/`, which 404s. Rahul decided on 2026-09-17 that application docs do not belong in the protocol docs | Commit 204e2ef, local only, repoints it | Adithya for a copy. Opening the pull request is a GATE |
| `moidocs/static/downloads/coco-0.8.2-skills.zip` | Tracked in git and referenced by nothing now; the skills index points at the 0.9.2 zip on the CDN. Commit bcbcbf8 kept it on purpose, "so its URL keeps working" | Keep it unless someone decides old links no longer matter | Rahul or Gokul |
| The js-moi-sdk skill | Says it was checked against SDK v0.7.1 while its docs page says it targets the current SDK | Refresh the skill or correct the page | Gokul |
| `api-catalog` and `llms.txt` of moidocs | The pNet entry is titled "Provenance Network API (Indus TestNet)". `moi-devrel/references/terminology.md` says the current network is devnet and "Indus" is not the current name | Check what network the pNet API serves, then reword | Gokul <!-- slop-lint: ignore --> |
| `DOCS-STYLE-GUIDE.md` | Its robots section is older than the file (`crawlers.md`) | Correct the guide in PR #124 | The PR author |

## Rules
- Never hand-edit `llms.txt`, `llms-full.txt` or a `.md` copy on the Docusaurus sites. Change the page's title or description, or the config, and rebuild. The hand-kept `public/llms.txt` of the website, the Voyage app and the Launchpad are edited by hand (`the-layer.md`).
- Keep `agentInstructions` true. An agent is told to trust them over its memory.
- Keep the `Organization` `@id` exactly `https://moi.technology/#organization` everywhere, so search engines treat the sites as one family.
- A new JSX component used in a page also goes into `DROPPED_COMPONENTS` in `generate-llms.mjs` (moidocs, voyage-docs) or the `components` map (coco-docs).

## Not yet known
- Whether the SDK skill needs a refresh to match the current SDK. ASK: Gokul.
- Who publishes the Coco skill zip to R2 and when. ASK: Upendhar and Robert Špendl.
- Whether anyone but the previous operator edits `api-catalog`. ASK: Adithya.
