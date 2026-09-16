## 2026-09-15T13:13:27Z

You are Worker Verifier for the conversion of Part 1 of "دىن ۋە ھايات (2000 سوئالغا جاۋاب)".
Your working directory is `/Users/arslan/code/derslik/.agents/worker_gen3_verifier/`.
Read `/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your Tasks:
1. Delete the 4 obsolete skeleton files in `src/content/docs/2000/01-etiqad/`:
   - `04-rohiy-alemler.mdx`
   - `05-kitablar-peyghemberler.mdx`
   - `06-qaza-qeder.mdx`
   - `07-qiyamet-axiret.mdx`
   You can delete them using a simple python one-liner or rm command, for example:
   `python3 -c "import os; [os.remove(f'src/content/docs/2000/01-etiqad/{f}') for f in ['04-rohiy-alemler.mdx', '05-kitablar-peyghemberler.mdx', '06-qaza-qeder.mdx', '07-qiyamet-axiret.mdx'] if os.path.exists(f'src/content/docs/2000/01-etiqad/{f}') else None]"`
   Verify that exactly 8 canonical files remain in `src/content/docs/2000/01-etiqad/`.

2. Run the full E2E test suite:
   Execute `python3 tests/e2e_2000.py` in the workspace root (`/Users/arslan/code/derslik`).
   Capture the full test output and verify that all 4 tiers pass with 100% success!

3. Run the full site build:
   Execute `pnpm build` in the workspace root (`/Users/arslan/code/derslik`).
   Verify that the build completes with exit code 0 and pagefind search index is generated.

4. Write a comprehensive handoff report to `/Users/arslan/code/derslik/.agents/worker_gen3_verifier/handoff.md` with:
   - Verification of 8 canonical files in `01-etiqad/`
   - Verification of 14 canonical files in `02-ibadet/`
   - Full console output of `python3 tests/e2e_2000.py`
   - Full console output of `pnpm build`
   - Explicit confirmation of pass/fail for each tier

When done, send a message to parent (`65f8e8f1-2fca-49a7-8b3f-c817ab097747`) with your summary and handoff path.
