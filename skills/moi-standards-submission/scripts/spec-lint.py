#!/usr/bin/env python3
"""spec-lint.py: check drafts for an external standard before they go to the internal reviewer or upstream.

Covers the files of a CASA namespace (README.md and caip2.md), an x402 scheme specification, and the
text of a pull request description. Python 3 standard library only. Reads files, never writes one,
never touches the network.

Usage (run from the folder that holds the drafts; SKILLS is the folder that holds the moi-* skills,
quoted because a path can hold spaces):
    python3 "$SKILLS/moi-standards-submission/scripts/spec-lint.py" [options] <file or folder> [more]
    python3 "$SKILLS/moi-standards-submission/scripts/spec-lint.py" --list-rules

A folder is searched for *.md files (not inside .git, node_modules, dist or .cache). With --source it
is also searched for .ts, .tsx, .js, .mjs, .cjs, .json, .yml, .yaml and .txt files (lock files and files
over 2 MB are skipped and counted): the package of an x402 mechanism sends those upstream too. A file that
does not end in .md is read as kind source unless --kind says otherwise. A file whose name marks it as an
env file (.env, .env.*, *.env) is never opened: named on the command line it is an error (exit 2),
found inside a folder it is skipped and counted. A folder that cannot be read is an error (exit 2), never
a silent skip.

Options:
    --kind KIND   casa-readme, casa-caip2, x402-spec, x402-pr, casa-pr, source, internal or other.
                  Default: guessed per .md file from its front matter and first heading, else other;
                  source for any other extension. source is text that leaves the team but has no
                  required headings (code, config, changesets). internal skips the rules that only
                  make sense for text that leaves the team (private source, reviewer names). other
                  runs the generic rules only.
    --source      Also read source and config files found in folders (see above).
    --stale TEXT  Repeatable. Flag every use of TEXT, in prose and in code blocks, as obsolete after
                  a decision (for example moi:devnet after the reference format is chosen).
    --strict      Count warnings as errors for the exit code.
    --list-rules  Print every rule with its level and the kinds it applies to, then exit 0.

Output: path:line:level:rule:excerpt, one per hit. level is error, warn or note. The excerpt is at most
120 characters, taken after secret shapes (long hex, tokens with known prefixes, JWTs, private key
headers, runs of 12 or more short words that could be a recovery phrase) were masked, so a key that
sits next to a flagged phrase is never echoed: a masked value shows only "(masked)", not its first
characters. A summary goes to stderr.
A line that holds spec-lint:ignore (or slop-lint:ignore) is skipped, for a document that quotes a
wrong form on purpose.

Exit codes: 0 no error-level hit (warnings and notes allowed), 1 at least one error-level hit (with
--strict, a warning too), 2 usage error, or a file or folder that is missing, unreadable, not UTF-8,
over 2 MB (when named on the command line) or an env file.

Sources of the checks: CASA CONTRIBUTING, _template and CAIP-2 and CAIP-104 as read on 2026-10-03;
x402 CONTRIBUTING, specs/CONTRIBUTING.md, scheme_impl_template.md and the pull request template as
read on 2026-10-03; the merged scheme specs and the review audit of 2026-09-10; the corrections in
moi-devrel/references/terminology.md. See references/wording.md and references/verification.md.
"""
import datetime
import os
import re
import signal
import sys

try:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (AttributeError, ValueError):
    pass

KINDS = ("casa-readme", "casa-caip2", "x402-spec", "x402-pr", "casa-pr", "source", "internal", "other")
FILING = {"casa-readme", "casa-caip2", "x402-spec", "x402-pr", "casa-pr", "source"}   # text that leaves the team
CASA = {"casa-readme", "casa-caip2"}
X402 = {"x402-spec", "x402-pr"}
MAX_BYTES = 2 * 1024 * 1024
EXCERPT = 120
SOURCE_EXT = (".ts", ".tsx", ".js", ".mjs", ".cjs", ".json", ".yml", ".yaml", ".txt")
SKIP_FILES = ("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "npm-shrinkwrap.json")
SKIP_DIRS = (".git", "node_modules", "dist", ".cache")

# ---------------------------------------------------------------- masking (before any truncation)
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
            spans.append((run[0][0], run[-1][1]))
        del run[:]

    for m in _PIECE.finditer(s):
        t = m.group(0)
        if t[0].isalpha():
            if 3 <= len(t) <= 8 and t.lower() not in PHRASE_STOP:
                run.append((m.start(), m.end()))
            else:
                close()
        elif re.fullmatch(r"[\s,;]+", t):
            continue
        else:
            close()
    close()
    for a, b in reversed(spans):
        s = s[:a] + "(masked: 12 or more short words, possible recovery phrase)" + s[b:]
    return s


def mask(s):
    s = LONG_HEX.sub("(masked)", s)
    for rx in SECRET_SHAPES:
        s = rx.sub("(masked)", s)
    return _mask_phrases(s)


def excerpt(line):
    return " ".join(mask(line).split())[:EXCERPT]


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


# ---------------------------------------------------------------- rules
# (id, level, flags, regex, message, kinds or None for all, where) with where "prose" (outside code
# fences) or "all" (code fences too). A rule listed in SKIP_FOR_INTERNAL does not run for kind internal.
RULES = []


def rule(rid, level, flags, rx, msg, kinds=None, where="prose"):
    RULES.append((rid, level, re.compile(rx, re.I if "i" in flags else 0), msg, kinds, where))


# Placeholders and template leftovers
rule("placeholder-bracket", "error", "i",
     r"\[[^\]\n]*(?:TODO|TBD|TBC|FIXME|XXX|placeholder|fill in|remove this|before filing|to be completed|to confirm)[^\]\n]*\]",  # slop-lint:ignore
     "Bracketed placeholder or note to self left in the text.", where="all")
rule("placeholder-word", "error", "",
     r"\b(?:TODO|TBD|TBC|FIXME)\b",  # slop-lint:ignore
     "Placeholder word left in the text (a URL ending in /pull/TODO counts).", where="all")  # slop-lint:ignore
rule("to-be-completed", "error", "i",
     r"\bto be (?:completed|confirmed|decided|written)\b",
     "A section that says it is not written. State what is required in one or two lines, or write it. Never file a stub.", where="all")
rule("curly-placeholder", "error", "",
     r"\{\{[^}\n]*\}\}",
     "Unfilled {{field}} from a template of this skill.", where="all")  # slop-lint:ignore
rule("template-field", "error", "i",
     r"<[^>\n]*(?:same as name of folder|date created|FirstName|GitHubUsername|namespace common name|name of folder)[^>\n]*>"
     r"|\{(?:non-technical name|namespace common name|name of folder)[^}\n]*\}",
     "Unfilled field from the upstream template.", where="all")
# Typography and paths
rule("em-dash", "error", "",
     chr(0x2014), "Em dash. House default: none in anything you author. Whether the ban covers specs is unsettled (references/open-decisions.md).", where="all")
rule("local-path", "error", "",
     r"(?:/Us" r"ers/|/home/[a-z][\w.-]*/|(?<![\w.])~/|[A-Za-z]:\\Us" r"ers\\|\.claude/)",
     "A path from one person's machine. A reviewer cannot open it.", where="all")
rule("ai-attribution", "error", "i",
     r"co-authored-by:|generated with \[?claude",  # slop-lint:ignore
     "No AI co-author line or footer on commits or PRs (house rule). How to disclose AI assistance in words is an open decision: references/open-decisions.md.", where="all")
# Terms MOI has corrected (moi-devrel/references/terminology.md)
rule("account-centric", "error", "i", r"\baccount[- ](?:centric|based)\b",   # slop-lint:ignore
     "MOI is participant-centric. The account is only the vehicle that represents a participant's state (2026-09-14).")
rule("per-account-chain", "error", "i",   # slop-lint:ignore
     r"\bper-account\s+(?:chain|sequence|ledger)\b|\beach (?:participant )?account (?:has|keeps|maintains|holds) (?:its|their|a) (?:own )?(?:ordered )?(?:chain|ledger|sequence)\b|\ba chain per account\b",
     "The ledger is an MDAG of tesseracts. One participant's links are a view of it, not a separate chain (2026-09-14).")
rule("serval-labs", "error", "i", r"\bserval\s+labs\b",   # slop-lint:ignore
     "The company is Sarva Labs.")
rule("sarvalabs-one-word", "warn", "", r"\bSarvaLabs\b",   # slop-lint:ignore
     "Write Sarva Labs in prose. sarvalabs is right only as the GitHub org.")
rule("governance-inverted", "error", "i",   # slop-lint:ignore
     r"\bgoverned by sarva labs\b|\bsarva labs governs\b|\bMOI Foundation (?:builds|develops|designs)\b",
     "Designed and developed by Sarva Labs, governed by MOI Foundation (2026-09-14).")
rule("voyage-devnet", "error", "i", r"\bvoyage\s+devnet\b",   # slop-lint:ignore
     "Say devnet. Voyage is the explorer and tooling site (2026-09-25).")
rule("old-network-name", "warn", "", r"\b(?:Indus|Babylon)\b",   # slop-lint:ignore
     "Not the current network. Say devnet. Babylon is retired; whether /babylon/ is the same chain as /devnet/ is unknown.")  # slop-lint:ignore
rule("claims-filed", "warn", "i",
     r"\b(?:filed|submitted|registered|accepted)\s+(?:with|to|by|in)\s+(?:the\s+)?(?:Chain\s*Agnostic|CASA)\b",
     "Says the namespace is filed, registered or accepted. As of 2026-10-03 nothing was filed. Write it only once the PR is open, and merged only once it is.", kinds=FILING)
rule("chain-id", "warn", "i", r"\bchain[- ]?id\b",   # slop-lint:ignore
     "MOI's own identifier is the network ID. Keep chain ID only for another chain's convention (2026-09-14).")  # slop-lint:ignore
rule("flat-negative", "warn", "i",   # slop-lint:ignore
     r"\b(?:MOI|the protocol) has no (?:chain[- ]?id|genesis)\b|\bno genesis\b|\bno chain[- ]?id\b",
     "A flat negative that was refuted. Say what is verified: no chain of blocks and no global height; a genesis tesseract exists and is reachable only through a founding account (2026-09-14).")
rule("hedge", "warn", "i",
     r"\b(?:arguably|perhaps|maybe|somewhat|it should be noted|it is worth noting|in a sense|sort of|kind of|basically|hopefully)\b",  # slop-lint:ignore
     "Hedge. Direct, short, no hedging; a paragraph that keeps hedging is usually the problem (2026-09-10). Starter list: extend it with what the reviewer strikes.", kinds=FILING)
# Citations a reader cannot open (rule: only public artefacts in anything public)
rule("private-source", "error", "i",
     r"\bgo-moi\b|\bgo-pisa\b|\bsarvalabs/cocolang\b",
     "Private repository. Cite what a reader can open: js-moi-sdk, js-polo, the docs, the explorer, or behaviour visible on the wire.", kinds=FILING)
rule("private-link", "error", "i",
     r"github\.com/sarvalabs/(?:go-moi|go-pisa|cocolang|moidocs|voyage-docs|coco-docs|voyage|voyage-api|moi-agent-launchpad|agent-explorer|moi-project)\b",
     "Link to a repository that is private as of 2026-10-02. A reviewer cannot open it.", kinds=FILING, where="all")
rule("reviewer-name", "warn", "",
     r"\b(?:Rahul|Gokul|Upendhar|Srikar|Vinay|Prakhar)\b",
     "An internal person is named. Public text carries no reviewer names. (The author line is the one place a person is named.)", kinds=FILING)
# x402 specifics
rule("x-payment-header", "error", "",
     r"\bX-PAYMENT(?:-RESPONSE)?\b",
     "Retired v1 header name. v2 uses PAYMENT-REQUIRED, PAYMENT-SIGNATURE and PAYMENT-RESPONSE.", kinds=X402, where="all")
# CASA style (CONTRIBUTING, read 2026-10-03)
rule("inline-link-casa", "warn", "",
     r"\]\(https?://",
     "CASA style: use a link alias in the text and define [Name]: URL at the end of References.", kinds=CASA)
rule("casa-github-link", "warn", "i",
     r"github\.com/ChainAgnostic/CAIPs",
     "CASA style: link the rendered form on chainagnostic.org, not the git repository.", kinds=CASA, where="all")

LIVE = re.compile(
    r"\blive\b|\bsupported\b|\bsupports\b|\bshipped\b|\bdeployed (?:on|to|at|in)\b|\b(?:is|are|now|already) in production\b|"
    r"\bgenerally available\b|\bat the time of writing\b", re.I)
SOURCE = re.compile(
    r"\bas of \d{4}-\d{2}-\d{2}|\bread \d{4}-\d{2}-\d{2}|\b20\d\d-\d{2}-\d{2}\b|https?://|\]\([^)]+\)|"
    r"\[[^\]\n]+\]\[[^\]\n]*\]|\bsource:|\bchecked:", re.I)
AI_SENTENCE = re.compile(r"\bAI[- ]assist|\bdrafted with AI|\bwritten with AI|\bgenerated (?:by|with) an? (?:AI|LLM)\b|\bAI tool\b", re.I)
IGNORE = re.compile(r"(?:spec|slop)-lint:\s*ignore", re.I)

CAIP104_ORDER = ["namespace-identifier", "title", "author", "resolution", "discussions-to", "status",
                 "review-period-end", "type", "category", "created", "updated", "requires", "replaces",
                 "superseded-by"]
REQUIRED_KEYS = {
    "casa-readme": ["namespace-identifier", "title", "author", "status", "type", "created"],
    "casa-caip2": ["namespace-identifier", "title", "author", "discussions-to", "status", "type", "created"],
}
STATUS_VALUES = {"Draft", "Last Call", "Accepted", "Active", "Abandoned", "Rejected", "Superseded"}
TYPE_VALUES = {"Standards Track", "Informational", "Meta"}

REQUIRED_HEADINGS = {   # (label, predicate on the normalised heading list) with the source in the message
    "casa-readme": [("a first heading starting 'Namespace for'", lambda hs: any(h[0] == 1 and h[1].startswith("namespace for") for h in hs)),
                    ("Rationale", None), ("Governance", None), ("References", None), ("Copyright", None)],
    "casa-caip2": [("a first heading 'CAIP-2'", lambda hs: any(h[0] == 1 and h[1] == "caip-2" for h in hs)),
                   ("Introduction", None), ("Specification", None), ("Semantics", None), ("Syntax", None),
                   ("Resolution Mechanics", None), ("Rationale", None), ("Backwards Compatibility", None),
                   ("Test Cases", None), ("References", None), ("Copyright", None)],
    "x402-spec": [("a first heading starting 'Scheme:'", lambda hs: any(h[0] == 1 and h[1].startswith("scheme:") for h in hs)),
                  ("Summary", None), ("a heading naming the payload", lambda hs: any("payload" in h[1] for h in hs)),
                  ("a heading for verification or settlement", lambda hs: any(("verification" in h[1] or "settlement" in h[1]) for h in hs)),
                  ("Appendix", None)],
    "x402-pr": [("Description", None), ("Tests", None), ("Checklist", None)],
}
EXPECTED_HEADINGS = {   # accepted profiles and merged specs (review audit 2026-09-10): a warning, not a block
    "casa-caip2": ["Security Considerations"],
    "x402-spec": ["Versions supported", "Supported Networks", "Protocol Flow", "PaymentRequirements",
                  "PAYMENT-RESPONSE", "Duplicate Settlement Mitigation", "Security Considerations"],
}
SOURCE_OF_HEADINGS = {
    "casa-readme": "CASA _template/README.md, read 2026-10-03",
    "casa-caip2": "CASA _template/caip2.md, read 2026-10-03",
    "x402-spec": "x402 specs/scheme_impl_template.md and specs/CONTRIBUTING.md, read 2026-10-03",
    "x402-pr": "x402 .github/pull_request_template.md, read 2026-10-03",
}


def norm_heading(t):
    t = re.sub(r"[`*_]", "", t).strip().rstrip(":").strip()
    return re.sub(r"\s+", " ", t).lower()


def parse(lines):
    """Return (frontmatter [(key, value, lineno)], headings [(level, normalised, lineno)], fence flags,
    unclosed-fence line or 0). fence[i] is True for a line inside or on the edge of a code fence."""
    fm, headings = [], []
    i, n = 0, len(lines)
    fm_end = 0
    if n and lines[0].strip() == "---":
        j = 1
        while j < n and lines[j].strip() not in ("---", "..."):
            m = re.match(r"^([A-Za-z][\w-]*)\s*:\s*(.*)$", lines[j])
            if m:
                fm.append((m.group(1), m.group(2).strip(), j + 1))
            j += 1
        if j < n:
            fm_end = j + 1
    fence = [False] * n
    in_fence, marker, fence_line = False, "", 0
    for k in range(fm_end, n):
        m = re.match(r"^\s{0,3}(`{3,}|~{3,})", lines[k])
        if m:
            if not in_fence:
                in_fence, marker, fence_line = True, m.group(1)[0], k + 1
                fence[k] = True
                continue
            if m.group(1)[0] == marker:
                in_fence = False
                fence[k] = True
                continue
        fence[k] = in_fence
        if not in_fence:
            h = re.match(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$", lines[k])
            if h:
                headings.append((len(h.group(1)), norm_heading(h.group(2)), k + 1))
    return fm, headings, fence, fm_end, (fence_line if in_fence else 0)


def guess_kind(path, lines, fm):
    keys = {k: v for k, v, _ in fm}
    ident = keys.get("namespace-identifier", "")
    if ident:
        return "casa-caip2" if ident.strip("\"' ").endswith("-caip2") else "casa-readme"
    for ln in lines[:12]:
        if re.match(r"^#\s+Scheme:", ln):
            return "x402-spec"
    base = os.path.basename(path).lower()
    if "pr-description" in base or "pr_description" in base or "pull_request" in base:
        head = " ".join(lines[:6])
        if re.search(r"ChainAgnostic|CASA", head):
            return "casa-pr"
        if re.search(r"x402", head, re.I):
            return "x402-pr"
    return "other"


def units(lines, fence, fm_end):
    """Paragraph-like units of prose: (first line number, text, current heading)."""
    out, cur, start, heading = [], [], 0, ""
    def flush():
        if cur:
            out.append((start, " ".join(cur), heading))
            del cur[:]
    for i in range(fm_end, len(lines)):
        ln = lines[i]
        s = ln.strip()
        if fence[i] or not s or s.startswith("<!--") or re.match(r"^\[[^\]]+\]:\s*\S", s):
            flush()
            continue
        h = re.match(r"^\s{0,3}#{1,6}\s+(.*?)\s*#*\s*$", ln)
        if h:
            flush()
            heading = norm_heading(h.group(1))
            continue
        if s.startswith("|") or re.match(r"^([-*+]|\d+[.)])\s", s):
            flush()
            out.append((i + 1, s, heading))
            continue
        if not cur:
            start = i + 1
        cur.append(s)
    flush()
    return out


def test_cases(lines, headings, fence, text, want_ns="moi"):
    """CAIP-2 profile: the Syntax regex against the Valid and Invalid cases. Returns (hits, counts)."""
    hits, rx, rx_line = [], None, 0
    in_syntax = False
    for i, ln in enumerate(lines):
        m = re.match(r"^\s{0,3}#{2,4}\s+(.*?)\s*#*\s*$", ln)
        if m and not fence[i]:
            in_syntax = norm_heading(m.group(1)) == "syntax"
        if in_syntax and fence[i] and re.match(r"^\s*\^.*\$\s*$", ln):
            rx, rx_line = ln.strip(), i + 1
            break
    if rx is None:
        return [(1, "testcase-regex", "warn", "No Syntax regex found in a code block that starts with ^ and ends with $, so the test cases were not checked.", "")], (0, 0)
    try:
        cre = re.compile(rx)
    except re.error as e:
        return [(rx_line, "testcase-regex", "error", "The Syntax regex does not compile: %s" % e, "")], (0, 0)
    bound = 4294967295 if re.search(r"32-bit|4294967295", text) else None
    mode, valid, invalid = None, 0, 0
    for i, ln in enumerate(lines):
        m = re.match(r"^\s{0,3}#{2,4}\s+(.*?)\s*#*\s*$", ln)
        if m and not fence[i]:
            t = norm_heading(m.group(1))
            mode = "valid" if t.startswith("valid") else "invalid" if t.startswith("invalid") else None
            continue
        case = None
        if mode and fence[i] and not re.match(r"^\s{0,3}(`{3,}|~{3,})", ln):
            case = ln.split("#", 1)[0].strip()
        elif mode and not fence[i] and ln.lstrip().startswith("|"):
            tm = re.search(r"`([^`\n]*:[^`\n]*)`", ln)
            case = tm.group(1) if tm else None
        if mode and case is not None:
            if not case or ":" not in case:
                continue
            ns, ref = case.split(":", 1)
            ok = ns == want_ns and cre.fullmatch(ref) is not None
            if ok and bound is not None and ref.isdigit():
                ok = int(ref) <= bound
            if mode == "valid":
                valid += 1
                if not ok:
                    hits.append((i + 1, "testcase-mismatch", "error", "Valid case does not match the Syntax regex.", excerpt(case)))
            else:
                invalid += 1
                if ok:
                    hits.append((i + 1, "testcase-mismatch", "error", "Invalid case matches the Syntax regex.", excerpt(case)))
    return hits, (valid, invalid)


def lint_text(path, text, kind_opt, stale):
    hits = []
    lines = text.splitlines()
    fm, headings, fence, fm_end, unclosed = parse(lines)
    kind = kind_opt or guess_kind(path, lines, fm)
    if unclosed:
        hits.append((unclosed, "unclosed-fence", "error", "A code fence is opened and never closed.", ""))

    def skipped(i):
        return IGNORE.search(lines[i]) is not None

    # line rules
    for i, ln in enumerate(lines):
        if skipped(i):
            continue
        for rid, level, rx, msg, kinds, where in RULES:
            if kinds is not None and kind not in kinds:
                continue
            if kind == "internal" and rid in ("private-source", "private-link", "reviewer-name", "hedge"):
                continue
            if where == "prose" and fence[i]:
                continue
            if rx.search(ln):
                hits.append((i + 1, rid, level, msg, excerpt(ln)))
        for t in stale:
            if t in ln:
                hits.append((i + 1, "stale", "error", "Obsolete after a decision: " + t, excerpt(ln)))

    # filing-kind checks on boxes and AI wording
    if kind in ("x402-pr", "casa-pr"):
        for i, ln in enumerate(lines):
            if skipped(i) or fence[i]:
                continue
            if re.match(r"^\s*[-*]\s*\[[ xX]\]", ln) and re.search(r"internal|Rahul|Gokul|review(?:ed)? by", ln, re.I):
                hits.append((i + 1, "internal-checkbox", "error", "An internal-process line. It must not be posted upstream. Delete it after the gate clears.", excerpt(ln)))
            elif re.match(r"^\s*[-*]\s*\[ \]", ln):
                hits.append((i + 1, "open-checkbox", "warn", "Unchecked box in text that will be posted. Tick it only when it is true, or delete the line.", excerpt(ln)))
    if kind in ("x402-pr", "casa-pr"):
        if any(AI_SENTENCE.search(l) for l in lines):
            hits.append((1, "ai-disclosure", "note", "An AI-assistance sentence is present. Its wording is an open decision (references/open-decisions.md); this lint does not rule on it.", ""))
        else:
            hits.append((1, "ai-disclosure", "note", "No AI-assistance sentence found. x402 CONTRIBUTING asks for one when most of a PR was AI-generated; the wording is an open decision (references/open-decisions.md).", ""))

    # statements of live or supported with no source marker
    for lineno, txt, heading in units(lines, fence, fm_end):
        if "versions supported" in heading or IGNORE.search(txt):
            continue
        txt = re.sub(r"supported networks|versions supported", "", txt, flags=re.I)
        m = LIVE.search(txt)
        if m and not SOURCE.search(txt):
            a = max(0, m.start() - 40)
            if a:
                a = txt.find(" ", a - 1) + 1 or a
            hits.append((lineno, "live-no-source", "warn",
                         "States something is live or supported with no source marker (a date written 'as of YYYY-MM-DD' or 'read YYYY-MM-DD', a link or 'source:').", excerpt(txt[a:])))

    # front matter, headings, CASA test cases
    if kind in REQUIRED_KEYS:
        keys = [k for k, _, _ in fm]
        vals = {k: (v, ln) for k, v, ln in fm}
        if not fm:
            hits.append((1, "frontmatter-missing", "error", "No front matter block. CAIP-104: every reference document begins with one.", ""))
        for k in REQUIRED_KEYS[kind]:
            if k not in keys:
                hits.append((1, "frontmatter-missing", "error", "Front matter lacks '%s' (CAIP-104 and the CASA template, read 2026-10-03)." % k, ""))
        known = [k for k in keys if k in CAIP104_ORDER]
        if known != sorted(known, key=CAIP104_ORDER.index):
            hits.append((fm[0][2] if fm else 1, "frontmatter-order", "error", "Front matter keys are out of order. CAIP-104 order: " + ", ".join(CAIP104_ORDER), ""))
        for k in keys:
            if k not in CAIP104_ORDER:
                hits.append((vals[k][1], "frontmatter-unknown", "warn", "Key '%s' is not in the CAIP-104 list." % k, ""))
        if "created" in vals:
            v, ln = vals["created"]
            try:
                datetime.date.fromisoformat(v.strip("\"' "))
            except ValueError:
                hits.append((ln, "frontmatter-date", "error", "created must be an ISO 8601 date (yyyy-mm-dd).", excerpt(v)))
        if "status" in vals and vals["status"][0].strip("\"' ") not in STATUS_VALUES:
            hits.append((vals["status"][1], "frontmatter-value", "error", "status must be one of: " + ", ".join(sorted(STATUS_VALUES)), ""))
        if "type" in vals and vals["type"][0].strip("\"' ") not in TYPE_VALUES:
            if vals["type"][0].strip("\"' ") == "Standard" and kind == "casa-caip2":
                hits.append((vals["type"][1], "frontmatter-value", "warn", "CAIP-104 lists: " + ", ".join(sorted(TYPE_VALUES)) + ". The merged neo, stellar and aptos caip2.md files say Standard (read 2026-10-03).", ""))
            else:
                hits.append((vals["type"][1], "frontmatter-value", "error", "type must be one of: " + ", ".join(sorted(TYPE_VALUES)), ""))
        if "author" in vals and not re.search(r"\(@[\w-]+\)|<[^>]+@[^>]+>", vals["author"][0]):
            hits.append((vals["author"][1], "frontmatter-author", "warn", "author should read 'Name (@githubhandle)' or 'Name <email>'. CASA chases the listed author on the PR.", ""))
        for k, v, ln in fm:
            if re.fullmatch(r"<[^>]*>", v.strip()):
                hits.append((ln, "frontmatter-unfilled", "error", "Value left as a template field.", excerpt(k + ": " + v)))
        if "namespace-identifier" in vals:
            folder = os.path.basename(os.path.dirname(os.path.abspath(path)))
            want = folder + ("-caip2" if kind == "casa-caip2" else "")
            got = vals["namespace-identifier"][0].strip("\"' ")
            if folder and got not in (want, "moi" + ("-caip2" if kind == "casa-caip2" else "")):
                hits.append((vals["namespace-identifier"][1], "frontmatter-identifier", "warn", "namespace-identifier '%s' differs from the folder name ('%s' expected)." % (got, want), ""))
    if kind in REQUIRED_HEADINGS:
        for label, pred in REQUIRED_HEADINGS[kind]:
            ok = pred(headings) if pred else any(h[1] == label.lower() for h in headings)
            if not ok:
                hits.append((1, "heading-missing", "error", "Upstream template requires %s (%s)." % (label, SOURCE_OF_HEADINGS[kind]), ""))
    for label in EXPECTED_HEADINGS.get(kind, []):
        want = label.lower()
        if not any(h[1] == want or h[1].startswith(want) or want in h[1] for h in headings):
            hits.append((1, "heading-expected", "warn", "Accepted profiles or merged specs carry '%s' (review audit 2026-09-10). Add it or decide to leave it out." % label, ""))
    if kind == "x402-spec" and not re.search(r"\bMUST\b", text):
        hits.append((1, "no-must", "warn", "No MUST in a scheme specification. Every settlement rule is testable and in MUST wording.", ""))
    summary = ""
    if kind == "casa-caip2":
        ident = {k: v for k, v, _ in fm}.get("namespace-identifier", "moi-caip2").strip("\"' ")
        th, counts = test_cases(lines, headings, fence, text, re.sub(r"-caip2$", "", ident) or "moi")
        hits.extend(th)
        summary = "test cases: %d valid, %d invalid" % counts
        if counts != (0, 0):
            hits.append((1, "testcase-count", "note", "Syntax regex checked against %d valid and %d invalid cases. Check these counts against the PR text and the decisions log." % counts, ""))
    return kind, hits, summary


def collect(args, with_source):
    files, skipped_env, skipped_big, problems = [], 0, 0, []

    def walk_error(err):
        problems.append("cannot read folder %s: %s" % (err.filename, err.strerror or err))

    for a in args:
        if os.path.isdir(a):
            for root, dirs, names in os.walk(a, onerror=walk_error):
                dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
                for nme in sorted(names):
                    p = os.path.join(root, nme)
                    low = nme.lower()
                    is_md = low.endswith(".md")
                    if not is_md and not (with_source and low.endswith(SOURCE_EXT) and low not in SKIP_FILES):
                        continue
                    if is_env_file(p):
                        skipped_env += 1
                        continue
                    if not is_md:
                        try:
                            if os.path.getsize(p) > MAX_BYTES:
                                skipped_big += 1
                                continue
                        except OSError:
                            pass   # reported when the file is opened
                    files.append(p)
        elif is_env_file(a):
            problems.append("refusing to open %s: env files can hold keys and are never opened" % os.path.basename(a))
        elif os.path.isfile(a):
            files.append(a)
        else:
            problems.append("cannot read %s: no such file or folder" % a)
    return files, skipped_env, skipped_big, problems


def list_rules():
    for rid, level, rx, msg, kinds, where in RULES:
        print("%-22s %-5s %-14s %s" % (rid, level, ",".join(sorted(kinds)) if kinds else "all", msg))
    for rid, level, scope, msg in (
        ("frontmatter-*", "error", "casa-*", "Keys present, in CAIP-104 order, valid status, type and created, author with a handle."),
        ("heading-missing", "error", "casa-*, x402-spec, x402-pr", "Headings the upstream template requires."),
        ("heading-expected", "warn", "casa-caip2, x402-spec", "Headings accepted profiles and merged specs carry."),
        ("testcase-mismatch", "error", "casa-caip2", "Syntax regex against the Valid and Invalid test cases."),
        ("live-no-source", "warn", "all", "live, supported, shipped... with no date, link or source: marker."),
        ("internal-checkbox", "error", "x402-pr, casa-pr", "A checkbox that records an internal review."),
        ("open-checkbox", "warn", "x402-pr, casa-pr", "A box still unchecked."),
        ("ai-disclosure", "note", "x402-pr, casa-pr", "Reports whether an AI-assistance sentence exists. Never blocks."),
        ("stale", "error", "all", "Every use of a --stale TEXT."),
        ("unclosed-fence", "error", "all", "A code fence never closed."),
    ):
        print("%-22s %-5s %-14s %s" % (rid, level, scope, msg))


def main(argv):
    kind_opt, stale, strict, with_source, paths = None, [], False, False, []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--list-rules":
            list_rules()
            return 0
        if a in ("-h", "--help"):
            print(__doc__)
            return 0
        if a == "--strict":
            strict = True
        elif a == "--source":
            with_source = True
        elif a == "--kind":
            i += 1
            if i >= len(argv) or argv[i] not in KINDS:
                print("spec-lint: --kind needs one of: " + ", ".join(KINDS), file=sys.stderr)
                return 2
            kind_opt = argv[i]
        elif a == "--stale":
            i += 1
            if i >= len(argv) or not argv[i]:
                print("spec-lint: --stale needs the text to flag", file=sys.stderr)
                return 2
            stale.append(argv[i])
        elif a.startswith("--"):
            print("spec-lint: unknown option %s (see --help)" % a, file=sys.stderr)
            return 2
        else:
            paths.append(a)
        i += 1
    if not paths:
        print("usage: spec-lint.py [--kind KIND] [--stale TEXT] [--strict] [--source] <file or folder> [more]", file=sys.stderr)
        return 2
    files, skipped_env, skipped_big, problems = collect(paths, with_source)
    if problems:
        for p in problems:
            print("spec-lint: " + p, file=sys.stderr)
        return 2
    if not files:
        print("spec-lint: no .md files found in the paths given (use --source for code and config files)", file=sys.stderr)
        return 2
    counts = {"error": 0, "warn": 0, "note": 0}
    checked = []
    for p in files:
        try:
            if os.path.getsize(p) > MAX_BYTES:
                print("spec-lint: %s is over 2 MB; not a draft" % p, file=sys.stderr)
                return 2
            with open(p, "rb") as fh:
                raw = fh.read()
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            print("spec-lint: cannot read %s: not UTF-8 text" % p, file=sys.stderr)
            return 2
        except OSError as e:
            print("spec-lint: cannot read %s: %s" % (p, e.strerror or e), file=sys.stderr)
            return 2
        if text.startswith(chr(0xFEFF)):
            text = text[1:]
        if "\x00" in text:
            print("spec-lint: cannot read %s: binary content" % p, file=sys.stderr)
            return 2
        default_kind = None if p.lower().endswith(".md") else "source"
        kind, hits, summary = lint_text(p, text, kind_opt or default_kind, stale)
        checked.append("%s [%s]%s" % (p, kind, (" " + summary) if summary else ""))
        for lineno, rid, level, msg, exc in sorted(hits, key=lambda h: (h[0], h[1])):
            counts[level] += 1
            print("%s:%d:%s:%s:%s" % (p, lineno, level, rid, (exc + " => " + msg) if exc else msg))
    err = counts["error"] + (counts["warn"] if strict else 0)
    print("spec-lint: %d file(s), %d error(s), %d warning(s), %d note(s)%s. Skipped %d env-named file(s) and %d file(s) over 2 MB found in folders."
          % (len(files), counts["error"], counts["warn"], counts["note"], " (strict: warnings count)" if strict else "", skipped_env, skipped_big),
          file=sys.stderr)
    for c in checked:
        print("  checked " + c, file=sys.stderr)
    return 1 if err else 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as exc:   # a clear message, never a traceback
        print("spec-lint: internal error: %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
        sys.exit(2)
