# BRIEFING — 2026-09-15T01:46:37Z

## Mission
Build the comprehensive, opaque-box E2E test suite in `tests/e2e_2000.py` validating 4 tiers of acceptance criteria for Din ve Hayat (2000 Sualliq) Part 1 conversion.

## 🔒 My Identity
- Archetype: Test Writer
- Roles: specialist, qa
- Working directory: /Users/arslan/code/derslik/.agents/test_writer_e2e
- Original parent: 402b5da9-8a97-44a9-a924-d815f3a13527
- Milestone: E2E Testing Track

## 🔒 Key Constraints
- Write and modify test code only — never implementation code.
- Opaque-box, requirement-driven verification derived strictly from user requirements and acceptance criteria in ORIGINAL_REQUEST.md, PROJECT.md, and TEST_INFRA.md.
- Tiers 1 through 4 independent verification:
  1. Tier 1: Question count exactly 647, set(range(1, 648)) complete, question/answer structure non-empty, Section 00 (4 pages), Section 01 (8 pages, Q1-163), Section 02 (14 pages, Q164-647).
  2. Tier 2: Zero legacy glyphs (\u066e, \u067b), zero interior tatweels (\u0640) in Uyghur words, verbatim boundary integrity for Q1, Q48, Q49, Q163, Q164, Q647.
  3. Tier 3: 99 Names of Allah table in 01-etiqad/03-allahning-isimliri.mdx (exactly 99 rows, 3 columns populated), Option B CSS in custom.css, sidebar navigation in astro.config.mjs.
  4. Tier 4: Build check (pnpm build) and Pagefind search index generation in dist/pagefind/.
- Test harness must be runnable standalone via `/usr/bin/python3 tests/e2e_2000.py` with granular flags / tier selection.
- Create TEST_READY.md at project root and `.agents/TEST_READY.md`.
- Handoff report in `.agents/test_writer_e2e/handoff.md`.

## Current Parent
- Conversation ID: 402b5da9-8a97-44a9-a924-d815f3a13527
- Updated: not yet

## Task Summary
- **What to build**: Comprehensive, standalone Python E2E test harness `tests/e2e_2000.py` and `TEST_READY.md`.
- **Success criteria**: Test harness executes, parses markdown/mdx, checks all constraints across Tiers 1-4, returns clear status per tier and overall exit code.
- **Interface contracts**: /Users/arslan/code/derslik/.agents/PROJECT.md § Interface Contracts
- **Code layout**: /Users/arslan/code/derslik/.agents/PROJECT.md § Code Layout

## Key Decisions Made
- Design `tests/e2e_2000.py` with modular test classes/functions for Tiers 1-4, supporting CLI args (`--tier 1`, `--tier 2`, `--tier 3`, `--tier 4`, `--all`, `--skip-build` for fast verification when build is not yet triggered).
- Ensure robust parsing of MDX/HTML qa-card blocks, extracting question numbers from both id attributes (`id="q1"`) and span elements (`<span class="qa-number">1</span>`).
- Implement precise regex checks for legacy glyphs `\u066e`, `\u067b`, and interior tatweels `\u0640` between Uyghur characters.

## Artifact Index
- `tests/e2e_2000.py` — Standalone E2E test harness
- `TEST_READY.md` — Test suite documentation and instructions
- `.agents/test_writer_e2e/handoff.md` — Handoff report

## Loaded Skills
- None specified by orchestrator

## Quality Status
- **Build/test result**: Initializing test runner
- **Lint status**: Clean
- **Tests added/modified**: `tests/e2e_2000.py`
