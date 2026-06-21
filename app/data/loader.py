import json
import os
from typing import List, Dict, Any

DEFAULT_CORPUS_PATH = os.path.join(os.path.dirname(__file__), "corpus", "sample.json")


def normalize_scheme(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes raw scheme dictionary into the canonical SchemeWayfinder schema.
    """

    def _parse_list_string(val: Any) -> List[str]:
        if not val or not isinstance(val, str):
            return []
        return [item.strip() for item in val.split(";") if item.strip()]

    return {
        "id": str(raw_data.get("id", "")),
        "name": str(raw_data.get("scheme_name", "")),
        "level": str(raw_data.get("level", "")),
        "eligibility_rules": _parse_list_string(raw_data.get("eligibility_criteria", "")),
        "required_documents": _parse_list_string(raw_data.get("documents_required", "")),
        "apply_url": str(raw_data.get("url", "")),
    }


def load_schemes(filepath: str = DEFAULT_CORPUS_PATH) -> List[Dict[str, Any]]:
    """
    Loads and normalizes the dataset from the given JSON filepath.
    Defaults to the bundled corpus if no path is provided.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        raw_schemes = json.load(f)

    return [normalize_scheme(scheme) for scheme in raw_schemes]
