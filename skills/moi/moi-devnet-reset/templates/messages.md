# Draft messages for a devnet reset

Drafts only. Claude fills the angle brackets from the reset log, the operator reads each one, and the operator sends it. Nothing here is sent by Claude (GATE). Who gets what, when, and the rules: `../references/telling-people.md`. Write times as a date, 24-hour UTC and India time. Never paste a key or a recovery phrase into a message. Back to `../SKILL.md`.

Check a filled draft before the operator reads it. Save it in the reset folder (`devnet-reset-<date>/`, which git ignores) and run these from the working copy that holds that folder, never from inside a skill folder:
```
python3 "$SKILLS/moi-devrel/scripts/check-message.py" --to <kind> "devnet-reset-<date>/<draft>.txt"
bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" "devnet-reset-<date>/<draft>.txt"
bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" "devnet-reset-<date>/<draft>.txt"
```
The kind: `protocol` for messages 1 and 2, `devops` for 3a to 3c, `status` for 5, `other` for 4a, 4b, 6 and 7. Exit 1 means an error (a placeholder left in, a secret-shaped value, a skill word such as `ASK:` or `GATE`); the no-question and no-date warnings on the notices (2, 4a, 7) are expected because they state facts and ask for nothing. Other drafts for teammates (a review request, a decision, one question) are in `moi-devrel/templates/messages.md`; its draft 6, "After a suspected reset", is the short form of message 1 here.

## 1. To the protocol team: the facts (step 1 and step 4)
Channel: not known. ASK: Rahul. Send to Gokul.
```
Hi Gokul, devnet looks reset. What we read at <HH:MM> UTC on <YYYY-MM-DD> (<HH:MM> IST):
- net.Version is <version>, the genesis tesseract of <founding account, short form> is now <short hash>, it was <short hash>
- the registry <old short id> answers "account not found"
Could you tell us the following?
1. the new registry logic id
2. whether agents were re-imported, and from which snapshot
3. the js-moi-sdk and js-moi-agent-registry versions to use
4. whether KMOI's asset id, the fuel price floor, the minimum grant for creating a participant, or the RPC path changed
5. whether the faucet wallets are alive
6. whether this state is final, or will the registry be replaced again
We are not moving anything until we hear. Thanks.
```

## 2. To the protocol team: done (step 14)
```
Hi Gokul, update on the reset of <YYYY-MM-DD>. The Launchpad, the MCP server and the Explorer now point at <new short id>. What we checked, all by receipt or read:
- <check and result>
- <check and result>
Not done yet: <item>, because <reason>.
If you want anything re-checked on your side, tell us which.
```

## 3a. To DevOps: the Launchpad's registration wallets
Channel: not fixed. ASK: Upendhar. One task per message. Do not ask for the mnemonics in chat.
```
Hi <name>, the three Launchpad registration wallets were wiped with devnet, so new users cannot activate a wallet.
Fix: our script scripts/recreate-registration-wallets.mjs creates them again from one funded sponsor wallet. It needs MOI_REGISTRATION_MNEMONIC_1 to _3 in the environment of whoever runs it, and we do not hold them.
Could you tell us which of us runs it, and how the three values reach that person without going through chat? We would like to hear by <weekday and date>.
How to check: the dry run lists all three as existing, and a fresh wallet activates on https://launchpad.moi.technology/connect.
Sponsor wallet: <who> funded it from the faucet at <HH:MM> UTC.
```

## 3b. To DevOps: a deploy or a VM task
```
Hi <name>, one thing on <host or product>: <the problem in one line>.
Fix: <the exact action, for example "run the workflow 'Deploy MOI MCP Gateway' on feat/moi-mcp with deploy_target production">.
Why now: <the registry id changed to <short id> after the reset of <date>>.
How to check: <the exact command and the expected answer>.
Could you do this by <weekday and date>?
```

## 3c. To DevOps: the Explorer sync
```
Hi <name>, the Explorer index still lists the agents of the old registry. Once the new image is up, could you run "npm run sync" in server/ inside the backend container of the production Explorer? It rebuilds the agents table from the registry <short id>. As far as the code shows, it removes no rows.
How to check: every agent of the registry <short id> appears at https://api.agents.moi.technology/registry/agents. Rows of the old registry may remain; tell us if you want them removed, we will not touch them. We would like the sync run by <weekday and date>.
```

## 4a. To users: first notice (needs the operator's call and, if Rahul wants it, his review)
Send only after the protocol team has confirmed the reset (step 4): the notice names the cause. Channel: the Discord server behind the Launchpad dashboard's "reach out on Discord" link. Which channel: ASK: Rahul, Sai Kiran.
```
Devnet was reset on <YYYY-MM-DD>. Wallets, assets and agent registrations on devnet were wiped.
What this means on the Launchpad: activating a new wallet and registering an agent do not work yet. Nothing is wrong with your wallet.
What you will need to do afterwards: agents you created before the reset will show "need registering again" on your dashboard. Register them from there. If you run an agent on your own machine, download its setup script again.
We will post here when it works. If you are stuck, reply here.
```

## 4b. To users: fixed (only after step 14 and a fresh-wallet pass)
```
The Launchpad works on devnet again as of <HH:MM> UTC on <YYYY-MM-DD> (<HH:MM> IST).
New wallets can be activated and agents can be registered.
If you created agents before the reset, open your dashboard and register them again. Self-hosted agents need a fresh setup script from launchpad.moi.technology.
Something still wrong? Reply here with the message you see.
```

## 5. To Rahul: status
Lists only work done. To-dos are labelled as to-dos.
```
Reset of <YYYY-MM-DD>, status at <HH:MM> UTC.
Done: <each item with its proof>.
To do: <each item, who it waits on>.
Decisions for you: <ownership of each product; whether a notice goes to users; ...>.
Unknown: <each ASK still open>.
```

## 6. To the Voyage team: the MCP sync pull request
```
Hi <name>, a pull request in voyage-api: <link>. It syncs moi-mcp/ from sarvalabs/moi-mcp master and pins the registry <short id> after the reset of <date>. Nothing deploys until someone runs "Deploy MOI MCP Gateway". Could you review it by <weekday and date>, and tell us who runs the workflow for dev and for production?
How to check after the run: both /health answer ok and the tool moi_resolve_agent returns an agent.
```

## 7. To the owner of a copy we cannot edit
One sentence per item, and the replacement.
```
Hi <name>, devnet was reset on <YYYY-MM-DD>, so <the id, hash or claim> in <the Luma page, the Buffer draft, the call deck, the YouTube description> is no longer true.
Please change "<exact old sentence>" to "<exact new sentence>", or take it out.
If it is a demo: please run the session's preflight before you present it again.
```
