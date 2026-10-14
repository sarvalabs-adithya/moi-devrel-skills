# Other projects: Moinkee, Agent dating, MOI Sprint

**Status: inactive.** Three small projects DevRel built that nobody runs day to day. Each repo moves from Adithya's GitHub account to the sarvalabs organisation on 14 October 2026. The one thing with ongoing value is the Pinata account behind Moinkee: see "Moving Pinata" below.

Marketing: How it works. Developers: everything.

None of the three needs anything to keep running. Each repo's README has a "Pick it up" section for whoever restarts it.

## How it works

| Project | What it is | Live | Repo after the transfer |
|---|---|---|---|
| **Moinkee World Tour mementos** | A site where visitors mint a memento NFT on devnet: a photo from a Moinkee event, pinned to IPFS through Pinata and minted from the site's wallet | moinkee-nft-minter.vercel.app (Vercel) | sarvalabs/moinkee-nft-minter |
| **Agent dating** | An OpenClaw plugin: two AI agents register on the MOI agent registry, find each other and chat through a small relay, shown live | Not hosted. The public relay was retired with its server; anyone runs their own relay (README, Pick it up) | sarvalabs/agent-dating |
| **MOI Sprint** | A self-paced challenge track ("learn MOI by building"): two Coco challenges (Soulbound Badge, Simple Swap) and a guide site. Scratched from the handover on 13 October | moisprint.vercel.app (Vercel), guide only | sarvalabs/moisprint (guide site) and sarvalabs/tSwapper (challenge scaffolds; branch `solution` holds the answers) |

The Sprint's chapter text is already in moi-foundation/moi-sprint.

## Variables

| Item | Owner | Notes |
|---|---|---|
| The four repos | sarvalabs org (from 14 October) | Public. Moved from sarvalabs-adithya |
| Vercel projects moinkee-nft-minter and moisprint | Adithya's Vercel account today | Transfer to a company Vercel team, or delete if nobody wants the sites up (open item) |
| Pinata account (Moinkee images and metadata, 71 files, 13.6 MB) | Adithya's account today | Moves to a company Pinata account that Srikar is creating. See below |
| Moinkee minting wallet | Nobody | Nothing to move. The next owner makes a new devnet wallet and a new collection (README) |
| Agent dating relay server | Retired | Its VPS was cancelled; the plugin no longer points at it |

## Env vars

Names only. Moinkee: `ADMIN_MNEMONIC`, `NEXT_PUBLIC_ASSET_ID`, `PINATA_JWT`, `NEXT_PUBLIC_FOLDER_CID`, `RECOVERY_SECRET` (see the repo's `.env.example`; production values are in the Vercel project). Agent dating: `.env.example` in the repo (relay URL and token, per-agent devnet wallet, optional model key). MOI Sprint: the progress logic id in the site's Vercel environment, gone after any devnet reset. The cross-product index is ENV-VARS.md.

## Process

### Moving the repos

One command per repo, run by the repo owner (Adithya) with a GitHub login that can create repos in sarvalabs. An org owner may have to accept.

```bash
gh api repos/sarvalabs-adithya/moinkee-nft-minter/transfer -f new_owner=sarvalabs
```

The same for `agent-dating`, `moisprint` and `tSwapper`. GitHub redirects the old addresses. After a move, a Vercel project that deploys from the repo keeps serving its last build, but new pushes will not deploy until the Vercel GitHub app is allowed on the sarvalabs repo (Vercel, project, Settings, Git).

### Moving Pinata

Why it matters: every Moinkee image and token metadata file lives on IPFS, and Pinata keeps it online (pinned). If the account closes and nothing else pins the files, the images and metadata disappear and the recovery flow after a devnet reset stops working. **IPFS addresses (CIDs) are content hashes, so they do not change when the files move**; minted tokens point at `ipfs://<CID>` and the site reads through the public ipfs.io gateway, not an account-specific one. Moving the account changes nothing users see.

The list of every pinned file (CID, name, size, date) is in this repo at `others/moinkee/pinata_pins.json` (71 rows), with `recovered.json` and `snapshot.json` (token owners and metadata, used by the recovery flow).

Option A, simplest: hand the existing Pinata account to a company login (change its email to a company address in Pinata's account settings, if the plan allows). Pins, keys and everything else stay as they are. Then rotate the API key and update `PINATA_JWT` on Vercel.

Option B: re-pin into the company account.

1. Srikar creates the company Pinata account. The free plan is enough for 71 files and 13.6 MB.
2. In it, create an API key with pinning rights and read access to the pin list. Keep the JWT in the password manager.
3. Pin every CID by hash. Pinata fetches the files from IPFS while the old account still pins them, so nothing is uploaded again. Paste the new JWT at the hidden prompt:

   ```bash
   read -rs NEW_JWT && for cid in $(jq -r '.rows[].ipfs_pin_hash' others/moinkee/pinata_pins.json); do curl -s -X POST https://api.pinata.cloud/pinning/pinByHash -H "Authorization: Bearer $NEW_JWT" -H "Content-Type: application/json" -d "{\"hashToPin\":\"$cid\"}" > /dev/null; done; unset NEW_JWT
   ```

   If the plan does not offer pin by hash, download each file through `https://ipfs.io/ipfs/<CID>` and upload it in the new account, then check the CID comes out the same.
4. Check: the new account's pin list shows all 71 CIDs as pinned (Pinata, Files; or `GET https://api.pinata.cloud/data/pinList?status=pinned&pageLimit=1000` with the new JWT).
5. Point the site at it: Vercel, moinkee-nft-minter, Settings, Environment Variables, `PINATA_JWT` = the new JWT; redeploy.
6. After a week with nothing broken: revoke the old account's API keys, then unpin or close the old account.

Do this before Adithya's account goes away. Until then the files stay pinned.

### After a devnet reset

Only Moinkee and the Sprint hold chain state. Moinkee: new collection, new `NEXT_PUBLIC_ASSET_ID`, then the recovery flow in `docs/pinata-recovery.md` re-mints every memento to its owner from what Pinata kept. Sprint: a new progress logic. Agent dating agents register again.

## Claude skill

None. The moi-devnet-reset skill lists Moinkee as one row of what a reset breaks.

## Open items

- Transfer the four repos to sarvalabs (14 October), then reconnect Vercel if the sites should keep deploying.
- Move Pinata (Option A or B) once Srikar's company account exists. Owner: Srikar.
- Decide for each Vercel site (Moinkee, Sprint): transfer to a company Vercel team or delete. Moinkee's live site still pins the February 2026 code and its asset id predates the devnet resets, so minting likely fails until a new collection is set.
- The Agent Explorer also lists a Pinata account, with no key passed in production; who owns it is not recorded (ASK: Rahul).
