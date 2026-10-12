# Publishing: the package and registry questions that are open

Nothing is published. This file lists what is open, who decides, and the checks you can run without deciding anything. **Do not guess a name, a scope, an owner or a date.** Facts are as of 2026-10-03 (npm and GitHub reads) and 2026-10-02 (research). Back to `../SKILL.md`.

## State, and how to re-check it (all read-only)

| Fact | Re-check |
|---|---|
| `@moi-protocol/mcp-server` and `@sarvalabs/mcp-server` are both unclaimed: the npm registry answered "Not found" for each on 2026-10-03 | `npm view @moi-protocol/mcp-server` and `npm view @sarvalabs/mcp-server` (an E404 means unclaimed) |
| `package.json` in `sarvalabs/moi-mcp` names the package `@moi-protocol/mcp-server`, version 0.1.0, with four bins (`mcp-server`, `moi-mcp`, `moi-mcp-http`, `moi-mcp-hosted`) | Read the file on `master` |
| `moi-mcp` has no git tag | `git ls-remote --tags https://github.com/sarvalabs/moi-mcp.git` prints nothing |
| `.github/workflows/publish.yml` publishes on a pushed tag matching `v*`: typecheck, tests, build, then `npm publish --access public --provenance` with the secret `NPM_TOKEN` | Read the file. Whether `NPM_TOKEN` is set: `gh secret list -R sarvalabs/moi-mcp` (names only; repo admin access) |
| The live server already calls itself `@moi-protocol/mcp-server` in its `ping` answer, so a rename changes what the server reports | The `ping` line of `mcp-health.sh` |
| `README.md`, `docs/quickstart.md` and `examples/claude-desktop.json` all tell users to run `npx -y @moi-protocol/mcp-server`. That fails today | Say so to any user who asks |
| The repo's `docs/publishing.md` is stale in one point: its step "create the GitHub repo" is done (`sarvalabs/moi-mcp` exists and is public) | Read it before you quote it |

## Open questions

| # | Question | Why it matters | ASK |
|---|---|---|---|
| 1 | Which name: `@moi-protocol/mcp-server` or `@sarvalabs/mcp-server`? | Whoever owns the npm org owns the release, and claiming the wrong scope is awkward to undo. The repo calls this a decision, not a technical step | Rahul |
| 2 | Who owns the npm organisation and account, and who creates `NPM_TOKEN` | The workflow cannot publish without it. Nobody is recorded as holding either | Rahul |
| 3 | Ship a shared `WC_PROJECT_ID`, or make every user bring one | Today each user needs a free Reown project, an extra step on every local install | Rahul |
| 4 | Has the phone-approved write path passed once (transfer and create-asset, `connect-and-verify.md` rows 13 to 15)? | The repo's plan says not to publish a write path no human has approved. Its record stops at 2026-09-01 | Adithya |
| 5 | Which pitch: "MOI needs an MCP endpoint" (then the hosted Go idea leads and this server is a reference) or "an agent touches MOI without holding keys" (then this server is the product) | It decides which package is promoted and what the announcement says. Rahul's objection that there is no big use case is unresolved in the repo's plan | Rahul |
| 6 | Does the production copy in voyage-api become an install of the published package once it exists | `DEPENDENCIES.md` section 18 raises it as an option (a local file: ASK: Adithya for a copy) | Rahul, Srikar |
| 7 | Directory listings (Smithery, Glama, PulseMCP, mcp.so, Cursor, then Anthropic's connector directory last): who submits, from which account | Drafts exist in `docs/launch/` on `master`. The plan says one first impression per directory, so not before a demo exists | Rahul |
| 8 | Is the Go server `moi-mcp-go` a release train of its own | The plan says separate repo and lifecycle. It has no remote and exists only on the previous operator's machine | Adithya |

## What DevRel does now
- Run the read-only checks above and report any change: the name appearing on npm under someone else's account is the case to catch.
- Do not run `npm publish`, do not create or push a `v*` tag, do not set `NPM_TOKEN`. A pushed tag publishes to a public registry: it is a GATE and, until questions 1 and 2 are answered, not a decision DevRel can make.
- Public wording about this server: say devnet, and make no mainnet claim. The repo's plan notes MOI published no mainnet RPC URL or CAIP-2 id; the devnet identifier question is open (`moi-devrel/references/devnet.md`). Any post goes through `moi-devrel/claim-check` first and is published by `moi-blog`.
- Do not tell users to use `npx` for this server.

## If Rahul settles questions 1 to 4 (the repo's own sequence, every step a GATE)

| # | Step | Do this | Gate |
|---|---|---|---|
| 1 | Name | If it changes, edit `name` in `package.json` (and the docs and examples that quote it) by PR | GATE |
| 2 | Token | The owner sets `NPM_TOKEN`, typing the value at a hidden prompt: `gh secret set NPM_TOKEN -R sarvalabs/moi-mcp`. Claude never sees it | GATE |
| 3 | Tarball check | In a working copy of `sarvalabs/moi-mcp`: `npm run typecheck && npm test && npm run build && npm pack`, install the tarball in a scratch folder, run `moi-mcp help`, start `moi-mcp-http` and GET `/health` with nothing configured. This caught a phantom dependency and a silent bin. `npm ci` and the tarball install download from npm | GATE (the downloads), then local |
| 4 | Phone checks | `connect-and-verify.md` rows 13 to 15 pass once | GATE |
| 5 | Tag | The plan says publish `0.1.0`, not `1.0.0`, because the write path may change when the wallet's own send call is fixed. `git tag v0.1.0` then push the tag: this publishes | GATE |
| 6 | Verify | `npm view <name>` (read), then install it in a scratch folder and start it (a download) | read, then GATE for the install |
| 7 | After | A working demo (`docs/demo-script.md`), directory submissions, then the announcement | GATE for each send |

## Not yet known
- Everything in the open-question table. The owner of each decision is in its last column.
- Whether Anthropic's connector directory sets requirements this server does not meet. ASK: Rahul.
