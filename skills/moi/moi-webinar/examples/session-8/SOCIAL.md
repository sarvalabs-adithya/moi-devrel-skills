# Social pack - MOI Builders #8

Replace `LUMA_URL` before scheduling. Two variants of the X post: pick one. <!-- slop-lint:ignore -->

No emoji, per brand voice.

---

## X - single post

Give an AI agent a wallet and you hit a problem more code cannot fix.

The agent holds its own key. Any limit you write into a contract is one it can skip.

Friday we put the rule somewhere it cannot reach: your own account, checked by the protocol.

LUMA_URL <!-- slop-lint:ignore -->

---

## X - thread (5 posts)

**1/**
Give an AI agent a wallet and you hit a problem you cannot solve with more code.

It holds its own key. Every limit you write into a contract is one it can decide to skip.

Friday we show where the rule actually has to live.

**2/**
The obvious fix is a budget contract the agent spends through.

That is a gate with no fence. On MOI assets are native, so the agent can move them directly and never call your contract at all.

**3/**
So you go stricter: lock the asset up so only your contract can move it.

Except the agent created that lockup. It can release it.

The rule and the power to delete the rule sit behind the same signature.

**4/**
An access policy sits on YOUR account instead. The protocol reads it before any write lands.

The agent is not asked, cannot decline, cannot reach it.

Same call, three times, same key: refused, allowed, refused.

**5/**
Nothing about the agent changes in between. Not its key, not its code, not one line of the program. <!-- slop-lint:ignore -->

One record moves, on somebody else's account.

Friday, free, live on devnet:
LUMA_URL <!-- slop-lint:ignore -->

---

## LinkedIn

Most teams building AI agents set spending limits in a config file. <!-- slop-lint:ignore -->

That works right up until it matters. The agent holds its own signing key, which means every limit written in your code is a limit it can choose to skip. You are not constraining the agent. You are asking it nicely.

The obvious fix is to put the budget in a smart contract and route the agent through it. On MOI that gives you a gate with no fence: assets are native to the protocol, so the agent can move them directly and never call your contract.

Go stricter and lock the asset up so only your contract can touch it, and you run into the version of this problem that is genuinely hard to argue with. The agent created that lockup. It can release it. The rule and the power to delete the rule sit behind the same signature.

This Friday at MOI Builders #8, we show where the rule actually has to live: on your own account, read by the protocol before any write is allowed to land.

We run the same call three times from the same key. Refused. Then allowed. Then refused again. Nothing about the agent changes in between. Not its key, not its code, not one line of the program. The only thing that moves is a single record on somebody else's account. <!-- slop-lint:ignore -->

Worth saying up front: access policies cover storage today. Assets and logic are declared in the type system but not yet live. You will see the mechanism working on the resource where it works, and hear where it goes next. We would rather tell you that now than have you find out afterwards.

Free, live, and the code runs on devnet with one funded wallet.

LUMA_URL <!-- slop-lint:ignore -->

---

## Notes

- The LinkedIn post carries the storage caveat. It costs a little polish and buys the room's trust. Do not cut it.
- The thread's post 3 is the strongest single idea in the session. If you only post one thing, post that.
- Both link to the Luma, not the blog. Publish the blog after the session and repost then.
