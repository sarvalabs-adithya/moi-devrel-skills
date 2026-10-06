# Script tests for the moi-devrel scripts

Moved out of `evals.md` on 2026-10-04 to keep each file under 200 lines. The prompts and the final checks stay in `evals.md`. Back to `../SKILL.md`.

Run on 2026-10-03 on macOS 27.0 (bash 3.2.57, zsh 5.9, Python 3.13). Not tested on Linux. Inputs are built at run time from a known prefix plus filler, so no secret-shaped string is stored in the skill. `$M` is `"$SKILLS/moi-devrel/scripts"`. Each line is a command and its real result. `time-table.sh` did not change since 2026-10-02 and was run again to confirm. `slop-lint.sh` changed on 2026-10-04: the placeholder rule skips a `{{` that follows `=` (a JSX prop), and its last rows below record that.

## Setup
````
T=$(mktemp -d) && cd "$T"; CO="Co-Authored""-By"; GEN="Generated ""with"
F=$(python3 -c "import string; s=string.ascii_letters+string.digits; print(''.join(s[(i*7+3)%len(s)] for i in range(40)))")
WORDS=$(python3 -c "print('-'.join(c * 5 for c in 'abcdefghijkl'))")
mkdir bin_ok bin_slow; : > empty.gitconfig; export GIT_CONFIG_GLOBAL="$T/empty.gitconfig"
printf '#!/bin/sh\n[ "$1" = "--version" ] && { echo gh version 0.0.0; exit 0; }\necho "  Logged in to github.com account operator-demo (keyring)"\necho "  - Active account: true"\necho "  - Token: gho_%s"\n' "$F" > bin_ok/gh
printf '#!/bin/sh\n[ "$1" = "--version" ] && { echo gh version 0.0.0; exit 0; }\nsleep 20\n' > bin_slow/gh; chmod +x bin_*/gh
mk() { git init -q -b feature/demo "$1"; git -C "$1" config user.name Demo; git -C "$1" config user.email demo@example.org
       echo hi > "$1/a.txt"; git -C "$1" add a.txt; git -C "$1" commit -qm "$2"; }
mk repo_clean "docs: add a note"
for n in Claude Anthropic Copilot ChatGPT OpenAI Codex Gemini Cursor; do mk repo_t_$n "$(printf 'docs: note\n\n%s: %s <x@y.z>' "$CO" "$n")"; done
for n in Claude Copilot ChatGPT Gemini Cursor; do mk repo_f_$n "$(printf 'docs: note\n\n%s %s Code' "$GEN" "$n")"; done
mk repo_human "$(printf 'docs: note\n\n%s: Pat Example <pat@example.org>' "$CO")"
````

## preflight.sh
| Command | Result |
|---|---|
| `(cd repo_clean && PREFLIGHT_WORK_DOMAINS=example.org PATH="$T/bin_ok:$PATH" bash "$M/preflight.sh")` | exit 0, `PASS  no AI co-author or footer line in the last 20 commits`, one WARN (no origin remote). The fake `gh` prints a token line, and the output holds no filler |
| the same in each of `repo_t_*` (eight assistant names in a trailer) and `repo_f_*` (five names in a "generated with" footer) | each prints `WARN  1 line(s) in the last 20 commits name an AI assistant (Claude, Anthropic, Copilot, ChatGPT, OpenAI, Codex, Gemini or Cursor) ...` |
| the same in `repo_human` (a human co-author) | no co-author WARN |
| a `prepare-commit-msg` hook that appends a trailer naming Gemini; a commit template whose only AI line is a "generated with" footer naming Cursor | `WARN  hook prepare-commit-msg can add a Co-Authored-By line or an AI footer`; `WARN  commit template (tmpl.txt) contains a Co-Authored-By line or an AI footer` |
| `PREFLIGHT_GH_TIMEOUT=2` with `bin_slow` first on `PATH` | `FAIL  gh auth status did not answer in 2 seconds (network, or a stuck keychain prompt), so the login is unchecked`, `1 FAIL`, 3 seconds elapsed (no `timeout` command on macOS, so the python3 path ran) |
| a `timeout` shim on `PATH` that runs the command, then one that exits 124 | `PASS  gh login: operator-demo (github.com)`; then `FAIL  gh auth status did not answer in 15 seconds ...` (the `timeout` branch works as well as the python3 branch) |
| `PATH` holding git, awk, sed, grep and the fake `gh` but no `timeout`, `gtimeout` or `python3` | `FAIL  no timeout tool (timeout, gtimeout or python3) is available, so the gh call was not run`; the real `gh` is never started without a limit |
| a git `user.name` of `Demo ghp_` plus the filler | `PASS  git user.name: Demo <masked>` |
| the original cases: remote with user, password, query token and fragment; gmail address, a Claude trailer, gh not logged in, on `main`; only git on `PATH`; `PREFLIGHT_EXPECT_GH_LOGIN=someone-else`; `yahoo.in`, `outlook.in`, `rediffmail.com`, `hey.com`; `zsh` | unchanged: `remote origin: https://github.com/example-org/demo.git`, `0 FAIL, 0 WARN`; `1 FAIL, 4 WARN` exit 1; `FAIL  tool gh is missing`; `FAIL  gh login is operator-demo but PREFLIGHT_EXPECT_GH_LOGIN is someone-else`; each provider WARNs; zsh `0 FAIL, 0 WARN` |

## slop-lint.sh
Built with `python3` writing `bad.md` (eleven lines: an em dash built with `chr(8212)`, "Not save a setting, not call your logic", "12:00 AM UTC", "Every action on MOI costs fuel", "account-based" with "Serval Labs", "fixed supply", "Voyage devnet", a trailer built from `"Co-Authored" + "-By"`, "Most teams quietly accept both", "The floor is yours", "Use the token for the fee"), `fence.md` (a closed fence holding "Voyage devnet", a line with an em dash and the trailer), `stray.md` (a fence opened and never closed, then the same lines), `leak.md` (a 40-character key next to "Serval Labs") and `good.md`. <!-- slop-lint: ignore -->
| Command | Result |
|---|---|
| `bash "$M/slop-lint.sh" bad.md` | exit 1, `9 error(s), 4 warning(s)`. `account-based` is reported as `account-centric` <!-- slop-lint: ignore --> |
| `bash "$M/slop-lint.sh" good.md` | `0 error(s), 0 warning(s)`, exit 0 (the marked wrong form is skipped) |
| `bash "$M/slop-lint.sh" fence.md` | `em-dash` on the dash line and `ai-attribution` on the trailer line reported, "Voyage devnet" inside the fence skipped, `2 error(s), 0 warning(s)` <!-- slop-lint: ignore --> |
| `bash "$M/slop-lint.sh" stray.md` | exit 1, `stray.md:1:unclosed-fence`, and the lines below it are still linted (`fuel-universal`, `em-dash`, `ai-attribution`), `4 error(s)` |
| `bash "$M/slop-lint.sh" leak.md` | the excerpt shows `key <masked> next to Se`; a search for the 40-character key in the output gives 0 |
| `bash "$M/slop-lint.sh" nope.md`, then with no argument | `cannot read nope.md`, exit 2; usage text, exit 2 |
| `bash "$M/slop-lint.sh" "$SKILLS"/moi-devrel/SKILL.md "$SKILLS"/moi-devrel/references/*.md` | `0 error(s), 0 warning(s)`, exit 0 |
| One file each holding `{{version}}`, `[FILL IN: x]`, `FILL-IN`, `[Sentence 1: what]`, `<<< EVIDENCE >>>` and `RELEASE_URL` (built at run time, 2026-10-04) | exit 1 each, one `placeholder` error. The same `{{version}}` under a folder named `templates` is `0 error(s), 1 warning(s)`, exit 0, and inside a fenced block it is skipped | <!-- slop-lint:ignore -->
| A JSX file with `style={{ flex: 1 }}` and `style={{ fontSize: "1rem" }}` props, and `design/ui_kits/marketing/components.jsx` (102 such props); a Markdown file holding `x = {{version}}`; one holding `Hello {{ name }} and {{{raw}}}` (2026-10-04) | The two JSX files: `0 error(s), 0 warning(s)` (before the change the real file gave 66 `placeholder` errors and exit 1). The two Markdown files: one `placeholder` error each, exit 1 | <!-- slop-lint:ignore -->
| `marker.env` holding a retired term, `.env.local`, `.envrc`, a symlink named `link.txt` that points at `marker.env`, and `p1.md marker.env` together (2026-10-04) | exit 2 each, "slop-lint: refusing to read ...: an env file can hold keys and is never opened." Nothing is read or printed from the env file, and a good file named beside it is not linted either (the run stops first) |

## time-table.sh
| Command | Result |
|---|---|
| `bash "$M/time-table.sh" "2026-09-10 09:15" America/New_York` | `Given Thu 2026-09-10 09:15 EDT (UTC-04:00)`, `UTC Thu 2026-09-10 13:15`, ISO line `2026-09-10T13:15:00Z (the form the MOI-Webinars buffer.mjs --at needs)` |
| `bash "$M/time-table.sh" "2026-09-11 00:00" UTC` | India `Fri 2026-09-11 05:30 IST`, US Eastern `Thu 2026-09-10 20:00 EDT` |
| the same time with zone `EST`, `PST`, `IST` or `Etc/GMT+5` | `'EST' is an abbreviation or fixed-offset name ... Use an area/city zone such as America/New_York`, exit 2 each time |
| `"2026-09-11 12:00 AM" UTC`; `"2026-09-11 00:00" Mars/Olympus`; `"2026-03-08 02:30" America/New_York` | `malformed time`; `unknown IANA zone ...`; `does not exist in America/New_York (clocks skip forward at that moment)` |
| `zsh "$M/time-table.sh" "2026-10-02 15:30" Asia/Kolkata` | UTC row `Fri 2026-10-02 10:00 UTC` |

## secret-scan.sh
Built in `scan/` with `python3`: `keys.txt` (`"sk-ant-" + "x" * 30` and a `ghp_` line), a private-key header, a 12-word line made of `aaaaa bbbbb ccccc` and so on in ten shapes, `ok_short_list.txt`, `sub/clean.md`, `node_modules/pkg/skip.txt`, `.env`, `prod.env`, `report.pdf`, `perm/` (one chmod 000 file and one chmod 000 folder) and `link.txt` (a symlink to a `.env`). The new shapes are built in `ss/` from `$F` and `$WORDS`: `url_pw.txt` (`https://deploy:$F@git.example.org/repo.git`), `query.txt` (`...?token=$F`), `bearer.txt` (`Authorization: Bearer $F`), `assign.txt` (`api_key = $F`, `the admin secret is $F`, a JSON `client_secret`, `SESSION_SECRET=$F`), `hyphen.txt` (`seed: $WORDS`), `hex64.txt` (a 64-digit hex string with and without `0x`), and `good.txt` (placeholders and prose, below).
| Command | Result |
|---|---|
| `bash "$M/secret-scan.sh" scan` | unchanged from 2026-10-02: exit 1, 13 findings in 14 files: two key prefixes, a private-key block, ten recovery-phrase lines; `ok_short_list.txt` is not flagged; `NOT scanned: 2 env-named file(s) (never opened), ..., skipped by extension: .pdf x1, 0 symlink(s), 1 folder(s) skipped by name` |
| `bash "$M/secret-scan.sh" ss/url_pw.txt`, `ss/query.txt`, `ss/bearer.txt` | `url_pw.txt:1:url-with-password`, `query.txt:1:token-in-query`, `bearer.txt:1:bearer-token`, exit 1 each. The value is not printed |
| `bash "$M/secret-scan.sh" ss/assign.txt` | four lines flagged `secret-named-assignment`, including `the admin secret is ...`; exit 1 |
| `bash "$M/secret-scan.sh" ss/hyphen.txt` | `hyphen.txt:1:recovery-phrase-hyphen-run`, exit 1 |
| `bash "$M/secret-scan.sh" ss/hex64.txt` | stdout empty, stderr `secret-scan: info: hex64.txt:1:hex64-info` and line 2, `0 finding(s)`, `2 line(s) hold a 64-digit hex string ... NOT a finding`, exit 0 |
| `bash "$M/secret-scan.sh" ss/good.txt` | `0 finding(s)`, exit 0. It holds `https://user:password@example.com`, `user:<password>@host`, `?key=short`, `?token=your-token-goes-here-please`, `Bearer <token>`, `token = process.env.GITHUB_TOKEN_VALUE_HERE`, a lower-case hyphenated `secret:` value, `API_KEY=YOUR_API_KEY_GOES_HERE_PLEASE` and a 15-word kebab-case sentence |
| `bash "$M/secret-scan.sh" named` where the file is called `sk-ant-` plus filler and holds a key | `named/<masked>.txt:2:anthropic-api-key`: the file name is masked; a search for the filler in the output gives 0 |
| `bash "$M/secret-scan.sh" perm/unreadable.txt`; `perm`; `link.txt`; `scan/nope`; no argument | `cannot read file: perm/unreadable.txt` exit 2; file and folder both named, exit 2; `NOT scanned: 1 env-named file(s) (never opened)`, exit 0; `no such file or folder: scan/nope`, exit 2; usage text, exit 2 |
| `zsh "$M/secret-scan.sh" scan/keys.txt` | `scan/keys.txt:1:anthropic-api-key` and `scan/keys.txt:2:github-token` |
| `bash "$M/secret-scan.sh" "$SKILLS/moi-devrel"` | `0 finding(s)`, exit 0, with the `hex64-info` lines (if any) listed on stderr |

## check-message.py
Moved here from the removed teammate-comms skill; re-run on 2026-10-04 from a `mktemp -d` scratch folder with `PYTHONDONTWRITEBYTECODE=1`, `CM="$M/check-message.py"`, commands `python3 "$CM" [options] file`. Exit 0 means no error-level finding (warnings are allowed), 1 at least one error, 2 bad input. Inputs were built at run time with `printf` and a few lines of Python. Every secret-shaped input is a known prefix plus filler (`sk-ant-`, `ghp_`, `eyJ` and repeated `zq`, repeated `ab12` for hex, twelve consecutive words from the BIP-39 list, `aB3dE5gH7jK9mN1p` for the mixed values), and the em dash is `chr(0x2014)`. A search of every output for the filler, the phrase words and the mixed value found nothing.
| # | Input | Options | Result |
|---|---|---|---|
| 1 | Good: a two-line DevOps request with a health URL, a UTC time and a dated deadline | `--to devops` | Exit 0. 0 errors, 0 warnings |
| 2 | Bad: `Owner:` and `Task:` labels, boilerplate, `<NAME>`, a token request, the platform wallet variable, Vercel, a rotate request for the agent-key secret, `ASK:`, "the operator", "12:00 AM UTC", "today", EST, a weakness term, an em dash | `--to devops` | Exit 1. 9 errors (boilerplate, em-dash, label-owner, never-rotate, placeholder, secret-ask, settled-subject, skill-marker, twelve-am-utc) and 8 warnings (label-line, no-date, no-question, operator-word, relative-time, security-detail, tz-abbreviation, vercel) | <!-- slop-lint: ignore -->
| 3 | Shaped like a secret: `sk-ant-`, `ghp_`, a JWT, a 64-digit hex string, a 12-word phrase, an IPv4 address | none | Exit 1. 5 `secret-shaped` errors, each "(value not shown)", and an `ip-address` warning showing "(masked ip)" |
| 4 | Secret shapes the first version missed: `admin secret is <mixed value>`, a URL with a password in it, `?token=` in a URL, `Authorization: Bearer ...`, `api_key = ...` | none | Exit 1. 5 `secret-shaped` errors, nothing echoed |
| 5 | A 12-word phrase one word per line; the same as a numbered list `1. word`; joined with hyphens on one line | none | Exit 1 each: 12 errors, 12 errors, 1 error. No word printed |
| 6 | Eleven words from the list on one line | none | Exit 0. 0 findings (the run is under 12) |
| 7 | An interaction hash (`0x` and 64 hex digits) in a protocol question | `--to protocol` | Exit 1. 1 `secret-shaped` error, with the hint to use `--hashes-ok` |
| 8 | The same file | `--to protocol --hashes-ok` | Exit 0. 1 `hash-shaped` warning, value not shown |
| 9 | "I will not send a token here" in a DevOps request | `--to devops` | Exit 0. 0 findings (draft 5 passes its own checker) |
| 10 | "please send me the token" | `--to devops` | Exit 1. 1 `secret-ask` error | <!-- slop-lint: ignore -->
| 11 | "Friday 2026-10-08" (a Thursday) | `--to devops` | Exit 1. 1 `weekday-date-mismatch` error naming the real weekday |
| 12 | "a vulnerability in the checkout page" | `--to devops` | Exit 0. 1 `security-detail` warning, which points to the repo-map row |
| 13 | Status with an unevidenced Done line, a shipped file name, future tense and "next week" | `--to status` | Exit 0. 4 warnings: future-claim, no-date, relative-time, status-no-open-items |
| 14 | Status with evidence, a To do, a Not verified and a numbered decision; and one with Partly done and To do in future tense | `--to status` | Exit 0 each. 0 findings; future tense is allowed under Partly done and To do |
| 15 | Four numbered protocol questions with a date; the same file with limits | `--to protocol`; then `--max-lines 2 --max-chars 50` | Exit 0. 0 findings; then two `long(warn)` findings |
| 16 | A message that names `moi-devrel` as the skill; a message that names `sarvalabs/moi-mcp`, `MOI-Webinars` and `moidocs` | `--to devops` | Exit 1 with a `skill-marker` error; exit 0 (repo names are not markers) |
| 17 | Bad: `.env`, `prod.env`, `.env.local`, `server.env.example` and a symlink to `.env` | none | Exit 2 each. "refusing to read ...: an env file can hold keys and is never opened" |
| 18 | Bad: a missing path, a folder, an empty file, a whitespace-only file | none | Exit 2 each. "no such file", "is a folder, not a draft file", "is empty" |
| 19 | Bad: a file with a NUL byte, a Latin-1 file, a 400 KB file | none | Exit 2 each. "looks binary", "is not UTF-8 text", "A message that long is a document" |
| 20 | Bad: a named pipe with no writer, `/dev/zero`, a file with mode 000 | none | Exit 2 each. "is not a regular file", "Permission denied" |
| 21 | Bad: no argument, `--to nonsense`, `--max-lines -3`, `--max-chars abc` | various | Exit 2 each. A usage line and the reason, no traceback |
| 22 | Edge: a byte order mark and CRLF line ends; a URL containing `?` and an email in angle brackets | none | Exit 0 each. 2 lines, 0 findings; neither the email nor the `?` in the URL counts as a placeholder or a question |
| 23 | Performance: 190 KB on one line of `secret`, `ab-`, `token=`, `token is a1b2c3d4e5f6 `, `send `, `abandon `, `_`, `://a:`, `Bearer `, `?key=a1b2c3d4`; and 20000 one-word lines | `--to status` | CPU time 0.1 to 0.2 seconds each. No traceback |
| 24 | The template file, which is full of placeholders by design | none | Exit 1. 48 lines flagged `placeholder`, plus the skill markers in its headings. Each of the 16 drafts in `templates/messages.md` was filled in with plain values and run with its own `--to` (draft 8 with `--hashes-ok`): 0 errors, and only the warnings its sample text invites |
