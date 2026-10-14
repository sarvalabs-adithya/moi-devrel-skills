# Buffer: how the scheduling tool is driven

Facts are as of 2026-10-02. Sources: `scripts/lib/senders.js`, `scripts/lib/social.js` and `.github/workflows/distribute.yml` in `sarvalabs/MOI-Website` on `main`; `scripts/buffer.mjs` as it now ships in this library (`moi-webinar/scripts/buffer.mjs`), read in full; commit messages. Names only: no key, token or channel id appears here. Back to `../SKILL.md`.

## What Buffer is here, and why
Buffer holds the connections to MOI's X account ("MOI_Tech") and LinkedIn company page ("moi-tech"). A draft or a scheduled post sits on Buffer's servers until it is published. X's own drafts screen stays empty, and that is normal. Check `publish.buffer.com`, the channel, Drafts.
Why Buffer and not the platform APIs, from the message of commit `cc6ddf1` (2026-08-24): X ended its free tier in February and bills per post containing a link, which every post here has. LinkedIn company-page posting needs approval under its Marketing Developer Platform programme, which runs for months. Buffer's plan carries approved integrations for both. X has no per-person roles, so without Buffer "give someone access" means sharing the account password. Plan limits and prices are not recorded. ASK: Rahul which plan the organisation is on.
Only a Buffer organisation owner can create an API key. Chandra owns the organisation (`project-handover-docs/BLOG.md`).

## Two tools, two key names
The two do not share a variable.
| | Website pipeline | `scripts/buffer.mjs` |
|---|---|---|
| Key name | `BUFFER_ACCESS_TOKEN` | `BUFFER_API_KEY` |
| Also needs | `BUFFER_CHANNEL_X`, `BUFFER_CHANNEL_LINKEDIN` (Buffer channel ids) | A channel id passed as `--channel` |
| Where the key lives | A GitHub Actions secret on `sarvalabs/MOI-Website`. It cannot be read back | `.env` at `$SKILLS/moi-webinar/.env` (the folder above `scripts/`), or the process environment |
| Used by | The "Distribute a post" workflow, through `scripts/lib/senders.js` | The script, run by hand |
| Channel ids from | `npm run buffer:channels` | `node "$SKILLS/moi-webinar/scripts/buffer.mjs" channels` |
| What it does with a post | Always a draft | A scheduled post publishes by itself unless you pass `--draft` |
| Where the code is | `main` of `sarvalabs/MOI-Website` | This library: `$SKILLS/moi-webinar/scripts/buffer.mjs` |
Rules for both: never open an `.env`, never paste a key into chat. A Buffer key was pasted in chat on 2026-08-31 and revoked. Where a command needs the key, hand it over without echo (zsh): `read -rs "T?Buffer key: " && echo && BUFFER_API_KEY="$T" <command>; unset T`. `moi-devrel/references/consent-and-identity.md` section 4 has the details, and `moi-devrel/references/keys-and-access.md` the owners and status.

## The website pipeline's draft guarantee
`sendBuffer` builds the payload in one place: `saveToDraft: true`, `mode: 'addToQueue'`, `schedulingType: 'automatic'`. Before the request it throws "Refusing to send: Buffer posts must be drafts." if either is wrong. The draft state travels with the call, not with a Buffer setting, because one click in Buffer's settings would otherwise turn queued posts into scheduled ones (`debe765`, #47). `shareNow` and `shareNext` are not reachable from the code. An environment flag, `BUFFER_MODE=now`, existed and was deleted in `67c1e33` (#48): a guarantee that depends on a variable nobody sets is not one. If asked to "just publish this once", the answer is a pull request, not a flag. Do not add an environment variable, a workflow input or a `--publish` argument.

## What `scripts/buffer.mjs` does
The script is not in the website repo. It ships in this library at `$SKILLS/moi-webinar/scripts/buffer.mjs`. Call it by that full path from any folder: a relative `scripts/buffer.mjs` is not found from inside a session folder (the failure on 2026-08-31). Node 24 was used. It has no dependency.
```
B="$SKILLS/moi-webinar/scripts/buffer.mjs"
node "$B" channels
node "$B" post --file <path> --channel <id> [--at <iso8601>] [--draft] [--confirm]
node "$B" post --text "..." --channel <id> [--at <iso8601>] [--draft] [--confirm]
node "$B" post --thread-dir <dir> --channel <id> ...
node "$B" post ... --follow <file>
```
- `channels` prints service, name and id for the channels of the first organisation on the account.
- Without `--confirm` a run prints the channel, the `fate` line, the character count and the text, then stops. The `fate` line reads `DRAFT`, `PUBLISHES AUTOMATICALLY at <UTC string>, nobody reviews it` or `PUBLISHES AUTOMATICALLY in the next queue slot`.
- `--draft` saves a draft and ignores `--at`. `--at` schedules with `customScheduled`.
- `--follow` attaches a second text file: the second post of an X thread, or the first comment on LinkedIn. Other services refuse it.
- `--thread-dir` posts an X thread from files named `1.txt`, `2.txt` and so on, sorted by number. The first is the root post. It works for X only and cannot be combined with `--follow`. It prints `thread of N posts` with the length of each.
- The key is read from `.env` at `$SKILLS/moi-webinar/.env`. The last occurrence wins, so appending a rotated key works, and an already-set process variable beats the file. With no key the script exits 1 before doing anything.

## What it does not do
| Not done | What that means |
|---|---|
| No length check | It prints characters and never stops at 280. The website pipeline blocks over-length copy |
| No placeholder check | Two files of the v0.13.0 pack ended with `RELEASE_URL` and the script would not have said so <!-- slop-lint:ignore --> |
| No time zone check | `--at "2026-09-10T08:45:00"` is read in the machine's zone. End every value in `Z` and read the printed UTC string before `--confirm` |
| No list, edit or delete | A wrong post is deleted by hand in the Buffer app. It was done twice on 2026-09-10 |
| No images | Posts carry no media. Add one in Buffer |
| No Discord or Telegram | Those go through the website pipeline |
| First organisation only | An account with several organisations is not handled |
| No UTM tags and no record | It tags nothing, and keeps no list of what was sent. A folder of `.txt` files is not a record |
| A dry run is not offline | It still reads the key and asks Buffer for the channel list to name the channel. It writes nothing, although it prints "Dry run. Nothing was posted". Running `scripts/buffer.mjs` in any form, a dry run included (it sends the key to Buffer), is a GATE in every skill that mentions it: the operator runs it or says yes first |
`--thread-dir` is in the copy in this library and in its usage text (`node "$B" --help` prints it and exits 0).

## The run, when a scheduled post is the right tool
For a release thread (`release-pack/GUIDE.md`) or a webinar day-of post (`moi-webinar`), not for announcing a blog post.
1. `B="$SKILLS/moi-webinar/scripts/buffer.mjs"; node "$B" channels` (a gate, see above). Pick the id. Never write ids into notes.
2. Write the text to a file. Check it by hand: no placeholder, no em dash, at most 280 characters per X post with each URL counted as 23, plain text.
3. Convert the time: `bash "$SKILLS/moi-devrel/scripts/time-table.sh" "<YYYY-MM-DD HH:MM>" <area/city>`. Use the `ISO UTC` line for `--at`.
4. Dry run first, with `--draft` if you can. Read the `fate` line aloud. A scheduled post publishes with nobody reviewing it. The midnight incident of 2026-09-10 is in `moi-devrel/references/terminology.md`, table C.
5. `--confirm` needs the operator's yes that names the channel, the text and the UTC time. Use `--draft` unless an exact time matters.
6. Check in Buffer, Drafts or Scheduled. Record what went where in a file.

## The API, in brief
Endpoint `https://api.buffer.com`, GraphQL, header `Authorization: Bearer <key>`. The previous operator read the schema by introspection on 2026-08-25, and commit `67c1e33` says its types were read off introspection. Re-run an introspection query to re-check. The previous operator found that introspection answers with no key or a made-up one, so never use a real key for it (not re-checked on 2026-10-02).
- `organizations` is not a root field. It hangs off `account`. `channels(input:)` takes an `OrganizationId`, a custom scalar, not a string. A channel's `service` is an enum with no `x`: X reports as `twitter`.
- `createPost(input: CreatePostInput!)` needs `channelId`, `mode` and `schedulingType`, with no defaults. `ShareMode` is `addToQueue`, `customScheduled`, `shareNext` or `shareNow`. The result is a union of `PostActionSuccess` and six error types, so decide success by `__typename`.
- Buffer authenticates before it validates. A query with a bad field and a fake token still answers 401, so "I got a 401, so the shape is fine" proves nothing. The first send with a real token is where a wrong shape shows (`67c1e33`). Use introspection to check shapes.
- Buffer's own documentation example used `PostInput`. That type exists, with one field `id`, so the mistake parses and fails only on type checking against `CreatePostInput!`. Read the schema, not the example.

## Setup for the website pipeline
Each step that changes a shared system is a gate.
1. Connect the X account and the LinkedIn company page as channels in Buffer (the owner does this).
2. The owner creates an API key. A member account cannot.
3. Print the channel ids, handing the key over without echo as above: `npm run buffer:channels`. It flags a disconnected channel.
4. Set three Actions secrets (the operator types each value at a hidden prompt): `gh secret set BUFFER_ACCESS_TOKEN --repo sarvalabs/MOI-Website`, then `BUFFER_CHANNEL_X`, then `BUFFER_CHANNEL_LINKEDIN`.
5. Dry run first, then the real run (`distribution.md`). A channel with no secret is skipped and named, so channels can be switched on one at a time.

## Troubleshooting
| Symptom | Cause | Fix |
|---|---|---|
| `401` or "Access token is not valid" | Wrong, revoked or non-owner key. A stale duplicate above a new key in `.env` is harmless only because the last one wins | Ask the owner for a new key. A bad token also hides a bad query |
| `Variable '$input' of type 'PostInput!' used in position expecting type 'CreatePostInput!'` | The wrong input type | Use `CreatePostInput!` |
| `Buffer InvalidInputError` | A bad `channelId`, or `mode` or `schedulingType` missing | Re-run the channels command and check the payload |
| `Buffer UnauthorizedError` | The key has no rights on that channel | Use a channel of the organisation that issued the key |
| `Buffer LimitReachedError` | Queue or request budget used up | Wait, or clear the queue |
| `Buffer RestProxyError: <message>` | Buffer's link to the network refused it, often a disconnected channel | The error's `code` and `link` are not shown: `link` is never requested and `code` is dropped. Look at `isDisconnected` in the channels output |
| `Refusing to send: Buffer posts must be drafts.` | A change dropped `saveToDraft` or `mode` | Restore them. Do not weaken the assertion |
| `X: 312/280 characters` | Over length | Shorten it. The count already treats each URL as 23 |

## Not yet known
- Which plan the Buffer organisation is on. Chandra owns it. ASK: Rahul for the plan.
- As of October 2026 `BUFFER_ACCESS_TOKEN` and the two channel ids are set on `sarvalabs/MOI-Website` (`project-handover-docs/BLOG.md`). Confirm the names with `gh secret list --repo sarvalabs/MOI-Website`. Values are readable by nobody.
- `BUFFER_API_KEY` comes from Chandra: only a Buffer organisation owner can create one. Check with marketing (Vardan) before any run, because they own the company channels.
