# What to migrate off my accounts

As of 11 October 2026. Names only, no values.

## Under my own accounts today: move to DevOps or a company login

| Product | What | Where it sits | Move to |
|---|---|---|---|
| Agent Launchpad | Supabase project (all app state) | Done: transferred to the company Supabase organisation on 8 October | Check the plan has backups on |
| Agent Launchpad | Telegram bot @moinetworkbot and the alert chat | My Telegram, via BotFather | Company Telegram account |
| Agent dating plugin | The repo | sarvalabs-adithya/agent-dating | sarvalabs org, after PR #1 is merged: one transfer call, an org owner may have to accept |
| Agent dating plugin | The relay VPS | Mine, being cancelled | Done in sarvalabs-adithya/agent-dating PR #1 (11 October): no baked-in relay address, the installer asks for DATING_RELAY_URL, the deploy workflow and VPS scripts removed, the three VPS secrets deleted, a "Pick it up" guide in the README. Merge the PR |
| Moinkee NFT Minter | The repo | sarvalabs-adithya/moinkee-nft-minter | sarvalabs org, after PR #1 (the handover: README, env template, the April recovery routes behind a secret) is merged |
| Moinkee NFT Minter | Minting wallet and the collection asset | My devnet wallet, seed in the Vercel env | Nothing to move: the next owner makes a new devnet wallet and a new collection (README, Pick it up). What does move: the Vercel project (four variables) and the Pinata account, or its pins re-pinned under a company account; the CIDs stay the same |
| Contextual Compute website | The repo | sarvalabs-adithya/contextual-compute-foundation-website | sarvalabs org |
| Dataroom | Supabase project and bucket | Done: transferred to the company Supabase organisation on 8 October | Same |
| MOI Website | Old copy at moi-website.vercel.app | A Vercel project, team not yet found (a delete on 9 October did not take; the site still serves) | Find the team that holds it and delete the project |
| Dataroom | Second static data room, sarva-dataroom.vercel.app | A Vercel project, team not yet found (a delete on 9 October did not take; the site still serves) | Find the team that holds it and delete the project |

## How the Supabase projects move (done on 8 October; kept for the record)

The Launchpad and Dataroom projects sat in my personal Supabase organisation. Supabase moves a project between organisations in place: the project reference, the URL, the anon and service keys, the database, the storage bucket and the auth users all stay the same, so nothing in either app or in GitHub changes and there is no downtime.

1. DevOps creates the company Supabase organisation (or picks the existing one) on a paid plan. The transfer needs a paid plan on the receiving side, and a paid plan is what gives the projects daily backups, which they have never had.
2. DevOps invites my Supabase login to that organisation. The rule is: owner of the organisation the project leaves, member of the one it joins.
3. In the Supabase dashboard, for each project: Project Settings, General, Transfer project, choose the company organisation, confirm. Once for the Launchpad project, once for the Dataroom project.
4. What does not move and has to be redone by hand: organisation members (DevOps invites whoever needs the dashboard), any log drain, and project-scoped roles. Neither app uses the Supabase GitHub integration, so nothing there.
5. Check both apps: open launchpad.moi.technology and sign in, open dataroom.moi.technology and read a document. Both should behave exactly as before, because nothing they point at changed.
6. DevOps removes my login from the organisation. Billing for the two projects now lands on the company account.

Not part of this: the Points Program project is on the Points email account, not mine. The Website's Supabase project may be the Dataroom's one; confirm before assuming a third transfer.

## How the Telegram bot moves

The Launchpad bot @moinetworkbot was created from my Telegram account in BotFather. Ownership moves inside BotFather; the token and the chat id stay the same, so nothing in the app changes.

1. The receiving account (DevOps, or a company Telegram account) opens the bot and sends it a message, so Telegram knows it. It must not have the bot blocked.
2. My account needs two-step verification switched on for at least 7 days before the transfer, with the password unchanged, and the Telegram session I transfer from has to be at least 24 hours old.
3. In BotFather: /mybots, the bot, Transfer Ownership, choose the recipient, confirm. It cannot be undone.
4. The bot keeps running: the token in the GitHub secret stays valid and the webhook stays set. The new owner can later regenerate the token in BotFather; if they do, update TELEGRAM_BOT_TOKEN in the Launchpad's Actions secrets and run the webhook setup again, or messages stop arriving.
5. The alert chat: add the new owner's account to it. The chat id in ADMIN_ALERT_TELEGRAM_CHAT_ID does not change.

The Points Program has its own bot and group; who owns them is not recorded.

## Secrets

The secrets themselves sit in each repo's GitHub Actions settings, not with me. Where to get each one again if it is lost (which dashboard, which account) is written: ENV-VARS.md, one section per product, with the consoles and who holds each login.

Not to migrate: the Points Program's Supabase project (it is on the Points email account, not mine; it is still on the free plan with no backups, so a paid plan is worth doing when someone takes it over), the AgentMarket contract (the current one is not in use; whoever redeploys it does so from their own wallet), and Groq (the shared relay that needed it is gone).

## Owner not on record: settle who holds the login

| Product | Account |
|---|---|
| MOI Website | Cloudflare Pages. Settled: Tag Manager, Analytics and Search Console are under sarvalabsdeveloper@gmail.com; the chatbot keys and the calendar database are no longer used |
| Dataroom | Anthropic and OpenAI keys |
| Points Program | Google OAuth client, X developer app (paid), Discord app and bot, Telegram bot and group, Reown project, Resend account. Their secrets are in GitHub; who holds each account is not recorded |
| Agent Explorer | Server devnet wallet, Reown project, Pinata account, the GitHub token used for images |
| Moinkee NFT Minter | Vercel project, Pinata account |
| Contextual Compute website | Vercel project, the domain registration (renews by 2027-03-28), Cloudflare zone, the join-form webhook |
| Shared | Luma, YouTube channel, the meeting account. Settled: Chandra owns the Buffer organisation; Vardan has Mailchimp access |
