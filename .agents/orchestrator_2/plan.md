# Plan — Project Orchestrator (Generation 2)

## Goal
Complete Part 1 conversion of "دىن ۋە ھايات (2000 سوئالغا جاۋاب)" at `/Users/arslan/code/derslik` and verify that all acceptance criteria and E2E tests pass.

## Steps
1. **Initialize State & Heartbeat**:
   - Set up DISPATCH.md, BRIEFING.md, plan.md, progress.md.
   - Start 10-minute heartbeat cron.
2. **Milestone 3 & 4 Content Generation (Parallel Workers)**:
   - Worker 1 (`worker_m3_etiqad_gen2`): Generate Section 01 (`src/content/docs/2000/01-etiqad/`, 8 MDX files: Q1–163 + 99 Names of Allah table) from `tools/extracted_2000.json`.
   - Worker 2 (`worker_m4_ibadet_gen2`): Generate Section 02 (`src/content/docs/2000/02-ibadet/`, 14 MDX files: Q164–647) from `tools/extracted_2000.json`.
   - Enforce Option B card markup and zero legacy glyphs.
3. **Verification & Audit**:
   - Dispatch Reviewers to inspect generated files and run `python3 tests/e2e_2000.py`.
   - Dispatch Challenger to stress-test boundary questions and table formatting.
   - Dispatch Forensic Auditor (`teamwork_preview_auditor`) to verify zero cheating, genuine text logic, and no hardcoded workarounds.
4. **Final Site Build & Pagefind Search Index**:
   - Verify `pnpm build` completes cleanly with exit code 0.
   - Confirm search index assets are generated.
5. **Sentinel Reporting**:
   - Send complete report with test outputs and verification evidence to the Sentinel (`e3d33290-8e81-427d-9b9d-fc995603a89d`).
