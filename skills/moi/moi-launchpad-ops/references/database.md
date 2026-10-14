# Database: migrations

Facts are as of 2026-10-03, from `supabase/migrations/` (0001 to 0012) on `origin/master`, `docs/HANDOFF.md` section 3 and the research. The Launchpad database is Supabase Postgres. Only the Launchpad has one here: the Explorer's MySQL changes its own schema at boot (`../explorer/references/ship-a-change.md`) and the MCP server has no database. Back to `../SKILL.md`.

## How migrations are applied
- By hand, in numeric order, by pasting the file into the Supabase SQL editor of the project named by the `SUPABASE_URL` variable. A deploy never applies one. There is no tracking table, so nothing records what is applied: you find out by reading the schema.
- The production project was not reachable through the previous operator's Supabase connector (`docs/HANDOFF.md` section 3). If your session has one, do not use it on the production project without a yes. Claude does not run SQL against production; the operator pastes it.
- The project is in the company Supabase organisation (moved 8 October 2026) and DevRel owns it (`project-handover-docs/AGENT-LAUNCHPAD.md`). Whether it is on a paid plan with backups is not recorded: read the plan in the Supabase dashboard; ASK: Rahul.
- There is no down migration. To undo one, write a new forward migration and ship it like any change.

## The 12 files
"Twice" means safe to run a second time. The column was read from each file on 2026-10-03.
| File | What it does | Twice? | If it is missing |
|---|---|---|---|
| `0001_init` | Tables `profiles`, `nonces`, `agents`, `runs`, `logs_entries`, `usage`, `platform_state`; row-level security with no policies; functions `consume_interaction`, `record_spend`, `consume_nonce` | No | Nothing works |
| `0002_inbound` | `inbound_messages`, `profiles.focused_agent_id`, function `claim_inbound` | No | No two-way chat |
| `0003_marketplace` | `agents.visibility`, `category`, `cloned_from`; table `subscriptions` | No | No marketplace |
| `0004_pricing` | `agents.price` (0 is free) | No | Everything is treated as free |
| `0005_payment_dedup` | `subscriptions.payment_tx` and a unique index | No | One payment could unlock many paid agents (the file's own warning) |
| `0006_interaction_cap` | Makes the cap a parameter of `consume_interaction(uid, cap)` | Yes | Users blocked at 10 while the dashboard shows 40. The code probes and falls back (commit 3ea312a) |
| `0007_unique_agent_name` | Unique name per owner; renames duplicates | No | Superseded by 0008 |
| `0008_global_unique_agent_name` | Unique name across all live agents; the oldest keeps the name, newer duplicates get a short id suffix. Drops the 0007 index | No. It rewrites data on the first run and creates its index without a guard | Duplicate names allowed |
| `0009_deprecate_tx` | `agents.deprecate_tx` | Yes | Deleting still works; the hash is not kept |
| `0010_chain_events` | Table `agent_chain_events` and indexes | Yes | Listing and delisting events are not recorded |
| `0011_config_sync` | `config_version`, `config_synced_version`, `config_synced_at` on `agents` | Yes | The page cannot say a settings change reached a running agent |
| `0012_message_encryption` | `agents.message_pubkey` | Yes | Messages stay plain text at rest. What the code does with the column absent is unknown |
The post-cutover checklist (section 0.5, undated) confirms only 0010 and 0011 as applied in production. Everything else is unrecorded. Whether 0012 is applied is unknown: the read-only checks below include a `message_pubkey` row.

## Read-only checks (the operator pastes these into the SQL editor)
Written for this skill from the migration files. They only select. They were not run against any database, so read them before use and expect to adjust a name.
```sql
select v.migration, v.tbl, v.col, (c.column_name is not null) as present
from (values
  ('0002','profiles','focused_agent_id'), ('0003','agents','visibility'), ('0003','agents','category'),
  ('0003','agents','cloned_from'), ('0004','agents','price'), ('0005','subscriptions','payment_tx'),
  ('0009','agents','deprecate_tx'), ('0011','agents','config_version'),
  ('0011','agents','config_synced_version'), ('0011','agents','config_synced_at'),
  ('0012','agents','message_pubkey')
) as v(migration, tbl, col)
left join information_schema.columns c
  on c.table_schema = 'public' and c.table_name = v.tbl and c.column_name = v.col
order by v.migration;

select 'table inbound_messages (0002)' as object, to_regclass('public.inbound_messages') is not null as present
union all select 'table subscriptions (0003)', to_regclass('public.subscriptions') is not null
union all select 'table agent_chain_events (0010)', to_regclass('public.agent_chain_events') is not null
union all select 'index subscriptions_payment_tx_key (0005)', to_regclass('public.subscriptions_payment_tx_key') is not null
union all select 'index agents_name_key (0008)', to_regclass('public.agents_name_key') is not null
union all select 'old index agents_owner_name_key is gone (0008)', to_regclass('public.agents_owner_name_key') is null
union all select 'consume_interaction(uid, cap) (0006)', exists (
  select 1 from pg_proc p join pg_namespace n on n.oid = p.pronamespace
  where n.nspname = 'public' and p.proname = 'consume_interaction'
    and pg_get_function_identity_arguments(p.oid) like '%cap integer%');
```
Every `present` should be true. A false row names the migration to look at.

## Run: apply a migration
| # | Step | Command or action | Done when | Gate |
|---|---|---|---|---|
| 1 | Read the state | The operator pastes the two queries above, one at a time (the SQL editor may show only the last result of a multi-statement run; not tested here), and gives you each result | You know which files are applied | read-only |
| 2 | Read the file | Read the whole migration. Does it rewrite data, drop anything, or lack `if not exists`? Match it to the table above | You can say what it changes and whether a second run is safe | read-only |
| 3 | Save what it changes | For a file that rewrites rows (like 0008), the operator copies the affected columns (`id`, `name`) to a local file first, outside git, since the file holds user data. Ask whether a backup exists | A copy exists, or the operator accepted the risk in writing | OPERATOR |
| 4 | Try it away from production | If the Supabase CLI and Docker are installed, in the working copy: `supabase start` (pulls Docker images the first time: say so before running it) then `supabase db reset`, which applies all files to a local database. `npm run test:atomicity` needs a live database and fires many parallel calls: run it against a local one only | Applies cleanly, or step skipped and said so | local |
| 5 | Apply | The operator opens the SQL editor of the project named by `SUPABASE_URL`, pastes the file verbatim, runs it once. Numeric order. Never again unless step 2 says "Yes" for twice | The editor reports success | GATE, OPERATOR |
| 6 | Check | The operator re-pastes the queries of step 1 | The new object reads true | read-only |
| 7 | Then the code | Merge the code that needs it (`ship-a-change.md`). Apply first, merge second. The code is written to degrade without 0009, 0010 and 0006, which is a safety net and not a plan | The merge is done after step 6 | GATE |
| 8 | Verify | Health script. Use the feature the migration serves. A DevOps log read can show whether a "migration NNNN is not applied" warning stopped | Healthy and the feature works | read-only |
| 9 | Record | File name, time, who ran it, result of step 6, in `../templates/change-checklist.md` | The note exists | local |

## If a migration goes wrong
Stop. Do not run it again. Paste the exact error (not the data). If rows were rewritten, use the copy from step 3 to put the old values back by hand with a reviewed `update`. Treat that restore as a new GATE. Tell Rahul. A migration that locks or empties a table needs DevOps and the project owner, not a guess.

## Not yet known
- The Supabase plan and whether backups exist (the project is in the company organisation). ASK: Rahul.
- Whether 0001 to 0009 and 0012 are applied in production.
- Whether the app logs a warning for each missing migration or only some.
