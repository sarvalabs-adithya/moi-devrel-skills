# Release slide checks

How to check the protocol slides against the release note and source before a call. The general method for any public claim belongs to `moi-devrel/claim-check`. This file holds what is specific to a release slide. Facts are as of 2026-10-02. Back to `../GUIDE.md`.

## Sources, in order of authority
1. Tagged source: go-moi at the release tag, go-pisa, the published js-moi-sdk and js-polo packages.
2. The protocol team's release note.
3. The release post in `sarvalabs/MOI-Website` (`blog/src/content/posts/`). It was claim-checked, but it is a derived text.
4. docs.moi.technology. The weakest source: its op-code numbers were swapped in August 2026.

Source access: go-moi and go-pisa are private. ASK: Gokul for read access. Until you have it, mark post-only claims UNVERIFIABLE, never VERIFIED.

A release note is a lead. It is quoted verbatim where a slide quotes it. The slide never says more than the source says.

## The copy of the note in this library
`../examples/cc14/sources/RELEASE-NOTE.md` is the v0.13.0 note, a restructured copy of what the protocol team sent, not the original text (its header says so). It was copied from the previous operator's working files on 2026-10-02, where the original file was never committed. The note first pasted on 2026-09-10 had an em dash in its title, a sentence "We are rolling out moipod v0.13.0 with several important updates" and separate sentences about the sender not paying. The file holds the restructured sentences from the X thread. The original text is not in this library.
- For the next release: ASK: Rahul or Gokul for the original text and where it is posted. Save it unedited and say so in its header only if it is.
- The v0.13.0 original and the release pack (`protocol-release-0.13.0/`) were never pushed to the public repo and are not recorded in this library (the previous DevRel's notes). ASK: Rahul or Gokul for the original note.

## Steps
1. Get the note as sent. Save it unedited next to the deck.
2. Split every release slide and every release sentence of the script into one claim per line.
3. For each claim, find the line in the note. If it is not there, find it in the post. If it is only in the post, trace it to source before the call, or cut it.
4. Record a verdict per claim: VERIFIED, SCOPED (true only with a limit the slide must state), OVERSTATED, UNVERIFIABLE, FALSE or CUT. Keep the table next to the deck.
5. Audit every package, not only the headline. Non-headline packages, point releases and release candidates are the items that fall off decks. Compare each deck line with the package's GitHub release notes and the source.
6. Check status words: shipped, live, available. See "Live" below.
7. Copy ids, versions and amounts character for character from the note.
8. The operator decides. Show the whole table.

## Live
- A feature in the tip of `develop` is not live until the network redeploys. On 2026-09-10 the live devnet still returned `payer` on interactions and `net.Version` of `0.12.0`, so the fee payer field was inert there. The word `fee_payer` on the wire means the new build.
- `moi-devrel/references/devnet.md` records the upgrade as announced for 00:00 UTC on 11 September 2026, not confirmed to the minute, and that `net.Version` read 0.13.0 on 2026-10-02. No read from the day of CC14 is on record, and no check of the wire field name after the 11 September wipe is on record. On 14 October 2026 `net.Version` answered 0.13.0 while `net.NetworkID` still returned method-not-found (-32601), so the live-build check stays open. ASK: Gokul.
- Before saying "live on devnet" in a deck, read the live node: its version and a recent interaction's field names. `moi-devrel/references/devnet.md` holds the endpoint and how to read it. If you cannot check, ask the protocol team and write what they confirm.
- The 2026-09-25 instruction fixed the wording ("went live on devnet", with the network called devnet). It did not verify the claim.

## Write the time as a date and 00:00 UTC
The note says "scheduled for today at 12:00 AM UTC", with no date. That was read as midday and two scheduled posts were wrong and had to be deleted by hand. A correction reply for X was drafted: "the moipod v0.13.0 network update is scheduled for 00:00 UTC on 11 September". The date and the 00:00 form exist in that reply, not in the note. Write "00:00 UTC on 11 September" and never "today" or "12:00 AM". <!-- slop-lint:ignore -->

## Release candidates
Never present a release candidate as shipped. At CC13 a deck line said `js-moi-agent-registry v0.3.0-rc1` shipped, and it was an RC pinned to an exact SDK peer. Keep an `-rc` suffix as the note writes it, as CC14 does for `js-moi-sdk` 0.9.0-rc2. Do not add a sentence explaining what an RC is.

## Wording that was corrected in this release
| Do not write | Why | Write |
|---|---|---|
| "Every action on MOI costs fuel", "every interaction costs fuel" | Removed from the post as an exaggeration (2026-09-11) | Say what the change does, for example "an interaction can now name another account to pay its fuel" | <!-- slop-lint:ignore -->
| "the token", "the fee", "MOI's own token" | Strongest complaints of the review | "KMOI", and on first use "the native token of the MOI network, like ETH on Ethereum" |
| "fixed supply" | Wrong word | "capped supply" | <!-- slop-lint:ignore -->
| "the app pays for you" with no qualifier | Fee delegation covers fuel only and the sender still funds any value sent | "pays the fuel" |
| A manual anu conversion in a slide or script | The note says "Do not calculate these conversions manually" | "Use `parseKmoi`", which the post names |

## Worked table: CC14 slides 2 and 3
Each line is compared with the note copy in `../examples/cc14/sources/RELEASE-NOTE.md` and with the release post. Verdicts are the library author's reading on 2026-10-02 and need the protocol team's confirmation where marked.

| Slide line | In the note | In the post | Verdict |
|---|---|---|---|
| moipod v0.13.0, 11 September | "scheduled for today at 12:00 AM UTC", no date | Yes: "live ... since 11 September 2026" | VERIFIED for the version. The moment 00:00 UTC on 11 September comes from the correction reply in the release pack, not from the note. ASK: Gokul to confirm it in writing | <!-- slop-lint:ignore -->
| "live on devnet" | No | "live on Voyage devnet since 11 September" (the post's words; say "devnet") | SCOPED: supported by `devnet.md` as of 2026-10-02. Not read on the call day. Read the node again before every call | <!-- slop-lint:ignore -->
| An interaction can name another account to pay its fuel; the payer signs | Yes | Yes | VERIFIED |
| The payer covers fuel only; no open tab | "pays the fuel cost" | Yes, with a FAQ that cites the node code | VERIFIED on the post |
| "Your app holds one funded account and names it as payer" | No | Implied: an app can cover that cost | Framing. Keep it as an example only |
| "So a new user, or an agent, can start with zero KMOI" | No | "a new user can start without holding KMOI for fuel", and "an agent no longer needs to hold KMOI for its fuel" | SCOPED: the post covers fuel only. "Start with zero KMOI" goes further than fuel, so say "does not need KMOI for fuel" |
| "KMOI moved to MASN, the standard reserved for the fuel token" | "a new native asset standard" | "made for KMOI alone" | UNVERIFIABLE: "reserved for the fuel token" is in neither text. The post says "made for KMOI alone". ASK: Gokul whether any asset besides KMOI can use MASN |
| Nobody can mint or burn it, not even the asset manager | Yes | Yes | VERIFIED |
| Script: "every interaction paid its own fuel, so an account holding no KMOI could not do anything at all" | No | "the account that sent an interaction paid its fuel from its own KMOI" | OVERSTATED: the same family of universal that was removed from the post. ASK: Gokul whether any interaction costs no fuel |
| 1 KMOI is a billion anu; fuel from 50 anu; storage a million anu a byte | Yes | Yes | VERIFIED |
| Convert with `parseKmoi` | "Use the KMOI and anu conversion functions in the SDK" | Names `parseKmoi` and `formatKmoi` | VERIFIED |
| js-moi-sdk 0.9.0-rc2, js-polo 0.1.5 | Yes | Yes | VERIFIED |
| Script: older SDK gives "errors that do not point at the cause" | No | "do not know the new KMOI id or the fee payer" | UNVERIFIABLE: the error behaviour is stated nowhere |
| Search for old id `0x108000004cd973c4` | No | Yes, item 1 | Post only. Trace to source before use |
| Max supply 0 or over 18 decimals is refused | No | Yes, item 5 | Post only. Trace to source before use |
| Participant lists drop sender and fee payer; notary exception | Yes | Yes | VERIFIED |
| Storage amounts are a millionth; fuel below 50 anu refused; leave `fuel_price` unset | "previous values can be too low" | Yes | VERIFIED on the post |

## Not yet known
- How the protocol team delivers the note and who is the named contact besides Gokul. ASK: Rahul.
- Whether the answer to "does a brand-new participant with zero KMOI need anything before its first interaction" is on record. It is not. ASK: Gokul before the host's question comes up again.
- Whether devnet was on v0.13.0 on the day of CC14 (2026-09-25, inferred). The wipe announced for 11 September suggests it was, and no read from that day is on record. ASK: Gokul.
