#!/usr/bin/env bash
# rebase-proof.sh: say whether a rebased branch changed nothing but its base.
#
# Usage:   cd <the working copy of the repo you are in>
#          bash "$SKILLS/moi-devrel/ship/scripts/rebase-proof.sh" <backup-ref> <rebased-ref> <new-base>
#            backup-ref   the branch as it was before the rebase (the backup branch you made)
#            rebased-ref  the branch after the rebase
#            new-base     what it was rebased onto, for example origin/main
#          SKILLS is the folder that holds the moi-* skills. Run it from inside the repository.
#
# What it proves: it replays the backup's own changes onto the new base with a three-way merge
# (git merge-tree --write-tree <new-base> <backup>, which finds the old fork point itself) and compares
# the resulting tree with the rebased branch's tree. Equal trees mean the rebase added nothing, dropped
# nothing and let no stale copy win. It also checks that the rebased branch sits on the new base.
#
# What it does not prove: a conflict you resolved by hand cannot be proved by a merge, so the verdict is
# then UNPROVEN and the conflicted files are listed for you to read. A DIFFERENT verdict means look at
# the listed files, not that the rebase is wrong: a rebase replays commit by commit and a merge replays
# the sum, and the two can differ when a later commit undoes an earlier one.
#
# Output:  SAME, DIFFERENT, UNPROVEN or NOT ON THE NEW BASE, then the evidence. File names are printed,
#          file contents never are. Env-named files show as [env-named file] and every printed value is
#          masked for secret shapes before any shortening.
# Exit:    0 the trees are equal, 1 different or unproven, 2 bad input (wrong arguments, a ref that does
#          not resolve, no common history, not a git repository, git older than 2.38).
# Safety:  read-only. It moves no ref, touches no working file and makes no network call. The merge
#          writes its trees into a temporary object folder that is deleted on exit, so the repository's
#          own object store is left as it was. Python 3 standard library only. Works under bash 3.2 and zsh.

for tool in python3 git; do
  command -v "$tool" >/dev/null 2>&1 || { echo "rebase-proof: $tool is needed and was not found on PATH" >&2; exit 2; }
done
exec python3 - "$@" <<'PY'
import os
import re
import shutil
import subprocess
import sys
import tempfile

LONG_HEX = re.compile(r"0x[0-9A-Fa-f]{17,}|[0-9A-Fa-f]{24,}")
SECRET_SHAPES = [re.compile(p) for p in (
    r"\bsk-[A-Za-z0-9_-]{8,}",
    r"\bgsk_[A-Za-z0-9]{12,}",
    r"\bAIza[0-9A-Za-z_-]{20,}",
    r"\b(?:AKIA|ASIA)[0-9A-Z]{12,}",
    r"\b(?:sk|rk)_live_[0-9A-Za-z]{8,}",
    r"\bnpm_[A-Za-z0-9]{20,}",
    r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{16,}|\bgithub_pat_[A-Za-z0-9_]{16,}",
    r"\bxox[abprso]-[A-Za-z0-9-]{8,}",
    r"https://hooks\.slack\.com/services/\S+",
    r"https://(?:ptb\.|canary\.)?discord(?:app)?\.com/api/webhooks/\S+",
    r"\b\d{8,10}:[A-Za-z0-9_-]{30,}",
    r"-----BEGIN (?:[A-Z]+ )*PRIVATE KEY(?: BLOCK)?-----",
    r"\beyJ[A-Za-z0-9_-]{6,}\.eyJ[A-Za-z0-9_-]{6,}\.[A-Za-z0-9_-]{6,}",
    r"(?<![A-Za-z0-9+/=])(?=[A-Za-z0-9+/=]*[A-Za-z])(?=[A-Za-z0-9+/=]*\d)[A-Za-z0-9+/=]{32,}",
)]
PHRASE_MIN = 12
PHRASE_STOP = frozenset(
    "after and are been being both but could did does each every for from get got had has her here "
    "him his how its let many may most not our out per see she should some than the their them these "
    "those too using via was were which while who why with would yes your".split())
_PIECE = re.compile(r"[A-Za-z]+|[^A-Za-z]+")
USAGE = ("usage: rebase-proof.sh <backup-ref> <rebased-ref> <new-base>\n"
         "exit: 0 trees equal, 1 different or unproven, 2 bad input")


def _mask_phrases(s):
    spans, run = [], []

    def close():
        if len(run) >= PHRASE_MIN:
            spans.append((run[0][1], run[-1][2]))
        del run[:]

    for m in _PIECE.finditer(s):
        text = m.group(0)
        if text[0].isalpha():
            if 3 <= len(text) <= 8 and text.lower() not in PHRASE_STOP:
                run.append((text, m.start(), m.end()))
            else:
                close()
        elif re.fullmatch(r"[\s,;]+", text):
            continue
        else:
            close()
    close()
    for a, b in reversed(spans):
        s = s[:a] + "(masked: 12 or more short words, possible recovery phrase)" + s[b:]
    return s


def mask(s):
    s = LONG_HEX.sub(lambda m: m.group(0)[:6] + "...(masked)", s)
    for rx in SECRET_SHAPES:
        s = rx.sub(lambda m: m.group(0)[:4] + "...(masked)", s)
    return _mask_phrases(s)


def is_env_name(path):
    low = os.path.basename(path).lower()
    return low in (".env", ".envrc") or low.startswith(".env.") or low.endswith(".env") or ".env." in low


def shown(path):
    """A path as it may be printed: env-named files by placeholder, the rest masked then shortened."""
    if is_env_name(path):
        return "[env-named file]"
    p = mask(path)
    return p if len(p) <= 110 else p[:107] + "..."


def bad(msg):
    print("rebase-proof: " + mask(msg), file=sys.stderr)
    return 2


def git(args, env=None, check=False):
    p = subprocess.run(["git"] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def resolve(ref):
    """The commit a ref names, or None. A ref that starts with a dash is refused outright."""
    if not ref or ref.startswith("-") or "\n" in ref or "\0" in ref:
        return None
    rc, out, _ = git(["rev-parse", "--verify", "--quiet", "--end-of-options", ref + "^{commit}"])
    return out.strip() if rc == 0 and out.strip() else None


def tree_of(commit):
    rc, out, _ = git(["rev-parse", "--verify", "--quiet", commit + "^{tree}"])
    return out.strip() if rc == 0 else None


def diff_names(tree_a, tree_b, env=None):
    """(status, path) pairs between two trees, as the second differs from the first."""
    rc, out, _ = git(["diff-tree", "-r", "--name-status", "-z", "--no-renames", tree_a, tree_b], env=env)
    if rc != 0:
        return None
    parts = out.split("\0")
    pairs = []
    i = 0
    while i + 1 < len(parts):
        if parts[i]:
            pairs.append((parts[i], parts[i + 1]))
        i += 2
    return pairs


def git_version():
    rc, out, _ = git(["--version"])
    m = re.search(r"(\d+)\.(\d+)", out)
    return (int(m.group(1)), int(m.group(2))) if rc == 0 and m else (0, 0)


def listing(title, pairs, limit=30):
    print(title)
    for st, path in pairs[:limit]:
        print("  %s  %s" % (st, shown(path)))
    if len(pairs) > limit:
        print("  ... and %d more" % (len(pairs) - limit))


def main(argv):
    if any(a in ("-h", "--help") for a in argv):
        print(USAGE)
        return 0
    if len(argv) != 3:
        print(USAGE, file=sys.stderr)
        return 2
    backup_ref, rebased_ref, base_ref = argv

    rc, out, _ = git(["rev-parse", "--is-inside-work-tree"])
    if rc != 0 or out.strip() != "true":
        return bad("not inside a git working copy. cd into the repository first")
    if git_version() < (2, 38):
        return bad("git 2.38 or newer is needed for merge-tree --write-tree. Update git, or compare by hand "
                   "with git diff <backup> <rebased> and read every file the new base also changed")

    commits = {}
    for label, ref in (("backup-ref", backup_ref), ("rebased-ref", rebased_ref), ("new-base", base_ref)):
        c = resolve(ref)
        if not c:
            return bad("%s '%s' does not name a commit in this repository" % (label, shown(ref)))
        commits[label] = c
    backup, rebased, base = commits["backup-ref"], commits["rebased-ref"], commits["new-base"]

    rc, out, _ = git(["merge-base", backup, base])
    if rc != 0 or not out.strip():
        return bad("the backup and the new base share no history, so there is nothing to replay")
    old_base = out.strip()

    print("backup   %s  (%s)" % (backup[:12], shown(backup_ref)))
    print("rebased  %s  (%s)" % (rebased[:12], shown(rebased_ref)))
    print("new base %s  (%s)" % (base[:12], shown(base_ref)))
    print("old fork point of the backup: %s" % old_base[:12])

    rc, _, _ = git(["merge-base", "--is-ancestor", base, rebased])
    if rc != 0:
        print("\nNOT ON THE NEW BASE: the rebased branch does not contain %s. "
              "It was not rebased onto it, so its content cannot be compared." % base[:12])
        return 1

    rc, out, _ = git(["rev-list", "--count", old_base + ".." + backup])
    n_old = out.strip() if rc == 0 else "?"
    rc, out, _ = git(["rev-list", "--count", base + ".." + rebased])
    n_new = out.strip() if rc == 0 else "?"
    print("commits: backup %s, rebased %s%s" % (
        n_old, n_new, "" if n_old == n_new else "  (different: some were squashed, split, added or dropped)"))

    # The merge writes tree objects. Send them to a temporary folder and read the real store as an
    # alternate, so this script leaves the repository's own object store untouched.
    rc, objdir, _ = git(["rev-parse", "--git-path", "objects"])
    if rc != 0:
        return bad("cannot find the object store")
    objdir = os.path.abspath(objdir.strip())
    tmp = tempfile.mkdtemp(prefix="rebase-proof-")
    try:
        env = dict(os.environ)
        env["GIT_OBJECT_DIRECTORY"] = tmp
        env["GIT_ALTERNATE_OBJECT_DIRECTORIES"] = objdir
        env["GIT_OPTIONAL_LOCKS"] = "0"
        rc, out, err = git(["merge-tree", "--write-tree", "--name-only", base, backup], env=env)
        if rc not in (0, 1) or not out.strip():
            return bad("git merge-tree failed: " + (err.strip().splitlines() or ["no message"])[0])
        lines = out.split("\n")
        replay_tree = lines[0].strip()
        conflicted = []
        if rc == 1:
            for ln in lines[1:]:
                if ln == "":
                    break
                conflicted.append(ln)
        rebased_tree = tree_of(rebased)
        if not rebased_tree or not re.fullmatch(r"[0-9a-f]{40,64}", replay_tree):
            return bad("could not read the trees to compare")

        # diff-tree must read the replay tree, which lives only in the temporary object folder.
        pairs = diff_names(replay_tree, rebased_tree, env=env)
        if pairs is None:
            return bad("could not compare the trees")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if not conflicted and not pairs:
        print("\nSAME: the rebased branch is exactly the backup's changes replayed on the new base. "
              "The rebase added nothing, dropped nothing and kept no stale copy.")
        return 0

    if not conflicted:
        print("\nDIFFERENT: %d file(s) in the rebased branch differ from the backup's changes replayed "
              "on the new base." % len(pairs))
        listing("  (M = changed in the rebased branch only, A = only in the rebased branch, "
                "D = in the replay but missing from the rebased branch)", pairs)
        print("Read each file against the new base and the backup. A stale copy of a page that another "
              "change updated is the usual cause (references/rebase-and-update.md).")
        return 1

    outside = [(st, p) for st, p in pairs if p not in conflicted]
    print("\nUNPROVEN: replaying the backup onto the new base conflicts in %d file(s). A merge cannot "
          "check a conflict you resolved by hand, so read these files yourself:" % len(conflicted))
    for p in conflicted[:30]:
        print("  C  %s" % shown(p))
    if len(conflicted) > 30:
        print("  ... and %d more" % (len(conflicted) - 30))
    if outside:
        listing("Outside those files, %d file(s) also differ from the replay:" % len(outside), outside)
    else:
        print("Outside those files the rebased branch equals the replay.")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as exc:  # a clear message and exit 2, never a traceback
        print("rebase-proof: unexpected error (%s): %s" % (type(exc).__name__, mask(str(exc))), file=sys.stderr)
        sys.exit(2)
PY
