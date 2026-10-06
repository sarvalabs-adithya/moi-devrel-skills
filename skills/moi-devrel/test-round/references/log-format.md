# Log format: a record someone else can re-check

Facts are as of 2026-10-03. `ASK:` is defined in `moi-devrel/SKILL.md`. The template is `templates/test-log.csv`. The Launchpad kept this record as a ledger "so no chat context is required to reconstruct any decision": per agent, the config used, the input and output, what was wrong, and the fix commit. This format keeps that and adds what the old record lacked: the node version, the time and a full hash for every on-chain case. Back to `../GUIDE.md`.

## One row per case, 19 columns
Seed the rows from the plan before the first case runs, with the outcome blank. The checker then lists every case not yet run.

| Column | Holds | Needed |
|---|---|---|
| `case_id` | The plan's id. A retest is `<id>-r1` | Always |
| `round` | `R1`, `R2` or a date | Always |
| `title` | A few words | Always |
| `kind` | `chain`, `read`, `app`, `simulated` (`real-chain.md`) | Always |
| `performed_by` | `operator`, `claude`, `both` | Once run. A chain case is never `claude` |
| `config` | What was set for this case: template and settings, price, account label, branch, the build the tester ran. Never a key | When a setting matters |
| `input` | The exact words typed, the click path or the command | Always |
| `expected` | The plan's `must`, copied | Always |
| `output` | The result as it appeared, after masking (below) | A fail |
| `outcome` | `pass`, `fail`, `blocked`, `skipped`. Blank until run | Once run |
| `evidence` | What proves the verdict: a balance pair, a receipt read, a page value, a command and its answer | A pass |
| `interaction_hash` | The full hash: `0x` and 64 hex digits. Several, separated by a space | A chain case |
| `receipt_status` | The `status` read from the receipt, as the node gave it | A chain case |
| `node_version` | The `net.Version` answer on the day, for example `0.13.0` | A chain case |
| `run_at_utc` | `YYYY-MM-DD HH:MM UTC`, 24 hour | A chain or read case |
| `simulated_what` | What stood in for the real thing. For anything else: `none`, with a reason if a word like "simulation" appears in the case | A simulated case |
| `fix` | A commit or PR, the path of an issue draft in `drafts/`, or `accepted: <who>, <date>` | A fail |
| `retest_of` | The `case_id` of the failure this row retests | A retest |
| `note` | Anything else. Why a case is blocked or skipped | Blocked, skipped |

## Rules for the cells
1. **Hashes in full.** An abbreviated hash cannot be looked up; the session 8 build notes shortened theirs to ten characters, and `moi-webinar` says not to copy that. The checker accepts only `0x` plus 64 hex digits, as devnet returned on 2026-10-03.
2. **Receipt, not broadcast.** `receipt_status` comes from the receipt read in `real-chain.md`. A refusal that the case expects on chain records the status as read, and the `evidence` names the refusal reason. A pass for the wrong reason is a fail (an out-of-fuel agent looks like a forbidden one).
3. **UTC, 24 hour.** Write `2026-10-03 16:02 UTC`. Convert a local time with `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "<YYYY-MM-DD HH:MM>" <area/city>`. A run time shown in the wrong zone happened during the Launchpad rounds.
4. **One node version per row.** A reset or an upgrade between two cases changes it. A hash from before a reset is not found afterwards, so the version and time say which chain it was on.
5. **Output as it appeared, then masked.** Keep the message, the status line, the console JSON. Replace people's names and handles in pasted chats ("Name | MOI, [date]" lines carry a full name) with `user`. Remove any token. Never paste a key or a recovery phrase: the checker flags the shapes it knows, and a clean result is not proof.
6. **Config states what was set, not what was meant.** For an agent: template id, each setting, the time zone. For a wallet: its label (A, B, F). Not its address, unless the case is about the address.
7. **A failing row stays `fail`.** Never overwrite it. The fix goes in its `fix` cell. The retest is a new row with `retest_of`, and its outcome is its own.
8. **Blocked or skipped.** `blocked` means something outside the case stopped it (a reset, an empty wallet, a feature not deployed). `skipped` means the plan chose not to run it (retired feature, out of scope). Both need a `note`.
9. **Quote cells.** A cell with a comma or a line break is quoted. Appending a row with `>>` to a file that lacks a final newline glues it to the last row: write rows with the editor, or check `tail -c1` first.
10. **Kind is what happened.** The plan says what to expect, the row says what occurred. If a signed interaction reached the chain in a case the plan called `read` or `app` (the double charge of 2026-08-02 came from a case that expected a refusal), the row is `chain`, with every hash. Say so in `note`.

## Three rows
Hashes here are placeholders (`0x` and 63 zeros then a digit). Real ones are 64 arbitrary hex digits.
```
case_id,round,title,kind,performed_by,config,input,expected,output,outcome,evidence,interaction_hash,receipt_status,node_version,run_at_utc,simulated_what,fix,retest_of,note
P1,R1,Node build,read,claude,,net.Version on the devnet path,A version,"{""result"":""0.13.0""}",pass,Answer 0.13.0 at the stated time,,,0.13.0,2026-10-03 15:23 UTC,none,,,
L6.1,R1,Buyer pays 100,chain,operator,"price 100, wallet A sells, wallet B buys",Pay 100 KMOI and subscribe in wallet B,Subscribed panel with a hash; A +100; B -100 and fuel,Subscribed,pass,"A 1000 to 1100. B 500 to 397. Receipt read back",0x0000000000000000000000000000000000000000000000000000000000000001,0,0.13.0,2026-10-03 16:02 UTC,none,,,
L6.4,R1,Repeat purchase,chain,operator,same buyer and agent as L6.1,Buy the same agent again,Refused. No second interaction,Two Subscribe interactions succeeded,fail,"Two hashes, same buyer and agent",0x0000000000000000000000000000000000000000000000000000000000000001 0x0000000000000000000000000000000000000000000000000000000000000002,0,0.13.0,2026-10-03 16:30 UTC,none,Guard moved before the wallet opens: commit <sha>,,
```
The third row is the Launchpad defect of 2026-08-02: both payments succeeded and the screen reported success. A retest row `L6.4-r1` would follow with `retest_of` set to `L6.4`.

## How a second person re-checks a row
| Kind | Re-check |
|---|---|
| chain | Read the receipt for each hash (`real-chain.md`) and compare `status`. Balances cannot be re-read after they move, so `evidence` holds both numbers |
| read | Run the `input` again and compare with `output`. The answer may have moved: the logged time says when it was true |
| app | Repeat the `input` on the same target, same config, same build |
| simulated | Read `simulated_what`. It does not prove the real path |

## Where the log lives
In `test-round-<slug>/`, at the root of the working copy of the product's repo, with `.gitignore` holding `*` so a stray `git add` cannot stage it. A log names accounts, test wallets and sometimes people, and `sarvalabs/moi-mcp` is public. To keep results in a repo, write a cleaned summary by hand after a yes. The Launchpad's practice was to paste payment hashes into `docs/QA-LEDGER.md` in its private repo; do that only after a yes, with names removed. Committing, pushing or uploading the log to Drive is a gate. ASK: Rahul where the durable record belongs.

## The checker
```
python3 "$SKILLS/moi-devrel/test-round/scripts/test-log-check.py" test-round-<slug>/test-log.csv
```
Prints counts by kind and outcome, then seven lists and a WARN list. It prints case ids and titles, masked, and no other cell. It makes no network call, writes nothing and refuses an env-named file.

| Exit | Meaning |
|---|---|
| 0 | Nothing stands. Read the WARN list, every simulated case and every blocked or skipped case before saying Ready |
| 1 | Cases to fix: no outcome, a pass with no evidence, a chain case missing its hash or context, a simulated case not labelled, a fail with no output or fix, no kind or a broken `retest_of`, or a secret-shaped value |
| 2 | Bad input: unreadable file, missing column, an unquoted comma, a kind, `performed_by` or outcome outside the vocabulary, an env file |

It cannot tell that a hash is the right hash, that a pass is correct, or that a screenshot says what the row says. It reads a 0x string as a public identifier; a private key written with 0x looks the same, so never paste one.

## Not yet known
- The URL pattern of a hash page on the explorer. The Launchpad source builds `/interaction/<hash>` links, but a GET of that path on voyage.moi.technology answered a redirect to the trailing-slash form and then 404 on 2026-10-03 (checked again at 17:38 UTC with a hash the node returned). Use the node read. ASK: Gokul.
