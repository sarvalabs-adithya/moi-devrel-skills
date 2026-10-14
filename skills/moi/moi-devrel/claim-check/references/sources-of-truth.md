# Sources of truth: the order of authority and how to reach each

Facts are as of 2026-10-02. `ASK: <person>` is defined in `moi-devrel/SKILL.md`. Back to `../GUIDE.md`.

## The order
For a claim about what MOI does or announced, the order is ranks 1 to 4. "Is it live" is its own question: a live read answers it and outranks the source tip for it.
| Rank | Source | Public? | Settles | Limit |
|---|---|---|---|---|
| 1 | Tagged source: go-moi at the release tag, go-pisa, cocolang; the published packages js-moi-sdk, js-polo, js-moi-identifiers | The packages and `sarvalabs/js-moi-sdk` yes. go-moi, go-pisa and cocolang are private as of 2026-10-02 | What a version does | Read the tag. The `develop` tip is not the release |
| 2 | The protocol team's release note, quoted verbatim | Sent to the team | What the team announced | A lead, not evidence. August 2026 notes were wrong in at least two places |
| 3 | An earlier MOI post, such as the release post in `sarvalabs/MOI-Website` | Public | Consistency with what MOI already said | A derived text. It can carry an old error |
| 4 | docs.moi.technology | Public | A cross-check | The weakest. Its interaction op-code numbers were swapped against the node source at v0.12.0 (August 2026). The only record is a line in the release-blog research of 2026-10-02 and the previous operator's older copy of the `moi-blog` skill. It was not re-checked since and cannot be checked from a repo (that copy is not recorded; ASK: Rahul). Other skills repeat it as a dated August 2026 fact |
| Own question | A live read of devnet | Public endpoint | Whether something is live now, and the wire field names | Proves now, never since (`live-reads.md`) |
For a question about the world outside MOI (a comparison, a standard, a statistic), the source is the other party's own public page, fetched now and dated. On 2026-09-10 the tip had `fee_payer` and devnet still answered `payer`, which is why a live read outranks the tip for "is it live".
If sources disagree, source beats note, note beats docs. Where the note and the source disagree and nobody can rule, word the text so it contradicts neither and raise the discrepancy separately (August 2026, commit `5c0f763` in `sarvalabs/MOI-Website`). Do not silently pick a side.

## Private source
- It may be read where the operator has it. It is never cited, quoted or linked in public text: no file path, no line number, no excerpt. Public text cites only what a reader can open: js-moi-sdk, js-polo, the docs, the explorer, or behaviour visible on the wire. Private clones are for checking, not citing (standards rule, 2026-09).
- A ledger is an internal working file. It may name a private file in `source`, so the ledger stays out of any public repo. The example ledger does this and says so.
- Reading does not change the clone. Use `git -C <clone> show <ref>:<path>` and `git -C <clone> grep -n "<pattern>" <ref> -- "<glob>"`, where `<ref>` is a tag such as `v0.13.0`. Do not check out, pull or push. If the tag is not in the clone, check `git -C <clone> tag -l "v0.1*"` first, and look for a second clone. `git fetch --tags` downloads from the remote and writes tags and objects into the clone, so it is not a read: it needs the operator's yes, with what it fetches and from where. Write the ref you read in `note`.
- When a claim can only be proved from private source, the public sentence says what the wire shows, or it is softened or cut. "Observed on the wire: ..." is the accepted shape.
- A newcomer has no clone. How to get access: an org admin of each repo grants read access to `sarvalabs/go-moi`, `sarvalabs/go-pisa` and `sarvalabs/cocolang` (`moi-devrel/references/keys-and-access.md` lists it as owner TBD). ASK: Rahul who the admin is. Until then, a claim that goes beyond the release note's own words stays `unverified`, never `verified` (release slide checks, 2026-10-02: post-only claims are unverifiable until traced to source).
- The previous operator had clones of go-moi (tip `develop`), go-pisa, cocolang and js-moi-sdk on his machine and read them read-only, using `git show origin/develop:<path>`. The v0.13.0 tag was not in the go-moi clone used for `../examples/september-release/` (tags up to v0.12.0, tip of 2026-09-07), so that ledger says "at the tip" wherever it relies on go-moi. A second go-moi clone on the same machine does have the tag: the `v0.13.0` tag commit is dated 2026-09-10 12:50 IST (07:20 UTC), sits on the `main` branch and not on `develop` (read 2026-10-02). Four of the example's go-moi citations (the executor refusal, the reserved asset standard, the asset limits, the redundant participant error) hold at the tag as well. That clone is not available after the handover: clone go-moi yourself once Rahul grants access, and check out the tag.

## How to reach each source
| Source | How | Gate |
|---|---|---|
| Release note | Ask the protocol team through the operator. ASK: Gokul where this version's note is. Save it unedited next to the text, and write "unedited" in its header only if it is | None |
| Published package version | `npm view js-moi-sdk dist-tags` and `npm view js-moi-sdk@<version> dist.unpackedSize` read metadata. On 2026-10-02 `latest` was 0.9.0-rc2 for js-moi-sdk and 0.1.5 for js-polo | None |
| Package source | Open `sarvalabs/js-moi-sdk` (public, `main`) in a browser at the tag. Or `npm pack <name>@<version>` into a scratch folder | `npm pack` downloads a file: state its name, source and size, and ask first |
| docs.moi.technology, voyage-docs, ethereum.org and other pages | A browser, or a read-only HTTP GET. Quote at most 15 words | None |
| Devnet | `live-reads.md` | Read methods only. Never submit an interaction |
| Explorer | https://voyage.moi.technology for hashes and receipts. It can lag by minutes | None |

## What each source cannot prove
- A package constant that mirrors the chain is a copy: the SDK's own comment says the blockchain is the source of truth for the minimum storage deposit (`js-moi-constants` `storage.js`).
- A passing test against the tip does not show the release behaves the same.
- A release note proves what was announced. Paraphrasing it into a stronger sentence adds a claim that needs its own source ("support" became "the versions to pair with" in the September post; example row C021).
- A source read on the day of one check says nothing about the day of the call. Date every read.

## Specs and upstream filings
A spec for an external standard (x402, CASA) went through seven rungs in September 2026. Each rung catches what the one before cannot:
1. The public package source: install the real dependencies fresh and read the shipped type files.
2. The upstream's live state: recount with its public API, quote its docs verbatim.
3. Private source, read-only, then phrase the public text without private paths.
4. The live network: probe devnet and transcribe a real settled interaction.
5. Mechanical: type check, lint, formatting, tests.
6. Comparison with the closest merged package from another chain.
7. An adversarial sweep of design claims, and a check that every citation an agent produced exists.
Record each pass in the commit message and the status file with what it refuted. Fix a refuted claim everywhere it appears. The record is in `caught-claims.md`, section E.

## Not yet known
- The original text of the v0.13.0 release note. The copy in this library is restructured and its header says "unedited". ASK: Gokul or Rahul where it was posted.
- How the protocol team delivers a release note, and who besides Gokul is the contact. ASK: Rahul.
- Whether the v0.13.0 tag of go-moi is readable by the next operator, and who grants access. ASK: Rahul. Whether the example's other go-moi citations hold at the tag: re-read them, they were checked at the tip only.
- Whether `docs.moi.technology` still has the swapped op-code numbers. Not re-checked since August 2026. ASK: Gokul.
