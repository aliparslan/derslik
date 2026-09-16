#!/usr/bin/env python3
"""
tools/extract_book2.py
Extraction, normalization, and MDX generation for Book 2
(Questions 1318 through 2000 — Sections 05 through 12)
"""

import os
import sys
import re
import json
from pathlib import Path

# Add tools dir to path for imports
tools_dir = Path(__file__).parent
sys.path.append(str(tools_dir))
from extract_2000 import normalize_text

PDF_P1 = "/Users/arslan/Desktop/2000/book2_part1.pdf"
PDF_P2 = "/Users/arslan/Desktop/2000/book2_part2.pdf"
OUTPUT_JSON_B2 = "/Users/arslan/code/derslik/tools/extracted_2000_book2.json"
OUTPUT_JSON_ALL = "/Users/arslan/code/derslik/tools/extracted_2000.json"
DOCS_DIR = Path("/Users/arslan/code/derslik/src/content/docs/2000")

# Sections configuration
SECTIONS_CONFIG = [
    {
        "dir": DOCS_DIR / "05-haram-cheklengen",
        "pages": [
            {
                "filename": "01-halal-haram-esasliri.mdx",
                "title": "ھالال-ھارام ئۇقۇمى ۋە ئاساسلىرى",
                "sidebar_label": "ھالال-ھارام ئاساسلىرى (1318–1347)",
                "order": 1,
                "start_q": 1318,
                "end_q": 1347,
                "heading": "ھالال-ھارام ئۇقۇمى، پرىنسىپلىرى ۋە ئاساسلىرى (سوئال 1318 – 1347)"
            },
            {
                "filename": "02-yimek-ichmek-hasiyetliri.mdx",
                "title": "يېمەك-ئىچمەك ۋە ھايۋانلاردىكى ھالال-ھارام",
                "sidebar_label": "يېمەك-ئىچمەك ۋە ھايۋانلار (1348–1385)",
                "order": 2,
                "start_q": 1348,
                "end_q": 1385,
                "heading": "يېمەك-ئىچمەك، سۇيۇقلۇقلار ۋە ھايۋانلاردىكى ھالال-ھارام ئەھكاملىرى (سوئال 1348 – 1385)"
            },
            {
                "filename": "03-iqtisadiy-gunahlar-sudxurliq.mdx",
                "title": "پۇل-مۇئامىلە، سۈدخورلۇق ۋە ھارام كەسىپلەر",
                "sidebar_label": "سۈدخورلۇق ۋە ھارام كەسىپ (1386–1420)",
                "order": 3,
                "start_q": 1386,
                "end_q": 1420,
                "heading": "جازانىخورلۇق، قىمار، ئوغرىلىق ۋە ھارام كىرىملەر (سوئال 1386 – 1420)"
            },
            {
                "filename": "04-organ-yotkesh-tibbiy-ehkamlar.mdx",
                "title": "ئورگان كۆچۈرۈش ۋە زامانىۋى تېببىي ئەھكام",
                "sidebar_label": "ئورگان كۆچۈرۈش ۋە تېببىي ئەھكام (1421–1455)",
                "order": 4,
                "start_q": 1421,
                "end_q": 1455,
                "heading": "ئادەم ئەزاسى يۆتكەش، داۋالىنىش ۋە تېببىي چەكلىمىلەر (سوئال 1421 – 1455)"
            },
            {
                "filename": "05-turmush-va-koyinish-cheklimiliri.mdx",
                "title": "كىيىنىش، زىبۇ-زىننەت ۋە ئادەتتىكى چەكلىمىلەر",
                "sidebar_label": "كىيىنىش ۋە زىبۇ-زىننەت (1456–1495)",
                "order": 5,
                "start_q": 1456,
                "end_q": 1495,
                "heading": "ئەر-ئاياللارنىڭ كىيىنىشى، زىبۇ-زىننەت ۋە ھاياتتىكى چەكلىمىلەر (سوئال 1456 – 1495)"
            },
            {
                "filename": "06-naxsha-muziqa-surunlar.mdx",
                "title": "ناخشا-مۇزىكا، كۆڭۈل ئېچىش ۋە سورۇنلار",
                "sidebar_label": "ناخشا-مۇزىكا ۋە كۆڭۈل ئېچىش (1496–1525)",
                "order": 6,
                "start_q": 1496,
                "end_q": 1525,
                "heading": "ناخشا-مۇزىكا، كىنو-تېلېۋىزور، ھەيكەل ۋە سورۇن ئەدەپلىرى (سوئال 1496 – 1525)"
            },
            {
                "filename": "07-chong-gunahlar-kapparet.mdx",
                "title": "چوڭ گۇناھلار ۋە گۇناھ-مەسىيەتتىن ساقلىنىش",
                "sidebar_label": "چوڭ گۇناھلار ۋە مەسىيەت (1526–1555)",
                "order": 7,
                "start_q": 1526,
                "end_q": 1555,
                "heading": "ئاللاھنىڭ ھەققىگە قارشى ئىشلەنگەن چوڭ گۇناھلار ۋە مەسىيەتلەر (سوئال 1526 – 1555)"
            },
        ]
    },
    {
        "dir": DOCS_DIR / "06-quran-sunnet",
        "pages": [
            {
                "filename": "01-quran-heqqide-omumiy.mdx",
                "title": "قۇرئان كەرىمنىڭ خۇسۇسىيەتلىرى ۋە چۈشۈش تارىخى",
                "sidebar_label": "قۇرئان كەرىم ھەققىدە (1556–1589)",
                "order": 1,
                "start_q": 1556,
                "end_q": 1589,
                "heading": "قۇرئان كەرىمنىڭ تەرىپى، ئىسىملىرى، سۈپەتلىرى ۋە چۈشۈش جەريانى (سوئال 1556 – 1589)"
            },
            {
                "filename": "02-quran-toplinishi-ve-nusxiliri.mdx",
                "title": "قۇرئاننىڭ توپلىنىشى ۋە نۇسخىلىرى",
                "sidebar_label": "قۇرئاننىڭ توپلىنىشى ۋە نۇسخىلىرى (1590–1620)",
                "order": 2,
                "start_q": 1590,
                "end_q": 1620,
                "heading": "قۇرئان كەرىمنىڭ توپلىنىشى، كىتاب قىلىنىشى ۋە نۇسخىلىرى (سوئال 1590 – 1620)"
            },
            {
                "filename": "03-quran-oqur-adabliri.mdx",
                "title": "قۇرئان ئوقۇش، قىرائەت ۋە يادلاش پەزىلەتلىرى",
                "sidebar_label": "قۇرئان ئوقۇش پەزىلىتى (1621–1650)",
                "order": 3,
                "start_q": 1621,
                "end_q": 1650,
                "heading": "قۇرئان ئوقۇش، قىرائەت، تەجۋىد ۋە يادلاشنىڭ پەزىلىتى ۋە ساۋابى (سوئال 1621 – 1650)"
            },
            {
                "filename": "04-sunnet-ve-hedis-ilmi.mdx",
                "title": "پەيغەمبەر سۈننىتى، ھەدىس تۈرلىرى ۋە دەرىجىلىرى",
                "sidebar_label": "سۈننەت ۋە ھەدىس ئىلمى (1651–1680)",
                "order": 4,
                "start_q": 1651,
                "end_q": 1680,
                "heading": "سۈننەت، ھەدىس، قۇرئانچىلارغا رەددىيە ۋە سەھىھ-زەئىف ھەدىسلەر (سوئال 1651 – 1680)"
            },
        ]
    },
    {
        "dir": DOCS_DIR / "07-islamiy-ilimler",
        "pages": [
            {
                "filename": "01-islamiy-ilimler-muqeddimisi.mdx",
                "title": "ئىسلامىي ئىلىملەر تۈرلىرى ۋە ئەھمىيىتى",
                "sidebar_label": "ئىسلامىي ئىلىملەر تۈرلىرى (1681–1715)",
                "order": 1,
                "start_q": 1681,
                "end_q": 1715,
                "heading": "ئىسلامىي ئىلىملەر، ئىلىم ئۆگىنىشنىڭ پەرزلىكى ۋە تۈرلىرى (سوئال 1681 – 1715)"
            },
            {
                "filename": "02-tepsir-ve-tefsirchiler.mdx",
                "title": "تەپسىر ئىلمى ۋە مەشھۇر مۆتىۋەر تەپسىرلەر",
                "sidebar_label": "تەپسىر ئىلمى ۋە مۆتىۋەر ئەسەرلەر (1716–1750)",
                "order": 2,
                "start_q": 1716,
                "end_q": 1750,
                "heading": "تەپسىر ئىلمىنىڭ ئاساسلىرى، مەشھۇر مۇپەسسىرلەر ۋە كىتابلار (سوئال 1716 – 1750)"
            },
            {
                "filename": "03-fiqh-ve-mezhebler.mdx",
                "title": "فىقھى ئىلمى ۋە تۆت چوڭ فىقھى مەزھەب",
                "sidebar_label": "فىقھى ئىلمى ۋە تۆت مەزھەب (1751–1790)",
                "order": 3,
                "start_q": 1751,
                "end_q": 1790,
                "heading": "فىقھى مەزھەپلەر (ھەنەفىي، مالىكىي، شافىئىي، ھەنبەلىي) ۋە تەقلىد (سوئال 1751 – 1790)"
            },
            {
                "filename": "04-eqide-ve-kelam.mdx",
                "title": "ئەھلى سۈننەت ئەقىدىسى ۋە كالام ئىلمى",
                "sidebar_label": "ئەھلى سۈننەت ئەقىدىسى (1791–1839)",
                "order": 4,
                "start_q": 1791,
                "end_q": 1839,
                "heading": "تەۋھىدنىڭ تۈرلىرى، بىدئەت، ئەھلى سۈننەت ۋە ئېتىقادىي ئېقىملار (سوئال 1791 – 1839)"
            },
        ]
    },
    {
        "dir": DOCS_DIR / "08-quran-mojiziliri",
        "pages": [
            {
                "filename": "01-ilmiy-ve-edebiy-mojiziler.mdx",
                "title": "قۇرئان كەرىمنىڭ ئىلمىي ۋە بەدىئىي مۆجىزىلىرى",
                "sidebar_label": "قۇرئان كەرىمنىڭ مۆجىزىلىرى (1840–1845)",
                "order": 1,
                "start_q": 1840,
                "end_q": 1845,
                "heading": "قۇرئان كەرىمنىڭ ئەدەبىي، ئىلمىي، تارىخىي ۋە غەيبىي مۆجىزىلىرى (سوئال 1840 – 1845)"
            },
        ]
    },
    {
        "dir": DOCS_DIR / "09-muqeddes-jaylar",
        "pages": [
            {
                "filename": "01-mekke-medine-ve-quddus.mdx",
                "title": "ھەرەمەين، كەبە ۋە مەسجىدى ئەقسا",
                "sidebar_label": "ھەرەمەين ۋە مەسجىدى ئەقسا (1846–1870)",
                "order": 1,
                "start_q": 1846,
                "end_q": 1870,
                "heading": "مەككە، كەبەتۇللاھ، مەدىنە مۇنەۋۋەرە ۋە مەسجىدى ئەقسانىڭ پەزىلىتى (سوئال 1846 – 1870)"
            },
            {
                "filename": "02-tarixiy-medrisiler-ve-uyghur-yurtliri.mdx",
                "title": "تارىخىي بىلىم يۇرتلىرى ۋە ئۇيغۇر ۋەقپىلىرى",
                "sidebar_label": "مەد Frederick يۇرتلىرى ۋە ئۇيغۇر تارىخى (1871–1894)",
                "order": 2,
                "start_q": 1871,
                "end_q": 1894,
                "heading": "ئىسلام تارىخىدىكى مەشھۇر مەدرىسىلەر، ھەرەمەيندىكى ئۇيغۇر ۋەقپىلىرى ۋە تارىخ (سوئال 1871 – 1894)"
            },
        ]
    },
    {
        "dir": DOCS_DIR / "10-ateizm-allahning-barliqi",
        "pages": [
            {
                "filename": "01-ateizm-ve-darvinizmge-reddiye.mdx",
                "title": "ئاتېئىزم، ماتېرىيالىزم ۋە دارۋىنىزمغا شەرئىي-ئىلمىي رەددىيە",
                "sidebar_label": "ئاتېئىزم ۋە دارۋىنىزمغا رەددىيە (1895–1915)",
                "order": 1,
                "start_q": 1895,
                "end_q": 1915,
                "heading": "ئاتېئىزم، ماتېرىيالىزم ۋە دارۋىنىزم سەپسەتىلىرىگە ئىلمىي رەددىيە (سوئال 1895 – 1915)"
            },
            {
                "filename": "02-allahning-barliqi-deliller.mdx",
                "title": "ئاللاھنىڭ بارلىقى ۋە بىرلىكىنىڭ ئەقلىي-پەننىي دەلىللىرى",
                "sidebar_label": "ئاللاھنىڭ بارلىقىنىڭ دەلىللىرى (1916–1938)",
                "order": 2,
                "start_q": 1916,
                "end_q": 1938,
                "heading": "ئىلىم-پەن، كائىنات ۋە ئىنسان يارىتىلىشى ئارقىلىق ئاللاھنىڭ بارلىقىنى ئىسپاتلاش (سوئال 1916 – 1938)"
            },
        ]
    },
    {
        "dir": DOCS_DIR / "11-shek-shubhiler",
        "pages": [
            {
                "filename": "01-zamaniviy-meseleler-ve-shubhiler.mdx",
                "title": "زامانىۋى مەسىلىلەر، ئاياللار ھوقۇقى ۋە شەك-شۈبھىلەرگە جاۋاب",
                "sidebar_label": "شەك-شۈبھىلەر ۋە زامانىۋى مەسىلىلەر (1939–1958)",
                "order": 1,
                "start_q": 1939,
                "end_q": 1958,
                "heading": "ئىسلامغا ئارتىلغان شەك-شۈبھىلەر، ئاياللار ھوقۇقى، تېررورلۇق ۋە جىھاد (سوئال 1939 – 1958)"
            },
        ]
    },
    {
        "dir": DOCS_DIR / "12-islam-dowliti",
        "pages": [
            {
                "filename": "01-xilafet-ve-tarixiy-dewirler.mdx",
                "title": "ئىسلام دۆلىتى، خۇلەفائۇرراشىدۇن ۋە تارىخىي خەلىپىلىكلەر",
                "sidebar_label": "ئىسلام دۆلىتى ۋە خەلىپىلىكلەر (1959–2000)",
                "order": 1,
                "start_q": 1959,
                "end_q": 2000,
                "heading": "ئىسلامدا ھاكىمىيەت، كېڭەش تۈزۈمى، خۇلەفائۇرراشىدۇن، ئەمەۋىي، ئابباسىي ۋە ئوسمانىيلار (سوئال 1959 – 2000)"
            },
        ]
    },
]

def clean_span_chars(chars):
    out = []
    i = 0
    while i < len(chars):
        c = chars[i]["c"]
        w = chars[i]["bbox"][2] - chars[i]["bbox"][0]
        if c == "\u0640":
            i += 1
            continue
        if c == "ا":
            if w < 0.5:
                # zero-width alef before lam
                if i + 1 < len(chars) and chars[i+1]["c"] == "ل":
                    out.append("لا")
                    i += 2
                    continue
                else:
                    i += 1
                    continue
            elif w < 1.8: # kashida artifact
                i += 1
                continue
        out.append(c)
        i += 1
    return "".join(out)

def extract_cleaned_lines():
    import fitz
    all_lines = []
    for path, part_name in [(PDF_P1, "B2P1"), (PDF_P2, "B2P2")]:
        doc = fitz.open(path)
        print(f"Loaded {path} ({len(doc)} pages)")
        for p_idx in range(len(doc)):
            page = doc[p_idx]
            data = json.loads(page.get_text("rawjson"))
            for b in data.get("blocks", []):
                for l in b.get("lines", []):
                    line_chars = []
                    for s in l.get("spans", []):
                        line_chars.extend(s.get("chars", []))
                    cleaned = clean_span_chars(line_chars)
                    cleaned = normalize_text(cleaned)
                    l_str = cleaned.strip()
                    if l_str:
                        all_lines.append((part_name, p_idx + 1, l_str))
    print(f"Total processed lines: {len(all_lines)}")
    return all_lines

def extract_book2_questions(all_lines):
    q_word_re = re.compile(r"^س[ئاو\:\s]*ل")
    q_num_re = re.compile(r"^(?:\.|\b)?(1\d{3}|2000)(?:\.|\b)?$")
    q_inline_re = re.compile(r"(?:^|\s)(1\d{3}|2000)\s*[:\.]?\s*س[ئۇا\:\s]*ال[:\.\s]*(.*)$")
    q_inline_re2 = re.compile(r"س[ئۇا\:\s]*ال[:\.\s]*(.*)\s+(1\d{3}|2000)(?:\.|\b)?$")
    q_inline_re3 = re.compile(r"س[ئۇا\:\s]*ال[:\.\s]*(1\d{3}|2000)[:\.\s]*(.*)$")

    questions = {}
    expected_q = 1318
    i = 0
    while i < len(all_lines) and expected_q <= 2000:
        part, pnum, line = all_lines[i]
        q_num = None
        q_title = ""
        consumed = 1

        # Check special case 1591
        if expected_q == 1591 and "1591" in line:
            cand = 1591
            for j in range(1, 4):
                if i + j < len(all_lines):
                    nl = all_lines[i+j][2]
                    if "قۇرئان كەرىم" in nl or "نۇسخى" in nl:
                        q_num = 1591
                        q_title = nl.replace("ئال:", "").replace("ئال", "").strip()
                        consumed = j + 1
                        break

        # Check standalone number
        if not q_num:
            m_num = q_num_re.match(line)
            if m_num:
                cand = int(m_num.group(1))
                if cand == expected_q:
                    for j in range(1, 5):
                        if i + j < len(all_lines):
                            next_l = all_lines[i+j][2]
                            if q_word_re.search(next_l) or "سوئال" in next_l or "سو :ئال" in next_l:
                                q_num = cand
                                t = next_l
                                for k in ["سوئال:", ":سوئال", "سوئال", "س:وئال", "سو:ئال", "سو :ئال", "سۇئال:", "سۇئال"]:
                                    t = t.replace(k, "")
                                q_title = t.strip()
                                consumed = j + 1
                                # Gather remaining title lines until :جاۋاب
                                jawabb_pattern = re.compile(r'(?:جاۋ[^\s\w]*[الله]*[^\s\w]*ب|:?جاۋاب:?|ج\s*:\s*اۋاب|جاۋا\s*:\s*ب|جاۋ\s*:\s*اب|جاۋاب\s*:|:?\s*ج\s*ا+\s*ۋ\s*(?:[الله]*)\s*ا*\s*ب\s*:?|\(\s*جاۋاب\s*\))')
                                while i + consumed < len(all_lines):
                                    f_line = all_lines[i+consumed][2]
                                    if jawabb_pattern.search(f_line):
                                        break
                                    if any(f_line.startswith(k) for k in [":جاۋاب", "جاۋاب:", "جاۋاب"]):
                                        break
                                    if q_num_re.match(f_line) or "بۆلۈم" in f_line:
                                        break
                                    q_title += (" " + f_line.strip()).strip()
                                    consumed += 1
                                break

        # Check inline number
        if not q_num:
            for pattern in [q_inline_re, q_inline_re2, q_inline_re3]:
                m = pattern.search(line)
                if m:
                    cand = int(m.group(1) if pattern != q_inline_re2 else m.group(2))
                    if cand == expected_q:
                        q_num = cand
                        q_title = (m.group(2) if pattern != q_inline_re2 else m.group(1)).strip()
                        break

        if q_num and q_num == expected_q:
            jawabb_pattern = re.compile(r'(?:جاۋ[^\s\w]*[الله]*[^\s\w]*ب|:?جاۋاب:?|ج\s*:\s*اۋاب|جاۋا\s*:\s*ب|جاۋ\s*:\s*اب|جاۋاب\s*:|:?\s*ج\s*ا+\s*ۋ\s*(?:[الله]*)\s*ا*\s*ب\s*:?|\(\s*جاۋاب\s*\))')
            m_jawabb = jawabb_pattern.search(q_title)
            embedded_ans = ""
            if m_jawabb:
                clean_q = q_title[:m_jawabb.start()].strip()
                embedded_ans = q_title[m_jawabb.end():].strip()
                q_title = clean_q

            questions[q_num] = {
                "number": q_num,
                "question": q_title,
                "part": part,
                "page": pnum,
                "answer_start": i + consumed,
                "embedded_ans": embedded_ans,
                "answer_lines": []
            }
            expected_q += 1
            i += consumed
        else:
            i += 1

    sorted_nums = sorted(questions.keys())
    print(f"Total questions indexed: {len(sorted_nums)} / 683")
    missing = set(range(1318, 2001)) - set(sorted_nums)
    if missing:
        raise ValueError(f"Missing questions in Book 2: {sorted(missing)}")
    else:
        print("PERFECT: All 683 questions (1318 through 2000) are present!")

    def clean_text_typography(p: str) -> str:
        # Strip tatweel / kashida
        p = p.replace("\u0640", "")

        # Punctuation & misplaced symbols
        p = re.sub(r'(\b[\u0600-\u06ff]{2,}):([نلداە]\b)', r'\1\2', p)
        p = re.sub(r'\bئا للاھ\b', 'ئاللاھ', p)

        # Suffix and word reconnection
        suffixes = r'(دۇ|دى|گە|قا|دا|دە|تى|تىگە|سى|سىگە|نىڭ|نى|لار|لەر|دىن|تىن|غان|گەن|لىق|لىك|لىقى|تلەردە|لاردىن|لەردىن|منىڭ|لىرى|ىدىغان|ىدۇ|ىش|غا)'
        p = re.sub(r'(\b[\u0600-\u06ff]{2,}) ' + suffixes + r'\b', r'\1\2', p)
        p = re.sub(r'(\b[\u0600-\u06ff]{2,}) ([ىنەادرتيى])\b', r'\1\2', p)
        p = re.sub(r'\b([ئك]) ([\u0600-\u06ff]{2,}\b)', r'\1\2', p)

        # Number & punctuation artifacts
        uy_letter = r"[\u0621-\u064A\u0671-\u06D5]"
        p = re.sub(r"(\d+)\s*[-–—]\s*،\s*(" + uy_letter + r")", r"\1-\2", p)
        p = re.sub(r"(\d+)(" + uy_letter + r")", r"\1 \2", p)
        p = re.sub(r"(" + uy_letter + r")(\d+)", r"\1 \2", p)

        # Punctuation spacing
        p = re.sub(r'\s+،', '،', p)
        p = re.sub(r'،(?=[^\s])', '، ', p)
        p = re.sub(r'\s+:', ':', p)
        p = re.sub(r':(?=[^\s\d])', ': ', p)
        p = re.sub(r' +', ' ', p)
        return p.strip()

    def format_q1887_custom(raw_lines, clean_fn):
        filtered = []
        for l in raw_lines:
            if any(w in l for w in ['ەۋ اغرلاۇئ', 'كىلتەۋىسانۇم', 'رەلىلىسەم', 'للااھ–ماراھ', 'رۇغيۇئ ىكىدىرايىد', 'ملاسىئ ىكىدىساينۇد']):
                continue
            if any(l.startswith(k) for k in ["بۆلۈم", "-بۆلۈم", ":بۆلۈم", "مۇندەرىجە", "پايدىلىنىلغان"]):
                continue
            if any(k in l for k in ["ئىسالمدىكى", "ئىسلامدىكى", "ۇقەددەس", "ھىجرىيە يىلنامىسى", "قىسقىچە چۈشەنچە"]):
                continue
            if l.strip() in ['-', '–', '—']:
                continue
            if re.match(r"^\d{1,3}$", l.strip()):
                continue
            filtered.append(l)

        full_text = " ".join(filtered)
        full_text = clean_fn(full_text)

        subs = [
            ("كۆيۈپ كۈل بولغان", "كۆيۈپ كۈل بولغان\n\n---\n\n### 1. ئۇيغۇر دىيارىدىكى ئالاھىدە ئۈچ مەسجىد\n\n"),
            ("ئۇيغۇر دىيارىدىكى ئالاھىدە ئۈچ مە سجىد ئەڭ دەسلەپ سېلىنغان مەسجىد-ئاتۇش جامەسى", "#### 1) ئەڭ دەسلەپ سېلىنغان مەسجىد — ئاتۇش جامەسى\n\n"),
            ("تۇنجى مەسجىدنى سالىدۇ كالا تېرىسى پىلانى ئاتۇشتا مەسجىد سېلىشنى", "تۇنجى مەسجىدنى سالىدۇ.\n\n##### كالا تېرىسى پىلانى\n\nئاتۇشتا مەسجىد سېلىشنى"),
            ("ئەڭ مەشھۇر مەسجىد-قەشقەر ھېيت گاھ جامەسى", "\n\n#### 2) ئەڭ مەشھۇر مەسجىد — قەشقەر ھېيتگاھ جامەسى\n\n"),
            ("ئەڭ مەشھۇر مەسجىد-قەشقەر ھېيتگاھ جامەسى", "\n\n#### 2) ئەڭ مەشھۇر مەسجىد — قەشقەر ھېيتگاھ جامەسى\n\n"),
            ("ئەڭ چوڭ مەسجىد-كېرىيە جامەسى", "\n\n#### 3) ئەڭ چوڭ مەسجىد — كېرىيە جامەسى\n\n"),
            ("ئىسلام دۇنياسىدىكى بەزى مەشھۇر بىلىم يۇرتلىرى", "\n\n---\n\n### 2. ئىسلام دۇنياسىدىكى بەزى مەشھۇر بىلىم يۇرتلىرى\n\n"),
            ("بەيتۇل ھېكمەت(بيت ال كمس)", "\n\n#### 1) بەيتۇلھېكمەت (بيت الحكمة)\n\n"),
            ("قەرەۋىيىن ئۇنىۋېرستېتى(جاممس القروين)", "\n\n#### 2) قەرەۋىيىن ئۇنىۋېرستېتى (جامعة القرويين)\n\n"),
            ("ئەڭ قەدىمى ئىسلام ئالىي بىلىمگاھى -ئەزھەر بىلىم يۇرتى(جاممس األزھر الشريف)", "\n\n#### 3) ئەڭ قەدىمىي ئىسلام ئالىي بىلىمگاھى — ئەزھەر بىلىم يۇرتى (جامعة الأزهر الشريف)\n\n"),
            ("نىزامىيە مەدرەسەسى(المدرسس النظاميس)", "\n\n#### 4) نىزامىيە مەدرەسەسى (المدرسة النظامية)\n\n"),
            ("نىَامىيە مەدرەسەسى(المدرسس النظاميس)", "\n\n#### 4) نىزامىيە مەدرەسەسى (المدرسة النظامية)\n\n"),
            ("مەدرەسە مۇستەنسىرىيە(المدرسس المستنصريس)", "\n\n#### 5) مەدرەسە مۇستەنسىرىيە (المدرسة المستنصرية)\n\n"),
            ("دارۇلھەدىس خەيرىيەت بىلىمگاھى(دار ال ديث الخيريس)", "\n\n#### 6) دارۇلھەدىس خەيرىيەت بىلىمگاھى (دار الحديث الخيرية)\n\n"),
            ("دارۇلھەدىس بىلىمگاھىنىڭد ە رسلىكلىرى", "\n\n**دارۇلھەدىس بىلىمگاھىنىڭ دەرسلىكلىرى:**\n\n"),
            ("دارۇلھەدىس بىلىمگاھىنىڭ دەرسلىكلىرى", "\n\n**دارۇلھەدىس بىلىمگاھىنىڭ دەرسلىكلىرى:**\n\n"),
            ("دارۇلھەدىس بىلىمگاھىنىڭ سىنىپلىرى", "\n\n**دارۇلھەدىس بىلىمگاھىنىڭ سىنىپلىرى:**\n\n"),
            ("دارۇلھەدىس بىلىمگاھىغا قوبۇل قىلىش شەرتلىرى دارۇلھەدىس بىلىمگاھى: غا قوبۇل قىلىش شەرتلىرى تۆۋەندىكىچە", "\n\n**دارۇلھەدىس بىلىمگاھىغا قوبۇل قىلىش شەرتلىرى:**\n\n"),
            ("دارۇلھەدىس بىلىمگاھىغا قوبۇل قىلىش شەرتلىرى", "\n\n**دارۇلھەدىس بىلىمگاھىغا قوبۇل قىلىش شەرتلىرى:**\n\n"),
            ("ئۇممۇلقۇرا ئۇنىۋېرستېتى(جاممس أم القرى)", "\n\n#### 7) ئۇممۇلقۇرا ئۇنىۋېرستېتى (جامعة أم القرى)\n\n"),
            ("ئۇممۇلقۇرا ئۇنىۋېرستېتىنىڭ اكۇلتېتلىرى", "\n\n**ئۇممۇلقۇرا ئۇنىۋېرستېتىنىڭ فاكۇلتېتلىرى ۋە شارائىتلىرى:**\n\n"),
            ("مۇھەممەد ئىبنى ئەلى سەنۇسى ئۇنىۋېرستېتى( جاممس م مد بن علي ال سنوسي)", "\n\n#### 8) مۇھەممەد ئىبنى ئەلى سەنۇسى ئۇنىۋېرستېتى (جامعة محمد بن علي السنوسي)\n\n"),
            ("مۇھەممەد ئىبنى ئەلى سەنۇسى ئۇنىۋېرستېتى", "\n\n#### 8) مۇھەممەد ئىبنى ئەلى سەنۇسى ئۇنىۋېرستېتى (جامعة محمد بن علي السنوسي)\n\n"),
            ("مەدىنە ئىسلام ئۇنىۋېرستېتى (الجاممس إلسلاميس بالمدينس المنورة)", "\n\n#### 9) مەدىنە ئىسلام ئۇنىۋېرستېتى (الجامعة الإسلامية بالمدينة المنورة)\n\n"),
            ("مەدىنە ئىسلام ئۇنىۋېرستېتىنىڭ تەمىنلىشى", "\n\n**مەدىنە ئىسلام ئۇنىۋېرستېتىنىڭ تەمىنلىشى:**\n\n"),
            ("مەدىنە ئىسلام ئۇنىۋېرستېتىغا قوبۇل قىلىش شەرتلىرى: مەدىنە ئىسلام ئۇنىۋېرستېتىغا قوبۇل قىلىش شەرتلىرى تۆۋەندىكىچە", "\n\n**مەدىنە ئىسلام ئۇنىۋېرستېتىغا قوبۇل قىلىش شەرتلىرى:**\n\n"),
            ("مەدىنە ئىسلام ئۇنىۋېرستېتىغا قوبۇل قىلىش شەرتلىرى", "\n\n**مەدىنە ئىسلام ئۇنىۋېرستېتىغا قوبۇل قىلىش شەرتلىرى:**\n\n"),
            ("تۈركىيىدىكى(ئىمام، خاتىب ئىنىستتوتىImam Hatip Lisesi )", "\n\n#### 10) تۈركىيىدىكى ئىمام-خاتىب ئىنىستىتۇتى (İmam Hatip Lisesi)\n\n"),
            ("تۈرك ىيىدىكى ئىمام، خاتىب ئىنىستتوتىنىڭ دەرسلىكلىرى", "\n\n**تۈركىيىدىكى ئىمام-خاتىب ئىنىستىتۇتىنىڭ دەرسلىكلىرى:**\n\n"),
            ("تۈركىيىدىكى ئىلاھىيات اك ۇ(لتېتلىرىIlahiyat fakulteleri )", "\n\n#### 11) تۈركىيىدىكى ئىلاھىيات فاكۇلتېتلىرى (İlahiyat Fakülteleri)\n\n"),
            ("ئىلاھىيات اك ۇ لتېتلىر ىنىڭ دەرسلىكلىرى", "\n\n**ئىلاھىيات فاكۇلتېتلىرىنىڭ دەرسلىكلىرى:**\n\n"),
            ("مالايشىيا خەلقئارا ئىسلام ئۇنىۋېرستېتى( International Islamic University Malaysia )", "\n\n#### 12) مالايشىيا خەلقئارا ئىسلام ئۇنىۋېرستېتى (International Islamic University Malaysia)\n\n"),
            ("ئىسلام ئاباد خەلقئارا ئۇنىۋېرستېتى( International Islamic University Islamabad )", "\n\n#### 13) ئىسلام ئاباد خەلقئارا ئۇنىۋېرستېتى (International Islamic University Islamabad)\n\n"),
            ("ئىسلام ئاباد خەلقئارا ئۇنىۋېرستېتىنىڭ فاكۇلتېتلىرى", "\n\n**ئىسلام ئاباد خەلقئارا ئۇنىۋېرستېتىنىڭ فاكۇلتېتلىرى:**\n\n"),
            ("ئىمان ئۇنىۋېرستېتى(جاممس اإليمان)", "\n\n#### 14) ئىمان ئۇنىۋېرستېتى (جامعة الإيمان)\n\n"),
            ("ئىمام مۇھەممەد ئىبنى سۇئۇد ئۇنىۋېرستېتى(جاممس نمام م مد بن سمود)", "\n\n#### 15) ئىمام مۇھەممەد ئىبنى سۇئۇد ئۇنىۋېرستېتى (جامعة الإمام محمد بن سعود)\n\n"),
            ("ئىمام مۇھەممەد ئىبنى سۇ ئۇد ئۇنىۋېرستېتىگە قوبۇل قىلىش شەرتلىرى: ئىمام مۇھەممەد ئىبنى سۇئۇد ئۇنىۋېرستېتىگە قوبۇل قىلىش شەرتلىرى تۆۋەندىكىچە", "\n\n**ئىمام مۇھەممەد ئىبنى سۇئۇد ئۇنىۋېرستېتىگە قوبۇل قىلىش شەرتلىرى:**\n\n"),
            ("ئامېرىكا ئوچۇق ئۇنىۋېرستېتى( the American Open Universty )", "\n\n#### 16) ئامېرىكا ئوچۇق ئۇنىۋېرستېتى (The American Open University)\n\n"),
            ("ئۇيغۇر دىيار ىدىكى بەزى مەش ھۇر ئىلىم يۇرتلىرى", "\n\n---\n\n### 3. ئۇيغۇر دىيارىدىكى بەزى مەشھۇر ئىلىم يۇرتلىرى\n\n"),
            ("خانلىق مەدرەسە قەشقەر«خانلىق مەدر ەسە »", "\n\n#### 1) خانلىق مەدرەسە (قەشقەر)\n\nقەشقەر «خانلىق مەدرەسە»"),
            ("قەشقەر«ساچىيە »مەدرەسەسى", "\n\n#### 2) ساچىيە مەدرەسەسى (قەشقەر)\n\n"),
            ("قەشقەر ساقىيە مەدرەسەسى", "\n\n#### 3) ساقىيە مەدرەسەسى (قەشقەر)\n\n"),
            ("لۈكچۈن مەدرەسەسى", "\n\n#### 4) لۈكچۈن جاھاننامە مەدرەسەسى (تۇرپان)\n\n"),
            ("دامىكۇ پۇناق مەدرەسەسى", "\n\n#### 5) دامىكۇ پۇناق مەدرەسەسى (چىرا)\n\n"),
            ("كېرىيە دۆڭ مەدرەسە", "\n\n#### 6) كېرىيە دۆڭ مەدرەسە\n\n"),
        ]
        res = full_text
        for orig, target in subs:
            if orig in res:
                res = res.replace(orig, target, 1)

        res = re.sub(r'(\(\s*\d+\s*\))', r'\n\n\1 ', res)
        res = re.sub(r'\n{3,}', '\n\n', res)
        return res.strip()

    # Populate answer lines for each question
    for idx, num in enumerate(sorted_nums):
        q = questions[num]
        start_line = q["answer_start"]
        end_line = questions[sorted_nums[idx+1]]["answer_start"] - 1 if idx + 1 < len(sorted_nums) else len(all_lines)
        raw_lines = []
        if q.get("embedded_ans"):
            raw_lines.append(q["embedded_ans"])

        for l_idx in range(start_line, min(end_line + 1, len(all_lines))):
            part, pnum, l_str = all_lines[l_idx]
            # Stop if we hit the next question number line
            if q_num_re.match(l_str) and int(q_num_re.match(l_str).group(1)) == num + 1:
                break
            # Skip page headers / footers
            if any(l_str.startswith(k) for k in ["بۆلۈم", "-بۆلۈم", ":بۆلۈم", "مۇندەرىجە", "پايدىلىنىلغان"]):
                continue
            if re.match(r"^\d{1,3}$", l_str):
                continue
            # Filter reverse running headers or corrupted header artifacts
            if any(w in l_str for w in ['ەۋ اغرلاۇئ', 'كىلتەۋىسانۇم', 'رەلىلىسەم', 'للااھ–ماراھ']):
                continue
            # Clean answer prefix
            clean_l = l_str
            m_j = jawabb_pattern.match(clean_l)
            if m_j:
                clean_l = clean_l[m_j.end():].lstrip(":").strip()
            else:
                for k in [":جاۋاب", "جاۋاب:", "جاۋاب", "ج:اۋاب", "جاۋا :ب", "جاۋ:اب", "جاۋاللهب"]:
                    if clean_l.startswith(k):
                        clean_l = clean_l[len(k):].strip()
                        break
            if clean_l:
                raw_lines.append(clean_l)

        # Separate trailing standalone subtopic headings that leaked into previous question answer
        while len(raw_lines) > 1:
            last = raw_lines[-1]
            words = last.split()
            if len(words) <= 3 and not any(last.endswith(p) for p in ['.', '،', ':', '؟', '!', '»', ')', '—', '–']):
                if any(k in last for k in ['ھالال', 'ھارام', 'مەسىلىلەر', 'ھەققىدە', 'ئەھمىيىتى', 'زۆرۈرلىكى', 'شەرتلىرى', 'تاللىنىشى', 'ئۇسۇلى', 'يىلنامىسى']):
                    raw_lines.pop()
                    continue
            break

        if num == 1887:
            q["answer"] = format_q1887_custom(raw_lines, clean_text_typography)
        else:
            # Group lines into paragraphs and list items
            paragraphs = []
            curr_p = []
            for l in raw_lines:
                is_item_start = bool(re.match(r'^\(?\s*\d+\s*[\)\.\:\-–]', l))
                if is_item_start:
                    if curr_p:
                        paragraphs.append(' '.join(curr_p))
                    curr_p = [l]
                else:
                    curr_p.append(l)
            if curr_p:
                paragraphs.append(' '.join(curr_p))

            # Format paragraphs and repair word breaks
            cleaned_paragraphs = []
            for p in paragraphs:
                cleaned_p = clean_text_typography(p)
                if cleaned_p:
                    cleaned_paragraphs.append(cleaned_p)

            q["answer"] = "\n\n".join(cleaned_paragraphs).strip()

        # Clean question title
        q_title_cleaned = clean_text_typography(q["question"])
        if not q_title_cleaned:
            q_title_cleaned = f"{num}-سوئال"
        q["question"] = q_title_cleaned

    return [questions[num] for num in sorted_nums]

def format_card(q):
    num = q["number"]
    q_text = q["question"].strip()
    ans_text = q["answer"].strip()

    # Normalize question mark
    if not q_text.endswith("؟") and not q_text.endswith("?"):
        q_text += "؟"

    card_html = f"""<div class="qa-card" id="q{num}">
  <div class="qa-question">
    <a href="#q{num}" class="qa-number-link" title="سوئال {num} گە بىۋاسىتە ئۇلىنىش"><span class="qa-number">{num}</span></a>
    <span class="qa-label">سوئال:</span>
    <span class="qa-text">{q_text}</span>
    <a href="#q{num}" class="qa-anchor" aria-label="سوئال {num} نىڭ بىۋاسىتە ئۇلىنىشى" title="بىۋاسىتە ئۇلىنىش">#</a>
  </div>
  <div class="qa-answer">
    <span class="qa-label">جاۋاب:</span> {ans_text}
  </div>
</div>"""
    return card_html

def generate_section_pages(questions):
    q_by_num = {q["number"]: q for q in questions}

    for sec in SECTIONS_CONFIG:
        sec_dir = sec["dir"]
        sec_dir.mkdir(parents=True, exist_ok=True)
        for cfg in sec["pages"]:
            start_q = cfg["start_q"]
            end_q = cfg["end_q"]
            filename = cfg["filename"]
            out_path = sec_dir / filename

            page_questions = [q_by_num[n] for n in range(start_q, end_q + 1) if n in q_by_num]
            cards = "\n\n".join(format_card(q) for q in page_questions)

            content = f"""---
title: "{cfg['title']}"
description: "{cfg['title']} — سوئال {start_q}–{end_q}"
sidebar:
  label: "{cfg['sidebar_label']}"
  order: {cfg['order']}
---

## {cfg['heading']}

{cards}
"""
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Generated {out_path} ({len(page_questions)} questions)")

def main():
    lines = extract_cleaned_lines()
    questions = extract_book2_questions(lines)

    # Save Book 2 JSON
    with open(OUTPUT_JSON_B2, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print(f"Saved Book 2 dataset to {OUTPUT_JSON_B2}")

    # Generate MDX pages for Sections 05 through 12
    generate_section_pages(questions)

    # Merge into complete extracted_2000.json
    all_2000 = []
    # 1. Load Part 1 (1-647)
    part1_json = "/Users/arslan/code/derslik/tools/extracted_2000.json"
    if os.path.exists(part1_json):
        try:
            with open(part1_json) as f:
                d = json.load(f)
                if isinstance(d, list):
                    all_2000.extend([q for q in d if q.get("number", 0) <= 647])
        except Exception as e:
            print("Notice on reading part 1:", e)
    # 2. Load Part 2 (648-821)
    part2_json = "/Users/arslan/code/derslik/tools/extracted_2000_part2.json"
    if os.path.exists(part2_json):
        with open(part2_json) as f:
            all_2000.extend(json.load(f))
    # 3. Load Part 3 (822-1317)
    part3_json = "/Users/arslan/code/derslik/tools/extracted_2000_part3.json"
    if os.path.exists(part3_json):
        with open(part3_json) as f:
            all_2000.extend(json.load(f))
    # 4. Append Book 2 (1318-2000)
    all_2000.extend(questions)

    # Sort and save unified JSON
    all_2000.sort(key=lambda x: x.get("number", 0))
    with open(OUTPUT_JSON_ALL, "w", encoding="utf-8") as f:
        json.dump(all_2000, f, ensure_ascii=False, indent=2)
    print(f"Unified dataset contains {len(all_2000)} questions (1..{all_2000[-1]['number'] if all_2000 else 0}) -> {OUTPUT_JSON_ALL}")

if __name__ == "__main__":
    main()
