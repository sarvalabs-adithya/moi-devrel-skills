<!--
Author notes. Delete this whole comment before the text is posted.
1. Fill every {{field}}. spec-lint.py reports any that is left.
2. The namespaces repository has no pull request template (no file at the usual .github paths,
   read 2026-10-03), so this body is the project's own. Keep it to what an editor needs.
3. CASA chases the author named in the front matter. Name a person who will answer.
4. Tagging reviewers familiar with the namespace is acceptable (CASA CONTRIBUTING).
5. No reviewer name from inside MOI, no internal-review line, no placeholder PR number.
6. The AI-assistance sentence: wording is an open decision (references/open-decisions.md,
   conflict B). CASA's CONTRIBUTING says nothing about AI.
7. Do not write the reference format sentence until the format is decided (open decision A).
-->

**Title:** Add `moi` namespace (CAIP-104 profile + CAIP-2 chains profile)

This PR adds the `moi` namespace: `namespaces/moi/README.md` (the CAIP-104 profile) and `namespaces/moi/caip2.md` (the CAIP-2 chains profile). The files follow `_template/` and are modelled on the accepted {{profiles, for example neo}} profile.

{{One or two sentences on what is particular to MOI, in the agreed MDAG wording: MOI is participant-centric, its ledger is a DAG of tesseracts and not a chain of blocks, and no network is identified by a genesis hash.}}

{{One sentence naming the reference format, after the decision: for example "A MOI network is identified by {{its network ID or its name}}, and a client confirms it with {{the real RPC method}}."}}

Discussion happens at {{the discussions-to URL}}. {{Author name (@handle)}} answers comments.

{{Only after the open decision is settled: the AI-assistance sentence, in the agreed words.}}
