List of dependencies:

As of 4 October 2026. No secret value is written here, only names and where to find them. (confirm) marks what neither the code nor GitHub settles.


1. Community Call:

   a. Variables:
      i. Slide deck
      ii. Luma (Vardan)
      iii. Riverside (Vardan)
      iv. Pre call and post call tweets + shorts (Vardan)

   b. Handover: moi-webinar Claude skill. Its community-call branch covers the
      line-up, what each segment owes, the numbers ledger, the release slides,
      the host's question, the day itself and the recording description. Its
      deck branch builds and checks the deck and exports the PDF. A cleaned
      copy of the September deck is in the skill as a worked example.

   c. Process: The call is monthly, in the 3rd or 4th week. Vardan keeps the
      dates (CC15 is expected Fri 23 Oct 2026, reserve 30 Oct: confirm). A
      planning call about a week before fixes the segments and who presents:
      protocol, DevRel, product, marketing, partnerships, close. The protocol
      and DevRel slides are mine. I collect what each segment owes: the
      release note from the protocol team (kept unedited, every "live" checked
      against the node), the AI visibility report and community numbers from
      Sai Kiran, event facts and photos from marketing. I build the deck with
      the skill (one idea per slide, every figure written down with its source
      before it goes on a slide), run the checker, export the PDF, and write a
      script only for my own slides. I read it aloud once the day before. On
      the day Vardan has the Luma page and the Riverside room ready and I
      present from the deck with the presenter window. After the call Vardan
      posts the tweets and shorts, and I write the recording description with
      chapters and links.

   d. ToDo:
      i. Commit the September (CC14) deck and the Builders intro deck. Neither
         is in a repo yet. Decide with Rahul where call folders live (the
         webinars repo is public).
      ii. Fix both decks. Each prints a correct PDF but is broken in the
         browser: CC14's slides 11 and 12 fall out of frame in a small window,
         and the intro deck's arrow keys and presenter window are dead. The
         skill's checker flags both.
      iii. Figures on the September deck were never confirmed (47 queries, 221
         of 226 responses, the community numbers). Ask Sai Kiran before CC15
         reuses them.
      iv. No recording description or recap exists for CC14. Find who holds
         the recording and which YouTube channel it goes to (owner: confirm).
      v. Confirm for CC15: date, start time, host, line-up (Vardan, Rahul).
      vi. Put the moi-webinar skill in a repo.


2. Dev Webinars:

   a. Variables:
      i. Slide Deck
      ii. Luma
      iii. Pre session posts (buffer)
      iv. Session Bounty
      v. Gmeets link (Vardan)
      vi. Post session blog
      vii. Codebase (moi-foundation/MOI-Webinars)

   b. Handover: moi-webinar Claude skill (topic and storyline, the demo, run
      of show, Luma copy, pre session posts, game day, bounty; its deck branch
      builds the deck and the script) and moi-blog Claude skill (the post
      session blog, announcing it, the newsletter). In the repo: README.md for
      the series, then each session's own README.md.

   c. Process: Meet with Rahul a week before the webinar and discuss ideas for
      a project to build, finalize the project 5 days before the session and
      create a luma. As soon as luma is created schedule a linkedin and x post
      for the same day. Then 3 more x and linkedin posts 2 days before, 1 day
      before and 1 hour before. I have created a custom claude skill,
      moi-webinar, that takes care of the slide deck, helps with lesson
      planning and also schedules posts on buffer after approval from the
      user. The API key for buffer must be set up (BUFFER_API_KEY in a .env at
      the repo root, made by the Buffer organisation owner) but the rest works
      the same. The scheduling script is scripts/buffer.mjs, on the branch
      claude/agent-payments-simple, not on main. A post scheduled that way
      publishes with nobody reviewing it, so I use drafts unless an exact time
      matters. The moi-blog skill drafts the post session blog, and both skills
      carry what they need on the MOI tech stack and blog writing.

   d. ToDo:
      i. Finalize the existing bounty list and finalize the bounty system on
         the points program. Session 8's challenge is in the Points code but
         switched off (Points Program, ToDo 7).
      i-b. Make the session bounty extensible: whoever runs a webinar creates
         its bounty on the Points site themselves, without a code change.
         Today each bounty is a task hard-wired in the code plus a deploy.
      ii. Land the unmerged work. Sessions 8 and 9, the x402 work and the
         scheduling script are on a branch 95 commits ahead of main with no
         PR. Six more commits and the event copy for sessions 7 and 8 (Luma
         text, runbook, social posts) are not pushed yet. Ask Rahul how
         session folders should land: the branch's commits carry an AI
         co-author line, so not as a PR from that branch.
      iii. The session 8 write-up is not published. PR #52 on the website
         holds an older draft: swap in the 4 September draft or close it.
      iv. Decide whether session 9 (planned, never delivered) is dropped and
         what number the next session takes.
      v. Rehearse any old session on today's devnet before reusing it. None
         has been run since the 11 September wipe.
      vi. Settle Buffer: who owns the Buffer organisation, and which of the
         two routes a session uses (scripts/buffer.mjs with BUFFER_API_KEY, or
         the blog's workflow with BUFFER_ACCESS_TOKEN).
      vii. Put both skills in a repo.


3. Agent Launchpad:

   1. Stack:
      1. Supabase — Postgres for all app state
      2. Next.js 14 + TypeScript + Tailwind — the web app and every API route
      3. js-moi-sdk + js-moi-agent-registry — all on-chain calls, MOI devnet
      4. Coco — the AgentMarket contract for marketplace payments. Not
         redeployed since the devnet wipes, so paid agents are off (confirm)
      5. Telegram bot (@moinetworkbot) — delivers agent messages to users
      6. WalletConnect — phone sign-in by QR. Written, not merged: production
         signs in with the desktop wallet extension only
      7. Docker + GitHub Actions + Teleport — build and deploy to the DevOps VM
      8. Agent runtime — one bundled file users run on their own laptop under pm2

   2. Variables:
      1. Codebase (sarvalabs/moi-agent-launchpad deploys, my fork
         sarvalabs-adithya/moi-agent-launchpad is where I work)
      2. Supabase project (Adithya)
      3. Telegram bot and the alert chat (Adithya)
      4. WalletConnect project id (Adithya; only the unmerged phone sign-in
         uses it)
      5. Groq API key for internal calls (Adithya)
      6. AgentMarket contract on devnet (Adithya, deployer wallet)
      7. VM, CI/CD, container registry, Teleport (DevOps)
      8. Domain launchpad.moi.technology (DevOps)
      9. Registration wallets that activate new users (DevOps)
      10. Agent registry logic on devnet, id changes on every devnet reset
          (Protocol team)

   3. Env vars:

      1. Where they live:
         1. Production: GitHub → sarvalabs/moi-agent-launchpad → Settings →
            Secrets and variables → Actions. Secrets there cannot be read back.
         2. Production, the readable copy: /opt/moi-agent-launchpad/.env on
            the VM, reached through Teleport (DevOps)
         3. Local: .env.local in the repo, copied from .env.example
         4. Anything starting NEXT_PUBLIC_ is baked into the Docker image at
            build time, so changing it needs a rebuild, not a restart. Only
            three reach the build today: NEXT_PUBLIC_APP_URL,
            NEXT_PUBLIC_MOI_EXPLORER_URL, NEXT_PUBLIC_WALLET_INSTALL_URL
         5. A new variable needs a line in deploy.yml (it writes a fixed list
            of names to the VM), and a new NEXT_PUBLIC_ one also needs an ARG
            in the Dockerfile and a --build-arg in the build workflow

      2. Needed to boot:
         1. SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY — Supabase dashboard →
            the project → Settings → API
         2. SESSION_SECRET — generate with: openssl rand -hex 32
         3. AGENT_KEY_ENCRYPTION_SECRET — copy it from the VM env file.
            Never generate a new one, every stored agent key would be lost
         4. MOI_RPC_URL — leave empty. The code uses the SDK's built-in devnet
            endpoint, and the host in .env.example does not resolve
         5. MOI_PLATFORM_MNEMONIC — the funded devnet wallet, in Actions
            secrets and the VM env file. The code uses it for registry reads
            and the heartbeat (the README calls it optional: confirm)
         6. NEXT_PUBLIC_APP_URL — https://launchpad.moi.technology

      3. Telegram:
         1. TELEGRAM_BOT_TOKEN — Telegram → BotFather → /mybots →
            moinetworkbot → API Token
         2. TELEGRAM_BOT_USERNAME — moinetworkbot
         3. TELEGRAM_WEBHOOK_SECRET — generate with: openssl rand -hex 20,
            then re-run setWebhook or messages stop arriving. If it is unset
            the secret is derived from SESSION_SECRET, so rotating that one
            would stop Telegram too
         4. ADMIN_ALERT_TELEGRAM_CHAT_ID — the chat that receives alerts

      4. Chain:
         1. MOI_AGENT_REGISTRY_LOGIC_ID — from whoever redeployed the
            registry. The one value to change after a devnet reset
         2. MOI_AGENT_MARKET_LOGIC_ID — printed by
            contracts/agent_market/deploy.mjs. deploy.yml does not pass it
            yet, so setting it also needs a deploy.yml edit

      5. Activating new users:
         1. MOI_REGISTRATION_MNEMONIC_1, _2, _3 — ask DevOps, never copy
            them around
         2. or MOI_REGISTRATION_API_URL + MOI_REGISTRATION_API_KEY — also
            DevOps, not in use today

      6. The rest:
         1. GROQ_API_KEY — console.groq.com/keys
         2. CRON_SECRET — generate with: openssl rand -hex 32. Only for calling
            the cleanup route by hand: the cleanup runs inside the app every
            6 hours
         3. INBOX_WAIT_MS — 20000, hard-coded in deploy.yml
         4. GLOBAL_DAILY_SPEND_CAP_CENTS — 500
         5. NEXT_PUBLIC_MOI_EXPLORER_URL, NEXT_PUBLIC_WALLET_INSTALL_URL —
            values are in .env.example
         6. Phone sign-in branch only, not on master: NEXT_PUBLIC_WC_PROJECT_ID
            (cloud.reown.com → the project → Project ID) and
            NEXT_PUBLIC_MOI_CHAIN_ID

      7. Full list with comments: .env.example in the repo

   4. Handover: docs/HANDOFF.md in the repo (operator guide; on master its top
      still describes Vercel, my corrected copy is local) + moi-launchpad-ops
      Claude skill covering env vars, deploy, runbook and decisions (its
      explorer branch covers the Agent Explorer)

   5. Process: I work on a branch, run typecheck and tests, then open a PR on
      the org repo. CI runs neither, so my local run is the only gate. Merging
      to master builds a Docker image and deploys it to the VM on its own,
      nothing is deployed by hand. A failed run leaves the old container
      serving with no alert, so I check the run and the live site. If I touch
      the templates or the runtime I rebuild the runtime bundle and commit it.
      New database migrations are run by hand in the Supabase SQL editor, in
      order (nothing records which of the 12 are applied: confirm 0012). After
      a devnet reset I update the registry logic id in the repo variables and
      then run the deploy workflow by hand, because setting the variable
      deploys nothing. I redeploy the market contract if it was wiped.

   6. ToDo:
      0. Deploys are blocked as of 2026-10-07: the GHCR login step fails
         ("denied") with the GHCR_PAT secret set on 2026-07-31; the last good
         deploy was 2026-09-15. DevOps rotates the token (write:packages,
         read:packages) and re-runs the workflow. Production runs the
         15 September build until then.
      1. PR #32 (phone sign-in, new-wallet registration, two fixes) merged
         2026-10-07, not deployed yet (item 0). Set NEXT_PUBLIC_WC_PROJECT_ID as an Actions variable to
         switch the QR sign-in on. Then push or drop the rest of the unpushed
         work: one local-only branch (stats and script
         names, 3 commits), the labs folder and four helper scripts
      2. The AgentMarket contract stays as it is: paid agents are off and the
         next owner redeploys it when needed
      3. Move every secret into a shared vault. Today the VM env file is the
         only readable copy
      4. Transfer the Supabase project, Telegram bot, WalletConnect and Groq
         accounts to a company login
      5. Push the README, deploy doc, HANDOFF and env template fixes. They are
         written, not pushed, and master still says Vercel


4. MOI Website:

   1. Stack:
      1. React 19 + Vite 7 + React Router 7 + Tailwind 4, Three.js, GSAP — the
         site at moi.technology: home, why-moi, manifesto, papers, calendar admin
      2. Express 4 in server/ — chat and calendar API at moi.technology/api
      3. Supabase — documents (chatbot) and community_calls (calendar); the SQL
         files at the repo root are run by hand and may not match production
      4. Chatbot (Claude, OpenAI embeddings) — hidden since 2026-06-08, so no
         chat on the live page on 2026-10-04; the route is in the code, untested
      5. Community calendar — on 2026-10-04 the API answers 500 and the live
         bundle calls the dev host, so the homepage shows three AMA dates from
         the code (17 Oct, 13 Nov, 11 Dec), none confirmed
      6. Astro 5 — blog.moi.technology, in blog/ of the same repo. The same
         markdown feeds the listing at moi.technology/blog, RSS, sitemap, llms.txt
      7. scripts/ + social/ — announce a post: Buffer drafts for X and LinkedIn
         (Discord, Telegram not used since 2026-08-31); Mailchimp mails from
         /rss-email.xml on the 15th of every month (RSS campaign)
      8. GitHub Actions + Teleport — start a script on the VM that builds and
         restarts the server (nginx 1.24); PR previews on the VM and Cloudflare
      9. Tag Manager, Analytics, Search Console — measurement

   2. Variables:
      1. Codebase (sarvalabs/MOI-Website, main deploys; I push to it, no fork)
      2. VM, Teleport, nginx, preview VM, TLS, DNS, VM deploy script (DevOps)
      3. Supabase project, Anthropic and OpenAI keys (owner: confirm)
      4. Tag Manager, Analytics, Search Console, Cloudflare Pages (owner: confirm)
      5. Buffer, Discord webhook, Telegram bot, Mailchimp (owner: confirm)
      6. Zoom account for call links (owner: confirm); call and AMA dates (Vardan)
      7. Old copy sarvalabs-adithya/moi-website at moi-website.vercel.app (Adithya)

   3. Env vars:

      1. Where they live:
         1. Production: GitHub → sarvalabs/MOI-Website → Settings → Secrets and
            variables → Actions. Secrets there cannot be read back
         2. Production, the readable copy: the env file the deploy script writes
            on the VM, via Teleport (DevOps). Issue #9 says server/.env but the
            code reads .env in the repo root: confirm which
         3. Local: .env at the repo root, copied from .env.example, only for the
            Express server and npm run ingest. Both sites build with none
         4. VITE_ values are baked in at build (redeploy to change). Secrets
            reach the VM only at deploy, and only the names deploy.yml lists

      2. The server and the build:
         1. ANTHROPIC_API_KEY, OPENAI_API_KEY — the two consoles → API keys
         2. SUPABASE_URL, SUPABASE_KEY — Supabase dashboard → the project →
            Settings → API (which project, and anon or service key: confirm)
         3. VITE_CHATBOT_API — the browser's API address. The live bundle has
            the dev host baked in; likely fix https://moi.technology or empty
            (untried, confirm with DevOps)
         4. ADMIN_API_KEY — generate with: openssl rand -hex 32. deploy.yml on
            main does not pass it; the change that passes it is local, not merged
         5. ALLOWED_ORIGINS, PORT — values in .env.example. deploy.yml does not
            pass them, so DevOps sets them on the VM (confirm)
         6. Passed by deploy.yml, read by nothing in production: VITE_GA_ID,
            PUBLIC_GA_ID (Tag Manager measures instead), DATA_ROOM_CHAT_URL (dev
            proxy only). DATA_ROOM_API_KEY: old Vercel function only, not passed

      3. Announcing a post, GitHub secrets only (no secret, channel skipped):
         1. BUFFER_ACCESS_TOKEN — Buffer; only the organisation owner can make one
         2. BUFFER_CHANNEL_X, BUFFER_CHANNEL_LINKEDIN — run npm run buffer:channels
         3. DISCORD_WEBHOOK_URL — Discord → Server Settings → Integrations
         4. TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID — BotFather, bot added as admin
         5. BLOG_ORIGIN — optional, in no template, passed by no workflow

      4. Deploy access (DevOps): secrets TELEPORT_PROXY, TELEPORT_JOIN_TOKEN,
         TELEPORT_NODE, VM_USERNAME; variables PREVIEW_VM_HOST, PREVIEW_VM_USER

      5. Full list with comments: .env.example in the repo

   4. Handover: no operator guide in the repo yet. Start with README.md,
      DEPLOYMENT.md, CONTENT.md, blog/README.md and social/README.md; the first
      four are partly wrong on main, corrected copies are uncommitted on my
      laptop (ToDo 7). Claude skills: moi-web-products-ops (site, chatbot,
      calendar, settings, health) and moi-blog (posts, announcing, newsletter),
      in ~/moi-devrel-skills/skills on my Mac, not in a repo yet

   5. Process: I work on a branch and push it to the org repo. No PR runs lint
      or tests, only the preview build, so I run npm run lint, npm run build and
      npm run build --prefix blog first (only the blog build checks a post).
      Merging to main (or a manual run on main) runs Deploy MOI Website:
      Teleport, then a script on the VM that is in no repo; per issue #9
      (2026-08-11) it pulls the branch, builds, copies into nginx and restarts
      the Express process under pm2. Nothing is deployed by hand. One markdown
      file feeds both builds, so both must run, and a green run proves little: I
      open the live page. No rollback, I revert in a new PR. Merging a post
      announces nothing: Prepare social copy opens a PR, I rewrite the copy and
      merge it, then run Distribute a post as a dry run and once for real (no
      undo). Since 2026-08-31 that is X and LinkedIn only, as Buffer drafts I
      publish by hand. A new page also needs a line in public/sitemap.xml. A
      devnet reset needs nothing here, the site makes no chain calls.

   6. ToDo:
      1. The calendar admin check is unsafe unless DevOps already sets its own
         key on the VM (confirm); the fix is local, not pushed (branch
         local/sweep-oct1). Before merging it, a repo admin creates the
         ADMIN_API_KEY secret and DevOps confirms the VM script hands it on.
      2. Calendar: the API answers 500 and the live bundle asks the dev host;
         both need fixing (issue #3 is about the chat). Get DevOps to read the
         "Fetch calls error:" log line, find the Supabase project (it may be the
         Dataroom's), create only the community_calls table and index, never the
         placeholder INSERT, fix VITE_CHATBOT_API, redeploy. Fallback dates end
         2026-12-18.
      3. The chatbot is parked (decided 2026-10-07): no work for now. If it
         ever comes back: Back: pick model and store (issue #3:
         the store's function name differs), load the litepaper the site serves
         (docs/ holds an older file), remove {false && ( in HomePage.jsx. Gone:
         delete route, widget, docs/, ingest.
      4. PR #57 (prerender, performance) is open, mergeable, unreviewed as of
         2026-10-04. Merge moidocs #124 first (open, changes requested).
      5. DevOps, nginx: the try_files rule #57 needs, a real 404 for unknown
         addresses, the discovery Link header, a download header on /papers
         PDFs. Also ALLOWED_ORIGINS and PORT, and the deploy script into the repo.
      6. #52, #54 and #56 were closed on 2026-10-07. Ask Upendhar to close
         #8 (his Cloudflare test). Close issue #9 if the blog deploy is
         finished.
      7. Push the corrected README, DEPLOYMENT, CONTENT and blog/README (local
         only); fix CLAUDE.md and DESIGN_SYSTEM.md, still the old look.
      8. Take down moi-website.vercel.app, archive the old fork, delete
         vercel.json and api/ after #57.
      9. Move the accounts to company logins, every secret to a shared vault,
         and the two skills into a repo.


5. Dataroom:

   1. Stack:
      1. Next.js 16 + React 19 + TypeScript + Tailwind 4 + pdfjs-dist — the
         site, the admin page and every API route, in moi-data-room/. The PDF
         viewer loads its worker from cdnjs
      2. Supabase — Postgres with pgvector and the private investor-docs
         bucket. No login, the whole site is open. adopters, document_leads
         and documents.require_email were made by hand, in no SQL file
      3. pdf-parse, mammoth + OpenAI text-embedding-3-small — read each upload
         and index it. PDF and Word work, PPTX cannot be read. 2026-10-04: 23
         documents, 17 indexed, 5 stuck, 1 failed
      4. Claude (claude-sonnet-4-20250514) — the chat, answers only from the
         indexed documents. Widget hidden since 2026-08-21, route still
         deployed. The website's server code does not call it
      5. GitHub Actions + SSH key — deploy to the DevOps VM behind nginx 1.24,
         by a script that is on the VM, not in the repo. Last deploy 2026-08-22

   2. Variables:
      1. Codebase (sarvalabs/moi-dataroom0 deploys and is public; my fork is
         public and stale, I push branches to the org repo). 60 commits: 46
         mine, 10 Srikar, 4 Claude. Repo admins: gokul, chandra, srikar, git, me
      2. Supabase project: database and bucket (owner: confirm; the website
         chatbot may use the same one)
      3. The documents: whitepaper, litepaper, decks, papers; 3 link to
         doi.org records (owner: confirm)
      4. Anthropic and OpenAI API keys, the admin secret, and who may read the
         captured email leads (owner: confirm)
      5. VM, nginx (what it forwards for /api: confirm), the SSH key, domain
         dataroom.moi.technology, and the deploy script on the VM (DevOps).
         Srikar wrote the workflow; does he still own the VM? (confirm)
      6. A second, static data room (Sarva Labs Confidential Data Room),
         sarva-dataroom.vercel.app, on Vercel (whose account: confirm). Code
         only on my Mac, ~/dataroomsarva (Adithya)

   3. Env vars:

      1. Where they live:
         1. Production: GitHub → sarvalabs/moi-dataroom0 → Settings →
            Secrets and variables → Actions. Cannot be read back. The deploy
            hands six of them to the VM script
         2. Production, the readable copy: on the VM, through DevOps (confirm)
         3. Local: moi-data-room/.env.local, copied from .env.local.example
            (my Mac only for now, the repo has no template)
         4. A changed secret needs a manual run of the workflow. NEXT_PUBLIC_
            values are baked in at build: a rebuild, not a restart
      2. Needed to boot:
         1. NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY —
            Supabase dashboard → the project → Settings → API
         2. SUPABASE_SERVICE_ROLE_KEY — same page. Server side only
         3. ANTHROPIC_API_KEY — console.anthropic.com → API keys
         4. OPENAI_API_KEY — platform.openai.com → API keys. Missing, every
            upload ends failed and the chat answers without document text
         5. ADMIN_SECRET — generate with: openssl rand -hex 32. Never leave it
            empty. Production has one (lock screen showed on 2026-10-04)
      3. Chat limits, optional, defaults in the code, set by nothing (a DevOps
         job): CLAUDE_PER_IP_HOURLY_LIMIT 30, CLAUDE_DAILY_TOKEN_BUDGET
         500000, CLAUDE_MAX_INPUT_TOKENS 8000, CLAUDE_MAX_OUTPUT_TOKENS 2048.
         Reset on every restart
      4. Read by the code, set by no deploy: ADMIN_TOKEN (one admin check,
         ToDo 1, nothing reads it after my local fix) and DATAROOM_URL (only
         scripts/set-whitepaper.mjs, default is the live site)
      5. Deploy access (DevOps): VM_HOST, VM_USERNAME, VM_SSH_KEY
      6. Full list with comments: .env.local.example (my Mac only, ToDo 6)

   4. Handover: nothing usable on GitHub (AGENTS.md is Vercel boilerplate,
      SECURITY_VULNERABILITY_ANALYSIS.md is empty). Read supabase/*.sql and
      the header of scripts/set-whitepaper.mjs. A README, env template and
      new AGENTS.md exist only on my Mac. Claude skill moi-web-products-ops
      (the dataroom-* files and traps) covers deploy, documents, secrets,
      SQL and the health check. Ask me for the security note before touching
      admin.

   5. Process: I work on a branch pushed to the org repo, run npx tsc
      --noEmit, npm run lint and npm run build myself (no PR check, no
      tests), open a PR and merge it, no reviewer on record. Merging to main
      runs Deploy MOI Dataroom: SSH to the VM, then a script that lives
      there. Nothing checks the site afterwards, so I open it, phone too. No
      rollback, I revert in a new PR. A database change is a SQL file run by
      hand in the Supabase SQL editor before the code merges (whose login:
      confirm). A new document is not a deploy: I upload it in the admin page
      (PDF or Word, under 50 MB), wait for completed, then ask the chat route
      a question only that file answers. The whitepaper swap is
      scripts/set-whitepaper.mjs. A deploy resets the chat limits and may
      strand an upload (confirm). No chain calls, nothing to redo after a
      devnet reset.

   6. ToDo:
      1. Security: one admin check is open to anyone in production (as of
         2026-10-04) and the others are unsafe. The fix is written
         (branch local/sweep-oct1), not pushed. ADMIN_SECRET is
         set in GitHub, so it will not lock admin out. Merge it, redeploy,
         treat the old admin password as leaked and change ADMIN_SECRET
      2. Decide if the repo, the site and the chat route stay open to anyone:
         the repo is public, the site has no login, the server skips the
         email gate on 3 documents
      3. Six documents are not indexed (2026-10-04): GTM Deck failed (likely
         no text in the file); Whitepaper, IM Deck, Tokenomics Overview,
         Parallelism in shared spaces, Truth of Happiness are stuck.
         Re-index one at a time, ask DevOps for the log on any left
      4. Two whitepaper rows: Whitepaper (home tile, stuck), White Paper (no
         tile, indexed). Find which is v2.1, keep a copy, delete the other.
         The swap script renames the tile's document to "Litepaper" on every
         run: fix it first
      5. Home page figures are typed into src/lib/constants.ts, no source
         recorded. My fork says 2,100+ nodes, the live page 100. Source or
         drop
      6. Push the README, env template and AGENTS.md (done locally) after
         fixing three README lines (sign-in, website chat, a command that
         types the secret). Add a migration for adopters, document_leads and
         require_email
      7. Get the deploy script into the repo (it sits in /root, the login is
         an SSH key, others use Teleport), add a PR check and a post-deploy
         check. Move secrets into a shared vault. Confirm who owns the
         Supabase project (plan, backups) and the two API keys
      8. Decide on the Events page (hidden since 2026-08-22) and the second
         data room (push to an org repo or take it down). /home failed to
         load on a phone on 2026-08-22, cause unknown: test on a real phone
      9. Delete the three stale branches on the org repo and archive the old
         fork sarvalabs-adithya/MOI-dataroom


6. Agent dating Plugin:

   1. Stack:
      1. TypeScript 6 + Node 22 — an OpenClaw plugin, version 1.2.0. Two
         agents with their own wallets register on the MOI registry, find
         each other and talk
      2. js-moi-sdk 0.7.0-rc15 + js-moi-agent-registry 0.1.1 — identity
         and discovery on chain. Both old: npm has 0.9.0-rc2 and 0.3.0-rc1
         (as of 2026-10-04)
      3. relay/broker.mjs — one file, no dependencies. Passes messages,
         serves the live viewer at /app, keeps history as plain files
      4. systemd + GitHub Actions + ssh — runs the broker on one VPS and
         deploys it on a push to master that touches the broker
      5. Docker Compose — two test agents on one host. Not the relay
      6. A model key through OpenClaw — the agents' replies. Optional,
         canned lines without one
      7. install.sh — one-command agent setup on someone's machine

   2. Variables:
      1. Codebase sarvalabs-adithya/agent-dating (public, my account, never
         moved to the org). master is current, last commit 2026-07-16.
         Nothing in my clone is unpushed (checked 2026-10-04)
      2. The relay VPS at 187.124.119.232, port 8787, plain http. Healthy
         on 2026-10-04 with 3 agents connected (owner: confirm who pays
         for it and who holds the root login)
      3. GitHub secrets holding an ssh key for root on that VPS (Adithya)
      4. Two demo agent wallets and their seed phrases (Adithya)
      5. Model API key, OpenAI or Anthropic (Adithya, which one: confirm)
      6. The faucet key the relay uses to fund new wallets (Adithya, who
         issued it: confirm)
      7. Devnet and its agent registry, new id after every reset
         (Protocol team)

   3. Env vars:

      1. Where they live:
         1. Relay: /root/dating-relay.env on the VPS, if it exists
            (confirm). The service file sets the port and data folder
         2. Deploy: GitHub → sarvalabs-adithya/agent-dating → Settings →
            Secrets and variables → Actions. VPS_HOST, VPS_USER and
            VPS_SSH_KEY are set, VPS_PORT is optional and not set.
            Secrets there cannot be read back
         3. Agents set up with install.sh: OpenClaw's config on that
            machine (openclaw config set plugins.entries.agent-dating...),
            and the wallet file in ~/.agent-dating
         4. Two-agent demo: .env copied from .env.example
      2. Relay (relay/broker.mjs), all optional:
         1. RELAY_TOKEN — shared secret agents must send, empty is open.
            generate with: openssl rand -hex 32, same value as each
            agent's DATING_RELAY_TOKEN. The build's default is empty;
            whether the live relay has one: confirm
         2. RELAY_PORT, RELAY_DATA, RELAY_PUBLIC_VIEW, RELAY_WHEEL_TTL, and
            four limits starting RELAY_RL_ — defaults are fine
         3. MOI_FAUCET_KEY, MOI_FAUCET_URL — the devnet faucet key (ask
            Protocol team who issues it: confirm) and an optional address
            template for it. Without the key the faucet answers "not
            configured"
      3. Per agent:
         1. MOI_MNEMONIC — the agent's wallet seed phrase. install.sh creates
            and funds one; scripts/gen-keys.mjs fills the two demo slots. A
            throwaway devnet wallet, never one with real funds
         2. DATING_RELAY_URL, DATING_RELAY_TOKEN, MOI_NETWORK and the persona
            names — your choice; the relay address defaults to the one in
            src/network.ts
         3. OPENAI_API_KEY (or an Anthropic key pasted into install.sh) — the
            agents' replies. Optional, canned lines without one
      4. Full list: .env.example (agent side), ARCHITECTURE.md section D
         (relay side)

   4. Handover: the repo's own docs. Root: README.md, USAGE.md,
      ARCHITECTURE.md, SECURITY.md, TESTING.md, CLAUDE.md. In docs/:
      DEPLOYMENT.md (how it ships and recovers; its backup and watchdog
      parts still say docker), PRODUCTION.md (done and left),
      DEMO-RUNBOOK.md. No Claude skill covers it; moi-devnet-reset lists
      it in one row. The repo's skills/agent-dating/SKILL.md is for the
      agents, and the moi-agent-dating skill in the Session 3 folder of
      MOI-Webinars is a separate thing

   5. Process: parked. master's last commit is 2026-07-16 and three side
      branches were pushed up to 2026-07-27, but the relay still runs. I
      worked on a branch or straight on master in my own repo. CI runs on
      every push: install, typecheck, broker syntax check, broker tests. A
      push to master that changes relay/broker.mjs, the service file or the
      apply script also runs deploy.yml (it can be started by hand too),
      which tests, copies the broker to the VPS over ssh, restarts
      dating-relay, waits for /health and puts the old file back if it
      fails (last run 2026-07-16, passed). The plugin has no deploy: each
      machine runs git pull (or install.sh again) and restarts its
      gateway. After a devnet reset I fund the wallets again and register
      each agent again, and may need a newer registry package, because the
      installed one embeds an old registry id (confirm). The relay's files
      survive a reset

   6. ToDo:
      1. The VPS is being cancelled. Remove the code that points at it (the
         relay address in install.sh and src/network.ts, deploy.yml and its
         VPS secrets) and leave the relay unconfigured. The project is
         inactive
      2. Put the two demo agents' seed phrases and the model key in a shared
         vault (where each is kept today: confirm)
      3. CI has been red since 2026-07-16: the typecheck step cannot find
         the openclaw package, so the broker check and the tests behind it
         never run on pushes. deploy.yml has its own test step, so deploys
         still ran. Add the package as a dev dependency or drop the step
      4. Merge or drop the three unmerged branches pushed up to
         2026-07-27: groq-duo, moi-wallet, token-optimization. Two older
         unrelated branches, wallet-app and claude/readme-update-e4gp4g,
         can go
      5. Move the repo to the org and the VPS to a company login, and
         rotate the root ssh key then. Back up /root/relay-data (chats,
         keys, cards, leaderboard), no backup is on record
      6. The relay address is baked into install.sh and src/network.ts. Put
         a domain in front before the next release
      7. Upgrade both chain libraries before running it on devnet again
      8. Decide if it is alive. The relay's counters showed no message
         passed since it last started, about 2026-09-11 06:18 UTC (read
         2026-10-04). If not alive, stop the service and archive the repo


7. Contextual Compute website:

   1. Stack:
      1. Next.js 14.2 + React 18 + Tailwind 4 + Framer Motion 12 — a
         one-page marketing site: hero, thesis, six papers, a join form
      2. One API route — the join form posts each email to a webhook
      3. Papers — a list in src/components/Papers.tsx. CC0 and CC2 open PDFs
         that the site serves itself from public/docs/. The other four
         cards are marked locked
      4. Vercel — hosting through its GitHub connection. No workflow in
         the repo

   2. Variables:
      1. Codebase sarvalabs-adithya/contextual-compute-foundation-website
         (public, my account). 7 commits, last 2026-04-10. GitHub main is
         what is live
      2. Vercel project (owner: confirm which login or team)
      3. Domain contextualcompute.org, live on 2026-10-04, apex redirects
         to www. The registrar is Namecheap and the registration runs to
         2027-03-28 (whois, 2026-10-04). DNS is on Cloudflare, and mail
         for the domain is forwarded through Namecheap (owner: confirm who
         holds each login)
      4. Where join-form emails end up, the webhook's destination (owner:
         confirm)
      5. The mailbox info@sarva.ai that the page links (owner: confirm)

   3. Env vars:
      1. Where they live: Vercel → the project → Settings → Environment
         Variables. The repo has no .env.example
      2. SUBSCRIBE_WEBHOOK_URL — the address the join form posts each email
         to. The only variable the code reads. Nothing in the repo says
         where it points (confirm). Unset, the form still says thank you
         and keeps nothing

   4. Handover: none, and none needed beyond this section. The README is
      the unedited Next.js template. No Claude skill covers it

   5. Process: I edit, push to main, and Vercel builds and publishes it as
      Production (GitHub shows six Production builds, the last on
      2026-04-10 for the current main). To add a paper I add an entry in
      src/components/Papers.tsx, and put the PDF in public/docs/ if the
      site hosts it. Nothing in it is a security risk

   6. ToDo:
      1. Confirm SUBSCRIBE_WEBHOOK_URL is set in Vercel and where it goes.
         If it is not, every sign-up is thrown away
      2. Two changes are not pushed: an edit to Papers.tsx (CC2 to point at
         a Zenodo record instead of the site's own PDF) and five paper PDFs,
         of which CC4 and CC5 are in no repo. Commit or drop the edit, and put
         the PDFs somewhere shared and private, not in this public repo
      3. The PDF of CC3, which the page shows as locked, is still served at
         its file address (200 on 2026-10-04), and it sits in the public
         repo's history. Remove it from public/docs/ if locked should mean
         locked, knowing the history keeps it
      4. Confirm who owns the domain registration (renews by 2027-03-28),
         the Cloudflare zone, the Vercel project, the webhook and the
         mailbox
      5. Move the repo to the org and reconnect Vercel to it


8. Moinkee NFT Minter:

   1. Stack:
      1. Next.js 16.1 + React 19.2 + Tailwind 4 — the Moinkee World Tour
         site, where visitors mint a memento NFT
      2. Three.js with react-globe.gl — the globe
      3. js-moi-sdk 0.7.0-rc8 — mints on MOI devnet. Old: npm has
         0.9.0-rc2 (as of 2026-10-04)
      4. Pinata — keeps the images and each token's metadata on IPFS
      5. Vercel — hosting through its GitHub connection. vercel.json gives
         the mint, token and Pinata routes 15 seconds

   2. Variables:
      1. Codebase sarvalabs-adithya/moinkee-nft-minter (public, my account).
         main has 7 commits, last 2026-02-26, and is what is live. Branch
         claude/ipfs-pinata-metadata-kLRqz has 15, last 2026-04-13, pushed
         and not merged
      2. Vercel project moinkee-nft-minter. moinkee-nft-minter.vercel.app
         answered 200 on 2026-10-04 (owner: confirm)
      3. Pinata account and its API token. 71 files were pinned on
         2026-04-13 (owner: confirm)
      4. The minting wallet, which authorises and pays for every mint
         (Adithya; seed phrase in Vercel and in .env.local on my Mac)
      5. The collection's asset on devnet, new after every reset (Adithya)
      6. The Moinkee programme. The MOI Programs sheet (early 2026) lists
         it under Sai Kiran; who owns it now, and whether this site
         belongs to it (owner: confirm)

   3. Env vars:

      1. Where they live:
         1. Production: Vercel → the project → Settings → Environment
            Variables
         2. Local: .env.local in the repo folder, kept out of git by the
            .env* rule. There is no .env.example; docs/VERCEL.md lists them
         3. Anything starting NEXT_PUBLIC_ is baked into the build, so
            changing it needs a redeploy
      2. Needed to run:
         1. PINATA_JWT — Pinata → API Keys
         2. ADMIN_MNEMONIC — the minting wallet's seed phrase, all 12 words
            on one line, no quotes. A devnet wallet only, funded at the
            Voyage faucet
         3. NEXT_PUBLIC_ASSET_ID — printed by scripts/create-collection.mjs
            when it creates the collection (it reads ADMIN_MNEMONIC). New
            after every reset
         4. NEXT_PUBLIC_FOLDER_CID — optional, the IPFS folder for gallery
            images. The code has a default
      3. Helper script only: MNEMONIC, read by the token-listing script in
         scripts/

   4. Handover: on main, docs/VERCEL.md (hosting and env) and
      docs/getTDU-token-ids-issue.md (a known SDK limit: no way to list
      which token ids an address owns). On the branch only,
      docs/pinata-recovery.md (how to re-mint after a reset from what
      Pinata kept). The README is the unedited Next.js template. No Claude
      skill covers it; moi-devnet-reset lists it in one row of what a reset
      breaks

   5. Process: main is from February 2026. The branch is from April 2026,
      committed by a Claude session on my account, and it is not merged. A
      push to main builds a Production deploy on Vercel and a push to any
      other branch builds a Preview (GitHub shows the last Production
      deploy on 2026-02-26 for the current main, and 8 Previews of the
      branch). No CI, nothing by hand. After a devnet reset I create the
      collection again with scripts/create-collection.mjs, put the new id in
      NEXT_PUBLIC_ASSET_ID on Vercel and redeploy. To bring the old
      mementos back I run the branch on my Mac with PINATA_JWT,
      ADMIN_MNEMONIC and the new asset id in .env.local and follow
      docs/pinata-recovery.md: it recovers what Pinata kept and mints each
      memento again to its owner. That code is not on main, so the live
      site cannot do it. The minting wallet has to be funded again first.
      The three recovery files on my Mac date from 2026-04-13; whether the
      re-mint was ever run: confirm

   6. ToDo:
      1. The live site is unsafe to leave up. It has no access check on the
         actions that spend the minting wallet and the Pinata account, and
         its connect box has visitors paste a wallet seed phrase and sends
         it to the server. No fix is written. Take the site down unless it
         is wanted
      2. A wallet seed phrase is committed in a helper script in the public
         repo. Whether it is the minting wallet
         is not known (confirm). Treat it as public and never fund that
         wallet
      3. The recovery code on the branch has no admin check, and 8 Preview
         builds of the branch exist (last 2026-04-13); whether they sit
         behind Vercel's deployment protection is not known (confirm). Add
         the check before the branch is merged or deployed
      4. Minting probably fails: the last Production build was 2026-02-26
         and the asset id is baked in at build, so it predates the devnet
         wipes of 2026-08-15 and 2026-09-11 (inferred, confirm)
      5. Put the minting wallet seed, the Pinata token and the three recovery
         files (pinata_pins.json, recovered.json, snapshot.json) in a shared
         vault. Pinata keeps the metadata while the account stays reachable
      6. Confirm who owns the Vercel project and the Pinata account
      7. Decide if it is alive (Rahul, Sai Kiran). If not, take down the
         Vercel project, revoke the Pinata token and archive the repo. If
         so, merge the branch (main is 8 commits and 46 days behind), move
         the repo to the org and upgrade the SDK


9. Points Program:

   1. Stack:
      1. Next.js 16 + React 19 + TypeScript + Tailwind 4 — web app and API
      2. Supabase — Postgres for all state, through Drizzle, 11 migrations
      3. Better Auth — Google sign-in, the only login
      4. X, Discord, Telegram — linked by members, checked by the app
      5. Reown + js-moi-signer — wallet linking, keys read from the devnet RPC
      6. Resend — sign-in emails
      7. Docker + GitHub Actions + GHCR + Teleport — build and deploy to the
         DevOps box, one container behind nginx
      8. Health route and a nightly job route — health check; re-audit,
         purge and point totals (nothing is known to call the job)

   2. Variables:
      1. Codebase (sarvalabs/moi-project, private; admins gokul, chandra, git,
         adithya, upendhar on 2026-10-04). feature/ci-cd deploys, not main
      2. Supabase project (on the Points email account, free plan, no
         backups as of 2026-10-04)
      3. Google OAuth client, X developer app (paid API), Discord app and bot,
         Telegram bot and group, Reown project, Resend account, old Vercel
         project (owner: confirm for each)
      4. The box, nginx, TLS, Teleport, DNS, GHCR image (DevOps: Upendhar)
      5. MOI devnet RPC, written into the code, wiped by a reset (Protocol team)
      6. App code, first version (Harsh Gupta); CI/CD (Upendhar); who sits in
         ADMIN_EMAILS and admin_users (owner: confirm)
      7. Tasks on, 2026-10-04: join_x_verified 50, join_discord 50,
         join_telegram 50, create_wallet 100; the rest off (owner: confirm)

   3. Env vars:

      1. Where they live:
         1. Production: GitHub → sarvalabs/moi-project → Settings → Secrets
            and variables → Actions (13 secrets, 20 variables, 2026-10-04).
            Secrets there cannot be read back
         2. Production, the box: /opt/moi-project/.env holds the variables
            only, rewritten at every deploy. Secrets go straight into the
            container, so the only readable copy is there (DevOps)
         3. Local: .env.local in the repo, copied from .env.example
         4. A changed value needs a workflow run. The image build gets only
            the five names under Needed to boot

      2. Needed to boot:
         1. DATABASE_URL — Supabase dashboard → the project → Connect
         2. BETTER_AUTH_SECRET — generate with: openssl rand -hex 32.
            Replacing it signs everyone out and makes every stored X
            connection unreadable until members reconnect X
         3. BETTER_AUTH_URL — https://points.moi.technology, https required
         4. GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET — Google Cloud console →
            APIs & Services → Credentials; redirect must match BETTER_AUTH_URL

      3. Tasks and email (an enabled task missing a name stops the container):
         1. X_CLIENT_ID, X_CLIENT_SECRET, X_TARGET_URL — developer.x.com →
            the app; X_TARGET_URL is the profile members must follow
         2. DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET, DISCORD_BOT_TOKEN,
            DISCORD_GUILD_ID, DISCORD_INVITE_URL — Discord developer portal
         3. TELEGRAM_BOT_TOKEN, TELEGRAM_BOT_USERNAME, TELEGRAM_CHAT_ID —
            BotFather and the group; TELEGRAM_INVITE_MODE — join_request or
            direct; TELEGRAM_WEBHOOK_SECRET — generate with: openssl rand
            -hex 32 (set the webhook again after a change)
         4. MOI_NETWORK — devnet, the only value the code accepts;
            REOWN_PROJECT_ID — Reown dashboard → the project
         5. RESEND_API_KEY — resend.com → API keys; EMAIL_FROM — the sender
            (MOI Points <no-reply@moi.technology>). Both, or no email is sent

      4. The rest:
         1. CRON_SECRET — generate with: openssl rand -hex 32. ADMIN_EMAILS —
            emails that get the admin pages once Google has verified them.
            VERIFICATION_WINDOW_MINUTES, VERIFICATION_LIMIT_PER_USER,
            VERIFICATION_LIMIT_PER_IP, SOCIAL_AUDIT_BATCH_SIZE — plain numbers
         2. In the template, read by code, not passed by the deploy, so unset:
            MOI_RPC_URL (dev challenges), X_TOKEN_ENCRYPTION_KEY,
            X_TOKEN_ENCRYPTION_KEY_PREVIOUS, CLIENT_IP_HEADER (unset, the
            per-IP limit does nothing), DATABASE_SSL, PG_POOL_MAX,
            NEXT_PUBLIC_SITE_URL, FAUCET_URL, FAUCET_API_KEY,
            FAUCET_TOKEN_ADDRESS, FAUCET_VERIFY_MODE
         3. Read by code, not in the template: DATABASE_CA_CERT, MIGRATIONS_DIR,
            GIT_SHA, ALLOW_INSECURE_AUTH_URL, SKIP_STARTUP_CHECKS (leave unset)
         4. Deploy access (DevOps): GHCR_PAT, TELEPORT_PROXY,
            TELEPORT_JOIN_TOKEN, VM_HOST, VM_USER

      5. Full list with comments: .env.example in the repo

   4. Handover: no operator guide on the deploy branch. Read
      drizzle/TRIGGERS.md (database rules), README.md (local setup; its
      nightly-audit text is what PR #21 removes), .impeccable.md (design).
      CICD.md, on PR #15's branch only, describes a setup that is not live.
      Claude skill: moi-web-products-ops

   5. Process: I branch from feature/ci-cd, not main, run pnpm run ci myself
      (no check runs on a PR) and open one PR against it. Merging is the
      deploy: the workflow builds the image, pushes it to GHCR, logs in to
      the box through Teleport, rewrites the .env, removes the old container
      and starts the new one. About 4 minutes, no staging, no rollback. The
      health route shows no build (sha is null), so I check applied equals
      expected, then sign in. By hand: migrations (hand-written, never
      db:generate; DevOps applies them on the box before the merge that needs
      them, or the new build will not start), new variables (a PR on
      deploy.yml plus a value in GitHub), provider callbacks, the Telegram
      webhook, the flag that switches a task on (a code change). An X like
      campaign needs no code, a session bounty does. After a devnet reset
      (inferred): members need a fresh account before they can link a wallet,
      linked wallets stay bound (only an admin erase clears one), a moved RPC
      address is a PR (config/moi-networks.ts).

   6. ToDo:
      1. Test a wallet link. The devnet RPC certificate expired on 2026-10-04
         and was renewed by 2026-10-05; the server reads wallet keys from
         that host, so linking may have failed in between (not tried).
      2. Put the Supabase project (on the Points email account) on a paid
         plan with backups; it holds every user and every point.
         Then drop the schema backup.tasks_before_0008 (6 rows, still there).
      3. Move every secret into a shared vault; GitHub cannot show them back.
         A secret was exposed in an old build record in September, accepted
         on 2026-09-15; the 17 records have not expired (2026-10-04). Delete
         them, rotate before a real launch or if access widens.
      4. The deploy logs in to the box as root and publishes the container
         port beyond nginx; it answered over http from outside on 2026-10-04
         (firewall: confirm). PR #15 fixes both after DevOps setup and adds a
         rollback, but conflicts with Upendhar's 92f9c48: rebuild or close
         it, then deploy from main.
      5. Decide #21 (emails, avatars, wallet keys, X likes, no nightly audit;
         clean to merge, no migration) and #1 (Upendhar's first CI/CD, base
         feat/dev-challenges: retarget or close). Planned, not done: close
         Points-Program #1 and sarvalabs-adithya/moi-project #1.
      6. Nothing is known to run the nightly job (the old schedule sat in
         vercel.json on stale main). #21 replaces it with a purge-and-totals
         job: ask Upendhar what calls it and who schedules the new one.
      7. Session 8 bounty is deployed but off: needs MOI_RPC_URL in
         deploy.yml, one real submission, then the flag. Open it or drop it.
         Then make bounties extensible: a webinar host should be able to
         create one from the admin side without a code change or a deploy.
      8. Pass X_TOKEN_ENCRYPTION_KEY (read x-credentials.ts first),
         CLIENT_IP_HEADER (nginx must set it) and GIT_SHA from the deploy,
         match the Dockerfile's pnpm (11.11.0) to package.json (10.34.5),
         retire the old Vercel project, write an operator guide.


10. Agent Explorer:

   1. Stack:
      1. React 19 + Vite + React Router 7 + TanStack Query — the web client
      2. Express 4 + TypeScript + MySQL — the API and an indexer that copies
         the on-chain agent registry into MySQL
      3. js-moi-sdk + js-moi-agent-registry — registry reads and writes (main
         pins the SDK at ^0.8.0, PR #5 moves it to 0.9.0-rc2)
      4. WalletConnect — wallet sign-in, registering an agent, admin sign-off
      5. Pinata — IPFS pins for agent cards, but no key is passed in production
      6. Docker + GitHub Actions + GHCR + SSH — a merge to main builds two
         images and runs them on one VM behind nginx 1.24 (the nginx config is not on record), at
         agents.moi.technology and api.agents.moi.technology

   2. Variables:
      1. Codebase (sarvalabs/agent-explorer, private, main deploys; I push
         branches to the org repo, no fork)
      2. App code, admin and verification rules (Gokul, per my 1 October
         list; GitHub records no owner: no CODEOWNERS, main unprotected,
         2026-10-04)
      3. Workflow, VM, nginx, SSH key, GHCR token, DNS (DevOps; Upendhar
         wrote 24 commits, all CI/CD)
      4. MySQL database, host not on record (DevOps)
      5. The agent registry on devnet, new id after every reset (Protocol
         team, Gokul publishes it). The Explorer reads it, and its Register
         Agent page writes to it
      6. Mine: 8 of 60 commits on main, PR #5, and one of five repo admins
         (Gokul, Upendhar, chandra, git, me). Whether DevRel owns the
         Explorer is not settled (owner: confirm, Rahul)
      7. The server's devnet wallet and agent identity, the WalletConnect
         project in Reown, the Pinata account, whose login holds GH_TOKEN
         (owner: confirm)
      8. The Launchpad, whose agents the verified rule looks for (Adithya)

   3. Env vars:

      1. Where they live:
         1. Production: GitHub → sarvalabs/agent-explorer → Settings →
            Environments → PROD (5 secrets, 14 variables), plus one repo-
            level secret, GH_TOKEN. Secrets cannot be read back; the
            readable copy is the running containers, through Upendhar.
            Names and dates: gh secret list -e PROD, gh variable list -e
            PROD --json name,updatedAt (the bare form prints values)
         2. Local: server/.env copied from server/.env.example; the client
            has no template, use client/.env.local
         3. The backend gets only the names the workflow's docker run lists,
            the rest run on code defaults. VITE_ names are baked into the
            frontend image at build: changing one needs a deploy, not a
            restart, and a new one also needs an ARG in client/Dockerfile
         4. DEV and TEST environments exist but are empty (2026-10-04)

      2. Needed to boot:
         1. DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASSWORD — ask DevOps.
            Local: your own MySQL
         2. PORT — the workflow sets 5005, local default 4000
      3. Chain and admin:
         1. MOI_RPC_URL — public, https://dev.voyage-rpc.moi.technology/devnet
         2. MOI_AGENT_REGISTRY_LOGIC_ID — not passed by the workflow, so the
            default in server/src/config.ts runs. New id after a reset: ask
            Gokul
         3. MOI_MNEMONIC — the server's devnet wallet, a secret. Ask Gokul
         4. MOI_AGENT_ID, MOI_INTELLIGENCE_LOGIC_ID — chain ids kept as
            secrets, wiped by a reset. Ask Gokul. These two and MOI_MNEMONIC
            were last set 2026-06-17, before the 2026-09-11 wipe
         5. ADMIN_ADDRESSES — wallets allowed to verify agents. Not passed,
            so no admin exists unless the container was started by hand
         6. PINATA_JWT — no default, not passed, so uploads answer "not
            configured". From the Pinata account (owner: confirm)
         7. LAUNCHPAD_ORIGIN (PR #5: LAUNCHPAD_HOSTS), MOI_WS_URL,
            MOI_DERIVATION_PATH — code defaults, none passed. PR #5 adds
            MOI_READ_CALLER_ADDRESS, SYNC_INTERVAL_HOURS and the client
            build override VITE_MOI_AGENT_REGISTRY_LOGIC_ID, same way
      4. Client build, variables in PROD:
         1. VITE_API_BASE_URL, VITE_WC_PROJECT_ID, VITE_TESSERACT_BASE_URL,
            VITE_MOI_NETWORK, VITE_MOI_CHAIN_ID, VITE_TRANSACTION_FUEL_LIMIT
            — ask Gokul; the project id comes from the Reown dashboard
         2. VITE_INTELLIGENCE_LOGIC_ID — filled from MOI_INTELLIGENCE_LOGIC_ID
      5. Listed, but read by nothing or never passed:
         1. VITE_AGENT_REGISTRY_LOGIC_ID — passed, no client code reads it
         2. VITE_PARTICIPANT_BASE_URL, VITE_PUBLIC_URL — read, never passed
         3. LAUNCHPAD_ORIGINS, LAUNCHPAD_CONFIRM_ORIGIN — closed PR #4 only
      6. Build and deploy: GH_TOKEN (GHCR login). Deploy only:
         SSH_PRIVATE_KEY, VM_HOST, VM_USER — ask Upendhar

      7. Full list with comments: server/.env.example in the repo

   4. Handover: nothing in the repo (client/README.md is the unmodified Vite
      template). Claude skill moi-launchpad-ops, explorer branch, covers
      health, shipping a change, settings, index sync, verifying agents and
      rollback (facts dated 2026-10-03); moi-devnet-reset for what to redo
      after a reset. PR #5's description is the best written account of the
      registry problems

   5. Process: I work on a branch in the org repo, run tsc and the Vite
      build, and open a PR to main. Nothing runs on a PR: no tests, no
      lint, no required review. A merge is a production deploy, and a manual
      run can deploy any branch to PROD, which has no rule. The workflow
      builds two images, pushes them to ghcr.io/sarvalabs and replaces both
      containers over SSH (their names end in -test), old ones first, with
      no rollback. The API reports no version, so I prove a client change by
      searching the live script for a new string. Last deploy: run #17,
      2026-09-24, after Gokul merged my PR #3. By hand: git restore
      server/dist after a local build (it is tracked); Upendhar runs npm run
      sync on the VM (confirm). After a devnet reset I get the new registry
      id from Gokul, change it in server/src/config.ts (on main that alone
      does not take, see ToDo 3), check that the MOI_MNEMONIC wallet,
      MOI_AGENT_ID, MOI_INTELLIGENCE_LOGIC_ID and the node address are still
      valid, deploy and run a sync. Old rows stay. After the 2026-09-11 wipe
      the new id reached production 13 days later

   6. ToDo:
      1. Security, as of 2026-10-04: some server routes need no sign-in, and
         a test script in server/ has a recovery phrase written in it, on
         every branch. Server and client env files were also committed on
         2026-04-02 and deleted soon after; they stay in git history (not
         opened). No fix exists on any branch. Needs Gokul; treat that
         wallet and anything in those files as exposed
      2. Decide PR #5 (open since 2026-10-02, no reviewer). It fixes registry
         reads, adds a 4-hourly sync and a new verified rule. It was never
         run against a real MySQL, and its first boot changes the production
         database. Tell Gokul and Upendhar first, ask for a backup (none is
         on record), and remove the AI co-author line and footer (rewrites a
         pushed branch)
      3. Until then the live site is the 2026-09-24 build: 49 agents indexed
         on 2026-10-04 against 157 on chain on 2026-10-02 (PR #5's count),
         1 verified, 23 on the retired Vercel host. From the code, not run:
         main sets the new registry id after the registry package has read
         its built-in one, and Register an Agent needs the Pinata upload,
         which has no key in production
      4. Ask Upendhar how the live client was built: its script is not the
         file the last deploy run produced, and it carries a value the
         workflow never passes (checked 2026-10-04)
      5. Post or drop the design issue I promised when I closed PR #4 on
         2026-09-24 (no issue exists). The draft is written, not posted,
         and predates PR #5, so parts are overtaken
      6. Pass the missing settings through the workflow: ADMIN_ADDRESSES
         first (nobody can verify an agent without it), PINATA_JWT, then the
         PR #5 ones. Drop the unused VITE_AGENT_REGISTRY_LOGIC_ID, and fill
         or remove the empty DEV and TEST environments
      7. Prune the index: nothing deletes rows, so probe, test and old-chain
         rows stay. A database write by Upendhar after a backup, Gokul's yes
      8. Move every secret into a shared vault; settle owners for the server
         wallet, the Reown project, the Pinata account and GH_TOKEN
      9. Write a handover doc in the repo, add a PR check and write down a
         rollback
