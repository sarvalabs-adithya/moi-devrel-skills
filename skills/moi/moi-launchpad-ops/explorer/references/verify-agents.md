# Verify agents on the Explorer

Facts are as of 2026-10-03 (probes) and 2026-10-02 (research and the previous operator's clone of `sarvalabs/agent-explorer`). `ASK:` is defined in `moi-devrel/SKILL.md`. Back to `../GUIDE.md`.

Agent Explorer: A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin.

## 1. What "verified" means
The `agents` table has a `verified` flag. It is set in three ways.
| Source | Rule | Where | Live on 2026-10-03 |
|---|---|---|---|
| An admin decision | An admin wallet signs the decision and the server writes it. On PR #5 it also writes `verified_by_admin`, which the reconcile never overwrites | The admin page of the site | Only if some admin address is set in production. Unknown. ASK: Gokul or Upendhar |
| The Launchpad rule on `main` | At indexing, `verified` is set when the card URI's origin equals `LAUNCHPAD_ORIGIN` (default `https://launchpad.moi.technology`), its path starts `/api/moi/card/` and the card was fetched. The update is `verified = verified OR new`, so the rule only adds | `server/src/indexer/agents.ts` | Presumably, from the successful run of 2026-09-24 (the live commit cannot be read from outside). It acts only when a row is indexed. The 23 rows on the retired Launchpad host cannot match it |
| The host rule on PR #5 | Verified when the card URI or the `url` host is in `LAUNCHPAD_HOSTS` (default `launchpad.moi.technology,moi-agent-launchpad.vercel.app`). No call to the Launchpad. The reconcile recomputes `verified` only where `verified_by_admin` is NULL | same file | No: PR #5 is not deployed |
On 2026-10-03 the index held 49 rows and 1 verified. Do not write that verified means audited, vetted, endorsed or safe. The rules look at where an agent's card is hosted. What the flag is meant to prove is a question for Gokul.

History, because old commit messages disagree: an opt-in auto-verify, off by default, on 2026-09-22 (`3807372`), then polling the Launchpad's marketplace the same day (`bb5d38e`), both removed on 2026-09-23 (`a43f125`, "Verification goes back to admin-only"), then the card-URI rule (`96b411f`, 2026-09-23), then the host rule in PR #5 (`508be01`, 2026-10-02). Read the code, not the message.

## 2. Who can verify
A wallet whose address is on the server's admin list can verify. Whether any admin address is set in production is not known. ASK: Gokul or Upendhar. The admin page checks the connected wallet's address first, writes nothing, and shows "This wallet is not authorized to access the admin panel." when it is not on the list.

## 3. The run: verify or un-verify one agent
Kinds: READ, GATE (needs the operator's yes naming the agent, the value and the site), VERIFY.
| # | Kind | Step | Command or where | Done when |
|---|---|---|---|---|
| 1 | READ | Find the agent and its current state. Note `agent_id`, `card_uri`, `url`, `verified` | `curl -s 'https://api.agents.moi.technology/registry/agents?verified=false'`, or add `owner=<address>` | You have the exact `agent_id` |
| 2 | READ | Look at the card the row points to. If the host does not serve it, the row shows a raw id | Open `card_uri` in a browser | You know whether the card loads |
| 3 | READ | Decide whether it should be verified. What qualifies an agent beyond the Launchpad rule is not written down. ASK: Rahul or Gokul, in writing | The reply | The operator holds the answer |
| 4 | READ | Is the operator's wallet an admin. Step 5 is an admin write: read the Agent Explorer line at the top of this file first | Open https://agents.moi.technology/admin, connect MOI Wallet. The page says "This wallet is not authorized to access the admin panel." when it is not | Admin or not. If not, stop and ASK: Gokul |
| 5 | GATE | Toggle the agent. This is an admin write on production. The operator does it in the browser. The page asks the wallet to sign the message `moi-explorer-admin:verify:<agentId>:<true or false>:<unix seconds>`; what the wallet displays of it is not recorded. Claude never signs and never handles a recovery phrase | The admin page | The page shows no error |
| 6 | VERIFY | Read the row back | `curl -s https://api.agents.moi.technology/registry/agents/<agentId>` | `verified` is the value chosen |
| 7 | VERIFY | Check the decision holds. On `main`, an un-verify of an agent that matches the Launchpad rule is undone the next time the row is upserted (a full sync), because the update is `verified OR new`. On PR #5 it holds (`verified_by_admin`) | Read the row again after the next sync | Still the value chosen |

If the page reports an error, these are the answers it can carry. A signature is valid for 5 minutes.

| Answer | Meaning |
|---|---|
| 400 | A field is missing |
| 401 `Signature expired` | The timestamp is more than 5 minutes off. Try again, and check the clock of the machine with the wallet |
| 403 `not_an_admin_address` | The address is not on the server's admin list |
| 403 `no_account_keys` or `key_not_registered` | The account does not exist on the current chain, or the signing key is not one of its keys. After a reset an admin account may be gone (inferred) |
| 404 `Agent not found` | The `agentId` is not a row |

## 4. Verifying Launchpad agents in bulk
Do not mark them one by one. The rule does it at indexing (`main`) or at every reconcile (PR #5), so the fix for unverified Launchpad agents is a working sync: `index-sync.md`. On 2026-10-03 no row sits on `launchpad.moi.technology`, and the Launchpad's `/api/stats` read `registered: 0`, so the registry may hold none of them (inferred, not measured; the research could not explain why `registered` fell from 6 on 2026-10-01 to 0 on 2026-10-02). The Launchpad's own side is `moi-launchpad-ops`.

## 5. Open questions the previous operator drafted for Gokul
A draft design issue, never posted, exists on the previous operator's machine (`drafts/agent-explorer-design-issue.md` in his worktree of MOI-Webinars, untracked). ASK: Adithya for a copy. It was written for the closed PR #4 and before PR #5, so two of its decisions are overtaken (PR #5 contains the read-only caller and the page advance). Its questions that still stand:
1. Which address does the Launchpad write in `card_uri`: `agent_id`, `agent_wallet` or another?
2. Does the production server set `MOI_AGENT_REGISTRY_LOGIC_ID` and `MOI_MNEMONIC` today?
3. Who tests a browser registration before the client moves to SDK 0.9.0-rc2?
4. Should pruning rows that are not on chain sit inside `npm run sync` or apart from it?
The draft's fifth question (page size 50) is overtaken: PR #5 advances by what the registry returns, and its commit message says the cap is 25.

## 6. Wording in public text
Say "marked verified by the Explorer's admins or by its Launchpad rule", with the date and the count. Do not say audited, vetted or endorsed. Check any such sentence with `moi-devrel/claim-check` before it ships.

## Not yet known
- Whether any admin address is set in production, and who holds those wallets. ASK: Gokul, Upendhar.
- What qualifies an agent for an admin's yes. ASK: Rahul.
- The answers to questions 1 to 4. ASK: Gokul.
