#!/usr/bin/env python3
"""
tools/extract_part2.py
Extraction, normalization, and MDX generation for Book 1 Part 2
(Questions 648 through 821 — Section 03: Exlaq)
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

PDF_PATH = "/Users/arslan/Desktop/2000/book1_part2.pdf"
OUTPUT_JSON = "/Users/arslan/code/derslik/tools/extracted_2000_part2.json"
TARGET_DIR = Path("/Users/arslan/code/derslik/src/content/docs/2000/03-exlaq")

# Definition of the 6 canonical pages for Section 03
PAGES_CONFIG = [
    {
        "filename": "01-exlaq-omumiy-bayan.mdx",
        "title": "ئەخلاق ھەققىدە ئومۇمىي بايان",
        "sidebar_label": "ئەخلاق ھەققىدە ئومۇمىي بايان (648–673)",
        "order": 1,
        "start_q": 648,
        "end_q": 673,
        "heading": "ئەخلاق ھەققىدە ئومۇمىي چۈشەنچە ۋە ئۇنىڭ قىممىتى (سوئال 648 – 673)"
    },
    {
        "filename": "02-exlaq-turler-terepiler.mdx",
        "title": "ئەخلاقنىڭ تۈرلىرى ۋە شەخسىي-ئىجتىمائىي تەرەپلىرى",
        "sidebar_label": "ئەخلاقنىڭ تۈرلىرى ۋە تەرەپلىرى (674–717)",
        "order": 2,
        "start_q": 674,
        "end_q": 717,
        "heading": "ئەخلاقنىڭ مۇناسىۋىتى ئېتىبارى بىلەن تۈرلىنىشى (سوئال 674 – 717)"
    },
    {
        "filename": "03-peyghamber-exlaqi.mdx",
        "title": "پەيغەمبەر ئەلەيھىسسالامنىڭ ئەخلاقىدىن ئۆرنەكلەر",
        "sidebar_label": "پەيغەمبەر ئەلەيھىسسالامنىڭ ئەخلاقى (718–746)",
        "order": 3,
        "start_q": 718,
        "end_q": 746,
        "heading": "رەسۇلۇللاھنىڭ گۈزەل ئەخلاقى ۋە ئىنسانىي ئۆرنەكلىرى (سوئال 718 – 746)"
    },
    {
        "filename": "04-soygu-ve-qimmiti.mdx",
        "title": "سۆيگۈ ۋە ئۇنىڭ قىممىتى",
        "sidebar_label": "سۆيگۈ ۋە ئۇنىڭ قىممىتى (747–779)",
        "order": 4,
        "start_q": 747,
        "end_q": 779,
        "heading": "ئىسلامدا سۆيگۈ-مۇھەببەت ۋە قېرىنداشلىق قىممەتلىرى (سوئال 747 – 779)"
    },
    {
        "filename": "05-ihsan-ata-ana-soz.mdx",
        "title": "ئېھسان ۋە ئۇنىڭ ئەھمىيىتى (ئاتا-ئانا ۋە ئائىلە)",
        "sidebar_label": "ئېھسان: ئاتا-ئانا، ئائىلە ۋە سۆز (780–804)",
        "order": 5,
        "start_q": 780,
        "end_q": 804,
        "heading": "ئاتا-ئانا، ئۇرۇق-تۇغقان ۋە كىشىلىك مۇناسىۋەتلەردە ئېھسان (سوئال 780 – 804)"
    },
    {
        "filename": "06-rehim-shepqet.mdx",
        "title": "رەھىم-شەپقەت ۋە ئۇنىڭ يوللىرى",
        "sidebar_label": "رەھىم-شەپقەت ۋە ئۇنىڭ يوللىرى (805–821)",
        "order": 6,
        "start_q": 805,
        "end_q": 821,
        "heading": "ئىسلام دىنىدا شەپقەت، رەھىمدىللىك ۋە ياردەملىشىش (سوئال 805 – 821)"
    },
]

def extract_part2_questions():
    import fitz
    
    doc = fitz.open(PDF_PATH)
    print(f"Loaded {PDF_PATH} ({len(doc)} pages)")
    
    # Collect all lines with page number
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
    
    # Question regex patterns
    # Handles .NNN سوئال: ..., NNN. سوئال: ..., سوئال: ... .NNN, etc.
    q_start_re1 = re.compile(r'^(?:\.|\b)?(\d{3,4})(?:\.|\b)?\s*[:\.]?\s*سوئال[:\.\s]*(.*)$')
    q_start_re2 = re.compile(r'^سوئال[:\.\s]*(.*)\s+(?:\.|\b)?(\d{3,4})(?:\.|\b)?$')
    q_start_re3 = re.compile(r'^سوئال[:\.\s]*(\d{3,4})[:\.\s]*(.*)$')
    
    ans_start_re = re.compile(r'^(?:جاۋاب|:جاۋاب|جاۋاب:)[:\.\s]*(.*)$')
    
    questions = []
    current_q = None
    in_answer = False
    
    i = 0
    while i < len(doc_lines):
        p_num, line = doc_lines[i]
        i += 1
        
        # Skip running headers and standalone page numbers
        if line.startswith("بۆلۈم-3") or line.startswith("بۆلۆم-3") or "ئەخلاق" in line and len(line.split()) <= 3:
            continue
        if re.match(r'^\d{1,3}$', line):
            continue
        if "ئائىلە ھاياتىدىكى يۈرۈش – تۇرۇش ئەدەبلىرى" in line or "ئەدەب – ئەخلاقلار" in line:
            continue
            
        # Check if line matches Question pattern
        m1 = q_start_re1.match(line)
        m2 = q_start_re2.match(line)
        m3 = q_start_re3.match(line)
        
        # Special check for split lines like line 1: سوئال: ..., line 2: .712, line 3: text
        num = None
        q_text = ""
        
        if m1:
            num = int(m1.group(1))
            q_text = m1.group(2).strip()
        elif m2:
            num = int(m2.group(2))
            q_text = m2.group(1).strip()
        elif m3:
            num = int(m3.group(1))
            q_text = m3.group(2).strip()
        elif "سوئال:" in line or line.startswith("سوئال"):
            # Check next line for number (like Q712)
            if i < len(doc_lines):
                next_p, next_l = doc_lines[i]
                m_next = re.match(r'^(?:\.|\b)?(\d{3,4})(?:\.|\b)?$', next_l.strip())
                if m_next:
                    num = int(m_next.group(1))
                    q_text = line.replace("سوئال:", "").replace("سوئال", "").strip()
                    i += 1  # consume next line
                    # check if line after has remaining question text
                    if i < len(doc_lines):
                        after_p, after_l = doc_lines[i]
                        if not after_l.startswith("جاۋاب") and not after_l.startswith(":جاۋاب"):
                            q_text += " " + after_l.strip()
                            i += 1
                            
        # Validate question number
        if num and 648 <= num <= 821:
            if current_q:
                questions.append(current_q)
            current_q = {
                "number": num,
                "question": q_text,
                "answer": "",
                "page": p_num,
                "book_page": p_num + 295,
            }
            in_answer = False
            continue
            
        # Check if line starts Answer
        m_ans = ans_start_re.match(line)
        if m_ans and current_q:
            in_answer = True
            ans_text = m_ans.group(1).strip()
            if ans_text:
                current_q["answer"] = ans_text
            continue
            
        # Continuation of Question or Answer
        if current_q:
            if in_answer:
                if current_q["answer"]:
                    current_q["answer"] += " " + line
                else:
                    current_q["answer"] = line
            else:
                if current_q["question"]:
                    current_q["question"] += " " + line
                else:
                    current_q["question"] = line
                    
    if current_q:
        questions.append(current_q)
        
    print(f"Extracted {len(questions)} raw question records.")
    
    # Sort and deduplicate / verify
    q_map = {}
    for q in questions:
        num = q["number"]
        if num not in q_map or len(q["answer"]) > len(q_map[num]["answer"]):
            q_map[num] = q
            
    sorted_q = [q_map[n] for n in sorted(q_map.keys())]
    print(f"Unique questions extracted: {len(sorted_q)} (from Q{sorted_q[0]['number']} to Q{sorted_q[-1]['number']})")
    
    missing = [n for n in range(648, 822) if n not in q_map]
    if missing:
        print(f"WARNING: Missing questions: {missing}")
    else:
        print("PERFECT: All questions 648 through 821 are present and contiguous!")
        
    return sorted_q

def format_card(q):
    num = q["number"]
    q_text = q["question"].strip()
    ans_text = q["answer"].strip()
    
    # Clean question text if it still has trailing punctuation or question mark issues
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

def generate_mdx_files(questions):
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    q_by_num = {q["number"]: q for q in questions}
    
    for cfg in PAGES_CONFIG:
        start_q = cfg["start_q"]
        end_q = cfg["end_q"]
        filename = cfg["filename"]
        out_path = TARGET_DIR / filename
        
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
    questions = extract_part2_questions()
    
    # Save JSON dataset
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print(f"Saved dataset to {OUTPUT_JSON}")
    
    # Generate MDX pages
    generate_mdx_files(questions)
    print("All MDX files for Section 03 (03-exlaq) successfully created!")

if __name__ == "__main__":
    main()
