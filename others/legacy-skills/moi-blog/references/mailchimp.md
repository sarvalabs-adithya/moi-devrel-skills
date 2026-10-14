# The newsletter

Mailchimp polls an RSS feed on a schedule and mails whatever is new. There is no code
path, no credential, and no CI step on our side, which is why the newsletter is absent
from `.github/workflows/` while the four channels that do send, Discord, Telegram, X and
LinkedIn, are all in `distribute.yml`. Verified:
`grep -rniE 'mailchimp|newsletter|rss' .github/workflows/` returns nothing. (`devto` and
`reddit` are in the `utm.js` vocabulary but have no workflow either.)

What the repo owns is the feed Mailchimp reads, the form that fills the list, and the
HTML the campaign renders. Everything else lives in Mailchimp's UI and is marked below as
an operational note.

| Thing | Where |
| --- | --- |
| Feed Mailchimp polls | `blog/src/pages/rss-email.xml.js` → `https://blog.moi.technology/rss-email.xml` |
| Public feed (readers) | `blog/src/pages/rss.xml.js` → `/rss.xml` |
| UTM convention | `blog/src/lib/utm.js` |
| Signup form | `blog/src/components/Subscribe.astro` |
| Campaign HTML | `references/mailchimp-header.html`, `-body.html`, `-footer.html` |
| Email images | `blog/public/brand/moi-mark-purple.png`, `blog/public/brand/social/*.png` |
| Schedule, audience, subject, sender | Mailchimp UI only |

A post reaches the feed only after `deploy.yml` runs (push to `main` → Teleport → VM). A
merged PR is not yet in the feed.

## Two feeds, on purpose

```
/rss.xml        https://blog.moi.technology/article/what-is-moi-network/
/rss-email.xml  https://blog.moi.technology/article/what-is-moi-network/?utm_source=newsletter&utm_medium=email&utm_campaign=what-is-moi-network
```

Both are the same posts, same order, same `draft: false` filter. The only difference is
that `rss-email.xml.js:34-37` runs each link through `withUtm()`:

```js
link: withUtm(new URL(`/article/${post.id}/`, context.site).href, {
  channel: NEWSLETTER,          // bySource('newsletter') → { source:'newsletter', medium:'email' }
  campaign: post.id,            // the slug, same as every other channel
}),
```

Mailchimp takes each item's `<link>` verbatim. Point it at `/rss.xml` and every reader
lands in GA4 as direct or referral. Tagging `/rss.xml` in place would be worse: feed
readers are not the newsletter, and filing their traffic as `medium=email` corrupts the
data in the other direction. Hence two feeds.

`withUtm` takes an absolute URL (`new URL(url)` inside it), which is why `rss-email.xml.js`
resolves against `context.site` while `rss.xml.js` can pass the bare path, because `@astrojs/rss`
absolutises the plain one for you.

Only `/rss.xml` is advertised for autodiscovery (`blog/src/layouts/Base.astro:52-57`), and
neither endpoint appears in `sitemap-0.xml`. `/rss-email.xml` is reachable but unlisted.
That is correct: a feed reader that found it would report itself as email traffic forever.

### Gotchas in the feed

**Mailchimp's own "Google Analytics link tracking" must be OFF.** *(Operational: a
campaign setting, not in the repo.)* Left on, it rewrites every link with its own UTMs and
names `utm_campaign` after the Mailchimp campaign instead of the post slug. The links still
carry UTMs, GA4 still shows email traffic, and the numbers look fine, but the post no
longer joins up with its X, LinkedIn, Discord and Telegram rows, which is the entire point
of `utm_campaign = slug`.

**`utm.js` is a feed-affecting file.** The built `<guid isPermaLink="true">` carries the
full query string, identical to `<link>`:

```xml
<guid isPermaLink="true">https://blog.moi.technology/article/moi-august-2026-release/?utm_source=newsletter&amp;utm_medium=email&amp;utm_campaign=moi-august-2026-release</guid>
```

Edit the source, medium, or parameter order in `blog/src/lib/utm.js` and every guid in
`/rss-email.xml` changes at once. Mailchimp decides what is new from guid and pubDate
*(operational: its dedupe rules are not observable from here)*, so a cosmetic rename in
`utm.js` can look to Mailchimp like an archive of brand-new posts. Same hazard on a slug
change, which moves both the URL and the guid.

**The feed carries summaries, not articles.** `items[].description` is `post.data.summary`
and nothing sets `content`, so the built XML has `<description>` and no
`<content:encoded>`. `*|RSSITEM:CONTENT|*` therefore renders the one-line summary. That is
the intended digest shape. If someone asks why the email is "truncated", it is not
truncated: full bodies would need a `content:` field added to the `rss()` items.

## The signup form

`blog/src/components/Subscribe.astro` posts straight to the hosted endpoint. No backend,
no Mailchimp JS:

```js
const ACTION = 'https://technology.us5.list-manage.com/subscribe/post?u=5e0c585d54cd6a99ab449871d&id=b599b2bb66&f_id=00fa42edf0';
const HONEYPOT = 'b_5e0c585d54cd6a99ab449871d_b599b2bb66';
```

Rendered on the index (`heading="Never miss a post"`) and at the foot of every article.

Two things carried over from Mailchimp's generated embed that must survive any refactor:

| Keep | If you drop it |
| --- | --- |
| `<input name="b_<user>_<audience>">`, hidden via `.sr-only` | Bots fill every field they find; a submission arriving with the honeypot non-empty is what Mailchimp discards. Signups still work, so nothing fails: the list just fills with junk and the send count against the plan climbs. |
| `target="_blank"` on the form | Mailchimp's confirmation page navigates the reader out of the article they were reading. |

The honeypot is hidden **off-screen** (`position:absolute; width:1px; clip:rect(0,0,0,0)`),
not with `display:none`. Switching to `display:none` looks tidier and is the exact failure:
bots skip fields that are not rendered, so the trap stops catching anything while still
appearing to be there.

The rest of Mailchimp's embed (a stylesheet, jQuery, `mc-validate.js`, and several hundred
lines of SMS country-code handling for a field this audience does not have enabled) is
deliberately absent. Do not "restore the official embed".

## Building the campaign

*(Operational: Mailchimp UI, current as of this writing. The menu names move.)*

1. **Automations → Flow templates → "Nurture leads" → "Share blog updates via RSS".**
2. Name + audience. **Pick a segment or tag containing only test addresses.** Never point a
   first run at the full list.
3. **RSS Feed step:** feed URL `https://blog.moi.technology/rss-email.xml`, plus schedule.
4. **Setup step:** subject line and From name.
5. **Design:** see the template section below.
6. **"Start RSS."** The dropdown beside it also offers *"Send now and start RSS
   campaign"*: that one sends **immediately**, to whoever the audience is. The two sit in
   the same control.

Then rebuild the campaign against the real audience. Mailchimp generally will not let you
swap the audience on a running RSS campaign, so "test on a segment, then switch" is not a
sequence that exists: it is test, discard, rebuild.

### Timing, which surprises people

| Behaviour | Consequence |
| --- | --- |
| "Start RSS" activates the schedule only | Nothing sends at that moment. Not a failure. |
| Sends only if the feed has new content | An unchanged feed at send time is a silent no-op. |
| A post must be in the feed **≥ 3 hours** before send time | Merge-and-deploy an hour before the window and the post waits a full cycle. |
| First send looks back a fixed window: 24h daily / 7 days weekly / 30 days monthly | A weekly campaign started today, with all posts older than a week, sends **nothing** on its first run. This is correct behaviour and gets misread as a broken feed. |
| One email per **cycle**, containing all new items | Three posts in one week is one email, not three. |

Ours polls weekly (`social/README.md`: "Mailchimp polls `/rss-email.xml` weekly on its own,
so it needs no code and no secrets").

## The template

**Use the three-part set, not the single file:**

| File | Paste into |
| --- | --- |
| `references/mailchimp-header.html` | Header code block |
| `references/mailchimp-body.html` | The block replacing the designer's RSS Items block |
| `references/mailchimp-footer.html` | Footer code block |

`references/mailchimp-template.html` is the earlier single-file draft. It is kept as the
worked example of the bug below and **should not be pasted into a campaign**: it still
carries the foster-parenting bug, and its masthead points at
`/brand/logo-email.png`, which was renamed away in commit `b150873` and now 404s.

### The RSS loop bug

Mailchimp's loop is `*|RSSITEMS:|* … *|END:RSSITEMS|*`, with `*|RSSITEM:TITLE|*`,
`*|RSSITEM:URL|*`, `*|RSSITEM:CONTENT|*`, `*|RSSITEM:DATE|*` inside it.

Putting those markers as bare text between `<tr>` elements does not work. Text cannot be a
direct child of `<table>`, so the HTML5 parser *foster-parents* it, lifts it out of the
table and drops it immediately before. Both markers land next to each other, wrapping
nothing.

Run `mailchimp-template.html` through a real parser and you can watch it happen:

```
…<body><table role="presentation" …>
  <tbody><tr>
    <td align="center" …>

      *|RSSITEMS:|*
      *|END:RSSITEMS|*

      <table role="presentation" width="600" …>
```

Source order has 25 lines and two `<tr>` blocks between those markers. After parsing,
nothing but whitespace separates them. The same test on `mailchimp-body.html` leaves 1440
characters (the whole repeating unit) still inside the loop.

**Symptom:** exactly one item renders, and the literal text `*|RSSITEMS:|* *|END:RSSITEMS|*`
sits together on one line above the content. It looks like a merge-tag problem. It is a
parser problem, and no amount of correcting the tag spelling fixes it.

**Fix:** put the markers inside a `<td>`, and make the repeating unit a complete nested
`<table>`, which is what `mailchimp-body.html:3-31` does:

```html
<td style="padding:0;">
  *|RSSITEMS:|*
  <table role="presentation" width="100%" …>
    <tr><td>…*|RSSITEM:TITLE|*…</td></tr>
    <tr><td>…divider…</td></tr>
  </table>
  *|END:RSSITEMS|*
</td>
```

### Email HTML constraints

- Tables and inline styles only. Outlook ignores flexbox, grid, and most `<style>` blocks.
- **No SVG.** Gmail strips it; Outlook never supported it. The brand SVGs in
  `blog/public/brand/logos/SVG/` are unusable here: that is why the PNGs exist.
- Web fonts mostly do not load. Every declaration in these templates is
  `'Poppins','Helvetica Neue',Helvetica,Arial,sans-serif`; the fallback is what most
  recipients actually see. Design to it rather than to Poppins.
- Colours are the blog's tokens flattened to opaque hex, because `rgba()` is unreliable in
  email. `#4b17e5` (`--moi-main`) and `#0a051a` (`--ink`) appear in the template set and
  match `blog/src/styles/global.css` exactly; the greys are opaque approximations of the
  `rgba()` muted and line tokens. `#fcfbff` (`--bg`) is the page background behind the
  card: it is not in the three-part set, because the designer's own template supplies the
  outer wrapper; set it there.

### Required merge tags

| Tag | Where in the set |
| --- | --- |
| `*\|UNSUB\|*` | `mailchimp-footer.html:38` |
| `*\|UPDATE_PROFILE\|*` | `mailchimp-footer.html:36` |
| `*\|LIST:ADDRESS\|*` | `mailchimp-footer.html:42` |
| `*\|CURRENT_YEAR\|*` | `mailchimp-footer.html:42` |

The physical postal address is required by CAN-SPAM and enforced by Mailchimp. It can be
made visually quiet (ours is 10px `#c4c0cf` alongside the copyright) but it cannot be
removed, and Mailchimp will refuse to send without it.

### Images: never overwrite, always rename

Mailchimp caches images by URL and gives you no way to purge one. Its designer *and the
campaign archive* keep serving the copy it fetched first.

This is not theoretical here. `blog/public/brand/logo-email.png` was added (`b8c3dea`),
then replaced in place with a different variant (`85629a5`), and the old dark-on-lavender
mark kept being served no matter what the origin returned. The only fix was a rename to
`moi-mark-purple.png` (`b150873`). The colour icons in `17bcf5a` were added as new
filenames for the same reason.

So: **changing an email image means a new filename, every time.** Overwrite it and the
origin will be correct, the browser will show the new image, and the email will keep
showing the old one: a failure that verifies as fixed everywhere except where it matters.

Current assets and their intended display sizes (retina source, displayed smaller, correct
aspect ratio: the social assets are 2x/half, the header mark is 4x/quarter; set
`width`/`height` as attributes as well as inline styles, because Outlook ignores the CSS):

| File | Actual px | Displayed |
| --- | --- | --- |
| `brand/moi-mark-purple.png` | 160×123 | 39×30 in the header lockup |
| `brand/social/moi.png` | 62×48 | 31×24 |
| `brand/social/{x,linkedin,discord,telegram,github}.png` | 48×48 | 24×24 |
| `brand/social/{x,linkedin,discord,telegram,github}-colour.png` | 48×48 | 24×24 |

**`mailchimp-footer.html` currently references the monochrome icons** (`x.png`,
`linkedin.png`, …). Commit `17bcf5a` added the `-colour.png` set precisely because a single
purple tint "made the row read as five variations of one mark rather than five
destinations". The colours: X black, LinkedIn `#0A66C2`, Discord `#5865F2`, Telegram `#26A5E4`, GitHub
`#181717`, with the MOI mark staying purple and staying first. Before pasting the footer,
switch those five `src` values to the `-colour` filenames; leave `moi.png` alone.

## Plan and deliverability

*(Operational: Mailchimp account facts, unverifiable from the repo.)*

| | |
| --- | --- |
| Free tier (since 17 Feb 2026) | 250 contacts, 500 sends/month, 250/day |
| MOI list size | ~5,496 subscribers, well past free; a paid plan is required |

**Domain authentication is required, not recommended.** Google and Yahoo both enforce it
for bulk senders. Two CNAME records (DKIM) plus one TXT (DMARC), up to 48h to propagate;
Mailchimp's Entri flow automates it if the DNS provider is supported. Sending to thousands
from an unauthenticated domain is not a warning to dismiss: it is a deliverability
failure that shows up as a quietly collapsing open rate rather than as an error.
