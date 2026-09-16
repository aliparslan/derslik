# E2E Test Infra: Din ve Hayat (2000 Sualliq)

## Test Philosophy
- Opaque-box, requirement-driven. No dependency on implementation design.
- Methodology: Category-Partition + BVA + Pairwise + Workload Testing.

## Acceptance & Verification Criteria
1. **Extraction & Question Coverage**:
   - Total questions extracted must equal exactly 647.
   - Question numbers must strictly form the complete set `1..647` without any missing numbers or duplicates.
   - Question text and answer text must be non-empty and well-formed.
2. **Unicode & Normalization Integrity**:
   - Zero occurrences of legacy glyphs `\u066e` (dotless beh) and `\u067b` (beeh with 2 vertical dots) in all generated MDX files.
   - Zero occurrences of `\u06cc` (Farsi yeh) in Uyghur text (normalized to `\u064a`).
   - Zero occurrences of interior tatweels/kashidas (`\u0640`) within words.
3. **99 Names of Allah Table**:
   - Table present in `src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx`.
   - Exactly 99 rows present.
   - All 3 columns populated: Arabic Name with tashkeel, Uyghur Pronunciation, and Uyghur Meaning.
4. **Structural & Page Completeness**:
   - `00-muqeddimu/`: 4 pages present (`01-kitab-heqqide.mdx`, `02-aptur-heqqide.mdx`, `03-kirish-soz.mdx`, `04-munderije.mdx`).
   - `01-etiqad/`: 8 pages present covering Q1–Q163 and 99 Names.
   - `02-ibadet/`: 14 pages present covering Q164–Q647.
   - `index.mdx`: Present and linking to sections.
5. **Starlight & Build Verification**:
   - `astro.config.mjs` contains `2000 سوئال-جاۋاب` navigation group.
   - `src/styles/custom.css` contains `.qa-card`, `.qa-question`, `.qa-answer`, `.qa-number`.
   - `pnpm build` compiles with exit code 0.
   - Pagefind search index generated in `dist/pagefind/`.

## Test Runner
- Executable script: `tests/e2e_2000.py`
- Command: `/usr/bin/python3 tests/e2e_2000.py && pnpm build`
