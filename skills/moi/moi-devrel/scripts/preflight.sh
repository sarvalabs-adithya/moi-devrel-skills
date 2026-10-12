#!/usr/bin/env bash
# preflight.sh: read-only check to run before any commit, pull request or post.
#
# What it checks (one PASS, WARN or FAIL line each):
#   - required tools: git, gh, node, python3 (FAIL if missing);
#     Google Chrome and poppler (WARN if missing, only deck export and PDF checks need them)
#   - git user.name and user.email for the current repository
#   - WARN when the email is at a personal mail provider, or is a GitHub no-reply address
#   - WARN when no work domain is configured, because then the email cannot be checked at all
#   - WARN when a commit template or commit hook would add a Co-Authored-By line or an AI footer
#   - WARN when recent commits already carry an AI co-author line or a "generated with" footer. The
#     assistant names are the same as in moi-devrel/ship/scripts/ship-preflight.sh: Claude, Anthropic, Copilot,
#     ChatGPT, OpenAI, Codex, Gemini and Cursor
#   - the active gh login name (never the token)
#   - the current branch and the origin remote (scheme, host and path only: no user, password,
#     query string or fragment is ever printed)
#
# Usage:   cd <the repository you will commit in>
#          bash "$SKILLS/moi-devrel/scripts/preflight.sh"
#          SKILLS is the folder that holds the moi-* skills. Run it from inside the repository.
#
# Environment variables. Set both once, on your first day, in your shell profile:
#   PREFLIGHT_WORK_DOMAINS="example.org example.com"
#       The mail domains your work address may use (space separated). With it set, any other domain
#       WARNs. Left unset, the email check can only WARN: "cannot confirm". ASK: Rahul for the domain.
#   PREFLIGHT_EXPECT_GH_LOGIN=<login>
#       Your own work GitHub login. If the active gh login differs, preflight FAILs.
#   A personal-provider email is a WARN and the exit code stays 0, so read the lines. Do not gate on
#   the exit code alone.
# Exit codes: 0 no FAIL (WARN lines are allowed), 1 at least one FAIL.
#
# Safety: read-only. It changes nothing and posts nothing. `gh auth status` is the only call that
# may reach GitHub; it reads your own login and creates no activity. Every gh call runs under a
# timeout (PREFLIGHT_GH_TIMEOUT seconds, default 15, using timeout, gtimeout or python3); if gh does
# not answer in time the login is a FAIL, not a guess. gh output is filtered down to the login name,
# so a token can never be printed, and every line printed is masked for secret shapes (key prefixes,
# JWTs, long hex) first. Works under bash 3.2 and zsh.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"

FAILS=0
WARNS=0
GH_TIMEOUT="${PREFLIGHT_GH_TIMEOUT:-15}"
case "$GH_TIMEOUT" in '' | *[!0-9]*) GH_TIMEOUT=15 ;; esac
AI_NAMES='claude|anthropic|copilot|chatgpt|openai|codex|gemini|cursor'
AI_TRAILER_RE="^[[:space:]]*co-authored-by:.*($AI_NAMES)|noreply@anthropic\.com"
AI_FOOTER_RE="generated[[:space:]]+(with|by)[^[:cntrl:]]{0,40}($AI_NAMES)"

# mask: replace secret-shaped runs with <masked> in everything this script prints.
mask() {
  printf '%s' "$*" | sed -E \
    -e 's/sk-[A-Za-z0-9_-]{12,}/<masked>/g' \
    -e 's/gsk_[A-Za-z0-9]{12,}/<masked>/g' \
    -e 's/(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{16,}/<masked>/g' \
    -e 's/github_pat_[A-Za-z0-9_]{16,}/<masked>/g' \
    -e 's/(AKIA|ASIA)[0-9A-Z]{12,}/<masked>/g' \
    -e 's/xox[abprso]-[A-Za-z0-9-]{10,}/<masked>/g' \
    -e 's/eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}/<masked>/g' \
    -e 's/[0-9A-Fa-f]{32,}/<masked>/g'
}
pass() { printf 'PASS  %s\n' "$(mask "$*")"; }
warn() { printf 'WARN  %s\n' "$(mask "$*")"; WARNS=$((WARNS + 1)); }
fail() { printf 'FAIL  %s\n' "$(mask "$*")"; FAILS=$((FAILS + 1)); }

# run_timeout SECONDS cmd args...: prints the command's output (stdout and stderr merged) and returns
# its exit code, or 124 when the time ran out. Uses timeout, gtimeout or python3; if none exists the
# command is not run and 125 is returned, so a gh call is never left without a limit.
run_timeout() {
  local secs="$1"
  shift
  if command -v timeout >/dev/null 2>&1; then
    timeout "$secs" "$@" 2>&1
    return $?
  fi
  if command -v gtimeout >/dev/null 2>&1; then
    gtimeout "$secs" "$@" 2>&1
    return $?
  fi
  if command -v python3 >/dev/null 2>&1; then
    python3 - "$secs" "$@" <<'PYT'
import subprocess
import sys
secs, cmd = float(sys.argv[1]), sys.argv[2:]
try:
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=secs)
    sys.stdout.write(p.stdout.decode("utf-8", "replace"))
    sys.exit(p.returncode)
except subprocess.TimeoutExpired:
    sys.exit(124)
except OSError:
    sys.exit(127)
PYT
    return $?
  fi
  return 125
}

# ---------------------------------------------------------------- tools
version_of() {
  case "$1" in
    git) git --version 2>&1 | head -n 1 ;;
    gh) run_timeout "$GH_TIMEOUT" gh --version | head -n 1 ;;
    node) node --version 2>&1 | head -n 1 ;;
    python3) python3 --version 2>&1 | head -n 1 ;;
  esac
}

for tool in git gh node python3; do
  if command -v "$tool" >/dev/null 2>&1; then
    pass "tool $tool present ($(version_of "$tool"))"
  else
    fail "tool $tool is missing; see references/environment.md"
  fi
done

if command -v node >/dev/null 2>&1; then
  node_major="$(node -p 'process.versions.node.split(".")[0]' 2>/dev/null)"
  case "$node_major" in
    '' | *[!0-9]*) warn "could not read the node major version" ;;
    *)
      if [ "$node_major" -lt 18 ]; then
        warn "node $node_major is older than 18; coco-docs needs 18 or newer"
      fi
      ;;
  esac
fi

if command -v python3 >/dev/null 2>&1; then
  if ! python3 -c 'import zoneinfo' >/dev/null 2>&1; then
    warn "python3 has no zoneinfo module; scripts/time-table.sh needs Python 3.9 or newer"
  fi
fi

chrome=""
if [ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
  chrome="Google Chrome (macOS app)"
else
  for c in google-chrome google-chrome-stable chromium chromium-browser; do
    if command -v "$c" >/dev/null 2>&1; then
      chrome="$c"
      break
    fi
  done
fi
if [ -n "$chrome" ]; then
  pass "Chrome present ($chrome)"
else
  warn "Chrome not found; deck PDF export (headless Chrome) will not work"
fi

missing_poppler=""
for p in pdfinfo pdftotext pdftoppm; do
  command -v "$p" >/dev/null 2>&1 || missing_poppler="$missing_poppler $p"
done
if [ -z "$missing_poppler" ]; then
  pass "poppler present (pdfinfo, pdftotext, pdftoppm)"
else
  warn "poppler tools missing:$missing_poppler; PDF checks will not work"
fi

# ---------------------------------------------------------------- git identity
in_repo=0
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  in_repo=1
  pass "inside a git repository"
else
  warn "not inside a git repository; checking your global git identity only (cd into the repo first)"
fi

git_name="$(git config user.name 2>/dev/null)"
git_email="$(git config user.email 2>/dev/null)"

if [ -z "$git_name" ]; then
  fail "git user.name is not set (git config user.name \"Your Name\")"
else
  pass "git user.name: $git_name"
fi

scope="global"
if [ "$in_repo" = 1 ] && [ -n "$(git config --local user.email 2>/dev/null)" ]; then
  scope="repo-local"
fi

if [ -z "$git_email" ]; then
  fail "git user.email is not set (git config user.email you@work-domain)"
else
  pass "git user.email: $git_email ($scope setting)"
  email_lc="$(printf '%s' "$git_email" | tr 'A-Z' 'a-z')"
  case "$email_lc" in
    *@*) domain="${email_lc##*@}" ;;
    *) domain="" ;;
  esac
  if [ -z "$domain" ]; then
    fail "git user.email does not look like an email address"
  else
    personal=0
    for d in gmail.com googlemail.com yahoo.com yahoo.co.in yahoo.in ymail.com hotmail.com hotmail.co.in outlook.com outlook.in live.com live.in msn.com icloud.com me.com mac.com aol.com proton.me protonmail.com pm.me gmx.com gmx.net yandex.com mail.com rediffmail.com hey.com fastmail.com zoho.com tutanota.com; do
      if [ "$domain" = "$d" ]; then
        personal=1
      fi
    done
    case "$domain" in
      users.noreply.github.com)
        warn "git email is a GitHub no-reply address; confirm it belongs to your work account"
        ;;
      *)
        if [ "$personal" = 1 ]; then
          warn "git email is at a personal mail provider ($domain); commits and PRs must carry your work identity"
        elif [ -n "${PREFLIGHT_WORK_DOMAINS:-}" ]; then
          case " $PREFLIGHT_WORK_DOMAINS " in
            *" $domain "*) pass "git email domain $domain is on your work list" ;;
            *) warn "git email domain $domain is not on your PREFLIGHT_WORK_DOMAINS list" ;;
          esac
        else
          warn "PREFLIGHT_WORK_DOMAINS is not set, so $domain cannot be checked as your work domain. Set it once (export PREFLIGHT_WORK_DOMAINS=\"<work domain>\"); ASK: Rahul for the domain"
        fi
        ;;
    esac
  fi
fi

# ---------------------------------------------------------------- co-author lines
if [ "$in_repo" = 1 ]; then
  coauthor_found=0

  template="$(git config commit.template 2>/dev/null)"
  if [ -n "$template" ]; then
    case "$template" in
      "~/"*) template="$HOME/${template#\~/}" ;;
    esac
    if [ -r "$template" ] && { grep -qi 'co-authored-by' "$template" 2>/dev/null || grep -qiE "$AI_FOOTER_RE|noreply@anthropic\.com" "$template" 2>/dev/null; }; then
      warn "commit template ($(basename "$template")) contains a Co-Authored-By line or an AI footer; remove it"
      coauthor_found=1
    fi
  fi

  hooks_dir="$(git rev-parse --git-path hooks 2>/dev/null)"
  if [ -n "$hooks_dir" ] && [ -d "$hooks_dir" ]; then
    for h in prepare-commit-msg commit-msg post-commit; do
      if [ -f "$hooks_dir/$h" ] && { grep -qi 'co-authored-by' "$hooks_dir/$h" 2>/dev/null || grep -qiE "$AI_FOOTER_RE|noreply@anthropic\.com" "$hooks_dir/$h" 2>/dev/null; }; then
        warn "hook $h can add a Co-Authored-By line or an AI footer; remove it from the hook"
        coauthor_found=1
      fi
    done
  fi

  if [ "$coauthor_found" = 0 ]; then
    pass "no commit template or hook adds a Co-Authored-By line"
  fi

  recent="$(git log -n 20 --format=%B 2>/dev/null | grep -ciE "$AI_TRAILER_RE|$AI_FOOTER_RE")"
  case "$recent" in
    '' | 0) pass "no AI co-author or footer line in the last 20 commits" ;;
    *) warn "$recent line(s) in the last 20 commits name an AI assistant (Claude, Anthropic, Copilot, ChatGPT, OpenAI, Codex, Gemini or Cursor) as co-author or generator; do not rewrite merged history, and fix an open PR only with the operator's yes" ;;
  esac
fi

# ---------------------------------------------------------------- gh login (name only)
if command -v gh >/dev/null 2>&1; then
  gh_raw="$(run_timeout "$GH_TIMEOUT" gh auth status)"
  gh_rc=$?
  gh_parsed="$(printf '%s\n' "$gh_raw" | awk '
    /Logged in to / {
      n = split($0, p, " ")
      for (i = 1; i <= n; i++) {
        if (p[i] == "to" && (p[i + 2] == "account" || p[i + 2] == "as")) {
          host = p[i + 1]; user = p[i + 3]
        }
      }
      if (host == "github.com" && user != "") {
        sub(/[^A-Za-z0-9-].*$/, "", user)
        count++
        if (first == "") first = user
        cur = user
      }
    }
    /Active account:/ {
      has_active = 1
      if ($0 ~ /true/ && cur != "") active = cur
    }
    END {
      if (!has_active) active = first
      printf "%s %d\n", active, count
    }')"
  gh_raw=""
  gh_login="${gh_parsed%% *}"
  gh_count="${gh_parsed##* }"
  if [ "$gh_rc" = 124 ]; then
    fail "gh auth status did not answer in $GH_TIMEOUT seconds (network, or a stuck keychain prompt), so the login is unchecked; run preflight again"
  elif [ "$gh_rc" = 125 ]; then
    fail "no timeout tool (timeout, gtimeout or python3) is available, so the gh call was not run and the login is unchecked"
  elif [ -z "$gh_login" ]; then
    fail "gh is not logged in to github.com (run gh auth login yourself; this skill never does)"
  else
    pass "gh login: $gh_login (github.com)"
    case "$gh_count" in
      '' | 0 | 1) : ;;
      *) warn "gh holds $gh_count github.com accounts; the active one is $gh_login. Confirm it before opening a PR" ;;
    esac
    if [ -n "${PREFLIGHT_EXPECT_GH_LOGIN:-}" ]; then
      want_lc="$(printf '%s' "$PREFLIGHT_EXPECT_GH_LOGIN" | tr 'A-Z' 'a-z')"
      have_lc="$(printf '%s' "$gh_login" | tr 'A-Z' 'a-z')"
      if [ "$want_lc" != "$have_lc" ]; then
        fail "gh login is $gh_login but PREFLIGHT_EXPECT_GH_LOGIN is $PREFLIGHT_EXPECT_GH_LOGIN"
      fi
    fi
  fi
fi

# ---------------------------------------------------------------- branch and remote
if [ "$in_repo" = 1 ]; then
  branch="$(git symbolic-ref --short -q HEAD 2>/dev/null)"
  if [ -z "$branch" ]; then
    warn "detached HEAD; check out a topic branch before committing"
  else
    case "$branch" in
      main | master | develop)
        warn "on branch $branch; work on a topic branch (a merge to main or master can deploy)"
        ;;
      *) pass "branch: $branch" ;;
    esac
  fi
  remote="$(git remote get-url origin 2>/dev/null)"
  if [ -z "$remote" ]; then
    warn "no origin remote; nothing can be pushed from here"
  else
    # Print scheme, host and path only. Drop the fragment and query string first, then any user or
    # password in front of the host, in a URL form (scheme://user:pass@host/path) or a scp form
    # (user@host:path), so a token carried in any of those places can never be printed.
    safe_remote="${remote%%#*}"
    safe_remote="${safe_remote%%\?*}"
    case "$safe_remote" in
      *://*)
        remote_scheme="${safe_remote%%://*}"
        remote_rest="${safe_remote#*://}"
        remote_auth="${remote_rest%%/*}"
        remote_path="${remote_rest#"$remote_auth"}"
        safe_remote="$remote_scheme://${remote_auth##*@}$remote_path"
        ;;
      *@*:*) safe_remote="${safe_remote#*@}" ;;
    esac
    pass "remote origin: $safe_remote"
  fi
fi

printf '\nSummary: %d FAIL, %d WARN.\n' "$FAILS" "$WARNS"
if [ -f "$SCRIPT_DIR/../references/consent-and-identity.md" ]; then
  printf 'Rules behind these checks: references/consent-and-identity.md and references/environment.md\n'
fi

if [ "$FAILS" -gt 0 ]; then
  exit 1
fi
exit 0
