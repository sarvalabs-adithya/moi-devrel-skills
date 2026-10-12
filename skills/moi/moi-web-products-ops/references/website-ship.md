# Website: ship a change

Facts are as of 2026-10-03 from `sarvalabs/MOI-Website` (public) `main` at commit `5e91afa`, its workflow files, the public GitHub API and GET reads. Back to `../GUIDE.md`. Commits, pull requests and merges are `moi-devrel/ship`; writing and announcing a blog post is `moi-blog` (its merge and live check are in `moi-blog/references/publishing.md`). This file holds what is specific to this repo.

## The path from a change to the live site
- `main` deploys. The workflow "Deploy MOI Website" (`deploy.yml`) runs on a push to `main` and on a manual run. It logs in through Teleport, then runs the website deploy script on the VM and hands it the API keys and the `VITE_*` values as `export` lines. That script is not in git and nothing in this repo says what it does. ASK: Upendhar for a copy.
- Two builds feed two hosts. `npm run build` makes `dist/` for moi.technology, including the static `/blog` listing. `npm run build --prefix blog` makes `blog/dist/` for blog.moi.technology. One markdown file feeds both, so a deploy must run both or a post is live but unlisted, or listed but missing (`DEPLOYMENT.md` on `main`). Whether the VM script runs both is in the script, so unknown to the repo.
- No pull request runs lint or tests. The only check on a PR is the preview build ("MOI Website PR Preview", `preview.yml`): it builds both sites with Node 22 and checks that each `index.html` exists. Run the checks below yourself.
- A preview is built from the PR head and served at `https://pr-<N>.preview.moi.technology` and `https://pr-<N>-blog.preview.moi.technology`, on a separate preview VM. The workflow posts them in a PR comment, rewrites the comment on every push, and deletes a preview when the PR closes or after 7 days.
- A merge never announces anything. Announcing is `moi-blog`.

## Run: change code or copy

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Baseline | `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" website`; `gh pr list -R sarvalabs/MOI-Website --state open` (read-only), from any folder. Open PRs on 2026-10-03: #57, #56, #54, #52, #8 | Output read. No open PR already does your change |
| 2 | GATE | Get the code (a download) | In a folder the operator chooses: `git clone https://github.com/sarvalabs/MOI-Website.git`, then `cd MOI-Website` (every command below runs from this folder, the clone root), then `npm ci` (add `npm ci --prefix blog` for a blog change, `npm ci --prefix server` to run the server). Node 22. Say source and size first | The operator said yes. Nothing was cloned before. `pwd` ends in `MOI-Website` |
| 3 | LOCAL | Identity and branch | In the clone: `bash "$SKILLS/moi-devrel/scripts/preflight.sh"`, then `git switch --no-track -c <prefix>/<name> origin/main`. Prefixes in use: `blog/`, `content/`, `chore/`, `ci/`, `fix/`, `feature/`, `favicon/` | Preflight has no FAIL. Branch is off the current `main` |
| 4 | LOCAL | Edit | Pages and papers: `website-content.md`. A post: `moi-blog`. Visual changes follow `moi-devrel/design` | The change is on disk |
| 5 | LOCAL | Check, because CI will not | `npm run lint`; `npm run build`; with a blog change also `npm run build --prefix blog`. Only the blog build checks post frontmatter; the root build exits 0 with a bad one | All exit 0 |
| 6 | LOCAL | Read it | `npm run dev` (Vite on localhost:5173; it generates the listing first). Note the PID and stop only that one. The Express server (`npm run dev:server`, port 3001) needs a local `.env` that the operator creates | The operator has seen it |
| 7 | GATE | Push and open one PR | Ask: "Ready to push `<branch>` (files: ...) to origin as `<login>` and open one PR against `main`. Yes?" Part A of `templates/change-checklist.md` is the body (part B stays out of the repo). No AI trailer. Whether to push to the org repo or a fork: ASK: Rahul | PR open, preview comment appears |
| 8 | CHECK | Read both previews | Desktop and phone width, the pages you touched, and `/blog` if a post changed. Preview cards in `/blog` link to production hosts, so judge a new post by its own preview URL | The operator has read both |
| 9 | GATE | Merge (this deploys) | Ask naming the PR number, base `main`, and "this deploys the site and the blog". Who approves is not recorded. ASK: Rahul | Merge commit exists |
| 10 | VERIFY | Wait, then read the live site | `gh run list -R sarvalabs/MOI-Website --workflow "Deploy MOI Website" --limit 3` until it finishes, then `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" website`, then open the page you changed. A deleted post: the blog URL must answer 404: `python3 "$SKILLS/moi-blog/scripts/check-live.py" <slug> --expect-gone` | The live page shows the change. A green run alone is not done |

## Run: deploy again without a change (after a secret or variable changed)

| # | Kind | Step | Command or action | Done when |
|---|---|---|---|---|
| 1 | CHECK | Confirm the need | `website-settings.md` says whether a redeploy is what the change needs | Yes |
| 2 | GATE | Manual run, on `main` only | `gh workflow run "Deploy MOI Website" -R sarvalabs/MOI-Website --ref main` | Run starts. The workflow exports the ref name to the VM script as `BRANCH`, and what the script does with it is unknown, so never run it from another branch |
| 3 | VERIFY | As step 10 above | | |

## Traps for this file
- `public/sitemap.xml` is written by hand. A new page needs a line there (`website-content.md`).
- The ref name goes to the VM script on a manual run. Use `main`.
- Secrets reach the VM only at deploy, as `export` lines. A name the workflow does not list never reaches the server.
- `vercel.json` and `api/` do nothing on the VM. Do not write them into deploy notes.
- Guides on `main` are stale (`website-health.md`). Trust the workflow files and live reads.
- Install steps download packages. Ask first.

## Not yet known
- What the website deploy script on the VM does: build order, `npm ci` or `npm install`, how the Express server is restarted, what `BRANCH` changes. ASK: Upendhar.
- How long a deploy takes, and whether anything notifies on failure. ASK: Upendhar.
- Who reviews and merges website PRs, and whether you push to the org repo. ASK: Rahul.
