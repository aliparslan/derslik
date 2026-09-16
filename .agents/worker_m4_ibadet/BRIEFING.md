# BRIEFING — 2026-09-15T05:55:00Z

## Mission
Generate the 14 MDX documentation pages under `src/content/docs/2000/02-ibadet/` using verified data in `tools/extracted_2000.json` (Questions 164 to 647).

## 🔒 My Identity
- Archetype: Section 02 (Ibadet) Content Worker
- Roles: implementer, qa, specialist
- Working directory: /Users/arslan/code/derslik/.agents/worker_m4_ibadet
- Original parent: 402b5da9-8a97-44a9-a924-d815f3a13527
- Milestone: m4_ibadet

## 🔒 Key Constraints
- Exclusively own all files inside `src/content/docs/2000/02-ibadet/`. DO NOT touch any other directory or file.
- No dummy/facade implementations, genuine extraction from `tools/extracted_2000.json`.
- Zero legacy glyphs (`\u066e`, `\u067b`).
- Card format: Option B continuous reading card styling with classes `qa-card`, `qa-question`, `qa-number`, `qa-text`, `qa-answer`.
- Valid YAML frontmatter (`title`, `description`).
- Handoff report in `/Users/arslan/code/derslik/.agents/worker_m4_ibadet/handoff.md`.
- Send completion message to parent when done.

## Current Parent
- Conversation ID: 402b5da9-8a97-44a9-a924-d815f3a13527
- Updated: not yet

## Task Summary
- **What to build**: 14 MDX files covering Q164-Q647:
  1. `01-ibadet-esasliri.mdx`: Q164-Q183
  2. `02-sheriy-atalghular.mdx`: Q184-Q204
  3. `03-pakizliq-taharet.mdx`: Q205-Q248
  4. `04-ayallar-ehkami.mdx`: Q249-Q259
  5. `05-ghusli-teyemmum.mdx`: Q260-Q274
  6. `06-namaz-ehkamliri.mdx`: Q275-Q332
  7. `07-namaz-tertibi.mdx`: Q333-Q393
  8. `08-jamaet-jume.mdx`: Q394-Q428
  9. `09-bashqa-namazlar.mdx`: Q429-Q477
  10. `10-jinaza-qebre.mdx`: Q478-Q506
  11. `11-zakat.mdx`: Q507-Q553
  12. `12-roza-ramizan.mdx`: Q554-Q607
  13. `13-hej-omre.mdx`: Q608-Q634
  14. `14-sawab-gunah.mdx`: Q635-Q647
- **Success criteria**: Valid MDX, clean frontmatter, proper QA card structure, no legacy glyphs, passing build/verification.

## Change Tracker
- **Files modified**: None yet.
- **Build status**: Pending.
- **Pending issues**: None.

## Quality Status
- **Build/test result**: Pending.
- **Lint status**: Clean.
- **Tests added/modified**: None yet.

## Loaded Skills
- None specified.

## Key Decisions Made
- Use python or node script to extract directly from `tools/extracted_2000.json` or do structured file writes adhering exactly to the schema and formatting requirements.

## Artifact Index
- `.agents/worker_m4_ibadet/DISPATCH.md` — Assignment instructions
- `.agents/worker_m4_ibadet/BRIEFING.md` — Agent state and briefing
- `.agents/worker_m4_ibadet/progress.md` — Progress tracker
