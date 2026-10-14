#!/usr/bin/env python3
"""Pin every Moinkee file (listed in pinata_pins.json) into another Pinata account, by CID.

Nothing is uploaded: Pinata fetches each file from IPFS by its content hash, so the CIDs stay the same and every
minted token keeps working. The old account must still pin the files while this runs.

  python3 repin-to-pinata.py --dry-run     list what would be pinned, no network, no key
  python3 repin-to-pinata.py --check       only report which of the CIDs the target account already pins
  python3 repin-to-pinata.py               pin the missing ones, then wait until all are pinned

The target account's API key (the JWT) is read at a hidden prompt and never printed or saved. The key needs the
pinByHash and pinList permissions (or admin). A log goes to ~/handover-notes/pinata-repin-log.txt.
"""
import getpass
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request

API = "https://api.pinata.cloud"
HERE = os.path.dirname(os.path.abspath(__file__))
PINS = os.path.join(HERE, "pinata_pins.json")
LOG = os.path.expanduser("~/handover-notes/pinata-repin-log.txt")
WAIT_SECONDS = 15 * 60

try:  # Python from python.org on macOS ships without a CA bundle; certifi has one.
    import certifi
    TLS = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    TLS = ssl.create_default_context()


def log(line):
    print(line)
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + line + "\n")


def load_pins():
    rows = json.load(open(PINS))["rows"]
    out = []
    for r in rows:
        name = (r.get("metadata") or {}).get("name") or r["ipfs_pin_hash"]
        out.append({"cid": r["ipfs_pin_hash"], "name": name, "kind": r.get("mime_type") or "", "size": int(r.get("size") or 0)})
    return out


def call(method, path, jwt, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header("Authorization", "Bearer " + jwt)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60, context=TLS) as resp:
            return resp.status, json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        text = e.read().decode(errors="replace")[:300]
        return e.code, {"error": text}


def pinned_in_target(jwt):
    status, body = call("GET", "/data/pinList?status=pinned&pageLimit=1000", jwt)
    if status != 200:
        raise SystemExit(f"Could not read the target account's pin list (HTTP {status}): {body.get('error', body)}")
    return {row["ipfs_pin_hash"] for row in body.get("rows", [])}


def main():
    args = set(sys.argv[1:])
    if args & {"-h", "--help"}:
        print(__doc__)
        return 0
    pins = load_pins()
    folders = [p for p in pins if p["kind"] == "directory"]
    print(f"{len(pins)} CIDs in the pin list ({len(folders)} folder, {len(pins) - len(folders)} files, "
          f"{sum(p['size'] for p in pins) / 1e6:.1f} MB).")
    if "--dry-run" in args:
        for p in pins:
            print(f"  would pin {p['cid']}  {p['kind'] or 'file'}  {p['name']}")
        return 0

    jwt = getpass.getpass("Target account JWT (hidden): ").strip()
    if not jwt:
        raise SystemExit("No key given. Nothing done.")
    status, body = call("GET", "/data/testAuthentication", jwt)
    if status != 200:
        raise SystemExit(f"The key was refused (HTTP {status}). Check it has pinList and pinByHash rights.")
    log("Key accepted by Pinata.")

    have = pinned_in_target(jwt)
    missing = [p for p in pins if p["cid"] not in have]
    log(f"Target already pins {len(pins) - len(missing)} of {len(pins)}; {len(missing)} to pin.")
    if "--check" in args or not missing:
        return 0 if not missing else 1

    # The folder first: it holds the memento images, so it matters most.
    missing.sort(key=lambda p: p["kind"] != "directory")
    for i, p in enumerate(missing, 1):
        status, body = call("POST", "/pinning/pinByHash", jwt,
                            {"hashToPin": p["cid"], "pinataMetadata": {"name": p["name"]}})
        if status != 200:
            log(f"[{i}/{len(missing)}] FAILED {p['cid']} (HTTP {status}): {body.get('error', body)}")
            if i == 1:
                raise SystemExit("The first pin failed, so stopping. If the message says pin by hash is not "
                                 "available on this plan, use the fallback in OTHER-PROJECTS.md.")
            continue
        log(f"[{i}/{len(missing)}] queued {p['cid']} ({body.get('status', 'queued')}) {p['name']}")
        time.sleep(0.4)

    log("Waiting for Pinata to fetch the files from IPFS (up to 15 minutes)...")
    deadline = time.time() + WAIT_SECONDS
    while True:
        have = pinned_in_target(jwt)
        left = [p for p in pins if p["cid"] not in have]
        log(f"Pinned in target: {len(pins) - len(left)} of {len(pins)}.")
        if not left:
            log("Done: every CID is pinned in the target account.")
            return 0
        if time.time() > deadline:
            for p in left:
                log(f"  still not pinned: {p['cid']} {p['name']}")
            log("Not all pinned yet. Run with --check later; pin jobs can take longer for the folder.")
            return 1
        time.sleep(30)


if __name__ == "__main__":
    sys.exit(main())
