## 2026-09-15T12:06:00Z

You are a Worker subagent assigned to complete the remaining tasks for the conversion of Part 1 of "دىن ۋە ھايات (2000 سوئالغا جاۋاب)".

Your working directory is: `/Users/arslan/code/derslik/.agents/worker_gen3_1/`
Read the original user request at: `/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md`

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your Tasks:
1. Delete the 4 obsolete skeleton files in `src/content/docs/2000/01-etiqad/`:
   - `04-rohiy-alemler.mdx`
   - `05-kitablar-peyghemberler.mdx`
   - `06-qaza-qeder.mdx`
   - `07-qiyamet-axiret.mdx`
   Verify that exactly the 8 canonical files remain in `01-etiqad/`:
   `01-din-ve-etiqad.mdx`, `02-allahqa-iman.mdx`, `03-allahning-isimliri.mdx`, `04-perishtiler-jinlar.mdx`, `05-samawiy-kitablar.mdx`, `06-peyghamberler.mdx`, `07-qada-qeder.mdx`, `08-qiyamet-axiret.mdx`.

2. Generate remaining files 07 through 14 (Q333–Q647) in `src/content/docs/2000/02-ibadet/` directly from `tools/extracted_2000.json` using Option B card markup:
   - `07-namaz-oqush.mdx`: Q333–393, title: "ناماز ئوقۇش تەرتىبى", description: "ناماز ئوقۇش تەرتىبى — سوئال 333–393", order: 7
   - `08-jamaet-jume.mdx`: Q394–428, title: "جامائەت ۋە جۈمە نامازى", description: "جامائەت ۋە جۈمە نامازى — سوئال 394–428", order: 8
   - `09-bashqa-namazlar.mdx`: Q429–477, title: "باشقا نامازلار", description: "باشقا نامازلار — سوئال 429–477", order: 9
   - `10-jinaze-depne.mdx`: Q478–506, title: "جىنازە ۋە دەپنە", description: "جىنازە ۋە دەپنە — سوئال 478–506", order: 10
   - `11-zakat.mdx`: Q507–553, title: "زاكات ئەھكاملىرى", description: "زاكات ئەھكاملىرى — سوئال 507–553", order: 11
   - `12-roza-ramizan.mdx`: Q554–607, title: "روزا ۋە رامىزان", description: "روزا ۋە رامىزان — سوئال 554–607", order: 12
   - `13-hej-omre.mdx`: Q608–634, title: "ھەج ۋە ئۈمرە", description: "ھەج ۋە ئۈمرە — سوئال 608–634", order: 13
   - `14-sawab-gunah.mdx`: Q635–647, title: "ساۋاب ۋە گۇناھ", description: "ساۋاب ۋە گۇناھ — سوئال 635–647", order: 14

   Check existing implementation patterns in `tools/generate_01_etiqad.py` and `src/content/docs/2000/02-ibadet/01-ibadet-esasliri.mdx` through `06-namaz-ehkamliri.mdx`.
   Ensure clean Uyghur text normalization:
   - Convert `\u066e` -> `\u0649`
   - Convert `\u067b` -> `\u06d0`
   - Convert `\u06cc` -> `\u064a`
   - Strip interior tatweels/kashidas (`\u0640`) between Uyghur letters.
   - Format each question card with:
     `<div class="qa-card" id="q{number}">`
       `<div class="qa-question">`
         `<span class="qa-number">{number}</span>`
         `<span class="qa-label">سوئال:</span> {question}`
       `</div>`
       `<div class="qa-answer">`
         `<span class="qa-label">جاۋاب:</span> {answer}`
         `{footnotes div if footnotes exist}`
       `</div>`
     `</div>`
   You can write a python generator script (e.g. `tools/generate_02_ibadet.py`) and execute it.

3. Run the full test suite and build:
   - Run `python3 tests/e2e_2000.py` and verify all 4 tiers pass with 100% success.
   - Run `pnpm build` and verify it succeeds with exit code 0.

4. Write a comprehensive handoff report to `/Users/arslan/code/derslik/.agents/worker_gen3_1/handoff.md` with:
   - Summary of files deleted in 01-etiqad
   - Summary of files generated in 02-ibadet with question counts
   - Full output of `python3 tests/e2e_2000.py`
   - Full output of `pnpm build`
   - Verification status

When done, use `send_message` to report back to your parent orchestrator (`65f8e8f1-2fca-49a7-8b3f-c817ab097747`).
