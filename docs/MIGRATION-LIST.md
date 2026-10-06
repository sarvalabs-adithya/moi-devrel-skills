# What to migrate off my accounts

As of 6 October 2026. Names only, no values.

## Under my own accounts today: move to DevOps or a company login

| Product | What | Where it sits | Move to |
|---|---|---|---|
| Agent Launchpad | Supabase project (all app state) | My Supabase login | Company Supabase, paid plan with backups |
| Agent Launchpad | Telegram bot @moinetworkbot and the alert chat | My Telegram, via BotFather | Company Telegram account |
| Points Program | Supabase project (every user and every point) | My personal Supabase login, free plan, no backups | Company Supabase, paid plan with backups. Most urgent item on this list |
| Agent dating plugin | The repo | sarvalabs-adithya/agent-dating | sarvalabs org |
| Agent dating plugin | The relay VPS | Mine, being cancelled | Nothing to migrate. Remove the code that points at it (the relay address in install.sh and src/network.ts, the deploy workflow and its secrets) and leave the relay unconfigured. The project is inactive |
| Moinkee NFT Minter | The repo | sarvalabs-adithya/moinkee-nft-minter | sarvalabs org |
| Moinkee NFT Minter | Minting wallet and the collection asset | My devnet wallet, seed in the Vercel env | Company wallet, or take the site down |
| Contextual Compute website | The repo | sarvalabs-adithya/contextual-compute-foundation-website | sarvalabs org |
| Dataroom | Supabase project and bucket | My Supabase login | Company Supabase |
| MOI Website | Old copy at moi-website.vercel.app | My Vercel | Take down |
| Dataroom | Second static data room, sarva-dataroom.vercel.app | Vercel (whose account: confirm); code only on my Mac | Push to an org repo or take down |

## Secrets

The secrets themselves sit in each repo's GitHub Actions settings, not with me. What is missing is a note of where to get each one again if it is lost (which dashboard, which account). The names are already listed per product in the skills library (moi-devrel, keys-by-product); the "where to find it" part is still to write.

Not to migrate: the AgentMarket contract (the current one is not in use; whoever redeploys it does so from their own wallet), and Groq (the shared relay that needed it is gone).

## Owner not on record: settle who holds the login

| Product | Account |
|---|---|
| MOI Website | Supabase project (may be the Dataroom's), Anthropic and OpenAI keys for the chatbot, Tag Manager, Analytics, Search Console, Cloudflare Pages |
| Dataroom | Anthropic and OpenAI keys |
| Points Program | Google OAuth client, X developer app (paid), Discord app and bot, Telegram bot and group, Reown project, Resend account. Their secrets are in GitHub; who holds each account is not recorded |
| Agent Explorer | Server devnet wallet, Reown project, Pinata account, the GitHub token used for images |
| Moinkee NFT Minter | Vercel project, Pinata account |
| Contextual Compute website | Vercel project, the domain registration (renews by 2027-03-28), Cloudflare zone, the join-form webhook |
| Shared | Buffer organisation, Mailchimp, Luma, YouTube channel, the meeting account |
