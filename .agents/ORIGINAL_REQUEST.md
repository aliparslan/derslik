# Original User Request

## 2026-09-15T01:17:38Z

Convert Part 1 of the 700-page Uyghur religious reference work "دىن ۋە ھايات (2000 سوئالغا جاۋاب)" from PDF into an organized, searchable web section under `/2000/...` in the Astro/Starlight project using Option B (continuous reading cards layout).

Working directory: `/Users/arslan/code/derslik`
Integrity mode: development

## Source Material
PDF Location: `/Users/arslan/.gemini/antigravity/brain/4cef4897-f493-4acb-b5ac-2ecb06b0aee7/.user_uploaded/media_1789428359497.pdf` (300 pages, covers Questions 1 through 647 across Divisions 1 and 2).

## Requirements

### R1. Extraction & Uyghur Unicode Normalization
Extract all text from the PDF using PyMuPDF (`fitz`). Normalize legacy Uyghur typography glyph mappings:
- Convert `\u066e` (dotless beh) -> standard Uyghur `ى` (`\u0649`).
- Convert `\u067b` (beeh with 2 vertical dots below) -> standard Uyghur `ې` (`\u06d0`).
- Convert `\u06cc` (Farsi yeh) -> standard Uyghur `ي` (`\u064a`).
- Strip interior tatweels/kashidas (`\u0640`) from words while preserving Arabic text and diacritics.

### R2. Structural Parsing & MDX Generation
Parse the normalized text into structured Markdown/MDX files under `src/content/docs/2000/`:
- **00-muqeddimu**: About the book, dedication, author biography, and foreword.
- **01-etiqad**: Questions 1 to 163 grouped logically into topical pages (Religion, God, 99 Names of Allah table, Angels, Jinn, Scripture & Prophets, Qada & Qadar, Day of Judgement).
- **02-ibadet**: Questions 164 to 647 grouped logically into topical pages (Worship basics, Shar'i terms [Farz/Wajib/Sunnah/Haram/Makruh/Mubah], Purity & Wudu, Women's rulings, Ghusl & Tayammum, Prayer rules, Prayer step-by-step, Congregational & Friday prayers, Other prayers, Funeral & Graves, Zakat, Fasting & Ramadan, Hajj & Umrah, Rewards & Sins).
- Format each question with clean question headers, highlighted numbers, answer blocks (Option B continuous card styling), and footnote citations.

### R3. 99 Names of Allah Table
Format the 99 Names of Allah table (pages 56–69) into a clean, responsive Markdown table with columns: Arabic Name, Uyghur Pronunciation, and Meaning.

### R4. Starlight Configuration & Sidebar
Update `astro.config.mjs` to add a dedicated navigation group for `2000 سوئال-جاۋاب` linking to `/2000/` and its sub-divisions with proper RTL support.

## Acceptance Criteria

### Extraction & Integrity
- [ ] All questions from 1 through 647 are extracted and present in the generated files without gaps.
- [ ] Zero occurrences of legacy glyphs (`\u066e`, `\u067b`) remain in generated files.
- [ ] The 99 Names table is fully populated and correctly formatted.

### Build & Verification
- [ ] `pnpm build` or `astro check` compiles cleanly with no syntax errors.
- [ ] The routes under `terbiye.org/2000/...` are functional and indexed for search.
