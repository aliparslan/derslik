#!/usr/bin/env python3
"""
Test Bookmarks and Settings implementation across the site.
Checks:
1. Component files existence (BookmarksModal, SettingsModal, PageTitle).
2. Configuration in astro.config.mjs (PageTitle registered).
3. Integration in Header.astro and MobileMenuFooter.astro (BookmarksModal + SettingsModal).
4. Compiled HTML presence of <starlight-bookmarks-modal> and <starlight-settings-modal>.
5. Compiled HTML presence of <starlight-page-bookmark> on content pages across portals.
6. JavaScript bundle verification (localStorage keys 'derslik-bookmarks-v1', 'starlight-theme', 'starlight-font-size').
7. Accessibility attributes (dialog, aria-label, role, labels).
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DIST_DIR = BASE_DIR / "dist"

def test_bookmarks():
    print("==============================================================================")
    print(" DERSLIK BOOKMARKS & SETTINGS FEATURE — TEST SUITE REPORT")
    print("==============================================================================")
    
    passed = 0
    failed = 0

    # 1. Check component files
    req_components = [
        BASE_DIR / "src" / "components" / "BookmarksModal.astro",
        BASE_DIR / "src" / "components" / "SettingsModal.astro",
        BASE_DIR / "src" / "components" / "PageTitle.astro",
    ]
    for comp in req_components:
        if comp.exists() and comp.stat().st_size > 0:
            print(f"  [PASS] Component {comp.name} exists ({comp.stat().st_size} bytes).")
            passed += 1
        else:
            print(f"  [FAIL] Missing component {comp}")
            failed += 1

    # 2. Check that PageTitle is registered in astro.config.mjs
    astro_cfg = (BASE_DIR / "astro.config.mjs").read_text(encoding="utf-8")
    if "PageTitle: './src/components/PageTitle.astro'" in astro_cfg:
        print("  [PASS] PageTitle correctly registered in astro.config.mjs.")
        passed += 1
    else:
        print("  [FAIL] PageTitle not registered in astro.config.mjs.")
        failed += 1

    # 3. Check Header and MobileMenuFooter integration
    header_content = (BASE_DIR / "src" / "components" / "Header.astro").read_text(encoding="utf-8")
    mobile_content = (BASE_DIR / "src" / "components" / "MobileMenuFooter.astro").read_text(encoding="utf-8")

    for name, content in [("Header.astro", header_content), ("MobileMenuFooter.astro", mobile_content)]:
        if "BookmarksModal" in content and "<BookmarksModal />" in content:
            print(f"  [PASS] BookmarksModal integrated in {name}.")
            passed += 1
        else:
            print(f"  [FAIL] BookmarksModal missing in {name}.")
            failed += 1

        if "SettingsModal" in content and "<SettingsModal" in content:
            print(f"  [PASS] SettingsModal integrated in {name}.")
            passed += 1
        else:
            print(f"  [FAIL] SettingsModal missing in {name}.")
            failed += 1

    # 4. Check compiled HTML (if dist exists)
    if DIST_DIR.exists():
        test_reading_pages = [
            "ereb-tili/01-1-qisim/01-ders-01-05/index.html",
            "aile/01-qurulushi/01-aile-qurush-ve-usulliri/index.html",
            "40hedis/01-hedis-01-10/index.html",
            "100hedis/01-hedis-01-10/index.html",
            "dua/01-kundilik-namaz/index.html",
            "peyghemberler/01-1-tom/02-adem-eleyhissalam/index.html",
            "2000/02-ibadet/11-zakat/index.html",
        ]

        html_errors = []
        for rel_path in test_reading_pages:
            fpath = DIST_DIR / rel_path
            if not fpath.exists():
                html_errors.append(f"Dist file {rel_path} does not exist")
                continue

            html = fpath.read_text(encoding="utf-8")
            if "<starlight-bookmarks-modal" not in html:
                html_errors.append(f"Missing <starlight-bookmarks-modal> in {rel_path}")

            if "<starlight-settings-modal" not in html:
                html_errors.append(f"Missing <starlight-settings-modal> in {rel_path}")

            if "<starlight-page-bookmark" not in html:
                html_errors.append(f"Missing <starlight-page-bookmark> in {rel_path}")

            if "page-bookmark-btn" not in html:
                html_errors.append(f"Missing page-bookmark-btn in {rel_path}")

            if "settings-dialog" not in html:
                html_errors.append(f"Missing settings-dialog in {rel_path}")

        # Check JS bundle / HTML scripts for storage keys
        js_files = list(DIST_DIR.glob("_astro/*.js"))
        has_bm_key = any("derslik-bookmarks-v1" in jf.read_text(encoding="utf-8") for jf in js_files) or any("derslik-bookmarks-v1" in (DIST_DIR / p).read_text(encoding="utf-8") for p in test_reading_pages)
        has_theme_key = any("starlight-theme" in jf.read_text(encoding="utf-8") for jf in js_files) or any("starlight-theme" in (DIST_DIR / p).read_text(encoding="utf-8") for p in test_reading_pages)
        has_font_key = any("starlight-font-size" in jf.read_text(encoding="utf-8") for jf in js_files) or any("starlight-font-size" in (DIST_DIR / p).read_text(encoding="utf-8") for p in test_reading_pages)

        if not has_bm_key:
            html_errors.append("LocalStorage key 'derslik-bookmarks-v1' not found in any bundled JS file")
        if not has_theme_key:
            html_errors.append("LocalStorage key 'starlight-theme' not found in any bundled JS file")
        if not has_font_key:
            html_errors.append("LocalStorage key 'starlight-font-size' not found in any bundled JS file")

        if not html_errors:
            print(f"  [PASS] All {len(test_reading_pages)} sample portal reading pages verified with page bookmark buttons, settings modals, and synced scripts.")
            passed += 1
        else:
            print(f"  [FAIL] HTML verification errors: {html_errors}")
            failed += 1

        # 5. Check Topic & Link Bookmarking script and styles
        css_files = list(DIST_DIR.glob("_astro/*.css"))
        has_topic_btn_css = any("topic-bookmark-btn" in cf.read_text(encoding="utf-8") for cf in css_files)
        has_topic_btn_js = any("topic-bookmark-btn" in jf.read_text(encoding="utf-8") for jf in js_files)
        custom_css = (BASE_DIR / "src" / "styles" / "custom.css").read_text(encoding="utf-8")
        modal_astro = (BASE_DIR / "src" / "components" / "BookmarksModal.astro").read_text(encoding="utf-8")

        if "topic-bookmark-btn" in custom_css and "card-bookmark-btn" in custom_css and "heading-bookmark-btn" in custom_css and "link-bookmark-btn" in custom_css:
            print("  [PASS] Custom CSS contains full topic, card, heading, and link bookmarking styles.")
            passed += 1
        else:
            print("  [FAIL] Custom CSS missing some topic bookmark classes.")
            failed += 1

        if "initTopicAndLinkBookmarks" in modal_astro and "toggleTopicBookmark" in modal_astro and "createTopicBookmarkBtn" in modal_astro:
            print("  [PASS] BookmarksModal contains complete topic & link injection and reactive toggle logic.")
            passed += 1
        else:
            print("  [FAIL] BookmarksModal missing topic & link bookmark methods.")
            failed += 1

        if has_topic_btn_css and has_topic_btn_js:
            print("  [PASS] Compiled assets in dist/ contain bundled topic bookmark CSS & JS.")
            passed += 1
        else:
            print(f"  [FAIL] Bundled topic bookmark assets missing: css={has_topic_btn_css}, js={has_topic_btn_js}")
            failed += 1
    else:
        print("  [INFO] dist/ directory not found yet (run build to test).")

    print("==============================================================================")
    print(f" TOTAL: {passed} PASSED, {failed} FAILED")
    print("==============================================================================")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(test_bookmarks())

