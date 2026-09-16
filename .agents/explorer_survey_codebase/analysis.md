# Deep Codebase Survey & Analysis Report

**Date**: 2026-09-15  
**Investigator**: Codebase Explorer  
**Subject**: Astro / Starlight Project Architecture & Readiness for "دىن ۋە ھايات (2000 سوئالغا جاۋاب)" Conversion  
**Project Root**: `/Users/arslan/code/derslik`  

---

## Executive Summary

The project `derslik` is an Astro v7.2 + Starlight v0.42 documentation site hosted on Cloudflare Workers (`terbiye.org`). The primary language is Uyghur (RTL, Arabic script) set as the root locale, with an English translation scaffold under `/en/`.

Part 1 of the 700-page book "دىن ۋە ھايات (2000 سوئالغا جاۋاب)" covers Questions 1 to 647. An initial attempt at generating `src/content/docs/2000/` was started but left in an incomplete and severely corrupted state:
1. **Critical text reversal defect**: In all currently existing MDX files in `src/content/docs/2000/01-etiqad/`, Uyghur words within sentences were extracted in visual LTR order instead of logical RTL reading order (e.g. `بولغان؟ پەیدا نەدىن ئىنسانلار` instead of `ئىنسانلار نەدىن پەيدا بولغان؟`).
2. **Missing sections and questions**: `00-muqeddimu/` is completely absent; `01-etiqad/` is missing questions 100–163 and the 99 Names of Allah table; `02-ibadet/` contains only 1 question (Q337) across 14 stub files.
3. **Missing Option B CSS**: HTML classes `.qa-card`, `.qa-question`, `.qa-number`, `.qa-answer` are present in MDX files but have **zero CSS definitions** in `src/styles/custom.css` or anywhere else.
4. **Environment**: Python 3 at `/usr/bin/python3` has `fitz` (`PyMuPDF`) installed and verified against the 300-page source PDF.

---

## 1. Package Manager, Dependencies, Scripts & Python Environment

### Package Manager & Scripts
From [`package.json`](file:///Users/arslan/code/derslik/package.json):
```json
{
  "name": "derslik",
  "type": "module",
  "version": "0.0.1",
  "scripts": {
    "dev": "astro dev",
    "start": "astro dev",
    "build": "astro build",
    "preview": "astro preview",
    "astro": "astro",
    "deploy": "pnpm build && wrangler deploy"
  },
  "dependencies": {
    "@astrojs/starlight": "^0.42.0",
    "astro": "^7.2.10",
    "sharp": "^0.35.3"
  },
  "devDependencies": {
    "wrangler": "^4.131.1"
  }
}
```
- **Package Manager**: `pnpm` (evidenced by [`pnpm-lock.yaml`](file:///Users/arslan/code/derslik/pnpm-lock.yaml), [`pnpm-workspace.yaml`](file:///Users/arslan/code/derslik/pnpm-workspace.yaml), and the `deploy` script).
- **TypeScript**: Extends `astro/tsconfigs/strict` ([`tsconfig.json`](file:///Users/arslan/code/derslik/tsconfig.json)).
- **Astro Check**: `@astrojs/check` is **not** installed in `dependencies` or `devDependencies`. `pnpm build` (`astro build`) is the primary verification command.
- **Wrangler**: Cloudflare Workers deployment configured in [`wrangler.jsonc`](file:///Users/arslan/code/derslik/wrangler.jsonc) with static assets pointing to `./dist` and `html_handling: "force-trailing-slash"`.

### Python & PyMuPDF Availability
- Verified system Python: `/usr/bin/python3`.
- `fitz` (`PyMuPDF` v1.x) is **installed and functional** in the macOS system Python environment (verified via previous execution log in `.gemini/antigravity/brain/4cef4897-f493-4acb-b5ac-2ecb06b0aee7/.system_generated/logs/transcript.jsonl:104`).
- Confirmed reading the 300-page PDF at `/Users/arslan/.gemini/antigravity/brain/4cef4897-f493-4acb-b5ac-2ecb06b0aee7/.user_uploaded/media_1789428359497.pdf` (`Page count: 300`).
- Note: Python is used as an out-of-band extraction and data normalization utility, rather than an npm package dependency.

---

## 2. Starlight Configuration in `astro.config.mjs`

### Locales & RTL Configuration
From [`astro.config.mjs`](file:///Users/arslan/code/derslik/astro.config.mjs):
```javascript
export default defineConfig({
  site: 'https://terbiye.org',
  vite: {
    resolve: {
      alias: {
        '~': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
  },
  integrations: [
    starlight({
      title: { uy: 'تەربىيە', en: 'Terbiye' },
      defaultLocale: 'root',
      locales: {
        root: { label: 'ئۇيغۇرچە', lang: 'uy', dir: 'rtl' },
        en: { label: 'English', lang: 'en', dir: 'ltr' },
      },
      ...
```
- **Root Locale**: Uyghur (`lang: 'uy'`), with `dir: 'rtl'`.
- **RTL Support**: Built into Starlight core; custom typography specified in [`src/styles/custom.css`](file:///Users/arslan/code/derslik/src/styles/custom.css) loading Google Font `'Noto Sans Arabic'`:
  ```css
  [dir='rtl'] {
    --sl-font: 'Noto Sans Arabic', 'Noto Naskh Arabic', system-ui, sans-serif;
    --sl-font-mono: 'Noto Sans Arabic', 'Noto Naskh Arabic', system-ui, sans-serif;
  }
  ```
- **Routing Middleware**: [`src/middleware.ts`](file:///Users/arslan/code/derslik/src/middleware.ts) strips phantom `/uy/...` and `/en/uy/...` prefixes created by Astro's internal mapping of root locale to language code.

### Sidebar Architecture
The current sidebar contains:
1. `مۇقەددىمە` (`slug: 'introduction'`)
2. `1. ئۆسمۈرلەر باسقۇچى` (`autogenerate: { directory: '1-osmurler' }`)
3. `2. ياشلار باسقۇچى` (`autogenerate: { directory: '2-yashlar' }`)
4. `3. تەييارلىق باسقۇچى` (`autogenerate: { directory: '3-tayyarliqs' }`)
5. `4. تەشكىللەش باسقۇچى` (`autogenerate: { directory: '4-tashkillash' }`)
6. `5. دەۋەتچى يېتىلدۈرۈش باسقۇچى` (`autogenerate: { directory: '5-dawatchi' }`)
7. `6. يېتەكچى ئۇستاز يېتىلدۈرۈش باسقۇچى` (`autogenerate: { directory: '6-yetakchi' }`)

**Current Gap**: There is **no entry** for `2000` (`دىن ۋە ھايات (2000 سوئالغا جاۋاب)`) in `astro.config.mjs`. It must be added to the sidebar structure with nested items or autogenerate directives for `2000/00-muqeddimu`, `2000/01-etiqad`, and `2000/02-ibadet`.

### Search Integration (Pagefind)
- Starlight automatically invokes Pagefind during `astro build`.
- [`src/components/Header.astro`](file:///Users/arslan/code/derslik/src/components/Header.astro) conditionally renders `<Search />` component.
- Pagefind index is emitted to [`dist/pagefind/`](file:///Users/arslan/code/derslik/dist/pagefind/).
- UI localization for Pagefind and Starlight is provided in [`src/content/i18n/uy.json`](file:///Users/arslan/code/derslik/src/content/i18n/uy.json) (e.g. `"search.label": "ئىزدەش"`).

---

## 3. Content Collections Setup

[`src/content.config.ts`](file:///Users/arslan/code/derslik/src/content.config.ts) follows the modern Astro 5 Content Layer pattern:
```typescript
import { defineCollection } from 'astro:content';
import { docsLoader, i18nLoader } from '@astrojs/starlight/loaders';
import { docsSchema, i18nSchema } from '@astrojs/starlight/schema';

export const collections = {
  docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }),
  i18n: defineCollection({ loader: i18nLoader(), schema: i18nSchema() }),
};
```
- No custom content collection schemas exist.
- All docs pages live under `src/content/docs/` and conform to `docsSchema()` (supporting `title`, `description`, `sidebar.order`, `sidebar.label`, `tableOfContents`, etc.).

---

## 4. Existing Content Structure under `src/content/docs/`

### File Tree & Hierarchy
```
src/content/docs/
├── 1-osmurler/
├── 2-yashlar/
├── 3-tayyarliqs/
├── 4-tashkillash/
├── 5-dawatchi/
├── 6-yetakchi/
├── 2000/
│   ├── index.mdx                      # Portal landing page (links to 01-etiqad & 02-ibadet)
│   ├── 01-etiqad/
│   │   ├── 01-din-ve-etiqad.mdx       # Q1–34 (corrupted word order)
│   │   ├── 02-allahqa-iman.mdx        # Q35–48 (corrupted word order)
│   │   ├── 03-allahning-isimliri.mdx  # Q49–62 (corrupted; missing 99 Names table)
│   │   ├── 04-rohiy-alemler.mdx       # Q63–82 (corrupted word order)
│   │   ├── 05-kitablar-peyghemberler.mdx # Q83–99 (corrupted; missing Q100-115)
│   │   ├── 06-qaza-qeder.mdx          # 168 bytes (empty stub)
│   │   └── 07-qiyamet-axiret.mdx      # 206 bytes (empty stub)
│   └── 02-ibadet/
│       ├── 01-ibadet-esasliri.mdx     # 180 bytes (empty stub)
│       ├── ... (stubs 02 through 05)
│       ├── 06-namaz-ehkamliri.mdx     # 866 bytes (contains ONLY Q337)
│       └── ... (stubs 07 through 14)
├── en/                                # English translations mirror
├── 404.mdx
├── index.mdx
└── introduction.mdx
```

### Critical Findings & Text Quality Audit
1. **Scrambled Word Order in Existing Files**:
   - In [`01-din-ve-etiqad.mdx:12`](file:///Users/arslan/code/derslik/src/content/docs/2000/01-etiqad/01-din-ve-etiqad.mdx):
     ```html
     <span class="qa-label">سوئال:</span> بولغان؟ پەیدا نەدىن ئىنسانلار
     ```
     Correct Uyghur order: `ئىنسانلار نەدىن پەيدا بولغان؟`
   - In [`02-allahqa-iman.mdx:12`](file:///Users/arslan/code/derslik/src/content/docs/2000/01-etiqad/02-allahqa-iman.mdx):
     ```html
     <span class="qa-label">سوئال:</span> كﭔرەك؟ كەلتۆرۈش ئىمان قانداق ئاللاھقا
     ```
     Correct Uyghur order: `ئاللاھقا قانداق ئىمان كەلتۈرۈش كېرەك؟`
   - Cause: PyMuPDF's default `.get_text()` returns words in visual LTR order for right-to-left layout streams. The previous parser processed this without re-ordering words per line.
2. **Missing Divisions**:
   - `src/content/docs/2000/00-muqeddimu/` does not exist at all (needs book dedication, author biography Muhammad Yusuf Muhammad Tursun, and foreword).
   - In `01-etiqad/`, questions 100 to 163 are missing.
   - In `02-ibadet/`, questions 164 to 647 are missing (except lone Q337).
3. **Missing 99 Names Table**:
   - Pages 56–69 of the source PDF contain the 99 Names of Allah with Arabic Name, Pronunciation, and Uyghur Meaning. This is completely missing from `03-allahning-isimliri.mdx`.
4. **Header/Footer Pollution**:
   - Running page headers from the PDF (e.g. `ئىشلار بولىدىغان كۆنىدە قىیامەت`, `ئﭔتىقاد :بۈلۆم-1`) leaked directly into question answers.

---

## 5. Option B: "Continuous Reading Cards Layout" Styling Analysis

### Definition & Design Intent
As defined in the project architecture (`/Users/arslan/.gemini/antigravity/brain/4cef4897-f493-4acb-b5ac-2ecb06b0aee7/implementation_plan.md:95`):
- **Option B (Continuous Reading Layout)**:
  - Questions and answers are displayed sequentially as distinct cards/callouts.
  - Readers can read straight through without clicking to expand (unlike Option A accordions).
  - All text remains open in DOM for instant browser Ctrl+F and Pagefind search indexing.

### Current Codebase State
- The MDX files attempt to use HTML tags:
  ```html
  <div class="qa-card" id="q1">
    <div class="qa-question">
      <span class="qa-number">1</span>
      <span class="qa-label">سوئال:</span> ئىنسانلار نەدىن پەيدا بولغان؟
    </div>
    <div class="qa-answer">
      <span class="qa-label">جاۋاب:</span> ئىنسانلار ئاللاھ تەرىپىدىن يارىتىلغان.
    </div>
  </div>
  ```
- **CSS Status**: There is **no CSS** defined anywhere in the project for `.qa-card`, `.qa-question`, `.qa-number`, `.qa-label`, or `.qa-answer`. They currently display as unstyled, borderless block elements.

### Comparison with Existing Starlight Components
1. **Starlight `<Card>`** ([`Card.astro`](file:///Users/arslan/code/derslik/node_modules/@astrojs/starlight/dist/user-components/Card.astro)):
   - Designed for grid boxes in `<CardGrid>`. Uses fixed 4-color cycling border styles and small padding. Not suited for full-width sequential reading cards.
2. **Starlight `<Aside>`** ([`Aside.astro`](file:///Users/arslan/code/derslik/node_modules/@astrojs/starlight/dist/user-components/Aside.astro)):
   - Uses `border-inline-start: 0.25rem solid var(--sl-color-asides-border)` with soft background tint (`var(--sl-color-blue-low)`). Highly readable for RTL.
3. **Custom `StageCard.astro`** ([`StageCard.astro`](file:///Users/arslan/code/derslik/src/components/StageCard.astro)):
   - Contains navigation card styling with hover shadows and absolute anchor overlay.

### Implementation Recommendation for Option B
Add dedicated CSS classes directly to [`src/styles/custom.css`](file:///Users/arslan/code/derslik/src/styles/custom.css) (within `@layer starlight.components` or `:root`):

```css
/* Option B: Continuous Reading QA Cards */
.qa-card {
  position: relative;
  margin-block: 1.75rem;
  border-radius: 0.5rem;
  border: 1px solid var(--sl-color-gray-5);
  background-color: var(--sl-color-black);
  padding: 1.25rem 1.5rem;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  scroll-margin-top: calc(var(--sl-nav-height) + 1rem);
}

:root[data-theme='light'] .qa-card {
  background-color: var(--sl-color-gray-7, #fbfcfe);
  border-color: var(--sl-color-gray-5);
}

.qa-card:hover {
  border-color: var(--sl-color-accent);
}

.qa-question {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  font-size: var(--sl-text-h4);
  font-weight: 600;
  color: var(--sl-color-white);
  line-height: var(--sl-line-height-headings);
  border-bottom: 1px solid var(--sl-color-gray-6);
  padding-bottom: 0.75rem;
  margin-bottom: 0.75rem;
}

:root[data-theme='light'] .qa-question {
  color: var(--sl-color-gray-1);
}

.qa-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 2rem;
  height: 2rem;
  padding: 0 0.5rem;
  border-radius: 9999px;
  background-color: var(--sl-color-accent-low);
  color: var(--sl-color-accent-high);
  font-weight: 700;
  font-size: var(--sl-text-sm);
  flex-shrink: 0;
}

.qa-label {
  color: var(--sl-color-accent);
  font-weight: 700;
}

.qa-answer {
  font-size: var(--sl-text-body);
  line-height: 1.8;
  color: var(--sl-color-gray-2);
}

:root[data-theme='light'] .qa-answer {
  color: var(--sl-color-gray-2);
}

/* Quranic verse quotes within answers */
.qa-answer blockquote {
  margin-block: 1rem;
  padding-inline-start: 1.25rem;
  border-inline-start: 3px solid var(--sl-color-accent);
  font-style: normal;
  color: var(--sl-color-text-accent);
}
```

This guarantees:
- Fast loading with zero extra JS runtime.
- Seamless RTL layout (all logical properties like `padding-inline-start`, `border-inline-start`).
- Deep linking capability (anchors via `id="q{number}"` with proper `scroll-margin-top`).
- Full compatibility with Pagefind indexing.

---

## 6. Actionable Implementation Roadmap

| Milestone | Target | Key Deliverables |
|---|---|---|
| **M1: Extraction & Normalization Script** | `scripts/process_2000.py` | PyMuPDF logical RTL line reconstruction (reversing word streams per line), Unicode normalizer (`\u066e` $\to$ `ى`, `\u067b` $\to$ `ې`, `\u06cc` $\to$ `ي`, removing interior tatweels `\u0640`), header/footer cleaner. |
| **M2: 00-muqeddimu Generation** | `src/content/docs/2000/00-muqeddimu/` | `01-heqqide.mdx` (author bio, dedication, book stats), `02-kirish.mdx` (foreword). |
| **M3: 01-etiqad & 99 Names** | `src/content/docs/2000/01-etiqad/` | Q1 to Q163 properly formatted in Option B cards, 99 Names of Allah responsive table in `03-allahning-isimliri.mdx`. |
| **M4: 02-ibadet Generation** | `src/content/docs/2000/02-ibadet/` | Q164 to Q647 across 14 topical files with clean Option B cards. |
| **M5: Starlight Navigation & Styling** | `astro.config.mjs`, `custom.css` | Add `2000` sidebar group; add Option B `.qa-card` CSS rules. |
| **M6: Verification & Search Indexing** | Root project | `pnpm build` verification; inspect `dist/pagefind/` and `dist/2000/`. |
