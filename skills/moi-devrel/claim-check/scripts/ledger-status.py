#!/usr/bin/env python3
"""Say whether a claim ledger is finished: counts per verdict, and every row that still stands.

Usage (SKILLS is the folder that holds the moi-* skills, quoted because a path can hold spaces):
    python3 "$SKILLS/moi-devrel/claim-check/scripts/ledger-status.py" <ledger.csv> [--allow-bom]

Reads one CSV file and never writes anything. It refuses an env-named file (.env, .env.*, *.env).
Header (extra columns are allowed, order does not matter): id,claim,where,type,source,verdict,
checked_by,as_of,note. A row whose id starts with # is a comment and is skipped (the count is
printed). Quote any cell that contains a comma.

Verdicts (any letter case): verified, scoped, argument, cut, unverified.
    verified    needs a source (a placeholder such as TBD, n/a or - is not a source)
    scoped      true only with a stated limit, and the limit is in the note and in the text
    argument    an opinion, labelled as one in the text
    cut         the sentence was removed from the text
    unverified  nobody has checked it yet

Prints the count per verdict, then four lists. A row can be in more than one list.
    1. UNVERIFIED                  verdict unverified
    2. VERIFIED WITHOUT A SOURCE   verdict verified and the source cell is empty or a placeholder
    3. SCOPED WITHOUT A NOTE       verdict scoped and the note cell is empty
    4. CHECKED BY NOBODY           a verdict other than unverified and checked_by empty or "nobody..."
Then a WARN list that does not change the exit code: a verdict row whose as_of is empty or is not a
real YYYY-MM-DD date, an argument or cut row with no note, and ids that are empty or used twice.
Secret shapes are masked in everything printed: long hex strings (a private key has the same shape
as an asset id), common API key and token prefixes, JWTs, long mixed tokens and runs of 12 or more
short words that could be a recovery phrase. The mask is a backstop, not proof.

Exit codes: 0 every row has a verdict that stands (lists 1 to 4 are empty);
            1 at least one row is in lists 1 to 4;
            2 the input is unreadable or malformed: the file cannot be read, a header column is
              missing, a row has more cells than the header, the file starts with a byte order
              mark (an Excel "CSV UTF-8" export; save as plain UTF-8, or pass --allow-bom to
              accept it), a verdict is not one of the five, or there are no rows at all.
"""
import argparse
import csv
import datetime
import io
import os
import re
import signal
import sys

REQUIRED = ["id", "claim", "where", "type", "source", "verdict", "checked_by", "as_of", "note"]
VERDICTS = ["verified", "scoped", "argument", "cut", "unverified"]
LONG_HEX = re.compile(r"0x[0-9A-Fa-f]{17,}|[0-9A-Fa-f]{24,}")
# Same shapes as extract-claims.py, looser than secret-scan.sh on purpose.
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
PLACEHOLDER_SOURCES = frozenset(
    ["tbd", "todo", "n/a", "na", "none", "nil", "null", "unknown", "-", "--", "?", "??", "x", "...",
     "see above", "same", "tba", "pending", "wip"])


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


def is_placeholder(v):
    return v.strip().strip(".:;").lower() in PLACEHOLDER_SOURCES or v.strip().lower() in PLACEHOLDER_SOURCES


def real_date(v):
    try:
        return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", v)) and bool(datetime.date.fromisoformat(v))
    except ValueError:
        return False


def short(r, width=80):
    # mask the whole claim first: cutting it short first could leave the front half of a secret
    claim = mask(" ".join(r["claim"].split()))
    if len(claim) > width:
        claim = claim[:width - 3] + "..."
    return "%s | %s | %s" % (mask(r["id"] or "(no id)"), mask(r["where"] or "(no where)"), claim)


def fail_input(msg):
    print("ledger-status: " + msg, file=sys.stderr)
    return 2


def main():
    ap = argparse.ArgumentParser(
        description="Counts per verdict and every claim-ledger row that still stands.",
        epilog="Exit 0 every row stands, 1 rows to fix, 2 unreadable or malformed input.")
    ap.add_argument("ledger")
    ap.add_argument("--allow-bom", action="store_true",
                    help="accept a UTF-8 byte order mark at the start of the file")
    args = ap.parse_args()

    if is_env_file(args.ledger):
        return fail_input("refusing to read %s: an env file can hold keys and is never opened"
                          % os.path.basename(args.ledger))
    try:
        with open(args.ledger, "rb") as fh:
            raw = fh.read()
    except OSError as e:
        return fail_input("cannot read %s: %s" % (args.ledger, e))
    if raw.startswith(b"\xef\xbb\xbf"):
        if not args.allow_bom:
            return fail_input("%s starts with a byte order mark. Save the file as plain UTF-8 "
                              "(not \"CSV UTF-8\"), or run again with --allow-bom" % args.ledger)
        raw = raw[3:]
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        return fail_input("%s is not UTF-8 text: %s" % (args.ledger, e))

    rows, comments = [], 0
    try:
        reader = csv.DictReader(io.StringIO(text, newline=""))
        header = [h.strip() for h in (reader.fieldnames or [])]
        missing = [c for c in REQUIRED if c not in header]
        if missing:
            hint = ""
            if len(header) == 1 and ";" in header[0]:
                hint = "\n  the columns look joined by semicolons: save the file comma separated"
            return fail_input("the ledger is missing column(s): %s\n  expected header: %s%s" %
                              (", ".join(missing), ",".join(REQUIRED), hint))
        for r in reader:
            if None in r:
                return fail_input("ledger line %d has more cells than the header; quote any cell "
                                  "that contains a comma" % reader.line_num)
            r = {(k or "").strip(): (v or "").strip() for k, v in r.items()}
            if not any(r.values()):
                continue
            if r["id"].startswith("#"):
                comments += 1
                continue
            r["_line"] = reader.line_num
            v = r["verdict"].lower()
            if v not in VERDICTS:
                return fail_input("ledger line %d (%s): the verdict %r is not one of %s" %
                                  (reader.line_num, r["id"] or "no id", r["verdict"],
                                   ", ".join(VERDICTS)))
            r["verdict"] = v
            rows.append(r)
    except csv.Error as e:
        return fail_input("cannot parse %s as CSV: %s" % (args.ledger, e))
    if not rows:
        return fail_input("the ledger has no rows. Run extract-claims.py on the text first")

    counts = {v: sum(1 for r in rows if r["verdict"] == v) for v in VERDICTS}
    unverified = [r for r in rows if r["verdict"] == "unverified"]
    no_source = [r for r in rows if r["verdict"] == "verified"
                 and (not r["source"] or is_placeholder(r["source"]))]
    no_note = [r for r in rows if r["verdict"] == "scoped" and not r["note"]]
    nobody = [r for r in rows if r["verdict"] != "unverified"
              and (not r["checked_by"] or r["checked_by"].lower().startswith("nobody"))]
    no_date = [r for r in rows if r["verdict"] in ("verified", "scoped") and not r["as_of"]]
    bad_date = [r for r in rows if r["verdict"] != "unverified" and r["as_of"] and not real_date(r["as_of"])]
    no_why = [r for r in rows if r["verdict"] in ("argument", "cut") and not r["note"]]
    ids = [r["id"] for r in rows if r["id"]]
    dup_ids = sorted({i for i in ids if ids.count(i) > 1})
    empty_ids = [r for r in rows if not r["id"]]

    print("ledger-status: %s" % args.ledger)
    print("rows: %d" % len(rows) + ("   (%d comment row(s) skipped: id starts with #)" % comments if comments else ""))
    for v in VERDICTS:
        print("  %-10s %d" % (v, counts[v]))
    print()

    def section(title, items):
        print("%s (%d)" % (title, len(items)))
        for r in items:
            print("  " + short(r))
        if not items:
            print("  none")
        print()

    section("1. UNVERIFIED", unverified)
    section("2. VERIFIED WITHOUT A SOURCE (empty, or a placeholder such as TBD)", no_source)
    section("3. SCOPED WITHOUT A NOTE (the limit goes in the note and in the text)", no_note)
    section("4. CHECKED BY NOBODY (checked_by empty or nobody...)", nobody)
    warn = []
    warn += ["%s | no as_of date on a %s row" % (mask(r["id"] or "(no id)"), r["verdict"]) for r in no_date]
    warn += ["%s | as_of %s is not a YYYY-MM-DD date" % (mask(r["id"] or "(no id)"), mask(r["as_of"])[:30])
             for r in bad_date]
    warn += ["%s | the %s row has no note saying why" % (mask(r["id"] or "(no id)"), r["verdict"])
             for r in no_why]
    warn += ["id %s is used more than once" % mask(i) for i in dup_ids]
    warn += ["line %d has no id" % r["_line"] for r in empty_ids]
    print("WARN, does not change the exit code (%d)" % len(warn))
    for w in warn:
        print("  " + w)
    if not warn:
        print("  none")
    print()

    bad = unverified or no_source or no_note or nobody
    if bad:
        print("RESULT: FAIL, %d row(s) still stand. Not ready to hand back (exit 1)" %
              len({id(r) for r in unverified + no_source + no_note + nobody}))
        return 1
    print("RESULT: PASS, every row has a verdict that stands (exit 0). Read the argument and "
          "scoped rows once more: each limit and each label must be in the text")
    return 0


if __name__ == "__main__":
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)   # a closed pipe such as | head ends quietly
    except (AttributeError, ValueError):
        pass
    sys.exit(main())
