# Devnet reset log: <YYYY-MM-DD>

Copy to `devnet-reset-<YYYY-MM-DD>/LOG.md` and fill it in as you go. Keep the folder out of git: it names accounts and people, and the working copies this skill runs in include public repos. Make it self-ignoring once: `mkdir -p devnet-reset-<YYYY-MM-DD> && printf '*\n' > devnet-reset-<YYYY-MM-DD>/.gitignore` (the `*` hides the folder, itself included, from `git add`). Times are UTC with the date; add IST for anything people will read. Ids are written in the short form (the 8 hex digits after `0x20000000` for a logic, the first 16 hex digits otherwise). Never write a key, a token or a recovery phrase here. Back to `../SKILL.md`.

## 1. The event
| Item | Value |
|---|---|
| First signal (what, where, UTC) | |
| Operator | |
| Verdict from `references/detect.md` (reset, registry moved, upgrade, outage, unknown) | |
| Lines that support it (copy from `reset-detect.sh`, with their times) | |
| Confirmed by the protocol team (who, when, channel) | |
| Told it is final (who, when) | |

## 2. Ids and versions
| Item | Old | New | Source of the new value (who, when, or the read) | Read at (UTC) |
|---|---|---|---|---|
| `net.Version` | | | | |
| `net.NetworkID` | method not found on 2026-10-03 | | | |
| Genesis tesseract of the founding account (first 16 hex digits) | | | | |
| Registry logic id | | | | |
| AgentMarket logic id | | | | |
| KMOI asset id (from the SDK, with the SDK version) | | | | |
| Fuel price floor | | | | |
| Default storage fund | | | | |
| Minimum grant to create a participant | | | | |
| `js-moi-sdk` version | | | | |
| `js-moi-agent-registry` version | | | | |
| Read caller used by the MCP and the Explorer | | | | |
| RPC path each product uses | | | | |
| Agent count in the new registry, and the snapshot it came from | | | | |

## 3. Where the old ids were pinned (step 2, before any edit)
One line per `id-grep.sh` run: `bash "$SKILLS/moi-devnet-reset/scripts/id-grep.sh" --files <old id> <paths>`.
| Old id | Paths searched | Files with a hit | Notes (which hits are meant to stay) |
|---|---|---|---|
| | | | |

## 4. The steps
Numbers are the rows of the run table in `SKILL.md`. A GATE needs the operator's yes: write where it was given, not what was said.
| # | Step | Who | Started UTC | Done UTC | Proof (command, result, link) | GATE yes (when) |
|---|---|---|---|---|---|---|
| 1 | Detect and confirm | | | | | |
| 2 | Open the log, record old ids | | | | | |
| 3 | Freeze | | | | | |
| 4 | Facts from the protocol team | | | | | |
| 5 | Verify the new registry | | | | | |
| 6 | Constants and SDK | | | | | |
| 7 | Wallets and funds | | | | | |
| 8 | Launchpad | | | | | |
| 9 | MCP server | | | | | |
| 10 | Agent Explorer | | | | | |
| 11 | Drift check | | | | | |
| 12 | Content and demos | | | | | |
| 13 | Tell people | | | | | |
| 14 | Verify and new baseline | | | | | |

## 5. Per product
| Product | Check | Before | After | Proof |
|---|---|---|---|---|
| Launchpad | `/api/stats` `chainStatus` | | | |
| Launchpad | chain marketplace (`?source=chain`) | | | |
| Launchpad | Actions variable and code default | | | |
| Launchpad | registration wallets exist and are funded | | | |
| Launchpad | market listing read | | | |
| Launchpad | fresh-wallet pass: activation receipt status, registration receipt status, `card_uri` | | | |
| MCP | `moi_resolve_agent` | | | |
| MCP | `MOI_READ_CALLER` set, `/health` both hosts | | | |
| MCP | deploy run (link), tools listed | | | |
| Explorer | registry id in `config.ts` (and `vite.config.ts` on PR #5) | | | |
| Explorer | server identity reads the registry | | | |
| Explorer | `/registry/agents` total against the registry count | | | |

## 6. Content and demos (step 12)
| Item | Dead id, hash or claim found | Fixed (path) or handed to (who) | Date |
|---|---|---|---|
| | | | |

## 7. People told (step 13)
| Who | Message (number) | Sent by the operator at (UTC) | Channel |
|---|---|---|---|
| | | | |

## 8. Open
| Item | Waits on | ASK |
|---|---|---|
| | | |

## 9. The next baseline
After step 14 run `bash "$SKILLS/moi-devnet-reset/scripts/reset-detect.sh" --registry <full registry id: 0x then 64 hex digits, not the 8-digit short id> --genesis-account <new KMOI id> --version <new version> --print-state` (the old baseline would report the reset again; `reset-detect.sh` needs the full id, while `id-grep.sh` also takes the short one). Rename the old `state.txt` to `state-before.txt`, paste the printed `version` and `genesis_hash` lines into a new `devnet-reset-<YYYY-MM-DD>/state.txt`, and write the full ids by hand:
```
version=
genesis_account=
genesis_hash=
registry=
known_hash=
```

## 10. Hand-back
Produced, remaining, not verified, Ready yes or no and why: the block at the end of `SKILL.md`.
