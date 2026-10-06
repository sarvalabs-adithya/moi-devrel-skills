# Pre-event social: the campaign shape and timing

Facts are as of 2026-10-02. Posts that drive registrations to the event page, on X and LinkedIn, drafted before the session. How Buffer, drafts, schedules and channels work is `moi-blog`'s: read `moi-blog/references/buffer.md`, and do not restate it here. This file holds the shape of a session's campaign and its copy rules. Nothing is scheduled, saved as a draft or posted without the operator's explicit yes for that post (`moi-devrel/references/consent-and-identity.md`, section 1). Back to `../SKILL.md`.

## What session 8 did (observed from file names and file times)

All copy lived in `SOCIAL.md` (a first pack) and then in one file per post under `social/` (local only: it exists only on the previous operator's machine, ASK: Adithya for a copy). Whether every file went out as scheduled is not recorded: on 3 Sep `GAMEDAY.md` still said "Nothing is scheduled".

| Day | Files | Note |
|---|---|---|
| Mon 31 Aug | `x.txt`, `linkedin.txt`, with `x-reply.txt` and `linkedin-comment.txt` carrying the link | The announcement pair, drafted 08:16 to 08:45 |
| Tue, Wed, Thu | `tue-*`, `wed-*`, `thu-*`, one X and one LinkedIn each | Drafted 31 Aug (`tue-linkedin.txt` was edited on 1 Sep). Thursday's X post says "Tomorrow" and "Last call". An alternate announcement, `x-alt.txt`, is also there |
| Tue 1 Sep | `mon-x.txt`, `mon-linkedin.txt`, with reply and comment files | A second pair about the "why". The `mon-` prefix does not mean Monday |
| Fri 4 Sep | `fri-linkedin-t5h.txt`, `fri-x.txt`, `fri-linkedin-t1h.txt`, `fri-x-t30.txt`, `fri-x-live.txt`, `fri-linkedin-live.txt`, plus `fri-x-reply.txt` and `fri-x-narrative.txt` | Five hours out, one hour out, 30 minutes out ("WE'RE LIVE IN 30."), live. The last two files are an X reply and a second X version of the day's post |

Times mentioned for scheduling: 5:30 pm IST on 1 Sep, 11:00 IST and 15:30 IST on 4 Sep. The same folder holds two unrelated posts about the Voyage login move (`voyage-x.txt`, `voyage-linkedin.txt`): ignore them for this session.

## The shape to follow (library default, inferred from session 8)

`../templates/SOCIAL.md` has the schedule table. In short: an announcement pair on the day the topic locks, one pair a day until the day before, then posts at four moments on the day (5 hours out, 1 hour out, 30 minutes out, live). Every post before the session links the event page. Every post after links the write-up (`after-the-session.md`).

## Copy rules

1. **Hook first, then the tension, then the point.** A tension hook is welcome on a webinar post. A release announcement is different: no hook (`moi-devrel/references/house-style.md`).
2. **Plain text.** No emoji, no em dashes, no backticks or bold on X and LinkedIn. All 25 session 8 post files have no emoji and no em dash. Session 7's pack still had both, so the rule tightened after it.
3. **Each post stands alone.** Read each one by itself before it is shown to the operator.
4. **Do not give away implementation detail in the announcement and the day-of posts.** On 31 Aug 2026 the first LinkedIn draft was cut as too long, and the error text and fuel figure were removed. The Tuesday pair does quote the error string, so this is a preference for the first announcement and the day-of posts, not a ban (whether that pair was approved is unknown).
5. **Name what is not live.** The LinkedIn post carries the storage-only caveat and the pack's notes say not to cut it.
6. **Cut vague attribution.** "Most teams quietly accept both" was removed on 31 Aug 2026 because it cannot be cited. A drafted line quoting a fuel figure was removed on 4 Sep. <!-- slop-lint:ignore -->
7. **Do not reference the dropped design,** and name no reviewer. The first pack's framing about a budget contract was replaced for that reason (`../examples/session-8/README.md`).
8. **Where the link goes.** The first design put the link in an X reply and a LinkedIn first comment. A later instruction (4 Sep) put the LinkedIn link in the post body. Use the body for LinkedIn and a reply or a thread's second post for X. Link placement on X has no recorded decision. ASK: Rahul.
9. **Every factual line is a claim** for the ledger (`moi-devrel/claim-check`) and is checked against `NOTES.md`.
10. **Run the lint** on every file: `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" session-<N>/SOCIAL.md session-<N>/social/*.txt`. Leave the glob out until `social/` holds a `.txt` file, because zsh stops with "no matches found".

## Variants

For a post that matters, write variants and let the operator pick: A (stop-slop only), B (humanizer only), C (both), in `social/variants/`. The previous operator picked A for session 8. Both helpers are optional and are not part of this library. When wording is contested, show A and B and let the operator choose.

## Tools in the session folder

`scripts/buffer.mjs` in `moi-foundation/MOI-Webinars` is on the branch, not on main as of 2026-10-02. Its surface: `channels`, then `post --file <path> --channel <id> [--at <iso8601>] [--draft] [--confirm] [--follow <file>]`. Without `--confirm` it prints what it would send and stops. Its `--thread-dir` option (an X thread from numbered files) is in a local commit that was never pushed. ASK: Adithya for a copy. Its key is `BUFFER_API_KEY` in a local `.env`. That is a different name from the website pipeline's `BUFFER_ACCESS_TOKEN`: the two do not share a variable. Run it from the repo root, because running it from inside a session folder failed on 31 Aug 2026. It cannot delete a post.

Which route a session's posts should take, this script or `moi-blog`'s, is not settled. ASK: Adithya, then Rahul.

## Incidents

- **2026-08-31.** A Buffer key was pasted into the chat and revoked. Never paste a key or recovery phrase into a chat. A rotated key appended below a dead one in `.env` works, because the last entry wins.
- **2026-09-10.** Two wrongly scheduled Buffer posts for a release were deleted by hand (`moi-devrel/references/terminology.md`, table C). Use `time-table.sh`, write a date, 24-hour UTC and IST, and echo it before scheduling. A `--at` value must end in `Z`. <!-- slop-lint:ignore -->
- A scheduled Buffer post publishes with nobody reviewing it. Use a draft unless an exact time matters.

## Not yet known

- Which session 8 posts went out, and when. ASK: Adithya.
- Whether hashtags are banned or only unused, and whether UTM tags apply to webinar posts. The session 8 files use bare event page links. ASK: Rahul.
- Who besides the operator approves a post.
