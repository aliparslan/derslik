# Dispatch — orchestrator_2

## 2026-09-15T09:02:07Z
You are Project Orchestrator (Generation 2) for the conversion of Part 1 of "دىن ۋە ھايات (2000 سوئالغا جاۋاب)" at `/Users/arslan/code/derslik`.

Read your context file at `/Users/arslan/code/derslik/.agents/orchestrator_2/context.md` and `/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md`.
Maintain your own `plan.md`, `progress.md`, and `BRIEFING.md` inside `/Users/arslan/code/derslik/.agents/orchestrator_2/`.

Current State:
- Phase 0 and 1 are complete (`PROJECT.md`, `TEST_INFRA.md`, `TEST_READY.md`).
- `tests/e2e_2000.py` is ready and operational across all 4 tiers.
- `tools/extracted_2000.json` (566 KB, 7,457 lines) has all 647 questions, 99 Names, and front matter fully extracted and normalized into standard Uyghur Unicode with logical RTL word order.
- Milestone 2 (`00-muqeddimu/`, 4 MDX pages) and Milestone 5 (`astro.config.mjs`, `custom.css`, `index.mdx`) are complete.

Your Remaining Task:
1. Dispatch workers to generate Section 01 (`src/content/docs/2000/01-etiqad/`, 8 MDX files: Q1–163 + 99 Names table) and Section 02 (`src/content/docs/2000/02-ibadet/`, 14 MDX files: Q164–647) directly from `tools/extracted_2000.json` using Option B card markup, overwriting any legacy/reversed files.
2. Run `python3 tests/e2e_2000.py` and `pnpm build` via a worker to verify all 4 tiers pass cleanly.
3. When all acceptance criteria pass, report completion and full test results back to the Sentinel.

## 2026-09-15T11:31:35Z
Sentinel Resume / Liveness Nudge:
Quota reset window has long passed.
Current state:
- `01-etiqad`: All 8 target files generated (01-din-ve-etiqad through 08-qiyamet-axiret + 99 Names table). Please clean up the 4 obsolete placeholder files (`04-rohiy-alemler.mdx`, `05-kitablar-peyghemberler.mdx`, `06-qaza-qeder.mdx`, `07-qiyamet-axiret.mdx`).
- `02-ibadet`: Files 01 through 06 are completed (through Q332). Files 07 through 14 (Q333–Q647) remain to be generated.
Please resume worker execution, finish generating files 07 to 14, run `python3 tests/e2e_2000.py`, and report victory when all acceptance criteria pass.

