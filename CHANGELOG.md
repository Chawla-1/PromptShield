# Changelog

All notable changes to the **PromptShield** project since Milestone 1 are documented in this file.

## [Milestone 2] - 2026-11-23

### Added
- **Repository Structure**: Organized files according to Milestone 2 requirements (`prompts/`, `code/`, `test-data/`, `docs/`, `attacks/`, `results/`).
- **Prompt Versions**: Saved prompt iteration files in `prompts/v1/`, `prompts/v2/`, `prompts/v3/`, and `prompts/final/`.
- **Final Prompt Sheet**: Created `prompts/final/prompt_sheet_final.md` documenting parameters, variables, and production examples.
- **Supporting Documentation**:
  - `docs/PromptShield_Technical_Report.md`: 2-page empirical technical report.
  - `docs/milestone_2_report_draft.md`: Complete Milestone 2 student report with all 7 required sections.
  - `docs/architecture_and_diagrams.md`: Mermaid flowcharts for RAG pipeline, system architecture, and prompt workflow.
- **Evaluation Outputs**: Aggregated 360 evaluation runs into `results/all_runs.csv` and backed up to `test-data/saved_eval_outputs.csv`.

## [Milestone 2 - Development & Experiments] - 2026-11-22

### Added
- **LLM Backend**: Integrated Google Gemini REST API in `backend.py` with automatic `.env` loading and exponential backoff retry.
- **Defense Iterations**:
  - `v0`: Baseline system prompt with secret canary token (`CANARY-7F3K9`).
  - `v1`: Hardened instructions with confidentiality directives and designated refusal template.
  - `v2`: Spotlighting defense enclosing context and query within `<untrusted>` XML tags.
- **Evaluation Benchmark Suite**:
  - 30 adversarial attacks (`attacks/attacks.json`) across direct injection, prompt extraction, and indirect injection.
  - 10 benign evaluation questions (`test-data/benign.json`).
  - Automated rule-based judge (`judge.py`).
  - Command-line evaluation harness (`run_eval.py`).
- **Web UI**: Interactive Streamlit application (`app.py`) for live human-in-the-loop red-teaming.

## [Milestone 1] - 2026-11-10

### Initial Release
- Project ideation and scoping for university policy assistant security.
- Creation of synthetic university policy knowledge corpus in `data/policy_docs/` (`exams.txt`, `fees.txt`, `hostel.txt`, `library.txt`).
- Initial naive chatbot architecture exploration.
