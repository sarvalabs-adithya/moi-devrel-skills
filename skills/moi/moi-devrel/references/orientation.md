# Orientation: what MOI DevRel does

Facts are as of 2026-10-02, with the changes of 13 October 2026 marked. Evidence: the research behind this library (in the handover repo's git history), Google Drive, the repos and the handover docs in `project-handover-docs/`. Back to `../SKILL.md`.

## In plain words
- MOI has two current one-liners, "The participant layer for AI agents" (docs standard) and "on-chain authority for the agentic economy" (website headline from the May to June 2026 redesign), and two more lines in use that nobody has classified (`terminology.md`, table D). ASK: Rahul which one leads where.
- Sarva Labs designs and builds MOI. The MOI Foundation governs the protocol.
- Past blog posts were signed "Ecosystem, Sarva Labs" and one tutorial "DevRel" (the byline policy is open, see `house-style.md`). The KRAs (Drive, January 2026) set two public events a month and these timings: run-of-show and speaker brief 48 hours before a call, notes and recording within 24 hours after, Q&A log with owners within 48 hours.
- The work falls into four groups:
 1. Tell people what shipped: community call, release posts, blog, social, newsletter, docs.
 2. Teach developers to build: Builders webinars, Forge, awesome-moi, docs.
 3. Keep working the products the previous operator built or ran: Launchpad, Explorer, MCP server, website, Dataroom, Points Program, demo repos. Whether DevRel now owns them is not settled. ASK: Rahul.
 4. Standards: x402 and the CASA namespace.

## The work ranked by how often it came up
Ranked by how often each job came up in the previous operator's request history as of 2026-10-02. Categories overlap. Rows 1 to 4 are modes that run through every other job.

| # | Job | Skill or branch (the routing tables are in `../SKILL.md`) |
|---|---|---|
| 1 | Explain a mechanism before building or presenting | `moi-devrel/explain` (`glossary.md`) |
| 2 | Ship: commit, PR, rebase, merge, deploy, preview | `moi-devrel/ship` |
| 3 | Status and what is left | `moi-devrel` (the hand-back format in `../SKILL.md`; a status to Rahul is `house-style.md` section 4) |
| 4 | Keys, env vars, where a value goes | `moi-devrel` (`keys-and-access.md`, `keys-by-product.md`) |
| 5 | Blog and long-form writing, publishing | `moi-blog` |
| 6 | Verify claims, "are you sure" | `moi-devrel/claim-check` |
| 7 | Decks, scripts, webinar run-of-show | `moi-webinar`, `moi-webinar/deck`, `moi-webinar/community-call` |
| 8 | x402, CASA and CAIP-2 submissions | `moi-standards-submission` |
| 9 | Test plans and rounds, then fixes | `moi-devrel/test-round` |
| 10 | Messages to and about people | `moi-devrel` (`house-style.md` section 4, `../templates/messages.md`); `moi-devrel/call-digest` for a call transcript |
| 11 | Social posts through Buffer | `moi-blog`, `moi-blog/release-pack`, `moi-webinar` |
| 12 | GEO, SEO and the docs standard | `moi-docs`, `moi-docs/geo` |
| 13 | Git identity and authorship fixes | `moi-devrel/ship` (`consent-and-identity.md` section 2) |
| 14 | Model and credit spend | `moi-devrel` (house rule 7) |
| 15 | Newsletter (Mailchimp) | `moi-blog` |
| 16 | Handover and skill packaging | `moi-devrel` (this library, `../SKILL.md`) |
| 17 | Product stats lookups | `moi-launchpad-ops`, `moi-launchpad-ops/explorer`, `moi-mcp-ops`, `moi-web-products-ops` |

The library has ten skills and eleven branches as of 2026-10-04, and `../SKILL.md` routes to every one of them. Six branches live inside `moi-devrel`. Recurring jobs the log does not rank have a home too: a devnet reset (`moi-devnet-reset`), a protocol release (`moi-blog/release-pack`), brand and visuals (`moi-devrel/design`), the monthly call (`moi-webinar/community-call`) and the education programmes (`moi-education-programs`).

Reading it: most of the work is explaining, approving and shipping. The recurring outputs are blogs, decks, scripts and posts. The recurring risks are unverified claims, wrong git identity, spend and pushing too early.

## Programmes DevRel owns or touches (Drive, MOI Programs sheet, as of early 2026)
| Programme | Owner in the sheet | What |
|---|---|---|
| MOI Community Updates | Adithya | one community call and one X AMA a month |
| MOI Forge, Advance | Adithya | campus cohort, 12 weeks; KPIs: 1 project onboarded a month, 1 demo day a month |
| MOI Forge, Basic | Sai Kiran | campus roadshow and logistics |
| MOI DevX monthly hackathon | Adithya | challenge track (MOI Sprint, its other track, was scratched 13 October 2026) |
| Tech Spotlight, podcast, Galxe, KOL outreach | Rahul, Vardan, Harsh, Vardan and Louis | owned by others in the sheet; context only |
The owners are the sheet's, as of early 2026, and Adithya hands over on 14 October 2026. Which programmes are still active, and who takes each, is not known. ASK: Rahul. The skill for them is `moi-education-programs`.

## What the DevRel operator inherits
Observed state, with the pointers: six products with live URLs and open PRs (`repo-map.md`), a call and AMA rhythm (`calendar.md`), accounts whose owners are mostly unconfirmed (`keys-and-access.md`), and a devnet that was wiped on 2026-08-15 and again around 2026-09-11, the second wipe announced for 00:00 UTC on 11 September and not confirmed to the minute (`devnet.md`). Decks for calls 2 to 14 are in `moi-foundation/MOI-Webinars` under `community-call-N/deck/` (PR #2, merged 13 October 2026), and the intro-session deck is in the handover repo (`skills/moi/moi-webinar/past-sessions/intro-session-deck/`). Other work may still exist only on the previous operator's machine, as read on 2026-10-03: 6 local commits unpushed (one of them, 27efaa3 with 11 files, holds part of `protocol-release-0.13.0/`, and 3 more files of it are untracked; the other 5 are x402 and `buffer.mjs` work), edits to the x402 review package (a copy is in the handover repo, `skills/moi/moi-standards-submission/x402-review-package/`), and unpushed MCP work. Whether any of it has been pushed since is not recorded (the previous DevRel's notes); check `git log` and `gh` on each repo, then ASK: Rahul. Before you touch a product's admin, read that product's row in `repo-map.md`.

## First week (proposed; built from the observed jobs)
| Day | Do | Done when |
|---|---|---|
| 1 | Read `SKILL.md`, `house-style.md`, `consent-and-identity.md`, `terminology.md`. Install tools (`environment.md`). Set `PREFLIGHT_WORK_DOMAINS` and `PREFLIGHT_EXPECT_GH_LOGIN`, then run `bash "$SKILLS/moi-devrel/scripts/preflight.sh"` from inside a repo (`$SKILLS` is defined in `../SKILL.md`). Ask the access owner for the names in `keys-and-access.md`. | Preflight passes and the access list is requested. |
| 2 | Open every live URL in `repo-map.md`. Run the read-only health checks for the website, Dataroom, Points and `launchpad.moi.technology/api/stats`. Compare with the "as of" list. | You can say where each product deploys from and who to ask. |
| 3 | Read `glossary.md` and the docs pages named in `terminology.md`. Read the latest release post at blog.moi.technology. The operator writes five sentences about MOI in their own words and Claude marks each one against the glossary (`moi-devrel/explain`). | Every sentence is marked right or fixed. |
| 4 | Read `calendar.md`. Find the next community call date in the Drive sheet "Community Call + AMA Calender 2026" and confirm it with Rahul or marketing. Read the `session-8-policies/` pack to see what a webinar pack holds (it is on branch `claude/agent-payments-simple` of `moi-foundation/MOI-Webinars`, not `main`, and its gitignored files were local to the previous operator and are not recorded elsewhere (the previous DevRel's notes); ASK: Vardan for the Luma page text). | You know the next three dated events and who runs each. |
| 5 | One supervised task, local only: claim-check one published post against source, or check the links in `moi-foundation/awesome-moi` (last checked in January). Hand back in the standard format. | A hand-back exists. No PR is opened without a yes. |

## Working rules
- Accept a one-word yes for the one action it names. A pick from your menu covers that pick.
- When the operator says they are away and for how long, keep working and hold questions. Stop before anything irreversible or visible.
- Edit only the sentence the operator points at. Offer a way to see the previous version.
- Show real output. "Run it", a preview link or an opened file beats a description.
- Define jargon on first use, in MOI terms. Generic analogies (a payments-company comparison, for example) were rejected in favour of MOI context.

## Not yet known
- Which of the product apps (Launchpad, Explorer, MCP, Dataroom, Points) belong to DevRel and which to product engineering. The previous operator built and ran them. ASK: Rahul.
- Rahul's title and what he formally approves. ASK: Rahul.
- Whether the Forge 12-week cohort is real, planned or abandoned. ASK: Rahul or Sai Kiran.
- How long each process takes. The request history holds no durations.
