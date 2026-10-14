# Templates

Copy a file out, fill every `[FILL IN: ...]` marker, and run the lint named below. A marker left in a file is an error in both linters, so an unfilled template can never pass.

| File | Use | Check with |
|---|---|---|
| `post-skeleton.md` | An explainer, argument, how-to or session write-up | `python3 "$SKILLS/moi-blog/scripts/post-lint.py" --strict <file>` |
| `release-post-skeleton.md` | A monthly release post, in the shape of the September 2026 post. The only release post skeleton: the scaffold of the release-pack branch (`release-pack/scripts/new-release-pack.sh`) copies it into `BLOG.md` | `python3 "$SKILLS/moi-blog/scripts/post-lint.py" --strict <file>` |
| `pr-body.md` | The body of the publish pull request. It ends with no AI footer, on purpose | Read it once |
| `announce/social-copy.md` | The announcement copy file, `social/<slug>.md`, X and LinkedIn only | `python3 "$SKILLS/moi-blog/scripts/copy-lint.py" <file>` |
| `announce/status.md` | The record of what was sent where. Keep it outside the repo | Read it once |
| `announce/one-off-send.md` | A one-off email to an audience other than the monthly list | `bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" <file>` |
| `mailchimp/header.html`, `body.html`, `footer.html` | The three parts of the monthly RSS email (`references/newsletter.md`) | A test send, read on a phone |

The announcement pack's skeletons (the X thread, LinkedIn, Discord and `SOCIAL.md`) are in `release-pack/templates/`.

The Mailchimp parts were read before they were copied. None holds a secret, a personal address or a tracking id. The footer carries MOI's public social links, copied from the website footer, among them its public Discord invite. Two changes were made to the previous operator's originals: the header uses a colon in place of an HTML dash entity, and the footer uses the `-colour` icon files. The earlier single-file draft, `mailchimp-template.html`, is left out on purpose: it carries the loop bug and points at an image that no longer exists.
