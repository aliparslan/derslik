#!/usr/bin/env python3
"""
Generate Section 02 MDX files (07 through 14) for 2000 Sualliq (Q333–Q647),
and remove obsolete skeleton files in 01-etiqad.
"""

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "tools" / "extracted_2000.json"
ETIQAD_DIR = ROOT / "src" / "content" / "docs" / "2000" / "01-etiqad"
IBADET_DIR = ROOT / "src" / "content" / "docs" / "2000" / "02-ibadet"

# Task 1: Obsolete files to delete from 01-etiqad
OBSOLETE_ETIQAD_FILES = [
    "04-rohiy-alemler.mdx",
    "05-kitablar-peyghemberler.mdx",
    "06-qaza-qeder.mdx",
    "07-qiyamet-axiret.mdx",
]

# Task 2: Config for files 07 through 14 in 02-ibadet
FILES_CONFIG_IBADET = [
    {
        "filename": "07-namaz-oqush.mdx",
        "title": "ناماز ئوقۇش تەرتىبى",
        "description": "ناماز ئوقۇش تەرتىبى — سوئال 333–393",
        "order": 7,
        "q_start": 333,
        "q_end": 393,
    },
    {
        "filename": "08-jamaet-jume.mdx",
        "title": "جامائەت ۋە جۈمە نامازى",
        "description": "جامائەت ۋە جۈمە نامازى — سوئال 394–428",
        "order": 8,
        "q_start": 394,
        "q_end": 428,
    },
    {
        "filename": "09-bashqa-namazlar.mdx",
        "title": "باشقا نامازلار",
        "description": "باشقا نامازلار — سوئال 429–477",
        "order": 9,
        "q_start": 429,
        "q_end": 477,
    },
    {
        "filename": "10-jinaze-depne.mdx",
        "title": "جىنازە ۋە دەپنە",
        "description": "جىنازە ۋە دەپنە — سوئال 478–506",
        "order": 10,
        "q_start": 478,
        "q_end": 506,
    },
    {
        "filename": "11-zakat.mdx",
        "title": "زاكات ئەھكاملىرى",
        "description": "زاكات ئەھكاملىرى — سوئال 507–553",
        "order": 11,
        "q_start": 507,
        "q_end": 553,
    },
    {
        "filename": "12-roza-ramizan.mdx",
        "title": "روزا ۋە رامىزان",
        "description": "روزا ۋە رامىزان — سوئال 554–607",
        "order": 12,
        "q_start": 554,
        "q_end": 607,
    },
    {
        "filename": "13-hej-omre.mdx",
        "title": "ھەج ۋە ئۈمرە",
        "description": "ھەج ۋە ئۈمرە — سوئال 608–634",
        "order": 13,
        "q_start": 608,
        "q_end": 634,
    },
    {
        "filename": "14-sawab-gunah.mdx",
        "title": "ساۋاب ۋە گۇناھ",
        "description": "ساۋاب ۋە گۇناھ — سوئال 635–647",
        "order": 14,
        "q_start": 635,
        "q_end": 647,
    },
]


def clean_uyghur_text(text: str) -> str:
    """Normalize legacy Uyghur glyphs and strip interior tatweels."""
    if not text:
        return ""
    # Normalize legacy glyphs
    text = text.replace("\u066e", "\u0649")  # dotless beh -> standard Uyghur ى
    text = text.replace("\u067b", "\u06d0")  # beeh with 2 vertical dots -> standard Uyghur ې
    text = text.replace("\u06cc", "\u064a")  # Farsi yeh -> standard Uyghur ي
    # Strip tatweels between letters
    text = re.sub(r"([\u0621-\u064a\u0671-\u06d3\u06d5])\u0640+([\u0621-\u064a\u0671-\u06d3\u06d5])", r"\1\2", text)
    return text.strip()


def build_card(q: dict) -> str:
    number = q["number"]
    question = clean_uyghur_text(q["question"])
    answer = clean_uyghur_text(q["answer"])

    # If footnotes exist, append them nicely inside answer
    footnotes = q.get("footnotes", [])
    fn_html = ""
    if footnotes:
        clean_fns = [clean_uyghur_text(fn) for fn in footnotes if fn]
        if clean_fns:
            fn_items = " ".join(f"<span>[{fn}]</span>" for fn in clean_fns)
            fn_html = f'\n    <div class="qa-footnotes" style="margin-top: 0.75rem; font-size: 0.85rem; opacity: 0.8;">{fn_items}</div>'

    card = f"""<div class="qa-card" id="q{number}">
  <div class="qa-question">
    <span class="qa-number">{number}</span>
    <span class="qa-label">سوئال:</span> {question}
  </div>
  <div class="qa-answer">
    <span class="qa-label">جاۋاب:</span> {answer}{fn_html}
  </div>
</div>"""
    return card


def clean_obsolete_etiqad():
    print("Cleaning obsolete files in 01-etiqad...")
    for filename in OBSOLETE_ETIQAD_FILES:
        target = ETIQAD_DIR / filename
        if target.exists():
            target.unlink()
            print(f"Deleted obsolete file: {target}")
        else:
            print(f"File already absent: {target}")

    # Check remaining files in 01-etiqad
    files = sorted([f.name for f in ETIQAD_DIR.glob("*.md*")])
    print(f"Remaining files in 01-etiqad ({len(files)}): {files}")
    assert len(files) == 8, f"Expected exactly 8 canonical files in 01-etiqad, found {len(files)}"


def generate_ibadet_files():
    print(f"Loading {JSON_PATH}...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions_by_num = {q["number"]: q for q in data["questions"]}
    print(f"Loaded {len(questions_by_num)} questions from JSON.")

    IBADET_DIR.mkdir(parents=True, exist_ok=True)

    for cfg in FILES_CONFIG_IBADET:
        filename = cfg["filename"]
        title = cfg["title"]
        description = cfg["description"]
        order = cfg["order"]
        q_start = cfg["q_start"]
        q_end = cfg["q_end"]

        content_parts = [
            "---",
            f'title: "{title}"',
            f'description: "{description}"',
            "sidebar:",
            f'  label: "{title}"',
            f"  order: {order}",
            "---",
            "",
        ]

        for num in range(q_start, q_end + 1):
            if num not in questions_by_num:
                print(f"ERROR: Missing question {num} in JSON!", file=sys.stderr)
                sys.exit(1)
            q = questions_by_num[num]
            content_parts.append(build_card(q))
            content_parts.append("")

        file_path = IBADET_DIR / filename
        file_content = "\n".join(content_parts)
        file_path.write_text(file_content, encoding="utf-8")
        print(f"Generated {filename} (Q{q_start}–{q_end}, {len(file_content)} bytes)")

    # Verify all 14 files exist in 02-ibadet
    all_ibadet_files = sorted([f.name for f in IBADET_DIR.glob("*.md*")])
    print(f"Total files in 02-ibadet ({len(all_ibadet_files)}): {all_ibadet_files}")
    assert len(all_ibadet_files) == 14, f"Expected 14 files, found {len(all_ibadet_files)}"


def main():
    clean_obsolete_etiqad()
    generate_ibadet_files()
    print("Done!")


if __name__ == "__main__":
    main()
