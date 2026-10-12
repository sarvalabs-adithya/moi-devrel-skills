# Call digest: <call title>, <YYYY-MM-DD>

Copy this file with `cp "$SKILLS/moi-devrel/call-digest/templates/digest.md" "$D/digest.md"` (`$D` is the folder from step 1 of the run) and fill it in. Delete every instruction line (the ones in italics). Write `none` in a section that has nothing. The folder is self-ignoring and nothing in it is committed. Shape rules: `references/output-format.md`. Method: `references/method.md`.

Source: <tool and file name>. Call date and start: <YYYY-MM-DD HH:MM> <area/city zone>. Read to timecode <H:MM:SS> of <N> lines. Clean copy: <file name>, made by `transcript-prep.py`.
On the call: <name: how identified (told by the operator, addressed by name, inferred from ...)>; <...>. Unlabelled: <labels you could not map>.
The operator: <was or was not on the call>. Their label: <Speaker N or name>.
Status: DRAFT until the operator has read section 4.

## 1. Brief
*At most eight lines. Counts, and the most important item of each kind.*
- Decided: <N. The one that matters most>
- You owe: <N. The first due, with its date or "no date given">
- Waiting on others: <N. Who, for what>
- Needs your decision: <N>
- Unclear: <the one thing the call left open>
- Check before you act: <N names and figures still marked check>

## 2. Decisions
*Status is decided, proposed or deferred (`method.md` section 2). Quote the speaker for each.*
| ID | Decision | Status | Who | Source (line, timecode) | Reason in their words |
|---|---|---|---|---|---|
| D1 | <what was chosen> | <decided> | <name or unlabelled> | <line 120, 0:12:03> | "<exact words>" |

## 3. Work owed
*One verb and one object per task. Direction is owed by you, waiting on, or unassigned. The date is a calendar date or `no date given`.*
| ID | Task | Owner | Date | Direction | Source (line, timecode) | Check |
|---|---|---|---|---|---|---|
| W1 | <verb and object> | <name or unlabelled> | <YYYY-MM-DD ("their words") or no date given> | <owed by you> | <line 130, 0:13:10> | <what to verify, or none> |

## 4. Needs your decision
*State the decision itself, not that one exists.*
N1. Decide: <the question, answerable yes or no>.
Options: A <...>. B <...>.
Recommendation: <A or B>, because <one reason from the transcript>.
Consequence: A <...>. B <...>.

## 5. Open questions
| ID | Question | Who can answer | Source (line, timecode) |
|---|---|---|---|
| Q1 | <asked and not answered, a disagreement, a figure given twice> | <name, or ASK: person> | <line 200, 0:20:00> |

## 6. In their words
*Only what was asked for or is contested. Exact words, as the clean copy has them. Add the check in brackets where a word looks mis-heard.*
1. <Speaker label as written> (<inferred: name>), <timecode>, line <n>: "<exact words>"

## 7. Names and figures to check
*Everything from auto-notes starts here. Remove a row only when its source is named.*
| ID | As heard | Read as | Checked against | Result |
|---|---|---|---|---|
| C1 | <"Server Labs"> | <Sarva Labs> | <terminology.md> | <confirmed or open> |

## 8. Not captured and privacy
- Unlabelled speakers: <which, and the lines>
- Parts not in the transcript: <screen shares, chat file, a cut-off file, audio only>
- Masked by the script: <rule names and line numbers from the report, or "nothing found; not proof">
- Told to the operator: <what, and when>
- Internal only: <lines that name a reviewer or an internal verdict and must not reach public text>
