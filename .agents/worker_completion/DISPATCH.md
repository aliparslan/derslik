## 2026-09-15T11:35:52Z

Your working directory is /Users/arslan/code/derslik/.agents/worker_completion.
Read your context file at /Users/arslan/code/derslik/.agents/worker_completion/context.md and /Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md.
Also read /Users/arslan/code/derslik/.agents/PROJECT.md and /Users/arslan/code/derslik/.agents/TEST_READY.md.

DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Exclusively Owned Path:
You own `src/content/docs/2000/01-etiqad/` and `src/content/docs/2000/02-ibadet/`.

Tasks:
1. In `src/content/docs/2000/01-etiqad/`:
   Delete the 4 obsolete placeholder files:
   - `04-rohiy-alemler.mdx`
   - `05-kitablar-peyghemberler.mdx`
   - `06-qaza-qeder.mdx`
   - `07-qiyamet-axiret.mdx`
   Verify that exactly 8 canonical MDX files remain: `01-din-ve-etiqad.mdx`, `02-allahqa-iman.mdx`, `03-allahning-isimliri.mdx`, `04-perishtiler-jinlar.mdx`, `05-samawiy-kitablar.mdx`, `06-peyghamberler.mdx`, `07-qada-qeder.mdx`, `08-qiyamet-axiret.mdx`.
   Verify `03-allahning-isimliri.mdx` has the full 99 Names table.

2. In `src/content/docs/2000/02-ibadet/`:
   Files 01 through 06 are completed (Q164–332).
   Generate the remaining files 07 through 14 (Q333–Q647) directly from `tools/extracted_2000.json` using Option B card markup:
   - `07-namaz-oqush.mdx`: Questions 333–393 (title: "نامازنىڭ تۈزۈلۈشى ۋە ئوقۇلۇش تەرتىپى")
   - `08-jamaet-jume.mdx`: Questions 394–428 (title: "جامائەت ۋە جۈمە نامىزى")
   - `09-bashqa-namazlar.mdx`: Questions 429–477 (title: "يولۇچىلار، ھېيت ۋە باشقا نامازلار")
   - `10-jinaze-depne.mdx`: Questions 478–506 (title: "جىنازا نامىزى ۋە دەپنە ئەھكاملىرى")
   - `11-zakat.mdx`: Questions 507–553 (title: "زاكات ۋە ئۇنىڭ ئەھكاملىرى")
   - `12-roza-ramizan.mdx`: Questions 554–607 (title: "روزا ۋە رامىزان ئەھكاملىرى")
   - `13-hej-omre.mdx`: Questions 608–634 (title: "ھەج ۋە ئۆمرە پائالىيىتى")
   - `14-sawab-gunah.mdx`: Questions 635–647 (title: "ساۋاب ۋە گۇناھ ھەققىدە")

   Card markup format:
   ```html
   <div class="qa-card" id="q{number}">
     <div class="qa-question">
       <span class="qa-number">{number}</span>
       <span class="qa-label">سوئال:</span> {question}
     </div>
     <div class="qa-answer">
       <span class="qa-label">جاۋاب:</span> {answer}
     </div>
   </div>
   ```

3. Verification:
   Run `python3 tests/e2e_2000.py` across all 4 tiers.
   Run `pnpm build` to verify the site builds cleanly and Pagefind search index is generated.

4. Write `handoff.md` and send a message back to the parent orchestrator with full test output.
