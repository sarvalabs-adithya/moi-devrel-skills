# Agent Skills

**Status: active.** Two public skill bundles teach coding agents how to build on MOI: the Coco skill (compiler 0.9.3, PISA 0.8.2, current) and the js-moi-sdk skill (rebuilt against SDK v0.9.0-rc2 on 13 October 2026 on an unpushed branch; the published copies still say v0.7.1 until that branch lands). Inactive: the devnet write test of the SDK examples (no funded post-reset account), and the R2 copy of the SDK skill, whose public URL nobody has confirmed.

A skill is a folder of Markdown that an agent (Claude Code, Cursor, OpenClaw) loads before writing code: an entry file it reads first, references it reads on demand, and runnable examples. Both skills exist so that an agent writing Coco or js-moi-sdk code gets the real API of a named version instead of guessing from stale npm docs. Robert Spendl maintains the Coco skill. I built the js-moi-sdk skill and maintained the docs-site pages that hand both out.

## Variables

| Variable | Owner | Notes |
|---|---|---|
| Coco skill source (coco-skills/ in sarvalabs/cocolang) and its CDN bundle | Robert Spendl | https://cdn.moi.technology/cocolang/coco-0.9.3-skills.zip. Versioned file name; one zip per compiler release |
| js-moi-sdk skill source (js-moi-skills/ in sarvalabs/js-moi-sdk) | DevRel, with the SDK team (Gokul) merging | On main and develop. The rebuild for v0.9.0-rc2 is the local branch skills/0.9.0 in /Users/adithyaganesh/js-moi-sdk, not pushed, no PR |
| js-moi-sdk skill zip on Cloudflare R2 | SDK team / DevOps | Uploaded by the publish workflow in sarvalabs/js-moi-sdk on every GitHub release. Bucket and prefix are Actions variables (R2_BUCKET, R2_PREFIX, R2_ACCOUNT_ID); keys are secrets. Public URL unknown: ask Upendhar, who wrote the job (PR #141) |
| Static copy the docs site serves | DevRel | moidocs, static/downloads/js-moi-sdk-skills.zip, linked from docs/build/skills/js-moi-sdk-skill.md. Updated by hand; the refreshed zip is committed on the geo-fixes branch of /Users/adithyaganesh/untitled folder 10/moidocs, not pushed |
| Docs pages for both skills | DevRel | moidocs docs/build/skills/ (index.md, coco-skill.md, js-moi-sdk-skill.md). The Coco page links the CDN zip by version; the SDK page links the static copy without naming a version |
| Devnet account for running the SDK examples | DevRel | The old DevRel test wallet's accounts no longer exist after the 11 September reset. Whoever reruns the examples needs an account that exists and holds KMOI |
| Coco compiler binaries | Cocolang team | 0.9.3 was built from the private repo for this audit; the public download is the one the Coco page points at |

## Stack

| Piece | What it is |
|---|---|
| Coco skill bundle | SKILLS.md (entry, with a "what's new" table per release), AGENTS.md (maintenance), reference/ (16 numbered topics from language basics to access control), examples/ (six .coco programs), standards/ (mas0, mas1, mas2 sources with their coco.nut). Verified by compiling, not by reading |
| js-moi-sdk skill bundle | SKILL.md (entry: migration table, 60-second flow, gotchas, reference map), AGENTS.md (maintenance: read the sources, never memory), references/ (ten files, one per SDK area, each stamped "verified against vX"), examples/ (four devnet flows in plain JavaScript with their Coco sources), README.md, CHANGELOG.md, LICENSE (MIT) |
| Publish path, Coco | Robert builds the zip from coco-skills/ and puts it on the CDN; the docs page is edited to the new file name |
| Publish path, js-moi-sdk | .github/workflows/publish.yml in sarvalabs/js-moi-sdk, job upload-agent-skill: after the npm publish it zips js-moi-skills/ twice (js-moi-sdk-<version>-skills.zip and js-moi-sdk-skills.zip) and uploads both to R2 with the AWS CLI. The docs site does not read R2; its copy is manual |
| Test tooling | The Coco compiler itself (`coco nut init`, `coco compile`); for the SDK, a scratch npm project with the exact package version, dotenv for the mnemonic, js-polo for decoding, and a Node script that builds every example's interaction offline |

## How it works

**Coco skill.** Each reference file describes one language area for a named compiler version, and the examples and standards are real programs. The claim the bundle makes is "this compiles with 0.9.3 at PISA 0.8.2", so the check is to compile every .coco in it. The 0.9.3 bundle passed on 13 October 2026: all six examples and all three standards exit 0 and emit a manifest. The entry file's "what's new" tables are the migration notes between compiler versions (0.9.2 dropped `endpoint enlist`; 0.9.3 added `sweep` on primitives and rejects write-after-sweep and recursive classes). Nothing in it names the SDK.

**js-moi-sdk skill.** The skill's own rule (AGENTS.md) is that every claim must be traceable to a file under packages/*/src.ts at the tagged version; release notes are a map of where to look, not a source (the 0.8.0 notes say `predictAssetId`, the code says `deriveAssetId`). The rebuild to v0.9.0-rc2 read the full diff between v0.7.1 and the rc2 tag and corrected: the LogicState/ActorState rename, the MAS0/1/2 `create` signatures and the MASX-only AssetFactory, KMOI as MASN with its new asset id, the fee payer, the sender no longer being a participant, the `decimals` argument position, fuel defaults 50 and 100000, the 10 KMOI storage fund bundled into every deploy or create, `deriveAssetId`/`deriveLogicId`, and the storage and access-policy interactions. The rc3 tag (GitHub only, not on npm) renames `payer` to `fee_payer` and adds key weight and asset call decoding fixes; those are noted inline so an agent can tell which it is running. The CHANGELOG entry lists the change per reference.

**Where each copy lives.** The SDK skill has three copies that can drift: the folder in the SDK repo (source of truth), the R2 zips (written by the release workflow, public URL unconfirmed), and the static zip on the docs site (manual). On 13 October the two public copies were byte-identical and both said v0.7.1 while npm `latest` was 0.9.0-rc2. The Coco skill has two: the repo folder and the versioned CDN zip, which matched.

## Process

**Re-checking a skill when a release lands**

Coco:

- Read the release notes for syntax changes, then the bundle's SKILLS.md "what's new" table; Robert usually ships the bundle with the compiler.
- Get the matching compiler (`coco version` prints Coco and PISA versions).
- For each file in examples/ and standards/: make an empty folder, `coco nut init <Module>` (the module name is the identifier after `coco` or `coco asset` on the first code line), copy the .coco in, set `[target.pisa] version` in coco.nut to the target the bundle names, run `coco compile .`, and record the exit code and the manifest file name, or the exact error text.
- A failure is a note to Robert, not an edit in our repo.
- Then point moidocs docs/build/skills/coco-skill.md and index.md at the new CDN file name.

js-moi-sdk:

- `git fetch --tags` in a clone of sarvalabs/js-moi-sdk and `git checkout vX.Y.Z`; `npm install` so the umbrella builds. Note what moved: `git diff --stat vPREV vX.Y.Z -- packages | grep -vE '/lib\.|package-lock'`.
- Walk the references in the package order AGENTS.md gives (constants and utils, identifiers, providers and interactions, signer and wallet, manifest, logic, asset, then concepts, patterns, SKILL.md). For every exported name, signature, enum value, constant and error string in a reference, grep it in src.ts and fix the text. Never write from the release notes or from memory.
- Bump every "verified against" stamp (`grep -ril "verified against" references/*.md | wc -l` must be 10) and add a CHANGELOG entry per reference.
- Test the examples: `npm install js-moi-sdk@X.Y.Z js-polo dotenv` in a scratch folder, load the devnet mnemonic through dotenv (never `source` the env file in a shell: an unquoted mnemonic prints its first word as a command-not-found error), run each example script against devnet with a funded account, check `receipt.status === 0` and every operation's status, and paste the interaction hashes into the CHANGELOG. Compile the Coco snippets embedded in the examples with the matching compiler.
- If devnet is unusable, run the offline script instead (below) and say so in the CHANGELOG and the examples; do not imply a run.
- Zip the folder as the workflow does (`cd js-moi-skills && zip -r ../js-moi-sdk-skills.zip .`), copy it over moidocs static/downloads/js-moi-sdk-skills.zip, and if the docs page ever names a version, update it.
- Open a PR to sarvalabs/js-moi-sdk; the release workflow uploads the zip to R2 on the next GitHub release.

**The exact test run of 13 October 2026**

Both logs and the scripts are in the side-session notes folder of the handover session (agent-skills-js-moi-sdk-test-log.md, offline-tests.mjs, probe.mjs) and in the Claude scratchpad paths named inside the log.

- Coco: prebuilt coco 0.9.3 binary (PISA 0.8.0 runtime), nine compiles as above at PISA target 0.8.2, nine passes, no content change.
- SDK, devnet reads: VoyageProvider("devnet") answered net.Version 0.13.0; moi.AssetInfoByAssetID on KMOI (decimals 0x9), moi.AccountMetaInfo on SARGA_ADDRESS, moi.StoragePricing and moi.LogicManifest on KMOI all answered.
- SDK, devnet writes: not run. The old DevRel test wallet's accounts answer `account not found` on /devnet/ and /babylon/ since the reset, and the faucet funds only existing accounts.
- SDK, offline: the script builds every example's interaction with a pinned sender (`ixData({ sender })`), inspects operations and participants, POLO-serializes and signs it, and asserts the validator rejections. 35 cases; the result table is in the log. It proves names, signatures, argument order, the bundled storage-fund transfer and its predicted beneficiary, and the participant rules. It cannot prove node acceptance, fuel or storage costs.

**Checking it is healthy**

- Download both zips from the docs site and the CDN, unzip, and compare the stamps with `npm view js-moi-sdk dist-tags` and the Cocolang release page. A stamp older than `latest` means the skill is stale.
- `grep -ril "verified against" references/*.md | wc -l` is 10 and `grep -rhoE "v0\.[0-9]+\.[0-9]+(-rc[0-9]+)?" SKILL.md references/*.md | sort | uniq -c` shows one dominant version.
- The docs page links resolve (static/downloads for the SDK zip, cdn.moi.technology for Coco).

## Open items

- Land the skills/0.9.0 branch: review, open a PR to sarvalabs/js-moi-sdk, and after the next release confirm the R2 upload and find out its public URL. Until then the docs site's zip (on the unpushed geo-fixes branch of moidocs) is the only refreshed public copy, and it is not pushed either.
- Run the four SDK examples on devnet with a funded post-reset account and add the interaction hashes to js-moi-skills/CHANGELOG.md; the examples say their last on-chain run was with 0.7.1 before the September reset.
- Decide whether the docs page should name the SDK version the zip was verified against; today it names none, so a reader cannot see staleness.
- rc3 is on GitHub only. When it or 0.9.0 final reaches npm, re-stamp: the `payer` to `fee_payer` rename changes what fee-payer code must write.
- The 0.8.0 release notes name `predictAssetId`/`predictLogicId`; the code exports `deriveAssetId`/`deriveLogicId`. Tell Gokul so the notes get fixed.
- The js-moi-sdk skill's lockup example reaches a protected provider method (`moi.Lockups`) that is not a public RPC in the SDK; it worked on 0.7.1 and has not been re-verified on 0.13.0.
- Automate the staleness check: the MCP server's upstream-watch workflow already opens an issue on each js-moi-sdk and cocolang release (MCP-SERVER.md); add "re-check the skill" to what that issue asks for.
