# The method, in full

Facts are as of 2026-10-02. The run table is in `../GUIDE.md`; this file says how to do each step and why. Back to `../GUIDE.md`.

## 1. What counts as a claim
- One verifiable proposition per row. If a sentence needs two checks, split it into two rows. Example from `../examples/september-release/ledger.csv`: "Storage costs 1,000,000 anu per byte, so 1 KB of stored data costs 1 KMOI" holds for the first half (row C129) and fails the second unless 1 KB means 1,000 bytes (row C017).
- An instruction hides a claim. "Replace every hardcoded KMOI id" claims that the id changed. Check the fact it relies on.
- Claims hide in front matter (`title`, `summary`, `takeaways` and `faq` answers feed the page and its JSON-LD), tables, code comments, presenter notes, descriptions and what a speaker adds aloud. The extractor reads front matter, tables and the `NOTES` array of a deck, and gives a code block one row. It reads only the files you give it, so pass the description and the social copy too. It cannot hear what a speaker adds aloud. If an HTML file has no `NOTES` array it says so on stderr: a deck whose notes were not read needs the notes file passed as well.
- A plain statement hides too. The default run lists a sentence only when a trigger word matches, so "Any fixed storage amount in your code is now a millionth of what it needs to be." and "Both are on npm." were skipped on the September post (50 of 246 sentences, read 2026-10-02). Run with `--all`, then delete what is not a claim.
- A code sample is a claim that the code works. The extractor gives each fenced block one row of type `code`.

## 2. Steps in detail

### Collect and extract
Check the final wording, not an earlier draft. If wording changes later, re-run step 8. `extract-claims.py` flags a sentence for any number, version, date or time, product or network name, universal ("first", "only", "every", "never", "all"), comparison with another project, promise about the future, statement that something is live, verb of what a system does, or vague attribution. It over-collects on purpose, so many rows are not claims, and `--all` adds the sentences no trigger matched. Secret shapes are masked in the claim text (long hex, common API key and token prefixes, a JWT, a long mixed token, a run of 12 or more short words that could be a recovery phrase): read what a row hides at the line named in `where`. If a recovery phrase turns up in a text, do not repeat it, and tell the operator it is exposed. The extractor never opens an env file.

### Classify
Read every row. Delete a row from `ledger.csv` only if its sentence states nothing checkable (a heading that repeats the section, a bare question). Keep `claims-candidates.csv` as extracted, so a reviewer can see what was dropped, and say in the hand-back how many rows were dropped. Step 8 passes `--dropped claims-candidates.csv`, so a dropped row does not come back as a new candidate. Without that flag every deleted row returns on every re-run and the loop can never reach exit 0. Set `type` to the kind that decides how to check it (`claim-types.md`).

### Check: the twelve rules
1. Find the claim in source at the released tag. If you can only read the `develop` tip or a package, write which in `note`.
2. `source` says where, exactly: a document and section or line; a command, its result and the UTC time; or the arithmetic written out. Quote a release note or a page in at most 15 words and paraphrase the rest.
3. Prefer two routes: a figure from the note and from the SDK or node. If they disagree, ASK the person who owns the fact and word the text so it contradicts neither (August 2026, commit `5c0f763` in `sarvalabs/MOI-Website`).
4. A universal is tested by looking for one counterexample, not by collecting support (worked example below).
5. Find the narrowest true statement and write its limit into the sentence. Scope words ("only the fuel", "by default", "for its fuel") must appear in every place the claim is repeated.
6. A comparison with another project needs a public, dated source for the other side, fetched now. Otherwise cut it.
7. A promise about the future needs the owner's written confirmation. Otherwise cut it or restate what is true now.
8. A "live" claim needs a read of the node. It proves now, never since (`live-reads.md`).
9. Recompute every derived figure. Do not trust a sum, a unit conversion or a percentage in the draft.
10. A code sample: check that every name exists in the published package (grep, or `typeof` in node). Run it if it needs no funded account and writes nothing. A flow that spends devnet funds is a gate: leave the row `unverified`, say why, and offer to run it with the operator's yes.
11. A quote is verbatim, and the text around it adds no fact the note does not give.
12. If you cannot check it, the verdict is `unverified` with an ASK and a person. Never write "probably".

### Verdicts
| Verdict | Means | The ledger needs | The text must |
|---|---|---|---|
| `verified` | The sentence as written is supported | `source`, `checked_by`, `as_of` | Be the sentence in the `claim` cell |
| `scoped` | True only with a limit | `note` stating the limit | Carry that limit in the sentence |
| `argument` | An opinion or a framing, not a fact | `note` saying why it is an opinion | Label itself as one ("In our view", "The design rule is") |
| `cut` | Removed | `note` saying why | No longer contain the sentence. `--against` checks this |
| `unverified` | Nobody has settled it | A `note` with the question and who can answer | Not go out while this stands |
There is no "accepted unverified" verdict. A public sentence that cannot be checked is cut, written into a true scoped form, or labelled as an argument. If the operator keeps one anyway, the hand-back says Ready: no and names the row. `checked_by` names the person or "Claude, pass N". "nobody" means the row was not checked. A verdict about a sentence belongs to that wording: when the wording changes, the `claim` cell changes and the row is checked again.

### Change the text
Show the operator the sentence before and after, one claim at a time, and wait for a yes. Do not add a fact the source does not give. New sentences go through `moi-devrel/scripts/slop-lint.sh`. After a cut, search for what it leaves behind: a bullet, a note, a table row or a teaser that depended on it (CC14, 2026-09-24: four cuts left sentences about a campaign, a competitor and trend arrows). After any correction, search every copy of the text: post, deck `NOTES`, `SCRIPT.md`, social copy, README, description. Search for the family of the claim as well as its words ("every ... fuel", "could not do anything").

### Re-run
`extract-claims.py --all --against ledger.csv --dropped claims-candidates.csv <files> > new.csv` prints rows for sentences the ledger does not cover and lists cut sentences still in the text. It exits 1 while either exists. A sentence is covered when its text equals a ledger claim (or a dropped row) after lower-casing and ignoring punctuation, so a reworded sentence needs its `claim` cell reworded. Add the new rows, check them, repeat. Add them with a newline guard, because a ledger saved without a final newline otherwise swallows the first new row into its last line: `[ -z "$(tail -c1 ledger.csv)" ] || echo >> ledger.csv` then `tail -n +2 new.csv >> ledger.csv`. Finish with `ledger-status.py`. A fix can introduce a new claim, which is why the loop ends on both exit codes.

### Working with the ledger file
- Edit it in a text editor or a spreadsheet and save plain CSV (UTF-8, comma separated). Quote any cell that contains a comma or a line break. Excel's "CSV UTF-8" adds a byte order mark: `ledger-status.py` refuses it with a message unless you pass `--allow-bom`.
- Show the operator the rows that need a decision (`scoped`, `argument`, `unverified`) as a numbered list: the sentence, the verdict, the source in one line, and the proposed edit. The operator answers by number. The release slide checks of `moi-webinar/community-call` do the same with the whole table.
- Never paste a key, a token or a recovery phrase into a cell. Both scripts mask secret shapes in what they print, and that is a backstop only. `ledger-status.py` warns about an `as_of` that is not a real YYYY-MM-DD date and about an `argument` or `cut` row with no note, and it does not count a placeholder such as TBD as a source.

## 3. Worked example: "Every action on MOI costs fuel" <!-- slop-lint: ignore -->
The sentence opened the September 2026 release post draft, and a variant said "every interaction sent to MOI costs fuel". On 2026-09-11 the previous operator rejected the first as untrue and the second as an exaggeration. Both were removed. The opener became "You can now pay fuel for another user." <!-- slop-lint: ignore -->
What the steps look like, with the check re-run on 2026-10-02:
1. Extract: the sentence is a row, type `universal` ("every"). The surviving universals in the published post are rows C062, C078 and C124 of `../examples/september-release/ledger.csv`.
2. Authority: tagged source for protocol behaviour, plus the earlier fact-check of 2026-08-07.
3. Check by looking for a counterexample. First: reads cost no fuel. The session 7 report (`session-7/blog-assets/factcheck-report.md`, on branch `claude/agent-payments-simple` of `moi-foundation/MOI-Webinars`, not on `main`) records "Reads take no signature and no fuel". Second, an interaction can be sent and cost nothing: in go-moi (private), at the development tip of 2026-09-07, the executor returns an insufficient-fuel receipt when the fee payer cannot cover the maximum fuel cost, and the code comment says the user was not charged. Find it with `git -C <your go-moi clone> grep -n -i 'insufficient' origin/develop -- '*.go'` and read the executor hit. The same check exists at tag v0.13.0 (read 2026-10-02 in a second clone that has the tag).
4. Verdict: `cut`, not `scoped`. No true limit rescues "every". The replacement sentence is its own row, `verified` against the release note's Fee Payer section and the fee payer rule in private source (example row C048).
5. Text: the operator approves the swap. Search the family: `grep -n -i -E "every .{0,30}fuel|could not do anything|could do nothing"` across every copy. It finds the same shape in a CC14 script line ("every interaction paid its own fuel, so an account holding no KMOI could not do anything at all", marked OVERSTATED on 2026-10-02 in `moi-webinar/community-call/references/release-slide-checks.md`) and in the published post (row C078). `slop-lint.sh` rule `fuel-universal` catches only the first form.
6. Re-run: `--against` stays quiet once the sentence is gone and reports it if a copy survives.
The ledger rows, in a fence because the CSV quotes the wrong form on purpose:
```
id,claim,where,type,source,verdict,checked_by,as_of,note
W1,Every action on MOI costs fuel.,draft:1,universal,"Reads cost no fuel (session 7 fact-check, 2026-08-07). An interaction whose payer cannot cover the maximum fuel is not charged (private source: go-moi executor, tip of 2026-09-07)",cut,Claude pass 1,2026-10-02,Replaced by W2. No limit rescues 'every'
W2,You can now pay fuel for another user.,draft:1,behavior,"Release note, Fee Payer section; private source: go-moi fee payer rule, tip of 2026-09-07",verified,Claude pass 1,2026-10-02,
```
What was recorded and what was re-run here: the 2026-09-11 rejection is history from the previous operator's sessions. The two counterexamples were found for this branch on 2026-10-02; the original call was made without those citations.

## 4. Two ledgers
| | Claim ledger (this branch) | Numbers ledger (`moi-webinar/community-call`) |
|---|---|---|
| Unit | A sentence that claims something | A figure printed on a slide |
| Columns | `id,claim,where,type,source,verdict,checked_by,as_of,note` | `slide,figure,value,source,as_of,confirmed_by,status` |
| Script | `ledger-status.py` reads the ledger only | `ledger-check.py` reads the deck and the ledger |
| Question | Is each statement supported by source? | Does every figure on a slide have a confirmed row? |
| Misses | Anything outside the files you give it | A universal, a "live" claim, a comparison, a promise, a spelled-out number ("seventh") |
| Status words | `verified, scoped, argument, cut, unverified`. No "accepted" state | `confirmed, unverified or pending, accepted-unverified, superseded or dropped`. The human may keep a figure nobody verified |
For a community call use both. The numbers ledger is the gate for figures on slides. This ledger covers the sentences around them: the release slides, "live", promises, comparisons, the script. A figure can appear in both with the same source cited. Neither script reads the other, and the verdict words differ on purpose (`confirmed` against `verified`). Do not merge them.

## 5. Older verdict words
Older reports use other words. Map them when reading or porting a table.
| Older word (session 7 fact-check, release slide checks) | Use now |
|---|---|
| VERIFIED, TRUE, SUPPORTED, INTERNAL VERIFIED | `verified` (INTERNAL: say in `note` that it is a count of the text itself) |
| FIXED | `verified` after the fix, with the fixed sentence in `claim` |
| SCOPED | `scoped` |
| ARGUABLE | `argument` if it is a framing, or `scoped` if a limit rescues it |
| OVERSTATED, FALSE | Rewrite to a true form and set `verified` or `scoped`, or `cut` |
| UNVERIFIABLE | `unverified` until someone can settle it, or `cut` |
| SECTION CUT, CUT | `cut` |

## Not yet known
- Where the final ledgers of earlier posts were saved. Only counts survive in PR bodies and commit messages (August: 88 agents, 553 claims, six errors held; September: 152 claims, three corrections). Not recorded (the previous DevRel's notes); ASK: Rahul.
- How long a check takes. No durations were recorded.
- Who on the protocol team confirms "live" before each community call. ASK: Rahul. Whether a given version is live is a question for Gokul.
