import pickle
from functools import lru_cache
import faiss
from app.config.settings import get_settings
from app.retrieval.embeddings import embed_query
from app.retrieval.reranker import rerank_results

ROLE_TERMS = ("role of", "functions of", "responsibilities of", "what does", "purpose of")

def expand_broad_role_query(query):
    q = query.lower()
    if "amf" in q and any(x in q for x in ROLE_TERMS):
        return f"{query} AMF general functions responsibilities registration connection reachability mobility NAS N1 N2 SMF TS 23.501 6.2.1"
    if "smf" in q and any(x in q for x in ROLE_TERMS):
        return f"{query} SMF general functions responsibilities session management PDU session TS 23.501"
    if "upf" in q and any(x in q for x in ROLE_TERMS):
        return f"{query} UPF general functions responsibilities user plane PDU session packet processing TS 23.501"
    return query

@lru_cache
def load_store():
    s = get_settings()
    if not s.faiss_path.exists() or not s.chunks_path.exists():
        raise FileNotFoundError("FAISS index not found. Run: python scripts/build_index.py")
    index = faiss.read_index(str(s.faiss_path))
    with s.chunks_path.open("rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def faiss_retrieve(query, fetch_k):
    index, chunks = load_store()
    q = embed_query(query).reshape(1, -1)
    scores, indices = index.search(q, fetch_k)
    result = []
    for score, idx in zip(scores[0], indices[0]):
        if idx >= 0:
            item = chunks[idx].copy()
            item["faiss_score"] = float(score)
            result.append(item)
    return result

def retrieve(query, fetch_k=None, top_k=None):
    s = get_settings()
    fetch_k, top_k = fetch_k or s.fetch_k, top_k or s.top_k
    retrieval_query = expand_broad_role_query(query)
    candidates = faiss_retrieve(retrieval_query, fetch_k)

    # Lightweight metadata boost: broad AMF role questions should prefer §6.2.1.
    q = query.lower()
    if "amf" in q and any(x in q for x in ROLE_TERMS):
        for x in candidates:
            if x.get("section") == "6.2.1":
                x["faiss_score"] += 0.20
            if "amf" in x.get("title", "").lower():
                x["faiss_score"] += 0.10

    return rerank_results(query, candidates, top_k)
