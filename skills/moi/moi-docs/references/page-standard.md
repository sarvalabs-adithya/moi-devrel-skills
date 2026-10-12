# The page standard: what a page must meet

Facts are as of 2026-10-03. Each rule shows its source and the lint rule that checks it (`python3 "$SKILLS/moi-docs/scripts/docs-page-lint.py" --list-rules` prints all of them with their level; `$SKILLS` is defined in `moi-devrel/SKILL.md`). A rule marked "derived" is this library's reading and is not written in the style guide. Back to `../SKILL.md`.

## Where the rules come from
| Source | What it is | State |
|---|---|---|
| `DOCS-STYLE-GUIDE.md` at the root of `sarvalabs/moidocs` | The rule set for all four sites: seven rules, new page, update a page, per-site table, new-site appendix, common mistakes. Read in full on 2026-10-03 from branch `geo-fixes` (commit `bcbcbf8`). The text was rewritten for humans after Rahul's call of 2026-09-17 and added in commit `52f428e` (author date 2026-09-22). It sits outside `docs/`, so no site publishes it (Rahul via the previous operator, 2026-09-22) | Only on PR #124's branch (`origin/geo-fixes`). Not on `main`, GitHub's default branch |
| Drive document "MOI Documentation Standard", two versions of 2026-09-14 | The standard written before the guide, with a "PR Review Checklist for Docs Reviewers". Version 2 is a superset of version 1 (the notes this library was built from compared them); that it is the canonical one is inferred. The guide came eight days later. Whether the Drive document is now retired is not stated | Drive only. Not read for this file, so every line sourced to it is secondhand. ASK: Adithya for a copy, ASK: Rahul which one governs |
| `DOCS-GEO-STANDARD.md`, ten rules | The standard that lived in the moidocs repo before the guide. Commit `52f428e` removed it ("retire the old standard"). It survives in the history of the PR branch (`742a2c2`) | Retired. Do not follow it |
| Rahul's review corrections | No application docs in protocol docs (2026-09-17); the guide must be written for humans (2026-09-17) | Quoted in `review-a-pr.md` |
| `moi-devrel` house rules and `moi-devrel/references/terminology.md` | No em dashes, MOI wording, claims checked against source | `moi-devrel/references/` |
When the guide and the files in the repo disagree, say so in the PR and follow the file for anything the build reads (`robots.txt` is the known case, owned by the `geo` branch).

## 1. Frontmatter
The file starts with `---` on line 1. Nothing above it, not even a blank line, or the site ignores the whole block (guide step 1; lint `fm-not-first`, `fm-missing`, `fm-unclosed`, `fm-bom`).
| Field | Needed | Rule | Lint rule |
|---|---|---|---|
| `title` | yes | The page's own name in a few words. No version number, no date unless the page is a changelog entry. The site adds its own name, so leave it out. Search results cut near 60 characters. coco-docs Book pages carry the chapter number in the title (`2.7 Logic and Actor State`) and leave it out of the `# H1` | `title-missing`, `title-long`, `title-version`, `title-site-name` |
| `description` | yes | A statement of what the page covers, not a teaser. 140 to 160 characters; 130 to 170 is accepted, and a few characters outside is fine if it reads well. Never pad or cut to hit a number. Wrap the whole value in double quotes if it contains a colon followed by a space, or the Docusaurus build fails (YAML). One line: the llms generator reads one line (inferred from its pattern). Count with `wc -m` on a file holding only the text | `description-missing`, `description-length`, `description-teaser`, `description-multiline`, `fm-yaml` |
| `sidebar_position` | yes | Where the page sits in its folder; pages and subfolders share one list. List both before you choose: `grep -h "^sidebar_position:" docs/<folder>/*.md*` and `grep -h '"position"' docs/<folder>/*/_category_.json`. Numbers need not be consecutive. An index page gets a warning, not an error: the coco-docs generator lists an index page first in its folder | `sidebar-position-missing`, `sidebar-position-value` |
| `image` | moidocs only | `/img/moi-card-learn.png` under `docs/learn/`, `/img/moi-card-build.png` under `docs/build/`, `/img/moi-card-guard.png` under `docs/guard/`. Leave out elsewhere and on the other sites | `image-wrong`, `image-extra`, `image-card-missing` (on `main` the cards do not exist yet: leave `image` out until PR #124 merges) |
| `keywords` | no | Google ignores it. Keep the ones a page has; a new page may add five to ten terms | none |
| `unlisted` | coco-docs stubs | `unlisted: true` marks a stub (see rule 6) | `stub-wrong-marker` |
A category folder needs `_category_.json`. The guide only says to add one. The existing `generated-index` categories carry a `link.description` of 143 to 150 characters (measured 2026-10-03; the guide does not state this rule). Lint: `category-json`, `category-description`.

## 2. The body
| # | Rule | Source | Lint rule |
|---|---|---|---|
| R1 | Open with one paragraph that says what the thing is, before prerequisites or history. It must make sense if it is the only paragraph read. Good: the first paragraph of `docs/learn/fundamentals/account.md`. Bad: "Before diving into accounts, it's worth understanding..." | Guide rule 2, step 2 | `opening-missing`, `opening-throat`, `opening-short` (heuristics) |
| R2 | One main title. Either the first body line `# Title` using the same words as the frontmatter `title`, or none and the site shows the frontmatter title. Copy the neighbouring page. voyage-docs leaves the `# H1` out, coco-docs writes it. Use `##` and `###` for sections | Guide rule 3, step 3, per-site table | `h1-multiple`, `h1-voyage`, `heading-skip` (derived) |
| R3 | Phrase a section heading as a question only where the section answers that question (`## What is an Account ID? {#account-id}`). A plain heading such as "Prerequisites" stays plain | Guide rule 3 | none |
| R4 | When you reword a heading keep its old anchor: `## How do I upgrade MOIPod to the latest version? {#upgrading-moipod-to-the-latest-version}`. To change an anchor on purpose, `grep -rn "old-anchor" .` from the repo root, fix every hit in the same change, and search the `sarvalabs` GitHub org too | Guide rule 4 | `anchor-lost` (needs `--added-lines-since`) |
| R5 | Spell product names as in section 3, in titles, headings, body and image alt text. Commands, package names, URLs and code keep their real spelling | Guide rule 5, step 4 | `name-*` |
| R6 | Mark an unfinished page: moidocs and voyage-docs put `<head><meta name="robots" content="noindex" /></head>` (multi-line form) directly after the frontmatter, coco-docs writes `unlisted: true`. A stub is a page whose question stays unanswered or that holds a placeholder. If unsure, say so in the PR. Remove the mark in the same change that finishes the page: nothing warns you, and a finished page that keeps it never appears in search. Example: `docs/learn/fundamentals/networks.md` | Guide rule 6, step 5 | `stub-unmarked`, `stub-marked-finished`, `stub-text`, `stub-wrong-marker` |
| R7 | moidocs only: a tutorial (actions in order) carries a `HowToSchema` call and an FAQ page a `FaqSchema` call, at the top of the body, with no `# Title` line and no blank line inside the call. The other two Docusaurus sites have neither component: write an ordinary page | Guide step 6 | `schema-*` (including `schema-component-missing` on a checkout without the components), `h1-with-schema`, `tutorial-no-howto`, `faq-no-schema` |
| R8 | Link to another page of the same site by its address from the site root, never with the domain, so a preview build stays on the preview: `/docs/build/json-rpc` (moidocs), `/docs/endpoint-docs/faucet` (voyage-docs), `/book/language/state/` with a trailing slash (coco-docs after PR #12; on `main` the Book is under `/docs/book/`, so write `/docs/book/language/state/` there and let the lint's `link-route-prefix` tell you which form the checkout wants). Existing relative links that work stay | Guide step 7, per-site table | `link-absolute-internal`, `link-form`, `link-route-prefix` |
| R9 | An external address always carries `https://`. Without a scheme the browser reads it as a path on the same site | derived (the same defect is checked on blog posts in `moi-blog`) | `link-no-scheme`, `link-empty`, `link-http` |
| R10 | If the page documents an API or an agent skill package, list it in the site's `.well-known` file (`api-catalog` on moidocs and voyage-docs, `agent-skills/index.json` on moidocs and coco-docs), copying the shape of an existing entry. Otherwise skip | Guide step 8 | none. File ownership: the `geo` branch |
| R11 | Never edit a generated file: `llms.txt`, `llms-full.txt`, the `.md` copies, the sitemap, structured data. Edit the page's title or description and rebuild. js-moi-sdk is the exception (rule 12) | Guide rule 7 | none |
| R12 | js-moi-sdk (Sphinx): the description is `.. meta::` then `   :description: ...` at the top of the `.rst`, plain text; the page is in the `toctree` of `index.rst`; after PR #150 also a row in `PAGES` in `docs/generate_llms.py` with the same description, and a line in `docs/source/_extra/sitemap.xml` | Guide, "If you work on js-moi-sdk" | `meta-description-missing`, `toctree-missing`, `sdk-*`, `rst-*` |
| R13 | No placeholder text: `TODO`, `TBD`, lorem ipsum, a bare `[link]`, a template's `FILL-IN` | Drive standard (secondhand, not read), house rule | `placeholder` <!-- slop-lint: ignore --> |
| R14 | No application docs in protocol docs. Rahul's reason: the Agent Launchpad is an app that uses MOI and could shut down, so its docs belong with the app and its use cases with moi.technology. A backlink is fine | Rahul, 2026-09-17 (commit `75f608b`) | `application-docs` |
| R15 | Do not publish a page you cannot ground in source. The kill-switch page was deleted on 2026-09-09 because it did not say what the kill switch is | The previous operator, 2026-09-09 | none: `moi-devrel/claim-check` |

## 3. Names
| Thing | Write | Never write | Lint rule |
|---|---|---|---|
| Protocol | MOI | Moi | `name-moi` |
| Wallet | MOI Wallet | Moi Wallet, MoiWallet | `name-moi-wallet` |
| Language | Coco; on first mention of a page "Coco (also known as Cocolang)" | CoCo, CocoLang | `name-coco` <!-- slop-lint: ignore --> |
| SDK | js-moi-sdk, lowercase even at the start of a sentence (rephrase) | JS-MOI-SDK, Js-Moi-Sdk | `name-js-moi-sdk` <!-- slop-lint: ignore --> |
| Guardian node software | MOIPod | Moipod | `name-moipod` <!-- slop-lint: ignore --> |
| Explorer and gateway | Voyage | | none |
| Company | Sarva Labs | SarvaLabs (guide); Serval Labs (an auto-notes misspelling, `moi-devrel/references/terminology.md`) | `name-sarva-labs` <!-- slop-lint: ignore --> |
Tagline, word for word where space allows: "The participant layer for AI agents." The wider wording rules (participant-centric, network ID, devnet, KMOI) are `moi-devrel/references/terminology.md`, enforced through `slop-lint.sh`, which the lint calls.

## 4. Differences per site
| | moidocs | voyage-docs | coco-docs |
|---|---|---|---|
| Pages in | `docs/` | `docs/` | `docs/book/`, `docs/install/`, `docs/releases/` |
| Address starts | `/docs/` | `/docs/` | After PR #12: `/book/`, the Book home is `/`. On `main`: `/docs/book/` |
| `# H1` | either, copy neighbours | leave out | write it |
| Stub mark | noindex block | noindex block | `unlisted: true` |
| `image` | section card | leave out | leave out |
| FAQ and tutorial components | yes | no | no |
| Components in pages | `Tabs`, `TabItem`, admonitions, `HowToSchema`, `FaqSchema`, `Whitepapers` (one page) | `Tabs`, `TabItem` | `InstallGuide`, `VSCodeExtension`, `DownloadGrid` (releases) |
A new component must also be handled by the llms generator (`write-docusaurus.md`).

## 5. Prose and code samples
- Short direct sentences, no metaphors, no filler, no generic AI phrasing (the previous operator's rule of 2026-09-09: real, direct, efficient). No em dashes in anything you write: 145 lines of existing moidocs pages carry one (lint run on the PR branch, 2026-10-03), so lint only your added lines (`--added-lines-since`). Run `slop-lint.sh`; `humanizer` and `stop-slop` are optional helpers on the previous operator's machine and are not part of this library.
- State no universal the protocol does not guarantee ("Every action on MOI costs fuel" was removed from a post as untrue, 2026-09-11). The same standard applies to a docs sentence. <!-- slop-lint: ignore -->
- A code sample runs as written against the SDK version the page names, or the page says it is simulated (house rule 5). Spending devnet funds to prove it needs the operator's yes. Never put a real key or recovery phrase in a sample.
- Authors may use AI. They must know whether what they publish is right or wrong (Rahul, call of 2026-09-17). That is the reason for `fact-check-a-pr.md`.

## 6. What the lint cannot judge
The facts, whether an opening paragraph actually defines the thing, whether a link target exists, whether an anchor on another page exists, whether the build passes, what an image shows, and whether a sample runs. A clean lint is the floor: read the page, open the preview and check the claims (`moi-devrel/claim-check`).

## Where the sources disagree
- Title format: the Drive standard, as notes record it, writes the title as `Page Name | Site Name`; the guide (later) says the site adds its own name, so leave it out. Follow the guide. The lint's `title-site-name` warns on a `|`. ASK: Rahul if the Drive document should be retired.
- Titles: the guide says the `# H1` uses the same words as the `title`. Some Book pages do not (`1.1 Flipper` is headed "Flipper: Your First Coco Program"). The lint does not compare them.
- Links: the guide says coco-docs addresses end with a slash. 29 links in the Book and the releases page do not (lint run on the PR branch, 2026-10-03). New links follow the guide. The guide's `/book/` form is the form after PR #12; `main` still uses `/docs/book/`.
- The guide says the build fails when a link points nowhere. `onBrokenLinks` is `throw` for routes, but `onBrokenMarkdownLinks` is `warn`, and heading anchors are not checked on Docusaurus 2.1 (inferred). Check them by hand.
- The guide says to set `trailingSlash` explicitly. moidocs and voyage-docs configs do not (they rely on the default). Changing it is a decision for the site owners. ASK: Rahul.
- The guide's crawler section still describes one block per crawler; the committed `robots.txt` has one group. `geo/references/crawlers.md` covers it.

## Terms
- **Frontmatter**: the block between two `---` lines at the very top of a page file. It holds `title`, `description`, `sidebar_position` and the other fields in section 1.
- **Anchor**: the part of a link after `#`. Docusaurus builds it from the heading text, so rewording a heading changes it. `{#old-anchor}` after the heading pins it.
- **Stub**: a page whose reader finishes with the question unanswered, or that holds a placeholder. A stub carries a mark that keeps it out of search results and the sitemap: the `noindex` block (`<head><meta name="robots" content="noindex" /></head>`) on moidocs and voyage-docs, `unlisted: true` on coco-docs.
- **Sidebar position**: where a page sits in its folder's list in the left menu. Pages and subfolders share one numbered list.
- **llms.txt, llms-full.txt, markdown copies, sitemap**: files the build writes for AI agents and search engines. Never edited by hand (rule R11). Owned by the `geo` branch.
- **Schema component** (`HowToSchema`, `FaqSchema`): a moidocs component that adds structured data to a tutorial or FAQ page. It exists on PR #124's branch only.
- **toctree**: the list in `index.rst` that makes a Sphinx page reachable. **PAGES**: the table in `docs/generate_llms.py` (PR #150) that repeats each SDK page's title and description.
- **Preview**: on moidocs, voyage-docs and coco-docs, the copy of the site that Cloudflare Pages builds for every pull request branch and comments on the PR. **Production**: the live site, built from `main` on every merge on those three; the js-moi-sdk docs pipeline and previews are unknown (`sites.md`).
- **Lint rule id**: the word after the colon in a lint line, for example `fm-yaml`. `python3 "$SKILLS/moi-docs/scripts/docs-page-lint.py" --list-rules` explains each.
