from utils import load_and_chunk, call_llm

def summarize_document(file_path):
    chunks = load_and_chunk(file_path)
    content = "\n".join([c['text'] for c in chunks])
    prompt = f"Summarize the following document:\n{content}"
    return {"summary": call_llm(prompt)}
