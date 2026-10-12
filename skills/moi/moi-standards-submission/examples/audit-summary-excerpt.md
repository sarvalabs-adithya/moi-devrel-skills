# Audit summary: the form

The summary table of the end-to-end audit of 2026-09-10. Below it the audit lists, for each PR, what was checked and passing, what is open, what changed that day, and what is not yet done.

## Summary

| PR | State | Blocking before filing |
|---|---|---|
| 1: CASA namespace | Text complete. Structure, regex, links, citations all pass. | Resolution Mechanics section (needs the protocol chain-id RPC); `discussions-to` PR number; reference-format decision (`devnet` vs numeric; note `moi:14` is already used by MOI Wallet). | <!-- slop-lint: ignore -->
| 2: x402 scheme spec | Text complete. Spec and code agree on every field, order and rule. | CASA merge (sequencing only). |
| 3: @x402/moi package | Typechecks on rc2; 28/28 unit tests; ESLint and Prettier clean; layout, package.json, workflow, changeset, e2e config all match upstream. | One live round trip on moipod v0.13.0 (goes live 00:00 UTC, 11 Sep). PR 2 merge (sequencing). |
