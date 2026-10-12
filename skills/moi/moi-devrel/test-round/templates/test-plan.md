# Test plan: <product>, round <R1>

Delete this paragraph when the plan is filled in. Copy to `test-round-<slug>/test-plan.md`. One case per line. Every `must` is true or false. Wallets are labels (A, B, F), never values and never a recovery phrase. Keep this folder out of git (`.gitignore` holding `*`). Guidance: `references/plan-format.md`; method: `references/method.md`.

| Field | Value |
|---|---|
| Round | <R1, or a date> |
| Product | <Agent Launchpad, MCP connector, ...> |
| Target (live host) | <https://... the live host, not an old one> |
| Version or commit under test | <commit of the last green deploy run, or the tools/list names; mark "inferred" if you did not read it> |
| Node version | <net.Version answer> at <YYYY-MM-DD HH:MM UTC> |
| Date and operator | <date>, <the operator's name> |
| Sign-off by | <name. ASK: Rahul if unknown> |
| Trigger | <before launch / after a deploy / after a reset / before a merge / new user> |
| The question this round answers | <one line> |

## Cost and gates
Chain cases spend devnet funds from: <wallet A, wallet B>. Cap per account: <KMOI and fuel>. The operator's yes, naming the paying account: <date and the words used>. Every case of kind chain waits for that yes. A write request to a live product, a faucet request and a download are gates too.

## Preconditions
| id | kind | who | ask or do | must | ground truth | cost |
|---|---|---|---|---|---|---|
| P1 | read | claude | `net.Version` | An answer; recorded | The node | none |
| P2 | app | operator | The wallet's active account is the account you are signed in as | Confirmed | The wallet | none |
| P3 | app | operator | Wallets <A> and <B> funded for <price> plus <fuel> | Balances recorded | The chain | none |

## Cases
### <Area 1>
| id | kind | who | ask or do | must | ground truth | cost |
|---|---|---|---|---|---|---|
| <id> | <chain / read / app / simulated> | <operator / claude / both> | <the exact words, click or command> | <true or false> | <where the right answer comes from> | <none, or the interaction and who pays> |

### <Area 2>
| id | kind | who | ask or do | must | ground truth | cost |
|---|---|---|---|---|---|---|

## Questions Claude asks the operator
- Before a chain case: "Case <id> costs one <interaction> from <account>, up to <cap>. Yes?"
- Before a wallet step: "Is the wallet's active account the one you are signed in as?"
- After any step: "Paste the message exactly as it appeared, the hash if there is one, and the balances."
- After a failure: "Does it happen again? Is anything else on the screen?"
- Before a re-download: "Did you download the setup script again and restart the agent after the last change?"

## Simulated in this round
| id | What stands in for the real thing, and why |
|---|---|
| <id> | <say it in plain words> |

## Stop triggers
- <what makes the round halt>

## Not covered
- <what this plan leaves out, said plainly>

## Sign-off (filled at the end)
| Area | Result (pass, fail, blocked) | Case ids | Read by |
|---|---|---|---|
| <Area 1> | | | |
