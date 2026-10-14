# moi-devrel/test-round: MOI test round

Branch of `moi-devrel`. `$SKILLS`, the operator, `ASK:`, the house rules and the gates are in `moi-devrel/SKILL.md`; this guide adds what is specific.

## What this covers
A test pass on a MOI product. The plan is written first, one case per line. Each case is run once and logged as it runs. The operator performs every wallet and phone step, and the chain is read back from the node. The result is a plan, a log that `scripts/test-log-check.py` checks, and drafts for whatever must change. Two passes are recorded and reusable: the Agent Launchpad (30 July to 4 August 2026) and the hosted MCP connector. No pass is recorded for the Explorer, website, Dataroom or Points: build one with `references/method.md`. Facts are as of 2026-10-03. Which products DevRel owns now is not settled. ASK: Rahul.
Not covered: running, deploying or resetting a product (`moi-launchpad-ops`, `moi-mcp-ops`, `moi-launchpad-ops/explorer`, `moi-web-products-ops`, `moi-devnet-reset`), building and rehearsing a demo (`moi-webinar`), checking a public claim (`moi-devrel/claim-check`), commits and pull requests (`moi-devrel/ship`), messages to teammates (`moi-devrel/references/house-style.md`, section 4).

## Before you start
Run every command from the working copy of the repo that holds the product (Launchpad: `sarvalabs/moi-agent-launchpad`, private; MCP: `sarvalabs/moi-mcp`, public), with paths quoted. Only the Launchpad verifier script (L11) and the MCP repo's own test tiers need a working copy; every other command reads a public host, so with no working copy use a new empty folder outside any repo. Set `SLUG` once in the shell to a short name for the round, for example `SLUG=launchpad-2026-10-05`; every command below quotes it. Terms such as interaction, fuel, KMOI, anu and devnet are in `moi-devrel/references/glossary.md`.
- [ ] The product, and what changed since it was last tested (a deploy, a reset, a new feature). The operator provides. Ask: "Which product, and what changed?"
- [ ] The target (the live host, never an old one) and the version under test. For the Launchpad no endpoint reports the commit: take the head of the last green "MOI Agent Launchpad CI/CD" run and write "inferred" (the run list needs read access to the private repo, ASK: Rahul). `GET /api/runtime/version` reports a fingerprint of the agent runtime bundle, not the commit: record it as well. ASK: Upendhar for the VM side; for history read `project-handover-docs/AGENT-LAUNCHPAD.md`.
- [ ] Wallets and funds. Two separate funded MOI Wallet accounts for the Launchpad (a creator cannot buy their own agent). The operator creates and funds them. Claude never handles a recovery phrase.
- [ ] A budget of devnet funds and time, and the paying account. Ask: "Which account pays, up to how much?"
- [ ] The plan sources. The Launchpad lists are copied into `references/launchpad-pass.md`, so the private repo is not needed to plan or run them. Its verifier script (`scripts/verify-purchase.mjs` in `sarvalabs/moi-agent-launchpad`, used in L11) stays in the private repo and needs the packages installed, a download and so a GATE. It needs read access to the private Launchpad repo (ASK: Rahul): if access is not granted, log the L11 verifier case as `blocked`.
- [ ] Tools: the MOI Wallet extension or phone, a Telegram account (Launchpad), a free Groq key of the tester's own (no company Groq key exists as of October 2026; each tester creates one at console.groq.com), typed by the operator at the agent's install prompt, a claude.ai plan that allows custom connectors (MCP; unknown, ASK: Rahul).
- [ ] Failures already known, so they are logged as known and not as news: `references/launchpad-pass.md` ("What changed", P3, L11) and `references/mcp-pass.md` ("Expected failure today").

## The run
Round files live in `test-round-<slug>/`. A log names accounts and people, and `sarvalabs/moi-mcp` is public, so step 1 makes the folder ignore itself.

| # | Step | What to do | Where or command | Done when |
|---|---|---|---|---|
| 1 | Scope | One line: what changed and what the round must show. `mkdir -p "test-round-$SLUG/drafts" && printf '*\n' > "test-round-$SLUG/.gitignore"` | `references/method.md` section 1 | The operator confirms the line and the target |
| 2 | Preflight (reads) | `net.Version`, product health, signs of a reset. Each is a `read` case | `references/method.md` section 2; `moi-devrel/references/devnet.md`; `moi-devrel/references/repo-map.md` | Node build recorded. No reset sign, or `moi-devnet-reset` first |
| 3 | Plan first | `cp "$SKILLS/moi-devrel/test-round/templates/test-plan.md" "test-round-$SLUG/test-plan.md"`. One case per line, each with the question to ask and a true or false pass criterion. Copy from the recorded pass that fits | `references/plan-format.md`; `references/launchpad-pass.md`; `references/mcp-pass.md` | Every case has kind, who, must and cost. The operator has read it |
| 4 | GATE: the spend and the test data | Show the chain cases, the paying accounts, the cap, and what the round leaves in the live product (agents, listings, clones) and how it is removed. Wait for the yes | Gates below | A yes that names the account and the cap |
| 5 | Seed the log | `cp "$SKILLS/moi-devrel/test-round/templates/test-log.csv" "test-round-$SLUG/test-log.csv"`, delete the `#` row, add one row per case with the outcome blank | `references/log-format.md` | The checker lists each case as NO OUTCOME (exit 1) |
| 6 | Run (a chain case and a download are GATE) | One case at a time, in dependency order. The operator does the wallet, phone, Telegram and browser steps and any download. Write the row when the case ends, with the output as it appeared | `references/method.md` section 4 | Every attempted case has an outcome and a row |
| 7 | Prove on chain | Read each hash back from the node. Fill `receipt_status`, `node_version`, `run_at_utc`. Success is the receipt | `references/real-chain.md` | No chain row lacks them |
| 8 | Diagnose, fix, retest (push, issue, merge, deploy are GATE) | Sort each fail, draft the finding and the issue, hand the change to `moi-devrel/ship`, retest as a new row | `references/after-the-round.md` | Each fail has a fix, a draft or an acceptance, and a passing retest |
| 9 | Check the log | `python3 "$SKILLS/moi-devrel/test-round/scripts/test-log-check.py" "test-round-$SLUG/test-log.csv"` | `references/log-format.md` | Exit 0, and the WARN list read |
| 10 | Hand back | Fill the plan's sign-off table, then the format at the end of this file | Hand-back | The operator has read it |

## Which file to read
| Doing | Read |
|---|---|
| The method: scope, preflight, the loop for one case, diagnosis | `references/method.md` |
| Writing the plan, the question to ask at each step | `references/plan-format.md`, `templates/test-plan.md` |
| Writing the log, the columns, re-checking a row | `references/log-format.md`, `templates/test-log.csv` |
| What counts as real and what is simulated, reading the chain | `references/real-chain.md` |
| Testing the Agent Launchpad | `references/launchpad-pass.md` |
| Testing the hosted MCP connector | `references/mcp-pass.md` |
| After a failure: finding, issue draft, fix, retest, messages | `references/after-the-round.md` |
| Every trap with its incident | `references/traps.md` |
| Testing a change to this branch | `evals/evals.md` |

## Facts that fail silently
| Rule | The incident |
|---|---|
| A success message is not proof. Count interactions on the chain | 2026-08-02: two Subscribe interactions succeeded for one agent while the screen said success |
| Success is the receipt, not the broadcast, a 200 or a simulation | September 2026: wallet activation said "Wallet is ready" while the chain reverted it. A fuel price of 1 simulated fine and bounced |
| A refusal passes only for the right reason | 2026-08-31: a policy beat "passed" because the agent was out of fuel |
| Test the build you think you are testing | 2026-07-30: a self-hosted agent keeps old behaviour until the setup script is downloaded again and pm2 restarted. Record `/api/runtime/version` |
| Label a hypothesis, and read the stored value first | "Goal 98" stayed open 2026-07-30 to 2026-08-02 under a wrong theory. The mouse wheel had changed a number input |
| A number needs its age. Read a stats endpoint twice | A first `/api/stats` call after idle can say `stale`. On 2026-10-03 at 17:37 UTC the chain marketplace listing answered 7 agents and about a minute later 0 |
| The wallet's active account must be the signed-in account | The most common cause of confusing failures in the Launchpad rounds |
| Write times in UTC and test date cases in the evening | 2026-08-02 at 8:43 pm US Eastern a date was filed a day late |
| A hash from before a reset is not found. Log the node version and time | Devnet was wiped on 2026-08-15 and 2026-09-11 |
| Never present a simulated pass as a real one | 2026-08-07: registry writes were down, so session 7 ran on two agents registered earlier, happy path only, and said so |
All of them, and more, are in `references/traps.md`.

## Gates
Every gate in `moi-devrel/SKILL.md` applies. These are the ones a round meets most.
- Any chain case: signing, spending devnet funds, registering or deleting an agent on devnet, creating an asset, deploying a logic. The yes names the paying account and the cap. A faucet request is a write: the operator makes it.
- A write request to a live product (a payment-less subscribe call, an API replay), test data the round leaves in it, and any admin write on production.
- Push, pull request, merge, issue, comment, a deploy or manual workflow run, a database migration or any write to a production database, a repository secret or variable. A merge to the Launchpad's `master` deploys it.
- Restarting or changing anything on a VM. Claude never logs in to one: ASK: Upendhar.
- Sending a message to anyone. Claude drafts, the operator sends.
- Committing, uploading or sharing the log or any file in cloud storage. Downloading a file, including `npm ci`: say its name, source and size.
- Marking a failure "accepted": only a named person, with the date, in the `fix` cell.
- Wallet and phone steps are the operator's. If a recovery phrase turns up in a log or a paste, do not repeat it and tell the operator it is exposed.
Details: `moi-devrel/references/consent-and-identity.md`.

## Keys and access
Names only. Where each lives: `moi-devrel/references/keys-and-access.md`.
- Two funded MOI Wallet accounts and a phone: the operator's own; no key is shared. The Voyage faucet holds no key.
- A free Groq key of the tester's own, typed by the operator at the agent's install prompt. The server's `GROQ_API_KEY` is a different key and is not needed. No company Groq key exists (October 2026), so every tester uses their own free key from console.groq.com.
- `TELEGRAM_BOT_TOKEN`: only for the Launchpad webhook check; the operator reads it into a variable without printing it (`moi-devrel/references/consent-and-identity.md`, section 4). It was held by the previous operator through BotFather. ASK: Rahul who holds it now; without it, log that check `skipped`.
- Read access to the private `sarvalabs/moi-agent-launchpad`, and a claude.ai plan with custom connectors: ASK: Rahul.
- MCP server: A security finding is open on this product as of 2026-10-02. See the Open items of project-handover-docs/MCP-SERVER.md before touching its admin; ASK: Rahul if unclear. This branch touches no admin.

## Hand-back
```
Round: <product>, <target>, <version>, node <net.Version>, <date>
Produced: <plan path>, <log path>, <drafts path>
Result: <N> passes on the real devnet or live product, <M> on something simulated, <F> fails, <B> blocked, <S> skipped
Open: <each fail or blocked case: fix, draft path, or owner>
Spend: <devnet funds spent, by which account, from the operator's numbers>
Not verified or simulated: <say so, or "none">
Ready: yes or no, because <one reason>
```
Ready is yes only when `scripts/test-log-check.py` exits 0, every fail has a passing retest or a named acceptance, and the operator has read the simulated and blocked cases. Whether to release is the product owner's call. A status lists work that was done; planned work is labelled as a to-do.
