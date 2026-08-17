from pathlib import Path
import pickle
import faiss
from app.ingestion.loader import load_docx
from app.ingestion.chunker import build_chunks
from app.retrieval.embeddings import embed_documents

def build_index(document_path: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    paragraphs = load_docx(document_path)
    chunks = build_chunks(paragraphs, document_path.name)
    texts = [
        f"3GPP TS 23.501\nSection: {x['section']}\nTitle: {x['title']}\n\n{x['text']}"
        for x in chunks
    ]
    embeddings = embed_documents(texts)
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    faiss_path, chunks_path = output_dir / "index.faiss", output_dir / "chunks.pkl"
    faiss.write_index(index, str(faiss_path))
    with chunks_path.open("wb") as f:
        pickle.dump(chunks, f)
    return {"paragraphs": len(paragraphs), "chunks": len(chunks),
            "vectors": index.ntotal, "dimension": index.d,
            "faiss_path": str(faiss_path), "chunks_path": str(chunks_path)}
