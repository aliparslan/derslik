## 2026-09-15T01:46:37Z

Your identity: Extraction Pipeline Worker
Working directory: /Users/arslan/code/derslik/.agents/worker_m1_extractor/
Parent conversation ID: 402b5da9-8a97-44a9-a924-d815f3a13527

MANDATORY FIRST STEP: Read the full verbatim requirements at:
/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md
Also read:
- /Users/arslan/code/derslik/.agents/PROJECT.md
- /Users/arslan/code/derslik/.agents/spec_miner_pdf_structure/handoff.md and analysis.md
- /Users/arslan/code/derslik/.agents/spec_miner_99names_divisions/analysis.md
- /Users/arslan/code/derslik/.agents/explorer_survey_codebase/handoff.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your objective:
Build the end-to-end Python extraction and normalization pipeline in `tools/extract_2000.py` to extract all content from the source PDF at:
`/Users/arslan/.gemini/antigravity/brain/4cef4897-f493-4acb-b5ac-2ecb06b0aee7/.user_uploaded/media_1789428359497.pdf`

Specific technical requirements:
1. Use PyMuPDF (`fitz`).
2. Implement proper logical RTL line reconstruction so words appear in natural Uyghur reading order (resolve the word-order reversal issue discovered in previous attempts).
3. Apply Uyghur Unicode normalization:
   - `\u066e` -> `\u0649` (`ى`)
   - `\u067b` -> `\u06d0` (`ې`)
   - `\u06cc` -> `\u064a` (`ي`)
   - Strip interior tatweels/kashidas (`\u0640`) within words, while preserving Arabic text and diacritics.
4. Extract all 647 questions (1 through 647):
   - Regex matching for `.N سوئال:` or `N. سوئال:` and `جاۋاب:`.
   - Keep answers associated with their questions.
   - Clean and attach footnotes.
5. Extract the 99 Names of Allah from PDF pages 56–69:
   - Parse all 3 columns: Arabic Name (with tashkeel), Uyghur Pronunciation, and Meaning.
   - Verify count is exactly 99.
6. Extract front matter (Section 00):
   - Book title, CIP data, Dedication, Author Biography, Foreword, Table of Contents.
7. Output cleanly structured JSON data (e.g. `tools/extracted_2000.json`) and run verification checks asserting:
   - Question count is 647.
   - Missing questions count is 0.
   - Legacy glyph count is 0.
   - 99 Names count is 99.
8. Document execution commands and verification results in `/Users/arslan/code/derslik/.agents/worker_m1_extractor/handoff.md`.
9. Send a message to parent when completed.
