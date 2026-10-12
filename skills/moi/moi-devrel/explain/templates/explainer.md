# Explainer: <concept>

Depth: <say it | present it | defend it>. For: <what the operator does next>. Written: <YYYY-MM-DD>. Facts are as of <YYYY-MM-DD>.
Keep this file in a self-ignoring folder (`explain-<slug>/`). It can name private source and people, so it is never committed or pushed without a yes, and nothing in it is pasted into public text without `moi-devrel/claim-check`.
Label each sentence at the end of its line: [doc] a docs page or note says it, [source] read in package source, [receipt] a devnet interaction shows it, [check] I will check.

## Index
1. In one line
2. Why it exists
3. How it works
4. Example with named actors
5. What it does not do
6. Likely questions
7. Sources
8. To check

## 1. In one line
<About 35 words. Yes or no first when it answers a question. Name the subject in the first clause. End with the limit that keeps it true.>

## 2. Why it exists
<Who can now do what, and what changes for them. Before and after, in MOI terms. No term the reader has not met.>

## 3. How it works
1. <One idea. Define each term at first use with the sense of its glossary row in `moi-devrel/references/glossary.md`.>
2. <Name the function, endpoint or RPC when the reader will touch code.>
3. <...>

## 4. Example
Actors: <Name, role>. <Name, role>. Real, read on <date>, or (constructed).
| Step | Who | Call | Effect | Each actor holds after |
|---|---|---|---|---|
| 1 | <actor> | <call> | <effect> | <state> |

## 5. What it does not do
- <The limit, in the same terms as the claim it limits.>
- <The wrong picture people bring (a number from `misconceptions.md`) and the correction.>

## 6. Likely questions
| Question | Answer, yes or no first | Limit | Source | Label |
|---|---|---|---|---|
| <question> | <answer> | <limit> | <page or file, with date> | [doc] |

## 7. Sources
| Source | Read on | What it settled |
|---|---|---|
| <page, file or read-only call> | <YYYY-MM-DD> | <the sentence it supports> |
Not read: <private source, a live read not done, a page that was a stub>.

## 8. To check
| Question | Who settles it | Asked on | Answer |
|---|---|---|---|
| <question> | ASK: <person> | <date, or "not yet sent"> | <answer, or open> |
