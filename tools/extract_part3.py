#!/usr/bin/env python3
"""
tools/extract_part3.py
Extraction, normalization, and MDX generation for Book 1 Part 3
(Questions 822 through 1317 — Completing Section 03 and creating Section 04: Sehiret)
"""

import os
import sys
import re
import json
from pathlib import Path

# Add tools dir to path for imports
tools_dir = Path(__file__).parent
sys.path.append(str(tools_dir))
from extract_2000 import normalize_text, reverse_visual_rtl_line

PDF_PATH = "/Users/arslan/Desktop/2000/book1_part3.pdf"
OUTPUT_JSON = "/Users/arslan/code/derslik/tools/extracted_2000_part3.json"

DIR_03 = Path("/Users/arslan/code/derslik/src/content/docs/2000/03-exlaq")
DIR_04 = Path("/Users/arslan/code/derslik/src/content/docs/2000/04-sehiret")

# Pages configuration for Part 3
PAGES_CONFIG_03 = [
    {
        "filename": "07-rastchilliq-amanet.mdx",
        "title": "راستچىللىق ۋە ئامانەتدارلىق",
        "sidebar_label": "راستچىللىق ۋە ئامانەت (822–856)",
        "order": 7,
        "start_q": 822,
        "end_q": 856,
        "heading": "ئىسلامدا راستچىللىق، سەمىمىيلىك ۋە ئامانەتدارلىق (سوئال 822 – 856)"
    },
    {
        "filename": "08-ippet-haya-sozlesh.mdx",
        "title": "ئىپپەت-شەرم، ھايا ۋە گۈزەل سۆزلەش ئەدەبى",
        "sidebar_label": "ئىپپەت، ھايا ۋە سۆز ئەدەبى (857–893)",
        "order": 8,
        "start_q": 857,
        "end_q": 893,
        "heading": "شەرم-ھايا، ئىپپەت ۋە تىلنى پاك تۇتۇش ئەدەپلىرى (سوئال 857 – 893)"
    },
    {
        "filename": "09-keng-qorsaq-sexiylik.mdx",
        "title": "كەڭ قورساقلىق، ئەپۇچانلىق ۋە مەردلىك",
        "sidebar_label": "كەڭ قورساقلىق ۋە مەردلىك (894–933)",
        "order": 9,
        "start_q": 894,
        "end_q": 933,
        "heading": "كەڭ قورساقلىق، ئەپۇچانلىق، كېچىرىمچانلىق ۋە مەردلىك (سوئال 894 – 933)"
    },
    {
        "filename": "10-dastixan-muhit-etika.mdx",
        "title": "داستىخان، كېسەل يوقلاش ۋە پاكىزلىق ئەدەپلىرى",
        "sidebar_label": "داستىخان ۋە كۈندىلىك ئەدەپلەر (934–967)",
        "order": 10,
        "start_q": 934,
        "end_q": 967,
        "heading": "داستىخان، كېسەل يوقلاش، سورۇن ۋە مۇھىت پاكىزلىقى (سوئال 934 – 967)"
    },
]

PAGES_CONFIG_04 = [
    {
        "filename": "01-makka-dewri.mdx",
        "title": "جاھىلىيەت دەۋرى، پەيغەمبەرلىك ۋە مەككە دەۋرى",
        "sidebar_label": "جاھىلىيەت ۋە مەككە دەۋرى (968–1019)",
        "order": 1,
        "start_q": 968,
        "end_q": 1019,
        "heading": "جاھىلىيەت دەۋرى، رەسۇلۇللاھنىڭ دۇنياغا كېلىشى ۋە مەككە دەۋرى (سوئال 968 – 1019)"
    },
    {
        "filename": "02-hijret-medine-gazatlar.mdx",
        "title": "ھىجرەت، مەدىنە دەۋرى ۋە دەسلەپكى غازاتلار",
        "sidebar_label": "ھىجرەت ۋە دەسلەپكى غازاتلار (1020–1060)",
        "order": 2,
        "start_q": 1020,
        "end_q": 1060,
        "heading": "ھىجرەت، مەدىنە دەۋرى ۋە ئىسلام تارىخىدىكى دەسلەپكى غازاتلار (سوئال 1020 – 1060)"
    },
    {
        "filename": "03-xendek-fetih-wapat.mdx",
        "title": "خەندەك غازىتى، پەتھى مەككە ۋە رەسۇلۇللاھنىڭ ۋاپاتى",
        "sidebar_label": "خەندەك، پەتھى ۋە ۋاپات (1061–1092)",
        "order": 3,
        "start_q": 1061,
        "end_q": 1092,
        "heading": "خەندەك غازىتى، ھۇدەيبىيە، مەككىنىڭ پەتھى ۋە رەسۇلۇللاھنىڭ ۋاپاتى (سوئال 1061 – 1092)"
    },
    {
        "filename": "04-ijtimaiy-munasiwetler-qoshna.mdx",
        "title": "ئائىلە، قوشنىدارلىق ۋە ئىجتىمائىي مۇناسىۋەتلەر",
        "sidebar_label": "ئائىلە ۋە قوشنىدارلىق (1093–1140)",
        "order": 4,
        "start_q": 1093,
        "end_q": 1140,
        "heading": "ئاتا-ئانا، سىلە-رەھىم، قوشنىدارلىق ۋە ئىجتىمائىي مۇناسىۋەتلەر (سوئال 1093 – 1140)"
    },
    {
        "filename": "05-soda-iqtisad-muamile.mdx",
        "title": "سودا-سېتىق ۋە مال-مۈلۈك مۇئامىلىلىرى",
        "sidebar_label": "سودا ۋە ئىقتىسادىي ئەھكام (1141–1230)",
        "order": 5,
        "start_q": 1141,
        "end_q": 1230,
        "heading": "ئىسلام فىقھىسىدا سودا-سېتىق، ئىقتىساد ۋە پۇل-مۇئامىلە ئەھكاملىرى (سوئال 1141 – 1230)"
    },
    {
        "filename": "06-qesem-nezir-kapparet.mdx",
        "title": "قەسەم، نەزىر ۋە ئۇلارنىڭ كاپارىتى",
        "sidebar_label": "قەسەم ۋە كاپارەت (1231–1317)",
        "order": 6,
        "start_q": 1231,
        "end_q": 1317,
        "heading": "قەسەم ۋە نەزىر ئەھكاملىرى، قەسەمنى بۇزۇشنىڭ كاپارىتى (سوئال 1231 – 1317)"
    },
]

def extract_part3_questions():
    import fitz
    
    doc = fitz.open(PDF_PATH)
    print(f"Loaded {PDF_PATH} ({len(doc)} pages)")
    
    doc_lines = []
    for p_idx, page in enumerate(doc):
        raw = page.get_text("text")
        for line in raw.splitlines():
            l_str = line.strip()
            if not l_str:
                continue
            rev = reverse_visual_rtl_line(l_str)
            norm = normalize_text(rev)
            if norm:
                doc_lines.append((p_idx + 1, norm))
                
    print(f"Total processed lines: {len(doc_lines)}")
    
    q_re1 = re.compile(r'^(?:\.|\b)?(\d{3,4})(?:\.|\b)?\s*[:\.]?\s*سوئال[:\.\s]*(.*)$')
    q_re2 = re.compile(r'^سوئال[:\.\s]*(.*)\s+(?:\.|\b)?(\d{3,4})(?:\.|\b)?$')
    q_re3 = re.compile(r'^سوئال[:\.\s]*(\d{3,4})[:\.\s]*(.*)$')
    q_re4 = re.compile(r'^(?:\.|\b)?(\d{3,4})\s+(.*?):سوئال\s*(.*)$')
    ans_start_re = re.compile(r'^(?:جاۋاب|:جاۋاب|جاۋاب:)[:\.\s]*(.*)$')
    
    questions = {}
    current_q = None
    in_answer = False
    
    i = 0
    while i < len(doc_lines):
        p_num, line = doc_lines[i]
        i += 1
        
        # Skip headers
        if any(line.startswith(p) for p in ['بۆلۈم-3', 'بۆلۆم-3', 'بۆلۈم-4', 'بۆلۆم-4', 'پايدىلىنىلغان']):
            continue
        if re.match(r'^\d{1,3}$', line):
            continue
            
        num = None
        q_text = ''
        
        m1 = q_re1.match(line)
        m2 = q_re2.match(line)
        m3 = q_re3.match(line)
        m4 = q_re4.match(line)
        
        if m1:
            num = int(m1.group(1))
            q_text = m1.group(2).strip()
        elif m2:
            num = int(m2.group(2))
            q_text = m2.group(1).strip()
        elif m3:
            num = int(m3.group(1))
            q_text = m3.group(2).strip()
        elif m4:
            num = int(m4.group(1))
            q_text = (m4.group(2) + ' ' + m4.group(3)).strip()
        elif 'سوئال' in line:
            m_num = re.search(r'\b(\d{3,4})\b', line)
            if m_num:
                num = int(m_num.group(1))
                q_text = line.replace('سوئال:', '').replace('سوئال', '').replace(str(num), '').strip()
            elif i < len(doc_lines):
                next_p, next_l = doc_lines[i]
                m_next = re.match(r'^(?:\.|\b)?(\d{3,4})(?:\.|\b)?$', next_l.strip())
                if m_next:
                    num = int(m_next.group(1))
                    q_text = line.replace('سوئال:', '').replace('سوئال', '').strip()
                    i += 1
                    if i < len(doc_lines):
                        after_p, after_l = doc_lines[i]
                        if not after_l.startswith('جاۋاب') and not after_l.startswith(':جاۋاب'):
                            q_text += ' ' + after_l.strip()
                            i += 1
        elif re.match(r'^(?:\.|\b)?(\d{3,4})(?:\.|\b)?$', line):
            cand_num = int(re.match(r'^(?:\.|\b)?(\d{3,4})(?:\.|\b)?$', line).group(1))
            if 822 <= cand_num <= 1320 and i < len(doc_lines):
                next_p, next_l = doc_lines[i]
                if not next_l.startswith('جاۋاب') and not next_l.startswith(':جاۋاب'):
                    num = cand_num
                    q_text = next_l.replace('سوئال:', '').replace('سوئال', '').strip()
                    i += 1
                    
        if num and 822 <= num <= 1317:
            if current_q:
                questions[current_q['number']] = current_q
            current_q = {
                'number': num,
                'question': q_text,
                'answer': '',
                'page': p_num,
                'book_page': p_num + 404,
            }
            in_answer = False
            continue
            
        m_ans = ans_start_re.match(line)
        if m_ans and current_q:
            in_answer = True
            current_q['answer'] = m_ans.group(1).strip()
            continue
            
        if current_q:
            if in_answer:
                if current_q['answer']:
                    current_q['answer'] += ' ' + line
                else:
                    current_q['answer'] = line
            else:
                if current_q['question']:
                    current_q['question'] += ' ' + line
                else:
                    current_q['question'] = line

    if current_q:
        questions[current_q['number']] = current_q

    sorted_q = [questions[n] for n in sorted(questions.keys())]
    print(f"Extracted {len(sorted_q)} questions (Q{sorted_q[0]['number']} to Q{sorted_q[-1]['number']})")
    
    missing = set(range(822, 1318)) - set(questions.keys())
    if missing:
        print(f"WARNING: Missing questions: {missing}")
    else:
        print("PERFECT: All questions 822 through 1317 are present and contiguous!")
        
    return sorted_q

def format_card(q):
    num = q["number"]
    q_text = q["question"].strip()
    ans_text = q["answer"].strip()
    
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

def generate_pages(questions, config, target_dir):
    target_dir.mkdir(parents=True, exist_ok=True)
    q_by_num = {q["number"]: q for q in questions}
    
    for cfg in config:
        start_q = cfg["start_q"]
        end_q = cfg["end_q"]
        filename = cfg["filename"]
        out_path = target_dir / filename
        
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
    questions = extract_part3_questions()
    
    # Save JSON dataset
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print(f"Saved dataset to {OUTPUT_JSON}")
    
    # Generate MDX pages for Section 03 (07-10)
    generate_pages(questions, PAGES_CONFIG_03, DIR_03)
    
    # Generate MDX pages for Section 04 (01-06)
    generate_pages(questions, PAGES_CONFIG_04, DIR_04)
    
    print("All MDX files for Part 3 successfully created!")

if __name__ == "__main__":
    main()
