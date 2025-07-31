import streamlit as st
import requests

# Page config
st.set_page_config(page_title="👨‍💻 AI Coding Assistant", layout="wide")
st.title("👨‍💻 Qwen2.5-Coder: AI Coding Assistant")

# Sidebar options
st.sidebar.title("Assistant Settings")
language = st.sidebar.selectbox("Programming Language", ["Python", "JavaScript", "C++", "Java", "Go", "Rust", "Other"])
code_goal = st.sidebar.text_area("What do you want to do?", placeholder="E.g., Write a function to reverse a linked list", height=150)

# Button trigger
if st.sidebar.button("Generate Code"):
    if not code_goal.strip():
        st.error("Please describe your coding task.")
    else:
        prompt = (
            f"You are a helpful coding assistant. Please write code in {language} to do the following task:\n\n{code_goal}\n\n"
            f"Include comments and best practices."
        )

        with st.spinner("Asking Qwen2.5-Coder..."):
            try:
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "qwen2.5-coder:0.5b",
                        "prompt": prompt,
                        "stream": False
                    }
                )
                result = response.json()
                answer = result.get("response", "⚠️ No output generated.")
                st.subheader("💡 Suggested Code")
                st.code(answer, language=language.lower() if language != "Other" else "text")
            except Exception as e:
                st.error(f"❌ Error from model: {e}")
