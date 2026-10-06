# MOI claim check

Branch of `moi-devrel`. `$SKILLS`, the operator, `ASK:`, the house rules and the gates are in `moi-devrel/SKILL.md`; this guide adds what is specific.

## What this covers
Every sentence that states something checkable in text that leaves the team: posts, slide text and presenter notes, scripts read aloud, social copy, docs pages, spec text, PR descriptions. The result is a ledger (one CSV row per claim, with a verdict and a source) and a text edited to match it. A release note is a lead, not evidence: the August 2026 notes were wrong in at least two places (as of 2026-10-02).
Not covered: writing the text (`moi-blog`, `moi-webinar`), building decks (`moi-webinar/deck`), house wording (`moi-devrel/references/house-style.md`). Docs pages are written and reviewed with `moi-docs`, which calls this branch on the changed pages; `moi-docs/references/page-standard.md` carries the docs rules. The numbers ledger of `moi-webinar/community-call` is a narrower sibling that checks the figures printed on slides. Keep both for a call and do not merge them (`references/method.md`, section 4).

## Before you start
Run every command from the working copy of the repo you are working in, with the path quoted. `<slug>` is a short lowercase name for the text, for example `september-release`. The **tag** is the commit a release was cut from (`v0.13.0`). The **tip** is the newest commit on `develop`, which can differ from any release.
- [ ] The final text, in every place it appears: post, deck and its `NOTES` (the presenter-notes array in the deck's HTML), `SCRIPT.md`, social copy, YouTube description. The operator provides. Ask: "Which files carry this text, and is this the final wording?" A rewrite after the check reopens it.
- [ ] For a release: the protocol team's note as sent, saved unedited as `claim-check-<slug>/RELEASE-NOTE.md`. ASK: Gokul where this version's note is.
- [ ] Read access to the protocol source (go-moi, go-pisa and cocolang are private as of 2026-10-02). ASK: Rahul who can grant it. Without it, a protocol behaviour claim that goes beyond the release note's own words cannot be `verified`: leave it `unverified` and say so (`references/sources-of-truth.md`).
- [ ] Any claim the operator already doubts, as a numbered list.
- [ ] Whether a second independent pass is wanted. The operator decides; sub-agents only when the operator asks, with the count stated first (`references/independent-check.md`).

## The run
The ledger folder `claim-check-<slug>/` sits at the root of the working copy and stays out of git: a ledger names private files and people, and `moi-foundation/MOI-Webinars` and `sarvalabs/MOI-Website` are public. Step 1 makes it self-ignoring. The ledger file is always named `ledger.csv`. A skill that calls this branch can name another folder for it (`session-<N>/` in `moi-webinar`, `protocol-release-<version>/` for a release pack in `moi-blog/release-pack`, `$WORK/<slug>/` for a post in `moi-blog`): use that path, and keep it out of git the same way.
For one sentence ("is this true?"), answer yes or no first, then the source and the verdict, and open a ledger only if the text will go out.

| # | Step | What to do, and the command | Done when |
|---|---|---|---|
| 1 | Collect the text | `mkdir -p claim-check-<slug> && printf '*\n' > claim-check-<slug>/.gitignore` (the `*` hides the folder, itself included, from `git add`). Gather the final text of every place the claims appear. For a release, save the note unedited in `claim-check-<slug>/RELEASE-NOTE.md`. List the files | Every file is named, and the operator confirmed the wording is final |
| 2 | Extract | `python3 "$SKILLS/moi-devrel/claim-check/scripts/extract-claims.py" --all <file> [more files] > claim-check-<slug>/claims-candidates.csv && cp -n claim-check-<slug>/claims-candidates.csv claim-check-<slug>/ledger.csv`. Pass paths relative to the working copy so `where` stays short. `--all` lists plain statements the default run skips. `cp -n` never overwrites a ledger you have filled in. Never run step 2 twice: later changes go through step 8 | Candidates exist. The raw file stays untouched |
| 3 | Classify | Read every row of `ledger.csv`. Delete a row only if its sentence states nothing checkable: step 8 knows about dropped rows because `claims-candidates.csv` stays as extracted. Split a sentence that needs two checks. Fix `type` with `references/claim-types.md`. Read the text once yourself against the rows | Every kept row is one claim with a type. The count of dropped rows is noted |
| 4 | Pick the authority | For each type choose the source that settles it: `references/sources-of-truth.md`. A "live" claim needs a read of the node | Each row has a named source to try, or an ASK |
| 5 | Check | `references/method.md`. Search for a counterexample to a universal. Read the tag, not the tip. Recompute arithmetic. Run read-only devnet reads from `references/live-reads.md`. Never submit an interaction | Each row has evidence or a reason it has none |
| 6 | Give a verdict | Fill `source`, `verdict`, `checked_by`, `as_of` (YYYY-MM-DD), `note` in the ledger. Quote a release note verbatim in the text and cite its section here | No row has a verdict without its fields |
| 7 | Change the text | For each claim that was wrong or too wide: show the operator the exact sentence before and after, and wait for a yes. `scoped`: write the limit into the sentence. `argument`: label it. `cut`: remove it, then search for what it leaves behind. Search every other copy of the text. A copy in a shared system (Drive, Luma, a Buffer draft, a YouTube description) is the operator's to edit: hand over the corrected sentence | The text on disk matches the ledger. The operator approved each edit |
| 8 | Re-run | `python3 "$SKILLS/moi-devrel/claim-check/scripts/extract-claims.py" --all --against claim-check-<slug>/ledger.csv --dropped claim-check-<slug>/claims-candidates.csv <files>` lists sentences the ledger does not cover and cut sentences still in the text. Add rows (`references/method.md`, "Re-run"), check them, repeat. Then `python3 "$SKILLS/moi-devrel/claim-check/scripts/ledger-status.py" claim-check-<slug>/ledger.csv` | `--against` exits 0 and `ledger-status.py` exits 0 |
| 9 | Hand back | The format at the end of this file | The operator has read it |

Interface that `moi-blog` (posts, and `moi-blog/release-pack`), `moi-webinar` (with `moi-webinar/community-call` and `moi-webinar/deck`) and `moi-docs` call, kept exactly:
- Ledger columns, in this order: `id,claim,where,type,source,verdict,checked_by,as_of,note`. The ledger file is `ledger.csv`; `templates/claim-ledger.csv` is only the seed that a scaffold copies to it (a header and one `#` comment row, which the scripts skip).
- Verdicts: `verified` (needs a source), `scoped` (true only with a stated limit, and the limit is written into the text), `argument` (an opinion, labelled as one in the text), `cut` (removed from the text), `unverified`.
- `scripts/extract-claims.py <file> [more files]` prints candidate claims as rows, all `unverified`. It flags sentences by trigger words and over-collects on purpose, and it also misses plain statements: `--all` lists every sentence. `scripts/ledger-status.py <ledger.csv>` prints the count per verdict and exits 0 only when no row is unverified, verified without a source (a placeholder such as TBD is not one), scoped without a note, or checked by nobody. Exit 1 means rows stand. Exit 2 means unreadable or malformed input, including a row with more cells than the header, a file that starts with a byte order mark (`--allow-bom` accepts one) and an env file. Both scripts mask secret shapes in what they print and refuse to open an env file.

## Which file to read
| Doing | Read |
|---|---|
| The method in full, a worked example, the two ledgers | `references/method.md` |
| Which source settles a question, private source rules, how to get access | `references/sources-of-truth.md` |
| Is it live, read-only checks against devnet | `references/live-reads.md` |
| What each kind of claim needs, and what makes it unverifiable | `references/claim-types.md` |
| What was caught wrong before, with dates | `references/caught-claims.md` |
| A second independent pass, sub-agents, cost | `references/independent-check.md` |
| A finished ledger to learn from | `examples/README.md` |
| Testing a change to this branch | `evals/evals.md` |

## Facts that fail silently
| Rule | The incident |
|---|---|
| Treat a release note as a lead and check the claim in source at the tag | The August 2026 notes named exports that do not exist at v0.8.0 and listed as new a method that was only renamed (2026-08-19) |
| Check against source, not against the draft or the status file | A status file said a key id was pinned while the code did not check it (2026-09-10) |
| Say which build you read. A feature in the `develop` tip is not the release and is not live | `fee_payer` was in the tip on 2026-09-07 while devnet still answered `payer` on 2026-09-10. A second clone on the previous operator's machine has the v0.13.0 tag, which the clone behind the example ledger lacked (read 2026-10-02): read the tag |
| A live read proves now, never since | The September post says live "since 11 September". The explorer's oldest listed interaction is dated 2026-09-10 13:18 UTC and its list stops at 355 entries (read 2026-10-02) |
| A field that is present is not a feature that is used | On 2026-10-02 all 346 readable listed interactions carried an all-zero `fee_payer`, which means no delegation (`references/live-reads.md`) |
| Test a universal by looking for one counterexample | "Every action on MOI costs fuel" was removed as untrue (2026-09-11). Reads cost no fuel, and an interaction whose payer cannot cover the fuel is not charged <!-- slop-lint: ignore --> |
| A correction must reach every copy | A claim proved false on 2026-08-07 survived in five more files and in the speaker notes of the presented deck |
| A limit stated in one section can vanish in another | The recap said "take on users that hold no KMOI" where the body said "pay fuel" (example row C186) |
| Recount after every edit | Namespace counts went 55, 50, 49; a "27 errors" headline met a table of 26 and a list of 25 |
| Open every citation an agent or a draft gives | Two spec citations produced by agents did not exist (2026-09-10) |
| Write a release time as a date, 00:00 UTC form and India time | "today at 12:00 AM UTC" was read as noon and two posts were scheduled wrong (2026-09-10) <!-- slop-lint: ignore --> |
| Keep the `-rc` suffix. A release candidate is not shipped | A CC13 slide said `js-moi-agent-registry v0.3.0-rc1` shipped (2026-08-27) <!-- slop-lint: ignore --> |
| Private source informs the check and never appears in public text | Standing rule since 2026-09 (`references/sources-of-truth.md`) |
| A clean `scripts/ledger-status.py` covers only the rows in the ledger. The extractor does not see images, charts, PDFs or lines the speaker adds | Slide figures once sat in screenshots and typed messages, not in the deck text (CC14, 2026-09-24) |
| A default extraction is not the whole text | On the September post the default run skipped 50 of 246 sentences, among them "Any fixed storage amount in your code is now a millionth of what it needs to be." and "Both are on npm." (2026-10-02) |

## Gates
Every gate in `moi-devrel/SKILL.md` applies (identity, secrets, spend, sub-agents, AI co-author lines). These are the ones this branch meets most:
- Committing or pushing a ledger or a changed text, opening a PR, merging, publishing, posting, scheduling or sending anything. A push to `moi-foundation/MOI-Webinars` publishes.
- Sending any question to Gokul, Rahul or anyone else. Claude drafts, the operator sends.
- Downloading anything to read it: `npm pack`, a clone, `git fetch` (it writes to the clone). State its name, source and size first.
- Uploading or sharing a ledger or a text in cloud storage, or editing a copy in a shared system (Drive, Luma, Buffer, YouTube).
- Anything that spends devnet funds, deploys, or submits an interaction (a wallet step: the operator signs and runs it). Live reads are read-only methods only.
- Saying a claim is "verified" to the author or a reviewer before the ledger shows it.

## Keys and access
Names only. The scripts need no key. Reading the protocol source needs GitHub read access to `sarvalabs/go-moi`, `sarvalabs/go-pisa` and `sarvalabs/cocolang` (private as of 2026-10-02): an org admin of each repo grants it, ASK: Rahul who. Public packages and docs need none. Never open an `.env` file or paste a key or a recovery phrase into a ledger cell. If a recovery phrase turns up in a text or a ledger, do not repeat it and tell the operator it is exposed. Where each credential lives: `moi-devrel/references/keys-and-access.md`.

## Hand-back
```
Checked: <files> on <date>. Ledger: <path>
Counts: verified N, scoped N, argument N, cut N, unverified N. Rows dropped as not claims: N of M
Text changes: <numbered, each with its row id and whether the operator approved it>
Open: <each unverified row, with who can settle it>
Not read: <private source unavailable, live read not done, images not checked>
Ready: yes or no, because <one reason>
```
Ready is yes only when `scripts/ledger-status.py` exits 0, `--against` exits 0, the operator has read every `scoped` and `argument` row, and the text on screen is the text that was checked. A status lists work that was done. A to-do is labelled as one.
