# After a GEO or docs pull request merges: the manual steps nothing automates

Facts are as of 2026-10-03, with the merges noted: voyage-docs #5, coco-docs #12 and the website #57 merged on 2026-10-05, moidocs #124 on 2026-10-13. The run after the merge below is therefore the live path now. A merge to `main` of a docs repo publishes through Cloudflare Pages with no manual deploy. Nothing below runs by itself: the weekly health check and the CI gate were removed on purpose on 2026-09-09. A step marked GATE needs the operator's explicit yes first. Pull request mechanics are `moi-devrel/ship`. Back to `../GUIDE.md`.

## Before the merge (history for #124, #5, #12, #57 and #150, merged; still the checklist for voyage #447 until it is deployed)
1. Merge order: moot for the pair that merged. The website's #57 merged on 2026-10-05 and moidocs #124 on 2026-10-13, and the website links to `docs.moi.technology/.well-known/agent-skills/index.json`, which answered 404 until #124 was live (read 2026-10-03), so the link could not resolve in between (inferred). Check that it answers 200 now. ASK: Rahul who merges each repo and who approves; the evidence does not say.
2. Update stale pull request bodies. As of 2026-10-02 three were wrong: `moidocs` #124 and `voyage-docs` #5 say each AI crawler is listed in `robots.txt` (it is now one group, `crawlers.md`), and `js-moi-sdk` #150 says it adds `docs/DOCS-GEO-STANDARD.md`, which commit 2c6c861 (in `js-moi-sdk`) removed. #124 and #5 have merged since; #150 has merged since (2026-10-14). Editing a body is a GATE (`moi-devrel/ship`).
3. `moidocs` #124: Rahul's change request (no Launchpad docs in protocol docs) was met by commit 75f608b and had no reply on 2026-10-02; #124 merged on 2026-10-13 and whether a reply was ever sent is not recorded. On an open PR, replying and re-requesting review is a GATE. Draft it for the operator to send.
4. The `launchpad.moi.technology` `llms.txt` pointed at `docs.moi.technology/docs/build/launchpad/`, which 404ed on 2026-10-03. It now points at `launchpad.moi.technology/docs` (Launchpad docs, PR #31); confirm that with the live check. Do not merge docs changes that remove pages without a search for every file that links to them (`discovery-files.md`).

## The run after the merge
| # | Step | What to do | Done when |
|---|---|---|---|
| 1 | Wait for production | Cloudflare Pages builds `main` to production (projects `moichain-docs`, `cocodocs`, `voyage-docs`). No action. How long it takes is not recorded | The home page serves the new build |
| 2 | Run the live check | `bash "$SKILLS/moi-docs/geo/scripts/geo-check.sh" https://<domain> --follow --indexnow-file <key file name>`. Find the name with the command under this table. Do not paste the name into chat or a file | No FAIL. A reason is written beside every WARN you keep |
| 3 | Same checks by hand | `curl -s -o /dev/null -w '%{http_code} %{content_type}\n' https://<domain>/robots.txt` wants `200 text/plain`, the same for `/llms.txt`, and `curl -s -o /dev/null -w '%{http_code}\n' -A "GPTBot/1.0" https://<domain>/` wants 200, repeated with `ClaudeBot/1.0` and `PerplexityBot/1.0`. Never trust a bare 200 on js-moi-sdk | Status and content type agree |
| 4 | coco-docs only | The three commands under this table. The two redirects were seen on the preview on 2026-10-03 and match `static/_redirects`. Fifteen old addresses return not found on purpose: the template's sample blog and sample page | The redirects and the canonical hold |
| 5 | coco-docs redirect rule | GATE. In the Cloudflare dashboard, a 301 from `cocolang.docs.moi.technology/*` to `https://cocolang.dev/*`. The mirror still answers 200 with a duplicate (2026-10-03). A dashboard change to a shared system, so the operator or the account owner does it. ASK: Rahul who owns the account | The mirror redirects |
| 6 | js-moi-sdk only | `curl -sI https://js-moi-sdk.docs.moi.technology/nonexistent-page` returns 404 once `404.html` is deployed. `/robots.txt` is `text/plain` | The soft 200 is gone |
| 7 | Search Console | GATE. Per property, submit the sitemap (usual path: Sitemaps, enter `sitemap.xml`, Submit; menus change). The 4 October dependency list (now only in git history) names Search Console only under the MOI Website heading, so a property per docs host is not recorded in the handover docs. js-moi-sdk's submission replaces a stale `v0.7.0-rc1` index. Which properties exist and who owns them is not recorded. ASK: Rahul | The sitemap shows no error. Note the date |
| 8 | Bing Webmaster Tools | GATE (granting OAuth). "Import from Google Search Console" takes one sign-in and brings verification. The previous operator did this on 2026-09-09 for the properties then listed; a property added later needs its own import (inferred). The sweep status doc says Bing's index feeds ChatGPT search and Copilot; that was not checked here | The property is listed in Bing |
| 9 | IndexNow | GATE: it sends addresses to search engines. Nothing submits the key file automatically. The command the previous operator used is not recorded (the previous DevRel's notes; ASK: Rahul). The protocol is below | Step 2 passes `indexnow-key`; the operator has submitted, or has decided not to |
| 10 | Record | Fill `templates/audit-report.md` with the date, the totals line of step 2 and what is left. Keep it in a self-hiding audit folder (`audit-method.md`, rule 2). Search Console and Bing results arrive later and only the operator can read them | The operator has the file path |

Commands for steps 2 and 4, each run from any folder except the first, which runs from the repo root:
```
ls static | grep -E '^[0-9a-f]{32}\.txt$'
curl -sI https://cocolang.dev/docs/book/ | grep -i -E '^(HTTP|location)'
curl -sI https://cocolang.dev/docs/book/language/state/ | grep -i -E '^(HTTP|location)'
curl -s https://cocolang.dev/ | grep -o 'rel="canonical" href="[^"]*"'
```
The first prints the IndexNow key file name (the three Docusaurus sites keep it in `static`; the website, the Voyage app and the Launchpad in `public`; Sphinx in `docs/source/_extra`). The next two want `301` and `location: /` then `location: /book/language/state/`. The last wants `https://cocolang.dev/`.

## IndexNow, from the protocol page
Read on 2026-10-03 at indexnow.org (documentation and FAQ). The key is a text file at the site root whose name is the key, and the site's pages must be reachable. A submission names the host, the key and the addresses. The global endpoint `https://api.indexnow.org/indexnow` shares a submission with the IndexNow search engines the FAQ lists (Bing, Naver, Seznam.cz, Yandex, Yep, Amazon). Google is not on that list. A 200 answer only means the request was received.
This shape is built from the protocol page. It is not a command anyone ran here. Running it sends addresses to search engines, so it is a GATE (step 9):
```
KEY='<the key file name without .txt, typed by the operator>'
curl -sS -X POST "https://api.indexnow.org/indexnow" -H "Content-Type: application/json; charset=utf-8" --data "{\"host\":\"docs.moi.technology\",\"key\":\"$KEY\",\"urlList\":[\"https://docs.moi.technology/\"]}"
```
The key is public by design (the file is committed and served). Keep it out of chat, notes and any file you write, and never print it.

## If a check fails
| Symptom | Likely cause | Fix, and who |
|---|---|---|
| `/robots.txt` 404 on a docs host | `static/` was not copied, or the Pages project's build command is not `npm run build` | Read the Pages build log. ASK: Rahul for Cloudflare access |
| 200 `text/html` for a machine file | The file is missing and the host's fallback page answers (js-moi-sdk, the website) | Add the file, then check the content type |
| 403 or 503 to a crawler name | A zone-level bot or WAF setting. cocolang.dev was blocked this way until 2026-09-09, when the previous operator switched a zone setting off; its name was not recorded | The account owner changes it. ASK: Rahul. Re-run step 2 after |
| Catalog served as `application/octet-stream` | `_headers` is not applied. A VM-served host ignores it | On Pages, fix `_headers`. On the website's VM, nginx needs an `add_header` line. ASK: Upendhar |
| Sitemap or canonical names `wiki.moi.technology` | `url` in `docusaurus.config.js` is wrong, or an old build is served | Fix `url`, rebuild, re-check |
| A stub appears in `llms.txt` | The generator lists every page and does not skip `noindex` ones (read in `generate-llms.mjs`, 2026-10-03) | A change to the generator. ASK: Gokul. Do not hand-edit `llms.txt` |
| Canonical has no slash and the host redirects to the slash form | `trailingSlash` unset (`traps.md`) | Set it in `docusaurus.config.js` and `llms.config.json` together, in a pull request |

## Not yet known
- The exact IndexNow command and whether it was ever run for the six sites. Not recorded (the previous DevRel's notes); ASK: Rahul.
- Which Search Console and Bing properties exist, and who owns them. ASK: Rahul.
- Which Cloudflare setting blocked crawlers on cocolang.dev. ASK: Rahul.
- Whether the previous operator's backup branches (`geo-fixes-before-rebase-oct1` and similar) matter to anyone. They exist only in his clones. Not recorded (the previous DevRel's notes); ASK: Rahul before anyone deletes them.
