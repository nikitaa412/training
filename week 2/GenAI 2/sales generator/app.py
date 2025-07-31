import streamlit as st
import requests

# Page settings
st.set_page_config(page_title="Sales Content Generator", layout="wide")
st.title("💼 AI Sales Content Generator")
st.sidebar.title("🛠️ Sales Content Options")

# Sidebar Inputs
content_type = st.sidebar.selectbox("Content Type", [
    "Sales Pitch", 
    "Follow-Up Email", 
    "Cold Outreach", 
    "Objection Handling", 
    "Upsell Message"
])

tone = st.sidebar.selectbox("Tone", [
    "Confident", 
    "Friendly", 
    "Persuasive", 
    "Urgent", 
    "Empathetic"
])

length = st.sidebar.selectbox("Length", [
    "Short", 
    "Medium", 
    "Long"
])

sales_context = st.sidebar.text_area("Enter Sales Context", 
    placeholder="Describe the product/service and the sales scenario...", height=150)

# Action button
if st.sidebar.button("Generate Sales Content"):
    with st.spinner("Generating sales content..."):
        prompt = (
            f"Write a {length.lower()} {content_type.lower()} in a {tone.lower()} tone "
            f"based on the following sales scenario:\n\n{sales_context}"
        )
        
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
            generated_text = result.get("response", "⚠️ No response from the model.")
            st.subheader("📄 Generated Sales Content")
            st.write(generated_text)
        except Exception as e:
            st.error(f"❌ Error generating content: {e}")
