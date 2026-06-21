import pytest
import json
from unittest.mock import patch, mock_open

from app.data.loader import load_schemes, normalize_scheme


def test_loader_file_not_found():
    """Assert that attempting to load a non-existent dataset raises a FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_schemes("non_existent_file.json")


def test_normalize_schema_valid():
    """Assert that a mock raw scheme dictionary is correctly transformed into the normalized dictionary."""
    raw_data = {
        "id": "123",
        "scheme_name": "Test Scheme",
        "level": "central",
        "eligibility_criteria": "Age 18-60",
        "documents_required": "Aadhar",
        "url": "http://example.com",
    }

    normalized = normalize_scheme(raw_data)

    assert normalized["id"] == "123"
    assert normalized["name"] == "Test Scheme"
    assert normalized["level"] == "central"
    assert normalized["eligibility_rules"] == ["Age 18-60"]
    assert normalized["required_documents"] == ["Aadhar"]
    assert normalized["apply_url"] == "http://example.com"


def test_normalize_schema_missing_fields():
    """Assert that missing fields in the raw data safely default to empty lists or strings without crashing."""
    raw_data = {"id": "124"}

    normalized = normalize_scheme(raw_data)

    assert normalized["id"] == "124"
    assert normalized["name"] == ""
    assert normalized["level"] == ""
    assert normalized["eligibility_rules"] == []
    assert normalized["required_documents"] == []
    assert normalized["apply_url"] == ""


@patch("os.path.exists", return_value=True)
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data=json.dumps(
        [
            {
                "id": "1",
                "scheme_name": "Mock Scheme",
                "level": "state",
                "eligibility_criteria": "Test rule 1; Test rule 2",
                "documents_required": "Doc 1; Doc 2",
                "url": "http://test.com",
            }
        ]
    ),
)
def test_load_schemes(mock_file, mock_exists):
    """Assert that the main loader successfully loads and normalizes the bundled dataset."""
    schemes = load_schemes("dummy.json")

    assert len(schemes) == 1
    assert schemes[0]["id"] == "1"
    assert schemes[0]["name"] == "Mock Scheme"
    assert schemes[0]["level"] == "state"
    assert schemes[0]["eligibility_rules"] == ["Test rule 1", "Test rule 2"]
    assert schemes[0]["required_documents"] == ["Doc 1", "Doc 2"]
    assert schemes[0]["apply_url"] == "http://test.com"
