# Plan format: what a test plan contains

Facts are as of 2026-10-03. `ASK:` is defined in `moi-devrel/SKILL.md`. The template is `templates/test-plan.md`. The Launchpad plan (`docs/E2E-TESTING.md`) and the MCP plan (`docs/testing-plan.md`, `docs/deploy-checklist.md`) set the shape. Back to `../GUIDE.md`.

## What the plan holds, in order
1. **Header.** Round name, product, target (live host), version or commit under test, `net.Version` read on the day, date, operator, who is asked to sign off. The Launchpad header named an old host, so check the target line against `moi-devrel/references/repo-map.md` before you trust a copied plan.
2. **The question the round answers.** One line. "After the 2026-09-11 reset, can a new user register an agent and pay for one?" A plan without it grows without end.
3. **Preconditions.** Wallets by label (A creator, B buyer; never a value), funds, accounts, tools, the build the testers run. Each is a case with id `P<n>` and a `must`.
4. **Cost and gates.** Which cases spend devnet funds, from which labelled account, with what cap in fuel and KMOI. The operator's yes names the paying account.
5. **Cases.** Tables, one case per line, below.
6. **Stop triggers.** What halts the round.
7. **Not covered.** Said plainly, so a pass is not read as more than it is.
8. **Sign-off table.** One row per area, filled at the end: pass, fail, blocked, with the case ids. The Launchpad's sign-off tables were never filled in; fill yours.

## A case, as a line
| Field | Holds | Rule |
|---|---|---|
| id | `L6.1`, `M4`, `P2` | Stable. A retest adds `-r1`. Reuse the ids of the pass you copied from |
| kind | chain, read, app, simulated | `real-chain.md` |
| who | operator, claude, both | A wallet, phone, Telegram or browser step is the operator's. Claude reads and logs |
| ask | The exact words typed, the click, or the command | Written so another person repeats it |
| must | What a pass looks like | True or false. Bold the part that decides it (the Launchpad's convention) |
| ground truth | Where the correct answer comes from | A URL, a chain read, a balance. "The model says so" is not one |
| cost | Free, or the interaction and the account that pays | Chain cases are gates |

The same case appears in the log as the seed row: `case_id`, `round`, `title`, `kind`, `performed_by`, `input` (the ask), `expected` (the must), outcome blank.

## The question to ask at each step
Two kinds of question run through a plan.

**The question put to the product.** It sits in the `ask` field, word for word. The previous operator asked for exactly this: "the questions I should ask" for each agent, and the requirements for each batch. Examples from the Launchpad batteries, each with a ground truth:

| Ask | Must | Ground truth |
|---|---|---|
| `what time is my delivery set for?` | The exact configured local time, correct across daylight saving | The agent's config on the page |
| `which timezone?` | The configured zone, or "not configured". Never a guess | Config |
| `did I apply to Netflix?` | "No". Inventing an application is a hard fail | The tracked list |
| `what's the price right now?` | The live number within drift, plus the distance to the threshold | CoinGecko `simple/price` for the asset |
| `convert 500 usd` | Real arithmetic with the rate shown | open.er-api.com rate |
| `change my threshold to 90000` | Refuses and points to the Launchpad | The product's rule |

Write probes of four kinds for any chat or agent product: a plain question it must answer from data; a question about a setting that does not exist (must say "not configured"); a request to change a setting from chat (must refuse); a question outside its scope (must say so). Add a CONFIG CHANGE step to every battery whose template has a setting (the Launchpad's `standup` has none): edit on the site, then expect both the "Settings updated" message and the changed answer within about 30 seconds, with no re-download.

**The question put to the operator.** Claude asks these at each step. They are in the plan so the operator is not surprised.

| When | Question |
|---|---|
| Before a chain case | "Case <id> costs one <interaction> from <account>, up to <cap>. Yes?" |
| Before a wallet step | "Is the wallet's active account the one you are signed in as?" |
| Before a phone step | "Is the phone paired to the account the test expects?" |
| Before a time-sensitive case | "What time is it for you, and in UTC?" |
| After any step | "Paste the message exactly as it appeared, the hash if there is one, and the balances." |
| After a failure | "Does it happen again? Is anything else on the screen?" |
| Before a re-download | "Did you download the setup script again and restart the agent after the last change?" |

## Rules for good cases
- **Real data.** Every battery uses real data. No invented values, no false "time set" claims.
- **Probes for invention.** Include a question whose true answer is "no" or "not available". The worst defect of 2026-07-30 was an agent that fabricated and stored three expenses when asked to delete one.
- **A control beside every negative case.** A refusal test needs one case that must succeed, "because a verifier that rejected everything would otherwise pass" (`moi-webinar/references/demo-standard.md`).
- **Count, do not read.** To test "not charged twice", count the interactions on the chain. The screen said success while two payments succeeded (2026-08-02).
- **Feedback on every flow.** Each flow shows loading, success and error states. Rahul asked for a pass over every flow for missing feedback; one case per flow.
- **Time of day matters.** Run date-sensitive cases in the evening local time, when local and UTC dates differ. The date defect appeared at 8:43 pm US Eastern on 2026-08-02.
- **One change per retest.** And re-download or recreate the thing under test when the plan says to.
- **Numbers on a screen are read from the page.** Read a stored value on the page before a probe that depends on it (the "goal 98" lesson).

## Worked lines (from the Launchpad plan, shortened)
```
| id   | kind  | who      | ask                                          | must                                                       | cost                  |
| L5.1 | chain | operator | Set the price to 100 in wallet A and approve the List | Note reads "Listed on-chain" with a hash; read it back | one List from A       |
| L6.2 | read  | claude   | Compare balances of A and B before (L6.0) and after  | A rose by exactly the price. B fell by the price plus fuel | none, reads only      |
| L6.4 | read  | both     | Subscribe to the same paid agent again, then count the Subscribe interactions on the chain | Sent to the copy already owned (the API says 409 already_subscribed). No wallet prompt. No new interaction | none |
```

## Stop triggers worth copying (post-cutover checklist)
A permanent on-chain value written wrong (the card address, `card_uri`, stored for each agent is permanent); long polls returning 502 or 504; a container in a restart loop; a webhook error date that keeps advancing. Stop taking new users until fixed.

## Not yet known
- A sign-off owner for each product. ASK: Rahul.
- The cap for devnet spend in a round. Only reactions are recorded. ASK: Rahul.
