# Comprehensive Remediation Plan & Handoff Report — explorer_fix_2

**Role**: teamwork_preview_explorer  
**Working Directory**: `/Users/arslan/code/derslik/.agents/explorer_fix_2/`  
**Target Project**: Din ve Hayat (2000 Sualliq) Part 1 Conversion  
**Authoritative Request**: `/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md`  
**Gate Input**: `/Users/arslan/code/derslik/.agents/orchestrator_7/GATE_STATUS.md`  
**Auditor Handoff**: `/Users/arslan/code/derslik/.agents/auditor_1/handoff.md`  
**Date**: 2026-09-15T20:58:00Z  

---

## Executive Summary

Following the comprehensive forensic audit by `auditor_1` (verdict: `INTEGRITY VIOLATION`), `reviewer_1` & `reviewer_2` (verdict: `REQUEST_CHANGES`), and `challenger_1` & `challenger_2` (verdict: `REJECT`), this report establishes an exact, empirical, step-by-step remediation plan to resolve 100% of the defects blocking approval:

1. **Delete 4 obsolete files** in `src/content/docs/2000/01-etiqad/` (`04-rohiy-alemler.mdx`, `05-kitablar-peyghemberler.mdx`, `06-qaza-qeder.mdx`, `07-qiyamet-axiret.mdx`), eliminating 53 duplicate cards, restoring Section 01 file count to 8, and clearing sidebar pollution.
2. **Update `00-muqeddimu/04-munderije.mdx`** (and harmonize `index.mdx`) with the canonical 8-file Section 01 structure and exact question ranges across all 22 Q&A files.
3. **Normalize all 6 lingering `\u06cc` (Farsi yeh)** characters across `01-etiqad/03-allahning-isimliri.mdx`, `01-etiqad/05-samawiy-kitablar.mdx`, and `01-etiqad/08-qiyamet-axiret.mdx` (plus `tools/extracted_2000.json`) to standard Uyghur `ي` (`\u064a`).
4. **Fix 99 Names of Allah table duplication** in `01-etiqad/03-allahning-isimliri.mdx` row 76 (line 88), replacing the duplicate `الصَّمَدُ` (`ئەسسەمەد`) with `السُّبُّوحُ` (`ئەسسۇببۇھ`) from page 66 of the source book, and synchronize `tools/extracted_2000.json` and `tools/extract_2000.py`.
5. **Add `test_zero_farsi_yeh` and distinct names assertion** to `tests/e2e_2000.py` to ensure regression prevention.
6. **Execute full production build** (`pnpm build`) and E2E test suite (`python3 tests/e2e_2000.py -v`).

---

## 1. Observation

### Obs 1. Physical Presence of 4 Obsolete Files in `src/content/docs/2000/01-etiqad/`
Direct listing of `src/content/docs/2000/01-etiqad/` confirms 12 files instead of 8:
- **Canonical files (8 files)**:
  1. `01-din-ve-etiqad.mdx` (11,661 bytes, `order: 1`, Q1–20)
  2. `02-allahqa-iman.mdx` (18,285 bytes, `order: 2`, Q21–48)
  3. `03-allahning-isimliri.mdx` (33,025 bytes, `order: 3`, Q49–62 + 99 Names table)
  4. `04-perishtiler-jinlar.mdx` (16,737 bytes, `order: 4`, Q63–82)
  5. `05-samawiy-kitablar.mdx` (11,349 bytes, `order: 5`, Q83–96)
  6. `06-peyghamberler.mdx` (13,857 bytes, `order: 6`, Q97–115)
  7. `07-qada-qeder.mdx` (12,153 bytes, `order: 7`, Q116–134)
  8. `08-qiyamet-axiret.mdx` (16,135 bytes, `order: 8`, Q135–163)
- **Obsolete files to be deleted (4 files)**:
  1. `04-rohiy-alemler.mdx` (25,115 bytes, `order: 4` [collides with canonical 04], duplicate Q63–82 with reversed RTL word order, e.g. line 12: `ئالەملەر؟ قانداق دﭔگەن ئالەملەر روھىي`)
  2. `05-kitablar-peyghemberler.mdx` (21,986 bytes, `order: 5` [collides with canonical 05], duplicate Q83–115 with reversed RTL word order, e.g. line 12: `كىتابلار؟ قانداق كىتابلىرى ئاللاھنىۅ`)
  3. `06-qaza-qeder.mdx` (168 bytes, 9 lines, `order: 6` [collides with canonical 06], empty skeleton with zero questions)
  4. `07-qiyamet-axiret.mdx` (206 bytes, 9 lines, `order: 7` [collides with canonical 07], empty skeleton with zero questions)

### Obs 2. Question Continuity & Card Duplication
- Across the canonical files:
  - Section 01: Q1–20, Q21–48, Q49–62, Q63–82, Q83–96, Q97–115, Q116–134, Q135–163 = 163 contiguous questions without gaps.
  - Section 02: Q164–183, Q184–204, Q205–248, Q249–259, Q260–274, Q275–332, Q333–393, Q394–428, Q429–477, Q478–506, Q507–553, Q554–607, Q608–634, Q635–647 = 484 contiguous questions without gaps.
  - Total canonical questions = 163 + 484 = 647 unique questions.
- In workspace currently: Grep for `qa-card` finds **700** cards (647 unique + 53 duplicates from `04-rohiy-alemler.mdx` [20 cards] and `05-kitablar-peyghemberler.mdx` [33 cards]).

### Obs 3. Broken Links and Desynchronized Ranges in `04-munderije.mdx`
In `src/content/docs/2000/00-muqeddimu/04-munderije.mdx`:
- Line 59 links to `/2000/01-etiqad/04-rohiy-alemler/` (becomes 404 dead link once obsolete file is deleted).
- Line 65 links to `/2000/01-etiqad/05-kitablar-peyghemberler/` (becomes 404 dead link).
- Line 72 links to `/2000/01-etiqad/06-qaza-qeder/` (becomes 404 dead link).
- Line 77 links to `/2000/01-etiqad/07-qiyamet-axiret/` (becomes 404 dead link).
- It omits links to 5 canonical pages: `04-perishtiler-jinlar.mdx`, `05-samawiy-kitablar.mdx`, `06-peyghamberler.mdx`, `07-qada-qeder.mdx`, `08-qiyamet-axiret.mdx`.
- Section 01 and Section 02 list out-of-sync question spans that contradict actual files (e.g. lists Q1–25 instead of Q1–20, Q26–47 instead of Q21–48, Q164–180 instead of Q164–183, etc.).

### Obs 4. Lingering Legacy Farsi Yeh (`\u06cc`) Glyphs
Across all canonical documentation files, exactly six (6) instances of `\u06cc` remain:
1. `src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx`:
   - Line 77: `| الحَيِيُّ | ئەل ھەیىي | ...` (Name 65 has `\u06cc` in `ئەل ھەیىي`)
   - Line 79: `| القَيُّومُ | ئەل قەیيۇم | ...` (Name 67 has `\u06cc` in `ئەل قەیيۇم`)
   - Line 81: `| الدَّيَّانُ | ئەددەیيان | ...` (Name 69 has `\u06cc` in `ئەددەیيان`)
   - Line 108: `| السَّيِّدُ | ئەسسەیيىد | ...` (Name 96 has `\u06cc` in `ئەسسەیيىد`)
2. `src/content/docs/2000/01-etiqad/05-samawiy-kitablar.mdx`:
   - Line 15: `ئاللاھنىڭ كىتابلىرى ئاللاھ پەیغەمبەرلەرگە چۈشۈرگەن مۇقەددەس كىتابلاردۇر.` (`\u06cc` in `پەیغەمبەرلەرگە`)
3. `src/content/docs/2000/01-etiqad/08-qiyamet-axiret.mdx`:
   - Line 65: `... دەلىللەر بىلەن رەت قىلىنىدۇ: یوقتىن ياراتقان ئاللاھ ...` (`\u06cc` in `یوقتىن`)
Additionally, `tools/extracted_2000.json` contains identical 6 instances (lines 92, 94, 96, 123, 1066, 1737).

### Obs 5. 99 Names of Allah Table Duplication (Row 76 vs Row 97)
In `src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx` (lines 11–111):
- Row 76 (line 88):
  `| الصَّمَدُ | ئەسسەمەد | ھېچكىمگە مۇھتاج بولمىغان، ھەممە مەخلۇقات ھاجەتلىرىنى راۋا قىلىشتا پەقەت ئۇنىڭغىلا يۈزلىنىدىغان ئۇلۇغ زاتتۇر. |`
- Row 97 (line 109):
  `| الصَّمَدُ | ئەسسەمەد | ھېچكىمگە مۇھتاج بولمىغان، بارچە مەۋجۇدات ئېھتىياجىدا ئۇنىڭغا مۇھتاج بولغان زاتتۇر. |`
- In the source book "دىن ۋە ھايات" on page 66, the name between `المُحِيطُ` and `المُبِينُ` is `السُّبُّوحُ` (`ئەسسۇببۇھ`), with meaning:
  `پۈتۈنلەي نۇقساندىن ۋە ھەر قانداق ئەيىبتىن پاك، بارلىق گۈزەل كامالىي سۈپەتلەر ئاللاھقىلا مەنسۇپ بولغان زاتتۇر.`
- In `tools/extracted_2000.json` line 103 and `tools/extract_2000.py` line 280 & 353, the name was also duplicated.

### Obs 6. Test Suite Blind Spot in `tests/e2e_2000.py`
- Tier 2 checks `\u066e` (`test_zero_dotless_beh`), `\u067b` (`test_zero_beeh_two_dots_below`), and interior `\u0640` (`test_zero_interior_tatweels`), but has no test method `test_zero_farsi_yeh` for `\u06cc`.
- Tier 3 `test_99_names_table` verifies row count is 99 and cells are non-empty, but does not assert that all 99 Arabic names are distinct (`len(set(arabic_names)) == 99`).

### Obs 7. Missing Production Build & Search Index
- `dist/2000/` does not exist on disk.
- `dist/sitemap-0.xml` contains 0 URLs under `/2000/`.
- `dist/pagefind/` search index does not include any of the 647 questions.

---

## 2. Logic Chain

1. **Test Failure Causality**: `tests/e2e_2000.py` Tier 1 tests `test_question_count` and `test_section_01_pages_and_boundaries` fail directly because the 4 obsolete files in `01-etiqad` cause file count to be 12 (asserts 8) and total question cards to be 700 (asserts 647).
2. **Navigation Corruption Causality**: Because `astro.config.mjs` configures `{ autogenerate: { directory: '2000/01-etiqad' } }`, Starlight generates sidebar navigation from all MDX files in the folder. Deleting the 4 obsolete files immediately restores clean 1..8 ordering without collisions.
3. **Link Integrity Causality**: Merely deleting the 4 obsolete files would leave 4 broken 404 links in `00-muqeddimu/04-munderije.mdx`. Therefore, updating `04-munderije.mdx` to reference the 8 canonical pages and synchronizing question ranges is required simultaneously.
4. **Specification Compliance Causality**: `ORIGINAL_REQUEST.md` §R1 mandates converting `\u06cc` (Farsi yeh) -> standard Uyghur `ي` (`\u064a`). The 6 lingering instances violate §R1. Replacing `\u06cc` with `\u064a` satisfies §R1. Adding `test_zero_farsi_yeh` ensures regression prevention.
5. **Theological & Content Accuracy Causality**: Having only 98 distinct names with `الصَّمَدُ` repeated twice violates `ORIGINAL_REQUEST.md` §R3 (full 99 Names of Allah table). Replacing row 76 with `السُّبُّوحُ` (`ئەسسۇببۇھ`) restores all 99 distinct canonical names.
6. **Acceptance Criteria Causality**: `ORIGINAL_REQUEST.md` Acceptance Criteria mandate a clean compile via `pnpm build` and indexed `/2000/` routes. Running `pnpm build` generates `dist/2000/` and Pagefind search indices.

---

## 3. Caveats

- **Read-Only Explorer Scope**: As an explorer agent (`teamwork_preview_explorer`), direct modification of project source code is prohibited by system guidelines. This report delivers complete, turnkey, machine-applicable code diffs and shell commands for the implementer/cleanup worker.
- **No Other Defects Discovered**: Thorough static AST parsing, line-by-line inspection, and regex searches confirmed that Sections 00, 01 (canonical), and 02 have zero other missing questions, zero interior tatweels, and zero other legacy glyphs.

---

## 4. Conclusion & Concrete Step-by-Step Remediation Plan

The exact sequence of remediation steps is as follows:

```
[Step 1: Delete 4 Obsolete Files in 01-etiqad]
       │
[Step 2: Update 00-muqeddimu/04-munderije.mdx & Harmonize index.mdx]
       │
[Step 3: Normalize Lingering \u06cc in Canonical MDX & JSON]
       │
[Step 4: Fix 99 Names Row 76 in 03-allahning-isimliri.mdx, JSON & Script]
       │
[Step 5: Enhance tests/e2e_2000.py with \u06cc & Distinct Names Checks]
       │
[Step 6: Run Full Build (pnpm build) & E2E Test Suite]
```

---

### Step 1: Delete 4 Obsolete Files in `src/content/docs/2000/01-etiqad/`

Execute shell deletion:
```bash
rm -f src/content/docs/2000/01-etiqad/04-rohiy-alemler.mdx \
      src/content/docs/2000/01-etiqad/05-kitablar-peyghemberler.mdx \
      src/content/docs/2000/01-etiqad/06-qaza-qeder.mdx \
      src/content/docs/2000/01-etiqad/07-qiyamet-axiret.mdx
```

*Verification after deletion*: Exactly 8 canonical files remain in `src/content/docs/2000/01-etiqad/` (`01` through `08`).

---

### Step 2: Update `src/content/docs/2000/00-muqeddimu/04-munderije.mdx` and `index.mdx`

#### 2.1 Complete Replacement for `src/content/docs/2000/00-muqeddimu/04-munderije.mdx`:

```markdown
---
title: "مۇندەرىجە"
description: "«دىن ۋە ھايات (2000 سوئالغا جاۋاب)» 1-قىسىمنىڭ تولۇق بۆلۈم، تېما ۋە سوئاللار مۇندەرىجىسى."
---

## كىرىش ۋە مۇقەددىمە

- [كىتاب ھەققىدە](/2000/00-muqeddimu/01-kitab-heqqide/)
  - كىتاب ھەققىدە قىسقىچە تونۇشتۇرۇش
  - نەشر ئۇچۇرلىرى ۋە CIP كاتالوگ مەلۇماتى
  - بېغىشلاش
  - كىتابنىڭ ئاساسىي ئالاھىدىلىكلىرى
- [ئاپتور ھەققىدە](/2000/00-muqeddimu/02-aptur-heqqide/)
  - مۇھەممەد يۈسۈپ مۇھەممەد تۇرسۇننىڭ تەرجىمىھالى
  - مىسىر ئەزھەر ئۇنىۋېرسىتېتىدىكى تەھسىلى
  - تەلىم-تەربىيە ۋە جامائەت خىزمەتلىرى
  - ئاپتورنىڭ ئىدىيەۋى قارىشى ۋە مېتودولوگىيەسى
  - ئاپتور يازغان ۋە نەشر قىلىنغان ئەسەرلەر
  - ئەرەب تىلىدىن ئۇيغۇرچىغا تەرجىمە قىلغان كىتابلىرى
- [كىرىش سۆز](/2000/00-muqeddimu/03-kirish-soz/)
  - ئاپتورنىڭ سۆزى
  - كىتابنىڭ قۇرۇلمىسى ۋە بۆلۈملىرى
  - تەتقىقات مېتودولوگىيەسى ۋە پىرىنسىپلىرى
- [مۇندەرىجە](/2000/00-muqeddimu/04-munderije/)

---

## 1-بۆلۈم: ئېتىقاد (سوئال 1 – 163)

### 1. [دىن ۋە ئېتىقاد](/2000/01-etiqad/01-din-ve-etiqad/) (سوئال 1 – 20)
- دىن ھەققىدە قىسقىچە چۈشەنچە
  - ئىنسان ۋە دىن
  - دىنىي ئاڭ ئىنسانلار بىلەن بىرگە يارىتىلغان
  - ئاللاھنىڭ دىنى ئەزەلدىن بىردۇر
  - دۇنيادا ھەق دىن بىردۇر
  - ئاللاھنىڭ دىنى پۈتۈن ئىنسانىيەتكە كەلگەن ئورتاق دىن
  - دىن ئىجتىمائىي زۆرۈرىيەتتۇر
  - ئىنسانلار ئىچكى دۇنياسىدىن باشقۇرىلىدۇ
  - ئىلىم-پەن دىننىڭ رولىنى ئوينىيالمايدۇ
  - ئىسلام دىنى ۋە ئۇنىڭ غايىسى
- ئىمان ۋە ئېتىقاد ئاساسلىرى
  - كەلىمە تەييىبە ۋە ئۇنىڭ مەنىسى
  - ئىنساننىڭ يارىتىلىش مەقسىتى ۋە ۋەزىپىسى
  - ئادەمنى ئىماندىن چىقىرىدىغان ئامىللار

### 2. [ئاللاھقا ئىمان كەلتۈرۈش](/2000/01-etiqad/02-allahqa-iman/) (سوئال 21 – 48)
- ئاللاھقا ئىمان كەلتۈرۈش ئۆز ئىچىگە ئالىدىغان ھەقىقەتلەر
- ئاللاھ تائالانى تونۇشنىڭ ۋاسىتىلىرى
- ئەقىلنىڭ ۋەزىپىسى ۋە ئۇنىڭ ئىسلام دىنىدىكى ئورنى
- ئاللاھنىڭ سۈپەتلىرى ئاللاھنى تونۇشنىڭ ۋاسىتىسىدۇر
- ئاللاھنى قۇرئان ۋە ھەدىسلەردە كەلگەن سۈپەتلىرىدىن تونۇش

### 3. [ئاللاھ تائالانىڭ گۈزەل ئىسىملىرى ۋە سۈپەتلىرى](/2000/01-etiqad/03-allahning-isimliri/) (سوئال 49 – 62)
- ئاللاھ تائالانىڭ 99 گۈزەل ئىسمى (مۇكەممەل ئۈچ ئىستونلۇق جەدۋەل)
- ئاللاھنىڭ ئىسىملىرى بىلەن سۈپەتلىرى ئوتتۇرىسىدىكى پەرق
- زاتىي ۋە سۈبۇتىي سۈپەتلەر
- ئاللاھ تائالانى دۇنيادا كۆز بىلەن كۆرگىلى بولمايدىغانلىقى ھەققىدە

### 4. [پەرىشتىلەر، جىنلار ۋە شەيتانلار](/2000/01-etiqad/04-perishtiler-jinlar/) (سوئال 63 – 82)
- روھىي ئالەملەرنىڭ ھەقىقىتى
- پەرىشتىلەرگە ئىمان كەلتۈرۈش ۋە ئۇلارنىڭ خاراكتېرى
- تۆت چوڭ پەرىشتە ۋە باشقا پەرىشتىلەرنىڭ ۋەزىپىلىرى
- جىنلار ۋە شەيتانلارنىڭ ھەقىقىتى، خاراكتېرى ھەم ئىنسانلار بىلەن بولغان مۇناسىۋىتى

### 5. [ساماۋىي كىتابلار ۋە قۇرئان كەرىم](/2000/01-etiqad/05-samawiy-kitablar/) (سوئال 83 – 96)
- ئاللاھنىڭ كىتابلىرىغا ئىمان كەلتۈرۈش (تەۋرات، زەبۇر، ئىنجىل ۋە سەھىپىلەر)
- ۋەھيى ۋە ئۇنىڭ مەنىسى
- قۇرئان كەرىمنىڭ ئالاھىدىلىكى ۋە ساقلىنىشى
- قۇرئان كەرىمنىڭ ئەدەبىي ۋە ئىلمىي مۆجىزىلىرى

### 6. [پەيغەمبەرلەرگە ئىمان كەلتۈرۈش](/2000/01-etiqad/06-peyghamberler/) (سوئال 97 – 115)
- پەيغەمبەرلەرگە ئىمان كەلتۈرۈش، ئۇلارنىڭ سانى ۋە ئالاھىدىلىكلىرى
- پەيغەمبەر ئەلەيھىسسالاملارنىڭ مۆجىزىلىرى
- ئۇلۇل ئەزم پەيغەمبەرلەر
- مۇھەممەد ئەلەيھىسسالامنىڭ ئاخىرقى پەيغەمبەرلىكى ۋە پەزىلەتلىرى

### 7. [قازا ۋە قەدەرگە ئىمان كەلتۈرۈش](/2000/01-etiqad/07-qada-qeder/) (سوئال 116 – 134)
- قازا ۋە قەدەرنىڭ مەنىسى ۋە ماھىيىتى
- تەقدىرگە ئىشىنىش ۋە ئىنساننىڭ ئىرادىسى
- ياخشىلىق ۋە يامانلىقنىڭ تەقدىرى
- تەۋەككۈل قىلىشنىڭ توغرا مەنىسى

### 8. [قىيامەت ۋە ئاخىرەتكە ئىمان كەلتۈرۈش](/2000/01-etiqad/08-qiyamet-axiret/) (سوئال 135 – 163)
- قىيامەتنىڭ كىچىك ۋە چوڭ ئالامەتلىرى
- ئۆلۈم، قەبرە ھاياتى ۋە بەرزەخ ئالىمى
- قايتا تىرىلىش، ھېساب-كىتاب، تارازا ۋە سىرات كۆۋرۈكى
- جەننەت ۋە دوزاخنىڭ مەڭگۈلۈكى

---

## 2-بۆلۈم: ئىبادەت (سوئال 164 – 647)

### 1. [ئىبادەتنىڭ ئەسلىي ماھىيىتى](/2000/02-ibadet/01-ibadet-esasliri/) (سوئال 164 – 183)
- ئىبادەتنىڭ تۈرلىرى، شەرتلىرى ۋە نىيەتنىڭ ئەھمىيىتى

### 2. [شەرىئەت ئىستىلاھلىرى](/2000/02-ibadet/02-sheriet-istilahliri/) (سوئال 184 – 204)
- پەرز (پەرزى ئەين، پەرزى كىپايە)، ۋاجىب، سۈننەت، مۇستەھەب، ھارام، مەكرۇھ ۋە مۇباھ

### 3. [پاكىزلىق ۋە تاھارەت](/2000/02-ibadet/03-pakliq-taharet/) (سوئال 205 – 248)
- تاھارەتنىڭ پەرزلىرى، سۈننەتلىرى ۋە تاھارەتنى سۇندۇرىدىغان ئامىللار
- سۇلارنىڭ تۈرلىرى ۋە پاكىزلىق قائىدىلىرى

### 4. [ئاياللارغا خاس ئەھكاملار](/2000/02-ibadet/04-ayallargha-xas/) (سوئال 249 – 259)
- ھەيز، نىپاس ۋە ئىستىھازە ئەھكاملىرى

### 5. [غۇسلى ۋە تەيەممۇم](/2000/02-ibadet/05-ghusul-teyemmum/) (سوئال 260 – 274)
- غۇسلىنىڭ پەرزلىرى ۋە تەرتىپى
- سۇ تېپىلمىغاندا ياكى ئىشلەتكىلى بولمىغاندا قىلىنىدىغان تەيەممۇم ئەھكاملىرى

### 6. [نامازنىڭ شەرتلىرى ۋە پەرزلىرى](/2000/02-ibadet/06-namaz-ehkamliri/) (سوئال 275 – 332)
- نامازنىڭ تۈرلىرى ۋە ۋاقىتلىرى
- ئەزان ۋە تەكبىر ئەھكاملىرى
- نامازنىڭ تاشقى شەرتلىرى ۋە ئىچكى رۇكۇنلىرى

### 7. [نامازنىڭ تۈزۈلۈشى ۋە ئوقۇلۇش تەرتىپى](/2000/02-ibadet/07-namaz-oqush/) (سوئال 333 – 393)
- نامازنىڭ باشتىن-ئاخىر ئەمەلىي ئوقۇلۇش باسقۇچلىرى
- قىرائەت، رۇكۇ، سەجدە ۋە تەشەھھۇد دۇئالىرى
- نامازدىكى ۋاجىبلار، سۈننەتلەر ۋە نامازنى بۇزىدىغان ئىشلار

### 8. [جامائەت ۋە جۈمە نامىزى](/2000/02-ibadet/08-jamaet-jume/) (سوئال 394 – 428)
- جامائەت نامىزىنىڭ پەزىلىتى ۋە ئىمامەتچىلىك شەرتلىرى
- جۈمە نامىزىنىڭ شەرتلىرى ۋە خۇتبە ئەھكاملىرى

### 9. [يولۇچىلار ۋە باشقا نامازلار](/2000/02-ibadet/09-bashqa-namazlar/) (سوئال 429 – 477)
- مۇساپىرنىڭ نامىزى، قەسىر قىلىش
- تەراۋىھ نامىزى، ھېيت نامازلىرى
- نەپلە نامازلار: تەھەججۇد، دۇھا، ئىستىخارە ۋە قۇياش-ئاي تۇتۇلغاندىكى نامازلار

### 10. [جىنازا نامىزى ۋە دەپنە ئىشلىرى](/2000/02-ibadet/10-jinaze-depne/) (سوئال 478 – 506)
- جان ئۈزۈلۈش ئالدىدىكى ئىشلار
- مېيىتنى يۇيۇش، كېپەنلەش ۋە جىنازا نامىزىنى ئوقۇش
- قەبرە ۋە دەپنە قىلىش قائىدىلىرى

### 11. [زاكات ۋە ئۇنىڭ ئەھكاملىرى](/2000/02-ibadet/11-zakat/) (سوئال 507 – 553)
- زاكاتنىڭ نىسابى ۋە ھېسابلاش قائىدىلىرى
- ئالتۇن، كۈمۈش، تىجارەت ماللىرى ۋە زىرائەتلەرنىڭ زاكىتى
- پىتىر سەدىقىسى ئەھكاملىرى

### 12. [روزا ۋە رامىزان ئەھكاملىرى](/2000/02-ibadet/12-roza-ramizan/) (سوئال 554 – 607)
- روزىنىڭ نىيىتى، پەرزلىرى ۋە روزىنى بۇزىدىغان ياكى بۇزمايدىغان ئىشلار
- قازا ۋە كاپارەت، پىديە ئەھكاملىرى
- ئېتىكاپنىڭ قائىدە-تەرتىپلىرى

### 13. [ھەج ۋە ئۆمرە پائالىيىتى](/2000/02-ibadet/13-hej-omre/) (سوئال 608 – 634)
- ھەج ۋە ئۆمرىنىڭ پەرزلىرى ۋە ۋاجىبلىرى
- ئىھرام، تاۋاپ، سەئيى، ئەرەفات ۋە مىنا ئەمەللىرى
- ھەج جىنايەتلىرى ۋە كاپارەتلىرى

### 14. [ساۋاب، گۇناھ ۋە تەۋبە](/2000/02-ibadet/14-sawab-gunah/) (سوئال 640 – 647)
- چوڭ گۇناھلار (كەبائىر) ۋە ئۇلارنىڭ دەرىجىلىرى
- ھەقىقىي تەۋبىنىڭ شەرتلىرى ۋە كەچۈرۈم تەلەپ قىلىش
```

#### 2.2 Alignment for `src/content/docs/2000/index.mdx` (Lines 65–73):

Replace:
```markdown
2. **01-ئېتىقاد بۆلۈمى (1–163-سوئاللار)**:
   - دىن ۋە ئىمان ئاساسلىرى (1–34)
   - ئاللاھ تائالاغا ئىمان ۋە سۈپەتلەر (35–48، 49–62)
   - ئاللاھنىڭ 99 گۈزەل ئىسمى (مەخسۇس ھۆسنۈل مۇستەقىل جەدۋەل)
   - پەرىشتىلەرگە ئىمان (63–72)
   - جىن ۋە شەيتانلار (73–82)
   - ساماۋى كىتابلار ۋە پەيغەمبەرلەر (83–115)
   - قازا ۋە قەدەر (116–134)
   - قىيامەت ۋە ئاخىرەت ھاياتى (135–163)
```

With:
```markdown
2. **01-ئېتىقاد بۆلۈمى (1–163-سوئاللار)**:
   - دىن ۋە ئېتىقاد ئاساسلىرى (1–20)
   - ئاللاھقا ئىمان كەلتۈرۈش (21–48)
   - ئاللاھنىڭ گۈزەل ئىسىملىرى ۋە سۈپەتلىرى (49–62، 99 ئىسىم جەدۋىلى)
   - پەرىشتىلەر، جىنلار ۋە شەيتانلار (63–82)
   - ساماۋى كىتابلار ۋە قۇرئان كەرىم (83–96)
   - پەيغەمبەرلەرگە ئىمان كەلتۈرۈش (97–115)
   - قازا ۋە قەدەرگە ئىمان (116–134)
   - قىيامەت ۋە ئاخىرەتكە ئىمان (135–163)
```

---

### Step 3: Normalize Residual `\u06cc` (Farsi Yeh) Across All Canonical Files & JSON

Apply character substitution `\u06cc` -> `\u064a` (`ي`):

#### 3.1 Target: `src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx`
- Line 77:
  - Before: `| الحَيِيُّ | ئەل ھەیىي | ...`
  - After:  `| الحَيِيُّ | ئەل ھەيىي | ...`
- Line 79:
  - Before: `| القَيُّومُ | ئەل قەیيۇم | ...`
  - After:  `| القَيُّومُ | ئەل قەييۇم | ...`
- Line 81:
  - Before: `| الدَّيَّانُ | ئەددەیيان | ...`
  - After:  `| الدَّيَّانُ | ئەددەييان | ...`
- Line 108:
  - Before: `| السَّيِّدُ | ئەسسەیيىد | ...`
  - After:  `| السَّيِّدُ | ئەسسەييىد | ...`

#### 3.2 Target: `src/content/docs/2000/01-etiqad/05-samawiy-kitablar.mdx`
- Line 15:
  - Before: `    <span class="qa-label">جاۋاب:</span> ئاللاھنىڭ كىتابلىرى ئاللاھ پەیغەمبەرلەرگە چۈشۈرگەن مۇقەددەس كىتابلاردۇر. ئۇلار ساماۋىي كىتابلار دەپ ئاتىلىدۇ.`
  - After:  `    <span class="qa-label">جاۋاب:</span> ئاللاھنىڭ كىتابلىرى ئاللاھ پەيغەمبەرلەرگە چۈشۈرگەن مۇقەددەس كىتابلاردۇر. ئۇلار ساماۋىي كىتابلار دەپ ئاتىلىدۇ.`

#### 3.3 Target: `src/content/docs/2000/01-etiqad/08-qiyamet-axiret.mdx`
- Line 65:
  - Before: `    <span class="qa-label">جاۋاب:</span> نەقلىي، ئەقلىي ۋە ھېسسىي دەلىللەر بىلەن رەت قىلىنىدۇ: یوقتىن ياراتقان ئاللاھ ئەلۋەتتە قايتا يارىتىشقا قادىردۇر; ...`
  - After:  `    <span class="qa-label">جاۋاب:</span> نەقلىي، ئەقلىي ۋە ھېسسىي دەلىللەر بىلەن رەت قىلىنىدۇ: يوقتىن ياراتقان ئاللاھ ئەلۋەتتە قايتا يارىتىشقا قادىردۇر; ...`

#### 3.4 Target: `tools/extracted_2000.json`
- Line 92: `"transliteration": "ئەل ھەيىي"`
- Line 94: `"transliteration": "ئەل قەييۇم"`
- Line 96: `"transliteration": "ئەددەييان"`
- Line 123: `"transliteration": "ئەسسەييىد"`
- Line 1066: `"answer": "... پەيغەمبەرلەرگە ..."`
- Line 1737: `"answer": "...: يوقتىن ..."`

---

### Step 4: Fix Duplicate Name Entry #76 in 99 Names Table

#### 4.1 Target: `src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx`
- Line 88 (Row 76):
  - Before:
    `| الصَّمَدُ | ئەسسەمەد | ھېچكىمگە مۇھتاج بولمىغان، ھەممە مەخلۇقات ھاجەتلىرىنى راۋا قىلىشتا پەقەت ئۇنىڭغىلا يۈزلىنىدىغان ئۇلۇغ زاتتۇر. |`
  - After:
    `| السُّبُّوحُ | ئەسسۇببۇھ | پۈتۈنلەي نۇقساندىن ۋە ھەر قانداق ئەيىبتىن پاك، بارلىق گۈزەل كامالىي سۈپەتلەر ئاللاھقىلا مەنسۇپ بولغان زاتتۇر. |`

#### 4.2 Target: `tools/extracted_2000.json`
- Line 103 (id 76):
  - Before:
    `{"id": 76, "arabic": "الصَّمَدُ", "transliteration": "ئەسسەمەد", "meaning": "ھېچكىمگە مۇھتاج بولمىغان، ھەممە مەخلۇقات ھاجەتلىرىنى راۋا قىلىشتا پەقەت ئۇنىڭغىلا يۈزلىنىدىغان ئۇلۇغ زاتتۇر."},`
  - After:
    `{"id": 76, "arabic": "السُّبُّوحُ", "transliteration": "ئەسسۇببۇھ", "meaning": "پۈتۈنلەي نۇقساندىن ۋە ھەر قانداق ئەيىبتىن پاك، بارلىق گۈزەل كامالىي سۈپەتلەر ئاللاھقىلا مەنسۇپ بولغان زاتتۇر."},`

#### 4.3 Target: `tools/extract_2000.py`
- Line 280: Replace `"الصَّمَدُ"` with `"السُّبُّوحُ"`.
- Line 353: Replace `"ئەسسەمەد"` with `"ئەسسۇببۇھ"`.

---

### Step 5: Enhance `tests/e2e_2000.py` for Regression Prevention

#### 5.1 Add `test_zero_farsi_yeh` to Tier 2 (after line 449):

```python
    def test_zero_farsi_yeh(self) -> TestCaseResult:
        """Verify zero occurrences of \\u06cc (Farsi yeh) across docs/2000."""
        farsi_yeh = "\u06cc"
        matches = []

        if self.docs_root.exists():
            for f in self.docs_root.glob("**/*"):
                if f.is_file() and f.suffix in (".mdx", ".md", ".json", ".html"):
                    try:
                        text = f.read_text(encoding="utf-8")
                        count = text.count(farsi_yeh)
                        if count > 0:
                            matches.append(f"{f.relative_to(self.project_root)}: {count} occurrences")
                    except Exception:
                        pass

        passed = len(matches) == 0
        msg = f"Occurrences of \\u06cc: {len(matches)} files affected"
        return TestCaseResult("Zero Legacy Glyph \\u06cc (Farsi Yeh)", passed, msg, matches[:10])
```

#### 5.2 Add `self.test_zero_farsi_yeh()` to `run_tier_2` (line 706):

```python
    def run_tier_2(self) -> List[TestCaseResult]:
        return [
            self.test_zero_dotless_beh(),
            self.test_zero_beeh_two_dots_below(),
            self.test_zero_farsi_yeh(),
            self.test_zero_interior_tatweels(),
            self.test_boundary_questions_integrity(),
        ]
```

#### 5.3 Add Distinct Names Assertion to `test_99_names_table` (around line 587):

```python
        arabic_names = [row[0] for row in data_rows]
        distinct_arabic_count = len(set(arabic_names))
        if distinct_arabic_count != 99:
            details.append(f"Expected 99 distinct Arabic names, found {distinct_arabic_count} (duplicates exist)")

        passed = (row_count == 99) and (unfilled_cells == 0) and (distinct_arabic_count == 99)
```

---

### Step 6: Automated Execution Script for Workers

Workers can execute the remediation deterministically with the following Python snippet or bash script:

```bash
#!/bin/bash
set -e

# 1. Delete obsolete files
rm -f src/content/docs/2000/01-etiqad/04-rohiy-alemler.mdx \
      src/content/docs/2000/01-etiqad/05-kitablar-peyghemberler.mdx \
      src/content/docs/2000/01-etiqad/06-qaza-qeder.mdx \
      src/content/docs/2000/01-etiqad/07-qiyamet-axiret.mdx

# 2. Run in-place replacement for \u06cc and Row 76
python3 -c '
from pathlib import Path

# Fix 03-allahning-isimliri.mdx
f3 = Path("src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx")
c3 = f3.read_text(encoding="utf-8")
c3 = c3.replace("\u06cc", "\u064a")
old_row_76 = "| الصَّمَدُ | ئەسسەمەد | ھېچكىمگە مۇھتاج بولمىغان، ھەممە مەخلۇقات ھاجەتلىرىنى راۋا قىلىشتا پەقەت ئۇنىڭغىلا يۈزلىنىدىغان ئۇلۇغ زاتتۇر. |"
new_row_76 = "| السُّبُّوحُ | ئەسسۇببۇھ | پۈتۈنلەي نۇقساندىن ۋە ھەر قانداق ئەيىبتىن پاك، بارلىق گۈزەل كامالىي سۈپەتلەر ئاللاھقىلا مەنسۇپ بولغان زاتتۇر. |"
assert old_row_76 in c3, "Row 76 not found in 03-allahning-isimliri.mdx"
c3 = c3.replace(old_row_76, new_row_76)
f3.write_text(c3, encoding="utf-8")

# Fix 05-samawiy-kitablar.mdx
f5 = Path("src/content/docs/2000/01-etiqad/05-samawiy-kitablar.mdx")
f5.write_text(f5.read_text(encoding="utf-8").replace("\u06cc", "\u064a"), encoding="utf-8")

# Fix 08-qiyamet-axiret.mdx
f8 = Path("src/content/docs/2000/01-etiqad/08-qiyamet-axiret.mdx")
f8.write_text(f8.read_text(encoding="utf-8").replace("\u06cc", "\u064a"), encoding="utf-8")

# Fix tools/extracted_2000.json
fj = Path("tools/extracted_2000.json")
cj = fj.read_text(encoding="utf-8")
cj = cj.replace("\u06cc", "\u064a")
old_json_76 = "{\"id\": 76, \"arabic\": \"الصَّمَدُ\", \"transliteration\": \"ئەسسەمەد\", \"meaning\": \"ھېچكىمگە مۇھتاج بولمىغان، ھەممە مەخلۇقات ھاجەتلىرىنى راۋا قىلىشتا پەقەت ئۇنىڭغىلا يۈزلىنىدىغان ئۇلۇغ زاتتۇر.\"},"
new_json_76 = "{\"id\": 76, \"arabic\": \"السُّبُّوحُ\", \"transliteration\": \"ئەسسۇببۇھ\", \"meaning\": \"پۈتۈنلەي نۇقساندىن ۋە ھەر قانداق ئەيىبتىن پاك، بارلىق گۈزەل كامالىي سۈپەتلەر ئاللاھقىلا مەنسۇپ بولغان زاتتۇر.\"},"
assert old_json_76 in cj, "Row 76 not found in tools/extracted_2000.json"
cj = cj.replace(old_json_76, new_json_76)
fj.write_text(cj, encoding="utf-8")

print("In-place fixes applied cleanly.")
'

# 3. Verify zero lingering \u06cc across documentation
python3 -c '
from pathlib import Path
for p in Path("src/content/docs/2000").glob("**/*"):
    if p.is_file() and p.suffix in (".mdx", ".md"):
        txt = p.read_text(encoding="utf-8")
        assert "\u06cc" not in txt, f"Lingering \u06cc in {p}"
print("Zero \\u06cc verified across all documentation!")
'

# 4. Build and run tests
pnpm build
python3 tests/e2e_2000.py -v
```

---

## 5. Verification Method

Independent agents and reviewers can verify complete resolution using the following checks:

### Check 1: File Count & Structure Verification
```bash
# Must return exactly 8 files:
ls -1 src/content/docs/2000/01-etiqad/ | wc -l
# Expected output: 8

# Obsolete slugs must NOT exist:
ls src/content/docs/2000/01-etiqad/04-rohiy-alemler.mdx 2>&1 | grep "No such file"
ls src/content/docs/2000/01-etiqad/05-kitablar-peyghemberler.mdx 2>&1 | grep "No such file"
ls src/content/docs/2000/01-etiqad/06-qaza-qeder.mdx 2>&1 | grep "No such file"
ls src/content/docs/2000/01-etiqad/07-qiyamet-axiret.mdx 2>&1 | grep "No such file"
```

### Check 2: Question Card Count Verification
```bash
# Must return exactly 647 (no duplicate cards):
python3 -c '
from pathlib import Path
import re
cards = []
for p in Path("src/content/docs/2000").glob("**/*.mdx"):
    matches = re.findall(r"id=[\"\x27]q(\d+)[\"\x27]", p.read_text(encoding="utf-8"))
    cards.extend([int(m) for m in matches])
print(f"Total cards: {len(cards)}, Unique cards: {len(set(cards))}")
assert len(cards) == 647, f"Expected 647, found {len(cards)}"
assert len(set(cards)) == 647, "Duplicates detected!"
assert set(cards) == set(range(1, 648)), "Missing question numbers!"
print("Question continuity 1..647: PERFECT")
'
```

### Check 3: Unicode Normalization Verification
```bash
# Must return zero matches:
python3 -c '
from pathlib import Path
docs = list(Path("src/content/docs/2000").glob("**/*.mdx"))
for glyph, name in [("\u066e", "dotless beh"), ("\u067b", "beeh 2 dots"), ("\u06cc", "farsi yeh")]:
    found = [str(p) for p in docs if glyph in p.read_text(encoding="utf-8")]
    assert len(found) == 0, f"FAIL: {name} found in {found}"
print("Unicode glyphs \\u066e, \\u067b, \\u06cc: ZERO OCCURRENCES (100% CLEAN)")
'
```

### Check 4: 99 Distinct Names Verification
```bash
python3 -c '
from pathlib import Path
f = Path("src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx")
lines = [l.strip() for l in f.read_text(encoding="utf-8").splitlines() if l.strip().startswith("|") and not l.strip().startswith("| :---")]
names = [l.split("|")[1].strip() for l in lines[1:]] # skip header
print(f"Total rows: {len(names)}, Distinct: {len(set(names))}")
assert len(names) == 99, f"Expected 99 rows, got {len(names)}"
assert len(set(names)) == 99, f"Duplicates exist: {[n for n in names if names.count(n) > 1]}"
assert "السُّبُّوحُ" in names, "Al-Subbuh missing!"
assert names.count("الصَّمَدُ") == 1, "Al-Samad duplicated!"
print("99 Names of Allah: 99 DISTINCT CANONICAL NAMES VERIFIED")
'
```

### Check 5: Internal Link Integrity in `04-munderije.mdx`
```bash
python3 -c '
from pathlib import Path
import re
toc = Path("src/content/docs/2000/00-muqeddimu/04-munderije.mdx").read_text(encoding="utf-8")
links = re.findall(r"\[.*?\]\((/2000/.*?/)\)", toc)
for link in links:
    rel = link.strip("/").replace("2000/", "")
    candidate = Path("src/content/docs/2000") / (rel + ".mdx")
    if not candidate.exists():
        candidate = Path("src/content/docs/2000") / rel / "index.mdx"
    assert candidate.exists(), f"Dead link in TOC: {link} -> {candidate} not found"
print(f"All {len(links)} TOC links resolve to valid MDX files!")
'
```

### Check 6: Full Production Build & E2E Test Suite
```bash
# 1. Run full E2E test suite:
python3 tests/e2e_2000.py -v

# 2. Run full production build:
pnpm build

# 3. Verify dist/2000 and dist/pagefind:
test -d dist/2000 && test -d dist/pagefind && echo "BUILD VERIFIED CLEAN"
```
