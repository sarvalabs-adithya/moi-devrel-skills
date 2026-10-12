# awesome-moi: maintaining the resource list

Facts are as of 2026-10-03, read from the public GitHub repo `moi-foundation/awesome-moi` that day. The research note of 2026-10-02 believed the structured README existed only on a branch. That is out of date: it is on `main`. Back to `../SKILL.md`.

## What it is
A curated markdown list of docs, papers, tools and tutorials for building on MOI. Public, MIT licence, no build and no deploy: a merge to `main` is the publication. It also carries the Sprint chapter table (`sprint.md`).

## State on GitHub (2026-10-03)
- `main` is at commit `1ed873a`, dated 2026-01-16, a merge by Rahul Lenkala of the previous operator's pull request #3 ("Restructure Awesome MOI with curated resources and MOI Sprint"). GitHub shows no push after 2026-01-16.
- Three pull requests exist in total, all closed, all from the two owners (the CODEOWNERS file and the first two content changes). No outside contribution has ever arrived. No open issue.
- Default owners in `.github/CODEOWNERS`: `@moi-rahul @sarvalabs-adithya @sarvalabs-rahul`. Who reviews now is not settled. ASK: Rahul.
- There is no CI, no link checker, no `CONTRIBUTING.md` and no pull request template. IDE files under `.idea/` are committed.
- Layout: `README.md` (index, Sprint chapter table, resource table, quick links), `essentials/` (docs, papers, community), `js-sdk/`, `coco-language/`, `developer-tools/` (Voyage, playgrounds, faucet), `resources/moi-sprint/` (a short Sprint README), and `solved-patterns/` and `web3-reimagined/` (both "Coming Soon", no content).
- Local only, on the previous operator's machine: a clone on branch `add-tswap-resource` (already on GitHub at `83653b1`) with two uncommitted edits: the Forge onboarding guide written over `resources/moi-sprint/README.md` (`forge-cohort.md`), and a trim of two links and one word in `js-sdk/README.md`. ASK: Adithya for a copy before anyone runs `git checkout .` there.
`DEPENDENCIES.md` (2026-10-01, the previous operator's file: ASK: Adithya for a copy) says the links have not been checked since January 2026, so the findings below are nine months of drift.

## What belongs (proposed: the repo states no criteria)
The only written rule is "Fork the repo, add your resource, and submit a PR", with these fields: name, short description, link, category (Paper, Network, Community). Proposed tests for a new entry. ASK: Rahul to confirm them.
1. First-party MOI material, or a third-party project that runs on MOI with a public repo.
2. Public and free to read. No private repository, no paid wall, no login.
3. The link works and is the canonical address.
4. A one-line description that states what it is. No claim about speed, price, partners or "first". Any claim is checked with `moi-devrel/claim-check`.
5. Wording follows `moi-devrel/references/terminology.md`. A tutorial that teaches a retired model (account-centric, "Global State Machines", "Interaction State Machine" as the engine) is refused until corrected. <!-- slop-lint: ignore -->
6. Nothing that pins a devnet id, an asset id or a faucet amount, because a reset breaks it (`moi-devrel/references/devnet.md`).
7. No promotion: a post that exists to sell something does not belong.

## How an entry is checked
Work in a working copy of `moi-foundation/awesome-moi`. The repo's own rule is fork, add, pull request.
| # | Step | Command or action | Done when |
|---|---|---|---|
| 0 | Working copy | Fork the repo and clone the fork. A fork and a clone are each a GATE (a clone is a download: name, source, size). In the clone: `bash "$SKILLS/moi-devrel/scripts/preflight.sh"`, then `git switch -c <branch>` | A clean branch and a passing identity check |
| 1 | Fit | Read the entry against the seven tests and the section it targets | Each test has a yes or a named reason |
| 2 | Links | From the repo root: `python3 "$SKILLS/moi-education-programs/scripts/link-check.py" <changed file.md>` (add `--root .` for links that start with a slash) | No DEAD. Every REDIRECT replaced by its new address. Every CHECK opened by hand |
| 3 | The thing itself | A repo: `curl -s https://api.github.com/repos/<owner>/<repo>` (a public read; read `visibility`, `license` and `pushed_at`), then does it run against today's SDK on devnet? A package: `npm view <name> version time`. A tutorial: follow it once on devnet (a GATE if it spends funds) | The date and result are written in the PR description |
| 4 | Wording | `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" <file>` | 0 errors. The list's existing emoji headings are the repo's own convention: ASK: Rahul whether new text follows them |
| 5 | Format | `$SKILLS/moi-education-programs/templates/list-entry-format.md` | Name, description, link, category are all present |
| 6 | Batch | Put every fix from one review on one branch and open one pull request | One PR. No AI co-author line or footer |
| 7 | Ship | Push, open the PR, merge: GATE each. A merge publishes a public list | Rahul's yes is in the conversation |

## What is wrong today (link check run 2026-10-03 over all 8 markdown files, with `--include-code`)
| File and line | Finding |
|---|---|
| `README.md` 23 | The Chapter 1 link points to `resources/moi-sprint/Chapter 1 - Native Assets.md`. The file was deleted on 2026-01-13. Chapter 1 now lives in `moi-foundation/moi-sprint` (`01-native-assets`). Chapters 2 and 3 are "Coming Soon" with no file |
| `coco-language/README.md` 28 | The Coco download link `github.com/sarvalabs/coco/releases` answers 404. The install page is cocolang.dev/docs/install and the releases are at cocolang.dev/docs/releases |
| `coco-language/README.md` 69 | The link `../resources/tswap/TUTORIAL.md` does not exist (the folder was removed). A `TUTORIAL.md` exists on tSwapper's `solution` branch, beside the full solutions: decide if that should be linked |
| `coco-language/README.md` | The install steps use `coco-0.7.0`. Coco v0.9.2 was released 2026-09-28 |
| `js-sdk/README.md` 16 | `docs.moi.technology/docs/build/packages/js-moi-sdk/` answers 404 (the local edit already drops it) |
| `js-sdk/README.md` 29 | The code sample uses the old `.../babylon/v0` RPC address, which timed out twice. The sample must be rewritten against the current SDK and run |
| `developer-tools/README.md` | Playground links use `?network=babylon`; the faucet text says 20K KMOI. A link check cannot catch either, because Voyage answers 200. Open them by hand |
| `README.md`, `essentials/`, `developer-tools/` | Two different Discord invite codes. All redirect to discord.com, which does not prove an invite is valid. ASK: Rahul which is canonical |
| `essentials/README.md` 11 | The "Concept Paper" link (Medium) answers 403 to a script. Open it by hand. It explains an "Interaction State Machine", which predates the 2026-09-14 wording |
Totals: 56 links, 47 fine, 3 redirected, 5 dead (2 missing local files), 1 to open by hand.

## How the list goes stale
| Trigger | Where to look | Detect with |
|---|---|---|
| A devnet reset | Any id, sample address or "live" sentence | `moi-devrel/references/devnet.md`, "Before you say live" |
| A js-moi-sdk release | Install lines and code samples. the newest on npm was `0.9.0-rc2` on 2026-10-03 | `npm view js-moi-sdk dist-tags time` |
| A Coco release | Install pin, language samples (v0.9.2 rejects `enlist` endpoints) | cocolang.dev/docs/releases |
| A docs reorganisation | Paths on docs.moi.technology and the SDK docs | the link check |
| A network or product rename | `babylon`, "IOMe" (Voyage moved to MOI Wallet in late August 2026), "testnet" | `grep -n -i "babylon\|iome\|testnet" <file>` |
| A deleted or moved file in this repo | Relative links | the link check (it also tests letter case, which GitHub enforces) |
| Time | "Coming Soon" sections without a date | proposed: recheck monthly and after every SDK, Coco or reset event |

## Not yet known
- Whether this is the Sprint home or the Foundation's general list. The January README tried to be both. ASK: Rahul.
- Who keeps it current and who may merge. ASK: Rahul.
- Whether the previous operator's local trim of `js-sdk/README.md` was meant to ship. ASK: Adithya.
