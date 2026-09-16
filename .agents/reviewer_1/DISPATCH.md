# DISPATCH — reviewer_1

## 2026-09-15T20:25:00Z

### Identity & Context
- Role: Independent Reviewer 1 (archetype: `teamwork_preview_reviewer`)
- Working Directory: `/Users/arslan/code/derslik/.agents/reviewer_1/`
- Project Root: `/Users/arslan/code/derslik`
- Original Request: `/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md`
- Project Architecture & Scope: `/Users/arslan/code/derslik/.agents/PROJECT.md`
- Test Specification: `/Users/arslan/code/derslik/.agents/TEST_READY.md`
- Test Harness: `/Users/arslan/code/derslik/tests/e2e_2000.py`
- Worker Handoff: `/Users/arslan/code/derslik/.agents/worker_cleanup_e2e/handoff.md`

### Mission & Instructions
You MUST read the authoritative request first:
`/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md`

Perform an exhaustive, independent review of the conversion of Part 1 of "دىن ۋە ھايات (2000 سوئالغا جاۋاب)":
1. Verify feature coverage and structural integrity:
   - Front matter in `src/content/docs/2000/00-muqeddimu/` (4 files: `01-kitab-heqqide.mdx`, `02-aptur-heqqide.mdx`, `03-kirish-soz.mdx`, `04-munderije.mdx`).
   - Section 01 in `src/content/docs/2000/01-etiqad/`: verify 8 canonical files covering Q1–163, and inspect the 4 obsolete skeleton files reported by worker.
   - 99 Names of Allah table in `01-etiqad/03-allahning-isimliri.mdx`: verify 99 rows, 3 columns (Arabic vocalized with tashkeel, Uyghur pronunciation, Uyghur meaning).
   - Section 02 in `src/content/docs/2000/02-ibadet/`: verify 14 canonical files covering Q164–647.
   - Question card markup: Option B styling (`.qa-card`, `.qa-question`, `.qa-number`, `.qa-answer`).
   - Unicode normalization: 0 occurrences of `\u066e`, `\u067b`, and 0 interior tatweels inside Uyghur words.
   - Starlight configuration in `astro.config.mjs` and CSS in `src/styles/custom.css`.
2. Evaluate test and build readiness:
   - Check compliance with `TEST_READY.md` across Tiers 1 through 4.
3. Write your review report in `/Users/arslan/code/derslik/.agents/reviewer_1/handoff.md` with your explicit verdict: `APPROVE` or `REQUEST_CHANGES`.
4. Send your verdict and summary to orchestrator_7.
