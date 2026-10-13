# Slide plan

The order used at CC14, why, what earns a slide, and what stays off a public call. Facts are as of 2026-10-02. Deck mechanics (components, backgrounds, rendering) are in the deck branch (`moi-webinar/deck`) and are not repeated here. Back to `../GUIDE.md`.

## The order used at CC14 (12 slides)
The deck is `../examples/cc14/deck/index.html`. Every number is in `../examples/cc14/numbers-ledger.csv`.

| # | Title | Job | Source |
|---|---|---|---|
| 1 | Title | Name the call, the number and the month | Announcement copy; the previous operator's correction "campfire chat" |
| 2 | The September release | One new capability and two breaking changes | Protocol team's release note and the release post |
| 3 | Upgrading from August | The action required: versions, what to search for, what to rewrite | Release note; the old id and asset limits come from the release post only |
| 4 | DevRel | What the DevRel side is doing: MCP server, x402, the blog | The previous operator's own status |
| 5 | AI visibility | The baseline: visibility, citations, mentions | Dashboard screenshot, Scribble report |
| 6 | By engine | The same measure per AI engine | Dashboard screenshot |
| 7 | The questions | What people ask AI about MOI | Scribble report, section 3 |
| 8 | Content plan | What we publish in answer | Scribble report, section 6 |
| 9 | Community | Discord growth, Game Night, Pip | Sai Kiran's pointers; first-draft deck |
| 10 | Events | Futuremode, Taipei, with two real photos (empty frames in this library's copy) | Photos the previous operator supplied (not in this library, see `../examples/cc14/README.md`); the event's own site |
| 11 | What is next | Two cards: AI visibility, community and campaigns | Scribble report, section 10; first-draft deck |
| 12 | Close | Logo and one line: "Thanks for building with us." | The previous operator |

## Why this order
- Protocol and DevRel come first. That is the segment order agreed on 2026-08-24. During the 24 to 25 September 2026 edits the previous operator moved DevRel to slide 4, "after action required", so all developer material sits together before the marketing material.
- The visibility block follows the numbered sections of the Scribble report: baseline, engines, questions, content plan. Slide 4 ends on the blog, which leads into slide 5 ("what we publish is what the AI engines read back").
- Community and events follow, then what is next, then the close. The rule that urgent upgrade material goes first is inferred. The segment order itself is observed.
- CC14 was built from a 14-slide first draft in another design system. The final deck kept none of that design. See `../examples/cc14/README.md`.

## What earns a slide
1. A release gets its own slide only if it carries a breaking change, an action for the audience, or a concept that needs explaining. At CC13 the previous operator asked for a slide per package; at CC14 he cut the release to two slides.
2. The developer update is one or two slides. The new material gets the room (instruction of 2026-09-24).
3. One idea per slide. Three cards at most. Four stats at a push. A fourth card means two slides.
4. A figure earns a place only when its ledger row is `confirmed`, or the human has set it to `accepted-unverified`, and the operator can name the source aloud.
5. An event earns a slide only with real photos and one sourced line of fact.
6. A segment with no confirmed input gets no slide. Do not fill the space.
7. The close is the logo and one line. No recap bullets, no "Open Q&A".

## What stays off a public call
The first six rows were removed from CC14 during 23 to 25 September 2026 with no reason given. The remaining rows come from the incidents named in their Evidence column. The pattern is inferred. ASK: Rahul whether it is a standing rule.

| Leave off | Evidence |
|---|---|
| Competitor comparison | The "MOI versus Lit Protocol" slide was removed. A bullet for it stayed on slide 8 and in its notes |
| Metrics nobody has resolved | A campaign slide with a click-through of 0 was removed. The source report says the figure needs investigation. A bullet about it stayed on slide 11 |
| Third-party enterprise or tender stories | The Algix and MeitY slide was removed |
| A product update | The Proofly slide was removed |
| Per-engine up and down arrows | Removed from the engine tiles. The sentence quoting the movements stayed on slide 6 |
| A guest slide | The CC14 guest slide was removed before the call. The guest's title was never supplied and was left off. This does not bar guests: when one is confirmed, see "A guest" below |
| Event outcomes and who attended, without a source | The assistant declined to name Futuremode speakers or claim outcomes. One carried-over sentence about "the people we met there" has no source |
| Anything that mentions cancelled or internal plans | Standing rule from the 31 August 2026 corrections: public content never mentions them |
| A claim the network does not yet show | Source-only features are not live. See `release-slide-checks.md` |
| A release candidate described as shipped | Caught at CC13 |
| Live counts that go stale | The intro session (a Builders session deck, on the previous operator's machine only; ASK: Adithya for a copy) removed its stats row. The reason is inferred |
| A promise about a future call | The CC13 draft description named guests from Coinfest Asia, Bali for CC14. The CC14 deck had neither. Whether the draft was posted is unknown |

## A guest
A confirmed guest gets one slide, built from the deck branch's guest component (`moi-webinar/deck/references/guest-slide.md`): a large headshot, then name, role, company, company logo and topic. Place it where the guest speaks; at CC14 the draft put it after the updates and before the close. The inputs and file names are in `inputs-checklist.md`, "The guest slide". The worked example is slide 12 of `../examples/cc14/deck/index-guest.html`.

## Starting skeleton for the next call
A suggestion, not a rule. Delete any row with no confirmed input.

| # | Segment | Slides | Presenter | Minutes | Cue |
|---|---|---|---|---|---|
| 1 | Open | 1 | ASK: the host | 1 | |
| 2 | Protocol | 1 or 2 | The DevRel operator (as at CC14; confirm in the line-up) | words / 140 | Host question cue if one is planted |
| 3 | DevRel | 1 | The DevRel operator (as at CC14; confirm in the line-up) | words / 140 | |
| 4 | Marketing: visibility, community, events | as inputs allow | ASK: Sai Kiran | ASK | |
| 5 | What is next | 1 | ASK | 1 | |
| 5a | Guest, if confirmed | 1 | The guest | ASK: Vardan | Host hands over |
| 6 | Close | 1 | The host | 0.5 | |

Minutes come from the script: words divided by 140 (a pace inferred from CC14, check it by reading aloud once). CC14 notes ran 1,091 words, about 8 minutes of script, and slides 2 to 4 (the previous operator's) ran 560 words, about 4 minutes. The length of the call is not on record. This table is the run-of-show the KRA document asks for. ASK: Rahul whether a separate document is still required.

## Not yet known
- Whether the call has a fixed length. ASK: Vardan.
- Whether a product, research or partnership slot exists for the next call. ASK: Rahul.
- Whether the "what stays off" pattern is a rule. ASK: Rahul.
