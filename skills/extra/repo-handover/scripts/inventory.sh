#!/usr/bin/env bash
# Read-only inventory of one repo, to seed a handover skill. Never touches a remote.
# Usage: inventory.sh <repo path>
set -u
r=${1:?repo path}; cd "$r" || exit 1
code_env=$(mktemp) || exit 1
doc_env=$(mktemp) || exit 1
trap 'rm -f "$code_env" "$doc_env"' EXIT
echo "== repo";        git remote -v 2>/dev/null | head -2
echo "== branch";      git branch --show-current 2>/dev/null
echo "== last commit"; git log -1 --format='%cd %an %s' --date=short 2>/dev/null
echo "== unpushed";    if git rev-parse --abbrev-ref '@{u}' >/dev/null 2>&1; then git log --oneline '@{u}..' 2>/dev/null | wc -l | tr -d ' '; else echo "no upstream set"; fi
echo "== dirty";       git status --short 2>/dev/null | wc -l | tr -d ' '
echo "== branches";    git branch --format='%(refname:short)' 2>/dev/null | tr '\n' ' '; echo
echo "== authors";     git shortlog -sn --no-merges HEAD 2>/dev/null | head -5
echo "== deploy files"
for f in Dockerfile docker-compose.yml docker-compose.yaml fly.toml vercel.json render.yaml railway.json Procfile; do [ -f "$f" ] && echo "  $f"; done
[ -d .github/workflows ] && ls .github/workflows | sed 's/^/  workflow: /'
echo "== env files present"; ls -a 2>/dev/null | grep -E '^\.env' | tr '\n' ' '; echo
for f in .env.example .env.production.example .env.sample; do
  [ -f "$f" ] && { echo "-- $f names:"; grep -oE '^[A-Z][A-Z_0-9]*' "$f" | sort -u | tr '\n' ' '; echo; }
done
echo "== env names read in code but absent from .env.example"
grep -rhoE 'process\.env\.[A-Z_0-9]+|process\.env\[["'"'"'][A-Z_0-9]+|os\.Getenv\("[A-Z_0-9]+"|os\.environ\[["'"'"'][A-Z_0-9]+|os\.environ\.get\(["'"'"'][A-Z_0-9]+' . --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=.next --exclude-dir=dist 2>/dev/null \
  | grep -oE '[A-Z][A-Z_0-9]{2,}' | sort -u > "$code_env"
if [ -f .env.example ]; then grep -oE '^[A-Z][A-Z_0-9]*' .env.example | sort -u > "$doc_env"; else : > "$doc_env"; fi
comm -23 "$code_env" "$doc_env" | tr '\n' ' '; echo
echo "== docs";        ls docs 2>/dev/null | tr '\n' ' '; ls *.md 2>/dev/null | tr '\n' ' '; echo
echo "== npm scripts"; [ -f package.json ] && python3 -c "import json;print(' '.join(json.load(open('package.json')).get('scripts',{})))"
