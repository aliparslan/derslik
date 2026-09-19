#!/usr/bin/env python3
"""
E2E Test suite for Ereb Tili portal ( «ئەرەب تىلى دەرسلىكى گرامماتىكا قائىدىلىرى» / Arabic Grammar Portal )
Verifies:
1. All 17 MDX files exist in src/content/docs/ereb-tili/.
2. Static assets exist in public/ereb-tili/ (PDF and cover image).
3. Index TOC links: all links in index.mdx resolve to valid MDX files or assets.
4. Unicode & text integrity: modern UEY, zero legacy presentation form glyphs.
5. MDX curly brace safety: zero unescaped raw { or } braces in prose.
6. Navigation and Sidebar isolation across configuration and components.
7. Portal cards present on main landing pages (Uyghur & English).
8. Build output: All 17 compiled HTML pages exist in dist/ereb-tili/ (if dist exists).
"""

import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / "src" / "content" / "docs" / "ereb-tili"
PUBLIC_DIR = BASE_DIR / "public" / "ereb-tili"
DIST_DIR = BASE_DIR / "dist" / "ereb-tili"

def main():
    print("==============================================================================")
    print(" EREB TILI PORTAL (ئەرەب تىلى گرامماتىكا قائىدىلىرى) — E2E TEST SUITE REPORT")
    print("==============================================================================")
    
    passed = 0
    failed = 0

    # Test 1: Files existence (17 files)
    required_mdx_files = [
        DOCS_DIR / "index.mdx",
        DOCS_DIR / "00-muqeddimu" / "01-kirish-soz.mdx",
        DOCS_DIR / "00-muqeddimu" / "02-kitab-heqqide.mdx",
        DOCS_DIR / "01-1-qisim" / "01-ders-01-05.mdx",
        DOCS_DIR / "01-1-qisim" / "02-ders-06-10.mdx",
        DOCS_DIR / "01-1-qisim" / "03-ders-11-15.mdx",
        DOCS_DIR / "01-1-qisim" / "04-ders-16-23.mdx",
        DOCS_DIR / "02-2-qisim" / "01-ders-01-07.mdx",
        DOCS_DIR / "02-2-qisim" / "02-ders-08-15.mdx",
        DOCS_DIR / "02-2-qisim" / "03-ders-16-23.mdx",
        DOCS_DIR / "02-2-qisim" / "04-ders-24-31.mdx",
        DOCS_DIR / "03-3-qisim" / "01-muqeddimu.mdx",
        DOCS_DIR / "03-3-qisim" / "02-ders-01-08.mdx",
        DOCS_DIR / "03-3-qisim" / "03-ders-09-16.mdx",
        DOCS_DIR / "03-3-qisim" / "04-ders-17-24.mdx",
        DOCS_DIR / "03-3-qisim" / "05-ders-25-32.mdx",
        DOCS_DIR / "03-3-qisim" / "06-xatime.mdx",
    ]

    missing_files = [f for f in required_mdx_files if not f.exists()]
    if not missing_files:
        print(f"  [PASS] All {len(required_mdx_files)} required ereb-tili MDX files exist.")
        passed += 1
    else:
        print(f"  [FAIL] Missing MDX files: {[str(f.relative_to(BASE_DIR)) for f in missing_files]}")
        failed += 1

    # Test 2: Public static assets
    required_assets = [
        PUBLIC_DIR / "ereb-tili-dersliki-grammatika-qaidiliri.pdf",
        PUBLIC_DIR / "cover.png",
    ]
    missing_assets = [f for f in required_assets if not f.exists() or f.stat().st_size == 0]
    if not missing_assets:
        pdf_size = required_assets[0].stat().st_size
        img_size = required_assets[1].stat().st_size
        print(f"  [PASS] Static assets exist in public/ereb-tili/ (PDF: {pdf_size} bytes, Cover: {img_size} bytes).")
        passed += 1
    else:
        print(f"  [FAIL] Missing static assets: {missing_assets}")
        failed += 1

    # Test 3: Index TOC links check
    index_content = (DOCS_DIR / "index.mdx").read_text(encoding="utf-8")
    toc_links = (
        re.findall(r'href=[\"\'](/ereb-tili/[^\"\']+)[\"\']', index_content) +
        re.findall(r'link:\s*[\"\'](/ereb-tili/[^\"\']+)[\"\']', index_content) +
        re.findall(r'\[.+?\]\((/ereb-tili/[^)]+)\)', index_content)
    )
    broken_links = []

    for link in set(toc_links):
        if link.endswith(".pdf"):
            target_file = BASE_DIR / "public" / link.lstrip("/")
            if not target_file.exists():
                broken_links.append(f"Broken PDF link {link} -> {target_file} not found")
            continue
        rel_path = link.removeprefix("/ereb-tili/").strip("/")
        if not rel_path:
            continue
        target_mdx = DOCS_DIR / f"{rel_path}.mdx"
        if not target_mdx.exists():
            broken_links.append(f"Broken link {link} -> {target_mdx} not found")

    if not broken_links:
        print(f"  [PASS] All {len(toc_links)} navigation links in index.mdx resolve to valid targets.")
        passed += 1
    else:
        print(f"  [FAIL] Broken links found in index.mdx: {broken_links}")
        failed += 1

    # Test 4: Unicode presentation forms check
    presentation_forms = re.compile(r'[\uFB50-\uFDFF\uFE70-\uFEFF]')
    found_glyphs = 0
    for fpath in required_mdx_files:
        content = fpath.read_text(encoding="utf-8")
        matches = [c for c in presentation_forms.findall(content) if c not in ('\ufd3e', '\ufd3f')]
        if matches:
            found_glyphs += len(matches)
            print(f"  [FAIL] Legacy presentation forms found in {fpath.name}: {len(matches)}")
            failed += 1

    if found_glyphs == 0:
        print("  [PASS] Zero legacy Arabic presentation forms (UEY standard confirmed).")
        passed += 1

    # Test 5: MDX raw brace check
    brace_issues = []
    for fpath in required_mdx_files:
        content = fpath.read_text(encoding="utf-8")
        lines = content.splitlines()
        for idx, line in enumerate(lines, 1):
            if "{" in line or "}" in line:
                s = line.strip()
                if s.startswith("import ") or s.startswith("<Aside") or s.startswith("</Aside>") or s.startswith("<CardGrid") or s.startswith("</CardGrid>") or s.startswith("<LinkCard") or s.startswith("</LinkCard>"):
                    continue
                if "&#123;" in line or "&#125;" in line:
                    continue
                brace_issues.append((fpath.name, idx, line))

    if not brace_issues:
        print("  [PASS] Zero unescaped MDX curly braces across all 17 files.")
        passed += 1
    else:
        print(f"  [FAIL] Found {len(brace_issues)} unescaped curly brace lines: {brace_issues[:3]}")
        failed += 1

    # Test 6: Sidebar & component isolation check
    astro_cfg = (BASE_DIR / "astro.config.mjs").read_text(encoding="utf-8")
    sitetitle = (BASE_DIR / "src" / "components" / "SiteTitle.astro").read_text(encoding="utf-8")
    pagination = (BASE_DIR / "src" / "components" / "Pagination.astro").read_text(encoding="utf-8")
    sidebar = (BASE_DIR / "src" / "components" / "Sidebar.astro").read_text(encoding="utf-8")
    lang_select = (BASE_DIR / "src" / "components" / "LanguageSelect.astro").read_text(encoding="utf-8")
    header = (BASE_DIR / "src" / "components" / "Header.astro").read_text(encoding="utf-8")
    mobile_footer = (BASE_DIR / "src" / "components" / "MobileMenuFooter.astro").read_text(encoding="utf-8")

    isolation_errors = []
    if "directory: 'ereb-tili/03-3-qisim'" not in astro_cfg:
        isolation_errors.append("astro.config.mjs missing ereb-tili/03-3-qisim autogenerate")
    if "isErebTili" not in sitetitle:
        isolation_errors.append("SiteTitle.astro missing isErebTili check")
    if "isErebTili" not in pagination:
        isolation_errors.append("Pagination.astro missing isErebTili check")
    if "isErebTili" not in sidebar:
        isolation_errors.append("Sidebar.astro missing isErebTili check")
    if "otherPortalsForErebTili" not in sidebar:
        isolation_errors.append("Sidebar.astro missing otherPortalsForErebTili group")
    if "isErebTili" not in lang_select or "hideLanguage = " not in lang_select or "isErebTili" not in lang_select.split("hideLanguage = ")[1].split("\n")[0]:
        isolation_errors.append("LanguageSelect.astro missing isErebTili in hideLanguage")
    if "!isErebTili" not in header:
        isolation_errors.append("Header.astro missing !isErebTili check on LanguageSelect")
    if "!isErebTili" not in mobile_footer:
        isolation_errors.append("MobileMenuFooter.astro missing !isErebTili check on LanguageSelect")

    if not isolation_errors:
        print("  [PASS] Complete Sidebar, Component navigation, and LanguageSelect removal isolation confirmed.")
        passed += 1
    else:
        print(f"  [FAIL] Navigation isolation errors: {isolation_errors}")
        failed += 1

    # Test 7: Portal cards in root indexes
    ug_index = (BASE_DIR / "src" / "content" / "docs" / "index.mdx").read_text(encoding="utf-8")
    en_index = (BASE_DIR / "src" / "content" / "docs" / "en" / "index.mdx").read_text(encoding="utf-8")

    card_errors = []
    if "/ereb-tili/" not in ug_index or "ئەرەب تىلى گرامماتىكىسى" not in ug_index:
        card_errors.append("Root index.mdx missing /ereb-tili/ PortalCard")
    if "/ereb-tili/" not in en_index or "Arabic Grammar" not in en_index:
        card_errors.append("English en/index.mdx missing /ereb-tili/ PortalCard")

    if not card_errors:
        print("  [PASS] Portal cards verified in both Uyghur and English root homepages.")
        passed += 1
    else:
        print(f"  [FAIL] Portal card errors: {card_errors}")
        failed += 1

    # Test 8: Compiled HTML in dist/ereb-tili/ (if dist exists)
    if DIST_DIR.exists():
        html_files = list(DIST_DIR.rglob("index.html"))
        if len(html_files) == 17:
            print(f"  [PASS] All 17 HTML pages successfully compiled in dist/ereb-tili/.")
            passed += 1
        else:
            print(f"  [FAIL] Expected 17 compiled HTML files in dist/ereb-tili/, found {len(html_files)}.")
            failed += 1

        # Check that language select is completely removed from all ereb-tili HTML pages
        pages_with_lang_select = []
        for hf in html_files:
            html_text = hf.read_text(encoding="utf-8")
            if "starlight-lang-select" in html_text:
                pages_with_lang_select.append(str(hf.relative_to(DIST_DIR)))

        if not pages_with_lang_select:
            print("  [PASS] Zero language selection dropdowns found across all compiled ereb-tili pages.")
            passed += 1
        else:
            print(f"  [FAIL] Language select unexpectedly present in: {pages_with_lang_select}")
            failed += 1
    else:
        print("  [INFO] dist/ereb-tili/ does not exist yet (run pnpm build to generate).")

    print("==============================================================================")
    print(f" TOTAL: {passed} PASSED, {failed} FAILED")
    print("==============================================================================")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
