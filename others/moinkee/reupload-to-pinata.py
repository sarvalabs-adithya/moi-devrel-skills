#!/usr/bin/env python3
"""Copy the Moinkee files into another Pinata account by uploading them again (works on Pinata's free plan).

Pin by CID needs a paid Pinata plan, so this uploads the same bytes instead and checks that every CID comes out
identical to the original. If any CID differs, that upload is unpinned and the script stops, so the target account
never holds a copy under a different address.

  python3 reupload-to-pinata.py DIR --verify    recompute every CID from the downloaded files (no network, no key)
  python3 reupload-to-pinata.py DIR             upload to the target account (asks for its JWT, hidden)
  python3 reupload-to-pinata.py DIR --check     report how many of the 71 CIDs the target account pins

DIR holds what the download step fetched: DIR/folder/<file> (the 52 entries of the image folder),
DIR/json/<cid> (the 70 metadata files) and DIR/folder.json (the folder's entry list). The key is never printed
or saved. A log goes to ~/handover-notes/pinata-reupload-log.txt.
"""
import base64
import getpass
import hashlib
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request
import uuid

API = "https://api.pinata.cloud"
HERE = os.path.dirname(os.path.abspath(__file__))
PINS = os.path.join(HERE, "pinata_pins.json")
LOG = os.path.expanduser("~/handover-notes/pinata-reupload-log.txt")
CHUNK = 262144  # the IPFS default chunk size the original upload used

try:
    import certifi
    TLS = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    TLS = ssl.create_default_context()


def log(line):
    print(line)
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + line + "\n")


# ---- CIDs, computed the way IPFS does for CIDv1 with raw leaves and 256 KiB chunks ----

def varint(n):
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def field_bytes(num, data):
    return varint(num << 3 | 2) + varint(len(data)) + data


def field_int(num, value):
    return varint(num << 3) + varint(value)


def cid_bytes(codec, block):
    return b"\x01" + varint(codec) + b"\x12\x20" + hashlib.sha256(block).digest()


def cid_str(raw):
    return "b" + base64.b32encode(raw).decode().lower().rstrip("=")


def pb_link(cid_raw, name, tsize):
    return field_bytes(1, cid_raw) + field_bytes(2, name.encode()) + field_int(3, tsize)


def file_node(data):
    """Return (cid bytes, cumulative size) for a file."""
    if len(data) <= CHUNK:
        return cid_bytes(0x55, data), len(data)
    chunks = [data[i:i + CHUNK] for i in range(0, len(data), CHUNK)]
    links = b"".join(field_bytes(2, pb_link(cid_bytes(0x55, c), "", len(c))) for c in chunks)
    unixfs = field_int(1, 2) + field_int(3, len(data)) + b"".join(field_int(4, len(c)) for c in chunks)
    block = links + field_bytes(1, unixfs)
    return cid_bytes(0x70, block), len(block) + len(data)


def dir_node(entries):
    """entries: list of (name, cid bytes, cumulative size). Return (cid bytes, block)."""
    links = b"".join(field_bytes(2, pb_link(c, n, s)) for n, c, s in sorted(entries, key=lambda e: e[0].encode()))
    block = links + field_bytes(1, field_int(1, 1))
    return cid_bytes(0x70, block), block


def load(dir_):
    rows = json.load(open(PINS))["rows"]
    folder_row = next(r for r in rows if r.get("mime_type") == "directory")
    files = [r for r in rows if r.get("mime_type") != "directory"]
    entries = json.load(open(os.path.join(dir_, "folder.json")))
    return folder_row, files, entries


def verify(dir_):
    folder_row, files, entries = load(dir_)
    bad = 0
    for r in files:
        path = os.path.join(dir_, "json", r["ipfs_pin_hash"])
        got = cid_str(file_node(open(path, "rb").read())[0]) if os.path.exists(path) else "missing"
        if got != r["ipfs_pin_hash"]:
            bad += 1
            log(f"metadata MISMATCH {r['ipfs_pin_hash']} -> {got}")
    built = []
    for e in entries:
        path = os.path.join(dir_, "folder", e["name"])
        if not os.path.exists(path):
            bad += 1
            log(f"folder file missing: {e['name']}")
            continue
        c, size = file_node(open(path, "rb").read())
        if cid_str(c) != e["cid"]:
            bad += 1
            log(f"folder file MISMATCH {e['name']}: {e['cid']} -> {cid_str(c)}")
        built.append((e["name"], c, size))
    folder_cid = cid_str(dir_node(built)[0]) if len(built) == len(entries) else "incomplete"
    ok_folder = folder_cid == folder_row["ipfs_pin_hash"]
    log(f"verify: {len(files)} metadata files, {len(entries)} folder files, folder CID "
        f"{'matches' if ok_folder else 'DIFFERS: ' + folder_cid}; {bad} problem(s)")
    return bad == 0 and ok_folder


# ---- Pinata ----

def request(method, path, jwt, body=None, content_type=None):
    req = urllib.request.Request(API + path, data=body, method=method)
    req.add_header("Authorization", "Bearer " + jwt)
    if content_type:
        req.add_header("Content-Type", content_type)
    try:
        with urllib.request.urlopen(req, timeout=300, context=TLS) as resp:
            return resp.status, json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode(errors="replace")[:300]}


def upload(jwt, parts, name):
    """parts: list of (filepath in the upload, bytes). Returns (status, body)."""
    boundary = uuid.uuid4().hex
    out = bytearray()
    for filepath, data in parts:
        out += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{filepath}\"\r\n"
                "Content-Type: application/octet-stream\r\n\r\n").encode() + data + b"\r\n"
    for key, value in (("pinataMetadata", {"name": name}), ("pinataOptions", {"cidVersion": 1})):
        out += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"\r\n\r\n"
                + json.dumps(value) + "\r\n").encode()
    out += f"--{boundary}--\r\n".encode()
    return request("POST", "/pinning/pinFileToIPFS", jwt, bytes(out), f"multipart/form-data; boundary={boundary}")


def pinned(jwt):
    status, body = request("GET", "/data/pinList?status=pinned&pageLimit=1000", jwt)
    if status != 200:
        raise SystemExit(f"Could not read the target's pin list (HTTP {status}).")
    return {r["ipfs_pin_hash"] for r in body.get("rows", [])}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    flags = set(a for a in sys.argv[1:] if a.startswith("-"))
    if "-h" in flags or "--help" in flags or not args:
        print(__doc__)
        return 0 if args or "-h" in flags or "--help" in flags else 2
    dir_ = os.path.expanduser(args[0])
    if "--verify" in flags:
        return 0 if verify(dir_) else 1
    if not verify(dir_):
        raise SystemExit("The downloaded files do not reproduce the original CIDs. Nothing uploaded.")

    jwt = getpass.getpass("Target account JWT (hidden): ").strip()
    if not jwt:
        raise SystemExit("No key given. Nothing done.")
    status, _ = request("GET", "/data/testAuthentication", jwt)
    if status != 200:
        raise SystemExit(f"The key was refused (HTTP {status}).")
    log("Key accepted by Pinata.")
    folder_row, files, entries = load(dir_)
    have = pinned(jwt)
    want = len(files) + 1
    log(f"Target already pins {sum(1 for r in files if r['ipfs_pin_hash'] in have) + (folder_row['ipfs_pin_hash'] in have)} of {want}.")
    if "--check" in flags:
        return 0

    # The image folder first.
    fcid = folder_row["ipfs_pin_hash"]
    if fcid not in have:
        name = folder_row["metadata"].get("name") or "folder"
        parts = [(f"{name}/{e['name']}", open(os.path.join(dir_, "folder", e["name"]), "rb").read()) for e in entries]
        status, body = upload(jwt, parts, name)
        got = body.get("IpfsHash")
        if status != 200:
            raise SystemExit(f"Folder upload failed (HTTP {status}): {body.get('error', body)}")
        if got != fcid:
            request("DELETE", f"/pinning/unpin/{got}", jwt)
            raise SystemExit(f"The folder came back as {got}, not {fcid}; unpinned it and stopped. Tell Claude.")
        log(f"folder pinned with the same CID: {fcid}")
    for i, r in enumerate(files, 1):
        cid = r["ipfs_pin_hash"]
        if cid in have:
            continue
        data = open(os.path.join(dir_, "json", cid), "rb").read()
        name = (r.get("metadata") or {}).get("name") or cid
        status, body = upload(jwt, [(f"{cid}.json", data)], name)
        got = body.get("IpfsHash")
        if status != 200 or got != cid:
            if got and got != cid:
                request("DELETE", f"/pinning/unpin/{got}", jwt)
            raise SystemExit(f"[{i}/{len(files)}] {cid} failed (HTTP {status}, got {got}). Stopped. Tell Claude.")
        log(f"[{i}/{len(files)}] pinned {cid} {name}")
        time.sleep(0.3)
    have = pinned(jwt)
    left = [r["ipfs_pin_hash"] for r in files if r["ipfs_pin_hash"] not in have] + ([] if fcid in have else [fcid])
    log("Done: all 71 CIDs are pinned in the target account." if not left else f"Not yet listed as pinned: {left}")
    return 0 if not left else 1


if __name__ == "__main__":
    sys.exit(main())
