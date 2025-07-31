import streamlit as st
import requests
from datetime import datetime
import os
import json
import docx2txt
import PyPDF2
import pandas as pd
from bs4 import BeautifulSoup
import tempfile
from pathlib import Path
import time
import base64
from PIL import Image
import io

st.set_page_config(page_title="Long Session Chatbot", layout="wide")
st.title("🧠 Long Session Chatbot")

SESSION_FILE = Path("chat_session.json")

# Load chat history
if SESSION_FILE.exists():
    with open(SESSION_FILE, "r") as f:
        st.session_state.messages = json.load(f)
else:
    if "messages" not in st.session_state:
        st.session_state.messages = []

if "chat_ended" not in st.session_state:
    st.session_state.chat_ended = False
if "document_summary" not in st.session_state:
    st.session_state.document_summary = None
if "document_text" not in st.session_state:
    st.session_state.document_text = None
if "last_image" not in st.session_state:
    st.session_state.last_image = None

# Sidebar
model_options = ["llama3.2-vision:11b", "qwen2.5-coder:0.5b"]
selected = st.sidebar.selectbox("Choose a model:", ["Select a model..."] + model_options, index=0)

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.session_state.chat_ended = False
    st.session_state.document_summary = None
    st.session_state.document_text = None
    st.session_state.last_image = None
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()
    st.rerun()

if selected == "Select a model...":
    st.warning("Please select a model to start chatting.")
    st.stop()

model = selected

# -------------------------
# 📄 Document Upload & Summarization
# -------------------------
def extract_text(file):
    file_type = file.name.split('.')[-1].lower()
    if file_type == "pdf":
        reader = PyPDF2.PdfReader(file)
        return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    elif file_type == "docx":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name
        return docx2txt.process(tmp_path)
    elif file_type == "csv":
        df = pd.read_csv(file)
        return df.to_string()
    elif file_type == "xlsx":
        df = pd.read_excel(file)
        return df.to_string()
    elif file_type == "html":
        soup = BeautifulSoup(file.read(), "html.parser")
        return soup.get_text()
    elif file_type == "json":
        try:
            json_data = json.load(file)
            return json.dumps(json_data, indent=2)
        except Exception:
            return None
    return None

if model == "llama3.2-vision:11b":
    st.markdown("### 📄 Upload a document to summarize and ask questions")
    uploaded_file = st.file_uploader(
        "Upload PDF, DOCX, XLSX, CSV, HTML, or JSON",
        type=["pdf", "docx", "xlsx", "csv", "html", "json"],
        label_visibility="collapsed"
    )

    if uploaded_file and st.session_state.document_summary is None:
        with st.spinner("Extracting and summarizing document..."):
            raw_text = extract_text(uploaded_file)
            if raw_text:
                st.session_state.document_text = raw_text
                messages = [{"role": "user", "content": f"Summarize this document:\n{raw_text[:3000]}"}]
                try:
                    response = requests.post(
                        "http://localhost:8000/chat",
                        json={"model": model, "messages": messages}
                    )
                    result = response.json()
                    summary = result["choices"][0]["message"]["content"]
                    st.session_state.document_summary = summary
                except Exception as e:
                    summary = f"❌ Error during summarization: {e}"
                st.subheader("📝 Document Summary")
                st.markdown(summary)
            else:
                st.error("Failed to extract or parse the file.")
    elif st.session_state.document_summary:
        st.subheader("📝 Document Summary")
        st.markdown(st.session_state.document_summary)

# -------------------------
# 🖼️ Image Recognition
# -------------------------
if model == "llama3.2-vision:11b":
    st.markdown("### 🖼️ Upload an Image for Recognition")
    image_file = st.file_uploader("Upload PNG or JPG image", type=["png", "jpg", "jpeg"], key="image")

    if image_file:
        img_bytes = image_file.read()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")
        img_format = image_file.type.split("/")[-1]
        st.session_state.last_image = {
            "img_base64": img_base64,
            "format": img_format
        }

        image_prompt = st.text_input("Ask something about this image:", "What is in this image?")

        if st.button("🔍 Analyze Image"):
            with st.spinner("Analyzing image..."):
                payload = {
                    "model": model,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": image_prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/{img_format};base64,{img_base64}"
                                    }
                                }
                            ]
                        }
                    ]
                }

                try:
                    response = requests.post("http://localhost:8000/chat", json=payload)
                    result = response.json()
                    vision_reply = result["choices"][0]["message"]["content"]
                    st.image(Image.open(io.BytesIO(img_bytes)), caption="Uploaded Image", use_column_width=True)
                    st.markdown("**🧠 Model Response:**")
                    st.success(vision_reply)
                except Exception as e:
                    st.error(f"❌ Failed to process image: {e}")

# -------------------------
# 💬 Chat Interface
# -------------------------
prompt = st.chat_input("Say something... or type 'exit' to end session")

avatars = {"user": "👀", "assistant": "🧠"}
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=avatars.get(msg["role"], "💬")):
        st.markdown(f"{msg['content']}  \n*🧒 {msg.get('timestamp', '')}*")

if prompt and prompt.strip().lower() == "exit":
    st.session_state.chat_ended = True
    st.rerun()

if st.session_state.chat_ended:
    chat_text = "\n".join(
        f"{msg['role'].capitalize()} ({msg.get('timestamp', '')}): {msg['content']}"
        for msg in st.session_state.messages
    )
    st.text_area("📜 Chat Log", chat_text, height=300)
    st.download_button("⬇️ Download Chat Log", chat_text, file_name="chat_history.txt")
    st.stop()

if prompt:
    user_time = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": user_time})

    with st.chat_message("user", avatar="👀"):
        st.markdown(f"{prompt}  \n*🧒 {user_time}*")

    with st.chat_message("assistant", avatar="🧠"):
        with st.spinner("Waiting for response..."):
            start_time = time.time()
            try:
                messages = st.session_state.messages[-5:]

                system_messages = []
                if st.session_state.document_summary:
                    system_messages.append({
                        "role": "system",
                        "content": f"The user uploaded a document earlier. Here’s the summary:\n\n{st.session_state.document_summary}\n\nUse it to help answer their questions."
                    })
                elif st.session_state.document_text:
                    system_messages.append({
                        "role": "system",
                        "content": f"The user uploaded a document earlier. Here’s some content:\n\n{st.session_state.document_text[:1500]}"
                    })
                else:
                    system_messages.append({
                        "role": "system",
                        "content": "You're a helpful assistant capable of casual conversation, document summarization, and image understanding."
                    })

                if st.session_state.last_image:
                    messages = [{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{st.session_state.last_image['format']};base64,{st.session_state.last_image['img_base64']}"
                                }
                            }
                        ]
                    }]

                payload = {"model": model, "messages": system_messages + messages}
                response = requests.post("http://localhost:8000/chat", json=payload)
                result = response.json()
                reply = result["choices"][0]["message"]["content"]
                end_time = time.time()
                duration = end_time - start_time
                reply_with_time = f"{reply}\n\n⏱️ *Responded in {duration:.2f} seconds*"
            except Exception as e:
                reply_with_time = f"❌ Error: {e}"

        bot_time = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({"role": "assistant", "content": reply_with_time, "timestamp": bot_time})
        st.markdown(f"{reply_with_time}  \n*🧒 {bot_time}*")

    with open(SESSION_FILE, "w") as f:
        json.dump(st.session_state.messages, f)
