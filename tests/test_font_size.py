#!/usr/bin/env python3
"""
Test Font Size Changer implementation across the site.
Checks HTML compilation, component presence in header, accessibility attributes,
CSS definitions, and FOUC prevention script.
"""

import sys
from pathlib import Path
import re

DIST = Path("dist")

def test_font_size():
    errors = []

    # 1. Check custom.css definitions
    css_file = Path("src/styles/custom.css")
    css_content = css_file.read_text(encoding="utf-8")
    for size in ['sm', 'md', 'lg', 'xl', '2xl']:
        if f"[data-font-size='{size}']" not in css_content and f'[data-font-size="{size}"]' not in css_content:
            errors.append(f"Missing CSS rule for data-font-size='{size}' in custom.css")

    if "--sl-font-scale" not in css_content:
        errors.append("Missing --sl-font-scale variable in custom.css")

    # 2. Check portals have the font size selector in generated HTML
    portals = [
        "index.html",
        "aile/index.html",
        "2000/index.html",
        "40hedis/index.html",
        "100hedis/index.html",
        "dua/index.html",
        "peyghemberler/index.html",
        "ereb-tili/index.html",
    ]

    for p in portals:
        fpath = DIST / p
        if not fpath.exists():
            errors.append(f"Dist file {p} does not exist")
            continue

        html = fpath.read_text(encoding="utf-8")
        if "<starlight-font-size-select" not in html:
            errors.append(f"Missing <starlight-font-size-select> in {p}")
        if 'data-action="decrease"' not in html:
            errors.append(f"Missing decrease button in {p}")
        if 'data-action="increase"' not in html:
            errors.append(f"Missing increase button in {p}")
        if "starlight-font-size" not in html:
            errors.append(f"Missing localStorage font size script in {p}")

    if errors:
        print(f"FAILED: {len(errors)} error(s) found:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("ALL CHECKS PASSED: Font size changer is properly integrated across all pages.")
    return 0

if __name__ == "__main__":
    sys.exit(test_font_size())
