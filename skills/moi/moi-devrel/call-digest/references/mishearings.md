# Mishearings: what auto-notes get wrong, to check every digest against

Facts are as of 2026-10-03. Sources: Gemini notes of Builders sessions II and III, Forge calls and the August 2026 marketing standups (read 2026-10-02), pasted Otter and Zoom transcripts, the Otter file of 2026-08-04 (read 2026-10-03; local to the previous operator and not available after the handover), the call transcript of 2026-09-14, and `moi-devrel/SKILL.md` fact 4. Otter and Gemini both misspell Sarva Labs and both mis-hear product names. `scripts/transcript-prep.py` holds the same rows in its `MISHEARINGS` table, under the id in the first column. When you change a row here, change it there too. A hit is a prompt to check, never a correction: "Moy" can be a surname and "KOI" a fish. Back to `../GUIDE.md`.

How to use it:
1. Run the script and read the "Known mishearings" part of its report. Then read the transcript for the same shapes the script cannot know.
2. In the digest, quote what the notes say and add what you read it as, in brackets, with the check: `"Server Labs" [transcript reads Server Labs; Sarva Labs]`. Do not edit the transcript.
3. A name, product or amount stays marked "check" until its source is named (`method.md` section 8).

## A. Names and products heard wrongly
| Id | The notes wrote | Check against | Recorded in | Settle it by |
|---|---|---|---|---|
| moy | "Moy", "MOY" | MOI | Gemini notes, read 2026-10-02 | Context: the company or network name |
| koi | "KOI" | KMOI, the native token of the MOI network | Gemini notes, read 2026-10-02 | Context: a token amount follows |
| server-labs | "Server Labs" (Gemini), "Serval Labs" (the 2026-09-14 call transcript; the tool is not recorded) | Sarva Labs (GitHub org `sarvalabs`, site sarva.ai) | Gemini notes of Forge calls; the 2026-09-14 transcript. Otter also misspells it | `moi-devrel/references/terminology.md` table A | <!-- slop-lint: ignore -->
| grock | "Grock" | Groq, the model provider | Gemini notes, read 2026-10-02 | Context: a model or key is being discussed |
| x402 | "X42", "X 002" | x402, the payment protocol (the same file also writes "X402") | The Otter file of 2026-08-04, lines 245 and 296 of the original | Context: a payment protocol or the agentic payments demo |
| my-forge | "My Forge" | MOI Forge, the campus programme | Gemini notes of Forge calls | Context |
| open-claw | "Open Claw" | OpenClaw, one word, the third-party agent framework of Builders session 3 | Gemini notes, read 2026-10-02. The research lists it as mangled and does not give the intended form; one word is the spelling this library uses | Context |
| hermes | "Hermes" | Not recorded. The research lists it among mangled names without the intended word. The session 3 roadmap lists Hermes among agent frameworks | Gemini notes, read 2026-10-02 | not recorded (the previous DevRel's notes); ASK: Rahul what was meant |
| voyage | "Voyage" | Voyage is the explorer and tooling site, never the network | Pasted Otter or Zoom transcripts, listed as mis-transcribed. The wrong form was not recorded | Ask what the speaker meant |
| iome | "IOME" | IOME is the earlier wallet and login, replaced by MOI Wallet in late August 2026 | The same pasted transcripts | Ask whether MOI Wallet was meant |
| kl-or-pr, lms | "KL or PR", "LMS" | Not recorded | Gemini standup notes, August 2026, listed as imprecise names | ASK: Sai Kiran what was meant |
Also listed as imprecise in the same standup notes: "Scribble". Scribble is a real outside agency or partner (`people-and-teams.md`), and the notes' use of the word was the imprecise part. The script does not flag it. Read the sentence it sits in.

## B. Wording MOI corrects when it is spoken
These are not mishearings. A speaker said the old form. The digest quotes it as said and adds the right form. Do not write the old form in your own sentences. `moi-devrel/references/terminology.md` has the full rows and the dates.
| Id | Said or written | Write | Date of the rule |
|---|---|---|---|
| voyage-devnet | "Voyage devnet" | devnet | 2026-09-25 | <!-- slop-lint: ignore -->
| chain-id | "chain ID" for MOI's own identifier | network ID | 2026-09-14 | <!-- slop-lint: ignore -->
| account-centric | "account-centric", "account-based" | participant-centric | 2026-09-14 | <!-- slop-lint: ignore -->
| old-network | "Indus", "Babylon" as the current network | devnet | 2026-08, day not recorded | <!-- slop-lint: ignore -->
| building-in-public | "Building in Public" as the call's name | The Campfire Chat | 2026-09, CC14 | <!-- slop-lint: ignore -->
| rc-suffix | "rc2" or "release candidate" described as shipped | Keep the `-rc` suffix; a candidate is not shipped | 2026-08-27, CC13 | <!-- slop-lint: ignore -->
| twelve-am-utc | "12:00 AM UTC" | 00:00 UTC, with the date and IST | 2026-09-10 | <!-- slop-lint: ignore -->
| us-zone | "EST", "EDT", "PST", "PDT" | An area/city zone, converted with `time-table.sh` | 2026-09-10 |

## C. Figures to recompute
Auto-notes get numbers wrong, and so do speakers. Never copy a figure from notes without checking it.
| Figure | What is on record | What to do |
|---|---|---|
| Bounty or challenge amounts | At Builders III the challenges were heard as "500k and 1M token"; the research says the amounts are as Gemini heard them and must be verified before reuse | Ask the presenter. The bounty amounts are set by Rahul and the session host: ASK: Rahul |
| The faucet amount | 20K KMOI in the Forge guide (13 January), 100K on the 30 January call and on 24 September | Read it live. Do not write one without checking |
| Units | 1 KMOI is 1,000,000,000 anu. As of v0.13.0 the lowest fuel price is 50 anu and storage costs 1,000,000 anu per byte (`glossary.md`) | A spoken "fifty" or "a million" with no unit is an open question. Convert with the SDK, never by hand |
| Versions | Keep the exact tag and any `-rc` suffix. Devnet `net.Version` read 0.13.0 on 2026-10-02 | `moi-devrel/references/devnet.md` before you write "live" |
| Two figures for one thing | The CC14 material carried 13.5% (the Scribble report text), 17.3% (the dashboard) and an offhand "18%" (the user) for AI visibility, three sources for one measure (2026-09-24). The trap is the same on a call | Quote all of them with their speaker and source. Do not pick |
| A sum or a product | On the CC14 slides 47 queries on 5 engines was set against 226 responses, and 47 times 5 is 235 | Recompute before you repeat it |
| A count of agents, users or posts | Counts move. The Explorer's index was stale on 2026-10-02 (49 agents) | Read the source on the day |

## D. Times and dates
| What | Rule |
|---|---|
| A Gemini document title | It carries a zone ("2026/09/24 13:53 EDT"). That moment is 17:53 UTC and 23:23 IST (`time-table.sh`, 2026-10-03). Convert it before you compare two calls |
| A call titled "8:30 PM IST" | The same call began at 20:29 IST (the 2026-04-14 governance call). Title and start differ by a minute, so quote the start the notes give |
| "Tomorrow", "next Friday", "end of the month" | Turn into a date from the call date and say the date |
| A time of day with no zone | Ask which zone. The team announces in IST and the protocol runs in UTC |

## E. People: spelling and look-alikes
Check every name against `moi-devrel/references/people-and-teams.md`. A first name not on it is a question for the operator if they were on the call, otherwise ASK: Rahul. It is never a guess.
| Name in the notes | Care |
|---|---|
| Srikar, Sreekar | One DevOps person, spelled both ways on record |
| Ruta, Rutha | The host of the community call, spelled both ways in Drive scripts. The name is not settled. ASK: Vardan |
| Harsh | Harsh Gupta (Points), Harsh Rastogi (SDK), and a Harsh tied to Galxe who may be Rastogi. Ask which |
| Rahul, Ram, Rishal | Different people whose names share a first letter. No mix-up is on record. Confirm who before you assign a decision |
| Prateek, Piyush, Prakhar | Different people: Prateek gave the product update (Proofly), Piyush is in marketing, Prakhar is on the Voyage team. No mix-up is on record |
| Krishna | The video editor, a match the research calls inferred |
| Bertan | Heard in the Builders III notes as the colleague who watched chat. The spelling is unverified |
| Robert Špendl | The surname may lose its diacritic in notes |

## Not yet known
- The wrong forms of "Voyage" and "IOME" in the Otter transcript, and the intended words behind "Hermes", "KL or PR" and "LMS". not recorded (the previous DevRel's notes); ASK: Rahul.
- Whether Otter and Gemini make different kinds of error beyond Sarva Labs. Nobody compared them.
- Which spelling of the host's name is right. ASK: Vardan.
