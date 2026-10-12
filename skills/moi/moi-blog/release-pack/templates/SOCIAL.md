# Release pack plan and record: moipod v{{version}}

Status as of {{date}}. This file records decisions and what was sent. It holds no copy of any post. Each text lives once, in `social/`, so the record cannot drift from the files. The process is `moi-blog/release-pack/GUIDE.md`.

## The note
| Field | Value |
|---|---|
| Received from | {{person at the protocol team}} |
| Channel and time received (UTC) | {{channel, date, HH:MM}} |
| Pasted into RELEASE-NOTE.md by | {{operator}} on {{date}} |
| SHA-256 of RELEASE-NOTE.md | {{output of shasum -a 256, taken when the note was pasted}} |
| Release moment, in the protocol team's words | {{exact words, for example "scheduled for today at 12:00 AM UTC"}} <!-- slop-lint:ignore --> |
| Release moment as date and UTC | {{day month year, HH:MM UTC}}, confirmed in writing by {{person}} on {{date}} |
| India time | {{HH:MM IST}} from `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "<YYYY-MM-DD HH:MM>" UTC` |

## Answers from the protocol team
| Question | Answer | From, date |
|---|---|---|
| Does the upgrade wipe devnet? If so, which registry id replaces the old one, and when? | {{answer}} | {{person, date}} |
| Do KMOI's asset id, the fuel-price floor, the participant-creation minimum or the RPC path change? | {{answer}} | {{person, date}} |
| What should "full release notes" link to? | {{URL or "no link"}} | {{person, date}} |
| Who confirms "live" once the upgrade has run? | {{person}} | {{person, date}} |
| Which call returns the network ID? | {{answer}} | {{person, date}} |

## Decisions
| Question | Decision | Decided by, date |
|---|---|---|
| Verbatim (thread, linkedin.txt) or channel-native (x.txt, linkedin.native.txt, discord.txt) | {{A or B}} | {{operator, date}} |
| Channels | {{X, LinkedIn, Discord; Telegram only if Rahul says so}} | {{operator, date}} |
| Draft in Buffer, or schedule at an exact time | {{draft or scheduled, and why}} | {{operator, date}} |
| Discord channel to post in | {{the channel Rahul names}} | {{Rahul, date}} |

## Differences from the note
List every place the pack text differs from `RELEASE-NOTE.md`, even a merged sentence or a replaced dash.
| Where | The note says | The pack says | Why |
|---|---|---|---|
| {{file:line}} | {{words}} | {{words}} | {{reason}} |

## Channels
Status is one of: not sent, drafted, scheduled, sent by hand. After each action, open the live post and read it, then fill the proof column.
| Channel | File | Tool | Fate | Time (UTC, IST) | Status | Proof (Buffer id or post link) | Done by, date |
|---|---|---|---|---|---|---|---|
| X thread | `social/thread/` | `scripts/buffer.mjs --thread-dir` | {{draft or scheduled}} | {{time}} | not sent | | |
| LinkedIn | `social/{{file}}` | `scripts/buffer.mjs --file` | {{draft or scheduled}} | {{time}} | not sent | | |
| Discord | `social/discord.txt` | by hand | sent by hand | {{time}} | not sent | | |

## Checks, with the date each was run
The commands are in step 6 of `moi-blog/release-pack/GUIDE.md`.
- [ ] `thread-lint.py` on `social/`, exit 0: {{date}}
- [ ] `slop-lint.sh` on every shipped text, 0 errors: {{date}}
- [ ] `secret-scan.sh` on this folder: {{date}}
- [ ] `ledger-status.py` on `ledger.csv`, exit 0: {{date}}
- [ ] Devnet read before any "live" word: version, network ID, wire field name: {{date}}
- [ ] The operator read the final text of every post once: {{date}}

## Corrections
Keep the wrong text here with its date. Do not rewrite history in the files above.
| Date | What was wrong | Where it was posted | What was done |
|---|---|---|---|
| {{date}} | {{statement}} | {{channel}} | {{action}} |
