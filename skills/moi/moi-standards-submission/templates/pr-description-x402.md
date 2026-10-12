<!--
Author notes. Delete this whole comment before the text is posted.
1. Fill every {{field}}. spec-lint.py reports any that is left, and any internal line.
2. Use these headings exactly. The x402 pull request template has Description, Tests and
   Checklist (read 2026-10-03). Re-read it before filing, because it changes.
3. Keep it short. x402 states that verbose, generic, AI-looking PR text may be closed.
4. No reviewer name, no "internal review" line, no placeholder PR number in what is posted.
5. The AI-assistance sentence: its wording is an open decision (references/open-decisions.md,
   conflict B). Do not add a co-author line or a "generated with" footer.
6. The title is in conventional-commit style, subject at most 72 characters. Merged spec-only precedents (read 2026-10-03): `specs(exact): propose Starknet exact scheme for x402 v2 (spec-only)`; for the package: `feat(moi): add @x402/moi mechanism package for the exact scheme`.
7. Tick a box only when it is true. Leave a box unticked and say why in the text, or delete it.
-->

**Title:** {{type}}({{scope}}): {{subject}}

## Description

{{One paragraph on what the PR adds and why, in x402's terms. Spec PR: the file path, the payment flow (upfront), and that /verify is omitted because every rule runs in /settle. Package PR: the package path and the spec file it implements.}}

{{One paragraph on what was checked against what. Name the checks and the sources a reader can open, not the people.}}

{{Proposal: "Closes #N" for the issue opened first (specs/CONTRIBUTING.md step 1), if one was opened.}}

{{Spec PR only: The moi CAIP-2 namespace is in review at ChainAgnostic/namespaces#{{number}}. This PR should not merge before it.}}

{{Only after the open decision is settled: the AI-assistance sentence, in the agreed words.}}

## Tests

{{Spec PR: "Specification only, no code." and how the rules were checked, using public steps: for example that the interaction and receipt bodies of rule 7 were read back from a settled transfer on devnet on {{date}}.}}

{{Package PR: the commands run from typescript/ and their results: pnpm test (number of tests), pnpm test:integration, pnpm lint:check, pnpm format:check, tsc. Say plainly what was not run, for example the full pay, prove and settle round trip.}}

## Checklist

- [ ] I have formatted and linted my code
- [ ] All new and existing tests pass
- [ ] My commits are signed (required for merge)
- [ ] I added a changelog fragment for user-facing changes (docs-only changes can skip)
