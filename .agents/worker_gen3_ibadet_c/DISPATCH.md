## 2026-09-15T08:02:12Z

Target files:
1. `src/content/docs/2000/02-ibadet/11-zakat.mdx`:
   - Title: "زاكات ئەھكاملىرى"
   - Description: "زاكات ئەھكاملىرى — سوئال 507–553"
   - Sidebar label: "زاكات ئەھكاملىرى", order: 11
   - Covers Questions 507 through 553 (located around lines 5856–6395 in `tools/extracted_2000.json`).

2. `src/content/docs/2000/02-ibadet/12-roza-ramizan.mdx`:
   - Title: "روزا ۋە رامىزان"
   - Description: "روزا ۋە رامىزان — سوئال 554–607"
   - Sidebar label: "روزا ۋە رامىزان", order: 12
   - Covers Questions 554 through 607 (located around lines 6396–6996 in `tools/extracted_2000.json`).

3. `src/content/docs/2000/02-ibadet/13-hej-omre.mdx`:
   - Title: "ھەج ۋە ئۈمرە"
   - Description: "ھەج ۋە ئۈمرە — سوئال 608–634"
   - Sidebar label: "ھەج ۋە ئۈمرە", order: 13
   - Covers Questions 608 through 634 (located around lines 6997–7312 in `tools/extracted_2000.json`).

Option B Card markup:
```html
<div class="qa-card" id="q{number}">
  <div class="qa-question">
    <span class="qa-number">{number}</span>
    <span class="qa-label">سوئال:</span> {question}
  </div>
  <div class="qa-answer">
    <span class="qa-label">جاۋاب:</span> {answer}
    {if footnotes exist:
    <div class="qa-footnotes" style="margin-top: 0.75rem; font-size: 0.85rem; opacity: 0.8;"><span>[{fn}]</span></div>
    }
  </div>
</div>
```
Text cleaning:
- Normalize legacy glyphs: \u066e -> \u0649, \u067b -> \u06d0, \u06cc -> \u064a.
- Strip interior tatweels/kashidas (\u0640) between letters.

CRITICAL INSTRUCTION: DO NOT use run_command. Use view_file to read tools/extracted_2000.json and use write_to_file to generate the MDX files directly.
