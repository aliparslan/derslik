# DISPATCH — orchestrator_7

## 2026-09-15T19:28:50Z

You are the Project Orchestrator (orchestrator_7) for converting Part 1 of "دىن ۋە ھايات (2000 سوئالغا جاۋاب)" from PDF into the Astro/Starlight web section under /2000/.

Your working directory is `/Users/arslan/code/derslik/.agents/orchestrator_7/`.
Authoritative request: `/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md`.
Test harness: `/Users/arslan/code/derslik/tests/e2e_2000.py`.
Test specification: `/Users/arslan/code/derslik/.agents/TEST_READY.md`.

Current state of the project:
1. All 647 questions (Q1-647), front matter, and 99 Names of Allah are completely extracted and generated on disk:
   - `src/content/docs/2000/00-muqeddimu/` (4 files)
   - `src/content/docs/2000/01-etiqad/` (8 canonical files: 01-din-ve-etiqad.mdx, 02-allahqa-iman.mdx, 03-allahning-isimliri.mdx, 04-perishtiler-jinlar.mdx, 05-samawiy-kitablar.mdx, 06-peyghamberler.mdx, 07-qada-qeder.mdx, 08-qiyamet-axiret.mdx)
   - `src/content/docs/2000/02-ibadet/` (14 files covering Q164-647)
   - `src/content/docs/2000/index.mdx`
   - `astro.config.mjs` (navigation configured)
   - `src/styles/custom.css` (Option B card styling configured)
2. CRITICAL REMAINING CLEANUP:
   In `src/content/docs/2000/01-etiqad/`, there are 4 obsolete skeleton files that must be removed so exactly the 8 canonical files remain:
   - `04-rohiy-alemler.mdx`
   - `05-kitablar-peyghemberler.mdx`
   - `06-qaza-qeder.mdx`
   - `07-qiyamet-axiret.mdx`
3. Verification:
   - Execute the full 4-tier E2E test suite: `python3 tests/e2e_2000.py -v`.
   - Verify `pnpm build` succeeds with zero errors.
   - If tests fail, investigate and fix.
4. When all tests pass and all acceptance criteria from ORIGINAL_REQUEST.md are satisfied, submit your final completion report and victory claim to Sentinel so Sentinel can trigger the independent Victory Audit.
