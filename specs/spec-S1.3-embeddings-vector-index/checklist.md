# Checklist — S1.3: Embeddings + vector index

This checklist tracks the implementation of S1.3.

- [x] **Phase 1: Setup & Dependencies**
  - [x] Add `google-genai` and `tenacity` (or relevant SDK dependencies if using Vertex/Google AI Studio) to `pyproject.toml` dependencies if not already present.
  - [x] Sync dependencies in the virtual environment.
- [x] **Phase 2: Tests First (TDD)**
  - [x] Create test file at `tests/data/test_index.py`.
  - [x] Write `test_empty_input_validation` to verify input sanity checks.
  - [x] Write `test_caching_behavior` mocking the embedding API to verify it reads from cache on subsequent calls.
  - [x] Write `test_similarity_ranking` to verify cosine similarity ranking matches expectations.
  - [x] Run `.venv/bin/pytest tests/data/test_index.py` and confirm tests fail (Red).
- [x] **Phase 3: Implementation**
  - [x] Implement embedding generator in [app/data/index.py](file:///Users/nishantgaurav/Project/schemewayfinder/app/data/index.py) using Gemini APIs with Tenacity retries.
  - [x] Implement caching mechanism to write/read from local cache file (`app/data/corpus/embeddings_cache.json`).
  - [x] Implement cosine similarity vector search logic.
- [x] **Phase 4: Integration**
  - [x] Run `.venv/bin/pytest tests/data/test_index.py` and verify all tests pass (Green).
  - [x] Run the complete test suite to ensure no regressions.
- [x] **Phase 5: Verification**
  - [x] Run `ruff check` and `ruff format` on the new files.
  - [x] Verify no secrets (API keys) are checked in.
  - [x] Update `roadmap.md` status to `done` for S1.3.
