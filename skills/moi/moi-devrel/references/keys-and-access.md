# Keys and access, by name: the index

Names only. This file never holds a value, a length or a prefix. It is the index of accounts and keys shared across products. The variable names of each product are in `keys-by-product.md`. Facts are as of 2026-10-02 from `project-handover-docs/LIST-OF-DEPENDENCIES.md` (the 4 October snapshot) and the ops research notes, updated from `project-handover-docs/ENV-VARS.md` and `MIGRATION-LIST.md` (13 October 2026), with changes dated where a row says so. Status is TBD for every row: the owner settles access at the end. "ASK" has the one meaning defined in `../SKILL.md`: the evidence does not settle it, so put the question to that person through the operator. Back to `../SKILL.md`.

## Rules
- Never open an `.env` file. Never ask for a value in chat or accept one. If the operator pastes a key or recovery phrase, say so, tell them to revoke or rotate it, and do not repeat it. This has happened with a Buffer token, Telegram bot tokens and devnet recovery phrases.
- GitHub secrets cannot be read back and no shared vault exists. The only readable copy of the Launchpad's production secrets is on its VM (ASK: Upendhar). Points passes its secrets to the container at start and keeps only non-secret variables on the VM. The Voyage MCP deploy passes values inline and has no `.env`. Put each value in an org vault before you change it. ASK: Rahul which vault.
- Secrets reach a VM only at deploy. After changing one, re-run the deploy workflow on the right branch. A name the workflow does not list never reaches the app.
- Rotation. Launchpad: free for `SESSION_SECRET` and `CRON_SECRET` (users are logged out); `TELEGRAM_WEBHOOK_SECRET` needs a re-run of `setWebhook` or delivery stops silently; `AGENT_KEY_ENCRYPTION_SECRET` is never rotated, because every stored agent key becomes unreadable. Dataroom: a secret rotation there is an admin step; follow `moi-web-products-ops` after the handover note named in `repo-map.md` has been read. MCP: a new `MOI_SESSION_KEY` signs everyone out of every dapp.
- Claude never handles a recovery phrase, including a throwaway one (`consent-and-identity.md` section 5). Wallet and mnemonic steps are steps the operator performs: the operator types a phrase at a hidden prompt or on the command line. Treat any phrase ever pasted in chat as exposed.

## Code access
| Name | Unlocks | Used by | Lives in | Who grants | Status |
|---|---|---|---|---|---|
| Work GitHub identity and `gh` login | Push, PRs, review | Every repo | `gh auth` on the operator's machine | Org admin of `sarvalabs` and `moi-foundation` | TBD |
| Private repo access: moidocs, voyage-docs, coco-docs, voyage, voyage-api, moi-agent-launchpad, agent-explorer, moi-project, go-moi, cocolang | Read and PR | Docs, ops, claim checks | GitHub | Org admin per repo. `moi-project` returned 404 until access was given on 2026-09-15 | TBD |
| Repo admin | Edit Actions secrets and variables | Every deploying repo | GitHub settings | Org admin. On `moi-project` the admins were gokul, chandra, git, adithya, upendhar (2026-09-15) | TBD |
| GPG signing key | Signed commits on upstream PRs (x402, CASA) | Standards work | Operator's machine | Recorded as "not configured". ASK: Rahul | TBD |
| `UPSTREAM_READ_TOKEN` | Read-only access to go-moi and cocolang for the upstream watch (fine-grained token) | `sarvalabs/moi-mcp` | Actions secret | Not set as of 13 October 2026. Rahul decides which account creates it (`project-handover-docs/MCP-SERVER.md`) | TBD |
| `NPM_TOKEN` | npm publish workflow, unused so far | `sarvalabs/moi-mcp` | Actions secret | Nobody holds an npm account for it yet; Rahul decides the name and the account (`ENV-VARS.md`) | TBD |
| npm package name `@moi-protocol/mcp-server` | Publishing the MCP server | `moi-mcp` | Not claimed | Rahul decides the name | TBD |
| The `npm` environment of `x402-foundation/x402` | Publishing `@x402/moi` after a merge | Standards work | The upstream repo's settings | Owner unknown. ASK: Rahul | TBD |

## Deploy access (DevOps holds all of it)
| Name | Unlocks | Used by | Lives in | Who grants | Status |
|---|---|---|---|---|---|
| `TELEPORT_PROXY`, `TELEPORT_JOIN_TOKEN`; website also `TELEPORT_NODE`, `VM_USERNAME`; voyage-api also `TELEPORT_PROD_PROXY`, `TELEPORT_PROD_JOIN_TOKEN`, `MCP_DEV_MACHINE`, `MCP_PROD_MACHINE` | Workflows reach a VM | Website, Launchpad, Points, voyage, voyage-api | Actions secrets and variables | Upendhar | TBD |
| `GHCR_PAT`; Explorer uses `GH_TOKEN` | Push and pull images in `ghcr.io/sarvalabs` | Launchpad, Points, Explorer | Actions secrets | Upendhar. Owner of `GH_TOKEN`: not recorded (`MIGRATION-LIST.md`); it is expired or revoked as of 2026-10-14 (the Explorer deploy fails at "Login to GHCR"), and Upendhar has been asked to replace it and re-run; ASK: Upendhar, then Rahul | TBD |
| `VM_HOST`, `VM_USER`; Dataroom `VM_HOST`, `VM_USERNAME`, `VM_SSH_KEY`; Explorer `SSH_PRIVATE_KEY` | SSH deploy | Launchpad, Points, Dataroom, Explorer | Actions secrets and variables | Upendhar | TBD |
| `PREVIEW_VM_HOST`, `PREVIEW_VM_USER` | PR previews on `*.preview.moi.technology` | `MOI-Website` | Actions variables | Upendhar | TBD |
| VMs, nginx, TLS, DNS for `*.moi.technology`, the two VM deploy scripts | Everything on a host | All sites | The VMs, not in git | Upendhar | TBD |
| Who may edit the production environment of `sarvalabs/voyage-api` (the MCP copy) | The MCP production settings | `moi-mcp` | GitHub settings of `voyage-api` | Not settled. ASK: Srikar, then Rahul | TBD |

## Accounts with no repo secret
| Name | Unlocks | Used by | Lives in | Who grants | Status |
|---|---|---|---|---|---|
| Buffer organisation (X channel "MOI_Tech", LinkedIn page "moi-tech") | Social drafts and scheduling. Only the owner can create an API token | Blog, release and webinar posts | buffer.com | Chandra owns the organisation (stated by the previous operator, 2026-10-06) | TBD |
| Mailchimp | RSS campaign on the 15th of every month (about 5,500 subscribers, paid plan). Vardan has access (stated by the previous operator, 2026-10-06). The sender must be a real MOI address. The Mailchimp template parts are in `moi-blog/templates/mailchimp/` | Newsletter | mailchimp.com | Vardan holds the login (`project-handover-docs/ENV-VARS.md`) | TBD |
| Luma | Builders event pages, made by hand. No automation. The community call page and the website's Luma block link (PR #60) | Webinars, calls | luma.com | Vardan holds the shared Luma, Riverside and YouTube logins (`COMMUNITY-CALL.md`); Builders pages are DevRel's (`DEV-WEBINARS.md`) | TBD |
| Google Workspace shared accounts `info@moi.technology` (Builders and call Meets, recordings, Gemini notes) and `marketing@moinetwork.io` (standups); Drive forms and sheets, including the Programs sheet, the programme forms and the content-bounty sheet | Meet hosting, recordings, calendars, programme sheets | Calls, webinars, education programmes | Google | ASK: Rahul which Google account owns the forms and sheets | TBD |
| YouTube channel | Call recordings and AMA clips | Calls | youtube.com | Vardan holds the login (`COMMUNITY-CALL.md`); confirm the account (`MIGRATION-LIST.md`) | TBD |
| Google Analytics 4 and Tag Manager | Measurement, UTM by post slug | Website, blog | Google, under the sarvalabsdeveloper@gmail.com account (stated by the previous operator, 2026-10-06) | The holder of that account | TBD |
| Google Search Console and Bing Webmaster Tools | Indexing, sitemaps. Bing imported from Search Console on 2026-09-09 | Website, blog, docs | Google, Microsoft | Search Console: the sarvalabsdeveloper@gmail.com account (`MIGRATION-LIST.md`). Bing: ASK: Rahul | TBD |
| Cloudflare: Pages projects `moichain-docs`, `cocodocs`, `voyage-docs`, `moi-website`; R2 behind `cdn.moi.technology`; zone settings | Docs builds and previews, skill zips, AI-crawler blocking | Docs, SDK | Cloudflare | Company-owned account (`ENV-VARS.md`); who administers it: ASK: Rahul | TBD |
| Otter.ai, Slack, Discord server, Zoom, Teams | Transcripts, inputs, community, call links, one file hand-off | Everyone | Each | Zoom owner not recorded. ASK: Rahul | TBD |
| Discord server admin and mentor roles, the Telegram announcement channel, the WhatsApp group admin for Forge | Programme community channels | Education programmes | Each | ASK: Rahul, Sai Kiran | TBD |
| Telegram bots: `moinetworkbot` (Launchpad), the blog channel bot, the Points bot | Messaging | Launchpad, blog, Points | BotFather | `moinetworkbot`: Adithya's Telegram account until the transfer in `MIGRATION-LIST.md` is done (to Rahul Lenkala; Telegram refused it on 14 October, retry pending). The Points bot and the blog channel bot: the sarvalabsdeveloper@gmail.com account | TBD |
| Supabase projects: Launchpad, Points, Dataroom, website chatbot and old calendar | Databases | Each product | supabase.com | Launchpad and Dataroom: the company Supabase organisation (moved 8 October 2026). Points: the Points email account, free plan, no backups. The website chatbot's project is not recorded (`MOI-WEBSITE.md`) | TBD |
| Vercel project of the Sprint guide site (`moisprint`) and the wallet that deployed its on-chain logic | Nothing now: MOI Sprint was scratched 13 October 2026 | MOI Sprint (scratched 13 October 2026) | vercel.com, devnet | Scratched 13 October 2026; nothing to do | TBD | <!-- slop-lint: ignore -->
| Reown (WalletConnect) projects at cloud.reown.com | Wallet pairing for Launchpad, MCP, Explorer, Points | Those products | Reown | Launchpad, MCP and Points projects: the sarvalabsdeveloper@gmail.com account (`ENV-VARS.md`). The Explorer's: not recorded (`MIGRATION-LIST.md`); ASK: Gokul | TBD |
| Anthropic, OpenAI, Groq and Google AI consoles | Model and embedding keys | Website, Dataroom, Launchpad | Each console | No company-owned Anthropic, OpenAI or Groq account exists as of 13 October 2026, and the keys now set are not company keys; the chat features stay off until company keys exist (`ENV-VARS.md`). A Google AI key is not recorded; ASK: Rahul | TBD |
| Resend (domain `moi.technology` verified with DKIM and SPF), Google OAuth client, X developer app | Points emails and sign-in | Points | Each | The sarvalabsdeveloper@gmail.com account, the shared company developer account (`ENV-VARS.md`, 13 October 2026) | TBD |
| Medium, Zenodo, Canva, Scribble | Cross-posts, paper records, older call decks, AI-visibility report | Blog, papers, calls | Each | ASK: Rahul. The Scribble login is not recorded | TBD |
| Figma account that holds the MOI brand file | The brand book source | `moi-devrel/design` | figma.com | Not recorded (the previous DevRel's notes); ASK: Rahul. The brand book PDF and logo pack are in the handover repo, `others/legacy-skills/moi-design/uploads/` | TBD |
| Wikidata, Crunchbase, LinkedIn organisation pages | Entity consistency for search | GEO | Each | Sai Kiran prepares Wikidata. ASK: Rahul for the rest | TBD |
| MOI Wallet (extension and mobile), Voyage faucet | Test wallets and funds. The faucet funds existing accounts only, and needs a faucet token from the Voyage dashboard (`devnet.md`) | Demos, tests | Browser, phone | No key. Each person makes their own | TBD |

## Where each product's names are
`keys-by-product.md` has one section per product: website and blog, MOI-Webinars scripts, Dataroom, Points Program, Agent Launchpad, Agent Explorer, MCP server, docs sites, the Forge demo, and the x402 standards work (MOI Sprint was scratched 13 October 2026).

## Not yet known
- The owner and login of the vendor accounts that `project-handover-docs/ENV-VARS.md` and `MIGRATION-LIST.md` do not settle: the Explorer's accounts, the website's Supabase project, the Google Workspace forms and sheets, Zoom. ASK: Rahul.
- Which vault the org will use, and who creates the first entries. ASK: Rahul.
- Who holds the three Launchpad registration mnemonics outside GitHub. ASK: Upendhar, then Rahul.
- Which account will hold `UPSTREAM_READ_TOKEN` and renew it: not set yet (`MCP-SERVER.md`); Rahul decides.
