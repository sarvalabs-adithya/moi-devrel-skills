# Worked examples: explanations that held up, and what made them work

Facts are as of 2026-10-03. "Held up" means the previous operator or the founder kept the explanation after review, or it was delivered live. The research notes hold no audience reaction to any of them: they record no attendee questions for a Builders session or a community call as of 2026-10-02. Each entry gives the source, the shape in short, what made it work, and what to re-check before you reuse it. Definitions are not repeated here: they live in `moi-devrel/references/glossary.md` and `terminology.md`.
Cleaning: quotations are shortened, em dashes became commas or colons, typos are fixed, no reviewer name appears, and no key, address or hash is copied. Files marked branch are on `claude/agent-payments-simple` of `moi-foundation/MOI-Webinars`, not on `main`. Files marked local exist only on the previous operator's machine (not recorded; ASK: Rahul). "The operator" and `ASK:` are defined in `moi-devrel/SKILL.md`. Back to `../GUIDE.md`.

## W1. KMOI, then anu, in two sentences (2026-09-11)
- **Source:** the cleaned September release post, section "Why price in anu?" (`moi-blog/examples/moi-september-2026-release.md`), and `terminology.md` B.
- **Shape:** "KMOI is the native token of the MOI network, like ETH on Ethereum. You pay fuel and storage deposits in KMOI, and the network counts it in anu, its smallest unit, the way Ethereum counts ETH in wei." Then the number a listener can check (one KMOI is 1,000,000,000 anu) and the SDK helpers instead of arithmetic by hand.
- **What made it work:** it names the thing instead of using a vague noun, defines it once, and puts the unit second. The previous operator's instruction was "say what is KMOI and then talk about anu". The analogy points at something the developer already knows, and the number can be checked.
- **Re-check:** the figures are as of v0.13.0; constants come from the SDK (`KMOI_ASSET_ID`, `DEFAULT_FUEL_PRICE`), never from a post. The ETH and wei comparison is optional, and the previous operator offered it as such.

## W2. An opener that is a new capability (2026-09-11)
- **Source:** the same post, opening and "Four terms come up throughout" list.
- **Shape:** "You can now pay fuel for another user." Then the second paragraph counts what breaks and names it before explaining any of it. Four terms are defined in one list near the top, in MOI context.
- **What made it work:** three earlier openers were rejected, one after another, as abstract, vague and over-general (`moi-blog/examples/README.md`). This one says what a developer can now do.
- **Re-check:** label what a count counts. The published post says three breaking changes, four changes and five things; the cleaned copy says "five places in your code can break".

## W3. Start from a job, then ask where the information lives (2026-09-04)
- **Source:** `session-8-policies/SCRIPT.md` (branch), slides 2 to 8.
- **Shape:** "Imagine you ask it to book your flights. You tell it you prefer aisle seats, you don't want overnight flights, and you give it a limit on what it can spend." Two kinds of information: what the agent does, and what it needed to know about you. Then a question: where does that information live, so the agent can read it? Slide 3 answers with today's two homes (the application, the agent). Slide 6 turns the consequence into the reason for the session: if your data sits on your account, a program that updates it writes to an account it does not own. Slide 7 voices the objection (why not write a rule in a program), slide 8 gives the answer.
- **What made it work:** the use case is a job the audience would give an agent. The question at the end of each slide is the topic of the next. The objection is said before the audience can raise it. The closing "Honest scope" slide says what the mechanism does not do yet.
- **Re-check:** the slide 6 sentences about Ethereum and Solana are claims about other projects, so read their sources again (the docs Access Control page frames the Ethereum side). Slide numbers drift: refer to slides by title. The spend limit in the story is not enforceable today (`misconceptions.md`, M11).

## W4. One variable changes (2026-09-04)
- **Source:** `session-8-policies/SCRIPT.md`, slides 11 to 14 and "Likely questions" (branch); the live results are in `NOTES.md` (branch).
- **Shape:** one file is run three times. Refused, then allowed after the owner grants a policy, then refused after the owner revokes it. "The agent's code, key, and arguments stayed constant across all three, and the one variable in the whole experiment was the policy on my account." The logic is thirty lines, read whole before it runs, and it contains no permission check, so the audience can see the decision is not in it.
- **What made it work:** one variable, a code file small enough to read, a refusal the audience can see with its error text, a receipt anyone can look up, and a recorded run as the fallback.
- **Re-check:** the fuel figures (86 refused, 134 allowed) are devnet-build facts from 2026-08-31 on a node that answered 0.12.0. No run of any session is on record since the wipe announced for 11 September 2026 (`moi-webinar/SKILL.md`). Run it again before you reuse the numbers. Running it spends devnet funds: a gate.

## W5. Named actors and a table of calls (session 4)
- **Source:** the session 4 README (`main`), "What each on-chain call does".
- **Shape:** a table with Step, Who, Call, Effect. Alice locks 100 TKA for Bob, Bob locks 90 TKB for Alice, Alice claims hers, Bob claims his. The README opens with the limit: "This is a trust-based swap, not a chain-enforced atomic swap."
- **What made it work:** each row has one actor and one call, so a listener can follow the money. The limit sits on the first screen, before anyone asks.
- **Re-check:** "irrevocable" and "only the beneficiary can pull" are the README's words. The 2026-08-07 audit found Lockup and Release semantics are node-side and could not be verified from the SDK, and no later check is on record. The docs Assets page describes Lockup more loosely: the amount stays owned but cannot be transferred until released (read 2026-10-03). Treat the README's two phrases as "I will check" (ASK: Gokul). The same README says release called with nothing locked "succeeds" and moves zero funds.

## W6. The teaching guide: ideas in order, one aha, honest boundaries (session 6)
- **Source:** `TEACHING-GUIDE.md` in the previous DevRel's fork (sarvalabs-adithya/moi-agent-budget) (private; ASK: Rahul for access), and the session 6 README (`main`).
- **Shape:** what you are teaching in one sentence; four ideas in the order to teach them; the live demo mapped step by step to the ideas; one aha said aloud ("Same question, same math, different answer, and the only thing in between was one transaction. The identity was never stored anywhere. It's computed."); honest boundaries for Q&A; gotchas; a pre-flight list.
- **What made it work:** every demo step maps to an idea, and the boundaries are written down before anyone asks. The guide's own boundaries said sub-accounts share the primary's key and the chain does not enforce what an agent may do. That is the reason `session-8-policies/NOTES.md` (branch) gives for ending the first session 8 design after a reviewer's objection. Carry a teaching guide's boundaries into the next design.
- **Re-check:** the guide compares a sub-account to "an account you open at one specific bank", with the primary account as "you". That is a plain picture for the chat, not wording for public text. Sub-accounts have no glossary row, though the docs Interactions page describes AccountInherit as creating an application-specific sub-account of a primary account (read 2026-10-03). The contract in the demo was wiped by the devnet resets since July. Session 6 has no record of having been held (`moi-webinar/SKILL.md`; ASK: Vardan), so this is a model of structure and not evidence of delivery.

## W7. A standard explained for a reviewer: example first, then before and after (2026-08-27 to 08-31)
- **Source:** `x402-compat/x402.md`, sections 1, 3 (first part) and 4 (branch).
- **Shape:** two sentences on what x402 is. "HTTP 402 and x402 are not the same thing." A weather example with named actors: an agent planning a delivery route, a forecasting service selling at a tenth of a cent a call, four numbered steps, "no signup, no subscription, no invoice". Then, before the naming standard, a plain paragraph on what CASA is and why x402 needs a name. Then a developer before and after table.
- **What made it work:** the previous operator asked for exactly this: a specific example before the section, the context of CASA before CAIP-2, and a before and after framing specific to MOI. He rejected comparisons with other companies.
- **Re-check:** the draft carries statements fixed later: `moi:mainnet` listed as if it existed, "no single genesis block", "about 50" registered chains (49 on 2026-09-09), "seven security decisions" (the spec later has eight MUST rules) and "~600 lines" (an estimate with no source). Use the shape, re-verify every number.

## W8. The fifteen-second answer with a second beat
- **Source:** `moi-webinar/community-call/references/host-qa-prep.md` (CC14, 2026-09-25).
- **Shape:** a yes or no first, about 35 words, the subject in the first clause so it works as a clip; a second beat with the limit; the trap written for the operator only; an honest fallback; the source for each part.
- **What made it work:** it stayed in the CC14 slide notes as a bracketed cue, and it states the limit that a fast answer would drop.
- **Re-check:** the open edge in that file (a brand-new participant's first action). ASK: Gokul.

## Not yet known
- Which of these an audience followed. No attendee questions or feedback are on record. ASK: Vardan whether any exist in the call or Discord records.
- Whether the explainers the previous operator asked for ("do the explainer doc") were kept anywhere he reads again. not recorded (the previous DevRel's notes); ASK: Rahul.
