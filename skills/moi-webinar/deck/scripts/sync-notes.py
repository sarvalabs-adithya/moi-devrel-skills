#!/usr/bin/env python3
"""sync-notes.py: copy a SCRIPT.md into the NOTES array of a MOI deck, so the two stay identical.

Usage:  sync-notes.py <deck.html> <SCRIPT.md> [--confirm]
Does:   for every slide that has a section in SCRIPT.md (header contains SLIDE N), replaces that
        entry of the NOTES array with the section text, escaped as a JavaScript string. Entries
        for slides the script does not cover are left exactly as they are.
        If the deck has more slides than NOTES has entries, it adds an empty entry ("") for each
        missing slide, in slide order, so a new slide does not need a hand edit of NOTES. It
        never adds a TITLES entry: write those by hand and check-deck.py (check e) reminds you.
Safe:   without --confirm it only prints what it would change and writes nothing. With --confirm
        it rewrites the NOTES array in <deck.html> (and nothing else in the file) and says so.
        It refuses an env file (.env, .env.*, *.env) and never opens it.
Exit:   0 done or nothing to do; 1 both files were read and cannot be synced (two sections for one
        slide, or a section for a slide the deck lacks); 2 bad usage, an unreadable or env file, a
        deck with no NOTES array, or a script with no slide sections.
Then:   run check-deck.py <deck.html> --script SCRIPT.md. Check h should read PASS.
"""
import importlib.util
import json
import os
import re
import sys

sys.dont_write_bytecode = True  # importing check-deck.py must not leave a __pycache__ in the skill folder
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("check_deck", os.path.join(here, "check-deck.py"))
cd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cd)


def array_span(src, name):
    """(start, end) of 'var NAME = [ ... ];' in src, skipping string literals; None if absent."""
    m = re.search(r"\b(?:var|let|const)\s+%s\s*=\s*\[" % re.escape(name), src)
    if not m:
        return None
    i, depth = m.end(), 1
    while i < len(src) and depth:
        c = src[i]
        if c in "\"'`":
            _, i, _ = cd._read_string(src, i)
            continue
        if src.startswith("//", i):
            i = src.find("\n", i)
            continue
        depth += (c == "[") - (c == "]")
        i += 1
    if depth:
        return None
    end = i
    if src[end:end + 1] == ";":
        end += 1
    return m.start(), end


def is_env_file(path):
    """An env-named file is never opened: .env, .envrc, .env.*, *.env, anything holding .env."""
    names = [os.path.basename(str(path))]
    try:
        names.append(os.path.basename(os.path.realpath(str(path))))
    except OSError:
        pass
    for n in names:
        low = n.lower()
        if low in (".env", ".envrc") or low.startswith(".env.") or low.endswith(".env") or ".env." in low:
            return True
    return False


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    confirm = "--confirm" in argv
    if len(args) != 2 or any(a.startswith("--") and a != "--confirm" for a in argv):
        print(__doc__, file=sys.stderr)
        return 2
    deck, script = args
    for named in (deck, script):
        if is_env_file(named):
            print("sync-notes: refusing to read %s: an env file can hold keys and is never opened. "
                  "Pass the deck and the script instead." % os.path.basename(named), file=sys.stderr)
            return 2
    try:
        src = open(deck, encoding="utf-8").read()
        text = open(script, encoding="utf-8").read()
    except (OSError, UnicodeDecodeError) as e:
        print("cannot read: %s" % e, file=sys.stderr)
        return 2
    span = array_span(src, "NOTES")
    if not span:
        print("no 'var NOTES = [ ... ]' array found in %s" % deck, file=sys.stderr)
        return 2
    block = src[span[0]:span[1]]
    entries, problems = cd.parse_array(block, "NOTES", src.count("\n", 0, span[0]) + 1)
    sections, dupes = cd.script_sections(text, raw=True)
    if not sections:
        print("no slide sections found in %s (headings must contain SLIDE N)" % script, file=sys.stderr)
        return 2
    if dupes:
        print("two sections for slide(s) %s in the script file" % ", ".join(map(str, sorted(set(dupes)))), file=sys.stderr)
        return 1
    parser = cd.DeckParser()
    parser.feed(src)
    parser.close()
    n_slides = len(parser.slides)
    too_far = [k for k in sections if k > n_slides]
    if too_far:
        print("the script has a section for slide %d but the deck has only %d slide%s; "
              "add the slide to the deck first" % (too_far[0], n_slides, "" if n_slides == 1 else "s"), file=sys.stderr)
        return 1
    pad_from = len(entries) + 1
    total = max(len(entries), n_slides)
    new_texts, changed = [], []
    for k in range(1, total + 1):
        if k in sections:
            if k > len(entries) or cd.norm(entries[k - 1]["text"]) != cd.norm(sections[k]):
                changed.append(k)
            new_texts.append(sections[k])
        elif k <= len(entries):
            new_texts.append(entries[k - 1]["text"])
        else:
            new_texts.append("")
    padded = [k for k in range(pad_from, total + 1) if k not in sections]
    if not changed and not padded and not problems:
        print("nothing to change: NOTES already match the %d sections of %s" % (len(sections), os.path.basename(script)))
        return 0
    none_txt = "none (rewriting only to repair the array)" if problems and not padded else "none"
    print("slides to update: %s" % (", ".join(map(str, changed)) or none_txt))
    if padded:
        print("empty NOTES entries to add for slide%s %s (no script for %s yet)"
              % ("s" if len(padded) > 1 else "", ", ".join(map(str, padded)), "them" if len(padded) > 1 else "it"))
    for p in problems:
        print("repairing: %s" % p)
    t_span = array_span(src, "TITLES")
    if t_span:
        t_entries, _ = cd.parse_array(src[t_span[0]:t_span[1]], "TITLES", src.count("\n", 0, t_span[0]) + 1)
        if t_entries is not None and len(t_entries) != n_slides:
            print("note: TITLES has %d entries for %d slides. Add the missing titles by hand (check e)."
                  % (len(t_entries), n_slides))
    if not confirm:
        print("dry run: nothing written. Run again with --confirm to rewrite the NOTES array in %s." % deck)
        return 0
    body = ",\n".join("      " + json.dumps(t, ensure_ascii=False) for t in new_texts)
    new_block = "var NOTES = [\n%s\n];" % body
    new_src = src[:span[0]] + new_block + src[span[1]:]
    tmp = deck + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(new_src)
    os.replace(tmp, deck)
    print("rewrote the NOTES array in %s (%d entries, %d updated, %d empty added). Review the change, then run check-deck.py."
          % (deck, len(new_texts), len(changed), len(padded)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
