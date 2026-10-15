# Migration record

A record of what moved off Adithya's own accounts before he left, and when. Everything here is done. Names only, no secret values.

| Date | What | From | To |
|---|---|---|---|
| 8 October 2026 | Launchpad Supabase project | Adithya's personal Supabase organisation | The company Supabase organisation (owned by sarvalabsdeveloper@gmail.com) |
| 8 October 2026 | Dataroom Supabase project and bucket | Adithya's personal Supabase organisation | The same company organisation |
| 13 October 2026 | Agent dating relay | Adithya's VPS | Retired. agent-dating PR #1 removed the relay address, the deploy workflow and its secrets |
| 13 October 2026 | Moinkee handover changes | | moinkee-nft-minter PR #2 merged (README, env template, recovery routes behind a secret) |
| 14 October 2026 | Repos: moinkee-nft-minter, agent-dating, moisprint, contextual-compute-foundation-website | sarvalabs-adithya on GitHub | The sarvalabs organisation |
| 14 October 2026 | Moinkee files on IPFS (71 files) | Adithya's Pinata account | The company Pinata account (sarvalabsdeveloper@gmail.com), same CIDs |
| 14 October 2026 | Contextual Compute site's Vercel project | Adithya's Vercel account | The sarvalabsdeveloper@gmail.com Vercel account |
| 14 October 2026 | Old Vercel copies: moinkee-nft-minter, moisprint, moi-website, sarva-dataroom | Adithya's Vercel account | Deleted |
| 14 October 2026 | Launchpad Telegram bot @moinetworkbot | Adithya's Telegram account | Rahul Lenkala's Telegram account (@p2pbuddy) |
| 14 October 2026 | Points admin access | adithya@moinetwork.io | sarvalabsdeveloper@gmail.com and points@moinetwork.io (Harsh Gupta's address stays) |
| 14 October 2026 | Handover video folders in Google Drive | Shared with Adithya only | Open to anyone at moinetwork.io, and Rahul invited. Still owned by adithya@moinetwork.io |

**Not moved, on purpose**

- The Points Supabase project stays in the points@moinetwork.io account (managed by Sai Kiran), because the company organisation is at its free-plan limit of two projects. See POINTS-PROGRAM.md.
- tSwapper stays at sarvalabs-adithya/tSwapper.
- The Moinkee minting wallet: nothing to move. Whoever restarts Moinkee makes a new devnet wallet and collection.
- Secrets: they live in each repo's GitHub Actions settings, not with Adithya. ENV-VARS.md says where each one comes from.
