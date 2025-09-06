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

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not set. Check your .env file.")

# Load FAISS vector store
print("🔍 Loading vector store...")
vectorstore = FAISS.load_local("vector_store", OpenAIEmbeddings(), allow_dangerous_deserialization=True)

# Set up retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# Load LLM
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

# Build the RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# ✅ Function to expose to your Streamlit app
def ask_question(question: str):
    if not question:
        return {
            "result": "⚠️ No question provided.",
            "source_documents": []
        }

    try:
        result = qa_chain(question)
        return result
    except Exception as e:
        return {
            "result": f"❌ Error: {e}",
            "source_documents": []
        }
