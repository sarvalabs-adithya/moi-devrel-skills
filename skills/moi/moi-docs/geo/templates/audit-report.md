# GEO audit: <scope>, <YYYY-MM-DD>

How to use: copy this file into `geo-audit-<YYYY-MM-DD>/` (the folder hides itself from git with a `.gitignore` holding `*`; it names private repo paths, so it is never committed). Fill every section or write "none". Delete these instructions. The sections follow the status message of 2026-09-10. Put only finished work above "Next steps".

Operator: <name>. Rubric for scores: <the rubric you used, or "no scores given">. Every fetch below carries its date.

## Summary
- Properties audited: <N>. FAIL before: <N>. FAIL after: <N>. Findings open: <N>.
- Ready: <yes or no>, because <one reason>.

## Properties
| Host | Repo and branch | Pull request | Fetched on | Before (geo-check totals) | After (totals) | After is from |
|---|---|---|---|---|---|---|
| <host> | <repo, branch> | <#, state> | <YYYY-MM-DD> | <N PASS, N WARN, N FAIL> | <totals> | live, or preview <host> |

## What was done
Only completed work. Each line names the file or the check.
### Content changes
- <page, change, or none>
### Frontmatter and metadata
- <descriptions, canonicals, share tags, or none>
### llms.txt and markdown copies
- <generator change, or none>
### robots.txt and crawler access
- <file change, crawler check result with date, or none>
### Entity presence
- <Wikidata, organisation profiles: only what exists. Write "not done" for the rest>
### Analytics
- <Search Console, Bing, GA4 state, or none>
### Scores
| Property | SEO | GEO | AEO | Describes | Rubric |
|---|---|---|---|---|---|
| <host> | <n> | <n> | <n> | live, or branch <name> | <name> |

## Findings
The table is `findings-table.csv` in this folder (copy it from `templates/`; it holds the header row only). One row per finding. `area` is SEO, GEO or AEO. `severity` is Critical, High, Medium or Quick win. `status` is open, fixed, verified, needs-owner or wontfix. `evidence` is the path or file you fetched and what you saw, with the date. `where` is the repo and file that holds the cause. Put a cell that holds a comma in double quotes. Counts by severity: Critical <N>, High <N>, Medium <N>, Quick win <N>.

## What this audit did not check
- Indexing and rankings (Search Console, Bing).
- How the real crawlers are treated (checks ran from this machine).
- Pages that need JavaScript to show content, unless a render was run.
- <anything else, including a tool not run>

## Next steps (to-dos, not done)
1. <action, owner, GATE if it needs a yes>

## Open questions
- ASK: <person>, <question>
