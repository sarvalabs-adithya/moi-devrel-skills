#!/usr/bin/env bash
# render.sh: check a MOI deck, then print it to PDF with headless Chrome.
#
# Usage:  render.sh [--force] <deck.html> [output.pdf]     one deck, optional PDF name
#         render.sh [--force] <deck.html> <deck2.html> ... several decks, each PDF beside its HTML
# Output: one deck + one .pdf argument writes that PDF. A name with a slash is used as given. A bare
#         name (no slash) is written beside the deck, not in the current directory.
#         Otherwise each PDF is written beside its HTML as <name>.pdf. The path written is printed.
# Steps:  1. check-deck.py (refuses to render on any FAIL unless --force is given)
#         2. headless Chrome prints the deck to a temporary file (print CSS: one slide per page)
#         3. counts the pages of that file against the slides. On a match it is moved into place.
#            On a mismatch the existing PDF is left untouched and the bad render is kept next to
#            it as <name>.pdf.rejected (an older .rejected file is overwritten). Exit 1.
#         An existing PDF with the same name is replaced on a match, and the line says (replaced).
# Chrome: $CHROME if set, then the usual macOS and Linux locations. $CHROME_FLAGS adds flags.
# Needs:  python3, Chrome or Chromium. pdfinfo (poppler) for an exact page count.
# Exit:   0 every deck rendered with a matching page count; 1 a deck was refused, failed
#         to render or came out with the wrong page count; 2 bad input (usage, no Chrome, a deck
#         that does not exist, an env file named, or an output folder that does not exist).
#         An env file (.env, .env.*, *.env) is refused and never opened.
# Writes: the PDF (or a .pdf.rejected file), a temporary folder that is deleted afterwards, and
#         Chrome's own state under the user's profile folders (on macOS ~/Library/Application Support/Google/).
# Note:   Chrome is run in the background and stopped by its own process id if it has written
#         the PDF but does not exit within $RENDER_TIMEOUT seconds (default 60).
set -u

here=$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)
force=0
htmls=()
pdfs=()
for a in "$@"; do
  case "$a" in
    --force) force=1 ;;
    -h|--help) sed -n '2,24p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *.pdf) pdfs+=("$a") ;;
    -*) echo "unknown option $a" >&2; exit 2 ;;
    *) htmls+=("$a") ;;
  esac
done
if [ ${#htmls[@]} -eq 0 ]; then
  echo "usage: render.sh [--force] <deck.html> [output.pdf]   (see the header of this script)" >&2; exit 2
fi
if [ ${#pdfs[@]} -gt 1 ] || { [ ${#pdfs[@]} -eq 1 ] && [ ${#htmls[@]} -ne 1 ]; }; then
  echo "a .pdf name is only allowed with exactly one deck: render.sh deck.html name.pdf" >&2; exit 2
fi

# Bad input is exit 2 before anything is rendered.
for h in "${htmls[@]}"; do
  hb=$(basename "$h"); hl=$(printf '%s' "$hb" | tr 'A-Z' 'a-z')
  case "$hl" in
    .env|.envrc|.env.*|*.env|*.env.*)
      echo "render.sh: refusing $hb: an env file can hold keys and is never opened. Pass the deck instead." >&2; exit 2 ;;
  esac
  [ -f "$h" ] || { echo "no such file: $h" >&2; exit 2; }
done
if [ ${#pdfs[@]} -eq 1 ]; then
  case "${pdfs[0]}" in
    */*) [ -d "$(dirname "${pdfs[0]}")" ] || { echo "output folder does not exist: $(dirname "${pdfs[0]}")" >&2; exit 2; } ;;
  esac
fi

find_chrome() {
  if [ -n "${CHROME:-}" ]; then
    [ -x "$CHROME" ] && { echo "$CHROME"; return 0; }
    echo "CHROME is set to '$CHROME' but that is not an executable file" >&2; return 1
  fi
  local c
  for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           "/Applications/Chromium.app/Contents/MacOS/Chromium"; do
    [ -x "$c" ] && { echo "$c"; return 0; }
  done
  for c in google-chrome google-chrome-stable chromium chromium-browser; do
    command -v "$c" >/dev/null 2>&1 && { command -v "$c"; return 0; }
  done
  echo "Chrome not found. Install Google Chrome or Chromium, or set CHROME to the browser binary." >&2
  return 1
}
chrome=$(find_chrome) || exit 2

tmp=$(mktemp -d "${TMPDIR:-/tmp}/moi-deck-render.XXXXXX") || exit 2
trap 'rm -rf "$tmp"' EXIT

count_slides() {
  python3 - "$1" <<'PY'
import re, sys
s = open(sys.argv[1], encoding="utf-8").read()
print(len(re.findall(r'<section\b[^>]*\bclass="[^"]*\bslide\b', s)))
PY
}

count_pages() {
  if command -v pdfinfo >/dev/null 2>&1; then
    pdfinfo "$1" 2>/dev/null | awk '/^Pages:/{print $2}'
  else
    echo "pdfinfo not found, counted page objects instead (install poppler for an exact count)" >&2
    grep -a -c '/Type */Page[^s]' "$1"
  fi
}

rc=0
render_one() {
  local html=$1 pdf=$2
  [ -f "$html" ] || { echo "no such file: $html" >&2; rc=1; return; }
  local dir base script_arg=()
  dir=$(cd "$(dirname "$html")" && pwd); base=$(basename "$html")
  # a bare PDF name (no slash) goes beside the deck, not into the current directory
  case "$pdf" in */*) ;; *) pdf="$dir/$pdf" ;; esac
  # a SCRIPT.md beside the deck, or in the session folder above it, is compared with NOTES
  if [ -f "$dir/SCRIPT.md" ]; then script_arg=(--script "$dir/SCRIPT.md")
  elif [ -f "$dir/../SCRIPT.md" ]; then script_arg=(--script "$dir/../SCRIPT.md"); fi

  echo "== $base"
  if ! python3 "$here/check-deck.py" "$dir/$base" ${script_arg[@]+"${script_arg[@]}"} --layout --chrome "$chrome" --quiet; then
    if [ "$force" -eq 1 ]; then
      echo "WARNING: check-deck.py reported FAIL. Rendering anyway because --force was given."
    else
      echo "REFUSED: not rendering $base. Fix the FAIL lines above and run again."
      echo "         (--force renders anyway; use it only when the operator has said to.)"
      rc=1; return
    fi
  fi

  local out_dir out_base out existed=0
  out_dir=$(cd "$(dirname "$pdf")" 2>/dev/null && pwd) || { echo "output folder does not exist: $(dirname "$pdf")" >&2; rc=1; return; }
  out_base=$(basename "$pdf"); out="$out_dir/$out_base"
  [ -f "$out" ] && existed=1
  local uri
  uri=$(python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).resolve().as_uri())' "$dir/$base")
  local work="$tmp/render-$$-$RANDOM.pdf"
  # shellcheck disable=SC2086
  "$chrome" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=8000 \
    ${CHROME_FLAGS:-} --print-to-pdf="$work" "$uri" >"$tmp/chrome.log" 2>&1 &
  local cpid=$! waited=0 limit=${RENDER_TIMEOUT:-60}
  while kill -0 "$cpid" 2>/dev/null && [ "$waited" -lt "$limit" ]; do sleep 1; waited=$((waited + 1)); done
  if kill -0 "$cpid" 2>/dev/null; then
    echo "note: Chrome was still running after ${limit}s; stopping it (process $cpid)." >&2
    kill "$cpid" 2>/dev/null; sleep 1
  fi
  wait "$cpid" 2>/dev/null
  if [ ! -s "$work" ]; then
    echo "FAILED: Chrome wrote no PDF (an existing $out_base was left as it was). Last lines of its output:" >&2
    tail -n 5 "$tmp/chrome.log" >&2; rc=1; return
  fi
  local slides pages
  slides=$(count_slides "$dir/$base"); pages=$(count_pages "$work")
  if [ "$slides" = "$pages" ]; then
    mv -f "$work" "$out" || { echo "FAILED: could not write $out" >&2; rc=1; return; }
    echo "wrote $out ($([ $existed -eq 1 ] && echo replaced || echo new)): $slides slides, $pages pages, match"
    [ -e "$out.rejected" ] && echo "note: an older rejected render is still there: $out.rejected" >&2
  else
    mv -f "$work" "$out.rejected" || { echo "FAILED: could not write $out.rejected" >&2; rc=1; return; }
    echo "REJECTED: $slides slides but $pages pages, MISMATCH. A malformed <section> or an overflowing slide is the usual cause." >&2
    echo "          The bad render is kept as $out.rejected. $([ $existed -eq 1 ] && echo "The existing $out_base was left untouched." || echo "No $out_base was written.")" >&2
    rc=1
  fi
}

if [ ${#pdfs[@]} -eq 1 ]; then
  for p in "${pdfs[@]}"; do for h in "${htmls[@]}"; do render_one "$h" "$p"; done; done
else
  for h in "${htmls[@]}"; do render_one "$h" "${h%.html}.pdf"; done
fi
exit $rc
