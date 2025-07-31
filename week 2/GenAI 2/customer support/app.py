import streamlit as st
import requests

# Page setup
st.set_page_config(page_title="🛎️ AI Customer Support", layout="wide")
st.title("🛎️ AI Customer Support Assistant")

# Session state to maintain conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Intro message
if len(st.session_state.messages) == 0:
    st.session_state.messages.append({"role": "assistant", "content": "Hi there! How can I assist you today?"})

# Chat UI display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input area for user
user_input = st.chat_input("Type your support question here...")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare prompt for the model
    prompt = (
        "You are a helpful and polite customer support agent. Respond to the following user query:\n\n"
        f"{user_input}\n\n"
        "Provide concise, friendly, and accurate information."
    )

    try:
        # Query Qwen model
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5-coder:0.5b",
                "prompt": prompt,
                "stream": False
            }
        )
        result = response.json()
        reply = result.get("response", "⚠️ Sorry, I'm having trouble understanding that.")

    except Exception as e:
        reply = f"❌ Sorry, an error occurred: {e}"

    # Show assistant message
    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})