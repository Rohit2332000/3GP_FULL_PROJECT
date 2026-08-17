from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    groq_api_key: str
    generation_model: str = "llama-3.3-70b-versatile"
    generation_temperature: float = 0.0
    evaluation_model: str = "openai/gpt-oss-20b"
    evaluation_temperature: float = 0.0
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    fetch_k: int = 15
    top_k: int = 3
    max_iterations: int = 1
    min_accept_score: float = 0.90
    min_faithfulness: float = 0.80
    min_relevance: float = 0.70
    document_path: str = "data/raw/3gpp/23501-j80.docx"
    vector_store_dir: str = "data/indexes/faiss"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def document_file(self): return BASE_DIR / self.document_path
    @property
    def index_dir(self): return BASE_DIR / self.vector_store_dir
    @property
    def faiss_path(self): return self.index_dir / "index.faiss"
    @property
    def chunks_path(self): return self.index_dir / "chunks.pkl"

@lru_cache
def get_settings():
    return Settings()
