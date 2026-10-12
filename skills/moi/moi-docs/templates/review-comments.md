# Review comment set

A review is drafted here. The operator reads it once and posts it. Nothing below is sent by Claude.

## 1. Summary (the top comment)

Reviewed FILL-IN repo and PR number at commit FILL-IN, on FILL-IN date.
Ran: docs-page-lint on the changed pages (FILL-IN errors, FILL-IN warnings), the preview (FILL-IN pages opened), a source check of FILL-IN claims against FILL-IN ref.
Found: FILL-IN breaking, FILL-IN minor, FILL-IN questions. Counts match the list below.
Verdict: FILL-IN approve, or request changes because FILL-IN.
Not checked: FILL-IN (for example: private source not available, images not opened).

## 2. One issue (the format of 2026-08-21)

Issue FILL-IN number: FILL-IN what the issue is.
Why it is an issue: FILL-IN the effect on a reader, or the rule it breaks with its source.
Where: FILL-IN file and line, or the page and heading.
Suggested fix: FILL-IN the exact replacement text, or the step to take.
Severity: FILL-IN breaking (a reader acts on a wrong statement or the build breaks) or minor.

## 3. A style finding

Issue FILL-IN number: the description is FILL-IN characters (FILL-IN to FILL-IN is accepted).
Why it is an issue: search results and the llms.txt line use it as the preview.
Where: FILL-IN file, line of the description.
Suggested fix: FILL-IN a rewritten description of 140 to 160 characters that states what the page covers.
Severity: minor.

## 4. A fact finding with evidence

Issue FILL-IN number: FILL-IN the page says X.
Why it is an issue: FILL-IN the protocol or SDK behaves as Y at FILL-IN release tag or package version, so a reader following the page FILL-IN consequence.
Where: FILL-IN file, line.
Evidence: FILL-IN a public artefact (the package source at its tag, a documented method, a live read with its date). In a public repo never name a private file or line.
Suggested fix: FILL-IN replacement sentence.
Severity: FILL-IN.

## 5. A question, when the source cannot settle it

Question FILL-IN number: FILL-IN what you could not verify and why.
Who can settle it: FILL-IN a named person.
Until then: FILL-IN keep the sentence, soften it, or leave it out.

## 6. An anchor change

Issue FILL-IN number: the heading FILL-IN old text no longer has the anchor #FILL-IN.
Why it is an issue: links to that section land at the top of the page and nothing reports it.
Where: FILL-IN file, line.
Suggested fix: add {#FILL-IN old anchor} after the new heading text, or update every link first (grep the repo and search the sarvalabs org).
Severity: minor.

## 7. Re-review after a fix

Checked FILL-IN the fix commit. Issues FILL-IN numbers are resolved. Issue FILL-IN number still stands because FILL-IN.
