#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path
import fitz

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = PROJECT_ROOT / "public" / "namaz" / "namazdin-sawat.pdf"
DOCS_DIR = PROJECT_ROOT / "src" / "content" / "docs" / "namaz"

doc = fitz.open(str(PDF_PATH))

def normalize_text(text: str) -> str:
    text = text.replace('\u0640', '') # strip tatweel
    text = re.sub(r'[ \t]+', ' ', text)

    # Broken spaces in common words
    text = re.sub(r'ئال\s+لاھ', 'ئاللاھ', text)
    text = re.sub(r'ئىس\s+لام', 'ئىسلام', text)
    text = re.sub(r'ئىخ\s+لاس', 'ئىخلاس', text)
    text = re.sub(r'ماختاش\s+لار', 'ماختاشلار', text)
    text = re.sub(r'مىكروب\s+لار', 'مىكروبلار', text)
    text = re.sub(r'ئىش\s+لار', 'ئىشلار', text)
    text = re.sub(r'ھاجەت\s+خانا', 'ھاجەتخانا', text)
    text = re.sub(r'تەن\s+ھەرىكەت', 'تەنھەرىكەت', text)
    text = re.sub(r'ئال\s+لىنىپ', 'ئالىنىپ', text)
    text = re.sub(r'قىيام\s+ەت', 'قىيامەت', text)
    text = re.sub(r'ئەھمىيەت\s+لىك', 'ئەھمىيەتلىك', text)
    text = re.sub(r'مۇسۇلمان\s+لار', 'مۇسۇلمانلار', text)

    specific_reps = [
        (r'ئالالھ', 'ئاللاھ'),
        (r'ئىسالم', 'ئىسلام'),
        (r'ئېالن', 'ئېلان'),
        (r'ئىخالس', 'ئىخلاس'),
        (r'ساالم', 'سالام'),
        (r'باالغەت', 'بالاغەت'),
        (r'باال', 'بالا'),
        (r'ئىالھ', 'ئىلاھ'),
        (r'تىالۋەت', 'تىلاۋەت'),
        (r'ئىختىالپ', 'ئىختىلاپ'),
        (r'پىالستىنكا', 'پلاستىنكا'),
        (r'ئاالھىدە', 'ئالاھىدە'),
        (r'ئاالقىدار', 'ئالاقىدار'),
        (r'ئاالمىتى', 'ئالامىتى'),
        (r'ئاالھىدىلىكى', 'ئالاھىدىلىكى'),
        (r'تائاال', 'تائالا'),
        (r'زااللەت', 'زالالەت'),
        (r'قۇالق', 'قۇلاق'),
        (r'قۇالقنى', 'قۇلاقنى'),
        (r'قۇالقنىڭ', 'قۇلاقنىڭ'),
        (r'قۇالقلار', 'قۇلاقلار'),
        (r'قۇالقالر', 'قۇلاقلار'),
        (r'ئۇالر', 'ئۇلار'),
        (r'ئايالالر', 'ئاياللار'),
        (r'مۇسۇلمانالر', 'مۇسۇلمانلار'),
        (r'ماددىالر', 'ماددىلار'),
        (r'ئىشالر', 'ئىشلار'),
        (r'ھالالر', 'ھاللار'),
        (r'ئۆزۈرالر', 'ئۆزۈرلەر'),
        (r'ئالىمالر', 'ئالىملار'),
        (r'ئۆلىماالر', 'ئۆلىمالار'),
        (r'ساھابىالر', 'ساھابىلار'),
        (r'سەۋەبالر', 'سەۋەبلەر'),
        (r'گۇناھالر', 'گۇناھلار'),
        (r'خاتالىقالر', 'خاتالىقلار'),
        (r'نۇقسانالر', 'نۇقسانلار'),
        (r'دۇئاالر', 'دۇئالار'),
        (r'جايلىالر', 'جايلار'),
        (r'جايالر', 'جايلار'),
        (r'پۇتالر', 'پۇتلار'),
        (r'قولالر', 'قوللار'),
        (r'تىزالر', 'تىزلار'),
        (r'ئورۇنالر', 'ئورۇنلار'),
        (r'يولۇچىالر', 'يولۇچىلار'),
        (r'مۇقىمالر', 'مۇقىملار'),
        (r'كاپىرالر', 'كاپىرلار'),
        (r'ساراڭالر', 'ساراڭلار'),
        (r'ئاڭلىغۇچىالر', 'ئاڭلىغۇچىلار'),
        (r'ئوقۇغۇچىالر', 'ئوقۇغۇچىلار'),
        (r'باشقىالر', 'باشقىلار'),
        (r'مەزھەپالر', 'مەزھەپلەر'),
        (r'رەكئەتالر', 'رەكئەتلەر'),
        (r'ۋاقىتالر', 'ۋاقىتلار'),
        (r'سائەتالر', 'سائەتلەر'),
        (r'سەجدەالر', 'سەجدىلەر'),
        (r'ئايەتالر', 'ئايەتلەر'),
        (r'سۈرەالر', 'سۈرىلەر'),
        (r'پەرزالر', 'پەرزلەر'),
        (r'ۋاجىپالر', 'ۋاجىپلار'),
        (r'سۈننەتالر', 'سۈننەتلەر'),
        (r'كىتابالر', 'كىتابلار'),
        (r'ژۇرنالالر', 'ژۇرناللار'),
        (r'ۋاراقالر', 'ۋاراقلار'),
        (r'كۆزالر', 'كۆزلەر'),
        (r'ھايۋانالر', 'ھايۋانلار'),
        (r'قورالالر', 'قوراللار'),
        (r'ئوقۇيالمىغانالر', 'ئوقۇيالمىغانلار'),
        (r'قىلغانالر', 'قىلغانلار'),
        (r'كەلگەنالر', 'كەلگەنلەر'),
        (r'بولغانالر', 'بولغانلار'),
        (r'ئېيتقانالر', 'ئېيتقانلار'),
        (r'سـاۋابالر', 'ساۋابلار'),
        (r'يويىمىز', 'يۇيىمىز'),
        (r'ئوشىقى', 'ئوشۇقى'),
        (r'ئاپىيىتى', 'ئافىيىتى'),
        (r'پۇرشىلىق', 'چوتكىلىق'),
        (r'دۇرۇتى', 'دۇرۇدى'),
        (r'رەزىيەلالھۇ', 'رەزىيەللاھۇ'),
        (r'ئەلەيھىسسـاالم', 'ئەلەيھىسسالام'),
        (r'ئەلەيھىسساالم', 'ئەلەيھىسسالام'),
        (r'ئەلەيھسساالم', 'ئەلەيھىسسالام'),
        (r'ئەئۇزۇ بىلالھى', 'ئەئۇزۇ بىللاھى'),
        (r'بىسمىلالھىر', 'بىسمىللاھىر'),
        (r'بىسملالھ', 'بىسمىللاھ'),
        (r'سۇبھانەلالھ', 'سۇبھاناللاھ'),
        (r'ئەلھەمدۇ لىللاھ', 'ئەلھەمدۇلىللاھ'),
        (r'ئەلھەمدۇلىلالھ', 'ئەلھەمدۇلىللاھ'),
        (r'ئاللاھۇ ئەكبەر', 'ئاللاھۇ ئەكبەر'),
        (r'تەھلىل', 'تەھلىل'),
        (r'سـۈبھى كازىـب', 'سۈبھى كازىب'),
        (r'سـۇبھى سـادىق', 'سۈبھى سادىق'),
    ]
    for pattern, rep in specific_reps:
        text = re.sub(pattern, rep, text)

    # Suffixes
    text = re.sub(r'الر(دا|دىن|غا|نى|نىڭ|مۇ|گىچە|لىرى|لىرىنى|لىرىنىڭ|لىرىغا|لىرىدا|لىرىدىن)?\b', r'لار\1', text)
    text = re.sub(r'الپ\b', 'لاپ', text)
    text = re.sub(r'الش\b', 'لاش', text)
    text = re.sub(r'الشتۇر', 'لاشتۇر', text)
    text = re.sub(r'الشقان', 'لاشقان', text)
    text = re.sub(r'اليمىز\b', 'لايمىز', text)
    text = re.sub(r'اليمەن\b', 'لايمەن', text)
    text = re.sub(r'النمايدۇ\b', 'لانمايدۇ', text)
    text = re.sub(r'النماقچى\b', 'لانماقچى', text)
    text = re.sub(r'النغان\b', 'لانغان', text)
    text = re.sub(r'النسا\b', 'لانسا', text)
    text = re.sub(r'النىدۇ\b', 'لىنىدۇ', text)
    text = re.sub(r'الندى\b', 'لاندى', text)
    text = re.sub(r'اللىق\b', 'لالىق', text)
    text = re.sub(r'الاليدۇ\b', 'لالايدۇ', text)
    text = re.sub(r'الالمايدۇ\b', 'لالمايدۇ', text)
    text = re.sub(r'الالمىغان\b', 'لالمىغان', text)
    text = re.sub(r'المايدۇ\b', 'لىمايدۇ', text)
    text = re.sub(r'المىغان\b', 'لىمىغان', text)
    text = re.sub(r'المىسا\b', 'لىمىسا', text)
    text = re.sub(r'(\w+)(داق|پ|ەت|ۈن|ىر|تىن|دە|دا|لىق|سى|يۈز|دۇر)ال\b', r'\1\2لا', text)
    text = re.sub(r'(\w+)ال(\b)', r'\1لا\2', text)

    return text

def fix_rtl_line_punctuation(line: str) -> str:
    line = line.strip()
    if not line:
        return ""
    m = re.match(r'^([.,،!؟:؛\-\)\(»«\s]+)(.+)$', line)
    if m:
        punct = m.group(1).strip()
        rest = m.group(2).strip()
        if punct in ['.', '،', '!', '؟', ':', '؛']:
            return rest + punct
        if punct in ['..', '...', '---', '_', '-']:
            return rest
    return line

def get_page_lines(pno):
    page = doc[pno]
    d = page.get_text("dict")
    body_lines = []
    fn_lines = []
    
    for b in d["blocks"]:
        if "lines" not in b: continue
        y0 = b["bbox"][1]
        
        # Bottom page number
        raw = "".join(s["text"] for l in b["lines"] for s in l["spans"]).strip()
        if raw.isdigit() and y0 > 620:
            continue
            
        # Footnote detection
        is_fn = False
        if y0 >= 550:
            avg_size = sum(s["size"] for l in b["lines"] for s in l["spans"]) / max(1, sum(len(l["spans"]) for l in b["lines"]))
            if avg_size <= 9.5 or "(((" in raw:
                is_fn = True
                
        for l in b["lines"]:
            spans = l["spans"]
            lt = "".join(s["text"] for s in spans).strip()
            if not lt or lt.isdigit(): continue
            lt = fix_rtl_line_punctuation(lt)
            lt = normalize_text(lt)
            max_size = max(s["size"] for s in spans)
            font_name = spans[0]["font"]
            color = spans[0]["color"]
            
            item = {
                "text": lt,
                "size": max_size,
                "font": font_name,
                "color": color,
                "y0": l["bbox"][1],
                "is_arabic": "TraditionalArab" in font_name or "Amiri" in font_name,
                "is_heading": max_size >= 13.0 or color in [0x00a777, 0xec008c, 0xaa1f23],
                "level": 2 if (max_size >= 13.0 and color == 0x00a777) else (3 if color in [0xec008c, 0xaa1f23] else 0)
            }
            if is_fn:
                fn_lines.append(item)
            else:
                body_lines.append(item)
                
    return body_lines, fn_lines

print("Line parser configured.")
