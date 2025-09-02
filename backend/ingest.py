import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.pdf_parser import parse_multiple_pdfs

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def create_vector_store(chunks, persist_path="vector_store"):
    print("🔄 Converting chunks to Document objects...")
    documents = [
        Document(
            page_content=chunk["content"],
            metadata={"title": chunk["title"], "source": chunk["source"]}
        )
        for chunk in chunks
    ]

    print("🔎 Creating embeddings...")
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

    print("📦 Creating FAISS vector store...")
    vectorstore = FAISS.from_documents(documents, embedding=embeddings)

    if not os.path.exists(persist_path):
        os.makedirs(persist_path)
    vectorstore.save_local(persist_path)
    print(f"✅ Vector store saved to: {persist_path}")


if __name__ == "__main__":
    chunks = parse_multiple_pdfs("data")
    create_vector_store(chunks)
