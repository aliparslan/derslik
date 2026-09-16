## 2026-09-15T01:46:37Z
Your identity: E2E Test Suite Writer
Working directory: /Users/arslan/code/derslik/.agents/test_writer_e2e/
Parent conversation ID: 402b5da9-8a97-44a9-a924-d815f3a13527

MANDATORY FIRST STEP: Read the full verbatim requirements at:
/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md
Also read:
- /Users/arslan/code/derslik/.agents/PROJECT.md
- /Users/arslan/code/derslik/.agents/TEST_INFRA.md

Your objective:
Build the comprehensive, opaque-box E2E test suite in `tests/e2e_2000.py` derived strictly from user requirements and acceptance criteria.
The test suite must independently verify:
1. Tier 1 - Feature Coverage:
   - Verification of Question Count: exactly 647 questions extracted and formatted across `src/content/docs/2000/`.
   - Verification of Question Number Set: `set(range(1, 648))` matches all question numbers found in `qa-number` spans or IDs.
   - Verification of Question Structure: every question has question text, answer text, and proper HTML/MDX structure.
   - Verification of Section 00: all 4 pages exist (`01-kitab-heqqide.mdx`, `02-aptur-heqqide.mdx`, `03-kirish-soz.mdx`, `04-munderije.mdx`) with non-empty content.
   - Verification of Section 01: 8 pages exist with correct question boundaries (Q1-163).
   - Verification of Section 02: 14 pages exist with correct question boundaries (Q164-647).
2. Tier 2 - Boundary & Integrity Tests:
   - Zero occurrences of `\u066e` (dotless beh) across all generated files under `src/content/docs/2000/`.
   - Zero occurrences of `\u067b` (beeh with 2 dots below) across all generated files under `src/content/docs/2000/`.
   - Zero occurrences of interior tatweel/kashida (`\u0640`) in Uyghur words.
   - Boundary checks: Question 1, Question 48, Question 49, Question 163, Question 164, Question 647 verbatim integrity and non-empty answers.
3. Tier 3 - 99 Names of Allah Table & Cross-Feature Verification:
   - Presence of 99 Names table in `src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx`.
   - Table has exactly 99 rows.
   - All 3 columns (Arabic Name, Uyghur Pronunciation, Meaning) are populated for all 99 names.
   - Option B CSS presence: `src/styles/custom.css` contains `.qa-card`, `.qa-question`, `.qa-answer`, `.qa-number`.
   - Navigation config: `astro.config.mjs` contains sidebar navigation for `2000 سوئال-جاۋاب`.
4. Tier 4 - Build & Search Validation:
   - Full site build via `pnpm build`.
   - Pagefind search index generation check in `dist/pagefind/`.

Write `tests/e2e_2000.py` and run it to verify its syntax and execution logic.
When the test harness is complete and ready, create `/Users/arslan/code/derslik/.agents/TEST_READY.md` (and at project root `/Users/arslan/code/derslik/TEST_READY.md`) with the test runner command and tier summary.
Write your handoff report to `/Users/arslan/code/derslik/.agents/test_writer_e2e/handoff.md`.
Send a completion message back to parent (conversation ID: 402b5da9-8a97-44a9-a924-d815f3a13527).
