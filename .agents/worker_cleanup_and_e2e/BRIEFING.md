# BRIEFING — 2026-09-15T17:10:13Z

## Mission
Cleanup obsolete skeleton files in `src/content/docs/2000/01-etiqad/`, confirm canonical 8 files, run full 4-tier E2E tests and `pnpm build`, fix any issues, and produce handoff report.

## 🔒 My Identity
- Archetype: worker
- Roles: implementer, qa, specialist
- Working directory: `/Users/arslan/code/derslik/.agents/worker_cleanup_and_e2e/`
- Original parent: cb463600-d33e-4888-b751-c418ef73c451
- Milestone: E2E Verification & Cleanup

## 🔒 Key Constraints
- DO NOT CHEAT. All implementations must be genuine.
- Remove obsolete skeleton files: 04-rohiy-alemler.mdx, 05-kitablar-peyghemberler.mdx, 06-qaza-qeder.mdx, 07-qiyamet-axiret.mdx.
- Exactly 8 canonical MDX files in src/content/docs/2000/01-etiqad/.
- Full 4-tier E2E test `python3 tests/e2e_2000.py -v` must pass.
- `pnpm build` must succeed with zero errors and generate `dist/pagefind/`.

## Current Parent
- Conversation ID: cb463600-d33e-4888-b751-c418ef73c451
- Updated: 2026-09-15T17:10:13Z

## Task Summary
- **What to build/cleanup**: Remove 4 obsolete files from `src/content/docs/2000/01-etiqad/`, run e2e_2000.py and pnpm build, fix defects if any.
- **Success criteria**: 8 canonical files present, all 4-tier E2E tests pass, pnpm build succeeds with dist/pagefind/ generated, handoff.md written.
- **Interface contracts**: `/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md`, `/Users/arslan/code/derslik/.agents/TEST_READY.md`
- **Code layout**: `src/content/docs/2000/01-etiqad/`, `tests/e2e_2000.py`

## Change Tracker
- **Files modified**: None yet
- **Build status**: Untested
- **Pending issues**: None

## Quality Status
- **Build/test result**: Untested
- **Lint status**: Untested
- **Tests added/modified**: tests/e2e_2000.py will be executed

## Key Decisions Made
- Proceed with verification of current state before making any modifications.

## Artifact Index
- `/Users/arslan/code/derslik/.agents/worker_cleanup_and_e2e/handoff.md` — Final handoff report
