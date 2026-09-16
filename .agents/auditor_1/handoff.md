# Forensic Integrity Audit Report — auditor_1

**Work Product**: Din ve Hayat (2000 Sualliq) Part 1 Conversion (`src/content/docs/2000/`, `tests/e2e_2000.py`, `tools/extracted_2000.json`)  
**Profile**: General Project (Integrity Mode: `development` per `ORIGINAL_REQUEST.md`)  
**Verdict**: **INTEGRITY VIOLATION**

---

## Executive Summary
While the underlying content extracted from the source PDF and recorded in `tools/extracted_2000.json` is genuine, scholarly, and complete (covering all 647 questions and all 99 Names of Allah), the work product delivered into `src/content/docs/2000/` fails multiple core integrity checks and cannot be certified as clean:
1. **Facade / Dummy Implementations**: `src/content/docs/2000/01-etiqad/06-qaza-qeder.mdx` (168 bytes) and `src/content/docs/2000/01-etiqad/07-qiyamet-axiret.mdx` (206 bytes) are empty skeleton pages that contain only frontmatter titles and descriptions claiming to cover Q116–134 and Q135–163, but contain zero question cards or answers.
2. **Corrupted & Duplicate Question Cards**: `src/content/docs/2000/01-etiqad/04-rohiy-alemler.mdx` and `src/content/docs/2000/01-etiqad/05-kitablar-peyghemberler.mdx` remain present alongside the canonical files, containing 53 duplicate question cards (Q63–Q115) with corrupted, inverted word order (visual RTL reversal defect) and legacy characters. This inflates the total question card count from 647 to 700.
3. **Starlight Autogeneration Pollution**: Because `astro.config.mjs` configures `items: [{ autogenerate: { directory: '2000/01-etiqad' } }]`, Starlight automatically exposes all 12 files in the public sidebar, showing two empty stub pages and two corrupted duplicate pages to end users.
4. **Acceptance Criteria Failure (Production Build & Search Index)**: The `dist/` directory contains stale artifacts from an earlier build that predates the `/2000/` section. `dist/2000/` does not exist, `dist/sitemap-0.xml` contains zero `/2000/` URLs, and `dist/pagefind/` indexes none of the 647 questions.
5. **Unnormalized Legacy Glyphs (`\u06cc`)**: Contrary to `ORIGINAL_REQUEST.md` §R1 ("Convert `\u06cc` (Farsi yeh) -> standard Uyghur `ي` (`\u064a`)"), 6 occurrences of `\u06cc` remain in canonical documentation files (and dozens in obsolete files).

---

## 1. Observation

### Observation 1: Presence of Empty Facade Files in `01-etiqad`
Direct inspection of `src/content/docs/2000/01-etiqad/` reveals two empty skeleton files:
- `src/content/docs/2000/01-etiqad/06-qaza-qeder.mdx` (168 bytes, 9 lines):
  ```markdown
  ---
  title: "قازا ۋە قەدەر"
  description: "Divine Decree (Qada & Qadar) — سوئال 116–134"
  sidebar:
    label: "قازا ۋە قەدەر"
    order: 6
  ---
  ```
  Lines 8–9 are completely blank. No question cards, no answer blocks.
- `src/content/docs/2000/01-etiqad/07-qiyamet-axiret.mdx` (206 bytes, 9 lines):
  ```markdown
  ---
  title: "قىيامەت كۈنى ۋە ئاخىرەت"
  description: "Day of Judgement & Hereafter — سوئال 135–163"
  sidebar:
    label: "قىيامەت كۈنى ۋە ئاخىرەت"
    order: 7
  ---
  ```
  Lines 8–9 are completely blank. No question cards, no answer blocks.

### Observation 2: Presence of Corrupted Duplicate Files in `01-etiqad`
Two legacy extraction attempt files remain in `src/content/docs/2000/01-etiqad/`:
- `src/content/docs/2000/01-etiqad/04-rohiy-alemler.mdx` (25,115 bytes, 209 lines): Contains Q63–Q82 with reversed word order.
  Example from Line 12:
  `<span class="qa-label">سوئال:</span> ئالەملەر؟ قانداق دﭔگەن ئالەملەر روھىي`
  (Words reversed from natural Uyghur: "روھىي ئالەملەر دېگەن قانداق ئالەملەر؟").
- `src/content/docs/2000/01-etiqad/05-kitablar-peyghemberler.mdx` (21,986 bytes, 179 lines): Contains Q83–Q115 with reversed word order.
  Example from Line 12:
  `<span class="qa-label">سوئال:</span> كىتابلار؟ قانداق كىتابلىرى ئاللاھنىۅ`
  (Words reversed from natural Uyghur: "ئاللاھنىڭ كىتابلىرى قانداق كىتابلار؟").

### Observation 3: File Count and Question Card Duplication
- `list_dir` on `src/content/docs/2000/01-etiqad/` shows 12 `.mdx` files instead of the required 8 canonical files:
  1. `01-din-ve-etiqad.mdx` (canonical, Q1–20)
  2. `02-allahqa-iman.mdx` (canonical, Q21–48)
  3. `03-allahning-isimliri.mdx` (canonical, 99 names + Q49–62)
  4. `04-perishtiler-jinlar.mdx` (canonical, Q63–82)
  5. `04-rohiy-alemler.mdx` (OBSOLETE DUPLICATE, Q63–82)
  6. `05-kitablar-peyghemberler.mdx` (OBSOLETE DUPLICATE, Q83–115)
  7. `05-samawiy-kitablar.mdx` (canonical, Q83–96)
  8. `06-peyghamberler.mdx` (canonical, Q97–115)
  9. `06-qaza-qeder.mdx` (OBSOLETE EMPTY SKELETON)
  10. `07-qada-qeder.mdx` (canonical, Q116–134)
  11. `07-qiyamet-axiret.mdx` (OBSOLETE EMPTY SKELETON)
  12. `08-qiyamet-axiret.mdx` (canonical, Q135–163)
- Grepping for `<div class="qa-card"` across `src/content/docs/2000/` finds **700** cards instead of the expected 647, because Questions 63 through 115 are present twice.

### Observation 4: Stale Build Directory and Missing Search Index
- `dist/` contains pages from other sections (`1-osmurler`, `2-yashlar`, etc.), but `dist/2000` does not exist:
  `list_dir /Users/arslan/code/derslik/dist/2000 -> directory does not exist`
- `dist/sitemap-0.xml` does not contain a single reference to `/2000/`.
- Grepping `2000` in `dist/` returns only XML schema namespaces in SVG files (`xmlns="http://www.w3.org/2000/svg"`).
- `pnpm build` was never executed after creating the `2000` content.

### Observation 5: Lingering Legacy Farsi Yeh (`\u06cc`) Glyphs
`ORIGINAL_REQUEST.md` §R1 explicitly specifies:
`Convert \u06cc (Farsi yeh) -> standard Uyghur ي (\u064a)`.
Grep search for `\u06cc` (excluding obsolete files) identified 6 remaining instances in canonical files:
1. `src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx`:
   - Line 77: `| الحَيِيُّ | ئەل ھەیىي | ...` (Name 65 contains `\u06cc`)
   - Line 79: `| القَيُّومُ | ئەل قەیيۇم | ...` (Name 67 contains `\u06cc`)
   - Line 81: `| الدَّيَّانُ | ئەددەیيان | ...` (Name 69 contains `\u06cc`)
   - Line 108: `| السَّيِّدُ | ئەسسەیيىد | ...` (Name 96 contains `\u06cc`)
2. `src/content/docs/2000/01-etiqad/05-samawiy-kitablar.mdx`:
   - Line 15: `ئاللاھ پەیغەمبەرلەرگە چۈشۈرگەن` (`پەیغەمبەرلەرگە` contains `\u06cc`)
3. `src/content/docs/2000/01-etiqad/08-qiyamet-axiret.mdx`:
   - Line 65: `یوقتىن ياراتقان ئاللاھ` (`یوقتىن` contains `\u06cc`)

### Observation 6: Positive Authentic Implementations
- **Source extraction**: `tools/extracted_2000.json` (566,322 bytes, 7,457 lines) is 100% authentic, containing all 647 questions, valid metadata, and 99 Names of Allah.
- **Section 00 (Muqeddimu)**: All 4 files (`01-kitab-heqqide.mdx`, `02-aptur-heqqide.mdx`, `03-kirish-soz.mdx`, `04-munderije.mdx`) are genuine, rich, and accurately formatted.
- **Section 02 (Ibadet)**: Exactly 14 files covering Questions 164 through 647 continuously in Option B card format.
- **99 Names Table**: `src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx` lines 11–111 contain all 99 rows with vocalized Arabic, Uyghur pronunciation transliteration, and detailed theological meaning.
- **Zero `\u066e` and zero `\u067b`**: Standard Uyghur letters (`ى`, `ې`) are used; zero legacy dotless beh or beeh with 2 dots below exist.
- **Zero interior tatweels**: No interior `\u0640` found inside Uyghur words.
- **Option B CSS**: Present in `src/styles/custom.css` (`.qa-card`, `.qa-question`, `.qa-answer`, `.qa-number`).
- **Astro Config**: Configured in `astro.config.mjs` with RTL locale and `2000 سوئال-جاۋاب` navigation group.

---

## 2. Logic Chain

1. Per `ORIGINAL_REQUEST.md` and the Integrity Forensics Profile (Development Mode), facade implementations (empty placeholders, dummy skeletons) and unverified project completion claims are strictly prohibited integrity violations.
2. From Observation 1, `06-qaza-qeder.mdx` and `07-qiyamet-axiret.mdx` are literal facades: files with frontmatter titles claiming to provide question coverage, but providing zero content.
3. From Observation 2 and Observation 3, `04-rohiy-alemler.mdx` and `05-kitablar-peyghemberler.mdx` are uncleaned legacy artifacts with reversed word ordering and duplicate cards that corrupt the section file count (12 instead of 8) and card count (700 instead of 647).
4. Because `astro.config.mjs` uses `autogenerate: { directory: '2000/01-etiqad' }`, these 4 invalid files are rendered directly into the production documentation site navigation.
5. In `tests/e2e_2000.py`:
   - `test_section_01_pages_and_boundaries` asserts `len(sec01_files) == 8`. With 12 files present, this test **fails**.
   - `test_question_count` asserts `total_cards == 647`. With 700 cards present, this test **fails**.
6. From Observation 4, `ORIGINAL_REQUEST.md` Acceptance Criteria mandate that `pnpm build` or `astro check` compiles cleanly and that routes under `terbiye.org/2000/...` are functional and indexed for search. Because `dist/` contains only pre-existing files without `/2000/`, this acceptance criterion is unfulfilled.
7. From Observation 5, `ORIGINAL_REQUEST.md` §R1 explicitly requires converting `\u06cc` -> `\u064a`. The presence of `\u06cc` in 6 canonical locations is a direct specification defect.
8. Therefore, the work product cannot be certified as CLEAN in its present state.

---

## 3. Caveats

- Interactive terminal command execution via `run_command` timed out due to workstation environment security policy. All observations in this report were verified empirically and deterministically through static AST parsing, file reads, and ripgrep searches across the entire repository.
- The defect is completely remediable with simple, bounded operations. The underlying extracted dataset and canonical generator logic are solid.

---

## 4. Conclusion

**Verdict: INTEGRITY VIOLATION**

The work product must be rejected until the following 4 remediation steps are executed:
1. **Remove the 4 obsolete / facade files** from `src/content/docs/2000/01-etiqad/`:
   - `04-rohiy-alemler.mdx`
   - `05-kitablar-peyghemberler.mdx`
   - `06-qaza-qeder.mdx`
   - `07-qiyamet-axiret.mdx`
2. **Normalize remaining `\u06cc` characters** to `\u064a` (`ي`):
   - `src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx`: lines 77, 79, 81, 108
   - `src/content/docs/2000/01-etiqad/05-samawiy-kitablar.mdx`: line 15
   - `src/content/docs/2000/01-etiqad/08-qiyamet-axiret.mdx`: line 65
3. **Execute Production Build**:
   - Run `pnpm build` to compile the 26 canonical MDX files into `dist/2000/` and regenerate Pagefind search indices.
4. **Execute Full E2E Verification**:
   - Run `python3 tests/e2e_2000.py -v` and confirm 100% pass across all 4 tiers.

---

## 5. Verification Method

To independently verify the defects identified in this report:

```bash
# 1. Verify that 12 files (not 8) exist in 01-etiqad:
ls -la src/content/docs/2000/01-etiqad/

# 2. Verify that 06-qaza-qeder.mdx and 07-qiyamet-axiret.mdx are empty stubs:
cat src/content/docs/2000/01-etiqad/06-qaza-qeder.mdx
cat src/content/docs/2000/01-etiqad/07-qiyamet-axiret.mdx

# 3. Verify that 04-rohiy-alemler.mdx has reversed word order:
head -n 20 src/content/docs/2000/01-etiqad/04-rohiy-alemler.mdx

# 4. Verify that total question card count is 700 (53 duplicate cards):
grep -c 'class="qa-card"' src/content/docs/2000/*/*.mdx

# 5. Verify that dist/2000 does not exist:
ls -d dist/2000

# 6. Verify remaining \u06cc occurrences:
grep -n P '\x{06cc}' src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx
```
