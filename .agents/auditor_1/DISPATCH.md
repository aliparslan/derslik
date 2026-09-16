# DISPATCH — auditor_1

## 2026-09-15T20:25:00Z

### Identity & Context
- Role: Forensic Auditor (archetype: `teamwork_preview_auditor`)
- Working Directory: `/Users/arslan/code/derslik/.agents/auditor_1/`
- Project Root: `/Users/arslan/code/derslik`
- Original Request: `/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md`
- Project Architecture & Scope: `/Users/arslan/code/derslik/.agents/PROJECT.md`
- Test Specification: `/Users/arslan/code/derslik/.agents/TEST_READY.md`
- Test Harness: `/Users/arslan/code/derslik/tests/e2e_2000.py`
- Worker Handoff: `/Users/arslan/code/derslik/.agents/worker_cleanup_e2e/handoff.md`

### Mission & Instructions
You MUST read the authoritative request first:
`/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md`

Perform a comprehensive Forensic Integrity Audit on the work done for "Din ve Hayat (2000 Sualliq)" Part 1:
1. Integrity Checks:
   - Check for cheating: Are test results hardcoded? Are there dummy/facade implementations or fake cards?
   - Verify authenticity of Question/Answer blocks: Compare against the authoritative source dataset `tools/extracted_2000.json`.
   - Verify question coverage: Confirm all 647 questions are authentic, genuine representations of the book content.
   - Verify 99 Names of Allah table: Confirm that all 99 names are authentic and not dummy placeholders.
   - Check Unicode normalization integrity: Ensure standard Uyghur glyphs are used, and no ungenuine workarounds were applied.
   - Audit the file system under `src/content/docs/2000/` and identify any anomalies or unauthorized alterations.
2. Deliver your audit report in `/Users/arslan/code/derslik/.agents/auditor_1/handoff.md` with your explicit binary verdict: `CLEAN` or `INTEGRITY VIOLATION`.
3. Send your verdict and findings to orchestrator_7.
