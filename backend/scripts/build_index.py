from app.config.settings import get_settings
from app.ingestion.indexer import build_index

if __name__ == "__main__":
    s = get_settings()
    if not s.document_file.exists():
        raise FileNotFoundError(f"Put 23501-j80.docx at: {s.document_file}")
    result = build_index(s.document_file, s.index_dir)
    print("=" * 70)
    print("3GPP FAISS INDEX CREATED")
    print("=" * 70)
    for k, v in result.items():
        print(f"{k}: {v}")
