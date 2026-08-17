from functools import lru_cache
import numpy as np
from sentence_transformers import SentenceTransformer
from app.config.settings import get_settings

@lru_cache
def get_embedding_model():
    return SentenceTransformer(get_settings().embedding_model)

def embed_documents(texts):
    return get_embedding_model().encode(
        texts, convert_to_numpy=True, normalize_embeddings=True,
        show_progress_bar=False
    ).astype("float32")

def embed_query(query):
    return get_embedding_model().encode(
        [query], convert_to_numpy=True, normalize_embeddings=True,
        show_progress_bar=False
    )[0].astype("float32")
