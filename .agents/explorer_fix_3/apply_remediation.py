#!/usr/bin/env python3
"""
apply_remediation.py
Remediation script for Din ve Hayat (2000 Sualliq) Part 1 defects.
Executed by worker agent to bring the repository to 100% compliance.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path("/Users/arslan/code/derslik")

def step1_delete_obsolete_files():
    print("=== Step 1: Deleting 4 Obsolete Files in 01-etiqad ===")
    obsolete_files = [
        REPO_ROOT / "src/content/docs/2000/01-etiqad/04-rohiy-alemler.mdx",
        REPO_ROOT / "src/content/docs/2000/01-etiqad/05-kitablar-peyghemberler.mdx",
        REPO_ROOT / "src/content/docs/2000/01-etiqad/06-qaza-qeder.mdx",
        REPO_ROOT / "src/content/docs/2000/01-etiqad/07-qiyamet-axiret.mdx",
    ]
    for f in obsolete_files:
        if f.exists():
            f.unlink()
            print(f"Deleted: {f.name}")
        else:
            print(f"Already absent: {f.name}")
            
    # Verify exactly 8 files remain
    etiqad_files = sorted(list((REPO_ROOT / "src/content/docs/2000/01-etiqad").glob("*.mdx")))
    print(f"Remaining files in 01-etiqad: {len(etiqad_files)} (Expected: 8)")
    assert len(etiqad_files) == 8, f"Expected 8 files, found {len(etiqad_files)}"


def step2_fix_munderije_and_index():
    print("\n=== Step 2: Updating 04-munderije.mdx and index.mdx ===")
    munderije_path = REPO_ROOT / "src/content/docs/2000/00-muqeddimu/04-munderije.mdx"
    munderije_content = """---
title: "مۇندەرىجە"
description: "«دىن ۋە ھايات (2000 سوئالغا جاۋاب)» 1-قىسىمنىڭ تولۇق بۆلۈم، تېما ۋە سوئاللار مۇندەرىجىسى."
---

## كىرىش ۋە مۇقەددىمە

- [كىتاب ھەققىدە](/2000/00-muqeddimu/01-kitab-heqqide/)
  - كىتاب ھەققىدە قىسقىچە تونۇشتۇرۇش
  - نەشر ئۇچۇرلىرى ۋە CIP كاتالوگ مەلۇماتى
  - بېغىشلاش
  - كىتابنىڭ ئاساسىي ئالاھىدىلىكلىرى
- [ئاپتور ھەققىدە](/2000/00-muqeddimu/02-aptur-heqqide/)
  - مۇھەممەد يۈسۈپ مۇھەممەد تۇرسۇننىڭ تەرجىمىھالى
  - مىسىر ئەزھەر ئۇنىۋېرسىتېتىدىكى تەھسىلى
  - تەلىم-تەربىيە ۋە جامائەت خىزمەتلىرى
  - ئاپتورنىڭ ئىدىيەۋى قارىشى ۋە مېتودولوگىيەسى
  - ئاپتور يازغان ۋە نەشر قىلىنغان ئەسەرلەر
  - ئەرەب تىلىدىن ئۇيغۇرچىغا تەرجىمە قىلغان كىتابلىرى
- [كىرىش سۆز](/2000/00-muqeddimu/03-kirish-soz/)
  - ئاپتورنىڭ سۆزى
  - كىتابنىڭ قۇرۇلمىسى ۋە بۆلۈملىرى
  - تەتقىقات مېتودولوگىيەسى ۋە پىرىنسىپلىرى
- [مۇندەرىجە](/2000/00-muqeddimu/04-munderije/)

---

## 1-بۆلۈم: ئېتىقاد (سوئال 1 – 163)

### 1. [دىن ۋە ئىنسان](/2000/01-etiqad/01-din-ve-etiqad/) (سوئال 1 – 20)
- دىن ھەققىدە قىسقىچە چۈشەنچە
  - ئىنسان ۋە دىن
  - دىنىي ئاڭ ئىنسانلار بىلەن بىرگە يارىتىلغان
  - ئاللاھنىڭ دىنى ئەزەلدىن بىردۇر
  - دۇنيادا ھەق دىن بىردۇر
  - ئاللاھنىڭ دىنى پۈتۈن ئىنسانىيەتكە كەلگەن ئورتاق دىن
  - دىن ئىجتىمائىي زۆرۈرىيەتتۇر
  - ئىنسانلار ئىچكى دۇنياسىدىن باشقۇرىلىدۇ
  - ئىلىم-پەن دىننىڭ رولىنى ئوينىيالمايدۇ
  - ئىسلام دىنى ۋە ئۇنىڭ غايىسى
- ئىمان ۋە ئېتىقاد ئاساسلىرى
  - كەلىمە تەييىبە ۋە ئۇنىڭ مەنىسى
  - ئىنساننىڭ يارىتىلىش مەقسىتى ۋە ۋەزىپىسى
  - ئادەمنى ئىماندىن چىقىرىدىغان ئامىللار

### 2. [ئاللاھقا ئىمان كەلتۈرۈش](/2000/01-etiqad/02-allahqa-iman/) (سوئال 21 – 48)
- ئاللاھقا ئىمان كەلتۈرۈش ئۆز ئىچىگە ئالىدىغان ھەقىقەتلەر
- ئاللاھ تائالانى تونۇشنىڭ ۋاسىتىلىرى
- ئەقىلنىڭ ۋەزىپىسى ۋە ئۇنىڭ ئىسلام دىنىدىكى ئورنى
- ئاللاھنىڭ سۈپەتلىرى ئاللاھنى تونۇشنىڭ ۋاسىتىسىدۇر
- ئاللاھنى قۇرئان ۋە ھەدىسلەردە كەلگەن سۈپەتلىرىدىن تونۇش

### 3. [ئاللاھنىڭ گۈزەل ئىسىملىرى ۋە سۈپەتلىرى](/2000/01-etiqad/03-allahning-isimliri/) (سوئال 49 – 62)
- ئاللاھ تائالانىڭ 99 گۈزەل ئىسمى (مۇكەممەل ئۈچ ئىستونلۇق جەدۋەل)
- ئاللاھنىڭ ئىسىملىرى بىلەن سۈپەتلىرى ئوتتۇرىسىدىكى پەرق
- زاتىي ۋە سۈبۇتىي سۈپەتلەر
- ئاللاھ تائالانى دۇنيادا كۆز بىلەن كۆرگىلى بولمايدىغانلىقى ھەققىدە

### 4. [پەرىشتىلەر، جىنلار ۋە شەيتانلار](/2000/01-etiqad/04-perishtiler-jinlar/) (سوئال 63 – 82)
- روھىي ئالەملەرنىڭ ھەقىقىتى
- پەرىشتىلەرگە ئىمان كەلتۈرۈش ۋە ئۇلارنىڭ خاراكتېرى
- تۆت چوڭ پەرىشتە ۋە باشقا پەرىشتىلەرنىڭ ۋەزىپىلىرى
- جىنلار ۋە شەيتانلارنىڭ ھەقىقىتى، خاراكتېرى ھەم ئىنسانلار بىلەن بولغان مۇناسىۋىتى

### 5. [ساماۋىي كىتابلار ۋە قۇرئان كەرىم](/2000/01-etiqad/05-samawiy-kitablar/) (سوئال 83 – 96)
- ئاللاھنىڭ كىتابلىرىغا ئىمان كەلتۈرۈش (تەۋرات، زەبۇر، ئىنجىل ۋە سەھىپىلەر)
- قۇرئان كەرىمنىڭ ئالاھىدىلىكى ۋە ساقلىنىشى

### 6. [پەيغەمبەرلەرگە ئىمان كەلتۈرۈش](/2000/01-etiqad/06-peyghamberler/) (سوئال 97 – 115)
- پەيغەمبەرلەرگە ئىمان كەلتۈرۈش، ئۇلارنىڭ سانى ۋە ئالاھىدىلىكلىرى
- پەيغەمبەر ئەلەيھىسسالاملارنىڭ مۆجىزىلىرى
- مۇھەممەد ئەلەيھىسسالامنىڭ ئاخىرقى پەيغەمبەرلىكى

### 7. [قازا ۋە قەدەرگە ئىمان](/2000/01-etiqad/07-qada-qeder/) (سوئال 116 – 134)
- قازا ۋە قەدەرنىڭ مەنىسى ۋە ماھىيىتى
- تەقدىرگە ئىشىنىش ۋە ئىنساننىڭ ئىرادىسى
- تەۋەككۈل قىلىشنىڭ توغرا مەنىسى

### 8. [قىيامەت ۋە ئاخىرەتكە ئىمان](/2000/01-etiqad/08-qiyamet-axiret/) (سوئال 135 – 163)
- قىيامەتنىڭ كىچىك ۋە چوڭ ئالامەتلىرى
- ئۆلۈم، قەبرە ھاياتى ۋە بەرزەخ ئالىمى
- قايتا تىرىلىش، ھېساب-كىتاب، تارازا ۋە سىرات كۆۋرۈكى
- جەننەت ۋە دوزاخنىڭ مەڭگۈلۈكى

---

## 2-بۆلۈم: ئىبادەت (سوئال 164 – 647)

### 1. [ئىبادەتنىڭ ئەسلىي ماھىيىتى ۋە شەرتلىرى](/2000/02-ibadet/01-ibadet-esasliri/) (سوئال 164 – 183)
- ئىبادەتنىڭ تۈرلىرى، شەرتلىرى ۋە نىيەتنىڭ ئەھمىيىتى

### 2. [شەرىئەت ئىستىلاھلىرى](/2000/02-ibadet/02-sheriet-istilahliri/) (سوئال 184 – 204)
- پەرز (پەرزى ئەين، پەرزى كىپايە)، ۋاجىب، سۈننەت، مۇستەھەب، ھارام، مەكرۇھ ۋە مۇباھ

### 3. [پاكىزلىق ۋە تاھارەت ئەھكاملىرى](/2000/02-ibadet/03-pakliq-taharet/) (سوئال 205 – 248)
- تاھارەتنىڭ پەرزلىرى، سۈننەتلىرى ۋە تاھارەتنى سۇندۇرىدىغان ئامىللار
- سۇلارنىڭ تۈرلىرى ۋە پاكىزلىق قائىدىلىرى

### 4. [ئاياللارغا خاس ئەھكاملار](/2000/02-ibadet/04-ayallargha-xas/) (سوئال 249 – 259)
- ھەيز، نىپاس ۋە ئىستىھازە ئەھكاملىرى

### 5. [غۇسلى ۋە تەيەممۇم ئەھكاملىرى](/2000/02-ibadet/05-ghusul-teyemmum/) (سوئال 260 – 274)
- غۇسلىنىڭ پەرزلىرى ۋە تەرتىپى
- سۇ تېپىلمىغاندا ياكى ئىشلەتكىلى بولمىغاندا قىلىنىدىغان تەيەممۇم ئەھكاملىرى

### 6. [نامازنىڭ ئەھمىيىتى ۋە شەرتلىرى](/2000/02-ibadet/06-namaz-ehkamliri/) (سوئال 275 – 332)
- نامازنىڭ تۈرلىرى ۋە ۋاقىتلىرى
- ئەزان ۋە تەكبىر ئەھكاملىرى
- نامازنىڭ تاشقى شەرتلىرى ۋە ئىچكى رۇكۇنلىرى

### 7. [ناماز ئوقۇش تەرتىبى](/2000/02-ibadet/07-namaz-oqush/) (سوئال 333 – 393)
- نامازنىڭ باشتىن-ئاخىر ئەمەلىي ئوقۇلۇش باسقۇچلىرى
- قىرائەت، رۇكۇ، سەجدە ۋە تەشەھھۇد دۇئالىرى
- نامازدىكى ۋاجىبلار، سۈننەتلەر ۋە نامازنى بۇزىدىغان ئىشلار

### 8. [جامائەت ۋە جۈمە نامازى](/2000/02-ibadet/08-jamaet-jume/) (سوئال 394 – 428)
- جامائەت نامىزىنىڭ پەزىلىتى ۋە ئىمامەتچىلىك شەرتلىرى
- جۈمە نامىزىنىڭ شەرتلىرى ۋە خۇتبە ئەھكاملىرى

### 9. [باشقا نامازلار](/2000/02-ibadet/09-bashqa-namazlar/) (سوئال 429 – 477)
- مۇساپىرنىڭ نامىزى، قەسىر قىلىش
- تەراۋىھ نامىزى، ھېيت نامازلىرى
- نەپلە نامازلار: تەھەججۇد، دۇھا، ئىستىخارە ۋە قۇياش-ئاي تۇتۇلغاندىكى نامازلار

### 10. [جىنازە ۋە دەپنە](/2000/02-ibadet/10-jinaze-depne/) (سوئال 478 – 506)
- جان ئۈزۈلۈش ئالدىدىكى ئىشلار
- مېيىتنى يۇيۇش، كېپەنلەش ۋە جىنازا نامىزىنى ئوقۇش
- قەبرە ۋە دەپنە قىلىش قائىدىلىرى

### 11. [زاكات ئەھكاملىرى](/2000/02-ibadet/11-zakat/) (سوئال 507 – 553)
- زاكاتنىڭ نىسابى ۋە ھېسابلاش قائىدىلىرى
- ئالتۇن، كۈمۈش، تىجارەت ماللىرى ۋە زىرائەتلەرنىڭ زاكىتى
- پىتىر سەدىقىسى ئەھكاملىرى

### 12. [روزا ۋە رامىزان](/2000/02-ibadet/12-roza-ramizan/) (سوئال 554 – 607)
- روزىنىڭ نىيىتى، پەرزلىرى ۋە روزىنى بۇزىدىغان ياكى بۇزمايدىغان ئىشلار
- قازا ۋە كاپارەت، پىديە ئەھكاملىرى
- ئېتىكاپنىڭ قائىدە-تەرتىپلىرى

### 13. [ھەج ۋە ئۈمرە](/2000/02-ibadet/13-hej-omre/) (سوئال 608 – 634)
- ھەج ۋە ئۆمرىنىڭ پەرزلىرى ۋە ۋاجىبلىرى
- ئىھرام، تاۋاپ، سەئيى، ئەرەفات ۋە مىنا ئەمەللىرى
- ھەج جىنايەتلىرى ۋە كاپارەتلىرى

### 14. [ساۋاب ۋە گۇناھ](/2000/02-ibadet/14-sawab-gunah/) (سوئال 640 – 647)
- چوڭ گۇناھلار (كەبائىر) ۋە ئۇلارنىڭ دەرىجىلىرى
- ھەقىقىي تەۋبىنىڭ شەرتلىرى ۋە كەچۈرۈم تەلەپ قىلىش
"""
    munderije_path.write_text(munderije_content, encoding="utf-8")
    print(f"Updated {munderije_path.name}")

    index_path = REPO_ROOT / "src/content/docs/2000/index.mdx"
    idx_content = index_path.read_text(encoding="utf-8")
    old_sec01_block = """2. **01-ئېتىقاد بۆلۈمى (1–163-سوئاللار)**:
   - دىن ۋە ئىمان ئاساسلىرى (1–34)
   - ئاللاھ تائالاغا ئىمان ۋە سۈپەتلەر (35–48، 49–62)
   - ئاللاھنىڭ 99 گۈزەل ئىسمى (مەخسۇس ھۆسنۈل مۇستەقىل جەدۋەل)
   - پەرىشتىلەرگە ئىمان (63–72)
   - جىن ۋە شەيتانلار (73–82)
   - ساماۋى كىتابلار ۋە پەيغەمبەرلەر (83–115)
   - قازا ۋە قەدەر (116–134)
   - قىيامەت ۋە ئاخىرەت ھاياتى (135–163)"""

    new_sec01_block = """2. **01-ئېتىقاد بۆلۈمى (1–163-سوئاللار)**:
   - دىن ۋە ئىنسان (1–20)
   - ئاللاھقا ئىمان كەلتۈرۈش (21–48)
   - ئاللاھنىڭ گۈزەل ئىسىملىرى ۋە سۈپەتلىرى (49–62، ئەسمائۇل ھۇسنا 99 ئىسىم جەدۋىلى)
   - پەرىشتىلەر، جىنلار ۋە شەيتانلار (63–82)
   - ساماۋىي كىتابلار ۋە قۇرئان كەرىم (83–96)
   - پەيغەمبەرلەرگە ئىمان كەلتۈرۈش (97–115)
   - قازا ۋە قەدەرگە ئىمان (116–134)
   - قىيامەت ۋە ئاخىرەتكە ئىمان (135–163)"""

    if old_sec01_block in idx_content:
        idx_content = idx_content.replace(old_sec01_block, new_sec01_block)
        index_path.write_text(idx_content, encoding="utf-8")
        print(f"Synchronized Section 01 ranges in {index_path.name}")
    else:
        print(f"Section 01 block in {index_path.name} already synchronized or different.")


def step3_normalize_farsi_yeh():
    print("\n=== Step 3: Normalizing Farsi Yeh (\\u06cc -> \\u064a) ===")
    targets = [
        REPO_ROOT / "src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx",
        REPO_ROOT / "src/content/docs/2000/01-etiqad/05-samawiy-kitablar.mdx",
        REPO_ROOT / "src/content/docs/2000/01-etiqad/08-qiyamet-axiret.mdx",
        REPO_ROOT / "tools/extracted_2000.json",
        REPO_ROOT / "tools/extract_2000.py",
    ]
    for p in targets:
        if p.exists():
            text = p.read_text(encoding="utf-8")
            count = text.count("\u06cc")
            if count > 0:
                text = text.replace("\u06cc", "\u064a")
                p.write_text(text, encoding="utf-8")
                print(f"Normalized {count} occurrences of \\u06cc in {p.name}")
            else:
                print(f"No \\u06cc found in {p.name}")


def step4_fix_99_names_duplicate():
    print("\n=== Step 4: Replacing Duplicate Name #76 with Al-Subbuh ===")
    # 1. In 03-allahning-isimliri.mdx
    names_file = REPO_ROOT / "src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx"
    content = names_file.read_text(encoding="utf-8")
    
    target_row = "| الصَّمَدُ | ئەسسەمەد | ھېچكىمگە مۇھتاج بولمىغان، ھەممە مەخلۇقات ھاجەتلىرىنى راۋا قىلىشتا پەقەت ئۇنىڭغىلا يۈزلىنىدىغان ئۇلۇغ زاتتۇر. |"
    replacement_row = "| السُّبُّوحُ | ئەسسۇببۇھ | پۈتۈنلەي نۇقساندىن ۋە ھەر قانداق ئەيىبتىن پاك، بارلىق گۈزەل كامالىي سۈپەتلەر ئاللاھقىلا مەنسۇپ بولغان زاتتۇر. |"
    
    if target_row in content:
        content = content.replace(target_row, replacement_row)
        names_file.write_text(content, encoding="utf-8")
        print("Replaced Row 76 with Al-Subbuh in 03-allahning-isimliri.mdx")
    else:
        print("Target row 76 not found in 03-allahning-isimliri.mdx (may already be updated)")

    # 2. In tools/extracted_2000.json
    json_file = REPO_ROOT / "tools/extracted_2000.json"
    if json_file.exists():
        j_text = json_file.read_text(encoding="utf-8")
        old_json_entry = '{"id": 76, "arabic": "الصَّمَدُ", "transliteration": "ئەسسەمەد", "meaning": "ھېچكىمگە مۇھتاج بولمىغان، ھەممە مەخلۇقات ھاجەتلىرىنى راۋا قىلىشتا پەقەت ئۇنىڭغىلا يۈزلىنىدىغان ئۇلۇغ زاتتۇر."}'
        new_json_entry = '{"id": 76, "arabic": "السُّبُّوحُ", "transliteration": "ئەسسۇببۇھ", "meaning": "پۈتۈنلەي نۇقساندىن ۋە ھەر قانداق ئەيىبتىن پاك، بارلىق گۈزەل كامالىي سۈپەتلەر ئاللاھقىلا مەنسۇپ بولغان زاتتۇر."}'
        if old_json_entry in j_text:
            j_text = j_text.replace(old_json_entry, new_json_entry)
            json_file.write_text(j_text, encoding="utf-8")
            print("Replaced Entry #76 in tools/extracted_2000.json")

    # 3. In tools/extract_2000.py
    py_file = REPO_ROOT / "tools/extract_2000.py"
    if py_file.exists():
        p_text = py_file.read_text(encoding="utf-8")
        p_text = p_text.replace('"الحَقُّ", "المُحِيطُ", "الصَّمَدُ", "المُبِينُ"', '"الحَقُّ", "المُحِيطُ", "السُّبُّوحُ", "المُبِينُ"')
        p_text = p_text.replace('"ئەل ھەق", "ئەل مۇھىيت", "ئەسسەمەد", "ئەل مۇبىين"', '"ئەل ھەق", "ئەل مۇھىيت", "ئەسسۇببۇھ", "ئەل مۇبىين"')
        if "ئەسسۇببۇھ" not in p_text:
            p_text = p_text.replace("ئەسسەمەد|ئەل مۇبىين", "ئەسسۇببۇھ|ئەسسەمەد|ئەل مۇبىين")
        py_file.write_text(p_text, encoding="utf-8")
        print("Updated Al-Subbuh definitions in tools/extract_2000.py")


def main():
    step1_delete_obsolete_files()
    step2_fix_munderije_and_index()
    step3_normalize_farsi_yeh()
    step4_fix_99_names_duplicate()
    print("\nRemediation completed successfully!")

if __name__ == "__main__":
    main()
