# Context: Worker Milestone 4 (Section 02 Ibadet)

## Mission
Generate Section 02 (`src/content/docs/2000/02-ibadet/`, 14 MDX files: Q164–647) directly from `/Users/arslan/code/derslik/tools/extracted_2000.json` using Option B card markup, overwriting/replacing the placeholder files.

## Exclusively Owned Path
`src/content/docs/2000/02-ibadet/`
You MUST NOT write to any other content directories.

## Specifications
1. Read `/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md` and `/Users/arslan/code/derslik/.agents/PROJECT.md`.
2. Inspect `/Users/arslan/code/derslik/tools/extracted_2000.json`.
3. Generate exactly 14 MDX files in `src/content/docs/2000/02-ibadet/`:
   - `01-ibadet-esasliri.mdx`: Questions 164–183 (title: "ئىبادەتنىڭ ئەسلىي ماھىيىتى ۋە شەرتلىرى")
   - `02-sheriet-istilahliri.mdx`: Questions 184–204 (title: "شەرىئەت ئىستىلاھلىرى")
   - `03-pakliq-taharet.mdx`: Questions 205–248 (title: "پاكىزلىق ۋە تاھارەت ئەھكاملىرى")
   - `04-ayallargha-xas.mdx`: Questions 249–259 (title: "ئاياللارغا خاس ئەھكاملار")
   - `05-ghusul-teyemmum.mdx`: Questions 260–274 (title: "غۇسلى ۋە تەيەممۇم ئەھكاملىرى")
   - `06-namaz-ehkamliri.mdx`: Questions 275–332 (title: "نامازنىڭ ئەھمىيىتى ۋە شەرتلىرى")
   - `07-namaz-oqush.mdx`: Questions 333–393 (title: "نامازنىڭ تۈزۈلۈشى ۋە ئوقۇلۇش تەرتىپى")
   - `08-jamaet-jume.mdx`: Questions 394–428 (title: "جامائەت ۋە جۈمە نامىزى")
   - `09-bashqa-namazlar.mdx`: Questions 429–477 (title: "يولۇچىلار، ھېيت ۋە باشقا نامازلار")
   - `10-jinaze-depne.mdx`: Questions 478–506 (title: "جىنازا نامىزى ۋە دەپنە ئەھكاملىرى")
   - `11-zakat.mdx`: Questions 507–553 (title: "زاكات ۋە ئۇنىڭ ئەھكاملىرى")
   - `12-roza-ramizan.mdx`: Questions 554–607 (title: "روزا ۋە رامىزان ئەھكاملىرى")
   - `13-hej-omre.mdx`: Questions 608–634 (title: "ھەج ۋە ئۆمرە پائالىيىتى")
   - `14-sawab-gunah.mdx`: Questions 635–647 (title: "ساۋاب ۋە گۇناھ ھەققىدە")
4. Card Markup (Option B):
   ```html
   <div class="qa-card" id="q164">
     <div class="qa-question">
       <span class="qa-number">164</span>
       <span class="qa-label">سوئال:</span> ئىبادەتنىڭ ماھىيىتى نېمە؟
     </div>
     <div class="qa-answer">
       <span class="qa-label">جاۋاب:</span> ...
     </div>
   </div>
   ```
5. Run `python3 tests/e2e_2000.py --skip-build` to verify tests pass.
6. Write `handoff.md` and report back to parent.
