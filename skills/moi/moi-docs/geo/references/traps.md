# Traps: results that are wrong with no error

Facts are as of 2026-10-03. Each row is something that happened or was observed, with its date. The rule is what to do about it. Page-level traps (quoted colons, headings, anchors, names) are in `moi-docs/references/traps.md`; only the ones that break the layer are repeated here. Back to `../GUIDE.md`.

## The build
| Looks right | Actually | Rule |
|---|---|---|
| The build is green | Only broken route links stop it. Links to `.md` files warn, and heading anchors are not checked on Docusaurus 2.1 (inferred) | Read the `generate-llms:` and `inject-schema:` lines, not only the exit code |
| A blank line above the first `---` | The site ignores the whole frontmatter, and the generator's parser needs `---` at position 0 | Start the file with `---` |
| A title or description over two YAML lines | The generator reads one-line values only (inferred; every page today uses one line) | Keep both on one line |
| A new component in a page | Raw JSX leaks into `llms-full.txt` and the `.md` copies. It did: 265 lines, fixed in f639f41 | Add the component to `DROPPED_COMPONENTS` or the `components` map |
| A stub marked `noindex` | It is out of the sitemap but still in `llms.txt`, `llms-full.txt` and the `.md` copies (PR #124 preview, 2026-10-03: `networks`) | Check all three. A generator change is needed; ASK: Gokul |
| A stub finished, mark left on | It never appears in search | Remove the mark in the same change |
| The sitemap has no stub | The sample page of the template can still be there (`markdown-page` in the docs sitemap, 2026-10-03) | Read the sitemap addresses, every time |
| `dateModified` is present | On a shallow clone it is the newest commit's date for every page. A history rewrite also moves dates (`verify-locally.md`) | Compare one untouched page with `git log -1 --format=%cI -- <file>` |
| JSON-LD present | Built from built HTML it came out entity-encoded ("MOI&#x27;s") until commit 859b3ee, and `<` must be escaped | `geo-check.sh` warns on entities. Escape `<` as `inject-schema.mjs` does (`<`) |
| A rebase finished | It can restore an older copy of a page another pull request updated. Commit 0899368 fixed this for `submit-ixn.md` | Diff the changed pages against `main` after every rebase |
| One fix in one generator | Three variants exist: moidocs and voyage-docs (identical), coco-docs (newer), js-moi-sdk (Python) | `diff` the pair, carry a fix across by hand |
| coco-docs `static/` | The generator deletes every `.md` under it on each build | Never keep a hand-written `.md` there |
| js-moi-sdk generated files | They are committed, so a docs change adds thousands of lines | Review `generate_llms.py`, not the output |
| js-moi-sdk page added | `.. meta::`, the `PAGES` row and the sitemap line are three copies that nothing compares | Check all three; `toctree` too |
| `html_baseurl` set in Sphinx | It adds `.html`, so every canonical points at a 308 redirect | Leave it unset; the base address lives in `layout.html` |

## Addresses and hosts
| Looks right | Actually | Rule |
|---|---|---|
| `trailingSlash` left at its default | moidocs and voyage-docs configs do not set it. On the PR #124 and #5 previews the host answers 308 from `/docs/build/json-rpc` to `/docs/build/json-rpc/` while the canonical has no slash (2026-10-03). The wallet docs show the same on the live host. coco-docs sets `true` and its canonical matches | Set it in `docusaurus.config.js` and `llms.config.json` together. The style guide's appendix step 2 says this. Whether the mismatch hurts ranking is not known |
| `url` in the config | A wrong value misdirects the whole site. voyage-docs and moidocs named the dead `wiki.moi.technology`; the Voyage app named `voyage.ai` | Read canonical and sitemap on the live host |
| A 200 answer | js-moi-sdk, the website and the Agent Explorer answer 200 to a missing file with an HTML page | Check the content type and the first line of the body |
| A preview that looks wrong | Previews send `x-robots-tag: noindex`, and their robots and sitemap name the production host. Both are by design | Do not "fix" them. Judge against the production host, as `geo-check.sh` does |
| The mirror host | `cocolang.docs.moi.technology` still answers 200 with a duplicate (2026-10-03) | The redirect rule in `after-merge.md` |

## Robots and crawlers
| Looks right | Actually | Rule |
|---|---|---|
| A `Content-Signal` line at the top of the file | Above every `User-agent` line it attaches to nothing, and a per-crawler group does not inherit it. Fixed on 2026-10-01 (7d58640) | One group, the line inside it (`crawlers.md`) |
| A group added for one crawler | That crawler now ignores the `*` group | Copy every line it needs into the group |
| `Disallow` for a private path | The address can stay in the index if linked | Add `X-Robots-Tag: noindex` |
| `curl -A GPTBot` returns 200 | It comes from your address. It proves the name is not refused here, not what the real crawler gets | Say so in the report |
| Files are right | A zone-level Cloudflare setting overrides them. cocolang.dev returned 403 to AI crawlers until 2026-09-09 | Run the crawler check after every Cloudflare, WAF or hosting change |
| The style guide says one block per crawler | The committed file is one group and is newer | Trust the file; fix the guide |
| cocolang.dev robots after the merge | Cloudflare's managed text is the only content today; whether it will be added to the repo file is unknown | Read the live file after the merge |

## Discovery files
| Looks right | Actually | Rule |
|---|---|---|
| `/.well-known/api-catalog` exists | It has no extension and goes out as `application/octet-stream` unless `_headers` forces `application/linkset+json` | Check the content type |
| `_headers` is in the repo | Only Cloudflare Pages reads it. The website is served by nginx on a VM, which ignores it; its two links are declared in `index.html` instead | A header on the VM needs an nginx line. ASK: Upendhar |
| The skills index names a zip | A release changes the zip, the index, the skill page and the book pages, and nothing links them | `discovery-files.md` |
| A docs section was removed | The Launchpad's `llms.txt` named its page on 2026-10-03 and it 404ed; it now points at `launchpad.moi.technology/docs` | Search every clone and the `sarvalabs` organisation for the removed path |
| An `agentInstructions` line | An agent trusts it over its own memory | Keep it true |

## Process and reporting
| Looks right | Actually | Rule |
|---|---|---|
| Add the CI gate or the weekly cron back | Both were removed on purpose on 2026-09-09 (commits d0b6a19 and 77059a7, "per maintainer preference"; the commits do not name the maintainer) | Do not add them without asking. ASK: Rahul whether the preference still stands |
| The pull request body | Three of five were stale on 2026-10-02 | Re-read the body against the branch before review |
| A status message listing planned work | On 2026-09-10 a line claimed organisation descriptions were standardised. They were not, and it was removed | Done work and to-dos in separate parts |
| A score of 9 | It is the auditor's rubric on a branch, while the live sites still showed the before state on 2026-10-03 (four of the five have merged since) | State the rubric, and whether it describes live or a branch |
| Merge #57 before #124 | The website links to a file that did not exist until #124 was live. #57 merged on 2026-10-05 and #124 on 2026-10-13, so the pair is moot | For any similar pair, merge the page that creates the file first |
| IndexNow was "submitted" | Nothing submits automatically, and the 200 answer means only "received" | The operator submits; record the date |
| A visibility figure in a post | Most are unconfirmed (`measure.md`) | Do not quote them in posts |

## Not yet known
- Whether any of the previous operator's local backup branches carries work that is not on a pull request. Not recorded (the previous DevRel's notes); ASK: Rahul.
- Whether Docusaurus 2.1 on moidocs fails on a broken heading anchor. The config says `warn` for `.md` links only. ASK: Gokul.
