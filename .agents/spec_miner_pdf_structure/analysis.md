# PDF Structure Analysis: "دىن ۋە ھايات (2000 سوئالغا جاۋاب)" — 1-قىسىم

**Document Target**: `/Users/arslan/.gemini/antigravity/brain/4cef4897-f493-4acb-b5ac-2ecb06b0aee7/.user_uploaded/media_1789428359497.pdf`  
**Analyzer**: PDF Structure Miner  
**Date**: 2026-09-15  
**Integrity Mode**: Development / Authoritative Extraction Specification  

---

## 1. Executive Summary & Source Document Overview

The source PDF represents Volume 1 (بىرىنچى قىسىم) of the landmark Uyghur Islamic reference work **"دىن ۋە ھايات (2000 سوئالغا جاۋاب)"** (*Religion and Life: 2000 Questions and Answers*) by the prominent scholar **Muhammad Yusuf Muhammad Tursun** (مۇھەممەد يۈسۈپ مۇھەممەد تۇرسۇن).

- **Total PDF Page Count**: Exactly **300 pages**.
- **Scope of Questions**: Exactly covers **Question 1 through Question 647** sequentially without any missing numbers or gaps.
- **Divisions Covered**:
  1. **مۇقەددىمە (Front Matter / Foreword)**: PDF Pages 1–30 (Book Pages 1–28). Includes Title, CIP, Dedication, Author Biography, Author Foreword, and Detailed Table of Contents (`مۇندەرىجە`).
  2. **1-بۆلۈم: ئېتىقاد (Division 1: Creed / Theology)**: PDF Pages 31–114 (Book Pages 29–111).
     - Topical introductory exposition on religion, intellect, and faith: Book Pages 30–35 (PDF 33–38).
     - **Questions 1 through 163**: Book Pages 36–111 (PDF 39–114).
     - **The 99 Names of Allah Table (`ئاللاھ تائالانىڭ ئىسىم-سۈپەتلىرى`)**: 3-column table spanning Book Pages 53–66 (PDF Pages 56–69), positioned between Question 48 and Question 49.
  3. **2-بۆلۈم: ئىبادەت (Division 2: Worship / Fiqh of Ibadah)**: PDF Pages 115–298 (Book Pages 112–294).
     - Topical introductory exposition on the essence of worship: Book Pages 113–114 (PDF 117–118).
     - **Questions 164 through 647**: Book Pages 115–294 (PDF 119–298).
  4. **3-بۆلۈم: ئەخلاق (Division 3: Ethics / Transition Page)**: PDF Page 299 (Book Page 295) marks the start of Division 3 in Volume 2; PDF Page 300 is blank.

---

## 2. Basic PDF Metadata & Page Geometry

| Attribute | Specification Value |
|---|---|
| **Total Pages** | 300 pages |
| **Physical Book Dimensions** | 16.5 cm × 24.0 cm (Royal 8vo format, 1401 pages across complete work) |
| **Page Layout** | Single-column RTL book layout with top running header and footnote footer |
| **Running Header** | Top of page separated by a thin horizontal rule (`<hr>`); contains Section Title / Topic on the inner side, and Book Page Number on the outer margin |
| **Running Footer** | Bottom of page separated by a horizontal rule when footnotes are present |
| **Page Numbering Offset** | • PDF Pages 1–12: Unnumbered / preliminary front matter<br>• PDF Pages 13–29: Book pages 12–28 (`مۇندەرىجە`)<br>• PDF Page 31: Division 1 Divider (Book Page 29)<br>• PDF Pages 33–114: Book pages 30–111 (Formula: `Book_Page = PDF_Page - 3`)<br>• PDF Page 115: Division 2 Divider (Book Page 112)<br>• PDF Pages 117–298: Book pages 113–294 (Formula: `Book_Page = PDF_Page - 4`) |
| **Blank Pages** | PDF Page 12, Page 30, Page 32, Page 116, Page 300 |

---

## 3. Text Extraction Quality & Typographical Quirks

### 3.1 RTL and Character Ordering
- **Extracted Stream Direction**: The extracted text maintains logical Right-to-Left character flow for Uyghur Arabic words.
- **Bi-directional Punctuation Flip**: In raw extraction, question numbers preceded by periods often invert due to Unicode BiDi algorithms (e.g., extracted as `.1 سوئال:` or `1. سوئال:` or `42. سوئال:`). The parsing regex must be resilient to both leading and trailing periods/spaces around question numbers.
- **Numbers**: Western Arabic digits (`0-9`) are used throughout the book for question numbers and page numbers, rather than Eastern Arabic digits (`٠-٩`).

### 3.2 Tatweel / Kashida Spacing
- The typesetting in the PDF applies extreme justification using `\u0640` (tatweel/kashida), sometimes inserting 2 to 6 tatweels within Uyghur words (e.g. `ئـٮنـسانـلارنـٮڭ`, `مۇھەمـمەد`, `قـٮلـٮش`, `ئـٮسـلام`).
- **Impact**: Searching for "ئىنسانلارنىڭ" fails completely on raw text containing tatweels. All interior tatweels within words MUST be stripped during normalization, while preserving intentional elongation in Arabic decorative script where appropriate.

### 3.3 Arabic Ligatures & Special Glyph Encodings
- In Arabic Qur'anic verses, certain OpenType ligatures in the PDF's proprietary Arabic typesetting font map to ASCII characters or unusual glyphs:
  - `الله` (Allah) is frequently extracted as `ا:` or `ا:Eُ` or `اÄ`.
  - `صلاة` is sometimes extracted as `صhة`.
  - `العالمين` is sometimes extracted as `3ََ` or `اْVعـ َعاV`.
  - `الرحمن` is sometimes extracted as `ال َر ْح َم ُن` or `الـ Eر ْـحمـٰ ِن`.
- **Parsing Strategy**: When processing Qur'anic citations and common Islamic phrases, standardize them into clean UTF-8 Arabic text with proper Uthmani diacritics.

---

## 4. Uyghur Legacy Glyph Normalization Specification

The source PDF was compiled using a legacy Uyghur DTP font system (common in Uyghur publications from the 1990s–2010s) that encoded specific Uyghur vowels using Arabic presentation glyphs.

| Legacy Code | Legacy Character | Description | Standard Code | Standard Uyghur | Standard Character Name |
|---|---|---|---|---|---|
| `\u066E` | `ٮ` | Arabic Letter Dotless Beh | `\u0649` | `ى` | Arabic Letter Alef Maksura (Uyghur Vowel "I") |
| `\u067B` | `ٻ` | Arabic Letter Beeh with 2 Vertical Dots | `\u06D0` | `ې` | Arabic Letter E (Uyghur Vowel "E") |
| `\u06CC` | `ی` | Arabic Letter Farsi Yeh | `\u064A` | `ي` | Arabic Letter Yeh (Uyghur Consonant "Y") |
| `\u0640` | `ـ` | Arabic Tatweel / Kashida | `""` | ` ` (stripped) | Interior tatweels removed from Uyghur words |

### Concrete Normalization Rules
1. **Rule 1 (`\u066E` -> `\u0649`)**:
   - Every occurrence of `\u066e` must become `\u0649` (`ى`).
   - Example: `دٮن` -> `دىن`, `بٮلەن` -> `بىلەن`, `قٮلٮش` -> `قىلىش`.
2. **Rule 2 (`\u067B` -> `\u06D0`)**:
   - Every occurrence of `\u067b` must become `\u06d0` (`ې`).
   - Example: `دٻگەن` -> `دېگەن`, `ئٻرٮشـكەن` -> `ئېرىشكەن`, `كٻیٮن` -> `كېيىن`.
3. **Rule 3 (`\u06CC` -> `\u064A`)**:
   - Every occurrence of Farsi yeh `\u06cc` must become standard Arabic/Uyghur yeh `\u064a` (`ي`).
   - Example: `یـاخشـى` -> `ياخشى`.
4. **Rule 4 (Tatweel Stripping)**:
   - Regex: `re.sub(r'([\u0600-\u06FF])\u0640+([\u0600-\u06FF])', r'\1\2', text)` repeated until all interior tatweels are removed.
5. **Rule 5 (Allah Ligature Clean-up)**:
   - Any broken representations like `ا:`, `ا:Eُ`, `اÄ`, `الـ Eر ْـحمـٰ ِن` normalized to standard `الله`, `الرحمن`.

---

## 5. Question Numbering Patterns & Syntactic Structure

Questions 1 to 647 follow a consistent structural pattern across the 300 pages:

### 5.1 Pattern Syntax
Each question unit consists of:
1. **Header Number & Prefix**:
   - Delimiter patterns in text:
     - `\.\s*(\d+)\s*سوئال:\s*` (e.g. `.1 سوئال:`, `.10 سوئال:`)
     - `(\d+)\s*\.\s*سوئال:\s*` (e.g. `42. سوئال:`, `164. سوئال:`)
     - `(\d+)\s*سوئال:\s*` (rare variant without period)
2. **Question Body**:
   - The question text ends with a question mark (`؟`).
3. **Answer Prefix**:
   - Followed by `جاۋاب:` (often with tatweels `جـاۋاب:`).
4. **Answer Body**:
   - Paragraph text explaining the ruling.
   - May contain numbered lists: `(1)`, `(2)`, `(3)` or `1`, `2`, `3`.
   - May contain Quranic quotes `﴿ ... ﴾` and Hadith citations.
   - May contain sub-sections or dialogue.

### 5.2 Option B Presentation (Continuous Reading Cards)
To provide the optimal reading experience requested in `ORIGINAL_REQUEST.md`:
- Each question should be formatted as a styled card component or Markdown section:
  ```markdown
  ### 1. ئنسانلار نەدىن پەيدا بولغان؟
  
  **جاۋاب**: ئىنسانلار ئاللاھ تەرىپىدىن يارىتىلغان.
  ```
- With Starlight Option B continuous reading card layout, question number `1` is highlighted in a badge or card header, followed by the question prompt, and the answer in the card body.

---

## 6. Footnotes and Scholarly Citations

### 6.1 Footnote Formatting in the PDF
- **In-Text Reference Markers**:
  - Quranic verse citations and Hadith sources are referenced by bracketed numbers: `(1)`, `(2)`, `(3)`, `1( )`, `( )1`, `(1)`.
  - Numbering restarts from `(1)` on **each page**.
- **Page Footers**:
  - Separated by a horizontal divider line at the bottom of the page.
  - Formatted as `1( ) سۈرە نامى ...` or `1() ئەھمەد رىۋايىتى.`
- **Nature of Footnotes**:
  1. **Qur'an Citations**: Exact Surah name and Ayah number (e.g., `مائىدە سۈرىسى 3-ئايەت`).
  2. **Hadith Collections**: Primary narrator and collection (`بۇخارى ۋە مۇسلىم رىۋايىتى`, `تىرمىزى رىۋايىتى`, `ئەبۇ داۋۇد رىۋايىتى`).
  3. **Biographical / Fiqh Commentary**: Lengthy scholarly treatises (e.g. Page 146 on the fiqh of wiping over socks; Page 161 on Ibn Taymiyyah's life; Page 178 on Dr. Yusuf al-Qaradawi's life; Page 199 on Imam al-Nawawi's life).
  4. **Definitions & Glossaries**: Explaining classical Arabic or Islamic terminology (e.g. `مەقامۇ ئىبراھىم`, `ئېھتىلام`, `سا`).

### 6.2 Markdown Footnote Conversion Specification
- Convert page-level footnote references into standard Markdown footnotes:
  - In-text reference: `[^q1_1]` or `[^q142_1]` (scoped by question number to avoid collisions).
  - Footnote definition at the end of the question or page:
    ```markdown
    [^q1_1]: مائىدە سۈرىسى 3-ئايەت.
    ```

---

## 7. Question Continuity & Verification Audit (1 through 647)

A complete page-by-page audit across all 300 pages confirms:
- **Starting Question**: Question 1 (PDF Page 39, Book Page 36).
- **Division 1 Endpoint**: Question 163 (PDF Page 114, Book Page 111).
- **Division 2 Startpoint**: Question 164 (PDF Page 119, Book Page 115).
- **Ending Question**: Question 647 (PDF Page 297–298, Book Page 293–294).
- **Continuity Status**: **100% Sequential, Zero Gaps, Zero Duplicates, Zero Skipped Numbers**.
- **Total Question Count**: Exactly **647 questions**.

### Questions Split Across Page Boundaries
Several questions and answers span across page boundaries. A robust parser must concatenate text until the next `\d+\s*سوئال:` delimiter or section heading:
- Question 34: spans PDF Page 44 (items 1-13) and Page 45 (items 14-15).
- Question 41: spans PDF Page 48 and Page 49.
- Question 43: spans PDF Page 50 and Page 51.
- Question 46: spans PDF Page 52 and Page 53.
- Question 91: spans PDF Page 81 and Page 82.
- Question 96: spans PDF Page 83, 84, and 85.
- Question 106: spans PDF Page 87 and Page 88.
- Question 108: spans PDF Page 88 and Page 89.
- Question 118: spans PDF Page 92 and Page 93.
- Question 119: spans PDF Page 94 and Page 95.
- Question 120: spans PDF Page 95 and Page 96.
- Question 125: spans PDF Page 96 and Page 97.
- Question 127: spans PDF Page 97 and Page 98.
- Question 131: spans PDF Page 99 and Page 100.
- Question 134: spans PDF Page 100 and Page 101.
- Question 139: spans PDF Page 102 and Page 103.
- Question 140: spans PDF Page 103, 104, and 105.
- Question 142: spans PDF Page 106 and Page 107.
- Question 147: spans PDF Page 108 and Page 109.
- Question 156: spans PDF Page 111 and Page 112.
- Question 157: spans PDF Page 112 and Page 113.
- Question 179: spans PDF Page 122, 123, and 124.
- Question 203: spans PDF Page 129 and Page 130.
- Question 204: spans PDF Page 130 and Page 131.
- Question 224: spans PDF Page 136.
- Question 229: spans PDF Page 137 and Page 138.
- Question 230: spans PDF Page 138, 139, and 140.
- Question 234: spans PDF Page 141 and Page 142.
- Question 236: spans PDF Page 142 and Page 143.
- Question 239: spans PDF Page 143 and Page 144.
- Question 243: spans PDF Page 145, 146, and 147.
- Question 247: spans PDF Page 147 and Page 148.
- Question 254: spans PDF Page 149 and Page 150.
- Question 259: spans PDF Page 150 and Page 151.
- Question 265: spans PDF Page 152 and Page 153.
- Question 278: spans PDF Page 158 and Page 159.
- Question 279: spans PDF Page 159 and Page 160.
- Question 283: spans PDF Page 162 and Page 163.
- Question 285: spans PDF Page 164, 165, and 166.
- Question 291: spans PDF Page 167 and Page 168.
- Question 293: spans PDF Page 168 and Page 169.
- Question 304: spans PDF Page 171 and Page 172.
- Question 315: spans PDF Page 175 and Page 176.
- Question 318: spans PDF Page 177, 178, and 179.
- Question 323: spans PDF Page 180 and Page 181.
- Question 329: spans PDF Page 181 and Page 182.
- Question 338: spans PDF Page 183 and Page 184.
- Question 341: spans PDF Page 184 and Page 185.
- Question 342: spans PDF Page 185 and Page 186.
- Question 343: spans PDF Page 187, 188, 189, 190, and 191 (detailed prayer steps).
- Question 347: spans PDF Page 191 and Page 192.
- Question 355: spans PDF Page 193 and Page 194.
- Question 356: spans PDF Page 194, 195, 196, and 197 (post-prayer supplications).
- Question 357: spans PDF Page 197 and Page 198.
- Question 358: spans PDF Page 198, 199, and 200.
- Question 360: spans PDF Page 201 and Page 202.
- Question 366: spans PDF Page 203 and Page 204.
- Question 370: spans PDF Page 204 and Page 205.
- Question 377: spans PDF Page 206 and Page 207.
- Question 386: spans PDF Page 208 and Page 209.
- Question 389: spans PDF Page 209 and Page 210.
- Question 392: spans PDF Page 211 and Page 212.
- Question 398: spans PDF Page 215 and Page 216.
- Question 406: spans PDF Page 217 and Page 218.
- Question 410: spans PDF Page 219 and Page 220.
- Question 413: spans PDF Page 220 and Page 221.
- Question 417: spans PDF Page 221 and Page 222.
- Question 423: spans PDF Page 223 and Page 224.
- Question 428: spans PDF Page 225 and Page 226.
- Question 431: spans PDF Page 227 and Page 228.
- Question 433: spans PDF Page 229 and Page 230.
- Question 437: spans PDF Page 231 and Page 232.
- Question 442: spans PDF Page 232 and Page 233.
- Question 449: spans PDF Page 234 and Page 235.
- Question 460: spans PDF Page 238 and Page 239.
- Question 464: spans PDF Page 240 and Page 241.
- Question 474: spans PDF Page 242 and Page 243.
- Question 475: spans PDF Page 243 and Page 244.
- Question 483: spans PDF Page 245 and Page 246.
- Question 485: spans PDF Page 246 and Page 247.
- Question 489: spans PDF Page 247 and Page 248.
- Question 493: spans PDF Page 248 and Page 249.
- Question 498: spans PDF Page 250 and Page 251.
- Question 503: spans PDF Page 251 and Page 252.
- Question 510: spans PDF Page 254 and Page 255.
- Question 511: spans PDF Page 255 and Page 256.
- Question 515: spans PDF Page 257, 258, and 259.
- Question 523: spans PDF Page 260 and Page 261.
- Question 530: spans PDF Page 261 and Page 262.
- Question 534: spans PDF Page 262 and Page 263.
- Question 538: spans PDF Page 263 and Page 264.
- Question 546: spans PDF Page 265 and Page 266.
- Question 552: spans PDF Page 266 and Page 267.
- Question 566: spans PDF Page 269 and Page 270.
- Question 572: spans PDF Page 270 and Page 271.
- Question 576: spans PDF Page 271 and Page 272.
- Question 607: spans PDF Page 276 and Page 277.
- Question 612: spans PDF Page 278 and Page 279.
- Question 617: spans PDF Page 279 and Page 280.
- Question 619: spans PDF Page 280 and Page 281.
- Question 621: spans PDF Page 282 and Page 283.
- Question 622: spans PDF Page 283 and Page 284.
- Question 624: spans PDF Page 284 and Page 285.
- Question 625: spans PDF Page 286, 287, and 288.
- Question 627: spans PDF Page 289, 290, and 291.
- Question 631: spans PDF Page 292 and Page 293.
- Question 634: spans PDF Page 293 and Page 294.
- Question 641: spans PDF Page 295, 296, and 297.
- Question 647: spans PDF Page 297 and Page 298.

---

## 8. Detailed Section & Question Mapping to Recommended Files

| Section / Folder | File Name | Content Scope | Questions Included | PDF Page Range | Book Page Range |
|---|---|---|---|---|---|
| **00-muqeddimu** | `01-heqqide.mdx` | About book, CIP, Dedication, Edition statement | N/A | Pages 1–4 | Pages 1–4 |
| **00-muqeddimu** | `02-aptor.mdx` | Author Biography (ئاپتور ھەققىدە) | N/A | Pages 5–8 | Pages 5–8 |
| **00-muqeddimu** | `03-kirish-soz.mdx` | Foreword / Introduction (كىرىش سۆز) | N/A | Pages 9–11 | Pages 9–11 |
| **00-muqeddimu** | `04-munderije.mdx` | Complete Table of Contents (مۇندەرىجە) | N/A | Pages 13–29 | Pages 12–28 |
| **01-etiqad** | `01-din-heqqide.mdx` | Intro to religion, intellect, universal faith | Questions 1–20 | Pages 33–40 | Pages 30–37 |
| **01-etiqad** | `02-iman-allah.mdx` | Faith pillars, Kalima Tayyiba, Nullifiers of faith, Believing in Allah | Questions 21–48 | Pages 41–54 | Pages 38–51 |
| **01-etiqad** | `03-99-isim.mdx` | The 99 Names of Allah Table & Divine Attributes | Questions 49–62 + 99 Names Table | Pages 55–73 | Pages 52–70 |
| **01-etiqad** | `04-perishtiler-jinlar.mdx` | Spiritual worlds, Angels, Jinn, Devils, Iblis | Questions 63–82 | Pages 74–79 | Pages 71–76 |
| **01-etiqad** | `05-kitablar-quran.mdx` | Heavenly books, Wahi, Qur'an miracles & structure | Questions 83–96 | Pages 80–85 | Pages 77–82 |
| **01-etiqad** | `06-peyghamberler.mdx` | Prophets, 25 named prophets, Ulul Azm, Muhammad ﷺ, Durood | Questions 97–115 | Pages 86–91 | Pages 83–88 |
| **01-etiqad** | `07-qada-qeder.mdx` | Predestination, Human free will, Means, Tawakkul, Lawh Mahfuz | Questions 116–134 | Pages 92–101 | Pages 89–98 |
| **01-etiqad** | `08-qiyamet-axiret.mdx` | Doomsday signs, Barzakh, Grave, Resurrection, Hashr, Mizan, Sirat, Heaven & Hell | Questions 135–163 | Pages 102–114 | Pages 99–111 |
| **02-ibadet** | `01-ibadet-asasi.mdx` | Worship overview, Acceptance, Ihsan, Ikhlas, Discernment/puberty | Questions 164–183 | Pages 117–125 | Pages 113–121 |
| **02-ibadet** | `02-sheriy-istilahlar.mdx` | Shar'i terms: Farz, Wajib, Sunnah, Haram, Makruh, Mubah | Questions 184–204 | Pages 126–131 | Pages 122–127 |
| **02-ibadet** | `03-taharet-pakizliq.mdx` | Purity, Water types, Najasat, Cleaning, Istinja, Istibra | Questions 205–223 | Pages 132–135 | Pages 128–131 |
| **02-ibadet** | `04-ayallar-ehkami.mdx` | Restroom manners, Hayd, Nifas, Istihadah, Special women's rulings | Questions 224–257 | Pages 136–151 | Pages 132–147 |
| **02-ibadet** | `05-ghusl-teyemmum.mdx` | Ghusl requirements & method, Tayammum rules & steps | Questions 258–274 | Pages 152–157 | Pages 148–153 |
| **02-ibadet** | `06-namaz-shertliri.mdx` | Prayer importance, 5 prayer times, Prohibited times, Adhan, Iqamah, Awrah, Qiblah, Rakat counts | Questions 275–332 | Pages 158–182 | Pages 154–178 |
| **02-ibadet** | `07-namaz-terkibi.mdx` | Farz, Wajib, Sunnah of prayer, Step-by-step 5 prayers + Witr, Du'as, Post-prayer Azkar, Makruhs, Nullifiers | Questions 333–358 | Pages 183–200 | Pages 179–196 |
| **02-ibadet** | `08-namaz-mesililiri.mdx` | Delaying/stopping prayer, Doubts, Sajdah Sahw, Sutrah, Sajdah Tilawah (14 verses), Qada, Jam' | Questions 359–394 | Pages 201–214 | Pages 197–210 |
| **02-ibadet** | `09-jamaet-namizi.mdx` | Congregational prayer, Women in congregation, Mosque manners, Imamate criteria, Rows | Questions 395–418 | Pages 215–222 | Pages 211–218 |
| **02-ibadet** | `10-jume-namizi.mdx` | Friday prayer, Conditions, Khutbah rules, Sunnahs, Prohibitions | Questions 419–428 | Pages 223–226 | Pages 219–222 |
| **02-ibadet** | `11-yoluchi-namizi.mdx` | Traveler's prayer (Qasr), Distance, 15-day rule | Questions 429–433 | Pages 227–230 | Pages 223–226 |
| **02-ibadet** | `12-heyt-namazliri.mdx` | Eid al-Fitr & Eid al-Adha prayers, Takbirs, Takbir Tashriq period | Questions 434–442 | Pages 231–233 | Pages 227–229 |
| **02-ibadet** | `13-terawih-bashqa.mdx` | Tarawih, Sick prayer, Gesture prayer, Istisqa, Eclipse, Fear, Nafl: Tahiyyah, Duha, Tahajjud, Tawaf, Tawbah, Istikharah, Hajat | Questions 443–477 | Pages 234–244 | Pages 230–240 |
| **02-ibadet** | `14-jinaza-qebre.mdx` | Janaza prayer, Talqin, Shrouding (Kafan), Burial, Graves, Martyrs | Questions 478–506 | Pages 245–252 | Pages 241–248 |
| **02-ibadet** | `15-zakat-ehkami.mdx` | Zakat: obligation, philosophy, Nisab, Asset classes, Recipients, Non-recipients, Debt, Bank interest | Questions 507–553 | Pages 254–267 | Pages 250–263 |
| **02-ibadet** | `16-roza-ramizan.mdx` | Ramadan fasting, Nullifiers, Qada vs Kaffarah, Exemptions, Fidyah, Sadaqat al-Fitr, I'tikaf, Day rulings | Questions 554–607 | Pages 268–277 | Pages 264–273 |
| **02-ibadet** | `17-hejj-omre.mdx` | Hajj & Umrah: Farz, Wajib, Sunnah, Ihram prohibitions, Chronology, Tawaf, Sa'y, Women's rules | Questions 608–627 | Pages 278–291 | Pages 274–287 |
| **02-ibadet** | `18-qurbanliq-sawab-gunah.mdx` | Qurbani types, Animal defects, Meat distribution, Thawab & Tawhid, Major sins list (closing Q647) | Questions 628–647 | Pages 292–298 | Pages 288–294 |

---

## 9. Features Discovered & Edge Cases

### 9.1 Features Discovered Table

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | Typography | Legacy `\u066e` Glyph | Medial/initial Uyghur vowel `ى` encoded as dotless beh | Raw PDF text stream | Normalized `\u0649` (`ى`) | If unmapped, broken rendering and broken search | PDF Pages 1–298 |
| 2 | Typography | Legacy `\u067b` Glyph | Uyghur vowel `ې` encoded as beeh with 2 vertical dots | Raw PDF text stream | Normalized `\u06d0` (`ې`) | If unmapped, unrecognizable dialect/foreign glyph | PDF Pages 1–298 |
| 3 | Typography | Farsi Yeh `\u06cc` | Arabic Letter Farsi Yeh used in isolated/final positions | Raw PDF text stream | Normalized `\u064a` (`ي`) | Breaks exact term search | PDF Pages 1–298 |
| 4 | Typography | Interior Tatweels | Extended justification using Kashidas (`\u0640`) within words | Word internal `\u0640` | Stripped `\u0640` | Search queries fail to match hyphenated/stretched words | PDF Pages 1–298 |
| 5 | Typography | Broken Allah Ligature | Font mapping representing `الله` as `ا:` or `ا:Eُ` or `اÄ` | Corrupted ligature string | Standardized `الله` | Text looks corrupted with colons/letters | PDF Pages 41, 56, 173, 186 |
| 6 | Structure | 99 Names Table | Standalone 3-column table between Q48 and Q49 | PDF Pages 56–69 (Book pp. 53–66) | Markdown table (Arabic Name, Pronunciation, Meaning) | Must not be confused with a question/answer block | PDF Pages 56–69 |
| 7 | Structure | Multi-page Questions | Long questions and multi-step answers spanning page breaks | Page-split question text | Single consolidated Question entity | Premature truncation if split on page footer | PDF Pages 44, 83, 146, 187, etc. |
| 8 | Structure | Footnotes and References | Scriptural references and biographical essays at page bottoms | Bracketed numbers `(1)`, `1( )` | Markdown footnote markers `[^id]` and footnotes | Footnote text mixing with answer body if not parsed | PDF Pages 34, 40, 146, 161, 178 |
| 9 | Structure | Adhan and Du'a Transliterations | Arabic liturgical texts followed by phonetic Uyghur and translation | Trilingual blocks (Arabic, Phonetic, Uyghur) | Structured markdown blockquote with clear labels | Corrupted reading if Arabic and Uyghur transliteration merge | PDF Pages 173, 187–190, 193–196, 243, 246 |
| 10 | Structure | Sajdah Tilawah Surah List | Exact list of 14 Qur'anic chapters requiring recitation prostration | PDF Page 207 (Q381) | Markdown numbered list of 14 Surahs and Ayahs | Missing verses if unparsed | PDF Page 207 |
| 11 | Continuity | Complete Sequence (1–647) | All 647 questions are strictly sequential | 1 to 647 integers | 647 discrete Question items | No gaps or duplicate numbering detected | PDF Pages 39–298 |

### 9.2 Edge Cases Table

| # | Feature | Input | Observed Behavior | Handling Recommendation |
|---|---------|-------|-------------------|--------------------------|
| 1 | Question Delimiter | `.1 سوئال:` vs `164. سوئال:` | Period appears either before or after digit due to BiDi | Use regex `(?:\.|\b)(\d{1,3})\s*(?:\.|\b)\s*سوئال:` |
| 2 | Sub-points in Answers | `(1)`, `(2)`, `(3)` or `1`, `2`, `3` | Digits in answer lists could trigger false question splits | Ensure regex strictly requires `سوئال:` keyword |
| 3 | Long Footnote on Socks | PDF Page 146 (Book p. 142) | Footnote takes up 70% of the physical page space | Extract footnote section separately based on bottom rule separator |
| 4 | Biographical Essay Footnotes | PDF Page 161 (Ibn Taymiyyah), Page 178 (al-Qaradawi) | Lengthy multiline biographies within footnote 1 | Maintain as Markdown footnote definition or separate callout note |
| 5 | Quranic Bracket Extraction | `﴿ ... ﴾` | Verses contain Uthmani diacritics and broken font ligatures | Strip proprietary font junk characters; maintain verse quotes |
| 6 | 99 Names Interruption | Between Q48 and Q49 | Spans 14 pages without any question headers | Dedicated parser for the table, linking smoothly to Q49 |
| 7 | Section End Marker | PDF Page 299 (Division 3 title) | Signals end of Volume 1; no questions follow | Stop question parsing at page 298 |
