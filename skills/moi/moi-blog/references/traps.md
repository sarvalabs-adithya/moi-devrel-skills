# Traps

Most rows come from real runs, mostly with no error message. A row marked (preventive) does not: it states a rule that follows from how the code or the tool works. Dates are the incident dates. States are as of 2026-10-02. The detail sits in the file named in the last column. The three checks named below are scripts in this skill: run each as `python3 "$SKILLS/moi-blog/scripts/<name>" ...` from your working copy. Back to `../SKILL.md`.

## Writing and claims
| # | Trap | Why, and the incident | Catch, and where to read |
|---|---|---|---|
| 1 | A post misstates the protocol | The release notes were the only source. In August two API names and a "removed" claim were wrong in the notes themselves (`1d537dd`, 2026-08-19). 553 claims were checked and six were wrong (`175a733`, 2026-08-21) | A ledger row per claim against tagged source, then notes, then docs. `authoring.md` |
| 2 | "Live on devnet" from the source tip | On 2026-09-10 devnet still ran 0.12.0 and answered `payer` while the source had `fee_payer` | Read `net.Version` and a recent interaction's field names. `moi-devrel/references/devnet.md` |
| 3 | A claim that sounds right and is not backed | "A native asset standard made for KMOI alone" was a draft line in September and is still in the published post. "Every action costs fuel" was removed (2026-09-11) | Quote the note verbatim. `polish.md` <!-- slop-lint:ignore --> |
| 4 | A universal slips in | "Nobody holds your money" was proved false (2026-08-07) | Search for every, always, never, nobody. `polish.md` |
| 5 | A corrected claim survives elsewhere | The session 7 correction survived in a README, an explainer, a demo plan and deck notes | After any correction, search every doc, the social copy and the deck notes |
| 6 | Counts disagree inside one post | The September post says three breaking changes, four changes and five things break, each counting something different | Say what each number counts. `../examples/README.md` |
| 7 | Wording that came back | "the token", "the fee", "fixed supply", "Voyage devnet", "Participant: an account" (2026-09-11 to 2026-09-25) | `slop-lint.sh` through `post-lint.py`. `moi-devrel/references/terminology.md` <!-- slop-lint:ignore --> |
| 8 | Internal history in public text | A cancelled session and reviewer names appeared in drafts (2026-08-31) | Read for session numbers and names. `authoring.md` |
| 9 | A claim rests on a private repo | `go-moi` and `go-pisa` are private. Without read access the claim is UNVERIFIABLE, never verified | ASK: Gokul for read access. `authoring.md` |
| 10 | A link in the post returns 404 | The September check found one to an access-policies page | Open every link. The lint does not fetch |
| 11 | A placeholder or comment ships | Four HTML comments, one a TODO inside a runbook step, sat in the August post at `draft: false` and blocked publishing until they were removed (`1d537dd`, 2026-08-19). Webinar drafts use `<<< EVIDENCE >>>` and `LUMA_URL` | `post-lint.py` <!-- slop-lint:ignore --> |

## Build and publish
| # | Trap | Why, and the incident | Catch, and where to read |
|---|---|---|---|
| 12 | Only one build was run | The root build never runs the schema, so a missing `summary` becomes `undefined` and exits 0 | Both builds. `publishing.md` |
| 13 | A webinar `BLOG.md` was copied in | `description`, `authorRole`, a string `author` and a `# ` heading do not fit the blog (a string `author` fails the build, checked 2026-10-02) | `authoring.md`, section "Converting a session write-up" |
| 14 | The date error is not about the date | A missing `date` reports "expected date, received Date" | `post-lint.py` names the field |
| 15 | A tag nobody can see | Only `agents`, `protocol` and `native-assets` show. 19 tag pages exist for 6 posts and 16 have no link | `authoring.md`, `geo.md` |
| 16 | `updated` equals `date` | No Updated line shows. It still sets `dateModified` | `post-lint.py` warns |
| 17 | A personal byline reads as an organisation | JSON-LD types every author `Organization` | Do not fix it in a content PR |
| 18 | `<Subscribe />` in the body | The page already renders the form. In a `.md` file the tag is inert. The September post has one | `post-lint.py` warns |
| 19 | The preview listing links to production | `BLOG_ORIGIN` is set nowhere in the workflows | Verify at the blog preview URL. `publishing.md` |
| 20 | A preview link in a post | Previews are deleted after 7 days or when the PR closes | `post-lint.py` rejects `*.preview.moi.technology` |
| 21 | A green deploy is taken as live | Deleted posts survived deploys in August because the VM script ran `npm install` and not `npm ci --prefix blog` (2026-08-18) | `check-live.py <slug>` and `--expect-gone` |
| 22 | The apex status code is trusted | `moi.technology` answers 200 for any path (observed 2026-10-02) | Use the blog host, or read the page text |
| 23 | The checked-in guides are believed | `CONTENT.md`, `DEPLOYMENT.md` and `blog/README.md` are wrong in several places | `authoring.md` |
| 24 | A published slug is renamed | The slug is the URL, the canonical and the feed `guid` | Do not rename. `publishing.md` |
| 25 | The deploy workflow is run by hand on a branch | It hands the branch name to a script nobody here has read (preventive) | Run it on `main` only |
| 26 | A PR per review tweak | On 2026-09-15 five one-tweak PRs were opened during a review of another repo and one batch PR was asked for instead. The September post's PR had 24 commits and landed as one | One branch, small commits, one PR |
| 27 | The ledger or a record is committed | `sarvalabs/MOI-Website` is public and the ledger's source column may name private repos (preventive) | Keep it in `$WORK/<slug>/` |

## Announcing
| # | Trap | Why, and the incident | Catch, and where to read |
|---|---|---|---|
| 28 | Distribute run before the copy PR merged | It reads `main` and stops with "No copy file" | Merge first. `distribution.md` |
| 29 | The seeded copy is sent | The scaffold fills all four channels with the title and summary. PR #56 shows it | `copy-lint.py` |
| 30 | Discord and Telegram post unreviewed | They send at once when their secrets are set. Whether they are set is not recorded | Empty both blocks unless told otherwise |
| 31 | Distribute run twice | No idempotency: a second run posts again and makes a second draft | One real run, then `status.md` |
| 32 | A clean local dry run is trusted | With no secrets every channel prints "missing" and exits 0. Length is never tested | Throwaway values and `--dry-run`. `distribution.md` |
| 33 | A bare domain in X copy | The pipeline counts it literally and X may charge 23 | Write `https://` |
| 34 | Edited post, no new copy | Prepare only looks at added files | `social:init <slug> -- --force`. `distribution.md` |
| 35 | Prepare run with force and no slug | It would overwrite every post's copy. It now refuses (`bc7a489`) | Name a slug |
| 36 | The announcement stalls unnoticed | PR #56 has been open since 2026-09-11 and nothing tracks it | `status.md` and the hand-back |
| 37 | Telegram markup | The message is HTML-escaped, so `**bold**` shows literally | Plain text only |
| 38 | Medium first | The first copy becomes the canonical copy | Set the canonical link, or post only on the blog |

## Buffer
| # | Trap | Why, and the incident | Catch, and where to read |
|---|---|---|---|
| 39 | The wrong key name | `BUFFER_ACCESS_TOKEN` is for the pipeline and `BUFFER_API_KEY` for `buffer.mjs` | `buffer.md` |
| 40 | A scheduled post publishes unreviewed | `buffer.mjs` is the opposite of the pipeline's draft guarantee. The midnight incident of 2026-09-10 is in `moi-devrel/references/terminology.md`, table C | `--draft`, and print the UTC string first |
| 41 | `--at` without `Z` | It is read in the machine's zone | End every time in `Z`. `time-table.sh` |
| 42 | No length, placeholder or delete support | `buffer.mjs` prints characters, ignores `RELEASE_URL` and cannot delete | Check by hand. `buffer.md` <!-- slop-lint:ignore --> |
| 43 | A 401 is read as "the query is fine" | Buffer authenticates before it validates (`67c1e33`) | Use introspection to check shapes |
| 44 | The script is run from a session folder | It is only at the repo root (2026-08-31) | `cd "$(git rev-parse --show-toplevel)"` |
| 45 | `--thread-dir` is missing | It is in an unpushed commit. The pushed branch lacks it | ASK: Adithya for a copy |
| 46 | A key is pasted in chat | A Buffer key was pasted and revoked (2026-08-31) | Hidden prompt only. Never open an `.env` |

## Newsletter
| # | Trap | Why, and the incident | Catch, and where to read |
|---|---|---|---|
| 47 | The campaign reads `/rss.xml` | Clicks land as direct or referral | Read `/rss-email.xml`. `newsletter.md` |
| 48 | Mailchimp's own Google Analytics tracking is on | `utm_campaign` becomes the campaign name and the data still looks fine | Leave it off |
| 49 | A change to `utm.js` or a slug | Every feed `guid` changes at once | Do not touch it casually |
| 50 | The email shows only a summary | The feed carries the summary, not the body. That is the design | `newsletter.md` |
| 51 | One item renders and raw loop markers show | Bare text between `<tr>` rows is lifted out of the table by the parser | Use `templates/mailchimp/body.html` |
| 52 | A new weekly campaign sends nothing | The first send looks back one cycle (a Mailchimp rule, not re-checked) | Wait for a new post |
| 53 | "Send now and start RSS campaign" | It sends at once to the audience | Use "Start RSS". A gate |
| 54 | The preview is read, not the inbox | Logo size, one post only and an all-purple layout were found only in a real test email (2026-08-24) | Test send, read on a phone |
| 55 | An image changed in place | Mailchimp caches by URL and has no purge (`b8c3dea`, `85629a5`, `b150873`, 2026-08-24) | A new file name each time. `assets.md` |
| 56 | The footer icons are the monochrome set | The `-colour` set is current. `moi.png` is 62 by 48 and is squashed if set to a square | The template already uses `-colour`. `assets.md` |

## Images, search and measurement
| # | Trap | Why, and the incident | Catch, and where to read |
|---|---|---|---|
| 57 | An SVG cover without its PNG | `og:image` points at a missing `.png`. No post sets `cover` today | `post-lint.py`, `check-live.py --expect-cover` |
| 58 | The wrong logo file | `default-light.svg` is the purple mark. The previous operator's older design folder said the reverse and its SVGs rendered black. The design branch of this library has the corrected rule | `assets.md`, `moi-devrel/design/references/logos-and-mascot.md` |
| 59 | The documented figure is copied | `agent-flow.svg` is drawn in the old palette | `post-lint.py` warns |
| 60 | sharp ignores Poppins | The renderer falls back to Helvetica Neue (the previous operator's test) | A headless browser. `assets.md` |
| 61 | The apex is registered, the blog is not | Search Console treats the subdomain as a separate property | `geo.md` |
| 62 | A link tagged `LinkedIn` | GA4 splits it from `linkedin` | Lowercase, always. `geo.md` |
| 63 | An AI crawler is blocked by the zone, not by the file | `cocolang.dev` returned 403 to AI crawlers until 2026-09-09 | `curl -A` after any Cloudflare change. `geo.md` |
| 64 | `VITE_GA_ID` is changed | Nothing reads it | Measurement runs through Tag Manager |
