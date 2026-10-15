# What to migrate off Adithya's accounts

**Status: done for DevRel.** Both Supabase projects moved on 8 October, and the agent dating plugin no longer depends on a VPS. On 14 October four repos moved to the sarvalabs organisation, the orphan Vercel projects were deleted, and the Moinkee files were pinned in the company Pinata account. The Launchpad Telegram bot was transferred to Rahul Lenkala the same day.

Marketing: Owner not on record: settle who holds the login, and Open items. Developers: every section.

This doc is current as of the end of 14 October 2026. It lists what sat under Adithya's own accounts and where each item went. It also has the steps for the two moves that needed a walkthrough, Supabase and Telegram, both done. It gives names only, no values.

## What sat under Adithya's accounts, and where it went

| Product | What | Where it sat | Where it went |
|---|---|---|---|
| Agent Launchpad | Supabase project (all app state) | Adithya's personal Supabase organisation | Done 8 October: the company Supabase organisation (owned by sarvalabsdeveloper@gmail.com). It is on the free plan, so there are no automatic backups |
| Agent Launchpad | Telegram bot @moinetworkbot and the alert chat | Was on Adithya's Telegram, through **BotFather** (Telegram's own bot for creating and managing bots). Done: transferred on 14 October 2026 | Rahul Lenkala's Telegram account (@p2pbuddy) |
| Agent dating plugin | The repo | Done: moved to sarvalabs/agent-dating on 14 October 2026 (it was sarvalabs-adithya/agent-dating) | sarvalabs org |
| Agent dating plugin | The relay VPS | Adithya's, now cancelled | Nothing: retired. Done in agent-dating PR #1 (merged). The plugin has no baked-in relay address, and the installer asks for DATING_RELAY_URL. The deploy workflow and VPS scripts are removed, the three VPS secrets are deleted, and the README has a "Pick it up" guide |
| Moinkee NFT Minter | The repo | Done: moved to sarvalabs/moinkee-nft-minter on 14 October 2026 (it was sarvalabs-adithya/moinkee-nft-minter) | sarvalabs org. The handover PR is merged: it is PR #2 (the README, the env template, and the April recovery routes behind a secret). PR #1 was replaced to remove Claude authorship |
| Moinkee NFT Minter | Minting wallet and the collection asset | Adithya's **devnet** wallet (devnet is the shared MOI test network), with its seed in the **Vercel** env (Vercel hosts the app) | Nothing to move. The next owner makes a new devnet wallet and a new collection (README, Pick it up). What did change: the Vercel project was deleted on 14 October. The **Pinata** files (Pinata keeps files online by "pinning" them under content addresses called CIDs) were uploaded again to the company Pinata account on 14 October with identical CIDs, and all 71 are pinned. Adithya's Pinata account no longer matters and can be closed |
| Contextual Compute website | The repo | Done: moved to sarvalabs/contextual-compute-foundation-website on 14 October 2026 (it was sarvalabs-adithya/contextual-compute-foundation-website) | sarvalabs org |
| Dataroom | Supabase project and bucket | Adithya's personal Supabase organisation | Done 8 October: the same company organisation, same free plan |
| MOI Website | Old copy at moi-website.vercel.app | Done: deleted on 14 October 2026 (the address answers 404) | Nothing |
| Dataroom | Second static data room, sarva-dataroom.vercel.app | Done: deleted on 14 October 2026 (the address answers 404) | Nothing |
| All | The product demo videos and the Launchpad launch video folder in Google Drive | Owned by adithya@moinetwork.io. Since 14 October the folders are open to anyone at moinetwork.io, and Rahul is invited | Sharing does not move ownership. If that account is closed, the files go with it. Transfer ownership to Rahul, or ask IT to transfer the files when the account is closed |

## How the Supabase projects move (done on 8 October; kept for the record)

The Launchpad and Dataroom projects sat in Adithya's personal Supabase organisation. Supabase moves a project between organisations in place. The project reference, the URL, the **anon and service keys** (the public key the browser uses and the private key only servers use), the database, the storage bucket and the auth users all stay the same. So nothing in either app or in GitHub changes, and there is no downtime.

1. Pick the receiving organisation. On 8 October it was the company organisation, owned by sarvalabsdeveloper@gmail.com, on the free plan (two projects at most, no automatic backups). A paid plan would add daily backups.
2. DevOps invites Adithya's Supabase login to that organisation. The rule is that he must be an owner of the organisation the project leaves and a member of the one it joins.
3. In the Supabase dashboard, for each project: Project Settings, General, Transfer project, choose the company organisation, confirm. Do it once for the Launchpad project and once for the Dataroom project.
4. Some things do not move, so you redo them by hand: organisation members (DevOps invites whoever needs the dashboard), any **log drain** (a feed that ships a project's logs to another service) and project-scoped roles. Neither app uses the Supabase GitHub integration, so there is nothing to redo there.
5. Check both apps. Open launchpad.moi.technology and sign in. Open dataroom.moi.technology and read a document. Both should behave exactly as before, because nothing they point at changed.
6. DevOps removes Adithya's login from the organisation. Billing for the two projects now lands on the company account.

Not part of this: the Points Program project is on the points@moinetwork.io account, not Adithya's. Sai Kiran manages it. It is kept there because the company organisation is at its free-plan limit (see POINTS-PROGRAM.md). The Website's Supabase project is probably the Dataroom's one. Confirm before assuming a third transfer.

## How the Telegram bot moved (done on 14 October; kept for the record)

Adithya created the Launchpad bot @moinetworkbot from his Telegram account in BotFather. Ownership moves inside BotFather. The token and the chat id stay the same, so nothing in the app changes.

1. The receiving account opens the bot and sends it a message, so Telegram knows it. The receiving account must not have the bot blocked.
2. Adithya's account needs two-step verification switched on for at least 7 days before the transfer, with the password unchanged. The Telegram session the transfer is made from has to be at least 24 hours old. On 14 October Telegram first refused the transfer under the 7-day rule. A later try the same day went through, and the bot is now on Rahul Lenkala's Telegram account (@p2pbuddy).
3. In BotFather: /mybots, the bot, Transfer Ownership, choose the recipient, confirm. It cannot be undone.
4. The bot keeps running. The token in the GitHub secret stays valid, and the **webhook** (the address Telegram posts the bot's new messages to) stays set. The new owner can later regenerate the token in BotFather. If they do, update TELEGRAM_BOT_TOKEN in the Launchpad's Actions secrets and run the webhook setup again, or messages stop arriving.
5. The alert chat: add the new owner's account to it. The chat id in ADMIN_ALERT_TELEGRAM_CHAT_ID does not change.

The Points Program has its own bot, held under sarvalabsdeveloper@gmail.com. Who owns its group is not recorded.

## Secrets

The secrets themselves sit in each repo's GitHub Actions settings, not with Adithya. If one is lost, ENV-VARS.md says where to get it again (which dashboard, which account). It has one section per product, with the consoles and who holds each login.

Not to migrate: the Points Program's Supabase project and the **AgentMarket** contract. The Points project is on the points@moinetwork.io account, not Adithya's. Sai Kiran manages it, and it is kept there because the company organisation is at its free-plan limit (see POINTS-PROGRAM.md). It is still on the free plan with no backups, so a paid plan is worth doing when someone takes it over. The AgentMarket contract is the paid-agent marketplace contract. The current one is not in use, and whoever redeploys it does so from their own wallet.

Groq: the Launchpad no longer uses a server key (every agent runs on its owner's own key), so there is nothing to migrate.

## Owner not on record: settle who holds the login

| Product | Account |
|---|---|
| MOI Website | Hosted on a DevOps VM (deploys go through Teleport), with Cloudflare in front, on the company-owned Cloudflare account. Settled: Tag Manager, Analytics and Search Console are under sarvalabsdeveloper@gmail.com. The chatbot and its Express server are not running, and their Supabase project no longer exists (MOI-WEBSITE.md) |
| Dataroom | Anthropic and OpenAI keys: no company account holds them, and the keys now set are not company keys. The next owner creates company keys |
| Points Program | Settled 13 October: the Google OAuth client, X developer app (paid), Discord app and bot, Telegram bot, Reown project and Resend account are all under sarvalabsdeveloper@gmail.com. Their secrets are in GitHub |
| Agent Explorer | Server devnet wallet, Reown project, Pinata account, the GitHub token used for images |
| Moinkee NFT Minter | Vercel project deleted on 14 October 2026. The Pinata files are pinned in the company account since 14 October (see above and OTHER-PROJECTS.md) |
| Contextual Compute website | Settled 14 October 2026: the Vercel project is on the sarvalabsdeveloper@gmail.com Vercel account, and the domain (Namecheap, renews by 2027-03-28) and the Cloudflare zone are company-owned. The join form's webhook is not set, so sign-ups are discarded (see OTHER-PROJECTS.md) |
| Shared | Luma, Riverside, Google Meet and YouTube: Vardan holds them per ENV-VARS.md. Confirm the account. Settled: Chandra owns the Buffer organisation, and Vardan has Mailchimp access |

## Open items

- The Google Drive video folders: move ownership off adithya@moinetwork.io before that account is closed (see the table).
- Who holds the Luma, Riverside, Google Meet and YouTube accounts: ENV-VARS.md says Vardan. Confirm.
- Who holds the Agent Explorer accounts (AGENT-EXPLORER.md): not recorded.
- Agent Explorer deploys are broken. Its GH_TOKEN Actions secret (set 31 July) is refused by GHCR (GitHub's container registry), so the 7 October and 14 October deploys failed at "Login to GHCR". PR #6 (deprecated agents hidden, never auto-verified) is merged (aa9488c6) but not live. The live site is a build from 8 October, deployed by hand, and 70 deprecated agents still show as verified until the deploy runs. Upendhar has been asked to replace GH_TOKEN with a token that has write:packages and re-run the deploy.
