# Decisions log: the form

Two blocks of `DECISIONS.md` from the CASA folder. Each block says who decides, the options, exactly what changes, and what changes outside the PR.

## 1. The reference format: BLOCKING

**Decides:** the protocol team and the reviewer.

The reference half of `moi:<reference>` is currently a network name (`moi:devnet`). The client SDK
also carries `enum Chain { TEST_NET = 111, DEV_NET = 112, MAIN_NET = 113 }`, unused today, and the
planned network-identity RPC may surface exactly those numbers. If it does, a numeric reference
becomes available and every other registered chain that has a chain id uses one. <!-- slop-lint: ignore -->

**Option A: keep names.** `moi:devnet`, `moi:mainnet`. Human-legible, matches `stellar:pubnet`.
Nothing in the document changes.

**Option B: use the network ID.** `moi:112` for devnet. Matches `eip155` and `neo`. Changes:

| Section | Change |
| --- | --- |
| Semantics | reference becomes the network ID, not the network's name |
| Syntax | regex becomes `^(0\|[1-9][0-9]{0,9})$`, plus a range bound: copy Neo's wording |
| Well-known networks | table keys on ids: devnet `112`, mainnet `113` |
| Resolution Mechanics | reads the id from the new RPC |
| Rationale | the "numeric chain id was rejected" paragraph inverts; the "short network name" paragraph becomes the rejected option | <!-- slop-lint: ignore -->
| Test Cases | every example is rewritten; the hyphen and case cases stop being meaningful |

Roughly an hour of editing, mechanical once the choice is made.

**Knock-on outside this PR:** `moi:*` appears in the scheme spec (PR 2) and in
`src/constants.ts` of the mechanism package (PR 3). Both follow whatever is decided here.

---

## 3. `discussions-to`: can be closed today

**Decides:** the author named in the front matter.

Currently the CASA PR's own URL, with
the number filled in once the PR is opened. That is the simplest route and needs nothing set up
beforehand.

It does not have to be the CASA PR, though. Neo points at `neo-project/proposals/issues/238` and
Stellar at a CAIP pull request, so any monitored URL is acceptable. An issue on a public MOI repo
would give CASA somewhere to send questions that outlives the PR thread, if that is wanted later.

Whoever owns that URL has to actually watch it. The only namespace PR that has ever failed on
merit failed because its author went quiet for 587 days.
