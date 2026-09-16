# Handoff Report — challenger_2

## 1. Observation

### 1.1 Option B CSS Rules (`src/styles/custom.css`)
- Verified `src/styles/custom.css` (lines 71–176):
  - `.qa-card` (lines 71–95): defines `position: relative`, `margin-block-end: 1.5rem`, `border-radius: 0.625rem`, `scroll-margin-top: calc(var(--sl-nav-height) + 1.5rem)`, hover states, and `:root[data-theme='light']` variants.
  - `.qa-question` (lines 96–112): defines `display: flex`, `gap: 0.75rem`, `border-inline-start: 4px solid var(--sl-color-accent)`, `padding-inline-start: 0.75rem`, `margin-block-end: 0.85rem`.
  - `.qa-number` (lines 113–128): defines `display: inline-flex`, `min-width: 2.25rem`, `border-radius: 9999px`, background and accent colors.
  - `.qa-text` (lines 130–138): defines `flex-grow: 1`, font-weight, dark/light text color.
  - `.qa-label` (lines 140–144): defines `color: var(--sl-color-accent)`, `font-weight: 700`, `margin-inline-end: 0.25rem`.
  - `.qa-answer` (lines 146–175): defines `padding-inline-start: calc(0.75rem + 4px)`, paragraph spacing, and blockquote styling (`border-inline-start: 3px solid var(--sl-color-accent)`).
  - Verified RTL logical properties are used consistently across all selectors.
  - Verified inclusion in `astro.config.mjs` line 130 (`customCss: ['./src/styles/custom.css']`).

### 1.2 Card Structure Across MDX Files
- Inspected canonical MDX files across `01-etiqad` (8 files) and `02-ibadet` (14 files):
  - Card format adheres strictly to Option B:
    ```html
    <div class="qa-card" id="q{N}">
      <div class="qa-question">
        <span class="qa-number">{N}</span>
        <span class="qa-label">سوئال:</span> {text}
      </div>
      <div class="qa-answer">
        <span class="qa-label">جاۋاب:</span> {text}
      </div>
    </div>
    ```
  - Contiguity in canonical files: Q1–Q163 in `01-etiqad`, Q164–Q647 in `02-ibadet` (total: 647 contiguous questions without gaps).

### 1.3 Frontmatter and Routing of `src/content/docs/2000/index.mdx` and `00-muqeddimu/`
- `src/content/docs/2000/index.mdx`:
  - Contains valid YAML frontmatter with `title: "دىن ۋە ھايات (2000 سوئالغا جاۋاب)"`, `template: splash`, and `hero` with action links pointing to `/2000/00-muqeddimu/01-kitab-heqqide/`, `/2000/01-etiqad/01-din-ve-etiqad/`, and `/2000/02-ibadet/01-ibadet-esasliri/`.
  - Contains Starlight `CardGrid` and `LinkCard` components correctly linked.
- `src/content/docs/2000/00-muqeddimu/`:
  - Contains exactly 4 canonical files:
    1. `01-kitab-heqqide.mdx` (63 lines, 5,042 bytes)
    2. `02-aptur-heqqide.mdx` (83 lines, 11,141 bytes)
    3. `03-kirish-soz.mdx` (60 lines, 7,182 bytes)
    4. `04-munderije.mdx` (146 lines, 9,987 bytes)
  - All 4 files contain valid YAML frontmatter, informative content, and correct internal routing links.

### 1.4 Starlight Configuration in `astro.config.mjs` & Navigation Breakdown
- `astro.config.mjs` lines 93–127 defines:
  ```javascript
  {
    label: '2000 سوئال-جاۋاب',
    translations: { en: '2000 Q&A' },
    items: [
      { label: 'ئومۇمىي بايان', link: '/2000/', translations: { en: 'Overview' } },
      { label: '00-مۇقەددىمە', translations: { en: '00-Introduction' }, items: [{ autogenerate: { directory: '2000/00-muqeddimu' } }] },
      { label: '01-ئېتىقاد (1–163)', translations: { en: '01-Creed (1–163)' }, items: [{ autogenerate: { directory: '2000/01-etiqad' } }] },
      { label: '02-ئىبادەت (164–647)', translations: { en: '02-Worship (164–647)' }, items: [{ autogenerate: { directory: '2000/02-ibadet' } }] },
    ],
  }
  ```
- Because `{ autogenerate: { directory: '2000/01-etiqad' } }` is used, Starlight builds sidebar items for **every** `.mdx` file inside `src/content/docs/2000/01-etiqad/`.

### 1.5 Defect 1: Four Obsolete Skeleton Files Remain in `01-etiqad/`
- Direct directory inspection of `src/content/docs/2000/01-etiqad/` reveals 12 files instead of the required 8:
  1. `04-rohiy-alemler.mdx` (25,115 bytes): Obsolete duplicate of Q63–Q82. Contains inverted word order (e.g. line 12: `ئالەملەر؟ قانداق دﭔگەن ئالەملەر روھىي`) and unnormalized presentation glyphs. Frontmatter specifies `order: 4`, colliding with `04-perishtiler-jinlar.mdx` (`order: 4`).
  2. `05-kitablar-peyghemberler.mdx` (21,986 bytes): Obsolete duplicate of Q83–Q115. Contains inverted word order (e.g. line 12: `كىتابلار؟ قانداق كىتابلىرى ئاللاھنىۅ`). Frontmatter specifies `order: 5`, colliding with `05-samawiy-kitablar.mdx` (`order: 5`).
  3. `06-qaza-qeder.mdx` (168 bytes): Empty skeleton file containing only 7 lines of frontmatter with `order: 6` (colliding with `06-peyghamberler.mdx` with `order: 6`) and zero questions.
  4. `07-qiyamet-axiret.mdx` (206 bytes): Empty skeleton file containing only 7 lines of frontmatter with `order: 7` (colliding with `07-qada-qeder.mdx` with `order: 7`) and zero questions.
- Impact on test suite:
  - `tests/e2e_2000.py` Tier 1 `test_section_01_pages_and_boundaries` asserts `len(mdx_files) == 8`. Found 12 files -> **FAILS**.
  - `tests/e2e_2000.py` Tier 1 `test_question_count` asserts `total_cards == 647`. Found 700 cards (53 duplicate cards) -> **FAILS**.
- Impact on UI / Starlight:
  - Sidebar autogeneration creates duplicate routes and links for Creed subsections.
  - Sidebar autogeneration creates dead/blank pages (`06-qaza-qeder` and `07-qiyamet-axiret`).

### 1.6 Defect 2: Unnormalized Farsi Yeh (`\u06cc` -> `ي` `\u064a`) in Canonical Files
- Requirement §R1 explicitly states:
  > "Convert `\u06cc` (Farsi yeh) -> standard Uyghur `ي` (`\u064a`)."
- Empirical `grep_search` across `src/content/docs/2000/` reveals unnormalized `\u06cc` in canonical files:
  1. `src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx`:
     - Line 77: `| الحَيِيُّ | ئەل ھەیىي | ...` (contains `\u06cc` in `ئەل ھەیىي`)
     - Line 79: `| القَيُّومُ | ئەل قەیيۇم | ...` (contains `\u06cc` in `ئەل قەیيۇم`)
     - Line 81: `| الدَّيَّانُ | ئەددەیيان | ...` (contains `\u06cc` in `ئەددەیيان`)
     - Line 108: `| السَّيِّدُ | ئەسسەیيىد | ...` (contains `\u06cc` in `ئەسسەیيىد`)
  2. `src/content/docs/2000/01-etiqad/05-samawiy-kitablar.mdx`:
     - Line 15: `ئاللاھنىڭ كىتابلىرى ئاللاھ پەیغەمبەرلەرگە چۈشۈرگەن ...` (contains `\u06cc` in `پەیغەمبەرلەرگە`)
  3. `src/content/docs/2000/01-etiqad/08-qiyamet-axiret.mdx`:
     - Line 65: `... دەلىللەر بىلەن رەت قىلىنىدۇ: یوقتىن ياراتقان ئاللاھ ...` (contains `\u06cc` in `یوقتىن`)
- (In addition, the 2 obsolete duplicate files `04-rohiy-alemler.mdx` and `05-kitablar-peyghemberler.mdx` contain over 50 instances of `\u06cc`).
- Test suite omission:
  - `tests/e2e_2000.py` Tier 2 checks `\u066e` (`test_zero_dotless_beh`), `\u067b` (`test_zero_beeh_two_dots_below`), and `\u0640` (`test_zero_interior_tatweels`), but has **no assertion** for `\u06cc`. Consequently, these unnormalized glyphs evaded automated detection.

---

## 2. Logic Chain

1. From Observation 1.5, four obsolete skeleton/duplicate files (`04-rohiy-alemler.mdx`, `05-kitablar-peyghemberler.mdx`, `06-qaza-qeder.mdx`, `07-qiyamet-axiret.mdx`) remain in `src/content/docs/2000/01-etiqad/`.
2. From Observation 1.4, `astro.config.mjs` configures `{ autogenerate: { directory: '2000/01-etiqad' } }`, which automatically reads every file in that directory. Therefore, the Starlight sidebar displays duplicate and empty navigation links to end users, violating UX integrity and sidebar navigation contracts.
3. From Observation 1.5, the presence of these files causes `tests/e2e_2000.py` to fail in Tier 1 (`test_section_01_pages_and_boundaries` and `test_question_count`), and introduces inverted Uyghur text into the documentation bundle.
4. From Observation 1.6, canonical files in `01-etiqad` violate §R1 Unicode Normalization requirements by retaining Farsi Yeh (`\u06cc`) instead of standard Uyghur `ي` (`\u064a`) across 6 distinct lines in `03-allahning-isimliri.mdx`, `05-samawiy-kitablar.mdx`, and `08-qiyamet-axiret.mdx`.
5. Because implementation review rules prohibit challenger agents from modifying implementation code directly, these defects must be resolved by an implementation worker.
6. Therefore, the verification cannot pass in this state.

---

## 3. Caveats

- Unattended subprocess terminal execution (`run_command`) triggers an interactive macOS security permission prompt that times out in unattended environments; all file contents, Unicode code points, regular expressions, and directory structures were verified directly via cortex filesystem inspection tools (`grep_search`, `list_dir`, `view_file`).
- The 26 canonical MDX files (4 in `00-muqeddimu`, 8 in `01-etiqad`, 14 in `02-ibadet`) and `src/styles/custom.css` are otherwise well-structured, complete, and high quality.

---

## 4. Conclusion

**Verdict: REJECT**

The current implementation cannot be approved due to two blocking issues:
1. **Obsolete Skeleton Files**: Four obsolete files remain in `src/content/docs/2000/01-etiqad/` (`04-rohiy-alemler.mdx`, `05-kitablar-peyghemberler.mdx`, `06-qaza-qeder.mdx`, `07-qiyamet-axiret.mdx`), which poison the Starlight autogenerated sidebar, introduce empty/duplicate pages, and cause Tier 1 E2E tests to fail.
2. **Residual Unnormalized Farsi Yeh (`\u06cc`)**: Canonical files contain `\u06cc` (in `03-allahning-isimliri.mdx` lines 77, 79, 81, 108; `05-samawiy-kitablar.mdx` line 15; `08-qiyamet-axiret.mdx` line 65), violating §R1 Unicode Normalization.

---

## 5. Verification Method

To resolve these defects and verify the solution:

### Step 1: Remove the 4 Obsolete Files
```bash
rm -f src/content/docs/2000/01-etiqad/04-rohiy-alemler.mdx \
      src/content/docs/2000/01-etiqad/05-kitablar-peyghemberler.mdx \
      src/content/docs/2000/01-etiqad/06-qaza-qeder.mdx \
      src/content/docs/2000/01-etiqad/07-qiyamet-axiret.mdx
```

### Step 2: Normalize Residual `\u06cc` in Canonical Files
Replace `\u06cc` (`ی`) with standard Uyghur `\u064a` (`ي`) in:
- `src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx`
- `src/content/docs/2000/01-etiqad/05-samawiy-kitablar.mdx`
- `src/content/docs/2000/01-etiqad/08-qiyamet-axiret.mdx`

Verify zero occurrences remain across all documentation files:
```bash
python3 -c '
from pathlib import Path
docs = Path("src/content/docs/2000")
matches = [f"{p}: {p.read_text(encoding=\"utf-8\").count(\"\u06cc\")}"
           for p in docs.glob("**/*") if p.is_file() and p.suffix in (".mdx", ".md") and "\u06cc" in p.read_text(encoding="utf-8")]
print("Farsi Yeh occurrences:", matches if matches else "ZERO (CLEAN)")
'
```

### Step 3: Run Full E2E Test Suite
```bash
python3 tests/e2e_2000.py -v
```

Expected result after fixes:
- Tier 1: PASS (647 questions, 1..647 set, 4 sec00 pages, exactly 8 sec01 pages, exactly 14 sec02 pages)
- Tier 2: PASS (0 legacy glyphs, landmark questions integrity)
- Tier 3: PASS (99 names table, Option B CSS, sidebar navigation config)
- Tier 4: PASS (`pnpm build` succeeds with exit code 0)
