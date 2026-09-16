# Plan: Din ve Hayat (2000 Sualliq) PDF to Astro/Starlight Conversion

## Goal
Convert Part 1 of "دىن ۋە ھايات (2000 سوئالغا جاۋاب)" from PDF into an organized, searchable web section under `/2000/...` in the Astro/Starlight project at `/Users/arslan/code/derslik` covering Questions 1-647.

## Key Phases
1. **Phase 0: Survey & Specification Mining**
   - Survey Explorer 1: Inspect Astro/Starlight codebase layout, content collections, `astro.config.mjs`, UI components, Option B styling, RTL setups, build commands.
   - Survey Explorer 2: Inspect source PDF structure, page ranges, TOC, question formatting, font encodings, PyMuPDF extraction, legacy glyph anomalies (`\u066e`, `\u067b`, `\u06cc`, `\u0640`), footnote patterns.
   - Survey Explorer 3: Inspect 99 Names of Allah section (pages 56-69), tables, headings, division boundaries (Muqeddimu, Etiqad, Ibadet).
2. **Phase 1: Architecture, PROJECT.md, and E2E Test Suite Initialization**
   - Synthesize survey findings into `PROJECT.md` and feature inventory.
   - Launch E2E Testing Orchestrator / Test Writer to establish test runner and Tier 1-4 test cases (opaque-box requirements).
3. **Phase 2: Implementation Milestones**
   - Milestone 1: PDF Extraction and Unicode Normalization Scripts.
   - Milestone 2: 00-muqeddimu generation.
   - Milestone 3: 01-etiqad & 99 Names generation (Q1-163).
   - Milestone 4: 02-ibadet generation (Q164-647).
   - Milestone 5: Astro/Starlight Navigation, Sidebar & RTL Configuration.
4. **Phase 3: E2E Verification & Hardening**
   - Run 100% E2E tests against the generated content and build.
   - Phase 2 adversarial coverage hardening.
   - Forensic Audit verification.
5. **Phase 4: Completion & Reporting**
   - Report verified results to Sentinel.
