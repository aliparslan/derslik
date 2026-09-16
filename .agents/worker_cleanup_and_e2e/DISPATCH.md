# Worker Dispatch: Cleanup Obsolete Files and Run E2E Test Suite

## Identity & Context
- Role: E2E Test and Cleanup Worker
- Working Directory: `/Users/arslan/code/derslik/.agents/worker_cleanup_and_e2e/`
- Project Root: `/Users/arslan/code/derslik`
- Original Request: `/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md`
- Test Ready Specification: `/Users/arslan/code/derslik/.agents/TEST_READY.md`
- Test Runner: `/Users/arslan/code/derslik/tests/e2e_2000.py`

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Tasks
1. Read `/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md` and `/Users/arslan/code/derslik/.agents/TEST_READY.md`.
2. Remove the 4 obsolete skeleton files in `src/content/docs/2000/01-etiqad/`:
   - `src/content/docs/2000/01-etiqad/04-rohiy-alemler.mdx`
   - `src/content/docs/2000/01-etiqad/05-kitablar-peyghemberler.mdx`
   - `src/content/docs/2000/01-etiqad/06-qaza-qeder.mdx`
   - `src/content/docs/2000/01-etiqad/07-qiyamet-axiret.mdx`
3. Verify that `src/content/docs/2000/01-etiqad/` contains exactly the 8 canonical MDX files:
   - `01-din-heqqide.mdx`
   - `02-allahqa-iman.mdx`
   - `03-allahning-isimliri.mdx`
   - `04-perishtiler-cinlar.mdx`
   - `05-muqeddes-kitablar-peyghemberler.mdx`
   - `06-qaza-qeder-heqqide.mdx`
   - `07-axiret-kuni.mdx`
   - `08-etiqadqa-munasiwetlik.mdx`
4. Run the full 4-tier E2E tests:
   ```bash
   python3 tests/e2e_2000.py -v
   ```
   If any tests fail, inspect the failures, make the necessary corrections to ensure full compliance with ORIGINAL_REQUEST.md, and re-run.
5. Also run `pnpm build` to verify that the build succeeds and the search index is generated.
6. Write a detailed `handoff.md` in your working directory `/Users/arslan/code/derslik/.agents/worker_cleanup_and_e2e/` reporting all test outputs, verified counts, and build statuses.
7. Send a message to the orchestrator when completed.

## 2026-09-15T17:10:13Z
You are the E2E Test and Cleanup Worker.
Your working directory is `/Users/arslan/code/derslik/.agents/worker_cleanup_and_e2e/`.

Please read your task specifications at:
`/Users/arslan/code/derslik/.agents/worker_cleanup_and_e2e/DISPATCH.md`

Authoritative specifications:
- `/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md`
- `/Users/arslan/code/derslik/.agents/TEST_READY.md`
- Test harness: `/Users/arslan/code/derslik/tests/e2e_2000.py`

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Key tasks:
1. Remove the 4 obsolete skeleton files in `src/content/docs/2000/01-etiqad/`:
   - `04-rohiy-alemler.mdx`
   - `05-kitablar-peyghemberler.mdx`
   - `06-qaza-qeder.mdx`
   - `07-qiyamet-axiret.mdx`
2. Confirm that `src/content/docs/2000/01-etiqad/` contains exactly the 8 canonical MDX files:
   - `01-din-heqqide.mdx`
   - `02-allahqa-iman.mdx`
   - `03-allahning-isimliri.mdx`
   - `04-perishtiler-cinlar.mdx`
   - `05-muqeddes-kitablar-peyghemberler.mdx`
   - `06-qaza-qeder-heqqide.mdx`
   - `07-axiret-kuni.mdx`
   - `08-etiqadqa-munasiwetlik.mdx`
3. Run the full 4-tier E2E tests:
   `python3 tests/e2e_2000.py -v`
   If any issues are found, diagnose and fix them, then re-run until all pass.
4. Also verify `pnpm build` succeeds with zero errors and generates `dist/pagefind/`.
5. Document all commands, execution outputs, and verified file statuses in `/Users/arslan/code/derslik/.agents/worker_cleanup_and_e2e/handoff.md`.
6. Send a message to your parent with your completion summary.
