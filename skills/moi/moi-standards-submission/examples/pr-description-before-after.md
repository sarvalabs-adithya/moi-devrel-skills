# A PR description: the drafted form and the form to post

The left column is the drafted body of the scheme specification PR as it stood on 2026-10-03, shortened and cleaned (the reviewer's name is replaced by "the reviewer"). The right column is the form `templates/pr-description-x402.md` asks for. `spec-lint.py` reports most differences in the first column: the missing headings, the placeholder number, the unticked boxes and the internal line. It does not judge the order of the paragraphs.

| Drafted | To post |
|---|---|
| `# PR description` header with the target repo | No header. The title goes in the title field |
| The body opens on the file and the flow, then three paragraphs on `upfront` and the other flows | Headings Description, Tests, Checklist, as the upstream template has them |
| "This PR should not merge before that one does." after a link ending in `#TODO` | The real PR number, or the sentence deleted until the CASA PR exists | <!-- slop-lint: ignore -->
| `- [ ] CAIP-2 namespace PR to CASA opened` | A line is ticked only when true, or deleted |
| `- [ ] Commits GPG-signed, conventional prefixes` | `- [ ] My commits are signed (required for merge)`, ticked when true |
| `- [ ] AI assistance disclosed (this PR was drafted with AI assistance and human-reviewed)` | Wording is an open decision; the box is the upstream template's own four boxes only |
| `- [ ] Internal review (the reviewer) complete` | Deleted. It is an internal-process line, and public text carries no reviewer names |

What was good about the draft: it says why `upfront` is a choice, what `/verify` omission means, and that the spec follows the structure of merged specs. Keep those paragraphs, shorter.
