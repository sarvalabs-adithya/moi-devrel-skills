# What to migrate off Adithya's accounts

**Status: in progress.** Both Supabase projects moved on 8 October and the agent dating plugin no longer depends on a VPS. The repo transfers wait on Rahul's answer on which organisation each repo goes to. The Telegram bot, the Pinata account and two orphan Vercel projects are still to move or delete.

Marketing: Owner not on record: settle who holds the login, and Open items. Developers: every section.

As of 13 October 2026, this lists what still sits under Adithya's own accounts and where each item should go, plus the steps for the two moves that need a walkthrough (Supabase, done; Telegram, pending). Names only, no values.

## Under Adithya's own accounts today: move to DevOps or a company login

| Product | What | Where it sits | Move to |
|---|---|---|---|
| Agent Launchpad | Supabase project (all app state) | Done: transferred to the company Supabase organisation on 8 October | Check the plan has backups on |
| Agent Launchpad | Telegram bot @moinetworkbot and the alert chat | Adithya's Telegram, via **BotFather** (Telegram's own bot for creating and managing bots) | Company Telegram account |
| Agent dating plugin | The repo | sarvalabs-adithya/agent-dating | sarvalabs org, one transfer call (an org owner may have to accept). PR #1 is merged, so the transfer is unblocked; it waits on Rahul's answer on which organisation it goes to |
| Agent dating plugin | The relay VPS | Adithya's, being cancelled | Done in sarvalabs-adithya/agent-dating PR #1 (merged): no baked-in relay address, the installer asks for DATING_RELAY_URL, the deploy workflow and VPS scripts removed, the three VPS secrets deleted, a "Pick it up" guide in the README |
| Moinkee NFT Minter | The repo | sarvalabs-adithya/moinkee-nft-minter | sarvalabs org. The handover PR is merged: it is PR #2 (the README, the env template, the April recovery routes behind a secret); PR #1 was replaced to remove Claude authorship. The transfer waits on Rahul's answer on which organisation it goes to |
| Moinkee NFT Minter | Minting wallet and the collection asset | Adithya's **devnet** wallet (devnet is the shared MOI test network), seed in the **Vercel** env (Vercel hosts the app) | Nothing to move: the next owner makes a new devnet wallet and a new collection (README, Pick it up). What does move: the Vercel project (four variables) and the **Pinata** account (Pinata keeps files online by "pinning" them under content addresses called CIDs), or its pins re-pinned under a company account; the CIDs stay the same. Pinata is on Adithya's account today, and Srikar is creating a company Pinata account to transfer it to |
| Contextual Compute website | The repo | sarvalabs-adithya/contextual-compute-foundation-website | sarvalabs org, once Rahul says which organisation |
| Dataroom | Supabase project and bucket | Done: transferred to the company Supabase organisation on 8 October | Same |
| MOI Website | Old copy at moi-website.vercel.app | Done: deleted on 14 October 2026 (the address answers 404) | Delete the project. Keep this item open until the site stops answering |
| Dataroom | Second static data room, sarva-dataroom.vercel.app | Still serving on 14 October 2026 after the other Vercel deletes: the project sits in a Vercel team nobody has found. Find it and delete it | Delete the project. Keep this item open until the site stops answering |

## How the Supabase projects move (done on 8 October; kept for the record)

The Launchpad and Dataroom projects sat in Adithya's personal Supabase organisation. Supabase moves a project between organisations in place. The project reference, the URL, the **anon and service keys** (the public key the browser uses and the private key only servers use), the database, the storage bucket and the auth users all stay the same, so nothing in either app or in GitHub changes and there is no downtime.

1. DevOps creates the company Supabase organisation (or picks the existing one) on a paid plan. The transfer needs a paid plan on the receiving side, and a paid plan is what gives the projects the daily backups they have never had.
2. DevOps invites Adithya's Supabase login to that organisation. The rule is: owner of the organisation the project leaves, member of the one it joins.
3. In the Supabase dashboard, for each project: Project Settings, General, Transfer project, choose the company organisation, confirm. Do it once for the Launchpad project and once for the Dataroom project.
4. Some things do not move and have to be redone by hand: organisation members (DevOps invites whoever needs the dashboard), any **log drain** (a feed that ships a project's logs to another service) and project-scoped roles. Neither app uses the Supabase GitHub integration, so nothing there.
5. Check both apps: open launchpad.moi.technology and sign in, open dataroom.moi.technology and read a document. Both should behave exactly as before, because nothing they point at changed.
6. DevOps removes Adithya's login from the organisation. Billing for the two projects now lands on the company account.

Not part of this: the Points Program project is on the points@moinetwork.io account (managed by Sai Kiran; kept there because the company organisation is at its free-plan limit, see POINTS-PROGRAM.md), not Adithya's. The Website's Supabase project is probably the Dataroom's one; confirm before assuming a third transfer.

## How the Telegram bot moves

Adithya created the Launchpad bot @moinetworkbot from his Telegram account in BotFather. Ownership moves inside BotFather, and the token and the chat id stay the same, so nothing in the app changes.

1. The receiving account (DevOps, or a company Telegram account) opens the bot and sends it a message, so Telegram knows it. It must not have the bot blocked.
2. Adithya's account needs two-step verification switched on for at least 7 days before the transfer, with the password unchanged. The Telegram session the transfer is made from has to be at least 24 hours old.
3. In BotFather: /mybots, the bot, Transfer Ownership, choose the recipient, confirm. It cannot be undone.
4. The bot keeps running: the token in the GitHub secret stays valid and the **webhook** (the address Telegram posts the bot's new messages to) stays set. The new owner can later regenerate the token in BotFather. If they do, update TELEGRAM_BOT_TOKEN in the Launchpad's Actions secrets and run the webhook setup again, or messages stop arriving.
5. The alert chat: add the new owner's account to it. The chat id in ADMIN_ALERT_TELEGRAM_CHAT_ID does not change.

The Points Program has its own bot, held under sarvalabsdeveloper@gmail.com. Who owns its group is not recorded.

## Secrets

The secrets themselves sit in each repo's GitHub Actions settings, not with Adithya. If one is lost, ENV-VARS.md says where to get it again (which dashboard, which account): one section per product, with the consoles and who holds each login.

Not to migrate: the Points Program's Supabase project and the **AgentMarket** contract. The Points project is on the points@moinetwork.io account (managed by Sai Kiran; kept there because the company organisation is at its free-plan limit, see POINTS-PROGRAM.md), not Adithya's. It is still on the free plan with no backups, so a paid plan is worth doing when someone takes it over. The AgentMarket contract is the paid-agent marketplace contract; the current one is not in use, and whoever redeploys it does so from their own wallet.

Groq: no company-owned Groq key exists. The key the Launchpad server uses is not a company key, and whose account holds it is not recorded. The next owner creates a company key at console.groq.com/keys and sets GROQ_API_KEY before relying on it.

## Owner not on record: settle who holds the login

| Product | Account |
|---|---|
| MOI Website | Cloudflare Pages, on the company-owned Cloudflare account. Settled: Tag Manager, Analytics and Search Console are under sarvalabsdeveloper@gmail.com. The chatbot and the Express server stay (MOI-WEBSITE.md); the chatbot's keys are not company keys, and the Supabase project they use is not recorded |
| Dataroom | Anthropic and OpenAI keys: no company account holds them, and the keys now set are not company keys; the next owner creates company keys |
| Points Program | Settled 13 October: the Google OAuth client, X developer app (paid), Discord app and bot, Telegram bot, Reown project and Resend account are all under sarvalabsdeveloper@gmail.com. Their secrets are in GitHub |
| Agent Explorer | Server devnet wallet, Reown project, Pinata account, the GitHub token used for images |
| Moinkee NFT Minter | Vercel project deleted on 14 October 2026. The Pinata account is Adithya's (see above and OTHER-PROJECTS.md) |
| Contextual Compute website | Vercel project, the domain registration (renews by 2027-03-28), the join-form webhook. The Cloudflare zone is company-owned |
| Shared | Luma, Riverside, Google Meet and YouTube: Vardan holds them per ENV-VARS.md; confirm the account. Settled: Chandra owns the Buffer organisation; Vardan has Mailchimp access |

## Open items

- The Moinkee, Agent dating and MOI Sprint repos and the Pinata move: steps in OTHER-PROJECTS.md.

- The repo transfers go to the sarvalabs organisation (decided 14 October 2026): agent-dating, moinkee-nft-minter, moisprint, tSwapper, contextual-compute-foundation-website. Steps in OTHER-PROJECTS.md.
- Where the MOI Website is deployed. MOI-WEBSITE.md describes a VM; the MOI Website row above says Cloudflare Pages. Neither is verified; ask DevOps (Srikar).
- Who holds the Luma, Riverside, Google Meet and YouTube accounts: ENV-VARS.md says Vardan; confirm.
- moi-website.vercel.app, moinkee-nft-minter.vercel.app and moisprint.vercel.app were deleted on 14 October 2026 (404). sarva-dataroom.vercel.app still answered 200 after that: its Vercel project is in a team nobody has found; find and delete it.
- Whose account holds the Launchpad's Groq key, and who holds the Agent Explorer accounts: not recorded.
