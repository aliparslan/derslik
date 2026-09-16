# Project: Din ve Hayat (2000 Sualliq) Part 1 Conversion

## Architecture
The conversion system consists of:
1. **Extraction & Normalization Engine**: Python script using PyMuPDF (`fitz`) to parse raw text from the 300-page source PDF, reconstructing logical RTL word order for lines, applying Uyghur Unicode normalization (`\u066e` -> `\u0649`, `\u067b` -> `\u06d0`, `\u06cc` -> `\u064a`, stripping interior `\u0640` tatweels), extracting footnotes, and structuring Question/Answer blocks.
2. **Content Generation Module**: Converts structured JSON/dictionaries into clean, valid Starlight MDX files under `src/content/docs/2000/`:
   - `00-muqeddimu/` (Front matter, dedication, author biography, foreword, table of contents)
   - `01-etiqad/` (Questions 1 to 163 across 8 topical pages + 99 Names table)
   - `02-ibadet/` (Questions 164 to 647 across 14 topical pages)
   - `index.mdx` (Section landing page with overview and directory links)
3. **Starlight UI & Navigation Configuration**:
   - `astro.config.mjs`: Starlight sidebar group `2000 سوئال-جاۋاب` with nested sections.
   - `src/styles/custom.css`: Option B continuous reading card styling (`.qa-card`, `.qa-question`, `.qa-answer`, `.qa-number`) with responsive RTL logical properties.
4. **E2E Testing Harness**:
   - Automated test runner verifying question continuity (1..647 without missing numbers), legacy glyph absence, 99 Names table completeness, and `pnpm build` verification.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | PDF Text & RTL Extraction | Extract text using PyMuPDF with logical RTL line reconstruction | M1 | Survey |
| 2 | Legacy Unicode Normalization | Replace `\u066e`->`\u0649`, `\u067b`->`\u06d0`, `\u06cc`->`\u064a`, strip interior `\u0640` | M1 | ORIGINAL_REQUEST §R1 |
| 3 | Footnote & Citation Extraction | Extract per-page footnotes and map to scoped markdown footnotes | M1 | Survey |
| 4 | Section 00 (Muqeddimu) Content | Generate 4 MDX pages: book info, bio, foreword, TOC | M2 | ORIGINAL_REQUEST §R2 |
| 5 | Section 01 (Etiqad) Content | Generate 8 MDX pages covering Questions 1 to 163 | M3 | ORIGINAL_REQUEST §R2 |
| 6 | 99 Names of Allah Table | Generate responsive 3-column table (Arabic, Uyghur transliteration, meaning) | M3 | ORIGINAL_REQUEST §R3 |
| 7 | Section 02 (Ibadet) Content | Generate 14 MDX pages covering Questions 164 to 647 | M4 | ORIGINAL_REQUEST §R2 |
| 8 | Option B Card Styling | Add CSS for `.qa-card`, `.qa-question`, `.qa-answer`, `.qa-number` to `src/styles/custom.css` | M5 | ORIGINAL_REQUEST §R2 |
| 9 | Starlight Navigation Config | Add `2000 سوئال-جاۋاب` sidebar group to `astro.config.mjs` with RTL config | M5 | ORIGINAL_REQUEST §R4 |
| 10 | 2000 Root Index Page | Create `src/content/docs/2000/index.mdx` landing portal | M5 | Survey |
| 11 | Full Question Continuity Verification | Verify Questions 1 through 647 are 100% present without gaps | E2E | Acceptance Criteria |
| 12 | Zero Legacy Glyphs Verification | Verify 0 occurrences of `\u066e` or `\u067b` across all MDX | E2E | Acceptance Criteria |
| 13 | 99 Names Completeness Verification | Verify all 99 names are present and formatted in table | E2E | Acceptance Criteria |
| 14 | Astro Build & Search Verification | `pnpm build` succeeds, Pagefind search index built | E2E | Acceptance Criteria |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| E2E | E2E Testing Track | Build test runner and Tiers 1-4 test suites; publish TEST_READY.md | none | DONE |
| M1 | Extraction & Normalization Engine | Build Python extraction scripts with RTL ordering & Unicode normalization | none | DONE |
| M2 | Section 00 (Muqeddimu) Generation | Generate 4 MDX pages under `src/content/docs/2000/00-muqeddimu/` | M1 | DONE |
| M3 | Section 01 (Etiqad) & 99 Names | Generate 8 MDX pages under `src/content/docs/2000/01-etiqad/` (Q1-163 + 99 Names) | M1 | DONE |
| M4 | Section 02 (Ibadet) Generation | Generate 14 MDX pages under `src/content/docs/2000/02-ibadet/` (Q164-647) | M1 | DONE |
| M5 | Navigation, Styling & Index | Configure `astro.config.mjs`, `custom.css`, `index.mdx` | M2, M3, M4 | DONE |
| M6 | Final Verification & Hardening | Run 100% E2E tests, adversarial stress tests, and Forensic Audit | E2E, M5 | DONE |

## Interface Contracts
### Extraction Script ↔ Content Generators
- Output JSON format:
  ```json
  {
    "questions": [
      {
        "number": 1,
        "question": "ئىنسانلار نەدىن پەيدا بولغان؟",
        "answer": "ئىنسانلار ئاللاھ تەرىپىدىن يارىتىلغان.",
        "footnotes": [],
        "page": 39
      }
    ],
    "names_99": [
      {
        "id": 1,
        "arabic": "الله",
        "transliteration": "ئاللاھ",
        "meaning": "پۈتۈن مەۋجۇداتنىڭ ياراتقۇچىسى..."
      }
    ]
  }
  ```
- File encodings: UTF-8 strictly without BOM.
- Zero occurrences of `\u066e`, `\u067b`, or interior `\u0640`.

### MDX Format ↔ Starlight
- Frontmatter:
  ```yaml
  ---
  title: "بۆلۈم ماۋزۇسى"
  description: "بۆلۈم چۈشەندۈرۈشى"
  ---
  ```
- Question block format (Option B):
  ```html
  <div class="qa-card" id="q1">
    <div class="qa-question">
      <span class="qa-number">1</span>
      <span class="qa-text">سوئال: ئىنسانلار نەدىن پەيدا بولغان؟</span>
    </div>
    <div class="qa-answer">
      جاۋاب: ئىنسانلار ئاللاھ تەرىپىدىن يارىتىلغان.
    </div>
  </div>
  ```

## Code Layout
- Extraction scripts: `tools/extract_2000.py` or `scripts/extract_2000.py`
- Test suite: `tests/e2e_2000.py` or `scripts/verify_2000.py`
- Generated Content:
  - `src/content/docs/2000/index.mdx`
  - `src/content/docs/2000/00-muqeddimu/*.mdx`
  - `src/content/docs/2000/01-etiqad/*.mdx`
  - `src/content/docs/2000/02-ibadet/*.mdx`
- Styles: `src/styles/custom.css`
- Config: `astro.config.mjs`
