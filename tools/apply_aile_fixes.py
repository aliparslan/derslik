#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "src" / "content" / "docs" / "aile"

with open('/tmp/verse_map.json', encoding='utf-8') as f:
    verse_map = json.load(f)

with open('/tmp/passages_full.json', encoding='utf-8') as f:
    passages = json.load(f)

def fix_uyghur_lam_alif(text):
    # 1. Known words with separated / inverted Lam-Alif
    text = re.sub(r'ئىسالم', 'ئىسلام', text)
    text = re.sub(r'ھاالل', 'ھالال', text)
    text = re.sub(r'ئاالق', 'ئالاق', text)
    text = re.sub(r'ئاالھىدە', 'ئالاھىدە', text)
    text = re.sub(r'باالغەت', 'بالاغەت', text)
    text = re.sub(r'باال', 'بالا', text)
    text = re.sub(r'ساالم', 'سالام', text)
    text = re.sub(r'كەالم', 'كالام', text)
    text = re.sub(r'ئەخالق', 'ئەخلاق', text)
    text = re.sub(r'ئىخالس', 'ئىخلاس', text)
    text = re.sub(r'ئىسلاھ', 'ئىسلاھ', text)
    text = re.sub(r'ئېسالھ', 'ئىسلاھ', text)
    text = re.sub(r'ئۆلىماالر', 'ئۆلىمالار', text)
    text = re.sub(r'ئالىماالر', 'ئالىملار', text)
    text = re.sub(r'ئالىمالر', 'ئالىملار', text)
    text = re.sub(r'ماالر\b', 'ماللار', text)
    text = re.sub(r'تائاال', 'تائالا', text)
    text = re.sub(r'ئالالھ', 'ئاللاھ', text)
    text = re.sub(r'ئالال', 'ئاللا', text)
    text = re.sub(r'زااللەت', 'زالالەت', text)
    text = re.sub(r'ئاالمايدۇ', 'ئالالمايدۇ', text)
    text = re.sub(r'ئاالمدۇ', 'ئالامدۇ', text)
    text = re.sub(r'ئااللىشىغا', 'ئالالىشىغا', text)
    text = re.sub(r'ئاالىدۇ', 'ئالالىدۇ', text)
    text = re.sub(r'ئاالمىغان', 'ئالالمىغان', text)
    text = re.sub(r'ئااللمىسا', 'ئالالمىسا', text)
    text = re.sub(r'ئاال', 'ئالا', text)

    # 2. Plural suffix: word ending in [consonant/vowel] + الر -> [consonant/vowel] + لار
    text = re.sub(r'([ئا-ە])الر([نىغاىڭدەتىمۋپ]*)\b', r'\1لار\2', text)
    text = re.sub(r'ئاالل', 'ئالال', text)

    # 3. Join separated letters
    text = re.sub(r'([كپبتمسشخغفقدزژچجڭگنھۋري])\s+([ئا-ە])\s+([ئا-ە])\s+([ئا-ە])\s+([ئا-ە])\b', r'\1\2\3\4\5', text)
    text = re.sub(r'([كپبتمسشخغفقدزژچجڭگنھۋري])\s+([ئا-ە])\s+([ئا-ە])\s+([ئا-ە])\b', r'\1\2\3\4', text)
    text = re.sub(r'([كپبتمسشخغفقدزژچجڭگنھۋري])\s+([ئا-ە])\s+([ئا-ە])\b', r'\1\2\3', text)
    text = re.sub(r'([كپبتمسشخغفقدزژچجڭگنھۋري])\s+([ئا-ە])\b', r'\1\2', text)

    # 4. Footnote citations with reversed numbers
    text = re.sub(r'بەقەرە\s+591\s+ئايەت', 'بەقەرە سۈرىسى 195 - ئايەت', text)
    text = re.sub(r'ئىسرا\s+سۈرىسى\s+23\s*-\s*ئايەت', 'ئىسرا سۈرىسى 32 - ئايەت', text)
    text = re.sub(r'بەقەرە\s+سۈرىسى\s+122\s+ئايەت', 'بەقەرە سۈرىسى 221 - ئايەت', text)
    text = re.sub(r'ئەھزاپ\s+سۈرىسى\s+63\s+ئايەت', 'ئەھزاب سۈرىسى 36 - ئايەت', text)
    text = re.sub(r'بەقەرە\s+سۈرىسى\s+781\s+ئايەت', 'بەقەرە سۈرىسى 187 - ئايەت', text)
    text = re.sub(r'نىسا\s+سۈرىسى\s+43\s+ئايەت', 'نىسا سۈرىسى 34 - ئايەت', text)

    return text

def run():
    print("Starting full replacement run...")
    # Step 1: Replace all 133 passages by exact string
    passages_replaced = 0
    for idx, p in enumerate(passages):
        fname = p["file"]
        matches = list(DOCS_DIR.rglob(fname))
        if not matches:
            continue
        fpath = matches[0]
        content = fpath.read_text("utf-8")
        
        old_txt = p["text"]
        new_txt = verse_map.get(str(idx))
        if not new_txt:
            continue

        if old_txt in content:
            content = content.replace(old_txt, new_txt)
            fpath.write_text(content, "utf-8")
            passages_replaced += 1

    print(f"Passages replaced: {passages_replaced} / {len(passages)}")

    # Step 2: Apply Lam-Alif and typography fixes
    all_files = sorted(DOCS_DIR.rglob("*.mdx"))
    for fpath in all_files:
        content = fpath.read_text("utf-8")
        fixed = fix_uyghur_lam_alif(content)
        if fixed != content:
            fpath.write_text(fixed, "utf-8")
            print(f"  Applied fixes to {fpath.name}")

    print("Complete!")

if __name__ == "__main__":
    run()
