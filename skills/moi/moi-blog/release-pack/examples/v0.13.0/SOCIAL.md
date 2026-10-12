# Social pack: moipod v0.13.0

Both posts are the official release note in its own framing, with sentences restructured
for clarity where the user flagged them (no facts added). Only formatting differs:
backticks removed (LinkedIn and X render them literally), bullets as plain hyphens, and the
release time corrected to 12:00 UTC (noon) per the user. Files sent to Buffer: `social/thread/1-7.txt` (X), `social/linkedin.txt` (LinkedIn).

---

## X: thread (7 posts, one section per post)

**1/**
MOI Protocol Release: v0.13.0

The moipod v0.13.0 network update is scheduled for today at 12:00 AM UTC. This release includes breaking changes. Please review the changes below before you upgrade. <!-- slop-lint:ignore -->

**2/**
Fee Payer

An interaction can now specify a separate fee payer. The fee payer also signs the interaction and pays the fuel cost instead of the sender.

**3/**
KMOI Native Asset

KMOI now uses MASN, a new native asset standard. You cannot mint or burn KMOI, and neither can the asset manager. KMOI also has a new Asset ID.

**4/**
Participant List

The node now reads the sender and fee payer from the interaction header, so do not add them to the participant list. The one exception is a fee payer that also acts as a notary, co-signing for the operations and not only the fuel.

**5/**
ANU

The protocol now prices in ANU, the smallest unit of KMOI. 1 KMOI = 1,000,000,000 anu

The following prices have changed:
- Minimum fuel price: 1 anu → 50 anu
- Storage price per byte: 1 anu → 1,000,000 anu

**6/**
Action required

If your application uses fixed storage funding values, check them. The previous values can be too low after this update. Use the KMOI and anu conversion functions in the SDK. Do not calculate these conversions manually.

**7/**
SDK Versions

The following SDK versions support fee payers and MASN:
- js-moi-sdk: 0.9.0-rc2
- js-polo: 0.1.5

Update your integration before the network moves to moipod v0.13.0.

---

## LinkedIn

MOI Protocol Release: v0.13.0

The moipod v0.13.0 network update is scheduled for today at 12:00 AM UTC. This release includes breaking changes. Please review the changes below before you upgrade. <!-- slop-lint:ignore -->

Fee Payer

An interaction can now specify a separate fee payer. The fee payer also signs the interaction and pays the fuel cost instead of the sender.

KMOI Native Asset

KMOI now uses MASN, a new native asset standard. You cannot mint or burn KMOI, and neither can the asset manager. KMOI also has a new Asset ID.

Participant List

The node now reads the sender and fee payer from the interaction header, so do not add them to the participant list. The one exception is a fee payer that also acts as a notary, co-signing for the operations and not only the fuel.

ANU

The protocol now prices in ANU, the smallest unit of KMOI. 1 KMOI = 1,000,000,000 anu

The following prices have changed:
- Minimum fuel price: 1 anu → 50 anu
- Storage price per byte: 1 anu → 1,000,000 anu

Action required

If your application uses fixed storage funding values, check them. The previous values can be too low after this update. Use the KMOI and anu conversion functions in the SDK. Do not calculate these conversions manually.

SDK Versions

The following SDK versions support fee payers and MASN:
- js-moi-sdk: 0.9.0-rc2
- js-polo: 0.1.5

Update your integration before the network moves to moipod v0.13.0.

---

## Notes

- Text is the release note as sent, unedited. Rewritten drafts (brand-voice and
  linkedin-post-writer versions) were dropped at the user's request.
- Scheduled through `scripts/buffer.mjs` to `MOI_Tech` (X) and `moi-tech` (LinkedIn).
