import json
import pytest
from eval.scorer import calculate_metrics, run_eval_harness


def test_eval_scorer_precision_recall():
    """Test precision, recall, and F1 calculations."""
    expected = {"scheme_a", "scheme_b"}

    # Perfect match
    actual = {"scheme_a", "scheme_b"}
    p, r, f1 = calculate_metrics(expected, actual)
    assert p == 1.0
    assert r == 1.0
    assert f1 == 1.0

    # Under match (Recall drop)
    actual = {"scheme_a"}
    p, r, f1 = calculate_metrics(expected, actual)
    assert p == 1.0
    assert r == 0.5
    assert f1 == (2 * 1.0 * 0.5) / (1.0 + 0.5)

    # Over match (Precision drop)
    actual = {"scheme_a", "scheme_b", "scheme_c"}
    p, r, f1 = calculate_metrics(expected, actual)
    assert p == 2 / 3
    assert r == 1.0
    assert f1 == (2 * (2 / 3) * 1.0) / ((2 / 3) + 1.0)

    # No match
    actual = {"scheme_c"}
    p, r, f1 = calculate_metrics(expected, actual)
    assert p == 0.0
    assert r == 0.0
    assert f1 == 0.0


@pytest.fixture
def dummy_persona_dir(tmp_path):
    persona_dir = tmp_path / "personas"
    persona_dir.mkdir()

    dummy = {"profile": {"age": 30}, "expected_matches": ["scheme_a"], "expected_rejections": []}

    with open(persona_dir / "dummy.json", "w") as f:
        json.dump(dummy, f)

    return persona_dir


def test_eval_harness_integration(dummy_persona_dir, monkeypatch):
    """Test the eval harness runs without throwing errors."""

    # Mock Matcher and Auditor outputs
    def mock_run_matcher(*args, **kwargs):
        return ["scheme_a", "scheme_b"]

    def mock_run_auditor(*args, **kwargs):
        return ["scheme_a"]

    monkeypatch.setattr("eval.scorer.run_matcher", mock_run_matcher)
    monkeypatch.setattr("eval.scorer.run_auditor", mock_run_auditor)

    results = run_eval_harness(personas_dir=str(dummy_persona_dir))

    assert len(results) == 1
    assert "dummy.json" in results
    assert results["dummy.json"]["before_p"] == 0.5  # scheme_a and scheme_b -> 1 / 2
    assert results["dummy.json"]["before_r"] == 1.0  # scheme_a expected and found -> 1 / 1
    assert results["dummy.json"]["after_p"] == 1.0  # scheme_a only -> 1 / 1
    assert results["dummy.json"]["after_r"] == 1.0  # scheme_a expected and found -> 1 / 1
