# The Launchpad pass: a reusable case list

Facts are as of 2026-10-03. `ASK:` is defined in `moi-devrel/SKILL.md`. Source: `docs/E2E-TESTING.md`, `docs/QA-LEDGER.md`, `docs/TEST-REPORT.md`, `docs/POST-CUTOVER-CHECKLIST.md`, `docs/UI-INVENTORY.md` and `scripts/verify-purchase.mjs` in `sarvalabs/moi-agent-launchpad`. That repo is private. All six are on `master` on GitHub as of the last fetch of the previous operator's clone, whose `origin/master` tip is dated 2026-09-15 (read with git on 2026-10-03, not fetched, so later commits are possible). ASK: Rahul for read access. The cases below are copied, so the files are not needed to run the pass, except the verifier script in L11. Back to `../GUIDE.md`.

Target: `https://launchpad.moi.technology`. The original plan's header names the old host; do not use it. The product's owner for questions: ASK: Adithya (history), Gokul (registry id), Upendhar (anything on the VM). Which of these DevRel owns now: ASK: Rahul.

## How to read the ids and the gates
- `L<n>.<m>`: L1 to L9 follow sections 1 to 9 of the original `E2E-TESTING.md`; L10 the Telegram batteries (sections 10, 11 and 14); L11 the payments audit (section 12); L12 the platform sweep and L13 the listing and settings controls (section 13, phases 5 and 3). `m` is this list's own running number: several original steps are merged into one line, so it does not match the original step numbers. A probe in L10 is `L10.<template>.<position>`.
- The `kind` below is the plan's expectation. The log records what happened (`log-format.md`, rule 10).
- Every `chain` case is a gate: the operator's yes names the paying account. Every case that downloads a file (L2.9, L13.5, every re-download in L10) is a gate too: the operator names the file, its source and its size first.
- Wallet, phone, Telegram and browser steps are the operator's. Claude reads, asks and logs. pm2 is the process manager that keeps a downloaded agent running on the operator's own machine.

## What changed since the list was written (30 July to 4 August 2026)
- The Test run button was removed (2026-08-02). Chat on Telegram replaces it.
- The shared free AI tier was retired (2026-08-02). Install now asks for the tester's own free Groq key, once. Section 8 of the original (the `n/40` daily counter and a migration warning in the server logs) is left out: the counter may be obsolete, and the log check is VM work. ASK: Adithya whether the counter still exists; ASK: Upendhar for the logs.
- A settings edit reaches a running agent within about 30 seconds with no re-download. Agents created before 2026-08-02 store no time zone: recreate them, do not re-download.
- Price history: `E2E-TESTING.md` section 11 expects "I don't keep price history", section 14 expects a real dated price. Use section 14.
- The wallet activation grant default is 10 KMOI in the code since PR #30 (September 2026). The README and env examples still say 100000 KMOI, and L1.4 was recorded against 100,000. Expect the code value and ASK: Adithya.
- The Launchpad has 10 templates (read from `lib/templates/index.ts` on `master`): `weather_brief`, `daily_digest`, `price_watch`, `fx_rate`, `alarm_reminder`, `standup`, `expense_logger`, `job_search`, `grant_scout`, `application_tracker`.
- After the 2026-09-11 wipe the registry moved on 2026-09-15 and earlier agents show "need registering again". Whether the AgentMarket contract was redeployed is not known (ASK: Adithya, Gokul), so section L11 stays `blocked` until it is.

## P. Preflight (10 minutes, reads)
| id | kind | ask or do | must |
|---|---|---|---|
| P1 | read | `GET /api/stats` twice, 20 to 60 seconds apart | The second answer has `chainStatus` `ok` and `chainError` null. A first call after idle can say `stale`. `chainAsOf` is the age of `registered` (ms since 1970) |
| P2 | read | `GET /api/marketplace?source=chain` | 200 with `"source":"chain"`. 502 `chain_unreachable` means the registry read fails. The default listing (no `source`) falls back to a database index and its `source` field says `db`: do not count it |
| P3 | read | `GET /api/marketplace/<public agent address>/listing`, address from P2 | `onchain` is an object. `null` means the read failed, not "unlisted" (the route's own comment). Expected fail for now: it answered `null` on 2026-10-02 and 2026-10-03 (17:37 UTC), consistent with the market contract not being redeployed (inferred; ASK: Adithya, Gokul) |
| P4 | read | `net.Version` (`real-chain.md`) | Recorded |
| P5 | read | Wallets A and B exist, funded for the test price plus about 2k fuel each. A creator cannot buy their own agent. A faucet request is a write: the operator makes it | Balances recorded from the chain (`moi_get_account`, `real-chain.md`) |
| P6 | app | The wallet's active account is the account you are signed in as | Switching accounts means signing out and in again |
| P7 | app | Extension installed and unlocked, Telegram ready, a free Groq key at hand | Operator confirms |
| P8 | read | `GET /api/runtime/version` | A 12-character fingerprint of the agent runtime bundle (not the commit). Record it. The route exists so that an installed agent can tell it is stale (its own comment), so an agent downloaded before the last deploy is probably older (inferred): re-download when it changes |

On 2026-10-03 the first stats call answered `registered` 20 with `chainStatus` `stale`, and a call 25 seconds later answered `registered` 0 with `ok`; the chain marketplace listing returned 200 with an empty `agents` list. At 17:36 UTC two stats calls 26 seconds apart agreed (20, `ok`), and the chain listing answered 7 agents at 17:37 and 0 a minute later. Read twice and log the time.

## L1 to L9. Platform cases
| id | kind | ask or do | must |
|---|---|---|---|
| L1.1 | app | Open the site in a browser without the extension | "You need a MOI Wallet" screen |
| L1.2 | app | Click Install MOI Wallet extension | The real extension listing, not a generic store page |
| L1.3 | app | Open on mobile | "Connect on desktop" screen |
| L1.4 | app | Fresh wallet F (the operator creates it): Connect, follow the one-time setup, then it signs in by itself | Auto-routed to setup with no dead end; extension shows the grant. Read the account from the chain: a "Wallet is ready" message alone is not evidence |
| L1.5 | app | Sign in with wallet A | Message signature, no fuel, lands on the dashboard |
| L1.6 | app | Lock the extension, sign in again | The error names the cause (locked), not "returned no signature" |
| L1.7 | app | Sign out, sign back in | Session restored, agents listed |
| L2.1 | app | Create, pick a template | Name pre-filled with an available suggestion |
| L2.2 | app | Dice button several times; type a taken name; type a fresh one | Never repeats at once; "taken" and "available" inline |
| L2.5 | chain | Leave it private, deploy | Wallet asks to sign the registration; agent active; the card address written on chain names the live host (permanent per agent) |
| L2.6 | app | Link Telegram | Deep link opens, bot confirms, banner clears |
| L2.7 | app | Message the agent on Telegram | A sensible reply |
| L2.9 | app | Download the setup script (a download: gate), read its relay URL, run the runtime under pm2 | Live host in the URL, no localhost. Runs and delivers on schedule |
| L2.10 | app | Pause, then Resume | Status flips. No runs while paused. The local log says paused, then active again |
| L2.11 | app | Install a second agent | The first install demands a key (Enter on empty asks again); the second offers the saved key |
| L3.1 | app | Open Marketplace; filter by category, by price, both together | Each listing has a category and a Free or price badge. Filters combine (AND) |
| L3.2 | app | Filter to an empty combination; Clear | "No agents match these filters" and Clear filters resets both |
| L3.3 | app | Open a detail page | Name, schedule, creator, price |
| L4.1 | app | As B, subscribe to a free agent of A | No payment step; a clone. Name suffixed if taken |
| L4.2 | app | Finish setup; subscribe to the same agent again; subscribe to your own | Clone delivers to B's Telegram; the second gives the existing copy; "This is your own agent" |
| L5.1 | chain | As A set a price (100), Save; approve the List | "Listed on-chain" with a hash. Wait for the confirmation |
| L5.2 | app | Cancel the List prompt | Says the price saved but the listing is incomplete and not purchasable |
| L5.3 | chain | Set the price to 0, Save; then list again | Wallet signs a delist; "Delisted on-chain" |
| L6.0 | read | Balances of A and B before (`moi_get_account`) | Recorded from the chain |
| L6.1 | chain | As B open A's paid agent, Pay and subscribe, approve | "Subscribed" panel with the payment hash |
| L6.2 | read | Balances after | B fell by exactly the price plus fuel. A rose by exactly the price |
| L6.3 | app | Continue to setup | Clone registers and delivers to B |
| L6.4 | read | Subscribe to the same paid agent again; count Subscribe interactions on the chain | Routed to the existing copy; no second payment |
| L6.5 | app | Buy an agent whose creator has not listed it | "isn't listed on-chain yet ... nothing was charged", no wallet prompt |
| L6.6 | app | Cancel the payment prompt | "Payment cancelled, nothing charged"; no clone |
| L6.7 | app | Switch the extension account without signing in again, then buy | Blocked up front: the active account does not match |
| L6.8 | chain | As a wallet holding less than the price, try to buy; the operator signs | The interaction reverts (read its receipt); no payment moves; the server creates no clone |
| L7.1 | app | Delete an unregistered agent | Gone at once, no wallet prompt |
| L7.2 | chain | Delete a registered agent | Wallet signs the deprecation; the agent disappears; the page shows the deprecation hash |
| L7.3 | app | Cancel that prompt; delete with an empty-fuel wallet; with the extension locked | Kept; removed locally with a note that the registry entry remains; offers "Remove it from your dashboard anyway?" |
| L7.4 | chain | Delete all with several agents; cancel a signature midway | Count and signatures confirmed; "Deleting 2 of 5"; stops and says how many were deleted; per-agent receipts with hashes |
| L7.5 | app | Reuse a deleted agent's name | Free again |
| L9.1 | app | Two agents, one name; each category; detail page | Second refused; each category in its filter; on-chain address and registry link |
| L9.2 | app | Open a public agent's share page; sign out and open a private agent's URL | No config values or keys shown; redirected to `/connect` |

## L10. Template batteries (Telegram; 45 minutes for all)
Re-download an agent after any template change (a download: gate), then restart pm2. An agent keeps its old behaviour until you do: testing without it tests stale code. A bold must in the original is a pass or fail. Every battery except `standup` ends with a CONFIG CHANGE: edit on the site, then expect the "Settings updated" message and the changed answer within about 30 seconds, no re-download. Each numbered probe is one case, `L10.<template>.<n>`, written `n ask -> must`.

| Template | Probes (config in brackets) |
|---|---|
| `weather_brief` | 1 `what's the weather like today?` -> real numbers for your city. 2 `what time is my delivery set for?` -> the exact configured local time. 3 `which timezone?` -> config or "not configured", never a guess. 4 `make it 3pm` -> refuses. 5 `is this my daily update?` -> no. 6 `will it rain at 8pm?` -> future hours only. 7 CONFIG CHANGE city -> the new city's weather |
| `daily_digest` | 1 `what are today's top headlines?` -> three bullets, each with source and link. 2 `tell me more about <name from a bullet>` -> answers, never "no information". 3 `what time do you deliver?` -> the exact configured time. 4 `change my topic to <x>` -> refuses and fetches nothing. 5 `hi` -> cheap, no invented schedule. 6 CONFIG CHANGE topic -> the new topic's headlines |
| `job_search` | 1 `suggest jobs` -> real listings with links. 2 `what's the salary for the <company> role?` -> "not in the data", an invented number is a hard fail. 3 `which of these did I apply to last week?` -> refuses. 4 `tell me more about the second one` -> the right listing. 5 `what's my experience level?` -> verbatim. 6 `any senior roles?` -> a mismatch heads-up if the level is configured. 7 CONFIG CHANGE city |
| `grant_scout` | 1 `show me opportunities` -> cards with title, kind, org, prize, deadline, url, reasons in plain words. 2 `what's the prize for the first one?` -> answers that item. 3 `what's my area set to?` -> verbatim. 4 `when's the deadline for the second one?` -> from the card or "check the link". 5 `change my area to robotics` -> refuses. 6 CONFIG CHANGE area |
| `application_tracker` | Read the weekly goal on the agent page first. 1 `applied to Google, software engineer`. 2 `applied to Stripe yesterday`. 3 `what am I tracking?` -> exactly those two. 4 `got an interview at Google` -> the status updates on re-query. 5 `did I apply to Netflix?` -> no (inventing is a hard fail). 6 `status on this week?` -> count 2 and the configured goal. 7 `pm2 restart`, then ask 3 again -> state survives. 8 CONFIG CHANGE goal 10 to 25 -> goal 25 |
| `price_watch` (asset by CoinGecko id, threshold just under the live price) | 1 `what's the price right now?` -> live number and distance to threshold. 2 `what was the price yesterday?` -> a real dated price. 3 `what was it 5 days ago?` -> the same, with the resolved date. 4 `what's DOGE worth?` -> "I only track <asset>". 5 `what's my alert set to?` -> verbatim. 6 `change my threshold to 90000` -> refuses. 7 `is this my daily update?` -> no, and no invented delivery time. 8 CONFIG CHANGE threshold across the live price -> the alert fires within about 15 minutes. Ground truth: CoinGecko `simple/price` |
| `fx_rate` (a pair such as USD/AED) | 1 `what's the rate now?`. 2 `convert 500 usd` -> real multiplication, rate shown. 3 `convert 2000 aed` -> divides. 4 `what was the rate last month?` -> no history, live rate. 5 `what's EUR/JPY?` -> "I only track <pair>". 6 CONFIG CHANGE pair. Ground truth: open.er-api.com |
| `standup` (no setting) | 1 `shipping the dashboard today, no blockers` -> logged. 2 `what did I say today?` -> verbatim. 3 `what did I work on last Friday?` -> "Nothing logged for Friday (date)". 4 `x` -> asks for a real plan |
| `alarm_reminder` | 1 `when is my reminder?` -> verbatim message and local time, zero model tokens. 2 `remind me to call mom at 6` -> refuses. 3 the fire arrives at the configured minute and the process exits cleanly (once). 4 CONFIG CHANGE time about 10 minutes out -> fires at the new time |
| `expense_logger` | 1 `coffee 5`, `spent 12 on uber`, `groceries 40.50` -> logged. 2 `how much did I spend today?` -> 57.50. 3 `delete the coffee expense` -> really deletes (52.50). 4 `spent 8 on subway yesterday` -> logged for the real date. 5 `did I buy anything yesterday?` -> the 8 appears. 6 `delete the pizza expense` -> "couldn't find", nothing else deleted. 7 `hello?` -> normal chat. 8 CONFIG CHANGE currency -> totals in the new currency |

## L11. Payments audit (blocked until the market contract is confirmed deployed)
Evidence is the chain, not the screen. Run from a working copy of the repo: `node scripts/verify-purchase.mjs 0x<hash>`. It needs no env, no database and no secrets, reads devnet only and prints a verdict. It imports `js-moi-sdk`, so the packages must be installed first: `npm ci` is a download and a gate. It pins an AgentMarket id by default; set `MOI_AGENT_MARKET_LOGIC_ID` after a redeploy. Without a working copy, read the receipt (`status`), the interaction and both balances by hand (`real-chain.md`); that proves the money moved, not that the calldata names the right agent and seller. Log an L11 case whose text says "replay" with `simulated_what` set to "none, replay is the attack under test", or the checker lists it.

| id | kind | ask or do | must |
|---|---|---|---|
| L11.1 | chain | A lists a fresh agent at 100, then re-lists at 150 | Two List hashes. The listing read shows `listed` true, price 150, creator A |
| L11.2 | chain | B buys; record both balances from the chain first | Payment hash; the verifier ends with a pass; A gains exactly 150, B loses 150 plus fuel |
| L11.3 | app | Subscribe API call with no payment (the operator makes it; it is a write to production, so a gate) | 402 `payment_required`; no clone |
| L11.4 | app | Replay the used payment hash against the same agent; against a different agent | `payment_already_used`; `agent_mismatch` |
| L11.5 | app | Cancel mid-buy; buy with less than the price; switch account; delist then buy | Nothing charged; no wallet prompt on a delisted agent |
| L11.6 | read | Read that Subscribe takes no amount argument | Underpayment cannot be built; note it in the report |
| L11.7 | chain | A third wallet buys the same agent; run the verifier on every hash | The seller ends with twice the price; every verdict passes |

The round substantiates five claims: every payment is buyer-signed, bound to one agent and its recorded seller, exactly the listed price, replay-proof on the server, and verifiable by anyone from the hash.

## L12 and L13. Platform sweep (15 minutes) and listing and settings controls (20 minutes)
| id | kind | ask or do | must |
|---|---|---|---|
| L12.1 | app | Run History after an agent's first scheduled run | Populates with status, summary and tokens |
| L12.2 | app | The dashboard "No runs yet" line | Says when the first run is due |
| L12.3 | chain | A single delete (same run as L7.2) | The page shows the deprecation hash; read it back. Open on 2026-08-02: it showed none |
| L12.4 | chain | Delete all at the end (same run as L7.4) | Per-agent receipt lines with hashes |
| L12.5 | app | Digest and job links in Telegram | Short hyperlinks, not raw URLs |
| L12.6 | app | A clone's card, `/api/moi/card/<address>` | Shows `cloned_from` and `subscribers` |
| L12.7 | app | Change a setting on a running agent | The agent page flips to "reached your running copy" |
| L13.1 | app | Agent page, Marketplace section: Listed free, Save | Under Free in the marketplace; no wallet prompt |
| L13.2 | app | Switch to Private, Save | Gone from the marketplace; no wallet prompt |
| L13.3 | chain | Listed paid (100), Save, approve | "Listed on-chain" with a hash; under Paid |
| L13.4 | chain | Back to Private on that paid agent | Wallet signs a delist; gone from the marketplace |
| L13.5 | app | Settings, Edit, change the delivery hour, Save | Values pre-filled; a saved note and a Download updated agent button (a download: gate) |
| L13.6 | app | Save a bad value (a blank required field) | A readable error; nothing saved |
| L13.7 | app | Pause a self-hosted agent, then Resume | Neutral dashboard note, not red; the local log says paused and goes quiet; on resume it says active again and the next run delivers |
| L13.8 | app | Visit `/create?agent=<deleted id>` | Explains; no blank wizard |
| L13.9 | app | The agent page's on-chain history after L13.3 and L13.4 | Both events, with clickable explorer hashes |

Order of one sitting, with times: P (10), the new-user journey L1.4 to L2.9 (20), L10 (45), L13 (20), L11 (45), L12 (15): 2 to 3 hours.

## Subsets
**After a devnet reset.** P1 to P8, then L1.4 (a fresh wallet is activated and the account exists on the new chain: read the receipt, because PR #30 found activation "succeeding" while the chain reverted), L2.5 (receipt status of the registration, and the card address names the live host), L2.9 with a fresh download (the bundle holds the asset id and the fuel price), L10 for `weather_brief`, and L11 once the market is confirmed. Earlier agents show "N agents need registering again": owners re-register, and their rows are never deleted. The dashboard notice is hardcoded to older reset dates, so read it as a case.

**After a host move** (`POST-CUTOVER-CHECKLIST.md`, written for the move of 2026-08-03). Smoke test, 5 minutes: cold load in a private window with no console errors, sign in, open an agent with history, marketplace loads, message the bot and see no `last_error_message` in the webhook info (that read needs `TELEGRAM_BOT_TOKEN`, which the operator reads into a variable without printing it; if the operator has no bot token, log that check `skipped`). Then: the relay URL in a downloaded script is the live host (L2.9); a 3-minute pm2 run polls continuously with no 502 or 504; a fresh wallet is set up (L1.4); an agent created before the move fails with a clear error and not a 500 (that breakage is accepted, a crash is not); a second new agent writes the real card address; a settings save shows "reached your running copy". VM checks (logs, restart, reboot, certificate renewal, memory after 24 hours): ASK: Upendhar.

## Recorded results
- 2026-07-30: round 1, nine templates and the platform, nine of nine with defects. Round 2, five templates, four with defects. 14 agent sessions, 13 defective, all fixed. One defect (the message ignored) appeared in four templates.
- 2026-08-01: fresh-wallet onboarding passed on production.
- 2026-08-02: a double charge (two Subscribe interactions), a price typed as 1000000 listed as 999998 by the mouse wheel, dates filed in UTC at 8:43 pm US Eastern. All fixed.
- Open on 2026-08-02: delete receipts showed no hash. Skipped on purpose: cross-agent hash and account-mismatch attacks.
- Never recorded: the sign-off tables, and the post-cutover checks of reboot, certificate renewal and memory after 24 hours (VM work: ASK: Upendhar).

## Not yet known
- Whether the AgentMarket contract was redeployed after 2026-09-11, and its id. ASK: Adithya, Gokul.
- Whether the `n/40` daily counter and the shared tier's message still exist. ASK: Adithya.
- The original's old-runtime check (an agent installed before the shared tier was retired should show "add your own free Groq key" and not hang) is not in this list, because it needs such an agent and none is recorded. ASK: Adithya.
