# BRIEFING — 2026-09-15T04:44:00Z

## Mission
Generate Section 01 (`src/content/docs/2000/01-etiqad/`, 8 MDX files: Q1–163 + 99 Names table) directly from `tools/extracted_2000.json` using Option B card markup, overwriting/replacing any legacy/reversed files.

## 🔒 My Identity
- Archetype: worker_m3_etiqad_gen2
- Roles: implementer, qa, specialist
- Working directory: /Users/arslan/code/derslik/.agents/worker_m3_etiqad_gen2
- Original parent: cb7a7160-41a4-4a29-91ad-ed9e29ae26b6
- Milestone: M3 (Section 01 Etiqad & 99 Names)

## 🔒 Key Constraints
- Exclusively owned path: `src/content/docs/2000/01-etiqad/`
- MUST NOT modify any other files in `src/content/docs/2000/`
- No cheating, no hardcoding, genuine generation
- Zero occurrences of `\u066e`, `\u067b`, or interior `\u0640`
- Generate exactly 8 MDX files in `src/content/docs/2000/01-etiqad/`
- Use Option B card markup with `.qa-card`, `.qa-question`, `.qa-answer`, `.qa-number`
- Populate 99 Names of Allah table in `03-allahning-isimliri.mdx` from `tools/extracted_2000.json`

## Current Parent
- Conversation ID: cb7a7160-41a4-4a29-91ad-ed9e29ae26b6
- Updated: 2026-09-15T04:44:00Z

## Task Summary
- **What to build**: 8 MDX files in `src/content/docs/2000/01-etiqad/` covering Q1–163 and 99 Names table
- **Success criteria**: All tests for Section 01, Q1–163, and 99 Names table pass in `python3 tests/e2e_2000.py --skip-build`
- **Interface contracts**: PROJECT.md and TEST_READY.md
- **Code layout**: `src/content/docs/2000/01-etiqad/*.mdx`

## Key Decisions Made
- Inspect existing files in `src/content/docs/2000/01-etiqad/` and clean up obsolete ones.
- Parse `tools/extracted_2000.json` to generate MDX files.

## Artifact Index
- `tools/extracted_2000.json` — Source JSON extracted from PDF
- `src/content/docs/2000/01-etiqad/` — Target MDX directory

## Change Tracker
- **Files modified**: None yet
- **Build status**: Pending
- **Pending issues**: None

## Quality Status
- **Build/test result**: Pending
- **Lint status**: N/A
- **Tests added/modified**: N/A

## Loaded Skills
- None
