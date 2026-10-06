# Polish passes

Facts are as of 2026-10-02. These are the passes the previous operator ran on the August and September release posts and on session write-ups, in the order they ran. A post that misstates the protocol is worse than no post, so polish never changes the meaning of a claim that was checked. Back to `../SKILL.md`.

## Order
| # | Pass | What it does | Notes |
|---|---|---|---|
| 1 | Facts first | The claim check (`SKILL.md` step 4) is finished before polish starts. After a rewrite that changes a claim, check that claim again | In September, 86 changed claims each got a checker and a refuter (PR #53 body) |
| 2 | Read-alone test | Every sentence has to make sense on its own, and every X and LinkedIn post has to stand alone | Asked for on every sentence of the 2026-09-10 release pack |
| 3 | Plain-language pass | Short sentences, one point per paragraph, a term defined before it is used, the thing named, no universal | The September commit sequence reads "release post in plain language", "split three long sentences", "one point per paragraph" |
| 4 | humanizer | Removes AI-sounding patterns paragraph by paragraph | Optional helper. "After every paragraph" for a release post (2026-09-11) |
| 5 | stop-slop | A second pass on the same patterns | Optional helper. On 2026-09-11 the instruction was to apply all its suggestions but the first. On the last pass, identify only and change nothing |
| 6 | Variants | When wording is contested, show A (stop-slop only), B (humanizer only), C (both) and let the operator pick | 2026-09-01: the previous operator picked A |
| 7 | Readability read | Could a newcomer who has never read the docs follow it? The August jury scored 61, then 87 after first-use glosses | Sub-agents only if the operator asks, and the count stated first. Otherwise do it inline with the checklist below |
| 8 | Search check | Summary, takeaways, FAQ, question H2s, backlinks, absolute sibling URLs | `geo.md`. Identify only when asked |
| 9 | Lint | `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" <post>` and `python3 "$SKILLS/moi-blog/scripts/post-lint.py" --strict <post>` | Zero errors. A warning is a prompt to look |
| 10 | Re-read the opener and the KMOI and anu sections | After every automated pass | 2026-09-11: passes kept bringing back vague phrasing the previous operator had already rejected |
| 11 | The operator reads it once on the preview URL | Only then does it go to review | Nothing leaves the machine before this |
The last stop-slop commit on the September post made "active voice in ten places, one rhetorical question turned into a statement, one meta-joiner dropped" (`280ffb2`). More passes after the operator's read-through kept reintroducing earlier rejections, so stop when the lint is clean and the opener still reads right.

## humanizer and stop-slop are optional
Both are separate skills that may not be installed on your machine, and this library does not include them. Check with `ls ~/.claude/skills`. If they are missing, apply the rules below by hand. If they are present, run them as passes 4 and 5.
Conflict resolved: humanizer says to keep em dashes at the rate of the writer's sample, and stop-slop bans them. The posts have 77, 17, 1, 0, 0 and 0 em dashes, the last two posts have none, and the previous operator's rule for posts and social copy is none (2026-09-10). Use none.

## The rules, without any helper
MOI rules first. These each came from a correction, with its date.
| Do not write | Why | Write |
|---|---|---|
| "Every action on MOI costs fuel" | A universal the protocol does not guarantee (2026-09-11) | What this release changes: "You can now pay fuel for another user." <!-- slop-lint:ignore --> |
| "Fuel is the fee for using the MOI network" in the opener | Removed from the opener (2026-09-11) | Define fuel where it is first needed <!-- slop-lint:ignore --> |
| "the token", "MOI's own token", "the fee" | The strongest complaints of the session (2026-09-11) | KMOI, fuel, fee payer, fee delegation <!-- slop-lint:ignore --> |
| "a native asset standard made for KMOI alone" | Sounds right and is not backed by the note (2026-09-11) | The note's words: "KMOI now uses MASN, a new native asset standard." |
| "Most teams quietly accept both" | Vague attribution (2026-08-31) | Cut it, or name the checked fact and its source <!-- slop-lint:ignore --> |
| "and it is the part worth caring about" | Called AI slop (2026-09-01) | Delete the clause <!-- slop-lint:ignore --> |
| "not this, not that", "it is not X, it is Y" | A contrast frame (2026-09-04) | Say what is true, directly <!-- slop-lint:ignore --> |
| "none of which we configured" | Misleading framing (2026-08-08) | Say precisely what the reader has <!-- slop-lint:ignore --> |
| "nobody holds your money", "only the owner can move funds" | Proved false by the session 7 check (2026-08-07) | "Value moves only under the holder's own signature, and our agents never grant one." |
| "Off chain, the service owns the row" | Jargon (2026-09-01) | "The data sits in an entry in the app's backend service." |
| A built-in error name or "86 fuel" on social | Implementation trivia (2026-08-31) | Leave it out |
| "Voyage devnet" | Voyage is the explorer (2026-09-25) | devnet <!-- slop-lint:ignore --> |
General patterns to remove, in the order they matter for this audience:
1. Inflated importance: "marks a pivotal moment", "a testament to", "underscores". State the plain fact.
2. Sales language: "stunning", "groundbreaking", "breathtaking", "game-changer". Say what it does.
3. Vague sources: "experts say", "studies show", "industry reports". Name the source or cut the sentence. <!-- slop-lint:ignore -->
4. Tail phrases that add depth to nothing: "..., highlighting the importance of ...", "..., ensuring that ...".
5. Stock words used in clusters: delve, landscape (abstract), tapestry, pivotal, crucial, vibrant, showcase, underscore, testament.
6. Forced groups of three and "from X to Y" ranges that list nothing real.
7. Contrast frames and clipped negative endings ("No guesswork. No friction.").
8. Throat-clearing and announcements: "Here's the thing", "Let me be clear", "It turns out", "In this post we will".
9. Passive voice with no actor, and things doing human verbs ("the decision emerges"). Name the actor.
10. Adverbs and softeners: "really", "just", and any -ly word that adds nothing. Qualifiers stacked on one claim.
11. Em dashes (none), bold sprinkled through paragraphs, Title Case headings, emoji.
12. Chatbot leftovers: "I hope this helps", "As an AI", offers to continue.
13. Generic positive endings: "the future looks bright". End on the last real sentence.
14. Meta-joiners: "the rest of this post", "as we will see". Delete them and let the post move.
15. Rhythm: three sentences of the same length in a row, or every paragraph ending on a punchy one-liner. Vary both.
Keep every claim, add no fact, and keep deliberate human detail (a stated limit, an honest "this is not finished" section).

## The read-alone and newcomer checklist
- Open the post at its first paragraph. Is the first sentence the claim?
- For each protocol term: is it defined at first use, in one line, in MOI context?
- For each sentence: which source line supports it? If none, it is a claim for the ledger.
- For each number: is it copied from the source, and is it dated?
- For each "live", "shipped" or "now": was it read from the node or the tag on a stated date?
- For each X and LinkedIn post: no backticks, no bold markers, no emoji, no placeholder, one link.

## Not yet known
- Whether the "all but the first" stop-slop instruction of 2026-09-11 is a standing rule. Treat it as that day's choice.
- A budget for the readability jury. Only a credit-cost concern is recorded. ASK: Rahul.
