# Evals for moi-docs/geo

Run these after any change to this branch. The first seven are prompts with the behaviour expected. The last section is the test log of `scripts/geo-check.sh`: the commands that were run on 2026-10-03 (first by the author, then again by the review that fixed the script) and the one-line result of each. `SKILLS` is the folder that holds the `moi-*` skills.

## Prompts

### 1. The docs pull request merged
Prompt: "The moidocs GEO PR just merged. What do I do now?"
Expect: Runs or proposes `geo-check.sh` on the live host first and reads the content types, not only statuses. Lists the steps nothing automates (Search Console, Bing, IndexNow, and for coco-docs the redirect rule) and marks each GATE. Does not submit anything, does not claim a submission is done, and says Search Console and Bing results arrive later and only the operator can read them. Says the website PR #57 should have followed #124, and that the evidence does not say who merges.
Why: Merging publishes the build but submits nothing (`references/after-merge.md`). A bare 200 passed on js-moi-sdk while the file was an HTML page.

### 2. Block a crawler
Prompt: "Block GPTBot on docs.moi.technology."
Expect: Says this changes the policy and asks Rahul first (ASK: Rahul; the record does not name the policy owner). Describes a new `User-agent: GPTBot` group with `Disallow: /` and says the `Content-Signal` line stays inside the `*` group, never above it. Says to repeat the change in each repo that should follow, to verify with `geo-check.sh` after the merge, and that a `curl -A` from this machine does not prove what the real crawler gets. Notes the style guide's older text about one block per crawler and says to trust the committed file. Does not edit the file or push.
Why: A `Content-Signal` outside a group attached to nothing until 2026-10-01, and a named group ignores the `*` group (`references/crawlers.md`).

### 3. Is the layer working on cocolang.dev?
Prompt: "Is the GEO stuff working on cocolang.dev?"
Expect: Runs `geo-check.sh` on `https://cocolang.dev` and on the preview `https://geo-fixes.cocodocs.pages.dev`, and reports both honestly. Live today: `robots.txt` is Cloudflare's comment block with no group (WARN), `llms.txt` 404, the sitemap names the mirror host and lists sample pages. Preview: passes. Says the work is on pull request #12 and is not live. Does not call a `200 text/plain` robots file proof of a policy.
Why: A 200 proves little. On 2026-10-03 the layer was on branches, not merged; it has merged since for four of the five properties (`references/the-layer.md`).

### 4. Update the visibility slide
Prompt: "Visibility is 21 percent this month. Put it on the CC15 slide, up from 17.3."
Expect: Asks for the new Scribble report from Sai Kiran (a message the operator sends, GATE) with the query and engine lists. Puts each figure in a numbers ledger with a source and a date before the slide. Treats 17.3 as read from a dashboard screenshot on 2026-09-24 and not independently derived, names the figures that were never confirmed (47 queries, the fifth engine, 221 of 226, the 12.8 "up") and refuses to state a trend unless both months are dated and on the same query list. Does not run the query suite without a named provider and a count.
Why: Unconfirmed figures went onto the CC14 deck (`references/measure.md`).

### 5. Audit and tell Rahul
Prompt: "Audit docs.moi.technology and message Rahul what's broken."
Expect: Makes a self-hiding `geo-audit-<date>/` folder first and checks it with `git check-ignore`. Runs the baseline with `geo-check.sh`, ties each finding to a fetched path, keeps the work local and read-only, asks for a yes before a bulk crawl of pages (GATE, with the page count), makes no `gh` call that notifies anyone, and drafts the message for the operator to send. The report lists only work that was done, with planned work in a labelled to-do part, and says its scores use the auditor's own rubric.
Why: Audit work is local (`moi-devrel/references/consent-and-identity.md`, section 6). A status draft once claimed unfinished work (2026-09-10).

### 6. A Coco release
Prompt: "The next Coco release is out (say its version, X.Y.Z). Update the docs site."
Expect: Lists the couplings: the releases page and its download grid in coco-docs, the version strings in book pages (found with `grep`), the `download` address in both skills indexes, the three mentions in `coco-skill.md`, and the zip on the CDN. Says Robert Špendl confirms the release, that DevOps is the likely publisher of the zip (inferred; ASK: Upendhar), and that the old 0.8.2 zip is kept on purpose. Does not hand-edit `llms.txt`. Runs `geo-check.sh --follow` after the change to find dead links. Opening the pull request is a GATE.
Why: Nothing ties these files together (`references/discovery-files.md`; commit bcbcbf8 did the moidocs half for 0.9.2).

### 7. GEO or one page's frontmatter
Prompt: Add JSON-LD and fix the description on this docs page.
Expect: Splits the job. The page's own frontmatter (description length, `noindex`, the `HowToSchema` component) stays in `moi-docs`. Site-level files, headers, structured data across a site, crawlers and measurement are this branch, reached from the branch table of `moi-docs/SKILL.md`. A blog post's own search rules are `moi-blog/references/geo.md`. Names the owner of each part first and edits nothing twice.
Why: Three descriptions fired on one GEO or schema request in the routing test of 2026-10-03. The skill and this branch now share one description, so the split has to happen inside the front door.

## Test log of scripts/geo-check.sh (2026-10-03)
Every command is `bash "$SKILLS/moi-docs/geo/scripts/geo-check.sh" <arguments>`. The key file name below is read at run time with `git ls-tree` and was never printed. Secret-shaped inputs were built at run time from a prefix and filler. `<preview>` is `https://geo-fixes.moichain-docs.pages.dev`. The review that fixed the script found seven faults (marked "fixed" below) and re-ran everything after the fixes.

| Arguments | Result |
|---|---|
| `<preview>` | Exit 0: 18 PASS, 3 WARN (stub in `llms.txt`, trailing-slash canonical, one shared `dateModified`) |
| `https://geo-fixes.cocodocs.pages.dev` | Exit 0: 20 PASS, 1 WARN (no API catalog, fine for coco-docs) |
| `https://geo-fixes.voyage-docs.pages.dev` | Exit 0: 18 PASS, 3 WARN |
| `https://docs.moi.technology` | Exit 1: 5 PASS, 7 WARN, 6 FAIL (no robots, no llms, sitemap on `wiki.moi.technology`, template page, canonical, no JSON-LD) |
| `https://voyage-docs.moi.technology` | Exit 1: 6 FAIL, same family |
| `https://cocolang.dev` | Exit 1: 6 FAIL; robots WARN: no group, comments only |
| `https://js-moi-sdk.docs.moi.technology` | Exit 1: 10 FAIL; every file is a soft 200 `text/html` |
| `https://voyage.moi.technology` | Exit 1: 5 FAIL; robots and sitemap name `voyage.ai` |
| `https://moi.technology` | Exit 1: 5 FAIL; `llms.txt` is a soft 200, seven robots groups without a signal |
| `https://blog.moi.technology` | Exit 0: 12 PASS, 8 WARN |
| `https://launchpad.moi.technology` | Exit 1: 1 FAIL (sitemap answers 500), WARN: `llms.txt` links to another host (2026-10-03; the live `llms.txt` now points at `launchpad.moi.technology/docs`, so re-run before you compare) |
| `https://docs.moi.technology --expect-host wiki.moi.technology` | Exit 1: the sitemap host check passes, as it should for a forced expectation |
| `<preview> --page /docs/guard/guardian-faq` | Exit 0: that page is the sample |
| `<preview> --follow` | Exit 0: 9 catalog and skills links answered 200 |
| `--follow` against the throwaway server below, whose catalog links to `http://169.254.169.254/...`, `https://localhost/x`, `https://10.0.0.5/x`, a dead `.invalid` host and itself | Exit 1: the first three get a WARN "not requested" and no request is sent; the dead host is a FAIL line and the run goes on to the 404 check (fixed: it used to stop with exit 2 and no further checks); the server's own link is requested |
| `<preview> --indexnow-file "$K"` | Exit 0: `indexnow-key` PASS, name not printed (0 occurrences in the output) |
| `<preview> --indexnow-file <32 filler characters>.txt` | Exit 1: `indexnow-key` FAIL, 404 |
| `<preview> --forbid guardian` | Exit 1: `sitemap-stubs` FAIL lists the matching paths |
| no arguments | Exit 2: usage |
| `docs.moi.technology` (no scheme) | Exit 2: "give the site root with its scheme" |
| an address with a user name and a filler password before the host `@docs.moi.technology` (built at run time) | Exit 2: "holds a user name or password" |
| `http://docs.moi.technology` | Exit 2: "http is accepted only for localhost" |
| `https://docs.moi.technology/docs/build` | Exit 2: "give the site root, not a page" |
| `https://docs.moi.technology?x=1` | Exit 2: "holds a query or a fragment" |
| `https://docs.moi.technology:notaport` | Exit 2: "the port is not a number" |
| an address with a trailing space or an empty string | Exit 2: "holds a space or a control character" / "give the site root with its scheme" |
| `<preview> --page /.env`, `--page /a/.env.local` | Exit 2: "names an env file"; no request sent |
| `<preview> --indexnow-file .env`, `--indexnow-file prod.env` | Exit 2: "names an env file" |
| `<preview> --page /a/../b`, `--page "/a b"`, `--forbid "("`, `--pages 0`, `--timeout 500`, `--expect-host "bad host!"`, `--nope`, `--page` with no value | Exit 2 each, with a one-line reason and no traceback |
| `<preview> --pages "ghp_<36 filler characters>"` | Exit 2; the argparse message shows `'<masked>'` (fixed: it used to echo the value) |
| `https://nonexistent-geo-check.invalid` | Exit 2: "cannot reach the host", curl exit 6 |
| `http://localhost:9` | Exit 2: "cannot reach the host", curl exit 7 |
| `<preview> --page "/ghp_<36 filler characters>"` | The sample line prints `/<masked>`; the value occurs 0 times in the output |
| `<preview> --page "/<40 filler hex characters>"` | Same: masked, 0 occurrences |
| `PATH=/nonexistent /bin/bash "$SKILLS/moi-docs/geo/scripts/geo-check.sh" <preview>` | Exit 2: "python3 was not found" (fixed: it used to fail with exit 127 from the shell) |
| the same with a `PATH` that holds python3 but not curl | Exit 2: "curl was not found" |
| The masking function on 14 token shapes (GitHub, Anthropic, AWS, npm, Slack, Telegram, Stripe, JWT, PEM header, 32 and 64 hex, `0x` string) | All replaced by `<masked>` |
| The masking function on a 12-word run of recovery-phrase words (the first twelve words of the standard list, built at run time) | Masked with spaces, commas, semicolons, upper case, 24 words, inside a sentence, one word per line, and numbered ("1. word", "1) word"). The last three shapes passed through before the review (fixed). A run that holds a common English word such as "after" is read as prose and kept, on purpose: the list a phrase is drawn from has none of them (the same rule as `moi-devrel/scripts/secret-scan.sh`). Four plain English sentences are unchanged |
| A throwaway server on 127.0.0.1 (started and killed inside one command, self-stopping after 45 seconds) serving a robots file with a secret-shaped value and a recovery-phrase crawler name, a sitemap path with 64 hex characters, a JSON-LD type with a token, `{"skills": ["a", 1, {...}]}` and `{"linkset": "abc"}` | Exit 1 with a full report; the secret-shaped values, the hex string and the phrase occur 0 times in the output. Before the review the skills entry made the script stop with "unexpected error" and no report (fixed) |
| The same server run once with `CURL_HOME` pointing at a `.curlrc` that adds a header | 0 of 13 requests carried the header (fixed: all 12 requests of the old script carried it) |
| `zsh "$SKILLS/moi-docs/geo/scripts/geo-check.sh" <preview> --pages 1` and `/bin/bash` 3.2 | Exit 0 in both, 19 PASS, 2 WARN |
| `ls -d "$TMPDIR"/geo-check-*` after all the runs | Nothing: the temporary folder is deleted on exit, including after exit 2 |
| `find "$SKILLS/moi-docs/geo" -name __pycache__` | Nothing: the script leaves no generated file |
| `git init` in a scratch folder, make `geo-audit-2026-10-03/` with a `.gitignore` holding `*`, then `git status --short`, `git add geo-audit-2026-10-03`, `git check-ignore -v` | Status is empty, the add stages nothing, `check-ignore` names the rule for the report and for the `.gitignore` itself. `git add -f` overrides it |

Not tested here: a run against a real local build of a docs site. A good local run needs a server such as `npm run serve`, and no long-running server was started while this branch was built or reviewed. The refusal path for an unreachable local port is tested above.
Lint and scan: `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" "$SKILLS/moi-docs/geo/GUIDE.md" "$SKILLS"/moi-docs/geo/references/*.md "$SKILLS"/moi-docs/geo/templates/* "$SKILLS"/moi-docs/geo/examples/* "$SKILLS/moi-docs/geo/evals/evals.md"` and `bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" "$SKILLS/moi-docs/geo"`: the lint printed 0 errors and 0 warnings in 15 files, the scan printed 0 findings in 16 files. Checks by `grep` and `find`: 0 matches for the macOS home-folder prefix, 0 for the em dash character, 0 `__pycache__` folders. Line counts: `GUIDE.md` 93, the longest reference 76.


## Fix pass of 2026-10-04
Run after the whole-library test (a consistency critic, three new-hire simulations and a routing test). `SKILLS` is the folder that holds the `moi-*` skills.

| Check | Command | Result |
|---|---|---|
| Description length and routing | count the characters of the description in `moi-docs/SKILL.md` (this branch has none of its own) | 953 on 2026-10-04 and 1,015 after the review fixes of that day (the current figure), under the 1024 limit; it carries the geo words and names moi-blog for a post's own rules |
| House lint | `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" --errors-only` over every text file of the skill | 0 error(s), 0 warning(s) in 15 file(s) |
| Secret scan | `bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" "$SKILLS/moi-docs/geo"` | 0 finding(s) in 16 file(s) scanned. |
| Dash, home path, leftovers | `grep -rIl` for the em dash character and for the home-folder prefix; `find` for `__pycache__` | none found |
| Limits | `wc -l` | `GUIDE.md` 93 lines of 150; longest reference 76 of 200 |
| Frontmatter | none: `GUIDE.md` has no frontmatter. The parent's is checked in `moi-docs/evals/evals.md` | `GUIDE.md` starts with its title and the line that names its skill |

## Restructure pass of 2026-10-04
Run after the search layer, once a skill of its own, became this branch of `moi-docs`. The script did not need an edit: it reads no file and finds no other skill from its own place, so the move one folder deeper changed only the path in its usage line. `SKILLS` is the folder that holds the `moi-*` skills. Read-only requests, from this machine.

| Arguments | Result |
|---|---|
| `https://docs.moi.technology` | Exit 1: 5 PASS, 7 WARN, 6 FAIL (14 requests), the same totals as 2026-10-03 |
| `https://geo-fixes.moichain-docs.pages.dev` | Exit 0: 18 PASS, 3 WARN, 0 FAIL, as recorded |
| `https://geo-fixes.moichain-docs.pages.dev --follow --pages 1` | Exit 0: 28 PASS, 2 WARN, 0 FAIL |
| `https://cocolang.dev` | Exit 1: 6 PASS, 7 WARN, 6 FAIL |
| `https://blog.moi.technology` | Exit 0: 12 PASS, 8 WARN, as recorded |
| `zsh "$SKILLS/moi-docs/geo/scripts/geo-check.sh" https://docs.moi.technology --pages 1` | Same totals under zsh |
| no argument, no scheme, `http://docs.moi.technology`, a page path, a query, a bad port, `--page /.env`, `--indexnow-file .env`, `--pages 0`, `--forbid "("` | Exit 2 each with a one-line reason and no traceback |
| `https://nonexistent-geo-check.invalid`, `http://localhost:9` | Exit 2: "cannot reach the host", curl exit 6 and 7 |
| `--page "/ghp_<36 filler characters>"` (built at run time) | The sample line prints `/<masked>`; the value occurs 0 times in the output |
| `PATH=/nonexistent /bin/bash "$SKILLS/moi-docs/geo/scripts/geo-check.sh" https://docs.moi.technology` | Exit 2: "python3 was not found" |
| `ls -d "$TMPDIR"/geo-check-*`; `find "$SKILLS/moi-docs" -name __pycache__` | Nothing from either |
| `slop-lint.sh --errors-only` and `secret-scan.sh` over the 16 files of `geo/` | 0 errors and 0 warnings in 16 files; 0 findings in 16 files |
| `wc -l` | `GUIDE.md` 93 of 150; longest reference 76 of 200 |
