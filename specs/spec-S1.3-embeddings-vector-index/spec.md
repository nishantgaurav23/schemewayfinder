# Specification — S1.3: Embeddings + vector index

## Overview
Build an embedding generator and a local vector index over the scheme eligibility corpus. To avoid latency and API costs, the embedding system must be cached locally and deterministic. This index will be used by the Eligibility Matcher agent to fetch candidate schemes matching a citizen's profile.

## Dependencies
- **Logical/Technical**:
  - [S1.1: Scheme corpus loader](file:///Users/nishantgaurav/Project/schemewayfinder/specs/spec-S1.1-scheme-corpus-loader/spec.md)
  - [S1.2: Corpus schema + models](file:///Users/nishantgaurav/Project/schemewayfinder/specs/spec-S1.2-corpus-schema-models/spec.md)

## Target Location
- [app/data/index.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/data/index.py)
- [tests/data/test_index.py](file:///Users/nishantgaurav/Project/schemewayfinder/tests/data/test_index.py)

## Functional Requirements (FRs)

### **FR1**: Embedding Generation
- **Inputs**: `text`: `str` or `List[str]`
- **Outputs**: Vector representation `List[float]` or `List[List[float]]`.
- **Edge Cases**:
  - Empty or null strings must raise `ValueError`.
  - External API calls to Gemini (e.g., `text-embedding-004`) must use Tenacity retries (3 attempts, exponential backoff) to handle transient rate limits or connection failures.

### **FR2**: Local Caching & Index Building
- **Inputs**: A list of `Scheme` objects.
- **Outputs**: A local file-based cache containing the generated embeddings mapped to scheme IDs.
- **Edge Cases**:
  - Deterministic: Check if the cache file (e.g., `app/data/corpus/embeddings_cache.json`) exists. If it does, load directly and bypass calling the external API.
  - Compute and save: If the cache is missing or schemes are updated, generate missing embeddings and write them to the cache file.

### **FR3**: Vector Search (Cosine Similarity)
- **Inputs**: `query`: `str`, `k`: `int` (default 5)
- **Outputs**: Sorted list of matching `(Scheme, score)` tuples, descending by cosine similarity score.
- **Edge Cases**:
  - Cosine similarity scores must fall strictly between `-1.0` and `1.0`.

---

## Tangible Outcomes
- Embedding search index implemented at [app/data/index.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/data/index.py).
- Local cache file generated at `app/data/corpus/embeddings_cache.json` (ignored or tracked based on git setup).
- Unit tests written at [tests/data/test_index.py](file:///Users/nishantgaurav/Project/schemewayfinder/tests/data/test_index.py).

## Test-Driven Requirements (TDD)
1. **`test_caching_behavior`**:
   - Mock the Gemini embedding API client.
   - Assert that building the index the first time makes API requests and writes a cache file.
   - Assert that building the index the second time loads from the cache file and makes **zero** API requests.
2. **`test_similarity_ranking`**:
   - Seed a mock index with 3 schemes (e.g., farming, student, senior citizen).
   - Mock embeddings such that a query "crop farming" yields the highest cosine similarity with the farming scheme.
   - Assert that the query returns the schemes in correct ranked order.
3. **`test_empty_input_validation`**:
   - Assert that passing empty strings or empty lists raises `ValueError`.
