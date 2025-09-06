
import streamlit as st
import tempfile
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.query_engine import qa_chain
import base64

import streamlit as st
from gtts import gTTS
import tempfile
import os
import sys
import base64

# Fix for importing from parent folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.query_engine import qa_chain

st.set_page_config(page_title="🧠 AI Research Assistant", layout="wide")

# Custom CSS
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

# Title
st.title("🧠 AI Research Assistant for Papers & PDFs")
st.write("Upload academic PDFs, then ask questions like 'What’s the main contribution?' or 'Summarize section 3.1.'")

st.markdown("---")

# Question input
question = st.text_input("🔎 Ask a question about your documents")

if question:
    with st.spinner("🤔 Thinking..."):
        try:
            result = qa_chain(question)
            answer = result['result']
            sources = result['source_documents']

            # Chat bubble response
            st.markdown(f"""
                <div class="assistant-bubble">
                    <div class="emoji-avatar">🗣️</div>
                    <div><strong>Assistant:</strong><br> {answer} </div>
                </div>
            """, unsafe_allow_html=True)

            # ✅ gTTS fix for Windows — safe audio playback
            tts = gTTS(answer)

            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tmp_path = tmp_file.name
            tmp_file.close()  # Close so gTTS can write to it

            tts.save(tmp_path)

            with open(tmp_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
                b64 = base64.b64encode(audio_bytes).decode()
                st.audio(f"data:audio/mp3;base64,{b64}", format="audio/mp3")

            try:
                os.remove(tmp_path)
            except Exception as e:
                st.warning(f"⚠️ Could not delete temp audio file: {e}")

            # Sources
            with st.expander("📚 Sources used in this answer"):
                for doc in sources:
                    st.markdown(f"- **File**: `{doc.metadata.get('source', 'Unknown')}`")
                    st.markdown(f"  ↳ **Section**: *{doc.metadata.get('title', 'N/A')}*")

        except Exception as e:
            st.error(f"❌ Something went wrong while generating your answer: {e}")
