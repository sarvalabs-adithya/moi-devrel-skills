-- Template for a hand-written Points migration that touches the "tasks" table.
-- Copy to drizzle/00NN_<name>.sql in sarvalabs/moi-project, keep ONE of the three patterns, delete the rest,
-- then add the journal entry and run `pnpm check:migrations` (references/points-settings-and-database.md).
-- Never run `pnpm db:generate` or `drizzle-kit push`: the snapshots stop at 0003 (drizzle/TRIGGERS.md).
-- The runner splits the file on the text "--> statement-breakpoint", so put it after every statement.
-- Columns are those of drizzle/0009_dev_challenges.sql: id, title, description, points, verification_type,
-- active, sort_order, metadata. Replace each <...>. No secret belongs in this file.

-- Pattern A. Add a task (copy of the 0009 form for a legacy code dev challenge, the session 8 style; a webinar
-- bounty needs no migration, see references/points-tasks.md). Safe to run twice.
INSERT INTO "tasks"
  ("id", "title", "description", "points", "verification_type", "active", "sort_order", "metadata")
VALUES
  (
    '<task_id>',
    '<Title shown to members>',
    '<One or two sentences: what the member does and how it is verified.>',
    500,
    'onchain_challenge',
    true,
    100,
    '{"kind":"challenge","href":"/challenges/<name>","session":<N>,"difficulty":"intermediate","estimate":"1-2 hours"}'::jsonb
  )
ON CONFLICT ("id") DO NOTHING;
--> statement-breakpoint

-- Pattern B. Change what a task awards from now on (the form of 0004). The ledger is append-only, so earlier
-- awards do not change. Also change the same number in TASK_POINTS in lib/rewards/tasks.ts.
UPDATE "tasks"
SET
  "points" = <N>,
  "updated_at" = now()
WHERE "id" = '<task_id>';
--> statement-breakpoint

-- Pattern C. Add or overwrite a task in one statement (the form of 0008). Overwrites the listed columns.
INSERT INTO "tasks"
  ("id", "title", "description", "points", "verification_type", "active", "sort_order", "metadata")
VALUES
  ('<task_id>', '<Title>', '<Description>', <N>, '<verification_type>', true, <sort_order>, '{}'::jsonb)
ON CONFLICT ("id") DO UPDATE SET
  "title" = EXCLUDED."title",
  "description" = EXCLUDED."description",
  "points" = EXCLUDED."points",
  "verification_type" = EXCLUDED."verification_type",
  "active" = EXCLUDED."active",
  "sort_order" = EXCLUDED."sort_order",
  "metadata" = EXCLUDED."metadata",
  "updated_at" = now();
--> statement-breakpoint
