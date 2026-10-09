# Agent Launchpad

**Status: active.** Live at launchpad.moi.technology. Paid agents (the AgentMarket contract) inactive.

The web app at launchpad.moi.technology where anyone can launch an AI agent on MOI: pick a template, register the agent on chain, and talk to it on Telegram. I built it and run it. DevOps owns the server it runs on.

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Codebase | Me | sarvalabs/moi-agent-launchpad deploys. I work in my fork, sarvalabs-adithya/moi-agent-launchpad |
| Database (Supabase) | Company Supabase organisation (transferred 8 October) | Holds all app state |
| Telegram bot and the alert chat | Me | @moinetworkbot delivers agent messages to users |
| AgentMarket contract on devnet | Me | Not redeployed since the devnet wipes, so paid agents are off. The code is there; the next owner redeploys it when it is needed |
| Server, CI/CD, container registry, Teleport | DevOps | |
| Domain launchpad.moi.technology | DevOps | |
| Registration wallets that activate new users | DevOps | |
| Agent registry on devnet | Protocol team | Its id changes on every devnet reset |

The full list of settings and secrets, by name, is in the dependencies doc and in `.env.example` in the repo.

## Process

**Shipping a change**

- Work on a branch in my fork.
- Run typecheck and tests myself. Nothing runs them on a pull request.
- If I changed an agent template or the agent runtime (the one file users download and run on their own laptop), rebuild that file and commit it. The repo serves the built copy.
- Open a pull request on the org repo.
- Merging to master builds a Docker image and deploys it to the server. Nothing is deployed by hand.
- Check the deploy run and the live site. A failed run leaves the old version serving, with no alert.

**Changing a setting or a secret**

- Set it in GitHub, under the repo's Actions secrets and variables.
- Run the deploy workflow by hand. Setting a value deploys nothing on its own.
- A new setting also needs a line in the deploy workflow.
- Never replace the agent key encryption secret: every stored agent key would be lost.

**Changing the database**

- Write the migration file.
- Run it by hand in the Supabase SQL editor, in order, before the code that needs it is merged.

**After a devnet reset**

- Get the new agent registry id from the Protocol team.
- Update it in the repo variables.
- Run the deploy workflow by hand.
- Check with DevOps that the registration wallets are funded again.
- Redeploy the AgentMarket contract if it was wiped.
- Sign in as a new user and register an agent, to prove it works.

**Checking it is healthy**

- Open launchpad.moi.technology and sign in.
- Look at the stats: registered agents should not be zero.
- Send the Telegram bot a message.

## Claude skill

The **moi-launchpad-ops** skill covers running the Launchpad. After a devnet reset, start with the **moi-devnet-reset** skill, which gives the order of work across every product.

| When | What to tell Claude | What the skill does |
|---|---|---|
| Something looks wrong | "Is the Launchpad healthy?" | Runs a read-only health check on the live site and says what each failure means. |
| Shipping | "Ship this Launchpad change." | Walks the branch, the local checks and the pull request, and says what merging will deploy. |
| A setting or secret | "I need to change this Launchpad setting: ..." | Says where it is set and whether it needs a deploy or a rebuild. It never sees the secret's value. |
| The database | "I need a migration for ..." | Writes the SQL and says when to run it. I run it in Supabase. |
| Devnet reset | "Devnet was reset. What do I redo?" | Confirms the reset, then lists the steps in order. |
| A user reports a problem | "A user says ..." | Finds the cause among the known cases and drafts the reply. |
| A bad deploy | "Roll back the Launchpad." | Gives the rollback steps. |

What the skill never does without my yes: push, merge (a merge deploys), change a secret, run a migration, or touch anything on the server. It never handles a wallet seed phrase.

## Open items

- Phone sign-in (PR #32) merged and deployed on 7 October after Upendhar rotated the registry login token. The QR sign-in is still off: add NEXT_PUBLIC_WC_PROJECT_ID as an Actions variable and run the deploy to switch it on. Test a real scan and a brand-new wallet first.
- Move every secret into a shared vault. Today the server's env file is the only readable copy.
- Transfer the Telegram bot to DevOps or a company Telegram account (steps in the migration list). The Supabase project was transferred on 8 October.
- Push the README and handover doc fixes. The ones in the repo still describe Vercel.
