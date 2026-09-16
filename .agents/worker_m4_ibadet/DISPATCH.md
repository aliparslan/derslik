## 2026-09-15T05:44:02Z
Your identity: Section 02 (Ibadet) Content Worker
Working directory: /Users/arslan/code/derslik/.agents/worker_m4_ibadet/
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
`src/content/docs/2000/02-ibadet/`
DO NOT touch any other directory or file.

Your objective:
Generate the 14 MDX documentation pages under `src/content/docs/2000/02-ibadet/` using the verified data in `/Users/arslan/code/derslik/tools/extracted_2000.json` (covering Questions 164 through 647):
1. `01-ibadet-esasliri.mdx`: Questions 164 to 183 (Worship basics, conditions of acceptance, puberty).
2. `02-sheriy-atalghular.mdx`: Questions 184 to 204 (Shar'i terms: Farz, Wajib, Sunnah, Haram, Makruh, Mubah).
3. `03-pakizliq-taharet.mdx`: Questions 205 to 248 (Purity, types of water, istinja, wudu rules & nullifiers, socks wiping).
4. `04-ayallar-ehkami.mdx`: Questions 249 to 259 (Women's rulings: menses, postnatal, istihada).
5. `05-ghusli-teyemmum.mdx`: Questions 260 to 274 (Ghusl methods & obligations, Tayammum).
6. `06-namaz-ehkamliri.mdx`: Questions 275 to 332 (Prayer importance, Khushu, 5 prayer times, adhan, awrah, qiblah, rakat count).
7. `07-namaz-tertibi.mdx`: Questions 333 to 393 (Prayer step-by-step, Witr, du'as, Sajdah Sahw, Qada prayers, joining prayers).
8. `08-jamaet-jume.mdx`: Questions 394 to 428 (Congregational prayer, Imamate, Friday prayer rulings, Khutbah).
9. `09-bashqa-namazlar.mdx`: Questions 429 to 477 (Traveler's prayer, Eid prayers, Tarawih, Sick person's prayer, Eclipse, Istisqa, Nawafil).
10. `10-jinaza-qebre.mdx`: Questions 478 to 506 (Funeral prayer, washing, shrouding, burial, graves, martyr).
11. `11-zakat.mdx`: Questions 507 to 553 (Zakat obligations, Nisab, eligible recipients, questions & answers).
12. `12-roza-ramizan.mdx`: Questions 554 to 607 (Fasting rules, nullifiers, Kaffarah, Qada, Ramadan blessings, Fidya, Fitr charity, Itikaf).
13. `13-hej-omre.mdx`: Questions 608 to 634 (Hajj & Umrah, types of Hajj, Ihram, women's rulings, ritual steps, Qurbanliq).
14. `14-sawab-gunah.mdx`: Questions 635 to 647 (Sins & Rewards: virtuous deeds, major and minor sins, list of forbidden matters).

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
Write your handoff report to `/Users/arslan/code/derslik/.agents/worker_m4_ibadet/handoff.md`.
Send a completion message back to parent when done.
