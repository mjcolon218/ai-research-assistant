import streamlit as st
#from backend.query_engine import qa_chain
#from gtts import gTTS
import tempfile
import base64

st.set_page_config(page_title="🧠 AI Research Assistant", layout="wide")

st.markdown("""
    <style>
    .assistant-bubble {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 1.2rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: flex-start;
    }
    .emoji-avatar {
        font-size: 2.5rem;
        margin-right: 1rem;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.6; }
        100% { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 AI Research Assistant for Papers & PDFs")
st.write("Upload academic PDFs, then ask questions like 'What’s the main contribution?' or 'Summarize section 3.1.'")

st.markdown("---")

# User input
question = st.text_input("🔎 Ask a question about your documents")

if question:
    with st.spinner("🤔 Thinking..."):
        result = qa_chain(question)
        answer = result['result']
        sources = result['source_documents']

        st.markdown("""
            <div class="assistant-bubble">
                <div class="emoji-avatar">🗣️</div>
                <div><strong>Assistant:</strong><br> {} </div>
            </div>
        """.format(answer), unsafe_allow_html=True)

        # Text-to-speech using gTTS
        tts = gTTS(answer)
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as tmp_file:
            tts.save(tmp_file.name)
            with open(tmp_file.name, "rb") as audio_file:
                audio_bytes = audio_file.read()
                b64 = base64.b64encode(audio_bytes).decode()
                st.audio(f"data:audio/mp3;base64,{b64}", format="audio/mp3")

        with st.expander("📚 Sources used in this answer"):
            for doc in sources:
                st.markdown(f"- **File**: `{doc.metadata.get('source', 'Unknown')}`  ")
                st.markdown(f"  ↳ **Section**: *{doc.metadata.get('title', 'N/A')}*\n")
