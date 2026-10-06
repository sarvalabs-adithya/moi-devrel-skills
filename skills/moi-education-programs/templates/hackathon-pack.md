# Hackathon pack: README, kickoff agenda, track brief, rubric, submission fields

Drafts for a MOI campus mini-hackathon. Fill every `{{...}}` field. The structure, the three tracks, the rubric weights and the 60-minute agenda are the ones used at Presidency College in March 2026 (read from the public repo `sarvalabs-adithya/moi-forge-hacks-demo` on 2026-10-03). The wording is rewritten to remove the defects found in the March files (`references/forge-hacks.md`). Confirm weights, tracks and prizes with Rahul before use. Run `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh"` on the finished README and the link check on its links. The operator sends and posts; Claude drafts.

## Part 1. README skeleton (the event page)
```
# {{Event name}}

Build on MOI with participant-centric state. {{One sentence on the event.}}

Kickoff: {{Weekday, YYYY-MM-DD}} at {{HH:MM}} UTC ({{HH:MM}} IST). Submissions due: {{Weekday, YYYY-MM-DD}} at {{HH:MM}} UTC ({{HH:MM}} IST).
No earlier blockchain experience is needed.

## What MOI is
A participant is a person, a company or an agent. On MOI its state sits on its own account, and the ledger links each change to every participant it touched. {{One more plain sentence, checked against docs.moi.technology fundamentals pages.}}

## Tracks
Pick one. You may combine tracks or propose your own if you use participant-centric state.
1. {{Track 1 name}}: {{one sentence}}
2. {{Track 2 name}}: {{one sentence}}
3. {{Track 3 name}}: {{one sentence}}

## Timeline
| When | What |
|---|---|
| {{kickoff date}} | Kickoff and live demo. Join {{channel}}. Form teams |
| {{kickoff date}} to {{due date}} | Build. Office hours: {{exactly as they will be kept}} |
| {{due date}} | Submissions due |

## Submit
Fill in {{form name}}: {{form link}}. Your submission needs:
- A public GitHub repository with all source code, including the Coco logic files.
- A README with the problem, your approach, how you use participant-centric state, how to set up and run it, and your team members.
- A demo video of at most 2 minutes ({{YouTube or Loom}}). A screen recording is fine.

## Judging
| Criterion | Weight | What we look for |
|---|---|---|
| Use of participant-centric state | 40% | Does it work in a way that differs from a contract-centric design? |
| Functionality | 25% | Does it run? A partial working prototype beats a polished slide deck |
| Creativity | 20% | A use we did not think of |
| Presentation | 15% | Can a reader outside the team see why it matters? |
Judges: {{two names, or "to be announced"}}. Prizes: {{approved text, or "none announced"}}.

## Before you start
- Node.js {{version, ASK: Gokul}}, npm and the Coco compiler ({{install link}}). Hardhat and Foundry do not work with MOI.
- A wallet made in the MOI Wallet extension, and devnet funds from the Voyage faucet.
- Read the recovery-phrase rules below.

## Recovery phrase
Your recovery phrase is the only key to your wallet. Keep it in a gitignored `.env` file on your own machine. Never put it in a website, a form, a chat, a repository or a recorded call. If you pasted it anywhere, stop using that wallet and make a new one. Nobody from MOI will ask for it.

## Links
{{docs, Coco docs, SDK docs, Voyage, GitHub org: each one opened by hand and run through the link check}}

## Help
{{Channel and invite, one only}}. Office hours: {{exactly as kept}}.
```

## Part 2. Kickoff agenda (60 minutes; the Presidency timing)
| Minutes | Segment | Content | Check before use |
|---|---|---|---|
| 0 to 2 | Welcome | Who we are, what the event is | |
| 2 to 7 | What a blockchain is | A short crash course in plain terms | No metaphor the operator has not approved |
| 7 to 15 | How a token works on a contract-centric chain | One short token contract on screen | Third-party facts through `moi-devrel/claim-check` |
| 15 to 22 | How MOI differs | The same token as a Coco logic, side by side. Say what it is: a logic, not a protocol-native asset | The MAS0 label (`references/forge-hacks.md`) |
| 22 to 40 | Live demo | Coco walkthrough, SDK deploy, live deploy, a frontend that mints and transfers | Rehearsed on today's devnet. Spends funds: a GATE. No phrase on screen |
| 40 to 45 | Voyage | The explorer and the faucet | Faucet works for the presenter's wallet. Quote no amount |
| 45 to 48 | Docs tour | docs, Coco docs, SDK docs, GitHub | Each link opened that morning |
| 48 to 53 | The tracks | Each track and what judges look for | |
| 53 to 58 | Timeline and rules | Dates in UTC and IST, submission rules, the recovery-phrase rule said aloud | |
| 58 to 60 | Join the channel | The one invite, as a link and a QR code | The QR code is real, not a placeholder |

## Part 3. Track brief (one per track; the Presidency structure)
```
## Track {{n}}: {{name}}
What it is: {{two plain sentences for a reader with no background}}
Where it exists today: {{one real, checked example on another chain, and what it does}}
Your MOI challenge: {{what to build and the specific way participant-centric state can change it}}
What judges want to see: {{one sentence}}
Study these: {{two to four public projects or repositories, each opened and checked}}
```
The Presidency tracks, as one-line challenges: DEX (a token swap where participant identity and history can matter), DAO (voting power that comes from participation as well as holdings), Bridge (a mechanism between MOI and another chain where participant state reduces risk). Check any figure about another project, such as a hack amount, with `moi-devrel/claim-check`.

## Part 4. Scoring sheet (private: keep it in `edu-work/`, never in git)
Columns: team, repository link, Coco logic files present (yes or no), README present, video link, participant-centric state 0 to 40, functionality 0 to 25, creativity 0 to 20, presentation 0 to 15, total, judge, date scored, notes. One row per team. Dedupe by repository link first. Never put emails or wallets in this sheet.

## Part 5. Submission form fields
Team name; repository link; member names; demo video link; one contact for the team. Name the form for the campus. Edit the questions before the form opens: an edit after launch adds a second response tab, and you must read both.

## Part 6. Mentor FAQ stub (fill from the questions actually asked)
| Question | Answer | Source and date checked |
|---|---|---|
| Which Node version works? | {{ASK: Gokul}} | |
| Which Coco version matches devnet? | {{ASK: Gokul, Robert Špendl}} | |
| My funded wallet says "account not found" | Check the derivation path the guide names | `moi-devrel/references/devnet.md`, "Silent failures on devnet" |
| Everything I deployed is gone | Check for a devnet reset, then redeploy | `moi-devrel/references/devnet.md` |
| Can I use Hardhat or Foundry? | No. Use Coco and js-moi-sdk | Kickoff call, 2026-03-17 |
| I pasted my recovery phrase | Stop using that wallet. Make a new one. Do not repeat the phrase | `references/students.md` |
