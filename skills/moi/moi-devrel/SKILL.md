---
name: moi-devrel
description: "Start here for MOI developer relations (DevRel): house rules, repo map, people, devnet facts. Use when new to MOI DevRel, or for \"where does X live\", \"who owns X\", \"who do I ask\", \"which skill do I use\", \"is devnet live\", \"what time is that in IST\", \"lint this text\", \"scan for secrets\", or a message to DevOps, Rahul, a reviewer or the protocol team (\"status update\"). Branches: ship (\"commit\", \"push\", \"open a PR\", \"rebase\", \"merge\", \"is it live\", \"remove the co-author\"); design (\"brand colours\", \"logo\", \"social card\", \"make a graphic\", \"Pip\"); claim-check (\"fact check\", \"is this true\", \"are you sure\"); explain (\"explain X\", \"teach me\"); call-digest (\"call transcript\", \"meeting notes\", \"what did we decide on the call\", \"what do I owe\", \"action items\"); test-round (\"test pass\", \"test round\", \"regression pass\"). Other topics have their own skills (webinar and decks, blog, docs, Launchpad, MCP, the website and Dataroom and Points, devnet reset, standards, education), all listed inside."
---

# MOI DevRel: start here

## What this covers
The main skill, and the one every other skill leans on. Its own job is to orient a newcomer and hold what every job needs: the house rules, the standing work loop, the repo map with product health checks, people, calendar, keys and accounts (names only), devnet facts, wording rules, teammate messages and the shared scripts. DevRel makes what Sarva Labs and the protocol team ship usable and visible: the monthly community call, Builders webinars, release posts, blog and social, four docs sites, decks, standards work (x402, CASA) and six products the previous operator built or ran (Agent Launchpad, Agent Explorer, MCP server, website, Dataroom, Points Program). Which of them DevRel now owns is not settled. ASK: Rahul. A human operator approves every step that leaves the machine; Claude researches, builds, verifies and explains.
Six branches live inside this skill, each its own guide (`<branch>/GUIDE.md`):
- `moi-devrel/ship`: how any change gets out, from work identity to a checked live page.
- `moi-devrel/design`: the visual brand: colour and type tokens, logos, the mascot Pip, page and card starters, a brand checker.
- `moi-devrel/claim-check`: a ledger that checks each claim in text that leaves the team against source.
- `moi-devrel/explain`: teaches a MOI concept top down until the operator can say it and defend it.
- `moi-devrel/call-digest`: a call transcript into decisions, owed work with owner and date, and open questions.
- `moi-devrel/test-round`: a planned, recorded test pass on a product, with a log someone else can trust.
`ship` (how any change gets out) and `design` (the brand) are the underlying instructions for every skill in the library, and the other skills do not repeat them. `claim-check` runs before anything public: posts, decks, scripts, social copy, docs pages, filings.
Not covered here: Builders sessions, the monthly call and decks (`moi-webinar`, `moi-webinar/community-call`, `moi-webinar/deck`); the blog and release posts (`moi-blog`, `moi-blog/release-pack`); docs sites and search visibility (`moi-docs`, `moi-docs/geo`); the Launchpad and the Explorer (`moi-launchpad-ops`, `moi-launchpad-ops/explorer`); the MCP server (`moi-mcp-ops`); a devnet reset (`moi-devnet-reset`); outside standards (`moi-standards-submission`); Forge and awesome-moi (`moi-education-programs`; MOI Sprint was scratched on 13 October 2026).

## Before you start
Conventions every `moi-*` skill and branch uses. They point here for them.
- **`$SKILLS`** is the `skills/moi` folder of the handover repo `sarvalabs/moi-devrel-skills`: clone it, then `export SKILLS=<clone>/skills/moi` (the repo README has the install steps). Quote it, because a path can hold spaces. Run every command from the working copy of the repo you are working in, never from inside a skill folder. Session folders (`community-call-<N>`, `session-<N>`) sit at the root of a working copy of `moi-foundation/MOI-Webinars`; the decks for calls 2 to 14 are in `community-call-<N>/deck/` there (PR #2, merged 13 October 2026). Whether they get committed, and on which branch, is a policy nobody has written down (ASK: Rahul). Until it is settled, scaffolds keep internal files out of git, and nothing is staged beyond what the operator names or pushed without their yes: a push to that repo publishes.
- **The operator** is the human working with Claude now. **The previous operator** is Adithya Ganesh, who hands over on 14 October 2026. Lines about the past say "the previous operator". A question about history that no handover doc answers is marked "not recorded (the previous DevRel's notes); ASK: Rahul". Questions about roles, ownership or policy go to ASK: Rahul, or the named person the evidence supports. Never send the operator a question that a new person cannot answer.
- **`ASK: <person>`** means the evidence does not settle this. Put the question to that person through the operator: draft it, the operator sends, and you never message that person yourself. Do not guess meanwhile.
- Every fact in `references/` is true "as of" the date beside it. Re-check anything that moves: versions, ids, open PRs, owners.

Checklist (what, who provides it, how to ask):
- [ ] A one-line goal and the row below that fits it. The operator provides it. Ask: "What should exist at the end, in one line?"
- [ ] `SKILLS` set and the repo open. Ask: "Which folder holds the moi-* skills, and which repo are we in?"
- [ ] Identity check: set `PREFLIGHT_WORK_DOMAINS` and `PREFLIGHT_EXPECT_GH_LOGIN` once, `cd` into the repo, run `bash "$SKILLS/moi-devrel/scripts/preflight.sh"`. Fix every FAIL and read every WARN before a commit. The operator provides the work login and the mail domain of the work address (a domain only, as the script header explains). If either is missing, draft the request to Rahul: the operator's name, the address they will commit with and the area they will work in. The operator sends. ASK: Rahul.
- [ ] The source of truth for each claim: release note, docs.moi.technology, SDK source, a live devnet read. The protocol team provides release notes, through the operator. ASK: Gokul where this version's note is.
- [ ] Who approves the output (`references/people-and-teams.md`). ASK: Rahul if the table does not say.

## The run
Seven house rules apply at every step, in every skill and branch.
1. Brief by default: answer first, then bullets. Long text only for scripts read aloud and learning documents.
2. Every public claim is checked against MOI source or docs before it goes out. A release note is quoted verbatim.
3. Nothing leaves the machine without an explicit yes (see Gates).
4. Work identity only on commits and pull requests. No AI co-author line, no "generated with" footer.
5. Demos and tests use real devnet interactions. Say plainly when something is simulated.
6. Public text has no em dashes, no "not this, not that" constructions, no vague attribution, and reads aloud naturally. <!-- slop-lint:ignore -->
7. Sub-agents only when the operator asks for them.

| # | Step | What to do | Where or command | Done when |
|---|---|---|---|---|
| 1 | Goal | Restate the goal in one line. For anything new, propose a short plan: steps, outputs, what only a human can do. | the conversation | The operator says yes to the plan. |
| 2 | Teach | If the operator does not yet own the mechanism, explain top down: end use, mechanism, one example with named actors, plain words, each term defined on first use. | `moi-devrel/explain`, `references/glossary.md` | The operator restates it ("so ... right?") and you answer yes or no first. |
| 3 | Build | Work locally. Do not push, post or deploy. | a file on disk | A draft exists and you state its exact path. |
| 4 | Show | Show it running or rendered, and name the path or URL that is fresh. | local server on a new port, preview link, opened file | The operator has seen the real output. |
| 5 | Review | Number the items. Change exactly the item or sentence the operator points at and nothing around it. | `references/house-style.md` section 1 | Every numbered item is answered. |
| 6 | Verify | List each claim on its own line, check it against source, mark verified, argument or cut. Quote release notes verbatim. | `moi-devrel/claim-check`; `references/devnet.md` "Before you say live" | No unsupported claim remains. |
| 7 | Polish | Prose pass, variants A and B when wording is contested, then lint. Scan anything you will share. | `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" <files>` and `bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" <path>` | Lint reports 0 errors. The scan is a backstop: read its NOT scanned line. |
| 8 | Final | Show the exact final text, destination and time in one place. | `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "<YYYY-MM-DD HH:MM>" <area/city>` | The operator has read it once. |
| 9 | Ship | Only on an explicit yes that names the action. After a manual step by the human, re-read state before continuing. | `moi-devrel/ship`; Gates below | The live URL or file has been checked after the run. |
| 10 | Close | Hand back in the format at the end of this file. | Hand-back | Remaining work and a ready verdict are stated. |

Where a branch takes over: step 2 is `moi-devrel/explain`; step 3 is `moi-devrel/design` for anything visual and `moi-web-products-ops` for a change to the website, Dataroom or Points; step 4 can be a recorded pass, `moi-devrel/test-round`; step 6 is `moi-devrel/claim-check`; step 9 is `moi-devrel/ship`. A call transcript enters at step 1 through `moi-devrel/call-digest`. A message to a teammate is drafted at step 3 (`references/house-style.md` section 4) and sent by the operator.

## Which file to read
This skill's own files:
| Doing | Read |
|---|---|
| First week, what DevRel does, ranked jobs | `references/orientation.md` |
| Where a repo lives, how it deploys, who to ask, a product's handover warning | `references/repo-map.md` |
| Who someone is, what to go to them for | `references/people-and-teams.md` |
| Dates, cadence, scheduling, time zones | `references/calendar.md` |
| An account or a key shared across products | `references/keys-and-access.md` |
| The variable names of one product | `references/keys-by-product.md` |
| Saying anything about devnet, a reset, "live" | `references/devnet.md` |
| Wording MOI insists on | `references/terminology.md` |
| A MOI concept in plain words | `references/glossary.md` |
| How to write: replies, public copy, scripts read aloud | `references/house-style.md` sections 1 to 3 |
| A message to DevOps, the protocol team, a reviewer or Rahul; reading one that arrived. For the website, Dataroom or Points, the asks already known are in `moi-web-products-ops/references/who-to-ask.md` | `references/house-style.md` section 4, `templates/messages.md`, then `scripts/check-message.py` |
| A review request, a reply to a change request, reviewing a colleague's PR, a status update to Rahul, a last read of any message before the operator sends it | `references/review-requests.md`, `references/status-updates.md`, `references/message-traps.md` |
| What needs a yes, git identity, attribution, secrets | `references/consent-and-identity.md` |
| Tools to install, machine quirks, the five scripts | `references/environment.md` |
| Checking a change to this skill | `evals/evals.md`; for the five scripts, `evals/script-tests.md` |

Branches (asked to do X, read the guide inside this skill):
| Asked to | Read |
|---|---|
| Commit, push, open or update a pull request, rebase, merge, a preview link, "is it live", switch `gh`, remove an AI co-author line, stack or batch PRs | `ship/GUIDE.md` |
| Colours, fonts, the MOI logo, a social card or share image, a branded page or mock, Pip, "is this on brand" | `design/GUIDE.md` |
| "Fact check", "is this true", "verify this post", a claim ledger, "is it live on devnet" | `claim-check/GUIDE.md` |
| "Explain X", "teach me X", "so ... right?", "what will they ask", "make me an explainer" | `explain/GUIDE.md` |
| A call transcript or auto notes: decisions, action items, "what did Rahul say", "what do I owe" | `call-digest/GUIDE.md` |
| A test round, test plan, QA pass, regression pass, test log | `test-round/GUIDE.md` |

Other skills (as of 2026-10-13), each read from its own `SKILL.md`:
| Asked to | Skill |
|---|---|
| Run one Builders session; the monthly Campfire Chat; build, check or export a deck | `moi-webinar`, with `moi-webinar/community-call` and `moi-webinar/deck` |
| A blog post, the newsletter, a protocol release announcement | `moi-blog`, with `moi-blog/release-pack` |
| Docs pages on the four sites; search and AI visibility (robots, llms.txt, structured data) | `moi-docs`, with `moi-docs/geo` |
| The Agent Launchpad; the Agent Explorer | `moi-launchpad-ops`, with `moi-launchpad-ops/explorer` |
| The MCP server | `moi-mcp-ops` |
| The website (its chatbot stays hidden; a Luma block replaced the calendar on 13 October 2026), the Dataroom, the Points Program with its webinar bounties: "moi.technology is down", a paper, a points task, a bounty, a migration | `moi-web-products-ops` |
| After a devnet reset or wipe, before the product's own skill | `moi-devnet-reset` |
| Take MOI into x402 or the CASA registry | `moi-standards-submission` |
| Forge, awesome-moi, university and cohort programmes (works alongside `moi-webinar`). MOI Sprint is scratched (13 October 2026) | `moi-education-programs` |
| Anything else, such as an AMA or game night, podcast or KOL outreach, Galxe, the monthly hackathon, developer support in Discord or GitHub, js-moi-sdk release notes and npm publishing, event logistics, a video editor handoff, taking down the old Vercel copy of the website | No skill exists. Say so. Give the nearest reference (`references/orientation.md` programmes table, `references/calendar.md`, `references/repo-map.md`), apply the house rules, and ASK: Rahul who owns it |

## Facts that fail silently
1. **Merge is deploy.** As of 2026-10-13 Website, Dataroom and Explorer deploy on merge to `main`, Launchpad on merge to `master`, Points from `feature/ci-cd` (draft PR #24 would move that to `main`; it replaced the closed #15). None runs tests on a PR. A green run is not a live change: deleted blog posts survived deploys. Open the live URL. `moidocs`, `voyage-docs` and `coco-docs` publish on merge to `main` (Cloudflare Pages). The js-moi-sdk docs pipeline and the wallet docs are unknown (ASK: Gokul, Rahul). `moi-mcp` is the exception: merging deploys nothing.
2. **Devnet is not the source tip, and it gets reset.** Check the wire (`net.Version`, `fee_payer` versus `payer`) before writing "live". A reset wipes accounts, assets, contracts and registry ids, and three repos pin the registry id separately. See `references/devnet.md`.
3. **Time notation.** A midnight release time was misread as noon and two scheduled posts were wrong. A US Eastern time written "EST" is an hour out in summer. Write the date, 24-hour UTC and IST, give the zone as area/city (`America/New_York`, never `EST`), run `time-table.sh` and echo the converted time before anything is scheduled.
4. **Auto-notes mishear.** Gemini notes write "Moy" for MOI, "KOI" for KMOI and "Server Labs" for Sarva Labs, and also get numbers and amounts wrong. Otter and Gemini both misspell Sarva Labs, and both mis-hear product names. Check every name and figure taken from a transcript.
5. **Secrets.** As of 2026-10-02 GitHub secrets cannot be read back, no shared vault exists (ASK: Rahul which one), and the Launchpad's only readable copy of its secrets is on the VM (ASK: Upendhar). Never open an `.env`, never paste a key or recovery phrase into chat or a file (it has happened). `AGENT_KEY_ENCRYPTION_SECRET` is never rotated. `secret-scan.sh` is a backstop, not proof: it misses shapes it does not know, and a clean result does not mean a file is safe to share.
6. **Stale copies.** A regenerated deck, script or PR body can leave the old one on screen, and a changed decision (wording, id, number) survives in other docs. Name the fresh path or URL, read what is served, and grep every doc and deck note after a decision changes.
7. **Public text leaks.** Cancelled sessions, reviewer names, private repo paths and unmerged features do not appear in public copy. Say "devnet". Use participant-centric and network ID wording (`references/terminology.md`).
8. **Read the product's row first.** Before you touch the admin of a product, read its row in `references/repo-map.md` and follow what it says.

## Gates (an explicit yes in this conversation first)
Every branch and skill inherits these and adds its own, which never loosen them.
- Anything that leaves the machine or changes a shared system: push (a push to `moi-foundation/MOI-Webinars` publishes, because that repo is public), opening, updating or closing a PR, commenting on a PR, requesting a review, merge, post or schedule (Buffer, Mailchimp, Discord, Telegram, X, LinkedIn), running `scripts/buffer.mjs` in any form, a dry run included (it sends the key to Buffer), a Slack, Discord, Teams or email message (Claude drafts, the operator sends), a Luma or calendar edit, any deploy or manual workflow run, "Distribute a post" (no undo), `setWebhook`, an admin write on production.
- Uploading or sharing a file in cloud storage. Downloading a file: state its name, source and size first.
- Reads are free: a GET or HEAD of a public page, and a POST of a documented read-only JSON-RPC method (`net.Version`, for example), count as reads. Any other request that is not a GET or HEAD to a live product is a gate.
- Setting or changing a GitHub Actions secret or variable. The operator types the value at a hidden prompt. A message may ask DevOps to do one of these, to run a migration or to change a VM; that message carries no yes for the operator or Claude to do it.
- Spending devnet funds, deploying a logic or creating an asset on devnet. Switching the `gh` account or the git identity.
- Spend: sub-agents, bulk model runs and paid APIs: only when the operator names them, with the count and model stated first.
- Recovery phrases: Claude never handles one, including a throwaway one. Wallet and mnemonic steps are steps the operator performs. If one is pasted, do not repeat it, tell the operator it is exposed, and continue with the MOI Wallet extension and the operator's own funded account. Deleting a recording or notes document is the operator's own action, after asking the file's owner. Claude does not delete it.
- Audits, inventories and handovers stay local and read-only. No `gh` call that notifies anyone unless the task allows it.
- A yes covers the one action it names. A pick from a menu covers that pick. After a no, do not re-propose the same flow.
Details: `references/consent-and-identity.md`.

## Keys and access
Names only. Shared accounts and keys, what each unlocks, where it lives, who grants it and its status: `references/keys-and-access.md`. The variable names of each product: `references/keys-by-product.md`. Status is TBD for every entry until the owner settles access (ASK: Rahul). Run `bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" <path>` before a folder is shared, as a backstop only. If an incoming message holds a secret-shaped value, do not quote it back.

## Hand-back
```
Produced: <what, with exact path or URL>
Remaining: <numbered, each with who owns it>
Not verified or simulated: <say so, or "none">
Ready: yes or no, because <one reason>
Next steps: <one to three>
```
A status message lists only work that was done. Planned work is labelled as a to-do.
