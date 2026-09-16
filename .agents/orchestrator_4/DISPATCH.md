# Dispatch Log

## 2026-09-15T17:04:03Z

You are the Project Orchestrator (orchestrator_4) for converting Part 1 of "دىن ۋە ھايات (2000 سوئالغا جاۋاب)" from PDF to Astro/Starlight web section under /2000/.

Your working directory is `/Users/arslan/code/derslik/.agents/orchestrator_4/`.
The authoritative request is in `/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md`.
Test requirements and test suite are in `/Users/arslan/code/derslik/.agents/TEST_READY.md` and `/Users/arslan/code/derslik/tests/e2e_2000.py`.

Current project state:
- All 647 questions and Section 00 front matter have been extracted to `tools/extracted_2000.json`.
- `00-muqeddimu/` has all 4 canonical MDX files complete.
- `01-etiqad/` has all 8 canonical MDX files complete (including the full 99 Names responsive table in `03-allahning-isimliri.mdx`).
  CRITICAL: 4 obsolete skeleton files remain in `src/content/docs/2000/01-etiqad/`:
    `04-rohiy-alemler.mdx`, `05-kitablar-peyghemberler.mdx`, `06-qaza-qeder.mdx`, `07-qiyamet-axiret.mdx`.
  These 4 obsolete files must be removed so exactly the 8 canonical files remain.
- `02-ibadet/` has all 14 MDX files complete (covering Q164-647).
- `astro.config.mjs` and `src/styles/custom.css` are configured with Option B card styles and Starlight navigation.
- E2E tests are ready in `tests/e2e_2000.py`.

Your immediate goals:
1. Remove the 4 obsolete files from `src/content/docs/2000/01-etiqad/`.
2. Verify / run the E2E tests (`python3 tests/e2e_2000.py`) covering all 4 tiers (Tier 1 coverage, Tier 2 legacy glyphs/landmarks, Tier 3 99 Names table & CSS/config, Tier 4 build/search).
3. If any issues or gaps are discovered, dispatch a worker to resolve them.
4. When everything is verified passing and all acceptance criteria from ORIGINAL_REQUEST.md are met, send a message to Sentinel with your final completion report and victory claim so Sentinel can spawn the Victory Auditor.
