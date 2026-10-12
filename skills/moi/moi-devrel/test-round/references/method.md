# Method: plan first, one case per line, log as you run

Facts are as of 2026-10-03. `ASK:` is defined in `moi-devrel/SKILL.md`. The method comes from the Agent Launchpad test rounds (30 July to 4 August 2026, 19 August, 12 to 24 September) and the MCP connector checks. Back to `../GUIDE.md`.

## The loop in six lines
1. Write the plan before the first case runs. One case per line. The operator reads it and says yes.
2. Seed the log from the plan: one row per case, outcome blank. Every case not yet run then shows up in the checker.
3. Run one case at a time, in dependency order. Do not batch two cases into one step.
4. The operator performs everything that needs a wallet, a phone, a Telegram account or a browser session. Claude reads, asks, logs and reads the chain. Claude never signs and never handles a recovery phrase.
5. Write the row when the case ends, not at the end of the day. Paste the output as it appeared.
6. Read every hash back from the node. Success is the receipt, not the screen.

## 1. Scope the round
Say in one line what changed and what this round must show. The Launchpad rounds had these triggers; each one changes which cases matter.

| Trigger | Cases to run | Where it was done |
|---|---|---|
| Before a launch or a merge to production | The full list for the product | Launchpad rounds, 30 July to 4 August 2026 |
| After a payment or relay change | Payments and the chat batteries | Named as a trigger in the notes on the Launchpad pass; no dated round is recorded for it |
| After a host move | Smoke test, then the cases only the move can break | `POST-CUTOVER-CHECKLIST.md`, after the move of 2026-08-03 |
| After a devnet reset | Fresh-wallet journey and the payments audit | Launchpad post-reset checks, 12 to 24 September 2026 |
| After each production deploy of the MCP server | The end-to-end check in `mcp-pass.md` | `docs/deploy-checklist.md`, step 7 |
| Onboarding a new user of the MCP server | The same check | Same |

Write down the target (the live host, never an old one), the version under test, and what the round will not cover. The post-cutover checklist states that it does not replace the full list; say the same about any short round.

## 2. Preflight, read-only
Nothing here costs devnet funds. Log each as a case of kind `read` with id `P1`, `P2` and so on.
1. Node build: `net.Version` (command in `real-chain.md`). Record it. A product tested on an older node than the release notes describe gives results about the older node (`moi-devrel/references/devnet.md`, "The build-lag trap"). If `curl` exits 60 the certificate has expired (as of 2026-10-04): log `P1` as blocked with the exit code and the UTC time (`real-chain.md`).
2. Reset signs: the product's own status endpoint, the registry read, "account not found" anywhere (`moi-devrel/references/devnet.md`, "Signs of a reset"). If the chain was wiped, stop and run `moi-devnet-reset` first.
3. Product health: the GET checks in `moi-devrel/references/repo-map.md` ("Read-only health checks"). Read the data, not only the status code, and call a stats endpoint twice 20 to 60 seconds apart.
4. The tester's side: wallet extension or phone installed and unlocked, the active account is the one you sign in as, balances recorded before the first chain case.
5. The plan's own header: the target is a live host and the documents in front of you do not name an older one.

## 3. Write the plan
`plan-format.md` says what the plan holds. Rules that came from the rounds:
- Order cases by dependency: preflight, sign-in, create, use, pay, delete. A fresh wallet journey runs early, because it is the flow a newcomer meets first.
- Inventory a web product first: list its pages, buttons and fields (the Launchpad's `docs/UI-INVENTORY.md` was extracted from source: 8 routes, 5 shared components) and check each control appears in a case.
- Every case has a pass criterion that is either true or false. "Looks fine" is not one.
- Put the cost on the plan: which cases spend devnet funds, from which account, with what cap. The operator's yes names the paying account (`../GUIDE.md`, Gates).
- Add the time. The Launchpad final pass was 2 to 3 hours in one sitting: preflight 10 minutes, the new-user journey 20, template batteries 45, new controls 20, payments 45, platform sweep 15. The MCP end-to-end check takes about 10 minutes with a funded wallet. No time is recorded for the public health checks: time your own and write it in the plan.
- Add stop triggers: what makes the round halt (a restart loop, a permanent on-chain value written wrong, every self-hosted agent dead).
- Decide a safe release: if a feature is not proven, ship without it on a separate branch. During the Launchpad rounds the previous operator asked for the build without payments, with payments on their own branch, and said nothing about payments should deploy until they were complete. Who decides now: ASK: Rahul.

## 4. Run: the loop for one case
Say each of these to the operator as plain lines. Keep the case id in every message.

| Step | Claude says or does | Why |
|---|---|---|
| 1 | "Case L6.1. You: click Pay in wallet B. Cost: one Subscribe interaction from B. Yes?" Wait for a yes on any chain case | Spending devnet funds is a gate |
| 2 | Before a wallet step: "Is the wallet's active account the one you are signed in as?" | The most common cause of confusing failures in the Launchpad rounds |
| 3 | After the step: "Paste the message as it appeared, the hash if there is one, and the balances." | The exact message usually pins the cause (`E2E-TESTING.md` header) |
| 4 | Write the row now. `config` holds what was set, `input` the exact words or clicks, `output` the paste, `evidence` what proves the verdict | A log written later is a memory, not a record |
| 5 | Chain case: read the hash back, then fill `receipt_status`, `node_version`, `run_at_utc` | `real-chain.md` |
| 6 | Pass or fail against the plan's `must`, and nothing else. If the result is something the plan did not foresee, log what happened and add a case | Do not move the goalposts after the fact |

Run `python3 "$SKILLS/moi-devrel/test-round/scripts/test-log-check.py" test-round-<slug>/test-log.csv` after every ten rows or so. Exit 2 means a row broke the CSV (an unquoted comma shifts the columns).

Pace: one thing at a time. When the operator narrows a request, do exactly that. During the Launchpad rounds (July to August 2026) a request to drop one step from the instructions and explain only the config step meant exactly that.

## 5. Diagnose a failure
1. Capture the exact message first. The Launchpad shows machine codes and wallet errors verbatim, so the message is usually enough.
2. Reproduce once. A failure that does not repeat is logged as seen once, with the time.
3. Decide whose it is: the product, the test, the environment (a reset, an empty wallet, a stale document) or not ours (the wallet, the chain). `after-the-round.md`, section 1.
4. State the cause as observed or as a hypothesis, in those words. The "goal 98" item stayed open from 2026-07-30 to 2026-08-02 with a suspected cause (config drift) that proved wrong. The real cause, the mouse wheel changing a number input, showed only when the stored value was read on the page.
5. Change one thing, then retest. Fix, redeploy, retest.

## 6. Close the round
- Run the checker until it exits 0. Fill the plan's sign-off table (the Launchpad's own sign-off tables were never filled in).
- Write the hand-back from `../GUIDE.md`. State passes on the real devnet and passes on something simulated as two numbers.
- Drafts for fixes, issues and messages go in `test-round-<slug>/drafts/`. `after-the-round.md`.
- List what the round created in the live product (agents, listings, clones) and propose removing it with the product's own delete flow (`launchpad-pass.md`, L7). On the Launchpad that is a chain case and a gate, and the product keeps soft-deleted rows and the registry keeps deprecated entries, so a cleaned-up round still leaves a trace (`docs/QA-LEDGER.md`).

## Other products
No pass is recorded for these. Start from their health checks and build a plan with `plan-format.md`.

| Product | Where its checks live | Note |
|---|---|---|
| Agent Explorer | `moi-devrel/references/repo-map.md` health checks; compare `/registry/agents` total with the chain | `/health` says ok while the index is stale (49 agents on 2026-10-02). `moi-launchpad-ops/explorer` |
| Website and blog | `moi-devrel/references/repo-map.md` health checks | A 200 proves little: the site answers 200 for any address. `moi-web-products-ops` |
| Dataroom | `moi-devrel/references/repo-map.md` health checks | `moi-web-products-ops` |
| Points Program | `moi-devrel/references/repo-map.md` health checks | `moi-web-products-ops` |
| A webinar demo | `moi-webinar/references/demo-standard.md` | Preflight, spike, adversarial suite with a control |

A test case never touches a product's admin. Read the product's row in `moi-devrel/references/repo-map.md` first. Four of the products above carry a marker:
- Agent Explorer: A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin.
- Website: A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin.
- Dataroom: A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin.
- Points: A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin.

## Not yet known
- Who owns test rounds and signs off a release now. ASK: Rahul.
- Whether a standing automated QA agent is wanted. The previous operator asked for one and then said he would test by hand. ASK: Rahul.
- Where a durable record of a round should live. The Launchpad kept hashes in `docs/QA-LEDGER.md` in its private repo. ASK: Rahul.
