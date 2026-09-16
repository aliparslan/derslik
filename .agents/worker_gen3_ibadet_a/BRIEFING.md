# BRIEFING — 2026-09-15T13:12:30Z

## Mission
Generate 2 MDX files for 2000-sualliq-eser ibadet section: 07-namaz-oqush.mdx (Q333-Q393) and 08-jamaet-jume.mdx (Q394-Q428) directly from extracted_2000.json using Option B Card markup and text normalization without running shell commands.

## 🔒 My Identity
- Archetype: implementer
- Roles: implementer, qa
- Working directory: /Users/arslan/code/derslik/.agents/worker_gen3_ibadet_a/
- Original parent: 65f8e8f1-2fca-49a7-8b3f-c817ab097747
- Milestone: 2000-sualliq ibadet content generation part A

## 🔒 Key Constraints
- DO NOT use run_command.
- Read tools/extracted_2000.json via view_file.
- Write files using write_to_file.
- Use Option B Card markup.
- Normalize legacy glyphs: \u066e -> \u0649, \u067b -> \u06d0, \u06cc -> \u064a.
- Strip interior tatweels/kashidas (\u0640) between letters.

## Current Parent
- Conversation ID: 65f8e8f1-2fca-49a7-8b3f-c817ab097747
- Updated: 2026-09-15T13:12:30Z

## Task Summary
- **What to build**:
  1. `src/content/docs/2000/02-ibadet/07-namaz-oqush.mdx`: Q333 - Q393
  2. `src/content/docs/2000/02-ibadet/08-jamaet-jume.mdx`: Q394 - Q428
- **Success criteria**: MDX files properly formatted with frontmatter, Option B card markup, normalized text, valid footnotes, covering all specified questions.

## Change Tracker
- **Files modified**:
  - `src/content/docs/2000/02-ibadet/07-namaz-oqush.mdx`: generated with 61 questions (Q333-Q393)
  - `src/content/docs/2000/02-ibadet/08-jamaet-jume.mdx`: generated with 35 questions (Q394-Q428)
- **Build status**: verified via tool checks (no legacy glyphs, complete question spans, syntax check)
- **Pending issues**: none

## Quality Status
- **Build/test result**: passed inspection
- **Lint status**: zero legacy glyphs, proper frontmatter
- **Tests added/modified**: n/a (content MDX generation)
