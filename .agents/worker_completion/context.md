# Context: Worker Completion (Finish 01 Cleanup, 02 Generation, and E2E Tests)

## Mission
1. In `src/content/docs/2000/01-etiqad/`:
   Delete the 4 obsolete placeholder files:
   - `04-rohiy-alemler.mdx`
   - `05-kitablar-peyghemberler.mdx`
   - `06-qaza-qeder.mdx`
   - `07-qiyamet-axiret.mdx`
   Verify that exactly the 8 canonical MDX files remain: `01-din-ve-etiqad.mdx`, `02-allahqa-iman.mdx`, `03-allahning-isimliri.mdx`, `04-perishtiler-jinlar.mdx`, `05-samawiy-kitablar.mdx`, `06-peyghamberler.mdx`, `07-qada-qeder.mdx`, `08-qiyamet-axiret.mdx`.

2. In `src/content/docs/2000/02-ibadet/`:
   Files 01 through 06 are completed.
   Generate the remaining files 07 through 14 (Q333–Q647) directly from `/Users/arslan/code/derslik/tools/extracted_2000.json` using Option B card markup:
   - `07-namaz-oqush.mdx`: Questions 333–393 (title: "نامازنىڭ تۈزۈلۈشى ۋە ئوقۇلۇش تەرتىپى")
   - `08-jamaet-jume.mdx`: Questions 394–428 (title: "جامائەت ۋە جۈمە نامىزى")
   - `09-bashqa-namazlar.mdx`: Questions 429–477 (title: "يولۇچىلار، ھېيت ۋە باشقا نامازلار")
   - `10-jinaze-depne.mdx`: Questions 478–506 (title: "جىنازا نامىزى ۋە دەپنە ئەھكاملىرى")
   - `11-zakat.mdx`: Questions 507–553 (title: "زاكات ۋە ئۇنىڭ ئەھكاملىرى")
   - `12-roza-ramizan.mdx`: Questions 554–607 (title: "روزا ۋە رامىزان ئەھكاملىرى")
   - `13-hej-omre.mdx`: Questions 608–634 (title: "ھەج ۋە ئۆمرە پائالىيىتى")
   - `14-sawab-gunah.mdx`: Questions 635–647 (title: "ساۋاب ۋە گۇناھ ھەققىدە")

3. Run `python3 tests/e2e_2000.py` across all 4 tiers.
4. Run `pnpm build` and ensure exit code 0.
5. Record full test execution details in `handoff.md` and report back to parent orchestrator.
