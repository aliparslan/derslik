## 2026-09-15T07:49:01Z

Your identity: Comprehensive Content Generator Worker
Working directory: /Users/arslan/code/derslik/.agents/worker_content_generator/
Parent conversation ID: 402b5da9-8a97-44a9-a924-d815f3a13527

MANDATORY FIRST STEP: Read the full verbatim requirements at:
/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md
Also read:
- /Users/arslan/code/derslik/.agents/PROJECT.md
- /Users/arslan/code/derslik/.agents/TEST_READY.md
- /Users/arslan/code/derslik/tests/e2e_2000.py

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

File Write Boundaries:
You exclusively own:
- `src/content/docs/2000/01-etiqad/`
- `src/content/docs/2000/02-ibadet/`
- `tools/generate_all_mdx.py`

Your objective:
Generate all MDX content files for Section 01 (Etiqad, Q1-163 & 99 Names) and Section 02 (Ibadet, Q164-647) by writing and executing a Python script `tools/generate_all_mdx.py` that reads the complete, verified extraction data in `/Users/arslan/code/derslik/tools/extracted_2000.json`.

Section 01 (01-etiqad) requires exactly 8 MDX files:
1. `01-din-ve-etiqad.mdx`: Q1 to Q34
2. `02-allahqa-iman.mdx`: Q35 to Q48, Q49 to Q62
3. `03-allahning-isimliri.mdx`: The 99 Names of Allah Table (all 99 names from `names_99` with columns: Arabic Name, Uyghur Pronunciation, Meaning) plus introductory hadith and notes
4. `04-perishtilerge-iman.mdx`: Q63 to Q72
5. `05-jinlar-ve-sheytanlar.mdx`: Q73 to Q82
6. `06-kitablar-peyghemberler.mdx`: Q83 to Q115
7. `07-qaza-qeder.mdx`: Q116 to Q134
8. `08-qiyamet-axiret.mdx`: Q135 to Q163

Section 02 (02-ibadet) requires exactly 14 MDX files:
1. `01-ibadet-esasliri.mdx`: Q164 to Q183
2. `02-sheriy-atalghular.mdx`: Q184 to Q204
3. `03-pakizliq-taharet.mdx`: Q205 to Q248
4. `04-ayallar-ehkami.mdx`: Q249 to Q259
5. `05-ghusli-teyemmum.mdx`: Q260 to Q274
6. `06-namaz-ehkamliri.mdx`: Q275 to Q332
7. `07-namaz-tertibi.mdx`: Q333 to Q393
8. `08-jamaet-jume.mdx`: Q394 to Q428
9. `09-bashqa-namazlar.mdx`: Q429 to Q477
10. `10-jinaza-qebre.mdx`: Q478 to Q506
11. `11-zakat.mdx`: Q507 to Q553
12. `12-roza-ramizan.mdx`: Q554 to Q607
13. `13-hej-omre.mdx`: Q608 to Q634
14. `14-sawab-gunah.mdx`: Q635 to Q647

Card Formatting Requirements (Option B):
Every question must be formatted as:
```html
<div class="qa-card" id="q{number}">
  <div class="qa-question">
    <span class="qa-number">{number}</span>
    <span class="qa-text">سوئال: {question}</span>
  </div>
  <div class="qa-answer">
    جاۋاب: {answer}
  </div>
</div>
```

Every page must have valid Starlight YAML frontmatter:
```yaml
---
title: "..."
description: "..."
---
```

After generating all files, run:
`/usr/bin/python3 tests/e2e_2000.py --skip-build`
and verify that Tiers 1, 2, and 3 pass cleanly.
Write your handoff report to `/Users/arslan/code/derslik/.agents/worker_content_generator/handoff.md` and send a message back to parent.
