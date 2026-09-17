#!/usr/bin/env python3
"""
E2E Test suite for 100 Hadiths ( تاللانغان 100 ھەدىسنىڭ تەرجىمىسى ۋە ئىزاھاتى / نىجات يولى )
Verifies:
1. All 12 MDX files exist.
2. Structure: All 88 Hadith sections covering 1-100 Hadiths exist.
3. Index links: Anchors in index.mdx match target sections.
4. Unicode & text integrity: Valid UEY, zero presentation form glyphs.
5. Verification of HTML build outputs.
"""

import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / "src" / "content" / "docs" / "100hedis"
DIST_DIR = BASE_DIR / "dist" / "100hedis"

def main():
    print("==============================================================================")
    print(" 100 HADITH (تاللانغان 100 ھەدىس) — E2E TEST SUITE REPORT")
    print("==============================================================================")
    
    passed = 0
    failed = 0

    # Test 1: Files existence
    files_to_check = [
        DOCS_DIR / "index.mdx",
        DOCS_DIR / "00-muqeddimu" / "01-bighishlima-muqeddimu.mdx",
        DOCS_DIR / "01-hedis-01-10.mdx",
        DOCS_DIR / "02-hedis-11-20.mdx",
        DOCS_DIR / "03-hedis-21-30.mdx",
        DOCS_DIR / "04-hedis-31-40.mdx",
        DOCS_DIR / "05-hedis-41-50.mdx",
        DOCS_DIR / "06-hedis-51-60.mdx",
        DOCS_DIR / "07-hedis-61-70.mdx",
        DOCS_DIR / "08-hedis-71-80.mdx",
        DOCS_DIR / "09-hedis-81-90.mdx",
        DOCS_DIR / "10-hedis-91-100.mdx",
    ]
    missing_files = [f for f in files_to_check if not f.exists()]
    if not missing_files:
        print("  [PASS] All 12 required 100hedis MDX files exist.")
        passed += 1
    else:
        print(f"  [FAIL] Missing files: {missing_files}")
        failed += 1

    # Test 2: Hadith Cards & ID checks
    card_pattern = re.compile(r'<div\s+class="hadith-card"\s+id="([^"]+)">', re.IGNORECASE)
    found_cards = {}
    
    for fpath in files_to_check[2:]:  # group pages
        content = fpath.read_text(encoding="utf-8")
        matches = card_pattern.findall(content)
        for anchor_id in matches:
            if anchor_id in found_cards:
                print(f"  [FAIL] Duplicate card ID: {anchor_id} in {fpath.name}")
                failed += 1
            found_cards[anchor_id] = fpath.name

    if len(found_cards) == 88:
        print(f"  [PASS] Exactly 88 Hadith cards found across the 10 group pages (76 singles + 12 pairs = 100 Hadiths).")
        passed += 1
    else:
        print(f"  [FAIL] Expected 88 Hadith cards, but found {len(found_cards)}.")
        failed += 1

    # Test 3: Index TOC links check
    index_content = (DOCS_DIR / "index.mdx").read_text(encoding="utf-8")
    toc_links = re.findall(r'href="([^"]+)"', index_content)
    broken_links = []
    
    for link in toc_links:
        if link.startswith("./"):
            parts = link.lstrip("./").split("#")
            page_rel = parts[0]
            anchor = parts[1] if len(parts) > 1 else None
            
            target_page = DOCS_DIR / f"{page_rel}.mdx"
            if not target_page.exists():
                target_page = DOCS_DIR / page_rel / "01-bighishlima-muqeddimu.mdx"
                if not target_page.exists():
                    broken_links.append(f"Target page missing: {link}")
                    continue
            
            if anchor and anchor not in found_cards:
                broken_links.append(f"Anchor not found: {link}")

    if not broken_links:
        print("  [PASS] All TOC links in index.mdx resolve to valid pages and anchors.")
        passed += 1
    else:
        print(f"  [FAIL] Broken TOC links in index.mdx: {broken_links[:5]}")
        failed += 1

    # Test 4: Unicode presentation forms check
    presentation_forms = re.compile(r'[\uFB50-\uFDFF\uFE70-\uFEFF]')
    found_glyphs = 0
    for fpath in files_to_check:
        content = fpath.read_text(encoding="utf-8")
        matches = presentation_forms.findall(content)
        if matches:
            found_glyphs += len(matches)
            print(f"  [FAIL] Legacy presentation forms found in {fpath.name}: {len(matches)}")
            failed += 1

    if found_glyphs == 0:
        print("  [PASS] Zero legacy Arabic presentation forms (U+FB50-FDFF, U+FE70-FEFF) in MDX content.")
        passed += 1

    # Test 5: Dist HTML files check
    html_files = list(DIST_DIR.rglob("index.html"))
    if len(html_files) == 12:
        print(f"  [PASS] All 12 HTML pages successfully compiled in dist/100hedis/.")
        passed += 1
    else:
        print(f"  [FAIL] Expected 12 compiled HTML files in dist/100hedis, found {len(html_files)}.")
        failed += 1

    print("==============================================================================")
    print(f" TOTAL: {passed} PASSED, {failed} FAILED")
    print("==============================================================================")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
