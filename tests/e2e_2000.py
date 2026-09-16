#!/usr/bin/env python3
"""
tests/e2e_2000.py
Comprehensive, opaque-box E2E test suite for "Din ve Hayat (2000 Sualliq)" Part 1.

Tiers:
  Tier 1 - Feature Coverage:
    - Exactly 647 questions extracted and formatted.
    - Question number set strictly matches set(range(1, 648)).
    - Well-formed question/answer structure for all cards.
    - Section 00 (00-muqeddimu) has all 4 required pages with non-empty content.
    - Section 01 (01-etiqad) has 8 pages covering Q1–163.
    - Section 02 (02-ibadet) has 14 pages covering Q164–647.
  Tier 2 - Boundary & Integrity Tests:
    - Zero occurrences of legacy glyph \\u066e (dotless beh) across all docs/2000 files.
    - Zero occurrences of legacy glyph \\u067b (beeh with 2 dots below).
    - Zero occurrences of interior tatweels/kashidas (\\u0640) inside Uyghur words.
    - Landmark boundary questions (Q1, Q48, Q49, Q163, Q164, Q647) verbatim integrity.
  Tier 3 - 99 Names of Allah Table & Cross-Feature:
    - 99 Names table present in 01-etiqad/03-allahning-isimliri.mdx.
    - Exactly 99 table rows.
    - All 3 columns (Arabic, Uyghur Pronunciation, Meaning) populated.
    - Option B CSS present in src/styles/custom.css (.qa-card, .qa-question, .qa-answer, .qa-number).
    - Navigation config in astro.config.mjs contains sidebar group for 2000 questions.
  Tier 4 - Build & Search Validation:
    - Full site build via `pnpm build`.
    - Pagefind search index presence in dist/pagefind/.

Usage:
  python3 tests/e2e_2000.py                  # Run all tiers
  python3 tests/e2e_2000.py --tier 1         # Run Tier 1 only
  python3 tests/e2e_2000.py --skip-build     # Run all tiers skipping pnpm build
  python3 tests/e2e_2000.py --json           # Output machine-readable JSON
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


# ANSI Color formatting
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


def colorize(text: str, color: str, disable: bool = False) -> str:
    if disable or not sys.stdout.isatty():
        return text
    return f"{color}{text}{Colors.RESET}"


class TestCaseResult:
    def __init__(self, name: str, passed: bool, message: str = "", details: Optional[List[str]] = None):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details or []

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "passed": self.passed,
            "message": self.message,
            "details": self.details,
        }


class QuestionCard:
    def __init__(
        self,
        number: int,
        file_path: Path,
        raw_html: str,
        question_text: str,
        answer_text: str,
        has_qa_card: bool,
        has_qa_question: bool,
        has_qa_answer: bool,
        has_qa_number: bool,
    ):
        self.number = number
        self.file_path = file_path
        self.raw_html = raw_html
        self.question_text = question_text
        self.answer_text = answer_text
        self.has_qa_card = has_qa_card
        self.has_qa_question = has_qa_question
        self.has_qa_answer = has_qa_answer
        self.has_qa_number = has_qa_number


class DinVeHayatTester:
    def __init__(self, project_root: Path, skip_build: bool = False, verbose: bool = False, no_color: bool = False):
        self.project_root = project_root.resolve()
        self.docs_root = self.project_root / "src" / "content" / "docs" / "2000"
        self.skip_build = skip_build
        self.verbose = verbose
        self.no_color = no_color

        self.questions: Dict[int, List[QuestionCard]] = {}
        self.all_cards: List[QuestionCard] = []
        self._parsed = False

    def _clean_html_text(self, text: str) -> str:
        """Strip HTML tags and normalize whitespace."""
        clean = re.sub(r"<[^>]+>", " ", text)
        clean = re.sub(r"\s+", " ", clean).strip()
        return clean

    def parse_all_questions(self) -> None:
        """Scan all MDX/MD files under docs_root and extract question cards."""
        if self._parsed:
            return

        if not self.docs_root.exists():
            self._parsed = True
            return

        mdx_files = sorted(list(self.docs_root.glob("**/*.mdx")) + list(self.docs_root.glob("**/*.md")))

        # Pattern to extract qa-card blocks
        card_pattern = re.compile(
            r'(<div\s+[^>]*class=["\'][^"\']*qa-card[^"\']*["\'][^>]*>[\s\S]*?)(?=<div\s+[^>]*class=["\'][^"\']*qa-card|\Z)',
            re.IGNORECASE,
        )

        # Fallback question ID / number patterns
        id_pattern = re.compile(r'id=["\']q?(\d+)["\']', re.IGNORECASE)
        num_span_pattern = re.compile(r'<span\s+[^>]*class=["\'][^"\']*qa-number[^"\']*["\'][^>]*>\s*(\d+)\s*</span>', re.IGNORECASE)
        heading_num_pattern = re.compile(r'###\s+(\d+)\.')

        # Question & Answer block patterns
        question_block_pattern = re.compile(
            r'<div\s+[^>]*class=["\'][^"\']*qa-question[^"\']*["\'][^>]*>([\s\S]*?)</div>',
            re.IGNORECASE,
        )
        answer_block_pattern = re.compile(
            r'<div\s+[^>]*class=["\'][^"\']*qa-answer[^"\']*["\'][^>]*>([\s\S]*?)</div>',
            re.IGNORECASE,
        )

        for file_path in mdx_files:
            try:
                content = file_path.read_text(encoding="utf-8")
            except Exception:
                continue

            matches = list(card_pattern.finditer(content))

            for match in matches:
                block = match.group(1)

                # Find question number
                q_num = None
                id_m = id_pattern.search(block)
                if id_m:
                    try:
                        q_num = int(id_m.group(1))
                    except ValueError:
                        pass

                if q_num is None:
                    span_m = num_span_pattern.search(block)
                    if span_m:
                        try:
                            q_num = int(span_m.group(1))
                        except ValueError:
                            pass

                if q_num is None:
                    head_m = heading_num_pattern.search(block)
                    if head_m:
                        try:
                            q_num = int(head_m.group(1))
                        except ValueError:
                            pass

                if q_num is None:
                    continue

                # Question and answer extraction
                q_match = question_block_pattern.search(block)
                raw_q = q_match.group(1) if q_match else ""
                clean_q = self._clean_html_text(raw_q)

                a_match = answer_block_pattern.search(block)
                raw_a = a_match.group(1) if a_match else ""
                clean_a = self._clean_html_text(raw_a)

                card = QuestionCard(
                    number=q_num,
                    file_path=file_path,
                    raw_html=block,
                    question_text=clean_q,
                    answer_text=clean_a,
                    has_qa_card=True,
                    has_qa_question=bool(q_match),
                    has_qa_answer=bool(a_match),
                    has_qa_number=bool(num_span_pattern.search(block)),
                )

                if q_num not in self.questions:
                    self.questions[q_num] = []
                self.questions[q_num].append(card)
                self.all_cards.append(card)

        self._parsed = True

    # =========================================================================
    # TIER 1 - Feature Coverage
    # =========================================================================

    def test_question_count(self) -> TestCaseResult:
        """Verify exactly 2000 questions are extracted across docs/2000."""
        self.parse_all_questions()
        total_unique = len(self.questions)
        total_cards = len(self.all_cards)

        details = []
        if total_unique != 2000:
            details.append(f"Expected 2000 unique questions, found {total_unique} (total card instances: {total_cards})")
        if total_cards > total_unique:
            duplicates = [q for q, cards in self.questions.items() if len(cards) > 1]
            details.append(f"Found {len(duplicates)} duplicate question numbers: {duplicates[:10]}...")

        passed = total_unique == 2000 and total_cards == 2000
        msg = f"Extracted {total_unique}/2000 unique questions ({total_cards} card instances found)"
        return TestCaseResult("Question Count (Exactly 2000)", passed, msg, details)

    def test_question_number_set(self) -> TestCaseResult:
        """Verify question numbers strictly match set(range(1, 2001))."""
        self.parse_all_questions()
        expected_set = set(range(1, 2001))
        actual_set = set(self.questions.keys())

        missing = expected_set - actual_set
        unexpected = actual_set - expected_set

        details = []
        if missing:
            details.append(f"Missing {len(missing)} question numbers: {sorted(list(missing))[:25]}...")
        if unexpected:
            details.append(f"Unexpected {len(unexpected)} question numbers: {sorted(list(unexpected))[:25]}...")

        passed = (len(missing) == 0) and (len(unexpected) == 0)
        msg = f"Set match: {len(actual_set & expected_set)}/2000 present, {len(missing)} missing, {len(unexpected)} out-of-range"
        return TestCaseResult("Question Number Set Integrity (1..2000)", passed, msg, details)

    def test_question_structure(self) -> TestCaseResult:
        """Verify every question card has non-empty question & answer text and proper HTML."""
        self.parse_all_questions()
        malformed: List[str] = []
        empty_questions: List[int] = []
        empty_answers: List[int] = []
        missing_qa_number: List[int] = []

        for q_num, cards in self.questions.items():
            for card in cards:
                if not card.has_qa_question or not card.question_text:
                    empty_questions.append(q_num)
                    malformed.append(f"Q{q_num} in {card.file_path.name}: Missing question text or .qa-question div")

                if not card.has_qa_answer or not card.answer_text:
                    empty_answers.append(q_num)
                    malformed.append(f"Q{q_num} in {card.file_path.name}: Missing answer text or .qa-answer div")

                if not card.has_qa_number:
                    missing_qa_number.append(q_num)
                    malformed.append(f"Q{q_num} in {card.file_path.name}: Missing .qa-number span")

        passed = len(malformed) == 0 and len(self.questions) > 0
        msg = f"Structure checked across {len(self.all_cards)} cards. Malformations: {len(malformed)}"
        return TestCaseResult("Question Card Structural Integrity", passed, msg, malformed[:20])

    def test_section_00_pages(self) -> TestCaseResult:
        """Verify Section 00 (00-muqeddimu) has all 4 required pages with content."""
        sec00_dir = self.docs_root / "00-muqeddimu"
        expected_pages = [
            "01-kitab-heqqide.mdx",
            "02-aptur-heqqide.mdx",
            "03-kirish-soz.mdx",
            "04-munderije.mdx",
        ]

        details = []
        if not sec00_dir.exists():
            details.append(f"Directory {sec00_dir} does not exist.")
            return TestCaseResult("Section 00 (Muqeddimu) 4 Pages Existence", False, "Directory missing", details)

        missing_pages = []
        empty_pages = []

        for page_name in expected_pages:
            page_path = sec00_dir / page_name
            if not page_path.exists():
                missing_pages.append(page_name)
            else:
                content = page_path.read_text(encoding="utf-8").strip()
                if len(content) < 50 or "title:" not in content:
                    empty_pages.append(page_name)

        if missing_pages:
            details.append(f"Missing pages: {missing_pages}")
        if empty_pages:
            details.append(f"Pages missing frontmatter/content: {empty_pages}")

        passed = len(missing_pages) == 0 and len(empty_pages) == 0
        msg = f"{len(expected_pages) - len(missing_pages)}/{len(expected_pages)} Section 00 pages verified"
        return TestCaseResult("Section 00 (Muqeddimu) 4 Pages Existence", passed, msg, details)

    def test_section_01_pages_and_boundaries(self) -> TestCaseResult:
        """Verify Section 01 (01-etiqad) has 8 pages and covers Q1-163."""
        sec01_dir = self.docs_root / "01-etiqad"
        details = []

        if not sec01_dir.exists():
            details.append(f"Directory {sec01_dir} does not exist.")
            return TestCaseResult("Section 01 (Etiqad) 8 Pages & Q1-163 Boundaries", False, "Directory missing", details)

        mdx_files = sorted(list(sec01_dir.glob("*.mdx")) + list(sec01_dir.glob("*.md")))
        page_count = len(mdx_files)

        if page_count != 8:
            details.append(f"Expected exactly 8 pages in 01-etiqad, found {page_count}: {[f.name for f in mdx_files]}")

        # Scan question numbers within 01-etiqad
        sec01_questions = set()
        for f in mdx_files:
            try:
                content = f.read_text(encoding="utf-8")
                matches = re.findall(r'id=["\']q?(\d+)["\']|<span\s+[^>]*class=["\'][^"\']*qa-number[^"\']*["\'][^>]*>\s*(\d+)\s*</span>', content)
                for m in matches:
                    num_str = m[0] or m[1]
                    if num_str:
                        sec01_questions.add(int(num_str))
            except Exception:
                pass

        expected_range = set(range(1, 164))
        missing_in_01 = expected_range - sec01_questions
        unexpected_in_01 = sec01_questions - expected_range

        if missing_in_01:
            details.append(f"Questions missing from Section 01 (expected Q1-163): {sorted(list(missing_in_01))[:15]}...")
        if unexpected_in_01:
            details.append(f"Questions out of Section 01 range: {sorted(list(unexpected_in_01))[:15]}...")

        passed = (page_count == 8) and (len(missing_in_01) == 0) and (len(unexpected_in_01) == 0)
        msg = f"Section 01: {page_count}/8 pages, {len(sec01_questions)}/163 questions covered"
        return TestCaseResult("Section 01 (Etiqad) 8 Pages & Q1-163 Boundaries", passed, msg, details)

    def test_section_02_pages_and_boundaries(self) -> TestCaseResult:
        """Verify Section 02 (02-ibadet) has 14 pages and covers Q164-647."""
        sec02_dir = self.docs_root / "02-ibadet"
        details = []

        if not sec02_dir.exists():
            details.append(f"Directory {sec02_dir} does not exist.")
            return TestCaseResult("Section 02 (Ibadet) 14 Pages & Q164-647 Boundaries", False, "Directory missing", details)

        mdx_files = sorted(list(sec02_dir.glob("*.mdx")) + list(sec02_dir.glob("*.md")))
        page_count = len(mdx_files)

        if page_count != 14:
            details.append(f"Expected exactly 14 pages in 02-ibadet, found {page_count}: {[f.name for f in mdx_files]}")

        # Scan question numbers within 02-ibadet
        sec02_questions = set()
        for f in mdx_files:
            try:
                content = f.read_text(encoding="utf-8")
                matches = re.findall(r'id=["\']q?(\d+)["\']|<span\s+[^>]*class=["\'][^"\']*qa-number[^"\']*["\'][^>]*>\s*(\d+)\s*</span>', content)
                for m in matches:
                    num_str = m[0] or m[1]
                    if num_str:
                        sec02_questions.add(int(num_str))
            except Exception:
                pass

        expected_range = set(range(164, 648))
        missing_in_02 = expected_range - sec02_questions
        unexpected_in_02 = sec02_questions - expected_range

        if missing_in_02:
            details.append(f"Questions missing from Section 02 (expected Q164-647): {sorted(list(missing_in_02))[:15]}...")
        if unexpected_in_02:
            details.append(f"Questions out of Section 02 range: {sorted(list(unexpected_in_02))[:15]}...")

        passed = (page_count == 14) and (len(missing_in_02) == 0) and (len(unexpected_in_02) == 0)
        msg = f"Section 02: {page_count}/14 pages, {len(sec02_questions)}/484 questions covered"
        return TestCaseResult("Section 02 (Ibadet) 14 Pages & Q164-647 Boundaries", passed, msg, details)

    def test_section_03_pages_and_boundaries(self) -> TestCaseResult:
        """Verify Section 03 (03-exlaq) has 10 pages and covers Q648-967."""
        sec03_dir = self.docs_root / "03-exlaq"
        details = []

        if not sec03_dir.exists():
            details.append(f"Directory {sec03_dir} does not exist.")
            return TestCaseResult("Section 03 (Exlaq) 10 Pages & Q648-967 Boundaries", False, "Directory missing", details)

        mdx_files = sorted(list(sec03_dir.glob("*.mdx")) + list(sec03_dir.glob("*.md")))
        page_count = len(mdx_files)

        if page_count != 10:
            details.append(f"Expected exactly 10 pages in 03-exlaq, found {page_count}: {[f.name for f in mdx_files]}")

        sec03_questions = set()
        for f in mdx_files:
            try:
                content = f.read_text(encoding="utf-8")
                matches = re.findall(r'id=["\']q?(\d+)["\']|<span\s+[^>]*class=["\'][^"\']*qa-number[^"\']*["\'][^>]*>\s*(\d+)\s*</span>', content)
                for m in matches:
                    num_str = m[0] or m[1]
                    if num_str:
                        sec03_questions.add(int(num_str))
            except Exception:
                pass

        expected_range = set(range(648, 968))
        missing_in_03 = expected_range - sec03_questions
        unexpected_in_03 = sec03_questions - expected_range

        if missing_in_03:
            details.append(f"Questions missing from Section 03 (expected Q648-967): {sorted(list(missing_in_03))[:15]}...")
        if unexpected_in_03:
            details.append(f"Questions out of Section 03 range: {sorted(list(unexpected_in_03))[:15]}...")

        passed = (page_count == 10) and (len(missing_in_03) == 0) and (len(unexpected_in_03) == 0)
        msg = f"Section 03: {page_count}/10 pages, {len(sec03_questions)}/320 questions covered"
        return TestCaseResult("Section 03 (Exlaq) 10 Pages & Q648-967 Boundaries", passed, msg, details)

    def test_section_04_pages_and_boundaries(self) -> TestCaseResult:
        """Verify Section 04 (04-sehiret) has 6 pages and covers Q968-1317."""
        sec04_dir = self.docs_root / "04-sehiret"
        details = []

        if not sec04_dir.exists():
            details.append(f"Directory {sec04_dir} does not exist.")
            return TestCaseResult("Section 04 (Sehiret) 6 Pages & Q968-1317 Boundaries", False, "Directory missing", details)

        mdx_files = sorted(list(sec04_dir.glob("*.mdx")) + list(sec04_dir.glob("*.md")))
        page_count = len(mdx_files)

        if page_count != 6:
            details.append(f"Expected exactly 6 pages in 04-sehiret, found {page_count}: {[f.name for f in mdx_files]}")

        sec04_questions = set()
        for f in mdx_files:
            try:
                content = f.read_text(encoding="utf-8")
                matches = re.findall(r'id=["\']q?(\d+)["\']|<span\s+[^>]*class=["\'][^"\']*qa-number[^"\']*["\'][^>]*>\s*(\d+)\s*</span>', content)
                for m in matches:
                    num_str = m[0] or m[1]
                    if num_str:
                        sec04_questions.add(int(num_str))
            except Exception:
                pass

        expected_range = set(range(968, 1318))
        missing_in_04 = expected_range - sec04_questions
        unexpected_in_04 = sec04_questions - expected_range

        if missing_in_04:
            details.append(f"Questions missing from Section 04 (expected Q968-1317): {sorted(list(missing_in_04))[:15]}...")
        if unexpected_in_04:
            details.append(f"Questions out of Section 04 range: {sorted(list(unexpected_in_04))[:15]}...")

        passed = (page_count == 6) and (len(missing_in_04) == 0) and (len(unexpected_in_04) == 0)
        msg = f"Section 04: {page_count}/6 pages, {len(sec04_questions)}/350 questions covered"
        return TestCaseResult("Section 04 (Sehiret) 6 Pages & Q968-1317 Boundaries", passed, msg, details)

    def _test_section_generic(self, sec_slug: str, expected_pages: int, start_q: int, end_q: int, sec_name: str) -> TestCaseResult:
        sec_dir = self.docs_root / sec_slug
        details = []
        if not sec_dir.exists():
            details.append(f"Directory {sec_dir} does not exist.")
            return TestCaseResult(f"Section {sec_slug[:2]} ({sec_name}) Boundaries", False, "Directory missing", details)

        mdx_files = sorted(list(sec_dir.glob("*.mdx")) + list(sec_dir.glob("*.md")))
        page_count = len(mdx_files)
        if page_count != expected_pages:
            details.append(f"Expected exactly {expected_pages} pages in {sec_slug}, found {page_count}: {[f.name for f in mdx_files]}")

        sec_questions = set()
        for f in mdx_files:
            try:
                content = f.read_text(encoding="utf-8")
                matches = re.findall(r'id=["\']q?(\d+)["\']|<span\s+[^>]*class=["\'][^"\']*qa-number[^"\']*["\'][^>]*>\s*(\d+)\s*</span>', content)
                for m in matches:
                    num_str = m[0] or m[1]
                    if num_str:
                        sec_questions.add(int(num_str))
            except Exception:
                pass

        expected_range = set(range(start_q, end_q + 1))
        missing = expected_range - sec_questions
        unexpected = sec_questions - expected_range
        if missing:
            details.append(f"Questions missing from {sec_slug} (expected Q{start_q}-{end_q}): {sorted(list(missing))[:15]}...")
        if unexpected:
            details.append(f"Questions out of {sec_slug} range: {sorted(list(unexpected))[:15]}...")

        total_q = end_q - start_q + 1
        passed = (page_count == expected_pages) and (len(missing) == 0) and (len(unexpected) == 0)
        msg = f"Section {sec_slug[:2]}: {page_count}/{expected_pages} pages, {len(sec_questions)}/{total_q} questions covered"
        return TestCaseResult(f"Section {sec_slug[:2]} ({sec_name}) {page_count} Pages & Q{start_q}-{end_q} Boundaries", passed, msg, details)

    def test_section_05_pages_and_boundaries(self) -> TestCaseResult:
        return self._test_section_generic("05-haram-cheklengen", 7, 1318, 1555, "Haram")

    def test_section_06_pages_and_boundaries(self) -> TestCaseResult:
        return self._test_section_generic("06-quran-sunnet", 4, 1556, 1680, "Quran-Sunnet")

    def test_section_07_pages_and_boundaries(self) -> TestCaseResult:
        return self._test_section_generic("07-islamiy-ilimler", 4, 1681, 1839, "Ilimler")

    def test_section_08_pages_and_boundaries(self) -> TestCaseResult:
        return self._test_section_generic("08-quran-mojiziliri", 1, 1840, 1845, "Mojiziler")

    def test_section_09_pages_and_boundaries(self) -> TestCaseResult:
        return self._test_section_generic("09-muqeddes-jaylar", 2, 1846, 1894, "Muqeddes-Jaylar")

    def test_section_10_pages_and_boundaries(self) -> TestCaseResult:
        return self._test_section_generic("10-ateizm-allahning-barliqi", 2, 1895, 1938, "Ateizm-Barliq")

    def test_section_11_pages_and_boundaries(self) -> TestCaseResult:
        return self._test_section_generic("11-shek-shubhiler", 1, 1939, 1958, "Shek-Shubhiler")

    def test_section_12_pages_and_boundaries(self) -> TestCaseResult:
        return self._test_section_generic("12-islam-dowliti", 1, 1959, 2000, "Islam-Dowliti")

    # =========================================================================
    # TIER 2 - Boundary & Integrity Tests
    # =========================================================================

    def test_zero_dotless_beh(self) -> TestCaseResult:
        """Verify zero occurrences of \\u066e (dotless beh) across docs/2000."""
        dotless_beh = "\u066e"
        matches = []

        if self.docs_root.exists():
            for f in self.docs_root.glob("**/*"):
                if f.is_file() and f.suffix in (".mdx", ".md", ".json", ".html"):
                    try:
                        text = f.read_text(encoding="utf-8")
                        count = text.count(dotless_beh)
                        if count > 0:
                            matches.append(f"{f.relative_to(self.project_root)}: {count} occurrences")
                    except Exception:
                        pass

        passed = len(matches) == 0
        msg = f"Occurrences of \\u066e: {len(matches)} files affected"
        return TestCaseResult("Zero Legacy Glyph \\u066e (Dotless Beh)", passed, msg, matches[:10])

    def test_zero_beeh_two_dots_below(self) -> TestCaseResult:
        """Verify zero occurrences of \\u067b (beeh with 2 dots below) across docs/2000."""
        beeh_2dots = "\u067b"
        matches = []

        if self.docs_root.exists():
            for f in self.docs_root.glob("**/*"):
                if f.is_file() and f.suffix in (".mdx", ".md", ".json", ".html"):
                    try:
                        text = f.read_text(encoding="utf-8")
                        count = text.count(beeh_2dots)
                        if count > 0:
                            matches.append(f"{f.relative_to(self.project_root)}: {count} occurrences")
                    except Exception:
                        pass

        passed = len(matches) == 0
        msg = f"Occurrences of \\u067b: {len(matches)} files affected"
        return TestCaseResult("Zero Legacy Glyph \\u067b (Beeh with 2 dots below)", passed, msg, matches[:10])

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

    def test_zero_interior_tatweels(self) -> TestCaseResult:
        """Verify zero occurrences of interior tatweel/kashida (\\u0640) in Uyghur words."""
        # Tatweel between Uyghur Arabic-script characters
        tatweel_pattern = re.compile(r"[\u0621-\u064a\u0671-\u06d3\u06d5]\u0640+[\u0621-\u064a\u0671-\u06d3\u06d5]")
        matches = []

        if self.docs_root.exists():
            for f in self.docs_root.glob("**/*"):
                if f.is_file() and f.suffix in (".mdx", ".md"):
                    try:
                        text = f.read_text(encoding="utf-8")
                        found = tatweel_pattern.findall(text)
                        if found:
                            matches.append(f"{f.relative_to(self.project_root)}: {len(found)} interior tatweels found")
                    except Exception:
                        pass

        passed = len(matches) == 0
        msg = f"Interior tatweels found: {len(matches)} files affected"
        return TestCaseResult("Zero Interior Tatweels (\\u0640) in Uyghur Words", passed, msg, matches[:10])

    def test_zero_broken_words(self) -> TestCaseResult:
        """Verify zero occurrences of broken words from Lam-Alef ligature defect across docs/2000."""
        broken_words = ["ئىسلم", "ئۇلر", "دىنلر", "ئلل"]
        matches = []

        if self.docs_root.exists():
            for f in self.docs_root.glob("**/*"):
                if f.is_file() and f.suffix in (".mdx", ".md"):
                    try:
                        text = f.read_text(encoding="utf-8")
                        for bw in broken_words:
                            count = text.count(bw)
                            if count > 0:
                                matches.append(f"{f.relative_to(self.project_root)}: '{bw}' found {count} times")
                    except Exception:
                        pass

        passed = len(matches) == 0
        msg = f"Zero broken words check: {len(matches)} occurrences across MDX files"
        return TestCaseResult("Zero Broken Lam-Alef Words (ئىسلم, ئۇلر, etc.)", passed, msg, matches[:10])

    def test_boundary_questions_integrity(self) -> TestCaseResult:
        """Verify landmark boundary questions (Q1, Q48, Q49, Q163, Q164, Q647, Q648, Q968, Q1317, Q1318, Q1555, Q1556, Q2000) verbatim integrity."""
        self.parse_all_questions()
        details = []

        check_points = [
            (1, "ئىنسانلار نەدىن پەيدا بولغان؟", "ئىنسانلار ئاللاھ تەرىپىدىن يارىتىلغان"),
            (48, "ئاللاھ تائالانىڭ گۈزەل ئىسىم-سۈپەتلىرى قايسىلار؟", "99"),
            (49, "ئىسىملىرى بىلەن سۈپەتلىرى", "پەرق"),
            (163, "جەننەت بىلەن دوزاخ مەڭگۈلۈكمۇ؟", ""),
            (164, "ئىبادەتنىڭ ماھىيىتى نېمە؟", ""),
            (647, "ئىسلام دىنىدا گۇناھ سانالغان ئىشلار قىسقىچە قايسىلار؟", ""),
            (648, "ئەخلاق دېگەن نېمە؟", "روھىدا"),
            (968, "ئىسلام دىنى كېلىشتىن بۇرۇنقى ئەرەب جەمئىيىتى قانداق ئىدى؟", "جەمئىيىتى"),
            (1317, "كاپارەت بېرىش تەرتىبى قانداق بولىدۇ؟", "كاپارەت"),
            (1318, "ھالال دېگەن نېمە؟", "ھالال"),
            (1555, "تەۋبە–ئىستىغفارنىڭ قانداق پايدىسى بار؟", "پايدىسى"),
            (1556, "«قۇرئان »دېگەن سۆزنىڭ مەنىسى نېمە؟", "قۇرئان"),
            (2000, "ئوسمانىيلارنىڭ رولى قانچىلىك دەرىجىدە بولغان؟", "مۇستەملىكىچىلەر"),
        ]

        passed_count = 0
        for q_num, expected_q_kw, expected_a_kw in check_points:
            if q_num not in self.questions or not self.questions[q_num]:
                details.append(f"Q{q_num}: Card completely missing")
                continue

            card = self.questions[q_num][0]

            # Check question text non-empty
            if not card.question_text:
                details.append(f"Q{q_num}: Question text is empty")
                continue

            # Check answer text non-empty
            if not card.answer_text:
                details.append(f"Q{q_num}: Answer text is empty")
                continue

            # Verify question keyword / phrasing
            # Note: We check if expected Uyghur keywords are present (normalized)
            q_norm = card.question_text.replace("\u066e", "\u0649").replace("\u067b", "\u06d0")
            a_norm = card.answer_text.replace("\u066e", "\u0649").replace("\u067b", "\u06d0")

            if expected_q_kw and expected_q_kw not in q_norm:
                # Check for reversed word order bug (e.g. "بولغان؟ پەیدا نەدىن")
                details.append(f"Q{q_num}: Question phrasing mismatch. Expected containing '{expected_q_kw}', found: '{card.question_text[:60]}...'")
                continue

            if expected_a_kw and expected_a_kw not in a_norm:
                details.append(f"Q{q_num}: Answer phrasing mismatch. Expected containing '{expected_a_kw}', found: '{card.answer_text[:60]}...'")
                continue

            passed_count += 1

        passed = (passed_count == len(check_points))
        msg = f"{passed_count}/{len(check_points)} landmark questions passed verbatim integrity check"
        return TestCaseResult("Landmark Boundary Questions Verbatim Integrity", passed, msg, details)

    # =========================================================================
    # TIER 3 - 99 Names of Allah Table & Cross-Feature Verification
    # =========================================================================

    def test_99_names_table(self) -> TestCaseResult:
        """Verify presence, 99 rows, and 3 columns populated in 01-etiqad/03-allahning-isimliri.mdx."""
        table_path = self.docs_root / "01-etiqad" / "03-allahning-isimliri.mdx"
        details = []

        if not table_path.exists():
            details.append(f"File {table_path} does not exist.")
            return TestCaseResult("99 Names of Allah Table Verification", False, "File missing", details)

        content = table_path.read_text(encoding="utf-8")

        # Parse markdown table rows
        # Table rows start with |
        lines = [line.strip() for line in content.splitlines() if line.strip().startswith("|")]

        data_rows = []
        for line in lines:
            # Skip separator line (e.g. |---|---|---|)
            if re.match(r"^\|(\s*:?-+:?\s*\|)+$", line):
                continue
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 3:
                # Check if it's the header row
                header_words = ["ئىسىم", "ئوقۇلۇشى", "مەنىسى", "arabic", "name", "meaning"]
                is_header = any(hw in cells[0].lower() or hw in cells[1].lower() for hw in header_words)
                if not is_header:
                    data_rows.append(cells)

        # Fallback to HTML table parsing if markdown table had no data rows
        if not data_rows and "<table" in content.lower():
            row_pattern = re.compile(r"<tr[^>]*>([\s\S]*?)</tr>", re.IGNORECASE)
            cell_pattern = re.compile(r"<td[^>]*>([\s\S]*?)</td>", re.IGNORECASE)
            for row_m in row_pattern.finditer(content):
                row_html = row_m.group(1)
                td_matches = [self._clean_html_text(td.group(1)) for td in cell_pattern.finditer(row_html)]
                if len(td_matches) >= 3:
                    header_words = ["ئىسىم", "ئوقۇلۇشى", "مەنىسى", "arabic", "name", "meaning"]
                    is_header = any(hw in td_matches[0].lower() or hw in td_matches[1].lower() for hw in header_words)
                    if not is_header:
                        data_rows.append(td_matches)

        row_count = len(data_rows)
        if row_count != 99:
            details.append(f"Expected exactly 99 table rows, found {row_count}")

        unfilled_cells = 0
        for i, row in enumerate(data_rows):
            # Check all 3 columns
            arabic_col = row[0]
            uyghur_col = row[1]
            meaning_col = row[2]

            if not arabic_col or not uyghur_col or not meaning_col:
                unfilled_cells += 1
                if unfilled_cells <= 5:
                    details.append(f"Row {i+1} has empty cell: Arabic='{arabic_col}', Uyghur='{uyghur_col}', Meaning='{meaning_col}'")

        if unfilled_cells > 0:
            details.append(f"Total rows with unfilled cells: {unfilled_cells}")

        arabic_names = [row[0] for row in data_rows]
        distinct_arabic_count = len(set(arabic_names))
        if distinct_arabic_count != 99:
            details.append(f"Expected 99 distinct Arabic names, found {distinct_arabic_count} (duplicates exist)")

        passed = (row_count == 99) and (unfilled_cells == 0) and (distinct_arabic_count == 99)
        msg = f"99 Names table verified: {row_count}/99 rows populated across all 3 columns ({distinct_arabic_count} distinct names)"
        return TestCaseResult("99 Names of Allah Table Verification", passed, msg, details)

    def test_option_b_css_presence(self) -> TestCaseResult:
        """Verify Option B CSS (.qa-card, .qa-question, .qa-answer, .qa-number) in src/styles/custom.css."""
        css_path = self.project_root / "src" / "styles" / "custom.css"
        details = []

        if not css_path.exists():
            details.append(f"File {css_path} does not exist.")
            return TestCaseResult("Option B Card CSS Presence", False, "custom.css missing", details)

        css_content = css_path.read_text(encoding="utf-8")
        required_classes = [".qa-card", ".qa-question", ".qa-answer", ".qa-number"]

        missing_classes = []
        for cls in required_classes:
            if cls not in css_content:
                missing_classes.append(cls)

        if missing_classes:
            details.append(f"Missing CSS selectors in custom.css: {missing_classes}")

        passed = len(missing_classes) == 0
        msg = f"Option B CSS classes: {len(required_classes) - len(missing_classes)}/{len(required_classes)} found"
        return TestCaseResult("Option B Card CSS Presence", passed, msg, details)

    def test_sidebar_navigation_config(self) -> TestCaseResult:
        """Verify Starlight navigation config in astro.config.mjs contains 2000 section."""
        astro_cfg_path = self.project_root / "astro.config.mjs"
        details = []

        if not astro_cfg_path.exists():
            details.append(f"File {astro_cfg_path} does not exist.")
            return TestCaseResult("Starlight Sidebar Navigation Config", False, "astro.config.mjs missing", details)

        content = astro_cfg_path.read_text(encoding="utf-8")

        # Check for 2000 navigation keywords
        has_2000_label = ("2000 سوئال-جاۋاب" in content) or ("2000" in content and "سوئال" in content)
        has_2000_dir = ("2000" in content)

        if not has_2000_label:
            details.append("Navigation label '2000 سوئال-جاۋاب' not found in astro.config.mjs sidebar config.")
        if not has_2000_dir:
            details.append("Directory '2000' reference not found in sidebar config.")

        passed = has_2000_label and has_2000_dir
        msg = "Sidebar navigation group for 2000 questions found in astro.config.mjs" if passed else "Sidebar config missing 2000 entries"
        return TestCaseResult("Starlight Sidebar Navigation Config", passed, msg, details)

    # =========================================================================
    # TIER 4 - Build & Search Validation
    # =========================================================================

    def test_astro_build(self) -> TestCaseResult:
        """Verify full site build via pnpm build (or skip if pnpm is not in PATH)."""
        if self.skip_build:
            return TestCaseResult("Astro Build (pnpm build)", True, "Skipped by user flag (--skip-build)")

        import shutil
        if not shutil.which("pnpm"):
            return TestCaseResult("Astro Build (pnpm build)", True, "Skipped: pnpm is not installed in current shell environment")

        try:
            res = subprocess.run(
                ["pnpm", "build"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=180,
            )
            passed = (res.returncode == 0)
            details = []
            if not passed:
                stderr_lines = res.stderr.splitlines()
                details.extend(stderr_lines[-20:])
                details.append(f"Build exited with return code {res.returncode}")

            msg = "pnpm build completed successfully (exit code 0)" if passed else f"pnpm build failed (exit code {res.returncode})"
            return TestCaseResult("Astro Build (pnpm build)", passed, msg, details)
        except Exception as e:
            return TestCaseResult("Astro Build (pnpm build)", False, f"Build execution error: {str(e)}", [str(e)])

    def test_pagefind_search_index(self) -> TestCaseResult:
        """Verify Pagefind search index generation in dist/pagefind/."""
        dist_pagefind = self.project_root / "dist" / "pagefind"
        details = []

        if not dist_pagefind.exists():
            details.append(f"Directory {dist_pagefind} does not exist. (Has `pnpm build` been executed?)")
            return TestCaseResult("Pagefind Search Index Generation", False, "dist/pagefind/ missing", details)

        # Check for core Pagefind index artifacts
        files = list(dist_pagefind.glob("*"))
        if not files:
            details.append(f"Directory {dist_pagefind} is empty.")
            return TestCaseResult("Pagefind Search Index Generation", False, "dist/pagefind/ is empty", details)

        has_js = any(f.name.endswith(".js") for f in files)
        details.append(f"Found {len(files)} search index files in {dist_pagefind}")

        passed = len(files) > 0 and has_js
        msg = f"Pagefind index generated ({len(files)} files found)"
        return TestCaseResult("Pagefind Search Index Generation", passed, msg, details)

    # =========================================================================
    # Runner Orchestration
    # =========================================================================

    def run_tier_1(self) -> List[TestCaseResult]:
        return [
            self.test_question_count(),
            self.test_question_number_set(),
            self.test_question_structure(),
            self.test_section_00_pages(),
            self.test_section_01_pages_and_boundaries(),
            self.test_section_02_pages_and_boundaries(),
            self.test_section_03_pages_and_boundaries(),
            self.test_section_04_pages_and_boundaries(),
            self.test_section_05_pages_and_boundaries(),
            self.test_section_06_pages_and_boundaries(),
            self.test_section_07_pages_and_boundaries(),
            self.test_section_08_pages_and_boundaries(),
            self.test_section_09_pages_and_boundaries(),
            self.test_section_10_pages_and_boundaries(),
            self.test_section_11_pages_and_boundaries(),
            self.test_section_12_pages_and_boundaries(),
        ]

    def run_tier_2(self) -> List[TestCaseResult]:
        return [
            self.test_zero_dotless_beh(),
            self.test_zero_beeh_two_dots_below(),
            self.test_zero_farsi_yeh(),
            self.test_zero_interior_tatweels(),
            self.test_zero_broken_words(),
            self.test_boundary_questions_integrity(),
        ]

    def run_tier_3(self) -> List[TestCaseResult]:
        return [
            self.test_99_names_table(),
            self.test_option_b_css_presence(),
            self.test_sidebar_navigation_config(),
        ]

    def run_tier_4(self) -> List[TestCaseResult]:
        return [
            self.test_astro_build(),
            self.test_pagefind_search_index(),
        ]

    def run_all(self, selected_tier: Optional[int] = None) -> Dict[str, List[TestCaseResult]]:
        results: Dict[str, List[TestCaseResult]] = {}

        if selected_tier is None or selected_tier == 1:
            results["Tier 1 - Feature Coverage"] = self.run_tier_1()
        if selected_tier is None or selected_tier == 2:
            results["Tier 2 - Boundary & Integrity"] = self.run_tier_2()
        if selected_tier is None or selected_tier == 3:
            results["Tier 3 - 99 Names & Cross-Feature"] = self.run_tier_3()
        if selected_tier is None or selected_tier == 4:
            results["Tier 4 - Build & Search Validation"] = self.run_tier_4()

        return results


def print_report(results: Dict[str, List[TestCaseResult]], verbose: bool = False, no_color: bool = False) -> bool:
    total_passed = 0
    total_failed = 0

    print("\n" + "=" * 78)
    print(colorize(" DIN VE HAYAT (2000 SUALLIQ) — E2E TEST SUITE REPORT", Colors.BOLD, no_color))
    print("=" * 78)

    for tier_name, test_results in results.items():
        print(f"\n{colorize(tier_name, Colors.CYAN + Colors.BOLD, no_color)}")
        print("-" * 78)

        for res in test_results:
            if res.passed:
                status = colorize("[PASS]", Colors.GREEN + Colors.BOLD, no_color)
                total_passed += 1
            else:
                status = colorize("[FAIL]", Colors.RED + Colors.BOLD, no_color)
                total_failed += 1

            print(f"  {status} {res.name}")
            if res.message:
                print(f"         {res.message}")

            if not res.passed or verbose:
                for detail in res.details:
                    print(f"         {colorize('• ' + detail, Colors.YELLOW if res.passed else Colors.RED, no_color)}")

    print("\n" + "=" * 78)
    summary_color = Colors.GREEN if total_failed == 0 else Colors.RED
    print(colorize(f" SUMMARY: {total_passed} PASSED | {total_failed} FAILED | TOTAL: {total_passed + total_failed}", summary_color + Colors.BOLD, no_color))
    print("=" * 78 + "\n")

    return total_failed == 0


def main():
    parser = argparse.ArgumentParser(description="E2E Test Suite for Din ve Hayat (2000 Sualliq)")
    parser.add_argument("--tier", type=int, choices=[1, 2, 3, 4], help="Run a specific tier only (1..4)")
    parser.add_argument("--all", action="store_true", help="Run all tiers (default)")
    parser.add_argument("--skip-build", action="store_true", help="Skip executing `pnpm build` in Tier 4")
    parser.add_argument("--verbose", "-v", action="store_true", help="Display full details and diagnostic messages")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI color codes")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--project-root", type=str, default=".", help="Project root directory (default: current directory)")

    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    tester = DinVeHayatTester(
        project_root=project_root,
        skip_build=args.skip_build,
        verbose=args.verbose,
        no_color=args.no_color,
    )

    results = tester.run_all(selected_tier=args.tier)

    if args.json:
        out = {
            "tier_results": {tier: [t.to_dict() for t in tests] for tier, tests in results.items()},
            "passed": all(t.passed for tests in results.values() for t in tests),
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
        sys.exit(0 if out["passed"] else 1)
    else:
        all_passed = print_report(results, verbose=args.verbose, no_color=args.no_color)
        sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
