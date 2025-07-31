import streamlit as st
from backend import generate_marketing_content

st.set_page_config(page_title="Marketing Generator", layout="centered")

st.title("📣 Marketing Content Generator")
st.write("Generate slogans, social media posts, or email blurbs using AI.")

# User input
content_type = st.selectbox("Select Content Type", ["Slogan", "Social Media Post", "Email Blurb"])
product_name = st.text_input("Enter Product or Service Name")
description = st.text_area("Enter Description or Key Features")

if st.button("Generate"):
    if not product_name or not description:
        st.warning("Please enter both product name and description.")
    else:
        with st.spinner("Generating content..."):
            prompt = f"""
You are a creative marketing assistant.

Generate a {content_type.lower()} for the following product or service.

Product Name: {product_name}
Description: {description}

The output should be engaging, professional, and suitable for marketing.
"""
            output = generate_marketing_content(prompt)
            st.subheader(f"Generated {content_type}:")
            st.success(output)
