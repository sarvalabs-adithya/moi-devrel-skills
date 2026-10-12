#!/usr/bin/env python3
"""Check a branded page, stylesheet or SVG against the MOI design rules that fail silently.

Usage (SKILLS is the folder that holds the moi-* skills, quoted because a path can hold spaces):
    python3 "$SKILLS/moi-devrel/design/scripts/brand-check.py" [--allow-mono] <file> [<file> ...]
    python3 "$SKILLS/moi-devrel/design/scripts/brand-check.py" --list-rules

Reads each file and never writes anything. It reads .html, .htm, .css, .svg, .jsx and .js text. It
refuses an env-named file (.env, .env.*, *.env) without opening it. Output is one line per finding:
    file:line:LEVEL:rule:excerpt
FAIL rules are mechanical faults that break the brand on screen. WARN rules are a prompt to look.
A [Bracketed Placeholder] left in the visible text of an HTML or SVG file, or in an alt, title, content,
aria-label, placeholder or value attribute, is a FAIL (placeholder-bracket): the starters keep their
brackets on purpose, so an untouched starter never passes. Text inside script, style, code, pre and
comments is not read for it, and a bracket that starts with a digit or a lower-case letter (a citation,
an array) is not one.
Excerpts are masked before they are cut: long hex strings, common API key and token prefixes, JWTs,
long mixed tokens and runs of 12 or more short words never appear. A line that contains
"brand-check: ignore" is skipped. A summary goes to stderr, including what the check does not cover.

Exit codes: 0 no FAIL (warnings allowed); 1 at least one FAIL; 2 bad input: a path that is missing,
a directory, an env file, a file that is not UTF-8 text, a file over 5 MB, no argument, or a palette
file (../colors_and_type.css) that cannot be read. Exit 2 wins over 1 so an unread file is never
taken for a clean one.

The palette is read from ../colors_and_type.css (every hex and every rgb triple in it) plus the pale
logo gradient start #DBCEF9. A colour outside that set is a WARN: the rule is "do not invent hues".
A named colour (black, red and so on; white is MOI White and passes) and a colour function the check
cannot compare (hsl, oklch, color-mix) are also a WARN. The font shorthand (font: 300 16px Arial) is
read for its weight, italic and family like the long-hand properties.
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSS_PATH = os.path.join(HERE, "..", "colors_and_type.css")
MAX_BYTES = 5 * 1024 * 1024
TEXT_EXT = (".html", ".htm", ".css", ".svg", ".jsx", ".js")
ALLOWED_WEIGHTS = {"400", "500", "600", "700", "normal", "inherit", "initial", "unset"}
MONO_FAMILIES = ("ui-monospace", "monospace", "menlo", "consolas", "sf mono", "courier", "courier new")

RULES = [
    ("logo-as-received", "FAIL", "The page points at assets/logos/SVG-as-received/. Those files render solid black. Use assets/logos/SVG/ or a PNG."),
    ("svg-no-style", "FAIL", "An SVG uses class cls-1 or cls-2 with no style block, so it renders black as an img. Use the repaired copy in assets/logos/SVG/."),
    ("placeholder-bracket", "FAIL", "A [Bracketed Placeholder] from a starter is still in the page text or an attribute. Replace every bracket with the real words before this ships."),
    ("css-import-order", "FAIL", "An @import comes after another rule. Browsers ignore it, so the fonts it names never load. Make it the first rule."),
    ("font-family", "FAIL", "First font family is not Poppins. MOI uses Poppins exclusively (brand book D1)."),
    ("font-import", "FAIL", "A Google Fonts link or import names a family other than Poppins."),
    ("font-weight", "FAIL", "A weight outside 400, 500, 600 and 700. The book lists Thin, Extra Light, Light, Extra Bold and Black as weights not to use (D1)."),
    ("font-mono", "WARN", "A monospace family. The book is silent on code; the deck and blog use one for code only (references/type.md). Pass --allow-mono once decided."),
    ("font-weight-relative", "WARN", "lighter or bolder lands on a weight you did not choose. Name a weight."),
    ("poppins-not-loaded", "WARN", "The page sets fonts but never links colors_and_type.css or Google Fonts Poppins, so it may fall back."),
    ("colour-not-token", "WARN", "A colour that is not in colors_and_type.css. Use a token, or ask before adding a hue."),
    ("colour-named", "WARN", "A named colour (black, red...) or a colour function (hsl, oklch...) that this check cannot compare with the palette. Use a token."),
    ("italic", "WARN", "Italic. The book does not mention it; the previous operator's skill banned it (house choice)."),
    ("tracking", "WARN", "Letter spacing other than 0. The book allows tracking changes on over-line text only (D3); negative values are never right."),
    ("em-dash", "WARN", "Em dash. House rule: none in anything you author. slop-lint.sh reports it as an error."),
]

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


def is_env_file(path):
    names = [os.path.basename(path)]
    try:
        names.append(os.path.basename(os.path.realpath(path)))
    except OSError:
        pass
    for n in names:
        low = n.lower()
        if low in (".env", ".envrc") or low.startswith(".env.") or low.endswith(".env") or ".env." in low:
            return True
    return False


def norm_hex(h):
    h = h.lstrip("#").upper()
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return h[:6]


HEX_RE = re.compile(r"(?<![&\w])#([0-9A-Fa-f]{8}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})(?![0-9A-Za-z_-])")
RGB_RE = re.compile(r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*(?:,\s*[\d.]+\s*)?\)")


def load_palette():
    try:
        with open(CSS_PATH, "r", encoding="utf-8") as fh:
            css = fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        reason = getattr(exc, "strerror", None) or str(exc)
        print("brand-check: cannot read the palette file ../colors_and_type.css next to this script: %s" % reason,
              file=sys.stderr)
        return None
    hexes = set(norm_hex(m.group(1)) for m in HEX_RE.finditer(css))
    hexes.add("DBCEF9")  # pale logo gradient start
    triples = set((int(a), int(b), int(c)) for a, b, c in RGB_RE.findall(css))
    for h in hexes:
        triples.add((int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)))
    return hexes, triples


FAMILY_CSS_RE = re.compile(r"font-?family\s*:\s*([^;}<>]+)", re.I)
FAMILY_ATTR_RE = re.compile(r"font-?family\s*=\s*([\"'])(.*?)\1", re.I)
FONT_SHORT_RE = re.compile(r"(?<![-\w])font\s*:\s*([^;}<>]+)", re.I)
SIZE_TOKEN_RE = re.compile(r"^(?:\d*\.?\d+(?:px|rem|em|pt|%|vw|vh|ch)(?:/\S+)?|xx-small|x-small|small|medium|large|x-large|xx-large|smaller|larger)$", re.I)
COLOUR_PROP_RE = re.compile(r"(?<![-\w])(?:color|background(?:-color)?|border(?:-(?:top|right|bottom|left))?(?:-color)?|outline(?:-color)?|fill|stroke|caret-color|accent-color|text-decoration-color|stop-color|flood-color)\s*:\s*([^;}<>]+)", re.I)
COLOUR_ATTR_RE = re.compile(r"(?<![-\w])(?:fill|stroke|color|stop-color|flood-color)\s*=\s*[\"']([^\"']+)[\"']", re.I)
COLOUR_FUNC_RE = re.compile(r"(?<![-\w])(?:hsla?|hwb|lab|lch|oklab|oklch|color-mix|color)\(", re.I)
NAMED_COLOURS = frozenset(
    "aliceblue antiquewhite aqua aquamarine azure beige bisque black blanchedalmond blue blueviolet brown "
    "burlywood cadetblue chartreuse chocolate coral cornflowerblue cornsilk crimson cyan darkblue darkcyan "
    "darkgoldenrod darkgray darkgreen darkgrey darkkhaki darkmagenta darkolivegreen darkorange darkorchid "
    "darkred darksalmon darkseagreen darkslateblue darkslategray darkslategrey darkturquoise darkviolet "
    "deeppink deepskyblue dimgray dimgrey dodgerblue firebrick floralwhite forestgreen fuchsia gainsboro "
    "ghostwhite gold goldenrod gray green greenyellow grey honeydew hotpink indianred indigo ivory khaki "
    "lavender lavenderblush lawngreen lemonchiffon lightblue lightcoral lightcyan lightgoldenrodyellow "
    "lightgray lightgreen lightgrey lightpink lightsalmon lightseagreen lightskyblue lightslategray "
    "lightslategrey lightsteelblue lightyellow lime limegreen linen magenta maroon mediumaquamarine "
    "mediumblue mediumorchid mediumpurple mediumseagreen mediumslateblue mediumspringgreen mediumturquoise "
    "mediumvioletred midnightblue mintcream mistyrose moccasin navajowhite navy oldlace olive olivedrab "
    "orange orangered orchid palegoldenrod palegreen paleturquoise palevioletred papayawhip peachpuff peru "
    "pink plum powderblue purple rebeccapurple red rosybrown royalblue saddlebrown salmon sandybrown "
    "seagreen seashell sienna silver skyblue slateblue slategray slategrey snow springgreen steelblue tan "
    "teal thistle tomato turquoise violet wheat whitesmoke yellow yellowgreen".split())
STRIP_FOR_NAMES = re.compile(r"var\([^)]*\)|url\([^)]*\)|#[0-9A-Fa-f]+|--[\w-]+")
WEIGHT_RE = re.compile(r"font-?weight\s*[:=]\s*[\"']?\s*([A-Za-z0-9]+)", re.I)
TRACK_RE = re.compile(r"letter-?spacing\s*[:=]\s*[\"']?\s*(-?\d*\.?\d+)\s*(em|rem|px|%)?", re.I)
ITALIC_RE = re.compile(r"font-?style\s*[:=]\s*[\"']?\s*(italic|oblique)", re.I)
ITALIC_TAG_RE = re.compile(r"<(?:em|i)[\s>]", re.I)
GFONT_RE = re.compile(r"fonts\.googleapis\.com/css2?\?[^\"')\s]*", re.I)
FAMILY_PARAM_RE = re.compile(r"family=([^:&;\"'|]+)")
STYLE_BLOCK_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)


def excerpt(line, pos, width=100):
    safe = mask(line)
    # positions move after masking, so cut around the first occurrence of the matched text if possible
    start = max(0, min(pos, len(safe)) - 30)
    return " ".join(safe[start:start + width].split())


def first_family(value):
    """The first font family named in a CSS value, without quotes. Stops at a comma, a closing quote
    of the attribute that holds the style, or a !important."""
    v = value.strip()
    if v[:1] in ("\"", "'"):
        end = v.find(v[0], 1)
        name = v[1:end] if end != -1 else v[1:]
    else:
        name = re.match(r"[^,\"'!]*", v).group(0)
    return name.split(",")[0].strip().strip("\"'").strip()


def named_colours_in(value):
    """Named colours in a CSS colour value, ignoring var(), url(), hex and custom property names."""
    cleaned = STRIP_FOR_NAMES.sub(" ", value)
    return [w for w in re.findall(r"[A-Za-z]+", cleaned) if w.lower() in NAMED_COLOURS]


def check_import_order(text, findings, name):
    blocks = []
    if name.lower().endswith(".css"):
        blocks.append((text, 0))
    else:
        for m in STYLE_BLOCK_RE.finditer(text):
            blocks.append((m.group(1), m.start(1)))
    for body, offset in blocks:
        clean = COMMENT_RE.sub(lambda m: " " * len(m.group(0)), body)
        brace = clean.find("{")
        for m in re.finditer(r"@import\b", clean):
            if brace != -1 and m.start() > brace:
                line = text.count("\n", 0, offset + m.start()) + 1
                findings.append((line, "css-import-order", "@import after the first rule"))
                break


BRACKET_RE = re.compile(r"\[[A-Z][^\]\n]{2,200}\]")
ATTR_RE = re.compile(r"\b(?:alt|title|content|aria-label|placeholder|value)\s*=\s*(?:\"([^\"]*)\"|'([^']*)')", re.I)


def bracket_findings(text, raw_lines):
    """(line, excerpt) for each [Placeholder] in visible text or a text attribute. Line numbers are kept."""
    def blank(m):
        return "\n" * m.group(0).count("\n")
    t = re.sub(r"<!--.*?-->", blank, text, flags=re.S)
    t = re.sub(r"<(script|style|code|pre)\b.*?</\1\s*>", blank, t, flags=re.S | re.I)
    out = []
    for n, line in enumerate(t.split("\n"), 1):
        for m in ATTR_RE.finditer(line):
            inner = m.group(1) if m.group(1) is not None else m.group(2)
            hit = BRACKET_RE.search(inner)
            if hit:
                out.append((n, hit.start() + m.start(), line))
    visible = re.sub(r"</?[A-Za-z][^>]*>", blank, t)
    for n, line in enumerate(visible.split("\n"), 1):
        for m in BRACKET_RE.finditer(line):
            out.append((n, m.start(), line))
    return [(n, line, pos) for n, pos, line in out if n <= len(raw_lines) and "brand-check: ignore" not in raw_lines[n - 1]]


def check_text(path, text, palette, allow_mono):
    hexes, triples = palette
    findings = []
    lower_name = path.lower()
    if lower_name.endswith(".svg"):
        if re.search(r'class\s*=\s*"cls-\d', text) and not re.search(r"<style", text, re.I):
            findings.append((1, "svg-no-style", "class cls-N used, no style block"))
    check_import_order(text, findings, lower_name)
    lines = text.splitlines()
    uses_fonts = False
    loads_poppins = bool(re.search(r"colors_and_type\.css", text)) or bool(re.search(r"fonts\.googleapis\.com[^\"')]*Poppins", text, re.I))
    for n, line in enumerate(lines, 1):
        if "brand-check: ignore" in line:
            continue
        if "SVG-as-received" in line:
            findings.append((n, "logo-as-received", excerpt(line, line.find("SVG-as-received"))))
        if "\u2014" in line:
            findings.append((n, "em-dash", excerpt(line, line.find("\u2014"))))
        for m in GFONT_RE.finditer(line):
            for fam in FAMILY_PARAM_RE.findall(m.group(0)):
                if fam.replace("+", " ").strip().lower() != "poppins":
                    findings.append((n, "font-import", excerpt(line, m.start())))
        fam_values = [(m.start(), m.group(1)) for m in FAMILY_CSS_RE.finditer(line)]
        fam_values += [(m.start(), m.group(2)) for m in FAMILY_ATTR_RE.finditer(line)]
        short_pos = []
        for m in FONT_SHORT_RE.finditer(line):
            toks = [(t.group(0), t.start(), t.end()) for t in re.finditer(r"\S+", m.group(1))]
            size_at = next((i for i, t in enumerate(toks) if SIZE_TOKEN_RE.match(t[0])), None)
            if size_at is None:
                continue
            for text, _, _ in toks[:size_at]:
                tl = text.lower()
                if tl in ("italic", "oblique"):
                    findings.append((n, "italic", excerpt(line, m.start())))
                elif tl in ("lighter", "bolder"):
                    findings.append((n, "font-weight-relative", excerpt(line, m.start())))
                elif (tl.isdigit() and tl not in ALLOWED_WEIGHTS) or tl in (
                        "thin", "light", "black", "heavy", "extrabold", "extralight", "ultralight"):
                    findings.append((n, "font-weight", excerpt(line, m.start())))
            fam_values.append((m.start(), m.group(1)[toks[size_at][2]:].lstrip(" ,")))
        for pos, value in sorted(fam_values):
            uses_fonts = True
            fam = first_family(value)
            low = fam.lower()
            if low in ("poppins", "inherit", "initial", "unset", "") or low.startswith("var("):
                continue
            if low in MONO_FAMILIES:
                if not allow_mono:
                    findings.append((n, "font-mono", excerpt(line, pos)))
            else:
                findings.append((n, "font-family", excerpt(line, pos)))
        for m in WEIGHT_RE.finditer(line):
            w = m.group(1).lower()
            if w in ("lighter", "bolder"):
                findings.append((n, "font-weight-relative", excerpt(line, m.start())))
            elif w.isdigit() and w not in ALLOWED_WEIGHTS:
                findings.append((n, "font-weight", excerpt(line, m.start())))
            elif w in ("thin", "light", "black", "heavy", "extrabold", "extralight", "ultralight"):
                findings.append((n, "font-weight", excerpt(line, m.start())))
        for m in ITALIC_RE.finditer(line):
            findings.append((n, "italic", excerpt(line, m.start())))
        if lower_name.endswith((".html", ".htm", ".jsx")) and ITALIC_TAG_RE.search(line):
            findings.append((n, "italic", excerpt(line, ITALIC_TAG_RE.search(line).start())))
        for m in TRACK_RE.finditer(line):
            try:
                val = float(m.group(1))
            except ValueError:
                continue
            if val != 0.0:
                findings.append((n, "tracking", excerpt(line, m.start())))
        ctx_skip = re.compile(r"(?:href|id|for|xlink:href)\s*=\s*[\"']?$|url\(\s*[\"']?$", re.I)
        for m in HEX_RE.finditer(line):
            if ctx_skip.search(line[max(0, m.start() - 14):m.start()]):
                continue
            h = norm_hex(m.group(1))
            if h not in hexes:
                findings.append((n, "colour-not-token", excerpt(line, m.start())))
        for m in RGB_RE.finditer(line):
            t = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
            if t not in triples:
                findings.append((n, "colour-not-token", excerpt(line, m.start())))
        named = [m for m in list(COLOUR_PROP_RE.finditer(line)) + list(COLOUR_ATTR_RE.finditer(line))
                 if named_colours_in(m.group(1))] + list(COLOUR_FUNC_RE.finditer(line))
        if named:  # one finding per line is enough: the line is what needs reading
            findings.append((n, "colour-named", excerpt(line, min(m.start() for m in named))))
    if lower_name.endswith((".html", ".htm", ".svg")):
        seen = set()
        for n, line, pos in bracket_findings(text, lines):
            if n in seen:
                continue
            seen.add(n)
            findings.append((n, "placeholder-bracket", excerpt(line, pos)))
    if lower_name.endswith((".html", ".htm")) and uses_fonts and not loads_poppins:
        findings.append((1, "poppins-not-loaded", "no link to colors_and_type.css or Google Fonts Poppins"))
    return findings


def main(argv):
    ap = argparse.ArgumentParser(
        description="Check a branded page, stylesheet or SVG against the MOI design rules that fail silently.",
        epilog="Exit 0 no FAIL, 1 a FAIL, 2 bad input.")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--allow-mono", action="store_true", help="do not warn about a monospace family (code only)")
    ap.add_argument("--list-rules", action="store_true", help="print the rules and exit")
    args = ap.parse_args(argv[1:])
    if args.list_rules:
        for rid, level, msg in RULES:
            print("%-22s %-4s %s" % (rid, level, msg))
        return 0
    if not args.files:
        ap.print_usage(sys.stderr)
        print("brand-check: give at least one file", file=sys.stderr)
        return 2
    palette = load_palette()
    if palette is None:
        return 2
    bad = 0
    fails = warns = checked = 0
    for path in args.files:
        if is_env_file(path):
            print("brand-check: refusing %s: an env file can hold keys and is never opened" % os.path.basename(path), file=sys.stderr)
            bad += 1
            continue
        if os.path.isdir(path):
            print("brand-check: %s is a directory; pass the files (for example brand-x/*.html)" % path, file=sys.stderr)
            bad += 1
            continue
        try:
            size = os.path.getsize(path)
            if size > MAX_BYTES:
                print("brand-check: %s is over 5 MB; this check reads text files only" % path, file=sys.stderr)
                bad += 1
                continue
            with open(path, "rb") as fh:
                raw = fh.read()
        except OSError as exc:
            print("brand-check: cannot read %s: %s" % (path, exc.strerror), file=sys.stderr)
            bad += 1
            continue
        if b"\x00" in raw:
            print("brand-check: %s is a binary file; this check reads text files only" % path, file=sys.stderr)
            bad += 1
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            print("brand-check: %s is not UTF-8 text" % path, file=sys.stderr)
            bad += 1
            continue
        if not path.lower().endswith(TEXT_EXT):
            print("brand-check: note: %s has an unusual extension; checking it as text" % path, file=sys.stderr)
        checked += 1
        levels = dict((rid, level) for rid, level, _ in RULES)
        for line, rid, ex in sorted(check_text(path, text, palette, args.allow_mono)):
            print("%s:%d:%s:%s:%s" % (path, line, levels[rid], rid, ex))
            if levels[rid] == "FAIL":
                fails += 1
            else:
                warns += 1
    sys.stdout.flush()
    print("brand-check: %d FAIL, %d WARN in %d file(s)" % (fails, warns, checked), file=sys.stderr)
    print("brand-check: NOT checked: which logo file sits on which ground, contrast, images, the wording "
          "(run slop-lint.sh) and the rendered result. Look at the page.", file=sys.stderr)
    if bad:
        return 2
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
