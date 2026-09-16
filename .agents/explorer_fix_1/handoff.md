# Comprehensive Remediation Plan & Handoff Report — explorer_fix_1

**Target Artifact**: Din ve Hayat (2000 Sualliq) Part 1 Conversion  
**Author**: `explorer_fix_1` (teamwork_preview_explorer)  
**Recipient**: `orchestrator_7`  
**Date**: 2026-09-15T20:50:00Z  
**Status**: COMPLETE (Remediation Plan Ready for Execution)  

---

## Executive Summary
This report presents an exact, forensic, character-level remediation specification addressing every single defect identified in the forensic audit report (`auditor_1/handoff.md`), reviewer reports (`reviewer_1/handoff.md`, `reviewer_2/handoff.md`), and challenger reports (`challenger_1/handoff.md`, `challenger_2/handoff.md`).

All 5 core integrity failures are completely resolved by the steps outlined below:
1. **Physical deletion of 4 obsolete skeleton/duplicate files** in `src/content/docs/2000/01-etiqad/`, eliminating 53 duplicate cards and sidebar pollution.
2. **Comprehensive overhaul of Table of Contents in `00-muqeddimu/04-munderije.mdx`** and synchronization with `index.mdx`, eliminating all 404 links and aligning question ranges across both Creed and Worship sections.
3. **Normalization of all 6 residual `\u06cc` (Farsi yeh) characters** to standard Uyghur `ي` (`\u064a`) across canonical files and extraction dictionaries.
4. **Correction of the 99 Names of Allah table** by replacing the duplicate row 76 `الصَّمَدُ` with `السُّبُّوحُ` (`ئەسسۇببۇھ`), restoring all 99 distinct names.
5. **Hardening of the automated test harness `tests/e2e_2000.py`** with dedicated assertions for `\u06cc` (Farsi Yeh) and 99 distinct names uniqueness, followed by production build execution (`pnpm build`).

---

## 1. Observation

### Observation 1: The 4 Obsolete Files in `src/content/docs/2000/01-etiqad/`
A filesystem listing of `/Users/arslan/code/derslik/src/content/docs/2000/01-etiqad/` reveals 12 files instead of the required 8 canonical files:
- **Obsolete 1**: `04-rohiy-alemler.mdx` (25,115 bytes, 209 lines): Contains duplicate Q63–Q82 with reversed visual RTL word order (line 12: `ئالەملەر؟ قانداق دﭔگەن ئالەملەر روھىي`) and frontmatter `order: 4` colliding with canonical `04-perishtiler-jinlar.mdx`.
- **Obsolete 2**: `05-kitablar-peyghemberler.mdx` (21,986 bytes, 179 lines): Contains duplicate Q83–Q115 with reversed RTL word order (line 12: `كىتابلار؟ قانداق كىتابلىرى ئاللاھنىۅ`) and frontmatter `order: 5` colliding with canonical `05-samawiy-kitablar.mdx`.
- **Obsolete 3**: `06-qaza-qeder.mdx` (168 bytes, 9 lines): Empty skeleton containing only frontmatter stubs with `order: 6` (colliding with canonical `06-peyghamberler.mdx`) and zero question cards.
- **Obsolete 4**: `07-qiyamet-axiret.mdx` (206 bytes, 9 lines): Empty skeleton containing only frontmatter stubs with `order: 7` (colliding with canonical `07-qada-qeder.mdx`) and zero question cards.

The 8 canonical files present alongside them are:
1. `01-din-ve-etiqad.mdx` (`order: 1`, Q1–20)
2. `02-allahqa-iman.mdx` (`order: 2`, Q21–48)
3. `03-allahning-isimliri.mdx` (`order: 3`, 99 Names Table + Q49–62)
4. `04-perishtiler-jinlar.mdx` (`order: 4`, Q63–82)
5. `05-samawiy-kitablar.mdx` (`order: 5`, Q83–96)
6. `06-peyghamberler.mdx` (`order: 6`, Q97–115)
7. `07-qada-qeder.mdx` (`order: 7`, Q116–134)
8. `08-qiyamet-axiret.mdx` (`order: 8`, Q135–163)

### Observation 2: Broken Links & Out-of-Sync Question Spans in `00-muqeddimu/04-munderije.mdx`
Direct inspection of `src/content/docs/2000/00-muqeddimu/04-munderije.mdx` reveals:
- Lines 59–82 link directly to obsolete files:
  - Line 59: `### 4. [روھىي ئالەملەر: پەرىشتىلەر ۋە جىنلار](/2000/01-etiqad/04-rohiy-alemler/) (سوئال 79 – 106)`
  - Line 65: `### 5. [كىتابلار ۋە پەيغەمبەرلەرگە ئىمان](/2000/01-etiqad/05-kitablar-peyghemberler/) (سوئال 107 – 142)`
  - Line 72: `### 6. [قازا ۋە قەدەرگە ئىمان](/2000/01-etiqad/06-qaza-qeder/) (سوئال 143 – 152)`
  - Line 77: `### 7. [قىيامەت ۋە ئاخىرەتكە ئىمان](/2000/01-etiqad/07-qiyamet-axiret/) (سوئال 153 – 163)`
- Unlinking the obsolete files without updating `04-munderije.mdx` will create 4 dead 404 links on the site and leave 5 canonical files unlinked.
- The question number ranges in `04-munderije.mdx` contradict the canonical files:
  - Section 01: Claims Q1–25, Q26–47, Q48–78, Q79–106, Q107–142, Q143–152, Q153–163 (Actual: Q1–20, Q21–48, Q49–62, Q63–82, Q83–96, Q97–115, Q116–134, Q135–163).
  - Section 02: Claims Q164–180, Q181–193, Q194–226, Q227–241, Q242–257, Q258–322, Q323–384, Q385–442, Q443–500, Q501–525, Q526–572, Q573–614, Q615–639, Q640–647.
  - Actual canonical Section 02 ranges (also listed in `index.mdx`): Q164–183, Q184–204, Q205–248, Q249–259, Q260–274, Q275–332, Q333–393, Q394–428, Q429–477, Q478–506, Q507–553, Q554–607, Q608–634, Q635–647.

### Observation 3: Lingering Farsi Yeh (`\u06cc`) in Canonical Files
Ripgrep regex search (`\x{06cc}`) across the entire `src/` directory confirms exactly 6 occurrences in canonical documentation files:
1. `src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx`:
   - Line 77: `| الحَيِيُّ | ئەل ھەیىي | ...` (contains `\u06cc` in `ئەل ھەیىي`)
   - Line 79: `| القَيُّومُ | ئەل قەیيۇم | ...` (contains `\u06cc` in `ئەل قەیيۇم`)
   - Line 81: `| الدَّيَّانُ | ئەددەیيان | ...` (contains `\u06cc` in `ئەددەیيان`)
   - Line 108: `| السَّيِّدُ | ئەسسەیيىد | ...` (contains `\u06cc` in `ئەسسەیيىد`)
2. `src/content/docs/2000/01-etiqad/05-samawiy-kitablar.mdx`:
   - Line 15: `... ئاللاھ پەیغەمبەرلەرگە چۈشۈرگەن ...` (contains `\u06cc` in `پەیغەمبەرلەرگە`)
3. `src/content/docs/2000/01-etiqad/08-qiyamet-axiret.mdx`:
   - Line 65: `... دەلىللەر بىلەن رەت قىلىنىدۇ: یوقتىن ياراتقان ئاللاھ ...` (contains `\u06cc` in `یوقتىن`)
Additionally, `tools/extracted_2000.json` has 2 occurrences:
- Line 96 (id 69): `"transliteration": "ئەددەیيان"`
- Line 123 (id 96): `"transliteration": "ئەسسەیيىد"`

### Observation 4: 99 Names of Allah Table Duplication (Only 98 Distinct Names)
In `src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx`:
- Line 88 (Row 76): `| الصَّمَدُ | ئەسسەمەد | ھېچكىمگە مۇھتاج بولمىغان، ھەممە مەخلۇقات ھاجەتلىرىنى راۋا قىلىشتا پەقەت ئۇنىڭغىلا يۈزلىنىدىغان ئۇلۇغ زاتتۇر. |`
- Line 109 (Row 97): `| الصَّمَدُ | ئەسسەمەد | ھېچكىمگە مۇھتاج بولمىغان، بارچە مەۋجۇدات ئېھتىياجىدا ئۇنىڭغا مۇھتاج بولغان زاتتۇر. |`
- The name `الصَّمَدُ` appears twice. As verified from the original source PDF page 66 and reviewer/challenger reports, row 76 is `السُّبُّوحُ` (`ئەسسۇببۇھ`) with meaning:
  `پۈتۈنلەي نۇقساندىن ۋە ھەر قانداق ئەيىبتىن پاك، بارلىق گۈزەل كامالىي سۈپەتلەر ئاللاھقىلا مەنسۇپ بولغان زاتتۇر.`
- `tools/extract_2000.py` line 280 and `tools/extracted_2000.json` line 103 carry the same duplication.

### Observation 5: Missing Build Artifacts & Test Gaps in `tests/e2e_2000.py`
- `dist/2000/` does not exist on disk.
- `tests/e2e_2000.py` currently checks `\u066e` and `\u067b` in Tier 2, but has no check for `\u06cc` (Farsi Yeh).
- `tests/e2e_2000.py` Tier 3 checks `row_count == 99` and `unfilled_cells == 0`, but does not assert that all 99 names are distinct (`len(set(arabic_names)) == 99`).

---

## 2. Logic Chain

1. **Sidebar Navigation & Test Failure**: From Observation 1, because `astro.config.mjs` configures `{ autogenerate: { directory: '2000/01-etiqad' } }`, having 12 files in `01-etiqad/` exposes empty stubs and corrupt inverted text in the public sidebar, and causes `tests/e2e_2000.py` Tier 1 to fail (`test_section_01_pages_and_boundaries` sees 12 files instead of 8, and `test_question_count` sees 700 cards instead of 647).
2. **Link Integrity & User Experience**: From Observation 2, deleting the 4 obsolete files without modifying `04-munderije.mdx` would break navigation on the site with 4 critical 404 errors. Furthermore, the question number ranges in `04-munderije.mdx` misinform visitors about question distributions. Aligning both `04-munderije.mdx` and `index.mdx` with the 8 canonical files restores navigation integrity.
3. **Typography & Normalization Compliance**: From Observation 3, `ORIGINAL_REQUEST.md` §R1 explicitly commands: `"Convert \u06cc (Farsi yeh) -> standard Uyghur ي (\u064a)"`. Replacing the 6 lingering `\u06cc` occurrences satisfies this requirement 100%.
4. **Scholarly & Data Integrity**: From Observation 4, the 99 Names of Allah must contain 99 distinct divine names. Replacing duplicate #76 with `السُّبُّوحُ` (`ئەسسۇببۇھ`) restores the complete canonical list of 99 names as intended by author Muhammad Yusuf.
5. **Regression Prevention & Final Acceptance**: From Observation 5, enhancing `tests/e2e_2000.py` with `test_zero_farsi_yeh` and 99 distinct names validation permanently ensures these violations cannot recur. Executing `pnpm build` creates the production `dist/2000/` routes and Pagefind search index, satisfying the final acceptance criteria.

---

## 3. Caveats

- Unattended subprocess execution via `run_command` can time out on macOS environments if security dialog prompts require interactive confirmation. The implementation worker should execute the file edits directly using filesystem tools (`replace_file_content` / `write_to_file`) or execute commands with proper timeout handling.
- The 26 canonical MDX files themselves are genuine, scholar-reviewed, and structurally sound. Zero re-extraction or external downloads are required.

---

## 4. Conclusion & Concrete Remediation Plan

All defects are 100% remediable via the following 6 sequential steps.

### Step 1: Remove the 4 Obsolete Files from `01-etiqad/`
Delete the following 4 files from disk:
1. `/Users/arslan/code/derslik/src/content/docs/2000/01-etiqad/04-rohiy-alemler.mdx`
2. `/Users/arslan/code/derslik/src/content/docs/2000/01-etiqad/05-kitablar-peyghemberler.mdx`
3. `/Users/arslan/code/derslik/src/content/docs/2000/01-etiqad/06-qaza-qeder.mdx`
4. `/Users/arslan/code/derslik/src/content/docs/2000/01-etiqad/07-qiyamet-axiret.mdx`

Shell command:
```bash
rm -f src/content/docs/2000/01-etiqad/04-rohiy-alemler.mdx \
      src/content/docs/2000/01-etiqad/05-kitablar-peyghemberler.mdx \
      src/content/docs/2000/01-etiqad/06-qaza-qeder.mdx \
      src/content/docs/2000/01-etiqad/07-qiyamet-axiret.mdx
```

### Step 2: Update Table of Contents in `04-munderije.mdx` & `index.mdx`

#### 2.1 Edit `src/content/docs/2000/00-muqeddimu/04-munderije.mdx`
Replace lines 28–146 with:
```markdown
## 1-بۆلۈم: ئېتىقاد (سوئال 1 – 163)

### 1. [دىن ۋە ئىنسان](/2000/01-etiqad/01-din-ve-etiqad/) (سوئال 1 – 20)
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

### 3. [ئاللاھنىڭ گۈزەل ئىسىملىرى ۋە سۈپەتلىرى](/2000/01-etiqad/03-allahning-isimliri/) (سوئال 49 – 62 ۋە 99 ئىسىم جەدۋىلى)
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
- قۇرئان كەرىمنىڭ ئالاھىدىلىكى ۋە ساقلىنىشى
- قۇرئان كەرىمنىڭ مۆجىزىلىرى

### 6. [پەيغەمبەرلەرگە ئىمان كەلتۈرۈش](/2000/01-etiqad/06-peyghamberler/) (سوئال 97 – 115)
- پەيغەمبەرلەرگە ئىمان كەلتۈرۈش، ئۇلارنىڭ سانى ۋە ئالاھىدىلىكلىرى
- پەيغەمبەر ئەلەيھىسسالاملارنىڭ مۆجىزىلىرى
- مۇھەممەد ئەلەيھىسسالامنىڭ ئاخىرقى پەيغەمبەرلىكى

### 7. [قازا ۋە قەدەرگە ئىمان](/2000/01-etiqad/07-qada-qeder/) (سوئال 116 – 134)
- قازا ۋە قەدەرنىڭ مەنىسى ۋە ماھىيىتى
- تەقدىرگە ئىشىنىش ۋە ئىنساننىڭ ئىرادىسى
- تەۋەككۈل قىلىشنىڭ توغرا مەنىسى

### 8. [قىيامەت ۋە ئاخىرەتكە ئىمان](/2000/01-etiqad/08-qiyamet-axiret/) (سوئال 135 – 163)
- قىيامەتنىڭ كىچىك ۋە چوڭ ئالامەتلىرى
- ئۆلۈم، قەبرە ھاياتى ۋە بەرزەخ ئالىمى
- قايتا تىرىلىش، ھېساب-كىتاب، تارازا ۋە سىرات كۆۋرۈكى
- جەننەت ۋە دوزاخنىڭ مەڭگۈلۈكى

---

## 2-بۆلۈم: ئىبادەت (سوئال 164 – 647)

### 1. [ئىبادەتنىڭ ئەسلىي ماھىيىتى ۋە شەرتلىرى](/2000/02-ibadet/01-ibadet-esasliri/) (سوئال 164 – 183)
- ئىبادەتنىڭ تۈرلىرى، شەرتلىرى ۋە نىيەتنىڭ ئەھمىيىتى

### 2. [شەرىئەت ئىستىلاھلىرى](/2000/02-ibadet/02-sheriet-istilahliri/) (سوئال 184 – 204)
- پەرز (پەرزى ئەين، پەرزى كىپايە)، ۋاجىب، سۈننەت، مۇستەھەب، ھارام، مەكرۇھ ۋە مۇباھ

### 3. [پاكىزلىق ۋە تاھارەت ئەھكاملىرى](/2000/02-ibadet/03-pakliq-taharet/) (سوئال 205 – 248)
- تاھارەتنىڭ پەرزلىرى، سۈننەتلىرى ۋە تاھارەتنى سۇندۇرىدىغان ئامىللار
- سۇلارنىڭ تۈرلىرى ۋە پاكىزلىق قائىدىلىرى

### 4. [ئاياللارغا خاس ئەھكاملار](/2000/02-ibadet/04-ayallargha-xas/) (سوئال 249 – 259)
- ھەيز، نىپاس ۋە ئىستىھازە ئەھكاملىرى

### 5. [غۇسلى ۋە تەيەممۇم ئەھكاملىرى](/2000/02-ibadet/05-ghusul-teyemmum/) (سوئال 260 – 274)
- غۇسلىنىڭ پەرزلىرى ۋە تەرتىپى
- سۇ تېپىلمىغاندا ياكى ئىشلەتكىلى بولمىغاندا قىلىنىدىغان تەيەممۇم ئەھكاملىرى

### 6. [نامازنىڭ ئەھمىيىتى ۋە شەرتلىرى](/2000/02-ibadet/06-namaz-ehkamliri/) (سوئال 275 – 332)
- نامازنىڭ تۈرلىرى ۋە ۋاقىتلىرى
- ئەزان ۋە تەكبىر ئەھكاملىرى
- نامازنىڭ تاشقى شەرتلىرى ۋە ئىچكى رۇكۇنلىرى

### 7. [ناماز ئوقۇش تەرتىبى](/2000/02-ibadet/07-namaz-oqush/) (سوئال 333 – 393)
- نامازنىڭ باشتىن-ئاخىر ئەمەلىي ئوقۇلۇش باسقۇچلىرى
- قىرائەت، رۇكۇ، سەجدە ۋە تەشەھھۇد دۇئالىرى
- نامازدىكى ۋاجىبلار، سۈننەتلەر ۋە نامازنى بۇزىدىغان ئىشلار

### 8. [جامائەت ۋە جۈمە نامازى](/2000/02-ibadet/08-jamaet-jume/) (سوئال 394 – 428)
- جامائەت نامىزىنىڭ پەزىلىتى ۋە ئىمامەتچىلىك شەرتلىرى
- جۈمە نامىزىنىڭ شەرتلىرى ۋە خۇتبە ئەھكاملىرى

### 9. [باشقا نامازلار](/2000/02-ibadet/09-bashqa-namazlar/) (سوئال 429 – 477)
- مۇساپىرنىڭ نامىزى، قەسىر قىلىش
- تەراۋىھ نامىزى، ھېيت نامازلىرى
- نەپلە نامازلار: تەھەججۇد، دۇھا، ئىستىخارە ۋە قۇياش-ئاي تۇتۇلغاندىكى نامازلار

### 10. [جىنازە ۋە دەپنە](/2000/02-ibadet/10-jinaze-depne/) (سوئال 478 – 506)
- جان ئۈزۈلۈش ئالدىدىكى ئىشلار
- مېيىتنى يۇيۇش، كېپەنلەش ۋە جىنازا نامىزىنى ئوقۇش
- قەبرە ۋە دەپنە قىلىش قائىدىلىرى

### 11. [زاكات ئەھكاملىرى](/2000/02-ibadet/11-zakat/) (سوئال 507 – 553)
- زاكاتنىڭ نىسابى ۋە ھېسابلاش قائىدىلىرى
- ئالتۇن، كۈمۈش، تىجارەت ماللىرى ۋە زىرائەتلەرنىڭ زاكىتى
- پىتىر سەدىقىسى ئەھكاملىرى

### 12. [روزا ۋە رامىزان](/2000/02-ibadet/12-roza-ramizan/) (سوئال 554 – 607)
- روزىنىڭ نىيىتى، پەرزلىرى ۋە روزىنى بۇزىدىغان ياكى بۇزمايدىغان ئىشلار
- قازا ۋە كاپارەت، پىديە ئەھكاملىرى
- ئېتىكاپنىڭ قائىدە-تەرتىپلىرى

### 13. [ھەج ۋە ئۈمرە](/2000/02-ibadet/13-hej-omre/) (سوئال 608 – 634)
- ھەج ۋە ئۆمرىنىڭ پەرزلىرى ۋە ۋاجىبلىرى
- ئىھرام، تاۋاپ، سەئيى، ئەرەفات ۋە مىنا ئەمەللىرى
- ھەج جىنايەتلىرى ۋە كاپارەتلىرى

### 14. [ساۋاب ۋە گۇناھ](/2000/02-ibadet/14-sawab-gunah/) (سوئال 635 – 647)
- چوڭ گۇناھلار (كەبائىر) ۋە ئۇلارنىڭ دەرىجىلىرى
- ھەقىقىي تەۋبىنىڭ شەرتلىرى ۋە كەچۈرۈم تەلەپ قىلىش
```

#### 2.2 Edit `src/content/docs/2000/index.mdx`
Replace lines 65–73 with:
```markdown
2. **01-ئېتىقاد بۆلۈمى (1–163-سوئاللار)**:
   - دىن ۋە ئىنسان (1–20)
   - ئاللاھقا ئىمان كەلتۈرۈش (21–48)
   - ئاللاھنىڭ گۈزەل ئىسىملىرى ۋە سۈپەتلىرى (49–62 ۋە 99 ئىسىم جەدۋىلى)
   - پەرىشتىلەر، جىنلار ۋە شەيتانلار (63–82)
   - ساماۋىي كىتابلار ۋە قۇرئان كەرىم (83–96)
   - پەيغەمبەرلەرگە ئىمان كەلتۈرۈش (97–115)
   - قازا ۋە قەدەرگە ئىمان (116–134)
   - قىيامەت ۋە ئاخىرەت ھاياتى (135–163)
```

### Step 3: Normalize Residual `\u06cc` (Farsi Yeh) Characters to `\u064a` (`ي`)

Perform exact character replacements:
1. `src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx`:
   - Line 77: `ئەل ھەیىي` -> `ئەل ھەيىي`
   - Line 79: `ئەل قەیيۇم` -> `ئەل قەييۇم`
   - Line 81: `ئەددەیيان` -> `ئەددەييان`
   - Line 108: `ئەسسەیيىد` -> `ئەسسەييىد`
2. `src/content/docs/2000/01-etiqad/05-samawiy-kitablar.mdx`:
   - Line 15: `پەیغەمبەرلەرگە` -> `پەيغەمبەرلەرگە`
3. `src/content/docs/2000/01-etiqad/08-qiyamet-axiret.mdx`:
   - Line 65: `یوقتىن` -> `يوقتىن`
4. `tools/extracted_2000.json`:
   - Line 96: `"transliteration": "ئەددەیيان"` -> `"transliteration": "ئەددەييان"`
   - Line 123: `"transliteration": "ئەسسەیيىد"` -> `"transliteration": "ئەسسەييىد"`

### Step 4: Fix 99 Names of Allah Duplicate Entry #76
In `src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx`:
Line 88 (Row 76):
Replace:
```markdown
| الصَّمَدُ | ئەسسەمەد | ھېچكىمگە مۇھتاج بولمىغان، ھەممە مەخلۇقات ھاجەتلىرىنى راۋا قىلىشتا پەقەت ئۇنىڭغىلا يۈزلىنىدىغان ئۇلۇغ زاتتۇر. |
```
With:
```markdown
| السُّبُّوحُ | ئەسسۇببۇھ | پۈتۈنلەي نۇقساندىن ۋە ھەر قانداق ئەيىبتىن پاك، بارلىق گۈزەل كامالىي سۈپەتلەر ئاللاھقىلا مەنسۇپ بولغان زاتتۇر. |
```

Also update dictionary files:
- `tools/extracted_2000.json` (line 103):
  ```json
  {"id": 76, "arabic": "السُّبُّوحُ", "transliteration": "ئەسسۇببۇھ", "meaning": "پۈتۈنلەي نۇقساندىن ۋە ھەر قانداق ئەيىبتىن پاك، بارلىق گۈزەل كامالىي سۈپەتلەر ئاللاھقىلا مەنسۇپ بولغان زاتتۇر."},
  ```
- `tools/extract_2000.py` (line 280): Replace `"الصَّمَدُ"` at item 76 with `"السُّبُّوحُ"`.

### Step 5: Test Suite Hardening in `tests/e2e_2000.py`
In `tests/e2e_2000.py`:
1. Add `test_zero_farsi_yeh` to Tier 2:
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
2. Register `self.test_zero_farsi_yeh()` inside `run_tier_2()`:
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
3. In `test_99_names_table`, add uniqueness check:
   ```python
   arabic_names = [row[0] for row in data_rows]
   distinct_names = set(arabic_names)
   if len(distinct_names) != 99:
       duplicates = [n for n in distinct_names if arabic_names.count(n) > 1]
       details.append(f"Expected 99 distinct names, found {len(distinct_names)} (duplicates: {duplicates})")
   passed = (row_count == 99) and (unfilled_cells == 0) and (len(distinct_names) == 99)
   ```

### Step 6: Build & Test Suite Verification
Run the verification sequence:
```bash
python3 tests/e2e_2000.py --skip-build -v
pnpm build
python3 tests/e2e_2000.py -v
```

---

## 5. Verification Method

To independently verify the complete fix once applied:

```bash
# 1. Verify exactly 8 files in 01-etiqad (no obsolete files remain)
test $(ls -1 src/content/docs/2000/01-etiqad/*.mdx | wc -l) -eq 8 && echo "PAGE COUNT: PASS (8 files)"

# 2. Verify exactly 647 question cards across docs/2000
test $(grep -c 'class="qa-card"' src/content/docs/2000/*/*.mdx | awk -F: '{s+=$2} END {print s}') -eq 647 && echo "CARDS COUNT: PASS (647 cards)"

# 3. Verify ZERO occurrences of \u06cc across docs/2000
python3 -c '
from pathlib import Path
matches = [str(f) for f in Path("src/content/docs/2000").glob("**/*") if f.is_file() and "\u06cc" in f.read_text(encoding="utf-8")]
assert len(matches) == 0, f"FAIL: Farsi yeh found in {matches}"
print("UNICODE NORMALIZATION: PASS (0 occurrences of \u06cc)")
'

# 4. Verify 99 distinct names in 03-allahning-isimliri.mdx
python3 -c '
from pathlib import Path
content = Path("src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx").read_text(encoding="utf-8")
names = [line.split("|")[1].strip() for line in content.splitlines() if line.strip().startswith("|") and not line.strip().startswith("| :---") and "ئەرەبچە" not in line]
assert len(names) == 99, f"Row count {len(names)} != 99"
assert len(set(names)) == 99, f"Only {len(set(names))} distinct names!"
assert "السُّبُّوحُ" in names, "السُّبُّوحُ missing!"
print("99 NAMES TABLE: PASS (99 rows, 99 distinct names, As-Subbuh present)")
'

# 5. Verify no broken links to obsolete files in 04-munderije.mdx
python3 -c '
content = Path("src/content/docs/2000/00-muqeddimu/04-munderije.mdx").read_text(encoding="utf-8")
bad = [s for s in ["rohiy-alemler", "kitablar-peyghemberler", "06-qaza-qeder", "07-qiyamet-axiret"] if s in content]
assert len(bad) == 0, f"FAIL: Obsolete slugs referenced in munderije: {bad}"
print("TABLE OF CONTENTS LINKS: PASS (0 obsolete slugs)")
'

# 6. Run full E2E test suite (Tiers 1-4)
python3 tests/e2e_2000.py -v
```
