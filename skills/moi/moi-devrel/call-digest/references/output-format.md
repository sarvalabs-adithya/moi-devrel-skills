# Output format: the digest, brief first

Facts are as of 2026-10-03. The template to copy is `../templates/digest.md`. The method that fills it is `method.md`. Back to `../GUIDE.md`.

## Rules of shape
1. Brief first. Answer first, then bullets. The Brief fits on one screen and says what was decided, what the operator owes, what they wait on, what needs their decision, and what is unclear.
2. Decisions come before tasks, tasks before open questions, and "Needs your decision" sits right after the work, not at the end.
3. One claim per line. A line has an ID (D1, W1, Q1, N1), so the operator can answer "change W3".
4. Every decision and task carries its source: the line number in the clean copy and the timecode. A re-export changes line numbers, so the timecode stays.
5. A quote is the speaker's exact words in quotation marks, with the label as the file wrote it, the timecode and the line. Keep each to a sentence or two. A flagged word is followed by the check in brackets (`method.md` section 3).
6. A date is a calendar date or `no date given`. A time is a date, 24-hour UTC and IST. A person is a name or `unlabelled`. Nothing is left blank.
7. No secret, no recovery word, no email or phone number, no student name that the work does not need. Say where something was and that it was masked.
8. The digest says which document it came from, so a review is never mistaken for a transcript.
9. Plain words and full sentences. No em dashes. Do not paste the transcript into the digest.
10. The digest lives in `call-digest-<YYYY-MM-DD>-<slug>/digest.md`, in the self-ignoring folder from step 1 of the run. It is never committed. The operator decides who sees it.

## The sections
| # | Section | What goes in it |
|---|---|---|
| 0 | Header | Call title and date. Source tool and file. Start time and zone. Read to timecode. Who was on the call and how each was identified. Whether the operator spoke and which label is theirs. Status DRAFT until the operator has read section 4 |
| 1 | Brief | At most eight lines. Counts and the single most important item of each kind |
| 2 | Decisions | ID, decision, status (decided, proposed, deferred), who said it, source, the reason in their words if they gave one |
| 3 | Work owed | ID, task (one verb, one object), owner, date, direction (owed by you, waiting on, unassigned), source, check |
| 4 | Needs your decision | The decision, options, recommendation and consequence (`method.md` section 10) |
| 5 | Open questions | ID, question, who can answer, source |
| 6 | In their words | Quotes the operator asked for, and every contested point. Use it for "what did X say" |
| 7 | Names and figures to check | As heard, read as, checked against, result |
| 8 | Not captured and privacy | Unlabelled speakers, a cut-off file, screen shares, the chat file, anything masked and what the operator must do |

Sections 2 to 5 may be empty. Write `none` in an empty section so the reader knows it was looked at.

## Answering "what did X say?"
Skip the full digest. Reply with: the source document in one line, then a numbered list of the points in the order said, each with its exact words, label, timecode and line. Add "not a decision" or "decision" to each point only when the transcript shows which. Offer the digest after. The previous operator asked for this form: "all of Rahul's feedback exactly".

## A short digest for a standup or a notes document
Gemini notes of a standup carry Summary, Decisions and Next steps already. Do not re-summarise them. Check each of its items against the transcript, then write sections 2, 3 and 5 only, and mark each item `in the notes and in the transcript` or `auto summary only`. Gemini assigns next steps by name, so each owner is a guess until you find the words.

## Worked example
Built from the recorded outcome of the 2026-09-14 call that reviewed the first CAIP namespace draft (a note kept on the previous operator's machine, not on GitHub and not available after the handover; the wording rules it produced are in `moi-devrel/references/terminology.md`). The transcript was not read for this example, so there are no line numbers, timecodes or quotes, and the speaker is named only as the notes name him: "the founder". Real digests carry all three. In the example "you" is the previous operator, who owned the follow-up.
```
# Call digest: review of the CAIP namespace draft, 2026-09-14
Source: a call transcript; the tool is not recorded. Example only: no line numbers.

## Brief
- Decided: three corrections to how the draft describes MOI.
- You owe: a revision of the draft with the corrected wording.
- Waiting on others: an endpoint that returns the network ID, promised the same day.
- Needs your decision: none recorded.
- Unclear: whether Sarva Labs "operates" the public networks.
- Check before you act: the company name, written "Serval Labs" in the transcript.

## 2. Decisions
D1 decided: MOI is described as participant-centric (wording owned by `moi-devrel/references/terminology.md`, table A).
D2 decided: write "designed and developed by Sarva Labs, governed by MOI Foundation".
D3 decided: say "network ID", not "chain ID" (`terminology.md`, table A).

## 3. Work owed
W1 Revise the draft to D1 to D3. Owner: the previous operator. Date: no date given. Direction: owed by you.
   Evidence: a revision of the draft dated 2026-09-14 exists in Drive.
W2 Expose the network ID by RPC. Owner: not recorded. Date: 2026-09-14 (same day, per the note). Direction: waiting on others.
   Status 2026-10-03: net.NetworkID returned error -32601 (method does not exist) on the devnet RPC. ASK: Gokul.

## 5. Open questions
Q1 Does Sarva Labs operate the public networks? The 2026-09-14 draft flags it to be confirmed. ASK: Rahul.

## 7. Names and figures to check
N1 "Serval Labs" read as Sarva Labs (GitHub org sarvalabs, site sarva.ai). Checked against terminology.md.
```
Why this example is good: every decision has a status, a promise made on the call is tracked as work the operator waits on, the later state of that promise is dated, and the one unsettled point is an open question with a named person.

## Not yet known
- Where digests are filed once the operator accepts them. Nothing in the record says. Keep them in the self-ignoring folder until Rahul says otherwise (ASK: Rahul).
- Whether a digest is shared with the call's attendees as a follow-up. That is a message and needs the operator's yes (draft it with `moi-devrel/templates/messages.md`).
