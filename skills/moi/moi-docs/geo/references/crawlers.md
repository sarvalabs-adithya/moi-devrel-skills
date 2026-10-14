# Allow or block a crawler, and where the content signal goes

Facts are as of 2026-10-03, from `static/robots.txt` on branch `geo-fixes` of `moidocs`, `voyage-docs` and `coco-docs`, `next-sitemap.config.js` in `sarvalabs/voyage`, the live files, and commit 7d58640 (2026-10-01). Back to `../GUIDE.md`.

## The file today
The three Docusaurus sites carry this file on `main` since the sweep PRs merged (voyage-docs #5 and coco-docs #12 on 2026-10-05, moidocs #124 on 2026-10-13); it was read on the PR branches on 2026-10-03. Only the comment header and the `Sitemap:` line differ (checked with `diff` on 2026-10-03). The js-moi-sdk copy, `docs/source/_extra/robots.txt`, has the same four lines.
```
User-agent: *
Content-Signal: search=yes, ai-input=yes, ai-train=yes
Allow: /
Sitemap: https://<domain>/sitemap.xml
```
It is one group on purpose. The comment in the file gives the reason: a `Content-Signal` line only counts inside a `User-agent` group, and a crawler obeys the one group that names it most specifically. So a group for `GPTBot` or `ClaudeBot` takes that crawler out of the `*` group and it loses the signals. The file names no crawler. Commit 7d58640 replaced an earlier file that had a group per crawler; commit 0b6319b of 2026-09-09 ("robots: add the 2026 AI-crawler token split") had added five more groups to it.

## The placement rule
1. `Content-Signal` goes inside a `User-agent` group. Above the first `User-agent` line it attaches to nothing. `geo-check.sh` fails that.
2. A crawler that has its own group ignores the `*` group completely. If you add a named group, copy into it every line that should still apply: the `Content-Signal` line and any `Disallow` for private paths.
3. A named group that only says `Disallow: /` is a block. The signals no longer matter for that crawler.
4. A `Disallow` does not remove an address from search results. An address linked from elsewhere can stay listed. Use an `X-Robots-Tag: noindex` header or a `noindex` meta tag for that (the Voyage app's `/admin` and `/setting` need it; the header change exists only as an uncommitted edit in the previous operator's clone; not recorded (the previous DevRel's notes), ASK: Rahul).
5. `Sitemap:` lines may sit anywhere in the file. Leave them as they are unless the sitemap moved.

## To allow or block one named crawler
This procedure is inferred from the rules above and from how the Voyage app is built. It was not run on a MOI site. A policy change needs a decision before anyone edits: ASK: Rahul (see "Policy" below).
1. Edit the file in each repo that should change: `static/robots.txt`, or `docs/source/_extra/robots.txt` for js-moi-sdk. Each site has its own copy.
2. To block `<Name>`: add a group.
```
User-agent: <Name>
Disallow: /
```
3. To allow `<Name>` with its own rules: add `User-agent: <Name>`, then every line the `*` group has (including `Content-Signal` and `Allow: /`).
4. Change nothing else in the file.
5. Verify locally that the file is copied (`build/robots.txt`, `verify-locally.md`), open the pull request (`moi-devrel/ship`, GATE), and after the merge run `bash "$SKILLS/moi-docs/geo/scripts/geo-check.sh" https://<domain>` (`after-merge.md`). The check shows the group count and whether any named group lacks a signal.
6. Then confirm by name, from any folder: `curl -s -o /dev/null -w '%{http_code}\n' -A "<Name>/1.0" https://<domain>/`. A 200 for an allowed crawler is what the style guide asks for. This request comes from your address, not the vendor's range, so it cannot prove what the real crawler is served.

## Crawler names
The style guide's list of crawlers it wanted allowed: GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot, Claude-User, Claude-SearchBot, PerplexityBot, Perplexity-User, Google-Extended, Applebot-Extended and CCBot. Notes from `moi-blog/references/geo.md` (pages read 2026-10-02):
- OpenAI lists `OAI-SearchBot` for search results, `GPTBot` for training and `ChatGPT-User` for pages a ChatGPT user asks it to open, each set separately.
- Google says `Google-Extended` controls training of future Gemini models and grounding in Gemini apps, and has no effect on Google Search. It is a robots token only, so you cannot test it with `curl -A`; read `robots.txt` instead.
- Names and meanings change. Read the vendor's crawler page again before you rely on a row.

## Where the other sites stand
| Site | Robots today | Notes |
|---|---|---|
| docs, voyage-docs, coco-docs, js-moi-sdk docs | One `*` group with the signal, on `main` since the merges. Live on 2026-10-03, before the merges: no file on docs or voyage-docs, Cloudflare's text only on cocolang.dev, an HTML page on js-moi-sdk (#150 is still open) | Merge state: `the-layer.md` |
| Voyage app | `next-sitemap.config.js` builds one group per crawler (14 names, including `*`), each repeating `Disallow: /admin/` and `/setting/`, and no `Content-Signal`. A named group must repeat the private paths, which is why it is built this way | Live file names `voyage.ai` as host and sitemap until PR #447 merges |
| moi.technology and blog.moi.technology | Seven groups, one per crawler, no `Content-Signal` (read live 2026-10-03). PR #57 (merged 2026-10-05) replaces the website file with the single group and signal; the reading is from before the merge | The apex file also lists the blog's sitemap, because a sitemap cannot list another host's addresses |
| cocolang.dev | The live file is a 24-line comment block from Cloudflare, with no group and no `Content-Signal` line (read 2026-10-03). Whether Cloudflare adds its text on top of the repo's file after the merge is unknown | ASK: Rahul, who can read the zone's settings |

## Policy
`ai-train=yes` was set "per policy decision" (commit b4d4810, written 2026-09-09; the rebase of 2026-10-01 reset its committer date). The record does not say who decided or whether it still holds. Treat the three values as a policy question: ASK: Rahul before any change. A signal is a request that crawlers may honour. It does not block anyone, and the file alone does not change what a Cloudflare setting does: a zone-level block overrides every file (cocolang.dev, until 2026-09-09).

## The style guide disagrees with the file
`DOCS-STYLE-GUIDE.md` (on `main` since PR #124 merged on 2026-10-13; committed 2026-09-22) still describes a list of two-line blocks, one per crawler, and says the file "allows the AI crawlers we care about". The committed file is newer (2026-10-01) and has one group naming no crawler. Trust the file. Say so in a follow-up pull request and ask the author to correct the guide. The `DOCS-STYLE-GUIDE.md` appendix step 3 repeats the old wording.

## Not yet known
- Who set the policy, and whether `ai-train=yes` still stands. ASK: Rahul.
- Whether to give the Voyage app and the apex the same single-group file. The Voyage layout is deliberate and PR #447 keeps it. ASK: Gokul.
