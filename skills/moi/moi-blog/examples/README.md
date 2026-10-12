# Example: the September 2026 release post, cleaned

`moi-september-2026-release.md` here is the release post for moipod v0.13.0 with the defects that came to light afterwards corrected. Read it as a model of the form. Back to `../SKILL.md`. Facts are as of 2026-10-02.

## Where it comes from
- The published post: `blog/src/content/posts/moi-september-2026-release.md` on `main` of `sarvalabs/MOI-Website` (commit `5e91afa`). It was merged as PR #53 on 2026-09-11 at 13:04 UTC, after 24 commits that landed as one. The byline as published is Adithya Ganesh, Ecosystem, Sarva Labs, and the byline policy is open (ASK: Rahul).
- The published post still carries the wording corrected here. This copy is not an amendment. Whether the published post is amended is not decided. ASK: Rahul.
- Do not reuse its facts or its byline. The facts are the post's, checked by the previous operator before publication (200 claims in the first independent pass, 86 re-checked after the rewrite, per the PR body) and not re-verified by this library, except as the last section says. The byline is the published one. Whose name goes on a new post is not settled (ASK: Rahul).
- Source for the corrections: the wording rules in `moi-devrel/references/terminology.md`, the lint rules, and the claim checks recorded in `moi-webinar/community-call/references/release-slide-checks.md`.

## What was good: keep it
- The opening is what the developer can now do: "You can now pay fuel for another user." Three earlier openers were rejected, in turn, as abstract, vague and over-general.
- The second paragraph says how many changes break code and names them before the post explains any of them.
- Four terms are defined in one list near the top, in MOI context.
- One table answers "can it break your code?" for each change.
- Six of nine H2s are questions, each answered in its first sentence. The recap section and the `takeaways` box are both written.
- Exact versions appear in a table, `0.9.0-rc2` stays as tagged with no sentence explaining a release candidate, and the runbook starts with the install line.
- One code sample of three calls, and the docs link for the rest. No pictures, no cover, no HTML comments, no em dashes.
- Eight takeaways and seven FAQ entries, each written to stand alone because it goes verbatim into the `FAQPage` JSON-LD.
- It was checked against source before it was merged: the node code at the release tags and the published SDK package. The notes were treated as a lead.

## What was corrected in this copy
The published version has 3 errors and 5 warnings under `post-lint.py` with `--repo` pointing at a clone (run on 2026-10-02). This copy has none of them in `--strict` mode. Outside a clone it prints one honest warning, `siblings-not-checked`, because it links to other posts and has no clone to check them against.
| Published post | This copy | Why |
|---|---|---|
| Title of 82 characters | 58 characters: "MOI September 2026 Release: fee delegation and anu pricing" | The docs standard says up to 60. The title tag adds a separator and "MOI Blog" |
| Summary of 240 characters | 164 characters, and it says "live on devnet" | The summary is the meta description. A reviewer fix in PR #53 had already shortened it once |
| "Live on Voyage devnet since 11 September 2026" in a takeaway and in the opening paragraph, linked to the explorer | "live on devnet", with no date | Voyage is the explorer, not the network (2026-09-25). `slop-lint.sh` reports an error. A read of the node shows now, never since (see the first item under "still open") <!-- slop-lint:ignore --> |
| Glossary: "Participant: an account on MOI. Every user has one." | "a person, a company or an agent. Its state is held in an account." | Contested since the 2026-09-14 correction. The safe form is in `terminology.md` <!-- slop-lint:ignore --> |
| Glossary: "Fuel: the fee for running an interaction" | "what an interaction costs to run, paid in KMOI" | One word per concept: fuel is what is paid, fee payer is the role <!-- slop-lint:ignore --> |
| "Before v0.13.0, an account with no KMOI could do nothing: not save a setting, not call your logic ... The user never sees fuel." | "A new user does not need KMOI to pay fuel ... Fuel is all the payer covers." | A contrast frame, which the lint rejects. The universal was rated overstated in the CC14 checks, and the same lines were removed from the call script on 2026-09-25 <!-- slop-lint:ignore --> |
| "It runs on MASN, a native asset standard made for KMOI alone." | "It uses MASN, a new native asset standard." | The release note says "KMOI now uses MASN, a new native asset standard." The other wording was recorded as a claim that sounds right and is not backed (2026-09-11) |
| Recap: "One funded account signing as payer is the whole setup." | "... covers the fuel." | The payer covers fuel and nothing else, which the post's own FAQ says |
| "Five things break" | "Five places in your code can break" | The post counts three breaking changes, four changes and five things. Each now says what it counts |
| A 66-character asset id in a code block and in a FAQ answer | `0x1080fffe4cd973c4...` and a note to import `KMOI_ASSET_ID` | The id is a public constant, checked on 2026-10-02: it equals `KMOI_ASSET_ID` at tag `v0.9.0-rc2` of `sarvalabs/js-moi-sdk`. A long hex literal looks like a key, and constants come from the SDK, never from a post |
| `<Subscribe />` as the last line | Removed | The article page renders the form. In a `.md` file the tag is inert |

## What is still open
- "Since 11 September 2026" is not settled, so this copy says only "live on devnet". `moi-devrel/references/devnet.md` records the upgrade at 00:00 UTC on 11 September and `net.Version` read 0.13.0 on 2026-10-02, but a read on 2026-10-02 dated the node's oldest interactions at 2026-09-10 13:18 UTC, before that moment (`moi-devrel/claim-check/references/live-reads.md`). The field name on the wire after the wipe (`payer` or `fee_payer`) is not on record either. Write "since <date>" only when the protocol team has confirmed that moment. ASK: Gokul when devnet moved to v0.13.0.
- The merged PR left two boxes unchecked: the go-live date against the go-moi tag date (10 September), and the internal review.
- Some claims are in the post and not in the release note: the old id to search for, the rule on max supply and decimals, and what the node code does for a fee payer. They rest on private source. ASK: Gokul for read access before reusing them.
- Whether the sentence about an app covering fuel "for the people who use it" needs a qualifier for a brand-new participant with zero KMOI is unanswered. ASK: Gokul.

## Check it yourself
```
python3 "$SKILLS/moi-blog/scripts/post-lint.py" --strict "$SKILLS/moi-blog/examples/moi-september-2026-release.md"
```
Expect 0 errors and the one warning above. Add `--repo "<path to a clone of sarvalabs/MOI-Website>"` and it is 0 and 0. To see the published version's findings, save it from `main` outside the repo and lint that: `git show origin/main:blog/src/content/posts/moi-september-2026-release.md > "$WORK/sept-published.md"`.
This file has not been through the Astro build. It is a copy for reading, and the build is `npm run build --prefix blog` in the repo.

## The other posts on main
| Slug | What it shows |
|---|---|
| `moi-august-2026-release` | A release post with a section per package and an operator runbook |
| `what-is-moi-network` | An explainer: 18 H2s, six figures, a recap |
| `how-to-give-an-ai-agent-authority-without-your-credentials` | An argument piece |
| `how-ai-agents-pay-each-other-moi` | A session write-up. It has 77 em dashes and no takeaways, so do not copy its style |
| `move-your-voyage-login-to-moi-wallet` | A short how-to with 17 FAQ entries |
