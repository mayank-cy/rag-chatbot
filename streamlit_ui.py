
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from embeddings import (
    load_embeddings_and_index,
    retrieve_context_from_query,
    filter_results,
    build_context
)
from llm_utils import get_llm_response

# --- Page config ---
st.set_page_config(page_title="RAG Chatbot", layout="wide")

st.title("📄 RAG Chatbot")

# --- Load embeddings once ---
@st.cache_resource
def load_data():
    return load_embeddings_and_index()

index, chunks = load_data()

# --- Session state for chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- User input ---
user_query = st.chat_input("Ask something about the document...")

if user_query:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)

    # --- RAG pipeline ---
    with st.spinner("Thinking..."):
        retrieved_context = retrieve_context_from_query(user_query, index, chunks)
        filtered = filter_results(retrieved_context)
        context = build_context(filtered, max_chunks=3)

        response = get_llm_response(user_query, context)
        answer = response["content"]

    # Show assistant response
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)

    # Optional: expandable context
    with st.expander("🔍 Retrieved Context"):
        st.write(context)