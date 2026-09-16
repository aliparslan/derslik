# Handoff Report: Codebase Survey & Astro / Starlight Architecture

**Agent**: Codebase Explorer  
**Date**: 2026-09-15  
**Working Directory**: `/Users/arslan/code/derslik/.agents/explorer_survey_codebase/`  
**Parent Conversation ID**: `402b5da9-8a97-44a9-a924-d815f3a13527`  
**Handoff Type**: Hard (Investigation complete)  

---

## 1. Observation

1. **`package.json` and Package Manager**:
   - Location: [`/Users/arslan/code/derslik/package.json`](file:///Users/arslan/code/derslik/package.json), lines 5–20.
   - Scripts: `"dev": "astro dev"`, `"start": "astro dev"`, `"build": "astro build"`, `"preview": "astro preview"`, `"astro": "astro"`, `"deploy": "pnpm build && wrangler deploy"`.
   - Dependencies: `"@astrojs/starlight": "^0.42.0"`, `"astro": "^7.2.10"`, `"sharp": "^0.35.3"`.
   - DevDependencies: `"wrangler": "^4.131.1"`.
   - Package manager is `pnpm` (lockfile present at [`pnpm-lock.yaml`](file:///Users/arslan/code/derslik/pnpm-lock.yaml) [128 KB] and [`pnpm-workspace.yaml`](file:///Users/arslan/code/derslik/pnpm-workspace.yaml)).
   - `@astrojs/check` is **not installed** in `package.json`.
2. **Python Environment & PyMuPDF**:
   - System python `/usr/bin/python3` has `fitz` (`PyMuPDF`) installed.
   - Verbatim evidence from system logs at [`/Users/arslan/.gemini/antigravity/brain/4cef4897-f493-4acb-b5ac-2ecb06b0aee7/.system_generated/logs/transcript.jsonl:104`](file:///Users/arslan/.gemini/antigravity/brain/4cef4897-f493-4acb-b5ac-2ecb06b0aee7/.system_generated/logs/transcript.jsonl):
     ```
     Output:
     fitz is installed!
     pypdf NOT installed
     pypdf2 NOT installed
     pdfplumber NOT installed
     pdfminer NOT installed
     ```
   - Verbatim evidence testing PDF at line 106:
     ```
     Page count: 300
     Page 1 text snippet:
     ' ﯾﯜﺳﯜپ ﻣﯘھەﻣﻤەد\n ھﺎﯾﺎت ۋە دٮﻦ\n (ﺟﺎۋاب ﺳﻮﺋﺎﻟﻐﺎ 2000)\n ﻗٮﺴٮﻢ ﺑٮﺮٮﻨﭽﻰ\n {1}\n ﻧەﺷﺮٮﯿﺎﺗﻰ ﺋەﺳەرﻟەر ﺋٮﺴﻼﻣٮﻲ\n'
     ```
3. **Starlight Configuration in `astro.config.mjs`**:
   - Location: [`/Users/arslan/code/derslik/astro.config.mjs`](file:///Users/arslan/code/derslik/astro.config.mjs), lines 8–101.
   - `defaultLocale: 'root'`.
   - `locales`: `root` (`lang: 'uy'`, `dir: 'rtl'`) and `en` (`lang: 'en'`, `dir: 'ltr'`).
   - Sidebar: Lines 40–92 contain `introduction` and 6 stage items (`1-osmurler` through `6-yetakchi`). **No entry exists for `2000`**.
   - Custom CSS: Line 94 references `'./src/styles/custom.css'`.
   - Custom Components: Lines 97–98 override `Header` (`'./src/components/Header.astro'`) and `Footer` (`'./src/components/Footer.astro'`).
   - Search: Handled via `@astrojs/starlight` built-in Pagefind integration; search results and UI index exist in `dist/pagefind/`.
4. **Content Collections Setup**:
   - Location: [`/Users/arslan/code/derslik/src/content.config.ts`](file:///Users/arslan/code/derslik/src/content.config.ts), lines 5–8:
     ```typescript
     export const collections = {
       docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }),
       i18n: defineCollection({ loader: i18nLoader(), schema: i18nSchema() }),
     };
     ```
   - Uses Astro 5 Content Layer API with Starlight loaders and schemas. No custom content collection exists.
5. **Existing Docs Structure & Quality of `src/content/docs/2000/`**:
   - Directory contents: `index.mdx` (1808 bytes), `01-etiqad/` (7 files), `02-ibadet/` (14 files).
   - `00-muqeddimu/` is completely absent.
   - Word order reversal: In [`01-din-ve-etiqad.mdx:12`](file:///Users/arslan/code/derslik/src/content/docs/2000/01-etiqad/01-din-ve-etiqad.mdx), line reads:
     `<span class="qa-label">سوئال:</span> بولغان؟ پەیدا نەدىن ئىنسانلار`
     (Natural Uyghur order is: `ئىنسانلار نەدىن پەيدا بولغان؟`).
   - Incomplete questions: `05-kitablar-peyghemberler.mdx` ends at Q99; `06-qaza-qeder.mdx` and `07-qiyamet-axiret.mdx` are 0-content stubs; `02-ibadet/` has only Q337 in `06-namaz-ehkamliri.mdx`.
   - The 99 Names of Allah table is entirely missing from `03-allahning-isimliri.mdx`.
6. **Option B "Continuous Reading Cards Layout"**:
   - Requirement defined in `/Users/arslan/.gemini/antigravity/brain/4cef4897-f493-4acb-b5ac-2ecb06b0aee7/implementation_plan.md:95`: Questions and answers sequentially displayed with distinct card borders for straight-through reading and instant Pagefind indexing.
   - In `src/content/docs/2000/*.mdx`, HTML tags are present: `<div class="qa-card" id="q...">`, `<div class="qa-question">`, `<span class="qa-number">`, `<div class="qa-answer">`.
   - Grep search for `qa-card` or `qa-` across `src/styles/` and `src/components/` returned **zero matches**. No styling rules exist for these classes.

---

## 2. Logic Chain

1. **Why existing MDX files have reversed words**:
   - Observation 2 shows that PyMuPDF's `get_text()` returns `ﯾﯜﺳﯜپ ﻣﯘھەﻣﻤەد` (visual left-to-right), where `Yusup` appears before `Muhammad`. In an RTL layout, the start of the line is on the right.
   - In Observation 5, [`01-din-ve-etiqad.mdx:12`](file:///Users/arslan/code/derslik/src/content/docs/2000/01-etiqad/01-din-ve-etiqad.mdx) contains `بولغان؟ پەیدا نەدىن ئىنسانلار`.
   - Therefore, the prior parser ingested lines in PyMuPDF's visual stream without reversing word order to reconstruct logical RTL reading order. The extraction script must explicitly reconstruct lines in logical Uyghur word order.
2. **Why `2000` is currently unreachable from the main sidebar**:
   - Observation 3 shows `astro.config.mjs` sidebar only includes `introduction` and `1-osmurler` through `6-yetakchi`.
   - Therefore, while `src/content/docs/2000/index.mdx` exists, Starlight does not display it in the navigation tree until `astro.config.mjs` is updated.
3. **Why Option B styling is currently non-functional**:
   - Observation 5 & 6 show MDX files use `.qa-card`, `.qa-question`, `.qa-number`, `.qa-answer`, but Observation 6 confirms zero CSS definitions exist in `src/styles/custom.css`.
   - Therefore, the continuous reading layout looks like unformatted text without card backgrounds, padding, or borders. Adding CSS rules to `src/styles/custom.css` with logical properties (`border-inline-start`, etc.) is required to realize Option B.
4. **Why `pnpm build` is the mandatory build verification**:
   - Observation 1 shows `@astrojs/check` is not in `package.json`, but `pnpm build` (`astro build`) is configured and exercises full MDX compilation, asset bundling, and Pagefind search index generation.

---

## 3. Caveats

- Interactive shell commands (`run_command`) triggered an interactive user confirmation prompt that timed out; all environmental and system facts were verified directly from package descriptors, configuration files, Git logs, and Python execution transcripts in the workspace.
- The source PDF at `/Users/arslan/.gemini/antigravity/brain/4cef4897-f493-4acb-b5ac-2ecb06b0aee7/.user_uploaded/media_1789428359497.pdf` has 300 pages; detailed parsing logic for pages 1–30 (`00-muqeddimu`) and 56–69 (99 Names table) will be produced by peer miners `spec_miner_pdf_structure` and `spec_miner_99names_divisions`.
- No changes to source code were made during this investigation (strictly read-only).

---

## 4. Conclusion

1. **Environment & Tooling**:
   - Package manager: `pnpm`. Build command: `pnpm build`.
   - Python 3 with `fitz` (`PyMuPDF`) is installed at `/usr/bin/python3`.
2. **Content Status**:
   - Existing MDX files under `src/content/docs/2000/` are broken due to line word-order reversal and are incomplete (missing `00-muqeddimu`, 99 Names table, Q100-163, and Q164-647). They must be regenerated with a proper RTL-aware normalization pipeline.
3. **Configuration & Styling Needed**:
   - Add `2000 سوئال-جاۋاب` navigation group to `astro.config.mjs`.
   - Add Option B `.qa-card` CSS styles to `src/styles/custom.css`.

---

## 5. Verification Method

To independently verify these findings:

1. **Verify Dependencies & Config**:
   - Inspect [`package.json`](file:///Users/arslan/code/derslik/package.json) lines 5–20.
   - Inspect [`astro.config.mjs`](file:///Users/arslan/code/derslik/astro.config.mjs) lines 40–95.
   - Inspect [`src/content.config.ts`](file:///Users/arslan/code/derslik/src/content.config.ts) lines 1–8.
2. **Verify Text Defects in Existing MDX**:
   - Inspect [`src/content/docs/2000/01-etiqad/01-din-ve-etiqad.mdx`](file:///Users/arslan/code/derslik/src/content/docs/2000/01-etiqad/01-din-ve-etiqad.mdx) line 12: observe reversed word order.
   - Inspect [`src/content/docs/2000/02-ibadet/01-ibadet-esasliri.mdx`](file:///Users/arslan/code/derslik/src/content/docs/2000/02-ibadet/01-ibadet-esasliri.mdx): observe empty stub (no questions).
3. **Verify CSS Absence for Option B**:
   - Search for `.qa-card` in [`src/styles/custom.css`](file:///Users/arslan/code/derslik/src/styles/custom.css): observe zero occurrences.
4. **Project Build Command**:
   - `pnpm build` will compile the entire site into `./dist` and generate Pagefind search indices in `./dist/pagefind`.
