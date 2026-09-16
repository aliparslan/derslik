# Dispatch Assignment — Orchestrator Generation 3

## 2026-09-15T11:58:37Z

You are Project Orchestrator (Generation 3) for the conversion of Part 1 of "دىن ۋە ھايات (2000 سوئالغا جاۋاب)" at `/Users/arslan/code/derslik`.

Read your context file at `/Users/arslan/code/derslik/.agents/orchestrator_3/context.md` and `/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md`.
Maintain your own `plan.md`, `progress.md`, and `BRIEFING.md` inside `/Users/arslan/code/derslik/.agents/orchestrator_3/`.

Current State:
- `tools/extracted_2000.json` (566 KB) has all 647 questions, 99 Names, and front matter fully extracted and normalized.
- `00-muqeddimu/` (4 MDX files) is 100% complete.
- `01-etiqad/`: All 8 target files (Q1–163 + 99 Names table) are 100% complete. Just delete the 4 obsolete skeleton files (`04-rohiy-alemler.mdx`, `05-kitablar-peyghemberler.mdx`, `06-qaza-qeder.mdx`, `07-qiyamet-axiret.mdx`).
- `02-ibadet/`: Files 01 through 06 (Q164–Q332) are 100% complete.
- `astro.config.mjs`, `custom.css`, and `index.mdx` are complete.
- `tests/e2e_2000.py` is ready.

Your Remaining Task:
1. Dispatch a worker to:
   - Remove the 4 obsolete skeleton files in `01-etiqad/`.
   - Generate remaining files 07 through 14 (Q333–Q647) in `src/content/docs/2000/02-ibadet/` directly from `tools/extracted_2000.json` using Option B card markup.
   - Run `python3 tests/e2e_2000.py` across all 4 tiers and verify 100% pass.
   - Run `pnpm build` and verify clean build.
2. Report project completion to the Sentinel with test evidence.
