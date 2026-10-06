# Publishing a post

Facts are as of 2026-10-02, from `sarvalabs/MOI-Website` on `main` (commit `5e91afa`), its workflow files, the public GitHub API and read-only requests to the live site. Back to `../SKILL.md`.

## The repo and the folder
`sarvalabs/MOI-Website` is public, and `main` deploys. The marketing site (React and Vite) is at the root. The blog is a separate Astro app in `blog/` with its own `package.json`. One Markdown file feeds both builds.
| Path | What |
|---|---|
| `blog/src/content/posts/<slug>.md` | The post. The only file a plain post needs |
| `blog/src/assets/<post>/` | Images used in the body (`assets.md`) |
| `blog/public/covers/`, `blog/public/brand/` | Cover images and brand files, served as they are |
| `social/<slug>.md` | The announcement copy (`distribution.md`) |
| `scripts/` | `build-blog-index.js`, `social-init.js`, `distribute.js`, `share-links.js`, `buffer-channels.js` |
| `.github/workflows/` | `deploy.yml`, `preview.yml`, `social-prepare.yml`, `distribute.yml` |
`public/blog/` and `public/covers/` at the root are generated and gitignored. Do not edit or commit them.

## Branch, identity, files
1. From inside the clone: `bash "$SKILLS/moi-devrel/scripts/preflight.sh"`, then `git status`.
2. `git fetch origin`, then `git switch --no-track -c blog/<slug> origin/main`, so the branch starts from the current `main`, not a stale local copy. Prefixes seen in the repo: `blog/`, `content/`, `chore/`, `ci/`, `fix/`, `feature/`.
3. Commit under your work identity. No AI co-author line and no "generated with" footer. The September PR body carries the footer and so do open PRs #52 and #54 (read 2026-10-02). On 2026-10-01 the previous operator had the trailer and footer removed from the six open geo-fixes pull requests, #57 here among them. Merged history is left as it is. Do not add either to a new commit or PR body.
4. Local edits and local commits need no gate once the operator has asked for the commit. A push does.
Pull requests #53 and #55 came from branches inside `sarvalabs/MOI-Website`, not from a fork, and #53 was merged by its author. ASK: Rahul whether you push to the org repo or to a fork, and how access is granted.

## Build and read locally
```
npm ci                           # once; a download, so a yes first
npm ci --prefix blog             # once; a download
npm run dev --prefix blog        # the blog at localhost:4321
npm run build --prefix blog      # validates frontmatter, renders, emits sitemap, feeds, llms.txt
npm run build                    # root: build-blog-index.js, then vite build
python3 "$SKILLS/moi-blog/scripts/post-lint.py" --strict blog/src/content/posts/<slug>.md
```
- Run both builds. Only the blog build validates the post. The root build parses frontmatter with `gray-matter`, writes `undefined` into the listing card and exits 0. The blog build never writes the apex listing, and the root build never renders the article.
- `npm run dev` at the root serves the apex site at localhost:5173, with the listing at `/blog`. It runs the listing script first.
- When you start a server, note its port or PID and stop only that. Never stop one by name pattern.
- The operator reads the whole post once locally before the PR.

## The pull request
Ask in this shape and then do exactly that: "Ready to push branch `blog/<slug>` (files: `blog/src/content/posts/<slug>.md`) to origin as <login>. Yes?" Then, from the clone:
```
git push -u origin blog/<slug>
gh pr create --repo sarvalabs/MOI-Website --base main --head blog/<slug> --title "blog: <what>" --body-file "$WORK/<slug>/pr-body.md"
```
The operator may open it in the browser instead. Copy the template and fill it first: `cp "$SKILLS/moi-blog/templates/pr-body.md" "$WORK/<slug>/pr-body.md"`.
- One PR per post. Title: `blog: <what>`. The September one was `blog: MOI September 2026 release (moipod v0.13.0, fee delegation)`. Body: `../templates/pr-body.md`.
- Verification in the body gives counts and public sources only. The ledger stays outside the repo, and no private repo path goes in a public PR.
- Review changes go on the same branch in small commits, in one batch, and merge as one squash. The September PR had 24 commits and landed as one. Do not open a PR per tweak.
- Comparing versions: a preview-only PR of the earlier commit, titled as a preview only, marked do not merge, and closed after comparing (#55). It is another PR, so it needs its own yes and it notifies reviewers.
- The preview comment appears on the PR: `https://pr-<N>.preview.moi.technology` and `https://pr-<N>-blog.preview.moi.technology`. It is rewritten on every push. The previews are deleted after 7 days or when the PR closes. The workflow runs `npm ci`, `npm ci --prefix blog`, `npm run build` and `npm run build --prefix blog`, so a frontmatter error fails it.
- Verify the post at `https://pr-<N>-blog.preview.moi.technology/article/<slug>/`, by reading it. `check-live.py` is for production: on a preview its canonical check fails by design, because the site hardcodes the production host. Do not verify through the apex preview's `/blog` listing: `BLOG_ORIGIN` is set nowhere in the workflows, so every card links to production and a new slug 404s there. The card's text still checks the frontmatter.
- Cloudflare Pages also comments a build on each PR (seen on #53). Its use for the blog is not recorded.

## Review and merge
- The September PR body names the internal reviewer and says the post was framed per the internal review. It carried two boxes still unchecked when it merged: confirm the go-live date (the go-moi tag was dated 10 September, the upgrade 11 September) and the internal review. Keep such boxes open until someone answers them.
- Who else must approve, and who may merge, is not recorded. ASK: Rahul.
- A merge to `main` deploys the site and the blog together. Merge only on a yes that names the PR number, never to look at it. #53 was a squash merge: `gh pr merge <N> --repo sarvalabs/MOI-Website --squash`, or the button.
- About a minute after a merge the "Prepare social copy" workflow opens a second PR with `social/<slug>.md` (26 seconds on 2026-09-11). Nothing is sent.

## What deploys, and how
The website's deploy path (the workflow "Deploy MOI Website", the VM script that is not in git, a manual run on `main` only, the leftover `vercel.json`) is `moi-web-products-ops/references/website-ship.md`. Read it before a manual run. What the blog adds:
- `moi.technology` and `blog.moi.technology` are separate hosts. The blog builds with no secret.

## Check the live page
Find the deploy run with `gh run list --repo sarvalabs/MOI-Website --workflow "Deploy MOI Website" --limit 3` and wait for it to finish, then run `python3 "$SKILLS/moi-blog/scripts/check-live.py" <slug>`. It makes GET requests only, and checks the page, the canonical, one H1, JSON-LD, `llms.txt`, the sitemap, both feeds and the apex listing. Then by hand:
1. Open the URL. Read the title tag and the first screen.
2. Click every link, including the docs links, and open every image.
3. Open `https://moi.technology/blog` and find the card. A post that is live and missing there means the root build did not run.
4. After deleting a post: `python3 "$SKILLS/moi-blog/scripts/check-live.py" <slug> --expect-gone`. The apex answers 200 for any path (`https://moi.technology/definitely-not-a-page`, observed 2026-10-02), so its status code proves nothing. The blog host answers 404 for an unknown article.
5. Ask the operator before requesting indexing in the Search Console property of the blog (`geo.md`).
Read-only health reads: `curl -sI https://blog.moi.technology/`, and the same for `/rss.xml`, `/rss-email.xml`, `/sitemap-index.xml` and `/llms.txt`. All answered 200 on 2026-10-02.

## Editing or deleting a published post
- An edit goes through the same flow. Set `updated` only if the post changed after publication. An edit never re-announces: "Prepare social copy" only looks at added files.
- To delete, remove the file in a PR (or set `draft: true`). After the deploy, run `python3 "$SKILLS/moi-blog/scripts/check-live.py" <slug> --expect-gone`. Deleted posts survived deploys in August 2026, and Srikar said he had fixed the script (2026-08-18). The fix is not in git and was not re-checked.
- Do not rename a published slug. The slug is the URL, the canonical and the feed `guid`. In `/rss-email.xml` the `guid` is the tagged URL, so a rename, or an edit to `blog/src/lib/utm.js`, changes every guid at once. Mailchimp decides what is new from guid and publication date (a Mailchimp behaviour not observable from here).

## Broken or unknown as of 2026-10-02
| Item | State | Who knows |
|---|---|---|
| `CONTENT.md`, `DEPLOYMENT.md`, `blog/README.md` | Stale on `main`. Corrected copies are uncommitted on the previous operator's machine | ASK: Adithya for a copy |
| Open PRs in `sarvalabs/MOI-Website` | #56 September copy (never merged), #52 access-policies post (open since 2026-08-31, not a draft; read 2026-10-03), #54 x402 post (draft), #57 prerender and metadata for the marketing routes, #8 Cloudflare preview test | ASK: Rahul what to do with #52 and #54 |
| Owners of Search Console, Analytics, Tag Manager, Buffer, Mailchimp | Not recorded | ASK: Rahul |
| Whether a PR preview is open to anyone with the link | Not recorded | ASK: Upendhar |
| Whether a merge needs a second approval | Not recorded | ASK: Rahul |
The website's own faults and unknowns (the VM deploy script, the apex answering 200 for any address, the calendar API, `VITE_GA_ID`) are in `moi-web-products-ops/references/` (`website-health.md`, `website-ship.md`, `website-settings.md`), not here.

Before touching the website's admin, read its row in `moi-devrel/references/repo-map.md`.

## Not yet known
- The October release post date, and whether a release post is expected every month (two exist, so monthly is inferred). ASK: Rahul.
- How long a deploy takes and how to see its log without admin access. ASK: Upendhar.
- Whether Cloudflare Pages previews are used for the blog. ASK: Upendhar.
