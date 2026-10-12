#!/usr/bin/env python3
"""Say what still stands in a MOI test round log before the round can be handed back.

Usage (SKILLS is the folder that holds the moi-* skills, quoted because a path can hold spaces):
    python3 "$SKILLS/moi-devrel/test-round/scripts/test-log-check.py" <test-log.csv> [--allow-bom]

Reads one CSV file and never writes anything. It makes no network call. It refuses an env-named
file (.env, .env.*, *.env). Header, in this order in the template (order does not matter here, extra
columns are allowed): case_id, round, title, kind, performed_by, config, input, expected, output,
outcome, evidence, interaction_hash, receipt_status, node_version, run_at_utc, simulated_what, fix,
retest_of, note. A row whose case_id starts with # is a comment and is skipped. Quote any cell that
contains a comma or a line break.

Vocabulary (any letter case; a value outside it is bad input, exit 2):
    kind          chain      a signed interaction was submitted to devnet in this case
                  read       a read of the node or of the live product, nothing submitted
                  app        product behaviour with no interaction submitted (screen, chat, API refusal)
                  simulated  anything standing in for the real thing (mock, fixture, dry run, replay)
    performed_by  operator, claude or both (blank only while a case is not yet run)
    outcome       pass, fail, blocked, skipped. Blank, not-run or todo means the case has no outcome.

What stands (each list names the case and the reason, never the cell value):
    1. NO OUTCOME                    blank or not-run
    2. PASS WITHOUT EVIDENCE         pass and the evidence cell is empty, a placeholder or under 6 characters
    3. ON-CHAIN CASE WITHOUT A HASH OR ITS CONTEXT
                                     kind chain, outcome pass or fail, and: no hash, a hash that is not a full
                                     0x plus 64 hex digits (an abbreviated hash cannot be looked up), a hash
                                     without 0x, no receipt_status, no node_version like 0.13.0, no
                                     run_at_utc (YYYY-MM-DD HH:MM), or performed_by claude (Claude never
                                     signs). A read case needs run_at_utc.
    4. SIMULATED CASE NOT LABELLED   kind simulated with an empty simulated_what; or another kind whose
                                     simulated_what describes a stand-in; or another kind whose text uses
                                     words such as simulated, mock, dry run, fixture, stub, fake, replay,
                                     canned or fallback while simulated_what is not "none" plus a reason
    5. FAIL WITHOUT THE EXACT OUTPUT OR A FIX
                                     fail with an empty output, or with an empty fix (a fix, an issue
                                     draft or "accepted: <who>, <date>")
    6. NO KIND, OR A BROKEN LINK     kind blank, or retest_of names a case that is not in the log
    7. SECRET-SHAPED VALUE           a cell holds an API key prefix, a JWT, a private key block, a
                                     credential inside a URL, unprefixed hex of 32 or more digits, a long
                                     mixed token or 12 or more short words (a possible recovery phrase).
                                     The cell is named, the value is not printed. Treat the value as exposed.
A 0x-prefixed hex string is read as a public identifier (hash, address, logic id). A private key
written with 0x looks the same, so the check cannot catch it: never paste one.
Then a WARN list that does not change the exit code: ids used twice, a fail with a fix and no passing
retest row, blocked or skipped with no note, a pass with no expected result, no round, performed_by
blank on a pass or fail, no run_at_utc on an app or simulated case.
Secret shapes are masked in everything printed (long hex, key prefixes, JWTs, long mixed tokens, runs
of 12 or more short words), before any text is shortened. The mask is a backstop, not proof.

Exit codes: 0 nothing stands (lists 1 to 7 are empty);
            1 at least one case is in lists 1 to 7;
            2 the input is unreadable or malformed: the file cannot be read, is an env file, a column is
              missing, a row has more cells than the header, the file starts with a byte order mark
              (save as plain UTF-8, or pass --allow-bom), kind, performed_by or outcome is outside the
              vocabulary, or there are no rows at all.
"""
import argparse
import csv
import datetime
import io
import os
import re
import signal
import sys

COLUMNS = ["case_id", "round", "title", "kind", "performed_by", "config", "input", "expected", "output",
           "outcome", "evidence", "interaction_hash", "receipt_status", "node_version", "run_at_utc",
           "simulated_what", "fix", "retest_of", "note"]
KINDS = ["chain", "read", "app", "simulated"]
PERFORMERS = ["operator", "claude", "both"]
OUTCOMES = ["pass", "fail", "blocked", "skipped"]
NO_OUTCOME = frozenset(["", "not-run", "not run", "notrun", "todo", "pending", "tbd", "-"])
PLACEHOLDERS = frozenset(
    ["tbd", "todo", "n/a", "na", "none", "nil", "null", "unknown", "-", "--", "?", "??", "x", "...", "ok",
     "okay", "yes", "pass", "passed", "worked", "works", "done", "fine", "good", "same", "see above", "pending",
     "wip", "tba"])

PUBLIC_ID = re.compile(r"\b0[xX][0-9a-fA-F]{16,}\b")
LONG_HEX = re.compile(r"0[xX][0-9A-Fa-f]{17,}|[0-9A-Fa-f]{24,}")
BARE_HEX = re.compile(r"(?<![0-9A-Za-z])[0-9a-fA-F]{32,}(?![0-9A-Za-z])")
HEX_TOKEN = re.compile(r"0[xX][0-9a-fA-F]*")
FULL_HASH = re.compile(r"0[xX][0-9a-fA-F]{64}")
NODE_VERSION = re.compile(r"\d+\.\d+\.\d+")
RUN_AT = re.compile(r"^(\d{4}-\d{2}-\d{2})[ T](\d{2}):(\d{2})(?::\d{2})?\s*(?:UTC|Z)?$", re.IGNORECASE)
SIM_WORDS = re.compile(
    r"\bsimulat\w*|\bmock\w*|\bdry[- ]?run\w*|\bfixture\w*|\bstub\w*|\bfake\w*|\breplay\w*|\bcanned\b|"
    r"\bfall-?back\b", re.IGNORECASE)

# Same shapes as ledger-status.py in moi-devrel/claim-check, looser than secret-scan.sh on purpose. The last
# pattern (a long mixed token) is applied only after 0x identifiers are removed.
KEY_PREFIX_SHAPES = [
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
]
SECRET_SHAPES = [re.compile(p) for p in KEY_PREFIX_SHAPES + [
    r"-----BEGIN (?:[A-Z]+ )*PRIVATE KEY(?: BLOCK)?-----",
    r"\beyJ[A-Za-z0-9_-]{6,}\.eyJ[A-Za-z0-9_-]{6,}\.[A-Za-z0-9_-]{6,}",
    r"(?<![A-Za-z0-9+/=])(?=[A-Za-z0-9+/=]*[A-Za-z])(?=[A-Za-z0-9+/=]*\d)[A-Za-z0-9+/=]{32,}",
]]
RX_KEY_PREFIX = [re.compile(p) for p in KEY_PREFIX_SHAPES]
RX_PRIVATE_BLOCK = re.compile(r"-----BEGIN (?:[A-Z]+ )*PRIVATE KEY(?: BLOCK)?-----")
RX_JWT = re.compile(r"\beyJ[A-Za-z0-9_-]{6,}\.eyJ[A-Za-z0-9_-]{6,}\.[A-Za-z0-9_-]{6,}")
RX_URL_CRED = re.compile(r"(?<![A-Za-z0-9+.-])[A-Za-z][A-Za-z0-9+.-]{0,20}://[^/\s:@]+:[^@\s/]{3,}@")
RX_MIXED = re.compile(
    r"(?<![A-Za-z0-9+/=])(?=[A-Za-z0-9+/=]*[A-Za-z])(?=[A-Za-z0-9+/=]*\d)[A-Za-z0-9+/=]{32,}")
PHRASE_MIN = 12
PHRASE_STOP = frozenset(
    "after and are been being both but could did does each every for from get got had has her here "
    "him his how its let many may most not our out per see she should some than the their them these "
    "those too using via was were which while who why with would yes your".split())
_PIECE = re.compile(r"[A-Za-z]+|[^A-Za-z]+")


def _phrase_spans(s):
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
    return spans


def mask(s):
    s = LONG_HEX.sub(lambda m: m.group(0)[:6] + "...(masked)", s)
    for rx in SECRET_SHAPES:
        s = rx.sub(lambda m: m.group(0)[:4] + "...(masked)", s)
    for a, b in reversed(_phrase_spans(s)):
        s = s[:a] + "(masked: 12 or more short words, possible recovery phrase)" + s[b:]
    return s


def secret_kinds(cell):
    """Names of the secret shapes in a cell. Never returns the value."""
    found = []
    rest = PUBLIC_ID.sub(" ", cell)          # a 0x identifier is public; a bare hex string may be a key
    if any(rx.search(cell) for rx in RX_KEY_PREFIX):
        found.append("an API key or token prefix")
        for rx in RX_KEY_PREFIX:
            rest = rx.sub(" ", rest)
    if RX_PRIVATE_BLOCK.search(cell):
        found.append("a private key block")
    if RX_JWT.search(cell):
        found.append("a JWT")
        rest = RX_JWT.sub(" ", rest)
    if RX_URL_CRED.search(cell):
        found.append("a credential inside a URL")
    if BARE_HEX.search(rest):
        found.append("unprefixed hex of 32 or more digits (the shape of a private key)")
        rest = BARE_HEX.sub(" ", rest)
    if RX_MIXED.search(rest):
        found.append("a long mixed token")
    if _phrase_spans(cell):
        found.append("12 or more short words (possible recovery phrase)")
    return found


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


def weak(v):
    t = v.strip().strip(".:;").lower()
    return len(v.strip()) < 6 or t in PLACEHOLDERS


def blank_or_placeholder(v):
    t = v.strip().strip(".:;").lower()
    return not t or t in PLACEHOLDERS


def real_run_at(v):
    m = RUN_AT.match(v.strip())
    if not m:
        return False
    try:
        datetime.date.fromisoformat(m.group(1))
    except ValueError:
        return False
    return int(m.group(2)) < 24 and int(m.group(3)) < 60


def hash_problems(cell):
    """Reasons the interaction_hash cell is not one or more full hashes. Empty list means fine."""
    hex_found = HEX_TOKEN.findall(cell)
    bare = re.findall(r"(?<![0-9A-Za-z])[0-9a-fA-F]{64}(?![0-9A-Za-z])", cell)
    problems = []
    if not hex_found and not bare:
        return ["no hash"]
    for t in hex_found:
        if not FULL_HASH.fullmatch(t):
            problems.append("a hash that is not a full 0x plus 64 hex digits (an abbreviated hash cannot be looked up)")
            break
    if bare:
        problems.append("a hash without the 0x prefix")
    return problems


def split_ids(v):
    return [x for x in re.split(r"[\s,;|]+", v.strip()) if x]


def short(r, width=60):
    # mask first: cutting the text short first could leave the front half of a secret
    title = mask(" ".join(r["title"].split()))
    if len(title) > width:
        title = title[:width - 3] + "..."
    return "%s | %s" % (mask(r["case_id"] or "(no id)"), title or "(no title)")


def fail_input(msg):
    print("test-log-check: " + msg, file=sys.stderr)
    return 2


def load(path, allow_bom):
    if is_env_file(path):
        return None, fail_input("refusing to read %s: an env file can hold keys and is never opened"
                                % os.path.basename(path))
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except OSError as e:
        return None, fail_input("cannot read %s: %s" % (path, e.strerror or e))
    if raw.startswith(b"\xef\xbb\xbf"):
        if not allow_bom:
            return None, fail_input("%s starts with a byte order mark. Save the file as plain UTF-8 "
                                    "(not \"CSV UTF-8\"), or run again with --allow-bom" % path)
        raw = raw[3:]
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        return None, fail_input("%s is not UTF-8 text: %s" % (path, e))
    rows, comments = [], 0
    try:
        csv.field_size_limit(8 * 1024 * 1024)
        reader = csv.DictReader(io.StringIO(text, newline=""))
        header = [h.strip() for h in (reader.fieldnames or [])]
        if not header:
            return None, fail_input("%s is empty. Copy templates/test-log.csv and add one row per case" % path)
        missing = [c for c in COLUMNS if c not in header]
        if missing:
            hint = ""
            if len(header) == 1 and ";" in header[0]:
                hint = "\n  the columns look joined by semicolons: save the file comma separated"
            return None, fail_input("the log is missing column(s): %s\n  expected header: %s%s" %
                                    (", ".join(missing), ",".join(COLUMNS), hint))
        for r in reader:
            if None in r:
                return None, fail_input("log line %d has more cells than the header; quote any cell that "
                                        "contains a comma" % reader.line_num)
            r = {(k or "").strip(): (v or "").strip() for k, v in r.items()}
            if not any(r.values()):
                continue
            if r["case_id"].startswith("#"):
                comments += 1
                continue
            r["_line"] = reader.line_num
            where = "log line %d (%s)" % (reader.line_num, mask(r["case_id"] or "no id"))
            k = r["kind"].lower()
            if k and k not in KINDS:
                return None, fail_input("%s: the kind %r is not one of %s (a comma inside a cell that is "
                                        "not quoted shifts every column after it)" %
                                        (where, mask(r["kind"])[:30], ", ".join(KINDS)))
            r["kind"] = k
            p = r["performed_by"].lower()
            if p and p not in PERFORMERS:
                return None, fail_input("%s: performed_by %r is not one of %s" %
                                        (where, mask(r["performed_by"])[:30], ", ".join(PERFORMERS)))
            r["performed_by"] = p
            o = r["outcome"].lower()
            if o in NO_OUTCOME:
                o = ""
            elif o not in OUTCOMES:
                return None, fail_input("%s: the outcome %r is not one of %s (leave it blank until the "
                                        "case is run)" % (where, mask(r["outcome"])[:30], ", ".join(OUTCOMES)))
            r["outcome"] = o
            rows.append(r)
    except csv.Error as e:
        return None, fail_input("cannot parse %s as CSV: %s" % (path, e))
    if not rows:
        return None, fail_input("the log has no rows. Copy templates/test-log.csv and add one row per case")
    return (rows, comments), 0


def analyse(rows):
    ids = [r["case_id"] for r in rows if r["case_id"]]
    idset = set(ids)
    L = {k: [] for k in range(1, 8)}
    warn = []

    def add(n, r, reason):
        L[n].append((r, reason))

    for r in rows:
        o, kind = r["outcome"], r["kind"]
        # 7. secrets, whatever the outcome
        for col in COLUMNS:
            for what in secret_kinds(r.get(col, "")):
                add(7, r, "column %s holds %s. Treat it as exposed" % (col, what))
        # 6. kind and links
        if not kind:
            add(6, r, "kind is blank (chain, read, app or simulated)")
        for target in split_ids(r["retest_of"]):
            if target not in idset:
                add(6, r, "retest_of names a case that is not in the log")
            elif target == r["case_id"]:
                add(6, r, "retest_of names the case itself")
        # 1. outcome
        if not o:
            add(1, r, "no outcome yet")
            continue
        # 2. evidence
        if o == "pass" and weak(r["evidence"]):
            add(2, r, "pass with no evidence a second person could re-check")
        # 3. on-chain
        if kind == "chain" and o in ("pass", "fail"):
            for prob in hash_problems(r["interaction_hash"]):
                add(3, r, prob)
            if blank_or_placeholder(r["receipt_status"]):
                add(3, r, "no receipt_status (read it from the receipt, not from the broadcast)")
            if not NODE_VERSION.search(r["node_version"]):
                add(3, r, "no node_version like 0.13.0 (the net.Version answer)")
            if not real_run_at(r["run_at_utc"]):
                add(3, r, "run_at_utc is missing or not YYYY-MM-DD HH:MM UTC")
            if r["performed_by"] == "claude":
                add(3, r, "performed_by is claude, and Claude never signs: the operator performs a chain case")
            elif not r["performed_by"]:
                add(3, r, "performed_by is blank")
        if kind == "read" and o in ("pass", "fail") and not real_run_at(r["run_at_utc"]):
            add(3, r, "a read proves now only: run_at_utc is missing or not YYYY-MM-DD HH:MM UTC")
        # 4. simulated
        sim = r["simulated_what"]
        sim_none = sim.lower().startswith("none")
        if kind == "simulated":
            if blank_or_placeholder(sim) or sim_none:
                add(4, r, "kind is simulated but simulated_what does not say what stood in for the real thing")
        elif kind:
            if sim and not sim_none:
                add(4, r, "simulated_what describes a stand-in but kind is %s: set kind to simulated, "
                          "or write 'none' and a reason" % kind)
            elif not sim_none:
                hit = [c for c in ("title", "config", "input", "expected", "output", "evidence", "note")
                       if SIM_WORDS.search(r[c])]
                if hit:
                    add(4, r, "the %s cell uses a word such as simulated, mock, fixture or fallback while kind "
                              "is %s: set kind to simulated, or write 'none' and a reason in simulated_what"
                        % (", ".join(hit), kind))
        # 5. fail
        if o == "fail":
            if not r["output"].strip():
                add(5, r, "fail with no exact output (paste the message as it appeared)")
            if blank_or_placeholder(r["fix"]):
                add(5, r, "fail with no fix, issue draft or 'accepted: <who>, <date>'")
        # warnings
        if o in ("blocked", "skipped") and not r["note"]:
            warn.append("%s | %s with no note saying why" % (short(r), o))
        if o == "pass" and not r["expected"]:
            warn.append("%s | pass with no expected result written down" % short(r))
        if not r["round"]:
            warn.append("%s | no round" % short(r))
        if o in ("pass", "fail") and kind != "chain" and not r["performed_by"]:
            warn.append("%s | outcome recorded but performed_by is blank" % short(r))
        if kind in ("app", "simulated") and o in ("pass", "fail") and not real_run_at(r["run_at_utc"]):
            warn.append("%s | no valid run_at_utc" % short(r))
    for i in sorted({i for i in ids if ids.count(i) > 1}):
        warn.append("case_id %s is used more than once" % mask(i))
    for r in rows:
        if not r["case_id"]:
            warn.append("log line %d has no case_id" % r["_line"])
        if r["outcome"] == "fail" and not blank_or_placeholder(r["fix"]) \
                and not r["fix"].lower().startswith(("accepted", "known")):
            passed = any(r["case_id"] in split_ids(x["retest_of"]) and x["outcome"] == "pass" for x in rows)
            if not passed:
                warn.append("%s | fail with a fix and no passing retest row (add a row with retest_of)"
                            % short(r))
    return L, warn


TITLES = {
    1: "1. NO OUTCOME (a case in the plan that was never run, or never recorded)",
    2: "2. PASS WITHOUT EVIDENCE",
    3: "3. ON-CHAIN CASE WITHOUT A HASH OR ITS CONTEXT",
    4: "4. SIMULATED CASE NOT LABELLED AS ONE",
    5: "5. FAIL WITHOUT THE EXACT OUTPUT OR A FIX",
    6: "6. NO KIND, OR A BROKEN LINK",
    7: "7. SECRET-SHAPED VALUE (the value is not printed)",
}


def main():
    ap = argparse.ArgumentParser(
        description="List what still stands in a MOI test round log.",
        epilog="Exit 0 nothing stands, 1 cases to fix, 2 unreadable or malformed input.")
    ap.add_argument("log")
    ap.add_argument("--allow-bom", action="store_true",
                    help="accept a UTF-8 byte order mark at the start of the file")
    args = ap.parse_args()

    loaded, code = load(args.log, args.allow_bom)
    if loaded is None:
        return code
    rows, comments = loaded
    L, warn = analyse(rows)

    print("test-log-check: %s" % os.path.basename(args.log))
    print("cases: %d" % len(rows) + ("   (%d comment row(s) skipped: case_id starts with #)" % comments
                                     if comments else ""))
    print("%-10s %6s %6s %8s %8s %6s" % ("kind", "pass", "fail", "blocked", "skipped", "no outcome"))
    for k in KINDS + [""]:
        sub = [r for r in rows if r["kind"] == k]
        if not sub and k == "":
            continue
        print("%-10s %6d %6d %8d %8d %6d" % (
            k or "(no kind)", *[sum(1 for r in sub if r["outcome"] == o) for o in OUTCOMES],
            sum(1 for r in sub if not r["outcome"])))
    real_pass = sum(1 for r in rows if r["outcome"] == "pass" and r["kind"] in ("chain", "read", "app"))
    sim_pass = sum(1 for r in rows if r["outcome"] == "pass" and r["kind"] == "simulated")
    print("passes on the real devnet or the live product: %d. Passes on something simulated: %d. "
          "Say both in the hand-back." % (real_pass, sim_pass))
    print()

    standing = {}
    for n in range(1, 8):
        print("%s (%d)" % (TITLES[n], len(L[n])))
        for r, reason in L[n]:
            print("  %s | %s" % (short(r), reason))
            standing[id(r)] = 1
        if not L[n]:
            print("  none")
        print()
    print("WARN, does not change the exit code (%d)" % len(warn))
    for w in warn:
        print("  " + w)
    if not warn:
        print("  none")
    print()

    if standing:
        print("RESULT: FAIL, %d case(s) still stand. Not ready to hand back (exit 1)" % len(standing))
        return 1
    print("RESULT: PASS, nothing stands (exit 0). Read the WARN list, the simulated cases and every blocked "
          "or skipped case once more before you say Ready")
    return 0


if __name__ == "__main__":
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)   # a closed pipe such as | head ends quietly
    except (AttributeError, ValueError):
        pass
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as exc:   # bad input must never end in a traceback
        print("test-log-check: unexpected problem reading the log (%s)" % type(exc).__name__, file=sys.stderr)
        sys.exit(2)
