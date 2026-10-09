# MOI DevRel skills: design

A library of Claude skills that lets a new developer-relations hire at MOI do the whole job. Built from an investigation of how the work was actually done: ten research notes in `_research/`, covering 111 processes.

This is the private repo `sarvalabs-adithya/moi-devrel-skills`. `skills/` is the part people install; everything else is documentation, provenance or kept for reference.

## Shape

Ten skills. Everything else is a branch: a sub-tool that lives inside the skill that uses it most, with its own `GUIDE.md`, references, scripts and examples.

```
moi-devrel                 THE MAIN ONE. Start here: house rules, who and where, the map of skills.
│   ship                   how any change gets out: identity, commit, pull request, rebase, merge
│   design                 the visual brand: colours, type, logos, mascot
│   claim-check            every public claim against source, before it goes out
│   explain                teach a MOI concept until the person can defend it
│   call-digest            a meeting transcript into decisions and owed work
│   test-round             a structured test pass on a product
│
moi-webinar                one MOI Builders session, topic to write-up
│   deck                   build, check and export any deck
│   community-call         the monthly Campfire Chat
│
moi-blog                   write, publish, announce a post; the newsletter
│   release-pack           a protocol release: the note, the announcements, the release post
│
moi-docs                   write and review docs pages
│   geo                    the search and AI-visibility layer of every site
│
moi-launchpad-ops          run the Agent Launchpad
│   explorer               run the Agent Explorer
│
moi-mcp-ops                run the MCP server
moi-web-products-ops       run the website (chatbot, calendar), the Dataroom and the Points Program
moi-devnet-reset           what to redo in every product after a reset
moi-standards-submission   taking MOI into an external standard
moi-education-programs     MOI Sprint, Forge, awesome-moi; works alongside moi-webinar
```

## Why this shape

- **One main skill.** `moi-devrel` holds what every job needs: the rules, the people, the repo map, the keys by name, and the tools every job uses (ship, design, claim-check). It points to every other skill.
- **Few doors, many rooms.** A newcomer picks from ten skills, not twenty-one. The skill's `SKILL.md` routes to the branch.
- **A branch sits where it is used.** The deck and the community call sit with the webinar because all three are live sessions built the same way. The release pack sits with the blog because it ends in a post.
- **By job, not by repo.** A newcomer asks "how do I run the community call", not "what is in MOI-Webinars".
- **The devnet reset stays a skill of its own.** It is the one recurring event that touches every product at once, and it happened five times between 6 August and 11 September 2026.

The cost of condensing: one description now has to carry the trigger words for a skill and all its branches in 1,024 characters, so routing leans more on each `SKILL.md` than on the descriptions.

## History

| When | What |
|---|---|
| 2026-10-02 | Investigation, then `moi-devrel`, community call, deck, webinar, release pack, blog, claim check |
| 2026-10-03 | Operations, docs, geo, ship, comms, call digest, explain, test round, standards, education, design: 22 skills |
| 2026-10-04 | Whole-library test. Then condensed to 10 skills with 11 branches at the owner's request; the teammate-comms skill was removed, its message checker and drafts kept in `moi-devrel`. Web products was a branch of `moi-devrel` for an hour and went back to being a skill |

## Keys and accounts

Left open on purpose. Every skill names the keys it needs. `moi-devrel/references/keys-and-access.md` is the index and `keys-by-product.md` the per-product list, with where each lives, who grants it, and a status column. It gets settled once, at the end.

## How the library is checked

1. A hostile reviewer tries to refute every statement against the research notes and the repos, and runs every script.
2. A consistency critic reads the skills against each other.
3. A fresh reader is given only the library and a realistic task, and reports every point where it had to guess.
4. A routing test puts plain requests against the descriptions.

Then the gaps are fixed. See `SKILL-STANDARD.md` for the bar.

## What stays out

- Anything personal to one person's way of working (shorthand, model preferences).
- Personal projects.
- Secrets, and any file that quotes one.
- The detail of any open security finding on a live product.

## How the library was checked

1. Every skill: a hostile reviewer tried to refute each statement against `_research/` and the source repos, ran every script on good and bad input, and fixed what it found.
2. The whole library: a consistency critic read all the skills against each other, two simulated new hires ran real tasks using only `skills/`, and a routing test put 30 plain requests against the descriptions.
3. Findings were applied or rejected with a written reason, then every script was run again.

About 530 findings in all, 38 of them marked blocker. Most blockers were scripts that could print a secret-shaped value, examples holding a key-shaped id, and steps with no gate: those are fixed. Six came from a simulated new hire and were questions only a person can answer; they are carried as `ASK:` lines.

## Open before this is shared

- Keys and accounts: `skills/moi-devrel/references/keys-and-access.md` lists every one by name with status TBD.
- The `ASK:` lines. Each names who can answer. Search for `ASK:` to list them.
- Several source files exist only on the previous operator's machine (the community call 14 folder, the release pack, the handover notes). The skills say so wherever they point at one.
- The examples in `moi-claim-check/examples` and `moi-community-call/examples` are cleaned of private paths and names, but nobody has yet said they may be published.
- Seven products carry a one-line note that a security finding is open. The detail is deliberately not in the library.
