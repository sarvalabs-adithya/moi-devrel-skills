# Health: is the MOI MCP server up, and is what it says true

Run it after every deploy, after any devnet reset signal, and when a user reports a fault. No scheduled monitor for the three hosts is documented (research, 2026-10-02): only the nightly canary and the daily upstream watch run on their own (`watch-and-canary.md`). Facts are as of 2026-10-03 unless dated; the live build, tool counts and registry reading were corrected on 2026-10-14. Back to `../SKILL.md`.

## Layer 1: from outside, one command (read-only)
`bash "$SKILLS/moi-mcp-ops/scripts/mcp-health.sh"` checks the production write and read gateways and the two chain RPC paths. Add `--env dev` for the dev pair, `--github` for open canary and watch issues and the latest scheduled runs, `--write-host H` for any other host (a PR preview), `--selftest` to test the masking and the error handling (no network). Exit 0 means no FAIL, 1 at least one FAIL, 2 bad usage, 3 a fault in the script itself. Read every WARN: they do not change the exit code.

| Line | Healthy answer | If not | Go to |
|---|---|---|---|
| `health` | HTTP 200, `ok` true. Write: `{"ok":true,"network":"voyage","readOnly":false,"pairingMounted":true}`. Read: `{"ok":true,"version":"0.1.0","network":"voyage","readOnly":true}` | FAIL unreachable: DNS, TLS, nginx or the VM. 502: process down or wrong port. 503 with `ok` false: the config failed to load and the error log names the variable | `troubleshoot.md` rows 1 to 5. VM: ASK: Upendhar |
| `oauth issuer` | Equals `https://<the host>` exactly | `http://localhost...` means the environment never reached the process | `troubleshoot.md`, sign-in loops |
| `protected-resource metadata` | `resource` is `https://<host>/mcp` and the `/mcp` document answers 200 | WARN on production until 2026-10-14: bare origin and 404 (the build predated PR #18). The fix is live since the 2026-10-14 deploy | `troubleshoot.md`, Connect spins |
| `wallet tool without a token` | 401 | Anything else: check by hand | `connect-and-verify.md` |
| `tools/list` | 33 on the write gateway, 43 on the read gateway (since 2026-10-14; it was 13 and 6 on 2026-10-03). The script's defaults are still 13 and 6, so pass `--expect-write 33 --expect-read 43` or it WARNs | A different count after a deploy is news, not a fault. State which build is live | `architecture.md` |
| `ping` | server, version, network | FAIL: the process answers health but not a tool call | `troubleshoot.md` |
| `moi_resolve_agent` | An agent or "not found". It answers on dev and production since the 2026-10-14 deploy | WARN with "account not found": the registry id went stale (a devnet reset) or `MOI_READ_CALLER` is unset (the workflow passes it since voyage-api #323) | `settings-and-secrets.md`, reset runbook |
| `net.Version` | The same value on `/devnet/` and `/babylon/` (0.13.0) | FAIL both missing: every read tool fails; the line names the reason, such as a certificate that did not verify (the certificate that expired on 2026-10-04 was renewed, valid 2026-10-05 to 2027-01-03). A difference: ASK: Gokul | `moi-devrel/references/devnet.md` |
| `--github` issues and runs | No open `chain-canary` issue. Scheduled runs green and under 36 hours old | An open issue: triage it | `watch-and-canary.md` |

## Layer 2: by hand (what the script does)
```
curl -s https://mcp.voyage.moi.technology/health
curl -s https://mcp-read.voyage.moi.technology/health
curl -s https://mcp.voyage.moi.technology/.well-known/oauth-authorization-server
curl -s https://mcp.voyage.moi.technology/.well-known/oauth-protected-resource
curl -s -X POST https://mcp.voyage.moi.technology/mcp -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```
The MCP endpoint answers in server-sent events: the JSON follows a `data:` line. Replace the method with `tools/call` and `"params":{"name":"ping","arguments":{}}` for a tool call. Do not call a write tool this way.

The script masks every long hex string, so it hides the registry logic id in the `moi_resolve_agent` warning. A logic id is public chain data, not a key. To read which registry the server still points at, call the tool by hand and compare the first characters with the ids in `moi-devrel/references/devnet.md` (reset history):
```
curl -s -X POST https://mcp-read.voyage.moi.technology/mcp -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"moi_resolve_agent","arguments":{"query":"agent"}}}'
```
On 2026-10-03 the text named a logic whose id began `0x20000000c684f926`, the registry wiped on 2026-09-11. Since 2026-10-14 the tool answers instead; the current id in the code begins `0x200000002f3e9469`, the same as the Agent Explorer.

## Known readings (2026-10-03, with the newer rows marked)

| Reading | Meaning |
|---|---|
| 2026-10-03: production 13 tools, registry read fails, OAuth metadata in the old form | The live build then matched the 2026-09-23 sync (`architecture.md`). Master was newer |
| 2026-10-03: dev 13 tools, registry read fails, OAuth metadata in the new form | Dev was newer than production, and still without the registry fix |
| 2026-10-14: production and dev 33 and 43 tools, OAuth metadata fix live, agent lookup answers (dev: 10 PASS, 0 FAIL) | Both run moi-mcp master `3ae48cc0`. The 2026-09-23 sync is gone from production |
| `ping` says `readOnly` true on the write gateway | The ping tool reports true on both. Read the kind from `/health` |
| Every build says version 0.1.0 | The version cannot identify a sync |
| Canary and watch green | See "What each check cannot see" in `watch-and-canary.md` |
| 2026-10-13: production 9 PASS, 4 WARN, 0 FAIL; dev 10 PASS, 2 WARN, 0 FAIL. `net.Version` 0.13.0; `net.NetworkID` still answers method-not-found (-32601) | The WARNs were the known ones then (registry read, OAuth metadata form); both cleared by the 2026-10-14 deploy. Not a fault in the checks |

## Layer 3: CI side (read-only, needs `gh` access to the public repo)

| Check | Command | Healthy |
|---|---|---|
| Recent runs | `gh run list -R sarvalabs/moi-mcp --limit 8` | Canary and watch green; a failed CI run on a Dependabot branch was seen on 2026-10-01 |
| Open canary issues | `gh issue list -R sarvalabs/moi-mcp --label chain-canary --state open` | None |
| Open watch issues | `gh issue list -R sarvalabs/moi-mcp --label upstream-release --state open` | None unattended. #17 was open on 2026-10-03 |

## Layer 4: on the VM (DevOps holds it; Claude never logs in)
Each of these is a GATE: Claude drafts the ask, the operator sends it to DevOps, and DevOps reads and answers. The VMs are `voyagedev` (dev) and `prod-voyage` (production); only DevOps logs in. ASK: Upendhar or Srikar.

| Check | What DevOps reads on the VM (ASK: Upendhar how) | Healthy |
|---|---|---|
| Processes | The pm2 process list | `moi-mcp-read` (port 8787) and `moi-mcp-write` (port 8788) online, the write gateway as a single instance |
| Logs | The write gateway's last 100 log lines. The server logs to stderr with the prefix `[moi-mcp]`, so the error log matters most | No config errors. After a crash, "had broadcast before exit; recording it confirmed" and "cannot be safely re-broadcast; marking orphaned" are normal reconciliation: the user retries in chat |
| nginx | Read the server block | `proxy_buffering off`, `proxy_read_timeout` and `proxy_send_timeout` 300s, `X-Forwarded-For $remote_addr`, no redirect in front (not even http to https for the MCP path), nginx connecting from the same machine, the gateway ports blocked from outside |
| Logging itself | Does the process manager rotate logs | Unknown. ASK: Upendhar |

## What a green health check does not prove
- `/health` ok proves the process is up. It does not prove registry reads, a phone pairing or a write (the registry fault above ran for days with health ok, until the 2026-10-14 deploy).
- A green canary does not prove the hosted server (it tests `master` code against devnet).
- The phone path can only be proven by a person with a phone: `connect-and-verify.md`.

## Not yet known
- Whether any external uptime monitor or alert watches the hosts. None found.
- Whether process-manager or nginx logs are rotated and for how long they are kept. ASK: Upendhar.
