# Other projects: Moinkee, Agent dating, MOI Sprint, Contextual Compute website

**Status: three inactive, one live.** Four small projects DevRel built. Moinkee, Agent dating and MOI Sprint are inactive; none is hosted any more (the Moinkee and Sprint Vercel projects were deleted on 14 October 2026). Each repo moves from Adithya's GitHub account to the sarvalabs organisation on 14 October 2026. The one thing with ongoing value is the Pinata account behind Moinkee: see "Moving Pinata" below.

Marketing: How it works. Developers: everything.

None of the three needs anything to keep running. Each repo's README has a "Pick it up" section for whoever restarts it.

## How it works

| Project | What it is | Live | Repo after the transfer |
|---|---|---|---|
| **Moinkee World Tour mementos** | A site where visitors mint a memento NFT on devnet: a photo from a Moinkee event, pinned to IPFS through Pinata and minted from the site's wallet | Not hosted: the Vercel project was deleted on 14 October 2026 | sarvalabs/moinkee-nft-minter |
| **Agent dating** | An OpenClaw plugin: two AI agents register on the MOI agent registry, find each other and chat through a small relay, shown live | Not hosted. The public relay was retired with its server; anyone runs their own relay (README, Pick it up) | sarvalabs/agent-dating |
| **MOI Sprint** | A self-paced challenge track ("learn MOI by building"): two Coco challenges (Soulbound Badge, Simple Swap) and a guide site. Scratched from the handover on 13 October | Not hosted: the Vercel project was deleted on 14 October 2026 | sarvalabs/moisprint (guide site) and sarvalabs/tSwapper (challenge scaffolds; branch `solution` holds the answers) |

| **Contextual Compute Foundation website** | A one-page site: thesis, six papers (CC0 to CC5), a join form that posts each email to a webhook | **Live** at www.contextualcompute.org (Vercel; the apex redirects to www) | sarvalabs/contextual-compute-foundation-website |

The Sprint's chapter text is already in moi-foundation/moi-sprint.

## Variables

| Item | Owner | Notes |
|---|---|---|
| The four repos | sarvalabs org (from 14 October) | Public. Moved from sarvalabs-adithya |
| Vercel projects moinkee-nft-minter and moisprint | Deleted on 14 October 2026 | To bring a site back, import the repo into a company Vercel team and set its env vars (README) |
| Pinata account (Moinkee images and metadata, 71 files, 13.6 MB) | Adithya's account today | Moves to a company Pinata account that Srikar is creating. See below |
| Moinkee minting wallet | Nobody | Nothing to move. The next owner makes a new devnet wallet and a new collection (README) |
| Contextual Compute site: Vercel project, domain contextualcompute.org (Namecheap, registered to 2027-03-28), DNS (Cloudflare, company-owned), mail forwarding (Namecheap) | Vercel and Namecheap logins not recorded (ASK: Rahul) | The only one of the four still live. Keep its Vercel project |
| Agent dating relay server | Retired | Its VPS was cancelled; the plugin no longer points at it |

## Env vars

Names only. Moinkee: `ADMIN_MNEMONIC`, `NEXT_PUBLIC_ASSET_ID`, `PINATA_JWT`, `NEXT_PUBLIC_FOLDER_CID`, `RECOVERY_SECRET` (see the repo's `.env.example`; the Vercel project that held the production values was deleted). Agent dating: `.env.example` in the repo (relay URL and token, per-agent devnet wallet, optional model key). MOI Sprint: the progress logic id in the site's Vercel environment, gone after any devnet reset. Contextual Compute site: `SUBSCRIBE_WEBHOOK_URL` only, the address the join form posts to (in its Vercel project; where it points is not recorded). The cross-product index is ENV-VARS.md.

## Process

### Moving the repos

One command per repo, run by the repo owner (Adithya) with a GitHub login that can create repos in sarvalabs. An org owner may have to accept.

```bash
gh api repos/sarvalabs-adithya/moinkee-nft-minter/transfer -f new_owner=sarvalabs
```

The same for `agent-dating`, `moisprint`, `tSwapper` and `contextual-compute-foundation-website`. The Contextual Compute site keeps serving after its move; check that its Vercel project still deploys from the moved repo. GitHub redirects the old addresses. No hosting is attached any more, so nothing else needs reconnecting.

### Moving Pinata

Why it matters: every Moinkee image and token metadata file lives on IPFS, and Pinata keeps it online (pinned). If the account closes and nothing else pins the files, the images and metadata disappear and the recovery flow after a devnet reset stops working. **IPFS addresses (CIDs) are content hashes, so they do not change when the files move**; minted tokens point at `ipfs://<CID>` and the site reads through the public ipfs.io gateway, not an account-specific one. Moving the account changes nothing users see.

The list of every pinned file (CID, name, size, date) is in this repo at `others/moinkee/pinata_pins.json` (71 rows), with `recovered.json` and `snapshot.json` (token owners and metadata, used by the recovery flow).

**The company account already exists**: sarvalabsdeveloper@gmail.com (the shared company developer login) has a Pinata account. Adithya's account (login adithya@sarva.ai, free plan, one workspace, members need a paid plan) is the source. The 71 CIDs are one folder holding the memento images (13.6 MB) and 70 small metadata files. The script `others/moinkee/repin-to-pinata.py` does Option B against the company account: `--dry-run` lists the CIDs, a plain run asks for the company JWT at a hidden prompt, pins the folder first and waits until all 71 are pinned, and `--check` confirms. It writes a log and never prints the key.

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
5. The site is not hosted now. Whoever brings it back sets `PINATA_JWT` to the company account's JWT.
6. After a week with nothing broken: revoke the old account's API keys, then unpin or close the old account.

Do this before Adithya's account goes away. Until then the files stay pinned.

### After a devnet reset

Only Moinkee and the Sprint hold chain state. Moinkee: new collection, new `NEXT_PUBLIC_ASSET_ID`, then the recovery flow in `docs/pinata-recovery.md` re-mints every memento to its owner from what Pinata kept. Sprint: a new progress logic. Agent dating agents register again.

## Claude skill

None. The moi-devnet-reset skill lists Moinkee as one row of what a reset breaks.

## Open items

- Transfer the five repos to sarvalabs (14 October).
- Two public repos contain a committed 12-word devnet recovery phrase: moinkee-nft-minter `scripts/getTdu.mjs` and tSwapper `Swap/src/lib/logic.js` (`POOL_OWNER_MNEMONIC`). Treat both wallets as public: never fund them. Removing the lines does not remove them from history.
- MOI Sprint: the guide repo's README is the unedited Next.js template, and tSwapper's `solution` branch holds the challenge answers in public. A challenge prototype (`Sprint/Challenge 1/moisprint-challenge-mas0`) existed only on Adithya's laptop and is not in any repo.
- Contextual Compute site: confirm where `SUBSCRIBE_WEBHOOK_URL` sends sign-ups (if unset, every sign-up is thrown away). The CC3 paper shows as locked on the page but its PDF is still served at /docs/CC3.pdf. The README is the unedited Next.js template. Who holds the Vercel and Namecheap logins is not recorded (ASK: Rahul).
- Leftover branches: moinkee-nft-minter (three merged handover and Claude branches) and agent-dating (seven old feature branches) can be deleted after the move.
- Move Pinata (Option A or B) once Srikar's company account exists. Owner: Srikar.
- The Agent Explorer also lists a Pinata account, with no key passed in production; who owns it is not recorded (ASK: Rahul).
