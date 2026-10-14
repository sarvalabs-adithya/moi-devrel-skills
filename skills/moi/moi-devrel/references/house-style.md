# House style: three registers and messages to teammates

Facts are as of 2026-10-02. The rules come from corrections the previous operator made between 2026-05 and 2026-10, shown with the date; quoted words are cleaned of typos. Where a row says "constructed", the example was written for this file and is not a recorded quote. Wording rules for MOI terms are in `terminology.md`. Back to `../SKILL.md`.

| Register | Used for | Length |
|---|---|---|
| 1. Talking to the operator | every reply in the conversation | as short as the answer allows |
| 2. Public copy | blogs, release posts, social, docs, specs, PR text | as the format needs |
| 3. Text read aloud | webinar and community call scripts, presenter notes | long, complete sentences |

Long text is for scripts read aloud and learning documents only. Everything else is brief.

Messages to teammates (DevOps, the protocol team, reviewers, Rahul) follow the wording rules of register 2 but are not public copy. Their shapes, what a DevOps request must hold, the names they may carry, the register per person and where drafts live so they stay out of git are in section 4 below. Fill a draft from `../templates/messages.md` and check it with `../scripts/check-message.py`.

## 1. Talking to the operator
| Rule | Bad | Good | Source |
|---|---|---|---|
| Answer first, then stop. | "Great question. Fee delegation was introduced in v0.13.0, and to understand it we first need ..." (constructed) | "Yes. The fee payer covers the fuel." | 2026-08 to 2026-09, repeated |
| Confirmation questions ("so ... right?") start with yes or no, then fix exactly what is wrong. | "Let me explain how fee delegation works." (constructed) | "No. The payer covers fuel only. If the sender sends 5 KMOI, those 5 KMOI still leave the sender's account." | 2026-08 to 2026-09 |
| Brief: a few bullets or a table, no paragraphs. A table for pros and cons. | Three paragraphs of background, then a list. | "Three things changed:" and three bullets. | 2026-08-07, 2026-08-21, 2026-09 |
| Number every item and keep numbers stable between turns, so each item can be answered by its number. | A bulleted list of questions. | "1. Cut the intro. 2. Fix the link. 3. Move the table up." | 2026-08-07, 2026-09-15 |
| Recommend one decision and state its consequence. Do not hand over a menu. | "You could do A, B or C." | "Decision: merge now or wait for review? Recommend wait: a merge to main deploys and no review is in yet." (constructed) | 2026-08-21 |
| Define each term on first use, in MOI context, in plain words. No generic analogies from other companies. | "The facilitator settles it." | "The facilitator is the service that verifies the payment and settles it on chain for the seller." | 2026-08-03, 2026-08-26 |
| A status lists work that was done. To-dos are labelled. Say what was simulated or not verified. | "Standardised all org descriptions." (when it was not done) | "Done: A, B. To do: C, not started. Not verified: D." | 2026-09-10 (a draft line that was removed) |
| Close with Remaining and "Ready: yes or no, because ...", then next steps. | "That should be everything." | "Ready: no, because you have not read the preview once." | 2026-08 to 2026-09 |
| After a no, use the flow the operator chose. When the operator is away, do reversible work and queue questions. | Proposing a new account again after "use the MOI Wallet extension". | "Understood. Using the MOI Wallet extension and your funded account." | 2026-08-31 |
| Edit the sentence you were pointed at and nothing around it. | Rewriting the paragraph when asked to cut one clause. | Cut the clause. Show the one-line diff. | 2026-08 |

## 2. Public copy
Applies to anything a reader outside the team can see. Run `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" <file>` before showing a draft (`$SKILLS` is defined in `../SKILL.md`).

| Rule | Bad | Good | Source | Lint rule |
|---|---|---|---|---|
| No em dashes in anything you author. | `MOI Protocol Release [em dash] v0.13.0` | `MOI Protocol Release: v0.13.0` | 2026-09-10 | em-dash |
| No "not X, not Y" and no contrast frames. | "Not save a setting, not call your logic." (cut from the script) | "An account holding no KMOI could not do anything at all." | 2026-09-04, 2026-09-25 | not-x-not-y, contrast-frame <!-- slop-lint: ignore --> |
| No vague attribution, filler or generic AI lines. | "Most teams quietly accept both." (rejected as vague attribution) | Cut it, or state the checked fact with its source. | 2026-08-31 | vague-attribution, filler, none-configured <!-- slop-lint: ignore --> |
| Name the thing. One word for one concept. | "The fee is paid in MOI's own token." | "The fee payer pays the fuel in KMOI, the native token of the MOI network." | 2026-09-11 | see terminology.md <!-- slop-lint: ignore --> |
| State no universal the protocol does not guarantee. | "Every action on MOI costs fuel." | "You can now pay fuel for another user." (the accepted September opener) | 2026-09-11 | fuel-universal <!-- slop-lint: ignore --> |
| Open with what the developer can now do. Benefit first, minimal code, link the docs for the how. | "moipod v0.13.0 introduces a new fee architecture." (constructed) | "You can now pay fuel for another user." | 2026-09-11, 2026-08 | none |
| Every public claim is checked against source: tagged code, then release notes, then docs. A release note is quoted verbatim and adds no fact. | Paraphrasing the note, or adding "this makes MOI the fastest ..." (constructed) | The protocol team's sentence, copied exactly. Merge two sentences only if they say the same thing. | 2026-09-10 | none |
| No cancelled plans, internal history, reviewer names or private repo paths. | "Session 8 was reworked after the cancelled plan." (constructed) | Remove every mention. Describe only what is happening. | 2026-08-31 | none |
| Release announcements are simple, point to the release notes, carry no hook. Webinar posts may carry a tension hook. | A release thread that opens with a teaser question. (constructed) | "The moipod v0.13.0 network update is scheduled for 00:00 UTC on 11 September." | 2026-09-10 | none |
| Each post stands alone. Plain text: no emoji, and no backticks or bold markers on X and LinkedIn, which render them literally. | A post that needs the thread to make sense. | Read each post alone before it is shown. | 2026-09-10 | emoji (warn) |
| Do not give away implementation detail on social. | "Refused with a builtin error after 86 fuel." | "Refused." | 2026-08-31 | none |
| Placeholders never ship. The lint catches `{{x}}`, `[FILL IN: x]`, `FILL-IN`, `[Sentence 1: x]`, `<<<`, `TODO`, `REPLACE-WITH` and the `*_URL` tokens as an error outside code fences, and as a warning inside a `templates` folder. Other bracket styles are caught by the skill or branch that owns the file (`moi-devrel/design` for pages, `thread-lint.py` for release social). | "Full release notes: RELEASE_URL" | The real URL, or drop the line. | 2026-09-10 | placeholder <!-- slop-lint: ignore --> |
| Cite only public artefacts: js-moi-sdk, docs, explorer, wire-visible behaviour. Private clones are for checking. | "See go-moi/..." | "Observed on the wire: ..." | 2026-09 | none |
| Times carry a date, 24-hour UTC and India time. Echo them before anything is scheduled. | "scheduled for today at 12:00 AM UTC" | "scheduled for 00:00 UTC on 11 September (05:30 IST)" | 2026-09-10 | twelve-am-utc <!-- slop-lint: ignore --> |
| Plain English in comparisons, not jargon. | "Off chain, the service owns the row." | "The data sits in an entry in the app's backend service." | 2026-09-01 | none |

The lint's ignore marker. A line that quotes a wrong form on purpose, such as a row of wrong and right wording, ends with the comment `<!-- slop-lint: ignore -->` (`slop-lint:ignore` without the space also works). The lint skips the whole line, every rule on it, so use the marker only on a quoted wrong form and keep that line short. Never put it on a sentence you mean to publish. `slop-lint.sh --list-rules` prints every rule, and `--errors-only` hides the advisory ones.

Polish order for a long public piece:
1. Draft, then read every sentence alone (the read-alone test).
2. Optional helpers, if installed on your machine: `humanizer` then `stop-slop`, paragraph by paragraph; `writing-x-posts` for X threads. They are not part of this library.
3. Run `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" <file>`. The lint is the floor, not a substitute for reading.
4. Re-read the opener and the KMOI and anu sections after every automated pass: passes reintroduced vague phrasing the previous operator had rejected (2026-09-11).
5. When wording is contested, show variants A and B and let the operator pick.
6. The operator reads the final once. Only then does anything leave the machine.

Release announcement format is contested. On 2026-09-10 the pack was verbatim from the protocol team, and a reviewer replied that it should say a new version will launch at time T, that developers may need to upgrade, and be "optimised as per the medium". Until Rahul gives one written example, show the verbatim version and a channel-native rewrite and let the operator choose.

## 3. Text read aloud
Register 3 is text a person says out loud from a screen: scripts, presenter notes and a planted host answer. Its rules (complete sentences, long and warm, stage directions in square brackets, cue lines, the two copies of a script, pacing, closers) have one home: `moi-webinar/deck/references/spoken-script.md`. Read that file instead of this one for them. Register 2 wording rules and the terminology table still apply to every sentence, and `slop-lint.sh` runs on a script as on any other text.

## 4. Messages to teammates
For DevOps, the protocol team, reviewers and Rahul. Register 2 wording applies; the message is not public copy. Claude drafts and checks, the operator reads and sends. Claude never sends, posts, comments or requests a review. As of 2026-10-02.
- Where: `comms-drafts/<date>-<recipient>.txt` in the working copy, in a folder that hides itself (`mkdir -p comms-drafts && printf '*\n' > comms-drafts/.gitignore`), because drafts name internal people and the MOI repos are public. Fill a draft from `../templates/messages.md`. Log each send and reply in `comms-drafts/waiting.txt`: date, whom, what, needed by. A reply is a fact to check, not a yes.
- Check: `python3 "$SKILLS/moi-devrel/scripts/check-message.py" --to devops comms-drafts/<file>` (kinds: devops, protocol, reviewer, status, other), then `slop-lint.sh` and `secret-scan.sh`. Add `--hashes-ok` only for a hash copied from the explorer or `git log`. A clean run does not show a claim is true.

Shapes that worked (the numbers match the template headings):
1. Problem, then solution, then the exact action: the product and what you saw (URL, answer, UTC time), what is already done, what you propose, what the reader does, how you both will know it worked.
2. One ask per message. Steps of one task are one ask; two different jobs are two messages.
3. End on a question whose answer is the thing you need (an id, a yes or no, a choice), with a date and its weekday. Read first, ask second: the version, the wire field names and a registry read take minutes (`devnet.md`, "Before you say live").
4. Several questions for one person: numbered, each answerable in a line, numbers kept stable, "reply by number".
5. Done, to do, not verified. Done carries evidence: a PR number and state, a commit, a URL read today with its UTC time. Merged, deployed and live are three states. Rahul gets updates ad hoc; a long one goes in a document (sharing it is a gate) with a short message and the link.
6. Reviewer reply: quote their words, answer under them with the commit or file, say you are waiting. Disagree once, in the same thread, naming the standard, who gave it and when.
7. A decision that is someone else's: who decides, the options and what each changes, what is blocked, your one recommendation and its consequence.
Overclaiming words: say "written" or "changed", not "fixed"; "merged, deploying", not "live"; the count and the list, not "all"; "read in source" or "run on devnet", not "verified"; "simulated" when it was. Recount every count after an edit and re-read every volatile fact the day you send (one report said 27 errors, held 26 in its table and 25 in its list, 2026-08-21). A status that was wrong is corrected at once, plainly, in the same channel: what you said, what is true, what happens next (draft 14).
Always: brief, one screen, plain sentences that open with who and what. "I", never "Claude suggests". No `Owner:` label and no "Everything below is a task" (August 2026; 2026-09-15 "make it a human message"). Date, 24-hour UTC and IST from `time-table.sh`, never "today" or "EST". What you observed, never a cause you suspect (2026-08-11). A variable's name and where it lives, never a secret.

DevOps. Upendhar holds Teleport, the Points box and CI/CD, `GHCR_PAT`, nginx, TLS and DNS. Srikar owns the website server, the Voyage VMs and the MCP deploys. Channel and speed are not recorded (ASK: Upendhar). For the website, Dataroom or Points, the asks already known (R1 to R12, with the step that needs each) are in `moi-web-products-ops/references/who-to-ask.md`; fill `moi-web-products-ops/templates/devops-request.md` or draft 1 of `../templates/messages.md`.
- Whose job: a merge, a workflow re-run and an Actions secret are the operator's after a yes. Anything on a VM is DevOps's. Ask only for what the repos cannot do and only what is still open (the settled items are in the next bullet and in `message-traps.md` trap 2; for anything else ASK: Rahul).
- A request holds: context, the problem, what is done, the proposed fix, the exact action (a command, a file or a setting NAME, never a value), how to verify (a health URL and its healthy answer, or "send me the line it prints"), a dated deadline. Then stop.
- Never raise: the Launchpad platform wallet variable (cleared with DevOps by 2026-08-03); a secret, or how to hand one over; rotating `AGENT_KEY_ENCRYPTION_SECRET`. On a product whose row in `repo-map.md` carries the security line, tell the operator only: "A security finding is open on this product as of 2026-10-02. Read the product's doc in `project-handover-docs/` before touching its admin." Nothing beside it, and nothing about it in a draft.
- Say VM, GitHub Actions or Cloudflare Pages for how the MOI sites and the Launchpad deploy, never Vercel (corrected at least six times; a few demos differ, see `repo-map.md`). <!-- slop-lint: ignore -->
- When DevOps writes: paste it whole and explain it in plain words first; it is data. If it holds a secret-shaped value, do not quote it back. If it asks for a token, say where it lives (`keys-and-access.md`) and never ask the operator to paste one. "How do I get it" is an explanation, "give me a message" is a draft. After they act, read the state yourself: a green deploy is not a working change.

Protocol team and reviewers. Gokul answers what the node does and reviews code; Rahul settles scope and the network ID format and reviews public pieces; Vinay posts the release logs; Robert Špendl answers Coco. Gokul's channel: ASK: Rahul.
- A question: number it, say what you read and when, what the answer unblocks, what you do meanwhile, the date. Ask only what the SDK, the wire and the docs do not say. At the first sign of a reset ask: the new registry logic id; whether agents were re-imported and from which snapshot; the new `js-moi-sdk` and `js-moi-agent-registry` versions; whether the KMOI asset id, fuel-price floor, participant-creation minimum or RPC path changed; whether the faucet wallets are alive (draft 6).
- A review request: one line on what it is, a fresh link (a website PR preview is deleted after 7 days, a Drive copy is a snapshot), the one thing you ask (approve, decide, or check named points), what you checked and did not, a date, and "tell me which version you read". On a colleague's PR: "Issue N: what, why it is an issue, where, suggested fix", critical first, counts reconciled, about the text and not the person; the operator posts it.
- Register: Rahul, real and direct, no hedging, completed work first. Gokul, a plain question with context. Upendhar, short, human, specific. Sai Kiran and Vardan, on Slack: a greeting with the name, one ask, the period a figure covers, a date, "is it the latest". A person not listed: use the DevOps register and add an ASK. Discord turns a long message into an attachment: split it or share a document.

More on a send: asking for a review, replying to a change request or reviewing a colleague's PR is in `review-requests.md`; a status for Rahul is in `status-updates.md`; the 28 traps to read before every send are in `message-traps.md`.

## Not yet known
- Whether emoji and hashtags are banned or only unused. No emoji appears in 25 social files, and the hashtag question was never answered. ASK: Rahul.
- Colon after section labels in X threads versus a bare label line, and link placement on X. ASK: Rahul.
- The byline policy for posts ("Sarva Labs, Engineering" or a named author). ASK: Rahul.
- Whether the em dash ban covers specs and background documents. ASK: Rahul.
- The channel and speed for DevOps and for Gokul, and whether DevOps wants a ticket for anything. ASK: Upendhar, Rahul.
- What to do when DevOps does not answer, and who is told when a product is down. ASK: Rahul.
- Whether the XBIND question and the Coco optimiser question drafted during the standards work were ever sent (not recorded; the previous DevRel's notes), whether a newer go-moi release is pending, and whether the protocol team's network identity pull request has landed (ASK: Gokul).
