# Examples

Two real artefacts from the September 2026 sweep and this branch's first live checks. Facts are as of 2026-10-03.

## `baseline-2026-10-03.md`
Two unedited `geo-check.sh` runs: the live `docs.moi.technology` (still the state before the sweep) and the Cloudflare Pages preview of `sarvalabs/moidocs` pull request #124 (the layer). What is good about it:
- It is the shape of an audit's "before" and "after": the totals line of each run goes into `templates/audit-report.md`.
- Every FAIL of the first run maps to something the pull request changes (robots, llms, sitemap host, template page, canonical, structured data).
- The WARNs of the second run are real follow-ups, not noise: a stub still listed in `llms.txt`, a canonical that differs from the served address by a slash, and five pages sharing one `dateModified`.
Nothing was changed except that the file wraps the output in a heading. The output holds hosts and paths only.

## `ai-visibility-queries.yaml`
The previous operator's promptfoo suite of 25 questions about MOI, in four groups. It ran three times on 2026-09-09 and never completed, so no result exists and it is an example, not a baseline. Read `references/measure.md` before using it.
What was changed from the original: one em dash in a header comment was replaced with ", which", a header block listing the six known weaknesses was added (the last two warn about the weekly schedule it suggests and the file name in its run line), and the line that names a retired network carries the lint ignore marker. The queries and assertions are untouched. The original held no key, no address and no personal detail.
