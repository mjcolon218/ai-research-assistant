from backend.pdf_parser import parse_multiple_pdfs, preview_chunks
from dotenv import load_dotenv
import os
#chunks = parse_multiple_pdfs("data")
#for c in chunks[:5]:
#    print(c.keys())  # Should include 'title', 'content', 'source'
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)