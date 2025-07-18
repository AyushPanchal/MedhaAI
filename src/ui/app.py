# src/ui/app.py

import time
import streamlit as st
import requests
from langchain_core.messages import HumanMessage, AIMessage
from fpdf import FPDF
from streamlit.components.v1 import html
# --- Page Config ---
st.set_page_config(page_title="MedhaAI - SVNIT Chatbot", page_icon="🤖")

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ MedhaAI Settings")

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    if st.button("📄 Export Chat as PDF"):
        def export_chat_to_pdf(chat_history):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for msg in chat_history:
                role = "User" if isinstance(msg, HumanMessage) else "Medha"
                pdf.multi_cell(0, 10, f"{role}: {msg.content}\n", align='L')
            pdf.output("medha_chat.pdf")


        export_chat_to_pdf(st.session_state.chat_history)
        st.success("✅ Chat saved as `medha_chat.pdf`")

# --- Title ---
st.title("🤖 MedhaAI - SVNIT Chatbot")
st.markdown("###### Hello! I'm Medha, your helpful assistant for the Computer Science Department at SVNIT Surat.")

# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Display Chat History ---
for msg in st.session_state.chat_history:
    with st.chat_message("user" if isinstance(msg, HumanMessage) else "ai"):
        st.markdown(msg.content)

# --- Input Box ---
user_input = st.chat_input("Ask me anything about SVNIT CSE...")

# --- Process Input ---
if user_input:
    st.chat_message("user").markdown(user_input)

    # Convert LangChain messages to dicts for API
    formatted_history = [
        {"type": "human" if isinstance(m, HumanMessage) else "ai", "content": m.content}
        for m in st.session_state.chat_history
    ]

    # Send request to FastAPI
    try:
        with st.spinner("Medha is thinking..."):
            res = requests.post("http://127.0.0.1:8000/query", json={
                "query": user_input,
                "chat_history": formatted_history
            })
            res.raise_for_status()
            answer = res.json()["answer"]
    except Exception as e:
        answer = "❌ Sorry, there was an error: " + str(e)

    # Live typing animation
    with st.chat_message("ai"):
        placeholder = st.empty()
        typed = ""
        for char in answer:
            typed += char
            placeholder.markdown(typed)
            time.sleep(0.015)

    # Update chat history
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.chat_history.append(AIMessage(content=answer))
