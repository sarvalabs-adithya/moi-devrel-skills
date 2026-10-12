# Future improvements

Not blocking the three PRs. Each is a follow-up once `upfront` is filed.

| # | Improvement | Why | Depends on |
|---|---|---|---|
| 1 | A USD-denominated asset on MOI, or a KMOI/USD price feed sellers can quote against | x402 sellers price in dollars; today `"$0.10"` is refused on MOI because nothing resolves it. Until this exists, MOI sellers price in KMOI and buyers must hold KMOI | A stablecoin issuer on MOI, or an oracle. Interim: `registerMoneyParser` lets a seller plug in its own conversion |
| 2 | `authorization` scheme (`scheme_exact_moi` v2 or a flow variant) | Buyer signs, facilitator co-signs as fee payer and submits; money moves after the resource, which is what every other x402 chain offers by default | moipod v0.13.0 fee payer live on devnet; an expiry on relayed interactions would make it clean |
| 3 | `escrow` scheme via a Coco escrow logic (or `Lockup` / `Release` for a custodial variant) | Buyer protection for larger purchases: the deposit sits in the logic's own account before the resource and is released by code after. Source check on 2026-09-10 (go-pisa `XBIND`/`CALLX`/`CALLM`, go-moi asset engine): a logic can bind itself as origin and call the asset's `Transfer` from its own balance, so the escrow is programmable, not custodial. See `ESCROW-RESEARCH-2026-09-10.md` and `escrow-poc/` | A devnet execution of the proof-of-concept logic with a funded wallet; a refund/expiry rule and per-buyer accounting in the logic; a follow-up scheme spec |
| 4 | Hosted MOI facilitator with a free tier | Coinbase's facilitator is why Base sellers need no infra. A MOI one is cheap to run (reads only) | Someone to operate it |
| 5 | On-chain sponsorship policy for fee payers | Today a sponsor co-signs every interaction from a live service. A Coco logic acting as fee payer, or a signed allowance with expiry, would take the sponsor out of the hot path | Protocol: logic-as-payer, or an allowance primitive |
| 6 | Network id emitted by the node and adopted by the wallet | Closes CASA Resolution Mechanics and the `devnet` / `14` / `112` split | The chain-id PR |
| 7 | Public go-moi | A namespace reviewer can read the node; the CASA doc stops having to say "not public" | Sarva Labs decision |
