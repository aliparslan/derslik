## 2026-09-15T13:02:12Z

You are Worker B. Your working directory is `/Users/arslan/code/derslik/.agents/worker_gen3_ibadet_b/`.
Read `/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

CRITICAL INSTRUCTION: DO NOT use `run_command`. Use `view_file` to read `tools/extracted_2000.json` and use `write_to_file` to generate the MDX files directly.

Your assigned files:
1. `src/content/docs/2000/02-ibadet/09-bashqa-namazlar.mdx`:
   - Title: "باشقا نامازلار"
   - Description: "باشقا نامازلار — سوئال 429–477"
   - Sidebar label: "باشقا نامازلار", order: 9
   - Covers Questions 429 through 477 (located around lines 4961–5531 in `tools/extracted_2000.json`).

2. `src/content/docs/2000/02-ibadet/10-jinaze-depne.mdx`:
   - Title: "جىنازە ۋە دەپنە"
   - Description: "جىنازە ۋە دەپنە — سوئال 478–506"
   - Sidebar label: "جىنازە ۋە دەپنە", order: 10
   - Covers Questions 478 through 506 (located around lines 5532–5855 in `tools/extracted_2000.json`).

Option B Card markup for each question:
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

Use `write_to_file` with Overwrite=True to write each file.
Write your handoff report to `/Users/arslan/code/derslik/.agents/worker_gen3_ibadet_b/handoff.md` and send a message back to parent (`65f8e8f1-2fca-49a7-8b3f-c817ab097747`).
