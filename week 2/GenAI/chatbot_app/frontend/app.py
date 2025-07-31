import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Long Session Chatbot", layout="wide")
st.title("🧠 Long Session Chatbot")

# Sidebar UI
model_options = ["llama3.2-vision:11b", "qwen2.5-coder:0.5b"]
selected = st.sidebar.selectbox(
    "Choose a model:", ["Select a model..."] + model_options, index=0
)
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.session_state.chat_ended = False
    st.rerun()

# Stop if model not selected
if selected == "Select a model...":
    st.warning("Please select a model to start chatting.")
    st.stop()

model = selected

# Init session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_ended" not in st.session_state:
    st.session_state.chat_ended = False

# Chat input
prompt = st.chat_input("Say something... or type 'exit' to end session")

# Display messages
avatars = {"user": "👀", "assistant": "🤖"}
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=avatars.get(msg["role"], "💬")):
        st.markdown(f"{msg['content']}  \n*🕒 {msg.get('timestamp', '')}*")

# Handle chat end
if prompt and prompt.strip().lower() == "exit":
    st.session_state.chat_ended = True
    st.rerun()

# After end of chat, show download
if st.session_state.chat_ended:
    st.markdown("💬 **Chat session has ended.**")
    st.markdown("Here's your full conversation:")

    chat_text = "\n".join([
        f"{msg['role'].capitalize()} ({msg.get('timestamp', '')}): {msg['content']}"
        for msg in st.session_state.messages
    ])
    st.text_area("Chat Log", chat_text, height=300)

    st.download_button("📥 Download Chat Log", chat_text, file_name="chat_history.txt")
    st.stop()

# On new prompt
if prompt:
    user_time = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": user_time})

    with st.chat_message("user", avatar="👀"):
        st.markdown(f"{prompt}  \n*🕒 {user_time}*")

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Waiting for response..."):
            try:
                response = requests.post(
                    "http://localhost:8000/chat",
                    json={"model": model, "messages": st.session_state.messages}
                )
                result = response.json()
                reply = result["choices"][0]["message"]["content"]
            except Exception as e:
                reply = f"❌ Error: {e}"

            bot_time = datetime.now().strftime("%H:%M:%S")
            st.session_state.messages.append({"role": "assistant", "content": reply, "timestamp": bot_time})
            st.markdown(f"{reply}  \n*🕒 {bot_time}*")
