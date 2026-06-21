---
name: eval-harness
description: Add a labeled persona test case and scorer entry to the SchemeWayfinder eval set, and run the eligibility precision/recall + rejection-risk auditor before/after report. Use for any eligibility or auditor change.
---

# Skill: eval-harness

When asked to evaluate eligibility or the auditor:

1. Add labeled personas under `eval/personas/` — each: a `CitizenProfile` + the known-correct set of scheme IDs (and which should be flagged weak/rejection-risk).
2. In `eval/scorer.py`, compute precision / recall / F1 of matched schemes vs. the labels, and the rejection-risk auditor's effect (matches before vs. after the critic loop).
3. Write results to `eval/REPORT.md`: a table of metrics, coverage (schemes indexed, languages tested), and the auditor before/after delta.
4. Keep it deterministic (fixed seed, cached embeddings) so numbers are reproducible.
5. Run via `make eval`.

Output: new persona(s), scorer updates, and a regenerated REPORT.md with hard numbers. This is the submission's technical differentiator — favor real metrics over adjectives.
