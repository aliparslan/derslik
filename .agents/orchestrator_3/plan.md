# Execution Plan — Orchestrator Generation 3

## Objective
Finalize Section 02 (Q333–Q647), clean up Section 01 obsolete files, run complete 4-tier E2E test suite and `pnpm build`, and report completion to Sentinel.

## Milestones

### Milestone 1: Implementation & Section Cleanup
- Create working directory `.agents/worker_gen3_1/`.
- Dispatch `teamwork_preview_worker` to:
  1. Remove the 4 obsolete skeleton files in `src/content/docs/2000/01-etiqad/`:
     - `04-rohiy-alemler.mdx`
     - `05-kitablar-peyghemberler.mdx`
     - `06-qaza-qeder.mdx`
     - `07-qiyamet-axiret.mdx`
  2. Write/run generator script or directly generate files 07–14 in `src/content/docs/2000/02-ibadet/` from `tools/extracted_2000.json`:
     - `07-namaz-oqush.mdx`: Q333–393, title: "ناماز ئوقۇش تەرتىبى", order: 7
     - `08-jamaet-jume.mdx`: Q394–428, title: "جامائەت ۋە جۈمە نامازى", order: 8
     - `09-bashqa-namazlar.mdx`: Q429–477, title: "باشقا نامازلار", order: 9
     - `10-jinaze-depne.mdx`: Q478–506, title: "جىنازە ۋە دەپنە", order: 10
     - `11-zakat.mdx`: Q507–553, title: "زاكات ئەھكاملىرى", order: 11
     - `12-roza-ramizan.mdx`: Q554–607, title: "روزا ۋە رامىزان", order: 12
     - `13-hej-omre.mdx`: Q608–634, title: "ھەج ۋە ئۈمرە", order: 13
     - `14-sawab-gunah.mdx`: Q635–647, title: "ساۋاب ۋە گۇناھ", order: 14
     Using Option B card markup: `<div class="qa-card" id="q{N}">...` and footnote handling.
  3. Execute `python3 tests/e2e_2000.py` across all 4 tiers and verify 100% pass.
  4. Execute `pnpm build` and verify clean exit code 0.
  5. Write detailed report in `.agents/worker_gen3_1/handoff.md`.

### Milestone 2: Independent Review & Verification
- Review worker findings and test results.
- Verify that question count is 647, zero legacy glyphs remain, 99 Names table is populated, and build succeeded.

### Milestone 3: Sentinel Completion Report
- Send comprehensive completion report to Sentinel (`e3d33290-8e81-427d-9b9d-fc995603a89d`) with test execution results.
