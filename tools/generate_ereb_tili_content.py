#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/generate_ereb_tili_content.py

Generates all 17 high-quality, fully detailed MDX pages for:
«ئەرەب تىلى دەرسلىكى گرامماتىكا قائىدىلىرى» (قواعد دروس اللغة العربية لغير الناطقين بها)
Author: دوكتۇر ف . ئابدۇرەھىم (Dr. V. Abdur Rahim)
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "src" / "content" / "docs" / "ereb-tili"

def write_mdx(rel_path, content):
    dest = DOCS_DIR / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated {dest} ({len(content)} chars)")

print("Generating ereb-tili portal MDX files...")
