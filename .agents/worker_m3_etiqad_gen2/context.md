# Context: Worker Milestone 3 (Section 01 Etiqad & 99 Names Table)

## Mission
Generate Section 01 (`src/content/docs/2000/01-etiqad/`, 8 MDX files: Q1–163 + 99 Names of Allah table) directly from `/Users/arslan/code/derslik/tools/extracted_2000.json` using Option B card markup, overwriting/replacing any legacy/reversed files.

## Exclusively Owned Path
`src/content/docs/2000/01-etiqad/`
You MUST NOT write to any other content directories.

## Specifications
1. Read `/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md` and `/Users/arslan/code/derslik/.agents/PROJECT.md`.
2. Inspect `/Users/arslan/code/derslik/tools/extracted_2000.json`.
3. Generate exactly 8 MDX files in `src/content/docs/2000/01-etiqad/`:
   - `01-din-ve-etiqad.mdx`: Questions 1–20 (title: "دىن ۋە ئىنسان")
   - `02-allahqa-iman.mdx`: Questions 21–48 (title: "ئاللاھقا ئىمان كەلتۈرۈش")
   - `03-allahning-isimliri.mdx`: Questions 49–62 + 99 Names of Allah table (title: "ئاللاھنىڭ گۈزەل ئىسىملىرى ۋە سۈپەتلىرى")
   - `04-perishtiler-jinlar.mdx`: Questions 63–82 (title: "پەرىشتىلەر، جىنلار ۋە شەيتانلار")
   - `05-samawiy-kitablar.mdx`: Questions 83–96 (title: "ساماۋىي كىتابلار ۋە قۇرئان كەرىم")
   - `06-peyghamberler.mdx`: Questions 97–115 (title: "پەيغەمبەرلەرگە ئىمان كەلتۈرۈش")
   - `07-qada-qeder.mdx`: Questions 116–134 (title: "قازا ۋە قەدەرگە ئىمان")
   - `08-qiyamet-axiret.mdx`: Questions 135–163 (title: "قىيامەت ۋە ئاخىرەتكە ئىمان")
   Delete any other stale .mdx or .md files in `src/content/docs/2000/01-etiqad/` so there are exactly 8 files.
4. Card Markup (Option B):
   ```html
   <div class="qa-card" id="q1">
     <div class="qa-question">
       <span class="qa-number">1</span>
       <span class="qa-label">سوئال:</span> ئىنسانلار نەدىن پەيدا بولغان؟
     </div>
     <div class="qa-answer">
       <span class="qa-label">جاۋاب:</span> ئىنسانلار ئاللاھ تەرىپىدىن يارىتىلغان.
     </div>
   </div>
   ```
5. 99 Names of Allah Table in `03-allahning-isimliri.mdx`:
   Must have 99 rows and 3 columns:
   `| ئەرەبچە نامى | ئۇيغۇرچە ئوقۇلۇشى | مەنىسى |`
   Data from `names_99` in `extracted_2000.json`.
6. Run `python3 tests/e2e_2000.py --skip-build` to verify tests pass.
7. Write `handoff.md` and report back to parent.
