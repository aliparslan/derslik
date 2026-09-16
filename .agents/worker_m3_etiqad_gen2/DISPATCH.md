## 2026-09-15T04:41:32Z

Generate Section 01 (`src/content/docs/2000/01-etiqad/`, 8 MDX files: Q1–163 + 99 Names table) directly from `tools/extracted_2000.json` using Option B card markup, overwriting/replacing any legacy/reversed files.
1. Inspect `tools/extracted_2000.json` (contains questions 1..163 and `names_99`).
2. Generate exactly these 8 MDX files in `src/content/docs/2000/01-etiqad/`:
   - `01-din-ve-etiqad.mdx` (Q1–20, title: "دىن ۋە ئىنسان")
   - `02-allahqa-iman.mdx` (Q21–48, title: "ئاللاھقا ئىمان كەلتۈرۈش")
   - `03-allahning-isimliri.mdx` (Q49–62 + 99 Names of Allah table, title: "ئاللاھنىڭ گۈزەل ئىسىملىرى ۋە سۈپەتلىرى")
   - `04-perishtiler-jinlar.mdx` (Q63–82, title: "پەرىشتىلەر، جىنلار ۋە شەيتانلار")
   - `05-samawiy-kitablar.mdx` (Q83–96, title: "ساماۋىي كىتابلار ۋە قۇرئان كەرىم")
   - `06-peyghamberler.mdx` (Q97–115, title: "پەيغەمبەرلەرگە ئىمان كەلتۈرۈش")
   - `07-qada-qeder.mdx` (Q116–134, title: "قازا ۋە قەدەرگە ئىمان")
   - `08-qiyamet-axiret.mdx` (Q135–163, title: "قىيامەت ۋە ئاخىرەتكە ئىمان")
   Make sure to delete any obsolete files in `src/content/docs/2000/01-etiqad/` (like `04-rohiy-alemler.mdx`, `05-kitablar-peyghemberler.mdx`, `06-qaza-qeder.mdx`, `07-qiyamet-axiret.mdx`) so that there are EXACTLY 8 files in total.
3. In `03-allahning-isimliri.mdx`, include the 99 Names of Allah responsive table with columns:
   `| ئەرەبچە نامى | ئۇيغۇرچە ئوقۇلۇشى | مەنىسى |`
   populated with all 99 names from `names_99` in `tools/extracted_2000.json`.
4. Use standard Option B card markup for every question:
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
5. Run `python3 tests/e2e_2000.py --skip-build` to verify that Section 01, Q1–163, and 99 Names table tests pass.
6. Write your handoff report to `.agents/worker_m3_etiqad_gen2/handoff.md` and send a completion message to the parent orchestrator with your results.

## 2026-09-15T10:02:47Z
**Context**: Section 01 Etiqad Generation
**Content**: Heartbeat status query: What is your current progress on generating the 8 MDX files from tools/extracted_2000.json?
**Action**: Update progress.md with your latest timestamp and report status.

