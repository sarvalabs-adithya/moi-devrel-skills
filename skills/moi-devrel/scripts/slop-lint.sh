#!/usr/bin/env bash
# slop-lint.sh: flag wording MOI has corrected before, in drafts of blogs, posts, scripts and docs.
#
# Usage:   bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" [--errors-only] <file...>
#          bash "$SKILLS/moi-devrel/scripts/slop-lint.sh" --list-rules
#          SKILLS is the folder that holds the moi-* skills.
# Output:  file:line:rule:excerpt   one line per hit. A rule shown as name(warn) is advisory.
#          A summary goes to stderr.
#          The excerpt is the flagged phrase with a little context, at most 120 characters, and any
#          run of 20 or more characters without a space is replaced by <masked>, so a token or key
#          that sits next to a flagged phrase is never echoed.
#          Fenced code blocks (``` and ~~~): only the em-dash and ai-attribution rules apply inside
#          them, because a PR body or commit message pasted in a fence must still be checked.
#          A fence that is opened and never closed is reported as an error (unclosed-fence) and the
#          lines after it are linted as normal text, never skipped.
#          A line that contains slop-lint:ignore is skipped (use it when a document quotes a
#          wrong form on purpose, for example in a table of wrong and right wording).
#          The placeholder rule is an error: a file with {{x}} (not a JSX prop such as style={{ a: 1 }}), [FILL IN: x], FILL-IN, [Sentence 1: x],
#          <<<, TODO, REPLACE-WITH or a RELEASE_URL, LUMA_URL or CANONICAL_URL token must not ship.
#          Inside a fenced block it is skipped. In a file under a folder named templates it is only a
#          warning, because a template is meant to hold placeholders until it is filled in.
#          An env file (.env, .env.*, *.env, .envrc) is never opened: it can hold keys. Naming one
#          stops the run before any file is read.
# Exit codes: 0 no error-level hit (warnings allowed), 1 at least one error-level hit (an unclosed
#             fence counts), 2 usage error, unreadable file, or an env file was named.
#
# To add or change a rule, edit RULES below. Each entry is
#   (rule id, level "error" or "warn", regex flags "i" for ignore-case or "" for exact case,
#    regex, message). The terminology rows these rules enforce are in references/terminology.md.
# Matching is per line, so a phrase broken across two lines is not caught. Python 3 standard library only.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
export SCRIPT_DIR
exec python3 - "$@" <<'PY'
import os
import re
import sys

# ----------------------------------------------------------------------------
# RULES: the one place to edit. Order does not matter.
# ----------------------------------------------------------------------------
RULES = [
    # -- style (house-style.md) --------------------------------------------
    ("em-dash", "error", "", "\u2014",
     "Em dash. Use a comma, a colon or a full stop."),
    ("not-x-not-y", "error", "i",
     r"(?:^|[.!?:]\s+|[\"\u201c(]\s*)not\s+[^.,;:!?\n]{1,60},\s*not\s+|"
     r"(?:^|[.!?]\s+)not\s+[^.!?\n]{1,40}[.!?]\s+not\s+",
     "Not X, not Y construction. State what is true in a full sentence."),
    ("contrast-frame", "warn", "i",
     r"\b(?:it|this|that)\s+(?:is|was)\s+not\s+(?:just|only|about)\s+[^.;\n]{1,60}[;,]\s*(?:it|this|that)\s+(?:is|was)\b|"
     r"\b(?:it|this|that)\s+(?:isn't|wasn't)\s+(?:just|only|about)\s+[^.;\n]{1,60}[;,.]\s*(?:it|this|that)'?s\b",
     "Contrast frame (it is not X, it is Y). Say the point directly."),
    ("vague-attribution", "warn", "i",
     r"\b(?:most teams|many teams|some say|experts agree|studies show)\b",
     "Vague attribution. Name the source or cut the sentence."),
    ("filler", "warn", "i",
     r"\b(?:it(?:'s| is) worth noting|worth caring about)\b",
     "Filler. Cut it."),
    ("none-configured", "warn", "i",
     r"\bnone of which we configured\b",
     "Misleading framing. Say precisely what the reader has."),
    ("applause-closer", "warn", "i",
     r"\b(?:the floor is yours|open q&a)\b",
     "Closer that hands over the floor. Cut it."),
    ("emoji", "warn", "",
     "[\U0001F300-\U0001FAFF\u2600-\u27bf]",
     "Emoji. MOI posts carry none (brand voice)."),
    ("placeholder", "error", "",
     r"(?<!=)\{\{[^}\n]+\}\}|\[FILL[ -]IN\b|\bFILL-IN\b|\[Sentence \d|<<<|\bTODO\b|\bREPLACE-WITH\b|"
     r"\b(?:RELEASE|LUMA|CANONICAL)_URL\b",
     "Placeholder text must not ship."),
    ("ai-attribution", "error", "i",
     r"co-authored-by:|generated with \[?claude",
     "No AI co-author line or footer on commits, PRs or posts."),
    # -- time and release words ---------------------------------------------
    ("twelve-am-utc", "error", "i",
     r"(?<![\d:])\b(?:12|0?0)(?::00)?\s*(?:am|a\.m\.)\s+utc\b",
     "Write 00:00 UTC with the date and the India time, never 12:00 AM UTC."),
    ("am-pm-utc", "warn", "i",
     r"\b(?!(?:12|0?0)(?::00)?\s*(?:am|a\.m\.)\b)\d{1,2}(?::\d{2})?\s*(?:am|pm)\s+utc\b",
     "Use 24-hour UTC, for example 14:30 UTC."),
    ("rc-as-shipped", "warn", "i",
     r"(?:-rc\d+|release candidate)[^.\n]{0,80}\b(?:latest|stable|shipped|released|generally available)\b|"
     r"\b(?:latest|stable|shipped|released)\b[^.\n]{0,80}(?:-rc\d+|release candidate)",
     "A release candidate is not shipped. Quote the version as tagged and do not call it stable or latest."),
    # -- MOI names and models (terminology.md) -------------------------------
    ("account-centric", "error", "i",
     r"\baccount[- ](?:centric|based)\b",
     "MOI is participant-centric, not account-centric or account-based."),
    ("per-account-chain", "error", "i",
     r"\bper-account\s+(?:chain|sequence|ledger)\b|"
     r"\beach account (?:has|keeps|maintains) (?:its|their|a) (?:own )?(?:chain|ledger)\b|"
     r"\ba chain per account\b|\bevery account has its own chain\b",
     "The ledger is an MDAG of tesseracts. A participant's links are a view of it, not a separate chain."),
    ("serval-labs", "error", "i",
     r"\bserval\s+labs\b",
     "The company is Sarva Labs."),
    ("sarvalabs-one-word", "warn", "",
     r"\bSarvaLabs\b",
     "Write Sarva Labs in prose. sarvalabs is correct only as the GitHub org."),
    ("governance-inverted", "error", "i",
     r"\bgoverned by sarva labs\b|\bsarva labs governs\b|\bMOI Foundation (?:builds|develops|designs)\b",
     "Designed and developed by Sarva Labs, governed by MOI Foundation."),
    ("chain-id", "warn", "i",
     r"\bchain[- ]?id\b",
     "MOI's own identifier is the network ID. Keep chain ID only for another chain's convention."),
    ("voyage-devnet", "error", "i",
     r"\bvoyage\s+devnet\b",
     "Say devnet. Voyage is the explorer, not the network."),
    ("old-network-name", "warn", "",
     r"\b(?:Indus|Babylon)\b",
     "Not the current network. Say devnet."),
    ("fuel-universal", "error", "i",
     r"\bevery\s+(?:action|interaction|transaction|call)\b[^.\n]{0,40}\bcosts?\s+fuel\b",
     "A universal the protocol does not guarantee. Say what this release changes."),
    ("fixed-supply", "error", "i",
     r"\bfixed[- ]supply\b",
     "Say capped supply."),
    ("the-token", "warn", "i",
     r"\b(?:the token|MOI'?s own token)\b",
     "Name KMOI, the native token of the MOI network."),
    ("the-fee", "warn", "i",
     r"\bthe fee\b(?!\s+(?:payer|delegation))",
     "Say fuel, fee payer or fee delegation, whichever you mean."),
    ("participant-is-account", "warn", "i",
     r"\bparticipant[*_]{0,2}:?\s+an account\b",
     "Contested definition. A participant is a person, company or agent whose state an account holds."),
    ("coco-name", "warn", "",
     r"\b(?:CoCo|CocoLang)\b",
     "Write Coco, and Coco (also known as Cocolang) on first mention."),
    ("moipod-caps", "warn", "",
     r"\bMoipod\b",
     "Docs style is MOIPod in prose. Keep moipod in commands and package names."),
    ("js-moi-sdk-case", "warn", "",
     r"\b(?!js-moi-sdk\b)[Jj][Ss]-[Mm][Oo][Ii]-[Ss][Dd][Kk]\b",
     "js-moi-sdk is always lowercase, even at the start of a sentence."),
    ("retired-positioning", "error", "i",
     r"\bnot your context,? not your agent\b",
     "Retired line. Current positioning lines are in terminology.md."),
    ("context-infrastructure", "warn", "i",
     r"\bcontext infrastructure\b",
     "Retired positioning. Current lines are in terminology.md."),
    ("building-in-public", "warn", "i",
     r"\bbuilding in public\b",
     "Retired call branding. The call is The Campfire Chat."),
    ("vercel", "warn", "",
     r"\bVercel\b",
     "MOI left Vercel in August 2026. Check this is not a hosting or deploy claim."),
]
# ----------------------------------------------------------------------------

USAGE = (
    "usage: slop-lint.sh [--errors-only] <file...>\n"
    "       slop-lint.sh --list-rules\n"
    "exit: 0 clean of errors, 1 error-level hit, 2 usage error, unreadable file or env file"
)
FENCE_OPEN = re.compile(r"^\s*(`{3,}|~{3,})")
FENCE_CLOSE = re.compile(r"^\s*(`{3,}|~{3,})\s*$")
IGNORE = re.compile(r"slop-lint:\s*ignore")
# Rules that still apply inside a fenced block.
FENCE_RULES = ("em-dash", "ai-attribution")
# Rules that are only a warning in a file under a folder named templates.
TEMPLATE_WARN = ("placeholder",)
# Any run of this many characters without a space is masked in an excerpt.
MASK_RUN = re.compile(r"\S{20,}")
EXCERPT_MAX = 120


def compile_rules():
    compiled = []
    for rid, level, flags, rx, msg in RULES:
        f = re.IGNORECASE if "i" in flags else 0
        compiled.append((rid, level, re.compile(rx, f), msg))
    return compiled


def find_fences(lines):
    """Return (set of 1-based line numbers inside closed fences, list of line numbers of unclosed openers)."""
    inside, unclosed = set(), []
    i, total = 0, len(lines)
    while i < total:
        m = FENCE_OPEN.match(lines[i])
        if not m:
            i += 1
            continue
        marker = m.group(1)
        j = i + 1
        while j < total:
            c = FENCE_CLOSE.match(lines[j])
            if c and c.group(1)[0] == marker[0] and len(c.group(1)) >= len(marker):
                break
            j += 1
        if j < total:
            inside.update(range(i + 1, j + 2))
            i = j + 1
        else:
            unclosed.append(i + 1)
            i += 1
    return inside, unclosed


def excerpt_for(line, rx, hit):
    """A short excerpt around the hit, with every long unbroken run masked first."""
    safe = MASK_RUN.sub("<masked>", line)
    again = rx.search(safe)
    if again:
        start, end = again.span()
        text = safe[max(0, start - 25):end + 25]
    else:
        text = safe[:60]
    return text.strip().replace("\t", " ")[:EXCERPT_MAX]


def is_env_file(path):
    """An env-named file is never opened: .env, .envrc, .env.*, *.env, anything holding .env."""
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


def in_templates(path):
    parts = os.path.normpath(path).split(os.sep)
    return "templates" in parts[:-1]


def lint_file(path, rules, errors_only):
    errs = warns = 0
    templated = in_templates(path)
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    except OSError as exc:
        sys.stderr.write("slop-lint: cannot read %s: %s\n" % (path, exc.strerror))
        return None
    inside, unclosed = find_fences(lines)
    for opener in unclosed:
        sys.stdout.write(
            "%s:%d:unclosed-fence:code fence opened here is never closed; the lines after it were linted as normal text\n"
            % (path, opener)
        )
        errs += 1
    for number, line in enumerate(lines, 1):
        in_fence = number in inside
        if IGNORE.search(line):
            continue
        for rid, level, rx, msg in rules:
            if templated and rid in TEMPLATE_WARN:
                level = "warn"
            if errors_only and level != "error":
                continue
            if in_fence and rid not in FENCE_RULES:
                continue
            hit = rx.search(line)
            if hit:
                label = rid if level == "error" else rid + "(warn)"
                sys.stdout.write("%s:%d:%s:%s\n" % (path, number, label, excerpt_for(line, rx, hit)))
                if level == "error":
                    errs += 1
                else:
                    warns += 1
    return errs, warns


def main(argv):
    args = argv[1:]
    errors_only = False
    if args and args[0] in ("-h", "--help"):
        sys.stdout.write(USAGE + "\n")
        return 0
    if args and args[0] == "--list-rules":
        for rid, level, flags, rx, msg in RULES:
            sys.stdout.write("%-24s %-5s %s\n" % (rid, level, msg))
        sys.stdout.write("%-24s %-5s %s\n" % ("unclosed-fence", "error", "A code fence is opened and never closed (structural check)."))
        terminology = os.path.join(os.environ.get("SCRIPT_DIR", "."), "..", "references", "terminology.md")
        if os.path.isfile(terminology):
            sys.stdout.write("Why each wording rule exists: references/terminology.md\n")
        return 0
    if args and args[0] == "--errors-only":
        errors_only = True
        args = args[1:]
    if not args:
        sys.stderr.write(USAGE + "\n")
        return 2
    for path in args:
        if is_env_file(path):
            sys.stderr.write(
                "slop-lint: refusing to read %s: an env file can hold keys and is never opened. "
                "Pass the text file instead.\n" % os.path.basename(path)
            )
            return 2
    rules = compile_rules()
    total_err = total_warn = 0
    unreadable = False
    for path in args:
        result = lint_file(path, rules, errors_only)
        if result is None:
            unreadable = True
            continue
        total_err += result[0]
        total_warn += result[1]
    sys.stdout.flush()
    sys.stderr.write("slop-lint: %d error(s), %d warning(s) in %d file(s)\n" % (total_err, total_warn, len(args)))
    if unreadable:
        return 2
    return 1 if total_err else 0


sys.exit(main(sys.argv))
PY
