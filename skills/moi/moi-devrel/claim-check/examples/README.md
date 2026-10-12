# Example: the September 2026 release post, checked

A worked claim ledger built on 2026-10-02 from a real file: the post "MOI September 2026 Release" for moipod v0.13.0. It is a snapshot in the middle of a run, not a finished one. It shows what the extractor produces, what a checked row looks like, and how a row that cannot be closed is left. Read it before the first check you run. `SKILLS` is the folder that holds the `moi-*` skills, quoted if it holds spaces.
This copy is cleaned for sharing. A `source` cell that rests on private source (go-moi) says "private source", gives the tag or the tip date and the read date, and describes in words what was read. It holds no file path, function name or commit id of private code, and no person's name sits in a `source` or `checked_by` cell. The 64-character KMOI asset id in `BLOG.md` is public (it is in the live post and js-moi-sdk 0.9.0-rc2 exports it as `KMOI_ASSET_ID`) but has the shape of a key, so the two copies of it in this example are shortened to `0x1080fffe4cd973c4...00000000`, and the two ledger rows that quote them (C031, C113) read the same way.

## What is here
| File | What it is |
|---|---|
| `september-release/BLOG.md` | The post, 202 lines. Copied on 2026-10-02 from `protocol-release-0.13.0/BLOG.md` on the previous operator's machine, where it is untracked and local only (ASK: Adithya for a copy). The research records it as byte-identical to the published post in `sarvalabs/MOI-Website` (`blog/src/content/posts/moi-september-2026-release.md`, merged 2026-09-11, commit `280ffb2`). A GET of the live page on 2026-10-02 showed the same wording on every phrase tested. Five lines (10, 40, 45, 46, 66) carry a `slop-lint: ignore` marker because the post quotes forms the lint flags. Remove the markers and restore the two shortened asset ids and the file equals the original, and on 2026-10-02 it also equalled the file on `main` of `sarvalabs/MOI-Website`: `sed -e 's/ <!-- slop-lint: ignore -->$//' -e 's/ # slop-lint: ignore$//' BLOG.md` |
| `september-release/claims-candidates.csv` | The raw output of the extractor: 196 rows, all `unverified`. One edit: the `note` cell of five rows (C008, C056, C060, C061, C078) holds `slop-lint: ignore`, because those sentences quote forms the lint flags |
| `september-release/ledger.csv` | The same 196 rows. 57 are resolved (54 verified, 3 scoped) and 30 more carry a reason or a proposed edit but stay unverified. The ids are the same. No row was dropped |

## How it was made
To repeat it, copy the example into a scratch folder and run from there, so `where` reads `BLOG.md:55` and nothing is written inside the branch folder:
```
EX="$SKILLS/moi-devrel/claim-check/examples/september-release"
W="$(mktemp -d)" && cp "$EX/BLOG.md" "$EX/ledger.csv" "$W/" && cd "$W"
python3 "$SKILLS/moi-devrel/claim-check/scripts/extract-claims.py" BLOG.md > claims-candidates.csv
python3 "$SKILLS/moi-devrel/claim-check/scripts/ledger-status.py" ledger.csv
python3 "$SKILLS/moi-devrel/claim-check/scripts/extract-claims.py" --against ledger.csv BLOG.md
```
The extractor read 251 sentences and flagged 196, which is the over-collecting this branch describes: a bare product name or a small number is enough. It was run without `--all`, which did not exist then. With `--all` it lists 246 rows (5 sentences are bare markers). The other 50 sentences, such as "Any fixed storage amount in your code is now a millionth of what it needs to be." and "Both are on npm.", are claims the default run skips and no row covers. Then the rows below were checked and filled in, against these sources:
- The release note copy at `$SKILLS/moi-webinar/community-call/examples/cc14/sources/RELEASE-NOTE.md`. It is restructured from the X thread and is not the original text.
- The published js-moi-sdk 0.9.0-rc2 packages (and the 0.8.0 packages for the old id), read from copies installed on the previous operator's machine. `npm view` confirmed the `latest` tags on 2026-10-02.
- go-moi, which is private, read at the tip of its development branch (2026-09-07) and at tag v0.12.0. The v0.13.0 tag was not in that clone, so go-moi rows say "tip of 2026-09-07". A second clone on the previous operator's machine has the tag, and the notes of C102 and C161 record a read there on 2026-10-02 (ASK: Adithya for that clone). Private source informs a check and never appears in public text, so do not carry any `source` cell into the post.
- A node run of the post's two-line conversion sample, the ethereum.org page the post links, arithmetic, and the live reads in `references/live-reads.md`.

## What the ledger shows
Result of `ledger-status.py`: 54 verified, 3 scoped, 0 argument, 0 cut, 139 unverified. Exit 1, so the answer to "ready" is no. `--against` exits 0: every sentence the default run flags has a row. The 50 plain sentences it does not flag have none (see above).
- Verified rows with a precise `source`: units and prices (C015, C128, C129), the asset id (C031, C113), `FeePayer()` semantics (C026), the payer's signature (C028), the participant-list rule (C041), failed interactions still charging the payer (C094), the conversion sample run in node (C143).
- Claims the release note does not carry, traced to source: the asset limits (C161) and the old id prefix (C155, C032). The CC14 numbers ledger had left both unverified.
- Scoped rows where the limit is already in the text: "by default" (C131) and "for its fuel" (C051, C099).
- Rows left unverified with a reason and a proposed edit, each a lesson:
  - C017: "1 KB costs 1 KMOI" is true only if 1 KB is 1,000 bytes.
  - C186: the recap says "take on users that hold no KMOI" where the body says "pay fuel". A limit was lost between sections.
  - C082 and C185: "Nobody can spend the payer's fuel without its signature" is verified at pool admission only.
  - C158: "The node rejects anything below 50 anu" drops the "by default" that C131 carries.
  - C011, C053, C101, C187: "now has a capped supply". At v0.12.0 the genesis tool already summed a max supply.
  - C008 and C056: a live read proves now, not "since 11 September", and "Voyage devnet" is a corrected form. <!-- slop-lint: ignore -->
  - C078 and C117: a universal and a promise.
  - C061: contested wording after the 2026-09-14 correction.
- One answer to an open question in `moi-webinar/community-call`: "a native asset standard made for KMOI alone" (C102) is supported at the tip and at tag v0.13.0, where MASN instances are created by the genesis routine only.
- No row is `argument` or `cut`. A `cut` row means the sentence was removed, and this snapshot does not edit the published post. The unverified rows carry the proposed edit in `note`.

## What is not here
No text was changed and no second pass was run. 109 rows have not been looked at. Images are not checked: the post has none. The open questions in the `note` cells are for Gokul (when the devnet was re-initialised, whether anything mints after genesis, whether any interaction costs no fuel, how go-moi and moipod relate) and Rahul (the "participant" wording and the two sentences removed from the CC14 script).

## Use of this example
Copy the shape, not the verdicts. A verdict belongs to a sentence, a source and a date. Re-read the sources before you reuse a row, and do not copy a `source` cell naming a private file into a public text.
