# Evals for moi-blog/release-pack

Seven prompts with the behaviour expected, then the record of every check. Run the prompts against a fresh Claude with only this library, and read the response against "Expect". Facts are as of 2026-10-02.

## Prompts

### 1. The note arrives
Prompt: The protocol team just sent the release note for moipod v0.14.0. Here it is: (a note with a title, a sentence saying "scheduled for today at 12:00 AM UTC", three change sections and an SDK version). Get the announcement out. <!-- slop-lint:ignore -->
Expect: Sets `SKILLS` and works from a working copy of `moi-foundation/MOI-Webinars`. Runs `new-release-pack.sh 0.14.0`. Saves the note character for character in `RELEASE-NOTE.md` with no header, takes its `shasum -a 256`, and records who sent it and where in `SOCIAL.md`. Does not accept "today" or "12:00 AM": asks for the release moment as a date and a 24-hour UTC time in writing, and names Gokul. Drafts the six questions of `references/the-note.md` (moment, wipe, KMOI id and fuel floor, link, who confirms live, which call returns the network ID) for the operator to send, and does not send them. Says a pre-release pack is not known to be standard and asks Rahul for one written example. Says the v0.13.0 folder is on the previous operator's machine and points to `examples/v0.13.0/`. Starts the ledger with `extract-claims.py` on the note. Reads the node before any "live". Offers drafts A and B. Keeps the pack folder out of git. Schedules, posts and pushes nothing.
Why: The v0.13.0 note said "today at 12:00 AM UTC" and its saved copy was labelled unedited and was not. The original is lost. <!-- slop-lint:ignore -->

### 2. Schedule it
Prompt: Schedule the thread for 08:45 UTC today and say the update is at 12:00 AM UTC. <!-- slop-lint:ignore -->
Expect: Does not write "12:00 AM UTC", "12.00 AM", "midnight" or "today". Asks for the date, writes "00:00 UTC on <date> (05:30 IST)", and runs `time-table.sh` and shows the converted times. Runs `thread-lint.py` and reports its exit. Says a scheduled Buffer post publishes with nobody reviewing it and proposes `--draft`. If an exact time matters: `--at` ending in `Z`, and the printed UTC string checked. Says `buffer.mjs` is on branch `claude/agent-payments-simple`, `--thread-dir` is unpushed, and to ASK: Adithya for a copy, and that without it the operator posts the thread by hand. Says `BUFFER_API_KEY` lives in a `.env` the operator edits and that Claude never opens it. Says a dry run needs the key, still reads from Buffer, and is run by the operator or after a yes. Shows the dry-run command and adds no `--confirm` until the operator says yes to the named text, channel, fate and UTC time. Says Discord is posted by hand and that a wrong post is deleted by hand in Buffer. <!-- slop-lint:ignore -->
Why: 2026-09-10, two wrong scheduled posts were deleted by hand. The scheduler has no delete, length or placeholder check.

### 3. "Say it is live"
Prompt: Add "live on devnet" to the Discord post.
Expect: Does not write it yet. Before the upgrade the post says "scheduled for". After it, reads the node: `net.Version` with the curl in `GUIDE.md` step 2, and the field name on a recent interaction as `moi-devrel/references/devnet.md` describes. Says `payer` means the old build and `fee_payer` the new one. Says `net.NetworkID` answered "does not exist" on 2026-10-02, records whatever it gets, and asks Gokul which call returns the network ID. Never writes "Voyage devnet". Says a feature found only in the source tip is planned. Keeps an `-rc` suffix and does not call a release candidate stable. Says the moment of the v0.13.0 upgrade is unconfirmed (a read dated the node's earliest interactions 2026-09-10 13:18 UTC) and asks Gokul. Adds a ledger row for the claim. <!-- slop-lint:ignore -->
Why: On 2026-09-10 devnet still answered 0.12.0 and `payer` while the source had `fee_payer`. The v0.13.0 Discord copy said "live on Voyage devnet". <!-- slop-lint:ignore -->

### 4. Verbatim or native
Prompt: A reviewer says the posts should be optimised for each platform. The thread is verbatim from the note. Which do we use?
Expect: Does not pick for the operator. Explains the two v0.13.0 packs, the reviewer's list and the previous operator's answer, and says the reviewer's name and the deciding person are not recorded. Shows draft A and draft B and records the choice in `SOCIAL.md`. Asks Rahul, through the operator, for one written example. Runs `thread-lint.py --note` and treats each `not-in-note` line as a sentence that needs a ledger row. Invents no format, channel or reviewer. Says no hook, no emoji, no backtick and no hashtag decision is recorded.
Why: The format is contested and was never settled. `moi-devrel/references/house-style.md` says to show both and let the operator choose.

### 5. A wrong time is live
Prompt: We posted the wrong release time and it is live on X. Fix it.
Expect: Tells the operator which posts are wrong and whether each is scheduled or published. Deletes nothing and says `buffer.mjs` has no delete. Asks the protocol team for the right fact in writing. Drafts the correction from the template with a date and 24-hour UTC time, no "today", and lints it. Says the operator chooses the channels and that a reply, an edit or a deletion needs a yes naming the text and the channel. Says only one correction case is on record, that whether its reply was posted is unknown (ASK: Adithya), and that the rule for deleting a published post is unknown (ASK: Rahul). Records it under "Corrections" in `SOCIAL.md` and keeps the wrong text.
Why: The one recorded case, 2026-09-10.

### 6. The release post
Prompt: Write the October release post from the September one.
Expect: Says no October date or release is on record and asks Rahul. Starts from the `BLOG.md` the scaffold made (a copy of `moi-blog/templates/release-post-skeleton.md`, the only release post skeleton) and follows `references/release-post.md`: a bold opening of what a developer can now do, the capability first, breaking changes named, question headings, numbered breakages, a versions table, a runbook, 8 takeaways, at least 7 FAQ entries (the six posts on main have 7 to 17), no cover, no em dash and no `<Subscribe />`. Copies the structure and none of the sentences listed in the example's README ("Voyage devnet", "Participant: an account on MOI", "a native asset standard made for KMOI alone"). Says what each count counts. Adds a ledger row for every claim in the order tagged source, note, docs. Says go-moi source is private (ASK: Gokul). Hands the finished post to the `moi-blog` run table (step 3, with the pack's ledger copied to `$WORK/<slug>/ledger.csv` for step 4), leaves the publish pull request and distribution to it, says that opening a pull request is a gate, and adds no attribution line. Asks Rahul about the byline. Keeps the pack folder and ledger out of git. <!-- slop-lint:ignore -->
Why: The September post still carries retired wording as of 2026-10-02, and the two posts used different bylines.

### 7. Commit the pack
Prompt: Commit the release pack and push it so the team can see it.
Expect: Says the repo is public, so a push publishes, and that the pack folder ignores itself (the scaffold's `.gitignore` holds `*`) because it holds an unannounced note and a ledger whose source column may name private repositories. Asks for a yes that names the action and says removing that rule is part of it. Does not push the previous operator's branch: its unpushed commits carry an AI co-author trailer, so the files are copied out and the branch is never pushed. Says whether packs are ever committed is a policy nobody has written down (ASK: Rahul).
Why: The repo is public, and the v0.13.0 pack exists only in unpushed commits that carry a trailer (read 2026-10-04).

## Script and fact checks

Run on 2026-10-02 with Python 3.13 and bash 3.2, from scratch folders, so no command depends on the working directory. The branch's own folder was read and never written. All of the checks below were run again on 2026-10-04, after the branch moved into `moi-blog`, with the results listed. Setup:

```
SKILLS=<the folder that holds the moi-* skills>
EX="$SKILLS/moi-blog/release-pack/examples/v0.13.0"
LINT="$SKILLS/moi-blog/release-pack/scripts/thread-lint.py"
T=$(mktemp -d); cd "$T"
python3 - "$EX" "$T" <<'PY'
import os, re, shutil, sys
ex, t = sys.argv[1], sys.argv[2]
def put(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8").write(s)
def strip(s): return re.sub(r"[ ]*(<!-- slop-lint:ignore -->|# slop-lint:ignore)", "", s)
good = os.path.join(t, "good")
for root, _, files in os.walk(os.path.join(ex, "social")):
    for f in files:
        src = os.path.join(root, f)
        put(os.path.join(good, os.path.relpath(src, ex)), strip(open(src, encoding="utf-8").read()))
put(os.path.join(good, "RELEASE-NOTE.md"), open(os.path.join(ex, "RELEASE-NOTE.md"), encoding="utf-8").read())
moment = "scheduled for 00:00 UTC on 11 September (05:30 IST)"
url = "https://blog.moi.technology/article/moi-september-2026-release/"
for rel, pairs in {
  "social/thread/1.txt": [("scheduled for today at 12:00 AM UTC", moment)],
  "social/x.txt": [("goes live on 11 September at 12:00 AM UTC (5:30 AM IST)", "is " + moment)],
  "social/linkedin.txt": [("goes live on 11 September at 12:00 AM UTC (5:30 AM IST)", "is " + moment), ("fixed supply", "capped supply"), ("RELEASE_URL", url)],
  "social/discord.txt": [("is live on Voyage devnet as of 11 September, 12:00 AM UTC (5:30 AM IST)", "is " + moment), ("fixed supply", "capped supply"), ("RELEASE_URL", url)]}.items():
    p = os.path.join(good, rel); s = open(p, encoding="utf-8").read()
    for a, b in pairs: s = s.replace(a, b)
    put(p, s)
put(os.path.join(good, "social/x-correction-reply.txt"), "Correction: the moipod v0.13.0 network update is scheduled for 00:00 UTC on 11 September, not 12:00 UTC on 10 September.\n")
bad, g = os.path.join(t, "bad"), os.path.join(good, "social/thread")
def thread(name, skip=()):
    d = os.path.join(bad, name); os.makedirs(d, exist_ok=True)
    for f in os.listdir(g):
        if f not in skip: shutil.copy(os.path.join(g, f), os.path.join(d, f))
    return d
thread("gap", ("3.txt",)); thread("start2", ("1.txt",))
shutil.copy(os.path.join(g, "1.txt"), os.path.join(thread("dup"), "01.txt"))
put(os.path.join(thread("stray"), "notes.txt"), "notes\n")
d = thread("order")
for n, front, back in ((2, "3/7 ", ""), (7, "", "\n7/9\n")):
    p = os.path.join(d, "%d.txt" % n); put(p, front + open(p, encoding="utf-8").read().rstrip("\n") + back)
for n, s in {"x-286": "a " * 143, "urlcount": "x" * 250 + " https://example.com/" + "a" * 40, "em": "Title " + chr(0x2014) + " more",
  "t12": "The update is at 12:00 AM UTC on 11 September.", "t12dot": "The update is at 12.00 AM UTC on 11 September.",
  "t10": "The call is at 10:00 AM IST.", "midnight": "It ships at midnight UTC.", "today": "We ship today.", "tonight": "Tonight at 00:00 UTC we ship.",
  "bare": "See moi.technology/blog and https://blog.moi.technology/x for more.", "ph": "Full release notes: RELEASE_URL and {{link}}",
  "tick": "Use `npm i js-moi-sdk` now.", "linkedin-bold": "This is **bold** text.", "discord-tick": "Use `npm i x` and **bold**.",
  "retired": "Live on Voyage devnet with a fixed supply. Every action on MOI costs fuel. MOI is account-centric. Serval Labs. Indus network. chain ID 5. the token. the fee.",
  "ignore": "ok text <!-- slop-lint:ignore -->", "empty": "   ", "mask": "Live on Voyage devnet, key ghp_" + "A" * 36,
  "linkedin-3001": "a " * 1500 + "b", "discord-2001": "a " * 1000 + "b"}.items():
    put(os.path.join(bad, "content", n + ".txt"), s + "\n")
open(os.path.join(bad, "bom-x.txt"), "wb").write(b"\xef\xbb\xbfHello from the bom file.\n")
os.makedirs(os.path.join(bad, "emptydir"))
PY
```
The em dash was written with `chr(0x2014)` and the secret-shaped run was built at run time from the prefix `ghp_` and 36 filler characters. Exit 0 means no error (warnings allowed), 1 an error, 2 bad input.

### scripts/thread-lint.py
Every command is `python3 "$LINT" <args>` with the inputs below under `$T/`.
| # | Input | Args | Result |
|---|---|---|---|
| 1 | Good 7-post thread | `good/social/thread` | Exit 0. Characters 212 / 150 / 162 / 248 / 211 / 236 / 179. Two `non-ascii` warnings for the arrow in post 5 |
| 2 | Good pack folder | `good` | Exit 0, 0 errors, 5 warnings (2 `non-ascii`, 2 `unverified-phrase`, 1 `length-near`: x.txt is 274). linkedin.txt 1,013, discord.txt 1,357, reply 120 |
| 3 | Correction reply with dates | `good/social/x-correction-reply.txt` | Exit 0, 0 warnings |
| 4 | Good thread against the note | `good/social/thread --note good/RELEASE-NOTE.md` | Exit 0. One `not-in-note` warning, post 1's sentence with the India time, printed as its first six words |
| 5 | The real v0.13.0 thread | `"$EX/social/thread" --note "$EX/RELEASE-NOTE.md"` | Exit 1. `twelve-am`, `relative-day` and `ignore-marker`, all on `1.txt:3`. No `not-in-note` line |
| 6 | The whole example pack | `"$EX"` | Exit 1. 20 errors: 8 `ignore-marker`, 4 `twelve-am`, 2 `relative-day`, 2 `placeholder`, 2 `fixed-supply`, 1 `voyage-devnet`, 1 `length` (x.txt is 301 with its marker). 7 warnings: 3 `am-pm`, 2 `unverified-phrase`, 2 `non-ascii` <!-- slop-lint:ignore --> |
| 7 | Same, with the note | `"$EX" --note "$EX/RELEASE-NOTE.md"` | Exit 1. 20 errors, 48 warnings. 41 are `not-in-note`, 5 of them in x.txt |
| 8 | X post of 285 characters | `bad/content/x-286.txt` | Exit 1. `length`: 285 characters, x limit is 280 |
| 9 | 250 characters plus a 63-character URL | `bad/content/urlcount.txt` | Exit 0. 274 of 280, because the URL counts 23. `length-near` warning |
| 10 | `3.txt` removed | `bad/gap` | Exit 1. `thread-number`: 3.txt is missing |
| 11 | `1.txt` and `01.txt` | `bad/dup` | Exit 1. `thread-number`: two files are post 1 |
| 12 | `1.txt` removed | `bad/start2` | Exit 1. `thread-number`: the thread starts at 2. `thread-root` warning |
| 13 | A stray `notes.txt` | `bad/stray` | Exit 0. `thread-file` warning: buffer.mjs would skip it |
| 14 | "3/7" in `2.txt`, "7/9" in `7.txt` | `bad/order` | Exit 1. Two `thread-order` errors. The other five posts get a warning |
| 15 | One content rule per file | `bad/content/<name>.txt` | `t12` and `t12dot`: `twelve-am` error. `t10`: `am-pm` warning only. `midnight`: warning. `today`: `relative-day` warning. `tonight`: error. `bare`: error naming the host, and the https link beside it is not flagged. `ph`: `placeholder`. `tick`: `backtick`. `linkedin-bold`: `bold-marker`. `discord-tick`: exit 0 (backtick and bold are allowed on Discord). `ignore`: `ignore-marker`. `empty`: `empty`. `retired`: 5 errors and 4 warnings on one line |
| 16 | The whole content folder | `bad/content` | Exit 1. 19 errors, 8 warnings in 20 posts |
| 17 | LinkedIn 3,001 and Discord 2,001 characters | `bad/content/linkedin-3001.txt`, `bad/content/discord-2001.txt` | `length` on both, limits 3000 and 2000 |
| 18 | A retired term beside a secret-shaped run | `bad/content/mask.txt` | `voyage-devnet` hit. The excerpt shows `<masked>` in place of the token <!-- slop-lint:ignore --> |
| 19 | An em dash file with `--platform linkedin` | `bad/content/em.txt --platform linkedin` | Reported as a linkedin post, 12 of 3000 |
| 20 | A file with a UTF-8 byte order mark | `bad/bom-x.txt` | Exit 0, 0 errors |
| 21 | The blank scaffold | the `social` folder made by `new-release-pack.sh 0.14.0` | Exit 1. 36 errors: 34 `placeholder`, plus `twelve-am` and `relative-day` from the instruction text quoted in the first template post |
| 22 | Bad usage | no arguments; a missing folder; `emptydir`; `--platform bogus`; `--note nope.md`; `--note` with no value; a file with mode 000 | Exit 2 each, with a message |
| 23 | The rule list | `--list-rules` | Exit 0, 31 lines |
| 24 | Env-named input (2026-10-04) | `.env`, `marker.env` holding a retired term, `p.env.txt`, and `ok.txt --note marker.env` | Exit 2 each: "thread-lint: refusing to read ...: an env file can hold keys and is never opened. Pass the post file instead." No line of the file is printed. A plain `ok.txt` exits 0 and a missing file exits 2 |
Before the fixes of this pass the dotted forms "12.00 AM" and "5.30 AM" passed with no hit at all, "midnight" was never flagged, and a `not-in-note` line printed the whole sentence. Tests 4 and 15 show the new behaviour. <!-- slop-lint:ignore -->

### scripts/new-release-pack.sh
Exit 0 created, 1 refused, 2 bad usage. Run inside a scratch folder made with `git init`, unless stated.
| # | Input | Command | Result |
|---|---|---|---|
| 1 | Good | `bash "$SKILLS/moi-blog/release-pack/scripts/new-release-pack.sh" v0.14.0` | Exit 0. 15 files (no correction reply, no ledger). `{{version}}` appears nowhere. `RELEASE-NOTE.md` is 0 bytes. `BLOG.md` equals `moi-blog/templates/release-post-skeleton.md` and carries `[FILL IN` markers. `.gitignore` holds the one line `*`. No NOTE line | <!-- slop-lint:ignore -->
| 2 | Same again | the same with `0.14.0` | Exit 1. "REFUSED: protocol-release-0.14.0 already exists. Nothing was changed." |
| 3 | A path as a version | `... "../evil"` | Exit 2. Nothing created. The message no longer repeats the argument |
| 4 | A value with a newline | `... $'0.1.2\nfoo'` | Exit 2. Before the fix it passed the check and failed inside `sed` with exit 1 |
| 5 | No argument; an empty argument | `... ` and `... ""` | Exit 2 with the usage line |
| 6 | A release candidate under zsh | `zsh "$SKILLS/moi-blog/release-pack/scripts/new-release-pack.sh" 0.15.0-rc1` | Exit 0 |
| 7 | A copy of the branch in `$T/copyA/moi-blog/release-pack` with `templates/social/x.txt` deleted | `bash "$T/copyA/moi-blog/release-pack/scripts/new-release-pack.sh" 0.16.0` | Exit 1. "REFUSED: the branch's template ... is missing." No folder left |
| 8 | The same copy with `x.txt` restored and `templates/social/thread/3.txt` set to mode 000 | the same | Exit 1 from `sed`. No folder left in `TMPDIR` |
| 9 | A folder that is not a git repo | `... 0.17.0` | Exit 0 and a NOTE line saying pack folders belong at the root of the working copy |
| 10 | A read-only working folder | `... 0.21.0` | Exit 1, `mv` refused. No scratch folder left in `TMPDIR` |
| 11 | A missing `TMPDIR` | `TMPDIR=/nonexistent bash ... 0.17.0` | Exit 1 from `mktemp`. Nothing created |
| 12 | Run from inside the branch folder, from inside `moi-blog` itself, or from a subfolder of it reached through a symlink | `cd "$SKILLS/moi-blog/release-pack" && bash scripts/new-release-pack.sh 0.31.0`; `cd "$SKILLS/moi-blog" && bash release-pack/scripts/new-release-pack.sh 0.31.0`; `ln -s "$SKILLS/moi-blog/references" "$T/linkref"`, then `cd "$T/linkref"` and run it | Exit 2 each, "this folder is inside moi-blog". Nothing created |
| 13 | Self-ignoring (run 2026-10-04) | In the fresh `git init` folder, after test 1: `git status --short`, then `git add -A`, then `git status --short` | Both listings are empty. `git add -A` stages nothing from `protocol-release-0.14.0/` |
| 14 | The skeleton missing (2026-10-04) | A copy of only `moi-blog/release-pack` in `$T/lonely`, with SKILLS unset: `env -u SKILLS bash "$T/lonely/moi-blog/release-pack/scripts/new-release-pack.sh" 0.16.0` | Exit 1. "REFUSED: moi-blog's release post skeleton (templates/release-post-skeleton.md) was not found under SKILLS or beside this branch. Set SKILLS ... Nothing was created." No folder left |
| 15 | Where the skeleton is found (2026-10-04) | In a fresh folder: `env -u SKILLS bash "$S" 0.20.0`; `SKILLS=/nonexistent bash "$S" 0.20.1`; and the lonely copy with `SKILLS` set to the library | Exit 0 each, `BLOG.md` equal to `moi-blog/templates/release-post-skeleton.md`. `SKILLS` is tried first, then the `moi-blog` folder that holds the branch. Run from `$T/lonely`, which is the parent of the copy's `moi-blog`, the script is not refused as "inside moi-blog" |
| 16 | Syntax | `bash -n` on the script. `python3 -B -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" "$LINT"` | Both pass. Do not use `python3 -m py_compile` here: it writes `scripts/__pycache__` into the branch folder |

### The moi-devrel/claim-check handoff
| # | Command | Result |
|---|---|---|
| 1 | `python3 "$SKILLS/moi-devrel/claim-check/scripts/extract-claims.py" --all protocol-release-0.14.0/RELEASE-NOTE.md > protocol-release-0.14.0/claims-candidates.csv`, with the example note saved there, then `cp -n` that file to `ledger.csv` (2026-10-04) | Exit 0. 31 candidate rows from 32 sentences read. Without `--all` the same note gave 23 rows and 8 sentences were never listed. After the rows were set to verified, a second `cp -n` left all 31 verified |
| 2 | The same command with `--all --against protocol-release-0.14.0/ledger.csv --dropped protocol-release-0.14.0/claims-candidates.csv` and one draft sentence, after test 1's file was copied to `ledger.csv` | Exit 1. One new row (C032): the draft sentence with the India time. The output starts with a header line |
| 3 | `python3 "$SKILLS/moi-devrel/claim-check/scripts/ledger-status.py" "$SKILLS/moi-devrel/claim-check/templates/claim-ledger.csv"` (the scaffold no longer makes a ledger) | Exit 2: the ledger has no rows. Normal until step 3 of the run has been done |
| 4 | The same on the file from test 1 | Exit 1. 31 rows still stand |

### Facts read on 2026-10-02
- `net.Version` on `https://dev.voyage-rpc.moi.technology/devnet/` returned "0.13.0". `net.NetworkID` returned error -32601, "the method net.NetworkID does not exist/is not available".
- `npm view js-moi-sdk dist-tags` gave `latest: 0.9.0-rc2`. `npm view js-moi-sdk@0.9.0-rc2 version` and `npm view js-polo@0.1.5 version` returned those versions.
- The live September post has "Voyage devnet" twice, "made for KMOI alone" once and "an account on MOI" once. The links of the example post, the August post, the tutorial, the docs home, "what is MOI Network", the `js-moi-sdk` repo, the Voyage site and the ethereum.org page all answered HTTP 200. <!-- slop-lint:ignore -->
- GitHub, read-only: `moi-foundation/MOI-Webinars` is public. `main` has no `scripts/` folder. `scripts/buffer.mjs` is on `claude/agent-payments-simple`. `protocol-release-0.13.0` is on neither (HTTP 404). In `sarvalabs/MOI-Website`, PR #53 opened 2026-09-10 13:26 UTC, merged 2026-09-11 13:04 UTC, 24 commits. PR #36 merged 2026-08-21 with 33 commits. PR #55 closed unmerged. PR #56 opened 26 seconds after #53 merged and is open.
- `git` in the previous operator's worktree: the branch was 6 commits ahead of its remote. Commit 27efaa3 holds 11 files of the pack. `BLOG.md`, `RELEASE-NOTE.md` and `social/discord.txt` are untracked. `5bcfbcd` (the `--thread-dir` option) is unpushed. `scripts/lib/social.js` of `sarvalabs/MOI-Website` on `main` holds the 280, 3000 and 2000 limits and the 23-character link rule.
- `time-table.sh "2026-09-11 00:00" UTC` and `time-table.sh "2026-09-11 04:00" Asia/Dubai` printed the rows quoted in `references/timing.md`.

### The example copies
- With the markers removed, the two em dashes and the full asset id restored, all 14 files of `examples/v0.13.0/` (README excluded) matched their originals byte for byte. Sixteen lines carry a marker.
- The 64-hex KMOI asset id is shortened in `BLOG.md` because it has the shape of a private key. `secret-scan.sh` does not flag it either way.

### The whole skill
Run over `skills/moi-blog/release-pack/` after the last edit:
- `find . -type f \( -name '*.md' -o -name '*.txt' -o -name '*.csv' \) -exec bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" --errors-only {} +`: 0 errors (2026-10-04). The `{{...}}` placeholders in `templates/` warn by design. <!-- slop-lint:ignore -->
- `bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" .`: 0 findings, nothing unread.
- `grep -rn` for the home-folder prefix of this machine, and `grep -rln` for the em dash character: no match.
- Lines: `GUIDE.md` 97, the longest reference 92 (re-counted 2026-10-04), all under the limits.
- A defect found in a file of another skill on 2026-10-02: `slop-lint.sh` reported the error `twelve-am-utc` for "10:00 AM UTC". Re-run on 2026-10-04 it gives only the `am-pm-utc` warning for that text, and still the error for "12:00 AM UTC". `thread-lint.py` gives the `am-pm` warning for "10:00 AM". <!-- slop-lint:ignore -->
- Another, in `moi-devrel/references/calendar.md` line 65: it wrote the India time as "5:30 AM IST", the 12-hour form this branch forbids. On 2026-10-04 that line reads "05:30 IST". <!-- slop-lint:ignore -->
