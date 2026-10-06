#!/usr/bin/env bash
# Scaffold a new MOI deck. Usage: new-deck.sh <session-folder> "<Deck title>"
set -euo pipefail
folder=${1:?session folder, e.g. community-call-15}
title=${2:-MOI deck}
skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$folder/deck/assets"
cp "$skill_dir/assets/template.html" "$folder/deck/index.html"
python3 - "$folder/deck/index.html" "$title" <<'PY'
import sys
p, title = sys.argv[1], sys.argv[2]
s = open(p, encoding='utf-8').read()
s = s.replace('<title>MOI deck</title>', '<title>%s</title>' % title)
s = s.replace('Deck title <span class="accent">here</span>', title)
open(p, 'w', encoding='utf-8').write(s)
PY
echo "created $folder/deck/index.html"
echo "next: write the slides, then $skill_dir/scripts/render.sh $folder/deck/index.html"
