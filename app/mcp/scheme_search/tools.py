import json
import re
from app.mcp.scheme_search.server import mcp
from app.models.schemes import CitizenProfile, MatchResult, EligibilityRule, Scheme
from app.data.index import SchemeIndex
from app.data.loader import load_schemes


def get_all_schemes() -> list[Scheme]:
    try:
        raw_data = load_schemes()
    except Exception:
        return []

    schemes = []
    for item in raw_data:
        desc = item.get("name", "")
        rules = []
        for criteria in item.get("eligibility_rules", []):
            criteria_lower = criteria.lower()
            if "farmer" in criteria_lower:
                rules.append(
                    EligibilityRule(
                        field="occupation",
                        operator="==",
                        value="Farmer",
                        explanation="Must be a farmer",
                    )
                )
            elif "student" in criteria_lower:
                rules.append(
                    EligibilityRule(
                        field="occupation",
                        operator="==",
                        value="Student",
                        explanation="Must be a student",
                    )
                )

            if "age" in criteria_lower:
                match = re.search(r"(\d+)\s*-\s*(\d+)", criteria_lower)
                if match:
                    rules.append(
                        EligibilityRule(
                            field="age",
                            operator=">=",
                            value=int(match.group(1)),
                            explanation=f"Must be at least {match.group(1)} years old",
                        )
                    )
                    rules.append(
                        EligibilityRule(
                            field="age",
                            operator="<=",
                            value=int(match.group(2)),
                            explanation=f"Must be at most {match.group(2)} years old",
                        )
                    )
                else:
                    match_single = re.search(r"(\d+)", criteria_lower)
                    if match_single:
                        val = int(match_single.group(1))
                        if (
                            "older" in criteria_lower
                            or "above" in criteria_lower
                            or ">" in criteria_lower
                        ):
                            rules.append(
                                EligibilityRule(
                                    field="age",
                                    operator=">=",
                                    value=val,
                                    explanation=f"Must be {val} or older",
                                )
                            )
                        elif (
                            "younger" in criteria_lower
                            or "below" in criteria_lower
                            or "<" in criteria_lower
                        ):
                            rules.append(
                                EligibilityRule(
                                    field="age",
                                    operator="<=",
                                    value=val,
                                    explanation=f"Must be {val} or younger",
                                )
                            )

            if "income" in criteria_lower:
                if "2 lakhs" in criteria_lower:
                    rules.append(
                        EligibilityRule(
                            field="income",
                            operator="<=",
                            value=200000.0,
                            explanation="Income must be below 2 Lakhs",
                        )
                    )
                else:
                    match_num = re.search(r"(\d+)", criteria_lower)
                    if match_num:
                        val = float(match_num.group(1))
                        rules.append(
                            EligibilityRule(
                                field="income",
                                operator="<=",
                                value=val,
                                explanation=f"Income must be below {val}",
                            )
                        )

        level = item.get("level", "central")
        state_val = None
        if level == "state":
            state_val = "Karnataka"

        schemes.append(
            Scheme(
                id=item.get("id"),
                name=item.get("name"),
                description=desc,
                level=level,
                state=state_val,
                eligibility_rules=rules,
                required_documents=item.get("required_documents", []),
                apply_url=item.get("apply_url") or None,
            )
        )
    return schemes


def evaluate_rule(rule: EligibilityRule, profile: CitizenProfile) -> bool:
    if not hasattr(profile, rule.field):
        return False

    val = getattr(profile, rule.field)
    op = rule.operator
    expected = rule.value

    if op == ">=":
        try:
            return float(val) >= float(expected)
        except (ValueError, TypeError):
            return False
    elif op == "<=":
        try:
            return float(val) <= float(expected)
        except (ValueError, TypeError):
            return False
    elif op == "==":
        if isinstance(val, str) and isinstance(expected, str):
            return val.lower().strip() == expected.lower().strip()
        return val == expected
    elif op == "in":
        if isinstance(expected, list):
            target_list = [str(x).lower().strip() for x in expected]
        elif isinstance(expected, str):
            target_list = [x.lower().strip() for x in expected.split(",")]
        else:
            target_list = [str(expected).lower().strip()]
        return str(val).lower().strip() in target_list
    elif op == "contains":
        if isinstance(val, list):
            return str(expected).lower().strip() in [str(x).lower().strip() for x in val]
        return str(expected).lower().strip() in str(val).lower()

    return False


@mcp.tool()
async def find_schemes(profile: dict) -> str:
    """Search for schemes matching the given CitizenProfile.

    Runs rule comparison checks and returns a JSON list of MatchResults.
    """
    try:
        citizen = CitizenProfile(**profile)
    except Exception as e:
        return json.dumps({"error": f"Invalid profile data: {str(e)}"})

    index = SchemeIndex()
    schemes = get_all_schemes()
    index.build_index(schemes)

    query_parts = []
    if citizen.occupation:
        query_parts.append(citizen.occupation)
    if citizen.state:
        query_parts.append(citizen.state)
    if citizen.category:
        query_parts.append(citizen.category)

    query = " ".join(query_parts) if query_parts else "general welfare scheme"
    candidates = index.search(query, k=5)

    match_results = []
    for scheme, _ in candidates:
        matched_rules = []
        failed_rules = []

        for rule in scheme.eligibility_rules:
            if evaluate_rule(rule, citizen):
                matched_rules.append(rule)
            else:
                failed_rules.append(rule)

        total_rules = len(scheme.eligibility_rules)
        if total_rules == 0:
            overall_score = 1.0
            is_eligible = True
        else:
            passed_count = len(matched_rules)
            overall_score = passed_count / total_rules
            is_eligible = passed_count == total_rules

        result = MatchResult(
            scheme_id=scheme.id,
            is_eligible=is_eligible,
            matched_rules=matched_rules,
            failed_rules=failed_rules,
            overall_score=overall_score,
        )
        match_results.append(result.model_dump())

    return json.dumps(match_results)


@mcp.tool()
async def get_scheme(id: str) -> str:
    """Retrieve full details of a welfare scheme by its ID.

    Returns the serialized Scheme object, or an error if not found.
    """
    cleaned_id = str(id).strip()
    if not cleaned_id:
        return json.dumps({"error": "Scheme ID cannot be empty"})

    schemes = get_all_schemes()
    for scheme in schemes:
        if scheme.id == cleaned_id:
            return json.dumps(scheme.model_dump())

    return json.dumps({"error": f"Scheme with ID '{cleaned_id}' not found"})
