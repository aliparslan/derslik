# DISPATCH — worker_remediation_2

## 2026-09-15T21:30:00Z

### Identity & Mission
You are `worker_remediation_2` (archetype: `teamwork_preview_worker`), reporting to orchestrator_7.
Your working directory is `/Users/arslan/code/derslik/.agents/worker_remediation_2/`.
You MUST read the authoritative request first:
`/Users/arslan/code/derslik/.agents/ORIGINAL_REQUEST.md`

### Reference Documents:
- Full Remediation Plan: `/Users/arslan/code/derslik/.agents/explorer_fix_2/handoff.md`
- Automated Remediation Script: `/Users/arslan/code/derslik/.agents/explorer_fix_3/apply_remediation.py`
- Forensic Audit Findings: `/Users/arslan/code/derslik/.agents/auditor_1/handoff.md`
- Gate Status: `/Users/arslan/code/derslik/.agents/orchestrator_7/GATE_STATUS.md`
- Test Harness: `/Users/arslan/code/derslik/tests/e2e_2000.py`

### Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

### File Ownership:
You have exclusive write access to:
- `src/content/docs/2000/01-etiqad/`
- `src/content/docs/2000/00-muqeddimu/04-munderije.mdx`
- `src/content/docs/2000/index.mdx`
- `tools/extracted_2000.json`
- `tools/extract_2000.py`
- `tests/e2e_2000.py`

### Assignments to Complete:
1. **Execute Remediation Script / Actions**:
   You can run `python3 .agents/explorer_fix_3/apply_remediation.py` or apply the exact changes documented in `/Users/arslan/code/derslik/.agents/explorer_fix_2/handoff.md`:
   a. **Delete 4 obsolete files** in `src/content/docs/2000/01-etiqad/`:
      - `04-rohiy-alemler.mdx`
      - `05-kitablar-peyghemberler.mdx`
      - `06-qaza-qeder.mdx`
      - `07-qiyamet-axiret.mdx`
      Verify that exactly the 8 canonical MDX files remain in `01-etiqad/`.
   b. **Update `src/content/docs/2000/00-muqeddimu/04-munderije.mdx`** with the canonical links and synchronized question ranges, and align `src/content/docs/2000/index.mdx`.
   c. **Normalize lingering Farsi yeh (`\u06cc` -> `\u064a`)** in:
      - `src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx` (lines 77, 79, 81, 108)
      - `src/content/docs/2000/01-etiqad/05-samawiy-kitablar.mdx` (line 15)
      - `src/content/docs/2000/01-etiqad/08-qiyamet-axiret.mdx` (line 65)
      - `tools/extracted_2000.json` and `tools/extract_2000.py`
   d. **Fix Name #76 in 99 Names Table**:
      In `src/content/docs/2000/01-etiqad/03-allahning-isimliri.mdx`, replace the duplicate `الصَّمَدُ` (`ئەسسەمەد`) with `السُّبُّوحُ` (`ئەسسۇببۇھ`):
      `| السُّبُّوحُ | ئەسسۇببۇھ | پۈتۈنلەي نۇقساندىن ۋە ھەر قانداق ئەيىبتىن پاك، بارلىق گۈزەل كامالىي سۈپەتلەر ئاللاھقىلا مەنسۇپ بولغان زاتتۇر. |`
      Also update `tools/extracted_2000.json` and `tools/extract_2000.py`.

2. **Enhance `tests/e2e_2000.py`**:
   Add `test_zero_farsi_yeh` to Tier 2 and distinct names check to `test_99_names_table` as specified in `/Users/arslan/code/derslik/.agents/explorer_fix_2/handoff.md`.

3. **Verify Build and Tests**:
   - Run `python3 tests/e2e_2000.py -v` and confirm 100% pass across all 4 tiers.
   - Run `pnpm build` and verify clean build with zero errors, generating `dist/2000/` and Pagefind search index.

4. **Deliver Handoff**:
   Write `/Users/arslan/code/derslik/.agents/worker_remediation_2/handoff.md` and send a message back to orchestrator_7.
