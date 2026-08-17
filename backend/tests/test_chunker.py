from app.ingestion.chunker import detect_section, split_text_by_words

def test_detect_section():
    assert detect_section("6.2.1 AMF") == ("6.2.1", "AMF")

def test_split_text():
    chunks = split_text_by_words(" ".join(["word"] * 1000), 450, 60)
    assert len(chunks) > 1
    assert all(len(x.split()) <= 450 for x in chunks)
