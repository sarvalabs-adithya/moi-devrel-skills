# Incident note: <product>: <what broke>

Fill this while the problem is open and keep it with the hand-back. It is a local file: it names people and may name private repos, and two of the repos are public, so it stays out of git. Keep it outside the clone, or inside a self-ignoring folder: `mkdir -p web-ops-<slug> && printf '*\n' > web-ops-<slug>/.gitignore` (the `*` hides the folder, itself included, from `git add`). No secret, no key, no recovery phrase, no visitor email in it.

- First seen (UTC, with the date): <...>   Seen by: <name>   Reported through: <channel>
- Product and address: <website | Dataroom | Points> <host>
- Symptom in one sentence: <what a visitor or member sees>
- `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" <product>` at <UTC time>: the FAIL and WARN lines, copied: <...>
- KNOWN lines present (ids): <...>   New since the last note: <none | list>
- The data, not only the status: <for example `migrations.applied` 10 of 11; `embedding_status` of the document; the JSON of `/api/community-calls`>
- Last deploy run: <`gh run list` line: workflow, branch, conclusion, UTC time>
- Layer, by `references/<product>-health.md`: <web server or VM | app | database | build ahead of schema | configuration | content>
- Told: <name, channel, UTC time, which request R-number from `references/who-to-ask.md`>. Sent by the operator: <yes>
- Cause: <known, with the evidence | unknown, ASK: <person>>
- Fix applied: <what, by whom, UTC time, with the operator's yes quoted> or <none yet>
- Verified by: <the read that shows recovery, UTC time>
- Follow-up: <numbered, each with an owner and a date>
- Trap or runbook row to update: <file and row, if this was new>
