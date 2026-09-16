# Review & Adversarial Critic Report — reviewer_1

## Review Summary

**Verdict**: **`REQUEST_CHANGES`**

---

## 1. Observation

1. **Physical Presence of Obsolete & Corrupt Files in Section 01 (`src/content/docs/2000/01-etiqad/`)**:
   - The directory currently contains **12 files** rather than the expected **8 canonical files**:
     - `04-rohiy-alemler.mdx` (25,115 bytes, 209 lines): Contains duplicate questions Q63–82 with legacy glyphs (`\u067b`, e.g. line 12 `دﭔگەن`), non-standard diacritics (`\u06ed`), and reversed right-to-left word ordering (e.g. line 12 `ئالەملەر؟ قانداق دﭔگەن ئالەملەر روھىي`).
     - `05-kitablar-peyghemberler.mdx` (21,986 bytes, 179 lines): Contains duplicate questions Q83–115 with reversed word ordering (e.g. line 12 `كىتابلار؟ قانداق كىتابلىرى ئاللاھنىۅ`).
     - `06-qaza-qeder.mdx` (168 bytes, 9 lines): Empty skeleton containing only frontmatter stubs.
     - `07-qiyamet-axiret.mdx` (206 bytes, 9 lines): Empty skeleton containing only frontmatter stubs.
   - The 8 canonical files also exist side-by-side:
     - `01-din-ve-etiqad.mdx` (11,661 bytes, Q1–20)
     - `02-allahqa-iman.mdx` (18,285 bytes, Q21–48)
     - `03-allahning-isimliri.mdx` (33,025 bytes, 99 Names Table + Q49–62)
     - `04-perishtiler-jinlar.mdx` (16,737 bytes, Q63–82)
     - `05-samawiy-kitablar.mdx` (11,349 bytes, Q83–96)
     - `06-peyghamberler.mdx` (13,857 bytes, Q97–115)
     - `07-qada-qeder.mdx` (12,153 bytes, Q116–134)
     - `08-qiyamet-axiret.mdx` (16,135 bytes, Q135–163)

2. **Broken Internal Links and Desynchronization in `00-muqeddimu/04-munderije.mdx`**:
   - In `src/content/docs/2000/00-muqeddimu/04-munderije.mdx`, the markdown table of contents points directly to the 4 obsolete filenames:
     - Line 59: `### 4. [روھىي ئالەملەر: پەرىشتىلەر ۋە جىنلار](/2000/01-etiqad/04-rohiy-alemler/) (سوئال 79 – 106)`
     - Line 65: `### 5. [كىتابلار ۋە پەيغەمبەرلەرگە ئىمان](/2000/01-etiqad/05-kitablar-peyghemberler/) (سوئال 107 – 142)`
     - Line 72: `### 6. [قازا ۋە قەدەرگە ئىمان](/2000/01-etiqad/06-qaza-qeder/) (سوئال 143 – 152)`
     - Line 77: `### 7. [قىيامەت ۋە ئاخىرەتكە ئىمان](/2000/01-etiqad/07-qiyamet-axiret/) (سوئال 153 – 163)`
   - As a result:
     - If the 4 obsolete files are deleted without updating `04-munderije.mdx`, lines 59, 65, 72, and 77 become **404 DEAD LINKS**.
     - `04-munderije.mdx` completely fails to link to 5 canonical pages: `04-perishtiler-jinlar.mdx`, `05-samawiy-kitablar.mdx`, `06-peyghamberler.mdx`, `07-qada-qeder.mdx`, and `08-qiyamet-axiret.mdx`.
   - Question ranges listed in `04-munderije.mdx` are completely out-of-sync with the canonical files across both sections:
     - Section 01:
       - Lists Q1–25 for `01-din-ve-etiqad` (actual is Q1–20)
       - Lists Q26–47 for `02-allahqa-iman` (actual is Q21–48)
       - Lists Q48–78 for `03-allahning-isimliri` (actual is Q49–62)
       - Lists Q79–106 for Spiritual Beings (actual is Q63–82)
       - Lists Q107–142 for Scripture & Prophets (actual is Q83–96 & Q97–115)
       - Lists Q143–152 for Divine Decree (actual is Q116–134)
       - Lists Q153–163 for Day of Judgement (actual is Q135–163)
     - Section 02:
       - Lists Q164–180 (actual is Q164–183)
       - Lists Q181–193 (actual is Q184–204)
       - Lists Q194–226 (actual is Q205–248)
       - Lists Q227–241 (actual is Q249–259)
       - Lists Q242–257 (actual is Q260–274)
       - Lists Q258–322 (actual is Q275–332)
       - Lists Q323–384 (actual is Q333–393)
       - Lists Q385–442 (actual is Q394–428)
       - Lists Q443–500 (actual is Q429–477)
       - Lists Q501–525 (actual is Q478–506)
       - Lists Q526–572 (actual is Q507–553)
       - Lists Q573–614 (actual is Q554–607)
       - Lists Q615–639 (actual is Q608–634)
       - Lists Q640–647 (actual is Q635–647)
   *(Note: In contrast, `src/content/docs/2000/index.mdx` contains the 100% correct question ranges).*

3. **E2E Test Harness Failures (`tests/e2e_2000.py`)**:
   - `test_question_count`: Scans all files in `src/content/docs/2000/`. Because `04-rohiy-alemler.mdx` and `05-kitablar-peyghemberler.mdx` contain duplicate card IDs (`id="q63"` .. `id="q115"`), `len(self.all_cards)` is 700 cards instead of 647. Fails with `Found 53 duplicate question numbers`.
   - `test_section_01_pages_and_boundaries`: Fails because `len(list(sec01_dir.glob("*.mdx")))` is 12 instead of 8.

4. **Starlight Navigation Configuration in `astro.config.mjs`**:
   - Line 117: `items: [{ autogenerate: { directory: '2000/01-etiqad' } }]`.
   - Starlight autogenerates sidebar navigation links from all `.mdx` files in the folder. With the 4 obsolete files present, the production sidebar exposes duplicate links, broken text, and blank pages.

5. **Inaccurate Self-Attestation in Worker Handoff Report**:
   - `/Users/arslan/code/derslik/.agents/worker_cleanup_e2e/handoff.md` reported that `01-din-ve-etiqad.mdx` contained Q1–18 and `02-allahqa-iman.mdx` contained Q19–48. Direct inspection confirms `01-din-ve-etiqad.mdx` contains Q1–20 and `02-allahqa-iman.mdx` contains Q21–48.
   - Worker handoff reported that `01-ibadet-esasliri.mdx` contained Q164–188 and `02-sheriet-istilahliri.mdx` contained Q189–212. Direct inspection confirms `01-ibadet-esasliri.mdx` contains Q164–183 and `02-sheriet-istilahliri.mdx` contains Q184–204.
   - Worker asserted that the pipeline was complete without checking internal link integrity in `04-munderije.mdx`.

6. **Verified Genuine Content & High Quality Implementations**:
   - **Section 00 (`00-muqeddimu/`)**: `01-kitab-heqqide.mdx` (CIP data & dedication), `02-aptur-heqqide.mdx` (Azhar biography, bibliography), `03-kirish-soz.mdx` (methodology, structure).
   - **Section 01 (`01-etiqad/`) Canonical Files**: Exactly 163 questions (Q1–163) contiguous without gaps.
   - **99 Names of Allah Table**: Located in `01-etiqad/03-allahning-isimliri.mdx` (lines 11–111). Exactly 99 data rows, 3 fully populated columns (Arabic vocalized with tashkeel, Uyghur transliteration, Uyghur meaning).
   - **Section 02 (`02-ibadet/`) Canonical Files**: Exactly 14 files, 484 questions (Q164–647) contiguous without gaps.
   - **Option B Card Styling**: Fully implemented in `src/styles/custom.css` (`.qa-card`, `.qa-question`, `.qa-number`, `.qa-answer`) using RTL logical properties (`border-inline-start`, `padding-inline-start`).
   - **Unicode Normalization**: 0 occurrences of `\u066e`, 0 occurrences of `\u067b`, and 0 interior tatweels in any canonical content.

---

## 2. Logic Chain

1. From Observation 1 and Observation 3, having 12 files in `01-etiqad/` causes `tests/e2e_2000.py` Tier 1 tests (`test_question_count` and `test_section_01_pages_and_boundaries`) to fail deterministically.
2. From Observation 1 and Observation 4, Starlight's `{ autogenerate: { directory: '2000/01-etiqad' } }` setting means that leaving the 4 obsolete files on disk corrupts the live site's navigation sidebar with duplicate and blank entries.
3. From Observation 2, simply deleting the 4 obsolete files without modifying `04-munderije.mdx` creates 4 broken internal links (404s) and leaves 5 canonical files orphaned from the table of contents.
4. From Observation 2 and Observation 5, `04-munderije.mdx` contains erroneous question ranges that contradict the actual canonical content files (whereas `index.mdx` has the correct ranges).
5. Therefore, the task is **not ready for approval**. Changes must be requested to clean up the obsolete files, fix the broken links, and synchronize `04-munderije.mdx`.

---

## 3. Findings

### [Critical] Finding 1: Obsolete & Corrupt Skeleton Files Present in `01-etiqad/`
- **What**: 4 obsolete files (`04-rohiy-alemler.mdx`, `05-kitablar-peyghemberler.mdx`, `06-qaza-qeder.mdx`, `07-qiyamet-axiret.mdx`) remain on disk.
- **Where**: `src/content/docs/2000/01-etiqad/`
- **Why**: Violates file layout contracts, pollutes the autogenerated Starlight sidebar with duplicate corrupted pages and empty stubs, and causes E2E Tier 1 tests to fail.
- **Suggestion**: Delete all 4 obsolete files.

### [Critical] Finding 2: Broken Links and Desynchronized Ranges in `00-muqeddimu/04-munderije.mdx`
- **What**: The table of contents links to the 4 obsolete files, omits links to 5 canonical files, and displays erroneous question number ranges.
- **Where**: `src/content/docs/2000/00-muqeddimu/04-munderije.mdx` (lines 59, 65, 72, 77, and throughout section breakdowns).
- **Why**: Deleting the obsolete files causes 404 links on the site; visitors using the table of contents will navigate to non-existent or wrong pages.
- **Suggestion**:
  1. Update link targets to canonical files:
     - `/2000/01-etiqad/04-perishtiler-jinlar/`
     - `/2000/01-etiqad/05-samawiy-kitablar/` and `/2000/01-etiqad/06-peyghamberler/`
     - `/2000/01-etiqad/07-qada-qeder/`
     - `/2000/01-etiqad/08-qiyamet-axiret/`
  2. Align question number ranges with `src/content/docs/2000/index.mdx` and the actual canonical content files.

### [Minor] Finding 3: Inaccurate Boundary Assertions in Worker Handoff
- **What**: Worker report documented inaccurate question spans (`Q1–18`, `Q19–48`, `Q164–188`, `Q189–212`).
- **Where**: `.agents/worker_cleanup_e2e/handoff.md`
- **Why**: Created confusion during verification.
- **Suggestion**: Use the verified question ranges documented in this review report.

---

## 4. Adversarial Stress-Testing & Attack Surface

| Challenge | Attack Scenario | Predicted / Actual Behavior | Status |
|-----------|-----------------|-----------------------------|--------|
| **Link Integrity** | User visits `/2000/00-muqeddimu/04-munderije/` and clicks on Section 01 links after obsolete files are unlinked. | Results in 404 Not Found on 4 links; unable to navigate to 5 canonical pages. | **VULNERABILITY CONFIRMED** |
| **Sidebar Pollution** | User navigates the documentation via the Starlight sidebar without deleting obsolete files. | Sidebar displays 12 entries under `01-ئېتىقاد`, two of which show backwards text and two show empty pages. | **VULNERABILITY CONFIRMED** |
| **Duplicate Card Anchors** | HTML deep link to `#q63` or `#q83`. | Browser anchor conflict because identical IDs exist in two separate files under the same URL path prefix. | **VULNERABILITY CONFIRMED** |
| **Unicode Normalization** | Search for legacy glyphs `\u066e` or `\u067b` in canonical files. | 0 occurrences found across all 26 canonical MDX files. | **PASSED** |
| **99 Names Completeness** | Missing cells or incorrect columns in `03-allahning-isimliri.mdx`. | 99 rows parsed, 0 empty cells, 3 complete columns verified. | **PASSED** |
| **Boundary Questions** | Keyword check for Q1, Q48, Q49, Q163, Q164, Q647. | All 6 landmark questions verified verbatim with non-empty answers. | **PASSED** |

---

## 5. Verified Claims

- Question continuity Q1 through Q647 present across canonical files → verified via direct file inspection → **PASS**
- 99 Names of Allah table has 99 rows and 3 columns → verified via direct file inspection → **PASS**
- Option B CSS present in `src/styles/custom.css` → verified via direct file inspection → **PASS**
- Starlight sidebar group configured in `astro.config.mjs` → verified via direct file inspection → **PASS**
- Zero legacy glyphs (`\u066e`, `\u067b`) in canonical files → verified via regex grep search → **PASS**
- Zero interior tatweels in canonical files → verified via regex grep search → **PASS**

---

## 6. Caveats

- Terminal execution (`pnpm build` and `python3 tests/e2e_2000.py`) was not executed dynamically in this turn due to interactive terminal confirmation constraints in the environment. All assertions are based on comprehensive, static code inspection and parsing of the codebase.
- No integrity violations (cheating, fake implementations, hardcoded falsifications) were found; the work done is genuine but currently blocked by lingering obsolete files and link desynchronization.

---

## 7. Conclusion

The conversion of Part 1 of "دىن ۋە ھايات (2000 سوئالغا جاۋاب)" has achieved exceptional content quality across all 647 questions, the 99 Names table, Option B CSS styling, and Starlight configuration.
However, because the 4 obsolete skeleton files remain on disk (blocking E2E Tier 1 tests and polluting the sidebar) and `00-muqeddimu/04-munderije.mdx` contains broken links pointing to those obsolete files, the review verdict is **`REQUEST_CHANGES`**.

---

## 8. Verification Method & Actionable Remediation Plan

To bring the project to 100% `APPROVE` readiness:

1. **Delete the 4 obsolete skeleton files**:
   ```bash
   rm -f src/content/docs/2000/01-etiqad/04-rohiy-alemler.mdx \
         src/content/docs/2000/01-etiqad/05-kitablar-peyghemberler.mdx \
         src/content/docs/2000/01-etiqad/06-qaza-qeder.mdx \
         src/content/docs/2000/01-etiqad/07-qiyamet-axiret.mdx
   ```

2. **Update `src/content/docs/2000/00-muqeddimu/04-munderije.mdx`**:
   - Replace the Section 01 links with:
     - `### 4. [پەرىشتىلەر، جىنلار ۋە شەيتانلار](/2000/01-etiqad/04-perishtiler-jinlar/) (سوئال 63 – 82)`
     - `### 5. [ساماۋىي كىتابلار ۋە قۇرئان كەرىم](/2000/01-etiqad/05-samawiy-kitablar/) (سوئال 83 – 96)`
     - `### 6. [پەيغەمبەرلەرگە ئىمان كەلتۈرۈش](/2000/01-etiqad/06-peyghamberler/) (سوئال 97 – 115)`
     - `### 7. [قازا ۋە قەدەرگە ئىمان](/2000/01-etiqad/07-qada-qeder/) (سوئال 116 – 134)`
     - `### 8. [قىيامەت ۋە ئاخىرەتكە ئىمان](/2000/01-etiqad/08-qiyamet-axiret/) (سوئال 135 – 163)`
   - Synchronize question ranges across all entries to match `src/content/docs/2000/index.mdx`.

3. **Verify via E2E test runner and build**:
   ```bash
   python3 tests/e2e_2000.py -v
   pnpm build
   ```
