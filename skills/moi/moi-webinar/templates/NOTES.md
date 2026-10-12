<!-- TEMPLATE NOTES (delete this comment when the file is filled in)
Derived from the session 8 build notes. This is the running build log: what was proven on devnet and
how. It is tracked in the session 8 branch, so a push publishes it: no reviewer names, no secrets.
Keep every interaction hash IN FULL (a truncated hash cannot be looked up), with its date and the
node version. A devnet reset wipes them, so the date is what makes an old hash meaningful.
-->
# Session {{NUMBER}}: build notes

## Why the design changed (delete if it did not)

FILL What the first design was, what was found wrong with it, and why it was dropped. Keep the old build on disk and say where. Internal only: none of this goes in public copy.

## Verified live

| Check | Result | Date | Node version (`net.Version`) |
|---|---|---|---|
| FILL the method or feature exists, proved without spending | FILL | FILL | FILL |

## Status: the demo runs end to end, FILL date

| Beat | Result | Interaction hash (full) | Fuel |
|---|---|---|---|
| 1 | FILL | FILL | FILL |

The line worth putting on the screen, copied from a run:

```
FILL
```

## Live findings

One entry per surprise, each with the measurement behind it:

- FILL what happened, what was measured, what to do about it.

Receipt semantics, measured not assumed: FILL which status field is the one that matters.

## The trap this session can fail into, and the guard

FILL How the demo could go green for the wrong reason, the code that prevents it, and the date you forced the guard to fire.

## Claim audit, FILL date

| Claim | Was | Now | Evidence |
|---|---|---|---|
| FILL | doc-derived | receipt-proven | FILL hash or command |

## Decisions worth remembering

- FILL decision, and the reason, in one sentence each.

Source: FILL the docs pull request or page the example comes from (public ones only in public copy).
