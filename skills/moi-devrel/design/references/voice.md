# Voice for on-image copy

Facts are as of 2026-10-03. The authority for wording is `moi-devrel/references/terminology.md` (names, money words, release words, positioning) and `moi-devrel/references/house-style.md` (the three registers; on-image copy is register 2, public copy). This file lists where the previous operator's design skill agrees with them, where it differs, and what is contested. Where two sources differ and no one has settled it, this file says so and does not pick. Back to `../GUIDE.md`.

## The old design skill against the authorities
| Old rule | Authority | Verdict |
|---|---|---|
| Second person, "you", almost never "we" | Website `CONTENT.md`, "Voice" (on `main` of `sarvalabs/MOI-Website`, commit `5e91afa`, read 2026-10-03): "Second person ... Almost never 'we'", declarative, short lines | Agree |
| Sentence case headlines. Uppercase only for section labels and small chips | `CONTENT.md`: sentence case, "UPPERCASE only for small section labels" | Agree |
| No emoji | `CONTENT.md`: "No emoji." `house-style.md` section 2 says the same for X and LinkedIn, and lists "banned or only unused" as not known (ASK: Rahul). The lint warns on emoji | Agree. Whether it is a ban or a habit is open |
| Use participant, authority, scope, revoke, on chain, agent. Avoid user, permissions, blockchain, AI assistant | `CONTENT.md` "Voice" and `terminology.md` table D | Agree for website and marketing copy |
| Also avoid "account" and "identity" | `terminology.md` table A: an account is "the vehicle that represents a participant's state", and the docs pages are named account and tesseract. "Identity" is retired as a headline word but "still names an agent's on-chain identity in product text" | Differ. On a docs image or a protocol explainer, "account" stays. On marketing art, follow the website list |
| "On chain", never "blockchain" | The positioning line "on-chain authority for the agentic economy" hyphenates the adjective | No conflict: "on chain" as an adverb, "on-chain" before a noun |
| Em dashes in long-form lists are fine | `house-style.md` rule 1 of section 2 and the lint: no em dashes in anything you author | Differ. The authorities win. This library has none |
| "Cause then consequence", "quiet menace, then exit" | `house-style.md`: no contrast frames, no "not X, not Y". Open with what the reader can now do | Style note only. Do not build a line on a contrast | <!-- slop-lint: ignore -->
| Numerals always ("2,100+ Validators", "9 seconds", "Seven years") | `house-style.md`: every public claim is checked against source | The three examples have no source in this library. Do not use them |
| "MOI currently works with @openclaw, with @LangChain support coming next" | `moi-devrel/claim-check` | Unverified, from an old folder whose files are dated 28 May 2026. Do not publish. The library mentions OpenClaw only as a third-party agent framework used in Builders session 3 (`moi-devrel/references/consent-and-identity.md`, section 7) |
| A four-step promise: exist on-chain, monitor, scope, revoke | `moi-devrel/claim-check` | Unverified as a product description. "In real time", "at machine speed" and "globally enforced" are claims about the protocol: each needs a check before it is printed |

## Positioning: the lines in use, none chosen
| Line | Where it appears | Status in the sources |
|---|---|---|
| "on-chain authority for the agentic economy" | The moi.technology headline | Current (`terminology.md` table D, 2026-06-02) |
| "The participant layer for AI agents." | Docs sites, word for word where space allows | Current (table D, 2026-09-22) |
| "the on-chain authority layer for AI agents" | The old design README, its skill description, the UI kit's page title and footer (the old folder's files are dated 28 May 2026) | In `terminology.md` table D as in use and unclassified. Neither current nor retired in the sources |
| "Authority Layer for the Agentic Economy" | The moidocs site config tagline (read 2026-10-03) | In `terminology.md` table D as in use and unclassified |
`terminology.md` Contested item 2: the sources do not say which line leads on the blog, social posts and decks. ASK: Rahul.
Retired, never use: "context infrastructure", "Not Your Context, Not Your Agent", and "identity" as the headline word. The old README also carried "Not your Context, Not your KitKat" under an `OFFICIAL STATEMENT` chip. Whether that is also retired is not recorded. <!-- slop-lint: ignore -->
What to do when a branded asset needs a positioning line:
1. Ask the operator which line, and tell them the question is open (ASK: Rahul).
2. If nobody answers yet, leave a visible bracket on the draft, or show variants A and B and let the operator pick (`house-style.md`, polish order, step 5).
3. Never copy a line from the old README, the UI kit or the preview cards as if it were approved.

## Lines the old README called verbatim Figma copy
Kept as tone samples only. Approval status unknown; each is a statement that must pass `moi-devrel/claim-check` before it goes on a public asset.
- "You haven't met the participant yet."
- "Your authority, four ways."
- "Monitor, scope and revoke AI Agents in real time." (called the hero sub-line for moi.technology)
- "Pip. Your participant. On-chain."
- "You exist once, on chain, as a coherent participant."

## Rules for text printed on an image
1. Short and declarative. Every sentence readable aloud (register 3 of `house-style.md` if it is also spoken).
2. Name the thing: KMOI, fuel, fee payer, devnet, network ID, capped supply, participant-centric. `terminology.md` has the full list.
3. Say "devnet", never "Voyage devnet" or "Indus". <!-- slop-lint: ignore -->
4. A date is a date: "11 September", never "today" or "last Friday". A time is "00:00 UTC on 11 September (05:30 IST)".
5. A version keeps its suffix: `0.9.0-rc2`. A release candidate is not shipped. <!-- slop-lint: ignore -->
6. No figure without a source and a date. Quote a release note verbatim.
7. No cancelled plans, reviewer names, private repo paths or unmerged features on the image.
8. A release announcement is simple, points to the release notes and carries no hook. The blog's release posts carry no pictures (August decision, `moi-blog/references/assets.md`), so ask before making art for one.
9. Alt text on every image is a full sentence that says what the picture shows.
10. The handle is `@MOI_Tech`, the site `moi.technology`, in lowercase.

## Checks
```
bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" brand-<slug>/index.html
python3 "$SKILLS/moi-devrel/design/scripts/brand-check.py" brand-<slug>/index.html
```
The lint reads the markup too, so a hit may sit in an attribute. Read every warning. The lint is a floor.
