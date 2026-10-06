# Message drafts

Drafts only. Claude fills one in, the operator reads it, edits it and sends it. Claude never sends, posts, comments or requests a review. Facts are as of 2026-10-02. Replace every `<...>`. The checker treats an unfilled placeholder as an error, so run it on your filled copy and not on this file. Each shape, and what a DevOps request must hold, is in `../references/house-style.md`, section 4. Channels are suggestions from `../references/people-and-teams.md`. Where the channel is not on record the line says ASK.

Before you send, from the working copy the message is about, never from inside a skill folder (`SKILLS` is the folder that holds the `moi-*` skills, quoted):
```
mkdir -p comms-drafts && printf '*\n' > comms-drafts/.gitignore
python3 "$SKILLS/moi-devrel/scripts/check-message.py" --to devops comms-drafts/<file>.txt
bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" comms-drafts/<file>.txt
bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" comms-drafts/<file>.txt
```
The first line makes a folder that hides itself from `git add`, because drafts name internal people. For a time, run `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "<YYYY-MM-DD HH:MM>" <area/city>` and write the weekday, date, 24-hour UTC and India time. `--to` takes devops, protocol, reviewer, status or other. Add `--hashes-ok` only when the draft carries an interaction hash or commit id copied from the explorer or `git log` (draft 8).

## To DevOps (Upendhar). Channel: Discord or a direct message, not fixed. ASK: Upendhar

For the website, Dataroom or Points, the asks already known (R1 to R12, with the step that needs each) are in `moi-web-products-ops/references/who-to-ask.md`. Fill `moi-web-products-ops/templates/devops-request.md` or draft 1 below.

### 1. One thing for them to do (shape 1)
```text
Hi <NAME>, about <product>: <what you saw, with the URL and the UTC time you read it>.
I think the fix is <what you propose>. Could you <the exact action: a command, a file, or the NAME of a setting> and send me <what to send back>?
I will check <health URL> right after and expect <healthy answer>. I would like this by <weekday and date>.
Already done on my side: <one line, or delete this line>.
```
Fill in: the product and the thing in the first sentence. Names, never values. One task.

### 2. Log lines for a time window
```text
Hi <NAME>, <product> is up but <page or action> fails since <date and UTC time>. Its health page shows <answer>.
Could you send me the <service or container> log lines from <UTC start> to <UTC end> on <date>? I am looking for <error text>. I would like them by <weekday and date>, because <what is waiting>.
```
Fill in: on 2026-09-15 a missing table was found this way.

### 3. Run the repo's migration once
```text
Hi <NAME>, the migration pull request <#N> in <repo> merged and the deploy finished at <UTC time> on <date>. The health page still shows <applied> applied and <expected> expected.
Could you run the repo's migrate command against production once and send me the line it prints? I will check the health page right after, and I am holding the code that needs the new table until the two numbers match. By <weekday and date>.
```
Fill in: for Points the command in the repo is `pnpm migrate`. How DevOps runs it on the box is not recorded. ASK: Upendhar. Do not invent the command. Running a migration on production is a write to a production database: it is DevOps's to do, and the message is a request, not a yes.

### 4. Close the loop
```text
Thanks <NAME>. I checked <URL> at <UTC time> on <date> and it shows <answer>, so <the outcome>. Nothing more is needed from you on this.
```
If it did not work: "It still shows <answer>. Could you <next exact action>?"

### 5. They asked for a token or key
```text
Hi <NAME>, a token should not travel in chat, so I will not send one here.
<Option A: if a token from me is what you need, which permissions does <workflow or package> need, so I create it and set it in GitHub myself?>
<Option B: you hold <variable NAME>. Could you set it in <repo>'s Actions secrets and tell me when it is done? I will re-run <workflow> only after you confirm.>
```
Fill in: keep one option. The approved way to give DevOps a secret is not recorded, so both options are proposals. ASK: Upendhar, then Rahul. `GHCR_PAT` and the Teleport tokens are DevOps's (`../references/keys-and-access.md`). Setting a secret and re-running a workflow are each a GATE for whoever does them.

## To the protocol team (Gokul). Channel not recorded. ASK: Rahul

### 6. After a suspected reset (shape 3 and 4)
```text
Hi <NAME>, I think devnet was reset. What I read: net.Version answered <version> at <UTC time> on <date>, and <the failing read or the account-not-found sign>. I have changed nothing yet.
Could you reply by number?
1. What is the new registry logic id?
2. Were agents re-imported, and from which snapshot?
3. Which js-moi-sdk and js-moi-agent-registry versions go with it?
4. Did KMOI's asset id, the fuel-price floor, the participant-creation minimum or the RPC path change?
5. Are the faucet wallets alive?
Until I hear, nothing points at a new id, and <what users cannot do>. I need 1 and 2 by <weekday and date>.
```
Fill in: the question list is inferred from what broke in August and September 2026. For a release note, use the six questions in `moi-blog/release-pack/references/the-note.md` in the same numbered form.

### 7. One question
```text
Hi <NAME>, <what you read: the command or URL, the answer, the UTC time>. <The question, naming the form of the answer: an id, a version, yes or no>? I need it by <weekday and date>, because <what it unblocks>.
```

### 8. A finding on the chain
```text
Hi <NAME>, I found something on devnet I would like you to look at. I did <the action, one line>. Interaction hash <hash>, receipt status <status>. net.Version read <version> at <UTC time> on <date>. I expected <expected> and got <observed>. Is this expected? By <weekday and date>.
```
Fill in: the receipt, never only the broadcast acknowledgement. Copy the hash from the explorer, then run the checker with `--hashes-ok`: it reads a 64 digit hex value as a possible key unless told otherwise, and reports it as a warning to confirm.

## To a reviewer (Rahul, Gokul, Robert). Rahul: Discord or the pull request. Others: ASK

### 9. Ask for a review
```text
Hi <NAME>, could you review <what, one line> by <weekday and date>? It is here: <fresh link> (a preview, deleted on <date>).
I am asking you to <approve | decide these points | check these points>: <the points>. I have checked <what>. I have not checked <what>.
When you reply, please say which version you read (<date or commit>).
```

### 10. Reply to a change request (shape 6)
```text
Hi <NAME>. On your request:
> <their words, exactly>
I did this in <commit or file read today>: <what changed>. I did not change <item> because <reason>, if any.
I checked <build, links, claim check>. Not verified: <what>.
Could you look again by <weekday and date>?
```
Fill in: read the commit id from the branch on the day, because a rebase changes ids. Replying and re-requesting review is a GATE.

### 11. Disagree once
```text
Hi <NAME>. On <their comment>: I followed <the standard>, which <person> gave me on <date> in <place>. I read your request as <their request>.
Two versions: A) <wording>. B) <wording>. Which should I use? If it is not yours to settle, who decides? By <weekday and date>.
```

## To Rahul. Discord, per `../references/people-and-teams.md`

### 12. Status update (shape 5)
```text
Hi Rahul, update as of <date>.
Done:
- <what changed> (<PR number and state, or commit, or URL read at UTC time>)
Partly done:
- <what>: <what remains>
To do:
- <what>, <not started | started | blocked on a name>, by <date>
Not verified:
- <what you assumed or did not read>
Needs from you:
1. <decision or question>? I recommend <option>, because <consequence>.
```
Fill in: delete an empty heading. Every Done line carries evidence. A long one goes in a document with a short message and the link (a GATE).

### 13. A decision (shape 7)
```text
Hi Rahul, one decision is blocking <what>: <the decision, one line>? You decide, or tell me who does.
A) <option>. This changes <what>.
B) <option>. This changes <what>.
Blocked until it is settled: <what>. Meanwhile I am doing <what>.
I recommend <A or B>, because <consequence>. I need it by <weekday and date>.
```

### 14. Correct a status already sent
```text
Hi <NAME>, a correction to my update of <date>. I said <what you said>. What is true: <what is true>. Next: <what happens, and by when>.
```

## To marketing owners and a colleague

### 15. Ask for an input. Slack. ASK: Sai Kiran which channel
```text
Hi <NAME>, for <what it is for> I need <the one thing>, with the dates it covers. Could you send it by <weekday and date>? Is it the latest for the month?
```
Fill in: delete the last question unless the thing is a figure. The community-call asks are in the `moi-webinar/community-call` input request set.

### 16. One finding on a colleague's pull request. The operator posts it
```text
Issue <N>: <what the issue is>
Why it is an issue: <why, with the source>
Where: <file and line or section>
Suggested fix: <the fix>
```
Fill in: send the critical issues first and reconcile the counts. Findings about the text, not the person.
