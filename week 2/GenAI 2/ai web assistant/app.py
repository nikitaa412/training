import streamlit as st
import requests
import json
from pathlib import Path

# Set up page
st.set_page_config(page_title="Unified AI Assistant", layout="wide")
st.title("🤖 Unified AI Assistant")

# Sidebar navigation
st.sidebar.title("🧭 Select Assistant")
option = st.sidebar.selectbox("Choose a feature:", ["Marketing", "Sales", "Coding", "Customer Support"])

# Model config
MODEL_NAME = "qwen2.5-coder:0.5b"
OLLAMA_API = "http://localhost:11434/api/generate"

# Persistent session memory
HISTORY_FILES = {
    "Marketing": Path("marketing_history.json"),
    "Sales": Path("sales_history.json"),
    "Coding": Path("coding_history.json"),
    "Customer Support": Path("support_history.json"),
}

def load_history(assistant):
    path = HISTORY_FILES[assistant]
    if path.exists():
        return json.loads(path.read_text())
    return []

def save_history(assistant, history):
    path = HISTORY_FILES[assistant]
    path.write_text(json.dumps(history, indent=2))

# Model call helper
def generate_response(prompt):
    try:
        response = requests.post(
            OLLAMA_API,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False}
        )
        return response.json().get("response", "⚠️ No response.")
    except Exception as e:
        return f"❌ Error: {e}"

# Prompt formatter
def format_chat_history(history):
    prompt = ""
    for msg in history:
        if msg["role"] == "user":
            prompt += f"User: {msg['content']}\n"
        elif msg["role"] == "assistant":
            prompt += f"Assistant: {msg['content']}\n"
    prompt += "Assistant:"
    return prompt

# -------------------------
# 📢 MARKETING ASSISTANT
# -------------------------
if option == "Marketing":
    st.header("📢 Marketing Content Generator")
    if "marketing_history" not in st.session_state:
        st.session_state.marketing_history = load_history("Marketing")

    content_type = st.selectbox("Content Type", ["Product Description", "Ad Copy", "Social Media Post", "Email Campaign"])
    tone = st.selectbox("Tone", ["Professional", "Persuasive", "Excited", "Casual"])
    length = st.selectbox("Length", ["Short", "Medium", "Long"])
    product_info = st.text_area("Enter Product/Service Info", height=150)

    if st.button("Generate Marketing Content"):
        if not product_info.strip():
            st.warning("Please provide product/service info.")
        else:
            user_msg = f"Write a {length.lower()} {content_type.lower()} in a {tone.lower()} tone for the following:\n\n{product_info}"
            st.session_state.marketing_history.append({"role": "user", "content": user_msg})
            full_prompt = format_chat_history(st.session_state.marketing_history)

            with st.spinner("Generating response..."):
                reply = generate_response(full_prompt)

            st.session_state.marketing_history.append({"role": "assistant", "content": reply})
            save_history("Marketing", st.session_state.marketing_history)
            st.subheader("📝 Output")
            st.write(reply)

# -------------------------
# 💼 SALES ASSISTANT
# -------------------------
elif option == "Sales":
    st.header("💼 Sales Content Generator")
    if "sales_history" not in st.session_state:
        st.session_state.sales_history = load_history("Sales")

    content_type = st.selectbox("Content Type", ["Sales Pitch", "Follow-Up Email", "Cold Outreach", "Objection Handling", "Upsell Message"])
    tone = st.selectbox("Tone", ["Confident", "Friendly", "Persuasive", "Urgent", "Empathetic"])
    length = st.selectbox("Length", ["Short", "Medium", "Long"])
    context = st.text_area("Enter Sales Context", height=150)

    if st.button("Generate Sales Content"):
        if not context.strip():
            st.warning("Please enter a sales scenario.")
        else:
            user_msg = f"Write a {length.lower()} {content_type.lower()} in a {tone.lower()} tone based on the following sales context:\n\n{context}"
            st.session_state.sales_history.append({"role": "user", "content": user_msg})
            full_prompt = format_chat_history(st.session_state.sales_history)

            with st.spinner("Generating response..."):
                reply = generate_response(full_prompt)

            st.session_state.sales_history.append({"role": "assistant", "content": reply})
            save_history("Sales", st.session_state.sales_history)
            st.subheader("📄 Output")
            st.write(reply)

# -------------------------
# 👨‍💻 CODING ASSISTANT
# -------------------------
elif option == "Coding":
    st.header("👨‍💻 Coding Assistant")
    if "coding_history" not in st.session_state:
        st.session_state.coding_history = load_history("Coding")

    language = st.selectbox("Programming Language", ["Python", "JavaScript", "C++", "Java", "Go", "Rust", "Other"])
    task = st.text_area("Describe the coding task", height=150)

    if st.button("Generate Code"):
        if not task.strip():
            st.warning("Please describe your coding task.")
        else:
            user_msg = f"You are a helpful coding assistant. Write {language} code for the following task:\n\n{task}\n\nUse best practices and add comments."
            st.session_state.coding_history.append({"role": "user", "content": user_msg})
            full_prompt = format_chat_history(st.session_state.coding_history)

            with st.spinner("Generating response..."):
                reply = generate_response(full_prompt)

            st.session_state.coding_history.append({"role": "assistant", "content": reply})
            save_history("Coding", st.session_state.coding_history)
            st.subheader("💡 Code Output")
            st.code(reply, language=language.lower() if language != "Other" else "text")

# -------------------------
# 🛎️ CUSTOMER SUPPORT ASSISTANT
# -------------------------
elif option == "Customer Support":
    st.header("🛎️ Customer Support Chat")
    if "support_history" not in st.session_state:
        st.session_state.support_history = load_history("Customer Support")
        if not st.session_state.support_history:
            st.session_state.support_history.append({"role": "assistant", "content": "Hi! How can I help you today?"})

    # Show previous chat
    for msg in st.session_state.support_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Type your question here...")

    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.support_history.append({"role": "user", "content": user_input})

        full_prompt = format_chat_history(st.session_state.support_history)

        with st.spinner("Generating response..."):
            reply = generate_response(full_prompt)

        st.session_state.support_history.append({"role": "assistant", "content": reply})
        save_history("Customer Support", st.session_state.support_history)
        st.chat_message("assistant").markdown(reply)
