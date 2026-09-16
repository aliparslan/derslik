#!/usr/bin/env python3
"""
Generate Section 01 MDX files for 2000 Sualliq.
Produces exactly 8 MDX files in src/content/docs/2000/01-etiqad/
from tools/extracted_2000.json.
"""

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "tools" / "extracted_2000.json"
TARGET_DIR = ROOT / "src" / "content" / "docs" / "2000" / "01-etiqad"

FILES_CONFIG = [
    {
        "filename": "01-din-ve-etiqad.mdx",
        "title": "دىن ۋە ئىنسان",
        "description": "دىن ۋە ئىنسان — سوئال 1–20",
        "order": 1,
        "q_start": 1,
        "q_end": 20,
    },
    {
        "filename": "02-allahqa-iman.mdx",
        "title": "ئاللاھقا ئىمان كەلتۈرۈش",
        "description": "ئاللاھقا ئىمان كەلتۈرۈش — سوئال 21–48",
        "order": 2,
        "q_start": 21,
        "q_end": 48,
    },
    {
        "filename": "03-allahning-isimliri.mdx",
        "title": "ئاللاھنىڭ گۈزەل ئىسىملىرى ۋە سۈپەتلىرى",
        "description": "ئاللاھنىڭ گۈزەل ئىسىملىرى ۋە سۈپەتلىرى — سوئال 49–62",
        "order": 3,
        "q_start": 49,
        "q_end": 62,
        "include_99_names": True,
    },
    {
        "filename": "04-perishtiler-jinlar.mdx",
        "title": "پەرىشتىلەر، جىنلار ۋە شەيتانلار",
        "description": "پەرىشتىلەر، جىنلار ۋە شەيتانلار — سوئال 63–82",
        "order": 4,
        "q_start": 63,
        "q_end": 82,
    },
    {
        "filename": "05-samawiy-kitablar.mdx",
        "title": "ساماۋىي كىتابلار ۋە قۇرئان كەرىم",
        "description": "ساماۋىي كىتابلار ۋە قۇرئان كەرىم — سوئال 83–96",
        "order": 5,
        "q_start": 83,
        "q_end": 96,
    },
    {
        "filename": "06-peyghamberler.mdx",
        "title": "پەيغەمبەرلەرگە ئىمان كەلتۈرۈش",
        "description": "پەيغەمبەرلەرگە ئىمان كەلتۈرۈش — سوئال 97–115",
        "order": 6,
        "q_start": 97,
        "q_end": 115,
    },
    {
        "filename": "07-qada-qeder.mdx",
        "title": "قازا ۋە قەدەرگە ئىمان",
        "description": "قازا ۋە قەدەرگە ئىمان — سوئال 116–134",
        "order": 7,
        "q_start": 116,
        "q_end": 134,
    },
    {
        "filename": "08-qiyamet-axiret.mdx",
        "title": "قىيامەت ۋە ئاخىرەتكە ئىمان",
        "description": "قىيامەت ۋە ئاخىرەتكە ئىمان — سوئال 135–163",
        "order": 8,
        "q_start": 135,
        "q_end": 163,
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


def build_99_names_table(names_99: list) -> str:
    lines = [
        "## ئاللاھ تائالانىڭ 99 گۈزەل ئىسمى (ئەسمائۇل ھۇسنا)",
        "",
        "| ئەرەبچە نامى | ئۇيغۇرچە ئوقۇلۇشى | مەنىسى |",
        "| :--- | :--- | :--- |",
    ]
    for item in names_99:
        arabic = clean_uyghur_text(item["arabic"]).replace("|", "/")
        translit = clean_uyghur_text(item["transliteration"]).replace("|", "/")
        meaning = clean_uyghur_text(item["meaning"]).replace("|", "/")
        lines.append(f"| {arabic} | {translit} | {meaning} |")
    lines.append("")
    return "\n".join(lines)


def main():
    print(f"Loading {JSON_PATH}...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions_by_num = {q["number"]: q for q in data["questions"]}
    names_99 = data["names_99"]

    print(f"Total questions in JSON: {len(questions_by_num)}")
    print(f"Total names in names_99: {len(names_99)}")

    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Clean up obsolete files in TARGET_DIR
    valid_filenames = {cfg["filename"] for cfg in FILES_CONFIG}
    existing_files = list(TARGET_DIR.glob("*.mdx")) + list(TARGET_DIR.glob("*.md"))
    for f in existing_files:
        if f.name not in valid_filenames:
            print(f"Deleting obsolete file: {f.name}")
            f.unlink()

    # 2. Generate each of the 8 MDX files
    for cfg in FILES_CONFIG:
        filename = cfg["filename"]
        title = cfg["title"]
        description = cfg["description"]
        order = cfg["order"]
        q_start = cfg["q_start"]
        q_end = cfg["q_end"]
        include_99_names = cfg.get("include_99_names", False)

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

        if include_99_names:
            content_parts.append(build_99_names_table(names_99))

        for num in range(q_start, q_end + 1):
            if num not in questions_by_num:
                print(f"ERROR: Missing question {num}!", file=sys.stderr)
                sys.exit(1)
            q = questions_by_num[num]
            content_parts.append(build_card(q))
            content_parts.append("")

        file_path = TARGET_DIR / filename
        file_content = "\n".join(content_parts)
        file_path.write_text(file_content, encoding="utf-8")
        print(f"Generated {filename} (Q{q_start}–{q_end}, size: {len(file_content)} bytes)")

    # 3. Verify exactly 8 files exist
    final_files = sorted([f.name for f in TARGET_DIR.glob("*.mdx")] + [f.name for f in TARGET_DIR.glob("*.md")])
    print(f"Total files in {TARGET_DIR}: {len(final_files)}")
    print("Files:", final_files)
    assert len(final_files) == 8, f"Expected 8 files, found {len(final_files)}"
    print("Generation complete and verified!")


if __name__ == "__main__":
    main()
