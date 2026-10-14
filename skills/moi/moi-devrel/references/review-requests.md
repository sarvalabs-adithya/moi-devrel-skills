# Review requests and replies to reviewers

Facts are as of 2026-10-02 (the date of the evidence), including pull request states, unless dated. Sources: the docs, standards and Drive research, `people-and-teams.md` and `repo-map.md` (in this folder). "Recorded" means a note shows it; "inferred" means the researcher's reading. `ASK:`, `$SKILLS` and "the operator" are defined in `../SKILL.md`. Drafts are in `../templates/messages.md`; the shapes are in `house-style.md` section 4. Back to `../SKILL.md`.

## Who reviews what (recorded)
| Reviewer | Reviews | Seen |
|---|---|---|
| Rahul | Public pieces: decks, blog posts, docs scope. The whole standards package before anything is filed upstream (agreed 2026-09-09). Title not recorded | Changes requested on moidocs #124, 2026-09-17 |
| Gokul | Code. "Every code change goes through Gokul's review" (the x402 package). SDK, Voyage and docs PRs | Review requested on moidocs #124 (merged 13 October 2026), js-moi-sdk #150 (merged 14 October by Gokul, live) and voyage #447 (merged 14 October by Gokul, not live) |
| Robert Špendl | Coco and its docs | Approved coco-docs #12 on 2026-09-29 |
| Vinay | js-moi-sdk and Voyage pull requests (`people-and-teams.md`) | not seen |
Who has merge rights and who must approve each repo is not recorded. ASK: Rahul.

## Asking for a review
Draft 9 of `../templates/messages.md`. Parts, in order:
1. What it is, in one line, and what changes for a reader.
2. Where: a fresh link to the PR, the preview, the Drive document or the file. Say when a link expires: website PR previews are deleted after 7 days (as of 2026-10-02). Drive copies are snapshots. The 2026-09-09 set carried counts and versions that the package had moved past by 2026-10-02: regenerate and recount before every share.
3. What you want from them, as one thing: approve, decide named points, or check named points. Ask them to name the version they read. It is not recorded which generation of the review package Rahul read.
4. What you checked, and what you did not. Use the `moi-devrel/claim-check` hand-back lines if a ledger exists (counts, open rows), and say what was built, linted or read live.
5. By when.
When two reviewers are on one PR, say what each is asked. A PR body in a public repository is public text: name the reviewer in the request, not in the body (`house-style.md`: no reviewer names in public copy).
Batching: on 2026-09-15, while the previous operator walked through the moi-project audit pull requests and asked for tweaks, the rule set was one batch branch and one pull request at the end, not one per tweak. Applying that to tweaks a teammate sends is an extension of the rule, not a recorded one. `moi-devrel/ship` owns the mechanics.
Gates: requesting a review on a PR notifies a teammate, and sharing a Drive document leaves the machine. Both need the operator's yes. On audit, inventory and handover work no PR, comment or review request is made (2026-09-28).

## Replying to a change request
1. Read the comment itself on the PR. Copy it exactly. If it was given on a call, quote the speaker and do not summarise. Mark names and figures from a transcript "check" (`../SKILL.md`, "Facts that fail silently" 4).
2. Decide each item: do it, do it differently, or disagree (section below). Do not decide for the reviewer which items matter.
3. Make the change on the working set. Verify it: build, links, and `moi-devrel/claim-check` if a fact moved. Search every other copy of the text for the same family of mistake. A claim proved false on 2026-08-07 survived in five more files and in the speaker notes of the presented deck.
4. Check the PR description still matches the branch before you ask again. Three PR bodies were stale on 2026-10-02.
5. Draft the reply (draft 10 of `../templates/messages.md`): the quoted request, then under it what changed and where, what was not changed and why, and what is not verified. Read the commit from the branch on the day you send, because a rebase changes commit ids.
6. GATE: the operator posts the reply and re-requests review. Say in the hand-back who you are now waiting on and since when.
The incident (recorded, as of 2026-10-02): on 2026-09-17 Rahul asked that Launchpad content come out of the protocol docs PR (moidocs #124), because Launchpad is an app that uses MOI and application docs belong with the app. Commit 75f608b met it. The PR showed no reply and no re-review, and Gokul's review was requested and not yet done. The website PR #57 must merge after #124, because the site links to a file #124 creates. The change was done and nothing recorded tells the reviewer so.
Authors may use AI, and Rahul said on 2026-09-17 that they should know whether the result is right. The operator reads the reply once and can defend every line before it is posted.

## When you disagree
Say it once, in the same thread. Name the standard you followed and where it came from: who gave it, when, in which message. Offer both versions if wording is the dispute, and ask the person who decides (draft 11).
The incident (recorded): on 2026-09-10 a team reviewer replied to the release announcements that the message had gone straight onto the team's socials, asked for it to be rephrased so that it says a new version will launch at a stated time and that developers may need to upgrade, and asked for messages suited to the medium. The previous operator answered that he had followed the exact standard he was given. The reviewer is not named in the research (inferred to be Rahul or another senior reviewer), the standard's source is not recorded, and the dispute is unresolved. Until Rahul gives one written example, show the verbatim version and a channel-native rewrite and let the operator choose (`house-style.md`). Inferred lesson: keep the instruction in writing so the reply can cite it. ASK: Rahul who decides announcement format.

## When the operator is the reviewer
The format the previous operator used for a colleague's pull request (moidocs #120, 2026-08-21) was: "Issue N: what the issue is, why it is an issue, where it is, suggested fix."
1. Check each claim against source one by one (`moi-devrel/claim-check`; `moi-docs` for docs pages). Build a per-file table: claim, result, evidence with file and line.
2. Reconcile the counts before reporting. The headline said 27 errors, the table held 26 and the list 25.
3. Send the critical issues first. The plan on 2026-08-21 was eight critical issues first and the next sixteen after review.
4. Walk the operator through the findings one at a time, asking for each whether it could be correct. Give a typo that looks like a bug a plain before and after, without paragraphs.
5. Deliver a markdown file. The operator posts it. Claude posts nothing (draft 16 is one issue).
Address the text and its evidence, not the author. The author of #120 is Abhinav Agarwalla.

## Upstream reviewers
Messages and comments on a CASA or x402 pull request are public. No skill covers them since 14 October 2026, and the AI-disclosure question is open (ASK: Rahul). Who answers upstream comments is not recorded. ASK: Rahul.

## Not yet known
- Merge rights and required approvals per repo. ASK: Rahul.
- The form of Rahul's clearance on the standards package and what else he approves formally. ASK: Rahul.
- How fast reviewers answer. moidocs #124 merged on 13 October 2026; the answer to Rahul's change request is still not recorded. ASK: Gokul.
- The standard behind the 2026-09-10 announcement dispute: not recorded (the previous DevRel's notes); ASK: Rahul.
