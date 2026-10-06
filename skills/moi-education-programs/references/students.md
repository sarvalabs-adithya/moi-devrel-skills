# What a student needs before day one

Facts are as of 2026-10-03. Every row comes from a prerequisite that a MOI student document recorded. Where documents disagree the row says so and the answer is an ASK. `moi-devrel/explain` teaches the operator the mechanism so they can present it; it has no student-audience path, so student-facing text is written plainly from `moi-devrel/references/glossary.md` and checked with `moi-devrel/claim-check`. Back to `../SKILL.md`.

## The list
| # | A student needs | For | Recorded in | Conflict or caution |
|---|---|---|---|---|
| 1 | A laptop that runs Node and the Coco compiler | All programmes | Coco install page: macOS, Linux and Windows | The student's operating system was never recorded. Windows installs differ (a setup program or a manual unpack) |
| 2 | Node.js and npm | Sprint, Forge Hacks, Chapter 1 | Sprint scaffolds: "Node.js v18+". `moi-sprint` README and Chapter 1: v16+. The first Sprint prototype README (previous operator's machine): 20+ | Three answers. The scaffolds use Vite 5, `js-moi-sdk` 0.9.0-rc2 declares no `engines` field. Proposed default until settled: 18 or newer. ASK: Gokul which is right |
| 3 | The Coco compiler (`coco version` must print a version) | Compiling any `.coco` file | cocolang.dev/docs/install. Downloads: cocolang.dev/docs/releases | awesome-moi pins `coco-0.7.0` and links GitHub releases that answer 404. The newest release is v0.9.2 (2026-09-28) and rejects `enlist` endpoints. Which version fits today's devnet: ASK: Gokul or Robert Špendl |
| 4 | A code editor. The Coco extension for VS Code is optional | Writing logic | awesome-moi `coco-language/README.md` | |
| 5 | A MOI wallet with a recovery phrase the student made and keeps | Signing every interaction | Sprint READMEs: "Your wallet mnemonic (12 or 24 words)". Forge guide: "Generate IOMe Id" on Voyage | "IOMe" is the earlier name. Voyage moved its login to MOI Wallet in late August 2026 (announcement post dated 2026-08-27); MOI Wallet is a browser extension and a phone app. Check what Voyage offers today |
| 6 | Devnet funds from the Voyage faucet (voyage.moi.technology/faucet/), after the wallet is registered on chain | Paying fuel for every interaction | All student documents | The faucet funds accounts that already exist; it stopped creating them (the post blog.moi.technology/article/move-your-voyage-login-to-moi-wallet/, 2026-08-27). The student documents do not say how to register first: ASK: Gokul for the current step. The amount is 20K in two documents and 100K in others: never quote one |
| 7 | A GitHub account | Cloning, and submitting a public repo | Forge Hacks README | A work or personal choice for the student. Not MOI's concern |
| 8 | Discord, and Telegram for announcements; a WhatsApp group for a campus cohort | Questions, mentors, office hours | Forge README and guide | The invite and the channel differ between documents (`forge-hacks.md`) |
| 9 | A way to record a 2-minute screen video, and YouTube or Loom | Hackathon submission | Forge Hacks README | |
| 10 | Basic JavaScript and async/await. React or Next.js familiarity for Chapter 1 | Sprint | Sprint site; Chapter 1 | Forge Hacks: "No prior blockchain experience required" |
| 11 | Time | Planning | Sprint site: 1 to 2 hours (Soulbound), 2 to 4 hours (Swap). Hackathon: a 1-hour kickoff and 14 days. Cohort: 12 weeks | Hours a week for the cohort were never recorded |
| 12 | Not Hardhat or Foundry | Hackathon | Presidency kickoff call | They do not work on MOI. Use Coco and js-moi-sdk |

## The network the student uses
The scaffold READMEs name `https://dev.voyage-rpc.moi.technology/devnet`. Say "devnet" and nothing else (`moi-devrel/references/terminology.md`). `net.Version` answered 0.13.0 on 2026-10-03. Do not hardcode it in new material: the SDK has a default devnet provider and webinar code uses it (`moi-devrel/references/devnet.md`).

## The day-one check (read-only; a student can run it)
1. `node --version` and `npm --version`.
2. `coco version`.
3. `curl -s -X POST https://dev.voyage-rpc.moi.technology/devnet/ -H 'content-type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"net.Version","params":[]}'`. It prints a version. If it prints an error, devnet or the student's network is down: stop and ask in the channel.
4. Open the wallet, register it on chain (the current step: ASK: Gokul), claim the faucet, wait, and look the account up on voyage.moi.technology. The explorer can lag by minutes.
5. Deploy nothing yet. The first deploy is a step of the programme, on a funded wallet.

## The recovery-phrase paragraph (put it in every student document)
Say this in plain words, on the first page, and repeat it before the first deploy:
- The recovery phrase is the only key to the wallet. It goes in a gitignored `.env` file on the student's own machine, nowhere else.
- Never type it into a website, a form, a chat, a repo or a recorded call. Check `.gitignore` before the first commit.
- If it was pasted anywhere, treat the wallet as exposed: stop using it and make a new one.
- Nobody from MOI will ask for it. The operator never asks for one, never reads one and never keeps one. Claude never handles one, including a throwaway.
This paragraph was in the Forge Hacks README on 2026-03-17 and was removed the same morning (`forge-hacks.md`). Do not repeat that.

## The first things that go wrong (all from `moi-devrel/references/devnet.md`)
| Symptom | Cause | Say |
|---|---|---|
| The faucet says the account does not exist | The faucet only funds accounts that already exist on chain (Voyage post, 2026-08-27) | Register the wallet first, then claim |
| "account not found" on a funded wallet | The wallet was derived on another path. Faucet wallets use `m/44'/6174'/7020'/0/0`, SDK-only wallets use `m/44'/6174'/0'/0/N` | Use the path the guide names |
| Assets, logics and balances are gone | A devnet reset wipes accounts, assets, logics and funds. Full wipes were recorded on 2026-08-15 and 2026-09-11 | Keep the deploy scripts; redeploy; claim again |
| A transfer "succeeded" but nothing moved | Simulation accepts what the chain later refuses, and a refused transfer still has a hash | Read the receipt status |
| The wallet is stuck | A pending interaction blocks it | Replace it with a new interaction at the same nonce and enough fuel |
| A tutorial's amounts or ids are wrong | Constants moved at v0.13.0 (the KMOI asset id, the fuel floor, the default storage fund) | Take constants from the SDK, never from a document |

## Not yet known
- The students' operating systems and the Node version that really works with the pinned packages. ASK: Gokul.
- Which Coco version matches devnet. ASK: Gokul, Robert Špendl.
- Whether any support channel is staffed after a programme ends. ASK: Rahul.
