# Other projects: Moinkee, Agent dating, MOI Sprint, Contextual Compute website

**Status: three inactive, one live.** Four small projects DevRel built. Moinkee, Agent dating and MOI Sprint are inactive. None of them is hosted any more: the Moinkee and Sprint Vercel projects were deleted on 14 October 2026. The repos moved from Adithya's GitHub account to the sarvalabs organisation on 14 October 2026. The exception is tSwapper, the Sprint's challenge scaffolds, which stays on his account. The Moinkee files on IPFS were copied into the company Pinata account on 14 October 2026 (see "Moving Pinata").

Marketing: How it works. Developers: How it works, Variables, Env vars, Process, Claude skill, Open items.

None of the three inactive ones needs anything to keep running. Each repo's README has a "Pick it up" section for whoever restarts it.

## How it works

| Project | What it is | Live | Repo after the transfer |
|---|---|---|---|
| **Moinkee World Tour mementos** | A site where visitors mint a memento NFT on devnet: a photo from a Moinkee event, pinned to IPFS through Pinata and minted from the site's wallet | Not hosted: the Vercel project was deleted on 14 October 2026 | sarvalabs/moinkee-nft-minter |
| **Agent dating** | An OpenClaw plugin: two AI agents register on the MOI agent registry, find each other and chat through a small relay, shown live | Not hosted. The public relay was retired with its server. Anyone can run their own relay (README, Pick it up) | sarvalabs/agent-dating |
| **MOI Sprint** | A self-paced challenge track ("learn MOI by building"): two challenges in Coco (also known as Cocolang), Soulbound Badge and Simple Swap, and a guide site. Scratched from the handover on 13 October | Not hosted: the Vercel project was deleted on 14 October 2026 | sarvalabs/moisprint (guide site); the challenge scaffolds stay at sarvalabs-adithya/tSwapper (branch `solution` holds the answers) |
| **Contextual Compute Foundation website** | A one-page site: thesis, six papers (CC0 to CC5), and a join form that posts each email to a webhook | **Live** at www.contextualcompute.org (Vercel, on the sarvalabsdeveloper@gmail.com account; the apex redirects to www) | sarvalabs/contextual-compute-foundation-website |

The Sprint's chapter text is already in moi-foundation/moi-sprint.

## Variables

| Item | Owner | Notes |
|---|---|---|
| The four repos | sarvalabs org (from 14 October) | Public. Moved from sarvalabs-adithya |
| Vercel projects moinkee-nft-minter and moisprint | Deleted on 14 October 2026 | To bring a site back, import the repo into a company Vercel team and set its env vars (README) |
| Pinata account (Moinkee images and metadata, 71 files, 13.6 MB) | The company Pinata account (sarvalabsdeveloper@gmail.com) since 14 October 2026 | Done 14 October 2026: the files were uploaded again, and all 71 are pinned there with the same CIDs as before. Adithya's account no longer matters and can be closed |
| Moinkee minting wallet | Nobody | Nothing to move. The next owner makes a new devnet wallet and a new collection (README) |
| Contextual Compute site: Vercel project, domain contextualcompute.org (Namecheap, registered to 2027-03-28), DNS (Cloudflare), mail forwarding (Namecheap) | Vercel: the sarvalabsdeveloper@gmail.com Vercel account (transferred from Adithya's account on 14 October 2026). Namecheap and Cloudflare: company accounts | The only one of the four still live |
| Agent dating relay server | Retired | Its VPS was cancelled. The plugin no longer points at it |

## Env vars

The index across every product, with the consoles and who holds each login, is ENV-VARS.md. This section gives names only.

- Moinkee: `ADMIN_MNEMONIC`, `NEXT_PUBLIC_ASSET_ID`, `PINATA_JWT`, `NEXT_PUBLIC_FOLDER_CID`, `RECOVERY_SECRET`. See the repo's `.env.example`. The Vercel project that held the production values was deleted.
- Agent dating: `.env.example` in the repo (relay URL and token, per-agent devnet wallet, optional model key).
- MOI Sprint: the progress logic id in the site's Vercel environment. It is gone after any devnet reset.
- Contextual Compute site: `SUBSCRIBE_WEBHOOK_URL` only, the address the join form posts to. It is not set (14 October 2026), so sign-ups are discarded.

## Process

**After a devnet reset**

Only Moinkee and the Sprint hold chain state.

- Moinkee: make a new collection and set a new `NEXT_PUBLIC_ASSET_ID`. Then run the recovery flow in `docs/pinata-recovery.md`. It re-mints every memento to its owner from what Pinata kept.
- Sprint: make a new progress logic.
- Agent dating: the agents register again.

**Moving the repos**

**Done on 14 October 2026** for four repos. The repo owner (Adithya) ran the command for each repo, with a GitHub login that can create repos in sarvalabs. An org owner may have to accept. Kept for reference:

```bash
gh api repos/sarvalabs-adithya/moinkee-nft-minter/transfer -f new_owner=sarvalabs
```

The same was done for `agent-dating`, `moisprint` and `contextual-compute-foundation-website`. `tSwapper` was not moved and stays at sarvalabs-adithya/tSwapper. GitHub redirects the old addresses. The Contextual Compute site kept serving, and its Vercel project now deploys from the sarvalabs repo. The other three have no hosting, so nothing else needed reconnecting.

**Moving Pinata**

**Done on 14 October 2026.** Pin by CID needs a paid plan. So the files were downloaded, checked against their CIDs, and uploaded again to the company account (sarvalabsdeveloper@gmail.com) with `project-handover-docs/attachments/moinkee/reupload-to-pinata.py`. The image folder (`bafybeig65m3...`) and all 70 metadata files came back with their original CIDs. The log is in ~/handover-notes/pinata-reupload-log.txt on Adithya's laptop. The rest of this section is how it was done, kept for a future move.

Why it matters: every Moinkee image and token metadata file lives on IPFS, and Pinata keeps it online (pinned). If the account closes and nothing else pins the files, the images and metadata disappear. Then the recovery flow after a devnet reset stops working. **IPFS addresses (CIDs) are content hashes, so they do not change when the files move.** Minted tokens point at `ipfs://<CID>`. The site reads through the public ipfs.io gateway, which is not tied to any account. Moving the account changes nothing users see.

The list of every pinned file (CID, name, size, date) is in this repo at `project-handover-docs/attachments/moinkee/pinata_pins.json` (71 rows). With it are `recovered.json` and `snapshot.json` (token owners and metadata, used by the recovery flow).

How to repeat it (for example to move the files again):

1. In the destination Pinata account, create an API key with upload rights. Keep the JWT in the password manager.
2. Download the files into a folder, say DIR. Put the 52 entries of the image folder into DIR/folder/ (from `https://ipfs.io/ipfs/<folder CID>/<name>`), the 70 metadata files into DIR/json/<cid>, and the folder's entry list into DIR/folder.json. Public gateways rate-limit, so fetch slowly and retry.
   Then run `python3 project-handover-docs/attachments/moinkee/reupload-to-pinata.py DIR --verify`, which recomputes every CID offline. Then run it without `--verify`. It asks for the JWT at a hidden prompt and never prints or saves it. It uploads the image folder first and then the metadata. If any CID comes back different, it unpins and stops.
3. Run it with `--check`, or look at the account's file list. All 71 CIDs should be there.
4. Whoever brings the Moinkee site back sets `PINATA_JWT` to that account's key.

Pin by CID (`repin-to-pinata.py`, beside it) is quicker but needs a paid Pinata plan. On the free plan it answers "paid feature only".

## Claude skill

None. The moi-devnet-reset skill lists Moinkee as one row of what a reset breaks.

## Open items

None as of 14 October 2026.
