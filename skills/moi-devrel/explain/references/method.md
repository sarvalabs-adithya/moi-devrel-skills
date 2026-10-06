# Method: how to teach a MOI concept

Facts are as of 2026-10-03. The method is the one the previous operator asked for, instruction by instruction, between 2026-08 and 2026-10, shown with the date of each. Definitions of MOI terms are not here: they live in `moi-devrel/references/glossary.md` and `terminology.md`, and a teaching reply points to the glossary row instead of paraphrasing it. "The operator" and `ASK:` are defined in `moi-devrel/SKILL.md`. Quoted words are the previous operator's, cleaned of typos. Back to `../GUIDE.md`.

## 1. Before you speak: read, then label
On 2026-08-26 the previous operator told the assistant it had been wrong about two things on x402 and ordered deep research first, with nothing pushed. A fluent explanation is not a checked one.
1. Open the authority for the concept (`concept-paths.md`) and read the page or the file. Do not teach from memory.
2. Label each sentence you mean to say: doc-derived, source-derived or receipt-proven (the three labels are defined in `moi-webinar/references/demo-standard.md`), or "I will check". If sources disagree, the order of authority is in `moi-devrel/claim-check/references/sources-of-truth.md`.
3. If a sentence says something is live, read the node first (`moi-devrel/claim-check/references/live-reads.md`). The release note, the source tip and devnet are three different things.
4. If the glossary lists the term under "Not yet defined here", do not define it. Say what the sources do say, mark the rest "I will check", and put an ASK line in your reply.
5. Search your own draft for a universal: only, every, nobody, always, never, free, any. Each one needs a source or a limit.

## 2. End use first
The instruction, 2026-08: "do a top down explanation, like what is the end product use case then get into how it works". On 2026-08-27, for a standards document: "I want it framed as a simple before and after section, like what happens after MOI does all the steps, what does that change for a developer".
1. The first sentence says what someone can now do, or what problem goes away. The accepted opener for the September release was "You can now pay fuel for another user." (2026-09-11, `moi-devrel/references/house-style.md`).
2. Put the "today" picture before the mechanism only when the listener knows it. Session 8 opened with a job the audience would give an agent (book my flights) and asked where its preferences live today, before it said anything about access policies.
3. Use no term the operator has not met. If one is needed, define it in the same sentence. Define fuel where it is first needed, not in the opener (2026-09-11).
4. Context before jargon. On 2026-08-31 the instruction for the standards document was to explain what the naming body is and why x402 needs a name before going into the naming standard.

## 3. The mechanism
1. Numbered steps, one idea each, one section per turn. In the 2026-09-10 review of the spec and package pull requests the previous operator moved on with "ok next" or "next section" fourteen times.
2. Define each term at first use, in MOI context, in plain words, with the sense of its glossary row. One word per concept: fuel is what is paid, fee payer is the role, fee delegation is the feature (`terminology.md` section B).
3. When the listener will touch code, name the function, endpoint or RPC in each step: "tell me exactly which function is being used from where" (2026-09-10). Leave it out at the shallowest depth.
4. "Explain each step like I'm an idiot" (2026-09-10) asks for shorter words and one idea per step. It does not ask for a longer answer.
5. No generic analogy from another company. "Don't talk about Stripe, talk specifically in the context of MOI" (2026-08-27). A comparison with another chain is allowed when it is a fact the reader can check, and then it is a claim that needs a source. Session 8 compared Ethereum and Solana (the "How others enforce" slide, 2026-09-04), and its claims were audited on 2026-09-01.
6. A sentence the operator will repeat in public carries no metaphor: "real, direct, efficient" (2026-09-09). A plain picture is fine in the teaching chat. Tell the operator which sentences are only for the chat.
7. A flow gets a diagram: "explain with a diagram" (2026-08) and, in another session, "a box flow with arrows". Draw it as text in the reply. A diagram file is made only when the operator asks, and sharing it is a gate.

## 4. One example with named actors
Actors that carried a concept in earlier sessions: Alice and Bob swapping two assets (session 4), Jack and Jill finding each other in the registry (session 3), a seller and a buyer (session 7), an owner and an agent (session 8), a sender, a beneficiary and a payer (the docs sponsor tutorial), Bob and Alice sharing a calendar (the docs Access Control page).
1. Each actor has one job. Say what each holds at the start and at the end (balances, a counter, a policy), so the listener can check the claim.
2. Name the function, the endpoint or the RPC at each step when the depth calls for it.
3. A real devnet interaction is better than a described one: the previous operator ruled "no mock mode for chain, chain always has to run" for demos (2026-08). Running one spends devnet funds, so it is a gate. The operator performs every wallet step. When you describe an example you did not run, write "(constructed)" after it.
4. Read the receipt status, not the hash. A refused transfer still has a hash, and the explorer can lag by minutes (`moi-devrel/references/devnet.md`).
5. Include one refusal that is not ours when the concept has one (session 8 showed a write refused by the runtime, then allowed, then refused).
6. Keep it small enough to say aloud. The session 8 example was three runs of one file.

## 5. The restate loop
An operator checks understanding by writing "so ... right?". The previous operator wrote it 31 times in his log as of 2026-10-02. Example: "so 1 makes sense of the bytes and 2 converts the info back into bytes" (2026-09-10).
1. Start with "Yes." or "No.". Then fix exactly what is wrong and stop (`moi-devrel/references/house-style.md`, section 1).
2. Check the restatement against the source. Do not check it against what you said earlier, because a check against your own draft cannot find the draft's errors.
3. When the restatement is right but loose, add the limit: "Yes, for fuel. The sender still funds any value it sends."
4. Mark the parts right, wrong or missing. Move on only when every part is right.
5. When a restatement misses twice, the earlier explanation missed. Say it again shorter and with a different example. The previous operator's re-asks ("wdym, I don't get any of it", then "brief") asked for shorter, not longer (2026-09-11, inferred from position).

## 6. Pace and length
1. Chat answers are brief: answer first, then stop. Bullets, numbered items, or a table for pros and cons. Keep item numbers stable between turns, because a reviewer may reply by number: the previous operator wrote "explain 5" style replies about 20 times in his log.
2. When the operator wants more, they will say so, as the previous operator did ("no I want technical details"). Go deeper only then.
3. A learning document may be long when the operator asks for one, with an index first. A script read aloud may be long. Everything else stays short (`house-style.md`).
4. Do not insist after a no. If the operator chose a flow, such as the MOI Wallet extension with their own funded account, teach inside that flow (2026-08-31).
5. Recommend one decision and say its consequence when the operator must choose. Do not hand over a menu (2026-08-21).

## 7. Finish: say it, walk it, defend it
The explanation is done when the operator can do the three things in `levels.md` for the agreed depth. Then `defend-it.md`: three likely questions, the limit of each answer, its source, and an "I will check" for everything the evidence does not settle. Close with the hand-back in `../GUIDE.md`.

## 8. The written copy
1. Make it only when the explanation is big or the operator asks. Their words: "create a learning plan because I want to know every detail of this so create an index first". Use `templates/explainer.md`.
2. Date every volatile fact, list the sources read with the date and what was not read, and mark each sentence doc-derived, source-derived, receipt-proven or "I will check".
3. Keep it out of git. It can name private source and people. The command in step 10 of `../GUIDE.md` makes the folder self-ignoring.
4. After any correction, search every copy of the explainer and of anything built from it (README, script, deck notes). The false custodian claim survived in six files because the correction reached the blog and not the other copies (`traps.md`, rule 4).

## Not yet known
- Where earlier explainers and learning plans were kept, or whether any survived. ASK: Adithya.
- How long a teaching session takes. The request log holds no durations.
- Whether the previous operator's index-first learning plans exist as files.
