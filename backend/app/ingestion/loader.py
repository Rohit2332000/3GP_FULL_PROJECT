from pathlib import Path
from docx import Document

def load_docx(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")
    doc = Document(path)
    return [{"paragraph_id": i, "text": p.text.strip()} for i, p in enumerate(doc.paragraphs)]
