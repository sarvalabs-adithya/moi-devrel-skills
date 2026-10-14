# Example: one real health run

`web-health-2026-10-03.txt` is the unedited output of `bash "$SKILLS/moi-web-products-ops/scripts/web-health.sh" all`, run from a scratch folder on 2026-10-03 against the live public hosts, with exit code 0.

What was changed: nothing. The output holds only public host names, public paths, the titles of public Dataroom documents and public health fields. It has no key, no address of a stored file and no personal data. The script prints none of those by design.

What is good about it:
- It shows what a run with no new problem looks like: 25 PASS, 13 KNOWN, no WARN and no FAIL. Every KNOWN line carries the fault id, the date it was first recorded and the date it was seen again, and the file that describes it.
- It shows the reading rule of this skill. The homepage, the redirect and the page checks all PASS while `GET /api/community-calls` is KNOWN as 500 and the baked API base is KNOWN as the dev host. A reader who looked only at status codes would call the website healthy.
- It has no WARN. A Points WARN that says the database is ahead of the running build is normal between applying a migration and merging its code (`references/points-settings-and-database.md`); any other WARN or a FAIL is news.
- Compare a later run with it. A KNOWN line that turns into PASS ("looks fixed") means the fault is gone: update the row in `references/*-health.md` and the `KNOWN` table at the top of the script. A new WARN or FAIL is news.

Since website PR #60 (13 October 2026) the homepage no longer reads the calendar API, so the KNOWN calendar lines describe the old server routes only, not the homepage. It is a dated record, not a promise about today. Run the script again before quoting any line.
