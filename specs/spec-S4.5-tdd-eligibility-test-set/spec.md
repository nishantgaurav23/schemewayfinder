# Spec S4.5: TDD Eligibility Test Set

Labeled personas (farmer, widow-pension, student, PwD) with known-correct matches. Use `eval-harness` skill.

## Overview
This spec creates a deterministic evaluation harness to measure the precision and recall of the `EligibilityMatcherAgent` and the `RejectionRiskAuditorAgent`. By establishing labeled personas (e.g., a farmer, a student, a PwD), we can run bulk evaluations to ensure that scheme matching is highly accurate and that the auditor effectively flags weak/hallucinated matches before generating final reports. This is a critical technical differentiator for the project.

## Dependencies
- Logical: `S3.3` (EligibilityMatcherAgent), `S4.3` (RejectionRiskAuditorAgent)
- Technical: `pytest`

## Target Location
- [NEW] `eval/personas/`
- [NEW] `eval/scorer.py`
- [NEW] `eval/REPORT.md` (generated output)
- [MODIFY] `Makefile` (add `eval` target)

## Functional Requirements (FRs)

- **FR1: Labeled Personas Setup**
  - **Inputs**: Define 4 canonical personas (farmer, widow-pension, student, PwD) as JSON files in `eval/personas/`. Include the expected `scheme_id` matches and which ones should be rejected.
  - **Outputs**: Golden dataset for evaluation.
  - **Edge Cases**: Ensure the datasets reflect borderline eligibility cases to effectively test the Auditor.

- **FR2: Evaluation Scorer Script**
  - **Inputs**: The labeled personas and the orchestrator pipeline (Matcher + Auditor).
  - **Outputs**: `eval/scorer.py` runs the pipeline for each persona, computes Precision, Recall, and F1-score for the matched schemes vs. labels.
  - **Edge Cases**: Must track and compare results *before* the critic loop (Matcher output) and *after* the critic loop (Auditor output) to quantify the RejectionRiskAuditor's impact. Must be deterministic.

- **FR3: Report Generation**
  - **Inputs**: Output of the scorer script.
  - **Outputs**: Automatically generates `eval/REPORT.md` containing a table of metrics (Precision/Recall/F1), coverage stats, and the auditor before/after delta.

## Tangible Outcomes
1. `eval/personas/` containing at least 4 labeled JSON persona profiles.
2. `eval/scorer.py` script calculating strict Precision, Recall, and F1.
3. `make eval` command executing the scorer and writing to `eval/REPORT.md`.
4. `eval/REPORT.md` with baseline performance numbers.

## Test-Driven Requirements (TDD)
- `test_eval_scorer_precision_recall`: Verify the `scorer.py` math logic correctly calculates precision and recall given mock outputs vs. mock labels.
- `test_eval_harness_integration`: Verify `make eval` accurately executes without throwing errors on a simple dummy persona.
