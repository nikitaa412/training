import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import requests

# Load components
G, nodes, node_texts = pickle.load(open("nodes.pkl", "rb"))
index = faiss.read_index("index.faiss")
embedder = SentenceTransformer("mxbai-embed-large")

def retrieve_nodes(query, top_k=2):
    q_emb = embedder.encode([query], normalize_embeddings=True)
    D, I = index.search(np.array(q_emb), top_k)
    return [nodes[i] for i in I[0]]

def build_prompt(query, relevant_nodes):
    context_lines = []
    for node in relevant_nodes:
        for succ in G.successors(node):
            edge = G.edges[node, succ]
            context_lines.append(f"{node} {edge['relation']} {succ} (year: {edge.get('year')})")
    context = "\n".join(context_lines)
    return f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

def generate_answer(prompt):
    payload = {
        "model": "deepseek-r1:1.5b",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post("http://localhost:11434/api/generate", json=payload)
    return response.json()["response"]

# Example usage
query = "What did Einstein do in 1905?"
nodes = retrieve_nodes(query)
prompt = build_prompt(query, nodes)
response = generate_answer(prompt)

print("Answer:", response)
