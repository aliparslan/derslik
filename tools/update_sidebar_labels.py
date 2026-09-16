#!/usr/bin/env python3
"""
Updates the frontmatter sidebar.label in all 2000 MDX files to exactly match
the content and structure of "تۈزۈلۈش تەرتىپى".
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
DOCS_2000 = ROOT / "src" / "content" / "docs" / "2000"

# Target labels from "تۈزۈلۈش تەرتىپى"
LABELS_MAP = {
    # 00-muqeddimu
    "00-muqeddimu/01-kitab-heqqide.mdx": ("كىتاب ھەققىدە ۋە بېغىشلاش", 1),
    "00-muqeddimu/02-aptur-heqqide.mdx": ("ئاپتور مۇھەممەد يۈسۈپ ھەققىدە", 2),
    "00-muqeddimu/03-kirish-soz.mdx": ("كىرىش سۆز ۋە مېتودولوگىيە", 3),
    "00-muqeddimu/04-munderije.mdx": ("تولۇق مۇندەرىجە", 4),

    # 01-etiqad (1–163)
    "01-etiqad/01-din-ve-etiqad.mdx": ("دىن ۋە ئېتىقاد ئاساسلىرى (1–20)", 1),
    "01-etiqad/02-allahqa-iman.mdx": ("ئاللاھقا ئىمان كەلتۈرۈش (21–48)", 2),
    "01-etiqad/03-allahning-isimliri.mdx": ("ئاللاھنىڭ گۈزەل ئىسىملىرى ۋە سۈپەتلىرى (49–62، 99 ئىسىم جەدۋىلى)", 3),
    "01-etiqad/04-perishtiler-jinlar.mdx": ("پەرىشتىلەر، جىنلار ۋە شەيتانلار (63–82)", 4),
    "01-etiqad/05-samawiy-kitablar.mdx": ("ساماۋىي كىتابلار ۋە قۇرئان كەرىم (83–96)", 5),
    "01-etiqad/06-peyghamberler.mdx": ("پەيغەمبەرلەرگە ئىمان كەلتۈرۈش (97–115)", 6),
    "01-etiqad/07-qada-qeder.mdx": ("قازا ۋە قەدەرگە ئىمان (116–134)", 7),
    "01-etiqad/08-qiyamet-axiret.mdx": ("قىيامەت ۋە ئاخىرەتكە ئىمان (135–163)", 8),

    # 02-ibadet (164–647)
    "02-ibadet/01-ibadet-esasliri.mdx": ("ئىبادەت ئاساسلىرى ۋە شەرتلىرى (164–183)", 1),
    "02-ibadet/02-sheriet-istilahliri.mdx": ("شەرىئەت ئاتالغۇلىرى: پەرز، ۋاجىب، سۈننەت، ھارام، مەكرۇھ، مۇباھ (184–204)", 2),
    "02-ibadet/03-pakliq-taharet.mdx": ("پاكلىق ۋە تاھارەت ئەھكاملىرى (205–248)", 3),
    "02-ibadet/04-ayallargha-xas.mdx": ("ئاياللارغا خاس ئەھكاملار (249–259)", 4),
    "02-ibadet/05-ghusul-teyemmum.mdx": ("غۇسلى ۋە تەيەممۇم (260–274)", 5),
    "02-ibadet/06-namaz-ehkamliri.mdx": ("ناماز ۋە ئۇنىڭ پەرز-سۈننەتلىرى (275–332)", 6),
    "02-ibadet/07-namaz-oqush.mdx": ("ناماز ئوقۇشنىڭ ئەمەلىي تەرتىپى (333–393)", 7),
    "02-ibadet/08-jamaet-jume.mdx": ("جامائەت ۋە جۈمە نامىزى (394–428)", 8),
    "02-ibadet/09-bashqa-namazlar.mdx": ("باشقا نامازلار: ھېيت، سەپەر، تەراۋىھ، نەپلە (429–477)", 9),
    "02-ibadet/10-jinaze-depne.mdx": ("جىنازە ۋە دەپنە ئىشلىرى (478–506)", 10),
    "02-ibadet/11-zakat.mdx": ("زاكات ئەھكاملىرى ۋە مال مىقدارلىرى (507–553)", 11),
    "02-ibadet/12-roza-ramizan.mdx": ("روزا، رامىزان ۋە ئېتىكاپ (554–607)", 12),
    "02-ibadet/13-hej-omre.mdx": ("ھەج ۋە ئۆمرە پائالىيەتلىرى (608–634)", 13),
    "02-ibadet/14-sawab-gunah.mdx": ("ساۋابلىق ۋە گۇناھ ئەمەللەر (635–647)", 14),
}

def update_file(rel_path: str, label: str, order: int):
    file_path = DOCS_2000 / rel_path
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    content = file_path.read_text(encoding="utf-8")
    
    # Check if frontmatter exists
    fm_match = re.match(r"^---\n([\s\S]*?)\n---", content)
    if not fm_match:
        print(f"No frontmatter in {rel_path}")
        return
    
    fm_text = fm_match.group(1)
    
    # Update or add sidebar block
    if "sidebar:" in fm_text:
        # Replace sidebar block
        fm_text = re.sub(
            r"sidebar:\s*\n\s*label:[^\n]*\n\s*order:[^\n]*",
            f"sidebar:\n  label: \"{label}\"\n  order: {order}",
            fm_text
        )
    else:
        # Append sidebar block
        fm_text += f"\nsidebar:\n  label: \"{label}\"\n  order: {order}"
        
    new_content = f"---\n{fm_text}\n---" + content[fm_match.end():]
    file_path.write_text(new_content, encoding="utf-8")
    print(f"Updated {rel_path} -> {label} (order {order})")

for rel_path, (label, order) in LABELS_MAP.items():
    update_file(rel_path, label, order)

print("Finished updating all frontmatter labels!")
