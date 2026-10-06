# Traps: failures that give no error

Every row is a real incident or a property of a tool that was read. The full command for each tool is in `../GUIDE.md`, steps 4 to 7. Facts are as of 2026-10-02. `ASK:` is defined in `moi-devrel/SKILL.md`. `SKILLS` is set as in `../GUIDE.md`. Back to `../GUIDE.md`.

## The time
| Trap | What happened | Check |
|---|---|---|
| "today at 12:00 AM UTC" | Read as noon. Two scheduled posts were wrong and were deleted by hand (2026-09-10) | Write "00:00 UTC on <date> (05:30 IST)". Run `time-table.sh`. `thread-lint.py` rules `twelve-am` and `relative-day` <!-- slop-lint:ignore --> |
| A `--at` value with no `Z` | `Date.parse` reads it in the machine's local zone | End it in `Z`. Compare the printed UTC string with `time-table.sh` |
| A scheduled post | It publishes at its time with nobody reviewing it | Use `--draft`. Schedule only on a yes that names the text and the UTC time |
| EST written for a US Eastern time | EST is UTC-5 all year, so a summer time is an hour out | Give `America/New_York` to `time-table.sh` |
| "Scheduled for" left in a post that publishes after the moment | The text is then false | Re-read the tense of every post against its publish time |

## The tool
| Trap | What happened | Check |
|---|---|---|
| Two Buffer tools with two variable names | `scripts/buffer.mjs` uses `BUFFER_API_KEY` from a local `.env`. The website pipeline uses `BUFFER_ACCESS_TOKEN` from GitHub secrets. The first publishes on its own unless `--draft` is given. The second saves X and LinkedIn as drafts | Know which tool you are in. `moi-blog` owns the second |
| No delete, no length check, no placeholder check | `buffer.mjs` prints a post's length and stops at no limit. It checks no placeholder | `thread-lint.py` before any send. Delete a wrong post by hand in Buffer |
| A dry run is not offline | It exits without `BUFFER_API_KEY` and still reads the organisation and channel list from Buffer | Say so when asking the operator to run it |
| Thread file names | Only `<n>.txt` is read. Any other name is skipped silently. The first file is the root. X only. Not with `--follow` | `thread-lint.py` rules `thread-number` and `thread-file` |
| Wrong folder | On 2026-08-31 the command failed because it ran inside a session folder | `cd "$(git rev-parse --show-toplevel)"` first |
| `--thread-dir` is not on any shared branch | It is in commit 5bcfbcd, unpushed (as of 2026-10-02) | ASK: Adithya for a copy |
| A key pasted into chat | A Buffer key was pasted on 2026-08-31 and revoked | Keys go in `.env` only. A stale key above a new one is harmless because the last line wins. The symptom of a stale key is "access token is not valid" |

## The files
| Trap | What happened | Check |
|---|---|---|
| The folder is not a record | In v0.13.0 `SOCIAL.md` said the time was corrected to noon while its own text said 12:00 AM. It said `linkedin.txt` was sent, then the file was overwritten with a rewrite | One copy of each text. `SOCIAL.md` holds status and decisions only |
| "Unedited" was not true | `RELEASE-NOTE.md` was labelled "as sent by the protocol team, unedited". It held the thread's sentences. The original is lost | Hash the note when pasted. Log every difference |
| Placeholders ship | `RELEASE_URL` ended `discord.txt` and `linkedin.txt`. The webinar packs have `LUMA_URL` and `CANONICAL_URL` | `thread-lint.py` rule `placeholder`. `slop-lint.sh` warns too <!-- slop-lint:ignore --> |
| Three copies of a sentence | A fix to one left the others. The same release note sentences sat in the note, `SOCIAL.md`, the thread and LinkedIn | After any change, grep the pack and the post |
| The ignore marker in a post | `slop-lint:ignore` makes the lint skip a line. In a post it would be published | `thread-lint.py` rule `ignore-marker` |

## The words
| Trap | What happened | Check |
|---|---|---|
| "Live" read from the source | On 2026-09-10 devnet still returned `payer` and version 0.12.0 while the source had `fee_payer` | Read the node. Before the upgrade write "scheduled" |
| Retired wording survived | "Voyage devnet" stayed in `discord.txt` and in the post twice. "Fixed supply" stayed in two drafts | `slop-lint.sh`. Say devnet and capped supply <!-- slop-lint:ignore --> |
| A universal | "Every action on MOI costs fuel" was removed from the post twice (2026-09-11) | Say what the release changes <!-- slop-lint:ignore --> |
| A noun with no name | "The token", "the fee", "MOI's own token" drew the strongest complaints (2026-09-11) | Write KMOI. Fuel for what is paid, fee payer for the role <!-- slop-lint:ignore --> |
| A claim from the note alone | A draft said KMOI's standard is "made for KMOI alone". It is in neither the note nor source | Source it or use the note's words (`unverified-phrase`) |
| A release candidate called stable | At CC13 an RC was written up as shipped. As of 2026-10-02 the npm `latest` tag of `js-moi-sdk` is 0.9.0-rc2 | Keep the `-rc` suffix. Never write "stable". "Latest" says only what npm says <!-- slop-lint:ignore --> |
| Counts that disagree | The September post says three breaking changes, four changes and five things that break. Each count is of a different thing | Say what each number counts |
| "Participant: an account on MOI" | The glossary line predates the 2026-09-14 correction. The wording is contested | Use the safe form in `moi-devrel/references/terminology.md`: "A participant is a person, a company or an agent. Its state is held in an account." ASK: Rahul whether the glossary line is rewritten <!-- slop-lint:ignore --> |
| Automated passes undo edits | Humanizer and stop-slop passes brought back vague phrasing that had been rejected (2026-09-11) | Re-read the opener and the KMOI and anu paragraphs after every pass |

## The process
| Trap | What happened | Check |
|---|---|---|
| A ledger that checks the post against itself | A draft checked against a draft proves nothing | Source order: tagged source, then the note, then docs.moi.technology. The docs had op-code numbers swapped in August 2026 |
| A claim resting only on the note | Soften it, as the post did on 2026-09-11 | Give it a ledger verdict `scoped` or `argument`, or cut it |
| The copy PR stalls | Merging the post opened PR #56 in 26 seconds. As of 2026-10-02 it is still open, and no evidence shows the post was announced through the pipeline | After the merge, follow the copy PR to the end (`moi-blog`) |
| The seeded copy reaches Discord | The website's Prepare step seeds Discord and Telegram blocks with the post summary | Empty a block you do not mean to send |
| Attribution lines | The commits and body of PR #53 carry an AI co-author line and footer, which the previous operator later banned (2026-10-01) | None on any commit or PR |
| A Medium-first post | The first one published there becomes the canonical copy | Do not post a release on Medium first |
| Sub-agents | A claim run once used 15 agents. Another plan used 79, which was too many | Only when the operator asks. State the count and the model first |
| A wipe nobody warned about | The note was silent. The Launchpad took 4 days to move to the new registry, the Explorer 11, and the MCP pinned it after 12 | Ask the protocol team before the pack goes out (`timing.md`) |

## Not yet known
- Whether Buffer shows a character count the way X will count it. Keep a margin and read the draft.
- How X counts a character outside plain ASCII. Post 5 of v0.13.0 uses an arrow. ASK: Adithya whether that post displayed correctly.
