# The release post: what it holds and what earned its place

The release post is a blog post, "MOI <Month> 2026 Release", published on `blog.moi.technology`. This file holds what is specific to a release post. How to write a post in the house style, the frontmatter contract, the publish pull request, announcing it and the newsletter are in `moi-blog`: `moi-blog/references/authoring.md`, `moi-blog/references/geo.md` and `moi-blog/references/distribution.md`. Facts are as of 2026-10-02. `ASK:` is defined in `moi-devrel/SKILL.md`. Back to `../GUIDE.md`.

## What is on record
| | August 2026 | September 2026 |
|---|---|---|
| Slug and title | `moi-august-2026-release`. The title first led with the version and was changed to lead with the month | `moi-september-2026-release`, "MOI September 2026 Release: fee delegation, a new KMOI asset id, and prices in anu" |
| Pull request | #36 of `sarvalabs/MOI-Website`, merged 2026-08-21, about 2.5 days and more than 30 commits | #53, opened 2026-09-10 13:26 UTC and merged 2026-09-11 13:04 UTC, 24 commits |
| Shape | Per-package subsections, an operator section and an op-code table. The research counts 12 component versions in it | The structure below |
Cadence is monthly (`project-handover-docs/BLOG.md`). No October date is on record. ASK: Rahul.
Names: slug `moi-<month>-<year>-release`. File `blog/src/content/posts/<slug>.md`. The scaffold copies `moi-blog/templates/release-post-skeleton.md` into `protocol-release-<version>/BLOG.md`: that skeleton, `moi-blog/scripts/post-lint.py` and `moi-blog/references/authoring.md` decide the frontmatter, the title and summary lengths and the placeholder style (as of 2026-10-02 the lint warns above 60 characters of title and outside 130 to 170 of summary, and the September title is 82 characters and its summary 240). Only the rules specific to a release post are kept in this file. The skeleton shows one takeaway and one FAQ stub: a release post writes exactly 8 takeaways and at least 7 FAQ entries (see the frontmatter line below).

## Before writing
- The note, saved and hashed (`the-note.md`), and the ledger started (step 3 of `../GUIDE.md`).
- For every component: its GitHub release page and tag. August had 12 component versions.
- Tagged source for each claim. go-moi and go-pisa are private. ASK: Gokul for read access. A private path never appears in public text. Until you have access, mark post-only claims `unverified`.
- The previous release post, as the sibling in style. The live node, if the post says "live".
- Docs links for the how, so the post stays high level.

## The structure that shipped in September
| Part | What it holds | Why it earned its place |
|---|---|---|
| Bold opening sentence | What a developer can now do: "You can now pay fuel for another user." | Three earlier openings were rejected: too abstract, a vague noun ("the fee"), an overgeneralisation. Fuel is not defined in the opener <!-- slop-lint:ignore --> |
| Second paragraph | The new capability, then "Outside of that, there are three breaking changes", then each named, then "Each of these is covered in detail later in this post." | The reader learns what breaks before the detail |
| Status line | What moipod is, the version, and "live ... since 11 September 2026" | "Live" only after a node read. See `timing.md` |
| Four-term glossary | Interaction, fuel, participant, logic | A term is defined before use and then used the same way. The participant line is contested (`traps.md`) |
| `What changed in moipod v0.13.0?` | A table: Change, What you get, Can it break your code? Then the SDK versions | A reader who scans gets the whole release |
| One question heading per change | What is fee delegation, what changed for KMOI, why price in anu, what changed in the participant list. Each opens with a bold claim | Question headings serve search and AI citation (`moi-blog` `geo.md`) |
| Two short code samples | The fee payer flow in three steps, and `parseKmoi` and `formatKmoi`. A third block shows the new asset id | The post stays high level and links the docs for the rest. PR #53 records both samples as checked against the published SDK |
| `What do developers need to change?` | Numbered breakages, the most likely first, then updates worth making | The reader's action list |
| `Everything shipped` | A table of component, exact version, what it carries | Exact versions in one place |
| `What to do now` | An ordered runbook that starts with the `npm i` line | The reader can act without reading the rest |
| `Key takeaways, recap` | Bullets with a bold lead clause | Closes the post. Do not add `<Subscribe />`: the page already renders the signup form, the tag is inert in a `.md` file and `moi-blog`'s lint warns on it. The September post has one stray |
Frontmatter in September: `title`, `summary` (kept short, it feeds the meta description), `date` (the day it goes live, 2026-09-11), `author`, `tags` (`protocol, native-assets, release, moipod, fee-delegation, kmoi`), exactly 8 `takeaways`, 7 `faq` entries (the six posts on main have 7 to 17), `draft: false`, no cover. The contract is `moi-blog` `references/authoring.md`.

## Rules for a release post
1. Open with what the developer can now do. Benefit first, minimal code, a link for the how.
2. Plain words, short sentences, one point per paragraph.
3. Name the thing. KMOI is "the native token of the MOI network, like ETH on Ethereum", counted in anu the way Ethereum counts ETH in wei. Fee delegation is the feature, fee payer the role, fuel what is paid. Capped supply, never "fixed supply". <!-- slop-lint:ignore -->
4. State no universal. "Every action on MOI costs fuel" was removed twice (2026-09-11). Say what the fee payer covers and what it does not. It covers fuel only, and the sender still funds any value it sends. <!-- slop-lint:ignore -->
5. Keep a release candidate as tagged (`0.9.0-rc2`) with no sentence about release candidates. Tell readers to update only to a version the operator confirmed with the protocol team.
6. No pictures and no cover. No em dash and no HTML comment (PR #53 states both). September has none. August had 17 em dashes.
7. Cut what the operator cuts. The agents section and the x402 paragraph were removed in September. A release post makes no x402 integration claim.
8. Say what each count counts. September has three breaking changes, four changes and five things that break, and the post does not explain why the counts differ.
9. Terminology is in `moi-devrel/references/terminology.md`. Run `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" protocol-release-<version>/BLOG.md` on the draft.

## The ledger for the post
- Source order: tagged source, then the note, then docs.moi.technology. The docs are weakest: their op-code numbers were swapped in August.
- A claim that rests only on the note is softened, as on 2026-09-11. Where the note and source disagree and nobody has ruled, word the post so it contradicts neither and raise the difference separately.
- For "live on devnet", read the node (`moi-devrel/references/devnet.md`).
- PR #53 records an independent first pass of 200 claims (187 true, 8 partly, 5 unverifiable, 0 false) and a second pass of 86 changed claims. A commit message in it records a sweep of 152 claims and three corrections. Those are the previous operator's numbers. They are not re-verified here.
- Sub-agents for a claim run only when the operator asks, with the count and the model said first.

## The pull request
The `moi-blog` run table (`moi-blog/SKILL.md`, steps 7 and 8) opens it. Opening it, merging it and pushing are gates. PR #53's body is the model: Summary (who it is for, the framing, the slug and URL), Shape (word count, headings, takeaways, FAQ, runbook), Verification (what was checked against which tags and packages, how many claims, build results), "Before marking ready" checkboxes (confirm the go-live date, internal review by Rahul) and "Nothing is announced by merging". The preview is `https://pr-<N>-blog.preview.moi.technology/article/<slug>/`. To compare an earlier draft with the current one, open a preview-only PR of the earlier commit, as PR #55 did, and close it after. No attribution line goes in a commit or a PR body.

## After the merge
Merging deploys the post and announces nothing. Steps 9 and 10 of `moi-blog/SKILL.md` run Prepare and Distribute and the newsletter. Follow the copy PR to its end: for September it was #56, closed without merging (read 13 October 2026).

## Defects in the September post
`../examples/v0.13.0/README.md` lists them with line numbers. Do not copy: "Voyage devnet", "Participant: an account on MOI", "a native asset standard made for KMOI alone", "not save a setting, not call your logic", the flat "an account with no KMOI could do nothing" (the CC14 script's version of it was rated OVERSTATED in `moi-webinar/community-call/references/release-slide-checks.md`). <!-- slop-lint:ignore -->

## Not yet known
- The byline: "Adithya Ganesh, Ecosystem, Sarva Labs" in September, "Sarva Labs, Engineering" in August. ASK: Rahul.
- Whether the post is amended after publication, and whether the retired wording in the live September post changes. ASK: Rahul.
- Who confirms the go-live date. The "Confirm the go-live date" box in PR #53 names no owner. ASK: Rahul.
- Whether Medium is still a channel. ASK: Rahul.
