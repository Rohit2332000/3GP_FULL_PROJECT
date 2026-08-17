import re

SECTION_PATTERN = re.compile(r"^(\d+(?:\.\d+)*(?:[a-z])?)\s+(.+?)$")

def detect_section(text: str):
    m = SECTION_PATTERN.match(text.strip())
    if not m or len(m.group(2).strip()) > 150:
        return None
    return m.group(1), m.group(2).strip()

def find_document_start(paragraphs):
    positions = [
        i for i, p in enumerate(paragraphs)
        if p["text"].strip() in {"1\tScope", "1 Scope", "1\tScope\t25"}
    ]
    if len(positions) < 2:
        raise ValueError("Could not reliably identify the actual document start.")
    return positions[1]

def extract_sections(paragraphs):
    sections, current_text = [], []
    current_section = current_title = "unknown"
    current_start = None

    for p in paragraphs:
        text = p["text"].strip()
        if not text:
            continue
        detected = detect_section(text)
        if detected:
            if current_text:
                sections.append({
                    "section": current_section,
                    "title": current_title,
                    "paragraph_start": current_start,
                    "paragraph_end": p["paragraph_id"] - 1,
                    "text": "\n".join(current_text),
                })
            current_section, current_title = detected
            current_text = [text]
            current_start = p["paragraph_id"]
        elif current_start is not None:
            current_text.append(text)

    if current_text:
        sections.append({
            "section": current_section,
            "title": current_title,
            "paragraph_start": current_start,
            "paragraph_end": paragraphs[-1]["paragraph_id"],
            "text": "\n".join(current_text),
        })
    return sections

def split_text_by_words(text, max_words=450, overlap_words=60):
    words = text.split()
    if len(words) <= max_words:
        return [text]
    chunks, start = [], 0
    while start < len(words):
        end = min(start + max_words, len(words))
        chunks.append(" ".join(words[start:end]))
        if end >= len(words):
            break
        start = end - overlap_words
    return chunks

def build_chunks(paragraphs, source_name, max_words=450, overlap_words=60):
    actual = paragraphs[find_document_start(paragraphs):]
    sections = extract_sections(actual)
    result, chunk_id = [], 0
    for section in sections:
        for piece in split_text_by_words(section["text"], max_words, overlap_words):
            result.append({
                "chunk_id": chunk_id,
                "source": source_name,
                "section": section["section"],
                "title": section["title"],
                "paragraph_start": section["paragraph_start"],
                "paragraph_end": section["paragraph_end"],
                "text": piece,
            })
            chunk_id += 1
    return result
