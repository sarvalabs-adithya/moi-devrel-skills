# Claim types: how each is checked and what makes it unverifiable

Facts are as of 2026-10-02. The `type` column of the ledger holds one or more of these words, separated by `;`, the first one being the kind that decides how to check the sentence. `extract-claims.py` fills it in that order: live, promise, comparison, universal, attribution, version, date, number, behavior, name, code. Correct it when it is wrong. Back to `../GUIDE.md`.

## At a glance
| Type | Flagged by | Check against | Unverifiable when | Then |
|---|---|---|---|---|
| live | live, shipped, available, stable, latest, now can | A read of the node (`live-reads.md`) | The sentence says "since" or "everywhere", or no read is possible | Scope to now, or ask the protocol team and write what they confirm |
| promise | will, soon, planned, next call, scheduled | The owner's written confirmation | Nobody who can commit has said yes | Cut it, or state what is true now |
| comparison | than, versus, another project's name | The other party's own public page, fetched now | The other side has no public dated source, or "faster" has no measured benchmark | Cut it |
| universal | first, only, every, never, all, nobody, no X can | One counterexample search in source | You cannot search every case | `scoped` to the narrowest true statement, or cut |
| attribution | most teams, experts, according to | A named source | There is none | Name the source, or cut <!-- slop-lint: ignore --> |
| version | `v0.13.0`, `0.9.0-rc2`, rc | The tag and the published package | The string is paraphrased | Copy it exactly from the tag |
| date | a month, a weekday, UTC, today, since | The source of the schedule | It is relative ("today", "last Friday") | Write the date, 00:00 UTC form and India time |
| number | any figure | The source of the figure, recomputed | The figure came from a screenshot or an old report nobody can reopen | Ask the owner by name, date it, or drop it |
| behavior | rejects, charges, signs, returns, can | Source at the tag, or the wire | Only private source proves it and you have none | `unverified`, or say what the wire shows |
| name | MOI, KMOI, MASN, js-moi-sdk, devnet | The name's spelling in `moi-devrel/references/terminology.md`, and that the thing exists | The name was invented | Fix or cut |
| code | a fenced block | Names exist in the package, and it runs if free | It needs funded accounts | `unverified`, and say it is a spend gate |

## live
- "Live on devnet" needs check 1 of `live-reads.md` (the version) and, for a feature, a field it needs (check 4). Status words are claims too: `shipped`, `available`, `stable`, `latest`, `supported`.
- A release candidate is not shipped. A CC13 slide said `js-moi-agent-registry v0.3.0-rc1` shipped, and it was a candidate pinned to an exact SDK peer (2026-08-27). Keep the `-rc` suffix and add no sentence explaining it. <!-- slop-lint: ignore -->
- A feature found only in the `develop` tip is "planned" until a live read shows it. On 2026-09-10 devnet answered `payer` while the tip had `fee_payer`.
- Community calls: no devnet read from the day of CC14 is on record. CC14 was apparently Friday 25 September (inferred; ASK: Adithya for history, or Vardan for the sheet). The instruction of 2026-09-25 fixed the wording "went live on devnet"; it was not a check.

## promise
- A statement about the future, or about who will appear, is a claim about someone else's plans. The CC13 description named guests that the CC14 deck did not have. A promise for the next call goes in only when the owner has confirmed it.
- Example row C117 of `../examples/september-release/ledger.csv`: "the next change will not break you either". Cut it, or say what the SDK constant does now.
- A promise that is the owner's own, in the owner's words, is `verified` against that message, with its date and sender in `source`.

## comparison
- The other side is a fact about someone else. Fetch their page now and quote at most 15 words. Example: "the way Ethereum counts ETH in wei" was checked against the page the post itself links, which says wei is the smallest possible amount of ether (row C119, read 2026-10-02).
- A superlative over another project ("faster", "cheaper") needs a measurement with its conditions and a date. Without one, cut it.
- Competitor and third-party stories stay off the community call: the Lit Protocol comparison and the enterprise tender slide were removed from CC14 (2026-09-24). No reason was recorded, so treat it as a pattern and ASK: Rahul before reinstating one.
- An analogy ("like ETH on Ethereum") is checked on both halves: the MOI half in source, the other half on a public page.

## universal
- Search for one counterexample instead of collecting support. Worked example: `method.md`, section 3.
- Past catches: "only the owner can move funds, there can't be a custodian" was false because MAS0 has `Approve` and `TransferFrom` and `Lockup` and `Release` (2026-08-07). "Every action on MOI costs fuel" (2026-09-11). <!-- slop-lint: ignore -->
- A universal can hold at one layer and not at another. "Nobody can spend the payer's fuel without its signature" is checked where the pool admits interactions. Whether validators re-check it is a separate read (example row C082).
- "Every copy", "all", "any": the extractor flags them, and the fix is usually a scope ("ignoring case") or a different sentence.

## attribution
- "Most teams quietly accept both" was cut as vague attribution (2026-08-31 or 09-01, the request log does not say which). Name who said it, with a link, or delete the sentence. `slop-lint.sh` warns on `vague-attribution`. <!-- slop-lint: ignore -->

## version
- Copy the string from the tag or the package. Check the package with `npm view <name> dist-tags` and note the date: on 2026-10-02 js-moi-sdk `latest` was 0.9.0-rc2 (`sources-of-truth.md`).
- A version pinned by a sub-package is not pinned by the umbrella package: js-polo 0.1.5 is pinned by four js-moi-sdk packages and listed in none of the umbrella `package.json` (example row C173).
- Never tell readers to upgrade to a version the operator has not confirmed as the latest compatible one (August 2026: the agent-registry candidate stayed in the post and the upgrade instruction was dropped).

## date
- Write the date, 24-hour UTC and India time, for example "00:00 UTC on 11 September (05:30 IST)". Run `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "YYYY-MM-DD HH:MM" <area/city>`. Never "today", "tonight", "last Friday", "since the last call" (stale on CC14 slide 9).
- A 12-hour release time was misread and two posts were scheduled wrong (2026-09-10, `moi-devrel/references/terminology.md`, table C). The correction reply said "00:00 UTC on 11 September". <!-- slop-lint: ignore -->
- "Since <date>" is a claim about the past that a live read cannot prove. See `live-reads.md`.
- An event's date and venue come from the event's own site, fetched and dated (the CC14 Futuremode slide, 2026-09-24).

## number
- Name the source and recompute. Examples from September 2026: 1 KMOI is 1,000,000,000 anu and 50 anu is 0.00000005 KMOI (rows C015, C035 of the example ledger). "1 KB costs 1 KMOI" holds only if 1 KB is 1,000 bytes (row C017).
- Counts go stale. Namespaces were 55, then 50, then 49 (2026-09-09). RPC methods were 36 and are 42 in js-moi-sdk 0.9.0-rc2. Test counts were 28, 13 and 36 in the same package. A "27 errors" headline met a table of 26 and a list of 25 (2026-08-21). Put the date in `as_of`, recount after every edit, and reconcile every count in a document with every other.
- A figure from a screenshot or a typed message needs its owner to confirm it. CC14 had three sets of AI-visibility figures (13.5%, 17.3%, 18%) and 47 queries on five engines, which is 235 and not the 226 responses on the slide (2026-09-24). Slide figures also go in the numbers ledger of `moi-webinar/community-call`.
- Units: say anu or KMOI every time, and never convert by hand in text (the release note says "Do not calculate these conversions manually").

## behavior
- "X does Y" about the protocol or an SDK is the claim the August and September checks existed for. Find it at the tag. "Now" means it changed, so compare with the previous tag: the example shows `ErrRedundantParticipant` is absent from every Go file at v0.12.0, which supports "now rejects" (row C041).
- Prefer wire-visible behaviour in public text. A spec appendix may describe only what a reviewer can observe (2026-09-10).
- Description is not the same as enforcement. A status file said a key id was pinned while the code did not check it (2026-09-10), and a resource binding described in a spec did not exist in the code (2026-09-09).

## name
- Spelling and form: `moi-devrel/references/terminology.md`. The names an assistant invents are function and export names. `predictAssetId` and `predictLogicId` came from release notes and do not exist at v0.8.0 (2026-08-19). Grep the package for every name.

## code
- Names exist, arguments match, and the sample runs if it needs no funds. The example ran `parseKmoi("0.5")` and `formatKmoi(1500000000n)` in node against the installed js-moi-sdk 0.9.0-rc2 and got the values the comments promise (row C143). The fee delegation sample needs funded devnet accounts and stays `unverified` (row C090).
- Line counts quoted in a post ("713 lines across six files") are numbers: recount after every code change (2026-08-07).

## Not yet known
- Whether competitor and third-party stories are barred from the community call by policy or were cut case by case. ASK: Rahul.
