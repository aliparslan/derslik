#!/usr/bin/env python3
"""
E2E Test suite for Hayat Portal ( «ھاياتىڭىزنى قەدىرلەڭ» — مۇھەممەد يۈسۈپ )
Verifies:
1. All 11 MDX files exist.
2. Structure: All 57 chapter cards, 40 beacon cards, and 9 recommendation cards exist (total 106 cards).
3. Index links: Anchors in index.mdx match target sections.
4. Unicode & text integrity: Valid UEY, zero presentation form glyphs.
5. PDF asset existence and integrity.
6. Verification of HTML build outputs (if built).
"""

import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / "src" / "content" / "docs" / "hayat"
DIST_DIR = BASE_DIR / "dist" / "hayat"
PDF_FILE = BASE_DIR / "public" / "hayat" / "hayatingizni-qedirleng.pdf"

def main():
    print("==============================================================================")
    print(" HAYAT PORTAL (ھاياتىڭىزنى قەدىرلەڭ) — E2E TEST SUITE REPORT")
    print("==============================================================================")
    
    passed = 0
    failed = 0

    # Test 1: Files existence
    files_to_check = [
        DOCS_DIR / "index.mdx",
        DOCS_DIR / "00-muqeddimu" / "01-muellip-heqqide.mdx",
        DOCS_DIR / "00-muqeddimu" / "02-kirish-soz.mdx",
        DOCS_DIR / "01-bap-01-10.mdx",
        DOCS_DIR / "02-bap-11-20.mdx",
        DOCS_DIR / "03-bap-21-30.mdx",
        DOCS_DIR / "04-bap-31-40.mdx",
        DOCS_DIR / "05-bap-41-50.mdx",
        DOCS_DIR / "06-bap-51-57.mdx",
        DOCS_DIR / "07-40-mesh-el.mdx",
        DOCS_DIR / "08-toqquz-tewsiye.mdx",
    ]
    missing_files = [f for f in files_to_check if not f.exists()]
    if not missing_files:
        print("  [PASS] All 11 required hayat MDX files exist.")
        passed += 1
    else:
        print(f"  [FAIL] Missing files: {missing_files}")
        failed += 1

    # Test 2: PDF asset
    if PDF_FILE.exists() and PDF_FILE.stat().st_size > 1_000_000:
        print(f"  [PASS] PDF asset exists at public/hayat/hayatingizni-qedirleng.pdf ({PDF_FILE.stat().st_size / 1024 / 1024:.2f} MB).")
        passed += 1
    else:
        print("  [FAIL] PDF asset missing or too small.")
        failed += 1

    # Test 3: Hadith/Content Cards & ID checks
    card_pattern = re.compile(r'<div\s+class="hadith-card"\s+id="([^"]+)">', re.IGNORECASE)
    found_cards = {}
    
    for fpath in files_to_check[3:]:  # content pages
        content = fpath.read_text(encoding="utf-8")
        matches = card_pattern.findall(content)
        for anchor_id in matches:
            if anchor_id in found_cards:
                print(f"  [FAIL] Duplicate card ID: {anchor_id} in {fpath.name}")
                failed += 1
            found_cards[anchor_id] = fpath.name

    # Check 57 chapters
    missing_baps = [f"bap-{i:02d}" for i in range(1, 58) if f"bap-{i:02d}" not in found_cards]
    # Check 40 mesh-el
    missing_meshel = [f"mesh-el-{i}" for i in range(1, 41) if f"mesh-el-{i}" not in found_cards]
    # Check 9 tewsiye
    missing_tewsiye = [f"tewsiye-{i}" for i in range(1, 10) if f"tewsiye-{i}" not in found_cards]

    if not missing_baps and not missing_meshel and not missing_tewsiye and len(found_cards) == 106:
        print(f"  [PASS] Exactly 106 cards found: 57 chapters (bap-01..57), 40 beacons (mesh-el-1..40), 9 recommendations (tewsiye-1..9).")
        passed += 1
    else:
        print(f"  [FAIL] Total cards found: {len(found_cards)} (expected 106).")
        if missing_baps:
            print(f"         Missing chapters: {missing_baps}")
        if missing_meshel:
            print(f"         Missing beacons: {missing_meshel}")
        if missing_tewsiye:
            print(f"         Missing recommendations: {missing_tewsiye}")
        failed += 1

    # Test 4: Index TOC links check
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

    # Test 5: Unicode presentation forms check (excluding standard Quranic brackets ﴿ ﴾ U+FD3E/U+FD3F)
    presentation_forms = re.compile(r'[\uFB50-\uFD3D\uFD40-\uFDFF\uFE70-\uFEFF]')
    dirty_files = []
    for fpath in DOCS_DIR.rglob("*.mdx"):
        content = fpath.read_text(encoding="utf-8")
        matches = presentation_forms.findall(content)
        if matches:
            dirty_files.append((fpath.name, len(matches)))

    if not dirty_files:
        print("  [PASS] Zero Arabic presentation forms found. All text in standard Unicode UEY.")
        passed += 1
    else:
        print(f"  [FAIL] Presentation forms detected: {dirty_files}")
        failed += 1

    # Test 6: HTML build verification if dist exists
    if DIST_DIR.exists():
        html_files = list(DIST_DIR.rglob("index.html"))
        if len(html_files) >= 10:
            print(f"  [PASS] Production build output verified: {len(html_files)} HTML pages generated under dist/hayat/.")
            passed += 1
        else:
            print(f"  [FAIL] Insufficient HTML output: only {len(html_files)} files.")
            failed += 1

    print("------------------------------------------------------------------------------")
    print(f" Results: {passed} PASSED, {failed} FAILED")
    print("==============================================================================")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
