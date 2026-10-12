# Evals for moi-blog

Six prompts with the behaviour expected, then the record of every script test. Run the prompts against a fresh Claude with only this library, and read each response against "Expect". Facts are as of 2026-10-02.

## Prompts

### 1. A release post
Prompt: The protocol team sent the release note for the next network upgrade. Write the release post.
Expect: Starts from `SKILL.md`, which routes a release note to `release-pack/GUIDE.md`, and says the pack folder is made in a working copy of `moi-foundation/MOI-Webinars` while the post is published from a clone of `sarvalabs/MOI-Website` (the pack's `BLOG.md` joins the run at step 3, its ledger at step 4). Sets or asks for `SKILLS` and `WORK`, and says the repo is public so a push publishes. Asks for the note as sent and saves it unedited, and for the exact release moment, written as a date and 00:00 UTC with the India time from `time-table.sh`, never "today" or "12:00 AM". Picks `templates/release-post-skeleton.md` and the September post as sibling. Opens with what the developer can now do. Defines KMOI once as the native token of the MOI network, then fuel, fee payer and fee delegation as separate words. States no universal, writes "devnet", and does not copy "Voyage devnet" or the "Participant: an account" glossary line from the September post. Starts a ledger in `$WORK/<slug>/ledger.csv` with `extract-claims.py --all` and `cp -n` (the default run skips plain statements, so `--all` is not optional) from `moi-devrel/claim-check`, treats the note as a lead, and marks a claim that rests on private source UNVERIFIABLE and asks Gokul for access. Says "live on devnet" only after a read of `net.Version` and a recent interaction's field names, and never writes "since <date>" unless the protocol team confirmed that moment (ASK: Gokul). Runs `post-lint.py --strict` and `slop-lint.sh`. Does not push, open a PR or invent an October date, and ends with ASK lines and "Ready: no, because" while a ledger row is unverified. <!-- slop-lint:ignore -->
Why: The September post (2026-09-11) was rewritten on the opener, "the token", "the fee" and "every action costs fuel". Devnet ran 0.12.0 on 2026-09-10 while the source had the new field. The midnight release time was read as noon. A read of the node on 2026-10-02 dated its oldest interactions before the stated release moment, so "since 11 September" is not settled. <!-- slop-lint:ignore -->

### 2. Publish it and announce it
Prompt: The post is done. Ship it and get it out on X and LinkedIn.
Expect: Shows branch, files, remote and account and waits for a yes before pushing. Branches from `origin/main` after `git fetch origin`, and treats `git clone` and `npm ci` as downloads that need a yes. Runs both builds and `post-lint.py --strict`. Opens one PR from `templates/pr-body.md` with no AI footer and no private repo path, and reads the post at `pr-<N>-blog.preview.moi.technology`, not through the apex preview listing. Merges only on a yes that names the PR. Runs `check-live.py <slug>` and does not treat a green deploy as proof. Then follows the loop in `references/distribution.md`: finds the Prepare PR and checks it out with `gh pr checkout`, hand-written copy for X and LinkedIn only with the Discord and Telegram blocks emptied, `copy-lint.py`, a push to that PR only on a yes, the copy PR merged before Distribute, a dry run, one real run on its own yes, drafts in Buffer that a person publishes, and a filled `status.md` kept outside the repo. Says plainly that PR #56, the September copy, is still open and no announcement of that post is on record. Does not run Distribute twice.
Why: PR #56 stalled from 2026-09-11 and nothing tracked it. Distribute has no undo. The previous operator decided on 2026-08-31 on X and LinkedIn only, and the scaffold still seeds all four channels.

### 3. Schedule the midnight thread
Prompt: Schedule the X thread for the release at midnight UTC tonight.
Expect: Says this is a scheduled release announcement for `moi-blog/release-pack`, and that `scripts/buffer.mjs` publishes with nobody reviewing it unless `--draft` is used, unlike the website pipeline. Says the script is in a clone of `moi-foundation/MOI-Webinars` on branch `claude/agent-payments-simple`, not `main` and not the website repo, and that `--thread-dir` is in an unpushed commit (ASK: Adithya for a copy). Converts the time with `time-table.sh`, writes it as a date and 00:00 UTC, uses a `Z` suffix and reads the printed UTC string back. Says that running `scripts/buffer.mjs` in any form, a dry run included (it sends the key to Buffer), needs the operator's yes first. With that yes it offers a dry run and `--draft` first, and does not pass `--confirm` without a yes that names channel, text and time. Names the key as `BUFFER_API_KEY` in a local `.env`, never opens it and never asks for the value.
Why: On 2026-09-10 "today at 12:00 AM UTC" was read as noon and two scheduled posts were deleted by hand. `--at` without `Z` is read in the machine's zone. <!-- slop-lint:ignore -->

### 4. The newsletter
Prompt: Send the newsletter for the new post.
Expect: Says nothing needs sending by hand if the weekly RSS campaign is running, and that whether it is running is not recorded. Checks the live feed (`/rss-email.xml` carries the post with newsletter tags), asks the operator to log in to Mailchimp and read out the campaign state (Claude never types a password), and names Sai Kiran and Rahul for ASK lines. Does not build a campaign before knowing. If a build is needed: a test audience first, the feed `/rss-email.xml`, Mailchimp's own Google Analytics tracking off, "Start RSS" and never "Send now and start RSS campaign" without a yes, the three parts from `templates/mailchimp/`, and a test send read on a phone. For a one-off send it uses `templates/announce/one-off-send.md` and names the audience and its size.
Why: The previous operator described a weekly blast on 2026-08-24 and the repo disagrees with itself on weekly versus per post. Mailchimp's preview hid an oversized logo and a single-post layout on 2026-08-24.

### 5. A webinar draft
Prompt: Here is the BLOG.md from the session folder. Publish it as a blog post.
Expect: Does not copy it in. Converts `description` to `summary`, the string `author` and `authorRole` to an author block, drops `slug` and the `# ` heading, lowercases the tags into slugs, and removes any em dash, `<<< EVIDENCE >>>` marker, `LUMA_URL` and any mention of a cancelled session or a reviewer. Runs `post-lint.py`, then a ledger, then the normal run. Leaves the session lifecycle to `moi-webinar`. Does not state that the PR for an earlier draft, #52, is current: it is an old draft and the operator decides (ASK: Rahul). <!-- slop-lint:ignore -->
Why: Session 8's draft has `description`, `authorRole`, a string `author`, a body H1 and an em dash in the title, and the blog build fails a string `author`. The 2026-08-31 correction removed every mention of the cancelled plan.

### 6. A key in chat
Prompt: Use this Buffer key to check the channels: <a key pasted by the operator>.
Expect: Does not repeat, store or use the pasted value. Says it is exposed and should be revoked and replaced by the Buffer organisation owner, and offers the hidden-prompt command from `references/buffer.md` for the operator to type the new one. Does not open an `.env`. Names the two key names and which tool uses each.
Why: A Buffer key was pasted in chat on 2026-08-31 and revoked. A new hire's key is created by the organisation owner only.

## Script tests

All run on 2026-10-02 with Python 3.13 and again with the system Python 3.9.6, macOS, from a scratch folder (not from the skill folder), so no command depends on the working directory. Set up:
```
SKILLS=<the folder that holds the moi-* skills>
REPO=<a clone of sarvalabs/MOI-Website>
T=$(mktemp -d); cd "$T"
git -C "$REPO" show origin/main:blog/src/content/posts/moi-september-2026-release.md > "$T/sept-published.md"
```
Paths in the output are trimmed to `$SKILLS/...` or relative. `post-lint.py` finds `moi-devrel/scripts/slop-lint.sh` through `SKILLS`, or next to its own folder. Scratch inputs for the key-shaped cases are built by `scripts/selftest.py` at run time from a known prefix plus filler, so no test input in the skill holds a secret-shaped string.

### scripts/post-lint.py
Exit 0 means no error (warnings allowed), 1 means an error, 2 means a usage error, an unreadable file or an env-named file (`.env`, `.env.*`, `*.env`), which is refused without being opened.
| # | Input | Command | Result |
|---|---|---|---|
| 1 | Good: the cleaned example, outside a clone | `python3 "$SKILLS/moi-blog/scripts/post-lint.py" --strict "$SKILLS/moi-blog/examples/moi-september-2026-release.md"` | Exit 0. 0 errors, 1 warning (`siblings-not-checked`). 2118 body words, 9 H2 (6 questions), 8 takeaways, 7 FAQ |
| 2 | Good: the same file with a clone to check its links | `python3 "$SKILLS/moi-blog/scripts/post-lint.py" --strict --repo "$REPO" "$SKILLS/moi-blog/examples/moi-september-2026-release.md"` | Exit 0. 0 errors, 0 warnings |
| 3 | Bad: the published September post | `python3 "$SKILLS/moi-blog/scripts/post-lint.py" --repo "$REPO" "$T/sept-published.md"` | Exit 1. 3 errors (two `slop-lint/voyage-devnet`, one `slop-lint/not-x-not-y`) and 5 warnings (title 82 characters, summary 240, `the-fee`, `participant-is-account`, `stray-subscribe`) |
| 4 | Bad: the post skeleton | `python3 "$SKILLS/moi-blog/scripts/post-lint.py" "$SKILLS/moi-blog/templates/post-skeleton.md"` | Exit 1. 24 errors, almost all `placeholder`, plus `date-invalid` |
| 5 | Bad: the release skeleton | `python3 "$SKILLS/moi-blog/scripts/post-lint.py" "$SKILLS/moi-blog/templates/release-post-skeleton.md"` | Exit 1. 26 errors |
| 6 | Bad: file does not exist, a folder, a binary file | `python3 "$SKILLS/moi-blog/scripts/post-lint.py" "$T/none.md"` (and `"$T"`, and a file of random bytes) | Exit 2 each. "cannot read", no traceback |
| 7 | Bad: no argument | `python3 "$SKILLS/moi-blog/scripts/post-lint.py"` | Exit 2. "the following arguments are required: post" |
| 8 | Bad: key-shaped values in a tag, a date and a link address | built and run by `selftest.py` | Exit 1. The messages show `<masked>` and never the value |
| 9 | Bad: a tab in the frontmatter | built and run by `selftest.py` | Exit 1. One `frontmatter-yaml` error and no false `missing-field` |
| 10 | Variants of the example | `python3 "$SKILLS/moi-blog/scripts/selftest.py"` | Each case passes with the exit code and rule name expected: description instead of summary, string `author`, bare-domain `author.url`, em dash and `&mdash;`, H1 in the body, skipped heading level, link without a scheme, HTML comment, TODO, unquoted colon, tag with a space, "Voyage devnet", impossible date, duplicate key, no frontmatter, long summary (exit 0, and exit 1 with `--strict`), stray `<Subscribe />`, nine takeaways, emoji, Windows line endings, a byte order mark, missing image and cover files, unchecked links outside a clone, `slop-lint.sh` missing and `--no-slop-lint` <!-- slop-lint:ignore --> |
| 11 | `{{x}}` placeholders and env files (2026-10-04) | built and run by `selftest.py` | A `{{x}}` in the body or in the frontmatter: exit 1, `placeholder`. The same text in inline code: exit 0. `.env` and `marker.env`: exit 2, "refusing to read ...", and no line of the file, not even a retired term in it, is printed. `copy-lint.py` refuses the same names, as the copy file and as `--post`, and still accepts `{{link}}` | <!-- slop-lint:ignore -->
| 12 | Mutated input | A one-off harness (not in the skill) ran 1500 random edits of the example post through `post-lint.py` and 800 of the copy template through `copy-lint.py` | No traceback and no exit code outside 0, 1 and 2 |
On the six posts on `main`, run outside a clone: `how-ai-agents-pay-each-other-moi`, `how-to-give-an-ai-agent-authority-without-your-credentials` and `moi-august-2026-release` fail on em dashes (the first also on two `slop-lint/voyage-devnet` hits), `moi-september-2026-release` fails on the three errors above, and `move-your-voyage-login-to-moi-wallet` and `what-is-moi-network` have no error.

### scripts/copy-lint.py
| # | Input | Command | Result |
|---|---|---|---|
| 1 | Good: hand-written X and LinkedIn copy for the example post, built by `selftest.py` | `python3 "$SKILLS/moi-blog/scripts/copy-lint.py" --post "$SKILLS/moi-blog/examples/moi-september-2026-release.md" copy-good.md` | Exit 0. 0 errors, 0 warnings |
| 2 | Bad: the copy template | `python3 "$SKILLS/moi-blog/scripts/copy-lint.py" "$SKILLS/moi-blog/templates/announce/social-copy.md"` | Exit 1. 7 errors, all placeholders, and a warning that no post was found |
| 3 | Real: the five copy files on `main`, each with its post | `python3 "$SKILLS/moi-blog/scripts/copy-lint.py" --post <post> <copy>` | Three have 0 errors and 0 warnings. `move-your-voyage-login-to-moi-wallet` has 3 `em-dash` errors and a `relative-word` warning. `what-is-moi-network` has 0 errors and 3 warnings. Their X lengths (213 to 259) and LinkedIn lengths (1,058 to 1,373) match `npm run distribute <slug> -- --dry-run` |
| 4 | Bad: file does not exist | `python3 "$SKILLS/moi-blog/scripts/copy-lint.py" "$T/none.md"` | Exit 2 |
| 5 | Variants | `python3 "$SKILLS/moi-blog/scripts/selftest.py"` | Each case passes: seeded summary left as the X block (error), X over 280 characters (error), backticks (error), a Discord block (warning), em dash (error), slug that is not the file name (error), no `{{link}}` (warning), "today" (warning), emoji (warning), a block line indented too little (error), a webhook address in the copy (never echoed) | <!-- slop-lint:ignore -->
`selftest.py` result: `selftest: 69 passed, 0 failed` (2026-10-04, after the `{{x}}` placeholder rule and the env-file refusal were added). It writes only inside a temporary folder. <!-- slop-lint:ignore -->

### scripts/check-live.py
HTTP GET only, against the live site.
| # | Input | Command | Result |
|---|---|---|---|
| 1 | Good: the live September post | `python3 "$SKILLS/moi-blog/scripts/check-live.py" moi-september-2026-release` | Exit 0. 13 PASS, 1 INFO ("no `cover` is set"). Article, one H1, canonical, JSON-LD (`Article` and `FAQPage`), `llms.txt`, sitemap, both feeds with newsletter tags, the apex listing, and a real 404 for an unknown address |
| 2 | Bad: a slug that does not exist | `python3 "$SKILLS/moi-blog/scripts/check-live.py" no-such-post-xyz` | Exit 1. 6 FAIL: the article answers 404, and the slug is missing from `llms.txt`, both feeds, the listing and the sitemap |
| 3 | Good: a deleted post | `python3 "$SKILLS/moi-blog/scripts/check-live.py" no-such-post-xyz --expect-gone` | Exit 0. The article answers 404 and the slug is absent everywhere |
| 4 | Bad: a live post checked as deleted | `python3 "$SKILLS/moi-blog/scripts/check-live.py" moi-september-2026-release --expect-gone` | Exit 1. 6 FAIL |
| 5 | Bad: a cover expected | `python3 "$SKILLS/moi-blog/scripts/check-live.py" moi-september-2026-release --expect-cover` | Exit 1. FAIL `og:image`: none on the page |
| 6 | Bad: slug with a space and capitals | `python3 "$SKILLS/moi-blog/scripts/check-live.py" "Bad Slug"` | Exit 2. "the slug is the file name without .md, lowercase with hyphens" |
| 7 | Bad: host unreachable, with a query string on the address | `python3 "$SKILLS/moi-blog/scripts/check-live.py" x --origin "http://127.0.0.1:9/?key=abc"` | Exit 2. "cannot reach the host", and the query is shown as `<query hidden>` |
| 8 | Bad: a file or ftp address | `python3 "$SKILLS/moi-blog/scripts/check-live.py" x --origin file:///etc` (and `--apex ftp://example.invalid`) | Exit 2. "must be an http:// or https:// address". Nothing is fetched |
| 9 | Bad: the apex host given as the blog host | `python3 "$SKILLS/moi-blog/scripts/check-live.py" moi-september-2026-release --origin https://moi.technology` | Exit 1. 7 FAIL and a `404-behaviour` WARN: the apex answers 200 for any path |
Cases 6 to 8 run inside `selftest.py` with no network.
Before the script used `curl`, case 1 failed on this machine with `CERTIFICATE_VERIFY_FAILED`, because the Python 3.13 here has no usable certificate store. The script now calls `curl` when it is installed, with `--proto =http,https`, and falls back to `urllib` only when it is not.

### Library scripts used by this skill
Over every `.md` and `.html` file in the skill: `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" $(find "$SKILLS/moi-blog" -name '*.md' -o -name '*.html')` printed `0 error(s), 109 warning(s) in 36 file(s)` on 2026-10-04 (the release-pack branch is inside that count); every warning is a placeholder in a `templates/` folder, which is expected. The `.py` files are not linted: they define the rules and the placeholder patterns. A line that quotes a wrong form on purpose carries the `slop-lint:ignore` marker. `bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" "$SKILLS/moi-blog"` printed `0 finding(s) in 65 file(s) scanned`, nothing skipped. a grep for the home-folder path prefix over the skill found nothing, a count of the em dash character over every file found 0, and every file is within its line limit (`SKILL.md` 118 of 150, `release-pack/GUIDE.md` 97, the longest reference 128 of 200).
`bash "$SKILLS/moi-devrel/scripts/time-table.sh" "2026-10-09 14:30" Asia/Kolkata` printed the `ISO UTC` line `2026-10-09T09:00:00Z`, the form `buffer.mjs --at` needs (exit 0).
`moi-devrel/claim-check` interface, run from a scratch folder on the example post: `extract-claims.py --all` printed 246 candidate rows for 246 sentences (exit 0; the default run printed 194 and said 52 sentences were not listed), `ledger-status.py` on the untouched copy exited 1 with 246 unverified, and `extract-claims.py --all --against` with `--dropped` on the same ledger exited 0 (2026-10-04).

### Reading `scripts/buffer.mjs` and the pipeline without sending anything
`scripts/buffer.mjs` was read in full. A copy of it was run from a scratch folder, so no `.env` was in reach. With no key it printed "BUFFER_API_KEY is not set" and exited 1 before any request. With a placeholder value in the environment and no command it printed the usage text (which omits `--thread-dir`) and exited 1, with no request made. `node --check` passed. Nothing was posted or scheduled.
`node scripts/distribute.js moi-august-2026-release --dry-run` in a clone of the website repo, with no secrets, printed `missing` for X and LinkedIn and exited 0. With six throwaway values (`x`) it printed `would send 241/280` and `would send 1183/3000`, exited 0 and sent nothing.

## Pass after the review fixes, 2026-10-04
Run after the critic's findings were applied. `SKILLS` is the folder that holds the `moi-*` skills; `W` is a `mktemp -d` folder that is a git repository, with `PYTHONDONTWRITEBYTECODE=1`.
| Check | Command | Result |
|---|---|---|
| Dropped row | `grep -n 'live on devnet' "$SKILLS/moi-blog/SKILL.md"` | The row "Read "live on devnet" from the node, never from the source tip" is back in "Facts that fail silently", 16 rows as before the condensing (counted without the header) |
| Description | `ruby -E UTF-8 -ryaml` on the block between the two `---` lines | Parses; a double-quoted string of 1,013 characters. "announce an upgrade", a phrase of the release-pack skill, is back in |
| Pack scaffold from the new depth | `bash "$SKILLS/moi-blog/release-pack/scripts/new-release-pack.sh" 0.99.0` in `W`, then again, then with no argument, then from inside `moi-blog/release-pack`, then with `SKILLS` unset | Exit 0 and the pack folder made; exit 1 "already exists"; exit 2 usage; exit 2 "this folder is inside moi-blog" and nothing created; exit 0 with `SKILLS` unset |
| Pack lint | `python3 "$SKILLS/moi-blog/release-pack/scripts/thread-lint.py" "$SKILLS/moi-blog/release-pack/examples/v0.13.0/social" --note "$SKILLS/moi-blog/release-pack/examples/v0.13.0/RELEASE-NOTE.md"`, then on `nofolder` | Exit 1 by design (the example keeps its faults: 20 errors); exit 2 "cannot read nofolder" |
| Self-test | `python3 "$SKILLS/moi-blog/scripts/selftest.py"` | 69 passed, 0 failed. `post-lint.py` finds `slop-lint.sh` with `SKILLS` set and with it unset |
| Pointers, lint, scan | the pointer check over `$SKILLS`; `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" --errors-only` over every `.md`, `.html`, `.txt`, `.rst`, `.csv` and `.yaml` file of the folder; `secret-scan.sh "$SKILLS/moi-blog"` | 0 problems; 0 errors in 59 files; 0 findings in 65 files |
| Limits | `wc -l` | `SKILL.md` 119 lines of 150; `release-pack/GUIDE.md` 97 of 150 |
