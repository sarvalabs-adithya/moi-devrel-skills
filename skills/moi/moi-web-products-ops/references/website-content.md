# Website: pages, papers, PDFs and the sitemap

Updated 13 October 2026 for PR #57 (merged 5 October) and PR #60. Facts are as of 2026-10-03 from `sarvalabs/MOI-Website` `main` (`5e91afa`: `src/App.jsx`, `src/pages/PapersPage.jsx`, `public/sitemap.xml`, the file sizes in the git tree) and GET and HEAD reads. Back to `../SKILL.md`. A blog post is `moi-blog`. Search and AI-visibility work on any page is `moi-docs/geo`. Colours, type and logos are `moi-devrel/design`. A claim on a page is checked with `moi-devrel/claim-check`.

## What the site holds

| Path | What |
|---|---|
| `src/App.jsx` | The routes today: `/`, `/why-moi`, `/how-it-works` (redirects to `/why-moi`), `/manifesto`, `/papers` and the old calendar admin page (the homepage no longer uses it; the community block is `content/community-calls.json`, `website-calendar.md`) |
| `public/sitemap.xml` | Written by hand. Its header comment says to add an entry when you add a route. Blog articles are not listed here; the blog ships its own sitemap |
| `src/pages/PapersPage.jsx` | The `PAPERS` array: five entries, three of them (tech, math, PIC) external links to Zenodo records |
| `public/papers/moi-lite-paper.pdf`, `public/papers/moi-white-paper.pdf` | The files the Papers page serves |
| `public/MOILitePaper.pdf` | A second litepaper path, identical to the first (same git blob) |
| `docs/MOILitePaper.pdf` | The chat's ingest source. A different file from the other two |

Since 5 October 2026 (PR #57) the marketing pages are prerendered at build time, so a new page also needs a route in `src/entry-server.jsx` and an entry in `scripts/ssg.mjs`, besides `src/App.jsx` and `public/sitemap.xml`. Read how the existing pages are listed in those two files and add yours the same way.

## Run: add a page

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Baseline and branch | `website-ship.md` steps 1 to 3 | Clone and branch ready |
| 2 | LOCAL | Add the route | `<Route path="/<name>" element={<Page />} />` in `src/App.jsx`, the page file under `src/pages/`, the matching entries in `src/entry-server.jsx` and `scripts/ssg.mjs` (copy a neighbour), a navbar link if it should be reachable | The page renders on `npm run dev`, and `npm run build` writes its prerendered file |
| 3 | LOCAL | Add the sitemap line | A `<url><loc>https://moi.technology/<name></loc><priority>0.8</priority></url>` block in `public/sitemap.xml`, in the style of its neighbours | The file is valid XML (`xmllint --noout public/sitemap.xml` if installed) |
| 4 | LOCAL | Copy rules | Second person, declarative, short lines, sentence-case headlines, no emoji. Words: participant, authority, scope, revoke, on chain, agent. Avoid user, permissions, blockchain, AI assistant. Terms: `moi-devrel/references/terminology.md` | `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" <changed files>` has no error |
| 5 | GATE | Ship | `website-ship.md` steps 5 to 10 | Live |
| 6 | VERIFY | Read it | `curl -sI https://moi.technology/<name>` answers 200, but this host answers 200 for any address, so open the page and check the sitemap line is served: `curl -s https://moi.technology/sitemap.xml` | The page and its sitemap entry are live |

## Run: add or change a paper

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Get the real abstract | From the paper itself or its Zenodo record, never from a MOI brief. On 2026-06-04 a blurb drafted from a brief PDF was rejected because it described MOI, not the paper, and the Contextual Compute paper is the tech paper, not the vision paper | The abstract is in hand |
| 2 | LOCAL | Edit `PAPERS` | Object keys: `key`, `eyebrow`, `title`, `blurb`, `file`, `downloadName`; for a link use `external: true` and the Zenodo or DOI address. A PDF goes in `public/papers/` | `npm run build` passes |
| 3 | CHECK | Claims | Run `moi-devrel/claim-check` on the blurb. Its ledger folder names private files and people and the website repo is public, so it stays out of git (that branch makes it self-ignoring) | `python3 "$SKILLS/moi-devrel/claim-check/scripts/ledger-status.py" claim-check-<slug>/ledger.csv` exits 0 |
| 4 | GATE | Ship | `website-ship.md` | Live |
| 5 | VERIFY | Read the served file | `curl -sI https://moi.technology/papers/<file>.pdf` and compare `Content-Length` with `wc -c < public/papers/<file>.pdf` in the clone, which holds the file you shipped | Same size. Then open `/papers` and click the link |

To replace a paper that also lives in the Dataroom and the chat store, use `dataroom-papers.md` instead; it covers all copies.

## Traps
- Three paper paths drift: `public/papers/*.pdf`, `public/MOILitePaper.pdf`, `docs/MOILitePaper.pdf`. The website whitepaper has the size 2,245,957 bytes on `main` and on the live site (HEAD, 2026-10-03).
- PDFs are served without a download header (W-K5). Do not promise a "download" button's behaviour until nginx applies it.
- The sitemap is by hand, so a page without a line is invisible to crawlers.
- `vercel.json` rewrites the admin pages and `/papers` for the old host and does nothing on the VM.

## Not yet known
- Whether the Dataroom's Litepaper and the website's should be one file. ASK: Rahul.
- Whether the nginx PDF header fix was applied under a different path. ASK: Srikar.
