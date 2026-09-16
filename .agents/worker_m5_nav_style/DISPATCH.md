## 2026-09-15T05:44:02Z

Your identity: Starlight Navigation & Styling Worker
Working directory: /Users/arslan/code/derslik/.agents/worker_m5_nav_style/
Parent conversation ID: 402b5da9-8a97-44a9-a924-d815f3a13527

MANDATORY FIRST STEP: Read the full verbatim requirements at:
/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md
Also read:
- /Users/arslan/code/derslik/.agents/PROJECT.md
- /Users/arslan/code/derslik/.agents/explorer_survey_codebase/analysis.md
- /Users/arslan/code/derslik/.agents/TEST_READY.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

File Write Boundaries:
You exclusively own:
- `/Users/arslan/code/derslik/astro.config.mjs`
- `/Users/arslan/code/derslik/src/styles/custom.css`
- `/Users/arslan/code/derslik/src/content/docs/2000/index.mdx`
DO NOT touch any other directory or file.

Your objective:
1. `src/styles/custom.css`:
   Add Option B continuous reading cards styling using RTL logical properties as designed in Codebase Explorer's analysis:
   - `.qa-card`: card wrapper with border, border-radius, background, margin-bottom, padding, transition, and hover box-shadow.
   - `.qa-question`: bold question line with border-inline-start accent border, margin-bottom, color.
   - `.qa-number`: highlighted badge/pill for the question number with background color, border-radius, padding, margin-inline-end.
   - `.qa-text`: question text styling.
   - `.qa-answer`: clean answer text with line-height and Uyghur font compatibility.
   - Responsive table styling for the 99 Names of Allah table.
2. `astro.config.mjs`:
   Update Starlight sidebar configuration to add a dedicated navigation group for `2000 سوئال-جاۋاب`:
   - Group label: `2000 سوئال-جاۋاب`
   - Link / overview: `2000/index`
   - Nested group: `00-مۇقەددىمە` linking to all 4 pages under `2000/00-muqeddimu/`
   - Nested group: `01-ئېتىقاد (1–163)` linking to all 8 pages under `2000/01-etiqad/`
   - Nested group: `02-ئىبادەت (164–647)` linking to all 14 pages under `2000/02-ibadet/`
   Ensure existing stage items (`1-osmurler` through `6-yetakchi`) remain intact.
3. `src/content/docs/2000/index.mdx`:
   Create the main portal page for `2000 سوئال-جاۋاب`:
   - Title: `دىن ۋە ھايات (2000 سوئالغا جاۋاب)`
   - Introduction to the book, author, and structure of Part 1.
   - Navigation links/cards pointing to `00-muqeddimu/`, `01-etiqad/`, and `02-ibadet/`.

Write your handoff report to `/Users/arslan/code/derslik/.agents/worker_m5_nav_style/handoff.md`.
Send a completion message back to parent when done.
