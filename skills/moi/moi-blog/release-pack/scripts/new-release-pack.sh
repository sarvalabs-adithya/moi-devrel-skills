#!/usr/bin/env bash
# new-release-pack.sh: scaffold protocol-release-<version>/ in the current folder from this branch's templates.
#
# Usage:  bash "$SKILLS/moi-blog/release-pack/scripts/new-release-pack.sh" <version>
#         SKILLS is the folder that holds the moi-* skills. Run it from the root of the working copy of
#         moi-foundation/MOI-Webinars, where pack folders sit, never from inside moi-blog. <version> is the protocol release without
#         the v, for example 0.13.0 (v0.13.0 is accepted). A release candidate is written 0.14.0-rc1.
# Makes:  protocol-release-<version>/RELEASE-NOTE.md    empty on purpose: paste the note exactly as received
#         protocol-release-<version>/SOCIAL.md          the plan and the record, with no copy of any post
#         protocol-release-<version>/BLOG.md            a copy of moi-blog's release post skeleton
#         protocol-release-<version>/.gitignore         one line, *, so the folder ignores itself
#         protocol-release-<version>/social/thread/1.txt to 7.txt, social/linkedin.txt,
#         social/linkedin.native.txt, social/discord.txt, social/x.txt
#         The correction reply template is not copied. corrections.md says when to copy it.
#         No ledger.csv is made: step 3 of moi-blog/release-pack/GUIDE.md makes it with cp -n from the extractor's
#         output, whose header is moi-devrel/claim-check's, so there is one header and a rerun cannot
#         overwrite a ledger that has verdicts in it.
# Why the .gitignore: the folder holds an unannounced release note and a ledger whose source column may
#         name private repositories, and the repo is public. The rule hides the folder, itself included,
#         from git add. Remove it only on the operator's yes.
# Fills:  {{version}} in the social and SOCIAL.md templates. Every other {{...}} stays, and thread-lint.py
#         reports it as a placeholder until it is replaced. BLOG.md carries [FILL IN: ...] markers from
#         moi-blog's skeleton, which post-lint.py reports.
# Refuses to overwrite: if protocol-release-<version> already exists (a folder, a file or a link),
#         nothing is written. The folder is built in a scratch folder and moved into place at the end,
#         so a failure leaves nothing half made.
# Reads this branch's templates and moi-blog's release post skeleton (found under $SKILLS/moi-blog when
#         SKILLS is set, else next to this branch in moi-blog/templates), and writes only that one new folder. It builds it first in a scratch folder
#         under TMPDIR and removes that on exit. The only git command it runs is
#         `git rev-parse --show-toplevel`, to check where it is. It pushes nothing, posts nothing and calls
#         no service.
# Exit:   0 created; 1 refused (folder exists, or a template or the skeleton is missing); 2 bad usage, a
#         version it does not accept, or a run from inside moi-blog or its release-pack folder (it would
#         write there).
set -eu

usage() {
  echo 'usage: new-release-pack.sh <version>   e.g. new-release-pack.sh 0.13.0' >&2
}
if [ $# -ne 1 ] || [ -z "$1" ]; then usage; exit 2; fi
version=${1#v}
# The character check comes first: grep reads a value line by line, so a value with a newline in it
# would pass the pattern below on its first line.
case "$version" in
  *[!0-9a-z.-]*) bad=1 ;;
  *) bad=0 ;;
esac
if [ "$bad" -ne 0 ] || ! printf '%s' "$version" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+(-rc[0-9]+)?$'; then
  echo "REFUSED: that is not a version I accept. Write it like 0.13.0 or 0.14.0-rc1. Nothing was created." >&2
  exit 2
fi

# This script sits in moi-blog/release-pack/scripts. branch_dir is release-pack, blog_dir is moi-blog.
branch_dir=$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd -P)
blog_dir=$(cd "$branch_dir/.." && pwd -P)
tpl="$branch_dir/templates"
dest="protocol-release-$version"

inside() {
  case "$(pwd -P)/" in
    "$1"/*) return 0 ;;
  esac
  return 1
}
# Inside release-pack always refuses. Inside moi-blog refuses only when that folder is the skill (it has a
# SKILL.md), so a copy of the branch in a scratch folder can still be run from the scratch folder's parent.
if inside "$branch_dir" || { [ -f "$blog_dir/SKILL.md" ] && inside "$blog_dir"; }; then
  echo "REFUSED: this folder is inside moi-blog. Run it from the root of a working copy of moi-foundation/MOI-Webinars. Nothing was created." >&2
  exit 2
fi

if [ -e "$dest" ] || [ -L "$dest" ]; then
  echo "REFUSED: $dest already exists. Nothing was changed. Work in that folder, or pick another version." >&2
  exit 1
fi
for need in SOCIAL.md social/thread/1.txt social/x.txt social/discord.txt; do
  if [ ! -f "$tpl/$need" ]; then
    echo "REFUSED: the branch's template $tpl/$need is missing. Nothing was created." >&2
    exit 1
  fi
done
# The release post skeleton is moi-blog's, so there is one copy of it. Look under $SKILLS first, then in the
# moi-blog folder that holds this branch.
blog_skel=""
if [ -n "${SKILLS:-}" ] && [ -f "$SKILLS/moi-blog/templates/release-post-skeleton.md" ]; then
  blog_skel="$SKILLS/moi-blog/templates/release-post-skeleton.md"
elif [ -f "$blog_dir/templates/release-post-skeleton.md" ]; then
  blog_skel="$blog_dir/templates/release-post-skeleton.md"
fi
if [ -z "$blog_skel" ]; then
  echo "REFUSED: moi-blog's release post skeleton (templates/release-post-skeleton.md) was not found under SKILLS or beside this branch. Set SKILLS to the folder that holds the moi-* skills. Nothing was created." >&2
  exit 1
fi

stage=$(mktemp -d "${TMPDIR:-/tmp}/moi-release-pack.XXXXXX")
trap 'rm -rf "$stage"' EXIT
chmod 755 "$stage"

: > "$stage/RELEASE-NOTE.md"
find "$tpl" -type f | while IFS= read -r src; do
  rel=${src#"$tpl"/}
  case "$rel" in
    social/x-correction-reply.txt) continue ;;   # copied only when a correction is needed
    *) out="$rel" ;;
  esac
  mkdir -p "$stage/$(dirname "$out")"
  sed "s/{{version}}/$version/g" "$src" > "$stage/$out"
done
cp "$blog_skel" "$stage/BLOG.md"
printf '*\n' > "$stage/.gitignore"

mv "$stage" "$dest"
trap - EXIT

echo "Created $dest/"
( cd "$dest" && find . -type f | sort | sed 's|^\./|  |' )
echo "The folder ignores itself (.gitignore holds one line, *). git add cannot pick it up. Remove that rule only on the operator's yes."
here=$(pwd -P)
top=$(git rev-parse --show-toplevel 2>/dev/null || true)
if [ -z "$top" ] || [ "$top" != "$here" ]; then
  echo "NOTE: this is not the root of a git working copy. Pack folders belong at the root of moi-foundation/MOI-Webinars."
fi
echo "Next:"
echo "  1. Paste the release note into $dest/RELEASE-NOTE.md exactly as received, nothing else (moi-blog/release-pack/references/the-note.md)."
echo "  2. Record where it came from and its hash in $dest/SOCIAL.md: shasum -a 256 $dest/RELEASE-NOTE.md"
echo "  3. Start the ledger (moi-blog/release-pack/GUIDE.md step 3), fill the posts, then: python3 \"\$SKILLS/moi-blog/release-pack/scripts/thread-lint.py\" $dest/social"
echo "Nothing was added to git and nothing was sent."
