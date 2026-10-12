#!/usr/bin/env bash
# time-table.sh: print one instant in the time zones MOI work uses, in 24-hour form with weekday and date.
#
# Usage:   bash "$SKILLS/moi-devrel/scripts/time-table.sh" "<YYYY-MM-DD HH:MM>" <area/city zone>
#   SKILLS is the folder that holds the moi-* skills. The zone is an IANA area/city name.
#   example: bash "$SKILLS/moi-devrel/scripts/time-table.sh" "2026-09-11 00:00" UTC
#   example: bash "$SKILLS/moi-devrel/scripts/time-table.sh" "2026-09-10 09:15" America/New_York
#   example: bash "$SKILLS/moi-devrel/scripts/time-table.sh" "2026-09-10 12:45" Asia/Dubai
# The time is read in the zone you give. The first line echoes it back as you gave it, then the
# table shows UTC, India, US Eastern, US Pacific, Central Europe and Singapore, then the ISO UTC
# form that the MOI-Webinars scripts/buffer.mjs expects after --at (it must end in Z).
# Zones: UTC, or an area/city name such as America/New_York or Asia/Kolkata. Abbreviations and
# fixed-offset names (EST, EDT, PST, MST, HST, IST, CET, GMT, Etc/GMT+5 and the like) are REJECTED:
# EST is UTC-5 all year, so "9:15 EST" in summer would be converted an hour wrong.
# Exit codes: 0 printed, 2 malformed time, unknown or rejected zone, or a local time that does not exist.
#
# Why it exists: "12:00 AM UTC" was read as noon and two scheduled posts were wrong (2026-09-10).
# Always echo the converted times to the operator before anything is scheduled.
# Uses the Python 3 standard library (zoneinfo, Python 3.9 or newer). Works under bash 3.2 and zsh.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
export SCRIPT_DIR
exec python3 - "$@" <<'PY'
import re
import sys
from datetime import datetime, timezone

try:
    from zoneinfo import ZoneInfo
except ImportError:  # Python older than 3.9
    sys.stderr.write("time-table: needs Python 3.9 or newer (zoneinfo)\n")
    sys.exit(2)

USAGE = (
    'usage: time-table.sh "<YYYY-MM-DD HH:MM>" <area/city zone>\n'
    '  example: time-table.sh "2026-09-11 00:00" UTC\n'
    '  example: time-table.sh "2026-09-10 09:15" America/New_York\n'
    '  example: time-table.sh "2026-09-10 12:45" Asia/Dubai\n'
    "  time is 24-hour; 12-hour forms such as 12:00 AM are rejected\n"
    "  the zone is UTC or an area/city name; abbreviations such as EST, PST or IST are rejected"
)

# Abbreviations and fixed-offset names are not places. Each maps to the area/city zone to use instead.
LEGACY_HINTS = {
    "EST": "America/New_York", "EDT": "America/New_York", "CST": "America/Chicago", "CDT": "America/Chicago",
    "MST": "America/Denver", "MDT": "America/Denver", "PST": "America/Los_Angeles", "PDT": "America/Los_Angeles",
    "HST": "Pacific/Honolulu", "AKST": "America/Anchorage", "AKDT": "America/Anchorage",
    "IST": "Asia/Kolkata for India", "CET": "Europe/Berlin", "CEST": "Europe/Berlin", "EET": "Europe/Athens",
    "WET": "Europe/Lisbon", "GMT": "Europe/London", "BST": "Europe/London", "SGT": "Asia/Singapore",
    "GST": "Asia/Dubai", "JST": "Asia/Tokyo",
}

# Row label, IANA zone. Edit this list to add a zone.
ROWS = [
    ("UTC", "UTC"),
    ("India", "Asia/Kolkata"),
    ("US Eastern", "America/New_York"),
    ("US Pacific", "America/Los_Angeles"),
    ("Central Europe", "Europe/Berlin"),
    ("Singapore", "Asia/Singapore"),
]


def die(message):
    sys.stderr.write("time-table: %s\n%s\n" % (message, USAGE))
    sys.exit(2)


def offset_text(dt):
    off = dt.utcoffset()
    total = int(off.total_seconds() // 60)
    sign = "+" if total >= 0 else "-"
    total = abs(total)
    return "UTC%s%02d:%02d" % (sign, total // 60, total % 60)


def render(dt):
    return "%s %s %s" % (dt.strftime("%a %Y-%m-%d %H:%M"), dt.tzname(), "(" + offset_text(dt) + ")")


def main(argv):
    if len(argv) == 2 and argv[1] in ("-h", "--help"):
        sys.stdout.write(USAGE + "\n")
        return 0
    if len(argv) != 3:
        die("expected a time and a zone")
    stamp, zone_name = argv[1], argv[2]
    if not re.match(r"^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}$", stamp):
        die("malformed time %r" % stamp)
    try:
        naive = datetime.strptime(stamp.replace("T", " "), "%Y-%m-%d %H:%M")
    except ValueError:
        die("not a real date or time: %r" % stamp)
    if zone_name.upper() == "UTC" or zone_name == "Etc/UTC":
        zone_name = "UTC"
    elif "/" not in zone_name or zone_name.startswith("Etc/"):
        hint = LEGACY_HINTS.get(zone_name.upper())
        die(
            "%r is an abbreviation or fixed-offset name, which ignores daylight saving (EST is UTC-5 all year, "
            "so a US Eastern summer time comes out an hour wrong) or means two places (IST). "
            "Use an area/city zone such as America/New_York%s."
            % (zone_name, " (for %s: %s)" % (zone_name, hint) if hint else "")
        )
    try:
        zone = ZoneInfo(zone_name)
    except Exception:
        die("unknown IANA zone %r (examples: UTC, Asia/Kolkata, Asia/Dubai, America/New_York)" % zone_name)

    local = naive.replace(tzinfo=zone)
    as_utc = local.astimezone(timezone.utc)
    if as_utc.astimezone(zone).replace(tzinfo=None) != naive:
        die("%s does not exist in %s (clocks skip forward at that moment)" % (stamp, zone_name))
    note = None
    first = naive.replace(tzinfo=zone, fold=0).utcoffset()
    second = naive.replace(tzinfo=zone, fold=1).utcoffset()
    if first != second:
        note = "NOTE: %s happens twice in %s (clocks go back); the first occurrence is used." % (stamp, zone_name)

    width = max(len(label) for label, _ in ROWS + [("Given", "")])
    out = []
    out.append("%-*s  %s  [%s]" % (width, "Given", render(local), zone_name))
    out.append("-" * (width + 2 + 40))
    for label, name in ROWS:
        out.append("%-*s  %s  [%s]" % (width, label, render(as_utc.astimezone(ZoneInfo(name))), name))
    out.append("%-*s  %s" % (width, "ISO UTC", as_utc.strftime("%Y-%m-%dT%H:%M:%SZ") + "  (the form the MOI-Webinars buffer.mjs --at needs)"))
    if note:
        out.append(note)
    sys.stdout.write("\n".join(out) + "\n")
    return 0


sys.exit(main(sys.argv))
PY
