# Review a docs pull request

The review method and the comment format. Facts are as of 2026-10-03. No reviewer section exists in the style guide: a "How to check your page" section was removed on 2026-09-22 ("rm step 7 and 10", the previous operator's request), so the passes below are assembled from the guide's rules, its "Update an existing page" list and its "Common mistakes" table. They are derived, not recorded as a procedure. `$SKILLS`, "the operator" and `ASK:` are defined in `moi-devrel/SKILL.md`. Back to `../SKILL.md`.

## What a review is here
Claude reads, checks and drafts. The operator reads the draft once and posts it. Posting, approving, requesting changes, resolving a thread and re-requesting review are all visible to teammates and need the operator's explicit yes (`moi-devrel/references/consent-and-identity.md`). Reading a PR posts nothing: `gh pr view` and `gh pr diff` are fine for a review task. In an audit or handover task keep to plain `git` and skip `gh` (2026-09-28).

The draft lives in a self-ignoring folder, because a review can name private files and people:
`mkdir -p docs-review-<N> && printf '*\n' > docs-review-<N>/.gitignore`, run from the working copy. The `*` hides the folder, itself included, from `git add`. This matters most in `sarvalabs/js-moi-sdk`, which is public.

## Who reviews what (as of 2026-10-02)
| Area | Reviewer seen | Evidence |
|---|---|---|
| Scope and public pieces of moidocs | Rahul | Requested changes on #124 on 2026-09-17 |
| Protocol, SDK, Voyage content | Gokul | Requested on #124, #150, #447; owns Voyage docs; `CODEOWNERS` of js-moi-sdk |
| Coco and cocolang.dev | Robert Špendl | Maintains it; approved #12 on 2026-09-29 after rebasing it to v0.9.2 |
Who may merge, and whether an approval is required by branch protection, is not recorded. ASK: Rahul.

## The passes
| # | Pass | How | Finds |
|---|---|---|---|
| 1 | Read the PR | `gh pr view <N> --repo sarvalabs/<repo> --json title,body,baseRefName,headRefName,files,reviews`; `gh pr diff <N> --repo sarvalabs/<repo> --name-only`. Note the base commit and the head commit you reviewed | The list of changed pages and what the body claims |
| 2 | Scope | Is every change protocol content for this site? No Launchpad or other application docs in moidocs (Rahul, 2026-09-17). Nothing about an unreleased feature or a cancelled plan. No link to a private repo. A page you cannot ground in source does not belong (the kill-switch page was deleted for that, 2026-09-09) | Wrong-audience pages |
| 3 | Mechanics | GATE for the fetch (it downloads and writes to the clone): `git fetch origin pull/<N>/head:pr-<N>`, then `git switch pr-<N>` and `BASE=$(git merge-base origin/<baseRefName> pr-<N>)`, where `baseRefName` is the base branch from pass 1. Then `python3 "$SKILLS/moi-docs/scripts/docs-page-lint.py" --added-lines-since "$BASE" <changed pages>`. Use the merge base, not the tip of the base branch: a PR that is behind it would otherwise show the newer lines of the base branch as its own. Without the flag a page with old content reports its old em dashes and old names | Frontmatter, titles, names, links, stubs, placeholders |
| 4 | The preview | Open the Cloudflare comment's link. Click every changed page, the sidebar entry and each new link. Look at the page where the browser tab shows the title | Rendering, order, dead links, two titles |
| 5 | The checklist | The ten items below, read on the diff | What the lint cannot see |
| 6 | Facts | Every changed technical claim against source. Small PR: spot-check each with `moi-devrel/claim-check`. Technical PR: `fact-check-a-pr.md` | Wrong statements |
| 7 | Side effects | Generated files in the diff (not allowed on the Docusaurus sites; expected on js-moi-sdk). A change to config, `robots.txt`, `_headers` or `.well-known`: it needs the `geo` branch (`geo/GUIDE.md`), and `curl -A "GPTBot/1.0" -I https://<domain>/` must still answer 200 after deploy. A moved or renamed page: is there a redirect? (`write-docusaurus.md`) | Broken old links, blocked crawlers |
| 8 | Hygiene | PR body still true (`pr-upkeep.md`). Commits carry the work identity and no AI co-author line. If the branch was rebased, the pages in the diff match `main` apart from the intended change | Stale body, lost content |
| 9 | Reconcile | Count your findings in the summary, the table and the list. They must agree before anything is shown | The "27 errors versus 26 versus 25" defect |

## The checklist (pass 5)
1. Frontmatter starts on line 1; `title` short and without a version; `description` present, 140 to 160 characters (130 to 170 tolerated), quoted if it holds `: `; `sidebar_position` set; `image` right on moidocs; stub marks present or removed correctly.
2. The opening paragraph defines the thing and stands alone.
3. One main title. No `# Title` next to a `FaqSchema` or `HowToSchema` call. A reworded heading carries `{#old-anchor}`. If an anchor changed on purpose, every inbound link was updated (`grep -rn "old-anchor" .` and a search of the `sarvalabs` org).
4. Names follow the table. A quick check: `grep -rnE "Moipod|MoiWallet|Moi Wallet|JS-MOI-SDK|CocoLang|CoCo|SarvaLabs" docs`. <!-- slop-lint: ignore -->
5. Internal links start with `/` and match the site's form.
6. A new API reference or skill package has its `.well-known` entry.
7. Generated files are not edited and not committed (js-moi-sdk excepted).
8. Every changed claim was checked against source and the PR says how.
9. Code samples run as written, or say they are simulated.
10. Nothing in the diff is a secret, a recovery phrase or a personal address.

## Severity
- **Breaking**: a reader acts on a wrong statement, a sample fails, the build breaks, a page that must not be public is public, or a stub or secret ships.
- **Minor**: wording, length, naming, order, a missing nice-to-have.
Put breaking items first. In the recorded case (#120) the first batch sent to the author was the breaking items and the rest followed after review.

## The comment format
One finding, four parts, in the previous operator's format of 2026-08-21: "Issue N: what the issue is, why it is an issue, where the issue is, suggested fix." Add a severity word. `templates/review-comments.md` holds a full set: the summary comment, a style finding, a fact finding, a question, an anchor change and a re-review note. Rules:
- Number the issues once and keep the numbers stable between drafts, so the operator can answer by number.
- Give the exact replacement text where you can. A reviewer who says "make this clearer" has not helped.
- Evidence is public wherever the repo is public. In the #120 check the evidence was private source (go-moi at v0.12.0); whether any posted comment named a private file is not recorded, and whether one may on a private repo is not settled. ASK: Rahul. Page text never does.
- Say what you did not check ("private source not available", "images not opened").
- A review reports checks that were done. A planned check is labelled as one.

## Verdicts
- Request changes while any breaking item stands. The Drive standard says not to approve a PR that fails any item of its reviewer checklist (secondhand: the Drive document was not read, ASK: Adithya for a copy).
- Approve only after the lint shows no error on added lines, the preview was opened, and the facts are checked or the gaps are named in the comment.
- After the author fixes, re-read the fix commit against the numbered issues. Draft the reply for the operator to post and the request for re-review. On 2026-10-02 Rahul's change request on #124 was met by commit `75f608b` and nobody had answered him.

## What reviewers have asked before
| Date | Who | Asked | Result |
|---|---|---|---|
| 2026-09-17 | Rahul | No Agent Launchpad section in the protocol docs; application docs go with the app, use cases on moi.technology, backlinks are fine | Commit `75f608b` removed it from #124 |
| 2026-09-17 | Rahul | The guide must be written for humans, say what to do and why, cover creating and updating a page and explain how llms.txt is generated | The guide was rewritten on 2026-09-22 |
| 2026-09-29 | Robert Špendl | Page titles like "Coco - Context-Oriented Programming Language for MOI" are too long for a browser tab | Back to "Coco"; the long form stays on the Book home page, which overrides `<title>` in a `<head>` block |

## Hand-back
Give the operator the path of the draft, the counts (breaking, minor, questions), the verdict you recommend and why, what you did not check, and "Ready to post: yes or no". Do not post.

## Not yet known
- Whether Gokul has reviewed #124 (requested, no review recorded on 2026-10-02) and who must approve each repo. ASK: Rahul.
- Whether a posted comment may name private source on a private repo. ASK: Rahul.
