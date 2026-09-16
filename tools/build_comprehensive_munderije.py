#!/usr/bin/env python3
"""
tools/build_comprehensive_munderije.py
Generates a complete, beautifully structured, and fully linked 'تولۇق مۇندەرىجە' (Table of Contents) page:
1. Quick navigation table across all 13 sections.
2. Direct links on every Section Heading (##) to that section's first page.
3. Direct links on every Page Heading (###) to that page.
4. Direct anchor links (#q...) on all subtopics and blocks across all 46 pages.
"""

import re
from pathlib import Path
import sys

tools_dir = Path(__file__).parent
sys.path.append(str(tools_dir))

from apply_direct_links_and_blocks import PAGES_CONFIG

DOCS_ROOT = Path("src/content/docs/2000")
OUT_FILE = DOCS_ROOT / "00-muqeddimu" / "04-munderije.mdx"

# Map PAGES_CONFIG by (dir_name, filename)
PAGES_CONFIG_MAP = {}
for p in PAGES_CONFIG:
    d_name = Path(p["dir"]).name
    PAGES_CONFIG_MAP[(d_name, p["filename"])] = p

md_out = []

md_out.append("""---
title: "مۇندەرىجە"
description: "«دىن ۋە ھايات (2000 سوئالغا جاۋاب)» نىڭ تولۇق بۆلۈم، تېما ۋە سوئاللار مۇندەرىجىسى."
sidebar:
  label: "تولۇق مۇندەرىجە"
  order: 4
---

## بۆلۈملەر بويىچە تېز كۆرۈش

تۆۋەندىكى تىزىملىكتىن ئۆزىڭىز قىزىققان بۆلۈمنى تاللاپ بىۋاسىتە شۇ بۆلۈمنىڭ تېمىلىرىغا يۆتكىلەيسىز ياكى ھەربىر تېمىغا چېكىپ شۇ سوئال كارتىسىغا كىرەلەيسىز:

| بۆلۈم | بۆلۈم نامى | سوئال دائىرىسى | سەھىپە سانى |
| :--- | :--- | :--- | :--- |
| **00** | [مۇقەددىمە](#00-مۇقەددىمە-ۋە-كىرىش-سۆز) | كىرىش سۆز ۋە مەلۇماتلار | 4 سەھىپە |
| **01** | [ئېتىقاد](#1-بۆلۈم-ئېتىقاد-سوئال-1--163) | سوئال 1 – 163 | 8 سەھىپە |
| **02** | [ئىبادەت](#2-بۆلۈم-ئىبادەت-سوئال-164--647) | سوئال 164 – 647 | 14 سەھىپە |
| **03** | [ئەخلاق](#3-بۆلۈم-ئەخلاق-سوئال-648--967) | سوئال 648 – 967 | 10 سەھىپە |
| **04** | [سەھىرەت ۋە تۇرمۇش](#4-بۆلۈم-سەھىرەت-ۋە-تۇرمۇش-سوئال-968--1317) | سوئال 968 – 1317 | 6 سەھىپە |
| **05** | [ھارام ۋە چەكلەنگەن ئىشلار](#5-بۆلۈم-ھارام-ۋە-چەكلەنگەن-ئىشلار-سوئال-1318--1555) | سوئال 1318 – 1555 | 7 سەھىپە |
| **06** | [قۇرئان ۋە سۈننەت](#6-بۆلۈم-قۇرئان-ۋە-سۈننەت-سوئال-1556--1680) | سوئال 1556 – 1680 | 4 سەھىپە |
| **07** | [ئىسلامىي ئىلىملەر ۋە مەزھەبلەر](#7-بۆلۈم-ئىسلامىي-ئىلىملەر-ۋە-مەزھەبلەر-سوئال-1681--1839) | سوئال 1681 – 1839 | 4 سەھىپە |
| **08** | [قۇرئان كەرىمنىڭ مۆجىزىلىرى](#8-بۆلۈم-قۇرئان-كەرىمنىڭ-مۆجىزىلىرى-سوئال-1840--1845) | سوئال 1840 – 1845 | 1 سەھىپە |
| **09** | [مۇقەددەس جايلار ۋە بىلىم يۇرتلىرى](#9-بۆلۈم-مۇقەددەس-جايلار-ۋە-بىلىم-يۇرتلىرى-سوئال-1846--1894) | سوئال 1846 – 1894 | 2 سەھىپە |
| **10** | [ئاتېئىزم ۋە ئاللاھنىڭ بارلىقى](#10-بۆلۈم-ئاتېئىزم-ۋە-ئاللاھنىڭ-بارلىقى-سوئال-1895--1938) | سوئال 1895 – 1938 | 2 سەھىپە |
| **11** | [شەك-شۈبھىلەرگە رەددىيە](#11-بۆلۈم-شەك-شۈبھىلەرگە-رەددىيە-سوئال-1939--1958) | سوئال 1939 – 1958 | 1 سەھىپە |
| **12** | [ئىسلام دۆلىتى ۋە خەلىپىلىكلەر](#12-بۆلۈم-ئىسلام-دۆلىتى-ۋە-خەلىپىلىكلەر-سوئال-1959--2000) | سوئال 1959 – 2000 | 1 سەھىپە |

---

## [00-مۇقەددىمە ۋە كىرىش سۆز](/2000/00-muqeddimu/01-kitab-heqqide/)

- **[01. كىتاب ھەققىدە ۋە بېغىشلاش](/2000/00-muqeddimu/01-kitab-heqqide/)**
  - [كىتاب ھەققىدە قىسقىچە تونۇشتۇرۇش](/2000/00-muqeddimu/01-kitab-heqqide/#كىتاب-ھەققىدە-قىسقىچە-تونۇشتۇرۇش)
  - [نەشر ئۇچۇرلىرى ۋە CIP كاتالوگ مەلۇماتى](/2000/00-muqeddimu/01-kitab-heqqide/#نەشر-ئۇچۇرلىرى-ۋە-cip-كاتالوگ-مەلۇماتى)
  - [ئاپتورنىڭ ئاتىسىغا بېغىشلىشى](/2000/00-muqeddimu/01-kitab-heqqide/#بېغىشلاش)
  - [كىتابنىڭ ئاساسىي ئالاھىدىلىكلىرى](/2000/00-muqeddimu/01-kitab-heqqide/#كىتابنىڭ-ئاساسىي-ئالاھىدىلىكلىرى)
- **[02. ئاپتور مۇھەممەد يۈسۈپ ھەققىدە](/2000/00-muqeddimu/02-aptur-heqqide/)**
  - [مۇھەممەد يۈسۈپ مۇھەممەد تۇرسۇننىڭ تەرجىمىھالى](/2000/00-muqeddimu/02-aptur-heqqide/#مۇھەممەد-يۈسۈپ-مۇھەممەد-تۇرسۇننىڭ-تەرجىمىھالى)
  - [مىسىر ئەزھەر ئۇنىۋېرسىتېتىدىكى تەھسىلى](/2000/00-muqeddimu/02-aptur-heqqide/#مىسىر-ئەزھەر-ئۇنىۋېرسىتېتىدىكى-تەھسىلى)
  - [تەلىم-تەربىيە ۋە جامائەت خىزمەتلىرى](/2000/00-muqeddimu/02-aptur-heqqide/#تەلىم-تەربىيە-ۋە-جامائەت-خىزمەتلىرى)
  - [ئاپتورنىڭ ئىدىيەۋى قارىشى ۋە مېتودولوگىيەسى](/2000/00-muqeddimu/02-aptur-heqqide/#ئاپتورنىڭ-ئىدىيەۋى-قارىشى-ۋە-مېتودولوگىيەسى)
  - [ئاپتور يازغان ۋە نەشر قىلىنغان ئەسەرلەر](/2000/00-muqeddimu/02-aptur-heqqide/#ئاپتور-يازغان-ۋە-نەشر-قىلىنغان-ئەسەرلەر)
  - [ئەرەب تىلىدىن ئۇيغۇرچىغا تەرجىمە قىلغان كىتابلىرى](/2000/00-muqeddimu/02-aptur-heqqide/#ئەرەب-تىلىدىن-ئۇيغۇرچىغا-تەرجىمە-قىلغان-كىتابلىرى)
- **[03. كىرىش سۆز ۋە مېتودولوگىيە](/2000/00-muqeddimu/03-kirish-soz/)**
  - [ئاپتورنىڭ كىتابخانلارغا سۆزى](/2000/00-muqeddimu/03-kirish-soz/#ھۆرمەتلىك-كىتابخان)
  - [كىتابنىڭ قۇرۇلمىسى ۋە بۆلۈملىرى](/2000/00-muqeddimu/03-kirish-soz/#كىتابنىڭ-قۇرۇلمىسى-ۋە-بۆلۈملىرى)
  - [تەتقىقات مېتودولوگىيەسى ۋە پىرىنسىپلىرى](/2000/00-muqeddimu/03-kirish-soz/#تەتقىقات-مېتودولوگىيەسى-ۋە-پىرىنسىپلىرى)
  - [دۇئا ۋە تىلەك](/2000/00-muqeddimu/03-kirish-soz/#دۇئا-ۋە-تىلەك)
- **[04. تولۇق مۇندەرىجە](/2000/00-muqeddimu/04-munderije/)**""")

SECTIONS_CONFIG = [
    {"dir_name": "01-etiqad", "sec_num": "1", "sec_title": "ئېتىقاد", "q_range": "سوئال 1 – 163"},
    {"dir_name": "02-ibadet", "sec_num": "2", "sec_title": "ئىبادەت", "q_range": "سوئال 164 – 647"},
    {"dir_name": "03-exlaq", "sec_num": "3", "sec_title": "ئەخلاق", "q_range": "سوئال 648 – 967"},
    {"dir_name": "04-sehiret", "sec_num": "4", "sec_title": "سەھىرەت ۋە تۇرمۇش", "q_range": "سوئال 968 – 1317"},
    {"dir_name": "05-haram-cheklengen", "sec_num": "5", "sec_title": "ھارام ۋە چەكلەنگەن ئىشلار", "q_range": "سوئال 1318 – 1555"},
    {"dir_name": "06-quran-sunnet", "sec_num": "6", "sec_title": "قۇرئان ۋە سۈننەت", "q_range": "سوئال 1556 – 1680"},
    {"dir_name": "07-islamiy-ilimler", "sec_num": "7", "sec_title": "ئىسلامىي ئىلىملەر ۋە مەزھەبلەر", "q_range": "سوئال 1681 – 1839"},
    {"dir_name": "08-quran-mojiziliri", "sec_num": "8", "sec_title": "قۇرئان كەرىمنىڭ مۆجىزىلىرى", "q_range": "سوئال 1840 – 1845"},
    {"dir_name": "09-muqeddes-jaylar", "sec_num": "9", "sec_title": "مۇقەددەس جايلار ۋە بىلىم يۇرتلىرى", "q_range": "سوئال 1846 – 1894"},
    {"dir_name": "10-ateizm-allahning-barliqi", "sec_num": "10", "sec_title": "ئاتېئىزم ۋە ئاللاھنىڭ بارلىقى", "q_range": "سوئال 1895 – 1938"},
    {"dir_name": "11-shek-shubhiler", "sec_num": "11", "sec_title": "شەك-شۈبھىلەرگە رەددىيە", "q_range": "سوئال 1939 – 1958"},
    {"dir_name": "12-islam-dowliti", "sec_num": "12", "sec_title": "ئىسلام دۆلىتى ۋە خەلىپىلىكلەر", "q_range": "سوئال 1959 – 2000"},
]

for sec in SECTIONS_CONFIG:
    sec_dir = DOCS_ROOT / sec["dir_name"]
    files = sorted(sec_dir.glob("*.mdx"))
    first_url = f"/2000/{sec['dir_name']}/{files[0].stem}/" if files else "#"
    
    md_out.append(f"\n---\n\n## [{sec['sec_num']}-بۆلۈم: {sec['sec_title']} ({sec['q_range']})]({first_url})\n")

    for idx, f in enumerate(files, 1):
        content = f.read_text(encoding="utf-8")
        m_t = re.search(r'title:\s*\"([^\"]+)\"', content)
        p_title = m_t.group(1) if m_t else f.stem
        q_ids = [int(x) for x in re.findall(r'id=\"q(\d+)\"', content)]
        p_qrange = f"سوئال {min(q_ids)} – {max(q_ids)}" if q_ids else ""
        page_url = f"/2000/{sec['dir_name']}/{f.stem}/"

        md_out.append(f"### {idx}. [{p_title}]({page_url}) ({p_qrange})\n")

        # Check if page is in PAGES_CONFIG (Section 01 and Section 02)
        cfg_entry = PAGES_CONFIG_MAP.get((sec["dir_name"], f.name))
        if cfg_entry:
            for b in cfg_entry["blocks"]:
                if b.get("is_table"):
                    md_out.append(f"- [{b['title']} (مۇكەممەل جەدۋەل)]({page_url}#ئاللاھ-تائالانىڭ-99-گۈزەل-ئىسمى)\n")
                elif "q_start" in b:
                    b_range = f"(سوئال {b['q_start']} – {b['q_end']})" if b['q_start'] != b['q_end'] else f"(سوئال {b['q_start']})"
                    md_out.append(f"- [{b['title']} {b_range}]({page_url}#q{b['q_start']})\n")
        else:
            # Extract ## headings from markdown file
            h2_matches = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
            for h in h2_matches:
                m_q = re.search(r'سوئال\s*(\d+)\s*[–-]\s*(\d+)', h)
                start_q = int(m_q.group(1)) if m_q else (min(q_ids) if q_ids else 1)
                md_out.append(f"- [{h}]({page_url}#q{start_q})\n")

full_md = "".join(md_out)
OUT_FILE.write_text(full_md, encoding="utf-8")
print(f"Generated {OUT_FILE} with {len(full_md)} characters.")
