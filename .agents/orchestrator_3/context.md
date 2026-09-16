# Project Orchestrator (Generation 3) Context

## Current Status & High-Velocity Completion Plan
You are succeeding the previous orchestrators at `/Users/arslan/code/derslik`.

### Already Completed Assets:
1. **Requirements & Specs**:
   - `/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md`
   - `/Users/arslan/code/derslik/.agents/PROJECT.md`
   - `/Users/arslan/code/derslik/.agents/TEST_READY.md`
2. **Intermediate Extraction Dataset**:
   - `/Users/arslan/code/derslik/tools/extracted_2000.json` (566 KB, 7,457 lines): 100% complete with all 647 questions, 99 Names of Allah, and front matter extracted with normalized standard Uyghur Unicode and logical RTL word order.
3. **Section 00 (00-muqeddimu)**:
   - All 4 MDX pages complete in `src/content/docs/2000/00-muqeddimu/`.
4. **Section 01 (01-etiqad)**:
   - All 8 target MDX pages complete: `01-din-ve-etiqad.mdx`, `02-allahqa-iman.mdx`, `03-allahning-isimliri.mdx` (including the full 99 Names responsive table), `04-perishtiler-jinlar.mdx`, `05-samawiy-kitablar.mdx`, `06-peyghamberler.mdx`, `07-qada-qeder.mdx`, `08-qiyamet-axiret.mdx`.
   - **Action needed**: Delete the 4 obsolete skeleton files:
     - `src/content/docs/2000/01-etiqad/04-rohiy-alemler.mdx`
     - `src/content/docs/2000/01-etiqad/05-kitablar-peyghemberler.mdx`
     - `src/content/docs/2000/01-etiqad/06-qaza-qeder.mdx`
     - `src/content/docs/2000/01-etiqad/07-qiyamet-axiret.mdx`
5. **Section 02 (02-ibadet)**:
   - Files 01 through 06 (`01-ibadet-esasliri.mdx` through `06-namaz-ehkamliri.mdx`, Q164–Q332) are complete.
   - **Action needed**: Generate remaining files 07 through 14 (Q333–Q647) from `tools/extracted_2000.json`:
     - `07-namaz-oqush.mdx`: Q333–393
     - `08-jamaet-jume.mdx`: Q394–428
     - `09-bashqa-namazlar.mdx`: Q429–477
     - `10-jinaze-depne.mdx`: Q478–506
     - `11-zakat.mdx`: Q507–553
     - `12-roza-ramizan.mdx`: Q554–607
     - `13-hej-omre.mdx`: Q608–634
     - `14-sawab-gunah.mdx`: Q635–647
6. **Navigation & Styles**:
   - `astro.config.mjs`, `src/styles/custom.css`, and `src/content/docs/2000/index.mdx` are complete.
7. **E2E Test Runner**:
   - `tests/e2e_2000.py` is complete across all 4 tiers.

### Your Immediate Task:
1. Dispatch a worker to:
   a. Delete the 4 obsolete files in `01-etiqad/`.
   b. Generate the remaining 8 MDX files in `02-ibadet/` (files 07–14) from `tools/extracted_2000.json` using Option B card markup.
   c. Run `python3 tests/e2e_2000.py` across all 4 tiers and verify 100% pass.
   d. Run `pnpm build` and verify exit code 0.
2. Report project completion to the Sentinel (`e3d33290-8e81-427d-9b9d-fc995603a89d`) with complete test logs.
