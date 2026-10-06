<!-- TEMPLATE NOTES (delete this comment when the file is filled in)
Derived from the session 8 student README. Reader: a student who clones the repo and runs the demo
after the session. This file is tracked, so a push publishes it. The repo is public.
Rules: no reviewer names, no mention of any cancelled plan, no claim the screen did not show,
every limit stated plainly. Fill every FILL marker. Replace each command with the one that really works.
-->
# {{TITLE}}

FILL Three or four sentences. Open with the thing that happens (session 8 opened with one call made three times: refused, allowed, refused), then say what changes between the runs and what does not.

```bash
cd {{FOLDER}}             # from the root of the cloned repo
npm install
cp .env.example .env      # add your recovery phrase yourself, in the file, never in a chat
npm run preflight         # reads only: does this devnet support what the demo needs?
FILL one setup command per line, each with a short comment
npm run demo
```

**FILL what to fund, and how much.** Say which account needs the faucet (https://voyage.moi.technology), the amount that works, and the error you get below it. Quote only numbers you measured and dated. Session 8 found that a policy write failed with `insufficient funds` at about 10,000 KMOI and worked at about 109,000, and the exact threshold was never measured.

Slow it down for narration:

```bash
DEMO_PAUSE_MS=1500 npm run demo
```

What the first beat prints, and the line worth having on the screen:

```
FILL the real output line, copied from a run
```

FILL One sentence on where that line comes from (the chain, not the script).

## Why this session exists

FILL The question the previous session left open and the answer this one gives. State the mechanism in plain words, no label first. Name only public things.

## What the demo actually shows

FILL One paragraph on the setup.

| Beat | What happens | Result |
|---|---|---|
| 1 | FILL | FILL |
| 2 | FILL | FILL |
| 3 | FILL | FILL |

FILL One paragraph on the shape people expect wrongly (session 8: a refusal is a mined, charged receipt with a non-zero status, not a thrown error).

## The core snippet

```ts
FILL at most 15 lines, one comment per line saying which question it answers
```

FILL Three or four things worth knowing about the snippet, each one sentence.

## What is not here

FILL What the type system or docs declare that is not live, and what was left off on purpose and why. Say it here as plainly as it was said in the session.

## Files

```
FILL path/to/file     one-line role
```
