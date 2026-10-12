# Traps: failures that produce a wrong result with no error

Facts are as of 2026-10-03. `ASK:` is defined in `moi-devrel/SKILL.md`. Each row is a rule and the incident behind it, with its date. The ten most costly are repeated in `../GUIDE.md`. Back to `../GUIDE.md`.

## Evidence that misleads
| Rule | The incident |
|---|---|
| A success message is not proof. Count interactions on the chain | 2026-08-02: two Subscribe interactions succeeded for one agent, 200 KMOI paid for one. The screen reported success, and the planned case "buy again, not charged twice" would have passed |
| Read the receipt, not the broadcast, an HTTP 200 or a simulation | September 2026 (PR #30): wallet activation said "Wallet is ready" while the chain reverted it, because the grant was under the 1 KMOI floor and a call-site name was rejected under the new asset standard. MCP issue 7: a fuel price of 1 simulated fine and bounced at broadcast. The nightly canary once passed while asset creation failed |
| A refusal passes only for the right reason | 2026-08-31: a policy beat "passed" because the agent was out of fuel. The demo now requires the error text to name the rule |
| A refused pull of the standard asset returns a hash and no error | Sessions 8 and 9: the only oracle is a balance difference |
| `onchain: null` is not "unlisted", and a database listing is not the chain | The Launchpad's default marketplace listing is a database index and can show agents as on-chain from a dead chain. `?source=chain` reads the registry (observed 2026-10-02) |
| A number needs its age. Read a stats endpoint twice | The Launchpad's stats page kept 46 on-chain agents for days after the registry vanished (commit 8b06cd6). Its refresh is request-driven, so an idle site first reports `stale` (observed 2026-10-02 and 2026-10-03). On 2026-10-03 at 17:37 UTC `GET /api/marketplace?source=chain` answered 7 agents, and about a minute later 0 |
| A health endpoint can say ok over stale data | The Explorer's `/health` answered ok while its index held 49 agents (2026-10-02) |
| A read proves now, never since | The September release post said "since 11 September"; the oldest listed interaction was dated 2026-09-10 (`moi-devrel/claim-check/references/live-reads.md`) |
| A hash from before a reset is not found | Devnet was wiped on 2026-08-15 and 2026-09-11. Two hashes from the July 2026 Launchpad ledger answered "tesseract hash not found" on the receipt read and "error fetching interaction" on the interaction read (2026-10-03 15:47 UTC). That ledger lists no node version beside its hashes, so they cannot be placed on a chain. The log format keeps the version and the time |

## The setup under test
| Rule | The incident |
|---|---|
| The wallet's active account must be the account you are signed in as | The most common cause of confusing failures in the Launchpad rounds. The app blocks the mismatch with a message, but avoid it. After switching accounts, sign out and in |
| Test the build you think you are testing | 2026-07-30: a self-hosted agent keeps its old behaviour until the setup script is downloaded again and pm2 restarted. Agents created before 2026-08-02 have no time zone stored: recreate them |
| A copied plan carries old facts | The Launchpad plan's header names an old host and its Phase 0 talks about the old host's environment. It expects a `n/40` counter that may be retired, and it contradicts itself on price history (sections 11 and 14) |
| A brand-new wallet cannot sign until it is registered | 2026-07-31: the extension refused to sign ("couldn't retrieve nonce"). Treat registration as a precondition |
| A wrong derivation path gives "account not found" | Faucet `m/44'/6174'/7020'/0/0`, SDK-only `m/44'/6174'/0'/0/N`, Launchpad registration and the session 8 owner `m/44'/6174'/1'/0/0` (`moi-devrel/references/devnet.md`) |
| A stuck interaction blocks a wallet | 2026-08-11 to 2026-08-13: the cure was a replacement interaction at the same sequence with enough fuel. Do not blame an upcoming upgrade without a read that shows it: the previous operator objected sharply to that explanation during those days (inferred from the reply) |
| A stale popup in the wallet is not the product's fault | 2026-08-01: "Another request is already in progress" was cleared by answering or toggling the extension |
| A reset wipes the ground under the test | After 2026-09-11 earlier agents show "need registering again". Run `moi-devnet-reset` first. Owners re-register and their rows are never deleted |
| The faucet funds existing accounts only, and documents quote its amount differently | 20K KMOI in one, 100K in others (`moi-devrel/references/devnet.md`). Read it live. Asking the faucet is a write |

## Diagnosis
| Rule | The incident |
|---|---|
| Label a hypothesis, and read the stored value first | 2026-07-30 to 2026-08-02: "goal 98 against 10" was blamed on config drift. The cause was the mouse wheel changing a number input: a price typed as 1000000 was listed as 999998, and a goal of 10 became 8 |
| One broad keyword collapses every answer | 2026-07-30: the `fx_rate` matcher held a bare `?`, so every question got the same reply. Give each intent its own probe in one battery |
| Hunt invention, not only wrong answers | 2026-07-30: a delete request made the expense agent store three fabricated entries. A question whose true answer is "no" belongs in every battery |
| A normal outcome is not a fault | 2026-08-02: `delivered=false` on `price_watch` is the usual "threshold not crossed". The relay answering 403 is the pause signal |
| Run date cases when local and UTC dates differ | 2026-08-02 at 8:43 pm US Eastern: an expense was filed under the next day and "yesterday" returned today |
| A shared quota looks like a bug | 2026-07-30: "only 3 messages" was a pool drained by earlier testing |
| When one defect class shows, test its siblings | The message-ignored defect appeared in four templates independently |
| A guard nobody has seen fire is not a guard | `moi-webinar/references/demo-standard.md`: force the guard once and watch it stop |

## Process and records
| Rule | The incident |
|---|---|
| Write the row when the case ends | 2026-07-30: the previous operator asked for everything to be tracked as testing went on: each agent's config, every input and output, what was changed, and all creation and deletion hashes |
| Fill in the sign-off table | None of the sign-off tables in the Launchpad repo was ever filled in |
| Do not ship what the round has not proven | During the Launchpad rounds the previous operator asked for a build without payments, with payments on their own branch. The MCP docs hold that a write path must be approved on a phone by a human at least once before release |
| A short checklist does not replace the full list | `POST-CUTOVER-CHECKLIST.md` says so about itself. Its VM items (reboot, certificate renewal, memory after 24 hours) have no recorded results |
| A pasted chat carries real names | Telegram transcripts begin "Name | MOI, [date]". Replace names with `user` before they enter a log |
| The log names accounts and people | Keep it out of git. On 2026-06-08 a call transcript was committed and had to be scrubbed from history |
| A fix needs a retest on the live host | A merge to the Launchpad's `master` deploys it, and the pipeline runs no tests on a pull request. A green run is not a working product |
| No sub-agents unless the operator asks | The previous operator asked for a standing QA agent once during the Launchpad rounds and then said he would test by hand (date not recorded) |

## Wallets and secrets
| Rule | The incident |
|---|---|
| Claude never signs and never handles a recovery phrase, even a throwaway one the operator offers | Phrases were pasted into chats on several days between June and September 2026, one with an explicit offer of consent. Continue with the MOI Wallet extension and the operator's funded account |
| Never read or confirm seed words on a recorded call | 2026-09-24: a phrase reached Gemini notes of a screen-shared wallet setup |
| A pasted key is exposed | A Buffer token was revoked after 2026-08-31; Telegram bot tokens were pasted on several days. Say where it is, not what it is, and name who can revoke it (`moi-devrel/references/keys-and-access.md`) |
| A clean scan is not proof | `scripts/test-log-check.py` and `secret-scan.sh` know common shapes. A clean result does not make a log safe to share |
