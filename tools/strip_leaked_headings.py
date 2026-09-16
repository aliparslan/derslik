#!/usr/bin/env python3
"""
tools/strip_leaked_headings.py
Scans all 2000 questions and removes leaked next-question subtopic headings
and header/footnote artifacts appended to preceding answers.
Updates:
1. All MDX files in src/content/docs/2000/
2. tools/extracted_2000.json
3. tools/extracted_2000_book2.json
"""

import os
import sys
import re
import json
from pathlib import Path

ROOT = Path("/Users/arslan/code/derslik")
DOCS_ROOT = ROOT / "src" / "content" / "docs" / "2000"
JSON_ALL = ROOT / "tools" / "extracted_2000.json"
JSON_B2 = ROOT / "tools" / "extracted_2000_book2.json"

TOPIC_KEYWORDS = {
    'ھەققىدە', 'ئەھمىيىتى', 'شەرتلىرى', 'پەرقى', 'مۇناسىۋىتى', 'مۇناسىۋەتلىك', 'تۈرلىرى',
    'قائىدىلىرى', 'ھالال', 'ھارام', 'مەسىلىلەر', 'زۆرۈرلىكى', 'تاللىنىشى', 'ئۇسۇلى',
    'دەۋرى', 'دۆلىتى', 'خەلىپىلىكى', 'كېڭەش', 'ئادالەتپەرۋەرلىكى', 'ئاساسلىرى', 'ھۆكۈملىرى',
    'ئەدەپلىرى', 'خۇسۇسىيەتلىرى', 'چارىلىرى', 'سەۋەبلىرى', 'ۋەزىپىلىرى', 'ئالامەتلىرى',
    'ئورنى', 'ئاساسى'
}

FORBIDDEN_LEAK_WORDS = {
    'كەلمەكتە', 'ئاتايدۇ', 'ئىبادەتتۇر', 'چىقىرالىدى', 'ئوقۇغان', 'يېزىلغان', 'تۇرىدۇ',
    'قىلغاندا', 'شەرھلەيدۇ', 'بىرلىشەلمىگەندەك'
}

VALID_PREDICATES = [
    'ئوخشاش', 'دۇر', 'تۇر', 'ئىدى', 'بولىدۇ', 'قىلىنىدۇ', 'كېلىدۇ', 'سانىلىدۇ',
    'ئەمەس', 'كۆرسىتىدۇ', 'ئاتىغان', 'ئاتىلاتتى', 'ئېرىشىدۇ', 'گۇناھتۇر', 'قالىدۇ', 'لازىم',
    'بېرىلىدۇ', 'كېتىدۇ', 'بولمايدۇ', 'تۈرتكە', 'بولغان', 'بايقالغان', 'ئېلىنغان',
    'قىلىدۇ', 'دەيدۇ', 'كۆرىدۇ', 'ئىپادىلىنىدۇ', 'تەلەپلىرىدۇر',
    'ھارام', 'ھارامدۇر', 'يەتكۈزگەن'
]

# Explicit manual fixes for truncated endings
SPECIAL_REPAIRS = {
    648: lambda a: re.sub(r'ئەخلاق گۆزەل ياكى\)ئەخلاق ياخشى \(ئەخلاق ۋە يامان ياكى\)ئەخلاق ناچار.*$', 'ئەخلاق گۈزەل ئەخلاق (ياكى ياخشى ئەخلاق) ۋە يامان ئەخلاق (ياكى ناچار ئەخلاق) دەپ ئىككىگە بۆلۈنىدۇ.', a, flags=re.DOTALL),
    657: lambda a: re.sub(r'بۇ ئىككى پىرقىنىڭ ھېچقايسىسى ئىسلامدىن.*$', 'بۇ ئىككى پىرقىنىڭ ھېچقايسىسى ئىسلامدىن ئەمەس! سۇ بىلەن ئوت بىرلىشەلمىگەندەك، تەلەبكە لايىق ئورۇندالغان ئىبادەت بىلەن يامان ئەخلاق بىرلىشەلمەيدۇ.', a, flags=re.DOTALL),
    690: lambda a: a.strip() + ' ئەخلاقلىق ئەردۇر!' if not a.strip().endswith('ئەردۇر!') else a,
}

EXCLUDE_NUMS = {648, 657, 690, 1595, 1628, 1820, 1882, 1917, 1923}

def normalize_phrase(p):
    p = p.replace('ھا رام', 'ھارام').replace('ھا الل', 'ھالال').replace('ھاالل', 'ھالال')
    p = p.replace('بۇغۇزلاش', 'بوغۇزلاش')
    p = re.sub(r'\s+', ' ', p).strip()
    return p

def check_leak_full(raw_target, next_q):
    clean = re.sub(r'\s+', ' ', raw_target).strip()
    clean_norm = normalize_phrase(clean)
    next_norm = normalize_phrase(next_q)
    
    next_words = set(re.findall(r'[\u0600-\u06ff]+', next_norm))
    stopwords = {'قايسى', 'نېمە', 'قانداق', 'سوئال', 'ۋە', 'بىلەن', 'ئۈچۈن', 'بولامدۇ', 'بار', 'يوق', 'دەپ', 'بولسا', 'قىلىش', 'كېرەك', 'قايسىلار', 'قايسىسى'}
    meaningful_next = next_words - stopwords

    # Special case for Q1990
    if 'ئەمەۋىيلەر دەۋرى' in clean and 'خەلىپىلەر تارىخى' in clean:
        idx = clean.find('1))')
        prec = clean[:idx].strip()
        leak = clean[idx:].strip()
        if not prec.endswith('.'): prec += '.'
        return ('footnote_heading', prec, leak)

    # Check 1: After terminal punctuation (. ! ؟)
    punct_matches = list(re.finditer(r'[\.\!\؟]\s*', clean))
    if punct_matches:
        last_m = punct_matches[-1]
        last_pos = last_m.end()
        trailing = clean[last_pos:].strip()
        if trailing:
            trailing_norm = normalize_phrase(trailing)
            t_words = re.findall(r'[\u0600-\u06ff]+', trailing_norm)
            if 1 <= len(t_words) <= 16:
                if not (trailing.startswith('[') and trailing.endswith(']')):
                    if not re.match(r'^\(?\s*\d+\s*[\)\.\:\-–]', trailing):
                        if not any(fw in t_words for fw in FORBIDDEN_LEAK_WORDS):
                            overlap = set(t_words) & meaningful_next
                            stem_match = any(w in next_norm for w in t_words if len(w) >= 3 and w not in stopwords)
                            has_topic_kw = bool(set(t_words) & TOPIC_KEYWORDS)
                            if overlap or stem_match or has_topic_kw:
                                prec = clean[:last_pos].strip()
                                for fp in [') (', '()', '()1', ')']:
                                    if prec.endswith(fp) and not prec.endswith('.'):
                                        prec = prec[:-len(fp)].strip()
                                if not prec.endswith(('.', '!', '؟')):
                                    prec += '.'
                                return ('after_punct', prec, trailing)

    # Check 2: No sentence punct
    if not clean.endswith(('.', '!', '؟', '»', ')', ']')):
        words = clean.split()
        for k in range(1, min(10, len(words))):
            phrase = ' '.join(words[-k:])
            phrase_norm = normalize_phrase(phrase)
            p_words = set(re.findall(r'[\u0600-\u06ff]+', phrase_norm))
            if any(fw in p_words for fw in FORBIDDEN_LEAK_WORDS):
                continue
            overlap = p_words & meaningful_next
            stem_match = any(w in next_norm for w in p_words if len(w) >= 3 and w not in stopwords)
            has_topic_kw = bool(p_words & TOPIC_KEYWORDS)
            two_topic_kw = (len(p_words & TOPIC_KEYWORDS) >= 2)
            if (len(overlap) >= 2) or (len(overlap) >= 1 and has_topic_kw) or (stem_match and has_topic_kw) or two_topic_kw or (phrase_norm in next_norm and len(p_words) >= 1):
                prec = ' '.join(words[:-k]).strip()
                if re.search(r'\(\s*\d+\s*\)\s*$', prec):
                    continue
                prec_norm = normalize_phrase(prec)
                if any(prec_norm.endswith(v) for v in VALID_PREDICATES) or prec.endswith('.'):
                    if not prec.endswith('.'):
                        prec_clean = prec + '.'
                    else:
                        prec_clean = prec
                    return ('no_punct', prec_clean, phrase)

    # Check 3: Reverse running header at end
    words = clean.split()
    if len(words) >= 3:
        last_chunk = ' '.join(words[-15:])
        for art in ['ەدىققەھ', 'ىرىلناغىدىلوب', 'ەۋ اغرلاۇئ', 'كىلتەۋىسانۇم', 'رەلىلىسەم', 'للااھ–ماراھ', 'رۇغيۇئ ىكىدىرايىد', 'ملاسىئ ىكىدىساينۇد', 'لام اقشلازۇغۇب', 'ىكىداھىج', 'رەلىلىسەئە', 'ىھانۇگ', 'ىرىلكىلىپىلەخ']:
            if art in last_chunk:
                idx = clean.rfind(art)
                prec = clean[:idx].strip()
                if not prec.endswith(('.', '!', '؟', '»', ')')):
                    prec += '.'
                leak = clean[idx:].strip()
                return ('reverse_artifact', prec, leak)

    return None

def main():
    print("Loading MDX files...")
    card_pattern = re.compile(
        r'(<div\s+[^>]*class=["\'][^"\']*qa-card[^"\']*["\'][^>]*>[\s\S]*?)(?=<div\s+[^>]*class=["\'][^"\']*qa-card|\Z)',
        re.IGNORECASE
    )
    id_pattern = re.compile(r'id=["\']q?(\d+)["\']', re.IGNORECASE)
    question_pattern = re.compile(r'<span\s+[^>]*class=["\'][^"\']*qa-text[^"\']*["\'][^>]*>([\s\S]*?)</span>', re.IGNORECASE)
    answer_pattern = re.compile(r'<div\s+[^>]*class=["\'][^"\']*qa-answer[^"\']*["\'][^>]*>([\s\S]*?)</div>', re.IGNORECASE)

    cards = {}
    file_contents = {}
    for f in sorted(DOCS_ROOT.glob("**/*.mdx")):
        c = f.read_text(encoding="utf-8")
        file_contents[f] = c
        for m in card_pattern.finditer(c):
            block = m.group(1)
            id_m = id_pattern.search(block)
            if not id_m: continue
            q_num = int(id_m.group(1))
            qm = question_pattern.search(block)
            q_text = qm.group(1).strip() if qm else ""
            am = answer_pattern.search(block)
            a_text = am.group(1).strip() if am else ""
            cards[q_num] = {
                "file": f,
                "q_text": q_text,
                "a_text": a_text,
                "block": block
            }

    print(f"Total cards found: {len(cards)}")

    # Detect leaks and generate replacements
    repairs = {}
    # First, special repairs
    for num, fn in SPECIAL_REPAIRS.items():
        if num in cards:
            c = cards[num]
            new_a = fn(c['a_text'])
            repairs[num] = new_a
            print(f"Special repair applied to Q{num}")

    # General leak detection
    cleaned_count = 0
    for n in range(648, 2000):
        if n in EXCLUDE_NUMS:
            continue
        if n not in cards or (n+1) not in cards:
            continue
        c = cards[n]
        next_c = cards[n+1]
        raw_ans = c['a_text']
        
        # Check if answer has multiple <p> tags
        p_matches = list(re.finditer(r'<p>([\s\S]*?)</p>', raw_ans))
        if p_matches:
            target = p_matches[-1].group(1)
            is_p = True
        else:
            # Plain answer text with <span class="qa-label">جاۋاب:</span>
            m_label = re.search(r'^\s*<span[^>]*>جاۋاب:</span>\s*', raw_ans)
            if m_label:
                target = raw_ans[m_label.end():]
                prefix = raw_ans[:m_label.end()]
            else:
                target = raw_ans
                prefix = ""
            is_p = False

        res = check_leak_full(target, next_c['q_text'])
        if res:
            mode, prec, leak = res
            if is_p:
                # Replace content of last <p>
                last_m = p_matches[-1]
                new_ans = raw_ans[:last_m.start(1)] + prec + raw_ans[last_m.end(1):]
            else:
                new_ans = prefix + prec
            
            repairs[n] = new_ans
            cleaned_count += 1

    print(f"Total answers to update: {len(repairs)} (including {cleaned_count} automatic leaks)")

    # Apply updates to MDX files
    files_modified = set()
    for num, new_ans in repairs.items():
        c = cards[num]
        f = c['file']
        old_block = c['block']
        
        # Update answer inside old_block
        m_ans = answer_pattern.search(old_block)
        if not m_ans:
            print(f"WARNING: could not find qa-answer in Q{num}")
            continue
        
        # New answer block
        new_block = old_block[:m_ans.start(1)] + "\n    " + new_ans.strip() + "\n  " + old_block[m_ans.end(1):]
        # Replace old_block in file_contents[f]
        if old_block in file_contents[f]:
            file_contents[f] = file_contents[f].replace(old_block, new_block, 1)
            files_modified.add(f)
            # update cards cache
            cards[num]['block'] = new_block
            cards[num]['a_text'] = new_ans
        else:
            print(f"ERROR: old_block for Q{num} not found in {f.name}")

    # Write modified MDX files
    for f in files_modified:
        f.write_text(file_contents[f], encoding="utf-8")
        print(f"Updated {f.name}")

    print(f"Total MDX files updated: {len(files_modified)}")

    # Update JSON files
    def clean_plain_answer(a_html):
        # Extract text without html tags
        txt = re.sub(r'<span[^>]*>جاۋاب:</span>\s*', '', a_html)
        # replace <p> with \n\n
        txt = re.sub(r'</p>\s*<p>', '\n\n', txt)
        txt = re.sub(r'<[^>]+>', '', txt)
        return txt.strip()

    if JSON_ALL.exists():
        with open(JSON_ALL, "r", encoding="utf-8") as f:
            all_data = json.load(f)
        all_updated = 0
        for item in all_data:
            num = item.get("number")
            if num in repairs:
                item["answer"] = clean_plain_answer(repairs[num])
                all_updated += 1
        with open(JSON_ALL, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        print(f"Updated {all_updated} questions in tools/extracted_2000.json")

    if JSON_B2.exists():
        with open(JSON_B2, "r", encoding="utf-8") as f:
            b2_data = json.load(f)
        b2_updated = 0
        for item in b2_data:
            num = item.get("number")
            if num in repairs:
                item["answer"] = clean_plain_answer(repairs[num])
                b2_updated += 1
        with open(JSON_B2, "w", encoding="utf-8") as f:
            json.dump(b2_data, f, ensure_ascii=False, indent=2)
        print(f"Updated {b2_updated} questions in tools/extracted_2000_book2.json")

if __name__ == "__main__":
    main()
