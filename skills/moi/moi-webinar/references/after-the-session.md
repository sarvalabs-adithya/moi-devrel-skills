# After the session: the write-up, the bounty and the proof forms

Facts are as of 2026-10-02. The write-up and everything about announcing it are `moi-blog`'s. This file says what the session folder hands over, what the bounty and the proof-of-completion forms looked like, and what is not settled. Sending a message, uploading a file, publishing, creating a form or pushing the folder all need the operator's explicit yes. Back to `../SKILL.md`.

## The write-up

A target in session 7's post file: publish within 48 hours of the session. The 4 Aug 2026 call asked for a post for every dev talk. Session 8's post was written before the event, dated 4 Sep, and as of 2026-10-02 is not published (`session-history.md`). A post with session 7's slug is live (read on 2026-10-02). Write it with `moi-blog` (house style, the publish pull request, the announcement). Hand it from this folder:

- `README.md` and `NOTES.md`, with every interaction hash in full and the node version of each run.
- The demo output, copied from a real run. A draft written before the session (session 8's first design and session 9's) keeps `<<< EVIDENCE >>>` placeholders and a "write after the session" FAQ; fill them from the questions actually asked. <!-- slop-lint:ignore -->
- The previous session's post, to link. Each post links the one before it and the earlier session folders.
- The reviewer's framing, if one was given, as a note for the writer.

What the session posts had in common (observed; `moi-blog/references/authoring.md` decides the house style): an answer-first "what is X" block with one proof sentence from a real run; the problem; a numbered walk-through with evidence blocks; an "honest part" saying what is self-imposed, not live or unsolved; a table against other chains (session 8 only); every tool linked; a one-line design rule; a FAQ of seven or eight questions.

### Gates before it publishes

1. **Claim check.** Run it through `moi-devrel/claim-check`. Session 7's fact check found "only the owner can move funds" false, because MAS0 has `Approve`, `TransferFrom`, `Lockup` and `Release`. The post was rewritten to "value moves only under the holder's own signature, and our agents never grant one", and the old claim survived in five other documents and the deck notes. After any correction, search every document and the deck notes.
2. **Placeholders.** Search the post and the session documents for `<<<`, `REPLACE-WITH`, `CANONICAL_URL`, `LUMA_URL`, `EVENT_URL` and `FILL`. A publish with one in it is a defect. `session-preflight.sh` counts them in the session documents, and `moi-blog`'s `post-lint.py` checks the post itself. <!-- slop-lint:ignore -->
3. **Numbers recounted** after any code change (line counts, forgeries, hashes).
4. **No cancelled plan, no reviewer name.** Session 9's draft links a post for a session that was not delivered.
5. **Hashes.** The previous operator asked for each hash to link to the explorer. The committed session 8 post file has plain code-fenced hashes. The explorer's URL pattern is not on record (`demo-standard.md`).
6. **The home of the post.** Session 7's plan on 8 Aug 2026 was a text-only Medium story first (`blog-assets/PUBLISH.md` on the branch), and whether that story went live is not recorded. A Medium-first post becomes the canonical copy, and a later site version arrives as the duplicate unless Medium's canonical link is pointed at the site (story settings, advanced). A post under the slug `how-ai-agents-pay-each-other-moi` is live on blog.moi.technology (read on 2026-10-02). Which copy is canonical is not recorded. ASK: Rahul.
7. **Frontmatter.** The session post files carry `description`, `authorRole` and `slug`, which the website build ignores (`moi-blog/scripts/post-lint.py`, as of 2026-10-02). `moi-blog` rewrites the frontmatter and runs that lint.

A rule from 24 Aug 2026 says publishing a post is not the end of the task: it also goes out across MOI's social accounts and to the mailing list. Whether that covers session write-ups is not stated, so ask. Announcing a post is `moi-blog`'s Distribute step: it has no undo and posts again on a rerun, so never run it twice.

## The social pack after the session

A post after the session links the write-up, never the event page. Session 7 had an X thread of nine, a LinkedIn post and a Reddit post, all linking the canonical copy. The social post is the hook and the crawler follows the link. Session 7's pack still led on a statistic the post had cut: re-read the pack against the final post. No after-session pack is on file for session 8.

## The recap and the filing

- **Recap to attendees.** The next steps recorded for session III: send attendees a summary with the repo and bounty links, add the submission form to the event page, and upload step-by-step instructions to the repo. Claude drafts, the operator sends.
- **Recording and deck PDF.** Session 8's `GAMEDAY.md` says to push them. A push to `moi-foundation/MOI-Webinars` publishes, because the repo is public. An upload to Drive is a share. Each needs a yes. Hand the recording to the editor (`recording.md`).
- **The session folder.** The plan on file is one branch per session and a pull request to `main` after the session. Sessions 8 and 9 sit on a branch that is 95 commits ahead of `main` as of 2026-10-02, shared with the x402 work. All 95 commits carry an AI co-author trailer, which house rule 4 forbids, and 3 of them are authored under an AI identity instead of the work identity (`git log`, read on 2026-10-02). The 2026-10-01 cleanup of trailers covered open pull requests only. Opening one from that branch would carry the trailers into `main`. Do not open it. ASK: Rahul how session folders should land, for example as a fresh branch from `main` under your work identity.

## The bounty

Each session set a task that reproduces the demo. Rewards are written in the session READMEs and slides. Who pays, who verifies and how a payment is recorded is not on record. ASK: Rahul.

| Session | The task, as written |
|---|---|
| 2 | Mint a MAS0 token and deploy a TaxToken. Submit both asset ids |
| 3 | Two tracks: register an agent through OpenClaw and submit the agent id, wallet and a transaction hash; and an open bounty for a useful on-chain agent, judged on Discord |
| 4 | Deploy two assets and complete the lockup and release swap. Submit asset ids and a swap hash |
| 5 | Build an NFT marketplace. Submit a repo link and a token id or hash |
| 6 | Provision an agent under the budget logic. Submit a repo link with the logic id, the agent address and the provision hash, plus the report output |
| 7 | Register both agents, get a quote, run the identity check, make a real transfer. A form with a wallet, an email and a repo link |
| 8 | A challenge on the Points app (a MOI product, `moi-devrel/references/repo-map.md`): submit interaction hashes that the server checks by reading the chain. The first spec asked for four hashes; the previous operator corrected it, and the final wording is not on record |

Session 8's bounty was not live on game day. It shipped behind a flag and needed a migration, `MOI_RPC_URL` in the deploy environment and the flag flipped. `sarvalabs/Points-Program` PR 1 is listed as open in the previous operator's `DEPENDENCIES.md` of 2026-10-01 (local only: ASK: Adithya for a copy). Announce an unfinished bounty as coming, never as open. The Sprint plan of January 2026 held that rewards should depend on verified on-chain activity, not on completion.

Before touching the Points admin, read its row in `moi-devrel/references/repo-map.md`.

## The proof-of-completion form

- **What it is.** A Google Form per session, in the previous operator's Drive root, named `MOI Builders <Roman numeral> - <Topic>`. It collects on-chain proof so a bounty can be checked. It is not a registration form (registration is on the event page), and no feedback form was found in the Drive.
- **Fields observed** (from the one readable response sheet and the session III recording): email, wallet address, and either asset ids, a transaction hash, or an agent id with the owner wallet. Form questions cannot be read through the Drive tool; the operator opens the form.
- **When created.** Session II about 3.5 days before; III about 75 minutes before the start; IV on 2026-07-03; VII on the day. Create it by the day of the event at the latest, and link it from the event page.
- **No master form was found.** Later forms were probably copies of an earlier one, renamed (inferred from timestamps). Three untitled forms exist, so a copy that was never renamed looks like a stray. ASK: Adithya which form to copy.
- **Responses.** Only session II has a response sheet in Drive. A form edited after launch gets a new response tab, so read both. The sheets hold other people's names, emails and wallets: copy none of it into notes, the repo or a chat. Read headers and counts.
- **Verify** every submission on chain, by hand with the explorer or the SDK, before any payout. "I'm going to verify each and every agent myself" (session III). No verifier script exists in this skill.

## Close the session folder

Update `README.md` and `NOTES.md` with what was presented and what changed on the day. Put the final status of the event page, the posts, the post and the bounty in the hand-back.

## Not yet known

- Reward amounts that are still current, who pays and who verifies. ASK: Rahul.
- Where responses for III, IV and VII go, and what each form asks. ASK: Adithya.
- Whether the Points challenge ever went live, and its final rules. ASK: Adithya.
- Whether any attendee data (count, questions) is kept. None is on record.
