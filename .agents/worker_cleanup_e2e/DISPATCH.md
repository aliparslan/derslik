# DISPATCH — worker_cleanup_e2e

## 2026-09-15T19:30:00Z

### Identity & Mission
You are `worker_cleanup_e2e` (archetype: `teamwork_preview_worker`), reporting to orchestrator_7.
Your working directory is `/Users/arslan/code/derslik/.agents/worker_cleanup_e2e/`.
You MUST read the authoritative request first:
`/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md`

You also need to consult:
- Scope & Architecture: `/Users/arslan/code/derslik/.agents/PROJECT.md`
- Test Harness: `/Users/arslan/code/derslik/tests/e2e_2000.py`
- Test Specification: `/Users/arslan/code/derslik/.agents/TEST_READY.md`

### Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

### Tasks to Perform:
1. **Critical Cleanup in `src/content/docs/2000/01-etiqad/`**:
   Remove the 4 obsolete skeleton files:
   - `src/content/docs/2000/01-etiqad/04-rohiy-alemler.mdx`
   - `src/content/docs/2000/01-etiqad/05-kitablar-peyghemberler.mdx`
   - `src/content/docs/2000/01-etiqad/06-qaza-qeder.mdx`
   - `src/content/docs/2000/01-etiqad/07-qiyamet-axiret.mdx`
   Verify that exactly the 8 canonical MDX files remain in `src/content/docs/2000/01-etiqad/`:
   - `01-din-ve-etiqad.mdx`
   - `02-allahqa-iman.mdx`
   - `03-allahning-isimliri.mdx`
   - `04-perishtiler-jinlar.mdx`
   - `05-samawiy-kitablar.mdx`
   - `06-peyghamberler.mdx`
   - `07-qada-qeder.mdx`
   - `08-qiyamet-axiret.mdx`

2. **Execute Full E2E Test Suite**:
   Run: `python3 tests/e2e_2000.py -v` in `/Users/arslan/code/derslik`.
   Check that all 4 tiers pass:
   - Tier 1: Question count (647), question set (1..647), card structure, section pages & boundaries.
   - Tier 2: Unicode normalization (0 dotless beh, 0 beeh with two vertical dots, 0 interior tatweels), boundary questions integrity.
   - Tier 3: 99 Names table (99 rows, 3 columns), Option B CSS, sidebar navigation.
   - Tier 4: Astro build (`pnpm build`) and Pagefind search index.

3. **Verify Astro Build**:
   Run: `pnpm build` in `/Users/arslan/code/derslik` and verify it exits 0 with no errors.

4. **Remediate if any tests fail**:
   If any test fails, diagnose the exact cause, fix the issue in the relevant file, and re-run until 100% passing.

5. **Reporting**:
   - Update `progress.md` with timestamps and task checkpoints.
   - Write a comprehensive `handoff.md` in `/Users/arslan/code/derslik/.agents/worker_cleanup_e2e/handoff.md` with:
     - Exact actions taken
     - Output of `python3 tests/e2e_2000.py -v`
     - Output of `pnpm build`
     - Files verified
     - Layout compliance
   - Send completion message to orchestrator_7 via `send_message`.

## 2026-09-15T20:01:33Z
**Sender**: parent (24422224-954f-4b52-930c-abad546b5195)
**Context**: Checking progress on cleanup and E2E testing
**Content**: It has been ~25 minutes since your last progress update. What is your current status? Are commands (e.g. `pnpm build` or `python3 tests/e2e_2000.py`) currently running or completed?
**Action**: Please update progress.md and report current status immediately.

