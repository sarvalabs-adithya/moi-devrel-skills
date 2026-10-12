# Traps: failures that give no error

Facts are as of 2026-10-03. Every row is a real incident, written as a rule. Back to `../SKILL.md`.

## Reading the state
| Rule | The incident |
|---|---|
| A green health answer proves the process, not the data | Explorer `/health` says `ok` while its index holds the pre-reset 49 agents. The MCP `/health` was `ok:true` on 2026-10-03 while registry reads failed. The Launchpad's default marketplace listing is a database index and kept showing `onchain:true` for a dead chain, so use `?source=chain` |
| A read cannot see a frozen registry | `b97ce717` stopped executing writes on 2026-08-06 and kept serving reads. Registrations hung about 127 seconds and nobody saw it for four days. Only a registration receipt shows it |
| `onchain:null` means unavailable, not "unlisted" | The market listing read returns null on 2026-10-02 and 2026-10-03 because the contract is probably gone |
| `stale` on an idle Launchpad is normal | The chain refresh runs only when someone asks. Read twice, 20 to 60 seconds apart |
| Read the receipt, never the broadcast | Wallet activation said "Wallet is ready" while the chain reverted it: a grant under the floor, the callsite `Transfer!` instead of `Transfer`, and HTTP 200 on a revert (PR #30, 2026-09-15). Simulation also accepts what the chain refuses: fuel price 1 simulated and bounced at broadcast |
| A hash from before the reset is not found | Do not use an old hash as a fixture, and do not write "every hash in it is on chain" about a recording that predates a reset |
| A number needs its age | `/api/stats` kept showing 46 on-chain agents for days after the registry vanished (swallowed errors, fixed 2026-09-14). Carry `chainAsOf` with any count |
| An unchanged genesis hash does not rule out a wipe, and a changed one is not yet proof | The rule that the hash changes on re-initialisation comes from reading go-moi, and no reset has been watched with it (`detect.md`) |

## Ids and where they hide
| Rule | The incident |
|---|---|
| Three repos pin the registry id separately, and the Explorer pins it in two places once its PR #5 merges (one on `main`) | After the 2026-09-11 wipe they moved 4, 11 and 12 days later. Run `id-grep.sh` over all of them every time |
| The registry package embeds an id and reads the environment once, when it loads | `js-moi-agent-registry@0.3.0-rc1` embeds the wiped `c684f926`. An unset variable hands the package that dead address, and an empty one hands it an empty string, which is what the deploy writes when an Actions variable is unset. npm's "latest" is the latest publish, not the highest version, so a bumped package does not carry the current address |
| Merging does not deploy the MCP | The live server is a copy in `voyage-api`. It was still on the wiped registry 22 days after the wipe (2026-10-03), although `moi-mcp` `master` held the new id from 2026-09-24: the copy had not been synced and deployed |
| A deploy workflow passes only the names it lists | The MCP workflow passes neither the registry id nor the read caller. The Explorer workflow passes `MOI_MNEMONIC`, `MOI_AGENT_ID` and `MOI_INTELLIGENCE_LOGIC_ID` and not `MOI_AGENT_REGISTRY_LOGIC_ID`, `MOI_READ_CALLER_ADDRESS` or `MOI_WS_URL` |
| `NEXT_PUBLIC_*` and `VITE_*` are fixed at build | Restarting a container changes none of them. `NEXT_PUBLIC_APP_URL` is also written into every on-chain `card_uri`, permanently. The Explorer's `VITE_AGENT_REGISTRY_LOGIC_ID` is read by no client code |
| The Launchpad ignores `MOI_RPC_URL` when it contains "voyage" or "devnet" | The documented example host does not resolve, and changing the variable to another devnet URL changes nothing |
| `/devnet/` and `/babylon/` may be one network | The MCP read gateway is deployed with `/babylon/`, the code default is `/devnet/`. On 2026-10-03 both gave `net.Version` 0.13.0 and the same genesis tesseract, which is consistent with one network. ASK: Gokul |
| `net.NetworkID` does not exist on the running build | Answered -32601 on 2026-10-02 and 2026-10-03. Publish no network ID. The reference format is undecided (`moi-devrel/references/terminology.md`, Contested 1) |
| An SDK that is too old prints the retired KMOI id | In the Launchpad clone read on 2026-10-03 the installed `js-moi-sdk` was 0.8.0 (its `package.json` asks for ^0.9.0-rc2) and `KMOI_ASSET_ID` printed the id from before v0.13.0. Check the version before trusting an id or a genesis alarm |
| Old ids that stay are on purpose | A Launchpad test pins the wiped id out of the source. History files name old registries. The September post tells readers to search their code for the old KMOI id. Do not strip them |
| Probe scripts default to dead ids | `probe-registry.mjs` and `_map.mjs` in the Launchpad default to `b97ce717`, the registry that froze on 2026-08-06 |

## Wallets, funds, secrets
| Rule | The incident |
|---|---|
| A wiped account cannot recreate itself | Creating a participant needs an existing funded sender. The faucet funds only accounts that exist. A person with a MOI Wallet account on the new chain must start the chain of funding |
| The recreate script succeeds on "visible", not on a receipt, and its default grant is 0.5 KMOI | The floor is 1 KMOI (measured in September). The app grants 10 KMOI per activation. Set `MOI_REGISTRATION_GRANT` and read each receipt |
| "Account not found" for a funded wallet can be the wrong derivation path | 2026-07-30. Faucet wallets use `m/44'/6174'/7020'/0/0`, SDK-only wallets `m/44'/6174'/0'/0/N`, the Launchpad registration default is `m/44'/6174'/1'/0/0`, and the session 8 owner wallet from the extension used `m/44'/6174'/1'/0/0` |
| The wallet's active account may not be the signed-in one | The most common cause of confusing Launchpad failures |
| Claude never handles a recovery phrase, including a throwaway one | The sponsor and deployer phrases go in at a no-echo prompt, never in chat or a file. `deploy-local.sh` uses `read -s -p`, which fails under zsh ("no coprocess"), so run it with bash. A phrase pasted into chat or read out on a recorded call is exposed: seed words reached Gemini notes on 2026-09-24 |
| Do not rotate secrets in the rush | `AGENT_KEY_ENCRYPTION_SECRET` is never rotated: every stored agent key becomes unreadable. Rotating `TELEGRAM_WEBHOOK_SECRET` without `setWebhook` silently stops delivery |
| An Explorer `MOI_MNEMONIC` that is set never falls back | If its wallet is gone, every read fails, however the read-only caller is configured |

## Data and people
| Rule | The incident |
|---|---|
| Never delete rows to fix a reset | The Launchpad's stranded check compares chain and database by itself. Explorer rows are never deleted by any code, so decide with Gokul and treat it as a production-database write |
| The new registry may hold an old snapshot | MOI imported an old snapshot into `2f3e9469`: 144 agents, only 1 of the 11 listed agents carried over. Owners re-register. Tell them |
| `GetAllAgentIds` reverts at about 135 agents and returns an empty list | August. The registry restored on 2026-09-11 held 144 agents. The Launchpad reads by owner. Whether the Explorer's paging copes is untested |
| Dashboard copy is fixed to one reset | The notice keys and text name the August events. Edit them or a user who dismissed the old notice never sees a new one |
| Wait for the protocol team to say the new state is final | The registry failed on 2026-08-06, was replaced on 08-10 and 08-13, and the chain was wiped on 08-15. Anything funded before the wipe went with it |
| Do not follow an old worked example blindly | `docs/REGISTRY-C684F926-CUTOVER.md` is the August reset, with that month's ids and SDK |
| CI does not protect a reset deploy | The Launchpad runs no tests in CI and a red run leaves the old image serving with no alert (two failed on 2026-09-14). Check the run yourself: `gh run list -R sarvalabs/moi-agent-launchpad --limit 3` |
| Say "devnet", and say "live" only after the reads | Devnet lagged the source in September; the network name was corrected on 2026-09-25: it is devnet, and Voyage is the explorer (`moi-devrel/references/devnet.md`) |
| Never tell people it is fixed before the fresh-wallet pass | The Launchpad said "Wallet is ready" while the chain reverted. A draft status line that claimed work not done was removed on 2026-09-10 |
| A scheduled post cannot be removed by script | `buffer.mjs` cannot delete. Two wrong posts were deleted by hand on 2026-09-10 |

## Not yet known
- Whether a reset can happen with no go-moi release before it, and whether it can happen on a day nobody is watching. ASK: Gokul.
- Whether the Launchpad kill switch (`platform_state.killed`) can be reset. The Launchpad refuses every model call when platform spend crosses its daily cap. ASK: Adithya.
