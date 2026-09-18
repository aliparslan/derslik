#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path

DOCS_DIR = Path("src/content/docs/aile")
files = sorted(DOCS_DIR.glob("**/*.mdx"))

def fix_line(line):
    # Protect Quranic verses and Hadith blockquotes
    if line.strip().startswith('>') or '﴿' in line:
        return line

    # -------------------------------------------------------------
    # 1. Inverted Lam-Alif Forms (ال vs لا)
    # -------------------------------------------------------------
    # ئەۋلاد forms
    line = re.sub(r'\bئەۋالدلار\b', 'ئەۋلادلار', line)
    line = re.sub(r'\bئەۋالدلىرىنىڭ\b', 'ئەۋلادلىرىنىڭ', line)
    line = re.sub(r'\bئەۋالدلىرىڭلارنىڭ\b', 'ئەۋلادلىرىڭلارنىڭ', line)
    line = re.sub(r'\bئەۋالدلىرى\b', 'ئەۋلادلىرى', line)
    line = re.sub(r'\bئەۋالدىدىن\b', 'ئەۋلادىدىن', line)
    line = re.sub(r'\bئەۋالدىنى\b', 'ئەۋلادىنى', line)
    line = re.sub(r'\bئەۋالدىنىڭ\b', 'ئەۋلادىنىڭ', line)
    line = re.sub(r'\bئەۋالدى\b', 'ئەۋلادى', line)
    line = re.sub(r'\bئەۋالد\b', 'ئەۋلاد', line)

    # ئىسلاھ / ئىسلاھات
    line = re.sub(r'\bئىسالھاتنى\b', 'ئىسلاھاتنى', line)
    line = re.sub(r'\bئىسالھاتچى\b', 'ئىسلاھاتچى', line)
    line = re.sub(r'\bئىسالھات\b', 'ئىسلاھات', line)
    line = re.sub(r'\bئىسالھ\b', 'ئىسلاھ', line)

    # ئىپلاس
    line = re.sub(r'\bئىپالسلار\b', 'ئىپلاسلار', line)
    line = re.sub(r'\bئىپالس\b', 'ئىپلاس', line)

    # تىلاۋەت
    line = re.sub(r'\bتىالۋىتى\b', 'تىلاۋىتى', line)
    line = re.sub(r'\bتىالۋەت\b', 'تىلاۋەت', line)

    # ئىلاھ / ئىلاھىي
    line = re.sub(r'\bئىالھلىرىمدىن\b', 'ئىلاھلىرىمدىن', line)
    line = re.sub(r'\bئىالھىى\b', 'ئىلاھىي', line)
    line = re.sub(r'\bئىالھىي\b', 'ئىلاھىي', line)
    line = re.sub(r'\bئىالھ\b', 'ئىلاھ', line)

    # لايىق / لاياقەت
    line = re.sub(r'\bاليىقىدا\b', 'لايىقىدا', line)
    line = re.sub(r'\bاليىق\b', 'لايىق', line)
    line = re.sub(r'\bالياقىتىگە\b', 'لاياقىتىگە', line)
    line = re.sub(r'\bالياقەتلىكتۇر\b', 'لاياقەتلىكتۇر', line)
    line = re.sub(r'\bالياقەتلىك\b', 'لاياقەتلىك', line)
    line = re.sub(r'\bالزىملىقىنى\b', 'لازىملىقىنى', line)
    line = re.sub(r'\bالزىم\b', 'لازىم', line)

    # باشلاڭ / باشلامچىسى
    line = re.sub(r'\bباشالڭلار\b', 'باشلاڭلار', line)
    line = re.sub(r'\bباشالڭ\b', 'باشلاڭ', line)
    line = re.sub(r'\bباشالمچىسى\b', 'باشلامچىسى', line)

    # ئۇخلاۋاتقان / تازىلايتتىم / تاشلايسىز / ئاڭلايتتى
    line = re.sub(r'\bئۇخالۋاتقاندا\b', 'ئۇخلاۋاتقاندا', line)
    line = re.sub(r'\bئۇخالۋاتقان\b', 'ئۇخلاۋاتقان', line)
    line = re.sub(r'\bتازىاليتتىم\b', 'تازىلايتتىم', line)
    line = re.sub(r'\bتاشاليسىز\b', 'تاشلايسىز', line)
    line = re.sub(r'\bئاڭاليتتى\b', 'ئاڭلايتتى', line)

    # پېئىل سۇففىكسلىرى: قارىلاتتى, قوللىنىلاتتى, يىغلاتقانلار, پايلاقچىلىق
    line = re.sub(r'\bقارىالتتى\b', 'قارىلاتتى', line)
    line = re.sub(r'\bقۋللىنىالتتى\b', 'قوللىنىلاتتى', line)
    line = re.sub(r'\bيىغالتقانلار\b', 'يىغلاتقانلار', line)
    line = re.sub(r'\bپايالقچىلىق\b', 'پايلاقچىلىق', line)

    # ئېھتىلام / ئىھتىلام
    line = re.sub(r'\bئېھتىالمدىن\b', 'ئېھتىلامدىن', line)
    line = re.sub(r'\bئېھتىالم\b', 'ئېھتىلام', line)
    line = re.sub(r'\bئىھتىالم\b', 'ئىھتىلام', line)

    # داموللام / بىسمىللاھ / ئەلەيھىسسالام
    line = re.sub(r'\bدامۋلالم\b', 'داموللام', line)
    line = re.sub(r'\bبىسمىلالھىر\b', 'بىسمىللاھىر', line)
    line = re.sub(r'\bبىسمىلالھ\b', 'بىسمىللاھ', line)
    line = re.sub(r'\bئەلەيھىسسالمنىڭ\b', 'ئەلەيھىسسالامنىڭ', line)
    line = re.sub(r'\bئەلەيھىسسالم\b', 'ئەلەيھىسسالام', line)
    line = re.sub(r'\bتۋپالملىرىدا\b', 'توپلاملىرىدا', line)
    line = re.sub(r'\bتۋپالم\b', 'توپلام', line)
    line = re.sub(r'\bسانىالمدۇ\b', 'سانالامدۇ', line)

    # باشقا تەتۈر قال / قلا شەكىللىرى
    line = re.sub(r'\bقاالقلىق\b', 'قالاقلىق', line)
    line = re.sub(r'\bقۋالقلىرىدىكى\b', 'قۇلاقلىرىدىكى', line)
    line = re.sub(r'\bقۋالق\b', 'قۇلاق', line)
    line = re.sub(r'\bتۋيالقتىن\b', 'تۇياقتىن', line)
    line = re.sub(r'\bخالقسىزلىقتىن\b', 'ئەخلاقسىزلىقتىن', line)
    line = re.sub(r'\bيۋقالغانلىقى\b', 'يوقالغانلىقى', line)
    line = re.sub(r'\bيۋقالغان\b', 'يوقالغان', line)
    line = re.sub(r'\bيۋقالڭلار\b', 'يوقلاڭلار', line)
    line = re.sub(r'\bيۋقاليدىكەن\b', 'يوقلايدىكەن', line)
    line = re.sub(r'\bئۋچۇقاليدۇكى\b', 'ئوچۇقلايدۇكى', line)
    line = re.sub(r'\bەخالقلىرى\b', 'ئەخلاقلىرى', line)
    line = re.sub(r'\bئۋنالين\b', 'ئونلاين', line)
    line = re.sub(r'\bسۋرۇنداشالغا\b', 'سورۇنداشلارغا', line)
    line = re.sub(r'\bئەلالمە\b', 'ئەللامە', line)
    line = re.sub(r'\bالمجمۋ\b', 'المجموع', line)

    # -------------------------------------------------------------
    # 2. Separated Case & Possessive Suffixes
    # -------------------------------------------------------------
    # Genitive -نىڭ: e.g. ئەر نىڭ -> ئەرنىڭ
    line = re.sub(r'([\u0621-\u06FF]+)[ \t]+نىڭ\b', r'\1نىڭ', line)

    # Accusative -نى: e.g. خوتۇن نى -> خوتۇننى, قىز نى -> قىزنى
    line = re.sub(r'([\u0621-\u06FF]+)[ \t]+نى\b', r'\1نى', line)

    # Isolated ڭ at end of word: e.g. ئۇنى ڭ -> ئۇنىڭ, قىلىشى ڭ -> قىلىشىڭ
    line = re.sub(r'([\u0621-\u06FF]+)[ \t]+ڭ\b', r'\1ڭ', line)

    # Isolated ئ at start of word: e.g. ئ الدانغان -> ئالدانغان
    line = re.sub(r'\bئ[ \t]+([\u0621-\u06FF]+)\b', r'ئ\1', line)

    # Plural possessive -لىرى...: e.g. قىز لىرىنىڭ -> قىزلىرىنىڭ
    line = re.sub(r'([\u0621-\u06FF]+)[ \t]+(لىرى[\u0621-\u06FF]*)\b', r'\1\2', line)

    # Suffix -لىق / -لىك
    line = re.sub(r'([\u0621-\u06FF]+)[ \t]+(لىق|لىك)\b', r'\1\2', line)

    # Suffix -سى / -سىنى / -سىغا / -سىدا / -سىدىن / -سىنىڭ
    line = re.sub(r'([\u0621-\u06FF]+)[ \t]+(سى|سىنى|سىغا|سىدا|سىدىن|سىنىڭ)\b', r'\1\2', line)

    # Copula suffix -دۇر
    line = re.sub(r'([\u0621-\u06FF]+)[ \t]+دۇر\b', r'\1دۇر', line)

    # Dative suffixes: غا, گە, قا, كە (except after ۋە / ۋ)
    def repl_dat(m):
        w1, w2 = m.group(1), m.group(2)
        if w1 in ['ۋە', 'ۋ']:
            return m.group(0)
        return w1 + w2
    line = re.sub(r'([\u0621-\u06FF]+)[ \t]+(غا|گە|قا|كە)\b', repl_dat, line)

    # Ablative suffixes: -دىن / -تىن (except after prepositions / pronouns)
    def repl_din(m):
        w1, w2 = m.group(1), m.group(2)
        if w1 in ['بۇ', 'شۇ', 'ئۇ', 'ھەر', 'بىر', 'ھەق', 'مەزكۇر', 'قايسى', 'ئۆز', 'ۋە', 'ۋ']:
            return m.group(0)
        return w1 + w2
    line = re.sub(r'([\u0621-\u06FF]+)[ \t]+(دىن|تىن)\b', repl_din, line)

    # -------------------------------------------------------------
    # 3. Suffixes starting with "ى"
    # -------------------------------------------------------------
    line = re.sub(r'\bتويئ[ \t]+ىشلىرىدا\b', 'توي ئىشلىرىدا', line)
    line = re.sub(r'\bيامانئ[ \t]+ىكەنلىكىنىڭ\b', 'يامان ئىكەنلىكىنىڭ', line)
    line = re.sub(r'\bئۇنىڭئ[ \t]+ىززىتىنى\b', 'ئۇنىڭ ئىززىتىنى', line)
    line = re.sub(r'\bنىڭئ[ \t]+ىزىنى\b', 'نىڭ ئىزىنى', line)
    line = re.sub(r'\bبىرق[ \t]+ىز\b', 'بىر قىز', line)
    line = re.sub(r'\bرۇخسەتق[ \t]+ىلغانلىقنىڭ\b', 'رۇخسەت قىلغانلىقنىڭ', line)
    line = re.sub(r'\bسەۋەبلەردىني[ \t]+ىراق\b', 'سەۋەبلەردىن يىراق', line)
    line = re.sub(r'\bئىشلارن[ \t]+ىكاھتىن\b', 'ئىشلار نىكاھتىن', line)
    line = re.sub(r'\bبۇخارى[ \t]+ىۋايىتى\b', 'بۇخارىي رىۋايىتى', line)
    line = re.sub(r'\bالز[ \t]+ىم\b', 'لازىم', line)
    line = re.sub(r'\bبۋينى[ \t]+نى\b', 'بويۇننى', line)

    # Specific compound verb splits: noun + ق + ى... -> noun + space + قى...
    line = re.sub(r'\bتەلەبق[ \t]+ىلىنىدۇ\b', 'تەلەپ قىلىنىدۇ', line)
    line = re.sub(r'\bتەكلىپق[ \t]+ىلسا\b', 'تەكلىپ قىلسا', line)
    line = re.sub(r'\bمەھرۇمق[ \t]+ىلىنغان\b', 'مەھرۇم قىلىنغان', line)
    line = re.sub(r'\bقەسەمق[ \t]+ىلسۇن\b', 'قەسەم قىلسۇن', line)
    line = re.sub(r'\bتاالقق[ \t]+ىلىپ\b', 'تالاق قىلىپ', line)
    line = re.sub(r'\bتاالقق[ \t]+ىلسا\b', 'تالاق قىلسا', line)
    line = re.sub(r'\bتاالقق[ \t]+ىلىنغان\b', 'تالاق قىلىنغان', line)
    line = re.sub(r'\bياراملىقق[ \t]+ىلىپ\b', 'ياراملىق قىلىپ', line)
    line = re.sub(r'\bقايتۇرىۋېلىش[ \t]+ىسلەرگە\b', 'قايتۇرىۋېلىشى سىلەرگە', line)
    line = re.sub(r'\bبىلەنب[ \t]+ىر\b', 'بىلەن بىر', line)
    line = re.sub(r'\bشەيخۇلئ[ \t]+ىسالم\b', 'شەيخۇلئىسلام', line)
    line = re.sub(r'\bئېمىلداشئ[ \t]+ىكەنلىكىنى\b', 'ئېمىلداش ئىكەنلىكىنى', line)

    # Specific words broken before ى
    line = re.sub(r'\bۋاقىتق[ \t]+ىچىلىك\b', 'ۋاقىتقىچىلىك', line)
    line = re.sub(r'\bپاكلانغ[ \t]+ىچىلىك\b', 'پاكلانغىچىلىك', line)
    line = re.sub(r'\bقاندۇرالمايدۇ[ \t]+ىغان\b', 'قاندۇرالمايدىغان', line)
    line = re.sub(r'\bيېمەكئ[ \t]+ىچمەك\b', 'يېمەك - ئىچمەك', line)
    line = re.sub(r'\bدېگەنئ[ \t]+ىبارىنى\b', 'دېگەن ئىبارىنى', line)
    line = re.sub(r'\bگۇناھئ[ \t]+ىش\b', 'گۇناھ ئىش', line)
    line = re.sub(r'\bسىلەرئ[ \t]+ىسيانكارلىق\b', 'سىلەر ئىسيانكارلىق', line)
    line = re.sub(r'\bئورۇند[ \t]+ىيالمايدۇ\b', 'ئورۇندىيالمايدۇ', line)
    line = re.sub(r'\bئورۇند[ \t]+ىيالايدۇ\b', 'ئورۇندىيالايدۇ', line)
    line = re.sub(r'\bئائ[ \t]+ىلىدە\b', 'ئائىلىدە', line)
    line = re.sub(r'\bتەربىي[ \t]+ىلىشىگە\b', 'تەربىيىلىنىشىگە', line)
    line = re.sub(r'\bئۇنىڭد[ \t]+ىنمۇ\b', 'ئۇنىڭدىنمۇ', line)
    line = re.sub(r'\bكۆرىل[ \t]+ىدىغانلىقىنى\b', 'كۆرۈلىدىغانلىقىنى', line)
    line = re.sub(r'\bكۈنلىر[ \t]+ىدىكى\b', 'كۈنلىرىدىكى', line)
    line = re.sub(r'\bھەبەش[ \t]+ىستان\b', 'ھەبەشىستان', line)
    line = re.sub(r'\bئەدەپ[ \t]+ىيات\b', 'ئەدەبىيات', line)
    line = re.sub(r'\bتەرك[ \t]+ىيدۇنيالىق\b', 'تەركىيدۇنيالىق', line)
    line = re.sub(r'\bئات[ \t]+ىلارنىڭ\b', 'ئانىلىرىنىڭ', line)
    line = re.sub(r'\bئائىل[ \t]+ىلەردىكى\b', 'ئائىلىلەردىكى', line)
    line = re.sub(r'\bئائىل[ \t]+ىۋىي\b', 'ئائىلىۋىي', line)
    line = re.sub(r'\bئۈستىد[ \t]+ىكى\b', 'ئۈستىدىكى', line)
    line = re.sub(r'\bيېق[ \t]+ىنقى\b', 'يېقىنقى', line)
    line = re.sub(r'\bمۇناس[ \t]+ىۋەتكە\b', 'مۇناسىۋەتكە', line)
    line = re.sub(r'\bچىقىد[ \t]+ىغان\b', 'چىقىدىغان', line)
    line = re.sub(r'\bئىدد[ \t]+ىتى\b', 'ئىددىتى', line)
    line = re.sub(r'\bئىكك[ \t]+ىنچى\b', 'ئىككىنچى', line)
    line = re.sub(r'\bئۋخش[ \t]+ىغان\b', 'ئوخشىغان', line)
    line = re.sub(r'\bتەر[ \t]+ىكىگە\b', 'تەركىگە', line)
    line = re.sub(r'\bئۆلگەنل[ \t]+ىكىگە\b', 'ئۆلگەنلىكىگە', line)
    line = re.sub(r'\bيۇ[ \t]+ق[ \t]*ىرىقىلاردىن\b', 'يۇقىرىقىلاردىن', line)

    # General reconnection for any word + space + bare ى...
    def repl_general_y(m):
        w1, w2 = m.group(1), m.group(2)
        if w2 in ['ىف', 'في'] or w1 in ['ۋە', 'ۋ']:
            return m.group(0)
        return w1 + w2

    line = re.sub(r'\b([\u0621-\u06FF]+)[ \t]+(ى[^\s\d_#\*\>«»\(\)\[\]\{\}]+)\b', repl_general_y, line)

    # -------------------------------------------------------------
    # 4. Intra-word letter-spacing cleanups
    # -------------------------------------------------------------
    line = re.sub(r'\bئاللا[ \t]+ھ\b', 'ئاللاھ', line)
    line = re.sub(r'\bرە[ \t]+سۇ[ \t]+لۇ[ \t]*لالھ\b', 'رەسۇلۇللاھ', line)
    line = re.sub(r'\bيا[ \t]+رەسۇلۇللاھ\b', 'يا رەسۇلۇللاھ', line)
    line = re.sub(r'\bسەھى[ \t]+ھ\b', 'سەھىھ', line)
    line = re.sub(r'\bسا[ \t]+ۋ[ \t]+اب\b', 'ساۋاب', line)
    line = re.sub(r'\bسە[ \t]+دىقىد[ \t]+ۇر\b', 'سەدىقىدۇر', line)
    line = re.sub(r'\bئۈ[ \t]*لگىد[ \t]*ۇر\b', 'ئۈلگىدۇر', line)
    line = re.sub(r'\bئۆ[ \t]+يل[ \t]*ە[ \t]*نگۈ[ \t]*چىل[ \t]*ە[ \t]*رنى[ \t]*ڭ\b', 'ئۆيلەنگۈچىلەرنىڭ', line)
    line = re.sub(r'\bشې[ \t]+ھىتل[ \t]*ە[ \t]*رنى[ \t]*ڭ\b', 'شېھىتلەرنىڭ', line)
    line = re.sub(r'\bئۈ[ \t]*ممە[ \t]*تل[ \t]*ە[ \t]*رنى[ \t]*ڭ\b', 'ئۈممەتلەرنىڭ', line)
    line = re.sub(r'\bسۈ[ \t]*پە[ \t]*تل[ \t]*ە[ \t]*رنى[ \t]*ڭ\b', 'سۈپەتلەرنىڭ', line)
    line = re.sub(r'\bھ[ \t]*ە[ \t]*ۋە[ \t]*سل[ \t]*ە[ \t]*رنى\b', 'ھەۋەسلەرنى', line)
    line = re.sub(r'\bتە[ \t]*جىرىبىل[ \t]*ە[ \t]*رمۇ\b', 'تەجرىبىلەرمۇ', line)
    line = re.sub(r'\bيۋرۇ[ \t]*قلىرى[ \t]*ڭ[ \t]*ال[ \t]*رمۇ\b', 'يورۇقلىرىڭلارمۇ', line)
    line = re.sub(r'\bنې[ \t]*مە[ \t]*تل[ \t]*ە[ \t]*رگە\b', 'نېمەتلەرگە', line)
    line = re.sub(r'\bنەقەدە[ \t]*رغ[ \t]*ۇرۇ[ \t]*رل[ \t]*ۇق\b', 'نەقەدەر غۇرۇرلۇق', line)
    line = re.sub(r'\bئا[ \t]+يىقىغىچە\b', 'ئايىغىغىچە', line)
    line = re.sub(r'\bپارچىال[ \t]+پ\b', 'پارچىلاپ', line)
    line = re.sub(r'\bئې[ \t]+زىپ\b', 'ئېزىپ', line)
    line = re.sub(r'\bبول[ \t]+ۇ[ \t]+شى\b', 'بولۇشى', line)
    line = re.sub(r'\bبول[ \t]+ۇ[ \t]+شقا\b', 'بولۇشقا', line)
    line = re.sub(r'\bبۋلمى[ \t]+سا\b', 'بولمىسا', line)
    line = re.sub(r'\bچىرىكل[ \t]*ە[ \t]*شك[ \t]*ەن\b', 'چىرىكلەشكەن', line)
    line = re.sub(r'\bكې[ \t]+لە[ \t]+چە[ \t]+ك\b', 'كېلەچەك', line)
    line = re.sub(r'\bكې[ \t]+چە[ \t]+ك\b', 'كېچەك', line)
    line = re.sub(r'\bتەن[ \t]+سا[ \t]*ق[ \t]*لىقىغا\b', 'تەن ساقلىقىغا', line)
    line = re.sub(r'\bچەك[ \t]*-[ \t]*چ[ \t]+ېگراسى\b', 'چەك - چېگراسى', line)
    line = re.sub(r'\bئۆ[ \t]*زل[ \t]*ۈ[ \t]*كىدىن\b', 'ئۆزلۈكىدىن', line)
    line = re.sub(r'\bتە[ \t]*ربىيە\b', 'تەربىيە', line)
    line = re.sub(r'\bپەيغەمبەر[ \t]+ئەلەيھىسسالا[ \t]+م\b', 'پەيغەمبەر ئەلەيھىسسالام', line)
    line = re.sub(r'\bئايا[ \t]+ل\b', 'ئايال', line)
    line = re.sub(r'\bكە[ \t]+لمە[ \t]+كتە\b', 'كەلمەكتە', line)
    line = re.sub(r'\bئۆ[ \t]+تمۈ[ \t]+شتە\b', 'ئۆتمۈشتە', line)
    line = re.sub(r'\bئۈ[ \t]+ممىتىمدىن\b', 'ئۈممىتىدىن', line)
    line = re.sub(r'\bماۋز[ \t]+ۇدىكى\b', 'ماۋزۇدىكى', line)

    return line

total_changed = 0
for f in files:
    content = f.read_text(encoding='utf-8')
    lines = content.splitlines()
    new_lines = []
    file_changed = False

    for l in lines:
        fixed = fix_line(l)
        if fixed != l:
            total_changed += 1
            file_changed = True
        new_lines.append(fixed)

    if file_changed:
        f.write_text("\n".join(new_lines) + "\n", encoding='utf-8')
        print(f"Updated {f.name}")

print(f"\nDone! Updated {total_changed} lines across files.")
