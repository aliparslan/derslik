#!/usr/bin/env python3
"""
E2E Test suite for Aile portal ( «ئىسلامدىكى ئائىلە تۈزۈمى» / Family System in Islam )
Verifies:
1. All 18 MDX files exist in src/content/docs/aile/.
2. Static assets exist in public/aile/ (PDF and cover image).
3. Index TOC links: all links in index.mdx resolve to valid MDX files.
4. Unicode & text integrity: modern UEY, zero legacy presentation form glyphs (allowing Quranic brackets ﴾ and ﴿).
5. Build output: All 18 compiled HTML pages exist in dist/aile/.
"""

import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / "src" / "content" / "docs" / "aile"
PUBLIC_DIR = BASE_DIR / "public" / "aile"
DIST_DIR = BASE_DIR / "dist" / "aile"

def main():
    print("==============================================================================")
    print(" AILE PORTAL (ئىسلامدىكى ئائىلە تۈزۈمى) — E2E TEST SUITE REPORT")
    print("==============================================================================")
    
    passed = 0
    failed = 0

    # Test 1: Files existence
    required_mdx_files = [
        DOCS_DIR / "index.mdx",
        DOCS_DIR / "00-muqeddimu" / "01-muqeddimiler-ve-aptur.mdx",
        DOCS_DIR / "01-qurulushi" / "01-aile-qurush-ve-usulliri.mdx",
        DOCS_DIR / "01-qurulushi" / "02-mehrem-ve-ewret.mdx",
        DOCS_DIR / "01-qurulushi" / "03-nikah-ehkamliri.mdx",
        DOCS_DIR / "01-qurulushi" / "04-toy-ve-meros.mdx",
        DOCS_DIR / "02-er-ayalliq-hayat" / "01-jinsi-alaqe-ve-adabliri.mdx",
        DOCS_DIR / "02-er-ayalliq-hayat" / "02-ayallargha-xas-haletler.mdx",
        DOCS_DIR / "02-er-ayalliq-hayat" / "03-er-xotun-heq-hoquqliri.mdx",
        DOCS_DIR / "02-er-ayalliq-hayat" / "04-bala-tughulush-ve-xetne.mdx",
        DOCS_DIR / "02-er-ayalliq-hayat" / "05-islah-ve-ijtimaiy-munasiwetler.mdx",
        DOCS_DIR / "03-ailining-buzulushi" / "01-buzulush-sewebliri-ve-talaq.mdx",
        DOCS_DIR / "03-ailining-buzulushi" / "02-talaq-turleri-ve-ehkamliri.mdx",
        DOCS_DIR / "03-ailining-buzulushi" / "03-talaqtin-keyinki-heqler-iddet.mdx",
        DOCS_DIR / "04-ata-anilar-heqqide" / "01-ata-anining-heqliri-ve-ulughluqi.mdx",
        DOCS_DIR / "04-ata-anilar-heqqide" / "02-ata-anigha-30-tewsiye-ve-gunahlar.mdx",
        DOCS_DIR / "05-balilar-heqqide" / "01-bala-terbiyisi-ve-heqliri.mdx",
        DOCS_DIR / "05-balilar-heqqide" / "02-aile-hayatigha-aitt-soal-jawablar.mdx",
    ]

    missing_files = [f for f in required_mdx_files if not f.exists()]
    if not missing_files:
        print(f"  [PASS] All {len(required_mdx_files)} required aile MDX files exist.")
        passed += 1
    else:
        print(f"  [FAIL] Missing MDX files: {missing_files}")
        failed += 1

    # Test 2: Public static assets
    required_assets = [
        PUBLIC_DIR / "islamdiki-aile-tuzumi.pdf",
        PUBLIC_DIR / "cover.png",
    ]
    missing_assets = [f for f in required_assets if not f.exists() or f.stat().st_size == 0]
    if not missing_assets:
        print(f"  [PASS] All {len(required_assets)} required static assets exist in public/aile/ (PDF: {required_assets[0].stat().st_size} bytes).")
        passed += 1
    else:
        print(f"  [FAIL] Missing static assets: {missing_assets}")
        failed += 1

    # Test 3: Index TOC links check
    index_content = (DOCS_DIR / "index.mdx").read_text(encoding="utf-8")
    toc_links = re.findall(r'href="([^"]+)"', index_content) + re.findall(r'link:\s*"([^"]+)"', index_content) + re.findall(r'\[.+?\]\((/aile/[^)]+)\)', index_content)
    broken_links = []

    for link in toc_links:
        if link.startswith("/aile/") and not link.endswith(".pdf"):
            rel_path = link.removeprefix("/aile/").strip("/")
            if not rel_path:
                continue
            target_mdx = DOCS_DIR / f"{rel_path}.mdx"
            if not target_mdx.exists():
                broken_links.append(f"Broken link {link} -> {target_mdx} not found")

    if not broken_links:
        print(f"  [PASS] All {len(toc_links)} navigation links in index.mdx resolve to valid MDX files.")
        passed += 1
    else:
        print(f"  [FAIL] Broken links found in index.mdx: {broken_links}")
        failed += 1

    # Test 4: Unicode presentation forms check
    presentation_forms = re.compile(r'[\uFB50-\uFDFF\uFE70-\uFEFF]')
    found_glyphs = 0
    for fpath in required_mdx_files:
        content = fpath.read_text(encoding="utf-8")
        # Allow legitimate ornate Quranic parentheses: ﴾ (U+FD3E) and ﴿ (U+FD3F)
        matches = [c for c in presentation_forms.findall(content) if c not in ('\ufd3e', '\ufd3f')]
        if matches:
            found_glyphs += len(matches)
            print(f"  [FAIL] Legacy presentation forms found in {fpath.name}: {len(matches)}")
            failed += 1

    if found_glyphs == 0:
        print("  [PASS] Zero legacy Arabic presentation forms (UEY compliance confirmed).")
        passed += 1

    # Test 5: Dist HTML files check
    html_files = list(DIST_DIR.rglob("index.html"))
    if len(html_files) == 18:
        print(f"  [PASS] All 18 HTML pages successfully compiled in dist/aile/.")
        passed += 1
    else:
        print(f"  [FAIL] Expected 18 compiled HTML files in dist/aile/, found {len(html_files)}.")
        failed += 1

    # Test 6: Uyghur Lam-Alif orthography check
    broken_la_words = []
    for fpath in required_mdx_files:
        content = fpath.read_text(encoding="utf-8")
        matches = re.findall(
            r'\b[ئا-ە]*?ئاال[ئا-ە]*?\b|'
            r'\b[ئا-ە]*?ھاالل[ئا-ە]*?\b|'
            r'\b[ئا-ە]*?ئىسالم[ئا-ە]*?\b|'
            r'\bباال[نىغاىڭدەتىمۋپ]*\b|'
            r'\b[ئا-ە]+?الر[\u0621-\u06FF]*\b|'
            r'\b[ئا-ە]+?الن(?:غان|مايدىغان|دۇر|ماقچى)[\u0621-\u06FF]*\b|'
            r'\bتاالق[\u0621-\u06FF]*\b|'
            r'\bئەۋالد[\u0621-\u06FF]*\b|'
            r'\bئىسالھ[\u0621-\u06FF]*\b|'
            r'\bئىپالس[\u0621-\u06FF]*\b|'
            r'\bتىالۋ[ئا-ە]*\b|'
            r'\bئېھتىالم[\u0621-\u06FF]*\b|'
            r'\bقاالق[\u0621-\u06FF]*\b|'
            r'\bقۋالق[\u0621-\u06FF]*\b|'
            r'\bدامۋلالم\b',
            content
        )
        if matches:
            broken_la_words.extend([(fpath.name, m) for m in matches])

    if not broken_la_words:
        print("  [PASS] Zero separated Lam-Alif words found across all Aile pages.")
        passed += 1
    else:
        print(f"  [FAIL] Found {len(broken_la_words)} separated Lam-Alif words: {broken_la_words[:5]}")
        failed += 1

    # Test 7: Arabic script integrity check (zero broken/reversed artifacts)
    arabic_artifacts = []
    for fpath in required_mdx_files:
        content = fpath.read_text(encoding="utf-8")
        matches = re.findall(r'معلص|ىلق', content)
        if matches:
            arabic_artifacts.extend([(fpath.name, m) for m in matches])

    if not arabic_artifacts:
        print("  [PASS] Zero broken Arabic ligature artifacts found (clean connected script confirmed).")
        passed += 1
    else:
        print(f"  [FAIL] Found {len(arabic_artifacts)} broken Arabic artifacts: {arabic_artifacts[:5]}")
        failed += 1

    # Test 8: Space around 'ى' and disconnected case/plural suffixes check
    space_y_artifacts = []
    for fpath in required_mdx_files:
        content = fpath.read_text(encoding="utf-8")
        for line in content.splitlines():
            if line.strip().startswith('>') or '﴿' in line:
                continue
            matches = re.findall(
                r'\b[\u0621-\u06FF]+ن[ \t]+ىڭ\b|'
                r'\b[\u0621-\u06FF]+[ \t]+نىڭ\b|'
                r'\b[\u0621-\u06FF]+[ \t]+نى\b|'
                r'\b[\u0621-\u06FF]+[ \t]+لىرى[\u0621-\u06FF]*\b|'
                r'\b[\u0621-\u06FF]+[ \t]+ىچىلىك\b|'
                r'\b(?:چ|ق|ك|د|ب|م)[ \t]+ى[\u0621-\u06FF]+\b',
                line
            )
            if matches:
                space_y_artifacts.extend([(fpath.name, m) for m in matches])

    if not space_y_artifacts:
        print("  [PASS] Zero separated 'ى' and disconnected suffix artifacts found across all Aile pages.")
        passed += 1
    else:
        print(f"  [FAIL] Found {len(space_y_artifacts)} separated 'ى'/suffix artifacts: {space_y_artifacts[:5]}")
        failed += 1

    print("==============================================================================")
    print(f" TOTAL: {passed} PASSED, {failed} FAILED")
    print("==============================================================================")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
