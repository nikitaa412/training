import streamlit as st
from chatbot_chain import get_chatbot_chain

st.set_page_config(page_title="VSoft Consulting Chatbot", layout="wide")

# --- CSS Styling ---
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #f0f0f0;
    }

    .welcome-text {
        font-size: 48px;
        font-weight: bold;
        margin-bottom: 0;
        color: black;
    }

    .ask-text {
        font-size: 20px;
        margin-top: 5px;
        color: black;
    }

    .input-label {
        color: black !important;
        font-weight: 600;
        margin-bottom: 4px;
    }

    /* Ensure input text stays black always */
    input[type="text"],
    .stTextInput input,
    .stTextInput input:focus,
    .stTextInput input:hover {
        background-color: white !important;
        color: black !important;
        caret-color: black !important;
    }

    input::placeholder {
        color: gray !important;
    }

    h3 {
        color: black !important;
    }

    .response-text {
        color: black !important;
        font-size: 16px;
    }

    .details-text {
        color: black !important;
        font-size: 14px;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    .stSpinner > div > div {
        color: black !important;
    }
    </style>

    <script>
    // JS fallback: ensure input text stays black after rerender
    const observer = new MutationObserver(() => {
        document.querySelectorAll('input[type="text"]').forEach(input => {
            input.style.color = 'black';
            input.style.backgroundColor = 'white';
            input.style.caretColor = 'black';
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """,
    unsafe_allow_html=True
)


# --- Logo and Header ---
col1, col2 = st.columns([8, 1])
with col2:
    st.image("V-soft-logo.png", width=180)

st.markdown('<p class="welcome-text">Welcome to VSoft Chatbot</p>', unsafe_allow_html=True)
st.markdown('<p class="ask-text">💡 Ask Me Anything About VSoft Consulting</p>', unsafe_allow_html=True)
st.markdown("---")

# --- Initialize session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Display chat history ---
for i, (user_msg, bot_msg) in enumerate(st.session_state.chat_history):
    st.markdown(f"**💬 You:** {user_msg}")
    st.markdown(f'<div class="response-text">🤖 <b>VSoft:</b> {bot_msg}</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <p class="details-text">
            For more details, go to 
            <a href="https://www.vsoftconsulting.com/" target="_blank" style="color: blue; text-decoration: underline;">
                https://www.vsoftconsulting.com/
            </a>
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# --- New question input without a button ---
st.markdown('<p class="input-label">Enter your question about VSoft:</p>', unsafe_allow_html=True)

# Dynamically create a key to prevent duplication during reruns
user_input_key = f"user_input_{len(st.session_state.chat_history)}"

query = st.text_input(
    "",
    key=user_input_key,
    placeholder="Type your question and press Enter...",
    label_visibility="collapsed"
)

# Check and respond if query is entered
if query:
    with st.spinner("Waiting for response..."):
        chain = get_chatbot_chain()
        response = chain.run(query)

    # Save the query and response to history
    st.session_state.chat_history.append((query, response))

    # Rerun to display updated chat
    st.rerun()

