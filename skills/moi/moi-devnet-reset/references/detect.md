# Detect: a reset, an outage, an upgrade or something else

Facts are as of 2026-10-03 unless dated. `SKILLS` and `ASK:` are defined in `moi-devrel/SKILL.md`. Every command here only reads. The one file written is the baseline you type yourself. Back to `../SKILL.md`.

## First five minutes
Woken by an alert: (1) run step 1 of `../SKILL.md`, which reads and writes nothing; (2) treat a CHANGED line as a suspect, not a verdict, and read "Decide" below; (3) change nothing, spend nothing and say nothing public until the verdict is in the log and the protocol team has answered; (4) then open the file for your symptom in the table "Which file to read" in `../SKILL.md`.

## What looks alike
| Event | What is true on chain | What people see | How to tell it apart | Seen |
|---|---|---|---|---|
| Wipe (a reset) | Accounts, assets, contracts, the registry: gone | "account not found" on any old id; Launchpad `chainStatus` `stale` or `unreachable` with "account not found"; activation 503 `faucet_unavailable`; MCP "Could not load the MOI agent registry" | The genesis tesseract hash differs, old ids do not exist, an old interaction hash is not found | 2026-08-15 about 23:38 UTC, 2026-09-11 |
| Registry replaced, no wipe | Accounts survive. The old registry may still answer reads | New registrations land on a different contract than the one a product reads; rows show as "stranded" | Genesis hash unchanged, the old registry still exists, the protocol team gives a new id | 2026-08-10, 2026-08-13 |
| Registry frozen | Reads work from frozen state, writes never execute | Registrations hang about 127 seconds in the wallet and never land | No read shows it. Only a registration receipt does (`launchpad.md` row L11) | 2026-08-06, unnoticed for four days |
| Upgrade | A new `net.Version` | Possibly nothing | Version differs, genesis hash same, known hash found. No upgrade that kept the state is on record: v0.13.0 wiped | 2026-09-10 tag, 2026-09-11 live |
| Outage | Intact | Timeouts, 5xx, a red deploy, no answer from a host | The chain reads answer and the product does not (a transport failure, not "account not found") | not catalogued |
| One wallet only | Intact | "account not found" for one funded wallet | Other wallets work. A wrong derivation path (faucet wallets `m/44'/6174'/7020'/0/0`, SDK-only `m/44'/6174'/0'/0/N`, Launchpad registration `m/44'/6174'/1'/0/0`) or the wallet's active account is not the signed-in one | 2026-07-30 |
| Idle site | Intact | Launchpad `chainStatus` `stale` on the first call | The second call, 20 to 60 seconds later, says `ok`. The refresh is request-driven | normal |

## Signs, earliest first
1. A go-moi release. The daily upstream watch (03:17 UTC) in `sarvalabs/moi-mcp` opens "Upstream release: go-moi <tag>" with label `upstream-release`: `gh issue list -R sarvalabs/moi-mcp --label upstream-release --state open`. Without its `UPSTREAM_READ_TOKEN` the watch skips go-moi with a warning, so silence proves nothing. v0.13.0 came on 2026-09-10 and the wipe on 2026-09-11. A second case is inferred: go-moi v0.12.0 on 2026-08-14 and the wipe on 2026-08-15 (`history.md`). ASK: Gokul whether a release always precedes a wipe.
2. A message from the protocol team (Gokul) with a new registry id and package versions. The channel is not known. ASK: Rahul, Gokul.
3. The nightly chain canary (02:43 UTC) opens "Chain canary failing", label `chain-canary`: `gh issue list -R sarvalabs/moi-mcp --label chain-canary --state open`. It simulates building an interaction; it does not write.
4. Launchpad `/api/stats` shows `unreachable` or `stale` with "account not found". Wallet activation answers 503 `faucet_unavailable` and the Launchpad's admin Telegram chat is alerted at most once an hour per process.
5. A user writes "account not found".

## Run the reads
```
bash "$SKILLS/moi-devnet-reset/scripts/reset-detect.sh" --state "devnet-reset-<YYYY-MM-DD>/state.txt"
```
With no `--state` it still reads the node and the three products, but it has nothing to compare with: every PASS then only says the node answers, and the script ends the node block with a WARN saying so. Options and exit codes are in the script header (`--help`). It prints PASS, WARN or CHANGED per signal with the UTC time of the read, writes no file, and prints only host names. Exit 0 nothing changed, 1 something CHANGED, 3 a read got no answer (an outage must not look green).

## First baseline
The state file holds the last good values, one `key=value` per line, full-line `#` comments only, a key left out when unknown. A file built after a reset cannot show it, so build the first one now, or from values that predate the event. The products keep pinning the old registry until step 8 to 10 of `../SKILL.md`, so the code is a valid source during a reset. No install is needed:
```
grep -A1 "const DEFAULT_AGENT_REGISTRY_LOGIC_ID" lib/moi/registry.ts
grep -A1 "KMOI_ASSET_ID" packages/js-moi-constants/src.ts/asset.ts
```
Run the first in a working copy of `sarvalabs/moi-agent-launchpad` (private; ASK: Rahul for access) and the second in one of `sarvalabs/js-moi-sdk` (public, `main`), at the commit the products use. Without Launchpad access, `grep -A1 "export const DEFAULT_REGISTRY_LOGIC_ID" src/moi/registry.ts` in the public `sarvalabs/moi-mcp` gives the registry the MCP source pins; check that it matches what the Launchpad and Explorer pin. If someone has already changed the pins, read the older commit with `git show <commit>:<path>`. Then write the file by hand:
```
version=0.13.0
genesis_account=<66 characters: 0x and 64 hex digits, KMOI_ASSET_ID from the second grep>
genesis_hash=0x4529116966dd8c85
registry=<the 66-character registry id from the first grep>
known_hash=<an interaction hash that existed, 0x and 64 hex digits>
```
`version` and `genesis_hash` are what both RPC paths answered on 2026-10-03 (the hash is the first 16 digits; a prefix of 16 to 64 digits is accepted). Get a `known_hash` from the explorer list (`moi-devrel/claim-check/references/live-reads.md`, check 4) and write the date you saw it in the log. After step 14 `--print-state` prints `version` and `genesis_hash` for the next baseline.

Check the SDK version before trusting a `KMOI_ASSET_ID` taken from an installed copy: an old SDK prints a retired id. In the Launchpad clone read on 2026-10-03 the installed `js-moi-sdk` was 0.8.0 (its `package.json` asks for ^0.9.0-rc2) and printed the id from before v0.13.0, which does not exist on devnet. Use 0.9.0-rc2 or later (as of 2026-10-03). Inside an installed working copy (an install is a download: GATE) the check is `npm ls js-moi-sdk --depth=0`, then `node -e "import('js-moi-sdk').then(m => console.log(m.KMOI_ASSET_ID))"`.

## What each line means
| Line | Meaning | Then |
|---|---|---|
| `net.Version` differs from the baseline | A new build | Not a wipe by itself. Read the genesis line. Ask the protocol team whether state is kept (message 1) |
| `net.NetworkID` WARN, error -32601 | The node has no such method (also on 2026-10-02, 2026-10-03 and again on 14 October). The network ID cannot be read from the node | Do not publish a network ID. ASK: Gokul |
| Genesis hash differs, or the founding account is gone | The network was re-initialised since the baseline. Strong evidence, not proof: the rule comes from reading go-moi, and no reset has yet been watched with this check. A hash that is unchanged does not rule out a wipe | Treat as a wipe and send message 1 |
| Genesis check WARN with an error | Often a wrong or retired id | Check the SDK version (above), then rerun |
| Both paths hold the same genesis hash | `/devnet/` and `/babylon/` are consistent with one network (both held the same hash on 2026-10-03) | Still ASK: Gokul before saying they are one |
| Registry "does not exist" | That id is gone: wiped, or replaced | Genesis unchanged means replaced; changed means wiped |
| Registry exists, all 10 routines present | The contract is there. It does not show that writes execute | Only a registration receipt does |
| Known hash not found | Wiped since it was made, or it was never on this network | Needs the genesis line to decide |
| Launchpad stats or chain marketplace CHANGED | The Launchpad reads a registry or caller that is gone | `launchpad.md` |
| MCP read gateway CHANGED | The hosted MCP points at a registry that is gone. It did so on 2026-10-03 and again on 13 to 14 October with no new reset | `mcp.md` |
| "no baseline, so this run cannot show a reset" WARN | No version, genesis hash, registry or known hash was given, so every PASS only says the node answers | Build the baseline (First baseline above), then rerun |
| Explorer total (always WARN) | The index is not cleared by a reset, so the total cannot show one | `explorer.md` |

## Decide
| Reads | Verdict | Next |
|---|---|---|
| Genesis changed, registry and known hash gone | Wipe | Message 1 goes to the protocol team now (step 1 of `../SKILL.md`; the operator sends it). Do not wait for the reply before steps 2, 3 and 6: open the log, freeze and prepare the SDK pair while you wait. Step 5 and later need the reply |
| Genesis same, registry gone or the protocol team gave a new id | Registry replaced. If the known hash is still found, wallets survive and the wallet steps may be skipped. If it is gone too, treat it as a wipe | The same, and ask in message 1 whether the new one is final |
| Genesis same, version changed | Upgrade, state kept (not yet seen) | Ask the protocol team, rerun in an hour, fix the constants (step 6 of `../SKILL.md`) |
| Everything PASS, a user still fails | One wallet, the wrong path, or a frozen registry | The row "One wallet only" above, then `launchpad.md` row L11 |
| Chain reads PASS, a product line is a transport WARN | Outage | The ops skill of that product; the VM is Upendhar's |
| Chain reads got no answer (exit 3) | The RPC host or your network | Retry with `--timeout 30`; ASK: Gokul |
| Anything else | Unknown | Write it in the log with an ASK. Do not call it a reset |
The decision is the operator's. Write it in the log with the UTC time and the lines that support it.

## Not yet known
- Where the protocol team announces a reset and a new registry id, and who the contact is besides Gokul. ASK: Rahul.
- Whether the genesis hash changes on every reset. The only statement of it is in `PR-1-chain-id-edits.md` of the x402 review package, a file on the previous operator's machine that is not in git, reasoned from go-moi source. ASK: Gokul. The reads of 2026-10-03 (15:30 and 16:35 UTC) gave a hash beginning 0x4529116966dd8c85 on both paths, the same prefix that file records for 14 September. If the rule holds, devnet was not re-initialised between those dates (inferred). <!-- slop-lint: ignore -->
- Why `net.NetworkID` does not exist, and whether a version bump adds it. ASK: Gokul.
- Whether any monitor watches the three hosts. None is recorded. ASK: Upendhar.
