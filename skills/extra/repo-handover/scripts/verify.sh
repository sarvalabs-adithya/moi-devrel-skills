#!/usr/bin/env bash
# Does the handover skill still match the repo? Read-only.
# Usage: verify.sh <repo path> <skill dir>
set -u
r=${1:?repo}; s=${2:?skill dir}
s=$(cd "$s" && pwd) || exit 1   # absolute, because the next line changes directory
cd "$r" || exit 1
code=$(grep -rhoE 'process\.env\.[A-Z_0-9]+|process\.env\[["'"'"'][A-Z_0-9]+|os\.Getenv\("[A-Z_0-9]+"|os\.environ\[["'"'"'][A-Z_0-9]+|os\.environ\.get\(["'"'"'][A-Z_0-9]+' . --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=.next --exclude-dir=dist 2>/dev/null | grep -oE '[A-Z][A-Z_0-9]{2,}' | sort -u)
doc=$(grep -oE '`[A-Z][A-Z_0-9]{2,}`' "$s/references/env.md" 2>/dev/null | tr -d '`' | sort -u)
missing=$(comm -23 <(printf '%s\n' "$code") <(printf '%s\n' "$doc") | sed '/^$/d')
stale=$(comm -13 <(printf '%s\n' "$code") <(printf '%s\n' "$doc") | sed '/^$/d')
if [ -n "$missing" ]; then echo "env vars in code but not documented:"; echo "$missing" | sed 's/^/  /'; else echo "env.md covers every variable the code reads"; fi
if [ -n "$stale" ]; then echo "documented but not read by app code (check runtime/ and scripts/ before deleting):"; echo "$stale" | sed 's/^/  /'; fi
if git rev-parse --abbrev-ref '@{u}' >/dev/null 2>&1; then up=$(git log --oneline '@{u}..' 2>/dev/null | wc -l | tr -d ' '); else up="no upstream set"; fi
echo "branch: $(git branch --show-current), unpushed: $up, dirty: $(git status --short | wc -l | tr -d ' ')"
d=$(grep -oE '[Aa]s of [^|]{0,40}' "$s/references/state.md" 2>/dev/null | head -1); [ -n "$d" ] && echo "state.md: $d"
exit 0
