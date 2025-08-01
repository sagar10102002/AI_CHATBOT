import streamlit as st
from PIL import Image
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os

# ========== Setup API Keys ==========
os.environ["OPENAI_API_KEY"] = "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"  # REPLACE THIS
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

# ========== Page Configuration ==========
st.set_page_config(page_title="AI Assistant", layout="wide")

# ========== Load Avatar ==========
avatar_path = "IMG_20240320_194823_406.png"
if os.path.exists(avatar_path):
    avatar = Image.open(avatar_path)
else:
    avatar = None

# ========== Header ==========
col1, col2 = st.columns([8, 1])
with col1:
    st.markdown("## 🤖 LangChain AI Assistant")
    st.markdown("Ask any question and get real-time answers powered by OpenRouter + LangChain.")
with col2:
    if avatar:
        st.image(avatar, width=70)

st.markdown("---")

# ========== Sidebar ==========
with st.sidebar:
    st.markdown("### 📌 Settings")
    uploaded_file = st.file_uploader("Upload a document (optional)", type=["pdf", "txt", "md"])

# ========== LLM Setup ==========
llm = ChatOpenAI(
    model_name="openai/gpt-3.5-turbo",  # or "mistralai/mixtral-8x7b"
    temperature=0,
)

# ========== Session Chat History ==========
if "messages" not in st.session_state:
    st.session_state.messages = []

# ========== User Chat ==========
user_input = st.chat_input("Ask your question here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        response = llm.invoke([HumanMessage(content=user_input)])
    st.session_state.messages.append({"role": "assistant", "content": response.content})

# ========== Display Chat ==========
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
