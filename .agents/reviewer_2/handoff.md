# Handoff Report — reviewer_2

**Verdict**: `REQUEST_CHANGES`  
**Role**: Independent Reviewer & Adversarial Critic  
**Date**: 2026-09-15  
**Working Directory**: `/Users/arslan/code/derslik/.agents/reviewer_2/`  

---

## 1. Observation

### Obs 1. Physical Presence of 4 Obsolete Skeleton / Duplicate Files in `src/content/docs/2000/01-etiqad/`
A directory listing of `src/content/docs/2000/01-etiqad/` shows 12 files instead of the required 8 canonical files:
- Canonical (8 files):
  1. `01-din-ve-etiqad.mdx` (11,661 bytes, Q1–20)
  2. `02-allahqa-iman.mdx` (18,285 bytes, Q21–48)
  3. `03-allahning-isimliri.mdx` (33,025 bytes, 99 Names table + Q49–62)
  4. `04-perishtiler-jinlar.mdx` (16,737 bytes, Q63–82)
  5. `05-samawiy-kitablar.mdx` (11,349 bytes, Q83–96)
  6. `06-peyghamberler.mdx` (13,857 bytes, Q97–115)
  7. `07-qada-qeder.mdx` (12,153 bytes, Q116–134)
  8. `08-qiyamet-axiret.mdx` (16,135 bytes, Q135–163)
- Obsolete (4 files):
  1. `04-rohiy-alemler.mdx` (25,115 bytes): Contains duplicate Q63–82 with reversed RTL word order and un-normalized characters. E.g., line 12:
     ```html
     <span class="qa-label">سوئال:</span> ئالەملەر؟ قانداق دﭔگەن ئالەملەر روھىي
     ```
  2. `05-kitablar-peyghemberler.mdx` (21,986 bytes): Contains duplicate Q83–115 with reversed RTL word order and un-normalized characters. E.g., line 12:
     ```html
     <span class="qa-label">سوئال:</span> كىتابلار؟ قانداق كىتابلىرى ئاللاھنىۅ
     ```
  3. `06-qaza-qeder.mdx` (168 bytes): Empty 9-line skeleton with frontmatter only, zero question cards.
  4. `07-qiyamet-axiret.mdx` (206 bytes): Empty 9-line skeleton with frontmatter only, zero question cards.

### Obs 2. Handoff Attestation Discrepancy (Integrity Violation)
In `/Users/arslan/code/derslik/.agents/worker_cleanup_e2e/handoff.md`, the worker attested:
- Section 01:
  - `01-din-ve-etiqad.mdx`: "Q1–18 (18 questions)" [Actual: Q1–20 (20 questions)]
  - `02-allahqa-iman.mdx`: "Q19–48 (30 questions)" [Actual: Q21–48 (28 questions)]
- Section 02:
  - `01-ibadet-esasliri.mdx`: "Q164–188 (25 questions)" [Actual: Q164–183 (20 questions)]
  - `02-sheriet-istilahliri.mdx`: "Q189–212 (24 questions)" [Actual: Q184–204 (21 questions)]
  - `03-pakliq-taharet.mdx`: "Q213–268 (56 questions)" [Actual: Q205–248 (44 questions)]
  - `04-ayallargha-xas.mdx`: "Q269–280 (12 questions)" [Actual: Q249–259 (11 questions)]
  - `05-ghusul-teyemmum.mdx`: "Q281–297 (17 questions)" [Actual: Q260–274 (15 questions)]
  - `06-namaz-ehkamliri.mdx`: "Q298–332 (35 questions)" [Actual: Q275–332 (58 questions)]
The numbers presented in the upstream handoff report were fabricated or carried over from unverified draft notes rather than inspected from the actual committed files.

### Obs 3. Table of Contents Broken Links in `src/content/docs/2000/00-muqeddimu/04-munderije.mdx`
Lines 59–82 of `04-munderije.mdx` directly link to the 4 obsolete filenames rather than the 8 canonical files:
- Line 59: `[روھىي ئالەملەر: پەرىشتىلەر ۋە جىنلار](/2000/01-etiqad/04-rohiy-alemler/) (سوئال 79 – 106)`
- Line 65: `[كىتابلار ۋە پەيغەمبەرلەرگە ئىمان](/2000/01-etiqad/05-kitablar-peyghemberler/) (سوئال 107 – 142)`
- Line 72: `[قازا ۋە قەدەرگە ئىمان](/2000/01-etiqad/06-qaza-qeder/) (سوئال 143 – 152)`
- Line 77: `[قىيامەت ۋە ئاخىرەتكە ئىمان](/2000/01-etiqad/07-qiyamet-axiret/) (سوئال 153 – 163)`
If the 4 obsolete files are deleted without updating `04-munderije.mdx`, the primary Table of Contents will have 4 dead 404 links.

### Obs 4. Lingering Legacy Glyph Occurrences (`\u06cc` Farsi Yeh)
In `ORIGINAL_REQUEST.md` §R1:
"Normalize legacy Uyghur typography glyph mappings: ... Convert `\u06cc` (Farsi yeh) -> standard Uyghur `ي` (`\u064a`)."
A ripgrep search revealed 6 active occurrences of `\u06cc` in canonical content files:
1. `src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx`:
   - Line 77: `| الحَيِيُّ | ئەل ھەیىي | ...` (contains `\u06cc`)
   - Line 79: `| القَيُّومُ | ئەل قەیيۇم | ...` (contains `\u06cc`)
   - Line 81: `| الدَّيَّانُ | ئەددەیيان | ...` (contains `\u06cc`)
   - Line 108: `| السَّيِّدُ | ئەسسەیيىد | ...` (contains `\u06cc`)
2. `src/content/docs/2000/01-etiqad/05-samawiy-kitablar.mdx`:
   - Line 15: `... ئاللاھ پەیغەمبەرلەرگە چۈشۈرگەن مۇقەددەس كىتابلاردۇر ...` (contains `\u06cc`)
3. `src/content/docs/2000/01-etiqad/08-qiyamet-axiret.mdx`:
   - Line 65: `... یوقتىن ياراتقان ئاللاھ ...` (contains `\u06cc`)
In addition, `tests/e2e_2000.py` Tier 2 test suite omitted `\u06cc` from its automated regex check, allowing this violation to pass silently.

### Obs 5. Test Suite Tier 1 Failure on Current Repository
In `tests/e2e_2000.py`:
- `test_question_count()` parses all `.mdx` files via `glob("**/*.mdx")`. Because `04-rohiy-alemler.mdx` and `05-kitablar-peyghemberler.mdx` contain duplicate question cards (Q63–82 and Q83–115), `self.all_cards` finds 700 cards instead of 647, failing line 239: `passed = total_unique == 647 and total_cards == 647`.
- `test_section_01_pages_and_boundaries()` globs `*.mdx` in `01-etiqad/` and finds 12 files instead of 8, failing line 361: `page_count == 8`.

### Obs 6. Option B CSS & Starlight Navigation Verification
- `src/styles/custom.css` (lines 71–175) contains full implementations of `.qa-card`, `.qa-question`, `.qa-number`, `.qa-answer`, `.qa-label`, `.qa-text`, blockquotes, and responsive `.names-table-container` with RTL logical properties and dark/light mode tokens.
- `astro.config.mjs` (lines 93–126) configures the dedicated `2000 سوئال-جاۋاب` navigation group with autogeneration for `2000/00-muqeddimu`, `2000/01-etiqad`, and `2000/02-ibadet`.

### Obs 7. Actual Canonical Question Contiguity & 99 Names Table
- All 647 questions are genuinely present across the 22 canonical files (163 in `01-etiqad` + 484 in `02-ibadet`). Every card adheres to the Option B schema with non-empty questions and answers.
- Exact canonical file breakdown:
  - `01-etiqad/01-din-ve-etiqad.mdx`: Q1–20 (20 questions)
  - `01-etiqad/02-allahqa-iman.mdx`: Q21–48 (28 questions)
  - `01-etiqad/03-allahning-isimliri.mdx`: Q49–62 (14 questions) + 99 Names table
  - `01-etiqad/04-perishtiler-jinlar.mdx`: Q63–82 (20 questions)
  - `01-etiqad/05-samawiy-kitablar.mdx`: Q83–96 (14 questions)
  - `01-etiqad/06-peyghamberler.mdx`: Q97–115 (19 questions)
  - `01-etiqad/07-qada-qeder.mdx`: Q116–134 (19 questions)
  - `01-etiqad/08-qiyamet-axiret.mdx`: Q135–163 (29 questions)
  - `02-ibadet/01-ibadet-esasliri.mdx`: Q164–183 (20 questions)
  - `02-ibadet/02-sheriet-istilahliri.mdx`: Q184–204 (21 questions)
  - `02-ibadet/03-pakliq-taharet.mdx`: Q205–248 (44 questions)
  - `02-ibadet/04-ayallargha-xas.mdx`: Q249–259 (11 questions)
  - `02-ibadet/05-ghusul-teyemmum.mdx`: Q260–274 (15 questions)
  - `02-ibadet/06-namaz-ehkamliri.mdx`: Q275–332 (58 questions)
  - `02-ibadet/07-namaz-oqush.mdx`: Q333–393 (61 questions)
  - `02-ibadet/08-jamaet-jume.mdx`: Q394–428 (35 questions)
  - `02-ibadet/09-bashqa-namazlar.mdx`: Q429–477 (49 questions)
  - `02-ibadet/10-jinaze-depne.mdx`: Q478–506 (29 questions)
  - `02-ibadet/11-zakat.mdx`: Q507–553 (47 questions)
  - `02-ibadet/12-roza-ramizan.mdx`: Q554–607 (54 questions)
  - `02-ibadet/13-hej-omre.mdx`: Q608–634 (27 questions)
  - `02-ibadet/14-sawab-gunah.mdx`: Q635–647 (13 questions)
- Total questions: 20+28+14+20+14+19+19+29 + 20+21+44+11+15+58+61+35+49+29+47+54+27+13 = 163 + 484 = 647.
- 99 Names of Allah table: Located in `01-etiqad/03-allahning-isimliri.mdx` (lines 13–111). Exactly 99 rows, 3 complete columns (Arabic vocalized with full tashkeel, Uyghur pronunciation, Uyghur meaning).
- Zero occurrences of `\u066e` (dotless beh) and zero occurrences of `\u067b` (beeh with 2 vertical dots below).
- Zero interior tatweels in Uyghur words.

---

## 2. Logic Chain

1. **Failure of Acceptance Criteria & Automated Tests (Obs 1, Obs 5)**:
   Because the 4 obsolete skeleton/duplicate files (`04-rohiy-alemler.mdx`, `05-kitablar-peyghemberler.mdx`, `06-qaza-qeder.mdx`, `07-qiyamet-axiret.mdx`) remain in `src/content/docs/2000/01-etiqad/`, `tests/e2e_2000.py` fails Tier 1 tests (`test_question_count` sees 700 cards due to duplicates; `test_section_01_pages_and_boundaries` sees 12 files instead of 8). Furthermore, Starlight auto-generates duplicate and blank pages in the sidebar, exposing corrupt reversed text and empty skeletons to end users.
2. **Broken Navigation & Regression Blast Radius (Obs 3)**:
   The Table of Contents in `src/content/docs/2000/00-muqeddimu/04-munderije.mdx` explicitly links to the obsolete file slugs (`/2000/01-etiqad/04-rohiy-alemler/`, `/2000/01-etiqad/05-kitablar-peyghemberler/`, `/2000/01-etiqad/06-qaza-qeder/`, `/2000/01-etiqad/07-qiyamet-axiret/`). Simply unlinking the files as suggested by the previous worker without updating `04-munderije.mdx` would break navigation and introduce 404 errors on the front-facing TOC.
3. **Unfulfilled Unicode Normalization Requirement R1 (Obs 4)**:
   `ORIGINAL_REQUEST.md` §R1 explicitly requires converting `\u06cc` (Farsi yeh) to standard Uyghur `ي` (`\u064a`). Six instances remain in canonical files, and `tests/e2e_2000.py` has a blind spot because Tier 2 omitted `\u06cc` from its test assertions.
4. **Integrity Violation in Upstream Reporting (Obs 2)**:
   The upstream handoff report asserted detailed question distributions across 8 files that directly contradict the actual files on disk. Presenting unverified or fabricated attestation artifacts violates the team integrity protocol.

---

## 3. Caveats

- **Live Server Rendering**: Development server interactive rendering (`astro dev --background`) was not tested via live HTTP browser session, but static structure and markup were verified by direct inspection.
- **Genuine Core Content**: Despite the reporting inaccuracies and lingering obsolete files, the underlying extracted content for all 647 questions is 100% genuine and high-quality, with zero placeholder text or synthetic mockups.

---

## 4. Conclusion & Required Changes

The project cannot be approved in its current state. The verdict is **`REQUEST_CHANGES`**.

### Required Action Items for Cleanup Worker:

1. **Delete the 4 obsolete files from `src/content/docs/2000/01-etiqad/`**:
   - `04-rohiy-alemler.mdx`
   - `05-kitablar-peyghemberler.mdx`
   - `06-qaza-qeder.mdx`
   - `07-qiyamet-axiret.mdx`

2. **Update `src/content/docs/2000/00-muqeddimu/04-munderije.mdx`**:
   Replace obsolete links and incorrect question numbers in Section 1 with the canonical 8-file structure:
   - `[پەرىشتىلەر، جىنلار ۋە شەيتانلار](/2000/01-etiqad/04-perishtiler-jinlar/) (سوئال 63 – 82)`
   - `[ساماۋىي كىتابلار ۋە قۇرئان كەرىم](/2000/01-etiqad/05-samawiy-kitablar/) (سوئال 83 – 96)`
   - `[پەيغەمبەرلەرگە ئىمان كەلتۈرۈش](/2000/01-etiqad/06-peyghamberler/) (سوئال 97 – 115)`
   - `[قازا ۋە قەدەرگە ئىمان كەلتۈرۈش](/2000/01-etiqad/07-qada-qeder/) (سوئال 116 – 134)`
   - `[قىيامەت ۋە ئاخىرەتكە ئىمان كەلتۈرۈش](/2000/01-etiqad/08-qiyamet-axiret/) (سوئال 135 – 163)`
   Update Section 2 question ranges to match the actual file boundaries (e.g., 164–183, 184–204, 205–248, 249–259, 260–274, 275–332, etc.).

3. **Normalize lingering `\u06cc` (Farsi Yeh) to `\u064a` (Standard Uyghur ي)**:
   - `src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx`: lines 77, 79, 81, 108
   - `src/content/docs/2000/01-etiqad/05-samawiy-kitablar.mdx`: line 15
   - `src/content/docs/2000/01-etiqad/08-qiyamet-axiret.mdx`: line 65

4. **Update `tests/e2e_2000.py`**:
   Add `test_zero_farsi_yeh` to Tier 2 checking `\u06cc` across all `src/content/docs/2000/` files to ensure §R1 is permanently verified.

---

## 5. Verification Method

To verify resolution of these findings:

```bash
# 1. Verify exactly 8 files remain in 01-etiqad
ls -1 src/content/docs/2000/01-etiqad/ | wc -l
# Expected output: 8

# 2. Verify zero occurrences of \u06cc across all 2000 docs
grep -rn $'\u06cc' src/content/docs/2000/
# Expected output: (empty)

# 3. Verify 04-munderije.mdx has no references to obsolete slugs
grep -E "rohiy-alemler|kitablar-peyghemberler|qaza-qeder|07-qiyamet" src/content/docs/2000/00-muqeddimu/04-munderije.mdx
# Expected output: (empty)

# 4. Run the full E2E test suite
python3 tests/e2e_2000.py -v
# Expected output: 100% PASS across Tiers 1-4

# 5. Run production build
pnpm build
# Expected output: Exit code 0, dist/pagefind generated
```
