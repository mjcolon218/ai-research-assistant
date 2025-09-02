from backend.pdf_parser import parse_multiple_pdfs, preview_chunks

chunks = parse_multiple_pdfs("data")
for i, chunk in enumerate(chunks[:10]):
    print(f"✅ Chunk {i+1} keys: {chunk.keys()}")
    assert "source" in chunk, "❌ Missing 'source' key!"
