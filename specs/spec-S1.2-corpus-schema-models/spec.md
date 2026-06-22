# Specification — S1.2: Corpus schema + models

## Overview
Define the core Pydantic models for SchemeWayfinder: `Scheme`, `EligibilityRule`, `CitizenProfile`, and `MatchResult`. These models establish the data structures and runtime validations required for profile intake, scheme representation, and matcher/auditor operations.

## Dependencies
- **Technical/Logical**: [S1.1: Scheme corpus loader](file:///Users/nishantgaurav/Project/schemewayfinder/specs/spec-S1.1-scheme-corpus-loader/spec.md)

## Target Location
- [app/models/schemes.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/models/schemes.py)
- [tests/models/test_schemes.py](file:///Users/nishantgaurav/Project/schemewayfinder/tests/models/test_schemes.py)

## Functional Requirements (FRs)

### **FR1**: `EligibilityRule` Pydantic Model
- **Inputs**:
  - `field`: `str` (the attribute to check in the profile, e.g., "age", "income")
  - `operator`: `str` (supported operators: `>=`, `<=`, `==`, `in`, `contains`)
  - `value`: `Any` (the target value or criteria to evaluate against)
  - `explanation`: `str` (plain-language explanation of what this rule expects)
- **Outputs**: Instantiated Pydantic model representation of the eligibility rule.
- **Edge Cases**:
  - `operator` must be one of the supported operators. Any other value must raise a `ValidationError`.

### **FR2**: `Scheme` Pydantic Model
- **Inputs**:
  - `id`: `str` (unique slug, e.g., "pm-kisan")
  - `name`: `str`
  - `description`: `str`
  - `level`: `str` (must be either "central" or "state")
  - `state`: `Optional[str]` (required if level is "state")
  - `eligibility_rules`: `List[EligibilityRule]` (defaults to empty list)
  - `required_documents`: `List[str]` (defaults to empty list)
  - `apply_url`: `Optional[str]` (defaults to `None`)
- **Outputs**: Instantiated `Scheme` Pydantic model.
- **Edge Cases**:
  - Custom validator: If `level` is "state", `state` must not be `None` or empty. If level is "central", `state` must be `None` or empty.

### **FR3**: `CitizenProfile` Pydantic Model
- **Inputs**:
  - `age`: `int` (must be greater than 0)
  - `income`: `float` (must be greater than or equal to 0)
  - `state`: `str`
  - `category`: `str` (caste/category list, e.g., "General", "OBC", "SC", "ST")
  - `disability`: `bool`
  - `occupation`: `Optional[str]`
- **Outputs**: Instantiated `CitizenProfile` model.
- **Edge Cases**:
  - Custom validators: `age` must be positive. `income` must be non-negative.

### **FR4**: `MatchResult` Pydantic Model
- **Inputs**:
  - `scheme_id`: `str`
  - `is_eligible`: `bool`
  - `matched_rules`: `List[EligibilityRule]`
  - `failed_rules`: `List[EligibilityRule]`
  - `overall_score`: `float`
- **Outputs**: Instantiated `MatchResult` model.
- **Edge Cases**:
  - Custom validator: `overall_score` must be between `0.0` and `1.0` inclusive.

---

## Tangible Outcomes
- Pydantic models implemented at [app/models/schemes.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/models/schemes.py).
- Unit tests written at [tests/models/test_schemes.py](file:///Users/nishantgaurav/Project/schemewayfinder/tests/models/test_schemes.py).

## Test-Driven Requirements (TDD)
1. **`test_eligibility_rule_validation`**:
   - Assert `ValidationError` is raised when operator is not in `[">=", "<=", "==", "in", "contains"]`.
2. **`test_scheme_state_validation`**:
   - Assert `ValidationError` is raised when level is `"state"` but `state` is missing or `None`.
   - Assert validation passes when level is `"central"` and `state` is `None`.
3. **`test_citizen_profile_bounds`**:
   - Assert `ValidationError` is raised when `age <= 0`.
   - Assert `ValidationError` is raised when `income < 0`.
4. **`test_match_result_score_bounds`**:
   - Assert `ValidationError` is raised when `overall_score < 0.0` or `overall_score > 1.0`.
