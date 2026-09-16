## 2026-09-15T05:44:02Z
Your identity: Section 01 (Etiqad & 99 Names) Content Worker
Working directory: /Users/arslan/code/derslik/.agents/worker_m3_etiqad/
Parent conversation ID: 402b5da9-8a97-44a9-a924-d815f3a13527

MANDATORY FIRST STEP: Read the full verbatim requirements at:
/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md
Also read:
- /Users/arslan/code/derslik/.agents/PROJECT.md
- /Users/arslan/code/derslik/.agents/TEST_READY.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

File Write Boundaries:
You exclusively own all files inside:
`src/content/docs/2000/01-etiqad/`
DO NOT touch any other directory or file.

Your objective:
Generate the 8 MDX documentation pages under `src/content/docs/2000/01-etiqad/` using the verified data in `/Users/arslan/code/derslik/tools/extracted_2000.json` (covering Questions 1 through 163 and the 99 Names of Allah table):
1. `01-din-ve-etiqad.mdx`: Introductory essays + Questions 1 to 34 (Religion, Intellect, Faith basics).
2. `02-allahqa-iman.mdx`: Questions 35 to 48 and Questions 49 to 62 (Belief in Allah, Attributes).
3. `03-allahning-isimliri.mdx`: The 99 Names of Allah Table (pages 56–69). Format as a clean, responsive table with 3 columns:
   - Arabic Name (`ئىسىم`) vocalized with full Arabic diacritics/tashkeel.
   - Uyghur Pronunciation (`ئوقۇلۇشى`).
   - Uyghur Meaning & Theological Definition (`مەنىسى`).
   Ensure ALL 99 names from `names_99` in `tools/extracted_2000.json` are present. Include introductory hadith context and concluding notes.
4. `04-perishtilerge-iman.mdx`: Questions 63 to 72 (Angels).
5. `05-jinlar-ve-sheytanlar.mdx`: Questions 73 to 82 (Jinn & Devils).
6. `06-kitablar-peyghemberler.mdx`: Questions 83 to 115 (Scriptures, Prophets, Muhammad SAW, Durood).
7. `07-qaza-qeder.mdx`: Questions 116 to 134 (Qada and Qadar, Free Will, Tawakkul).
8. `08-qiyamet-axiret.mdx`: Questions 135 to 163 (Day of Judgement, Barzakh, Grave, Resurrection, Heaven & Hell).

Formatting:
- Each question MUST use Option B continuous reading card styling:
```html
<div class="qa-card" id="q{N}">
  <div class="qa-question">
    <span class="qa-number">{N}</span>
    <span class="qa-text">سوئال: {question_text}</span>
  </div>
  <div class="qa-answer">
    جاۋاب: {answer_text}
  </div>
</div>
```
- Valid YAML frontmatter on each page (`title`, `description`).
- Zero legacy glyphs (`\u066e`, `\u067b`).
Write your handoff report to `/Users/arslan/code/derslik/.agents/worker_m3_etiqad/handoff.md`.
Send a completion message back to parent when done.
