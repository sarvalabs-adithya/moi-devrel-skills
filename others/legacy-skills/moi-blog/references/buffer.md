# Buffer

X and LinkedIn copy is queued into Buffer as **drafts**. Nothing this repo sends ever reaches a
timeline; a person opens the draft in Buffer, rewrites the hook, and publishes. Discord and
Telegram post immediately: those are different code paths (`sendDiscord` / `sendTelegram` in
`scripts/lib/senders.js`) and are not covered here.

Files that matter:

| Path | What it is |
| --- | --- |
| `scripts/lib/senders.js` (lines 47–117) | `sendBuffer`: the only place a Buffer payload is built |
| `scripts/buffer-channels.js` | One-off script that prints channel IDs; `npm run buffer:channels` |
| `scripts/lib/social.js` (lines 23–58) | `CHANNELS` registry: which env var holds which channel ID, per-channel limits. The two Buffer entries are lines 40–57 (`x` 40–48, `linkedin` 49–57) |
| `.github/workflows/distribute.yml` (lines 59–61) | Where the three secrets are injected |
| `.env.example` (lines 21–27) | Secret names, with the "org owner only" note |
| `social/README.md` (lines 52–71) | The user-facing version of the safety model |

## Why Buffer instead of the platform APIs

Operational notes: learned from vendor pricing and partner-programme pages, not verifiable from
this repo. Treat as context for *why the dependency exists*, not as current pricing.

- **X** ended its free API tier for new developers on 6 Feb 2026 and charges per post, roughly
  $0.015, rising to about $0.20 when the post contains a link. Every post here contains a link.
- **LinkedIn** company-page posting needs the `w_organization_social` scope via the Community
  Management API, under the Marketing Developer Platform partner programme. Approval runs weeks
  to months.
- Buffer's free tier carries **already-approved integrations for both**, so neither of the above
  applies.
- It also solves credentials. X has no per-person roles: without a tool in the middle, "give
  someone access to X" means sharing the account password. Buffer holds the connection; people
  get Buffer logins.

Buffer free tier, as understood at time of setup (operational, unverified from repo):

| Limit | Value |
| --- | --- |
| Channels | 3 |
| Queued posts per channel | 10, rolling |
| API access | included, 1 key |
| Request budget | ~100/day, ~3000/30 days |
| LinkedIn **company pages** | supported on free |
| Who can create an API key | organisation **owner** only |

One of these *is* checkable in the schema: `CreatePostInput.saveToDraft`'s own description says
that when saving as draft, "Posting limits are not checked" and post status becomes `draft`
rather than `buffer`. Drafts therefore do not eat the 10-post queue allowance.

## API shape (verified by introspection, 2026-08-25)

Endpoint `https://api.buffer.com`, header `Authorization: Bearer <BUFFER_ACCESS_TOKEN>`.

**Introspection needs no auth.** This is the whole debugging strategy (see gotcha 1).

```bash
curl -s https://api.buffer.com -H 'Content-Type: application/json' \
  -d '{"query":"{ __type(name:\"CreatePostInput\"){ inputFields { name defaultValue type { kind name ofType { kind name } } } } }"}'
```

### Reading channel IDs

`organizations` is **not** a root Query field. The root fields are exactly:
`account, dailyPostingLimits, channel, channels, aggregatedPostMetrics, post, posts, postTemplate,
postTemplates, ideaGroups, ideas`. Organisations hang off `account`:

```graphql
{ account { organizations { id name } } }

query($id: OrganizationId!) {
  channels(input: { organizationId: $id }) { id name service displayName isDisconnected }
}
```

- `channels(input: ChannelsInput!)`, and `ChannelsInput.organizationId` is `OrganizationId!`:
  a custom scalar ("the MongoDB ObjectId of a Buffer Organization"), **not** `String!`.
- `Channel.id` is `ChannelId!`, also a custom scalar. `Channel.service` is the `Service` **enum**,
  not a string.
- `Service` enum values: `bluesky, facebook, googlebusiness, instagram, linkedin, mastodon,
  pinterest, startPage, threads, tiktok, twitter, youtube`. **There is no `x` member: X reports
  as `twitter`.** `scripts/buffer-channels.js:31-35` maps both `twitter` and `x` to
  `BUFFER_CHANNEL_X`; only the `twitter` branch will ever fire, and that is defensive padding,
  not a live path.

### Creating a post

`createPost(input: CreatePostInput!): PostActionPayload!`

`CreatePostInput` in full:

| Field | Type | Default | Note |
| --- | --- | --- | --- |
| `text` | `String` | none | nullable; for threads must match the first `thread` item |
| `channelId` | `ChannelId!` | none | custom scalar, not `String` |
| `mode` | `ShareMode!` | none | **required, no default** |
| `schedulingType` | `SchedulingType!` | none | **required, no default** |
| `saveToDraft` | `Boolean` | none | the safety switch |
| `needsApproval` | `Boolean!` | `false` | non-null but defaulted, so omittable |
| `assets` | `[AssetInput!]!` | `[]` | non-null but defaulted, so omittable |
| `dueAt` | `DateTime` | none | |
| `tagIds` | `[TagId!]` | none | |
| `draftId` / `ideaId` | `DraftId` / `IdeaId` | none | set when generated from a Draft/Idea |
| `metadata` | `PostInputMetaData` | none | per-network extras |
| `aiAssisted` | `Boolean` | none | |
| `source` | `String` | none | tracking only |

`ShareMode` = `addToQueue | customScheduled | shareNext | shareNow`.
`SchedulingType` = `automatic` (Buffer's workers send it) | `notification` (Buffer reminds a
person to publish by hand).

`PostActionPayload` is a **union** of seven members:

| Member | Fields |
| --- | --- |
| `PostActionSuccess` | `post` (`Post!`) |
| `NotFoundError` | `message` |
| `UnauthorizedError` | `message` |
| `InvalidInputError` | `message` |
| `LimitReachedError` | `message` |
| `UnexpectedError` | `message` |
| `RestProxyError` | `message`, `code`, `link` |

The six error members all implement the `MutationError` interface, so
`... on MutationError { message }` is legal and would compile. The repo enumerates all seven and
switches on `__typename` anyway (`senders.js:62-75`, `112-114`) so that an error type added later
reports itself by name instead of falling through as a silent success.

## The safety model

Read `scripts/lib/senders.js:77-117`. Three things are load-bearing and each was arrived at by
removing something weaker:

**1. `saveToDraft: true` is set on the call, not in Buffer's UI.** Originally the draft state was
left to Buffer's per-channel approval toggle. That put the safeguard somewhere the repo cannot
see, cannot verify, and cannot test. One click in Buffer's settings would have turned every
queued post into a scheduled one, silently. The guarantee now travels with the request.

**2. `shareNow` and `shareNext` are not wired to anything.** They exist in `ShareMode` and are
reachable from the API; they are simply absent from this codebase. An env flag (`BUFFER_MODE=now`)
existed and was deleted in PR #48 (`67c1e33` on `main`; the reasoning is written up in
`2e36557`, on the pre-squash `fix/buffer-mutation-types` branch): a guarantee that holds only
while nobody sets a variable is not a guarantee. Enabling publishing should cost a code change and a PR.

**3. The payload is built in one place and asserted before it leaves:**

```js
if (input.saveToDraft !== true || input.mode !== 'addToQueue') {
  throw new Error('Refusing to send: Buffer posts must be drafts.');
}
```

If you are asked to "just publish directly this once", the answer is a PR, not a flag. Do not
reintroduce an env var, a workflow input, or a `--publish` argument: every one of those was
considered and rejected for the same reason.

## Two debugging lessons

**1. Buffer authenticates before it validates.** Confirmed live:

```
$ curl -s -w '%{http_code}' https://api.buffer.com -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer <FAKE_OR_INVALID_TOKEN>' \
    -d '{"query":"mutation { createPost(input: {thisFieldDoesNotExist: 1}) { __typename } }"}'
{"errors":[{"message":"Access token is not valid","extensions":{"code":"UNAUTHENTICATED"}}]}401
```

A query with a nonexistent input field still returns 401, not a validation error. So **"I tested
with a fake token and got 401, so the query shape is fine" is a false inference**: the 401 is
returned before the document is checked and tells you nothing about shape. This exact mistake
shipped a broken mutation to a production run; it only surfaced on the first run with a real
token. Introspection is the only free way to check shapes, and it works with **no token, or even
a bogus one** (`Authorization: Bearer bogus` on an introspection query returns HTTP 200).

**2. Buffer's own published example used `PostInput`; the real type is `CreatePostInput`.** This
is not a "no such type" error you would catch by eye: `PostInput` **exists** in the schema: it
is an input object with exactly one field, `id`. So `mutation CreatePost($input: PostInput!)`
parses fine and fails only on variable-position type checking against
`createPost(input: CreatePostInput!)`. Read the schema, not the example.

## Where the posts actually go

Buffer holds drafts on **its own servers**. They never touch X or LinkedIn until Buffer publishes
them. Opening X's own drafts or scheduled-posts screen and finding nothing is the expected
outcome, not a bug: there is nothing there to find.

Check `publish.buffer.com` → the channel → **Drafts**.

The last mile is human by design: open the draft, rewrite the hook (the seeded copy comes from the
post's `summary` field and reads generated), then publish or schedule from Buffer.

## Setup checklist

1. In Buffer, connect the X account and the LinkedIn **company page** as channels.
2. As the organisation **owner**, create an API access token (a member account cannot).
3. Get the channel IDs (Buffer surfaces them nowhere in its web UI, so the API is the only route):
   ```bash
   BUFFER_ACCESS_TOKEN=... npm run buffer:channels
   ```
   It prints `service  <id>  <displayName>  -> BUFFER_CHANNEL_X` per channel and flags
   `[disconnected]` ones.
4. Set three repository secrets (not a local `.env`: these are read only by the Distribute
   workflow):

   | Secret | Holds |
   | --- | --- |
   | `BUFFER_ACCESS_TOKEN` | the org owner's API token |
   | `BUFFER_CHANNEL_X` | the `twitter` channel's `id` |
   | `BUFFER_CHANNEL_LINKEDIN` | the `linkedin` channel's `id` |

   ```bash
   gh secret set BUFFER_ACCESS_TOKEN --repo sarvalabs/MOI-Website
   gh secret set BUFFER_CHANNEL_X --repo sarvalabs/MOI-Website
   gh secret set BUFFER_CHANNEL_LINKEDIN --repo sarvalabs/MOI-Website
   ```
5. Dry-run before ever sending. `planFor` (`social.js:158`) reports missing credentials per
   channel rather than failing the run, so a partial setup is a usable state:
   ```bash
   npm run distribute <slug> -- --dry-run --only=x,linkedin
   ```
6. Real send: Actions → **Distribute a post** → slug, channels, `dry_run: false`. The workflow
   defaults `dry_run` to `true`.
7. Confirm in `publish.buffer.com` → channel → Drafts.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `401` / `Access token is not valid` | Token wrong, revoked, or created by a non-owner | Recreate as org owner. Note this 401 also appears for *any* request with a bad token, including ones with broken queries: it proves nothing about the query. |
| `Buffer: Variable '$input' of type 'PostInput!' used in position expecting type 'CreatePostInput!'` | Wrong input type: the shape Buffer's docs example showed | Use `CreatePostInput!`. `PostInput` is a real but unrelated type (`{ id }` only). |
| `Buffer InvalidInputError: ...` | Bad `channelId`, or a required field missing (`mode` and `schedulingType` have no defaults) | Re-run `npm run buffer:channels`; check the payload at `senders.js:81-87`. |
| `Buffer UnauthorizedError: ...` | Token valid but has no rights on that channel/org | Confirm the channel belongs to the org that issued the token. |
| `Buffer LimitReachedError: ...` | Queue or API budget exhausted | Drafts skip posting limits, so this usually means the API request budget. Wait, or clear the queue in Buffer. |
| `✗ LinkedIn  Buffer RestProxyError: <message>` | Buffer's proxy to the network refused | `code` and `link` carry the useful detail and neither reaches the log: `link` is never selected in `CREATE_POST` (`senders.js:72` asks for `message code`), and `code` is selected but dropped by the throw at `senders.js:113`, which prints only `__typename` and `message`. To see them, add `link` to the `RestProxyError` selection and put `result.code` / `result.link` in the error message. Cause is usually a disconnected or re-auth-needed channel; `isDisconnected` in `npm run buffer:channels` shows this. |
| `Refusing to send: Buffer posts must be drafts.` | A refactor changed `saveToDraft` or `mode` | Intentional guard. Restore `saveToDraft: true` / `mode: 'addToQueue'`; do not weaken the assertion. |
| `– X  missing BUFFER_ACCESS_TOKEN, BUFFER_CHANNEL_X` | Secret absent | Expected for a partial setup: the channel is skipped, not failed. Set the secret when ready. |
| `! X  312/280 characters` followed by an em dash and `shorten it` | Over-length copy | Hard stop, never truncated. X counts every URL as 23 chars regardless of length (`measure`, `social.js:148-154`), so the count shown is already URL-adjusted. |
| Nothing in X's drafts/scheduled screen | Not a bug | Drafts live on Buffer's servers. Check `publish.buffer.com` → channel → Drafts. |
| Workflow green but a send failed | `set -o pipefail` missing around the `tee` | Already handled at `distribute.yml:65`; if you edit that step, keep it. |
