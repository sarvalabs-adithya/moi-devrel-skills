# Support: the questions that came up and the answers that were right

Facts are as of 2026-10-03, updated 2026-10-14 where a row says so. No ticket system, support log or FAQ file exists in the evidence. The answers below are reconstructed from the product's own messages, `docs/E2E-TESTING.md`, `docs/QA-LEDGER.md`, `docs/HANDOFF.md`, the README and the troubleshooting records. They are what the evidence supports, not a record of replies that were sent. Back to `../SKILL.md`.

## Where users ask, and who answers
- The dashboard sends unknowns to a Discord invite link (variable `NEXT_PUBLIC_DISCORD_INVITE_URL`). Questions also arrive in Telegram, on calls and from Rahul. Which channel is watched, and by whom, is not on record. ASK: Rahul.
- Launchpad user docs are live at launchpad.moi.technology/docs (PR #31, merged and deployed 12 October 2026): point users there first.
- Chain and registry questions go to Gokul. Anything on the VM goes to Upendhar. Product calls go to Rahul.
- Claude drafts the reply and the operator sends it. A reply in Discord or Telegram is a message on the operator's behalf: GATE.

## Run: answer a question
| # | Step | Command or action | Done when | Gate |
|---|---|---|---|---|
| 1 | Get the facts | Ask for the exact on-screen message (the app shows machine codes and wallet errors as they are), which part of the product, the wallet's active account, and desktop or phone | You have the message word for word | read-only |
| 2 | Check the product | `bash "$SKILLS/moi-launchpad-ops/scripts/launchpad-health.sh"`. If it is unhealthy, the cause is on our side: say so | You know whether it is the user or us | read-only |
| 3 | Match | Find the question in the table below. If none fits, use `troubleshoot.md` | One answer, or a new failure class | read-only |
| 4 | Draft | Plain words, short. Say what was and was not charged. Say honestly when the cause is on MOI's side | A draft the operator can send | local |
| 5 | Send | The operator posts it | Sent | GATE |
| 6 | Learn | A new failure class goes into the incident note and, through a PR, into this table | The note exists | local |

## Questions and answers
"Basis" names the source. "Inferred" means the answer is built from the code or the docs and was not seen in a real reply.
| Question | Answer | Basis |
|---|---|---|
| "I can't sign in" or "couldn't retrieve nonce" | A new wallet is only a keypair; the chain has never heard of it. On the connect page click Connect: it spots a new wallet and shows "One-time wallet setup". In the MOI Wallet extension finish its registration steps, copy the long code starting with 0x it then shows, paste it where the page asks ("Paste the setup code from your MOI Wallet") and press "Set up my wallet". It activates the wallet and signs you in. Wording as read on 2026-10-03: the connect page wording changed after 13 October (one-time wallet setup, Register it on Voyage, Come back here), so confirm with a real sign-in before quoting it | `app/connect/page.tsx` on `master`, QA ledger, E2E section 1. The README's button name for this is out of date |
| Sign-in or a purchase is blocked after switching accounts | The wallet's active account must match the account you are signed in as. Log out and reconnect | E2E section 0 |
| "My agent does not reply on Telegram" | Chat runs on your own computer. The downloaded runtime must be running under pm2 and Telegram must be linked with the deep link. After a change to the agent's template code, the installed copy keeps its old behaviour until you download its setup script again (or run the update line its log prints) and restart pm2. Settings edits reach a running copy by themselves | E2E section 10, `docs/specs/config-sync.md` |
| "It answered a few times and then stopped", or an AI error | Every agent runs on your own model key. A free Groq key works. The setup script asks for one and saves it. The shared model tier was retired on 2026-08-02 | `docs/HANDOFF.md` |
| "It says my agents need registering again", or asks me to re-download | The test network was reset. Use the button on the dashboard, and activate your wallet first if it asks. An agent from before 2026-08-03 whose key no longer decrypts cannot be recovered: create a new one | Reset notes, post-cutover checks 2.4 and 2.5 |
| The setup script fails with a 404 from the vercel.app host | The script was made on the old hosting. Download a fresh one from the production site | Inferred |
| "Why was my agent name refused?" | Names are unique across all live agents, ignoring case. Choose another | Migration 0008, `docs/HANDOFF.md` section 3 |
| "I paid, but it says it is not listed" | Paid agents are off in production (the AgentMarket contract is not redeployed; fact as of 13 October 2026), and the app says "Paid agents are temporarily unavailable while the payment contract is redeployed. Free agents are unaffected." When payments run, nothing is charged until the creator's listing is confirmed on-chain, a second subscribe returns the same copy without a second charge, and the chain enforces the exact price. Check the switch first (`architecture.md`) | `project-handover-docs/AGENT-LAUNCHPAD.md`, `lib/payments.ts`, E2E sections 6 and 12 |
| A wallet shows a pending interaction that never finishes, and nothing else goes through | In August 2026 the cure was a replacement interaction at the same sequence number with enough fuel, which needed a wallet build that lets you set the fuel limit. How it was done is not recorded (the previous DevRel's notes). ASK: Gokul. Do not improvise with a user's wallet | Research note on the August 2026 stuck-interaction incident. Inferred as a support answer |
| "Can I use my phone?" | Yes. On the connect page choose the phone QR sign-in and scan the code with your wallet app (live since 7 October 2026; since 13 October it also works when the extension is installed; tested 13 October). On a desktop the MOI Wallet extension works too | `project-handover-docs/AGENT-LAUNCHPAD.md` (the E2E known gap is out of date) |
| "Our side isn't ready on the new network yet" | Nothing is wrong with your wallet. The team has been alerted. Try again later. This message appears when the registration wallets are missing after a reset | `app/api/wallet/activate-public/route.ts`, `troubleshoot.md` row 14 |
| "Which model does it use, and what happens to my data?" | The agent uses the key you give it. A free Groq key is suggested and any supported provider works. The research records that `.env.example` says Groq does not retain or train on inputs; that is a claim about a third party, so check Groq's own page before repeating it to anyone, and say nothing about other providers' policies | Research note on `.env.example` (not re-read, because only variable names may be read from it) |
| "Who holds my agent's key?" | The README's security section says agent keys are encrypted at rest, decrypted only for the owner's one-time, authenticated setup-script download, and left out of every other response. No seed phrase or private key is entered on the site | README, Security posture |
| "Is this live?" or "Is this mainnet?" | It runs on devnet, a test network. A reset wipes accounts and contracts, so agents may need registering again. Say "devnet", not "Voyage devnet" | `moi-devrel/references/devnet.md` | <!-- slop-lint:ignore -->
| "Where do I report a bug?" | The Discord link on the dashboard. No monitored channel is on record: ASK: Rahul | Dashboard |

## How to word replies
- Brief and plain, no jargon. Say what happened, whose side it is on, and what to do next.
- Never ask for a recovery phrase, a private key or a token, and never accept one. If a user pastes one, do not repeat it and tell them to treat it as exposed (`moi-devrel/references/consent-and-identity.md`).
- Do not promise a date, a fix or paid agents. Do not quote an agent count without the read time (`health.md`).
- Use the house terms: devnet, participant, network ID (`moi-devrel/references/terminology.md`).
- A user who reports a security problem gets a short thanks and no detail. Tell the operator to pass it to Rahul at once. ASK: Rahul who receives security reports.
- Docs for the Launchpad do not belong in the protocol docs (Rahul, 2026-09-17: application docs belong with the app and use cases on moi.technology). Launchpad user docs live at launchpad.moi.technology/docs (PR #31, 12 October 2026). Other questions about where docs belong: `moi-docs`.

## Not yet known
- Which support channel is monitored, and any announcement template for reset notices to users. ASK: Rahul.
- Whether any FAQ exists outside the repos.
