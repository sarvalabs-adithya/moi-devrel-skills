# The newsletter

Facts are as of 2026-10-02. Back to `../SKILL.md`. Mailchimp polls an RSS feed on a schedule and mails what is new. There is no code, no secret and no workflow on MOI's side: `git grep -i -E "mailchimp|newsletter|rss" .github/workflows` finds nothing on `main`. What the repo owns is the feed Mailchimp reads, the signup form, and the images. The campaign itself, its schedule, audience, subject and sender live only in Mailchimp, so most of this file is what to check before you touch it.

## What is confirmed and what is not
Read on 2026-10-02 with GET requests and in the code:
- `https://blog.moi.technology/rss-email.xml` answers 200 with every published post, each link tagged `utm_source=newsletter&utm_medium=email&utm_campaign=<slug>`. `/rss.xml` carries the same posts with bare links.
- Every article page ends with a signup form that posts to Mailchimp's hosted endpoint (`blog/src/components/Subscribe.astro`). The live September page has it.
Not confirmed, because no evidence shows it:
- That the weekly campaign exists and is running, its day and hour, its audience, its sender, and whether the September post went out. On 2026-08-24 the previous operator described a weekly blast that sends "if and only if any new blogs have gone up", and no artifact shows the result. His messages mention a Monday blast, so Monday is inferred, not recorded. The repo disagrees with itself: `social/README.md` says Mailchimp polls weekly, the message of `cc6ddf1` says an RSS campaign "mails each new post automatically", and the signup form on every article promises "One email per post". ASK: Sai Kiran, then Rahul.
- Who owns the Mailchimp account, and the plan. About 5,500 subscribers is recorded (the previous operator's `DEPENDENCIES.md`, a file on his machine only; ASK: Adithya for a copy), which needs a paid plan. ASK: Rahul.
- A one-off send to all validators (28 to 31 August 2026) about the Voyage login moving to MOI Wallet was prepared. The previous operator asked for the subject, the HTML and the logo, removed a line about the faucet and the network rename, and asked to schedule nothing until GitHub was back. Whether it was sent is not recorded. ASK: Adithya.
- Whether the sending domain has DKIM and DMARC records for Mailchimp. DevOps owns the DNS. ASK: Upendhar.
Before you build anything, find out whether the campaign exists. Ask the operator to log in to Mailchimp, open the campaign list and read you its state, then write it in the hand-back. Claude never types a password.

## Two feeds, on purpose
```
/rss.xml        https://blog.moi.technology/article/<slug>/
/rss-email.xml  https://blog.moi.technology/article/<slug>/?utm_source=newsletter&utm_medium=email&utm_campaign=<slug>
```
Mailchimp takes each item's link as it is. Point it at `/rss.xml` and every reader lands in GA4 as direct or referral. Tagging `/rss.xml` in place would file feed-reader traffic as email. So the campaign reads `/rss-email.xml`, and feed readers keep `/rss.xml`. Only `/rss.xml` is advertised for autodiscovery, and neither feed is in the sitemap.
- Mailchimp's own Google Analytics link tracking stays off. Left on, it rewrites every link and names `utm_campaign` after the Mailchimp campaign, not the slug. The data still looks fine and the post stops joining up with its X and LinkedIn rows.
- The feed's `guid` is the full tagged URL. A slug rename, or an edit to the source, medium or order of parameters in `blog/src/lib/utm.js`, changes every guid at once. Mailchimp decides what is new from guid and publication date, so a cosmetic change could look like a batch of new posts (a Mailchimp behaviour, not observable here).
- The feed carries each post's `summary` as `<description>` and no full body. `*|RSSITEM:CONTENT|*` therefore renders the summary. That is the digest shape, not a truncation.
- A post reaches the feed only after the deploy has run. A merged PR is not yet in the feed.

## The signup form
`Subscribe.astro` posts to Mailchimp with no backend and none of the embed's scripts. Two parts of Mailchimp's own markup must survive any change: the hidden `b_<user>_<audience>` input (the honeypot, hidden off-screen, never with `display: none`, because bots skip fields that are not rendered) and `target="_blank"` (the confirmation page must not replace the article). Do not "restore the official embed".

## Building the campaign
The Mailchimp interface changes, so treat the menu names as a guide. Everything in this section and the next is the previous operator's account of Mailchimp, not re-checked on 2026-10-02. Check Mailchimp's help before relying on a rule. Every step is a gate.
1. Automations, Flow templates, "Share blog updates via RSS".
2. Name and audience. Use a segment or tag that holds only test addresses. Never point a first run at the full list.
3. RSS Feed step: the feed URL `https://blog.moi.technology/rss-email.xml`, and the schedule.
4. Setup step: subject line and From name. The sender must be a real MOI address. Sai Kiran and Vardan Aggarwal were asked about the sender identity on 2026-08-24. ASK: Sai Kiran what was decided.
5. Design: paste the three templates (below).
6. "Start RSS". The dropdown beside it also offers "Send now and start RSS campaign", which sends at once to whoever the audience is. Never choose it by habit.
Mailchimp generally will not let you change the audience of a running RSS campaign, so "test, then switch" does not exist: test, discard, rebuild against the real audience.
| Behaviour | Consequence |
|---|---|
| "Start RSS" only activates the schedule | Nothing sends at that moment. That is not a failure |
| It sends only if the feed has new content | An unchanged feed at send time is a silent no-op |
| A post should be in the feed at least 3 hours before the send time | A post deployed an hour before the window waits a cycle |
| The first send looks back one cycle: 24 hours daily, 7 days weekly | A weekly campaign started today, with only older posts, sends nothing. That is correct |
| One email per cycle holds all new items | Three posts in a week make one email |

## The templates
`../templates/mailchimp/` holds three HTML parts, carried forward from the previous operator's skill after a check: no secret, no personal address and no tracking id in any of them.
| File | Paste into |
|---|---|
| `header.html` | The Header code block |
| `body.html` | The block that replaces the designer's RSS Items block |
| `footer.html` | The Footer code block |
They declare only `width="100%"`. In the designer set the content width to 600px and the page background to `#fcfbff`. Changes from the originals: the header line uses a colon in place of an HTML em dash entity, and the footer uses the `-colour` icon files, which exist on `main`.
Left out on purpose: the earlier single-file draft. It carries the bug below and points at `/brand/logo-email.png`, which was renamed away in `b150873` and now returns 404.
- The loop bug. The loop is `*|RSSITEMS:|*` to `*|END:RSSITEMS|*`. Bare text between `<tr>` rows is lifted out of the table by the HTML parser, so both markers land together and wrap nothing. The symptom: one item renders and the literal markers show above it. It looks like a merge-tag problem and is a parser problem. The fix, as in `body.html`: put the markers inside a `<td>` and make the repeating unit a complete nested table.
- Tables and inline styles only. No SVG. Fonts fall back to Helvetica or Arial in most clients, so design for the fallback. Colours are opaque hex.
- Required merge tags: `*|UNSUB|*`, `*|UPDATE_PROFILE|*`, `*|LIST:ADDRESS|*` (the postal address Mailchimp holds for the audience) and `*|CURRENT_YEAR|*`. Mailchimp will not send without the address.
- Images: absolute URLs under `https://blog.moi.technology/brand/`. Deploy an image before pasting a template that uses it. Never change an image in place (`assets.md`).
- A Mailchimp preview is not an inbox. On 2026-08-24 an oversized logo, a single post and an all-purple layout were found only in a real test email. Send a test to the operator's own address and read it on a phone.

## One-off sends
For an audience that is not the weekly list, such as the validators. Claude drafts the subject, the preview line and the body from `../templates/announce/one-off-send.md`. The operator builds and sends it in Mailchimp.
- Name the audience or segment exactly, and the number of people in it.
- Tag the link `utm_source=newsletter&utm_medium=email&utm_campaign=<slug>`, lowercase, with the slug of the post it points to.
- Put the send time as a date, 24-hour UTC and India time (`time-table.sh`).
- Send a test first. "Send" is a gate that names the audience and the time.
- Public-text rules apply: no em dash, no emoji, no placeholder, the network is devnet, no cancelled plans.

## Deliverability
Google and Yahoo require domain authentication for bulk senders. Two DKIM records and one DMARC record are the usual setup, and unauthenticated sending shows up as a falling open rate, not as an error (the previous operator's note). Whether MOI's Mailchimp domain is authenticated is not recorded. ASK: Upendhar.

## Not yet known
- Whether the weekly campaign is live, and its day, hour and audience. ASK: Sai Kiran.
- Who owns the account, the plan and the sender identity. ASK: Rahul.
- Whether the validator email was sent. ASK: Adithya.
- Whether the September post, or any post, was emailed. ASK: Sai Kiran.
