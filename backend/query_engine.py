# backend/query_engine.py

import os
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not set. Check your .env file.")

# Load FAISS vector store
print("🔍 Loading vector store...")
vectorstore = FAISS.load_local("vector_store", OpenAIEmbeddings(), allow_dangerous_deserialization=True)

# Set up retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# Load LLM
llm = ChatOpenAI(model_name="gpt-4.1-mini", temperature=0)

# Build RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# --- Interactive loop ---
print("\n🤖 Ask a question about your PDFs (type 'exit' to quit)\n")

while True:
    query = input("🔎 You: ")
    if query.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break

    result = qa_chain(query)
    answer = result["result"]
    sources = result["source_documents"]

    print("\n🧠 Answer:")
    print(answer)

    print("\n📚 Sources:")
    for doc in sources:
        print(f" - {doc.metadata.get('source')} | Section: {doc.metadata.get('title')}")
    print("\n" + "-"*50 + "\n")
