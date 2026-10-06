# MOI DevRel skills: design

A library of Claude skills that lets a new developer-relations hire at MOI do the whole job. Built from an investigation of how the work was actually done: ten research notes in `_research/`, covering 111 processes.

This folder is local. It is not a git repo yet. When it becomes one, `skills/` is the part people install.

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
