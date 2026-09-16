# BRIEFING — 2026-09-15T05:44:02Z

## Mission
Generate the 8 MDX documentation pages under `src/content/docs/2000/01-etiqad/` using verified data in `tools/extracted_2000.json` (Questions 1-163 and the 99 Names of Allah table).

## 🔒 My Identity
- Archetype: content_worker
- Roles: implementer, qa, specialist
- Working directory: /Users/arslan/code/derslik/.agents/worker_m3_etiqad/
- Original parent: 402b5da9-8a97-44a9-a924-d815f3a13527
- Milestone: M3 Section 01 (Etiqad & 99 Names)

## 🔒 Key Constraints
- Exclusively own files inside `src/content/docs/2000/01-etiqad/`. Do NOT touch any other directory or file.
- DO NOT CHEAT. Genuine implementation from `tools/extracted_2000.json`.
- Option B continuous reading card styling for all questions:
  `<div class="qa-card" id="q{N}">...</div>`
- Valid YAML frontmatter on each page (`title`, `description`).
- Zero legacy glyphs (`\u066e`, `\u067b`).
- 99 Names of Allah formatted as 3-column table with vocalized Arabic, pronunciation, meaning & definition.
- Build and test must pass cleanly.

## Current Parent
- Conversation ID: 402b5da9-8a97-44a9-a924-d815f3a13527
- Updated: not yet

## Task Summary
- **What to build**: 8 MDX files in `src/content/docs/2000/01-etiqad/`:
  1. `01-din-ve-etiqad.mdx`: Essays + Q1-34
  2. `02-allahqa-iman.mdx`: Q35-48 & Q49-62
  3. `03-allahning-isimliri.mdx`: 99 Names of Allah table (names_99) + introductory context & notes
  4. `04-perishtilerge-iman.mdx`: Q63-72
  5. `05-jinlar-ve-sheytanlar.mdx`: Q73-82
  6. `06-kitablar-peyghemberler.mdx`: Q83-115
  7. `07-qaza-qeder.mdx`: Q116-134
  8. `08-qiyamet-axiret.mdx`: Q135-163
- **Success criteria**: 8 files generated, formatted with Option B card styling, 0 legacy glyphs, Starlight build & tests pass, handoff report written.
- **Interface contracts**: `/Users/arslan/code/derslik/.agents/PROJECT.md`
- **Code layout**: `src/content/docs/2000/01-etiqad/`

## Key Decisions Made
- [TBD]

## Artifact Index
- `/Users/arslan/code/derslik/.agents/worker_m3_etiqad/DISPATCH.md` — Assignment dispatch
- `/Users/arslan/code/derslik/.agents/worker_m3_etiqad/BRIEFING.md` — Agent briefing & situational awareness
- `/Users/arslan/code/derslik/.agents/worker_m3_etiqad/progress.md` — Progress tracker and heartbeat
- `/Users/arslan/code/derslik/.agents/worker_m3_etiqad/handoff.md` — Final handoff report

## Change Tracker
- **Files modified**: None yet
- **Build status**: Untested
- **Pending issues**: None

## Quality Status
- **Build/test result**: Not run yet
- **Lint status**: 0
- **Tests added/modified**: TBD

## Loaded Skills
- None specified in dispatch
