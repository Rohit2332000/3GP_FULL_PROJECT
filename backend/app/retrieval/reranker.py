from functools import lru_cache
from sentence_transformers import CrossEncoder
from app.config.settings import get_settings

@lru_cache
def get_reranker():
    return CrossEncoder(get_settings().reranker_model, max_length=512)

def rerank_results(query, candidates, top_k):
    if not candidates:
        return []
    pairs = [(query, x["text"]) for x in candidates]
    scores = get_reranker().predict(pairs, show_progress_bar=False)
    ranked = []
    for item, score in zip(candidates, scores):
        x = item.copy()
        x["reranker_score"] = float(score)
        ranked.append(x)
    ranked.sort(key=lambda x: x["reranker_score"], reverse=True)
    return ranked[:top_k]
