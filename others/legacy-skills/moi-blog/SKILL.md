---
name: moi-blog
description: Working on MOI's blog (blog.moi.technology) — writing or editing a post, shipping it, announcing it to X, LinkedIn, Discord and Telegram through Buffer, running the Mailchimp RSS newsletter, or checking GEO/schema/UTM measurement. Use for anything under blog/, social/, scripts/distribute.js, or the Mailchimp campaign templates.
---

# MOI blog

Three systems that touch the same Markdown files and are otherwise independent.

**Publish** is a PR into `blog/src/content/posts/`; merging to `main` deploys and announces nothing.
**Distribute** is a copy file a human writes plus a workflow a human triggers. It never reaches a
timeline by itself: Discord and Telegram post immediately, X and LinkedIn stop at a Buffer draft that
a person opens and publishes. **The newsletter** is outside both — Mailchimp polls `/rss-email.xml` on
its own schedule with no code, no secret and no CI step on our side.

## End to end

| # | Do | Where |
| --- | --- | --- |
| 1 | Write the post, frontmatter first | `blog/src/content/posts/<slug>.md` |
| 2 | Validate and read it | `npm run build --prefix blog` (zod-validates), `npm run dev --prefix blog` → :4321 |
| 3 | Check the apex listing card | `npm run dev` at the root → :5173/blog. `public/blog/` and `public/covers/` are gitignored build output — nothing to commit |
| 4 | Open the PR, verify on the preview | `https://pr-<N>-blog.preview.moi.technology/article/<slug>/`. Same host serves `/rss-email.xml` — the safe end-to-end rehearsal for a newsletter change |
| 5 | Merge → live | `deploy.yml` (Teleport → VM). Post is public. Nothing has been sent |
| 6 | Merge also opens *Prepare social copy* | PR adding `social/<slug>.md`. Rewrite all four blocks by hand, merge it |
| 7 | Announce | Actions → **Distribute a post** → slug, channels, `dry_run: true`, then re-run with `false` |
| 8 | Finish the last mile | `publish.buffer.com` → channel → Drafts: add an image (the API attaches none), rewrite the hook, publish |
| 9 | Measure | `npm run social:links <slug> -- --md` for tagged links; GA4 by `utm_campaign=<slug>`; Search Console **blog** property |

Steps 6 and 7 are ordered: `distribute.yml` checks out `main`, so running it before the Prepare PR
merges dies with `No copy file at social/<slug>.md`.

## Which module

| Doing | Read |
| --- | --- |
| Writing or editing a post — frontmatter contract, what consumes each field, body shape, voice, protocol-claim verification | `references/authoring.md` |
| Announcing — the copy file format, channels and limits, `{{link}}`, UTM tagging, both workflows, local dry runs, secrets | `references/distribution.md` |
| Buffer itself — GraphQL shape, channel IDs, the draft guarantee, setup checklist, error-by-error troubleshooting | `references/buffer.md` |
| Newsletter — the two feeds, building the RSS campaign, the three-part template set, signup form, deliverability | `references/mailchimp.md` |
| Schema, robots, sitemap, `llms.txt`, GTM/GA4 wiring, the publish checklist | `references/geo.md` |
| Logos, covers and `og:image`, email image rules, rasterising SVG → PNG | `references/assets.md` |

Campaign HTML lives beside the modules: paste `mailchimp-header.html`, `mailchimp-body.html` and
`mailchimp-footer.html` into Mailchimp's Header / RSS-items / Footer code blocks. They declare only
`width="100%"`, so set the designer's content width (600px) and page background (`#fcfbff`) yourself.
`mailchimp-template.html` is the earlier single-file draft, kept only as the worked example of the
foster-parenting bug — do not paste it.

## Load-bearing facts

Each of these fails silently rather than loudly.

- **Two builds, two hosts.** Only the blog build validates; the root build parses frontmatter with
  `gray-matter`, writes `undefined` into a listing card and exits 0. Run both or the post is
  live-but-unlisted, or listed-and-404ing.
- **Distribute has no idempotency.** Re-running it posts to Discord and Telegram a second time and
  creates a second Buffer draft. The `dry_run: true` default is the only guard, and the repo has no
  undo — clean up by hand in Buffer (its schema exposes `deletePost`/`editPost`; nothing here calls them).
- **`social-prepare.yml` dispatched with `force: true` and a blank slug** resolves to `--all --force`
  and regenerates every published post's copy file, overwriting hand-written copy without asking.
  Always fill in the slug.
- **`utm_campaign` is always the slug, lowercase, everywhere.** GA4 files `LinkedIn` and `linkedin` as
  two channels; Mailchimp's own Google Analytics option renames `utm_campaign` after the campaign and
  looks correct while breaking every cross-channel comparison. Adding a channel to
  `scripts/lib/social.js` whose `utm` value is not also in `blog/src/lib/utm.js` throws at send time,
  not at validation.
- **Email and social images are cached by URL forever.** Mailchimp offers no purge and LinkedIn sticks
  a broken card to the URL. Change an image means a new filename, every time — and deploy the image
  before pasting a template, since every `src` in the set is an absolute
  `https://blog.moi.technology/brand/…` URL that 404s until `deploy.yml` has run.
- **Three checked-in guides are stale; trust the code.** `CONTENT.md`, `DEPLOYMENT.md:100-118` and
  `blog/README.md` all describe the blog wrongly. The README calls it cream/ink/purple
  (`#F5F3EE`/`#1A1A1A`/`#7B5EA7`) — that is the *marketing site's* palette from `CLAUDE.md`. Those
  three hexes appear in no blog stylesheet; the real tokens are `--moi-main #4b17e5`,
  `--ink #0a051a`, `--bg #fcfbff`, Poppins. The README also still claims `blog.moi.technology`
  needs a DNS record and a TLS certificate before it resolves.
- **Never copy the documented figure example.** `CONTENT.md:188`, `DEPLOYMENT.md:103` and
  `blog/README.md:23` all point at `![…](../../assets/agent-flow.svg)`. That file exists, is
  referenced by no post, and is the one place those old hexes survive — drawn cream/ink/purple in
  DM Mono. Copying it embeds an off-brand diagram in a `#4b17e5` Poppins page and the build says
  nothing. Real convention: a per-post subdirectory of `blog/src/assets/`.
- **Corpus conventions the schema does not enforce.** `takeaways` is exactly 8 items or absent
  entirely; `faq` runs 7–13 and drives a full `FAQPage` JSON-LD block (`CONTENT.md`'s "2-4 questions"
  is wrong by 3–6×). Sibling posts are linked by absolute `https://blog.moi.technology/article/<slug>/`
  URLs, so body links in a preview go to production too. Every article ends with `<Subscribe />`,
  which injects an `<h2>` after the FAQ — the post's own last section is never the last thing on the page.

## The repo

`github.com/sarvalabs/MOI-Website`, branch `main`. Work in any fresh clone of it; every path in the
modules is relative to the repo root. On the author's Mac the current clone is
`~/untitled folder 10/MOI-Website` — the older copies (`~/mw/MOI-Website`, `~/MOIWB` and the
`compare-repos-main` worktree this skill was written in) are stale and should not be edited. The blog is a separate Astro build under `blog/` with its own `package.json`; distribution
scripts (`social:init`, `distribute`, `social:links`, `buffer:channels`) are root scripts.
