# Pull request: title, body, what never goes in, reviewers

Facts are as of 2026-10-03 unless dated. Sources: the PR bodies and corrections recorded in the research notes of 2026-10-02, `moi-blog/references/publishing.md` and its `templates/pr-body.md`, and `moi-devrel/references/consent-and-identity.md`. Back to `../GUIDE.md`.

## 1. Before you open one
1. The operator said to open it. Opening, editing, commenting on, closing or requesting review on a PR each need a yes naming the action (`templates/gate-asks.md`). On audit, inventory and handover work do none of it, and prefer plain `git` to `gh`, so nobody is notified (2026-09-28).
2. The branch passed the local proof and `ship-preflight.sh` has 0 FAIL (`branch-and-commit.md`, section 6).
3. The push happened and `git ls-remote origin refs/heads/<branch>` equals your `HEAD`. On 2026-09-09 the files the previous operator wanted to review were not on the remote after a "push the current branch": name the files and the branch in the ask and check afterwards.
4. The PR targets the right base. Most repos: the default branch. Points Program: `feature/ci-cd`. A voyage-api sync PR: `feat/moi-mcp`. A stacked PR: the branch below it (`stacked-and-batched.md`). `voyage` deploys from `develop`, yet its PR #447 targeted `main` (as of 2026-10-01; merged 14 October 2026, not live): confirm the base before a merge. ASK: Gokul.

## 2. Title and body
- Title: say what changes for the reader, in the form the repo uses. Seen: `blog: MOI September 2026 release (moipod v0.13.0, fee delegation)`; `social: copy for <slug>`; `chore(moi-mcp): sync subtree ...`; `specs: add exact scheme for MOI (moi:*), upfront flow`; `feat(moi): add @x402/moi mechanism package for the exact scheme`. Voyage commits need a conventional type prefix such as `feat:`, `fix:` or `docs:`.
- Body: `cp "$SKILLS/moi-devrel/ship/templates/pr-body.md" "$WORK/pr-body.md"` (`WORK` is set in `../GUIDE.md`, "Before you start"), then fill it in. It follows the shape of the docs PRs of 2026-09 to 2026-10 (what this is, why, what changed, a rebased note, verification, post-merge checks, review notes) and of PR #53 (summary, shape, verification, "before marking ready"). A blog post uses `moi-blog/templates/pr-body.md` instead.
- Verification gives commands run and their results, counts, and public sources by name. Say what you did not verify. The Launchpad's PR bodies read as "what was measured against the real chain, what is NOT verified, test counts".
- Post-merge checks go in the body as a checklist of read-only commands, for example the `curl` lines of `merge-and-deploy.md`.
- Lint it: `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" "$WORK/pr-body.md"` and `bash "$SKILLS/moi-devrel/scripts/secret-scan.sh" "$WORK/pr-body.md"`. The lint flags an AI attribution line inside a code fence too. It also exits 1 on any FILL IN slot still in the body, because only a file under a folder named `templates` is let off. Nothing else reads the body, so an unfilled one would go out as public text. Delete the "Rebased" section if the branch was not rebased. Do not keep `WORK` inside a `templates` folder.
- Draft first. Show the operator the final title, base, head and body in one place, then ask.

## 3. What never goes in
A commit message, a branch name, a PR title and a PR body are all public in a public repo (list in `branch-and-commit.md`, section 4).
| Never | Why, with the date |
|---|---|
| A co-author line or footer naming Claude or any AI, anywhere in the body, code fences included | 2026-06-08 "don't put co-authored by Claude". 2026-10-01 the lines were removed from 130 commits and six PR bodies. PR #53 of `MOI-Website` (merged 2026-09-11, 24 of 24 commits) and its open PRs #52 and #54 still carry the footer in the body and the trailer on their commits (read 2026-10-03). Leave them unless the operator asks (`rewrite-history.md`). Their state may have changed since that read: check with `gh pr view` before relying on it |
| A cancelled plan, an unmerged feature, or how a thing was fixed | 2026-08-31 Luma text and a blog still referred to the cancelled session 8 plan and had to be cleaned. Public content "never mentions cancelled or internal plans" |
| Application content in a protocol docs PR | Rahul's change request on `moidocs` PR #124: no Launchpad docs in the protocol docs (2026-09-22: do not mention the Launchpad in the docs PRs) |
| A private repository's file path or line, or a citation of private source | The protocol repos are private. Private source informs the check and never appears in public text (`moi-devrel/claim-check`). Cite wire-visible behaviour, `js-moi-sdk`, docs, the explorer |
| Names of people or reviewers in the title or body | Ask for review in GitHub's reviewers field, not in prose. The `moi-blog` template carries an "Internal review done" checkbox with no name; the September PR #53 precedent named the reviewer, and public text does not |
| A secret, a recovery phrase, a personal handle or address, a transcript | `consent-and-identity.md`, sections 2 and 4 |
| The weakness behind a security finding | Where `repo-map.md` marks a product, say only: "A security finding is open on this product as of 2026-10-02. Read the product's doc in `project-handover-docs/` before touching its admin." Nothing about the weakness goes in any title, body, commit or comment |
| A claim you did not check | Every public claim is checked against source first (`moi-devrel/claim-check`). Quote a release note verbatim |
| Em dashes, "not this, not that" constructions, vague attribution | House rule 6, enforced by `slop-lint.sh` <!-- slop-lint:ignore --> |
| A hosting provider MOI left, written as where something deploys | `repo-map.md`, "How things deploy" |

## 4. Reviewers
Review is asked through the PR, and a message to a person is drafted by Claude and sent by the operator (`moi-devrel/references/house-style.md`, section 4, for the wording).
| For | Ask | Evidence |
|---|---|---|
| Any public piece, scope, narrative, anything filed upstream | Rahul | The internal gate for upstream filing, agreed 2026-09-09. He reviews decks, posts and docs scope |
| Code, protocol facts, SDK, Voyage and docs PRs | Gokul | Reviews code; the x402 package "goes through Gokul's review" |
| Coco compiler and `coco-docs` | Robert Špendl | Approved coco-docs #12 on 2026-09-29 |
| Workflow files, deploy scripts, anything on a VM | Upendhar (Srikar wrote earlier workflows) | DevOps. Raise it through the operator; do not paste a secret into a message |
| A docs PR of a colleague (fact-check) | The author, through the operator | Abhinav Agarwalla's `moidocs` #120 was fact-checked against source |
Who must approve and who may merge each repo is not recorded. ASK: Rahul. After you fix a change request, reply and re-request review: moidocs #124 met Rahul's request on 2026-10-01 but had not been answered or re-reviewed on 2026-10-02.

### When a reviewer asks for changes
1. Read everything, read-only: `gh pr view <N> --repo <org>/<repo> --comments` for the conversation, `gh api repos/<org>/<repo>/pulls/<N>/comments` for comments pinned to lines, `gh pr diff <N> --repo <org>/<repo>` for the change. On audit work use plain `git` instead (section 1).
2. Number every request in a list for the operator. Change exactly the item pointed at, and nothing around it. One small commit per item. Tweaks across several PRs go on one batch branch (`stacked-and-batched.md`, section 2).
3. Run the local proof again, then push on a yes (`templates/gate-asks.md`). A rebase is a separate decision (`rebase-and-update.md`).
4. Draft one reply per item; the operator sends it, or says yes to Claude posting it. Then ask for a re-review (the `moidocs` #124 case above).
5. Update the PR body if a change made it untrue.

## 5. Open it
```
gh pr create --repo <org>/<repo> --base <base> --head <branch> --title "<title>" --body-file "$WORK/pr-body.md"
```
The operator may open it in the browser instead. `--draft` fits a PR that cannot merge yet (Points draft PR #24 is one). From a fork, the head is `<fork owner>:<branch>`. Then read it back, read-only: `gh pr view <N> --repo <org>/<repo>`. Check base, head, title, files changed and that your account is the author. Write the PR number and URL in the hand-back.
- `MOI-Website` posts a preview comment on the PR (`previews.md`), rewritten on every push. Read the preview before asking for review.
- Cloudflare Pages comments a build on docs PRs and on `MOI-Website` PRs (seen on #53).

## 6. Upstream PRs (x402, CASA)
They follow `moi-standards-submission`; `moi-standards-submission/references/umbrella.md`, "Filing mechanics", holds the fork, identity, signing and push steps, so this file adds none. The filing order is fixed: namespace, then spec, then mechanism. Nothing is filed until Rahul has reviewed (agreed 2026-09-09). The upstream repos ask for an AI-assistance disclosure in the PR description, while house rule 4 bans the "generated with" footer. Do not file until Rahul says how to word the disclosure. ASK: Rahul.

## Not yet known
- Whether any repo has a PR template, required labels, or a required reviewer. None is recorded. ASK: Rahul.
- Who approves a Voyage, SDK or workflow PR besides Gokul and Upendhar. ASK: Gokul.
- How to meet an upstream disclosure rule without a footer. ASK: Rahul.
