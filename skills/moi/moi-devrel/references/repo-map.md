# Repo map: every repo a DevRel person touches

Facts are as of 2026-10-02 unless dated. Sources: `DEPENDENCIES.md` (the previous operator's handover file, local to his machine and not in git as of 2026-10-02; ASK: Adithya for a copy; checked 2026-10-01), the ops research notes (live probes 2026-10-02), the repos' workflow files, and reads of 2026-10-03 where a row says so. Where they disagree the newer reading wins. A product's row also carries any handover warning: read it before you touch the product. Back to `../SKILL.md`.

## How things deploy
- GitHub orgs: `sarvalabs` (every repo that deploys), `moi-foundation` (MOI-Webinars, awesome-moi, moi-sprint), `moinetwork` (old copy of the points app, nothing deploys). The previous operator's work account `sarvalabs-adithya` holds forks used to open PRs and some demos.
- MOI sites and products deploy through GitHub Actions to VMs that DevOps owns (Teleport or SSH). Docs sites publish through Cloudflare Pages. As of 2026-10-02 none of them runs on Vercel: the Launchpad left on 2026-08-03, Points by 2026-10-01, and the Dataroom's old Vercel project is gone. `vercel.json`, an `api/` folder, `AGENTS.md` boilerplate and README deploy text in some repos are leftovers. Do not write Vercel into any MOI deploy document. Three demo apps and an old copy of the website still sit on Vercel (see Demos). <!-- slop-lint: ignore -->
- The website and Dataroom deploy scripts live on the VM and are not in git. For anything on a VM, including those scripts: ASK: Upendhar.
- Private repos need access from an org admin. Public docs and PRs cite only public artefacts.

## Docs sites (Cloudflare Pages)
| Repo | What | Live URL | How it publishes | Ask |
|---|---|---|---|---|
| `sarvalabs/moidocs` (private) | Protocol docs, Docusaurus 2.1, sections learn, build, guard, 36 pages | docs.moi.technology | Merge to `main` publishes (Pages project `moichain-docs`). Every branch gets a preview URL. `npm run build` also generates `llms.txt` and page schema. No secrets | Rahul (scope), Gokul (review) |
| `sarvalabs/voyage-docs` (private) | Voyage docs: JSON-RPC, faucet, wallet sign-in, Docusaurus 2.1, 6 pages | voyage-docs.moi.technology | Same, Pages project `voyage-docs`. Its two scripts must stay identical to moidocs | Gokul (content) |
| `sarvalabs/coco-docs` (private) | Coco language docs, Docusaurus 3.9, 36 pages | cocolang.dev | Same, Pages project `cocodocs`. Downloads and the skill zip sit on `cdn.moi.technology/cocolang/` (Cloudflare R2). The Book is at `/docs/book/` on `main` (live read 2026-10-03: 200; `/book/` gave 404) and moves to `/book/` after PR #12. 27 of its 36 pages have no description on `main` (clone fetched 2026-09-28) | Robert Špendl |
| `sarvalabs/js-moi-sdk`, folder `docs/` | SDK API docs, Sphinx, 10 pages | js-moi-sdk.docs.moi.technology | On Cloudflare per the text of PR #150. Project name, pipeline and previews unknown. Generated files are committed in `docs/source/_extra/`; run `make llms` in `docs/` | SDK team |
| unknown | MOI Wallet docs | docs.wallet.moi.technology | Repo, owner and status unknown | ASK: Rahul |
Rules for all four: `DOCS-STYLE-GUIDE.md` at the root of moidocs (it is only in open PR #124 as of 2026-10-02) and the Drive doc "MOI Documentation Standard" (two versions; v2 is canonical, inferred; ASK: Rahul). The style guide is not published on the site.

## Website, blog and web products
| Repo | What | Live URL | How it deploys | Ask |
|---|---|---|---|---|
| `sarvalabs/MOI-Website` (public) | Marketing site (React 19, Vite 7), Express chatbot and calendar server in `server/`, Astro blog in `blog/` | moi.technology, blog.moi.technology | Merge to `main` runs "Deploy MOI Website": Teleport, then the VM script. PR previews at `pr-<N>.preview.moi.technology` and `pr-<N>-blog.preview.moi.technology`, deleted after 7 days. One markdown file feeds both builds, so both must run | Upendhar (VM), Rahul (content). A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin. |
| `sarvalabs/moi-dataroom0` (public) | Investor Dataroom, Next.js 16, Supabase, chat over uploaded documents | dataroom.moi.technology | Merge to `main` runs "Deploy MOI Dataroom": SSH to the VM, then the VM script. No health check afterwards | Srikar, Upendhar. A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin. |
| `sarvalabs/moi-project` (private) | Points Program, Next.js 16.2, pnpm, Supabase Postgres by Drizzle | points.moi.technology (preview.points.moi.technology, same box) | Deploys from branch `feature/ci-cd` (`main` has been stale since 2026-08-03). Image to GHCR, Teleport, then a container run on the VM behind nginx (details on the VM: ASK: Upendhar). The old container is removed before the new one starts | Upendhar (CI/CD, box), Harsh Gupta (app), Adithya (audit, database login). A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin. |
Old: `sarvalabs/Points-Program` (PR #1 open, still used? unknown), `moinetwork/moi-project` (nothing deploys). The blog is a separate Astro app under `blog/`, with a listing page generated into `moi.technology/blog`.

## Chain products
| Repo | What | Live URL | How it deploys | Ask |
|---|---|---|---|---|
| `sarvalabs/moi-agent-launchpad` (private) | No-code agents with on-chain registration, Telegram and a marketplace; Next.js 14, Supabase | launchpad.moi.technology | Merge to `master` (the branch `feature/moi-agent-launchpad-cicd` also triggers it) runs "MOI Agent Launchpad CI/CD": image to `ghcr.io/sarvalabs/moi-agent-launchpad`, Teleport, then `docker compose up` on the VM (ASK: Upendhar). About 4 minutes. CI runs no tests and a red run leaves the old image serving with no alert | Adithya (301 of 338 commits), Upendhar (VM, DNS), Gokul (registry id) |
| `sarvalabs/agent-explorer` (private) | Public directory of on-chain agents; React and Vite client, Express and MySQL server | agents.moi.technology, API api.agents.moi.technology | Merge to `main` runs "Build Push and Deploy Agent Explorer": two GHCR images, SSH to the VM, containers that carry a test name even in production (ASK: Upendhar). No rollback | Gokul (app, registry), Upendhar (CI/CD). A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin. |
| `sarvalabs/moi-mcp` (public, `master`) | MCP server: a chat assistant reads MOI and proposes writes that a phone wallet signs | mcp.voyage.moi.technology (write, OAuth), mcp-read.voyage.moi.technology (read). `mcp.moi.technology` does not exist | Merging here deploys nothing. Production is a copy in `sarvalabs/voyage-api` (private), branch `feat/moi-mcp`, folder `moi-mcp/`. Open a "sync subtree" PR, then run the manual workflow "Deploy MOI MCP Gateway" (dev, production or both). Short outage per deploy. Not on npm; the package name is undecided | Adithya (author), Voyage team and Srikar (voyage-api). A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin. |
| `sarvalabs/voyage` (private) | Voyage explorer app, faucet, playgrounds; Next.js 13 | voyage.moi.technology | Merge to `develop` builds image `voyage-ui` through GitHub Actions and Teleport. Commits need `feat:` or `fix:` prefixes | Vinay, Gokul, Prakhar |

## SDK, node and examples
| Repo | What | Deploys by | Ask |
|---|---|---|---|
| `sarvalabs/js-moi-sdk` (public, `main`) | TypeScript monorepo, 13 packages. Repo at 0.9.0-rc3, but rc3 existed on GitHub only when last checked. The Launchpad, Explorer and MCP pin 0.9.0-rc2, and `npm view js-moi-sdk dist-tags` answered `latest: 0.9.0-rc2` on 2026-10-03, with rc2 the newest version on npm. Pin rc2 unless Gokul names another, and run that command before quoting a version | A release publishes to npm and uploads the skill zip to R2 | Gokul, Harsh Rastogi, Vinay |
| `js-moi-agent-registry` (npm) | Registry client; embeds a registry id and reads an override once at load | npm | ASK: Gokul where the repo is |
| `sarvalabs/go-moi` (private, `develop`) | The node. Release tags such as v0.13.0, which the release notes call moipod | The protocol team releases; devnet runs some build of it | Gokul |
| `sarvalabs/cocolang` (private) | Coco compiler; releases tagged v0.9.x | Docs at cocolang.dev | Robert Špendl |
| `moi-foundation/MOI-Webinars` (public) | Builders sessions with code, decks and scripts; release pack; x402 review package. Not an app | No deploy. One branch per session, PR to `main`. A push here publishes, because the repo is public. As of 2026-10-02: `main` holds sessions 1 to 7, and session 7's code, README, EXPLAINER and deck are all there (48 files). Sessions 8, 8-policies and 9, `x402-compat/` and `scripts/buffer.mjs` are on branch `claude/agent-payments-simple`, about 100 commits ahead of `main` on 2026-10-01. `protocol-release-0.13.0/` is on neither: it exists only on the previous operator's machine, as one of 6 unpushed local commits (27efaa3, 11 files; the other 5 are x402 and `buffer.mjs` work) plus 3 untracked files (`BLOG.md`, `RELEASE-NOTE.md`, `social/discord.txt`), read with git on 2026-10-03. ASK: Adithya for a copy | Adithya |
`community-call-14/` and `intro-session/` in MOI-Webinars are untracked and exist only on the previous operator's machine, as do those 6 unpushed commits and about 35 files. ASK: Adithya for a copy.

Demos in the account `sarvalabs-adithya`, not the org:
- `agent-dating` (July; still live on 2026-10-01). A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin.
- `moi-agent-budget` (private), `moi-forge-hacks-demo` (March), `moinkee-nft-minter`, `contextual-compute-foundation-website` (contextualcompute.org), and `moisprint` (see Programs).
- `moinkee-nft-minter`, the contextual-compute site and `moisprint` run on Vercel (`moisprint.vercel.app` answered 200 on 2026-10-03), and an old copy of the website is still live at moi-website.vercel.app (200 on 2026-10-03; to take down). `moi-mcp-go` and `moi-dex-demo` have no remote. Each needs a devnet redeploy after a reset and several pin old SDK versions. <!-- slop-lint: ignore -->

## Programs
| Repo | What | State | Ask |
|---|---|---|---|
| `moi-foundation/awesome-moi` (public) | Curated MOI resource list, markdown, PR to `main`, no deploy | Links not checked since January 2026. CODEOWNERS lists `@moi-rahul @sarvalabs-adithya @sarvalabs-rahul`. Read on GitHub 2026-10-03: `main` is at commit 1ed873a (2026-01-16), and the branch `add-tswap-resource` is on GitHub at 83653b1. The Forge onboarding rewrite of `resources/moi-sprint/README.md` is uncommitted on the previous operator's machine (ASK: Adithya for a copy) | Rahul |
| `moi-foundation/moi-sprint` (public) and `sarvalabs-adithya/tSwapper`, `moisprint` | MOI Sprint: self-paced challenges, built January and February 2026 | `moisprint.com`, which the READMEs cite, did not resolve on 2026-10-02 or 2026-10-03. `moi-sprint` was read on 2026-10-03: a README, `01-native-assets/README.md` and a LICENSE, 3 commits, the last on 2026-01-13, Discussions off | ASK: Rahul if it is alive. A security finding is open on this product as of 2026-10-02. ASK: Adithya for the handover note before touching its admin. |
| `sarvalabs-adithya/moi-forge-hacks-demo` | MOI Forge Hacks, run once at Presidency College, 17 to 31 March 2026 | No later run found | ASK: Rahul |

## Standards work
| Target (external) | What | State |
|---|---|---|
| `ChainAgnostic/namespaces` (CASA) | PR 1: namespace folder `moi/` | Nothing filed as of 2026-10-02. The reference format (`moi:devnet`, `moi:112`, `moi:14`) is undecided |
| `x402-foundation/x402` | PR 2: `specs/schemes/exact/scheme_exact_moi.md`. PR 3: `typescript/packages/mechanisms/moi`, package `@x402/moi`. PR 4, other SDKs, recommended skip | Not filed. Filing order is fixed: namespace, spec, mechanism |
The review package is `x402-compat/review-package/` in MOI-Webinars (branch `claude/agent-payments-simple`), with uncommitted edits dated 2026-10-01 that exist only on the previous operator's machine (ASK: Adithya for a copy). Drive copies are older. Nothing is filed until Rahul reviews (agreed 2026-09-09). Blockers: network ID reference, the `discussions-to` URL, a GPG signing key ("not configured"), a funded wallet, who files. Upstream rules ask for an AI-assistance disclosure in the PR description while house rule 4 bans the "generated with" footer. ASK: Rahul how to word the disclosure.

## State to know on day one (as of 2026-10-02, from live probes)
| Where | State |
|---|---|
| Website | `GET /api/community-calls` returns 500 (issue #3 since 2026-04-20). The browser also calls the dev host for the API, so fixing Supabase alone will not fix the homepage, which falls back to a schedule written in code. The chatbot has been hidden since 2026-06-08. Open PRs: #57, #56 (September release social copy, never merged), #54, #52, #8 |
| Dataroom | 6 of 23 documents are not embedded |
| Points | Production runs `feature/ci-cd` at the 16 September commit. Database is on a personal free Supabase login with no backups. PRs #21, #15, #1 open |
| Launchpad | `/api/stats` reported chainStatus ok, 33 active agents. Pins the post-2026-09-11 registry id |
| Explorer | Live index stale (49 agents, `/admin/sync` returns 404), so PR #5 is not deployed |
| MCP | Live server is the 2026-09-23 sync: 13 tools, registry reads still hit the wiped registry. The registry pin of 2026-09-23 is on `master` (pushed; clone fetched 2026-09-24), so what production lacks is a sync and a deploy. voyage-api PR #313 open, no review. Other unpushed work exists on the previous operator's machine (ASK: Adithya for a copy) |
| Docs sweep | PRs open: moidocs #124 (Rahul's change request met, not re-reviewed), coco-docs #12 (approved by Robert), voyage-docs #5, js-moi-sdk #150, voyage #447 |

## Read-only health checks (GET only; observed healthy answers on 2026-10-02 unless noted)
| Product | Command | Healthy answer |
|---|---|---|
| Website | `curl -sI https://moi.technology/` and `curl -s https://moi.technology/api/health` | 200, `{"status":"ok"}`. `curl -s https://moi.technology/api/community-calls` should be a JSON array but returned 500 |
| Blog | `curl -sI https://blog.moi.technology/` (also `/rss.xml`, `/llms.txt`) | 200 |
| Dataroom | `curl -sI https://dataroom.moi.technology/` and `curl -s https://dataroom.moi.technology/api/documents` | 307 to `/home`; JSON list where every `embedding_status` is `completed` (6 of 23 were not) |
| Points | `curl -s https://points.moi.technology/api/health` | `healthy` true, `database` ok, `migrations.applied` equal to `expected` |
| Launchpad | `curl -s https://launchpad.moi.technology/api/stats` | `"chainStatus":"ok"`. The first call after idle can say `stale`; call again after 20 to 60 seconds |
| Explorer | `curl -s https://api.agents.moi.technology/health` | `{"status":"ok"}`. That only proves the process is up; compare `/registry/agents` total with the chain |
| MCP | `curl -s https://mcp.voyage.moi.technology/health` and the same on `mcp-read.voyage.moi.technology` | `"ok":true` on both |
Read the data in each answer as well as the status code. A green deploy run proves little, and a 200 proves little on a site that answers 200 for any address (the website does).

## Not yet known
- Who owns the Cloudflare account, the Supabase projects (website, Dataroom, Launchpad) and each vendor login. See `keys-and-access.md`. ASK: Rahul.
- What the two VM deploy scripts and the nginx configs do. ASK: Upendhar.
- How the js-moi-sdk docs build and deploy after a merge. ASK: Gokul.
- Whether `sarvalabs/Points-Program` and `moi-foundation/moi-sprint` are still used. ASK: Rahul.
- Which merges need whose approval, per repo. ASK: Rahul.
- Who owns the VM today, Upendhar or Srikar. ASK: Rahul.
