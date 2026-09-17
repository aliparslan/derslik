#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/extract_aile.py

Comprehensive extraction and processing script for:
«ئىسلامدىكى ئائىلە تۈزۈمى» (نظام الأسرة في الإسلام)
Author: مۇھەممەد يۈسۈپ (Muhemmed Yusup)

1. Extracts 505 pages from public/aile/islamdiki-aile-tuzumi.pdf.
2. Performs font-aware glyph decoding for UKIJ Tuz Basma, Traditional Arabic, etc.
3. Decodes visual RTL glyph sequences to standard logical modern Uyghur (UEY).
4. Cleans tatweels, broken ligatures, and applies Uyghur orthographic normalization.
5. Groups content into structured MDX pages under src/content/docs/aile/.
6. Generates index.mdx with comprehensive Table of Contents and download links.
"""

import os
import sys
import re
import io
from pathlib import Path
from collections import defaultdict
import fitz
from fontTools.ttLib import TTFont

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = PROJECT_ROOT / "public" / "aile" / "islamdiki-aile-tuzumi.pdf"
DOCS_DIR = PROJECT_ROOT / "src" / "content" / "docs" / "aile"

# Glyph name to modern Uyghur Arabic script (UEY) mapping
GLYPH_TO_UEY = {
    # Alif
    'uni0627': 'ا', 'uniFE8D': 'ا', 'uniFE8E': 'ا',
    # Beh
    'uni0628': 'ب', 'uniFE8F': 'ب', 'uniFE90': 'ب', 'uniFE91': 'ب', 'uniFE92': 'ب',
    # Peh
    'uni067E': 'پ', 'uniFB56': 'پ', 'uniFB57': 'پ', 'uniFB58': 'پ', 'uniFB59': 'پ',
    # Teh
    'uni062A': 'ت', 'uniFE95': 'ت', 'uniFE96': 'ت', 'uniFE97': 'ت', 'uniFE98': 'ت',
    # Jim
    'uni062C': 'ج', 'uniFE9D': 'ج', 'uniFE9E': 'ج', 'uniFE9F': 'ج', 'uniFEA0': 'ج',
    # Chim
    'uni0686': 'چ', 'uniFB7A': 'چ', 'uniFB7B': 'چ', 'uniFB7C': 'چ', 'uniFB7D': 'چ',
    # Xeh
    'uni062E': 'خ', 'uniFEA5': 'خ', 'uniFEA6': 'خ', 'uniFEA7': 'خ', 'uniFEA8': 'خ',
    # Dal
    'uni062F': 'د', 'uniFEA9': 'د', 'uniFEAA': 'د',
    # Reh
    'uni0631': 'ر', 'uniFEAD': 'ر', 'uniFEAE': 'ر',
    # Zeyn
    'uni0632': 'ز', 'uniFEAF': 'ز', 'uniFEB0': 'ز',
    # Zhey
    'uni0698': 'ژ', 'uniFB8A': 'ژ', 'uniFB8B': 'ژ',
    # Sin
    'uni0633': 'س', 'uniFEB1': 'س', 'uniFEB2': 'س', 'uniFEB3': 'س', 'uniFEB4': 'س',
    # Shin
    'uni0634': 'ش', 'uniFEB5': 'ش', 'uniFEB6': 'ش', 'uniFEB7': 'ش', 'uniFEB8': 'ش',
    # Ghayn
    'uni063A': 'غ', 'uniFECD': 'غ', 'uniFECE': 'غ', 'uniFECF': 'غ', 'uniFED0': 'غ',
    # Feh
    'uni0641': 'ف', 'uniFED1': 'ف', 'uniFED2': 'ف', 'uniFED3': 'ف', 'uniFED4': 'ف',
    # Qaf
    'uni0642': 'ق', 'uniFED5': 'ق', 'uniFED6': 'ق', 'uniFED7': 'ق', 'uniFED8': 'ق',
    # Kaf
    'uni0643': 'ك', 'uniFED9': 'ك', 'uniFEDA': 'ك', 'uniFEDB': 'ك', 'uniFEDC': 'ك',
    # Gaf
    'uni06AF': 'گ', 'uniFB92': 'گ', 'uniFB93': 'گ', 'uniFB94': 'گ', 'uniFB95': 'گ',
    # Nga (Ngeh)
    'uni06AD': 'ڭ', 'uniFBD3': 'ڭ', 'uniFBD4': 'ڭ', 'uniFBD5': 'ڭ', 'uniFBD6': 'ڭ',
    # Lam
    'uni0644': 'ل', 'uniFEDD': 'ل', 'uniFEDE': 'ل', 'uniFEDF': 'ل', 'uniFEE0': 'ل',
    # Mim
    'uni0645': 'م', 'uniFEE1': 'م', 'uniFEE2': 'م', 'uniFEE3': 'م', 'uniFEE4': 'م',
    # Nun
    'uni0646': 'ن', 'uniFEE5': 'ن', 'uniFEE6': 'ن', 'uniFEE7': 'ن', 'uniFEE8': 'ن',
    # Heh (Uyghur heh)
    'uni06BE': 'ھ', 'uniFBAB': 'ھ',
    # Ae (Uyghur e)
    'uni06D5': 'ە', 'uni0647': 'ە', 'uniFEE9': 'ە', 'uniFEEA': 'ە',
    # O (Uyghur o / ۆ)
    'uni06C6': 'ۆ', 'uniFBDB': 'ۆ', 'uniFBDA': 'ۆ',
    # U (Uyghur u / ۇ)
    'uni06C7': 'ۇ', 'uniFBD7': 'ۇ', 'uniFBD8': 'ۇ',
    # Oe/Yu (Uyghur ü / ۈ)
    'uni06C8': 'ۈ', 'uniFBDD': 'ۈ', 'uniFBDC': 'ۈ',
    # We (Uyghur w / ۋ)
    'uni06CB': 'ۋ', 'uni0648': 'ۋ', 'uniFEED': 'ۋ', 'uniFEEE': 'ۋ', 'uniFBDE': 'ۋ', 'uniFBDF': 'ۋ',
    # E (Uyghur e / ې)
    'uni06D0': 'ې', 'uniFBE4': 'ې', 'uniFBE5': 'ې', 'uniFBE6': 'ې', 'uniFBE7': 'ې',
    # I (Uyghur i / ى)
    'uniFBE8': 'ى', 'uniFBE9': 'ى', 'uni0649': 'ى', 'uniFEEF': 'ى', 'uniFEF0': 'ى',
    # Y (Uyghur y / ي)
    'uni064A': 'ي', 'uniFEF1': 'ي', 'uniFEF2': 'ي', 'uniFBFE': 'ي', 'uniFBFF': 'ي',
    # Hamza on Yeh (Uyghur initial vowel sign / ئ)
    'uni0626': 'ئ', 'uniFE89': 'ئ', 'uniFE8A': 'ئ', 'uniFE8B': 'ئ', 'uniFE8C': 'ئ',
    # Lam-Alif (Reversed in visual glyph map so txt[::-1] produces correct logical Modern Uyghur 'لا')
    'uniFEFB': 'ال', 'uniFEFC': 'ال', 'uniFEF5': 'آل', 'uniFEF6': 'آل', 'uniFEF7': 'أل', 'uniFEF8': 'أل', 'uniFEF9': 'إل', 'uniFEFA': 'إل',
    # Allah
    'uniFDF2': 'ھالالئ',
    # Arabic / Quranic specific
    'uni0621': 'ء', 'uni0622': 'آ', 'uni0623': 'أ', 'uni0624': 'ؤ', 'uni0625': 'إ', 'uni0629': 'ة',
    'uni064B': 'ً', 'uni064C': 'ٌ', 'uni064D': 'ٍ', 'uni064E': 'َ', 'uni064F': 'ُ',
    'uni0650': 'ِ', 'uni0651': 'ّ', 'uni0652': 'ْ', 'uni0670': 'ٰ',
    'uniFD3E': '﴾', 'uniFD3F': '﴿',
    # Ligatures in traditional Arabic
    'uniFC60': 'صلعم', 'uniFC62': 'قلى', 'uniFC32': 'فى', 'uniFCAA': 'صلعم',
    # Tatweel
    'uni0640': '',
    # Punctuation
    'uni060C': '،', 'uni061F': '؟', 'uni061B': '؛',
    'space': ' ', 'period': '.', 'comma': '،', 'colon': ':', 'hyphen': '-', 'endash': '–', 'emdash': '—',
    'parenleft': '(', 'parenright': ')', 'bracketleft': '[', 'bracketright': ']',
    'guillemotleft': '«', 'guillemotright': '»', 'quotedblleft': '“', 'quotedblright': '”',
    'exclam': '!', 'question': '؟', 'slash': '/', 'backslash': '/',
    'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
    'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
}

# Standard Uyghur orthography fixes
WORD_REPLACEMENTS = [
    (r'\bئالالھ\b', 'ئاللاھ'),
    (r'\bئالالھنىڭ\b', 'ئاللاھنىڭ'),
    (r'\bئالالھقا\b', 'ئاللاھقا'),
    (r'\bئالالھتا\b', 'ئاللاھتا'),
    (r'\bئالالھتىن\b', 'ئاللاھتىن'),
    (r'\bتائاال\b', 'تائالا'),
    (r'\bتائاالنىڭ\b', 'تائالانىڭ'),
    (r'\bتائاالغا\b', 'تائالاغا'),
    (r'\bتائاالدا\b', 'تائالادا'),
    (r'\bتائاالدىن\b', 'تائالادىن'),
    (r'\bئايالالر\b', 'ئاياللار'),
    (r'\bئايالالرنى\b', 'ئاياللارنى'),
    (r'\bئايالالرنىڭ\b', 'ئاياللارنىڭ'),
    (r'\bئايالالرغا\b', 'ئاياللارغا'),
    (r'\bئايالالردا\b', 'ئاياللاردا'),
    (r'\bئايالالردىن\b', 'ئاياللاردىن'),
    (r'\bئىنسانالر\b', 'ئىنسانلار'),
    (r'\bئىنسانالرنى\b', 'ئىنسانلارنى'),
    (r'\bئىنسانالرنىڭ\b', 'ئىنسانلارنىڭ'),
    (r'\bئىنسانالرغا\b', 'ئىنسانلارغا'),
    (r'\bئىنسانالردا\b', 'ئىنسانلاردا'),
    (r'\bئىنسانالردىن\b', 'ئىنسانلاردىن'),
    (r'\bقىزالر\b', 'قىزلار'),
    (r'\bقىزالرنى\b', 'قىزلارنى'),
    (r'\bقىزالرنىڭ\b', 'قىزلارنىڭ'),
    (r'\bقىزالرغا\b', 'قىزلارغا'),
    (r'\bقىزالردا\b', 'قىزلاردا'),
    (r'\bقىزالردىن\b', 'قىزلاردىن'),
    (r'\bئۇالر\b', 'ئۇلار'),
    (r'\bئۇالرنى\b', 'ئۇلارنى'),
    (r'\bئۇالرنىڭ\b', 'ئۇلارنىڭ'),
    (r'\bئۇالرغا\b', 'ئۇلارغا'),
    (r'\bئۇالردا\b', 'ئۇلاردا'),
    (r'\bئۇالردىن\b', 'ئۇلاردىن'),
    (r'\bساالم\b', 'سالام'),
    (r'\bساالمغا\b', 'سالامغا'),
    (r'\bساالمنى\b', 'سالامنى'),
    (r'\bساالمى\b', 'سالامى'),
    (r'\bماختاشالر\b', 'ماختاشلار'),
    (r'\bماختاشالرنى\b', 'ماختاشلارنى'),
    (r'\bزااللەت\b', 'زالالەت'),
    (r'\bبۋل\b', 'بول'),
    (r'\bبۋلدى\b', 'بولدى'),
    (r'\bبۋلىدۇ\b', 'بولىدۇ'),
    (r'\bبۋلسا\b', 'بولسا'),
    (r'\bبۋلغان\b', 'بولغان'),
    (r'\bبۋلۇپ\b', 'بولۇپ'),
    (r'\bبۋلغاچقا\b', 'بولغاچقا'),
    (r'\bبۋلمايدۇ\b', 'بولمايدۇ'),
    (r'\bبۋلمىسا\b', 'بولمىسا'),
    (r'\bبۋلسۇن\b', 'بولسۇن'),
    (r'\bبۋلمىسۇن\b', 'بولمىسۇن'),
    (r'\bبۋلسىمۇ\b', 'بولسىمۇ'),
    (r'\bبۋالمدۇ\b', 'بولامدۇ'),
    (r'\bيۋل\b', 'يول'),
    (r'\bيۋلى\b', 'يولى'),
    (r'\bيۋلدا\b', 'يولدا'),
    (r'\bيۋلغا\b', 'يولغا'),
    (r'\bيۋللار\b', 'يوللار'),
    (r'\bيۋللارنى\b', 'يوللارنى'),
    (r'\bيۋللارنىڭ\b', 'يوللارنىڭ'),
    (r'\bيۋلۇڭدا\b', 'يولۇڭدا'),
    (r'\bيۋلىنى\b', 'يولىنى'),
    (r'\bيۋقىرى\b', 'يۇقىرى'),
    (r'\bيۋقىرىقى\b', 'يۇقىرىقى'),
    (r'\bيۋق\b', 'يوق'),
    (r'\bيۋقال\b', 'يوقال'),
    (r'\bسۋرايدۇ\b', 'سورايدۇ'),
    (r'\bسۋراپ\b', 'سوراپ'),
    (r'\bسۋرىسا\b', 'سورىسا'),
    (r'\bسۋراچ\b', 'سوراش'),
    (r'\bسۋرا\b', 'سورا'),
    (r'\bسۋئال\b', 'سوئال'),
    (r'\bسۋئاللار\b', 'سوئاللار'),
    (r'\bئۋقۇ\b', 'ئوقۇ'),
    (r'\bئۋقۇش\b', 'ئوقۇش'),
    (r'\bئۋقۇدى\b', 'ئوقۇدى'),
    (r'\bئۋقۇغان\b', 'ئوقۇغان'),
    (r'\bئۋقۇدۇم\b', 'ئوقۇدۇم'),
    (r'\bئۋقۇدۇڭ\b', 'ئوقۇدۇڭ'),
    (r'\bئۋقۇسا\b', 'ئوقۇسا'),
    (r'\bئۋقۇپ\b', 'ئوقۇپ'),
    (r'\bئۋقۇمايدۇ\b', 'ئوقۇمايدۇ'),
    (r'\bئۋقۇمايدىغان\b', 'ئوقۇمايدىغان'),
    (r'\bئۋقۇيدىغان\b', 'ئوقۇيدىغان'),
    (r'\bتۋغرا\b', 'توغرا'),
    (r'\bتۋغرۇلۇق\b', 'توغرۇلۇق'),
    (r'\bتۋغرىسىدا\b', 'توغرىسىدا'),
    (r'\bتۋنۇ\b', 'تونۇ'),
    (r'\bتۋنۇپ\b', 'تونۇپ'),
    (r'\bتۋنۇيدۇ\b', 'تونۇيدۇ'),
    (r'\bتۋنۇتىدۇ\b', 'تونۇتىدۇ'),
    (r'\bتۋنۇش\b', 'تونۇش'),
    (r'\bتۋنۇشىغا\b', 'تونۇشىغا'),
    (r'\bخۋتۇن\b', 'خوتۇن'),
    (r'\bخۋتۇنلۇق\b', 'خوتۇنلۇق'),
    (r'\bخۋتۇنچىلىق\b', 'خوتۇنچىلىق'),
    (r'\bخۋتۇننىڭ\b', 'خوتۇننىڭ'),
    (r'\bخۋتۇنى\b', 'خوتۇنى'),
    (r'\bخۋتۇنلار\b', 'خوتۇنلار'),
    (r'\bخۋشاللىق\b', 'خۇشاللىق'),
    (r'\bخۋشال\b', 'خۇشال'),
    (r'\bھۋقۇق\b', 'ھوقۇق'),
    (r'\bھۋقۇقى\b', 'ھوقۇقى'),
    (r'\bھۋقۇقلار\b', 'ھوقۇقلار'),
    (r'\bھۋقۇقلىرى\b', 'ھوقۇقلىرى'),
    (r'\bھۋقۇقلىرىنى\b', 'ھوقۇقلىرىنى'),
    (r'\bھۋقۇقىغا\b', 'ھوقۇقىغا'),
    (r'\bئۋتتۇرا\b', 'ئوتتۇرا'),
    (r'\bئۋتتۇرىسىدا\b', 'ئوتتۇرىسىدا'),
    (r'\bئۋرۇن\b', 'ئورۇن'),
    (r'\bئۋرنىدا\b', 'ئورنىدا'),
    (r'\bئۋرۇنلار\b', 'ئورۇنلار'),
    (r'\bتۋي\b', 'توي'),
    (r'\bتۋيدا\b', 'تويدا'),
    (r'\bتۋينى\b', 'توينى'),
    (r'\bتۋينىڭ\b', 'توينىڭ'),
    (r'\bتۋيلار\b', 'تويلار'),
    (r'\bنۋرمال\b', 'نورمال'),
    (r'\bنۋرمالسىز\b', 'نورمالسىز'),
    (r'\bنۋرمالسىزلىقى\b', 'نورمالسىزلىقى'),
    (r'\bقۋل\b', 'قول'),
    (r'\bقۋلى\b', 'قولى'),
    (r'\bقۋلدا\b', 'قولدا'),
    (r'\bقۋلغا\b', 'قولغا'),
    (r'\bقۋلىغا\b', 'قولىغا'),
    (r'\bقۋللار\b', 'قوللار'),
    (r'\bقۋللىنىش\b', 'قوللىنىش'),
    (r'\bقۋبۇل\b', 'قوبۇل'),
    (r'\bدۋزاخ\b', 'دوزاخ'),
    (r'\bچۋڭ\b', 'چوڭ'),
    (r'\bچۋڭلار\b', 'چوڭلار'),
    (r'\bدېن\b', 'دىن'),
    (r'\bدېنى\b', 'دىنى'),
    (r'\bدېنىدا\b', 'دىنىدا'),
    (r'\bدېنىمىز\b', 'دىنىمىز'),
    (r'\bدېنىمىزنىڭ\b', 'دىنىمىزنىڭ'),
    (r'\bدېندۇر\b', 'دىندۇر'),
    (r'\bدېنىغا\b', 'دىنىغا'),
    (r'\bدېننى\b', 'دىننى'),
    (r'\bدېننىڭ\b', 'دىننىڭ'),
    (r'\bئېنسان\b', 'ئىنسان'),
    (r'\bئېنسانلار\b', 'ئىنسانلار'),
    (r'\bئېنسانىيەت\b', 'ئىنسانىيەت'),
    (r'\bئېنساننىڭ\b', 'ئىنساننىڭ'),
    (r'\bئېنسانى\b', 'ئىنسانىي'),
    (r'\bئېنسانىي\b', 'ئىنسانىي'),
    (r'\bئېسالم\b', 'ئىسلام'),
    (r'\bئېسالمدا\b', 'ئىسلامدا'),
    (r'\bئېسالمىي\b', 'ئىسلامىي'),
    (r'\bئېسالمنىڭ\b', 'ئىسلامنىڭ'),
    (r'\bئېسالمغا\b', 'ئىسلامغا'),
    (r'\bئېمان\b', 'ئىمان'),
    (r'\bئېمانى\b', 'ئىمانى'),
    (r'\bئېماننىڭ\b', 'ئىماننىڭ'),
    (r'\bئېمانغا\b', 'ئىمانغا'),
    (r'\bھېدايەت\b', 'ھىدايەت'),
    (r'\bھەقېقەت\b', 'ھەقىقەت'),
    (r'\bھەقېقىي\b', 'ھەقىقىي'),
    (r'\bھەقېقەتەن\b', 'ھەقىقەتەن'),
    (r'\bھەقېقەتنىڭ\b', 'ھەقىقەتنىڭ'),
    (r'\bپەزېلەت\b', 'پەزىلەت'),
    (r'\bپەزېلەتلىك\b', 'پەزىلەتلىك'),
    (r'\bپەزېلىتى\b', 'پەزىلىتى'),
    (r'\bئالېي\b', 'ئالىي'),
    (r'\bئېلم\b', 'ئىلىم'),
    (r'\bئېلمى\b', 'ئىلمى'),
    (r'\bئېلمىي\b', 'ئىلمىي'),
    (r'\bئېلمىنىڭ\b', 'ئىلىمنىڭ'),
    (r'\bئېلمىگە\b', 'ئىلىمگە'),
    (r'\bئېش\b', 'ئىش'),
    (r'\bئېشى\b', 'ئىشى'),
    (r'\bئېشنى\b', 'ئىشنى'),
    (r'\bئېشلار\b', 'ئىشلار'),
    (r'\bئېشلارنى\b', 'ئىشلارنى'),
    (r'\bئېشلارغا\b', 'ئىشلارغا'),
    (r'\bئېشلاردا\b', 'ئىشلاردا'),
    (r'\bئېشلاردىن\b', 'ئىشلاردىن'),
    (r'\bئېچ\b', 'ئىچ'),
    (r'\bئېچى\b', 'ئىشى'),
    (r'\bئېچىدە\b', 'ئىچىدە'),
    (r'\bئېچىگە\b', 'ئىچىگە'),
    (r'\bئېچىدىن\b', 'ئىچىدىن'),
    (r'\bئېپتېدائى\b', 'ئىپتىدائىي'),
    (r'\bئېپتېدائىي\b', 'ئىپتىدائىي'),
    (r'\bئېجتېمائىي\b', 'ئىجتىمائىي'),
    (r'\bئېجتېمائېي\b', 'ئىجتىمائىي'),
    (r'\bئېسالھ\b', 'ئىسلاھ'),
    (r'\bئېللەتلەر\b', 'ئىللەتلەر'),
    (r'\bئېلغار\b', 'ئىلغار'),
    (r'\bتەشكېل\b', 'تەشكىل'),
    (r'\bتەركېبېنى\b', 'تەركىبىنى'),
    (r'\bتەركېبى\b', 'تەركىبى'),
    (r'\bمۇئمىن\b', 'مۆمىن'),
    (r'\bمۇئمىنلەر\b', 'مۆمىنلەر'),
    (r'\bمۇئمىنلەرگە\b', 'مۆمىنلەرگە'),
    (r'\bمۇئمىنلەرنىڭ\b', 'مۆمىنلەرنىڭ'),
    (r'\bمۇئمىنلەرنى\b', 'مۆمىنلەرنى'),
    (r'\bقېلېپ\b', 'قىلىپ'),
    (r'\bقېلىش\b', 'قىلىش'),
    (r'\bقېلىشى\b', 'قىلىشى'),
    (r'\bقېلىپ\b', 'قىلىپ'),
    (r'\bقېلىندى\b', 'قىلىندى'),
    (r'\bقېلىنىدۇ\b', 'قىلىنىدۇ'),
    (r'\bقېلىنغان\b', 'قىلىنغان'),
    (r'\bقېلغان\b', 'قىلغان'),
    (r'\bقېلېدۇ\b', 'قىلىدۇ'),
    (r'\bقېلىدۇ\b', 'قىلىدۇ'),
    (r'\bقېل\b', 'قىل'),
    (r'\bيارېتېپ\b', 'يارىتىپ'),
    (r'\bيارېتىپ\b', 'يارىتىپ'),
    (r'\bيارېتىلغان\b', 'يارىتىلغان'),
    (r'\bيارىتىلىشى\b', 'يارىتىلىشى'),
    (r'\bچېقېشى\b', 'چىقىشى'),
    (r'\bچېقىپ\b', 'چىقىپ'),
    (r'\bچېقىدۇ\b', 'چىقىدۇ'),
    (r'\bچېقىش\b', 'چىقىش'),
    (r'\bكېلېدۇ\b', 'كېلىدۇ'),
    (r'\bتەۋسىيە\b', 'تەۋسىيە'),
    (r'\bپەيغەمبېرېمېز\b', 'پەيغەمبىرىمىز'),
    (r'\bھەزرېتى\b', 'ھەزرىتى'),
    (r'\bئەلەيھېسساالمغا\b', 'ئەلەيھىسسالامغا'),
    (r'\bئەلەيھېسساالم\b', 'ئەلەيھىسسالام'),
    (r'\bئەلەيھىسساالم\b', 'ئەلەيھىسسالام'),
    (r'\bساھابېلېرېغا\b', 'ساھابىلىرىغا'),
    (r'\bساھابىلىرى\b', 'ساھابىلىرى'),
    (r'\bتاۋابېئاتلېرېغا\b', 'تاۋابىئاتلىرىغا'),
    (r'\bبېزلەرگېچە\b', 'بىزلەرگىچە'),
    (r'\bبېزلەرگە\b', 'بىزلەرگە'),
    (r'\bبېزگە\b', 'بىزگە'),
    (r'\bبېزنى\b', 'بىزنى'),
    (r'\bبېزنىڭ\b', 'بىزنىڭ'),
    (r'\bبېز\b', 'بىز'),
    (r'\bبېر\b', 'بىر'),
    (r'\bبېرىنى\b', 'بىرىنى'),
    (r'\bبېرىگە\b', 'بىرىگە'),
    (r'\bبېرى\b', 'بىرى'),
    (r'\bبېرنەرسە\b', 'بىر نەرسە'),
    (r'\bقېيامەتكېچە\b', 'قىيامەتكىچە'),
    (r'\bقېيامەت\b', 'قىيامەت'),
    (r'\bمۇبارەك\b', 'مۇبارەك'),
]

class AileExtractor:
    def __init__(self, pdf_path):
        self.doc = fitz.open(pdf_path)
        self.font_cache = {}
        self.cmd_pattern = re.compile(
            r'(/F\w+)\s+[\d\.]+\s+Tf|'
            r'([-\d\.]+)\s+([-\d\.]+)\s+Td|'
            r'([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+Tm|'
            r'\[(.*?)\]\s*TJ|'
            r'<([0-9a-fA-F]+)>\s*Tj'
        )

    def get_font_glyphs(self, xref):
        if xref in self.font_cache:
            return self.font_cache[xref]
        obj = self.doc.xref_object(xref)
        desc_match = re.search(r'/DescendantFonts\s+(\d+)', obj)
        if desc_match:
            arr_obj = self.doc.xref_object(int(desc_match.group(1)))
            cid_font_xref = int(re.search(r'(\d+)\s+0\s+R', arr_obj).group(1))
            cid_font_obj = self.doc.xref_object(cid_font_xref)
            fd_xref = int(re.search(r'/FontDescriptor\s+(\d+)', cid_font_obj).group(1))
        elif '/DescendantFonts' in obj:
            m = re.search(r'/DescendantFonts\s*\[\s*(\d+)', obj)
            cid_font_xref = int(m.group(1))
            cid_font_obj = self.doc.xref_object(cid_font_xref)
            fd_xref = int(re.search(r'/FontDescriptor\s+(\d+)', cid_font_obj).group(1))
        elif '/FontDescriptor' in obj:
            fd_xref = int(re.search(r'/FontDescriptor\s+(\d+)', obj).group(1))
        else:
            return None
        fd_obj = self.doc.xref_object(fd_xref)
        m = re.search(r'/FontFile2\s+(\d+)', fd_obj)
        if not m:
            return None
        ff2_xref = int(m.group(1))
        tt = TTFont(io.BytesIO(self.doc.xref_stream(ff2_xref)))
        self.font_cache[xref] = tt.getGlyphOrder()
        return self.font_cache[xref]

    def extract_page_lines(self, page_idx):
        page = self.doc[page_idx]
        font_map = {}
        for f in page.get_fonts():
            font_map[f[4]] = self.get_font_glyphs(f[0])

        contents = b''.join([self.doc.xref_stream(c) for c in page.get_contents()]).decode('latin1', errors='ignore')
        contents = contents.replace('\r\n', '\n').replace('\r', '\n')

        items = []
        cur_font = None
        cur_x, cur_y = 0, 0

        for m in self.cmd_pattern.finditer(contents):
            g = m.groups()
            if g[0]:
                cur_font = g[0].lstrip('/')
            elif g[1] is not None:
                cur_x += float(g[1])
                cur_y += float(g[2])
            elif g[3] is not None:
                cur_x = float(g[7])
                cur_y = float(g[8])
            elif g[9] is not None:
                tj = g[9]
                hex_strings = re.findall(r'<([0-9a-fA-F]+)>', tj)
                chars = []
                for hx in hex_strings:
                    for k in range(0, len(hx), 4):
                        cid = int(hx[k:k+4], 16)
                        fo = font_map.get(cur_font)
                        if fo and cid < len(fo):
                            gname = fo[cid]
                            chars.append(GLYPH_TO_UEY.get(gname, ''))
                txt = ''.join(chars)
                if txt.strip():
                    items.append((cur_y, cur_x, txt[::-1]))
            elif g[10] is not None:
                hx = g[10]
                chars = []
                for k in range(0, len(hx), 4):
                    cid = int(hx[k:k+4], 16)
                    fo = font_map.get(cur_font)
                    if fo and cid < len(fo):
                        gname = fo[cid]
                        chars.append(GLYPH_TO_UEY.get(gname, ''))
                txt = ''.join(chars)
                if txt.strip():
                    items.append((cur_y, cur_x, txt[::-1]))

        # Cluster by y
        lines_by_y = defaultdict(list)
        for y, x, txt in items:
            # Filter running headers (y > 510 in PDF coordinates)
            if y > 510:
                continue
            # Cluster within 3.5 pt
            found_y = None
            for ky in lines_by_y:
                if abs(ky - y) < 3.5:
                    found_y = ky
                    break
            if found_y is None:
                found_y = y
            lines_by_y[found_y].append((x, txt))

        result = []
        for y in sorted(lines_by_y.keys(), reverse=True):
            # Sort within line by x descending (RTL order)
            sorted_chunks = [t for x, t in sorted(lines_by_y[y], key=lambda item: item[0], reverse=True)]
            line_str = ' '.join(sorted_chunks).strip()
            # Clean spaces
            line_str = re.sub(r'[ \t]+', ' ', line_str)
            if line_str:
                result.append(line_str)
        return result

    def clean_text(self, text):
        # Join single separated letters like "ت ە ر ە ققىي" or "م ە كتىپى"
        text = re.sub(r'(\b[ئا-ە])\s+([ئا-ە]\b)', r'\1\2', text)
        for pattern, rep in WORD_REPLACEMENTS:
            text = re.sub(pattern, rep, text)
        # Escape MDX/JSX sensitive characters
        text = text.replace('{', '&#123;').replace('}', '&#125;')
        return text

    def extract_page_range(self, start_page, end_page):
        all_lines = []
        for p in range(start_page - 1, end_page):
            if p < len(self.doc):
                lines = self.extract_page_lines(p)
                for l in lines:
                    cleaned = self.clean_text(l)
                    if cleaned:
                        all_lines.append(cleaned)
                all_lines.append("")
        return self.format_markdown_content(all_lines)

    def format_markdown_content(self, lines):
        output = []
        
        for line in lines:
            line = line.strip()
            if not line:
                if output and output[-1] != "":
                    output.append("")
                continue

            # Major divisions
            if line.startswith("بىرىنچى بۆلۈم") or line.startswith("ئىككىنچى بۆلۈم") or \
               line.startswith("ئۈچىنچى بۆلۈم") or line.startswith("تۆتىنچى بۆلۈم") or \
               line.startswith("بەشىنچى بۆلۈم"):
                output.append(f"\n## {line}\n")
                continue

            # Check if line is a numbered major section or subtopic
            if re.match(r'^\d+\s*[\.–]\s*[ئا-ەA-Za-z]', line) or \
               line in [
                   "ئائىلە قۇرۇش", "ئائىلە قۇرۇش چوڭ نېئمەت", "ئائىلە قۇرۇش بىر مۆجىزە", "ئۆيلىنىشنىڭ ھۆكمى",
                   "مۇسۇلمان ئادەمنىڭ ئۆيلىنىشتىكى مۇددىئاسى", "ھارامدىن ساقلىنىش", "پەرزەنت كۆرۈش",
                   "ئىنسانلارنى ئۆيلىنىشكە تەشەببۇس قىلىشنىڭ ھېكمىتى", "تۇرمۇش قۇرغۇچىلاردا بولىدىغان سۈپەتلەر",
                   "تۇرمۇش قۇرۇشتا ئەرلەرنىڭ جۈپ تاللاش پرىنسىپى", "تۇرمۇش قۇرۇشتا ئاياللارنىڭ جۈپ تاللاش پرىنسىپى",
                   "مۇھەببەت", "ئىشق", "كۈندەشلىك", "ئىسلام دىنىدىكى كۈندەشلىكنىڭ مەنىسى", "ئالدانغان ئىشەنچ",
                   "غۇرۇرنىڭ يوقالغانلىقى ئەركەكلىكنىڭ ئۆلگەنلىكىدۇر", "يامان ئاقىۋەتلەرگە سەۋەب بولىدىغان بوشلۇقلار",
                   "مەھرەم ۋە نامەھرەم ئۇقۇملىرى", "مەھرىمى يوق ئايال سەپەرگە چىقىش مەسىلىسى",
                   "ئەۋرەت ۋە ئۇنىڭ چەك-چېگراسى", "ئاياللارنىڭ ئاۋازى ئەۋرەت ئەمەس", "مۇسۇلمانلارنىڭ تۇرمۇش قۇرۇشتىكى پرىنسىپى",
                   "مۇسۇلمان ئەرنىڭ مۇسۇلمان ئەمەس ئايالغا ئۆيلىنىش مەسىلىسى", "مۇسۇلمان قىزلار مۇسۇلمان ئەمەسلەرگە ھارامدۇر",
                   "مۇسۇلمان ئاياللارنى مۇسۇلمان ئەمەسلەرگە ياتلىق قىلماسلىقنىڭ سىرى", "ۋاقىتلىق نىكاھلىنىشنىڭ ھاراملىقى",
                   "نىكاھلىنىشتا مەڭگۈلۈك بولۇش نىيىتى شەرت", "ئىسلام دىنى ۋە كۆپ خوتۇنلۇق بولۇش مەسىلىسى",
                   "ئۆيلەنگۈچىلەرنىڭ بىر-بىرىنى كۆرۈشى", "تويدىن بۇرۇنقى ئۇچرىشىشنىڭ شەرتلىرى",
                   "قىز-ئوغۇللارنىڭ جۈپ تاللاشتىكى ئىختىيارى", "ئۆيلىنىشتىكى بەزى قىيىنچىلىقلار",
                   "نىكاھلىنىشقا بولمايدىغان ئاياللار", "ئېمىلداشلىق ۋە ئۇنىڭ شەرتلىرى",
                   "سۆز سالدۇرۇش", "نىشانلىنىش", "تويدىكى خۇشاللىق تەنتەنىسى", "نىكاھ ۋە ئۇنىڭ ئەھكاملىرى",
                   "نىكاھ بىلەن بەلگىلىنىدىغان ئىشلار", "مەھرى", "نەپىقە", "مىراس", "قۇرئان كەرىمدىكى مىراس ئايەتلىرى",
                   "ئەر-خوتۇنلۇق ھاياتى", "دەسلەپكى ئۇچرىشىش", "جىنسىي ئالاقە", "يېقىنچىلىقنىڭ مۇقەددىمىلىرى",
                   "يېقىنچىلىقنىڭ ئەدەپلىرى", "ئاياللارغا خاس ھالەتلەر", "سپېرما ۋە ئۇنىڭغا مۇناسىۋەتلىك مەسىلىلەر",
                   "ئائىلىنىڭ مەسئۇلىيىتى", "ئەر بىلەن ئايالنىڭ باراۋەرلىكى", "ئەر-ئايال ئوتتۇرىسىدىكى ھەق-ھوقۇقلار",
                   "ئىناقلىق ئاياللارنى ھۆرمەتلەشتىن باشلىنىدۇ", "ئاياللارنىڭ كىيىنىشى ۋە سەپەر قىلىشىدىكى بەلگىلىمىلەر",
                   "ھامىلدار بولۇشنىڭ ئالدىنى ئېلىش مەسىلىسى", "قورساقتا بالىنى چۈشۈرۈۋېتىش جىنايىتى",
                   "تۆرەلمىگە قاچان جان كىرىدۇ", "ئەقىقە ۋە ئۇنىڭ ئەھمىيىتى", "ئوغۇللارنى خەتنە قىلىش ۋە خەتنە توي",
                   "ئانا-بالا ھەقلىرى", "ئاياللارنىڭ ھەق-ھوقۇقلىرى", "ئەر-ئايال ئارىسىنى ئىسلاھ قىلىش ئۇسۇلى",
                   "ھىجابنىڭ ئىسلام شەرىئىتىدىكى ئۆلچىمى", "ئائىلىنىڭ باشقىلار بىلەن بولغان مۇناسىۋىتى",
                   "سىلە-رەھىم ۋە ئۇنىڭ ئەھكاملىرى", "قوشنىلار بىلەن ياخشى ئۆتۈشنىڭ پرىنسىپلىرى",
                   "ئەر-خوتۇن مۇناسىۋىتىنىڭ بۇزۇلۇشى", "تالاق ۋە ئۇنىڭ ئەھكاملىرى", "تالاق قىلىشنىڭ تۈرلىرى",
                   "تالاقتىن كېيىنكى ھەق-ھوقۇقلار", "ئاتا-ئانىلارنىڭ بالىلىرى ئۈستىدىكى ھەقلىرى",
                   "ئاتا-ئانىنىڭ ئۇلۇغلۇقى", "ئاتا-ئانىڭىزنى ھايات ۋاقتىدا خۇش قىلىڭ", "ئاتا-ئانىلار ھەققىدە 30 مۇھىم تەۋسىيە",
                   "ئاتا-ئانىنى قاقشىتىشنىڭ گۇناھى", "بالىلار نېئمەت ۋە ئامانەتتۇر", "بالا تەربىيىسى ئاتا-ئانىنىڭ بۇرچى",
                   "بالىلارنىڭ ئاتا-ئانىلار ئۈستىدىكى ھەقلىرى", "تەربىيەنىڭ مەسئۇلىيىتى", "ئائىلە ھاياتى ھەققىدە سوئال - جاۋابلار"
               ]:
                output.append(f"\n### {line}\n")
                continue

            # Quranic ayah quote block
            if line.startswith("﴿") or line.startswith("»") or line.startswith("«") or (line.startswith("(") and ("سۈرىسى" in line or "ئايەت" in line)):
                output.append(f"> {line}")
            else:
                output.append(line)

        return "\n\n".join([p for p in "\n".join(output).split("\n\n") if p.strip()])


CHAPTER_DEFINITIONS = [
    {
        "dir": "00-muqeddimu",
        "filename": "01-muqeddimiler-ve-aptur.mdx",
        "title": "مۇقەددىمىلەر ۋە ئاپتور ھەققىدە",
        "sidebar_label": "مۇقەددىمىلەر ۋە ئاپتور",
        "order": 1,
        "start": 7,
        "end": 24,
        "description": "ئەسەرنىڭ 1-، 2-، 3- ۋە 4-نەشر مۇقەددىمىلىرى ھەمدە ئاپتور مۇھەممەد يۈسۈپنىڭ تەپسىلىي تەرجىمىھالى."
    },
    {
        "dir": "01-qurulushi",
        "filename": "01-aile-qurush-ve-usulliri.mdx",
        "title": "ئائىلە قۇرۇش، ھېكمەتلىرى ۋە جۈپ تاللاش پرىنسىپلىرى",
        "sidebar_label": "ئائىلە قۇرۇش ۋە جۈپ تاللاش",
        "order": 1,
        "start": 40,
        "end": 81,
        "description": "ئائىلە قۇرۇشنىڭ نېئمەتلىكى، ئۆيلىنىشنىڭ ھۆكمى ۋە ھېكمەتلىرى، ئەر-ئاياللارنىڭ جۈپ تاللاش پرىنسىپلىرى، مۇھەببەت ۋە غۇرۇر."
    },
    {
        "dir": "01-qurulushi",
        "filename": "02-mehrem-ve-ewret.mdx",
        "title": "مەھرەم ۋە نامەھرەم، ئەۋرەت چېگرالىرى ۋە غەيرى دىندىكىلەر بىلەن توي",
        "sidebar_label": "مەھرەم ۋە ئەۋرەت چېگرالىرى",
        "order": 2,
        "start": 82,
        "end": 100,
        "description": "مەھرەم ۋە نامەھرەم ئۇقۇملىرى، ئەۋرەتنىڭ چېگرالىرى، سەپەر بەلگىلىمىلىرى ۋە غەيرى دىندىكىلەر بىلەن تويلىشىش ھۆكۈملىرى."
    },
    {
        "dir": "01-qurulushi",
        "filename": "03-nikah-ehkamliri.mdx",
        "title": "نىكاھ ئەھكاملىرى، كۆپ خوتۇنلۇق ۋە ھارام بولغان ئاياللار",
        "sidebar_label": "نىكاھ ئەھكاملىرى ۋە ئېمىلداشلىق",
        "order": 3,
        "start": 101,
        "end": 128,
        "description": "ۋاقىتلىق نىكاھنىڭ ھاراملىقى، كۆپ خوتۇنلۇق بولۇش شەرتلىرى، تويدىن بۇرۇن كۆرۈشۈش، چەكلەنگەن ئاياللار ۋە ئېمىلداشلىق قائىدىلىرى."
    },
    {
        "dir": "01-qurulushi",
        "filename": "04-toy-ve-meros.mdx",
        "title": "سۆز سالدۇرۇش، توي خۇشاللىقى ۋە قۇرئاندىكى مىراس تەقسىماتى",
        "sidebar_label": "توي ئەدەپلىرى ۋە مىراس نىزامى",
        "order": 4,
        "start": 129,
        "end": 176,
        "description": "ئەلچىلىك، نىشانلىنىش، توي تەنتەنىسى ۋە ساز چېلىش، مەھر، نەپىقە ھەمدە قۇرئان كەرىمدىكى تولۇق مىراس پېيىلىرى."
    },
    {
        "dir": "02-er-ayalliq-hayat",
        "filename": "01-jinsi-alaqe-ve-adabliri.mdx",
        "title": "ئەر-خوتۇنلۇق جىنسىي ھايات ۋە يېقىنچىلىق ئەدەپلىرى",
        "sidebar_label": "جىنسىي ھايات ۋە ئەدەپلەر",
        "order": 1,
        "start": 181,
        "end": 192,
        "description": "دەسلەپكى ئۇچرىشىش، ھالال ۋە ھارام يېقىنچىلىق، تۈرلىرى، بەدەن پاكلىقى، زىننەت ۋە سىر ساقلاش ئەدەپلىرى."
    },
    {
        "dir": "02-er-ayalliq-hayat",
        "filename": "02-ayallargha-xas-haletler.mdx",
        "title": "ئاياللارغا خاس ھالەتلەر ۋە سۇيۇقلۇقلارنىڭ ھۆكۈملىرى",
        "sidebar_label": "ئاياللارغا خاس ھالەتلەر ۋە پاكلىق",
        "order": 2,
        "start": 193,
        "end": 211,
        "description": "ھەيز، نىفاس، ئىستىھازە مەزگىلىدىكى ئەھكاملار، ئارقا تەرەپكە كېلىشنىڭ ھاراملىقى، سپېرما، مەزى، ۋەدى ھۆكۈملىرى ۋە ئېھتىلام."
    },
    {
        "dir": "02-er-ayalliq-hayat",
        "filename": "03-er-xotun-heq-hoquqliri.mdx",
        "title": "ئەر-ئايالنىڭ ئۆزئارا ھەق-ھوقۇقلىرى، باراۋەرلىك ۋە ئائىلە ئىناقلىقى",
        "sidebar_label": "ئەر-ئايال ھەق-ھوقۇقلىرى",
        "order": 3,
        "start": 212,
        "end": 267,
        "description": "ئائىلىدە مەسئۇلىيەت تەقسىماتى، باراۋەرلىك دائىرىلىرى، ئاياللارنى ھۆرمەتلەش، ھىجاب ۋە كىيىنىش ئۆلچەملىرى."
    },
    {
        "dir": "02-er-ayalliq-hayat",
        "filename": "04-bala-tughulush-ve-xetne.mdx",
        "title": "ھامىلىدارلىق، ئەقىقە، ئوغۇللارنى خەتنە قىلىش ۋە ئانا-بالا ھەقلىرى",
        "sidebar_label": "تۇغۇلۇش، ئەقىقە ۋە خەتنە توي",
        "order": 4,
        "start": 268,
        "end": 302,
        "description": "ھامىلىدارلىقنىڭ ئالدىنى ئېلىش، تۆرەلمىگە جان كىرىش، بالا ئالدۇرۇشنىڭ جىنايەتلىكى، ئەقىقە، خەتنە، بالا بېقىش ۋە ھەزانە ھوقۇقى."
    },
    {
        "dir": "02-er-ayalliq-hayat",
        "filename": "05-islah-ve-ijtimaiy-munasiwetler.mdx",
        "title": "ئەر-ئايال ئارىسىنى ئىسلاھ قىلىش ۋە ئائىلىنىڭ ئىجتىمائىي مۇناسىۋەتلىرى",
        "sidebar_label": "ئىسلاھ قىلىش، سىلە-رەھىم ۋە قوشنا",
        "order": 5,
        "start": 303,
        "end": 364,
        "description": "كېلىشمەسلىكلەرنى ئىسلاھ قىلىش باسقۇچلىرى، تەن جازاسىدىن توسۇش، سىلە-رەھىم، قوشنىدارچىلىق، مېھماندارچىلىق ۋە ئۆيگە كىرىش ئەدەپلىرى."
    },
    {
        "dir": "03-ailining-buzulushi",
        "filename": "01-buzulush-sewebliri-ve-talaq.mdx",
        "title": "ئائىلىنىڭ بۇزۇلۇش سەۋەبلىرى ۋە تالاق ئۇقۇمى",
        "sidebar_label": "بۇزۇلۇش سەۋەبلىرى ۋە تالاق",
        "order": 1,
        "start": 369,
        "end": 384,
        "description": "ئائىلىنى بۇزۇدىغان خەتەرلىك ئامىللار، نامەھرەمگە قاراش، خىيانەت، زىنا ھەمدە تالاق ئەھكاملىرىنىڭ ماھىيىتى."
    },
    {
        "dir": "03-ailining-buzulushi",
        "filename": "02-talaq-turleri-ve-ehkamliri.mdx",
        "title": "تالاق تۈرلىرى، شەرتلىرى ۋە ئالاھىدە ھالەتلەردىكى ھۆكۈملەر",
        "sidebar_label": "تالاق تۈرلىرى ۋە ھۆكۈملىرى",
        "order": 2,
        "start": 385,
        "end": 400,
        "description": "رەجئىي ۋە بائىن تالاق، بىر لەۋزدە ئۈچ تالاق قىلىش، مەس، مەجبۇرلانغان ۋە غەزەپلەنگەننىڭ تالاقى، غائىبلىق، خۇلئى (بەدەلسىز تالاق)."
    },
    {
        "dir": "03-ailining-buzulushi",
        "filename": "03-talaqtin-keyinki-heqler-iddet.mdx",
        "title": "تالاقتىن كېيىنكى ھەق-ھوقۇقلار ۋە ئىددەت ئەھكاملىرى",
        "sidebar_label": "تالاقتىن كېيىنكى ھەقلەر ۋە ئىددەت",
        "order": 3,
        "start": 401,
        "end": 406,
        "description": "قېپقالغان مەھرى، نەپىقە، بالىلارنىڭ چىقىمى، تۇرالغۇ ھوقۇقى، ئايالنىڭ ئىددەت تۇتۇش تۈرلىرى ۋە مۇددىتى."
    },
    {
        "dir": "04-ata-anilar-heqqide",
        "filename": "01-ata-anining-heqliri-ve-ulughluqi.mdx",
        "title": "ئاتا-ئانىنىڭ ئۇلۇغلۇقى، ھەقلىرى ۋە ئۇلارنى خۇش قىلىش",
        "sidebar_label": "ئاتا-ئانىنىڭ ئۇلۇغلۇقى ۋە ھەقلىرى",
        "order": 1,
        "start": 409,
        "end": 429,
        "description": "ئاتا-ئانىغا ياخشىلىق قىلىش پەيغەمبەرلەر ئەخلاقى ۋە جىھادتىن ئەۋزەل ئىبادەت، ھاياتىدا ۋە ۋاپاتىدىن كېيىن رازى قىلىش، ئانىنىڭ پەزىلىتى."
    },
    {
        "dir": "04-ata-anilar-heqqide",
        "filename": "02-ata-anigha-30-tewsiye-ve-gunahlar.mdx",
        "title": "ئاتا-ئانىلار ھەققىدە 30 تەۋسىيە ۋە قاقشىتىشنىڭ ئېغىر گۇناھى",
        "sidebar_label": "30 تەۋسىيە ۋە قاقشىتىشنىڭ گۇناھى",
        "order": 2,
        "start": 430,
        "end": 440,
        "description": "پەرزەنتلەر ئۈچۈن 30 نۇقتىلىق گۈزەل تەۋسىيە، ئاتا-ئانىنى قاقشىتىشنىڭ دۇنيا ۋە ئاخىرەتتىكى ئېغىر جازاسى."
    },
    {
        "dir": "05-balilar-heqqide",
        "filename": "01-bala-terbiyisi-ve-heqliri.mdx",
        "title": "بالىلار نېئمەتتۇر، بالا تەربىيىسى ۋە ئاتا-ئانىنىڭ مەسئۇلىيىتى",
        "sidebar_label": "بالا تەربىيىسى ۋە بالىلار ھەققى",
        "order": 1,
        "start": 445,
        "end": 488,
        "description": "بالىلار ئامانەتتۇر، ياخشى ئۈلگە بولۇش، ئادالەت، بەددۇئا قىلماسلىق، ئېتىقاد، ئەخلاق، ئەقىل ۋە تەن-تەربىيە، يامان ئادەتلەردىن قوغداش."
    },
    {
        "dir": "05-balilar-heqqide",
        "filename": "02-aile-hayatigha-aitt-soal-jawablar.mdx",
        "title": "ئائىلە ھاياتى ھەققىدە سوئال - جاۋابلار (36 سوئال-جاۋاب) ۋە مەنبەلەر",
        "sidebar_label": "36 سوئال-جاۋاب ۋە مەنبەلەر",
        "order": 2,
        "start": 489,
        "end": 505,
        "description": "ئائىلە، نىكاھ، تالاق، ھەيز، ھامىلىدارلىق ۋە مىراسقا دائىر 36 ئەمەلىي پەتىۋا سوئال-جاۋابى ھەمدە كىتاب مەنبەلىرى."
    },
]

def generate_index_mdx():
    return '''---
title: "ئىسلامدىكى ئائىلە تۈزۈمى"
description: "مۇھەممەد يۈسۈپنىڭ «ئىسلامدىكى ئائىلە تۈزۈمى» (نظام الأسرة في الإسلام) ئەسىرى — ئىسلامدا ئائىلە قۇرۇش، ئەر-ئاياللىق ھايات، ئەدەپ-ئەخلاق، تالاق، ئاتا-ئانا ۋە بالىلار ھەق-ھوقۇقلىرى تولۇق تەپسىلىي كۆرسەتمىسى."
template: splash
prev: false
hero:
  title: "ئىسلامدىكى ئائىلە تۈزۈمى"
  tagline: "مۇھەممەد يۈسۈپ — نظام الأسرة في الإسلام (تولۇق كىتاب نۇسخىسى)"
  image:
    file: /aile/cover.png
  actions:
    - text: "مۇقەددىمىدىن باشلاش"
      link: "/aile/00-muqeddimu/01-muqeddimiler-ve-aptur/"
      icon: right-arrow
      variant: primary
    - text: "PDF نۇسخىسىنى چۈشۈرۈش"
      link: "/aile/islamdiki-aile-tuzumi.pdf"
      icon: document
      variant: secondary
---

import { CardGrid, LinkCard } from '@astrojs/starlight/components';

## كىتاب ۋە ئاپتور ھەققىدە

**«ئىسلامدىكى ئائىلە تۈزۈمى» (نظام الأسرة في الإسلام)** ھۆرمەتلىك ئۇستاز، تونۇلغان ئىسلام تەتقىقاتچىسى ۋە دىنىي ئالىم **مۇھەممەد يۈسۈپ (Muhemmed Yusup)** تەرىپىدىن يېزىلغان قىممەتلىك ئەسەردۇر. بۇ كىتاب ئىسلام شەرىئىتىدە ئائىلە قۇرۇشتىن تارتىپ، ئەر-خوتۇن ئوتتۇرىسىدىكى ھەق-ھوقۇقلار، تۇرمۇش ئەدەپلىرى، ئاياللارنىڭ ئورنى ۋە ئەۋرەت چېگرالىرى، پەرزەنت تەربىيىسى، ئاتا-ئانىغا ياخشىلىق قىلىش، ئائىلە كېلىشمەسلىكلىرىنى ھەل قىلىش، تالاق ۋە مىراس ئەھكاملىرىغىچە بولغان پۈتۈن مەسىلىلەرنى قۇرئان كەرىم ئايەتلىرى ۋە سەھىھ ھەدىسلەر ئاساسىدا ئەتراپلىق يورۇتۇپ بېرىدۇ.

ئەسەر جەمئىي بەش چوڭ بۆلۈم، مۇقەددىمىلەر، تەرجىمىھال ۋە ئائىلە مەسىلىلىرىگە دائىر 36 سوئال-جاۋابتىن تەركىب تاپقان.

---

## كىتابنىڭ بۆلۈملىرى

تۆۋەندىكى بۆلۈملەر ئارقىلىق كىتاب مەزمۇنلىرىغا بىۋاسىتە كىرەلەيسىز:

<CardGrid>
  <LinkCard
    title="00-مۇقەددىمىلەر ۋە ئاپتور"
    description="1-، 2-، 3- ۋە 4-نەشر مۇقەددىمىلىرى ھەمدە ئاپتور مۇھەممەد يۈسۈپنىڭ ھاياتى ۋە ئەسەرلىرى."
    href="/aile/00-muqeddimu/01-muqeddimiler-ve-aptur/"
  />
  <LinkCard
    title="01-ئائىلىنىڭ قۇرۇلۇشى"
    description="ئائىلە قۇرۇش، ھېكمىتى، جۈپ تاللاش، مەھرەم-نامەھرەم، نىكاھ، مەھرى، نەپىقە ۋە مىراس ئاساسلىرى."
    href="/aile/01-qurulushi/01-aile-qurush-ve-usulliri/"
  />
  <LinkCard
    title="02-ئەر - ئاياللىق ھايات"
    description="جىنسىي ھايات ۋە ئەدەپلەر، ئاياللارغا خاس ھالەتلەر، ھوقۇقلار، ئەقىقە، خەتنە ۋە تۇغۇت ئەھكاملىرى."
    href="/aile/02-er-ayalliq-hayat/01-jinsi-alaqe-ve-adabliri/"
  />
  <LinkCard
    title="03-ئائىلىنىڭ بۇزۇلۇشى"
    description="ئائىلىنى بۇزغۇچى ئامىللار، زىنا خەۋپى، تالاق تۈرلىرى (رەجئىي، بائىن، خۇلئى) ۋە ئىددەت تۇتۇش."
    href="/aile/03-ailining-buzulushi/01-buzulush-sewebliri-ve-talaq/"
  />
  <LinkCard
    title="04-ئاتا - ئانىلار ھەققىدە"
    description="ئاتا-ئانىنىڭ ئۇلۇغلۇقى، ھاياتىدا ۋە ۋاپاتىدا خۇش قىلىش، 30 مۇھىم تەۋسىيە ۋە ئاتا-ئانىنى قاقشىتىشنىڭ گۇناھى."
    href="/aile/04-ata-anilar-heqqide/01-ata-anining-heqliri-ve-ulughluqi/"
  />
  <LinkCard
    title="05-بالىلار ھەققىدە ۋە سوئال-جاۋابلار"
    description="بالا تەربىيىسى، ئېتىقاد ۋە ئەخلاق يېتەكچىلىكى، ئائىلە ھاياتىغا دائىر 36 سوئال-جاۋاب ۋە پايدىلىنىلغان مەنبەلەر."
    href="/aile/05-balilar-heqqide/01-bala-terbiyisi-ve-heqliri/"
  />
</CardGrid>

---

## تولۇق مۇندەرىجە

### 00-مۇقەددىمىلەر
- [بىرىنچى، ئىككىنچى، ئۈچىنچى، تۆتىنچى نەشر مۇقەددىمىلىرى ۋە ئاپتور ھەققىدە](/aile/00-muqeddimu/01-muqeddimiler-ve-aptur/)

### 01-بىرىنچى بۆلۈم: ئائىلىنىڭ قۇرۇلۇشى
- [1. ئائىلە قۇرۇش، ھېكمەتلىرى ۋە جۈپ تاللاش پرىنسىپلىرى](/aile/01-qurulushi/01-aile-qurush-ve-usulliri/)
- [2. مەھرەم ۋە نامەھرەم، ئەۋرەت چېگرالىرى ۋە غەيرى دىندىكىلەر بىلەن توي](/aile/01-qurulushi/02-mehrem-ve-ewret/)
- [3. نىكاھ ئەھكاملىرى، كۆپ خوتۇنلۇق ۋە ھارام بولغان ئاياللار](/aile/01-qurulushi/03-nikah-ehkamliri/)
- [4. سۆز سالدۇرۇش، توي خۇشاللىقى ۋە قۇرئاندىكى مىراس تەقسىماتى](/aile/01-qurulushi/04-toy-ve-meros/)

### 02-ئىككىنچى بۆلۈم: ئەر - ئاياللىق ھايات
- [1. ئەر-خوتۇنلۇق جىنسىي ھايات ۋە يېقىنچىلىق ئەدەپلىرى](/aile/02-er-ayalliq-hayat/01-jinsi-alaqe-ve-adabliri/)
- [2. ئاياللارغا خاس ھالەتلەر ۋە سۇيۇقلۇقلارنىڭ ھۆكۈملىرى](/aile/02-er-ayalliq-hayat/02-ayallargha-xas-haletler/)
- [3. ئەر-ئايالنىڭ ئۆزئارا ھەق-ھوقۇقلىرى، باراۋەرلىك ۋە ئائىلە ئىناقلىقى](/aile/02-er-ayalliq-hayat/03-er-xotun-heq-hoquqliri/)
- [4. ھامىلىدارلىق، ئەقىقە، ئوغۇللارنى خەتنە قىلىش ۋە ئانا-بالا ھەقلىرى](/aile/02-er-ayalliq-hayat/04-bala-tughulush-ve-xetne/)
- [5. ئەر-ئايال ئارىسىنى ئىسلاھ قىلىش ۋە ئائىلىنىڭ ئىجتىمائىي مۇناسىۋەتلىرى](/aile/02-er-ayalliq-hayat/05-islah-ve-ijtimaiy-munasiwetler/)

### 03-ئۈچىنچى بۆلۈم: ئائىلىنىڭ بۇزۇلۇشى
- [1. ئائىلىنىڭ بۇزۇلۇش سەۋەبلىرى ۋە تالاق ئۇقۇمى](/aile/03-ailining-buzulushi/01-buzulush-sewebliri-ve-talaq/)
- [2. تالاق تۈرلىرى، شەرتلىرى ۋە ئالاھىدە ھالەتلەردىكى ھۆكۈملەر](/aile/03-ailining-buzulushi/02-talaq-turleri-ve-ehkamliri/)
- [3. تالاقتىن كېيىنكى ھەق-ھوقۇقلار ۋە ئىددەت ئەھكاملىرى](/aile/03-ailining-buzulushi/03-talaqtin-keyinki-heqler-iddet/)

### 04-تۆتىنچى بۆلۈم: ئاتا - ئانىلار ھەققىدە
- [1. ئاتا-ئانىنىڭ ئۇلۇغلۇقى، ھەقلىرى ۋە ئۇلارنى خۇش قىلىش](/aile/04-ata-anilar-heqqide/01-ata-anining-heqliri-ve-ulughluqi/)
- [2. ئاتا-ئانىلار ھەققىدە 30 تەۋسىيە ۋە قاقشىتىشنىڭ ئېغىر گۇناھى](/aile/04-ata-anilar-heqqide/02-ata-anigha-30-tewsiye-ve-gunahlar/)

### 05-بەشىنچى بۆلۈم: بالىلار ھەققىدە
- [1. بالىلار نېئمەتتۇر، بالا تەربىيىسى ۋە ئاتا-ئانىنىڭ مەسئۇلىيىتى](/aile/05-balilar-heqqide/01-bala-terbiyisi-ve-heqliri/)
- [2. ئائىلە ھاياتى ھەققىدە سوئال - جاۋابلار (36 سوئال-جاۋاب) ۋە مەنبەلەر](/aile/05-balilar-heqqide/02-aile-hayatigha-aitt-soal-jawablar/)
'''

def main():
    print(f"Starting extraction from {PDF_PATH}...")
    if not PDF_PATH.exists():
        print(f"Error: {PDF_PATH} does not exist!")
        sys.exit(1)

    extractor = AileExtractor(str(PDF_PATH))
    print(f"Opened PDF with {len(extractor.doc)} pages.")

    # Create directories
    for ch in CHAPTER_DEFINITIONS:
        ch_dir = DOCS_DIR / ch["dir"]
        ch_dir.mkdir(parents=True, exist_ok=True)

    # Write index.mdx
    index_path = DOCS_DIR / "index.mdx"
    index_path.write_text(generate_index_mdx(), encoding="utf-8")
    print(f"Generated index page: {index_path}")

    # Generate each chapter
    for ch in CHAPTER_DEFINITIONS:
        out_file = DOCS_DIR / ch["dir"] / ch["filename"]
        print(f"Extracting pages {ch['start']} to {ch['end']} for {ch['filename']}...")
        body = extractor.extract_page_range(ch["start"], ch["end"])

        mdx_content = f"""---
title: "{ch['title']}"
description: "{ch['description']}"
sidebar:
  label: "{ch['sidebar_label']}"
  order: {ch['order']}
---

{body}
"""
        out_file.write_text(mdx_content, encoding="utf-8")
        print(f"  -> Successfully generated {out_file.name} ({len(mdx_content)} bytes)")

    print("\nExtraction complete! All 17 chapters + index.mdx created.")

if __name__ == "__main__":
    main()
