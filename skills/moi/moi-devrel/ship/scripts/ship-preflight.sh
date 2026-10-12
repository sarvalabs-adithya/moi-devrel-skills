#!/usr/bin/env bash
# ship-preflight.sh: read-only check of a branch before the push gate. One PASS, WARN or FAIL line each.
#
# Usage:   cd <the working copy of the repo you are shipping from>
#          bash "$SKILLS/moi-devrel/ship/scripts/ship-preflight.sh" [--no-preflight] [<base>]
#            base   the ref the pull request will target, for example origin/main. Default: the
#                   remote's default branch (origin/HEAD), else origin/main, origin/master, origin/develop.
#                   A Points Program PR targets origin/feature/ci-cd, so pass it.
#            --no-preflight   skip moi-devrel's preflight.sh (use it only offline; the default runs it)
#          SKILLS is the folder that holds the moi-* skills. Run it from inside the repository.
#          It finds moi-devrel's preflight.sh and secret-scan.sh in $SKILLS when that is set and holds
#          them, otherwise three folders above its own scripts folder (this is a branch of moi-devrel).
#
# What it checks:
#   1. moi-devrel's preflight.sh (tools, git identity, gh login, remote), its output shown indented;
#   2. the branch is not the default branch, the base's branch or a branch that deploys on push;
#   3. how the branch stands against its upstream (not pushed, in step, behind, diverged) and against the
#      base (commits ahead, commits behind, a predicted conflict, merge commits in the range);
#   4. every commit in base..HEAD: no AI co-author trailer or "generated with" footer (Claude, Anthropic,
#      Copilot, ChatGPT, OpenAI, Codex, Gemini or Cursor named in it), no author or
#      committer address at a personal mail provider, subjects of 72 characters or fewer, no fixup/squash;
#   5. the working tree: uncommitted changes, and untracked env-named files that `git add -A` would stage;
#   6. the files changed, with FAIL for an env-named file in any commit of the range and WARN for
#      transcripts, recordings, ledgers or review packages, and generated or build output;
#   7. moi-devrel's secret-scan.sh over the committed copy of every changed file and every commit message.
#   It then prints the files changed. File contents are never printed.
#
# Output:  PASS, WARN, FAIL per line, then a summary. A WARN leaves the exit code at 0: read every WARN.
#          Every printed value is masked for secret shapes (keys, tokens, JWTs, long hex, recovery-phrase
#          runs) before it is shortened. Env-named files show as [env-named file] and are never opened.
# Exit:    0 no FAIL, 1 at least one FAIL, 2 bad usage or not inside a git repository.
# Safety:  read-only. It moves no ref and edits no file; git runs with optional locks off, so even the
#          index is not refreshed. No network call except the one gh auth status inside preflight.sh.
#          Python 3 standard library only. Works under bash 3.2 and zsh (run it with bash).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
export SCRIPT_DIR
for tool in python3 git; do
  command -v "$tool" >/dev/null 2>&1 || { echo "ship-preflight: $tool is needed and was not found on PATH" >&2; exit 2; }
done
exec python3 - "$@" <<'PY'
import os
import re
import shutil
import subprocess
import sys
import tempfile

SCRIPT_DIR = os.environ["SCRIPT_DIR"]


def find_library():
    """The folder that holds the moi-* skills. This script sits in <library>/moi-devrel/ship/scripts, so its own
    library is three folders up. $SKILLS wins when it is set and holds moi-devrel's scripts; otherwise the
    script's own location is used."""
    own = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
    env = os.environ.get("SKILLS", "")
    if env and os.path.isfile(os.path.join(env, "moi-devrel", "scripts", "preflight.sh")):
        return env
    return own


LIBRARY = find_library()
PREFLIGHT = os.path.join(LIBRARY, "moi-devrel", "scripts", "preflight.sh")
SECRET_SCAN = os.path.join(LIBRARY, "moi-devrel", "scripts", "secret-scan.sh")

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

PERSONAL_DOMAINS = frozenset(
    "gmail.com googlemail.com yahoo.com yahoo.co.in yahoo.in ymail.com hotmail.com hotmail.co.in "
    "outlook.com outlook.in live.com live.in msn.com icloud.com me.com mac.com aol.com proton.me "
    "protonmail.com pm.me gmx.com gmx.net yandex.com mail.com rediffmail.com hey.com fastmail.com "
    "zoho.com tutanota.com".split())
# Branches that start a deploy when pushed (moi-devrel/references/repo-map.md, as of 2026-10-03).
DEPLOY_BRANCHES = frozenset(["main", "master", "develop", "feature/ci-cd", "feature/moi-agent-launchpad-cicd"])
AI_NAMES = "claude|anthropic|copilot|chatgpt|openai|codex|gemini|cursor"
AI_TRAILER = re.compile(r"^\s*co-authored-by:.*(%s)|noreply@anthropic\.com" % AI_NAMES, re.I | re.M)  # slop-lint:ignore
AI_FOOTER = re.compile(r"generated\s+(?:with|by)\b[^\n]{0,40}(%s)" % AI_NAMES, re.I)
TEMPLATE_SUFFIXES = (".example", ".sample", ".template", ".dist", ".tpl")
PRIVATE_LOOKING = re.compile(
    r"transcript|\.(vtt|srt|mp4|m4a|mov|wav|mp3|webm)$|claim-ledger|claim-check-|numbers-ledger|"
    r"(^|/)ledger\.csv$|review-package|test-log|(^|/)(HANDOVER|DEPENDENCIES|FIX-PLAN)[^/]*\.md$", re.I)
GENERATED = re.compile(
    r"(^|/)(node_modules|\.next|\.docusaurus|build)/|(^|/)llms(-full)?\.txt$|^public/(blog|covers)/", re.I)

counts = {"PASS": 0, "WARN": 0, "FAIL": 0}
GIT_ENV = dict(os.environ, GIT_OPTIONAL_LOCKS="0", LC_ALL="C")


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


def is_env_template(path):
    return is_env_name(path) and os.path.basename(path).lower().endswith(TEMPLATE_SUFFIXES)


def shown(text, width=100):
    """Printable form: env-named files by placeholder, then masked, then shortened (never the reverse)."""
    if is_env_name(text):
        return "[env-named file]"
    t = mask(text.replace("\n", " "))
    return t if len(t) <= width else t[:width - 3] + "..."


def say(level, msg):
    counts[level] += 1
    print("%-5s %s" % (level, mask(msg)))


def note(msg):
    print("      " + mask(msg))


def git(args, text=True):
    p = subprocess.run(["git"] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=GIT_ENV)
    if text:
        return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")
    return p.returncode, p.stdout, p.stderr


def resolve(ref):
    if not ref or ref.startswith("-") or "\n" in ref or "\0" in ref:
        return None
    rc, out, _ = git(["rev-parse", "--verify", "--quiet", "--end-of-options", ref + "^{commit}"])
    return out.strip() if rc == 0 and out.strip() else None


def usage_error(msg):
    print("ship-preflight: " + mask(msg), file=sys.stderr)
    return 2


def count_pair(left, right):
    """(only on the left, only on the right) commit counts for left...right."""
    rc, out, _ = git(["rev-list", "--left-right", "--count", "%s...%s" % (left, right)])
    if rc != 0:
        return None
    a, b = out.split()
    return int(a), int(b)


def run_preflight():
    if not os.path.isfile(PREFLIGHT):
        say("FAIL", "moi-devrel preflight.sh was not found. Set SKILLS to the folder that holds the moi-* "
                    "skills, including moi-devrel; this script looked there and three folders above itself")
        return
    try:
        p = subprocess.run(["bash", PREFLIGHT], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    except subprocess.TimeoutExpired:
        say("FAIL", "preflight.sh did not finish in 120 seconds (gh auth status may be waiting on the network). "
                    "Run it by hand, or pass --no-preflight offline")
        return
    text = p.stdout.decode("utf-8", "replace")
    fails = warns = 0
    print("--- moi-devrel preflight.sh (identity, tools, gh login, remote) ---")
    for ln in text.splitlines():
        print("  | " + mask(ln))
        if ln.startswith("FAIL"):
            fails += 1
        elif ln.startswith("WARN"):
            warns += 1
    print("--- end of preflight.sh ---")
    if p.returncode != 0 or fails:
        say("FAIL", "preflight.sh reported %d FAIL line(s) (exit %d). Fix them before any commit or PR" % (fails, p.returncode))
    else:
        say("PASS", "preflight.sh reported no FAIL")
    if warns:
        say("WARN", "preflight.sh printed %d WARN line(s) above. Read each one" % warns)


def main(argv):
    skip_pre = False
    base_arg = None
    for a in argv:
        if a in ("-h", "--help"):
            print("usage: ship-preflight.sh [--no-preflight] [<base>]\n"
                  "exit: 0 no FAIL, 1 at least one FAIL, 2 bad usage")
            return 0
        if a == "--no-preflight":
            skip_pre = True
        elif a.startswith("-"):
            return usage_error("unknown option '%s'. usage: ship-preflight.sh [--no-preflight] [<base>]" % shown(a))
        elif base_arg is None:
            base_arg = a
        else:
            return usage_error("only one base is accepted")

    rc, out, _ = git(["rev-parse", "--is-inside-work-tree"])
    if rc != 0 or out.strip() != "true":
        return usage_error("not inside a git working copy. cd into the repository you are shipping from")
    rc, top, _ = git(["rev-parse", "--show-toplevel"])
    repo_name = os.path.basename(top.strip()) if rc == 0 else "?"

    # ---- base and branch
    rc, out, _ = git(["symbolic-ref", "--short", "-q", "HEAD"])
    branch = out.strip() if rc == 0 else ""
    rc, out, _ = git(["symbolic-ref", "--short", "-q", "refs/remotes/origin/HEAD"])
    default_ref = out.strip() if rc == 0 else ""   # for example origin/main
    base_ref = base_arg
    if base_ref is None:
        for cand in [default_ref, "origin/main", "origin/master", "origin/develop"]:
            if cand and resolve(cand):
                base_ref = cand
                break
    if base_ref is None:
        return usage_error("cannot find a base branch. Pass one, for example origin/main")
    base = resolve(base_ref)
    if not base:
        return usage_error("base '%s' does not name a commit. Fetch first, or pass origin/<branch>" % shown(base_ref))

    print("ship-preflight: repo %s, branch %s, base %s" % (shown(repo_name), shown(branch or "(detached)"), shown(base_ref)))
    rc, urls, _ = git(["remote", "-v"])
    if rc == 0 and "moi-project" in urls and not base_ref.endswith("feature/ci-cd"):
        say("WARN", "this looks like the Points Program repo, which deploys from feature/ci-cd and not from main "
                    "(repo-map.md). Pass origin/feature/ci-cd as the base unless the PR is meant for another branch")
    if not skip_pre:
        run_preflight()
    else:
        say("WARN", "moi-devrel preflight.sh was skipped (--no-preflight). Identity and gh login are unchecked")

    # ---- branch is not a branch that deploys
    if not branch:
        say("FAIL", "detached HEAD. Check out a topic branch before shipping")
    else:
        default_name = default_ref.split("/", 1)[1] if default_ref.startswith("origin/") else ""
        base_name = base_ref.split("/", 1)[1] if base_ref.startswith("origin/") else base_ref
        if branch in (default_name, base_name) or branch in DEPLOY_BRANCHES:
            say("FAIL", "branch %s is the default branch, the base or a branch that deploys on push. "
                        "Work on a topic branch (merge is deploy)" % shown(branch))
        else:
            say("PASS", "branch %s is a topic branch (not the default %s or a deploy branch)"
                % (shown(branch), shown(default_name or "branch")))

    # ---- against the base
    pair = count_pair(base_ref, "HEAD")
    behind_base = ahead_base = 0
    if pair is None:
        say("FAIL", "cannot compare HEAD with %s (no common history?)" % shown(base_ref))
    else:
        behind_base, ahead_base = pair
        if ahead_base == 0:
            say("FAIL", "no commit ahead of %s: there is nothing to ship" % shown(base_ref))
        else:
            say("PASS", "%d commit(s) ahead of %s" % (ahead_base, shown(base_ref)))
        if behind_base:
            say("WARN", "%d commit(s) behind %s. Rebase before the pull request if it would conflict or if "
                        "the base changed files you touched (references/rebase-and-update.md)" % (behind_base, shown(base_ref)))
        else:
            say("PASS", "up to date with the last fetched %s" % shown(base_ref))
    rc, out, _ = git(["rev-list", "--merges", "%s..HEAD" % base_ref])
    n_merges = len(out.split()) if rc == 0 else 0
    if n_merges:
        say("WARN", "%d merge commit(s) in the range. Prefer a linear branch: a rewrite cannot be limited to "
                    "your own commits when merges from the base are inside it" % n_merges)

    # a predicted conflict, with the merge's trees sent to a temporary folder so no object is written
    rc, objdir, _ = git(["rev-parse", "--git-path", "objects"])
    rc_v, ver, _ = git(["--version"])
    m = re.search(r"(\d+)\.(\d+)", ver)
    if rc == 0 and rc_v == 0 and m and (int(m.group(1)), int(m.group(2))) >= (2, 38) and ahead_base:
        tmp = tempfile.mkdtemp(prefix="ship-preflight-")
        try:
            env = dict(GIT_ENV, GIT_OBJECT_DIRECTORY=tmp, GIT_ALTERNATE_OBJECT_DIRECTORIES=os.path.abspath(objdir.strip()))
            p = subprocess.run(["git", "merge-tree", "--write-tree", "--name-only", base_ref, "HEAD"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
            if p.returncode == 1:
                lines = p.stdout.decode("utf-8", "replace").split("\n")[1:]
                files = []
                for ln in lines:
                    if ln == "":
                        break
                    files.append(ln)
                say("WARN", "merging this branch into %s would conflict in %d file(s): %s. Rebase and resolve "
                            "before the pull request" % (shown(base_ref), len(files), ", ".join(shown(f, 40) for f in files[:5])))
            elif p.returncode == 0:
                say("PASS", "a merge into %s would be clean" % shown(base_ref))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # ---- against the upstream
    rc, out, _ = git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"])
    upstream = out.strip() if rc == 0 else ""
    if not upstream:
        say("WARN", "no upstream: the branch has not been pushed, or does not track a remote branch. "
                    "That is expected before the first push")
    else:
        up = count_pair(upstream, "HEAD")
        rc, sha, _ = git(["rev-parse", "--short=12", upstream])
        seen = sha.strip() if rc == 0 else "?"
        if up is None:
            say("WARN", "cannot compare with %s" % shown(upstream))
        else:
            behind, ahead = up
            if behind == 0 and ahead == 0:
                say("PASS", "in step with %s (last fetched remote commit %s)" % (shown(upstream), seen))
            elif behind == 0:
                say("PASS", "%d commit(s) not pushed yet to %s (last fetched remote commit %s)" % (ahead, shown(upstream), seen))
            elif ahead == 0:
                say("WARN", "%d commit(s) behind %s. Someone else pushed to the branch, or you rewrote it on "
                            "another machine. Fetch and read them before you push" % (behind, shown(upstream)))
            else:
                say("WARN", "diverged from %s (ahead %d, behind %d, last fetched remote commit %s). A plain "
                            "push will be refused. Read the %d commit(s) the remote has and you lack "
                            "(git log HEAD..%s): if they are not yours, stop. If they are your own earlier versions "
                            "because you rewrote on purpose, push only with --force-with-lease=<branch>:<the remote "
                            "commit you last saw before the rewrite> and the operator's yes "
                            "(references/rebase-and-update.md, section 3)"
                    % (shown(upstream), ahead, behind, seen, behind, shown(upstream)))

    # ---- the commits in the range
    rc, out, _ = git(["log", "--format=%x1e%H%x1f%ae%x1f%ce%x1f%s%x1f%B", "%s..HEAD" % base_ref])
    records = [r for r in out.split("\x1e") if r.strip()] if rc == 0 else []
    ai, personal, noreply, offdomain, longsub, wip = [], [], [], [], [], []
    work_domains = os.environ.get("PREFLIGHT_WORK_DOMAINS", "").lower().split()
    messages = []
    for r in records:
        parts = r.split("\x1f", 4)
        if len(parts) < 5:
            continue
        sha, ae, ce, subj, body = parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3], parts[4]
        messages.append((sha, body))
        label = "%s %s" % (sha[:9], shown(subj, 60))
        if AI_TRAILER.search(body) or AI_FOOTER.search(body):
            ai.append(label)
        for who, addr in (("author", ae), ("committer", ce)):
            dom = addr.lower().rsplit("@", 1)[-1] if "@" in addr else ""
            if dom in PERSONAL_DOMAINS:
                personal.append("%s (%s at %s)" % (sha[:9], who, dom))
            elif dom == "users.noreply.github.com":
                noreply.append("%s (%s)" % (sha[:9], who))
            elif work_domains and dom not in work_domains:
                offdomain.append("%s (%s at %s)" % (sha[:9], who, dom))
        if len(subj) > 72:
            longsub.append(label)
        if re.match(r"(fixup|squash|amend)!|wip\b", subj, re.I):
            wip.append(label)
    n = len(records)
    shaped = [sha[:9] for sha, body in messages if any(rx.search(body) for rx in SECRET_SHAPES[:-1])]
    if shaped:
        say("WARN", "%d commit message(s) hold a secret-shaped string (not printed): %s. A pushed message "
                    "cannot be taken back" % (len(shaped), ", ".join(shaped[:5])))
    if ai:
        say("FAIL", "%d of %d commit(s) carry an AI co-author trailer or a generated-with footer. No such line "
                    "belongs on MOI work. Removing it from a pushed branch is a rewrite (references/rewrite-history.md)" % (len(ai), n))
        for x in ai[:10]:
            note(x)
        if len(ai) > 10:
            note("... and %d more" % (len(ai) - 10))
    elif n:
        say("PASS", "no AI co-author trailer or footer in the %d commit(s) of the range" % n)
    if personal:
        say("FAIL", "%d author or committer address(es) at a personal mail provider. Commits carry the work "
                    "identity only" % len(personal))
        for x in personal[:10]:
            note(x)
    elif n:
        say("PASS", "no personal-provider address among authors and committers")
    if noreply:
        say("WARN", "%d commit(s) use a GitHub no-reply address. Confirm it belongs to your work account: %s"
            % (len(noreply), ", ".join(noreply[:5])))
    if offdomain:
        say("WARN", "%d address(es) not on PREFLIGHT_WORK_DOMAINS: %s" % (len(offdomain), ", ".join(offdomain[:5])))
    elif n and not work_domains:
        say("WARN", "PREFLIGHT_WORK_DOMAINS is not set, so commit addresses cannot be confirmed as work "
                    "addresses. ASK: Rahul for the domain (moi-devrel/references/consent-and-identity.md)")
    if longsub:
        say("WARN", "%d subject(s) longer than 72 characters (upstream x402 asks for 72 or fewer)" % len(longsub))
        for x in longsub[:5]:
            note(x)
    if wip:
        say("WARN", "%d fixup, squash or wip commit(s) are still in the range: %s" % (len(wip), "; ".join(wip[:3])))

    # ---- the working tree
    rc, out, _ = git(["status", "--porcelain=v1", "-z"], text=False)
    entries = [e.decode("utf-8", "replace") for e in out.split(b"\0") if e] if rc == 0 else []
    dirty = [e for e in entries if not e.startswith("??")]
    untracked = [e[3:] for e in entries if e.startswith("??")]
    if dirty:
        say("WARN", "%d uncommitted change(s) in tracked files. They are not part of this push" % len(dirty))
    else:
        say("PASS", "no uncommitted change in tracked files")
    env_untracked = [p for p in untracked if is_env_name(p) and not is_env_template(p)]
    if env_untracked:
        say("WARN", "%d untracked env-named file(s) are not ignored: git add -A would stage them. Add them to "
                    ".gitignore, or never use git add -A" % len(env_untracked))
    if untracked:
        say("WARN", "%d untracked file(s) (not in this push): %s" % (len(untracked), ", ".join(shown(p, 40) for p in untracked[:5])))

    # ---- files in the range
    rc, out, _ = git(["log", "--format=", "--name-only", "-z", "%s..HEAD" % base_ref], text=False)
    all_paths = sorted(set(p.decode("utf-8", "replace") for p in out.split(b"\0") if p.strip())) if rc == 0 else []
    env_in_history = [p for p in all_paths if is_env_name(p) and not is_env_template(p)]
    if env_in_history:
        say("FAIL", "an env-named file is in a commit of the range (name hidden). Never push it. If it held "
                    "a key, that key is exposed: tell the operator to rotate it, then remove the file from "
                    "the history (references/rewrite-history.md)")
    elif all_paths:
        say("PASS", "no env-named file in any commit of the range")
    private = [p for p in all_paths if PRIVATE_LOOKING.search(p)]
    if private:
        say("WARN", "%d file(s) look private (transcript, recording, ledger, review package, handover note). "
                    "Keep them out of a public repository: %s" % (len(private), ", ".join(shown(p, 50) for p in private[:5])))
    generated = [p for p in all_paths if GENERATED.search(p)]
    if generated:
        say("WARN", "%d generated or build file(s) in the range. The docs sites keep generated files out of "
                    "the commit: %s" % (len(generated), ", ".join(shown(p, 50) for p in generated[:5])))

    # ---- secret scan over the committed copy of the changed files and the commit messages
    rc, out, _ = git(["diff", "--name-only", "-z", "--diff-filter=ACMR", "%s...HEAD" % base_ref], text=False)
    changed = [p.decode("utf-8", "replace") for p in out.split(b"\0") if p] if rc == 0 else []
    if not os.path.isfile(SECRET_SCAN):
        say("WARN", "moi-devrel secret-scan.sh was not found, so no secret scan ran")
    elif changed or messages:
        tmp = tempfile.mkdtemp(prefix="ship-preflight-scan-")
        try:
            skipped = 0
            for p in changed:
                if is_env_name(p) or p.startswith("/") or ".." in p.split("/"):
                    skipped += 1
                    continue
                rcb, blob, _ = git(["cat-file", "blob", "HEAD:" + p], text=False)
                if rcb != 0 or len(blob) > 2_000_000:
                    skipped += 1
                    continue
                dest = os.path.join(tmp, "files", p)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, "wb") as fh:
                    fh.write(blob)
            os.makedirs(os.path.join(tmp, "msgs"), exist_ok=True)
            for sha, body in messages:
                with open(os.path.join(tmp, "msgs", sha[:12] + ".txt"), "w", encoding="utf-8") as fh:
                    fh.write(body)
            try:
                scan = subprocess.run(["bash", SECRET_SCAN, tmp], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
            except subprocess.TimeoutExpired:
                scan = None
                say("WARN", "secret-scan.sh did not finish in 120 seconds, so the scan is incomplete")
            hits = [ln for ln in scan.stdout.decode("utf-8", "replace").splitlines() if ln.strip()] if scan else []
            if scan is None:
                pass
            elif scan.returncode == 0:
                say("PASS", "secret-scan.sh found nothing in %d changed file(s) and %d commit message(s). "
                            "It is a backstop, not proof%s" % (len(changed) - skipped, len(messages),
                                                               "; %d file(s) skipped (env-named, binary or large)" % skipped if skipped else ""))
            elif scan.returncode == 1:
                say("FAIL", "secret-scan.sh found %d secret-shaped string(s). Do not push. Read the places "
                            "below (the values are not printed); a real key is exposed and must be rotated" % len(hits))
                for ln in hits[:15]:
                    rel = ln.replace(tmp + os.sep, "").replace(tmp, "")
                    if rel.startswith("msgs" + os.sep):
                        rel = "commit message " + rel[len("msgs" + os.sep):]
                    elif rel.startswith("files" + os.sep):
                        rel = rel[len("files" + os.sep):]
                    note(shown(rel, 110))
            else:
                say("WARN", "secret-scan.sh could not read everything (exit %d), so the scan is incomplete" % scan.returncode)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # ---- the files changed
    rc, out, _ = git(["diff", "--name-status", "-z", "--no-renames", "%s...HEAD" % base_ref], text=False)
    parts = [x.decode("utf-8", "replace") for x in out.split(b"\0") if x] if rc == 0 else []
    pairs = [(parts[i], parts[i + 1]) for i in range(0, len(parts) - 1, 2)]
    rc, stat, _ = git(["diff", "--shortstat", "%s...HEAD" % base_ref])
    print("\nFiles changed against %s (%d)%s" % (shown(base_ref), len(pairs), (": " + stat.strip()) if stat.strip() else ""))
    for st, path in pairs[:80]:
        print("  %s  %s" % (st, shown(path, 110)))
    if len(pairs) > 80:
        print("  ... and %d more" % (len(pairs) - 80))
    if not pairs:
        print("  (none)")

    print("\nSummary: %d FAIL, %d WARN, %d PASS." % (counts["FAIL"], counts["WARN"], counts["PASS"]))
    print("A WARN does not stop the exit code. Read every WARN, and fix or explain it, before the push gate.")
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as exc:  # a clear message and exit 2, never a traceback
        print("ship-preflight: unexpected error (%s): %s" % (type(exc).__name__, mask(str(exc))), file=sys.stderr)
        sys.exit(2)
PY
