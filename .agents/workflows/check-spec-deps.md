---
name: check-spec-deps
description: Verify all prerequisite specs for a given SchemeWayfinder spec are implemented and their tests pass before starting it.
---

# /check-spec-deps — Verify prerequisites

Input: a spec id (e.g., `S4.1`).

## Step 1: Resolve Spec

1. Read `roadmap.md` and find the row for the given spec
2. Extract the **Depends On** column (e.g., "S1.3, S2.2")
3. If "—" or empty → report "No dependencies — ready to implement" and stop

## Step 2: For Each Dependency Spec

For each dependency spec ID (e.g., S1.3):

### 2a. Check roadmap status
- Read the spec's row in `roadmap.md` → check Status column
- If not `done`: flag as **BLOCKING**

### 2b. Check code file exists
- Read the spec's **Location** column (e.g., `app/data/index.py`)
- Glob for the file — if missing: flag as **BLOCKING**

### 2c. Check test file exists
- Glob for `tests/**/test_*.py` files that correspond to the code location
- If no matching test file: flag as **WARNING** (some specs like data/skill/doc files may have none)

### 2d. Check tests pass
- If test file exists, run: `python -m pytest {test_file} -v --tb=short -q`
- If tests fail: flag as **BLOCKING**

## Step 3: Report

Print a summary table:

```
Dependency Check for {spec_id}
─────────────────────────────
| Dep   | Status  | Code | Tests  | Result   |
|-------|---------|------|--------|----------|
| S1.3  | done    | ✓    | ✓ 5/5  | READY    |
| S2.2  | pending | ✓    | ✗ 2/4  | BLOCKING |
```

Final verdict:
- **READY**: All deps satisfied → safe to implement
- **BLOCKED**: List which deps need work first, in dependency order
