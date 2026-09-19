#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/e2e_namaz.py

E2E Test suite for «نامازدىن ساۋات» (Basics of Prayer) portal:
1. Verifies existence of all 16 MDX files (index + 15 chapters).
2. Verifies public assets (cover.png, namazdin-sawat.pdf, instructional images).
3. Verifies TOC links in index.mdx resolve to valid pages and anchors.
4. Verifies Unicode integrity (clean modern UEY, zero presentation form glyphs, zero tatweels).
5. Verifies zero unescaped JSX curly braces in body prose.
"""

import sys
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "src" / "content" / "docs" / "namaz"
PUBLIC_DIR = BASE_DIR / "public" / "namaz"

def main():
    print("==============================================================================")
    print(" NAMAZ PORTAL («نامازدىن ساۋات») — E2E TEST SUITE REPORT")
    print("==============================================================================")

    passed = 0
    failed = 0

    # Test 1: Required MDX files
    required_files = [
        DOCS_DIR / "index.mdx",
        DOCS_DIR / "00-muqeddimu" / "01-muqeddimu-ve-ibadet.mdx",
        DOCS_DIR / "01-birinchi-bolum" / "01-namazning-orni-ve-su.mdx",
        DOCS_DIR / "01-birinchi-bolum" / "02-istinja-nijaset.mdx",
        DOCS_DIR / "01-birinchi-bolum" / "03-taharet-ve-meshi.mdx",
        DOCS_DIR / "01-birinchi-bolum" / "04-ayallar-ghusli-teyemmum.mdx",
        DOCS_DIR / "01-birinchi-bolum" / "05-waqit-ezan-ewret-qible.mdx",
        DOCS_DIR / "02-ikkinchi-bolum" / "01-reketer-perzler.mdx",
        DOCS_DIR / "02-ikkinchi-bolum" / "02-namaz-oqulush-tertipi.mdx",
        DOCS_DIR / "02-ikkinchi-bolum" / "03-namazni-buzidighan-sehwi.mdx",
        DOCS_DIR / "02-ikkinchi-bolum" / "04-sutre-qiraet-tilawet-qaza.mdx",
        DOCS_DIR / "03-uchinchi-bolum" / "01-jamaet-ve-jume.mdx",
        DOCS_DIR / "03-uchinchi-bolum" / "02-jinaze-namizi.mdx",
        DOCS_DIR / "03-uchinchi-bolum" / "03-yoluchi-namizi.mdx",
        DOCS_DIR / "03-uchinchi-bolum" / "04-heyit-ve-terawih.mdx",
        DOCS_DIR / "03-uchinchi-bolum" / "05-kesel-ve-neple.mdx",
    ]
    missing_files = [f for f in required_files if not f.exists()]
    if not missing_files:
        print(f"  [PASS] All {len(required_files)} required MDX files exist.")
        passed += 1
    else:
        print(f"  [FAIL] Missing files: {missing_files}")
        failed += 1

    # Test 2: Public assets
    required_assets = [
        PUBLIC_DIR / "cover.png",
        PUBLIC_DIR / "namazdin-sawat.pdf",
        PUBLIC_DIR / "images" / "wudu-1-2.png",
        PUBLIC_DIR / "images" / "teyemmum.png",
        PUBLIC_DIR / "images" / "namaz-takbir.png",
        PUBLIC_DIR / "images" / "namaz-qiyam.png",
        PUBLIC_DIR / "images" / "namaz-ruku.png",
        PUBLIC_DIR / "images" / "namaz-sajdah.png",
        PUBLIC_DIR / "images" / "namaz-olturush-erler.png",
        PUBLIC_DIR / "images" / "namaz-olturush-ayallar.png",
        PUBLIC_DIR / "images" / "namaz-salam.png",
    ]
    missing_assets = [a for a in required_assets if not a.exists()]
    if not missing_assets:
        print(f"  [PASS] All {len(required_assets)} public assets (cover, PDF, images) exist.")
        passed += 1
    else:
        print(f"  [FAIL] Missing assets: {missing_assets}")
        failed += 1

    # Test 3: Index TOC link resolution
    index_text = (DOCS_DIR / "index.mdx").read_text("utf-8")
    links = re.findall(r'href="([^"]+)"', index_text)
    broken_links = []

    for link in links:
        if link.startswith("/namaz/"):
            clean_link = link[len("/namaz/"):]
            parts = clean_link.split("#")
            page_route = parts[0].rstrip("/")
            anchor = parts[1] if len(parts) > 1 else None

            target_file = DOCS_DIR / f"{page_route}.mdx"
            if not target_file.exists():
                broken_links.append(f"Missing target file: {link} -> {target_file}")
            elif anchor:
                target_text = target_file.read_text("utf-8")
                # check if anchor exists as heading or id
                # Starlight slugifies headings: e.g. "## ماۋزۇ"
                # Check for either the heading text or explicit id
                decoded_anchor = re.sub(r'[\-_]+', ' ', anchor)
                if anchor not in target_text and decoded_anchor not in target_text:
                    broken_links.append(f"Anchor '{anchor}' not found in {target_file.name}")

    if not broken_links:
        print(f"  [PASS] All {len(links)} TOC links in index.mdx resolve successfully.")
        passed += 1
    else:
        print(f"  [FAIL] Broken TOC links: {broken_links}")
        failed += 1

    # Test 4: Unicode presentation forms and tatweels
    presentation_forms = re.compile(r'[\uFB50-\uFD3D\uFD40-\uFDFF\uFE70-\uFEFF]')
    tatweel = re.compile(r'\u0640')
    unicode_errors = []

    for f in required_files:
        txt = f.read_text("utf-8")
        pf_matches = presentation_forms.findall(txt)
        tw_matches = tatweel.findall(txt)
        if pf_matches:
            unicode_errors.append(f"{f.name}: {len(pf_matches)} presentation form glyphs")
        if tw_matches:
            unicode_errors.append(f"{f.name}: {len(tw_matches)} tatweels")

    if not unicode_errors:
        print("  [PASS] Zero legacy presentation forms and zero tatweels across all pages.")
        passed += 1
    else:
        print(f"  [FAIL] Unicode issues found: {unicode_errors}")
        failed += 1

    # Test 5: Check for raw curly braces in prose (which would fail MDX compilation)
    raw_curlies = []
    for f in required_files:
        lines = f.read_text("utf-8").splitlines()
        for lno, l in enumerate(lines, 1):
            if l.startswith("import ") or l.startswith("tags=") or l.startswith("---"):
                continue
            if "{" in l or "}" in l:
                raw_curlies.append(f"{f.name}:{lno}: {l}")

    if not raw_curlies:
        print("  [PASS] Zero unescaped curly braces in MDX prose.")
        passed += 1
    else:
        print(f"  [FAIL] Unescaped curly braces: {raw_curlies[:5]}")
        failed += 1

    # Test 6: Check for unicode replacement characters (\ufffd) and inverted hamza
    fffd_files = []
    inverted_hamza_errors = []
    for f in required_files:
        txt = f.read_text("utf-8")
        if "\ufffd" in txt:
            fffd_files.append(f.name)
        
        # Inverted start vowels (\b[vowel]ئ)
        for m in re.finditer(r"(?<![\u0600-\u06FF])([ىۇۆېەائوئۈ])ئ([^\s.,،!؟:؛\-\)\(»«\[\]\"`\/]+)?", txt):
            inverted_hamza_errors.append(f"{f.name}: start inversion '{m.group(0)}'")
            
        # Internal broken hamza patterns
        for m in re.finditer(r"[^\s.,،!؟:؛\-\)\(»«\[\]\"`\/]*(?:ائي|قاىئ|جاىئ|رەكەئت|رەكىئ|قىراەئت|مەنىئ|دۇائسى)[^\s.,،!؟:؛\-\)\(»«\[\]\"`\/]*", txt):
            inverted_hamza_errors.append(f"{f.name}: internal inversion '{m.group(0)}'")

    if not fffd_files and not inverted_hamza_errors:
        print("  [PASS] Zero \\ufffd characters and zero inverted hamza occurrences across all pages.")
        passed += 1
    else:
        if fffd_files:
            print(f"  [FAIL] \\ufffd replacement character found in: {fffd_files}")
        if inverted_hamza_errors:
            print(f"  [FAIL] Inverted hamza occurrences: {inverted_hamza_errors[:5]}")
        failed += 1

    # Test 7: Verify specific fixed phrases
    intro_file = DOCS_DIR / "00-muqeddimu" / "01-muqeddimu-ve-ibadet.mdx"
    intro_txt = intro_file.read_text("utf-8")
    expected_phrases = [
        "### ئىبادەت ۋە ئۇنىڭ تۈرلىرى",
        "مۇسۇلمانلارغا ئىماندىن كېيىنلا بۇيرۇلغان ئەڭ مۇھىم نەرسە ئىبادەتتۇر.",
        "ئىبادەتلەر ساغلام ئەقىدىنىڭ دەلىلى ۋە ئۇنىڭ ئەمەلدىكى تەرجىمىسىدۇر.",
    ]
    missing_phrases = [p for p in expected_phrases if p not in intro_txt]
    if not missing_phrases:
        print("  [PASS] Required corrected phrases (including 'ساغلام') verified in introductory chapter.")
        passed += 1
    else:
        print(f"  [FAIL] Missing expected phrases in {intro_file.name}: {missing_phrases}")
        failed += 1

    # Test 8: Verify zero disconnected / inverted lam-alif patterns (e.g. ساغالم -> ساغلام)
    lam_alif_typos = [
        r"\bساغالم\b",
        r"\bباشالم",
        r"\bتولۇقال",
        r"\bباغال",
        r"\bالزىم\b",
        r"\bاليىق\b",
        r"\bئەخالق\b",
        r"\bساالھىيەت\b",
        r"\bھاالكەت\b",
        r"\bئابدۇلالھ\b",
        r"\bرەسۇلەلالھ\b",
        r"\bنامازالر\b",
    ]
    typo_errors = []
    for f in required_files:
        txt = f.read_text("utf-8")
        for typo_pat in lam_alif_typos:
            m = re.search(typo_pat, txt)
            if m:
                typo_errors.append(f"{f.name}: found inverted pattern '{m.group(0)}'")

    if not typo_errors:
        print("  [PASS] Zero inverted 'ال' ligature typos (e.g. ساغالم, الزىم, اليىق) across all pages.")
        passed += 1
    else:
        print(f"  [FAIL] Found inverted lam-alif typos: {typo_errors[:5]}")
        failed += 1

    # Test 9: Number placement (numbers before text, zero trailing list numbers)
    ch1_file = DOCS_DIR / "01-birinchi-bolum" / "01-namazning-orni-ve-su.mdx"
    ch1_txt = ch1_file.read_text("utf-8")
    expected_list_items = [
        "1. يامغۇر سۈيى",
        "2. دېڭىز، دەريا، ئېرىق، ئۆستەڭ سۇلىرى",
        "1. پاكىزلىق",
        "2. تاھارەت (غۇسلى بىلەن تەيەممۇمنىمۇ ئۆز ئىچىگە ئالىدۇ)",
    ]
    missing_list_items = [item for item in expected_list_items if item not in ch1_txt]

    trailing_list_errors = []
    # Check for trailing numbers at the end of words that were lists: e.g. يامغۇر سۈيى1, پاكىزلىق1
    for f in required_files:
        txt = f.read_text("utf-8")
        if re.search(r"يامغۇر سۈيى1|پاكىزلىق1|تەھىيەتۇل مەسجىد نامىزى1\.", txt):
            trailing_list_errors.append(f"{f.name}: found trailing list numbers")

    if not missing_list_items and not trailing_list_errors:
        print("  [PASS] Number placement verified: numbers appear before text in lists and headings.")
        passed += 1
    else:
        if missing_list_items:
            print(f"  [FAIL] Missing numbered list items: {missing_list_items}")
        if trailing_list_errors:
            print(f"  [FAIL] Trailing list numbers: {trailing_list_errors}")
        failed += 1

    print("------------------------------------------------------------------------------")
    print(f" TOTAL: {passed} PASSED, {failed} FAILED")
    print("==============================================================================")
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()

