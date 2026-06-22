from typing import List, Tuple, Dict, Any, Union
import os
import json
import math
from google import genai
from tenacity import retry, stop_after_attempt, wait_exponential
from app.models.schemes import Scheme


def dot_product(v1: List[float], v2: List[float]) -> float:
    return sum(x * y for x, y in zip(v1, v2))


def magnitude(v: List[float]) -> float:
    return math.sqrt(sum(x * x for x in v))


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    m1 = magnitude(v1)
    m2 = magnitude(v2)
    if m1 == 0 or m2 == 0:
        return 0.0
    return dot_product(v1, v2) / (m1 * m2)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _call_embedding_api(client: genai.Client, model: str, contents: Any) -> Any:
    return client.models.embed_content(model=model, contents=contents)


def generate_embeddings(texts: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
    if not texts:
        raise ValueError("Input text cannot be empty")

    if isinstance(texts, str):
        if not texts.strip():
            raise ValueError("Input text cannot be empty")
        client = genai.Client()
        response = _call_embedding_api(client, "text-embedding-004", texts)
        return response.embeddings[0].values
    else:
        if len(texts) == 0:
            raise ValueError("Input text cannot be empty")
        for t in texts:
            if not isinstance(t, str) or not t.strip():
                raise ValueError("Input text cannot be empty")

        client = genai.Client()
        response = _call_embedding_api(client, "text-embedding-004", texts)
        return [emb.values for emb in response.embeddings]


class SchemeIndex:
    def __init__(self, cache_path: str = "app/data/corpus/embeddings_cache.json"):
        self.cache_path = cache_path
        self.embeddings: Dict[str, List[float]] = {}
        self.schemes_map: Dict[str, Scheme] = {}

    def build_index(self, schemes: List[Scheme]):
        self.schemes_map = {s.id: s for s in schemes}

        if self._load_cache():
            missing_scheme_ids = [s.id for s in schemes if s.id not in self.embeddings]
            if not missing_scheme_ids:
                return

            missing_schemes = [self.schemes_map[sid] for sid in missing_scheme_ids]
            texts_to_embed = [self._get_scheme_text(s) for s in missing_schemes]
            new_vectors = generate_embeddings(texts_to_embed)

            if len(texts_to_embed) == 1:
                self.embeddings[missing_scheme_ids[0]] = new_vectors
            else:
                for sid, vec in zip(missing_scheme_ids, new_vectors):
                    self.embeddings[sid] = vec
            self._save_cache()
        else:
            if not schemes:
                return
            texts_to_embed = [self._get_scheme_text(s) for s in schemes]
            vectors = generate_embeddings(texts_to_embed)
            if len(schemes) == 1:
                self.embeddings[schemes[0].id] = vectors
            else:
                for s, vec in zip(schemes, vectors):
                    self.embeddings[s.id] = vec
            self._save_cache()

    def search(self, query: str, k: int = 5) -> List[Tuple[Scheme, float]]:
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        query_vector = generate_embeddings(query)
        results = []
        for sid, scheme in self.schemes_map.items():
            if sid in self.embeddings:
                sim = cosine_similarity(query_vector, self.embeddings[sid])
                results.append((scheme, sim))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]

    def _get_scheme_text(self, scheme: Scheme) -> str:
        text = f"Scheme Name: {scheme.name}. Description: {scheme.description}."
        for rule in scheme.eligibility_rules:
            text += f" Eligibility rule: {rule.explanation}."
        return text

    def _load_cache(self) -> bool:
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r") as f:
                    self.embeddings = json.load(f)
                return True
            except Exception:
                return False
        return False

    def _save_cache(self):
        if os.path.dirname(self.cache_path):
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        with open(self.cache_path, "w") as f:
            json.dump(self.embeddings, f)
