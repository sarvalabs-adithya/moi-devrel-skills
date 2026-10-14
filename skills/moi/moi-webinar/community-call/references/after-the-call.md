# After the call

The recording description and distribution. Facts are as of 2026-10-02, except where a line cites the handover note of 2026-10-13 (`project-handover-docs/COMMUNITY-CALL.md`), which wins: every call is on the MOI YouTube channel, in one playlist (https://www.youtube.com/playlist?list=PL4-oiZj2acUPhBkDGm-8ue9jIVxh-NXvs), and Vardan owns the recording, the post call tweets and the shorts. **The description evidence is one call only.** CC13 (27 August 2026) has a YouTube description on record. For CC14 (25 September 2026, inferred) the playlist holds the recording; no description, recap post or follow-up was in the record, which ran to 1 October. Every step below is therefore the CC13 pattern, the January 2026 KRA targets, or a question to settle. Each unknown ends in an ASK line. Back to `../GUIDE.md`.

## What is on record
| Item | Evidence | Status |
|---|---|---|
| YouTube description with chapters | CC13, drafted about 15 minutes after the call (inferred from timestamps) and link-checked | Structure kept in `../templates/youtube-description.md`. The text itself was pasted in chat and not saved |
| Recording | Meet recordings sit under the shared info account in Drive for earlier calls | Newer calls: on the MOI YouTube playlist (handover note); Vardan owns it |
| Recap videos | CC6 recaps were filed in the call's Drive folder | Later calls: unknown |
| Blog per call | The strategy meeting of 4 August 2026 decided every dev talk and video is accompanied by a blog | Whether it covers the community call is unknown |
| Social announcement before the call | Copy "MOI Community Call #14 is happening tomorrow" was pasted on 2026-09-24 | Author and channels unknown |
| Notes, resources and action items within 24 hours; Q&A and follow-ups logged within 48 hours | The January 2026 KRA document | Whether it is applied is unknown |

## Steps
1. **Get the recording.** Vardan owns it (handover note) and it goes to the MOI YouTube playlist. ASK: Vardan for the file or the draft video, and who holds the YouTube login.
2. **Draft the description.** Run `python3 "$SKILLS/moi-webinar/community-call/scripts/youtube-description.py" community-call-<N>/deck/index.html > community-call-<N>/description.txt`, with `SKILLS` set as in `../GUIDE.md`. It prints the structure of the CC13 description with a `00:00 Welcome` first chapter and `[__:__]` for every other chapter.
3. **Fill the timestamps from the recording.** Watch it. Chapters must match the order actually presented. Delete a chapter you did not present and merge slides presented together. YouTube needs the first chapter at 00:00.
4. **Fill the rest.** The three-sentence summary says only what was said. The date is written out in full. Upgrade lines carry the exact versions from the ledger, `-rc` suffix included. The validators block stays only if the call carried one.
5. **Add the write-ups.** One line per blog post of the month with descriptive text before the URL. The blog links are the SEO backlinks the 27 August 2026 call notes ask for.
6. **Check every link.** Open each one. CC13's description had 20 links and 2 were dead, one because its pull request was not merged.
7. **Count the characters.** The draft warns above 5,000. Count again after filling the placeholders.
8. **Check the teaser.** Keep "Next up" only if the line-up is confirmed. The CC13 draft description named guests from Coinfest Asia, Bali for CC14, and the CC14 deck had neither. Whether the draft was posted is unknown.
9. **Show the text to the human.** Nothing is uploaded or posted by Claude, and the human pastes it into YouTube.
10. **Log the Q&A.** List each audience question, the answer given, and who owns any follow-up. The target is 48 hours.
11. **Update the ledger and README.** Record what was presented and which rows were still unverified on the day. A stale README misled CC14 readers.
12. **File the deck.** Ask the human before uploading the PDF to Drive. Nothing is uploaded without a yes. The Drive folder is `Community Call`, one subfolder per call, and it is shared. Saving the call folder to the repo is a push and needs a yes: `moi-foundation/MOI-Webinars` is public (as of 2026-10-01), so a push publishes `SCRIPT.md`, the ledger and the host prep. The decks for calls 2 to 14 were merged into the repo under `community-call-N/deck/` in PR #2 (13 October 2026): CC13 is a PDF only, CC14 has the HTML source, `SCRIPT.md` and assets. A new call folder goes in by pull request, after the same yes.

## Distribution
- A manager rule from 24 August 2026 says publishing a blog is not the end of the task: every post must also go out across MOI's social accounts and to the mailing list. Whether that rule covers a call recap is unknown. ASK: Rahul.
- The blog and social pipeline is `moi-blog`. Draft the text and show it to the human; post nothing. Each post goes out only on the human's explicit yes. Posts scheduled with `node "$SKILLS/moi-webinar/scripts/buffer.mjs"` (`buffer.mjs` lives in this library at `moi-webinar/scripts/buffer.mjs`) publish with nobody reviewing them, so use `--draft` unless an exact time matters. Its key is `BUFFER_API_KEY`, kept in a local `.env` and never pasted into chat.
- The 15-second clips: the host wanted them. The shorts are Vardan's (handover note). A video editor works from outside the team; the editor's contact is not recorded (the previous DevRel's notes). ASK: Vardan for the clip plan and the editor. The 7 August standup decided, for AMA clips on YouTube, to post video clips only. Whether it applies to call clips is unknown. ASK: the host.
- The website's homepage calendar was replaced by a Luma block (MOI-Website PR #60, 13 October 2026). It links to the MOI calendar on Luma and stays hidden until `lumaUrl` is set in `content/community-calls.json`; an optional `nextCall` holds the next date, title and link. Setting either is a pull request to a public site, so it needs the human's yes. The runbook is `moi-web-products-ops/references/website-calendar.md`. See `moi-devrel/references/keys-and-access.md`.
  Before touching the website, read its row in `moi-devrel/references/repo-map.md`.

## Traps
- A description can promise something the next call drops. Write only what is confirmed.
- A chapter list copied from the slide titles is a draft. Slide titles such as "Title" and "By engine" are internal. Rename chapters in words a viewer would search for.
- A link to a post whose pull request is unmerged is dead at posting time.
- `buffer.mjs` has no delete command. A wrong scheduled post is deleted by hand in Buffer.
- The YouTube login is a shared account held by Vardan (handover note). See `moi-devrel/references/keys-and-access.md`.

## Not yet known
- Who uploads the recording and writes its description. The recording is Vardan's; whether DevRel pastes the description is not recorded. ASK: Vardan.
- Whether CC14 has a description, and whether CC13's was posted unchanged: open the two videos in the playlist and read them.
- Whether a recap blog or social post is expected. ASK: Rahul.
- Who cuts the 15-second clips: the shorts are Vardan's. ASK: Vardan.
- Whether the 24-hour and 48-hour KRA targets still apply. ASK: Rahul.
