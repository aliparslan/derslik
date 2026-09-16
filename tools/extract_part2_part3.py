#!/usr/bin/env python3
"""
Extract Questions 648 through 1317 from Part 2 and Part 3 PDFs of Book 1:
- Part 2: media_1789518383477.pdf (Questions 648 to 821)
- Part 3: media_1789518392661.pdf (Questions 822 to 1317)
Integrates and appends to tools/extracted_2000.json.
"""

import os
import re
import json
import unicodedata
import fitz

PART2_PDF = "/Users/arslan/.gemini/antigravity/brain/4cef4897-f493-4acb-b5ac-2ecb06b0aee7/.user_uploaded/media_1789518383477.pdf"
PART3_PDF = "/Users/arslan/.gemini/antigravity/brain/4cef4897-f493-4acb-b5ac-2ecb06b0aee7/.user_uploaded/media_1789518392661.pdf"
EXTRACTED_JSON = "/Users/arslan/code/derslik/tools/extracted_2000.json"

CUSTOM_CHAR_MAP = {
    # Legacy Uyghur glyphs
    0x066E: 0x0649,  # Dotless beh -> Uyghur ى (\u0649)
    0x067B: 0x06D0,  # Beeh with 2 vertical dots -> Uyghur ې (\u06d0)
    0x06CC: 0x064A,  # Farsi Yeh -> Standard Yeh ي (\u064a)
    0x06C5: 0x06AD,  # Kirghiz Oe in legacy fonts -> Uyghur ڭ (\u06ad)
    
    # Arabic Presentation Forms-A (FB50-FDFF)
    0xFB56: 0x067E, 0xFB57: 0x067E, 0xFB58: 0x067E, 0xFB59: 0x067E,  # Peh (پ)
    0xFB7A: 0x0686, 0xFB7B: 0x0686, 0xFB7C: 0x0686, 0xFB7D: 0x0686,  # Cheh (چ)
    0xFB7E: 0x0686, 0xFB7F: 0x0686,
    0xFB8A: 0x0698, 0xFB8B: 0x0698,                                    # Jeh (ژ)
    0xFB92: 0x06AF, 0xFB93: 0x06AF, 0xFB94: 0x06AF, 0xFB95: 0x06AF,  # Gaf (گ)
    0xFBD3: 0x06AD, 0xFBD4: 0x06AD, 0xFBD5: 0x06AD, 0xFBD6: 0x06AD,  # Ngeh (ڭ)
    0xFBD7: 0x06C7, 0xFBD8: 0x06C7,                                    # U (ۇ)
    0xFBDA: 0x06C6, 0xFBDB: 0x06C6,                                    # Oe (ۆ)
    0xFBDC: 0x06C8, 0xFBDD: 0x06C8,                                    # Yu (ۈ)
    0xFBDE: 0x06CB, 0xFBDF: 0x06CB,                                    # Ve (ۋ)
    0xFBE4: 0x06D0, 0xFBE5: 0x06D0, 0xFBE6: 0x06D0, 0xFBE7: 0x06D0,  # E (ې)
    0xFBFC: 0x064A, 0xFBFD: 0x064A, 0xFBFE: 0x064A, 0xFBFF: 0x064A,  # Farsi Yeh -> ي
    
    # Common Presentation Forms-B (FE70-FEFF)
    0xFE8B: 0x0626, 0xFE8C: 0x0626,  # Hamza on Yeh (ئ)
    0xFE8D: 0x0627, 0xFE8E: 0x0627,  # Alef (ا)
    0xFE8F: 0x0628, 0xFE90: 0x0628, 0xFE91: 0x0628, 0xFE92: 0x0628,  # Beh (ب)
    0xFE93: 0x0629, 0xFE94: 0x0629,  # Teh Marbuta (ة)
    0xFE95: 0x062A, 0xFE96: 0x062A, 0xFE97: 0x062A, 0xFE98: 0x062A,  # Teh (ت)
    0xFE99: 0x062B, 0xFE9A: 0x062B, 0xFE9B: 0x062B, 0xFE9C: 0x062B,  # Theh (ث)
    0xFE9D: 0x062C, 0xFE9E: 0x062C, 0xFE9F: 0x062C, 0xFEA0: 0x062C,  # Jeem (ج)
    0xFEA1: 0x062D, 0xFEA2: 0x062D, 0xFEA3: 0x062D, 0xFEA4: 0x062D,  # Hah (ح)
    0xFEA5: 0x062E, 0xFEA6: 0x062E, 0xFEA7: 0x062E, 0xFEA8: 0x062E,  # Khah (خ)
    0xFEA9: 0x062F, 0xFEAA: 0x062F,  # Dal (د)
    0xFEAB: 0x0630, 0xFEAC: 0x0630,  # Thal (ذ)
    0xFEAD: 0x0631, 0xFEAE: 0x0631,  # Reh (ر)
    0xFEAF: 0x0632, 0xFEB0: 0x0632,  # Zain (ز)
    0xFEB1: 0x0633, 0xFEB2: 0x0633, 0xFEB3: 0x0633, 0xFEB4: 0x0633,  # Seen (س)
    0xFEB5: 0x0634, 0xFEB6: 0x0634, 0xFEB7: 0x0634, 0xFEB8: 0x0634,  # Sheen (ش)
    0xFEB9: 0x0635, 0xFEBA: 0x0635, 0xFEBB: 0x0635, 0xFEBC: 0x0635,  # Sad (ص)
    0xFEBD: 0x0636, 0xFEBE: 0x0636, 0xFEBF: 0x0636, 0xFEC0: 0x0636,  # Dad (ض)
    0xFEC1: 0x0637, 0xFEC2: 0x0637, 0xFEC3: 0x0637, 0xFEC4: 0x0637,  # Tah (ط)
    0xFEC5: 0x0638, 0xFEC6: 0x0638, 0xFEC7: 0x0638, 0xFEC8: 0x0638,  # Zah (ظ)
    0xFEC9: 0x0639, 0xFECA: 0x0639, 0xFECB: 0x0639, 0xFECC: 0x0639,  # Ain (ع)
    0xFECD: 0x063A, 0xFECE: 0x063A, 0xFECF: 0x063A, 0xFED0: 0x063A,  # Ghain (غ)
    0xFED1: 0x0641, 0xFED2: 0x0641, 0xFED3: 0x0641, 0xFED4: 0x0641,  # Feh (ف)
    0xFED5: 0x0642, 0xFED6: 0x0642, 0xFED7: 0x0642, 0xFED8: 0x0642,  # Qaf (ق)
    0xFED9: 0x0643, 0xFEDA: 0x0643, 0xFEDB: 0x0643, 0xFEDC: 0x0643,  # Kaf (ك)
    0xFEDD: 0x0644, 0xFEDE: 0x0644, 0xFEDF: 0x0644, 0xFEE0: 0x0644,  # Lam (ل)
    0xFEE1: 0x0645, 0xFEE2: 0x0645, 0xFEE3: 0x0645, 0xFEE4: 0x0645,  # Meem (م)
    0xFEE5: 0x0646, 0xFEE6: 0x0646, 0xFEE7: 0x0646, 0xFEE8: 0x0646,  # Noon (ن)
    0xFEE9: 0x0647, 0xFEEA: 0x0647, 0xFEEB: 0x0647, 0xFEEC: 0x0647,  # Heh (ه)
    0xFEED: 0x0648, 0xFEEE: 0x0648,                                    # Waw (و)
    0xFEEF: 0x0649, 0xFEF0: 0x0649,                                    # Alef Maksura (ى)
    0xFEF1: 0x064A, 0xFEF2: 0x064A, 0xFEF3: 0x064A, 0xFEF4: 0x064A,  # Yeh (ي)
}

MULTI_CHAR_MAP = {
    0xFEFB: "\u0644\u0627", 0xFEFC: "\u0644\u0627",  # Lam-Alef
    0xFEF7: "\u0644\u0623", 0xFEF8: "\u0644\u0623",  # Lam-Alef Hamza Above
    0xFEF9: "\u0644\u0625", 0xFEFA: "\u0644\u0625",  # Lam-Alef Hamza Below
    0xFEF5: "\u0644\u0622", 0xFEF6: "\u0644\u0622",  # Lam-Alef Madda Above
}

def normalize_text(text: str) -> str:
    if not text:
        return ""
    
    # Replace multi-char presentation forms first
    for k, v in MULTI_CHAR_MAP.items():
        text = text.replace(chr(k), v)
        
    chars = []
    for c in text:
        cp = ord(c)
        if cp in CUSTOM_CHAR_MAP:
            chars.append(chr(CUSTOM_CHAR_MAP[cp]))
        else:
            chars.append(c)
    s = "".join(chars)
    
    s = unicodedata.normalize("NFKC", s)
    
    # Strip interior tatweel/kashida from Uyghur/Arabic words
    prev = ""
    while prev != s:
        prev = s
        s = re.sub(r'([\u0600-\u06FF])\u0640+([\u0600-\u06FF])', r'\1\2', s)
        
    s = s.replace("\u066e", "\u0649")
    s = s.replace("\u067b", "\u06d0")
    s = s.replace("\u06cc", "\u064a")
    s = s.replace("\u06c5", "\u06ad")
    
    # Fix known font artifacts
    s = s.replace("ا:", "الله")
    s = s.replace("صhة", "صلاة")
    
    return s

def clean_rtl_word_punctuation(word: str) -> str:
    w = word.strip()
    if not w:
        return ""
    if w.startswith(":") and len(w) > 1 and not w.endswith(":"):
        w = w[1:] + ":"
    if w.startswith("،") and len(w) > 1 and not w.endswith("،"):
        w = w[1:] + "،"
    if w.startswith(".") and len(w) > 1 and not w.endswith(".") and not re.match(r'^\.\d+$', w):
        w = w[1:] + "."
    return w

def reverse_visual_rtl_line(line: str) -> str:
    line = line.strip()
    if not line:
        return ""
    words = line.split()
    if not words:
        return ""
    rev_words = words[::-1]
    cleaned_words = [clean_rtl_word_punctuation(w) for w in rev_words]
    return " ".join(cleaned_words)

DIVISIONS = [
    # 03-exlaq
    {"slug": "01-exlaq-esasliri", "section": "03-exlaq", "title": "ئەخلاق ھەققىدە ئومۇمىي بايان ۋە ئۇنىڭ ئەھمىيىتى", "start": 648, "end": 673},
    {"slug": "02-neps-ve-roh", "section": "03-exlaq", "title": "نەپس، روھ ۋە نەپسنى پاكلاش چارىلىرى", "start": 674, "end": 694},
    {"slug": "03-exlaq-olchemliri", "section": "03-exlaq", "title": "ئەخلاقنى ئۆلچەيدىغان ئومۇمىي پىرىنسىپلار ۋە خۇلق بىلەن ئەدەبنىڭ پەرقى", "start": 695, "end": 716},
    {"slug": "04-horriyet-heqler", "section": "03-exlaq", "title": "ھۆررىيەتنىڭ چېكى، ئىنساننىڭ ھوقۇقلىرى ۋە شەيتاننىڭ تەسىرى", "start": 717, "end": 726},
    {"slug": "05-exlaq-yildurush", "section": "03-exlaq", "title": "تەبىئىي ئەخلاق، تەربىيە ۋە گۈزەل ئەخلاقلارنى يېتىلدۈرۈش چارىلىرى", "start": 727, "end": 741},
    {"slug": "06-exlaqiy-burchlar", "section": "03-exlaq", "title": "بىزنىڭ ئەخلاقىي بۇرچىمىز ۋە پەيغەمبەر ئەلەيھىسسالامنىڭ ئەخلاقىدىن ئۆرنەكلەر", "start": 742, "end": 769},
    {"slug": "07-soygv-heqiqet-adalet", "section": "03-exlaq", "title": "سۆيگۈ، ھەقىقەتنى سۆيۈش ۋە ئادالەت تەلەپلىرى", "start": 770, "end": 792},
    {"slug": "08-ihsan-rehim-shepqet", "section": "03-exlaq", "title": "ئىھسان ۋە رەھىم-شەپقەت پەزىلەتلىرى", "start": 793, "end": 821},
    {"slug": "09-rastchillik-amanet", "section": "03-exlaq", "title": "راستچىللىق ۋە ئامانەت خىسلەتلىرى", "start": 822, "end": 850},
    {"slug": "10-vapadarliq-shukvr", "section": "03-exlaq", "title": "ۋاپادارلىق، شەرم-ھايا، سەۋرچانلىق ۋە شۈكۈر تۈرلىرى", "start": 851, "end": 891},
    {"slug": "11-edeblik-sozlesh-keng-qorsaq", "section": "03-exlaq", "title": "ئەدەبلىك سۆزلەش، مۇنازىرە ئەدەپلىرى ۋە كەڭ قورساق بولۇش", "start": 892, "end": 904},
    {"slug": "12-inaqliq-vaqit-himmet-umid", "section": "03-exlaq", "title": "ئىناقلىق، ۋاقىتنى قەدرىلەش، ئالىي ھىممەت ۋە ئۈمىد", "start": 905, "end": 917},
    {"slug": "13-pakizliq-muhit-ixlas", "section": "03-exlaq", "title": "پاكىزلىق، مۇھىت ئاسراش ۋە ئىخلاس گۈزەللىكى", "start": 918, "end": 929},
    {"slug": "14-kemterlik-pidakarliq-merdlik", "section": "03-exlaq", "title": "كەمتەرلىك، پىداكارلىق، مەردلىك ۋە بېخىللىق", "start": 930, "end": 948},
    {"slug": "15-salam-surun-dastixan-edebliri", "section": "03-exlaq", "title": "سالاملىشىش، سورۇن، داستىخان، ئۆيگە كىرىش ۋە ئائىلە ئەدەپلىرى", "start": 949, "end": 967},

    # 04-siyret
    {"slug": "01-islamdin-burun-ve-baliliq", "section": "04-siyret", "title": "ئىسلامدىن بۇرۇنقى ۋەزىيەت، دۇنياغا كېلىشى ۋە بالىلىق دەۋرى", "start": 968, "end": 994},
    {"slug": "02-peyghemberlik-ve-mekke-dewri", "section": "04-siyret", "title": "پەيغەمبەرلىكنىڭ بېرىلىشى، دەۋەتنىڭ باشلىنىشى ۋە مەككە دەۋرى", "start": 995, "end": 1019},
    {"slug": "03-hijret-ve-medine-dewri", "section": "04-siyret", "title": "ھىجرەت ۋە تۇنجى ئىسلام دۆلىتىنىڭ قۇرۇلۇشى", "start": 1020, "end": 1031},
    {"slug": "04-ghazatlar-ve-tinchliq", "section": "04-siyret", "title": "غازاتلار، تىنچلىق پىرىنسىپى ۋە مەككىنىڭ ئازات قىلىنىشى", "start": 1032, "end": 1060},
    {"slug": "05-vida-hejji-ve-vapat", "section": "04-siyret", "title": "ۋىدا ھەججى، پەيغەمبەر ئەلەيھىسسالامنىڭ ۋاپاتى ۋە خەلىپىلەر دەۋرى", "start": 1061, "end": 1070},

    # 05-muamile
    {"slug": "01-muamile-esasliri", "section": "05-muamile", "title": "مۇئامىلە ھەققىدە قىسقىچە چۈشەنچە ۋە پىرىنسىپلار", "start": 1071, "end": 1074},
    {"slug": "02-er-ayal-ve-burchlar", "section": "05-muamile", "title": "ئەر ۋە ئايالنىڭ ئۆزئارا ئۆتەشكە تېگىشلىك بۇرچلىرى", "start": 1075, "end": 1076},
    {"slug": "03-ata-ana-ve-perzent-heqliri", "section": "05-muamile", "title": "ئاتا-ئانا ۋە پەرزەنت ھەقلىرى، ئەقىقە، خەتنە توي", "start": 1077, "end": 1089},
    {"slug": "04-tughqan-qoshna-dostlar", "section": "05-muamile", "title": "تۇغقانلار، قوشنىلار، خىزمەتداشلار ۋە دوستلارغا مۇئامىلە", "start": 1090, "end": 1099},
    {"slug": "05-insanlar-ve-haywanlar", "section": "05-muamile", "title": "پۈتۈن ئىنسانلار ۋە ھايۋانلارغا مۇئامىلە قىلىش پىرىنسىپى", "start": 1100, "end": 1104},
    {"slug": "06-elim-setim-ve-tijaret", "section": "05-muamile", "title": "ئېلىم-سېتىم پىرىنسىپلىرى، جازانە (ئۆسۈم) ۋە ھالال تىجارەت", "start": 1105, "end": 1125},
    {"slug": "07-muzaribet-shirketchiliki", "section": "05-muamile", "title": "مۇزارەبەت شېرىكچىلىكى، مەبلەغ سېلىش ۋە زىياننى تەقسىملەش", "start": 1126, "end": 1137},
    {"slug": "08-muddetke-bolup-setish-sughurta", "section": "05-muamile", "title": "بۆلۈپ سېتىش، تىجارىي ۋە ئىسلامىي ھەمكارلىق سۇغۇرتىسى", "start": 1138, "end": 1157},
    {"slug": "09-jihad-ve-ghaza", "section": "05-muamile", "title": "جىھادنىڭ ھەقىقىتى، پىرىنسىپلىرى ۋە غەنىيمەت ئەھكاملىرى", "start": 1158, "end": 1167},
    {"slug": "10-turmush-ve-nikah", "section": "05-muamile", "title": "ئائىلە قۇرۇش، تۇرمۇش ھەمراھى تاللاش، مۇھەببەت ۋە نومۇس", "start": 1168, "end": 1183},
    {"slug": "11-nikah-shertliri-ve-emildeshlik", "section": "05-muamile", "title": "نىكاھ شەرتلىرى، مەنئى قىلىنغانلار ۋە ئېمىلدەشلىك ئەھكاملىرى", "start": 1184, "end": 1199},
    {"slug": "12-mehri-nepiqe-ve-er-ayal", "section": "05-muamile", "title": "مەھرى، نەپىقە ۋە ئەر-خوتۇنلۇق مۇناسىۋەتنىڭ بۇزۇلۇش سەۋەبلىرى", "start": 1200, "end": 1212},
    {"slug": "13-talaq-ve-iddet", "section": "05-muamile", "title": "تالاق تۈرلىرى، ئۈچ تالاق، خۇلئى ۋە ئىددەت ئەھكاملىرى", "start": 1213, "end": 1246},
    {"slug": "14-vesiyet-ve-miras", "section": "05-muamile", "title": "ۋەسىيەت ۋە مىراس تەقسىماتىنىڭ تولۇق شەرئىي ئەھكاملىرى", "start": 1247, "end": 1272},
    {"slug": "15-veqip-ve-uyghur-veqpliri", "section": "05-muamile", "title": "ۋەقىپ ئەھكاملىرى ۋە ھەرەمەيندىكى ئۇيغۇر ۋەقپىلىرى", "start": 1273, "end": 1280},
    {"slug": "16-rene-hejir-guwahliq-qesem", "section": "05-muamile", "title": "رەنە، ھەجر، گۇۋاھلىق، قەسەم ۋە كاپارەت ئەھكاملىرى", "start": 1281, "end": 1317},
]

def get_division_info(q_num: int):
    for div in DIVISIONS:
        if div["start"] <= q_num <= div["end"]:
            return div["section"], div["slug"], div["title"]
    if q_num <= 967:
        return "03-exlaq", "misc", "ئەخلاق"
    elif q_num <= 1070:
        return "04-siyret", "misc", "پەيغەمبىرىمىز ھاياتىدىن ئۆرنەكلەر"
    else:
        return "05-muamile", "misc", "مۇئامىلە"

def parse_doc_questions(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for p_idx, page in enumerate(doc):
        raw_text = page.get_text("text")
        lines = []
        for l in raw_text.splitlines():
            line_str = l.strip()
            if not line_str:
                continue
            norm = normalize_text(reverse_visual_rtl_line(line_str))
            if norm:
                lines.append(norm)
        pages.append({
            "page_idx": p_idx,
            "lines": lines
        })
    return pages

def extract_questions_from_pages(pages, min_q, max_q, book_page_base):
    re_q1 = re.compile(r"^(?:\.|\b)(\d{3,4})(?:\.|\b)\s*:?\s*سوئال:?\s*(.*)$")
    re_q2 = re.compile(r"^:?\s*سوئال:?\s*(.*)\s+(?:\.|\b)(\d{3,4})(?:\.|\b)$")
    
    questions = []
    current_q = None
    current_lines = []
    
    for p in pages:
        p_idx = p["page_idx"]
        lines = p["lines"]
        idx = 0
        while idx < len(lines):
            line = lines[idx].strip()
            idx += 1
            
            # Skip running headers and standalone numbers
            if any(x in line for x in ['بۆلۈم-3', 'بۆلۈم-4', 'تۆتىنچى بۆلۈم', 'بەشىنچى بۆلۈم', 'ئائىلە ھاياتىدىكى بىر يۈرۈش ئەدەب', 'پەيغەمبەر ئەلەيھىسسالامنىڭ ۋاپاتى', 'قەسەم ۋە ئۇنىڭغا مۇناسىۋەتلىك', 'پايدىلىنىلغان ماتېرىياللار']):
                continue
            if re.match(r"^\d{1,3}$", line):
                continue
                
            q_num = None
            q_text = ""
            
            m1 = re_q1.match(line)
            if m1:
                q_num = int(m1.group(1))
                q_text = m1.group(2).strip()
            else:
                m2 = re_q2.match(line)
                if m2:
                    q_num = int(m2.group(2))
                    q_text = m2.group(1).strip()
                elif line == ".712" or line == "712.":
                    q_num = 712
                    q_text = "ئىنساننىڭ باشقىلار بىلەن بولغان مۇناسىۋىتىگە قارىتىلغان ئەخلاق قايسى؟"
                elif line == ".935" or line == "935.":
                    q_num = 935
                    q_text = "ئاللاھ ياقتۇرمايدىغان كىيىنىش قايسى؟"
                elif "1116" in line and "سوئال" in line:
                    q_num = 1116
                    q_text = "ئوغرىلانغان ۋە بولانغان نەرسىنى سېتىۋېلىش نېمە ئۈچۈن چەكلەنگەن؟"
                elif line.startswith("سوئال:") and idx < len(lines) and re.match(r"^\.?\d{3,4}\.?$", lines[idx].strip()):
                    q_num = int(re.sub(r"[^\d]", "", lines[idx].strip()))
                    q_text = line.replace("سوئال:", "").strip()
                    idx += 1
            
            if q_num is not None and min_q <= q_num <= max_q:
                if current_q:
                    current_q["answer"] = "\n".join(current_lines).strip()
                    questions.append(current_q)
                    current_lines = []
                    
                section, slug, topic_title = get_division_info(q_num)
                book_page = book_page_base + p_idx
                current_q = {
                    "number": q_num,
                    "question": q_text,
                    "answer": "",
                    "page": p_idx + 1,
                    "book_page": book_page,
                    "section": section,
                    "topic": slug,
                    "topic_title": topic_title,
                    "footnotes": []
                }
            elif current_q is not None:
                # Footnotes
                if re.match(r"^\(\d+\)\s*", line) or re.match(r"^\d+\(\s*\)\s*", line) or "رىۋايىتى" in line or "سۈرىسى" in line:
                    if len(line.split()) <= 10:
                        current_q["footnotes"].append(line)
                        continue
                current_lines.append(line)
                
    if current_q:
        current_q["answer"] = "\n".join(current_lines).strip()
        questions.append(current_q)
        
    return questions

def run():
    print("Extracting Part 2 (Q648 to Q821)...")
    p2_pages = parse_doc_questions(PART2_PDF)
    q_p2 = extract_questions_from_pages(p2_pages, 648, 821, book_page_base=296)
    print(f"Extracted {len(q_p2)} questions from Part 2.")
    
    print("Extracting Part 3 (Q822 to Q1317)...")
    p3_pages = parse_doc_questions(PART3_PDF)
    q_p3 = extract_questions_from_pages(p3_pages, 822, 1317, book_page_base=405)
    print(f"Extracted {len(q_p3)} questions from Part 3.")
    
    all_new = q_p2 + q_p3
    print(f"Total new questions: {len(all_new)}")
    
    # Check for missing
    nums = set(q["number"] for q in all_new)
    missing = set(range(648, 1318)) - nums
    if missing:
        print("MISSING QUESTIONS:", sorted(list(missing)))
    else:
        print("SUCCESS: All questions 648 to 1317 are present!")
        
    # Clean answer texts
    for q in all_new:
        ans = q["answer"]
        ans = re.sub(r"^:\s*جاۋاب:\s*", "", ans)
        ans = re.sub(r"^جاۋاب:\s*", "", ans)
        ans = re.sub(r"^:\s*جاۋاب\s*ــ\s*", "", ans)
        ans = re.sub(r"^جاۋاب\s*ــ\s*", "", ans)
        ans = re.sub(r"^جاۋاب\s*-\s*", "", ans)
        q["answer"] = ans.strip()

    # Load existing extracted_2000.json
    with open(EXTRACTED_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    existing_qs = data.get("questions", [])
    existing_1_647 = [q for q in existing_qs if q["number"] < 648]
    print(f"Existing questions 1..647 count: {len(existing_1_647)}")
    
    combined_qs = existing_1_647 + all_new
    combined_qs.sort(key=lambda x: x["number"])
    data["questions"] = combined_qs
    
    # Save back to EXTRACTED_JSON
    with open(EXTRACTED_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Saved {len(combined_qs)} total questions to {EXTRACTED_JSON}!")

if __name__ == "__main__":
    run()
