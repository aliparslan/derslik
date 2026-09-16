#!/usr/bin/env python3
"""
Regenerates all Section 01 and Section 02 MDX files with:
1. Clear Markdown block headings (##) with anchors.
2. Direct clickable anchor links on each question (both number badge and permalink icon).
3. Preserving 100% of question text, answer text, footnotes, and 99 Names table.
"""

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "tools" / "extracted_2000.json"
DOCS_ROOT = ROOT / "src" / "content" / "docs" / "2000"
ETIQAD_DIR = DOCS_ROOT / "01-etiqad"
IBADET_DIR = DOCS_ROOT / "02-ibadet"

# Map of pages and blocks with question ranges
PAGES_CONFIG = [
    # Section 01: Etiqad (Q1-163)
    {
        "dir": ETIQAD_DIR,
        "filename": "01-din-ve-etiqad.mdx",
        "title": "دىن ۋە ئىنسان",
        "description": "دىن ۋە ئىنسان — سوئال 1–20",
        "order": 1,
        "blocks": [
            {"title": "دىن ۋە دۇنيادىكى دىنلارنىڭ تۈرلىرى", "q_start": 1, "q_end": 16},
            {"title": "ئىسلام دىنى ۋە ئۇنىڭ غايىسى", "q_start": 17, "q_end": 20},
        ],
    },
    {
        "dir": ETIQAD_DIR,
        "filename": "02-allahqa-iman.mdx",
        "title": "ئاللاھقا ئىمان كەلتۈرۈش",
        "description": "ئاللاھقا ئىمان كەلتۈرۈش — سوئال 21–48",
        "order": 2,
        "blocks": [
            {"title": "ئىماننىڭ ئاساسىي پىرىنسىپلىرى", "q_start": 21, "q_end": 24},
            {"title": "ئەخلاق ۋە ئۇنىڭ تۈرلىرى", "q_start": 25, "q_end": 27},
            {"title": "كەلىمە تەييىبە ۋە شاھادەت كەلىمىسى", "q_start": 28, "q_end": 32},
            {"title": "ئىنساننىڭ يارىتىلىش مەقسىتى ۋە ۋەزىپىسى", "q_start": 33, "q_end": 34},
            {"title": "ئاللاھقا ئىمان كەلتۈرۈش ھەقىقەتلىرى", "q_start": 35, "q_end": 37},
            {"title": "ئاللاھ تائالانى تونۇشنىڭ ۋاسىتىلىرى", "q_start": 38, "q_end": 40},
            {"title": "ئەقىلنىڭ ۋەزىپىسى ۋە ئىسلامدىكى ئورنى", "q_start": 41, "q_end": 41},
            {"title": "ئاللاھنىڭ سۈپەتلىرى ئارقىلىق تونۇش", "q_start": 42, "q_end": 45},
            {"title": "ئاللاھنى قۇرئان ۋە ھەدىستىكى سۈپەتلىرىدىن تونۇش", "q_start": 46, "q_end": 48},
        ],
    },
    {
        "dir": ETIQAD_DIR,
        "filename": "03-allahning-isimliri.mdx",
        "title": "ئاللاھنىڭ گۈزەل ئىسىملىرى ۋە سۈپەتلىرى",
        "description": "ئاللاھنىڭ گۈزەل ئىسىملىرى ۋە سۈپەتلىرى — سوئال 49–62",
        "order": 3,
        "include_99_names": True,
        "blocks": [
            {"title": "ئاللاھ تائالانىڭ 99 گۈزەل ئىسمى", "is_table": True},
            {"title": "ئىسىم بىلەن سۈپەت ئوتتۇرىسىدىكى پەرق", "q_start": 49, "q_end": 49},
            {"title": "سۈپەتلەرنىڭ تۈرلىنىشى", "q_start": 50, "q_end": 52},
            {"title": "ئاللاھ تائالانىڭ زاتىي سۈپەتلىرى", "q_start": 53, "q_end": 61},
            {"title": "ئاللاھ تائالانى كۆرۈش ھەققىدە", "q_start": 62, "q_end": 62},
        ],
    },
    {
        "dir": ETIQAD_DIR,
        "filename": "04-perishtiler-jinlar.mdx",
        "title": "پەرىشتىلەر، جىنلار ۋە شەيتانلار",
        "description": "پەرىشتىلەر، جىنلار ۋە شەيتانلار — سوئال 63–82",
        "order": 4,
        "blocks": [
            {"title": "روھىي ئالەملەرنىڭ ھەقىقىتى", "q_start": 63, "q_end": 64},
            {"title": "پەرىشتىلەرگە ئىمان كەلتۈرۈش", "q_start": 65, "q_end": 68},
            {"title": "پەرىشتىلەرنىڭ خاراكتېرى ۋە ۋەزىپىلىرى", "q_start": 69, "q_end": 72},
            {"title": "جىنلارنىڭ ھەقىقىتى ۋە تائىپىلىرى", "q_start": 73, "q_end": 77},
            {"title": "شەيتانلارنىڭ خاراكتېرى ۋە ئىبلىس", "q_start": 78, "q_end": 82},
        ],
    },
    {
        "dir": ETIQAD_DIR,
        "filename": "05-samawiy-kitablar.mdx",
        "title": "ساماۋىي كىتابلار ۋە قۇرئان كەرىم",
        "description": "ساماۋىي كىتابلار ۋە قۇرئان كەرىم — سوئال 83–96",
        "order": 5,
        "blocks": [
            {"title": "ساماۋىي كىتابلارغا ئىمان كەلتۈرۈش", "q_start": 83, "q_end": 85},
            {"title": "چۈشۈرۈلگەن كىتابلار ۋە ۋەھيى", "q_start": 86, "q_end": 91},
            {"title": "قۇرئان كەرىم ۋە ئۇنىڭ مۆجىزىلىرى", "q_start": 92, "q_end": 96},
        ],
    },
    {
        "dir": ETIQAD_DIR,
        "filename": "06-peyghamberler.mdx",
        "title": "پەيغەمبەرلەرگە ئىمان كەلتۈرۈش",
        "description": "پەيغەمبەرلەرگە ئىمان كەلتۈرۈش — سوئال 97–115",
        "order": 6,
        "blocks": [
            {"title": "پەيغەمبەرلىك ماقامى ۋە ئەۋەتىلىش سەۋەبى", "q_start": 97, "q_end": 99},
            {"title": "پەيغەمبەرلەرنىڭ سانى ۋە قۇرئاندىكى ناملىرى", "q_start": 100, "q_end": 103},
            {"title": "پەيغەمبەرلەرنىڭ دەلىللىرى ۋە ئالاھىدىلىكلىرى", "q_start": 104, "q_end": 108},
            {"title": "ھەزرىتى مۇھەممەد ئەلەيھىسسالام ۋە دۇرۇدلار", "q_start": 109, "q_end": 115},
        ],
    },
    {
        "dir": ETIQAD_DIR,
        "filename": "07-qada-qeder.mdx",
        "title": "قازا ۋە قەدەرگە ئىمان كەلتۈرۈش",
        "description": "قازا ۋە قەدەرگە ئىمان كەلتۈرۈش — سوئال 116–134",
        "order": 7,
        "blocks": [
            {"title": "قازا ۋە قەدەرنىڭ مەنىسى ھەم ماھىيىتى", "q_start": 116, "q_end": 119},
            {"title": "قازا-قەدەر بىلەن سەۋەبنىڭ مۇناسىۋىتى ۋە پايدىسى", "q_start": 120, "q_end": 122},
            {"title": "ھىدايەت ۋە زالالەت ئەھكاملىرى", "q_start": 123, "q_end": 127},
            {"title": "تەۋەككۈل ۋە ئۇنىڭ شەرتلىرى", "q_start": 128, "q_end": 129},
            {"title": "قازا-قەدەرگە ئالاقىدار سوئاللارغا جاۋاب", "q_start": 130, "q_end": 131},
            {"title": "ئىنساننىڭ ئىختىيارىدىن تاشقىرى ئىشلار ۋە لەۋھۇلمەھپۇز", "q_start": 132, "q_end": 134},
        ],
    },
    {
        "dir": ETIQAD_DIR,
        "filename": "08-qiyamet-axiret.mdx",
        "title": "قىيامەت ۋە ئاخىرەتكە ئىمان كەلتۈرۈش",
        "description": "قىيامەت ۋە ئاخىرەتكە ئىمان كەلتۈرۈش — سوئال 135–163",
        "order": 8,
        "blocks": [
            {"title": "قىيامەت كۈنىگە ئىمان ۋە قايتا تىرىلىش دەلىللىرى", "q_start": 135, "q_end": 140},
            {"title": "قىيامەتنىڭ كىچىك ۋە چوڭ ئالامەتلىرى", "q_start": 141, "q_end": 142},
            {"title": "قەبرە ھاياتى، بەرزەخ ئالىمى ۋە روھلارنىڭ قارارگاھى", "q_start": 143, "q_end": 148},
            {"title": "قىيامەت كۈنىدىكى سوت، ھېساب، مىزان ۋە سىرات", "q_start": 149, "q_end": 160},
            {"title": "جەننەت بىلەن دوزاخ ۋە ئۇلارنىڭ مەڭگۈلۈكلىكى", "q_start": 161, "q_end": 163},
        ],
    },

    # Section 02: Ibadet (Q164-647)
    {
        "dir": IBADET_DIR,
        "filename": "01-ibadet-esasliri.mdx",
        "title": "ئىبادەتنىڭ ئەسلىي ماھىيىتى",
        "description": "ئىبادەتنىڭ ئەسلىي ماھىيىتى — سوئال 164–183",
        "order": 1,
        "blocks": [
            {"title": "ئىبادەتنىڭ ماھىيىتى ۋە قوبۇل بولۇش شەرتلىرى", "q_start": 164, "q_end": 169},
            {"title": "ئىبادەتتە ئىخلاس، نىيەت ۋە ئىھسان", "q_start": 170, "q_end": 174},
            {"title": "ئىبادەت تۈرلىرى ۋە ئورۇنداش شەرتلىرى", "q_start": 175, "q_end": 181},
            {"title": "بالىلارنىڭ بالاغەتكە يېتىشى ۋە نىشانلىرى", "q_start": 182, "q_end": 183},
        ],
    },
    {
        "dir": IBADET_DIR,
        "filename": "02-sheriet-istilahliri.mdx",
        "title": "شەرىئەت ئىستىلاھلىرى",
        "description": "شەرىئەت ئىستىلاھلىرى — سوئال 184–204",
        "order": 2,
        "blocks": [
            {"title": "شەرىئەت ئىستىلاھلىرى ۋە پەرزنىڭ تۈرلىرى", "q_start": 184, "q_end": 190},
            {"title": "ۋاجىب ۋە سۈننەت ئەھكاملىرى", "q_start": 191, "q_end": 196},
            {"title": "ھارام ۋە مەكرۇھنىڭ دەرىجىلىرى", "q_start": 197, "q_end": 200},
            {"title": "مۇباھ ئەمەللەرنىڭ ئىبادەتكە ئايلىنىشى", "q_start": 201, "q_end": 204},
        ],
    },
    {
        "dir": IBADET_DIR,
        "filename": "03-pakliq-taharet.mdx",
        "title": "پاكىزلىق ۋە تاھارەت",
        "description": "پاكىزلىق ۋە تاھارەت — سوئال 205–248",
        "order": 3,
        "blocks": [
            {"title": "پاكىزلىقنىڭ ئىسلامدىكى ئەھمىيىتى ۋە سۇلارنىڭ تۈرلىرى", "q_start": 205, "q_end": 216},
            {"title": "ئىستىنجا، ئىستىبرا ۋە ھاجەتخانا ئەدەپلىرى", "q_start": 217, "q_end": 224},
            {"title": "نىجاسەتنىڭ تۈرلىرى ۋە پاكلاش ئۇسۇللىرى", "q_start": 225, "q_end": 231},
            {"title": "تاھارەتنىڭ پەرز، سۈننەتلىرى ۋە ئەمەلىي تەرتىپى", "q_start": 232, "q_end": 236},
            {"title": "مىسۋاك، تاھارەتنى بۇزىدىغان ۋە بۇزمايدىغان ئامىللار", "q_start": 237, "q_end": 241},
            {"title": "پايپاققا ۋە تېڭىققا مەسھى قىلىش ھەم ئۆزۈرلۈكلەر تاھارىتى", "q_start": 242, "q_end": 248},
        ],
    },
    {
        "dir": IBADET_DIR,
        "filename": "04-ayallargha-xas.mdx",
        "title": "ئاياللارغا خاس ئەھكاملار",
        "description": "ئاياللارغا خاس ئەھكاملار — سوئال 249–259",
        "order": 4,
        "blocks": [
            {"title": "ھەيز ۋە نىپاس ئەھكاملىرى", "q_start": 249, "q_end": 255},
            {"title": "ئىستىھازە ۋە تاھارەتسىز چەكلەنگەن ئىشلار", "q_start": 256, "q_end": 259},
        ],
    },
    {
        "dir": IBADET_DIR,
        "filename": "05-ghusul-teyemmum.mdx",
        "title": "غۇسلى ۋە تەيەممۇم",
        "description": "غۇسلى ۋە تەيەممۇم — سوئال 260–274",
        "order": 5,
        "blocks": [
            {"title": "غۇسلىنىڭ پەرزلىرى، سۈننەتلىرى ۋە تەرتىپى", "q_start": 260, "q_end": 268},
            {"title": "تەيەممۇمنىڭ شەرتلىرى، پەرزلىرى ۋە تەرتىپى", "q_start": 269, "q_end": 274},
        ],
    },
    {
        "dir": IBADET_DIR,
        "filename": "06-namaz-ehkamliri.mdx",
        "title": "نامازنىڭ شەرتلىرى ۋە پەرزلىرى",
        "description": "نامازنىڭ شەرتلىرى ۋە پەرزلىرى — سوئال 275–332",
        "order": 6,
        "blocks": [
            {"title": "نامازنىڭ ئەھمىيىتى، ئورنى ۋە خۇشۇئ روھى", "q_start": 275, "q_end": 285},
            {"title": "نامازنىڭ تۈرلىرى ۋە بەش ۋاخ ناماز ھۆكمى", "q_start": 286, "q_end": 293},
            {"title": "نامازنىڭ ۋاقىتلىرى ۋە مەنئى قىلىنغان ۋاقىتلار", "q_start": 294, "q_end": 304},
            {"title": "ئەزان ۋە تەكبىر (قامەت) ئەھكاملىرى", "q_start": 305, "q_end": 315},
            {"title": "ئەۋرەت چەكلىرى، قىبلە ۋە نىيەت مەسىلىلىرى", "q_start": 316, "q_end": 324},
            {"title": "بەش ۋاخ نامازنىڭ رەكئەت تۈزۈلمىسى", "q_start": 325, "q_end": 332},
        ],
    },
    {
        "dir": IBADET_DIR,
        "filename": "07-namaz-oqush.mdx",
        "title": "نامازنىڭ تۈزۈلۈشى ۋە ئوقۇلۇش تەرتىپى",
        "description": "نامازنىڭ تۈزۈلۈشى ۋە ئوقۇلۇش تەرتىپى — سوئال 333–393",
        "order": 7,
        "blocks": [
            {"title": "نامازنىڭ پەرز، ۋاجىب ۋە سۈننەتلىرى", "q_start": 333, "q_end": 342},
            {"title": "بەش ۋاخ نامازنىڭ ئەمەلىي ئوقۇلۇش تەرتىپى", "q_start": 343, "q_end": 353},
            {"title": "ۋىتىر نامىزى، قۇنۇت دۇئاسى ۋە زىكىرلەر", "q_start": 354, "q_end": 356},
            {"title": "نامازدىكى مەكرۇھلار، بۇزىدىغان ئىشلار ۋە شەكلىنىش", "q_start": 357, "q_end": 362},
            {"title": "سەجدە سەھۋى ۋە سۈترە ئەھكاملىرى", "q_start": 363, "q_end": 372},
            {"title": "تىلاۋەت سەجدىسى ئەھكاملىرى", "q_start": 373, "q_end": 381},
            {"title": "قازا نامازلار، جەمئى قىلىش ۋە ئۇلاغلاردا ناماز", "q_start": 382, "q_end": 393},
        ],
    },
    {
        "dir": IBADET_DIR,
        "filename": "08-jamaet-jume.mdx",
        "title": "جامائەت ۋە جۈمە نامىزى",
        "description": "جامائەت ۋە جۈمە نامىزى — سوئال 394–428",
        "order": 8,
        "blocks": [
            {"title": "جامائەت نامىزىنىڭ پەزىلىتى ۋە مەسجىد ئەدەپلىرى", "q_start": 394, "q_end": 398},
            {"title": "ئىماملىق شەرتلىرى ۋە ئىمامغا ئەگىشىش قائىدىلىرى", "q_start": 399, "q_end": 407},
            {"title": "جامائەت سېپى ۋە جامائەتكە ئۈلگۈرۈش", "q_start": 408, "q_end": 418},
            {"title": "جۈمە نامىزى، خۇتبە ئەھكاملىرى ۋە كۈندىلىك سۈننەتلەر", "q_start": 419, "q_end": 428},
        ],
    },
    {
        "dir": IBADET_DIR,
        "filename": "09-bashqa-namazlar.mdx",
        "title": "يولۇچىلار ۋە باشقا نامازلار",
        "description": "يولۇچىلار ۋە باشقا نامازلار — سوئال 429–477",
        "order": 9,
        "blocks": [
            {"title": "يولۇچىلار نامىزى (قەسرى ۋە مۇقاملار ھۆكمى)", "q_start": 429, "q_end": 433},
            {"title": "ھېيت نامازلىرى ۋە تەشرىق تەكبىرلىرى", "q_start": 434, "q_end": 442},
            {"title": "تەراۋىھ نامىزى ۋە رامىزان خەتمىسى", "q_start": 443, "q_end": 451},
            {"title": "كېسەللەر نامىزى، كۇسۇف، خۇسۇف ۋە قورقۇنچ نامازلىرى", "q_start": 452, "q_end": 460},
            {"title": "مۇستەھەب ۋە نەپلە نامازلار (تەھەججۇد، تاۋاپ، تەۋبە، ئىستىخارە)", "q_start": 461, "q_end": 477},
        ],
    },
    {
        "dir": IBADET_DIR,
        "filename": "10-jinaze-depne.mdx",
        "title": "جىنازا نامىزى ۋە دەپنە ئىشلىرى",
        "description": "جىنازا نامىزى ۋە دەپنە ئىشلىرى — سوئال 478–506",
        "order": 10,
        "blocks": [
            {"title": "جىنازا نامىزى، سەكەرات ھالىتى ۋە يۇيۇش-كېپەنلەش", "q_start": 478, "q_end": 494},
            {"title": "مېيىتنى دەپنە قىلىش ۋە لەھەد تەرتىپى", "q_start": 495, "q_end": 498},
            {"title": "قەبرە ئەدەپلىرى، زىيارەت ۋە مېيىتقا ئاتالغان ساۋاب", "q_start": 499, "q_end": 504},
            {"title": "شېھىدلەر ۋە دەپنە تەرتىپى", "q_start": 505, "q_end": 506},
        ],
    },
    {
        "dir": IBADET_DIR,
        "filename": "11-zakat.mdx",
        "title": "زاكات ۋە ئۇنىڭ ئەھكاملىرى",
        "description": "زاكات ۋە ئۇنىڭ ئەھكاملىرى — سوئال 507–553",
        "order": 11,
        "blocks": [
            {"title": "زاكاتنىڭ مەنىسى، ئەھمىيىتى ۋە پەرز بولۇش نىسابى", "q_start": 507, "q_end": 517},
            {"title": "نەق پۇل، تىجارەت، چارۋا ۋە زىرائەتلەر زاكىتى", "q_start": 518, "q_end": 532},
            {"title": "زاكات چۈشمەيدىغان ماللار ۋە بېرىش ۋاقتى", "q_start": 533, "q_end": 534},
            {"title": "زاكات بېرىلىدىغان 8 تۈرلۈك كىشىلەر ۋە بېرىلمەيدىغانلار", "q_start": 535, "q_end": 538},
            {"title": "زاكاتقا مۇناسىۋەتلىك پەتۋالار ۋە سوئال-جاۋابلار", "q_start": 539, "q_end": 553},
        ],
    },
    {
        "dir": IBADET_DIR,
        "filename": "12-roza-ramizan.mdx",
        "title": "روزا ۋە رامىزان ئەھكاملىرى",
        "description": "روزا ۋە رامىزان ئەھكاملىرى — سوئال 554–607",
        "order": 12,
        "blocks": [
            {"title": "روزىنىڭ پەرزلىكى ۋە بۇزىدىغان ئامىللار", "q_start": 554, "q_end": 564},
            {"title": "روزىنىڭ تۈرلىرى ۋە رامىزان كۈنلىرىنىڭ پەزىلىتى", "q_start": 565, "q_end": 575},
            {"title": "روزا تۇتماسلىققا رۇخسەتلەر، پىديە ۋە پىتىر سەدىقىسى", "q_start": 576, "q_end": 586},
            {"title": "ئېتىكاپ ۋە روزىغا ئالاقىدار كۈندىلىك سوئاللار", "q_start": 587, "q_end": 607},
        ],
    },
    {
        "dir": IBADET_DIR,
        "filename": "13-hej-omre.mdx",
        "title": "ھەج ۋە ئۆمرە پائالىيىتى",
        "description": "ھەج ۋە ئۆمرە پائالىيىتى — سوئال 608–634",
        "order": 13,
        "blocks": [
            {"title": "ھەجنىڭ پەرز، ۋاجىب ۋە سۈننەتلىرى ھەم تۈرلىرى", "q_start": 608, "q_end": 619},
            {"title": "ئىھرام چەكلىمىلىرى، جازالىرى ۋە ئاياللارغا خاس ھۆكۈملەر", "q_start": 620, "q_end": 624},
            {"title": "ھەج ۋە ئۆمرىنىڭ ئەمەلىي تەرتىپى (كۈندىلىك باسقۇچلار)", "q_start": 625, "q_end": 627},
            {"title": "قۇربانلىق، ئۇنىڭ تۈرلىرى، شەرتلىرى ۋە گۆشىنى تەقسىملەش", "q_start": 628, "q_end": 634},
        ],
    },
    {
        "dir": IBADET_DIR,
        "filename": "14-sawab-gunah.mdx",
        "title": "ساۋاب، گۇناھ ۋە تەۋبە",
        "description": "ساۋاب، گۇناھ ۋە تەۋبە — سوئال 635–647",
        "order": 14,
        "blocks": [
            {"title": "ساۋاب ۋە ئۇنىڭغا ئېرىشىش يوللىرى", "q_start": 635, "q_end": 641},
            {"title": "گۇناھلار، چوڭ گۇناھلار (كەبائىر) ۋە تەۋبە", "q_start": 642, "q_end": 647},
        ],
    },
]


def clean_uyghur(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\u066e", "\u0649")  # dotless beh -> ى
    text = text.replace("\u067b", "\u06d0")  # beeh with 2 vertical dots -> ې
    text = text.replace("\u06cc", "\u064a")  # Farsi yeh -> ي
    text = text.replace("\u06c5", "\u06ad")  # ڭ
    # Strip tatweel between arabic letters
    text = re.sub(r"([\u0600-\u06ff])\u0640+([\u0600-\u06ff])", r"\1\2", text)
    return text.strip()


def build_card_with_direct_links(q: dict) -> str:
    number = q["number"]
    question = clean_uyghur(q["question"])
    answer = clean_uyghur(q["answer"])

    footnotes = q.get("footnotes", [])
    fn_html = ""
    if footnotes:
        clean_fns = []
        for fn in footnotes:
            if not fn:
                continue
            fn_str = fn.get("text", "") if isinstance(fn, dict) else str(fn)
            fn_cleaned = clean_uyghur(fn_str)
            if fn_cleaned:
                clean_fns.append(fn_cleaned)
        if clean_fns:
            fn_items = " ".join(f"<span>[{fn}]</span>" for fn in clean_fns)
            fn_html = f'\n    <div class="qa-footnotes" style="margin-top: 0.75rem; font-size: 0.85rem; opacity: 0.8;">{fn_items}</div>'

    card = f"""<div class="qa-card" id="q{number}">
  <div class="qa-question">
    <a href="#q{number}" class="qa-number-link" title="سوئال {number} گە بىۋاسىتە ئۇلىنىش"><span class="qa-number">{number}</span></a>
    <span class="qa-label">سوئال:</span>
    <span class="qa-text">{question}</span>
    <a href="#q{number}" class="qa-anchor" aria-label="سوئال {number} نىڭ بىۋاسىتە ئۇلىنىشى" title="بىۋاسىتە ئۇلىنىش">#</a>
  </div>
  <div class="qa-answer">
    <span class="qa-label">جاۋاب:</span> {answer}{fn_html}
  </div>
</div>"""
    return card


def main():
    print(f"Reading {JSON_PATH}...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions_by_num = {q["number"]: q for q in data["questions"]}
    print(f"Loaded {len(questions_by_num)} questions.")

    # 99 Names Table
    names_99 = data.get("names_99", [])
    print(f"Loaded {len(names_99)} names from 99 Names list.")

    for page_cfg in PAGES_CONFIG:
        target_dir = page_cfg["dir"]
        target_dir.mkdir(parents=True, exist_ok=True)
        file_path = target_dir / page_cfg["filename"]

        title = page_cfg["title"]
        desc = page_cfg["description"]
        order = page_cfg["order"]

        lines = [
            "---",
            f'title: "{title}"',
            f'description: "{desc}"',
            "sidebar:",
            f'  label: "{title}"',
            f"  order: {order}",
            "---",
            "",
        ]

        for block in page_cfg["blocks"]:
            block_title = block["title"]

            if block.get("is_table"):
                lines.append(f"## {block_title}")
                lines.append("")
                lines.append("| ئەرەبچە نامى | ئۇيغۇرچە ئوقۇلۇشى | مەنىسى |")
                lines.append("| :--- | :--- | :--- |")
                for item in names_99:
                    ar = clean_uyghur(item.get("arabic", ""))
                    ug = clean_uyghur(item.get("transliteration", ""))
                    mn = clean_uyghur(item.get("meaning", ""))
                    lines.append(f"| {ar} | {ug} | {mn} |")
                lines.append("")
                continue

            q_start = block["q_start"]
            q_end = block["q_end"]

            # Markdown block heading with question span
            if q_start == q_end:
                heading_span = f"(سوئال {q_start})"
            else:
                heading_span = f"(سوئال {q_start} – {q_end})"
            lines.append(f"## {block_title} {heading_span}")
            lines.append("")

            for num in range(q_start, q_end + 1):
                if num not in questions_by_num:
                    print(f"ERROR: Missing Q{num}!", file=sys.stderr)
                    sys.exit(1)
                q = questions_by_num[num]
                lines.append(build_card_with_direct_links(q))
                lines.append("")

        content = "\n".join(lines)
        file_path.write_text(content, encoding="utf-8")
        print(f"Generated {page_cfg['filename']} ({len(content)} bytes)")

    print("All MDX files regenerated with direct links and blocks!")


if __name__ == "__main__":
    main()
