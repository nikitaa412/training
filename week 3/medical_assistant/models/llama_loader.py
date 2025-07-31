from langchain_community.chat_models import ChatOllama

def load_llama():
    return ChatOllama(
        model="llama3.2-vision:11b",
        temperature=0,
        base_url="http://localhost:11434"
    )