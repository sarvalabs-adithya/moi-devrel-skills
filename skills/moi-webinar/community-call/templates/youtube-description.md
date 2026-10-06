# YouTube description template

The structure of the one description on record (Community Call 13, 27 August 2026).
No other call has a description on record, so treat the structure as a starting point.

How to use it:

1. With `SKILLS` set to the folder that holds the `moi-*` skills, run from the working copy:
   `python3 "$SKILLS/moi-webinar/community-call/scripts/youtube-description.py" community-call-<N>/deck/index.html > community-call-<N>/description.txt`.
   It fills `{{TITLE}}`, `{{CHAPTERS}}` and `{{NEXT_NUMBER}}` and prints the draft. The first
   chapter is `00:00 Welcome`. Without a `<title>` in the deck's head it prints `[CALL TITLE]`.
2. Watch the recording and replace every `[__:__]` with the real time. Delete the
   chapters you did not present, and merge slides you presented together. Chapters must
   match the order actually presented. YouTube needs the first chapter at 00:00.
3. Fill every other `[PLACEHOLDER]`. Delete a block you have nothing true to put in.
4. Keep it under 5,000 characters. Count again after filling.
5. Descriptive text before each link ("September 2026 release post: https://..."), never
   "read more". Open each link before posting. The Call 13 description had 20 links and 2
   were dead, one because its pull request was not merged.
6. Show the final text to the human. Nothing is posted by this branch. The human pastes it into
   YouTube.

Block rules:

| Block | Where the content comes from |
|---|---|
| Summary, three sentences | The slides as presented. Say only what was said. |
| Recorded date | The call date. Write it out in full. |
| If you are upgrading | The numbers ledger rows for versions. Keep an `-rc` suffix as written. |
| Validators | Only if the call carried a validator notice. Call 13 had one. |
| Full write-ups | The blog posts for the month. The blog links are the SEO backlinks the 27 August 2026 call notes ask for. |
| Next up | Only a line-up that is confirmed. The Call 13 draft description named guests from Coinfest Asia, Bali for Call 14, and Call 14 had neither. Whether the draft was posted is unknown. |
| Hashtags | Which hashtags Call 13 used is not on record. ASK: Sai Kiran which tags the channel uses. |

<!-- BEGIN DESCRIPTION -->
{{TITLE}}

[Sentence 1: what this call covered.] [Sentence 2: the headline from the protocol segment, as presented.] [Sentence 3: what the community and marketing segments covered.]

Recorded [DAY MONTH YEAR]

CHAPTERS
{{CHAPTERS}}

IF YOU ARE UPGRADING
[Package name, exact version as written in the release note: what it carries]
[One line per package]

VALIDATORS
[Only if the call carried a validator notice, otherwise delete this block]

READ THE FULL WRITE-UPS
[Release post title: https://blog.moi.technology/article/<slug>/]
[Any other post from the month: link]

BUILD ON MOI
[Docs: link]
[SDK or repo: link]

COMMUNITY
[Discord invite: link]
[Other community links]

ABOUT MOI
[One line: one of the two current lines in moi-devrel/references/terminology.md section D. The choice for YouTube is open; the operator asks before filling this]

Next up: Community Call #{{NEXT_NUMBER}} [only if the line-up is confirmed, otherwise delete this line]

[HASHTAGS]
<!-- END DESCRIPTION -->
