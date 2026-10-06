# DevOps request skeleton for the website, the Dataroom and Points

Claude drafts, the operator sends (Discord or a direct message; the channel is not fixed, ASK: Upendhar). One task per message. Never put a secret, a key or a recovery phrase in it, and never ask for one: secrets live in GitHub. Which request to use: `references/who-to-ask.md`. Check a filled draft with `python3 "$SKILLS/moi-devrel/scripts/check-message.py" --to devops <file>` (see `moi-devrel/templates/messages.md`).

## The shape
```
<Name>, <one sentence: what I saw, on which product, at what UTC time>.
<One sentence: what I think is wrong, or "I do not know the cause">.
Could you <the exact action>? <Where it is: the workflow, the file, the command, the branch.>
To check it worked, <a URL or a command> should show <the exact expected result>.
Once you confirm I will <the next step you take>.
```
Rules from past corrections (`references/who-to-ask.md`): specific and actionable, no labels such as "Owner:", no em dashes, say what the request is about, do not reopen settled items, state only work that was done. Times carry a date and 24-hour UTC.

## Filled examples (replace the angle brackets)
R8, Points migration:
```
Upendhar, Points pull request <#N> adds migration <NNNN_name>, and I have not merged it. The app refuses to start when the database has fewer migrations than the build, and a merge deploys at once, so the database needs the migration first.
Could you apply it to production before the merge? The runner is `node scripts/migrate.mjs` (`pnpm migrate`). It reads the drizzle folder of the current directory, or the folder named in MIGRATIONS_DIR, and DATABASE_URL, so it can run from a checkout of branch <branch>. Please send me the lines it prints: "migrations: applied <tag>", then "migrations: <n> applied, <m> total", or "migrations: up to date (N applied)".
To check it worked, https://points.moi.technology/api/health should show migrations applied <N+1> and expected <N>, still healthy, because a database ahead of the build is allowed.
Once you confirm I will merge pull request <#N>, and after the deploy the same page should show <N+1> of <N+1>.
```
R3, website log line:
```
Upendhar, https://moi.technology/api/community-calls answered 500 on 2026-10-02 and again at <UTC time>.
I think the Supabase project does not have the table or function the server expects, but I cannot see why.
Could you send me the server log lines that start with "Fetch calls error:" from the last <hour>? They name the reason.
To check, the lines should name the reason the request failed.
Once I have it I will take it to whoever owns the Supabase project.
```
R4, nginx:
```
Upendhar, three small nginx changes for moi.technology would remove old faults: unknown addresses answer 200 with the app shell, the home page has no Link header, and the PDFs under /papers/ have no Content-Disposition.
Could you make unknown addresses return 404, add this Link header on / (<the Link line of public/_headers, from PR #57 or main: see R4 in who-to-ask.md>), and add "Content-Disposition: attachment" for /papers/*.pdf?
To check, `curl -sI https://moi.technology/zz-no-such-page` should say 404 and `curl -sI https://moi.technology/papers/moi-white-paper.pdf` should show the Content-Disposition header.
Once you confirm I will re-run the health script and close the notes.
```
