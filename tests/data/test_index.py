from unittest.mock import MagicMock, patch
import pytest
import os
import json
from app.models.schemes import Scheme
from app.data.index import SchemeIndex, generate_embeddings


def test_empty_input_validation():
    # Empty string for generate_embeddings should raise ValueError
    with pytest.raises(ValueError, match="Input text cannot be empty"):
        generate_embeddings("")

    with pytest.raises(ValueError, match="Input text cannot be empty"):
        generate_embeddings([])


@patch("app.data.index.genai.Client")
def test_caching_behavior(mock_client_class, tmp_path):
    # Setup mock client and response
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client

    mock_emb1 = MagicMock()
    mock_emb1.values = [0.1, 0.2, 0.3]
    mock_emb2 = MagicMock()
    mock_emb2.values = [0.4, 0.5, 0.6]

    mock_response = MagicMock()
    mock_response.embeddings = [mock_emb1, mock_emb2]
    mock_client.models.embed_content.return_value = mock_response

    # Setup dummy schemes
    scheme1 = Scheme(
        id="pm-kisan",
        name="PM Kisan",
        description="Central landholder scheme",
        level="central",
        eligibility_rules=[],
        required_documents=[],
    )
    scheme2 = Scheme(
        id="pm-poshan",
        name="PM Poshan",
        description="Midday meal scheme",
        level="central",
        eligibility_rules=[],
        required_documents=[],
    )
    schemes = [scheme1, scheme2]

    cache_file = tmp_path / "embeddings_cache.json"

    # First call: cache does not exist, should call Gemini embedding API
    index = SchemeIndex(cache_path=str(cache_file))
    index.build_index(schemes)

    assert mock_client.models.embed_content.call_count == 1
    assert os.path.exists(cache_file)

    # Verify cache content structure
    with open(cache_file, "r") as f:
        cache_data = json.load(f)
    assert "pm-kisan" in cache_data
    assert cache_data["pm-kisan"] == [0.1, 0.2, 0.3]

    # Reset mock call count
    mock_client.models.embed_content.reset_mock()

    # Second call: index built again with same cache, should NOT call Gemini API
    new_index = SchemeIndex(cache_path=str(cache_file))
    new_index.build_index(schemes)

    assert mock_client.models.embed_content.call_count == 0


@patch("app.data.index.genai.Client")
def test_similarity_ranking(mock_client_class, tmp_path):
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client

    # We will seed the cache file directly to bypass API call and define exact embeddings
    cache_file = tmp_path / "embeddings_cache.json"

    # Seed embeddings:
    # Scheme 1 (farming): [1.0, 0.0]
    # Scheme 2 (education): [0.0, 1.0]
    cache_content = {"pm-kisan": [1.0, 0.0], "scholarship": [0.0, 1.0]}
    with open(cache_file, "w") as f:
        json.dump(cache_content, f)

    scheme1 = Scheme(
        id="pm-kisan",
        name="PM Kisan",
        description="Farming scheme",
        level="central",
        eligibility_rules=[],
        required_documents=[],
    )
    scheme2 = Scheme(
        id="scholarship",
        name="National Scholarship",
        description="Student scheme",
        level="central",
        eligibility_rules=[],
        required_documents=[],
    )
    schemes = [scheme1, scheme2]

    # Setup mock query embedding:
    # Query "farmer support" should be close to [1.0, 0.0]
    mock_query_emb = MagicMock()
    mock_query_emb.values = [0.9, 0.1]
    mock_response = MagicMock()
    mock_response.embeddings = [mock_query_emb]
    mock_client.models.embed_content.return_value = mock_response

    index = SchemeIndex(cache_path=str(cache_file))
    index.build_index(schemes)

    # Search for "farmer support"
    results = index.search(query="farmer support", k=2)

    assert len(results) == 2
    # First result should be pm-kisan
    assert results[0][0].id == "pm-kisan"
    # Similarity score should be positive and close to cosine of [0.9, 0.1] & [1.0, 0.0] (approx 0.99)
    assert 0.9 < results[0][1] <= 1.0

    # Second result should be scholarship
    assert results[1][0].id == "scholarship"
    assert results[1][1] < 0.2
