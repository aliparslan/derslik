# Project Orchestrator (Generation 2) Dispatch Context

## Project State & Progress
You are succeeding the previous orchestrator to complete the Din ve Hayat (2000 Sualliq) Part 1 conversion at `/Users/arslan/code/derslik`.

### Already Completed Assets:
1. **Verbatim Requirements**: `/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md`
2. **Architecture & Test Specifications**: `/Users/arslan/code/derslik/.agents/PROJECT.md`, `TEST_INFRA.md`, `TEST_READY.md`
3. **E2E Test Runner**: `/Users/arslan/code/derslik/tests/e2e_2000.py` (all 4 tiers implemented)
4. **Intermediate Extracted Dataset**: `/Users/arslan/code/derslik/tools/extracted_2000.json` (566 KB, 7,457 lines). Contains all 647 questions, 99 Names, and front matter with standard Uyghur Unicode and logical RTL word order.
5. **Section 00 (00-muqeddimu)**: `/Users/arslan/code/derslik/src/content/docs/2000/00-muqeddimu/` (4 MDX files generated and verified: 01-kitab-heqqide.mdx, 02-aptur-heqqide.mdx, 03-kirish-soz.mdx, 04-munderije.mdx).
6. **Navigation & Styling**: `astro.config.mjs` (sidebar configured with `2000 سوئال-جاۋاب`), `src/styles/custom.css` (Option B card styles and 99 Names table styles), `src/content/docs/2000/index.mdx` (portal landing page).

### Remaining Work Items:
1. **Milestone 3**: Generate Section 01 (`src/content/docs/2000/01-etiqad/`) - 8 MDX files covering Questions 1 to 163 and the 99 Names of Allah responsive table from `tools/extracted_2000.json`. Overwrite any legacy/reversed files in that directory.
2. **Milestone 4**: Generate Section 02 (`src/content/docs/2000/02-ibadet/`) - 14 MDX files covering Questions 164 to 647 from `tools/extracted_2000.json`. Overwrite any legacy/reversed files in that directory.
3. **E2E Verification & Build**: Run `python3 tests/e2e_2000.py` and `pnpm build` to verify 100% pass across all 4 tiers (Feature Coverage, Unicode & Integrity, 99 Names table, and Astro build + Pagefind index).
4. **Victory Report**: Send a completion message to the Sentinel (`e3d33290-8e81-427d-9b9d-fc995603a89d`) with complete test evidence.
