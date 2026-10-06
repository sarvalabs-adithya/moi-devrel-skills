# Measure AI visibility and report it

Facts are as of 2026-10-03, from the Community Call 14 (CC14) deck and its ledger (2026-09-24 and 2026-09-25) and the record of the September sweep. Building the slide is `moi-webinar/community-call` and `moi-webinar/deck`; checking a figure is `moi-devrel/claim-check`. Back to `../GUIDE.md`.

## What exists
| Source | What it measures | State |
|---|---|---|
| The Scribble AI-visibility report and dashboard | How often MOI appears in the answers of AI engines to a fixed list of questions, how often our pages are cited, and per engine | The only series that exists. One baseline, 2026-09-24. Nobody on record has re-run it |
| Google Search Console | Google queries, impressions, indexing | Which properties exist and who owns them is not recorded. ASK: Rahul. The blog is its own property (`moi-blog/references/geo.md`) |
| Bing Webmaster Tools | Bing indexing. The sweep status draft said it has a first-party report of when Copilot cites us; that was not verified | Imported from Search Console on 2026-09-09 |
| Cloudflare AI crawl dashboard | Hits per crawler. This is access, not visibility | Suggested during the sweep, never shown as used |
| GA4 referrers such as `chatgpt.com` and `perplexity.ai` | Visits that arrive from an AI answer | Proposed, never set up |
| The promptfoo query suite | A model's answer to 25 questions (`examples/ai-visibility-queries.yaml`) | Ran three times on 2026-09-09 and never completed (`timed out after 300000ms in queue`). No result exists |
| Wikidata items for MOI and Sarva Labs | Entity recognition | Drafted. Whether they exist is unknown. ASK: Sai Kiran |

Crawler hits, index counts and answer mentions are three different things. Do not report one as another.

## The Scribble series
Scribble is the outside agency or partner behind the article wave ("the campaign we did with Scribble", Rahul). Whether it also runs the tracking tool, who can log in and how it computes visibility are all unknown. Sai Kiran passed its report and dashboard screenshots to the call. ASK: Sai Kiran for the report, the login holder and the formula.
What the CC14 slides said each figure meant (the previous operator's wording, not Scribble's definitions): visibility, how often MOI shows up in the answers to the tracked questions; citations, times our pages were cited as a source inside answers; mentions, times MOI was named in an answer, cited or not. The slides called it "the baseline we measure every month from here" and said to re-run "the same 47 queries every month".
The strongest tracked questions in the report: What is MOI Network? Is MOI a blockchain? What is the MOI Agent Launchpad? Is MOI compatible with other chains?

## Which numbers to trust
Source of the ledger: `moi-webinar/community-call/examples/cc14/numbers-ledger.csv`.
| Figure | Standing | Why |
|---|---|---|
| Visibility 17.3 percent, citations 1,203, mentions 650 | Read from the dashboard on 2026-09-24 and typed by the previous operator. "Confirmed" in the ledger means that and no more | Nobody re-derived them. The formula is unknown |
| Perplexity 20, Gemini 19.1, ChatGPT 12.8 percent | The same: dashboard screenshot, 2026-09-24 | The same |
| Copilot 19 percent | Typed by the previous operator, no screenshot on record | Weaker than the three above |
| 47 queries | Unconfirmed | It comes from the report text, which was older than the dashboard. Nobody answered the request for the current figure |
| Five engines | Unconfirmed | The deck shows four logos and never names the fifth (Claude, inferred) |
| 221 of 226 responses, 97.8 percent | Unconfirmed | From the same older text. 47 queries on 5 engines is 235, not 226, and nothing explains the gap |
| Gemini "up 12.8 points", ChatGPT "slipped 4.3" | Unconfirmed, contested | 12.8 is also ChatGPT's level, possibly a transcription slip. No source figure for 4.3. The previous operator asked on 2026-09-24 to remove trend arrows; the sentences stayed on the slide |
| 13.5 percent, 1,187 citations, 639 mentions; ChatGPT 17, Perplexity 17, Gemini 6.4 | Superseded | These were in the report text and the dashboard replaced them. An offhand "18 percent" was also replaced |
Rules: quote a figure only with its date and source. Do not quote any of them in a blog post (`moi-blog/references/geo.md`). A comparison needs both months' figures, each dated, on the same query list. ASK: Sai Kiran whether the 47 queries changed.

## Produce next month's figures
1. Ask Sai Kiran for the new report and the dashboard screenshots, and for the query list and engine list in the same message (`moi-webinar/community-call/templates/input-request-messages.md` has the wording). GATE: it is a message. The operator sends it; Claude drafts.
2. Put every figure in a numbers ledger with source, date and who confirmed it, before it goes on a slide. In September three sources gave three sets of figures, and the deck README still said "figures unchanged".
3. Compute the changes yourself and show the arithmetic. Check totals: queries times engines against the response count.
4. Mark each figure the report does not let you refresh as unverified, by name, and tell the operator. In September these went onto the CC14 deck unconfirmed.
5. Build the block with `moi-webinar/deck`: baseline cards, per engine, the questions, the content plan, what is next. Engine logos came from Wikimedia Commons.
6. Say the stage line the CC14 script used only if it is still true: the gap is a content problem before it is a product one, answered by core education, product-led and comparison content, and by documentation an AI system can read and cite.
7. Hand-back: what changed, which figures are unverified, and what the operator must still ask.

## Run your own check (optional)
`examples/ai-visibility-queries.yaml` is the previous operator's suite of 25 questions in four groups: direct questions about MOI, problem-space questions, disambiguation checks and competitive framing.
- It sends each question to a model API and tests the answer text. Nothing in it enables web search (inferred from the file), so it measures what a model says, which is not what a live answer engine cites. It cannot replace the Scribble figures.
- Its first assertion looks for the letters "MOI" in any case, which also matches inside other words. Tighten it before you trust a pass rate.
- It needs a provider key, typed by the operator at the terminal and never pasted into chat or a file. Paid calls are spend: state the number of questions and providers first (`moi-devrel/SKILL.md`, Gates). The free Groq model queued and timed out on 2026-09-09.
- Run it with `npx promptfoo eval -c <file>`. That downloads a package: GATE. It was never run to completion, so there is no baseline.

## What to say about it
- Quote exactly. Report what was measured, on which date, from which source. Do not claim a measurement that was not run: the promptfoo baseline does not exist.
- Judge change over four to eight weeks. Week to week movement on a handful of posts is noise (the previous operator's advice, in `moi-blog`).
- External authority, meaning mentions and third-party listings, was named as the gap to a top score (`audit-method.md`). Docs and posts alone do not close it.

## Not yet known
- Where the Scribble report lives, who logs in, how visibility is computed and who refreshes it. ASK: Sai Kiran.
- The fifth engine and its figure. ASK: Sai Kiran.
- Whether the 47 queries, the 221 of 226 coverage and the 12.8 "up" are right. ASK: Sai Kiran, from the dashboard.
- Whether the docs team receives the monthly query list before the call. ASK: Sai Kiran.
