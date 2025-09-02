# backend/pdf_parser.py

import fitz  # PyMuPDF
import re
import os   
def extract_sections_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text_by_page = [page.get_text() for page in doc]
    full_text = "\n".join(text_by_page)
    
    # Regex pattern to identify numbered sections (e.g., 1. Introduction, 2.1 Method)
    section_pattern = r"\n(?P<title>\d+(\.\d+)*\s+[^\n]+)\n"

    matches = list(re.finditer(section_pattern, full_text))
    
    if not matches:
        return [{"title": "Full Document", "content": full_text.strip(), "source": os.path.basename(pdf_path)}]

    chunks = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(full_text)
        title = match.group("title").strip()
        content = full_text[start:end].strip()
        chunks.append({"title": title, "content": content, "source": os.path.basename(pdf_path) })
    
    return chunks


def preview_chunks(chunks, n=3):
    for i, chunk in enumerate(chunks[:n]):
        print(f"\n--- Section {i + 1}: {chunk['title']} ---")
        print(chunk['content'][:500], '...')

def parse_multiple_pdfs(folder_path="data"):
    all_chunks = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            chunks = extract_sections_from_pdf(pdf_path)
            all_chunks.extend(chunks)
    return all_chunks
#x= extract_sections_from_pdf("data/AB Testing.pdf")
#print(preview_chunks(x))