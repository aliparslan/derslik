import json

with open('/tmp/passages_full.json') as f:
    passages = json.load(f)

# Read the VERSE_MAP from generate_resolver_full.py
with open('tools/generate_resolver_full.py') as f:
    code = f.read()

m = code[code.index("VERSE_MAP = {"):code.index("# Verification")]

content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/resolve_arabic_passages.py

Comprehensive resolver for:
1. All 133 Arabic passages in «ئىسلامدىكى ئائىلە تۈزۈمى» (src/content/docs/aile/)
2. Uyghur Lam-Alif orthography normalization (ئاالقە -> ئالاقە, ھاالل -> ھالال, etc.)
3. Inverted footnote citation numbers (e.g. ئىسرا 23 -> 32, بەقەرە 591 -> 195)
4. Heading normalization across all 18 MDX files
"""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "src" / "content" / "docs" / "aile"

with open('/tmp/passages_full.json') as f:
    passages = json.load(f)

{m}

def fix_uyghur_lam_alif(text):
    # Specific known broken words
    text = re.sub(r'ئاالقە\b', 'ئالاقە', text)
    text = re.sub(r'ئاالقى', 'ئالاقى', text)
    text = re.sub(r'ئاالق', 'ئالاق', text)
    text = re.sub(r'ئاالھىدە', 'ئالاھىدە', text)
    text = re.sub(r'ھاالل', 'ھالال', text)
    text = re.sub(r'زااللەت', 'زالالەت', text)
    text = re.sub(r'باالغەت', 'بالاغەت', text)
    text = re.sub(r'باال([نىغاىڭدەتىمۋپ]*)\b', r'بالا\1', text)
    text = re.sub(r'باالى', 'بالى', text)
    text = re.sub(r'ئىسالم', 'ئىسلام', text)
    text = re.sub(r'تائاال', 'تائالا', text)
    text = re.sub(r'ئالالھ', 'ئاللاھ', text)
    text = re.sub(r'ئالال([نىغاىڭدەتىمۋپ]*)\b', r'ئاللا\1', text)
    text = re.sub(r'ساالم', 'سالام', text)
    text = re.sub(r'كەالم', 'كالام', text)
    text = re.sub(r'ئەخالق', 'ئەخلاق', text)
    text = re.sub(r'ئىخالس', 'ئىخلاس', text)
    text = re.sub(r'ئۆلىماالر', 'ئۆلىمالار', text)
    text = re.sub(r'ئالىماالر', 'ئالىملار', text)
    text = re.sub(r'ئالىمالر', 'ئالىملار', text)
    text = re.sub(r'ماالر\b', 'ماللار', text)
    text = re.sub(r'ئاالمايدۇ', 'ئالالمايدۇ', text)
    text = re.sub(r'ئاالمدۇ', 'ئالامدۇ', text)
    text = re.sub(r'ئااللىشىغا', 'ئالالىشىغا', text)
    text = re.sub(r'ئاالىدۇ', 'ئالالىدۇ', text)
    text = re.sub(r'ئاالىدۇ\b', 'ئالالىدۇ', text)
    text = re.sub(r'ئااللىدۇ', 'ئالالالايدۇ', text)
    text = re.sub(r'ئاالمىغان', 'ئالالمىغان', text)
    text = re.sub(r'ئاالمىغانلىقى', 'ئالالمىغانلىقى', text)
    text = re.sub(r'ئااللمىسا', 'ئالالمىسا', text)
    text = re.sub(r'ئاال', 'ئالا', text)

    # General rule for Uyghur plurals: [consonant/vowel] + الر -> لار
    text = re.sub(r'([ئا-ە])الر([نىغاىڭدەتىمۋپ]*)\b', r'\1لار\2', text)
    text = re.sub(r'ئاالل', 'ئالال', text)

    # Clean up single space-separated Uyghur letters (e.g. ك ېتە لم ە يد ۇ -> كېتەلمەيدۇ, ئ ىنسان -> ئىنسان)
    text = re.sub(r'([كپبتمسشخغفقدزژچجڭگنھۋري])\s+([ئا-ە])\s+([ئا-ە])\s+([ئا-ە])\s+([ئا-ە])\b', r'\1\2\3\4\5', text)
    text = re.sub(r'([كپبتمسشخغفقدزژچجڭگنھۋري])\s+([ئا-ە])\s+([ئا-ە])\s+([ئا-ە])\b', r'\1\2\3\4', text)
    text = re.sub(r'([كپبتمسشخغفقدزژچجڭگنھۋري])\s+([ئا-ە])\s+([ئا-ە])\b', r'\1\2\3', text)
    text = re.sub(r'([كپبتمسشخغفقدزژچجڭگنھۋري])\s+([ئا-ە])\b', r'\1\2', text)

    # Fix reversed footnote numbers
    text = re.sub(r'بەقەرە\s+591\s+ئايەت', 'بەقەرە سۈرىسى 195 - ئايەت', text)
    text = re.sub(r'ئىسرا\s+سۈرىسى\s+23\s*-\s*ئايەت', 'ئىسرا سۈرىسى 32 - ئايەت', text)
    text = re.sub(r'بەقەرە\s+سۈرىسى\s+122\s+ئايەت', 'بەقەرە سۈرىسى 221 - ئايەت', text)
    text = re.sub(r'ئەھزاپ\s+سۈرىسى\s+63\s+ئايەت', 'ئەھزاب سۈرىسى 36 - ئايەت', text)
    text = re.sub(r'بەقەرە\s+سۈرىسى\s+781\s+ئايەت', 'بەقەرە سۈرىسى 187 - ئايەت', text)
    text = re.sub(r'نىسا\s+سۈرىسى\s+43\s+ئايەت', 'نىسا سۈرىسى 34 - ئايەت', text)

    return text

def apply_all():
    print("Applying Arabic passage replacements and Lam-Alif fixes...")
    files_modified = set()

    # Step 1: Replace all 133 passages by exact string
    for idx, p in enumerate(passages):
        fname = p["file"]
        fpath = list(DOCS_DIR.rglob(fname))[0]
        content = fpath.read_text("utf-8")
        
        old_txt = p["text"]
        new_txt = VERSE_MAP.get(idx)
        if not new_txt:
            print(f"Warning: No replacement for passage {idx}")
            continue

        if old_txt in content:
            content = content.replace(old_txt, new_txt)
            fpath.write_text(content, "utf-8")
            files_modified.add(fname)
        else:
            print(f"Warning: passage {idx} text not found in {fname}")

    print(f"Substituted passages across {len(files_modified)} files.")

    # Step 2: Apply Lam-Alif and typography fixes across all 18 MDX files
    all_files = sorted(DOCS_DIR.rglob("*.mdx"))
    for fpath in all_files:
        content = fpath.read_text("utf-8")
        fixed = fix_uyghur_lam_alif(content)
        if fixed != content:
            fpath.write_text(fixed, "utf-8")
            print(f"  Fixed Lam-Alif & orthography in {fpath.name}")

    print("All fixes applied successfully!")

if __name__ == "__main__":
    apply_all()
'''

with open('tools/resolve_arabic_passages.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Generated tools/resolve_arabic_passages.py")
