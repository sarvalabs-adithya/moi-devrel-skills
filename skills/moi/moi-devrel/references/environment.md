# Environment: tools, checks and machine quirks

Facts are as of 2026-10-02 (the scripts were last changed and tested 2026-10-03). All the evidence comes from one macOS machine running zsh, so treat every quirk as macOS until the operator says otherwise. Back to `../SKILL.md`.

## 1. Tools
Set `SKILLS` and run `bash "$SKILLS/moi-devrel/scripts/preflight.sh"` first, from inside the repo (see `../SKILL.md`, "Before you start"). It checks all of these in one go and prints PASS, WARN or FAIL. The table says how to check each by hand.

| Tool | Needed for | Check | If missing |
|---|---|---|---|
| git | everything | `git --version` | FAIL. Install it, then set your work identity (`consent-and-identity.md`). |
| gh | PRs, login, and `gh secret set` (which needs a yes, `consent-and-identity.md` section 1) | `gh --version`, then read the login line from `preflight.sh`. Never paste `gh auth status` output. | FAIL. Install GitHub CLI, then log in yourself with `gh auth login`. |
| node | `scripts/buffer.mjs` in `moi-foundation/MOI-Webinars` (on branch `claude/agent-payments-simple`, not on `main` as of 2026-10-02; its `--thread-dir` option was in a commit that was not pushed as of 2026-10-03: not recorded (the previous DevRel's notes); ASK: Rahul; v24 was used), docs site builds, `node --check` on a deck's script | `node --version` | FAIL. moidocs and voyage-docs need 16.14 or newer, coco-docs 18 or newer. |
| python3 | `slop-lint.sh`, `time-table.sh`, `secret-scan.sh` and `check-message.py` in this skill (`preflight.sh` checks that it exists), `make html` for the js-moi-sdk docs | `python3 --version` and `python3 -c "import zoneinfo"` | FAIL. 3.9 or newer for `time-table.sh`. |
| Google Chrome | headless PDF export of a deck and PNG export of a design card (`moi-devrel/design`, step 9), no login needed | `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --version` | WARN. Only deck and card export need it. |
| poppler | `pdfinfo`, `pdftotext`, `pdftoppm` to check a PDF's page count, text and a rendered contact sheet | `pdfinfo -v` | WARN. Only PDF checks need it. |
| curl | live reads such as the `net.Version` call, crawler checks | `curl --version` | ships with macOS |
| docker | third-party agent frameworks (`consent-and-identity.md` section 7) | `docker --version` | install only when that work comes |
| pnpm | the Points Program (`sarvalabs/moi-project`): install and `pnpm run ci` | `pnpm --version` | install only when that work comes (a download: a yes first) |
| make | the js-moi-sdk docs: `make html` and `make llms` in `docs/` | `make --version` | install only when that work comes (on macOS it comes with the Xcode command line tools; a download: a yes first) |
| pandoc | optional: Word copies of markdown for the internal review gate, markdown stays the source | `pandoc --version` | optional |

## 2. Scripts in this skill
Run them with `bash` (`python3` for the `.py` one), from the working copy of the repo you are in, writing the path in full with `$SKILLS` (the folder that holds the `moi-*` skills). All use Python 3 standard library or plain shell, work in bash 3.2 and zsh, and print no secret. The scripts of the branches (`ship`, `claim-check`, `call-digest`, `test-round`) sit in their own `scripts/` folders and are named in each `GUIDE.md`.

| Script | Use | Exit codes |
|---|---|---|
| `bash "$SKILLS/moi-devrel/scripts/preflight.sh"` | before any commit, PR or post: tools, git identity, personal-mail WARNs, AI co-author and "generated with" WARNs for eight assistant names (the list in `moi-devrel/ship/scripts/ship-preflight.sh`), the active `gh` login (every `gh` call has a timeout, `PREFLIGHT_GH_TIMEOUT` seconds, default 15), the origin remote with no credentials. Reads `PREFLIGHT_WORK_DOMAINS` and `PREFLIGHT_EXPECT_GH_LOGIN` (`consent-and-identity.md` section 2) | 0 no FAIL (WARN lines still exit 0, so read them), 1 a FAIL |
| `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" <file...>` | on any draft of public text: em dashes, contrast constructions, retired and wrong terms. Inside a code fence only the em-dash and `ai-attribution` rules apply. An unclosed fence is an error | 0 no error-level hit, 1 error-level hit, 2 bad usage |
| `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "<YYYY-MM-DD HH:MM>" <area/city zone>` | before scheduling: one instant in UTC, India, US Eastern, US Pacific, Central Europe, Singapore. The zone is `UTC` or area/city such as `America/New_York`. `EST`, `PST`, `IST` and other abbreviations are rejected | 0 printed, 2 bad input or rejected zone |
| `bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" <path>` | before a folder is shared or a transcript or log is saved: `file:line:rule` only, then a summary of what was not scanned. Knows key prefixes, URL passwords, token and key query values, bearer values, secret-named assignments and recovery phrases (also hyphen-joined). A 64-digit hex string is an `info` note on stderr and never changes the exit code. A backstop, not proof | 0 clean, 1 findings, 2 usage error or something could not be read (the scan is incomplete) |
| `python3 "$SKILLS/moi-devrel/scripts/check-message.py" --to <kind> <draft>` | before a teammate message goes to the operator (`house-style.md` section 4): a placeholder left in, an em dash, a skill marker, a secret shape or a request for a secret, a relative time, a weekday that does not match its date, a settled DevOps subject, a status line with no evidence. Kinds: devops, protocol, reviewer, status, other. Never opens an env file. A clean run does not show a claim is true | 0 no error-level finding, 1 an error, 2 bad input |

## 3. Machine quirks
| Quirk | What happens | Do this | Source date |
|---|---|---|---|
| The shell is zsh | Commands written for bash fail. `read -rsp` gave "read: -p: no coprocess". macOS bash is 3.2, with no associative arrays and no `mapfile`. | Write commands that work in zsh. Keep scripts to bash 3.2 features. For a hidden prompt use the zsh form in `consent-and-identity.md` section 4. | about 2026-08-24; bash 3.2 checked on the build machine 2026-10-02 |
| Wrong directory, missing file | The MOI-Webinars `scripts/buffer.mjs` was "not found" because the command ran inside `session-8-policies/`. A `cd` into a missing folder failed. | Put a `cd "$(git rev-parse --show-toplevel)"` first in every command you hand over, and check the file exists. | 2026-08-31 |
| Paths with spaces | Some checkouts sit in folders with spaces in the name. | Quote every path. | 2026-10-02 |
| Downloads and Desktop are blocked | macOS stopped the tool reading `~/Downloads` four times (EPERM) and `openssl` failed on the Desktop with "Operation not permitted". | Ask the operator to copy the file in, and give the exact command: `cp ~/Downloads/<file> "$(git rev-parse --show-toplevel)"/<file>`. | 2026-08-27 |
| Generated files and rebases | Docusaurus repos rebuild `llms.txt`, `llms-full.txt`, the sitemap and `.md` copies on every build and do not commit them. js-moi-sdk docs commit them (about 22,000 generated lines in PR #150 on 2026-10-01). A rebase once restored an older copy of a page another PR had updated (commit 0899368). | In the Docusaurus repos a generated file in your diff is a mistake: drop it from the commit. In js-moi-sdk docs, if a rebase stops on a generated file, take the target branch's copy, finish the rebase, then run `make llms` in `docs/`. Never hand-merge or hand-edit a generated file. After any rebase, diff the pages against main. The generated-file steps are a library rule, not a recorded incident. | 2026-10-01 |
| Stale artefact after "regenerate" | The previous operator saw the old deck and script three times in a row. | Name the exact fresh file path and URL, start the server on a new port, and read the served page for a string only the new version has. | 2026-09-04 |
| Stopping servers | Killing by name can stop another session's server. Several sessions share one machine, and one was editing `moi-mcp` while the research ran. | Note the PID or port when you start a server and stop only that. Never use `pkill`, `killall` or a `kill` built from `ps` and `grep`. If a port is busy, use a new port and tell the operator the URL. This is a library rule, not a recorded incident. | 2026-10-02 |
| Shared stash | `git stash` is shared by every worktree of a repository. | Use a temporary WIP commit instead. If you must stash, use `git stash push -u -m "<unique tag>"` and restore with `git stash apply <sha>`. | git behaviour |
| Remote or cloud sessions cannot push | Pushes returned 403, and the work came back as `.bundle` files moved by hand. | Package the work as a bundle or write a handoff prompt. | 2026-08, day not recorded |
| GitHub Actions outage or billing block | Scheduled jobs such as the Mailchimp RSS newsletter may silently not run. The previous operator retried "try now" seven times. | Check the run list, do not assume. Retry about every four hours, not every ten minutes. | 2026-08-28 to 2026-08-30 |
| Discord and long text | A long message became a `message.txt` attachment. | Split it into numbered parts or put it in a document. | 2026-09 |
| Time zones | The audience is announced in IST and the protocol runs on UTC. A run time was once displayed in the wrong zone (01:15 for a 9:15 US Eastern run, written "EST"). | Ask for the operator's zone once, give it as area/city (`America/New_York`, never `EST`), then print every time with `time-table.sh` before scheduling. | about August 2026, day not recorded (inferred from position in the request log; not recorded elsewhere) |
| Files that exist on one machine | Until 13 October 2026 `community-call-14/` and `intro-session/` in MOI-Webinars were untracked and lived on one machine. The decks for calls 2 to 14 are now in `community-call-N/deck/` (PR #2) and the intro-session deck is in the handover repo. | Before you rely on a file, check that it is in git or the handover repo, and back it up. A lost laptop loses the rest. | 2026-10-13 |

## 4. Safe habits
1. Scratch work goes in a directory from `mktemp -d`. Delete it when you finish.
2. Read-only first: `git status`, `git log`, `git diff` before any change.
3. A script that changes something outside its own output file needs a `--confirm` flag and says what it will do first.
4. Say which file or URL is fresh every time you regenerate anything.

## Not yet known
- The operator's operating system. Chrome's path, the Downloads block and the zsh default are macOS facts. Ask the operator which system they use at the start.
- Which Node version the webinar demo repos need: `engines` says 20 or newer, yet the live scripts run `.ts` directly. Not recorded (the previous DevRel's notes); ASK: Rahul.
- Whether the sarvalabs org requires signed commits outside the x402 upstream repo. ASK: Rahul.
