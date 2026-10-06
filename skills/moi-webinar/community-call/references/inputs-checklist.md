# Inputs checklist

Per segment: the artefact, who owns it, where it arrives, and what to ask for. Facts are as of 2026-10-02. Draft messages for each row are in `../templates/input-request-messages.md`. The human sends them. Back to `../GUIDE.md`.

## Timing
- Observed: CC14 inputs arrived one to two days before the call (first draft requested 23 September, the Scribble report, dashboard numbers and photos on 24 September, call on 25 September, inferred). CC13's deck was updated about five hours before the call.
- Suggested: ask as soon as the date is confirmed, about a week before, with inputs due three days before so the run-of-show can go out 48 hours before. The 48-hour target is from the January 2026 KRA document. No run-of-show document exists in Drive. ASK: Rahul whether one is still required. Do not wait for the answer: the starting skeleton table in `slide-plan.md` serves as the run-of-show until he says otherwise.
- Rehearsal the day before. Not confirmed for CC14. See `segments-and-roles.md`.
- The CC14 deck was reshaped as the inputs arrived. Late inputs are the main cost of this job.
- Reaching people: `moi-devrel/references/people-and-teams.md` has each channel (as of 2026-10-02: Vardan and Sai Kiran on Slack, Rahul on Discord). No response time is on record, so name the date you need an answer by in every message.

## Per segment
| Segment | Artefact | Owner | Where it arrives | What to ask for |
|---|---|---|---|---|
| Protocol | The month's release note, as sent | Protocol team. Gokul for chain facts. Vinay posts release logs | A Discord release log, or the call's manager (Rahul, inferred) pastes it. How it reaches DevRel is unknown. ASK: Rahul | The note verbatim and unedited. The release moment in UTC. SDK versions with any `-rc` suffix. Point releases and release candidates. Whether the network is on the release now |
| Protocol, source | The release post and tags | Protocol team, the blog | `blog/src/content/posts/` in `sarvalabs/MOI-Website`, tags in the repos | Only when the blog exists. See `release-slide-checks.md` |
| DevRel | The operator's own status | The operator | `DEPENDENCIES.md` (the previous operator's handover file, untracked on his machine as of 2026-10-02; ASK: Adithya for a copy), `moi-devrel/references/repo-map.md` | MCP server status, x402 status, blog posts of the month with URLs |
| Product | A product update, if the slot exists | Prateek was planned to give it at CC13 (ASK: Adithya whether he did). Owner now unknown | ASK: Rahul whether the slot exists | Name, one-line claim, a screenshot or demo. Plan no product slide until a named presenter confirms an artefact |
| AI visibility | The monthly Scribble report and dashboard screenshots | Scribble produces it. Sai Kiran passed it on for CC14 | Slack. ASK: Sai Kiran which channel | New figures with their date. The query list and whether it is still 47. The five engines by name. Coverage. The CC14 figures still unverified (see `../examples/cc14/numbers-ledger.csv`) |
| Community | Growth key pointers | Sai Kiran | Slack | Discord joins and active members with the period they cover. Game Night dates, run number and attendance. Pip status. Ask him to confirm they are the month's latest |
| Events and partnerships | Photos and event facts | Marketing. ASK: Sai Kiran who owns events and who holds the photos. The CC14 photos came from the previous operator | Slack attachments, the event's own site | Event name, dates, venue, what the team actually did there. Real photos with permission to show them. No guest names or outcomes without a source |
| Guest, if any | Confirmation, slide content | Whoever invited the guest. ASK: Vardan | Slack | Confirmation they will attend, name, title as the guest wants it written, portrait file, company logo file, topic |
| Host | Question list and clip plan | The host. ASK: Vardan who hosts | Slack, as a message to the operator | The planted question word for word, whether to expect it at a given slide, and the clip plan. See `host-qa-prep.md` |
| What is next | Next month's plans | Marketing for its half, the operator for DevRel | Slack | Items that are decided. Anything undecided stays off |
| Sign-off | Segment order, line-up, rehearsal day | The call's manager, taken to be Rahul (inferred; see `segments-and-roles.md`) | Discord or a call | A yes on the order |

## When an input arrives
1. Save attachments under `community-call-<N>/deck/assets/` with the names the slide will read. On the previous operator's Mac, tools could not read `~/Downloads` (27 August 2026; this may no longer apply). If a file will not open, ask the human to copy it into the call folder with `cp`. Downloading any file needs the human's yes.
2. Add every figure to the numbers ledger at once, with source, date and who supplied it. Never write a figure into a slide first.
3. If two sources disagree, use the later and more precise one, keep the other as a `superseded` row, and tell the human.
4. If a figure cannot be refreshed, ask for it by name. CC14 shipped three figures that were never reconfirmed because the request went unanswered.
5. Photos must be real files, and the human must have the right to show them. A slide may show an empty frame that reads its filename. It never shows a stand-in.
6. A name or title the supplier did not give is left off. Do not look one up and add it.

## The numbers ledger
One file per call, `community-call-<N>/numbers-ledger.csv`, copied from `../templates/numbers-ledger.csv`. One row per figure on a slide.

| Column | What goes in it |
|---|---|
| `slide` | The slide number. Several slides: `5;11`. A cut slide: `cut` |
| `figure` | What the number measures, in words |
| `value` | The figure written exactly as the slide prints it, for example "17.3%". A spelled form such as "17.3 percent" will not match |
| `source` | The document, screenshot or message it came from |
| `as_of` | The date the figure was true or supplied, as YYYY-MM-DD |
| `confirmed_by` | The person or source that confirmed it. For a row that is not confirmed, write why nobody has. For `accepted-unverified`, write who accepted it and when, for example "accepted by <name> on 2026-10-22: <reason>" |
| `status` | `confirmed`; `unverified` or `pending` (not confirmed until settled); `accepted-unverified` (the human decided to keep a figure nobody verified); `superseded` (replaced by a later figure); `dropped` (its slide was cut). The last two retire a figure |

Quote any cell that contains a comma. A row with more cells than the header stops the checker with exit 2.

`accepted-unverified` is the only way to keep an unverified figure on a slide and still get a clean check. The checker treats it as a WARN, not a FAIL, and requires `confirmed_by` to read "accepted by <name> on <YYYY-MM-DD>: <reason>". Only the human can accept a figure. Claude never sets this status on its own. Every accepted row goes in the hand-back, and the call is "ready: yes" only with those rows named.

Command, from the working copy with `SKILLS` set:
`python3 "$SKILLS/moi-webinar/community-call/scripts/ledger-check.py" community-call-<N>/deck/index.html community-call-<N>/numbers-ledger.csv --notes`

It lists figures on slides with no row, rows not confirmed, retired figures still showing, and confirmed rows with no source, then the accepted rows as warnings. It detects numbers with digits, versions, hex ids and the words thousand, million and billion. Other spelled-out numbers ("seventh") are invisible to it, so add those rows by hand. The filled example is `../examples/cc14/numbers-ledger.csv`.

## Sources worth knowing
- Slack: where marketing inputs arrive. The workspace and channel names are not on record. ASK: Adithya which workspace and channel the CC14 inputs came in on, then ask Sai Kiran to confirm it is still the place, and write the answer into this file.
- Scribble report: location, login and how visibility is computed are unknown. ASK: Sai Kiran. As of 2026-09-24 CC14 was the baseline: 17.3 percent visibility, 1,203 citations, 650 mentions. Those three are confirmed in the CC14 ledger. The 47 queries, five engines and 221 of 226 coverage are not.
- Drive: the `Community Call` folder holds one subfolder per call, with the deck PDF and recap videos. Most call artefacts are owned by shared accounts, so search shared files too. Uploading to it needs the human's yes.
- Month-to-month comparison: slide 5 of CC14 says "the baseline we measure every month from here" and slide 11 says "Track the same 47 queries every month". A CC15 visibility slide therefore needs both months' figures, each with a date, and the same query set. ASK: Sai Kiran whether the set changed.

## Not yet known
- The Slack channel names and whether one channel holds all inputs. ASK: Adithya, then Sai Kiran.
- Whether a protocol contact besides Gokul confirms release status before each call. ASK: Rahul.
- Who writes the host's questions. ASK: the host.
