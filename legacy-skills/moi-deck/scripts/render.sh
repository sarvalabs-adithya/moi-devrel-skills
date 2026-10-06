#!/usr/bin/env bash
# Render a MOI deck to PDF and check the deck's own script parses.
# Usage: render.sh <deck.html> [output.pdf]
#        render.sh <deck.html> <deck2.html> ...      (each next to its HTML)
set -euo pipefail
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -x "$CHROME" ] || { echo "Chrome not found at $CHROME"; exit 1; }

render() {
  local html=$1 pdf=$2
  local dir base
  dir=$(cd "$(dirname "$html")" && pwd); base=$(basename "$html")
  if command -v node >/dev/null; then
    python3 - "$dir/$base" <<'PY' > /tmp/moi-deck-check.js
import re, sys
s = open(sys.argv[1], encoding='utf-8').read()
m = re.search(r'<script>(.*?)</script>', s, flags=re.S)
sys.stdout.write(m.group(1) if m else '')
PY
    node --check /tmp/moi-deck-check.js \
      || { echo "FAIL: $base has a JavaScript error (usually a real newline, or a missing comma, inside a NOTES string)"; exit 1; }
  fi
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=8000 \
    --print-to-pdf="$pdf" "file://$dir/$base" 2>&1 | grep -E 'bytes written' || true
  if command -v pdfinfo >/dev/null; then
    local slides pages
    slides=$(grep -c '<section class="slide' "$dir/$base")
    pages=$(pdfinfo "$pdf" | awk '/^Pages/{print $2}')
    echo "$base -> $(basename "$pdf"): $slides slides, $pages pages$([ "$slides" = "$pages" ] || echo '   <-- MISMATCH')"
  fi
}

if [ $# -eq 2 ] && [ "${2##*.}" = "pdf" ]; then
  render "$1" "$2"
else
  for html in "$@"; do render "$html" "${html%.html}.pdf"; done
fi
