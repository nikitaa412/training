from vector_store_pinecone import retrieve_chunks  # or switch to weaviate
from utils import load_and_chunk, call_llm

def answer_question(file_path, question):
    chunks = load_and_chunk(file_path)
    retrieve_chunks(chunks)  # store in vector DB
    retrieved = retrieve_chunks(question, top_k=5)
    context = "\n".join([chunk['text'] for chunk in retrieved])
    prompt = f"Answer the question based on the following:\n{context}\n\nQuestion: {question}"
    return {"answer": call_llm(prompt)}
