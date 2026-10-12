# Previews

Facts are as of 2026-10-02 from the ops and docs research notes, and `MOI-Website`'s `preview.yml` re-read on 2026-10-03 from `origin/main` in the previous operator's clone as last fetched. A preview lets someone read a change before it is merged. It is never proof that production works. Back to `../GUIDE.md`.

## 1. Which repos have one
| Repo | Preview | Made by | Lasts |
|---|---|---|---|
| `MOI-Website` | `https://pr-<N>.preview.moi.technology` (site) and `https://pr-<N>-blog.preview.moi.technology` (blog) | The workflow "MOI Website PR Preview", on a PR opened, pushed to, reopened or closed. It builds both sites and posts one comment on the PR with the two links, rewritten on every push | Deleted after 7 days or when the PR closes |
| `moidocs`, `voyage-docs`, `coco-docs` | A Cloudflare Pages branch preview, `<branch>.<project>.pages.dev`, with projects `moichain-docs`, `voyage-docs`, `cocodocs`. Copy the URL from the Cloudflare check on the PR: how a branch name with `/` becomes a host name is not recorded | Cloudflare Pages, for every branch | Not recorded |
| `voyage-api` (MCP sync PRs) | `https://pr-<N>-mcp.preview.voyage.moi.technology`, deployed on the dev VM by `moi-mcp.preview.yml` on every PR to `voyage-api` | The Voyage workflow. Which branch of `voyage-api` holds the file is not recorded. ASK: Upendhar | Not recorded |
| `js-moi-sdk` docs | Not known. ASK: Gokul | | |
| Dataroom, Launchpad, Explorer, `moi-mcp`, `voyage`, Points | None recorded per PR. `preview.points.moi.technology` is the Points box under another name, not a preview of your branch. ASK: Upendhar whether any exists | | |
Where there is none, the local run is the preview (section 3), and the PR body says "no preview exists for this repo". A Cloudflare Pages build (project `moi-website`, `<branch>.moi-website.pages.dev`) also comments on `MOI-Website` PRs (read on #53 on 2026-10-03). Whether anyone still uses it is not settled. ASK: Upendhar.

## 2. Reading the Website preview
1. Wait for the comment. The workflow runs `npm ci`, `npm ci --prefix blog`, `npm run build` and `npm run build --prefix blog`, so a frontmatter error fails it, and a failed workflow leaves no comment.
2. Open both links on a desktop and on a phone. Click every link, and open every image. The operator reads the whole change once.
3. For a post, open `https://pr-<N>-blog.preview.moi.technology/article/<slug>/`. Do not run `check-live.py` against a preview: its canonical check fails by design, because the site hardcodes the production host.
4. Do not judge the listing from the apex preview. Its `/blog` cards link to production (`BLOG_ORIGIN` is set nowhere in the workflows), so a new slug 404s there. The card text still shows the frontmatter.
5. A production-only behaviour cannot be seen here: the community calendar reads an API on the dev host, and the chatbot is hidden. Do not call the change verified on the strength of a preview.

## 3. Reading a local preview
1. Install the repo's dependencies if they are missing (a download: a yes first, `templates/gate-asks.md`). Start the repo's own dev server on a free port and write the URL down. Known ports: Website `npm run dev` 5173 (it runs the blog index first), its Express server `npm run dev:server` 3001, blog `npm run dev --prefix blog` 4321, Dataroom and Points 3000. The Express server needs a `.env` the operator edits; Claude never opens it.
2. Note the port or the process id of what you started. Stop only that one. Never stop a process by a name pattern.
3. Name the fresh URL in the reply, and read what it serves. After a regenerate or a rebuild the operator once kept seeing the old deck and the old script (2026-09-04): restart the server on a new port and read the served page, not the file you edited.
4. A build under a running dev server corrupts the Launchpad's `.next`: stop the server before `npm run build`.
5. The operator may want to see it in a browser pane or on a phone. Tell them the exact address and which machine serves it.
6. Decks are viewed with `moi-webinar/deck`, which owns how to open, present and export one.

## 4. A preview-only PR
To compare an earlier text with the current one, the previous operator opened a PR of the earlier commit titled as a preview only and marked do not merge (PR #55), then closed it. It is a PR like any other: it needs its own yes, it notifies reviewers, and it gets closed with a yes.

## 5. Sending a link
A preview link is internal. Send it through the operator to a reviewer (a draft from `moi-devrel/templates/messages.md`), say it is a preview that expires, and do not put it in a public post or a public PR body beyond the comment the workflow itself makes. Links that expire in 7 days should not be pasted into long-lived docs.

## Not yet known
- Whether the docs previews can be opened without a login. ASK: Rahul, who owns the Cloudflare account.
- A preview for the Dataroom, Launchpad or Explorer. ASK: Upendhar.
- How long the Cloudflare and `voyage-api` previews live. ASK: Upendhar.
- The `js-moi-sdk` docs preview path. ASK: Gokul.
