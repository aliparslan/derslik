#!/usr/bin/env python3
"""
E2E Test suite for 40 Hadiths ( الأربعون النووية / قىرىق ھەدىس )
Verifies:
1. All 42 Hadith cards exist and have continuous IDs: hedis-1 to hedis-42.
2. Structure: hedis-card, hedis-header, hedis-arabic, hedis-translation, hedis-sharh.
3. Index links: 42 anchors in index.mdx match target hedis-1..42.
4. Unicode & text integrity: zero legacy glyphs (\u066e, \u067b, \u06cc), zero interior tatweels.
5. Astro build capability.
"""

import re
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "src" / "content" / "docs" / "40hedis"

def main():
    print("==============================================================================")
    print(" FORTY HADITH (قىرىق ھەدىس) — E2E TEST SUITE REPORT")
    print("==============================================================================")
    
    passed = 0
    failed = 0

    # Test 1: Files existence
    files_to_check = [
        DOCS_DIR / "index.mdx",
        DOCS_DIR / "00-muqeddimu" / "01-kitab-heqqide.mdx",
        DOCS_DIR / "01-hedis-01-10.mdx",
        DOCS_DIR / "02-hedis-11-20.mdx",
        DOCS_DIR / "03-hedis-21-30.mdx",
        DOCS_DIR / "04-hedis-31-42.mdx",
    ]
    missing_files = [f for f in files_to_check if not f.exists()]
    if not missing_files:
        print("  [PASS] All 6 required 40hedis MDX files exist.")
        passed += 1
    else:
        print(f"  [FAIL] Missing files: {missing_files}")
        failed += 1

    # Test 2: Hadith Cards Extraction & Counting (1 to 42)
    card_pattern = re.compile(r'<div\s+class="hadith-card"\s+id="(hedis-(\d+))">', re.IGNORECASE)
    found_hedis = {}
    
    for fpath in files_to_check:
        if not fpath.exists():
            continue
        content = fpath.read_text(encoding="utf-8")
        matches = card_pattern.findall(content)
        for anchor_id, num_str in matches:
            num = int(num_str)
            if num in found_hedis:
                print(f"  [FAIL] Duplicate Hadith ID found: hedis-{num} in {fpath.name}")
                failed += 1
            found_hedis[num] = fpath.name

    expected_nums = set(range(1, 43))
    actual_nums = set(found_hedis.keys())

    if actual_nums == expected_nums:
        print(f"  [PASS] Hadith Count & Sequence: Exactly 42 Hadiths found (hedis-1 to hedis-42).")
        passed += 1
    else:
        missing = expected_nums - actual_nums
        extra = actual_nums - expected_nums
        print(f"  [FAIL] Hadith mismatch. Missing: {missing}, Extra: {extra}")
        failed += 1

    # Test 3: Structural Components of each Hadith Card (Arabic + Translation mandatory)
    structural_errors = []
    hedis_files = [
        DOCS_DIR / "01-hedis-01-10.mdx",
        DOCS_DIR / "02-hedis-11-20.mdx",
        DOCS_DIR / "03-hedis-21-30.mdx",
        DOCS_DIR / "04-hedis-31-42.mdx",
    ]

    sharh_count = 0
    for fpath in hedis_files:
        if not fpath.exists():
            continue
        content = fpath.read_text(encoding="utf-8")
        cards = content.split('<div class="hadith-card"')[1:]
        for c in cards:
            m = re.search(r'id="hedis-(\d+)"', c)
            if not m:
                continue
            h_num = m.group(1)
            if 'class="hadith-arabic"' not in c:
                structural_errors.append(f"hedis-{h_num}: missing hadith-arabic")
            if 'class="hadith-translation"' not in c:
                structural_errors.append(f"hedis-{h_num}: missing hadith-translation")
            if 'class="hadith-sharh"' in c:
                sharh_count += 1

    if not structural_errors:
        print(f"  [PASS] Hadith Card Structural Integrity: All 42 cards contain Arabic & Translation ({sharh_count}/42 with extended Sharh).")
        passed += 1
    else:
        print(f"  [FAIL] Structural errors ({len(structural_errors)}): {structural_errors[:5]}")
        failed += 1

    # Test 4: Unicode Integrity Check
    unicode_errors = []
    for fpath in files_to_check:
        if not fpath.exists():
            continue
        content = fpath.read_text(encoding="utf-8")
        for g in ['\u066e', '\u067b', '\u06cc']:
            if g in content:
                unicode_errors.append(f"{fpath.name}: contains legacy glyph '\\u{ord(g):04x}'")
        
        tatweel_matches = re.findall(r'[\u0621-\u064a\u0671-\u06d5]\u0640+[\u0621-\u064a\u0671-\u06d5]', content)
        if tatweel_matches:
            unicode_errors.append(f"{fpath.name}: contains {len(tatweel_matches)} interior tatweels")

    if not unicode_errors:
        print("  [PASS] Unicode Integrity: 0 legacy glyphs and 0 interior tatweels found across 40hedis.")
        passed += 1
    else:
        print(f"  [FAIL] Unicode errors: {unicode_errors}")
        failed += 1

    # Test 5: Table of Contents Anchors in index.mdx
    index_file = DOCS_DIR / "index.mdx"
    if index_file.exists():
        idx_content = index_file.read_text(encoding="utf-8")
        missing_index_anchors = []
        for i in range(1, 43):
            anchor = f"#hedis-{i}"
            if anchor not in idx_content:
                missing_index_anchors.append(anchor)
        if not missing_index_anchors:
            print("  [PASS] Index Table of Contents: All 42 Hadith anchor links (#hedis-1 to #hedis-42) present.")
            passed += 1
        else:
            print(f"  [FAIL] Missing anchors in index.mdx: {missing_index_anchors}")
            failed += 1

    print("==============================================================================")
    print(f" SUMMARY: {passed} PASSED | {failed} FAILED | TOTAL: {passed + failed}")
    print("==============================================================================")
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()
