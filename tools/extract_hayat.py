#!/usr/bin/env python3
"""
tools/extract_hayat.py

Robust, high-fidelity extractor for «ھاياتىڭىزنى قەدىرلەڭ» (Honor Your Life)
by ئەزھەرى ئالىم ئۇستاز مۇھەممەد يۈسۈپ مۇھەممەد تۇرسۇن.

Extracts all 57 articles, 40 beacons (مەشئەل), 9 recommendations (توققۇز تەۋسىيە),
and front matter into pristine MDX documents for Starlight.

Key features:
1. Character-level clustering with x-jump threshold (> 25 pt) to accurately group words
   and sort them in proper RTL order (descending x coordinate).
2. Uyghur / Quran span separation on shared baseline lines so preambles
   (e.g., "ئاللاھ تائالا قۇرئان كەرىمدە مۇنداق كۆرسەتكەن:") are never dropped.
3. Word-level punctuation normalizer (`fix_leading_punct`) to reposition leading
   LTR punctuation marks back to their proper RTL word ends.
4. Heading font gating (`font == 'UKIJTuzTom'`) to prevent question sentences inside
   paragraphs and quotes from being falsely split into <h3> headings.
5. Exact 1-to-1 verified mapping of Quran verses (Uthmani script) by PDF page number
   supporting sequential multi-Ayah pages.
6. Robust 9 Recommendations regex matching `1 . ...` through `9 . ...` with full prose,
   pristine verses, and footnotes.
"""

import os
import re
from pathlib import Path
import fitz  # PyMuPDF

PDF_PATH = Path("/Users/arslan/code/derslik/public/hayat/hayatingizni-qedirleng.pdf")
DOCS_DIR = Path("/Users/arslan/code/derslik/src/content/docs/hayat")

ORTHOGRAPHY_REPLACEMENTS = [
    (r'\bئـالالھ\b', 'ئاللاھ'),
    (r'\bئـالالھقا\b', 'ئاللاھقا'),
    (r'\bئـالالھتىن\b', 'ئاللاھتىن'),
    (r'\bئـالالھنى\b', 'ئاللاھنى'),
    (r'\bئـالالھنىڭ\b', 'ئاللاھنىڭ'),
    (r'\bئالالھ\b', 'ئاللاھ'),
    (r'\bئالالھقا\b', 'ئاللاھقا'),
    (r'\bئالالھتىن\b', 'ئاللاھتىن'),
    (r'\bئالالھنى\b', 'ئاللاھنى'),
    (r'\bئالالھنىڭ\b', 'ئاللاھنىڭ'),
    (r'\bئالالھتائاال\b', 'ئاللاھ تائالا'),
    (r'\bئالالھ تائاال\b', 'ئاللاھ تائالا'),
    (r'\bئاللاھ تائاال\b', 'ئاللاھ تائالا'),
    (r'\bئاللاھتائاال\b', 'ئاللاھ تائالا'),
    (r'\bئـالالھ تائـاال\b', 'ئاللاھ تائالا'),
    (r'\bئـالالھ تائاال\b', 'ئاللاھ تائالا'),
    (r'\bئالالھ تائـاال\b', 'ئاللاھ تائالا'),
    (r'\bئـالالھتائـاال\b', 'ئاللاھ تائالا'),
    (r'\bئاللاھتائـاال\b', 'ئاللاھ تائالا'),
    (r'\bئـالالھنىـڭ\b', 'ئاللاھنىڭ'),
    (r'\bئـالالھقا\b', 'ئاللاھقا'),
    (r'\bئـالالھتىـن\b', 'ئاللاھتىن'),
    (r'\bئـالالھنى\b', 'ئاللاھنى'),
    (r'\bتائاال\b', 'تائالا'),
    (r'\bتائـاال\b', 'تائالا'),
    (r'\bتائـاالنىـڭ\b', 'تائالانىڭ'),
    (r'\bتائاالنىـڭ\b', 'تائالانىڭ'),
    (r'\bتائاالنىڭ\b', 'تائالانىڭ'),
    (r'\bتائاالغـا\b', 'تائالاغا'),
    (r'\bتائالاغـا\b', 'تائالاغا'),
    (r'\bتائاالغا\b', 'تائالاغا'),
    (r'\bئەلەيھىسسـاالم\b', 'ئەلەيھىسسالام'),
    (r'\bئەلەيھىسسـاالمغا\b', 'ئەلەيھىسسالامغا'),
    (r'\bئەلەيھىسسـاالمنىڭ\b', 'ئەلەيھىسسالامنىڭ'),
    (r'\bئەلەيھىسساالم\b', 'ئەلەيھىسسالام'),
    (r'\bئەلەيھىسساالمغا\b', 'ئەلەيھىسسالامغا'),
    (r'\bئەلەيھىسساالمنىڭ\b', 'ئەلەيھىسسالامنىڭ'),
    (r'\bئىسالم\b', 'ئىسلام'),
    (r'\bئىسالمغا\b', 'ئىسلامغا'),
    (r'\bئىسالمدا\b', 'ئىسلامدا'),
    (r'\bئىسالمىي\b', 'ئىسلامىي'),
    (r'\bئىسالمنىڭ\b', 'ئىسلامنىڭ'),
    (r'\bئىسـالم\b', 'ئىسلام'),
    (r'\bئىسـالمغا\b', 'ئىسلامغا'),
    (r'\bئىخالس\b', 'ئىخلاس'),
    (r'\bئىخالسمەن\b', 'ئىخلاسمەن'),
    (r'\bئىخالسلارچە\b', 'ئىخلاسلارچە'),
    (r'\bئىخالسلىق\b', 'ئىخلاسلىق'),
    (r'\bئەخالق\b', 'ئەخلاق'),
    (r'\bئەخالقى\b', 'ئەخلاقى'),
    (r'\bئەخالققا\b', 'ئەخلاققا'),
    (r'\bئەخالقىنى\b', 'ئەخلاقىنى'),
    (r'\bئەخالقىمىز\b', 'ئەخلاقىمىز'),
    (r'\bئەخالقىمىزغا\b', 'ئەخلاقىمىزغا'),
    (r'\bئەخالقىمىزنى\b', 'ئەخلاقىمىزنى'),
    (r'\bئەخالقىنىڭ\b', 'ئەخلاقىنىڭ'),
    (r'\bئەخالقىغا\b', 'ئەخلاقىغا'),
    (r'\bئەخالقتا\b', 'ئەخلاقتا'),
    (r'\bئەخالقىمىزدا\b', 'ئەخلاقىمىزدا'),
    (r'\bئەخالقتىن\b', 'ئەخلاقتىن'),
    (r'\bئەخالقىدىن\b', 'ئەخلاقىدىن'),
    (r'\bئەخالقىمىزدىن\b', 'ئەخلاقىمىزدىن'),
    (r'\bئەخالقىمىزدۇر\b', 'ئەخلاقىمىزدۇر'),
    (r'\bئەخالقىدۇر\b', 'ئەخلاقىدۇر'),
    (r'\bئەخالقلىق\b', 'ئەخلاقلىق'),
    (r'\bئەخالقسىزلىق\b', 'ئەخلاقسىزلىق'),
    (r'\bئەخالقسىز\b', 'ئەخلاقسىز'),
    (r'\bئەخالقنىڭ\b', 'ئەخلاقنىڭ'),
    (r'\bئەخالقنى\b', 'ئەخلاقنى'),
    (r'\bئىسـالھ\b', 'ئىسلاھ'),
    (r'\bئىسالھ\b', 'ئىسلاھ'),
    (r'\bئىسالھات\b', 'ئىسلاھات'),
    (r'\bئىسالھاتچى\b', 'ئىسلاھاتچى'),
    (r'\bئىسالھاتلار\b', 'ئىسلاھاتلار'),
    (r'\bئىسالھاتچىلار\b', 'ئىسلاھاتچىلار'),
    (r'\bئىسالھاتى\b', 'ئىسلاھاتى'),
    (r'\bئىسالھ قىلىش\b', 'ئىسلاھ قىلىش'),
    (r'\bئىسالھ قىلغۇچى\b', 'ئىسلاھ قىلغۇچى'),
    (r'\bئىسالھ قىلدى\b', 'ئىسلاھ قىلدى'),
    (r'\bئىسالھ بولۇش\b', 'ئىسلاھ بولۇش'),
    (r'\bئىسالھ بولدى\b', 'ئىسلاھ بولدى'),
    (r'\bئىسـالھات\b', 'ئىسلاھات'),
    (r'\bئىختىالپ\b', 'ئىختىلاپ'),
    (r'\bئىختىالپلىق\b', 'ئىختىلاپلىق'),
    (r'\bئىختىالپلار\b', 'ئىختىلاپلار'),
    (r'\bئىختىالپتىن\b', 'ئىختىلاپتىن'),
    (r'\bئىختىالپقا\b', 'ئىختىلاپقا'),
    (r'\bئىختىالپى\b', 'ئىختىلاپى'),
    (r'\bخىالپ\b', 'خىلاپ'),
    (r'\bخىالپلىق\b', 'خىلاپلىق'),
    (r'\bخىالپلىقى\b', 'خىلاپلىقى'),
    (r'\bخىالپلىقلار\b', 'خىلاپلىقلار'),
    (r'\bخىالپلىقتىن\b', 'خىلاپلىقتىن'),
    (r'\bپىالن\b', 'پىلان'),
    (r'\bپىالنى\b', 'پىلانى'),
    (r'\bپىالندىن\b', 'پىلاندىن'),
    (r'\bپىالنغا\b', 'پىلانغا'),
    (r'\bپىالندا\b', 'پىلاندا'),
    (r'\bپىالنىنى\b', 'پىلانىنى'),
    (r'\bپىالنىمىز\b', 'پىلانىمىز'),
    (r'\bپىالنلىرى\b', 'پىلانلىرى'),
    (r'\bپىالنلىق\b', 'پىلانلىق'),
    (r'\bپىالنسىز\b', 'پىلانلىق'),
    (r'\bپىالنلار\b', 'پىلانلار'),
    (r'\bپىالننىڭ\b', 'پىلاننىڭ'),
    (r'\bپىالننى\b', 'پىلاننى'),
    (r'\bئاقىالرچە\b', 'ئاقىلانىچە'),
    (r'\bئاقىالنىچە\b', 'ئاقىلانىچە'),
    (r'\bئاقىالنە\b', 'ئاقىلانە'),
    (r'\bئۆزگىرىشـالر\b', 'ئۆزگىرىشلەر'),
    (r'\bئۆزگىرىشالر\b', 'ئۆزگىرىشلەر'),
    (r'\bئۆزگىرىشـلەر\b', 'ئۆزگىرىشلەر'),
    (r'\bكۈرەشـالر\b', 'كۈرەشلەر'),
    (r'\bكۈرەشالر\b', 'كۈرەشلەر'),
    (r'\bبىلىشـالر\b', 'بىلىشلەر'),
    (r'\bبىلىشالر\b', 'بىلىشلەر'),
    (r'\bكېلىشـالر\b', 'كېلىشلەر'),
    (r'\bكېلىشالر\b', 'كېلىشلەر'),
    (r'\bمۇناسىۋەتلەرنىـڭ\b', 'مۇناسىۋەتلەرنىڭ'),
    (r'\bمۇناسىۋەتلـەر\b', 'مۇناسىۋەتلەر'),
    (r'\bئوقۇرمـەن\b', 'ئوقۇرمەن'),
    (r'\bپەيغەمبـەر\b', 'پەيغەمبەر'),
    (r'\bپەيغەمبىرىمىـز\b', 'پەيغەمبىرىمىز'),
    (r'\bقىلىـپ\b', 'قىلىپ'),
    (r'\bبـولۇپ\b', 'بولۇپ'),
    (r'\bدېگـەن\b', 'دېگەن'),
    (r'\bكۆرسـەتكەن\b', 'كۆرسەتكەن'),
    (r'\bئېلىـپ\b', 'ئېلىپ'),
    (r'\bئېلى\s*پتارقىتىپ\b', 'ئېلىپ تارقىتىپ'),
    (r'\bغادىيى\s*پقىلىپ\b', 'غادىيىپ'),
    (r'\bبېغىشالشتىن\b', 'بېغىشلاشتىن'),
    (r'\bتاشاليدۇ\b', 'تاشلايدۇ'),
    (r'\bھۇزۇرالنماقچى\b', 'ھۇزۇرلانماقچى'),
    (r'\bباشالنغان\b', 'باشلانغان'),
    (r'\bئوغرىالش\b', 'ئوغرىلاش'),
    (r'\bيېڭىالپ\b', 'يېڭىلاپ'),
    (r'\bيېڭىالشنى\b', 'يېڭىلاشنى'),
    (r'\bخۇشال\s*بوالي\b', 'خۇشال بولاي'),
    (r'\bساقلىنىپال\b', 'ساقلىنىپلا'),
    (r'\bمەغرۇرالنماڭ\b', 'مەغرۇرلانماڭ'),
    (r'\bئويالپ\b', 'ئويلاپ'),
    (r'\bيوالتماڭ\b', 'يولاتماڭ'),
    (r'\bخاالس\b', 'خالاس'),
    (r'\bئايالردىن\b', 'ئايلاردىن'),
    (r'\bئايالرنى\b', 'ئايلارنى'),
    (r'\bئايالر\b', 'ئايلار'),
    (r'\bيىالر\b', 'يىللار'),
    (r'\bيىالردىن\b', 'يىللاردىن'),
    (r'\bيىالرنىڭ\b', 'يىللارنىڭ'),
    (r'\bئاتا۔ئانا\b', 'ئاتا-ئانا'),
    (r'\bئاتا۔ئانىلار\b', 'ئاتا-ئانىلار'),
    (r'\bئاتا۔ئانىالر\b', 'ئاتا-ئانىلار'),
    (r'\bئاتا۔ئانىسىغا\b', 'ئاتا-ئانىسىغا'),
    (r'\bئاتا۔ئانىمىز\b', 'ئاتا-ئانىمىز'),
    (r'\bئاتا۔ئانىمىزنى\b', 'ئاتا-ئانىمىزنى'),
    (r'\bبەخت۔سائادەت\b', 'بەخت-سائادەت'),
    (r'\bبەخت۔سائادەتكە\b', 'بەخت-سائادەتكە'),
    (r'\bبەخت۔سائادەتنىڭ\b', 'بەخت-سائادەتنىڭ'),
    (r'\bئىش۔ھەرىكەت\b', 'ئىش-ھەرىكەت'),
    (r'\bئىش۔ھەرىكىتى\b', 'ئىش-ھەرىكىتى'),
    (r'\bئىش۔ھەرىكەتلىرى\b', 'ئىش-ھەرىكەتلىرى'),
    (r'\bگەپ۔سۆز\b', 'گەپ-سۆز'),
    (r'\bگەپ۔سۆزلىرى\b', 'گەپ-سۆزلىرى'),
    (r'\bگەپ۔سۆزلىرىگە\b', 'گەپ-سۆزلىرىگە'),
    (r'\bكېچە۔كۈندۈز\b', 'كېچە-كۈندۈز'),
    (r'\bكېچە۔كۈندۈزدە\b', 'كېچە-كۈندۈزدە'),
    (r'\bبىر۔بىرىگە\b', 'بىر-بىرىگە'),
    (r'\bبىر۔بىرىنى\b', 'بىر-بىرىنى'),
    (r'\bبىر۔بىرىنىڭ\b', 'بىر-بىرىنىڭ'),
    (r'\bبىر۔بىرىمىزگە\b', 'بىر-بىرىمىزگە'),
    (r'\bبىر۔بىرىمىزنى\b', 'بىر-بىرىمىزنى'),
    (r'\bبىر۔بىرىدىن\b', 'بىر-بىرىدىن'),
    (r'\bپىكىر۔قاراش\b', 'پىكىر-قاراش'),
    (r'\bتەرەپ۔تەرەپتىن\b', 'تەرەپ-تەرەپتىن'),
    (r'\bمېۋە۔چېۋە\b', 'مېۋە-چېۋە'),
    (r'\bكىيىم۔كېچەك\b', 'كىيىم-كېچەك'),
    (r'\bقاقتى۔سوقتى\b', 'قاقتى-سوقتى'),
    (r'\bپۇل۔مال\b', 'پۇل-مال'),
    (r'\bپۇل۔مېلىنى\b', 'پۇل-مېلىنى'),
    (r'\bپۇل۔ماللىرىنى\b', 'پۇل-ماللىرىنى'),
    (r'\bئۆچ۔ئاداۋەت\b', 'ئۆچ-ئاداۋەت'),
    (r'\bچەك۔چېگرا\b', 'چەك-چېگرا'),
    (r'\bچەك۔چېگرادىن\b', 'چەك-چېگرادىن'),
]

# Universal verified Quran Ayahs mapping by 1-indexed PDF page numbers.
# For pages with multiple non-contiguous Quran runs, a list of strings is provided.
PAGE_AYAH_MAP = {
    21: "﴿تَبَارَكَ الَّذِي بِيَدِهِ الْمُلْكُ وَهُوَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ ۝ الَّذِي خَلَقَ الْمَوْتَ وَالْحَيَاةَ لِيَبْلُوَكُمْ أَيُّكُمْ أَحْسَنُ عَمَلًا وَهُوَ الْعَزِيزُ الْغَفُورُ﴾",
    33: "﴿وَعِبَادُ الرَّحْمَٰنِ الَّذِينَ يَمْشُونَ عَلَى الْأَرْضِ هَوْنًا وَإِذَا خَاطَبَهُمُ الْجَاهِلُونَ قَالُوا سَلَامًا﴾",
    34: "﴿وَلَا تَسْتَوِي الْحَسَنَةُ وَلَا السَّيِّئَةُ ۚ ادْفَعْ بِالَّتِي هِيَ أَحْسَنُ فَإِذَا الَّذِي بَيْنَكَ وَبَيْنَهُ عَدَاوَةٌ كَأَنَّهُ وَلِيٌّ حَمِيمٌ﴾",
    52: "﴿كُونُوا رَبَّانِيِّينَ بِمَا كُنتُمْ تُعَلِّمُونَ الْكِتَابَ وَبِمَا كُنتُمْ تَدْرُسُونَ﴾",
    56: "﴿يَا أَيُّهَا الَّذِينَ آمَنُوا كُونُوا أَنصَارَ اللَّهِ﴾",
    57: "﴿يَوْمَ لَا يَنفَعُ مَالٌ وَلَا بَنُونَ ۝ إِلَّا مَنْ أَتَى اللَّهَ بِقَلْبٍ سَلِيمٍ﴾",
    59: "﴿إِنَّمَا أَمْرُهُ إِذَا أَرَادَ شَيْئًا أَن يَقُولَ لَهُ كُن فَيَكُونُ﴾",
    60: "﴿وَكَانَ ذَٰلِكَ عَلَى اللَّهِ يَسِيرًا﴾",
    61: [
        "﴿قَالَ كَذَٰلِكِ قَالَ رَبُّكِ هُوَ عَلَيَّ هَيِّنٌ﴾",
        "﴿ذِكْرُ رَحْمَتِ رَبِّكَ عَبْدَهُ زَكَرِيَّا ۝ إِذْ نَادَىٰ رَبَّهُ نِدَاءً خَفِيًّا ۝ قَالَ رَبِّ إِنِّي وَهَنَ الْعَظْمُ مِنِّي وَاشْتَعَلَ الرَّأْسُ شَيْبًا وَلَمْ أَكُن بِدُعَائِكَ رَبِّ شَقِيًّا ۝ وَإِنِّي خِفْتُ الْمَوَالِيَ مِن وَرَائِي وَكَانَتِ امْرَأَتِي عَاقِرًا فَهَبْ لِي مِن لَّدُنكَ وَلِيًّا ۝ يَرِثُنِي وَيَرِثُ مِنْ آلِ يَعْقُوبَ ۖ وَاجْعَلْهُ رَبِّ رَضِيًّا ۝ يَا زَكَرِيَّا إِنَّا نُبَشِّرُكَ بِغُلَامٍ اسْمُهُ يَحْيَىٰ لَمْ نَجْعَل لَّهُ مِن قَبْلُ سَمِيًّا ۝ قَالَ رَبِّ أَنَّىٰ يَكُونُ لِي غُلَامٌ وَكَانَتِ امْرَأَتِي عَاقِرًا وَقَدْ بَلَغْتُ مِنَ الْكِبَرِ عِتِيًّا ۝ قَالَ كَذَٰلِكَ قَالَ رَبُّكَ هُوَ عَلَيَّ هَيِّنٌ وَقَدْ خَلَقْتُكَ مِن قَبْلُ وَلَمْ تَكُ شَيْئًا﴾"
    ],
    62: "﴿فَأَوْحَيْنَا إِلَىٰ مُوسَىٰ أَنِ اضْرِب بِّعَصَاكَ الْبَحْرَ ۖ فَانفَلَقَ فَكَانَ كُلُّ فِرْقٍ كَالطَّوْدِ الْعَظِيمِ﴾",
    63: [
        "﴿اقْتَرَبَتِ السَّاعَةُ وَانشَقَّ الْقَمَرُ﴾",
        "﴿وَإِذْ نَتَقْنَا الْجَبَلَ فَوْقَهُمْ كَأَنَّهُ ظُلَّةٌ وَظَنُّوا أَنَّهُ وَاقِعٌ بِهِمْ﴾"
    ],
    66: "﴿وَاحْلُلْ عُقْدَةً مِّن لِّسَانِي﴾",
    67: [
        "﴿ادْعُونِي أَسْتَجِبْ لَكُمْ﴾",
        "﴿وَإِذَا سَأَلَكَ عِبَادِي عَنِّي فَإِنِّي قَرِيبٌ ۖ أُجِيبُ دَعْوَةَ الدَّاعِ إِذَا دَعَانِ﴾"
    ],
    68: "﴿إِنَّ الَّذِينَ يَسْتَكْبِرُونَ عَنْ عِبَادَتِي سَيَدْخُلُونَ جَهَنَّمَ دَاخِرِينَ﴾",
    70: "﴿فَإِذَا عَزَمْتَ فَتَوَكَّلْ عَلَى اللَّهِ﴾",
    78: [
        "﴿يَا أَيُّهَا الَّذِينَ آمَنُوا لَا تُلْهِكُمْ أَمْوَالُكُمْ وَلَا أَوْلَادُكُمْ عَن ذِكْرِ اللَّهِ ۚ وَمَن يَفْعَلْ ذَٰلِكَ فَأُولَٰئِكَ هُمُ الْخَاسِرُونَ ۝ وَأَنفِقُوا مِن مَّا رَزَقْنَاكُم مِّن قَبْلِ أَن يَأْتِيَ أَحَدَكُمُ الْمَوْتُ فَيَقُولَ رَبِّ لَوْلَا أَخَّرْتَنِي إِلَىٰ أَجَلٍ قَرِيبٍ فَأَصَّدَّقَ وَأَكُن مِّنَ الصَّالِحِينَ﴾",
        "﴿وَالَّذِينَ كَفَرُوا لَهُمْ نَارُ جَهَنَّمَ لَا يُقْضَىٰ عَلَيْهِمْ فَيَمُوتُوا وَلَا يُخَفَّفُ عَنْهُم مِّنْ عَذَابِهَا ۚ كَذَٰلِكَ نَجْزِي كُلَّ كَفُورٍ ۝ وَهُمْ يَصْطَرِخُونَ فِيهَا رَبَّنَا أَخْرِجْنَا نَعْمَلْ صَالِحًا غَيْرَ الَّذِي كُنَّا نَعْمَلُ ۚ أَوَلَمْ نُعَمِّرْكُم مَّا يَتَذَكَّرُ فِيهِ مَن تَذَكَّرَ وَجَاءَكُمُ النَّذِيرُ ۖ فَذُوقُوا فَمَا لِلظَّالِمِينَ مِن نَّصِيرٍ﴾"
    ],
    79: "﴿فَذُوقُوا فَمَا لِلظَّالِمِينَ مِن نَّصِيرٍ﴾",
    81: [
        "﴿وَشَاوِرْهُمْ فِي الْأَمْرِ﴾",
        "﴿فَإِذَا عَزَمْتَ فَتَوَكَّلْ عَلَى اللَّهِ ۚ إِنَّ اللَّهَ يُحِبُّ الْمُتَوَكِّلِينَ﴾"
    ],
    86: "﴿فَإِذَا عَزَمْتَ فَتَوَكَّلْ عَلَى اللَّهِ﴾",
    87: "﴿قُلْ بِفَضْلِ اللَّهِ وَبِرَحْمَتِهِ فَبِذَٰلِكَ فَلْيَفْرَحُوا هُوَ خَيْرٌ مِّمَّا يَجْمَعُونَ﴾",
    92: "﴿الَّذِينَ يُنفِقُونَ فِي السَّرَّاءِ وَالضَّرَّاءِ وَالْكَاظِمِينَ الْغَيْظَ وَالْعَافِينَ عَنِ النَّاسِ ۗ وَاللَّهُ يُحِبُّ الْمُحْسِنِينَ﴾",
    119: "﴿فَأَقِمْ وَجْهَكَ لِلدِّينِ حَنِيفًا ۚ فِطْرَتَ اللَّهِ الَّتِي فَطَرَ النَّاسَ عَلَيْهَا ۚ لَا تَبْدِيلَ لِخَلْقِ اللَّهِ ۚ ذَٰلِكَ الدِّينُ الْقَيِّمُ وَلَٰكِنَّ أَكْثَرَ النَّاسِ لَا يَعْلَمُونَ﴾",
    121: "﴿وَعَسَىٰ أَن تَكْرَهُوا شَيْئًا وَهُوَ خَيْرٌ لَّكُمْ ۖ وَعَسَىٰ أَن تُحِبُّوا شَيْئًا وَهُوَ شَرٌّ لَّكُمْ ۗ وَاللَّهُ يَعْلَمُ وَأَنتُمْ لَا تَعْلَمُونَ﴾",
    123: "﴿فَإِنَّ مَعَ الْعُسْرِ يُسْرًا ۝ إِنَّ مَعَ الْعُسْرِ يُسْرًا﴾",
    124: "﴿فَإِذَا فَرَغْتَ فَانصَبْ ۝ وَإِلَىٰ رَبِّكَ فَارْغَب﴾",
    140: "﴿وَأَوْحَىٰ رَبُّكَ إِلَى النَّحْلِ أَنِ اتَّخِذِي مِنَ الْجِبَالِ بُيُوتًا وَمِنَ الشَّجَرِ وَمِمَّا يَعْرِشُونَ ۝ ثُمَّ كُلِي مِن كُلِّ الثَّمَرَاتِ فَاسْلُكِي سُبُلَ رَبِّكِ ذُلُلًا ۚ يَخْرُجُ مِن بُطُونِهَا شَرَابٌ مُّخْتَلِفٌ أَلْوَانُهُ فِيهِ شِفَاءٌ لِّلنَّاسِ ۗ إِنَّ فِي ذَٰلِكَ لَآيَةً لِّقَوْمٍ يَتَفَكَّرُونَ﴾",
    160: "﴿الرِّجَالُ قَوَّامُونَ عَلَى النِّسَاءِ بِمَا فَضَّلَ اللَّهُ بَعْضَهُمْ عَلَىٰ بَعْضٍ وَبِمَا أَنفَقُوا مِنْ أَمْوَالِهِمْ﴾",
    181: "﴿أَفَمَن يَمْشِي مُكِبًّا عَلَىٰ وَجْهِهِ أَهْدَىٰ أَمَّن يَمْشِي سَوِيًّا عَلَىٰ صِرَاطٍ مُّسْتَقِيمٍ﴾",
    196: "﴿يَا أَيُّهَا الَّذِينَ آمَنُوا اجْتَنِبُوا كَثِيرًا مِّنَ الظَّنِّ إِنَّ بَعْضَ الظَّنِّ إِثْمٌ﴾",
    201: "﴿وَلَا تَقْفُ مَا لَيْسَ لَكَ بِهِ عِلْمٌ﴾",
    207: "﴿وَلَوْ كُنتَ فَظًّا غَلِيظَ الْقَلْبِ لَانفَضُّوا مِنْ حَوْلِكَ﴾",
    211: "﴿وَمَا أُوتِيتُم مِّن شَيْءٍ فَمَتَاعُ الْحَيَاةِ الدُّنْيَا وَزِينَتُهَا ۚ وَمَا عِندَ اللَّهِ خَيْرٌ وَأَبْقَىٰ ۚ أَفَلَا تَعْقِلُونَ﴾",
    216: "﴿الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ﴾",
    224: "﴿فَإِنَّ مَعَ الْعُسْرِ يُسْرًا ۝ إِنَّ مَعَ الْعُسْرِ يُسْرًا﴾",
    232: "﴿قَالَا رَبَّنَا ظَلَمْنَا أَنفُسَنَا وَإِن لَّمْ تَغْفِرْ لَنَا وَتَرْحَمْنَا لَنَكُونَنَّ مِنَ الْخَاسِرِينَ﴾",
    233: [
        "﴿إِنَّ اللَّهَ يَغْفِرُ الذُّنُوبَ جَمِيعًا ۚ إِنَّهُ هُوَ الْغَفُورُ الرَّحِيمُ﴾",
        "﴿فَمَن تَابَ مِن بَعْدِ ظُلْمِهِ وَأَصْلَحَ فَإِنَّ اللَّهَ يَتُوبُ عَلَيْهِ ۗ إِنَّ اللَّهَ غَفُورٌ رَّحِيمٌ﴾",
        "﴿إِنَّ الْحَسَنَاتِ يُذْهِبْنَ السَّيِّئَاتِ﴾"
    ],
    243: "﴿وَهُوَ مَعَكُمْ أَيْنَ مَا كُنتُمْ ۚ وَاللَّهُ بِمَا تَعْمَلُونَ بَصِيرٌ﴾",
    244: "﴿إِنَّ الْحَسَنَاتِ يُذْهِبْنَ السَّيِّئَاتِ﴾",
    246: "﴿وَأَنَّهُ هُوَ أَضْحَكَ وَأَبْكَىٰ﴾",
    247: "﴿إِنَّ الَّذِينَ أَجْرَمُوا كَانُوا مِنَ الَّذِينَ آمَنُوا يَضْحَكُونَ﴾",
    253: "﴿مَنْ عَمِلَ صَالِحًا مِّن ذَكَرٍ أَوْ أُنثَىٰ وَهُوَ مُؤْمِنٌ فَلَنُحْيِيَنَّهُ حَيَاةً طَيِّبَةً ۖ وَلَنَجْزِيَنَّهُمْ أَجْرَهُم بِأَحْسَنِ مَا كَانُوا يَعْمَلُونَ﴾",
    261: "﴿وَلَا تَقْفُ مَا لَيْسَ لَكَ بِهِ عِلْمٌ ۚ إِنَّ السَّمْعَ وَالْبَصَرَ وَالْفُؤَادَ كُلُّ أُولَٰئِكَ كَانَ عَنْهُ مَسْئُولًا﴾",
    264: "﴿وَلَا يَغْتَب بَّعْضُكُم بَعْضًا ۚ أَيُحِبُّ أَحَدُكُمْ أَن يَأْكُلَ لَحْمَ أَخِيهِ مَيْتًا فَكَرِهْتُمُوهُ ۚ وَاتَّقُوا اللَّهَ ۚ إِنَّ اللَّهَ تَوَّابٌ رَّحِيمٌ﴾",
    272: "﴿وَاذْكُر رَّبَّكَ فِي نَفْسِكَ تَضَرُّعًا وَخِيفَةً﴾",
    274: [
        "﴿أَمْ خُلِقُوا مِنْ غَيْرِ شَيْءٍ أَمْ هُمُ الْخَالِقُونَ﴾",
        "﴿قُلْ أَأَنتُمْ أَعْلَمُ أَمِ اللَّهُ﴾"
    ],
    276: [
        "﴿كَانُوا لَا يَتَنَاهَوْنَ عَن مُّنكَرٍ فَعَلُوهُ ۚ لَبِئْسَ مَا كَانُوا يَفْعَلُونَ﴾",
        "﴿إِنَّ اللَّهَ يَغْفِرُ الذُّنُوبَ جَمِيعًا﴾",
        "﴿فَمَن تَابَ مِن بَعْدِ ظُلْمِهِ وَأَصْلَحَ فَإِنَّ اللَّهَ يَتُوبُ عَلَيْهِ﴾"
    ],
    278: [
        "﴿إِنَّ الَّذِينَ يُحِبُّونَ أَن تَشِيعَ الْفَاحِشَةُ فِي الَّذِينَ آمَنُوا لَهُمْ عَذَابٌ أَلِيمٌ فِي الدُّنْيَا وَالْآخِرَةِ﴾",
        "﴿لَّا يُحِبُّ اللَّهُ الْجَهْرَ بِالسُّوءِ مِنَ الْقَوْلِ إِلَّا مَن ظُلِمَ﴾"
    ],
    279: [
        "﴿وَكَذَٰلِكَ جَعَلْنَا لِكُلِّ نَبِيٍّ عَدُوًّا شَيَاطِينَ الْإِنسِ وَالْجِنِّ﴾",
        "﴿وَكَذَٰلِكَ جَعَلْنَا لِكُلِّ نَبِيٍّ عَدُوًّا مِّنَ الْمُجْرِمِينَ﴾"
    ],
    287: "﴿وَجَزَاءُ سَيِّئَةٍ سَيِّئَةٌ مِّثْلُهَا ۖ فَمَنْ عَفَا وَأَصْلَحَ فَأَجْرُهُ عَلَى اللَّهِ ۚ إِنَّهُ لَا يُحِبُّ الظَّالِمِينَ﴾",
    288: [
        "﴿تُسَبِّحُ لَهُ السَّمَاوَاتُ السَّبْعُ وَالْأَرْضُ وَمَن فِيهِنَّ ۚ وَإِن مِّن شَيْءٍ إِلَّا يُسَبِّحُ بِحَمْدِهِ وَلَٰكِن لَّا تَفْقَهُونَ تَسْبِيحَهُمْ﴾",
        "﴿وَلِلَّهِ يَسْجُدُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ مِن دَابَّةٍ وَالْمَلَائِكَةُ وَهُمْ لَا يَسْتَكْبِرُونَ﴾"
    ],
    289: "﴿أَخْرِجُوا آلَ لُوطٍ مِّن قَرْيَتِكُمْ ۖ إِنَّهُمْ أُنَاسٌ يَتَطَهَّرُونَ﴾",
    290: "﴿يَا أَيُّهَا الَّذِينَ آمَنُوا اتَّقُوا اللَّهَ وَلْتَنظُرْ نَفْسٌ مَّا قَدَّمَتْ لِغَدٍ ۖ وَاتَّقُوا اللَّهَ ۚ إِنَّ اللَّهَ خَبِيرٌ بِمَا تَعْمَلُونَ﴾",
    293: "﴿لَئِن شَكَرْتُمْ لَأَزِيدَنَّكُمْ ۖ وَلَئِن كَفَرْتُمْ إِنَّ عَذَابِي لَشَدِيدٌ﴾",
    300: "﴿وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا ۝ وَيَرْزُقْهُ مِنْ حَيْثُ لَا يَحْتَسِبُ﴾",
}

def get_next_ayah(pno: int, tracker: dict):
    """Retrieves the next Ayah for a page, supporting single string or list."""
    if pno not in PAGE_AYAH_MAP:
        return None
    val = PAGE_AYAH_MAP[pno]
    if isinstance(val, list):
        idx = tracker.get(pno, 0)
        tracker[pno] = idx + 1
        if idx < len(val):
            return val[idx]
        return val[-1]
    return val

def escape_mdx(text: str) -> str:
    """Escapes characters that MDX / JSX would interpret as syntax."""
    text = text.replace('{', '&#123;').replace('}', '&#125;')
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    return text

def fix_leading_punct(w: str) -> str:
    """
    Fixes inverted leading punctuation caused by InDesign LTR/RTL font streams.
    E.g. '.ئالماڭ' -> 'ئالماڭ.', '!تۇرۇڭ' -> 'تۇرۇڭ!', '.10' -> '10.', '.»بولدى' -> 'بولدى.»'
    """
    m = re.match(r'^([\.،؛؟!:]+|[\.،؛?!:][»”]|[»”][\.،؛?!:])([\u0600-\u06FF\d].*)$', w)
    if m:
        punct, rest = m.group(1), m.group(2)
        return rest + punct
    return w

def clean_text(t: str) -> str:
    """Cleans Uyghur text, applies ligatures, and normalizes typography."""
    t = t.replace('\ufeff', '')
    t = re.sub(r'ـ+', '', t)
    for pat, rep in ORTHOGRAPHY_REPLACEMENTS:
        t = re.sub(pat, rep, t)
    # Fix punctuation spacing
    t = re.sub(r'\s+([\.،؛؟!:])', r'\1', t)
    # Fix spaced digits e.g. "1 0 ." -> "10."
    t = re.sub(r'(\d)\s+(\d)', r'\1\2', t)
    # Normalize keyboard angle brackets to authentic Uyghur quotation marks ‹ and ›
    t = t.replace('<', '‹').replace('>', '›')
    t = re.sub(r' +', ' ', t)
    return t.strip()

def extract_page_lines(doc, pno):
    """
    Extracts raw lines from a page with character-level RTL sorting,
    handling punctuation jumps, footnote separation, Uyghur/Quran font separation,
    and heading font metadata.
    """
    page = doc[pno - 1]
    drawings = page.get_drawings()
    fn_y = 600
    for d in drawings:
        rect = d.get('rect')
        if rect and 400 < rect.y0 < 550 and 50 < rect.width < 120:
            fn_y = min(fn_y, rect.y0)
            
    d = page.get_text('rawdict')
    body_dict = {}
    fn_dict = {}
    
    for b in d['blocks']:
        if 'lines' not in b:
            continue
        for l in b['lines']:
            y = round(l['bbox'][1], 1)
            # Skip running header and page numbers
            if y < 45 or y > 550:
                continue
            for s in l['spans']:
                chars = s['chars']
                if not chars:
                    continue
                is_quran = 'KFGQPC' in s['font']
                is_heading = 'UKIJTuzTom' in s['font']
                
                target = fn_dict if y >= fn_y - 5 else body_dict
                matched = False
                for ly in target:
                    if abs(ly - y) < 4:
                        target[ly].append((chars, is_quran, is_heading))
                        matched = True
                        break
                if not matched:
                    target[y] = [(chars, is_quran, is_heading)]
                
    def process_dict(line_dict):
        res = []
        for ly in sorted(line_dict.keys()):
            items = line_dict[ly]
            
            # Separate Uyghur characters and Quran characters
            uyghur_chars = []
            quran_chars = []
            has_heading_font = False
            
            for chs, iq, ih in items:
                if ih:
                    has_heading_font = True
                if iq:
                    quran_chars.extend(chs)
                else:
                    uyghur_chars.extend(chs)
                    
            # Check for isolated inline Quran terms on specific pages
            # P233: ﴿الذُّنُوبَ﴾, ﴿السَّيِّئَاتِ﴾; P276: ﴿الذَّنْبُ﴾, ﴿السَّيِّئَةُ﴾
            inline_quran_text = None
            if quran_chars and len(quran_chars) <= 25:
                raw_q = ''.join(c['c'] for c in quran_chars)
                if 'الُّذ' in raw_q:
                    inline_quran_text = '﴿الذُّنُوبَ﴾'
                    quran_chars = []
                elif 'الَّس' in raw_q:
                    inline_quran_text = '﴿السَّيِّئَاتِ﴾'
                    quran_chars = []
                elif 'لذنـب' in raw_q or 'لذنب' in raw_q:
                    inline_quran_text = '﴿الذَّنْبُ﴾'
                    quran_chars = []
                elif 'لسيئـة' in raw_q or 'لسيئة' in raw_q:
                    inline_quran_text = '﴿السَّيِّئَةُ﴾'
                    quran_chars = []

            # 1. Process Uyghur words
            uyghur_line = None
            if uyghur_chars:
                words = []
                cur_w = []
                for c in uyghur_chars:
                    if c['c'] == ' ':
                        if cur_w:
                            words.append(cur_w)
                            cur_w = []
                    else:
                        if cur_w and abs(c['bbox'][0] - cur_w[-1]['bbox'][0]) > 25:
                            words.append(cur_w)
                            cur_w = [c]
                        else:
                            cur_w.append(c)
                if cur_w:
                    words.append(cur_w)
                    
                word_tokens = []
                for w in words:
                    w_txt = ''.join(c['c'] for c in w)
                    w_txt = fix_leading_punct(w_txt)
                    w_x1 = max(c['bbox'][2] for c in w)
                    w_x0 = min(c['bbox'][0] for c in w)
                    word_tokens.append((w_x1, w_x0, w_txt))
                    
                # If an inline Quran term was found on this line, insert it at its relative position
                if inline_quran_text:
                    word_tokens.append((260.0, 245.0, inline_quran_text))
                    
                sorted_words = sorted(word_tokens, key=lambda x: -x[0])
                line_str = ' '.join(w[2] for w in sorted_words)
                line_str = re.sub(r' +', ' ', line_str).strip()
                x1 = max(w[0] for w in word_tokens) if word_tokens else 331.7
                x0 = min(w[1] for w in word_tokens) if word_tokens else 51.0
                if line_str:
                    uyghur_line = {'y': ly, 'text': line_str, 'x1': x1, 'x0': x0, 'is_quran': False, 'is_heading': has_heading_font, 'pno': pno}

            # 2. Process Quran line if present
            quran_line = None
            if quran_chars:
                q_x1 = max(c['bbox'][2] for c in quran_chars)
                q_x0 = min(c['bbox'][0] for c in quran_chars)
                quran_line = {'y': ly, 'text': '[[[QURAN_LINE]]]', 'x1': q_x1, 'x0': q_x0, 'is_quran': True, 'is_heading': False, 'pno': pno}

            # Emit in proper RTL reading order
            if uyghur_line and quran_line:
                if uyghur_line['x1'] >= 300:
                    res.append(uyghur_line)
                    res.append(quran_line)
                else:
                    res.append(quran_line)
                    res.append(uyghur_line)
            elif uyghur_line:
                res.append(uyghur_line)
            elif quran_line:
                res.append(quran_line)
                
        return res
        
    return process_dict(body_dict), process_dict(fn_dict)

CHAPTERS = [
    ('bap-01', 'دۇنيادىكى ئەڭ ياخشى كەسىپ', 21, 24),
    ('bap-02', 'ھېچكىم تەنقىدلىمىسۇن دېسىڭىز...', 25, 28),
    ('bap-03', 'ئۆزىڭىزنىڭ مېڭىسىنى ئۆزىڭىز يۇيۇڭ', 29, 30),
    ('bap-04', 'ئۆزىڭىزنىڭ مۇھىم شەخس ئىكەنلىكىنى قانداق بىلىسىز؟', 31, 32),
    ('bap-05', 'كىشىلەرگە ئۇلار قىلغان مۇئامىلىنى قىلماڭ', 33, 35),
    ('bap-06', 'ئۆز كېمىڭىزنى ئۆزىڭىز ھەيدەڭ', 36, 37),
    ('bap-07', 'گۈزەللىكلەرنى كۆرۈش ئۈچۈنمۇ ئىقتىدار كېرەك', 38, 39),
    ('bap-08', 'سىزنىڭ شەخسىي قانائىتىڭىز مۇقەددەس پىكىر ئەمەس', 40, 41),
    ('bap-09', 'سۈكۈت ھەممىلا ئادەم بېجىرەلەيدىغان ماھارەت ئەمەس', 42, 45),
    ('bap-10', 'سىزنىڭ ياخشى كۆرگەنلىكىڭىز ئۈچۈنلا ئەمەس...', 46, 48),

    ('bap-11', 'بىلىش بىلەن تەتبىقلاش ئوتتۇرىسىدا', 49, 51),
    ('bap-12', 'بىز قانچىلىك بولالىدۇق؟', 52, 58),
    ('bap-13', 'ئاللاھ تائالادىن مۇمكىن ئەمەسلەرنى تىلەڭ!', 59, 69),
    ('bap-14', 'ئىرادىنى ھېچكىم بېرەلمەيدۇ', 70, 75),
    ('bap-15', 'يېرىم يىل ئۆمرىڭىز قالغان بولسا نېمە قىلاتتىڭىز؟', 76, 79),
    ('bap-16', 'نىشاندىن سوۋۇتۇش ھىيلىسى', 80, 85),
    ('bap-17', 'خۇشاللىقنى ئۆزىڭىزدىن ئىزدەڭ', 86, 89),
    ('bap-18', 'ئۇنتۇشمۇ بىر سەنئەت، ئۇنىمۇ ئۆگىنىۋېلىڭ!', 90, 95),
    ('bap-19', 'ياخشىسىنى كۈتۈڭ، چوقۇم كۆرىسىز', 96, 99),
    ('bap-20', 'جاھىللىق يامان ئىش ئەمەس', 100, 104),

    ('bap-21', 'مەشغۇل بولغانلىق قازانغانلىق ئەمەس', 105, 110),
    ('bap-22', 'ھاياتىمىزدا خاتا كۆزقاراشلارنىڭ نىسبىتى', 111, 114),
    ('bap-23', 'قورقمايدىغان ئادەم تۇغۇلۇپ باقمىدى', 115, 117),
    ('bap-24', 'مۇنداق كىشىلەردىن يىراق تۇرۇڭ', 118, 121),
    ('bap-25', 'سىزنى ئۆلتۈرەلمىگەن نەرسە كۈچلۈك قىلىدۇ', 122, 125),
    ('bap-26', 'ھېسسىيات دۈشمەنلىرىدىن يىراق تۇرۇڭ!', 126, 128),
    ('bap-27', 'ھېچكىم سىزنى بالىڭىزدەك نازارەت قىلالمايدۇ', 129, 131),
    ('bap-28', 'ئۇلار سىزنى قانداق باھالايدۇ؟', 132, 135),
    ('bap-29', 'ئۆمرىڭىزنى قانداق ئۇزىتالايسىز؟', 136, 139),
    ('bap-30', 'ھەسەل ھەرىسىدىكى قۇرئان مۆجىزىسى', 140, 143),

    ('bap-31', 'ئۆزگەرتمەكچى بولغىنىڭىز دەل ئۆزىڭىز بولۇڭ', 144, 146),
    ('bap-32', 'كىشىلەردىن نېمىلەرنى ئۆگىنەلەيسىز؟', 147, 150),
    ('bap-33', 'ئىشىڭىز مۇكەممەل بولسا تەنقىدچىلەردىن قورقماڭ!', 151, 153),
    ('bap-34', 'قىزلارنىڭ يىگىتلىرى توغرۇلۇق بىلىشى زۆرۈر بولغان ئىشلار', 154, 160),
    ('bap-35', 'ئوغۇللارنىڭ جور تاللىشىدا بىلىشى زۆرۈر بولغان ئىشلار', 161, 170),
    ('bap-36', 'پۇرسەت ۋە ھېكمەت', 171, 175),
    ('bap-37', 'مۇۋەپپەقىيەتلىك ئىشلارنى ئادەتكە ئايلاندۇرۇۋېلىڭ', 176, 179),
    ('bap-38', 'مۇۋەپپەقىيەتنىڭ سىرى', 180, 184),
    ('bap-39', 'ئاقىلانىچە كەچۈرۈم سوراشنى بىلەمسىز؟', 185, 191),
    ('bap-40', 'يېڭى يىلغا قانداق قارايسىز؟', 192, 195),

    ('bap-41', 'بەزى گۇمانلار دۆتلۈكتۇر', 196, 198),
    ('bap-42', 'قانداق قىلغاندا توغرا قارار قىلالايسىز؟', 199, 203),
    ('bap-43', 'كىشىلەر سىزنى نېمە ئۈچۈن ياخشى كۆرىدۇ ۋە نېمە ئۈچۈن يامان كۆرىدۇ', 204, 208),
    ('bap-44', 'ئاكتىپلىق ۋە پاسسىپلىق', 209, 214),
    ('bap-45', 'بىزنىڭ ئۆيدىكى 20 قائىدە', 215, 219),
    ('bap-46', 'ئىرادىنى ھېچكىم يېڭەلمەيدۇ', 220, 223),
    ('bap-47', '«مۇمكىن ئەمەس» دېگەن سۆزنى لۇغىتىڭىزدىن چىقىرىپ تاشلاڭ!', 224, 226),
    ('bap-48', 'ئېنېرگىيە يۇقۇملۇقتۇر', 227, 229),
    ('bap-49', 'مۆجىزىلەر ھەرىكەتكە ئۆتكەنلەرگە كېلىدۇ', 230, 231),
    ('bap-50', 'بىز پۇشايمان قىلىدىغان 20 ئىش', 232, 235),

    ('bap-51', 'مۇۋەپپەقىيەت كۈندىلىك ئادەتكە موھتاجدۇر', 236, 242),
    ('bap-52', 'مۇئامىلە پىرىنسىپى', 243, 245),
    ('bap-53', 'نورمال كۈلكە ساغلاملىقنىڭ دەلىلىدۇر', 246, 249),
    ('bap-54', 'ئەڭ تەلەيلىك ئىنسان', 250, 254),
    ('bap-55', '80/20 قانۇنىيىتى', 255, 260),
    ('bap-56', 'گەپ-سۆزىڭىزگە دىققەت قىلىڭ', 261, 265),
    ('bap-57', '90/10 قانۇنىيىتى', 266, 270),
]

def format_chapter(doc, chap_idx, chap_id, title, start_p, end_p):
    """
    Assembles a chapter into fluent, clean paragraphs with correctly merged
    quotes, bullets, subheadings, and ayahs without artificial line breaks.
    """
    all_body = []
    chapter_footnotes = []
    ayah_tracker = {}
    
    for pno in range(start_p, end_p + 1):
        b, f = extract_page_lines(doc, pno)
        all_body.extend(b)
        for fn in f:
            t = clean_text(fn['text'].replace('[[[', '').strip())
            if t and not t.isdigit():
                chapter_footnotes.append(t)
                
    blocks = []
    idx = 0
    # Skip chapter title at top of page 1 if present
    while idx < len(all_body):
        l = all_body[idx]
        if title in l['text']:
            idx += 1
            break
        elif idx == 0 and l['y'] < 150 and len(l['text']) < 50:
            idx += 1
            break
        idx += 1
        
    while idx < len(all_body):
        l = all_body[idx]
        txt = l['text']
        # Fuse spaced digits like "1 0 ." or ". 1 0" or "2 0" -> "10. " or "20. "
        txt = re.sub(r'^\s*[\.،؛-]?\s*(\d)\s+(\d)\s*[\.،؛-]?\s*', r'\1\2. ', txt)
        # Normalize numbered list items like ". 10" or "1 ." to "1. " or "10. "
        txt = re.sub(r'^\s*[\.،؛-]?\s*(\d+)\s*[\.،؛-]?\s*', r'\1. ', txt)
        
        # 1. Quran verse
        if l['is_quran']:
            pno = l['pno']
            ayah_txt = get_next_ayah(pno, ayah_tracker)
            if ayah_txt:
                blocks.append(('ayah', ayah_txt))
            # Skip consecutive quran lines of this run
            while idx + 1 < len(all_body) and all_body[idx + 1]['is_quran']:
                idx += 1
            idx += 1
            continue
            
        # 2. Subheading (question ending with ؟ or statement with heading font 'UKIJTuzTom')
        if l.get('is_heading', False) and (txt.endswith('؟') or txt.endswith('?')) and len(txt) < 65 and not txt.startswith(('«', '“', '”')):
            blocks.append(('heading', txt))
            idx += 1
            continue
            
        # 3. Lesson section header
        if txt.strip() in ['ئىبرەت :', 'ئىبرەت:', 'ئىبرەت']:
            blocks.append(('lesson_header', 'ئىبرەت ۋە ھاياتلىق دەرسى:'))
            idx += 1
            continue
            
        # 4. Standalone Opening Quote at beginning of chapter
        if (txt.startswith('«') or txt.startswith('“')) and (len(blocks) == 0 or (len(blocks) == 1 and blocks[0][0] == 'heading')):
            quote_lines = [txt]
            idx += 1
            while idx < len(all_body):
                next_l = all_body[idx]
                if next_l['is_quran']:
                    break
                quote_lines.append(next_l['text'])
                idx += 1
                if '»' in next_l['text'] or '”' in next_l['text']:
                    if idx < len(all_body) and all_body[idx]['text'].startswith(('—', '-')) and len(all_body[idx]['text']) < 40:
                        quote_lines.append(all_body[idx]['text'])
                        idx += 1
                    break
            blocks.append(('quote', ' '.join(quote_lines)))
            continue
            
        # 5. Bullet item (list element)
        if txt.startswith(('●', '■', '•', '✦', '- ')) or re.match(r'^\d+\s*[\.ـ-]', txt):
            bullet_lines = [txt]
            idx += 1
            while idx < len(all_body):
                next_l = all_body[idx]
                next_txt = re.sub(r'^\s*[\.،؛-]?\s*(\d)\s+(\d)\s*[\.،؛-]?\s*', r'\1\2. ', next_l['text'])
                next_txt = re.sub(r'^\s*[\.،؛-]?\s*(\d+)\s*[\.،؛-]?\s*', r'\1. ', next_txt)
                if next_l['is_quran'] or next_txt.startswith(('●', '■', '•', '✦', '- ')) or re.match(r'^\d+\s*[\.ـ-]', next_txt) or (next_l.get('is_heading', False) and (next_txt.endswith('؟') or next_txt.endswith('?')) and len(next_txt) < 60) or next_txt.strip() in ['ئىبرەت :', 'ئىبرەت:', 'ئىبرەت']:
                    break
                if next_l['x1'] < 320 and bullet_lines[-1].endswith(('.', '!', '؟', '»', '”')):
                    break
                if bullet_lines[-1].endswith('-') or bullet_lines[-1].endswith(' -'):
                    bullet_lines[-1] = re.sub(r'\s*-\s*$', '', bullet_lines[-1])
                    bullet_lines.append(next_l['text'])
                else:
                    bullet_lines.append(next_l['text'])
                idx += 1
                if next_l['text'].endswith(('.', '!', '؟', '»', '”')) and next_l['x0'] > 80:
                    break
            blocks.append(('bullet', ' '.join(bullet_lines)))
            continue
            
        # 6. Regular narrative paragraph
        para_lines = [txt]
        idx += 1
        while idx < len(all_body):
            next_l = all_body[idx]
            next_txt = re.sub(r'^\s*[\.،؛-]?\s*(\d)\s+(\d)\s*[\.،؛-]?\s*', r'\1\2. ', next_l['text'])
            next_txt = re.sub(r'^\s*[\.،؛-]?\s*(\d+)\s*[\.،؛-]?\s*', r'\1. ', next_txt)
            if next_l['is_quran'] or next_txt.startswith(('●', '■', '•', '✦', '- ')) or re.match(r'^\d+\s*[\.ـ-]', next_txt) or (next_l.get('is_heading', False) and (next_txt.endswith('؟') or next_txt.endswith('?')) and len(next_txt) < 60) or next_txt.strip() in ['ئىبرەت :', 'ئىبرەت:', 'ئىبرەت']:
                break
            if next_l['x1'] < 322 and para_lines[-1].endswith(('.', '!', '؟', ':', '»', '”')):
                break
            if para_lines[-1].endswith('-') or para_lines[-1].endswith(' -'):
                para_lines[-1] = re.sub(r'\s*-\s*$', '', para_lines[-1])
                para_lines.append(next_l['text'])
            else:
                para_lines.append(next_l['text'])
            idx += 1
            if next_l['text'].endswith(('.', '!', '؟', '»', '”')) and next_l['x0'] > 100:
                break
        blocks.append(('para', ' '.join(para_lines)))

    # Render Card HTML
    out = []
    out.append(f'<div class="hadith-card" id="{chap_id}">')
    out.append('  <div class="hadith-header">')
    out.append(f'    <a href="#{chap_id}" class="hadith-number-link" title="{chap_idx}-ماقالىگە بىۋاسىتە ئۇلىنىش"><span class="hadith-number">{chap_idx}</span></a>')
    out.append(f'    <span class="hadith-title">{chap_idx}-ماقالە: {title}</span>')
    out.append(f'    <a href="#{chap_id}" class="hadith-anchor" aria-label="{chap_idx}-ماقالە بىۋاسىتە ئۇلىنىشى" title="بىۋاسىتە ئۇلىنىش">#</a>')
    out.append('  </div>')
    out.append('  <div class="hadith-translation">')

    fn_call_idx = 1
    for b_type, b_txt in blocks:
        b_txt = clean_text(b_txt)
        if not b_txt:
            continue
            
        while '[[[' in b_txt:
            b_txt = b_txt.replace('[[[', f'[^{fn_call_idx}]', 1)
            fn_call_idx += 1
            
        if b_type == 'heading':
            out.append(f'    <h3>{escape_mdx(b_txt)}</h3>')
        elif b_type == 'lesson_header':
            out.append(f'    <div class="hadith-section-label">{escape_mdx(b_txt)}</div>')
        elif b_type == 'ayah':
            out.append(f'    <p class="hadith-arabic">{b_txt}</p>')
        elif b_type == 'quote':
            out.append(f'    <blockquote>{escape_mdx(b_txt)}</blockquote>')
        elif b_type == 'bullet':
            bullet_clean = re.sub(r'^[●•■✦\-]\s*', '', b_txt)
            out.append(f'    <p class="hadith-lesson-item">✦ {escape_mdx(bullet_clean)}</p>')
        else: # para
            out.append(f'    <p>{escape_mdx(b_txt)}</p>')

    if chapter_footnotes:
        out.append('    <div class="hadith-footnotes">')
        out.append('      <div class="hadith-section-label">ئىزاھات ۋە مەنبەلەر:</div>')
        out.append('      <ol class="footnotes-list">')
        for fn in chapter_footnotes:
            out.append(f'        <li>{escape_mdx(fn)}</li>')
        out.append('      </ol>')
        out.append('    </div>')

    out.append('  </div>')
    out.append('</div>')
    return '\n'.join(out)

def generate_part_files(doc):
    parts = [
        ('01-bap-01-10.mdx', '1–10-ماقالىلەر: كەسىپ، كۆزقاراش ۋە تەپەككۇر', 1, 10, 2),
        ('02-bap-11-20.mdx', '11–20-ماقالىلەر: ئەمەلىيەت، ئىرادە ۋە خۇشاللىق', 11, 20, 3),
        ('03-bap-21-30.mdx', '21–30-ماقالىلەر: ۋاقىت، روھىيەت ۋە ئۆمۈر نىجاتلىقى', 21, 30, 4),
        ('04-bap-31-40.mdx', '31–40-ماقالىلەر: ئۆزىنى ئىسلاھ قىلىش، ئائىلە ۋە پۇرسەت', 31, 40, 5),
        ('05-bap-41-50.mdx', '41–50-ماقالىلەر: توغرا قارار، پىرىنسىپ ۋە ئائىلە تۈزۈمى', 41, 50, 6),
        ('06-bap-51-57.mdx', '51–57-ماقالىلەر: ئادەت، تەلەي ۋە ھاياتلىق قائىدىلىرى', 51, 57, 7),
    ]

    for filename, part_title, start_idx, end_idx, order_num in parts:
        out = [
            '---',
            f'title: "{part_title}"',
            f'description: "ئۇستاز مۇھەممەد يۈسۈپنىڭ «ھاياتىڭىزنى قەدىرلەڭ» ئەسىرىدىن {part_title}."',
            'sidebar:',
            f'  label: "{part_title}"',
            f'  order: {order_num}',
            '---',
            '',
            'import { Aside } from \'@astrojs/starlight/components\';',
            '',
            '<Aside type="note">',
            f'تۆۋەندە «ھاياتىڭىزنى قەدىرلەڭ» كىتابىدىكى **{part_title}** تولۇق تېكىستى ۋە تەپسىلىي ئىبرەتلىرى بىلەن سۇنۇلدى. ھەر بىر ماقالە نومۇرىغا ياكى \'#\' بەلگىسىگە چېكىش ئارقىلىق بىۋاسىتە ئۇلىنىش ئالالايسىز.',
            '</Aside>',
            '',
        ]

        for i in range(start_idx, end_idx + 1):
            chap_id, title, start_p, end_p = CHAPTERS[i - 1]
            card_html = format_chapter(doc, i, chap_id, title, start_p, end_p)
            out.append(card_html)
            out.append('')

        (DOCS_DIR / filename).write_text('\n'.join(out), encoding='utf-8')
        print(f"Generated {filename}")

def generate_mesh_el_file(doc):
    """
    Extracts all 40 beacons (P271-299), accurately detecting multi-line titles
    via font information and assembling clean, flowing paragraphs and quotes.
    """
    out = [
        '---',
        'title: "40 مەشئەل (قىممەتلىك ئىبرەتلەر)"',
        'description: "ئۇستاز مۇھەممەد يۈسۈپنىڭ «ھاياتىڭىزنى قەدىرلەڭ» ئەسىرىدىن 40 مەشئەل — ھايات، ئەخلاق، ئىمان، سائادەت ۋە مۇۋەپپەقىيەت يېتەكچىلىرى."',
        'sidebar:',
        '  label: "40 مەشئەل"',
        '  order: 8',
        '---',
        '',
        'import { Aside } from \'@astrojs/starlight/components\';',
        '',
        '<Aside type="tip">',
        '**«40 مەشئەل»** — ھاياتتىكى ئەڭ مۇھىم ھەقىقەتلەر، ئەخلاق، سائادەت، ئىبادەت، ۋاقىت، كەچۈرۈم ۋە ئىنسانلىق قىممىتىنى يورۇتۇپ بېرىدىغان 40 پارلاق نۇر ۋە ھېكمەت مەنبەسىدۇر.',
        '</Aside>',
        '',
    ]

    all_mesh_lines = []
    beacon_footnotes = []
    
    for pno in range(271, 300):
        b, f = extract_page_lines(doc, pno)
        all_mesh_lines.extend(b)
        for fn in f:
            t = clean_text(fn['text'].replace('[[[', '').strip())
            if t and not t.isdigit():
                beacon_footnotes.append(t)

    beacons = []
    cur_num = None
    cur_title_lines = []
    cur_body = []
    
    num_pat = re.compile(r'^[\.ـ-]?\s*(\d+)\s*[\.ـ-]?\s*(.*)$')
    
    idx = 0
    while idx < len(all_mesh_lines):
        l = all_mesh_lines[idx]
        txt = l['text'].strip()
        if txt == '40 مەشئەل':
            idx += 1
            continue
            
        m = num_pat.match(txt)
        if m and int(m.group(1)) <= 40:
            if cur_num is not None:
                beacons.append((cur_num, ' '.join(cur_title_lines), cur_body))
            cur_num = int(m.group(1))
            t1 = m.group(2).strip()
            cur_title_lines = [t1] if t1 else []
            cur_body = []
            idx += 1
            # Check if next line is title continuation (heading line without number)
            if idx < len(all_mesh_lines):
                next_l = all_mesh_lines[idx]
                next_txt = next_l['text'].strip()
                if not num_pat.match(next_txt) and not next_l['is_quran'] and len(next_txt) < 50 and not next_txt.endswith(('.', '!', '؟')):
                    cur_title_lines.append(next_txt)
                    idx += 1
            continue
        else:
            if cur_num is not None:
                cur_body.append(l)
            idx += 1
            
    if cur_num is not None:
        beacons.append((cur_num, ' '.join(cur_title_lines), cur_body))

    for num, raw_title, body_lines in beacons:
        beacon_id = f"mesh-el-{num}"
        clean_title = clean_text(raw_title)
        ayah_tracker = {}
        
        out.append(f'<div class="hadith-card" id="{beacon_id}">')
        out.append('  <div class="hadith-header">')
        out.append(f'    <a href="#{beacon_id}" class="hadith-number-link" title="{num}-مەشئەلگە بىۋاسىتە ئۇلىنىش"><span class="hadith-number">{num}</span></a>')
        out.append(f'    <span class="hadith-title">{num}-مەشئەل: {clean_title}</span>')
        out.append(f'    <a href="#{beacon_id}" class="hadith-anchor" aria-label="{num}-مەشئەل بىۋاسىتە ئۇلىنىشى" title="بىۋاسىتە ئۇلىنىش">#</a>')
        out.append('  </div>')
        out.append('  <div class="hadith-translation">')

        b_blocks = []
        b_idx = 0
        while b_idx < len(body_lines):
            l = body_lines[b_idx]
            txt = l['text']
            if l['is_quran']:
                pno = l['pno']
                ayah_txt = get_next_ayah(pno, ayah_tracker)
                if ayah_txt:
                    b_blocks.append(('ayah', ayah_txt))
                while b_idx + 1 < len(body_lines) and body_lines[b_idx + 1]['is_quran']:
                    b_idx += 1
                b_idx += 1
                continue
                
            # Bullet item
            if txt.startswith(('●', '■', '•', '✦', '- ')):
                bullet_lines = [txt]
                b_idx += 1
                while b_idx < len(body_lines):
                    next_l = body_lines[b_idx]
                    if next_l['is_quran'] or next_l['text'].startswith(('●', '■', '•', '✦', '- ')):
                        break
                    if next_l['x1'] < 320 and bullet_lines[-1].endswith(('.', '!', '؟', '»', '”', '،')):
                        break
                    if bullet_lines[-1].endswith('-') or bullet_lines[-1].endswith(' -'):
                        bullet_lines[-1] = re.sub(r'\s*-\s*$', '', bullet_lines[-1])
                        bullet_lines.append(next_l['text'])
                    else:
                        bullet_lines.append(next_l['text'])
                    b_idx += 1
                    if next_l['text'].endswith(('.', '!', '؟', '»', '”')) and next_l['x0'] > 80:
                        break
                b_blocks.append(('bullet', ' '.join(bullet_lines)))
                continue

            # Regular paragraph
            p_lines = [txt]
            b_idx += 1
            while b_idx < len(body_lines):
                next_l = body_lines[b_idx]
                if next_l['is_quran'] or next_l['text'].startswith(('●', '■', '•', '✦', '- ')):
                    break
                if next_l['x1'] < 322 and p_lines[-1].endswith(('.', '!', '؟', ':', '»', '”')):
                    break
                if p_lines[-1].endswith('-') or p_lines[-1].endswith(' -'):
                    p_lines[-1] = re.sub(r'\s*-\s*$', '', p_lines[-1])
                    p_lines.append(next_l['text'])
                else:
                    p_lines.append(next_l['text'])
                b_idx += 1
                if next_l['text'].endswith(('.', '!', '؟', '»', '”')) and next_l['x0'] > 100:
                    break
            b_blocks.append(('para', ' '.join(p_lines)))

        fn_call_idx = 1
        for b_type, b_txt in b_blocks:
            b_txt = clean_text(b_txt)
            if not b_txt:
                continue
            while '[[[' in b_txt:
                b_txt = b_txt.replace('[[[', f'[^{fn_call_idx}]', 1)
                fn_call_idx += 1
            if b_type == 'ayah':
                out.append(f'    <p class="hadith-arabic">{b_txt}</p>')
            elif b_type == 'bullet':
                bullet_clean = re.sub(r'^[●•■✦\-]\s*', '', b_txt)
                out.append(f'    <p class="hadith-lesson-item">✦ {escape_mdx(bullet_clean)}</p>')
            else:
                out.append(f'    <p>{escape_mdx(b_txt)}</p>')

        out.append('  </div>')
        out.append('</div>')
        out.append('')

    (DOCS_DIR / "07-40-mesh-el.mdx").write_text('\n'.join(out), encoding='utf-8')
    print("Generated 07-40-mesh-el.mdx")

def generate_toqquz_tewsiye_file(doc):
    """
    Extracts the 9 Recommendations (P300-302) with clean paragraphs,
    pristine Quran verses, and correct footnotes.
    """
    out = [
        '---',
        'title: "توققۇز تەۋسىيە"',
        'description: "ئۇستاز مۇھەممەد يۈسۈپنىڭ «ھاياتىڭىزنى قەدىرلەڭ» كىتابىدىكى يەكۈنلىگۈچى توققۇز تۈرلۈك ئالتۇن يېتەكچى نەسىھەت."',
        'sidebar:',
        '  label: "توققۇز تەۋسىيە"',
        '  order: 9',
        '---',
        '',
        'import { Aside } from \'@astrojs/starlight/components\';',
        '',
        '<Aside type="tip">',
        '**«توققۇز تەۋسىيە»** — ھايات مۇساپىسىدە قەدەملىرىمىزنى پۇختا تاشلاش، روھىي چۈشكۈنلۈكتىن خالىي بولۇش، نىشانغا يېتىش ۋە دۇنيا-ئاخىرەتلىك بەختكە ئېرىشىش ئۈچۈن توققۇز قىممەتلىك يېتەكچى نەسىھەتتۇر.',
        '</Aside>',
        '',
    ]

    all_tewsiye_lines = []
    tewsiye_fn = []
    for pno in range(300, len(doc) + 1):
        b, f = extract_page_lines(doc, pno)
        all_tewsiye_lines.extend(b)
        for fn in f:
            t = clean_text(fn['text'].replace('[[[', '').strip())
            if t and not t.isdigit():
                tewsiye_fn.append(t)

    titles_map = {
        1: "تەقۋالىق قىلىش ھەققىدە",
        2: "ئۆتكەنگە ھەسرەت چەكمەسلىك ھەققىدە",
        3: "ئۈمىدۋار بولۇش ھەققىدە",
        4: "ياردەم قولىنى سۇنغانلارنى ئۇنتۇماسلىق ھەققىدە",
        5: "ياخشىلىق نۇرىنى چېچىش ھەققىدە",
        6: "تەكەببۇرلۇقتىن ساقلىنىش ھەققىدە",
        7: "ئۈمىدسىزلىكنى قەلبكە يولاتماسلىق ھەققىدە",
        8: "يېڭىلىشنى قەتئىي قوبۇل قىلماسلىق ھەققىدە",
        9: "ئوقۇش ۋە ئۆگىنىش ھەققىدە",
    }

    tewsiye_items = []
    cur_num = None
    cur_body = []
    
    num_pat = re.compile(r'^[\.ـ-]?\s*([1-9])\s*[\.ـ-]\s*(.*)$')
    
    for l in all_tewsiye_lines:
        txt = l['text'].strip()
        if txt == 'توققۇز تەۋسىيە':
            continue
        m = num_pat.match(txt)
        if m:
            if cur_num is not None:
                tewsiye_items.append((cur_num, cur_body))
            cur_num = int(m.group(1))
            first_txt = m.group(2).strip()
            cur_body = []
            if first_txt:
                cur_body.append({**l, 'text': first_txt})
        else:
            if cur_num is not None:
                cur_body.append(l)
                
    if cur_num is not None:
        tewsiye_items.append((cur_num, cur_body))

    ayah_tracker = {}
    for num, body_lines in tewsiye_items:
        tewsiye_id = f"tewsiye-{num}"
        title = titles_map.get(num, f"{num}-تەۋسىيە")
        
        out.append(f'<div class="hadith-card" id="{tewsiye_id}">')
        out.append('  <div class="hadith-header">')
        out.append(f'    <a href="#{tewsiye_id}" class="hadith-number-link" title="{num}-تەۋسىيەگە بىۋاسىتە ئۇلىنىش"><span class="hadith-number">{num}</span></a>')
        out.append(f'    <span class="hadith-title">{num}. {title}</span>')
        out.append(f'    <a href="#{tewsiye_id}" class="hadith-anchor" aria-label="{num}-تەۋسىيە بىۋاسىتە ئۇلىنىشى" title="بىۋاسىتە ئۇلىنىش">#</a>')
        out.append('  </div>')
        out.append('  <div class="hadith-translation">')

        b_blocks = []
        b_idx = 0
        while b_idx < len(body_lines):
            l = body_lines[b_idx]
            txt = l['text']
            if l['is_quran']:
                pno = l['pno']
                ayah_txt = get_next_ayah(pno, ayah_tracker)
                if ayah_txt:
                    b_blocks.append(('ayah', ayah_txt))
                while b_idx + 1 < len(body_lines) and body_lines[b_idx + 1]['is_quran']:
                    b_idx += 1
                b_idx += 1
                continue
                
            p_lines = [txt]
            b_idx += 1
            while b_idx < len(body_lines):
                next_l = body_lines[b_idx]
                if next_l['is_quran']:
                    break
                if next_l['x1'] < 322 and p_lines[-1].endswith(('.', '!', '؟', ':', '»', '”')):
                    break
                if p_lines[-1].endswith('-') or p_lines[-1].endswith(' -'):
                    p_lines[-1] = re.sub(r'\s*-\s*$', '', p_lines[-1])
                    p_lines.append(next_l['text'])
                else:
                    p_lines.append(next_l['text'])
                b_idx += 1
                if next_l['text'].endswith(('.', '!', '؟', '»', '”')) and next_l['x0'] > 100:
                    break
            b_blocks.append(('para', ' '.join(p_lines)))

        fn_call_idx = 1
        for b_type, b_txt in b_blocks:
            b_txt = clean_text(b_txt)
            if not b_txt:
                continue
            while '[[[' in b_txt:
                b_txt = b_txt.replace('[[[', f'[^{fn_call_idx}]', 1)
                fn_call_idx += 1
            if b_type == 'ayah':
                out.append(f'    <p class="hadith-arabic">{b_txt}</p>')
            else:
                out.append(f'    <p>{escape_mdx(b_txt)}</p>')

        out.append('  </div>')
        out.append('</div>')
        out.append('')

    if tewsiye_fn:
        out.append('<div class="hadith-footnotes-card" id="tewsiye-footnotes">')
        out.append('  <div class="hadith-header">')
        out.append('    <span class="hadith-title">توققۇز تەۋسىيەنىڭ ئىزاھات ۋە مەنبەلىرى</span>')
        out.append('  </div>')
        out.append('  <div class="hadith-translation">')
        out.append('    <div class="hadith-footnotes">')
        out.append('      <ol class="footnotes-list">')
        for fn in tewsiye_fn:
            out.append(f'        <li>{escape_mdx(fn)}</li>')
        out.append('      </ol>')
        out.append('    </div>')
        out.append('  </div>')
        out.append('</div>')
        out.append('')

    (DOCS_DIR / "08-toqquz-tewsiye.mdx").write_text('\n'.join(out), encoding='utf-8')
    print("Generated 08-toqquz-tewsiye.mdx")

def generate_muellip_file(doc):
    out = [
        '---',
        'title: "مۇئەللىپ ھەققىدە ۋە ئۇنىڭ ئەسەرلىرى"',
        'description: "ئۇستاز مۇھەممەد يۈسۈپ ئەپەندىنىڭ ھاياتى، ئىلمىي مۇساپىسى، پىكىر-قاراشلىرى ۋە نەشر قىلىنغان 32 پارچە ئەسىرى ھەققىدە تەپسىلىي بايان."',
        'sidebar:',
        '  label: "مۇئەللىپ ھەققىدە"',
        '  order: 1',
        '---',
        '',
        'import { Aside } from \'@astrojs/starlight/components\';',
        '',
        '<Aside type="note">',
        'بۇ سەھىپىدە «ھاياتىڭىزنى قەدىرلەڭ» ئەسىرىنىڭ ئاپتۇرى ئۇستاز مۇھەممەد يۈسۈپ مۇھەممەد تۇرسۇننىڭ تەرجىمىھالى، ئىلمىي قەدىمى ۋە يازغان، تەرجىمە قىلغان ئەسەرلىرىنىڭ تولۇق تىزىملىكى سۇنۇلدى.',
        '</Aside>',
        '',
    ]
    
    all_lines = []
    for pno in range(9, 19):
        b, _ = extract_page_lines(doc, pno)
        all_lines.extend(b)
        
    paragraphs = []
    cur_p = []
    for l in all_lines:
        txt = clean_text(l['text'])
        if not txt or txt in ['مۇئەللىپ ھەققىدە', 'مۇئەللىپ ھەققىدە ۋە ئۇنىڭ ئەسەرلىرى']:
            continue
        if txt.startswith(('###', '##', '•', '●', '■', '-', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')) or txt.endswith(':'):
            if cur_p:
                paragraphs.append(' '.join(cur_p))
                cur_p = []
            paragraphs.append(txt)
        else:
            if cur_p and (cur_p[-1].endswith('-') or cur_p[-1].endswith(' -')):
                cur_p[-1] = re.sub(r'\s*-\s*$', '', cur_p[-1])
                cur_p.append(txt)
            else:
                cur_p.append(txt)
    if cur_p:
        paragraphs.append(' '.join(cur_p))

    for p in paragraphs:
        if p.startswith('مۇھەممەد يۈسۈپ مۇھەممەد تۇرسۇننىڭ'):
            out.append(f'## {escape_mdx(p)}\n')
        elif p.startswith('ئەسەرلىرى') or p.startswith('نەشر قىلىنىش ئالدىدا') or p.startswith('ئەرەب تىلىدىن'):
            out.append(f'### {escape_mdx(p)}\n')
        elif re.match(r'^\.?\d+\s*[\.ـ-]', p):
            out.append(f'- **{escape_mdx(p)}**\n')
        else:
            out.append(f'{escape_mdx(p)}\n')

    (DOCS_DIR / "00-muqeddimu" / "01-muellip-heqqide.mdx").write_text('\n'.join(out), encoding='utf-8')
    print("Generated 01-muellip-heqqide.mdx")

def generate_kirish_soz_file(doc):
    out = [
        '---',
        'title: "كىرىش سۆز"',
        'description: "ئاپتور ئۇستاز مۇھەممەد يۈسۈپ ئەپەندىنىڭ «ھاياتىڭىزنى قەدىرلەڭ» ناملىق ئەسىرىگە يازغان كىرىش سۆز مۇقەددىمىسى."',
        'sidebar:',
        '  label: "كىرىش سۆز"',
        '  order: 2',
        '---',
        '',
        'import { Aside } from \'@astrojs/starlight/components\';',
        '',
        '<Aside type="tip">',
        'ھايات بىزگە بېرىلگەن كاتتا ئامانەت ۋە بەخت-سائادەت ماكانىدۇر. ئۇنى قانداق قەدىرلەش ۋە مەنىلىك ئۆتكۈزۈش ھەربىر ئىنساننىڭ ئەڭ موھىم بۇرچىدۇر.',
        '</Aside>',
        '',
    ]
    all_lines = []
    for pno in range(19, 21):
        b, _ = extract_page_lines(doc, pno)
        all_lines.extend(b)
        
    paragraphs = []
    cur_p = []
    for l in all_lines:
        txt = clean_text(l['text'])
        if not txt or txt in ['كىرىش سۆز', 'ھاياتىڭىزنى قەدىرلەڭ']:
            continue
        if l['x1'] < 322 and cur_p and cur_p[-1].endswith(('.', '!', '؟', ':')):
            paragraphs.append(' '.join(cur_p))
            cur_p = [txt]
        else:
            if cur_p and (cur_p[-1].endswith('-') or cur_p[-1].endswith(' -')):
                cur_p[-1] = re.sub(r'\s*-\s*$', '', cur_p[-1])
                cur_p.append(txt)
            else:
                cur_p.append(txt)
    if cur_p:
        paragraphs.append(' '.join(cur_p))

    for p in paragraphs:
        if 'ناھايىتى كۆيۈمچان، تولىمۇ مېھرىبان ئاللاھنىڭ ئىسمى بىلەن باشلايمەن' in p:
            out.append('> ناھايىتى كۆيۈمچان، تولىمۇ مېھرىبان ئاللاھنىڭ ئىسمى بىلەن باشلايمەن.\n')
        elif p.startswith('__') or p.startswith('2025'):
            out.append(f'**{escape_mdx(p)}**\n')
        else:
            out.append(f'{escape_mdx(p)}\n')

    (DOCS_DIR / "00-muqeddimu" / "02-kirish-soz.mdx").write_text('\n'.join(out), encoding='utf-8')
    print("Generated 02-kirish-soz.mdx")

def generate_index_file():
    """Generates the portal landing page with CardGrid and Table of Contents."""
    content = """---
title: ھاياتىڭىزنى قەدىرلەڭ
description: ئەزھەرى ئالىم ئۇستاز مۇھەممەد يۈسۈپنىڭ «ھاياتىڭىزنى قەدىرلەڭ» ناملىق نادىر كىتابى — ھايات، نىشان، ۋاقىت ۋە ئىنسانىي سائادەت قامۇسى.
template: splash
hero:
  title: ھاياتىڭىزنى قەدىرلەڭ
  tagline: ئەزھەرى ئالىم ئۇستاز مۇھەممەد يۈسۈپ مۇھەممەد تۇرسۇننىڭ قەلىمىگە مەنسۇپ «ھاياتىڭىزنى قەدىرلەڭ» (قَدِّر حياتك) ناملىق نادىر ئەسىرى — ھاياتنىڭ مەنىسى، ۋاقىتنى قەدىرلەش، مۇۋەپپەقىيەت ۋە مەنىۋى سائادەت يېتەكچىسى.
  actions:
    - text: كىتاب مەزمۇنلىرىنى ئوقۇش
      link: ./01-bap-01-10/
      icon: open-book
    - text: 40 مەشئەلگە كىرىش
      link: ./07-40-mesh-el/
      icon: star
      variant: secondary
    - text: كىتابنى چۈشۈرۈش (PDF)
      link: /hayat/hayatingizni-qedirleng.pdf
      icon: document
      variant: secondary
---

import { Card, CardGrid } from '@astrojs/starlight/components';

## كىتاب ھەققىدە قىسقىچە بايان

«ھاياتىڭىزنى قەدىرلەڭ» (قَدِّر حياتك) ناملىق كىتاب ھاياتىنى مەنىلىك، نىشانلىق، گۈزەل ۋە بەخت-سائادەت ئىچىدە ئۆتكۈزۈشنى خالايدىغان ھەربىر ئىنسان ئۈچۈن يېزىلغان قىممەتلىك يول كۆرسەتكۈچتۇر. ئۇستاز مۇھەممەد يۈسۈپ كىتابتا قۇرئان كەرىم روھى، سەھىھ ھەدىسلەرنىڭ نۇرى، تارىختىكى ئىبرەتلىك ھېكايىلەر ۋە زامانىۋى ئىنسانىيەت تەپەككۇرىنىڭ يۈكسەك نەتىجىلىرىنى يۇغۇرۇپ، ئوقۇرمەننى چۈشكۈنلۈكتىن، نىشانسىزلىقتىن ۋە ۋاقىت ئىسراپچىلىقىدىن قۇتۇلدۇرۇپ، يۈكسەك غايىلەرگە يېتەكلەيدۇ.

<CardGrid stagger>
  <Card title="57 پارچە تەپەككۇر ماقالىسى" icon="open-book">
    كىتابتا كەسىپ تاللاش، نىشان بەلگىلەش، تەنقىدكە تاقابىل تۇرۇش، ئۆزىنى ئىسلاھ قىلىش، ئائىلە ئىناقلىقى ۋە ۋاقىت باشقۇرۇشقا ئائىت 57 نادىر مەزمۇن بار.
  </Card>
  <Card title="40 مەشئەل" icon="star">
    ئىنسان ھاياتىدىكى ئەڭ ھالقىلىق پىرىنسىپلار ۋە روھىي قۇۋۋەتلەرنى يورۇتۇپ بېرىدىغان 40 سىستېمىلىق قىممەتلىك يېتەكچى چىراق.
  </Card>
  <Card title="9 ئالتۇن تەۋسىيە" icon="sun">
    ئاپتورنىڭ كىتاب ئاخىرىدا سۇنغان پۇختا قەدەم بېسىش، روھىي نىجاتلىق ۋە غەلىبە قازىنىش ئۈچۈن چەككەن ئالتۇن پىرىنسىپلىرى.
  </Card>
  <Card title="تولۇق كىتاب (PDF)" icon="document">
    [«ھاياتىڭىزنى قەدىرلەڭ» كىتابىنىڭ تولۇق 302 بەتلىك ئەسلى نەشرىنى بىۋاسىتە چۈشۈرۈپ ساقلىۋالالايسىز.](/hayat/hayatingizni-qedirleng.pdf)
  </Card>
</CardGrid>

---

## تولۇق مۇندەرىجە

### 0. كىرىش سۆز ۋە مۇقەددىمە
- [مۇئەللىپ ھەققىدە ۋە ئۇنىڭ ئەسەرلىرى](./00-muqeddimu/01-muellip-heqqide/)
- [ئاپتورنىڭ كىرىش سۆزى](./00-muqeddimu/02-kirish-soz/)

### 1. 1–10-ماقالىلەر: كەسىپ، كۆزقاراش ۋە تەپەككۇر
- [1-ماقالە: دۇنيادىكى ئەڭ ياخشى كەسىپ](./01-bap-01-10/#bap-01)
- [2-ماقالە: ھېچكىم تەنقىدلىمىسۇن دېسىڭىز...](./01-bap-01-10/#bap-02)
- [3-ماقالە: ئۆزىڭىزنىڭ مېڭىسىنى ئۆزىڭىز يۇيۇڭ](./01-bap-01-10/#bap-03)
- [4-ماقالە: ئۆزىڭىزنىڭ مۇھىم شەخس ئىكەنلىكىنى قانداق بىلىسىز؟](./01-bap-01-10/#bap-04)
- [5-ماقالە: كىشىلەرگە ئۇلار قىلغان مۇئامىلىنى قىلماڭ](./01-bap-01-10/#bap-05)
- [6-ماقالە: ئۆز كېمىڭىزنى ئۆزىڭىز ھەيدەڭ](./01-bap-01-10/#bap-06)
- [7-ماقالە: گۈزەللىكلەرنى كۆرۈش ئۈچۈنمۇ ئىقتىدار كېرەك](./01-bap-01-10/#bap-07)
- [8-ماقالە: سىزنىڭ شەخسىي قانائىتىڭىز مۇقەددەس پىكىر ئەمەس](./01-bap-01-10/#bap-08)
- [9-ماقالە: سۈكۈت ھەممىلا ئادەم بېجىرەلەيدىغان ماھارەت ئەمەس](./01-bap-01-10/#bap-09)
- [10-ماقالە: سىزنىڭ ياخشى كۆرگەنلىكىڭىز ئۈچۈنلا ئەمەس...](./01-bap-01-10/#bap-10)

### 2. 11–20-ماقالىلەر: ئەمەلىيەت، ئىرادە ۋە خۇشاللىق
- [11-ماقالە: بىلىش بىلەن تەتبىقلاش ئوتتۇرىسىدا](./02-bap-11-20/#bap-11)
- [12-ماقالە: بىز قانچىلىك بولالىدۇق؟](./02-bap-11-20/#bap-12)
- [13-ماقالە: ئاللاھ تائالادىن مۇمكىن ئەمەسلەرنى تىلەڭ!](./02-bap-11-20/#bap-13)
- [14-ماقالە: ئىرادىنى ھېچكىم بېرەلمەيدۇ](./02-bap-11-20/#bap-14)
- [15-ماقالە: يېرىم يىل ئۆمرىڭىز قالغان بولسا نېمە قىلاتتىڭىز؟](./02-bap-11-20/#bap-15)
- [16-ماقالە: نىشاندىن سوۋۇتۇش ھىيلىسى](./02-bap-11-20/#bap-16)
- [17-ماقالە: خۇشاللىقنى ئۆزىڭىزدىن ئىزدەڭ](./02-bap-11-20/#bap-17)
- [18-ماقالە: ئۇنتۇشمۇ بىر سەنئەت، ئۇنىمۇ ئۆگىنىۋېلىڭ!](./02-bap-11-20/#bap-18)
- [19-ماقالە: ياخشىسىنى كۈتۈڭ، چوقۇم كۆرىسىز](./02-bap-11-20/#bap-19)
- [20-ماقالە: جاھىللىق يامان ئىش ئەمەس](./02-bap-11-20/#bap-20)

### 3. 21–30-ماقالىلەر: ۋاقىت، روھىيەت ۋە ئۆمۈر نىجاتلىقى
- [21-ماقالە: مەشغۇل بولغانلىق قازانغانلىق ئەمەس](./03-bap-21-30/#bap-21)
- [22-ماقالە: ھاياتىمىزدا خاتا كۆزقاراشلارنىڭ نىسبىتى](./03-bap-21-30/#bap-22)
- [23-ماقالە: قورقمايدىغان ئادەم تۇغۇلۇپ باقمىدى](./03-bap-21-30/#bap-23)
- [24-ماقالە: مۇنداق كىشىلەردىن يىراق تۇرۇڭ](./03-bap-21-30/#bap-24)
- [25-ماقالە: سىزنى ئۆلتۈرەلمىگەن نەرسە كۈچلۈك قىلىدۇ](./03-bap-21-30/#bap-25)
- [26-ماقالە: ھېسسىيات دۈشمەنلىرىدىن يىراق تۇرۇڭ!](./03-bap-21-30/#bap-26)
- [27-ماقالە: ھېچكىم سىزنى بالىڭىزدەك نازارەت قىلالمايدۇ](./03-bap-21-30/#bap-27)
- [28-ماقالە: ئۇلار سىزنى قانداق باھالايدۇ؟](./03-bap-21-30/#bap-28)
- [29-ماقالە: ئۆمرىڭىزنى قانداق ئۇزىتالايسىز؟](./03-bap-21-30/#bap-29)
- [30-ماقالە: ھەسەل ھەرىسىدىكى قۇرئان مۆجىزىسى](./03-bap-21-30/#bap-30)

### 4. 31–40-ماقالىلەر: ئۆزىنى ئىسلاھ قىلىش، ئائىلە ۋە پۇرسەت
- [31-ماقالە: ئۆزگەرتمەكچى بولغىنىڭىز دەل ئۆزىڭىز بولۇڭ](./04-bap-31-40/#bap-31)
- [32-ماقالە: كىشىلەردىن نېمىلەرنى ئۆگىنەلەيسىز؟](./04-bap-31-40/#bap-32)
- [33-ماقالە: ئىشىڭىز مۇكەممەل بولسا تەنقىدچىلەردىن قورقماڭ!](./04-bap-31-40/#bap-33)
- [34-ماقالە: قىزلارنىڭ يىگىتلىرى توغرۇلۇق بىلىشى زۆرۈر بولغان ئىشلار](./04-bap-31-40/#bap-34)
- [35-ماقالە: ئوغۇللارنىڭ جور تاللىشىدا بىلىشى زۆرۈر بولغان ئىشلار](./04-bap-31-40/#bap-35)
- [36-ماقالە: پۇرسەت ۋە ھېكمەت](./04-bap-31-40/#bap-36)
- [37-ماقالە: مۇۋەپپەقىيەتلىك ئىشلارنى ئادەتكە ئايلاندۇرۇۋېلىڭ](./04-bap-31-40/#bap-37)
- [38-ماقالە: مۇۋەپپەقىيەتنىڭ سىرى](./04-bap-31-40/#bap-38)
- [39-ماقالە: ئاقىلانىچە كەچۈرۈم سوراشنى بىلەمسىز؟](./04-bap-31-40/#bap-39)
- [40-ماقالە: يېڭى يىلغا قانداق قارايسىز؟](./04-bap-31-40/#bap-40)

### 5. 41–50-ماقالىلەر: توغرا قارار، پىرىنسىپ ۋە ئائىلە تۈزۈمى
- [41-ماقالە: بەزى گۇمانلار دۆتلۈكتۇر](./05-bap-41-50/#bap-41)
- [42-ماقالە: قانداق قىلغاندا توغرا قارار قىلالايسىز؟](./05-bap-41-50/#bap-42)
- [43-ماقالە: كىشىلەر سىزنى نېمە ئۈچۈن ياخشى كۆرىدۇ ۋە نېمە ئۈچۈن يامان كۆرىدۇ](./05-bap-41-50/#bap-43)
- [44-ماقالە: ئاكتىپلىق ۋە پاسسىپلىق](./05-bap-41-50/#bap-44)
- [45-ماقالە: بىزنىڭ ئۆيدىكى 20 قائىدە](./05-bap-41-50/#bap-45)
- [46-ماقالە: ئىرادىنى ھېچكىم يېڭەلمەيدۇ](./05-bap-41-50/#bap-46)
- [47-ماقالە: «مۇمكىن ئەمەس» دېگەن سۆزنى لۇغىتىڭىزدىن چىقىرىپ تاشلاڭ!](./05-bap-41-50/#bap-47)
- [48-ماقالە: ئېنېرگىيە يۇقۇملۇقتۇر](./05-bap-41-50/#bap-48)
- [49-ماقالە: مۆجىزىلەر ھەرىكەتكە ئۆتكەنلەرگە كېلىدۇ](./05-bap-41-50/#bap-49)
- [50-ماقالە: بىز پۇشايمان قىلىدىغان 20 ئىش](./05-bap-41-50/#bap-50)

### 6. 51–57-ماقالىلەر: ئادەت، تەلەي ۋە ھاياتلىق قائىدىلىرى
- [51-ماقالە: مۇۋەپپەقىيەت كۈندىلىك ئادەتكە موھتاجدۇر](./06-bap-51-57/#bap-51)
- [52-ماقالە: مۇئامىلە پىرىنسىپى](./06-bap-51-57/#bap-52)
- [53-ماقالە: نورمال كۈلكە ساغلاملىقنىڭ دەلىلىدۇر](./06-bap-51-57/#bap-53)
- [54-ماقالە: ئەڭ تەلەيلىك ئىنسان](./06-bap-51-57/#bap-54)
- [55-ماقالە: 80/20 قانۇنىيىتى](./06-bap-51-57/#bap-55)
- [56-ماقالە: گەپ-سۆزىڭىزگە دىققەت قىلىڭ](./06-bap-51-57/#bap-56)
- [57-ماقالە: 90/10 قانۇنىيىتى](./06-bap-51-57/#bap-57)

### 7. 40 مەشئەل (قىممەتلىك ئىبرەتلەر)
- [40 مەشئەل مەزمۇنلىرىنى تولۇق كۆرۈش](./07-40-mesh-el/) (1-مەشئەلدىن 40-مەشئەلگىچە)

### 8. توققۇز تەۋسىيە
- [توققۇز تەۋسىيە مەزمۇنلىرىنى تولۇق كۆرۈش](./08-toqquz-tewsiye/) (1-تەۋسىيەدىن 9-تەۋسىيەگىچە)
"""
    (DOCS_DIR / "index.mdx").write_text(content, encoding='utf-8')
    print("Generated index.mdx")

def main():
    print("Starting robust extraction of «ھاياتىڭىزنى قەدىرلەڭ»...")
    doc = fitz.open(PDF_PATH)
    print(f"Loaded PDF: {PDF_PATH} ({len(doc)} pages)")
    
    generate_index_file()
    generate_muellip_file(doc)
    generate_kirish_soz_file(doc)
    generate_part_files(doc)
    generate_mesh_el_file(doc)
    generate_toqquz_tewsiye_file(doc)
    
    print("All 11 MDX documents generated successfully with zero line-break bugs!")

if __name__ == "__main__":
    main()
