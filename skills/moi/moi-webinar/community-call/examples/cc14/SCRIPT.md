# MOI Community Call 14, The Campfire Chat: speaking script, slides 2 to 4

This file covers only the slides the previous operator presented: protocol (slides 2 and 3) and DevRel (slide 4). The other slides were not scripted by him, and their notes in the deck are first-draft text that appears to have had no voice pass.

How to read this file

- Each block is the exact text for one slide. The deck's NOTES array holds the same text, word for word.
- A line in square brackets is a cue. Do not read it out unless the host asks the question it names.
- PRESS NEXT means advance the deck, then start the block below it.
- The same text is in the presenter window. Press P on the deck.

---

==============================================================
## PRESS NEXT --> SLIDE 2 · The September release
==============================================================

moipod v0.13.0 shipped on the eleventh of September, and it is on devnet now. One new thing, and two that break.

The new thing is fee delegation. Before this, every interaction paid its own fuel, so an account holding no KMOI could not do anything at all. Now an interaction can name a second account to pay the fuel.

The payer signs every interaction separately, so you are not handing an app an open tab. And it pays fuel, nothing else, so if the user is sending value, they still fund that part themselves.

[If the host asks the zero-KMOI question here: yes. You sign the interaction, the app's account signs alongside it and pays the fuel, so you can turn up with an empty wallet and your first action still goes through. It signs each one separately, so there is no standing allowance, and it only ever covers fuel.]

Now the two that break. KMOI moved to MASN, the standard reserved for the fuel token, so nobody can mint or burn it any more. Not even the asset manager. Only the protocol touches supply. That gives KMOI a new asset id, so pull the constant out of the SDK instead of hardcoding one.

And everything is priced in anu, which is a billionth of a KMOI. Fuel starts at fifty anu and storage costs a million anu a byte. Do not work that out by hand. Use parseKmoi.

---

==============================================================
## PRESS NEXT --> SLIDE 3 · Upgrading from August
==============================================================

If you are still on the August build, upgrade all three pieces together. The node to v0.13.0, js-moi-sdk to 0.9.0-rc2, js-polo to 0.1.5. Upgrade half of it and you get errors that do not point at the cause, because the older SDK knows neither the new KMOI id nor the fee payer.

Then three things in your own code. Search for the old KMOI id and swap in the constant. Any storage amount you wrote as a fixed number is now a millionth of what it should be, so run it through parseKmoi. And fuel below fifty anu gets refused, so the easy fix is to not set a fuel price at all and take the default.

Two more if you assemble interactions by hand. Participant lists should not carry the sender or the fee payer any more, because the node reads both off the interaction. The exception is a fee payer acting as a notary, when it signs the operations. And asset creation got stricter, so a max supply of zero, or more than eighteen decimals, gets rejected.

Anything you hit that is not on this slide, put it in the dev chat and we will add it.

---

==============================================================
## PRESS NEXT --> SLIDE 4 · Meeting agents where they are
==============================================================

Most of what we have been doing on the DevRel side comes down to meeting agents where they already are.

The MCP server is in progress. It lets an agent transact on MOI through MOI Wallet and WalletConnect, so the agent acts, but the server never holds a key. The wallet is still the thing that signs.

We are also wiring MOI into x402, the standard for paying over HTTP 402. An agent hits a resource it has to pay for, pays, and gets it, with nobody sitting in the middle approving it.

And the blog carries on, which matters more than it sounds. What we publish is what the AI engines read back to people, and that is the next slide.

---
