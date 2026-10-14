# Session 8 social posts (cleaned copies)

Thirteen of the 25 files under `social/` in session 8 (local only: the folder is ignored by git and is not in the repo; the originals are not recorded in the handover, and these are the cleaned copies), in the order
a reader meets them: the announcement pair first, then one pair a day, then the day-of posts. Each file is a
post; a `-reply` or `-comment` file carries the event page link. Plain text, no emoji, no em dashes. The two
posts about the Voyage login move and the variant files are left out. `examples/session-8/README.md` lists
the lines in these posts that must not be copied.

## `social/x.txt`

```
On most chains, programs own the data and you ask for access.

MOI flips it. You own the data. Programs ask you.

Friday we grant an AI agent access to one thing, watch it work, then take it back.
```

## `social/x-reply.txt`

```
Access policies: fine-grained control over your own account, checked by the protocol rather than by the program asking.

We write one live and watch a write get refused.

https://luma.com/g0bmqt8p
```

## `social/linkedin.txt`

```
The hardest question in agentic AI is not what an agent can do. It is how you take a permission back.

Revoking an API key breaks everything the agent does, not just the thing you wanted to stop. Rewriting its rules assumes it runs the code you gave it. You quietly accept both, because the alternative is not giving the agent real capability at all.

MOI treats this as an account problem, not a code problem. Your data lives on your account. An access policy on that account says which programs may touch it and who has to be behind the call. Grant it in one interaction. Revoke it in one interaction. The protocol enforces both, so the agent's cooperation is never part of the equation.

Friday at MOI Builders #8, we do the whole loop live: grant an agent access to one thing, watch it work, revoke it, watch it stop. No redeploy, no key rotation, no asking the agent to behave.

Policies cover storage today, with the rest of the account to follow.
```

## `social/linkedin-comment.txt`

```
Friday 4 September, 4pm IST. Free, live, and the code runs on devnet with one funded wallet.

https://luma.com/g0bmqt8p
```

## `social/tue-x.txt`

```
An AI agent tried to write to an account it didn't own.

The chain's reply, verbatim:

builtin.AccessError: actor is not allowed to write into other actor's storage

Mined, charged, refused. Friday we show the whole loop live.

https://luma.com/g0bmqt8p
```

## `social/thu-x.txt`

```
Tomorrow: same call, same key, three times.

Refused. Allowed. Refused.

The only thing that changes is one record on the account being written to.

4pm IST, live on devnet. Last call:

https://luma.com/g0bmqt8p
```

## `social/fri-linkedin-t5h.txt`

```
Everyone reaches for one of two answers to where an AI agent's authority should live.

Put it in the app? Your preferences end up scattered, one copy per service, and you re-teach them to every new one.

Hand it to the agent? The agent becomes the central point. Move to a different agent and you start from zero.

Both fail for the same reason. The thing that is yours is stored inside something that is not.

So MOI puts your data on your account. Not inside the program, not inside the agent.

That creates a capability no other chain has. On Ethereum your account holds a balance and a nonce, and no storage a contract can write into. On MOI, a program that updates your data is writing to an account it does not own.

Which leaves you owing an answer to a question nobody else has to ask. Who is allowed to write to my account, and for what?

An access policy is that answer. One record, on your account, naming which program may write and who has to be behind the call.

We run it live today, 4pm IST, on devnet.

Where does your agent's authority live right now? In the app, in the agent, or somewhere else?

https://luma.com/g0bmqt8p
```

## `social/fri-x.txt`

```
Your AI agent holds its own key.

Any limit you write into a program is a limit it can decline to look up.

You're not constraining it. You're asking it nicely.

Participant-centric means the rule lives on your account, not in the program.

Access policies. Today, 4pm IST.
```

## `social/fri-x-reply.txt`

```
Live on devnet, and you can run all of it yourself afterwards with one wallet.

https://luma.com/g0bmqt8p
```

## `social/fri-linkedin-t1h.txt`

```
One hour out, and here is the whole session in three attempts.

An AI agent calls a program that writes to an account it does not own. Same call, same key, three times.

First it is refused by the network.

Then the owner grants an access policy, and the identical call lands.

Then the owner revokes it, and it is refused again.

Nothing about the agent changes in between. Not its key, not a line of its code. The only thing that moves is one record on the account being written to.

If you are building agents that touch anything valuable, that is the thing to look at. Not what the agent promises to do. What the account it writes to will actually permit.

No redeploy, no key rotation, no asking the agent to behave.

MOI Builders #8. 4pm IST, live on devnet.
```

## `social/fri-x-t30.txt`

```
WE'RE LIVE IN 30.

https://luma.com/g0bmqt8p
```

## `social/fri-x-live.txt`

```
We're live.

Same call, same key, three times. Refused, allowed, refused.

Nothing about the agent changes in between.

https://luma.com/g0bmqt8p
```

## `social/fri-linkedin-live.txt`

```
We are live.

MOI Builders #8, access policies, running on devnet right now.

An agent writing to an account it does not own. Refused, then allowed, then refused again, with nothing about the agent changing in between.

Come and break it with us. If you catch this late, the recording and the full repo go out afterwards, and one funded devnet wallet runs the entire thing yourself.
```
