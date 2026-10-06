# Levels: three depths of the same concept

Facts are as of 2026-10-03. The same concept is taught at one of three depths. A file named without a folder (`glossary.md`, `terminology.md`) is in `moi-devrel/references/`. The depth follows from what the operator does next and who may challenge them, not from how much they already know. "The operator" and `ASK:` are defined in `moi-devrel/SKILL.md`. Back to `../GUIDE.md`.

## The three depths
| Depth | The operator can | Size | Shape | Test |
|---|---|---|---|---|
| 1. Say it | Answer a question in one breath, with the limit that keeps the answer true | About 35 words, which is 15 seconds at 140 words a minute (`moi-webinar/community-call/references/host-qa-prep.md`) | Yes or no first, then the answer, then the limit. The subject is named in the first clause so the sentence stands alone | Said aloud without notes, with the limit |
| 2. Present it | Teach it to an audience: a slide, a webinar segment, a blog section, a docs paragraph | A few minutes. CC14 slides 2 to 4 came to 560 words, about 4 minutes at the same pace, which is inferred from CC14: time a read-aloud (`moi-webinar/community-call/references/call-script.md`) | End use, mechanism in steps, one example with named actors, the honest limit | Walks the example with named actors, no notes, using the right terms |
| 3. Defend it | Hold the concept against a reviewer or a Q&A: every sentence traceable, the edges known | As long as the sources need, in a written explainer | Level 2, plus the source of each sentence, what it does not do, the comparison with other chains, three likely questions and an "I will check" list | Names the source of any sentence, and answers "what if" with a limit or "I will check" |

## How to choose
The table is this branch's own rule of thumb. No past session recorded a choice of depth, so adjust it with the operator.
| What happens next | Who may challenge | Depth |
|---|---|---|
| A host's question, a short reply, a social post | The words may be quoted alone, as a clip or a post, with nothing around them | 1 |
| A slide, a webinar segment, a blog section, a docs paragraph | The audience, and Rahul in review | 2, with a depth 1 sentence for each key claim |
| A Q&A, a spec or a pull request description, an upstream reviewer, a protocol-team review | Someone who will check each sentence | 3 |
| Building a demo or an app on it | The chain, which refuses or reverts | 2, plus the edges and a live read |
| The operator is new to the whole area | Nobody yet | Start with five sentences about MOI as a whole (depth 1), then one concept at a time at depth 2 |
1. Start at depth 1 and climb. The previous operator asked for detail when he wanted it ("no I want technical details", date not recorded) and asked "briefly explain it again so I can defend it" once an explanation already existed. Do not guess a deeper depth.
2. Day 3 of the first week in `moi-devrel/references/orientation.md` asks for MOI in five sentences that the operator confirms. Here the operator writes the five sentences and you mark each yes or no against the glossary and the docs pages named in `terminology.md`. That reading is this branch's, because the orientation row does not say who writes them.
3. When two depths fit, take the deeper one for any sentence that will be published. A published sentence is read by people who can check it.

## One concept at three depths: fee delegation
Every factual sentence below comes from the protocol team's release note as quoted in `moi-webinar/community-call/references/host-qa-prep.md`, from the September release post (the cleaned copy in `moi-blog/examples/moi-september-2026-release.md`), or from the docs sponsor tutorial (docs.moi.technology, `build/tutorials/sponsored-ix-tutorial`, read 2026-10-03). The actors marked (constructed) are invented for the example.

### Depth 1: say it (34 words)
"An interaction can name another account as its fee payer. The payer signs too and pays the fuel, and only the fuel; if the sender sends 5 KMOI, those still leave the sender's account."
Source: the release note says the fee payer "also signs the interaction and pays the fuel cost instead of the sender". The 5 KMOI sentence is in the post's FAQ.

### Depth 2: present it (about four minutes, the shape)
1. End use: you can now pay fuel for another user, so a new user can start without holding KMOI for fuel.
2. Before: the account that sent an interaction paid its fuel from its own KMOI.
3. Mechanism, in three calls (SDK 0.9.0-rc2, per the post and the tutorial): the sender builds the interaction and names the payer; the payer signs the same interaction with its own wallet; the sender submits it with both signatures.
4. Example (constructed): Mira, a new user, and Lamp, an app. Mira names Lamp's account as payer and sends 5 KMOI to a friend. Lamp's account is charged the fuel. Mira's account loses the 5 KMOI.
5. The limit: the payer signs each interaction one at a time, so there is no standing allowance. It covers fuel only. It also pays when the interaction fails (stated in the post).

### Depth 3: defend it (what a written explainer adds)
| Sentence | Source and label | Edge or check |
|---|---|---|
| The node rejects an interaction that names a payer unless the payer signed | Post FAQ, doc-derived. The post was checked against tagged source on 2026-09-11 | Nobody can name your account without your signature |
| Only a participant account can be a payer | Docs sponsor tutorial, doc-derived: the SDK refuses a logic id or an asset id in the payer field | That is SDK behaviour. Whether the node refuses it too is not on record. ASK: Gokul |
| The payer's signature covers fuel only, and a logic asking who signed does not see it | Post, doc-derived | A payer that should vouch for the operations is listed as a notary (`glossary.md`) |
| The participant list leaves out the sender and the fee payer | Post FAQ, doc-derived | The one exception is a fee payer that also acts as a notary. The SDK does it for you |
| It is live on devnet | The post says moipod v0.13.0 is live on devnet, which is a claim and not a read. Read the node: `net.Version` answered 0.13.0 on 2026-10-03 at 15:32 UTC and again at 17:37 UTC | That proves now, never since. Check the field name on the wire (`moi-devrel/claim-check/references/live-reads.md`, check 4). On 2026-10-02 all 346 readable listed interactions carried an all-zero `fee_payer`, so the field existed and nobody had used it. ASK: Gokul when devnet moved to v0.13.0 |
| A user with zero KMOI can do their first action | Not settled. The record does not say whether a brand-new participant must be created or activated first, or whether that costs fuel | "I will check." ASK: Gokul |
Then the three likely questions for this concept from `defend-it.md`, section A.

## One more: access policies, depth 1
"A program that writes to your account in an interaction you did not sign needs your permission: a policy stored on your account, checked by the runtime at the write. Today only storage writes are checked."
Source: docs Access Control page, "Why Writes Need Authorization", "Ground Rules" and "Current Scope" (read 2026-10-03). The limit is in the first clause: the page says the owner never needs a policy for its own state, so "a program that writes to your account needs your permission" would be false. Re-read "Current Scope" before you say "today".

## Not yet known
- How long a depth 2 explanation takes to give in a real session. The only timing on record is the CC14 word count at an assumed pace.
- Whether a depth 3 written explainer was ever made for an upstream review other than the review package. ASK: Adithya.
