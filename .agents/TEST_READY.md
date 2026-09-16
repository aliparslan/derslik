# TEST_READY: Din ve Hayat (2000 Sualliq) E2E Test Suite

## Overview
A comprehensive, opaque-box E2E test harness has been built in `tests/e2e_2000.py` to independently verify the conversion of Part 1 of "دىن ۋە ھايات (2000 سوئالغا جاۋاب)" from PDF into the Astro/Starlight web documentation under `src/content/docs/2000/`.

The test suite requires zero external Python dependencies (pure Python 3 standard library: `argparse`, `json`, `os`, `re`, `subprocess`, `sys`, `pathlib`) and tests against user requirements and acceptance criteria across 4 progressive tiers.

---

## Test Runner Commands

### 1. Run Complete Test Suite
```bash
python3 tests/e2e_2000.py
```
Runs all 4 tiers sequentially. Exits with code `0` on 100% pass, code `1` if any test fails.

### 2. Run Fast Mode (Skip Astro Build)
```bash
python3 tests/e2e_2000.py --skip-build
```
Executes all static and integrity checks (Tiers 1, 2, 3, and Tier 4 search index check) without executing `pnpm build`. Ideal during local content iteration.

### 3. Run Specific Tier
```bash
python3 tests/e2e_2000.py --tier 1   # Tier 1: Feature Coverage (Questions & Structure)
python3 tests/e2e_2000.py --tier 2   # Tier 2: Boundary & Unicode Integrity
python3 tests/e2e_2000.py --tier 3   # Tier 3: 99 Names Table & Starlight Config
python3 tests/e2e_2000.py --tier 4   # Tier 4: Astro Build & Pagefind Search Index
```

### 4. Diagnostic & Machine-Readable Output
```bash
# Verbose mode with full failure diagnostics & sample excerpts
python3 tests/e2e_2000.py -v

# JSON output for CI / Orchestrator integration
python3 tests/e2e_2000.py --json
```

---

## Tier Summary & Verification Scope

### Tier 1 - Feature Coverage
| Test Case | Method | Assertion / Criteria |
|-----------|--------|----------------------|
| **Question Count** | `test_question_count` | Exactly **647** unique question cards extracted and formatted across `src/content/docs/2000/`. Duplicate card count must be 0. |
| **Question Number Set** | `test_question_number_set` | Extracted question numbers strictly match `set(range(1, 648))` with zero missing numbers and zero out-of-range numbers. |
| **Question Structure** | `test_question_structure` | Every question card contains `.qa-question` with non-empty text, `.qa-answer` with non-empty text, and `.qa-number` span. |
| **Section 00 Pages** | `test_section_00_pages` | All 4 required pages exist in `00-muqeddimu/`: `01-kitab-heqqide.mdx`, `02-aptur-heqqide.mdx`, `03-kirish-soz.mdx`, `04-munderije.mdx` with non-empty content and valid YAML frontmatter. |
| **Section 01 Pages & Boundaries** | `test_section_01_pages_and_boundaries` | `01-etiqad/` contains exactly 8 pages and covers questions Q1 through Q163 continuously. |
| **Section 02 Pages & Boundaries** | `test_section_02_pages_and_boundaries` | `02-ibadet/` contains exactly 14 pages and covers questions Q164 through Q647 continuously. |

### Tier 2 - Boundary & Integrity Tests
| Test Case | Method | Assertion / Criteria |
|-----------|--------|----------------------|
| **Zero Dotless Beh** | `test_zero_dotless_beh` | 0 occurrences of `\u066e` (dotless beh `ٮ`) across all files under `src/content/docs/2000/`. |
| **Zero Beeh (2 Dots Below)** | `test_zero_beeh_two_dots_below` | 0 occurrences of `\u067b` (beeh with 2 vertical dots `ٻ`) across all files under `src/content/docs/2000/`. |
| **Zero Interior Tatweels** | `test_zero_interior_tatweels` | 0 occurrences of interior kashida/tatweel `\u0640` inside Uyghur words (`[\u0621-\u064a\u0671-\u06d5]\u0640+[\u0621-\u064a\u0671-\u06d5]`). |
| **Boundary Questions Integrity** | `test_boundary_questions_integrity` | Verbatim text and non-empty answers for landmark questions: Q1 (creation of mankind), Q48 (99 names hadith), Q49 (names vs attributes distinction), Q163 (eternity of Paradise and Hell), Q164 (essence of worship), Q647 (classification of sins). |

### Tier 3 - 99 Names of Allah Table & Cross-Feature Verification
| Test Case | Method | Assertion / Criteria |
|-----------|--------|----------------------|
| **99 Names Table** | `test_99_names_table` | Table present in `01-etiqad/03-allahning-isimliri.mdx`, exactly 99 data rows, all 3 columns (Arabic vocalized with tashkeel, Uyghur pronunciation, Uyghur meaning) non-empty. Supports both Markdown and HTML table syntax. |
| **Option B Card CSS** | `test_option_b_css_presence` | `src/styles/custom.css` contains rules for `.qa-card`, `.qa-question`, `.qa-answer`, and `.qa-number`. |
| **Sidebar Navigation** | `test_sidebar_navigation_config` | `astro.config.mjs` configures sidebar navigation group for `2000 سوئال-جاۋاب` pointing to `/2000/` and its divisions. |

### Tier 4 - Build & Search Validation
| Test Case | Method | Assertion / Criteria |
|-----------|--------|----------------------|
| **Astro Build** | `test_astro_build` | `pnpm build` executes successfully with exit code 0. |
| **Pagefind Search Index** | `test_pagefind_search_index` | `dist/pagefind/` exists and contains generated search index assets (`pagefind.js`, wasm, entries). |

---

## Exit Codes & CI Integration
- **Code 0**: All executed test cases passed.
- **Code 1**: One or more test cases failed. Detailed failure logs are printed to stderr/stdout with offending filenames, line numbers, and sample snippets.
