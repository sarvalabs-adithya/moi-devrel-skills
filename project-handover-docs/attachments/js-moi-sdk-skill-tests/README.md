# js-moi-sdk skill: test kit

The offline test suite used to check the js-moi-sdk Claude skill against js-moi-sdk 0.9.0-rc2 (13 and 14 October 2026). It builds and signs interactions locally and makes a few read-only devnet calls; it never sends anything.

    npm ci
    echo 'MOI_MNEMONIC="<12 words of a devnet test wallet>"' > .env
    node offline-tests.mjs

The last run passed 35 of 35 (`results-2026-10-13.txt` is the earlier 13 October record). `flipper.json` and `taxtoken.json` are the compiled Coco manifests the tests encode against. Update the `js-moi-sdk` version in package.json to test a newer release, and see project-handover-docs/AGENT-SKILLS.md for the full procedure.
