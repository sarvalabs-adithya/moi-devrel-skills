# Legacy skills

These are older Claude skills from the previous operator's setup. They are **superseded**: each one has a maintained replacement under `skills/` in this repo. They are kept for two reasons: so you can see what the old guidance said, and because a few binary files (the brand guidelines PDF and the logo pack) exist only here.

Do not install these next to their replacements. They claim the same work and will fight for it.

| Old skill | Replaced by | Why it is still here |
| --- | --- | --- |
| `moi-blog/` | `skills/moi/moi-blog/` | Reference only. Its `references/` files document the MOI-Website blog, social and Mailchimp pipeline in detail, and the paths they cite (`blog/`, `social/`, `scripts/`) live in the MOI-Website repo, not here. |
| `moi-deck/` | `skills/moi/moi-webinar/deck/` (`GUIDE.md`, `templates/template.html`) | Reference only. Includes the old `scripts/render.sh`, `scripts/new-deck.sh` and `assets/template.html`. |
| `moi-design/` | `skills/moi/moi-devrel/design/` (`GUIDE.md`), a restructured copy with the known defects fixed | Source of the brand material: `moi-design/uploads/MOI Brand Guidelines.pdf` and `moi-design/uploads/MOI Logos.zip` are the official brand book and logo pack and are not stored anywhere else. |

## Known problems in the old copies

Read `skills/moi/moi-devrel/design/references/provenance.md` for the full list for `moi-design`. The ones most likely to bite:

- `moi-design/README.md` has the logo rule inverted (it says to use `Default - Dark.svg` on light backgrounds; the brand book says the opposite). A note in that file marks it.
- The old SVG logos render black, and the old `colors_and_type.css` loads Google Fonts in a way browsers ignore.
- `moi-design/README.md` names files that do not exist (`lucide.svg`, `pip-orbit.svg`) and a Figma file (`MOI Protocol.fig`) that is not in this repo.

## The duplicate folder

`moi-design/MOI Design System/` (about 21 MB) is a byte-identical duplicate of its parent `moi-design/`. This was checked with `diff -r` before the Legacy notes and punctuation fixes were applied to the parent, so the parent's `README.md`, `SKILL.md` and sub-READMEs now differ from the duplicate by those edits only. Nothing else in the repo links to the duplicate. It was left in place (nothing is deleted from this folder), but there is no reason to use it.

## What was changed in this folder

Each old `SKILL.md` has a short "Legacy" note after its frontmatter. Markdown files here (apart from the duplicate folder) had their em dashes replaced with ordinary punctuation, one example bearer value in `moi-blog/references/buffer.md` was replaced with a placeholder, and `moi-design/README.md` carries "Legacy note" corrections. HTML, CSS and script files are untouched.
