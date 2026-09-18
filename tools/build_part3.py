#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tools/build_part3.py

Generates all 6 MDX files for Part 3 of «ئەرەب تىلى دەرسلىكى گرامماتىكا قائىدىلىرى»:
1. 01-muqeddimu.mdx: Part 3 Grammar Intro (المعرب والمبني، الإعراب الأصلي والفرعي، التقديري، المرفوعات، المنصوبات، المجرورات، التوابع، إعراب الأفعال)
2. 02-ders-01-08.mdx: Lessons 1-8 (واو الحال، اسم الفعل، المبني للمجهول ونائب الفاعل، اسم الفاعل والمفعول، اسم الزمان والمكان والآلة، المعرفة والنكرة، النسبة)
3. 03-ders-09-16.mdx: Lessons 9-16 (أفعال الشروع، المبتدأ والخبر، مفعول فيه، جوازم المضارع وجواب الطلب، أدوات الشرط، أبواب الثلاثي المجرد 6، ما وأنواعها)
4. 04-ders-17-24.mdx: Lessons 17-24 (أبواب الثلاثي المزيد التسعة: أفعل، فعّل، فاعل، تفعّل، تفاعل، انفعل، افتعل، افعلّ، استفعل، معانيها وإعرابها)
5. 05-ders-25-32.mdx: Lessons 25-32 (الفعل الرباعي، ضمير الفصل، المفعول المطلق والمصدر الميمي، المفعول لأجله، التمييز والتعجب، الحال، الاستثناء، نون التوكيد)
6. 06-xatime.mdx: Khatimah (الممنوع من الصرف وأحكامه، أوزان المصادر 27 للثلاثي المجرد، جموع التكسير أوزان القلة والكثرة ومنتهى الجموع)
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "src" / "content" / "docs" / "ereb-tili" / "03-3-qisim"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

def write_file(name, content):
    p = DOCS_DIR / name
    p.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Created {p} ({len(content)} chars)")

print("Generating Part 3 files...")
